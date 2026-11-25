#!/usr/bin/env python3
"""
Adapter 5: Gemeinde-Homepage ohne Ratsinformationssystem (typ = "homepage")
===========================================================================

Für Gemeinden, bei denen kein RIS gefunden wurde. Der Crawler startet auf der Homepage und
folgt nur Links zu Bekanntmachungen, Amtsblatt, Bauleitplanung und Beteiligung (maximal
zwei Ebenen, wenige Seiten je Gemeinde). Seiten und PDFs mit PV-Bezug und Planungsbezug
werden im selben Format wie bei den anderen Adaptern geliefert.

Grenzen
  * Best effort: Jede Gemeinde baut ihre Seite anders. Es gibt keinen Zugriff auf Beschlüsse
    nicht öffentlicher Sitzungen, und viele Gemeinden veröffentlichen nur die Bekanntmachung
    (Auslegung), nicht den Aufstellungsbeschluss selbst. Der Beschlusstyp wird heuristisch erkannt.
  * robots.txt und die Pause pro Server gelten (Http aus pv_beschluesse).
  * Amtsblätter als PDF werden gelesen, soweit sie ohne Anmeldung abrufbar sind.
"""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

FOLGEN = re.compile(
    r"bekanntmach|amtsblatt|mitteilungsblatt|bauleit|bebauungsplan|b-plan|bplan|flaechennutzung|"
    r"flächennutzung|oeffentliche-?bekannt|öffentliche|beteiligung|auslegung|planung|bauen|"
    r"bekanntgabe|aktuelles|neuigkeiten|nachrichten|solar|photovoltaik|energie|ortsrecht|satzung", re.I)
PV_URL = re.compile(r"solar|photovoltaik|pv-?park|freiflaech|freifläch", re.I)
SKIP = re.compile(r"\.(png|jpe?g|gif|svg|css|js|ico|woff2?|zip|mp4|docx?|xlsx?)(\?|$)|mailto:|tel:", re.I)
MAX_SEITEN = 20
MAX_TIEFE = 2
# Gemeinden mit bekanntem Solarpark (MaStR): tiefer suchen
MAX_SEITEN_TIEF = 70
MAX_TIEFE_TIEF = 3
SUCHE = ("/?s={q}", "/suche?q={q}", "/search?q={q}", "/suche?searchterm={q}", "/suche.html?q={q}")


def _park_namen(hinweis: str) -> list[str]:
    m = re.search(r"park=([^|]*)", hinweis or "")
    namen = [x.strip() for x in (m.group(1).split(";") if m else []) if x.strip()]
    return namen[:4]


def _sitemap_treffer(http, basis: str, tokens: list[str]) -> list[str]:
    """URLs aus sitemap.xml, die nach Solar/PV/Bauleitplanung oder dem Parknamen aussehen."""
    out: list[str] = []
    for pfad in ("/sitemap.xml", "/sitemap_index.xml"):
        try:
            xml = http.get(basis.rstrip("/") + pfad, cache=False)
        except Exception:  # noqa: BLE001
            continue
        for u in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)[:5000]:
            low = u.lower()
            if u.endswith(".xml"):
                continue
            if PV_URL.search(low) or re.search(r"bebauungsplan|bauleit|b-plan|bekanntmach", low) \
                    or any(t.lower().replace(" ", "-") in low for t in tokens):
                out.append(u)
    return out[:40]


def homepage_vorlagen(http, q, seit: str | None, zustand=None):
    import pv_beschluesse as pv  # lazy, vermeidet Zirkelimport

    gemeinde = q.name.replace(" [MaStR]", "")
    host = urlparse(q.url).netloc.removeprefix("www.")
    queue: list[tuple[str, int]] = [(q.url, 0)]
    gesehen: set[str] = set()
    treffer = 0
    tief = q.typ.lower() == "homepage_mastr"
    max_seiten = MAX_SEITEN_TIEF if tief else MAX_SEITEN
    max_tiefe = MAX_TIEFE_TIEF if tief else MAX_TIEFE
    if tief:
        from urllib.parse import quote
        namen = _park_namen(getattr(q, "hinweis", ""))
        basis = f"{urlparse(q.url).scheme}://{urlparse(q.url).netloc}"
        for u in _sitemap_treffer(http, basis, namen):
            queue.insert(0, (u, 1))
        for term in ["Solarpark", "Photovoltaik"] + namen:
            for muster in SUCHE[:3]:
                queue.append((basis + muster.format(q=quote(term)), 1))
    while queue and len(gesehen) < max_seiten:
        url, tiefe = queue.pop(0)
        url = url.split("#")[0]
        if url in gesehen or SKIP.search(url):
            continue
        gesehen.add(url)
        ist_pdf = bool(re.search(r"\.pdf(\?|$)", url, re.I))
        try:
            if ist_pdf:
                text = pv.dokument_text(http, url)
                soup = None
            else:
                html = http.get(url, cache=False)
                soup = BeautifulSoup(html, "html.parser")
                text = pv.html_text(html)
                if len(text) < 200 and soup.find("script"):
                    gerendert = http.render(url)
                    if gerendert:
                        html = gerendert
                        soup = BeautifulSoup(html, "html.parser")
                        text = pv.html_text(html)
        except PermissionError:
            continue
        except Exception:  # noqa: BLE001
            continue
        if soup is not None and tiefe < max_tiefe:
            for a in soup.find_all("a", href=True):
                absu = urljoin(url, a["href"]).split("#")[0]
                h = urlparse(absu).netloc.removeprefix("www.")
                if absu in gesehen or SKIP.search(absu) or h != host:
                    continue
                label = a.get_text(" ", strip=True)
                if PV_URL.search(absu + " " + label):
                    queue.insert(0, (absu, tiefe + 1))      # PV-Links zuerst
                elif FOLGEN.search(absu) or FOLGEN.search(label):
                    queue.append((absu, tiefe + 1))
        if url == q.url or (soup is not None and len(soup.find_all("a")) > 40):
            continue   # Startseite und Listen-/Übersichtsseiten sind keine Einzelmitteilung
        titel = ""
        if soup is not None:
            t = soup.find("h1") or soup.find("title")
            titel = t.get_text(" ", strip=True)[:300] if t else ""
        if not pv.PV_RE.search(titel + "\n" + text[:6000]) or not pv.PLANUNG_RE.search(text[:20000]):
            continue
        if zustand and zustand.hat(url):
            continue
        datum = pv.erstes_datum(text)
        if seit and datum and datum < seit:
            continue
        treffer += 1
        http.zaehle("Homepage: Treffer")
        yield {"titel": titel or f"{gemeinde}: Bekanntmachung", "datum": datum,
               "text": f"{gemeinde}\n{text[:20000]}", "link": url,
               "dokument_link": url if ist_pdf else "", "body_name": gemeinde, "schluessel": url}
    http.zaehle(f"Homepage: {len(gesehen)} Seiten geprüft")

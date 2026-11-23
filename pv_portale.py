#!/usr/bin/env python3
"""
Adapter 4: Landesportale für Bauleitplanung (typ = "portal")
============================================================

Allgemeiner Crawler für zentrale Landesportale (DiPlanung `<land>.beteiligung.diplanung.de`,
bauleitplanung.sachsen.de, Beteiligungsportale u. a.). Er geht serverseitig gerenderte Seiten
eines Portals durch, erkennt Seiten mit PV-Bezug und liefert sie im selben Format wie die
anderen Adapter (titel, datum, text, link, dokument_link, body_name).

WICHTIG
  * Best effort: Die Portale wurden noch nie mit echten Daten getestet (die Entwicklungsumgebung
    erreicht sie nicht). Läuft ein Portal als reine JavaScript-App, findet der Crawler nichts
    und meldet das als Diagnose ("Seite ohne Inhalt"). Dann zuerst `portale_sonde.py` laufen
    lassen und den Bericht prüfen; für ein solches Portal braucht es einen eigenen Adapter.
  * Respektiert robots.txt und die Pause pro Server (Http aus pv_beschluesse).
  * Diese Portale zeigen vor allem Auslegungen und in Kraft getretene Pläne, nicht den
    Aufstellungsbeschluss. Die Beschlusstypen werden trotzdem heuristisch erkannt.
"""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

# Links, denen der Crawler folgt (Verfahrens- und Planungsseiten)
LINK_HINT = re.compile(
    r"verfahren|beteiligung|bauleit|bebauungsplan|b-plan|bplan|auslegung|offenlage|"
    r"planung|projekt|vorgang|detail|dokument|plan(?:id|nr)|page=|seite=|offset=", re.I)
SKIP_EXT = re.compile(r"\.(png|jpe?g|gif|svg|css|js|ico|woff2?|ttf|zip|mp4)(\?|$)", re.I)
URL_IN_TEXT = re.compile(r"https?://[^\s<>\"']+")


def _titel(soup: BeautifulSoup) -> str:
    for tag in ("h1", "title"):
        t = soup.find(tag)
        if t and t.get_text(strip=True):
            return t.get_text(" ", strip=True)[:300]
    return ""


def _sitemap_urls(http, basis: str, limit: int = 300) -> list[str]:
    """URLs aus sitemap.xml (auch Sitemap-Index, eine Ebene tief), gefiltert nach LINK_HINT."""
    out: list[str] = []
    for start in (urljoin(basis, "/sitemap.xml"),):
        try:
            xml = http.get(start, cache=False)
        except Exception:  # noqa: BLE001
            continue
        locs = URL_IN_TEXT.findall(re.sub(r"</?loc>", " ", xml))
        for u in locs[:20]:
            if u.endswith(".xml"):
                try:
                    locs += URL_IN_TEXT.findall(re.sub(r"</?loc>", " ", http.get(u, cache=False)))
                except Exception:  # noqa: BLE001
                    pass
        out += [u for u in locs if not u.endswith(".xml") and LINK_HINT.search(u)]
    return list(dict.fromkeys(out))[:limit]


def _feed_urls(soup: BeautifulSoup, seite: str) -> list[str]:
    return [urljoin(seite, a["href"]) for a in soup.find_all("link", href=True)
            if "alternate" in (a.get("rel") or []) and
            re.search(r"rss|atom|json", a.get("type", ""), re.I)]


def _karten(soup: BeautifulSoup, seite: str):
    """Verfahrenskarten einer DiPlanung-Liste (<li class="c-procedurelist__item">).

    Die Detailseiten (…/public/detail) sind eine JavaScript-App und liefern ohne Browser keinen Text.
    Die Karten auf der Startseite/Verfahrensliste enthalten aber schon Titel, Gemeinde, Zeitraum und
    Phase – das reicht, um PV-Verfahren zu erkennen. Liefert (detail_url, kartentext, titel).
    """
    for li in soup.select("li.c-procedurelist__item"):
        a = li.find("a", href=re.compile(r"/verfahren/"))
        if not a:
            continue
        text = re.sub(r"\s+", " ", li.get_text(" ", strip=True))
        text = re.sub(r"^Zur Beteiligung:\s*", "", text)
        titel = re.sub(r"^Zur Beteiligung:\s*", "", a.get_text(" ", strip=True)) or text[:120]
        yield urljoin(seite, a["href"]).split("#")[0], text, titel


def portal_vorlagen(http, q, seit: str | None, zustand=None,
                    max_seiten: int = 120, max_detail: int = 400):
    """Generator wie die anderen Adapter. q: Quelle (name, url, bundesland)."""
    import pv_beschluesse as pv  # lazy, vermeidet Zirkelimport

    host = urlparse(q.url).netloc
    queue = [q.url] + _sitemap_urls(http, q.url)
    gesehen: set[str] = set()
    detail_n = 0
    leer = 0
    karten_gesehen: set[str] = set()
    while queue and len(gesehen) < max_seiten:
        url = queue.pop(0).split("#")[0]
        if url in gesehen or SKIP_EXT.search(url):
            continue
        gesehen.add(url)
        try:
            html = http.get(url, cache=False)
        except PermissionError:
            continue
        except Exception:  # noqa: BLE001
            continue
        soup = BeautifulSoup(html, "html.parser")
        text = pv.html_text(html)
        if len(text) < 200 and soup.find("script"):
            gerendert = http.render(url)
            if gerendert:
                html = gerendert
                soup = BeautifulSoup(html, "html.parser")
                text = pv.html_text(html)
        if len(text) < 200 and soup.find("script"):
            leer += 1
            http.zaehle("Portal: Seite ohne Inhalt (JavaScript-App?)")
        # Feeds und Links einsammeln
        for f in _feed_urls(soup, url):
            http.zaehle("Portal: Feed gefunden")
            queue.append(f)
        for a in soup.find_all("a", href=True):
            absu = urljoin(url, a["href"]).split("#")[0]
            if urlparse(absu).netloc != host or absu in gesehen or SKIP_EXT.search(absu):
                continue
            if LINK_HINT.search(absu) or LINK_HINT.search(a.get_text(" ", strip=True)):
                queue.append(absu)
        # Verfahrenskarten (DiPlanung): PV-Verfahren direkt aus der Liste übernehmen
        for kurl, ktext, ktitel in _karten(soup, url):
            if kurl in karten_gesehen or detail_n >= max_detail:
                continue
            karten_gesehen.add(kurl)
            # PV-Bezug nur im Titel prüfen: im Kartentext steht auch der Absender (z. B. "BgA Photovoltaik")
            if not (pv.PV_RE.search(ktitel or ktext) and pv.PLANUNG_RE.search(ktext)):
                continue
            if zustand and zustand.hat(kurl):
                continue
            kdatum = pv.erstes_datum(ktext)
            if seit and kdatum and kdatum < seit:
                continue
            detail_n += 1
            http.zaehle("Portal: Treffer (Verfahrenskarte)")
            yield {"titel": ktitel, "datum": kdatum, "text": f"{q.name}\n{ktext}",
                   "link": kurl, "dokument_link": "", "body_name": q.name, "schluessel": kurl}
        # Treffer: Seite mit PV-Bezug und Planungsbezug (nicht die Startseite)
        if url == q.url or detail_n >= max_detail or url in karten_gesehen:
            continue
        titel = _titel(soup)
        if not pv.PV_RE.search(titel + "\n" + text[:3000]):
            continue
        if not pv.PLANUNG_RE.search(text[:20000]):
            continue
        if zustand and zustand.hat(url):
            continue
        datum = pv.erstes_datum(text)
        if seit and datum and datum < seit:
            continue
        detail_n += 1
        pdfs = [urljoin(url, x["href"]) for x in soup.find_all("a", href=True)
                if re.search(r"\.pdf(\?|$)|download|getfile|/file/", x["href"], re.I)][:2]
        anhang = "\n".join(pv.dokument_text(http, u)[:15000] for u in pdfs)
        http.zaehle("Portal: Treffer")
        yield {"titel": titel or q.name, "datum": datum, "text": text[:20000] + "\n" + anhang,
               "link": url, "dokument_link": pdfs[0] if pdfs else "", "body_name": q.name}
    if leer and not detail_n:
        http.zaehle("Portal: kein Treffer, Seiten leer -> portale_sonde.py auswerten")

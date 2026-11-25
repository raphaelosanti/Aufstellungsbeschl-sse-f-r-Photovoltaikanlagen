#!/usr/bin/env python3
"""
Adapter 6: Planverfahrenslisten der Industrie- und Handelskammern (typ = "ihk")
==============================================================================

Die IHKs werden bei Bauleitplanverfahren als Träger öffentlicher Belange beteiligt und veröffentlichen
die laufenden Verfahren ihres Bezirks (z. B. "Aktuelle Planverfahren", "Beteiligungsportal"). Das ist eine
Sammelquelle über viele Gemeinden hinweg, auch dort, wo es kein Ratsinformationssystem und kein Landesportal gibt
(Thüringen, Mecklenburg-Vorpommern, Sachsen, Brandenburg).

Jede IHK baut die Liste anders (Tabelle, Überschrift mit Absatz, Aufzählung, Detailseite mit Schlüssel/Wert-Tabelle).
Der Adapter erkennt diese vier Formen und liefert jeden Eintrag mit PV-Bezug als eigenen Treffer.

Grenzen
  * Die Listen zeigen meist Verfahren in Beteiligung oder Auslegung, selten den Aufstellungsbeschluss selbst.
    Der Beschlusstyp wird aus dem Text erkannt (z. B. "Aufstellung", "frühzeitige Beteiligung", "Entwurf").
  * Das Datum ist die genannte Frist oder Auslegung, sonst der Tag des ersten Abrufs.
  * Archivseiten alter Verfahren werden mit gelesen; `--seit` filtert nach dem erkannten Datum.
  * robots.txt und Pause pro Server gelten (Http aus pv_beschluesse).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

FOLGEN = re.compile(r"bauleit|planverfahren|planung|beteiligung|bebauungsplan|flaechennutzung|flächennutzung|"
                    r"aktuell|landkreis|kreis|stadt|gemeinde|verfahren|archiv|raumordnung|standort", re.I)
SKIP = re.compile(r"\.(png|jpe?g|gif|svg|css|js|ico|woff2?|zip|mp4|docx?|xlsx?|pdf)(\?|$)|mailto:|tel:", re.I)
KV_KEYS = {"stadt/gemeinde", "gemeinde", "stadt", "bezeichnung", "inhalt", "plandokumente und informationen"}
GEMEINDE_KOPF = re.compile(r"gemeinde|kommune|stadt|planungstr|ort", re.I)
PRAEFIX = re.compile(r"^((?:Stadt|Gemeinde|Samtgemeinde|Verbandsgemeinde|Ortsgemeinde|Amt|Markt|Ortschaft)\s+"
                     r"[A-ZÄÖÜ][^:|]{1,40}?)\s*[:\-–]\s+\S")
MAX_SEITEN = 30
MAX_TIEFE = 2


def _txt(el) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if hasattr(el, "get_text") else str(el).strip()


def _gemeinde_bereinigen(s: str) -> str:
    s = re.sub(r"\([^)]*\)", "", s)                       # "Frohndorf (SÖM)" -> "Frohndorf"
    return re.sub(r"\s+", " ", s).strip(" :-–|")[:80]


def eintraege(soup: BeautifulSoup) -> list[tuple[str, str, str]]:
    """(Titel, Gemeinde-Vermutung, Text) je Eintrag der Seite."""
    for t in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
        t.decompose()
    h1 = soup.find("h1")
    out: list[tuple[str, str, str]] = []

    # 1. Detailseite mit Schlüssel/Wert-Tabelle (IHK-Beteiligungsportal)
    kv: dict[str, str] = {}
    for tr in soup.find_all("tr"):
        z = [_txt(c) for c in tr.find_all(["th", "td"])]
        if len(z) == 2 and z[0].lower().rstrip(":") in KV_KEYS:
            kv[z[0].lower().rstrip(":")] = z[1]
    if kv.get("stadt/gemeinde"):
        titel = _txt(h1) if h1 else kv.get("bezeichnung", "")
        text = " | ".join(f"{k}: {v}" for k, v in kv.items())
        return [(titel, _gemeinde_bereinigen(kv["stadt/gemeinde"]), text)]

    # 2. Tabellen: eine Zeile = ein Verfahren
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue
        kopf = [_txt(c).lower() for c in rows[0].find_all(["th", "td"])]
        gcol = next((i for i, k in enumerate(kopf) if GEMEINDE_KOPF.search(k)), 0)
        for tr in rows[1:]:
            z = [_txt(c) for c in tr.find_all(["th", "td"])]
            if len(z) < 2:
                continue
            out.append((" ".join(z)[:200], _gemeinde_bereinigen(z[gcol] if gcol < len(z) else z[0]), " | ".join(z)))

    # 3. Überschrift + folgende Absätze (nur Blöcke ohne Liste/Tabelle; die sind unter 2 und 4 feiner erfasst)
    for h in soup.find_all(["h2", "h3", "h4"]):
        block, strukturiert = [], False
        for sib in h.next_siblings:
            if getattr(sib, "name", None) in ("h1", "h2", "h3", "h4"):
                break
            if getattr(sib, "name", None) in ("ul", "ol", "table") or (hasattr(sib, "find_all") and sib.find(["li", "tr"])):
                strukturiert = True
                break
            t = _txt(sib)
            if t:
                block.append(t)
        if strukturiert:
            continue
        kopf = _txt(h)
        rest = " ".join(block)
        text = (kopf + " " + rest).strip()
        if len(text) > 12:
            # Ist die Überschrift selbst das Verfahren (PV-Bezug), dient sie als Titel; sonst ist sie die Gemeinde
            ist_verfahren = bool(re.search(r"photovoltaik|solar|\bpv\b|bebauungsplan|b-plan|flächennutzungsplan", kopf, re.I))
            titel = kopf if ist_verfahren else (rest[:200] or kopf)
            out.append((titel, _gemeinde_bereinigen(kopf if not ist_verfahren else ""), text[:1800]))

    # 4. Aufzählungen; Gemeinde aus Präfix "Gemeinde X: ..." oder aus der vorherigen Überschrift
    for li in soup.find_all("li"):
        t = _txt(li)
        if not 20 < len(t) < 700:
            continue
        m = PRAEFIX.match(t)
        if m:
            g = _gemeinde_bereinigen(m.group(1))
        else:
            h = li.find_previous(["h2", "h3", "h4"])
            g = _gemeinde_bereinigen(_txt(h)) if h else ""
        out.append((t[:200], g, t))
    return out


def _schluessel(url: str, text: str) -> str:
    norm = re.sub(r"\W+", " ", text.lower()).strip()
    return f"{url}#{hashlib.sha1(norm.encode()).hexdigest()[:12]}"


def ihk_vorlagen(http, q, seit: str | None, zustand=None):
    import pv_beschluesse as pv  # lazy, vermeidet Zirkelimport

    p = urlparse(q.url)
    host = p.netloc.removeprefix("www.")
    segmente = [s for s in p.path.split("/") if s]
    praefix = "/" + segmente[0] if segmente else "/"      # eine IHK = erster Pfadabschnitt (/erfurt/, /pfalz/ ...)
    queue: list[tuple[str, int]] = [(q.url, 0)]
    gesehen: set[str] = set()
    gelesen: list[str] = []
    treffer = 0
    heute = dt.date.today().isoformat()
    while queue and len(gesehen) < MAX_SEITEN:
        url, tiefe = queue.pop(0)
        url = url.split("#")[0]
        if url in gesehen or SKIP.search(url):
            continue
        gesehen.add(url)
        try:
            html = http.get(url, cache=False)
        except PermissionError:
            continue
        except Exception:  # noqa: BLE001
            continue
        soup = BeautifulSoup(html, "html.parser")
        if tiefe < MAX_TIEFE:
            for a in soup.find_all("a", href=True):
                absu = urljoin(url, a["href"]).split("#")[0]
                pa = urlparse(absu)
                if absu in gesehen or SKIP.search(absu) or pa.netloc.removeprefix("www.") != host \
                        or not pa.path.startswith(praefix):
                    continue
                if FOLGEN.search(pa.path) or FOLGEN.search(a.get_text(" ", strip=True)):
                    queue.append((absu, tiefe + 1))
        h1 = soup.find("h1")
        seitentitel = _txt(h1) if h1 else ""
        planung_im_kopf = bool(pv.PLANUNG_RE.search(seitentitel + " " + urlparse(url).path))
        for titel, gemeinde, text in eintraege(soup):
            if not pv.PV_RE.search(titel + " " + text):
                continue
            if not (pv.PLANUNG_RE.search(text) or planung_im_kopf):
                continue
            if any(text[:80] in g or g[:80] in text for g in gelesen):     # Duplikate aus verschachtelten Blöcken
                continue
            gelesen.append(text)
            schluessel = _schluessel(url, text)
            if zustand and zustand.hat(schluessel):
                continue
            datum = pv.erstes_datum(text) or heute
            if seit and datum < seit:
                continue
            treffer += 1
            http.zaehle("IHK: Treffer")
            yield {"titel": titel[:300] or f"{q.name}: Planverfahren", "datum": datum,
                   "text": f"{gemeinde}\n{text}\nQuelle: Planverfahrensliste {q.name}\n{seitentitel}",
                   "link": url, "dokument_link": "", "body_name": gemeinde or q.name, "schluessel": schluessel}
    http.zaehle(f"IHK: {len(gesehen)} Seiten geprüft")

#!/usr/bin/env python3
"""
Adapter 5: Stadt Bremen – Deputation für Mobilität, Bau und Stadtentwicklung (typ = "bremen")
==========================================================================================

Warum ein eigener Adapter?
  In der Stadt Bremen fassen nicht Rat oder Bezirk die Aufstellungsbeschlüsse für Bebauungspläne,
  sondern die städtische Deputation für Mobilität, Bau und Stadtentwicklung. Ihre Unterlagen liegen
  nicht in ALLRIS/SessionNet, sondern
    * als "Abstimmungsergebnisse"-PDF je Sitzung auf bau.bremen.de
      (…/sixcms/media.php/13/Abstimmungsergebnisse_städtisch_MoBS_TT.MM.JJJJ.pdf) und
    * im Sitzungsdienst der Bremischen Bürgerschaft (sd.bremische-buergerschaft.de, SD.NET).

Vorgehen
  1. Auf der Deputationsseite (und im Archiv) alle Links auf Abstimmungsergebnisse-PDFs sammeln.
     Fehlt ein PDF in den Links, wird der Dateiname aus dem Sitzungsdatum der Seite gebildet.
  2. Jedes PDF in Tagesordnungspunkte (TOP) zerlegen; nur TOPs mit PV-Bezug werden weitergegeben.
  3. Zusätzlich: Links der Seite auf sd.bremische-buergerschaft.de/tops/ durchsehen
     (best effort – dieser Teil konnte bisher nicht gegen die echte Seite getestet werden).

Die Ausgabe hat dasselbe Format wie die anderen Adapter (titel, datum, text, link, dokument_link,
body_name, schluessel). Robots.txt und Pausen übernimmt die Http-Klasse aus pv_beschluesse.
"""
from __future__ import annotations

import datetime as dt
import re
from urllib.parse import quote, urljoin, urlparse

from bs4 import BeautifulSoup

import pv_beschluesse as pv

START_URL = "https://bau.bremen.de/ressort/deputation-3443"
ARCHIV_URL = "https://bau.bremen.de/ressort/deputation/deputation-archiv-4693?max=100&skip=0"
PDF_BASIS = "https://bau.bremen.de/sixcms/media.php/13/"
GREMIUM = "Städtische Deputation für Mobilität, Bau und Stadtentwicklung"

MONATE = {"januar": 1, "februar": 2, "märz": 3, "maerz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7,
          "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12}
DATUM_TEXT_RE = re.compile(
    r"\b(\d{1,2})\.\s*(Januar|Februar|März|Maerz|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+(20\d{2})\b",
    re.I)
DATUM_NUM_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(20\d{2})\b")
PDF_LINK_RE = re.compile(r"Abstimmungsergebnisse.*\.pdf", re.I)
TOP_RE = re.compile(r"(?ms)^[ \t]*TOP[ \t]+(\d+)[ \t]+(.*?)(?=^[ \t]*TOP[ \t]+\d+[ \t]|\Z)")


def _datum_iso(tag: int, monat: int, jahr: int) -> str:
    try:
        return dt.date(jahr, monat, tag).isoformat()
    except ValueError:
        return ""


def sitzungsdaten(text: str) -> list[str]:
    """Alle Sitzungsdaten ("10. September 2026") einer Seite als ISO-Daten, neueste zuerst."""
    out = {_datum_iso(int(t), MONATE[m.lower()], int(j)) for t, m, j in DATUM_TEXT_RE.findall(text)}
    return sorted((d for d in out if d), reverse=True)


def pdf_url(datum_iso: str, art: str) -> str:
    """art: 'städtisch' oder 'staatlich'."""
    j, m, t = datum_iso.split("-")
    return f"{PDF_BASIS}{quote(f'Abstimmungsergebnisse_{art}_MoBS_{t}.{m}.{j}.pdf')}"


def datum_aus_pdf(text: str, url: str) -> str:
    kopf = text[:600]
    m = re.search(r"\bam\s+(\d{1,2})\.(\d{1,2})\.(20\d{2})", kopf) or DATUM_NUM_RE.search(url) \
        or DATUM_NUM_RE.search(kopf)
    return _datum_iso(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else ""


def tops_aus_text(text: str) -> list[tuple[str, str]]:
    return [(n, re.sub(r"\s+", " ", body).strip()) for n, body in TOP_RE.findall(text)]


def _seiten(http, start: str) -> list[tuple[str, str]]:
    seiten = []
    for url in dict.fromkeys([start, ARCHIV_URL]):
        try:
            seiten.append((url, http.get(url, cache=False)))
        except PermissionError:
            raise
        except Exception:  # noqa: BLE001
            continue
    return seiten


def bremen_vorlagen(http, q, seit: str | None, zustand=None, max_pdfs: int = 80):
    start = q.url or START_URL
    seiten = _seiten(http, start)
    if not seiten:
        raise RuntimeError("Deputationsseite nicht erreichbar")

    # 1. PDF-Links und Sitzungsdaten sammeln
    pdfs: dict[str, str] = {}          # url -> Datum (ISO oder "")
    sdnet: list[str] = []
    daten: set[str] = set()
    for url, html in seiten:
        soup = BeautifulSoup(html, "html.parser")
        daten.update(sitzungsdaten(soup.get_text(" ", strip=True)))
        for a in soup.find_all("a", href=True):
            ziel = urljoin(url, a["href"])
            if PDF_LINK_RE.search(ziel) or PDF_LINK_RE.search(a.get_text(" ", strip=True)) and ziel.lower().endswith(".pdf"):
                m = DATUM_NUM_RE.search(ziel)
                pdfs[ziel] = _datum_iso(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else ""
            elif "sd.bremische-buergerschaft.de" in urlparse(ziel).netloc:
                sdnet.append(ziel)
    # fehlende PDFs aus den Sitzungsdaten bilden (städtisch + staatlich)
    bekannte_daten = {d for d in pdfs.values() if d}
    for d in sorted(daten, reverse=True):
        if d in bekannte_daten or (seit and d < seit) or d > dt.date.today().isoformat():
            continue
        for art in ("städtisch", "staatlich"):
            pdfs.setdefault(pdf_url(d, art), d)
    print(f"   Bremen: {len(pdfs)} Abstimmungsergebnis-PDFs, {len(set(sdnet))} Links zum Sitzungsdienst")

    gesehen = set()
    # 2. Abstimmungsergebnisse-PDFs
    for url, datum in sorted(pdfs.items(), key=lambda x: x[1], reverse=True)[:max_pdfs]:
        if seit and datum and datum < seit:
            continue
        try:
            data = http.get(url, binary=True)
        except PermissionError:
            raise
        except Exception:  # noqa: BLE001
            continue            # nicht jedes gebildete PDF existiert (404) – ist ok
        if data[:4] != b"%PDF":
            continue
        http.zaehle("Sitzungs-PDFs gelesen")
        text = pv.pdf_text(data, max_seiten=40)
        datum = datum_aus_pdf(text, url) or datum
        art = "staatliche" if "staatlich" in url.lower() else "städtische"
        for nr, body in tops_aus_text(text):
            if not pv.PV_RE.search(body):
                continue
            key = f"{url}#TOP{nr}"
            if key in gesehen or (zustand and zustand.hat(key)):
                continue
            gesehen.add(key)
            http.zaehle("PV-Tagesordnungspunkte")
            gremium = GREMIUM if art == "städtische" else GREMIUM.replace("Städtische", "Staatliche")
            ueberschrift = re.split(r"\s+-\s+", body, maxsplit=1)[0]
            if re.search(r"aufstellungsbeschluss", body, re.I):
                ueberschrift += " – Planaufstellungsbeschluss"   # gleichzeitig beschlossene "Veröffentlichung im Internet" soll den Typ nicht überlagern
            yield {"titel": f"TOP {nr} {ueberschrift}"[:300], "datum": datum,
                   "text": f"{gremium}, Bremen\nAbstimmungsergebnisse der Sitzung am {datum}\nTOP {nr} {body}",
                   "link": url, "dokument_link": url, "body_name": "Bremen", "schluessel": key}

    # 3. Sitzungsdienst der Bürgerschaft (SD.NET) – best effort
    for url in list(dict.fromkeys(sdnet))[:40]:
        if "/tops" not in url:
            continue
        try:
            html = http.get(url)
        except PermissionError:
            raise
        except Exception:  # noqa: BLE001
            continue
        soup = BeautifulSoup(html, "html.parser")
        seite = soup.get_text(" ", strip=True)
        m = DATUM_NUM_RE.search(seite)
        datum = _datum_iso(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else ""
        if seit and datum and datum < seit:
            continue
        for zeile in soup.find_all(["tr", "li"]):
            kontext = zeile.get_text(" ", strip=True)
            if not (pv.PV_RE.search(kontext) and pv.PLANUNG_RE.search(kontext)):
                continue
            key = f"{url}#{kontext[:80]}"
            if key in gesehen or (zustand and zustand.hat(key)):
                continue
            gesehen.add(key)
            links = [urljoin(url, a["href"]) for a in zeile.find_all("a", href=True)]
            doc = next((u for u in links if not u.rstrip("/").endswith(urlparse(url).path.rstrip("/"))), "")
            anhang = pv.dokument_text(http, doc)[:15000] if doc else ""
            http.zaehle("PV-Tagesordnungspunkte")
            yield {"titel": kontext[:300], "datum": datum,
                   "text": f"{GREMIUM}, Bremen\n{kontext}\n{anhang}",
                   "link": url, "dokument_link": doc, "body_name": "Bremen", "schluessel": key}

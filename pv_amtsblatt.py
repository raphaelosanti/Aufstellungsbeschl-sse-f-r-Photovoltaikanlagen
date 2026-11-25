#!/usr/bin/env python3
"""
Adapter 7: Amtsblätter und Mitteilungsblätter als PDF (typ = "amtsblatt")
========================================================================

Viele Gemeinden bekommen Aufstellungsbeschlüsse nur als amtliche Bekanntmachung im Amtsblatt der Gemeinde, des
Amts oder der Verbandsgemeinde. Die Ausgaben liegen meist als PDF auf einer Übersichtsseite. Der Adapter öffnet die
Übersicht (und wenige Archivseiten), lädt die neuesten noch nicht gelesenen PDFs und schneidet aus dem Volltext die
Stellen mit PV-Bezug und Planungsbezug heraus. Eine Ausgabe hat viele Bekanntmachungen, deshalb wird nicht der ganze Text
bewertet, sondern je Fundstelle ein Textfenster.

Grenzen
  * Nur Amtsblätter, die ohne Anmeldung als PDF abrufbar sind. Gescannte PDFs ohne Textebene bleiben stumm.
  * Pro Quelle und Lauf werden höchstens MAX_PDF neue Ausgaben gelesen (die neuesten zuerst); ältere folgen an den
    nächsten Tagen. Jede gelesene Ausgabe wird gemerkt und nicht erneut geladen.
  * Das Fenster kann mehrere Bekanntmachungen enthalten. Der Beschlusstyp wird heuristisch erkannt.
"""
from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

PDF_LINK = re.compile(r"\.pdf(\?|$)|getfile|download|/media/|/file/|dokument", re.I)
AUSGABE = re.compile(r"amtsblatt|mitteilungsblatt|ausgabe|\bnr\b|kw\s?\d|20\d\d|bekanntmach|kurier|anzeiger|bote", re.I)
ARCHIV = re.compile(r"archiv|ausgaben|jahrgang|20\d\d|vorherige|weitere", re.I)
SKIP = re.compile(r"\.(png|jpe?g|gif|svg|css|js|ico|woff2?|zip|mp4|docx?|xlsx?)(\?|$)|mailto:|tel:", re.I)
DATUM_URL = re.compile(r"(20\d\d)[-_./]?(0[1-9]|1[0-2])[-_./]?(0[1-9]|[12]\d|3[01])")
MAX_PDF = 12
MAX_ARCHIV = 6
MAX_MB = 40


def fenster(text: str, vor: int = 1500, nach: int = 2500, max_n: int = 6) -> list[str]:
    """Textfenster um PV-Fundstellen, die zugleich nach Planung/Bekanntmachung aussehen."""
    import pv_beschluesse as pv

    spannen: list[list[int]] = []
    for m in pv.PV_RE.finditer(text):
        a, b = max(0, m.start() - vor), min(len(text), m.end() + nach)
        if spannen and a <= spannen[-1][1]:
            spannen[-1][1] = max(spannen[-1][1], b)
        else:
            spannen.append([a, b])
    out = []
    for a, b in spannen:
        w = text[a:b]
        if pv.PLANUNG_RE.search(w) and re.search(r"bekanntmach|aufstellung|auslegung|beteiligung|beschluss", w, re.I):
            out.append(w)
        if len(out) >= max_n:
            break
    return out


def _titel(fens: str) -> str:
    import pv_beschluesse as pv

    zeilen = [z.strip() for z in fens.splitlines() if 15 < len(z.strip()) < 220]
    for z in zeilen:
        if pv.PV_RE.search(z) and pv.PLANUNG_RE.search(z):
            return z
    for z in zeilen:
        if pv.PLANUNG_RE.search(z):
            return z
    return zeilen[0] if zeilen else fens[:150]


def pdf_kandidaten(http, start: str, host: str) -> list[tuple[str, str]]:
    """(URL, Beschriftung) der PDFs auf der Übersicht und auf wenigen Archivseiten, neueste zuerst."""
    kand: dict[str, str] = {}
    seiten = [start]
    gesehen: set[str] = set()
    archiv = 0
    while seiten:
        url = seiten.pop(0)
        if url in gesehen:
            continue
        gesehen.add(url)
        try:
            html = http.get(url, cache=False)
        except Exception:  # noqa: BLE001
            continue
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            absu = urljoin(url, a["href"]).split("#")[0]
            label = a.get_text(" ", strip=True)
            if SKIP.search(absu):
                continue
            if PDF_LINK.search(absu) and (AUSGABE.search(absu + " " + label) or absu.lower().endswith(".pdf")):
                kand.setdefault(absu, label)
            elif url == start and archiv < MAX_ARCHIV and urlparse(absu).netloc.removeprefix("www.") == host \
                    and ARCHIV.search(label + " " + absu) and not PDF_LINK.search(absu):
                archiv += 1
                seiten.append(absu)

    def sortschluessel(item):
        m = DATUM_URL.search(item[0] + " " + item[1])
        return m.group(0).replace("-", "").replace("_", "").replace(".", "").replace("/", "") if m else ""

    liste = list(kand.items())
    if any(sortschluessel(i) for i in liste):
        liste.sort(key=sortschluessel, reverse=True)       # mit erkennbarem Datum: neueste zuerst
    return liste                                            # sonst Reihenfolge der Seite (meist neueste oben)


def amtsblatt_vorlagen(http, q, seit: str | None, zustand=None):
    import pv_beschluesse as pv  # lazy, vermeidet Zirkelimport

    host = urlparse(q.url).netloc.removeprefix("www.")
    kandidaten = pdf_kandidaten(http, q.url, host)
    gelesen = 0
    treffer = 0
    for url, label in kandidaten:
        if gelesen >= MAX_PDF:
            break
        if zustand and zustand.hat(url):
            continue
        m = DATUM_URL.search(url + " " + label)
        ausgabe_datum = f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""
        if seit and ausgabe_datum and ausgabe_datum < seit:
            continue
        try:
            data = http.get(url, binary=True)
        except PermissionError:
            continue
        except Exception:  # noqa: BLE001
            continue
        gelesen += 1
        if len(data) > MAX_MB * 1_000_000:
            text = ""
        elif data[:4] == b"%PDF":
            text = pv.pdf_text(data, max_seiten=80)
        else:
            text = pv.html_text(data.decode("utf-8", errors="replace"))
        if zustand:
            zustand.verwirf(url)             # Ausgabe ist gelesen: nicht noch einmal laden
        for i, w in enumerate(fenster(text)):
            datum = pv.erstes_datum(w) or ausgabe_datum
            if seit and datum and datum < seit:
                continue
            titel = _titel(w)
            treffer += 1
            http.zaehle("Amtsblatt: Treffer")
            yield {"titel": titel[:300], "datum": datum, "text": f"{q.name}\n{w}", "link": url,
                   "dokument_link": url, "body_name": q.name, "schluessel": f"{url}#{i}"}
    http.zaehle(f"Amtsblatt: {gelesen} Ausgaben gelesen, {len(kandidaten)} gefunden")

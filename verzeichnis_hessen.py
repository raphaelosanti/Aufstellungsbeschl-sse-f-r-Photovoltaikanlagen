#!/usr/bin/env python3
"""
Hessen: Verzeichnis "Bebauungspläne im Verfahren"  ->  quellen_verzeichnis.csv  (typ = "homepage")
=================================================================================================

bauleitplanung.hessen.de führt je Gemeinde (alphabetisch, A bis Z) Links zu "Bebauungsplan im Verfahren" auf die Seiten
der Gemeinden. Das Land ist nach BauGB verpflichtet, in Aufstellung befindliche Pläne zugänglich zu machen. Das
Verzeichnis liefert für jede hessische Gemeinde die richtige Unterseite, auch ohne RIS. Die Seiten werden vom
Homepage-Crawler (pv_homepage.py) gelesen.

Es wird nur das Verzeichnis abgerufen (wenige Seiten), nicht die Gemeinden selbst.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from quellen_entdecken import QUELLEN_FELDER, lade_csv, schreibe_csv

START = ["https://bauleitplanung.hessen.de/bebauungsplaene-in-hessen-a-z/a-c",
         "https://bauleitplanung.hessen.de/flaechennutzungsplaene-in-hessen-a-z/a-c"]
GRUPPE = re.compile(r"(bebauungsplaene|flaechennutzungsplaene)-in-hessen-a-z/", re.I)
IM_VERFAHREN = re.compile(r"im verfahren", re.I)


def parse_seite(html: str, basis: str) -> tuple[list[tuple[str, str]], list[str]]:
    """([(Gemeinde, URL)], weitere Verzeichnisseiten)"""
    soup = BeautifulSoup(html, "html.parser")
    funde, weitere = [], []
    for a in soup.find_all("a", href=True):
        absu = urljoin(basis, a["href"]).split("#")[0]
        text = a.get_text(" ", strip=True)
        if IM_VERFAHREN.search(text):
            h = a.find_previous(["h2", "h3", "h4"])
            name = h.get_text(" ", strip=True) if h else ""
            if name and urlparse(absu).scheme in ("http", "https"):
                funde.append((name, absu))
        elif GRUPPE.search(absu) and urlparse(absu).netloc.endswith("bauleitplanung.hessen.de"):
            weitere.append(absu)
    return funde, weitere


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="quellen_verzeichnis.csv")
    ap.add_argument("--pause", type=float, default=1.0)
    a = ap.parse_args()
    import pv_beschluesse as pv
    http = pv.Http(pause=a.pause)
    rows = {r["url"]: r for r in lade_csv(a.out)}
    queue, gesehen, neu = list(START), set(), 0
    while queue and len(gesehen) < 60:
        url = queue.pop(0)
        if url in gesehen:
            continue
        gesehen.add(url)
        try:
            html = http.get(url, cache=False)
        except Exception as e:  # noqa: BLE001
            print(f"   ! {url}: {e}")
            continue
        funde, weitere = parse_seite(html, url)
        queue += [w for w in weitere if w not in gesehen]
        for name, link in funde:
            if link not in rows:
                rows[link] = {"name": name, "landkreis": "", "typ": "homepage", "url": link, "bundesland": "Hessen",
                              "hinweis": "Hessen-Verzeichnis: Bebauungsplan im Verfahren"}
                neu += 1
    zeilen = sorted(rows.values(), key=lambda r: r["name"])
    schreibe_csv(a.out, QUELLEN_FELDER, zeilen)
    print(f"Hessen-Verzeichnis: {len(gesehen)} Seiten, {neu} neue Links, {len(zeilen)} gesamt → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

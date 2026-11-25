#!/usr/bin/env python3
"""
Amtsblatt-Seiten der Gemeinden finden  ->  quellen_amtsblatt.csv  (typ = "amtsblatt")
=====================================================================================

Für Gemeinden ohne RIS (oder mit durch robots.txt gesperrtem RIS) wird die Startseite abgerufen und nach einem Link
zu Amtsblatt, Mitteilungsblatt oder amtlichen Bekanntmachungen gesucht. Die gefundene Übersichtsseite wird als Quelle
für den Adapter `pv_amtsblatt.py` eingetragen. Mehrere Gemeinden desselben Amts teilen sich eine Quelle.

Pro Lauf werden höchstens --budget Gemeinden geprüft (Standard 2000); geprüfte Gemeinden werden 120 Tage lang nicht
erneut abgerufen (daten/amtsblatt_geprueft.json).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from quellen_entdecken import QUELLEN_FELDER, lade_csv, schreibe_csv

# Reihenfolge = Priorität
AMTS = [re.compile(p, re.I) for p in (
    r"amtsblatt", r"mitteilungsblatt", r"amtliche[rn]? bekanntmachung", r"amtsbote|gemeindebote|gemeindeanzeiger",
    r"verbandsgemeinde-?kurier|gemeindekurier|amtsanzeiger|wochenblatt", r"bekanntmachungen")]
AUSSCHLUSS = re.compile(r"europ[äa]isch|bundesanzeiger|ministerial|staatsanzeiger|gesetz- und verordnungs|"
                        r"abo|bestell|anzeige aufgeben|werbung|impressum|datenschutz", re.I)
SKIP = re.compile(r"\.(png|jpe?g|gif|svg|css|js|ico|woff2?|zip|mp4|docx?|xlsx?)(\?|$)|mailto:|tel:|javascript:", re.I)
RECHECK_TAGE = 120


def beste_verlinkung(html: str, basis: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    host = urlparse(basis).netloc.removeprefix("www.")
    beste: tuple[int, int, str] | None = None
    for a in soup.find_all("a", href=True):
        absu = urljoin(basis, a["href"]).split("#")[0]
        if SKIP.search(absu):
            continue
        label = a.get_text(" ", strip=True)
        z = f"{label} {absu}"
        if AUSSCHLUSS.search(label) or len(label) > 80 and not AMTS[0].search(absu):
            continue
        for rang, rx in enumerate(AMTS):
            if rx.search(label) or rx.search(urlparse(absu).path):
                gleicher_host = 0 if urlparse(absu).netloc.removeprefix("www.") == host else 1
                kandidat = (rang, gleicher_host, absu)
                if beste is None or kandidat[:2] < beste[:2]:
                    beste = kandidat
                break
    return beste[2] if beste else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gemeinden", default=os.path.join("daten", "gemeinden.csv"))
    ap.add_argument("--out", default="quellen_amtsblatt.csv")
    ap.add_argument("--stand", default=os.path.join("daten", "amtsblatt_geprueft.json"))
    ap.add_argument("--land", nargs="+", default=["alle"])
    ap.add_argument("--budget", type=int, default=2000)
    ap.add_argument("--parallel", type=int, default=8)
    ap.add_argument("--status", nargs="+", default=["kein_ris", "gesperrt"])
    ap.add_argument("--pause", type=float, default=0.7)
    a = ap.parse_args()

    import pv_beschluesse as pv
    http = pv.Http(pause=a.pause)
    heute = dt.date.today()
    stand = json.load(open(a.stand, encoding="utf-8")) if os.path.exists(a.stand) else {}
    rows = {r["url"]: r for r in lade_csv(a.out)}
    gem = lade_csv(a.gemeinden)
    offen = []
    for g in gem:
        if g["ris_status"] not in a.status or not g["web"] or ("alle" not in a.land and g["land"] not in a.land):
            continue
        z = stand.get(g["web"])
        if z and (heute - dt.date.fromisoformat(z)).days < RECHECK_TAGE:
            continue
        offen.append(g)
    offen.sort(key=lambda g: stand.get(g["web"], ""))        # nie geprüfte zuerst
    offen = offen[:a.budget]
    print(f"Amtsblatt-Suche: {len(offen)} Gemeinden in diesem Lauf", flush=True)

    def pruefe(g):
        try:
            html = http.get(g["web"], cache=False)
        except Exception:  # noqa: BLE001
            return g, None, False
        return g, beste_verlinkung(html, g["web"]), True

    neu = 0
    with ThreadPoolExecutor(max_workers=a.parallel) as pool:
        for g, url, erreichbar in pool.map(pruefe, offen):
            if erreichbar:
                stand[g["web"]] = heute.isoformat()
            if url and url not in rows and url.rstrip("/") != g["web"].rstrip("/"):
                rows[url] = {"name": g["name"], "landkreis": g["landkreis"], "typ": "amtsblatt", "url": url,
                             "bundesland": g["land"], "hinweis": "Amtsblatt/Bekanntmachungen als PDF"}
                neu += 1
    os.makedirs(os.path.dirname(a.stand) or ".", exist_ok=True)
    with open(a.stand, "w", encoding="utf-8") as f:
        json.dump(stand, f, ensure_ascii=False, indent=0, sort_keys=True)
    zeilen = sorted(rows.values(), key=lambda r: (r["bundesland"], r["name"]))
    schreibe_csv(a.out, QUELLEN_FELDER, zeilen)
    print(f"Amtsblatt-Quellen: {neu} neu, {len(zeilen)} gesamt → {a.out}; geprüft insgesamt {len(stand)} Gemeinden")
    return 0


if __name__ == "__main__":
    sys.exit(main())

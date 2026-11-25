#!/usr/bin/env python3
"""
Zielliste aus dem MaStR-Abgleich: Gemeinden mit bekannter Freiflächen-PV, für die das Register noch nichts hat.

Liest entdeckung/mastr_gemeinden.csv (von mastr_abgleich.py) und daten/gemeinden.csv und schreibt
quellen_mastr.csv: je Gemeinde eine Quelle vom Typ "homepage_mastr". Der Adapter pv_homepage.py durchsucht die
Homepage dann tiefer als bei normalen Homepage-Quellen (70 statt 20 Seiten, sitemap.xml, interne Suche, Parkname).

Aufgenommen werden Gemeinden, die NICHT 'im Register' sind und eine Homepage haben, nach Leistung sortiert.
"""
from __future__ import annotations

import csv
import os
import sys

FELDER = ["name", "landkreis", "typ", "url", "bundesland", "hinweis"]


def lies(pfad: str) -> list[dict]:
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    mastr = lies(os.path.join("entdeckung", "mastr_gemeinden.csv"))
    if not mastr:
        print("entdeckung/mastr_gemeinden.csv fehlt – erst mastr_abgleich.py laufen lassen")
        return 1
    tab = lies(os.path.join("daten", "gemeinden.csv"))
    nach_ags = {t["ags"].zfill(8): t for t in tab}
    ziele, ohne_web = [], 0
    for m in sorted(mastr, key=lambda r: -float(r.get("mw") or 0)):
        if m["kategorie"] == "im Register":
            continue
        t = nach_ags.get((m.get("ags") or "").zfill(8), {})
        web = (m.get("web") or t.get("web") or "").strip()
        if not web:
            ohne_web += 1
            continue
        parks = (m.get("parks") or "").replace("|", "/")
        hinweis = f"MaStR {m['mw']} MW, {m['anlagen']} Anlagen, {m['kategorie']}"
        if parks:
            hinweis += f" | park={parks}"
        ziele.append({"name": f"{m['gemeinde'].split(',')[0]} [MaStR]", "landkreis": m["landkreis"],
                      "typ": "homepage_mastr", "url": web, "bundesland": m["land"], "hinweis": hinweis})
    with open("quellen_mastr.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, FELDER)
        w.writeheader()
        w.writerows(ziele)
    print(f"{len(ziele)} Gemeinden in quellen_mastr.csv ({ohne_web} ohne bekannte Homepage übersprungen)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

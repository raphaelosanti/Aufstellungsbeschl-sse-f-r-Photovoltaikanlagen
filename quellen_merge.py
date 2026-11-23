#!/usr/bin/env python3
"""
Führt die Ergebnisse der parallelen Länder-Läufe (quellen-entdecken.yml) zusammen.

Jeder Länder-Job startet vom Stand im Repo, arbeitet NUR sein Bundesland ab und liefert seine
beiden Dateien (quellen_alle.csv, daten/gemeinden.csv) als Artefakt ab:  <shards>/<slug>/...
Dieses Skript übernimmt aus jedem Shard ausschließlich die Zeilen des eigenen Bundeslands
und lässt alles andere (andere Länder, manuelle Zeilen) unverändert.

Aufruf:
    python quellen_merge.py --shards shards --laender "Brandenburg=brandenburg" "Bayern=bayern" ...
"""
from __future__ import annotations

import argparse
import os
import sys

from quellen_entdecken import GEM_FELDER, QUELLEN_FELDER, lade_csv, schreibe_csv


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards", default="shards")
    ap.add_argument("--laender", nargs="+", required=True, help='"Bundesland=slug" je Land, das gelaufen ist')
    ap.add_argument("--quellen", default="quellen_alle.csv")
    ap.add_argument("--gemeinden", default=os.path.join("daten", "gemeinden.csv"))
    a = ap.parse_args()

    quellen = [{k: (r.get(k) or "") for k in QUELLEN_FELDER} for r in lade_csv(a.quellen)]
    gem = {r["ags"]: {k: (r.get(k) or "") for k in GEM_FELDER} for r in lade_csv(a.gemeinden)}

    uebernommen = 0
    for eintrag in a.laender:
        land, _, slug = eintrag.partition("=")
        q_pfad = os.path.join(a.shards, slug, "quellen_alle.csv")
        g_pfad = os.path.join(a.shards, slug, "gemeinden.csv")
        if not (os.path.exists(q_pfad) and os.path.exists(g_pfad)):
            print(f"! {land}: kein Ergebnis (Job fehlgeschlagen/abgebrochen) – Stand bleibt unverändert")
            continue
        neu_q = [{k: (r.get(k) or "") for k in QUELLEN_FELDER} for r in lade_csv(q_pfad)
                 if (r.get("bundesland") or "") == land]
        quellen = [r for r in quellen if r["bundesland"] != land] + neu_q
        neu_g = [r for r in lade_csv(g_pfad) if r.get("land") == land]
        for r in neu_g:
            gem[r["ags"]] = {k: (r.get(k) or "") for k in GEM_FELDER}
        uebernommen += 1
        print(f"{land}: {len(neu_q)} Quellen, {len(neu_g)} Gemeinden übernommen")

    if not uebernommen:
        print("Nichts zu mergen.")
        return 0
    schreibe_csv(a.quellen, QUELLEN_FELDER, quellen)
    schreibe_csv(a.gemeinden, GEM_FELDER, sorted(gem.values(), key=lambda r: (r["land"], r["name"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())

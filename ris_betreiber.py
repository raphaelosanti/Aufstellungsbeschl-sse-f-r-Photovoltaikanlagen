#!/usr/bin/env python3
"""
RIS-Betreiber-Auswertung für das PV-Beschlussregister
=====================================================

Liest daten/gemeinden.csv (und quellen_alle.csv) und beantwortet:
  * Welche Plattform (SessionNet, ALLRIS, ratsinfo-online.net, ...) steckt hinter dem RIS?
  * Wie viele Gemeinden teilen sich denselben Betreiber (Amt, Verbandsgemeinde, Dienstleister)?
  * Wo sind die Lücken (nicht geprüft / kein RIS / gesperrt) je Bundesland?
  * Welcher Adapter würde die meisten zusätzlichen Gemeinden freischalten?

Schreibt:
  entdeckung/betreiber.csv   eine Zeile je RIS-Betreiber (Host+Pfad) mit Plattform und Gemeindeliste
  entdeckung/abdeckung.md    Bericht (Länderübersicht, Plattformen, Adapter-Ranking)

Aufruf:
    python ris_betreiber.py
    python ris_betreiber.py --gemeinden daten/gemeinden.csv --quellen quellen_alle.csv
Nur Standardbibliothek, kein Netzwerkzugriff.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
from collections import Counter, defaultdict
from urllib.parse import urlparse

# Plattform-Erkennung: (Name, Regex auf die URL, hat Adapter in pv_beschluesse.py?)
# Reihenfolge = Priorität. "Dienstleister-OParl" (gemeinsame OParl-Hosts) läuft über den OParl-Adapter.
PLATTFORMEN = [
    ("SessionNet (Somacos)", r"sessionnet|/bi/|buergerinfo|vo0040|si0040|to0040", "ja"),
    ("ALLRIS (CC e-gov)", r"allris|vo020\.asp|si010_e\.asp|/ri/", "teilweise (HTML)"),
    ("ratsinfo-online.net", r"ratsinfo-online\.net", "teilweise (auto)"),
    ("ratsinfomanagement.net (OParl)", r"ratsinfomanagement\.net", "ja (OParl)"),
    ("kdvz-frechen.de (OParl)", r"kdvz-frechen\.de", "ja (OParl)"),
    ("ekom21 (OParl)", r"ekom21\.de", "ja (OParl)"),
    ("gremien.info (OParl)", r"gremien\.info", "ja (OParl)"),
    ("sitzung-online.de", r"sitzung-online\.de", "nein"),
    ("Mandatos", r"mandatos", "nein"),
    ("sdnet / Sitzungsdienst", r"sdnet|sitzungsdienst", "nein"),
    ("Kommunalportal / more!rubin", r"kommunalportal|rubin|more-rubin", "nein"),
    ("OParl (sonstige)", r"oparl", "ja (OParl)"),
]


def plattform(url: str, typ: str) -> tuple[str, str]:
    for name, rx, adapter in PLATTFORMEN:
        if re.search(rx, url, re.I):
            return name, adapter
    if typ == "oparl":
        return "OParl (sonstige)", "ja (OParl)"
    if typ == "sessionnet":
        return "SessionNet (Somacos)", "ja"
    return "unbekannt", "nein"


def betreiber_schluessel(url: str) -> str:
    """Host + erster Pfadabschnitt: unterscheidet z. B. ratsinfo-online.net/<amt>-bi/ je Betreiber."""
    p = urlparse(url if "://" in url else "https://" + url)
    host = p.netloc.lower().removeprefix("www.")
    teile = [t for t in p.path.split("/") if t]
    if host in ("ratsinfo-online.net", "ratsinfomanagement.net", "gremien.info") and teile:
        return f"{host}/{teile[0]}"
    return host + ("/" + teile[0] if teile and teile[0].lower() in ("bi", "ris", "buergerinfo", "ratsinfo") else "")


def lade(pfad: str) -> list[dict]:
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gemeinden", default="daten/gemeinden.csv")
    ap.add_argument("--quellen", default="quellen_alle.csv")
    ap.add_argument("--out", default="entdeckung")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    gem = lade(a.gemeinden)
    quellen = {q["url"]: q for q in lade(a.quellen)} if os.path.exists(a.quellen) else {}

    # --- Lücken je Land -------------------------------------------------
    land = defaultdict(Counter)
    for g in gem:
        st = g["ris_status"] or ("ungeprueft" if not g["geprueft_am"] else "geprueft_ohne_status")
        land[g["land"]][st] += 1
        land[g["land"]]["gesamt"] += 1

    # --- Betreiber bilden -----------------------------------------------
    betr = {}
    for g in gem:
        if not g["ris_url"]:
            continue
        key = betreiber_schluessel(g["ris_url"])
        b = betr.setdefault(key, {
            "betreiber": key, "land": g["land"], "url": g["ris_url"], "typ": g["ris_typ"],
            "status": g["ris_status"], "gemeinden": [], "landkreise": set()})
        b["gemeinden"].append(g["name"])
        b["landkreise"].add(g["landkreis"])
    for b in betr.values():
        b["plattform"], b["adapter"] = plattform(b["url"], b["typ"])
        b["in_quellen"] = "ja" if b["url"] in quellen or any(
            betreiber_schluessel(u) == b["betreiber"] for u in quellen) else "nein"

    with open(os.path.join(a.out, "betreiber.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["betreiber", "bundesland", "plattform", "adapter", "status", "anzahl_gemeinden",
                    "in_quellen_alle", "url", "landkreise", "gemeinden"])
        for b in sorted(betr.values(), key=lambda x: -len(x["gemeinden"])):
            w.writerow([b["betreiber"], b["land"], b["plattform"], b["adapter"], b["status"],
                        len(b["gemeinden"]), b["in_quellen"], b["url"],
                        "; ".join(sorted(b["landkreise"])), "; ".join(sorted(b["gemeinden"]))])

    # --- Plattform-Ranking ----------------------------------------------
    pl = defaultdict(lambda: {"betreiber": 0, "gemeinden": 0, "adapter": ""})
    for b in betr.values():
        p = pl[b["plattform"]]
        p["betreiber"] += 1
        p["gemeinden"] += len(b["gemeinden"])
        p["adapter"] = b["adapter"]

    n = len(gem)
    ungeprueft = sum(c["ungeprueft"] for c in land.values())
    md = [f"# RIS-Abdeckung ({n} Gemeinden)\n",
          f"Geprüft: {n - ungeprueft} | noch nie geprüft: {ungeprueft} "
          f"| RIS-Betreiber bisher: {len(betr)}\n",
          "## Je Bundesland\n",
          "| Land | Gemeinden | RIS gefunden | gesperrt | kein RIS | ungeprüft |",
          "|---|---:|---:|---:|---:|---:|"]
    for l, c in sorted(land.items(), key=lambda kv: -kv[1]["gesamt"]):
        md.append(f"| {l} | {c['gesamt']} | {c['gefunden']} | {c['gesperrt']} | "
                  f"{c['kein_ris'] + c['keine_homepage']} | {c['ungeprueft']} |")
    md += ["\n## Plattformen (nur bereits gefundene RIS)\n",
           "| Plattform | Betreiber | Gemeinden | Adapter vorhanden |", "|---|---:|---:|---|"]
    for name, p in sorted(pl.items(), key=lambda kv: -kv[1]["gemeinden"]):
        md.append(f"| {name} | {p['betreiber']} | {p['gemeinden']} | {p['adapter']} |")
    offen = [(n_, p) for n_, p in pl.items() if p["adapter"] in ("nein", "teilweise (HTML)", "teilweise (auto)")]
    md += ["\n## Adapter-Ranking (fehlend oder nur teilweise)\n"]
    for n_, p in sorted(offen, key=lambda kv: -kv[1]["gemeinden"]):
        md.append(f"- {n_}: {p['gemeinden']} Gemeinden / {p['betreiber']} Betreiber ({p['adapter']})")
    gesperrt = [b for b in betr.values() if b["status"] == "gesperrt"]
    if gesperrt:
        md += ["\n## Per robots.txt gesperrt (Betreiber um Erlaubnis bitten)\n"]
        md += [f"- {b['betreiber']} ({len(b['gemeinden'])} Gemeinden)" for b in gesperrt]
    md.append("\nHinweis: Die Plattformzahlen beruhen nur auf den bisher geprüften Gemeinden. "
              "Sie werden belastbar, sobald quellen_entdecken.py alle Länder durchlaufen hat.\n")
    with open(os.path.join(a.out, "abdeckung.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

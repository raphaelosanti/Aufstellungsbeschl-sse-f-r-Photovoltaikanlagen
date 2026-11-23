#!/usr/bin/env python3
"""
MaStR-Abgleich: Wo gibt es Freiflächen-PV, aber (noch) keinen Beschluss im Register?
====================================================================================

Liest die Solareinheiten des Marktstammdatenregisters (Datenbank von `open-mastr`, bzw. CSV) und
aggregiert Freiflächenanlagen je Gemeinde. Dann wird abgeglichen mit
  * dem Register (ausgabe/PV_Beschluesse_Gesamt.xlsx, Blatt "Projekte") und
  * der Gemeindetabelle (daten/gemeinden.csv: ris_status, ris_typ),
und je Gemeinde eine Kategorie vergeben, warum sie noch fehlt:

  im Register             Beschluss gefunden
  Quelle ohne Treffer     RIS/Quelle angebunden, aber nichts gefunden (Filter/Zeitraum/Adapter prüfen)
  kein RIS                kein RIS erkannt (Homepage-Crawler oder Landesportal nötig)
  ungeprüft               Gemeinde noch nicht untersucht
  keine Homepage          Wikidata kennt keine Homepage
  gesperrt                robots.txt verbietet Zugriff
  unbekannt               Gemeinde nicht in der Gemeindetabelle (Namensabgleich fehlgeschlagen)

Ausgabe (Ordner entdeckung/):
  mastr_gemeinden.csv   eine Zeile je Gemeinde mit Freiflächen-PV
  mastr_bericht.md      Zusammenfassung je Bundesland und Kategorie

Aufruf:
  python mastr_abgleich.py --db ~/.open-MaStR/data/sqlite/open-mastr.db
  python mastr_abgleich.py --csv solar.csv        # Testmodus
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
import sys
import unicodedata
from collections import Counter, defaultdict

SPALTEN = {
    "ags": ("Gemeindeschluessel", "municipality_key", "Gemeindeschlüssel"),
    "gemeinde": ("Gemeinde", "municipality"),
    "landkreis": ("Landkreis", "district"),
    "land": ("Bundesland", "federal_state", "state"),
    "lage": ("Lage", "location", "Lage der Einheit"),
    "status": ("EinheitBetriebsstatus", "operating_status", "Betriebsstatus"),
    "mw": ("Bruttoleistung", "gross_power", "Nettonennleistung", "net_rated_power"),
    "reg": ("EinheitRegistrierungsdatum", "registration_date", "Registrierungsdatum"),
    "ibn": ("Inbetriebnahmedatum", "commissioning_date"),
}
BUNDESLAND_ALIAS = {"Baden-Wuerttemberg": "Baden-Württemberg", "Thueringen": "Thüringen",
                    "Nordrhein-Westfalen": "Nordrhein-Westfalen", "Freie Hansestadt Bremen": "Bremen",
                    "Freie und Hansestadt Hamburg": "Hamburg"}


def norm(name: str) -> str:
    s = unicodedata.normalize("NFKD", (name or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c)).replace("ß", "ss")
    s = re.sub(r"\(.*?\)|,.*$", "", s)                                   # "Neuruppin, Stadt" -> "neuruppin"
    s = re.sub(r"\b(stadt|gemeinde|markt|landeshauptstadt|hansestadt|kreisstadt|amt|ot|ortsteil)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


def zahl(v) -> float:
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return 0.0


def wahl(spalten: list[str], arten: tuple[str, ...]) -> str | None:
    klein = {c.lower(): c for c in spalten}
    for a in arten:
        if a.lower() in klein:
            return klein[a.lower()]
    return None


def zeilen_aus_db(pfad: str, protokoll: str = ""):
    con = sqlite3.connect(pfad)
    tabellen = [r[0] for r in con.execute("select name from sqlite_master where type in ('table','view')")]
    print("Tabellen:", ", ".join(tabellen), flush=True)
    info = ["Tabellen: " + ", ".join(tabellen)]
    wahl_t = None
    for t in [x for x in tabellen if "solar" in x.lower()]:
        cur = con.execute(f'select * from "{t}" limit 1')
        cols = [d[0] for d in cur.description]
        n = con.execute(f'select count(*) from "{t}"').fetchone()[0]
        info.append(f"\n## {t} ({n} Zeilen)\n" + ", ".join(cols))
        print(f"{t}: {n} Zeilen, Spalten: {', '.join(cols)}", flush=True)
        if wahl_t is None and (wahl(cols, SPALTEN["gemeinde"]) or wahl(cols, SPALTEN["ags"])) \
                and wahl(cols, SPALTEN["lage"]):
            wahl_t = t
    if protokoll:   # Spalten immer ablegen, damit sich Namen prüfen lassen
        os.makedirs(os.path.dirname(protokoll) or ".", exist_ok=True)
        open(protokoll, "w", encoding="utf-8").write("\n".join(info) + "\n")
    if not wahl_t:
        raise SystemExit("Keine Solar-Tabelle mit Gemeinde/Gemeindeschlüssel und Lage gefunden – "
                         "Spaltennamen siehe Ausgabe oder entdeckung/mastr_spalten.txt")
    print(f"Nutze Tabelle {wahl_t}", flush=True)
    cur = con.execute(f'select * from "{wahl_t}"')
    cols = [d[0] for d in cur.description]
    while True:
        block = cur.fetchmany(50000)
        if not block:
            break
        for r in block:
            yield dict(zip(cols, r))


def zeilen_aus_csv(pfad: str):
    with open(pfad, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def aggregiere(zeilen, min_mw: float, reg_ab: str):
    agg: dict[tuple, dict] = {}
    lagen: Counter = Counter()
    stati: Counter = Counter()
    sp = None
    for r in zeilen:
        if sp is None:
            sp = {k: wahl(list(r), v) for k, v in SPALTEN.items()}
            print("Spalten:", {k: v for k, v in sp.items()})
        lage = str(r.get(sp["lage"]) or "")
        lagen[lage] += 1
        if not re.search(r"freifl|ground|open", lage, re.I):
            continue
        status = str(r.get(sp["status"]) or "") if sp["status"] else ""
        stati[status] += 1
        if status and not re.search(r"planung|betrieb|planned|operation", status, re.I):
            continue                                   # z. B. endgültig stillgelegt
        reg = str(r.get(sp["reg"]) or "")[:10] if sp["reg"] else ""
        if reg and reg < reg_ab:
            continue
        mw = zahl(r.get(sp["mw"])) / 1000 if sp["mw"] else 0.0
        if mw < min_mw:
            continue
        land = BUNDESLAND_ALIAS.get(str(r.get(sp["land"]) or ""), str(r.get(sp["land"]) or ""))
        name = str(r.get(sp["gemeinde"]) or "")
        ags = re.sub(r"\D", "", str(r.get(sp["ags"]) or "")).zfill(8)[:8] if sp["ags"] and r.get(sp["ags"]) else ""
        key = (ags or norm(name), land)
        a = agg.setdefault(key, {"ags": ags, "gemeinde": name, "landkreis": str(r.get(sp["landkreis"]) or ""),
                                 "land": land, "anlagen": 0, "mw": 0.0, "in_planung": 0, "mw_planung": 0.0, "reg_max": ""})
        a["anlagen"] += 1
        a["mw"] += mw
        if re.search(r"planung|planned", status, re.I):
            a["in_planung"] += 1
            a["mw_planung"] += mw
        a["reg_max"] = max(a["reg_max"], reg)
    return list(agg.values()), lagen, stati


def lade_register(xlsx: str) -> Counter:
    import openpyxl
    z: Counter = Counter()
    if not os.path.exists(xlsx):
        return z
    ws = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)["Projekte"]
    it = ws.iter_rows(values_only=True)
    kopf = [str(k) for k in next(it)]
    for row in it:
        r = dict(zip(kopf, row))
        z[(norm(str(r.get("Gemeinde") or "")), str(r.get("Bundesland") or ""))] += 1
    return z


def kategorie(g: dict, reg: Counter, tab_ags: dict, tab_name: dict) -> tuple[str, dict]:
    t = tab_ags.get(g["ags"]) or tab_name.get((norm(g["gemeinde"]), g["land"]))
    if reg.get((norm(g["gemeinde"]), g["land"])) or (t and reg.get((norm(t["name"]), t["land"]))):
        return "im Register", t or {}
    if not t:
        return "unbekannt", {}
    s = t["ris_status"]
    if s == "gefunden":
        return "Quelle ohne Treffer", t
    return {"kein_ris": "kein RIS", "": "ungeprüft", "keine_homepage": "keine Homepage",
            "gesperrt": "gesperrt"}.get(s, "unbekannt"), t


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db"), ap.add_argument("--csv")
    ap.add_argument("--register", default=os.path.join("ausgabe", "PV_Beschluesse_Gesamt.xlsx"))
    ap.add_argument("--gemeinden", default=os.path.join("daten", "gemeinden.csv"))
    ap.add_argument("--out", default="entdeckung")
    ap.add_argument("--min-mw", type=float, default=1.0, help="nur Anlagen ab dieser Leistung (MW)")
    ap.add_argument("--reg-ab", default="2021-01-01", help="nur im MaStR registriert ab (Aufstellungsbeschlüsse sind jünger)")
    a = ap.parse_args()
    if not (a.db or a.csv):
        ap.error("--db oder --csv angeben")

    zeilen = zeilen_aus_db(os.path.expanduser(a.db), os.path.join(a.out, "mastr_spalten.txt")) if a.db else zeilen_aus_csv(a.csv)
    gem, lagen, stati = aggregiere(zeilen, a.min_mw, a.reg_ab)
    reg = lade_register(a.register)
    tab = list(csv.DictReader(open(a.gemeinden, encoding="utf-8"))) if os.path.exists(a.gemeinden) else []
    tab_ags = {t["ags"].zfill(8): t for t in tab}
    tab_name = {(norm(t["name"]), t["land"]): t for t in tab}

    os.makedirs(a.out, exist_ok=True)
    zaehl: dict[str, Counter] = defaultdict(Counter)
    ausgabe = []
    for g in sorted(gem, key=lambda x: -x["mw"]):
        kat, t = kategorie(g, reg, tab_ags, tab_name)
        zaehl[g["land"]][kat] += 1
        ausgabe.append({**g, "mw": round(g["mw"], 1), "mw_planung": round(g["mw_planung"], 1),
                        "kategorie": kat, "ris_typ": t.get("ris_typ", ""), "ris_url": t.get("ris_url", ""),
                        "web": t.get("web", "")})
    felder = ["land", "gemeinde", "landkreis", "ags", "anlagen", "mw", "in_planung", "mw_planung", "reg_max",
              "kategorie", "ris_typ", "ris_url", "web"]
    with open(os.path.join(a.out, "mastr_gemeinden.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, felder)
        w.writeheader()
        w.writerows(ausgabe)

    kats = ["im Register", "Quelle ohne Treffer", "kein RIS", "ungeprüft", "keine Homepage", "gesperrt", "unbekannt"]
    gesamt = Counter()
    for c in zaehl.values():
        gesamt.update(c)
    md = ["# MaStR-Abgleich: Gemeinden mit Freiflächen-PV", "",
          f"Freiflächenanlagen ab {a.min_mw:g} MW, im MaStR registriert ab {a.reg_ab}, Status In Planung/In Betrieb. "
          f"{len(gem)} Gemeinden.", "",
          "| Bundesland | Gemeinden | " + " | ".join(kats) + " |", "|---|---:|" + "---:|" * len(kats)]
    for land in sorted(zaehl):
        c = zaehl[land]
        md.append(f"| {land} | {sum(c.values())} | " + " | ".join(str(c[k]) for k in kats) + " |")
    md.append(f"| **Gesamt** | **{sum(gesamt.values())}** | " + " | ".join(f"**{gesamt[k]}**" for k in kats) + " |")
    md += ["", "Gedeckt ist nur 'im Register'. 'Quelle ohne Treffer' heißt: RIS angebunden, aber nichts Passendes gefunden – "
           "dort lohnt die Prüfung von Filter, Zeitraum und Adapter. Die anderen Kategorien sind Erkennungslücken.", "",
           "## Zur Kontrolle der Spaltenwerte", "", "Lage der Einheit (häufigste):",
           *[f"- {k or '(leer)'}: {v}" for k, v in lagen.most_common(8)], "", "Betriebsstatus (Freifläche):",
           *[f"- {k or '(leer)'}: {v}" for k, v in stati.most_common(8)]]
    with open(os.path.join(a.out, "mastr_bericht.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md[:30]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

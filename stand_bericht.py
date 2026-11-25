#!/usr/bin/env python3
"""
STAND.md automatisch erzeugen: was ist bisher passiert, was fehlt, wie hoch ist die Trefferquote
==============================================================================================

Liest nur Dateien des Repos (daten/, quellen_*.csv, entdeckung/mastr_gemeinden.csv) und schreibt

  STAND.md                 Kennzahlen, Verlauf, Ereignisse, Abdeckung je Land, Trefferquote gegenüber MaStR
  daten/verlauf.csv        eine Zeile pro Tag (Kennzahlen), wird fortgeschrieben
  daten/ereignisse.csv     Protokoll: neue Projekte, erkannte Aufstellungsbeschlüsse, Phasenwechsel
  daten/projektstand.json  letzter bekannter Stand je Projekt (Vergleichsbasis für die Ereignisse)

Aufruf (am Ende jedes Laufs):  python stand_bericht.py
Beim ersten Aufruf werden vorhandene Projekte nur als Ausgangsstand übernommen, nicht als Ereignis gemeldet.

Trefferquote: Die Erwartung kommt aus dem Marktstammdatenregister (MaStR): Gemeinden mit Freiflächen-PV ab 1 MW,
registriert ab 2021. Das ist eine Näherung, kein Soll. Nicht jede Anlage braucht einen Bebauungsplan
(privilegierte Streifen an Autobahn/Schiene), und manche Aufstellungsbeschlüsse liegen vor dem Erfassungszeitraum.
"""
from __future__ import annotations

import csv
import datetime as dt
import glob
import json
import os
import sys
from collections import Counter, defaultdict

from mastr_abgleich import kategorie, norm

LAENDER = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen",
           "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland",
           "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"]
VERLAUF_FELDER = ["datum", "projekte", "aufstellung", "unklar_projekte", "beschluesse", "unklar_beschluesse",
                  "quellen", "quellen_geprueft", "gemeinden_geprueft", "gemeinden_ris", "gemeinden_kein_ris",
                  "gemeinden_ungeprueft", "mastr_gemeinden", "mastr_im_register", "mastr_quelle_ohne_treffer"]
PHASEN = ["Frühphase", "Auslegung/Abwägung", "Satzung/rechtskräftig", "Unklar"]


def phase_fuer(typen: set[str]) -> str:
    if typen & {"Satzungsbeschluss", "Inkrafttreten/Bekanntmachung"}:
        return "Satzung/rechtskräftig"
    if typen & {"Entwurfs-/Auslegungsbeschluss", "Abwägungsbeschluss"}:
        return "Auslegung/Abwägung"
    if typen & {"Aufstellungsbeschluss", "Frühzeitige Beteiligung"}:
        return "Frühphase"
    return "Unklar"


def lade_beschluesse(daten: str) -> list[dict]:
    out = []
    for f in sorted(glob.glob(os.path.join(daten, "beschluesse_*.jsonl"))):
        with open(f, encoding="utf-8") as fh:
            for zeile in fh:
                zeile = zeile.strip()
                if zeile:
                    out.append(json.loads(zeile))
    return out


def lade_csv(pfad: str) -> list[dict]:
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def projekte_aus(beschluesse: list[dict]) -> dict[str, dict]:
    pro: dict[str, list[dict]] = defaultdict(list)
    for b in beschluesse:
        if b.get("projekt_id"):
            pro[b["projekt_id"]].append(b)
    res = {}
    for pid, ev in pro.items():
        echt = [e for e in ev if not e.get("negativ")]
        typen = {e["beschlusstyp"] for e in echt}
        aufst = sorted(e["datum"] for e in echt if e["beschlusstyp"] == "Aufstellungsbeschluss" and e.get("datum"))
        res[pid] = {"gemeinde": ev[0].get("gemeinde", ""), "land": ev[0].get("bundesland", ""),
                    "planname": next((e.get("planname") for e in ev if e.get("planname")), ""),
                    "phase": phase_fuer(typen), "aufstellung": bool(typen & {"Aufstellungsbeschluss"}),
                    "aufstellung_datum": aufst[0] if aufst else "", "beschluesse": len(ev)}
    return res


def ereignisse_bestimmen(proj: dict[str, dict], alt: dict, heute: str) -> list[dict]:
    if not alt:
        return []                                   # erster Lauf: nur Ausgangsstand
    ev = []
    for pid, p in sorted(proj.items()):
        a = alt.get(pid)
        name = p["planname"] or p["gemeinde"]
        if a is None:
            ev.append({"datum": heute, "art": "neues Projekt", "projekt_id": pid, "gemeinde": p["gemeinde"],
                       "land": p["land"], "text": f"{name} (Phase: {p['phase']})"})
            continue
        if p["aufstellung"] and not a.get("aufstellung"):
            ev.append({"datum": heute, "art": "Aufstellungsbeschluss erkannt", "projekt_id": pid,
                       "gemeinde": p["gemeinde"], "land": p["land"],
                       "text": f"{name}, Beschluss vom {p['aufstellung_datum'] or 'unbekanntem Datum'}"})
        if p["phase"] != a.get("phase"):
            ev.append({"datum": heute, "art": "Phase geändert", "projekt_id": pid, "gemeinde": p["gemeinde"],
                       "land": p["land"], "text": f"{name}: {a.get('phase')} → {p['phase']}"})
    return ev


def md_tabelle(kopf: list[str], zeilen: list[list], rechts_ab: int = 1) -> list[str]:
    out = ["| " + " | ".join(kopf) + " |",
           "|" + "|".join("---" if i < rechts_ab else "---:" for i in range(len(kopf))) + "|"]
    out += ["| " + " | ".join(str(c) for c in z) + " |" for z in zeilen]
    return out


def pct(a: float, b: float) -> str:
    return f"{100 * a / b:.1f} %" if b else "–"


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--daten", default="daten")
    ap.add_argument("--out", default="STAND.md")
    ap.add_argument("--mastr", default=os.path.join("entdeckung", "mastr_gemeinden.csv"))
    a = ap.parse_args()
    heute = dt.date.today().isoformat()

    beschluesse = lade_beschluesse(a.daten)
    proj = projekte_aus(beschluesse)
    gem = lade_csv(os.path.join(a.daten, "gemeinden.csv"))
    quellen = lade_csv("quellen_alle.csv")
    homepage = []                                  # alle weiteren Quellenlisten (Homepage, Hessen-Verzeichnis, IHK, Amtsblatt)
    for f in ("quellen_homepage.csv", "quellen_verzeichnis.csv", "quellen_ihk.csv", "quellen_amtsblatt.csv"):
        homepage += lade_csv(f)
    nach_typ = Counter((q.get("typ") or "?") for q in quellen + homepage)
    mastr = lade_csv(a.mastr)

    # --- Quellen: wann zuletzt gelaufen, wie viele Treffer ------------------------------------------
    zuletzt: dict[tuple[str, str], str] = {}
    for f in glob.glob(os.path.join(a.daten, "marken_*.json")):
        try:
            m = json.load(open(f, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for name, v in m.items():
            if isinstance(v, dict) and v.get("zuletzt"):
                zuletzt[(name, os.path.basename(f))] = v["zuletzt"]
    nach_land_q = defaultdict(lambda: Counter())
    for q in quellen + homepage:
        nach_land_q[q["bundesland"]]["quellen"] += 1
    letzte_tage = (dt.date.today() - dt.timedelta(days=2)).isoformat()
    quellen_geprueft = len(zuletzt)
    jung = sum(1 for d in zuletzt.values() if d >= letzte_tage)
    letzter_lauf = max(zuletzt.values(), default="–")

    # --- Gemeinden -----------------------------------------------------------------------------------
    gz = Counter(g["ris_status"] or "ungeprüft" for g in gem)
    gland = defaultdict(Counter)
    for g in gem:
        gland[g["land"]][g["ris_status"] or "ungeprüft"] += 1

    # --- Kennzahlen je Land --------------------------------------------------------------------------
    pl = defaultdict(Counter)
    for p in proj.values():
        pl[p["land"]]["projekte"] += 1
        pl[p["land"]]["aufst"] += p["aufstellung"]
        pl[p["land"]][p["phase"]] += 1
    bl = Counter(b.get("bundesland", "") for b in beschluesse)
    unklar_b = sum(1 for b in beschluesse if b["beschlusstyp"] == "Unklar")

    # --- MaStR-Abgleich (live gegen das aktuelle Register) -------------------------------------------
    reg = Counter((norm(p["gemeinde"]), p["land"]) for p in proj.values())
    reg_gem = set(reg)
    tab_ags = {t["ags"].zfill(8): t for t in gem}
    tab_name = {(norm(t["name"]), t["land"]): t for t in gem}
    kat_land = defaultdict(Counter)
    parks_gesamt = 0
    for g in mastr:
        k, _ = kategorie(g, reg, tab_ags, tab_name)
        kat_land[g["land"]][k] += 1
        n_parks = max(1, len([x for x in (g.get("parks") or "").split(";") if x.strip()]))
        parks_gesamt += n_parks
    kat = Counter()
    for c in kat_land.values():
        kat.update(c)
    N = len(mastr)
    n_reg, n_ohne = kat["im Register"], kat["Quelle ohne Treffer"]
    erreichbar = n_reg + n_ohne

    # --- Verlauf / Ereignisse fortschreiben ----------------------------------------------------------
    zeile = {"datum": heute, "projekte": len(proj), "aufstellung": sum(p["aufstellung"] for p in proj.values()),
             "unklar_projekte": sum(1 for p in proj.values() if p["phase"] == "Unklar"),
             "beschluesse": len(beschluesse), "unklar_beschluesse": unklar_b,
             "quellen": len(quellen) + len(homepage), "quellen_geprueft": quellen_geprueft,
             "gemeinden_geprueft": len(gem) - gz["ungeprüft"], "gemeinden_ris": gz["gefunden"],
             "gemeinden_kein_ris": gz["kein_ris"], "gemeinden_ungeprueft": gz["ungeprüft"],
             "mastr_gemeinden": N, "mastr_im_register": n_reg, "mastr_quelle_ohne_treffer": n_ohne}
    vpfad = os.path.join(a.daten, "verlauf.csv")
    verlauf = [r for r in lade_csv(vpfad) if r["datum"] != heute]
    vorher = verlauf[-1] if verlauf else None
    verlauf.append({k: str(v) for k, v in zeile.items()})
    with open(vpfad, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, VERLAUF_FELDER)
        w.writeheader()
        w.writerows(verlauf)

    spfad = os.path.join(a.daten, "projektstand.json")
    alt = json.load(open(spfad, encoding="utf-8")) if os.path.exists(spfad) else {}
    neu_ev = ereignisse_bestimmen(proj, alt, heute)
    epfad = os.path.join(a.daten, "ereignisse.csv")
    ereignisse = lade_csv(epfad)
    # Läuft der Bericht am selben Tag zweimal, bleiben Ereignisse des Tages erhalten (kein Doppeln)
    bekannt = {(e["datum"], e["art"], e["projekt_id"], e["text"]) for e in ereignisse}
    ereignisse += [e for e in neu_ev if (e["datum"], e["art"], e["projekt_id"], e["text"]) not in bekannt]
    felder_e = ["datum", "art", "projekt_id", "gemeinde", "land", "text"]
    with open(epfad, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, felder_e)
        w.writeheader()
        w.writerows(ereignisse)
    with open(spfad, "w", encoding="utf-8") as f:
        json.dump({k: {"phase": v["phase"], "aufstellung": v["aufstellung"]} for k, v in proj.items()}, f,
                  ensure_ascii=False, indent=0, sort_keys=True)

    # --- Markdown ------------------------------------------------------------------------------------
    def delta(key: str) -> str:
        if not vorher:
            return ""
        d = int(zeile[key]) - int(vorher.get(key) or 0)
        return f" ({d:+d} seit {vorher['datum']})" if d else f" (unverändert seit {vorher['datum']})"

    md = [f"# Stand des PV-Beschlussregisters ({dt.date.today().strftime('%d.%m.%Y')})", "",
          "Diese Datei wird nach jedem Lauf automatisch erzeugt (`stand_bericht.py`). Konzept und Ablauf stehen in "
          "`KONZEPT.md`, der Verlauf in `daten/verlauf.csv`, das Protokoll in `daten/ereignisse.csv`.", "",
          "## Kennzahlen", "",
          f"- **Projekte:** {zeile['projekte']}{delta('projekte')}",
          f"- **davon mit Aufstellungsbeschluss:** {zeile['aufstellung']}{delta('aufstellung')}",
          f"- **Phase noch unklar:** {zeile['unklar_projekte']} Projekte{delta('unklar_projekte')}; "
          f"{unklar_b} Beschlüsse mit unklarem Typ{delta('unklar_beschluesse')}",
          f"- **Beschlüsse insgesamt:** {zeile['beschluesse']}{delta('beschluesse')}",
          f"- **Quellen nach Art:** " + ", ".join(f"{t} {n}" for t, n in nach_typ.most_common()),
          f"- **Quellen:** {zeile['quellen']} angebunden, davon {quellen_geprueft} schon abgefragt, "
          f"{jung} in den letzten 2 Tagen; letzter Abruf {letzter_lauf}",
          f"- **Gemeinden:** {len(gem)} bekannt, {len(gem) - gz['ungeprüft']} geprüft "
          f"({gz['gefunden']} mit RIS, {gz['kein_ris']} ohne erkanntes RIS, {gz['keine_homepage']} ohne Homepage, "
          f"{gz['gesperrt']} gesperrt), {gz['ungeprüft']} noch nie geprüft", ""]

    md += ["## Trefferquote gegenüber der Erwartung (MaStR)", "",
           f"Erwartung: {N} Gemeinden mit Freiflächen-PV ab 1 MW, im MaStR seit 2021 registriert "
           f"(mindestens {parks_gesamt} Parks). Wo ein Park gebaut oder geplant wird, gab es meist einen Bebauungsplan "
           f"und damit einen Aufstellungsbeschluss. Das ist eine Näherung, kein Soll.", "",
           *md_tabelle(["Maß", "Wert", "Bedeutung"], [
               ["Gesamt-Trefferquote", f"{n_reg} von {N} = {pct(n_reg, N)}",
                "Gemeinden mit MaStR-Freiflächenpark, für die das Register ein Projekt hat"],
               ["Erreichbarkeit", f"{erreichbar} von {N} = {pct(erreichbar, N)}",
                "Gemeinden, deren RIS angebunden ist (Treffer oder nicht)"],
               ["Trefferquote bei erreichbarer Quelle", f"{n_reg} von {erreichbar} = {pct(n_reg, erreichbar)}",
                "Wo wir suchen können: wie oft finden wir etwas?"],
               ["Register-Gemeinden außerhalb der MaStR-Liste", f"{len(reg_gem) - n_reg} von {len(reg_gem)}",
                "Gemeinden mit Projekt im Register, aber ohne MaStR-Freiflächenpark ab 1 MW: Frühphase, noch nicht "
                "registriert (der eigentliche Mehrwert) oder Namensabgleich"],
           ], 3), "",
           f"Gesamt = Erreichbarkeit × Trefferquote bei Quelle ({pct(erreichbar, N)} × {pct(n_reg, erreichbar)}). "
           "Der Verlust liegt also vor allem bei der Erreichbarkeit, nicht beim Filter."]
    if erreichbar and n_reg:
        rate = n_reg / erreichbar
        md += ["",
               f"**Grobe Hochrechnung:** Wären alle {N} Gemeinden erreichbar und die Trefferquote bliebe bei "
               f"{pct(n_reg, erreichbar)}, ergäbe das etwa {round(N * rate)} Gemeinden mit Projekt (heute {n_reg}). Die Quote ist vermutlich zu niedrig angesetzt: Aufstellungsbeschlüsse vor "
               f"{os.environ.get('SEIT', '2022')} sind nicht erfasst, und privilegierte Anlagen haben keinen Beschluss. "
               f"Andererseits sind Projekte, die noch nicht im MaStR stehen (genau die Frühphase), in der Erwartung gar "
               f"nicht enthalten. Die wahre Zahl liegt also eher darüber."]
    md += ["", "Je Bundesland (MaStR-Gemeinden):", ""]
    zl = []
    for land in LAENDER:
        c = kat_land.get(land, Counter())
        n = sum(c.values())
        if not n:
            continue
        er = c["im Register"] + c["Quelle ohne Treffer"]
        zl.append([land, n, c["im Register"], c["Quelle ohne Treffer"], c["kein RIS"], c["ungeprüft"],
                   c["keine Homepage"] + c["gesperrt"] + c["unbekannt"], pct(c["im Register"], n), pct(er, n)])
    md += md_tabelle(["Land", "MaStR-Gemeinden", "im Register", "Quelle ohne Treffer", "kein RIS", "ungeprüft",
                      "sonstige", "Treffer", "erreichbar"], zl)

    md += ["", "## Je Bundesland", ""]
    zl = []
    for land in LAENDER:
        g = gland.get(land, Counter())
        p = pl.get(land, Counter())
        zl.append([land, nach_land_q[land]["quellen"], sum(g.values()), g["gefunden"], g["kein_ris"], g["ungeprüft"],
                   p["projekte"], p["aufst"], p["Frühphase"], p["Auslegung/Abwägung"], p["Satzung/rechtskräftig"],
                   p["Unklar"]])
    zl.append(["**Gesamt**"] + [f"**{sum(r[i] for r in zl)}**" for i in range(1, 12)])
    md += md_tabelle(["Land", "Quellen", "Gemeinden", "RIS", "kein RIS", "ungeprüft", "Projekte", "mit Aufst.-Beschl.",
                      "Frühphase", "Auslegung/Abwägung", "Satzung", "Unklar"], zl)

    md += ["", "## Was zuletzt passiert ist", ""]
    if not ereignisse:
        md.append("Noch keine Ereignisse. Ab dem nächsten Lauf werden neue Projekte, erkannte Aufstellungsbeschlüsse "
                  "und Phasenwechsel hier protokolliert (Ausgangsstand heute: "
                  f"{len(proj)} Projekte).")
    else:
        for e in reversed(ereignisse[-30:]):
            md.append(f"- {e['datum']} · {e['art']} · {e['gemeinde']} ({e['land']}): {e['text']}")
    md += ["", "## Verlauf", ""]
    md += md_tabelle(["Datum", "Projekte", "mit Aufst.-Beschl.", "Unklar", "Beschlüsse", "Quellen abgefragt",
                      "Gemeinden geprüft", "MaStR im Register"],
                     [[r["datum"], r["projekte"], r["aufstellung"], r["unklar_projekte"], r["beschluesse"],
                       r["quellen_geprueft"], r["gemeinden_geprueft"], r["mastr_im_register"]]
                      for r in verlauf[-15:]][::-1])

    md += ["", "## Offene Hebel (Zahlen von heute)", "",
           f"- {kat['Quelle ohne Treffer']} MaStR-Gemeinden haben ein angebundenes RIS, aber keinen Treffer: Filter, "
           f"Zeitraum (ab 2022) und Adapter prüfen.",
           f"- {kat['kein RIS']} MaStR-Gemeinden ohne erkanntes RIS: Homepage-Crawler (`quellen_homepage.csv`) und "
           f"Amt-Zuordnung.",
           f"- {kat['ungeprüft']} MaStR-Gemeinden noch nie geprüft: Quellensuche läuft täglich weiter.",
           f"- {gz['ungeprüft']} Gemeinden insgesamt noch nie geprüft.",
           f"- {zeile['unklar_projekte']} Projekte mit unklarer Phase: Schritt „Phase nachklären“ (Detailseiten/PDFs)."]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md[:40]))
    print(f"\nEreignisse neu: {len(neu_ev)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

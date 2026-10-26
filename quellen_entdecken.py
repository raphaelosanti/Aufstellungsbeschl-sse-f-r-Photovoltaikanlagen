#!/usr/bin/env python3
"""
Quellen-Entdeckung für das PV-Beschlussregister
===============================================

Baut quellen_*.csv automatisch auf:
 1. Holt alle Gemeinden eines Bundeslandes (über den amtlichen Gemeindeschlüssel) samt Homepage aus Wikidata.
 2. Sucht auf der Homepage nach dem Ratsinformationssystem (RIS).
 3. Prüft, ob dort OParl oder SessionNet läuft (gleiche Funktionen wie pv_beschluesse.py).
 4. Prüft robots.txt: gesperrte Systeme werden als auskommentierte Zeile (# ...) geschrieben.
 5. Dedupliziert: Ämter betreiben ein RIS für mehrere Gemeinden -> nur eine Zeile.

Aufruf (liegt im selben Ordner wie pv_beschluesse.py):
    python quellen_entdecken.py --max 20                 # Test mit 20 Gemeinden
    python quellen_entdecken.py                          # ganz Brandenburg
    python quellen_entdecken.py --land Brandenburg Sachsen-Anhalt Mecklenburg-Vorpommern
    python quellen_entdecken.py --raten                  # zusätzlich typische Subdomains probieren

Ergebnis:
    quellen_neu.csv   -> Zeilen prüfen, dann an quellen_brandenburg.csv anhängen
    ohne_ris.csv      -> Gemeinden ohne gefundenes RIS (manuell nachrecherchieren)

Wiederholungsläufe sind schnell, weil Http() alles in .cache_pv cached.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

import pv_beschluesse as pv

WIKIDATA = "https://query.wikidata.org/sparql"
# Präfix des amtlichen Gemeindeschlüssels (AGS) je Bundesland
BUNDESLAENDER = {
    "Schleswig-Holstein": "01", "Niedersachsen": "03", "Nordrhein-Westfalen": "05", "Hessen": "06",
    "Rheinland-Pfalz": "07", "Baden-Württemberg": "08", "Bayern": "09", "Saarland": "10",
    "Brandenburg": "12", "Mecklenburg-Vorpommern": "13", "Sachsen": "14",
    "Sachsen-Anhalt": "15", "Thüringen": "16",
}

RIS_HREF = re.compile(
    r"ratsinfo|buergerinfo|buerger-?info|sitzungsdienst|sessionnet|allris|si0040|si0046|gr0040|"
    r"oparl|mandatos|kommunalportal|sdnet|ratsinformation|/bi/|sitzungskalender|gremieninfo", re.I)
RIS_TEXT = re.compile(
    r"ratsinfo|bürgerinfo|buergerinfo|sitzungsdienst|sitzungskalender|gremieninfo|ratsinformation|"
    r"bürgerinformation|allris|sitzungen|gremien|sitzungstermine", re.I)
SUBDOMAINS = ["ratsinfo", "buergerinfo", "sessionnet", "sitzung", "bi", "ris", "sitzungsdienst"]
PFADE = ["bi/", "buergerinfo/", "sessionnet/", "ratsinfo/"]


# --------------------------------------------------------------------------- #
# Gemeinden aus Wikidata
# --------------------------------------------------------------------------- #
def gemeinden(land: str, ags: str) -> list[dict]:
    """Leichte Abfrage: alle Items mit 8-stelligem Gemeindeschlüssel (P439) des Bundeslandes."""
    query = f"""
    SELECT ?item ?name ?web ?parentName WHERE {{
      ?item wdt:P439 ?ags .
      FILTER(STRSTARTS(?ags, "{ags}") && STRLEN(?ags) = 8)
      ?item rdfs:label ?name . FILTER(LANG(?name) = "de")
      OPTIONAL {{ ?item wdt:P856 ?web }}
      OPTIONAL {{ ?item wdt:P131 ?parent . ?parent rdfs:label ?parentName . FILTER(LANG(?parentName) = "de") }}
    }}"""
    letzter_fehler = None
    for versuch in range(4):
        try:
            r = requests.post(WIKIDATA, data={"query": query, "format": "json"},
                              headers={"User-Agent": pv.USER_AGENT, "Accept": "application/sparql-results+json"},
                              timeout=120)
            r.raise_for_status()
            break
        except requests.RequestException as e:
            letzter_fehler = e
            print(f"   Wikidata-Fehler ({e.__class__.__name__}), neuer Versuch in {20 * (versuch + 1)} s")
            time.sleep(20 * (versuch + 1))
    else:
        raise SystemExit(f"Wikidata nicht erreichbar: {letzter_fehler}")
    out: dict[str, dict] = {}
    for row in r.json()["results"]["bindings"]:
        item = row["item"]["value"]
        g = out.setdefault(item, {"name": row["name"]["value"], "web": "", "eltern": set(), "land": land})
        if "web" in row and not g["web"]:
            g["web"] = row["web"]["value"]
        if "parentName" in row:
            g["eltern"].add(row["parentName"]["value"])
    for g in out.values():
        g["landkreis"] = _landkreis(g["eltern"])
    return sorted(out.values(), key=lambda g: g["name"])


def _landkreis(eltern: set[str]) -> str:
    """Nur zur Info/Geocoding: direktes Elternobjekt, falls es kein Amt ist."""
    for e in sorted(eltern):
        if not e.startswith("Amt "):
            return re.sub(r"^Landkreis\s+", "", e)
    return ""


# --------------------------------------------------------------------------- #
# RIS finden und prüfen
# --------------------------------------------------------------------------- #
def norm_basis(url: str) -> str:
    p = urlparse(url)
    pfad = p.path
    if not pfad.endswith("/"):
        letzter = pfad.rsplit("/", 1)[-1]
        pfad = pfad.rsplit("/", 1)[0] + "/" if "." in letzter else pfad + "/"
    return f"{p.scheme}://{p.netloc}{pfad}"


def links_der_seite(http: pv.Http, url: str) -> list[tuple[int, str]]:
    try:
        soup = BeautifulSoup(http.get(url), "html.parser")
    except Exception:  # noqa: BLE001
        return []
    res = []
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"]).split("#")[0]
        if not href.startswith("http") or re.search(r"\.(pdf|docx?|xlsx?|jpe?g|png|zip)$", href, re.I):
            continue
        s = (2 if RIS_HREF.search(href) else 0) + (1 if RIS_TEXT.search(a.get_text(" ", strip=True)) else 0)
        if s:
            res.append((s, href))
    return res


def kandidaten(http: pv.Http, home: str) -> list[str]:
    stufe1 = sorted(set(links_der_seite(http, home)), reverse=True)
    cands = [u for _, u in stufe1]
    # Stufe 2: Unterseiten der eigenen Homepage ("Rathaus > Sitzungen") nach externem RIS absuchen
    host = urlparse(home).netloc
    for s, u in stufe1[:3]:
        if urlparse(u).netloc == host and s == 1:
            cands += [x for sc, x in links_der_seite(http, u) if sc >= 2]
    return list(dict.fromkeys(cands))[:6]


def pruefe(http: pv.Http, url: str):
    """Gibt (typ, url) zurück oder None."""
    base = norm_basis(url)
    if "ratsinfo-online.net" in base:
        return "auto", base
    try:
        o = pv.oparl_entdecken(http, base)
        if o:
            return "oparl", o
        if pv.ist_sessionnet(http, base):
            return "sessionnet", base
        for p in pv.UEBERSICHT_PFADE:          # ALLRIS 4 / ältere SessionNet-Varianten
            u = urljoin(base, p)
            try:
                if pv.DETAIL_LINK_RE.search(http.get(u, cache=False)):
                    return "html", u
            except Exception:  # noqa: BLE001
                continue
    except Exception:  # noqa: BLE001
        pass
    return None


def raten(domain: str) -> list[str]:
    d = domain.removeprefix("www.")
    return [f"https://{s}.{d}/" for s in SUBDOMAINS] + [f"https://{domain}/{p}" for p in PFADE]


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--land", nargs="+", default=["Brandenburg"], choices=sorted(BUNDESLAENDER))
    ap.add_argument("--bestehend", default="quellen_brandenburg.csv", help="vorhandene Quellen werden übersprungen")
    ap.add_argument("--out", default="quellen_neu.csv")
    ap.add_argument("--ohne", default="ohne_ris.csv")
    ap.add_argument("--raten", action="store_true", help="auch typische Subdomains/Pfade probieren (langsamer)")
    ap.add_argument("--max", type=int, default=0, help="nur die ersten N Gemeinden (zum Testen)")
    ap.add_argument("--pause", type=float, default=0.7)
    a = ap.parse_args()

    http = pv.Http(pause=a.pause)

    bekannt: set[str] = set()
    try:
        with open(a.bestehend, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("url"):
                    bekannt.add(norm_basis(row["url"]))
    except OSError:
        pass

    treffer: dict[str, dict] = {}     # basis-url -> Zeile
    ohne: list[dict] = []
    liste: list[dict] = []
    for land in a.land:
        print(f"Lade Gemeinden {land} aus Wikidata …")
        liste += gemeinden(land, BUNDESLAENDER[land])
    if a.max:
        liste = liste[:a.max]
    print(f"{len(liste)} Gemeinden\n")

    for i, g in enumerate(liste, 1):
        print(f"[{i}/{len(liste)}] {g['name']}", end=" ", flush=True)
        if not g["web"]:
            print("– keine Homepage in Wikidata")
            ohne.append({**_basis_zeile(g), "grund": "keine Homepage"})
            continue
        cands = kandidaten(http, g["web"])
        if a.raten and not cands:
            cands = raten(urlparse(g["web"]).netloc)
        gefunden = None
        for u in cands:
            gefunden = pruefe(http, u)
            if gefunden:
                break
        if not gefunden:
            print("– kein RIS erkannt")
            ohne.append({**_basis_zeile(g), "grund": "kein RIS erkannt", "kandidaten": " | ".join(cands[:3])})
            continue
        typ, url = gefunden
        basis = norm_basis(url)
        if basis in bekannt:
            print(f"– schon in {a.bestehend}")
            continue
        if basis in treffer:
            treffer[basis]["hinweis"] += f"; {g['name']}"
            print(f"– gleiches RIS wie {treffer[basis]['name'].removeprefix('# ')}")
            continue
        try:
            erlaubt = http._erlaubt(url)       # robots.txt
        except Exception:  # noqa: BLE001
            erlaubt = True
        name = g["name"] if erlaubt else f"# {g['name']}"
        treffer[basis] = {"name": name, "landkreis": g["landkreis"], "typ": typ, "url": url,
                          "bundesland": g["land"],
                          "hinweis": "" if erlaubt else "robots.txt verbietet Bots"}
        print(f"→ {typ} {url}{'' if erlaubt else '  (robots.txt gesperrt)'}")

    felder = ["name", "landkreis", "typ", "url", "bundesland", "hinweis"]
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        w.writeheader()
        w.writerows(treffer.values())
    with open(a.ohne, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "landkreis", "bundesland", "web", "grund", "kandidaten"])
        w.writeheader()
        for o in ohne:
            w.writerow({k: o.get(k, "") for k in w.fieldnames})

    frei = sum(1 for t in treffer.values() if not t["name"].startswith("#"))
    print(f"\n{len(treffer)} neue RIS ({frei} nutzbar, {len(treffer) - frei} per robots.txt gesperrt) → {a.out}")
    print(f"{len(ohne)} Gemeinden ohne RIS → {a.ohne}")
    return 0


def _basis_zeile(g: dict) -> dict:
    return {"name": g["name"], "landkreis": g["landkreis"], "bundesland": g["land"], "web": g["web"]}


if __name__ == "__main__":
    sys.exit(main())

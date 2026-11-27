#!/usr/bin/env python3
"""
Landkreise, Ämter/Verbandsgemeinden und Planungsverbände als Quellen (typ = homepage)
=====================================================================================

Viele kleine Gemeinden veröffentlichen Bekanntmachungen nur über das Amt / die Verbandsgemeinde / die
Verwaltungsgemeinschaft; Landkreise und Regionale Planungsverbände sind Träger öffentlicher Belange und
führen oft Listen der Bauleitplanverfahren ihrer Gemeinden. Diese Stellen werden hier aus Wikidata geholt
und für den Homepage-Crawler (pv_homepage.py) als eigene Quellen angelegt.

Ausgabe: quellen_verwaltung.csv (gleiches Format wie quellen_homepage.csv).
  * Landkreise/kreisfreie Städte: über den Kreisschlüssel (P439 mit 5 Stellen), Land aus den ersten zwei Ziffern
  * Gemeindeverbände und Planungsverbände: über die Klasse (P31) mit deutscher Bezeichnung, Land über P131+

Aufruf:  python verwaltung_entdecken.py
Das Protokoll nennt die Zahl der Treffer je Art; liefert eine Abfrage nichts, steht das dort (kein Abbruch).
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import time
from collections import Counter
from urllib.parse import urlparse

import requests

import pv_beschluesse as pv
from quellen_entdecken import BUNDESLAENDER, QUELLEN_FELDER, WIKIDATA

LAND_NACH_AGS = {v: k for k, v in BUNDESLAENDER.items()}
KLASSEN = [
    "Verbandsgemeinde", "Verbandsgemeinde in Rheinland-Pfalz", "Verbandsgemeinde in Sachsen-Anhalt",
    "Samtgemeinde", "Samtgemeinde in Niedersachsen",
    "Verwaltungsgemeinschaft", "Verwaltungsgemeinschaft in Bayern", "Verwaltungsgemeinschaft in Sachsen",
    "Verwaltungsgemeinschaft in Thüringen", "Verwaltungsgemeinschaft in Sachsen-Anhalt",
    "vereinbarte Verwaltungsgemeinschaft", "Gemeindeverwaltungsverband", "Verwaltungsverband",
    "Amt in Brandenburg", "Amt in Mecklenburg-Vorpommern", "Amt in Schleswig-Holstein",
    "Regionaler Planungsverband", "Regionale Planungsgemeinschaft", "Planungsverband", "Planungsregion",
    "Regionalverband",
]
ANDERE_LISTEN = ("quellen_homepage.csv", "quellen_verzeichnis.csv", "quellen_ihk.csv", "quellen_amtsblatt.csv")


def sparql(query: str) -> list[dict]:
    for versuch in range(4):
        try:
            r = requests.post(WIKIDATA, data={"query": query, "format": "json"}, timeout=180,
                              headers={"User-Agent": pv.USER_AGENT, "Accept": "application/sparql-results+json"})
            r.raise_for_status()
            return r.json()["results"]["bindings"]
        except (requests.RequestException, ValueError) as e:
            print(f"   Wikidata-Fehler ({e.__class__.__name__}), neuer Versuch in {20 * (versuch + 1)} s")
            time.sleep(20 * (versuch + 1))
    return []


def landkreise() -> list[dict]:
    q = """
    SELECT ?item ?name ?web ?ags WHERE {
      ?item wdt:P439 ?ags . FILTER(STRLEN(?ags) = 5)
      ?item wdt:P856 ?web .
      ?item rdfs:label ?name . FILTER(LANG(?name) = "de")
    }"""
    out = []
    for r in sparql(q):
        land = LAND_NACH_AGS.get(r["ags"]["value"][:2])
        if land:
            out.append({"name": r["name"]["value"], "url": r["web"]["value"], "land": land, "art": "Landkreis"})
    return out


def verbaende() -> list[dict]:
    klassen = " ".join(f'"{k}"@de' for k in KLASSEN)
    laender = " ".join(f'"{k}"@de' for k in BUNDESLAENDER)
    q = f"""
    SELECT ?item ?name ?web ?klasse ?land WHERE {{
      VALUES ?kl {{ {klassen} }}
      ?k rdfs:label ?kl .
      ?item wdt:P31 ?k .
      ?item wdt:P856 ?web .
      ?item rdfs:label ?name . FILTER(LANG(?name) = "de")
      VALUES ?ln {{ {laender} }}
      ?l rdfs:label ?ln .
      ?item wdt:P131+ ?l .
    }}"""
    out = []
    for r in sparql(q.replace("?klasse ?land", "?kl ?ln")):
        art = "Planungsverband" if re.search("plan|region", r["kl"]["value"], re.I) else "Amt/Verbandsgemeinde"
        out.append({"name": r["name"]["value"], "url": r["web"]["value"], "land": r["ln"]["value"], "art": art})
    return out


def host(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="quellen_verwaltung.csv")
    a = ap.parse_args()

    bekannt = set()
    for f in ANDERE_LISTEN + ("quellen_alle.csv",):
        if os.path.exists(f):
            with open(f, encoding="utf-8", newline="") as fh:
                bekannt |= {host(r["url"]) for r in csv.DictReader(fh) if r.get("url")}

    gefunden = landkreise()
    print(f"Landkreise/kreisfreie Städte mit Homepage: {len(gefunden)}")
    v = verbaende()
    print(f"Gemeindeverbände/Planungsverbände mit Homepage: {len(v)}  ({dict(Counter(x['art'] for x in v))})")
    gefunden += v

    zeilen, gesehen = [], set()
    for g in gefunden:
        h = host(g["url"])
        if not h or h in gesehen or h in bekannt:
            continue
        gesehen.add(h)
        hinweis = ("Landkreis: Bauleitplanung/Beteiligung der Träger öffentlicher Belange" if g["art"] == "Landkreis"
                   else "Planungsverband: Verfahren und Stellungnahmen" if g["art"] == "Planungsverband"
                   else "Amt/Verbandsgemeinde: Bekanntmachungen der Mitgliedsgemeinden")
        zeilen.append({"name": g["name"], "landkreis": "",   # leer: die Gemeinde wird im Text gesucht, nicht über den Landkreis eingegrenzt
                        "typ": "homepage", "url": g["url"],
                       "bundesland": g["land"], "hinweis": hinweis})
    zeilen.sort(key=lambda r: (r["bundesland"], r["hinweis"], r["name"]))
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=QUELLEN_FELDER)
        w.writeheader()
        w.writerows(zeilen)
    print(f"{len(zeilen)} neue Quellen in {a.out} (schon bekannte Hosts übersprungen: {len(gefunden) - len(zeilen)})")
    print(dict(Counter(z["bundesland"] for z in zeilen)))


if __name__ == "__main__":
    main()

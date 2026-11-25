#!/usr/bin/env python3
"""
GeoJSON-Export des PV-Beschlussregisters (Blatt "Projekte" der Gesamt-Excel).

Ein Feature je Projekt, Geometrie = Point [lon, lat] (WGS84). Aufbau der Properties lehnt sich an
das Netzausbauplan-GeoJSON (Stromnetz Hamburg) an: Name, Operator, Element, Type, Info, ...
damit beide Dateien in derselben Auswertung nebeneinander verwendet werden können.

Aufruf:
    python pv_geojson.py ausgabe/PV_Beschluesse_Gesamt.xlsx ausgabe/PV_Beschluesse.geojson
    python pv_geojson.py ausgabe/PV_Beschluesse_Gesamt.xlsx ausgabe/PV_Aufstellungsbeschluesse.geojson --nur-aufstellung
"""
from __future__ import annotations

import json
import sys

import openpyxl


def num(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def baue(xlsx: str, nur_aufstellung: bool = False) -> dict:
    ws = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)["Projekte"]
    zeilen = ws.iter_rows(values_only=True)
    kopf = [str(k) for k in next(zeilen)]
    features, ohne_koord = [], 0
    for z in zeilen:
        r = dict(zip(kopf, z))
        lat, lon = num(r.get("Breitengrad (lat)")), num(r.get("Längengrad (lon)"))
        if lat is None or lon is None:
            ohne_koord += 1
            continue
        auf = r.get("Aufstellungsbeschluss (Datum)") or ""
        if nur_aufstellung and not auf:
            continue
        mw = num(r.get("Leistung (MW)"))
        features.append({
            "type": "Feature",
            "properties": {
                "Name": r.get("Planname") or r.get("Projekt-ID"),
                "Project_ID": r.get("Projekt-ID"),
                "Operator": r.get("Projektentwickler") or "N/A",
                "Element": "Solar Park",
                "Type": r.get("Aufstellungskonzept") or "N/A",
                "Status": r.get("Status"),
                "Aufstellungsbeschluss": bool(auf),
                "Aufstellungsbeschluss_Date": auf if auf[:2] == "20" else None,
                "Phase": r.get("Phase"),
                "Last_Decision": r.get("Letzter Beschluss"),
                "Last_Decision_Date": r.get("Datum letzter Beschluss"),
                "First_Decision_Date": r.get("Erster Beschluss (Datum)"),
                "Municipality": r.get("Gemeinde"),
                "District": r.get("Landkreis"),
                "State": r.get("Bundesland"),
                "Area_ha": num(r.get("Fläche (ha)")),
                "Added Capacity": f"{mw:g} MVA" if mw else "N/A MVA",   # Schreibweise wie im Hamburg-File (MW ≈ MVA)
                "Location_Accuracy": r.get("Koordinaten-Genauigkeit"),
                "Source_Links": [l for l in (r.get("Links") or "").split("\n") if l],
            },
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
        })
    print(f"{len(features)} Projekte exportiert, {ohne_koord} ohne Koordinaten übersprungen")
    return {"type": "FeatureCollection", "features": features}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__ + "\n  Option --nur-aufstellung: nur Projekte mit Aufstellungsbeschluss")
    with open(args[1], "w", encoding="utf-8") as f:
        json.dump(baue(args[0], "--nur-aufstellung" in sys.argv), f, ensure_ascii=False, indent=1)

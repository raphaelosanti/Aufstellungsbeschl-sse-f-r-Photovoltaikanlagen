#!/usr/bin/env python3
"""
XPlanung-Sonde: Welche Geodienste liefern das Datum des Aufstellungsbeschlusses?  ->  entdeckung/xplan_bericht.md
===============================================================================================================

Der Standard XPlanung kennt am Bebauungsplan (xplan:BP_Plan) die Felder aufstellungsbeschlussDatum,
auslegungsStartDatum, satzungsbeschlussDatum und inkrafttretensDatum. Ein Dienst, der diese Felder füllt, wäre eine
strukturierte Quelle ohne Textauswertung. Die Sonde prüft je Dienst aus xplan_dienste.csv:

  * GetCapabilities erreichbar? Welche Feature-Typen?
  * Anzahl Objekte je Typ (resultType=hits)
  * Stichprobe (bis 50 Objekte): kommen die Felder name, aufstellungsbeschlussDatum, rechtsstand vor und sind sie gefüllt?
  * Treffer mit PV-Bezug in Name/Beschreibung in der Stichprobe
  * OGC-API-Features (z. B. NRW): Sammlungen und Stichprobe

Das Ergebnis entscheidet, ob sich ein Adapter lohnt. Die Sonde ruft je Dienst nur wenige Anfragen ab, beachtet robots.txt
und den Abstand pro Server.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys
from urllib.parse import urlencode

import pv_beschluesse as pv

FELDER = ["aufstellungsbeschlussDatum", "auslegungsStartDatum", "satzungsbeschlussDatum", "inkrafttretensDatum",
          "rechtsstand", "planArt", "name", "beschreibung"]


def _tags(xml: str, tag: str) -> list[str]:
    return re.findall(rf"<(?:[\w\-]+:)?{tag}(?:\s[^>]*)?>([^<]*)</(?:[\w\-]+:)?{tag}>", xml)


def sonde_wfs(http, name: str, url: str, max_typen: int = 4) -> list[str]:
    out: list[str] = []
    basis = url.split("?")[0]
    try:
        cap = http.get(basis + "?" + urlencode({"SERVICE": "WFS", "REQUEST": "GetCapabilities", "VERSION": "2.0.0"}),
                       cache=False)
    except Exception as e:  # noqa: BLE001
        return [f"- GetCapabilities nicht abrufbar: {e}"]
    typen = re.findall(r"<(?:\w+:)?FeatureType>\s*<(?:\w+:)?Name>([^<]+)</", cap)
    out.append(f"- GetCapabilities ok, {len(typen)} Feature-Typen: " + ", ".join(typen[:12]) + (" …" if len(typen) > 12 else ""))
    kandidaten = [t for t in typen if re.search(r"bp_plan|b_plan|bplan|bebauungsplan|bauleit|plan$", t, re.I)] or typen
    for t in kandidaten[:max_typen]:
        try:
            hits = http.get(basis + "?" + urlencode({"SERVICE": "WFS", "REQUEST": "GetFeature", "VERSION": "2.0.0",
                                                     "TYPENAMES": t, "RESULTTYPE": "hits"}), cache=False)
            m = re.search(r'numberMatched="(\d+)"', hits)
            anzahl = m.group(1) if m else "?"
            probe = http.get(basis + "?" + urlencode({"SERVICE": "WFS", "REQUEST": "GetFeature", "VERSION": "2.0.0",
                                                      "TYPENAMES": t, "COUNT": "50"}), cache=False)
        except Exception as e:  # noqa: BLE001
            out.append(f"- Typ {t}: Abruf fehlgeschlagen ({e})")
            continue
        n_obj = len(re.findall(r"<(?:\w+:)?(?:member|featureMember)\b", probe)) or len(re.findall(r"gml:id=", probe))
        zeile = [f"- Typ **{t}**: {anzahl} Objekte, Stichprobe {n_obj}"]
        for f in FELDER:
            werte = [w.strip() for w in _tags(probe, f) if w.strip()]
            if werte:
                zeile.append(f"{f} gefüllt {len(werte)}× (z. B. {werte[0][:40]})")
        pvn = sum(1 for w in _tags(probe, "name") + _tags(probe, "beschreibung") if pv.PV_RE.search(w))
        zeile.append(f"PV-Bezug in Name/Beschreibung: {pvn}")
        out.append("; ".join(zeile))
    return out


def sonde_ogc_api(http, name: str, url: str) -> list[str]:
    out: list[str] = []
    basis = url.split("?")[0].rstrip("/")
    if basis.endswith("/api"):
        basis = basis[:-4]
    try:
        landing = http.json(basis + "/api?f=json", cache=False) if "/api" in url else http.json(basis + "?f=json", cache=False)
        cols = http.json(basis + "/collections?f=json", cache=False)
    except Exception as e:  # noqa: BLE001
        return [f"- OGC API nicht abrufbar: {e}"]
    namen = [c.get("id") for c in cols.get("collections", [])]
    out.append(f"- OGC API ok ({landing.get('title', '')}), Sammlungen: " + ", ".join(map(str, namen[:12])))
    for c in namen[:3]:
        try:
            items = http.json(f"{basis}/collections/{c}/items?f=json&limit=50", cache=False)
        except Exception as e:  # noqa: BLE001
            out.append(f"- Sammlung {c}: Abruf fehlgeschlagen ({e})")
            continue
        feats = items.get("features", [])
        keys = sorted({k for f in feats for k in (f.get("properties") or {})})
        pvn = sum(1 for f in feats if pv.PV_RE.search(" ".join(str(v) for v in (f.get("properties") or {}).values())))
        out.append(f"- Sammlung **{c}**: {items.get('numberMatched', '?')} Objekte, Stichprobe {len(feats)}, "
                   f"Felder: {', '.join(keys[:25])}; PV-Bezug in Stichprobe: {pvn}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dienste", default="xplan_dienste.csv")
    ap.add_argument("--out", default="entdeckung")
    ap.add_argument("--pause", type=float, default=1.0)
    a = ap.parse_args()
    http = pv.Http(pause=a.pause)
    md = [f"# XPlanung-Sonde ({dt.date.today().isoformat()})", "",
          "Prüft, ob die Dienste das Datum des Aufstellungsbeschlusses und PV-Bezug liefern. Gefüllte Felder und Treffer "
          "stammen aus einer Stichprobe von höchstens 50 Objekten je Typ.", ""]
    with open(a.dienste, encoding="utf-8", newline="") as f:
        dienste = [r for r in csv.DictReader(f) if r.get("url")]
    for d in dienste:
        md += [f"## {d['name']} ({d['bundesland']})", f"- URL: {d['url']}", f"- Art: {d['art']}; {d.get('hinweis', '')}"]
        try:
            md += sonde_ogc_api(http, d["name"], d["url"]) if d["art"] == "ogcapi" else sonde_wfs(http, d["name"], d["url"])
        except Exception as e:  # noqa: BLE001
            md.append(f"- Sonde abgebrochen: {e}")
        md.append("")
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "xplan_bericht.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())

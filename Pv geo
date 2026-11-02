#!/usr/bin/env python3
"""
Koordinaten und Gemeindenamen für das PV-Beschlussregister
==========================================================

Warum ein neues Modul?
  * Nominatim allein ist für Läufe auf GitHub Actions unzuverlässig (Rate-Limit/Sperren,
    der alte Code hat Fehler still verschluckt) und bekam oft Müll als "Gemeinde".
  * Jetzt gilt: erst lokale Tabellen (kein Netz-Limit), Nominatim nur als Notnagel,
    und jeder Fehlschlag wird mit Grund im Log ausgegeben.

Reihenfolge je Projekt:
  1. Gemeinde sauber bestimmen: bekannte Gemeindenamen (daten/gemeinden.csv, kommt aus
     Wikidata via quellen_entdecken.py) im Vorlagentext suchen, nur im passenden Landkreis.
  2. Ortsteil/Gemarkung -> GeoNames-Ortsliste (DE.zip, wird einmal geladen), nächster
     Treffer zur Gemeinde (max. 30 km) => Genauigkeit "Ortsteil/Gemarkung".
  3. sonst Mittelpunkt der Gemeinde aus gemeinden.csv => "Gemeinde".
  4. sonst (nur mit nominatim=True) Nominatim, Fehler werden NICHT gecacht.
"""
from __future__ import annotations

import csv
import io
import json
import math
import os
import re
import time
import zipfile
from collections import Counter, defaultdict

import requests

GEMEINDEN_CSV = os.path.join("daten", "gemeinden.csv")
GEONAMES_URL = "https://download.geonames.org/export/dump/DE.zip"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
MAX_KM_ORTSTEIL = 30.0

_BUCHST = "a-zäöüß0-9"
_ALIAS_SPLIT = re.compile(r"\s+(?:bei|an der|am|im|in der)\s+|/|\s*\(")
_PRAEFIX_VOR_NAME = re.compile(
    r"(gemeinde|stadt|amt|gemeindevertretung|stadtverordnetenversammlung)\s*$", re.I)


def norm(s: str) -> str:
    """Vergleichsform: klein, ohne Stadt/Gemeinde-Präfix, ohne Leer-/Sonderzeichen."""
    s = (s or "").lower().replace("ß", "ss")
    s = re.sub(r"^(?:stadt|gemeinde|ortsgemeinde|amt|ortsteil)\s+", "", s.strip())
    return re.sub(r"[^a-zäöü0-9]+", "", s)


def aliase(name: str) -> list[str]:
    """'Neuenhagen bei Berlin' -> ['Neuenhagen bei Berlin', 'Neuenhagen'] usw."""
    out = [name.strip()]
    kurz = _ALIAS_SPLIT.split(name.strip())[0].strip()
    if kurz and kurz not in out and len(kurz) >= 4:
        out.append(kurz)
    return out


def _muster(name: str) -> re.Pattern:
    teile = [re.escape(t) for t in re.split(r"[\s\-]+", name.strip()) if t]
    koerper = r"[\s\-]*".join(teile)
    return re.compile(rf"(?<![\wäöüÄÖÜß-]){koerper}(?![\wäöüÄÖÜß]|-\w)", re.I)


def km(lat1, lon1, lat2, lon2) -> float:
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 12742 * math.asin(math.sqrt(a))


class Gemeindetabelle:
    def __init__(self, pfad: str = GEMEINDEN_CSV):
        self.recs: list[dict] = []
        self.nach_land: dict[str, list[dict]] = defaultdict(list)
        self.nach_norm: dict[tuple[str, str], list[dict]] = defaultdict(list)
        try:
            with open(pfad, encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    try:
                        row["lat"] = float(row["lat"]) if row.get("lat") else None
                        row["lon"] = float(row["lon"]) if row.get("lon") else None
                    except ValueError:
                        row["lat"] = row["lon"] = None
                    row["_pat"] = None
                    self.recs.append(row)
                    land = row.get("land", "")
                    self.nach_land[land].append(row)
                    for al in aliase(row["name"]):
                        self.nach_norm[(land, norm(al))].append(row)
        except OSError:
            pass

    def __bool__(self) -> bool:
        return bool(self.recs)

    def _kandidaten(self, land: str, landkreis: str) -> list[dict]:
        pool = self.nach_land.get(land, []) if land else self.recs
        if landkreis:
            lk = norm(landkreis)
            eng = [r for r in pool if norm(r.get("landkreis", "")) == lk]
            return eng
        return pool

    def im_text(self, text: str, landkreis: str = "", land: str = "") -> dict | None:
        """Bester Gemeinde-Treffer im Text (nur innerhalb des Landkreises, wenn bekannt)."""
        best, best_score, best_pos = None, 0, 10 ** 9
        for r in self._kandidaten(land, landkreis):
            if r["_pat"] is None:
                r["_pat"] = [_muster(a) for a in aliase(r["name"])]
            treffer = [m for p in r["_pat"] for m in p.finditer(text)]
            if not treffer:
                continue
            score = len(treffer)
            if any(_PRAEFIX_VOR_NAME.search(text[max(0, m.start() - 40):m.start()]) for m in treffer):
                score += 5
            pos = min(m.start() for m in treffer)
            if score > best_score or (score == best_score and pos < best_pos):
                best, best_score, best_pos = r, score, pos
        return best

    def exakt(self, name: str, land: str = "", landkreis: str = "") -> dict | None:
        """Eindeutiger Treffer per Namen (im Land, bevorzugt im Landkreis), sonst None."""
        n = norm(name)
        if land:
            c = list(self.nach_norm.get((land, n), []))
        else:
            c = [r for (_, nn), v in self.nach_norm.items() if nn == n for r in v]
        c = list({id(r): r for r in c}.values())
        if landkreis:
            eng = [r for r in c if norm(r.get("landkreis", "")) == norm(landkreis)]
            c = eng or c
        return c[0] if len(c) == 1 else None

    def bbox(self, land: str):
        pts = [(r["lat"], r["lon"]) for r in self.nach_land.get(land, []) if r["lat"] is not None]
        if not pts:
            return (47.2, 55.1, 5.8, 15.1)
        la, lo = [p[0] for p in pts], [p[1] for p in pts]
        return (min(la) - .3, max(la) + .3, min(lo) - .3, max(lo) + .3)


class Geocoder:
    def __init__(self, daten: str = "daten", cache_dir: str = ".cache_pv", user_agent: str = "pv-register",
                 nominatim: bool = False, pause: float = 1.1):
        self.daten, self.cache_dir, self.ua = daten, cache_dir, user_agent
        self.nominatim, self.pause, self.letzte = nominatim, pause, 0.0
        self.gemeinden = Gemeindetabelle(os.path.join(daten, "gemeinden.csv"))
        self._gn: dict[str, list[tuple[float, float]]] | None = None
        self.stat: Counter = Counter()
        self.fehl: list[str] = []
        self.pfad = os.path.join(daten, "geocache.json")
        try:
            with open(self.pfad, encoding="utf-8") as f:
                self.cache = json.load(f)
        except (OSError, ValueError):
            self.cache = {}
        if not self.gemeinden:
            print("   ! daten/gemeinden.csv fehlt/leer -> erst quellen_entdecken.py laufen lassen "
                  "(liefert Gemeinde-Koordinaten). Ohne Tabelle nur Nominatim.")

    # ---- Gemeindename säubern (vor Projekt-Zuordnung aufrufen) ------------------------
    def kanonisch(self, text: str, landkreis: str, land: str, vorschlag: str) -> str:
        r = self.gemeinden.im_text(text, landkreis, land)
        if r:
            return r["name"]
        r = self.gemeinden.exakt(vorschlag, land, landkreis)
        return r["name"] if r else vorschlag

    # ---- GeoNames ---------------------------------------------------------------------
    def _geonames(self) -> dict:
        if self._gn is not None:
            return self._gn
        self._gn = defaultdict(list)
        zpath = os.path.join(self.cache_dir, "geonames_DE.zip")
        os.makedirs(self.cache_dir, exist_ok=True)
        try:
            if not os.path.exists(zpath):
                r = requests.get(GEONAMES_URL, timeout=180, headers={"User-Agent": self.ua})
                r.raise_for_status()
                with open(zpath, "wb") as f:
                    f.write(r.content)
            with zipfile.ZipFile(zpath) as z, z.open("DE.txt") as f:
                for zeile in io.TextIOWrapper(f, encoding="utf-8"):
                    p = zeile.rstrip("\n").split("\t")
                    if len(p) < 8 or p[6] != "P":
                        continue
                    pos = (float(p[4]), float(p[5]))
                    namen = {p[1], p[2], *[x for x in p[3].split(",") if x]}
                    for n in {norm(x) for x in namen if x}:
                        if len(n) >= 3:
                            self._gn[n].append(pos)
            print(f"   GeoNames geladen: {len(self._gn)} Ortsnamen")
        except Exception as e:  # noqa: BLE001
            print(f"   ! GeoNames nicht verfügbar ({e.__class__.__name__}: {e}) – Ortsteile nur per Fallback")
        return self._gn

    def _ortsteil(self, ortsteil: str, ref: dict | None):
        kand = self._geonames().get(norm(ortsteil), [])
        if not kand:
            return None
        if ref and ref["lat"] is not None:
            d, pos = min((km(ref["lat"], ref["lon"], *p), p) for p in kand)
            return pos if d <= MAX_KM_ORTSTEIL else None
        return kand[0] if len(kand) == 1 else None      # ohne Referenz nur eindeutige Namen

    # ---- Nominatim-Notnagel ----------------------------------------------------------
    def _nominatim(self, query: str, bbox):
        if query in self.cache:
            c = self.cache[query]
            return tuple(c) if c else None
        wait = self.pause - (time.time() - self.letzte)
        if wait > 0:
            time.sleep(wait)
        try:
            r = requests.get(NOMINATIM_URL, timeout=20, headers={"User-Agent": self.ua},
                             params={"q": query, "format": "jsonv2", "limit": 1, "countrycodes": "de"})
            self.letzte = time.time()
            if r.status_code != 200:
                self.stat[f"nominatim_http_{r.status_code}"] += 1
                return None                      # Fehler NICHT cachen
            treffer = r.json()
        except (requests.RequestException, ValueError) as e:
            self.stat[f"nominatim_{e.__class__.__name__}"] += 1
            return None
        pos = None
        if treffer:
            lat, lon = float(treffer[0]["lat"]), float(treffer[0]["lon"])
            if bbox[0] <= lat <= bbox[1] and bbox[2] <= lon <= bbox[3]:
                pos = (lat, lon)
        self.cache[query] = list(pos) if pos else None     # echtes "nichts gefunden" darf gecacht werden
        return pos

    # ---- Hauptfunktion ---------------------------------------------------------------
    def finde(self, ortsteil: str, gemeinde: str, landkreis: str, bundesland: str, projekt: str = ""):
        """-> (lat, lon, genauigkeit); (None, None, "") wenn nichts gefunden."""
        ref = self.gemeinden.exakt(gemeinde, bundesland, landkreis) if self.gemeinden else None
        if ortsteil:
            pos = self._ortsteil(ortsteil, ref)
            if pos:
                self.stat["ortsteil_geonames"] += 1
                return pos[0], pos[1], "Ortsteil/Gemarkung"
        if ref and ref["lat"] is not None:
            self.stat["gemeinde_tabelle"] += 1
            return ref["lat"], ref["lon"], "Gemeinde"
        grund = "Gemeinde nicht in Tabelle" if self.gemeinden else "keine Gemeindetabelle"
        if self.nominatim and gemeinde:
            bbox = self.gemeinden.bbox(bundesland)
            for q in ([f"{ortsteil}, {gemeinde}, {bundesland}, Deutschland"] if ortsteil else []) + \
                     [f"{gemeinde}, {landkreis}, {bundesland}, Deutschland" if landkreis
                      else f"{gemeinde}, {bundesland}, Deutschland"]:
                pos = self._nominatim(q, bbox)
                if pos:
                    self.stat["nominatim_ok"] += 1
                    return pos[0], pos[1], "Ortsteil/Gemarkung" if q.startswith(ortsteil + ",") and ortsteil else "Gemeinde"
            grund += "; Nominatim ohne Treffer/Fehler"
        self.stat["nicht_gefunden"] += 1
        self.fehl.append(f"{projekt or '?'} | Gemeinde='{gemeinde[:40]}' Ortsteil='{ortsteil}' Landkreis='{landkreis}' -> {grund}")
        return None, None, ""

    def speichern(self) -> None:
        os.makedirs(os.path.dirname(self.pfad) or ".", exist_ok=True)
        with open(self.pfad, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False)

    def bericht(self) -> None:
        print("   Geocoding:", ", ".join(f"{k}: {v}" for k, v in sorted(self.stat.items())) or "nichts zu tun")
        for z in self.fehl[:25]:
            print("   ! ohne Koordinate:", z)
        if len(self.fehl) > 25:
            print(f"   ! … und {len(self.fehl) - 25} weitere")

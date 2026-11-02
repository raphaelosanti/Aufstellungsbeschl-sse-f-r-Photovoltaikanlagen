#!/usr/bin/env python3
"""
Persistenter Zustand für das PV-Beschlussregister
=================================================

Problem vorher: Jeder Lauf begann bei null (Ergebnis nur als Artifact, Actions-Cache kann nach
7 Tagen ohne Zugriff verfallen, Gemini wurde jedes Mal neu bezahlt, SessionNet wurde jedes Mal
komplett rückwärts durchsucht).

Jetzt: Der Bestand liegt im Repo (daten/beschluesse_<Bundesland>.jsonl, eine Zeile je Beschluss)
plus Marken je Quelle (daten/marken_<Bundesland>.json, z. B. höchste gesehene Sitzungsnummer).
Der Workflow committet beides nach jedem Lauf. Ein Lauf verarbeitet nur, was neu ist.
"""
from __future__ import annotations

import glob
import json
import os
import re


def _slug(land: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", land.lower().replace("ä", "ae").replace("ö", "oe")
                  .replace("ü", "ue").replace("ß", "ss")).strip("_")


class Zustand:
    def __init__(self, verzeichnis: str, land: str):
        os.makedirs(verzeichnis, exist_ok=True)
        s = _slug(land)
        self.pfad = os.path.join(verzeichnis, f"beschluesse_{s}.jsonl")
        self.marken_pfad = os.path.join(verzeichnis, f"marken_{s}.json")
        self.eintraege: dict[str, dict] = {}
        self.marken: dict[str, dict] = {}
        self.neu = 0
        self.verworfen: set[str] = set()
        if os.path.exists(self.pfad):
            with open(self.pfad, encoding="utf-8") as f:
                for zeile in f:
                    if zeile.strip():
                        d = json.loads(zeile)
                        self.eintraege[self.key(d)] = d
        if os.path.exists(self.marken_pfad):
            with open(self.marken_pfad, encoding="utf-8") as f:
                self.marken = json.load(f)
        self.verworfen = set(self.marken.pop("_verworfen", []))

    @staticmethod
    def key(d: dict) -> str:
        return d.get("schluessel") or d.get("link") or f"{d.get('datum')}|{d.get('gemeinde')}|{d.get('titel')}"

    # ---- Beschlüsse -------------------------------------------------------------
    def hat(self, schluessel: str) -> bool:
        """Schon verarbeitet (als Treffer ODER als 'kein PV-Bauleitplan' verworfen)?"""
        return bool(schluessel) and (schluessel in self.eintraege or schluessel in self.verworfen)

    def verwirf(self, schluessel: str) -> None:
        if schluessel:
            self.verworfen.add(schluessel)

    def add(self, d: dict) -> None:
        k = self.key(d)
        if k not in self.eintraege:
            self.neu += 1
        self.eintraege[k] = d

    def alle(self) -> list[dict]:
        return list(self.eintraege.values())

    def ersetze(self, dicts: list[dict]) -> None:
        """Nach Projekt-Zuordnung/Geocoding den angereicherten Bestand zurückschreiben."""
        self.eintraege = {self.key(d): d for d in dicts}

    # ---- Marken je Quelle -------------------------------------------------------
    def marke(self, quelle: str, name: str, default=None):
        return self.marken.get(quelle, {}).get(name, default)

    def setze(self, quelle: str, name: str, wert) -> None:
        self.marken.setdefault(quelle, {})[name] = wert

    # ---- Speichern --------------------------------------------------------------
    def speichern(self) -> None:
        tmp = self.pfad + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for d in sorted(self.eintraege.values(), key=lambda x: (x.get("projekt_id", ""), x.get("datum", ""))):
                f.write(json.dumps(d, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(tmp, self.pfad)
        with open(self.marken_pfad, "w", encoding="utf-8") as f:
            json.dump({**self.marken, "_verworfen": sorted(self.verworfen)}, f, ensure_ascii=False, indent=1,
                      sort_keys=True)

    @staticmethod
    def alle_laender(verzeichnis: str) -> list[dict]:
        out = []
        for p in sorted(glob.glob(os.path.join(verzeichnis, "beschluesse_*.jsonl"))):
            with open(p, encoding="utf-8") as f:
                out += [json.loads(z) for z in f if z.strip()]
        return out

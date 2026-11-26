#!/usr/bin/env python3
"""
Quellen-Entdeckung für das PV-Beschlussregister (v2, inkrementell)
==================================================================

Was sich gegenüber v1 ändert:
 * Ergebnis wird direkt in die Master-Liste quellen_alle.csv eingemischt (kein Hand-Kopieren mehr);
   bestehende/manuelle Zeilen bleiben erhalten (auch auskommentierte "# ..."-Zeilen).
 * daten/gemeinden.csv = Gemeinde-Tabelle mit Koordinaten (Wikidata P625) UND Prüfstatus je Gemeinde.
   Daraus bezieht pv_geo.py die Koordinaten (kein Nominatim-Zwang mehr).
 * Inkrementell: schon geprüfte Gemeinden werden übersprungen (--recheck-tage), --budget begrenzt
   die Zahl neu geprüfter Gemeinden pro Lauf. Mehrere Läufe arbeiten das Land nach und nach ab.
 * OParl-Endpunktliste des OParl-Projekts wird zugeordnet (Wikidata-ID), ohne Homepage-Crawl.
 * Mehrere Bundesländer: --land alle (Reihenfolge: Brandenburg zuerst).

Aufruf:
    python quellen_entdecken.py --land Brandenburg --budget 50      # Test
    python quellen_entdecken.py --land alle --budget 300            # alle Länder, schrittweise
    python quellen_entdecken.py --nur-gemeinden                     # nur Tabelle/Koordinaten aktualisieren
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

import pv_beschluesse as pv

WIKIDATA = "https://query.wikidata.org/sparql"
OPARL_ENDPOINTS = "https://raw.githubusercontent.com/OParl/resources/main/endpoints.yml"
# Präfix des amtlichen Gemeindeschlüssels (AGS) je Bundesland; Reihenfolge = Priorität bei "alle"
BUNDESLAENDER = {
    "Brandenburg": "12", "Sachsen-Anhalt": "15", "Mecklenburg-Vorpommern": "13", "Sachsen": "14",
    "Thüringen": "16", "Niedersachsen": "03", "Schleswig-Holstein": "01", "Nordrhein-Westfalen": "05",
    "Hessen": "06", "Rheinland-Pfalz": "07", "Baden-Württemberg": "08", "Bayern": "09",
    "Saarland": "10", "Berlin": "11", "Hamburg": "02", "Bremen": "04",
}
GEM_FELDER = ["qid", "ags", "name", "landkreis", "land", "amt", "web", "lat", "lon",
              "ris_url", "ris_typ", "ris_status", "geprueft_am"]
QUELLEN_FELDER = ["name", "landkreis", "typ", "url", "bundesland", "hinweis"]

RIS_HREF = re.compile(
    r"ratsinfo|buergerinfo|buerger-?info|sitzungsdienst|sessionnet|allris|si0040|si0046|gr0040|"
    r"oparl|mandatos|kommunalportal|sdnet|ratsinformation|/bi/|sitzungskalender|gremieninfo", re.I)
RIS_TEXT = re.compile(
    r"ratsinfo|bürgerinfo|buergerinfo|sitzungsdienst|sitzungskalender|gremieninfo|ratsinformation|"
    r"bürgerinformation|allris|sitzungen|gremien|sitzungstermine", re.I)
SUBDOMAINS = ["ratsinfo", "buergerinfo", "sessionnet", "sitzung", "bi", "ris", "sitzungsdienst",
              "ratsinformation", "session", "allris", "gremien", "sitzungen", "rats-info", "bis"]
PFADE = ["bi/", "buergerinfo/", "sessionnet/", "ratsinfo/", "allris/", "session/", "ratsinformationssystem/",
         "sitzungsdienst/", "gremien/"]
# Gehostete RIS-Anbieter: Links auf diese Hosts sind (fast) immer ein RIS der Gemeinde
ANBIETER_HOST = re.compile(
    r"(ratsinfo-online\.net|sitzung-online\.de|ratsinfomanagement\.net|more-rubin\d*\.de|"
    r"session\.[a-z0-9-]+\.de|sdnet\.|kommunalweb\.de|buergerinfoportal|ris-portal|ratsinfo\.|"
    r"sitzungsdienst\.|buergerinfo\.|allris\.|\bsessionnet\.|\bbi\.[a-z0-9-]+\.(de|net)|"
    r"gremieninfo|ratsinformation\.)", re.I)
# Anbieter, die wir (noch) nicht auslesen können – nur zur Statistik in 'hinweis'
ANBIETER_UNBEKANNT = re.compile(r"(kdz|komm\.one|gemeinde-?portal|vgem|amt-?portal|ratsinfo\.at)", re.I)


# --------------------------------------------------------------------------- #
# Gemeinden aus Wikidata (inkl. Koordinaten)
# --------------------------------------------------------------------------- #
def gemeinden(land: str, ags: str) -> list[dict]:
    query = f"""
    SELECT ?item ?name ?web ?parentName ?coord ?ags WHERE {{
      ?item wdt:P439 ?ags .
      FILTER(STRSTARTS(?ags, "{ags}") && STRLEN(?ags) = 8)
      ?item rdfs:label ?name . FILTER(LANG(?name) = "de")
      OPTIONAL {{ ?item wdt:P856 ?web }}
      OPTIONAL {{ ?item wdt:P625 ?coord }}
      OPTIONAL {{ ?item wdt:P131 ?parent . ?parent rdfs:label ?parentName . FILTER(LANG(?parentName) = "de") }}
    }}"""
    letzter_fehler = None
    for versuch in range(4):
        try:
            r = requests.post(WIKIDATA, data={"query": query, "format": "json"},
                              headers={"User-Agent": pv.USER_AGENT, "Accept": "application/sparql-results+json"},
                              timeout=180)
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
        g = out.setdefault(item, {"qid": item.rsplit("/", 1)[-1], "ags": row["ags"]["value"],
                                  "name": row["name"]["value"], "web": "", "eltern": set(),
                                  "land": land, "lat": "", "lon": ""})
        if "web" in row and not g["web"]:
            g["web"] = row["web"]["value"]
        if "coord" in row and not g["lat"]:
            m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", row["coord"]["value"])
            if m:
                g["lon"], g["lat"] = m.group(1), m.group(2)
        if "parentName" in row:
            g["eltern"].add(row["parentName"]["value"])
    res = []
    for g in out.values():
        eltern = g.pop("eltern")
        g["amt"] = next((e for e in sorted(eltern) if e.startswith("Amt ")), "")
        g["landkreis"] = next((re.sub(r"^Landkreis\s+", "", e) for e in sorted(eltern)
                               if not e.startswith("Amt ") and e != land), "")
        res.append(g)
    return sorted(res, key=lambda g: g["name"])


def lade_csv(pfad: str) -> list[dict]:
    try:
        with open(pfad, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def schreibe_csv(pfad: str, felder: list[str], zeilen: list[dict]) -> None:
    os.makedirs(os.path.dirname(pfad) or ".", exist_ok=True)
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder, extrasaction="ignore")
        w.writeheader()
        w.writerows(zeilen)
    os.replace(tmp, pfad)


# --------------------------------------------------------------------------- #
# RIS finden und prüfen (unverändert gegenüber v1)
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
        if ANBIETER_HOST.search(urlparse(href).netloc):
            s += 3
        if s:
            res.append((s, href))
    return res


def kandidaten(http: pv.Http, home: str) -> list[str]:
    stufe1 = sorted(set(links_der_seite(http, home)), reverse=True)
    cands = [u for _, u in stufe1]
    host = urlparse(home).netloc
    # zweite Ebene: Unterseiten wie "Rathaus", "Politik", "Bürgerservice" (Sitzungsdienst steckt oft dort)
    for s, u in stufe1[:8]:
        if urlparse(u).netloc == host and s <= 2:
            cands += [x for sc, x in links_der_seite(http, u) if sc >= 2]
    for _, u in links_der_seite_menue(http, home)[:6]:
        cands += [x for sc, x in links_der_seite(http, u) if sc >= 2]
    return list(dict.fromkeys(cands))[:14]


MENUE_TEXT = re.compile(r"rathaus|politik|gemeindevertretung|stadtverordneten|gemeinderat|"
                        r"bürgerservice|buergerservice|verwaltung|politik\s*&|stadtrat|kreistag", re.I)


def links_der_seite_menue(http: pv.Http, url: str) -> list[tuple[int, str]]:
    """Links der Startseite auf Menüpunkte wie Rathaus/Politik (gleicher Host)."""
    try:
        soup = BeautifulSoup(http.get(url), "html.parser")
    except Exception:  # noqa: BLE001
        return []
    host = urlparse(url).netloc
    res = []
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"]).split("#")[0]
        if urlparse(href).netloc == host and MENUE_TEXT.search(a.get_text(" ", strip=True)) \
                and not re.search(r"\.(pdf|docx?|jpe?g|png)$", href, re.I):
            res.append((1, href))
    return list(dict.fromkeys(res))


def pruefe(http: pv.Http, url: str):
    base = norm_basis(url)
    if "ratsinfo-online.net" in base:
        return "auto", base
    if re.search(r"sitzung-online\.de|ratsinfomanagement\.net|more-rubin", base, re.I):
        return "auto", base
    try:
        o = pv.oparl_entdecken(http, base)
        if o:
            return "oparl", o
        if pv.ist_sessionnet(http, base):
            return "sessionnet", base
        for p in pv.UEBERSICHT_PFADE:
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
# OParl-Endpunktliste (liefert vor allem größere Städte; Brandenburg ist dort kaum vertreten)
# --------------------------------------------------------------------------- #
def oparl_endpunkte(http: pv.Http) -> dict[str, tuple[str, str]]:
    """Wikidata-ID -> (Titel, System-URL)."""
    try:
        import yaml
        daten = yaml.safe_load(http.get(OPARL_ENDPOINTS, cache=False))
    except Exception as e:  # noqa: BLE001
        print(f"   ! OParl-Endpunktliste nicht geladen: {e}")
        return {}
    if isinstance(daten, dict):
        daten = next((v for v in daten.values() if isinstance(v, list)), [])
    return {str(x["wd"]): (x.get("title", ""), x["url"])
            for x in daten if isinstance(x, dict) and x.get("wd") and x.get("url")}


# --------------------------------------------------------------------------- #
def amt_zuordnen(tab: dict, laender: list[str], eintragen) -> None:
    """Gemeinden eines Amts/einer Verbandsgemeinde teilen sich das RIS des Amts. Hat eine Gemeinde
    eines Amts ein RIS gefunden, bekommen die übrigen Gemeinden mit demselben Amt dasselbe."""
    je_amt: dict[tuple[str, str], dict] = {}
    for g in tab.values():
        if g["land"] in laender and g["amt"] and g["ris_status"] == "gefunden" and g["ris_url"]:
            je_amt.setdefault((g["land"], g["amt"]), g)
    n = 0
    for g in tab.values():
        if g["land"] not in laender or not g["amt"] or g["ris_status"] in ("gefunden", "gesperrt"):
            continue
        quelle = je_amt.get((g["land"], g["amt"]))
        if quelle:
            eintragen(g, quelle["ris_typ"], quelle["ris_url"])
            n += 1
    if n:
        print(f"Amtsebene: {n} Gemeinden dem RIS ihres Amts zugeordnet")


def homepage_liste(tab: dict, laender: list[str], pfad: str) -> None:
    """Gemeinden ohne RIS, aber mit Homepage -> Quellenliste für den Bekanntmachungs-Crawler (typ 'homepage')."""
    alt = {r["url"]: r for r in lade_csv(pfad)}
    neu = 0
    for g in tab.values():
        if g["land"] not in laender or g["ris_status"] != "kein_ris" or not g["web"]:
            continue
        if g["web"] not in alt:
            alt[g["web"]] = {"name": g["name"], "landkreis": g["landkreis"], "typ": "homepage",
                             "url": g["web"], "bundesland": g["land"], "hinweis": "kein RIS; Bekanntmachungen"}
            neu += 1
    zeilen = sorted(alt.values(), key=lambda r: (r["bundesland"], r["name"]))
    schreibe_csv(pfad, QUELLEN_FELDER, zeilen)
    print(f"Homepage-Quellen: {neu} neu, {len(zeilen)} gesamt → {pfad}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--land", nargs="+", default=["Brandenburg"], choices=sorted(BUNDESLAENDER) + ["alle"])
    ap.add_argument("--quellen", default="quellen_alle.csv", help="Master-Liste (wird fortgeschrieben)")
    ap.add_argument("--seed", default="quellen_brandenburg.csv", help="wird einmalig übernommen, falls Master fehlt")
    ap.add_argument("--gemeinden", default=os.path.join("daten", "gemeinden.csv"))
    ap.add_argument("--budget", type=int, default=0, help="max. neu geprüfte Gemeinden pro Lauf (0 = alle)")
    ap.add_argument("--recheck-tage", type=int, default=90, help="ohne RIS gefundene Gemeinden erst nach X Tagen erneut")
    ap.add_argument("--raten", action="store_true", help="auch typische Subdomains/Pfade probieren")
    ap.add_argument("--kein-ris-erneut", action="store_true",
                    help="Gemeinden mit Status kein_ris unabhängig vom Alter erneut prüfen (nach Erkennungs-Verbesserung)")
    ap.add_argument("--homepage-quellen", default="quellen_homepage.csv",
                    help="Liste der Gemeinden ohne RIS, deren Homepage nach Bekanntmachungen durchsucht wird")
    ap.add_argument("--nur-gemeinden", action="store_true", help="nur Gemeindetabelle (Koordinaten) aktualisieren")
    ap.add_argument("--pause", type=float, default=0.7)
    ap.add_argument("--parallel", type=int, default=8, help="Gemeinden gleichzeitig prüfen (je Server weiter nacheinander)")
    ap.add_argument("--frist", type=float, default=120.0, help="harte Frist je Gemeinde in Sekunden")
    ap.add_argument("--max-minuten", type=float, default=0, help="danach sauber beenden und speichern (0 = unbegrenzt)")
    a = ap.parse_args()

    http = pv.Http(pause=a.pause)
    heute = dt.date.today()
    laender = list(BUNDESLAENDER) if "alle" in a.land else a.land

    # --- Master-Quellenliste laden (oder aus Seed starten)
    quellen = lade_csv(a.quellen) or lade_csv(a.seed)
    quellen = [{k: (r.get(k) or "") for k in QUELLEN_FELDER} for r in quellen]
    bekannt = {norm_basis(q["url"]): q for q in quellen if q["url"]}

    # --- Gemeindetabelle aktualisieren (Wikidata, 1 Abfrage je Land)
    tab = {r["ags"]: r for r in lade_csv(a.gemeinden)}
    for land in laender:
        print(f"Lade Gemeinden {land} aus Wikidata …")
        for g in gemeinden(land, BUNDESLAENDER[land]):
            alt = tab.get(g["ags"], {})
            tab[g["ags"]] = {**{k: alt.get(k, "") for k in GEM_FELDER}, **{k: g[k] for k in
                             ("qid", "ags", "name", "landkreis", "land", "amt", "web", "lat", "lon")}}
        schreibe_csv(a.gemeinden, GEM_FELDER, sorted(tab.values(), key=lambda r: (r["land"], r["name"])))
    print(f"   {sum(1 for r in tab.values() if r['land'] in laender)} Gemeinden in der Tabelle")
    if a.nur_gemeinden:
        return 0

    def sichern() -> None:
        schreibe_csv(a.quellen, QUELLEN_FELDER, quellen)
        schreibe_csv(a.gemeinden, GEM_FELDER, sorted(tab.values(), key=lambda r: (r["land"], r["name"])))

    def eintragen(g: dict, typ: str, url: str, erlaubt: bool = True) -> None:
        basis = norm_basis(url)
        g.update(ris_url=url, ris_typ=typ, ris_status="gefunden" if erlaubt else "gesperrt",
                 geprueft_am=heute.isoformat())
        if basis in bekannt:
            hin = bekannt[basis]
            if g["name"] not in hin["hinweis"]:
                hin["hinweis"] = (hin["hinweis"] + "; " if hin["hinweis"] else "") + g["name"]
            return
        name = g["amt"] or g["name"]
        zeile = {"name": name if erlaubt else f"# {name}", "landkreis": g["landkreis"], "typ": typ, "url": url,
                 "bundesland": g["land"], "hinweis": ("" if erlaubt else "robots.txt verbietet Bots; ") + g["name"]}
        quellen.append(zeile)
        bekannt[basis] = zeile

    # --- OParl-Endpunktliste per Wikidata-ID zuordnen (kein Crawl nötig)
    for qid, (titel, url) in oparl_endpunkte(http).items():
        g = next((r for r in tab.values() if r["qid"] == qid and r["land"] in laender), None)
        if g and g["ris_status"] != "gefunden":
            eintragen(g, "oparl", url)
            print(f"   OParl-Liste: {g['name']} → {url}")

    # --- Gemeinden prüfen
    offen = []
    for land in laender:
        for g in tab.values():
            if g["land"] != land or g["ris_status"] == "gefunden" or g["ris_status"] == "gesperrt":
                continue
            if g["geprueft_am"] and not (a.kein_ris_erneut and g["ris_status"] == "kein_ris"):
                alter = (heute - dt.date.fromisoformat(g["geprueft_am"])).days
                if alter < a.recheck_tage:
                    continue
            offen.append(g)
    if a.budget:
        offen = offen[:a.budget]
    print(f"\n{len(offen)} Gemeinden werden in diesem Lauf geprüft\n")

    def pruefe_gemeinde(g: dict):
        """Läuft im Arbeits-Thread: nur lesen, nichts an gemeinsamen Listen ändern. Harte Frist je Gemeinde."""
        if not g["web"]:
            return ("keine_homepage", None, None, True)
        http.frist_setzen(a.frist)
        try:
            try:
                http.get(g["web"])
            except requests.RequestException:       # Startseite nicht erreichbar: Raten wäre Zeitverschwendung
                return ("kein_ris", None, None, True)
            cands = kandidaten(http, g["web"])
            gefunden = next((x for x in (pruefe(http, u) for u in cands) if x), None)
            if not gefunden:   # Rückfall: typische Subdomains/Pfade raten
                gefunden = next((x for x in (pruefe(http, u) for u in raten(urlparse(g["web"]).netloc)) if x), None)
            if not gefunden:
                return ("kein_ris", None, None, True)
            typ, url = gefunden
            try:
                erlaubt = http._erlaubt(url)
            except Exception:  # noqa: BLE001
                erlaubt = True
            return ("gefunden", typ, url, erlaubt)
        except TimeoutError:
            return ("zeitlimit", None, None, True)
        finally:
            http.frist_setzen(None)

    ende = time.time() + a.max_minuten * 60 if a.max_minuten else None
    fertig = 0
    stueck = max(1, a.parallel) * 4
    with ThreadPoolExecutor(max_workers=max(1, a.parallel)) as pool:
        for von in range(0, len(offen), stueck):
            if ende and time.time() > ende:
                print(f"\nZeitbudget von {a.max_minuten} Minuten erreicht – Rest beim nächsten Lauf.")
                break
            teil = offen[von:von + stueck]
            futs = {pool.submit(pruefe_gemeinde, g): g for g in teil}
            for f in as_completed(futs):
                g = futs[f]
                fertig += 1
                try:
                    status, typ, url, erlaubt = f.result()
                except Exception as e:  # noqa: BLE001
                    print(f"[{fertig}/{len(offen)}] {g['land']} / {g['name']} ! Fehler: {e}")
                    continue
                if status == "keine_homepage":
                    g.update(ris_status="keine_homepage", geprueft_am=heute.isoformat())
                    msg = "– keine Homepage in Wikidata"
                elif status == "gefunden":
                    eintragen(g, typ, url, erlaubt)
                    msg = f"→ {typ} {url}{'' if erlaubt else '  (robots.txt gesperrt)'}"
                elif status == "zeitlimit":     # als geprüft markieren, sonst blockiert sie jeden Lauf; Wiederholung nach recheck-tage
                    g.update(ris_status="kein_ris", geprueft_am=heute.isoformat())
                    msg = f"– Zeitlimit ({a.frist:.0f}s), als kein RIS markiert"
                else:
                    g.update(ris_status="kein_ris", geprueft_am=heute.isoformat())
                    msg = "– kein RIS erkannt"
                print(f"[{fertig}/{len(offen)}] {g['land']} / {g['name']} {msg}", flush=True)
                if fertig % 25 == 0:
                    sichern()
    amt_zuordnen(tab, laender, eintragen)
    sichern()
    homepage_liste(tab, laender, a.homepage_quellen)

    zaehle = {}
    for g in tab.values():
        if g["land"] in laender:
            zaehle[g["ris_status"] or "ungeprüft"] = zaehle.get(g["ris_status"] or "ungeprüft", 0) + 1
    print("\nStatus der Gemeinden:", ", ".join(f"{k}: {v}" for k, v in sorted(zaehle.items())))
    print(f"Master-Liste: {len(quellen)} Zeilen → {a.quellen}")
    print(f"Gemeindetabelle → {a.gemeinden}  (Gemeinden ohne RIS: Status 'kein_ris' / 'keine_homepage')")
    return 0


if __name__ == "__main__":
    sys.exit(main())

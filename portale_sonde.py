#!/usr/bin/env python3
"""
Portal-Sonde: untersucht die Landesportale aus portale.csv und schreibt einen Bericht.

Pro Portal wird geprüft: robots.txt, Startseite (Inhalt oder reine JavaScript-App?), sitemap.xml,
Feeds, Hinweise auf API-/JSON-Endpunkte und Beispiel-Links. Rohdaten (Startseite, robots.txt)
liegen danach in entdeckung/portale_proben/<portal>/, der Bericht in entdeckung/portale_bericht.md.

Aufruf:
    python portale_sonde.py                       # alle Portale aus portale.csv
    python portale_sonde.py --portale portale.csv --out entdeckung

Die Sonde ruft pro Portal nur wenige Seiten ab (robots.txt, Startseite, sitemap.xml) und
beachtet robots.txt. Ist der Zugriff verboten, wird nur das vermerkt.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

import pv_beschluesse as pv
from pv_portale import LINK_HINT, URL_IN_TEXT, _feed_urls

SPA_HINWEISE = [
    (r'id="(?:app|root|__nuxt)"', "SPA-Container (app/root)"),
    (r"__NEXT_DATA__", "Next.js"),
    (r"ng-version|<app-root", "Angular"),
    (r"data-reactroot|react", "React"),
    (r"vue", "Vue"),
]
API_RE = re.compile(r"""(?:["'(=\s])(/(?:api|graphql|rest|ows|wfs|oparl)[\w\-/.?=&]*|[\w\-/.]+\.json)""", re.I)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:60]


def sonde(http: pv.Http, name: str, url: str, outdir: str) -> list[str]:
    p = urlparse(url)
    root = f"{p.scheme}://{p.netloc}"
    d = os.path.join(outdir, "portale_proben", slug(name))
    os.makedirs(d, exist_ok=True)
    z = [f"### {name}", f"- URL: {url}"]

    # robots.txt
    try:
        r = http.s.get(root + "/robots.txt", timeout=15)
        z.append(f"- robots.txt: HTTP {r.status_code}")
        if r.status_code == 200:
            open(os.path.join(d, "robots.txt"), "w", encoding="utf-8").write(r.text[:5000])
            z.append(f"- robots.txt Auszug: `{' | '.join(r.text.splitlines()[:6])[:300]}`")
    except Exception as e:  # noqa: BLE001
        z.append(f"- robots.txt: nicht erreichbar ({type(e).__name__}) -> Portal vermutlich vom Runner aus nicht abrufbar")
    erlaubt = http._erlaubt(url)
    z.append(f"- Abruf für unseren User-Agent erlaubt: {'ja' if erlaubt else '**NEIN (robots.txt verbietet)**'}")
    if not erlaubt:
        z.append("- **Ergebnis: gesperrt.** Betreiber um Erlaubnis bitten oder anderen Weg wählen.\n")
        return z

    # Startseite
    try:
        html = http.get(url, cache=False)
    except Exception as e:  # noqa: BLE001
        z.append(f"- Startseite: Fehler ({type(e).__name__}: {str(e)[:120]})\n")
        return z
    open(os.path.join(d, "start.html"), "w", encoding="utf-8").write(html[:300000])
    soup = BeautifulSoup(html, "html.parser")
    text = pv.html_text(html)
    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
    gleich = [u for u in links if urlparse(u).netloc == p.netloc]
    treffer = [u for u in dict.fromkeys(gleich) if LINK_HINT.search(u)]
    skripte = len(soup.find_all("script"))
    spa = [txt for rx, txt in SPA_HINWEISE if re.search(rx, html, re.I)]
    z += [f"- Startseite: {len(html)} Zeichen HTML, {len(text)} Zeichen sichtbarer Text, {skripte} Skripte, "
          f"{len(gleich)} Links auf dem Host, {len(treffer)} davon verfahrensähnlich",
          f"- Hinweise auf JavaScript-Framework: {', '.join(spa) or 'keine'}"]

    # sitemap, Feeds, API-Hinweise
    try:
        sm = http.get(urljoin(root, "/sitemap.xml"), cache=False)
        locs = URL_IN_TEXT.findall(re.sub(r"</?loc>", " ", sm))
        z.append(f"- sitemap.xml: vorhanden, {len(locs)} URLs, Beispiele: " + ", ".join(locs[:3]))
    except Exception:  # noqa: BLE001
        z.append("- sitemap.xml: nicht vorhanden oder nicht abrufbar")
    feeds = _feed_urls(soup, url)
    z.append(f"- Feeds (RSS/Atom/JSON): {', '.join(feeds) if feeds else 'keine'}")
    api = sorted(set(m.group(1) for m in API_RE.finditer(html)))[:10]
    z.append(f"- Hinweise auf API/JSON-Pfade im HTML: {', '.join(api) if api else 'keine'}")
    if treffer:
        z.append("- Beispiel-Links: " + ", ".join(treffer[:5]))

    # Tiefere Proben: Listenseite, Detailseite, ggf. im Browser gerendert (zeigt, ob JavaScript-Details lesbar werden)
    kandidaten = []
    for u in dict.fromkeys(links):
        if urlparse(u).netloc != p.netloc:
            continue
        if re.search(r"/beteiligung/themen(\?format=Bauleit\w*)?$", u, re.I):
            kandidaten.append(("liste", u + ("" if "format=" in u or "bplan" in u else "?format=Bauleitplan")))
        elif re.search(r"/themen/\d+|/verfahren/[\w-]+", u, re.I) and not any(k == "detail" for k, _ in kandidaten):
            kandidaten.append(("detail", u))
    for art, u in kandidaten[:3]:
        try:
            h = http.get(u, cache=False)
        except Exception as e:  # noqa: BLE001
            z.append(f"- Probe {art} {u}: Fehler ({type(e).__name__})")
            continue
        open(os.path.join(d, f"{art}.html"), "w", encoding="utf-8").write(h[:300000])
        t = pv.html_text(h)
        weiter = re.findall(r"(?:page|seite|offset)=\d+", h, re.I)[:3]
        z.append(f"- Probe {art} {u}: {len(h)} Zeichen HTML, {len(t)} Zeichen Text, Blätter-Hinweise: {', '.join(weiter) or 'keine'}")
        if art == "detail":
            g = http.render(u)
            if g:
                open(os.path.join(d, "detail_gerendert.html"), "w", encoding="utf-8").write(g[:300000])
                z.append(f"  - im Browser gerendert: {len(pv.html_text(g))} Zeichen Text (statisch: {len(t)})")
            else:
                z.append("  - Browser nicht verfügbar oder Seite nicht geladen")

    # Urteil
    if len(text) >= 300 and len(treffer) >= 2:
        urteil = "serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden"
    elif spa or len(text) < 300:
        urteil = "vermutlich JavaScript-App -> eigener Adapter über deren API nötig (API-Hinweise prüfen)"
    else:
        urteil = "unklar -> start.html ansehen"
    z.append(f"- **Ergebnis: {urteil}**\n")
    return z


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--portale", default="portale.csv")
    ap.add_argument("--out", default="entdeckung")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    http = pv.Http()
    with open(a.portale, encoding="utf-8", newline="") as f:
        zeilen = [r for r in csv.DictReader(f) if r.get("url") and not r["name"].startswith("#")]
    md = [f"# Portal-Sonde ({dt.date.today().isoformat()})\n",
          "Prüft pro Portal robots.txt, Startseite, sitemap.xml, Feeds und API-Hinweise. "
          "Basis für die Entscheidung, ob der allgemeine Portal-Crawler reicht.\n"]
    for r in zeilen:
        print(f"→ {r['name']}")
        md += sonde(http, r["name"], r["url"], a.out)
    pfad = os.path.join(a.out, "portale_bericht.md")
    open(pfad, "w", encoding="utf-8").write("\n".join(md))
    print(f"\nBericht: {pfad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

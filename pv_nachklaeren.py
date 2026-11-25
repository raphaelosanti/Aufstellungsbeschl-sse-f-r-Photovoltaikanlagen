#!/usr/bin/env python3
"""
Phase nachklären: Detailseite und PDFs öffnen, wenn der Beschlusstyp "Unklar" ist
===============================================================================

Viele Treffer (Gemeinde-Homepages, Landesportale, Vorlagen mit knappem Titel) nennen im Titel keine Phase.
Dieses Modul öffnet für solche Einträge die Detailseite (bei JavaScript-Seiten im Browser) sowie bis zu
4 verlinkte PDFs (Beschlussvorlage, Bekanntmachung, Begründung), liest den Beschlussvorschlag und bestimmt
daraus den Verfahrensschritt (Aufstellungsbeschluss, frühzeitige Beteiligung, Auslegung, Abwägung, Satzung ...).
Fehlende Angaben (Plan-Name, Fläche, Leistung, Entwickler) werden aus dem größeren Text ergänzt.

Vorsicht statt Raten: Bleibt der Schritt unklar, bleibt er "Unklar". Jeder Eintrag wird höchstens alle
60 Tage erneut geprüft.
"""
from __future__ import annotations

import datetime as dt
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

ABSCHNITT_RE = re.compile(r"beschlussvorschlag|beschlussempfehlung|beschlussentwurf|beschlusstext|beschließt|"
                          r"wird beschlossen|beschlossen wird|der (gemeinde|stadt|ortsgemeinde|verbandsgemeinde)?rat .{0,40}beschließt",
                          re.I)
PDF_RE = re.compile(r"\.pdf|getfile|download|dokument|anlage|bekanntmachung|begr[üu]ndung|vorlage", re.I)
NEU_PRUEFEN_TAGE = 60
MAX_PDFS = 4
BEZUG = re.compile(r"beschl|bekannt|ausleg|beteilig|satzung|aufstell|abw[äa]g", re.I)


def beschlussabschnitt(text: str) -> str:
    m = ABSCHNITT_RE.search(text)
    return text[m.start():m.start() + 1800] if m else ""


def typ_aus_text(pv, titel: str, text: str) -> str | None:
    """Verfahrensschritt aus Titel, Beschlussvorschlag oder – nur bei Beschluss-/Bekanntmachungsbezug – dem übrigen Text."""
    for quelle in (titel, beschlussabschnitt(text)):
        low = quelle.lower()
        for name, pat in reversed(pv.BESCHLUSS_TYPEN):          # späterer Schritt gewinnt
            if re.search(pat, low):
                return name
    low = text[:12000].lower()
    for name, pat in reversed(pv.BESCHLUSS_TYPEN):
        for m in re.finditer(pat, low):
            if BEZUG.search(low[max(0, m.start() - 150):m.end() + 150]):
                return name
    return None


def _seitentext(http, pv, url: str):
    """(Text, PDF-Links) einer Seite; JavaScript-Seiten im Browser nachladen."""
    if re.search(r"\.pdf(\?|$)", url, re.I):
        return pv.dokument_text(http, url), []
    html = http.get(url, cache=False)
    soup = BeautifulSoup(html, "html.parser")
    text = pv.html_text(html)
    if len(text) < 400 and soup.find("script"):
        g = http.render(url)
        if g:
            html = g
            soup = BeautifulSoup(html, "html.parser")
            text = pv.html_text(html)
    pdfs = []
    for a in soup.find_all("a", href=True):
        absu = urljoin(url, a["href"]).split("#")[0]
        if PDF_RE.search(absu + " " + a.get_text(" ", strip=True)) and not re.search(r"\.(png|jpe?g|gif|zip|docx?|xlsx?)$", absu, re.I):
            pdfs.append(absu)
    return text, list(dict.fromkeys(pdfs))


def klaere_eintrag(http, pv, b) -> bool:
    """Versucht, den Schritt eines unklaren Beschlusses zu bestimmen. True, wenn geändert."""
    texte, pdfs = [], []
    seiten = [u for u in (b.link, b.dokument_link) if u]
    for u in dict.fromkeys(seiten):
        try:
            t, p = _seitentext(http, pv, u)
        except Exception:  # noqa: BLE001
            continue
        texte.append(t)
        pdfs += p
    for u in list(dict.fromkeys(pdfs))[:MAX_PDFS]:
        if u in seiten:
            continue
        try:
            texte.append(pv.dokument_text(http, u)[:20000])
        except Exception:  # noqa: BLE001
            continue
    text = "\n".join(texte)[:80000]
    if not text.strip():
        return False
    typ = typ_aus_text(pv, b.titel, text)
    if not typ:
        return False
    b.beschlusstyp = typ
    # Fehlende Angaben aus dem größeren Text ergänzen
    q = pv.Quelle(b.quelle or b.gemeinde, b.landkreis, "html", b.link or "", b.bundesland)
    n = pv.extrahiere_heuristisch({"titel": b.titel, "datum": b.datum, "text": text, "link": b.link,
                                   "dokument_link": b.dokument_link, "body_name": b.gemeinde}, q)
    for feld in ("planname", "plannr", "flaeche_ha", "leistung_mw", "entwickler", "konzept"):
        if not getattr(b, feld, "") and getattr(n, feld, ""):
            setattr(b, feld, getattr(n, feld))
    return True


def nachklaeren(http, z, beschluesse: list, max_n: int = 200, parallel: int = 1) -> None:
    import pv_beschluesse as pv
    heute = dt.date.today()
    todo = []
    for b in beschluesse:
        if b.beschlusstyp != "Unklar" or not (b.link or b.dokument_link):
            continue
        zuletzt = z.marke("_nachklaeren", b.schluessel or b.link)
        if zuletzt and (heute - dt.date.fromisoformat(zuletzt)).days < NEU_PRUEFEN_TAGE:
            continue
        todo.append(b)
    todo = todo[:max_n]
    if not todo:
        return
    print(f"Phase nachklären: {len(todo)} unklare Einträge …", flush=True)

    def arbeit(b):
        try:
            return klaere_eintrag(http, pv, b)
        except Exception as e:  # noqa: BLE001
            print(f"   ! Nachklären fehlgeschlagen ({b.gemeinde}): {e}")
            return False

    if parallel > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=parallel) as pool:
            ergebnis = list(pool.map(arbeit, todo))
    else:
        ergebnis = [arbeit(b) for b in todo]
    for b in todo:
        z.setze("_nachklaeren", b.schluessel or b.link, heute.isoformat())
    geklaert = sum(ergebnis)
    print(f"   Phase geklärt: {geklaert} von {len(todo)}", flush=True)
    for b, ok in zip(todo, ergebnis):
        if ok:
            print(f"   ✓ {b.gemeinde} | {b.beschlusstyp} | {b.titel[:70]}")

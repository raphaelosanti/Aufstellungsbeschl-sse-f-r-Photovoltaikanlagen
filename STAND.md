# Stand des PV-Beschlussregisters (26.11.2026)

Diese Datei wird nach jedem Lauf automatisch erzeugt (`stand_bericht.py`). Konzept und Ablauf stehen in `KONZEPT.md`, der Verlauf in `daten/verlauf.csv`, das Protokoll in `daten/ereignisse.csv`.

## Kennzahlen

- **Projekte:** 1506 (+1131 seit 2026-11-25)
- **davon mit Aufstellungsbeschluss:** 625 (+478 seit 2026-11-25)
- **Phase noch unklar:** 504 Projekte (+371 seit 2026-11-25); 603 Beschlüsse mit unklarem Typ (+449 seit 2026-11-25)
- **Beschlüsse insgesamt:** 2549 (+1811 seit 2026-11-25)
- **Quellen nach Art:** homepage 8394, amtsblatt 1870, sessionnet 475, auto 268, oparl 151, html 28, ihk 19, portal 10, bremen 1
- **Quellen:** 11216 angebunden, davon 5880 schon abgefragt, 5875 in den letzten 2 Tagen; letzter Abruf 2026-11-26
- **Gemeinden:** 11494 bekannt, 9552 geprüft (1119 mit RIS, 7950 ohne erkanntes RIS, 260 ohne Homepage, 223 gesperrt), 1942 noch nie geprüft

## Trefferquote gegenüber der Erwartung (MaStR)

Erwartung: 2339 Gemeinden mit Freiflächen-PV ab 1 MW, im MaStR seit 2021 registriert (mindestens 2827 Parks). Wo ein Park gebaut oder geplant wird, gab es meist einen Bebauungsplan und damit einen Aufstellungsbeschluss. Das ist eine Näherung, kein Soll.

| Maß | Wert | Bedeutung |
|---|---|---|
| Gesamt-Trefferquote | 244 von 2339 = 10.4 % | Gemeinden mit MaStR-Freiflächenpark, für die das Register ein Projekt hat |
| Erreichbarkeit | 481 von 2339 = 20.6 % | Gemeinden, deren RIS angebunden ist (Treffer oder nicht) |
| Trefferquote bei erreichbarer Quelle | 244 von 481 = 50.7 % | Wo wir suchen können: wie oft finden wir etwas? |
| Register-Gemeinden außerhalb der MaStR-Liste | 453 von 697 | Gemeinden mit Projekt im Register, aber ohne MaStR-Freiflächenpark ab 1 MW: Frühphase, noch nicht registriert (der eigentliche Mehrwert) oder Namensabgleich |

Gesamt = Erreichbarkeit × Trefferquote bei Quelle (20.6 % × 50.7 %). Der Verlust liegt also vor allem bei der Erreichbarkeit, nicht beim Filter.

**Grobe Hochrechnung:** Wären alle 2339 Gemeinden erreichbar und die Trefferquote bliebe bei 50.7 %, ergäbe das etwa 1187 Gemeinden mit Projekt (heute 244). Die Quote ist vermutlich zu niedrig angesetzt: Aufstellungsbeschlüsse vor 2022 sind nicht erfasst, und privilegierte Anlagen haben keinen Beschluss. Andererseits sind Projekte, die noch nicht im MaStR stehen (genau die Frühphase), in der Erwartung gar nicht enthalten. Die wahre Zahl liegt also eher darüber.

Je Bundesland (MaStR-Gemeinden):

| Land | MaStR-Gemeinden | im Register | Quelle ohne Treffer | kein RIS | ungeprüft | sonstige | Treffer | erreichbar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 236 | 14 | 20 | 144 | 53 | 5 | 5.9 % | 14.4 % |
| Bayern | 830 | 75 | 60 | 373 | 303 | 19 | 9.0 % | 16.3 % |
| Berlin | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Brandenburg | 132 | 22 | 4 | 104 | 0 | 2 | 16.7 % | 19.7 % |
| Hamburg | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Hessen | 96 | 17 | 8 | 71 | 0 | 0 | 17.7 % | 26.0 % |
| Mecklenburg-Vorpommern | 147 | 11 | 15 | 120 | 0 | 1 | 7.5 % | 17.7 % |
| Niedersachsen | 152 | 21 | 28 | 90 | 0 | 13 | 13.8 % | 32.2 % |
| Nordrhein-Westfalen | 140 | 20 | 45 | 72 | 0 | 3 | 14.3 % | 46.4 % |
| Rheinland-Pfalz | 173 | 19 | 21 | 77 | 56 | 0 | 11.0 % | 23.1 % |
| Saarland | 24 | 3 | 4 | 15 | 0 | 2 | 12.5 % | 29.2 % |
| Sachsen | 89 | 11 | 7 | 71 | 0 | 0 | 12.4 % | 20.2 % |
| Sachsen-Anhalt | 97 | 11 | 6 | 80 | 0 | 0 | 11.3 % | 17.5 % |
| Schleswig-Holstein | 142 | 14 | 14 | 100 | 0 | 14 | 9.9 % | 19.7 % |
| Thüringen | 79 | 6 | 5 | 68 | 0 | 0 | 7.6 % | 13.9 % |

## Je Bundesland

| Land | Quellen | Gemeinden | RIS | kein RIS | ungeprüft | Projekte | mit Aufst.-Beschl. | Frühphase | Auslegung/Abwägung | Satzung | Unklar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 1012 | 1101 | 115 | 743 | 229 | 70 | 32 | 26 | 18 | 8 | 18 |
| Bayern | 1679 | 2205 | 152 | 1123 | 809 | 266 | 129 | 126 | 39 | 28 | 73 |
| Berlin | 14 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brandenburg | 592 | 419 | 27 | 375 | 0 | 125 | 54 | 45 | 21 | 14 | 45 |
| Bremen | 5 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hamburg | 9 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hessen | 1172 | 432 | 50 | 376 | 0 | 93 | 42 | 41 | 18 | 7 | 27 |
| Mecklenburg-Vorpommern | 841 | 814 | 86 | 693 | 0 | 39 | 19 | 19 | 8 | 6 | 6 |
| Niedersachsen | 1178 | 1039 | 166 | 758 | 2 | 192 | 88 | 87 | 26 | 14 | 65 |
| Nordrhein-Westfalen | 590 | 396 | 127 | 256 | 0 | 155 | 57 | 50 | 33 | 22 | 50 |
| Rheinland-Pfalz | 1376 | 2307 | 219 | 1181 | 898 | 332 | 108 | 115 | 44 | 21 | 152 |
| Saarland | 85 | 53 | 5 | 35 | 0 | 8 | 2 | 5 | 2 | 0 | 1 |
| Sachsen | 578 | 468 | 15 | 441 | 0 | 47 | 16 | 18 | 9 | 3 | 17 |
| Sachsen-Anhalt | 211 | 227 | 33 | 190 | 0 | 66 | 30 | 27 | 12 | 10 | 17 |
| Schleswig-Holstein | 1006 | 1121 | 96 | 922 | 3 | 67 | 22 | 24 | 24 | 1 | 18 |
| Thüringen | 868 | 908 | 27 | 854 | 1 | 46 | 26 | 26 | 3 | 2 | 15 |
| **Gesamt** | **11216** | **11494** | **1119** | **7950** | **1942** | **1506** | **625** | **609** | **257** | **136** | **504** |

## Was zuletzt passiert ist

- 2026-11-26 · neues Projekt · Ellersleben (Thüringen): Ellersleben (Phase: Unklar)
- 2026-11-26 · neues Projekt · Ecklingerode (Thüringen): Ecklingerode (Phase: Unklar)
- 2026-11-26 · neues Projekt · Erfurt (Thüringen): Erfurt (Phase: Unklar)
- 2026-11-26 · neues Projekt · Riethgen (Thüringen): Riethgen (Phase: Unklar)
- 2026-11-26 · neues Projekt · Mühlhausen/Thüringen (Thüringen): Solarthermie und Geothermie  
nordwestlich der Stadtwerke (Phase: Auslegung/Abwägung)
- 2026-11-26 · neues Projekt · Kannawurf (Thüringen): Am Fuchsgründchen (Phase: Unklar)
- 2026-11-26 · neues Projekt · Hörselberg-Hainich (Thüringen): Am Karnhög (Phase: Unklar)
- 2026-11-26 · neues Projekt · Göllnitz (Thüringen): Wasserturmstr. 16a Starkenberg OT Neuposa (Phase: Unklar)
- 2026-11-26 · neues Projekt · Ebeleben (Thüringen): Weidengasse (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Abtsbessingen (Thüringen): Weidengasse (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Bilzingsleben (Thüringen): Photovoltaik -Frei-
flächenanlage - Solarpark Bilzingsleben (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Kella (Thüringen): Ershausen/Geismar (Phase: Satzung/rechtskräftig)
- 2026-11-26 · neues Projekt · Kella (Thüringen): Erweiterung Hintergas-
se (Phase: Auslegung/Abwägung)
- 2026-11-26 · neues Projekt · Greiz (Thüringen): Solarpark Greiz-Dölau (Phase: Unklar)
- 2026-11-26 · neues Projekt · Helbedündorf (Thüringen): Solarpark Friedrichs-
rode (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Ellersleben (Thüringen): Umsetzung ja oder nein (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Buttstädt (Thüringen): Umsetzung ja oder nein (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Gerstungen (Thüringen): Gerstungen (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Ködderitzsch (Thüringen): Kronos Solar (Phase: Unklar)
- 2026-11-26 · neues Projekt · Bad Berka (Thüringen): In der Unteraue (Phase: Auslegung/Abwägung)
- 2026-11-26 · neues Projekt · Neumark (Thüringen): Erneuerbare Ener-
gien Neumark (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Gerstungen (Thüringen): Hasenberg (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Menteroda (Thüringen): Solarpark Sollstedt (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Ködderitzsch (Thüringen): Solarpark Schmiedehausen (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Bilzingsleben (Thüringen): Erneuerbare-Energien-Gesetzes (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Ködderitzsch (Thüringen): Solarpark Bad Sulza (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Vachdorf (Thüringen): Dolmar-Salzbrücke (Phase: Unklar)
- 2026-11-26 · neues Projekt · Bilzingsleben (Thüringen): Solarpark Bilzingsleben an der Alten
Frömmstedter Straße (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Mühlhausen/Thüringen (Thüringen): Solarpark Schröterode (Phase: Frühphase)
- 2026-11-26 · neues Projekt · Riethgen (Thüringen): Photovoltaikfreiflächenanlage (Phase: Frühphase)

## Verlauf

| Datum | Projekte | mit Aufst.-Beschl. | Unklar | Beschlüsse | Quellen abgefragt | Gemeinden geprüft | MaStR im Register |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-26 | 1506 | 625 | 504 | 2549 | 5880 | 9552 | 244 |
| 2026-11-25 | 375 | 147 | 133 | 738 | 114 | 6480 | 46 |

## Offene Hebel (Zahlen von heute)

- 237 MaStR-Gemeinden haben ein angebundenes RIS, aber keinen Treffer: Filter, Zeitraum (ab 2022) und Adapter prüfen.
- 1387 MaStR-Gemeinden ohne erkanntes RIS: Homepage-Crawler (`quellen_homepage.csv`) und Amt-Zuordnung.
- 412 MaStR-Gemeinden noch nie geprüft: Quellensuche läuft täglich weiter.
- 1942 Gemeinden insgesamt noch nie geprüft.
- 504 Projekte mit unklarer Phase: Schritt „Phase nachklären“ (Detailseiten/PDFs).

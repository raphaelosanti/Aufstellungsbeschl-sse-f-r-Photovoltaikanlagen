# Stand des PV-Beschlussregisters (27.11.2026)

Diese Datei wird nach jedem Lauf automatisch erzeugt (`stand_bericht.py`). Konzept und Ablauf stehen in `KONZEPT.md`, der Verlauf in `daten/verlauf.csv`, das Protokoll in `daten/ereignisse.csv`.

## Kennzahlen

- **Projekte:** 2499 (+993 seit 2026-11-26)
- **davon mit Aufstellungsbeschluss:** 1100 (+475 seit 2026-11-26)
- **Phase noch unklar:** 770 Projekte (+266 seit 2026-11-26); 965 Beschlüsse mit unklarem Typ (+362 seit 2026-11-26)
- **Beschlüsse insgesamt:** 4211 (+1662 seit 2026-11-26)
- **Quellen nach Art:** homepage 9899, amtsblatt 3319, sessionnet 610, auto 321, oparl 155, html 28, ihk 19, portal 10, bremen 1
- **Quellen:** 14362 angebunden, davon 9983 schon abgefragt, 9982 in den letzten 2 Tagen; letzter Abruf 2026-11-27
- **Gemeinden:** 11494 bekannt, 11470 geprüft (1451 mit RIS, 9452 ohne erkanntes RIS, 320 ohne Homepage, 247 gesperrt), 24 noch nie geprüft

## Trefferquote gegenüber der Erwartung (MaStR)

Erwartung: 2339 Gemeinden mit Freiflächen-PV ab 1 MW, im MaStR seit 2021 registriert (mindestens 2827 Parks). Wo ein Park gebaut oder geplant wird, gab es meist einen Bebauungsplan und damit einen Aufstellungsbeschluss. Das ist eine Näherung, kein Soll.

| Maß | Wert | Bedeutung |
|---|---|---|
| Gesamt-Trefferquote | 418 von 2339 = 17.9 % | Gemeinden mit MaStR-Freiflächenpark, für die das Register ein Projekt hat |
| Erreichbarkeit | 666 von 2339 = 28.5 % | Gemeinden, deren RIS angebunden ist (Treffer oder nicht) |
| Trefferquote bei erreichbarer Quelle | 418 von 666 = 62.8 % | Wo wir suchen können: wie oft finden wir etwas? |
| Register-Gemeinden außerhalb der MaStR-Liste | 756 von 1174 | Gemeinden mit Projekt im Register, aber ohne MaStR-Freiflächenpark ab 1 MW: Frühphase, noch nicht registriert (der eigentliche Mehrwert) oder Namensabgleich |

Gesamt = Erreichbarkeit × Trefferquote bei Quelle (28.5 % × 62.8 %). Der Verlust liegt also vor allem bei der Erreichbarkeit, nicht beim Filter.

**Grobe Hochrechnung:** Wären alle 2339 Gemeinden erreichbar und die Trefferquote bliebe bei 62.8 %, ergäbe das etwa 1468 Gemeinden mit Projekt (heute 418). Die Quote ist vermutlich zu niedrig angesetzt: Aufstellungsbeschlüsse vor 2022 sind nicht erfasst, und privilegierte Anlagen haben keinen Beschluss. Andererseits sind Projekte, die noch nicht im MaStR stehen (genau die Frühphase), in der Erwartung gar nicht enthalten. Die wahre Zahl liegt also eher darüber.

Je Bundesland (MaStR-Gemeinden):

| Land | MaStR-Gemeinden | im Register | Quelle ohne Treffer | kein RIS | ungeprüft | sonstige | Treffer | erreichbar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 236 | 71 | 14 | 142 | 2 | 7 | 30.1 % | 36.0 % |
| Bayern | 830 | 159 | 90 | 556 | 5 | 20 | 19.2 % | 30.0 % |
| Berlin | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Brandenburg | 132 | 22 | 4 | 104 | 0 | 2 | 16.7 % | 19.7 % |
| Hamburg | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Hessen | 96 | 17 | 8 | 71 | 0 | 0 | 17.7 % | 26.0 % |
| Mecklenburg-Vorpommern | 147 | 16 | 11 | 119 | 0 | 1 | 10.9 % | 18.4 % |
| Niedersachsen | 152 | 30 | 21 | 88 | 0 | 13 | 19.7 % | 33.6 % |
| Nordrhein-Westfalen | 140 | 17 | 45 | 75 | 0 | 3 | 12.1 % | 44.3 % |
| Rheinland-Pfalz | 173 | 37 | 21 | 115 | 0 | 0 | 21.4 % | 33.5 % |
| Saarland | 24 | 3 | 4 | 15 | 0 | 2 | 12.5 % | 29.2 % |
| Sachsen | 89 | 11 | 7 | 71 | 0 | 0 | 12.4 % | 20.2 % |
| Sachsen-Anhalt | 97 | 9 | 6 | 82 | 0 | 0 | 9.3 % | 15.5 % |
| Schleswig-Holstein | 142 | 18 | 12 | 98 | 0 | 14 | 12.7 % | 21.1 % |
| Thüringen | 79 | 8 | 5 | 66 | 0 | 0 | 10.1 % | 16.5 % |

## Je Bundesland

| Land | Quellen | Gemeinden | RIS | kein RIS | ungeprüft | Projekte | mit Aufst.-Beschl. | Frühphase | Auslegung/Abwägung | Satzung | Unklar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 1895 | 1101 | 145 | 927 | 6 | 385 | 167 | 142 | 77 | 46 | 120 |
| Bayern | 3187 | 2205 | 264 | 1745 | 9 | 614 | 295 | 300 | 97 | 51 | 166 |
| Berlin | 14 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brandenburg | 592 | 419 | 27 | 375 | 0 | 127 | 55 | 46 | 23 | 14 | 44 |
| Bremen | 5 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hamburg | 9 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hessen | 1175 | 432 | 50 | 376 | 0 | 92 | 42 | 41 | 22 | 7 | 22 |
| Mecklenburg-Vorpommern | 841 | 814 | 86 | 693 | 0 | 81 | 53 | 47 | 13 | 14 | 7 |
| Niedersachsen | 1180 | 1039 | 166 | 760 | 0 | 326 | 166 | 159 | 35 | 28 | 104 |
| Nordrhein-Westfalen | 590 | 396 | 127 | 256 | 0 | 151 | 56 | 48 | 31 | 22 | 50 |
| Rheinland-Pfalz | 2126 | 2307 | 409 | 1875 | 5 | 476 | 160 | 166 | 78 | 44 | 188 |
| Saarland | 85 | 53 | 5 | 35 | 0 | 8 | 2 | 5 | 2 | 0 | 1 |
| Sachsen | 578 | 468 | 15 | 441 | 0 | 47 | 16 | 17 | 11 | 3 | 16 |
| Sachsen-Anhalt | 211 | 227 | 33 | 190 | 0 | 53 | 27 | 24 | 8 | 6 | 15 |
| Schleswig-Holstein | 1006 | 1121 | 96 | 922 | 3 | 86 | 30 | 33 | 27 | 2 | 24 |
| Thüringen | 868 | 908 | 27 | 854 | 1 | 53 | 31 | 31 | 6 | 3 | 13 |
| **Gesamt** | **14362** | **11494** | **1451** | **9452** | **24** | **2499** | **1100** | **1059** | **430** | **240** | **770** |

## Was zuletzt passiert ist

- 2026-11-27 · neues Projekt · Neuwied (Rheinland-Pfalz): SWN-Netzentwicklungsplan (Phase: Satzung/rechtskräftig)
- 2026-11-27 · neues Projekt · Ramstein-Miesenbach (Rheinland-Pfalz): Photovoltaik (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Urbar (Rheinland-Pfalz): Deutsche Giganetz GmbH (Phase: Unklar)
- 2026-11-27 · neues Projekt · Verbandsgemeinderat - 26.11.2026 - 18:30 Uhr (Rheinland-Pfalz): Verbandsgemeinderat - 26.11.2026 - 18:30 Uhr (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Neustadt (Wied) (Rheinland-Pfalz): Neustadt (Wied) (Phase: Unklar)
- 2026-11-27 · neues Projekt · Sankt Johann (Rheinland-Pfalz): Sankt Johann (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Asbach (Rheinland-Pfalz): Asbach (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Verbandsgemeinde Asbach (Rheinland-Pfalz): Verbandsgemeinde Asbach (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Neustadt (Wied) (Rheinland-Pfalz): Neustadt (Wied) (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Unklar)
- 2026-11-27 · neues Projekt · Neustadt (Wied) (Rheinland-Pfalz): Neustadt (Wied) (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Vallendar (Rheinland-Pfalz): Vallendar (Phase: Unklar)
- 2026-11-27 · neues Projekt · Vallendar (Rheinland-Pfalz): Vallendar (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Vallendar (Rheinland-Pfalz): Freiflächenfotovoltaik (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Sprendlingen (Rheinland-Pfalz): Sprendlingen (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Unklar)
- 2026-11-27 · neues Projekt · Bingen am Rhein (Rheinland-Pfalz): Bingen am Rhein (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Sprendlingen (Rheinland-Pfalz): Sprendlingen (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Urbar (Rheinland-Pfalz): Urbar (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Vallendar (Rheinland-Pfalz): Bündnis 90 - Die Grünen (Phase: Unklar)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Auslegung/Abwägung)
- 2026-11-27 · neues Projekt · Gensingen (Rheinland-Pfalz): Gensingen (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Bocholt (Nordrhein-Westfalen): Zuteilung von Kapazitäten (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Hamminkeln (Nordrhein-Westfalen): Freiflächen-PV-Anlage (Phase: Unklar)
- 2026-11-27 · neues Projekt · Emmerich am Rhein (Nordrhein-Westfalen): Emmerich am Rhein (Phase: Satzung/rechtskräftig)

## Verlauf

| Datum | Projekte | mit Aufst.-Beschl. | Unklar | Beschlüsse | Quellen abgefragt | Gemeinden geprüft | MaStR im Register |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-27 | 2499 | 1100 | 770 | 4211 | 9983 | 11470 | 418 |
| 2026-11-26 | 1506 | 625 | 504 | 2549 | 5880 | 9552 | 244 |
| 2026-11-25 | 375 | 147 | 133 | 738 | 114 | 6480 | 46 |

## Offene Hebel (Zahlen von heute)

- 248 MaStR-Gemeinden haben ein angebundenes RIS, aber keinen Treffer: Filter, Zeitraum (ab 2022) und Adapter prüfen.
- 1604 MaStR-Gemeinden ohne erkanntes RIS: Homepage-Crawler (`quellen_homepage.csv`) und Amt-Zuordnung.
- 7 MaStR-Gemeinden noch nie geprüft: Quellensuche läuft täglich weiter.
- 24 Gemeinden insgesamt noch nie geprüft.
- 770 Projekte mit unklarer Phase: Schritt „Phase nachklären“ (Detailseiten/PDFs).

# Stand des PV-Beschlussregisters (25.11.2026)

Diese Datei wird nach jedem Lauf automatisch erzeugt (`stand_bericht.py`). Konzept und Ablauf stehen in `KONZEPT.md`, der Verlauf in `daten/verlauf.csv`, das Protokoll in `daten/ereignisse.csv`.

## Kennzahlen

- **Projekte:** 375
- **davon mit Aufstellungsbeschluss:** 147
- **Phase noch unklar:** 133 Projekte; 154 Beschlüsse mit unklarem Typ
- **Beschlüsse insgesamt:** 738
- **Quellen:** 470 angebunden, davon 114 schon abgefragt, 109 in den letzten 2 Tagen; letzter Abruf 2026-11-23
- **Gemeinden:** 11494 bekannt, 6480 geprüft (565 mit RIS, 5706 ohne erkanntes RIS, 196 ohne Homepage, 13 gesperrt), 5014 noch nie geprüft

## Trefferquote gegenüber der Erwartung (MaStR)

Erwartung: 2339 Gemeinden mit Freiflächen-PV ab 1 MW, im MaStR seit 2021 registriert (mindestens 2827 Parks). Wo ein Park gebaut oder geplant wird, gab es meist einen Bebauungsplan und damit einen Aufstellungsbeschluss. Das ist eine Näherung, kein Soll.

| Maß | Wert | Bedeutung |
|---|---|---|
| Gesamt-Trefferquote | 46 von 2339 = 2.0 % | Gemeinden mit MaStR-Freiflächenpark, für die das Register ein Projekt hat |
| Erreichbarkeit | 187 von 2339 = 8.0 % | Gemeinden, deren RIS angebunden ist (Treffer oder nicht) |
| Trefferquote bei erreichbarer Quelle | 46 von 187 = 24.6 % | Wo wir suchen können: wie oft finden wir etwas? |
| Register-Gemeinden außerhalb der MaStR-Liste | 109 von 155 | Gemeinden mit Projekt im Register, aber ohne MaStR-Freiflächenpark ab 1 MW: Frühphase, noch nicht registriert (der eigentliche Mehrwert) oder Namensabgleich |

Gesamt = Erreichbarkeit × Trefferquote bei Quelle (8.0 % × 24.6 %). Der Verlust liegt also vor allem bei der Erreichbarkeit, nicht beim Filter.

**Grobe Hochrechnung:** Wären alle 2339 Gemeinden erreichbar und die Trefferquote bliebe bei 24.6 %, ergäbe das etwa 575 Gemeinden mit Projekt (heute 46). Die Quote ist vermutlich zu niedrig angesetzt: Aufstellungsbeschlüsse vor 2022 sind nicht erfasst, und privilegierte Anlagen haben keinen Beschluss. Andererseits sind Projekte, die noch nicht im MaStR stehen (genau die Frühphase), in der Erwartung gar nicht enthalten. Die wahre Zahl liegt also eher darüber.

Je Bundesland (MaStR-Gemeinden):

| Land | MaStR-Gemeinden | im Register | Quelle ohne Treffer | kein RIS | ungeprüft | sonstige | Treffer | erreichbar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 236 | 4 | 2 | 41 | 188 | 1 | 1.7 % | 2.5 % |
| Bayern | 830 | 6 | 23 | 212 | 572 | 17 | 0.7 % | 3.5 % |
| Berlin | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Brandenburg | 132 | 8 | 2 | 120 | 0 | 2 | 6.1 % | 7.6 % |
| Hamburg | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Hessen | 96 | 5 | 9 | 82 | 0 | 0 | 5.2 % | 14.6 % |
| Mecklenburg-Vorpommern | 147 | 5 | 0 | 137 | 4 | 1 | 3.4 % | 3.4 % |
| Niedersachsen | 152 | 2 | 24 | 81 | 44 | 1 | 1.3 % | 17.1 % |
| Nordrhein-Westfalen | 140 | 4 | 42 | 94 | 0 | 0 | 2.9 % | 32.9 % |
| Rheinland-Pfalz | 173 | 7 | 9 | 34 | 123 | 0 | 4.0 % | 9.2 % |
| Saarland | 24 | 0 | 2 | 22 | 0 | 0 | 0.0 % | 8.3 % |
| Sachsen | 89 | 0 | 7 | 82 | 0 | 0 | 0.0 % | 7.9 % |
| Sachsen-Anhalt | 97 | 3 | 9 | 85 | 0 | 0 | 3.1 % | 12.4 % |
| Schleswig-Holstein | 142 | 1 | 8 | 88 | 45 | 0 | 0.7 % | 6.3 % |
| Thüringen | 79 | 1 | 4 | 59 | 15 | 0 | 1.3 % | 6.3 % |

## Je Bundesland

| Land | Quellen | Gemeinden | RIS | kein RIS | ungeprüft | Projekte | mit Aufst.-Beschl. | Frühphase | Auslegung/Abwägung | Satzung | Unklar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 12 | 1101 | 12 | 166 | 923 | 38 | 16 | 12 | 8 | 4 | 14 |
| Bayern | 60 | 2205 | 60 | 570 | 1505 | 6 | 4 | 4 | 1 | 0 | 1 |
| Berlin | 13 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brandenburg | 25 | 419 | 22 | 380 | 0 | 81 | 32 | 25 | 12 | 10 | 34 |
| Bremen | 3 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hamburg | 8 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hessen | 50 | 432 | 50 | 376 | 0 | 28 | 12 | 12 | 3 | 1 | 12 |
| Mecklenburg-Vorpommern | 9 | 814 | 18 | 731 | 32 | 23 | 10 | 12 | 5 | 3 | 3 |
| Niedersachsen | 73 | 1039 | 93 | 578 | 331 | 9 | 3 | 1 | 3 | 1 | 4 |
| Nordrhein-Westfalen | 109 | 396 | 108 | 288 | 0 | 43 | 14 | 8 | 12 | 6 | 17 |
| Rheinland-Pfalz | 37 | 2307 | 85 | 623 | 1597 | 88 | 27 | 29 | 23 | 9 | 27 |
| Saarland | 2 | 53 | 2 | 50 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Sachsen | 15 | 468 | 15 | 441 | 0 | 5 | 2 | 2 | 0 | 0 | 3 |
| Sachsen-Anhalt | 21 | 227 | 33 | 190 | 0 | 19 | 9 | 7 | 4 | 3 | 5 |
| Schleswig-Holstein | 23 | 1121 | 47 | 653 | 418 | 19 | 7 | 6 | 5 | 0 | 8 |
| Thüringen | 10 | 908 | 20 | 656 | 208 | 16 | 11 | 10 | 0 | 1 | 5 |
| **Gesamt** | **470** | **11494** | **565** | **5706** | **5014** | **375** | **147** | **128** | **76** | **38** | **133** |

## Was zuletzt passiert ist

Noch keine Ereignisse. Ab dem nächsten Lauf werden neue Projekte, erkannte Aufstellungsbeschlüsse und Phasenwechsel hier protokolliert (Ausgangsstand heute: 375 Projekte).

## Verlauf

| Datum | Projekte | mit Aufst.-Beschl. | Unklar | Beschlüsse | Quellen abgefragt | Gemeinden geprüft | MaStR im Register |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-25 | 375 | 147 | 133 | 738 | 114 | 6480 | 46 |

## Offene Hebel (Zahlen von heute)

- 141 MaStR-Gemeinden haben ein angebundenes RIS, aber keinen Treffer: Filter, Zeitraum (ab 2022) und Adapter prüfen.
- 1139 MaStR-Gemeinden ohne erkanntes RIS: Homepage-Crawler (`quellen_homepage.csv`) und Amt-Zuordnung.
- 991 MaStR-Gemeinden noch nie geprüft: Quellensuche läuft täglich weiter.
- 5014 Gemeinden insgesamt noch nie geprüft.
- 133 Projekte mit unklarer Phase: Schritt „Phase nachklären“ (Detailseiten/PDFs).

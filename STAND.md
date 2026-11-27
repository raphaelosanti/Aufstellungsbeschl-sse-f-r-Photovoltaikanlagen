# Stand des PV-Beschlussregisters (27.11.2026)

Diese Datei wird nach jedem Lauf automatisch erzeugt (`stand_bericht.py`). Konzept und Ablauf stehen in `KONZEPT.md`, der Verlauf in `daten/verlauf.csv`, das Protokoll in `daten/ereignisse.csv`.

## Kennzahlen

- **Projekte:** 1977 (+471 seit 2026-11-26)
- **davon mit Aufstellungsbeschluss:** 861 (+236 seit 2026-11-26)
- **Phase noch unklar:** 615 Projekte (+111 seit 2026-11-26); 741 Beschlüsse mit unklarem Typ (+138 seit 2026-11-26)
- **Beschlüsse insgesamt:** 3340 (+791 seit 2026-11-26)
- **Quellen nach Art:** homepage 9647, amtsblatt 1870, sessionnet 595, auto 315, oparl 155, html 28, ihk 19, portal 10, bremen 1
- **Quellen:** 12640 angebunden, davon 8081 schon abgefragt, 8077 in den letzten 2 Tagen; letzter Abruf 2026-11-27
- **Gemeinden:** 11494 bekannt, 11160 geprüft (1405 mit RIS, 9203 ohne erkanntes RIS, 310 ohne Homepage, 242 gesperrt), 334 noch nie geprüft

## Trefferquote gegenüber der Erwartung (MaStR)

Erwartung: 2339 Gemeinden mit Freiflächen-PV ab 1 MW, im MaStR seit 2021 registriert (mindestens 2827 Parks). Wo ein Park gebaut oder geplant wird, gab es meist einen Bebauungsplan und damit einen Aufstellungsbeschluss. Das ist eine Näherung, kein Soll.

| Maß | Wert | Bedeutung |
|---|---|---|
| Gesamt-Trefferquote | 329 von 2339 = 14.1 % | Gemeinden mit MaStR-Freiflächenpark, für die das Register ein Projekt hat |
| Erreichbarkeit | 592 von 2339 = 25.3 % | Gemeinden, deren RIS angebunden ist (Treffer oder nicht) |
| Trefferquote bei erreichbarer Quelle | 329 von 592 = 55.6 % | Wo wir suchen können: wie oft finden wir etwas? |
| Register-Gemeinden außerhalb der MaStR-Liste | 595 von 924 | Gemeinden mit Projekt im Register, aber ohne MaStR-Freiflächenpark ab 1 MW: Frühphase, noch nicht registriert (der eigentliche Mehrwert) oder Namensabgleich |

Gesamt = Erreichbarkeit × Trefferquote bei Quelle (25.3 % × 55.6 %). Der Verlust liegt also vor allem bei der Erreichbarkeit, nicht beim Filter.

**Grobe Hochrechnung:** Wären alle 2339 Gemeinden erreichbar und die Trefferquote bliebe bei 55.6 %, ergäbe das etwa 1300 Gemeinden mit Projekt (heute 329). Die Quote ist vermutlich zu niedrig angesetzt: Aufstellungsbeschlüsse vor 2022 sind nicht erfasst, und privilegierte Anlagen haben keinen Beschluss. Andererseits sind Projekte, die noch nicht im MaStR stehen (genau die Frühphase), in der Erwartung gar nicht enthalten. Die wahre Zahl liegt also eher darüber.

Je Bundesland (MaStR-Gemeinden):

| Land | MaStR-Gemeinden | im Register | Quelle ohne Treffer | kein RIS | ungeprüft | sonstige | Treffer | erreichbar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 236 | 53 | 18 | 154 | 2 | 9 | 22.5 % | 30.1 % |
| Bayern | 830 | 96 | 97 | 572 | 46 | 19 | 11.6 % | 23.3 % |
| Berlin | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Brandenburg | 132 | 22 | 4 | 104 | 0 | 2 | 16.7 % | 19.7 % |
| Hamburg | 1 | 0 | 0 | 1 | 0 | 0 | 0.0 % | 0.0 % |
| Hessen | 96 | 17 | 8 | 71 | 0 | 0 | 17.7 % | 26.0 % |
| Mecklenburg-Vorpommern | 147 | 16 | 11 | 119 | 0 | 1 | 10.9 % | 18.4 % |
| Niedersachsen | 152 | 23 | 28 | 88 | 0 | 13 | 15.1 % | 33.6 % |
| Nordrhein-Westfalen | 140 | 17 | 45 | 75 | 0 | 3 | 12.1 % | 44.3 % |
| Rheinland-Pfalz | 173 | 36 | 18 | 101 | 18 | 0 | 20.8 % | 31.2 % |
| Saarland | 24 | 3 | 4 | 15 | 0 | 2 | 12.5 % | 29.2 % |
| Sachsen | 89 | 11 | 7 | 71 | 0 | 0 | 12.4 % | 20.2 % |
| Sachsen-Anhalt | 97 | 9 | 6 | 82 | 0 | 0 | 9.3 % | 15.5 % |
| Schleswig-Holstein | 142 | 18 | 12 | 98 | 0 | 14 | 12.7 % | 21.1 % |
| Thüringen | 79 | 8 | 5 | 66 | 0 | 0 | 10.1 % | 16.5 % |

## Je Bundesland

| Land | Quellen | Gemeinden | RIS | kein RIS | ungeprüft | Projekte | mit Aufst.-Beschl. | Frühphase | Auslegung/Abwägung | Satzung | Unklar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baden-Württemberg | 1234 | 1101 | 144 | 927 | 7 | 296 | 130 | 108 | 63 | 37 | 88 |
| Bayern | 2301 | 2205 | 254 | 1657 | 118 | 327 | 164 | 161 | 52 | 29 | 85 |
| Berlin | 14 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brandenburg | 592 | 419 | 27 | 375 | 0 | 125 | 54 | 45 | 22 | 14 | 44 |
| Bremen | 5 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hamburg | 9 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Hessen | 1172 | 432 | 50 | 376 | 0 | 92 | 42 | 41 | 18 | 7 | 26 |
| Mecklenburg-Vorpommern | 841 | 814 | 86 | 693 | 0 | 81 | 53 | 47 | 13 | 14 | 7 |
| Niedersachsen | 1178 | 1039 | 166 | 758 | 2 | 212 | 103 | 101 | 27 | 14 | 70 |
| Nordrhein-Westfalen | 590 | 396 | 127 | 256 | 0 | 148 | 55 | 47 | 31 | 21 | 49 |
| Rheinland-Pfalz | 1956 | 2307 | 374 | 1716 | 203 | 449 | 154 | 159 | 70 | 43 | 177 |
| Saarland | 85 | 53 | 5 | 35 | 0 | 8 | 2 | 5 | 2 | 0 | 1 |
| Sachsen | 578 | 468 | 15 | 441 | 0 | 47 | 16 | 17 | 11 | 3 | 16 |
| Sachsen-Anhalt | 211 | 227 | 33 | 190 | 0 | 53 | 27 | 24 | 8 | 6 | 15 |
| Schleswig-Holstein | 1006 | 1121 | 96 | 922 | 3 | 86 | 30 | 33 | 27 | 2 | 24 |
| Thüringen | 868 | 908 | 27 | 854 | 1 | 53 | 31 | 31 | 6 | 3 | 13 |
| **Gesamt** | **12640** | **11494** | **1405** | **9203** | **334** | **1977** | **861** | **819** | **350** | **193** | **615** |

## Was zuletzt passiert ist

- 2026-11-27 · neues Projekt · Wasungen (Thüringen): grün (Phase: Unklar)
- 2026-11-27 · neues Projekt · Greiz (Thüringen): Solarpark Deponie Steinsdorf (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Weida (Thüringen): Solarpark Deponie Steinsdorf (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Sondershausen (Thüringen): Soundcheck Museum (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Bodenrode-Westhausen (Thüringen): Solarpark Bodenrode-Westhausen (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Weißensee (Thüringen): Photovoltaikanlage Luthersborn, 1. BA (Phase: Frühphase)
- 2026-11-27 · neues Projekt · Schmalkalden (Thüringen): Sondergebiet Energiegewinnung aus Photovoltaik - Der Sandacker (Phase: Satzung/rechtskräftig)
- 2026-11-27 · Phase geändert · Ellersleben (Thüringen): Kloster Kerbscher Berg: Unklar → Auslegung/Abwägung
- 2026-11-27 · Phase geändert · Ecklingerode (Thüringen): Kloster Kerbscher Berg: Unklar → Auslegung/Abwägung
- 2026-11-27 · Phase geändert · Erfurt (Thüringen): Kloster Kerbscher Berg: Unklar → Auslegung/Abwägung
- 2026-11-27 · Phase geändert · Harzgerode (Sachsen-Anhalt): Harzgerode: Frühphase → Unklar
- 2026-11-27 · Phase geändert · Genthin (Sachsen-Anhalt): PV Dretzel: Frühphase → Unklar
- 2026-11-27 · Phase geändert · Gräfenhainichen (Sachsen-Anhalt): Fläming-Elbaue: Unklar → Satzung/rechtskräftig
- 2026-11-27 · Phase geändert · Osterwieck (Sachsen-Anhalt): Agri Photovoltaik Deersheim: Auslegung/Abwägung → Frühphase
- 2026-11-27 · Aufstellungsbeschluss erkannt · Flechtingen (Sachsen-Anhalt): Solarpark Klüden, Beschluss vom 2022-11-30
- 2026-11-27 · Aufstellungsbeschluss erkannt · Flechtingen (Sachsen-Anhalt): Flechtingen, Beschluss vom 2022-03-29
- 2026-11-27 · Phase geändert · Dessau-Roßlau (Sachsen-Anhalt): Photovoltaik am Dessauer Flugplatz: Unklar → Frühphase
- 2026-11-27 · Aufstellungsbeschluss erkannt · Dessau-Roßlau (Sachsen-Anhalt): Photovoltaik am Dessauer Flugplatz, Beschluss vom unbekanntem Datum
- 2026-11-27 · Phase geändert · Dessau-Roßlau (Sachsen-Anhalt): Sondergebiet Photovoltaik an der Lichtenauer Straße: Satzung/rechtskräftig → Auslegung/Abwägung
- 2026-11-27 · Phase geändert · Dessau-Roßlau (Sachsen-Anhalt): Dessau-Roßlau: Frühphase → Auslegung/Abwägung
- 2026-11-27 · Phase geändert · Möser (Sachsen-Anhalt): Osterpaket: Unklar → Frühphase
- 2026-11-27 · Aufstellungsbeschluss erkannt · Möser (Sachsen-Anhalt): Osterpaket, Beschluss vom unbekanntem Datum
- 2026-11-27 · Phase geändert · Möser (Sachsen-Anhalt): Möser: Frühphase → Unklar
- 2026-11-27 · Phase geändert · Stadtrat - 19.02.2026 - 18:00-20:25 Uhr (Sachsen-Anhalt): Stadtrat - 19.02.2026 - 18:00-20:25 Uhr: Satzung/rechtskräftig → Unklar
- 2026-11-27 · Phase geändert · Möser (Sachsen-Anhalt): FFPV-Anlage Körbelitz: Auslegung/Abwägung → Frühphase
- 2026-11-27 · Aufstellungsbeschluss erkannt · Möser (Sachsen-Anhalt): FFPV-Anlage Körbelitz, Beschluss vom 2025-11-05
- 2026-11-27 · Phase geändert · Wolmirstedt (Sachsen-Anhalt): Wolmirstedt: Satzung/rechtskräftig → Frühphase
- 2026-11-27 · Aufstellungsbeschluss erkannt · Wolmirstedt (Sachsen-Anhalt): Wolmirstedt, Beschluss vom 2025-07-01
- 2026-11-27 · Phase geändert · Dessau-Roßlau (Sachsen-Anhalt): Freiflächenphotovoltaikanlage Brambach: Auslegung/Abwägung → Frühphase
- 2026-11-27 · Phase geändert · Wolmirstedt (Sachsen-Anhalt): So ist es auch hier.: Frühphase → Unklar

## Verlauf

| Datum | Projekte | mit Aufst.-Beschl. | Unklar | Beschlüsse | Quellen abgefragt | Gemeinden geprüft | MaStR im Register |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-27 | 1977 | 861 | 615 | 3340 | 8081 | 11160 | 329 |
| 2026-11-26 | 1506 | 625 | 504 | 2549 | 5880 | 9552 | 244 |
| 2026-11-25 | 375 | 147 | 133 | 738 | 114 | 6480 | 46 |

## Offene Hebel (Zahlen von heute)

- 263 MaStR-Gemeinden haben ein angebundenes RIS, aber keinen Treffer: Filter, Zeitraum (ab 2022) und Adapter prüfen.
- 1618 MaStR-Gemeinden ohne erkanntes RIS: Homepage-Crawler (`quellen_homepage.csv`) und Amt-Zuordnung.
- 66 MaStR-Gemeinden noch nie geprüft: Quellensuche läuft täglich weiter.
- 334 Gemeinden insgesamt noch nie geprüft.
- 615 Projekte mit unklarer Phase: Schritt „Phase nachklären“ (Detailseiten/PDFs).

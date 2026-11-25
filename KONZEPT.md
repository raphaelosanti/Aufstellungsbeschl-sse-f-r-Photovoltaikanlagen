# Konzept und Ablauf des PV-Beschlussregisters

Dieses Dokument beschreibt Ziel, Quellen und Ablauf. Die aktuellen Zahlen stehen in `STAND.md` (automatisch erzeugt).

## Ziel
Ein bundesweites Register aller Gemeinde-Beschlüsse zu PV-Bebauungsplänen (Aufstellungsbeschluss bis Satzungsbeschluss) als frühes Signal für neue PV-Projekte. Das Register erfasst Bauleitplanungs-Beschlüsse aus Ratsinformationssystemen. Es ersetzt keinen Tracker für die EEG-Ausschreibungen der Bundesnetzagentur.

## Grundquelle
Ratsinformationssysteme (RIS) der Gemeinden, Ämter und Verbandsgemeinden. Daraus werden Vorlagen und Beschlüsse mit PV-Bezug gelesen.

| Zugriffsart | Beschreibung | Quellen im Bestand |
|---|---|---:|
| `oparl` | standardisierte OParl-API (vollständig automatisierbar) | 103 |
| `sessionnet` | Somacos SessionNet, HTML-Abruf der Sitzungen | 15 |
| `auto` | System wird beim Lauf erkannt (OParl, SessionNet oder HTML) | 10 |
| `html` | Vorlagenübersicht per HTML | 1 |
| `portal` | Landesportale für Bauleitplanung (allgemeiner Crawler, ungetestet an echten Portalen) | 5 |

Das Landesportal bauleitplanung.brandenburg.de verbietet automatisierten Zugriff und wird nicht abgefragt. robots.txt wird überall beachtet, pro Server gilt 1 Sekunde Pause.

## Ablauf
1. `quellen_entdecken.py` findet je Gemeinde das RIS (Basis: `daten/gemeinden.csv`, 11.493 Gemeinden mit Koordinaten aus Wikidata) und schreibt `quellen_alle.csv`. Läuft sonntags über GitHub Actions, Budget 400 Gemeinden pro Lauf.
2. `pv_beschluesse.py` ruft pro Bundesland die Quellen ab, filtert nach PV-Stichwörtern, extrahiert Gemeinde, Fläche, Leistung und Entwickler (Regeln oder Gemini) und ergänzt Koordinaten. Der Bestand liegt in `daten/beschluesse_<land>.jsonl`, es wird nur Neues verarbeitet. Läuft montags.
3. Der Export fasst alle Länder zusammen: `ausgabe/PV_Beschluesse_Gesamt.xlsx` mit den Tabellen Projekte, Beschluesse, Quellen und Legende.
4. `portale_sonde.py` untersucht die Portale aus `portale.csv` (Workflow „Portale prüfen“) und schreibt `entdeckung/portale_bericht.md`. `pv_portale.py` ist der zugehörige Adapter (`typ = portal`).
5. `ris_betreiber.py` wertet die Abdeckung aus: Plattformen, Betreiber, Lücken je Land und Adapter-Ranking (`entdeckung/abdeckung.md`, `entdeckung/betreiber.csv`).



## Bekannte Einschränkungen
- Die HTML-Adapter (SessionNet, ALLRIS) funktionieren nicht bei jedem System gleich gut. Ergebnisse stichprobenartig prüfen.
- Das Datum ist das Vorlagendatum, nicht immer das Sitzungsdatum.
- Die Spalte `amt` in `daten/gemeinden.csv` ist nur bei 837 Gemeinden gefüllt. Die Zuordnung Gemeinde zu Amt, Verbandsgemeinde oder Samtgemeinde ist unvollständig.
- Sechs Betreiber auf ratsinfo-online.net sperren per robots.txt (u. a. Hohen Neuendorf, Rüdersdorf, Schorfheide, Zeuthen).
- Für ratsinfo-online.net und ALLRIS gibt es nur Teilunterstützung, für sitzung-online.de und sdnet keinen Adapter.

## Weitere Bausteine (Stand November 2026)
- `pv_homepage.py`: Bekanntmachungen auf der Homepage für Gemeinden ohne RIS (`quellen_homepage.csv`, `quellen_mastr.csv`).
- `pv_nachklaeren.py`: öffnet Detailseiten und PDFs, wenn der Beschlusstyp „Unklar“ ist.
- `mastr_abgleich.py`: vergleicht mit dem Marktstammdatenregister (Abdeckungs-Kontrolle, nicht Quelle).
- `pv_ihk.py` und `quellen_ihk.csv`: Planverfahrenslisten der IHKs (Träger öffentlicher Belange) als Sammelquelle über viele Gemeinden, auch in Thüringen, MV, Sachsen, Brandenburg.
- `pv_amtsblatt.py`, `amtsblatt_entdecken.py`: Amtsblatt-PDFs der Gemeinden ohne RIS, Textfenster um PV-Fundstellen.
- `verzeichnis_hessen.py`: Verzeichnis "Bebauungsplan im Verfahren" von bauleitplanung.hessen.de als Linkliste für den Homepage-Crawler.
- `stand_bericht.py`: erzeugt `STAND.md`, `daten/verlauf.csv`, `daten/ereignisse.csv` nach jedem Lauf.
- Die Läufe sind täglich geplant: Quellensuche 01:17 UTC, Register 06:43 UTC.


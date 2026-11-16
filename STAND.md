# Stand des PV-Beschlussregisters (16.11.2026)

Dieses Dokument beschreibt, was das Repo heute kann, wie viele Daten vorliegen und was für die bundesweite Abdeckung fehlt.

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

## Datenstand
- 225 Projekte und 415 Beschlüsse.
- Projekte je Land: Rheinland-Pfalz 88, Brandenburg 54, Nordrhein-Westfalen 39, Hessen 15, Baden-Württemberg 13, Niedersachsen 9, Sachsen-Anhalt 6.
- Mecklenburg-Vorpommern, Sachsen und Schleswig-Holstein liefern bisher 0 Treffer. Es ist offen, ob das echte Nullen sind oder fehlende Quellen. Thüringen, Bayern, Saarland und die Stadtstaaten haben keine Quellen.
- Status der Projekte: Ruhend 117, In Planung 53, Genehmigt 28, Abgelehnt 26.

## Abdeckung der Quellen
- Von 11.493 Gemeinden sind 553 geprüft, 10.940 noch nie.
- 128 Gemeinden mit RIS gefunden (90 Betreiber), 12 durch robots.txt gesperrt, 407 ohne erkanntes RIS.
- Nur Brandenburg ist vollständig geprüft, dort stehen 386 von 419 Gemeinden auf „kein RIS“. Das spricht für eine Erkennungslücke, vermutlich bei der Zuordnung zum RIS des Amts.
- Die Quellenliste deckt damit rund 1 % der Gemeinden ab. Der Engpass ist die Quellenliste, nicht der Scraper.

## Bekannte Einschränkungen
- Die HTML-Adapter (SessionNet, ALLRIS) funktionieren nicht bei jedem System gleich gut. Ergebnisse stichprobenartig prüfen.
- Das Datum ist das Vorlagendatum, nicht immer das Sitzungsdatum.
- Die Spalte `amt` in `daten/gemeinden.csv` ist nur bei 837 Gemeinden gefüllt. Die Zuordnung Gemeinde zu Amt, Verbandsgemeinde oder Samtgemeinde ist unvollständig.
- Sechs Betreiber auf ratsinfo-online.net sperren per robots.txt (u. a. Hohen Neuendorf, Rüdersdorf, Schorfheide, Zeuthen).
- Für ratsinfo-online.net und ALLRIS gibt es nur Teilunterstützung, für sitzung-online.de und sdnet keinen Adapter.

## Nächste Schritte
0. Workflow „Portale prüfen (Sonde)“ einmal starten und `entdeckung/portale_bericht.md` lesen. Portale als „JavaScript-App“ brauchen einen eigenen Adapter.
1. Workflow „Quellen entdecken“ mit `land = alle` und `budget = 0` laufen lassen, dann `python ris_betreiber.py` ausführen.
2. Erkennung in Brandenburg und die Amt-Zuordnung in `quellen_entdecken.py` verbessern.
3. Adapter für die Plattformen ergänzen, die laut Ranking die meisten Gemeinden abdecken.
4. Zweite Quellenart für Gemeinden ohne RIS prüfen (Amtsblätter, Bekanntmachungen, Landesportale). Nutzungsbedingungen je Portal vorher klären.
5. GitHub-Actions-Minuten prüfen (privates Repo), bei Bedarf Repo öffentlich machen oder eigenen Runner nutzen.
6. Langfristig eine Datenbank (SQLite oder Parquet) als Bestand, aus der die Excel nur noch exportiert wird.

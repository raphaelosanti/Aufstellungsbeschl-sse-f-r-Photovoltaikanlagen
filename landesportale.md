# Landesportale für Bauleitplanung – Recherche (16.11.2026)

Ziel: Prüfen, welche zentralen Landesportale als zweite Quellenart neben den Ratsinformationssystemen taugen.

**Wichtig zur Einordnung**
- Die Portale nach § 3 Abs. 2 und § 4a BauGB zeigen vor allem die **Veröffentlichung der Entwürfe (Auslegung)** und **in Kraft getretene Pläne**. Der **Aufstellungsbeschluss** steht dort meist nicht. Sie füllen also die späteren Verfahrensschritte auch für Gemeinden ohne RIS.
- **Nutzungsbedingungen, robots.txt und Schnittstellen habe ich bei keinem Portal selbst geprüft.** Die Spalte „Zugriff“ beruht auf Sekundärquellen (v. a. einer Übersicht von schwarzplan.eu, Stand 08/2026) und auf Landesdokumenten. Vor jedem Adapter muss das Portal selbst geprüft werden.
- Die Aufwandsangaben sind meine Einschätzung, keine Messung.

## Zwei Plattform-Familien, die mehrere Länder abdecken

| Familie | Länder | Bedeutung |
|---|---|---|
| **DiPlanung** (`<kürzel>.beteiligung.diplanung.de`) | Hamburg, Berlin, Bremen, Brandenburg, Bayern, Schleswig-Holstein; Niedersachsen führt es ein | Ein Adapter könnte bis zu 7 Länder bedienen |
| **Beteiligungsportal der Sachsen-Kooperation** | Sachsen, Sachsen-Anhalt, NRW (`beteiligung.nrw.de`), Hessen; Rheinland-Pfalz seit 2025; Thüringen in Gesprächen | Ein weiterer Adapter für mehrere Länder |

## Übersicht je Bundesland

| Land | Portal | Inhalt | Format / Zugriff (laut Sekundärquellen) | Plattform | Nutzungsbedingungen | Einschätzung |
|---|---|---|---|---|---|---|
| Baden-Württemberg | Geoportal Raumordnung BW; Offenlagen über Gemeinde-Links | ca. 31.500 Planobjekte, nur Geltungsbereiche | XPlanGML 6.0, Geodienste je Gemeinde (INSPIRE) | eigenes | nicht geprüft | Kein zentraler Verfahrens-Feed. Wenig Nutzen. |
| Bayern | Zentrales Landesportal Bauleitplanung, abgelöst durch DiPlan Portal (Nutzung ab 31.10.2026 verbindlich) | Verfahren und Pläne | altes Portal nur Bilddienst | DiPlanung | nicht geprüft | Lohnt sich über die DiPlanung-Familie. Größtes Land (2.205 Gemeinden). |
| Berlin | Senatsverwaltung, DiPlanBeteiligung | B-Plan-Verfahren | – | DiPlanung | nicht geprüft | Nur 1 Eintrag. Über DiPlanung. |
| Brandenburg | Planungsportal / `bb.beteiligung.diplanung.de`; Geoportal | 6.748 wirksame Pläne | – | DiPlanung | bauleitplanung.brandenburg.de verbietet laut eurem README automatisierten Zugriff | DiPlanung-Seite getrennt prüfen. |
| Bremen | Bauleitplan-Informationssystem Bremen | 1.484 Pläne (nur Stadt Bremen) | teils strukturiert | DiPlanung | nicht geprüft | Klein. |
| Hamburg | Geoportal Hamburg, bauleitplanung.hamburg.de | 3.046 Pläne | vollständig maschinenlesbar | DiPlanung | nicht geprüft | Klein, aber gute Datenlage. |
| Hessen | Bauleitplanung Hessen | verweist auf Gemeinden, nur Pläne seit 2017 | – | Beteiligungsportal-Kooperation | nicht geprüft | Kein Landesbestand. RIS bleibt wichtiger. |
| Mecklenburg-Vorpommern | Bau- und Planungsportal M-V | Bestand unvollständig | nur PDF; WFS für Geltungsbereiche | eigenes | nicht geprüft | Wichtig, weil bisher 0 Treffer und kaum RIS. Aufwand hoch. |
| Niedersachsen | UVP-Portal Niedersachsen | Verfahren und Bekanntmachungen, nicht die Pläne | – | wechselt zu DiPlanung | nicht geprüft | Gut für Verfahren. Wechsel beobachten. |
| Nordrhein-Westfalen | bauleitplanung.nrw / Bauportal.NRW | ca. 82.000 Pläne, freiwillige Meldung, unvollständig | OGC-API INSPIRE | Beteiligung NRW | nicht geprüft | Schon 55 RIS-Quellen. Portal als Ergänzung. |
| Rheinland-Pfalz | GeoPortal.rlp | 14.792 Pläne; Offenlagen nur während der Offenlage sichtbar | Planumringe und PDFs | Beteiligungsportal seit 2025 | nicht geprüft | Viele Ortsgemeinden. Regelmäßiges Abrufen nötig. |
| Saarland | GeoPortal Saarland | 35 von 52 Gemeinden mit eigenem Dienst | reiner Bilddienst | eigenes | nicht geprüft | Klein, schwer zu nutzen. |
| Sachsen | Zentrales Landesportal Raumordnung und Bauleitplanung (bauleitplanung.sachsen.de) | Offenlagen aller Städte und Gemeinden, mit Phasenkennzeichnung | RAPIS-Client | Beteiligungsportal Sachsen | nicht geprüft | Laut Land verpflichtend für alle Gemeinden. **Vielversprechend** (bisher 2 RIS-Quellen). |
| Sachsen-Anhalt | Sachsen-Anhalt-Viewer; `beteiligung.sachsen-anhalt.de` | 122 Gemeindeflächen, Verlinkung auf kommunale Portale | – | Beteiligungsportal | nicht geprüft | Bauleitplanung im Portal produktiv. Abdeckung offen. |
| Schleswig-Holstein | Digitaler Atlas Nord | 678 Pläne, 335 in Kraft | strukturiert, wo digital | DiPlanung (Wechsel) | nicht geprüft | Mittel. |
| Thüringen | ThüringenViewer, Planungsviewer | 3.381 Pläne in Kraft | Umrisse und PDFs | keine | nicht geprüft | Keine RIS-Quellen, Portal einzige Option. Aufwand hoch. |

## Empfehlung für die Reihenfolge
1. **DiPlanung-Adapter** prüfen, weil er mehrere Länder auf einmal abdecken könnte (Bayern, Brandenburg, Schleswig-Holstein, Niedersachsen, Stadtstaaten).
2. **Sachsen** (bauleitplanung.sachsen.de) wegen der gesetzlichen Pflicht für alle Gemeinden und bisher fast ohne Quellen.
3. **Beteiligungsportal-Familie** (Sachsen-Anhalt, NRW, Hessen, Rheinland-Pfalz), sobald die Technik geklärt ist.
4. Mecklenburg-Vorpommern und Thüringen nur, wenn die Portale Daten maschinell zugänglich machen. Sonst Amtsblätter.

## Offene Punkte vor dem Bau
- Für jedes Portal: Nutzungsbedingungen, robots.txt und vorhandene Schnittstelle (API, Feed, WFS) selbst prüfen. Bei Unklarheit den Betreiber fragen.
- Prüfen, ob ein Feed Gemeindename, Titel, Datum und Link liefert und ob PV-Pläne daran erkennbar sind (Titel, Stichwörter).
- Prüfen, wie lange abgeschlossene Verfahren im Portal sichtbar bleiben (in Rheinland-Pfalz nur während der Offenlage).

## Quellen
- schwarzplan.eu/en/german-zoning-plans/ (Vergleich der Landesportale, Stand 08/2026)
- digitale.planung.bayern.de (Einführung DiPlanung, Verbindlichkeit ab 31.10.2026)
- berlin.de und entwicklungsstadt.de (Mitglieder der DiPlanung-Kooperation)
- diplanung.niedersachsen.de, ihk.de/hannover (UVP-Portal Niedersachsen)
- landesentwicklung.sachsen.de und sk.sachsen.de (Landesportal und Beteiligungsportal Sachsen, Länderkooperation)
- presse.sachsen-anhalt.de, ozg.sachsen-anhalt.de (Beteiligungsportal Sachsen-Anhalt)
- bauportal.nrw, wetransform.to Fachforum XPlanung 2022 (Bauportal.NRW)
- geoportal.rlp.de, geoportal.saarland.de (kommunale Pläne in den Geoportalen)
- schleswig-holstein.de/bauleitplanung (Digitaler Atlas Nord)

# PV-Beschlussregister – MVP Brandenburg

Sammelt Ratsvorlagen zu PV-Bebauungsplänen aus Ratsinformationssystemen (RIS) und erstellt eine Excel-Datei mit den Tabellen **Projekte**, **Beschluesse**, **Quellen** und **Legende**. Läuft automatisch jeden Montag über GitHub Actions.

## Einrichtung auf GitHub (einmalig)
1. Neues **privates** Repository anlegen und den Inhalt dieses Ordners hochladen (inklusive des Ordners `.github`).
2. *Settings → Secrets and variables → Actions*
   - **Secret** `GEMINI_API_KEY` (optional): aktiviert die Gemini-Extraktion. Ohne Key läuft das Skript mit festen Suchregeln.
   - **Variable** `PV_KONTAKT` (empfohlen): z. B. eine E-Mail-Adresse. Sie wird bei Abrufen mitgeschickt, damit Betreiber der Systeme wissen, wer abfragt.
3. Tab *Actions* → „PV-Beschlussregister“ → **Run workflow** für den ersten Testlauf.

## Ergebnis abholen
Tab *Actions* → gewünschten Lauf öffnen → unten unter *Artifacts* die ZIP-Datei herunterladen. Darin liegen die Excel-Datei und die Rohdaten (JSON). Die Downloads bleiben 90 Tage verfügbar.

## Quellen erweitern
Neue Ämter als Zeile in `quellen_brandenburg.csv` eintragen (direkt auf GitHub über das Stift-Symbol):

| Spalte | Bedeutung |
|---|---|
| name | Amt, Gemeinde oder Stadt (Träger des RIS) |
| landkreis | für Auswertungen nach Kreis |
| typ | `auto` (empfohlen), `oparl` (OParl-System-URL), `sessionnet` (Somacos SessionNet, geht die Sitzungen durch) oder `html` (URL der Vorlagenübersicht) |
| url | Adresse des Ratsinformationssystems |

In Brandenburg stehen Gemeindebeschlüsse meist im RIS des **Amtes**, nicht des Landkreises. Liefert eine Quelle 0 Treffer, zeigt der Tab *Quellen* in der Excel den Grund.

## Lokal ausführen
```bash
pip install -r requirements.txt
python pv_beschluesse.py --seit 2022-01-01
# optional mit Gemini: GEMINI_API_KEY setzen und --llm gemini anhängen
```

## Hinweise
- Respektiert robots.txt, pausiert 1 Sekunde pro Server und speichert heruntergeladene Dokumente zwischen (`.cache_pv/`, bei GitHub automatisch zwischen den Läufen).
- Das Landesportal bauleitplanung.brandenburg.de verbietet automatisierten Zugriff und wird nicht abgefragt.
- Der HTML-Modus (SessionNet, ALLRIS) funktioniert nicht bei jedem System gleich gut. Ergebnisse stichprobenartig prüfen.
- Das Datum ist das Vorlagendatum, nicht immer das Sitzungsdatum.

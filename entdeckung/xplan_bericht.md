# XPlanung-Sonde (2026-11-25)

Prüft, ob die Dienste das Datum des Aufstellungsbeschlusses und PV-Bezug liefern. Gefüllte Felder und Treffer stammen aus einer Stichprobe von höchstens 50 Objekten je Typ.

## Bauleitpläne MV (Land) (Mecklenburg-Vorpommern)
- URL: https://www.geodaten-mv.de/dienste/bauleitplan_wfs
- Art: wfs; Geltungsbereiche der Bebauungs- und Flächennutzungspläne; Attribute unbekannt
- GetCapabilities ok, 6 Feature-Typen: sm:B_Plan_wfs, sm:BP_Bereiche_wfs, sm:F_Plan_wfs, sm:FP_Bereich_wfs, sm:SO_Plan_wfs, sm:SO_Bereich_wfs
- Typ **sm:B_Plan_wfs**: 11101 Objekte, Stichprobe 50; rechtsstand gefüllt 50× (z. B. 4000); PV-Bezug in Name/Beschreibung: 0

## Bauleitplaene MV basic (Mecklenburg-Vorpommern)
- URL: https://bauleitplaene-mv.de/dienste/basic
- Art: wfs; Typ B_Plan laut Hilfeseite
- GetCapabilities ok, 190 Feature-Typen: ms:B_Plan, ms:BP_Bereich, ms:F_Plan, ms:FP_Bereich, ms:SO_Plan, ms:SO_Bereich, ms:BP_Baugebietsteilflaeche, ms:BP_AbstandsMass_Flaechen, ms:BP_AbstandsMass_Linien, ms:BP_AbstandsMass_Punkte, ms:BP_BesondererNutzungszweckFlaeche, ms:BP_AnpflanzungBindungErhaltung_Flaechen …
- Typ **ms:B_Plan**: 11100 Objekte, Stichprobe 50; rechtsstand gefüllt 50× (z. B. 4000); name gefüllt 50× (z. B. Am Beiksoll); beschreibung gefüllt 8× (z. B. Plan-ID: 2049); PV-Bezug in Name/Beschreibung: 1
- Typ **ms:F_Plan**: 1760 Objekte, Stichprobe 50; rechtsstand gefüllt 50× (z. B. 4000); name gefüllt 35× (z. B. 00. Flächennutzungsplan); beschreibung gefüllt 2× (z. B. Teilpläne Stadt Warin und Groß Labenz (G); PV-Bezug in Name/Beschreibung: 0
- Typ **ms:SO_Plan**: 160 Objekte, Stichprobe 50; name gefüllt 49× (z. B. Erhaltungssatzung Garz/Rügen OT Groß Sch); beschreibung gefüllt 4× (z. B. Örtliche Bauvorschrift nach § 86 der LBa); PV-Bezug in Name/Beschreibung: 0

## Bauleitplaene MV XPlanung (Demo) (Mecklenburg-Vorpommern)
- URL: https://demo.bauleitplaene-mv.de/ows/xplanung
- Art: wfs; Demo-Dienst; XPlanung-Typen
- GetCapabilities ok, 41 Feature-Typen: ms:F-Pläne, ms:FP-Bereiche, ms:SO-Pläne, ms:SO-Bereiche, ms:B-Pläne, ms:BP-Bereiche, ms:bp_baugebietsteilflaeche_polygons, ms:bp_gruenflaeche_polygons, ms:bp_strassenverkehrsflaeche_polygons, ms:bp_schutzpflegeentwicklungsmassnahme_polygons, ms:bp_verentsorgung_polygons, ms:bp_verkehrsflaechebesondererzweckbestimmung_polygons …
- Typ **ms:F-Pläne**: 1880 Objekte, Stichprobe 50; rechtsstand gefüllt 50× (z. B. 4000); name gefüllt 50× (z. B. Flächennutzungsplan der Gemeinde Ostseeh); PV-Bezug in Name/Beschreibung: 0
- Typ **ms:FP-Bereiche**: 330 Objekte, Stichprobe 50; name gefüllt 50× (z. B. Geltungsbereich); PV-Bezug in Name/Beschreibung: 0
- Typ **ms:SO-Pläne**: 199 Objekte, Stichprobe 50; name gefüllt 49× (z. B. Werbeanlagensatzung); beschreibung gefüllt 12× (z. B. Örtliche Bauvorschrift nach § 86 der LBa); PV-Bezug in Name/Beschreibung: 0
- Typ **ms:SO-Bereiche**: 48 Objekte, Stichprobe 48; name gefüllt 48× (z. B. Geltungsbereich); PV-Bezug in Name/Beschreibung: 0

## Bauleitpläne in Aufstellung Stadt Bremen (Bremen)
- URL: https://hb.xplanboxcloud.dataport.de/xplansyn-wfs/services/xplansynwfspre
- Art: wfs; Pläne in Aufstellung (xplanbox)
- GetCapabilities ok, 0 Feature-Typen: 

## Kreis Kleve XPlanung inkraftgetreten (Nordrhein-Westfalen)
- URL: https://xplanservices.krzn.de/kleve/xplansyn-wfs/services/xplansynwfs
- Art: wfs; nur Kreis Kleve; Gegenstück für In Aufstellung besteht laut Katalog
- GetCapabilities nicht abrufbar: 503 Server Error: Service Temporarily Unavailable for url: https://xplanservices.krzn.de/kleve/xplansyn-wfs/services/xplansynwfs?SERVICE=WFS&REQUEST=GetCapabilities&VERSION=2.0.0

## Bauleitplanung NRW (INSPIRE) (Nordrhein-Westfalen)
- URL: https://ogc-api.nrw.de/inspire-lu-bplan/api?f=json
- Art: ogcapi; landesweit; INSPIRE-Modell; täglich aktualisiert
- OGC API ok (), Sammlungen: spatialplan
- Sammlung **spatialplan**: 73473 Objekte, Stichprobe 50, Felder: besch, gkz, kommune, levelOfSpatialPlan.code, levelOfSpatialPlan.href, levelOfSpatialPlan.title, nr, officialDocument, officialTitle, planTypeName.code, planTypeName.href, planTypeName.title, planart.code, planart.href, planart.title, processStepGeneral.code, processStepGeneral.href, processStepGeneral.title, sonsturl, texturl, validFrom; PV-Bezug in Stichprobe: 0


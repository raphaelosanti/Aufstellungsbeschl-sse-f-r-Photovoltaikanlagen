# Portal-Sonde (2026-11-16)

Prüft pro Portal robots.txt, Startseite, sitemap.xml, Feeds und API-Hinweise. Basis für die Entscheidung, ob der allgemeine Portal-Crawler reicht.

### Portal DiPlanung Brandenburg
- URL: https://bb.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 12585716 Zeichen HTML, 299746 Zeichen sichtbarer Text, 17 Skripte, 1932 Links auf dem Host, 968 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://bb.beteiligung.diplanung.de/#jumpNavigation, https://bb.beteiligung.diplanung.de/#jumpContent, https://bb.beteiligung.diplanung.de/#loginLink, https://bb.beteiligung.diplanung.de/, https://bb.beteiligung.diplanung.de/informationen
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Bayern
- URL: https://by.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 4126350 Zeichen HTML, 104863 Zeichen sichtbarer Text, 17 Skripte, 797 Links auf dem Host, 402 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://by.beteiligung.diplanung.de/#jumpNavigation, https://by.beteiligung.diplanung.de/#jumpContent, https://by.beteiligung.diplanung.de/#loginLink, https://by.beteiligung.diplanung.de/, https://by.beteiligung.diplanung.de/informationen
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal Sachsen Bauleitplanung
- URL: https://www.bauleitplanung.sachsen.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `<!DOCTYPE html> | <html lang="de"><head id="head"> |                  |                 <meta http-equiv="X-UA-Compatible" content="IE=edge" /> |                  |                 <title>Startseite | Raumordnungs- und Bauleitplanung Sachsen</title>`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 352812 Zeichen HTML, 6893 Zeichen sichtbarer Text, 57 Skripte, 41 Links auf dem Host, 22 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: vorhanden, 13 URLs, Beispiele: http://www.sachsen.de/, https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png, https://sgx.geodatenzentrum.de/web_public/Datenquellen_TopPlus_Open.pdf\
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://www.bauleitplanung.sachsen.de/portal/bplan/startseite, https://www.bauleitplanung.sachsen.de/portal/bplan/beteiligung/themen, https://www.bauleitplanung.sachsen.de/portal/bplan/informationen/hilfe, https://www.bauleitplanung.sachsen.de/portal/bplan/portale/uebersicht, https://www.bauleitplanung.sachsen.de/portal/sachsen/startseite
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal Beteiligung Sachsen-Anhalt
- URL: https://beteiligung.sachsen-anhalt.de/
- robots.txt: nicht erreichbar (ConnectTimeout) -> Portal vermutlich vom Runner aus nicht abrufbar
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: Fehler (ConnectTimeout: HTTPSConnectionPool(host='beteiligung.sachsen-anhalt.de', port=443): Max retries exceeded with url: / (Caused by Connect)

### Portal Beteiligung NRW
- URL: https://beteiligung.nrw.de/portal/hauptportal/startseite
- robots.txt: HTTP 404
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 742214 Zeichen HTML, 11338 Zeichen sichtbarer Text, 55 Skripte, 50 Links auf dem Host, 32 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://beteiligung.nrw.de/portal/hauptportal/startseite#sucheCollapse, https://beteiligung.nrw.de/portal/hauptportal/startseite#anmeldenCollapse, https://beteiligung.nrw.de/portal/hauptportal/profil/passwort-vergessen, https://beteiligung.nrw.de/portal/hauptportal/startseite, https://beteiligung.nrw.de/portal/hauptportal/profil/registrieren
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

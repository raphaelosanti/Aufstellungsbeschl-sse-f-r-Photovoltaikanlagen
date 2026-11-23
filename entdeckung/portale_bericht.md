# Portal-Sonde (2026-11-23)

Prüft pro Portal robots.txt, Startseite, sitemap.xml, Feeds und API-Hinweise. Basis für die Entscheidung, ob der allgemeine Portal-Crawler reicht.

### Portal DiPlanung Brandenburg
- URL: https://bb.beteiligung.diplanung.de/
- robots.txt: nicht erreichbar (ConnectTimeout) -> Portal vermutlich vom Runner aus nicht abrufbar
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: Fehler (ConnectTimeout: HTTPSConnectionPool(host='bb.beteiligung.diplanung.de', port=443): Max retries exceeded with url: / (Caused by ConnectTi)

### Portal DiPlanung Bayern
- URL: https://by.beteiligung.diplanung.de/
- robots.txt: nicht erreichbar (ConnectTimeout) -> Portal vermutlich vom Runner aus nicht abrufbar
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: Fehler (ConnectTimeout: HTTPSConnectionPool(host='by.beteiligung.diplanung.de', port=443): Max retries exceeded with url: / (Caused by ConnectTi)

### Portal Sachsen Bauleitplanung
- URL: https://www.bauleitplanung.sachsen.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `<!DOCTYPE html> | <html lang="de"><head id="head"> |                  |                 <meta http-equiv="X-UA-Compatible" content="IE=edge" /> |                  |                 <title>Startseite | Raumordnungs- und Bauleitplanung Sachsen</title>`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 356605 Zeichen HTML, 7894 Zeichen sichtbarer Text, 57 Skripte, 41 Links auf dem Host, 22 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: vorhanden, 13 URLs, Beispiele: http://www.sachsen.de/, https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png, https://sgx.geodatenzentrum.de/web_public/Datenquellen_TopPlus_Open.pdf\
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://www.bauleitplanung.sachsen.de/portal/bplan/startseite, https://www.bauleitplanung.sachsen.de/portal/bplan/beteiligung/themen, https://www.bauleitplanung.sachsen.de/portal/bplan/informationen/hilfe, https://www.bauleitplanung.sachsen.de/portal/bplan/portale/uebersicht, https://www.bauleitplanung.sachsen.de/portal/sachsen/startseite
- Probe liste https://www.bauleitplanung.sachsen.de/portal/bplan/beteiligung/themen: 356600 Zeichen HTML, 7894 Zeichen Text, Blätter-Hinweise: keine
- Probe detail https://www.bauleitplanung.sachsen.de/portal/wachau/beteiligung/themen/1070221: 356600 Zeichen HTML, 7894 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 9838 Zeichen Text (statisch: 7894)
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
- Startseite: 700852 Zeichen HTML, 10703 Zeichen sichtbarer Text, 55 Skripte, 50 Links auf dem Host, 32 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://beteiligung.nrw.de/portal/hauptportal/startseite#sucheCollapse, https://beteiligung.nrw.de/portal/hauptportal/startseite#anmeldenCollapse, https://beteiligung.nrw.de/portal/hauptportal/profil/passwort-vergessen, https://beteiligung.nrw.de/portal/hauptportal/startseite, https://beteiligung.nrw.de/portal/hauptportal/profil/registrieren
- Probe liste https://beteiligung.nrw.de/portal/hauptportal/beteiligung/themen?format=Bauleitplan: 202809 Zeichen HTML, 7882 Zeichen Text, Blätter-Hinweise: keine
- Probe detail https://beteiligung.nrw.de/portal/infozentrale/beteiligung/themen/1000520: 90654 Zeichen HTML, 5702 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 5692 Zeichen Text (statisch: 5702)
- Probe liste https://beteiligung.nrw.de/portal/hauptportal/beteiligung/themen?format=Bauleitplan: 202802 Zeichen HTML, 7882 Zeichen Text, Blätter-Hinweise: keine
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Schleswig-Holstein
- URL: https://sh.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 79823 Zeichen HTML, 2632 Zeichen sichtbarer Text, 17 Skripte, 38 Links auf dem Host, 22 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://sh.beteiligung.diplanung.de/#jumpNavigation, https://sh.beteiligung.diplanung.de/#jumpContent, https://sh.beteiligung.diplanung.de/#loginLink, https://sh.beteiligung.diplanung.de/, https://sh.beteiligung.diplanung.de/informationen
- Probe detail https://sh.beteiligung.diplanung.de/verfahren/klein-offenseth-sparrieshoop-fplan-12-aenderung/public/detail: 134365 Zeichen HTML, 2867 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 9904 Zeichen Text (statisch: 2867)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Hamburg
- URL: https://hh.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 118995 Zeichen HTML, 1854 Zeichen sichtbarer Text, 17 Skripte, 36 Links auf dem Host, 20 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://hh.beteiligung.diplanung.de/#jumpNavigation, https://hh.beteiligung.diplanung.de/#jumpContent, https://hh.beteiligung.diplanung.de/#loginLink, https://hh.beteiligung.diplanung.de/, https://hh.beteiligung.diplanung.de/informationen
- Probe detail https://hh.beteiligung.diplanung.de/verfahren/d6b26d36-d8ab-433c-8bad-890ba8d4a59f/public/detail: 152067 Zeichen HTML, 2725 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 11947 Zeichen Text (statisch: 2725)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Berlin
- URL: https://be.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 292062 Zeichen HTML, 7290 Zeichen sichtbarer Text, 17 Skripte, 66 Links auf dem Host, 35 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://be.beteiligung.diplanung.de/#jumpNavigation, https://be.beteiligung.diplanung.de/#jumpContent, https://be.beteiligung.diplanung.de/#loginLink, https://be.beteiligung.diplanung.de/, https://be.beteiligung.diplanung.de/informationen
- Probe detail https://be.beteiligung.diplanung.de/verfahren/xxi-23/public/detail: 262781 Zeichen HTML, 2705 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 13156 Zeichen Text (statisch: 2705)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Bremen
- URL: https://hb.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 38611 Zeichen HTML, 547 Zeichen sichtbarer Text, 17 Skripte, 22 Links auf dem Host, 13 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://hb.beteiligung.diplanung.de/#jumpNavigation, https://hb.beteiligung.diplanung.de/#jumpContent, https://hb.beteiligung.diplanung.de/#loginLink, https://hb.beteiligung.diplanung.de/, https://hb.beteiligung.diplanung.de/informationen
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Niedersachsen
- URL: https://ni.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 118960 Zeichen HTML, 3051 Zeichen sichtbarer Text, 17 Skripte, 45 Links auf dem Host, 26 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://ni.beteiligung.diplanung.de/#jumpNavigation, https://ni.beteiligung.diplanung.de/#jumpContent, https://ni.beteiligung.diplanung.de/#loginLink, https://ni.beteiligung.diplanung.de/, https://ni.beteiligung.diplanung.de/informationen
- Probe detail https://ni.beteiligung.diplanung.de/verfahren/bpl-293-oestlichstadtweg-fruehzeitigebeteiligung/public/detail: 65598 Zeichen HTML, 381 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 1919 Zeichen Text (statisch: 381)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

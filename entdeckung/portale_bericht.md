# Portal-Sonde (2026-11-23)

Prüft pro Portal robots.txt, Startseite, sitemap.xml, Feeds und API-Hinweise. Basis für die Entscheidung, ob der allgemeine Portal-Crawler reicht.

### Portal DiPlanung Brandenburg
- URL: https://bb.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 9381038 Zeichen HTML, 227590 Zeichen sichtbarer Text, 17 Skripte, 1454 Links auf dem Host, 729 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://bb.beteiligung.diplanung.de/#jumpNavigation, https://bb.beteiligung.diplanung.de/#jumpContent, https://bb.beteiligung.diplanung.de/#loginLink, https://bb.beteiligung.diplanung.de/, https://bb.beteiligung.diplanung.de/informationen
- Probe detail https://bb.beteiligung.diplanung.de/verfahren/d800ff37-bb12-40a2-933e-a8a1ff708ac5/public/detail: 107416 Zeichen HTML, 2796 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 9077 Zeichen Text (statisch: 2796)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Bayern
- URL: https://by.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 3267178 Zeichen HTML, 81778 Zeichen sichtbarer Text, 17 Skripte, 613 Links auf dem Host, 309 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://by.beteiligung.diplanung.de/#jumpNavigation, https://by.beteiligung.diplanung.de/#jumpContent, https://by.beteiligung.diplanung.de/#loginLink, https://by.beteiligung.diplanung.de/, https://by.beteiligung.diplanung.de/informationen
- Probe detail https://by.beteiligung.diplanung.de/verfahren/bc89af48-adac-41a3-9f15-9dbed0da6546/public/detail: 93816 Zeichen HTML, 2983 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 8766 Zeichen Text (statisch: 2983)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal Sachsen Bauleitplanung
- URL: https://www.bauleitplanung.sachsen.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `<!DOCTYPE html> | <html lang="de"><head id="head"> |                  |                 <meta http-equiv="X-UA-Compatible" content="IE=edge" /> |                  |                 <title>Startseite | Raumordnungs- und Bauleitplanung Sachsen</title>`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 356600 Zeichen HTML, 7894 Zeichen sichtbarer Text, 57 Skripte, 41 Links auf dem Host, 22 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: vorhanden, 13 URLs, Beispiele: http://www.sachsen.de/, https://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.png, https://sgx.geodatenzentrum.de/web_public/Datenquellen_TopPlus_Open.pdf\
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://www.bauleitplanung.sachsen.de/portal/bplan/startseite, https://www.bauleitplanung.sachsen.de/portal/bplan/beteiligung/themen, https://www.bauleitplanung.sachsen.de/portal/bplan/informationen/hilfe, https://www.bauleitplanung.sachsen.de/portal/bplan/portale/uebersicht, https://www.bauleitplanung.sachsen.de/portal/sachsen/startseite
- Probe liste https://www.bauleitplanung.sachsen.de/portal/bplan/beteiligung/themen: 356605 Zeichen HTML, 7894 Zeichen Text, Blätter-Hinweise: keine
  - Blättertest page=2: 0 neue Einträge (Seite 1 hat 358)
  - Blättertest seite=2: 0 neue Einträge (Seite 1 hat 358)
  - Blättertest p=2: 0 neue Einträge (Seite 1 hat 358)
  - Blättertest offset=10: 0 neue Einträge (Seite 1 hat 358)
  - Blättertest start=10: 0 neue Einträge (Seite 1 hat 358)
  - Liste im Browser: 0 Einträge
- Probe detail https://www.bauleitplanung.sachsen.de/portal/wachau/beteiligung/themen/1070221: 356595 Zeichen HTML, 7894 Zeichen Text, Blätter-Hinweise: keine
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
- Startseite: 699550 Zeichen HTML, 10703 Zeichen sichtbarer Text, 55 Skripte, 50 Links auf dem Host, 32 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: keine
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://beteiligung.nrw.de/portal/hauptportal/startseite#sucheCollapse, https://beteiligung.nrw.de/portal/hauptportal/startseite#anmeldenCollapse, https://beteiligung.nrw.de/portal/hauptportal/profil/passwort-vergessen, https://beteiligung.nrw.de/portal/hauptportal/startseite, https://beteiligung.nrw.de/portal/hauptportal/profil/registrieren
- Probe liste https://beteiligung.nrw.de/portal/hauptportal/beteiligung/themen?format=Bauleitplan: 203472 Zeichen HTML, 7882 Zeichen Text, Blätter-Hinweise: keine
  - Blättertest page=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest seite=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest p=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest offset=10: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest start=10: 0 neue Einträge (Seite 1 hat 61)
  - Liste im Browser: 0 Einträge
- Probe detail https://beteiligung.nrw.de/portal/infozentrale/beteiligung/themen/1000520: 90648 Zeichen HTML, 5702 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 5716 Zeichen Text (statisch: 5702)
- Probe liste https://beteiligung.nrw.de/portal/hauptportal/beteiligung/themen?format=Bauleitplan: 203472 Zeichen HTML, 7882 Zeichen Text, Blätter-Hinweise: keine
  - Blättertest page=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest seite=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest p=2: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest offset=10: 0 neue Einträge (Seite 1 hat 61)
  - Blättertest start=10: 0 neue Einträge (Seite 1 hat 61)
  - Liste im Browser: 0 Einträge
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Schleswig-Holstein
- URL: https://sh.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 80999 Zeichen HTML, 2632 Zeichen sichtbarer Text, 17 Skripte, 38 Links auf dem Host, 22 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://sh.beteiligung.diplanung.de/#jumpNavigation, https://sh.beteiligung.diplanung.de/#jumpContent, https://sh.beteiligung.diplanung.de/#loginLink, https://sh.beteiligung.diplanung.de/, https://sh.beteiligung.diplanung.de/informationen
- Probe detail https://sh.beteiligung.diplanung.de/verfahren/klein-offenseth-sparrieshoop-fplan-12-aenderung/public/detail: 134318 Zeichen HTML, 2867 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 9904 Zeichen Text (statisch: 2867)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Hamburg
- URL: https://hh.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 110690 Zeichen HTML, 1698 Zeichen sichtbarer Text, 17 Skripte, 34 Links auf dem Host, 19 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://hh.beteiligung.diplanung.de/#jumpNavigation, https://hh.beteiligung.diplanung.de/#jumpContent, https://hh.beteiligung.diplanung.de/#loginLink, https://hh.beteiligung.diplanung.de/, https://hh.beteiligung.diplanung.de/informationen
- Probe detail https://hh.beteiligung.diplanung.de/verfahren/d6b26d36-d8ab-433c-8bad-890ba8d4a59f/public/detail: 152004 Zeichen HTML, 2725 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 11947 Zeichen Text (statisch: 2725)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Berlin
- URL: https://be.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 101113 Zeichen HTML, 1769 Zeichen sichtbarer Text, 17 Skripte, 32 Links auf dem Host, 18 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://be.beteiligung.diplanung.de/#jumpNavigation, https://be.beteiligung.diplanung.de/#jumpContent, https://be.beteiligung.diplanung.de/#loginLink, https://be.beteiligung.diplanung.de/, https://be.beteiligung.diplanung.de/informationen
- Probe detail https://be.beteiligung.diplanung.de/verfahren/xxi-23/public/detail: 262688 Zeichen HTML, 2705 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 13156 Zeichen Text (statisch: 2705)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

### Portal DiPlanung Bremen
- URL: https://hb.beteiligung.diplanung.de/
- robots.txt: HTTP 200
- robots.txt Auszug: `# www.robotstxt.org/ | # www.google.com/support/webmasters/bin/answer.py?hl=en&answer=156449 |  | User-agent: *`
- Abruf für unseren User-Agent erlaubt: ja
- Startseite: 38733 Zeichen HTML, 547 Zeichen sichtbarer Text, 17 Skripte, 22 Links auf dem Host, 13 davon verfahrensähnlich
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
- Startseite: 94203 Zeichen HTML, 2368 Zeichen sichtbarer Text, 17 Skripte, 39 Links auf dem Host, 23 davon verfahrensähnlich
- Hinweise auf JavaScript-Framework: SPA-Container (app/root)
- sitemap.xml: nicht vorhanden oder nicht abrufbar
- Feeds (RSS/Atom/JSON): keine
- Hinweise auf API/JSON-Pfade im HTML: keine
- Beispiel-Links: https://ni.beteiligung.diplanung.de/#jumpNavigation, https://ni.beteiligung.diplanung.de/#jumpContent, https://ni.beteiligung.diplanung.de/#loginLink, https://ni.beteiligung.diplanung.de/, https://ni.beteiligung.diplanung.de/informationen
- Probe detail https://ni.beteiligung.diplanung.de/verfahren/fnp-aenderung-110-salzgitter/public/detail: 110954 Zeichen HTML, 2760 Zeichen Text, Blätter-Hinweise: keine
  - im Browser gerendert: 8967 Zeichen Text (statisch: 2760)
- **Ergebnis: serverseitig gerendert -> allgemeiner Crawler (typ=portal) sollte Treffer finden**

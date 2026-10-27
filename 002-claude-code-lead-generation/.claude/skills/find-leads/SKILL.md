---
name: find-leads
description: Build a contact list of local businesses for a niche and a US city from OpenStreetMap. Use when I say "/find-leads <niche> <city>" or ask for leads, prospects or a lead list.
---

# /find-leads <niche> <city, state>

Follow CLAUDE.md. Steps:

0. **Check Python:** `python3 -c "import ssl, sys; print(sys.version.split()[0], ssl.OPENSSL_VERSION)"`. The scripts need Python 3.10+ with OpenSSL. If it prints LibreSSL or a version below 3.10 (the Python that ships with macOS), the map server rejects the connection: offer to install a current Python (`brew install python@3.12` or python.org) and use that one.
1. **Pick the OSM tag** for the niche (examples: dentists `amenity=dentist`, hair salons `shop=hairdresser`, vets `amenity=veterinary`, lawyers `office=lawyer`, car repair `shop=car_repair`, plumbers `craft=plumber`, HVAC `craft=hvac`). If unsure, ask me.
2. **Count first:** `python3 find_osm.py --tag <key=value> --city "<city>" --count`. If there are fewer than 30 results, tell me and suggest a nearby city or another niche before going on.
3. **Find:** `python3 find_osm.py --tag <key=value> --city "<city>" --out leads/businesses.csv`
4. **Enrich:** `python3 enrich.py leads/businesses.csv leads/enriched.csv` (runs about 1 second per page, tell me how long it will take first).
5. **Validate and export:** `python3 validate.py leads/enriched.csv leads/<niche>-<city>.csv --master leads/master.csv`
6. **Report** the funnel: businesses → with website → with email → valid domain, plus how many have only a phone. Show 5 sample rows with emails partly masked.
7. Remind me of the CAN-SPAM checklist from CLAUDE.md before I import the file into my sending tool.

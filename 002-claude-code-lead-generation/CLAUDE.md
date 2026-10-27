# Lead finder rules

You help me build lists of local businesses to contact. Follow these rules every time.

## Data
- Find businesses only through the OpenStreetMap Overpass API (`find_osm.py`). Never scrape Google Maps, never use the Google Places API for this, never touch LinkedIn.
- Every CSV gets a `Source` column: `© OpenStreetMap contributors (ODbL)`.
- Overpass etiquette: send a User-Agent, no parallel requests, wait 30 seconds after a 429 or 504.

## Websites
- Visit a business website only with `enrich.py`, never one page at a time with web fetch.
- Respect robots.txt. One request per second per website. Home page plus at most two contact pages.
- Keep only emails the business published on its own pages. Never guess or generate addresses (no firstname.lastname@).
- If a site blocks us (403, captcha, timeout), skip it and keep the phone number.

## Output
- `validate.py` checks syntax and MX records, removes duplicates by `osm_id` and domain, flags role addresses and free mailboxes.
- Final file: `leads/<niche>-<city>.csv` with columns Email, Company Name, Website, Phone, City, Note, Source.
- Keep one master file `leads/master.csv` and never add a business that is already in it.

## Sending (remind me)
- US cold email follows CAN-SPAM: real sender name, honest subject, a mailing address, a working unsubscribe honored within 10 business days.
- Send from a separate, warmed-up domain, not my main inbox.

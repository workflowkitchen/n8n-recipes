# Claude Code Lead Generation: free local business leads

One command in Claude Code: `/find-leads dentists Austin TX`. It finds local businesses on OpenStreetMap, reads the emails and phone numbers they publish on their own websites, checks every domain for a mail server and saves a CSV ready for Google Sheets or Instantly.

📺 Video walkthrough: [Claude Code Lead Generation: Free Local Leads](https://www.youtube.com/@workflowkitchen)

$0 for data. No Google Maps scraping, no Places API, no LinkedIn, no Apollo.

## What's inside

| File | Job |
|---|---|
| `CLAUDE.md` | The rules Claude follows in every session: OpenStreetMap only, robots.txt, 1 request per second, never guess emails, credit the source |
| `.claude/skills/find-leads/SKILL.md` | The `/find-leads <niche> <city>` command |
| `find_osm.py` | Lists businesses with one OpenStreetMap tag in a US city (Overpass API) |
| `enrich.py` | Reads each business website (home + contact pages) and keeps emails and phones the business published itself; notes online booking |
| `validate.py` | Email syntax + mail-server (MX) check, dedupe against `leads/master.csv`, flags `info@`-style and Gmail addresses, writes the final CSV |

The scripts use only the Python standard library. Nothing to install except Claude Code.

## Setup (about 20 minutes)

**You need:** Claude Code on a paid plan (the free plan doesn't include it; Pro is $20/month) and Python 3.10 or newer.

1. **Install Claude Code.** Mac/Linux: `curl -fsSL https://claude.ai/install.sh | bash`. Windows and the desktop app: [code.claude.com/docs/en/quickstart](https://code.claude.com/docs/en/quickstart).
2. **Copy this folder** (`002-claude-code-lead-generation`) to your computer and rename it `leads`.
3. **Check Python:** `python3 -c "import ssl, sys; print(sys.version.split()[0], ssl.OPENSSL_VERSION)"`. If you see a version below 3.10 or the word LibreSSL (the Python that ships with macOS), install a current one: `brew install python@3.12` or [python.org](https://www.python.org/downloads/).
4. `cd leads` and run `claude`.
5. Type `/find-leads dentists Austin TX`. Claude counts the businesses first, then asks before each script runs.

Output: `leads/<niche>-<city>.csv` with the columns `Email, Company Name, Website, Phone, City, Note, Source`.

## What to expect (our test, Austin TX, October 2026)

| Niche | Businesses | With a website | Emails (working domain) | With a phone |
|---|---|---|---|---|
| Dentists | 120 | 55 | 28 | 57 |
| Hair salons | 170 | 69 | 22 | 85 |
| HVAC | 12 | 12 | 4 | 12 |
| Plumbers | 3 | 3 | 2 | 3 |
| **Total** | **305** | **139 (46%)** | **56 (18%)** | **157 (51%)** |

Rule of thumb: 100 local businesses → about 18 emails and 50 phone numbers. 23 websites blocked the script.

Shops with a storefront (dentists, salons, vets) are mapped well. Mobile trades (plumbers, HVAC) are thin on the map: check the count first, it takes ten seconds.

## Not working? Quick fixes

| Problem | Fix |
|---|---|
| `[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE]` when finding businesses | Your Python is too old (macOS built-in). Install Python 3.12, step 3 |
| `Overpass busy (429)` | The free map server is busy. The script waits 30 s and retries; run one city at a time |
| `0 places tagged` | Check the city spelling and state (`"Austin, TX"`). Some niches use another tag, ask Claude to look it up |
| Lots of `blocked (403)` | Some sites block scripts. Don't fight it: keep the phone number and call |
| Few emails | Normal. Many small businesses only list a phone or a contact form |

## Sending the emails (US)

Cold email to businesses is legal in the US under CAN-SPAM if you: use your real name, write an honest subject line, include a mailing address (a PO box works), and honor unsubscribes within 10 business days. Fines go up to $53,088 per email. Send from a separate, warmed-up domain, not your main inbox.

---
Map data © OpenStreetMap contributors, available under the [Open Database License](https://www.openstreetmap.org/copyright). Every CSV keeps a `Source` column with this credit.

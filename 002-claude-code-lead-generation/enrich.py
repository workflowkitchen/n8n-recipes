#!/usr/bin/env python3
"""enrich.py leads/businesses.csv leads/enriched.csv
For every business with a website: reads the home page and up to two contact pages,
keeps emails and phone numbers the business published itself, and notes online booking.
Respects robots.txt, waits 1 s between requests to the same site, never guesses addresses."""
import csv, html, re, socket, sys, time, urllib.parse, urllib.request, urllib.robotparser

UA = "WorkflowKitchen-find-leads/1.0 (+https://github.com/workflowkitchen/n8n-recipes)"
CONTACT_PATHS = ("/contact", "/contact-us")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JUNK = re.compile(r"\.(png|jpe?g|gif|webp|svg)$|@(example|sentry|wixpress|domain)\.|^(name|email|your)@", re.I)
socket.setdefaulttimeout(10)            # robots.txt reads have no timeout of their own
BOOKING = ("book online", "book now", "book an appointment", "schedule online", "request an appointment", "online booking")


def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read(600_000).decode("utf-8", "ignore")


def allowed(base):
    rp = urllib.robotparser.RobotFileParser(urllib.parse.urljoin(base, "/robots.txt"))
    try:
        rp.read()
    except Exception:
        return lambda url: True          # no robots.txt reachable = no rules published
    return lambda url: rp.can_fetch(UA, url)


def emails_in(page):
    found = {html.unescape(m).split("?")[0] for m in re.findall(r'mailto:([^"\'>\s]+)', page, re.I)}
    found |= set(EMAIL.findall(html.unescape(re.sub(r"<[^>]+>", " ", page))))
    return {e.strip(".").lower() for e in found if not JUNK.search(e)}


def enrich(row):
    site = row["website"].strip()
    if not site:
        return {"status": "no website"}
    if not site.startswith("http"):
        site = "https://" + site
    try:
        final, home = fetch(site)
    except Exception as e:
        return {"status": f"blocked ({getattr(e, 'code', type(e).__name__)})"}
    base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(final))
    can = allowed(base)
    pages = [home]
    for path in CONTACT_PATHS:
        url = base + path
        if not can(url):
            continue
        time.sleep(1)
        try:
            pages.append(fetch(url)[1])
        except Exception:
            pass
    text = " ".join(pages)
    domain = urllib.parse.urlsplit(final).netloc.lower().removeprefix("www.")
    emails = sorted(emails_in(text), key=lambda e: (not e.endswith("@" + domain), e))
    tels = re.findall(r'tel:([+\d\-\s().]{7,20})', text)
    note = "online booking" if any(b in text.lower() for b in BOOKING) else "no online booking found"
    return {"status": "ok" if emails else "no email on site", "email": emails[0] if emails else "",
            "phone_site": tels[0].strip() if tels else "", "domain": domain, "note": note}


def main():
    src, dst = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    sites = sum(1 for r in rows if r["website"])
    print(f"checking {sites} websites (~{sites * 3} s)…", flush=True)
    out = []
    for i, r in enumerate(rows, 1):
        r = {**r, **{"status": "", "email": "", "phone_site": "", "domain": "", "note": ""}, **enrich(r)}
        if r["website"]:
            print(f"[{i}/{len(rows)}] {r['name'][:40]:40} {r['status']}", flush=True)
            time.sleep(1)
        out.append(r)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    n_mail = sum(1 for r in out if r["email"])
    print(f"{len(out)} businesses → {sites} websites → {n_mail} emails → saved {dst}")


if __name__ == "__main__":
    main()

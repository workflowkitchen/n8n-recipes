#!/usr/bin/env python3
"""validate.py leads/enriched.csv leads/dentists-austin.csv [--master leads/master.csv]
Checks email syntax and MX records (free DNS lookup), removes duplicates by osm_id and domain,
flags role addresses and free mailboxes, and writes a CSV ready for Instantly or Google Sheets."""
import argparse, csv, json, os, re, urllib.parse, urllib.request

SYNTAX = re.compile(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$")
ROLE = {"info", "contact", "office", "hello", "admin", "frontdesk", "front.desk", "appointments", "reception", "support", "team"}
FREE = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "msn.com", "live.com"}
FIELDS = ["Email", "Company Name", "Website", "Phone", "City", "Note", "Source"]
_mx = {}


def has_mx(domain):
    """MX lookup over DNS-over-HTTPS: stdlib only, works on Mac/Windows/Linux, no `dig` needed."""
    if domain not in _mx:
        url = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": domain, "type": "MX"})
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                _mx[domain] = any(a.get("type") == 15 for a in json.load(r).get("Answer", []))
        except Exception:  # lookup failed = we can't confirm a mail server
            _mx[domain] = False
    return _mx[domain]


def clean_url(u):
    p = urllib.parse.urlsplit(u if u.startswith("http") else "https://" + u)
    return f"{p.scheme}://{p.netloc}{p.path}".rstrip("/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--master", default="leads/master.csv")
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.src, encoding="utf-8")))
    seen_ids, seen_domains = set(), set()
    if os.path.exists(a.master):
        for m in csv.DictReader(open(a.master, encoding="utf-8")):
            seen_ids.add(m.get("osm_id", ""))
            seen_domains.add(m.get("domain", ""))
    out, master_new, stats = [], [], dict(emails=0, valid=0, role=0, free=0, dupes=0, phone_only=0)
    for r in rows:
        if r["osm_id"] in seen_ids or (r.get("domain") and r["domain"] in seen_domains):
            stats["dupes"] += 1
            continue
        seen_ids.add(r["osm_id"])
        if r.get("domain"):
            seen_domains.add(r["domain"])
        email = (r.get("email") or r.get("email_osm") or "").lower()
        phone = r.get("phone") or r.get("phone_site") or ""
        master_new.append({"osm_id": r["osm_id"], "domain": r.get("domain", "")})
        if not email:
            stats["phone_only"] += bool(phone)
            continue
        stats["emails"] += 1
        local, _, dom = email.partition("@")
        if not SYNTAX.match(email) or not has_mx(dom):
            continue
        stats["valid"] += 1
        flags = []
        if local in ROLE:
            flags.append("role address")
            stats["role"] += 1
        if dom in FREE:
            flags.append("free mailbox")
            stats["free"] += 1
        out.append({"Email": email, "Company Name": r["name"], "Website": clean_url(r["website"]) if r["website"] else "",
                    "Phone": phone, "City": r["city"], "Note": "; ".join([r.get("note", "")] + flags).strip("; "),
                    "Source": "© OpenStreetMap contributors (ODbL)"})
    os.makedirs(os.path.dirname(a.dst) or ".", exist_ok=True)
    with open(a.dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    new_master = not os.path.exists(a.master)
    with open(a.master, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["osm_id", "domain"])
        if new_master:
            w.writeheader()
        w.writerows(master_new)
    print(f"{len(rows)} businesses → {stats['emails']} emails → {stats['valid']} valid domains "
          f"({stats['role']} role, {stats['free']} free mailbox) · {stats['phone_only']} phone only · "
          f"{stats['dupes']} duplicates skipped → saved {a.dst}")


if __name__ == "__main__":
    main()

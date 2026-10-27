#!/usr/bin/env python3
"""find_osm.py --tag amenity=dentist --city "Austin, TX" [--count] [--out leads/businesses.csv]
Lists businesses with one OpenStreetMap tag inside a US city via the Overpass API.
Map data © OpenStreetMap contributors, ODbL. Standard library only."""
import argparse, csv, json, os, sys, time, urllib.parse, urllib.request

OVERPASS = "https://overpass-api.de/api/interpreter"
UA = "WorkflowKitchen-find-leads/1.0 (+https://github.com/workflowkitchen/n8n-recipes)"
STATES = dict(AL="Alabama", AK="Alaska", AZ="Arizona", AR="Arkansas", CA="California", CO="Colorado", CT="Connecticut",
              DE="Delaware", FL="Florida", GA="Georgia", HI="Hawaii", ID="Idaho", IL="Illinois", IN="Indiana", IA="Iowa",
              KS="Kansas", KY="Kentucky", LA="Louisiana", ME="Maine", MD="Maryland", MA="Massachusetts", MI="Michigan",
              MN="Minnesota", MS="Mississippi", MO="Missouri", MT="Montana", NE="Nebraska", NV="Nevada", NH="New Hampshire",
              NJ="New Jersey", NM="New Mexico", NY="New York", NC="North Carolina", ND="North Dakota", OH="Ohio",
              OK="Oklahoma", OR="Oregon", PA="Pennsylvania", RI="Rhode Island", SC="South Carolina", SD="South Dakota",
              TN="Tennessee", TX="Texas", UT="Utah", VT="Vermont", VA="Virginia", WA="Washington", WV="West Virginia",
              WI="Wisconsin", WY="Wyoming", DC="District of Columbia")


def query(tag, city, state, count):
    key, value = tag.split("=", 1)
    out = "out count;" if count else "out tags center;"
    return f"""[out:json][timeout:90];
area["name"="{state}"]["boundary"="administrative"]["admin_level"="4"]->.st;
area["name"="{city}"]["boundary"="administrative"]["admin_level"="8"](area.st)->.a;
nwr["{key}"="{value}"](area.a);
{out}"""


def overpass(q):
    data = urllib.parse.urlencode({"data": q}).encode()
    for attempt in range(3):
        req = urllib.request.Request(OVERPASS, data=data, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 502, 503, 504) and attempt < 2:
                print(f"Overpass busy ({e.code}), waiting 30 s…", file=sys.stderr)
                time.sleep(30)
                continue
            raise


def address(t):
    street = " ".join(x for x in (t.get("addr:housenumber"), t.get("addr:street")) if x)
    return ", ".join(x for x in (street, t.get("addr:city"), t.get("addr:postcode")) if x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--city", required=True, help='"Austin, TX"')
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--out", default="leads/businesses.csv")
    a = ap.parse_args()
    city, _, st = (p.strip() for p in a.city.partition(","))
    state = STATES.get(st.upper(), st)
    res = overpass(query(a.tag, city, state, a.count))
    if a.count:
        n = int(res["elements"][0]["tags"]["total"]) if res["elements"] else 0
        print(f"{n} places tagged {a.tag} in {city}, {st}")
        return
    rows = []
    for el in res["elements"]:
        t = el.get("tags", {})
        if not t.get("name"):
            continue
        rows.append({"osm_id": f"{el['type']}/{el['id']}", "name": t["name"], "address": address(t),
                     "phone": t.get("phone") or t.get("contact:phone", ""),
                     "website": t.get("website") or t.get("contact:website", ""),
                     "email_osm": t.get("email") or t.get("contact:email", ""),
                     "city": f"{city}, {st}", "tag": a.tag})
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["osm_id"])
        w.writeheader()
        w.writerows(rows)
    with_site = sum(1 for r in rows if r["website"])
    print(f"{len(rows)} businesses → {with_site} with a website → saved {a.out}")


if __name__ == "__main__":
    main()

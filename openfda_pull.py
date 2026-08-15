"""
openfda_pull.py
----------------
Extends the "Cardiovascular Medical Device Recalls" dashboard with data that
couldn't be pulled during the build (the build environment hit openFDA's
shared-IP rate limit). Run this on a normal internet connection.

What it pulls, beyond what's already in the dashboard:
  1. Yearly recall trend (2015-present)
  2. Top 10 recalling firms
  3. Recall status breakdown (Ongoing / Terminated / Completed)
  4. MAUDE adverse-event counts by event type, for the same device specialty

Requires: pip install requests
Docs: https://open.fda.gov/apis/device/recall/  and  /device/event/

Usage:
    python openfda_pull.py

Output:
    Prints a `DATA_EXTENSION` JS object to stdout (and saves to
    openfda_extension.json) that you can merge into the dashboard's
    <script> block to power additional charts.
"""

import json
import time
import requests

BASE_RECALL = "https://api.fda.gov/device/recall.json"
BASE_EVENT = "https://api.fda.gov/device/event.json"
SPECIALTY = 'openfda.medical_specialty_description:"Cardiovascular"'


def get(url, params, retries=3, backoff=5):
    """GET with basic retry/backoff for openFDA's rate limiting (429s)."""
    for attempt in range(retries):
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 429:
            wait = backoff * (attempt + 1)
            print(f"  Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Failed after {retries} retries: {url}")


def yearly_recall_trend(start_year=2015, end_year=2026):
    """One lightweight call per year: just reads meta.results.total."""
    print("Pulling yearly recall trend...")
    out = []
    for year in range(start_year, end_year + 1):
        params = {
            "search": f'{SPECIALTY}+AND+event_date_initiated:[{year}0101+TO+{year}1231]',
            "limit": 1,
        }
        try:
            data = get(BASE_RECALL, params)
            total = data.get("meta", {}).get("results", {}).get("total", 0)
        except requests.HTTPError:
            total = 0  # openFDA returns 404 when a search matches zero records
        out.append({"year": year, "count": total})
        print(f"  {year}: {total}")
        time.sleep(1)  # be polite to the shared rate limit
    return out


def top_firms(limit=10):
    print("Pulling top recalling firms...")
    params = {"search": SPECIALTY, "count": "recalling_firm.exact", "limit": limit}
    data = get(BASE_RECALL, params)
    return data["results"]


def recall_status_breakdown():
    print("Pulling recall status breakdown...")
    params = {"search": SPECIALTY, "count": "recall_status.exact"}
    data = get(BASE_RECALL, params)
    return data["results"]


def adverse_event_types(limit=10):
    print("Pulling MAUDE adverse event types...")
    params = {"search": SPECIALTY, "count": "event_type.exact", "limit": limit}
    data = get(BASE_EVENT, params)
    return data["results"]


def main():
    extension = {
        "yearly_trend": yearly_recall_trend(),
        "top_firms": top_firms(),
        "recall_status": recall_status_breakdown(),
        "adverse_event_types": adverse_event_types(),
    }

    with open("openfda_extension.json", "w") as f:
        json.dump(extension, f, indent=2)

    print("\nSaved to openfda_extension.json")
    print("\nPaste this into the dashboard's <script> block as a new const,")
    print("then add Chart.js charts that read from it (see build-dashboard")
    print("patterns already used in the HTML file for line/bar/doughnut charts).\n")
    print(json.dumps(extension, indent=2)[:1000] + "\n...")


if __name__ == "__main__":
    main()

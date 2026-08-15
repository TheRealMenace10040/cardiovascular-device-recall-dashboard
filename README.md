# Cardiovascular Medical Device Recalls — Portfolio Case Study

## Problem
Recruiters see dozens of near-identical portfolio projects built on the same Kaggle datasets (Titanic, superstore sales). I wanted a project that used **real, public, industry-relevant data** and applied the way of thinking I use daily as a Quality Microbiology Lab Technician — root-cause categorization, risk classification, CAPA-style trend analysis — to a dataset a medtech employer would actually recognize.

## Data & Approach
- **Source:** [openFDA Device Recall API](https://open.fda.gov/apis/device/recall/) — the FDA's public enforcement report data, filtered to the Cardiovascular device specialty.
- **Method:** Queried the API for (1) the top 15 reported root causes of recalls and (2) the FDA risk classification (Class I/II/III) of recalled devices — both pulled live on Aug 14, 2026.
- **Analysis layer:** Recoded the 15 raw FDA root-cause labels into four analyst-defined groups — Design, Manufacturing/Process, Human/Investigation, Other/Unclassified — the same kind of categorization work used when triaging CAPA root causes in a quality system.

## Key Findings
- **6,815** cardiovascular device recalls on record; **92.3%** are Class II (moderate risk), consistent with cardiovascular recalls skewing toward catheters, monitors, and stents rather than the smaller pool of Class III implantables.
- After recoding, **Manufacturing/Process issues (37.3%)** are the single largest driver of recalls — edging out **Design issues (32.8%)**. That cuts against the common assumption that recalls are mostly design flaws.
- **12.2%** of categorized recalls were still "Under Investigation by firm" at time of report — a leading indicator worth tracking separately since root cause isn't finalized yet.

## Recommendation (framed as I would for a quality team)
If this were a live internal dataset, the process-control skew would point toward auditing incoming-material inspection and in-process controls before investing further in design-verification activities — the opposite of where teams often default their CAPA budget.

## Engineering note (honesty about the build)
This dashboard was built inside a sandboxed cloud environment with restricted network access. I got two solid live pulls before hitting openFDA's shared-IP rate limit, so the dashboard ships with those two real breakdowns plus the derived recode. I included `openfda_pull.py`, a working, retry-aware script that pulls the remaining cuts (yearly trend, top recalling firms, MAUDE adverse-event types) — meant to be run on a normal connection and merged into the dashboard. I'd rather ship something honest about its scope than backfill it with fabricated numbers.

## Tools used
openFDA REST API, Python (requests, retry/backoff logic), HTML/CSS/JS, Chart.js.

## Files
- `cardiovascular_device_recall_dashboard.html` — the dashboard (open directly in a browser, no install needed)
- `openfda_pull.py` — extension script for yearly trend / top firms / adverse events
- This README as the case-study writeup for a portfolio site or GitHub repo

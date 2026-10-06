# Cardiovascular Medical Device Recalls

**Live dashboard:** https://therealmenace10040.github.io/cardiovascular-device-recall-dashboard/

## Why this project
Most portfolio projects reuse the same Kaggle datasets. I wanted public data a medtech employer would recognize, analyzed the way I already work as a Quality Microbiology Lab Technician: sorting root causes, looking at risk class, and asking what a CAPA program should do next.

## Data and approach
- **Source:** the [openFDA Device Recall API](https://open.fda.gov/apis/device/recall/), filtered to the Cardiovascular device specialty.
- **Queries:** the 15 most common reported root causes, and the FDA risk class (I, II, III) of recalled devices. Both pulled on Aug 14, 2026.
- **Analysis:** I grouped the 15 FDA root-cause labels into four categories (Design, Manufacturing / process, Human / under investigation, Other), the same kind of grouping used when triaging CAPA root causes.

## Findings
- There are **6,815** cardiovascular device recalls on record. **92.3%** are Class II (moderate risk), which fits a specialty dominated by catheters, monitors and stents rather than Class III implantables.
- **Manufacturing and process issues (37.3%)** are the largest driver, ahead of **design issues (32.8%)**. Most people assume the opposite.
- **12.2%** are human error or were still under investigation by the firm when reported. That group is worth tracking separately because the final root cause isn't settled yet.

## Recommendation
If this were internal data, the process-control share would point a quality team toward incoming material inspection and in-process controls before spending more on design verification.

## Limits
The API's rate limit stopped the pull after the two breakdowns above, so there is no yearly trend or top-manufacturer view yet. `openfda_pull.py` pulls both, plus MAUDE adverse-event types, with retry and backoff. I left those views out rather than fill them with made-up numbers.

## Files
- `index.html`: the dashboard. Opens in any browser with nothing to install.
- `openfda_pull.py`: script for the yearly trend, top recalling firms and adverse-event types.

## Tools
openFDA REST API, Python (requests, retry/backoff), HTML/CSS/JavaScript, Chart.js.

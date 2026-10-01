# Clean-clone reproduction from committed public data

Use Python 3.10+ from the repository root. These checks use the published pseudonymous sample; the private source workbook is not required.

The usage input is a frozen Excel-generated simulation: random measurements, ten chosen OLT IDs and five chosen dates. Reproducing metrics from those CSVs is possible; recreating original random generation is not established because formulas/seed were not supplied. See [simulation contract](simulation_contract.md).

The author supplied the original customer workbook privately on 1 October 2026. Its date reconciliation is documented in [source_workbook_review.md](source_workbook_review.md). To repeat that additional private check, use `python scripts/reconcile_source_workbook.py --source /private/path/original.xlsx`; the original workbook is intentionally absent from Git. This is separate from the public checks below.

The dataset is **already in the project**: `data/clean/` contains 1,280 service-account rows, 6,400 usage rows, 6,400 derived account-day rows, 50 OLT-day rows, 12 OLT definitions, four plans and 805 generated complaint events. `data/sample/` contains smaller 100-account and 500-account-day extracts for inspection; it does not extend the five-day history. The seven CSVs under `dashboard/OLT_Professional_Project/data/` are Power BI input copies of the clean tables. Use `data/clean/` for the read-only audit so the Power BI project stays untouched until approval.

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_public.py
python scripts/validate_sql.py
```

The audit prints aggregate JSON. To intentionally refresh its tracked evidence file, run `python scripts/audit_public.py --output docs/data_readiness_receipt.json` and review the diff. Expected current snapshot: 1,280 account keys, 6,400 account-days over 2026-08-01 through 2026-08-05, no complete risk windows, 1,135 assigned/logged OLT mismatches, and logged coverage of 10/12 OLTs. The SQL script runs eight queries and checks the same key risk/coverage facts.

`python scripts/03_build_metrics.py` rebuilds clean metrics **and** the Power BI project's copied CSV inputs. It is intentionally not part of the read-only check list: run it only when changing source data or metric code and review every resulting CSV diff. The current Power BI project requires setting its `DataRoot` parameter to the checkout's data folder, refreshing in Desktop and reconciling DAX. Those native steps are pending, not established by the Python tests.

`scripts/01_clean_data.py` needs an ignored private-source extract and is not reproducible from a public clone. `scripts/02_generate_complaints.py` creates synthetic complaints and must never be described as observed support activity. The Python overview image is not a Power BI screenshot. Never commit raw customer identifiers, contact details, credentials or an unreviewed PBIX with embedded data.

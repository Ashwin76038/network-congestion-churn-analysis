# Clean-clone reproduction

No private source, portal credentials or generated extra days are needed.

```bash
python -m pip install -r requirements.txt
python scripts/03_build_metrics.py
python -m unittest discover -s tests -v
python scripts/validate_sql.py
python scripts/audit_public.py
python scripts/build_dax_validation.py
python scripts/configure_powerbi.py
```

The metric rebuild updates derived clean tables, sample metrics and report copies. Frozen input dates remain 1–5 August 2026; no additional observations are created. Expect 15 tests passed, eight supplementary SQLite queries passed, 1,280 accounts, 6,400 account-days, 1,135 assignment conflicts, zero complete windows and unavailable full risk. The DAX generator prepares 133 expectations but does not execute Desktop.

Open `dashboard/OLT_Professional_Project/OLT_Churn_Network_Risk_Professional.pbip` in Power BI Desktop. The configure script sets the local DataRoot parameter. Refresh all data and apply pending changes. Run `docs/validate_measures.dax` in DAX query view: Checks=133, Passed=133, empty Failures. Inspect all three pages and repeat the logged OLT 1/reset check described in `powerbi_validation.md`. Save; never add `.pbi` caches to Git.

For native MySQL use `sql_engine_notes.md`. The optional private-source cleaner is not part of this public pipeline. Private source comparison requires the original confidential workbook and is distributed only as aggregate receipts. Original Excel random generation cannot be exactly reproduced without its formulas and frozen random state.

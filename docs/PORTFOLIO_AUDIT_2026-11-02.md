# Portfolio verification

Status: existing simulation preserved; automated regression workflow added.

The fresh public checkout passed 15 Python tests and executed eight portable
SQLite queries on 29 October 2026. The aggregate audit reconciled 6,400
account-days, 1,280 account labels, 805 simulated complaints, 1,135 conflicting
assigned/logged labels, and zero complete 14-day windows. No observed churn
or validated churn predictor is claimed. See `audit_2026-10-29.json`.

The added GitHub workflow rebuilds metrics, runs tests and SQL checks, audits
the public tables, and generates the native DAX validation query. Generation
is not DAX execution. Existing Power BI/MySQL receipts retain their original
dates; neither native engine was rerun by this audit. Remote CI results must
be checked after publication.

No new simulated observations were appended to hide the five-day limitation.
Historical filenames include binary report candidates; current sanitization
does not establish that old cached data is safe. Full historical content
review and any owner-approved history remediation remain separate work.

Readiness: 7/10 for analytical methods and data-quality demonstration. Window
completeness, units and separate OLT roles are tested; real outcomes, stable
identities and real telemetry remain unavailable.

Acceptance: public reproduction and CI pass; relocated PBIP refresh preserves
blank full-risk measures and the visible simulation classification.

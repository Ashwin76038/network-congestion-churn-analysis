# Simulated Network Service Experience & Data Readiness

Demonstrate service-metric calculations, dimensional joins and data-readiness checks using Excel-generated usage scenarios. The repository name and `churn_*` fields are legacy compatibility names; no measured customer-retention outcome is available.

## Executive summary

The project author confirms that usage, speed, downtime and latency were **generated with random Excel values** because operational logs were unavailable. Customer IDs were filled down as a row sequence; **ten OLT IDs** and **five dates (1-5 August 2026)** were chosen for the simulation. The frozen sample has **1,280 service-account keys** and **6,400 synthetic account-days**. Its calculated daily-average utilization is **9.83% across ten simulated OLT IDs**, using supplied capacity assumptions. This describes the scenario, not measured network conditions.

Full heuristic risk scoring remains **unavailable** because its rule requires two complete, non-overlapping seven-day windows. Five simulated days do not satisfy that rule. Customer source records come from an author-described confidential government-platform export; raw identifiers and portal/billing documents remain private. See the [simulation contract](docs/simulation_contract.md).

## Business questions

- How can account-day and OLT-day metrics be reproduced and reconciled?
- Are source-derived customer assignments compatible with simulated OLT assignments?
- Can synthetic complaint events be joined without using future information?
- Does the chosen scenario have enough history for the defined usage-change rule?

## Findings and actions

| Finding | Evidence | Decision |
|---|---|---|
| Scenario too short for the rule | 0 of 6,400 rows have two complete seven-day windows | Keep full scores blank; use explicitly labeled longer scenarios only for a separate simulation demonstration |
| Source/simulation assignments differ | 1,135 accounts have assigned/simulated OLT disagreement | Treat this as join compatibility, not an observed provisioning or migration problem |
| Simulation scope differs from customer groups | Ten simulated OLT IDs versus 12 source-address groups | Report both scopes; IDs 11/12 were outside the selected usage simulation |
| Daily-average calculation reconciles | 9.83% scenario mean, with no interval telemetry | Demonstrate units and arithmetic; avoid real capacity-upgrade conclusions |
| Synthetic complaint rule runs | 0 leakage-rule matches | Describe a rule demonstration, not actual support coverage |

The independent [data-readiness receipt](docs/data_readiness_receipt.json) quantifies the cross-source compatibility mismatch as **1,135/1,280 accounts (88.67%)** and the maximum synthetic OLT-day daily-average ratio as **17.98%**. Customer group IDs **11 and 12** lie outside the ten-ID usage simulation. These are scenario/merge findings, not real equipment failures or missing monitoring. See the [quality review](docs/data_readiness_review.md).

## Data and privacy

Public customer tables use generated row labels and omit direct contact identifiers. Usage measurements and complaints are synthetic; plans and capacities are supplied scenario metadata. See [data authenticity](docs/data_authenticity.md). Sequential IDs are not stable identities across reordered extracts. Pseudonymization does not guarantee protection against external linkage.

The author supplied the original customer workbook privately on 1 October 2026 and defined Activation Date as internet-service activation. Its 1,280 Combo-service rows corroborate the public customer ordering, but **1,275 public activation dates differ**. The original has **zero** dates after the configured OLT cutoff. A source-order comparison finds **71 simulated account-days across 15 keys** dated before original activation; arbitrary scenario dates cannot establish actual pre-activation traffic. See the [source review](docs/source_workbook_review.md) and [aggregate receipt](docs/source_workbook_receipt.json). Public data and Power BI inputs await reviewed correction.

## Method and KPIs

| KPI | Definition | Limit |
|---|---|---|
| Experience score | 0.5 speed score + 0.3 downtime score + 0.2 latency score | Analyst thresholds applied to synthetic measurements |
| Daily utilization | GB * 8 / 86400 / capacity Gbps | Scenario estimate using supplied capacities; daily average only |
| Usage drop | (prior 7-day mean - current 7-day mean) / prior mean | Two complete, disjoint windows required |
| Complaint leakage | Experience <50 and zero as-of 30-day complaints | Simulated complaints |
| Customer risk score | Weighted five-signal rule | Blank with insufficient history; not churn prediction |

See [methodology](docs/methodology.md), [dictionary](docs/data_dictionary.md) and [model](dashboard/Data_Model.md). Customer/date and OLT/date facts join their dimensions one-to-many. Duplicate keys and invalid capacities fail the rebuild.

The five-day simulation supports pipeline and metric verification. It cannot validate churn prediction, customer behavior or real network performance. Longer synthetic scenarios, if added separately, could demonstrate rule execution but would still not provide observed churn outcomes.

## Reproduce from public data

```bash
python -m pip install -r requirements.txt
python scripts/03_build_metrics.py
python -m unittest discover -s tests -v
python scripts/render_overview.py
python scripts/validate_sql.py
python scripts/audit_public.py
```

The rebuild updates clean and Power BI CSVs together, plus samples and [verified metrics](docs/validated_metrics.json). No private source is needed. `01_clean_data.py` is optional private-source preparation; never commit those inputs. `02_generate_complaints.py` is the documented synthetic generator.

For a read-only clean-clone verification path that does not rewrite the Power BI input copies, use [REPRODUCE_PUBLIC.md](docs/REPRODUCE_PUBLIC.md). `audit_public.py` checks raw/derived grains, capacity-ratio arithmetic, OLT coverage and assignment conflicts with an independent SQLite reconciliation. The author used **MySQL** in the original project; SQLite is the additional review-check engine, not the author's SQL platform. Native MySQL execution remains unverified in this review; see [SQL engine notes](docs/sql_engine_notes.md).

## Power BI report

Editable source: `dashboard/OLT_Professional_Project/OLT_Churn_Network_Risk_Professional.pbip`. Set the `DataRoot` Power Query parameter to the checkout's `dashboard/OLT_Professional_Project/data/` folder, including its final slash. Refresh and review the report in Power BI Desktop.

The old PBIX and screenshots were quarantined outside the repository because their risk counts predate the corrected metric definitions. A refreshed screenshot is pending; the source files are not claimed to have passed Desktop rendering tests. Legacy churn_* names and filenames are compatibility names only.

**Power BI validation remains pending:** Python, SQL and unit-test results do not prove DAX execution, slicer behavior or a current rendered report. No PBIP/TMDL/report files were changed during this data-readiness pass.

## Repository structure and skills

`data/clean/` holds public inputs and derived outputs; `scripts/` builds metrics; `tests/` covers edge cases; `sql/` contains executable SQLite analysis; `notebooks/` provides public EDA; `docs/` explains evidence and limits; `dashboard/` holds the editable Power BI model.

Skills: Python, pandas, MySQL (author-reported project engine), SQL window functions, DAX, dimensional modeling, data-quality validation and business communication. No measured retention improvement, predictive accuracy or causal effect is claimed.

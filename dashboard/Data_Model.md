# Model and filter contract

| Dimension / relationship | Facts filtered | Interpretation |
|---|---|---|
| olt_info_clean -> customers_clean by olt_id | Account metrics, usage and complaints through customers | 12 source-derived address groups; not physical inventory |
| plans_clean -> customers_clean by plan_id | Account metrics, usage and complaints through customers | Scenario tier metadata, not individual tariffs |
| customers_clean -> customer_daily_metrics / usage_logs_clean / complaints by customer_id | Account-day and event facts | Frozen service-account row labels |
| logged_olt -> customer_daily_metrics / usage_logs_clean / olt_daily_metrics by olt_id | Simulated logged measurements | Ten chosen simulation IDs with assumed capacities |
| DateTable -> each dated fact | Account/OLT daily metrics, usage and complaints | Five actual scenario dates |

All twelve relationships are many-to-one with single-direction dimension filtering. Assigned and logged OLT numbers are separate domains. Do not connect the network fact to assigned customer groups merely because labels overlap. Complaints have no logged-OLT attribute and do not respond to that slicer. Network daily-average ratios respond to logged OLT/date, not assigned OLT/plan. Source-group count reports assigned dimension scope. Slicers are page-local.

Exact customer activation dates are withheld; there is no activation-date relationship or cohort claim. Missing full risk is BLANK, while the count of complete rows can legitimately be zero. High-risk share divides by scored accounts and stays blank when none are scored. Distinct account totals are recalculated in context, not summed from overlapping categories.

Canonical measures are in `OLT_Professional_Project/OLT.SemanticModel/definition/tables/_Measures.tmdl`. [Executed DAX and visual validation](../docs/powerbi_validation.md) and [refresh guide](../docs/REPRODUCE_PUBLIC.md).

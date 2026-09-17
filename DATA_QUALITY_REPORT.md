# Data Quality Report

Scope: seven approved clean CSVs; source files preserved.

| Table | Rows | Columns | Grain | Duplicate Keys |
|---|---:|---:|---|---:|
| customers_clean | 1280 | 10 | customer_id | 0 |
| plans_clean | 4 | 5 | plan_id | 0 |
| usage_logs_clean | 6400 | 9 | customer_id + log_date | 0 |
| customer_daily_metrics | 6400 | 25 | customer_id + log_date | 0 |
| olt_daily_metrics | 50 | 8 | olt_id + log_date | 0 |
| olt_info_clean | 12 | 3 | olt_id | 0 |
| complaints | 805 | 5 | complaint_id | 0 |

## Confirmed Issues

- Invalid source utilization: source congestion_ratio_percent averages 32790.1191. The dashboard retains the prior rebuilt 24-hour utilization estimate of 0.0983313 (9.8%). It does not estimate peak congestion.
- 1,135 customer OLT assignments conflict with logged OLTs. Customer visuals use the assigned dimension OLT; network visuals use logged OLT. Operational comparisons need source-owner reconciliation.
- OLTs 11 and 12 have no network facts. Zero high-utilization OLTs applies only to observed OLTs.
- Only five dates are available. previous_7d_avg is a one-day-lagged expanding/rolling average, not a separate preceding seven-day period. Do not use it as a reliable seven-day usage-drop signal.
- Complaints are simulated according to existing project documentation. complaint_count is a customer-level all-period count repeated across dates, so leakage is not a historical as-of complaint measure.
- Daily risk categories overlap across dates. The professional distribution charts now assign each customer to their highest observed risk within the selected context. Default counts are 851 low, 424 medium, 5 high, totaling 1,280.
- Churn risk is a rule-based proxy; downtime and latency are inputs to its score. Diagnostic associations are descriptive, not causal validation or independent prediction.

## Validated Checks

No duplicate business keys, blank analytical IDs, invalid dates, or orphan parent keys were found. Experience scores and risk scores remain within 0-100. Existing leakage flags match the supplied check with zero differences and zero cases.

## Default KPIs

- Total Customers: 1280
- Total OLTs: 12
- High Congestion OLTs (average estimate): 0
- High Risk Customers: 5
- Avg Experience Score: 89.0703125
- Avg Congestion Ratio (average estimate): 0.09833129629629626
- Complaint Leakage: 0
- Avg Downtime Minutes: 14.99125
- Avg Latency Ms: 30.0309375

Complete column profiles, missing counts, numeric ranges and key checks are in dashboard/OLT_Professional_Project/data_quality.json.
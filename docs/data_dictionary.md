# Data dictionary

Public keys are pseudonymous service-account labels, not independently verified people. Data provenance and simulation status are documented in [data_authenticity.md](data_authenticity.md).

| Field | Type / example | Definition and source |
|---|---|---|
| customer_id | text; Customer_00001 | Pseudonymous supplied service row; primary key in customers_clean |
| plan_id | integer | FK to four supplied plan tiers |
| olt_id | integer | Assigned OLT in customers; logged OLT in usage/network tables; meanings differ |
| activation_date | date | Intended meaning: internet plan/service activation, confirmed by author; 1,275 public values differ from original workbook and require reconciliation before cohort claims |
| status | category | Supplied service state, not observed churn |
| customer_type | category | Supplied customer grouping |
| connection_count_per_customer | integer | Source attribute; do not sum across service rows |
| plan_tier / value_segment | category | Derived from source plan_category; not unique product identifiers |
| area | text | Generalized source geography; unknown stays unknown |
| speed_mbps / monthly_price | number | Supplied plan metadata; billing provenance unverified |
| olt_name / capacity_gbps | text / number | Generalized OLT label and supplied capacity |
| log_date | ISO date | Daily observation date |
| data_usage_gb | nonnegative number | Supplied daily volume, decimal GB assumption |
| avg_speed_mbps | nonnegative number | Supplied average speed |
| downtime_minutes | nonnegative number | Supplied daily downtime |
| latency_ms | nonnegative number | Supplied latency |
| speed_score / downtime_score / latency_score | integer 25-100 | Threshold component scores; exact cutoffs in methodology |
| experience_score | number 25-100 | 0.5 speed + 0.3 downtime + 0.2 latency scores |
| current_7d_avg | nullable number | Seven complete calendar days including log_date |
| previous_7d_avg | nullable number | Seven complete preceding days, disjoint from current window |
| usage_drop_percent | nullable number | 100*(previous-current)/previous; blank if incomplete or prior<=0 |
| usage_window_complete | boolean | Both seven-day averages exist and previous is positive |
| complaint_id | text; CMP_00001 | Synthetic event primary key |
| complaint_date / category / resolution_time_hours | date / text / integer | Generated event details; seed 42 |
| complaint_count | integer | Cumulative simulated events on/before row date |
| complaint_count_30d | integer | Events in (row date-30 days, row date] |
| complaint_leakage_flag | integer 0/1 | experience<50 and complaint_count_30d=0 |
| high_usage_drop_flag | integer 0/1 | Usage drop >=30; meaningful only when window complete |
| high_downtime_flag / high_latency_flag | integer 0/1 | Downtime>20 minutes / latency>40 ms |
| low_experience_flag | integer 0/1 | Experience<50 |
| risk_observed_component_score | integer 0-100 | Sum of observed weighted flags; incomplete score is not full risk |
| churn_risk_score | nullable integer | Compatibility name: weighted rule score, blank without complete history |
| churn_risk_category | text | Low/Medium/High Risk or Insufficient history |
| total_usage_gb | number | Sum by logged OLT/date |
| avg_gbps | number | total_usage_gb*8/86400 |
| congestion_ratio | decimal | avg_gbps/capacity_gbps |
| congestion_ratio_percent | decimal | Compatibility alias of ratio; do NOT multiply by 100 inside Power BI |
| congestion_status | text | Healthy below .6; Moderate .6-.8 inclusive; High above .8 |

Grains: customers=account; plans=plan; OLTs=OLT; usage/metrics=account-date; network=OLT-date; complaints=event. See [methodology](methodology.md) for missingness, thresholds and limitations. All examples are artificial/generalized.

# Power BI Dashboard Plan

## Dashboard Title

OLT Churn & Network Risk Overview

## Import Only These Clean Tables

- `customers_clean.csv`
- `plans_clean.csv`
- `usage_logs_clean.csv`
- `customer_daily_metrics.csv`
- `olt_daily_metrics.csv`
- `olt_info_clean.csv`
- `complaints.csv`

Do not import raw customer files or old Excel files.

## Relationships

| From | To |
| --- | --- |
| `plans_clean[plan_id]` | `customers_clean[plan_id]` |
| `customers_clean[customer_id]` | `customer_daily_metrics[customer_id]` |
| `customers_clean[customer_id]` | `complaints[customer_id]` |
| `olt_info_clean[olt_id]` | `customers_clean[olt_id]` |
| `olt_info_clean[olt_id]` | `olt_daily_metrics[olt_id]` |

## DAX Measures

```DAX
Total Customers =
DISTINCTCOUNT(customers_clean[customer_id])

High Risk Customers =
CALCULATE(
    DISTINCTCOUNT(customer_daily_metrics[customer_id]),
    customer_daily_metrics[churn_risk_category] = "High Risk"
)

% High Risk Customers =
DIVIDE([High Risk Customers], [Total Customers], 0)

Avg Experience Score =
AVERAGE(customer_daily_metrics[experience_score])

Complaint Leakage Count =
CALCULATE(
    COUNTROWS(customer_daily_metrics),
    customer_daily_metrics[complaint_leakage_flag] = 1
)

Avg Congestion Ratio =
AVERAGE(olt_daily_metrics[congestion_ratio_percent])

High Congestion OLTs =
CALCULATE(
    DISTINCTCOUNT(olt_daily_metrics[olt_id]),
    olt_daily_metrics[congestion_status] = "High"
)
```

## One-Page Layout

Top KPI cards:

- Total Customers: 1,280
- % High Risk Customers: 0.4%
- Avg Experience Score: 89.1
- Complaint Leakage Count: 0
- Avg Congestion Ratio: 32790.1%
- High Congestion OLTs: 10

Middle visuals:

- OLT congestion bar chart: `olt_id` by average `congestion_ratio_percent`
- Churn risk by value segment: `value_segment` by distinct customer count, colored by `churn_risk_category`

Bottom visuals:

- Complaint leakage table: customer ID, OLT ID, value segment, experience score, churn risk score
- Experience score trend: `log_date` by average `experience_score`

Slicers:

- Date
- Plan Tier
- Value Segment
- OLT ID
- Risk Category

## Screenshot Checklist

Export these after building the `.pbix` manually:

- `dashboard/screenshots/overview.png`
- `dashboard/screenshots/olt_congestion.png`
- `dashboard/screenshots/complaint_leakage.png`

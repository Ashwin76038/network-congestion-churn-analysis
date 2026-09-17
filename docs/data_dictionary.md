# Data Dictionary

## Privacy and Grain

The clean dataset is anonymized. Real names, phone numbers, emails, full addresses, service numbers, source-system service codes, staff names, and raw OLT IPs are removed from committed clean files.

| Table | Grain | Notes |
| --- | --- | --- |
| customers_clean | 1 row per customer | Uses `Customer_00001` IDs and area-level geography only. |
| plans_clean | 1 row per plan tier | Consolidates the duplicated plan source into the 4 analytical tiers. |
| usage_logs_clean | 1 row per customer per date | Daily customer experience and usage observations. |
| olt_info_clean | 1 row per OLT | Removes raw OLT IP and keeps capacity. |
| complaints | 1 row per simulated complaint | Simulated from poor-service cases to model incomplete complaint logging. |
| customer_daily_metrics | 1 row per customer per date | Adds experience, usage drop, complaint leakage, and churn-risk proxy. |
| olt_daily_metrics | 1 row per OLT per date | Adds corrected congestion calculations. |

## Metric Definitions

### Congestion Ratio

`avg_gbps = (total_usage_gb * 8) / (24 * 3600)`

`congestion_ratio = avg_gbps / capacity_gbps`

`congestion_ratio_percent = congestion_ratio * 100`

Status: `< 60% = Healthy`, `60% to 80% = Moderate`, `> 80% = High`.

### Experience Score

`experience_score = 0.5 * speed_score + 0.3 * downtime_score + 0.2 * latency_score`

Each component is bucketed from 25 to 100. Scores are validated between 0 and 100.

### Usage Drop Percent

`usage_drop_percent = ((previous_7d_avg - current_7d_avg) / previous_7d_avg) * 100`

If the previous rolling average is zero or unavailable, the result is blank.

### Complaint Leakage

`complaint_leakage_flag = 1` when `experience_score < 50` and `complaint_count = 0`; otherwise `0`.

### Churn Risk Score

Rule-based proxy score from 0 to 100:

| Signal | Weight |
| --- | ---: |
| High usage drop | 30 |
| High downtime | 25 |
| High latency | 20 |
| Low experience score | 15 |
| Complaint leakage | 10 |

Risk categories: `0-39 = Low Risk`, `40-69 = Medium Risk`, `70-100 = High Risk`.

## Complaint Simulation Logic

Complaint data is simulated because the project needs complaint leakage evidence and the original source does not include a trustworthy complaints table. Customers with high downtime, high latency, or low experience score are considered poor-service customers. A deterministic random seed records complaints for about 65% of these customers. The remaining silent poor-service customers become leakage cases.

# Final Validation

> Historical validation record. Its congestion figures were later found invalid. Current Professional report QA is in `../DATA_QUALITY_REPORT.md` and `../dashboard/OLT_Professional_Project/data_quality.json`. The dashboard uses a 9.8% daily average utilization estimate, not peak congestion. Do not use the old percentage claims below for decisions.

## Data Validation Summary

| Check | Result |
| --- | --- |
| Customers grain | 1,280 rows; unique `customer_id` = True |
| Usage grain | 6,400 rows; unique `customer_id + log_date` = True |
| Plans grain | 4 rows; unique `plan_id` = True |
| OLT grain | 12 rows; unique `olt_id` = True |
| Customer-plan join coverage | 100.0% |
| Customer-OLT join coverage | 100.0% |
| Usage-customer join coverage | 100.0% |
| Experience score range | 62 to 100 |
| Churn risk score range | 0 to 75 |

## KPI Traceability Table

| README KPI | Source File/Query/Measure | Match? | Notes |
| --- | --- | --- | --- |
| Total Customers = 1,280 | `data/clean/customers_clean.csv`; DAX `[Total Customers]`; SQL Query 7 | Yes | Distinct anonymized customer count. |
| High Risk Customers = 5 (0.4%) | `customer_daily_metrics.csv`; DAX `[% High Risk Customers]`; SQL Query 2/7 | Yes | Distinct customers with any high-risk customer-day before slicers. |
| Avg Experience Score = 89.1 | `customer_daily_metrics.csv`; DAX `[Avg Experience Score]`; SQL Query 7 | Yes | Average across customer-day metric rows before slicers. |
| Complaint Leakage Count = 0 | `customer_daily_metrics.csv`; DAX `[Complaint Leakage Count]`; SQL Query 6/7 | Yes | Strict requested rule: `experience_score < 50` and no complaint. |
| Avg Congestion Ratio = 32790.1% | `olt_daily_metrics.csv`; DAX `[Avg Congestion Ratio]`; SQL Query 5/7 | Yes | Average across OLT-date records. |

## Interview Q&A

1. Why did you build this project? To show how network experience data can be turned into retention and capacity-planning decisions for an ISP.
2. What business problem does it solve? It helps identify overloaded OLTs, poor customer experience, silent dissatisfaction, and rule-based customer risk.
3. Is this real data? The source contains realistic ISP-style records, but the portfolio version is anonymized and the complaints table is simulated.
4. How did you handle privacy? Direct PII was removed, customer IDs were replaced, addresses were reduced to area level, and raw files are blocked by `.gitignore`.
5. What is complaint leakage? It is a customer with poor measured service experience but no recorded complaint.
6. How did you calculate congestion ratio? I converted daily GB volume into average Gbps, then divided by OLT capacity in Gbps.
7. Why did you use experience score? It gives a single, explainable score that combines speed, downtime, and latency.
8. What SQL queries did you write? The SQL file includes joins, risk grouping, rolling averages, window functions, OLT ranking, leakage detection, and KPI validation.
9. What does the dashboard help the business decide? It shows where to prioritize capacity upgrades, customer outreach, and complaint-process improvements.
10. What would you improve next? Add real churn labels, longer history, complaint system extracts, and a production data model.

## Hiring-Manager Rating

Current score: 78/100.

Strong points: privacy handling, realistic business problem, corrected congestion formula, runnable Python scripts, SQL evidence, and a recruiter-friendly README.

Must-fix issues before claiming production readiness: build the actual Power BI `.pbix`, export real dashboard screenshots, add longer time history, and avoid calling the churn score a predictive model.

Improvements to reach 80+/100: finish the Power BI file, add automated tests for grain and join coverage, add a small ERD image, and extend the simulated dataset to at least 60-90 days.

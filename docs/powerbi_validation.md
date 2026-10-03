# Executed Power BI validation

On 2 October 2026, `dashboard/OLT_Professional_Project/OLT_Churn_Network_Risk_Professional.pbip` was opened, refreshed from sanitized CSVs, pending changes applied, all pages inspected and the project saved in Power BI Desktop.

**133/133 native DAX checks passed**, with empty Failures (375.3 ms in the captured run). The independent pandas generator checks 19 measures across All, assigned OLT 1, logged OLT 9, Basic plan, 1 August, assigned OLT 11, and combined assigned/logged/date contexts. Expectations and executed query are in `dax_validation_cases.json` and `validate_measures.dax`; screenshot `dashboard/screenshots/dax-validation.png` captures native results.

Checks cover blank risk/high-risk share, zero complete/scored rows, filter denominators, mismatch account counts, experience, units and the distinct filter scopes below. This validates selected contexts, not every possible interaction or real model performance.

## Visual checks

- Overview: 1,280 account keys, 6,400 account-days, five dates, experience 89.07 and blank risk; network ratio and plan charts rendered.
- Logged OLT 1 selection: 137 accounts, 685 account-days, five dates, experience 90.26, risk still blank. Independent pandas mean=90.25912408759125. Both charts updated; clearing selection restored overview totals.
- Experience page: 805 synthetic complaints, zero leakage matches, average downtime 14.99 minutes and latency 30.03 ms. Usage card abbreviates the exact total to 89K; exact expectations are in the DAX case file. Date bars use a continuous date axis; intermediate axis ticks are not extra observed days.
- Readiness: 1,135 conflicts, 88.67%, ten logged IDs, 12 assigned source groups, zero complete-window rows. Daily bars show 1,280 rows on each of the five dates.
- Current screenshots are native captures in `dashboard/screenshots/`; none are generated mockups.

## Filter contract

Twelve single-direction relationships connect nine data tables (plus a measure container). Assigned source OLT and plan filter customer/account facts. Logged OLT filters usage, customer metrics and network metrics. Scenario date filters the dated facts. Network ratios deliberately do not inherit assigned-OLT or customer-plan filters; their chart title says logged OLT/date only. Complaints filter by assigned customer and date, not logged OLT. Source-group count describes assigned dimension scope. Slicers are page-local, not synchronized across pages. See `dashboard/Data_Model.md`.

Native MySQL separately passed 12 checks. Python tests and SQL receipts do not substitute for this Desktop execution. All measurements and complaints remain simulated; no actual churn, peak congestion or operational causal effect is validated.

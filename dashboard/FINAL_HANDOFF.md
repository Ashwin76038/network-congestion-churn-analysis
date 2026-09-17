# Network Congestion and Churn Analysis: Final Handoff

## 1. Existing Work Found

Completed at discovery: seven clean CSV datasets, transformation scripts, SQL/notebook work, a reusable TMDL semantic model, core measures, and validation documentation.

Partially completed: a single-page report prototype and dashboard design work.

Not completed at discovery: the requested two-page Professional PBIX, tested navigation/reset, and final screenshots. These are now delivered. Valid prior work was preserved, not restarted.

## 2. Backup Created

Original PBIX (unchanged rollback):
`C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\OLT_Churn_Network_Risk.pbix`

Working PBIX (finished report):
`C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\OLT_Churn_Network_Risk_Professional.pbix`

Original SHA256 remains `88246c58a5d93708cfc403df52c3dd207da61a82c4e16294d91fce92de2ab992`.

## 3. Problems Found

- The original average congestion result of 32790.1% was invalid. Peak-throughput telemetry is unavailable; a simple percentage-format correction would not resolve the underlying problem.
- Assigned and logged OLTs differ for 1,135 customers. Customer analysis uses assigned OLT; network facts use logged OLT. These were not silently reconciled.
- Only 10 of 12 OLTs have network observations. Missing telemetry is not evidence of a healthy OLT.
- Only five days of data are supplied, August 1-5, 2026. Complaints are simulated. Churn risk is a rule-based proxy, not a validated churn prediction.
- Previous seven-day averages and repeated all-period complaint counts cannot support independent long-term or as-of causal claims.
- The initial reset bookmark failed to clear slicers and affected chart/table state. Live testing identified and repaired this.

## 4. Fixes Applied

- Recomputed OLT daily average throughput from logged usage: GB x 8 / 86400, divided by capacity in Gbps. Displayed as estimated 24-hour utilization, not peak congestion.
- Preserved original source datasets and used transformed clean model inputs.
- Used exclusive worst-observed customer risk categories to avoid counting the same customer in multiple categories over time.
- Replaced empty complaint-leakage detail with a truthful zero-case status card.
- Created the two-page report, synced filters, navigation, tooltips, conditional utilization colors, and a tested Reset Filters bookmark.
- Restored high-risk-only attention-table scope, descending OLT utilization sorting, and a table height showing all five default attention rows.
- Reimported the professional theme through Power BI Desktop and saved the finished PBIX. Final screenshots contain report canvas only, excluding the account header.

## 5. Page 1 - Executive Overview

Six measure-driven cards: Total Customers, High Risk Customers %, Average Experience Score, Complaint Leakage, Average Utilization (24h), and High Utilization OLTs.

Five slicers: Date, Plan Tier, Value Segment, OLT ID, Risk Category.

Visuals: experience trend, risk by value segment, descending OLT utilization overview, exclusive customer-risk donut, dynamic insight, and methodological footer. Consistent light background, white containers, blue navigation, and pink/teal/amber risk palette.

## 6. Page 2 - Network & Churn Analysis

Six cards: Total OLTs, High Utilization OLTs, Average Utilization (24h), High Risk Customers, Average Downtime, and Average Latency.

Visuals: descending OLT utilization detail, experience-versus-risk scatter, downtime by risk category with diagnostic tooltips, high-risk customer attention table, and complaint-leakage status. Shared slicers and page navigation are retained.

## 7. DAX / Model Changes

Reused `_Measures`, DateTable, clean tables, and active one-to-many, single-direction relationships. Customer IDs are unique: 1,280 rows represent 1,280 distinct customers, so Total Customers is appropriate.

Added diagnostic measures: Avg Downtime Minutes, Avg Latency Ms, Avg Risk Score, Max Risk Score, Total Usage GB, Utilization Status, Utilization Color, Network Coverage Summary, Executive Insight, and Worst Risk Customers. Existing core measures and dependencies remain intact.

DateTable covers the supplied five-day window and must be extended when new dates arrive. Usage logs are related and available through Total Usage GB; a redundant behavioral chart was omitted because the five-day window does not support the claimed prior-seven-day interpretation.

## 8. Files Modified

- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\README.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\docs\final_validation.md` (historical-result warning)
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\OLT_Professional_Project\OLT.Report\definition\` (final UI-tested report definitions synchronized from the saved PBIX)

## 9. Files Created

- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\OLT_Churn_Network_Risk_Professional.pbix`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\OLT_Professional_Project\` (editable PBIP/TMDL, clean model inputs, build/audit scripts, and QA JSON)
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\DAX_Measures.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\Data_Model.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\DATA_QUALITY_REPORT.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\PRIVACY_AUDIT.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\TRANSFORMATION_LOG.md`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\screenshots\executive_overview.png`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\screenshots\network_churn_analysis.png`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\screenshots\olt_congestion.png`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\screenshots\complaint_leakage.png`
- `C:\Users\Admin\Documents\Network Congestion and Churn analysis\dashboard\FINAL_HANDOFF.md`

The PBIX is the authoritative finished deliverable. Do not rerun the original build script over final report definitions without a backup: it scaffolds the report and does not include every final Desktop interaction repair.

## 10. Remaining Manual Actions

None for opening and using the completed local dashboard. Publication to Power BI Service was not requested or performed. Refresh on another computer requires updating local CSV paths and extending DateTable if the source period changes.

## 11. Final QA

Share with caveats: visually complete and usable within the supplied dataset, but not production-grade predictive evidence.

| Check | Result |
|---|---|
| PII | No direct customer names, emails, phones, or addresses in the seven model inputs or report screenshots. Pseudonymous analytical IDs remain. |
| Total Customers | 1,280 distinct customer IDs |
| Total OLTs | 12; 10 observed in network facts |
| High Utilization OLTs | 0 among observed OLTs; does not establish peak-congestion absence |
| High Risk Customers | 5; 0.390625%, displayed as 0.4% |
| Average Experience | 89.0703125, displayed as 89.1 |
| Average utilization | 9.83312963%, displayed as 9.8%; estimated 24-hour average |
| Complaint Leakage | 0 customers; 0% rate |
| Exclusive risk distribution | Low 851, Medium 424, High 5; total 1,280 |
| Average downtime / latency | 15.0 minutes / 30.0 ms |
| Relationships | Active single-direction one-to-many core paths; no new ambiguous fact-to-fact joins |
| PBIX structure | Two pages, 44 visual definitions, populated embedded DataModel |
| Reopening | Both saved pages reopened and rendered in Desktop |

Live interaction checks:

- Plan Basic: 91 customers, 74.5 experience, 3.3% high risk; network utilization remains 9.8%.
- OLT 1: 449 assigned customers and 1.9% logged network utilization. Navigation retained the OLT selection on diagnostics.
- High Risk: customer diagnostics narrowed, downtime 23.2 minutes and latency 45.8 ms; network utilization remained 9.8%.
- High-value segment: zero high-risk customers; attention table correctly becomes empty.
- August 3-5 plus high-value segment: Executive showed 746 customers and 92.7 experience; trend contained only the three selected dates.
- Reset restored all five default slicers, retained the current page, and preserved the repaired attention-table filter.
- Both navigation directions were exercised. Date, segment and OLT synchronization were observed. Plan and risk controls were exercised directly; exhaustive permutations were not tested.
- Default KPI values reconciled to independent clean-data checks. Both pages rendered without broken visuals. Four actual Desktop screenshots were exported.

## 12. Portfolio Assessment

Subjective assessment, not an external certification:

| Dimension | Score /10 |
|---|---:|
| Data quality | 5 |
| Data model | 8 |
| Business logic | 7 |
| Dashboard design | 8 |
| Storytelling | 8 |
| Recruiter readability | 8 |
| Overall | 7.5 |

The biggest remaining weakness is source validity, especially assigned/logged OLT disagreement, missing peak telemetry, simulated complaints, and the five-day observation window. More visual complexity would not fix those limits. The dashboard is suitable as an honestly documented telecom BI portfolio example, not as proof of causal network-driven churn or a validated production prediction model.

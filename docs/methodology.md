# Methodology

Grain: one pseudonymous service-account/date usage row, one OLT/date network row, one event per complaint. There are 1,280 service accounts, not independently verified unique people. The separate OLT portfolio project groups service records into 1,193 source customer labels; those keys cannot be cross-joined to this project.

Usage, speed, downtime and latency are Excel-generated synthetic values, confirmed by the author. Ten OLT IDs, five scenario dates and sequential customer IDs were deliberately chosen. Customer dimensions derive from a confidential original export; plan/capacity inputs are supplied scenario assumptions. Metrics describe simulated cases. See [simulation contract](simulation_contract.md).

Experience uses speed weights 100/75/50/25 for >=100/>=50/>=20/<20 Mbps; downtime weights 100/75/50/25 for <=10/<=30/<=60/>60 minutes; latency weights 100/75/50/25 for <=30/<=60/<=100/>100 ms. Composite weights are 0.5/0.3/0.2. Fractional boundaries are continuous. These thresholds are assumptions, not validated SLAs.

Current usage averages seven calendar days including the observation date. Previous usage averages the preceding seven disjoint days. All fourteen measurements and a positive prior average are required; missing history is not zero usage. Only five dates are supplied, so the full risk score and category are unavailable. Observed component points remain inspectable separately. No high-risk count should be published as zero.

Complaints count only events dated on or before each observation. The recent window is (date-30 days, date]. Leakage denotes experience <50 and zero recent simulated complaints; zero observed cases cannot validate complaint completeness.

Risk points: usage drop >=30%=30, downtime >20=25, latency >40=20, experience <50=15, leakage=10. Scores 0-39/40-69/70-100 map to low/medium/high only when the usage window is complete. No historical churn label exists; the legacy churn_* column names are retained for model compatibility only.

OLT ratios are decimal values in both congestion_ratio and the legacy congestion_ratio_percent field. Power BI formats the latter as %. Average utilization is an unweighted mean across observed OLT-days. Missing OLTs remain absent, not zero. Thresholds <0.6, 0.6-0.8 inclusive, >0.8 are illustrative daily-average bands and cannot establish peak capacity needs.

Use simulated usage OLT for scenario metrics and source-derived assigned OLT for customer segmentation, with both origins labeled. Their numeric labels do not establish a common real equipment identity. The 1,135 mismatches and absent IDs 11/12 are cross-source compatibility/scope checks, not observed migrations or missing monitoring. SQL groups accounts exclusively by worst complete score, with an explicit insufficient-history group.

Validation: unit fixtures test fourteen-day windows, future complaints, missing days, fractional thresholds, duplicate keys and capacity units. Public rebuild and SQL checks require no raw workbook. Power BI semantic/report files must still be refreshed and inspected in Desktop; existing binaries/screenshots were quarantined to avoid publishing stale metrics.

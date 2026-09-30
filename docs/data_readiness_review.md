# Network service experience: public data-readiness review

The strongest defensible result is a **data-readiness decision**, not a churn score or a finding that peak congestion is low. Reproduce the numbers with `python scripts/audit_public.py --output docs/data_readiness_receipt.json`. That script reads only committed public CSVs, recomputes the OLT daily-average ratios from usage and capacity, and cross-checks OLT mapping/coverage with SQLite. `python scripts/validate_sql.py` runs eight business and quality queries.

| Finding | Public evidence | Decision risk | Severity / confidence | Next action |
|---|---:|---|---|---|
| Behavioral history too short | 1,280 service-account keys x 5 dates = 6,400 account-days; 0 complete 14-day windows; 0 full scores | A high-risk count of zero would falsely imply risk was assessed | High / high | Obtain at least 14 consecutive, sourced days; preferably longer for holdout validation. Until then, show “Insufficient history” |
| Assigned/logged OLT conflict | 1,135/1,280 accounts (88.67%) differ; 5,675/6,400 account-days affected | A joined OLT-to-experience attribution could point teams at the wrong equipment | High / high | Ask the source owner whether fields represent provisioning, current attachment, migration or extraction error. Preserve both fields; do not auto-correct |
| OLT coverage gap | 10/12 OLTs logged; OLT 11 and 12 have 7 and 3 assigned accounts but no logged usage | Missing equipment could be mistaken for healthy/zero utilization | High / high | Confirm collection scope and source mapping before capacity decisions |
| Daily-average proxy only | Mean ratio 9.83%; maximum observed OLT-day ratio 17.98% | A day-level average can hide short peaks | Medium / high | Obtain interval throughput/capacity telemetry to study actual peak congestion |
| Complaint events are generated | 805 synthetic events; 0 complaint-leakage rule matches | Does not establish true support coverage or customer behavior | Medium / high | Use authentic, consented and pseudonymized complaint events or present the rule only as a simulation |
| Usage provenance unresolved | Original usage collection logs or generator are not in the public repo | “Real network telemetry” would be unsupported | High / high for the gap; cause unknown | Obtain a source-owner data contract or keep the case study labeled as a supplied sample |
| Power BI validation pending | PBIP source exists, but Desktop refresh and new visual evidence are not documented | A current interactive dashboard cannot yet be defended | Medium / high | Refresh, reconcile DAX and inspect slicers only after approval for Power BI changes |

## Likely causes versus verified facts

The two missing logged OLTs and large assignment mismatch could reflect changing attachment, different field meanings, mapping drift, or data extraction errors. **None of these causes is established by the public files.** The supplied five-day sample and generated complaints are enough to test pipeline behavior, but not to validate customer-retention outcomes. Thresholds for speed, downtime, latency and utilization remain analyst assumptions, not verified service-level agreements.

## Decision supported now

An operations analyst can prioritize source-system reconciliation and collection coverage: investigate the OLT assignment conflict, recover the two missing OLT groups, obtain longer account histories and interval telemetry, then refresh the BI report. Do not make customer-retention, network-upgrade or causal equipment decisions from these data alone.

## Before and after this review

| Item | Latest committed starting state | This review |
|---|---|---|
| History/risk availability | Five days, zero complete two-window scores | Unchanged; new audit and tests assert 0 complete scores and 6,400 unavailable account-day scores |
| OLT mapping | 1,135 conflicting account assignments already mentioned | Unchanged; new by-assigned-OLT queue and SQLite check reconcile 1,135/1,280 accounts and 5,675 account-days |
| OLT coverage and units | 10/12 logged groups and 9.83% daily-average ratio | Unchanged; new receipt identifies missing OLTs 11/12 and recomputes ratios from GB, seconds and Gbps |
| Automated checks | 6 passing baseline tests; 6 SQL queries | 9 passing tests; 8 SQL queries, including mapping and coverage checks |
| Power BI | PBIP source present, current Desktop output unverified | PBIP unchanged; DAX, filters, denominators and visuals still require Desktop validation |

The three strongest findings are the unavailable 14-day risk window, the 88.67% assigned/logged OLT conflict, and the 10-of-12 logged coverage with only daily-average utilization. This is a stronger **service-experience and data-readiness** case, but it does **not yet meet a defensible 4/5 BI-project rating**: authentic longitudinal usage and source-field meanings are unavailable, and the refreshed PBIP has not been validated in Desktop. Even after a Desktop refresh, this sample cannot substantiate churn prediction or peak congestion.

## Resume-safe explanation

“I built account-day and OLT-day service metrics, then found the published sample is not ready for the proposed risk score: five days cannot form two seven-day windows. I kept the score unavailable, quantified an 88.67% assigned/logged OLT mismatch and a 10-of-12 coverage gap, and used those findings to define what data must be repaired before targeting customers or equipment. The current Power BI source still needs Desktop refresh and validation.”

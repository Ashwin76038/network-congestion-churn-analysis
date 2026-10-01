# Simulated network service experience: data-readiness review

The author confirms that usage, speed, downtime and latency were generated with random Excel values. Ten OLT IDs, sequential account IDs and five scenario dates were deliberately chosen. Customer metadata comes from a privately supplied confidential government-platform export. This project demonstrates metric calculations, joins and rule readiness; its values do not describe measured network performance.

Reproduce aggregate evidence with `python scripts/audit_public.py`; `python scripts/validate_sql.py` executes eight demonstration queries. Frozen CSV values support repeatable metric calculations, but the original random generation cannot be recreated exactly without its Excel formulas and random state. See [simulation contract](simulation_contract.md).

| Finding | Evidence | Correct interpretation / action |
|---|---|---|
| Scenario too short for the rule | 1,280 keys x five dates = 6,400 synthetic account-days; zero complete 14-day windows | Keep full scores blank. A separate longer labeled simulation could demonstrate execution; no extra days were created |
| Source/simulation OLT assignments differ | 1,135/1,280 account keys (88.67%); 5,675 account-days | Cross-source join compatibility, not observed provisioning drift, customer migration or a causal experience driver |
| Different OLT scopes | Ten simulated usage IDs; source-address groups 11/12 have seven/three assigned accounts | State the ten-ID simulation scope. This is not established missing operational telemetry or a physical device inventory |
| Synthetic daily-average ratio | Mean 9.83%; maximum scenario OLT-day 17.98% | Demonstrates GB/seconds/Gbps units against supplied capacity assumptions; no actual peak congestion is measured |
| Generated complaint events | 805 synthetic events; zero leakage-rule matches | Demonstrates as-of joins/rules, not actual support completeness |
| Customer dates differ from original | 1,275 public activation dates differ under corroborated row-order comparison | Original activation meaning is author-confirmed; the transformation still needs documented, privacy-reviewed reconciliation |
| Simulation chronology differs | 71 synthetic account-days across 15 keys precede original activation | Arbitrary scenario dates do not establish real pre-activation traffic or source-system faults |
| Power BI still pending | Editable PBIP exists; current Desktop execution not documented | Adopt simulation labels and execute DAX, slicer and visual reconciliation after the user's approval |

## Before and after

The numeric sample is unchanged. Its origin and interpretation are now explicit: usage was generated in Excel, IDs were filled down, and ten OLT IDs/five dates were selected for demonstration. Earlier provisional descriptions of missing telemetry or operational mapping conflicts are superseded by the simulation contract. Private portal and billing documents will not be requested or published.

Tests increased from six baseline tests to twelve after the public/source audits; SQL checks increased from six to eight. Executed checks cover complete disjoint windows, missing dates, as-of complaints, fractional thresholds, units, public reconciliation, explicit source date parsing and refusal to force uncertain source linkage. Native Power BI execution and screenshots remain pending. Earlier creation-chat design advice is not empirical validation of churn or infrastructure claims.

## Portfolio scope and interview story

The three strongest results are correct unavailable-risk behavior, explicit separation of source and simulated equipment identities, and reproducible unit/denominator checks. A clearly disclosed simulation can be a valid analyst portfolio project without operational logs. A defensible 4/5 still needs a finished, useful Power BI report with executed DAX/filter/visual reconciliation and current evidence. Confidentiality does not require replacing absent facts with operational claims.

“I combined a sanitized customer export with a clearly labeled Excel usage simulation. I modeled account-day and OLT-day metrics, reconciled units and totals, kept the full heuristic score blank when five days could not satisfy its 14-day rule, and identified incompatible OLT assignments between the sources. The work demonstrates analytical modeling and validation. The Power BI source still needs Desktop validation.”

# Data authenticity

| Source | Classification | Evidence and limitation |
|---|---|---|
| Customer extract | Original workbook supplied privately by author on 1 October 2026; collection independently unverified | 1,320 original rows; Combo-service scope gives 1,280. Original Activation Date means service activation per author; 1,275 public dates differ under corroborated source-order comparison. See source_workbook_review.md. Raw identifiers remain private. |
| Usage, speed, downtime, latency | Supplied; real versus synthetic provenance unresolved | Only five days; no collection logs or original generator supplied in this repository. Do not describe these as verified real telemetry. |
| Plans and OLT capacity | Supplied metadata; provenance unverified | Four broad tiers and 12 OLTs. Tier assignment is derived from value_segment. |
| Complaints | Synthetic | Seed 42; scripts/02_generate_complaints.py selects approximately 65% of service accounts meeting heuristic conditions. Resolution hours are generated. |
| Experience and risk | Derived, rule-based | scripts/metrics.py; not independently validated churn outcomes. |
| OLT utilization | Derived daily average estimate | Logged GB * 8 / 86400 / capacity Gbps; not a peak congestion measurement. |

Simulation provides a demonstration of complaint joins and leakage rules, not evidence of customer behavior. Do not publish causal, predictive or real operational outcome claims. Customer dimension OLT and logged OLT disagree for 1,135 accounts; reconcile upstream before assigning accountability.

The original workbook contains no usage, speed, downtime, latency or interval-capacity logs. It resolves the intended activation-field meaning and provides source dates, but does not verify the network measurements. Fifteen account keys have 71 account-days preceding original activation under source-order mapping; investigate source timing and plan/service meanings before any exclusions.

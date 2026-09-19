# Data authenticity

| Source | Classification | Evidence and limitation |
|---|---|---|
| Customer extract | Supplied, pseudonymized; operational provenance unverified | Cleaner removes names/contact fields and replaces keys. One key per supplied service row; unique people cannot be recovered from public keys. |
| Usage, speed, downtime, latency | Supplied; real versus synthetic provenance unresolved | Only five days; no collection logs or original generator supplied in this repository. Do not describe these as verified real telemetry. |
| Plans and OLT capacity | Supplied metadata; provenance unverified | Four broad tiers and 12 OLTs. Tier assignment is derived from value_segment. |
| Complaints | Synthetic | Seed 42; scripts/02_generate_complaints.py selects approximately 65% of service accounts meeting heuristic conditions. Resolution hours are generated. |
| Experience and risk | Derived, rule-based | scripts/metrics.py; not independently validated churn outcomes. |
| OLT utilization | Derived daily average estimate | Logged GB * 8 / 86400 / capacity Gbps; not a peak congestion measurement. |

Simulation provides a demonstration of complaint joins and leakage rules, not evidence of customer behavior. Do not publish causal, predictive or real operational outcome claims. Customer dimension OLT and logged OLT disagree for 1,135 accounts; reconcile upstream before assigning accountability.

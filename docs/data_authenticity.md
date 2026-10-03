# Data authenticity

| Source | Classification | Evidence and limitation |
|---|---|---|
| Customer extract | Author-described confidential government-platform export, supplied privately | 1,320 original rows; Combo-service scope gives 1,280. Activation Date means service activation per author; 1,275 earlier prepared dates differed; all precise public dates are now withheld. Raw identifiers and confidential portal documentation remain private. |
| Usage, speed, downtime, latency | Synthetic Excel random values, confirmed by author | Ten OLT IDs and five scenario dates deliberately selected. Original Excel formulas/random seed were not supplied; frozen CSV values can be reanalyzed but original generation cannot be reproduced exactly. |
| Customer IDs | Generated row labels | Filled down sequentially; transformed to Customer_00001-style public labels. Stable only for the frozen sample/order, not a verified source identity. |
| Network plans and OLT capacity | Supplied scenario metadata; actual capacities and tariff mapping unverified | Four broad tiers, a 12-group customer/OLT dimension and ten usage-simulation IDs. Tier assignment is derived from value_segment; physical OLT inventory is not established by address/group counts. |
| Complaints | Synthetic | Seed 42; scripts/02_generate_complaints.py selects approximately 65% of service accounts meeting heuristic conditions. Resolution hours are generated. |
| Experience and risk | Derived, rule-based | scripts/metrics.py; not independently validated churn outcomes. |
| OLT utilization | Derived simulation estimate | Synthetic GB * 8 / 86400 / supplied capacity Gbps; not observed peak congestion. |

Simulation demonstrates calculations, joins and rule behavior. Customer dimension OLT and simulated usage OLT differ for 1,135 accounts; this is cross-source compatibility, not evidence of real provisioning errors, migration or operational mapping drift. IDs 11/12 are outside the chosen ten-ID simulation, so their absence is not verified missing telemetry. Confidential external portal/billing evidence is unavailable by design; retain clear author-attested definitions and assumptions without requesting or publishing it.

The original workbook contains customer/service records and listed plan amounts/periods. The author identifies amounts as relating to those periods; currency remains undisclosed. This supports reported-period descriptions, not billed/recognized revenue. The separate network plan-tier prices must not be substituted for actual customer billing. Fifteen account keys have 71 synthetic account-days preceding original activation under source-order mapping; arbitrary simulation dates do not establish actual pre-activation usage.

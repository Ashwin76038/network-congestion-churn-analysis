# Simulation scope and interpretation

The project author confirms on 1 October 2026 that operational network logs were unavailable. Usage volume, average speed, downtime and latency were generated with random Excel values. The author used ten OLT IDs and chose five dates as a manageable demonstration. Customer IDs were filled down sequentially. This statement establishes simulation provenance; the original formulas, ranges and random seed were not supplied.

The frozen sample contains 1,280 row-labeled accounts, 6,400 synthetic account-days over 1-5 August 2026 and 50 synthetic OLT-days. Customer metadata derives from the privately supplied original customer workbook. Its 12 distinct OLT-address groups are not a verified count of physical OLT devices and do not become the same entities as the ten simulated usage IDs merely because numeric labels overlap.

## Supported work

- Reproduce pandas/SQL calculations and preserve account-day/OLT-day grains.
- Demonstrate decimal GB-to-Gbps conversion and ratios against scenario capacity inputs.
- Check whether separately created dimensions/facts can be joined without misleading attribution.
- Test as-of complaint windows and the complete two-window usage-change gate.
- Show simulation outputs in a report clearly marked **Simulated data**.

The 1,135 assigned-versus-simulated OLT disagreements and absent usage IDs 11/12 are compatibility/scope findings. They are not observed network collection failures, customer migrations or infrastructure defects. The 71 dates preceding original customer activation similarly describe mixed real-metadata/simulation chronology, not actual traffic before service began.

## Limits and reproduction

The original Excel random generation is not exactly reproducible without its formula definitions and frozen random state. The committed CSV inputs are fixed: metric builds, tests and audits can be reproduced from those values. A future seeded generator would be a separately labeled simulation and must not be described as recreating the original Excel sample unless verified.

Five days cannot satisfy the current rule's two complete, disjoint seven-day windows. Keep full scores blank, not zero. A 14-day demonstration for 1,280 accounts would contain 17,920 account-days; no extra records were created in this review. Longer synthetic data can test rule behavior but cannot establish model accuracy, churn outcomes or real operating impact.

Capacities, plan tiers, scoring weights and thresholds are scenario assumptions unless a specific source definition is available. Customer plan amounts can be described with their supplied periods; confidential bills/portal documents are not required for this scoped demonstration and will not be published. Currency and financial recognition remain outside the claims.

The approved Power BI project now contains refreshed simulation/readiness pages and separate assigned/logged OLT roles. Native DAX and visual checks are documented in `powerbi_validation.md`. Exact customer activation dates are withheld; historical discrepancy flags remain. No synthetic extra days were added.

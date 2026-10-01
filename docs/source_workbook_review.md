# Original customer workbook reconciliation

On 1 October 2026, the project author supplied the original workbook privately and confirmed that **Activation Date means the date the customer's internet plan/service was activated**. The author states that the same workbook underlies both projects and identifies its source as a confidential government platform. Network usage was separately generated with random Excel values using ten OLT IDs, sequential customer IDs and five chosen dates. Portal/billing documentation remains confidential; no disclosure is required for the scoped simulation.

The original has 1,320 service rows. Filtering `Sub Service Type = BHARAT FIBER COMBO` yields 1,280 rows, 12 OLT groups and 1,193 customer-label groups after trimming, lowercasing and collapsing whitespace. The 40 excluded rows belong to other service types. All 1,280 status mappings, OLT group numbers and generated account positions corroborate the current customer-table row order. The separate OLT project additionally matches all fees, plan names and customer groups.

| Evidence | Original selected rows | Current public customer table |
|---|---|---|
| Activation range | 1999-02-15 through 2026-08-29 | 2025-06-04 through 2028-11-30 |
| Dates after configured OLT cutoff 2026-09-12 | 0 | 810 |
| Positional activation comparison | 5 dates match | 1,275 differ from source |
| Scenario dates preceding original activation | 15 account keys / 71 synthetic account-days under corroborated row-order mapping | Mixed-source chronology, not actual pre-activation traffic |

Both repositories share the same public activation-date sequence. The transformation responsible for those customer-date discrepancies is unknown. The source-order comparison is not a stable source-service-ID join. A/D/E business meanings and actual source snapshot date remain undisclosed; current mappings/cutoff are analytical assumptions. Because usage dates are synthetic, the pre-activation comparison is a scenario compatibility check and provides no evidence of actual source-system faults.

## Reproduce privately

```bash
python scripts/reconcile_source_workbook.py --source /private/path/original.xlsx
```

Optional `--output docs/source_workbook_receipt.json` saves aggregate evidence only. The script never writes raw rows, names, emails, addresses, OLT addresses, corrected datasets or Power BI files. A public clone cannot rerun this source comparison without private access to the workbook. The committed aggregate receipt records the comparison already executed.

Executed: the original-workbook comparison above and 12/12 unit tests passed, including day-first parsing, invalid-date rejection and refusal to force positional date matches when source scope differs. Existing public SQL validation passed eight queries in the earlier data-readiness review; no SQL metric code changed in this source comparison. Desktop/DAX execution remains pending.

## Remaining data and report work

The customer workbook does not extend the five-day simulation. The origin of usage is now author-confirmed as random Excel generation; its ten-ID OLT scope differs from source-address groups. Keep the two complete seven-day windows requirement and unavailable-risk behavior. Source-date restoration needs documented mapping, privacy review and an explicitly labeled analysis reference date if the actual snapshot date remains confidential. Refresh copied dashboard inputs and validate the PBIP after the user's Power BI approval. Keep raw contacts, workbook and screenshot outside Git.

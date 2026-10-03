# Before / after review

| Area | Earlier deliverable | Current deliverable |
|---|---|---|
| Usage provenance | Unresolved source/observed-sample implication | Author-confirmed Excel random simulation |
| Dates / account-days | Five / 6,400 | Unchanged; no extra days generated |
| Complete risk rows | Zero after pipeline correction | Zero; DAX full risk and high-risk share explicitly tested blank |
| Assigned/logged mismatch | 1,135 accounts | Unchanged, 88.67%; separate model roles, interpreted as scenario compatibility |
| OLT coverage | Ten of 12 numeric labels | Ten simulated IDs versus 12 source-address groups; 11/12 outside scenario scope |
| Mean daily-average ratio | 9.83% | Same arithmetic, explicitly synthetic and capacity-assumed; no peak claim |
| Prepared activation dates | 1,275 disagreements, 810 future flags | All 1,280 dates withheld; historical flags preserved |
| Power BI | Stale risk-oriented model/report | Three refreshed simulation/readiness pages; 133/133 native DAX checks |
| SQL platform evidence | SQLite supplementary audits; MySQL author-reported | Twelve native MySQL 8.0.46 checks plus supplementary SQLite checks |

Fifteen Python tests cover temporal windows, gaps, zero prior usage, future complaints, units, keys, privacy of dates and model-copy/OLT-role consistency. All pages and a logged-OLT slicer/reset were inspected in Desktop. See `powerbi_validation.md` for executed details and limits.

The original-source chronology comparison (71 synthetic days across 15 keys preceding activation) is a scenario check, not actual traffic. No label/outcome or business-impact claim is supported. Creation-chat advice is not empirical evidence.

# SQL engines

The author used **MySQL**. On 2 October 2026, MySQL 8.0.46 executed 12 public-data checks, reconciled against pandas: accounts/days/OLTs, mapping conflicts, scored rows, complete calendar windows, mean ratio, independently rebuilt units, complaints and withheld dates. See `mysql_validation.json` and `sql/mysql_kpi_queries.sql`.

```bash
python scripts/validate_mysql.py --client mysql --schema portfolio_audit_network_new -- --host=127.0.0.1 --port=3306 --user=YOUR_USER
```

Use your authorized instance and existing secure client credential configuration. The schema must be new; the validator does not drop or overwrite existing schemas. The window query requires MySQL 8 and uses TO_DAYS with calendar RANGE frames. This validates these audit queries, not undisclosed original project SQL.

`sql/queries.sql`, `scripts/validate_sql.py` and public audits remain separately labeled **SQLite** checks (eight queries). Native DAX/visual results are recorded separately in `powerbi_validation.md`.

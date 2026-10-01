# SQL engine and executed checks

The project author confirms using **MySQL** for the original project. The original MySQL workflow has not been executed in this review.

The added `sql/queries.sql`, `scripts/validate_sql.py` and public audit use **SQLite** for independent reconciliation of the frozen public scenario. Eight queries passed in that engine. These results do not establish MySQL execution, DAX behavior or Desktop rendering.

`queries.sql` explicitly uses SQLite date functions such as `julianday`. It must not be labeled an executed MySQL query file. A MySQL reproduction requires a separate engine-compatible version and a native run; no such run is claimed here.

For interview descriptions: “I used MySQL in the project. Additional Python/SQLite checks reconcile the simulated sample; native MySQL and Power BI execution checks are separately pending.”

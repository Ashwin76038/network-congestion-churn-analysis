from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
db=sqlite3.connect(':memory:')
for p in (ROOT/'data/clean').glob('*.csv'):pd.read_csv(p).to_sql(p.stem,db,index=False)
queries=[q.strip() for q in '\n'.join(line for line in (ROOT/'sql/queries.sql').read_text().splitlines() if not line.lstrip().startswith('--')).split(';') if q.strip()]
results=[db.execute(q).fetchall() for q in queries]
assert results[0][0][0]==1280
assert sum(row[1] for row in results[1])==1280
assert len(results[2])==6400, 'Join multiplied/dropped account-days'
assert all(row[2] is None for row in results[3]), 'Five days cannot support two seven-day windows'
print(f'{len(results)} SQL queries executed; grain, exclusive risk counts, join size and missing-history checks passed.')

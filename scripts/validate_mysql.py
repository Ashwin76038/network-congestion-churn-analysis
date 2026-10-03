"""Load public CSVs into a task-owned MySQL schema and reconcile headline KPIs.

Requires a MySQL 8 client and user-provided connection arguments. Never reads
private source files or alters an existing schema; schema names must be new.
"""
import argparse, json, subprocess, tempfile
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
def validate(client, connection, schema):
    if not schema.replace('_','').isalnum() or not schema.startswith('portfolio_audit_'):
        raise ValueError('Use a fresh portfolio_audit_ schema')
    model=ROOT/'data/clean'
    tables={p.stem:pd.read_csv(p) for p in model.glob('*.csv')}
    queries={
      'accounts':'SELECT COUNT(*) FROM customers_clean',
      'account_days':'SELECT COUNT(*) FROM usage_logs_clean',
      'scenario_days':'SELECT COUNT(DISTINCT log_date) FROM usage_logs_clean',
      'logged_olts':'SELECT COUNT(DISTINCT olt_id) FROM usage_logs_clean',
      'assigned_groups':'SELECT COUNT(*) FROM olt_info_clean',
      'mismatch_accounts':'SELECT COUNT(DISTINCT u.customer_id) FROM usage_logs_clean u JOIN customers_clean c USING(customer_id) WHERE u.olt_id<>c.olt_id',
      'scored_rows':'SELECT COUNT(churn_risk_score) FROM customer_daily_metrics',
      'complete_windows':"SELECT COUNT(*) FROM (SELECT customer_id,log_date,COUNT(*) OVER (PARTITION BY customer_id ORDER BY TO_DAYS(log_date) RANGE BETWEEN 13 PRECEDING AND CURRENT ROW) AS n14,SUM(data_usage_gb) OVER (PARTITION BY customer_id ORDER BY TO_DAYS(log_date) RANGE BETWEEN 13 PRECEDING AND 7 PRECEDING) AS prior_usage FROM usage_logs_clean) w WHERE n14=14 AND prior_usage>0",
      'mean_ratio':'SELECT AVG(congestion_ratio) FROM olt_daily_metrics',
      'ratio_max_error':'SELECT MAX(ABS(n.congestion_ratio-(u.gb*8/86400/o.capacity_gbps))) FROM olt_daily_metrics n JOIN (SELECT olt_id,log_date,SUM(data_usage_gb) gb FROM usage_logs_clean GROUP BY olt_id,log_date) u USING(olt_id,log_date) JOIN logged_olt o USING(olt_id)',
      'complaints':'SELECT COUNT(*) FROM complaints',
      'withheld_dates':'SELECT SUM(activation_date_withheld_flag) FROM customers_clean',
    }
    c=tables['customers_clean'];u=tables['usage_logs_clean'];m=tables['customer_daily_metrics'];n=tables['olt_daily_metrics']
    j=u.merge(c[['customer_id','olt_id']],on='customer_id',suffixes=('_logged','_assigned'),validate='many_to_one')
    expected={'accounts':len(c),'account_days':len(u),'scenario_days':u.log_date.nunique(),'logged_olts':u.olt_id.nunique(),'assigned_groups':len(tables['olt_info_clean']),'mismatch_accounts':j.loc[j.olt_id_logged.ne(j.olt_id_assigned),'customer_id'].nunique(),'scored_rows':int(m.churn_risk_score.notna().sum()),'complete_windows':int(m.usage_window_complete.sum()),'mean_ratio':float(n.congestion_ratio.mean()),'ratio_max_error':0,'complaints':len(tables['complaints']),'withheld_dates':int(c.activation_date_withheld_flag.sum())}
    sql=f'CREATE DATABASE `{schema}`; USE `{schema}`;\n'
    for name,df in tables.items():
        cols=','.join(f'`{c}` '+('DOUBLE' if pd.api.types.is_numeric_dtype(df[c]) else 'TEXT') for c in df)
        sql+=f'CREATE TABLE `{name}` ({cols});\n'
        def cell(v):
            if pd.isna(v):return 'NULL'
            if isinstance(v,bool):return '1' if v else '0'
            if isinstance(v,(int,float)):return str(v)
            return "'"+str(v).replace('\\','\\\\').replace("'","''")+"'"
        for start in range(0,len(df),250):
            sql+=f'INSERT INTO `{name}` VALUES '+','.join('('+','.join(cell(v) for v in row)+')' for row in df.iloc[start:start+250].itertuples(index=False,name=None))+';\n'
    sql+='SELECT VERSION();\n'+''.join(f'SELECT "{k}", ({q});\n' for k,q in queries.items())
    run=subprocess.run([client,*connection,'--batch','--skip-column-names'],input=sql,text=True,capture_output=True)
    if run.returncode:raise RuntimeError(run.stderr)
    lines=run.stdout.strip().splitlines();actual={k:float(v) for k,v in (l.split('\t') for l in lines[1:])}
    for k,v in expected.items():
        if abs(actual[k]-v)>1e-9:raise ValueError(f'MySQL/Python mismatch for {k}')
    receipt={'engine':'MySQL','version':lines[0],'checks':len(queries),'status':'passed','actual':actual,'limit':'native MySQL checks of these public aggregates; no original private MySQL workflow or Power BI validation implied'}
    (ROOT/'docs/mysql_validation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    (ROOT/'sql/mysql_kpi_queries.sql').write_text('-- MySQL 8: run against the loaded public model tables.\n'+''.join(f'-- {k}\n{q};\n' for k,q in queries.items()),encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--client',required=True);p.add_argument('--schema',required=True);p.add_argument('connection',nargs=argparse.REMAINDER);a=p.parse_args();validate(a.client,a.connection[1:] if a.connection[:1]==['--'] else a.connection,a.schema)

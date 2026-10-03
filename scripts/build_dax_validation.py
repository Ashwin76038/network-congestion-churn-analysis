"""Independent pandas expectations for native DAX, including distinct OLT roles."""
from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def build():
    d=ROOT/'data/clean'
    c=pd.read_csv(d/'customers_clean.csv');m=pd.read_csv(d/'customer_daily_metrics.csv');u=pd.read_csv(d/'usage_logs_clean.csv');n=pd.read_csv(d/'olt_daily_metrics.csv');q=pd.read_csv(d/'complaints.csv');o=pd.read_csv(d/'olt_info_clean.csv')
    contexts=[('All',{}),('Assigned 1',{'assigned':1}),('Logged 9',{'logged':9}),('Basic',{'tier':'Basic'}),('First day',{'date':'2026-08-01'}),('Assigned 11',{'assigned':11}),('Combined',{'assigned':1,'logged':9,'date':'2026-08-03'})]
    cases=[]
    for label,f in contexts:
        cs=c.copy();ns=n.copy();os=o.copy();qs=q.copy();pred=[]
        if 'assigned' in f:
            cs=cs[cs.olt_id.eq(f['assigned'])];os=os[os.olt_id.eq(f['assigned'])]
            pred.append(f'TREATAS({{{f["assigned"]}}},olt_info_clean[olt_id])')
        if 'tier' in f:
            cs=cs[cs.plan_tier.eq(f['tier'])];pred.append(f'TREATAS({{{json.dumps(f["tier"])}}},customers_clean[plan_tier])')
        ms=m[m.customer_id.isin(cs.customer_id)];us=u[u.customer_id.isin(cs.customer_id)];qs=qs[qs.customer_id.isin(cs.customer_id)]
        if 'logged' in f:
            ms=ms[ms.olt_id.eq(f['logged'])];us=us[us.olt_id.eq(f['logged'])];ns=ns[ns.olt_id.eq(f['logged'])]
            pred.append(f'TREATAS({{{f["logged"]}}},logged_olt[olt_id])')
        if 'date' in f:
            ms=ms[ms.log_date.eq(f['date'])];us=us[us.log_date.eq(f['date'])];ns=ns[ns.log_date.eq(f['date'])];qs=qs[qs.complaint_date.eq(f['date'])]
            y,mo,dy=f['date'].split('-');pred.append(f'TREATAS({{DATE({int(y)},{int(mo)},{int(dy)})}},DateTable[Date])')
        # Date dimension is restricted to the actual five scenario dates.
        qs=qs[qs.complaint_date.between('2026-08-01','2026-08-05')] if 'date' in f else qs
        joined=us.merge(c[['customer_id','olt_id']],on='customer_id',suffixes=('_logged','_assigned'),validate='many_to_one')
        mismatch=joined.loc[joined.olt_id_logged.ne(joined.olt_id_assigned),'customer_id'].nunique()
        accounts=ms.customer_id.nunique()
        val={'Service Accounts':accounts or None,'Account Days':len(ms) or None,'Scenario Days':ms.log_date.nunique() or None,'Experience Score':float(ms.experience_score.mean()) if len(ms) else None,'Daily Average Ratio':float(ns.congestion_ratio.mean()) if len(ns) else None,'Simulated OLTs':ns.olt_id.nunique() or None,'Source OLT Groups':len(os) or None,'Scored Accounts':int(ms.loc[ms.churn_risk_score.notna(),'customer_id'].nunique()),'High Risk Accounts':None,'High Risk Share':None,'Risk Score':None,'Complete Window Rows':int(ms.usage_window_complete.sum()),'Mismatch Accounts':int(mismatch),'Mismatch Share':float(mismatch/accounts) if accounts else None,'Total Usage GB':float(us.data_usage_gb.sum()) if len(us) else None,'Average Downtime Minutes':float(ms.downtime_minutes.mean()) if len(ms) else None,'Average Latency Ms':float(ms.latency_ms.mean()) if len(ms) else None,'Leakage Accounts':int(ms.loc[ms.complaint_leakage_flag.eq(1),'customer_id'].nunique()),'Synthetic Complaint Events':len(qs) or None}
        for name,value in val.items():
            expr='['+name+']'
            if pred:expr='CALCULATE('+expr+','+','.join(pred)+')'
            cases.append({'check':label+' / '+name,'expression':expr,'expected':value})
    rows=[]
    for case in cases:
        e=case['expression'];v=case['expected'];condition=f'ISBLANK({e})' if v is None else f'NOT ISBLANK({e}) && ABS({e}-({v}))<0.0000001'
        rows.append('ROW("Check",'+json.dumps(case['check'])+',"Passed",'+condition+')')
    (ROOT/'docs/validate_measures.dax').write_text('DEFINE\n VAR Checks = UNION(\n'+',\n'.join(rows)+'\n)\nEVALUATE ROW("Checks",COUNTROWS(Checks),"Passed",COUNTROWS(FILTER(Checks,[Passed])),"Failures",CONCATENATEX(FILTER(Checks,NOT [Passed]),[Check],"; "))\n')
    (ROOT/'docs/dax_validation_cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(f'Generated {len(cases)} expectations; execute separately in Desktop.')
if __name__=='__main__':build()

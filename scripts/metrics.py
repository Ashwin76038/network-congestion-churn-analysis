"""Public-data metrics with complete time windows and as-of complaint counts."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def add_scores(frame):
    out=frame.copy()
    for field in ['data_usage_gb','avg_speed_mbps','downtime_minutes','latency_ms']:
        v=pd.to_numeric(out[field],errors='raise')
        if v.isna().any() or not np.isfinite(v).all() or v.lt(0).any(): raise ValueError(f'Invalid measurement: {field}')
        out[field]=v
    out['speed_score']=np.select([out.avg_speed_mbps>=100,out.avg_speed_mbps>=50,out.avg_speed_mbps>=20],[100,75,50],default=25)
    out['downtime_score']=np.select([out.downtime_minutes<=10,out.downtime_minutes<=30,out.downtime_minutes<=60],[100,75,50],default=25)
    out['latency_score']=np.select([out.latency_ms<=30,out.latency_ms<=60,out.latency_ms<=100],[100,75,50],default=25)
    out['experience_score']=.5*out.speed_score+.3*out.downtime_score+.2*out.latency_score
    return out

def build_customer_metrics(usage,complaints):
    out=add_scores(usage)
    out['log_date']=pd.to_datetime(out.log_date,errors='raise').dt.normalize()
    if out[['customer_id','log_date']].isna().any().any() or out.duplicated(['customer_id','log_date']).any(): raise ValueError('Invalid account/date key')
    out=out.sort_values(['customer_id','log_date']).reset_index(drop=True)
    counts=complaints.copy()
    counts['complaint_date']=pd.to_datetime(counts.complaint_date,errors='raise').dt.normalize()
    if counts[['complaint_id','customer_id','complaint_date']].isna().any().any() or counts.complaint_id.duplicated().any(): raise ValueError('Invalid complaint key/date')
    if not counts.customer_id.isin(out.customer_id).all(): raise ValueError('Orphan complaint account')
    out['current_7d_avg']=np.nan;out['previous_7d_avg']=np.nan
    out['complaint_count']=0;out['complaint_count_30d']=0
    for cid,g in out.groupby('customer_id',sort=False):
        s=g.set_index('log_date').data_usage_gb
        calendar=s.reindex(pd.date_range(s.index.min(),s.index.max(),freq='D'))
        current=calendar.rolling(7,min_periods=7).mean()
        previous=current.shift(7)
        out.loc[g.index,'current_7d_avg']=current.reindex(g.log_date).to_numpy()
        out.loc[g.index,'previous_7d_avg']=previous.reindex(g.log_date).to_numpy()
        dates=counts.loc[counts.customer_id.eq(cid),'complaint_date'].sort_values().to_numpy()
        upper=np.searchsorted(dates,g.log_date.to_numpy(),side='right')
        lower=np.searchsorted(dates,g.log_date.to_numpy()-np.timedelta64(30,'D'),side='right')
        out.loc[g.index,'complaint_count']=upper
        out.loc[g.index,'complaint_count_30d']=upper-lower
    out['usage_drop_percent']=(out.previous_7d_avg-out.current_7d_avg)/out.previous_7d_avg.where(out.previous_7d_avg.gt(0))*100
    out['usage_window_complete']=out.current_7d_avg.notna() & out.previous_7d_avg.gt(0)
    out['high_usage_drop_flag']=out.usage_drop_percent.ge(30).astype(int)
    out['high_downtime_flag']=out.downtime_minutes.gt(20).astype(int)
    out['high_latency_flag']=out.latency_ms.gt(40).astype(int)
    out['low_experience_flag']=out.experience_score.lt(50).astype(int)
    out['complaint_leakage_flag']=(out.experience_score.lt(50)&out.complaint_count_30d.eq(0)).astype(int)
    out['risk_observed_component_score']=30*out.high_usage_drop_flag+25*out.high_downtime_flag+20*out.high_latency_flag+15*out.low_experience_flag+10*out.complaint_leakage_flag
    out['churn_risk_score']=out.risk_observed_component_score.where(out.usage_window_complete).astype('Int64')
    out['churn_risk_category']=pd.cut(out.churn_risk_score.astype(float),[-1,39,69,100],labels=['Low Risk','Medium Risk','High Risk']).astype('string').fillna('Insufficient history')
    out['log_date']=out.log_date.dt.strftime('%Y-%m-%d')
    return out

def build_olt_metrics(usage,olts):
    if olts.olt_id.isna().any() or olts.olt_id.duplicated().any(): raise ValueError('Invalid OLT key')
    out=usage.groupby(['olt_id','log_date'],as_index=False).data_usage_gb.sum().rename(columns={'data_usage_gb':'total_usage_gb'})
    out=out.merge(olts[['olt_id','capacity_gbps']],on='olt_id',how='left',validate='many_to_one')
    if out.capacity_gbps.isna().any() or not np.isfinite(out.capacity_gbps).all() or out.capacity_gbps.le(0).any(): raise ValueError('Missing/invalid capacity')
    out['avg_gbps']=out.total_usage_gb*8/86400
    out['congestion_ratio']=out.avg_gbps/out.capacity_gbps
    out['congestion_ratio_percent']=out.congestion_ratio # compatibility field: DECIMAL, formatted as percent in Power BI
    out['congestion_status']=np.select([out.congestion_ratio.lt(.6),out.congestion_ratio.le(.8)],['Healthy','Moderate'],default='High')
    return out

def main():
    data=ROOT/'data/clean'
    u=pd.read_csv(data/'usage_logs_clean.csv');c=pd.read_csv(data/'customers_clean.csv');o=pd.read_csv(data/'olt_info_clean.csv');q=pd.read_csv(data/'complaints.csv')
    if c.customer_id.duplicated().any() or not u.customer_id.isin(c.customer_id).all(): raise ValueError('Invalid account join')
    m=build_customer_metrics(u,q);n=build_olt_metrics(u,o)
    for folder in [data,ROOT/'dashboard/OLT_Professional_Project/data']:
        m.to_csv(folder/'customer_daily_metrics.csv',index=False,lineterminator='\n');n.to_csv(folder/'olt_daily_metrics.csv',index=False,lineterminator='\n')
    ids=pd.read_csv(ROOT/'data/sample/customers_sample.csv').customer_id
    m[m.customer_id.isin(ids)].to_csv(ROOT/'data/sample/customer_daily_metrics_sample.csv',index=False)
    joined=u.merge(c[['customer_id','olt_id']],on='customer_id',suffixes=('_logged','_assigned'),validate='many_to_one')
    evidence=dict(service_accounts=len(c),daily_observations=len(m),date_start=m.log_date.min(),date_end=m.log_date.max(),days=m.log_date.nunique(),olts_total=len(o),olts_observed=n.olt_id.nunique(),mean_daily_utilization=n.congestion_ratio.mean(),mean_experience_score=m.experience_score.mean(),complete_risk_rows=int(m.usage_window_complete.sum()),high_risk_accounts=None if not m.usage_window_complete.any() else int(m.loc[m.churn_risk_category.eq('High Risk'),'customer_id'].nunique()),complaint_leakage_accounts=int(m.loc[m.complaint_leakage_flag.eq(1),'customer_id'].nunique()),assigned_logged_olt_mismatch_accounts=int(joined.loc[joined.olt_id_logged.ne(joined.olt_id_assigned),'customer_id'].nunique()))
    (ROOT/'docs/validated_metrics.json').write_text(json.dumps(evidence,indent=2,default=int))
    print(json.dumps(evidence,indent=2,default=int))
if __name__=='__main__':main()

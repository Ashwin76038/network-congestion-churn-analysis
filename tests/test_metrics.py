import sys,unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from metrics import build_customer_metrics,build_olt_metrics,add_scores
class MetricsTests(unittest.TestCase):
 def usage(self):
  return pd.DataFrame(dict(customer_id=['demo']*14,olt_id=[1]*14,log_date=pd.date_range('2026-01-01',periods=14),data_usage_gb=[100]*7+[50]*7,avg_speed_mbps=[99.5]*14,downtime_minutes=[10.5]*14,latency_ms=[30.5]*14))
 def complaints(self):return pd.DataFrame(dict(complaint_id=['c1'],customer_id=['demo'],complaint_date=['2026-01-14']))
 def test_windows(self):
  m=build_customer_metrics(self.usage(),self.complaints());self.assertTrue(m.churn_risk_score.iloc[:13].isna().all());self.assertEqual(m.usage_drop_percent.iloc[-1],50)
 def test_future_complaint(self):
  m=build_customer_metrics(self.usage(),self.complaints());self.assertEqual(m.complaint_count.iloc[0],0);self.assertEqual(m.complaint_count.iloc[-1],1)
 def test_missing_day(self):self.assertTrue(build_customer_metrics(self.usage().drop(index=3),self.complaints()).churn_risk_score.isna().all())
 def test_zero_prior_usage_has_no_defined_percentage_or_full_risk(self):
  u=self.usage();u.loc[:6,'data_usage_gb']=0
  m=build_customer_metrics(u,self.complaints())
  self.assertTrue(m.churn_risk_score.isna().all());self.assertTrue(m.usage_drop_percent.isna().all())
 def test_fractional_boundaries(self):
  m=add_scores(self.usage());self.assertEqual(list(m[['speed_score','downtime_score','latency_score']].iloc[0]),[75,75,75])
 def test_duplicates(self):
  u=self.usage()
  with self.assertRaises(ValueError):build_customer_metrics(pd.concat([u,u.iloc[:1]]),self.complaints())
 def test_ratio(self):
  u=self.usage().iloc[:1].copy();u['data_usage_gb']=10800;o=pd.DataFrame(dict(olt_id=[1],capacity_gbps=[1]));self.assertEqual(build_olt_metrics(u,o).congestion_ratio_percent.iloc[0],1)
  o['capacity_gbps']=0
  with self.assertRaises(ValueError):build_olt_metrics(u,o)
if __name__=='__main__':unittest.main()

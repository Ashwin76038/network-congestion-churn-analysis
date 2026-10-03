import unittest
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
class ReportInputs(unittest.TestCase):
    def test_report_copies_and_withheld_dates(self):
        project=ROOT/'dashboard/OLT_Professional_Project'
        for path in (ROOT/'data/clean').glob('*.csv'):
            copy=project/'data'/path.name
            if copy.exists():pd.testing.assert_frame_equal(pd.read_csv(path),pd.read_csv(copy))
        c=pd.read_csv(project/'data/customers_clean.csv')
        self.assertTrue(c.activation_date.isna().all())
        self.assertEqual(int(c.activation_date_withheld_flag.sum()),1280)

    def test_olt_roles_do_not_force_assignment_onto_network_fact(self):
        project=ROOT/'dashboard/OLT_Professional_Project'
        relations=(project/'OLT.SemanticModel/definition/relationships.tmdl').read_text()
        for relation in relations.split('relationship ')[1:]:
            if 'fromColumn: olt_daily_metrics.olt_id' in relation:
                self.assertIn('toColumn: logged_olt.olt_id',relation)
                self.assertNotIn('toColumn: olt_info_clean',relation)
        logged=pd.read_csv(project/'data/logged_olt.csv')
        usage=pd.read_csv(project/'data/usage_logs_clean.csv')
        self.assertFalse(logged.olt_id.duplicated().any())
        self.assertEqual(set(logged.olt_id),set(usage.olt_id))
        self.assertEqual(len(logged),10)

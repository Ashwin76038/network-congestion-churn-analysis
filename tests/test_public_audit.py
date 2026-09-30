"""Regression checks for public data-readiness claims."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_public import audit  # noqa: E402


class PublicAuditTests(unittest.TestCase):
    def test_receipt_recomputes_from_committed_tables(self):
        current = audit()
        saved = json.loads((ROOT / "docs/data_readiness_receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(current, saved)
        self.assertEqual(current["account_days"], 6400)
        self.assertEqual(current["complete_14_day_window_rows"], 0)
        self.assertEqual(current["full_risk_score_rows"], 0)
        self.assertEqual(current["assigned_logged_mismatched_accounts"], 1135)
        self.assertEqual(current["missing_logged_olt_ids"], [11, 12])

    def test_missing_risk_is_not_reported_as_zero_high_risk(self):
        metrics = pd.read_csv(ROOT / "data/clean/customer_daily_metrics.csv")
        self.assertTrue(metrics.churn_risk_score.isna().all())
        self.assertTrue(metrics.churn_risk_category.eq("Insufficient history").all())
        self.assertEqual(int(metrics.usage_window_complete.fillna(False).sum()), 0)

    def test_audit_rejects_wrong_capacity_ratio(self):
        real_read_csv = pd.read_csv

        def corrupt_network(path, *args, **kwargs):
            frame = real_read_csv(path, *args, **kwargs)
            if Path(path).name == "olt_daily_metrics.csv":
                frame.loc[0, "congestion_ratio"] += 0.01
            return frame

        with patch("audit_public.pd.read_csv", side_effect=corrupt_network):
            with self.assertRaisesRegex(ValueError, "does not reconcile"):
                audit()


if __name__ == "__main__":
    unittest.main()

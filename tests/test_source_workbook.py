"""Guard the source date interpretation and uncertain row linkage."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reconcile_source_workbook import parse_activation, reconcile


class SourceWorkbookTests(unittest.TestCase):
    def test_ambiguous_day_month_is_parsed_day_first(self):
        dates = parse_activation(pd.Series(["08/03/2017 00:00:00", "14/06/2025 10:38:21"]))
        self.assertEqual(dates.dt.strftime("%Y-%m-%d").tolist(), ["2017-03-08", "2025-06-14"])

    def test_invalid_source_date_cannot_be_silently_replaced(self):
        with self.assertRaisesRegex(ValueError, "no date inferred"):
            parse_activation(pd.Series(["31/02/2026 00:00:00"]))

    def test_different_source_scope_does_not_force_date_alignment(self):
        source = pd.DataFrame({"Sub Service Type": ["BHARAT FIBER COMBO"], "Customer": ["Private fixture"], "OLT IP": ["private-fixture"], "Activation Date": ["14/06/2025 00:00:00"], "Status": ["A"], "FMC": [1], "Subscription Plan": ["Fixture"]})
        with patch("reconcile_source_workbook.pd.read_excel", return_value=source):
            result = reconcile(Path("not-read.xlsx"))
        self.assertFalse(result["row_order_corroborated"])
        self.assertIsNone(result["positional_activation_mismatches"])
        self.assertNotIn("Private fixture", str(result))
        self.assertFalse(result["public_data_changed"])


if __name__ == "__main__":
    unittest.main()

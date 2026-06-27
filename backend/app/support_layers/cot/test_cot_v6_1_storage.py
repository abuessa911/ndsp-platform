import tempfile
import unittest
from pathlib import Path

from app.support_layers.cot.cftc_auto_provider import CftcAutoProvider
from app.support_layers.cot.cot_engine import CotIntelligenceEngine
from app.support_layers.cot.cot_storage import CotStorage


class TestCotV61Storage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "cot_storage.json"
        self.storage = CotStorage(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def test_auto_snapshot_can_be_saved(self):
        CftcAutoProvider(self.storage).seed_auto_demo("EURUSD")
        record = self.storage.get_latest_record("EURUSD")

        self.assertIsNotNone(record)
        self.assertEqual(record["active_source"], "AUTO_CFTC")
        self.assertFalse(record["execution_allowed"])
        self.assertEqual(record["net_formula"], "net = long - short")

    def test_manual_override_wins_over_auto(self):
        CftcAutoProvider(self.storage).seed_auto_demo("EURUSD")

        self.storage.save_snapshot(
            symbol="EURUSD",
            report_date="2026-05-12",
            positions=[
                {"category": "institutional direction/Institutional", "long": 200000, "short": 100000},
                {"category": "market activity", "long": 50000, "short": 30000},
                {"category": "market momentum", "long": 70000, "short": 95000},
                {"category": "Dealer/Intermediary", "long": 60000, "short": 80000},
            ],
            source="operator_manual_entry",
            source_type="manual_override",
        )

        record = self.storage.get_latest_record("EURUSD")

        self.assertEqual(record["active_source"], "MANUAL_OVERRIDE")
        self.assertEqual(record["source_type"], "manual_override")
        self.assertFalse(record["execution_allowed"])

    def test_clear_manual_override_returns_to_auto(self):
        CftcAutoProvider(self.storage).seed_auto_demo("EURUSD")

        self.storage.save_snapshot(
            symbol="EURUSD",
            report_date="2026-05-12",
            positions=[
                {"category": "institutional direction/Institutional", "long": 200000, "short": 100000},
                {"category": "market activity", "long": 50000, "short": 30000},
            ],
            source="operator_manual_entry",
            source_type="manual_override",
        )

        self.assertEqual(self.storage.get_latest_record("EURUSD")["active_source"], "MANUAL_OVERRIDE")

        cleared = self.storage.clear_manual_override("EURUSD")
        self.assertTrue(cleared)

        self.assertEqual(self.storage.get_latest_record("EURUSD")["active_source"], "AUTO_CFTC")

    def test_snapshot_evaluates_through_existing_cot_engine(self):
        CftcAutoProvider(self.storage).seed_auto_demo("XAUUSD")
        snapshot = self.storage.get_latest_snapshot("XAUUSD")

        result = CotIntelligenceEngine().evaluate(snapshot)

        self.assertEqual(result.symbol, "XAUUSD")
        self.assertTrue(result.context_only)
        self.assertFalse(result.execution_allowed)


if __name__ == "__main__":
    unittest.main()

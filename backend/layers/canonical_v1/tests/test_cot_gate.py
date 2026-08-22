from datetime import datetime, timezone
import unittest
from backend.layers.canonical_v1.data.cot_validity_gate import ExpectedCotCycle, LatestCotReport, evaluate_cot_validity
from backend.layers.canonical_v1.core.contracts import DataGateStatus

class TestCotGate(unittest.TestCase):
    def test_missing_report_after_due_is_blocked(self):
        result=evaluate_cot_validity(
            now=datetime(2026,7,13,8,tzinfo=timezone.utc),
            expected_cycle=ExpectedCotCycle("2026-07-07",datetime(2026,7,10,19,30,tzinfo=timezone.utc)),
            latest_report=None,
        )
        self.assertEqual(result.status,DataGateStatus.EXPECTED_REPORT_MISSING)
        self.assertFalse(result.decision_use_allowed)

    def test_stale_previous_cycle_is_blocked(self):
        result=evaluate_cot_validity(
            now=datetime(2026,7,13,8,tzinfo=timezone.utc),
            expected_cycle=ExpectedCotCycle("2026-07-07",datetime(2026,7,10,19,30,tzinfo=timezone.utc)),
            latest_report=LatestCotReport("2026-06-30",True,frozenset({"BTCUSDT"})),
        )
        self.assertEqual(result.status,DataGateStatus.STALE)

if __name__ == "__main__":
    unittest.main()

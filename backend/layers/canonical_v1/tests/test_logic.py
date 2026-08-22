import unittest
from backend.layers.canonical_v1.direction.investment_policy import evaluate_investment_policy
from backend.layers.canonical_v1.direction.speculative_policy import evaluate_speculative_policy
from backend.layers.canonical_v1.quality.golden_signals import evaluate_golden_signals
from backend.layers.canonical_v1.quality.nmp_engine import calculate_nmp

class TestLogic(unittest.TestCase):
    def test_investment_direction_and_correction(self):
        result = evaluate_investment_policy(
            asset_managers_overall="bullish",
            asset_managers_weekly="bearish",
            leveraged_funds_weekly="bearish",
        )
        self.assertEqual(result["governing_direction"],"bullish")
        self.assertFalse(result["readiness_allowed"])
        self.assertEqual(result["correction_state"],"active")

    def test_lf_weekly_is_stability_not_direction(self):
        result = evaluate_investment_policy(
            asset_managers_overall="bullish",
            asset_managers_weekly="bullish",
            leveraged_funds_weekly="bearish",
        )
        self.assertEqual(result["governing_direction"],"bullish")
        self.assertTrue(result["readiness_allowed"])
        self.assertEqual(result["correction_risk"],"elevated")

    def test_speculative_tdl_remains_visible_outside_timing(self):
        result = evaluate_speculative_policy(timing_eligible=False,weekly_tdl_direction="bearish")
        self.assertEqual(result["weekly_tdl_direction"],"bearish")
        self.assertEqual(result["state"],"MONITORING_ONLY")

    def test_golden_and_enhanced(self):
        golden = evaluate_golden_signals(
            asset_managers_overall="bearish",
            asset_managers_weekly="bullish",
            leveraged_funds_weekly="bullish",
        )
        self.assertTrue(golden["golden_active"])
        self.assertFalse(golden["enhanced_active"])
        enhanced = evaluate_golden_signals(
            asset_managers_overall="bullish",
            asset_managers_weekly="bullish",
            leveraged_funds_weekly="bullish",
        )
        self.assertTrue(enhanced["enhanced_active"])
        self.assertFalse(enhanced["leveraged_funds_overall_used"])

    def test_nmp_uses_open_at_indicator_extreme(self):
        candles=[{"open":10,"close":11},{"open":20,"close":21},{"open":30,"close":31}]
        bull=calculate_nmp(candles=candles,indicator_values=[1,9,2],direction="bullish",indicator_name="RSI")
        bear=calculate_nmp(candles=candles,indicator_values=[-1,-9,-2],direction="bearish",indicator_name="CCI")
        self.assertEqual(bull["value"],20)
        self.assertEqual(bear["value"],20)

    def test_neutral_nmp_is_not_invented(self):
        result=calculate_nmp(candles=[{"open":10}],indicator_values=[50],direction="neutral",indicator_name="RSI")
        self.assertEqual(result["status"],"PENDING_DIRECTION")
        self.assertIsNone(result["value"])

if __name__ == "__main__":
    unittest.main()

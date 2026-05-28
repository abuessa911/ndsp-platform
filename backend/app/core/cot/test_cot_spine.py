import unittest

from app.core.market_positioning.cot_asset_mapper import resolve_cot_asset_mapping
from app.core.market_positioning.cot_contracts import CotReportFamily, CotDirection
from app.core.market_positioning.cot_engine import CotIntelligenceEngine
from app.core.market_positioning.manual_cot_provider import seed_demo_provider


class TestCotSpine(unittest.TestCase):
    def test_forex_uses_tff(self):
        mapping = resolve_cot_asset_mapping("EURUSD")
        self.assertEqual(mapping.report_family, CotReportFamily.TFF)

    def test_gold_uses_disaggregated(self):
        mapping = resolve_cot_asset_mapping("XAUUSD")
        self.assertEqual(mapping.report_family, CotReportFamily.DISAGGREGATED)

    def test_crypto_uses_legacy_fallback(self):
        mapping = resolve_cot_asset_mapping("BTCUSDT")
        self.assertEqual(mapping.report_family, CotReportFamily.LEGACY)

    def test_evaluate_eurusd(self):
        provider = seed_demo_provider()
        snapshot = provider.get_snapshot("EURUSD")
        self.assertIsNotNone(snapshot)

        result = CotIntelligenceEngine().evaluate(snapshot)

        self.assertEqual(result.symbol, "EURUSD")
        self.assertFalse(result.execution_allowed)
        self.assertTrue(result.context_only)
        self.assertIn(result.dominant_direction, {CotDirection.BULLISH, CotDirection.BEARISH, CotDirection.NEUTRAL})

    def test_evaluate_xauusd_alignment_or_conflict(self):
        provider = seed_demo_provider()
        snapshot = provider.get_snapshot("XAUUSD")
        self.assertIsNotNone(snapshot)

        result = CotIntelligenceEngine().evaluate(snapshot)

        self.assertEqual(result.symbol, "XAUUSD")
        self.assertFalse(result.execution_allowed)
        self.assertIn(result.alignment_state, {"golden_alignment", "participant_conflict", "mixed_or_neutral"})

    def test_cot_no_execution(self):
        provider = seed_demo_provider()
        snapshot = provider.get_snapshot("USOIL")
        result = CotIntelligenceEngine().evaluate(snapshot)

        self.assertFalse(result.execution_allowed)
        self.assertTrue(result.context_only)


if __name__ == "__main__":
    unittest.main()

import unittest

from app.support_layers.macro.consensus_provider import (
    MacroConsensus,
    MacroEventType,
    ManualMacroConsensusProvider,
)
from app.support_layers.macro.macro_logic import (
    MacroActual,
    MacroBias,
    calculate_macro_surprise,
    macro_quality_stack_effect,
)


class TestMacroLogic(unittest.TestCase):
    def test_manual_provider_returns_consensus(self):
        provider = ManualMacroConsensusProvider({
            MacroEventType.CPI: MacroConsensus(
                event_type=MacroEventType.CPI,
                expected_value=3.2,
                unit="percent",
                source="manual_test",
            )
        })

        c = provider.get_consensus(MacroEventType.CPI)

        self.assertIsNotNone(c)
        self.assertEqual(c.expected_value, 3.2)
        self.assertEqual(c.source, "manual_test")

    def test_missing_consensus_is_not_valid(self):
        actual = MacroActual(
            event_type=MacroEventType.CPI,
            actual_value=3.4,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, None)

        self.assertFalse(result.valid)
        self.assertEqual(result.reason, "consensus_missing")
        self.assertEqual(result.bias, MacroBias.UNKNOWN)
        self.assertEqual(result.confidence_effect, 0.0)

    def test_cpi_higher_than_expected_is_hawkish(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.CPI,
            expected_value=3.2,
            unit="percent",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.CPI,
            actual_value=3.5,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, consensus)

        self.assertTrue(result.valid)
        self.assertGreater(result.surprise, 0)
        self.assertEqual(result.bias, MacroBias.HAWKISH)
        self.assertGreater(result.quality_effect, 0)

    def test_cpi_lower_than_expected_is_dovish(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.CPI,
            expected_value=3.2,
            unit="percent",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.CPI,
            actual_value=3.0,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, consensus)

        self.assertTrue(result.valid)
        self.assertLess(result.surprise, 0)
        self.assertEqual(result.bias, MacroBias.DOVISH)

    def test_unemployment_higher_than_expected_is_dovish(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.UNEMPLOYMENT_RATE,
            expected_value=4.0,
            unit="percent",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.UNEMPLOYMENT_RATE,
            actual_value=4.3,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, consensus)

        self.assertTrue(result.valid)
        self.assertEqual(result.bias, MacroBias.DOVISH)

    def test_neutral_band(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.FED_RATE,
            expected_value=5.5,
            unit="percent",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.FED_RATE,
            actual_value=5.5,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, consensus)

        self.assertTrue(result.valid)
        self.assertEqual(result.bias, MacroBias.NEUTRAL)
        self.assertEqual(result.quality_effect, 0.0)

    def test_macro_quality_stack_effect(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.NFP,
            expected_value=180000,
            unit="jobs",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.NFP,
            actual_value=220000,
            unit="jobs",
        )

        result = calculate_macro_surprise(actual, consensus)
        effect = macro_quality_stack_effect(result)

        self.assertIn("macro_effect", effect)
        self.assertGreaterEqual(effect["macro_effect"], 0.0)
        self.assertLessEqual(effect["macro_effect"], 1.0)

    def test_macro_does_not_produce_direction(self):
        consensus = MacroConsensus(
            event_type=MacroEventType.CORE_CPI,
            expected_value=3.0,
            unit="percent",
            source="manual_test",
        )
        actual = MacroActual(
            event_type=MacroEventType.CORE_CPI,
            actual_value=3.5,
            unit="percent",
        )

        result = calculate_macro_surprise(actual, consensus)

        self.assertFalse(hasattr(result, "direction"))
        self.assertTrue(result.valid)


if __name__ == "__main__":
    unittest.main()

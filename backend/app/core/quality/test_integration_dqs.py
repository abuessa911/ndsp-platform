import unittest

from app.core.quality.decision_quality_stack import (
    DQSInput,
    DecisionQualityStack,
    calculate_total_quality,
)


class TestDQSIntegration(unittest.TestCase):
    def setUp(self):
        self.dqs = DecisionQualityStack()

    def test_perfect_alignment(self):
        result = self.dqs.calculate_total_quality(
            DQSInput(
                base_confidence=80.0,
                macro_effect=0.8,
                black_layer_penalty=0.0,
                black_severity="CLEAR",
            )
        )

        self.assertGreaterEqual(result.final_confidence, 90.0)
        self.assertEqual(result.grade, "A")
        self.assertEqual(result.decision_state, "active")
        self.assertEqual(result.risk_state, "normal")
        self.assertFalse(result.execution_allowed)
        self.assertEqual(result.execution_mode, "decision_support_only")

    def test_safety_veto_kill(self):
        result = self.dqs.calculate_total_quality(
            DQSInput(
                base_confidence=90.0,
                macro_effect=1.0,
                black_layer_penalty=1.0,
                black_severity="KILL",
                black_reasons=["DATA_STALE"],
            )
        )

        self.assertEqual(result.final_confidence, 0.0)
        self.assertEqual(result.grade, "F_BLOCKED")
        self.assertEqual(result.decision_state, "blocked")
        self.assertEqual(result.risk_state, "high")
        self.assertFalse(result.execution_allowed)
        self.assertIn("CRITICAL_SAFETY_BLOCK:KILL", result.reasons)

    def test_safety_veto_block(self):
        result = calculate_total_quality(
            base_confidence=85.0,
            macro_effect=0.5,
            black_layer_penalty=1.0,
            black_severity="BLOCK",
            black_reasons=["HIGH_SPREAD"],
        )

        self.assertEqual(result.final_confidence, 0.0)
        self.assertEqual(result.grade, "F_BLOCKED")
        self.assertEqual(result.decision_state, "blocked")
        self.assertFalse(result.execution_allowed)

    def test_caution_does_not_zero_confidence(self):
        result = self.dqs.calculate_total_quality(
            DQSInput(
                base_confidence=80.0,
                macro_effect=0.0,
                black_layer_penalty=0.35,
                black_severity="CAUTION",
                black_reasons=["HIGH_SPREAD"],
            )
        )

        self.assertGreater(result.final_confidence, 0.0)
        self.assertEqual(result.decision_state, "active_caution")
        self.assertEqual(result.risk_state, "caution")
        self.assertFalse(result.execution_allowed)
        self.assertIn("SAFETY_CAUTION", result.reasons)

    def test_macro_negative_effect_reduces_score(self):
        positive = calculate_total_quality(
            base_confidence=70,
            macro_effect=0.5,
            black_layer_penalty=0,
            black_severity="CLEAR",
        )
        negative = calculate_total_quality(
            base_confidence=70,
            macro_effect=-0.5,
            black_layer_penalty=0,
            black_severity="CLEAR",
        )

        self.assertGreater(positive.final_confidence, negative.final_confidence)

    def test_clamps_score_to_100(self):
        result = calculate_total_quality(
            base_confidence=95,
            macro_effect=1.0,
            black_layer_penalty=0,
            black_severity="CLEAR",
        )

        self.assertEqual(result.final_confidence, 100.0)

    def test_clamps_score_to_zero(self):
        result = calculate_total_quality(
            base_confidence=5,
            macro_effect=-1.0,
            black_layer_penalty=1.0,
            black_severity="CLEAR",
        )

        self.assertEqual(result.final_confidence, 0.0)

    def test_dqs_does_not_produce_direction(self):
        result = calculate_total_quality(
            base_confidence=80,
            macro_effect=0.5,
            black_layer_penalty=0,
            black_severity="CLEAR",
        )

        self.assertFalse(hasattr(result, "direction"))


if __name__ == "__main__":
    unittest.main()

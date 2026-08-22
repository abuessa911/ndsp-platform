import unittest

from app.support_layers.black_layer.black_layer_engine import (
    BlackLayerEngine,
    BlackReasonCode,
    BlackSeverity,
    black_layer_quality_effect_from_state,
)


class TestBlackLayer(unittest.TestCase):
    def setUp(self):
        self.engine = BlackLayerEngine()

    def test_spread_block(self):
        rule = self.engine.evaluate_spread(current_spread=4.0, avg_spread=1.0)
        self.assertEqual(rule.severity, BlackSeverity.BLOCK)
        self.assertEqual(rule.code, BlackReasonCode.HIGH_SPREAD)

    def test_spread_caution(self):
        rule = self.engine.evaluate_spread(current_spread=2.0, avg_spread=1.0)
        self.assertEqual(rule.severity, BlackSeverity.CAUTION)

    def test_data_staleness_kill(self):
        rule = self.engine.evaluate_freshness(last_update_seconds=70)
        self.assertEqual(rule.severity, BlackSeverity.KILL)
        self.assertEqual(rule.code, BlackReasonCode.DATA_STALE)

    def test_data_freshness_caution(self):
        rule = self.engine.evaluate_freshness(last_update_seconds=20)
        self.assertEqual(rule.severity, BlackSeverity.CAUTION)

    def test_multi_rule_integration_caution(self):
        rules = [
            self.engine.evaluate_spread(current_spread=2.0, avg_spread=1.0),
            self.engine.evaluate_freshness(last_update_seconds=5),
        ]
        result = self.engine.get_final_safety_state(rules)

        self.assertEqual(result["severity"], "CAUTION")
        self.assertTrue(result["can_execute"])
        self.assertEqual(result["decision_state"], "active_caution")
        self.assertEqual(result["risk_state"], "caution")

    def test_kill_overrides_caution(self):
        rules = [
            self.engine.evaluate_spread(current_spread=2.0, avg_spread=1.0),
            self.engine.evaluate_freshness(last_update_seconds=70),
        ]
        result = self.engine.get_final_safety_state(rules)

        self.assertEqual(result["severity"], "KILL")
        self.assertFalse(result["can_execute"])
        self.assertEqual(result["decision_state"], "blocked")
        self.assertIn("DATA_STALE", result["active_reasons"])

    def test_block_prevents_execution(self):
        rules = [
            self.engine.evaluate_spread(current_spread=4.0, avg_spread=1.0),
        ]
        result = self.engine.get_final_safety_state(rules)

        self.assertEqual(result["severity"], "BLOCK")
        self.assertFalse(result["can_execute"])
        self.assertEqual(result["decision_state"], "blocked")

    def test_penalty_is_max_not_sum(self):
        rules = [
            self.engine.evaluate_spread(current_spread=4.0, avg_spread=1.0),
            self.engine.evaluate_freshness(last_update_seconds=70),
        ]
        result = self.engine.get_final_safety_state(rules)

        self.assertEqual(result["penalty"], 1.0)

    def test_quality_effect_values(self):
        clear = self.engine.get_final_safety_state([])
        caution = self.engine.get_final_safety_state([
            self.engine.evaluate_spread(current_spread=2.0, avg_spread=1.0)
        ])
        block = self.engine.get_final_safety_state([
            self.engine.evaluate_spread(current_spread=4.0, avg_spread=1.0)
        ])
        kill = self.engine.get_final_safety_state([
            self.engine.evaluate_freshness(last_update_seconds=70)
        ])

        self.assertEqual(black_layer_quality_effect_from_state(clear), {"black_layer_penalty": 0.0})
        self.assertEqual(black_layer_quality_effect_from_state(caution), {"black_layer_penalty": 0.35})
        self.assertEqual(black_layer_quality_effect_from_state(block), {"black_layer_penalty": 1.0})
        self.assertEqual(black_layer_quality_effect_from_state(kill), {"black_layer_penalty": 1.0})


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

from backend.layers.canonical_v1.layer_orchestrator_v2 import run_all_layers


class TestCanonicalOrchestratorSmoke(unittest.TestCase):
    def test_all_16_layers_execute_in_order(self):
        project = Path(__file__).resolve().parents[4]
        registry = project / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
        payload = {
            "analysis_mode": "investment",
            "cot_validity": {
                "decision_use_allowed": True,
                "monitoring_use_allowed": True,
                "status": "CURRENT",
            },
            "asset_managers_overall": "bullish",
            "asset_managers_weekly": "bullish",
            "leveraged_funds_weekly": "bullish",
            "weekly_tdl_direction": "bullish",
            "timing_eligible": True,
            "divergence_result": {"status": "CONFIRMED", "confidence": 80},
            "scenario_levels": {
                "activation": 100,
                "arrival": 110,
                "review": 95,
                "invalidation": 90,
            },
            "candles": [{"open": 100}, {"open": 105}, {"open": 103}],
            "indicator_values": [20, 80, 40],
            "indicator_name": "RSI",
            "timeframe": "1W",
            "momentum_result": {"status": "CONFIRMED", "confidence": 80},
            "liquidity_structure_result": {
                "status": "CONFIRMED",
                "confidence": 80,
            },
            "usd_macro_result": {"status": "SUPPORTIVE", "confidence": 80},
            "risk_result": {
                "status": "PASSED",
                "confidence": 80,
                "blocked": False,
            },
            "devils_advocate_blocked": False,
        }

        result = run_all_layers(payload, registry)

        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["total_layers_executed"], 16)
        self.assertEqual(result["single_truth_state"], "READY")
        self.assertEqual(
            [layer["layer_id"] for layer in result["layers"]],
            [f"NDSP-CORE-L{i:02d}" for i in range(1, 17)],
        )


if __name__ == "__main__":
    unittest.main()

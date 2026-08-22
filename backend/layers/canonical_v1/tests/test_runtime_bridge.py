import unittest

from backend.layers.canonical_v1.runtime_bridge import (
    run_canonical_layers,
    to_legacy_api_envelope,
)


class TestRuntimeBridge(unittest.TestCase):
    def test_legacy_envelope_is_additive_and_non_mutating(self):
        source = {
            "ok": True,
            "single_truth_state": "READY",
            "layers": [
                {
                    "layer_id": "NDSP-CORE-L01",
                    "confidence": 65,
                    "output": {},
                },
                {
                    "layer_id": "NDSP-CORE-L16",
                    "confidence": 60,
                    "output": {},
                },
            ],
            "errors": [],
            "context_after_layers": {},
        }

        result = to_legacy_api_envelope(
            source,
            input_context_source="test-context",
        )

        self.assertEqual(result["total_layers_expected"], 16)
        self.assertEqual(result["total_layers_executed"], 2)
        self.assertEqual(result["total_errors"], 0)
        self.assertEqual(result["average_confidence"], 62)
        self.assertEqual(result["single_truth_state"], "READY")
        self.assertEqual(result["input_context_source"], "test-context")
        self.assertEqual(result["layers"][0]["legacy_layer_number"], 1)
        self.assertEqual(result["layers"][1]["legacy_layer_number"], 16)
        self.assertNotIn("module_file", source["layers"][0])

    def test_full_canonical_run_gets_legacy_envelope(self):
        canonical = run_canonical_layers({})
        result = to_legacy_api_envelope(canonical)

        self.assertEqual(result["total_layers_expected"], 16)
        self.assertEqual(result["total_layers_executed"], 16)
        self.assertEqual(result["total_errors"], len(result["errors"]))
        self.assertEqual(len(result["layers"]), 16)
        self.assertEqual(
            result["layers"][0]["layer_id"],
            "NDSP-CORE-L01",
        )
        self.assertEqual(
            result["layers"][-1]["layer_id"],
            "NDSP-CORE-L16",
        )
        self.assertEqual(
            result["engine_mode"],
            "canonical_v1_candidate",
        )


if __name__ == "__main__":
    unittest.main()

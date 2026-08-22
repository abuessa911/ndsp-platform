import unittest
from pathlib import Path

from canonical_runtime import (
    PROJECT_ROOT,
    health_metadata,
    run_layers_compat,
)


class TestCanonicalRuntime(unittest.TestCase):
    def test_bootstrap_and_compatibility_envelope(self):
        expected_root = Path(__file__).resolve().parents[2]
        self.assertEqual(PROJECT_ROOT, expected_root)

        health = health_metadata()
        self.assertTrue(health["canonical_import"])
        self.assertTrue(health["project_root_on_path"])
        self.assertEqual(
            health["engine_mode"],
            "canonical_v1_candidate",
        )

        result = run_layers_compat(
            {},
            input_context_source="unittest",
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["total_layers_expected"], 16)
        self.assertEqual(result["total_layers_executed"], 16)
        self.assertEqual(result["total_errors"], 0)
        self.assertEqual(
            result["input_context_source"],
            "unittest",
        )
        self.assertEqual(
            result["engine_mode"],
            "canonical_v1_candidate",
        )
        self.assertEqual(
            result["compatibility_mode"],
            "legacy_envelope_additive",
        )


if __name__ == "__main__":
    unittest.main()

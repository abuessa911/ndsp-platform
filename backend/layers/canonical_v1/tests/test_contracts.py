import unittest

from backend.layers.canonical_v1.core.contracts import (
    DecisionReadinessState,
    LayerResult,
)


class TestCanonicalContracts(unittest.TestCase):
    def test_readiness_states_are_exact(self):
        self.assertEqual(
            {state.value for state in DecisionReadinessState},
            {
                "DATA_BLOCKED",
                "BLOCKED_BY_DEVILS_ADVOCATE",
                "MONITORING_ONLY",
                "UNDER_REVIEW",
                "READY",
            },
        )

    def test_confidence_bounds_are_accepted(self):
        for confidence in (0, 100):
            result = LayerResult("L", "test", "TEST", confidence, {})
            self.assertEqual(result.confidence, confidence)

    def test_out_of_range_confidence_is_rejected(self):
        for confidence in (-1, 101):
            with self.assertRaises(ValueError):
                LayerResult("L", "test", "TEST", confidence, {})


if __name__ == "__main__":
    unittest.main()

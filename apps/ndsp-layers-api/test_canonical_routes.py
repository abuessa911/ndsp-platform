import unittest
from unittest.mock import patch

import app as api


class TestCanonicalShadowRoutes(unittest.TestCase):
    def test_legacy_and_shadow_routes_are_registered(self):
        routes = {
            (route.path, method)
            for route in api.app.routes
            for method in (route.methods or [])
        }

        self.assertIn(("/api/admin/layers/run", "GET"), routes)
        self.assertIn(("/api/admin/layers/run", "POST"), routes)
        self.assertIn(
            ("/api/admin/layers/canonical/health", "GET"),
            routes,
        )
        self.assertIn(
            ("/api/admin/layers/canonical/run", "GET"),
            routes,
        )
        self.assertIn(
            ("/api/admin/layers/canonical/run", "POST"),
            routes,
        )

    def test_shadow_get_executes_canonical_engine(self):
        context = {
            "asset": "GOLD",
            "symbol": "GOLD",
            "live_context_source": "route-unittest",
        }

        with patch.object(api, "live_context", return_value=context):
            result = api.run_canonical_layers_default("GOLD")

        self.assertTrue(result["ok"])
        self.assertEqual(result["total_layers_executed"], 16)
        self.assertEqual(result["total_errors"], 0)
        self.assertEqual(
            result["engine_mode"],
            "canonical_v1_candidate",
        )
        self.assertEqual(
            result["input_context_source"],
            "route-unittest",
        )

    def test_shadow_health_is_explicitly_non_production(self):
        result = api.canonical_health()

        self.assertTrue(result["ok"])
        self.assertEqual(result["mode"], "shadow")
        self.assertEqual(
            result["canonical"]["engine_mode"],
            "canonical_v1_candidate",
        )


if __name__ == "__main__":
    unittest.main()

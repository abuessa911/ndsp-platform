"""Tests for the governed NDSP Public API projection boundary."""

from __future__ import annotations

import unittest

from backend.contracts.canonical_v1.public_contracts import (
    PUBLIC_ROUTE_CONTRACTS,
    get_public_contract,
    project_public_response,
    public_contract_manifest,
)
from backend.platform.canonical_v1.public_projection import (
    build_market_context,
    build_public_core,
    build_public_evidence,
    build_public_overview,
)


class PublicContractTests(unittest.TestCase):
    def test_all_four_public_routes_are_registered(self) -> None:
        self.assertEqual(
            set(PUBLIC_ROUTE_CONTRACTS),
            {
                "/api/public/overview",
                "/api/public/core",
                "/api/public/market-context",
                "/api/public/evidence",
            },
        )

    def test_contract_metadata_is_public_read_v1(self) -> None:
        manifest = public_contract_manifest()

        for metadata in manifest.values():
            self.assertEqual(metadata["method"], "GET")
            self.assertEqual(metadata["version"], "v1")
            self.assertEqual(metadata["access_policy"], "public-read")
            self.assertFalse(metadata["entitlement_required"])

    def test_unknown_route_is_rejected(self) -> None:
        with self.assertRaises(KeyError):
            get_public_contract("/api/public/not-registered")

    def test_unapproved_top_level_fields_are_removed(self) -> None:
        payload = {
            "mode": "live",
            "updatedAt": "2026-08-09T00:00:00Z",
            "direction": "تحت المراقبة",
            "summary": "public",
            "governanceStatus": "available",
            "evidenceStatus": "available",
            "freshnessStatus": "fresh",
            "private_internal_field": "must-not-leak",
        }

        projected = project_public_response(
            "/api/public/core",
            payload,
        )

        self.assertNotIn("private_internal_field", projected)

    def test_unapproved_nested_evidence_fields_are_removed(self) -> None:
        projected = project_public_response(
            "/api/public/evidence",
            {
                "mode": "live",
                "updatedAt": "2026-08-09T00:00:00Z",
                "rows": [
                    {
                        "id": "PUBLIC-1",
                        "source": "Authorized Source",
                        "category": "Public Evidence",
                        "status": "Authorized",
                        "freshness": "Fresh",
                        "updatedAt": "2026-08-09T00:00:00Z",
                        "internal_payload": "must-not-leak",
                        "raw_value": 123,
                    }
                ],
            },
        )

        row = projected["rows"][0]
        self.assertNotIn("internal_payload", row)
        self.assertNotIn("raw_value", row)

    def test_overview_builder_does_not_fabricate_trend(self) -> None:
        payload = build_public_overview(
            governance_available=True,
            evidence_available=False,
            freshness_available=False,
        )

        self.assertEqual(payload["mode"], "live")
        self.assertEqual(payload["trend"], [])

    def test_core_builder_has_frontend_contract_fields(self) -> None:
        payload = build_public_core(
            governance_available=True,
            evidence_available=False,
            freshness_available=True,
        )

        self.assertEqual(
            set(payload),
            {
                "mode",
                "updatedAt",
                "direction",
                "summary",
                "governanceStatus",
                "evidenceStatus",
                "freshnessStatus",
            },
        )

    def test_market_context_builder_has_no_synthetic_series(self) -> None:
        payload = build_market_context()

        self.assertEqual(payload["mode"], "live")
        self.assertEqual(payload["contextSeries"], [])

    def test_evidence_builder_defaults_to_no_rows(self) -> None:
        payload = build_public_evidence()

        self.assertEqual(payload["mode"], "live")
        self.assertEqual(payload["rows"], [])


if __name__ == "__main__":
    unittest.main()

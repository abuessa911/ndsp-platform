"""Tests for governed NDSP live public providers."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from backend.platform.canonical_v1 import (
    live_public_providers as providers,
)


class LivePublicProviderTests(unittest.TestCase):
    def test_governance_requires_public_safe(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "public_safe": True,
            },
        ):
            self.assertTrue(
                providers.governance_is_available()
            )

    def test_core_projects_only_authorized_fields(self) -> None:
        def fake_fetch(url: str):
            if "9084" in url:
                return {
                    "ok": True,
                    "allowed_public_outputs": {
                        "directional_bias": "هابط",
                        "sanitized_summary": "ملخص عام مصرح.",
                        "decision_quality": 82,
                    },
                    "updated_at": "2026-08-09T18:10:15Z",
                    "decision_layers": ["private"],
                }

            if "9044" in url:
                return {
                    "ok": True,
                    "public_safe": True,
                }

            if "9078" in url:
                return {
                    "ok": True,
                    "decisions": [],
                }

            return None

        with patch.object(
            providers,
            "_fetch_json",
            side_effect=fake_fetch,
        ):
            result = providers.read_authorized_core()

        self.assertTrue(result.available)
        self.assertIsNotNone(result.payload)

        payload = result.payload or {}

        self.assertEqual(
            payload["direction"],
            "هابط",
        )
        self.assertEqual(
            payload["summary"],
            "ملخص عام مصرح.",
        )
        self.assertNotIn(
            "decision_quality",
            payload,
        )
        self.assertNotIn(
            "decision_layers",
            payload,
        )

    def test_core_is_unavailable_without_required_public_output(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value=None,
        ):
            result = providers.read_authorized_core()

        self.assertFalse(result.available)
        self.assertIsNone(result.payload)

    def test_market_does_not_expose_service_metadata(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "service": "private-provider-name",
                "version": "private-version",
                "mode": "private-mode",
                "timeframes": ["1H", "4H"],
                "updated_at": "2026-08-09T18:10:15Z",
            },
        ):
            result = providers.read_market_context()

        self.assertTrue(result.available)

        payload = result.payload or {}

        serialized = repr(payload)

        self.assertNotIn(
            "private-provider-name",
            serialized,
        )
        self.assertNotIn(
            "private-version",
            serialized,
        )
        self.assertNotIn(
            "private-mode",
            serialized,
        )
        self.assertEqual(
            payload["contextSeries"],
            [],
        )

    def test_evidence_uses_opaque_identifier(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "decisions": [
                    {
                        "id": "INTERNAL-DECISION-123",
                        "symbol": "BTCUSDT",
                        "updated_at": "2026-08-09T18:10:15Z",
                        "sensitive_result": "hidden",
                    }
                ],
            },
        ):
            result = providers.read_public_evidence()

        self.assertTrue(result.available)

        payload = result.payload or {}
        rows = payload["rows"]

        self.assertEqual(len(rows), 1)

        row = rows[0]

        self.assertTrue(
            row["id"].startswith("EVID-")
        )
        self.assertNotEqual(
            row["id"],
            "INTERNAL-DECISION-123",
        )
        self.assertNotIn(
            "symbol",
            row,
        )
        self.assertNotIn(
            "sensitive_result",
            row,
        )

    def test_overview_does_not_fabricate_trend(self) -> None:
        def fake_fetch(url: str):
            if "9044" in url:
                return {
                    "ok": True,
                    "public_safe": True,
                }

            if "9078" in url:
                return {
                    "ok": True,
                    "decisions": [],
                }

            if "9093" in url:
                return {
                    "ok": True,
                    "updated_at": "2026-08-09T18:10:15Z",
                }

            return None

        with patch.object(
            providers,
            "_fetch_json",
            side_effect=fake_fetch,
        ):
            payload = providers.build_live_overview()

        self.assertEqual(
            payload["trend"],
            [],
        )


if __name__ == "__main__":
    unittest.main()

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

        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "public_safe": False,
            },
        ):
            self.assertFalse(
                providers.governance_is_available()
            )

    def test_core_uses_only_authorized_public_outputs(self) -> None:
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
                    "protected_contract_data": {
                        "must_not": "cross"
                    },
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
            result = providers.build_live_core(
                "BTCUSDT"
            )

        self.assertEqual(
            result["direction"],
            "هابط",
        )
        self.assertEqual(
            result["summary"],
            "ملخص عام مصرح.",
        )
        self.assertEqual(
            result["freshnessStatus"],
            "Freshness Available",
        )

        self.assertNotIn(
            "protected_contract_data",
            result,
        )
        self.assertNotIn(
            "decision_quality",
            result,
        )

    def test_core_fails_closed(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value=None,
        ):
            result = providers.build_live_core()

        self.assertEqual(
            result["direction"],
            "تحت المراقبة",
        )
        self.assertEqual(
            result["freshnessStatus"],
            "Freshness Unconfirmed",
        )

    def test_market_never_fabricates_series(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "mode": "lazy_timeframes",
                "timeframes": [
                    "1H",
                    "4H",
                    "1D",
                ],
                "updated_at": "2026-08-09T18:10:15Z",
            },
        ):
            result = (
                providers.build_live_market_context()
            )

        self.assertEqual(
            result["contextSeries"],
            [],
        )

    def test_evidence_exposes_metadata_only(self) -> None:
        with patch.object(
            providers,
            "_fetch_json",
            return_value={
                "ok": True,
                "decisions": [
                    {
                        "id": "DEC-001",
                        "symbol": "BTCUSDT",
                        "updated_at": "2026-08-09T18:10:15Z",
                        "sensitive_result": "hidden",
                    }
                ],
            },
        ):
            result = providers.build_live_evidence()

        self.assertEqual(
            len(result["rows"]),
            1,
        )

        row = result["rows"][0]

        self.assertEqual(
            set(row),
            {
                "id",
                "source",
                "category",
                "status",
                "freshness",
                "updatedAt",
            },
        )

        self.assertNotIn(
            "symbol",
            row,
        )
        self.assertNotIn(
            "sensitive_result",
            row,
        )

    def test_overview_uses_real_provider_state(self) -> None:
        def fake_fetch(url: str):
            if "9044" in url:
                return {
                    "ok": True,
                    "public_safe": True,
                }

            if "9078" in url:
                return {
                    "ok": True,
                    "decisions": [
                        {
                            "id": "DEC-001",
                        }
                    ],
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
            result = providers.build_live_overview()

        kpis = {
            item["id"]: item
            for item in result["kpis"]
        }

        self.assertEqual(
            kpis["governance"]["status"],
            "positive",
        )
        self.assertEqual(
            kpis["evidence"]["status"],
            "positive",
        )
        self.assertEqual(
            result["trend"],
            [],
        )


if __name__ == "__main__":
    unittest.main()

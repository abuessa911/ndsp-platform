"""Governed projection layer for NDSP Public API V1.

Only already-authorized, presentation-safe values may enter these builders.
The final allowlist projection is enforced by canonical public contracts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.contracts.canonical_v1.public_contracts import (
    project_public_response,
)


OVERVIEW_ROUTE = "/api/public/overview"
CORE_ROUTE = "/api/public/core"
MARKET_CONTEXT_ROUTE = "/api/public/market-context"
EVIDENCE_ROUTE = "/api/public/evidence"


def utc_now_iso() -> str:
    """Return an RFC3339 UTC timestamp."""

    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _text(value: Any, fallback: str) -> str:
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned:
            return cleaned
    return fallback


def build_public_overview(
    *,
    governance_available: bool,
    evidence_available: bool,
    freshness_available: bool,
    trend: list[dict[str, Any]] | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Build the public overview from availability metadata and real trend data."""

    timestamp = updated_at or utc_now_iso()

    payload = {
        "mode": "live",
        "updatedAt": timestamp,
        "kpis": [
            {
                "id": "governance",
                "label": "الحوكمة",
                "value": "متاح" if governance_available else "غير متاح",
                "detail": "Authorized Public Projection",
                "status": "positive" if governance_available else "warning",
            },
            {
                "id": "evidence",
                "label": "الأدلة",
                "value": "متاحة" if evidence_available else "غير متاحة",
                "detail": "Authorized Evidence",
                "status": "positive" if evidence_available else "warning",
            },
            {
                "id": "freshness",
                "label": "حداثة البيانات",
                "value": "متاحة" if freshness_available else "غير مؤكدة",
                "detail": "Freshness Aware",
                "status": "neutral" if freshness_available else "warning",
            },
        ],
        "trend": trend or [],
    }

    return project_public_response(OVERVIEW_ROUTE, payload)


def build_public_core(
    *,
    direction: Any = None,
    summary: Any = None,
    governance_available: bool,
    evidence_available: bool,
    freshness_available: bool,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Build the authorized CORE public projection."""

    payload = {
        "mode": "live",
        "updatedAt": updated_at or utc_now_iso(),
        "direction": _text(direction, "تحت المراقبة"),
        "summary": _text(
            summary,
            "لا يتوفر حاليًا مخرج CORE عام محدث من المصدر المعتمد.",
        ),
        "governanceStatus": (
            "Governance Available"
            if governance_available
            else "Governance Unavailable"
        ),
        "evidenceStatus": (
            "Authorized Evidence Available"
            if evidence_available
            else "Authorized Evidence Unavailable"
        ),
        "freshnessStatus": (
            "Freshness Available"
            if freshness_available
            else "Freshness Unconfirmed"
        ),
    }

    return project_public_response(CORE_ROUTE, payload)


def build_market_context(
    *,
    title: Any = None,
    summary: Any = None,
    context_series: list[dict[str, Any]] | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Build public market context without fabricating unavailable series."""

    payload = {
        "mode": "live",
        "updatedAt": updated_at or utc_now_iso(),
        "title": _text(title, "سياق السوق"),
        "summary": _text(
            summary,
            "لا تتوفر حاليًا بيانات سياق عامة إضافية من المصدر المعتمد.",
        ),
        "contextSeries": context_series or [],
    }

    return project_public_response(MARKET_CONTEXT_ROUTE, payload)


def build_public_evidence(
    *,
    rows: list[dict[str, Any]] | None = None,
    updated_at: str | None = None,
) -> dict[str, Any]:
    """Build only evidence rows explicitly approved for public projection."""

    payload = {
        "mode": "live",
        "updatedAt": updated_at or utc_now_iso(),
        "rows": rows or [],
    }

    return project_public_response(EVIDENCE_ROUTE, payload)

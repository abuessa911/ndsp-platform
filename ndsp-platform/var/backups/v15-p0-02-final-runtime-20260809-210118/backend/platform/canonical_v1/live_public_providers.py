"""Canonical live providers for the governed NDSP Public API V1.

Only explicitly authorized public outputs cross this boundary.
Raw provider contracts and protected decision internals remain private.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any

from backend.platform.canonical_v1.public_projection import (
    build_market_context,
    build_public_core,
    build_public_evidence,
    build_public_overview,
)


GOVERNANCE_URL = "http://127.0.0.1:9044/api/governance/health"
CORE_URL = "http://127.0.0.1:9084/api/decision/quality-contract-v53"
MARKET_URL = "http://127.0.0.1:9093/health"
EVIDENCE_URL = "http://127.0.0.1:9078/api/completed"

DEFAULT_SYMBOL = "BTCUSDT"
HTTP_TIMEOUT_SECONDS = 3.0


def _fetch_json(url: str) -> dict[str, Any] | None:
    """Fetch a local provider response and fail closed on any error."""

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ndsp-public-projection-v1",
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=HTTP_TIMEOUT_SECONDS,
        ) as response:
            if response.status != 200:
                return None

            payload = json.loads(
                response.read().decode("utf-8", "ignore")
            )
    except Exception:
        return None

    return payload if isinstance(payload, dict) else None


def _safe_text(value: Any) -> str | None:
    """Normalize public scalar text."""

    if not isinstance(value, str):
        return None

    cleaned = value.strip()
    return cleaned or None


def _first_timestamp(payload: dict[str, Any]) -> str | None:
    """Read only presentation-safe freshness timestamps."""

    for key in ("updated_at", "generated_at"):
        value = _safe_text(payload.get(key))
        if value:
            return value

    return None


def governance_is_available() -> bool:
    """Verify that the governance service explicitly declares public safety."""

    payload = _fetch_json(GOVERNANCE_URL)

    return bool(
        payload
        and payload.get("ok") is True
        and payload.get("public_safe") is True
    )


def _read_authorized_core(
    symbol: str = DEFAULT_SYMBOL,
) -> tuple[dict[str, Any] | None, str | None]:
    """Read only allowed_public_outputs from the canonical CORE contract."""

    normalized_symbol = (
        _safe_text(symbol) or DEFAULT_SYMBOL
    ).upper()

    query = urllib.parse.urlencode(
        {"symbol": normalized_symbol}
    )

    payload = _fetch_json(
        f"{CORE_URL}?{query}"
    )

    if not payload or payload.get("ok") is not True:
        return None, None

    authorized = payload.get("allowed_public_outputs")

    if not isinstance(authorized, dict):
        return None, None

    return authorized, _first_timestamp(payload)


def _completed_decisions() -> list[dict[str, Any]]:
    """Read completed decisions without forwarding their raw payloads."""

    payload = _fetch_json(EVIDENCE_URL)

    if not payload or payload.get("ok") is not True:
        return []

    decisions = payload.get("decisions")

    if not isinstance(decisions, list):
        return []

    return [
        item
        for item in decisions
        if isinstance(item, dict)
    ]


def evidence_is_available() -> bool:
    """Report whether authorized completed-decision evidence exists."""

    return bool(_completed_decisions())


def build_live_core(
    symbol: str = DEFAULT_SYMBOL,
) -> dict[str, Any]:
    """Build the governed CORE public response."""

    authorized, updated_at = _read_authorized_core(symbol)

    direction = None
    summary = None

    if authorized is not None:
        direction = _safe_text(
            authorized.get("directional_bias")
        )
        summary = _safe_text(
            authorized.get("sanitized_summary")
        )

    core_available = authorized is not None

    return build_public_core(
        direction=direction,
        summary=summary,
        governance_available=governance_is_available(),
        evidence_available=evidence_is_available(),
        freshness_available=(
            core_available and updated_at is not None
        ),
        updated_at=updated_at,
    )


def _market_health() -> dict[str, Any] | None:
    """Return verified market-context service health."""

    payload = _fetch_json(MARKET_URL)

    if not payload or payload.get("ok") is not True:
        return None

    return payload


def build_live_market_context() -> dict[str, Any]:
    """Build market context without fabricating numerical series."""

    payload = _market_health()

    if payload is None:
        return build_market_context(
            title="سياق السوق",
            summary="مصدر سياق السوق العام غير متاح حاليًا.",
            context_series=[],
        )

    mode = _safe_text(payload.get("mode"))
    updated_at = _safe_text(payload.get("updated_at"))

    timeframes = payload.get("timeframes")
    timeframe_count = (
        len(timeframes)
        if isinstance(timeframes, list)
        else 0
    )

    summary_parts: list[str] = []

    if mode:
        summary_parts.append(
            f"حالة مصدر السياق: {mode}"
        )

    if timeframe_count:
        summary_parts.append(
            f"الأطر الزمنية المتاحة: {timeframe_count}"
        )

    summary = (
        " · ".join(summary_parts)
        if summary_parts
        else "مصدر سياق السوق العام متاح."
    )

    return build_market_context(
        title="سياق السوق",
        summary=summary,
        context_series=[],
        updated_at=updated_at,
    )


def _evidence_timestamp(
    item: dict[str, Any],
) -> str | None:
    """Select a safe public freshness timestamp."""

    for key in (
        "published_at",
        "completed_at",
        "updated_at",
        "created_at",
    ):
        value = _safe_text(item.get(key))

        if value:
            return value

    return None


def build_live_evidence() -> dict[str, Any]:
    """Project completed-decision metadata into the public evidence contract."""

    rows: list[dict[str, Any]] = []
    response_updated_at: str | None = None

    for index, item in enumerate(
        _completed_decisions()[:20],
        start=1,
    ):
        identifier = (
            _safe_text(item.get("id"))
            or _safe_text(item.get("decision_id"))
            or f"PUBLIC-EVIDENCE-{index:03d}"
        )

        timestamp = _evidence_timestamp(item)

        if timestamp is None:
            continue

        if (
            response_updated_at is None
            or timestamp > response_updated_at
        ):
            response_updated_at = timestamp

        rows.append(
            {
                "id": identifier,
                "source": "Completed Decision Ledger",
                "category": "Authorized Decision Evidence",
                "status": "Authorized",
                "freshness": "Available",
                "updatedAt": timestamp,
            }
        )

    return build_public_evidence(
        rows=rows,
        updated_at=response_updated_at,
    )


def build_live_overview() -> dict[str, Any]:
    """Build overview from verified provider availability."""

    governance_available = governance_is_available()
    evidence_available = evidence_is_available()
    market = _market_health()

    market_updated_at = (
        _safe_text(market.get("updated_at"))
        if market
        else None
    )

    return build_public_overview(
        governance_available=governance_available,
        evidence_available=evidence_available,
        freshness_available=market_updated_at is not None,
        trend=[],
        updated_at=market_updated_at,
    )

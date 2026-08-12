"""Canonical live providers for the governed NDSP Public API V1.

Only explicitly authorized public outputs cross this boundary.
Raw provider contracts, service metadata, and internal identifiers remain private.
"""

from __future__ import annotations

import hashlib
import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
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
HTTP_TIMEOUT_SECONDS = 8.0


@dataclass(frozen=True)
class PublicProviderResult:
    """Represent a governed provider result without exposing provider internals."""

    available: bool
    payload: dict[str, Any] | None


def _fetch_json(url: str) -> dict[str, Any] | None:
    """Fetch a local provider response and fail closed on any transport error."""

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

            value = json.loads(
                response.read().decode("utf-8", "ignore")
            )
    except Exception:
        return None

    return value if isinstance(value, dict) else None


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None

    cleaned = value.strip()
    return cleaned or None


def _first_timestamp(payload: dict[str, Any]) -> str | None:
    for key in ("updated_at", "generated_at"):
        timestamp = _safe_text(payload.get(key))

        if timestamp:
            return timestamp

    return None


def governance_is_available() -> bool:
    payload = _fetch_json(GOVERNANCE_URL)

    return bool(
        payload
        and payload.get("ok") is True
        and payload.get("public_safe") is True
    )


def read_authorized_core(
    symbol: str = DEFAULT_SYMBOL,
) -> PublicProviderResult:
    """Read only the allowed_public_outputs boundary from CORE."""

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
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    authorized = payload.get("allowed_public_outputs")

    if not isinstance(authorized, dict):
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    direction = _safe_text(
        authorized.get("directional_bias")
    )
    summary = _safe_text(
        authorized.get("sanitized_summary")
    )
    updated_at = _first_timestamp(payload)

    if not direction or not summary or not updated_at:
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    public_payload = build_public_core(
        direction=direction,
        summary=summary,
        governance_available=governance_is_available(),
        evidence_available=evidence_is_available(),
        freshness_available=True,
        updated_at=updated_at,
    )

    return PublicProviderResult(
        available=True,
        payload=public_payload,
    )


def _read_completed_decisions() -> PublicProviderResult:
    payload = _fetch_json(EVIDENCE_URL)

    if not payload or payload.get("ok") is not True:
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    decisions = payload.get("decisions")

    if not isinstance(decisions, list):
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    return PublicProviderResult(
        available=True,
        payload={
            "decisions": [
                item
                for item in decisions
                if isinstance(item, dict)
            ]
        },
    )


def evidence_is_available() -> bool:
    result = _read_completed_decisions()

    return bool(
        result.available
        and result.payload is not None
    )


def read_market_context() -> PublicProviderResult:
    """Use market health only as availability/freshness evidence."""

    payload = _fetch_json(MARKET_URL)

    if not payload or payload.get("ok") is not True:
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    updated_at = _safe_text(
        payload.get("updated_at")
    )

    if not updated_at:
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    public_payload = build_market_context(
        title="سياق السوق",
        summary="سياق السوق العام متاح ومحدث من المصدر المعتمد.",
        context_series=[],
        updated_at=updated_at,
    )

    return PublicProviderResult(
        available=True,
        payload=public_payload,
    )


def _evidence_timestamp(
    item: dict[str, Any],
) -> str | None:
    for key in (
        "published_at",
        "completed_at",
        "updated_at",
        "created_at",
    ):
        timestamp = _safe_text(item.get(key))

        if timestamp:
            return timestamp

    return None


def _public_evidence_id(
    raw_identifier: str,
) -> str:
    digest = hashlib.sha256(
        raw_identifier.encode("utf-8")
    ).hexdigest()[:16]

    return f"EVID-{digest.upper()}"


def read_public_evidence() -> PublicProviderResult:
    result = _read_completed_decisions()

    if not result.available or result.payload is None:
        return PublicProviderResult(
            available=False,
            payload=None,
        )

    decisions = result.payload["decisions"]

    rows: list[dict[str, Any]] = []
    response_updated_at: str | None = None

    for index, item in enumerate(
        decisions[:20],
        start=1,
    ):
        timestamp = _evidence_timestamp(item)

        if not timestamp:
            continue

        raw_identifier = (
            _safe_text(item.get("id"))
            or _safe_text(item.get("decision_id"))
            or f"public-row-{index}-{timestamp}"
        )

        if (
            response_updated_at is None
            or timestamp > response_updated_at
        ):
            response_updated_at = timestamp

        rows.append(
            {
                "id": _public_evidence_id(
                    raw_identifier
                ),
                "source": "NDSP Public Evidence",
                "category": "Decision Evidence",
                "status": "Authorized",
                "freshness": "Available",
                "updatedAt": timestamp,
            }
        )

    payload = build_public_evidence(
        rows=rows,
        updated_at=response_updated_at,
    )

    return PublicProviderResult(
        available=True,
        payload=payload,
    )


def build_live_overview() -> dict[str, Any]:
    market = read_market_context()
    evidence = read_public_evidence()

    updated_at = None

    if (
        market.available
        and market.payload is not None
    ):
        updated_at = _safe_text(
            market.payload.get("updatedAt")
        )

    return build_public_overview(
        governance_available=governance_is_available(),
        evidence_available=evidence.available,
        freshness_available=updated_at is not None,
        trend=[],
        updated_at=updated_at,
    )

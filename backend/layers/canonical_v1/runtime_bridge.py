from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from backend.layers.canonical_v1.layer_orchestrator_v2 import (
    run_all_layers as canonical_run_all_layers,
)
from backend.layers.canonical_v1.quality.golden_signals import (
    evaluate_golden_signals,
)
from backend.layers.canonical_v1.quality.nmp_engine import calculate_nmp


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = (
    PROJECT_ROOT / "docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json"
)


def run_canonical_layers(payload: Mapping[str, Any] | None) -> dict[str, Any]:
    return canonical_run_all_layers(dict(payload or {}), REGISTRY_PATH)


def canonical_nmp_from_legacy(
    *,
    opens: Sequence[Any],
    valid: Sequence[Sequence[Any]],
    direction: str,
    timeframe: str | None,
    indicator_name: str = "RSI",
) -> dict[str, Any]:
    """Translate the legacy preprocessed arrays into the canonical NMP engine."""
    candles = [{"open": value} for value in opens]
    indicator_values: list[float | None] = [None] * len(candles)

    for row in valid:
        if not isinstance(row, (list, tuple)) or len(row) < 2:
            continue
        try:
            index = int(row[0])
        except (TypeError, ValueError):
            continue
        if 0 <= index < len(indicator_values):
            indicator_values[index] = row[1]

    return calculate_nmp(
        candles=candles,
        indicator_values=indicator_values,
        direction=direction,
        indicator_name=indicator_name,
        timeframe=timeframe,
    )


def _walk(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key), child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _normalize_direction(value: Any) -> str | None:
    raw = str(value or "").strip().lower()
    aliases = {
        "bullish": "bullish",
        "bull": "bullish",
        "up": "bullish",
        "positive": "bullish",
        "صاعد": "bullish",
        "bearish": "bearish",
        "bear": "bearish",
        "down": "bearish",
        "negative": "bearish",
        "هابط": "bearish",
        "neutral": "neutral",
        "flat": "neutral",
        "محايد": "neutral",
    }
    return aliases.get(raw)


DIRECTION_KEYS = {
    "asset_managers_overall": (
        "asset_managers_overall",
        "asset_managers_overall_direction",
        "am_overall",
        "am_overall_direction",
        "tdl_medium_long_direction",
        "tdl_ml_direction",
    ),
    "asset_managers_weekly": (
        "asset_managers_weekly",
        "asset_managers_weekly_direction",
        "am_weekly",
        "am_weekly_direction",
        "asset_manager_weekly_direction",
    ),
    "leveraged_funds_weekly": (
        "leveraged_funds_weekly",
        "leveraged_funds_weekly_direction",
        "lf_weekly",
        "lf_weekly_direction",
        "leveraged_weekly_direction",
    ),
}


def _extract_direction(payload: Mapping[str, Any], candidates: Sequence[str]) -> str | None:
    lowered = {item.lower() for item in candidates}
    for key, value in _walk(payload):
        if key.lower() not in lowered:
            continue
        if isinstance(value, Mapping):
            for nested_key in ("direction", "value", "state", "signal"):
                normalized = _normalize_direction(value.get(nested_key))
                if normalized:
                    return normalized
        normalized = _normalize_direction(value)
        if normalized:
            return normalized
    return None


def apply_canonical_golden(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Overwrite legacy heuristic Golden fields with canonical COT-direction rules."""
    data = deepcopy(dict(payload))
    am_overall = _extract_direction(data, DIRECTION_KEYS["asset_managers_overall"])
    am_weekly = _extract_direction(data, DIRECTION_KEYS["asset_managers_weekly"])
    lf_weekly = _extract_direction(data, DIRECTION_KEYS["leveraged_funds_weekly"])

    missing = [
        name
        for name, value in (
            ("asset_managers_overall", am_overall),
            ("asset_managers_weekly", am_weekly),
            ("leveraged_funds_weekly", lf_weekly),
        )
        if value is None
    ]

    if missing:
        result = {
            "golden_active": False,
            "enhanced_active": False,
            "direction": "unknown",
            "asset_managers_overall": am_overall or "unknown",
            "asset_managers_weekly": am_weekly or "unknown",
            "leveraged_funds_weekly": lf_weekly or "unknown",
            "leveraged_funds_overall_used": False,
        }
        status = "not_evaluated"
        reason_code = "MISSING_CANONICAL_COT_DIRECTIONS"
    else:
        result = evaluate_golden_signals(
            asset_managers_overall=am_overall,
            asset_managers_weekly=am_weekly,
            leveraged_funds_weekly=lf_weekly,
        )
        status = (
            "enhanced"
            if result["enhanced_active"]
            else "active"
            if result["golden_active"]
            else "inactive"
        )
        reason_code = None

    data["golden_signal"] = bool(result["golden_active"])
    data["golden_alignment_active"] = bool(result["golden_active"])
    data["enhanced_golden_signal"] = bool(result["enhanced_active"])
    data["enhanced_golden_alignment_active"] = bool(result["enhanced_active"])
    data["golden_status"] = status
    data["golden_name"] = "NAWAF_GOLDEN_SIGNAL"
    data["enhanced_golden_name"] = "NAWAF_ENHANCED_GOLDEN_SIGNAL"

    data["golden_alignment"] = {
        "golden_signal": bool(result["golden_active"]),
        "enhanced_golden_signal": bool(result["enhanced_active"]),
        "golden_alignment_active": bool(result["golden_active"]),
        "enhanced_golden_alignment_active": bool(result["enhanced_active"]),
        "golden_status": status,
        "golden_name_public": "إشارة نواف الذهبية",
        "enhanced_golden_name_public": "إشارة نواف الذهبية المعززة",
        "direction": result["direction"],
        "asset_managers_overall": result["asset_managers_overall"],
        "asset_managers_weekly": result["asset_managers_weekly"],
        "leveraged_funds_weekly": result["leveraged_funds_weekly"],
        "leveraged_funds_overall_used": False,
        "rule_golden": "AM_WEEKLY_EQUALS_LF_WEEKLY",
        "rule_enhanced": "AM_OVERALL_EQUALS_AM_WEEKLY_EQUALS_LF_WEEKLY",
        "reason_code": reason_code,
        "missing_inputs": missing,
        "decision_authority": False,
        "not_recommendation": True,
        "no_buy_sell": True,
        "source_mode": "backend.layers.canonical_v1.quality.golden_signals",
        "wrapper_version": "2.0.0-canonical-consumer",
    }

    data["_ndsp_canonical_consumer"] = {
        "enabled": True,
        "canonical_source": "backend/layers/canonical_v1",
        "nmp_engine": "quality/nmp_engine.py",
        "golden_engine": "quality/golden_signals.py",
        "layer_orchestrator": "layer_orchestrator_v2.py",
        "golden_reason_code": reason_code,
    }
    return data


def to_legacy_api_envelope(
    canonical_result: Mapping[str, Any],
    *,
    input_context_source: str | None = None,
) -> dict[str, Any]:
    """Add the legacy API envelope without changing canonical layer IDs."""
    from .registry_lock import CANONICAL_MODULES

    data = deepcopy(dict(canonical_result))
    raw_layers = data.get("layers")
    layers = raw_layers if isinstance(raw_layers, list) else []

    compatible_layers: list[dict[str, Any]] = []
    confidences: list[int] = []

    for raw_layer in layers:
        if not isinstance(raw_layer, Mapping):
            continue

        layer = deepcopy(dict(raw_layer))
        layer_id = str(layer.get("layer_id") or "")
        relative_path = CANONICAL_MODULES.get(layer_id)

        if relative_path:
            layer.setdefault(
                "module_file",
                f"canonical_v1/{relative_path}",
            )

        layer.setdefault("canonical_layer_id", layer_id)

        if layer_id.startswith("NDSP-CORE-L") and layer_id[-2:].isdigit():
            layer.setdefault("legacy_layer_number", int(layer_id[-2:]))

        try:
            confidences.append(int(float(layer.get("confidence", 0))))
        except (TypeError, ValueError):
            pass

        compatible_layers.append(layer)

    raw_errors = data.get("errors")
    errors = raw_errors if isinstance(raw_errors, list) else []

    data["layers"] = compatible_layers
    data["errors"] = errors
    data["total_layers_expected"] = int(
        data.get("total_layers_expected") or 16
    )
    data["total_layers_executed"] = len(compatible_layers)
    data["total_errors"] = len(errors)
    data["average_confidence"] = (
        int(sum(confidences) / len(confidences))
        if confidences
        else 0
    )
    data["engine_mode"] = "canonical_v1_candidate"
    data["compatibility_mode"] = "legacy_envelope_additive"

    if input_context_source is not None:
        data["input_context_source"] = input_context_source

    return data

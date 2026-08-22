from __future__ import annotations

import json
from pathlib import Path
from typing import Any


EXPECTED_IDS = [f"NDSP-CORE-L{i:02d}" for i in range(1, 17)]

CANONICAL_MODULES = {
    "NDSP-CORE-L01": "direction/l01_tdl_medium_long.py",
    "NDSP-CORE-L02": "direction/l02_tdl_short_speculative.py",
    "NDSP-CORE-L03": "direction/l03_market_direction_context.py",
    "NDSP-CORE-L04": "direction/l04_correction_gate.py",
    "NDSP-CORE-L05": "quality/l05_divergence_engine.py",
    "NDSP-CORE-L06": "direction/l06_temporal_day_logic.py",
    "NDSP-CORE-L07": "structure/l07_scenario_levels.py",
    "NDSP-CORE-L08": "structure/l08_nmp_confirmation.py",
    "NDSP-CORE-L09": "quality/l09_momentum_engine.py",
    "NDSP-CORE-L10": "quality/l10_liquidity_structure_confirmation.py",
    "NDSP-CORE-L11": "risk/l11_usd_macro_filter.py",
    "NDSP-CORE-L12": "risk/l12_risk_engine.py",
    "NDSP-CORE-L13": "quality/l13_nawaf_golden_signal.py",
    "NDSP-CORE-L14": "quality/l14_nawaf_enhanced_golden_signal.py",
    "NDSP-CORE-L15": "risk/l15_devils_advocate.py",
    "NDSP-CORE-L16": "final/l16_decision_readiness_state_machine.py",
}


def _failure(error: str) -> dict[str, Any]:
    return {
        "ok": False,
        "layer_count": 0,
        "ids": [],
        "errors": [error],
        "canonical_modules": dict(CANONICAL_MODULES),
    }


def validate_registry_lock(
    registry_path: str | Path,
    package_root: str | Path,
) -> dict[str, Any]:
    registry_path = Path(registry_path)
    package_root = Path(package_root)

    try:
        raw = registry_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _failure(f"REGISTRY_NOT_FOUND: {registry_path}")
    except (OSError, UnicodeError) as exc:
        return _failure(f"REGISTRY_READ_FAILED: {exc}")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return _failure(
            f"REGISTRY_INVALID_JSON: line={exc.lineno} column={exc.colno}"
        )

    if not isinstance(data, dict):
        return _failure("REGISTRY_INVALID_SCHEMA: top level must be an object")

    errors: list[str] = []

    for key in ("document_id", "version", "status"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"registry {key} must be a non-empty string")

    layers = data.get("layers")
    if not isinstance(layers, list):
        return _failure("REGISTRY_INVALID_SCHEMA: layers must be an array")

    ids: list[Any] = []
    names: list[Any] = []

    for index, layer in enumerate(layers):
        if not isinstance(layer, dict):
            errors.append(f"layer at index {index} must be an object")
            ids.append(None)
            names.append(None)
            continue

        ids.append(layer.get("id"))
        names.append(layer.get("canonical_name"))

    if len(layers) != 16:
        errors.append(f"registry layer count must be 16, got {len(layers)}")

    if ids != EXPECTED_IDS:
        errors.append(f"registry IDs are not contiguous L01..L16: {ids}")

    normalized_names = [
        name.strip()
        for name in names
        if isinstance(name, str) and name.strip()
    ]

    if len(normalized_names) != len(names):
        errors.append("canonical_name values must be non-empty strings")

    if len(set(normalized_names)) != len(normalized_names):
        errors.append("canonical_name values must be unique")

    for index, layer in enumerate(layers):
        if not isinstance(layer, dict):
            continue

        layer_id = layer.get("id")
        if layer_id not in CANONICAL_MODULES:
            errors.append(f"unknown layer id at index {index}: {layer_id}")
            continue

        module = package_root / CANONICAL_MODULES[layer_id]
        if not module.is_file():
            errors.append(
                f"missing canonical module for {layer_id}: {module}"
            )

    extra_ids = sorted(set(CANONICAL_MODULES) - set(ids))
    if extra_ids:
        errors.append(
            f"canonical module map has IDs absent from registry: {extra_ids}"
        )

    return {
        "ok": not errors,
        "layer_count": len(layers),
        "ids": ids,
        "errors": errors,
        "canonical_modules": dict(CANONICAL_MODULES),
    }

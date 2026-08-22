from __future__ import annotations
import importlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .registry_lock import validate_registry_lock
from .core.contracts import DecisionReadinessState

IMPORTS = {
    "NDSP-CORE-L01": "backend.layers.canonical_v1.direction.l01_tdl_medium_long",
    "NDSP-CORE-L02": "backend.layers.canonical_v1.direction.l02_tdl_short_speculative",
    "NDSP-CORE-L03": "backend.layers.canonical_v1.direction.l03_market_direction_context",
    "NDSP-CORE-L04": "backend.layers.canonical_v1.direction.l04_correction_gate",
    "NDSP-CORE-L05": "backend.layers.canonical_v1.quality.l05_divergence_engine",
    "NDSP-CORE-L06": "backend.layers.canonical_v1.direction.l06_temporal_day_logic",
    "NDSP-CORE-L07": "backend.layers.canonical_v1.structure.l07_scenario_levels",
    "NDSP-CORE-L08": "backend.layers.canonical_v1.structure.l08_nmp_confirmation",
    "NDSP-CORE-L09": "backend.layers.canonical_v1.quality.l09_momentum_engine",
    "NDSP-CORE-L10": "backend.layers.canonical_v1.quality.l10_liquidity_structure_confirmation",
    "NDSP-CORE-L11": "backend.layers.canonical_v1.risk.l11_usd_macro_filter",
    "NDSP-CORE-L12": "backend.layers.canonical_v1.risk.l12_risk_engine",
    "NDSP-CORE-L13": "backend.layers.canonical_v1.quality.l13_nawaf_golden_signal",
    "NDSP-CORE-L14": "backend.layers.canonical_v1.quality.l14_nawaf_enhanced_golden_signal",
    "NDSP-CORE-L15": "backend.layers.canonical_v1.risk.l15_devils_advocate",
    "NDSP-CORE-L16": "backend.layers.canonical_v1.final.l16_decision_readiness_state_machine",
}

ORDER = [f"NDSP-CORE-L{i:02d}" for i in range(1,17)]

def run_all_layers(payload: dict[str, Any] | None, registry_path: str | Path):
    ctx = dict(payload or {})
    package_root = Path(__file__).resolve().parent
    lock = validate_registry_lock(registry_path, package_root)
    if not lock["ok"]:
        return {"ok":False,"single_truth_state":DecisionReadinessState.DATA_BLOCKED.value,"errors":lock["errors"],"layers":[]}

    cot = ctx.get("cot_validity") or {}
    if cot and not cot.get("decision_use_allowed", False):
        return {
            "ok": False,
            "single_truth_state": DecisionReadinessState.DATA_BLOCKED.value,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "layers": [],
            "errors": [cot.get("reason_code") or "CFTC_DATA_NOT_CURRENT"],
            "data_health": {"cot": cot},
        }

    results, errors = [], []
    for layer_id in ORDER:
        try:
            mod = importlib.import_module(IMPORTS[layer_id])
            result = mod.evaluate(ctx)
            results.append(result)
            ctx[f"l{int(layer_id[-2:]):02d}"] = result.get("output", {})
        except Exception as exc:
            errors.append({"layer_id":layer_id,"error":repr(exc)})
            break

    final = (ctx.get("l16") or {}).get("single_truth_state")
    return {
        "ok": not errors and len(results)==16,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_layers_expected": 16,
        "total_layers_executed": len(results),
        "single_truth_state": final or (DecisionReadinessState.DATA_BLOCKED.value if errors else DecisionReadinessState.UNDER_REVIEW.value),
        "layers": results,
        "errors": errors,
        "context_after_layers": ctx,
    }

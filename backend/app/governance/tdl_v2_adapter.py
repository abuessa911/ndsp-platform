from __future__ import annotations

from typing import Any, Dict
from app.core.tdl_real_cot_provider import load_real_cot
from app.core.tdl_v2_policy import derive_timing_context, derive_timing_authority, read_tdl_v2_policy


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _neutral_mapping() -> Dict[str, Any]:
    return {
        "source_priority": "unavailable",
        "data_source_mode": "unavailable",
        "mapping_type": "unavailable",
        "precision_level": "unavailable",
        "lm_categories": [],
        "s_categories": [],
        "fallback_reason": "required_categories_unavailable",
    }


def _direction(value: Any) -> str:
    try:
        v = float(value or 0)
    except Exception:
        v = 0.0
    if v > 0:
        return "bullish"
    if v < 0:
        return "bearish"
    return "neutral"


def _net_from_group(group: Dict[str, Any]) -> float:
    if not isinstance(group, dict):
        return 0.0
    if "net" in group:
        try:
            return float(group.get("net") or 0)
        except Exception:
            return 0.0
    long_v = group.get("long", group.get("longs", group.get("buy", group.get("total_long", 0))))
    short_v = group.get("short", group.get("shorts", group.get("sell", group.get("total_short", 0))))
    try:
        return float(long_v or 0) - float(short_v or 0)
    except Exception:
        return 0.0


def _find_source(payload: Dict[str, Any], keys: list[str]) -> Dict[str, Any]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, dict):
            return value
    meta = _safe_dict(payload.get("meta"))
    for key in keys:
        value = meta.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _extract_positions(payload: Dict[str, Any], weekly: bool = False) -> Dict[str, Any]:
    keys = [
        "weekly_positions",
        "weekly_cot",
        "weekly_positioning",
        "partial_cot",
        "cot_weekly",
    ] if weekly else [
        "macro_positions",
        "market_positioning",
        "positioning",
        "cot_positioning",
        "macro_positioning",
    ]

    source = _find_source(payload, keys)
    if not source:
        source = _safe_dict(_safe_dict(payload.get("meta")).get("market"))

    if isinstance(source.get("macro_positioning"), dict):
        source = source["macro_positioning"]
    if isinstance(source.get("weekly_positioning"), dict):
        source = source["weekly_positioning"]

    return source if isinstance(source, dict) else {}


def _build_layer(payload: Dict[str, Any], weekly: bool = False) -> Dict[str, Any]:
    pos = _extract_positions(payload, weekly=weekly)

    # Primary detailed mapping
    asset_manager = _net_from_group(pos.get("institutional direction") or pos.get("asset_manager") or pos.get("assetManager") or {})
    other_reportables = _net_from_group(pos.get("market activity") or pos.get("other_reportables") or pos.get("otherReportables") or {})
    leveraged_funds = _net_from_group(pos.get("market momentum") or pos.get("leveraged_funds") or pos.get("leveragedFunds") or {})
    dealer = _net_from_group(pos.get("market structure") or pos.get("dealer_intermediary") or pos.get("dealerIntermediary") or {})

    has_primary = any([asset_manager, other_reportables, leveraged_funds, dealer])

    if has_primary:
        lm_net = asset_manager + other_reportables
        s_net = leveraged_funds + dealer
        mapping = {
            "source_priority": "primary",
            "data_source_mode": "detailed_cot",
            "mapping_type": "primary_mapping",
            "precision_level": "full_precision",
            "lm_categories": ["institutional direction", "market activity"],
            "s_categories": ["market momentum", "market structure"],
        }
        return {
            "lm_net": lm_net,
            "s_net": s_net,
            "lm_direction": _direction(lm_net),
            "s_direction": _direction(s_net),
            "cot_mapping": mapping,
        }

    # Fallback legacy market_positioning mapping
    institutional_positioning = _net_from_group(pos.get("institutional_positioning") or pos.get("institutional_positioning") or pos.get("Commercial") or pos.get("commercial") or {})
    non_commercials = _net_from_group(pos.get("Non-institutional_positioning") or pos.get("non_commercials") or pos.get("NonCommercials") or pos.get("nonCommercials") or {})

    has_fallback = any([institutional_positioning, non_commercials])

    if has_fallback:
        mapping = {
            "source_priority": "fallback",
            "data_source_mode": "legacy_cot",
            "mapping_type": "fallback_mapping",
            "precision_level": "reduced_precision",
            "lm_categories": ["institutional_positioning"],
            "s_categories": ["Non-institutional_positioning"],
            "fallback_reason": "detailed_categories_unavailable",
        }
        return {
            "lm_net": institutional_positioning,
            "s_net": non_commercials,
            "lm_direction": _direction(institutional_positioning),
            "s_direction": _direction(non_commercials),
            "cot_mapping": mapping,
        }

    return {
        "lm_net": 0.0,
        "s_net": 0.0,
        "lm_direction": "neutral",
        "s_direction": "neutral",
        "cot_mapping": _neutral_mapping(),
    }


def _build_tdl_v2(payload: Dict[str, Any]) -> Dict[str, Any]:
    
    symbol = str(payload.get("symbol") or "").upper()
    real_cot = load_real_cot(symbol)

    if isinstance(real_cot, dict) and real_cot:
        payload["macro_positions"] = real_cot.get("macro", {})
        payload["weekly_positions"] = real_cot.get("weekly", {})

    macro = _build_layer(payload, weekly=False)
    weekly = _build_layer(payload, weekly=True)


    lm_macro = macro["lm_direction"]
    s_macro = macro["s_direction"]
    lm_weekly = weekly["lm_direction"]
    s_weekly = weekly["s_direction"]

    lm_aligned = lm_macro != "neutral" and lm_macro == lm_weekly
    s_aligned = s_macro != "neutral" and s_macro == s_weekly
    weekly_lm_s_aligned = lm_weekly != "neutral" and lm_weekly == s_weekly

    state = "TDL_NEUTRAL"
    classification = "neutral"

    if lm_aligned and weekly_lm_s_aligned:
        state = "TDL_PREMIUM_GOLDEN_ALIGNMENT"
        classification = "premium_golden_alignment"
    elif weekly_lm_s_aligned:
        state = "TDL_GOLDEN_EXECUTION"
        classification = "weekly_execution_alignment"
    elif lm_aligned:
        state = "TDL_GOLDEN_STRUCTURAL"
        classification = "structural_alignment"
    elif (lm_macro != "neutral" and lm_weekly != "neutral" and lm_macro != lm_weekly) or (
        s_macro != "neutral" and s_weekly != "neutral" and s_macro != s_weekly
    ):
        state = "TDL_CORRECTION"
        classification = "correction"
    elif lm_macro != "neutral" or s_macro != "neutral" or lm_weekly != "neutral" or s_weekly != "neutral":
        state = "TDL_ALIGNMENT"
        classification = "partial_alignment"

    return {
        "version": "2.0",
        "model": "weekly_scalping",
        "macro": {
            "lm_direction": lm_macro,
            "s_direction": s_macro,
            "lm_net": float(macro["lm_net"]),
            "s_net": float(macro["s_net"]),
        },
        "weekly": {
            "lm_direction": lm_weekly,
            "s_direction": s_weekly,
            "lm_net": float(weekly["lm_net"]),
            "s_net": float(weekly["s_net"]),
        },
        "state": state,
        "classification": classification,
        "execution_basis": "weekly_partial_direction",
        "macro_role": "context_only",
        "holding_policy": "no_next_week_carry",
        "signals": {
            "lm_macro_weekly_aligned": bool(lm_aligned),
            "s_macro_weekly_aligned": bool(s_aligned),
            "weekly_lm_s_aligned": bool(weekly_lm_s_aligned),
        },
    }, macro["cot_mapping"], weekly["cot_mapping"]



def _derive_dominant_timed_direction(tdl_v2: Dict[str, Any], timing_authority: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dominant timed direction.

    Timing Authority determines who owns direction.
    timing_model v2 provides the actual direction values.
    """
    if not isinstance(tdl_v2, dict):
        tdl_v2 = {}
    if not isinstance(timing_authority, dict):
        timing_authority = {}

    enabled = bool(timing_authority.get("enabled"))
    controller = timing_authority.get("controller")
    source = timing_authority.get("direction_source")

    if not enabled or timing_authority.get("effect") == "bypassed":
        return {
            "enabled": False,
            "controller": "NONE",
            "source": None,
            "direction": "neutral",
            "decision_authority": "tdl_general",
            "effect": "bypassed",
            "public_note": "Timing authority is bypassed; decision may use general timing_model context."
        }

    weekly = tdl_v2.get("weekly") if isinstance(tdl_v2.get("weekly"), dict) else {}
    macro = tdl_v2.get("macro") if isinstance(tdl_v2.get("macro"), dict) else {}

    direction = "neutral"

    if controller == "S":
        direction = str(weekly.get("s_direction") or "neutral").lower()
        source = source or "weekly.s_direction"
    elif controller == "L&M":
        direction = str(weekly.get("lm_direction") or "neutral").lower()
        source = source or "weekly.lm_direction"
    elif controller == "NEUTRAL":
        direction = "neutral"
        source = None
    else:
        # Safe fallback to general timing_model if controller unknown.
        direction = str(
            weekly.get("lm_direction")
            or weekly.get("s_direction")
            or macro.get("lm_direction")
            or macro.get("s_direction")
            or "neutral"
        ).lower()
        source = source or "tdl_general"

    if direction not in {"bullish", "bearish", "neutral"}:
        direction = "neutral"

    return {
        "enabled": True,
        "controller": controller or "UNKNOWN",
        "source": source,
        "direction": direction,
        "decision_authority": timing_authority.get("decision_authority", "timing_controller"),
        "effect": "applied" if direction != "neutral" else "neutral_controller",
        "public_note": "Final decision follows the active timing_controller when its direction is available."
    }


def attach_tdl_v2_to_decision(decision_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Final timing_model v2-only output policy:
    - No legacy timing_model in final response.
    - top-level timing_model = timing_model v2.
    - meta.timing_model = timing_model v2.
    - No tdl_legacy.
    """
    if not isinstance(decision_payload, dict):
        return decision_payload

    meta = _safe_dict(decision_payload.get("meta"))
    decision_payload["meta"] = meta

    tdl_v2, cot_mapping, weekly_cot_mapping = _build_tdl_v2(decision_payload)
    policy = read_tdl_v2_policy()
    timing_filter = derive_timing_context(policy)
    timing_authority = derive_timing_authority(policy)
    tdl_v2["timing_filter"] = timing_filter
    tdl_v2["timing_authority"] = timing_authority
    dominant_timed_direction = _derive_dominant_timed_direction(tdl_v2, timing_authority)
    tdl_v2["dominant_timed_direction"] = dominant_timed_direction

    for key in (
        "tdl_legacy",
        "legacy_tdl",
        "old_tdl",
        "tdl_v1",
        "tdl_v2_integration_error",
        "tdl_legacy_preserved",
    ):
        decision_payload.pop(key, None)
        meta.pop(key, None)

    decision_payload["timing_model"] = tdl_v2
    decision_payload["cot_mapping"] = cot_mapping
    decision_payload["weekly_cot_mapping"] = weekly_cot_mapping

    meta["timing_model"] = tdl_v2
    meta["timing_filter"] = timing_filter
    meta["timing_authority"] = timing_authority
    meta["dominant_timed_direction"] = dominant_timed_direction
    meta["cot_mapping"] = cot_mapping
    meta["weekly_cot_mapping"] = weekly_cot_mapping
    meta["tdl_output_policy"] = "tdl_v2_only"
    meta["tdl_previous_removed"] = True
    meta["tdl_v2_policy"] = {
        "tdl_v2_enabled": bool(policy.get("tdl_v2_enabled", True)),
        "timing_layer_enabled": bool(policy.get("timing_layer_enabled", True)),
        "timing_mode": policy.get("timing_mode", "control_days"),
    }

    # Ensure no explicit duplicate alias remains.
    meta.pop("tdl_v2", None)

    return decision_payload

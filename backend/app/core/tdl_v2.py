from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Any

Direction = Literal["bullish", "bearish", "neutral"]

PRIMARY_LM = ["institutional direction", "market activity"]
PRIMARY_S = ["market momentum", "market structure"]
FALLBACK_LM = ["institutional_positioning"]
FALLBACK_S = ["Non-institutional_positioning"]


def _norm_category(name: str) -> str:
    return " ".join(str(name).replace("_", " ").replace("-", " ").split()).lower()

def _has_categories(positioning: Dict[str, Any], categories: List[str]) -> bool:
    keys = {_norm_category(k) for k in positioning.keys()}
    return all(_norm_category(c) in keys for c in categories)


def _get_group(positioning: Dict[str, Any], category: str) -> Dict[str, float]:
    target = _norm_category(category)
    for key, value in positioning.items():
        if _norm_category(key) == target:
            return value or {}
    return {}


def _net_for_categories(positioning: Dict[str, Any], categories: List[str]) -> float:
    total = 0.0
    for category in categories:
        row = _get_group(positioning, category)
        long_value = float(row.get("long", row.get("longs", row.get("total_long", 0))) or 0)
        short_value = float(row.get("short", row.get("shorts", row.get("total_short", 0))) or 0)
        total += long_value - short_value
    return total

def _direction_from_net(net: float, neutral_threshold: float = 0.0) -> Direction:
    if net > neutral_threshold:
        return "bullish"
    if net < -neutral_threshold:
        return "bearish"
    return "neutral"


def detect_cot_mapping(positioning: Dict[str, Any]) -> Dict[str, Any]:
    if _has_categories(positioning, PRIMARY_LM + PRIMARY_S):
        return {
            "source_priority": "primary",
            "data_source_mode": "detailed_cot",
            "mapping_type": "primary_mapping",
            "precision_level": "full_precision",
            "lm_categories": PRIMARY_LM,
            "s_categories": PRIMARY_S,
            "fallback_available": True,
        }
    if _has_categories(positioning, FALLBACK_LM + FALLBACK_S):
        return {
            "source_priority": "fallback",
            "data_source_mode": "legacy_cot",
            "mapping_type": "fallback_mapping",
            "precision_level": "reduced_precision",
            "lm_categories": FALLBACK_LM,
            "s_categories": FALLBACK_S,
            "fallback_reason": "detailed_categories_unavailable",
        }
    return {
        "source_priority": "unavailable",
        "data_source_mode": "unavailable",
        "mapping_type": "unavailable",
        "precision_level": "unavailable",
        "lm_categories": [],
        "s_categories": [],
        "fallback_reason": "required_categories_unavailable",
    }


def build_macro_direction(positioning: Dict[str, Any], neutral_threshold: float = 0.0) -> Dict[str, Any]:
    mapping = detect_cot_mapping(positioning)
    if mapping["source_priority"] == "unavailable":
        return {
            "lm_direction": "neutral",
            "s_direction": "neutral",
            "lm_net": 0.0,
            "s_net": 0.0,
            "cot_mapping": mapping,
        }
    lm_net = _net_for_categories(positioning, mapping["lm_categories"])
    s_net = _net_for_categories(positioning, mapping["s_categories"])
    return {
        "lm_direction": _direction_from_net(lm_net, neutral_threshold),
        "s_direction": _direction_from_net(s_net, neutral_threshold),
        "lm_net": lm_net,
        "s_net": s_net,
        "cot_mapping": mapping,
    }

def classify_tdl_v2(
    lm_macro: Direction,
    s_macro: Direction,
    lm_weekly: Direction,
    s_weekly: Direction,
) -> Dict[str, Any]:
    neutral_seen = "neutral" in {lm_macro, s_macro, lm_weekly, s_weekly}
    lm_macro_weekly_aligned = lm_macro == lm_weekly and lm_macro != "neutral"
    s_macro_weekly_aligned = s_macro == s_weekly and s_macro != "neutral"
    weekly_lm_s_aligned = lm_weekly == s_weekly and lm_weekly != "neutral"

    # Layer 5.6: Participant Conflict State (صراع المتداولين)
    participant_conflict = (lm_weekly != s_weekly) and (lm_weekly != "neutral") and (s_weekly != "neutral")

    # Layer 5.7: Nawaf Golden Alignment
    golden_alignment_active = weekly_lm_s_aligned

    if neutral_seen and not weekly_lm_s_aligned and not lm_macro_weekly_aligned:
        state = "TDL_NEUTRAL"
        classification = "neutral"
    elif lm_macro_weekly_aligned and weekly_lm_s_aligned:
        state = "TDL_PREMIUM_GOLDEN_ALIGNMENT"
        classification = "weekly_execution_alignment"
    elif weekly_lm_s_aligned:
        state = "TDL_GOLDEN_EXECUTION"
        classification = "weekly_execution_alignment"
    elif lm_macro_weekly_aligned:
        state = "TDL_GOLDEN_STRUCTURAL"
        classification = "structural_continuation"
    elif (lm_macro != lm_weekly and lm_weekly != "neutral") or (s_macro != s_weekly and s_weekly != "neutral"):
        state = "TDL_CORRECTION"
        classification = "correction"
    else:
        state = "TDL_CONTEXT_ONLY"
        classification = "context_only"

    return {
        "version": "4.1", 
        "model": "weekly_scalping",
        
        # التزام المادة الثانية: تصدير مخرجات الطبقة الخامسة صراحة لتستهلكها الطبقة 13
        "layer_5_output": {
            "lm_direction": lm_weekly,
            "s_direction": s_weekly,
            "participant_conflict": participant_conflict,
            "golden_alignment_active": golden_alignment_active
        },
        
        "macro": {"lm_direction": lm_macro, "s_direction": s_macro},
        "weekly": {"lm_direction": lm_weekly, "s_direction": s_weekly},
        "state": state,
        "classification": classification,
        "execution_basis": "weekly_partial_direction",
        "macro_role": "context_only",
        "holding_policy": "no_next_week_carry",
        "signals": {
            "lm_macro_weekly_aligned": lm_macro_weekly_aligned,
            "s_macro_weekly_aligned": s_macro_weekly_aligned,
            "weekly_lm_s_aligned": weekly_lm_s_aligned,
        },
    }

def evaluate_tdl_v2(
    macro_positioning: Optional[Dict[str, Any]] = None,
    weekly_positioning: Optional[Dict[str, Any]] = None,
    neutral_threshold: float = 0.0,
) -> Dict[str, Any]:
    """
    المنفذ الرئيسي لتقييم timing_model. يقرأ بيانات الـ market_positioning ويصدر عقد الطبقة الخامسة.
    """
    macro_positioning = macro_positioning or {}
    weekly_positioning = weekly_positioning or macro_positioning

    macro = build_macro_direction(macro_positioning, neutral_threshold)
    weekly = build_macro_direction(weekly_positioning, neutral_threshold)

    timing_model = classify_tdl_v2(
        macro["lm_direction"],
        macro["s_direction"],
        weekly["lm_direction"],
        weekly["s_direction"],
    )
    timing_model["macro"]["lm_net"] = macro["lm_net"]
    timing_model["macro"]["s_net"] = macro["s_net"]
    timing_model["weekly"]["lm_net"] = weekly["lm_net"]
    timing_model["weekly"]["s_net"] = weekly["s_net"]
    
    return {
        "timing_model": timing_model, 
        "cot_mapping": macro["cot_mapping"], 
        "weekly_cot_mapping": weekly["cot_mapping"]
    }

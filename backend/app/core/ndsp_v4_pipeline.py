import uuid
import time
from typing import Dict, Any
from datetime import datetime, timezone

# 1. محاولة استيراد timing_model (إذا لم يوجد بعد نستخدم محاكاة للاختبار)
try:
    from app.core.tdl_v2 import evaluate_tdl_v2
except ImportError:
    def evaluate_tdl_v2(macro_positioning=None, weekly_positioning=None, **kwargs):
        return {
            "timing_model": {
                "layer_5_output": {
                    "lm_direction": "bullish",
                    "s_direction": "bearish",
                    "participant_conflict": True,
                    "golden_alignment_active": False
                }
            }
        }

# 2. محاولة استيراد طبقة المخاطر (risk shield)
try:
    from app.core.ndsp_layer_12_14_risk_gov import evaluate_system_risk
except ImportError:
    def evaluate_system_risk(timing, health, market):
        penalty = 30 if market.get("volatility_spike") else 0
        state = "caution" if penalty > 0 else "normal"
        return {
            "governance_output": {
                "risk_state": state,
                "decision_state": "ACTIVE_CAUTION" if state == "caution" else "ACTIVE",
                "execution_allowed": False,
                "execution_mode": "decision_support_only",
                "black_layer_penalty": penalty,
                "flags": {"blocked_reasons": [], "caution_reasons": []}
            }
        }

def get_timing_authority(symbol: str) -> dict:
    current_utc = datetime.now(timezone.utc)
    day_of_week = current_utc.weekday()
    if day_of_week in [0, 4]:
        controller = "L&M"
        day_group = "Institutional (Mon/Fri)"
    else:
        controller = "S"
        day_group = "Speculative (Tue/Wed/Thu/Sat/Sun)"
    return {
        "controller": controller, "effect": "active",
        "day_group": day_group, "timestamp_utc": current_utc.isoformat()
    }

def resolve_dominant_direction(timing: dict, tdl_result: dict) -> dict:
    controller = timing.get("controller", "NEUTRAL")
    layer_5_output = tdl_result.get("timing_model", {}).get("layer_5_output", {})
    lm_dir = layer_5_output.get("lm_direction", "neutral")
    s_dir = layer_5_output.get("s_direction", "neutral")
    
    final_direction = lm_dir if controller == "L&M" else s_dir
    source = f"weekly.{controller.lower()}_direction"
    
    return {"direction": final_direction, "source": source, "controller": controller}

def compute_decision_quality(tdl_result: dict, black_layer_penalty: int = 0) -> dict:
    layer_5_output = tdl_result.get("timing_model", {}).get("layer_5_output", {})
    conflict = layer_5_output.get("participant_conflict", False)
    golden = layer_5_output.get("golden_alignment_active", False)
    
    base_confidence = 50
    if golden: base_confidence += 15
    if conflict: base_confidence -= 12
    base_confidence -= black_layer_penalty
    
    final_confidence = max(0, min(100, base_confidence))
    grade = "F"
    if final_confidence >= 85: grade = "A"
    elif final_confidence >= 70: grade = "B"
    elif final_confidence >= 55: grade = "C"
    elif final_confidence >= 40: grade = "D"
    
    return {"final_confidence": int(final_confidence), "grade": grade, "quality_label": "Tested"}

def run_ndsp_v4_pipeline(symbol: str, raw_cot_data: dict = None, data_health: dict = None, market_conditions: dict = None) -> dict:
    timing = get_timing_authority(symbol)
    timing_model = evaluate_tdl_v2(macro_positioning=raw_cot_data, weekly_positioning=raw_cot_data)
    direction = resolve_dominant_direction(timing, timing_model)
    
    health = data_health or {"cot_age_hours": 24}
    market = market_conditions or {"volatility_spike": False, "low_liquidity": False}
    risk_gov = evaluate_system_risk(timing, health, market)
    gov_out = risk_gov["governance_output"]

    quality = compute_decision_quality(timing_model, black_layer_penalty=gov_out["black_layer_penalty"])
    
    return {
        "contract_id": f"NDSP-V4.1-{uuid.uuid4().hex[:8].upper()}",
        "timestamp_utc": int(time.time() * 1000),
        "symbol": symbol.upper(),
        "decision": {
            "direction": direction["direction"],
            "direction_source": direction["source"],
            "timing_controller": direction["controller"],
            "confidence": quality["final_confidence"],
            "grade": quality["grade"],
            "quality_label": quality["quality_label"],
            "risk_state": gov_out["risk_state"],
            "decision_state": gov_out["decision_state"],
            "execution_allowed": gov_out["execution_allowed"],
            "execution_mode": gov_out["execution_mode"]
        }
    }

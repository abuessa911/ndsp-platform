from __future__ import annotations


def run_phase_layer(timing_model: dict) -> dict:
    lm = timing_model.get("tdl_lm_direction", "neutral")
    s = timing_model.get("tdl_s_direction", "neutral")

    lm_score = timing_model.get("tdl_lm_score_total", 0)
    lm_change = timing_model.get("tdl_lm_score_change", 0)

    ########################################
    # GOLDEN
    ########################################
    if lm == "bullish" and s == "bullish":
        phase = "NDSP_GOLDEN_SIGNAL"

    elif lm == "bearish" and s == "bearish":
        phase = "NDSP_GOLDEN_SIGNAL"

    ########################################
    # 🔥 PULLBACK (المهم)
    ########################################
    elif lm == "bearish" and s == "bullish":
        phase = "PULLBACK_UP"

    elif lm == "bullish" and s == "bearish":
        phase = "PULLBACK_DOWN"

    ########################################
    else:
        phase = "RANGE"

    return {
        "phase": phase,
        "tdl_lm_score_total": lm_score,
        "tdl_lm_score_change": lm_change,
        "source": "tdl_only"
    }

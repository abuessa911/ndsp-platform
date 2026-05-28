def calculate_cot_tdl(data: dict) -> dict:
    """
    FINAL market_positioning timing_model ENGINE
    يدعم:
    - manual weekly (primary)
    - fallback logic
    """

    data = data or {}

    # =========================
    # 🔥 MANUAL OVERRIDE (الأهم)
    # =========================
    manual_lm = data.get("manual_lm") or {}
    manual_s = data.get("manual_s") or {}

    if manual_lm and manual_s:

        lm_total = float(manual_lm.get("tdl_lm_score_total", 0))
        lm_change = float(manual_lm.get("tdl_lm_score_change", 0))

        s_total = float(manual_s.get("tdl_s_score_total", 0))
        s_change = float(manual_s.get("tdl_s_score_change", 0))

        lm_dir = manual_lm.get("tdl_lm_direction", "neutral")
        s_dir = manual_s.get("tdl_s_direction", "neutral")

        # =========================
        # DOMINANCE
        # =========================
        if abs(s_total) > abs(lm_total):
            dominant = "timing_model-S"
            dominant_side = "timing_model-S"
        elif abs(lm_total) > abs(s_total):
            dominant = "timing_model-L&M"
            dominant_side = "timing_model-L&M"
        else:
            dominant = "NEUTRAL"
            dominant_side = "NEUTRAL"

        return {
            "tdl_lm_score": lm_total,
            "tdl_s_score": s_total,

            "tdl_lm_score_total": lm_total,
            "tdl_lm_score_change": lm_change,

            "tdl_s_score_total": s_total,
            "tdl_s_score_change": s_change,

            "tdl_lm_direction": lm_dir,
            "tdl_s_direction": s_dir,

            "dominant": dominant,
            "dominant_side": dominant_side,

            "golden_signal": False,
            "golden_name": None,

            "manual_lm": manual_lm,
            "manual_s": manual_s,

            "model": "cot_manual_override_v1"
        }

    # =========================
    # ❌ FALLBACK (لو ما فيه manual)
    # =========================
    return {
        "tdl_lm_score": 0,
        "tdl_s_score": 0,

        "tdl_lm_score_total": 0,
        "tdl_lm_score_change": 0,

        "tdl_s_score_total": 0,
        "tdl_s_score_change": 0,

        "tdl_lm_direction": "neutral",
        "tdl_s_direction": "neutral",

        "dominant": "UNKNOWN",
        "dominant_side": "UNKNOWN",

        "golden_signal": False,
        "golden_name": None,

        "model": "cot_fallback_empty"
    }

LAYER_ID = 6
LAYER_NAME = "Direction Day Authority"
LAYER_NAME_AR = "سلطة الاتجاه حسب يوم السيطرة"

def _get(payload, *keys, default=None):
    for k in keys:
        if isinstance(payload, dict) and k in payload and payload.get(k) is not None:
            return payload.get(k)
    return default

def _up(x):
    return str(x or "").upper()

def _compute(payload=None):
    payload = dict(payload or {})

    weekly = _up(_get(payload, "weekly_partial_direction", "tdl_bias", default="NEUTRAL"))
    weekly_ar = _get(payload, "weekly_partial_direction_ar", "tdl_bias_ar", default="محايد")
    overall = _up(_get(payload, "overall_trend_direction", default="NEUTRAL"))
    overall_ar = _get(payload, "overall_trend_direction_ar", default="محايد")
    movement = _get(payload, "movement_type", default="WATCH_ONLY")
    movement_ar = _get(payload, "movement_type_ar", default="مراقبة فقط")
    timing_allowed = bool(_get(payload, "timing_allowed", default=False))

    controlling_group = _get(payload, "controlling_group", "day_authority", default="UNKNOWN")
    controlling_group_ar = _get(payload, "controlling_group_ar", "day_authority_ar", default="غير معروف")
    weekday = _get(payload, "weekday", default=None)
    weekday_ar = _get(payload, "weekday_ar", default=None)
    authority_reason_ar = _get(payload, "authority_reason_ar", default=None)

    if timing_allowed and weekly in ("BULLISH", "BEARISH"):
        dominant = weekly
        dominant_ar = weekly_ar
        status = "ACTIVE_STRONG"
        confidence = 92
        blocking_factors = []
        supporting_factors = [
            f"اليوم: {weekday_ar or weekday}.",
            f"الفئة الحاكمة اليوم: {controlling_group_ar}.",
            f"سبب السلطة: {authority_reason_ar}.",
            f"اتجاه الفئة الحاكمة: {weekly_ar}.",
        ]
    else:
        dominant = "NEUTRAL"
        dominant_ar = "محايد"
        status = "CAUTION"
        confidence = 58
        blocking_factors = ["لا توجد سلطة يومية واضحة أو اتجاه أسبوعي صالح للفئة الحاكمة."]
        supporting_factors = []

    output = {
        "weekday": weekday,
        "weekday_ar": weekday_ar,
        "day_authority": controlling_group,
        "day_authority_ar": controlling_group_ar,
        "controlling_group": controlling_group,
        "controlling_group_ar": controlling_group_ar,
        "authority_reason_ar": authority_reason_ar,
        "dominant_direction": dominant,
        "dominant_direction_ar": dominant_ar,
        "direction_authority": "DAY_AUTHORITY_CONTROLLING_GROUP",
        "overall_trend_direction": overall,
        "overall_trend_direction_ar": overall_ar,
        "weekly_partial_direction": weekly,
        "weekly_partial_direction_ar": weekly_ar,
        "movement_type": movement,
        "movement_type_ar": movement_ar,
        "decision_basis": "DAY_AUTHORITY_CONTROLLING_GROUP_WEEKLY_DIRECTION",
        "timing_allowed": timing_allowed,
        "blocking_factors": blocking_factors,
        "supporting_factors": supporting_factors,
    }
    return status, confidence, output

def evaluate(payload=None):
    status, confidence, output = _compute(payload)
    return {
        "layer_id": LAYER_ID,
        "layer_name": LAYER_NAME,
        "status": status,
        "confidence": confidence,
        "output": output,
    }

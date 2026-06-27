


from __future__ import annotations


# NDSP runtime compatibility helper - required by Layer 8 NMP
def _float(v, default=0.0):
    try:
        return float(str(v).replace(",", "").strip())
    except Exception:
        return default


"""
NDSP — Latest 16 Backend Layer Logic Functions
نسخة دوال المنطق المحدثة للطبقات الـ16
الغرض:
- هذا الملف مرجعي للمالك والمطور.
- يحتوي دوال منطق قابلة للنسخ داخل ملفات الطبقات.
- كل دالة ترجع dict موحد جاهز للربط مع الواجهة أو layer_orchestrator.
ملاحظة:
- هذه الدوال لا تغيّر قاعدة البيانات.
- هذه الدوال لا تعتمد على واجهة المستخدم.
- يمكن استخدامها كمرجع أو استيرادها من ملفات الطبقات.
"""

from datetime import datetime, timezone
from typing import Any, Mapping


# ============================================================
# Helpers
# ============================================================

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(float(value))
    except Exception:
        return default


def _text(value: Any, default: str = "neutral") -> str:
    if value is None:
        return default
    value = str(value).strip()
    return value if value else default


def _bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "ok", "active", "enabled", "نعم", "صحيح", "مفعل"}


def _get(payload: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in payload and payload.get(key) is not None:
            return payload.get(key)
    return default


def _clamp(value: float, lo: int = 0, hi: int = 100) -> int:
    return int(max(lo, min(hi, value)))


def _direction(value: Any) -> str:
    v = _text(value, "neutral").lower()
    bullish = {"bullish", "up", "long", "buy", "positive", "supportive", "صاعد", "شراء", "داعم", "إيجابي", "ايجابي"}
    bearish = {"bearish", "down", "short", "sell", "negative", "pressure", "هابط", "بيع", "سلبي", "ضغط"}
    if v in bullish:
        return "BULLISH"
    if v in bearish:
        return "BEARISH"
    return "NEUTRAL"


def _status_from_score(score: float) -> str:
    if score >= 80:
        return "ACTIVE_STRONG"
    if score >= 65:
        return "ACTIVE"
    if score >= 45:
        return "CAUTION"
    return "LOW_CONFIDENCE"


def _layer_result(
    layer_id: int,
    layer_name: str,
    short_name: str,
    arabic_name: str,
    primary_output: str,
    output: dict[str, Any],
    score: float,
    signals: list[str] | None = None,
    warnings: list[str] | None = None,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    confidence = _clamp(score)
    return {
        "layer_id": layer_id,
        "layer_name": layer_name,
        "short_name": short_name,
        "arabic_name": arabic_name,
        "status": _status_from_score(confidence),
        "score": confidence,
        "confidence": confidence,
        "primary_output": primary_output,
        "output": output,
        "signals": signals or [],
        "warnings": warnings or [],
        "evidence": evidence or {},
        "generated_at": _now(),
    }


# ============================================================
# Layer 1 — Source Authority / Data Source Integrity
# File: backend/layers/data/l1_source.py
# ============================================================

def evaluate_l1_source(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    live_price = _num(_get(payload, "live_price", "price", "current_price", default=0), 0)
    sources_connected = _bool(_get(payload, "sources_connected", "data_connected", default=True), True)
    data_is_fresh = _bool(_get(payload, "data_is_fresh", "fresh", default=True), True)
    feed_age_seconds = _int(_get(payload, "feed_age_seconds", "age_seconds", default=30), 30)

    score = 100
    warnings = []
    signals = []

    if live_price <= 0:
        score -= 35
        warnings.append("Live price is missing or invalid.")
    else:
        signals.append("Live price is available.")

    if not sources_connected:
        score -= 30
        warnings.append("One or more data sources are disconnected.")
    else:
        signals.append("Data sources are connected.")

    if not data_is_fresh or feed_age_seconds > 300:
        score -= 25
        warnings.append("Data freshness is degraded.")
    else:
        signals.append("Data freshness is acceptable.")

    output = {
        "source_state": "CONNECTED" if score >= 70 else "DEGRADED",
        "live_price": live_price,
        "sources_connected": sources_connected,
        "data_is_fresh": data_is_fresh,
        "feed_age_seconds": feed_age_seconds,
    }

    return _layer_result(
        1,
        "Source Authority",
        "L1_SOURCE",
        "سلطة المصدر",
        "source_integrity_state",
        output,
        score,
        signals,
        warnings,
        {"input_keys": sorted(payload.keys())},
    )


# ============================================================
# Layer 2 — Session Authority
# File: backend/layers/data/l2_session.py
# ============================================================

def evaluate_l2_session(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    session = _text(_get(payload, "session", "market_session", default="unknown")).lower()
    asset = _text(_get(payload, "asset", "symbol", default="GOLD"))
    asset_class = _text(_get(payload, "asset_class", default="commodity")).lower()
    is_crypto = _bool(_get(payload, "is_crypto", default=False), False) or "crypto" in asset_class or asset.upper() in {"BTC", "ETH", "SOL", "BNB"}

    high_activity_sessions = {"london", "new_york", "ny", "us", "eu", "overlap", "london-new_york"}
    medium_activity_sessions = {"asia", "tokyo", "pre_market", "after_hours"}

    if is_crypto:
        state = "ALWAYS_OPEN"
        score = 82
        signals = ["Crypto market is continuous; session authority remains active."]
        warnings = []
    elif session in high_activity_sessions:
        state = "HIGH_ACTIVITY"
        score = 88
        signals = [f"Session {session} has high activity."]
        warnings = []
    elif session in medium_activity_sessions:
        state = "MEDIUM_ACTIVITY"
        score = 68
        signals = [f"Session {session} has medium activity."]
        warnings = []
    else:
        state = "UNKNOWN_OR_LOW_ACTIVITY"
        score = 45
        signals = []
        warnings = ["Session is unknown or low-activity."]

    output = {
        "asset": asset,
        "asset_class": asset_class,
        "session": session,
        "session_state": state,
        "is_crypto": is_crypto,
    }

    return _layer_result(
        2,
        "Session Authority",
        "L2_SESSION",
        "سلطة الجلسة",
        "session_authority_state",
        output,
        score,
        signals,
        warnings,
    )


# ============================================================
# Layer 3 — Timing Authority
# File: backend/layers/direction/l3_timing.py
# ============================================================

def evaluate_l3_timing(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    day = _text(_get(payload, "weekday", "day", default=datetime.now(timezone.utc).strftime("%A"))).lower()
    asset = _text(_get(payload, "asset", "symbol", default="GOLD"))
    asset_class = _text(_get(payload, "asset_class", default="commodity")).lower()
    is_crypto = _bool(_get(payload, "is_crypto", default=False), False) or "crypto" in asset_class or asset.upper() in {"BTC", "ETH", "SOL", "BNB"}

    asset_manager_days = {"monday", "mon", "friday", "fri", "الاثنين", "الإثنين", "الجمعة"}
    leveraged_days = {"tuesday", "tue", "wednesday", "wed", "thursday", "thu", "الثلاثاء", "الأربعاء", "الاربعاء", "الخميس"}
    weekend_days = {"saturday", "sat", "sunday", "sun", "السبت", "الأحد", "الاحد"}

    if day in asset_manager_days:
        group = "ASSET_MANAGERS"
        timing_bias = "INSTITUTIONAL_LONG_HORIZON"
        allowed = True
        score = 86
    elif day in leveraged_days:
        group = "LEVERAGED_FUNDS"
        timing_bias = "SPECULATIVE_WEEKLY_HORIZON"
        allowed = True
        score = 82
    elif day in weekend_days and is_crypto:
        group = "LEVERAGED_FUNDS"
        timing_bias = "CRYPTO_WEEKEND_SPECULATIVE_HORIZON"
        allowed = True
        score = 74
    else:
        group = "NO_PRIMARY_TIMING_AUTHORITY"
        timing_bias = "LOW_AUTHORITY"
        allowed = False
        score = 42

    output = {
        "weekday": day,
        "asset": asset,
        "controlling_group": group,
        "timing_bias": timing_bias,
        "allowed": allowed,
    }

    signals = [f"Timing group resolved as {group}."]
    warnings = [] if allowed else ["No strong timing authority for this asset/day combination."]

    return _layer_result(
        3,
        "Timing Authority",
        "L3_TIMING",
        "سلطة التوقيت",
        "timing_authority_state",
        output,
        score,
        signals,
        warnings,
    )



# ============================================================
# NDSP TDL Governance V3
# الاتجاه الكلي = إجمالي Long الحالي مقابل إجمالي Short الحالي
# الاتجاه الأسبوعي = تغير Long وتغير Short في آخر تقرير
# اعتماد السكالبينق الأسبوعي = الاتجاه الأسبوعي
# الاتجاه الكلي يحدد: استمرار أو تصحيح
# ============================================================

def _ndsp_num(v, default=0.0):
    try:
        return float(str(v).replace(",", "").strip())
    except Exception:
        return default


def _ndsp_pick(payload, *keys, default=None):
    for k in keys:
        if k in payload and payload.get(k) not in (None, ""):
            return payload.get(k)
    return default


def _ndsp_direction_from_long_short(long_value, short_value):
    # قاعدة NDSP الصحيحة:
    # الاتجاه لا يحسب بالطرح، بل بالمقارنة المباشرة.
    # إذا Long أكبر => صاعد.
    # إذا Short أكبر => هابط.
    long_value = _ndsp_num(long_value)
    short_value = _ndsp_num(short_value)

    if long_value > short_value:
        return "BULLISH", {
            "dominant_side": "LONG",
            "long_value": long_value,
            "short_value": short_value,
            "comparison_rule": "LONG_GREATER_THAN_SHORT",
            "comparison_gap_for_display_only": abs(long_value - short_value),
        }

    if short_value > long_value:
        return "BEARISH", {
            "dominant_side": "SHORT",
            "long_value": long_value,
            "short_value": short_value,
            "comparison_rule": "SHORT_GREATER_THAN_LONG",
            "comparison_gap_for_display_only": abs(short_value - long_value),
        }

    return "NEUTRAL", {
        "dominant_side": "EQUAL",
        "long_value": long_value,
        "short_value": short_value,
        "comparison_rule": "LONG_EQUALS_SHORT",
        "comparison_gap_for_display_only": 0,
    }


def _ndsp_weekly_direction_from_changes(change_long, change_short):
    # قاعدة NDSP الصحيحة للاتجاه الأسبوعي:
    # ليست عملية طرح.
    # نقارن تغير Long مع تغير Short كما هما.
    # إذا تغير Long أكبر => صاعد أسبوعي.
    # إذا تغير Short أكبر => هابط أسبوعي.
    change_long = _ndsp_num(change_long)
    change_short = _ndsp_num(change_short)

    if change_long > change_short:
        return "BULLISH", {
            "dominant_side": "LONG_CHANGE",
            "change_long": change_long,
            "change_short": change_short,
            "comparison_rule": "CHANGE_LONG_GREATER_THAN_CHANGE_SHORT",
            "comparison_gap_for_display_only": abs(change_long - change_short),
        }

    if change_short > change_long:
        return "BEARISH", {
            "dominant_side": "SHORT_CHANGE",
            "change_long": change_long,
            "change_short": change_short,
            "comparison_rule": "CHANGE_SHORT_GREATER_THAN_CHANGE_LONG",
            "comparison_gap_for_display_only": abs(change_short - change_long),
        }

    return "NEUTRAL", {
        "dominant_side": "EQUAL_CHANGE",
        "change_long": change_long,
        "change_short": change_short,
        "comparison_rule": "CHANGE_LONG_EQUALS_CHANGE_SHORT",
        "comparison_gap_for_display_only": 0,
    }


def _ndsp_movement_type(overall_direction, weekly_direction):
    overall_direction = str(overall_direction or "NEUTRAL").upper()
    weekly_direction = str(weekly_direction or "NEUTRAL").upper()

    if overall_direction == "NEUTRAL" or weekly_direction == "NEUTRAL":
        return "غير واضح", "WATCH_ONLY"

    if overall_direction == weekly_direction:
        return "استمرار أسبوعي مع الاتجاه الكلي", "WEEKLY_CONTINUATION"

    return "تصحيح أسبوعي داخل الاتجاه الكلي", "WEEKLY_CORRECTION"


def _ndsp_bias_ar(x):
    x = str(x or "").upper()
    if x == "BULLISH":
        return "صاعد"
    if x == "BEARISH":
        return "هابط"
    if x == "NEUTRAL":
        return "محايد"
    return "غير متاح"


def _ndsp_movement_ar(x):
    x = str(x or "").upper()
    if x == "WEEKLY_CORRECTION":
        return "تصحيح أسبوعي"
    if x == "WEEKLY_CONTINUATION":
        return "استمرار أسبوعي"
    if x == "WATCH_ONLY":
        return "مراقبة فقط"
    return "غير واضح"


def _ndsp_extract_group_numbers(payload, group):
    # يدعم عدة أسماء محتملة من Raw COT أو من طبقة الربط
    g = str(group or "").lower()

    aliases = {
        "asset_managers": [
            "asset_managers", "asset_manager", "asset_manager_institutional",
            "am", "long_term", "ml"
        ],
        "leveraged_funds": [
            "leveraged_funds", "leveraged", "lev_funds", "speculative",
            "short_term", "s"
        ],
        "dealer_intermediary": [
            "dealer_intermediary", "dealer", "dealers"
        ],
    }

    prefixes = aliases.get(g, [g])

    def find_value(suffixes):
        for pref in prefixes:
            for suf in suffixes:
                keys = [
                    f"{pref}_{suf}",
                    f"{pref}.{suf}",
                    f"{pref}:{suf}",
                ]
                for k in keys:
                    if k in payload and payload.get(k) not in (None, ""):
                        return payload.get(k)

        # مفاتيح سياقية سبق استعمالها
        if g == "asset_managers":
            for k in suffixes:
                for kk in [
                    f"raw_cot_asset_managers_{k}",
                    f"context_asset_managers_{k}",
                    f"asset_managers_{k}",
                ]:
                    if kk in payload and payload.get(kk) not in (None, ""):
                        return payload.get(kk)

        if g == "leveraged_funds":
            for k in suffixes:
                for kk in [
                    f"raw_cot_leveraged_funds_{k}",
                    f"context_leveraged_funds_{k}",
                    f"leveraged_funds_{k}",
                ]:
                    if kk in payload and payload.get(kk) not in (None, ""):
                        return payload.get(kk)

        return None

    long_current = find_value(["long", "longs", "current_long", "positions_long"])
    short_current = find_value(["short", "shorts", "current_short", "positions_short"])
    change_long = find_value(["change_long", "long_change", "change_in_long", "weekly_change_long"])
    change_short = find_value(["change_short", "short_change", "change_in_short", "weekly_change_short"])

    return {
        "long": long_current,
        "short": short_current,
        "change_long": change_long,
        "change_short": change_short,
        "has_current_totals": long_current is not None and short_current is not None,
        "has_weekly_changes": change_long is not None and change_short is not None,
    }



# ============================================================
# Layer 4 — COT / Positioning Manager
# File: backend/layers/data/l4_cot_manager.py
# ============================================================


def _ndsp_weekly_bias_ar_with_scope(weekly_direction, overall_direction, movement_type):
    weekly_direction = str(weekly_direction or "").upper()
    overall_direction = str(overall_direction or "").upper()
    movement_type = str(movement_type or "").upper()

    if movement_type == "WEEKLY_CORRECTION":
        if weekly_direction == "BULLISH":
            return "صاعد غير صريح / ذو أفق ضيق"
        if weekly_direction == "BEARISH":
            return "هابط غير صريح / ذو أفق ضيق"

    if weekly_direction == "BULLISH":
        return "صاعد"
    if weekly_direction == "BEARISH":
        return "هابط"
    if weekly_direction == "NEUTRAL":
        return "محايد"
    return "غير متاح"


def _ndsp_tdl_reading_ar(overall_direction, weekly_direction, movement_type):
    overall_ar = _ndsp_bias_ar(overall_direction)
    weekly_scope_ar = _ndsp_weekly_bias_ar_with_scope(weekly_direction, overall_direction, movement_type)
    movement_type = str(movement_type or "").upper()

    if movement_type == "WEEKLY_CORRECTION":
        return f"تصحيح أسبوعي {weekly_scope_ar} داخل اتجاه كلي {overall_ar}"
    if movement_type == "WEEKLY_CONTINUATION":
        return f"استمرار أسبوعي {weekly_scope_ar} مع الاتجاه الكلي {overall_ar}"
    return "مراقبة فقط / غير واضح"


# NDSP_TDL_COMPARE_NOT_SUBTRACT_RULE: الاتجاه يحسب بالمقارنة المباشرة بين Long و Short، وليس بعملية طرح لاتخاذ القرار.
def evaluate_l4_cot_manager(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    asset = _text(_get(payload, "asset", "symbol", default="ETHUSDT")).upper()
    asset_class = _text(_get(payload, "asset_class", "market", default="crypto")).lower()

    # للأصول الرقمية والعملات والمؤشرات:
    # الفئة المؤسسية طويلة الأمد = مدراء الأصول
    # الفئة القصيرة / المضاربة = الرافعات
    long_term_group = "ASSET_MANAGERS"
    short_term_group = "LEVERAGED_FUNDS"

    am = _ndsp_extract_group_numbers(payload, "asset_managers")
    lf = _ndsp_extract_group_numbers(payload, "leveraged_funds")

    # الاتجاه الكلي من إجمالي العقود الحالية
    am_overall, am_overall_net = _ndsp_direction_from_long_short(am.get("long"), am.get("short")) if am.get("has_current_totals") else (
        str(_get(payload, "asset_managers_bias", "long_term_bias", default="NEUTRAL")).upper(),
        None,
    )

    lf_overall, lf_overall_net = _ndsp_direction_from_long_short(lf.get("long"), lf.get("short")) if lf.get("has_current_totals") else (
        str(_get(payload, "leveraged_funds_bias", "speculative_bias", default="NEUTRAL")).upper(),
        None,
    )

    # الاتجاه الأسبوعي من التغيرات
    am_weekly, am_weekly_delta = _ndsp_weekly_direction_from_changes(am.get("change_long"), am.get("change_short")) if am.get("has_weekly_changes") else ("NEUTRAL", None)
    lf_weekly, lf_weekly_delta = _ndsp_weekly_direction_from_changes(lf.get("change_long"), lf.get("change_short")) if lf.get("has_weekly_changes") else ("NEUTRAL", None)

    # اعتماد السكالبينق الأسبوعي يكون على الاتجاه الجزئي الأسبوعي
    # إذا توفر اتجاه مدراء الأصول الأسبوعي نستخدمه للقراءة المؤسسية الأسبوعية.
    # وإذا لم يتوفر، لا نختلقه من الاتجاه الكلي.
    weekly_operational_bias = am_weekly if am_weekly != "NEUTRAL" else "NEUTRAL"

    movement_description, movement_type = _ndsp_movement_type(am_overall, weekly_operational_bias)

    correction_present = movement_type == "WEEKLY_CORRECTION"
    continuation_present = movement_type == "WEEKLY_CONTINUATION"

    output = {
        "asset": asset,
        "asset_class": asset_class,

        "long_term_group": long_term_group,
        "short_term_group": short_term_group,

        "asset_managers_long": am.get("long"),
        "asset_managers_short": am.get("short"),
        "asset_managers_change_long": am.get("change_long"),
        "asset_managers_change_short": am.get("change_short"),

        "leveraged_funds_long": lf.get("long"),
        "leveraged_funds_short": lf.get("short"),
        "leveraged_funds_change_long": lf.get("change_long"),
        "leveraged_funds_change_short": lf.get("change_short"),

        "asset_managers_overall_direction": am_overall,
        "asset_managers_overall_direction_ar": _ndsp_bias_ar(am_overall),
        "asset_managers_overall_comparison": am_overall_net,

        "asset_managers_weekly_direction": am_weekly,
        "asset_managers_weekly_direction_ar": _ndsp_weekly_bias_ar_with_scope(am_weekly, am_overall, movement_type),
        "asset_managers_weekly_comparison": am_weekly_delta,
        "asset_managers_weekly_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "asset_managers_weekly_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",

        "leveraged_funds_overall_direction": lf_overall,
        "leveraged_funds_overall_direction_ar": _ndsp_bias_ar(lf_overall),
        "leveraged_funds_overall_comparison": lf_overall_net,

        "leveraged_funds_weekly_direction": lf_weekly,
        "leveraged_funds_weekly_direction_ar": _ndsp_bias_ar(lf_weekly),
        "leveraged_funds_weekly_comparison": lf_weekly_delta,

        "decision_basis": "WEEKLY_PARTIAL_DIRECTION_FOR_SCALPING",
        "trend_context_basis": "OVERALL_CURRENT_TOTALS_LONG_VS_SHORT",

        "weekly_operational_bias": weekly_operational_bias,
        "weekly_operational_bias_ar": _ndsp_weekly_bias_ar_with_scope(weekly_operational_bias, am_overall, movement_type),
        "weekly_operational_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "weekly_operational_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",

        "movement_type": movement_type,
        "movement_type_ar": _ndsp_movement_ar(movement_type),
        "movement_description": movement_description,

        "correction_present": correction_present,
        "continuation_present": continuation_present,

        "has_current_totals": bool(am.get("has_current_totals")),
        "has_weekly_changes": bool(am.get("has_weekly_changes")),

        "raw_cot_report_date": _get(payload, "raw_cot_report_date", "cot_report_date", default=None),
        "report_age_days": _get(payload, "report_age_days", default=None),
    }

    score = 88 if output["has_current_totals"] and output["has_weekly_changes"] else 62
    warnings = []
    if not output["has_current_totals"]:
        warnings.append("الاتجاه الكلي لم يحسب من Long/Short الحالي بسبب نقص البيانات الرقمية.")
    if not output["has_weekly_changes"]:
        warnings.append("الاتجاه الأسبوعي لم يحسب من تغير Long/Short بسبب نقص بيانات التغير الأسبوعي.")

    return _layer_result(
        4,
        "COT Positioning Manager",
        "L4_COT_MANAGER",
        "مدير تموضع الفئات",
        "cot_positioning_state",
        output,
        score,
        [
            "الاتجاه الكلي يحسب من إجمالي Long الحالي مقابل Short الحالي.",
            "الاتجاه الأسبوعي يحسب من تغير Long وتغير Short.",
            "اعتماد السكالبينق الأسبوعي يكون على الاتجاه الجزئي الأسبوعي.",
        ],
        warnings,
    )


# ============================================================
# Layer 5 — TDL V2 Direction Logic
# File: backend/layers/direction/l5_tdl_v2.py
# ============================================================

def evaluate_l5_tdl_v2(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    overall_direction = str(_get(payload, "asset_managers_overall_direction", "long_term_bias", default="NEUTRAL")).upper()
    weekly_direction = str(_get(payload, "asset_managers_weekly_direction", "weekly_operational_bias", default="NEUTRAL")).upper()

    movement_type = str(_get(payload, "movement_type", default="WATCH_ONLY")).upper()
    correction_present = bool(_get(payload, "correction_present", default=(movement_type == "WEEKLY_CORRECTION")))
    continuation_present = bool(_get(payload, "continuation_present", default=(movement_type == "WEEKLY_CONTINUATION")))

    timing_allowed = bool(_get(payload, "timing_allowed", "allowed", default=True))

    # قاعدة TDL الجديدة:
    # الترند يقاس بالاتجاه الكلي.
    # قرار السكالبينق الأسبوعي يعتمد على الاتجاه الجزئي الأسبوعي.
    # الاتجاه الكلي يحدد هل الحركة استمرار أم تصحيح.
    if weekly_direction in {"BULLISH", "BEARISH"} and timing_allowed:
        tdl_state = "ALLOWED_WEEKLY_SCALPING_BIAS"
        tdl_bias = weekly_direction
    elif weekly_direction in {"BULLISH", "BEARISH"} and not timing_allowed:
        tdl_state = "WEEKLY_BIAS_TIMING_REVIEW"
        tdl_bias = weekly_direction
    else:
        tdl_state = "WATCH_ONLY"
        tdl_bias = "NEUTRAL"

    tdl_reading = _ndsp_tdl_reading_ar(overall_direction, weekly_direction, movement_type)

    output = {
        "tdl_state": tdl_state,
        "tdl_bias": tdl_bias,
        "tdl_bias_ar": _ndsp_weekly_bias_ar_with_scope(tdl_bias, overall_direction, movement_type),
        "tdl_bias_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "tdl_bias_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",

        "overall_trend_direction": overall_direction,
        "overall_trend_direction_ar": _ndsp_bias_ar(overall_direction),

        "weekly_partial_direction": weekly_direction,
        "weekly_partial_direction_ar": _ndsp_weekly_bias_ar_with_scope(weekly_direction, overall_direction, movement_type),
        "weekly_partial_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "weekly_partial_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",

        "decision_basis": "WEEKLY_PARTIAL_DIRECTION_FOR_SCALPING",
        "trend_context_basis": "OVERALL_CURRENT_TOTALS_LONG_VS_SHORT",

        "movement_type": movement_type,
        "movement_type_ar": _ndsp_movement_ar(movement_type),
        "tdl_reading": tdl_reading,

        "correction_present": correction_present,
        "continuation_present": continuation_present,
        "timing_allowed": timing_allowed,

        "important_governance_note": "الاتجاه الكلي سياق للترند، أما اعتماد قرار السكالبينق الأسبوعي فهو الاتجاه الجزئي الأسبوعي.",
    }

    score = 88 if tdl_state == "ALLOWED_WEEKLY_SCALPING_BIAS" else 64

    return _layer_result(
        5,
        "TDL V2 Direction Logic",
        "L5_TDL_V2",
        "منطق الاتجاه الزمني V2",
        "tdl_direction_state",
        output,
        score,
        [
            f"اعتماد القرار الأسبوعي: {_ndsp_weekly_bias_ar_with_scope(tdl_bias, overall_direction, movement_type)}.",
            f"السياق الكلي: {_ndsp_bias_ar(overall_direction)}.",
            tdl_reading,
        ],
        [],
    )


# ============================================================
# Layer 6 — Dominant Timed Direction / Direction Authority
# File: backend/layers/direction/l6_direction_authority.py
# ============================================================

def evaluate_l6_direction_authority(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    weekly_direction = str(_get(payload, "tdl_bias", "weekly_partial_direction", "weekly_operational_bias", default="NEUTRAL")).upper()
    overall_direction = str(_get(payload, "overall_trend_direction", "asset_managers_overall_direction", default="NEUTRAL")).upper()
    movement_type = str(_get(payload, "movement_type", default="WATCH_ONLY")).upper()

    timing_allowed = bool(_get(payload, "timing_allowed", default=True))
    correction_present = bool(_get(payload, "correction_present", default=(movement_type == "WEEKLY_CORRECTION")))
    continuation_present = bool(_get(payload, "continuation_present", default=(movement_type == "WEEKLY_CONTINUATION")))

    if weekly_direction in {"BULLISH", "BEARISH"}:
        dominant_direction = weekly_direction
        authority = "WEEKLY_SCALPING_AUTHORITY"
    else:
        dominant_direction = "NEUTRAL"
        authority = "WATCH_ONLY"

    support = []
    support.append(f"الاتجاه الكلي: {_ndsp_bias_ar(overall_direction)}.")
    support.append(f"الاتجاه الأسبوعي المعتمد للسكالبينق: {_ndsp_bias_ar(weekly_direction)}.")

    if correction_present:
        support.append("الحركة الحالية تصحيح أسبوعي داخل الاتجاه الكلي.")
    if continuation_present:
        support.append("الحركة الحالية استمرار أسبوعي مع الاتجاه الكلي.")
    if timing_allowed:
        support.append("التوقيت يسمح بالقراءة الأسبوعية.")

    output = {
        "dominant_direction": dominant_direction,
        "dominant_direction_ar": _ndsp_weekly_bias_ar_with_scope(dominant_direction, overall_direction, movement_type),
        "dominant_direction_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "dominant_direction_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",
        "direction_authority": authority,

        "overall_trend_direction": overall_direction,
        "overall_trend_direction_ar": _ndsp_bias_ar(overall_direction),

        "weekly_partial_direction": weekly_direction,
        "weekly_partial_direction_ar": _ndsp_weekly_bias_ar_with_scope(weekly_direction, overall_direction, movement_type),
        "weekly_partial_scope": "NARROW_CORRECTIVE_HORIZON" if movement_type == "WEEKLY_CORRECTION" else "DIRECTIONAL_CONTINUATION_OR_NEUTRAL",
        "weekly_partial_scope_ar": "غير صريح / ذو أفق ضيق" if movement_type == "WEEKLY_CORRECTION" else "اتجاه مباشر أو محايد",

        "movement_type": movement_type,
        "movement_type_ar": _ndsp_movement_ar(movement_type),

        "decision_basis": "WEEKLY_PARTIAL_DIRECTION_FOR_SCALPING",
        "trend_context_basis": "OVERALL_CURRENT_TOTALS_LONG_VS_SHORT",

        "correction_present": correction_present,
        "continuation_present": continuation_present,
        "timing_allowed": timing_allowed,

        "risk_pressure_score": 28 if dominant_direction != "NEUTRAL" else 55,
        "blocking_factors": [] if dominant_direction != "NEUTRAL" else ["الاتجاه الأسبوعي غير واضح."],
        "supporting_factors": support,
    }

    score = 92 if dominant_direction != "NEUTRAL" else 58

    return _layer_result(
        6,
        "Dominant Timed Direction",
        "L6_DIRECTION_AUTHORITY",
        "سلطة الاتجاه الزمني",
        "dominant_timed_direction",
        output,
        score,
        support,
        [],
    )


# ============================================================
# Layer 7 — Macro / USD Pressure
# File: backend/layers/quality/l7_macro.py
# ============================================================

def evaluate_l7_macro(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    asset = _text(_get(payload, "asset", "symbol", default="GOLD")).upper()
    usd_state = _text(_get(payload, "usd_state", "dollar_state", default="neutral")).lower()

    # NDSP Governance Rule:
    # All platform-tracked assets are treated as inverse to USD.
    # Strong USD = negative macro pressure.
    # Weak USD = positive macro support.
    inverse_asset = True

    high_impact_events = _int(_get(payload, "high_impact_events", "events_high", default=0), 0)

    if usd_state in {"strong", "bullish", "قوي"}:
        macro_state = "NEGATIVE_PRESSURE"
        score = 55
        warnings = ["Strong USD pressures all NDSP-tracked assets."]
    elif usd_state in {"weak", "bearish", "ضعيف"}:
        macro_state = "POSITIVE_SUPPORT"
        score = 82
        warnings = []
    else:
        macro_state = "NEUTRAL"
        score = 68
        warnings = ["USD state is neutral or unavailable."]

    if high_impact_events >= 3:
        score -= 8
        warnings.append("High-impact macro event density is elevated.")

    output = {
        "asset": asset,
        "usd_state": usd_state,
        "inverse_to_usd": inverse_asset,
        "macro_relationship_rule": "ALL_NDSP_ASSETS_INVERSE_TO_USD",
        "macro_state": macro_state,
        "high_impact_events": high_impact_events,
    }

    return _layer_result(
        7,
        "Macro And Dollar Pressure",
        "L7_MACRO",
        "ضغط الدولار والمشهد الكلي",
        "macro_pressure_state",
        output,
        score,
        [f"Macro state={macro_state}.", "All NDSP tracked assets are treated as inverse to USD."],
        warnings,
    )


# ============================================================
# Layer 8 — NMP Reference Zone
# File: backend/layers/quality/l8_nmp.py
# ============================================================

def _nmp_safe_float(v, default=0.0):
    try:
        return float(str(v).replace(",", "").strip())
    except Exception:
        return default


def _nmp_rsi_values(closes, period=14):
    out = [None] * len(closes)
    if len(closes) <= period:
        return out
    gains, losses = [], []
    for i in range(1, period + 1):
        ch = closes[i] - closes[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(abs(min(ch, 0.0)))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    out[period] = 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))
    for i in range(period + 1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gain = max(ch, 0.0)
        loss = abs(min(ch, 0.0))
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        out[i] = 100.0 if avg_loss == 0 else 100 - (100 / (1 + avg_gain / avg_loss))
    return out


def _nmp_ema_values(values, period):
    if not values:
        return []
    k = 2 / (period + 1)
    ema = values[0]
    out = []
    for i, v in enumerate(values):
        ema = v if i == 0 else (v * k) + (ema * (1 - k))
        out.append(ema)
    return out


def _nmp_macd_hist_values(closes):
    ema12 = _nmp_ema_values(closes, 12)
    ema26 = _nmp_ema_values(closes, 26)
    macd = [(a or 0.0) - (b or 0.0) for a, b in zip(ema12, ema26)]
    signal = _nmp_ema_values(macd, 9)
    return [m - (sig or 0.0) for m, sig in zip(macd, signal)]


def _nmp_cci_values(highs, lows, closes, period=20):
    tp = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
    out = []
    for i in range(len(tp)):
        if i + 1 < period:
            out.append(None)
            continue
        window = tp[i + 1 - period:i + 1]
        ma = sum(window) / period
        md = sum(abs(x - ma) for x in window) / period
        out.append(0.0 if md == 0 else (tp[i] - ma) / (0.015 * md))
    return out


def _nmp_obv_slope_values(closes, volumes, period=5):
    obv = [0.0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i - 1]:
            obv.append(obv[-1] + volumes[i])
        elif closes[i] < closes[i - 1]:
            obv.append(obv[-1] - volumes[i])
        else:
            obv.append(obv[-1])
    out = []
    for i in range(len(obv)):
        out.append(None if i < period else obv[i] - obv[i - period])
    return out


def _nmp_fetch_klines_safe(symbol, interval, limit=220):
    import json
    import urllib.parse
    import urllib.request

    qs = urllib.parse.urlencode({"symbol": symbol.upper(), "interval": interval, "limit": int(limit)})
    url = "https://api.binance.com/api/v3/klines?" + qs
    req = urllib.request.Request(url, headers={"User-Agent": "NDSP-NMP-Layer/1.0"})
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def _nmp_next_open_after_extreme(rows, values, direction, indicator, timeframe):
    candidates = []
    for i, v in enumerate(values[:-1]):
        if v is None:
            continue
        try:
            candidates.append((float(v), i))
        except Exception:
            pass
    if not candidates:
        return None

    if str(direction).lower() in {"bearish", "down", "هابط", "sell"}:
        score, idx = min(candidates, key=lambda x: x[0])
        nmp_direction = "BEARISH"
    else:
        score, idx = max(candidates, key=lambda x: x[0])
        nmp_direction = "BULLISH"

    m = rows[idx]
    nxt = rows[idx + 1]

    return {
        "timeframe": timeframe,
        "indicator": indicator,
        "nmp_direction": nmp_direction,
        "momentum_candle_open_time": int(m[0]),
        "momentum_candle_open": _nmp_safe_float(m[1]),
        "momentum_candle_high": _nmp_safe_float(m[2]),
        "momentum_candle_low": _nmp_safe_float(m[3]),
        "momentum_candle_close": _nmp_safe_float(m[4]),
        "momentum_value": round(float(score), 6),
        "next_candle_open_time": int(nxt[0]),
        "nmp_level": _nmp_safe_float(m[1]),
        "method": "MOMENTUM_CANDLE_OPEN",
    }


# NDSP_NMP_RULE_MOMENTUM_CANDLE_OPEN: NMP = opening price of the momentum candle itself, not the next candle.
def evaluate_l8_nmp(payload=None):
    payload = dict(payload or {})

    symbol = _text(_get(payload, "asset", "symbol", default="ETHUSDT")).upper()
    if symbol in {"ETH", "ETHER"}:
        symbol = "ETHUSDT"
    elif symbol in {"BTC", "BITCOIN"}:
        symbol = "BTCUSDT"

    direction = _text(_get(payload, "tdl_bias", "direction_bias", "selected_timeframe_direction", "direction", default="bullish")).lower()
    current_price = _float(_get(payload, "live_price", "price", default=0), 0.0)

    intervals = [("1h", "1H"), ("4h", "4H"), ("1d", "1D"), ("1w", "1W")]
    results = []
    errors = []

    for interval, label in intervals:
        try:
            rows = _nmp_fetch_klines_safe(symbol, interval, 220)
            if not isinstance(rows, list) or len(rows) < 40:
                errors.append(f"{label}: insufficient candles")
                continue

            highs = [_nmp_safe_float(r[2]) for r in rows]
            lows = [_nmp_safe_float(r[3]) for r in rows]
            closes = [_nmp_safe_float(r[4]) for r in rows]
            volumes = [_nmp_safe_float(r[5]) for r in rows]

            indicators = {
                "RSI": _nmp_rsi_values(closes, 14),
                "MACD_HISTOGRAM": _nmp_macd_hist_values(closes),
                "CCI": _nmp_cci_values(highs, lows, closes, 20),
                "OBV_SLOPE": _nmp_obv_slope_values(closes, volumes, 5),
            }

            for ind, vals in indicators.items():
                picked = _nmp_next_open_after_extreme(rows, vals, direction, ind, label)
                if picked:
                    results.append(picked)

        except Exception as e:
            errors.append(f"{label}: {type(e).__name__}: {e}")

    selected_tf = _text(_get(payload, "selected_timeframe", "timeframe", default="")).lower()
    tf_map = {
        "hourly": "1H", "h1": "1H", "1h": "1H",
        "4h": "4H", "h4": "4H",
        "daily": "1D", "1d": "1D",
        "weekly": "1W", "1w": "1W",
    }
    preferred = tf_map.get(selected_tf, "4H")

    primary = None
    for tf in [preferred, "4H", "1D", "1H", "1W"]:
        group = [x for x in results if x.get("timeframe") == tf]
        for ind in ["RSI", "MACD_HISTOGRAM", "CCI", "OBV_SLOPE"]:
            primary = next((x for x in group if x.get("indicator") == ind), None)
            if primary:
                break
        if primary:
            break

    primary_level = primary.get("nmp_level") if primary else None
    real_calculated = bool(primary)

    output = {
        "symbol": symbol,
        "current_price": current_price,
        "nmp_real_calculated": real_calculated,
        "nmp_method": "MOMENTUM_CANDLE_OPEN",
        "nmp_direction_basis": direction.upper(),
        "primary_nmp": primary,
        "primary_nmp_level": primary_level,
        "distance_from_primary_nmp": (current_price - float(primary_level)) if primary_level is not None and current_price else None,
        "all_timeframe_indicator_nmp_levels": results,
        "timeframes_checked": ["1H", "4H", "1D", "1W"],
        "indicators_checked": ["RSI", "MACD_HISTOGRAM", "CCI", "OBV_SLOPE"],
        "calculation_errors": errors,
        "zone_state": "REAL_NMP_CALCULATED" if real_calculated else "NMP_NOT_AVAILABLE",
    }

    return _layer_result(
        8,
        "Nawaf Meet Point",
        "L8_NMP",
        "نقطة التقاء نواف",
        "nmp_reference_zone",
        output,
        84 if real_calculated else 34,
        ["NMP is calculated from real candle momentum.", "NMP level is the opening price of the selected momentum candle itself."] if real_calculated else [],
        ([] if real_calculated else ["Real NMP could not be calculated from candle data."]) + (["Some NMP timeframe calculations failed."] if errors else []),
    )


# ============================================================
# Layer 9 — Horizon Structure
# File: backend/layers/quality/l9_horizon_structure.py
# ============================================================

def evaluate_l9_horizon_structure(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    short = _int(_get(payload, "short_horizon_strength", "short_strength", default=72), 72)
    medium = _int(_get(payload, "medium_horizon_strength", "medium_strength", default=66), 66)
    long = _int(_get(payload, "long_horizon_strength", "long_strength", default=58), 58)

    strengths = {"SHORT": short, "MEDIUM": medium, "LONG": long}
    dominant = max(strengths, key=strengths.get)
    score = strengths[dominant]

    output = {
        "short_horizon": short,
        "medium_horizon": medium,
        "long_horizon": long,
        "dominant_horizon": dominant,
        "horizon_strengths": strengths,
    }

    return _layer_result(
        9,
        "Horizon Structure",
        "L9_HORIZON_STRUCTURE",
        "هيكل الأفق الزمني",
        "horizon_structure_state",
        output,
        score,
        [f"Dominant horizon={dominant}."],
        [],
    )


# ============================================================
# Layer 10 — Momentum
# File: backend/layers/quality/l10_momentum.py
# ============================================================

def evaluate_l10_momentum(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    rsi = _num(_get(payload, "rsi", default=50), 50)
    macd_hist = _num(_get(payload, "macd_hist", "macd_histogram", default=0), 0)
    cci = _num(_get(payload, "cci", default=0), 0)
    obv_slope = _num(_get(payload, "obv_slope", default=0), 0)

    bull_points = 0
    bear_points = 0

    if rsi >= 55:
        bull_points += 1
    elif rsi <= 45:
        bear_points += 1

    if macd_hist > 0:
        bull_points += 1
    elif macd_hist < 0:
        bear_points += 1

    if cci > 50:
        bull_points += 1
    elif cci < -50:
        bear_points += 1

    if obv_slope > 0:
        bull_points += 1
    elif obv_slope < 0:
        bear_points += 1

    if bull_points > bear_points:
        momentum = "BULLISH"
        score = 60 + bull_points * 8
    elif bear_points > bull_points:
        momentum = "BEARISH"
        score = 60 + bear_points * 8
    else:
        momentum = "NEUTRAL"
        score = 50

    output = {
        "rsi": rsi,
        "macd_histogram": macd_hist,
        "cci": cci,
        "obv_slope": obv_slope,
        "bull_points": bull_points,
        "bear_points": bear_points,
        "momentum_state": momentum,
    }

    return _layer_result(
        10,
        "Momentum Engine",
        "L10_MOMENTUM",
        "محرك الزخم",
        "momentum_state",
        output,
        score,
        [f"Momentum resolved as {momentum}."],
        [],
    )


# ============================================================
# Layer 11 — Divergence
# File: backend/layers/quality/l11_divergence.py
# ============================================================

def evaluate_l11_divergence(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    price_trend = _direction(_get(payload, "price_trend", default="neutral"))
    rsi_trend = _direction(_get(payload, "rsi_trend", default="neutral"))
    obv_trend = _direction(_get(payload, "obv_trend", default="neutral"))
    divergence_type = _text(_get(payload, "divergence_type", default="auto")).lower()

    if divergence_type != "auto":
        state = divergence_type.upper()
        score = 75
    elif price_trend == "BULLISH" and rsi_trend == "BEARISH":
        state = "REGULAR_BEARISH_DIVERGENCE"
        score = 72
    elif price_trend == "BEARISH" and rsi_trend == "BULLISH":
        state = "REGULAR_BULLISH_DIVERGENCE"
        score = 72
    elif price_trend == rsi_trend and price_trend == obv_trend and price_trend != "NEUTRAL":
        state = "NO_DIVERGENCE_CONFIRMATION"
        score = 68
    else:
        state = "INCONCLUSIVE"
        score = 50

    output = {
        "price_trend": price_trend,
        "rsi_trend": rsi_trend,
        "obv_trend": obv_trend,
        "divergence_state": state,
    }

    return _layer_result(
        11,
        "Divergence Engine",
        "L11_DIVERGENCE",
        "محرك الانحراف",
        "divergence_state",
        output,
        score,
        [f"Divergence state={state}."],
        [],
    )


# ============================================================
# Layer 12 — Black Layer / Hidden Blockers
# File: backend/layers/execution/l12_black_layer.py
# ============================================================

def evaluate_l12_black_layer(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    manual_block = _bool(_get(payload, "manual_block", "owner_block", default=False), False)
    news_shock = _bool(_get(payload, "news_shock", "shock_event", default=False), False)
    data_broken = not _bool(_get(payload, "sources_connected", default=True), True)
    risk = _int(_get(payload, "risk_pressure_score", "risk", default=45), 45)

    blockers = []
    if manual_block:
        blockers.append("OWNER_MANUAL_BLOCK")
    if news_shock:
        blockers.append("NEWS_OR_SHOCK_EVENT")
    if data_broken:
        blockers.append("DATA_SOURCE_BROKEN")
    if risk >= 85:
        blockers.append("EXTREME_RISK_PRESSURE")

    blocked = bool(blockers)
    score = 25 if blocked else 88

    output = {
        "blocked": blocked,
        "black_layer_state": "BLOCKED" if blocked else "CLEAR",
        "blockers": blockers,
    }

    return _layer_result(
        12,
        "Black Layer",
        "L12_BLACK_LAYER",
        "طبقة المنع السوداء",
        "black_layer_block_state",
        output,
        score,
        ["Black layer is clear."] if not blocked else [],
        blockers,
    )


# ============================================================
# Layer 13 — Quality Stack
# File: backend/layers/quality/l13_quality_stack.py
# ============================================================

def evaluate_l13_quality_stack(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    data_clarity = _int(_get(payload, "data_clarity", default=84), 84)
    model_quality = _int(_get(payload, "model_quality", default=82), 82)
    source_reliability = _int(_get(payload, "source_reliability", default=86), 86)
    scenario_consistency = _int(_get(payload, "scenario_consistency", default=78), 78)

    final = _clamp((data_clarity + model_quality + source_reliability + scenario_consistency) / 4)

    output = {
        "data_clarity": data_clarity,
        "model_quality": model_quality,
        "source_reliability": source_reliability,
        "scenario_consistency": scenario_consistency,
        "decision_quality_score": final,
    }

    warnings = [] if final >= 70 else ["Decision quality stack is weak."]

    return _layer_result(
        13,
        "Quality Stack",
        "L13_QUALITY_STACK",
        "مكدس جودة القرار",
        "decision_quality_score",
        output,
        final,
        [f"Decision quality score={final}."],
        warnings,
    )


# ============================================================
# Layer 14 — Risk Governance
# File: backend/layers/execution/l14_risk_governance.py
# ============================================================

def evaluate_l14_risk_governance(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    risk = _int(_get(payload, "risk_pressure_score", "risk", default=45), 45)
    weekly_losses = _int(_get(payload, "weekly_losses", "losses_this_week", default=0), 0)
    black_blocked = _bool(_get(payload, "black_layer_blocked", "blocked", default=False), False)

    suspended = weekly_losses >= 3
    hard_block = black_blocked or suspended or risk >= 85

    if hard_block:
        score = 20
        state = "BLOCKED"
    elif risk >= 70:
        score = 52
        state = "CAUTION"
    else:
        score = 84
        state = "ALLOWED"

    warnings = []
    if suspended:
        warnings.append("Three weekly losses reached; suspend one full week.")
    if black_blocked:
        warnings.append("Black layer blocks execution.")
    if risk >= 85:
        warnings.append("Extreme risk pressure.")

    output = {
        "risk_pressure_score": risk,
        "weekly_losses": weekly_losses,
        "suspended": suspended,
        "risk_governance_state": state,
        "execution_allowed": state == "ALLOWED",
    }

    return _layer_result(
        14,
        "Risk Governance",
        "L14_RISK_GOVERNANCE",
        "حوكمة المخاطر",
        "risk_governance_state",
        output,
        score,
        [f"Risk governance state={state}."],
        warnings,
    )


# ============================================================
# Layer 15 — Final Decision
# File: backend/layers/execution/l15_final_decision.py
# ============================================================

def evaluate_l15_final_decision(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    tdl_state = _text(_get(payload, "tdl_state", default="BLOCKED")).upper()
    nmp_confirmed = _bool(_get(payload, "nmp_confirmed", default=False), False)
    risk_allowed = _bool(_get(payload, "risk_allowed", "execution_allowed", default=True), True)
    black_blocked = _bool(_get(payload, "black_blocked", "blocked", default=False), False)
    manual_override = _bool(_get(payload, "manual_override", default=False), False)
    automated = _bool(_get(payload, "automated", default=True), True)

    if black_blocked or not risk_allowed:
        state = "BLOCKED"
        score = 25
        reason = "Risk or black layer blocks final decision."
    elif manual_override and tdl_state in {"ALLOWED", "ARMED", "WAITING_FOR_CORRECTION"}:
        state = "MANUAL_ALLOWED"
        score = 72
        reason = "Owner manual override allows review; NMP optional in manual mode."
    elif automated and tdl_state == "ALLOWED" and nmp_confirmed:
        state = "ARMED"
        score = 88
        reason = "TDL allowed and NMP confirmed."
    elif automated and tdl_state == "ARMED":
        state = "ARMED"
        score = 90
        reason = "TDL already armed."
    elif tdl_state in {"ALLOWED", "WAITING_FOR_CORRECTION"}:
        state = "ALLOWED_PENDING_NMP"
        score = 66
        reason = "TDL allowed but NMP is not confirmed for automation."
    else:
        state = "BLOCKED"
        score = 38
        reason = "Final decision conditions are incomplete."

    output = {
        "final_decision_state": state,
        "reason": reason,
        "tdl_state": tdl_state,
        "nmp_confirmed": nmp_confirmed,
        "risk_allowed": risk_allowed,
        "black_blocked": black_blocked,
        "manual_override": manual_override,
        "automated": automated,
    }

    warnings = [] if state in {"ARMED", "MANUAL_ALLOWED"} else [reason]

    return _layer_result(
        15,
        "Final Decision Engine",
        "L15_FINAL_DECISION",
        "محرك القرار النهائي",
        "final_decision_state",
        output,
        score,
        [reason],
        warnings,
    )


# ============================================================
# Layer 16 — Scenario Alerts
# File: backend/layers/execution/l16_scenario_alerts.py
# ============================================================

def evaluate_l16_scenario_alerts(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})

    base = _int(_get(payload, "base_scenario_probability", "base", default=62), 62)
    optimistic = _int(_get(payload, "optimistic_scenario_probability", "optimistic", default=24), 24)
    conservative = _int(_get(payload, "conservative_scenario_probability", "conservative", default=max(0, 100 - base - optimistic)), max(0, 100 - base - optimistic))
    alerts_enabled = _bool(_get(payload, "alerts_enabled", default=True), True)
    final_state = _text(_get(payload, "final_decision_state", default="UNDER_MONITORING")).upper()

    scenarios = {
        "BASE": base,
        "OPTIMISTIC": optimistic,
        "CONSERVATIVE": conservative,
    }

    dominant = max(scenarios, key=scenarios.get)

    alert_level = "NONE"
    if alerts_enabled:
        if final_state in {"ARMED", "EXECUTED"}:
            alert_level = "HIGH"
        elif final_state in {"ALLOWED_PENDING_NMP", "MANUAL_ALLOWED"}:
            alert_level = "MEDIUM"
        elif dominant == "CONSERVATIVE":
            alert_level = "WATCH"
        else:
            alert_level = "LOW"

    score = max(scenarios.values()) if alerts_enabled else 45

    output = {
        "scenario_distribution": scenarios,
        "dominant_scenario": dominant,
        "alerts_enabled": alerts_enabled,
        "alert_level": alert_level,
        "final_decision_state": final_state,
    }

    warnings = [] if alerts_enabled else ["Alerts are disabled."]

    return _layer_result(
        16,
        "Scenario Alerts",
        "L16_SCENARIO_ALERTS",
        "تنبيهات السيناريو",
        "scenario_alert_state",
        output,
        score,
        [f"Dominant scenario={dominant}, alert_level={alert_level}."],
        warnings,
    )


# ============================================================
# Orchestrated evaluation
# ============================================================

LAYER_FUNCTIONS = [
    evaluate_l1_source,
    evaluate_l2_session,
    evaluate_l3_timing,
    evaluate_l4_cot_manager,
    evaluate_l5_tdl_v2,
    evaluate_l6_direction_authority,
    evaluate_l7_macro,
    evaluate_l8_nmp,
    evaluate_l9_horizon_structure,
    evaluate_l10_momentum,
    evaluate_l11_divergence,
    evaluate_l12_black_layer,
    evaluate_l13_quality_stack,
    evaluate_l14_risk_governance,
    evaluate_l15_final_decision,
    evaluate_l16_scenario_alerts,
]


def evaluate_all_16_layers(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    results = []
    errors = []

    # Run sequentially and feed important outputs forward.
    context = dict(payload)

    for fn in LAYER_FUNCTIONS:
        try:
            result = fn(context)
            results.append(result)

            out = result.get("output", {})
            if isinstance(out, Mapping):
                context.update(out)

            # Compatibility keys for later layers.
            if result["layer_id"] == 3:
                context["timing"] = out
                context["timing_allowed"] = out.get("allowed")
            elif result["layer_id"] == 5:
                context["tdl"] = out
                context["tdl_state"] = out.get("tdl_state")
                context["tdl_bias"] = out.get("tdl_bias")
            elif result["layer_id"] == 8:
                context["nmp_confirmed"] = out.get("zone_state") == "INSIDE_REFERENCE_ZONE"
            elif result["layer_id"] == 12:
                context["black_blocked"] = out.get("blocked")
            elif result["layer_id"] == 14:
                context["risk_allowed"] = out.get("execution_allowed")
            elif result["layer_id"] == 15:
                context["final_decision_state"] = out.get("final_decision_state")

        except Exception as exc:
            errors.append({"function": fn.__name__, "error": repr(exc)})

    avg_conf = 0
    if results:
        avg_conf = int(sum(int(x.get("confidence", 0)) for x in results) / len(results))

    return {
        "ok": not errors,
        "generated_at": _now(),
        "total_layers_executed": len(results),
        "total_errors": len(errors),
        "average_confidence": avg_conf,
        "layers": results,
        "errors": errors,
        "context_after_layers": context,
    }


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return evaluate_all_16_layers(payload)


def run(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return evaluate_all_16_layers(payload)


if __name__ == "__main__":
    import json
    import sys

    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {
        "asset": "GOLD",
        "asset_class": "commodity",
        "live_price": 3362.5,
        "direction_bias": "bullish",
        "weekday": "monday",
        "decision_quality_score": 87,
        "risk_pressure_score": 28,
        "macro_pressure": "supportive",
        "usd_state": "weak",
        "correction_present": True,
        "plan": "Elite",
        "trial_days_remaining": 11,
    }

    print(json.dumps(evaluate_all_16_layers(payload), ensure_ascii=False, indent=2))

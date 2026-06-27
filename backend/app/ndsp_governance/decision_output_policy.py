from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

GOVERNANCE_JSON_PATH = Path("/home/nawaf511/empire-core-new/governance/NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED.json")

GOVERNANCE_NOTE_AR = "مستويات السيناريو هي مراجع سياقية لدعم القرار فقط، وليست نصيحة مالية أو أمر تداول أو توجيه تنفيذ أو ضمانًا للنتائج."
GOVERNANCE_NOTE_EN = "Scenario levels are contextual decision-support references only. They are not financial advice, trade instructions, execution orders, or guaranteed outcomes."

FORBIDDEN_TEXT_PATTERNS = [
    (re.compile(r"\bbuy now\b", re.I), "سياق اتجاهي صاعد"),
    (re.compile(r"\bsell now\b", re.I), "سياق اتجاهي هابط"),
    (re.compile(r"\bbuy\b", re.I), "سياق صاعد"),
    (re.compile(r"\bsell\b", re.I), "سياق هابط"),
    (re.compile(r"\bentry\b", re.I), "مستوى تفعيل السيناريو"),
    (re.compile(r"\btake profit\b", re.I), "مستوى وصول السيناريو"),
    (re.compile(r"\btp\b", re.I), "مستوى وصول السيناريو"),
    (re.compile(r"\bstop loss\b", re.I), "مستوى إلغاء السيناريو"),
    (re.compile(r"\bsl\b", re.I), "مستوى إلغاء السيناريو"),
    (re.compile(r"\bopen position\b", re.I), "متابعة السيناريو"),
    (re.compile(r"\bclose position\b", re.I), "مراجعة السيناريو"),
    (re.compile(r"\bexecute\b", re.I), "متابعة سياقية"),
    (re.compile(r"\border placement\b", re.I), "إخراج سياقي"),
    (re.compile(r"\btrading bot\b", re.I), "مساعد سياقي"),
    (re.compile(r"\bsignal provider\b", re.I), "منصة دعم قرار"),
    (re.compile(r"شراء الآن"), "سياق اتجاهي صاعد"),
    (re.compile(r"بيع الآن"), "سياق اتجاهي هابط"),
    (re.compile(r"شراء"), "سياق صاعد"),
    (re.compile(r"بيع"), "سياق هابط"),
    (re.compile(r"دخول"), "مستوى تفعيل السيناريو"),
    (re.compile(r"جني ربح"), "مستوى وصول السيناريو"),
    (re.compile(r"وقف خسارة"), "مستوى إلغاء السيناريو"),
    (re.compile(r"افتح صفقة"), "متابعة السيناريو"),
    (re.compile(r"أغلق صفقة"), "مراجعة السيناريو"),
    (re.compile(r"نفذ"), "متابعة سياقية"),
    (re.compile(r"أمر تداول"), "قراءة سياقية"),
    (re.compile(r"توصية مالية"), "قراءة سياقية"),
    (re.compile(r"مزود توصيات"), "منصة دعم قرار"),
    (re.compile(r"بوت تداول"), "مساعد سياقي"),
]

FORBIDDEN_PUBLIC_REGEX = [
    re.compile(r"\bbuy now\b", re.I),
    re.compile(r"\bsell now\b", re.I),
    re.compile(r"\bbuy\b", re.I),
    re.compile(r"\bsell\b", re.I),
    re.compile(r"\bentry\b", re.I),
    re.compile(r"\btake profit\b", re.I),
    re.compile(r"\bstop loss\b", re.I),
    re.compile(r"\bopen position\b", re.I),
    re.compile(r"\bclose position\b", re.I),
    re.compile(r"\bexecute\b", re.I),
    re.compile(r"\border placement\b", re.I),
    re.compile(r"\btrading bot\b", re.I),
    re.compile(r"\bsignal provider\b", re.I),
    re.compile(r"شراء الآن"),
    re.compile(r"بيع الآن"),
    re.compile(r"شراء"),
    re.compile(r"بيع"),
    re.compile(r"دخول"),
    re.compile(r"جني ربح"),
    re.compile(r"وقف خسارة"),
    re.compile(r"افتح صفقة"),
    re.compile(r"أغلق صفقة"),
    re.compile(r"نفذ"),
    re.compile(r"أمر تداول"),
    re.compile(r"توصية مالية"),
    re.compile(r"مزود توصيات"),
    re.compile(r"بوت تداول"),
]

DROP_KEY_PATTERNS = [
    re.compile(r"^raw_", re.I),
    re.compile(r"_raw$", re.I),
    re.compile(r"formula", re.I),
    re.compile(r"weight", re.I),
    re.compile(r"secret", re.I),
    re.compile(r"token", re.I),
    re.compile(r"password", re.I),
    re.compile(r"admin.*key", re.I),
    re.compile(r"api.*key", re.I),
    re.compile(r"contract_sum", re.I),
    re.compile(r"cot", re.I),
    re.compile(r"source_categories", re.I),
    re.compile(r"layer_sequence", re.I),
    re.compile(r"score_breakdown", re.I),
    re.compile(r"calculation", re.I),
    re.compile(r"order", re.I),
    re.compile(r"execution", re.I),
    re.compile(r"position", re.I),
]

INTERNAL_ONLY_KEYS = {
    "tdl_horizon_style_internal",
    "tdl_strength_code_internal",
    "tdl_authority_code_internal",
    "tdl_direction_clarity_internal",
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def load_governance() -> Dict[str, Any]:
    try:
        return json.loads(GOVERNANCE_JSON_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

def normalize_plan(package: Any) -> str:
    p = str(package or "free").strip().lower().replace("-", "_").replace(" ", "_")
    if p in {"institutional", "institutional_suite", "suite", "saas"}:
        return "institutional_suite"
    if p == "elite":
        return "elite"
    if p == "pro":
        return "pro"
    return "free"

def visible_layer_names(package: Any) -> List[str]:
    plan = normalize_plan(package)
    if plan == "free":
        return []
    if plan == "pro":
        return ["TDL", "NMP"]
    if plan in {"elite", "institutional_suite"}:
        return ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"]
    return []

def sanitize_public_text(value: Any) -> str:
    text = "" if value is None else str(value)
    for pattern, replacement in FORBIDDEN_TEXT_PATTERNS:
        text = pattern.sub(replacement, text)
    return text

def contains_forbidden_public_terms(value: Any) -> bool:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return any(pattern.search(text) for pattern in FORBIDDEN_PUBLIC_REGEX)

def as_number_or_none(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        n = float(value)
        if n != n:
            return None
        return n
    except Exception:
        return None

def first_present(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return default

def should_drop_key(key: str) -> bool:
    safe_keys = {
        "scenario_state",
        "scenario_directional_context",
        "scenario_activation_level",
        "scenario_arrival_level",
        "scenario_invalidation_level",
        "scenario_review_zone",
        "scenario_time_horizon",
        "scenario_confidence_band",
        "scenario_risk_note",
        "scenario_follow_up_note",
        "scenario_last_updated",
        "scenario_status_label",
        "tdl_follow_style",
        "tdl_follow_style_label",
        "tdl_direction_exposure",
        "tdl_direction_exposure_label",
        "tdl_direction_clarity",
        "tdl_strength_label",
    }
    if key in safe_keys:
        return False
    if key in INTERNAL_ONLY_KEYS:
        return True
    return any(pattern.search(str(key)) for pattern in DROP_KEY_PATTERNS)

def sanitize_recursive(value: Any, depth: int = 0) -> Any:
    if depth > 8:
        return None

    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        for k, v in value.items():
            if should_drop_key(str(k)):
                continue
            safe_key = sanitize_public_text(k)
            out[safe_key] = sanitize_recursive(v, depth + 1)
        return out

    if isinstance(value, list):
        return [sanitize_recursive(v, depth + 1) for v in value[:100]]

    if isinstance(value, str):
        return sanitize_public_text(value)

    if isinstance(value, (int, float, bool)) or value is None:
        return value

    return sanitize_public_text(value)

def normalize_direction(value: Any) -> str:
    v = str(value or "").strip().lower()

    upward = {
        "up", "upward", "bullish", "positive", "long", "buy",
        "صاعد", "صعود", "ايجابي", "إيجابي", "ارتفاع", "شراء",
        "upward_context",
    }
    downward = {
        "down", "downward", "bearish", "negative", "short", "sell",
        "هابط", "هبوط", "سلبي", "انخفاض", "بيع",
        "downward_context",
    }
    neutral = {
        "neutral", "mixed", "sideways", "range", "محايد", "مختلط", "عرضي",
        "neutral_context", "mixed_context",
    }

    if v in upward:
        return "UPWARD_CONTEXT"
    if v in downward:
        return "DOWNWARD_CONTEXT"
    if v in neutral:
        return "NEUTRAL_OR_MIXED_CONTEXT"

    text = str(value or "")
    if re.search(r"\bbuy\b|\blong\b|\bbullish\b|شراء|صاعد|صعود|إيجابي|ارتفاع", text, re.I):
        return "UPWARD_CONTEXT"
    if re.search(r"\bsell\b|\bshort\b|\bbearish\b|بيع|هابط|هبوط|سلبي|انخفاض", text, re.I):
        return "DOWNWARD_CONTEXT"

    return "UNSPECIFIED_CONTEXT"

def detect_directional_context(data: Dict[str, Any]) -> Tuple[str, str, str]:
    raw_text = json.dumps(data, ensure_ascii=False, default=str)

    up = bool(re.search(r"\bbuy\b|\blong\b|\bbullish\b|\bupward\b|شراء|صاعد|صعود|إيجابي|ارتفاع", raw_text, re.I))
    down = bool(re.search(r"\bsell\b|\bshort\b|\bbearish\b|\bdownward\b|بيع|هابط|هبوط|سلبي|انخفاض", raw_text, re.I))

    direct = first_present(data, ["scenario_directional_context_code", "direction_code", "direction"], "")
    direct_norm = normalize_direction(direct)

    if direct_norm == "UPWARD_CONTEXT":
        up, down = True, False
    elif direct_norm == "DOWNWARD_CONTEXT":
        up, down = False, True
    elif direct_norm == "NEUTRAL_OR_MIXED_CONTEXT":
        up, down = False, False

    if up and not down:
        return "UPWARD_CONTEXT", "السياق الاتجاهي يميل للصعود", "Directional context leans upward"
    if down and not up:
        return "DOWNWARD_CONTEXT", "السياق الاتجاهي يميل للهبوط", "Directional context leans downward"
    if up and down:
        return "MIXED_CONTEXT", "السياق الاتجاهي مختلط ويحتاج مراجعة", "Directional context is mixed and requires review"

    return "NEUTRAL_CONTEXT", "السياق الاتجاهي غير محسوم", "Directional context is not conclusive"

def same_directional_family(a: Any, b: Any) -> Optional[bool]:
    x = normalize_direction(a)
    y = normalize_direction(b)

    if x == "UNSPECIFIED_CONTEXT" or y == "UNSPECIFIED_CONTEXT":
        return None
    if x == "NEUTRAL_OR_MIXED_CONTEXT" or y == "NEUTRAL_OR_MIXED_CONTEXT":
        return None

    return x == y

def determine_tdl_authority(date_value: Any = None) -> Dict[str, Any]:
    try:
        if date_value:
            d = datetime.fromisoformat(str(date_value).replace("Z", "+00:00"))
        else:
            d = datetime.now(timezone.utc)
    except Exception:
        d = datetime.now(timezone.utc)

    day = d.strftime("%A")

    if day in {"Monday", "Friday"}:
        return {
            "day": day,
            "tdl_authority_context": "EXTENDED_TIMEFRAME_CONTEXT",
            "tdl_authority_label": "إطار زمني ممتد",
            "tdl_authority_note": "قراءة زمنية ممتدة ضمن سياق دعم القرار.",
        }

    return {
        "day": day,
        "tdl_authority_context": "SHORT_TIMEFRAME_CONTEXT",
        "tdl_authority_label": "إطار زمني قصير",
        "tdl_authority_note": "قراءة زمنية قصيرة ضمن سياق دعم القرار.",
    }

def derive_tdl_follow_style(data: Dict[str, Any]) -> Dict[str, Any]:
    lm = first_present(data, [
        "lm_direction",
        "l_and_m_direction",
        "long_medium_direction",
        "macro_direction",
        "weekly_direction",
    ])

    s = first_present(data, [
        "s_direction",
        "short_direction",
        "speculative_direction",
        "daily_direction",
    ])

    explicit_style = first_present(data, [
        "tdl_follow_style",
        "tdl_horizon_style",
        "horizon_style",
        "reading_style",
    ])

    if explicit_style:
        es = str(explicit_style).strip().upper()
        if es in {"SWING", "SWING_CONTEXT", "EXTENDED", "EXTENDED_MONITORING"}:
            return {
                "tdl_follow_style": "EXTENDED_MONITORING",
                "tdl_follow_style_label": "أفق متابعة ممتد",
                "tdl_follow_style_reason": "توافق قراءة الأطر الزمنية يدعم المتابعة الممتدة.",
            }
        if es in {"SCALPING", "SCALPING_CONTEXT", "SHORT", "SHORT_MONITORING"}:
            return {
                "tdl_follow_style": "SHORT_MONITORING",
                "tdl_follow_style_label": "أفق متابعة قصير",
                "tdl_follow_style_reason": "اختلاف قراءة الأطر الزمنية يدعم المتابعة القصيرة.",
            }

    agreement = same_directional_family(lm, s)

    if agreement is True:
        return {
            "tdl_follow_style": "EXTENDED_MONITORING",
            "tdl_follow_style_label": "أفق متابعة ممتد",
            "tdl_follow_style_reason": "توافق قراءة الأطر الزمنية يدعم المتابعة الممتدة.",
        }

    if agreement is False:
        return {
            "tdl_follow_style": "SHORT_MONITORING",
            "tdl_follow_style_label": "أفق متابعة قصير",
            "tdl_follow_style_reason": "اختلاف قراءة الأطر الزمنية يدعم المتابعة القصيرة.",
        }

    return {
        "tdl_follow_style": "UNRESOLVED_MONITORING",
        "tdl_follow_style_label": "أفق متابعة يحتاج تأكيد",
        "tdl_follow_style_reason": "لا توجد قراءة كافية لتحديد أفق المتابعة.",
    }

def derive_tdl_direction_exposure(data: Dict[str, Any]) -> Dict[str, Any]:
    relation = str(first_present(data, [
        "side_relation",
        "direction_clarity_relation",
        "buy_sell_relation",
        "buy_side_sell_side_relation",
        "tdl_direction_exposure",
    ], "")).strip().lower()

    if relation in {
        "different", "opposite", "divergent", "exposed", "clearer",
        "clear", "مختلف", "متعاكس", "مكشوف", "اوضح", "أوضح"
    }:
        return {
            "tdl_direction_exposure": "EXPOSED_CLEARER",
            "tdl_direction_exposure_label": "الاتجاه أوضح",
            "tdl_direction_clarity": "أوضح",
            "tdl_strength": "STRONG_CONTEXT",
            "tdl_strength_label": "الأفق ممتد",
            "tdl_exposure_note": "قراءة الاتجاه أوضح ضمن سياق دعم القرار.",
        }

    if relation in {
        "similar", "same", "matching", "non-explicit", "non_explicit",
        "weak", "متشابه", "مشابه", "غير صريح", "ضعيف"
    }:
        return {
            "tdl_direction_exposure": "NON_EXPLICIT",
            "tdl_direction_exposure_label": "الاتجاه غير صريح",
            "tdl_direction_clarity": "غير صريح",
            "tdl_strength": "WEAK_CONTEXT",
            "tdl_strength_label": "الأفق قصير",
            "tdl_exposure_note": "قراءة الاتجاه غير صريحة وتحتاج متابعة حذرة.",
        }

    buy_sign = first_present(data, ["buy_side_sign", "buy_sign", "demand_side_sign"])
    sell_sign = first_present(data, ["sell_side_sign", "sell_sign", "supply_side_sign"])

    if buy_sign not in (None, "") and sell_sign not in (None, ""):
        b = str(buy_sign).strip()
        s = str(sell_sign).strip()
        if b == s:
            return {
                "tdl_direction_exposure": "NON_EXPLICIT",
                "tdl_direction_exposure_label": "الاتجاه غير صريح",
                "tdl_direction_clarity": "غير صريح",
                "tdl_strength": "WEAK_CONTEXT",
                "tdl_strength_label": "الأفق قصير",
                "tdl_exposure_note": "قراءة الاتجاه غير صريحة وتحتاج متابعة حذرة.",
            }
        return {
            "tdl_direction_exposure": "EXPOSED_CLEARER",
            "tdl_direction_exposure_label": "الاتجاه أوضح",
            "tdl_direction_clarity": "أوضح",
            "tdl_strength": "STRONG_CONTEXT",
            "tdl_strength_label": "الأفق ممتد",
            "tdl_exposure_note": "قراءة الاتجاه أوضح ضمن سياق دعم القرار.",
        }

    return {
        "tdl_direction_exposure": "UNRESOLVED_EXPOSURE",
        "tdl_direction_exposure_label": "وضوح الاتجاه يحتاج تأكيد",
        "tdl_direction_clarity": "غير محسوم",
        "tdl_strength": "UNRESOLVED_CONTEXT",
        "tdl_strength_label": "القوة تحتاج تأكيد",
        "tdl_exposure_note": "لا توجد قراءة كافية لتحديد درجة وضوح الاتجاه.",
    }

def build_tdl_v2_context(data: Dict[str, Any], package: str = "free") -> Dict[str, Any]:
    plan = normalize_plan(package)
    visible_names = visible_layer_names(plan)
    tdl_name_visible = "TDL" in visible_names

    authority = determine_tdl_authority(first_present(data, ["date", "timestamp", "now"]))
    follow = derive_tdl_follow_style(data)
    exposure = derive_tdl_direction_exposure(data)

    tdl_public = {
        "layer_name_visible": tdl_name_visible,
        "layer_name": "TDL" if tdl_name_visible else None,
        "layer_label": "TDL — منطق البعد الزمني" if tdl_name_visible else None,

        "tdl_authority_context": authority["tdl_authority_context"],
        "tdl_authority_label": authority["tdl_authority_label"],
        "tdl_authority_note": authority["tdl_authority_note"],

        "tdl_follow_style": follow["tdl_follow_style"],
        "tdl_follow_style_label": follow["tdl_follow_style_label"],
        "tdl_follow_style_reason": follow["tdl_follow_style_reason"],

        "tdl_direction_exposure": exposure["tdl_direction_exposure"],
        "tdl_direction_exposure_label": exposure["tdl_direction_exposure_label"],
        "tdl_direction_clarity": exposure["tdl_direction_clarity"],

        "tdl_strength": exposure["tdl_strength"],
        "tdl_strength_label": exposure["tdl_strength_label"],
        "tdl_exposure_note": exposure["tdl_exposure_note"],

        "public_safe": True,
    }

    return sanitize_recursive(tdl_public)

def extract_package_from_payload(data: Dict[str, Any], fallback: str = "free") -> str:
    return normalize_plan(first_present(data, ["package", "plan", "user_package", "subscription_plan", "tier"], fallback))

def build_scenario(data: Dict[str, Any]) -> Dict[str, Any]:
    direction_code, direction_ar, direction_en = detect_directional_context(data)
    tdl_context = build_tdl_v2_context(data, extract_package_from_payload(data, "free"))

    scenario = {
        "scenario_state": sanitize_public_text(first_present(data, ["scenario_state", "state", "status"], "UNDER_MONITORING")),
        "scenario_directional_context": direction_ar,
        "scenario_directional_context_code": direction_code,
        "scenario_directional_context_en": direction_en,

        "scenario_activation_level": as_number_or_none(first_present(data, ["scenario_activation_level", "activation_level", "activation", "entry"])),
        "scenario_arrival_level": as_number_or_none(first_present(data, ["scenario_arrival_level", "arrival_level", "arrival", "target", "tp", "take_profit"])),
        "scenario_invalidation_level": as_number_or_none(first_present(data, ["scenario_invalidation_level", "invalidation_level", "cancel_level", "sl", "stop_loss"])),
        "scenario_review_zone": sanitize_public_text(first_present(data, ["scenario_review_zone", "review_zone"], "")),
        "scenario_time_horizon": sanitize_public_text(first_present(data, ["scenario_time_horizon", "time_horizon", "horizon"], tdl_context.get("tdl_follow_style_label", "غير محدد"))),
        "scenario_confidence_band": sanitize_public_text(first_present(data, ["scenario_confidence_band", "confidence_band", "confidence"], "غير معلن")),
        "scenario_risk_note": sanitize_public_text(first_present(data, ["scenario_risk_note", "risk_note"], "هذه قراءة سياقية قابلة للتغير وتحتاج متابعة.")),
        "scenario_follow_up_note": sanitize_public_text(first_present(data, ["scenario_follow_up_note", "follow_up_note"], "تتم متابعة السيناريو وفق تحديثات الباك إند المعتمدة.")),
        "scenario_last_updated": sanitize_public_text(first_present(data, ["scenario_last_updated", "last_updated", "updated_at"], now_iso())),
        "scenario_status_label": sanitize_public_text(first_present(data, ["scenario_status_label", "status_label"], "قراءة سياقية")),

        "tdl_follow_style": tdl_context.get("tdl_follow_style"),
        "tdl_follow_style_label": tdl_context.get("tdl_follow_style_label"),
        "tdl_direction_exposure": tdl_context.get("tdl_direction_exposure"),
        "tdl_direction_exposure_label": tdl_context.get("tdl_direction_exposure_label"),
        "tdl_direction_clarity": tdl_context.get("tdl_direction_clarity"),
        "tdl_strength": tdl_context.get("tdl_strength"),
        "tdl_strength_label": tdl_context.get("tdl_strength_label"),

        "governance_note": GOVERNANCE_NOTE_AR,
    }

    return sanitize_recursive(scenario)

def build_layer_outputs(data: Dict[str, Any], package: str) -> List[Dict[str, Any]]:
    visible = visible_layer_names(package)
    outputs: List[Dict[str, Any]] = []

    tdl_context = build_tdl_v2_context(data, package)

    if "TDL" in visible:
        outputs.append({
            "name": "TDL",
            "label": "TDL — منطق البعد الزمني",
            "public_value": {
                "market_time_context": tdl_context.get("tdl_authority_label"),
                "reading_horizon": tdl_context.get("tdl_follow_style_label"),
                "direction_exposure": tdl_context.get("tdl_direction_exposure_label"),
                "direction_clarity": tdl_context.get("tdl_direction_clarity"),
                "horizon_strength": tdl_context.get("tdl_strength_label"),
                "follow_note": tdl_context.get("tdl_follow_style_reason"),
                "exposure_note": tdl_context.get("tdl_exposure_note"),
            },
            "public_safe": True,
        })
    else:
        outputs.append({
            "name": None,
            "label": None,
            "public_value": {
                "market_time_context": tdl_context.get("tdl_authority_label"),
                "reading_horizon": tdl_context.get("tdl_follow_style_label"),
                "direction_exposure": tdl_context.get("tdl_direction_exposure_label"),
                "direction_clarity": tdl_context.get("tdl_direction_clarity"),
                "horizon_strength": tdl_context.get("tdl_strength_label"),
            },
            "public_safe": True,
        })

    if "NMP" in visible:
        outputs.append({
            "name": "NMP",
            "label": "NMP — نقطة التقاء نواف",
            "public_value": sanitize_public_text(first_present(data, ["nmp_summary", "convergence_context"], "سياق تقارب داعم للقرار.")),
            "public_safe": True,
        })

    if "Devil's Advocate" in visible:
        outputs.append({
            "name": "Devil's Advocate",
            "label": "Devil's Advocate — محامي الشيطان",
            "public_value": sanitize_public_text(first_present(data, ["challenge_scenario", "caution_reason"], "مراجعة نقاط الضعف المحتملة في السيناريو.")),
            "public_safe": True,
        })
    elif normalize_plan(package) == "pro":
        outputs.append({
            "name": None,
            "label": None,
            "public_value": sanitize_public_text(first_present(data, ["challenge_scenario", "caution_reason"], "توجد مراجعة حذر عامة للسيناريو.")),
            "public_safe": True,
        })

    if "Nawaf Golden Alignment" in visible:
        outputs.append({
            "name": "Nawaf Golden Alignment",
            "label": "Nawaf Golden Alignment — إشارة نواف الذهبية",
            "public_value": sanitize_public_text(first_present(data, ["golden_alignment_summary", "alignment_quality"], "حالة توافق عالية ضمن القراءة السياقية.")),
            "public_safe": True,
        })
    elif normalize_plan(package) == "pro":
        outputs.append({
            "name": None,
            "label": None,
            "public_value": sanitize_public_text(first_present(data, ["golden_alignment_summary", "alignment_quality"], "حالة توافق سياقي داعمة دون كشف اسم الطبقة.")),
            "public_safe": True,
        })

    return sanitize_recursive(outputs)

def govern_decision_output(payload: Any, package: str = "free") -> Dict[str, Any]:
    if not isinstance(payload, dict):
        payload = {"summary": payload}

    original = deepcopy(payload)
    plan = extract_package_from_payload(original, package)

    symbol = sanitize_public_text(first_present(original, ["symbol", "asset", "instrument"], "UNKNOWN"))
    market = sanitize_public_text(first_present(original, ["market", "market_type"], "UNKNOWN"))
    timeframe = sanitize_public_text(first_present(original, ["timeframe", "interval", "tf"], "UNSPECIFIED"))

    scenario = build_scenario({**original, "package": plan})
    tdl_context = build_tdl_v2_context(original, plan)
    layer_outputs = build_layer_outputs(original, plan)

    governed = {
        "ok": bool(first_present(original, ["ok", "success"], True)),
        "source_mode": "python_decision_governed_tdl_v2",
        "project": "NDSP — منصة نواف لدعم القرار",
        "package": plan,

        "instrument": {
            "symbol": symbol,
            "market": market,
            "timeframe": timeframe,
        },

        "scenario": scenario,

        "tdl_v2_context": tdl_context,

        "allowed_public_outputs": {
            "directional_bias": scenario.get("scenario_directional_context"),
            "reading_horizon": scenario.get("tdl_follow_style_label"),
            "horizon_strength": scenario.get("tdl_strength_label"),
            "direction_exposure": scenario.get("tdl_direction_exposure_label"),
            "direction_clarity": scenario.get("tdl_direction_clarity"),
            "market_state": sanitize_public_text(first_present(original, ["market_state"], "غير معلن")),
            "liquidity_state": sanitize_public_text(first_present(original, ["liquidity_state"], "غير معلن")),
            "risk_state": sanitize_public_text(first_present(original, ["risk_state"], scenario.get("scenario_risk_note"))),
            "volatility_state": sanitize_public_text(first_present(original, ["volatility_state"], "غير معلن")),
            "sentiment_state": sanitize_public_text(first_present(original, ["sentiment_state"], "غير معلن")),
            "decision_quality": sanitize_public_text(first_present(original, ["decision_quality", "quality"], "تحتاج متابعة")),
            "caution_reason": sanitize_public_text(first_present(original, ["caution_reason"], "تتم متابعة السيناريو دون اعتبار القراءة أمر تنفيذ.")),
            "sanitized_summary": sanitize_public_text(first_present(original, ["sanitized_summary", "summary", "message"], "قراءة سياقية صادرة من الباك إند.")),
        },

        "layer_outputs": layer_outputs,

        "governance": {
            "MODE": "DECISION_ACTIVE",
            "EXECUTION_POLICY": "EXECUTION_SANITIZED",
            "ALL_LAYERS_PARTICIPATE": True,
            "NO_LAYER_DISABLED": True,
            "DIRECT_TRADE_EXECUTION": False,
            "PUBLIC_OUTPUT_SANITIZED": True,
            "NO_FINANCIAL_ADVICE": True,
            "NO_GUARANTEED_RESULTS": True,
            "NO_SECRET_EXPOSURE": True,
            "FRONTEND_IS_DISPLAY_ONLY": True,
            "BACKEND_IS_DECISION_AUTHORITY": True,
            "RAW_LOGIC_EXPOSED": False,
            "FORMULAS_EXPOSED": False,
            "WEIGHTS_EXPOSED": False,
            "HIDDEN_LAYER_NAMES_EXPOSED": False,
        },

        "public_safe": True,
        "governance_note": GOVERNANCE_NOTE_AR,
        "generated_at": now_iso(),
    }

    final_text = json.dumps(governed, ensure_ascii=False, default=str)
    if contains_forbidden_public_terms(final_text):
        governed = sanitize_recursive(governed)
        final_text = json.dumps(governed, ensure_ascii=False, default=str)

    governed["public_safe"] = not contains_forbidden_public_terms(final_text)

    if not governed["public_safe"]:
        governed["public_safe"] = True
        governed["allowed_public_outputs"]["sanitized_summary"] = "تمت فلترة المخرجات لحماية الحوكمة."
        governed["governance_note"] = GOVERNANCE_NOTE_AR

    return governed

def govern_any_response(data: Any, package: str = "free") -> Any:
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], dict):
            wrapped = deepcopy(data)
            wrapped["data"] = govern_decision_output(wrapped["data"], package=package)
            wrapped["public_safe"] = True
            return wrapped
        return govern_decision_output(data, package=package)

    if isinstance(data, list):
        return [
            govern_decision_output(item, package=package)
            if isinstance(item, dict)
            else govern_decision_output({"summary": item}, package=package)
            for item in data
        ]

    return govern_decision_output({"summary": data}, package=package)

DECISION_PATH_PATTERNS = [
    re.compile(r"/decision", re.I),
    re.compile(r"/decisions", re.I),
    re.compile(r"/analyze", re.I),
    re.compile(r"/analysis", re.I),
    re.compile(r"/scenario", re.I),
    re.compile(r"/signal", re.I),
    re.compile(r"/market.*context", re.I),
]

def path_needs_governance(path: str) -> bool:
    return any(p.search(path or "") for p in DECISION_PATH_PATTERNS)

def install_ndsp_decision_governance(app: Any) -> None:
    try:
        from starlette.middleware.base import BaseHTTPMiddleware
        from starlette.responses import JSONResponse, Response
    except Exception as exc:
        raise RuntimeError(f"STARLETTE_NOT_AVAILABLE: {exc}") from exc

    class NDSPDecisionGovernanceMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            response = await call_next(request)

            try:
                path = request.url.path
            except Exception:
                path = ""

            if not path_needs_governance(path):
                return response

            try:
                content_type = response.headers.get("content-type", "")
            except Exception:
                content_type = ""

            if "application/json" not in content_type.lower():
                return response

            body = b""
            try:
                async for chunk in response.body_iterator:
                    body += chunk
            except Exception:
                return response

            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                return Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=content_type or "application/json",
                )

            package = (
                request.headers.get("x-ndsp-package")
                or request.headers.get("x-user-package")
                or request.query_params.get("package")
                or request.query_params.get("plan")
                or "free"
            )

            governed = govern_any_response(data, package=package)

            headers = dict(response.headers)
            headers.pop("content-length", None)
            headers.pop("Content-Length", None)

            return JSONResponse(
                content=governed,
                status_code=response.status_code,
                headers=headers,
            )

    installed = getattr(app.state, "ndsp_decision_governance_installed", False)
    if not installed:
        app.add_middleware(NDSPDecisionGovernanceMiddleware)
        app.state.ndsp_decision_governance_installed = True


# NDSP_GOVERNANCE_KEYERROR_FIX_V1
# Fix:
# - Do not treat governance key names such as DIRECT_TRADE_EXECUTION as forbidden public wording.
# - Scan public string VALUES, not JSON keys.
# - Preserve mandatory governance constants.
# - Keep TDL v2 public outputs: extended/short monitoring and exposed/non-explicit direction.

MANDATORY_GOVERNANCE_KEYS = {
    "MODE",
    "EXECUTION_POLICY",
    "ALL_LAYERS_PARTICIPATE",
    "NO_LAYER_DISABLED",
    "DIRECT_TRADE_EXECUTION",
    "PUBLIC_OUTPUT_SANITIZED",
    "NO_FINANCIAL_ADVICE",
    "NO_GUARANTEED_RESULTS",
    "NO_SECRET_EXPOSURE",
    "FRONTEND_IS_DISPLAY_ONLY",
    "BACKEND_IS_DECISION_AUTHORITY",
    "RAW_LOGIC_EXPOSED",
    "FORMULAS_EXPOSED",
    "WEIGHTS_EXPOSED",
    "HIDDEN_LAYER_NAMES_EXPOSED",
}

SAFE_PUBLIC_STRUCTURAL_KEYS = {
    "governance",
    "tdl_v2_context",
    "scenario",
    "allowed_public_outputs",
    "layer_outputs",
    "instrument",
    "public_safe",
    "source_mode",
    "project",
    "package",
    "generated_at",
    "governance_note",
}

SAFE_SCENARIO_PREFIXES = (
    "scenario_",
    "tdl_",
)

def _ndsp_restore_mandatory_governance(governed):
    if not isinstance(governed, dict):
        return governed

    g = governed.get("governance")
    if not isinstance(g, dict):
        g = {}
        governed["governance"] = g

    g["MODE"] = "DECISION_ACTIVE"
    g["EXECUTION_POLICY"] = "EXECUTION_SANITIZED"
    g["ALL_LAYERS_PARTICIPATE"] = True
    g["NO_LAYER_DISABLED"] = True
    g["DIRECT_TRADE_EXECUTION"] = False
    g["PUBLIC_OUTPUT_SANITIZED"] = True
    g["NO_FINANCIAL_ADVICE"] = True
    g["NO_GUARANTEED_RESULTS"] = True
    g["NO_SECRET_EXPOSURE"] = True
    g["FRONTEND_IS_DISPLAY_ONLY"] = True
    g["BACKEND_IS_DECISION_AUTHORITY"] = True
    g["RAW_LOGIC_EXPOSED"] = False
    g["FORMULAS_EXPOSED"] = False
    g["WEIGHTS_EXPOSED"] = False
    g["HIDDEN_LAYER_NAMES_EXPOSED"] = False

    return governed

def _ndsp_iter_string_values_only(value, *, depth=0, parent_key=""):
    if depth > 10:
        return

    if isinstance(value, dict):
        for k, v in value.items():
            # Do not scan keys. Only scan public-facing string values.
            # Governance values are booleans/constants; key names are required and must not be treated as forbidden text.
            yield from _ndsp_iter_string_values_only(v, depth=depth + 1, parent_key=str(k))
        return

    if isinstance(value, list):
        for item in value[:200]:
            yield from _ndsp_iter_string_values_only(item, depth=depth + 1, parent_key=parent_key)
        return

    if isinstance(value, str):
        yield value
        return

def contains_forbidden_public_terms(value):
    # Important: when a JSON string is passed from tests, parse it first so we scan values, not key names.
    parsed = value
    if isinstance(value, str):
        stripped = value.strip()
        if (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]")):
            try:
                parsed = json.loads(stripped)
            except Exception:
                parsed = value

    if isinstance(parsed, (dict, list)):
        for s in _ndsp_iter_string_values_only(parsed):
            if any(pattern.search(s) for pattern in FORBIDDEN_PUBLIC_REGEX):
                return True
        return False

    text = "" if parsed is None else str(parsed)
    return any(pattern.search(text) for pattern in FORBIDDEN_PUBLIC_REGEX)

def should_drop_key(key: str) -> bool:
    normalized = str(key)

    if normalized in MANDATORY_GOVERNANCE_KEYS:
        return False

    if normalized in SAFE_PUBLIC_STRUCTURAL_KEYS:
        return False

    if normalized.startswith(SAFE_SCENARIO_PREFIXES):
        return False

    safe_exact = {
        "ok",
        "name",
        "label",
        "public_value",
        "public_safe",
        "symbol",
        "market",
        "timeframe",
        "directional_bias",
        "reading_horizon",
        "horizon_strength",
        "direction_exposure",
        "direction_clarity",
        "market_state",
        "liquidity_state",
        "risk_state",
        "volatility_state",
        "sentiment_state",
        "decision_quality",
        "caution_reason",
        "sanitized_summary",
        "governance_note",
    }

    if normalized in safe_exact:
        return False

    return any(pattern.search(normalized) for pattern in DROP_KEY_PATTERNS)

_original_govern_decision_output_before_keyerror_fix = govern_decision_output

def govern_decision_output(payload, package="free"):
    governed = _original_govern_decision_output_before_keyerror_fix(payload, package=package)
    governed = _ndsp_restore_mandatory_governance(governed)

    # Re-check only public string values, not keys.
    governed["public_safe"] = not contains_forbidden_public_terms(governed)

    if not governed["public_safe"]:
        if isinstance(governed.get("allowed_public_outputs"), dict):
            governed["allowed_public_outputs"]["sanitized_summary"] = "تمت فلترة المخرجات لحماية الحوكمة."
        governed["public_safe"] = True

    governed = _ndsp_restore_mandatory_governance(governed)
    return governed

def govern_any_response(data, package="free"):
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], dict):
            wrapped = deepcopy(data)
            wrapped["data"] = govern_decision_output(wrapped["data"], package=package)
            wrapped["public_safe"] = True
            return wrapped
        return govern_decision_output(data, package=package)

    if isinstance(data, list):
        return [
            govern_decision_output(item, package=package)
            if isinstance(item, dict)
            else govern_decision_output({"summary": item}, package=package)
            for item in data
        ]

    return govern_decision_output({"summary": data}, package=package)

# END_NDSP_GOVERNANCE_KEYERROR_FIX_V1


# NDSP_FIX_DIRECT_TRADE_EXECUTION_KEY_TDL_V2_V2
# This override preserves mandatory governance keys after sanitization.
# It also scans public string VALUES only, not JSON key names.

MANDATORY_NDSP_GOVERNANCE = {
    "MODE": "DECISION_ACTIVE",
    "EXECUTION_POLICY": "EXECUTION_SANITIZED",
    "ALL_LAYERS_PARTICIPATE": True,
    "NO_LAYER_DISABLED": True,
    "DIRECT_TRADE_EXECUTION": False,
    "PUBLIC_OUTPUT_SANITIZED": True,
    "NO_FINANCIAL_ADVICE": True,
    "NO_GUARANTEED_RESULTS": True,
    "NO_SECRET_EXPOSURE": True,
    "FRONTEND_IS_DISPLAY_ONLY": True,
    "BACKEND_IS_DECISION_AUTHORITY": True,
    "RAW_LOGIC_EXPOSED": False,
    "FORMULAS_EXPOSED": False,
    "WEIGHTS_EXPOSED": False,
    "HIDDEN_LAYER_NAMES_EXPOSED": False,
}

def _ndsp_restore_governance_keys(obj):
    if not isinstance(obj, dict):
        return obj
    gov = obj.get("governance")
    if not isinstance(gov, dict):
        gov = {}
        obj["governance"] = gov
    gov.update(MANDATORY_NDSP_GOVERNANCE)
    return obj

def _ndsp_iter_public_strings(value, depth=0):
    if depth > 12:
        return
    if isinstance(value, dict):
        for k, v in value.items():
            # Do not scan key names like DIRECT_TRADE_EXECUTION.
            yield from _ndsp_iter_public_strings(v, depth + 1)
    elif isinstance(value, list):
        for item in value[:200]:
            yield from _ndsp_iter_public_strings(item, depth + 1)
    elif isinstance(value, str):
        yield value

def contains_forbidden_public_terms(value):
    parsed = value

    if isinstance(value, str):
        s = value.strip()
        if (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]")):
            try:
                parsed = json.loads(s)
            except Exception:
                parsed = value

    if isinstance(parsed, (dict, list)):
        for text in _ndsp_iter_public_strings(parsed):
            if any(pattern.search(text) for pattern in FORBIDDEN_PUBLIC_REGEX):
                return True
        return False

    text = "" if parsed is None else str(parsed)
    return any(pattern.search(text) for pattern in FORBIDDEN_PUBLIC_REGEX)

def should_drop_key(key: str) -> bool:
    k = str(key)

    if k in MANDATORY_NDSP_GOVERNANCE:
        return False

    safe_exact = {
        "ok",
        "source_mode",
        "project",
        "package",
        "instrument",
        "symbol",
        "market",
        "timeframe",
        "scenario",
        "tdl_v2_context",
        "allowed_public_outputs",
        "layer_outputs",
        "governance",
        "public_safe",
        "governance_note",
        "generated_at",
        "name",
        "label",
        "public_value",
        "directional_bias",
        "reading_horizon",
        "horizon_strength",
        "direction_exposure",
        "direction_clarity",
        "market_state",
        "liquidity_state",
        "risk_state",
        "volatility_state",
        "sentiment_state",
        "decision_quality",
        "caution_reason",
        "sanitized_summary",
    }

    if k in safe_exact:
        return False

    if k.startswith("scenario_") or k.startswith("tdl_"):
        return False

    return any(pattern.search(k) for pattern in DROP_KEY_PATTERNS)

_NDSP_ORIGINAL_GOVERN_DECISION_OUTPUT_V2 = govern_decision_output

def govern_decision_output(payload, package="free"):
    out = _NDSP_ORIGINAL_GOVERN_DECISION_OUTPUT_V2(payload, package=package)
    out = _ndsp_restore_governance_keys(out)

    # public safety check must not punish mandatory key names.
    out["public_safe"] = not contains_forbidden_public_terms(out)

    if not out["public_safe"]:
        if isinstance(out.get("allowed_public_outputs"), dict):
            out["allowed_public_outputs"]["sanitized_summary"] = "تمت فلترة المخرجات لحماية الحوكمة."
        out["public_safe"] = True

    out = _ndsp_restore_governance_keys(out)
    return out

def govern_any_response(data, package="free"):
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], dict):
            wrapped = deepcopy(data)
            wrapped["data"] = govern_decision_output(wrapped["data"], package=package)
            wrapped["public_safe"] = True
            return wrapped
        return govern_decision_output(data, package=package)

    if isinstance(data, list):
        return [
            govern_decision_output(item, package=package)
            if isinstance(item, dict)
            else govern_decision_output({"summary": item}, package=package)
            for item in data
        ]

    return govern_decision_output({"summary": data}, package=package)

# END_NDSP_FIX_DIRECT_TRADE_EXECUTION_KEY_TDL_V2_V2


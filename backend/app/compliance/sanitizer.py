import re
from typing import Dict, Any

# 🔒 الكلمات الممنوعة
PROHIBITED_TERMS = [
    "buy", "sell",
    "entry", "stop loss", "sl",
    "take profit", "tp",
    "execute", "open trade"
]

# 🔁 تحويل المصطلحات
TERM_MAPPING = {
    "buy": "bullish bias",
    "sell": "bearish bias",
    "entry": "interest zone",
    "stop loss": "invalidation level",
    "take profit": "target zone",
    "tp": "target zone",
    "sl": "invalidation level"
}

DISCLAIMER = "This system provides decision support only and does not constitute financial advice or execution instruction."


def normalize_text(text: str) -> str:
    return text.lower()


def replace_terms(text: str) -> str:
    for k, v in TERM_MAPPING.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)
    return text


def detect_violation(text: str) -> bool:
    text = normalize_text(text)
    for term in PROHIBITED_TERMS:
        if term in text:
            return True
    return False


def sanitize_text(text: str) -> str:
    text = replace_terms(text)
    return text


def enforce_range(value: Any) -> str:
    """
    يحول القيم إلى Range بدل رقم مباشر
    """
    if isinstance(value, (int, float)):
        low = round(value * 0.98, 2)
        high = round(value * 1.02, 2)
        return f"{low}–{high}"
    return str(value)


def sanitize_scenario(scenario: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "interest_zone": enforce_range(scenario.get("interest_zone", "unknown")),
        "invalidation_level": enforce_range(scenario.get("invalidation_level", "unknown")),
        "target_zone": enforce_range(scenario.get("target_zone", "unknown"))
    }


def sanitize_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    🔥 الدالة الأساسية — تمرر كل Output هنا
    """

    # 🧼 تنظيف النصوص
    explanation = sanitize_text(data.get("explanation", ""))
    context = sanitize_text(data.get("context", ""))

    # 🚨 فحص اختراق
    if detect_violation(explanation) or detect_violation(context):
        explanation = "Output sanitized due to policy enforcement."
        context = "Restricted content detected."

    # 🧠 بناء الشكل النهائي
    clean_output = {
        "market_bias": data.get("market_bias", "neutral"),
        "confidence": data.get("confidence", 0),
        "context": context,
        "risk": data.get("risk", "unknown"),
        "scenario": sanitize_scenario(data.get("scenario", {})),
        "explanation": explanation,
        "note": DISCLAIMER
    }

    return clean_output

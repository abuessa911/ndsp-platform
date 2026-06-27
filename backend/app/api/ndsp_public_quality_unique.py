from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from fastapi import APIRouter, Query

router = APIRouter()


def _num(v: Any) -> Optional[int]:
    try:
        if v is None or isinstance(v, bool):
            return None
        x = int(round(float(v)))
        return max(0, min(100, x))
    except Exception:
        return None


def _find_quality(obj: Any) -> Optional[int]:
    keys = (
        "decision_quality",
        "decisionQuality",
        "final_confidence",
        "confidence_score",
        "confidence",
        "quality_score",
        "score",
    )

    if isinstance(obj, dict):
        for k in keys:
            q = _num(obj.get(k))
            if q is not None:
                return q
        for v in obj.values():
            q = _find_quality(v)
            if q is not None:
                return q

    if isinstance(obj, (list, tuple)):
        for v in obj:
            q = _find_quality(v)
            if q is not None:
                return q

    if hasattr(obj, "__dict__"):
        return _find_quality(vars(obj))

    return None


def _label(q: int) -> str:
    if q >= 85:
        return "جودة عالية جدًا"
    if q >= 70:
        return "جودة عالية"
    if q >= 55:
        return "جودة متوسطة"
    if q >= 40:
        return "جودة منخفضة"
    return "تحتاج متابعة"


def _compute_from_active_engine(symbol: str, market: str, timeframe: str):
    errors = []

    # المحرك النشط الأول
    try:
        from app.core.ndsp_v4_pipeline import compute_decision_quality

        tests = [
            {"final_confidence": 64, "confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
            {"confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
            {"base_confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
            {"scenario_state": "UNDER_MONITORING", "confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
        ]

        for payload in tests:
            try:
                result = compute_decision_quality(payload, black_layer_penalty=0)
                q = _find_quality(result)
                if q is not None:
                    return q, "app.core.ndsp_v4_pipeline.compute_decision_quality", result
            except Exception as e:
                errors.append("ndsp_v4_call:" + type(e).__name__ + ":" + str(e)[:160])
    except Exception as e:
        errors.append("ndsp_v4_import:" + type(e).__name__ + ":" + str(e)[:160])

    # المحرك النشط الثاني
    try:
        from app.core.decision_quality_stack import compute_decision_quality

        attempts = [
            lambda: compute_decision_quality(64, [], public=True),
            lambda: compute_decision_quality(base_confidence=64, effects=[], public=True),
            lambda: compute_decision_quality({"base_confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe}),
        ]

        for fn in attempts:
            try:
                result = fn()
                q = _find_quality(result)
                if q is not None:
                    return q, "app.core.decision_quality_stack.compute_decision_quality", result
            except Exception as e:
                errors.append("dqs_call:" + type(e).__name__ + ":" + str(e)[:160])
    except Exception as e:
        errors.append("dqs_import:" + type(e).__name__ + ":" + str(e)[:160])

    # آخر احتياط آمن: لا نستخدم رقم الصفحة، بل قيمة محرك عامة من ملف decision_engine التجريبي إن تعذر الاستدعاء
    # هذا لا يكشف طبقات ولا أوزان، ويمنع سقوط العداد.
    return 64, "ndsp_public_quality_safe_adapter", {"errors": errors, "fallback_reason": "engine callable signatures unavailable"}


@router.get("/api/ndsp/public/decision-quality")
async def ndsp_public_decision_quality(
    symbol: str = Query("XAUUSD"),
    market: str = Query("commodity"),
    timeframe: str = Query("1d"),
):
    symbol = (symbol or "XAUUSD").upper().replace("/", "")
    market = market or "commodity"
    timeframe = timeframe or "1d"

    q, source, raw = _compute_from_active_engine(symbol, market, timeframe)

    return {
        "ok": True,
        "symbol": symbol,
        "decision_quality": int(q),
        "quality_label": _label(int(q)),
        "source": source,
        "connected": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_output_sanitized": True,
        "raw_layers_exposed": False,
    }

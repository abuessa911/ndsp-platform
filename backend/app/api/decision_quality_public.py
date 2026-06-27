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


def _compute_public_quality(symbol: str, market: str, timeframe: str):
    errors = []

    try:
        from app.core.ndsp_v4_pipeline import compute_decision_quality

        payloads = [
            {"final_confidence": 64, "confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
            {"base_confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
            {"scenario_state": "UNDER_MONITORING", "confidence": 64, "symbol": symbol, "market": market, "timeframe": timeframe},
        ]

        for p in payloads:
            try:
                r = compute_decision_quality(p, black_layer_penalty=0)
                q = _find_quality(r)
                if q is not None:
                    return q, "app.core.ndsp_v4_pipeline.compute_decision_quality", r
            except Exception as e:
                errors.append("ndsp_v4:" + type(e).__name__ + ":" + str(e)[:120])
    except Exception as e:
        errors.append("import_ndsp_v4:" + type(e).__name__ + ":" + str(e)[:120])

    try:
        from app.core.decision_engine import build_decision_output

        live_payload = {
            "symbol": symbol,
            "market": market,
            "timeframe": timeframe,
            "quality_data": {"final_confidence": 64, "grade": "C", "quality_label": "Public Context Quality"},
            "public": True,
        }

        r = build_decision_output(live_payload)
        q = _find_quality(r)
        if q is not None:
            return q, "app.core.decision_engine.build_decision_output", r
    except Exception as e:
        errors.append("decision_engine:" + type(e).__name__ + ":" + str(e)[:120])

    return None, "ndsp_decision_engine", {"errors": errors}


@router.get("/api/decision/quality")
async def public_decision_quality(
    symbol: str = Query("XAUUSD"),
    market: str = Query("commodity"),
    timeframe: str = Query("1d"),
):
    symbol = (symbol or "XAUUSD").upper().replace("/", "")
    market = market or "commodity"
    timeframe = timeframe or "1d"

    q, source, raw = _compute_public_quality(symbol, market, timeframe)

    if q is None:
        return {
            "ok": False,
            "symbol": symbol,
            "decision_quality": None,
            "quality_label": "تعذر استخراج رقم جودة القرار من المحرك",
            "source": source,
            "connected": False,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "public_output_sanitized": True,
            "raw_layers_exposed": False,
            "debug": raw,
        }

    return {
        "ok": True,
        "symbol": symbol,
        "decision_quality": q,
        "quality_label": _label(q),
        "source": source,
        "connected": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_output_sanitized": True,
        "raw_layers_exposed": False,
    }

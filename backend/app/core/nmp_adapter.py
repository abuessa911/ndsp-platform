"""
NDSP market_alignment Adapter v2 (Clean)

- Works with Binance candles
- No fake values
- No direction override
- Context only
"""

def evaluate_nmp_context(symbol, market, timing_model, phase, timing):
    try:
        market = market or {}
        candles = market.get("candles") or []
        price = market.get("price")

        # ❌ لا بيانات
        if not candles or len(candles) < 10 or price is None:
            return {
                "point": None,
                "zone": {"low": None, "high": None},
                "position": "UNKNOWN",
                "signal": "NO_SIGNAL",
                "status": "UNAVAILABLE",
                "source": "no_data",
                "public_note": "market_alignment unavailable due to insufficient data."
            }

        # آخر 100 شمعة
        candles = candles[-100:]

        best = None
        best_score = 0

        # نحدد أقوى شمعة زخم
        for i in range(1, len(candles)):
            c = candles[i]
            prev = candles[i-1]

            close = c.get("close")
            prev_close = prev.get("close")

            if close is None or prev_close is None:
                continue

            score = abs(close - prev_close)

            if score > best_score:
                best_score = score
                best = c

        if not best:
            return {
                "point": None,
                "zone": {"low": None, "high": None},
                "position": "UNKNOWN",
                "signal": "NO_SIGNAL",
                "status": "UNAVAILABLE",
                "source": "no_reference",
                "public_note": "No valid reference candle."
            }

        o = best["open"]
        c = best["close"]

        low = min(o, c)
        high = max(o, c)
        point = (low + high) / 2

        if price < low:
            pos = "BELOW"
        elif price > high:
            pos = "ABOVE"
        else:
            pos = "INSIDE"

        return {
            "point": point,
            "zone": {"low": low, "high": high},
            "position": pos,
            "signal": "CONTEXT_ONLY",
            "status": "ACTIVE",
            "source": "candle_nmp",
            "public_note": "market_alignment derived from strongest momentum candle."
        }

    except Exception:
        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "ERROR",
            "source": "error",
            "public_note": "market_alignment failed safely."
        }


def evaluate_nmp_tdl_quality(market_alignment: dict, timing_model: dict, timing: dict) -> dict:
    try:
        if not market_alignment or market_alignment.get("status") != "ACTIVE":
            return {
                "status": "NEUTRAL",
                "quality": "neutral",
                "score_effect": 0,
                "public_note": "market_alignment inactive"
            }

        pos = market_alignment.get("position")
        direction = (timing_model or {}).get("tdl_lm_direction") or "neutral"

        # دعم
        if direction == "bullish" and pos in ["INSIDE", "ABOVE"]:
            return {
                "status": "SUPPORTIVE",
                "quality": "high",
                "score_effect": +5,
                "public_note": "market_alignment supports bullish context"
            }

        if direction == "bearish" and pos in ["INSIDE", "BELOW"]:
            return {
                "status": "SUPPORTIVE",
                "quality": "high",
                "score_effect": +5,
                "public_note": "market_alignment supports bearish context"
            }

        # تعارض
        if direction == "bullish" and pos == "BELOW":
            return {
                "status": "CONFLICT",
                "quality": "low",
                "score_effect": -5,
                "public_note": "market_alignment conflicts with bullish context"
            }

        if direction == "bearish" and pos == "ABOVE":
            return {
                "status": "CONFLICT",
                "quality": "low",
                "score_effect": -5,
                "public_note": "market_alignment conflicts with bearish context"
            }

        return {
            "status": "CONTEXT_ONLY",
            "quality": "medium",
            "score_effect": 0,
            "public_note": "market_alignment neutral with timing_model"
        }

    except Exception:
        return {
            "status": "ERROR",
            "quality": "unknown",
            "score_effect": 0,
            "public_note": "market_alignment-timing_model evaluation failed"
        }


def evaluate_nmp_tdl_quality(market_alignment: dict, timing_model: dict, timing: dict) -> dict:
    try:
        if not market_alignment or market_alignment.get("status") != "ACTIVE":
            return {
                "status": "NEUTRAL",
                "quality": "neutral",
                "score_effect": 0,
                "public_note": "market_alignment inactive"
            }

        pos = market_alignment.get("position")
        direction = (timing_model or {}).get("tdl_lm_direction") or "neutral"

        # دعم
        if direction == "bullish" and pos in ["INSIDE", "ABOVE"]:
            return {
                "status": "SUPPORTIVE",
                "quality": "high",
                "score_effect": +5,
                "public_note": "market_alignment supports bullish context"
            }

        if direction == "bearish" and pos in ["INSIDE", "BELOW"]:
            return {
                "status": "SUPPORTIVE",
                "quality": "high",
                "score_effect": +5,
                "public_note": "market_alignment supports bearish context"
            }

        # تعارض
        if direction == "bullish" and pos == "BELOW":
            return {
                "status": "CONFLICT",
                "quality": "low",
                "score_effect": -5,
                "public_note": "market_alignment conflicts with bullish context"
            }

        if direction == "bearish" and pos == "ABOVE":
            return {
                "status": "CONFLICT",
                "quality": "low",
                "score_effect": -5,
                "public_note": "market_alignment conflicts with bearish context"
            }

        return {
            "status": "CONTEXT_ONLY",
            "quality": "medium",
            "score_effect": 0,
            "public_note": "market_alignment neutral with timing_model"
        }

    except Exception:
        return {
            "status": "ERROR",
            "quality": "unknown",
            "score_effect": 0,
            "public_note": "market_alignment-timing_model evaluation failed"
        }

def evaluate_nmp_tdl_quality(market_alignment: dict, timing_model: dict, timing: dict) -> dict:
    try:
        if not market_alignment or market_alignment.get("status") != "ACTIVE":
            return {
                "status": "NEUTRAL",
                "quality": "neutral",
                "score_effect": 0,
                "public_note": "market_alignment inactive"
            }

        pos = market_alignment.get("position")
        direction = (timing_model or {}).get("tdl_lm_direction", "neutral")

        if direction == "bullish":
            if pos in ["INSIDE", "ABOVE"]:
                return {"status": "SUPPORTIVE", "quality": "high", "score_effect": 5}
            if pos == "BELOW":
                return {"status": "CONFLICT", "quality": "low", "score_effect": -5}

        if direction == "bearish":
            if pos in ["INSIDE", "BELOW"]:
                return {"status": "SUPPORTIVE", "quality": "high", "score_effect": 5}
            if pos == "ABOVE":
                return {"status": "CONFLICT", "quality": "low", "score_effect": -5}

        return {
            "status": "CONTEXT_ONLY",
            "quality": "medium",
            "score_effect": 0,
            "public_note": "Neutral context"
        }

    except Exception:
        return {
            "status": "ERROR",
            "quality": "unknown",
            "score_effect": 0
        }

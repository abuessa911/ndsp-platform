########################################
# 💀 NDSP INTELLIGENCE ENGINE (market_alignment + SMC)
########################################

import numpy as np


########################################
# 🔹 1. DETECT PEAK (Indicator)
########################################
def detect_peak(values, trend):

    if len(values) < 5:
        return None

    if trend == "BULLISH":
        return int(np.argmax(values))

    elif trend == "BEARISH":
        return int(np.argmin(values))

    return None


########################################
# 🔹 2. BUILD market_alignment ZONE
########################################
def build_nmp_zone(candles, peak_index):

    if peak_index is None or peak_index >= len(candles):
        return None

    candle = candles[peak_index]

    open_price = candle["open"]
    close_price = candle["close"]

    low = min(open_price, close_price)
    high = max(open_price, close_price)

    return {
        "low": low,
        "high": high,
        "open": open_price
    }


########################################
# 🔹 3. LIQUIDITY DETECTION
########################################
def detect_liquidity(candles):

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    liquidity_zones = {
        "high_liquidity": max(highs),
        "low_liquidity": min(lows)
    }

    return liquidity_zones


########################################
# 🔹 4. PRICE BEHAVIOR
########################################
def evaluate_price_behavior(current_price, market_alignment, trend):

    if not market_alignment:
        return "NO_DATA"

    low = market_alignment["low"]
    high = market_alignment["high"]
    open_price = market_alignment["open"]

    # داخل المنطقة
    if low <= current_price <= high:
        return "TESTING_ZONE"

    # قريب من الافتتاح
    if abs(current_price - open_price) < 5:
        return "CONTINUATION_SIGNAL"

    # بعيد
    if trend == "BULLISH" and current_price < low:
        return "REVERSAL_SIGNAL"

    if trend == "BEARISH" and current_price > high:
        return "REVERSAL_SIGNAL"

    return "NO_SIGNAL"


########################################
# 🔹 5. MARKET STRUCTURE (SMC)
########################################
def detect_structure(candles):

    if len(candles) < 5:
        return "UNKNOWN"

    highs = [c["high"] for c in candles[-5:]]
    lows = [c["low"] for c in candles[-5:]]

    if highs[-1] > highs[-2] and lows[-1] > lows[-2]:
        return "UPTREND"

    if highs[-1] < highs[-2] and lows[-1] < lows[-2]:
        return "DOWNTREND"

    return "RANGE"


########################################
# 🔹 6. MAIN INTELLIGENCE ENGINE
########################################
def run_intelligence(symbol: str, market: dict, timing_model: dict):

    try:

        ########################################
        # 🔹 INPUTS
        ########################################
        candles = market.get("candles", [])
        current_price = market.get("price", 0)

        # تحويل trend من timing_model
        dominant = timing_model.get("dominant", "NEUTRAL")

        if dominant == "LM":
            trend = "BULLISH"
        elif dominant == "S":
            trend = "BEARISH"
        else:
            trend = "NEUTRAL"

        ########################################
        # 🔹 INDICATOR MOCK (مؤقت)
        ########################################
        indicator = [c["close"] for c in candles]

        ########################################
        # 🔹 PEAK
        ########################################
        peak_index = detect_peak(indicator, trend)

        ########################################
        # 🔹 market_alignment
        ########################################
        market_alignment = build_nmp_zone(candles, peak_index)

        ########################################
        # 🔹 LIQUIDITY
        ########################################
        liquidity = detect_liquidity(candles)

        ########################################
        # 🔹 STRUCTURE
        ########################################
        structure = detect_structure(candles)

        ########################################
        # 🔹 BEHAVIOR
        ########################################
        signal = evaluate_price_behavior(current_price, market_alignment, trend)

        ########################################
        # 🔹 FINAL OUTPUT
        ########################################
        return {
            "trend": trend,
            "structure": structure,
            "nmp_zone": market_alignment,
            "liquidity": liquidity,
            "signal": signal,
            "confidence": 0.6
        }

    except Exception as e:
        return {
            "error": str(e)
        }

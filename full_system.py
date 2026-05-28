import requests
from datetime import datetime

BINANCE = "https://api.binance.com"


# =========================
# 📊 DATA
# =========================
def get_klines(symbol, interval="1m", limit=100):
    url = f"{BINANCE}/api/v3/klines"
    res = requests.get(url, params={
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }, timeout=5)

    data = res.json()

    return [{
        "high": float(c[2]),
        "low": float(c[3]),
        "close": float(c[4])
    } for c in data]


# =========================
# 📈 TREND + MOMENTUM
# =========================
def analyze_market(symbol):

    c1 = get_klines(symbol, "1m", 100)
    c5 = get_klines(symbol, "5m", 100)

    def trend(c):
        closes = [x["close"] for x in c]
        sma5 = sum(closes[-5:]) / 5
        sma20 = sum(closes[-20:]) / 20

        if abs(sma5 - sma20) / sma20 < 0.001:
            return "range"
        return "up" if sma5 > sma20 else "down"

    def momentum(c):
        closes = [x["close"] for x in c]
        r3 = (closes[-1] - closes[-4]) / closes[-4]
        r8 = (closes[-1] - closes[-9]) / closes[-9]
        return (r3 * 0.6) + (r8 * 0.4)

    return {
        "price": c1[-1]["close"],
        "trend": {
            "1m": trend(c1),
            "5m": trend(c5)
        },
        "momentum": {
            "1m": momentum(c1),
            "5m": momentum(c5)
        }
    }


# =========================
# 🐋 ORDERFLOW
# =========================
def analyze_orderflow(symbol):
    url = f"{BINANCE}/api/v3/depth"
    data = requests.get(url, params={"symbol": symbol, "limit": 100}).json()

    bids = sum(float(x[1]) for x in data["bids"])
    asks = sum(float(x[1]) for x in data["asks"])

    total = bids + asks
    if total == 0:
        return {"state": "neutral"}

    buy = bids / total
    sell = asks / total

    spoofing = False
    if float(data["bids"][0][1]) > bids * 0.3:
        spoofing = True
    if float(data["asks"][0][1]) > asks * 0.3:
        spoofing = True

    if buy > 0.6:
        state = "strong_buying"
    elif sell > 0.6:
        state = "strong_selling"
    else:
        state = "balanced"

    return {
        "state": state,
        "buy_pressure": round(buy, 3),
        "sell_pressure": round(sell, 3),
        "spoofing": spoofing
    }


# =========================
# 💣 SWEEPS
# =========================
def detect_sweep(symbol):
    candles = get_klines(symbol, "1m", 50)

    last = candles[-1]
    highs = [c["high"] for c in candles[:-1]]
    lows = [c["low"] for c in candles[:-1]]

    if last["high"] > max(highs) and last["close"] < max(highs):
        return {"state": "sweep_up"}

    if last["low"] < min(lows) and last["close"] > min(lows):
        return {"state": "sweep_down"}

    return {"state": "none"}


# =========================
# 🎯 SNIPER
# =========================
def sniper(symbol):
    candles = get_klines(symbol, "1m", 100)
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    high = max(highs)
    low = min(lows)
    r = high - low
    price = candles[-1]["close"]

    return {
        "entry_long": low + r * 0.2,
        "entry_short": high - r * 0.2,
        "stop_long": low - r * 0.02,
        "stop_short": high + r * 0.02,
        "target_long": high,
        "target_short": low,
        "price": price
    }


# =========================
# 🧠 DECISION
# =========================
def decide(symbol):

    market = analyze_market(symbol)
    flow = analyze_orderflow(symbol)
    sweep = detect_sweep(symbol)
    sn = sniper(symbol)

    score = 0
    signal = "neutral"

    # trend
    if market["trend"]["5m"] == "up":
        score += 1
    elif market["trend"]["5m"] == "down":
        score -= 1

    # momentum
    if market["momentum"]["1m"] > 0:
        score += 1
    else:
        score -= 1

    # orderflow
    if flow["state"] == "strong_buying":
        score += 2
    elif flow["state"] == "strong_selling":
        score -= 2

    # spoofing
    if flow["spoofing"]:
        score -= 2

    # sweeps
    if sweep["state"] == "sweep_down":
        score += 2
    elif sweep["state"] == "sweep_up":
        score -= 2

    if score > 1:
        signal = "bullish"
    elif score < -1:
        signal = "bearish"

    return {
        "symbol": symbol,
        "time": datetime.utcnow().isoformat(),
        "signal": signal,
        "score": score,
        "market": market,
        "orderflow": flow,
        "sweep": sweep,
        "sniper": sn
    }


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    while True:
        result = decide("BTCUSDT")
        print(result)

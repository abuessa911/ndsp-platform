import requests

BINANCE = "https://api.binance.com"


def get_klines(symbol, interval="1m", limit=50):
    url = f"{BINANCE}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    res = requests.get(url, params=params, timeout=5)
    data = res.json()

    candles = []
    for c in data:
        candles.append({
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4])
        })

    return candles


def detect_sweep(candles):

    if len(candles) < 10:
        return {"state": "none"}

    last = candles[-1]

    highs = [c["high"] for c in candles[:-1]]
    lows = [c["low"] for c in candles[:-1]]

    max_high = max(highs)
    min_low = min(lows)

    # 💣 sweep up
    if last["high"] > max_high and last["close"] < max_high:
        return {
            "state": "sweep_up",
            "direction": "bearish_reversal"
        }

    # 💣 sweep down
    if last["low"] < min_low and last["close"] > min_low:
        return {
            "state": "sweep_down",
            "direction": "bullish_reversal"
        }

    # breakout
    if last["close"] > max_high:
        return {"state": "breakout_up"}

    if last["close"] < min_low:
        return {"state": "breakout_down"}

    return {"state": "none"}


def analyze_sweeps(symbol):
    candles = get_klines(symbol)
    return detect_sweep(candles)

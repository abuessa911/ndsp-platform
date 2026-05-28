import json
import urllib.request

BASE = "https://api.binance.com/api/v3"

def _fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read().decode())
    except:
        return None

def _normalize(symbol):
    if symbol.endswith("USD") and not symbol.endswith("USDT"):
        return symbol.replace("USD", "USDT")
    return symbol

def get_binance_market(symbol):
    s = _normalize(symbol)

    ticker = _fetch(f"{BASE}/ticker/price?symbol={s}")
    if not ticker:
        return None

    try:
        price = float(ticker["price"])
    except:
        return None

    klines = _fetch(f"{BASE}/klines?symbol={s}&interval=1m&limit=50")

    candles = []
    if klines:
        for k in klines:
            candles.append({
                "time": k[0],
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
                "bid": float(k[4]),
                "ask": float(k[4]),
                "spread": 0.0,
                "nmp_low": 0.0,
                "nmp_high": 0.0,
            })

    return {
        "price": price,
        "candles": candles,
        "last_candle": candles[-1] if candles else None,
        "source": "binance",
        "source_status": "OK"
    }

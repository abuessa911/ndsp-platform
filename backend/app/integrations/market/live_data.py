import requests
import time

SYMBOLS = ["BTCUSDT", "ETHUSDT"]

LIVE_DATA = {}

def fetch_klines(symbol, interval="5m", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    r = requests.get(url, params=params, timeout=5)
    data = r.json()

    candles = []
    closes = []

    for k in data:
        candle = {
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5])
        }
        candles.append(candle)
        closes.append(float(k[4]))

    return candles, closes


def update_loop():
    global LIVE_DATA

    while True:
        try:
            for sym in SYMBOLS:
                candles, closes = fetch_klines(sym)

                LIVE_DATA[sym] = {
                    "open": candles[-1]["open"],
                    "closes": closes,
                    "history": candles
                }

        except Exception as e:
            print("LIVE ERROR:", e)

        time.sleep(5)

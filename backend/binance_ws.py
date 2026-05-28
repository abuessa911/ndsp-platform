import json
import time
import requests
import websocket

API_HTTP = "http://127.0.0.1:9001/md/ws"

# =========================
# أشهر العملات (Top Market)
# =========================
SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "bnbusdt",
    "solusdt",
    "xrpusdt",
    "adausdt",
    "dogeusdt",
    "avaxusdt",
    "linkusdt",
    "dotusdt",
    "maticusdt",
    "ltcusdt"
]

# =========================
# كل الفواصل الزمنية
# =========================
INTERVALS = [
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
    "1d",
    "3d",
    "1w",
    "1M"
]

# =========================
# بناء جميع الـ streams
# =========================
STREAMS = [
    f"{symbol}@kline_{interval}"
    for symbol in SYMBOLS
    for interval in INTERVALS
]

print(f"🔥 Total Streams: {len(STREAMS)}")

BINANCE_WS_URL = "wss://stream.binance.com:9443/stream?streams=" + "/".join(STREAMS)

# =========================
# WebSocket Callbacks
# =========================
def on_open(ws):
    print("🚀 Connected to Binance")
    print("Streams:", len(STREAMS))

def on_message(ws, message):
    try:
        raw = json.loads(message)

        if "data" not in raw:
            return

        event = raw["data"]
        if "k" not in event:
            return

        k = event["k"]

        payload = {
            "k": {
                "s": k["s"],
                "i": k["i"],   # interval مهم جدًا
                "o": k["o"],
                "h": k["h"],
                "l": k["l"],
                "c": k["c"],
                "v": k["v"],
                "t": k["t"],
                "T": k["T"],
                "x": k["x"]
            }
        }

        requests.post(API_HTTP, json=payload, timeout=2)

    except Exception as e:
        print("ERROR:", e)

def on_error(ws, error):
    print("WS ERROR:", error)

def on_close(ws, code, msg):
    print("WS CLOSED:", code, msg)
    time.sleep(2)

# =========================
# Runner
# =========================
def run():
    while True:
        try:
            ws = websocket.WebSocketApp(
                BINANCE_WS_URL,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever(ping_interval=20, ping_timeout=10)
        except Exception as e:
            print("RECONNECT:", e)
            time.sleep(3)

if __name__ == "__main__":
    run()

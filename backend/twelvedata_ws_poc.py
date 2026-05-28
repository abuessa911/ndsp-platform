#!/usr/bin/env python3
# twelvedata_ws_poc.py
# PoC: Subscribe to TwelveData WebSocket quotes and print incoming messages (simple).

import os
import time
import json
import threading
from websocket import WebSocketApp

API_KEY = os.environ.get("TWELVEDATA_KEY", "").strip()
SYMBOLS_ENV = os.environ.get("TD_SYMBOLS", "EUR/USD")
SYMBOLS = [s.strip() for s in SYMBOLS_ENV.split(",") if s.strip()]

if not API_KEY:
    raise SystemExit("ERROR: TWELVEDATA_KEY not set. export TWELVEDATA_KEY=\"your_key\" before running.")

WS_URL = f"wss://ws.twelvedata.com/v1/quotes/price?apikey={API_KEY}"\n\nFALLBACK_MAP = {
    "USD/JPY": ["USDJPY","USDJPY:FOREX","USDJPY.FX"],
    "EUR/USD": ["EURUSD","EURUSD:FOREX"],
    "BTC/USD": ["BTCUSD","BTC/USD:Coinbase Pro"]
}


def pretty_print(msg):
    try:
        obj = json.loads(msg)
        print(json.dumps(obj, ensure_ascii=False))
    except Exception:
        print("RAW:", msg)

def on_message(ws, message):
    pretty_print(message)

def on_open(ws):
    print("Connected to TwelveData WebSocket.")
    sub = {"action":"subscribe","params":{"symbols":",".join(SYMBOLS)}}
    print("Subscribing:", sub)
    ws.send(json.dumps(sub))

    # heartbeat every 10s to keep connection alive
    def heartbeat():
        while True:
            time.sleep(10)
            try:
                ws.send(json.dumps({"action":"heartbeat"}))
            except Exception:
                break
    threading.Thread(target=heartbeat, daemon=True).start()

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed:", close_status_code, close_msg)

def run_forever():
    while True:
        try:
            ws = WebSocketApp(WS_URL,
                              on_open=lambda ws: on_open(ws),
                              on_message=lambda ws, msg: on_message(ws, msg),
                              on_error=lambda ws, err: on_error(ws, err),
                              on_close=lambda ws, code, reason: on_close(ws, code, reason))
            ws.run_forever()
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")
            return
        except Exception as e:
            print("Connection failed, retrying in 3s. Error:", e)
            time.sleep(3)

if __name__ == "__main__":
    print("TwelveData WS PoC starting. Symbols:", SYMBOLS)
    run_forever()

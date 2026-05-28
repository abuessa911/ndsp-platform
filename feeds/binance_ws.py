#!/usr/bin/env python3
"""
binance_ws.py
- Connects to Binance combined websocket for kline/trade streams
- Posts incoming normalized messages to local backend: POST {BACKEND_API}/md/ws
Env:
  BINANCE_SYMBOLS = "BTCUSDT,ETHUSDT"    # comma separated (upper or lower)
  BINANCE_KLINE_INTERVAL = "1m"          # e.g. 1m, 5m, 1h
  BACKEND_API (optional) - full http base url (default http://127.0.0.1:9001)
"""
import os, json, time, urllib.parse
from websocket import create_connection, WebSocketConnectionClosedException
import requests

SYMS = os.getenv("BINANCE_SYMBOLS", "BTCUSDT,ETHUSDT").strip()
INTERVAL = os.getenv("BINANCE_KLINE_INTERVAL", "1m").strip()
BACKEND_API = os.getenv("BACKEND_API", "http://127.0.0.1:9001")
RECONNECT_DELAY = 5

def build_stream_url(symbols, interval):
    # lowercase names, kline stream per symbol
    parts = []
    for s in symbols.split(","):
        s2 = s.strip().lower()
        if not s2:
            continue
        parts.append(f"{s2}@kline_{interval}")
    stream_query = "/".join(parts)
    url = f"wss://stream.binance.com:9443/stream?streams={stream_query}"
    return url

def post_to_backend(payload):
    try:
        requests.post(f"{BACKEND_API}/md/ws", json=payload, timeout=3)
    except Exception as e:
        # backend may be down; just print (systemd will restart service on failure policy)
        print("POST ERROR:", e)

def run():
    url = build_stream_url(SYMS, INTERVAL)
    print("CONNECT", url)
    while True:
        try:
            ws = create_connection(url, timeout=30)
            print("connected to binance")
            while True:
                raw = ws.recv()
                if not raw:
                    continue
                try:
                    obj = json.loads(raw)
                except Exception:
                    continue
                # wrapper: {"stream":"...","data":{...}} for combined stream
                if "data" in obj:
                    payload = obj["data"]
                else:
                    payload = obj
                # attach a source marker
                payload["_src"] = "binance_ws"
                # forward to backend
                post_to_backend(payload)
        except WebSocketConnectionClosedException as e:
            print("WS closed, reconnecting in", RECONNECT_DELAY, "s:", e)
            time.sleep(RECONNECT_DELAY)
        except Exception as e:
            print("ERROR:", e)
            time.sleep(RECONNECT_DELAY)

if __name__ == "__main__":
    run()

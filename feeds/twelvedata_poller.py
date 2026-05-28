#!/usr/bin/env python3
"""
twelvedata_poller.py
- Polls TwelveData REST /time_series for a list of symbols at interval seconds
- Symbols example: EUR/USD , XAU/USD , WTI
Env:
  TWELVEDATA_KEY - required
  TD_SYMBOLS = "EUR/USD,XAU/USD,WTI"
  POLL_INTERVAL = 10   # seconds
  BACKEND_API (optional)
"""
import os, time, requests, json, urllib.parse

APIKEY = os.getenv("TWELVEDATA_KEY", "")
SYMS = os.getenv("TD_SYMBOLS", "EUR/USD").strip()
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))
BACKEND_API = os.getenv("BACKEND_API", "http://127.0.0.1:9001")

if not APIKEY:
    raise SystemExit("TWELVEDATA_KEY not set in environment")

TD_BASE = "https://api.twelvedata.com/time_series"

def fetch_symbol(sym):
    # convert EUR/USD -> EUR/USD (TwelveData accepts "/" format)
    params = {
        "symbol": sym,
        "interval": "1min",
        "outputsize": 1,
        "apikey": APIKEY
    }
    r = requests.get(TD_BASE, params=params, timeout=10)
    return r.json()

def post_to_backend(payload):
    try:
        requests.post(f"{BACKEND_API}/md/ws", json=payload, timeout=3)
    except Exception as e:
        print("POST ERROR:", e)

def main():
    symbols = [s.strip() for s in SYMS.split(",") if s.strip()]
    print("Polling TwelveData for:", symbols)
    while True:
        ts = int(time.time())
        for s in symbols:
            try:
                data = fetch_symbol(s)
                payload = {"symbol": s, "data": data, "_src": "twelvedata_poller", "ts": ts}
                post_to_backend(payload)
            except Exception as e:
                print("fetch error", s, e)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

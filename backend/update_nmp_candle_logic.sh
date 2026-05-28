#!/usr/bin/env bash
set -Eeuo pipefail

FILE="app/core/nmp_adapter.py"
cp "$FILE" "$FILE.bak.$(date +%s)"

python3 - <<'PY'
from pathlib import Path

p = Path("app/core/nmp_adapter.py")
s = p.read_text()

# ✨ استبدال evaluate_nmp_context بالكامل
new_func = '''
def evaluate_nmp_context(symbol: str, market: dict, tdl: dict, phase: dict, timing: dict) -> dict:
    try:
        market = market or {}
        candles = market.get("candles") or []
        price = market.get("price")

        if not candles or len(candles) < 10 or price is None:
            return {
                "point": None,
                "zone": {"low": None, "high": None},
                "position": "UNKNOWN",
                "signal": "NO_SIGNAL",
                "status": "UNAVAILABLE",
                "source": "no_data",
                "public_note": "NMP unavailable due to insufficient candles or price."
            }

        # نأخذ آخر 100 شمعة
        candles = candles[-100:]

        best = None
        best_score = 0

        for i in range(1, len(candles)):
            c = candles[i]
            prev = candles[i-1]

            close = c.get("close")
            open_ = c.get("open")
            prev_close = prev.get("close")

            if close is None or open_ is None or prev_close is None:
                continue

            # momentum بسيط
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
                "source": "no_reference_candle",
                "public_note": "No valid reference candle found."
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
            "source": "candle_fallback",
            "public_note": "NMP derived from strongest momentum candle."
        }

    except Exception:
        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "ERROR",
            "source": "error",
            "public_note": "NMP failed safely."
        }
'''

import re

s = re.sub(
    r"def evaluate_nmp_context\(.*?return.*?\}",
    new_func,
    s,
    flags=re.S
)

p.write_text(s)
PY

echo "== compile =="
python3 -m py_compile app/core/nmp_adapter.py

echo "== restart =="
sudo systemctl restart ndip-api-new.service
sleep 2

echo "== test BTCUSDT =="
curl -s http://127.0.0.1:9000/decision?symbol=BTCUSDT | python3 -m json.tool | grep -A10 '"nmp"'

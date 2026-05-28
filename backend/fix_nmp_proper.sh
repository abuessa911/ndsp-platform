#!/usr/bin/env bash
set -Eeuo pipefail

FILE="app/core/governed_pipeline.py"
cp "$FILE" "$FILE.bak.$(date +%s)"

python3 - <<'PY'
from pathlib import Path
import re

p = Path("app/core/governed_pipeline.py")
s = p.read_text()

# =========================================
# 1) Replace _run_nmp_safe بالكامل
# =========================================
new_func = '''
def _run_nmp_safe(symbol, market, phase, timing):
    try:
        price = market.get("price")
        last = market.get("last_candle") or {}

        low = last.get("nmp_low")
        high = last.get("nmp_high")

        if price is None:
            return {
                "point": None,
                "zone": {"low": None, "high": None},
                "position": "UNKNOWN",
                "signal": "NO_SIGNAL",
                "status": "UNAVAILABLE",
                "source": "no_price",
                "public_note": "NMP unavailable due to missing market price."
            }

        if low and high and low > 0 and high > 0:
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
                "source": "mt4_precomputed",
                "public_note": "Using MT4 provided NMP zone."
            }

        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "UNAVAILABLE",
            "source": "no_data",
            "public_note": "No NMP zone available."
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

# استبدال كامل للدالة
s = re.sub(
    r"def _run_nmp_safe\(.*?\n\s*return.*?\n\s*\}",
    new_func,
    s,
    flags=re.S
)

# =========================================
# 2) ربط nmp الحقيقي في output
# =========================================
s = s.replace(
    '"nmp": {\n            "point": None,',
    '"nmp": nmp,'
)

p.write_text(s)
PY

echo "== compile =="
python3 -m py_compile app/core/governed_pipeline.py

echo "== test =="
python3 - <<'PY'
from app.core.governed_pipeline import run_governed
r = run_governed("BTCUSDT")
print("NMP:", r["nmp"])
PY

echo "== restart =="
sudo systemctl restart ndip-api-new.service
sleep 2

echo "== API =="
curl -s http://127.0.0.1:9000/decision?symbol=BTCUSDT | python3 -m json.tool | grep -A10 '"nmp"'

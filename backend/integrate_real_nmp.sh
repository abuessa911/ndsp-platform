#!/usr/bin/env bash
set -Eeuo pipefail

PIPE="app/core/governed_pipeline.py"
cp "$PIPE" "$PIPE.bak.$(date +%s)"

python3 - <<'PY'
from pathlib import Path

p = Path("app/core/governed_pipeline.py")
s = p.read_text()

# 🔥 حذف placeholder القديم
s = s.replace("_run_nmp_safe(symbol, market, phase, timing)", "None")

# 🔥 إضافة NMP الحقيقي
if "_run_nmp_real" not in s:
    adapter = '''

def _run_nmp_real(market: dict, tdl: dict):
    try:
        price = market.get("price")
        last = market.get("last_candle") or {}

        # ✅ 1) MT4 precomputed
        low = last.get("nmp_low")
        high = last.get("nmp_high")

        if low and high:
            point = (low + high) / 2

            return {
                "point": point,
                "zone": {"low": low, "high": high},
                "position": "INSIDE" if low <= price <= high else "OUTSIDE",
                "signal": "CONTEXT_ONLY",
                "status": "MT4_PRECOMPUTED",
                "source": "mt4",
                "public_note": "Using MT4 NMP zone"
            }

        # ❌ لا يوجد بيانات
        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "UNAVAILABLE",
            "source": "none",
            "public_note": "No NMP data available"
        }

    except Exception:
        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "ERROR",
            "source": "error",
            "public_note": "NMP failed safely"
        }
'''
    s = s.replace("def _run_black_layer_safe", adapter + "\ndef _run_black_layer_safe")

# 🔥 ربط داخل pipeline
s = s.replace(
    "nmp = _run_nmp_safe(",
    "nmp = _run_nmp_real(market, tdl)"
)

# 🔥 إزالة override القديم اللي يرجع null
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

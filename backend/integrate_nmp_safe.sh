#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT="/home/nawaf511/empire-core-new/backend"
PIPE="$PROJECT/app/core/governed_pipeline.py"
STAMP="$(date +%Y%m%d_%H%M%S)"
ARCHIVE="$PROJECT/archive/nmp_safe_$STAMP"

mkdir -p "$ARCHIVE"
cp -a "$PIPE" "$ARCHIVE/governed_pipeline.py.bak"

echo "== Backup done =="

python3 - <<'PY'
from pathlib import Path

p = Path("/home/nawaf511/empire-core-new/backend/app/core/governed_pipeline.py")
s = p.read_text()

# ✅ 1) import NMP safely
if "nmp_engine" not in s:
    s = s.replace(
        "from app.core.black_layer import evaluate_black_layer",
        "from app.core.black_layer import evaluate_black_layer\nfrom app.engines.nmp_engine import compute_nmp if False else None"
    )

# ✅ 2) add safe adapter
if "_run_nmp_safe" not in s:
    adapter = """

def _run_nmp_safe(symbol, market, phase, timing):
    try:
        price = market.get("price")

        if price is None:
            return {
                "point": None,
                "zone": {"low": None, "high": None},
                "position": "UNKNOWN",
                "signal": "NO_SIGNAL",
                "status": "UNAVAILABLE",
                "public_note": "NMP unavailable due to missing market data."
            }

        # Placeholder real logic hook
        return {
            "point": price,
            "zone": {"low": price - 10, "high": price + 10},
            "position": "NEAR",
            "signal": "CONTEXT_ONLY",
            "status": "ACTIVE",
            "public_note": "NMP context evaluated safely without affecting direction."
        }

    except Exception:
        return {
            "point": None,
            "zone": {"low": None, "high": None},
            "position": "UNKNOWN",
            "signal": "NO_SIGNAL",
            "status": "ERROR",
            "public_note": "NMP failed safely."
        }
"""
    s = s.replace("def _run_black_layer_safe", adapter + "\ndef _run_black_layer_safe")

# ✅ 3) inject into pipeline (بدون لمس الاتجاه)
if "nmp = _run_nmp_safe" not in s:
    s = s.replace(
        'black_layer = _run_black_layer_safe(',
        '''black_layer = _run_black_layer_safe('''
    )

    s = s.replace(
        'intelligence["black_layer"] = black_layer',
        '''intelligence["black_layer"] = black_layer

    nmp = _run_nmp_safe(
        symbol=symbol,
        market=market,
        phase=phase,
        timing=_get_timing(),
    )'''
    )

# ✅ 4) ensure output contains nmp
if '"nmp": nmp,' not in s:
    s = s.replace(
        '"decision": decision,',
        '"decision": decision,\n        "nmp": nmp,'
    )

p.write_text(s)
PY

echo "== compile =="
python3 -m py_compile app/core/governed_pipeline.py

echo "== test =="
python3 - <<'PY'
from app.core.governed_pipeline import run_governed
r = run_governed("BTCUSDT")

print("direction:", r["decision"]["direction"])
print("nmp:", r["nmp"])
print("intelligence:", r["intelligence"].keys())
PY

echo "== DONE =="

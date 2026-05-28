#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUNTIME_DIR = BASE / "runtime"
LOGS_DIR = BASE / "logs"
OUT_FILE = RUNTIME_DIR / "tdl_ml_direction.env"
JSON_OUT_FILE = RUNTIME_DIR / "tdl_ml_direction.json"

sys.path.insert(0, str(BASE))

try:
    from app.core.tdl_data_provider import build_tdl_data
    from app.engines.tdl_crypto_engine import calculate_crypto_tdl
except Exception as e:
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text("TDL_ML_DIRECTION=NEUTRAL\nTDL_LM_DIRECTION=neutral\nTDL_S_DIRECTION=neutral\nTDL_ERROR=import_failed\n")
    print(f"ERROR: import_failed: {e}")
    sys.exit(1)


def normalize_direction(value: str) -> str:
    value = str(value or "").strip().lower()
    if value == "bullish":
        return "BULLISH"
    if value == "bearish":
        return "BEARISH"
    return "NEUTRAL"


def main() -> int:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "ETHUSDT"

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    # نحاول بناء بيانات TDL من مزود البيانات الحالي
    try:
        tdl_data = build_tdl_data(symbol=symbol, market={}, manual={})
    except Exception:
        tdl_data = {"symbol": symbol, "market": {}}

    # ندخل manual_lm/manual_s إن كانت موجودة من manual weekly
    market = {}
    manual_lm = (
        tdl_data.get("manual_lm", {}).get("tdl_lm_direction")
        if isinstance(tdl_data.get("manual_lm"), dict)
        else None
    )
    manual_s = (
        tdl_data.get("manual_s", {}).get("tdl_s_direction")
        if isinstance(tdl_data.get("manual_s"), dict)
        else None
    )

    if manual_lm:
        market["tdl_lm_direction"] = manual_lm
    if manual_s:
        market["tdl_s_direction"] = manual_s

    engine_input = {
        "symbol": symbol,
        "market": market,
    }

    result = calculate_crypto_tdl(engine_input)

    lm = str(result.get("tdl_lm_direction", "neutral")).lower()
    s = str(result.get("tdl_s_direction", "neutral")).lower()

    # اتجاه L&M هو الأساس، لأنه طويل/متوسط الأمد
    final_direction = normalize_direction(lm)

    payload = {
        "symbol": symbol,
        "tdl_ml_direction": final_direction,
        "tdl_lm_direction": lm,
        "tdl_s_direction": s,
        "golden_signal": bool(result.get("golden_signal")),
        "golden_name": result.get("golden_name"),
        "dominant": result.get("dominant"),
        "raw": result,
    }

    JSON_OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    OUT_FILE.write_text(
        "\n".join(
            [
                f"SYMBOL={symbol}",
                f"TDL_ML_DIRECTION={final_direction}",
                f"TDL_LM_DIRECTION={lm}",
                f"TDL_S_DIRECTION={s}",
                f"TDL_GOLDEN_SIGNAL={str(bool(result.get('golden_signal'))).upper()}",
                f"TDL_GOLDEN_NAME={result.get('golden_name') or ''}",
                f"TDL_DOMINANT={result.get('dominant') or ''}",
                "",
            ]
        )
    )

    print(f"TDL_ML_DIRECTION={final_direction}")
    print(f"OUT_FILE={OUT_FILE}")
    print(f"JSON_OUT_FILE={JSON_OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

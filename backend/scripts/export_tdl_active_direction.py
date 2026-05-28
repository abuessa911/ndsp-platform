#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUNTIME_DIR = BASE / "runtime"
CONFIG_DIR = BASE / "config"

TDL_ENV = RUNTIME_DIR / "tdl_ml_direction.env"
TDL_JSON = RUNTIME_DIR / "tdl_ml_direction.json"
POLICY_FILE = CONFIG_DIR / "tdl_control_policy.json"

OUT_ENV = RUNTIME_DIR / "tdl_active_direction.env"
OUT_JSON = RUNTIME_DIR / "tdl_active_direction.json"


def read_env(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def norm_dir(v: str) -> str:
    v = str(v or "").strip().lower()
    if v == "bullish":
        return "BULLISH"
    if v == "bearish":
        return "BEARISH"
    if v == "BULLISH":
        return "BULLISH"
    if v == "BEARISH":
        return "BEARISH"
    return "NEUTRAL"


def direction_to_action(direction: str) -> str:
    direction = norm_dir(direction)
    if direction == "BULLISH":
        return "LONG"
    if direction == "BEARISH":
        return "SHORT"
    return "WAIT"


def load_policy() -> dict:
    default = {
        "mode": "control_day",
        "allow_entries_all_week": True,
        "default_control": "S",
        "golden_boost": True,
        "days": {
            "monday": "S",
            "tuesday": "S",
            "wednesday": "S",
            "thursday": "LM",
            "friday": "LM",
            "saturday": "S",
            "sunday": "S",
        },
    }
    if not POLICY_FILE.exists():
        return default
    try:
        data = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            default.update(data)
    except Exception:
        pass
    return default


def main() -> int:
    symbol = sys.argv[1] if len(sys.argv) > 1 else ""

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

    env = read_env(TDL_ENV)

    tdl_json_payload = {}
    if TDL_JSON.exists():
        try:
            tdl_json_payload = json.loads(TDL_JSON.read_text(encoding="utf-8"))
        except Exception:
            tdl_json_payload = {}

    policy = load_policy()

    now = datetime.now()
    day_name = now.strftime("%A").lower()

    days = policy.get("days") if isinstance(policy.get("days"), dict) else {}
    control = str(days.get(day_name) or policy.get("default_control") or "S").upper().strip()

    lm_direction = norm_dir(
        env.get("TDL_LM_DIRECTION")
        or tdl_json_payload.get("tdl_lm_direction")
        or env.get("TDL_ML_DIRECTION")
    )

    s_direction = norm_dir(
        env.get("TDL_S_DIRECTION")
        or tdl_json_payload.get("tdl_s_direction")
    )

    golden_signal = str(env.get("TDL_GOLDEN_SIGNAL", "")).upper() == "TRUE"
    golden_name = env.get("TDL_GOLDEN_NAME") or tdl_json_payload.get("golden_name") or ""
    dominant = env.get("TDL_DOMINANT") or tdl_json_payload.get("dominant") or ""

    if control in ("LM", "L&M", "ML"):
        active_layer = "LM"
        active_direction = lm_direction
        entry_scope = "WEEKLY_CONTROL"
    else:
        active_layer = "S"
        active_direction = s_direction
        entry_scope = "PARTIAL_CONTROL"

    action = direction_to_action(active_direction)

    if not bool(policy.get("allow_entries_all_week", True)):
        action = "WAIT"

    confidence_tag = "GOLDEN" if golden_signal else "CONTROL_DAY"

    payload = {
        "symbol": symbol or env.get("SYMBOL") or tdl_json_payload.get("symbol") or "",
        "day": day_name,
        "active_layer": active_layer,
        "active_direction": active_direction,
        "active_action": action,
        "entry_scope": entry_scope,
        "lm_direction": lm_direction,
        "s_direction": s_direction,
        "golden_signal": golden_signal,
        "golden_name": golden_name,
        "dominant": dominant,
        "confidence_tag": confidence_tag,
        "policy": policy,
    }

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    OUT_ENV.write_text(
        "\n".join(
            [
                f"SYMBOL={payload['symbol']}",
                f"TDL_CONTROL_DAY={day_name}",
                f"TDL_ACTIVE_LAYER={active_layer}",
                f"TDL_ACTIVE_DIRECTION={active_direction}",
                f"TDL_ACTIVE_ACTION={action}",
                f"TDL_ENTRY_SCOPE={entry_scope}",
                f"TDL_LM_DIRECTION={lm_direction}",
                f"TDL_S_DIRECTION={s_direction}",
                f"TDL_GOLDEN_SIGNAL={str(golden_signal).upper()}",
                f"TDL_GOLDEN_NAME={golden_name}",
                f"TDL_DOMINANT={dominant}",
                f"TDL_CONFIDENCE_TAG={confidence_tag}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"TDL_CONTROL_DAY={day_name}")
    print(f"TDL_ACTIVE_LAYER={active_layer}")
    print(f"TDL_ACTIVE_DIRECTION={active_direction}")
    print(f"TDL_ACTIVE_ACTION={action}")
    print(f"OUT_ENV={OUT_ENV}")
    print(f"OUT_JSON={OUT_JSON}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

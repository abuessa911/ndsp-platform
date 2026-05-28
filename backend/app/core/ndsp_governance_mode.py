from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import os
from typing import Any, Dict


GOVERNANCE_MODE_FILE = Path(
    os.getenv(
        "NDSP_GOVERNANCE_MODE_FILE",
        "/home/nawaf511/empire-core-new/backend/runtime/ndsp_governance_mode.json",
    )
)


DEFAULT_GOVERNANCE_MODE: Dict[str, Any] = {
    "system": "NDSP",
    "governance_version": "6.1.0",
    "mode": "DECISION_ACTIVE",
    "execution_policy": "EXECUTION_SANITIZED",
    "decision_active": True,
    "execution_sanitized": True,
    "all_layers_participate": True,
    "no_layer_disabled": True,
    "tdl_direction_authority": True,
    "timing_layer_enabled": True,
    "direct_trade_execution": False,
    "public_buy_sell_commands": False,
    "public_tp_sl": False,
    "raw_logic_public": False,
    "updated_at": None,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_governance_mode_file() -> Dict[str, Any]:
    GOVERNANCE_MODE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not GOVERNANCE_MODE_FILE.exists():
        payload = dict(DEFAULT_GOVERNANCE_MODE)
        payload["updated_at"] = _utc_now()
        GOVERNANCE_MODE_FILE.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return payload
    return load_governance_mode()


def load_governance_mode() -> Dict[str, Any]:
    try:
        data = json.loads(GOVERNANCE_MODE_FILE.read_text(encoding="utf-8"))
        merged = dict(DEFAULT_GOVERNANCE_MODE)
        merged.update(data if isinstance(data, dict) else {})
        if not merged.get("updated_at"):
            merged["updated_at"] = _utc_now()
        return merged
    except Exception:
        payload = dict(DEFAULT_GOVERNANCE_MODE)
        payload["updated_at"] = _utc_now()
        return payload


def save_governance_mode(updates: Dict[str, Any]) -> Dict[str, Any]:
    current = load_governance_mode()
    allowed = {
        "mode",
        "execution_policy",
        "decision_active",
        "execution_sanitized",
        "all_layers_participate",
        "no_layer_disabled",
        "tdl_direction_authority",
        "timing_layer_enabled",
        "direct_trade_execution",
        "public_buy_sell_commands",
        "public_tp_sl",
        "raw_logic_public",
    }

    for key, value in updates.items():
        if key in allowed:
            current[key] = value

    current["system"] = "NDSP"
    current["governance_version"] = str(current.get("governance_version") or "6.1.0")
    current["mode"] = "DECISION_ACTIVE"
    current["execution_policy"] = "EXECUTION_SANITIZED"
    current["decision_active"] = True
    current["execution_sanitized"] = True
    current["all_layers_participate"] = True
    current["no_layer_disabled"] = True
    current["tdl_direction_authority"] = True
    current["direct_trade_execution"] = False
    current["public_buy_sell_commands"] = False
    current["public_tp_sl"] = False
    current["raw_logic_public"] = False
    current["updated_at"] = _utc_now()

    GOVERNANCE_MODE_FILE.parent.mkdir(parents=True, exist_ok=True)
    GOVERNANCE_MODE_FILE.write_text(
        json.dumps(current, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return current


def set_timing_layer_enabled(enabled: bool) -> Dict[str, Any]:
    current = load_governance_mode()
    current["timing_layer_enabled"] = bool(enabled)
    return save_governance_mode(current)


def governance_mode_public() -> Dict[str, Any]:
    current = ensure_governance_mode_file()
    return {
        "system": "NDSP",
        "governance_version": current.get("governance_version", "6.1.0"),
        "mode": "DECISION_ACTIVE",
        "execution_policy": "EXECUTION_SANITIZED",
        "decision_active": True,
        "execution_sanitized": True,
        "all_layers_participate": True,
        "no_layer_disabled": True,
        "tdl_direction_authority": True,
        "timing_layer_enabled": bool(current.get("timing_layer_enabled", True)),
        "direct_trade_execution": False,
        "public_buy_sell_commands": False,
        "public_tp_sl": False,
        "raw_logic_public": False,
        "updated_at": current.get("updated_at"),
    }

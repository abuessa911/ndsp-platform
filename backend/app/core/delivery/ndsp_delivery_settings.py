from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


CONFIG_PATH = Path(os.getenv("NDSP_DELIVERY_SETTINGS_FILE", "/home/nawaf511/empire-core-new/backend/runtime/delivery_settings.json"))

DEFAULT_SETTINGS: Dict[str, Any] = {
    "telegram": {"enabled": False},
    "email": {"enabled": False},
    "push": {"enabled": False},
}


def _ensure_dir() -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _read_json() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        return DEFAULT_SETTINGS.copy()

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return DEFAULT_SETTINGS.copy()
        return data
    except Exception:
        return DEFAULT_SETTINGS.copy()


def read_delivery_settings() -> Dict[str, Any]:
    data = _read_json()
    normalized = DEFAULT_SETTINGS.copy()

    for channel in ("telegram", "email", "push"):
        value = data.get(channel) or {}
        normalized[channel] = {
            "enabled": bool(value.get("enabled", False))
        }

    return normalized


def write_delivery_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    current = read_delivery_settings()

    for channel in ("telegram", "email", "push"):
        if channel in settings:
            value = settings.get(channel) or {}
            current[channel] = {
                "enabled": bool(value.get("enabled", False))
            }

    _ensure_dir()
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(current, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(CONFIG_PATH)

    try:
        os.chmod(CONFIG_PATH, 0o600)
    except Exception:
        pass

    return current


def get_channel_enabled(channel: str, env_name: str) -> bool:
    settings = read_delivery_settings()
    if channel in settings:
        return bool(settings[channel].get("enabled", False))

    return os.getenv(env_name, "").strip().lower() in {"1", "true", "yes", "on", "enabled"}


def public_settings_status() -> Dict[str, Any]:
    settings = read_delivery_settings()
    return {
        "settings_file": str(CONFIG_PATH),
        "channels": settings,
        "secrets_exposed": False,
    }

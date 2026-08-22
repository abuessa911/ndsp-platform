from __future__ import annotations

import json
import os
import time
import urllib.request
import urllib.error
from typing import Any, Dict


def _env_bool(name: str, default: bool = False) -> bool:
    value = str(os.getenv(name, "")).strip().lower()
    if not value:
        return default
    return value in ("1", "true", "yes", "on", "enabled")


def _normalize_symbol(symbol: str) -> str:
    s = str(symbol or "").upper().strip()

    if "/" in s:
        return s

    if s.endswith("USDT"):
        return s[:-4] + "/USDT"

    if s.endswith("USD"):
        return s[:-3] + "/USDT"

    return s


def _direction_to_side(direction: str) -> str | None:
    d = str(direction or "").lower().strip()

    if d in ("bullish", "buy", "long"):
        return "BUY"

    if d in ("bearish", "sell", "short"):
        return "SELL"

    return None


def maybe_send_execution_webhook(governed_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Private server-side bridge from NDSP governed decision to execution bot webhook.

    Disabled by default.
    Sends only when:
    - NDSP_EXECUTION_WEBHOOK_ENABLED=true
    - direction is bullish/bearish
    - risk_state is normal
    - system_state is not safe_mode
    - confidence >= NDSP_EXECUTION_MIN_CONFIDENCE
    """

    result = {
        "enabled": False,
        "sent": False,
        "skipped_reason": "",
        "status_code": None,
        "response": None,
        "error": None,
    }

    if not _env_bool("NDSP_EXECUTION_WEBHOOK_ENABLED", False):
        result["skipped_reason"] = "execution webhook disabled"
        return result

    url = os.getenv("NDSP_EXECUTION_WEBHOOK_URL", "").strip()
    secret = os.getenv("NDSP_EXECUTION_WEBHOOK_SECRET", "").strip()
    user_email = os.getenv("NDSP_EXECUTION_USER_EMAIL", "").strip()
    notional = float(os.getenv("NDSP_EXECUTION_NOTIONAL_USDT", "10") or 10)
    min_confidence = float(os.getenv("NDSP_EXECUTION_MIN_CONFIDENCE", "80") or 80)

    if not url or not secret or not user_email:
        result["skipped_reason"] = "missing webhook url/secret/user_email"
        return result

    decision = governed_payload.get("decision") or {}
    states = governed_payload.get("states") or {}
    risk = governed_payload.get("risk") or {}
    meta = governed_payload.get("meta") or {}

    direction = decision.get("direction")
    confidence = float(decision.get("confidence") or 0)
    side = _direction_to_side(direction)

    if not side:
        result["skipped_reason"] = f"direction not executable: {direction}"
        return result

    if confidence < min_confidence:
        result["skipped_reason"] = f"confidence below minimum: {confidence} < {min_confidence}"
        return result

    system_state = str(states.get("system_state") or "").lower()
    risk_state = str(states.get("risk_state") or risk.get("state") or "").lower()

    if system_state == "safe_mode" or risk_state != "normal":
        result["skipped_reason"] = f"risk/system blocked: system_state={system_state}, risk_state={risk_state}"
        return result

    symbol = _normalize_symbol(governed_payload.get("symbol") or meta.get("symbol_id") or "BTCUSDT")
    request_id = meta.get("request_id") or str(int(time.time()))

    payload = {
        "user_email": user_email,
        "symbol": symbol,
        "side": side,
        "notional_usdt": notional,
        "reason": f"NDSP governed decision | direction={direction} | confidence={confidence}",
        "ndsp_layer": "layer-15-final-decision",
        "signal_id": f"ndsp-{request_id}",
    }

    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-NDSP-SECRET": secret,
        },
    )

    result["enabled"] = True

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            result["status_code"] = resp.status
            result["response"] = raw
            result["sent"] = 200 <= resp.status < 300
            if not result["sent"]:
                result["error"] = raw
            return result

    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        result["status_code"] = exc.code
        result["response"] = raw
        result["error"] = raw
        return result

    except Exception as exc:
        result["error"] = repr(exc)
        return result

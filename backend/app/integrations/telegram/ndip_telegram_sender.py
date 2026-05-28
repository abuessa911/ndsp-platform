# Governed NDSP Telegram sender
# Backend = Brain
# UI/Telegram = Interface

import os
import requests

from app.integrations.telegram.channels import CHANNELS


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def _market_state(value):
    value = str(value or "neutral").lower().strip()

    if value in ("bullish", "buy", "long"):
        return "bullish"

    if value in ("bearish", "sell", "short"):
        return "bearish"

    return "neutral"


def _confidence(value):
    try:
        value = float(value)
    except Exception:
        return 0

    if value <= 1:
        value *= 100

    return max(0, min(100, int(round(value))))


def format_decision_message(decision_object: dict) -> str:
    symbol = decision_object.get("symbol", "UNKNOWN")

    decision = decision_object.get("decision", {}) or {}
    states = decision_object.get("states", {}) or {}
    risk = decision_object.get("risk", {}) or {}
    scenario = decision_object.get("scenario", {}) or {}
    market_alignment = decision_object.get("market_alignment", {}) or {}
    meta = decision_object.get("meta", {}) or {}

    market_state = _market_state(decision.get("direction") or decision.get("state"))
    confidence = _confidence(decision.get("confidence", 0))

    message = f"""
🧠 NDSP Decision Intelligence

Symbol: {symbol}

Market State: {market_state}
Confidence: {confidence}

System State: {states.get("system_state", "unknown")}
Risk State: {states.get("risk_state") or risk.get("state", "unknown")}
Position State: {states.get("position_state", "unknown")}

Scenario:
- Interest: {scenario.get("interest")}
- Invalidation: {scenario.get("invalidation")}
- Target: {scenario.get("target")}

market_alignment Context:
- Signal: {market_alignment.get("signal", "NO_SIGNAL")}
- Zone: {market_alignment.get("zone_context", "No zone context")}
- Effect: {market_alignment.get("entry_effect", "No entry adjustment")}

Governed Context:
- Control Layer: {meta.get("control_layer", "unknown")}
- Entry Scope: {meta.get("entry_scope", "unknown")}
- Momentum: {meta.get("momentum_status", "unknown")} / {meta.get("momentum_alignment", "unknown")}

—
NDSP • Decision Intelligence
""".strip()

    return message


def send_to_channel(message: str, channel_id: str):
    print("Sending governed NDSP message to Telegram")
    print("Channel:", channel_id)

    if not TELEGRAM_TOKEN:
        print("Telegram token missing")
        return {"ok": False, "reason": "telegram_token_missing"}

    if not channel_id:
        print("Channel ID is missing")
        return {"ok": False, "reason": "channel_id_missing"}

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": channel_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)

        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "text": response.text,
        }

    except Exception as e:
        print(f"Telegram error: {e}")
        return {"ok": False, "reason": str(e)}


def send_decision(decision_object: dict, plan: str = "free"):
    if not decision_object:
        print("No decision object provided")
        return {"ok": False, "reason": "missing_decision_object"}

    message = format_decision_message(decision_object)

    channel_id = CHANNELS.get(plan) or CHANNELS.get("free")
    if not channel_id:
        print("No valid channel found")
        return {"ok": False, "reason": "channel_missing"}

    return send_to_channel(message, channel_id)

import os
import time

from app.integrations.telegram.unified_sender import send_telegram_message
from app.saas.plans import can_receive_alerts, get_plan_channel


LAST_SENT = {}

COOLDOWN = int(os.getenv("NDSP_ALERT_COOLDOWN_SECONDS", "300"))
MIN_CONFIDENCE = int(os.getenv("NDSP_ALERT_MIN_CONFIDENCE", "65"))
SEND_NEUTRAL = os.getenv("NDSP_ALERT_SEND_NEUTRAL", "false").lower() == "true"


def should_send(symbol):
    now = time.time()
    last = LAST_SENT.get(symbol, 0)

    if now - last > COOLDOWN:
        LAST_SENT[symbol] = now
        return True

    return False


def normalize_market_state(direction):
    direction = str(direction or "neutral").lower().strip()

    if direction in ("bullish", "buy", "long"):
        return "bullish"

    if direction in ("bearish", "sell", "short"):
        return "bearish"

    return "neutral"


def should_alert(data):
    decision = data.get("decision", {})
    states = data.get("states", {})
    risk = data.get("risk", {})

    direction = normalize_market_state(decision.get("direction") or decision.get("state") or "neutral")
    confidence = int(decision.get("confidence", 0) or 0)

    system_state = states.get("system_state", "unknown")
    risk_state = states.get("risk_state") or risk.get("state") or "unknown"

    if system_state not in ("live", "safe_mode"):
        return False, f"system_state_blocked:{system_state}"

    if risk_state in ("paused", "drawdown"):
        return False, f"risk_state_blocked:{risk_state}"

    if direction == "neutral" and not SEND_NEUTRAL:
        return False, "neutral_blocked"

    if confidence < MIN_CONFIDENCE:
        return False, f"low_confidence:{confidence}"

    return True, "allowed"


def build_message(data):
    decision = data.get("decision", {})
    states = data.get("states", {})
    risk = data.get("risk", {})
    scenario = data.get("scenario", {})
    market_alignment = data.get("market_alignment", {})
    meta = data.get("meta", {})

    market_state = normalize_market_state(decision.get("direction") or decision.get("state") or "neutral")
    confidence = int(decision.get("confidence", 0) or 0)

    system_state = states.get("system_state", "unknown")
    risk_state = states.get("risk_state") or risk.get("state") or "unknown"
    position_state = states.get("position_state", "unknown")

    control_layer = meta.get("control_layer", "unknown")
    entry_scope = meta.get("entry_scope", "unknown")
    momentum_status = meta.get("momentum_status", "unknown")
    momentum_alignment = meta.get("momentum_alignment", "unknown")
    market_data_status = meta.get("market_data_status", "unknown")

    return f"""
🧠 NDSP Decision Intelligence

Symbol: {data.get("symbol")}

Market State: {market_state}
Confidence: {confidence}

System State: {system_state}
Risk State: {risk_state}
Position State: {position_state}

Scenario:
- Interest: {scenario.get("interest")}
- Invalidation: {scenario.get("invalidation")}
- Target: {scenario.get("target")}

market_alignment Context:
- Signal: {market_alignment.get("signal", "NO_SIGNAL")}
- Zone: {market_alignment.get("zone_context", "No zone context")}
- Effect: {market_alignment.get("entry_effect", "No entry adjustment")}

Governed Context:
- Control Layer: {control_layer}
- Entry Scope: {entry_scope}
- Momentum: {momentum_status} / {momentum_alignment}
- Market Data: {market_data_status}

NDSP is decision intelligence, not a trading bot or broker execution system.
""".strip()


def process_alert(data, plan: str = "pro"):
    symbol = data.get("symbol")

    if not symbol:
        return {
            "status": "skipped",
            "reason": "missing_symbol",
        }

    allowed, reason = should_alert(data)
    if not allowed:
        return {
            "status": "skipped",
            "reason": reason,
            "symbol": symbol,
        }

    if not should_send(symbol):
        return {
            "status": "skipped",
            "reason": "cooldown",
            "symbol": symbol,
        }

    if not can_receive_alerts(plan):
        return {
            "status": "skipped",
            "reason": "plan_alerts_disabled",
            "symbol": symbol,
            "plan": plan,
        }

    decision = data.get("decision", {})
    market_state = normalize_market_state(decision.get("direction") or decision.get("state") or "neutral")
    confidence = int(decision.get("confidence", 0) or 0)

    channel = get_plan_channel(plan)
    message = build_message(data)
    result = send_telegram_message(message, channel=channel)

    return {
        "status": "processed",
        "symbol": symbol,
        "market_state": market_state,
        "confidence": confidence,
        "plan": plan,
        "channel": channel,
        "telegram": result,
    }

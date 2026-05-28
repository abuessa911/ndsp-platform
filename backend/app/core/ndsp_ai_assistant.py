from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat()

def explain_decision(payload: dict, question: str = "") -> dict:
    decision = payload.get("decision") or {}
    states = payload.get("states") or {}
    market_alignment = payload.get("market_alignment") or {}
    explain = payload.get("explainability") or {}

    direction = decision.get("direction", "neutral")
    confidence = decision.get("confidence", 0)
    system_state = states.get("system_state", "unknown")
    risk_state = states.get("risk_state", "unknown")
    nmp_signal = market_alignment.get("signal", "NO_SIGNAL")

    answer = (
        f"NDSP reads the current context as {direction} with confidence {confidence}. "
        f"The system state is {system_state}, and the risk state is {risk_state}. "
        f"market_alignment context is {nmp_signal}. "
        f"This is decision-support guidance only, not an execution command."
    )

    if explain.get("reason"):
        answer += f" Reason: {explain.get('reason')}"

    return {
        "ok": True,
        "system": "NDSP",
        "assistant": "NDSP AI Assistant",
        "answer": answer,
        "question": question,
        "guardrails": {
            "no_buy_sell_commands": True,
            "no_tp_sl": True,
            "no_raw_logic": True,
            "no_hidden_weights": True,
            "decision_support_only": True,
        },
        "timestamp": now(),
    }

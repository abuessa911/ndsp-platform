from app.core.system_mode import MODE

def execute(symbol, decision):

    entry = decision.get("entry", {})
    conf = decision.get("decision", {}).get("confidence", 0)

    if MODE == "SAFE":
        if conf < 0.7 or not entry.get("approved"):
            return {"status": "no_trade", "reason": "safe_mode_filter"}

    if MODE == "AGGRESSIVE":
        if conf < 0.5:
            return {"status": "no_trade", "reason": "low_confidence"}

    return {
        "status": "executed",
        "symbol": symbol,
        "mode": MODE
    }

def execute_trade(symbol: str, decision: dict):

    direction = decision.get("direction")
    confidence = decision.get("confidence")

    return {
        "status": "simulated",
        "symbol": symbol,
        "action": direction,
        "confidence": confidence,
        "note": "SAFE MODE - no real trade executed"
    }

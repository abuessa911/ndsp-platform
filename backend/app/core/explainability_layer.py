def explain(response):

    decision = response.get("decision", {})
    context = response.get("context", {})

    state_raw = decision.get("state", "no_trade")
    confidence = decision.get("confidence", 0) * 100
    market_context = context.get("market_context", "unknown")

    if state_raw == "bullish":

        if confidence >= 70:
            state = "strong bullish pressure"
        elif confidence >= 55:
            state = "bullish bias"
        else:
            state = "weak bullish structure"

        guidance = f"upward behavior within {market_context}"

    elif state_raw == "bearish":

        if confidence >= 70:
            state = "strong bearish pressure"
        elif confidence >= 55:
            state = "bearish bias"
        else:
            state = "weak bearish structure"

        guidance = f"downward behavior within {market_context}"

    else:
        state = "neutral"
        guidance = f"no clear direction in {market_context}"

    response["explanation"] = {
        "state": state,
        "guidance": guidance,
        "risk": response.get("risk", {}).get("state", "unknown")
    }

    return response

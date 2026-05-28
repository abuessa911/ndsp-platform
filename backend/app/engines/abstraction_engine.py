def map_confidence(score):
    if score >= 600:
        return "high"
    elif score >= 500:
        return "medium"
    else:
        return "low"

def map_position(state):
    mapping = {
        "bullish": "favorable",
        "bearish": "unfavorable",
        "neutral": "neutral"
    }
    return mapping.get(state, "neutral")

def abstract_item(item, plan):

    base = {
        "symbol": item.get("symbol"),
        "market_position": map_position(item.get("market_state")),
        "confidence_band": map_confidence(item.get("decision_score")),
        "rank": item.get("rank")
    }

    # FREE
    if plan == "free":
        return base

    # PRO
    if plan == "pro":
        base["confidence"] = item.get("confidence")
        base["risk"] = item.get("risk")
        return base

    # INSTITUTIONAL
    if plan == "institutional":
        base["opportunity_score"] = item.get("decision_score")
        base["stability"] = item.get("momentum")
        base["liquidity_context"] = item.get("liquidity")
        return base

    return base


def abstract_response(data, plan):
    return [abstract_item(item, plan) for item in data]

from app.compliance.policy_engine import enforce_compliance


def build_scenario(state: str):
    """
    Build abstract scenario (NO execution values)
    """

    if state == "bullish":
        return {
            "interest_zone": "recent pullback area",
            "invalidation_level": "below recent structure",
            "target_zone": "higher resistance zone"
        }

    elif state == "bearish":
        return {
            "interest_zone": "recent supply zone",
            "invalidation_level": "above recent structure",
            "target_zone": "lower demand zone"
        }

    else:
        return {
            "interest_zone": "range zone",
            "invalidation_level": "range break",
            "target_zone": "range expansion"
        }


def build_explanation(state, confidence, context):
    """
    Generate human-readable explanation
    """

    if state == "bullish":
        return "Market shows upward pressure with structural support from momentum and liquidity alignment."

    elif state == "bearish":
        return "Market shows downward pressure with signs of weakness and potential continuation."

    return "Market is in a mixed or neutral state with no clear directional dominance."


def build_ndsp_output(data: dict) -> dict:
    """
    Convert raw engine output → NDSP compliant output
    """

    state = data.get("state", "neutral")
    confidence = data.get("confidence", 0.5)
    context = data.get("context", "no context")
    risk = data.get("risk", "moderate")
    score = data.get("score", 0)

    scenario = build_scenario(state)
    explanation = build_explanation(state, confidence, context)

    output = {
        "market_bias": state,
        "confidence": confidence,
        "context": context,
        "risk": risk,
        "score": score,
        "scenario": scenario,
        "explanation": explanation
    }

    # 🔒 IMPORTANT: Apply compliance layer
    output = enforce_compliance(output)

    return output

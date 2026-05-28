def build_narrative(reasoning: dict, final_state: str) -> str:
    """
    Convert structured reasoning → human narrative
    """

    momentum = reasoning.get("momentum")
    liquidity = reasoning.get("liquidity")
    divergence = reasoning.get("divergence")
    market_positioning = reasoning.get("market_positioning")

    parts = []

    if momentum == "bullish":
        parts.append("momentum dominance")
    elif momentum == "bearish":
        parts.append("momentum weakness")

    if liquidity == "bullish":
        parts.append("liquidity support")
    elif liquidity == "bearish":
        parts.append("liquidity pressure")

    if divergence == "bullish":
        parts.append("bullish divergence detected")
    elif divergence == "bearish":
        parts.append("bearish divergence detected")
    else:
        parts.append("no significant divergence")

    if market_positioning == "bullish":
        parts.append("institutional alignment")
    elif market_positioning == "bearish":
        parts.append("institutional selling pressure")

    sentence = " + ".join(parts)

    if final_state == "bullish":
        return f"{sentence} → overall upward bias"
    elif final_state == "bearish":
        return f"{sentence} → overall downward bias"
    else:
        return f"{sentence} → mixed signals, no clear direction"

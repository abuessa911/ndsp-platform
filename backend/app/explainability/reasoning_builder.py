def build_reasoning(engines: list) -> dict:
    """
    Extract structured reasoning from engines
    """

    reasoning = {
        "momentum": None,
        "liquidity": None,
        "divergence": None,
        "market_positioning": None
    }

    for e in engines:
        name = e.get("name")
        state = e.get("state")

        if name in reasoning:
            reasoning[name] = state

    return reasoning

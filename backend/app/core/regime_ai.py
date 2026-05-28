def detect_regime(symbol: str):
    return "volatile"

def adjust_weights_for_regime(weights, regime):
    if regime == "volatile":
        weights["volatility"] *= 1.5
    return weights

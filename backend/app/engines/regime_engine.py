def detect_regime(momentum: dict):

    m = momentum.get("momentum", 0)

    if abs(m) < 0.001:
        return "choppy"

    if abs(m) < 0.003:
        return "weak"

    return "trending"

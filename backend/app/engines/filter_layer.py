########################################
# 💀 NDSP FILTER LAYER (FIXED)
########################################

def block(reason: str):
    return {
        "allowed": False,
        "reason": reason
    }


def allow():
    return {
        "allowed": True
    }


def apply_filters(data: dict):

    if not isinstance(data, dict):
        return block("invalid_input")

    score = data.get("score", 0.5)
    signals = data.get("signals", {})

    ########################################
    # WEAK SCORE
    ########################################
    if score < 0.2:
        return block("weak_score")

    ########################################
    # NO SIGNALS
    ########################################
    if not signals or not isinstance(signals, dict):
        return block("no_signals")

    ########################################
    # CONFLICT
    ########################################
    if signals.get("conflict") is True:
        return block("conflict")

    ########################################
    # MOMENTUM CHECK
    ########################################
    momentum = signals.get("momentum", {})
    if isinstance(momentum, dict):
        strength = momentum.get("strength", 0)
        if strength < 0.3:
            return block("weak_momentum")

    ########################################
    # LIQUIDITY CHECK
    ########################################
    liquidity = signals.get("liquidity", {})
    if isinstance(liquidity, dict):
        if liquidity.get("state") == "dry":
            return block("low_liquidity")

    ########################################
    # PASS
    ########################################
    return allow()

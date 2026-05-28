
def calculate_confluence(layers):

    score = 0

    ########################################
    # TREND
    ########################################
    trend = layers.get("trend", {})
    if trend.get("direction") == "bullish":
        score += 2
    elif trend.get("direction") == "bearish":
        score += 2

    ########################################
    # MOMENTUM
    ########################################
    momentum = layers.get("momentum", {})
    if momentum.get("strength") == "strong":
        score += 2

    ########################################
    # LIQUIDITY
    ########################################
    liquidity = layers.get("liquidity", {})
    if liquidity.get("sweep"):
        score += 1

    ########################################
    # VOLUME
    ########################################
    volume = layers.get("volume", {})
    if volume.get("spike"):
        score += 1

    ########################################
    # STRUCTURE
    ########################################
    structure = layers.get("structure", {})
    if structure.get("break"):
        score += 2

    return score

########################################
# 💀 NDSP ENGINE CONTRACTS
########################################

ENGINE_CONTRACTS = {

    "momentum": ["signal", "state", "bias"],
    "liquidity": ["state"],
    "divergence": ["signal"],
    "orderflow": ["bias"],
    "volatility": ["state"],
    "zones": ["support", "resistance"],

    "decision": ["direction", "confidence"],
    "conflict": ["score", "reasons"],
    "entry": ["entry_score", "approved"]
}

########################################
# 💀 MARKET PROFILE ENGINE (MULTI-ASSET)
########################################

def resolve_market(symbol: str):

    symbol = symbol.upper()

    ########################################
    # 🪙 CRYPTO
    ########################################
    if symbol.endswith("USDT") or symbol.endswith("BTC"):
        return {
            "asset_class": "crypto",
            "tdl_type": "crypto_hybrid"
        }

    ########################################
    # 💱 FOREX
    ########################################
    if len(symbol) == 6:
        return {
            "asset_class": "forex",
            "tdl_type": "forex_cot"
        }

    ########################################
    # 🛢 ENERGY
    ########################################
    energy = ["WTI", "BRENT", "NG"]
    if symbol in energy:
        return {
            "asset_class": "energy",
            "tdl_type": "energy_cot"
        }

    ########################################
    # 🪨 COMMODITIES
    ########################################
    commodities = ["XAUUSD", "XAGUSD"]
    if symbol in commodities:
        return {
            "asset_class": "commodities",
            "tdl_type": "commodities_cot"
        }

    ########################################
    # 📊 INDICES
    ########################################
    indices = ["SPX", "NAS100", "DJI"]
    if symbol in indices:
        return {
            "asset_class": "indices",
            "tdl_type": "indices_cot"
        }

    ########################################
    # ❌ UNKNOWN
    ########################################
    return {
        "asset_class": "unknown",
        "tdl_type": "none"
    }

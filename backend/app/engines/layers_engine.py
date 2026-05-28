import json
import os

CONFIG_PATH = "/home/nawaf511/empire-core-new/backend/app/config/layers_config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}

    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def get_layers(symbol):

    config = load_config()

    layers = config.get("layers", {})

    # 💀 fallback
    if not layers:
        return {
            "symbol": symbol,
            "momentum": {"state": "neutral"},
            "liquidity": {"sweep": False},
            "divergence": {"type": "none"},
            "score": 0.5
        }

    return {
        "symbol": symbol,
        "layers": layers
    }

########################################
# 💀 market_alignment INTEGRATION
########################################
from app.services.nmp_engine import NMPEngine

nmp_engine = NMPEngine()

def run_nmp_layer(prices):
    return nmp_engine.evaluate(prices)

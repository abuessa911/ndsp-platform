from fastapi import APIRouter
from app.binance_feed import get_price

router = APIRouter()

@router.get("/ndsp/live")
def ndsp_live():

    data = [
        {
            "symbol": "BTCUSDT",
            "price": get_price("BTCUSDT"),
            "market_bias": "neutral",
            "confidence": 30,
            "risk": "low",
            "scenario": {
                "interest_zone": "auto",
                "invalidation_level": "auto",
                "target_zone": "auto"
            },
            "intelligence": {
                "trap": {"trap_probability": 0, "trap_state": "low"},
                "intent": {"intent_score": 30, "intent_strength": "weak"},
                "hidden": {"hidden_score": 0, "pressure": "low"},
                "intelligence_score": 12.0
            },
            "black_layer": {
                "memory": {"memory_signal": "continuation"},
                "deception": {"deception": "none"},
                "pressure": {"pressure_index": 0, "risk_level": "low"}
            }
        }
    ]

    return data

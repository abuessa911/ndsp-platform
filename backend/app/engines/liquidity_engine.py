from app.core.brain.registry import register

@register("liquidity")
def liquidity(symbol):
    return {"state": "normal"}

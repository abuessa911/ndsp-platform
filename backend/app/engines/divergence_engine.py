from app.core.brain.registry import register

@register("divergence")
def divergence(symbol):
    return {"signal": "neutral"}

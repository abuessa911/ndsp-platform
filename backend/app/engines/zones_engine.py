from app.core.brain.registry import register

@register("zones")
def zones(symbol):
    return {"support": 0, "resistance": 0}

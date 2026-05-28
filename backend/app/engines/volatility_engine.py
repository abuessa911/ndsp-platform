from app.core.brain.registry import register
from app.market.market_feed import get_price

@register("volatility")
def volatility(symbol):

    price = get_price(symbol)

    if price == 0:
        return {"state": "low"}

    if price > 50000:
        state = "high"
    else:
        state = "normal"

    return {
        "state": state,
        "value": price
    }

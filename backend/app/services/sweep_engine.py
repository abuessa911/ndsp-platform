from app.services.price_router import get_market_snapshot

def analyze_sweeps(symbol: str):

    market = get_market_snapshot(symbol)
    candles = market.get("candles", [])

    if not candles:
        return {"sweep": "none"}

    last = candles[-1]["close"]
    prev = candles[-5]["close"] if len(candles) >= 5 else last

    change = (last - prev) / prev if prev != 0 else 0

    if change > 0.003:
        sweep = "up"
    elif change < -0.003:
        sweep = "down"
    else:
        sweep = "none"

    return {"sweep": sweep, "strength": round(change, 5)}

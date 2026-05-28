import requests

def get_zones(symbol="BTCUSDT", interval="1h", limit=100):
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        res = requests.get(url, params=params, timeout=5)
        data = res.json()

        highs = [float(c[2]) for c in data]
        lows  = [float(c[3]) for c in data]
        closes = [float(c[4]) for c in data]

        if len(closes) < 20:
            return {"state": "neutral"}

        # 🟢 Demand Zone = أقل قاع حديث
        demand_zone = min(lows[-20:])

        # 🔴 Supply Zone = أعلى قمة حديثة
        supply_zone = max(highs[-20:])

        current_price = closes[-1]

        # 📊 تحديد الحالة
        if current_price <= demand_zone * 1.01:
            state = "bullish"
            location = "demand"
        elif current_price >= supply_zone * 0.99:
            state = "bearish"
            location = "supply"
        else:
            state = "neutral"
            location = "middle"

        return {
            "state": state,
            "demand_zone": demand_zone,
            "supply_zone": supply_zone,
            "location": location
        }

    except:
        return {"state": "neutral"}

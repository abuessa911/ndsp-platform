import requests
from app.indicators.rsi import calculate_rsi_series

def get_divergence(symbol="BTCUSDT", interval="1h", limit=100):
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        res = requests.get(url, params=params, timeout=5)
        data = res.json()

        closes = [float(c[4]) for c in data]

        if len(closes) < 30:
            return "neutral"

        rsi_values = calculate_rsi_series(closes)

        if len(rsi_values) < 10:
            return "neutral"

        # آخر قاعين
        price_low_1 = min(closes[-10:-5])
        price_low_2 = min(closes[-5:])

        rsi_low_1 = min(rsi_values[-10:-5])
        rsi_low_2 = min(rsi_values[-5:])

        # آخر قمتين
        price_high_1 = max(closes[-10:-5])
        price_high_2 = max(closes[-5:])

        rsi_high_1 = max(rsi_values[-10:-5])
        rsi_high_2 = max(rsi_values[-5:])

        # 🔻 Regular Bearish
        if price_high_2 > price_high_1 and rsi_high_2 < rsi_high_1:
            return "bearish"

        # 🔺 Regular Bullish
        if price_low_2 < price_low_1 and rsi_low_2 > rsi_low_1:
            return "bullish"

        # 🔻 Hidden Bearish
        if price_high_2 < price_high_1 and rsi_high_2 > rsi_high_1:
            return "bearish_hidden"

        # 🔺 Hidden Bullish
        if price_low_2 > price_low_1 and rsi_low_2 < rsi_low_1:
            return "bullish_hidden"

        return "neutral"

    except Exception:
        return "neutral"

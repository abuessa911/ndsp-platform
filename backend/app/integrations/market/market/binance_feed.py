import requests

BASE_URL = "https://api.binance.com/api/v3/ticker/price"

def get_price(symbol="BTCUSDT"):
    try:
        res = requests.get(BASE_URL, params={"symbol": symbol})
        data = res.json()
        return float(data["price"])
    except:
        return None

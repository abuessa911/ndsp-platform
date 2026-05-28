import requests, time

CACHE = {}
LAST_FETCH = {}

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"

def get_price(symbol):

    now = time.time()

    # 🧠 cache لمدة 3 ثواني
    if symbol in CACHE and now - LAST_FETCH.get(symbol, 0) < 3:
        return CACHE[symbol]

    try:
        r = requests.get(BINANCE_URL, params={"symbol": symbol}, timeout=2)
        price = float(r.json()["price"])

        CACHE[symbol] = price
        LAST_FETCH[symbol] = now

        return price

    except:
        return CACHE.get(symbol, 0.0)

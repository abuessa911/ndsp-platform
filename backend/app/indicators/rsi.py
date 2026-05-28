import requests

########################################
# 📊 GET CLOSE PRICES
########################################
def get_closes(symbol="BTCUSDT", interval="1h", limit=100):
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
        return closes

    except:
        return []

########################################
# 📈 RSI SERIES (REAL CALCULATION)
########################################
def calculate_rsi_series(closes, period=14):
    if len(closes) < period + 1:
        return []

    gains = []
    losses = []

    # أول حساب
    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(delta))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    rsi_values = []

    # RSI الأول
    if avg_loss == 0:
        rsi_values.append(100)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100 - (100 / (1 + rs)))

    # باقي القيم
    for i in range(period + 1, len(closes)):
        delta = closes[i] - closes[i - 1]

        gain = max(delta, 0)
        loss = max(-delta, 0)

        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        rsi_values.append(rsi)

    return rsi_values

########################################
# 🎯 SINGLE RSI (FOR CURRENT SYSTEM)
########################################
def get_rsi(symbol="BTCUSDT", interval="1h"):
    closes = get_closes(symbol, interval)

    if not closes:
        return None

    rsi_series = calculate_rsi_series(closes)

    if not rsi_series:
        return None

    return round(rsi_series[-1], 2)

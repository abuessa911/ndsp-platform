# /opt/empire-core/backend/app.services/intelligence_layer.py

import requests
import numpy as np

########################################
# 💀 CONFIG
########################################

BINANCE_KLINES = "https://api.binance.com/api/v3/klines"

########################################
# 📥 FETCH DATA
########################################

def get_klines(symbol, interval="1h", limit=150):
    try:
        res = requests.get(
            BINANCE_KLINES,
            params={"symbol": symbol, "interval": interval, "limit": limit},
            timeout=5
        )
        data = res.json()
        closes = [float(c[4]) for c in data]
        highs = [float(c[2]) for c in data]
        lows = [float(c[3]) for c in data]

        return closes, highs, lows
    except:
        return [], [], []

########################################
# 📊 EMA
########################################

def ema(data, period=14):
    if len(data) < period:
        return 0
    weights = np.exp(np.linspace(-1., 0., period))
    weights /= weights.sum()
    return np.convolve(data, weights, mode='valid')[-1]

########################################
# 📈 RSI
########################################

def rsi(data, period=14):
    if len(data) < period:
        return 50

    deltas = np.diff(data)
    seed = deltas[:period]

    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period

    if down == 0:
        return 100

    rs = up / down
    return 100 - (100 / (1 + rs))

########################################
# 💧 VOLATILITY
########################################

def volatility(data):
    if len(data) < 20:
        return 0
    return np.std(data[-20:])

########################################
# 💣 LIQUIDITY SWEEP DETECTION
########################################

def detect_sweep(highs, lows):
    if len(highs) < 20:
        return 0.1

    recent_high = max(highs[-20:])
    recent_low = min(lows[-20:])

    last_price = highs[-1]

    # sweep فوق
    if last_price > recent_high:
        return 0.3

    # sweep تحت
    if last_price < recent_low:
        return 0.3

    return 0.1

########################################
# 🧠 MAIN INTELLIGENCE ENGINE
########################################

def run_intelligence(symbol):

    closes, highs, lows = get_klines(symbol)

    if not closes:
        return {
            "price": 0,
            "score": 0.3,
            "signals": {
                "momentum": 0,
                "rsi": 50,
                "liquidity": 0,
                "volatility": 0
            }
        }

    current_price = closes[-1]

    ########################################
    # 📊 MOMENTUM (EMA CROSS)
    ########################################
    ema_fast = ema(closes, 9)
    ema_slow = ema(closes, 21)

    if ema_fast > ema_slow:
        momentum_score = 0.35
    else:
        momentum_score = 0.15

    ########################################
    # 📈 RSI LOGIC (SMART)
    ########################################
    rsi_value = rsi(closes)

    if rsi_value > 65:
        rsi_score = 0.35
    elif rsi_value < 35:
        rsi_score = 0.15
    else:
        rsi_score = 0.25

    ########################################
    # 💧 LIQUIDITY SWEEP
    ########################################
    liquidity_score = detect_sweep(highs, lows)

    ########################################
    # ⚡ VOLATILITY FILTER
    ########################################
    vol = volatility(closes)

    if vol > 150:
        volatility_score = 0.3
    else:
        volatility_score = 0.1

    ########################################
    # 🧠 FINAL SCORE
    ########################################
    score = (
        momentum_score +
        rsi_score +
        liquidity_score +
        volatility_score
    )

    # Normalize
    score = min(score, 1.0)

    ########################################
    # 📦 OUTPUT
    ########################################
    return {
        "price": current_price,
        "score": round(score, 2),
        "signals": {
            "momentum": momentum_score,
            "rsi": rsi_value,
            "liquidity": liquidity_score,
            "volatility": vol
        }
    }

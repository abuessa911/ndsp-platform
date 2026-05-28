import requests

SYMBOL = "BTCUSDT"
LIMIT = 500

print("📊 Fetching historical data...")

# =========================
# 📊 DATA (مرة واحدة فقط)
# =========================
url = "https://api.binance.com/api/v3/klines"
data = requests.get(url, params={
    "symbol": SYMBOL,
    "interval": "1m",
    "limit": LIMIT
}).json()

candles = [{
    "high": float(c[2]),
    "low": float(c[3]),
    "close": float(c[4])
} for c in data]

print("🚀 Running FAST backtest...\n")

# =========================
# 💰 SIMULATION
# =========================
balance = 1000
position = None
entry_price = 0

wins = 0
losses = 0


# =========================
# 🧠 HELPERS (بديل NDSP)
# =========================
def trend(c):
    closes = [x["close"] for x in c]
    sma5 = sum(closes[-5:]) / 5
    sma20 = sum(closes[-20:]) / 20

    if abs(sma5 - sma20) / sma20 < 0.001:
        return "range"
    return "up" if sma5 > sma20 else "down"


def momentum(c):
    closes = [x["close"] for x in c]
    r3 = (closes[-1] - closes[-4]) / closes[-4]
    r8 = (closes[-1] - closes[-9]) / closes[-9]
    return (r3 * 0.6) + (r8 * 0.4)


def sweep(c):
    last = c[-1]
    highs = [x["high"] for x in c[:-1]]
    lows = [x["low"] for x in c[:-1]]

    if last["low"] < min(lows) and last["close"] > min(lows):
        return "sweep_down"

    if last["high"] > max(highs) and last["close"] < max(highs):
        return "sweep_up"

    return "none"


# =========================
# 🔁 LOOP
# =========================
for i in range(50, len(candles)):

    window = candles[:i]
    price = candles[i]["close"]

    t = trend(window)
    m = momentum(window)
    s = sweep(window)

    score = 0

    # trend
    if t == "up":
        score += 1
    elif t == "down":
        score -= 1

    # momentum
    if m > 0:
        score += 1
    else:
        score -= 1

    # sweep
    if s == "sweep_down":
        score += 2
    elif s == "sweep_up":
        score -= 2

    # =========================
    # 🎯 ENTRY
    # =========================
    if position is None:

        if score >= 2:
            position = "long"
            entry_price = price

        elif score <= -2:
            position = "short"
            entry_price = price

    # =========================
    # 💰 EXIT
    # =========================
    else:

        change = (price - entry_price) / entry_price
        pnl = change if position == "long" else -change

        if pnl > 0.003:
            balance *= (1 + pnl)
            wins += 1
            position = None

        elif pnl < -0.003:
            balance *= (1 + pnl)
            losses += 1
            position = None


# =========================
# 📊 RESULTS
# =========================
print("===================================")
print("💰 Final Balance:", round(balance, 2))
print("🏆 Wins:", wins)
print("💀 Losses:", losses)

total = wins + losses
if total > 0:
    print("📊 Winrate:", round((wins/total)*100, 2), "%")

print("===================================")

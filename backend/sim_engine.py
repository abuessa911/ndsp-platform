import time
import requests

API = "http://127.0.0.1:9001/scanner"

positions = []

stats = {
    "total": 0,
    "wins": 0,
    "losses": 0
}

# ⚙️ إعدادات احترافية
MAX_OPEN_TRADES = 3
MIN_CONFIDENCE = 75


def print_stats():
    total = stats["total"]
    wins = stats["wins"]
    losses = stats["losses"]

    winrate = (wins / total * 100) if total > 0 else 0

    print("\n📊 PERFORMANCE:")
    print(f"Total Trades: {total}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Winrate: {winrate:.2f}%")
    print("-------------------------\n")


def open_trade(symbol, price, side):
    tp = price * 1.02 if side == "BUY" else price * 0.98
    sl = price * 0.99 if side == "BUY" else price * 1.01

    trade = {
        "symbol": symbol,
        "entry": price,
        "tp": tp,
        "sl": sl,
        "side": side,
        "status": "OPEN"
    }

    print(f"🚀 OPEN {side} {symbol} @ {price:.2f}")
    positions.append(trade)


def close_trade(trade, result):
    trade["status"] = result
    stats["total"] += 1

    if result == "WIN":
        stats["wins"] += 1
    else:
        stats["losses"] += 1

    print(f"{'💰 WIN' if result == 'WIN' else '❌ LOSS'} {trade['symbol']}")
    print_stats()


def check_positions(data):
    for trade in positions:
        if trade["status"] != "OPEN":
            continue

        for coin in data:
            if coin["symbol"] == trade["symbol"]:
                price = coin["price"]

                if trade["side"] == "BUY":
                    if price >= trade["tp"]:
                        close_trade(trade, "WIN")
                    elif price <= trade["sl"]:
                        close_trade(trade, "LOSS")

                elif trade["side"] == "SELL":
                    if price <= trade["tp"]:
                        close_trade(trade, "WIN")
                    elif price >= trade["sl"]:
                        close_trade(trade, "LOSS")


while True:
    try:
        # 💀 مقاومة سقوط API
        try:
            res = requests.get(API, timeout=3).json()
        except Exception as e:
            print("⚠ API DOWN... retrying:", e)
            time.sleep(3)
            continue

        open_trades_count = sum(
            1 for t in positions if t["status"] == "OPEN"
        )

        for coin in res:
            signal = coin["signal"]["signal"]
            symbol = coin["symbol"]
            price = coin["price"]
            confidence = coin["signal"]["confidence"]
            rsi = coin["signal"]["rsi"]

            already_open = any(
                t["symbol"] == symbol and t["status"] == "OPEN"
                for t in positions
            )

            # 🚫 منع Overtrading
            if open_trades_count >= MAX_OPEN_TRADES:
                break

            # 💀 فلترة احترافية
            if signal == "BUY":
                if confidence >= MIN_CONFIDENCE and rsi < 70 and not already_open:
                    open_trade(symbol, price, signal)

            elif signal == "SELL":
                if confidence >= MIN_CONFIDENCE and rsi > 30 and not already_open:
                    open_trade(symbol, price, signal)

        # 🔍 متابعة الصفقات
        check_positions(res)

        time.sleep(5)

    except Exception as e:
        print("ERROR:", e)
        time.sleep(5)

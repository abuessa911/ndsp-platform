import json
import time
import random

FILE = "/home/nawaf511/empire-core-new/backend/data/paper_portfolio.json"

def load():
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {"balance": 1000, "history": []}

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def execute(symbol, decision, price):

    data = load()

    balance = data["balance"]

    risk = 0.01  # 1% per trade

    position = balance * risk

    outcome = random.choices(
        ["win","loss"],
        weights=[0.55,0.45]
    )[0]

    pnl = position * (0.02 if outcome=="win" else -0.01)

    balance += pnl

    trade = {
        "time": time.time(),
        "symbol": symbol,
        "direction": decision.get("direction"),
        "price": price,
        "result": outcome,
        "pnl": round(pnl,2),
        "balance": round(balance,2)
    }

    data["balance"] = balance
    data["history"].append(trade)

    save(data)

    return trade

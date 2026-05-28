import json

FILE = "/home/nawaf511/empire-core-new/backend/data/paper_trades.json"

def stats():

    try:
        with open(FILE) as f:
            trades = json.load(f)
    except:
        return {}

    total = len(trades)
    wins = len([t for t in trades if t["result"] == "win"])
    pnl = sum([t["pnl"] for t in trades])

    return {
        "total_trades": total,
        "winrate": round((wins/total)*100,2) if total else 0,
        "pnl": round(pnl,2)
    }

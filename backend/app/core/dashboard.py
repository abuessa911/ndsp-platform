import json

PORTFOLIO = "/home/nawaf511/empire-core-new/backend/data/paper_portfolio.json"
OUT = "/home/nawaf511/empire-core-new/backend/data/dashboard.json"

def update_dashboard():

    try:
        with open(PORTFOLIO) as f:
            data = json.load(f)
    except:
        data = {"balance":1000,"history":[]}

    trades = data.get("history", [])

    wins = len([t for t in trades if t["result"]=="win"])
    total = len(trades)

    dashboard = {
        "balance": data.get("balance",1000),
        "total_trades": total,
        "winrate": round((wins/total)*100,2) if total else 0,
        "last_trade": trades[-1] if trades else None
    }

    with open(OUT,"w") as f:
        json.dump(dashboard,f)

    return dashboard

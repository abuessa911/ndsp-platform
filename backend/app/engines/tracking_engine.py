import json
import time
import os

TRACK_FILE = "/home/nawaf511/empire-core-new/backend/logs/performance.log"

########################################
# 🧠 SAVE DECISION
########################################

def track_decision(data):

    try:
        entry = {
            "timestamp": time.time(),
            "symbol": data.get("symbol"),
            "state": data.get("decision", {}).get("state"),
            "confidence": data.get("decision", {}).get("confidence"),
            "price": data.get("price", 0),
            "regime": data.get("context", {}).get("regime"),
            "evaluated": False,
            "result": None
        }

        with open(TRACK_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")

    except Exception as e:
        print("TRACK ERROR:", e)


########################################
# 💣 EVALUATE PERFORMANCE
########################################

def evaluate_performance(get_price_func):

    if not os.path.exists(TRACK_FILE):
        return

    updated = []

    with open(TRACK_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        try:
            entry = json.loads(line)

            if entry.get("evaluated"):
                updated.append(entry)
                continue

            symbol = entry.get("symbol")
            old_price = entry.get("price")
            state = entry.get("state")

            new_price = get_price_func(symbol)

            if old_price == 0:
                entry["result"] = "invalid"
            else:
                change = (new_price - old_price) / old_price

                if state == "bullish":
                    entry["result"] = "win" if change > 0 else "loss"
                elif state == "bearish":
                    entry["result"] = "win" if change < 0 else "loss"
                else:
                    entry["result"] = "neutral"

            entry["evaluated"] = True
            updated.append(entry)

        except:
            continue

    with open(TRACK_FILE, "w") as f:
        for e in updated:
            f.write(json.dumps(e) + "\n")


########################################
# 📊 ADVANCED STATS (V2)
########################################

def get_stats():

    if not os.path.exists(TRACK_FILE):
        return {"total": 0}

    total = 0
    wins = 0
    losses = 0

    confidence_buckets = {"low": [0,0], "mid": [0,0], "high": [0,0]}
    regime_stats = {}

    with open(TRACK_FILE, "r") as f:
        for line in f:
            try:
                e = json.loads(line)

                if not e.get("evaluated"):
                    continue

                total += 1

                result = e.get("result")
                conf = e.get("confidence", 0)
                regime = e.get("regime", "unknown")

                if result == "win":
                    wins += 1
                elif result == "loss":
                    losses += 1

                # confidence buckets
                if conf < 0.4:
                    key = "low"
                elif conf < 0.7:
                    key = "mid"
                else:
                    key = "high"

                confidence_buckets[key][1] += 1
                if result == "win":
                    confidence_buckets[key][0] += 1

                # regime stats
                if regime not in regime_stats:
                    regime_stats[regime] = {"wins":0,"total":0}

                regime_stats[regime]["total"] += 1
                if result == "win":
                    regime_stats[regime]["wins"] += 1

            except:
                continue

    accuracy = (wins / total) if total > 0 else 0

    # compute bucket accuracy
    bucket_accuracy = {}
    for k,v in confidence_buckets.items():
        w,t = v
        bucket_accuracy[k] = round((w/t),2) if t > 0 else 0

    # regime accuracy
    regime_accuracy = {}
    for k,v in regime_stats.items():
        regime_accuracy[k] = round(v["wins"]/v["total"],2) if v["total"] > 0 else 0

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "accuracy": round(accuracy,2),
        "confidence_accuracy": bucket_accuracy,
        "regime_accuracy": regime_accuracy
    }

import json
import os

LOG_FILE = "/home/nawaf511/empire-core-new/backend/logs/execution_learning.json"


class ExecutionLearning:

    def analyze(self):

        if not os.path.exists(LOG_FILE):
            return {"status": "no_data"}

        try:
            with open(LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            return {"status": "corrupted"}

        if not logs:
            return {"status": "empty"}

        total = len(logs)

        avg_slippage = sum(l.get("slippage", 0) for l in logs) / total
        avg_delay = sum(l.get("delay", 0) for l in logs) / total
        avg_chunks = sum(l.get("chunks", 0) for l in logs) / total

        return {
            "status": "ok",
            "samples": total,
            "avg_slippage": round(avg_slippage, 6),
            "avg_delay": round(avg_delay, 3),
            "avg_chunks": round(avg_chunks, 2)
        }

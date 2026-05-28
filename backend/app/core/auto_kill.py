import json

FILE = "/home/nawaf511/empire-core-new/backend/runtime/kill_switch.json"

def trigger_kill(reason="error"):

    data = {
        "active": True,
        "reason": reason
    }

    with open(FILE, "w") as f:
        json.dump(data, f)

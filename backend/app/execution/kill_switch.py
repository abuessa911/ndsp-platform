import json
import os

FILE = "/home/nawaf511/empire-core-new/backend/app/runtime/kill_switch.json"

def is_active():
    if not os.path.exists(FILE):
        return False
    data = json.load(open(FILE))
    return data.get("active", False)

def activate(reason="manual"):
    json.dump({"active": True, "reason": reason}, open(FILE, "w"))

def deactivate():
    json.dump({"active": False}, open(FILE, "w"))

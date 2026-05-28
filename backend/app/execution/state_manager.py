import time
import json
import os

STATE_FILE = "/home/nawaf511/empire-core-new/backend/app/runtime/state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_trade": 0, "trades": []}

    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

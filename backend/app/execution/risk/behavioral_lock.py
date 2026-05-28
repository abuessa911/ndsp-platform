import json
import os
from datetime import datetime, timedelta

STATE_FILE = "/home/nawaf511/empire-core-new/backend/logs/audit/behavioral_state.json"

LOSS_THRESHOLD = 0.15
LOCK_DAYS = 7

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"loss": 0, "locked_until": None}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def is_locked():
    state = load_state()
    if state["locked_until"]:
        if datetime.utcnow() < datetime.fromisoformat(state["locked_until"]):
            return True
    return False

def update_loss(pnl_ratio):
    state = load_state()
    state["loss"] += abs(pnl_ratio)

    if state["loss"] >= LOSS_THRESHOLD:
        state["locked_until"] = (datetime.utcnow() + timedelta(days=7)).isoformat()

    save_state(state)
    return state

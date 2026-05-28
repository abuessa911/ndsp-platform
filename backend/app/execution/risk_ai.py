import json
import os
import time
from app.config_risk_ai import *

FILE = "/home/nawaf511/empire-core-new/backend/app/runtime/risk_ai.json"

def load():
    if not os.path.exists(FILE):
        return {
            "daily_loss": 0,
            "loss_streak": 0,
            "blocked_until": 0
        }
    return json.load(open(FILE))

def save(data):
    json.dump(data, open(FILE, "w"))

def is_blocked(state):
    return time.time() < state["blocked_until"]

def update_after_trade(pnl):
    state = load()

    if pnl < 0:
        state["loss_streak"] += 1
        state["daily_loss"] += abs(pnl)
    else:
        state["loss_streak"] = 0

    ########################################
    # 🔥 BLOCK CONDITIONS
    ########################################
    if state["loss_streak"] >= MAX_LOSS_STREAK:
        state["blocked_until"] = time.time() + (BLOCK_HOURS * 3600)

    if state["daily_loss"] >= ACCOUNT_BALANCE * MAX_DAILY_LOSS:
        state["blocked_until"] = time.time() + (BLOCK_HOURS * 3600)

    save(state)

def can_trade():
    state = load()

    if is_blocked(state):
        return False, "BLOCKED_BY_RISK_AI"

    return True, "OK"

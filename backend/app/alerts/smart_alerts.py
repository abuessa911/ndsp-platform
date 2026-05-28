import json
import os

STATE_FILE = "/home/nawaf511/empire-core-new/backend/app/runtime/last_signal.json"

def load_last():
    if not os.path.exists(STATE_FILE):
        return {}
    return json.load(open(STATE_FILE))

def save_last(data):
    json.dump(data, open(STATE_FILE, "w"))

########################################
# 💀 DETECT CHANGE
########################################
def has_changed(new):

    old = load_last()

    if not old:
        save_last(new)
        return True, "FIRST_SIGNAL"

    ########################################
    # 🧠 STATE CHANGE
    ########################################
    if old.get("state") != new.get("state"):
        save_last(new)
        return True, "STATE_CHANGE"

    ########################################
    # 🔥 CONFIDENCE JUMP
    ########################################
    if abs(new.get("confidence", 0) - old.get("confidence", 0)) >= 15:
        save_last(new)
        return True, "CONFIDENCE_CHANGE"

    ########################################
    # 💀 market_alignment ACTIVATION
    ########################################
    if not old.get("market_alignment", {}).get("active") and new.get("market_alignment", {}).get("active"):
        save_last(new)
        return True, "NMP_TRIGGER"

    return False, None

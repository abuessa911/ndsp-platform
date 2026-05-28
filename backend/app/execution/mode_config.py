MODE = "SAFE"  # SAFE / AGGRESSIVE

def set_mode(new_mode):
    global MODE
    if new_mode in ["SAFE", "AGGRESSIVE"]:
        MODE = new_mode
        return {"status": "ok", "mode": MODE}
    return {"status": "error", "msg": "invalid mode"}

def get_mode():
    return MODE

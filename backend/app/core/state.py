# Global in-memory state (thread-safe بسيط)
STATE = {
    "price": 0.0,
    "closes": [],
    "rsi": 50.0,
    "momentum": 0.0
}

def update_state(new_data: dict):
    STATE.update(new_data)

def get_state():
    return STATE

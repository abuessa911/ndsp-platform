# ============================================
# RATE LIMITER MODULE
# ============================================

from typing import Dict
import time

# simple in-memory store
_REQUEST_STORE = {}


def apply_rate_limit(state: Dict) -> Dict:
    """
    Rate limiter to prevent abuse / overload

    INPUT:
        state: dict containing user_id / symbol / timestamp

    OUTPUT:
        modified state if rate limit exceeded
    """

    if not isinstance(state, dict):
        return {
            "system_state": "error",
            "reason": "invalid_state_format"
        }

    user_id = state.get("user_id", "anonymous")
    current_time = time.time()

    # ==============================
    # CONFIG
    # ==============================
    WINDOW = 5  # seconds
    MAX_REQUESTS = 5

    if user_id not in _REQUEST_STORE:
        _REQUEST_STORE[user_id] = []

    # تنظيف الطلبات القديمة
    _REQUEST_STORE[user_id] = [
        t for t in _REQUEST_STORE[user_id]
        if current_time - t < WINDOW
    ]

    # تحقق من الحد
    if len(_REQUEST_STORE[user_id]) >= MAX_REQUESTS:
        return {
            **state,
            "system_state": "blocked",
            "reason": "rate_limit_exceeded"
        }

    # تسجيل الطلب
    _REQUEST_STORE[user_id].append(current_time)

    return state

########################################
# 💀 TRADE LIMIT LAYER (REAL)
########################################

import time

########################################
# 📊 STORAGE
########################################
trades = {}

MAX_TRADES = 5          # عدد الصفقات
WINDOW_SECONDS = 86400  # 24 ساعة

########################################
# 🧠 CORE CHECK
########################################
def allow_trade(symbol):

    now = time.time()

    if symbol not in trades:
        trades[symbol] = []

    # حذف الصفقات القديمة
    trades[symbol] = [t for t in trades[symbol] if now - t < WINDOW_SECONDS]

    if len(trades[symbol]) >= MAX_TRADES:
        return False

    trades[symbol].append(now)
    return True


########################################
# 🔥 NDSP INTEGRATION
########################################
def apply_trade_limit(decision: dict):

    """
    يمنع الإفراط في التداول داخل النظام
    """

    symbol = decision.get("symbol")

    if not symbol:
        return decision

    allowed = allow_trade(symbol)

    ########################################
    # ❌ BLOCK
    ########################################
    if not allowed:
        decision["blocked"] = True
        decision["reason"] = "trade_limit_exceeded"

    ########################################
    # ✅ PASS
    ########################################
    decision.setdefault("meta", {})
    decision["meta"]["trade_limit"] = "ok" if allowed else "blocked"

    return decision

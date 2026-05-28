from app.core.circuit_breaker import check_circuit
from app.core.drawdown_guard import check_drawdown
from app.core.trade_limit import allow_trade
from app.core.kill_switch import is_kill_switch_active

def system_control(symbol, equity=1000):

    if is_kill_switch_active():
        return {"allowed": False, "reason": "kill_switch"}

    if check_circuit():
        return {"allowed": False, "reason": "circuit_breaker"}

    if not check_drawdown(equity):
        return {"allowed": False, "reason": "drawdown_limit"}

    if not allow_trade(symbol):
        return {"allowed": False, "reason": "trade_limit"}

    return {"allowed": True}

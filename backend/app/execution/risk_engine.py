class RiskEngine:

    def __init__(self, config):
        self.max_drawdown = config.get("max_drawdown", 0.2)
        self.daily_loss_limit = config.get("daily_loss_limit", 0.05)

    ########################################
    # 🧠 Adaptive Risk (NDSP Score Based)
    ########################################
    def get_dynamic_risk(self, ndsp_score):

        if ndsp_score >= 90:
            return 0.02
        elif ndsp_score >= 70:
            return 0.01
        elif ndsp_score >= 50:
            return 0.005
        else:
            return 0.0

    def calculate_risk_amount(self, balance, ndsp_score):
        risk_percent = self.get_dynamic_risk(ndsp_score)
        return balance * risk_percent, risk_percent

    ########################################
    # 💀 Risk Controls
    ########################################
    def check_drawdown(self, equity, peak_equity):
        if peak_equity == 0:
            return True, 0

        drawdown = (peak_equity - equity) / peak_equity

        if drawdown >= self.max_drawdown:
            return False, drawdown

        return True, drawdown

    def check_daily_loss(self, daily_pnl, balance):
        if abs(daily_pnl) >= balance * self.daily_loss_limit:
            return False
        return True

    ########################################
    # 🚀 Main Evaluation
    ########################################
    def evaluate(self, account_state, ndsp_score):

        balance = account_state["balance"]
        equity = account_state["equity"]
        peak = account_state["peak_equity"]
        daily_pnl = account_state["daily_pnl"]

        risk_amount, risk_percent = self.calculate_risk_amount(balance, ndsp_score)

        # ❌ لا تداول
        if risk_percent == 0:
            return {
                "allowed": False,
                "reason": "low_score",
                "risk_percent": risk_percent
            }

        dd_ok, dd_value = self.check_drawdown(equity, peak)
        daily_ok = self.check_daily_loss(daily_pnl, balance)

        return {
            "risk_amount": risk_amount,
            "risk_percent": risk_percent,
            "drawdown_ok": dd_ok,
            "drawdown": dd_value,
            "daily_ok": daily_ok,
            "allowed": dd_ok and daily_ok
        }

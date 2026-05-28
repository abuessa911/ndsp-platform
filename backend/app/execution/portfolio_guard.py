class PortfolioGuard:

    def __init__(self):
        self.positions = []
        self.max_total_risk = 0.3  # 30% max risk

    ########################################
    # 🧠 Validate New Position
    ########################################
    def validate(self, new_position):

        current_risk = sum(p["risk"] for p in self.positions)

        if current_risk + new_position["risk"] > self.max_total_risk:
            return False, "portfolio_risk_exceeded"

        return True, "ok"

    ########################################
    # 📊 Register Position
    ########################################
    def register(self, position):
        self.positions.append(position)

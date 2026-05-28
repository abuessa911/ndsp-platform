import numpy as np

########################################
# 💀 market_alignment ENGINE (Nawaf Meeting Point)
########################################

class NMPEngine:

    def __init__(self):
        pass

    ########################################
    # 🔥 CALCULATE market_alignment ZONE
    ########################################
    def detect_zone(self, prices):

        if len(prices) < 20:
            return {"zone": None, "strength": 0}

        high = max(prices[-20:])
        low = min(prices[-20:])
        current = prices[-1]

        mid = (high + low) / 2

        # 🔥 proximity to zone
        distance = abs(current - mid)

        # 🔥 normalize
        strength = max(0, 1 - (distance / (high - low + 1e-9)))

        return {
            "zone": mid,
            "strength": round(strength, 2),
            "position": "above" if current > mid else "below"
        }

    ########################################
    # 💀 DECISION ROLE
    ########################################
    def evaluate(self, prices):

        zone_data = self.detect_zone(prices)

        strength = zone_data["strength"]

        if strength > 0.7:
            signal = "high_interest"
        elif strength > 0.4:
            signal = "medium_interest"
        else:
            signal = "low_interest"

        return {
            "signal": signal,
            "zone": zone_data
        }

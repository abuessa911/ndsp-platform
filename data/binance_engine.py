import requests
import pandas as pd
import numpy as np
import time

# =========================
# CONFIG
# =========================
BASE_URL = "https://api.binance.com"
SYMBOL = "BTCUSDT"
INTERVALS = ["1m", "5m"]
LIMIT = 100

# =========================
# DATA LAYER (Binance)
# =========================
class BinanceClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def get_klines(self, symbol, interval, limit=100):
        url = f"{self.base_url}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        res = requests.get(url, params=params)
        data = res.json()

        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "qav", "num_trades",
            "taker_base_vol", "taker_quote_vol", "ignore"
        ])

        df["close"] = df["close"].astype(float)
        df["open"] = df["open"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["volume"] = df["volume"].astype(float)

        return df


# =========================
# FEATURE ENGINEERING
# =========================
class FeatureEngine:

    @staticmethod
    def compute_rsi(series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / (loss + 1e-9)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def compute_momentum(df):
        returns = df["close"].pct_change()
        rsi = FeatureEngine.compute_rsi(df["close"])
        momentum_score = (returns.rolling(5).mean() * 100) + (rsi / 100)
        return momentum_score.iloc[-1]

    @staticmethod
    def detect_trend(df):
        short_ma = df["close"].rolling(5).mean()
        long_ma = df["close"].rolling(20).mean()

        if short_ma.iloc[-1] > long_ma.iloc[-1]:
            return "UP"
        elif short_ma.iloc[-1] < long_ma.iloc[-1]:
            return "DOWN"
        else:
            return "RANGE"


# =========================
# ADAPTER (NDSP BRIDGE)
# =========================
class NDSPAdapter:
    def __init__(self, run_decision_fn, black_layer_fn):
        self.run_decision = run_decision_fn
        self.black_layer = black_layer_fn

    def process(self, market_state):
        decision = self.run_decision(market_state)
        final_output = self.black_layer(decision, market_state)
        return final_output


# =========================
# CORE ENGINE
# =========================
class NDSPMarketEngine:
    def __init__(self, symbol, adapter):
        self.client = BinanceClient()
        self.symbol = symbol
        self.adapter = adapter

    def build_market_state(self):
        data = {}

        for interval in INTERVALS:
            df = self.client.get_klines(self.symbol, interval, LIMIT)

            trend = FeatureEngine.detect_trend(df)
            momentum = FeatureEngine.compute_momentum(df)
            price = df["close"].iloc[-1]

            data[interval] = {
                "price": price,
                "trend": trend,
                "momentum": float(momentum),
            }

        return data

    def run(self):
        market_state = self.build_market_state()

        output = self.adapter.process(market_state)

        return {
            "market_state": market_state,
            "decision": output
        }


# =========================
# MOCK (Replace with your real system)
# =========================
def run_decision(market_state):
    # مثال بسيط — أنت تستبدله بنظامك
    if market_state["1m"]["trend"] == "UP" and market_state["1m"]["momentum"] > 0:
        return "BUY"
    elif market_state["1m"]["trend"] == "DOWN":
        return "SELL"
    return "HOLD"


def black_layer(decision, market_state):
    # مثال: فلترة إضافية
    if decision == "BUY" and market_state["5m"]["trend"] != "UP":
        return "FILTERED"
    return decision


# =========================
# MAIN LOOP (Production style)
# =========================
if __name__ == "__main__":
    adapter = NDSPAdapter(run_decision, black_layer)
    engine = NDSPMarketEngine(SYMBOL, adapter)

    while True:
        try:
            result = engine.run()

            print("Market State:", result["market_state"])
            print("Final Decision:", result["decision"])
            print("-" * 50)

            time.sleep(5)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

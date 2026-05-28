import sys
import json

try:
    data = json.load(sys.stdin)

    for coin in data:
        symbol = coin["symbol"]
        signal = coin["signal"]["signal"]
        confidence = coin["signal"]["confidence"]

        if signal == "BUY":
            print(f"🔥 BUY → {symbol} | confidence: {confidence}")

        elif signal == "SELL":
            print(f"⚠ SELL → {symbol} | confidence: {confidence}")

except Exception as e:
    print("ERROR:", e)

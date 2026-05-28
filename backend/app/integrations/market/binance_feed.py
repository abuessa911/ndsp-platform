import asyncio
import json
import websockets

DATA_FILE = "/home/nawaf511/empire-core-new/backend/data/prices.json"

async def stream():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    while True:
        try:
            print("🔌 Connecting to Binance...")
            async with websockets.connect(url) as ws:
                print("✅ Connected!")

                async for msg in ws:
                    data = json.loads(msg)

                    price = float(data["p"])

                    print("📈 BTC:", price)

                    with open(DATA_FILE, "w") as f:
                        json.dump({"BTCUSDT": price}, f)

        except Exception as e:
            print("❌ ERROR:", e)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(stream())

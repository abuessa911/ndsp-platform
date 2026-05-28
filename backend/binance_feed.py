import asyncio
import websockets
import json

price_data = {}

async def stream():
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            price_data["BTCUSDT"] = float(data["p"])
            print("BTC:", price_data["BTCUSDT"])

asyncio.run(stream())

import asyncio
import json
import random
from datetime import datetime

async def generate_signal():
    while True:
        data = {
            "price": round(random.uniform(2000, 3000), 2),
            "bias": random.choice(["bullish", "bearish", "neutral"]),
            "confidence": round(random.uniform(0.5, 0.9), 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        yield json.dumps(data)
        await asyncio.sleep(2)

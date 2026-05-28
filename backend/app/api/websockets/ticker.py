from __future__ import annotations

import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

SIMULATED_HEADLINES = [
    "MARKET DESK: FED INTEREST RATE DECISION PENDING...",
    "GLOBAL MARKETS: GOLD TESTS RECORD TERRITORY...",
    "MACRO WATCH: DOLLAR INDEX HOLDS NEAR KEY LEVELS...",
    "RISK MONITOR: VOLATILITY CONDITIONS REMAIN ELEVATED...",
]

@router.websocket("/ws/ticker")
async def ticker_socket(websocket: WebSocket):
    await websocket.accept()
    index = 0
    try:
        while True:
            await websocket.send_json({
                "system": "NDSP",
                "type": "simulated_market_headline",
                "headline": SIMULATED_HEADLINES[index % len(SIMULATED_HEADLINES)]
            })
            index += 1
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        return

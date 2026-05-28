from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from datetime import datetime

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # 💀 بيانات NDSP (مؤقتًا)
            data = {
                "state": "bullish",
                "confidence": 0.82,
                "risk": "moderate",
                "timestamp": datetime.utcnow().isoformat()
            }

            await websocket.send_json(data)

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("❌ Client disconnected")

    except Exception as e:
        print("💥 WebSocket Error:", e)

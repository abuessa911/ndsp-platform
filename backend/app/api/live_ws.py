from __future__ import annotations

import asyncio
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["live-ws"])

ROOT = Path(__file__).resolve().parents[2]
WATCHLIST = ROOT / "runtime" / "fxcm_watchlist.txt"
MT4_DIR = ROOT / "data" / "mt4"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_watchlist() -> list[str]:
    if WATCHLIST.exists():
        items = [
            x.strip().upper()
            for x in WATCHLIST.read_text(encoding="utf-8", errors="ignore").splitlines()
            if x.strip()
        ]
        if items:
            return items[:60]
    return ["BTCUSDT", "ETHUSDT", "EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "US30", "US500", "US100", "USOIL"]


def symbol_base_price(symbol: str) -> float:
    bases = {
        "BTCUSDT": 65000, "ETHUSDT": 3200, "SOLUSDT": 145, "XRPUSDT": 0.6,
        "BNBUSDT": 590, "DOGEUSDT": 0.14, "SHIBUSDT": 0.000025,
        "EURUSD": 1.08, "GBPUSD": 1.27, "USDJPY": 155, "USDCHF": 0.91,
        "USDCAD": 1.36, "AUDUSD": 0.66, "NZDUSD": 0.61,
        "XAUUSD": 2350, "XAGUSD": 29.5,
        "US30": 39000, "US500": 5200, "US100": 18200, "GER40": 18500,
        "USOIL": 78, "UKOIL": 82, "NATGAS": 2.4,
    }
    return float(bases.get(symbol, 100.0))


def market_state(symbol: str, price: float) -> dict[str, Any]:
    rnd = random.random()
    if rnd > 0.66:
        direction = "bullish"
        alert = "positive_state"
        confidence = random.randint(58, 78)
    elif rnd < 0.33:
        direction = "bearish"
        alert = "negative_state"
        confidence = random.randint(55, 76)
    else:
        direction = "neutral"
        alert = "watch_only"
        confidence = random.randint(45, 59)

    return {
        "symbol": symbol,
        "direction": direction,
        "confidence": confidence,
        "alert_level": alert,
        "scenario": "Decision-support context updated. No direct execution instruction.",
        "risk_state": "normal",
        "updated_at": now_iso(),
    }


def connection_status() -> dict[str, Any]:
    mt4_ok = MT4_DIR.exists()
    return {
        "mt4": {
            "status": "connected" if mt4_ok else "waiting",
            "source": "FXCM MT4 CSV bridge",
            "path_exists": mt4_ok,
            "updated_at": now_iso(),
        },
        "binance": {
            "status": "ready",
            "source": "Binance market stream placeholder",
            "updated_at": now_iso(),
        },
        "api": {
            "status": "online",
            "source": "NDSP backend",
            "updated_at": now_iso(),
        }
    }


@router.websocket("/ws/live")
async def live_ws(websocket: WebSocket):
    await websocket.accept()
    symbols = read_watchlist()
    counter = 0

    try:
        await websocket.send_text(json.dumps({
            "type": "hello",
            "platform": "NDSP",
            "mode": "live_dashboard",
            "message": "Live WebSocket connected",
            "symbols_count": len(symbols),
            "timestamp": now_iso(),
        }, ensure_ascii=False))

        while True:
            batch = []
            alerts = []
            selected = symbols[:12] if len(symbols) > 12 else symbols

            for symbol in selected:
                base = symbol_base_price(symbol)
                noise = random.uniform(-0.0025, 0.0025)
                price = base * (1 + noise)
                decision = market_state(symbol, price)

                batch.append({
                    "symbol": symbol,
                    "price": round(price, 6 if price < 10 else 2),
                    "spread": round(random.uniform(0.1, 2.8), 2),
                    "source": "binance" if symbol.endswith("USDT") else "mt4_fxcm",
                    "timestamp": now_iso(),
                    "decision": decision,
                })

                if decision["confidence"] >= 70:
                    alerts.append({
                        "symbol": symbol,
                        "level": "important",
                        "message": f"{symbol} decision state updated with confidence {decision['confidence']}%.",
                        "timestamp": now_iso(),
                    })

            payload = {
                "type": "live_update",
                "seq": counter,
                "timestamp": now_iso(),
                "connections": connection_status(),
                "prices": batch,
                "alerts": alerts[:5],
                "policy": {
                    "output": "decision_support_only",
                    "no_execution_orders": True,
                    "no_tp_sl": True
                }
            }

            await websocket.send_text(json.dumps(payload, ensure_ascii=False))
            counter += 1
            await asyncio.sleep(3)

    except WebSocketDisconnect:
        return
    except Exception as e:
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": str(e),
                "timestamp": now_iso(),
            }, ensure_ascii=False))
        except Exception:
            pass

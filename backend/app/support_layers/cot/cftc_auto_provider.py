"""
NDSP V6.1 CFTC Auto Provider Placeholder

Purpose:
- Provide a controlled extension point for official CFTC ingestion.
- Current implementation is a deterministic placeholder.
- Production ingestion can replace fetch_official_snapshot later.

Important:
- Auto data never overrides manual_override.
"""

from __future__ import annotations

from app.support_layers.cot.cot_storage import CotStorage


class CftcAutoProvider:
    def __init__(self, storage: CotStorage | None = None) -> None:
        self.storage = storage or CotStorage()

    def seed_auto_demo(self, symbol: str = "EURUSD") -> None:
        symbol = symbol.upper()

        if symbol == "EURUSD":
            positions = [
                {"category": "institutional direction/Institutional", "long": 110000, "short": 95000},
                {"category": "market activity", "long": 43000, "short": 39000},
                {"category": "market momentum", "long": 80000, "short": 90000},
                {"category": "Dealer/Intermediary", "long": 60000, "short": 65000},
            ]
        elif symbol in {"XAUUSD", "GOLD"}:
            positions = [
                {"category": "Producer/Merchant/Processor/User", "long": 72000, "short": 100000},
                {"category": "Swap Dealers", "long": 50000, "short": 47000},
                {"category": "market activity", "long": 44000, "short": 30000},
                {"category": "Managed Money", "long": 120000, "short": 80000},
            ]
        else:
            positions = [
                {"category": "institutional_positioning", "long": 5000, "short": 5500},
                {"category": "Noncommercials", "long": 11000, "short": 9500},
            ]

        self.storage.save_snapshot(
            symbol=symbol,
            report_date="2026-05-12",
            positions=positions,
            source="auto_demo_cftc_placeholder",
            source_type="auto_cftc",
        )

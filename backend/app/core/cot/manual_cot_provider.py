from __future__ import annotations

from app.core.market_positioning.cot_asset_mapper import normalize_symbol, resolve_cot_asset_mapping
from app.core.market_positioning.cot_contracts import CotCategoryPosition, CotSnapshot


class ManualCotProvider:
    def __init__(self) -> None:
        self._snapshots: dict[str, CotSnapshot] = {}

    def put_snapshot(
        self,
        *,
        symbol: str,
        report_date: str,
        positions: list[dict],
        source: str = "manual",
    ) -> CotSnapshot:
        normalized = normalize_symbol(symbol)
        mapping = resolve_cot_asset_mapping(normalized)

        snapshot = CotSnapshot(
            symbol=normalized,
            report_date=report_date,
            report_family=mapping.report_family,
            positions=tuple(
                CotCategoryPosition(
                    category=str(p["category"]),
                    long=float(p.get("long", 0.0)),
                    short=float(p.get("short", 0.0)),
                )
                for p in positions
            ),
            source=source,
            metadata={
                "asset_class": mapping.asset_class.value,
                "fallback_allowed": mapping.fallback_allowed,
                "mapping_notes": mapping.notes,
            },
        )

        self._snapshots[normalized] = snapshot
        return snapshot

    def get_snapshot(self, symbol: str) -> CotSnapshot | None:
        return self._snapshots.get(normalize_symbol(symbol))


def seed_demo_provider() -> ManualCotProvider:
    provider = ManualCotProvider()

    provider.put_snapshot(
        symbol="EURUSD",
        report_date="2026-05-12",
        positions=[
            {"category": "institutional direction/Institutional", "long": 125000, "short": 90000},
            {"category": "market activity", "long": 42000, "short": 38000},
            {"category": "market momentum", "long": 76000, "short": 98000},
            {"category": "Dealer/Intermediary", "long": 60000, "short": 70000},
        ],
    )

    provider.put_snapshot(
        symbol="XAUUSD",
        report_date="2026-05-12",
        positions=[
            {"category": "Producer/Merchant/Processor/User", "long": 70000, "short": 105000},
            {"category": "Swap Dealers", "long": 52000, "short": 48000},
            {"category": "market activity", "long": 45000, "short": 30000},
            {"category": "Managed Money", "long": 135000, "short": 76000},
        ],
    )

    provider.put_snapshot(
        symbol="USOIL",
        report_date="2026-05-12",
        positions=[
            {"category": "Producer/Merchant/Processor/User", "long": 200000, "short": 260000},
            {"category": "Swap Dealers", "long": 160000, "short": 140000},
            {"category": "market activity", "long": 80000, "short": 76000},
            {"category": "Managed Money", "long": 220000, "short": 180000},
        ],
    )

    provider.put_snapshot(
        symbol="BTCUSDT",
        report_date="2026-05-12",
        positions=[
            {"category": "institutional_positioning", "long": 5200, "short": 6100},
            {"category": "Noncommercials", "long": 12400, "short": 9000},
        ],
    )

    return provider

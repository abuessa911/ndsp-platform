"""
NDSP V6.1 market_positioning Storage

Purpose:
- Persist market_positioning snapshots in runtime storage.
- Manual Override has priority over auto source.
- Storage does not create trading signals.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from app.support_layers.cot.cot_asset_mapper import normalize_symbol, resolve_cot_asset_mapping
from app.support_layers.cot.cot_contracts import CotCategoryPosition, CotSnapshot


DEFAULT_STORAGE_PATH = Path(__file__).resolve().parents[3] / "runtime" / "cot_storage.json"


class CotStorage:
    def __init__(self, storage_path: str | Path | None = None) -> None:
        self.storage_path = Path(storage_path) if storage_path else DEFAULT_STORAGE_PATH
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        if not self.storage_path.exists():
            self.storage_path.write_text(
                json.dumps(
                    {
                        "manual_override": {},
                        "auto_cftc": {},
                        "metadata": {
                            "schema_version": "v6.1",
                            "net_formula": "net = long - short",
                            "execution_allowed": False,
                        },
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )

    def _read(self) -> dict[str, Any]:
        self._ensure_storage()
        return json.loads(self.storage_path.read_text())

    def _write(self, data: dict[str, Any]) -> None:
        self.storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def save_snapshot(
        self,
        *,
        symbol: str,
        report_date: str,
        positions: list[dict[str, Any]],
        source: str,
        source_type: str,
    ) -> CotSnapshot:
        if source_type not in {"manual_override", "auto_cftc"}:
            raise ValueError("source_type must be manual_override or auto_cftc")

        normalized = normalize_symbol(symbol)
        mapping = resolve_cot_asset_mapping(normalized)

        parsed_positions = [
            {
                "category": str(p["category"]),
                "long": float(p.get("long", 0.0)),
                "short": float(p.get("short", 0.0)),
                "net": float(p.get("long", 0.0)) - float(p.get("short", 0.0)),
            }
            for p in positions
        ]

        record = {
            "symbol": normalized,
            "report_date": report_date,
            "report_family": mapping.report_family.value,
            "asset_class": mapping.asset_class.value,
            "positions": parsed_positions,
            "source": source,
            "source_type": source_type,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "context_only": True,
            "execution_allowed": False,
            "net_formula": "net = long - short",
        }

        data = self._read()
        data[source_type][normalized] = record
        self._write(data)

        return self._record_to_snapshot(record)

    def get_latest_record(self, symbol: str) -> dict[str, Any] | None:
        normalized = normalize_symbol(symbol)
        data = self._read()

        manual = data.get("manual_override", {}).get(normalized)
        if manual:
            manual = dict(manual)
            manual["active_source"] = "MANUAL_OVERRIDE"
            return manual

        auto = data.get("auto_cftc", {}).get(normalized)
        if auto:
            auto = dict(auto)
            auto["active_source"] = "AUTO_CFTC"
            return auto

        return None

    def get_latest_snapshot(self, symbol: str) -> CotSnapshot | None:
        record = self.get_latest_record(symbol)
        if not record:
            return None
        return self._record_to_snapshot(record)

    def clear_manual_override(self, symbol: str) -> bool:
        normalized = normalize_symbol(symbol)
        data = self._read()

        if normalized in data.get("manual_override", {}):
            del data["manual_override"][normalized]
            self._write(data)
            return True

        return False

    def _record_to_snapshot(self, record: dict[str, Any]) -> CotSnapshot:
        positions = tuple(
            CotCategoryPosition(
                category=str(p["category"]),
                long=float(p.get("long", 0.0)),
                short=float(p.get("short", 0.0)),
            )
            for p in record.get("positions", [])
        )

        mapping = resolve_cot_asset_mapping(record["symbol"])

        return CotSnapshot(
            symbol=record["symbol"],
            report_date=record["report_date"],
            report_family=mapping.report_family,
            positions=positions,
            source=record.get("active_source", record.get("source_type", "unknown")),
            metadata={
                "asset_class": record.get("asset_class"),
                "source": record.get("source"),
                "source_type": record.get("source_type"),
                "active_source": record.get("active_source"),
                "context_only": True,
                "execution_allowed": False,
                "net_formula": "net = long - short",
            },
        )


def snapshot_to_dict(snapshot: CotSnapshot) -> dict[str, Any]:
    return {
        "symbol": snapshot.symbol,
        "report_date": snapshot.report_date,
        "report_family": snapshot.report_family.value,
        "source": snapshot.source,
        "positions": [
            {
                "category": p.category,
                "long": p.long,
                "short": p.short,
                "net": p.net,
            }
            for p in snapshot.positions
        ],
        "metadata": dict(snapshot.metadata),
    }

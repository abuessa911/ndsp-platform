#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.core.cot.cot_asset_mapper import resolve_cot_asset_mapping
from app.core.cot.cot_storage import CotStorage


def _categories_for_symbol(symbol: str) -> list[str]:
    mapping = resolve_cot_asset_mapping(symbol)
    return list(mapping.lm_categories + mapping.s_categories)


def manual_entry() -> int:
    print("")
    print("--- NDSP COT Manual Override Panel ---")
    print("This entry will override auto CFTC data for the selected symbol.")
    print("Net formula is fixed: net = long - short")
    print("")

    symbol = input("Symbol مثل EURUSD أو XAUUSD أو USOIL: ").strip().upper()
    report_date = input("Report date YYYY-MM-DD: ").strip()

    categories = _categories_for_symbol(symbol)
    positions = []

    print("")
    print("Enter Long/Short for each required category.")
    print("Press Enter for 0 if category not available.")
    print("")

    for cat in categories:
        raw_long = input(f"{cat} Long: ").strip() or "0"
        raw_short = input(f"{cat} Short: ").strip() or "0"
        positions.append(
            {
                "category": cat,
                "long": float(raw_long),
                "short": float(raw_short),
            }
        )

    storage = CotStorage()
    storage.save_snapshot(
        symbol=symbol,
        report_date=report_date,
        positions=positions,
        source="operator_manual_entry",
        source_type="manual_override",
    )

    print("")
    print(f"MANUAL_OVERRIDE_SAVED=True")
    print(f"SYMBOL={symbol}")
    print("EXECUTION_ALLOWED=False")
    return 0


if __name__ == "__main__":
    raise SystemExit(manual_entry())

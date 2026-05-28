from __future__ import annotations

from typing import Dict, Any, List, Optional
from pathlib import Path
import csv
import time


MT4_DIRS = [
    Path("/home/nawaf511/empire-core-new/backend/data/mt4"),
    Path("/home/nawaf511/empire-core-new/backend/data"),
    Path("/home/nawaf511/mt4"),
]


def _find_file(symbol: str) -> Optional[Path]:
    names = [
        f"{symbol}.csv",
        f"{symbol.upper()}.csv",
        f"{symbol.lower()}.csv",
        f"{symbol}_M1.csv",
        f"{symbol.upper()}_M1.csv",
        f"{symbol}_H1.csv",
        f"{symbol.upper()}_H1.csv",
    ]

    for base in MT4_DIRS:
        for name in names:
            p = base / name
            if p.exists() and p.is_file():
                return p

    return None


def _read_last_rows(path: Path, limit: int = 2) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        sample = f.read(2048)
        f.seek(0)

        has_header = any(x in sample.lower() for x in ["time", "open", "high", "low", "close"])

        if has_header:
            reader = csv.DictReader(f)
            rows = list(reader)
            return rows[-limit:]

        reader = csv.reader(f)
        rows = list(reader)[-limit:]
        converted = []

        for row in rows:
            if len(row) < 5:
                continue

            converted.append({
                "time": row[0],
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
                "volume": row[5] if len(row) > 5 else "0",
            })

        return converted


def _to_float(row: Dict[str, str], key: str) -> float:
    for k, v in row.items():
        if k.lower().strip() == key:
            return float(str(v).replace(",", "").strip())
    return 0.0


def get_mt4_symbol_pulse(symbol: str) -> Dict[str, Any]:
    symbol = symbol.upper()
    path = _find_file(symbol)

    if not path:
        return {
            "symbol": symbol,
            "last_price": None,
            "change_percent": None,
            "state": "WAITING_FEED",
            "source": "mt4",
            "live": False,
            "note": "MT4 CSV feed not found",
        }

    rows = _read_last_rows(path, 2)

    if not rows:
        return {
            "symbol": symbol,
            "last_price": None,
            "change_percent": None,
            "state": "WAITING_FEED",
            "source": "mt4",
            "live": False,
            "note": "MT4 CSV feed empty",
        }

    last = rows[-1]
    prev = rows[-2] if len(rows) > 1 else rows[-1]

    last_close = _to_float(last, "close")
    prev_close = _to_float(prev, "close")

    if not last_close:
        return {
            "symbol": symbol,
            "last_price": None,
            "change_percent": None,
            "state": "WAITING_FEED",
            "source": "mt4",
            "live": False,
            "note": "Invalid MT4 close price",
        }

    pct = 0.0
    if prev_close:
        pct = ((last_close - prev_close) / prev_close) * 100

    age_seconds = int(time.time() - path.stat().st_mtime)
    live = age_seconds <= 300

    if abs(pct) >= 0.5:
        state = "VOLATILE"
    elif pct > 0:
        state = "ACTIVE"
    elif pct < 0:
        state = "CAUTION"
    else:
        state = "NEUTRAL"

    if not live:
        state = "STALE_FEED"

    return {
        "symbol": symbol,
        "last_price": round(last_close, 6),
        "change_percent": round(pct, 4),
        "state": state,
        "source": "mt4",
        "live": live,
        "age_seconds": age_seconds,
    }


def get_mt4_pulse(symbols: List[str]) -> List[Dict[str, Any]]:
    return [get_mt4_symbol_pulse(s) for s in symbols]

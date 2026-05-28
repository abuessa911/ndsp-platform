from __future__ import annotations

import csv
import os
from pathlib import Path
from datetime import datetime, timezone


DEFAULT_MT4_CSV_DIR = Path("data/mt4")


def _num(value, default=0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def _parse_time(value):
    if not value:
        return None

    raw = str(value).strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(raw, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception:
            pass

    return raw


def _symbol_id(symbol: str) -> str:
    return str(symbol or "").upper().replace("-SPOT", "").strip()


def _base_dir() -> Path:
    raw = os.getenv("NDSP_MT4_CSV_DIR") or os.getenv("MT4_CSV_DIR") or str(DEFAULT_MT4_CSV_DIR)
    p = Path(raw)
    if not p.is_absolute():
        p = Path(__file__).resolve().parents[2] / p
    return p


def _symbol_aliases(symbol: str) -> list[str]:
    s = _symbol_id(symbol)

    aliases = {
        "USOIL": ["USOIL", "USOil", "USOilSpot", "WTI", "WTISPOT"],
        "UKOIL": ["UKOIL", "UKOil", "UKOilSpot", "BRENT", "BRENTSPOT"],
        "XAUUSD": ["XAUUSD", "GOLD", "Gold"],
        "XAGUSD": ["XAGUSD", "SILVER", "Silver"],
        "US30": ["US30", "DJ30", "DJI", "WallStreet30"],
        "US100": ["US100", "NAS100", "USTEC", "NASQ100"],
        "US500": ["US500", "SPX500", "SP500"],
        "GER40": ["GER40", "DE40", "DAX40"],
        "UK100": ["UK100", "FTSE100"],
        "FRA40": ["FRA40", "CAC40"],
        "EU50": ["EU50", "EUSTX50"],
        "JP225": ["JP225", "JPN225", "NIKKEI225"],
        "HK50": ["HK50", "HKG50", "HKG33"],
        "AUS200": ["AUS200", "ASX200"],
        "CHINA50": ["CHINA50", "CN50"],
        "ES35": ["ES35", "ESP35"],
    }

    out = aliases.get(s, [s])
    seen = set()
    unique = []
    for item in out:
        key = str(item).upper()
        if key not in seen:
            seen.add(key)
            unique.append(str(item))
    return unique


def _candidate_files(symbol: str, base_dir: Path) -> list[Path]:
    symbols = _symbol_aliases(symbol)
    frames = ["M1", "M5", "M15", "M30", "H1", "H4", "D1"]

    files: list[Path] = []

    for sym in symbols:
        variants = [sym, sym.upper(), sym.lower()]
        for v in variants:
            files.append(base_dir / f"{v}.csv")
            files.append(base_dir / f"{v}_PRICE.csv")
            files.append(base_dir / f"{v}_prices.csv")
            for tf in frames:
                files.append(base_dir / f"{v}_{tf}.csv")
                files.append(base_dir / f"NDSP_MT4_CANDLES_{v}_{tf}.csv")
                files.append(base_dir / f"NDIP_MT4_CANDLES_{v}_{tf}.csv")

    if base_dir.exists():
        for sym in symbols:
            files.extend(sorted(base_dir.glob(f"*{sym}*.csv")))
            files.extend(sorted(base_dir.glob(f"*{sym.upper()}*.csv")))
            files.extend(sorted(base_dir.glob(f"*{sym.lower()}*.csv")))

    seen = set()
    unique = []
    for path in files:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def _normalize_header_row(row: dict) -> dict:
    lower = {str(k).strip().lower(): v for k, v in row.items()}

    time_value = (
        lower.get("time")
        or lower.get("datetime")
        or lower.get("date")
        or lower.get("timestamp")
    )

    return {
        "time": _parse_time(time_value),
        "open": _num(lower.get("open")),
        "high": _num(lower.get("high")),
        "low": _num(lower.get("low")),
        "close": _num(lower.get("close")),
        "volume": _num(lower.get("volume", lower.get("tick_volume", lower.get("tickvolume")))),
        "bid": _num(lower.get("bid")),
        "ask": _num(lower.get("ask")),
        "spread": _num(lower.get("spread")),
        "nmp_low": _num(lower.get("nmp_low")),
        "nmp_high": _num(lower.get("nmp_high")),
    }


def _normalize_raw_row(row: list[str]) -> dict | None:
    if len(row) < 8:
        return None

    return {
        "symbol": str(row[0]).strip().upper(),
        "timeframe": str(row[1]).strip(),
        "time": _parse_time(row[2]),
        "open": _num(row[3]),
        "high": _num(row[4]),
        "low": _num(row[5]),
        "close": _num(row[6]),
        "volume": _num(row[7]),
        "bid": _num(row[8]) if len(row) > 8 else 0.0,
        "ask": _num(row[9]) if len(row) > 9 else 0.0,
        "spread": _num(row[10]) if len(row) > 10 else 0.0,
        "nmp_low": _num(row[11]) if len(row) > 11 else 0.0,
        "nmp_high": _num(row[12]) if len(row) > 12 else 0.0,
    }


def _looks_like_header(first_row: list[str]) -> bool:
    joined = ",".join(str(x).lower().strip() for x in first_row)
    return "open" in joined and "high" in joined and "low" in joined and "close" in joined


def _read_csv(path: Path, symbol: str) -> list[dict]:
    if not path.exists():
        return []

    rows = []

    with path.open("r", newline="", encoding="utf-8-sig") as f:
        sample_reader = csv.reader(f)
        all_rows = list(sample_reader)

    if not all_rows:
        return []

    aliases_upper = {x.upper() for x in _symbol_aliases(symbol)}

    if _looks_like_header(all_rows[0]):
        with path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [_normalize_header_row(row) for row in reader]
    else:
        for raw in all_rows:
            candle = _normalize_raw_row(raw)
            if not candle:
                continue

            candle_symbol = str(candle.get("symbol") or "").upper()
            if candle_symbol and candle_symbol not in aliases_upper:
                continue

            rows.append(candle)

    return [
        r for r in rows
        if r.get("open") or r.get("high") or r.get("low") or r.get("close")
    ]


def get_market_snapshot(symbol: str) -> dict:
    symbol_clean = _symbol_id(symbol)
    base_dir = _base_dir()

    selected = None
    candles = []

    for path in _candidate_files(symbol_clean, base_dir):
        rows = _read_csv(path, symbol_clean)
        if rows:
            selected = path
            candles = rows[-250:]
            break

    if not candles:
        return {
            "symbol": symbol_clean,
            "symbol_id": f"{symbol_clean}-MT4",
            "price": None,
            "ohlcv": [],
            "candles": [],
            "last_candle": None,
            "source": "mt4_fxcm",
            "source_status": {
                "mt4_available": False,
                "csv_dir": str(base_dir),
                "error": "no_mt4_csv_found_or_empty",
            },
        }

    last = candles[-1]
    price = last.get("close") or last.get("bid") or None

    return {
        "symbol": symbol_clean,
        "symbol_id": f"{symbol_clean}-MT4",
        "price": price,
        "bid": last.get("bid"),
        "ask": last.get("ask"),
        "spread": last.get("spread"),
        "time": last.get("time"),
        "ohlcv": candles,
        "candles": candles,
        "last_candle": last,
        "source": "mt4_fxcm",
        "source_status": {
            "mt4_available": True,
            "csv_file": str(selected),
            "csv_dir": str(base_dir),
            "candles": len(candles),
        },
    }


def get_price(symbol: str) -> float:
    return float(get_market_snapshot(symbol).get("price") or 0.0)

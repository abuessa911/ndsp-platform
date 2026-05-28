"""
NDSP V5.0 Binance Live Adapter

Purpose:
- Fetch Binance Spot OHLCV data.
- Normalize timestamps to UTC.
- Return NDSP-compatible market records.

Governance:
- Data adapter is Data Authority only.
- It must not produce direction, confidence, or execution decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json


@dataclass(frozen=True)
class OhlcvRecord:
    symbol: str
    interval: str
    timestamp: int
    open_time_utc: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    source: str = "binance_spot"


class BinanceLiveProvider:
    BASE_URL = "https://api.binance.com/api/v3"

    def _get_json(self, path: str, params: dict[str, Any], timeout: int = 8) -> Any:
        query = urlencode(params)
        url = f"{self.BASE_URL}{path}?{query}"
        req = Request(
            url,
            headers={
                "User-Agent": "NDSP-V5/1.0",
                "Accept": "application/json",
            },
        )
        with urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)

    def fetch_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 1) -> list[OhlcvRecord]:
        symbol = symbol.strip().upper()
        data = self._get_json(
            "/klines",
            {
                "symbol": symbol,
                "interval": interval,
                "limit": int(limit),
            },
        )

        records: list[OhlcvRecord] = []

        for row in data:
            open_time = int(row[0])
            close_time = int(row[6])
            records.append(
                OhlcvRecord(
                    symbol=symbol,
                    interval=interval,
                    timestamp=open_time,
                    open_time_utc=datetime.fromtimestamp(open_time / 1000, tz=timezone.utc).isoformat(),
                    open=float(row[1]),
                    high=float(row[2]),
                    low=float(row[3]),
                    close=float(row[4]),
                    volume=float(row[5]),
                    close_time=close_time,
                )
            )

        return records

    def fetch_latest_ohlcv_dict(self, symbol: str, interval: str = "1h") -> dict[str, Any] | None:
        records = self.fetch_ohlcv(symbol=symbol, interval=interval, limit=1)
        if not records:
            return None
        r = records[-1]
        return {
            "symbol": r.symbol,
            "interval": r.interval,
            "timestamp": r.timestamp,
            "open_time_utc": r.open_time_utc,
            "open": r.open,
            "high": r.high,
            "low": r.low,
            "close": r.close,
            "volume": r.volume,
            "source": r.source,
        }


def validate_ohlcv_record(record: OhlcvRecord) -> bool:
    if record.open <= 0 or record.high <= 0 or record.low <= 0 or record.close <= 0:
        return False
    if record.high < max(record.open, record.close):
        return False
    if record.low > min(record.open, record.close):
        return False
    if record.high < record.low:
        return False
    return True

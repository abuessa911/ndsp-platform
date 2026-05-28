"""
NDSP V5.5 Global Markets Provider

Purpose:
- Fetch global market prices for forex, metals, indices, and energy.
- Use provider failover:
  1) Twelve Data when API key is available.
  2) Yahoo Finance via yfinance when installed.
  3) Yahoo Finance chart endpoint via stdlib urllib.
- Normalize output into NDSP MarketDataRecord.

Governance:
- Data provider is Data Authority only.
- It must not produce direction, confidence, or execution signal.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import os
import time


class MarketAssetClass(str, Enum):
    FOREX = "forex"
    METALS = "metals"
    ENERGY = "energy"
    INDEX = "index"
    CRYPTO = "crypto"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class MarketDataRecord:
    symbol: str
    provider_symbol: str
    asset_class: MarketAssetClass
    price: float
    timestamp_ms: int
    utc_time: str
    source: str
    status: str
    raw: dict[str, Any]


class MarketRouter:
    """
    Maps NDSP symbols into provider symbols.

    Yahoo Finance examples:
    - EURUSD => EURUSD=X
    - XAUUSD/GOLD => GC=F
    - USOIL/OIL => CL=F
    - US30 => ^DJI
    - US500 => ^GSPC
    - US100 => ^IXIC
    """

    MAP: dict[str, dict[str, str]] = {
        "GOLD": {"twelve": "XAU/USD", "yahoo": "GC=F", "asset_class": "metals"},
        "XAUUSD": {"twelve": "XAU/USD", "yahoo": "GC=F", "asset_class": "metals"},
        "SILVER": {"twelve": "XAG/USD", "yahoo": "SI=F", "asset_class": "metals"},
        "XAGUSD": {"twelve": "XAG/USD", "yahoo": "SI=F", "asset_class": "metals"},

        "EURUSD": {"twelve": "EUR/USD", "yahoo": "EURUSD=X", "asset_class": "forex"},
        "GBPUSD": {"twelve": "GBP/USD", "yahoo": "GBPUSD=X", "asset_class": "forex"},
        "USDJPY": {"twelve": "USD/JPY", "yahoo": "JPY=X", "asset_class": "forex"},
        "AUDUSD": {"twelve": "AUD/USD", "yahoo": "AUDUSD=X", "asset_class": "forex"},
        "USDCAD": {"twelve": "USD/CAD", "yahoo": "CAD=X", "asset_class": "forex"},
        "USDCHF": {"twelve": "USD/CHF", "yahoo": "CHF=X", "asset_class": "forex"},
        "NZDUSD": {"twelve": "NZD/USD", "yahoo": "NZDUSD=X", "asset_class": "forex"},

        "US30": {"twelve": "DJI", "yahoo": "^DJI", "asset_class": "index"},
        "US500": {"twelve": "SPX", "yahoo": "^GSPC", "asset_class": "index"},
        "US100": {"twelve": "IXIC", "yahoo": "^IXIC", "asset_class": "index"},
        "GER40": {"twelve": "DAX", "yahoo": "^GDAXI", "asset_class": "index"},
        "UK100": {"twelve": "FTSE", "yahoo": "^FTSE", "asset_class": "index"},
        "JP225": {"twelve": "NIKKEI225", "yahoo": "^N225", "asset_class": "index"},

        "OIL": {"twelve": "WTI/USD", "yahoo": "CL=F", "asset_class": "energy"},
        "USOIL": {"twelve": "WTI/USD", "yahoo": "CL=F", "asset_class": "energy"},
        "UKOIL": {"twelve": "BRENT/USD", "yahoo": "BZ=F", "asset_class": "energy"},
        "BRENT": {"twelve": "BRENT/USD", "yahoo": "BZ=F", "asset_class": "energy"},
    }

    @classmethod
    def normalize(cls, name: str) -> str:
        return str(name or "").strip().upper().replace("/", "").replace("-", "")

    @classmethod
    def resolve(cls, name: str) -> dict[str, str]:
        key = cls.normalize(name)
        if key in cls.MAP:
            return cls.MAP[key]

        return {
            "twelve": name,
            "yahoo": name,
            "asset_class": "unknown",
        }

    @classmethod
    def twelve_symbol(cls, name: str) -> str:
        return cls.resolve(name)["twelve"]

    @classmethod
    def yahoo_symbol(cls, name: str) -> str:
        return cls.resolve(name)["yahoo"]

    @classmethod
    def asset_class(cls, name: str) -> MarketAssetClass:
        value = cls.resolve(name).get("asset_class", "unknown")
        try:
            return MarketAssetClass(value)
        except ValueError:
            return MarketAssetClass.UNKNOWN


class GlobalDataProvider:
    def __init__(self, api_key: str | None = None, timeout: int = 8) -> None:
        self.api_key = api_key or os.getenv("TWELVE_DATA_API_KEY", "").strip()
        self.timeout = timeout
        self.twelve_url = "https://api.twelvedata.com/time_series"

    def fetch_price(self, symbol: str, interval: str = "1h") -> MarketDataRecord | None:
        """
        Fetch price using failover.

        Returns:
        - MarketDataRecord on success
        - None when all providers fail
        """
        providers_tried: list[str] = []

        if self.api_key:
            providers_tried.append("twelvedata")
            record = self._fetch_twelve_data(symbol, interval)
            if record:
                return record

        providers_tried.append("yfinance")
        record = self._fetch_yfinance(symbol, interval)
        if record:
            return record

        providers_tried.append("yahoo_chart")
        record = self._fetch_yahoo_chart(symbol, interval)
        if record:
            return record

        return None

    def _format_output(
        self,
        *,
        symbol: str,
        provider_symbol: str,
        price: float,
        source: str,
        raw: dict[str, Any],
    ) -> MarketDataRecord:
        ts = int(time.time() * 1000)
        return MarketDataRecord(
            symbol=MarketRouter.normalize(symbol),
            provider_symbol=provider_symbol,
            asset_class=MarketRouter.asset_class(symbol),
            price=float(price),
            timestamp_ms=ts,
            utc_time=datetime.now(timezone.utc).isoformat(),
            source=source,
            status="HEALTHY",
            raw=raw,
        )

    def _fetch_twelve_data(self, symbol: str, interval: str) -> MarketDataRecord | None:
        provider_symbol = MarketRouter.twelve_symbol(symbol)

        try:
            params = {
                "symbol": provider_symbol,
                "interval": interval,
                "outputsize": 1,
                "apikey": self.api_key,
            }

            url = f"{self.twelve_url}?{urlencode(params)}"
            req = Request(url, headers={"User-Agent": "NDSP-V5.5/1.0", "Accept": "application/json"})

            with urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))

            if "values" not in data or not data["values"]:
                return None

            latest = data["values"][0]
            close = float(latest["close"])

            return self._format_output(
                symbol=symbol,
                provider_symbol=provider_symbol,
                price=close,
                source="twelvedata",
                raw={"provider": "twelvedata", "latest": latest},
            )

        except Exception:
            return None

    def _fetch_yfinance(self, symbol: str, interval: str) -> MarketDataRecord | None:
        provider_symbol = MarketRouter.yahoo_symbol(symbol)

        try:
            import yfinance as yf  # type: ignore

            ticker = yf.Ticker(provider_symbol)
            hist = ticker.history(period="5d", interval=interval)

            if hist is None or hist.empty:
                return None

            latest_price = float(hist["Close"].iloc[-1])

            return self._format_output(
                symbol=symbol,
                provider_symbol=provider_symbol,
                price=latest_price,
                source="yfinance",
                raw={"provider": "yfinance", "rows": int(len(hist))},
            )

        except Exception:
            return None

    def _fetch_yahoo_chart(self, symbol: str, interval: str) -> MarketDataRecord | None:
        provider_symbol = MarketRouter.yahoo_symbol(symbol)

        interval_map = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "60m",
            "1d": "1d",
        }
        yahoo_interval = interval_map.get(interval, "60m")

        try:
            params = {
                "range": "5d",
                "interval": yahoo_interval,
            }

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{provider_symbol}?{urlencode(params)}"
            req = Request(url, headers={"User-Agent": "NDSP-V5.5/1.0", "Accept": "application/json"})

            with urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))

            result = data.get("chart", {}).get("result", [])
            if not result:
                return None

            quote = result[0].get("indicators", {}).get("quote", [{}])[0]
            closes = quote.get("close", [])
            valid_closes = [float(x) for x in closes if x is not None]

            if not valid_closes:
                return None

            latest_price = valid_closes[-1]

            return self._format_output(
                symbol=symbol,
                provider_symbol=provider_symbol,
                price=latest_price,
                source="yahoo_chart",
                raw={"provider": "yahoo_chart", "points": len(valid_closes)},
            )

        except Exception:
            return None


def record_to_dict(record: MarketDataRecord | None) -> dict[str, Any] | None:
    if record is None:
        return None
    out = asdict(record)
    out["asset_class"] = record.asset_class.value
    return out

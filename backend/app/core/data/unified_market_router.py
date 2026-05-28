"""
NDSP V6.2 Unified Market Router

Purpose:
- Route crypto symbols to Binance provider.
- Route forex/metals/indices/energy to Global provider.
- Normalize market data into one contract.
- Never produce direction, confidence, or execution signal.

Governance:
- Data source router only.
- context_only=True
- execution_allowed=False
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from app.core.data.binance_live import BinanceLiveProvider, validate_ohlcv_record
from app.core.data.global_provider import GlobalDataProvider, MarketAssetClass, MarketRouter as GlobalMarketRouter


class UnifiedProviderName(str, Enum):
    BINANCE = "binance_spot"
    GLOBAL = "global_provider"


class UnifiedAssetClass(str, Enum):
    CRYPTO = "crypto"
    FOREX = "forex"
    METALS = "metals"
    ENERGY = "energy"
    INDEX = "index"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class UnifiedMarketRecord:
    symbol: str
    requested_symbol: str
    asset_class: UnifiedAssetClass
    price: float
    source: str
    provider_route: str
    timestamp_ms: int | None
    utc_time: str | None
    status: str
    context_only: bool
    execution_allowed: bool
    raw: dict[str, Any]


CRYPTO_SYMBOLS = {
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT",
    "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SHIBUSDT",
}


def normalize_symbol(symbol: str) -> str:
    return str(symbol or "").strip().upper().replace("/", "").replace("-", "")


def is_crypto_symbol(symbol: str) -> bool:
    s = normalize_symbol(symbol)
    return s in CRYPTO_SYMBOLS or s.endswith("USDT")


def resolve_unified_asset_class(symbol: str) -> UnifiedAssetClass:
    s = normalize_symbol(symbol)

    if is_crypto_symbol(s):
        return UnifiedAssetClass.CRYPTO

    global_class = GlobalMarketRouter.asset_class(s)

    if global_class == MarketAssetClass.FOREX:
        return UnifiedAssetClass.FOREX
    if global_class == MarketAssetClass.METALS:
        return UnifiedAssetClass.METALS
    if global_class == MarketAssetClass.ENERGY:
        return UnifiedAssetClass.ENERGY
    if global_class == MarketAssetClass.INDEX:
        return UnifiedAssetClass.INDEX

    return UnifiedAssetClass.UNKNOWN


class UnifiedMarketRouter:
    def __init__(
        self,
        binance_provider: BinanceLiveProvider | None = None,
        global_provider: GlobalDataProvider | None = None,
    ) -> None:
        self.binance_provider = binance_provider or BinanceLiveProvider()
        self.global_provider = global_provider or GlobalDataProvider()

    def route_name(self, symbol: str) -> UnifiedProviderName:
        if is_crypto_symbol(symbol):
            return UnifiedProviderName.BINANCE
        return UnifiedProviderName.GLOBAL

    def fetch_market_record(self, symbol: str, interval: str = "1h") -> UnifiedMarketRecord | None:
        requested = normalize_symbol(symbol)
        route = self.route_name(requested)

        if route == UnifiedProviderName.BINANCE:
            return self._fetch_binance(requested, interval)

        return self._fetch_global(requested, interval)

    def _fetch_binance(self, symbol: str, interval: str) -> UnifiedMarketRecord | None:
        try:
            records = self.binance_provider.fetch_ohlcv(symbol=symbol, interval=interval, limit=1)
        except Exception:
            return None

        if not records:
            return None

        latest = records[-1]
        valid = validate_ohlcv_record(latest)

        if not valid:
            return None

        return UnifiedMarketRecord(
            symbol=latest.symbol,
            requested_symbol=symbol,
            asset_class=UnifiedAssetClass.CRYPTO,
            price=float(latest.close),
            source=latest.source,
            provider_route=UnifiedProviderName.BINANCE.value,
            timestamp_ms=int(latest.timestamp),
            utc_time=latest.open_time_utc,
            status="HEALTHY",
            context_only=True,
            execution_allowed=False,
            raw={
                "open": latest.open,
                "high": latest.high,
                "low": latest.low,
                "close": latest.close,
                "volume": latest.volume,
                "interval": latest.interval,
                "close_time": latest.close_time,
            },
        )

    def _fetch_global(self, symbol: str, interval: str) -> UnifiedMarketRecord | None:
        record = self.global_provider.fetch_price(symbol, interval=interval)

        if record is None:
            return None

        return UnifiedMarketRecord(
            symbol=record.symbol,
            requested_symbol=symbol,
            asset_class=resolve_unified_asset_class(symbol),
            price=float(record.price),
            source=record.source,
            provider_route=UnifiedProviderName.GLOBAL.value,
            timestamp_ms=int(record.timestamp_ms),
            utc_time=record.utc_time,
            status=record.status,
            context_only=True,
            execution_allowed=False,
            raw={
                "provider_symbol": record.provider_symbol,
                "asset_class": record.asset_class.value,
                "raw": record.raw,
            },
        )


def market_record_to_dict(record: UnifiedMarketRecord | None) -> dict[str, Any] | None:
    if record is None:
        return None
    data = asdict(record)
    data["asset_class"] = record.asset_class.value
    return data

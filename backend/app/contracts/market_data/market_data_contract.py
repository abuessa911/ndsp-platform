"""
NDSP Market Data Contract
عقد بيانات السوق
"""

from dataclasses import dataclass
from typing import Optional


CONTRACT_VERSION = "NDSP_MARKET_DATA_V1"


@dataclass(frozen=True)
class Candle:
    asset: str
    timeframe: str

    open: float
    high: float
    low: float
    close: float

    timestamp: str

    volume: Optional[float] = None

    provider: Optional[str] = None
    dataset: Optional[str] = None

    contract_version: str = CONTRACT_VERSION


@dataclass(frozen=True)
class Freshness:
    report_date: str
    report_age_days: int
    max_age_days: int
    fresh: bool

    contract_version: str = CONTRACT_VERSION


def validate_candle(c: Candle) -> None:
    if not c.asset:
        raise ValueError("asset (الأصل) is required")

    if not c.timeframe:
        raise ValueError("timeframe (الإطار الزمني) is required")

    if not c.timestamp:
        raise ValueError("timestamp (الطابع الزمني) is required")

    if c.high < c.low:
        raise ValueError(
            "high (الأعلى) cannot be below low (الأدنى)"
        )

    for name, value in (
        ("open", c.open),
        ("close", c.close),
    ):
        if not (c.low <= value <= c.high):
            raise ValueError(
                f"{name} must be inside candle high/low range"
            )


def validate_freshness(f: Freshness) -> None:
    if f.report_age_days < 0:
        raise ValueError(
            "report_age_days (عمر التقرير) cannot be negative"
        )

    if f.max_age_days < 0:
        raise ValueError(
            "max_age_days (الحد الأقصى للعمر) cannot be negative"
        )

    expected = f.report_age_days <= f.max_age_days

    if f.fresh != expected:
        raise ValueError(
            "fresh (الحداثة) disagrees with "
            "report_age_days/max_age_days"
        )

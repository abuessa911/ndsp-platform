from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CotReportFamily(str, Enum):
    TFF = "TFF"
    DISAGGREGATED = "DISAGGREGATED"
    LEGACY = "LEGACY"


class CotAssetClass(str, Enum):
    FOREX = "forex"
    METALS = "metals"
    ENERGY = "energy"
    INDICES = "indices"
    CRYPTO = "crypto"
    UNKNOWN = "unknown"


class CotDirection(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass(frozen=True)
class CotAssetMapping:
    symbol: str
    asset_class: CotAssetClass
    report_family: CotReportFamily
    lm_categories: tuple[str, ...]
    s_categories: tuple[str, ...]
    fallback_allowed: bool
    notes: str


@dataclass(frozen=True)
class CotCategoryPosition:
    category: str
    long: float
    short: float

    @property
    def net(self) -> float:
        return float(self.long) - float(self.short)


@dataclass(frozen=True)
class CotSnapshot:
    symbol: str
    report_date: str
    report_family: CotReportFamily
    positions: tuple[CotCategoryPosition, ...]
    source: str = "manual"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CotGroupResult:
    group_name: str
    categories: tuple[str, ...]
    net: float
    direction: CotDirection


@dataclass(frozen=True)
class CotIntelligenceResult:
    symbol: str
    report_date: str
    report_family: CotReportFamily
    lm: CotGroupResult
    s: CotGroupResult
    dominant_group: str
    dominant_direction: CotDirection
    alignment_state: str
    confidence_effect: float
    context_only: bool
    execution_allowed: bool
    notes: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

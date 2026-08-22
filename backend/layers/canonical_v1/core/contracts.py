from __future__ import annotations
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any

class Direction(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"

class DataGateStatus(str, Enum):
    CURRENT = "CURRENT"
    EXPECTED_NOT_YET_DUE = "EXPECTED_NOT_YET_DUE"
    EXPECTED_RELEASE_WINDOW = "EXPECTED_RELEASE_WINDOW"
    DELAY_CONFIRMED = "DELAY_CONFIRMED"
    EXPECTED_REPORT_MISSING = "EXPECTED_REPORT_MISSING"
    STALE = "STALE"
    SOURCE_MISMATCH = "SOURCE_MISMATCH"
    INTEGRITY_FAILED = "INTEGRITY_FAILED"
    INCOMPLETE_MARKETS = "INCOMPLETE_MARKETS"
    DUPLICATE_PAYLOAD = "DUPLICATE_PAYLOAD"
    BACKLOG_MODE = "BACKLOG_MODE"

class DecisionReadinessState(str, Enum):
    DATA_BLOCKED = "DATA_BLOCKED"
    BLOCKED_BY_DEVILS_ADVOCATE = "BLOCKED_BY_DEVILS_ADVOCATE"
    MONITORING_ONLY = "MONITORING_ONLY"
    UNDER_REVIEW = "UNDER_REVIEW"
    READY = "READY"

def coerce_direction(value: Direction | str | None) -> Direction:
    if isinstance(value, Direction):
        return value
    raw = str(value or "").strip().lower()
    aliases = {
        "bullish": Direction.BULLISH, "bull": Direction.BULLISH,
        "up": Direction.BULLISH, "positive": Direction.BULLISH,
        "bearish": Direction.BEARISH, "bear": Direction.BEARISH,
        "down": Direction.BEARISH, "negative": Direction.BEARISH,
        "neutral": Direction.NEUTRAL, "flat": Direction.NEUTRAL,
        "unknown": Direction.UNKNOWN, "": Direction.UNKNOWN,
    }
    return aliases.get(raw, Direction.UNKNOWN)

def directional(value: Direction | str | None) -> bool:
    return coerce_direction(value) in {Direction.BULLISH, Direction.BEARISH}

@dataclass(frozen=True)
class LayerResult:
    layer_id: str
    canonical_name: str
    status: str
    confidence: int
    output: dict[str, Any]
    blocking: bool = False
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = list(self.reasons)
        return data

@dataclass(frozen=True)
class CotValidity:
    status: DataGateStatus
    decision_use_allowed: bool
    monitoring_use_allowed: bool
    report_as_of_date: str | None = None
    expected_report_as_of_date: str | None = None
    expected_release_at: str | None = None
    reason_code: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data

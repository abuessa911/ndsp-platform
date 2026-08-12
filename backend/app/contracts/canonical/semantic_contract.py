"""
NDSP Canonical Semantic Contract
العقد الدلالي القياسي

Governance baseline: NDSP_GOVERNANCE_V1
"""

from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass


CONTRACT_VERSION = "NDSP_CANONICAL_SEMANTIC_V1"


class Direction(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class DirectionScope(str, Enum):
    OVERALL = "OVERALL"
    WEEKLY = "WEEKLY"


class ParticipantGroup(str, Enum):
    ASSET_MANAGERS = "ASSET_MANAGERS"
    LEVERAGED_FUNDS = "LEVERAGED_FUNDS"
    DEALER_INTERMEDIARY = "DEALER_INTERMEDIARY"


class ExposureClass(str, Enum):
    PUBLIC = "PUBLIC"
    ADMIN = "ADMIN"
    INTERNAL = "INTERNAL"
    EXPERIMENTAL = "EXPERIMENTAL"
    WITHHELD = "WITHHELD"


class QualityStatus(str, Enum):
    VALID = "VALID"
    INCOMPLETE = "INCOMPLETE"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


@dataclass(frozen=True)
class CanonicalValue:
    field_id: str
    value: Any
    data_type: str
    semantic_role: str

    unit: Optional[str] = None

    asset: Optional[str] = None
    asset_class: Optional[str] = None

    producer: Optional[str] = None
    consumer: Optional[str] = None

    source: Optional[str] = None
    source_family: Optional[str] = None
    source_path: Optional[str] = None

    method_id: Optional[str] = None

    timeframe: Optional[str] = None
    horizon: Optional[str] = None

    observed_at: Optional[str] = None
    calculated_at: Optional[str] = None

    report_date: Optional[str] = None
    report_age_days: Optional[int] = None

    fresh: Optional[bool] = None
    complete: bool = True

    missing_reason: Optional[str] = None
    fallback_used: bool = False

    quality_status: str = QualityStatus.UNKNOWN.value
    authority: Optional[str] = None
    exposure_class: str = ExposureClass.INTERNAL.value

    contract_version: str = CONTRACT_VERSION


def validate_missing_semantics(value: CanonicalValue) -> None:
    """
    Missing (مفقود) must remain explicitly missing.
    لا نحول البيانات المفقودة إلى صفر أو محايد.
    """
    if value.value is None and value.complete:
        raise ValueError(
            f"{value.field_id}: value is missing but complete=True"
        )

    if value.value is None and not value.missing_reason:
        raise ValueError(
            f"{value.field_id}: missing value requires missing_reason"
        )


def validate_fallback_semantics(value: CanonicalValue) -> None:
    """
    Fallback (احتياطي) must remain distinguishable
    from authoritative data (البيانات المعتمدة).
    """
    if value.fallback_used and value.authority == "AUTHORITATIVE":
        raise ValueError(
            f"{value.field_id}: fallback cannot silently be AUTHORITATIVE"
        )

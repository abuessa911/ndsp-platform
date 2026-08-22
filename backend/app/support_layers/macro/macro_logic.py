"""
NDSP V4.1 Macro Surprise Logic

Purpose:
- Compare actual macro value against expected/consensus value.
- Convert the result into quality effect only.
- Never change direction.

Interpretation:
- surprise = actual - expected
- hawkish/dovish meaning depends on event type.
- For inflation/rates/jobs strength:
  higher-than-expected is generally hawkish USD pressure.
- This is a quality/macro pressure input, not a direction authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.support_layers.macro.consensus_provider import MacroConsensus, MacroEventType


class MacroBias(str, Enum):
    HAWKISH = "hawkish"
    DOVISH = "dovish"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class MacroActual:
    event_type: MacroEventType
    actual_value: float
    unit: str
    timestamp_utc: str | None = None


@dataclass(frozen=True)
class MacroSurpriseResult:
    event_type: MacroEventType
    actual_value: float
    expected_value: float | None
    surprise: float | None
    normalized_surprise: float
    bias: MacroBias
    confidence_effect: float
    quality_effect: float
    source: str
    valid: bool
    reason: str


HAWKISH_WHEN_HIGHER = {
    MacroEventType.FED_RATE,
    MacroEventType.CPI,
    MacroEventType.CORE_CPI,
    MacroEventType.NFP,
    MacroEventType.PCE,
    MacroEventType.CORE_PCE,
    MacroEventType.GDP,
    MacroEventType.RETAIL_SALES,
    MacroEventType.ISM,
}

DOVISH_WHEN_HIGHER = {
    MacroEventType.UNEMPLOYMENT_RATE,
}


def _normalize_surprise(surprise: float, expected: float) -> float:
    base = abs(expected)
    if base < 1e-9:
        base = 1.0

    ratio = surprise / base

    if ratio > 1.0:
        return 1.0
    if ratio < -1.0:
        return -1.0
    return ratio


def calculate_macro_surprise(
    actual: MacroActual,
    consensus: MacroConsensus | None,
    neutral_band: float = 0.0001,
) -> MacroSurpriseResult:
    if consensus is None:
        return MacroSurpriseResult(
            event_type=actual.event_type,
            actual_value=actual.actual_value,
            expected_value=None,
            surprise=None,
            normalized_surprise=0.0,
            bias=MacroBias.UNKNOWN,
            confidence_effect=0.0,
            quality_effect=0.0,
            source="missing_consensus",
            valid=False,
            reason="consensus_missing",
        )

    surprise = float(actual.actual_value) - float(consensus.expected_value)
    normalized = _normalize_surprise(surprise, float(consensus.expected_value))

    if abs(surprise) <= neutral_band:
        bias = MacroBias.NEUTRAL
    elif actual.event_type in HAWKISH_WHEN_HIGHER:
        bias = MacroBias.HAWKISH if surprise > 0 else MacroBias.DOVISH
    elif actual.event_type in DOVISH_WHEN_HIGHER:
        bias = MacroBias.DOVISH if surprise > 0 else MacroBias.HAWKISH
    else:
        bias = MacroBias.UNKNOWN

    effect_strength = min(1.0, abs(normalized))

    if bias == MacroBias.NEUTRAL:
        confidence_effect = 0.0
        quality_effect = 0.0
    elif bias == MacroBias.UNKNOWN:
        confidence_effect = 0.0
        quality_effect = 0.0
    else:
        confidence_effect = effect_strength
        quality_effect = effect_strength

    return MacroSurpriseResult(
        event_type=actual.event_type,
        actual_value=float(actual.actual_value),
        expected_value=float(consensus.expected_value),
        surprise=surprise,
        normalized_surprise=normalized,
        bias=bias,
        confidence_effect=confidence_effect,
        quality_effect=quality_effect,
        source=consensus.source,
        valid=True,
        reason="ok",
    )


def macro_quality_stack_effect(result: MacroSurpriseResult) -> dict[str, float]:
    """
    Convert macro surprise into DQS effect.

    DQS has macro_effect weight. This function returns a normalized value:
    - 0.0 when missing/neutral/unknown
    - positive when a valid macro surprise exists

    Direction alignment must be decided outside this function.
    Macro itself does not know or change decision.direction.
    """
    if not result.valid:
        return {"macro_effect": 0.0}

    if result.bias in {MacroBias.NEUTRAL, MacroBias.UNKNOWN}:
        return {"macro_effect": 0.0}

    return {"macro_effect": min(1.0, abs(result.quality_effect))}

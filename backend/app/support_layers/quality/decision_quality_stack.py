"""
NDSP V4.5 Decision Quality Stack Integration

Purpose:
- Integrate base confidence, macro effect, and risk shield safety state.
- Produce final_confidence, quality_score, grade, decision_state, and reasons.

Governance:
- DQS is the single source of confidence and grade.
- DQS must never change decision.direction.
- DQS must never allow direct execution.
- risk shield can veto the decision state, but execution remains sanitized.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QualityGrade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"
    BLOCKED = "F_BLOCKED"


class DQSDecisionState(str, Enum):
    ACTIVE = "active"
    ACTIVE_CAUTION = "active_caution"
    BLOCKED = "blocked"
    REVIEW_ONLY = "review_only"


class DQSRiskState(str, Enum):
    NORMAL = "normal"
    CAUTION = "caution"
    HIGH = "high"
    DATA_STALE = "data_stale"
    MARKET_CLOSED = "market_closed"


@dataclass(frozen=True)
class DQSInput:
    base_confidence: float
    macro_effect: float = 0.0
    black_layer_penalty: float = 0.0
    black_severity: str = "CLEAR"
    black_reasons: list[str] = field(default_factory=list)
    data_quality_penalty: float = 0.0
    session_penalty: float = 0.0
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QualityResult:
    final_confidence: float
    quality_score: float
    grade: str
    quality_label: str
    decision_state: str
    risk_state: str
    execution_allowed: bool
    execution_mode: str
    reasons: list[str]
    breakdown: dict[str, Any]


class DecisionQualityStack:
    """
    Central quality engine.

    Initial weights:
    - base_confidence is already 0..100
    - macro_effect is normalized -1.0..1.0 and contributes up to +/-20
    - black_layer_penalty is normalized 0.0..1.0 and subtracts up to 30
    - data/session penalties are normalized 0.0..1.0
    """

    MACRO_WEIGHT = 20.0
    BLACK_LAYER_WEIGHT = 30.0
    DATA_QUALITY_WEIGHT = 15.0
    SESSION_WEIGHT = 20.0

    def _clamp(self, value: float, low: float = 0.0, high: float = 100.0) -> float:
        return max(low, min(high, float(value)))

    def _clamp_effect(self, value: float, low: float = -1.0, high: float = 1.0) -> float:
        return max(low, min(high, float(value)))

    def _clamp_penalty(self, value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def _grade_from_score(self, score: float, blocked: bool) -> tuple[str, str]:
        if blocked:
            return QualityGrade.BLOCKED.value, "blocked_by_safety"

        if score >= 85:
            return QualityGrade.A.value, "elite_quality"
        if score >= 70:
            return QualityGrade.B.value, "strong_quality"
        if score >= 50:
            return QualityGrade.C.value, "caution_quality"
        if score >= 30:
            return QualityGrade.D.value, "weak_quality"
        return QualityGrade.F.value, "invalid_or_low_quality"

    def calculate_total_quality(self, inp: DQSInput) -> QualityResult:
        base = self._clamp(inp.base_confidence)
        macro_effect = self._clamp_effect(inp.macro_effect)
        black_penalty = self._clamp_penalty(inp.black_layer_penalty)
        data_penalty = self._clamp_penalty(inp.data_quality_penalty)
        session_penalty = self._clamp_penalty(inp.session_penalty)

        macro_contribution = macro_effect * self.MACRO_WEIGHT
        black_contribution = -(black_penalty * self.BLACK_LAYER_WEIGHT)
        data_contribution = -(data_penalty * self.DATA_QUALITY_WEIGHT)
        session_contribution = -(session_penalty * self.SESSION_WEIGHT)

        raw_score = (
            base
            + macro_contribution
            + black_contribution
            + data_contribution
            + session_contribution
        )

        final_score = self._clamp(raw_score)
        severity = str(inp.black_severity or "CLEAR").upper()

        reasons: list[str] = []

        if inp.black_reasons:
            reasons.extend(inp.black_reasons)

        blocked = severity in {"BLOCK", "KILL"}

        if blocked:
            final_score = 0.0
            reasons.append(f"CRITICAL_SAFETY_BLOCK:{severity}")
            decision_state = DQSDecisionState.BLOCKED.value
            risk_state = DQSRiskState.HIGH.value
        elif severity == "CAUTION":
            decision_state = DQSDecisionState.ACTIVE_CAUTION.value
            risk_state = DQSRiskState.CAUTION.value
            reasons.append("SAFETY_CAUTION")
        else:
            decision_state = DQSDecisionState.ACTIVE.value
            risk_state = DQSRiskState.NORMAL.value

        grade, label = self._grade_from_score(final_score, blocked=blocked)

        breakdown = {
            "base_confidence": base,
            "macro_effect": macro_effect,
            "macro_weight": self.MACRO_WEIGHT,
            "macro_contribution": round(macro_contribution, 4),
            "black_layer_penalty": black_penalty,
            "black_layer_weight": self.BLACK_LAYER_WEIGHT,
            "black_layer_contribution": round(black_contribution, 4),
            "data_quality_penalty": data_penalty,
            "data_quality_contribution": round(data_contribution, 4),
            "session_penalty": session_penalty,
            "session_contribution": round(session_contribution, 4),
            "raw_score": round(raw_score, 4),
            "black_severity": severity,
            "notes": inp.notes,
        }

        return QualityResult(
            final_confidence=round(final_score, 2),
            quality_score=round(final_score, 2),
            grade=grade,
            quality_label=label,
            decision_state=decision_state,
            risk_state=risk_state,
            execution_allowed=False,
            execution_mode="decision_support_only",
            reasons=reasons,
            breakdown=breakdown,
        )


def calculate_total_quality(
    base_confidence: float,
    macro_effect: float = 0.0,
    black_layer_penalty: float = 0.0,
    black_severity: str = "CLEAR",
    black_reasons: list[str] | None = None,
) -> QualityResult:
    """
    Convenience wrapper for tests and simple integrations.
    """
    dqs = DecisionQualityStack()
    return dqs.calculate_total_quality(
        DQSInput(
            base_confidence=base_confidence,
            macro_effect=macro_effect,
            black_layer_penalty=black_layer_penalty,
            black_severity=black_severity,
            black_reasons=black_reasons or [],
        )
    )

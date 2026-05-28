"""
NDSP Layer 13: Decision Quality Stack

Classification:
- INTERNAL CORE ENGINE
- Not for direct public/user exposure

Authority:
- Confidence Authority
- Quality Authority

Allowed Effects:
- Calculate final_confidence
- Calculate grade
- Calculate internal quality label
- Produce confidence_breakdown
- Apply positive/negative quality effects
- Apply protective penalties

Forbidden Effects:
- Must not modify decision.direction
- Must not modify timing authority
- Must not issue execution orders
- Must not expose raw internal terms to public outputs

Public exposure:
- Use sanitize_quality_for_public() before any user-facing output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, float(value)))


@dataclass(frozen=True)
class DecisionQualityWeights:
    """
    Internal Layer 13 weights.

    These are internal-only names. Do not expose these names to public UI.
    """
    golden_alignment: float = 25.0
    weekly_open_gravity: float = 15.0
    momentum_dual: float = 10.0
    macro_alignment: float = 20.0

    conflict_penalty: float = 12.0
    correction_penalty: float = 8.0
    data_degraded_penalty: float = 10.0
    session_degraded_penalty: float = 10.0
    protective_risk_penalty: float = 20.0
    black_layer_danger_penalty: float = 40.0

    max_positive_boost: float = 40.0
    max_total_penalty: float = 70.0


@dataclass
class DecisionQualityResult:
    final_confidence: int
    grade: str
    quality_label: str
    internal_label: str
    confidence_breakdown: Dict[str, Any] = field(default_factory=dict)
    authority: str = "Decision Quality Stack"
    affects_direction: bool = False
    public_safe: bool = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "final_confidence": self.final_confidence,
            "grade": self.grade,
            "quality_label": self.quality_label,
            "internal_label": self.internal_label,
            "confidence_breakdown": self.confidence_breakdown,
            "authority": self.authority,
            "affects_direction": self.affects_direction,
            "public_safe": self.public_safe,
        }


class DecisionQualityStack:
    """
    Layer 13 aggregates quality effects into confidence and grade.

    It does not create or modify direction.
    """

    def __init__(self, weights: DecisionQualityWeights | None = None) -> None:
        self.weights = weights or DecisionQualityWeights()

    def calculate_final_quality(
        self,
        tdl_base_conf: float,
        effects: Mapping[str, Any] | None = None,
    ) -> Dict[str, Any]:
        effects = effects or {}

        base = _clamp(tdl_base_conf)

        positive_effects: Dict[str, float] = {}
        penalties: Dict[str, float] = {}

        if bool(effects.get("golden_alignment_active")):
            positive_effects["golden_alignment"] = self.weights.golden_alignment

        if bool(effects.get("above_weekly_open")) or bool(effects.get("weekly_open_support")):
            positive_effects["weekly_open_gravity"] = self.weights.weekly_open_gravity

        if bool(effects.get("momentum_aligned")):
            positive_effects["momentum_dual"] = self.weights.momentum_dual

        if bool(effects.get("macro_aligned")):
            positive_effects["macro_alignment"] = self.weights.macro_alignment

        if bool(effects.get("participant_conflict")):
            penalties["conflict_penalty"] = self.weights.conflict_penalty

        if bool(effects.get("correction_state")):
            penalties["correction_penalty"] = self.weights.correction_penalty

        if bool(effects.get("data_degraded")):
            penalties["data_degraded_penalty"] = self.weights.data_degraded_penalty

        if bool(effects.get("session_degraded")):
            penalties["session_degraded_penalty"] = self.weights.session_degraded_penalty

        if bool(effects.get("protective_risk")):
            penalties["protective_risk_penalty"] = self.weights.protective_risk_penalty

        if bool(effects.get("black_layer_danger")):
            penalties["black_layer_danger_penalty"] = self.weights.black_layer_danger_penalty

        raw_positive_boost = sum(positive_effects.values())
        raw_penalty = sum(penalties.values())

        positive_boost = min(raw_positive_boost, self.weights.max_positive_boost)
        total_penalty = min(raw_penalty, self.weights.max_total_penalty)

        raw_score = base + positive_boost - total_penalty
        final_confidence = int(round(_clamp(raw_score)))

        grade = self._assign_grade(final_confidence)
        internal_label = self._get_internal_label(grade)
        public_label = self._get_public_label(grade)

        breakdown = {
            "base_confidence": int(round(base)),
            "positive_effects": positive_effects,
            "raw_positive_boost": raw_positive_boost,
            "positive_boost_applied": positive_boost,
            "positive_boost_cap": self.weights.max_positive_boost,
            "penalties": penalties,
            "raw_penalty": raw_penalty,
            "penalty_applied": total_penalty,
            "penalty_cap": self.weights.max_total_penalty,
            "raw_score_before_clamp": raw_score,
            "final_confidence": final_confidence,
            "direction_mutation": False,
        }

        return DecisionQualityResult(
            final_confidence=final_confidence,
            grade=grade,
            quality_label=public_label,
            internal_label=internal_label,
            confidence_breakdown=breakdown,
            public_safe=False,
        ).as_dict()

    @staticmethod
    def _assign_grade(confidence: float) -> str:
        if confidence >= 85:
            return "A"
        if confidence >= 70:
            return "B"
        if confidence >= 55:
            return "C"
        if confidence >= 40:
            return "D"
        return "F"

    @staticmethod
    def _get_internal_label(grade: str) -> str:
        labels = {
            "A": "Internal Strong Quality",
            "B": "Internal High Quality",
            "C": "Internal Moderate Quality",
            "D": "Internal Defensive Quality",
            "F": "Internal Blocked Quality",
        }
        return labels.get(grade, "Internal Unknown Quality")

    @staticmethod
    def _get_public_label(grade: str) -> str:
        labels = {
            "A": "Strong Context Quality",
            "B": "High Context Quality",
            "C": "Moderate Context Quality",
            "D": "Defensive Context Quality",
            "F": "Restricted Context Quality",
        }
        return labels.get(grade, "Unknown Context Quality")


def sanitize_quality_for_public(result: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Public-safe projection.

    Removes internal labels, raw effect names, and internal breakdown details.
    """
    return {
        "final_confidence": int(result.get("final_confidence", 0)),
        "grade": str(result.get("grade", "F")),
        "quality_label": str(result.get("quality_label", "Restricted Context Quality")),
        "public_safe": True,
        "authority": "Quality Assessment",
        "affects_direction": False,
    }


def compute_decision_quality(
    base_confidence: float,
    effects: Mapping[str, Any] | None = None,
    public: bool = False,
) -> Dict[str, Any]:
    stack = DecisionQualityStack()
    result = stack.calculate_final_quality(base_confidence, effects or {})
    if public:
        return sanitize_quality_for_public(result)
    return result


if __name__ == "__main__":
    demo = compute_decision_quality(
        50,
        {
            "golden_alignment_active": True,
            "above_weekly_open": True,
            "momentum_aligned": True,
            "black_layer_danger": False,
        },
        public=False,
    )
    import json
    print(json.dumps(demo, indent=2, ensure_ascii=False))

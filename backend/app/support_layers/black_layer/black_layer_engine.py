"""
NDSP V4.4 risk shield Engine

Purpose:
- Safety valve for unsafe market/data conditions.
- Can block execution/decision state.
- Must never change direction.

Compatibility:
- This package exists at app.core.black_layer.black_layer_engine.
- It is intentionally simple and can coexist with app.core.black_layer_engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class BlackSeverity(Enum):
    CLEAR = 0      # Normal
    CAUTION = 1    # Warning / reduce quality
    BLOCK = 2      # Block this opportunity
    KILL = 3       # Emergency stop / catastrophic condition


class BlackReasonCode(Enum):
    OK = "OK"
    HIGH_SPREAD = "HIGH_SPREAD"
    LOW_LIQUIDITY = "LOW_LIQUIDITY"
    DATA_STALE = "DATA_STALE"
    DATA_MISSING = "DATA_MISSING"
    SOURCE_DISCONNECTED = "SOURCE_DISCONNECTED"
    NEWS_SPIKE = "NEWS_SPIKE"
    MARKET_CLOSED = "MARKET_CLOSED"
    MANUAL_PROTECTIVE_BLOCK = "MANUAL_PROTECTIVE_BLOCK"


@dataclass(frozen=True)
class BlackRule:
    code: BlackReasonCode
    severity: BlackSeverity
    penalty: float
    message: str = ""


class BlackLayerEngine:
    """
    risk shield Safety Engine.

    Rules:
    - CLEAR allows normal decision state.
    - CAUTION allows decision but reduces quality.
    - BLOCK prevents the current opportunity.
    - KILL is strongest and overrides all lower severities.
    """

    def evaluate_spread(self, current_spread: float, avg_spread: float) -> BlackRule:
        if avg_spread <= 0:
            return BlackRule(
                BlackReasonCode.HIGH_SPREAD,
                BlackSeverity.BLOCK,
                1.0,
                "Average spread is invalid; blocking for safety.",
            )

        ratio = current_spread / avg_spread

        if ratio >= 3.0:
            return BlackRule(
                BlackReasonCode.HIGH_SPREAD,
                BlackSeverity.BLOCK,
                1.0,
                "Spread is extremely high.",
            )

        if ratio >= 1.5:
            return BlackRule(
                BlackReasonCode.HIGH_SPREAD,
                BlackSeverity.CAUTION,
                0.35,
                "Spread is elevated.",
            )

        return BlackRule(
            BlackReasonCode.OK,
            BlackSeverity.CLEAR,
            0.0,
            "Spread is acceptable.",
        )

    def evaluate_freshness(self, last_update_seconds: int) -> BlackRule:
        if last_update_seconds < 0:
            return BlackRule(
                BlackReasonCode.DATA_STALE,
                BlackSeverity.BLOCK,
                1.0,
                "Invalid negative freshness value.",
            )

        if last_update_seconds > 60:
            return BlackRule(
                BlackReasonCode.DATA_STALE,
                BlackSeverity.KILL,
                1.0,
                "Data is stale for more than 60 seconds.",
            )

        if last_update_seconds > 15:
            return BlackRule(
                BlackReasonCode.DATA_STALE,
                BlackSeverity.CAUTION,
                0.35,
                "Data freshness is degraded.",
            )

        return BlackRule(
            BlackReasonCode.OK,
            BlackSeverity.CLEAR,
            0.0,
            "Data freshness is acceptable.",
        )

    def evaluate_liquidity(self, liquidity_state: str) -> BlackRule:
        normalized = (liquidity_state or "").strip().lower()

        if normalized in {"low", "weak", "degraded"}:
            return BlackRule(
                BlackReasonCode.LOW_LIQUIDITY,
                BlackSeverity.CAUTION,
                0.35,
                "Liquidity is weak.",
            )

        if normalized in {"none", "halted", "closed"}:
            return BlackRule(
                BlackReasonCode.LOW_LIQUIDITY,
                BlackSeverity.BLOCK,
                1.0,
                "Liquidity is not acceptable.",
            )

        return BlackRule(
            BlackReasonCode.OK,
            BlackSeverity.CLEAR,
            0.0,
            "Liquidity is acceptable.",
        )

    def evaluate_session(self, session_state: str) -> BlackRule:
        normalized = (session_state or "").strip().lower()

        if normalized in {"closed", "market_closed", "closed_or_low_liquidity_review"}:
            return BlackRule(
                BlackReasonCode.MARKET_CLOSED,
                BlackSeverity.BLOCK,
                1.0,
                "Market session is closed or unsafe.",
            )

        if normalized in {"unsafe", "halt", "break", "suspended"}:
            return BlackRule(
                BlackReasonCode.MARKET_CLOSED,
                BlackSeverity.BLOCK,
                1.0,
                "Market session is unsafe.",
            )

        return BlackRule(
            BlackReasonCode.OK,
            BlackSeverity.CLEAR,
            0.0,
            "Market session is acceptable.",
        )

    def evaluate_manual_block(self, active: bool) -> BlackRule:
        if active:
            return BlackRule(
                BlackReasonCode.MANUAL_PROTECTIVE_BLOCK,
                BlackSeverity.KILL,
                1.0,
                "Manual protective block is active.",
            )

        return BlackRule(
            BlackReasonCode.OK,
            BlackSeverity.CLEAR,
            0.0,
            "No manual protective block.",
        )

    def get_final_safety_state(self, rules: list[BlackRule]) -> dict[str, Any]:
        """
        Aggregate rules into final safety state.

        Severity-first:
        KILL > BLOCK > CAUTION > CLEAR

        Penalty:
        max normalized penalty, not sum, to avoid double-counting.
        """

        if not rules:
            rules = [BlackRule(BlackReasonCode.OK, BlackSeverity.CLEAR, 0.0, "No rules supplied.")]

        max_rule = max(rules, key=lambda rule: rule.severity.value)

        active_rules = [rule for rule in rules if rule.severity != BlackSeverity.CLEAR]
        active_reasons = [rule.code.value for rule in active_rules]
        messages = [rule.message for rule in active_rules if rule.message]

        penalty = max((rule.penalty for rule in active_rules), default=0.0)
        penalty = max(0.0, min(1.0, float(penalty)))

        can_execute = max_rule.severity.value < BlackSeverity.BLOCK.value

        if max_rule.severity == BlackSeverity.KILL:
            decision_state = "blocked"
            risk_state = "high"
        elif max_rule.severity == BlackSeverity.BLOCK:
            decision_state = "blocked"
            risk_state = "high"
        elif max_rule.severity == BlackSeverity.CAUTION:
            decision_state = "active_caution"
            risk_state = "caution"
        else:
            decision_state = "active"
            risk_state = "normal"

        return {
            "severity": max_rule.severity.name,
            "can_execute": can_execute,
            "active_reasons": active_reasons,
            "penalty": penalty,
            "decision_state": decision_state,
            "risk_state": risk_state,
            "messages": messages,
        }


def black_layer_quality_effect_from_state(state: dict[str, Any]) -> dict[str, float]:
    """
    Convert final safety state into DQS normalized effect.

    CLEAR   => 0.0
    CAUTION => 0.35
    BLOCK   => 1.0
    KILL    => 1.0
    """

    severity = str(state.get("severity", "CLEAR")).upper()

    if severity == "CLEAR":
        return {"black_layer_penalty": 0.0}

    if severity == "CAUTION":
        return {"black_layer_penalty": 0.35}

    return {"black_layer_penalty": 1.0}

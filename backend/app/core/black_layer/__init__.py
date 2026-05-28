"""
NDSP Layer 12: risk shield

Authority:
- Risk Escalation Authority.

Allowed effects:
- confidence_penalty
- risk_penalty
- risk_state escalation
- protective block / blocked state

Forbidden effects:
- Must not calculate or mutate decision.direction.
- Must not enable execution.
- Must not expose raw sensitive internals to public output.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping


class BlackLayerEvaluator:
    """
    Layer 12: Risk escalation and protective blocking.
    """

    SEVERITY_ORDER = {
        "clear": 0,
        "caution": 1,
        "elevated_risk": 2,
        "blocked": 3,
    }

    SEVERITY_LADDER = {
        "CLEAR": {
            "state": "clear",
            "risk_state": "normal",
            "confidence_penalty": 0,
            "risk_penalty": 0,
            "blocked": False,
        },
        "CAUTION": {
            "state": "caution",
            "risk_state": "caution",
            "confidence_penalty": 25,
            "risk_penalty": 30,
            "blocked": False,
        },
        "ELEVATED_RISK": {
            "state": "elevated_risk",
            "risk_state": "elevated_risk",
            "confidence_penalty": 50,
            "risk_penalty": 60,
            "blocked": False,
        },
        "PROTECTIVE_BLOCK": {
            "state": "blocked",
            "risk_state": "blocked",
            "confidence_penalty": 100,
            "risk_penalty": 100,
            "blocked": True,
        },
    }

    TRIGGER_MATRIX = {
        "extreme_volatility_spike": "CAUTION",
        "unstable_volatility": "CAUTION",
        "zone_pressure": "CAUTION",
        "momentum_context_weak": "CAUTION",

        "liquidity_vacuum": "ELEVATED_RISK",
        "liquidity_event_detected": "ELEVATED_RISK",
        "macro_news_embargo": "ELEVATED_RISK",
        "feed_degraded": "ELEVATED_RISK",

        "flash_crash_signature": "PROTECTIVE_BLOCK",
        "data_feed_stale": "PROTECTIVE_BLOCK",
        "session_closed": "PROTECTIVE_BLOCK",
        "execution_safety_violation": "PROTECTIVE_BLOCK",
    }

    @classmethod
    def evaluate_by_triggers(cls, detected_anomalies: Iterable[str] | None = None) -> Dict[str, Any]:
        anomalies = [str(x) for x in (detected_anomalies or []) if x]

        highest_key = "CLEAR"
        active_triggers: List[str] = []

        for anomaly in anomalies:
            severity_key = cls.TRIGGER_MATRIX.get(anomaly, "CLEAR")
            if severity_key == "CLEAR":
                continue

            active_triggers.append(anomaly)

            current_state = cls.SEVERITY_LADDER[highest_key]["state"]
            next_state = cls.SEVERITY_LADDER[severity_key]["state"]

            if cls.SEVERITY_ORDER[next_state] > cls.SEVERITY_ORDER[current_state]:
                highest_key = severity_key

        ladder = cls.SEVERITY_LADDER[highest_key]

        return {
            "black_layer_state": ladder["state"],
            "state": ladder["state"],
            "risk_state": ladder["risk_state"],
            "confidence_penalty": ladder["confidence_penalty"],
            "black_layer_penalty": ladder["confidence_penalty"],
            "risk_penalty": ladder["risk_penalty"],
            "blocked": ladder["blocked"],
            "active_triggers": active_triggers,
            "affects_direction": False,
            "execution_allowed": False,
            "execution_mode": "decision_support_only",
            "authority": "risk_escalation_only",
            "public_safe": True,
        }

    @classmethod
    def evaluate_context(
        cls,
        momentum: Any = None,
        liquidity: Any = None,
        volatility: Any = None,
        zones: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        triggers: List[str] = []

        volatility_state = _read_state(volatility)
        liquidity_state = _read_state(liquidity)
        zones_state = _read_state(zones)
        momentum_state = _read_state(momentum)

        if volatility_state in {"high", "spike", "unstable", "extreme"}:
            triggers.append("unstable_volatility")

        if liquidity_state in {"sweep_up", "sweep_down", "low", "thin", "unstable", "vacuum"}:
            triggers.append("liquidity_event_detected")

        if zones_state in {"resistance", "support", "pressure", "rejection"}:
            triggers.append("zone_pressure")

        if momentum_state in {"weak", "divergent", "conflicted"}:
            triggers.append("momentum_context_weak")

        if _truthy(kwargs.get("data_feed_stale")):
            triggers.append("data_feed_stale")

        if _truthy(kwargs.get("session_closed")):
            triggers.append("session_closed")

        if _truthy(kwargs.get("flash_crash_signature")):
            triggers.append("flash_crash_signature")

        if _truthy(kwargs.get("macro_news_embargo")):
            triggers.append("macro_news_embargo")

        return cls.evaluate_by_triggers(triggers)


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on", "active"}
    return bool(value)


def _read_state(value: Any, default: str = "normal") -> str:
    if isinstance(value, Mapping):
        raw = value.get("state") or value.get("risk_state") or value.get("status") or value.get("signal")
        if raw is not None:
            return str(raw).lower()
        return default

    if value is None:
        return default

    return str(value).lower()


def evaluate_black_layer(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Compatibility entrypoint used by governed_pipeline.

    Supported calls:
    - evaluate_black_layer(["flash_crash_signature"])
    - evaluate_black_layer(momentum={...}, liquidity={...}, volatility={...}, zones={...})
    - evaluate_black_layer(momentum, liquidity, volatility, zones)
    """
    if args and len(args) == 1 and isinstance(args[0], (list, tuple, set)):
        return BlackLayerEvaluator.evaluate_by_triggers(args[0])

    if args and len(args) >= 4:
        return BlackLayerEvaluator.evaluate_context(
            momentum=args[0],
            liquidity=args[1],
            volatility=args[2],
            zones=args[3],
            **kwargs,
        )

    if "detected_anomalies" in kwargs:
        return BlackLayerEvaluator.evaluate_by_triggers(kwargs.get("detected_anomalies"))

    return BlackLayerEvaluator.evaluate_context(**kwargs)


__all__ = [
    "BlackLayerEvaluator",
    "evaluate_black_layer",
]

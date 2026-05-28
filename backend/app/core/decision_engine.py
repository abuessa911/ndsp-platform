"""
NDSP Layer 15: Final Decision Aggregator

Authority:
- Aggregation Authority only.

Law:
- Final Decision does not think.
- Final Decision aggregates.
- It must not calculate direction.
- It must not calculate confidence.
- It must not raise or lower risk.
- It must not enable execution.

Compatibility:
- Exposes run_decision(...) for governed_pipeline imports.
- Exposes FinalDecisionAggregator for strict upstream aggregation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional


PROTECTED_EXECUTION_ALLOWED = False
PROTECTED_EXECUTION_MODE = "decision_support_only"


@dataclass
class NDSPDecisionContract:
    trace_id: str
    symbol: str
    timestamp: str
    session_state: str
    dominant_direction: str
    direction_source: str
    timing_controller: str
    confidence_score: float
    grade: str
    quality_label: str
    applied_effects: list = field(default_factory=list)
    risk_state: str = "normal"
    decision_state: str = "review_only"
    execution_allowed: bool = False
    execution_mode: str = PROTECTED_EXECUTION_MODE
    source_mode: str = "http_decision"

    def model_dump(self) -> Dict[str, Any]:
        return asdict(self)

    def dict(self) -> Dict[str, Any]:
        return asdict(self)


def _safe_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return deepcopy(payload)
    if hasattr(payload, "model_dump"):
        try:
            data = payload.model_dump()
            return deepcopy(data) if isinstance(data, dict) else {}
        except Exception:
            return {}
    if hasattr(payload, "dict"):
        try:
            data = payload.dict()
            return deepcopy(data) if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def _read_mapping(data: Mapping[str, Any], *keys: str) -> Dict[str, Any]:
    for key in keys:
        value = data.get(key)
        if isinstance(value, Mapping):
            return dict(value)
    return {}


def _first(data: Mapping[str, Any], keys: list[str], default: Any) -> Any:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return value
    return default


class FinalDecisionAggregator:
    """
    Layer 15 Aggregator.

    This class only maps upstream outputs into the final decision contract.
    """

    @staticmethod
    def build_decision(
        trace_id: str,
        symbol: str,
        dominant_direction_data: Mapping[str, Any],
        quality_data: Mapping[str, Any],
        risk_data: Mapping[str, Any],
        governance_data: Mapping[str, Any],
    ) -> NDSPDecisionContract:
        return NDSPDecisionContract(
            trace_id=str(trace_id),
            symbol=str(symbol).upper(),
            timestamp=str(
                governance_data.get("timestamp")
                or datetime.now(timezone.utc).isoformat()
            ),
            session_state=str(risk_data.get("session_state", "unknown")),
            dominant_direction=str(dominant_direction_data.get("direction", "neutral")),
            direction_source=str(dominant_direction_data.get("source", "unknown")),
            timing_controller=str(
                dominant_direction_data.get("controller")
                or dominant_direction_data.get("timing_controller")
                or "unknown"
            ),
            confidence_score=float(quality_data.get("final_confidence", quality_data.get("confidence", 0.0))),
            grade=str(quality_data.get("grade", "F")),
            quality_label=str(quality_data.get("quality_label", "Restricted Context Quality")),
            applied_effects=list(quality_data.get("applied_effects", [])),
            risk_state=str(risk_data.get("risk_state", "normal")),
            decision_state=str(governance_data.get("decision_state", "review_only")),
            execution_allowed=PROTECTED_EXECUTION_ALLOWED,
            execution_mode=PROTECTED_EXECUTION_MODE,
            source_mode=str(governance_data.get("source_mode", "http_decision")),
        )


def contract_to_runtime_dict(contract: NDSPDecisionContract) -> Dict[str, Any]:
    raw = contract.model_dump()

    return {
        "ok": True,
        "system": "NDSP",
        "source": "layer15_final_decision_aggregator",
        "timestamp": raw["timestamp"],
        "symbol": raw["symbol"],
        "decision": {
            "direction": raw["dominant_direction"],
            "direction_source": raw["direction_source"],
            "timing_controller": raw["timing_controller"],
            "confidence": int(round(float(raw["confidence_score"]))),
            "confidence_score": raw["confidence_score"],
            "grade": raw["grade"],
            "quality_label": raw["quality_label"],
            "risk_state": raw["risk_state"],
            "decision_state": raw["decision_state"],
            "execution_allowed": False,
            "execution_mode": PROTECTED_EXECUTION_MODE,
        },
        "governance": {
            "decision_support_only": True,
            "direct_execution": False,
            "execution_allowed": False,
            "execution_mode": PROTECTED_EXECUTION_MODE,
            "source_mode": raw["source_mode"],
            "public_safe": True,
        },
    }


def run_decision(payload: Any = None, symbol: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
    """
    Compatibility wrapper for governed_pipeline.

    It does not calculate. It extracts already-produced upstream fields and aggregates them.
    """
    data = _safe_payload(payload)

    if kwargs:
        for key, value in kwargs.items():
            data.setdefault(key, value)

    nested_decision = _read_mapping(data, "decision")
    dominant_direction_data = _read_mapping(
        data,
        "dominant_direction_data",
        "dominant_direction",
        "direction_data",
        "direction",
    )
    quality_data = _read_mapping(
        data,
        "quality_data",
        "decision_quality",
        "quality",
        "layer13",
    )
    risk_data = _read_mapping(
        data,
        "risk_data",
        "risk",
        "risk_context",
    )
    governance_data = _read_mapping(
        data,
        "governance_data",
        "governance",
    )

    if not dominant_direction_data:
        dominant_direction_data = {
            "direction": _first(
                nested_decision or data,
                ["direction", "dominant_direction", "decision_direction"],
                "neutral",
            ),
            "source": _first(
                nested_decision or data,
                ["direction_source", "source"],
                "unknown",
            ),
            "controller": _first(
                nested_decision or data,
                ["timing_controller", "controller", "decision_authority"],
                "unknown",
            ),
        }

    if not quality_data:
        quality_data = {
            "final_confidence": _first(
                nested_decision or data,
                ["confidence", "final_confidence", "confidence_score"],
                0.0,
            ),
            "grade": _first(nested_decision or data, ["grade"], "F"),
            "quality_label": _first(
                nested_decision or data,
                ["quality_label"],
                "Restricted Context Quality",
            ),
            "applied_effects": data.get("applied_effects", []),
        }

    if not risk_data:
        risk_data = {
            "risk_state": _first(nested_decision or data, ["risk_state"], "normal"),
            "session_state": _first(data, ["session_state"], "unknown"),
        }

    if not governance_data:
        governance_data = {
            "decision_state": _first(nested_decision or data, ["decision_state"], "review_only"),
            "execution_allowed": False,
            "execution_mode": PROTECTED_EXECUTION_MODE,
            "source_mode": _first(data, ["source_mode"], "http_decision"),
        }

    resolved_symbol = str(symbol or data.get("symbol") or nested_decision.get("symbol") or "UNKNOWN").upper()
    trace_id = str(data.get("trace_id") or data.get("contract_id") or "NDSP-L15-RUNTIME")

    contract = FinalDecisionAggregator.build_decision(
        trace_id=trace_id,
        symbol=resolved_symbol,
        dominant_direction_data=dominant_direction_data,
        quality_data=quality_data,
        risk_data=risk_data,
        governance_data=governance_data,
    )

    result = contract_to_runtime_dict(contract)

    # Optional public-safe Layer 13 adapter can normalize quality output, but must not mutate protected fields.
    try:
        from app.core.layer13_runtime_adapter import enrich_decision_contract_with_layer13  # type: ignore

        enriched = enrich_decision_contract_with_layer13(result, public=True)
        if isinstance(enriched, dict):
            decision = enriched.setdefault("decision", {})
            if isinstance(decision, dict):
                decision["execution_allowed"] = False
                decision["execution_mode"] = PROTECTED_EXECUTION_MODE
            governance = enriched.setdefault("governance", {})
            if isinstance(governance, dict):
                governance["decision_support_only"] = True
                governance["direct_execution"] = False
                governance["execution_allowed"] = False
                governance["execution_mode"] = PROTECTED_EXECUTION_MODE
            return _ndsp_ensure_decision_risk_state(enriched)
    except Exception:
        pass

    return _ndsp_ensure_decision_risk_state(result)


def decide(payload: Any = None, **kwargs: Any) -> Dict[str, Any]:
    return run_decision(payload, **kwargs)


def build_decision(payload: Any = None, **kwargs: Any) -> Dict[str, Any]:
    return run_decision(payload, **kwargs)


if __name__ == "__main__":
    import json
    demo = run_decision({
        "symbol": "BTCUSDT",
        "dominant_direction_data": {"direction": "bullish", "source": "Weekly_LM", "controller": "L&M"},
        "quality_data": {"final_confidence": 88.5, "grade": "A", "quality_label": "Strong Context Quality"},
        "risk_data": {"risk_state": "normal", "session_state": "open"},
        "governance_data": {"decision_state": "active", "execution_allowed": False},
    })
    print(json.dumps(demo, indent=2, ensure_ascii=False))

# NDSP runtime safety fallback: public decision must always carry risk_state.

def _ndsp_ensure_decision_risk_state(contract):
    try:
        if isinstance(contract, dict):
            decision = contract.setdefault("decision", {})
            if isinstance(decision, dict):
                if not decision.get("risk_state"):
                    risk_state = None
                    risk = contract.get("risk")
                    governance = contract.get("governance")
                    if isinstance(risk, dict):
                        risk_state = risk.get("risk_state") or risk.get("state")
                    if isinstance(governance, dict):
                        risk_state = risk_state or governance.get("risk_state")
                    decision["risk_state"] = str(risk_state or "normal").lower()

                decision["execution_allowed"] = False
                decision["execution_mode"] = "decision_support_only"

            governance = contract.setdefault("governance", {})
            if isinstance(governance, dict):
                governance["decision_support_only"] = True
                governance["direct_execution"] = False
                governance["execution_allowed"] = False
                governance["execution_mode"] = "decision_support_only"
    except Exception:
        pass
    return contract

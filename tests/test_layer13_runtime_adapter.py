#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path("/home/nawaf511/empire-core-new")
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.core.layer13_runtime_adapter import enrich_decision_contract_with_layer13


def assert_true(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"{name}=True")


def main():
    contract = {
        "symbol": "BTCUSDT",
        "decision": {
            "direction": "bullish",
            "timing_controller": "L&M",
            "risk_state": "normal",
            "decision_state": "active",
            "execution_allowed": False,
            "execution_mode": "decision_support_only",
            "confidence": 50,
        },
        "quality_context": {
            "golden_alignment_active": True,
            "above_weekly_open": True,
            "momentum_aligned": True,
        },
    }

    original_decision = dict(contract["decision"])

    enriched = enrich_decision_contract_with_layer13(contract, public=True)
    decision = enriched["decision"]

    for key in (
        "direction",
        "timing_controller",
        "risk_state",
        "decision_state",
        "execution_allowed",
        "execution_mode",
    ):
        assert_true(f"PRESERVED_{key.upper()}", decision[key] == original_decision[key])

    assert_true("CONFIDENCE_ADDED", isinstance(decision.get("confidence"), int))
    assert_true("GRADE_ADDED", decision.get("grade") in {"A", "B", "C", "D", "F"})
    assert_true("QUALITY_LABEL_ADDED", isinstance(decision.get("quality_label"), str))
    assert_true("LAYER13_BOUND_TRUE", decision.get("layer13_bound") is True)

    public_json = json.dumps(enriched, ensure_ascii=False).lower()
    forbidden_public_terms = [
        "golden_alignment",
        "weekly_open_gravity",
        "black_layer",
        "tdl",
        "raw_score",
        "weights",
        "confidence_breakdown",
        "internal_label",
    ]

    # quality_context is internal in this synthetic test. The adapter itself
    # should not add forbidden terms into the decision object.
    decision_json = json.dumps(decision, ensure_ascii=False).lower()
    hits = [x for x in forbidden_public_terms if x in decision_json]
    assert_true("DECISION_PUBLIC_SAFE_NO_FORBIDDEN_TERMS", hits == [])

    blocked = {
        "decision": {
            "direction": "bearish",
            "timing_controller": "S",
            "risk_state": "blocked",
            "decision_state": "blocked",
            "execution_allowed": False,
            "execution_mode": "decision_support_only",
            "confidence": 80,
        },
        "risk": {"black_layer_danger": True},
    }

    blocked_enriched = enrich_decision_contract_with_layer13(blocked, public=True)
    bdec = blocked_enriched["decision"]

    assert_true("BLOCKED_DIRECTION_PRESERVED", bdec["direction"] == "bearish")
    assert_true("BLOCKED_EXECUTION_PRESERVED", bdec["execution_allowed"] is False)
    assert_true("BLOCKED_RISK_PRESERVED", bdec["risk_state"] == "blocked")
    assert_true("BLOCKED_CONFIDENCE_REDUCED_OR_CAPPED", bdec["confidence"] <= 80)

    print("FINAL_STATUS=TEST_LAYER13_RUNTIME_ADAPTER_DONE")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path("/home/nawaf511/empire-core-new")
BACKEND = ROOT / "backend"

sys.path.insert(0, str(BACKEND))

from app.core.decision_quality_stack import (
    DecisionQualityStack,
    compute_decision_quality,
    sanitize_quality_for_public,
)


def assert_true(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"{name}=True")


def main():
    stack = DecisionQualityStack()

    baseline = stack.calculate_final_quality(50, {})
    assert_true("BASELINE_CONFIDENCE_OK", baseline["final_confidence"] == 50)
    assert_true("BASELINE_DOES_NOT_AFFECT_DIRECTION", baseline["affects_direction"] is False)

    boosted = stack.calculate_final_quality(
        50,
        {
            "golden_alignment_active": True,
            "above_weekly_open": True,
            "momentum_aligned": True,
            "macro_aligned": True,
        },
    )

    assert_true("BOOSTED_CAPPED_OK", boosted["final_confidence"] == 90)
    assert_true("BOOST_CAP_OK", boosted["confidence_breakdown"]["positive_boost_applied"] == 40.0)
    assert_true("BOOST_GRADE_OK", boosted["grade"] == "A")

    danger = stack.calculate_final_quality(
        50,
        {
            "golden_alignment_active": True,
            "above_weekly_open": True,
            "black_layer_danger": True,
            "protective_risk": True,
            "participant_conflict": True,
        },
    )

    assert_true("DANGER_PENALTY_OK", danger["final_confidence"] <= 40)
    assert_true("DANGER_DIRECTION_NOT_MUTATED", danger["confidence_breakdown"]["direction_mutation"] is False)

    public = sanitize_quality_for_public(boosted)
    public_json = json.dumps(public, ensure_ascii=False).lower()

    forbidden = [
        "golden_alignment",
        "weekly_open_gravity",
        "black_layer",
        "tdl",
        "weights",
        "raw_score",
        "internal_label",
        "confidence_breakdown",
    ]

    hits = [x for x in forbidden if x in public_json]
    assert_true("PUBLIC_SANITIZED_NO_FORBIDDEN_TERMS", hits == [])
    assert_true("PUBLIC_SAFE_TRUE", public["public_safe"] is True)
    assert_true("PUBLIC_AUTHORITY_GENERALIZED", public["authority"] == "Quality Assessment")

    wrapper_internal = compute_decision_quality(50, {"golden_alignment_active": True}, public=False)
    wrapper_public = compute_decision_quality(50, {"golden_alignment_active": True}, public=True)

    assert_true("WRAPPER_INTERNAL_OK", "confidence_breakdown" in wrapper_internal)
    assert_true("WRAPPER_PUBLIC_OK", "confidence_breakdown" not in wrapper_public)

    print("FINAL_STATUS=TEST_LAYER13_DECISION_QUALITY_STACK_DONE")


if __name__ == "__main__":
    main()

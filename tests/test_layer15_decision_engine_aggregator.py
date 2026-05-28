#!/usr/bin/env python3
from app.core.decision_engine import FinalDecisionAggregator, run_decision

def assert_true(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"{name}=True")

def main():
    dom_dir = {"direction": "bullish", "source": "Weekly_LM", "controller": "L&M"}
    qual_data = {"final_confidence": 88.5, "grade": "A", "quality_label": "Strong Context Quality", "applied_effects": ["Golden_Alignment"]}
    risk_data = {"session_state": "open", "risk_state": "normal"}
    gov_data = {"decision_state": "active", "execution_allowed": True, "source_mode": "http_decision"}

    contract = FinalDecisionAggregator.build_decision(
        trace_id="TRC-999",
        symbol="BTCUSDT",
        dominant_direction_data=dom_dir,
        quality_data=qual_data,
        risk_data=risk_data,
        governance_data=gov_data,
    )

    assert_true("NO_MUTATION_DIRECTION_OK", contract.dominant_direction == "bullish")
    assert_true("NO_MUTATION_CONFIDENCE_OK", contract.confidence_score == 88.5)
    assert_true("NO_EXECUTION_ESCALATION_OK", contract.execution_allowed is False)
    assert_true("EXECUTION_MODE_LOCKED_OK", contract.execution_mode == "decision_support_only")

    result = run_decision({
        "symbol": "BTCUSDT",
        "dominant_direction_data": dom_dir,
        "quality_data": qual_data,
        "risk_data": risk_data,
        "governance_data": gov_data,
    })

    d = result["decision"]

    for field in [
        "confidence",
        "grade",
        "quality_label",
        "direction",
        "timing_controller",
        "risk_state",
        "execution_allowed",
        "execution_mode",
    ]:
        assert_true(f"RUNTIME_HAS_{field.upper()}", field in d)

    assert_true("RUNTIME_DIRECTION_PRESERVED", d["direction"] == "bullish")
    assert_true("RUNTIME_TIMING_PRESERVED", d["timing_controller"] == "L&M")
    assert_true("RUNTIME_EXECUTION_FALSE", d["execution_allowed"] is False)
    assert_true("RUNTIME_EXECUTION_MODE_LOCKED", d["execution_mode"] == "decision_support_only")

    public_text = str(result).lower()
    assert_true("PUBLIC_HIDES_WEEKLY_OPEN_GRAVITY", "weekly_open_gravity" not in public_text)
    assert_true("PUBLIC_HIDES_CONFIDENCE_BREAKDOWN", "confidence_breakdown" not in public_text)

    print("FINAL_STATUS=TEST_LAYER15_DECISION_ENGINE_AGGREGATOR_DONE")

if __name__ == "__main__":
    main()

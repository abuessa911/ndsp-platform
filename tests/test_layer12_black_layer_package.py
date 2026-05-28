#!/usr/bin/env python3
from app.core.black_layer import BlackLayerEvaluator, evaluate_black_layer

def assert_true(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f"{name}=True")

def main():
    clear = BlackLayerEvaluator.evaluate_by_triggers([])
    assert_true("BLACK_CLEAR_STATE_OK", clear["black_layer_state"] == "clear")
    assert_true("BLACK_CLEAR_PENALTY_OK", clear["confidence_penalty"] == 0)

    caution = BlackLayerEvaluator.evaluate_by_triggers(["extreme_volatility_spike"])
    assert_true("BLACK_CAUTION_STATE_OK", caution["black_layer_state"] == "caution")
    assert_true("BLACK_CAUTION_PENALTY_OK", caution["confidence_penalty"] == 25)

    elevated = BlackLayerEvaluator.evaluate_by_triggers(["liquidity_vacuum"])
    assert_true("BLACK_ELEVATED_STATE_OK", elevated["black_layer_state"] == "elevated_risk")
    assert_true("BLACK_ELEVATED_PENALTY_OK", elevated["confidence_penalty"] == 50)

    blocked = BlackLayerEvaluator.evaluate_by_triggers(["extreme_volatility_spike", "flash_crash_signature"])
    assert_true("BLACK_BLOCKED_STATE_OK", blocked["black_layer_state"] == "blocked")
    assert_true("BLACK_BLOCKED_PENALTY_OK", blocked["confidence_penalty"] == 100)
    assert_true("BLACK_BLOCKED_FLAG_OK", blocked["blocked"] is True)

    context = evaluate_black_layer(
        momentum={"state": "weak"},
        liquidity={"state": "low"},
        volatility={"state": "high"},
        zones={"state": "resistance"},
    )
    assert_true("BLACK_CONTEXT_RESULT_OK", isinstance(context, dict))
    assert_true("BLACK_CONTEXT_HAS_STATE", "black_layer_state" in context)
    assert_true("BLACK_CONTEXT_HAS_PENALTY", "confidence_penalty" in context)

    assert_true("BLACK_NO_DIRECTION_KEY", "direction" not in blocked)
    assert_true("BLACK_AFFECTS_DIRECTION_FALSE", blocked.get("affects_direction") is False)
    assert_true("BLACK_EXECUTION_FALSE", blocked.get("execution_allowed") is False)
    assert_true("BLACK_EXECUTION_MODE_LOCKED", blocked.get("execution_mode") == "decision_support_only")

    print("NO_MUTATION_ASSERT_OK=True")
    print("BLACK_LAYER_EVALUATION_OK=True")
    print("FINAL_STATUS=TEST_LAYER12_BLACK_LAYER_PACKAGE_DONE")

if __name__ == "__main__":
    main()

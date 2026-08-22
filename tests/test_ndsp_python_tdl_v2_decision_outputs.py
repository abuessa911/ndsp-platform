#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path("/home/nawaf511/empire-core-new")
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.ndsp_governance.decision_output_policy import (
    build_tdl_v2_context,
    contains_forbidden_public_terms,
    govern_decision_output,
)

def assert_safe(obj):
    text = json.dumps(obj, ensure_ascii=False, default=str)
    assert not contains_forbidden_public_terms(text), text

swing_exposed_payload = {
    "ok": True,
    "symbol": "BTCUSDT",
    "market": "crypto",
    "timeframe": "1h",
    "package": "elite",
    "direction": "bullish",
    "lm_direction": "UPWARD",
    "s_direction": "UPWARD",
    "side_relation": "DIFFERENT",
    "entry": 101000,
    "tp": 104000,
    "sl": 99000,
    "summary": "BUY NOW entry take profit stop loss",
    "raw_formula": "secret",
    "internal_weights": {"hidden": 1},
    "contract_sum": 123,
    "order": {"side": "buy"},
}

out1 = govern_decision_output(swing_exposed_payload, package="elite")
assert out1["source_mode"] == "python_decision_governed_tdl_v2"
assert out1["governance"]["DIRECT_TRADE_EXECUTION"] is False
assert out1["governance"]["PUBLIC_OUTPUT_SANITIZED"] is True
assert out1["governance"]["RAW_LOGIC_EXPOSED"] is False
assert out1["scenario"]["scenario_directional_context_code"] == "UPWARD_CONTEXT"
assert out1["scenario"]["scenario_activation_level"] == 101000
assert out1["scenario"]["scenario_arrival_level"] == 104000
assert out1["scenario"]["scenario_invalidation_level"] == 99000
assert out1["scenario"]["tdl_follow_style"] == "EXTENDED_MONITORING"
assert out1["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert out1["scenario"]["tdl_direction_exposure"] == "EXPOSED_CLEARER"
assert out1["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert out1["scenario"]["tdl_direction_clarity"] == "أوضح"
assert out1["scenario"]["tdl_strength_label"] == "الأفق ممتد"
assert out1["tdl_v2_context"]["layer_name"] == "TDL"
assert_safe(out1)

short_non_explicit_payload = {
    "ok": True,
    "symbol": "XAUUSD",
    "market": "metals",
    "timeframe": "4h",
    "package": "pro",
    "direction": "bearish",
    "lm_direction": "UPWARD",
    "s_direction": "DOWNWARD",
    "side_relation": "SIMILAR",
    "activation_level": 2350,
    "arrival_level": 2320,
    "invalidation_level": 2365,
}

out2 = govern_decision_output(short_non_explicit_payload, package="pro")
assert out2["scenario"]["scenario_directional_context_code"] == "DOWNWARD_CONTEXT"
assert out2["scenario"]["tdl_follow_style"] == "SHORT_MONITORING"
assert out2["scenario"]["tdl_follow_style_label"] == "أفق متابعة قصير"
assert out2["scenario"]["tdl_direction_exposure"] == "NON_EXPLICIT"
assert out2["scenario"]["tdl_direction_exposure_label"] == "الاتجاه غير صريح"
assert out2["scenario"]["tdl_direction_clarity"] == "غير صريح"
assert out2["scenario"]["tdl_strength_label"] == "الأفق قصير"
assert out2["tdl_v2_context"]["layer_name"] == "TDL"
assert_safe(out2)

free_payload = {
    "ok": True,
    "symbol": "ETHUSDT",
    "market": "crypto",
    "timeframe": "1h",
    "package": "free",
    "lm_direction": "UPWARD",
    "s_direction": "UPWARD",
    "side_relation": "DIFFERENT",
}

out3 = govern_decision_output(free_payload, package="free")
assert out3["tdl_v2_context"]["layer_name_visible"] is False
assert out3["tdl_v2_context"]["layer_name"] is None
assert out3["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert out3["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert_safe(out3)

ctx = build_tdl_v2_context({
    "lm_direction": "UPWARD",
    "s_direction": "DOWNWARD",
    "buy_side_sign": "+",
    "sell_side_sign": "+",
}, package="elite")
assert ctx["tdl_follow_style_label"] == "أفق متابعة قصير"
assert ctx["tdl_direction_exposure_label"] == "الاتجاه غير صريح"
assert_safe(ctx)

print("SOURCE_MODE=python_decision_governed_tdl_v2")
print("TDL_FOLLOW_STYLE_EXTENDED_MONITORING=True")
print("TDL_FOLLOW_STYLE_SHORT_MONITORING=True")
print("TDL_DIRECTION_EXPOSURE_EXPOSED_CLEARER=True")
print("TDL_DIRECTION_EXPOSURE_NON_EXPLICIT=True")
print("SCENARIO_REFERENCE_LEVELS=True")
print("PUBLIC_OUTPUT_SANITIZED=True")
print("DIRECT_TRADE_EXECUTION=False")
print("RAW_LOGIC_EXPOSED=False")
print("ASSERT_OK=True")
print("FINAL_STATUS=NDSP_PYTHON_TDL_V2_DECISION_OUTPUTS_TEST_OK")

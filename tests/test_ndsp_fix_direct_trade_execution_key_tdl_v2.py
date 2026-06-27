#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path("/home/nawaf511/empire-core-new")
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.ndsp_governance.decision_output_policy import (
    contains_forbidden_public_terms,
    govern_decision_output,
)

def assert_safe(obj):
    text = json.dumps(obj, ensure_ascii=False, default=str)
    assert not contains_forbidden_public_terms(text), text

payload = {
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

out = govern_decision_output(payload, package="elite")

assert out["governance"]["MODE"] == "DECISION_ACTIVE"
assert out["governance"]["EXECUTION_POLICY"] == "EXECUTION_SANITIZED"
assert out["governance"]["ALL_LAYERS_PARTICIPATE"] is True
assert out["governance"]["NO_LAYER_DISABLED"] is True
assert out["governance"]["DIRECT_TRADE_EXECUTION"] is False
assert out["governance"]["PUBLIC_OUTPUT_SANITIZED"] is True
assert out["governance"]["NO_FINANCIAL_ADVICE"] is True
assert out["governance"]["NO_GUARANTEED_RESULTS"] is True
assert out["governance"]["NO_SECRET_EXPOSURE"] is True
assert out["governance"]["FRONTEND_IS_DISPLAY_ONLY"] is True
assert out["governance"]["BACKEND_IS_DECISION_AUTHORITY"] is True
assert out["governance"]["RAW_LOGIC_EXPOSED"] is False
assert out["governance"]["FORMULAS_EXPOSED"] is False
assert out["governance"]["WEIGHTS_EXPOSED"] is False
assert out["governance"]["HIDDEN_LAYER_NAMES_EXPOSED"] is False

assert out["scenario"]["tdl_follow_style"] == "EXTENDED_MONITORING"
assert out["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert out["scenario"]["tdl_direction_exposure"] == "EXPOSED_CLEARER"
assert out["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert out["scenario"]["tdl_direction_clarity"] == "أوضح"
assert out["scenario"]["tdl_strength_label"] == "الأفق ممتد"
assert out["public_safe"] is True
assert_safe(out)

payload2 = {
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

out2 = govern_decision_output(payload2, package="pro")

assert out2["governance"]["DIRECT_TRADE_EXECUTION"] is False
assert out2["scenario"]["tdl_follow_style"] == "SHORT_MONITORING"
assert out2["scenario"]["tdl_follow_style_label"] == "أفق متابعة قصير"
assert out2["scenario"]["tdl_direction_exposure"] == "NON_EXPLICIT"
assert out2["scenario"]["tdl_direction_exposure_label"] == "الاتجاه غير صريح"
assert out2["scenario"]["tdl_direction_clarity"] == "غير صريح"
assert out2["scenario"]["tdl_strength_label"] == "الأفق قصير"
assert out2["public_safe"] is True
assert_safe(out2)

print("DIRECT_TRADE_EXECUTION_KEY_PRESERVED=True")
print("TDL_EXTENDED_MONITORING_OK=True")
print("TDL_SHORT_MONITORING_OK=True")
print("TDL_EXPOSED_CLEARER_OK=True")
print("TDL_NON_EXPLICIT_OK=True")
print("PUBLIC_OUTPUT_SANITIZED=True")
print("ASSERT_OK=True")
print("FINAL_STATUS=NDSP_FIX_DIRECT_TRADE_EXECUTION_KEY_TDL_V2_TEST_OK")

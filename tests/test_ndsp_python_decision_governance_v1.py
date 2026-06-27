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
    visible_layer_names,
)

def assert_safe(obj):
    text = json.dumps(obj, ensure_ascii=False, default=str)
    assert not contains_forbidden_public_terms(text), text

def visible_names(out):
    return [x.get("name") for x in out.get("layer_outputs", []) if x.get("name")]

raw_payload = {
    "ok": True,
    "symbol": "BTCUSDT",
    "market": "crypto",
    "timeframe": "1h",
    "direction": "BUY NOW bullish",
    "lm_direction": "UPWARD",
    "s_direction": "UPWARD",
    "side_relation": "DIFFERENT",
    "entry": 101000,
    "tp": 104000,
    "sl": 99000,
    "summary": "BUY NOW with entry and take profit and stop loss",
    "raw_layers": ["secret_layer_1", "secret_layer_2"],
    "internal_weights": {"x": 1},
    "formula": "secret formula",
    "contract_sum": 123,
    "source_categories": ["Asset Managers", "Leveraged Funds"],
    "order": {"side": "buy", "qty": 1},
    "execution": {"allowed": True},
    "hidden_layer_names": ["abc"],
    "caution_reason": "Do not execute blindly",
}

free_out = govern_decision_output(raw_payload, package="free")

assert free_out["ok"] is True
assert free_out["package"] == "free"

assert free_out["governance"]["MODE"] == "DECISION_ACTIVE"
assert free_out["governance"]["EXECUTION_POLICY"] == "EXECUTION_SANITIZED"
assert free_out["governance"]["ALL_LAYERS_PARTICIPATE"] is True
assert free_out["governance"]["NO_LAYER_DISABLED"] is True
assert free_out["governance"]["DIRECT_TRADE_EXECUTION"] is False
assert free_out["governance"]["PUBLIC_OUTPUT_SANITIZED"] is True
assert free_out["governance"]["NO_FINANCIAL_ADVICE"] is True
assert free_out["governance"]["NO_GUARANTEED_RESULTS"] is True
assert free_out["governance"]["NO_SECRET_EXPOSURE"] is True
assert free_out["governance"]["FRONTEND_IS_DISPLAY_ONLY"] is True
assert free_out["governance"]["BACKEND_IS_DECISION_AUTHORITY"] is True
assert free_out["governance"]["RAW_LOGIC_EXPOSED"] is False
assert free_out["governance"]["FORMULAS_EXPOSED"] is False
assert free_out["governance"]["WEIGHTS_EXPOSED"] is False
assert free_out["governance"]["HIDDEN_LAYER_NAMES_EXPOSED"] is False

assert free_out["scenario"]["scenario_directional_context_code"] == "UPWARD_CONTEXT"
assert free_out["scenario"]["scenario_activation_level"] == 101000
assert free_out["scenario"]["scenario_arrival_level"] == 104000
assert free_out["scenario"]["scenario_invalidation_level"] == 99000

# New rule:
# Free hides the TDL name, but safe TDL-derived context is allowed.
assert visible_names(free_out) == []
assert free_out["tdl_v2_context"]["layer_name_visible"] is False
assert free_out["tdl_v2_context"]["layer_name"] is None
assert free_out["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert free_out["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert free_out["scenario"]["tdl_direction_clarity"] == "أوضح"
assert free_out["scenario"]["tdl_strength_label"] == "الأفق ممتد"
assert_safe(free_out)

pro_out = govern_decision_output(raw_payload, package="pro")
assert pro_out["package"] == "pro"
assert visible_names(pro_out) == ["TDL", "NMP"]
assert pro_out["tdl_v2_context"]["layer_name_visible"] is True
assert pro_out["tdl_v2_context"]["layer_name"] == "TDL"
assert pro_out["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert pro_out["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert_safe(pro_out)

elite_out = govern_decision_output(raw_payload, package="elite")
elite_names = visible_names(elite_out)
assert "TDL" in elite_names
assert "NMP" in elite_names
assert "Devil's Advocate" in elite_names
assert "Nawaf Golden Alignment" in elite_names
assert elite_out["tdl_v2_context"]["layer_name_visible"] is True
assert elite_out["scenario"]["tdl_follow_style_label"] == "أفق متابعة ممتد"
assert elite_out["scenario"]["tdl_direction_exposure_label"] == "الاتجاه أوضح"
assert_safe(elite_out)

assert visible_layer_names("free") == []
assert visible_layer_names("pro") == ["TDL", "NMP"]
assert visible_layer_names("elite") == ["TDL", "NMP", "Devil's Advocate", "Nawaf Golden Alignment"]

print("SOURCE_MODE=python_decision_governed_tdl_v2")
print("PYTHON_DECISION_GOVERNANCE=True")
print("FREE_TDL_NAME_HIDDEN=True")
print("FREE_TDL_SAFE_CONTEXT_ALLOWED=True")
print("PRO_VISIBLE_TDL_NMP=True")
print("ELITE_VISIBLE_FOUR_LAYERS=True")
print("TDL_FOLLOW_STYLE_EXTENDED_MONITORING=True")
print("TDL_DIRECTION_EXPOSURE_EXPOSED_CLEARER=True")
print("PUBLIC_OUTPUT_SANITIZED=True")
print("DIRECT_TRADE_EXECUTION=False")
print("RAW_LOGIC_EXPOSED=False")
print("FORMULAS_EXPOSED=False")
print("WEIGHTS_EXPOSED=False")
print("HIDDEN_LAYER_NAMES_EXPOSED=False")
print("ASSERT_OK=True")
print("FINAL_STATUS=NDSP_PYTHON_DECISION_GOVERNANCE_V1_TDL_V2_AWARE_TEST_OK")

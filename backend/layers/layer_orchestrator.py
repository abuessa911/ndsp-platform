from __future__ import annotations
import importlib.util, json, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parent
OFFICIAL = [
"data/l1_source.py","data/l2_session.py","direction/l3_timing.py","data/l4_cot_manager.py",
"direction/l5_tdl_v2.py","direction/l6_direction_authority.py","quality/l7_macro.py",
"quality/l8_nmp.py","quality/l9_horizon_structure.py","quality/l10_momentum.py",
"quality/l11_divergence.py","execution/l12_black_layer.py","quality/l13_quality_stack.py",
"execution/l14_risk_governance.py","execution/l15_final_decision.py","execution/l16_scenario_alerts.py"
]

def load(path: Path):
    name = "ndsp_layer_" + "_".join(path.with_suffix("").parts[-5:])
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def feed(ctx, res):
    out = res.get("output", {})
    if isinstance(out, Mapping):
        ctx.update(out)
    lid = res.get("layer_id")
    if lid == 3:
        ctx["timing"] = out; ctx["timing_allowed"] = out.get("allowed")
    elif lid == 4:
        ctx["cot"] = out
    elif lid == 5:
        ctx["tdl"] = out; ctx["tdl_state"] = out.get("tdl_state"); ctx["tdl_bias"] = out.get("tdl_bias")
    elif lid == 8:
        ctx["nmp"] = out; ctx["nmp_confirmed"] = out.get("zone_state") == "INSIDE_REFERENCE_ZONE"
    elif lid == 12:
        ctx["black_layer"] = out; ctx["black_blocked"] = out.get("blocked")
    elif lid == 13:
        ctx["decision_quality_score"] = out.get("decision_quality_score", ctx.get("decision_quality_score"))
    elif lid == 14:
        ctx["risk_governance"] = out; ctx["risk_allowed"] = out.get("execution_allowed")
    elif lid == 15:
        ctx["final_decision"] = out; ctx["final_decision_state"] = out.get("final_decision_state")

def run_all_layers(payload=None):
    ctx = dict(payload or {})
    layers, errors = [], []
    for rel in OFFICIAL:
        try:
            res = load(ROOT / rel).evaluate(ctx)
            res.setdefault("module_file", rel)
            layers.append(res)
            feed(ctx, res)
        except Exception as e:
            errors.append({"module_file": rel, "error": repr(e)})
    conf = []
    for x in layers:
        try: conf.append(int(float(x.get("confidence", 0))))
        except Exception: pass
    return {
        "ok": not errors,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_layers_expected": 16,
        "total_layers_executed": len(layers),
        "total_errors": len(errors),
        "average_confidence": int(sum(conf)/len(conf)) if conf else 0,
        "layers": layers,
        "errors": errors,
        "context_after_layers": ctx
    }

def evaluate(payload=None): return run_all_layers(payload)
def run(payload=None): return run_all_layers(payload)

if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    payload = json.loads(raw) if raw else {}
    print(json.dumps(run_all_layers(payload), ensure_ascii=False, indent=2))

from __future__ import annotations
import importlib.util, sys
from pathlib import Path
from typing import Any, Mapping

LAYER_ID=9
LAYER_NAME='Horizon Structure'
LAYER_SHORT_NAME='L9_HORIZON_STRUCTURE'
LAYER_ARABIC_NAME='هيكل الأفق الزمني'
_SHARED_FILE = Path(__file__).resolve().parents[2] / "ndsp_latest_16_layers_logic_functions.py"

def _load_shared_module():
    module_name="ndsp_latest_16_layers_logic_functions"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec=importlib.util.spec_from_file_location(module_name, _SHARED_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load shared module: {_SHARED_FILE}")
    module=importlib.util.module_from_spec(spec)
    sys.modules[module_name]=module
    spec.loader.exec_module(module)
    return module

def evaluate(payload: Mapping[str, Any] | None=None) -> dict[str, Any]:
    module=_load_shared_module()
    result=getattr(module, 'evaluate_l9_horizon_structure')(payload or {})
    result.setdefault("layer_id", LAYER_ID)
    result.setdefault("layer_name", LAYER_NAME)
    result.setdefault("short_name", LAYER_SHORT_NAME)
    result.setdefault("arabic_name", LAYER_ARABIC_NAME)
    result.setdefault("module_file", str(Path(__file__).resolve()))
    return result

def run(payload=None): return evaluate(payload)
def compute(payload=None): return evaluate(payload)
def compute_layer(payload=None): return evaluate(payload)

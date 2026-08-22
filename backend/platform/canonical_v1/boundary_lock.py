from __future__ import annotations
import json
from pathlib import Path
from typing import Any

EXPECTED_LAYER_IDS = [f"NDSP-CORE-L{i:02d}" for i in range(1, 17)]
EXPECTED_CAPABILITY_IDS = [f"NDSP-CAP-{i:03d}" for i in range(1, 29)]

def validate_architecture_boundaries(layer_registry, capability_registry) -> dict[str, Any]:
    layer_data = json.loads(Path(layer_registry).read_text(encoding="utf-8"))
    cap_data = json.loads(Path(capability_registry).read_text(encoding="utf-8"))
    layers = layer_data.get("layers") or []
    caps = cap_data.get("capabilities") or []
    errors = []
    layer_ids = [x.get("id") for x in layers]
    cap_ids = [x.get("capability_id") for x in caps]

    if layer_ids != EXPECTED_LAYER_IDS:
        errors.append("layer IDs must be contiguous NDSP-CORE-L01..L16")
    if cap_ids != EXPECTED_CAPABILITY_IDS:
        errors.append("capability IDs must be contiguous NDSP-CAP-001..028")
    if any(str(x).startswith("NDSP-CAP") for x in layer_ids):
        errors.append("capability ID found in layer registry")
    if any(str(x).startswith("NDSP-CORE-L") for x in cap_ids):
        errors.append("layer ID found in capability registry")
    for cap in caps:
        if cap.get("decision_authority") is not False:
            errors.append(f"{cap.get('capability_id')} must have decision_authority=false")
    if len({x.get("canonical_name") for x in caps}) != len(caps):
        errors.append("capability canonical names must be unique")
    return {
        "ok": not errors,
        "layer_count": len(layers),
        "capability_count": len(caps),
        "errors": errors,
    }

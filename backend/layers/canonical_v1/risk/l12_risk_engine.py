from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L12"
CANONICAL_NAME = "risk_engine"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    output = payload.get("risk_result") or {
        "status": "NOT_EVALUATED",
        "blocked": False,
        "reason": "explicit_risk_input_required",
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, output.get("status", "NOT_EVALUATED"),
        int(output.get("confidence", 0) or 0), output,
        blocking=bool(output.get("blocked", False)),
    ).to_dict()

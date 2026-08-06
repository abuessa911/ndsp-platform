from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L11"
CANONICAL_NAME = "usd_macro_filter"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    output = payload.get("usd_macro_result") or {
        "status": "NOT_EVALUATED",
        "reason": "explicit_macro_input_required",
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME, output.get("status", "NOT_EVALUATED"),
        int(output.get("confidence", 0) or 0), output, blocking=False,
    ).to_dict()

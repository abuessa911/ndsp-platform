from __future__ import annotations

from typing import Any, Mapping

from ..core.contracts import LayerResult

LAYER_ID = "NDSP-CORE-L15"
CANONICAL_NAME = "devils_advocate"


def evaluate(payload: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload = dict(payload or {})
    blocked = bool(payload.get("devils_advocate_blocked", False))
    reasons = payload.get("devils_advocate_reasons") or []
    output = {
        "blocked": blocked,
        "reasons": reasons,
        "authority": "final_objection_only",
    }
    return LayerResult(
        LAYER_ID, CANONICAL_NAME,
        "BLOCKED" if blocked else "PASSED",
        95, output, blocking=blocked,
    ).to_dict()

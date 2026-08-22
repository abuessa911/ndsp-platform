from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_TEXT = str(PROJECT_ROOT)

if PROJECT_ROOT_TEXT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_TEXT)

from backend.layers.canonical_v1.runtime_bridge import (
    run_canonical_layers,
    to_legacy_api_envelope,
)


def run_layers_compat(
    payload: Mapping[str, Any] | None,
    *,
    input_context_source: str | None = None,
) -> dict[str, Any]:
    canonical = run_canonical_layers(payload)
    return to_legacy_api_envelope(
        canonical,
        input_context_source=input_context_source,
    )


def health_metadata() -> dict[str, Any]:
    return {
        "canonical_import": True,
        "engine_mode": "canonical_v1_candidate",
        "project_root": PROJECT_ROOT_TEXT,
        "project_root_on_path": PROJECT_ROOT_TEXT in sys.path,
    }

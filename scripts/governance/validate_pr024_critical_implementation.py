#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR024 = ROOT / "docs/99-governance/pr-024-critical-tests-ui-bindings"
UI_ROOT = ROOT / "frontend/user-portal-vite/src/features/critical-capabilities"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR024_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    tests = rows(PR024 / "PR024_EXECUTABLE_TEST_MATRIX.csv")
    bindings = rows(PR024 / "PR024_UI_BINDING_REGISTRY.csv")
    summary = json.loads(
        (PR024 / "PR024_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(tests) != 11:
        return fail(f"Expected 11 tests, found {len(tests)}")

    if len(bindings) != 14:
        return fail(f"Expected 14 bindings, found {len(bindings)}")

    if len({row["capability_id"] for row in tests}) != 11:
        return fail("Duplicate test capability IDs")

    if len({row["capability_id"] for row in bindings}) != 14:
        return fail("Duplicate binding capability IDs")

    panel = (UI_ROOT / "CriticalCapabilityPanel.tsx").read_text(
        encoding="utf-8"
    )

    for state in ("loading", "empty", "stale", "error", "ready"):
        if f'"{state}"' not in panel:
            return fail(f"Missing UI state: {state}")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records are forbidden")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    print("executable_contract_tests=11")
    print("ui_bindings=14")
    print("ui_states=loading,empty,stale,error,ready")
    print("ui_complete_records_created=0")
    print("full_capability_coverage_claimed=false")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR024_CRITICAL_IMPLEMENTATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

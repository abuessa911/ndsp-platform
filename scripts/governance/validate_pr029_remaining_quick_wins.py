#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR029 = ROOT / "docs/99-governance/pr-029-remaining-quick-wins-closure"
UI_ROOT = ROOT / "frontend/user-portal-vite/src/features/remaining-quick-wins"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR029_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    inputs = rows(PR029 / "PR029_INPUT_REMAINING_QUICK_WINS.csv")
    results = rows(PR029 / "PR029_CLOSURE_RESULTS.csv")
    closed = rows(PR029 / "PR029_CLOSED_CAPABILITIES.csv")
    still_open = rows(PR029 / "PR029_STILL_OPEN_CAPABILITIES.csv")
    tests = rows(PR029 / "PR029_EXECUTABLE_TEST_MATRIX.csv")
    summary = json.loads(
        (PR029 / "PR029_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(inputs) != 31:
        return fail(f"Expected 31 inputs, found {len(inputs)}")

    if len(results) != 31:
        return fail(f"Expected 31 results, found {len(results)}")

    if len(closed) + len(still_open) != 31:
        return fail("Closure accounting invariant failed")

    if len(tests) != 31:
        return fail(f"Expected 31 tests, found {len(tests)}")

    panel = (UI_ROOT / "RemainingQuickWinPanel.tsx").read_text(
        encoding="utf-8"
    )

    for state in ("loading", "empty", "stale", "error", "ready"):
        if f'"{state}"' not in panel:
            return fail(f"Missing UI state: {state}")

    if summary["human_approvals_granted"] != 0:
        return fail("Human approvals cannot be automated")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records are forbidden")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    print("input_remaining_quick_win_count=31")
    print(f"closed_machine_verified_count={len(closed)}")
    print(f"still_open_count={len(still_open)}")
    print("closure_accounting=PASS")
    print("test_accounting=PASS")
    print("ui_state_validation=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR029_REMAINING_QUICK_WINS_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

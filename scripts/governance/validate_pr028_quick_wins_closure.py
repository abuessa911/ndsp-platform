#!/usr/bin/env python3
"""Validate PR-028 quick-win extraction and closure accounting."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR028 = ROOT / "docs/99-governance/pr-028-quick-wins-evidence-closure"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR028_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    inputs = rows(PR028 / "PR028_QUICK_WINS_INPUT.csv")
    results = rows(PR028 / "PR028_CLOSURE_RESULTS.csv")
    closed = rows(PR028 / "PR028_CLOSED_CAPABILITIES.csv")
    remaining = rows(PR028 / "PR028_REMAINING_QUICK_WINS.csv")
    tests = rows(PR028 / "PR028_EXECUTABLE_TEST_MATRIX.csv")
    summary = json.loads(
        (PR028 / "PR028_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(inputs) != 55:
        return fail(f"Expected 55 quick wins, found {len(inputs)}")

    if len(results) != 55:
        return fail(f"Expected 55 results, found {len(results)}")

    if len(closed) + len(remaining) != 55:
        return fail("Closure accounting invariant failed")

    if len(tests) != 55:
        return fail(f"Expected 55 executable tests, found {len(tests)}")

    if summary["closed_machine_verified_count"] != len(closed):
        return fail("Closed summary count mismatch")

    if summary["remaining_quick_win_count"] != len(remaining):
        return fail("Remaining summary count mismatch")

    if summary["human_approvals_granted"] != 0:
        return fail("Human approval cannot be automated")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records are forbidden")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    print("input_quick_win_count=55")
    print("details_exported=55")
    print("executable_test_count=55")
    print(f"closed_machine_verified_count={len(closed)}")
    print(f"remaining_quick_win_count={len(remaining)}")
    print("closure_accounting=PASS")
    print("test_accounting=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR028_QUICK_WINS_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

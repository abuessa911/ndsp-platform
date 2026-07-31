#!/usr/bin/env python3
"""Validate PR-026 runtime verification accounting and safety."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR026 = ROOT / "docs/99-governance/pr-026-runtime-capability-verification"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR026_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    matrix = rows(PR026 / "PR026_RUNTIME_VERIFICATION_MATRIX.csv")
    verified = rows(PR026 / "PR026_RUNTIME_VERIFIED_CAPABILITIES.csv")
    pending = rows(PR026 / "PR026_RUNTIME_PENDING_CAPABILITIES.csv")
    summary = json.loads(
        (PR026 / "PR026_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(matrix) != 526:
        return fail(f"Expected 526 capabilities, found {len(matrix)}")

    if len(verified) + len(pending) != len(matrix):
        return fail("Runtime accounting invariant failed")

    if summary["unsafe_mutating_requests_executed"] != 0:
        return fail("Mutating runtime requests are forbidden")

    if summary["services_restarted"] != 0:
        return fail("Service restart is forbidden")

    if summary["environment_values_read"] is not False:
        return fail("Environment values must not be read")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records must not be created")

    if summary["runtime_verified_capabilities"] != len(verified):
        return fail("Verified summary count mismatch")

    if summary["runtime_pending_capabilities"] != len(pending):
        return fail("Pending summary count mismatch")

    expected_claim = len(pending) == 0

    if summary["full_capability_coverage_claimed"] is not expected_claim:
        return fail("Full coverage claim does not match evidence")

    print(f"total_capabilities={len(matrix)}")
    print(f"runtime_verified_capabilities={len(verified)}")
    print(f"runtime_pending_capabilities={len(pending)}")
    print("runtime_accounting=PASS")
    print("runtime_safety=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR026_RUNTIME_VERIFICATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

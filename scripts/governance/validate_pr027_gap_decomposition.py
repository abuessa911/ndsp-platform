#!/usr/bin/env python3
"""Validate PR-027 gap decomposition and batch accounting."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR027 = ROOT / "docs/99-governance/pr-027-runtime-gap-decomposition"

EXPECTED_CATEGORIES = {
    "SOURCE",
    "SERVICE",
    "ENDPOINT",
    "REAL_DATA",
    "CALCULATION",
    "TEST",
    "UI",
}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR027_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    gaps = rows(PR027 / "PR027_GAP_DECOMPOSITION.csv")
    batches = rows(PR027 / "PR027_REMEDIATION_BATCHES.csv")
    categories = rows(PR027 / "PR027_GAP_CATEGORY_SUMMARY.csv")
    summary = json.loads(
        (PR027 / "PR027_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(gaps) != 526:
        return fail(f"Expected 526 gap rows, found {len(gaps)}")

    if len({row["capability_id"] for row in gaps}) != 526:
        return fail("Duplicate capability IDs exist")

    if sum(int(row["capability_count"]) for row in batches) != 526:
        return fail("Batch accounting invariant failed")

    found_categories = {row["gap_category"] for row in categories}

    if found_categories != EXPECTED_CATEGORIES:
        return fail("Gap categories are incomplete")

    if summary["total_capabilities"] != 526:
        return fail("Summary capability count mismatch")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records are forbidden")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    print("total_capabilities=526")
    print("gap_accounting=PASS")
    print("batch_accounting=PASS")
    print("category_accounting=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR027_GAP_DECOMPOSITION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

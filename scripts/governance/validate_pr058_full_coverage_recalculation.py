#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR058 = ROOT / "docs/99-governance/pr-058-full-coverage-recalculation"
GAPS = {"SOURCE", "SERVICE", "ENDPOINT", "REAL_DATA", "CALCULATION", "TEST", "UI"}
STATUSES = {"FULLY_EVIDENCED", "PARTIALLY_EVIDENCED", "DISCOVERY_REQUIRED"}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR058_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    matrix = rows(PR058 / "PR058_CAPABILITY_COVERAGE_MATRIX.csv")
    remaining = rows(PR058 / "PR058_REMAINING_GAPS.csv")
    gap_summary = rows(PR058 / "PR058_GAP_CATEGORY_SUMMARY.csv")
    summary = json.loads((PR058 / "PR058_SUMMARY.json").read_text(encoding="utf-8"))

    if len(matrix) != 526:
        return fail(f"Expected 526 matrix rows, found {len(matrix)}")

    if len({row["capability_id"] for row in matrix}) != 526:
        return fail("Capability IDs are not unique")

    status_counts = Counter(row["recalculated_status"] for row in matrix)
    if not set(status_counts).issubset(STATUSES):
        return fail("Unknown recalculated status")

    if sum(status_counts.values()) != 526:
        return fail("Status accounting invariant failed")

    matrix_remaining = [row for row in matrix if row["remaining_gaps"]]
    if len(matrix_remaining) != len(remaining):
        return fail("Remaining-gap accounting invariant failed")

    gap_rows = {row["gap_type"]: row for row in gap_summary}
    if set(gap_rows) != GAPS:
        return fail("Gap summary does not contain all seven dimensions")

    for gap in GAPS:
        expected = sum(gap in row["remaining_gaps"].split("|") for row in matrix)
        actual = int(gap_rows[gap]["capability_count"])
        if actual != expected:
            return fail(f"Gap count mismatch for {gap}")

    full_claim_expected = (
        summary["fully_evidenced_capabilities"] == 526
        and summary["remaining_capability_count"] == 0
    )
    if summary["full_capability_coverage_claimed"] is not full_claim_expected:
        return fail("Full-coverage claim invariant failed")

    if summary["traceability_rows_modified"] != 0:
        return fail("PR-058 must not modify Traceability")

    if summary["runtime_changes"] != "none":
        return fail("PR-058 must not modify runtime")

    if summary["p0_remediation_batch_count"] != 19:
        return fail("Expected 19 P0 remediation batches")

    if summary["p0_planned_capabilities"] != 391:
        return fail("Expected 391 planned P0 capabilities")

    if summary["p0_closed_capabilities_verified"] != 391:
        return fail("P0 closure verification is incomplete")

    print("total_capabilities=526")
    print(f"fully_evidenced_capabilities={summary['fully_evidenced_capabilities']}")
    print(f"remaining_capability_count={summary['remaining_capability_count']}")
    print("coverage_accounting=PASS")
    print("gap_accounting=PASS")
    print("status_accounting=PASS")
    print("full_claim_invariant=PASS")
    print("p0_batch_accounting=PASS")
    print("p0_closure_verification=PASS")
    print("traceability_rows_modified=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR058_FULL_COVERAGE_RECALCULATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate PR-059 P0 Traceability reconciliation."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "docs/99-governance/pr-059-p0-traceability-reconciliation"
TRACEABILITY = ROOT / (
    "docs/99-governance/pr-018-full-capability-ui-governance/"
    "CAPABILITY_UI_TRACEABILITY.csv"
)


def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR059_P0_TRACEABILITY_RECONCILIATION_INVALID")
    return 1


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    required = [
        "README.md",
        "PR-059-P0-TRACEABILITY-RECONCILIATION.md",
        "PR059_RECONCILIATION_AUDIT.csv",
        "PR059_RECONCILIATION_AUDIT.json",
        "PR059_BATCH_SOURCES.json",
        "PR059_POST_RECONCILIATION_COVERAGE.csv",
        "PR059_POST_RECONCILIATION_COVERAGE.json",
        "PR059_REMAINING_GAPS.csv",
        "PR059_GAP_CATEGORY_SUMMARY.csv",
        "PR059_STATUS_SUMMARY.csv",
        "PR059_PRIORITY_SUMMARY.csv",
        "PR059_SUMMARY.json",
    ]

    for name in required:
        path = PACKAGE / name
        if not path.is_file() or path.stat().st_size == 0:
            return fail(f"Missing or empty artifact: {name}")
        print(f"{name}: OK")

    summary = json.loads(
        (PACKAGE / "PR059_SUMMARY.json").read_text(encoding="utf-8")
    )
    audit = json.loads(
        (PACKAGE / "PR059_RECONCILIATION_AUDIT.json").read_text(
            encoding="utf-8"
        )
    )
    coverage = json.loads(
        (PACKAGE / "PR059_POST_RECONCILIATION_COVERAGE.json").read_text(
            encoding="utf-8"
        )
    )
    traceability = read_csv(TRACEABILITY)

    if summary["total_capabilities"] != 526:
        return fail("Expected 526 total capabilities")
    if len(traceability) != 526 or len(coverage) != 526:
        return fail("Coverage or Traceability count is not 526")
    if summary["p0_assignment_count"] != 391:
        return fail("Expected 391 P0 assignments")
    if summary["p0_batch_count"] != 19:
        return fail("Expected 19 P0 batches")
    if summary["p0_machine_closed_count"] != 391:
        return fail("Expected 391 machine-closed P0 capabilities")
    if summary["p0_closure_records_accounted"] != 391:
        return fail("Expected 391 accounted closure records")
    if len(audit) != 391:
        return fail("Expected 391 reconciliation audit rows")
    if summary["p0_canonical_standard_gap_count"] != 0:
        return fail("Canonical P0 standard gaps remain")

    status_total = (
        summary["fully_evidenced_capabilities"]
        + summary["partially_evidenced_capabilities"]
        + summary["discovery_required_capabilities"]
    )
    if status_total != 526:
        return fail("Coverage status accounting does not equal 526")

    if summary["ui_complete_records_created"] != 0:
        return fail("PR-059 must not create UI_COMPLETE records")
    if summary["production_services_restarted"] != 0:
        return fail("PR-059 must not restart production services")
    if summary["mutating_requests_executed"] != 0:
        return fail("PR-059 must not execute mutating requests")
    if summary["runtime_changes"] != "none":
        return fail("PR-059 runtime_changes must be none")

    print("p0_closure_accounting=PASS")
    print("p0_canonical_reconciliation=PASS")
    print("coverage_accounting=PASS")
    print("runtime_safety=PASS")
    print("validation=PASS")
    print("status=PR059_P0_TRACEABILITY_RECONCILIATION_VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())

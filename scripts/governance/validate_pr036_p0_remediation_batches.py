#!/usr/bin/env python3
"""Validate PR-036 P0 remediation batch decomposition."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR036 = ROOT / "docs/99-governance/pr-036-p0-remediation-batches"

SIGNATURES = {
    "SERVICE_ENDPOINT_REAL_DATA",
    "SERVICE_ENDPOINT",
    "SERVICE_REAL_DATA",
    "ENDPOINT_REAL_DATA",
    "SERVICE_ONLY",
    "ENDPOINT_ONLY",
}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR036_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    top50 = rows(PR036 / "PR036_TOP_50_P0_CAPABILITIES.csv")
    batches = rows(PR036 / "PR036_REMEDIATION_BATCHES.csv")
    assignments = rows(PR036 / "PR036_BATCH_ASSIGNMENTS.csv")
    signature_summary = rows(PR036 / "PR036_SIGNATURE_SUMMARY.csv")
    summary = json.loads(
        (PR036 / "PR036_SUMMARY.json").read_text(encoding="utf-8")
    )

    if summary["p0_capability_count"] != 391:
        return fail("Expected 391 P0 capabilities")

    if len(top50) != 50:
        return fail(f"Expected top 50 rows, found {len(top50)}")

    if len(assignments) != 391:
        return fail(
            f"Expected 391 assignments, found {len(assignments)}"
        )

    capability_ids = [
        row["capability_id"]
        for row in assignments
    ]

    if len(set(capability_ids)) != 391:
        return fail("P0 assignment IDs are not unique")

    if not batches:
        return fail("No remediation batches were generated")

    batch_ids = {
        row["batch_id"]
        for row in batches
    }

    if len(batch_ids) != len(batches):
        return fail("Batch IDs are not unique")

    assignment_counts = Counter(
        row["batch_id"]
        for row in assignments
    )

    for batch in batches:
        batch_id = batch["batch_id"]
        expected = int(batch["capability_count"])
        actual = assignment_counts[batch_id]

        if batch_id not in assignment_counts:
            return fail(f"Batch has no assignments: {batch_id}")

        if expected != actual:
            return fail(
                f"Batch count mismatch for {batch_id}: "
                f"{expected} != {actual}"
            )

        if expected < 1 or expected > 25:
            return fail(f"Invalid batch size for {batch_id}")

        if batch["signature"] not in SIGNATURES:
            return fail(f"Unknown signature: {batch['signature']}")

        if batch["production_restart_allowed"] != "false":
            return fail("Production restart must remain forbidden")

        if batch["mutating_probe_allowed"] != "false":
            return fail("Mutating probes must remain forbidden")

    signature_counts = {
        row["signature"]: int(row["capability_count"])
        for row in signature_summary
    }

    if set(signature_counts) != SIGNATURES:
        return fail("Signature summary is incomplete")

    if sum(signature_counts.values()) != 391:
        return fail("Signature accounting does not equal 391")

    ranks = [int(row["rank"]) for row in top50]

    if ranks != list(range(1, 51)):
        return fail("Top-50 ranks are not contiguous")

    for previous, current in zip(top50, top50[1:]):
        previous_key = (
            -int(previous["p0_gap_count"]),
            -int(previous["total_gap_count"]),
            previous["capability_id"],
        )
        current_key = (
            -int(current["p0_gap_count"]),
            -int(current["total_gap_count"]),
            current["capability_id"],
        )

        if previous_key > current_key:
            return fail("Top-50 ranking order is invalid")

    if summary["unassigned_p0_capabilities"] != 0:
        return fail("Unassigned P0 capabilities remain")

    if summary["duplicate_assignments"] != 0:
        return fail("Duplicate assignments were detected")

    if summary["traceability_rows_modified"] != 0:
        return fail("PR-036 must not modify Traceability")

    if summary["runtime_changes"] != "none":
        return fail("PR-036 must not modify runtime")

    print("total_capabilities=526")
    print("p0_capability_count=391")
    print("top_50_exported=50")
    print(f"remediation_batch_count={len(batches)}")
    print("batch_assignment_count=391")
    print("batch_accounting=PASS")
    print("assignment_accounting=PASS")
    print("signature_accounting=PASS")
    print("top_50_ranking=PASS")
    print("batch_size_validation=PASS")
    print("runtime_safety=PASS")
    print("traceability_rows_modified=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR036_P0_REMEDIATION_BATCHES_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

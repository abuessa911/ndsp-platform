#!/usr/bin/env python3
"""Validate PR-037 batch-01 evidence closure."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR037 = ROOT / "docs/99-governance/pr-037-p0-batch-01-evidence-closure"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR037_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    batch_input = rows(PR037 / "PR037_BATCH_INPUT.csv")
    evidence = rows(PR037 / "PR037_EVIDENCE_MATRIX.csv")
    results = rows(PR037 / "PR037_CLOSURE_RESULTS.csv")
    remaining = rows(PR037 / "PR037_REMAINING_GAPS.csv")
    summary = json.loads(
        (PR037 / "PR037_SUMMARY.json").read_text(encoding="utf-8")
    )

    input_count = len(batch_input)

    if input_count < 1 or input_count > 25:
        return fail(f"Invalid batch size: {input_count}")

    if len(evidence) != input_count or len(results) != input_count:
        return fail("Evidence/result accounting mismatch")

    closed = [
        row for row in results
        if row["closure_state"] == "CLOSED_MACHINE_EVIDENCE_FOUND"
    ]
    open_rows = [
        row for row in results
        if row["closure_state"] == "OPEN_EVIDENCE_INCOMPLETE"
    ]

    if len(closed) != summary["machine_closed_count"]:
        return fail("Closed capability accounting mismatch")

    if len(open_rows) != summary["remaining_gap_count"]:
        return fail("Remaining capability accounting mismatch")

    if len(remaining) != len(open_rows):
        return fail("Remaining-gap file accounting mismatch")

    if summary["traceability_rows_updated"] != len(closed):
        return fail("Traceability update accounting mismatch")

    for row in evidence:
        service_ok = (
            row["service_required"] == "false"
            or row["service_evidence_found"] == "true"
        )
        endpoint_ok = (
            row["endpoint_required"] == "false"
            or row["endpoint_evidence_found"] == "true"
        )
        data_ok = (
            row["real_data_required"] == "false"
            or row["real_data_evidence_found"] == "true"
        )
        expected_closed = service_ok and endpoint_ok and data_ok

        if (row["machine_closed"] == "true") != expected_closed:
            return fail(
                f"Invalid closure decision: {row['capability_id']}"
            )

    if summary["production_services_restarted"] != 0:
        return fail("Production service restart is forbidden")

    if summary["mutating_requests_executed"] != 0:
        return fail("Mutating requests are forbidden")

    if summary["runtime_changes"] != "none":
        return fail("Runtime changes are forbidden")

    if summary["ui_complete_records_created"] != 0:
        return fail("PR-037 must not create UI_COMPLETE records")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("PR-037 must not claim full capability coverage")

    print(f"batch_id={summary['batch_id']}")
    print(f"input_capability_count={input_count}")
    print(f"machine_closed_count={len(closed)}")
    print(f"remaining_gap_count={len(open_rows)}")
    print(f"traceability_rows_updated={len(closed)}")
    print("closure_accounting=PASS")
    print("evidence_accounting=PASS")
    print("traceability_accounting=PASS")
    print("runtime_safety=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR037_P0_BATCH_01_EVIDENCE_CLOSURE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

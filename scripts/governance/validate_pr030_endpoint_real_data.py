#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR030 = ROOT / "docs/99-governance/pr-030-endpoint-real-data-closure"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR030_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    details = rows(PR030 / "PR030_CAPABILITY_DETAILS.csv")
    results = rows(PR030 / "PR030_CLOSURE_RESULTS.csv")
    closed = rows(PR030 / "PR030_CLOSED_CAPABILITIES.csv")
    still_open = rows(PR030 / "PR030_STILL_OPEN_CAPABILITIES.csv")
    tests = rows(PR030 / "PR030_EXECUTABLE_TEST_MATRIX.csv")
    summary = json.loads(
        (PR030 / "PR030_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(details) != 20:
        return fail(f"Expected 20 detail records, found {len(details)}")

    if len(results) != 20:
        return fail(f"Expected 20 results, found {len(results)}")

    if len(closed) + len(still_open) != 20:
        return fail("Closure accounting invariant failed")

    if len(tests) != 20:
        return fail(f"Expected 20 tests, found {len(tests)}")

    if summary["unsafe_mutating_requests_executed"] != 0:
        return fail("Mutating requests are forbidden")

    if summary["services_restarted"] != 0:
        return fail("Service restarts are forbidden")

    if summary["mock_data_created"] != 0:
        return fail("Mock data creation is forbidden")

    if summary["human_approvals_granted"] != 0:
        return fail("Human approval cannot be automated")

    if summary["ui_complete_records_created"] != 0:
        return fail("UI_COMPLETE records are forbidden")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    for row in closed:
        if "ENDPOINT" in row["original_missing_evidence"]:
            if not row["selected_route_source"]:
                return fail(
                    f"Closed endpoint lacks route source: "
                    f"{row['capability_id']}"
                )
            if not row["accepted_probe_url"]:
                return fail(
                    f"Closed endpoint lacks accepted probe: "
                    f"{row['capability_id']}"
                )

        if "REAL_DATA" in row["original_missing_evidence"]:
            if row["data_state"] not in {"REAL_LIVE", "REAL_SNAPSHOT"}:
                return fail(
                    f"Closed real-data row has invalid state: "
                    f"{row['capability_id']}"
                )

    print("input_capability_count=20")
    print("details_exported=20")
    print(f"closed_machine_verified_count={len(closed)}")
    print(f"still_open_count={len(still_open)}")
    print("closure_accounting=PASS")
    print("test_accounting=PASS")
    print("endpoint_evidence_validation=PASS")
    print("real_data_evidence_validation=PASS")
    print("runtime_safety=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR030_ENDPOINT_REAL_DATA_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

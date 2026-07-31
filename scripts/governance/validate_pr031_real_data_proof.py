#!/usr/bin/env python3
"""Validate PR-031 real-data proof accounting and safety."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR031 = ROOT / "docs/99-governance/pr-031-real-data-proof-closure"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR031_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    details = rows(PR031 / "PR031_CAPABILITY_DETAILS.csv")
    responses = rows(PR031 / "PR031_RESPONSE_PROFILES.csv")
    results = rows(PR031 / "PR031_CLOSURE_RESULTS.csv")
    closed = rows(PR031 / "PR031_CLOSED_CAPABILITIES.csv")
    still_open = rows(PR031 / "PR031_STILL_OPEN_CAPABILITIES.csv")
    tests = rows(PR031 / "PR031_EXECUTABLE_TEST_MATRIX.csv")
    summary = json.loads(
        (PR031 / "PR031_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(details) != 2:
        return fail(f"Expected 2 detail rows, found {len(details)}")

    if len(responses) != 2:
        return fail(f"Expected 2 response profiles, found {len(responses)}")

    if len(results) != 2:
        return fail(f"Expected 2 results, found {len(results)}")

    if len(closed) + len(still_open) != 2:
        return fail("Closure accounting invariant failed")

    if len(tests) != 2:
        return fail(f"Expected 2 tests, found {len(tests)}")

    if summary["payload_values_persisted"] is not False:
        return fail("Payload values must not be persisted")

    for field in (
        "unsafe_mutating_requests_executed",
        "services_restarted",
        "mock_data_created",
        "human_approvals_granted",
        "ui_complete_records_created",
    ):
        if summary[field] != 0:
            return fail(f"Safety invariant failed: {field}")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    for row in closed:
        if row["data_state"] not in {"REAL_LIVE", "REAL_SNAPSHOT"}:
            return fail(
                f"Invalid real-data state: {row['capability_id']}"
            )
        if not row["connector_evidence"]:
            return fail(
                f"Missing connector evidence: {row['capability_id']}"
            )
        if len(row["payload_sha256"]) != 64:
            return fail(
                f"Invalid payload digest: {row['capability_id']}"
            )
        if int(row["payload_bytes"]) <= 0:
            return fail(
                f"Empty payload: {row['capability_id']}"
            )
        if int(row["root_item_count"]) <= 0:
            return fail(
                f"Empty JSON root: {row['capability_id']}"
            )

    print("input_capability_count=2")
    print("details_exported=2")
    print(f"closed_machine_verified_count={len(closed)}")
    print(f"still_open_count={len(still_open)}")
    print("closure_accounting=PASS")
    print("test_accounting=PASS")
    print("connector_evidence_validation=PASS")
    print("response_profile_validation=PASS")
    print("payload_privacy_validation=PASS")
    print("runtime_safety=PASS")
    print("ui_complete_records_created=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR031_REAL_DATA_PROOF_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

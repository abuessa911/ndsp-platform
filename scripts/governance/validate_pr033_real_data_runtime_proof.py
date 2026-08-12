#!/usr/bin/env python3
"""Validate PR-033 runtime proof accounting, safety, and traceability."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR033 = ROOT / "docs/99-governance/pr-033-real-data-runtime-proof"
TRACEABILITY = (
    ROOT
    / "docs/99-governance/pr-018-full-capability-ui-governance"
    / "CAPABILITY_UI_TRACEABILITY.csv"
)

EXPECTED = {
    "CAP-4FF90CCC6DFE": (
        "GET /api/admin/timing_model-v2/policy",
        "TDL_V2_POLICY_STORE",
        "REAL_SNAPSHOT",
    ),
    "CAP-8A9DD9B6E7D5": (
        "GET /api/admin/timing_model-v2/auth-debug",
        "PROCESS_ENVIRONMENT_PRESENCE_METADATA",
        "REAL_LIVE",
    ),
}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR033_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    proof = rows(PR033 / "PR033_RUNTIME_PROOF.csv")
    closed = rows(PR033 / "PR033_CLOSED_CAPABILITIES.csv")
    still_open = rows(PR033 / "PR033_STILL_OPEN_CAPABILITIES.csv")
    trace = {
        row["capability_id"]: row
        for row in rows(TRACEABILITY)
    }
    summary = json.loads(
        (PR033 / "PR033_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(proof) != 2 or len(closed) != 2 or still_open:
        return fail("Closure accounting invariant failed")

    if {row["capability_id"] for row in proof} != set(EXPECTED):
        return fail("Unexpected capability set")

    for row in proof:
        capability_id = row["capability_id"]
        endpoint, data_source, data_state = EXPECTED[capability_id]

        if row["canonical_endpoint"] != endpoint:
            return fail(f"Endpoint mismatch: {capability_id}")

        if row["data_source"] != data_source:
            return fail(f"Data-source mismatch: {capability_id}")

        if row["data_state"] != data_state:
            return fail(f"Data-state mismatch: {capability_id}")

        if row["closure_state"] != "CLOSED_MACHINE_VERIFIED":
            return fail(f"Capability not closed: {capability_id}")

        if len(row["payload_sha256"]) != 64:
            return fail(f"Invalid payload digest: {capability_id}")

        if int(row["payload_bytes"]) <= 0:
            return fail(f"Empty payload: {capability_id}")

        if int(row["root_item_count"]) <= 0:
            return fail(f"Empty proof root: {capability_id}")

        trace_row = trace[capability_id]

        if trace_row["endpoint_or_contract"] != endpoint:
            return fail(f"Traceability endpoint mismatch: {capability_id}")

        if trace_row["data_source"] != data_source:
            return fail(f"Traceability source mismatch: {capability_id}")

        if trace_row["data_state"] != data_state:
            return fail(f"Traceability state mismatch: {capability_id}")

    expected_zero = (
        "production_services_restarted",
        "mutating_requests_executed",
        "human_approvals_granted",
        "ui_complete_records_created",
    )

    for field in expected_zero:
        if summary[field] != 0:
            return fail(f"Safety invariant failed: {field}")

    if summary["payload_values_persisted"] is not False:
        return fail("Payload values must not be persisted")

    if summary["temporary_admin_key_persisted"] is not False:
        return fail("Temporary admin key must not be persisted")

    if summary["full_capability_coverage_claimed"] is not False:
        return fail("Full coverage claim is forbidden")

    print("input_capability_count=2")
    print("closed_machine_verified_count=2")
    print("still_open_count=0")
    print("closure_accounting=PASS")
    print("canonical_contract_validation=PASS")
    print("data_source_validation=PASS")
    print("real_data_state_validation=PASS")
    print("runtime_proof_validation=PASS")
    print("payload_privacy_validation=PASS")
    print("runtime_safety=PASS")
    print("ui_complete_records_created=0")
    print("validation=PASS")
    print("status=PR033_REAL_DATA_RUNTIME_PROOF_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

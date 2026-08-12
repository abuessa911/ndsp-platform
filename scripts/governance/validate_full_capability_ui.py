#!/usr/bin/env python3
"""Validate NDSP capability-to-UI governance."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "docs/99-governance/pr-018-full-capability-ui-governance"
POLICY = PACKAGE / "FULL_CAPABILITY_UI_POLICY.json"
REGISTER = PACKAGE / "CAPABILITY_UI_TRACEABILITY.csv"

MARKER = "NDSP_FULL_CAPABILITY_UI_GOVERNANCE_START"

EXPECTED_COLUMNS = [
    "capability_id",
    "capability_name",
    "description",
    "source_or_algorithm",
    "runtime_service",
    "endpoint_or_contract",
    "data_source",
    "calculation_mode",
    "user_role",
    "screen",
    "visible_component",
    "coverage_state",
    "data_state",
    "canonicality",
    "evidence_path",
    "owner",
    "last_verified_at",
    "notes",
]

COVERAGE_STATES = {
    "DISCOVERY_REQUIRED",
    "SOURCE_IDENTIFIED",
    "SERVICE_CONNECTED",
    "API_CONNECTED",
    "UI_PARTIAL",
    "UI_COMPLETE",
    "NOT_USER_FACING",
    "DEPRECATED_WITH_APPROVAL",
}

DATA_STATES = {
    "UNKNOWN",
    "REAL_LIVE",
    "REAL_DELAYED",
    "REAL_SNAPSHOT",
    "CALCULATED_REAL",
    "MOCK_ONLY",
    "NOT_APPLICABLE",
}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=FULL_CAPABILITY_UI_GOVERNANCE_FAILED", file=sys.stderr)
    return 1


def changed_files(base_ref: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-ref")
    args = parser.parse_args()

    try:
        policy = json.loads(POLICY.read_text(encoding="utf-8"))

        if policy.get("runtime_changes") != "none":
            return fail("Policy must declare runtime_changes=none")

        for path in (
            ROOT / "AGENTS.md",
            ROOT / ".github/copilot-instructions.md",
        ):
            if MARKER not in path.read_text(encoding="utf-8"):
                return fail(f"Governance marker missing from {path}")

        with REGISTER.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)

            if reader.fieldnames != EXPECTED_COLUMNS:
                return fail("Unexpected traceability register columns")

            rows = list(reader)

        seen: set[str] = set()

        for number, row in enumerate(rows, start=2):
            capability_id = row["capability_id"].strip()

            if not capability_id:
                return fail(f"Row {number}: capability_id is required")

            if capability_id in seen:
                return fail(f"Duplicate capability_id: {capability_id}")

            seen.add(capability_id)

            if row["coverage_state"] not in COVERAGE_STATES:
                return fail(f"Row {number}: invalid coverage_state")

            if row["data_state"] not in DATA_STATES:
                return fail(f"Row {number}: invalid data_state")

        if policy.get("full_capability_coverage_claimed"):
            blockers = [
                row["capability_id"]
                for row in rows
                if row["coverage_state"] not in {
                    "UI_COMPLETE",
                    "NOT_USER_FACING",
                    "DEPRECATED_WITH_APPROVAL",
                }
                or row["data_state"] in {"UNKNOWN", "MOCK_ONLY"}
                or not row["evidence_path"].strip()
            ]

            if not rows or blockers:
                return fail("Full coverage claim lacks complete evidence")

        if args.base_ref:
            changed = changed_files(args.base_ref)
            product_changed = any(
                path.startswith(
                    ("frontend/", "backend/", "apps/", "services/", "packages/")
                )
                for path in changed
            )
            register_changed = str(REGISTER.relative_to(ROOT)) in changed

            if product_changed and not register_changed:
                return fail(
                    "Product code changed without traceability update"
                )

    except Exception as error:
        return fail(str(error))

    print(f"policy_status={policy['status']}")
    print(
        "full_capability_coverage_claimed="
        f"{str(policy['full_capability_coverage_claimed']).lower()}"
    )
    print(f"traceability_records={len(rows)}")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=FULL_CAPABILITY_UI_GOVERNANCE_ACTIVE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

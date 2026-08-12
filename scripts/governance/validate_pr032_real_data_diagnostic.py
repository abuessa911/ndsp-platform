#!/usr/bin/env python3
"""Validate PR-032 root-cause diagnostic accounting and safety."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR032 = ROOT / "docs/99-governance/pr-032-real-data-root-cause-diagnostic"

ALLOWED_BLOCKERS = {
    "EXPLICIT_DATA_SOURCE_MISSING",
    "REAL_DATA_STATE_MISSING",
    "CONNECTOR_EVIDENCE_MISSING",
    "ENDPOINT_NOT_RESPONSIVE",
    "PAYLOAD_EMPTY",
    "PAYLOAD_NOT_JSON",
    "PAYLOAD_ROOT_EMPTY",
}


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR032_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    diagnostics = rows(PR032 / "PR032_ROOT_CAUSE_DIAGNOSTIC.csv")
    actions = rows(PR032 / "PR032_REMEDIATION_ACTION_PLAN.csv")
    summary = json.loads(
        (PR032 / "PR032_SUMMARY.json").read_text(encoding="utf-8")
    )

    if len(diagnostics) != 2:
        return fail(
            f"Expected 2 diagnosed capabilities, found {len(diagnostics)}"
        )

    if not actions:
        return fail("Remediation plan is empty")

    if any(row["closure_state"] != "REMAINS_OPEN" for row in diagnostics):
        return fail("Diagnostic PR cannot close capabilities")

    blockers = {row["blocker"] for row in actions}
    if not blockers.issubset(ALLOWED_BLOCKERS):
        return fail("Unknown blocker classification detected")

    if summary["capabilities_closed"] != 0:
        return fail("Diagnostic PR cannot close capabilities")

    if summary["traceability_rows_modified"] != 0:
        return fail("Diagnostic PR cannot modify Traceability")

    if summary["runtime_changes"] != "none":
        return fail("Runtime changes are forbidden")

    if summary["services_restarted"] != 0:
        return fail("Service restarts are forbidden")

    if summary["mutating_requests_executed"] != 0:
        return fail("Mutating requests are forbidden")

    if summary["payload_values_persisted"] is not False:
        return fail("Payload values must not be persisted")

    print("input_capability_count=2")
    print("diagnosed_capability_count=2")
    print(f"blocker_record_count={len(actions)}")
    print("diagnostic_accounting=PASS")
    print("blocker_classification=PASS")
    print("remediation_plan_validation=PASS")
    print("runtime_safety=PASS")
    print("traceability_rows_modified=0")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR032_REAL_DATA_DIAGNOSTIC_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

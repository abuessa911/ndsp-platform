#!/usr/bin/env python3
"""Validate PR-062 audit artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


AUDIT_RELATIVE = Path(
    "docs/99-governance/pr-062-cot-direction-time-backend-audit"
)

REQUIRED_FILES = (
    "README.md",
    "PR-062-COT-DIRECTION-TIME-BACKEND-AUDIT.md",
    "PR062_LOGIC_INVENTORY.csv",
    "PR062_LOGIC_INVENTORY.json",
    "PR062_CODE_IMPACT_MAP.csv",
    "PR062_CODE_IMPACT_MAP.json",
    "PR062_UNRESOLVED_ITEMS.csv",
    "PR062_SUMMARY.json",
)


def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR062_COT_DIRECTION_TIME_BACKEND_AUDIT_INVALID")
    return 1


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    audit_dir = root / AUDIT_RELATIVE

    for name in REQUIRED_FILES:
        path = audit_dir / name
        if not path.is_file() or path.stat().st_size == 0:
            return fail(f"Missing or empty artifact: {name}")
        print(f"{name}: OK")

    summary = json.loads(
        (audit_dir / "PR062_SUMMARY.json").read_text(encoding="utf-8")
    )
    inventory_json = json.loads(
        (audit_dir / "PR062_LOGIC_INVENTORY.json").read_text(
            encoding="utf-8"
        )
    )
    impact_json = json.loads(
        (audit_dir / "PR062_CODE_IMPACT_MAP.json").read_text(
            encoding="utf-8"
        )
    )

    with (audit_dir / "PR062_LOGIC_INVENTORY.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        inventory_csv = list(csv.DictReader(handle))

    with (audit_dir / "PR062_CODE_IMPACT_MAP.csv").open(
        encoding="utf-8",
        newline="",
    ) as handle:
        impact_csv = list(csv.DictReader(handle))

    required_summary = {
        "candidate_files_scanned",
        "logic_candidate_file_count",
        "impact_map_record_count",
        "direction_candidate_count",
        "time_candidate_count",
        "approved_direction_rule",
        "approved_investment_rule",
        "approved_speculation_rule",
        "approved_time_rule",
        "approved_public_rule",
        "approved_shadow_rule",
        "traceability_rows_modified",
        "product_code_changes",
        "production_services_restarted",
        "mutating_requests_executed",
        "runtime_changes",
        "validation",
        "status",
    }

    missing = sorted(required_summary - set(summary))
    if missing:
        return fail("Summary keys missing: " + ", ".join(missing))

    if summary["candidate_files_scanned"] <= 0:
        return fail("No candidate files were scanned")

    if summary["logic_candidate_file_count"] <= 0:
        return fail("No logic candidates were discovered")

    if summary["logic_candidate_file_count"] != len(inventory_json):
        return fail("Inventory JSON accounting mismatch")

    if len(inventory_csv) != len(inventory_json):
        return fail("Inventory CSV/JSON mismatch")

    if summary["impact_map_record_count"] != len(impact_json):
        return fail("Impact JSON accounting mismatch")

    if len(impact_csv) != len(impact_json):
        return fail("Impact CSV/JSON mismatch")

    risk_total = sum(
        int(summary[key])
        for key in (
            "critical_risk_count",
            "high_risk_count",
            "medium_risk_count",
            "low_risk_count",
        )
    )
    if risk_total != summary["impact_map_record_count"]:
        return fail("Risk accounting mismatch")

    if summary["approved_direction_rule"] != "delta = long - short":
        return fail("Approved direction rule changed")

    if summary["traceability_rows_modified"] != 0:
        return fail("Traceability rows were modified")

    if summary["product_code_changes"] != 0:
        return fail("Product code changes were reported")

    if summary["production_services_restarted"] != 0:
        return fail("Production service restart was reported")

    if summary["mutating_requests_executed"] != 0:
        return fail("Mutating request execution was reported")

    if summary["runtime_changes"] != "none":
        return fail("Runtime changes are not none")

    if summary["validation"] != "PASS":
        return fail("Summary validation is not PASS")

    if summary["status"] != "COT_DIRECTION_TIME_BACKEND_AUDIT_COMPLETE":
        return fail("Unexpected summary status")

    checksums_path = audit_dir / "PR062_SHA256SUMS.txt"
    if not checksums_path.is_file():
        return fail("Checksum manifest is missing")

    for line in checksums_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(None, 1)
        relative = relative.strip()
        target = root / relative
        if not target.is_file():
            return fail(f"Checksum target missing: {relative}")
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            return fail(f"Checksum mismatch: {relative}")

    print("inventory_accounting=PASS")
    print("impact_accounting=PASS")
    print("risk_accounting=PASS")
    print("approved_rule_invariants=PASS")
    print("runtime_safety=PASS")
    print("checksum_validation=PASS")
    print("validation=PASS")
    print("status=PR062_COT_DIRECTION_TIME_BACKEND_AUDIT_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

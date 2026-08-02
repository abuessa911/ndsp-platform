#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

TRACE = ROOT / (
    "docs/99-governance/pr-018-full-capability-ui-governance/"
    "CAPABILITY_UI_TRACEABILITY.csv"
)
DOC = ROOT / (
    "docs/99-governance/"
    "pr-064c-runtime-engine-traceability-reconciliation"
)
ENGINE = "backend/services/decision_governance_core/main.cjs"

def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR064C_TRACEABILITY_RECONCILIATION_INVALID")
    return 1

required = [
    DOC / "README.md",
    DOC / "PR-064C-RUNTIME-ENGINE-TRACEABILITY-RECONCILIATION.md",
    DOC / "PR064C_TRACEABILITY_RECONCILIATION_AUDIT.csv",
    DOC / "PR064C_TRACEABILITY_RECONCILIATION_AUDIT.json",
    DOC / "PR064C_SUMMARY.json",
    DOC / "PR064C_SHA256SUMS.txt",
    TRACE,
]

for path in required:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing or empty file: {path.relative_to(ROOT)}"))
    print(f"{path.relative_to(ROOT)}: OK")

summary = json.loads(
    (DOC / "PR064C_SUMMARY.json").read_text(encoding="utf-8")
)

PR064_SUMMARY = (
    ROOT
    / "docs/99-governance/pr-064-canonical-direction-engine-correction"
    / "PR064_SUMMARY.json"
)

MUTABLE_TRACEABILITY_PATH = (
    "docs/99-governance/pr-018-full-capability-ui-governance/"
    "CAPABILITY_UI_TRACEABILITY.csv"
)

def approved_pr064_traceability_successor(relative: str) -> bool:
    if relative != MUTABLE_TRACEABILITY_PATH:
        return False

    if not PR064_SUMMARY.is_file():
        return False

    successor = json.loads(PR064_SUMMARY.read_text(encoding="utf-8"))

    return (
        successor.get("validation") == "PASS"
        and successor.get("status")
        == "CANONICAL_DIRECTION_ENGINE_CORRECTED_SHADOW_ONLY"
        and successor.get("traceability_rows_changed") == 1
        and successor.get("new_capability_created") is False
        and successor.get("execution_mode") == "SHADOW_ONLY"
        and successor.get("deployment_authorized") is False
        and successor.get("runtime_changes") == "none"
    )
audit = json.loads(
    (DOC / "PR064C_TRACEABILITY_RECONCILIATION_AUDIT.json").read_text(
        encoding="utf-8"
    )
)

expected = {
    "traceability_rows_changed": 1,
    "new_capability_created": False,
    "traceability_status_preserved": True,
    "product_source_recovery_accounted": "PASS",
    "behavior_changes": 0,
    "direction_logic_changes": 0,
    "systemd_changes": 0,
    "nginx_changes": 0,
    "database_changes": 0,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "validation": "PASS",
    "status": "RUNTIME_ENGINE_TRACEABILITY_RECONCILED",
}

for key, value in expected.items():
    if summary.get(key) != value:
        raise SystemExit(
            fail(f"Summary invariant mismatch: {key}={summary.get(key)!r}")
        )

if audit.get("new_capability_created") is not False:
    raise SystemExit(fail("Audit incorrectly creates a capability"))

if audit.get("status_preserved") is not True:
    raise SystemExit(fail("Audit did not preserve evidence status"))

with TRACE.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

matching = [
    row
    for row in rows
    if ENGINE in "|".join(str(value) for value in row.values())
]

runtime_records = [
    row
    for row in matching
    if str(row.get("capability_name", "")).strip().lower()
    == "ndsp decision governance core"
    and "ndsp-decision_governance_core.service"
    in str(row.get("runtime_service", ""))
]

capability_records = [
    row
    for row in matching
    if str(row.get("capability_name", "")).strip().lower()
    == "validate decision"
    and (
        "::validateDecision"
        in str(row.get("source_or_algorithm", ""))
        or "/api/governance/evaluate"
        in str(row.get("endpoint_or_contract", ""))
    )
]

if len(runtime_records) != 1:
    raise SystemExit(
        fail(
            "Expected exactly one runtime-service mapping for recovered engine; "
            f"found {len(runtime_records)}"
        )
    )

if len(capability_records) != 1:
    raise SystemExit(
        fail(
            "Expected exactly one functional-capability mapping for recovered "
            f"engine; found {len(capability_records)}"
        )
    )

if len(matching) != 2:
    raise SystemExit(
        fail(
            "Expected exactly two classified engine mappings "
            "(runtime service + functional capability); "
            f"found {len(matching)}"
        )
    )

checksums = DOC / "PR064C_SHA256SUMS.txt"

for line in checksums.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    expected_hash, relative = line.split(None, 1)
    target = ROOT / relative.strip()

    if not target.is_file():
        raise SystemExit(fail(f"Checksum target missing: {relative.strip()}"))

    actual = hashlib.sha256(target.read_bytes()).hexdigest()

    if actual != expected_hash:
        normalized = relative.strip()

        if approved_pr064_traceability_successor(normalized):
            print(
                "approved_traceability_successor_change="
                f"{normalized}:PR064"
            )
        else:
            raise SystemExit(fail(f"Checksum mismatch: {normalized}"))

print("historical_traceability_baseline=PASS")
print("mutable_traceability_successor_compatibility=PASS")
print("canonical_traceability_update=PASS")
print("runtime_engine_mapping=PASS")
print("runtime_service_mapping_count=1")
print("functional_capability_mapping_count=1")
print("classified_engine_mapping_count=2")
print("single_row_reconciliation=PASS")
print("new_capability_created=false")
print("traceability_status_preserved=PASS")
print("behavior_changes=0")
print("direction_logic_changes=0")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR064C_TRACEABILITY_RECONCILIATION_VALID")

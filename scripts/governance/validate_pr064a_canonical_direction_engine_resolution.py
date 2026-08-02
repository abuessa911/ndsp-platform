#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = ROOT / "docs/99-governance/pr-064a-canonical-direction-engine-resolution"

FILES = [
    "README.md",
    "ADR-064-CANONICAL-DIRECTION-ENGINE.md",
    "PR064A_CANONICAL_TARGET.json",
    "PR064A_LOGIC_OWNERSHIP.csv",
    "PR064A_INTEGRATION_POINTS.csv",
    "PR064A_RESULT_STORE_MAP.csv",
    "PR064A_TDL_DECISIONS.json",
    "PR064A_FILE_ACTION_PLAN.csv",
    "PR064A_UNRESOLVED_ITEMS.csv",
    "PR064A_SUMMARY.json",
]

def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR064A_CANONICAL_DIRECTION_ENGINE_RESOLUTION_INVALID")
    return 1

for relative in FILES:
    path = BASE / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing or empty artifact: {relative}"))
    print(f"{relative}: OK")

summary = json.loads(
    (BASE / "PR064A_SUMMARY.json").read_text(encoding="utf-8")
)
target = json.loads(
    (BASE / "PR064A_CANONICAL_TARGET.json").read_text(encoding="utf-8")
)
tdl = json.loads(
    (BASE / "PR064A_TDL_DECISIONS.json").read_text(encoding="utf-8")
)

if summary["product_code_changes"] != 0:
    raise SystemExit(fail("Product code changes were reported"))

if summary["runtime_changes"] != "none":
    raise SystemExit(fail("Runtime changes are not none"))

if summary["implementation_authorized"] is not False:
    raise SystemExit(fail("Implementation was incorrectly authorized"))

if summary["human_approval_required"] is not True:
    raise SystemExit(fail("Human approval requirement is missing"))

if summary["unresolved_rules_resolved"] is not False:
    raise SystemExit(fail("Unresolved rules were incorrectly marked resolved"))

if target["creation_allowed_before_approval"] is not False:
    raise SystemExit(fail("Canonical path creation was incorrectly allowed"))

if target["raw_data_gateway_may_publish_direction"] is not False:
    raise SystemExit(fail("Raw data gateway may not publish final direction"))

if tdl["investment"]["day_control"] != "DISABLED":
    raise SystemExit(fail("Investment Day Control is not disabled"))

if tdl["investment"]["tdl_ml"] != "DISABLED":
    raise SystemExit(fail("Investment TDL-M&L is not disabled"))

if tdl["investment"]["tdl_s"] != "DISABLED":
    raise SystemExit(fail("Investment TDL-S is not disabled"))

if summary["core_expanded_isolation"] != "PASS":
    raise SystemExit(fail("CORE/EXPANDED isolation is not PASS"))

checksums = BASE / "PR064A_SHA256SUMS.txt"
if not checksums.is_file():
    raise SystemExit(fail("Checksum manifest is missing"))

for line in checksums.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    expected, relative = line.split(None, 1)
    target_path = ROOT / relative.strip()

    if not target_path.is_file():
        raise SystemExit(fail(f"Checksum target missing: {relative.strip()}"))

    actual = hashlib.sha256(target_path.read_bytes()).hexdigest()

    if actual != expected:
        raise SystemExit(fail(f"Checksum mismatch: {relative.strip()}"))

print("canonical_target_package=PASS")
print("logic_ownership_map=PASS")
print("integration_point_map=PASS")
print("result_store_logical_map=PASS")
print("tdl_decision_safety=PASS")
print("file_action_plan=PASS")
print("human_approval_gate=PASS")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR064A_CANONICAL_DIRECTION_ENGINE_RESOLUTION_VALID")

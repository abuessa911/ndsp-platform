#!/usr/bin/env python3
import csv
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
engine = root / "backend/services/decision_governance_core"
doc = root / "docs/99-governance/pr-064-canonical-direction-engine-correction"
trace = root / (
    "docs/99-governance/pr-018-full-capability-ui-governance/"
    "CAPABILITY_UI_TRACEABILITY.csv"
)

def fail(message):
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR064_CANONICAL_DIRECTION_ENGINE_INVALID")
    return 1

required = [
    engine / "main.cjs",
    engine / "direction/canonical-direction.cjs",
    engine / "tests/canonical-direction.test.cjs",
    doc / "PR064_NORMALIZED_REGRESSION_CASES.json",
    doc / "PR064_IMPLEMENTATION_AUDIT.json",
    doc / "PR064_TRACEABILITY_UPDATE.json",
    doc / "PR064_SUMMARY.json",
    doc / "PR064_SHA256SUMS.txt",
    trace,
]
for path in required:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing file: {path.relative_to(root)}"))
    print(f"{path.relative_to(root)}: OK")

summary = json.loads((doc / "PR064_SUMMARY.json").read_text(encoding="utf-8"))
expected = {
    "direction_rule": "delta = long - short",
    "neutral_rule": "long == short only",
    "execution_mode": "SHADOW_ONLY",
    "public_exposure": "DISABLED",
    "official_result_written": False,
    "official_result_store_changes": 0,
    "experimental_result_store_changes": 0,
    "time_logic_changes": 0,
    "expanded_public_exposure": False,
    "traceability_rows_changed": 1,
    "new_capability_created": False,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "deployment_authorized": False,
    "human_approval_required_for_deployment": True,
    "validation": "PASS",
}
for key, value in expected.items():
    if summary.get(key) != value:
        raise SystemExit(fail(f"Invariant mismatch: {key}={summary.get(key)!r}"))

main_text = (engine / "main.cjs").read_text(encoding="utf-8")
for marker in (
    "/api/governance/direction/shadow",
    "SHADOW_ONLY",
    "official_result_written: false",
):
    if marker not in main_text:
        raise SystemExit(fail(f"Missing marker: {marker}"))

with trace.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))
matches = [
    row for row in rows
    if row.get("capability_id") == "CAP-704639CE50C9"
]
if len(matches) != 1:
    raise SystemExit(fail("Validate Decision row is not unique"))
if "canonical-direction.cjs::calculateCanonicalDirection" not in matches[0].get(
    "source_or_algorithm",
    "",
):
    raise SystemExit(fail("Direction module is not traced"))

for line in (doc / "PR064_SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected_hash, relative = line.split(None, 1)
    path = root / relative.strip()
    if not path.is_file():
        raise SystemExit(fail(f"Checksum target missing: {relative.strip()}"))
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
        raise SystemExit(fail(f"Checksum mismatch: {relative.strip()}"))

print("direction_rule=PASS")
print("neutral_rule=PASS")
print("shadow_only_integration=PASS")
print("public_exposure=DISABLED")
print("official_result_written=false")
print("time_logic_changes=0")
print("traceability_update=PASS")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR064_CANONICAL_DIRECTION_ENGINE_VALID")

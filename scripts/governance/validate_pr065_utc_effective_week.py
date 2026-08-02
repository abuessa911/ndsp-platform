#!/usr/bin/env python3
import csv
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
doc = root / "docs/99-governance/pr-065-utc-effective-week-correction"
module = root / (
    "backend/services/decision_governance_core/"
    "time/canonical-effective-week.cjs"
)
trace = root / (
    "docs/99-governance/pr-018-full-capability-ui-governance/"
    "CAPABILITY_UI_TRACEABILITY.csv"
)

def fail(message):
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR065_UTC_EFFECTIVE_WEEK_INVALID")
    return 1

summary = json.loads(
    (doc / "PR065_SUMMARY.json").read_text(encoding="utf-8")
)

expected = {
    "timezone": "UTC",
    "week_start": "MONDAY_00_00_00_UTC",
    "interval_semantics": "[effective_from,effective_until)",
    "effective_from_inclusive": True,
    "effective_until_exclusive": True,
    "runtime_integration_changes": 0,
    "direction_logic_changes": 0,
    "traceability_rows_changed": 1,
    "new_capability_created": False,
    "deployment_authorized": False,
    "runtime_changes": "none",
    "validation": "PASS",
}

for key, value in expected.items():
    if summary.get(key) != value:
        raise SystemExit(
            fail(f"Invariant mismatch: {key}={summary.get(key)!r}")
        )

with trace.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

matches = [
    row
    for row in rows
    if "canonical-effective-week.cjs::calculateEffectiveWeek"
    in row.get("source_or_algorithm", "")
]

if len(matches) != 1:
    raise SystemExit(
        fail(f"Expected one time mapping; found {len(matches)}")
    )

for line in (doc / "PR065_SHA256SUMS.txt").read_text(
    encoding="utf-8"
).splitlines():
    if not line.strip():
        continue

    expected_hash, relative = line.split(None, 1)
    path = root / relative.strip()

    if not path.is_file():
        raise SystemExit(
            fail(f"Checksum target missing: {relative.strip()}")
        )

    actual = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual != expected_hash:
        raise SystemExit(
            fail(f"Checksum mismatch: {relative.strip()}")
        )

print("timezone=UTC")
print("week_start=MONDAY_00_00_00_UTC")
print("interval_semantics=HALF_OPEN")
print("direction_logic_changes=0")
print("runtime_integration_changes=0")
print("traceability_update=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR065_UTC_EFFECTIVE_WEEK_VALID")

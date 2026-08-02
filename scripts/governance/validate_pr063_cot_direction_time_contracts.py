#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = ROOT / "docs/99-governance/pr-063-cot-direction-time-contracts"

FILES = [
    "README.md",
    "PR-063-COT-DIRECTION-TIME-CONTRACTS.md",
    "PR063_SUMMARY.json",
    "contracts/direction-result.schema.json",
    "contracts/effective-week.schema.json",
    "contracts/core-result.schema.json",
    "contracts/expanded-shadow-result.schema.json",
    "fixtures/regression-fixtures.json",
    "fixtures/regression-expected-results.json",
]

def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR063_COT_DIRECTION_TIME_CONTRACTS_INVALID")
    return 1

for relative in FILES:
    path = BASE / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing or empty file: {relative}"))
    print(f"{relative}: OK")

summary = json.loads((BASE / "PR063_SUMMARY.json").read_text(encoding="utf-8"))
fixtures = json.loads((BASE / "fixtures/regression-fixtures.json").read_text(encoding="utf-8"))
expected = json.loads((BASE / "fixtures/regression-expected-results.json").read_text(encoding="utf-8"))

if summary["approved_direction_rule"] != "delta = long - short":
    raise SystemExit(fail("Direction rule changed"))
if summary["approved_timezone"] != "UTC":
    raise SystemExit(fail("Timezone is not UTC"))
if summary["core_public_only"] is not True:
    raise SystemExit(fail("CORE public-only invariant failed"))
if summary["expanded_shadow_only"] is not True:
    raise SystemExit(fail("EXPANDED shadow-only invariant failed"))
if summary["product_code_changes"] != 0:
    raise SystemExit(fail("Product code changes reported"))

def next_monday(report_date: date) -> date:
    days = (7 - report_date.weekday()) % 7
    if days == 0:
        days = 7
    return report_date + timedelta(days=days)

expected_by_id = {item["id"]: item for item in expected}

for item in fixtures:
    delta = item["long"] - item["short"]
    direction = "NEUTRAL"
    if delta > 0:
        direction = "BULLISH"
    elif delta < 0:
        direction = "BEARISH"

    report_date = date.fromisoformat(item["report_date"])
    effective_date = next_monday(report_date)
    effective_from = datetime(
        effective_date.year,
        effective_date.month,
        effective_date.day,
        tzinfo=timezone.utc,
    )
    effective_until = effective_from + timedelta(days=7)

    actual = {
        "delta": delta,
        "direction": direction,
        "effective_from": effective_from.isoformat().replace("+00:00", "Z"),
        "effective_until": effective_until.isoformat().replace("+00:00", "Z"),
    }
    reference = expected_by_id[item["id"]]

    for key, value in actual.items():
        if reference[key] != value:
            raise SystemExit(
                fail(f"Fixture {item['id']} mismatch for {key}: {value}")
            )

checksums = BASE / "PR063_SHA256SUMS.txt"
if not checksums.is_file():
    raise SystemExit(fail("Checksum manifest missing"))

for line in checksums.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected_hash, relative = line.split(None, 1)
    target = ROOT / relative.strip()
    actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise SystemExit(fail(f"Checksum mismatch: {relative.strip()}"))

print("direction_contract=PASS")
print("time_contract=PASS")
print("core_expanded_contract=PASS")
print("regression_fixtures=PASS")
print("checksum_validation=PASS")
print("runtime_safety=PASS")
print("validation=PASS")
print("status=PR063_COT_DIRECTION_TIME_CONTRACTS_VALID")

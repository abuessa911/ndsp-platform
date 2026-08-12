#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
BASE = ROOT / "docs/99-governance/pr-070-runtime-path-inventory"

FILES = [
    "README.md",
    "PR-070-RUNTIME-PATH-INVENTORY.md",
    "PR070_PATH_INVENTORY.csv",
    "PR070_SYSTEMD_INVENTORY.csv",
    "PR070_NGINX_INVENTORY.csv",
    "PR070_REPOSITORY_REFERENCES.csv",
    "PR070_SUMMARY.json",
]

def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR070_RUNTIME_PATH_INVENTORY_INVALID")
    return 1

for relative in FILES:
    path = BASE / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing or empty file: {relative}"))
    print(f"{relative}: OK")

summary = json.loads((BASE / "PR070_SUMMARY.json").read_text(encoding="utf-8"))

for key in (
    "systemd_mutations",
    "nginx_mutations",
    "files_deleted",
    "files_moved",
    "production_services_restarted",
    "mutating_requests_executed",
):
    if summary[key] != 0:
        raise SystemExit(fail(f"Unsafe mutation reported: {key}"))

if summary["runtime_changes"] != "none":
    raise SystemExit(fail("Runtime changes are not none"))
if summary["scan_mode"] != "READ_ONLY":
    raise SystemExit(fail("Scan mode is not READ_ONLY"))
if summary["status"] != "RUNTIME_PATH_INVENTORY_COMPLETE":
    raise SystemExit(fail("Unexpected summary status"))

checksums = BASE / "PR070_SHA256SUMS.txt"
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

print("path_inventory=PASS")
print("systemd_inventory=PASS")
print("nginx_inventory=PASS")
print("repository_reference_inventory=PASS")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR070_RUNTIME_PATH_INVENTORY_VALID")

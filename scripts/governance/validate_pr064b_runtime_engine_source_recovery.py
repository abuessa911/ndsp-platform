#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

RECOVERED = ROOT / "backend/services/decision_governance_core"
DOC = ROOT / "docs/99-governance/pr-064b-runtime-engine-source-recovery"

REQUIRED_RECOVERED = [
    "main.cjs",
    "framework-adapter.cjs",
    "package.json",
    "service.yaml",
    "README.md",
]

REQUIRED_GOVERNANCE = [
    "README.md",
    "PR-064B-RUNTIME-ENGINE-SOURCE-RECOVERY.md",
    "PR064B_RUNTIME_SOURCE_MANIFEST.csv",
    "PR064B_RECOVERED_SOURCE_MANIFEST.csv",
    "PR064B_EXCLUSION_REPORT.csv",
    "PR064B_SYSTEMD_EVIDENCE.txt",
    "PR064B_SUMMARY.json",
    "PR064B_SHA256SUMS.txt",
]

FORBIDDEN_PARTS = {
    ".git",
    ".cache",
    "cache",
    "coverage",
    "dist",
    "logs",
    "node_modules",
    "runtime",
    "tmp",
    "__pycache__",
}

FORBIDDEN_SUFFIXES = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
    ".pid",
    ".sock",
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".pyc",
    ".pyo",
}

PRIVATE_KEY = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)

URI_CREDENTIALS = re.compile(
    rb"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis):\/\/"
    rb"[^:\s\/]+:[^@\s\/]+@"
)

def fail(message: str) -> int:
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR064B_RUNTIME_ENGINE_SOURCE_RECOVERY_INVALID")
    return 1

for relative in REQUIRED_RECOVERED:
    path = RECOVERED / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing recovered source file: {relative}"))
    print(f"{path.relative_to(ROOT)}: OK")

for relative in REQUIRED_GOVERNANCE:
    path = DOC / relative
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(fail(f"Missing governance artifact: {relative}"))
    print(f"{path.relative_to(ROOT)}: OK")

for path in RECOVERED.rglob("*"):
    relative = path.relative_to(RECOVERED)

    if any(part in FORBIDDEN_PARTS for part in relative.parts):
        raise SystemExit(fail(f"Forbidden recovered path: {relative}"))

    if path.is_symlink():
        raise SystemExit(fail(f"Recovered symlink is not allowed: {relative}"))

    if not path.is_file():
        continue

    if path.suffix.lower() in FORBIDDEN_SUFFIXES:
        raise SystemExit(fail(f"Forbidden recovered suffix: {relative}"))

    if path.name.startswith(".env"):
        raise SystemExit(fail(f"Environment file recovered: {relative}"))

    data = path.read_bytes()

    if PRIVATE_KEY.search(data):
        raise SystemExit(fail(f"Private key detected: {relative}"))

    if URI_CREDENTIALS.search(data):
        raise SystemExit(fail(f"Credential-bearing URI detected: {relative}"))

summary = json.loads(
    (DOC / "PR064B_SUMMARY.json").read_text(encoding="utf-8")
)

expected_invariants = {
    "runtime_engine_source_found": "PASS",
    "secrets_excluded": "PASS",
    "runtime_data_excluded": "PASS",
    "node_modules_excluded": "PASS",
    "source_runtime_checksum_inventory": "PASS",
    "behavior_changes": 0,
    "direction_logic_changes": 0,
    "systemd_changes": 0,
    "nginx_changes": 0,
    "database_changes": 0,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "validation": "PASS",
    "status": "RUNTIME_ENGINE_SOURCE_RECOVERED",
}

for key, expected in expected_invariants.items():
    actual = summary.get(key)
    if actual != expected:
        raise SystemExit(
            fail(f"Summary invariant mismatch: {key}={actual!r}")
        )

def load_manifest(name: str) -> list[dict[str, str]]:
    with (DOC / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

source_manifest = load_manifest("PR064B_RUNTIME_SOURCE_MANIFEST.csv")
recovered_manifest = load_manifest("PR064B_RECOVERED_SOURCE_MANIFEST.csv")

if source_manifest != recovered_manifest:
    raise SystemExit(fail("Source and recovered manifests differ"))

if len(source_manifest) != summary["runtime_engine_files_recovered"]:
    raise SystemExit(fail("Recovered file accounting mismatch"))

for row in recovered_manifest:
    relative = Path(row["path"])
    path = RECOVERED / relative

    if not path.is_file():
        raise SystemExit(fail(f"Manifest target missing: {relative}"))

    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()

    if actual_hash != row["sha256"]:
        raise SystemExit(fail(f"Recovered hash mismatch: {relative}"))

entry = (RECOVERED / "main.cjs").read_text(
    encoding="utf-8",
    errors="replace",
)

for route in (
    "/health",
    "/api/governance/evaluate",
    "/api/governance/submit",
):
    if route not in entry:
        raise SystemExit(fail(f"Expected route missing: {route}"))

checksums = DOC / "PR064B_SHA256SUMS.txt"

for line in checksums.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue

    expected, relative = line.split(None, 1)
    target = ROOT / relative.strip()

    if not target.is_file():
        raise SystemExit(fail(f"Checksum target missing: {relative.strip()}"))

    actual = hashlib.sha256(target.read_bytes()).hexdigest()

    if actual != expected:
        raise SystemExit(fail(f"Checksum mismatch: {relative.strip()}"))

print("runtime_engine_source_found=PASS")
print("runtime_engine_files_recovered=PASS")
print("secrets_excluded=PASS")
print("runtime_data_excluded=PASS")
print("node_modules_excluded=PASS")
print("source_runtime_checksum_inventory=PASS")
print("behavior_changes=0")
print("direction_logic_changes=0")
print("systemd_changes=0")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR064B_RUNTIME_ENGINE_SOURCE_RECOVERY_VALID")

#!/usr/bin/env python3
import csv
import hashlib
import json
import sys
from pathlib import Path

root = Path(
    sys.argv[1] if len(sys.argv) > 1 else "."
).resolve()

doc = (
    root
    / "docs/99-governance/pr-066-core-expanded-shadow-execution"
)

runner = (
    root
    / "backend/services/decision_governance_core"
    / "execution/core-expanded-shadow-runner.cjs"
)

traceability = (
    root
    / "docs/99-governance/pr-018-full-capability-ui-governance"
    / "CAPABILITY_UI_TRACEABILITY.csv"
)

def fail(message):
    print(f"error={message}")
    print("validation=FAIL")
    print("status=PR066_CORE_EXPANDED_SHADOW_INVALID")
    return 1

required = [
    runner,
    (
        root
        / "backend/services/decision_governance_core"
        / "tests/core-expanded-shadow-runner.test.cjs"
    ),
    doc / "PR066_SUMMARY.json",
    doc / "PR066_TRACEABILITY_EVIDENCE.json",
    doc / "PR066_SAFETY_AUDIT.json",
    doc / "PR066_SHA256SUMS.txt",
    traceability,
]

for path in required:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(
            fail(f"Missing file: {path.relative_to(root)}")
        )

    print(f"{path.relative_to(root)}: OK")

summary = json.loads(
    (doc / "PR066_SUMMARY.json").read_text(
        encoding="utf-8"
    )
)

expected = {
    "execution_mode": "SHADOW_ONLY",
    "official_model": "CORE_V1",
    "official_result_write": False,
    "experimental_model": "EXPANDED_SHADOW",
    "experimental_result_write": False,
    "expanded_public_exposure": False,
    "automatic_promotion": False,
    "direction_contract_source": "PR-064",
    "time_contract_source": "PR-065",
    "central_traceability_mutated": False,
    "validate_decision_canonicality": "REVIEW_REQUIRED",
    "validate_decision_disposition": (
        "REFERENCE_ONLY_PENDING_HUMAN_REVIEW"
    ),
    "expected_cot_cycle_canonicality": "CANONICAL",
    "runtime_route_changes": 0,
    "database_changes": 0,
    "systemd_changes": 0,
    "nginx_changes": 0,
    "deployment_authorized": False,
    "human_approval_required_for_deployment": True,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "validation": "PASS",
}

for key, value in expected.items():
    if summary.get(key) != value:
        raise SystemExit(
            fail(
                f"Invariant mismatch: "
                f"{key}={summary.get(key)!r}"
            )
        )

runner_text = runner.read_text(encoding="utf-8")

for marker in (
    'execution_mode: "SHADOW_ONLY"',
    "official_result_write: false",
    "experimental_result_write: false",
    "expanded_public_exposure: false",
    "automatic_promotion: false",
):
    if marker not in runner_text:
        raise SystemExit(
            fail(f"Runner safety marker missing: {marker}")
        )

trace_evidence = json.loads(
    (doc / "PR066_TRACEABILITY_EVIDENCE.json").read_text(
        encoding="utf-8"
    )
)

if trace_evidence.get("central_traceability_mutated") is not False:
    raise SystemExit(
        fail("Central Traceability mutation is not disabled")
    )

expected_ids = {
    "CAP-704639CE50C9",
    "CAP-C807F0E54F0D",
}

actual_ids = {
    item.get("capability_id")
    for item in trace_evidence.get("capabilities", [])
}

if actual_ids != expected_ids:
    raise SystemExit(
        fail(
            "Traceability evidence capability IDs mismatch: "
            f"{sorted(actual_ids)}"
        )
    )

with traceability.open(
    encoding="utf-8-sig",
    newline="",
) as handle:
    rows = list(csv.DictReader(handle))

expected_canonicality = {
    "CAP-704639CE50C9": "REVIEW_REQUIRED",
    "CAP-C807F0E54F0D": "CANONICAL",
}

for capability_id in expected_ids:
    matches = [
        row
        for row in rows
        if row.get("capability_id") == capability_id
    ]

    if len(matches) != 1:
        raise SystemExit(
            fail(
                f"Traceability capability mapping invalid: "
                f"{capability_id}"
            )
        )

    actual_canonicality = matches[0].get("canonicality")

    if actual_canonicality != expected_canonicality[capability_id]:
        raise SystemExit(
            fail(
                "Traceability canonicality mismatch: "
                f"{capability_id}:"
                f"expected={expected_canonicality[capability_id]}:"
                f"actual={actual_canonicality}"
            )
        )

for line in (
    doc / "PR066_SHA256SUMS.txt"
).read_text(encoding="utf-8").splitlines():

    if not line.strip():
        continue

    expected_hash, relative = line.split(None, 1)
    path = root / relative.strip()

    if not path.is_file():
        raise SystemExit(
            fail(
                f"Checksum target missing: "
                f"{relative.strip()}"
            )
        )

    actual_hash = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if actual_hash != expected_hash:
        raise SystemExit(
            fail(
                f"Checksum mismatch: "
                f"{relative.strip()}"
            )
        )

print("core_model=CORE_V1")
print("expanded_model=EXPANDED_SHADOW")
print("execution_mode=SHADOW_ONLY")
print("official_result_write=false")
print("experimental_result_write=false")
print("expanded_public_exposure=false")
print("automatic_promotion=false")
print("central_traceability_mutated=false")
print("validate_decision_canonicality=REVIEW_REQUIRED")
print("expected_cot_cycle_canonicality=CANONICAL")
print("validate_decision_disposition=REFERENCE_ONLY_PENDING_HUMAN_REVIEW")
print("traceability_evidence=PASS")
print("runtime_safety=PASS")
print("checksum_validation=PASS")
print("validation=PASS")
print("status=PR066_CORE_EXPANDED_SHADOW_VALID")

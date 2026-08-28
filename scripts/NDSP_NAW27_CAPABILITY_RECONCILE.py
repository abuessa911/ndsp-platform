#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

CAP_ID_RE = re.compile(r"^CAP-(\d{4})$")
ALLOWED_STATES = {
    "CONTRIBUTED",
    "BLOCKED",
    "NOT_APPLICABLE",
    "UNAVAILABLE",
    "STALE",
    "PARTIAL",
    "GOVERNANCE_PROTECTED",
}


def governed_state(record: dict[str, Any]) -> tuple[str, str]:
    status = str(record.get("status") or "").upper()
    classification = str(record.get("classification") or "").upper()
    implementation = str(record.get("implementation_status") or "").upper()

    if "DOCUMENTATION_ONLY" in {status, classification, implementation}:
        return "NOT_APPLICABLE", "DOCUMENTATION_ONLY_DISCOVERY_RECORD"

    if status in {"DISCOVERED", "HISTORICAL_REFERENCE", "NOT_APPROVED", ""}:
        return "UNAVAILABLE", "DISCOVERY_EVIDENCE_NOT_RUNTIME_AUTHORITY"

    if status in {"VERIFIED", "ACTIVE"}:
        evidence = record.get("evidence") or []
        runtime_proven = any(
            isinstance(row, dict)
            and str(row.get("runtime_evidence") or "").upper()
            not in {"", "NOT_EXECUTED", "UNKNOWN", "DISCOVERY_ONLY"}
            for row in evidence
        )
        if runtime_proven:
            return "CONTRIBUTED", "VERIFIED_RUNTIME_EVIDENCE"
        return "UNAVAILABLE", "STATUS_REQUIRES_RUNTIME_EVIDENCE"

    return "UNAVAILABLE", "UNVERIFIED_DISCOVERY_RECORD"


def reconcile(root: Path, expected_count: int) -> dict[str, Any]:
    contracts_dir = root / "governance" / "contracts" / "01_CAPABILITY_CONTRACTS"
    files = sorted(contracts_dir.glob("CAP-*.contract.json"))
    entries: list[dict[str, Any]] = []
    parse_errors: list[str] = []
    ids: list[int] = []

    for path in files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # fail closed, but never expose file contents
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue

        contract_id = str(record.get("contract_id") or "")
        match = CAP_ID_RE.fullmatch(contract_id)
        if not match:
            parse_errors.append(f"{path.name}:INVALID_CONTRACT_ID")
            continue

        numeric_id = int(match.group(1))
        ids.append(numeric_id)
        state, disposition = governed_state(record)
        if state not in ALLOWED_STATES:
            parse_errors.append(f"{path.name}:INVALID_GOVERNED_STATE")
            continue

        entries.append(
            {
                "contract_id": contract_id,
                "governed_state": state,
                "disposition": disposition,
                "contract_status": str(record.get("status") or "UNKNOWN"),
                "classification": str(record.get("classification") or "UNKNOWN"),
                "exposure": "INTERNAL_EVIDENCE_ONLY",
                "runtime_capability_claim": False,
            }
        )

    id_counts = Counter(ids)
    duplicates = sorted(value for value, count in id_counts.items() if count > 1)
    expected_ids = set(range(1, expected_count + 1))
    actual_ids = set(ids)
    missing_ids = sorted(expected_ids - actual_ids)
    out_of_range_ids = sorted(actual_ids - expected_ids)
    state_counts = Counter(row["governed_state"] for row in entries)
    status_counts = Counter(row["contract_status"] for row in entries)

    global_reconciled = (
        len(files) == expected_count
        and len(entries) == expected_count
        and not parse_errors
        and not duplicates
        and not missing_ids
        and not out_of_range_ids
    )

    return {
        "ok": True,
        "contract": "NDSP_CAPABILITY_DISCOVERY_RECONCILIATION_V1",
        "semantics": {
            "record_namespace": "CAP discovery/evidence records",
            "record_count_is_runtime_capability_count": False,
            "activation_claim": False,
            "user_visible_individual_records": False,
            "purpose": "Account for every discovered CAP record without silently treating discovery as runtime activation.",
        },
        "expected_record_count": expected_count,
        "record_count": len(files),
        "parsed_record_count": len(entries),
        "global_reconciled": global_reconciled,
        "silent_omission_count": len(missing_ids) + len(parse_errors),
        "duplicate_numeric_ids": duplicates,
        "missing_numeric_ids": missing_ids,
        "out_of_range_numeric_ids": out_of_range_ids,
        "parse_error_count": len(parse_errors),
        "parse_errors": parse_errors,
        "governed_state_counts": dict(sorted(state_counts.items())),
        "contract_status_counts": dict(sorted(status_counts.items())),
        "entries": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--expected-count", type=int, default=311)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output).resolve()
    payload = reconcile(root, args.expected_count)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"CAP_RECORD_COUNT={payload['record_count']}")
    print(f"CAP_PARSED_RECORD_COUNT={payload['parsed_record_count']}")
    print(f"CAP_SILENT_OMISSION_COUNT={payload['silent_omission_count']}")
    print(f"CAP_GLOBAL_RECONCILED={'YES' if payload['global_reconciled'] else 'NO'}")
    print("CAP_RUNTIME_COUNT_CLAIM=NO")
    print("CAP_ACTIVATION_CLAIM=NO")
    return 0 if payload["global_reconciled"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

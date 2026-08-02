#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "docs/99-governance/pr-064a-canonical-direction-engine-resolution"
OUT.mkdir(parents=True, exist_ok=True)

PR062 = ROOT / "docs/99-governance/pr-062-cot-direction-time-backend-audit"
PR063 = ROOT / "docs/99-governance/pr-063-cot-direction-time-contracts"

impact = json.loads(
    (PR062 / "PR062_CODE_IMPACT_MAP.json").read_text(encoding="utf-8")
)
inventory = json.loads(
    (PR062 / "PR062_LOGIC_INVENTORY.json").read_text(encoding="utf-8")
)
with (PR062 / "PR062_UNRESOLVED_ITEMS.csv").open(
    encoding="utf-8",
    newline="",
) as handle:
    unresolved = list(csv.DictReader(handle))
contracts = json.loads(
    (PR063 / "PR063_SUMMARY.json").read_text(encoding="utf-8")
)

if contracts.get("validation") != "PASS":
    raise SystemExit("PR-063 contract validation is not PASS")

if contracts.get("approved_direction_rule") != "delta = long - short":
    raise SystemExit("Unexpected PR-063 direction rule")

if contracts.get("core_public_only") is not True:
    raise SystemExit("CORE public-only invariant is missing")

if contracts.get("expanded_shadow_only") is not True:
    raise SystemExit("EXPANDED shadow-only invariant is missing")

canonical_path = "backend/services/decision_governance_core/"
canonical_path_exists = (ROOT / canonical_path).exists()

high_risk = [
    row
    for row in impact
    if str(row.get("risk", "")).upper() in {"HIGH", "CRITICAL"}
]

if not high_risk:
    raise SystemExit("PR-062 high-risk evidence is unexpectedly empty")

def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

target = {
    "schema_version": "1.0",
    "decision": "CANONICAL_DIRECTION_ENGINE_TARGET",
    "decision_status": "PROPOSED_FOR_HUMAN_APPROVAL",
    "canonical_engine_path": canonical_path,
    "canonical_engine_path_exists": canonical_path_exists,
    "creation_allowed_before_approval": False,
    "runtime_language": "Node.js",
    "module_format": "CommonJS",
    "contract_source": (
        "docs/99-governance/pr-063-cot-direction-time-contracts/contracts/"
    ),
    "raw_data_gateway_role": "RAW_DATA_ONLY",
    "raw_data_gateway_may_publish_direction": False,
    "direction_rule": "delta = long - short",
    "neutral_rule": "long == short only",
    "public_result_model": "CORE",
    "expanded_mode": "SHADOW_MODE",
    "expanded_public_exposure": False,
    "human_approval_required": True,
}

(OUT / "PR064A_CANONICAL_TARGET.json").write_text(
    json.dumps(target, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

ownership_rows = []
for row in impact:
    categories = str(row.get("categories", ""))
    if "DIRECTION" not in categories and "TIME" not in categories:
        continue

    ownership_rows.append({
        "path": row.get("path", ""),
        "current_owner": row.get("owner", "DISCOVERY_REQUIRED"),
        "proposed_logic_owner": "decision_governance_core",
        "source_kind": row.get("source_kind", ""),
        "categories": categories,
        "risk": row.get("risk", ""),
        "human_review_required": "true",
        "decision_status": "PROPOSED",
    })

write_csv(
    OUT / "PR064A_LOGIC_OWNERSHIP.csv",
    ownership_rows,
    [
        "path",
        "current_owner",
        "proposed_logic_owner",
        "source_kind",
        "categories",
        "risk",
        "human_review_required",
        "decision_status",
    ],
)

integration_rows = []
for row in high_risk:
    path = str(row.get("path", ""))
    kind = str(row.get("source_kind", ""))
    action = str(row.get("recommended_action", ""))

    role = "RUNTIME_LOGIC"
    if kind == "CONTRACT":
        role = "CONTRACT_ADAPTER"
    elif kind == "INTEGRATION":
        role = "INTEGRATION_ADAPTER"

    integration_rows.append({
        "path": path,
        "current_role": role,
        "risk": row.get("risk", ""),
        "proposed_action": action,
        "canonical_target": canonical_path,
        "runtime_change_allowed_in_pr064a": "false",
        "implementation_stage": (
            "PR-064" if "TIME" not in str(row.get("categories", ""))
            else "PR-064_OR_PR-065_AFTER_REVIEW"
        ),
        "human_review_required": "true",
    })

write_csv(
    OUT / "PR064A_INTEGRATION_POINTS.csv",
    integration_rows,
    [
        "path",
        "current_role",
        "risk",
        "proposed_action",
        "canonical_target",
        "runtime_change_allowed_in_pr064a",
        "implementation_stage",
        "human_review_required",
    ],
)

store_rows = [
    {
        "store_name": "Official Result Store",
        "logical_owner": "decision_governance_core",
        "model": "CORE",
        "exposure": "PUBLIC_OFFICIAL",
        "writer": "decision_governance_core",
        "reader": "Public API",
        "physical_location": "TO_BE_IMPLEMENTED_AFTER_APPROVAL",
        "current_location_identified": "false",
        "decision_status": "PROPOSED",
    },
    {
        "store_name": "Experimental Result Store",
        "logical_owner": "decision_governance_core",
        "model": "EXPANDED",
        "exposure": "INTERNAL_SHADOW_ONLY",
        "writer": "decision_governance_core_shadow",
        "reader": "Internal Admin API",
        "physical_location": "TO_BE_IMPLEMENTED_AFTER_APPROVAL",
        "current_location_identified": "false",
        "decision_status": "PROPOSED",
    },
]

write_csv(
    OUT / "PR064A_RESULT_STORE_MAP.csv",
    store_rows,
    [
        "store_name",
        "logical_owner",
        "model",
        "exposure",
        "writer",
        "reader",
        "physical_location",
        "current_location_identified",
        "decision_status",
    ],
)

tdl = {
    "schema_version": "1.0",
    "decision_status": "PARTIALLY_RESOLVED_REQUIRES_HUMAN_APPROVAL",
    "investment": {
        "day_control": "DISABLED",
        "tdl_ml": "DISABLED",
        "tdl_s": "DISABLED",
        "reason": "PR-063 approved investment invariants",
    },
    "speculation": {
        "input_basis": "CHANGES_ONLY",
        "tdl_ml": "DISABLED_UNTIL_SEPARATE_SEMANTICS_APPROVAL",
        "tdl_s": "DISABLED_UNTIL_SEPARATE_SEMANTICS_APPROVAL",
        "day_control": "DISABLED_UNTIL_SEPARATE_SEMANTICS_APPROVAL",
        "invented_semantics_allowed": False,
    },
    "public_core": {
        "expanded_exposure": "DISABLED",
        "shadow_metadata_exposure": "DISABLED",
    },
}

(OUT / "PR064A_TDL_DECISIONS.json").write_text(
    json.dumps(tdl, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

inventory_by_path = {
    str(row.get("path", "")): row
    for row in inventory
}

action_rows = []
for row in impact:
    path = str(row.get("path", ""))
    risk = str(row.get("risk", ""))
    source_kind = str(row.get("source_kind", ""))
    recommended = str(row.get("recommended_action", "REVIEW"))
    categories = str(row.get("categories", ""))

    if source_kind == "CONTRACT":
        action = "CONTRACT_ONLY"
    elif source_kind == "TEST":
        action = "TEST_ONLY"
    elif risk in {"HIGH", "CRITICAL"} and source_kind == "INTEGRATION":
        action = "WRAP"
    elif risk in {"HIGH", "CRITICAL"}:
        action = "REPLACE"
    elif recommended == "REVIEW_CONFIGURATION":
        action = "REVIEW_REQUIRED"
    else:
        action = "KEEP_OR_WRAP"

    action_rows.append({
        "path": path,
        "source_kind": source_kind,
        "categories": categories,
        "risk": risk,
        "pr062_recommended_action": recommended,
        "pr064a_action": action,
        "evidence_flags": row.get("flags", "NONE"),
        "implementation_allowed_now": "false",
        "human_review_required": "true",
        "evidence_sample": inventory_by_path.get(path, {}).get(
            "evidence_sample",
            "",
        ),
    })

write_csv(
    OUT / "PR064A_FILE_ACTION_PLAN.csv",
    action_rows,
    [
        "path",
        "source_kind",
        "categories",
        "risk",
        "pr062_recommended_action",
        "pr064a_action",
        "evidence_flags",
        "implementation_allowed_now",
        "human_review_required",
        "evidence_sample",
    ],
)

resolution_map = {
    "UNR-001": (
        "TDL-M&L disabled in investment and disabled in speculation until "
        "separate semantics approval"
    ),
    "UNR-002": (
        "TDL-S disabled in investment and disabled in speculation until "
        "separate semantics approval"
    ),
    "UNR-003": (
        "Logical stores proposed; physical stores remain unidentified and "
        "must be implemented after approval"
    ),
    "UNR-004": (
        "High-risk integration candidates mapped; exact runtime call graph "
        "still requires PR-064 implementation review"
    ),
    "UNR-005": (
        "PR-063 contract remains authoritative; no new explicitness semantics "
        "introduced by PR-064A"
    ),
}

unresolved_rows = []
for row in unresolved:
    item_id = row.get("item_id", "")
    unresolved_rows.append({
        "item_id": item_id,
        "topic": row.get("topic", ""),
        "previous_status": row.get("status", ""),
        "pr064a_resolution": resolution_map.get(
            item_id,
            "No safe automatic resolution",
        ),
        "resolution_status": (
            "EXPLICITLY_DISABLED_PENDING_APPROVAL"
            if item_id in {"UNR-001", "UNR-002"}
            else "PARTIALLY_RESOLVED"
        ),
        "human_approval_required": "true",
    })

write_csv(
    OUT / "PR064A_UNRESOLVED_ITEMS.csv",
    unresolved_rows,
    [
        "item_id",
        "topic",
        "previous_status",
        "pr064a_resolution",
        "resolution_status",
        "human_approval_required",
    ],
)

risk_counts = Counter(
    str(row.get("risk", "UNKNOWN"))
    for row in impact
)

summary = {
    "schema_version": "1.0",
    "document": "PR-064A Canonical Direction Engine Resolution",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source_commit": subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip(),
    "decision_package_type": "ARCHITECTURE_AND_GOVERNANCE_ONLY",
    "canonical_engine_path": canonical_path,
    "canonical_engine_path_status": "PROPOSED_FOR_HUMAN_APPROVAL",
    "canonical_engine_path_exists": canonical_path_exists,
    "direction_logic_owner": "decision_governance_core",
    "direction_logic_owner_status": "PROPOSED_FOR_HUMAN_APPROVAL",
    "official_result_store": "Official Result Store",
    "official_result_store_status": "LOGICAL_MODEL_IDENTIFIED_PHYSICAL_STORE_PENDING",
    "experimental_result_store": "Experimental Result Store",
    "experimental_result_store_status": "LOGICAL_MODEL_IDENTIFIED_PHYSICAL_STORE_PENDING",
    "public_api_writer": "decision_governance_core",
    "public_api_writer_status": "PROPOSED",
    "internal_admin_api_writer": "decision_governance_core_shadow",
    "internal_admin_api_writer_status": "PROPOSED",
    "investment_day_control": "DISABLED",
    "investment_tdl": "DISABLED",
    "speculation_tdl": "DISABLED_PENDING_SEPARATE_APPROVAL",
    "core_expanded_isolation": "PASS",
    "high_risk_record_count": risk_counts["HIGH"],
    "critical_risk_record_count": risk_counts["CRITICAL"],
    "logic_ownership_record_count": len(ownership_rows),
    "integration_point_count": len(integration_rows),
    "file_action_record_count": len(action_rows),
    "unresolved_item_count": len(unresolved_rows),
    "unresolved_rules_resolved": False,
    "human_approval_required": True,
    "implementation_authorized": False,
    "product_code_changes": 0,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "validation": "PASS",
    "status": "CANONICAL_DIRECTION_ENGINE_DECISION_PACKAGE_READY",
}

(OUT / "PR064A_SUMMARY.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

adr = f"""# ADR-064 — Canonical Direction Engine

## Status

**Proposed for human approval**

## Context

PR-062 identified {len(impact)} direction/time-related impact records,
including {risk_counts['HIGH']} high-risk records. PR-063 froze versioned
direction, timing, CORE, and EXPANDED contracts but explicitly retained human
approval before implementation.

The path `{canonical_path}` is not currently present in the repository.
Therefore this ADR proposes the path but does not create runtime code there.

## Decision

1. The proposed canonical owner is `decision_governance_core`.
2. The proposed canonical path is `{canonical_path}`.
3. The raw COT gateway remains raw-data-only.
4. CORE is the sole public official result.
5. EXPANDED remains internal and shadow-only.
6. Investment Day Control, TDL-M&L, and TDL-S are disabled.
7. Speculation TDL and Day Control remain disabled until separate semantics
   approval.
8. PR-064A changes governance artifacts only.
9. PR-064 implementation is prohibited until human approval and physical
   result-store decisions are recorded.

## Consequences

- No product or runtime change occurs in this PR.
- Existing high-risk integration points require WRAP or REPLACE review.
- Physical Official and Experimental Result Stores remain pending.
- No TDL semantics are invented.
- The decision package may be merged as evidence, but it does not authorize
  implementation.

## Approval gate

Implementation may begin only after a separately recorded approval confirms:

- canonical engine path;
- logic owner;
- physical result stores;
- public and internal API writers;
- TDL and Day Control policy;
- rollback and shadow deployment plan.
"""

(OUT / "ADR-064-CANONICAL-DIRECTION-ENGINE.md").write_text(
    adr,
    encoding="utf-8",
)

(OUT / "README.md").write_text(
    """# PR-064A Canonical Direction Engine Resolution

Architecture and governance decision package only.

This package proposes the canonical direction engine target, maps ownership,
integration points, logical result stores, TDL decisions, and file actions.
It does not authorize or implement runtime changes.
""",
    encoding="utf-8",
)

for key in (
    "canonical_engine_path",
    "canonical_engine_path_status",
    "direction_logic_owner",
    "direction_logic_owner_status",
    "official_result_store_status",
    "experimental_result_store_status",
    "investment_day_control",
    "investment_tdl",
    "speculation_tdl",
    "core_expanded_isolation",
    "high_risk_record_count",
    "critical_risk_record_count",
    "logic_ownership_record_count",
    "integration_point_count",
    "file_action_record_count",
    "unresolved_rules_resolved",
    "human_approval_required",
    "implementation_authorized",
    "product_code_changes",
    "production_services_restarted",
    "mutating_requests_executed",
    "runtime_changes",
    "validation",
    "status",
):
    value = summary[key]
    if isinstance(value, bool):
        value = str(value).lower()
    print(f"{key}={value}")

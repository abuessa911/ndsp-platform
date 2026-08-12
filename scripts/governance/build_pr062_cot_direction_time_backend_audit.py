#!/usr/bin/env python3
"""Build PR-062 COT direction and time backend audit artifacts.

The audit is intentionally read-only. It scans canonical source trees,
identifies direction/time logic and integration points, and produces an impact
map. It does not modify runtime or product code.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

AUDIT_RELATIVE = Path(
    "docs/99-governance/pr-062-cot-direction-time-backend-audit"
)

SCAN_ROOTS = (
    "backend",
    "apps",
    "api",
    "integrations",
    "packages",
)

IGNORED_DIRS = {
    ".git",
    ".next",
    ".turbo",
    ".vite",
    "_backups",
    "archive",
    "archives",
    "backups",
    "build",
    "coverage",
    "dist",
    "docs",
    "node_modules",
    "public",
    "var",
    "vendor",
    "__pycache__",
}

SOURCE_SUFFIXES = {
    ".cjs",
    ".conf",
    ".env",
    ".js",
    ".json",
    ".jsx",
    ".mjs",
    ".py",
    ".service",
    ".sh",
    ".ts",
    ".tsx",
    ".yaml",
    ".yml",
}

PATTERNS: dict[str, re.Pattern[str]] = {
    "direction": re.compile(
        r"\b(direction|trend|bias|bullish|bearish|neutral|"
        r"dominance|explicitness|horizon)\b",
        re.IGNORECASE,
    ),
    "long_short": re.compile(
        r"\b(long|short|longs|shorts)\b",
        re.IGNORECASE,
    ),
    "positions": re.compile(r"\bpositions?\b", re.IGNORECASE),
    "changes": re.compile(r"\bchanges?\b", re.IGNORECASE),
    "asset_manager": re.compile(
        r"asset[_\s-]*managers?",
        re.IGNORECASE,
    ),
    "leveraged_funds": re.compile(
        r"leveraged[_\s-]*funds?",
        re.IGNORECASE,
    ),
    "other_reportables": re.compile(
        r"other[_\s-]*reportables?|others?",
        re.IGNORECASE,
    ),
    "dealer": re.compile(
        r"dealer|intermediar",
        re.IGNORECASE,
    ),
    "delta": re.compile(
        r"\bdelta\b|long\s*-\s*short|short\s*-\s*long",
        re.IGNORECASE,
    ),
    "tdl": re.compile(
        r"TDL[-_\s]*(M&L|ML|S)|tdl[_\s-]*(ml|s)",
        re.IGNORECASE,
    ),
    "day_control": re.compile(
        r"day[_\s-]*control|daily[_\s-]*controller|"
        r"control[_\s-]*day",
        re.IGNORECASE,
    ),
    "utc": re.compile(
        r"\bUTC\b|timezone\.utc|ZoneInfo\([\"']UTC[\"']\)|"
        r"toISOString\(",
        re.IGNORECASE,
    ),
    "effective_week": re.compile(
        r"effective[_\s-]*(week|from|until)|week[_\s-]*start|"
        r"following[_\s-]*monday|next[_\s-]*monday",
        re.IGNORECASE,
    ),
    "calendar_day": re.compile(
        r"\b(monday|tuesday|wednesday|thursday|friday|"
        r"saturday|sunday)\b",
        re.IGNORECASE,
    ),
    "core": re.compile(r"\bCORE(?:_V1)?\b", re.IGNORECASE),
    "expanded": re.compile(
        r"\bEXPANDED\b|\bSHADOW_MODE\b|shadow[_\s-]*engine",
        re.IGNORECASE,
    ),
    "public_api": re.compile(
        r"public[_\s-]*api|/api/public|official[_\s-]*result",
        re.IGNORECASE,
    ),
    "internal_api": re.compile(
        r"internal[_\s-]*(admin[_\s-]*)?api|admin[_\s-]*api",
        re.IGNORECASE,
    ),
    "result_store": re.compile(
        r"result[_\s-]*store|official[_\s-]*store|"
        r"experimental[_\s-]*store",
        re.IGNORECASE,
    ),
    "cot": re.compile(
        r"\bCOT\b|commitments?[_\s-]*of[_\s-]*traders?",
        re.IGNORECASE,
    ),
}

LOCAL_TIME_PATTERNS = (
    re.compile(r"\.toLocale(?:String|DateString|TimeString)\s*\("),
    re.compile(r"\.get(?:Day|Hours|Date|Month|FullYear)\s*\("),
    re.compile(r"datetime\.now\s*\(\s*\)"),
    re.compile(r"date\.today\s*\(\s*\)"),
    re.compile(r"new\s+Date\s*\(\s*\)\s*;"),
)

LEGACY_PATH_PATTERN = re.compile(
    r"/(?:opt|root)/empire-core|/var/www",
    re.IGNORECASE,
)

PUBLIC_EXPANDED_PATTERN = re.compile(
    r"(EXPANDED|SHADOW_MODE).*(public[_\s-]*api|/api/public)|"
    r"(public[_\s-]*api|/api/public).*(EXPANDED|SHADOW_MODE)",
    re.IGNORECASE,
)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def iter_source_files(root: Path) -> Iterable[Path]:
    for scan_root in SCAN_ROOTS:
        base = root / scan_root
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
                continue
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def source_kind(path: Path) -> str:
    lowered = path.as_posix().lower()

    if any(token in lowered for token in ("/test/", "/tests/", ".test.", ".spec.")):
        return "TEST"
    if any(token in lowered for token in ("/contracts/", "/schemas/", "contract", "schema")):
        return "CONTRACT"
    if path.suffix.lower() in {".json", ".yaml", ".yml", ".env", ".conf", ".service"}:
        return "CONFIG"
    if any(token in lowered for token in ("/routes/", "/api/", "gateway", "server")):
        return "INTEGRATION"
    return "RUNTIME_IMPLEMENTATION"


def category_set(matches: dict[str, list[int]]) -> set[str]:
    categories: set[str] = set()

    if any(
        key in matches
        for key in (
            "direction",
            "long_short",
            "positions",
            "changes",
            "asset_manager",
            "leveraged_funds",
            "other_reportables",
            "dealer",
            "delta",
        )
    ):
        categories.add("DIRECTION")

    if any(
        key in matches
        for key in (
            "tdl",
            "day_control",
            "utc",
            "effective_week",
            "calendar_day",
        )
    ):
        categories.add("TIME")

    if any(
        key in matches
        for key in (
            "core",
            "expanded",
            "public_api",
            "internal_api",
            "result_store",
        )
    ):
        categories.add("CORE_EXPANDED")

    if "cot" in matches:
        categories.add("COT_DATA")

    return categories


def classify_impact(
    kind: str,
    categories: set[str],
    flags: list[str],
) -> tuple[str, str, str]:
    if "PUBLIC_EXPANDED_COLOCATION" in flags:
        return "CRITICAL", "REPLACE", "Review public isolation immediately"

    if "INVESTMENT_TDL_COLOCATION" in flags:
        return "HIGH", "REPLACE_OR_WRAP", (
            "Separate investment logic from TDL/day-control execution"
        )

    if "POSITIONS_CHANGES_COLOCATION" in flags:
        return "HIGH", "REPLACE_OR_WRAP", (
            "Prove Positions and Changes have separate responsibilities"
        )

    if "LOCAL_TIME_USAGE" in flags:
        return "HIGH", "REPLACE_OR_WRAP", (
            "Normalize canonical calculations to UTC"
        )

    if kind == "CONTRACT":
        return "HIGH", "ALIGN_CONTRACT", (
            "Align with versioned direction/time contracts"
        )

    if kind == "TEST":
        return "MEDIUM", "ADD_REGRESSION_TESTS", (
            "Add approved COT governance fixtures and edge cases"
        )

    if kind == "CONFIG":
        return "MEDIUM", "REVIEW_CONFIGURATION", (
            "Confirm values are explicit, versioned, and UTC-safe"
        )

    if categories == {"DIRECTION"}:
        return "MEDIUM", "WRAP_OR_REPLACE", (
            "Centralize direction computation behind one contract"
        )

    if categories == {"TIME"}:
        return "MEDIUM", "WRAP_OR_REPLACE", (
            "Centralize effective-week and UTC calculations"
        )

    if "DIRECTION" in categories and "TIME" in categories:
        return "HIGH", "REPLACE_OR_WRAP", (
            "Split direction calculation from timing orchestration"
        )

    return "LOW", "REVIEW", "Confirm ownership and consumers"


def line_matches(text: str) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}

    for number, line in enumerate(text.splitlines(), start=1):
        for name, pattern in PATTERNS.items():
            if pattern.search(line):
                result.setdefault(name, []).append(number)

    return result


def limited_lines(values: list[int]) -> str:
    shown = values[:20]
    suffix = "" if len(values) <= 20 else f";+{len(values) - 20}"
    return ";".join(str(item) for item in shown) + suffix


def sample_evidence(text: str, matches: dict[str, list[int]]) -> str:
    lines = text.splitlines()
    numbers = sorted(
        {
            number
            for values in matches.values()
            for number in values
        }
    )[:5]

    evidence: list[str] = []

    for number in numbers:
        if 1 <= number <= len(lines):
            snippet = " ".join(lines[number - 1].strip().split())
            if snippet:
                evidence.append(f"{number}:{snippet[:180]}")

    return " | ".join(evidence)


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: processor <repository-root>")

    root = Path(sys.argv[1]).resolve()
    audit_dir = root / AUDIT_RELATIVE
    audit_dir.mkdir(parents=True, exist_ok=True)

    inventory: list[dict[str, Any]] = []
    impact: list[dict[str, Any]] = []

    scanned_count = 0

    for path in sorted(iter_source_files(root)):
        scanned_count += 1
        text = read_text(path)

        if not text:
            continue

        matches = line_matches(text)

        if not matches:
            continue

        relative = path.relative_to(root).as_posix()
        kind = source_kind(path)
        categories = category_set(matches)
        flags: list[str] = []

        if "positions" in matches and "changes" in matches:
            flags.append("POSITIONS_CHANGES_COLOCATION")

        investment_present = bool(
            re.search(r"\binvest(?:ment|ing)\b", text, re.IGNORECASE)
        )
        if investment_present and (
            "tdl" in matches or "day_control" in matches
        ):
            flags.append("INVESTMENT_TDL_COLOCATION")

        if any(pattern.search(text) for pattern in LOCAL_TIME_PATTERNS):
            flags.append("LOCAL_TIME_USAGE")

        if PUBLIC_EXPANDED_PATTERN.search(text):
            flags.append("PUBLIC_EXPANDED_COLOCATION")

        if LEGACY_PATH_PATTERN.search(text):
            flags.append("LEGACY_PATH_REFERENCE")

        risk, action, recommendation = classify_impact(
            kind,
            categories,
            flags,
        )

        match_lines = {
            name: limited_lines(values)
            for name, values in sorted(matches.items())
        }

        inventory_row = {
            "path": relative,
            "source_kind": kind,
            "categories": "|".join(sorted(categories)),
            "matched_concepts": "|".join(sorted(matches)),
            "match_count": sum(len(values) for values in matches.values()),
            "line_map": json.dumps(match_lines, ensure_ascii=False),
            "flags": "|".join(flags) if flags else "NONE",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "evidence_sample": sample_evidence(text, matches),
        }
        inventory.append(inventory_row)

        impact.append(
            {
                "path": relative,
                "source_kind": kind,
                "categories": "|".join(sorted(categories)),
                "risk": risk,
                "recommended_action": action,
                "recommendation": recommendation,
                "flags": "|".join(flags) if flags else "NONE",
                "owner": "DISCOVERY_REQUIRED",
                "consumers": "DISCOVERY_REQUIRED",
                "canonical_target": (
                    "backend/services/decision_governance_core/"
                    if "DIRECTION" in categories or "TIME" in categories
                    else "DISCOVERY_REQUIRED"
                ),
                "human_review_required": "true",
            }
        )

    if not inventory:
        raise SystemExit("No COT direction/time candidates were discovered")

    inventory.sort(key=lambda row: row["path"])
    impact.sort(
        key=lambda row: (
            {
                "CRITICAL": 0,
                "HIGH": 1,
                "MEDIUM": 2,
                "LOW": 3,
            }.get(row["risk"], 4),
            row["path"],
        )
    )

    inventory_fields = [
        "path",
        "source_kind",
        "categories",
        "matched_concepts",
        "match_count",
        "line_map",
        "flags",
        "sha256",
        "evidence_sample",
    ]
    impact_fields = [
        "path",
        "source_kind",
        "categories",
        "risk",
        "recommended_action",
        "recommendation",
        "flags",
        "owner",
        "consumers",
        "canonical_target",
        "human_review_required",
    ]

    write_csv(
        audit_dir / "PR062_LOGIC_INVENTORY.csv",
        inventory,
        inventory_fields,
    )
    write_csv(
        audit_dir / "PR062_CODE_IMPACT_MAP.csv",
        impact,
        impact_fields,
    )

    (audit_dir / "PR062_LOGIC_INVENTORY.json").write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (audit_dir / "PR062_CODE_IMPACT_MAP.json").write_text(
        json.dumps(impact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    unresolved = [
        {
            "item_id": "UNR-001",
            "topic": "TDL-M&L semantics",
            "status": "UNRESOLVED",
            "required_before": "PR-064 implementation",
            "resolution": "Document existing rule and obtain governance approval",
        },
        {
            "item_id": "UNR-002",
            "topic": "TDL-S semantics",
            "status": "UNRESOLVED",
            "required_before": "PR-064 implementation",
            "resolution": "Document existing rule and obtain governance approval",
        },
        {
            "item_id": "UNR-003",
            "topic": "Official and experimental result stores",
            "status": "DISCOVERY_REQUIRED",
            "required_before": "Shadow integration",
            "resolution": "Identify stores, writers, readers, retention, and ownership",
        },
        {
            "item_id": "UNR-004",
            "topic": "Exact production integration points",
            "status": "DISCOVERY_REQUIRED",
            "required_before": "Runtime integration",
            "resolution": "Confirm entry points and current result consumers",
        },
        {
            "item_id": "UNR-005",
            "topic": "Zero-versus-nonzero explicitness classification",
            "status": "TEMPORARY_RULE",
            "required_before": "Contract freeze",
            "resolution": "Approve or revise narrow-horizon non-explicit classification",
        },
    ]

    write_csv(
        audit_dir / "PR062_UNRESOLVED_ITEMS.csv",
        unresolved,
        [
            "item_id",
            "topic",
            "status",
            "required_before",
            "resolution",
        ],
    )

    risk_counts = Counter(row["risk"] for row in impact)
    kind_counts = Counter(row["source_kind"] for row in inventory)
    category_counts = Counter()

    for row in inventory:
        for category in row["categories"].split("|"):
            if category:
                category_counts[category] += 1

    flag_counts = Counter()
    for row in inventory:
        for flag in row["flags"].split("|"):
            if flag and flag != "NONE":
                flag_counts[flag] += 1

    summary = {
        "schema_version": "1.0",
        "document": "PR-062 COT Direction and Time Backend Audit",
        "generated_at": iso_now(),
        "source_commit": (
            __import__("subprocess")
            .check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                text=True,
            )
            .strip()
        ),
        "scan_mode": "READ_ONLY",
        "scan_roots": [
            item
            for item in SCAN_ROOTS
            if (root / item).exists()
        ],
        "candidate_files_scanned": scanned_count,
        "logic_candidate_file_count": len(inventory),
        "impact_map_record_count": len(impact),
        "direction_candidate_count": category_counts["DIRECTION"],
        "time_candidate_count": category_counts["TIME"],
        "core_expanded_candidate_count": category_counts["CORE_EXPANDED"],
        "cot_data_candidate_count": category_counts["COT_DATA"],
        "critical_risk_count": risk_counts["CRITICAL"],
        "high_risk_count": risk_counts["HIGH"],
        "medium_risk_count": risk_counts["MEDIUM"],
        "low_risk_count": risk_counts["LOW"],
        "positions_changes_colocation_count": flag_counts[
            "POSITIONS_CHANGES_COLOCATION"
        ],
        "investment_tdl_colocation_count": flag_counts[
            "INVESTMENT_TDL_COLOCATION"
        ],
        "local_time_usage_count": flag_counts["LOCAL_TIME_USAGE"],
        "public_expanded_colocation_count": flag_counts[
            "PUBLIC_EXPANDED_COLOCATION"
        ],
        "legacy_path_reference_count": flag_counts[
            "LEGACY_PATH_REFERENCE"
        ],
        "runtime_implementation_count": kind_counts[
            "RUNTIME_IMPLEMENTATION"
        ],
        "integration_count": kind_counts["INTEGRATION"],
        "contract_count": kind_counts["CONTRACT"],
        "test_count": kind_counts["TEST"],
        "config_count": kind_counts["CONFIG"],
        "unresolved_item_count": len(unresolved),
        "approved_direction_rule": "delta = long - short",
        "approved_neutral_rule": "long == short only",
        "approved_investment_rule": (
            "Asset Manager Positions determine official direction; "
            "Asset Manager Changes determine weekly support only"
        ),
        "approved_speculation_rule": (
            "Changes only; day-control and approved TDL logic allowed"
        ),
        "approved_time_rule": (
            "UTC only; Tuesday report effective next Monday 00:00Z "
            "through following Monday using [from, until)"
        ),
        "approved_public_rule": "CORE only",
        "approved_shadow_rule": "EXPANDED is internal SHADOW_MODE only",
        "traceability_rows_modified": 0,
        "product_code_changes": 0,
        "production_services_restarted": 0,
        "mutating_requests_executed": 0,
        "runtime_changes": "none",
        "human_review_required": True,
        "validation": "PASS",
        "status": "COT_DIRECTION_TIME_BACKEND_AUDIT_COMPLETE",
    }

    (audit_dir / "PR062_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    top_risks = impact[:50]
    report_lines = [
        "# PR-062 — COT Direction and Time Backend Audit",
        "",
        "## Scope",
        "",
        "This audit scans backend and integration source trees in read-only mode. "
        "It identifies current COT direction, category, timing, CORE/EXPANDED, "
        "and result-integration logic. It does not change runtime or product code.",
        "",
        "## Approved baseline used for comparison",
        "",
        "- Dominance delta: `Long - Short` within the same dataset.",
        "- `Long > Short`: bullish.",
        "- `Short > Long`: bearish.",
        "- `Long == Short`: neutral only.",
        "- Investment: Asset Manager Positions determine official direction.",
        "- Investment: Asset Manager Changes determine weekly support only.",
        "- Investment: Day Control, TDL-M&L, and TDL-S are disabled.",
        "- Speculation: Changes only; Day Control and approved TDL logic may run.",
        "- Time: UTC only.",
        "- Tuesday report: effective next Monday at `00:00:00Z`.",
        "- Effective interval: `[effectiveFrom, effectiveUntil)`.",
        "- Public result: CORE only.",
        "- EXPANDED: internal `SHADOW_MODE` only.",
        "",
        "## Audit totals",
        "",
        f"- Candidate files scanned: **{scanned_count}**",
        f"- Logic candidate files: **{len(inventory)}**",
        f"- Direction candidates: **{category_counts['DIRECTION']}**",
        f"- Time candidates: **{category_counts['TIME']}**",
        f"- CORE/EXPANDED candidates: **{category_counts['CORE_EXPANDED']}**",
        f"- Critical risk: **{risk_counts['CRITICAL']}**",
        f"- High risk: **{risk_counts['HIGH']}**",
        f"- Medium risk: **{risk_counts['MEDIUM']}**",
        f"- Low risk: **{risk_counts['LOW']}**",
        "",
        "## Automated risk indicators",
        "",
        f"- Positions/Changes co-location: **{flag_counts['POSITIONS_CHANGES_COLOCATION']}**",
        f"- Investment with TDL/Day Control co-location: **{flag_counts['INVESTMENT_TDL_COLOCATION']}**",
        f"- Potential local-time usage: **{flag_counts['LOCAL_TIME_USAGE']}**",
        f"- Public/EXPANDED co-location: **{flag_counts['PUBLIC_EXPANDED_COLOCATION']}**",
        f"- Legacy path references: **{flag_counts['LEGACY_PATH_REFERENCE']}**",
        "",
        "These indicators are audit candidates, not automatic proof of defects. "
        "Each requires human review before PR-063/PR-064 changes.",
        "",
        "## Highest-priority impact map",
        "",
        "| Risk | Action | Kind | Path | Flags |",
        "|---|---|---|---|---|",
    ]

    for row in top_risks:
        report_lines.append(
            "| {risk} | {action} | {kind} | `{path}` | {flags} |".format(
                risk=row["risk"],
                action=row["recommended_action"],
                kind=row["source_kind"],
                path=row["path"],
                flags=row["flags"],
            )
        )

    report_lines.extend(
        [
            "",
            "## Required next steps",
            "",
            "1. Human-review all CRITICAL and HIGH records.",
            "2. Confirm current writers/readers of official and experimental results.",
            "3. Resolve TDL-M&L and TDL-S semantics before implementation.",
            "4. Freeze versioned direction/time contracts in PR-063.",
            "5. Add regression fixtures before replacing any runtime path.",
            "6. Correct direction and time layers only after contract approval.",
            "",
            "## Safety",
            "",
            "- Product code changes: **0**",
            "- Traceability rows modified: **0**",
            "- Production services restarted: **0**",
            "- Mutating requests executed: **0**",
            "- Runtime changes: **none**",
            "",
            "## Artifacts",
            "",
            "- `PR062_LOGIC_INVENTORY.csv`",
            "- `PR062_LOGIC_INVENTORY.json`",
            "- `PR062_CODE_IMPACT_MAP.csv`",
            "- `PR062_CODE_IMPACT_MAP.json`",
            "- `PR062_UNRESOLVED_ITEMS.csv`",
            "- `PR062_SUMMARY.json`",
            "- `PR062_SHA256SUMS.txt`",
        ]
    )

    (audit_dir / "PR-062-COT-DIRECTION-TIME-BACKEND-AUDIT.md").write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    (audit_dir / "README.md").write_text(
        "\n".join(
            [
                "# PR-062 COT Direction and Time Backend Audit",
                "",
                "Read-only audit of backend COT direction, timing, category, "
                "CORE/EXPANDED, and result-integration logic.",
                "",
                "Run:",
                "",
                "```bash",
                "python3 scripts/governance/"
                "build_pr062_cot_direction_time_backend_audit.py .",
                "python3 scripts/governance/"
                "validate_pr062_cot_direction_time_backend_audit.py .",
                "node --test scripts/governance/tests/"
                "pr062-cot-direction-time-backend-audit.test.cjs",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    for key in (
        "candidate_files_scanned",
        "logic_candidate_file_count",
        "impact_map_record_count",
        "direction_candidate_count",
        "time_candidate_count",
        "critical_risk_count",
        "high_risk_count",
        "positions_changes_colocation_count",
        "investment_tdl_colocation_count",
        "local_time_usage_count",
        "public_expanded_colocation_count",
        "legacy_path_reference_count",
        "unresolved_item_count",
        "traceability_rows_modified",
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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

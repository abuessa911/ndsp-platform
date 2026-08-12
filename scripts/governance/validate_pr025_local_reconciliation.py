#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR025 = ROOT / "docs/99-governance/pr-025-local-state-reconciliation"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR025_VALIDATION_FAILED", file=sys.stderr)
    return 1


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    summary = json.loads(
        (PR025 / "PR025_SUMMARY.json").read_text(encoding="utf-8")
    )
    recovery = rows(PR025 / "PR025_CAPABILITY_SOURCE_RECOVERY.csv")
    blocked = rows(PR025 / "PR025_BLOCKED_OR_SENSITIVE_PATHS.csv")

    if summary["primary_worktree_modified"] is not False:
        return fail("Primary worktree must remain read-only")

    if summary["local_changes_deleted"] is not False:
        return fail("Local changes must not be deleted")

    if summary["secrets_copied"] is not False:
        return fail("Secrets must not be copied")

    for row in recovery:
        path = row["path"].lower()
        if any(
            token in path
            for token in (
                ".env",
                "node_modules/",
                "backups/",
                "private_key",
                "credentials",
            )
        ):
            return fail(f"Unsafe recovered path: {row['path']}")

    for row in blocked:
        if not row["reason"]:
            return fail("Blocked path lacks reason")

    print(
        f"observed_local_change_count="
        f"{summary['observed_local_change_count']}"
    )
    print(
        f"recovered_from_local_count="
        f"{summary['recovered_from_local_count']}"
    )
    print(
        f"still_missing_source_count="
        f"{summary['still_missing_source_count']}"
    )
    print("primary_worktree_modified=false")
    print("local_changes_deleted=false")
    print("secrets_copied=false")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR025_LOCAL_RECONCILIATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

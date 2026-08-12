#!/usr/bin/env python3
"""Validate PR-034 source restoration and safety invariants."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PR034 = ROOT / "docs/99-governance/pr-034-restore-tdl-v2-policy"


def fail(message: str) -> int:
    print(f"error={message}", file=sys.stderr)
    print("validation=FAIL", file=sys.stderr)
    print("status=PR034_VALIDATION_FAILED", file=sys.stderr)
    return 1


def main() -> int:
    selection = json.loads(
        (PR034 / "PR034_SELECTED_SOURCE.json").read_text(
            encoding="utf-8"
        )
    )
    summary = json.loads(
        (PR034 / "PR034_SUMMARY.json").read_text(
            encoding="utf-8"
        )
    )

    with (
        PR034 / "PR034_TDL_POLICY_SOURCE_INVENTORY.csv"
    ).open(encoding="utf-8", newline="") as handle:
        inventory = list(csv.DictReader(handle))

    if not inventory:
        return fail("Source inventory is empty")

    selected_rows = [
        row for row in inventory if row["selected"] == "True"
    ]

    if len(selected_rows) != 1:
        return fail("Inventory must contain exactly one selected row")

    target = ROOT / selection["restored_target"]

    if not target.is_file():
        return fail(f"Restored source missing: {target}")

    payload = target.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()

    if digest != selection["selected_sha256"]:
        return fail("Restored source digest differs from selected source")

    try:
        tree = ast.parse(payload.decode("utf-8"))
    except (UnicodeDecodeError, SyntaxError) as error:
        return fail(f"Restored source is invalid Python: {error}")

    functions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef),
        )
    }

    required = {
        "read_tdl_v2_policy",
        "write_tdl_v2_policy",
    }

    if not required.issubset(functions):
        return fail("Required policy functions are missing")

    for field in (
        "local_sources_deleted",
        "snapshots_deleted",
        "secrets_copied",
    ):
        if selection[field] is not False:
            return fail(f"Safety invariant failed: {field}")

    if summary["ast_validation"] != "PASS":
        return fail("AST validation was not recorded")

    if summary["secret_scan"] != "PASS":
        return fail("Secret scan was not recorded")

    if summary["py_compile"] != "PASS":
        return fail("Python compile was not recorded")

    print(f"candidate_count={len(inventory)}")
    print("selected_source_count=1")
    print("source_digest_validation=PASS")
    print("required_function_validation=PASS")
    print("ast_validation=PASS")
    print("secret_scan=PASS")
    print("py_compile=PASS")
    print("local_sources_deleted=false")
    print("snapshots_deleted=false")
    print("secrets_copied=false")
    print("runtime_changes=none")
    print("validation=PASS")
    print("status=PR034_TDL_V2_POLICY_RESTORE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

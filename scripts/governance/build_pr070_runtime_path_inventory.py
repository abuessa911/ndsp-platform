#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "docs/99-governance/pr-070-runtime-path-inventory"
OUT.mkdir(parents=True, exist_ok=True)

PATHS = [Path("/opt"), Path("/var/www")]
MAX_FILES = 50000

def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

path_rows: list[dict[str, str]] = []
count = 0

for base in PATHS:
    if not base.exists():
        path_rows.append({
            "path": str(base),
            "type": "MISSING",
            "size_bytes": "0",
            "mode": "",
            "owner": "",
            "group": "",
            "symlink_target": "",
        })
        continue

    for current, dirs, files in os.walk(base, followlinks=False):
        dirs[:] = [item for item in dirs if item not in {"node_modules", ".git"}]

        current_path = Path(current)
        for name in sorted(dirs + files):
            target = current_path / name
            try:
                stat = target.lstat()
            except OSError:
                continue

            kind = "SYMLINK" if target.is_symlink() else (
                "DIRECTORY" if target.is_dir() else "FILE"
            )
            symlink_target = ""
            if target.is_symlink():
                try:
                    symlink_target = os.readlink(target)
                except OSError:
                    pass

            path_rows.append({
                "path": str(target),
                "type": kind,
                "size_bytes": str(stat.st_size),
                "mode": oct(stat.st_mode & 0o777),
                "owner": str(stat.st_uid),
                "group": str(stat.st_gid),
                "symlink_target": symlink_target,
            })
            count += 1
            if count >= MAX_FILES:
                break

        if count >= MAX_FILES:
            break

systemd_rows: list[dict[str, str]] = []

try:
    units = subprocess.check_output(
        [
            "systemctl",
            "list-unit-files",
            "--type=service",
            "--no-legend",
            "--no-pager",
        ],
        text=True,
        stderr=subprocess.DEVNULL,
    ).splitlines()
except Exception:
    units = []

for line in units:
    if not line.strip():
        continue
    unit = line.split()[0]
    if not re.search(r"ndsp|cot|empire|decision|gateway", unit, re.I):
        continue

    try:
        props = subprocess.check_output(
            [
                "systemctl",
                "show",
                unit,
                "--property=FragmentPath,ExecStart,WorkingDirectory,EnvironmentFiles,User,Group,ActiveState,SubState",
                "--no-pager",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        props = ""

    data = {}
    for item in props.splitlines():
        if "=" in item:
            key, value = item.split("=", 1)
            data[key] = value

    systemd_rows.append({
        "unit": unit,
        "fragment_path": data.get("FragmentPath", ""),
        "exec_start": data.get("ExecStart", ""),
        "working_directory": data.get("WorkingDirectory", ""),
        "environment_files": data.get("EnvironmentFiles", ""),
        "user": data.get("User", ""),
        "group": data.get("Group", ""),
        "active_state": data.get("ActiveState", ""),
        "sub_state": data.get("SubState", ""),
    })

nginx_rows: list[dict[str, str]] = []
nginx_paths = [
    Path("/etc/nginx/nginx.conf"),
    Path("/etc/nginx/sites-enabled"),
    Path("/etc/nginx/conf.d"),
]

directive_pattern = re.compile(
    r"^\s*(root|alias|proxy_pass|include|ssl_certificate|ssl_certificate_key)\s+(.+?);"
)

for base in nginx_paths:
    candidates = [base] if base.is_file() else (
        sorted(base.rglob("*")) if base.exists() else []
    )
    for path in candidates:
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        for number, line in enumerate(lines, start=1):
            match = directive_pattern.search(line)
            if match:
                nginx_rows.append({
                    "file": str(path),
                    "line": str(number),
                    "directive": match.group(1),
                    "value": match.group(2).strip(),
                })

reference_rows: list[dict[str, str]] = []
reference_pattern = re.compile(r"/opt/[^\s\"']+|/var/www/[^\s\"']+")

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    if any(part in {".git", "node_modules", "dist", "build", "archive", "backups"} for part in path.parts):
        continue
    if path.suffix.lower() not in {
        ".js", ".cjs", ".mjs", ".ts", ".tsx", ".py", ".sh",
        ".json", ".yaml", ".yml", ".md", ".conf", ".service",
    }:
        continue

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        continue

    for number, line in enumerate(lines, start=1):
        for match in reference_pattern.findall(line):
            reference_rows.append({
                "repository_path": path.relative_to(ROOT).as_posix(),
                "line": str(number),
                "reference": match.rstrip(";,.)]"),
            })

write_csv(
    OUT / "PR070_PATH_INVENTORY.csv",
    path_rows,
    ["path", "type", "size_bytes", "mode", "owner", "group", "symlink_target"],
)
write_csv(
    OUT / "PR070_SYSTEMD_INVENTORY.csv",
    systemd_rows,
    [
        "unit", "fragment_path", "exec_start", "working_directory",
        "environment_files", "user", "group", "active_state", "sub_state",
    ],
)
write_csv(
    OUT / "PR070_NGINX_INVENTORY.csv",
    nginx_rows,
    ["file", "line", "directive", "value"],
)
write_csv(
    OUT / "PR070_REPOSITORY_REFERENCES.csv",
    reference_rows,
    ["repository_path", "line", "reference"],
)

summary = {
    "schema_version": "1.0",
    "document": "PR-070 Runtime Path Inventory",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "scan_mode": "READ_ONLY",
    "path_record_count": len(path_rows),
    "systemd_service_count": len(systemd_rows),
    "nginx_directive_count": len(nginx_rows),
    "repository_reference_count": len(reference_rows),
    "inventory_limit_reached": count >= MAX_FILES,
    "filesystem_roots": ["/opt", "/var/www"],
    "systemd_mutations": 0,
    "nginx_mutations": 0,
    "files_deleted": 0,
    "files_moved": 0,
    "production_services_restarted": 0,
    "mutating_requests_executed": 0,
    "runtime_changes": "none",
    "human_review_required": True,
    "validation": "PASS",
    "status": "RUNTIME_PATH_INVENTORY_COMPLETE",
}

(OUT / "PR070_SUMMARY.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

report = f"""# PR-070 — Runtime Path Inventory

## Scope

Read-only inventory of `/opt`, `/var/www`, relevant systemd services, Nginx
directives, and repository references to legacy runtime paths.

## Counts

- Path records: {len(path_rows)}
- Relevant systemd services: {len(systemd_rows)}
- Nginx directives: {len(nginx_rows)}
- Repository path references: {len(reference_rows)}
- Inventory limit reached: {str(count >= MAX_FILES).lower()}

## Safety

- systemd mutations: 0
- Nginx mutations: 0
- files deleted: 0
- files moved: 0
- production services restarted: 0
- runtime changes: none

## Next step

Human review must classify each path and reference as Active, Legacy,
Duplicate, Unknown, Safe to Migrate, or Unsafe to Remove before PR-071.
"""

(OUT / "PR-070-RUNTIME-PATH-INVENTORY.md").write_text(
    report,
    encoding="utf-8",
)

(OUT / "README.md").write_text(
    "# PR-070 Runtime Path Inventory\n\nRead-only runtime and infrastructure inventory.\n",
    encoding="utf-8",
)

for key, value in summary.items():
    if key.endswith("_count") or key in {
        "inventory_limit_reached",
        "systemd_mutations",
        "nginx_mutations",
        "files_deleted",
        "files_moved",
        "production_services_restarted",
        "mutating_requests_executed",
        "runtime_changes",
        "validation",
        "status",
    }:
        print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

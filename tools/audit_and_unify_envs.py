#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
import re
import stat
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(os.getenv("ENV_AUDIT_ROOT", str(Path.home() / "empire-core-new"))).resolve()
OUT_DIR = Path(os.getenv("ENV_AUDIT_OUTPUT", str(ROOT / "env_audit_output"))).resolve()
GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:9001").rstrip("/")
PROTECTED_PATH = os.getenv("PROTECTED_PATH", "/api/decision/quality-live")

SKIP_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".cache",
    "_backups",
    "backup",
    "backups",
    "docs",
}

TOKEN_KEYS = {
    "ADMIN_KEY",
    "NDSP_ADMIN_KEY",
    "ADMIN_UI_KEY",
    "JWT_SECRET",
    "NDSP_INTERNAL_DEBUG_KEY",
    "NDSP_EXECUTION_WEBHOOK_SECRET",
}

SENSITIVE_HINTS = {
    "KEY",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "PASS",
    "JWT",
    "DATABASE_URL",
    "DB_URL",
}


def is_env_file(path: Path) -> bool:
    name = path.name.lower()
    if "example" in name or "template" in name or ".bak" in name or "backup" in name:
        return False
    return name == ".env" or name.startswith(".env.") or name.endswith(".env")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def clean_value(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def parse_env(path: Path) -> list[tuple[str, str, Path, int]]:
    rows = []

    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return rows

    for line_no, raw in enumerate(lines, 1):
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line.removeprefix("export ").strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()

        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue

        rows.append((key, clean_value(value), path, line_no))

    return rows


def is_sensitive(key: str) -> bool:
    upper = key.upper()
    return any(hint in upper for hint in SENSITIVE_HINTS)


def mask(key: str, value: str) -> str:
    if not value:
        return ""

    if not is_sensitive(key):
        return value

    digest = hashlib.sha256(value.encode()).hexdigest()[:10]
    return f"<secret len={len(value)} sha256={digest}>"


def quote_value(value: str) -> str:
    if not value:
        return ""

    if re.fullmatch(r"[A-Za-z0-9_./:@%+=,-]+", value):
        return value

    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def find_env_files() -> list[Path]:
    files = []

    for path in ROOT.rglob("*"):
        if should_skip(path):
            continue
        if path.is_file() and is_env_file(path):
            files.append(path)

    return sorted(files)


def pick_value(rows: list[tuple[str, str, Path, int]]) -> tuple[str, str, Path, int]:
    def score(row: tuple[str, str, Path, int]) -> tuple[int, str]:
        _, value, path, _ = row
        text = str(path).lower()
        points = 0

        if value:
            points += 100
        if path.name == ".env":
            points += 50
        if "prod" in text or "production" in text:
            points += 30
        if "backup" in text or "old" in text:
            points -= 40
        if "example" in text or "template" in text:
            points -= 90

        return points, str(path)

    return sorted(rows, key=score, reverse=True)[0]


def request_with_headers(headers: dict[str, str]) -> tuple[int | None, str]:
    url = GATEWAY_URL + "/" + PROTECTED_PATH.lstrip("/")
    req = Request(url, headers=headers, method="GET")

    try:
        with urlopen(req, timeout=8) as res:
            return res.status, res.read(800).decode("utf-8", errors="replace")
    except HTTPError as exc:
        return exc.code, exc.read(800).decode("utf-8", errors="replace")
    except URLError as exc:
        return None, str(exc)


def token_headers(value: str) -> list[tuple[str, dict[str, str]]]:
    return [
        ("authorization_bearer", {"Authorization": f"Bearer {value}"}),
        ("authorization_raw", {"Authorization": value}),
        ("x_admin_key_lower", {"x-admin-key": value}),
        ("x_admin_key_mixed", {"x_Admin_Key": value}),
        ("x_ndsp_admin_key", {"x-ndsp-admin-key": value}),
        ("x_internal_debug_key", {"x-internal-debug-key": value}),
        ("x_api_key", {"x-api-key": value}),
    ]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    env_files = find_env_files()
    grouped: dict[str, list[tuple[str, str, Path, int]]] = {}

    for env_file in env_files:
        for row in parse_env(env_file):
            grouped.setdefault(row[0], []).append(row)

    report_lines = [
        "# ENV Audit Report",
        "",
        f"- root: `{ROOT}`",
        f"- files found: `{len(env_files)}`",
        f"- unique keys: `{len(grouped)}`",
        "",
        "## Env Files",
        "",
    ]

    for path in env_files:
        report_lines.append(f"- `{path}`")

    report_lines += ["", "## Duplicate / Conflicting Keys", ""]

    for key in sorted(grouped):
        rows = grouped[key]
        values = {row[1] for row in rows}

        if len(rows) <= 1:
            continue

        label = "CONFLICT" if len(values) > 1 else "DUPLICATE_SAME_VALUE"
        selected = pick_value(rows)

        report_lines.append(f"### `{key}` — {label}")
        for _, value, path, line_no in rows:
            report_lines.append(f"- `{path}:{line_no}` = `{mask(key, value)}`")
        report_lines.append(f"- selected: `{selected[2]}:{selected[3]}`")
        report_lines.append("")

    unified_lines = [
        "# Unified .env generated by tools/audit_and_unify_envs.py",
        "# Review before production use.",
        "",
    ]

    template_lines = [
        "# Safe .env template. No secrets included.",
        "",
    ]

    for key in sorted(grouped):
        selected = pick_value(grouped[key])
        unified_lines.append(f"# source: {selected[2]}:{selected[3]}")
        unified_lines.append(f"{key}={quote_value(selected[1])}")
        unified_lines.append("")

        template_lines.append(f"{key}=" if is_sensitive(key) else f"{key}=CHANGE_ME")

    token_lines = ["", "## Token Matrix", ""]
    pass_lines = []
    fail_lines = []

    for key in sorted(TOKEN_KEYS):
        for _, value, _, _ in grouped.get(key, []):
            if not value:
                continue

            for style, headers in token_headers(value):
                status, body = request_with_headers(headers)
                preview = body.replace("\n", " ")[:180]
                line = f"{key} | {style} | status={status} | body={preview}"

                if status in {200, 201, 202}:
                    pass_lines.append(line)
                else:
                    fail_lines.append(line)

    if pass_lines:
        token_lines.append("### PASS")
        token_lines += [f"- {line}" for line in pass_lines]
    else:
        token_lines.append("### PASS")
        token_lines.append("- No working token found.")

    token_lines += ["", "### FAIL"]
    token_lines += [f"- {line}" for line in fail_lines]

    report_lines += token_lines

    report_path = OUT_DIR / "env_audit_report.md"
    unified_path = OUT_DIR / ".env.unified"
    template_path = OUT_DIR / ".env.template"

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    unified_path.write_text("\n".join(unified_lines) + "\n", encoding="utf-8")
    template_path.write_text("\n".join(template_lines) + "\n", encoding="utf-8")

    unified_path.chmod(stat.S_IRUSR | stat.S_IWUSR)

    print(f"Report: {report_path}")
    print(f"Unified: {unified_path}")
    print(f"Template: {template_path}")
    print("")
    print("PASS tokens:")
    if pass_lines:
        for line in pass_lines:
            print(line)
    else:
        print("No working token found.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOTS = [
    Path("/var/www/ndsp-admin"),
    Path("/var/www/ndsp-my"),
    Path("/var/www/ndsp"),
]

DEAD_HREFS = {"", "#", "null"}

class Parser(HTMLParser):
    def __init__(self, file: Path):
        super().__init__()
        self.file = file
        self.items = []
        self.current = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a", "button"}:
            self.current = {
                "tag": tag,
                "attrs": attrs,
                "text": "",
                "file": str(self.file),
                "line": self.getpos()[0],
            }
            self.items.append(self.current)
        elif tag == "script":
            self.current = {
                "tag": "script",
                "attrs": attrs,
                "text": "",
                "file": str(self.file),
                "line": self.getpos()[0],
            }

    def handle_data(self, data):
        if self.current:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.current and self.current.get("tag") == "script":
            self.scripts.append(self.current.get("text", ""))
            self.current = None
        elif tag in {"a", "button"}:
            self.current = None

def js_binds_id(scripts: str, idv: str) -> bool:
    if not idv:
        return False
    patterns = [
        rf'getElementById\(["\']{re.escape(idv)}["\']\)',
        rf'bindClick\(["\']{re.escape(idv)}["\']',
        rf'bindNav\(["\']{re.escape(idv)}["\']',
        rf'#{re.escape(idv)}',
    ]
    return any(re.search(p, scripts) for p in patterns)

def selector_bound(scripts: str, attrs: dict) -> bool:
    data_keys = [k for k in attrs if k.startswith("data-")]
    for key in data_keys:
        if f"[{key}]" in scripts or key in scripts:
            return True
    return False

def audit_file(path: Path):
    try:
        s = path.read_text(errors="ignore")
    except Exception:
        return []

    parser = Parser(path)
    try:
        parser.feed(s)
    except Exception:
        pass

    scripts = "\n".join(parser.scripts) + "\n" + s
    issues = []

    for item in parser.items:
        tag = item["tag"]
        attrs = item["attrs"]
        text = re.sub(r"\s+", " ", item["text"]).strip()[:150]
        idv = attrs.get("id", "")
        onclick = attrs.get("onclick")
        href = (attrs.get("href") or "").strip()

        if tag == "a":
            if href.lower() in DEAD_HREFS:
                if js_binds_id(scripts, idv) or selector_bound(scripts, attrs):
                    continue
                issues.append({**item, "text": text, "issue": "DEAD_LINK", "href": href})

        if tag == "button":
            typ = (attrs.get("type") or "").lower()
            if onclick or typ == "submit":
                continue
            if js_binds_id(scripts, idv) or selector_bound(scripts, attrs):
                continue
            if attrs.get("data-uf") and "ndsp-user-filter-buttons-binding-js" in s:
                continue
            issues.append({**item, "text": text, "issue": "BUTTON_NO_VISIBLE_BINDING"})

    return issues

def main():
    files = []
    for root in ROOTS:
        if root.exists():
            files.extend(root.rglob("*.html"))
            files.extend(root.rglob("*.htm"))

    files = sorted(set(files))
    issues = []
    for f in files:
        issues.extend(audit_file(f))

    result = {
        "files_scanned": len(files),
        "issues_count": len(issues),
        "dead_links": sum(1 for x in issues if x["issue"] == "DEAD_LINK"),
        "buttons_without_visible_binding": sum(1 for x in issues if x["issue"] == "BUTTON_NO_VISIBLE_BINDING"),
        "issues": issues[:300],
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

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

DEAD_HREFS = {"", "#", "javascript:void(0)", "javascript:;", "null"}

class Parser(HTMLParser):
    def __init__(self, file: Path):
        super().__init__()
        self.file = file
        self.stack = []
        self.items = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.stack.append((tag, a, ""))
        if tag in {"a", "button"}:
            self.items.append({
                "tag": tag,
                "attrs": a,
                "text": "",
                "file": str(self.file),
                "line": self.getpos()[0],
            })

    def handle_data(self, data):
        if self.items and data.strip():
            self.items[-1]["text"] += data.strip() + " "

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

def audit_file(path: Path):
    try:
        s = path.read_text(errors="ignore")
    except Exception:
        return []
    p = Parser(path)
    try:
        p.feed(s)
    except Exception:
        pass
    issues = []
    for item in p.items:
        tag = item["tag"]
        attrs = item["attrs"]
        text = item["text"].strip()
        if tag == "a":
            href = (attrs.get("href") or "").strip()
            if href.lower() in DEAD_HREFS:
                issues.append({**item, "issue": "DEAD_LINK", "href": href})
        if tag == "button":
            onclick = attrs.get("onclick")
            typ = (attrs.get("type") or "").lower()
            data_action = attrs.get("data-action") or attrs.get("data-endpoint") or attrs.get("data-api")
            if not onclick and typ != "submit" and not data_action:
                issues.append({**item, "issue": "BUTTON_NO_VISIBLE_BINDING"})
    return issues

def main():
    all_files = []
    for root in ROOTS:
        if root.exists():
            all_files.extend(root.rglob("*.html"))
            all_files.extend(root.rglob("*.htm"))

    issues = []
    for f in sorted(set(all_files)):
        issues.extend(audit_file(f))

    summary = {
        "files_scanned": len(set(all_files)),
        "issues_count": len(issues),
        "dead_links": sum(1 for x in issues if x["issue"] == "DEAD_LINK"),
        "buttons_without_visible_binding": sum(1 for x in issues if x["issue"] == "BUTTON_NO_VISIBLE_BINDING"),
        "issues": issues[:300],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOTS = [Path("/var/www/ndsp-admin"), Path("/var/www/ndsp-my"), Path("/var/www/ndsp")]
DEAD_HREFS = {"", "#", "null"}

class P(HTMLParser):
    def __init__(self, file: Path):
        super().__init__()
        self.file = file
        self.items = []
        self.current = None
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a","button"}:
            self.current = {"tag":tag, "attrs":attrs, "text":"", "file":str(self.file), "line":self.getpos()[0]}
            self.items.append(self.current)
        elif tag == "script":
            self.current = {"tag":"script", "attrs":attrs, "text":"", "file":str(self.file), "line":self.getpos()[0]}

    def handle_data(self, data):
        if self.current:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "script" and self.current and self.current.get("tag") == "script":
            self.scripts.append(self.current["text"])
            self.current = None
        elif tag in {"a","button"}:
            self.current = None

def js_binds_id(scripts: str, idv: str) -> bool:
    if not idv:
        return False
    pats = [
        rf'getElementById\(["\']{re.escape(idv)}["\']\)',
        rf'\$\(["\']#{re.escape(idv)}["\']\)',
        rf'bindClick\(["\']{re.escape(idv)}["\']',
        rf'bindNav\(["\']{re.escape(idv)}["\']',
        rf'id=["\']{re.escape(idv)}["\']',
    ]
    return any(re.search(p, scripts) for p in pats)

def selector_bound(scripts: str, attrs: dict) -> bool:
    for key in ["data-mkt","data-tf","data-plan","data-cat","data-evt","data-toggle"]:
        if key in attrs:
            if f"[{key}]" in scripts or key in scripts:
                return True
    return False

def audit_file(path: Path):
    try:
        s = path.read_text(errors="ignore")
    except Exception:
        return []
    parser = P(path)
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
        idv = attrs.get("id","")
        onclick = attrs.get("onclick")
        cls = attrs.get("class","")
        href = (attrs.get("href") or "").strip()
        if tag == "a":
            if href.lower() in DEAD_HREFS:
                if js_binds_id(scripts, idv) or "ndsp-user-real-bindings.js" in s:
                    continue
                issues.append({**item, "text":text, "issue":"DEAD_LINK", "href":href})
        if tag == "button":
            typ = (attrs.get("type") or "").lower()
            if onclick or typ == "submit":
                continue
            if js_binds_id(scripts, idv) or selector_bound(scripts, attrs):
                continue
            if "ndsp-user-real-bindings.js" in s and (idv or any(k.startswith("data-") for k in attrs)):
                continue
            issues.append({**item, "text":text, "issue":"BUTTON_NO_VISIBLE_BINDING"})
    return issues

def main():
    files = []
    for root in ROOTS:
        if root.exists():
            files += list(root.rglob("*.html")) + list(root.rglob("*.htm"))
    issues = []
    for f in sorted(set(files)):
        issues += audit_file(f)
    print(json.dumps({
        "files_scanned": len(set(files)),
        "issues_count": len(issues),
        "dead_links": sum(1 for x in issues if x["issue"]=="DEAD_LINK"),
        "buttons_without_visible_binding": sum(1 for x in issues if x["issue"]=="BUTTON_NO_VISIBLE_BINDING"),
        "issues": issues[:200],
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

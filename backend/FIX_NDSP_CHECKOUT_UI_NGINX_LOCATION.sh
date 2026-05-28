#!/usr/bin/env bash
set -Eeuo pipefail

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_UI_NGINX_LOCATION_FIX_$(date +%Y%m%d_%H%M%S).md"
STAMP="$(date +%Y%m%d_%H%M%S)"

MY_DIR="/var/www/checkout-plans"
ADMIN_DIR="/var/www/plans-console"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  echo "FAILED=True"
  echo "REPORT=$REPORT"
  exit 1
}

log "# NDSP Checkout UI Nginx Location Fix"
log "- TIME=$(date -Is)"

[ -f "$MY_DIR/index.html" ] || fail "Missing $MY_DIR/index.html"
[ -f "$ADMIN_DIR/index.html" ] || fail "Missing $ADMIN_DIR/index.html"

if grep -q '<div id="root"></div>' "$MY_DIR/index.html"; then
  log "MY_STATIC_ROOT_OK=True"
else
  fail "Static checkout index.html does not contain React root"
fi

if grep -q '<div id="root"></div>' "$ADMIN_DIR/index.html"; then
  log "ADMIN_STATIC_ROOT_OK=True"
else
  fail "Static admin index.html does not contain React root"
fi

sudo python3 <<'PY'
from pathlib import Path
import re
import shutil
from datetime import datetime

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

candidate_dirs = [
    Path("/etc/nginx/sites-available"),
    Path("/etc/nginx/sites-enabled"),
    Path("/etc/nginx/conf.d"),
]

files = []
seen = set()

for d in candidate_dirs:
    if not d.exists():
        continue
    for p in d.iterdir():
        if not p.is_file() and not p.is_symlink():
            continue
        try:
            real = p.resolve()
        except Exception:
            real = p
        if real in seen:
            continue
        seen.add(real)
        try:
            text = real.read_text(errors="ignore")
        except Exception:
            continue
        if "my.ndsp.app" in text or "admin.ndsp.app" in text:
            files.append(real)

if not files:
    raise SystemExit("NO_NGINX_DOMAIN_FILES_FOUND")

my_block = r'''
    # NDSP_CHECKOUT_PLANS_UI_BEGIN
    location = /checkout-plans {
        return 301 /checkout-plans/;
    }

    location ^~ /checkout-plans/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /checkout-plans/index.html;
    }
    # NDSP_CHECKOUT_PLANS_UI_END
'''

admin_block = r'''
    # NDSP_ADMIN_PLANS_UI_BEGIN
    location = /plans-console {
        return 301 /plans-console/;
    }

    location ^~ /plans-console/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /plans-console/index.html;
    }
    # NDSP_ADMIN_PLANS_UI_END
'''

def remove_marker_blocks(text: str) -> str:
    patterns = [
        r'\n\s*# NDSP_CHECKOUT_PLANS_UI_BEGIN.*?# NDSP_CHECKOUT_PLANS_UI_END\s*\n',
        r'\n\s*# NDSP_ADMIN_PLANS_UI_BEGIN.*?# NDSP_ADMIN_PLANS_UI_END\s*\n',
    ]
    for pat in patterns:
        text = re.sub(pat, "\n", text, flags=re.S)
    return text

def find_server_blocks(text: str):
    blocks = []
    pattern = re.compile(r'\bserver\s*\{')
    for m in pattern.finditer(text):
        start = m.start()
        brace_start = text.find("{", m.start())
        depth = 0
        i = brace_start
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    blocks.append((start, i + 1))
                    break
            i += 1
    return blocks

def server_has_name(block: str, domain: str) -> bool:
    return re.search(r'\bserver_name\s+[^;]*' + re.escape(domain) + r'[^;]*;', block) is not None

modified = []

for path in files:
    text = path.read_text(errors="ignore")
    original = text
    text = remove_marker_blocks(text)

    blocks = find_server_blocks(text)
    inserts = []

    for start, end in blocks:
        block = text[start:end]

        if server_has_name(block, "my.ndsp.app"):
            insert_pos = end - 1
            inserts.append((insert_pos, my_block))

        if server_has_name(block, "admin.ndsp.app"):
            insert_pos = end - 1
            inserts.append((insert_pos, admin_block))

    if not inserts:
        continue

    for pos, block in sorted(inserts, reverse=True):
        text = text[:pos] + block + "\n" + text[pos:]

    if text != original:
        backup = path.with_name(path.name + f".bak_checkout_ui_location_{stamp}")
        shutil.copy2(path, backup)
        path.write_text(text)
        modified.append(str(path))

print("MODIFIED_FILES=" + ",".join(modified))
if not modified:
    raise SystemExit("NO_FILES_MODIFIED")
PY

log "NGINX_LOCATION_PATCHED=True"

sudo nginx -t
log "NGINX_CONFIG_OK=True"

sudo systemctl reload nginx
log "NGINX_RELOAD_OK=True"

sleep 2

MY_CODE="$(curl -k -s -o /tmp/ndsp_my_checkout_fixed.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_CODE="$(curl -k -s -o /tmp/ndsp_admin_plans_fixed.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

log "MY_CHECKOUT_UI_HTTP_CODE=$MY_CODE"
log "ADMIN_PLANS_UI_HTTP_CODE=$ADMIN_CODE"

[ "$MY_CODE" = "200" ] || fail "my.ndsp.app checkout UI failed"
[ "$ADMIN_CODE" = "200" ] || fail "admin.ndsp.app plans UI failed"

if grep -q '<div id="root"></div>' /tmp/ndsp_my_checkout_fixed.html; then
  log "MY_UI_ROOT_FOUND=True"
else
  log "MY_UI_RESPONSE_HEAD=$(head -c 300 /tmp/ndsp_my_checkout_fixed.html | tr '\n' ' ' || true)"
  fail "React root still not found in my checkout UI"
fi

if grep -q '<div id="root"></div>' /tmp/ndsp_admin_plans_fixed.html; then
  log "ADMIN_UI_ROOT_FOUND=True"
else
  log "ADMIN_UI_RESPONSE_HEAD=$(head -c 300 /tmp/ndsp_admin_plans_fixed.html | tr '\n' ' ' || true)"
  fail "React root still not found in admin plans UI"
fi

API_CODE="$(curl -k -s -o /tmp/ndsp_checkout_api_check.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"
log "API_PLANS_HTTP_CODE=$API_CODE"
[ "$API_CODE" = "200" ] || fail "Checkout API failed after nginx reload"

log "FINAL_STATUS=NDSP_CHECKOUT_UI_NGINX_LOCATION_FIXED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_UI_NGINX_LOCATION_FIXED"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/checkout"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"

#!/usr/bin/env bash
set -Eeuo pipefail

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_UI_SAME_ORIGIN_API_$(date +%Y%m%d_%H%M%S).md"
STAMP="$(date +%Y%m%d_%H%M%S)"

FRONTEND="/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite"
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

log "# NDSP Checkout UI Same-Origin API Fix"
log "- TIME=$(date -Is)"

[ -d "$FRONTEND" ] || fail "Frontend not found: $FRONTEND"

if ! systemctl is-active --quiet ndsp-checkout-api.service; then
  fail "ndsp-checkout-api.service is not active"
fi

LOCAL_API_CODE="$(curl -s -o /tmp/ndsp_local_checkout_api.json -w '%{http_code}' http://127.0.0.1:8088/api/v1/plans || true)"
log "LOCAL_API_CODE=$LOCAL_API_CODE"
[ "$LOCAL_API_CODE" = "200" ] || fail "Local checkout API failed"

cd "$FRONTEND"

cat > ".env" <<'ENVEOF'
VITE_NDSP_API_BASE=/checkout-api
ENVEOF

cat > "vite.config.js" <<'VITEEOF'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()]
});
VITEEOF

npm install
npm run build

[ -f "$FRONTEND/dist/index.html" ] || fail "Vite dist index.html missing"

python3 - <<'PY'
from pathlib import Path

dist = Path("/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/dist")
index = dist / "index.html"
text = index.read_text()
marker = "<!-- NDSP_CHECKOUT_ADMIN_VITE_MARKER -->"

if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)

index.write_text(text)
PY

if grep -R "https://api.ndsp.app/checkout-api" "$FRONTEND/dist" >/dev/null 2>&1; then
  fail "Old absolute api.ndsp.app endpoint still exists in build"
fi

if grep -R "/checkout-api" "$FRONTEND/dist" >/dev/null 2>&1; then
  log "FRONTEND_RELATIVE_API_FOUND=True"
else
  fail "Relative /checkout-api endpoint not found in build"
fi

sudo mkdir -p "$MY_DIR" "$ADMIN_DIR"
sudo rsync -a --delete "$FRONTEND/dist/" "$MY_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_DIR/"
sudo chown -R www-data:www-data "$MY_DIR" "$ADMIN_DIR"

log "FRONTEND_REBUILT_AND_DEPLOYED=True"

NGINX_DUMP="/tmp/ndsp_nginx_same_origin_dump_$STAMP.txt"
sudo nginx -T > "$NGINX_DUMP" 2>/tmp/ndsp_nginx_same_origin_err_$STAMP.txt || {
  cat /tmp/ndsp_nginx_same_origin_err_$STAMP.txt || true
  fail "nginx -T failed"
}

ACTIVE_FILES="$(awk '
  /^# configuration file / {
    file=$4
    gsub(":", "", file)
    print file
  }
' "$NGINX_DUMP" | sort -u)"

[ -n "$ACTIVE_FILES" ] || fail "No active nginx files detected"

sudo python3 - "$STAMP" $ACTIVE_FILES <<'PY'
from pathlib import Path
import re
import shutil
import sys

stamp = sys.argv[1]
files = [Path(x) for x in sys.argv[2:]]

checkout_ui_block = r'''
    # NDSP_CHECKOUT_PLANS_UI_BEGIN
    location = /checkout-plans {
        return 301 /checkout-plans/;
    }

    location ^~ /checkout-plans/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /checkout-plans/index.html;
        add_header X-NDSP-Checkout-UI "checkout-plans" always;
    }
    # NDSP_CHECKOUT_PLANS_UI_END
'''

admin_ui_block = r'''
    # NDSP_ADMIN_PLANS_UI_BEGIN
    location = /plans-console {
        return 301 /plans-console/;
    }

    location ^~ /plans-console/ {
        root /var/www;
        index index.html;
        try_files $uri $uri/ /plans-console/index.html;
        add_header X-NDSP-Admin-Plans-UI "plans-console" always;
    }
    # NDSP_ADMIN_PLANS_UI_END
'''

same_origin_api_block = r'''
    # NDSP_CHECKOUT_SAME_ORIGIN_API_BEGIN
    location ^~ /checkout-api/ {
        proxy_pass http://127.0.0.1:8088/;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 15s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        add_header X-NDSP-Checkout-API "same-origin" always;
    }
    # NDSP_CHECKOUT_SAME_ORIGIN_API_END
'''

def strip_old_blocks(text: str) -> str:
    markers = [
        ("NDSP_CHECKOUT_PLANS_UI_BEGIN", "NDSP_CHECKOUT_PLANS_UI_END"),
        ("NDSP_ADMIN_PLANS_UI_BEGIN", "NDSP_ADMIN_PLANS_UI_END"),
        ("NDSP_CHECKOUT_SAME_ORIGIN_API_BEGIN", "NDSP_CHECKOUT_SAME_ORIGIN_API_END"),
        ("NDSP_CHECKOUT_API_PROXY_BEGIN", "NDSP_CHECKOUT_API_PROXY_END"),
    ]

    for begin, end in markers:
        text = re.sub(
            r'\n\s*# ' + re.escape(begin) + r'.*?# ' + re.escape(end) + r'\s*\n',
            "\n",
            text,
            flags=re.S,
        )

    return text

def find_server_blocks(text: str):
    blocks = []
    for m in re.finditer(r'\bserver\s*\{', text):
        start = m.start()
        brace = text.find("{", start)
        depth = 0
        i = brace

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

def is_ssl_server(block: str) -> bool:
    return (
        re.search(r'\blisten\s+[^;]*443[^;]*;', block) is not None
        or re.search(r'\bssl_certificate\s+', block) is not None
    )

modified = []
patched = 0

for path in files:
    if not path.exists() or not path.is_file():
        continue

    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue

    original = text
    text = strip_old_blocks(text)

    inserts = []

    for start, end in find_server_blocks(text):
        block = text[start:end]

        if is_ssl_server(block):
            insert_block = (
                checkout_ui_block
                + "\n"
                + admin_ui_block
                + "\n"
                + same_origin_api_block
            )
            inserts.append((end - 1, insert_block))
            patched += 1

    for pos, block in sorted(inserts, reverse=True):
        text = text[:pos] + block + "\n" + text[pos:]

    if text != original:
        backup = path.with_name(path.name + f".bak_same_origin_checkout_api_{stamp}")
        shutil.copy2(path, backup)
        path.write_text(text)
        modified.append(str(path))

if patched == 0:
    raise SystemExit("NO_SSL_SERVER_BLOCKS_PATCHED")

if not modified:
    raise SystemExit("NO_FILES_MODIFIED")

print("PATCHED_SSL_SERVERS=" + str(patched))
print("MODIFIED_FILES=" + ",".join(modified))
PY

log "NGINX_SAME_ORIGIN_PATCH_OK=True"

sudo nginx -t
log "NGINX_CONFIG_OK=True"

sudo systemctl reload nginx
log "NGINX_RELOAD_OK=True"

sleep 2

MY_UI_CODE="$(curl -k -s -o /tmp/ndsp_my_checkout_same_origin.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -s -o /tmp/ndsp_admin_plans_same_origin.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"

MY_API_CODE="$(curl -k -s -o /tmp/ndsp_my_checkout_same_origin_api.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/plans || true)"
ADMIN_API_CODE="$(curl -k -s -o /tmp/ndsp_admin_checkout_same_origin_api.json -w '%{http_code}' https://admin.ndsp.app/checkout-api/api/v1/plans || true)"
DIRECT_API_CODE="$(curl -k -s -o /tmp/ndsp_direct_checkout_api.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"

curl -k -sI https://my.ndsp.app/checkout-api/api/v1/plans > /tmp/ndsp_my_checkout_same_origin_api.headers || true
curl -k -sI https://admin.ndsp.app/checkout-api/api/v1/plans > /tmp/ndsp_admin_checkout_same_origin_api.headers || true

log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"
log "MY_SAME_ORIGIN_API_CODE=$MY_API_CODE"
log "ADMIN_SAME_ORIGIN_API_CODE=$ADMIN_API_CODE"
log "DIRECT_API_CODE=$DIRECT_API_CODE"

[ "$MY_UI_CODE" = "200" ] || fail "my checkout UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin plans UI failed"
[ "$MY_API_CODE" = "200" ] || fail "my same-origin API failed"
[ "$ADMIN_API_CODE" = "200" ] || fail "admin same-origin API failed"
[ "$DIRECT_API_CODE" = "200" ] || fail "direct api.ndsp.app API failed"

grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" /tmp/ndsp_my_checkout_same_origin.html || fail "my UI marker missing"
grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" /tmp/ndsp_admin_plans_same_origin.html || fail "admin UI marker missing"

if grep -qi 'X-NDSP-Checkout-API: same-origin' /tmp/ndsp_my_checkout_same_origin_api.headers; then
  log "MY_SAME_ORIGIN_API_HEADER_OK=True"
else
  log "MY_API_HEADERS_BEGIN"
  cat /tmp/ndsp_my_checkout_same_origin_api.headers >> "$REPORT" || true
  log "MY_API_HEADERS_END"
  fail "my same-origin API header missing"
fi

if grep -qi 'X-NDSP-Checkout-API: same-origin' /tmp/ndsp_admin_checkout_same_origin_api.headers; then
  log "ADMIN_SAME_ORIGIN_API_HEADER_OK=True"
else
  log "ADMIN_API_HEADERS_BEGIN"
  cat /tmp/ndsp_admin_checkout_same_origin_api.headers >> "$REPORT" || true
  log "ADMIN_API_HEADERS_END"
  fail "admin same-origin API header missing"
fi

log "FINAL_STATUS=NDSP_CHECKOUT_UI_FETCH_FIXED_SAME_ORIGIN"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_UI_FETCH_FIXED_SAME_ORIGIN"
echo "REPORT=$REPORT"
echo ""
echo "Hard refresh these pages:"
echo "https://my.ndsp.app/checkout-plans/#/checkout"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"

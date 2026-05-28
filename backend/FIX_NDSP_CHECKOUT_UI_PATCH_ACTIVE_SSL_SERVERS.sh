#!/usr/bin/env bash
set -Eeuo pipefail

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_CHECKOUT_UI_PATCH_ACTIVE_SSL_SERVERS_$(date +%Y%m%d_%H%M%S).md"
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

log "# NDSP Checkout UI Patch Active SSL Servers"
log "- TIME=$(date -Is)"

[ -d "$FRONTEND" ] || fail "Frontend not found: $FRONTEND"

cd "$FRONTEND"

cat > ".env" <<'ENVEOF'
VITE_NDSP_API_BASE=https://api.ndsp.app/checkout-api
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

p = Path("/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/dist/index.html")
text = p.read_text()
marker = "<!-- NDSP_CHECKOUT_ADMIN_VITE_MARKER -->"

if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)

p.write_text(text)
PY

sudo mkdir -p "$MY_DIR" "$ADMIN_DIR"
sudo rsync -a --delete "$FRONTEND/dist/" "$MY_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_DIR/"
sudo chown -R www-data:www-data "$MY_DIR" "$ADMIN_DIR"

grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" "$MY_DIR/index.html" || fail "Marker missing in checkout static index"
grep -q "NDSP_CHECKOUT_ADMIN_VITE_MARKER" "$ADMIN_DIR/index.html" || fail "Marker missing in admin static index"

log "STATIC_BUILD_AND_DEPLOY_OK=True"

NGINX_DUMP="/tmp/ndsp_nginx_active_dump_$STAMP.txt"
sudo nginx -T > "$NGINX_DUMP" 2>/tmp/ndsp_nginx_active_dump_err_$STAMP.txt || {
  cat /tmp/ndsp_nginx_active_dump_err_$STAMP.txt || true
  fail "nginx -T failed"
}

log "NGINX_DUMP_CREATED=True"

ACTIVE_FILES="$(awk '
  /^# configuration file / {
    file=$4
    gsub(":", "", file)
    print file
  }
' "$NGINX_DUMP" | sort -u)"

if [ -z "$ACTIVE_FILES" ]; then
  fail "No active nginx config files detected from nginx -T"
fi

log "ACTIVE_FILES_BEGIN"
echo "$ACTIVE_FILES" | tee -a "$REPORT"
log "ACTIVE_FILES_END"

sudo python3 - "$STAMP" $ACTIVE_FILES <<'PY'
from pathlib import Path
import re
import shutil
import sys

stamp = sys.argv[1]
files = [Path(x) for x in sys.argv[2:]]

checkout_block = r'''
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

admin_block = r'''
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

def strip_old_blocks(text: str) -> str:
    text = re.sub(
        r'\n\s*# NDSP_CHECKOUT_PLANS_UI_BEGIN.*?# NDSP_CHECKOUT_PLANS_UI_END\s*\n',
        "\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r'\n\s*# NDSP_ADMIN_PLANS_UI_BEGIN.*?# NDSP_ADMIN_PLANS_UI_END\s*\n',
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
    # نضيف فقط داخل server blocks الخاصة بـ HTTPS/SSL
    return (
        re.search(r'\blisten\s+[^;]*443[^;]*;', block) is not None
        or re.search(r'\bssl_certificate\s+', block) is not None
    )

modified = []
patched_servers = 0

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
            insert_pos = end - 1
            inserts.append((insert_pos, checkout_block + "\n" + admin_block))
            patched_servers += 1

    if not inserts:
        if text != original:
            backup = path.with_name(path.name + f".bak_strip_checkout_ui_{stamp}")
            shutil.copy2(path, backup)
            path.write_text(text)
            modified.append(str(path))
        continue

    for pos, block in sorted(inserts, reverse=True):
        text = text[:pos] + block + "\n" + text[pos:]

    if text != original:
        backup = path.with_name(path.name + f".bak_active_ssl_checkout_ui_{stamp}")
        shutil.copy2(path, backup)
        path.write_text(text)
        modified.append(str(path))

if patched_servers == 0:
    raise SystemExit("NO_SSL_SERVER_BLOCKS_FOUND")

if not modified:
    raise SystemExit("NO_FILES_MODIFIED")

print("PATCHED_SSL_SERVERS=" + str(patched_servers))
print("MODIFIED_FILES=" + ",".join(modified))
PY

log "ACTIVE_SSL_SERVER_PATCH_OK=True"

sudo nginx -t
log "NGINX_CONFIG_OK=True"

sudo systemctl reload nginx
log "NGINX_RELOAD_OK=True"

sleep 2

MY_CODE="$(curl -k -s -o /tmp/ndsp_my_checkout_sslpatch.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_CODE="$(curl -k -s -o /tmp/ndsp_admin_plans_sslpatch.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"
API_CODE="$(curl -k -s -o /tmp/ndsp_checkout_api_sslpatch.json -w '%{http_code}' https://api.ndsp.app/checkout-api/api/v1/plans || true)"

curl -k -sI https://my.ndsp.app/checkout-plans/ > /tmp/ndsp_my_checkout_sslpatch.headers || true
curl -k -sI https://admin.ndsp.app/plans-console/ > /tmp/ndsp_admin_plans_sslpatch.headers || true

log "MY_CHECKOUT_UI_HTTP_CODE=$MY_CODE"
log "ADMIN_PLANS_UI_HTTP_CODE=$ADMIN_CODE"
log "API_PLANS_HTTP_CODE=$API_CODE"

[ "$MY_CODE" = "200" ] || fail "my checkout UI returned HTTP $MY_CODE"
[ "$ADMIN_CODE" = "200" ] || fail "admin plans UI returned HTTP $ADMIN_CODE"
[ "$API_CODE" = "200" ] || fail "checkout API returned HTTP $API_CODE"

if grep -qi 'X-NDSP-Checkout-UI: checkout-plans' /tmp/ndsp_my_checkout_sslpatch.headers; then
  log "MY_NGINX_HEADER_OK=True"
else
  log "MY_HEADERS_BEGIN"
  cat /tmp/ndsp_my_checkout_sslpatch.headers >> "$REPORT" || true
  log "MY_HEADERS_END"
  fail "my.ndsp.app did not return checkout nginx header"
fi

if grep -qi 'X-NDSP-Admin-Plans-UI: plans-console' /tmp/ndsp_admin_plans_sslpatch.headers; then
  log "ADMIN_NGINX_HEADER_OK=True"
else
  log "ADMIN_HEADERS_BEGIN"
  cat /tmp/ndsp_admin_plans_sslpatch.headers >> "$REPORT" || true
  log "ADMIN_HEADERS_END"
  fail "admin.ndsp.app did not return admin nginx header"
fi

if grep -q 'NDSP_CHECKOUT_ADMIN_VITE_MARKER' /tmp/ndsp_my_checkout_sslpatch.html; then
  log "MY_UI_MARKER_FOUND=True"
else
  log "MY_UI_RESPONSE_HEAD=$(head -c 500 /tmp/ndsp_my_checkout_sslpatch.html | tr '\n' ' ' || true)"
  fail "my checkout marker not found"
fi

if grep -q 'NDSP_CHECKOUT_ADMIN_VITE_MARKER' /tmp/ndsp_admin_plans_sslpatch.html; then
  log "ADMIN_UI_MARKER_FOUND=True"
else
  log "ADMIN_UI_RESPONSE_HEAD=$(head -c 500 /tmp/ndsp_admin_plans_sslpatch.html | tr '\n' ' ' || true)"
  fail "admin plans marker not found"
fi

log "FINAL_STATUS=NDSP_CHECKOUT_UI_ACTIVE_SSL_SERVERS_PATCHED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_CHECKOUT_UI_ACTIVE_SSL_SERVERS_PATCHED"
echo "REPORT=$REPORT"
echo ""
echo "Open:"
echo "https://my.ndsp.app/checkout-plans/#/checkout"
echo "https://admin.ndsp.app/plans-console/#/admin/plans"

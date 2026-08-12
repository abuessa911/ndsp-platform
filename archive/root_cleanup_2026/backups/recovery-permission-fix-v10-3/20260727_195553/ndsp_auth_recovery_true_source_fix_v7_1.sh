#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

# ============================================================
# NDSP — Auth Recovery True Source Fix V7
#
# Fixes:
# 1) Login link in true auth source ui/src/main.tsx
# 2) Rebuilds ui-dist in a new atomic auth release
# 3) Routes recovery pages on my.ndsp.app to existing static pages
# 4) Routes same-origin recovery APIs to service 127.0.0.1:9027
# 5) Fixes reset email link in password_reset_gateway/server.js
#
# No database schema changes.
# No direct database edits.
# No direct edits to ui-dist.
# ============================================================

CONFIRM="${NDSP_CONFIRM_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7:-NO}"

DOMAIN="${NDSP_DOMAIN:-my.ndsp.app}"
PROJECT="${NDSP_PROJECT:-$HOME/empire-core-new}"

AUTH_BASE="${NDSP_AUTH_BASE:-/opt/ndsp-auth-core-clean}"
AUTH_CURRENT="${NDSP_AUTH_CURRENT:-$AUTH_BASE/current}"
AUTH_SERVICE="${NDSP_AUTH_SERVICE:-ndsp-auth-core-clean.service}"

RESET_PACKAGE="${NDSP_RESET_PACKAGE:-$PROJECT/backend/password_reset_gateway}"
RESET_SERVER="${NDSP_RESET_SERVER:-$RESET_PACKAGE/server.js}"
RESET_SERVICE="${NDSP_RESET_SERVICE:-ndsp-password-reset.service}"
RESET_PORT="${NDSP_RESET_PORT:-9027}"

WEB_ROOT="${NDSP_WEB_ROOT:-/var/www/ndsp-my}"
FORGOT_HTML="${NDSP_FORGOT_HTML:-$WEB_ROOT/forgot-password.html}"
RESET_HTML="${NDSP_RESET_HTML:-$WEB_ROOT/reset-password.html}"

CANONICAL_RECOVERY="${NDSP_CANONICAL_RECOVERY:-$PROJECT/frontend/auth-recovery}"

TS="$(date +%Y%m%d_%H%M%S)"
WORK="$(mktemp -d /tmp/ndsp-auth-recovery-v7.XXXXXX)"

BACKUP="$PROJECT/backups/auth-recovery-true-source-fix-v7/$TS"
REPORT="$PROJECT/docs/05-runbooks/NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_${TS}.md"

NEW_RELEASE="$AUTH_BASE/releases/${TS}-auth-recovery-true-source-fix-v7"
OLD_RELEASE=""

BACKEND_STAGE="$WORK/password-reset-server.js"
NGINX_STAGE="$WORK/nginx-stage"
NGINX_MANIFEST="$WORK/nginx-stage-manifest.tsv"

AUTH_CUTOVER=0
BACKEND_INSTALLED=0
NGINX_INSTALLED=0
CANONICAL_INSTALLED=0
CANONICAL_EXISTED=0

SUDO_KEEPALIVE_PID=""

mkdir -p \
    "$BACKUP/nginx" \
    "$NGINX_STAGE" \
    "$(dirname "$REPORT")"

: > "$REPORT"
chmod 600 "$REPORT"

log() {
    printf '%s\n' "$*" | tee -a "$REPORT"
}

section() {
    log ""
    log "============================================================"
    log "$*"
    log "============================================================"
}

fail() {
    log "FAIL=$*"
    return 1
}

cleanup() {
    local rc=$?

    if [[ -n "$SUDO_KEEPALIVE_PID" ]]; then
        kill "$SUDO_KEEPALIVE_PID" >/dev/null 2>&1 || true
    fi

    rm -rf "$WORK" >/dev/null 2>&1 || true
    exit "$rc"
}

rollback() {
    local rc=$?

    trap - ERR INT TERM
    set +e

    log ""
    log "ROLLBACK_REQUIRED=YES"
    log "ROLLBACK_TRIGGER_EXIT=$rc"

    if [[ "$NGINX_INSTALLED" == "1" ]] &&
       [[ -f "$BACKUP/nginx-files.tsv" ]]; then

        while IFS=$'\t' read -r ORIGINAL BACKUP_FILE; do
            [[ -n "$ORIGINAL" ]] || continue
            [[ -f "$BACKUP_FILE" ]] || continue
            sudo cp -a "$BACKUP_FILE" "$ORIGINAL" || true
            log "NGINX_RESTORED=$ORIGINAL"
        done < "$BACKUP/nginx-files.tsv"

        sudo nginx -t >/dev/null 2>&1 || true
        sudo systemctl reload nginx >/dev/null 2>&1 || true
        log "NGINX_ROLLBACK=COMPLETE"
    fi

    if [[ "$BACKEND_INSTALLED" == "1" ]] &&
       [[ -f "$BACKUP/password-reset-server.before.js" ]]; then

        sudo cp -a \
            "$BACKUP/password-reset-server.before.js" \
            "$RESET_SERVER" || true

        node --check "$RESET_SERVER" >/dev/null 2>&1 || true
        sudo systemctl restart "$RESET_SERVICE" >/dev/null 2>&1 || true
        log "PASSWORD_RESET_BACKEND_ROLLBACK=COMPLETE"
    fi

    if [[ "$AUTH_CUTOVER" == "1" ]] &&
       [[ -n "$OLD_RELEASE" ]] &&
       [[ -d "$OLD_RELEASE" ]]; then

        TEMP_LINK="$AUTH_BASE/.current-v7-rollback-$TS"
        sudo rm -f "$TEMP_LINK" || true
        sudo ln -s "$OLD_RELEASE" "$TEMP_LINK" || true
        sudo mv -Tf "$TEMP_LINK" "$AUTH_CURRENT" || true
        sudo systemctl restart "$AUTH_SERVICE" >/dev/null 2>&1 || true

        log "AUTH_RELEASE_ROLLBACK=COMPLETE"
        log "AUTH_RELEASE_RESTORED=$OLD_RELEASE"
    fi

    if [[ "$CANONICAL_INSTALLED" == "1" ]]; then
        rm -rf "$CANONICAL_RECOVERY" || true

        if [[ "$CANONICAL_EXISTED" == "1" ]] &&
           [[ -f "$BACKUP/canonical-recovery.before.tar.gz" ]]; then

            tar \
                -C "$(dirname "$CANONICAL_RECOVERY")" \
                -xzf "$BACKUP/canonical-recovery.before.tar.gz" || true
        fi

        log "CANONICAL_RECOVERY_ROLLBACK=COMPLETE"
    fi

    log "DATABASE_SCHEMA_CHANGED=NO"
    log "DATABASE_DIRECT_EDIT=NO"
    log "FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_FAILED"
    log "REPORT=$REPORT"
    exit "$rc"
}

trap cleanup EXIT
trap rollback ERR INT TERM

section "NDSP — AUTH RECOVERY TRUE SOURCE FIX V7"

log "DATE=$(date -Is)"
log "HOST=$(hostname -f 2>/dev/null || hostname)"
log "DOMAIN=$DOMAIN"
log "PROJECT=$PROJECT"
log "AUTH_CURRENT=$AUTH_CURRENT"
log "AUTH_SERVICE=$AUTH_SERVICE"
log "RESET_SERVER=$RESET_SERVER"
log "RESET_SERVICE=$RESET_SERVICE"
log "RESET_PORT=$RESET_PORT"
log "FORGOT_HTML=$FORGOT_HTML"
log "RESET_HTML=$RESET_HTML"
log "CANONICAL_RECOVERY=$CANONICAL_RECOVERY"
log "BACKUP=$BACKUP"
log "REPORT=$REPORT"

section "0) EXPLICIT CONFIRMATION AND PRIVILEGES"

[[ "$CONFIRM" == "YES" ]] ||
    fail "SET_NDSP_CONFIRM_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7=YES"

sudo -v

(
    while true; do
        sudo -n true >/dev/null 2>&1 || exit
        sleep 40
    done
) &

SUDO_KEEPALIVE_PID=$!

log "EXPLICIT_CONFIRMATION=YES"
log "SUDO_GATE=PASS"

section "1) REQUIRED COMMANDS AND TRUE SOURCE BINDINGS"

for command_name in \
    bash python3 node npm curl grep awk sed find sort \
    sha256sum stat install readlink systemctl nginx \
    rsync tar cmp ss; do

    command -v "$command_name" >/dev/null 2>&1 ||
        fail "MISSING_COMMAND:$command_name"
done

[[ -L "$AUTH_CURRENT" ]] ||
    fail "AUTH_CURRENT_IS_NOT_SYMLINK:$AUTH_CURRENT"

OLD_RELEASE="$(readlink -f "$AUTH_CURRENT")"

[[ -d "$OLD_RELEASE" ]] ||
    fail "ACTIVE_AUTH_RELEASE_MISSING:$OLD_RELEASE"

AUTH_UI_SOURCE="$OLD_RELEASE/ui/src/main.tsx"
AUTH_UI_DIST="$OLD_RELEASE/ui-dist/index.html"

[[ -f "$AUTH_UI_SOURCE" ]] ||
    fail "AUTH_UI_SOURCE_MISSING:$AUTH_UI_SOURCE"

[[ -f "$AUTH_UI_DIST" ]] ||
    fail "AUTH_UI_DIST_MISSING:$AUTH_UI_DIST"

[[ -f "$RESET_SERVER" ]] ||
    fail "PASSWORD_RESET_SOURCE_MISSING:$RESET_SERVER"

[[ -f "$FORGOT_HTML" ]] ||
    fail "EXISTING_FORGOT_PAGE_MISSING:$FORGOT_HTML"

[[ -f "$RESET_HTML" ]] ||
    fail "EXISTING_RESET_PAGE_MISSING:$RESET_HTML"

systemctl is-active --quiet "$AUTH_SERVICE" ||
    fail "AUTH_SERVICE_NOT_ACTIVE:$AUTH_SERVICE"

systemctl is-active --quiet "$RESET_SERVICE" ||
    fail "PASSWORD_RESET_SERVICE_NOT_ACTIVE:$RESET_SERVICE"

SERVICE_WORKDIR="$(
    systemctl show "$RESET_SERVICE" \
        -p WorkingDirectory \
        --value
)"

[[ "$SERVICE_WORKDIR" == "$RESET_PACKAGE" ]] ||
    fail "PASSWORD_RESET_SERVICE_WORKDIR_MISMATCH:$SERVICE_WORKDIR"

sudo ss -lntpH |
    grep -Eq ":${RESET_PORT}[[:space:]].*pid=" ||
    fail "PASSWORD_RESET_PORT_NOT_LISTENING:$RESET_PORT"

PUBLIC_LOGIN_BEFORE="$WORK/public-login-before.html"

LOGIN_BEFORE_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H 'Cache-Control: no-cache' \
        -o "$PUBLIC_LOGIN_BEFORE" \
        -w '%{http_code}' \
        "https://$DOMAIN/login/?v7_preflight=$TS"
)"

[[ "$LOGIN_BEFORE_HTTP" == "200" ]] ||
    fail "PUBLIC_LOGIN_PREFLIGHT_HTTP_$LOGIN_BEFORE_HTTP"

cmp -s "$PUBLIC_LOGIN_BEFORE" "$AUTH_UI_DIST" ||
    fail "PUBLIC_LOGIN_DOES_NOT_MATCH_ACTIVE_AUTH_UI_DIST"

grep -Fq 'href="/reset-password/"' "$AUTH_UI_SOURCE" ||
    grep -Fq "href='/reset-password/'" "$AUTH_UI_SOURCE" ||
    fail "EXPECTED_WRONG_FORGOT_LINK_NOT_FOUND_IN_TRUE_SOURCE"

grep -Fq '/reset-password.html?token=' "$RESET_SERVER" ||
    fail "EXPECTED_LEGACY_EMAIL_LINK_NOT_FOUND"

log "OLD_AUTH_RELEASE=$OLD_RELEASE"
log "PUBLIC_LOGIN_EQUALS_ACTIVE_UI_DIST=YES"
log "TRUE_LOGIN_SOURCE=$AUTH_UI_SOURCE"
log "TRUE_LOGIN_BUILD=$AUTH_UI_DIST"
log "TRUE_SOURCE_BINDING_GATE=PASS"

section "2) VERIFY EXISTING RECOVERY PAGE CONTRACT"

grep -Eqi \
    'forgot|استعادة|استرجاع|نسيت|email|البريد' \
    "$FORGOT_HTML" ||
    fail "FORGOT_PAGE_CONTENT_NOT_RECOGNIZED"

grep -Eqi \
    'reset|password|كلمة المرور|رمز|token' \
    "$RESET_HTML" ||
    fail "RESET_PAGE_CONTENT_NOT_RECOGNIZED"

# NDSP_RECOVERY_STRUCTURAL_GATE_V7_1
for RECOVERY_FILE in "$FORGOT_HTML" "$RESET_HTML"; do
    if grep -Eqi \
        'portal-v50|approved-design|decision-room-v31|data-ndsp-page=["'"'"']portal|class=["'"'"'][^"'"'"']*(sidebar|side-menu|top-menu|market-explorer|opportunity-explorer)' \
        "$RECOVERY_FILE"; then

        fail "RECOVERY_STATIC_FILE_CONTAINS_PORTAL_STRUCTURE:$RECOVERY_FILE"
    fi
done

grep -Fq '/api/auth/forgot-password' "$FORGOT_HTML" ||
    fail "FORGOT_PAGE_CANONICAL_API_MISSING"

grep -Eqi '<form|type=["'"'"']email["'"'"']|id=["'"'"'][^"'"'"']*email' "$FORGOT_HTML" ||
    fail "FORGOT_PAGE_FORM_STRUCTURE_MISSING"

grep -Fq '/api/auth/reset-password' "$RESET_HTML" ||
    fail "RESET_PAGE_CANONICAL_API_MISSING"

grep -Eqi 'newPassword|new_password|confirmPassword|newPassword2' "$RESET_HTML" ||
    fail "RESET_PAGE_PASSWORD_FIELDS_MISSING"

log "EXISTING_RECOVERY_PAGE_CONTENT_GATE=PASS"

section "3) BACKUP CURRENT SOURCES"

sudo cp -a \
    "$RESET_SERVER" \
    "$BACKUP/password-reset-server.before.js"

if [[ -d "$CANONICAL_RECOVERY" ]]; then
    CANONICAL_EXISTED=1

    tar \
        -C "$(dirname "$CANONICAL_RECOVERY")" \
        -czf "$BACKUP/canonical-recovery.before.tar.gz" \
        "$(basename "$CANONICAL_RECOVERY")"
fi

: > "$BACKUP/nginx-files.tsv"

NGINX_INDEX=0

for path in \
    /etc/nginx/sites-enabled/* \
    /etc/nginx/conf.d/*.conf; do

    [[ -e "$path" ]] || continue

    resolved="$(readlink -f "$path")"

    [[ -f "$resolved" ]] || continue

    if sudo grep -Eq \
        'server_name[[:space:]][^;]*my\.ndsp\.app' \
        "$resolved"; then

        NGINX_INDEX=$((NGINX_INDEX + 1))
        backup_file="$BACKUP/nginx/nginx-${NGINX_INDEX}.before.conf"

        sudo cp -a "$resolved" "$backup_file"
        sudo chown "$(id -u):$(id -g)" "$backup_file"

        printf '%s\t%s\n' \
            "$resolved" \
            "$backup_file" \
            >> "$BACKUP/nginx-files.tsv"
    fi
done

[[ "$NGINX_INDEX" -ge 1 ]] ||
    fail "ACTIVE_MY_NDSP_NGINX_SOURCE_NOT_FOUND"

sudo chown -R "$(id -u):$(id -g)" "$BACKUP"

sha256sum \
    "$AUTH_UI_SOURCE" \
    "$AUTH_UI_DIST" \
    "$RESET_SERVER" \
    "$FORGOT_HTML" \
    "$RESET_HTML" \
    "$BACKUP"/nginx/*.conf \
    > "$BACKUP/prechange-sha256.txt"

log "CANONICAL_RECOVERY_EXISTED=$CANONICAL_EXISTED"
log "NGINX_BACKUP_FILE_COUNT=$NGINX_INDEX"
log "BACKUP_GATE=PASS"

section "4) CREATE NEW AUTH RELEASE"

[[ ! -e "$NEW_RELEASE" ]] ||
    fail "NEW_AUTH_RELEASE_ALREADY_EXISTS:$NEW_RELEASE"

sudo mkdir -p "$NEW_RELEASE"

sudo rsync -a \
    --exclude='node_modules' \
    "$OLD_RELEASE/" \
    "$NEW_RELEASE/"

for RELATIVE_PATH in \
    node_modules \
    ui/node_modules \
    server/node_modules; do

    SOURCE_NODE_MODULES="$OLD_RELEASE/$RELATIVE_PATH"
    TARGET_NODE_MODULES="$NEW_RELEASE/$RELATIVE_PATH"

    if [[ -d "$SOURCE_NODE_MODULES" ]] ||
       [[ -L "$SOURCE_NODE_MODULES" ]]; then

        sudo mkdir -p "$(dirname "$TARGET_NODE_MODULES")"
        sudo rm -rf "$TARGET_NODE_MODULES"

        sudo ln -s \
            "$(readlink -f "$SOURCE_NODE_MODULES")" \
            "$TARGET_NODE_MODULES"

        log "NODE_MODULES_REUSED=$RELATIVE_PATH"
    fi
done

OLD_UID="$(stat -c '%u' "$OLD_RELEASE")"
OLD_GID="$(stat -c '%g' "$OLD_RELEASE")"

sudo chown -R "$OLD_UID:$OLD_GID" "$NEW_RELEASE"

NEW_AUTH_UI_SOURCE="$NEW_RELEASE/ui/src/main.tsx"

[[ -f "$NEW_AUTH_UI_SOURCE" ]] ||
    fail "NEW_AUTH_UI_SOURCE_MISSING"

log "NEW_AUTH_RELEASE=$NEW_RELEASE"
log "NEW_AUTH_RELEASE_COPY_GATE=PASS"

section "5) FIX LOGIN LINK IN TRUE SOURCE"

python3 - "$NEW_AUTH_UI_SOURCE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="strict")

pattern = re.compile(
    r"href=([\"'])/reset-password/\1"
    r"(?P<middle>[^>]*>)"
    r"(?P<label>\s*(?:نسيت\s+كلمة\s+المرور\??|Forgot\s+(?:your\s+)?password\??)\s*)",
    flags=re.IGNORECASE | re.DOTALL,
)

text, count = pattern.subn(
    lambda match: (
        'href="/forgot-password/"'
        + match.group("middle")
        + match.group("label")
    ),
    text,
)

if count != 1:
    raise SystemExit(
        f"EXPECTED_ONE_TRUE_SOURCE_REPLACEMENT_FOUND={count}"
    )

wrong = re.search(
    r"href=([\"'])/reset-password/\1"
    r"[^>]*>\s*(?:نسيت\s+كلمة\s+المرور|Forgot\s+(?:your\s+)?password)",
    text,
    flags=re.IGNORECASE | re.DOTALL,
)

if wrong:
    raise SystemExit(
        "WRONG_FORGOT_LINK_REMAINS_IN_TRUE_SOURCE"
    )

if "/forgot-password/" not in text:
    raise SystemExit(
        "CORRECT_FORGOT_LINK_MISSING"
    )

path.write_text(text, encoding="utf-8")
print("TRUE_SOURCE_REPLACEMENT_COUNT=1")
PY

log "TRUE_AUTH_SOURCE_LOGIN_LINK_GATE=PASS"

section "6) BUILD NEW AUTH UI"

BUILD_DIR="$(
    python3 - "$NEW_RELEASE" <<'PY'
from pathlib import Path
import json
import sys

release = Path(sys.argv[1])

for package_json in (
    release / "ui" / "package.json",
    release / "package.json",
):
    if not package_json.is_file():
        continue

    data = json.loads(
        package_json.read_text(encoding="utf-8")
    )

    if "build" in (data.get("scripts") or {}):
        print(package_json.parent)
        raise SystemExit(0)

raise SystemExit(1)
PY
)" || fail "AUTH_UI_BUILD_PACKAGE_NOT_FOUND"

sudo rm -rf "$NEW_RELEASE/ui-dist"

if [[ -f "$BUILD_DIR/pnpm-lock.yaml" ]] &&
   command -v pnpm >/dev/null 2>&1; then

    sudo env CI=1 \
        pnpm --dir "$BUILD_DIR" run build \
        2>&1 |
        tee "$BACKUP/auth-ui-build.log" |
        tee -a "$REPORT"

elif [[ -f "$BUILD_DIR/yarn.lock" ]] &&
     command -v yarn >/dev/null 2>&1; then

    (
        cd "$BUILD_DIR"
        sudo env CI=1 yarn build
    ) 2>&1 |
        tee "$BACKUP/auth-ui-build.log" |
        tee -a "$REPORT"

else
    sudo env CI=1 \
        npm --prefix "$BUILD_DIR" run build \
        2>&1 |
        tee "$BACKUP/auth-ui-build.log" |
        tee -a "$REPORT"
fi

NEW_UI_INDEX="$NEW_RELEASE/ui-dist/index.html"
NEW_UI_ASSETS="$NEW_RELEASE/ui-dist/assets"

[[ -f "$NEW_UI_INDEX" ]] ||
    fail "NEW_UI_DIST_INDEX_NOT_BUILT"

[[ -d "$NEW_UI_ASSETS" ]] ||
    fail "NEW_UI_DIST_ASSETS_NOT_BUILT"

python3 - "$NEW_UI_ASSETS" <<'PY'
from pathlib import Path
import re
import sys

assets = Path(sys.argv[1])
bundles = list(assets.glob("*.js"))

if not bundles:
    raise SystemExit("NO_BUILT_JS_BUNDLES")

correct = False
wrong = False

for bundle in bundles:
    text = bundle.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if re.search(
        r"href:[\"']/forgot-password/[\"']"
        r".{0,400}(?:نسيت كلمة المرور|Forgot(?: your)? password)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        correct = True

    if re.search(
        r"href:[\"']/reset-password/[\"']"
        r".{0,400}(?:نسيت كلمة المرور|Forgot(?: your)? password)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        wrong = True

if not correct:
    raise SystemExit(
        "BUILT_BUNDLE_CORRECT_FORGOT_LINK_MISSING"
    )

if wrong:
    raise SystemExit(
        "BUILT_BUNDLE_WRONG_FORGOT_LINK_REMAINS"
    )

print("TRUE_SOURCE_BUILD_GATE=PASS")
PY

log "AUTH_UI_BUILD_DIR=$BUILD_DIR"
log "TRUE_SOURCE_BUILD_GATE=PASS"

section "7) FIX RESET EMAIL LINK IN BACKEND SOURCE"

cp -a "$RESET_SERVER" "$BACKEND_STAGE"

python3 - "$BACKEND_STAGE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="strict")

replacement = (
    "    const link = "
    "`https://my.ndsp.app/reset-password/"
    "?token=${encodeURIComponent(resetToken)}"
    "&email=${encodeURIComponent(user.email)}`;"
)

pattern = re.compile(
    r"^[ \t]*const[ \t]+link[ \t]*=[ \t]*"
    r"`[^`]*?/reset-password\.html"
    r"\?token=\$\{resetToken\}"
    r"&email=\$\{encodeURIComponent\(user\.email\)\}`;[ \t]*$",
    flags=re.MULTILINE,
)

text, count = pattern.subn(replacement, text)

if count != 1:
    raise SystemExit(
        f"EXPECTED_ONE_EMAIL_LINK_REPLACEMENT_FOUND={count}"
    )

if "/reset-password.html?token=" in text:
    raise SystemExit(
        "LEGACY_RESET_HTML_LINK_REMAINS"
    )

if "https://my.ndsp.app/reset-password/?token=" not in text:
    raise SystemExit(
        "CANONICAL_RESET_LINK_MISSING"
    )

path.write_text(text, encoding="utf-8")
PY

node --check "$BACKEND_STAGE"

log "PASSWORD_RESET_EMAIL_LINK_SOURCE_GATE=PASS"

section "8) CREATE CANONICAL RECOVERY SOURCE SNAPSHOT"

CANONICAL_STAGE="$WORK/canonical-recovery"
mkdir -p "$CANONICAL_STAGE"

cp -a "$FORGOT_HTML" "$CANONICAL_STAGE/forgot-password.html"
cp -a "$RESET_HTML" "$CANONICAL_STAGE/reset-password.html"

cat > "$CANONICAL_STAGE/manifest.json" <<JSON
{
  "version": "7.0.0",
  "generated_at": "$(date -Is)",
  "forgot_page_source": "$FORGOT_HTML",
  "reset_page_source": "$RESET_HTML",
  "public_forgot_route": "/forgot-password/",
  "public_reset_route": "/reset-password/",
  "forgot_api": "/api/auth/forgot-password",
  "reset_api": "/api/auth/reset-password",
  "password_reset_service": "$RESET_SERVICE",
  "password_reset_port": $RESET_PORT,
  "database_schema_change": false,
  "database_direct_edit": false
}
JSON

CANONICAL_PARENT="$(dirname "$CANONICAL_RECOVERY")"
CANONICAL_NAME="$(basename "$CANONICAL_RECOVERY")"
CANONICAL_TEMP="$CANONICAL_PARENT/.${CANONICAL_NAME}.v7-stage-$TS"
CANONICAL_OLD="$CANONICAL_PARENT/.${CANONICAL_NAME}.v7-old-$TS"

mkdir -p "$CANONICAL_PARENT"
rm -rf "$CANONICAL_TEMP" "$CANONICAL_OLD"

rsync -a \
    --delete \
    "$CANONICAL_STAGE/" \
    "$CANONICAL_TEMP/"

if [[ -d "$CANONICAL_RECOVERY" ]]; then
    mv "$CANONICAL_RECOVERY" "$CANONICAL_OLD"
fi

mv "$CANONICAL_TEMP" "$CANONICAL_RECOVERY"
CANONICAL_INSTALLED=1

log "CANONICAL_RECOVERY_SOURCE=$CANONICAL_RECOVERY"
log "CANONICAL_RECOVERY_SOURCE_GATE=PASS"

section "9) PREPARE NGINX SOURCE ROUTES"

mapfile -t NGINX_FILES < <(
    cut -f1 "$BACKUP/nginx-files.tsv"
)

python3 - \
    "$NGINX_STAGE" \
    "$NGINX_MANIFEST" \
    "$RESET_PORT" \
    "${NGINX_FILES[@]}" <<'PY'
from pathlib import Path
import re
import sys

output_dir = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])
port = sys.argv[3]
source_files = [Path(value) for value in sys.argv[4:]]

BEGIN = "# NDSP_AUTH_RECOVERY_ROUTES_V7_BEGIN"
END = "# NDSP_AUTH_RECOVERY_ROUTES_V7_END"

managed = f"""
    {BEGIN}

    location = /forgot-password {{
        return 308 /forgot-password/$is_args$args;
    }}

    location = /forgot-password/ {{
        root /var/www/ndsp-my;
        try_files /forgot-password.html =404;
    }}

    location = /reset-password {{
        return 308 /reset-password/$is_args$args;
    }}

    location = /reset-password/ {{
        root /var/www/ndsp-my;
        try_files /reset-password.html =404;
    }}

    location = /api/auth/forgot-password {{
        proxy_pass http://127.0.0.1:{port}/api/auth/forgot-password;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }}

    location = /api/auth/reset-password {{
        proxy_pass http://127.0.0.1:{port}/api/auth/reset-password;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }}

    {END}
"""


def matching_brace(text, opening):
    depth = 0
    quote = None
    escaped = False
    comment = False

    for index in range(opening, len(text)):
        char = text[index]

        if comment:
            if char == "\n":
                comment = False
            continue

        if quote:
            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == quote:
                quote = None

            continue

        if char == "#":
            comment = True
            continue

        if char in ("'", '"'):
            quote = char
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1

            if depth == 0:
                return index

    raise RuntimeError("unmatched nginx brace")


def remove_managed(block):
    return re.sub(
        r"# NDSP_AUTH_RECOVERY_ROUTES_V[0-9]+_BEGIN"
        r".*?"
        r"# NDSP_AUTH_RECOVERY_ROUTES_V[0-9]+_END"
        r"\s*",
        "",
        block,
        flags=re.DOTALL,
    )


def remove_conflicts(block):
    patterns = [
        re.compile(
            r"(?m)^[ \t]*location[ \t]+=[ \t]+"
            r"/(?:forgot-password|reset-password|"
            r"api/auth/forgot-password|api/auth/reset-password)"
            r"/?[ \t]*\{"
        ),
    ]

    ranges = []

    for pattern in patterns:
        for match in pattern.finditer(block):
            opening = block.find("{", match.start())
            closing = matching_brace(block, opening)
            start = match.start()
            end = closing + 1

            while end < len(block) and block[end] in " \t":
                end += 1

            if end < len(block) and block[end] == "\n":
                end += 1

            ranges.append((start, end))

    for start, end in sorted(set(ranges), reverse=True):
        block = block[:start] + block[end:]

    return block


manifest = []
https_blocks = 0

for index, source in enumerate(source_files, start=1):
    text = source.read_text(encoding="utf-8", errors="strict")
    replacements = []

    for match in re.finditer(
        r"(?m)^[ \t]*server[ \t]*\{",
        text,
    ):
        opening = text.find("{", match.start())
        closing = matching_brace(text, opening)
        block = text[match.start():closing + 1]

        if not re.search(
            r"server_name\s+[^;]*\bmy\.ndsp\.app\b[^;]*;",
            block,
        ):
            continue

        if not (
            re.search(
                r"listen\s+(?:\[[^\]]+\]:)?443\b",
                block,
            )
            or re.search(r"\bssl_certificate\b", block)
        ):
            continue

        block = remove_managed(block)
        block = remove_conflicts(block)

        final_brace = block.rfind("}")

        block = (
            block[:final_brace].rstrip()
            + "\n"
            + managed
            + "\n"
            + block[final_brace:]
        )

        replacements.append(
            (match.start(), closing + 1, block)
        )

    if not replacements:
        continue

    https_blocks += len(replacements)

    for start, end, block in reversed(replacements):
        text = text[:start] + block + text[end:]

    stage = output_dir / f"nginx-{index}.conf"
    stage.write_text(text, encoding="utf-8")

    manifest.append(
        (str(source), str(stage), str(len(replacements)))
    )

if https_blocks != 1:
    raise SystemExit(
        f"EXPECTED_ONE_MY_NDSP_HTTPS_BLOCK_FOUND={https_blocks}"
    )

manifest_path.write_text(
    "\n".join("\t".join(row) for row in manifest) + "\n",
    encoding="utf-8",
)

print(f"NGINX_PATCHED_FILE_COUNT={len(manifest)}")
print(f"NGINX_PATCHED_HTTPS_SERVER_COUNT={https_blocks}")
PY

[[ -s "$NGINX_MANIFEST" ]] ||
    fail "NGINX_STAGE_MANIFEST_EMPTY"

grep -Rq \
    'NDSP_AUTH_RECOVERY_ROUTES_V7_BEGIN' \
    "$NGINX_STAGE" ||
    fail "NGINX_MANAGED_MARKER_MISSING"

log "NGINX_SOURCE_STAGE_GATE=PASS"

section "10) INSTALL BACKEND AND NGINX SOURCES"

BACKEND_UID="$(stat -c '%u' "$RESET_SERVER")"
BACKEND_GID="$(stat -c '%g' "$RESET_SERVER")"
BACKEND_MODE="$(stat -c '%a' "$RESET_SERVER")"

sudo install \
    -o "$BACKEND_UID" \
    -g "$BACKEND_GID" \
    -m "$BACKEND_MODE" \
    "$BACKEND_STAGE" \
    "$RESET_SERVER"

BACKEND_INSTALLED=1

while IFS=$'\t' read -r ORIGINAL STAGE COUNT; do
    [[ -n "$ORIGINAL" ]] || continue

    ORIGINAL_UID="$(stat -c '%u' "$ORIGINAL")"
    ORIGINAL_GID="$(stat -c '%g' "$ORIGINAL")"
    ORIGINAL_MODE="$(stat -c '%a' "$ORIGINAL")"

    sudo install \
        -o "$ORIGINAL_UID" \
        -g "$ORIGINAL_GID" \
        -m "$ORIGINAL_MODE" \
        "$STAGE" \
        "$ORIGINAL"

    log "NGINX_SOURCE_INSTALLED=$ORIGINAL"
done < "$NGINX_MANIFEST"

NGINX_INSTALLED=1

node --check "$RESET_SERVER"
sudo nginx -t

log "BACKEND_SOURCE_INSTALL_GATE=PASS"
log "NGINX_SOURCE_INSTALL_GATE=PASS"

section "11) ATOMIC AUTH CUTOVER AND RELOAD"

TEMP_LINK="$AUTH_BASE/.current-v7-$TS"

sudo rm -f "$TEMP_LINK"
sudo ln -s "$NEW_RELEASE" "$TEMP_LINK"
sudo mv -Tf "$TEMP_LINK" "$AUTH_CURRENT"

AUTH_CUTOVER=1

sudo systemctl restart "$AUTH_SERVICE"
sudo systemctl restart "$RESET_SERVICE"

sleep 3

systemctl is-active --quiet "$AUTH_SERVICE" ||
    fail "AUTH_SERVICE_FAILED_AFTER_CUTOVER"

systemctl is-active --quiet "$RESET_SERVICE" ||
    fail "RESET_SERVICE_FAILED_AFTER_RESTART"

sudo nginx -t
sudo systemctl reload nginx

sleep 2

ACTIVE_AFTER="$(readlink -f "$AUTH_CURRENT")"

[[ "$ACTIVE_AFTER" == "$NEW_RELEASE" ]] ||
    fail "AUTH_CURRENT_DID_NOT_POINT_TO_NEW_RELEASE"

log "AUTH_ACTIVE_RELEASE=$ACTIVE_AFTER"
log "AUTH_SERVICE_RESTARTED=YES"
log "RESET_SERVICE_RESTARTED=YES"
log "NGINX_RELOADED=YES"

section "12) VERIFY PUBLIC LOGIN TRUE BUILD"

PUBLIC_LOGIN_AFTER="$WORK/public-login-after.html"

LOGIN_AFTER_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H 'Cache-Control: no-cache' \
        -H 'Pragma: no-cache' \
        -o "$PUBLIC_LOGIN_AFTER" \
        -w '%{http_code}' \
        "https://$DOMAIN/login/?recovery_v7=$TS"
)"

[[ "$LOGIN_AFTER_HTTP" == "200" ]] ||
    fail "PUBLIC_LOGIN_AFTER_HTTP_$LOGIN_AFTER_HTTP"

cmp -s \
    "$PUBLIC_LOGIN_AFTER" \
    "$NEW_RELEASE/ui-dist/index.html" ||
    fail "PUBLIC_LOGIN_DOES_NOT_EQUAL_NEW_UI_DIST"

PUBLIC_JS_URL="$(
    python3 - \
        "$PUBLIC_LOGIN_AFTER" \
        "https://$DOMAIN/login/" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
import sys

html_file, base_url = sys.argv[1:]

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":
            source = dict(attrs).get("src")

            if source:
                self.sources.append(urljoin(base_url, source))

parser = Parser()
parser.feed(
    Path(html_file).read_text(
        encoding="utf-8",
        errors="ignore",
    )
)

for source in parser.sources:
    if ".js" in source:
        print(source)
        break
PY
)"

[[ -n "$PUBLIC_JS_URL" ]] ||
    fail "PUBLIC_LOGIN_JS_URL_NOT_FOUND"

curl -sS \
    --connect-timeout 8 \
    --max-time 30 \
    -H 'Cache-Control: no-cache' \
    -o "$WORK/public-login-after.js" \
    "$PUBLIC_JS_URL"

python3 - "$WORK/public-login-after.js" <<'PY'
from pathlib import Path
import re
import sys

text = Path(sys.argv[1]).read_text(
    encoding="utf-8",
    errors="ignore",
)

if not re.search(
    r"href:[\"']/forgot-password/[\"']"
    r".{0,400}(?:نسيت كلمة المرور|Forgot(?: your)? password)",
    text,
    flags=re.IGNORECASE | re.DOTALL,
):
    raise SystemExit(
        "PUBLIC_LOGIN_CORRECT_FORGOT_LINK_MISSING"
    )

if re.search(
    r"href:[\"']/reset-password/[\"']"
    r".{0,400}(?:نسيت كلمة المرور|Forgot(?: your)? password)",
    text,
    flags=re.IGNORECASE | re.DOTALL,
):
    raise SystemExit(
        "PUBLIC_LOGIN_WRONG_FORGOT_LINK_REMAINS"
    )

print("PUBLIC_LOGIN_TRUE_BUILD_GATE=PASS")
PY

log "PUBLIC_LOGIN_HTTP=$LOGIN_AFTER_HTTP"
log "PUBLIC_LOGIN_EQUALS_NEW_UI_DIST=YES"
log "PUBLIC_LOGIN_FORGOT_LINK=/forgot-password/"
log "PUBLIC_LOGIN_TRUE_BUILD_GATE=PASS"

section "13) VERIFY PUBLIC RECOVERY PAGES"

FORGOT_PAGE_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H 'Cache-Control: no-cache' \
        -o "$WORK/public-forgot.html" \
        -w '%{http_code}' \
        "https://$DOMAIN/forgot-password/?recovery_v7=$TS"
)"

RESET_PAGE_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H 'Cache-Control: no-cache' \
        -o "$WORK/public-reset.html" \
        -w '%{http_code}' \
        "https://$DOMAIN/reset-password/?token=test&email=test@example.invalid&recovery_v7=$TS"
)"

[[ "$FORGOT_PAGE_HTTP" == "200" ]] ||
    fail "PUBLIC_FORGOT_PAGE_HTTP_$FORGOT_PAGE_HTTP"

[[ "$RESET_PAGE_HTTP" == "200" ]] ||
    fail "PUBLIC_RESET_PAGE_HTTP_$RESET_PAGE_HTTP"

cmp -s "$WORK/public-forgot.html" "$FORGOT_HTML" ||
    fail "PUBLIC_FORGOT_PAGE_NOT_SERVED_FROM_GOVERNED_FILE"

cmp -s "$WORK/public-reset.html" "$RESET_HTML" ||
    fail "PUBLIC_RESET_PAGE_NOT_SERVED_FROM_GOVERNED_FILE"

log "PUBLIC_FORGOT_PAGE_HTTP=$FORGOT_PAGE_HTTP"
log "PUBLIC_RESET_PAGE_HTTP=$RESET_PAGE_HTTP"
log "PORTAL_SHELL_ON_RECOVERY_ROUTES=NO"
log "PUBLIC_RECOVERY_PAGE_GATE=PASS"

section "14) VERIFY SAME-ORIGIN API ROUTES"

FORGOT_API_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H "Origin: https://$DOMAIN" \
        -H "Referer: https://$DOMAIN/forgot-password/" \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        --data "{\"email\":\"ndsp-v7-${TS}@example.invalid\"}" \
        -o "$WORK/public-forgot-api.json" \
        -w '%{http_code}' \
        "https://$DOMAIN/api/auth/forgot-password"
)"

RESET_API_HTTP="$(
    curl -sS \
        --connect-timeout 8 \
        --max-time 30 \
        -H "Origin: https://$DOMAIN" \
        -H "Referer: https://$DOMAIN/reset-password/" \
        -H 'Content-Type: application/json' \
        -H 'Accept: application/json' \
        --data '{
          "token":"invalid-v7-public",
          "email":"ndsp-v7@example.invalid",
          "newPassword":"PublicOnly123!"
        }' \
        -o "$WORK/public-reset-api.json" \
        -w '%{http_code}' \
        "https://$DOMAIN/api/auth/reset-password"
)"

[[ "$FORGOT_API_HTTP" == "200" ]] ||
    fail "PUBLIC_FORGOT_API_HTTP_$FORGOT_API_HTTP"

case "$RESET_API_HTTP" in
    400|401|403|422)
        ;;
    *)
        fail "PUBLIC_RESET_API_HTTP_$RESET_API_HTTP"
        ;;
esac

grep -Eq '^[[:space:]]*\{' "$WORK/public-forgot-api.json" ||
    fail "PUBLIC_FORGOT_API_NON_JSON"

grep -Eq '^[[:space:]]*\{' "$WORK/public-reset-api.json" ||
    fail "PUBLIC_RESET_API_NON_JSON"

log "PUBLIC_FORGOT_API_HTTP=$FORGOT_API_HTTP"
log "PUBLIC_RESET_INVALID_TOKEN_HTTP=$RESET_API_HTTP"
log "FORGOT_REQUEST_REACHED_PASSWORD_RESET_BACKEND=PASS"
log "RESET_REQUEST_REACHED_PASSWORD_RESET_BACKEND=PASS"
log "REQUEST_REMAINED_FRONTEND_ONLY=NO"

section "15) SOURCE AND DEPLOYMENT AUDIT"

grep -Fq \
    'https://my.ndsp.app/reset-password/?token=' \
    "$RESET_SERVER" ||
    fail "CANONICAL_EMAIL_LINK_MISSING"

if grep -Fq \
    '/reset-password.html?token=' \
    "$RESET_SERVER"; then

    fail "LEGACY_EMAIL_LINK_REMAINS"
fi

sudo nginx -T \
    > "$WORK/nginx-effective-after.txt" \
    2>&1

grep -Fq \
    'NDSP_AUTH_RECOVERY_ROUTES_V7_BEGIN' \
    "$WORK/nginx-effective-after.txt" ||
    fail "EFFECTIVE_NGINX_MANAGED_ROUTES_MISSING"

grep -Fq \
    "127.0.0.1:${RESET_PORT}/api/auth/forgot-password" \
    "$WORK/nginx-effective-after.txt" ||
    fail "EFFECTIVE_FORGOT_PROXY_MISSING"

log "AUTH_LOGIN_CHANGED_IN_TRUE_SOURCE=YES"
log "AUTH_UI_REBUILT_FROM_TRUE_SOURCE=YES"
log "DIRECT_UI_DIST_EDIT_USED=NO"
log "AUTH_RELEASE_ATOMIC_CUTOVER=YES"
log "PASSWORD_RESET_BACKEND_SOURCE_CHANGED=YES"
log "NGINX_SOURCE_CHANGED=YES"
log "RUNTIME_PATCH_USED=NO"
log "DATABASE_SCHEMA_CHANGED=NO"
log "DATABASE_DIRECT_EDIT=NO"
log "SOURCE_AND_DEPLOYMENT_AUDIT=PASS"

section "16) FINAL RESULT"

sha256sum \
    "$NEW_AUTH_UI_SOURCE" \
    "$NEW_RELEASE/ui-dist/index.html" \
    "$RESET_SERVER" \
    "$FORGOT_HTML" \
    "$RESET_HTML" \
    "$CANONICAL_RECOVERY/manifest.json" \
    > "$BACKUP/final-sha256-manifest.txt"

while IFS=$'\t' read -r ORIGINAL STAGE COUNT; do
    sha256sum "$ORIGINAL" \
        >> "$BACKUP/final-sha256-manifest.txt"
done < "$NGINX_MANIFEST"

rm -rf "$CANONICAL_OLD" >/dev/null 2>&1 || true

log "FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_DEPLOYED_AND_VERIFIED"
log "ROOT_CAUSE=PUBLIC_LOGIN_WAS_SERVED_FROM_AUTH_CORE_UI_DIST"
log "TRUE_LOGIN_SOURCE=$NEW_AUTH_UI_SOURCE"
log "TRUE_LOGIN_BUILD=$NEW_RELEASE/ui-dist"
log "AUTH_ACTIVE_RELEASE=$NEW_RELEASE"
log "LOGIN_FORGOT_LINK=/forgot-password/"
log "FORGOT_PASSWORD_PAGE=VERIFIED"
log "RESET_PASSWORD_PAGE=VERIFIED"
log "FORGOT_PASSWORD_API_ON_MY_NDSP_APP=VERIFIED"
log "RESET_PASSWORD_API_ON_MY_NDSP_APP=VERIFIED"
log "EMAIL_RESET_LINK=https://my.ndsp.app/reset-password/"
log "REQUESTS_REACHED_BACKEND=YES"
log "PORTAL_SHELL_ON_RECOVERY_ROUTES=NO"
log "DATABASE_SCHEMA_CHANGED=NO"
log "DATABASE_DIRECT_EDIT=NO"
log "BACKUP=$BACKUP"
log "REPORT=$REPORT"

trap - ERR INT TERM

echo
echo "============================================================"
echo "تم إصلاح رحلة استعادة كلمة المرور من المصدر الحقيقي."
echo "افتح من الجوال:"
echo "https://$DOMAIN/forgot-password/?v=$TS"
echo
echo "التقرير:"
echo "$REPORT"
echo
echo "الإصدار النشط:"
echo "$NEW_RELEASE"
echo "============================================================"

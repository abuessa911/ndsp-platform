#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

# ============================================================
# NDSP — Prepare Reset Contract Then Run V7 — V10
#
# The recovered page is valid but calls the legacy endpoint:
#   /ndsp-rp/reset
#
# This script changes only the staged recovery-page source to:
#   /api/auth/reset-password
#
# Then it seeds the missing live file and runs the governed V7.
# V7 remains responsible for the true auth build, backend link,
# Nginx routes, service restarts, verification and rollback.
# ============================================================

CONFIRM="${NDSP_CONFIRM_PREPARE_RESET_AND_RUN_V7_V10:-NO}"

PROJECT="${NDSP_PROJECT:-$HOME/empire-core-new}"
WEB_ROOT="${NDSP_WEB_ROOT:-/var/www/ndsp-my}"

FORGOT_HTML="${NDSP_FORGOT_HTML:-$WEB_ROOT/forgot-password.html}"
RESET_HTML="${NDSP_RESET_HTML:-$WEB_ROOT/reset-password.html}"
RECOVERED_RESET="${NDSP_RECOVERED_RESET_SOURCE:-/var/www/html/reset-password.html}"

CANONICAL_DIR="${NDSP_CANONICAL_RECOVERY:-$PROJECT/frontend/auth-recovery}"
V7_SCRIPT="${NDSP_V7_SCRIPT:-$HOME/ndsp_auth_recovery_true_source_fix_v7.sh}"

EXPECTED_RECOVERED_SHA="a4c7e7ecb8dd0e3cca396f042657f8ec51b90fac0a45d6f6b5f85ff28034b90a"
EXPECTED_V7_SHA="c68b09d0570d64ea039144094154e12ab24976805e9fffa4117251cf5c7df82d"

TS="$(date +%Y%m%d_%H%M%S)"
WORK="$(mktemp -d /tmp/ndsp-reset-v10.XXXXXX)"
PATCHED_RESET="$WORK/reset-password.html"
CANONICAL_STAGE="$WORK/auth-recovery"

BACKUP="$PROJECT/backups/prepare-reset-contract-v10/$TS"
REPORT="$PROJECT/docs/05-runbooks/NDSP_PREPARE_RESET_CONTRACT_V10_${TS}.md"
V7_OUTPUT="$BACKUP/v7-output.log"

CANONICAL_EXISTED=0
RESET_EXISTED=0
CANONICAL_INSTALLED=0
RESET_INSTALLED=0
SUDO_KEEPALIVE_PID=""

mkdir -p "$CANONICAL_STAGE" "$BACKUP" "$(dirname "$REPORT")"
chmod 700 "$BACKUP"
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
    log "WRAPPER_ROLLBACK_REQUIRED=YES"
    log "WRAPPER_ROLLBACK_TRIGGER_EXIT=$rc"

    if [[ "$RESET_INSTALLED" == "1" ]]; then
        if [[ "$RESET_EXISTED" == "1" ]] &&
           [[ -f "$BACKUP/reset-password.before.html" ]]; then

            sudo cp -a \
                "$BACKUP/reset-password.before.html" \
                "$RESET_HTML" || true

            log "RESET_PAGE_RESTORED=YES"
        else
            sudo rm -f "$RESET_HTML" || true
            log "SEEDED_RESET_PAGE_REMOVED=YES"
        fi
    fi

    if [[ "$CANONICAL_INSTALLED" == "1" ]]; then
        rm -rf "$CANONICAL_DIR" || true

        if [[ "$CANONICAL_EXISTED" == "1" ]] &&
           [[ -f "$BACKUP/canonical.before.tar.gz" ]]; then

            tar \
                -C "$(dirname "$CANONICAL_DIR")" \
                -xzf "$BACKUP/canonical.before.tar.gz" || true

            log "CANONICAL_SOURCE_RESTORED=YES"
        else
            log "SEEDED_CANONICAL_SOURCE_REMOVED=YES"
        fi
    fi

    log "DATABASE_SCHEMA_CHANGED=NO"
    log "DATABASE_DIRECT_EDIT=NO"
    log "FINAL_STATUS=NDSP_PREPARE_RESET_CONTRACT_V10_FAILED"
    log "REPORT=$REPORT"

    exit "$rc"
}

trap cleanup EXIT
trap rollback ERR INT TERM

section "NDSP — PREPARE RESET CONTRACT THEN RUN V7 — V10"

log "DATE=$(date -Is)"
log "PROJECT=$PROJECT"
log "FORGOT_HTML=$FORGOT_HTML"
log "RECOVERED_RESET=$RECOVERED_RESET"
log "RESET_HTML=$RESET_HTML"
log "CANONICAL_DIR=$CANONICAL_DIR"
log "V7_SCRIPT=$V7_SCRIPT"
log "BACKUP=$BACKUP"
log "REPORT=$REPORT"

section "0) EXPLICIT CONFIRMATION AND PRIVILEGES"

[[ "$CONFIRM" == "YES" ]] ||
    fail "SET_NDSP_CONFIRM_PREPARE_RESET_AND_RUN_V7_V10=YES"

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

section "1) VERIFY INPUT SOURCES"

for command_name in \
    bash python3 node grep sha256sum stat install \
    tar rsync cmp awk sudo; do

    command -v "$command_name" >/dev/null 2>&1 ||
        fail "MISSING_COMMAND:$command_name"
done

[[ -f "$FORGOT_HTML" ]] ||
    fail "FORGOT_PAGE_MISSING:$FORGOT_HTML"

[[ -f "$RECOVERED_RESET" ]] ||
    fail "RECOVERED_RESET_MISSING:$RECOVERED_RESET"

[[ -f "$V7_SCRIPT" ]] ||
    fail "V7_SCRIPT_MISSING:$V7_SCRIPT"

RECOVERED_SHA="$(sha256sum "$RECOVERED_RESET" | awk '{print $1}')"
V7_SHA="$(sha256sum "$V7_SCRIPT" | awk '{print $1}')"

[[ "$RECOVERED_SHA" == "$EXPECTED_RECOVERED_SHA" ]] ||
    fail "RECOVERED_RESET_SHA_MISMATCH:$RECOVERED_SHA"

[[ "$V7_SHA" == "$EXPECTED_V7_SHA" ]] ||
    fail "V7_SHA_MISMATCH:$V7_SHA"

bash -n "$V7_SCRIPT"

grep -Fq '/api/auth/forgot-password' "$FORGOT_HTML" ||
    fail "CURRENT_FORGOT_PAGE_DOES_NOT_USE_CANONICAL_API"

if grep -Eqi \
    'Executive|مركز القيادة|غرفة القرار|مستكشف الفرص' \
    "$FORGOT_HTML" "$RECOVERED_RESET"; then

    fail "RECOVERY_SOURCE_CONTAINS_PORTAL_SHELL"
fi

log "RECOVERED_RESET_SHA256=$RECOVERED_SHA"
log "V7_SHA256=$V7_SHA"
log "FORGOT_PAGE_CANONICAL_API_GATE=PASS"
log "INPUT_SOURCE_GATE=PASS"

section "2) PATCH RECOVERED RESET PAGE IN STAGE"

cp -a "$RECOVERED_RESET" "$PATCHED_RESET"

python3 - "$PATCHED_RESET" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="strict")

legacy = "/ndsp-rp/reset"
canonical = "/api/auth/reset-password"

count = text.count(legacy)

if count != 1:
    raise SystemExit(
        f"EXPECTED_ONE_LEGACY_RESET_ENDPOINT_FOUND={count}"
    )

text = text.replace(legacy, canonical)

if legacy in text:
    raise SystemExit("LEGACY_RESET_ENDPOINT_REMAINS")

if canonical not in text:
    raise SystemExit("CANONICAL_RESET_ENDPOINT_MISSING")

if "newPassword" not in text:
    raise SystemExit("NEW_PASSWORD_FIELD_MISSING")

if "URLSearchParams" not in text or "token" not in text:
    raise SystemExit("RESET_TOKEN_QUERY_CONTRACT_MISSING")

marker = "<!-- NDSP_RESET_CONTRACT_V10 -->"
if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)

path.write_text(text, encoding="utf-8")

print("RESET_ENDPOINT_REPLACEMENT_COUNT=1")
print("RESET_API=/api/auth/reset-password")
PY

grep -Fq '/api/auth/reset-password' "$PATCHED_RESET" ||
    fail "PATCHED_RESET_CANONICAL_API_MISSING"

if grep -Fq '/ndsp-rp/reset' "$PATCHED_RESET"; then
    fail "PATCHED_RESET_LEGACY_API_REMAINS"
fi

python3 - "$PATCHED_RESET" "$WORK/inline.js" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
import sys

source = Path(sys.argv[1])
target = Path(sys.argv[2])

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside = False
        self.parts = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script" and not dict(attrs).get("src"):
            self.inside = True
            self.parts = []

    def handle_data(self, data):
        if self.inside:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.inside:
            self.scripts.append("".join(self.parts))
            self.inside = False
            self.parts = []

parser = Parser()
parser.feed(source.read_text(encoding="utf-8", errors="strict"))

if len(parser.scripts) != 1:
    raise SystemExit(
        f"EXPECTED_ONE_INLINE_SCRIPT_FOUND={len(parser.scripts)}"
    )

target.write_text(parser.scripts[0], encoding="utf-8")
PY

node --check "$WORK/inline.js"

log "PATCHED_RESET_SOURCE_GATE=PASS"
log "PATCHED_RESET_JAVASCRIPT_GATE=PASS"

section "3) BACKUP CURRENT PRE-SEED STATE"

if [[ -d "$CANONICAL_DIR" ]]; then
    CANONICAL_EXISTED=1

    tar \
        -C "$(dirname "$CANONICAL_DIR")" \
        -czf "$BACKUP/canonical.before.tar.gz" \
        "$(basename "$CANONICAL_DIR")"
fi

if [[ -f "$RESET_HTML" ]]; then
    RESET_EXISTED=1
    sudo cp -a "$RESET_HTML" "$BACKUP/reset-password.before.html"
fi

sudo chown -R "$(id -u):$(id -g)" "$BACKUP"

log "CANONICAL_EXISTED=$CANONICAL_EXISTED"
log "RESET_LIVE_EXISTED=$RESET_EXISTED"
log "BACKUP_GATE=PASS"

section "4) INSTALL CANONICAL RECOVERY SOURCE"

cp -a "$FORGOT_HTML" "$CANONICAL_STAGE/forgot-password.html"
cp -a "$PATCHED_RESET" "$CANONICAL_STAGE/reset-password.html"

cat > "$CANONICAL_STAGE/manifest.json" <<JSON
{
  "version": "10.0.0-pre-v7",
  "generated_at": "$(date -Is)",
  "forgot_api": "/api/auth/forgot-password",
  "reset_api": "/api/auth/reset-password",
  "recovered_reset_source": "$RECOVERED_RESET",
  "recovered_reset_sha256": "$RECOVERED_SHA",
  "legacy_reset_endpoint_removed": true,
  "database_change": false,
  "runtime_patch": false
}
JSON

CANONICAL_PARENT="$(dirname "$CANONICAL_DIR")"
CANONICAL_NAME="$(basename "$CANONICAL_DIR")"
CANONICAL_TEMP="$CANONICAL_PARENT/.${CANONICAL_NAME}.v10-stage-$TS"
CANONICAL_OLD="$CANONICAL_PARENT/.${CANONICAL_NAME}.v10-old-$TS"

mkdir -p "$CANONICAL_PARENT"
rm -rf "$CANONICAL_TEMP" "$CANONICAL_OLD"
rsync -a --delete "$CANONICAL_STAGE/" "$CANONICAL_TEMP/"

if [[ -d "$CANONICAL_DIR" ]]; then
    mv "$CANONICAL_DIR" "$CANONICAL_OLD"
fi

mv "$CANONICAL_TEMP" "$CANONICAL_DIR"
CANONICAL_INSTALLED=1
rm -rf "$CANONICAL_OLD"

log "CANONICAL_SOURCE_INSTALLED=YES"
log "CANONICAL_SOURCE=$CANONICAL_DIR"

section "5) SEED MISSING LIVE RESET FILE"

WEB_UID="$(stat -c '%u' "$FORGOT_HTML")"
WEB_GID="$(stat -c '%g' "$FORGOT_HTML")"
WEB_MODE="$(stat -c '%a' "$FORGOT_HTML")"
RESET_TEMP="$WEB_ROOT/.reset-password.v10-$TS.html"

sudo install \
    -o "$WEB_UID" \
    -g "$WEB_GID" \
    -m "$WEB_MODE" \
    "$CANONICAL_DIR/reset-password.html" \
    "$RESET_TEMP"

sudo mv -f "$RESET_TEMP" "$RESET_HTML"
RESET_INSTALLED=1

cmp -s "$CANONICAL_DIR/reset-password.html" "$RESET_HTML" ||
    fail "LIVE_RESET_DIFFERS_FROM_CANONICAL_SOURCE"

log "LIVE_RESET_SEED=PASS"

section "6) RUN GOVERNED TRUE-SOURCE V7"

set +e

NDSP_CONFIRM_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7=YES \
bash "$V7_SCRIPT" 2>&1 | tee "$V7_OUTPUT"

V7_RC="${PIPESTATUS[0]}"
set -e

cat "$V7_OUTPUT" >> "$REPORT"

[[ "$V7_RC" == "0" ]] ||
    fail "V7_EXECUTION_FAILED_EXIT_$V7_RC"

grep -Fq \
    'FINAL_STATUS=NDSP_AUTH_RECOVERY_TRUE_SOURCE_FIX_V7_DEPLOYED_AND_VERIFIED' \
    "$V7_OUTPUT" ||
    fail "V7_SUCCESS_STATUS_MISSING"

section "7) FINAL RESULT"

log "FINAL_STATUS=NDSP_PREPARE_RESET_CONTRACT_V10_AND_V7_COMPLETED"
log "V7_FINAL_STATUS=DEPLOYED_AND_VERIFIED"
log "FORGOT_API=/api/auth/forgot-password"
log "RESET_API=/api/auth/reset-password"
log "LEGACY_RESET_ENDPOINT=/ndsp-rp/reset REMOVED"
log "CANONICAL_SOURCE=$CANONICAL_DIR"
log "DATABASE_SCHEMA_CHANGED=NO"
log "DATABASE_DIRECT_EDIT=NO"
log "RUNTIME_PATCH_USED=NO"
log "BACKUP=$BACKUP"
log "REPORT=$REPORT"

trap - ERR INT TERM

echo
echo "============================================================"
echo "تم تصحيح عقد صفحة إعادة كلمة المرور وتشغيل V7."
echo "افتح:"
echo "https://my.ndsp.app/forgot-password/"
echo "التقرير:"
echo "$REPORT"
echo "============================================================"

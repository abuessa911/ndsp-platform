#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

PROJECT_DIR="/home/nawaf511/empire-core-new"
OUT_BASE="/home/nawaf511/ndsp_full_backups_v2"
PASSPHRASE_FILE=""
WARNINGS=0
FAILURES=0

usage() {
  echo "Usage: ndsp_backup_runtime_precheck_v1.sh --passphrase-file PATH [--project-dir PATH] [--output-dir PATH]"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --passphrase-file) PASSPHRASE_FILE="${2:-}"; shift 2 ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --output-dir) OUT_BASE="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

ok() { echo "[OK] $*"; }
warn() { WARNINGS=$((WARNINGS+1)); echo "[WARN] $*"; }
fail() { FAILURES=$((FAILURES+1)); echo "[FAIL] $*"; }

[ -n "$PASSPHRASE_FILE" ] || { echo "ERROR: --passphrase-file is required." >&2; exit 2; }

for tool in tar gzip sha256sum find stat du df flock gpg openssl python3 sudo; do
  if command -v "$tool" >/dev/null 2>&1; then ok "tool $tool"; else fail "missing tool $tool"; fi
done

if [ -d "$PROJECT_DIR" ]; then ok "project exists: $PROJECT_DIR"; else fail "project missing: $PROJECT_DIR"; fi
if [ -s "$PASSPHRASE_FILE" ]; then
  mode="$(stat -c '%a' "$PASSPHRASE_FILE" 2>/dev/null || true)"
  case "$mode" in 600|400) ok "passphrase file mode=$mode" ;; *) fail "passphrase file mode must be 600 or 400; actual=$mode" ;; esac
else
  fail "passphrase file missing or empty"
fi

PASS_REAL="$(realpath -m "$PASSPHRASE_FILE")"
PROJECT_REAL="$(realpath -m "$PROJECT_DIR")"
OUT_REAL="$(realpath -m "$OUT_BASE")"
case "$PASS_REAL" in
  "$PROJECT_REAL"|"$PROJECT_REAL"/*|"$OUT_REAL"|"$OUT_REAL"/*) fail "passphrase file is inside protected backup scope" ;;
  *) ok "passphrase file is outside project and output directory" ;;
esac

if sudo -n true 2>/dev/null; then ok "passwordless sudo"; else fail "passwordless sudo unavailable"; fi
mkdir -p "$OUT_BASE"
FREE_KB="$(df -Pk "$OUT_BASE" | awk 'NR==2 {print $4}')"
PROJECT_KB="$(du -sk "$PROJECT_DIR" 2>/dev/null | awk '{print $1}')"
REQUIRED=$((PROJECT_KB * 4 + 5 * 1024 * 1024))
if [ "$FREE_KB" -ge "$REQUIRED" ]; then ok "capacity free_kb=$FREE_KB required_estimate_kb=$REQUIRED"; else fail "insufficient capacity free_kb=$FREE_KB required_estimate_kb=$REQUIRED"; fi

if sudo nginx -t >/dev/null 2>&1; then ok "nginx configuration test"; else warn "nginx configuration test failed"; fi
if command -v pm2 >/dev/null 2>&1; then pm2 status >/dev/null 2>&1 && ok "PM2 reachable" || warn "PM2 command returned nonzero"; else warn "PM2 not installed"; fi

if command -v psql >/dev/null 2>&1 && sudo -n -u postgres psql -XAtqc 'SELECT 1' postgres >/dev/null 2>&1; then
  ok "local PostgreSQL logical access"
else
  warn "local PostgreSQL logical access unavailable; backup would continue with a warning"
fi

if command -v docker >/dev/null 2>&1; then
  if sudo -n docker ps >/dev/null 2>&1; then
    ok "Docker reachable"
    mapfile -t PG_CONTAINERS < <(sudo -n docker ps --format '{{.Names}}\t{{.Image}}' | awk 'tolower($2) ~ /(postgres|timescale)/ {print $1}')
    if [ "${#PG_CONTAINERS[@]}" -eq 0 ]; then warn "no running Docker PostgreSQL container discovered"; fi
    for c in "${PG_CONTAINERS[@]}"; do
      if sudo -n docker exec "$c" sh -lc 'u="${POSTGRES_USER:-postgres}"; d="${POSTGRES_DB:-postgres}"; export PGPASSWORD="${POSTGRES_PASSWORD:-}"; psql -U "$u" -d "$d" -XAtqc "SELECT 1"' >/dev/null 2>&1; then
        ok "Docker PostgreSQL logical access: $c"
      else
        warn "Docker PostgreSQL authentication unavailable: $c"
      fi
    done
  else
    warn "Docker command unavailable through sudo"
  fi
else
  warn "Docker not installed"
fi

if command -v redis-cli >/dev/null 2>&1 && redis-cli -h 127.0.0.1 -p 6379 PING 2>/dev/null | grep -qx PONG; then
  ok "Redis reachable"
else
  warn "Redis unavailable or authenticated"
fi

TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT
printf test > "$TEST_DIR/plain"
if gpg --batch --yes --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --symmetric --cipher-algo AES256 --output "$TEST_DIR/plain.gpg" "$TEST_DIR/plain" >/dev/null 2>&1 \
   && gpg --batch --quiet --pinentry-mode loopback --passphrase-file "$PASSPHRASE_FILE" --decrypt "$TEST_DIR/plain.gpg" 2>/dev/null | grep -qx test; then
  ok "GPG encrypt/decrypt test"
else
  fail "GPG encrypt/decrypt test failed"
fi

if [ "$FAILURES" -gt 0 ]; then
  echo "WARNINGS=$WARNINGS"
  echo "FAILURES=$FAILURES"
  echo "FINAL_STATUS=NDSP_BACKUP_RUNTIME_PRECHECK_FAILED"
  exit 1
fi

echo "WARNINGS=$WARNINGS"
echo "FAILURES=0"
echo "PRODUCTION_CHANGES=NONE"
echo "FINAL_STATUS=NDSP_BACKUP_RUNTIME_PRECHECK_OK"

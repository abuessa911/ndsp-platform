#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="${1:-/home/nawaf511/empire-core-new}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${ROOT}/var/audits"
OUT="${OUT_DIR}/legacy-path-inventory-${STAMP}.txt"

mkdir -p "$OUT_DIR"

PATTERN='/opt/empire-core|/root/empire-core|/var/www'

exec > >(tee "$OUT") 2>&1

echo "UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Canonical root: $ROOT"
echo

echo "=== Project references ==="

if command -v rg >/dev/null 2>&1; then
  rg -n \
    --hidden \
    -g '!**/.git/**' \
    -g '!**/.env*' \
    -g '!**/node_modules/**' \
    -g '!**/.venv/**' \
    -g '!**/var/handoff/**' \
    "$PATTERN" \
    "$ROOT" 2>/dev/null || true
else
  grep -RInE \
    --exclude='.env' \
    --exclude='.env.*' \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude-dir=.venv \
    --exclude-dir=handoff \
    "$PATTERN" \
    "$ROOT" 2>/dev/null || true
fi

echo
echo "=== Nginx references ==="
grep -RInE "$PATTERN" /etc/nginx 2>/dev/null || true

echo
echo "=== systemd references ==="
grep -RInE "$PATTERN" \
  /etc/systemd/system \
  /lib/systemd/system \
  /usr/lib/systemd/system \
  2>/dev/null || true

echo
echo "=== Cron references ==="
grep -RInE "$PATTERN" \
  /etc/cron.d \
  /etc/cron.daily \
  /etc/cron.hourly \
  /etc/cron.weekly \
  2>/dev/null || true

echo
echo "=== Running processes ==="
ps -eo pid,user,args | grep -E "$PATTERN" | grep -v grep || true

echo
echo "Inventory saved to: $OUT"

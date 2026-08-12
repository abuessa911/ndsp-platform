#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="${1:-/home/nawaf511/empire-core-new}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${ROOT}/var/migration-plans"
OUT="${OUT_DIR}/path-migration-plan-${STAMP}.txt"

mkdir -p "$OUT_DIR"

exec > >(tee "$OUT") 2>&1

echo "PATH MIGRATION PLAN — DRY RUN ONLY"
echo "UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Canonical root: $ROOT"
echo
echo "No file will be modified."
echo

echo "=== systemd candidates ==="
grep -RIlE \
  '/opt/empire-core|/root/empire-core|/var/www' \
  /etc/systemd/system \
  2>/dev/null || true

echo
echo "=== Nginx candidates ==="
grep -RIlE \
  '/opt/empire-core|/root/empire-core|/var/www' \
  /etc/nginx \
  2>/dev/null || true

echo
echo "=== Required procedure for every candidate ==="
echo "1. Identify service or route owner."
echo "2. Confirm replacement exists under canonical root."
echo "3. Back up original file with UTC timestamp."
echo "4. Produce and review a diff."
echo "5. Validate systemd or Nginx syntax."
echo "6. Restart one unit or reload one configuration at a time."
echo "7. Run health checks."
echo "8. Keep rollback copy."
echo
echo "Plan saved to: $OUT"

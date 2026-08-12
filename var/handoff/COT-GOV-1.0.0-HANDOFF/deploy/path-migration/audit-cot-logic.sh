#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="${1:-/home/nawaf511/empire-core-new}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${ROOT}/var/audits"
OUT="${OUT_DIR}/cot-backend-audit-${STAMP}.txt"

mkdir -p "$OUT_DIR"
cd "$ROOT"

exec > >(tee "$OUT") 2>&1

echo "============================================================"
echo "COT BACKEND AUDIT"
echo "============================================================"
echo "UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Root: $ROOT"
echo

echo "=== Git baseline ==="
git status --short 2>/dev/null || true
git branch --show-current 2>/dev/null || true
git rev-parse HEAD 2>/dev/null || true
echo

echo "=== Governance service files ==="
find backend/services/decision_governance_core \
  -maxdepth 7 -type f \
  ! -name '.env' \
  ! -name '.env.*' \
  ! -path '*/node_modules/*' \
  -print 2>/dev/null | sort
echo

echo "=== Raw COT gateway files ==="
find apps/ndsp-raw-cot-gateway \
  -maxdepth 6 -type f \
  ! -name '.env' \
  ! -name '.env.*' \
  ! -path '*/.venv/*' \
  ! -path '*/__pycache__/*' \
  -print 2>/dev/null | sort
echo

PATTERN='TDL[-_ ]?M(&|AND)L|TDL[-_ ]?S|day.?control|controller|asset.?manager|leveraged.?fund|other.?reportable|dealer|positions|changes|dominance|delta|bullish|bearish|direction|trend|timezone|UTC|week.?start|effective.?week|report.?activation'

echo "=== Direction and timing references ==="

if command -v rg >/dev/null 2>&1; then
  rg -n -i \
    --hidden \
    -g '!**/.env*' \
    -g '!**/node_modules/**' \
    -g '!**/.venv/**' \
    -g '!**/dist/**' \
    -g '!**/build/**' \
    "$PATTERN" \
    backend apps 2>/dev/null || true
else
  grep -RInE \
    --exclude='.env' \
    --exclude='.env.*' \
    --exclude='*.key' \
    --exclude='*.pem' \
    --exclude-dir=node_modules \
    --exclude-dir=.venv \
    --exclude-dir=dist \
    --exclude-dir=build \
    "$PATTERN" \
    backend apps 2>/dev/null || true
fi

echo
echo "=== Relevant systemd units ==="

for UNIT in \
  ndsp-decision-governance-core.service \
  ndsp-decision_governance_core.service \
  ndsp-raw-cot-gateway.service
do
  echo "--- $UNIT ---"
  systemctl cat "$UNIT" 2>/dev/null || true
done

echo
echo "=== Relevant Nginx references ==="

grep -RInE \
  'decision-governance|governance/evaluate|raw-cot|9076|9079' \
  /etc/nginx 2>/dev/null || true

echo
echo "Audit saved to: $OUT"

#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RETIRED_AR="$(printf '\u0646\u0648\u0627\u0641')"
RETIRED_EN="$(printf '\x6e\x61\x77\x61\x66')"
PATTERN="${RETIRED_AR}|${RETIRED_EN}"

echo "[1/6] Checking visible source for retired brand name..."
if grep -RniEi --exclude-dir=node_modules --exclude-dir=dist --exclude='*.log' "$PATTERN" .; then
  echo "ERROR: retired brand name is still present." >&2
  exit 1
fi

echo "[2/6] Checking legacy logo asset..."
if [[ -e public/assets/ndsp-logo-lockup.png ]]; then
  echo "ERROR: legacy logo lockup still exists." >&2
  exit 1
fi
test -f public/assets/ndsp-mark.png

echo "[3/6] Installing locked dependencies..."
npm ci --no-audit --no-fund

echo "[4/6] Type checking..."
npm run typecheck

echo "[5/6] Building..."
npm run build

echo "[6/6] Running Sites worker tests and scanning built output..."
npm run test:sites
if grep -RniEi --exclude='*.map' "$PATTERN" dist; then
  echo "ERROR: retired brand name leaked into built output." >&2
  exit 1
fi

echo "Verification completed successfully."

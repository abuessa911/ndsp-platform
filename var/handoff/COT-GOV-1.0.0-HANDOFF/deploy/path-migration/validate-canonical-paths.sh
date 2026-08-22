#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="${1:-/home/nawaf511/empire-core-new}"
MODE="${2:-REPORT_ONLY}"
PATTERN='/opt/empire-core|/root/empire-core|/var/www/(ndsp|ndsp-my|ndsp-admin|ndsp-public-gateway)'

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

grep -RInE \
  --exclude='.env' \
  --exclude='.env.*' \
  --exclude-dir=.git \
  --exclude-dir=node_modules \
  --exclude-dir=.venv \
  --exclude-dir=handoff \
  "$PATTERN" \
  "$ROOT" \
  /etc/nginx \
  /etc/systemd/system \
  2>/dev/null > "$TMP" || true

if [[ -s "$TMP" ]]; then
  echo "Legacy project path references found:"
  cat "$TMP"

  if [[ "$MODE" == "ENFORCE" ]]; then
    exit 1
  fi

  exit 0
fi

echo "No forbidden project path references found."

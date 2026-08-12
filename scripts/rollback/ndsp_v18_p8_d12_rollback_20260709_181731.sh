#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new"
BACKUP_DIR="$ROOT/backups/NDSP_V18_P8_D12_20260709_181731"

cp -f "$BACKUP_DIR/main.jsx.before" "$ROOT/frontend/user-portal-vite/src/main.jsx"
cp -f "$BACKUP_DIR/styles.css.before" "$ROOT/frontend/user-portal-vite/src/styles.css"

echo "ROLLBACK_OK=1"

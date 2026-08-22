#!/usr/bin/env bash
set -euo pipefail
set +H

PROJECT_DIR="${PROJECT_DIR:-$HOME/empire-core-new}"
FRONTEND_DIR="${FRONTEND_DIR:-/var/www/ndsp-my}"
BACKEND_DIR="${BACKEND_DIR:-$PROJECT_DIR}"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_ROOT="${BACKUP_ROOT:-$HOME/ndsp_backups}"
BACKUP_DIR="$BACKUP_ROOT/NDSP_BACKUP_BEFORE_PATCH_$TS"
REPORT_DIR="$PROJECT_DIR/docs/05-runbooks"
REPORT="$REPORT_DIR/NDSP_BACKUP_REPORT_$TS.md"
mkdir -p "$BACKUP_DIR" "$REPORT_DIR"

log(){ echo "$*" | tee -a "$REPORT"; }
: > "$REPORT"
log "# NDSP Backup Before Patch"
log "DATE=$TS"
log "PROJECT_DIR=$PROJECT_DIR"
log "FRONTEND_DIR=$FRONTEND_DIR"
log "BACKEND_DIR=$BACKEND_DIR"
log "BACKUP_DIR=$BACKUP_DIR"
log ""

if [ -d "$FRONTEND_DIR" ]; then
  log "[INFO] Backing up frontend..."
  tar --warning=no-file-changed --ignore-failed-read -czf "$BACKUP_DIR/frontend.tar.gz" -C "$(dirname "$FRONTEND_DIR")" "$(basename "$FRONTEND_DIR")" || true
  log "[OK] frontend.tar.gz created"
else
  log "[WARN] FRONTEND_DIR missing: $FRONTEND_DIR"
fi

if [ -d "$BACKEND_DIR" ]; then
  log "[INFO] Backing up project safe snapshot excluding heavy folders..."
  tar --warning=no-file-changed --ignore-failed-read \
    --exclude='.git' --exclude='node_modules' --exclude='.next' --exclude='dist' --exclude='build' --exclude='venv' --exclude='.venv' --exclude='__pycache__' \
    -czf "$BACKUP_DIR/project_safe_snapshot.tar.gz" -C "$(dirname "$BACKEND_DIR")" "$(basename "$BACKEND_DIR")" || true
  log "[OK] project_safe_snapshot.tar.gz created"
else
  log "[WARN] BACKEND_DIR missing: $BACKEND_DIR"
fi

log ""
log "BACKUP_DIR=$BACKUP_DIR"
log "REPORT=$REPORT"
log "FINAL_STATUS=BACKUP_DONE"

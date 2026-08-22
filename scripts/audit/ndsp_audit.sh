#!/usr/bin/env bash
set -euo pipefail
set +H

# ==========================================================
# NDSP System Audit Script
# الغرض: فحص سلامة المجلدات، حالة الخدمات، والبحث عن كلمات محظورة
# المسار المقترح:
# /home/nawaf511/empire-core-v5-1-1-clean/scripts/audit/ndsp_audit.sh
# ==========================================================

PROJECT_DIR="/home/nawaf511/empire-core-v5-1-1-clean"
REPORT_DIR="$PROJECT_DIR/docs/05-runbooks"
REPORT_FILE="$REPORT_DIR/NDSP_AUDIT_REPORT_$(date +%Y%m%d_%H%M%S).md"

mkdir -p "$REPORT_DIR"

log() {
  echo "$*" | tee -a "$REPORT_FILE"
}

log "=== NDSP SYSTEM AUDIT STARTING ==="
log "Date: $(date)"
log "Project: $PROJECT_DIR"
log "Report: $REPORT_FILE"
log ""

# ==========================================================
# 1. التحقق من سلامة المجلدات
# ==========================================================

log "--- [1/4] Directory Integrity ---"

REQUIRED_DIRS=(
  "docs/00-build-catalog"
  "docs/01-build-control-pack"
  "scripts/audit"
  "scripts/backup"
  "docs/05-runbooks"
  "docs/06-decision-room-contracts"
)

for dir in "${REQUIRED_DIRS[@]}"; do
  if [ -d "$PROJECT_DIR/$dir" ]; then
    log "[OK] Found: $dir"
  else
    log "[MISSING] Required directory not found: $dir"
  fi
done

log ""

# ==========================================================
# 2. التحقق من حالة الخدمات
# ==========================================================

log "--- [2/4] Service Status ---"

if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet nginx; then
    log "[OK] Nginx is running."
  else
    log "[ALERT] Nginx is NOT running."
  fi
else
  log "[WARN] systemctl command not found."
fi

if command -v pm2 >/dev/null 2>&1; then
  if pm2 describe ndsp-core-runtime >/dev/null 2>&1; then
    log "[OK] PM2 runtime found: ndsp-core-runtime"
  else
    log "[ALERT] PM2 runtime not found or stopped: ndsp-core-runtime"
  fi
else
  log "[WARN] pm2 command not found."
fi

log ""

# ==========================================================
# 3. فحص المصطلحات المحظورة
# ==========================================================

log "--- [3/4] Content Safety Audit ---"

FORBIDDEN=(
  "Buy Now"
  "Sell Now"
  "اشتر الآن"
  "بيع الآن"
  "بيّع"
  "توصية"
  "ربح مضمون"
  "اربح مضمون"
  "دخول الآن"
  "صفقة مضمونة"
)

SEARCH_EXCLUDES=(
  --exclude-dir=".git"
  --exclude-dir="node_modules"
  --exclude-dir="dist"
  --exclude-dir="build"
  --exclude-dir=".next"
  --exclude-dir="venv"
  --exclude-dir=".venv"
  --exclude-dir="__pycache__"
  --exclude-dir="docs"
  --exclude-dir="scripts"
  --exclude="*.png"
  --exclude="*.jpg"
  --exclude="*.jpeg"
  --exclude="*.gif"
  --exclude="*.webp"
  --exclude="*.pdf"
  --exclude="*.zip"
  --exclude="*.tar"
  --exclude="*.gz"
)

for word in "${FORBIDDEN[@]}"; do
  if grep -RIn --binary-files=without-match "${SEARCH_EXCLUDES[@]}" -- "$word" "$PROJECT_DIR" >/tmp/ndsp_audit_grep_result.txt 2>/dev/null; then
    log "[DANGER] Found forbidden term: '$word'"
    head -n 10 /tmp/ndsp_audit_grep_result.txt | while IFS= read -r line; do
      log "  - $line"
    done
  else
    log "[OK] No forbidden term: '$word'"
  fi
done

rm -f /tmp/ndsp_audit_grep_result.txt

log ""

# ==========================================================
# 4. ملخص نهائي
# ==========================================================

log "--- [4/4] Final Summary ---"
log "Audit completed."
log "Report saved to: $REPORT_FILE"
log ""
log "=== AUDIT COMPLETE ==="

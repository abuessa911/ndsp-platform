#!/usr/bin/env bash
set -u
set +H

PROJECT_DIR="${PROJECT_DIR:-$HOME/empire-core-new}"
FRONTEND_DIR="${FRONTEND_DIR:-/var/www/ndsp-my}"
BACKEND_DIR="${BACKEND_DIR:-$PROJECT_DIR}"
FRONTEND_BASE="${FRONTEND_BASE:-https://my.ndsp.app}"
API_BASE="${API_BASE:-https://api.ndsp.app}"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_DIR/docs/05-runbooks"
REPORT="$REPORT_DIR/NDSP_AUDIT_REPORT_$TS.md"
mkdir -p "$REPORT_DIR"

log(){ echo "$*" | tee -a "$REPORT"; }
status(){ if [ "$1" -eq 0 ]; then echo "OK"; else echo "ALERT"; fi; }
http_code(){ curl -k -L -s -o /dev/null -w "%{http_code}" --max-time 12 "$1" 2>/dev/null || echo "000"; }

: > "$REPORT"
log "# NDSP Audit Report"
log ""
log "DATE=$TS"
log "PROJECT_DIR=$PROJECT_DIR"
log "FRONTEND_DIR=$FRONTEND_DIR"
log "BACKEND_DIR=$BACKEND_DIR"
log "FRONTEND_BASE=$FRONTEND_BASE"
log "API_BASE=$API_BASE"
log ""

log "## 1) Directory Integrity"
for p in \
  "$PROJECT_DIR/docs/00-build-catalog" \
  "$PROJECT_DIR/docs/01-build-control-pack" \
  "$PROJECT_DIR/docs/02-execution-ready-pack" \
  "$PROJECT_DIR/docs/03-final-transition" \
  "$PROJECT_DIR/docs/04-legal" \
  "$PROJECT_DIR/docs/05-runbooks" \
  "$PROJECT_DIR/docs/06-decision-room-contracts" \
  "$PROJECT_DIR/scripts/audit" \
  "$PROJECT_DIR/scripts/backup" \
  "$PROJECT_DIR/scripts/tests"; do
  if [ -d "$p" ]; then log "[OK] Found: $p"; else log "[ALERT] Missing: $p"; fi
done
log ""

log "## 2) Official Frontend Files"
for f in index.html decision-support.html NDSP_Asset_View.html NDSP_Command_Center.html NDSP_Daily_Brief.html NDSP_Settings_Alerts.html login.html register.html disclaimer.html admin.html; do
  if [ -f "$FRONTEND_DIR/$f" ]; then log "[OK] $f"; else log "[WARN] Missing or not static: $f"; fi
done
log ""

log "## 3) HTTP Page Checks"
for route in / /index.html /decision-support.html /NDSP_Asset_View.html /NDSP_Command_Center.html /NDSP_Daily_Brief.html /NDSP_Settings_Alerts.html; do
  code="$(http_code "$FRONTEND_BASE$route")"
  log "[$code] $FRONTEND_BASE$route"
done
log ""

log "## 4) API Checks"
code="$(http_code "$API_BASE/api/health")"
log "[$code] $API_BASE/api/health"
api_url="$API_BASE/api/decision/quality-live?symbol=ETHUSDT"
api_body="$(curl -k -L -s --max-time 15 "$api_url" 2>/dev/null | head -c 2000)"
api_code="$(http_code "$api_url")"
log "[$api_code] $api_url"
if echo "$api_body" | grep -q 'decision_quality'; then log "[OK] decision_quality found"; else log "[ALERT] decision_quality missing or API failed"; fi
if echo "$api_body" | grep -q 'scenario_state'; then log "[OK] scenario_state found"; else log "[ALERT] scenario_state missing"; fi
if echo "$api_body" | grep -q 'live_price'; then log "[OK] live_price found"; else log "[WARN] live_price missing"; fi
log "API_SAMPLE_BEGIN"
log "$api_body"
log "API_SAMPLE_END"
log ""

log "## 5) Service Status"
if command -v systemctl >/dev/null 2>&1; then
  for svc in nginx ndsp-api ndip-api-new ndsp-next market-bridge; do
    if systemctl list-unit-files 2>/dev/null | grep -q "^$svc" || systemctl status "$svc" >/dev/null 2>&1; then
      systemctl is-active --quiet "$svc"; rc=$?
      log "[$(status $rc)] systemd $svc = $(systemctl is-active "$svc" 2>/dev/null || echo unknown)"
    else
      log "[INFO] systemd $svc not found"
    fi
  done
else
  log "[WARN] systemctl not available"
fi
if command -v pm2 >/dev/null 2>&1; then
  log "### PM2 list"
  pm2 list 2>/dev/null | sed 's/^/PM2: /' | tee -a "$REPORT" >/dev/null
else
  log "[INFO] pm2 not available"
fi
log ""

log "## 6) Nginx / SSL"
if command -v nginx >/dev/null 2>&1; then nginx -t 2>&1 | sed 's/^/NGINX: /' | tee -a "$REPORT" >/dev/null; else log "[WARN] nginx command unavailable"; fi
if command -v certbot >/dev/null 2>&1; then certbot certificates 2>/dev/null | grep -E 'Certificate Name|Expiry Date|Domains' | sed 's/^/CERTBOT: /' | tee -a "$REPORT" >/dev/null; else log "[INFO] certbot unavailable"; fi
log ""

log "## 7) Protected UI Element Presence"
if [ -d "$FRONTEND_DIR" ]; then
  radar_count="$(grep -RIlE 'radar|رادار|ndsp-radar' "$FRONTEND_DIR" 2>/dev/null | wc -l | tr -d ' ')"
  sidebar_count="$(grep -RIlE 'sidebar|side-menu|القائمة|menu' "$FRONTEND_DIR" 2>/dev/null | wc -l | tr -d ' ')"
  disclaimer_count="$(grep -RIlE 'disclaimer|إخلاء|ليست توصية|not financial advice|decision support' "$FRONTEND_DIR" 2>/dev/null | wc -l | tr -d ' ')"
  log "RADAR_FILE_COUNT=$radar_count"
  log "SIDEBAR_FILE_COUNT=$sidebar_count"
  log "DISCLAIMER_FILE_COUNT=$disclaimer_count"
else
  log "[ALERT] FRONTEND_DIR not found"
fi
log ""

log "## 8) Forbidden Wording Scan"
if [ -d "$FRONTEND_DIR" ]; then
  forbidden="Buy Now|Sell Now|Guaranteed profit|Enter trade|Exit trade|اشتر الآن|بع الآن|ادخل الصفقة|اخرج من الصفقة|ربح مضمون|صفقة مؤكدة"
  hits="$(grep -RInE "$forbidden" "$FRONTEND_DIR" 2>/dev/null | head -n 50 || true)"
  if [ -n "$hits" ]; then
    log "[ALERT] Forbidden wording found:"
    log "$hits"
  else
    log "[OK] No obvious forbidden wording found in first scan."
  fi
fi
log ""

log "## 9) Resource Snapshot"
df -h | sed 's/^/DF: /' | tee -a "$REPORT" >/dev/null
free -h 2>/dev/null | sed 's/^/MEM: /' | tee -a "$REPORT" >/dev/null || true
log ""
log "FINAL_STATUS=AUDIT_DONE"
log "REPORT=$REPORT"

#!/usr/bin/env bash
set -u
set +H

PROJECT_DIR="${PROJECT_DIR:-$HOME/empire-core-new}"
FRONTEND_DIR="${FRONTEND_DIR:-/var/www/ndsp-my}"
FRONTEND_BASE="${FRONTEND_BASE:-https://my.ndsp.app}"
API_BASE="${API_BASE:-https://api.ndsp.app}"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_DIR/docs/05-runbooks"
REPORT="$REPORT_DIR/NDSP_POST_PATCH_TEST_REPORT_$TS.md"
mkdir -p "$REPORT_DIR"
FAIL=0
log(){ echo "$*" | tee -a "$REPORT"; }
http_code(){ curl -k -L -s -o /dev/null -w "%{http_code}" --max-time 12 "$1" 2>/dev/null || echo "000"; }

: > "$REPORT"
log "# NDSP Post Patch Test Report"
log "DATE=$TS"
log "PROJECT_DIR=$PROJECT_DIR"
log "FRONTEND_DIR=$FRONTEND_DIR"
log "FRONTEND_BASE=$FRONTEND_BASE"
log "API_BASE=$API_BASE"
log ""

log "## 1) Required Pages HTTP"
for route in / /index.html /decision-support.html /NDSP_Asset_View.html /NDSP_Command_Center.html /NDSP_Daily_Brief.html /NDSP_Settings_Alerts.html; do
  code="$(http_code "$FRONTEND_BASE$route")"
  log "[$code] $FRONTEND_BASE$route"
  case "$code" in 200|301|302) ;; *) FAIL=1 ;; esac
done
log ""

log "## 2) Decision API Required Fields"
api_url="$API_BASE/api/decision/quality-live?symbol=ETHUSDT"
body="$(curl -k -L -s --max-time 15 "$api_url" 2>/dev/null | head -c 4000)"
for field in symbol live_price decision_quality scenario_state directional_context; do
  if echo "$body" | grep -q "\"$field\""; then log "[OK] field: $field"; else log "[ALERT] missing field: $field"; FAIL=1; fi
done
log ""

log "## 3) Protected UI Elements"
if [ -d "$FRONTEND_DIR" ]; then
  for pattern_name in RADAR SIDEBAR DISCLAIMER; do
    case "$pattern_name" in
      RADAR) pattern='radar|رادار|ndsp-radar' ;;
      SIDEBAR) pattern='sidebar|side-menu|القائمة|menu' ;;
      DISCLAIMER) pattern='disclaimer|إخلاء|ليست توصية|not financial advice|decision support' ;;
    esac
    count="$(grep -RIlE "$pattern" "$FRONTEND_DIR" 2>/dev/null | wc -l | tr -d ' ')"
    log "$pattern_name_COUNT=$count"
    if [ "$count" = "0" ]; then FAIL=1; fi
  done
else
  log "[ALERT] FRONTEND_DIR not found"
  FAIL=1
fi
log ""

log "## 4) Forbidden Wording"
if [ -d "$FRONTEND_DIR" ]; then
  forbidden="Buy Now|Sell Now|Guaranteed profit|Enter trade|Exit trade|اشتر الآن|بع الآن|ادخل الصفقة|اخرج من الصفقة|ربح مضمون|صفقة مؤكدة"
  hits="$(grep -RInE "$forbidden" "$FRONTEND_DIR" 2>/dev/null | head -n 50 || true)"
  if [ -n "$hits" ]; then
    log "[ALERT] Forbidden wording found:"
    log "$hits"
    FAIL=1
  else
    log "[OK] No obvious forbidden wording found."
  fi
fi
log ""

if [ "$FAIL" -eq 0 ]; then
  log "FINAL_STATUS=POST_PATCH_TEST_PASS"
  exit 0
else
  log "FINAL_STATUS=POST_PATCH_TEST_FAIL"
  exit 1
fi

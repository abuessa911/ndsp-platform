#!/usr/bin/env bash
set -u
set +H

TS="$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
FRONTEND_DIR="${FRONTEND_DIR:-/var/www/ndsp-my}"
FRONTEND_BASE="${FRONTEND_BASE:-https://my.ndsp.app}"
API_BASE="${API_BASE:-https://api.ndsp.app}"
REPORT="$PROJECT_DIR/docs/05-runbooks/NDSP_POST_PATCH_TEST_$TS.md"
mkdir -p "$PROJECT_DIR/docs/05-runbooks"

ALERTS=0
log(){ echo "$*" | tee -a "$REPORT"; }

http_check(){
  local url="$1"
  local code
  code="$(curl -k -sS -o /tmp/ndsp_post_patch_body_$$ -w "%{http_code}" "$url" || echo "000")"
  if [ "$code" = "200" ]; then
    log "[200] $url"
  else
    log "[ALERT] HTTP $code $url"
    ALERTS=$((ALERTS+1))
  fi
}

scan_count(){
  local pattern="$1"
  grep -RIE "$pattern" "$FRONTEND_DIR" "$PROJECT_DIR/apps/user-portal" "$PROJECT_DIR/backend" 2>/dev/null | wc -l | tr -d ' '
}

log "# NDSP Post Patch Test Report"
log "DATE=$TS"
log "PROJECT_DIR=$PROJECT_DIR"
log "FRONTEND_DIR=$FRONTEND_DIR"
log "FRONTEND_BASE=$FRONTEND_BASE"
log "API_BASE=$API_BASE"
log ""

log "## 1) Required Pages HTTP"
http_check "$FRONTEND_BASE/"
http_check "$FRONTEND_BASE/index.html"
http_check "$FRONTEND_BASE/decision-support.html"
http_check "$FRONTEND_BASE/NDSP_Asset_View.html"
http_check "$FRONTEND_BASE/NDSP_Command_Center.html"
http_check "$FRONTEND_BASE/NDSP_Daily_Brief.html"
http_check "$FRONTEND_BASE/NDSP_Settings_Alerts.html"
log ""

log "## 2) Decision API Required Fields"
API_JSON="/tmp/ndsp_post_patch_api_$TS.json"

if curl -k -fsS "$API_BASE/api/decision/quality-live?symbol=ETHUSDT" -o "$API_JSON"; then
  python3 - "$API_JSON" <<'PY' | tee -a "$REPORT"
import json, sys
data=json.load(open(sys.argv[1], encoding="utf-8"))

def get(path):
    cur=data
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur=cur[part]
    return cur

checks={
 "symbol":["instrument.symbol","symbol"],
 "live_price":["instrument.live_price","live_price"],
 "decision_quality":["allowed_public_outputs.decision_quality","decision_quality"],
 "scenario_state":["scenario.scenario_state","scenario_state"],
 "directional_context":["scenario.scenario_directional_context","allowed_public_outputs.directional_bias","directional_context"],
 "nmp_status":["scenario.nmp_status","allowed_public_outputs.nmp_status","nmp.status","nmp_status"],
 "nmp_level":["scenario.nmp_level","allowed_public_outputs.nmp_level","nmp.level","nmp_level"],
}

for name, paths in checks.items():
    found=None
    for p in paths:
        v=get(p)
        if v not in (None,""):
            found=p
            break
    if found:
        print(f"[OK] field: {name} via {found}")
    else:
        print(f"[ALERT] missing field: {name}")
PY
else
  log "[ALERT] API request failed"
  ALERTS=$((ALERTS+1))
fi

if grep -q "\[ALERT\]" "$REPORT"; then
  ALERTS=$((ALERTS+1))
fi
log ""

log "## 3) Protected UI Elements"
RADAR_COUNT="$(scan_count 'radar|decision-radar|risk-radar|الرادار')"
SIDEBAR_COUNT="$(scan_count 'sidebar|side-menu|sideNav|القائمة الجانبية|القائمة')"
DISCLAIMER_COUNT="$(scan_count 'disclaimer|إخلاء المسؤولية|ليست توصية|ليس توصية|not recommendation|not financial advice')"

log "RADAR_FILE_COUNT=$RADAR_COUNT"
log "SIDEBAR_FILE_COUNT=$SIDEBAR_COUNT"
log "DISCLAIMER_FILE_COUNT=$DISCLAIMER_COUNT"

[ "$RADAR_COUNT" -gt 0 ] && log "[OK] Radar presence detected" || { log "[ALERT] Radar not found"; ALERTS=$((ALERTS+1)); }
[ "$SIDEBAR_COUNT" -gt 0 ] && log "[OK] Sidebar presence detected" || { log "[ALERT] Sidebar not found"; ALERTS=$((ALERTS+1)); }
[ "$DISCLAIMER_COUNT" -gt 0 ] && log "[OK] Disclaimer presence detected" || { log "[ALERT] Disclaimer not found"; ALERTS=$((ALERTS+1)); }
log ""

log "## 4) Forbidden Wording Scan"
# Governed wording scan:
# - Scan public/live UI only.
# - Do not count backend policy rules or backups.
# - Do not count safe negative disclaimers such as "ليست توصية مالية أو أمر تنفيذ".
FORBIDDEN_COUNT="$(
  grep -RIE 'اشتر الآن|بيع الآن|ادخل صفقة|ربح مضمون|توصية مباشرة|Buy Now|Sell Now' \
    "$FRONTEND_DIR" "$PROJECT_DIR/apps/user-portal" \
    --exclude-dir=node_modules \
    --exclude-dir=.git \
    --exclude='*.log' \
    2>/dev/null | wc -l | tr -d ' '
)"

FATAL_EXECUTION_ORDER_COUNT="$(
  grep -RIE 'أمر تنفيذ' \
    "$FRONTEND_DIR" "$PROJECT_DIR/apps/user-portal" \
    --exclude-dir=node_modules \
    --exclude-dir=.git \
    --exclude='*.log' \
    2>/dev/null \
  | grep -vE 'ليس[ت]? توصية|ولا أمر تنفيذ|ليست توصية مالية أو أمر تنفيذ|ليس توصية مالية ولا أمر تنفيذ' \
  | wc -l | tr -d ' '
)"

if [ "$FORBIDDEN_COUNT" -eq 0 ] && [ "$FATAL_EXECUTION_ORDER_COUNT" -eq 0 ]; then
  log "[OK] No forbidden public wording found"
else
  log "[ALERT] Forbidden public wording count: $FORBIDDEN_COUNT"
  log "[ALERT] Unsafe execution-order wording count: $FATAL_EXECUTION_ORDER_COUNT"
  ALERTS=$((ALERTS+1))
fi
log ""

log "## 5) PM2 Runtime Check"
pm2 list | tee -a "$REPORT" || true
log ""

if [ "$ALERTS" -eq 0 ]; then
  log "FINAL_STATUS=POST_PATCH_TEST_OK"
else
  log "FINAL_STATUS=POST_PATCH_TEST_WITH_ALERTS"
  log "ALERTS=$ALERTS"
fi

log "REPORT=$REPORT"

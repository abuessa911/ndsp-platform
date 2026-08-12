#!/usr/bin/env bash
set -uo pipefail
set +H

TS="$(date +%Y%m%d_%H%M%S)"
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
FRONTEND_DIR="${FRONTEND_DIR:-/var/www/ndsp-my}"
FRONTEND_BASE="${FRONTEND_BASE:-https://my.ndsp.app}"
API_BASE="${API_BASE:-https://api.ndsp.app}"
REPORT="$PROJECT_DIR/docs/05-runbooks/NDSP_POST_PATCH_TEST_$TS.md"

mkdir -p "$PROJECT_DIR/docs/05-runbooks"

ALERTS=0

log(){
  echo "$*" | tee -a "$REPORT"
}

check_http(){
  local url="$1"
  local code
  code="$(curl -k -sS -o /tmp/ndsp_post_patch_http_body_$$ -w "%{http_code}" "$url" || echo "000")"
  if [ "$code" = "200" ]; then
    log "[200] $url"
  else
    log "[ALERT] HTTP $code $url"
    ALERTS=$((ALERTS+1))
  fi
}

count_matches(){
  local regex="$1"
  shift || true

  local dirs=()
  [ -d "$FRONTEND_DIR" ] && dirs+=("$FRONTEND_DIR")
  [ -d "$PROJECT_DIR/apps/user-portal" ] && dirs+=("$PROJECT_DIR/apps/user-portal")
  [ -d "$PROJECT_DIR/backend" ] && dirs+=("$PROJECT_DIR/backend")

  if [ "${#dirs[@]}" -eq 0 ]; then
    echo 0
    return 0
  fi

  grep -RIE "$regex" "${dirs[@]}" 2>/dev/null | wc -l | tr -d ' '
}

log "# NDSP Post Patch Test Report"
log "DATE=$TS"
log "PROJECT_DIR=$PROJECT_DIR"
log "FRONTEND_DIR=$FRONTEND_DIR"
log "FRONTEND_BASE=$FRONTEND_BASE"
log "API_BASE=$API_BASE"
log ""

log "## 1) Required Pages HTTP"
check_http "$FRONTEND_BASE/"
check_http "$FRONTEND_BASE/index.html"
check_http "$FRONTEND_BASE/decision-support.html"
check_http "$FRONTEND_BASE/NDSP_Asset_View.html"
check_http "$FRONTEND_BASE/NDSP_Command_Center.html"
check_http "$FRONTEND_BASE/NDSP_Daily_Brief.html"
check_http "$FRONTEND_BASE/NDSP_Settings_Alerts.html"
log ""

log "## 2) Decision API Required Fields"
API_JSON="/tmp/ndsp_post_patch_api_$TS.json"

if curl -k -fsS "$API_BASE/api/decision/quality-live?symbol=ETHUSDT" -o "$API_JSON"; then
  python3 - "$API_JSON" <<'PY' | tee -a "$REPORT"
import json, sys

path = sys.argv[1]

try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"[ALERT] invalid JSON: {e}")
    raise SystemExit(0)

def dig(obj, dotted):
    cur = obj
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur

checks = {
    "symbol": [
        "instrument.symbol",
        "symbol",
    ],
    "live_price": [
        "instrument.live_price",
        "live_price",
        "allowed_public_outputs.live_price",
    ],
    "decision_quality": [
        "allowed_public_outputs.decision_quality",
        "decision_quality",
    ],
    "scenario_state": [
        "scenario.scenario_state",
        "scenario_state",
    ],
    "directional_context": [
        "scenario.scenario_directional_context",
        "allowed_public_outputs.directional_bias",
        "directional_context",
    ],
    "nmp_status": [
        "scenario.nmp_status",
        "allowed_public_outputs.nmp_status",
        "nmp_status",
        "nmp.status",
    ],
    "nmp_level": [
        "scenario.nmp_level",
        "allowed_public_outputs.nmp_level",
        "nmp_level",
        "nmp.level",
    ],
}

for name, paths in checks.items():
    found_path = None
    value = None
    for p in paths:
        value = dig(data, p)
        if value not in (None, ""):
            found_path = p
            break

    if found_path:
        print(f"[OK] field: {name} via {found_path}")
    else:
        print(f"[ALERT] missing field: {name}")
PY

  if grep -q "\[ALERT\]" "$REPORT"; then
    ALERTS=$((ALERTS+1))
  fi
else
  log "[ALERT] API request failed: $API_BASE/api/decision/quality-live?symbol=ETHUSDT"
  ALERTS=$((ALERTS+1))
fi
log ""

log "## 3) Protected UI Elements"
RADAR_COUNT="$(count_matches 'radar|decision-radar|risk-radar|الرادار')"
SIDEBAR_COUNT="$(count_matches 'sidebar|side-menu|sideNav|القائمة الجانبية|القائمة')"
DISCLAIMER_COUNT="$(count_matches 'disclaimer|إخلاء المسؤولية|ليست توصية|ليس توصية|not recommendation|not financial advice')"

log "RADAR_FILE_COUNT=$RADAR_COUNT"
log "SIDEBAR_FILE_COUNT=$SIDEBAR_COUNT"
log "DISCLAIMER_FILE_COUNT=$DISCLAIMER_COUNT"

if [ "${RADAR_COUNT:-0}" -eq 0 ]; then
  log "[ALERT] Radar not found in scanned files"
  ALERTS=$((ALERTS+1))
else
  log "[OK] Radar presence detected"
fi

if [ "${SIDEBAR_COUNT:-0}" -eq 0 ]; then
  log "[ALERT] Sidebar not found in scanned files"
  ALERTS=$((ALERTS+1))
else
  log "[OK] Sidebar presence detected"
fi

if [ "${DISCLAIMER_COUNT:-0}" -eq 0 ]; then
  log "[ALERT] Disclaimer not found in scanned files"
  ALERTS=$((ALERTS+1))
else
  log "[OK] Disclaimer presence detected"
fi
log ""

log "## 4) Forbidden Wording Scan"
FORBIDDEN_COUNT="$(count_matches 'اشتر الآن|بيع الآن|ادخل صفقة|ربح مضمون|توصية مباشرة|أمر تنفيذ|Buy Now|Sell Now')"

if [ "${FORBIDDEN_COUNT:-0}" -eq 0 ]; then
  log "[OK] No obvious forbidden wording found"
else
  log "[ALERT] Forbidden wording count: $FORBIDDEN_COUNT"
  ALERTS=$((ALERTS+1))
fi
log ""

log "## 5) PM2 Runtime Check"
if command -v pm2 >/dev/null 2>&1; then
  pm2 list | tee -a "$REPORT" || true
else
  log "[INFO] PM2 not installed"
fi
log ""

if [ "$ALERTS" -eq 0 ]; then
  log "FINAL_STATUS=POST_PATCH_TEST_OK"
else
  log "FINAL_STATUS=POST_PATCH_TEST_WITH_ALERTS"
  log "ALERTS=$ALERTS"
fi

log "REPORT=$REPORT"

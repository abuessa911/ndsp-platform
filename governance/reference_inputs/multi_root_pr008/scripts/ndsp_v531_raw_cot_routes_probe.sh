#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V531_RAW_COT_ROUTES_PROBE_$TS.md"
mkdir -p "$HOME_DIR/ndsp_launch_reports"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=PROBE_ONLY_NO_CHANGES"
ROOT="$HOME_DIR/empire-core-new/apps/ndsp-raw-cot-gateway"
log "ROOT=$ROOT"

log ""
log "== 1) SERVICE =="
systemctl show ndsp-raw-cot-gateway.service -p ExecStart -p WorkingDirectory -p MainPID --no-pager 2>/dev/null | tee -a "$REPORT" || true

log ""
log "== 2) OPENAPI PATHS =="
OUT=/tmp/v531_openapi.json
CODE=$(curl -skL -o "$OUT" -w "%{http_code}" http://127.0.0.1:9076/openapi.json || echo 000)
SIZE=$(wc -c < "$OUT" 2>/dev/null || echo 0)
log "OPENAPI_HTTP=$CODE SIZE=$SIZE"
python3 - "$OUT" <<'PY' | tee -a "$REPORT"
import json,sys
p=sys.argv[1]
try:
 d=json.load(open(p))
 for path in sorted((d.get('paths') or {}).keys()): print('OPENAPI_PATH='+path)
except Exception as e:
 print('OPENAPI_ERROR='+str(e)); print(open(p,errors='ignore').read()[:500])
PY

log ""
log "== 3) FILE ROUTES =="
if [ -d "$ROOT" ]; then
  find "$ROOT" -maxdepth 4 -type f \( -name "*.py" -o -name "*.json" -o -name "*.csv" -o -name "*.md" \) ! -path "*/.venv/*" | sed 's#^#FILE=#' | tee -a "$REPORT"
  log "-- route grep --"
  grep -RInE '@app\.(get|post)|APIRouter|include_router|cot|COT|Asset Managers|Leveraged Funds|Commercials|Non-Commercials|Dealer|tdl|TDL|correction|explicit|implicit|على المكشوف|غير صريح' "$ROOT" --exclude-dir=.venv 2>/dev/null | head -220 | tee -a "$REPORT" || true
fi

log ""
log "== 4) CANDIDATE ENDPOINT TESTS =="
CANDIDATES=(
"/health"
"/"
"/api/health"
"/cot"
"/api/cot"
"/api/raw-cot"
"/api/raw-cot/latest"
"/api/raw-cot/BTCUSDT"
"/api/raw-cot?symbol=BTCUSDT"
"/api/tdl"
"/api/tdl?symbol=BTCUSDT"
"/api/tdl/correction?symbol=BTCUSDT"
"/api/correction?symbol=BTCUSDT"
"/raw-cot"
"/raw-cot/latest"
"/raw-cot/BTCUSDT"
"/tdl?symbol=BTCUSDT"
)
for P in "${CANDIDATES[@]}"; do
  U="http://127.0.0.1:9076$P"
  OUT=/tmp/v531_candidate.out
  CODE=$(curl -skL -o "$OUT" -w "%{http_code}" "$U" || echo 000)
  SIZE=$(wc -c < "$OUT" 2>/dev/null || echo 0)
  log "URL=$U HTTP=$CODE SIZE=$SIZE"
  if [ "$CODE" = "200" ]; then
    python3 - "$OUT" <<'PY' | tee -a "$REPORT"
import json,sys
p=sys.argv[1]
try:
 d=json.load(open(p)); print('JSON_HEAD='+json.dumps(d,ensure_ascii=False)[:700])
except Exception: print('TEXT_HEAD='+open(p,errors='ignore').read()[:500])
PY
  fi
done

log ""
log "== 5) TDL LAYER FILES =="
for F in "$HOME_DIR/empire-core-new/backend/layers/layer_orchestrator.py" "$HOME_DIR/empire-core-new/backend/layers/direction/l5_tdl_v2.py" "$HOME_DIR/empire-core-new/backend/layers/direction/l6_direction_authority.py"; do
  [ -f "$F" ] || continue
  log "FILE_SNIPPET=$F"
  sed -n '1,240p' "$F" | tee -a "$REPORT"
done

log "FINAL_STATUS=NDSP_V531_RAW_COT_ROUTES_PROBE_DONE"
log "REPORT=$REPORT"

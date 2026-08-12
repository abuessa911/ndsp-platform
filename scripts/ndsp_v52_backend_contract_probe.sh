#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V52_BACKEND_CONTRACT_PROBE_$TS.md"
RAW="$HOME_DIR/ndsp_launch_reports/NDSP_V52_BACKEND_CONTRACT_PROBE_RAW_$TS.log"
mkdir -p "$HOME_DIR/ndsp_launch_reports"
log(){ echo "$*" | tee -a "$REPORT"; }
raw(){ echo "$*" | tee -a "$RAW" >/dev/null; }
log "REPORT=$REPORT"
log "RAW=$RAW"
log "TS=$TS"
log "MODE=PROBE_ONLY_NO_CHANGES"

log ""
log "== 1) QUALITY JSON CONTRACT CHECK =="
for S in BTCUSDT ETHUSDT; do
  OUT="/tmp/ndsp_quality_${S}_$TS.json"
  curl -skS "https://my.ndsp.app/api/decision/quality-live?symbol=$S" -o "$OUT" || true
  python3 - "$S" "$OUT" <<'PY' | tee -a "$REPORT"
import sys,json
sym,path=sys.argv[1],sys.argv[2]
print(f"SYMBOL={sym}")
try: d=json.load(open(path))
except Exception as e:
 print('JSON_ERROR=',e); raise SystemExit
sc=d.get('scenario') or {}
checks=['nmp','nmp_level','nmp_status','nmp_timeframe','nmp_timeframes','nmp_levels_by_timeframe','levels_by_timeframe','correction_type','correction_visibility','reading_horizon','horizon_strength','tdl','tdl_state','tdl_context','risk_score','devil_advocate_score']
for k in checks:
 print(f"TOP.{k}=", 'YES' if k in d else 'NO')
for k in checks:
 print(f"SCENARIO.{k}=", 'YES' if k in sc else 'NO')
print('scenario_directional_context=', sc.get('scenario_directional_context'))
print('scenario_time_horizon=', sc.get('scenario_time_horizon'))
print('nmp_level=', d.get('nmp_level'))
print('nmp_timeframe=', d.get('nmp_timeframe'))
print('---')
PY
done

log ""
log "== 2) PUBLIC ENDPOINTS CHECK =="
for U in \
  "https://my.ndsp.app/api/decision/quality-live?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/nmp-timeframes-live?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v52?symbol=BTCUSDT"; do
  code=$(curl -skL -o /tmp/v52_probe_http.out -w "%{http_code}" "$U" || echo 000)
  size=$(wc -c < /tmp/v52_probe_http.out 2>/dev/null || echo 0)
  log "$U HTTP=$code SIZE=$size"
done

log ""
log "== 3) NGINX CANDIDATES =="
if command -v nginx >/dev/null 2>&1; then
  nginx -t 2>&1 | tee -a "$REPORT" || true
fi
sudo grep -RInE "server_name .*my\.ndsp\.app|quality-live|decision/quality|proxy_pass" /etc/nginx/sites-enabled /etc/nginx/conf.d 2>/dev/null | head -80 | tee -a "$REPORT" || true

log ""
log "== 4) SYSTEMD / PORTS =="
systemctl list-units --type=service --all 2>/dev/null | grep -Ei "ndsp|uvicorn|gunicorn|fastapi|python|decision|quality|nmp" | tee -a "$REPORT" || true
ss -ltnp 2>/dev/null | grep -Ei "905|906|800|uvicorn|python|gunicorn|node" | tee -a "$REPORT" || true

log ""
log "== 5) BACKEND FILE CANDIDATES =="
for ROOT in /opt /var/www /home/$USER_NAME /etc/systemd/system; do
  [ -d "$ROOT" ] || continue
  log "-- ROOT=$ROOT"
  sudo grep -RIlE "quality-live|nmp_level|scenario_time_horizon|FastAPI|uvicorn|decision/quality" "$ROOT" 2>/dev/null | head -80 | tee -a "$REPORT" || true
done

log ""
log "== 6) REQUIRED V52 CONTRACT =="
cat <<'EOF' | tee -a "$REPORT"
REQUIRED_ENDPOINTS:
/api/decision/nmp-timeframes-live?symbol=BTCUSDT
/api/decision/quality-contract-v52?symbol=BTCUSDT

REQUIRED_FIELDS:
nmp_timeframes.W1.level/status/timeframe/source
nmp_timeframes.D1.level/status/timeframe/source
nmp_timeframes.H4.level/status/timeframe/source
nmp_timeframes.H1.level/status/timeframe/source
nmp_timeframes.M15.level/status/timeframe/source
correction_type
correction_visibility
reading_horizon
horizon_strength
tdl_contract / tdl_state

GOVERNANCE:
Do not copy D1 NMP into H4/H1/W1/M15.
Do not invent correction_type if TDL backend does not compute it.
EOF
log "FINAL_STATUS=NDSP_V52_BACKEND_CONTRACT_PROBE_DONE"
log "REPORT=$REPORT"

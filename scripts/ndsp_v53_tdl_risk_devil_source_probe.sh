#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V53_TDL_RISK_DEVIL_SOURCE_PROBE_$TS.md"
RAW="$HOME_DIR/ndsp_launch_reports/NDSP_V53_TDL_RISK_DEVIL_SOURCE_PROBE_RAW_$TS.log"
mkdir -p "$HOME_DIR/ndsp_launch_reports"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "RAW=$RAW"
log "TS=$TS"
log "MODE=PROBE_ONLY_NO_CHANGES"

log ""
log "== 1) ENDPOINT FIELD PROBE =="
ENDPOINTS=(
"http://127.0.0.1:9066/api/risk-layer?symbol=BTCUSDT"
"http://127.0.0.1:9066/api/technical-confirmation?symbol=BTCUSDT"
"http://127.0.0.1:9066/api/market-structure?symbol=BTCUSDT"
"http://127.0.0.1:9066/api/ndsp16/layers/status?symbol=BTCUSDT"
"http://127.0.0.1:9044/api/governance/evaluate?symbol=BTCUSDT"
"http://127.0.0.1:9067/api/decision/quality-live?symbol=BTCUSDT"
"http://127.0.0.1:9082/api/decision/quality-live?symbol=BTCUSDT"
"http://127.0.0.1:9083/api/decision/quality-contract-v52?symbol=BTCUSDT"
"https://my.ndsp.app/api/decision/quality-contract-v52?symbol=BTCUSDT"
)
for U in "${ENDPOINTS[@]}"; do
  log ""
  log "URL=$U"
  OUT="/tmp/v53_endpoint.json"
  CODE=$(curl -skL -o "$OUT" -w "%{http_code}" "$U" || echo 000)
  SIZE=$(wc -c < "$OUT" 2>/dev/null || echo 0)
  log "HTTP=$CODE SIZE=$SIZE"
  python3 - "$OUT" <<'PY' | tee -a "$REPORT"
import sys,json
p=sys.argv[1]
try:
 d=json.load(open(p))
except Exception as e:
 print('JSON_ERROR='+str(e)); print(open(p,errors='ignore').read()[:260]); raise SystemExit
terms=['risk','devil','tdl','correction','visibility','horizon','quality','scenario','governance','allowed_public_outputs','confidence']
found=[]
def walk(o,prefix=''):
 if isinstance(o,dict):
  for k,v in o.items():
   name=f'{prefix}.{k}' if prefix else k
   if any(t in name.lower() for t in terms) and not isinstance(v,(dict,list)):
    found.append((name,v))
   walk(v,name)
 elif isinstance(o,list):
  for i,v in enumerate(o[:5]): walk(v,f'{prefix}[{i}]')
for k,v in found[:120]: print(f'{k} = {v}')
if not found: print('NO_RELEVANT_FIELDS_FOUND')
PY
done

log ""
log "== 2) SYSTEMD CANDIDATES =="
systemctl list-units --type=service --all 2>/dev/null | grep -Ei 'tdl|risk|devil|governance|decision|layer|quality|nmp' | tee -a "$REPORT" || true
log ""
for S in $(systemctl list-unit-files 2>/dev/null | awk '{print $1}' | grep -Ei 'tdl|risk|devil|governance|decision|layer|quality|nmp' | head -80); do
  echo "--- SERVICE=$S ---" | tee -a "$REPORT"
  systemctl show "$S" -p FragmentPath -p ExecStart -p WorkingDirectory -p MainPID --no-pager 2>/dev/null | tee -a "$REPORT" || true
done

log ""
log "== 3) CODE CANDIDATES =="
ROOTS=("/home/$USER_NAME/empire-core-new" "/home/$USER_NAME" "/opt" "/var/www")
for R in "${ROOTS[@]}"; do
  [ -d "$R" ] || continue
  log "-- ROOT=$R"
  sudo grep -RIlE 'correction_type|correction_visibility|tdl_state|TDL|risk_score|devil_advocate|محامي الشيطان|على المكشوف|غير صريح|implicit|explicit|Leveraged|Asset Managers|Commercials|Non-Commercials' "$R" 2>/dev/null | head -120 | tee -a "$REPORT" || true
done

log ""
log "== 4) HIGH SIGNAL SNIPPETS =="
for R in "/home/$USER_NAME/empire-core-new/backend" "/opt"; do
  [ -d "$R" ] || continue
  log "-- SNIPPETS ROOT=$R"
  sudo grep -RInE 'correction_type|correction_visibility|tdl_state|risk_score|devil_advocate|محامي الشيطان|على المكشوف|غير صريح' "$R" 2>/dev/null | head -200 | tee -a "$REPORT" || true
done

log ""
log "== 5) CONCLUSION TEMPLATE =="
cat <<'EOF' | tee -a "$REPORT"
If correction_type/correction_visibility are not found in endpoint outputs, they must not be displayed as real values.
If risk_score/devil_advocate_score are not found, radar must show NOT_PROVIDED or CONNECTED_TEXT_ONLY when only risk_note exists.
Next patch must only bind fields from a verified source file or endpoint.
EOF
log "FINAL_STATUS=NDSP_V53_TDL_RISK_DEVIL_SOURCE_PROBE_DONE"
log "REPORT=$REPORT"

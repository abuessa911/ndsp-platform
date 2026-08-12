#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APP="/opt/ndsp-v53-bridge/app.py"
SERVICE="ndsp-v53-bridge.service"
REPORT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v5481-profile-query-binding-$TS"
CHECKPOINT="$HOME_DIR/ndsp_release_checkpoints/NDSP_V5481_PROFILE_QUERY_BINDING_$TS"
REPORT="$REPORT_DIR/NDSP_V5481_PROFILE_QUERY_BINDING_FIX_$TS.md"
ROLLBACK="/tmp/ndsp_rollback_v5481_profile_query_binding_$TS.sh"
mkdir -p "$REPORT_DIR" "$BACKUP" "$CHECKPOINT"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=V5481_PROFILE_QUERY_BINDING_FIX"
log "APP=$APP"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] || { log "ERROR=APP_NOT_FOUND:$APP"; exit 1; }
cp -a "$APP" "$BACKUP/app.py.before_v5481"

log ""
log "== 1) PATCH ROUTE TO PASS ?profile= TO contract() =="
python3 - "$APP" <<'PY' | tee -a "$REPORT"
from pathlib import Path
import re, sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
orig=s

def add_profile_to_signature(line):
    if 'profile' in line:
        return line
    idx=line.rfind(')')
    if idx == -1:
        return line
    before=line[:idx].rstrip()
    after=line[idx:]
    if before.endswith('('):
        before += 'profile: str = "investor"'
    else:
        before += ', profile: str = "investor"'
    return before + after

def add_profile_to_contract_calls(line):
    # Add profile as second argument to single-line contract(...) calls where not already passed.
    start=0
    out=''
    changed=False
    while True:
        j=line.find('contract(', start)
        if j == -1:
            out += line[start:]
            break
        out += line[start:j]
        open_i=j+len('contract')
        depth=0
        k=open_i
        end=None
        while k < len(line):
            ch=line[k]
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    end=k
                    break
            k += 1
        if end is None:
            out += line[j:]
            break
        call=line[j:end+1]
        inner=line[open_i+1:end]
        if 'profile' not in inner:
            call='contract(' + inner.rstrip() + ', profile)'
            changed=True
        out += call
        start=end+1
    return out, changed

lines=s.splitlines(True)
out=[]
i=0
route_blocks=0
signature_patches=0
call_patches=0

while i < len(lines):
    line=lines[i]
    if line.lstrip().startswith('@'):
        dec_start=i
        decorators=[]
        while i < len(lines) and lines[i].lstrip().startswith('@'):
            decorators.append(lines[i])
            i += 1
        is_target=any('quality-contract-v53' in d for d in decorators)
        out.extend(decorators)
        if is_target and i < len(lines) and re.match(r'^\s*(async\s+def|def)\s+', lines[i]):
            route_blocks += 1
            def_line=add_profile_to_signature(lines[i])
            if def_line != lines[i]: signature_patches += 1
            out.append(def_line)
            def_indent=len(lines[i])-len(lines[i].lstrip())
            i += 1
            while i < len(lines):
                # Stop at next top-level def/decorator/class.
                if lines[i].lstrip().startswith('@') and (len(lines[i])-len(lines[i].lstrip()) <= def_indent):
                    break
                if re.match(r'^\s*(async\s+def|def|class)\s+', lines[i]) and (len(lines[i])-len(lines[i].lstrip()) <= def_indent):
                    break
                new_line, changed=add_profile_to_contract_calls(lines[i])
                if changed: call_patches += 1
                out.append(new_line)
                i += 1
            continue
        continue
    out.append(line)
    i += 1

s=''.join(out)

# Ensure contract() itself accepts profile parameter.
s2=re.sub(r'\ndef contract\((?![^)]*profile)([^)]*)\):', lambda m: '\ndef contract(' + (m.group(1).strip() + ', ' if m.group(1).strip() else '') + 'profile=None):', s, count=1)
contract_signature_patched = (s2 != s)
s=s2

# Ensure selected profile uses the function parameter, not hard-coded default.
if "sel=select_decision_profile_view(base, profile)" not in s and "select_decision_profile_view(base" in s:
    s=re.sub(r"sel\s*=\s*select_decision_profile_view\(base(?:,\s*[^)]*)?\)", "sel=select_decision_profile_view(base, profile)", s, count=1)

p.write_text(s,encoding='utf-8')
print(f'ROUTE_BLOCKS_FOUND={route_blocks}')
print(f'ROUTE_SIGNATURE_PATCHES={signature_patches}')
print(f'CONTRACT_CALL_PATCHES={call_patches}')
print(f'CONTRACT_SIGNATURE_PATCHED={contract_signature_patched}')
print('APP_CHANGED=' + str(s != orig))
PY

python3 -m py_compile "$APP"
systemctl restart "$SERVICE"
sleep 2

log ""
log "== 2) SHOW ROUTE SNIPPET =="
python3 - "$APP" <<'PY' | tee -a "$REPORT"
from pathlib import Path
s=Path(__import__('sys').argv[1]).read_text(encoding='utf-8',errors='ignore').splitlines()
for i,line in enumerate(s):
    if 'quality-contract-v53' in line:
        start=max(0,i-2); end=min(len(s),i+14)
        print('ROUTE_SNIPPET_START_LINE='+str(start+1))
        for n in range(start,end):
            print(f'{n+1}: {s[n]}')
        print('ROUTE_SNIPPET_END')
PY

log ""
log "== 3) API PROFILE SELECTION AUDIT =="
python3 - <<'PY' | tee -a "$REPORT"
import json, urllib.request, time, sys
base='https://my.ndsp.app/api/decision/quality-contract-v53'
final=True
for symbol in ['BTCUSDT','ETHUSDT']:
    for profile,expected in [('investor','OVERALL_DIRECTION'),('tactical','PARTIAL_OR_WEEKLY_DIRECTION')]:
        url=f'{base}?symbol={symbol}&profile={profile}&_={int(time.time())}'
        data=json.loads(urllib.request.urlopen(url,timeout=15).read().decode())
        view=data.get('selected_direction_view') or {}
        print('API_SYMBOL='+symbol)
        print('API_PROFILE_REQUESTED='+profile)
        print('API_SELECTED_PROFILE='+str(data.get('selected_profile')))
        print('API_SELECTED_PROFILE_AR='+str(data.get('selected_profile_ar')))
        print('API_CONTROLLING_TYPE='+str(view.get('controlling_direction_type')))
        print('API_CONTROLLING_AR='+str(view.get('controlling_direction_ar')))
        ok=(data.get('selected_profile')==profile and view.get('controlling_direction_type')==expected)
        print('API_PROFILE_MATCH_OK='+str(ok))
        if not ok: final=False
print('GATE_api_profile_selection_ok='+str(final))
print('FINAL_STATUS='+('PASS' if final else 'REVIEW'))
sys.exit(0 if final else 1)
PY
RC=${PIPESTATUS[0]}

log ""
log "== 4) HTTP CHECK =="
for url in \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT&profile=investor" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT&profile=tactical" \
  "https://my.ndsp.app/decision-center.html?symbol=BTCUSDT&profile=investor" \
  "https://my.ndsp.app/decision-center.html?symbol=BTCUSDT&profile=tactical"; do
  out="/tmp/v5481_http.out"
  code="$(curl -skL -o "$out" -w "%{http_code}" "$url" || echo 000)"
  size="$(wc -c < "$out" 2>/dev/null || echo 0)"
  marker="$(grep -Eo 'V5.4.8|selected_direction_view|ndsp-v548-profile-selector|PARTIAL_OR_WEEKLY_DIRECTION|OVERALL_DIRECTION' "$out" | head -1 || true)"
  log "HTTP_CHECK=$url HTTP=$code SIZE=$size MARKER=${marker:-NONE}"
done

log ""
log "== 5) CHECKPOINT / ROLLBACK =="
mkdir -p "$CHECKPOINT/backend"
cp -a "$APP" "$CHECKPOINT/backend/app.py"
find "$CHECKPOINT" -type f | sed 's#^#CHECKPOINT_FILE=#' | tee -a "$REPORT"
cat > "$ROLLBACK" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cp -a "$BACKUP/app.py.before_v5481" "$APP"
python3 -m py_compile "$APP"
systemctl restart "$SERVICE"
echo "ROLLBACK_V5481_OK_FROM=$BACKUP"
EOF
chmod +x "$ROLLBACK"
log "ROLLBACK=$ROLLBACK"
log "V5481_AUDIT_EXIT_CODE=$RC"
if [ "$RC" = 0 ]; then
  log "FINAL_STATUS=PASS"
else
  log "FINAL_STATUS=REVIEW"
fi
log "REPORT=$REPORT"
exit "$RC"

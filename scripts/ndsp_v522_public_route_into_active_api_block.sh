#!/usr/bin/env bash
set -euo pipefail
set +H
TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$HOME_DIR/ndsp_launch_reports/NDSP_V522_PUBLIC_ROUTE_ACTIVE_API_BLOCK_$TS.md"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v522-public-route-$TS"
mkdir -p "$HOME_DIR/ndsp_launch_reports" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
if [ "$(id -u)" != "0" ]; then log "ERROR=RUN_WITH_SUDO"; exit 1; fi
log "BACKUP=$BACKUP"
python3 - "$BACKUP" <<'PY' | tee -a "$REPORT"
from pathlib import Path
import shutil, time
backup=Path(__import__('sys').argv[1])
roots=[Path('/etc/nginx/conf.d'),Path('/etc/nginx/sites-enabled')]
route='''
    # NDSP V5.2 public contract routes - inserted before generic /api gateway
    location = /api/decision/v52/health {
        proxy_pass http://127.0.0.1:9083/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location = /api/decision/nmp-timeframes-live {
        proxy_pass http://127.0.0.1:9083/api/decision/nmp-timeframes-live$is_args$args;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location = /api/decision/quality-contract-v52 {
        proxy_pass http://127.0.0.1:9083/api/decision/quality-contract-v52$is_args$args;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

'''
patched=[]
for root in roots:
    if not root.exists(): continue
    for p in root.iterdir():
        if not p.is_file(): continue
        if '.disabled' in p.name or '.broken' in p.name: continue
        try: s=p.read_text(errors='ignore')
        except Exception: continue
        if 'server_name my.ndsp.app' not in s or 'location /api/' not in s: continue
        lines=s.splitlines(True)
        out=[]; depth=0; in_server=False; is_my=False; has_v52=False; inserted=False; block=[]
        def flush_block(block, is_my, has_v52):
            if not is_my or has_v52: return block, False
            new=[]; done=False
            for line in block:
                if (not done) and 'location /api/' in line:
                    new.append(route); done=True
                new.append(line)
            return new, done
        for line in lines:
            if (not in_server) and 'server' in line and '{' in line:
                in_server=True; depth=0; is_my=False; has_v52=False; block=[]
            if in_server:
                block.append(line)
                if 'server_name' in line and 'my.ndsp.app' in line: is_my=True
                if 'quality-contract-v52' in line or 'nmp-timeframes-live' in line or 'v52/health' in line: has_v52=True
                depth += line.count('{') - line.count('}')
                if depth<=0:
                    nb, did=flush_block(block,is_my,has_v52)
                    out.extend(nb); inserted = inserted or did
                    in_server=False; block=[]; depth=0
            else:
                out.append(line)
        if inserted:
            rel=p.as_posix().lstrip('/').replace('/','__')
            shutil.copy2(p, backup/(rel+'.before_v522'))
            p.write_text(''.join(out))
            patched.append(str(p))
            print('PATCHED='+str(p))
if not patched:
    print('PATCHED_NONE=YES')
PY
nginx -t
systemctl reload nginx
log ""
log "== PUBLIC VERIFY =="
for U in \
 "https://my.ndsp.app/api/decision/v52/health" \
 "https://my.ndsp.app/api/decision/nmp-timeframes-live?symbol=BTCUSDT" \
 "https://my.ndsp.app/api/decision/quality-contract-v52?symbol=BTCUSDT"; do
  OUT="/tmp/v522_check.out"
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$U" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  SVC="$(grep -Eo 'ndsp-platform-gateway-9002|ndsp-v52-contract|v52_contract' "$OUT" | head -1 || true)"
  log "$U HTTP=$CODE SIZE=$SIZE MARKER=${SVC:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json, urllib.request
try:
 d=json.loads(urllib.request.urlopen('https://my.ndsp.app/api/decision/nmp-timeframes-live?symbol=BTCUSDT',timeout=15).read().decode())
 for k,v in (d.get('nmp_timeframes') or {}).items(): print(f'NMP_FRAME_{k}_STATUS={v.get("status")} LEVEL={v.get("level")}')
except Exception as e:
 print('NMP_PUBLIC_JSON_ERROR='+str(e))
PY
log "FINAL_STATUS=NDSP_V522_PUBLIC_ROUTE_ACTIVE_API_BLOCK_DONE"
log "REPORT=$REPORT"

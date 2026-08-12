#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
TS="$(date +%Y%m%d_%H%M%S)"
U="${SUDO_USER:-nawaf511}"
H="$(getent passwd "$U" | cut -d: -f6 || echo /home/nawaf511)"
REPORT="$H/ndsp_launch_reports/NDSP_V53_BIND_TDL_DEVIL_$TS.md"
APPDIR="/opt/ndsp-v53-bridge"
APP="$APPDIR/app.py"
PRE="/var/www/ndsp-my/_premium"
mkdir -p "$H/ndsp_launch_reports" "$APPDIR" "$H/ndsp_launch_backups/ndsp-v53-$TS"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
[ "$(id -u)" = 0 ] || { log ERROR_RUN_WITH_SUDO; exit 1; }
[ -d "$PRE" ] && cp -a "$PRE" "$H/ndsp_launch_backups/ndsp-v53-$TS/_premium"
cat > "$APP" <<'PY'
#!/usr/bin/env python3
import csv,json,re,time,urllib.request,urllib.parse
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
PORT=9084
DATA=Path('/home/nawaf511/empire-core-new/backend/data/raw_cot')
def jget(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NDSP-V53'}),timeout=8) as r: return json.loads(r.read().decode())
def asset(sym):
    s=(sym or 'BTCUSDT').upper()
    if s.startswith('BTC'): return 'BTC','BITCOIN'
    if s.startswith('ETH'): return 'ETH','ETHER CASH SETTLED'
    if s.startswith('XAU') or 'GOLD' in s: return 'GOLD','GOLD'
    return re.sub('USDT$','',s),re.sub('USDT$','',s)
def devil(sym):
    a,_=asset(sym)
    try:
        d=jget(f'http://127.0.0.1:9077/api/layers/15/risk-invalidation/{a}')
        lvl=str(d.get('overallRiskLevel') or (d.get('data') or {}).get('overallRiskLevel') or 'UNKNOWN')
        sc={'Low':25,'Moderate':55,'Medium':55,'High':82,'Critical':96}.get(lvl,70)
        return {'connected':True,'status':lvl,'score':sc,'label_ar':{'High':'مرتفع','Moderate':'متوسط','Low':'منخفض','Critical':'حرج'}.get(lvl,lvl),'safety_margin':d.get('safetyMargin'),'source':'layer15_9077'}
    except Exception as e:
        return {'connected':False,'status':'NOT_CONNECTED','score':None,'error':str(e)[:120]}
def read_rows(p):
    try:
        return list(csv.reader(open(p,errors='ignore')))
    except Exception: return []
def tff_files():
    fs=list(DATA.glob('tff_futures_only_FinFutWk_*.txt'))
    cur=DATA/'current_tff_futures_only_FinFutWk.txt'
    if cur.exists(): fs.append(cur)
    return fs
def parse_tdl(sym):
    _,needle=asset(sym); rows=[]
    for f in tff_files():
        for r in read_rows(f):
            if len(r)>16 and needle in r[0].upper():
                try:
                    rows.append({'file':str(f),'market':r[0],'date':r[2],'am':float(r[11])-float(r[12]),'lf':float(r[14])-float(r[15])})
                except Exception: pass
    uniq={x['date']:x for x in rows}
    arr=[uniq[k] for k in sorted(uniq.keys())]
    if len(arr)<2:
        return {'tdl_state':'NOT_COMPUTED','correction_type':'NOT_PROVIDED','correction_visibility':'NOT_PROVIDED','source_status':'NEED_TWO_COT_REPORTS','matched_rows':len(arr)}
    p,c=arr[-2],arr[-1]; de=c['am']-p['am']; dn=c['lf']-p['lf']
    if de==0 or dn==0: typ,vis='NONE','لا يوجد تصحيح مؤكد'
    elif (de>0 and dn>0) or (de<0 and dn<0): typ,vis='IMPLICIT','غير صريح'
    else: typ,vis='EXPLICIT','على المكشوف'
    bias='BULLISH' if de>0 else 'BEARISH' if de<0 else 'NEUTRAL'
    return {'tdl_state':'CONNECTED','tdl_bias':bias,'correction_type':typ,'correction_visibility':vis,'extended_net_delta':round(de,2),'narrow_net_delta':round(dn,2),'previous_report':p,'current_report':c,'source_status':'RAW_COT_DERIVED'}
def contract(sym):
    try: base=jget(f'http://127.0.0.1:9083/api/decision/quality-contract-v52?symbol={sym}')
    except Exception as e: base={'ok':False,'symbol':sym,'v52_error':str(e)}
    dv=devil(sym); td=parse_tdl(sym)
    base.update({'devil_advocate':dv,'devil_advocate_status':dv['status'],'devil_advocate_score':dv['score'],'risk_status':'CONNECTED_FROM_LAYER15' if dv['connected'] else 'NOT_CONNECTED','risk_score':dv['score'],'tdl_contract':td,'tdl_state':td.get('tdl_state'),'tdl_bias':td.get('tdl_bias'),'correction_type':td.get('correction_type'),'correction_visibility':td.get('correction_visibility'),'v53_contract':{'ok':True,'version':'V5.3','sources':['raw_cot_files','layer15_devil','v52_nmp']}})
    return base
class H(BaseHTTPRequestHandler):
    def out(self,code,obj):
        b=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query); sym=q.get('symbol',['BTCUSDT'])[0].upper().replace('/','')
        if u.path=='/health': return self.out(200,{'ok':True,'service':'ndsp-v53-bridge','port':PORT})
        if u.path=='/api/decision/quality-contract-v53': return self.out(200,contract(sym))
        self.out(404,{'ok':False,'path':u.path})
    def log_message(self,*a): pass
ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
PY
chmod +x "$APP"
cat > /etc/systemd/system/ndsp-v53-bridge.service <<EOF
[Unit]
Description=NDSP V53 TDL Devil Bridge
After=network.target ndsp-v52-contract.service ndsp-16-layers.service
[Service]
Type=simple
ExecStart=/usr/bin/python3 $APP
Restart=always
RestartSec=3
User=root
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now ndsp-v53-bridge.service >/dev/null
systemctl restart ndsp-v53-bridge.service
sleep 2
python3 - <<'PY'
from pathlib import Path
route='''
    location = /api/decision/quality-contract-v53 {
        proxy_pass http://127.0.0.1:9084/api/decision/quality-contract-v53$is_args$args;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
'''
for p in list(Path('/etc/nginx/conf.d').glob('*'))+list(Path('/etc/nginx/sites-enabled').glob('*')):
    if not p.is_file() or '.disabled' in p.name: continue
    s=p.read_text(errors='ignore')
    if 'server_name my.ndsp.app' in s and 'location /api/' in s:
        if 'quality-contract-v53' not in s:
            i=s.find('location /api/')
            p.write_text(s[:i]+route+s[i:])
            print('PATCHED_NGINX='+str(p))
        break
PY
nginx -t && systemctl reload nginx
cat > "$PRE/assets/v53-bind.js" <<'JS'
(function(){if(window.__V53__)return;window.__V53__=1;const q=new URLSearchParams(location.search),sym=(q.get('symbol')||'BTCUSDT').toUpperCase();function box(l,t){document.querySelectorAll('.v501-box small').forEach(s=>{if((s.textContent||'').includes(l)){let b=s.parentElement.querySelector('b');if(b)b.textContent=t}})}function node(l,t){document.querySelectorAll('.v501-node').forEach(n=>{let s=n.querySelector('small'),b=n.querySelector('b');if(s&&b&&(s.textContent||'').includes(l))b.textContent=t})}async function run(){let d;try{d=await(await fetch('/api/decision/quality-contract-v53?symbol='+sym,{cache:'no-store'})).json()}catch(e){return}let dv=d.devil_advocate||{};box('نوع التصحيح',d.correction_visibility&&d.correction_visibility!=='NOT_PROVIDED'?d.correction_visibility:'غير محسوب');box('المخاطر',d.risk_status==='CONNECTED_FROM_LAYER15'?'متصل · '+(dv.label_ar||dv.status):'غير موصول');box('محامي الشيطان',dv.connected?'متصل · '+(dv.label_ar||dv.status):'غير موصول');node('المخاطر',d.risk_status==='CONNECTED_FROM_LAYER15'?'متصل':'غير موصول');node('محامي الشيطان',dv.connected?'متصل':'غير موصول');node('TDL',d.tdl_state==='CONNECTED'?'متصل':'غير محسوب')}setTimeout(run,700);setTimeout(run,1800);setTimeout(run,3500)})();
JS
for f in "$PRE/decision-center.html" "$PRE/decision-radar.html"; do [ -f "$f" ] || continue; python3 - "$f" "$TS" <<'PY'
import re,sys
p,ts=sys.argv[1],sys.argv[2]
s=open(p,encoding='utf-8').read()
s=re.sub(r'\s*<script[^>]+src=["\']/_premium/assets/v53-bind\.js\?v=[^"\']+["\'][^>]*>\s*</script>','',s)
s=s.replace('</body>',f'<script src="/_premium/assets/v53-bind.js?v={ts}"></script></body>')
open(p,'w',encoding='utf-8').write(s)
PY
done
chown -R www-data:www-data "$PRE" 2>/dev/null || true
log "== VERIFY =="
systemctl is-active ndsp-v53-bridge.service | sed 's/^/SERVICE_STATUS=/' | tee -a "$REPORT"
for URL in "http://127.0.0.1:9084/health" "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do OUT=/tmp/v53.out; C=$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000); S=$(wc -c < "$OUT"); log "$URL HTTP=$C SIZE=$S"; done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
d=json.loads(urllib.request.urlopen('http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT',timeout=10).read().decode())
for k in ['correction_visibility','correction_type','tdl_state','tdl_bias','risk_status','risk_score','devil_advocate_status','devil_advocate_score']:
 print(f'{k}={d.get(k)}')
PY
log "FINAL_STATUS=NDSP_V53_BIND_TDL_DEVIL_DONE"
log "URL_CENTER=https://my.ndsp.app/_premium/decision-center.html?symbol=BTCUSDT&v=$TS"
log "URL_RADAR=https://my.ndsp.app/_premium/decision-radar.html?symbol=BTCUSDT&v=$TS"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

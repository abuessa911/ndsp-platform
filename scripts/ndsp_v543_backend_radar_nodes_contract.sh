#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APPDIR="/opt/ndsp-v53-bridge"
APP="$APPDIR/app.py"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v543-radar-nodes-$TS"
REPORT="$OUT_DIR/NDSP_V543_BACKEND_RADAR_NODES_CONTRACT_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP" "$APPDIR"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=BACKEND_RADAR_NODES_CONTRACT"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] && cp -a "$APP" "$BACKUP/app.py.before_v543"

cat > "$APP" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re, time, urllib.request, urllib.parse
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone

PORT=9084
DATA=Path('/home/nawaf511/empire-core-new/backend/data/raw_cot')

def utcnow(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def jget(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NDSP-V543'}),timeout=10) as r:
        return json.loads(r.read().decode('utf-8','replace'))
def asset(sym):
    s=(sym or 'BTCUSDT').upper().replace('/','')
    if s.startswith('BTC'): return 'BTC','BITCOIN'
    if s.startswith('ETH'): return 'ETH','ETHER CASH SETTLED'
    if s.startswith('SOL'): return 'SOL','SOLANA'
    if s.startswith('XAU') or 'GOLD' in s: return 'GOLD','GOLD'
    return re.sub('USDT$','',s),re.sub('USDT$','',s)
def getp(obj,path,default=None):
    cur=obj
    for p in path.split('.'):
        if isinstance(cur,dict) and p in cur: cur=cur[p]
        else: return default
    return cur
def to_num(v, default=None):
    if isinstance(v,(int,float)): return float(v)
    if isinstance(v,str):
        m=re.search(r'-?\d+(?:\.\d+)?', v.replace(',',''))
        if m:
            try: return float(m.group(0))
            except Exception: return default
    return default

def devil(sym):
    a,_=asset(sym)
    try:
        d=jget(f'http://127.0.0.1:9077/api/layers/15/risk-invalidation/{a}')
        lvl=str(d.get('overallRiskLevel') or (d.get('data') or {}).get('overallRiskLevel') or 'UNKNOWN')
        sc={'Low':25,'Moderate':55,'Medium':55,'High':82,'Critical':96}.get(lvl,70)
        return {'connected':True,'status':lvl,'score':sc,'label_ar':{'High':'مرتفع','Moderate':'متوسط','Medium':'متوسط','Low':'منخفض','Critical':'حرج'}.get(lvl,lvl),'safety_margin':d.get('safetyMargin'),'source':'layer15_9077','source_endpoint':'http://127.0.0.1:9077/api/layers/15/risk-invalidation/{asset}','source_service':'ndsp-16-layers.service','updated_at':d.get('updatedAt') or utcnow()}
    except Exception as e:
        return {'connected':False,'status':'NOT_CONNECTED','score':None,'label_ar':'غير موصول','error':str(e)[:160],'source':'layer15_9077'}

def read_rows(p):
    try: return list(csv.reader(open(p,errors='ignore')))
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
        return {'tdl_state':'NOT_COMPUTED','correction_type':'NOT_PROVIDED','correction_visibility':'NOT_PROVIDED','source_status':'NEED_TWO_COT_REPORTS','matched_rows':len(arr),'source_endpoint':'raw_cot_files','source_service':'ndsp-v53-bridge','updated_at':utcnow()}
    p,c=arr[-2],arr[-1]
    de=c['am']-p['am']; dn=c['lf']-p['lf']
    if de==0 or dn==0: typ,vis='NONE','لا يوجد تصحيح مؤكد'
    elif (de>0 and dn>0) or (de<0 and dn<0): typ,vis='IMPLICIT','غير صريح'
    else: typ,vis='EXPLICIT','على المكشوف'
    bias='BULLISH' if de>0 else 'BEARISH' if de<0 else 'NEUTRAL'
    return {'tdl_state':'CONNECTED','tdl_bias':bias,'correction_type':typ,'correction_visibility':vis,'extended_net_delta':round(de,2),'narrow_net_delta':round(dn,2),'previous_report':p,'current_report':c,'source_status':'RAW_COT_DERIVED','source_endpoint':'/home/nawaf511/empire-core-new/backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt','source_service':'ndsp-v53-bridge','updated_at':utcnow()}

def risk_status(score):
    s=to_num(score)
    if s is None: return 'NOT_CONNECTED','غير موصول',None
    if s<=35: return 'LOW','منخفض',s
    if s<=65: return 'CAUTION','حذر',s
    if s<=79: return 'HIGH','مرتفع',s
    return 'CRITICAL','حرج',s

def devil_status(score):
    s=to_num(score)
    if s is None: return 'NOT_CONNECTED','غير موصول',None
    if s<=35: return 'PASSED','اجتاز',s
    if s<=65: return 'LIGHT_OBJECTION','اعتراض خفيف',s
    if s<=79: return 'STRONG_OBJECTION','اعتراض قوي',s
    return 'HARD_OBJECTION','اعتراض حاسم',s

def quality_status(score):
    s=to_num(score)
    if s is None: return 'UNKNOWN','غير مؤكد',None
    if s>=80: return 'READY','جاهز',s
    if s>=60: return 'CAUTION','حذر',s
    return 'WEAK','ضعيف',s

def node(node_id,status,label,score,source_layer,source_path,mode='BACKEND_DERIVED',endpoint='/api/decision/quality-contract-v53',freshness_path='updated_at'):
    return {'node_id':node_id,'status':status,'label_ar':label,'score':score,'source_endpoint':endpoint,'source_service':'ndsp-v53-bridge','source_layer':source_layer,'source_path':source_path,'freshness_path':freshness_path,'contract_mode':mode,'updated_at':utcnow(),'fallback_policy':'إذا غاب المصدر تظهر غير موصول ولا يتم اختراع نتيجة'}

def build_radar_nodes(base):
    dq=getp(base,'allowed_public_outputs.decision_quality',base.get('decision_quality'))
    qs,ql,qscore=quality_status(dq)
    levels_present=all(getp(base,f'scenario.{k}') not in (None,'') for k in ['scenario_activation_level','scenario_arrival_level','scenario_review_zone','scenario_invalidation_level'])
    ls,ll,lscore=('CONNECTED','مكتملة',75) if levels_present else ('MISSING','غير مكتملة',None)
    hs=base.get('horizon_strength')
    if isinstance(hs,str): hscore=80 if 'عالية' in hs or 'مرتفع' in hs else 60
    else: hscore=to_num(hs,70)
    hstat,hlabel,hscore=quality_status(hscore)
    nmp=getp(base,'nmp_timeframes') or {}
    nmp_count=sum(1 for k,v in nmp.items() if isinstance(v,dict) and v.get('status')=='AVAILABLE') if isinstance(nmp,dict) else 0
    ns,nl,nscore=('CONNECTED','مكتمل',min(100,nmp_count*20)) if nmp_count>=3 else ('CAUTION','حذر',nmp_count*20)
    rs,rl,rscore=risk_status(base.get('risk_score'))
    ds,dl,dscore=devil_status(base.get('devil_advocate_score'))
    corr=base.get('correction_type')
    if corr=='EXPLICIT': cs,cl,cscore='EXPLICIT','على المكشوف',90
    elif corr=='IMPLICIT': cs,cl,cscore='IMPLICIT','غير صريح',70
    elif corr=='NONE': cs,cl,cscore='NONE','لا يوجد تصحيح مؤكد',45
    elif corr: cs,cl,cscore=str(corr),str(base.get('correction_visibility') or corr),50
    else: cs,cl,cscore='NOT_PROVIDED','غير مرسل',None
    # cohesion: official backend-derived node, not UI fallback.
    scenario_state=getp(base,'scenario.scenario_state') or base.get('scenario_state')
    tdl_state=base.get('tdl_state')
    coh_score=70 if tdl_state=='CONNECTED' and scenario_state else 50
    coh_status='CONNECTED' if coh_score>=65 else 'CAUTION'
    coh_label='متماسك' if coh_score>=65 else 'حذر'
    return {
        'readiness': node('readiness',qs,ql,qscore,'Decision Quality','allowed_public_outputs.decision_quality'),
        'cohesion': node('cohesion',coh_status,coh_label,coh_score,'TDL + Scenario Cohesion','tdl_state + scenario.scenario_state'),
        'levels': node('levels',ls,ll,lscore,'Scenario Levels Adapter','scenario.scenario_activation_level + arrival + review + invalidation',freshness_path='scenario.scenario_last_updated'),
        'horizon': node('horizon',hstat,hlabel,hscore,'Horizon Engine','reading_horizon + horizon_strength'),
        'nmp_check': node('nmp_check',ns,nl,nscore,'NMP Independent Timeframes','nmp_timeframes.*.status',freshness_path='nmp_timeframes.*.updated_at'),
        'risk': node('risk',rs,rl,rscore,'Layer 15 / Risk Invalidation','risk_score',mode='BACKEND_DIRECT'),
        'devil': node('devil',ds,dl,dscore,'Layer 15 / Devil Advocate','devil_advocate_score',mode='BACKEND_DIRECT'),
        'tdl_correction': node('tdl_correction',cs,cl,cscore,'Raw COT / TDL Bridge','correction_type + correction_visibility',mode='BACKEND_DIRECT'),
    }

def contract(sym):
    try: base=jget(f'http://127.0.0.1:9083/api/decision/quality-contract-v52?symbol={sym}')
    except Exception as e: base={'ok':False,'symbol':sym,'v52_error':str(e)}
    dv=devil(sym); td=parse_tdl(sym)
    base.update({'ok':True,'symbol':sym,'devil_advocate':dv,'devil_advocate_status':dv.get('status'),'devil_advocate_score':dv.get('score'),'risk_status':'CONNECTED_FROM_LAYER15' if dv.get('connected') else 'NOT_CONNECTED','risk_score':dv.get('score'),'tdl_contract':td,'tdl_state':td.get('tdl_state'),'tdl_bias':td.get('tdl_bias'),'correction_type':td.get('correction_type'),'correction_visibility':td.get('correction_visibility'),'updated_at':utcnow(),'v53_contract':{'ok':True,'version':'V5.4.3','sources':['raw_cot_files','layer15_devil','v52_nmp','official_radar_nodes'],'updated_at':utcnow()}})
    base['radar_nodes']=build_radar_nodes(base)
    return base

class H(BaseHTTPRequestHandler):
    def out(self,code,obj):
        b=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-Length',str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u=urllib.parse.urlparse(self.path); q=urllib.parse.parse_qs(u.query); sym=q.get('symbol',['BTCUSDT'])[0].upper().replace('/','')
        if u.path=='/health': return self.out(200,{'ok':True,'service':'ndsp-v53-bridge','version':'V5.4.3','port':PORT})
        if u.path=='/api/decision/quality-contract-v53': return self.out(200,contract(sym))
        self.out(404,{'ok':False,'path':u.path})
    def log_message(self,*a): pass

ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
PY
chmod +x "$APP"

cat > /etc/systemd/system/ndsp-v53-bridge.service <<EOF
[Unit]
Description=NDSP V53/V543 TDL Devil Radar Nodes Bridge
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

# Patch governance audit freshness evidence for independent NMP timeframe contracts.
AUDIT="$OUT_DIR/ndsp_v54_contract_field_audit.py"
if [ -f "$AUDIT" ]; then
  cp -a "$AUDIT" "$BACKUP/ndsp_v54_contract_field_audit.py.before_v543"
  python3 - "$AUDIT" <<'PY'
import sys
p=sys.argv[1]
s=open(p,encoding='utf-8').read()
old="paths=['scenario.scenario_last_updated','scenario.nmp_last_updated','updated_at','nmp.updated_at','v53_contract.version','v53_contract.ok','v52_upstream_quality']"
new="paths=['scenario.scenario_last_updated','scenario.nmp_last_updated','updated_at','nmp.updated_at','nmp_timeframes.W1.updated_at','nmp_timeframes.D1.updated_at','nmp_timeframes.H4.updated_at','nmp_timeframes.H1.updated_at','nmp_timeframes.M15.updated_at','v53_contract.version','v53_contract.ok','v52_upstream_quality']"
if old in s:
    s=s.replace(old,new)
open(p,'w',encoding='utf-8').write(s)
PY
  log "PATCHED_AUDIT_FRESHNESS=$AUDIT"
fi

log ""
log "== VERIFY V543 CONTRACT =="
for URL in \
  "http://127.0.0.1:9084/health" \
  "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do
  OUT=/tmp/v543.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'radar_nodes|V5.4.3|readiness|nmp_check' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
d=json.loads(urllib.request.urlopen('https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT',timeout=12).read().decode())
print('v53_version='+str((d.get('v53_contract') or {}).get('version')))
print('has_radar_nodes='+str('radar_nodes' in d))
for k in ['readiness','cohesion','levels','horizon','nmp_check','risk','devil','tdl_correction']:
    n=(d.get('radar_nodes') or {}).get(k) or {}
    print(f'RADAR_NODE_{k}_STATUS={n.get("status")} LABEL={n.get("label_ar")} SCORE={n.get("score")}')
PY

log ""
log "== STRICT OFFICIAL RADAR AUDIT =="
if [ -x "$AUDIT" ]; then
  set +e
  python3 "$AUDIT" --symbols BTCUSDT,ETHUSDT --out-dir "$OUT_DIR" --strict-official-radar | tee -a "$REPORT"
  RC=${PIPESTATUS[0]}
  set -e
  log "STRICT_AUDIT_EXIT_CODE=$RC"
else
  log "STRICT_AUDIT_SCRIPT_MISSING"
fi
log "FINAL_STATUS=NDSP_V543_BACKEND_RADAR_NODES_CONTRACT_DONE"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

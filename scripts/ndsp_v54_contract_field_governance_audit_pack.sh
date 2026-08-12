#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
REPORT="$OUT_DIR/NDSP_V54_CONTRACT_FIELD_GOVERNANCE_INSTALL_$TS.md"
PY_SCRIPT="$OUT_DIR/ndsp_v54_contract_field_audit.py"
GOV_MD="$OUT_DIR/NDSP_V54_CONTRACT_FIELD_GOVERNANCE.md"
mkdir -p "$OUT_DIR"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=GOVERNANCE_AND_AUDIT_ONLY_NO_APP_CHANGES"

cat > "$GOV_MD" <<'MD'
# NDSP V5.4 — حوكمة عقود الحقول وربط الرادار

## الهدف
لا يظهر أي حقل في واجهة NDSP أو الرادار إلا إذا كان له عقد Backend واضح، قابل للفحص، ويعيد قيمة live لكل أصل.

## القاعدة التنفيذية
أي حقل UI يجب أن يملك:

1. `field_id` اسم ثابت للحقل.
2. `source_endpoint` نقطة API معروفة.
3. `json_path` مسار القيمة داخل JSON.
4. `source_layer` المحرك أو الطبقة المسؤولة.
5. `freshness_path` مسار وقت التحديث أو دليل live.
6. `contract_mode` واحد من:
   - `BACKEND_DIRECT`: الحقل موجود مباشرة في JSON.
   - `BACKEND_DERIVED`: الحقل مشتق داخل Backend من حقول موثقة.
   - `UI_DERIVED`: غير مقبول للإنتاج إلا كتحذير مؤقت.
7. `fallback_policy`: إذا غاب الحقل تظهر `غير موصول` ولا يتم اختراع نتيجة.

## حقول الرادار المطلوبة
| field_id | المطلوب | حالة القبول |
|---|---|---|
| radar.readiness | جاهزية القرار | Backend مباشر أو مشتق موثق |
| radar.cohesion | التماسك | Backend مباشر أو مشتق موثق |
| radar.levels | المستويات | Backend مباشر من مستويات السيناريو |
| radar.horizon | الأفق | Backend مباشر من reading_horizon/horizon_strength |
| radar.nmp_check | تحقق NMP | Backend مباشر من nmp_timeframes |
| radar.risk | المخاطر | Backend مباشر من risk_score |
| radar.devil | محامي الشيطان | Backend مباشر من devil_advocate_score |
| radar.tdl_correction | التصحيح TDL | Backend مباشر من correction_type/correction_visibility |

## حقول مركز القرار المطلوبة
- live_price
- scenario_state
- scenario_activation_level
- scenario_arrival_level
- scenario_review_zone
- scenario_invalidation_level
- reading_horizon
- horizon_strength
- nmp_timeframes
- correction_visibility
- risk_score
- devil_advocate_score

## سياسة الفشل
- Missing field = FAIL
- Null value = FAIL
- UI-only value = FAIL في الوضع الصارم
- Static placeholder مثل `حذر` بدون مصدر = FAIL في الوضع الصارم
- Derived without evidence = WARN أو FAIL حسب خيار strict

## أمر التشغيل القياسي
```bash
python3 /home/nawaf511/ndsp_final_governance_reports/ndsp_v54_contract_field_audit.py \
  --symbols BTCUSDT,ETHUSDT \
  --out-dir /home/nawaf511/ndsp_final_governance_reports
```

## نتيجة القبول
لا يتم ترقية `_premium` إلى الصفحات الرئيسية إلا إذا أعطى الفحص:

```text
FINAL_STATUS=PASS
```

أو إذا كان التحذير الوحيد متعلقًا بتحسين شكل الحقل وليس غياب عقد Backend.
MD

cat > "$PY_SCRIPT" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

BASE_PUBLIC_DEFAULT='https://my.ndsp.app'

ENDPOINTS={
  'v53':'{base}/api/decision/quality-contract-v53?symbol={symbol}&_={ts}',
  'nmp':'{base}/api/decision/nmp-timeframes-live?symbol={symbol}&_={ts}',
  'quality':'{base}/api/decision/quality-live?symbol={symbol}&_={ts}',
}

REGISTRY={
  # Radar fields
  'radar.readiness': {
    'endpoint':'v53', 'paths':['radar_nodes.readiness.status','allowed_public_outputs.decision_quality','decision_quality'],
    'source_layer':'Decision Quality / Readiness', 'mode':'BACKEND_DERIVED', 'strict_direct_path':'radar_nodes.readiness.status'
  },
  'radar.cohesion': {
    'endpoint':'v53', 'paths':['radar_nodes.cohesion.status','tdl_state','scenario.scenario_state'],
    'source_layer':'TDL + Scenario Cohesion', 'mode':'BACKEND_DERIVED', 'strict_direct_path':'radar_nodes.cohesion.status'
  },
  'radar.levels': {
    'endpoint':'v53', 'paths':['radar_nodes.levels.status','scenario.scenario_activation_level','scenario.scenario_arrival_level','scenario.scenario_review_zone','scenario.scenario_invalidation_level'],
    'source_layer':'Scenario Levels Adapter', 'mode':'BACKEND_DERIVED', 'strict_direct_path':'radar_nodes.levels.status'
  },
  'radar.horizon': {
    'endpoint':'v53', 'paths':['radar_nodes.horizon.status','reading_horizon','horizon_strength','allowed_public_outputs.reading_horizon'],
    'source_layer':'Horizon Engine', 'mode':'BACKEND_DERIVED', 'strict_direct_path':'radar_nodes.horizon.status'
  },
  'radar.nmp_check': {
    'endpoint':'v53', 'paths':['radar_nodes.nmp_check.status','nmp_timeframes.D1.status','nmp_timeframes.H4.status'],
    'source_layer':'NMP Timeframe Contract', 'mode':'BACKEND_DERIVED', 'strict_direct_path':'radar_nodes.nmp_check.status'
  },
  'radar.risk': {
    'endpoint':'v53', 'paths':['radar_nodes.risk.status','risk_score'],
    'source_layer':'Layer 15 / Risk Invalidation', 'mode':'BACKEND_DIRECT', 'strict_direct_path':'risk_score'
  },
  'radar.devil': {
    'endpoint':'v53', 'paths':['radar_nodes.devil.status','devil_advocate_score'],
    'source_layer':'Layer 15 / Devil Advocate', 'mode':'BACKEND_DIRECT', 'strict_direct_path':'devil_advocate_score'
  },
  'radar.tdl_correction': {
    'endpoint':'v53', 'paths':['radar_nodes.tdl_correction.status','correction_visibility','correction_type','tdl_contract.source_status'],
    'source_layer':'Raw COT / TDL Bridge', 'mode':'BACKEND_DIRECT', 'strict_direct_path':'correction_type'
  },
  # Decision center fields
  'decision.live_price': {'endpoint':'v53','paths':['instrument.live_price','live_price'],'source_layer':'Live Price Bridge','mode':'BACKEND_DIRECT'},
  'decision.scenario_state': {'endpoint':'v53','paths':['scenario.scenario_state'],'source_layer':'Scenario Engine','mode':'BACKEND_DIRECT'},
  'decision.scenario_activation_level': {'endpoint':'v53','paths':['scenario.scenario_activation_level'],'source_layer':'Scenario Levels','mode':'BACKEND_DIRECT'},
  'decision.scenario_arrival_level': {'endpoint':'v53','paths':['scenario.scenario_arrival_level'],'source_layer':'Scenario Levels','mode':'BACKEND_DIRECT'},
  'decision.scenario_review_zone': {'endpoint':'v53','paths':['scenario.scenario_review_zone'],'source_layer':'Scenario Levels','mode':'BACKEND_DIRECT'},
  'decision.scenario_invalidation_level': {'endpoint':'v53','paths':['scenario.scenario_invalidation_level'],'source_layer':'Scenario Levels','mode':'BACKEND_DIRECT'},
  'decision.reading_horizon': {'endpoint':'v53','paths':['reading_horizon','allowed_public_outputs.reading_horizon'],'source_layer':'Horizon Engine','mode':'BACKEND_DIRECT'},
  'decision.horizon_strength': {'endpoint':'v53','paths':['horizon_strength','allowed_public_outputs.horizon_strength'],'source_layer':'Horizon Engine','mode':'BACKEND_DIRECT'},
  'decision.nmp_timeframes': {'endpoint':'nmp','paths':['nmp_timeframes.W1.level','nmp_timeframes.D1.level','nmp_timeframes.H4.level','nmp_timeframes.H1.level','nmp_timeframes.M15.level'],'source_layer':'NMP Independent Timeframes','mode':'BACKEND_DIRECT'},
  'decision.correction_visibility': {'endpoint':'v53','paths':['correction_visibility'],'source_layer':'TDL Raw COT Bridge','mode':'BACKEND_DIRECT'},
  'decision.risk_score': {'endpoint':'v53','paths':['risk_score'],'source_layer':'Layer 15 / Risk','mode':'BACKEND_DIRECT'},
  'decision.devil_advocate_score': {'endpoint':'v53','paths':['devil_advocate_score'],'source_layer':'Layer 15 / Devil','mode':'BACKEND_DIRECT'},
}

STATIC_BAD={'حذر','متصل','غير موصول','—','N/A','NA','null','undefined','placeholder'}

def now_iso(): return datetime.now(timezone.utc).isoformat()

def fetch(url:str,timeout:int=12)->tuple[int,Any,str]:
    try:
        with urllib.request.urlopen(url,timeout=timeout) as r:
            raw=r.read().decode('utf-8','replace')
            try: data=json.loads(raw)
            except Exception: data={'_raw':raw[:500]}
            return r.status,data,raw
    except Exception as e:
        return 0,{'_error':repr(e)},''

def get_path(obj:Any,path:str):
    cur=obj
    for part in path.split('.'):
        if isinstance(cur,dict) and part in cur: cur=cur[part]
        else: return None
    return cur

def value_ok(v:Any)->tuple[bool,str]:
    if v is None: return False,'NULL_OR_MISSING'
    if isinstance(v,str):
        s=v.strip()
        if not s: return False,'EMPTY_STRING'
        if s in STATIC_BAD: return False,'STATIC_PLACEHOLDER'
    return True,'OK'

def fresh_evidence(data:dict)->list[str]:
    paths=['scenario.scenario_last_updated','scenario.nmp_last_updated','updated_at','nmp.updated_at','v53_contract.version','v53_contract.ok','v52_upstream_quality']
    out=[]
    for p in paths:
        v=get_path(data,p)
        if v is not None: out.append(f'{p}={v}')
    return out

def audit_symbol(symbol:str,base:str,strict:bool):
    ts=int(time.time())
    docs={}
    endpoint_status={}
    for name,tpl in ENDPOINTS.items():
        url=tpl.format(base=base.rstrip('/'),symbol=symbol,ts=ts)
        code,data,raw=fetch(url)
        docs[name]=data
        endpoint_status[name]={'url':url,'http':code,'size':len(raw)}
    rows=[]
    for field,reg in REGISTRY.items():
        ep=reg['endpoint']; data=docs.get(ep) or {}; found=[]
        for p in reg['paths']:
            v=get_path(data,p)
            if v is not None: found.append((p,v))
        status='PASS'; notes=[]
        if endpoint_status[ep]['http']!=200:
            status='FAIL'; notes.append(f'endpoint_http={endpoint_status[ep]["http"]}')
        if not found:
            status='FAIL'; notes.append('missing_all_contract_paths')
        else:
            ok_any=False
            for p,v in found:
                ok,why=value_ok(v)
                if ok: ok_any=True
                notes.append(f'{p}={str(v)[:120]}')
                if not ok: notes.append(f'{p}_bad={why}')
            if not ok_any: status='FAIL'
        # strict check: require official radar_nodes.* path if radar field asks for it
        if strict and field.startswith('radar.'):
            direct=reg.get('strict_direct_path')
            if direct and get_path(data,direct) is None:
                status='FAIL'; notes.append(f'strict_missing_official_backend_node={direct}')
        elif field.startswith('radar.') and reg.get('strict_direct_path') and get_path(data,reg['strict_direct_path']) is None:
            if status=='PASS': status='WARN'
            notes.append('backend_value_exists_but_no_official_radar_nodes_object_yet')
        fe=fresh_evidence(data)
        if fe: notes.extend(fe[:3])
        else:
            if status=='PASS': status='WARN'
            notes.append('no_freshness_evidence_found')
        rows.append({'field':field,'status':status,'endpoint':ep,'source_layer':reg['source_layer'],'mode':reg['mode'],'notes':notes})
    return endpoint_status,rows

def write_reports(symbol:str,out:Path,endpoint_status,rows):
    final='PASS'
    if any(r['status']=='FAIL' for r in rows): final='FAIL'
    elif any(r['status']=='WARN' for r in rows): final='WARN'
    md=[]
    md.append(f'# NDSP V5.4 Contract Field Audit — {symbol}')
    md.append('')
    md.append(f'Generated: {now_iso()}')
    md.append('')
    md.append('## Endpoints')
    for k,v in endpoint_status.items(): md.append(f'- {k}: HTTP={v["http"]} SIZE={v["size"]} URL={v["url"]}')
    md.append('')
    md.append('| Field | Status | Source Layer | Mode | Evidence |')
    md.append('|---|---:|---|---|---|')
    for r in rows:
        ev='<br>'.join(str(x).replace('|','/') for x in r['notes'][:8])
        md.append(f'| {r["field"]} | {r["status"]} | {r["source_layer"]} | {r["mode"]} | {ev} |')
    md.append('')
    md.append(f'FINAL_STATUS={final}')
    (out/f'NDSP_V54_FIELD_AUDIT_{symbol}.md').write_text('\n'.join(md),encoding='utf-8')
    (out/f'NDSP_V54_FIELD_AUDIT_{symbol}.json').write_text(json.dumps({'symbol':symbol,'final_status':final,'endpoints':endpoint_status,'rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    return final

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--symbols',default='BTCUSDT,ETHUSDT')
    ap.add_argument('--base-public',default=BASE_PUBLIC_DEFAULT)
    ap.add_argument('--out-dir',default='/home/nawaf511/ndsp_final_governance_reports')
    ap.add_argument('--strict-official-radar',action='store_true',help='Fail radar fields unless radar_nodes.* exists directly in backend contract')
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    finals=[]
    for sym in [s.strip().upper() for s in args.symbols.split(',') if s.strip()]:
        es,rows=audit_symbol(sym,args.base_public,args.strict_official_radar)
        final=write_reports(sym,out,es,rows)
        finals.append(final)
        print(f'SYMBOL={sym} FINAL_STATUS={final}')
        for r in rows:
            print(f'{sym} {r["field"]} {r["status"]}')
    overall='PASS'
    if 'FAIL' in finals: overall='FAIL'
    elif 'WARN' in finals: overall='WARN'
    print(f'FINAL_STATUS={overall}')
    sys.exit(0 if overall=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$PY_SCRIPT"

log "GOVERNANCE_MD=$GOV_MD"
log "AUDIT_SCRIPT=$PY_SCRIPT"
log ""
log "== RUN NON-STRICT AUDIT =="
set +e
python3 "$PY_SCRIPT" --symbols BTCUSDT,ETHUSDT --out-dir "$OUT_DIR" | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "AUDIT_EXIT_CODE=$RC"
log ""
log "== GENERATED REPORTS =="
ls -1 "$OUT_DIR"/NDSP_V54_FIELD_AUDIT_* 2>/dev/null | tee -a "$REPORT" || true
log "FINAL_STATUS=NDSP_V54_CONTRACT_FIELD_GOVERNANCE_AUDIT_PACK_DONE"
log "REPORT=$REPORT"

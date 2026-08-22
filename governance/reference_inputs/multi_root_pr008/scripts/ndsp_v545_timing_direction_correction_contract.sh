#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APP="/opt/ndsp-v53-bridge/app.py"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v545-timing-direction-correction-$TS"
REPORT="$OUT_DIR/NDSP_V545_TIMING_DIRECTION_CORRECTION_CONTRACT_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=BACKEND_TIMING_DIRECTION_CORRECTION_CONTRACT"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] || { log "ERROR=APP_NOT_FOUND:$APP"; exit 1; }
cp -a "$APP" "$BACKUP/app.py.before_v545"

python3 - "$APP" <<'PY'
from pathlib import Path
import sys, re
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

if 'def build_timing_direction_correction_contract(sym, base, td):' not in s:
    insert = r'''

def _direction_from_value(v):
    try:
        x=float(v)
    except Exception:
        return 'NEUTRAL','محايد'
    if x > 0: return 'BULLISH','صاعد'
    if x < 0: return 'BEARISH','هابط'
    return 'NEUTRAL','محايد'

def _weekday_authority(sym):
    wd=datetime.now(timezone.utc).weekday()
    names_ar=['الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','الأحد']
    names_en=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    s=(sym or '').upper()
    is_crypto=s.endswith('USDT') or s.startswith(('BTC','ETH','SOL'))
    if wd in (0,4):
        return 'EXTENDED_HORIZON','الأفق الممتد',wd,names_ar[wd],names_en[wd],'سلطة اليوم للأفق الممتد.'
    if wd in (1,2,3):
        return 'NARROW_HORIZON','الأفق الضيق',wd,names_ar[wd],names_en[wd],'سلطة اليوم للأفق الضيق.'
    if is_crypto:
        return 'NARROW_HORIZON','الأفق الضيق',wd,names_ar[wd],names_en[wd],'عطلة نهاية الأسبوع: الأصول المستمرة تتبع الأفق الضيق.'
    return 'NO_ACTIVE_AUTHORITY','لا توجد سلطة توقيت نشطة',wd,names_ar[wd],names_en[wd],'لا توجد سلطة توقيت نشطة لهذا الأصل في نهاية الأسبوع.'

def build_timing_direction_correction_contract(sym, base, td):
    authority, authority_ar, wd, wd_ar, wd_en, reason_ar = _weekday_authority(sym)
    prev=td.get('previous_report') if isinstance(td,dict) else None
    cur=td.get('current_report') if isinstance(td,dict) else None
    if authority == 'NO_ACTIVE_AUTHORITY':
        return {
            'ok': False,
            'version': 'V5.4.5',
            'public_name_ar': 'عقد التصحيح حسب سلطة التوقيت والاتجاه',
            'correction_type': 'UNKNOWN',
            'correction_visibility': 'غير مؤكد: لا توجد سلطة توقيت نشطة',
            'correction_state': 'UNKNOWN',
            'day_authority': authority,
            'day_authority_ar': authority_ar,
            'weekday': wd_en,
            'weekday_ar': wd_ar,
            'reason_ar': reason_ar,
            'source_service': 'ndsp-v53-bridge',
            'source_endpoint': '/api/decision/quality-contract-v53',
            'contract_mode': 'BACKEND_DERIVED',
            'updated_at': utcnow(),
            'fallback_policy': 'إذا غابت سلطة التوقيت أو البيانات لا يتم إعلان تصحيح.',
        }
    if not isinstance(prev,dict) or not isinstance(cur,dict):
        return {
            'ok': False,
            'version': 'V5.4.5',
            'public_name_ar': 'عقد التصحيح حسب سلطة التوقيت والاتجاه',
            'correction_type': 'UNKNOWN',
            'correction_visibility': 'غير مؤكد: لا توجد تقارير كافية لمقارنة الاتجاه الجزئي بالاتجاه العام',
            'correction_state': 'UNKNOWN',
            'day_authority': authority,
            'day_authority_ar': authority_ar,
            'weekday': wd_en,
            'weekday_ar': wd_ar,
            'reason_ar': 'يلزم توفر تقريرين على الأقل لنفس الأفق الحاكم حتى يتم تحديد التصحيح.',
            'source_service': 'ndsp-v53-bridge',
            'source_endpoint': '/api/decision/quality-contract-v53',
            'contract_mode': 'BACKEND_DERIVED',
            'updated_at': utcnow(),
            'fallback_policy': 'إذا غابت التقارير لا يتم اختراع تصحيح.',
        }
    if authority == 'EXTENDED_HORIZON':
        cur_net=cur.get('am'); prev_net=prev.get('am')
        authority_path='tdl_contract.current_report.extended_horizon_net'
        delta_path='tdl_contract.current_report.extended_horizon_delta'
    else:
        cur_net=cur.get('lf'); prev_net=prev.get('lf')
        authority_path='tdl_contract.current_report.narrow_horizon_net'
        delta_path='tdl_contract.current_report.narrow_horizon_delta'
    try:
        delta=float(cur_net)-float(prev_net)
    except Exception:
        delta=0.0
    overall_dir, overall_ar = _direction_from_value(cur_net)
    partial_dir, partial_ar = _direction_from_value(delta)
    if overall_dir == 'NEUTRAL' or partial_dir == 'NEUTRAL':
        state='UNKNOWN'
        ctype='UNKNOWN'
        vis='غير مؤكد: أحد الاتجاهين محايد ولا يكفي لإعلان تصحيح'
        score=40
        is_correction=False
    elif overall_dir != partial_dir:
        state='CORRECTION'
        ctype='TIMING_CORRECTION'
        vis='تصحيح: الاتجاه الجزئي يخالف الاتجاه العام لنفس الأفق الحاكم'
        score=90
        is_correction=True
    else:
        state='WITH_TREND'
        ctype='NONE'
        vis='مع الاتجاه: لا يوجد تصحيح لأن الاتجاه الجزئي يوافق الاتجاه العام لنفس الأفق الحاكم'
        score=55
        is_correction=False
    return {
        'ok': True,
        'version': 'V5.4.5',
        'public_name_ar': 'عقد التصحيح حسب سلطة التوقيت والاتجاه',
        'rule_ar': 'التصحيح لا يُحتسب من اختلاف أفقين مختلفين. يُحتسب فقط عندما يخالف الاتجاه الجزئي الاتجاه العام لنفس الأفق الذي تحكمه سلطة اليوم.',
        'day_authority': authority,
        'day_authority_ar': authority_ar,
        'weekday': wd_en,
        'weekday_ar': wd_ar,
        'authority_reason_ar': reason_ar,
        'overall_direction': overall_dir,
        'overall_direction_ar': overall_ar,
        'overall_direction_basis': 'صافي الاتجاه العام لنفس الأفق الحاكم',
        'partial_direction': partial_dir,
        'partial_direction_ar': partial_ar,
        'partial_direction_basis': 'تغير الاتجاه الجزئي/الأسبوعي لنفس الأفق الحاكم',
        'current_net': cur_net,
        'previous_net': prev_net,
        'partial_delta': delta,
        'is_correction': is_correction,
        'correction_state': state,
        'correction_type': ctype,
        'correction_visibility': vis,
        'score': score,
        'source_paths': [authority_path, delta_path],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
        'fallback_policy': 'إذا لم تتوفر بيانات نفس الأفق الحاكم تظهر غير مؤكد ولا يتم اختراع تصحيح.',
    }
'''
    marker='\ndef build_reference_levels_contract(base):\n'
    if marker not in s:
        raise SystemExit('REFERENCE_LEVELS_MARKER_NOT_FOUND')
    s=s.replace(marker, insert+marker, 1)

# Make timing correction authoritative before radar/scenario contracts are built.
needle="base['radar_nodes']=build_radar_nodes(base)"
replacement="""tc=build_timing_direction_correction_contract(sym, base, td)
    base['timing_correction_contract']=tc
    if isinstance(base.get('tdl_contract'), dict):
        base['tdl_contract']['authoritative_correction_contract']='timing_correction_contract'
        base['tdl_contract']['timing_correction_contract']=tc
    base['correction_type']=tc.get('correction_type')
    base['correction_visibility']=tc.get('correction_visibility')
    base['correction_state']=tc.get('correction_state')
    base['radar_nodes']=build_radar_nodes(base)"""
if replacement not in s:
    if needle not in s:
        raise SystemExit('RADAR_NODES_ASSIGNMENT_NOT_FOUND')
    s=s.replace(needle,replacement,1)

old="""if corr=='EXPLICIT': cs,cl,cscore='EXPLICIT','على المكشوف',90
    elif corr=='IMPLICIT': cs,cl,cscore='IMPLICIT','غير صريح',70
    elif corr=='NONE': cs,cl,cscore='NONE','لا يوجد تصحيح مؤكد',45
    elif corr: cs,cl,cscore=str(corr),str(base.get('correction_visibility') or corr),50
    else: cs,cl,cscore='NOT_PROVIDED','غير مرسل',None"""
new="""if corr in ('TIMING_CORRECTION','CORRECTION'):
        cs,cl,cscore='TIMING_CORRECTION',str(base.get('correction_visibility') or 'تصحيح'),90
    elif corr=='EXPLICIT': cs,cl,cscore='EXPLICIT','على المكشوف',90
    elif corr=='IMPLICIT': cs,cl,cscore='IMPLICIT','غير صريح',70
    elif corr in ('NONE','WITH_TREND','NO_CORRECTION'):
        cs,cl,cscore='NONE',str(base.get('correction_visibility') or 'مع الاتجاه: لا يوجد تصحيح'),45
    elif corr:
        cs,cl,cscore=str(corr),str(base.get('correction_visibility') or corr),50
    else:
        cs,cl,cscore='NOT_PROVIDED','غير مرسل',None"""
if old in s:
    s=s.replace(old,new,1)
else:
    s=re.sub(r"if corr=='EXPLICIT':.*?else: cs,cl,cscore='NOT_PROVIDED','غير مرسل',None", new, s, count=1, flags=re.S)

old2="correction_ok = correction_type in ('EXPLICIT','IMPLICIT')"
new2="correction_ok = correction_type in ('EXPLICIT','IMPLICIT','TIMING_CORRECTION','CORRECTION')"
if old2 in s:
    s=s.replace(old2,new2,1)

# Improve scenario explanation branch for no correction caused by with-trend timing.
old3="""elif not correction_ok:
        final_state = 'UNDER_MONITORING'
        final_state_ar = 'تحت المتابعة'
        main_reason_ar = 'لا يوجد تصحيح مؤكد من الطبقة الزمنية، لذلك تبقى القراءة تحت المتابعة رغم توفر بعض عناصر الدعم.'"""
new3="""elif not correction_ok:
        final_state = 'UNDER_MONITORING'
        final_state_ar = 'تحت المتابعة'
        tc = base.get('timing_correction_contract') or {}
        main_reason_ar = tc.get('correction_visibility') or 'لا يوجد تصحيح مؤكد من الطبقة الزمنية، لذلك تبقى القراءة تحت المتابعة رغم توفر بعض عناصر الدعم.'"""
if old3 in s:
    s=s.replace(old3,new3,1)

p.write_text(s,encoding='utf-8')
PY

python3 -m py_compile "$APP"
systemctl restart ndsp-v53-bridge.service
sleep 2

cat > "$OUT_DIR/ndsp_v545_timing_correction_audit.py" <<'PY'
#!/usr/bin/env python3
import json, urllib.request, argparse, sys, time
REQ=['timing_correction_contract','timing_correction_contract.day_authority','timing_correction_contract.overall_direction','timing_correction_contract.partial_direction','timing_correction_contract.correction_type','timing_correction_contract.correction_visibility','correction_type','correction_visibility','radar_nodes.tdl_correction.status','scenario_interpretation.gates.tdl_correction.status']
def gp(o,p):
    c=o
    for x in p.split('.'):
        if isinstance(c,dict) and x in c: c=c[x]
        else: return None
    return c
def fetch(url):
    with urllib.request.urlopen(url,timeout=12) as r: return json.loads(r.read().decode())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--symbols',default='BTCUSDT,ETHUSDT'); ap.add_argument('--base',default='https://my.ndsp.app'); args=ap.parse_args()
    final='PASS'
    for sym in [x.strip().upper() for x in args.symbols.split(',') if x.strip()]:
        d=fetch(f'{args.base}/api/decision/quality-contract-v53?symbol={sym}&_={int(time.time())}')
        print(f'SYMBOL={sym}')
        tc=d.get('timing_correction_contract') or {}
        print(f'{sym} DAY_AUTHORITY={tc.get("day_authority")} {tc.get("day_authority_ar")}')
        print(f'{sym} OVERALL={tc.get("overall_direction")} {tc.get("overall_direction_ar")} CURRENT_NET={tc.get("current_net")}')
        print(f'{sym} PARTIAL={tc.get("partial_direction")} {tc.get("partial_direction_ar")} DELTA={tc.get("partial_delta")}')
        print(f'{sym} IS_CORRECTION={tc.get("is_correction")} TYPE={tc.get("correction_type")} VISIBILITY={tc.get("correction_visibility")}')
        for p in REQ:
            v=gp(d,p); ok=v not in (None,'')
            print(f'{sym} PATH_{p}={ok} VALUE={str(v)[:140]}')
            if not ok: final='FAIL'
        if tc.get('overall_direction') in ('BULLISH','BEARISH') and tc.get('partial_direction') in ('BULLISH','BEARISH'):
            should = tc.get('overall_direction') != tc.get('partial_direction')
            if bool(tc.get('is_correction')) != should:
                final='FAIL'; print(f'{sym} RULE_MISMATCH=True EXPECTED_CORRECTION={should}')
            else:
                print(f'{sym} RULE_MATCH=True')
    print('FINAL_STATUS='+final)
    sys.exit(0 if final=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$OUT_DIR/ndsp_v545_timing_correction_audit.py"

log ""
log "== VERIFY V545 TIMING CORRECTION =="
for URL in \
  "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do
  OUT=/tmp/v545.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'timing_correction_contract|V5.4.5|TIMING_CORRECTION|WITH_TREND|correction_visibility' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
for sym in ['BTCUSDT','ETHUSDT']:
    d=json.loads(urllib.request.urlopen(f'https://my.ndsp.app/api/decision/quality-contract-v53?symbol={sym}',timeout=12).read().decode())
    tc=d.get('timing_correction_contract') or {}
    print('SYMBOL='+sym)
    print('TIMING_VERSION='+str(tc.get('version')))
    print('DAY_AUTHORITY='+str(tc.get('day_authority'))+' / '+str(tc.get('day_authority_ar')))
    print('OVERALL_DIRECTION='+str(tc.get('overall_direction'))+' / '+str(tc.get('overall_direction_ar')))
    print('PARTIAL_DIRECTION='+str(tc.get('partial_direction'))+' / '+str(tc.get('partial_direction_ar')))
    print('IS_CORRECTION='+str(tc.get('is_correction')))
    print('CORRECTION_TYPE='+str(d.get('correction_type')))
    print('CORRECTION_VISIBILITY='+str(d.get('correction_visibility')))
PY

log ""
log "== V545 RULE AUDIT =="
set +e
python3 "$OUT_DIR/ndsp_v545_timing_correction_audit.py" --symbols BTCUSDT,ETHUSDT --base https://my.ndsp.app | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "V545_AUDIT_EXIT_CODE=$RC"
log "FINAL_STATUS=NDSP_V545_TIMING_DIRECTION_CORRECTION_CONTRACT_DONE"
log "AUDIT_SCRIPT=$OUT_DIR/ndsp_v545_timing_correction_audit.py"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

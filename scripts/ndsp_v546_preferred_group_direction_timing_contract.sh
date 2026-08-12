#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APP="/opt/ndsp-v53-bridge/app.py"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v546-preferred-group-direction-$TS"
REPORT="$OUT_DIR/NDSP_V546_PREFERRED_GROUP_DIRECTION_TIMING_CONTRACT_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=BACKEND_PREFERRED_GROUP_DIRECTION_TIMING_CONTRACT"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] || { log "ERROR=APP_NOT_FOUND:$APP"; exit 1; }
cp -a "$APP" "$BACKUP/app.py.before_v546"

python3 - "$APP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

if 'def build_preferred_group_direction_timing_contract(sym):' not in s:
    insert = r'''

def _safe_float(x, default=0.0):
    try: return float(x)
    except Exception: return default

def _preferred_rows_from_tff(sym):
    _, needle = asset(sym)
    rows = []
    for f in tff_files():
        for r in read_rows(f):
            if len(r) > 18 and needle in str(r[0]).upper():
                am_long=_safe_float(r[11]); am_short=_safe_float(r[12])
                lf_long=_safe_float(r[14]); lf_short=_safe_float(r[15])
                other_long=_safe_float(r[17]) if len(r)>17 else 0.0
                other_short=_safe_float(r[18]) if len(r)>18 else 0.0
                dealer_long=_safe_float(r[8]); dealer_short=_safe_float(r[9])
                rows.append({
                    'file': str(f),
                    'market': r[0],
                    'report_date': r[2],
                    'preferred_long': am_long + other_long,
                    'preferred_short': am_short + other_short,
                    'preferred_net': (am_long + other_long) - (am_short + other_short),
                    'counter_long': lf_long + dealer_long,
                    'counter_short': lf_short + dealer_short,
                    'counter_net': (lf_long + dealer_long) - (lf_short + dealer_short),
                    'open_interest': _safe_float(r[7]) if len(r)>7 else None,
                })
    uniq={x['report_date']:x for x in rows if x.get('report_date')}
    return [uniq[k] for k in sorted(uniq.keys())]

def _pressure_from_longs_shorts(long_v, short_v):
    if long_v > short_v: return 'BULLISH','ضغط صاعد'
    if long_v < short_v: return 'BEARISH','ضغط هابط'
    return 'NEUTRAL','غير مؤكد'

def _partial_from_delta(long_delta, short_delta, net_delta):
    if long_delta > 0 and short_delta < 0:
        return 'BULLISH','ضغط صاعد','EXPLICIT_OPEN','أفق ممتد / قراءة على المكشوف','الشراء يزيد والبيع ينقص.'
    if long_delta < 0 and short_delta > 0:
        return 'BEARISH','ضغط هابط','EXPLICIT_OPEN','أفق ممتد / قراءة على المكشوف','الشراء ينقص والبيع يزيد.'
    if net_delta > 0:
        return 'BULLISH','ضغط صاعد','IMPLICIT_NARROW','أفق ضيق / قراءة غير صريحة','التغير الصافي يميل للصعود دون انكشاف كامل بين الشراء والبيع.'
    if net_delta < 0:
        return 'BEARISH','ضغط هابط','IMPLICIT_NARROW','أفق ضيق / قراءة غير صريحة','التغير الصافي يميل للهبوط دون انكشاف كامل بين الشراء والبيع.'
    return 'NEUTRAL','غير مؤكد','NEUTRAL','غير مؤكد','لا يوجد تغير كاف.'

def _time_control_v546(sym):
    wd=datetime.now(timezone.utc).weekday()
    ar=['الاثنين','الثلاثاء','الأربعاء','الخميس','الجمعة','السبت','الأحد'][wd]
    en=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][wd]
    s=(sym or '').upper()
    is_crypto=s.endswith('USDT') or s.startswith(('BTC','ETH','SOL'))
    if wd in (0,4):
        return 'PREFERRED_GROUP_TIME','وقت سيطرة مجموعة الاتجاه الأساسية',True,wd,en,ar,'الوقت مناسب لأن سلطة اليوم مع مجموعة الاتجاه الأساسية.'
    if wd in (1,2,3):
        return 'COUNTER_GROUP_TIME','وقت سيطرة مجموعة التذبذب المقابل',False,wd,en,ar,'الوقت غير مناسب لاتخاذ قرار لأن سلطة اليوم ليست مع مجموعة الاتجاه الأساسية.'
    if is_crypto:
        return 'COUNTER_GROUP_TIME','وقت سيطرة مجموعة التذبذب المقابل',False,wd,en,ar,'عطلة نهاية الأسبوع للأصول المستمرة ليست وقت مواءمة لمجموعة الاتجاه الأساسية.'
    return 'NO_ACTIVE_TIME','لا توجد سلطة توقيت نشطة',False,wd,en,ar,'لا توجد سلطة توقيت نشطة لهذا الأصل.'

def build_preferred_group_direction_timing_contract(sym):
    rows=_preferred_rows_from_tff(sym)
    time_group,time_group_ar,timing_ok,wd,en,ar,time_reason=_time_control_v546(sym)
    if len(rows)<2:
        return {
            'ok': False,
            'version': 'V5.4.6',
            'public_name_ar': 'عقد اتجاه مجموعة الأساس وتوقيت القرار',
            'source_family': 'TFF',
            'direction_basis_ar': 'مجموعة الاتجاه الأساسية + الآخرون حسب مصدر الأصل المفضل',
            'time_control_group': time_group,
            'time_control_group_ar': time_group_ar,
            'decision_timing_suitable': timing_ok,
            'correction_type': 'UNKNOWN',
            'correction_visibility': 'غير مؤكد: لا توجد تقارير كافية لحساب الاتجاه الجزئي والاتجاه العام.',
            'fallback_policy': 'إذا لم تتوفر تقارير كافية لا يتم اختراع اتجاه أو تصحيح.',
            'updated_at': utcnow(),
        }
    prev,cur=rows[-2],rows[-1]
    overall, overall_ar = _pressure_from_longs_shorts(cur['preferred_long'], cur['preferred_short'])
    long_delta = cur['preferred_long'] - prev['preferred_long']
    short_delta = cur['preferred_short'] - prev['preferred_short']
    net_delta = cur['preferred_net'] - prev['preferred_net']
    partial, partial_ar, signal_type, signal_type_ar, signal_reason_ar = _partial_from_delta(long_delta, short_delta, net_delta)
    if overall in ('BULLISH','BEARISH') and partial in ('BULLISH','BEARISH'):
        is_corr = overall != partial
        if is_corr:
            corr_type='TIMING_CORRECTION'
            corr_state='CORRECTION'
            corr_vis='تصحيح: الاتجاه الجزئي يخالف الاتجاه العام لمجموعة الاتجاه الأساسية.'
        else:
            corr_type='NONE'
            corr_state='WITH_TREND'
            corr_vis='مع الاتجاه: لا يوجد تصحيح لأن الاتجاه الجزئي يوافق الاتجاه العام لمجموعة الاتجاه الأساسية.'
    else:
        is_corr=False
        corr_type='UNKNOWN'
        corr_state='UNKNOWN'
        corr_vis='غير مؤكد: الاتجاه العام أو الجزئي غير واضح.'
    if not timing_ok:
        timing_state='NOT_SUITABLE'
        timing_label_ar='زمن القرار غير مناسب'
    else:
        timing_state='SUITABLE'
        timing_label_ar='زمن القرار مناسب'
    return {
        'ok': True,
        'version': 'V5.4.6',
        'public_name_ar': 'عقد اتجاه مجموعة الأساس وتوقيت القرار',
        'rule_ar': 'يتم استخراج الاتجاه من مجموعة الاتجاه الأساسية + الآخرون حسب مصدر الأصل المفضل. التصحيح يظهر فقط إذا خالف الاتجاه الجزئي/الأسبوعي الاتجاه العام لنفس المجموعة. ثم يتم فحص زمن السيطرة: إذا كانت السيطرة لمجموعة الاتجاه الأساسية فالزمن مناسب، وإذا كانت لمجموعة التذبذب المقابل فالزمن غير مناسب.',
        'source_family': 'TFF',
        'direction_basis_ar': 'مجموعة الاتجاه الأساسية + الآخرون',
        'direction_basis_en': 'Preferred direction group + others',
        'current_report': cur,
        'previous_report': prev,
        'overall_direction': overall,
        'overall_direction_ar': overall_ar,
        'overall_long': cur['preferred_long'],
        'overall_short': cur['preferred_short'],
        'overall_net': cur['preferred_net'],
        'partial_direction': partial,
        'partial_direction_ar': partial_ar,
        'partial_long_delta': long_delta,
        'partial_short_delta': short_delta,
        'partial_net_delta': net_delta,
        'signal_visibility_type': signal_type,
        'signal_visibility_ar': signal_type_ar,
        'signal_reason_ar': signal_reason_ar,
        'is_correction': is_corr,
        'correction_state': corr_state,
        'correction_type': corr_type,
        'correction_visibility': corr_vis,
        'time_control_group': time_group,
        'time_control_group_ar': time_group_ar,
        'weekday': en,
        'weekday_ar': ar,
        'decision_timing_suitable': timing_ok,
        'decision_timing_state': timing_state,
        'decision_timing_label_ar': timing_label_ar,
        'timing_reason_ar': time_reason,
        'source_paths': ['preferred_long','preferred_short','partial_long_delta','partial_short_delta','time_control_group'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
        'fallback_policy': 'إذا لم تتوفر بيانات مجموعة الاتجاه الأساسية أو توقيت السيطرة تظهر غير مؤكد ولا يتم اختراع تصحيح.',
    }
'''
    marker='\ndef build_reference_levels_contract(base):\n'
    if marker not in s:
        raise SystemExit('REFERENCE_LEVELS_MARKER_NOT_FOUND')
    s=s.replace(marker, insert+marker, 1)

needle="base['radar_nodes']=build_radar_nodes(base)"
replacement="""pd=build_preferred_group_direction_timing_contract(sym)
    base['preferred_direction_timing_contract']=pd
    base['timing_correction_contract']=pd
    if isinstance(base.get('tdl_contract'), dict):
        base['tdl_contract']['authoritative_direction_contract']='preferred_direction_timing_contract'
        base['tdl_contract']['preferred_direction_timing_contract']=pd
    base['correction_type']=pd.get('correction_type')
    base['correction_visibility']=pd.get('correction_visibility')
    base['correction_state']=pd.get('correction_state')
    base['decision_timing_suitable']=pd.get('decision_timing_suitable')
    base['decision_timing_state']=pd.get('decision_timing_state')
    base['decision_timing_label_ar']=pd.get('decision_timing_label_ar')
    base['radar_nodes']=build_radar_nodes(base)"""
if replacement not in s:
    if needle not in s:
        raise SystemExit('RADAR_NODES_ASSIGNMENT_NOT_FOUND')
    s=s.replace(needle,replacement,1)

# Add a timing gate to scenario interpretation if the previous script did not have it.
old="""hard_objection = advocate_status == 'HARD_OBJECTION' or (advocate_score is not None and float(advocate_score) >= 80)
    risk_critical = risk_status == 'CRITICAL' or (risk_score is not None and float(risk_score) >= 80)"""
new="""hard_objection = advocate_status == 'HARD_OBJECTION' or (advocate_score is not None and float(advocate_score) >= 80)
    risk_critical = risk_status == 'CRITICAL' or (risk_score is not None and float(risk_score) >= 80)
    timing_contract = base.get('preferred_direction_timing_contract') or base.get('timing_correction_contract') or {}
    timing_ok = timing_contract.get('decision_timing_suitable') is True"""
if old in s and 'timing_ok = timing_contract.get' not in s:
    s=s.replace(old,new,1)

old2="""if hard_objection:
        final_state = 'BLOCKED_FOR_REVIEW'
        final_state_ar = 'محجوب للمراجعة'
        main_reason_ar = 'محامي الشيطان يرفع اعتراضًا حاسمًا، لذلك تبقى القراءة محجوبة للمراجعة ولا تتحول إلى إشارة مفعلة.'"""
new2="""if hard_objection:
        final_state = 'BLOCKED_FOR_REVIEW'
        final_state_ar = 'محجوب للمراجعة'
        main_reason_ar = 'محامي الشيطان يرفع اعتراضًا حاسمًا، لذلك تبقى القراءة محجوبة للمراجعة ولا تتحول إلى إشارة مفعلة.'
    elif not timing_ok:
        final_state = 'TIME_NOT_SUITABLE'
        final_state_ar = 'زمن القرار غير مناسب'
        main_reason_ar = (timing_contract.get('timing_reason_ar') or 'زمن السيطرة الحالي غير موائم لمجموعة الاتجاه الأساسية.')"""
if old2 in s and "TIME_NOT_SUITABLE" not in s:
    s=s.replace(old2,new2,1)

old3="""'readiness': _gate(readiness_status, readiness_label, ready_ok, readiness_score, 'الجاهزية تلخص نضج القراءة.', 'radar_nodes.readiness'),"""
new3="""'readiness': _gate(readiness_status, readiness_label, ready_ok, readiness_score, 'الجاهزية تلخص نضج القراءة.', 'radar_nodes.readiness'),
        'decision_timing': _gate(timing_contract.get('decision_timing_state'), timing_contract.get('decision_timing_label_ar'), timing_ok, None, timing_contract.get('timing_reason_ar','زمن السيطرة الحالي'), 'preferred_direction_timing_contract'),"""
if old3 in s and "'decision_timing': _gate" not in s:
    s=s.replace(old3,new3,1)

old4="""'source_paths': ['radar_nodes','reference_levels_contract','correction_type','scenario','nmp_timeframes','risk_score','devil_advocate_score'],"""
new4="""'source_paths': ['preferred_direction_timing_contract','radar_nodes','reference_levels_contract','correction_type','scenario','nmp_timeframes','risk_score','devil_advocate_score'],"""
if old4 in s:
    s=s.replace(old4,new4,1)

p.write_text(s,encoding='utf-8')
PY

python3 -m py_compile "$APP"
systemctl restart ndsp-v53-bridge.service
sleep 2

cat > "$OUT_DIR/ndsp_v546_preferred_direction_audit.py" <<'PY'
#!/usr/bin/env python3
import json, urllib.request, argparse, sys, time
REQ=['preferred_direction_timing_contract','preferred_direction_timing_contract.overall_direction','preferred_direction_timing_contract.partial_direction','preferred_direction_timing_contract.signal_visibility_type','preferred_direction_timing_contract.is_correction','preferred_direction_timing_contract.time_control_group','preferred_direction_timing_contract.decision_timing_suitable','correction_type','correction_visibility','scenario_interpretation.gates.decision_timing.status']
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
        pd=d.get('preferred_direction_timing_contract') or {}
        print(f'SYMBOL={sym}')
        print(f'{sym} VERSION={pd.get("version")}')
        print(f'{sym} BASIS={pd.get("direction_basis_ar")}')
        print(f'{sym} OVERALL={pd.get("overall_direction")} {pd.get("overall_direction_ar")} LONG={pd.get("overall_long")} SHORT={pd.get("overall_short")} NET={pd.get("overall_net")}')
        print(f'{sym} PARTIAL={pd.get("partial_direction")} {pd.get("partial_direction_ar")} LONG_DELTA={pd.get("partial_long_delta")} SHORT_DELTA={pd.get("partial_short_delta")} NET_DELTA={pd.get("partial_net_delta")}')
        print(f'{sym} SIGNAL_VISIBILITY={pd.get("signal_visibility_type")} {pd.get("signal_visibility_ar")}')
        print(f'{sym} IS_CORRECTION={pd.get("is_correction")} TYPE={pd.get("correction_type")} VISIBILITY={pd.get("correction_visibility")}')
        print(f'{sym} TIME_CONTROL={pd.get("time_control_group")} {pd.get("time_control_group_ar")} SUITABLE={pd.get("decision_timing_suitable")}')
        for p in REQ:
            v=gp(d,p); ok=v is not None and v!=''
            print(f'{sym} PATH_{p}={ok} VALUE={str(v)[:160]}')
            if not ok: final='FAIL'
        ov=pd.get('overall_direction'); pa=pd.get('partial_direction')
        if ov in ('BULLISH','BEARISH') and pa in ('BULLISH','BEARISH'):
            should=(ov!=pa)
            print(f'{sym} RULE_EXPECTED_CORRECTION={should}')
            if bool(pd.get('is_correction')) != should:
                print(f'{sym} RULE_MISMATCH=True')
                final='FAIL'
            else:
                print(f'{sym} RULE_MATCH=True')
    print('FINAL_STATUS='+final)
    sys.exit(0 if final=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$OUT_DIR/ndsp_v546_preferred_direction_audit.py"

log ""
log "== VERIFY V546 CONTRACT =="
for URL in \
  "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do
  OUT=/tmp/v546.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'preferred_direction_timing_contract|V5.4.6|decision_timing_suitable|signal_visibility_type' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
for sym in ['BTCUSDT','ETHUSDT']:
    d=json.loads(urllib.request.urlopen(f'https://my.ndsp.app/api/decision/quality-contract-v53?symbol={sym}',timeout=12).read().decode())
    pd=d.get('preferred_direction_timing_contract') or {}
    print('SYMBOL='+sym)
    print('PREFERRED_VERSION='+str(pd.get('version')))
    print('OVERALL_DIRECTION='+str(pd.get('overall_direction'))+' / '+str(pd.get('overall_direction_ar')))
    print('PARTIAL_DIRECTION='+str(pd.get('partial_direction'))+' / '+str(pd.get('partial_direction_ar')))
    print('SIGNAL_VISIBILITY='+str(pd.get('signal_visibility_type'))+' / '+str(pd.get('signal_visibility_ar')))
    print('IS_CORRECTION='+str(pd.get('is_correction')))
    print('CORRECTION_TYPE='+str(d.get('correction_type')))
    print('CORRECTION_VISIBILITY='+str(d.get('correction_visibility')))
    print('TIME_CONTROL='+str(pd.get('time_control_group'))+' / '+str(pd.get('time_control_group_ar')))
    print('DECISION_TIMING_SUITABLE='+str(pd.get('decision_timing_suitable')))
PY

log ""
log "== V546 PREFERRED DIRECTION AUDIT =="
set +e
python3 "$OUT_DIR/ndsp_v546_preferred_direction_audit.py" --symbols BTCUSDT,ETHUSDT --base https://my.ndsp.app | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "V546_AUDIT_EXIT_CODE=$RC"
log "FINAL_STATUS=NDSP_V546_PREFERRED_GROUP_DIRECTION_TIMING_CONTRACT_DONE"
log "AUDIT_SCRIPT=$OUT_DIR/ndsp_v546_preferred_direction_audit.py"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

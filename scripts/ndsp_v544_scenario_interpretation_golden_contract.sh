#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APP="/opt/ndsp-v53-bridge/app.py"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v544-scenario-interpretation-$TS"
REPORT="$OUT_DIR/NDSP_V544_SCENARIO_INTERPRETATION_GOLDEN_CONTRACT_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=BACKEND_SCENARIO_INTERPRETATION_AND_GOLDEN_SIGNAL_CONTRACT"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] || { log "ERROR=APP_NOT_FOUND:$APP"; exit 1; }
cp -a "$APP" "$BACKUP/app.py.before_v544"

python3 - "$APP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')
if 'def build_scenario_interpretation_contract(base):' not in s:
    insert = r'''

def _public_level_status(v):
    if v is None or str(v).strip()=='' or str(v).strip()=='—':
        return 'MISSING','غير موصول',None
    return 'CONNECTED','متاح',v

def build_reference_levels_contract(base):
    sc = base.get('scenario') if isinstance(base.get('scenario'), dict) else {}
    fields = {
        'activation': ('scenario_activation_level','مستوى التفعيل'),
        'arrival': ('scenario_arrival_level','مستوى الوصول'),
        'review': ('scenario_review_zone','منطقة المراجعة'),
        'invalidation': ('scenario_invalidation_level','مستوى الإلغاء'),
    }
    levels = {}
    ok_count = 0
    for k,(src,label) in fields.items():
        val = sc.get(src) or base.get(src)
        st,ar,_ = _public_level_status(val)
        if st == 'CONNECTED': ok_count += 1
        levels[k] = {
            'key': k,
            'label_ar': label,
            'value': val,
            'status': st,
            'status_ar': ar,
            'source_path': 'scenario.' + src,
            'source_endpoint': '/api/decision/quality-contract-v53',
            'source_service': 'ndsp-v53-bridge',
            'contract_mode': 'BACKEND_DIRECT',
            'updated_at': utcnow(),
            'fallback_policy': 'إذا غاب المستوى يظهر غير موصول ولا يتم اختراع مستوى.',
        }
    return {
        'ok': ok_count == 4,
        'status': 'CONNECTED' if ok_count == 4 else 'PARTIAL',
        'status_ar': 'مكتملة' if ok_count == 4 else 'غير مكتملة',
        'connected_count': ok_count,
        'total_required': 4,
        'levels': levels,
        'source_layer': 'Scenario Reference Levels',
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'updated_at': utcnow(),
    }

def _node_score(base, name):
    n=(base.get('radar_nodes') or {}).get(name) or {}
    return n.get('score'), n.get('status'), n.get('label_ar')

def _gate(status, label, passed, score=None, reason_ar='', source_path=''):
    return {
        'status': status,
        'label_ar': label,
        'passed': bool(passed),
        'score': score,
        'reason_ar': reason_ar,
        'source_path': source_path,
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'updated_at': utcnow(),
    }

def build_scenario_interpretation_contract(base):
    rn = base.get('radar_nodes') or {}
    ref = base.get('reference_levels_contract') or build_reference_levels_contract(base)
    sc = base.get('scenario') if isinstance(base.get('scenario'), dict) else {}

    readiness_score, readiness_status, readiness_label = _node_score(base, 'readiness')
    levels_score, levels_status, levels_label = _node_score(base, 'levels')
    nmp_score, nmp_status, nmp_label = _node_score(base, 'nmp_check')
    risk_score, risk_status, risk_label = _node_score(base, 'risk')
    advocate_score, advocate_status, advocate_label = _node_score(base, 'devil')
    corr_score, corr_status, corr_label = _node_score(base, 'tdl_correction')
    horizon_score, horizon_status, horizon_label = _node_score(base, 'horizon')

    correction_type = base.get('correction_type')
    correction_visibility = base.get('correction_visibility')
    direction_context = sc.get('scenario_directional_context') or base.get('directional_bias') or (base.get('allowed_public_outputs') or {}).get('directional_bias') or 'غير مؤكد'

    hard_objection = advocate_status == 'HARD_OBJECTION' or (advocate_score is not None and float(advocate_score) >= 80)
    risk_critical = risk_status == 'CRITICAL' or (risk_score is not None and float(risk_score) >= 80)
    levels_ok = ref.get('ok') is True
    nmp_ok = nmp_status == 'CONNECTED' and (nmp_score is not None and float(nmp_score) >= 60)
    correction_ok = correction_type in ('EXPLICIT','IMPLICIT')
    ready_ok = readiness_status == 'READY' or (readiness_score is not None and float(readiness_score) >= 80)

    if hard_objection:
        final_state = 'BLOCKED_FOR_REVIEW'
        final_state_ar = 'محجوب للمراجعة'
        main_reason_ar = 'محامي الشيطان يرفع اعتراضًا حاسمًا، لذلك تبقى القراءة محجوبة للمراجعة ولا تتحول إلى إشارة مفعلة.'
    elif not correction_ok:
        final_state = 'UNDER_MONITORING'
        final_state_ar = 'تحت المتابعة'
        main_reason_ar = 'لا يوجد تصحيح مؤكد من الطبقة الزمنية، لذلك تبقى القراءة تحت المتابعة رغم توفر بعض عناصر الدعم.'
    elif not nmp_ok:
        final_state = 'NEEDS_NMP_CONFIRMATION'
        final_state_ar = 'يحتاج تحقق NMP'
        main_reason_ar = 'القراءة تحتاج تحقق NMP قبل رفع مستوى الثقة.'
    elif risk_critical:
        final_state = 'HIGH_CAUTION'
        final_state_ar = 'متابعة بحذر شديد'
        main_reason_ar = 'حالة المخاطر مرتفعة، لذلك تبقى القراءة في وضع حذر شديد.'
    elif ready_ok and levels_ok:
        final_state = 'COMPLETED_READING'
        final_state_ar = 'قراءة مكتملة'
        main_reason_ar = 'الجاهزية والمستويات وNMP والتصحيح متوافقة دون اعتراض حاسم.'
    else:
        final_state = 'CAUTION_READING'
        final_state_ar = 'قراءة حذرة'
        main_reason_ar = 'القراءة تملك عناصر دعم لكنها لم تصل إلى اكتمال كافٍ.'

    golden_active = correction_ok and nmp_ok and levels_ok and not hard_objection and not risk_critical
    enhanced_active = golden_active and ready_ok and horizon_status in ('READY','CONNECTED','CAUTION') and (readiness_score or 0) >= 80 and (nmp_score or 0) >= 80 and (levels_score or 0) >= 70 and (risk_score or 100) <= 65 and (advocate_score or 100) <= 65

    if enhanced_active:
        golden_status, golden_label, golden_score = 'ACTIVE', 'مفعلة', min(100, int((readiness_score+nmp_score+levels_score+corr_score)/4))
        enhanced_status, enhanced_label, enhanced_score = 'ACTIVE', 'مفعلة بقوة', golden_score
    elif golden_active:
        golden_status, golden_label, golden_score = 'WATCHING', 'تحت المراقبة المتقدمة', min(90, int(((readiness_score or 60)+(nmp_score or 60)+(levels_score or 60)+(corr_score or 60))/4))
        enhanced_status, enhanced_label, enhanced_score = 'NOT_ACTIVE', 'غير مفعلة', None
    else:
        golden_status, golden_label, golden_score = 'NOT_ACTIVE', 'غير مفعلة', None
        enhanced_status, enhanced_label, enhanced_score = 'NOT_ACTIVE', 'غير مفعلة', None

    gates = {
        'tdl_correction': _gate(correction_type or 'NOT_PROVIDED', correction_visibility or 'غير مرسل', correction_ok, corr_score, 'التصحيح الزمني شرط أساسي لرفع الثقة.', 'correction_type'),
        'reference_levels': _gate(ref.get('status'), ref.get('status_ar'), levels_ok, levels_score, 'المستويات المرجعية يجب أن تكون مكتملة.', 'reference_levels_contract'),
        'nmp': _gate(nmp_status, nmp_label, nmp_ok, nmp_score, 'NMP نقطة تحقق إضافية ولا يتم اختراعها.', 'radar_nodes.nmp_check'),
        'risk': _gate(risk_status, risk_label, not risk_critical, risk_score, 'المخاطر تقييم عكسي: الأقل أفضل.', 'radar_nodes.risk'),
        'advocate': _gate(advocate_status, advocate_label, not hard_objection, advocate_score, 'محامي الشيطان هو بوابة الاعتراض الحاسم.', 'radar_nodes.devil'),
        'readiness': _gate(readiness_status, readiness_label, ready_ok, readiness_score, 'الجاهزية تلخص نضج القراءة.', 'radar_nodes.readiness'),
    }

    explanation_ar = f'{main_reason_ar} السياق الحالي: {direction_context}. حالة المخاطر: {risk_label}. محامي الشيطان: {advocate_label}. NMP: {nmp_label}. المستويات المرجعية: {ref.get("status_ar")}.'
    explanation_en = f'{main_reason_ar} Current context: {direction_context}. Risk state: {risk_label}. Advocate layer: {advocate_label}. NMP: {nmp_label}. Reference levels: {ref.get("status_ar")}.'

    golden = {
        'public_name_ar': 'إشارة نواف الذهبية',
        'public_name_en': 'Nawaf Golden Signal',
        'status': golden_status,
        'label_ar': golden_label,
        'score': golden_score,
        'reason_ar': 'تتطلب توافق التصحيح والمستويات وNMP وعدم وجود اعتراض حاسم أو خطر حرج.',
        'not_financial_advice': True,
        'not_execution_order': True,
        'source_paths': ['correction_type','reference_levels_contract','radar_nodes.nmp_check','radar_nodes.risk','radar_nodes.devil'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
    }
    enhanced = {
        'public_name_ar': 'إشارة نواف الذهبية المعززة',
        'public_name_en': 'Enhanced Nawaf Golden Signal',
        'status': enhanced_status,
        'label_ar': enhanced_label,
        'score': enhanced_score,
        'reason_ar': 'تتطلب شروط الإشارة الذهبية مع جاهزية أعلى ومخاطر منخفضة واعتراض غير حاسم.',
        'not_financial_advice': True,
        'not_execution_order': True,
        'source_paths': ['golden_signal','radar_nodes.readiness','radar_nodes.horizon','radar_nodes.risk','radar_nodes.devil'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
    }
    return {
        'ok': True,
        'version': 'V5.4.4',
        'public_name_ar': 'مفسر سيناريو القرار',
        'public_name_en': 'Decision Scenario Interpreter',
        'contract_mode': 'BACKEND_DERIVED',
        'final_state': final_state,
        'final_state_ar': final_state_ar,
        'direction_context': direction_context,
        'explanation_ar': explanation_ar,
        'explanation_en': explanation_en,
        'normal_user_summary_ar': f'الخلاصة: {final_state_ar}. {main_reason_ar}',
        'advanced_summary_ar': explanation_ar,
        'gates': gates,
        'golden_signal': golden,
        'enhanced_golden_signal': enhanced,
        'source_paths': ['radar_nodes','reference_levels_contract','correction_type','scenario','nmp_timeframes','risk_score','devil_advocate_score'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'updated_at': utcnow(),
        'fallback_policy': 'إذا غاب أي مصدر مؤثر يتم تخفيض الحالة إلى تحت المتابعة أو غير موصول ولا يتم اختراع نتيجة.',
    }
'''
    marker='\ndef contract(sym):\n'
    if marker not in s:
        raise SystemExit('CONTRACT_FUNCTION_MARKER_NOT_FOUND')
    s=s.replace(marker, insert+marker, 1)
old="base['radar_nodes']=build_radar_nodes(base)"
new="""base['radar_nodes']=build_radar_nodes(base)
    base['reference_levels_contract']=build_reference_levels_contract(base)
    base['scenario_interpretation']=build_scenario_interpretation_contract(base)
    base['golden_signal']=base['scenario_interpretation']['golden_signal']
    base['enhanced_golden_signal']=base['scenario_interpretation']['enhanced_golden_signal']
    base['decision_explanation_contract']={
        'ok': True,
        'version': 'V5.4.4',
        'purpose': 'Explain the decision scenario from TDL correction, reference levels, NMP, risk, advocate layer, and golden signal states.',
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'source_paths': ['scenario_interpretation','reference_levels_contract','golden_signal','enhanced_golden_signal','radar_nodes'],
        'not_financial_advice': True,
        'not_execution_order': True,
        'updated_at': utcnow(),
    }"""
if new in s:
    pass
elif old in s:
    s=s.replace(old,new,1)
else:
    raise SystemExit('RADAR_NODES_ASSIGNMENT_NOT_FOUND')
p.write_text(s,encoding='utf-8')
PY

python3 -m py_compile "$APP"
systemctl restart ndsp-v53-bridge.service
sleep 2

cat > "$OUT_DIR/ndsp_v544_scenario_contract_audit.py" <<'PY'
#!/usr/bin/env python3
import json, urllib.request, argparse, sys, time
REQUIRED=['scenario_interpretation','reference_levels_contract','golden_signal','enhanced_golden_signal','decision_explanation_contract']
SUB=['scenario_interpretation.final_state','scenario_interpretation.explanation_ar','scenario_interpretation.gates.tdl_correction','scenario_interpretation.gates.nmp','scenario_interpretation.gates.risk','scenario_interpretation.gates.advocate','golden_signal.status','enhanced_golden_signal.status']
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
        for k in REQUIRED:
            ok=isinstance(d.get(k),dict)
            print(f'{sym} REQUIRED_{k}={ok}')
            if not ok: final='FAIL'
        for p in SUB:
            v=gp(d,p); ok=v not in (None,'')
            print(f'{sym} PATH_{p}={ok} VALUE={str(v)[:120]}')
            if not ok: final='FAIL'
    print('FINAL_STATUS='+final)
    sys.exit(0 if final=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$OUT_DIR/ndsp_v544_scenario_contract_audit.py"

log ""
log "== VERIFY V544 CONTRACT =="
for URL in \
  "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do
  OUT=/tmp/v544.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'scenario_interpretation|golden_signal|enhanced_golden_signal|reference_levels_contract|V5.4.4' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
d=json.loads(urllib.request.urlopen('https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT',timeout=12).read().decode())
si=d.get('scenario_interpretation') or {}
print('HAS_SCENARIO_INTERPRETATION='+str(bool(si)))
print('SCENARIO_VERSION='+str(si.get('version')))
print('SCENARIO_FINAL_STATE='+str(si.get('final_state')))
print('SCENARIO_FINAL_STATE_AR='+str(si.get('final_state_ar')))
print('GOLDEN_SIGNAL_STATUS='+str((d.get('golden_signal') or {}).get('status')))
print('ENHANCED_GOLDEN_SIGNAL_STATUS='+str((d.get('enhanced_golden_signal') or {}).get('status')))
print('REFERENCE_LEVELS_STATUS='+str((d.get('reference_levels_contract') or {}).get('status')))
print('HAS_DECISION_EXPLANATION_CONTRACT='+str('decision_explanation_contract' in d))
PY

log ""
log "== V544 SCENARIO AUDIT =="
set +e
python3 "$OUT_DIR/ndsp_v544_scenario_contract_audit.py" --symbols BTCUSDT,ETHUSDT --base https://my.ndsp.app | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "V544_AUDIT_EXIT_CODE=$RC"
log "FINAL_STATUS=NDSP_V544_SCENARIO_INTERPRETATION_GOLDEN_CONTRACT_DONE"
log "AUDIT_SCRIPT=$OUT_DIR/ndsp_v544_scenario_contract_audit.py"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
APP="/opt/ndsp-v53-bridge/app.py"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
BACKUP="$HOME_DIR/ndsp_launch_backups/ndsp-v547-decision-profile-direction-$TS"
REPORT="$OUT_DIR/NDSP_V547_DECISION_PROFILE_DIRECTION_CONTRACT_$TS.md"
mkdir -p "$OUT_DIR" "$BACKUP"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=BACKEND_DECISION_PROFILE_DIRECTION_CONTRACT"
[ "$(id -u)" = 0 ] || { log "ERROR=RUN_WITH_SUDO"; exit 1; }
[ -f "$APP" ] || { log "ERROR=APP_NOT_FOUND:$APP"; exit 1; }
cp -a "$APP" "$BACKUP/app.py.before_v547"

python3 - "$APP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text(encoding='utf-8')

if 'def build_decision_profile_direction_contract(base):' not in s:
    insert = r'''

def build_decision_profile_direction_contract(base):
    pd = base.get('preferred_direction_timing_contract') or base.get('timing_correction_contract') or {}
    overall = pd.get('overall_direction')
    overall_ar = pd.get('overall_direction_ar')
    partial = pd.get('partial_direction')
    partial_ar = pd.get('partial_direction_ar')
    is_corr = pd.get('is_correction')
    corr_type = pd.get('correction_type')
    corr_vis = pd.get('correction_visibility')
    timing_ok = pd.get('decision_timing_suitable') is True
    timing_state = pd.get('decision_timing_state')
    timing_label = pd.get('decision_timing_label_ar')
    timing_reason = pd.get('timing_reason_ar')

    investor_relation = 'CORRECTION_AGAINST_OVERALL' if is_corr else 'WITH_OVERALL'
    speculator_relation = 'AGAINST_OVERALL' if is_corr else 'WITH_OVERALL'

    investor = {
        'profile_id': 'investor_view',
        'public_name_ar': 'نمط المستثمر',
        'public_name_en': 'Investor View',
        'controlling_direction_type': 'OVERALL_DIRECTION',
        'controlling_direction_type_ar': 'الاتجاه العام / الكلي',
        'controlling_direction': overall,
        'controlling_direction_ar': overall_ar,
        'comparison_direction_type': 'PARTIAL_OR_WEEKLY_DIRECTION',
        'comparison_direction_type_ar': 'الاتجاه الجزئي / الأسبوعي',
        'comparison_direction': partial,
        'comparison_direction_ar': partial_ar,
        'correction_relation': investor_relation,
        'is_correction': bool(is_corr),
        'correction_type': corr_type,
        'correction_visibility': corr_vis,
        'direction_summary_ar': ('الاتجاه المعتمد للمستثمر هو الاتجاه العام. الاتجاه الجزئي يمثل تصحيحًا داخل الاتجاه العام.' if is_corr else 'الاتجاه المعتمد للمستثمر هو الاتجاه العام، والاتجاه الجزئي موافق له.'),
        'decision_timing_suitable': timing_ok,
        'decision_timing_state': timing_state,
        'decision_timing_label_ar': timing_label,
        'timing_reason_ar': timing_reason,
        'not_financial_advice': True,
        'not_execution_order': True,
        'source_paths': ['preferred_direction_timing_contract.overall_direction','preferred_direction_timing_contract.partial_direction','preferred_direction_timing_contract.is_correction'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
    }
    speculator = {
        'profile_id': 'speculator_view',
        'public_name_ar': 'النمط التكتيكي',
        'public_name_en': 'Tactical View',
        'controlling_direction_type': 'PARTIAL_OR_WEEKLY_DIRECTION',
        'controlling_direction_type_ar': 'الاتجاه الجزئي / الأسبوعي',
        'controlling_direction': partial,
        'controlling_direction_ar': partial_ar,
        'comparison_direction_type': 'OVERALL_DIRECTION',
        'comparison_direction_type_ar': 'الاتجاه العام / الكلي',
        'comparison_direction': overall,
        'comparison_direction_ar': overall_ar,
        'correction_relation': speculator_relation,
        'is_correction_against_overall': bool(is_corr),
        'correction_type': corr_type,
        'correction_visibility': corr_vis,
        'direction_summary_ar': ('الاتجاه المعتمد للنمط التكتيكي هو الاتجاه الجزئي/الأسبوعي، لكنه يخالف الاتجاه العام لذلك يعد حركة تصحيحية.' if is_corr else 'الاتجاه المعتمد للنمط التكتيكي هو الاتجاه الجزئي/الأسبوعي، وهو موافق للاتجاه العام.'),
        'decision_timing_suitable': timing_ok,
        'decision_timing_state': timing_state,
        'decision_timing_label_ar': timing_label,
        'timing_reason_ar': timing_reason,
        'not_financial_advice': True,
        'not_execution_order': True,
        'source_paths': ['preferred_direction_timing_contract.partial_direction','preferred_direction_timing_contract.overall_direction','preferred_direction_timing_contract.decision_timing_suitable'],
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
    }
    if overall in ('BULLISH','BEARISH') and partial in ('BULLISH','BEARISH'):
        divergence_state = 'DIVERGENT' if overall != partial else 'ALIGNED'
        divergence_ar = 'مختلفان' if overall != partial else 'متوافقان'
    else:
        divergence_state = 'UNKNOWN'
        divergence_ar = 'غير مؤكد'
    return {
        'ok': True,
        'version': 'V5.4.7',
        'public_name_ar': 'عقد اتجاه القرار حسب النمط',
        'public_name_en': 'Decision Profile Direction Contract',
        'rule_ar': 'يعرض القرار باتجاهين منظمين: المستثمر يعتمد الاتجاه العام، والنمط التكتيكي يعتمد الاتجاه الجزئي/الأسبوعي. التصحيح هو اختلاف الجزئي عن العام، وليس اتجاهًا واحدًا مطلقًا لكل المستخدمين.',
        'investor_view': investor,
        'tactical_view': speculator,
        'direction_alignment': divergence_state,
        'direction_alignment_ar': divergence_ar,
        'source_endpoint': '/api/decision/quality-contract-v53',
        'source_service': 'ndsp-v53-bridge',
        'source_paths': ['preferred_direction_timing_contract'],
        'contract_mode': 'BACKEND_DERIVED',
        'updated_at': utcnow(),
        'fallback_policy': 'إذا غاب أحد الاتجاهين لا يتم اختراع اتجاه للنمط، وتظهر الحالة غير مؤكدة.',
    }
'''
    marker='\ndef build_reference_levels_contract(base):\n'
    if marker not in s:
        raise SystemExit('REFERENCE_LEVELS_MARKER_NOT_FOUND')
    s=s.replace(marker, insert+marker, 1)

# Inject after preferred direction contract is assigned.
needle="base['decision_timing_label_ar']=pd.get('decision_timing_label_ar')"
add="""base['decision_timing_label_ar']=pd.get('decision_timing_label_ar')
    base['decision_profile_direction_contract']=build_decision_profile_direction_contract(base)
    base['investor_direction_view']=base['decision_profile_direction_contract']['investor_view']
    base['tactical_direction_view']=base['decision_profile_direction_contract']['tactical_view']"""
if add not in s:
    if needle not in s:
        raise SystemExit('DECISION_TIMING_LABEL_MARKER_NOT_FOUND')
    s=s.replace(needle,add,1)

# Add profile contract to decision explanation contract source paths when present.
old="""'source_paths': ['scenario_interpretation','reference_levels_contract','golden_signal','enhanced_golden_signal','radar_nodes'],"""
new="""'source_paths': ['decision_profile_direction_contract','scenario_interpretation','reference_levels_contract','golden_signal','enhanced_golden_signal','radar_nodes'],"""
if old in s:
    s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
PY

python3 -m py_compile "$APP"
systemctl restart ndsp-v53-bridge.service
sleep 2

cat > "$OUT_DIR/ndsp_v547_decision_profile_direction_audit.py" <<'PY'
#!/usr/bin/env python3
import json, urllib.request, argparse, sys, time
REQ=['decision_profile_direction_contract','decision_profile_direction_contract.investor_view.controlling_direction_type','decision_profile_direction_contract.investor_view.controlling_direction','decision_profile_direction_contract.tactical_view.controlling_direction_type','decision_profile_direction_contract.tactical_view.controlling_direction','investor_direction_view','tactical_direction_view','preferred_direction_timing_contract.overall_direction','preferred_direction_timing_contract.partial_direction']
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
        c=d.get('decision_profile_direction_contract') or {}
        inv=c.get('investor_view') or {}
        tac=c.get('tactical_view') or {}
        print(f'SYMBOL={sym}')
        print(f'{sym} PROFILE_VERSION={c.get("version")}')
        print(f'{sym} INVESTOR_CONTROLLING={inv.get("controlling_direction_type")} {inv.get("controlling_direction")} {inv.get("controlling_direction_ar")}')
        print(f'{sym} INVESTOR_COMPARISON={inv.get("comparison_direction_type")} {inv.get("comparison_direction")} {inv.get("comparison_direction_ar")}')
        print(f'{sym} TACTICAL_CONTROLLING={tac.get("controlling_direction_type")} {tac.get("controlling_direction")} {tac.get("controlling_direction_ar")}')
        print(f'{sym} TACTICAL_COMPARISON={tac.get("comparison_direction_type")} {tac.get("comparison_direction")} {tac.get("comparison_direction_ar")}')
        print(f'{sym} ALIGNMENT={c.get("direction_alignment")} {c.get("direction_alignment_ar")}')
        for p in REQ:
            v=gp(d,p); ok=v is not None and v!=''
            print(f'{sym} PATH_{p}={ok} VALUE={str(v)[:160]}')
            if not ok: final='FAIL'
        if inv.get('controlling_direction_type')!='OVERALL_DIRECTION': final='FAIL'; print(f'{sym} INVESTOR_RULE_MISMATCH=True')
        if tac.get('controlling_direction_type')!='PARTIAL_OR_WEEKLY_DIRECTION': final='FAIL'; print(f'{sym} TACTICAL_RULE_MISMATCH=True')
        if inv.get('controlling_direction') != gp(d,'preferred_direction_timing_contract.overall_direction'):
            final='FAIL'; print(f'{sym} INVESTOR_DIRECTION_SOURCE_MISMATCH=True')
        if tac.get('controlling_direction') != gp(d,'preferred_direction_timing_contract.partial_direction'):
            final='FAIL'; print(f'{sym} TACTICAL_DIRECTION_SOURCE_MISMATCH=True')
    print('FINAL_STATUS='+final)
    sys.exit(0 if final=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$OUT_DIR/ndsp_v547_decision_profile_direction_audit.py"

log ""
log "== VERIFY V547 PROFILE CONTRACT =="
for URL in \
  "http://127.0.0.1:9084/api/decision/quality-contract-v53?symbol=BTCUSDT" \
  "https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"; do
  OUT=/tmp/v547.out
  CODE="$(curl -skL -o "$OUT" -w "%{http_code}" "$URL" || echo 000)"
  SIZE="$(wc -c < "$OUT" 2>/dev/null || echo 0)"
  MARKER="$(grep -Eo 'decision_profile_direction_contract|investor_direction_view|tactical_direction_view|V5.4.7' "$OUT" | head -1 || true)"
  log "$URL HTTP=$CODE SIZE=$SIZE MARKER=${MARKER:-NONE}"
done
python3 - <<'PY' | tee -a "$REPORT"
import json,urllib.request
for sym in ['BTCUSDT','ETHUSDT']:
    d=json.loads(urllib.request.urlopen(f'https://my.ndsp.app/api/decision/quality-contract-v53?symbol={sym}',timeout=12).read().decode())
    c=d.get('decision_profile_direction_contract') or {}
    inv=c.get('investor_view') or {}; tac=c.get('tactical_view') or {}
    print('SYMBOL='+sym)
    print('PROFILE_VERSION='+str(c.get('version')))
    print('INVESTOR_DIRECTION='+str(inv.get('controlling_direction_type'))+' / '+str(inv.get('controlling_direction_ar')))
    print('TACTICAL_DIRECTION='+str(tac.get('controlling_direction_type'))+' / '+str(tac.get('controlling_direction_ar')))
    print('DIRECTION_ALIGNMENT='+str(c.get('direction_alignment'))+' / '+str(c.get('direction_alignment_ar')))
PY

log ""
log "== V547 PROFILE AUDIT =="
set +e
python3 "$OUT_DIR/ndsp_v547_decision_profile_direction_audit.py" --symbols BTCUSDT,ETHUSDT --base https://my.ndsp.app | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "V547_AUDIT_EXIT_CODE=$RC"
log "FINAL_STATUS=NDSP_V547_DECISION_PROFILE_DIRECTION_CONTRACT_DONE"
log "AUDIT_SCRIPT=$OUT_DIR/ndsp_v547_decision_profile_direction_audit.py"
log "URL_CONTRACT=https://my.ndsp.app/api/decision/quality-contract-v53?symbol=BTCUSDT"
log "REPORT=$REPORT"

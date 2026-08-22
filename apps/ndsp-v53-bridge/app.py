#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re, time, urllib.request, urllib.parse
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone

PORT=9084
DATA=Path('/home/nawaf511/.local/share/ndsp/runtime-data/backend/data/raw_cot')

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
    return {'tdl_state':'CONNECTED','tdl_bias':bias,'correction_type':typ,'correction_visibility':vis,'extended_net_delta':round(de,2),'narrow_net_delta':round(dn,2),'previous_report':p,'current_report':c,'source_status':'RAW_COT_DERIVED','source_endpoint':'/home/nawaf511/.local/share/ndsp/runtime-data/backend/data/raw_cot/current_tff_futures_only_FinFutWk.txt','source_service':'ndsp-v53-bridge','updated_at':utcnow()}

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


def _public_level_status(v):
    if v is None or str(v).strip()=='' or str(v).strip()=='—':
        return 'MISSING','غير موصول',None
    return 'CONNECTED','متاح',v


def _safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

def _preferred_rows_from_tff(sym):
    """
    Internal backend calculation only.
    Public UI must not expose internal source/faction names.
    """
    _, needle = asset(sym)
    rows = []
    for f in tff_files():
        for r in read_rows(f):
            if len(r) > 18 and needle in str(r[0]).upper():
                am_long = _safe_float(r[11])
                am_short = _safe_float(r[12])
                lf_long = _safe_float(r[14])
                lf_short = _safe_float(r[15])
                other_long = _safe_float(r[17]) if len(r) > 17 else 0.0
                other_short = _safe_float(r[18]) if len(r) > 18 else 0.0
                dealer_long = _safe_float(r[8])
                dealer_short = _safe_float(r[9])

                rows.append({
                    "file": str(f),
                    "market": r[0],
                    "report_date": r[2],
                    "preferred_long": am_long + other_long,
                    "preferred_short": am_short + other_short,
                    "preferred_net": (am_long + other_long) - (am_short + other_short),
                    "counter_long": lf_long + dealer_long,
                    "counter_short": lf_short + dealer_short,
                    "counter_net": (lf_long + dealer_long) - (lf_short + dealer_short),
                    "open_interest": _safe_float(r[7]) if len(r) > 7 else None,
                })

    uniq = {x["report_date"]: x for x in rows if x.get("report_date")}
    return [uniq[k] for k in sorted(uniq.keys())]

def _pressure_from_longs_shorts(long_v, short_v):
    if long_v > short_v:
        return "BULLISH", "ضغط صاعد"
    if long_v < short_v:
        return "BEARISH", "ضغط هابط"
    return "NEUTRAL", "غير مؤكد"

def _partial_from_delta(long_delta, short_delta, net_delta):
    if long_delta > 0 and short_delta < 0:
        return "BULLISH", "ضغط صاعد", "EXPLICIT_OPEN", "أفق ممتد / قراءة على المكشوف", "الشراء يزيد والبيع ينقص."
    if long_delta < 0 and short_delta > 0:
        return "BEARISH", "ضغط هابط", "EXPLICIT_OPEN", "أفق ممتد / قراءة على المكشوف", "الشراء ينقص والبيع يزيد."
    if net_delta > 0:
        return "BULLISH", "ضغط صاعد", "IMPLICIT_NARROW", "أفق ضيق / قراءة غير صريحة", "التغير الصافي يميل للصعود دون انكشاف كامل بين الشراء والبيع."
    if net_delta < 0:
        return "BEARISH", "ضغط هابط", "IMPLICIT_NARROW", "أفق ضيق / قراءة غير صريحة", "التغير الصافي يميل للهبوط دون انكشاف كامل بين الشراء والبيع."
    return "NEUTRAL", "غير مؤكد", "NEUTRAL", "غير مؤكد", "لا يوجد تغير كاف."

def _time_control_v548(sym):
    wd = datetime.now(timezone.utc).weekday()
    ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"][wd]
    en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][wd]
    s = (sym or "").upper()
    is_crypto = s.endswith("USDT") or s.startswith(("BTC", "ETH", "SOL"))

    if wd in (0, 4):
        return "PREFERRED_GROUP_TIME", "وقت سيطرة مجموعة الاتجاه الأساسية", True, wd, en, ar, "الوقت مناسب لأن سلطة اليوم مع مجموعة الاتجاه الأساسية."
    if wd in (1, 2, 3):
        return "COUNTER_GROUP_TIME", "وقت سيطرة مجموعة التذبذب المقابل", False, wd, en, ar, "الوقت غير مناسب لاتخاذ قرار لأن سلطة اليوم ليست مع مجموعة الاتجاه الأساسية."
    if is_crypto:
        return "COUNTER_GROUP_TIME", "وقت سيطرة مجموعة التذبذب المقابل", False, wd, en, ar, "عطلة نهاية الأسبوع للأصول المستمرة ليست وقت مواءمة لمجموعة الاتجاه الأساسية."
    return "NO_ACTIVE_TIME", "لا توجد سلطة توقيت نشطة", False, wd, en, ar, "لا توجد سلطة توقيت نشطة لهذا الأصل."

def build_preferred_group_direction_timing_contract(sym):
    rows = _preferred_rows_from_tff(sym)
    time_group, time_group_ar, timing_ok, wd, en, ar, time_reason = _time_control_v548(sym)

    if len(rows) < 2:
        return {
            "ok": False,
            "version": "V5.4.8",
            "public_name_ar": "عقد اتجاه مجموعة الأساس وتوقيت القرار",
            "source_family": "TFF",
            "direction_basis_ar": "مجموعة الاتجاه الأساسية + الآخرون حسب مصدر الأصل المفضل",
            "time_control_group": time_group,
            "time_control_group_ar": time_group_ar,
            "decision_timing_suitable": timing_ok,
            "correction_type": "UNKNOWN",
            "correction_visibility": "غير مؤكد: لا توجد تقارير كافية لحساب الاتجاه الجزئي والاتجاه العام.",
            "fallback_policy": "إذا لم تتوفر تقارير كافية لا يتم اختراع اتجاه أو تصحيح.",
            "updated_at": utcnow(),
        }

    prev, cur = rows[-2], rows[-1]

    overall, overall_ar = _pressure_from_longs_shorts(
        cur["preferred_long"],
        cur["preferred_short"],
    )

    long_delta = cur["preferred_long"] - prev["preferred_long"]
    short_delta = cur["preferred_short"] - prev["preferred_short"]
    net_delta = cur["preferred_net"] - prev["preferred_net"]

    partial, partial_ar, signal_type, signal_type_ar, signal_reason_ar = _partial_from_delta(
        long_delta,
        short_delta,
        net_delta,
    )

    if overall in ("BULLISH", "BEARISH") and partial in ("BULLISH", "BEARISH"):
        is_corr = overall != partial
        if is_corr:
            corr_type = "TIMING_CORRECTION"
            corr_state = "CORRECTION"
            corr_vis = "تصحيح"
        else:
            corr_type = "NONE"
            corr_state = "WITH_TREND"
            corr_vis = "لا يوجد تصحيح"
    else:
        is_corr = False
        corr_type = "UNKNOWN"
        corr_state = "UNKNOWN"
        corr_vis = "غير مؤكد: الاتجاه العام أو الجزئي غير واضح."

    if timing_ok:
        timing_state = "SUITABLE"
        timing_label_ar = "زمن القرار مناسب"
    else:
        timing_state = "NOT_SUITABLE"
        timing_label_ar = "زمن القرار غير مناسب"

    return {
        "ok": True,
        "version": "V5.4.8",
        "public_name_ar": "عقد اتجاه مجموعة الأساس وتوقيت القرار",
        "rule_ar": "يتم استخراج الاتجاه من مجموعة الاتجاه الأساسية + الآخرون. المستثمر يعتمد الاتجاه العام، والنمط التكتيكي يعتمد الاتجاه الجزئي/الأسبوعي. التصحيح هو اختلاف الجزئي عن العام.",
        "source_family": "TFF",
        "direction_basis_ar": "مجموعة الاتجاه الأساسية + الآخرون",
        "direction_basis_en": "Preferred direction group + others",

        "current_report": cur,
        "previous_report": prev,

        "overall_direction": overall,
        "overall_direction_ar": overall_ar,
        "overall_long": cur["preferred_long"],
        "overall_short": cur["preferred_short"],
        "overall_net": cur["preferred_net"],

        "partial_direction": partial,
        "partial_direction_ar": partial_ar,
        "partial_long_delta": long_delta,
        "partial_short_delta": short_delta,
        "partial_net_delta": net_delta,

        "signal_visibility_type": signal_type,
        "signal_visibility_ar": signal_type_ar,
        "signal_reason_ar": signal_reason_ar,

        "is_correction": is_corr,
        "correction_state": corr_state,
        "correction_type": corr_type,
        "correction_visibility": corr_vis,

        "time_control_group": time_group,
        "time_control_group_ar": time_group_ar,
        "weekday": en,
        "weekday_ar": ar,
        "decision_timing_suitable": timing_ok,
        "decision_timing_state": timing_state,
        "decision_timing_label_ar": timing_label_ar,
        "timing_reason_ar": time_reason,

        "source_paths": [
            "preferred_long",
            "preferred_short",
            "partial_long_delta",
            "partial_short_delta",
            "time_control_group",
        ],
        "source_endpoint": "/api/decision/quality-contract-v53",
        "source_service": "ndsp-v53-bridge",
        "contract_mode": "BACKEND_DERIVED",
        "updated_at": utcnow(),
        "fallback_policy": "إذا لم تتوفر بيانات مجموعة الاتجاه الأساسية أو توقيت السيطرة تظهر غير مؤكد ولا يتم اختراع تصحيح.",
    }


def build_decision_profile_direction_contract(base):
    pd = base.get("preferred_direction_timing_contract") or base.get("timing_correction_contract") or {}

    overall = pd.get("overall_direction") or "UNKNOWN"
    overall_ar = pd.get("overall_direction_ar") or "غير مؤكد"
    partial = pd.get("partial_direction") or "UNKNOWN"
    partial_ar = pd.get("partial_direction_ar") or "غير مؤكد"

    is_corr = bool(pd.get("is_correction"))
    corr_type = pd.get("correction_type") or "UNKNOWN"
    corr_vis = pd.get("correction_visibility") or "غير مؤكد"

    timing_ok = pd.get("decision_timing_suitable") is True
    timing_state = pd.get("decision_timing_state") or "UNKNOWN"
    timing_label = pd.get("decision_timing_label_ar") or "غير مؤكد"
    timing_reason = pd.get("timing_reason_ar") or "زمن السيطرة غير مؤكد."

    investor = {
        "profile_id": "investor",
        "public_name_ar": "نمط المستثمر",
        "public_name_en": "Investor View",
        "controlling_direction_type": "OVERALL_DIRECTION",
        "controlling_direction_type_ar": "الاتجاه العام / الكلي",
        "controlling_direction": overall,
        "controlling_direction_ar": overall_ar,
        "comparison_direction_type": "PARTIAL_OR_WEEKLY_DIRECTION",
        "comparison_direction_type_ar": "الاتجاه الجزئي / الأسبوعي",
        "comparison_direction": partial,
        "comparison_direction_ar": partial_ar,
        "is_correction": is_corr,
        "correction_type": corr_type,
        "correction_visibility": corr_vis,
        "direction_summary_ar": (
            "الاتجاه المعتمد للمستثمر هو الاتجاه العام. الاتجاه الجزئي يمثل تصحيحًا داخل الاتجاه العام."
            if is_corr else
            "الاتجاه المعتمد للمستثمر هو الاتجاه العام، والاتجاه الجزئي موافق له."
        ),
        "decision_timing_suitable": timing_ok,
        "decision_timing_state": timing_state,
        "decision_timing_label_ar": timing_label,
        "timing_reason_ar": timing_reason,
        "not_financial_advice": True,
        "not_execution_order": True,
        "source_paths": [
            "preferred_direction_timing_contract.overall_direction",
            "preferred_direction_timing_contract.partial_direction",
            "preferred_direction_timing_contract.is_correction",
        ],
        "source_endpoint": "/api/decision/quality-contract-v53",
        "source_service": "ndsp-v53-bridge",
        "contract_mode": "BACKEND_DERIVED",
        "updated_at": utcnow(),
    }

    tactical = {
        "profile_id": "tactical",
        "public_name_ar": "النمط التكتيكي",
        "public_name_en": "Tactical View",
        "controlling_direction_type": "PARTIAL_OR_WEEKLY_DIRECTION",
        "controlling_direction_type_ar": "الاتجاه الجزئي / الأسبوعي",
        "controlling_direction": partial,
        "controlling_direction_ar": partial_ar,
        "comparison_direction_type": "OVERALL_DIRECTION",
        "comparison_direction_type_ar": "الاتجاه العام / الكلي",
        "comparison_direction": overall,
        "comparison_direction_ar": overall_ar,
        "is_correction_against_overall": is_corr,
        "correction_type": corr_type,
        "correction_visibility": corr_vis,
        "direction_summary_ar": (
            "الاتجاه المعتمد للنمط التكتيكي هو الاتجاه الجزئي/الأسبوعي، لكنه يخالف الاتجاه العام لذلك يعد حركة تصحيحية."
            if is_corr else
            "الاتجاه المعتمد للنمط التكتيكي هو الاتجاه الجزئي/الأسبوعي، وهو موافق للاتجاه العام."
        ),
        "decision_timing_suitable": timing_ok,
        "decision_timing_state": timing_state,
        "decision_timing_label_ar": timing_label,
        "timing_reason_ar": timing_reason,
        "not_financial_advice": True,
        "not_execution_order": True,
        "source_paths": [
            "preferred_direction_timing_contract.partial_direction",
            "preferred_direction_timing_contract.overall_direction",
            "preferred_direction_timing_contract.decision_timing_suitable",
        ],
        "source_endpoint": "/api/decision/quality-contract-v53",
        "source_service": "ndsp-v53-bridge",
        "contract_mode": "BACKEND_DERIVED",
        "updated_at": utcnow(),
    }

    if overall in ("BULLISH", "BEARISH") and partial in ("BULLISH", "BEARISH"):
        alignment = "DIVERGENT" if overall != partial else "ALIGNED"
        alignment_ar = "مختلفان" if overall != partial else "متوافقان"
    else:
        alignment = "UNKNOWN"
        alignment_ar = "غير مؤكد"

    return {
        "ok": True,
        "version": "V5.4.8",
        "public_name_ar": "عقد اتجاه القرار حسب النمط",
        "public_name_en": "Decision Profile Direction Contract",
        "rule_ar": "يعرض القرار باتجاهين منظمين: المستثمر يعتمد الاتجاه العام، والنمط التكتيكي يعتمد الاتجاه الجزئي/الأسبوعي. التصحيح هو اختلاف الجزئي عن العام.",
        "investor_view": investor,
        "tactical_view": tactical,
        "direction_alignment": alignment,
        "direction_alignment_ar": alignment_ar,
        "source_endpoint": "/api/decision/quality-contract-v53",
        "source_service": "ndsp-v53-bridge",
        "source_paths": ["preferred_direction_timing_contract"],
        "contract_mode": "BACKEND_DERIVED",
        "updated_at": utcnow(),
        "fallback_policy": "إذا غاب أحد الاتجاهين لا يتم اختراع اتجاه للنمط، وتظهر الحالة غير مؤكدة.",
    }

def _normalize_decision_profile(profile):
    p = str(profile or "investor").strip().lower()
    if p in ("tactical", "active", "short", "weekly"):
        return "tactical"
    return "investor"

def select_decision_profile_view(base, profile=None):
    p = _normalize_decision_profile(profile)
    c = base.get("decision_profile_direction_contract") or {}
    if p == "tactical":
        view = c.get("tactical_view") or {}
        label_ar = "النمط التكتيكي"
    else:
        view = c.get("investor_view") or {}
        label_ar = "نمط المستثمر"

    return {
        "selected_profile": p,
        "selected_profile_ar": label_ar,
        "selected_direction_view": view,
        "selected_direction_summary_ar": view.get("direction_summary_ar") or "غير مؤكد",
        "selected_profile_source": "profile_query_param_or_default",
        "profile_options": [
            {"id": "investor", "label_ar": "نمط المستثمر", "direction_basis_ar": "الاتجاه العام / الكلي"},
            {"id": "tactical", "label_ar": "النمط التكتيكي", "direction_basis_ar": "الاتجاه الجزئي / الأسبوعي"},
        ],
        "profile_contract_version": "V5.4.8",
        "not_financial_advice": True,
        "not_execution_order": True,
        "updated_at": utcnow(),
    }


def _ndsp_public_correction_label_only(base):
    def label(t):
        t = str(t or '').upper()
        if t in ('TIMING_CORRECTION','CORRECTION','EXPLICIT','IMPLICIT'):
            return 'تصحيح'
        if t in ('NONE','WITH_TREND','NO_CORRECTION'):
            return 'لا يوجد تصحيح'
        return 'غير مؤكد'

    public_label = label(base.get('correction_type'))
    base['public_correction_label_ar'] = public_label
    base['correction_visibility'] = public_label

    for k in ('preferred_direction_timing_contract',
              'timing_correction_contract',
              'decision_profile_direction_contract'):
        c = base.get(k)
        if isinstance(c, dict):
            c['public_correction_label_ar'] = public_label
            c['correction_visibility'] = public_label
            c['public_display_policy'] = 'LABEL_ONLY'

    si = base.get('scenario_interpretation')
    if isinstance(si, dict):
        si['public_correction_label_ar'] = public_label
        gates = si.get('gates') or {}
        g = gates.get('tdl_correction')
        if isinstance(g, dict):
            g['label_ar'] = public_label
            g['reason_ar'] = 'تم تحديد التصنيف.'
        if public_label == 'تصحيح':
            safe = 'تم رصد تصحيح.'
        elif public_label == 'لا يوجد تصحيح':
            safe = 'لا يوجد تصحيح.'
        else:
            safe = 'حالة التصحيح غير مؤكدة.'
        for x in ('normal_user_summary_ar','advanced_summary_ar'):
            if x in si:
                si[x] = safe

    rn = base.get('radar_nodes')
    if isinstance(rn, dict) and isinstance(rn.get('tdl_correction'), dict):
        rn['tdl_correction']['label_ar'] = public_label

    return base

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
    correction_ok = correction_type in ('EXPLICIT','IMPLICIT','TIMING_CORRECTION','CORRECTION')
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

def contract(sym, profile=None):
    try: base=jget(f'http://127.0.0.1:9083/api/decision/quality-contract-v52?symbol={sym}')
    except Exception as e: base={'ok':False,'symbol':sym,'v52_error':str(e)}
    dv=devil(sym); td=parse_tdl(sym)
    base.update({'ok':True,'symbol':sym,'devil_advocate':dv,'devil_advocate_status':dv.get('status'),'devil_advocate_score':dv.get('score'),'risk_status':'CONNECTED_FROM_LAYER15' if dv.get('connected') else 'NOT_CONNECTED','risk_score':dv.get('score'),'tdl_contract':td,'tdl_state':td.get('tdl_state'),'tdl_bias':td.get('tdl_bias'),'correction_type':td.get('correction_type'),'correction_visibility':td.get('correction_visibility'),'updated_at':utcnow(),'v53_contract':{'ok':True,'version':'V5.4.3','sources':['raw_cot_files','layer15_devil','v52_nmp','official_radar_nodes'],'updated_at':utcnow()}})
    pd=build_preferred_group_direction_timing_contract(sym)
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
    base['decision_profile_direction_contract']=build_decision_profile_direction_contract(base)
    base['investor_direction_view']=base['decision_profile_direction_contract']['investor_view']
    base['tactical_direction_view']=base['decision_profile_direction_contract']['tactical_view']
    sel=select_decision_profile_view(base, profile)
    base['selected_profile']=sel.get('selected_profile')
    base['selected_profile_ar']=sel.get('selected_profile_ar')
    base['selected_direction_view']=sel.get('selected_direction_view')
    base['selected_direction_summary_ar']=sel.get('selected_direction_summary_ar')
    base['profile_options']=sel.get('profile_options')
    base['profile_contract_version']=sel.get('profile_contract_version')
    base['radar_nodes']=build_radar_nodes(base)
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
    }
    base=_ndsp_public_correction_label_only(base)
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



def _ndsp_v548_label(code):
    if code in ("TIMING_CORRECTION", "CORRECTION"):
        return "CORRECTION", "تصحيح"
    if code in ("NONE", "WITH_TREND", "NO_CORRECTION"):
        return "NO_CORRECTION", "لا يوجد تصحيح"
    return "UNKNOWN", "غير مؤكد"

def _ndsp_v548_view(view):
    view = view or {}
    status, label = _ndsp_v548_label(view.get("correction_type"))
    return {
        "name_ar": view.get("public_name_ar") or "النمط",
        "direction_ar": view.get("controlling_direction_ar") or "غير مؤكد",
        "correction_status": status,
        "correction_ar": label,
        "timing_ar": view.get("decision_timing_label_ar") or "غير مؤكد",
    }

def ndsp_public_summary_v548(symbol: str = "BTCUSDT"):
    raw = contract(symbol)
    profile = raw.get("decision_profile_direction_contract") or {}
    status, label = _ndsp_v548_label(raw.get("correction_type"))

    return {
        "ok": True,
        "version": "V5.4.8",
        "symbol": (raw.get("instrument") or {}).get("symbol") or symbol,
        "privacy_mode": "PUBLIC_RESULT_ONLY",
        "final_state_ar": ((raw.get("scenario_interpretation") or {}).get("final_state_ar") or "غير مؤكد"),
        "correction": {
            "status": status,
            "label_ar": label,
        },
        "investor_view": _ndsp_v548_view(profile.get("investor_view")),
        "tactical_view": _ndsp_v548_view(profile.get("tactical_view")),
        "risk_ar": ((raw.get("radar_nodes") or {}).get("risk") or {}).get("label_ar") or "غير مؤكد",
        "advocate_ar": ((raw.get("radar_nodes") or {}).get("devil") or {}).get("label_ar") or "غير مؤكد",
        "nmp_ar": ((raw.get("radar_nodes") or {}).get("nmp_check") or {}).get("label_ar") or "غير مؤكد",
        "golden_signal_ar": (raw.get("golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "enhanced_golden_signal_ar": (raw.get("enhanced_golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "notice_ar": "قراءة دعم قرار فقط، وليست توصية مالية ولا أمر تنفيذ.",
        "updated_at": utcnow(),
    }

@app.get("/api/decision/public-summary")
def public_summary_v548(symbol: str = "BTCUSDT"):
    return ndsp_public_summary_v548(symbol)

@app.get("/api/decision/public-contract-v548")
def public_contract_v548(symbol: str = "BTCUSDT"):
    return ndsp_public_summary_v548(symbol)


# NDSP_V548_FORCE_PUBLIC_SUMMARY_ROUTE_START

def _ndsp_v548_public_label(code):
    if code in ("TIMING_CORRECTION", "CORRECTION"):
        return "CORRECTION", "تصحيح"
    if code in ("NONE", "WITH_TREND", "NO_CORRECTION"):
        return "NO_CORRECTION", "لا يوجد تصحيح"
    return "UNKNOWN", "غير مؤكد"

def _ndsp_v548_public_view(view):
    view = view or {}
    status, label = _ndsp_v548_public_label(view.get("correction_type"))
    return {
        "name_ar": view.get("public_name_ar") or "النمط",
        "direction_ar": view.get("controlling_direction_ar") or "غير مؤكد",
        "correction_status": status,
        "correction_ar": label,
        "timing_ar": view.get("decision_timing_label_ar") or "غير مؤكد",
    }

def _ndsp_v548_public_summary(symbol: str = "BTCUSDT"):
    raw = contract(symbol)
    profile = raw.get("decision_profile_direction_contract") or {}
    status, label = _ndsp_v548_public_label(raw.get("correction_type"))

    return {
        "ok": True,
        "version": "V5.4.8",
        "symbol": (raw.get("instrument") or {}).get("symbol") or symbol,
        "privacy_mode": "PUBLIC_RESULT_ONLY",
        "final_state_ar": ((raw.get("scenario_interpretation") or {}).get("final_state_ar") or "غير مؤكد"),
        "correction": {
            "status": status,
            "label_ar": label,
        },
        "investor_view": _ndsp_v548_public_view(profile.get("investor_view")),
        "tactical_view": _ndsp_v548_public_view(profile.get("tactical_view")),
        "risk_ar": ((raw.get("radar_nodes") or {}).get("risk") or {}).get("label_ar") or "غير مؤكد",
        "advocate_ar": ((raw.get("radar_nodes") or {}).get("devil") or {}).get("label_ar") or "غير مؤكد",
        "nmp_ar": ((raw.get("radar_nodes") or {}).get("nmp_check") or {}).get("label_ar") or "غير مؤكد",
        "golden_signal_ar": (raw.get("golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "enhanced_golden_signal_ar": (raw.get("enhanced_golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "notice_ar": "قراءة دعم قرار فقط، وليست توصية مالية ولا أمر تنفيذ.",
        "updated_at": utcnow(),
    }

try:
    app.router.routes = [
        r for r in app.router.routes
        if getattr(r, "path", None) not in (
            "/api/decision/public-summary",
            "/api/decision/public-contract-v548",
        )
    ]
except Exception:
    pass

@app.get("/api/decision/public-summary")
def ndsp_public_summary_route_v548(symbol: str = "BTCUSDT"):
    return _ndsp_v548_public_summary(symbol)

@app.get("/api/decision/public-contract-v548")
def ndsp_public_contract_route_v548(symbol: str = "BTCUSDT"):
    return _ndsp_v548_public_summary(symbol)

# NDSP_V548_FORCE_PUBLIC_SUMMARY_ROUTE_END


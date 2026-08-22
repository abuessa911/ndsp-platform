#!/usr/bin/env bash
set -euo pipefail
set +H
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

TS="$(date +%Y%m%d_%H%M%S)"
USER_NAME="${SUDO_USER:-nawaf511}"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6 || echo /home/nawaf511)"
ROOT="/var/www/ndsp-my"
OUT_DIR="$HOME_DIR/ndsp_final_governance_reports"
REPORT="$OUT_DIR/NDSP_V541_ALL_PAGES_CONTRACT_GOVERNANCE_$TS.md"
PY_SCRIPT="$OUT_DIR/ndsp_v541_all_pages_contract_audit.py"
mkdir -p "$OUT_DIR"
log(){ echo "$*" | tee -a "$REPORT"; }
log "REPORT=$REPORT"
log "TS=$TS"
log "MODE=ALL_PAGES_CONTRACT_AUDIT_ONLY_NO_CHANGES"
log "ROOT=$ROOT"

cat > "$PY_SCRIPT" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, sys, urllib.request, urllib.parse, time
from pathlib import Path
from datetime import datetime, timezone

REQUIRED_API_BY_PAGE = {
  'decision-radar.html': ['quality-contract-v53'],
  'decision-center.html': ['quality-contract-v53'],
  'nmp.html': ['nmp-timeframes-live'],
  'decision-guide.html': ['quality-contract-v53'],
  'asset-selector.html': ['data/assets.json'],
  'completed-decisions.html': ['completed'],
  'index.html': [],
  'NDSP_Asset_View.html': ['quality-live'],
  'NDSP_Command_Center.html': ['quality-live'],
  'NDSP_Daily_Brief.html': ['quality-live'],
  'NDSP_Settings_Alerts.html': [],
  'decision-support.html': ['quality-live'],
}

DECISION_HINTS = ['radar','decision','nmp','scenario','quality','risk','devil','tdl','مخاطر','محامي الشيطان','NMP','TDL','مستويات','الأفق','حذر','غير موصول']
STATIC_STATUS_WORDS = ['>حذر<','>متصل<','>غير موصول<','>غير مرسل من المصدر<']


def now(): return datetime.now(timezone.utc).isoformat()

def read_file(p:Path):
  try: return p.read_text(encoding='utf-8',errors='ignore')
  except Exception: return ''

def fetch(url:str):
  try:
    with urllib.request.urlopen(url,timeout=12) as r:
      raw=r.read().decode('utf-8','replace')
      return r.status, raw
  except Exception as e:
    return 0, 'ERROR='+repr(e)

def rel_to_url(root:Path,p:Path,base:str):
  rel=p.relative_to(root).as_posix()
  return base.rstrip('/') + '/' + rel

def scripts_from_html(html:str):
  return re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, flags=re.I)

def resolve_script(root:Path, src:str):
  if src.startswith('/'): return root / src.lstrip('/')
  if src.startswith('http'): return None
  return root / src

def page_need(name:str, rel:str):
  if rel.startswith('_premium/'):
    return REQUIRED_API_BY_PAGE.get(Path(rel).name, [])
  return REQUIRED_API_BY_PAGE.get(name, [])

def scan_page(root:Path, page:Path, base:str):
  rel=page.relative_to(root).as_posix(); name=page.name
  html=read_file(page)
  url=rel_to_url(root,page,base)
  http, public_html=fetch(url+'?v='+str(int(time.time())))
  combined=html+'\n'+public_html
  scripts=scripts_from_html(combined)
  script_text=''
  for src in scripts:
    sp=resolve_script(root,src.split('?')[0])
    if sp and sp.exists(): script_text += '\n/*SCRIPT '+src+'*/\n' + read_file(sp)
  all_text=combined+'\n'+script_text
  expected=page_need(name,rel)
  found_api=[]
  for token in ['quality-contract-v53','nmp-timeframes-live','quality-live','completed','data/assets.json','v532-radar-label-authority','v531-risk-labels']:
    if token in all_text: found_api.append(token)
  decision_like=any(h in all_text for h in DECISION_HINTS) or any(k in name.lower() for k in ['decision','radar','nmp','asset'])
  status='PASS'; notes=[]
  if http!=200:
    status='FAIL'; notes.append(f'HTTP={http}')
  else:
    notes.append('HTTP=200')
  if expected:
    for token in expected:
      if token not in all_text:
        status='FAIL'; notes.append(f'MISSING_REQUIRED_CONTRACT_TOKEN={token}')
      else:
        notes.append(f'REQUIRED_CONTRACT_TOKEN_OK={token}')
  elif decision_like:
    if 'quality-contract-v53' not in all_text and 'quality-live' not in all_text and 'nmp-timeframes-live' not in all_text:
      if status=='PASS': status='WARN'
      notes.append('DECISION_LIKE_PAGE_WITHOUT_EXPLICIT_CONTRACT_TOKEN')
  bad_static=[]
  for w in STATIC_STATUS_WORDS:
    if w in html: bad_static.append(w)
  if bad_static and decision_like:
    if status=='PASS': status='WARN'
    notes.append('STATIC_STATUS_WORDS_IN_HTML='+','.join(bad_static[:5]))
  notes.append('FOUND_TOKENS='+(','.join(found_api) if found_api else 'NONE'))
  notes.append('SCRIPTS='+str(len(scripts)))
  return {'page':rel,'url':url,'status':status,'notes':notes,'expected':expected,'found_tokens':found_api}

def fetch_json(url:str):
  try:
    with urllib.request.urlopen(url,timeout=15) as r:
      return r.status,json.loads(r.read().decode('utf-8','replace'))
  except Exception as e:
    return 0,{'error':repr(e)}

def endpoint_contract_summary(base:str,symbols:list[str]):
  out=[]
  for sym in symbols:
    for name,path in [('v53','/api/decision/quality-contract-v53'),('nmp','/api/decision/nmp-timeframes-live'),('quality','/api/decision/quality-live')]:
      url=f'{base.rstrip()}{path}?symbol={sym}&_={int(time.time())}'
      code,data=fetch_json(url)
      row={'symbol':sym,'endpoint':name,'http':code,'url':url}
      if isinstance(data,dict):
        row['has_risk_score']='risk_score' in data
        row['has_devil_score']='devil_advocate_score' in data
        row['has_correction']='correction_type' in data or 'correction_visibility' in data
        row['has_nmp_timeframes']='nmp_timeframes' in data
        row['has_radar_nodes']='radar_nodes' in data
      out.append(row)
  return out

def main():
  ap=argparse.ArgumentParser()
  ap.add_argument('--root',default='/var/www/ndsp-my')
  ap.add_argument('--base-public',default='https://my.ndsp.app')
  ap.add_argument('--symbols',default='BTCUSDT,ETHUSDT')
  ap.add_argument('--out-dir',default='/home/nawaf511/ndsp_final_governance_reports')
  args=ap.parse_args()
  root=Path(args.root); out_dir=Path(args.out_dir); out_dir.mkdir(parents=True,exist_ok=True)
  pages=[]
  for pat in ['*.html','_premium/*.html']:
    pages.extend(sorted(root.glob(pat)))
  results=[scan_page(root,p,args.base_public) for p in pages if p.is_file()]
  eps=endpoint_contract_summary(args.base_public,[s.strip().upper() for s in args.symbols.split(',') if s.strip()])
  final='PASS'
  if any(r['status']=='FAIL' for r in results): final='FAIL'
  elif any(r['status']=='WARN' for r in results): final='WARN'
  md=[]
  md.append('# NDSP V5.4.1 — All Pages Contract Governance Audit')
  md.append('')
  md.append(f'Generated: {now()}')
  md.append(f'Root: `{root}`')
  md.append('')
  md.append('## Page Contract Matrix')
  md.append('| Page | Status | URL | Evidence |')
  md.append('|---|---:|---|---|')
  for r in results:
    ev='<br>'.join(x.replace('|','/') for x in r['notes'])
    md.append(f'| {r["page"]} | {r["status"]} | {r["url"]} | {ev} |')
  md.append('')
  md.append('## Endpoint Contract Summary')
  md.append('| Symbol | Endpoint | HTTP | Risk | Devil | Correction | NMP TF | radar_nodes |')
  md.append('|---|---|---:|---:|---:|---:|---:|---:|')
  for e in eps:
    md.append(f'| {e["symbol"]} | {e["endpoint"]} | {e["http"]} | {e.get("has_risk_score")} | {e.get("has_devil_score")} | {e.get("has_correction")} | {e.get("has_nmp_timeframes")} | {e.get("has_radar_nodes")} |')
  md.append('')
  md.append(f'FINAL_STATUS={final}')
  ts=datetime.now().strftime('%Y%m%d_%H%M%S')
  mdp=out_dir/f'NDSP_V541_ALL_PAGES_CONTRACT_AUDIT_{ts}.md'
  jsp=out_dir/f'NDSP_V541_ALL_PAGES_CONTRACT_AUDIT_{ts}.json'
  mdp.write_text('\n'.join(md),encoding='utf-8')
  jsp.write_text(json.dumps({'final_status':final,'pages':results,'endpoints':eps},ensure_ascii=False,indent=2),encoding='utf-8')
  for r in results: print(f'PAGE_STATUS {r["status"]} {r["page"]}')
  print('REPORT_MD='+str(mdp))
  print('REPORT_JSON='+str(jsp))
  print('FINAL_STATUS='+final)
  sys.exit(0 if final=='PASS' else 1)
if __name__=='__main__': main()
PY
chmod +x "$PY_SCRIPT"

log "PY_SCRIPT=$PY_SCRIPT"
log ""
log "== RUN ALL PAGES AUDIT =="
set +e
python3 "$PY_SCRIPT" --root "$ROOT" --base-public https://my.ndsp.app --symbols BTCUSDT,ETHUSDT --out-dir "$OUT_DIR" | tee -a "$REPORT"
RC=${PIPESTATUS[0]}
set -e
log "AUDIT_EXIT_CODE=$RC"
log "FINAL_STATUS=NDSP_V541_ALL_PAGES_CONTRACT_GOVERNANCE_DONE"
log "REPORT=$REPORT"

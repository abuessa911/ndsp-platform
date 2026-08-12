#!/usr/bin/env python3
# NDSP_PRODUCTION_MONITOR_V205
# NDSP_NONBLOCKING_LOCAL_OUTBOX_V208
from __future__ import annotations
import json, os, shutil, sqlite3, subprocess, sys, urllib.request
from datetime import datetime, timezone

DB=os.environ.get('NDSP_OPS_DB','/var/lib/ndsp-business-ops/ops.sqlite3')
STATE=os.environ.get('NDSP_OPS_MONITOR_STATE','/var/lib/ndsp-business-ops/monitor-state.json')
LATEST=os.environ.get('NDSP_OPS_LATEST_MONITOR','/var/lib/ndsp-business-ops/latest-monitor.json')
MAIL_USER=os.environ.get('NDSP_LOCAL_MAIL_USER','nawaf511')
PUBLIC=os.environ.get('NDSP_PUBLIC_BASE','https://my.ndsp.app')
LANDING=os.environ.get('NDSP_LANDING_BASE','https://ndsp.app')
LOCAL=os.environ.get('NDSP_LOCAL_DECISION_BASE','http://127.0.0.1:9082')
SERVICES=['ndsp-business-ops.service','ndsp-raw-cot-gateway.service','ndsp-quality-live-nmp-wrapper.service','ndsp-quality-live-golden-wrapper.service','ndsp-live-decision-quality.service']
URLS=[
 ('ops_local','http://127.0.0.1:9094/health','json'),
 ('decision_local',LOCAL+'/api/decision/quality-live?symbol=ETHUSDT&timeframe=weekly&analysis_mode=investment','decision'),
 ('landing',LANDING+'/','http'),
 ('login',PUBLIC+'/login/','http'),
 ('register',PUBLIC+'/register/','http'),
 ('portal',PUBLIC+'/portal-v50/','http'),
 ('decision_room',PUBLIC+'/decision-room-v31/','http'),
 ('public_health',PUBLIC+'/api/health','http'),
 ('ops_public',PUBLIC+'/api/ops/health','json'),
 ('start_page',PUBLIC+'/start/','http'),
 ('support_page',PUBLIC+'/support/','http'),
 ('subscribe_page',PUBLIC+'/subscribe/','http'),
]

def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def load(path,default):
 try: return json.load(open(path,encoding='utf-8'))
 except Exception: return default

def save(path,obj):
 os.makedirs(os.path.dirname(path),exist_ok=True)
 tmp=path+'.tmp'
 with open(tmp,'w',encoding='utf-8') as f: json.dump(obj,f,ensure_ascii=False,indent=2)
 os.replace(tmp,path)

def mail(subject,body):
 outbox=os.path.join(os.path.dirname(DB),'outbox')
 os.makedirs(outbox,exist_ok=True)
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
 safe=''.join(ch if ch.isalnum() else '_' for ch in subject).strip('_')[:80] or 'message'
 path=os.path.join(outbox,f'{stamp}_{safe}.eml')
 payload=f'To: {MAIL_USER}\nSubject: {subject}\nContent-Type: text/plain; charset=UTF-8\n\n{body}\n'
 tmp=path+'.tmp'
 with open(tmp,'w',encoding='utf-8') as f:
  f.write(payload)
 os.replace(tmp,path)
 return path

def service_check(name):
 p=subprocess.run(['systemctl','is-active',name],capture_output=True,text=True)
 return {'ok':p.returncode==0,'state':p.stdout.strip() or p.stderr.strip()}

def url_check(name,url,kind):
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'NDSP-Production-Monitor/204','Accept':'application/json,text/html'})
  with urllib.request.urlopen(req,timeout=18) as r:
   raw=r.read(2_000_000); code=r.status
  ok=200<=code<400; detail={'http':code,'bytes':len(raw)}
  if kind in {'json','decision'}:
   data=json.loads(raw.decode('utf-8'))
   ok=ok and data.get('ok') is True
   if kind=='decision':
    layers=data.get('decision_layers') or []
    caps=data.get('platform_capabilities') or []
    score=data.get('commercial_score') or data.get('commercial_quality_score') or {}
    score_ok=isinstance(score,dict) and (score.get('calculated') is True or isinstance(score.get('score'),(int,float)))
    ok=ok and len(layers)==16 and len(caps)==28 and score_ok
    detail.update({'layers':len(layers),'capabilities':len(caps),'commercial_score_ok':score_ok})
  return {'ok':ok,**detail}
 except Exception as e:
  return {'ok':False,'error':str(e)[:300]}

def main():
 checked=now(); services={s:service_check(s) for s in SERVICES}; urls={n:url_check(n,u,k) for n,u,k in URLS}
 failures=[f'service:{n}' for n,v in services.items() if not v['ok']]+[f'url:{n}' for n,v in urls.items() if not v['ok']]
 overall='HEALTHY' if not failures else 'DEGRADED'
 payload={'version':'V205','checked_at':checked,'overall_status':overall,'failures':failures,'services':services,'urls':urls}
 save(LATEST,payload)
 os.makedirs(os.path.dirname(DB),exist_ok=True)
 with sqlite3.connect(DB) as c:
  c.execute('CREATE TABLE IF NOT EXISTS monitor_checks(id INTEGER PRIMARY KEY AUTOINCREMENT,checked_at TEXT NOT NULL,overall_status TEXT NOT NULL,payload_json TEXT NOT NULL)')
  c.execute('INSERT INTO monitor_checks(checked_at,overall_status,payload_json) VALUES(?,?,?)',(checked,overall,json.dumps(payload,ensure_ascii=False)))
  c.execute('DELETE FROM monitor_checks WHERE id NOT IN (SELECT id FROM monitor_checks ORDER BY id DESC LIMIT 10000)')
 state=load(STATE,{'consecutive_failures':0,'alerted':False})
 if overall=='DEGRADED':
  state['consecutive_failures']=int(state.get('consecutive_failures',0))+1
  if state['consecutive_failures']>=3 and not state.get('alerted'):
   mail('[NDSP] Production alert',f'NDSP production has failed 3 consecutive checks.\nTime: {checked}\nFailures: '+', '.join(failures))
   state['alerted']=True
 else:
  if state.get('alerted'):
   mail('[NDSP] Production recovered',f'NDSP production recovered.\nTime: {checked}')
  state={'consecutive_failures':0,'alerted':False}
 state['last_status']=overall; state['last_checked_at']=checked; save(STATE,state)
 print(json.dumps({'overall_status':overall,'failures':failures},ensure_ascii=False))
 return 0 if overall=='HEALTHY' else 1
if __name__=='__main__': sys.exit(main())

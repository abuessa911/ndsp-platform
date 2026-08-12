#!/usr/bin/env python3
# NDSP_BUSINESS_DAILY_DIGEST_V205
# NDSP_NONBLOCKING_LOCAL_OUTBOX_V208
from __future__ import annotations
import json, os, shutil, sqlite3, subprocess
from datetime import datetime, timedelta, timezone
DB=os.environ.get('NDSP_OPS_DB','/var/lib/ndsp-business-ops/ops.sqlite3')
REPORT_DIR=os.environ.get('NDSP_OPS_REPORT_DIR','/home/nawaf511/ndsp_launch_reports')
MAIL_USER=os.environ.get('NDSP_LOCAL_MAIL_USER','nawaf511')
LATEST=os.environ.get('NDSP_OPS_LATEST_MONITOR','/var/lib/ndsp-business-ops/latest-monitor.json')

def send(subject,body):
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

def main():
 now=datetime.now(timezone.utc); since=(now-timedelta(hours=24)).isoformat(timespec='seconds')
 counts={}; open_counts={}
 with sqlite3.connect(DB) as c:
  for table in ['leads','support_tickets','subscription_requests','onboarding_events']:
   counts[table]=c.execute(f'SELECT count(*) FROM {table} WHERE created_at>=?',(since,)).fetchone()[0]
  open_counts['support_open']=c.execute("SELECT count(*) FROM support_tickets WHERE status NOT IN ('resolved','closed')").fetchone()[0]
  open_counts['subscriptions_pending']=c.execute("SELECT count(*) FROM subscription_requests WHERE status IN ('new','pending','open','in_progress')").fetchone()[0]
 try: monitor=json.load(open(LATEST,encoding='utf-8'))
 except Exception: monitor={'overall_status':'UNKNOWN','checked_at':None,'failures':[]}
 body='\n'.join([
  '# NDSP Daily Business Digest',
  f'DATE={now.isoformat(timespec="seconds")}',
  f'PRODUCTION_STATUS={monitor.get("overall_status")}',
  f'PRODUCTION_CHECKED_AT={monitor.get("checked_at")}',
  f'NEW_LEADS_24H={counts["leads"]}',
  f'NEW_SUPPORT_TICKETS_24H={counts["support_tickets"]}',
  f'NEW_SUBSCRIPTION_REQUESTS_24H={counts["subscription_requests"]}',
  f'ONBOARDING_EVENTS_24H={counts["onboarding_events"]}',
  f'OPEN_SUPPORT_TICKETS={open_counts["support_open"]}',
  f'PENDING_SUBSCRIPTIONS={open_counts["subscriptions_pending"]}',
  f'CURRENT_FAILURES={",".join(monitor.get("failures") or []) or "NONE"}',
 ])+'\n'
 os.makedirs(REPORT_DIR,exist_ok=True)
 path=os.path.join(REPORT_DIR,'NDSP_DAILY_BUSINESS_DIGEST_'+now.strftime('%Y%m%d')+'.md')
 open(path,'w',encoding='utf-8').write(body)
 send('[NDSP] Daily business digest',body)
 print(f'DAILY_DIGEST_REPORT={path}')
if __name__=='__main__': main()

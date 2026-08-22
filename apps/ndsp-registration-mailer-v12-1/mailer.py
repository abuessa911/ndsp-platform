#!/usr/bin/env python3
import html
import json
import os
import smtplib
import ssl
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path

ENV_FILE=Path('/etc/ndsp-registration-mailer-v12-1.json')

cfg=json.loads(ENV_FILE.read_text(encoding='utf-8'))
required=['SMTP_HOST','SMTP_PORT','SMTP_USER','SMTP_PASSWORD','SMTP_FROM','OWNER_EMAIL','OWNER_NOTICE_EMAIL','DB_ENV_FILE']
missing=[k for k in required if not cfg.get(k)]
if missing:
    print('MAILER_CONFIG_GATE=FAIL missing='+','.join(missing))
    raise SystemExit(2)

def load_shell_env(path):
    cmd=['bash','-lc',f"set -a; source {str(path)!r}; env -0"]
    raw=subprocess.check_output(cmd)
    env=os.environ.copy()
    for item in raw.split(b'\0'):
        if b'=' in item:
            k,v=item.split(b'=',1)
            env[k.decode(errors='ignore')]=v.decode(errors='ignore')
    return env

db_env=load_shell_env(Path(cfg['DB_ENV_FILE']))

def psql(sql, vars=None, tuples=True):
    cmd=['psql','-X','-v','ON_ERROR_STOP=1']
    if tuples:
        cmd += ['-At','-F','\t']
    for k,v in (vars or {}).items():
        cmd += ['-v',f'{k}={v}']
    proc=subprocess.run(
        cmd,
        input=sql,
        env=db_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    return proc.stdout.strip()

psql('''
CREATE TABLE IF NOT EXISTS public.ndsp_registration_email_dispatch (
  user_id uuid PRIMARY KEY,
  user_email text NOT NULL,
  user_sent_at timestamptz,
  owner_sent_at timestamptz,
  attempts integer NOT NULL DEFAULT 0,
  last_error text,
  updated_at timestamptz NOT NULL DEFAULT now()
);
''', tuples=False)

lookback=int(cfg.get('REGISTRATION_LOOKBACK_HOURS','72'))
rows=psql(f'''
SELECT u.id::text,
       replace(coalesce(u.name,''), E'\\t', ' '),
       replace(u.email, E'\\t', ' '),
       coalesce(u.created_at::text,''),
       coalesce(d.user_sent_at::text,''),
       coalesce(d.owner_sent_at::text,'')
FROM public.users u
LEFT JOIN public.ndsp_registration_email_dispatch d ON d.user_id=u.id
WHERE u.created_at >= now() - interval '{lookback} hours'
  AND upper(coalesce(u.status::text,'')) = 'ACTIVE'
  AND coalesce(u.email_verified,false) = true
  AND u.email ~* '^[^[:space:]@]+@[^[:space:]@]+\.[^[:space:]@]+$'
  AND lower(u.email) NOT LIKE '%.invalid'
  AND lower(u.email) <> lower(:'owner_email')
  AND (d.user_sent_at IS NULL OR d.owner_sent_at IS NULL)
ORDER BY u.created_at ASC
LIMIT 50;
''', {'owner_email':cfg['OWNER_EMAIL']})

items=[]
for line in rows.splitlines() if rows else []:
    parts=line.split('\t')
    if len(parts)>=6:
        items.append(parts[:6])

print(f'PENDING_REGISTRATION_EMAIL_COUNT={len(items)}')

def connect():
    host=cfg['SMTP_HOST']; port=int(cfg['SMTP_PORT'])
    mode=cfg.get('SMTP_SECURE','starttls').lower()
    context=ssl.create_default_context()
    if mode in ('ssl','smtps','true','1') or port==465:
        server=smtplib.SMTP_SSL(host,port,timeout=30,context=context)
    else:
        server=smtplib.SMTP(host,port,timeout=30)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
    server.login(cfg['SMTP_USER'],cfg['SMTP_PASSWORD'])
    return server

def send(to, subject, text, html_body):
    msg=EmailMessage()
    msg['From']=cfg['SMTP_FROM']
    msg['To']=to
    msg['Subject']=subject
    msg.set_content(text)
    msg.add_alternative(html_body, subtype='html')
    with connect() as s:
        s.send_message(msg)

for uid,name,email,created,user_sent,owner_sent in items:
    safe_name=html.escape(name or 'NDSP User')
    safe_email=html.escape(email)
    user_ok=bool(user_sent); owner_ok=bool(owner_sent)
    errors=[]
    if not user_ok:
        try:
            send(
              email,
              'NDSP — Welcome / مرحباً بك',
              f'''مرحباً {name or 'بك'},\n\nتم إنشاء حسابك في NDSP — Nawaf Decision Support Platform بنجاح.\nيمكنك تسجيل الدخول من: https://my.ndsp.app/login/\n\nهذه المنصة تقدم دعماً تفسيرياً للقرار وليست أوامر تداول.\n\nHello {name or 'there'},\nYour NDSP account has been created successfully.\nLogin: https://my.ndsp.app/login/''',
              f'''<div dir="rtl" style="font-family:Arial,sans-serif;line-height:1.8"><h2>مرحباً {safe_name}</h2><p>تم إنشاء حسابك في <b>NDSP — Nawaf Decision Support Platform</b> بنجاح.</p><p><a href="https://my.ndsp.app/login/">تسجيل الدخول</a></p><p style="color:#666">مخرجات المنصة تفسيرية وليست أوامر تداول.</p><hr><div dir="ltr"><h3>Welcome {safe_name}</h3><p>Your NDSP account has been created successfully.</p><p><a href="https://my.ndsp.app/login/">Sign in</a></p></div></div>''')
            user_ok=True
            print('USER_WELCOME_EMAIL=PASS user_id='+uid)
        except Exception as e:
            errors.append('USER:'+type(e).__name__+':'+str(e)[:300])
            print('USER_WELCOME_EMAIL=FAIL user_id='+uid+' error='+type(e).__name__)
    if not owner_ok:
        try:
            send(
              cfg['OWNER_NOTICE_EMAIL'],
              'NDSP — New User Registration / تسجيل مستخدم جديد',
              f'''تم تسجيل مستخدم جديد في NDSP.\nالاسم: {name}\nالبريد: {email}\nوقت التسجيل: {created}\nالحالة: ACTIVE''',
              f'''<div dir="rtl" style="font-family:Arial,sans-serif;line-height:1.8"><h2>تسجيل مستخدم جديد</h2><p><b>الاسم:</b> {safe_name}</p><p><b>البريد:</b> {safe_email}</p><p><b>وقت التسجيل:</b> {html.escape(created)}</p><p><b>الحالة:</b> ACTIVE</p></div>''')
            owner_ok=True
            print('OWNER_REGISTRATION_NOTICE=PASS user_id='+uid)
        except Exception as e:
            errors.append('OWNER:'+type(e).__name__+':'+str(e)[:300])
            print('OWNER_REGISTRATION_NOTICE=FAIL user_id='+uid+' error='+type(e).__name__)

    psql('''
INSERT INTO public.ndsp_registration_email_dispatch
(user_id,user_email,user_sent_at,owner_sent_at,attempts,last_error,updated_at)
VALUES (:'uid'::uuid, :'email',
        CASE WHEN :'user_ok'='1' THEN now() ELSE NULL END,
        CASE WHEN :'owner_ok'='1' THEN now() ELSE NULL END,
        1, nullif(:'last_error',''), now())
ON CONFLICT (user_id) DO UPDATE SET
 user_email=excluded.user_email,
 user_sent_at=CASE WHEN :'user_ok'='1' THEN coalesce(public.ndsp_registration_email_dispatch.user_sent_at,now()) ELSE public.ndsp_registration_email_dispatch.user_sent_at END,
 owner_sent_at=CASE WHEN :'owner_ok'='1' THEN coalesce(public.ndsp_registration_email_dispatch.owner_sent_at,now()) ELSE public.ndsp_registration_email_dispatch.owner_sent_at END,
 attempts=public.ndsp_registration_email_dispatch.attempts+1,
 last_error=nullif(:'last_error',''),
 updated_at=now();
''', {
      'uid':uid,'email':email,'user_ok':'1' if user_ok else '0',
      'owner_ok':'1' if owner_ok else '0','last_error':' | '.join(errors)
    }, tuples=False)

failed=psql("select count(*) from public.ndsp_registration_email_dispatch where user_sent_at is null or owner_sent_at is null;")
print('UNSENT_DISPATCH_COUNT='+failed)
if failed != '0':
    raise SystemExit(4)
print('FINAL_STATUS=NDSP_REGISTRATION_EMAIL_DISPATCH_COMPLETE')

#!/usr/bin/env python3
import os, sys, json, smtplib, ssl
from email.message import EmailMessage

def clean(v):
    v = str(v or "").strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v.strip()

payload = json.loads(sys.stdin.read() or "{}")

to = clean(payload.get("to"))
subject = clean(payload.get("subject"))
text = str(payload.get("text") or "")
html = str(payload.get("html") or "")

host = clean(os.environ.get("SMTP_HOST"))
port = int(clean(os.environ.get("SMTP_PORT")) or "587")
user = clean(os.environ.get("SMTP_USER"))
password = clean(os.environ.get("SMTP_PASS") or os.environ.get("SMTP_PASSWORD"))
sender = clean(os.environ.get("SMTP_FROM") or user)

if not host or not user or not password or not sender or not to:
    print(json.dumps({"ok": False, "error": "SMTP_CONFIG_OR_TO_MISSING"}))
    sys.exit(2)

msg = EmailMessage()
msg["From"] = sender
msg["To"] = to
msg["Subject"] = subject or "NDSP Notification"
msg.set_content(text or "NDSP notification")

if html:
    msg.add_alternative(html, subtype="html")

try:
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=25) as s:
            s.login(user, password)
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=25) as s:
            s.ehlo()
            s.starttls(context=ssl.create_default_context())
            s.login(user, password)
            s.send_message(msg)

    print(json.dumps({"ok": True, "to": to}))
except Exception as e:
    print(json.dumps({"ok": False, "error": str(e)}))
    sys.exit(1)

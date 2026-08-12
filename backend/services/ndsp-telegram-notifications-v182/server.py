#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import hmac
import http.server
import json
import os
import secrets
import sqlite3
import ssl
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

BASE_DIR=Path(__file__).resolve().parent
ENV_FILE=BASE_DIR/".env"

def load_env():
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text(encoding="utf-8",errors="ignore").splitlines():
        line=raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key,value=line.split("=",1)
        os.environ.setdefault(key.strip(),value.strip())

load_env()

PORT=int(os.environ.get("NDSP_TELEGRAM_PORT","9091"))
BASE_URL=os.environ.get("NDSP_BASE_URL","https://my.ndsp.app").rstrip("/")
AUTH_URL=os.environ.get("NDSP_AUTH_SESSION_URL",BASE_URL+"/api/auth/session")
BOT_TOKEN=os.environ.get("NDSP_TELEGRAM_BOT_TOKEN","").strip()
BOT_USERNAME=os.environ.get("NDSP_TELEGRAM_BOT_USERNAME","").strip().lstrip("@")
WEBHOOK_PATH=os.environ.get("NDSP_TELEGRAM_WEBHOOK_PATH","").strip()
WEBHOOK_SECRET=os.environ.get("NDSP_TELEGRAM_WEBHOOK_SECRET","").strip()
INTERNAL_SECRET=os.environ.get("NDSP_TELEGRAM_INTERNAL_SECRET","").strip()
DB_PATH=Path(os.environ.get("NDSP_TELEGRAM_DB",str(BASE_DIR/"data"/"telegram.sqlite3")))
LOCK=threading.RLock()
MAX_BODY=1024*1024

def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def now_epoch():
    return int(time.time())

def db():
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    connection=sqlite3.connect(DB_PATH,timeout=20)
    connection.row_factory=sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    return connection

def init_db():
    with LOCK,db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS bindings(
          user_key TEXT PRIMARY KEY,
          email TEXT NOT NULL,
          chat_id TEXT UNIQUE,
          telegram_username TEXT,
          active INTEGER NOT NULL DEFAULT 0,
          linked_at TEXT,
          updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS preferences(
          user_key TEXT PRIMARY KEY,
          decision_complete INTEGER NOT NULL DEFAULT 1,
          scenario_change INTEGER NOT NULL DEFAULT 1,
          level_update INTEGER NOT NULL DEFAULT 1,
          daily_brief INTEGER NOT NULL DEFAULT 0,
          quiet_start TEXT NOT NULL DEFAULT '23:00',
          quiet_end TEXT NOT NULL DEFAULT '07:00',
          timezone TEXT NOT NULL DEFAULT 'Asia/Riyadh',
          updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS link_codes(
          code_hash TEXT PRIMARY KEY,
          user_key TEXT NOT NULL,
          email TEXT NOT NULL,
          expires_at INTEGER NOT NULL,
          used_at INTEGER
        );
        CREATE TABLE IF NOT EXISTS delivery_log(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_key TEXT,
          event_type TEXT NOT NULL,
          status TEXT NOT NULL,
          summary TEXT,
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS accepted_events(
          event_key TEXT PRIMARY KEY,
          event_type TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        """)

def json_bytes(value):
    return json.dumps(value,ensure_ascii=False,separators=(",",":")).encode("utf-8")

def request_json(url,method="GET",payload=None,headers=None):
    body=None if payload is None else json_bytes(payload)
    req=urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Accept":"application/json","User-Agent":"NDSP-Telegram-V182",**(headers or {})},
    )
    if body is not None:
        req.add_header("Content-Type","application/json")
    with urllib.request.urlopen(req,timeout=15,context=ssl.create_default_context()) as response:
        raw=response.read()
        return response.status,(json.loads(raw.decode("utf-8")) if raw else {})

def recursive_find(value,keys,depth=0):
    if depth>7 or value is None:
        return None
    if isinstance(value,dict):
        for key in keys:
            if value.get(key) not in (None,""):
                return value[key]
        for child in value.values():
            found=recursive_find(child,keys,depth+1)
            if found not in (None,""):
                return found
    elif isinstance(value,list):
        for child in value:
            found=recursive_find(child,keys,depth+1)
            if found not in (None,""):
                return found
    return None

def session_from_cookie(cookie):
    if not cookie:
        return None
    try:
        _,payload=request_json(AUTH_URL,headers={"Cookie":cookie})
    except Exception:
        return None
    email=recursive_find(payload,["email","user_email"])
    user_id=recursive_find(payload,["user_id","userId","id","sub","account_id"])
    if not email and not user_id:
        return None
    return {
        "user_key":str(user_id or email),
        "email":str(email or user_id),
    }

def telegram(method,payload):
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_NOT_CONFIGURED")
    _,data=request_json(
        f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
        "POST",
        payload,
    )
    if not data.get("ok"):
        raise RuntimeError(str(data.get("description") or "TELEGRAM_API_ERROR"))
    return data.get("result")

def send_message(chat_id,text):
    return telegram("sendMessage",{
        "chat_id":str(chat_id),
        "text":str(text)[:3900],
        "disable_web_page_preview":True,
    })

def ensure_preferences(user_key):
    with LOCK,db() as con:
        con.execute(
            "INSERT INTO preferences(user_key,updated_at) VALUES(?,?) ON CONFLICT(user_key) DO NOTHING",
            (user_key,now_iso()),
        )

def preference(user_key):
    ensure_preferences(user_key)
    with LOCK,db() as con:
        row=con.execute("SELECT * FROM preferences WHERE user_key=?",(user_key,)).fetchone()
    return dict(row)

def binding(user_key):
    with LOCK,db() as con:
        row=con.execute("SELECT * FROM bindings WHERE user_key=?",(user_key,)).fetchone()
    return dict(row) if row else None

def mask(value):
    value=str(value or "")
    return ("*"*max(0,len(value)-4)+value[-4:]) if value else ""

def status(session):
    b=binding(session["user_key"])
    p=preference(session["user_key"])
    linked=bool(b and b.get("active") and b.get("chat_id"))
    return {
        "ok":True,
        "configured":bool(BOT_TOKEN and BOT_USERNAME),
        "bot_username":BOT_USERNAME,
        "linked":linked,
        "chat_id_masked":mask(b.get("chat_id") if b else ""),
        "telegram_username":b.get("telegram_username") if b else None,
        "linked_at":b.get("linked_at") if b else None,
        "preferences":{
            "decision_complete":bool(p["decision_complete"]),
            "scenario_change":bool(p["scenario_change"]),
            "level_update":bool(p["level_update"]),
            "daily_brief":bool(p["daily_brief"]),
            "quiet_start":p["quiet_start"],
            "quiet_end":p["quiet_end"],
            "timezone":p["timezone"],
        },
    }

def create_link(session):
    if not BOT_TOKEN or not BOT_USERNAME:
        raise RuntimeError("TELEGRAM_NOT_CONFIGURED")
    raw=secrets.token_urlsafe(10).replace("-","").replace("_","")[:12]
    digest=hashlib.sha256(raw.encode()).hexdigest()
    with LOCK,db() as con:
        con.execute("DELETE FROM link_codes WHERE user_key=? AND used_at IS NULL",(session["user_key"],))
        con.execute(
            "INSERT INTO link_codes(code_hash,user_key,email,expires_at) VALUES(?,?,?,?)",
            (digest,session["user_key"],session["email"],now_epoch()+600),
        )
    return {
        "ok":True,
        "link_url":f"https://t.me/{BOT_USERNAME}?start={raw}",
        "expires_in_seconds":600,
    }

def bind_code(code,message):
    digest=hashlib.sha256(code.encode()).hexdigest()
    with LOCK,db() as con:
        row=con.execute(
            "SELECT * FROM link_codes WHERE code_hash=? AND used_at IS NULL AND expires_at>=?",
            (digest,now_epoch()),
        ).fetchone()
        if not row:
            return False,None
        sender=message.get("from") or {}
        chat=message.get("chat") or {}
        chat_id=str(chat.get("id") or "")
        if not chat_id:
            return False,None
        con.execute("UPDATE bindings SET active=0,updated_at=? WHERE chat_id=?",(now_iso(),chat_id))
        con.execute("""
        INSERT INTO bindings(user_key,email,chat_id,telegram_username,active,linked_at,updated_at)
        VALUES(?,?,?,?,1,?,?)
        ON CONFLICT(user_key) DO UPDATE SET
          email=excluded.email,
          chat_id=excluded.chat_id,
          telegram_username=excluded.telegram_username,
          active=1,
          linked_at=excluded.linked_at,
          updated_at=excluded.updated_at
        """,(
            row["user_key"],row["email"],chat_id,str(sender.get("username") or ""),
            now_iso(),now_iso(),
        ))
        con.execute("UPDATE link_codes SET used_at=? WHERE code_hash=?",(now_epoch(),digest))
    ensure_preferences(row["user_key"])
    return True,chat_id

def update_preferences(user_key,payload):
    current=preference(user_key)
    quiet_start=str(payload.get("quiet_start",current["quiet_start"]))
    quiet_end=str(payload.get("quiet_end",current["quiet_end"]))
    for value in (quiet_start,quiet_end):
        dt.datetime.strptime(value,"%H:%M")
    timezone=str(payload.get("timezone",current["timezone"]))
    ZoneInfo(timezone)
    values=[
        1 if bool(payload.get("decision_complete",current["decision_complete"])) else 0,
        1 if bool(payload.get("scenario_change",current["scenario_change"])) else 0,
        1 if bool(payload.get("level_update",current["level_update"])) else 0,
        1 if bool(payload.get("daily_brief",current["daily_brief"])) else 0,
    ]
    with LOCK,db() as con:
        con.execute("""
        INSERT INTO preferences(
          user_key,decision_complete,scenario_change,level_update,daily_brief,
          quiet_start,quiet_end,timezone,updated_at
        ) VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(user_key) DO UPDATE SET
          decision_complete=excluded.decision_complete,
          scenario_change=excluded.scenario_change,
          level_update=excluded.level_update,
          daily_brief=excluded.daily_brief,
          quiet_start=excluded.quiet_start,
          quiet_end=excluded.quiet_end,
          timezone=excluded.timezone,
          updated_at=excluded.updated_at
        """,(user_key,*values,quiet_start,quiet_end,timezone,now_iso()))

def quiet(p):
    try:
        zone=ZoneInfo(p["timezone"])
        current=dt.datetime.now(zone).time()
        start=dt.datetime.strptime(p["quiet_start"],"%H:%M").time()
        end=dt.datetime.strptime(p["quiet_end"],"%H:%M").time()
    except Exception:
        return False
    if start==end:
        return False
    return (start<=current<end) if start<end else (current>=start or current<end)

def log_delivery(user_key,event_type,status_value,summary):
    with LOCK,db() as con:
        con.execute(
            "INSERT INTO delivery_log(user_key,event_type,status,summary,created_at) VALUES(?,?,?,?,?)",
            (user_key,event_type,status_value,str(summary)[:500],now_iso()),
        )

def history(user_key):
    with LOCK,db() as con:
        rows=con.execute(
            "SELECT event_type,status,summary,created_at FROM delivery_log WHERE user_key=? ORDER BY id DESC LIMIT 20",
            (user_key,),
        ).fetchall()
    return [dict(row) for row in rows]

def message_for(event_type,payload):
    title={
        "decision_complete":"اكتملت قراءة قرار جديدة",
        "scenario_change":"تغيرت حالة السيناريو",
        "level_update":"تم تحديث مستوى مرجعي",
        "daily_brief":"الملخص اليومي",
    }.get(event_type,"تحديث جديد")
    symbol=str(payload.get("symbol") or payload.get("asset_symbol") or payload.get("asset") or "NDSP")
    state=str(payload.get("scenario_state") or payload.get("decision_status") or payload.get("status") or "")
    quality=str(payload.get("decision_quality") or payload.get("quality") or "")
    context=str(payload.get("directional_context") or payload.get("trend_context") or "")
    lines=[f"NDSP — {title}",f"الأصل: {symbol}"]
    if state: lines.append(f"الحالة: {state}")
    if quality: lines.append(f"جودة القراءة: {quality}")
    if context: lines.append(f"السياق: {context}")
    lines.extend(["","هذه قراءة تفسيرية لدعم القرار وليست أمر شراء أو بيع.",BASE_URL+"/portal-v50/"])
    return "\n".join(lines)

def dispatch(event_type,payload):
    setting={
        "decision_complete":"decision_complete",
        "scenario_change":"scenario_change",
        "level_update":"level_update",
        "daily_brief":"daily_brief",
    }.get(event_type,"decision_complete")
    sent=skipped=failed=0
    with LOCK,db() as con:
        rows=con.execute("SELECT * FROM bindings WHERE active=1 AND chat_id IS NOT NULL").fetchall()
    for row in rows:
        b=dict(row)
        p=preference(b["user_key"])
        if not bool(p[setting]) or quiet(p):
            skipped+=1
            log_delivery(b["user_key"],event_type,"skipped","disabled or quiet hours")
            continue
        try:
            text=message_for(event_type,payload)
            send_message(b["chat_id"],text)
            sent+=1
            log_delivery(b["user_key"],event_type,"sent",text.splitlines()[0])
        except Exception as error:
            failed+=1
            log_delivery(b["user_key"],event_type,"failed",str(error))
    return {"sent":sent,"skipped":skipped,"failed":failed}

def accept_event(event_type,payload):
    explicit=payload.get("event_id") or payload.get("decision_id") or payload.get("id")
    canonical=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    key=f"{event_type}:{explicit or hashlib.sha256(canonical.encode()).hexdigest()}"
    with LOCK,db() as con:
        if con.execute("SELECT event_key FROM accepted_events WHERE event_key=?",(key,)).fetchone():
            return False,{"duplicate":True}
        con.execute(
            "INSERT INTO accepted_events(event_key,event_type,created_at) VALUES(?,?,?)",
            (key,event_type,now_iso()),
        )
    return True,dispatch(event_type,payload)

def verify_signature(raw,provided):
    if not INTERNAL_SECRET or not provided:
        return False
    expected="sha256="+hmac.new(INTERNAL_SECRET.encode(),raw,hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,provided)

class Handler(http.server.BaseHTTPRequestHandler):
    server_version="NDSPTelegram/176"

    def log_message(self,format,*args):
        return

    def common(self,content_type="application/json; charset=utf-8"):
        self.send_header("Content-Type",content_type)
        self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.send_header("X-Frame-Options","SAMEORIGIN")

    def send_json(self,status_value,payload):
        body=json_bytes(payload)
        self.send_response(status_value)
        self.common()
        self.send_header("Content-Length",str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_raw(self):
        length=int(self.headers.get("Content-Length","0") or "0")
        if length<0 or length>MAX_BODY:
            raise ValueError("BODY_TOO_LARGE")
        return self.rfile.read(length)

    def read_json(self):
        raw=self.read_raw()
        return (json.loads(raw.decode("utf-8")) if raw else {}),raw

    def require_session(self):
        session=session_from_cookie(self.headers.get("Cookie",""))
        if not session:
            self.send_json(401,{"ok":False,"code":"AUTH_REQUIRED"})
        return session

    def same_origin(self):
        origin=self.headers.get("Origin","").rstrip("/")
        referer=self.headers.get("Referer","")
        return (not origin or origin==BASE_URL) and (not referer or referer.startswith(BASE_URL+"/"))

    def do_GET(self):
        path=urllib.parse.urlsplit(self.path).path
        if path=="/api/telegram/health":
            self.send_json(200,{
                "ok":True,
                "service":"ndsp-telegram-notifications-v182",
                "configured":bool(BOT_TOKEN and BOT_USERNAME),
                "bot_username":BOT_USERNAME,
            })
            return
        session=self.require_session()
        if not session:
            return
        if path=="/api/telegram/status":
            self.send_json(200,status(session))
        elif path=="/api/telegram/history":
            self.send_json(200,{"ok":True,"items":history(session["user_key"])})
        else:
            self.send_json(404,{"ok":False,"code":"NOT_FOUND"})

    def do_POST(self):
        path=urllib.parse.urlsplit(self.path).path

        if WEBHOOK_PATH and path==f"/api/telegram/webhook/{WEBHOOK_PATH}":
            if WEBHOOK_SECRET:
                provided=self.headers.get("X-Telegram-Bot-Api-Secret-Token","")
                if not hmac.compare_digest(provided,WEBHOOK_SECRET):
                    self.send_json(403,{"ok":False})
                    return
            try:
                update,_=self.read_json()
            except Exception:
                self.send_json(400,{"ok":False})
                return
            message=update.get("message") or {}
            text=str(message.get("text") or "").strip()
            chat_id=(message.get("chat") or {}).get("id")
            if text.startswith("/start"):
                parts=text.split(maxsplit=1)
                if len(parts)==2:
                    linked,bound=bind_code(parts[1].strip(),message)
                    if linked:
                        try:
                            send_message(bound,"تم ربط حساب NDSP بنجاح.\nيمكنك الآن إدارة التنبيهات من لوحة المستخدم.")
                        except Exception:
                            pass
                    elif chat_id:
                        try:
                            send_message(chat_id,"رمز الربط غير صالح أو انتهت مدته.")
                        except Exception:
                            pass
            elif text.startswith("/stop") and chat_id:
                with LOCK,db() as con:
                    con.execute("UPDATE bindings SET active=0,updated_at=? WHERE chat_id=?",(now_iso(),str(chat_id)))
            self.send_json(200,{"ok":True})
            return

        if path=="/api/telegram/events":
            try:
                payload,raw=self.read_json()
            except Exception:
                self.send_json(400,{"ok":False,"code":"INVALID_JSON"})
                return
            if not verify_signature(raw,self.headers.get("X-NDSP-Telegram-Signature","")):
                self.send_json(403,{"ok":False,"code":"INVALID_SIGNATURE"})
                return
            event_type=str(payload.get("event_type") or "decision_complete")
            if event_type not in {"decision_complete","scenario_change","level_update","daily_brief"}:
                self.send_json(400,{"ok":False,"code":"INVALID_EVENT_TYPE"})
                return
            event_payload=payload.get("payload")
            if not isinstance(event_payload,dict):
                event_payload=payload
            accepted,result=accept_event(event_type,event_payload)
            self.send_json(202,{"ok":True,"accepted":accepted,"result":result})
            return

        session=self.require_session()
        if not session:
            return
        if not self.same_origin():
            self.send_json(403,{"ok":False,"code":"ORIGIN_REJECTED"})
            return
        try:
            payload,_=self.read_json()
        except Exception:
            self.send_json(400,{"ok":False,"code":"INVALID_JSON"})
            return

        if path=="/api/telegram/link":
            try:
                self.send_json(200,create_link(session))
            except RuntimeError as error:
                self.send_json(409,{"ok":False,"code":str(error)})
        elif path=="/api/telegram/preferences":
            try:
                update_preferences(session["user_key"],payload)
                self.send_json(200,status(session))
            except Exception:
                self.send_json(400,{"ok":False,"code":"INVALID_PREFERENCES"})
        elif path=="/api/telegram/test":
            b=binding(session["user_key"])
            if not BOT_TOKEN:
                self.send_json(409,{"ok":False,"code":"TELEGRAM_NOT_CONFIGURED"})
            elif not b or not b.get("active") or not b.get("chat_id"):
                self.send_json(409,{"ok":False,"code":"TELEGRAM_NOT_LINKED"})
            else:
                try:
                    send_message(b["chat_id"],"NDSP — رسالة اختبار\nتم ربط تنبيهات Telegram بنجاح.\n\nهذه قراءة تفسيرية وليست أمر شراء أو بيع.")
                    log_delivery(session["user_key"],"test","sent","Telegram test")
                    self.send_json(200,{"ok":True})
                except Exception:
                    self.send_json(502,{"ok":False,"code":"TELEGRAM_SEND_FAILED"})
        elif path=="/api/telegram/disconnect":
            with LOCK,db() as con:
                con.execute("UPDATE bindings SET active=0,updated_at=? WHERE user_key=?",(now_iso(),session["user_key"]))
            self.send_json(200,{"ok":True})
        else:
            self.send_json(404,{"ok":False,"code":"NOT_FOUND"})

def self_test():
    init_db()
    assert "BTCUSDT" in message_for("decision_complete",{"symbol":"BTCUSDT"})
    print("SELF_TEST=PASS")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    if args.self_test:
        self_test()
        return
    init_db()
    server=http.server.ThreadingHTTPServer(("127.0.0.1",PORT),Handler)
    server.daemon_threads=True
    server.serve_forever()

if __name__=="__main__":
    main()

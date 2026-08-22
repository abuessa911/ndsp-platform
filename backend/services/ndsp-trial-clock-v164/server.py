#!/usr/bin/env python3

import datetime as dt
import http.client
import http.server
import json
import os
import sqlite3
import ssl
import threading
import urllib.parse

PORT=int(os.environ.get("PORT","9089"))
LEDGER_DB=os.environ["LEDGER_DB"]
SESSION_URL=os.environ.get(
    "SESSION_URL",
    "https://api.ndsp.app/api/auth/session",
)
REGISTER_URL=os.environ.get(
    "REGISTER_URL",
    "http://127.0.0.1:9028/api/register",
)
STATUS_URL=os.environ.get(
    "STATUS_URL",
    "http://127.0.0.1:9001/api/trial/status",
)
TRIAL_DAYS=16
LOCK=threading.Lock()
MARKER="v164"

def utc_now():
    return dt.datetime.now(dt.timezone.utc)

def iso(value):
    return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00","Z")

def parse_date(value):
    if value in (None,""):
        return None

    try:
        parsed=dt.datetime.fromisoformat(str(value).replace("Z","+00:00"))

        if parsed.tzinfo is None:
            parsed=parsed.replace(tzinfo=dt.timezone.utc)

        return parsed.astimezone(dt.timezone.utc)
    except Exception:
        return None

def init_db():
    os.makedirs(os.path.dirname(LEDGER_DB),exist_ok=True)

    with sqlite3.connect(LEDGER_DB) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS trial_clock (
                user_key TEXT PRIMARY KEY,
                user_id TEXT,
                email TEXT,
                trial_started_at TEXT NOT NULL,
                trial_ends_at TEXT NOT NULL,
                duration_days INTEGER NOT NULL,
                source TEXT NOT NULL,
                source_reference TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS "
            "trial_clock_email_idx ON trial_clock(email) "
            "WHERE email IS NOT NULL AND email<>''"
        )
        connection.commit()

def flatten(value,output=None):
    if output is None:
        output=[]

    if isinstance(value,dict):
        for key,item in value.items():
            output.append((str(key).lower(),item))
            flatten(item,output)
    elif isinstance(value,list):
        for item in value:
            flatten(item,output)

    return output

def first_value(data,terms):
    rows=flatten(data)

    for term in terms:
        for key,value in rows:
            if (
                term in key
                and not isinstance(value,(dict,list))
                and value not in (None,"")
            ):
                return str(value)

    return ""

def identity_from(data,headers=None):
    headers=headers or {}

    user_id=first_value(
        data,
        ["user_id","account_id","subject","sub","id"],
    )
    email=first_value(
        data,
        ["email_address","user_email","email"],
    ).strip().lower()

    if not user_id:
        user_id=str(headers.get("x-ndsp-user-id","")).strip()

    if not email:
        email=str(headers.get("x-ndsp-user-email","")).strip().lower()

    return user_id,email

def user_key(user_id,email):
    if user_id:
        return "id:"+str(user_id)

    if email:
        return "email:"+email.lower()

    return ""

def put_clock(
    user_id,
    email,
    started_at,
    source,
    source_reference="",
):
    started=parse_date(started_at)

    if not started:
        raise ValueError("invalid trial start")

    ends=started+dt.timedelta(days=TRIAL_DAYS)
    key=user_key(user_id,email)

    if not key:
        raise ValueError("missing user identity")

    now=iso(utc_now())

    with LOCK:
        with sqlite3.connect(LEDGER_DB) as connection:
            connection.execute(
                """
                INSERT INTO trial_clock (
                    user_key,
                    user_id,
                    email,
                    trial_started_at,
                    trial_ends_at,
                    duration_days,
                    source,
                    source_reference,
                    created_at,
                    updated_at
                )
                VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(user_key) DO UPDATE SET
                    user_id=excluded.user_id,
                    email=excluded.email,
                    updated_at=excluded.updated_at
                """,
                (
                    key,
                    str(user_id or ""),
                    str(email or "").lower(),
                    iso(started),
                    iso(ends),
                    TRIAL_DAYS,
                    source,
                    source_reference,
                    now,
                    now,
                ),
            )
            connection.commit()

    return get_clock(user_id,email)

def get_clock(user_id,email):
    key=user_key(user_id,email)

    with sqlite3.connect(LEDGER_DB) as connection:
        connection.row_factory=sqlite3.Row
        row=None

        if key:
            row=connection.execute(
                "SELECT * FROM trial_clock WHERE user_key=?",
                (key,),
            ).fetchone()

        if row is None and email:
            row=connection.execute(
                "SELECT * FROM trial_clock WHERE lower(email)=lower(?)",
                (email,),
            ).fetchone()

        if row is None and user_id:
            row=connection.execute(
                "SELECT * FROM trial_clock WHERE user_id=?",
                (str(user_id),),
            ).fetchone()

    return dict(row) if row else None

def trial_payload(row):
    start=parse_date(row["trial_started_at"])
    end=parse_date(row["trial_ends_at"])
    now=utc_now()
    remaining_seconds=(end-now).total_seconds()
    remaining=max(0,int((remaining_seconds+86399)//86400))
    active=remaining_seconds>0

    return {
        "trial_started_at":iso(start),
        "trial_ends_at":iso(end),
        "trial_days":TRIAL_DAYS,
        "trial_days_remaining":remaining,
        "trial_active":active,
        "trial_status":"ACTIVE" if active else "EXPIRED",
        "trial_clock_source":row["source"],
        "trial_clock_authoritative":True,
        "trial_clock_server_recorded":True,
    }

def filtered_request_headers(headers):
    output={}

    for key,value in headers.items():
        lowered=key.lower()

        if lowered in {
            "host",
            "content-length",
            "connection",
            "accept-encoding",
        }:
            continue

        output[key]=value

    return output

def request_upstream(url,method,headers,body=b""):
    target=urllib.parse.urlsplit(url)
    path=target.path or "/"

    if target.query:
        path+="?"+target.query

    if target.scheme=="https":
        connection=http.client.HTTPSConnection(
            target.hostname,
            target.port or 443,
            timeout=30,
            context=ssl.create_default_context(),
        )
    else:
        connection=http.client.HTTPConnection(
            target.hostname,
            target.port or 80,
            timeout=30,
        )

    request_headers=filtered_request_headers(headers)

    if body:
        request_headers["Content-Length"]=str(len(body))

    connection.request(
        method,
        path,
        body=body if body else None,
        headers=request_headers,
    )

    response=connection.getresponse()
    raw=response.read()
    response_headers=response.getheaders()
    status=response.status
    connection.close()

    try:
        data=json.loads(raw.decode("utf-8"))
    except Exception:
        data=None

    return status,response_headers,raw,data

def merge_trial(data,trial):
    output=dict(data) if isinstance(data,dict) else {}
    output.update(trial)
    nested=output.get("trial")

    if not isinstance(nested,dict):
        nested={}

    nested.update(trial)
    nested["duration_days"]=TRIAL_DAYS
    output["trial"]=nested
    return output

def current_identity(headers):
    status,_,_,data=request_upstream(
        SESSION_URL,
        "GET",
        headers,
    )

    if status!=200 or not isinstance(data,dict):
        return None,None,data

    user_id,email=identity_from(data,headers)
    return user_id,email,data

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version="HTTP/1.1"

    def log_message(self,format,*args):
        print(
            "%s - - [%s] %s"
            % (
                self.client_address[0],
                self.log_date_time_string(),
                format%args,
            ),
            flush=True,
        )

    def begin_common_headers(self):
        self.send_header("X-NDSP-Trial-Clock",MARKER)

    def send_payload(self,status,headers,raw):
        excluded={
            "content-length",
            "content-encoding",
            "transfer-encoding",
            "connection",
            "x-ndsp-trial-clock",
        }

        self.send_response(status)

        for key,value in headers:
            if key.lower() in excluded:
                continue
            self.send_header(key,value)

        self.begin_common_headers()
        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(raw)

    def send_json(self,status,data,headers=None,extra=None):
        raw=json.dumps(
            data,
            ensure_ascii=False,
            separators=(",",":"),
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )

        for key,value in headers or []:
            lowered=key.lower()

            if lowered in {
                "content-length",
                "content-type",
                "content-encoding",
                "transfer-encoding",
                "connection",
                "x-ndsp-trial-clock",
            }:
                continue

            self.send_header(key,value)

        self.begin_common_headers()

        for key,value in extra or []:
            self.send_header(key,value)

        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        path=urllib.parse.urlsplit(self.path).path
        headers=dict(self.headers.items())

        if path=="/health":
            self.send_json(
                200,
                {
                    "ok":True,
                    "service":"ndsp-trial-clock-v164",
                    "port":PORT,
                    "ledger":LEDGER_DB,
                    "trial_days":TRIAL_DAYS,
                    "synthetic_clock":False,
                },
            )
            return

        if path=="/api/register":
            self.send_json(
                405,
                {
                    "ok":False,
                    "error":"METHOD_NOT_ALLOWED",
                    "required_method":"POST",
                },
                extra=[("Allow","POST")],
            )
            return

        if path=="/api/auth/session":
            status,response_headers,raw,data=request_upstream(
                SESSION_URL,
                "GET",
                headers,
            )

            if status!=200 or not isinstance(data,dict):
                self.send_payload(status,response_headers,raw)
                return

            user_id,email=identity_from(data,headers)
            row=get_clock(user_id,email)

            if row:
                data=merge_trial(data,trial_payload(row))
                self.send_json(200,data,response_headers)
                return

            self.send_payload(status,response_headers,raw)
            return

        if path=="/api/trial/status":
            user_id,email,session_data=current_identity(headers)

            status,response_headers,raw,data=request_upstream(
                STATUS_URL,
                "GET",
                headers,
            )

            if status!=200 or not isinstance(data,dict):
                self.send_payload(status,response_headers,raw)
                return

            row=get_clock(user_id,email)

            if row:
                data=merge_trial(data,trial_payload(row))
                self.send_json(200,data,response_headers)
                return

            self.send_payload(status,response_headers,raw)
            return

        self.send_json(404,{"ok":False,"error":"NOT_FOUND"})

    def do_POST(self):
        path=urllib.parse.urlsplit(self.path).path
        headers=dict(self.headers.items())
        length=int(self.headers.get("Content-Length","0") or "0")
        body=self.rfile.read(length) if length>0 else b""

        if path!="/api/register":
            self.send_json(404,{"ok":False,"error":"NOT_FOUND"})
            return

        status,response_headers,raw,data=request_upstream(
            REGISTER_URL,
            "POST",
            headers,
            body,
        )

        if status in {200,201}:
            try:
                request_data=json.loads(body.decode("utf-8"))
            except Exception:
                request_data={}

            response_data=data if isinstance(data,dict) else {}
            user_id,email=identity_from(response_data,headers)

            if not email:
                email=str(
                    request_data.get("email")
                    or request_data.get("user_email")
                    or ""
                ).strip().lower()

            if not user_id:
                user_id=str(
                    response_data.get("user_id")
                    or response_data.get("id")
                    or ""
                ).strip()

            if email or user_id:
                put_clock(
                    user_id,
                    email,
                    utc_now(),
                    "registration_success_201",
                    "my.ndsp.app/api/register",
                )

        self.send_payload(status,response_headers,raw)

def main():
    init_db()
    server=http.server.ThreadingHTTPServer(
        ("127.0.0.1",PORT),
        Handler,
    )
    print(
        "NDSP_TRIAL_CLOCK_V164_LISTENING "
        f"PORT={PORT} LEDGER={LEDGER_DB}",
        flush=True,
    )
    server.serve_forever()

if __name__=="__main__":
    main()

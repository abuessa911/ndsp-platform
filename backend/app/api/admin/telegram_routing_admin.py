from __future__ import annotations

import os
import json
import urllib.parse
import urllib.request
from typing import Optional

import psycopg2
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin/telegram-routing", tags=["telegram-routing-admin"])

def _read_env_file(path: str) -> None:
    try:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k,v=line.split("=",1)
                k=k.strip()
                v=v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k]=v
    except Exception:
        pass

_read_env_file("/etc/ndsp/ndsp-telegram.env")
_read_env_file("/etc/ndsp/ndsp-telegram-routing.env")
_read_env_file("/etc/ndsp/ndsp-db.env")
_read_env_file("/home/nawaf511/empire-core-new/backend/.env")

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)

def _admin_candidates():
    return [
        env("NDSP_ADMIN_ACTION_KEY"),
        env("NDSP_ADMIN_KEY"),
        env("ADMIN_KEY"),
        env("X_ADMIN_KEY"),
    ]

def admin_key_ok(v: Optional[str]) -> bool:
    return bool(v and any(x and v == x for x in _admin_candidates()))

def pick_admin_key(
    x_admin_key: Optional[str],
    x_ndsp_admin_key: Optional[str],
    x_ndsp_admin_action_key: Optional[str],
    authorization: Optional[str],
) -> Optional[str]:
    if x_admin_key:
        return x_admin_key
    if x_ndsp_admin_key:
        return x_ndsp_admin_key
    if x_ndsp_admin_action_key:
        return x_ndsp_admin_action_key
    if authorization and authorization.lower().startswith("bearer "):
        return authorization.split(" ",1)[1].strip()
    return None

def require_admin(
    x_admin_key: Optional[str],
    x_ndsp_admin_key: Optional[str],
    x_ndsp_admin_action_key: Optional[str],
    authorization: Optional[str],
) -> None:
    provided = pick_admin_key(x_admin_key, x_ndsp_admin_key, x_ndsp_admin_action_key, authorization)
    if not admin_key_ok(provided):
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

def db_conn():
    dsn = env("DATABASE_URL") or env("NDSP_DATABASE_URL")
    if dsn:
        return psycopg2.connect(dsn)
    password = env("POSTGRES_PASSWORD", "")
    kwargs = {
        "dbname": env("POSTGRES_DB", "ndsp_auth"),
        "user": env("POSTGRES_USER", "postgres"),
        "host": env("POSTGRES_HOST", "127.0.0.1"),
        "port": env("POSTGRES_PORT", "5432"),
    }
    if password:
        kwargs["password"] = password
    return psycopg2.connect(**kwargs)

def mask_chat_id(v: Optional[str]) -> Optional[str]:
    if not v:
        return None
    if len(v) <= 8:
        return "********"
    return v[:4] + "********" + v[-4:]

def ensure_table():
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_telegram_delivery_routes (
              id SERIAL PRIMARY KEY,
              plan_code TEXT UNIQUE NOT NULL,
              enabled BOOLEAN NOT NULL DEFAULT false,
              target_type TEXT NOT NULL DEFAULT 'channel',
              chat_id TEXT,
              daily_limit INTEGER,
              description TEXT,
              last_test_ok BOOLEAN,
              last_test_at TIMESTAMPTZ,
              last_test_message TEXT,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)
            cur.execute("""
            ALTER TABLE ndsp_telegram_delivery_routes
              ADD COLUMN IF NOT EXISTS last_test_ok BOOLEAN,
              ADD COLUMN IF NOT EXISTS last_test_at TIMESTAMPTZ,
              ADD COLUMN IF NOT EXISTS last_test_message TEXT;
            """)
            cur.execute("""
            INSERT INTO ndsp_telegram_delivery_routes
            (plan_code, enabled, target_type, chat_id, daily_limit, description)
            VALUES
            ('free', false, 'none', NULL, 0, 'Free package has no Telegram alerts'),
            ('pro', true, 'channel', '-1003491841685', 25, 'Pro limited Telegram alerts'),
            ('elite', true, 'channel', '-1003793881886', 250, 'Elite advanced Telegram alerts'),
            ('saas', true, 'channel', '-1003918395339', NULL, 'SaaS contract-based Telegram alerts'),
            ('institutional_suite', true, 'channel', '-1003918395339', NULL, 'Institutional Suite contract-based alerts')
            ON CONFLICT (plan_code) DO NOTHING;
            """)

class RouteUpdate(BaseModel):
    plan_code: str
    enabled: bool
    chat_id: Optional[str] = None
    daily_limit: Optional[int] = None
    description: Optional[str] = None

class TestPayload(BaseModel):
    plan_code: str
    text: Optional[str] = None

@router.get("/status")
def status(
    x_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_action_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    require_admin(x_admin_key, x_ndsp_admin_key, x_ndsp_admin_action_key, authorization)
    ensure_table()
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            SELECT plan_code, enabled, target_type, chat_id, daily_limit, description,
                   last_test_ok, last_test_at, last_test_message, updated_at
            FROM ndsp_telegram_delivery_routes
            ORDER BY CASE plan_code
              WHEN 'pro' THEN 1
              WHEN 'elite' THEN 2
              WHEN 'saas' THEN 3
              WHEN 'institutional_suite' THEN 4
              WHEN 'free' THEN 5
              ELSE 99
            END;
            """)
            rows = cur.fetchall()
    routes = []
    for r in rows:
        routes.append({
            "plan_code": r[0],
            "enabled": r[1],
            "target_type": r[2],
            "chat_id": r[3],
            "chat_id_masked": mask_chat_id(r[3]),
            "daily_limit": r[4],
            "description": r[5],
            "last_test_ok": r[6],
            "last_test_at": str(r[7]) if r[7] else None,
            "last_test_message": r[8],
            "updated_at": str(r[9]) if r[9] else None,
        })
    return {
        "ok": True,
        "summary": {
            "enabled_channels": sum(1 for x in routes if x["enabled"] and x["plan_code"] != "free"),
            "configured_channels": sum(1 for x in routes if x["chat_id"] and x["plan_code"] != "free"),
            "total_routes": len(routes),
        },
        "routes": routes,
    }

@router.post("/update")
def update(
    payload: RouteUpdate,
    x_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_action_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    require_admin(x_admin_key, x_ndsp_admin_key, x_ndsp_admin_action_key, authorization)
    ensure_table()
    plan = payload.plan_code.strip().lower()
    allowed = {"free", "pro", "elite", "saas", "institutional_suite"}
    if plan not in allowed:
        raise HTTPException(status_code=400, detail="INVALID_PLAN_CODE")
    chat_id = payload.chat_id.strip() if payload.chat_id else None
    if plan != "free" and payload.enabled and not chat_id:
        raise HTTPException(status_code=400, detail="CHAT_ID_REQUIRED_WHEN_ENABLED")
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            INSERT INTO ndsp_telegram_delivery_routes
            (plan_code, enabled, target_type, chat_id, daily_limit, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (plan_code) DO UPDATE SET
              enabled=EXCLUDED.enabled,
              target_type=EXCLUDED.target_type,
              chat_id=EXCLUDED.chat_id,
              daily_limit=EXCLUDED.daily_limit,
              description=EXCLUDED.description,
              updated_at=now()
            RETURNING plan_code, enabled, target_type, chat_id, daily_limit, description, updated_at;
            """, (
                plan,
                payload.enabled,
                "none" if plan == "free" else "channel",
                None if plan == "free" else chat_id,
                payload.daily_limit,
                payload.description or "",
            ))
            r = cur.fetchone()
    return {"ok": True, "route": {
        "plan_code": r[0],
        "enabled": r[1],
        "target_type": r[2],
        "chat_id_masked": mask_chat_id(r[3]),
        "daily_limit": r[4],
        "description": r[5],
        "updated_at": str(r[6]),
    }}

@router.post("/test")
def test_send(
    payload: TestPayload,
    x_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_key: Optional[str] = Header(default=None),
    x_ndsp_admin_action_key: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
):
    require_admin(x_admin_key, x_ndsp_admin_key, x_ndsp_admin_action_key, authorization)
    ensure_table()
    token = env("TELEGRAM_BOT_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN_MISSING")
    plan = payload.plan_code.strip().lower()
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("SELECT enabled, chat_id FROM ndsp_telegram_delivery_routes WHERE plan_code=%s LIMIT 1;", (plan,))
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="ROUTE_NOT_FOUND")
    enabled, chat_id = row
    if not enabled:
        raise HTTPException(status_code=400, detail="ROUTE_DISABLED")
    if not chat_id:
        raise HTTPException(status_code=400, detail="CHAT_ID_MISSING")
    text = payload.text or f"NDSP Admin Telegram Channel Test — {plan.upper()}"
    data = urllib.parse.urlencode({"chat_id": chat_id, "text": text, "disable_web_page_preview": "true"}).encode()
    ok = False
    detail = ""
    parsed = {}
    try:
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", "replace")
            code = resp.status
        parsed = json.loads(body)
        ok = bool(parsed.get("ok"))
        detail = "تم الإرسال بنجاح" if ok else json.dumps(parsed, ensure_ascii=False)
    except Exception as e:
        code = 0
        detail = f"TELEGRAM_SEND_FAILED: {e}"
        ok = False
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            UPDATE ndsp_telegram_delivery_routes
            SET last_test_ok=%s, last_test_at=now(), last_test_message=%s, updated_at=now()
            WHERE plan_code=%s;
            """, (ok, detail[:1000], plan))
    if not ok:
        raise HTTPException(status_code=502, detail=detail)
    return {
        "ok": True,
        "http_code": code,
        "plan_code": plan,
        "chat_id_masked": mask_chat_id(chat_id),
        "message": detail,
        "telegram": {"ok": parsed.get("ok"), "message_id": ((parsed.get("result") or {}).get("message_id"))},
    }

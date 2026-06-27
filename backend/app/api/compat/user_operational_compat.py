from __future__ import annotations

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any

import psycopg2
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["ndsp-user-operational-compat"])

def read_env_file(path: str) -> None:
    try:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass

for f in [
    "/etc/ndsp/ndsp-db.env",
    "/etc/ndsp/ndsp-api.env",
    "/etc/ndsp/ndsp-telegram.env",
    "/etc/ndsp/ndsp-telegram-routing.env",
    "/home/nawaf511/empire-core-new/backend/.env",
]:
    read_env_file(f)

def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)

def db_conn():
    dsn = (env("DATABASE_URL") or env("NDSP_DATABASE_URL") or "").strip().strip('"').strip("'")
    if dsn and "://" in dsn:
        return psycopg2.connect(dsn)

    kwargs = {
        "dbname": env("POSTGRES_DB", "ndsp_auth"),
        "user": env("POSTGRES_USER", "ndsp_auth"),
        "host": env("POSTGRES_HOST", "127.0.0.1"),
        "port": env("POSTGRES_PORT", "5432"),
    }
    password = env("POSTGRES_PASSWORD", "")
    if password:
        kwargs["password"] = password
    return psycopg2.connect(**kwargs)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

async def body_json(request: Request) -> Dict[str, Any]:
    try:
        return await request.json()
    except Exception:
        return {}

def normalize_email(v: Any) -> str:
    return str(v or "").strip().lower()

def ensure_compat_tables() -> None:
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_user_alert_preferences (
              id SERIAL PRIMARY KEY,
              email TEXT UNIQUE,
              user_id TEXT,
              in_app BOOLEAN NOT NULL DEFAULT true,
              email_enabled BOOLEAN NOT NULL DEFAULT true,
              telegram_enabled BOOLEAN NOT NULL DEFAULT false,
              telegram_id TEXT,
              preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
              updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS ndsp_operational_compat_audit (
              id SERIAL PRIMARY KEY,
              route TEXT NOT NULL,
              email TEXT,
              payload JSONB NOT NULL DEFAULT '{}'::jsonb,
              created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """)
            cur.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE ndsp_user_alert_preferences TO ndsp_auth;")
            cur.execute("GRANT SELECT, INSERT ON TABLE ndsp_operational_compat_audit TO ndsp_auth;")

def audit(route: str, email: str, payload: Dict[str, Any]) -> None:
    try:
        ensure_compat_tables()
        safe_payload = dict(payload or {})
        for k in list(safe_payload):
            if "password" in k.lower() or "token" in k.lower() or "secret" in k.lower():
                safe_payload[k] = "[redacted]"
        with db_conn() as con:
            with con.cursor() as cur:
                cur.execute(
                    "INSERT INTO ndsp_operational_compat_audit(route,email,payload) VALUES(%s,%s,%s::jsonb)",
                    (route, email or None, json.dumps(safe_payload, ensure_ascii=False)),
                )
    except Exception:
        pass

@router.get("/api/ndsp/compat/health")
def compat_health():
    return {
        "ok": True,
        "service": "ndsp-user-operational-compat",
        "timestamp": now_iso(),
        "routes": [
            "/api/trial/register",
            "/api/v1/trial/register",
            "/api/trial/request",
            "/api/auth/activate",
            "/api/v6/payments/nowpayments/subscription/create",
            "/api/payments/nowpayments/subscription/create",
            "/api/user/alert-preferences",
            "/api/telegram/link/start",
            "/api/telegram/link/verify",
            "/api/alerts/email/test",
        ],
    }

@router.post("/api/trial/register")
@router.post("/api/v1/trial/register")
@router.post("/api/trial/request")
@router.post("/api/auth/register-trial")
async def trial_register_compat(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("user_email"))
    name = str(payload.get("name") or payload.get("full_name") or "").strip()
    phone = str(payload.get("phone") or payload.get("mobile") or "").strip()

    audit("/api/trial/register", email, payload)

    if not email:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "EMAIL_REQUIRED"})

    try:
        with db_conn() as con:
            with con.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS ndsp_trial_activation_requests (
                  id SERIAL PRIMARY KEY,
                  email TEXT NOT NULL,
                  full_name TEXT,
                  phone TEXT,
                  requested_plan TEXT DEFAULT 'elite_trial',
                  status TEXT NOT NULL DEFAULT 'PENDING',
                  source TEXT DEFAULT 'compat',
                  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """)
                cur.execute("""
                INSERT INTO ndsp_trial_activation_requests(email, full_name, phone, requested_plan, status, source)
                VALUES(%s,%s,%s,%s,'PENDING','compat')
                RETURNING id, status, created_at;
                """, (email, name or None, phone or None, payload.get("plan") or "elite_trial"))
                row = cur.fetchone()
        return {
            "ok": True,
            "status": "pending_review",
            "message": "تم استلام طلب التجربة وسيتم مراجعته.",
            "request": {"id": row[0], "email": email, "status": row[1], "created_at": str(row[2])},
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"ok": False, "error": "TRIAL_REQUEST_FAILED", "message": str(exc)})

@router.post("/api/auth/activate")
@router.get("/api/auth/activate")
async def activate_compat(request: Request):
    if request.method == "GET":
        token = request.query_params.get("token") or request.query_params.get("code") or ""
        email = normalize_email(request.query_params.get("email"))
        payload = {"token": token, "email": email}
    else:
        payload = await body_json(request)
        token = str(payload.get("token") or payload.get("code") or payload.get("activation_token") or "").strip()
        email = normalize_email(payload.get("email"))

    audit("/api/auth/activate", email, payload)

    if not token and not email:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "TOKEN_OR_EMAIL_REQUIRED"})

    return {
        "ok": True,
        "status": "received",
        "message": "تم استقبال طلب التفعيل. إن كان الرمز صحيحًا سيتم تفعيل الحساب من مسار التفعيل الأساسي.",
        "requires_review": True,
    }

@router.get("/api/v6/payments/nowpayments/subscription/status")
@router.get("/api/payments/nowpayments/subscription/status")
async def subscription_status_compat(email: Optional[str] = None):
    email_norm = normalize_email(email)
    if not email_norm:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "EMAIL_REQUIRED"})

    try:
        with db_conn() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT plan_code, status, created_at, updated_at
                FROM ndsp_subscriptions
                WHERE lower(user_email)=lower(%s)
                ORDER BY updated_at DESC NULLS LAST, created_at DESC NULLS LAST
                LIMIT 1;
                """, (email_norm,))
                row = cur.fetchone()
        if not row:
            return {"ok": True, "found": False, "email": email_norm, "subscription": None}
        return {
            "ok": True,
            "found": True,
            "email": email_norm,
            "subscription": {
                "plan_code": row[0],
                "status": row[1],
                "created_at": str(row[2]) if row[2] else None,
                "updated_at": str(row[3]) if row[3] else None,
            },
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"ok": False, "error": "SUBSCRIPTION_STATUS_FAILED", "message": str(exc)})

@router.post("/api/v6/payments/nowpayments/subscription/create")
@router.post("/api/payments/nowpayments/subscription/create")
async def checkout_create_compat(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("user_email"))
    plan = str(payload.get("plan") or payload.get("plan_code") or "pro").strip().lower()

    audit("/api/v6/payments/nowpayments/subscription/create", email, payload)

    if not email:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "EMAIL_REQUIRED"})
    if plan not in {"pro", "elite", "saas", "institutional_suite"}:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "INVALID_PLAN"})

    try:
        with db_conn() as con:
            with con.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS ndsp_nowpayments_payments (
                  id SERIAL PRIMARY KEY,
                  user_email TEXT,
                  plan_code TEXT,
                  status TEXT NOT NULL DEFAULT 'pending_review',
                  amount NUMERIC,
                  currency TEXT DEFAULT 'USDT',
                  network TEXT,
                  payment_id TEXT,
                  invoice_url TEXT,
                  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """)
                cur.execute("""
                INSERT INTO ndsp_nowpayments_payments(user_email, plan_code, status, currency, network)
                VALUES(%s,%s,'pending_review','USDT',%s)
                RETURNING id, status, created_at;
                """, (email, plan, payload.get("network") or "TRC20"))
                row = cur.fetchone()

        return {
            "ok": True,
            "provider": "nowpayments",
            "mode": "manual_review_required",
            "payment": {
                "id": row[0],
                "email": email,
                "plan_code": plan,
                "status": row[1],
                "currency": "USDT",
                "network": payload.get("network") or "TRC20",
                "created_at": str(row[2]),
            },
            "message": "تم إنشاء طلب دفع قيد المراجعة اليدوية.",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail={"ok": False, "error": "CHECKOUT_CREATE_FAILED", "message": str(exc)})

@router.get("/api/user/alert-preferences")
async def alert_prefs_get(email: Optional[str] = None):
    email_norm = normalize_email(email)
    ensure_compat_tables()

    if not email_norm:
        return {
            "ok": True,
            "preferences": {
                "in_app": True,
                "email_enabled": True,
                "telegram_enabled": False,
                "telegram_id": None,
            },
            "default": True,
        }

    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            SELECT in_app, email_enabled, telegram_enabled, telegram_id, preferences, updated_at
            FROM ndsp_user_alert_preferences
            WHERE lower(email)=lower(%s)
            LIMIT 1;
            """, (email_norm,))
            row = cur.fetchone()

    if not row:
        return {
            "ok": True,
            "email": email_norm,
            "preferences": {
                "in_app": True,
                "email_enabled": True,
                "telegram_enabled": False,
                "telegram_id": None,
            },
            "default": True,
        }

    return {
        "ok": True,
        "email": email_norm,
        "preferences": {
            "in_app": row[0],
            "email_enabled": row[1],
            "telegram_enabled": row[2],
            "telegram_id": row[3],
            "extra": row[4] or {},
            "updated_at": str(row[5]) if row[5] else None,
        },
    }

@router.post("/api/user/alert-preferences")
async def alert_prefs_post(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("user_email"))
    telegram_id = str(payload.get("telegram_id") or payload.get("telegram") or "").strip() or None

    ensure_compat_tables()
    audit("/api/user/alert-preferences", email, payload)

    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            INSERT INTO ndsp_user_alert_preferences(email, in_app, email_enabled, telegram_enabled, telegram_id, preferences)
            VALUES(%s,%s,%s,%s,%s,%s::jsonb)
            ON CONFLICT (email) DO UPDATE SET
              in_app=EXCLUDED.in_app,
              email_enabled=EXCLUDED.email_enabled,
              telegram_enabled=EXCLUDED.telegram_enabled,
              telegram_id=EXCLUDED.telegram_id,
              preferences=EXCLUDED.preferences,
              updated_at=now()
            RETURNING email, in_app, email_enabled, telegram_enabled, telegram_id, updated_at;
            """, (
                email or None,
                bool(payload.get("in_app", True)),
                bool(payload.get("email_enabled", payload.get("email", True))),
                bool(payload.get("telegram_enabled", False)),
                telegram_id,
                json.dumps(payload, ensure_ascii=False),
            ))
            row = cur.fetchone()

    return {
        "ok": True,
        "preferences": {
            "email": row[0],
            "in_app": row[1],
            "email_enabled": row[2],
            "telegram_enabled": row[3],
            "telegram_id": row[4],
            "updated_at": str(row[5]),
        },
    }

@router.post("/api/telegram/link/start")
async def telegram_link_start(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("user_email"))
    audit("/api/telegram/link/start", email, payload)
    return {
        "ok": True,
        "status": "manual_link_required",
        "message": "أرسل /start للبوت ثم أدخل Telegram ID في الإعدادات.",
    }

@router.post("/api/telegram/link/verify")
async def telegram_link_verify(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("user_email"))
    telegram_id = str(payload.get("telegram_id") or payload.get("chat_id") or "").strip()
    audit("/api/telegram/link/verify", email, payload)

    if not telegram_id:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "TELEGRAM_ID_REQUIRED"})

    ensure_compat_tables()
    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            INSERT INTO ndsp_user_alert_preferences(email, telegram_enabled, telegram_id, preferences)
            VALUES(%s,true,%s,%s::jsonb)
            ON CONFLICT (email) DO UPDATE SET
              telegram_enabled=true,
              telegram_id=EXCLUDED.telegram_id,
              updated_at=now()
            RETURNING email, telegram_enabled, telegram_id, updated_at;
            """, (email or None, telegram_id, json.dumps({"source": "telegram_link_verify"}, ensure_ascii=False)))
            row = cur.fetchone()

    return {
        "ok": True,
        "linked": True,
        "email": row[0],
        "telegram_enabled": row[1],
        "telegram_id": row[2],
        "updated_at": str(row[3]),
    }

@router.post("/api/alerts/email/test")
async def email_test_compat(request: Request):
    payload = await body_json(request)
    email = normalize_email(payload.get("email") or payload.get("to"))
    audit("/api/alerts/email/test", email, payload)

    if not email:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "EMAIL_REQUIRED"})

    return {
        "ok": True,
        "queued": True,
        "mode": "compat_no_external_send",
        "email": email,
        "message": "تم قبول طلب اختبار البريد في وضع التوافق.",
    }

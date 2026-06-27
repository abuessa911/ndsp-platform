from __future__ import annotations

import os
import json
import time
import random
from typing import Any, Dict
from datetime import datetime, timezone

import psycopg2
from fastapi import APIRouter, Request, HTTPException

router = APIRouter(tags=["ndsp-nowpayments-create-alias"])

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

async def body_json(request: Request) -> Dict[str, Any]:
    try:
        return await request.json()
    except Exception:
        return {}

def normalize_email(v: Any) -> str:
    return str(v or "").strip().lower()

def make_order_id() -> str:
    return f"ndsp-pay-{int(time.time())}-{random.randint(100000, 999999)}"

@router.get("/api/ndsp/nowpayments-create-alias/health")
def health():
    return {
        "ok": True,
        "service": "ndsp-nowpayments-create-alias",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "routes": [
            "/api/v6/payments/nowpayments/subscription/create",
            "/api/payments/nowpayments/subscription/create",
        ],
    }

@router.post("/api/v6/payments/nowpayments/subscription/create")
@router.post("/api/payments/nowpayments/subscription/create")
async def create_subscription_payment(request: Request):
    payload = await body_json(request)

    email = normalize_email(payload.get("email") or payload.get("user_email"))
    plan = str(payload.get("plan") or payload.get("plan_code") or "pro").strip().lower()
    network = str(payload.get("network") or "TRC20").strip().upper()
    amount = payload.get("amount")
    billing_cycle = str(payload.get("billing_cycle") or "monthly").strip().lower()
    order_id = str(payload.get("order_id") or make_order_id()).strip()

    if not email:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "EMAIL_REQUIRED"})

    if plan not in {"pro", "elite", "saas", "institutional_suite"}:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "INVALID_PLAN"})

    if network not in {"TRC20", "BEP20"}:
        raise HTTPException(status_code=400, detail={"ok": False, "error": "INVALID_NETWORK", "allowed": ["TRC20", "BEP20"]})

    price_amount = amount if amount is not None else 0

    with db_conn() as con:
        with con.cursor() as cur:
            cur.execute("""
            INSERT INTO ndsp_nowpayments_payments
              (
                order_id,
                user_email,
                plan_code,
                billing_cycle,
                price_amount,
                price_currency,
                payment_status,
                status,
                amount,
                currency,
                network,
                raw_payload,
                raw_create_response,
                created_at,
                updated_at
              )
            VALUES
              (
                %s, %s, %s, %s, %s, 'usd',
                'created',
                'pending_review',
                %s, 'USDT', %s,
                %s::jsonb,
                %s::jsonb,
                now(),
                now()
              )
            RETURNING id, order_id, user_email, plan_code, status, payment_status, currency, network, created_at;
            """, (
                order_id,
                email,
                plan,
                billing_cycle,
                price_amount,
                amount,
                network,
                json.dumps(payload, ensure_ascii=False),
                json.dumps({"provider": "nowpayments", "mode": "manual_review_required"}, ensure_ascii=False),
            ))
            row = cur.fetchone()

    return {
        "ok": True,
        "provider": "nowpayments",
        "mode": "manual_review_required",
        "payment": {
            "id": row[0],
            "order_id": row[1],
            "email": row[2],
            "plan_code": row[3],
            "status": row[4],
            "payment_status": row[5],
            "currency": row[6],
            "network": row[7],
            "created_at": str(row[8]),
        },
        "message": "تم إنشاء طلب الدفع وهو بانتظار المراجعة اليدوية.",
    }

#!/usr/bin/env python3
# NDSP_BUSINESS_OPERATIONS_V205
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

HOST = os.environ.get("NDSP_OPS_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_OPS_PORT", "9094"))
DB_PATH = os.environ.get("NDSP_OPS_DB", "/var/lib/ndsp-business-ops/ops.sqlite3")
HASH_SALT = os.environ.get("NDSP_OPS_HASH_SALT", "")
LOCAL_PACKAGES_URL = os.environ.get("NDSP_LOCAL_PACKAGES_URL", "http://127.0.0.1:9022/api/packages")
LATEST_MONITOR = os.environ.get("NDSP_OPS_LATEST_MONITOR", "/var/lib/ndsp-business-ops/latest-monitor.json")
PUBLIC_BASE = os.environ.get("NDSP_PUBLIC_BASE", "https://my.ndsp.app")
LANDING_BASE = os.environ.get("NDSP_LANDING_BASE", "https://ndsp.app")
TRIAL_DAYS = 16
EMAIL_RE = re.compile(r"^[^\s@]{1,128}@[^\s@]{1,190}\.[^\s@]{2,63}$")
ALLOWED_STATUSES = {"new", "open", "pending", "in_progress", "waiting_user", "resolved", "closed", "rejected", "approved", "paid_verified", "activated"}
TABLES = {"leads", "support_tickets", "subscription_requests", "onboarding_events"}


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS leads (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              reference TEXT UNIQUE NOT NULL,
              created_at TEXT NOT NULL,
              name TEXT NOT NULL,
              email TEXT,
              phone TEXT,
              campaign TEXT,
              locale TEXT,
              consent INTEGER NOT NULL DEFAULT 0,
              source TEXT,
              status TEXT NOT NULL DEFAULT 'new',
              ip_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS support_tickets (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              reference TEXT UNIQUE NOT NULL,
              created_at TEXT NOT NULL,
              name TEXT NOT NULL,
              email TEXT NOT NULL,
              category TEXT NOT NULL,
              priority TEXT NOT NULL,
              subject TEXT NOT NULL,
              message TEXT NOT NULL,
              status TEXT NOT NULL DEFAULT 'open',
              ip_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS subscription_requests (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              reference TEXT UNIQUE NOT NULL,
              created_at TEXT NOT NULL,
              name TEXT NOT NULL,
              email TEXT NOT NULL,
              plan TEXT NOT NULL,
              payment_reference TEXT,
              notes TEXT,
              status TEXT NOT NULL DEFAULT 'pending',
              activation_mode TEXT NOT NULL DEFAULT 'manual_review',
              ip_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS onboarding_events (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              reference TEXT UNIQUE NOT NULL,
              created_at TEXT NOT NULL,
              email TEXT,
              event TEXT NOT NULL,
              metadata_json TEXT,
              status TEXT NOT NULL DEFAULT 'new',
              ip_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS rate_events (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              endpoint TEXT NOT NULL,
              ip_hash TEXT NOT NULL,
              created_epoch INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_rate_events_lookup ON rate_events(endpoint, ip_hash, created_epoch);
            CREATE TABLE IF NOT EXISTS monitor_checks (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              checked_at TEXT NOT NULL,
              overall_status TEXT NOT NULL,
              payload_json TEXT NOT NULL
            );
            """
        )


def clean(value: Any, limit: int = 500) -> str:
    text = str(value or "").strip()
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text[:limit]


def email_ok(value: str) -> bool:
    return bool(EMAIL_RE.match(value))


def make_ref(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"


def client_hash(handler: BaseHTTPRequestHandler) -> str:
    forwarded = handler.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    raw = forwarded or handler.headers.get("X-Real-IP", "") or handler.client_address[0]
    key = (HASH_SALT or "ndsp-ops-v205-local-salt").encode()
    return hmac.new(key, raw.encode(), hashlib.sha256).hexdigest()


def rate_allowed(endpoint: str, ip_hash: str, limit: int = 8, window: int = 3600) -> bool:
    now = int(time.time())
    with connect() as conn:
        conn.execute("DELETE FROM rate_events WHERE created_epoch < ?", (now - 86400,))
        count = conn.execute(
            "SELECT count(*) AS c FROM rate_events WHERE endpoint=? AND ip_hash=? AND created_epoch>=?",
            (endpoint, ip_hash, now - window),
        ).fetchone()["c"]
        if count >= limit:
            return False
        conn.execute("INSERT INTO rate_events(endpoint,ip_hash,created_epoch) VALUES(?,?,?)", (endpoint, ip_hash, now))
    return True


def load_plans() -> dict[str, Any]:
    try:
        req = urllib.request.Request(LOCAL_PACKAGES_URL, headers={"User-Agent": "NDSP-Business-Ops/204", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
        plans = data.get("packages") if isinstance(data, dict) else None
        if isinstance(plans, list) and plans:
            return {"ok": True, "source": "existing_ndsp_packages_api", "packages": plans}
    except Exception:
        pass
    return {
        "ok": True,
        "source": "governed_safe_catalog",
        "pricing_requires_confirmation": True,
        "packages": [
            {"code": "free", "name": "Free", "price": None, "trial_days": TRIAL_DAYS, "is_active": True},
            {"code": "pro", "name": "Pro", "price": None, "trial_days": TRIAL_DAYS, "is_active": True},
            {"code": "elite", "name": "Elite", "price": None, "trial_days": TRIAL_DAYS, "is_active": True},
            {"code": "institutional", "name": "Institutional", "price": None, "trial_days": 0, "is_active": True},
        ],
    }


def latest_monitor() -> dict[str, Any]:
    try:
        with open(LATEST_MONITOR, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {"overall_status": "PENDING_FIRST_CHECK", "checked_at": None}


class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPBusinessOps/204"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{utcnow()} {self.client_address[0]} {fmt % args}", flush=True)

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.end_headers()
        self.wfile.write(raw)

    def body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0 or length > 131072:
            raise ValueError("INVALID_BODY_SIZE")
        raw = self.rfile.read(length)
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON_OBJECT_REQUIRED")
        return data

    def admin_allowed(self) -> bool:
        return self.client_address[0] in {"127.0.0.1", "::1"} and self.headers.get("X-NDSP-Admin-Gate") == "1"

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Allow", "GET,POST,OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path in {"/health", "/api/ops/health"}:
            return self.send_json(200, {"ok": True, "service": "ndsp-business-ops", "version": "V205", "database": os.path.exists(DB_PATH)})
        if path == "/api/ops/public/config":
            return self.send_json(200, {
                "ok": True,
                "official_name": "NDSP — Nawaf Decision Support Platform",
                "trial_days": TRIAL_DAYS,
                "registration_url": f"{PUBLIC_BASE}/register/",
                "login_url": f"{PUBLIC_BASE}/login/",
                "landing_url": f"{LANDING_BASE}/",
                "subscription_activation_mode": "manual_review_after_payment_verification",
                "payment_auto_activation": False,
                "support_sla": {"urgent_hours": 4, "normal_hours": 24, "low_hours": 48},
                "decision_support_only": True,
            })
        if path == "/api/ops/public/plans":
            return self.send_json(200, load_plans())
        if path == "/api/ops/public/status":
            monitor = latest_monitor()
            return self.send_json(200, {"ok": True, "platform_status": monitor.get("overall_status", "UNKNOWN"), "checked_at": monitor.get("checked_at")})
        if path.startswith("/api/ops/admin/"):
            if not self.admin_allowed():
                return self.send_json(403, {"ok": False, "error": "ADMIN_GATE_REQUIRED"})
            if path == "/api/ops/admin/summary":
                return self.admin_summary()
            if path == "/api/ops/admin/export":
                return self.admin_export(parse_qs(parsed.query))
        return self.send_json(404, {"ok": False, "error": "NOT_FOUND", "path": path})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            data = self.body()
        except Exception as exc:
            return self.send_json(400, {"ok": False, "error": str(exc)})
        if clean(data.get("website"), 10):
            return self.send_json(202, {"ok": True})
        if path.startswith("/api/ops/admin/"):
            if not self.admin_allowed():
                return self.send_json(403, {"ok": False, "error": "ADMIN_GATE_REQUIRED"})
            if path == "/api/ops/admin/status":
                return self.admin_status(data)
        ip_hash = client_hash(self)
        if path == "/api/ops/public/lead":
            return self.public_lead(data, ip_hash)
        if path == "/api/ops/public/support":
            return self.public_support(data, ip_hash)
        if path == "/api/ops/public/subscription-request":
            return self.public_subscription(data, ip_hash)
        if path == "/api/ops/public/onboarding-event":
            return self.public_onboarding(data, ip_hash)
        return self.send_json(404, {"ok": False, "error": "NOT_FOUND", "path": path})

    def public_lead(self, data: dict[str, Any], ip_hash: str) -> None:
        name = clean(data.get("name"), 120)
        email = clean(data.get("email"), 254).lower()
        phone = clean(data.get("phone"), 40)
        if not name or (not email and not phone):
            return self.send_json(400, {"ok": False, "error": "NAME_AND_CONTACT_REQUIRED"})
        if email and not email_ok(email):
            return self.send_json(400, {"ok": False, "error": "INVALID_EMAIL"})
        if data.get("probe") is True:
            return self.send_json(200, {"ok": True, "probe": True})
        if not rate_allowed("lead", ip_hash):
            return self.send_json(429, {"ok": False, "error": "RATE_LIMITED"})
        ref = make_ref("LEAD")
        with connect() as conn:
            conn.execute(
                "INSERT INTO leads(reference,created_at,name,email,phone,campaign,locale,consent,source,status,ip_hash) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (ref, utcnow(), name, email, phone, clean(data.get("campaign"), 100), clean(data.get("locale"), 16), int(bool(data.get("consent"))), clean(data.get("source"), 100), "new", ip_hash),
            )
        return self.send_json(201, {"ok": True, "reference": ref, "status": "new"})

    def public_support(self, data: dict[str, Any], ip_hash: str) -> None:
        name = clean(data.get("name"), 120)
        email = clean(data.get("email"), 254).lower()
        category = clean(data.get("category"), 50) or "general"
        priority = clean(data.get("priority"), 20) or "normal"
        subject = clean(data.get("subject"), 180)
        message = clean(data.get("message"), 4000)
        if not name or not email_ok(email) or not subject or len(message) < 10:
            return self.send_json(400, {"ok": False, "error": "INVALID_SUPPORT_REQUEST"})
        if priority not in {"urgent", "normal", "low"}:
            priority = "normal"
        if data.get("probe") is True:
            return self.send_json(200, {"ok": True, "probe": True})
        if not rate_allowed("support", ip_hash, 6):
            return self.send_json(429, {"ok": False, "error": "RATE_LIMITED"})
        ref = make_ref("SUP")
        with connect() as conn:
            conn.execute(
                "INSERT INTO support_tickets(reference,created_at,name,email,category,priority,subject,message,status,ip_hash) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (ref, utcnow(), name, email, category, priority, subject, message, "open", ip_hash),
            )
        return self.send_json(201, {"ok": True, "reference": ref, "status": "open", "sla_hours": 4 if priority == "urgent" else 48 if priority == "low" else 24})

    def public_subscription(self, data: dict[str, Any], ip_hash: str) -> None:
        name = clean(data.get("name"), 120)
        email = clean(data.get("email"), 254).lower()
        plan = clean(data.get("plan"), 80).lower()
        payment_reference = clean(data.get("payment_reference"), 180)
        notes = clean(data.get("notes"), 1000)
        if not name or not email_ok(email) or not plan:
            return self.send_json(400, {"ok": False, "error": "INVALID_SUBSCRIPTION_REQUEST"})
        if data.get("probe") is True:
            return self.send_json(200, {"ok": True, "probe": True, "auto_activation": False})
        if not rate_allowed("subscription", ip_hash, 5):
            return self.send_json(429, {"ok": False, "error": "RATE_LIMITED"})
        ref = make_ref("SUB")
        with connect() as conn:
            conn.execute(
                "INSERT INTO subscription_requests(reference,created_at,name,email,plan,payment_reference,notes,status,activation_mode,ip_hash) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (ref, utcnow(), name, email, plan, payment_reference, notes, "pending", "manual_review", ip_hash),
            )
        return self.send_json(201, {"ok": True, "reference": ref, "status": "pending_manual_review", "payment_auto_activation": False})

    def public_onboarding(self, data: dict[str, Any], ip_hash: str) -> None:
        event = clean(data.get("event"), 80)
        email = clean(data.get("email"), 254).lower()
        allowed = {"start_viewed", "registration_clicked", "login_clicked", "decision_room_clicked", "guide_viewed"}
        if event not in allowed or (email and not email_ok(email)):
            return self.send_json(400, {"ok": False, "error": "INVALID_ONBOARDING_EVENT"})
        if data.get("probe") is True:
            return self.send_json(200, {"ok": True, "probe": True})
        if not rate_allowed("onboarding", ip_hash, 20):
            return self.send_json(429, {"ok": False, "error": "RATE_LIMITED"})
        ref = make_ref("ONB")
        metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
        with connect() as conn:
            conn.execute(
                "INSERT INTO onboarding_events(reference,created_at,email,event,metadata_json,status,ip_hash) VALUES(?,?,?,?,?,?,?)",
                (ref, utcnow(), email, event, json.dumps(metadata, ensure_ascii=False)[:2000], "new", ip_hash),
            )
        return self.send_json(201, {"ok": True, "reference": ref})

    def admin_summary(self) -> None:
        with connect() as conn:
            counts = {}
            for table in TABLES:
                counts[table] = conn.execute(f"SELECT count(*) AS c FROM {table}").fetchone()["c"]
            recent = {
                "leads": [dict(r) for r in conn.execute("SELECT id,reference,created_at,name,email,phone,campaign,status FROM leads ORDER BY id DESC LIMIT 20")],
                "support": [dict(r) for r in conn.execute("SELECT id,reference,created_at,name,email,category,priority,subject,status FROM support_tickets ORDER BY id DESC LIMIT 20")],
                "subscriptions": [dict(r) for r in conn.execute("SELECT id,reference,created_at,name,email,plan,payment_reference,status,activation_mode FROM subscription_requests ORDER BY id DESC LIMIT 20")],
                "onboarding": [dict(r) for r in conn.execute("SELECT id,reference,created_at,email,event,status FROM onboarding_events ORDER BY id DESC LIMIT 20")],
            }
        return self.send_json(200, {"ok": True, "version": "V205", "counts": counts, "recent": recent, "monitor": latest_monitor(), "payment_auto_activation": False})

    def admin_export(self, query: dict[str, list[str]]) -> None:
        table = clean((query.get("type") or [""])[0], 50)
        if table not in TABLES:
            return self.send_json(400, {"ok": False, "error": "INVALID_EXPORT_TYPE"})
        with connect() as conn:
            rows = [dict(r) for r in conn.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 5000")]
        for row in rows:
            row.pop("ip_hash", None)
        return self.send_json(200, {"ok": True, "type": table, "rows": rows})

    def admin_status(self, data: dict[str, Any]) -> None:
        table = clean(data.get("type"), 50)
        item_id = data.get("id")
        status = clean(data.get("status"), 40)
        if table not in TABLES or not isinstance(item_id, int) or status not in ALLOWED_STATUSES:
            return self.send_json(400, {"ok": False, "error": "INVALID_STATUS_UPDATE"})
        with connect() as conn:
            cur = conn.execute(f"UPDATE {table} SET status=? WHERE id=?", (status, item_id))
        if cur.rowcount != 1:
            return self.send_json(404, {"ok": False, "error": "ITEM_NOT_FOUND"})
        return self.send_json(200, {"ok": True, "type": table, "id": item_id, "status": status})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--init-only", action="store_true")
    args = parser.parse_args()
    init_db()
    if args.init_only:
        print("NDSP_BUSINESS_OPS_DB_INIT=PASS")
        return
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"NDSP business operations V205 listening on {HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

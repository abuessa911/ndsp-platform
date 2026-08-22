#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/var/www/ndsp/admin/admin-snapshot.json")

def q(sql):
    try:
        out = subprocess.check_output(
            ["sudo", "-u", "postgres", "psql", "-d", "ndsp_auth", "-At", "-c", sql],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        return out
    except Exception:
        return ""

def qi(sql):
    v = q(sql)
    try:
        return int(v or 0)
    except Exception:
        return 0

def table_exists(name):
    return q(f"SELECT to_regclass('public.{name}') IS NOT NULL;") == "t"

def col_exists(table, col):
    return q(f"""
SELECT EXISTS (
  SELECT 1 FROM information_schema.columns
  WHERE table_schema='public' AND table_name='{table}' AND column_name='{col}'
);
""") == "t"

users_total = qi("SELECT COUNT(*) FROM users;") if table_exists("users") else 0

active_users = 0
trial_users = 0
if table_exists("users"):
    if col_exists("users", "status"):
        active_users = qi("SELECT COUNT(*) FROM users WHERE lower(coalesce(status,'')) IN ('active','approved','enabled');")
    if col_exists("users", "trial_ends_at"):
        trial_users = qi("SELECT COUNT(*) FROM users WHERE trial_ends_at IS NOT NULL;")
    elif col_exists("users", "plan"):
        trial_users = qi("SELECT COUNT(*) FROM users WHERE lower(coalesce(plan,'')) LIKE '%trial%' OR lower(coalesce(plan,'')) LIKE '%elite%';")

pending_activations = 0
for t in ["trial_requests", "activation_requests", "plan_upgrade_requests", "payment_confirmations", "nowpayments_payments"]:
    if table_exists(t):
        if col_exists(t, "status"):
            pending_activations += qi(f"SELECT COUNT(*) FROM {t} WHERE lower(coalesce(status,'')) IN ('pending','pending_review','manual_review_required','awaiting','review');")

payments_total = 0
for t in ["nowpayments_payments", "payments", "payment_confirmations"]:
    if table_exists(t):
        payments_total += qi(f"SELECT COUNT(*) FROM {t};")

subscriptions_total = 0
for t in ["subscriptions", "user_subscriptions"]:
    if table_exists(t):
        subscriptions_total += qi(f"SELECT COUNT(*) FROM {t};")

feedback_total = qi("SELECT COUNT(*) FROM feedback_surveys;") if table_exists("feedback_surveys") else 0
notifications_total = qi("SELECT COUNT(*) FROM notifications;") if table_exists("notifications") else 0

cohorts = [
    {"key":"beginner","name_ar":"مستخدم مبتدئ","capacity":25,"reserved":0},
    {"key":"academic","name_ar":"متخصص / أكاديمي","capacity":10,"reserved":0},
    {"key":"premium","name_ar":"خاص مميز","capacity":15,"reserved":0},
]

if table_exists("users"):
    cat_col = None
    for c in ["category", "cohort", "trial_category", "user_category"]:
        if col_exists("users", c):
            cat_col = c
            break
    if cat_col:
        raw = q(f"SELECT coalesce({cat_col},'unknown') || '=' || COUNT(*) FROM users GROUP BY coalesce({cat_col},'unknown');")
        counts = {}
        for line in raw.splitlines():
            if "=" in line:
                k, v = line.rsplit("=", 1)
                try:
                    counts[k.lower()] = int(v)
                except Exception:
                    pass
        for c in cohorts:
            if c["key"] == "beginner":
                c["reserved"] = counts.get("beginner", 0) + counts.get("ordinary", 0) + counts.get("normal", 0)
            elif c["key"] == "academic":
                c["reserved"] = counts.get("academic", 0) + counts.get("specialist_academic", 0) + counts.get("specialist", 0)
            elif c["key"] == "premium":
                c["reserved"] = counts.get("premium", 0) + counts.get("private", 0) + counts.get("vip", 0)

seats_total = sum(c["capacity"] for c in cohorts)
seats_reserved = sum(c["reserved"] for c in cohorts)

payload = {
    "ok": True,
    "source": "ndsp_auth_admin_snapshot",
    "updated_at": datetime.now(timezone.utc).isoformat(),
    "users_total": users_total,
    "active_users": active_users,
    "trial_users": trial_users,
    "pending_activations": pending_activations,
    "seats_total": seats_total,
    "seats_reserved": seats_reserved,
    "payments_total": payments_total,
    "subscriptions_total": subscriptions_total,
    "feedback_total": feedback_total,
    "notifications_total": notifications_total,
    "cohorts": cohorts,
    "tables": {
        "users": table_exists("users"),
        "feedback_surveys": table_exists("feedback_surveys"),
        "notifications": table_exists("notifications"),
        "nowpayments_payments": table_exists("nowpayments_payments"),
        "subscriptions": table_exists("subscriptions")
    }
}

tmp = OUT.with_suffix(".tmp")
tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
tmp.replace(OUT)

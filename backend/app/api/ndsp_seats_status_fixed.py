import os
from pathlib import Path
from typing import Dict, Any

from fastapi import APIRouter

router = APIRouter()

ENV_FILE = Path("/etc/ndsp/ndsp-db.env")

def _load_env() -> Dict[str, str]:
    values: Dict[str, str] = {}
    if ENV_FILE.exists():
        for raw in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")

    for key, value in values.items():
        if value:
            os.environ[key] = value

    return values

def _connect():
    values = _load_env()

    host = values.get("PGHOST") or os.environ.get("PGHOST") or "127.0.0.1"
    port = int(values.get("PGPORT") or os.environ.get("PGPORT") or "5432")
    database = values.get("PGDATABASE") or os.environ.get("PGDATABASE") or "ndsp_auth"
    user = values.get("PGUSER") or os.environ.get("PGUSER") or "ndsp_auth"
    password = values.get("PGPASSWORD") or os.environ.get("PGPASSWORD") or values.get("DB_PASSWORD") or os.environ.get("DB_PASSWORD")

    try:
        import psycopg2
        return psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=5,
        )
    except ModuleNotFoundError:
        raise RuntimeError("psycopg2 is not installed in backend venv")

def _table_exists(cur, table_name: str) -> bool:
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = %s
        )
        """,
        (table_name,),
    )
    return bool(cur.fetchone()[0])

def _safe_count(cur, table: str, where_sql: str = "", params: tuple = ()) -> int:
    if not _table_exists(cur, table):
        return 0
    cur.execute(f"SELECT COUNT(*) FROM {table} {where_sql}", params)
    return int(cur.fetchone()[0] or 0)

@router.get("/api/seats/status")
def ndsp_seats_status() -> Dict[str, Any]:
    conn = None
    try:
        conn = _connect()
        cur = conn.cursor()

        # Trial seat policy:
        # 10 specialist/academic
        # 25 normal beginner
        # 15 premium/special invite-only
        quotas = {
            "specialist_academic": 10,
            "normal_beginner": 25,
            "premium_invite_only": 15,
            "total": 50,
        }

        users_table = "users"
        trial_table = "ndsp_trial_seats"
        invites_table = "ndsp_trial_invites"

        used = {
            "specialist_academic": 0,
            "normal_beginner": 0,
            "premium_invite_only": 0,
        }

        # Prefer dedicated table if it exists.
        if _table_exists(cur, trial_table):
            cur.execute(
                f"""
                SELECT COALESCE(cohort, user_type, seat_type, 'normal_beginner') AS cohort, COUNT(*)
                FROM {trial_table}
                GROUP BY 1
                """
            )
            for cohort, count in cur.fetchall():
                key = str(cohort or "").strip().lower()
                if key in used:
                    used[key] = int(count or 0)

        # Fallback to users table with flexible column discovery.
        elif _table_exists(cur, users_table):
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema='public' AND table_name=%s
                """,
                (users_table,),
            )
            columns = {r[0] for r in cur.fetchall()}

            cohort_col = None
            for c in ("trial_cohort", "cohort", "user_type", "seat_type", "trial_type"):
                if c in columns:
                    cohort_col = c
                    break

            plan_filter = ""
            params = []

            if "plan" in columns:
                plan_filter = "WHERE LOWER(COALESCE(plan::text,'')) LIKE %s"
                params.append("%trial%")
            elif "subscription_plan" in columns:
                plan_filter = "WHERE LOWER(COALESCE(subscription_plan::text,'')) LIKE %s"
                params.append("%trial%")
            elif "is_trial" in columns:
                plan_filter = "WHERE is_trial = TRUE"

            if cohort_col:
                cur.execute(
                    f"""
                    SELECT COALESCE({cohort_col}::text, 'normal_beginner') AS cohort, COUNT(*)
                    FROM {users_table}
                    {plan_filter}
                    GROUP BY 1
                    """,
                    tuple(params),
                )
                for cohort, count in cur.fetchall():
                    raw = str(cohort or "").strip().lower()
                    if raw in ("specialist", "academic", "specialist_academic", "professional", "expert"):
                        used["specialist_academic"] += int(count or 0)
                    elif raw in ("premium", "special", "premium_invite_only", "vip", "private"):
                        used["premium_invite_only"] += int(count or 0)
                    else:
                        used["normal_beginner"] += int(count or 0)
            else:
                total_users = _safe_count(cur, users_table, plan_filter, tuple(params))
                used["normal_beginner"] = total_users

        remaining = {
            "specialist_academic": max(0, quotas["specialist_academic"] - used["specialist_academic"]),
            "normal_beginner": max(0, quotas["normal_beginner"] - used["normal_beginner"]),
            "premium_invite_only": max(0, quotas["premium_invite_only"] - used["premium_invite_only"]),
        }

        premium_invites = {
            "required": True,
            "table_exists": _table_exists(cur, invites_table),
            "active": 0,
            "used": 0,
        }

        if premium_invites["table_exists"]:
            cur.execute(f"SELECT COUNT(*) FROM {invites_table} WHERE COALESCE(used,false)=false")
            premium_invites["active"] = int(cur.fetchone()[0] or 0)
            cur.execute(f"SELECT COUNT(*) FROM {invites_table} WHERE COALESCE(used,false)=true")
            premium_invites["used"] = int(cur.fetchone()[0] or 0)

        return {
            "ok": True,
            "source": "ndsp_seats_status_fixed",
            "policy": "50 trial seats: 10 specialist/academic, 25 normal beginner, 15 premium invite-only",
            "quotas": quotas,
            "used": {
                **used,
                "total": sum(used.values()),
            },
            "remaining": {
                **remaining,
                "total": sum(remaining.values()),
            },
            "premium_invite_only": premium_invites,
            "database": {
                "connected": True,
                "name": os.environ.get("PGDATABASE", "ndsp_auth"),
                "user": os.environ.get("PGUSER", "ndsp_auth"),
                "password_exposed": False,
            },
            "governance": {
                "payment_locked_during_trial": True,
                "telegram_alerts_expected_after_activation": True,
            },
        }
    except Exception as exc:
        return {
            "ok": False,
            "source": "ndsp_seats_status_fixed",
            "error": str(exc),
            "password_exposed": False,
        }
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

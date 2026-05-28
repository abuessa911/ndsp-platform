import os
from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter()


def _connect():
    import psycopg2

    return psycopg2.connect(
        host=os.environ.get("PGHOST") or os.environ.get("DB_HOST") or "127.0.0.1",
        port=int(os.environ.get("PGPORT") or os.environ.get("DB_PORT") or "5432"),
        dbname=os.environ.get("PGDATABASE") or os.environ.get("DB_NAME") or "ndsp_auth",
        user=os.environ.get("PGUSER") or os.environ.get("DB_USER") or "ndsp_auth",
        password=os.environ.get("PGPASSWORD") or os.environ.get("DB_PASSWORD") or os.environ.get("POSTGRES_PASSWORD"),
        connect_timeout=5,
    )


def _table_exists(cur, table_name: str) -> bool:
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema='public'
              AND table_name=%s
        )
        """,
        (table_name,),
    )
    return bool(cur.fetchone()[0])


def _columns(cur, table_name: str) -> set[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema='public'
          AND table_name=%s
        """,
        (table_name,),
    )
    return {str(r[0]) for r in cur.fetchall()}


@router.get("/api/seats/status")
def seats_status() -> Dict[str, Any]:
    quotas = {
        "specialist_academic": 10,
        "normal_beginner": 25,
        "premium_invite_only": 15,
        "total": 50,
    }

    used = {
        "specialist_academic": 0,
        "normal_beginner": 0,
        "premium_invite_only": 0,
    }

    premium_invites = {
        "required": True,
        "table_exists": False,
        "active": 0,
        "used": 0,
    }

    conn = None

    try:
        conn = _connect()
        cur = conn.cursor()

        if _table_exists(cur, "ndsp_trial_seats"):
            cols = _columns(cur, "ndsp_trial_seats")

            cohort_col = None
            for candidate in ("cohort", "user_type", "seat_type", "bucket", "trial_type"):
                if candidate in cols:
                    cohort_col = candidate
                    break

            if cohort_col:
                cur.execute(
                    f"""
                    SELECT COALESCE({cohort_col}::text, 'normal_beginner') AS cohort, COUNT(*)
                    FROM ndsp_trial_seats
                    GROUP BY 1
                    """
                )
                rows = cur.fetchall()
                for cohort, count in rows:
                    raw = str(cohort or "").strip().lower()
                    n = int(count or 0)

                    if raw in ("specialist", "academic", "specialist_academic", "professional", "analyst"):
                        used["specialist_academic"] += n
                    elif raw in ("premium", "special", "premium_invite_only", "vip", "private", "invite"):
                        used["premium_invite_only"] += n
                    else:
                        used["normal_beginner"] += n

        elif _table_exists(cur, "users"):
            cols = _columns(cur, "users")

            cohort_col = None
            for candidate in ("trial_cohort", "cohort", "user_type", "seat_type", "bucket", "trial_type", "plan"):
                if candidate in cols:
                    cohort_col = candidate
                    break

            where_sql = ""
            if "plan" in cols:
                where_sql = "WHERE LOWER(COALESCE(plan::text,'')) LIKE '%trial%' OR LOWER(COALESCE(plan::text,'')) LIKE '%elite%'"
            elif "subscription_plan" in cols:
                where_sql = "WHERE LOWER(COALESCE(subscription_plan::text,'')) LIKE '%trial%' OR LOWER(COALESCE(subscription_plan::text,'')) LIKE '%elite%'"
            elif "is_trial" in cols:
                where_sql = "WHERE is_trial = TRUE"

            if cohort_col:
                cur.execute(
                    f"""
                    SELECT COALESCE({cohort_col}::text, 'normal_beginner') AS cohort, COUNT(*)
                    FROM users
                    {where_sql}
                    GROUP BY 1
                    """
                )
                for cohort, count in cur.fetchall():
                    raw = str(cohort or "").strip().lower()
                    n = int(count or 0)

                    if raw in ("specialist", "academic", "specialist_academic", "professional", "analyst"):
                        used["specialist_academic"] += n
                    elif raw in ("premium", "special", "premium_invite_only", "vip", "private", "invite"):
                        used["premium_invite_only"] += n
                    else:
                        used["normal_beginner"] += n

        if _table_exists(cur, "ndsp_trial_invites"):
            premium_invites["table_exists"] = True
            cols = _columns(cur, "ndsp_trial_invites")

            if "used" in cols:
                cur.execute("SELECT COUNT(*) FROM ndsp_trial_invites WHERE COALESCE(used,false)=false")
                premium_invites["active"] = int(cur.fetchone()[0] or 0)

                cur.execute("SELECT COUNT(*) FROM ndsp_trial_invites WHERE COALESCE(used,false)=true")
                premium_invites["used"] = int(cur.fetchone()[0] or 0)
            else:
                cur.execute("SELECT COUNT(*) FROM ndsp_trial_invites")
                premium_invites["active"] = int(cur.fetchone()[0] or 0)

        remaining = {
            "specialist_academic": max(0, quotas["specialist_academic"] - used["specialist_academic"]),
            "normal_beginner": max(0, quotas["normal_beginner"] - used["normal_beginner"]),
            "premium_invite_only": max(0, quotas["premium_invite_only"] - used["premium_invite_only"]),
        }

        return {
            "ok": True,
            "source": "fastapi",
            "policy": "50 trial seats: 10 specialist/academic, 25 normal beginner, 15 premium invite-only",
            "quotas": quotas,
            "used": {**used, "total": sum(used.values())},
            "remaining": {**remaining, "total": sum(remaining.values())},
            "premium_invite_only": premium_invites,
            "database": {
                "connected": True,
                "name": os.environ.get("PGDATABASE", "ndsp_auth"),
                "user": os.environ.get("PGUSER", "ndsp_auth"),
                "password_exposed": False,
            },
        }

    except Exception as exc:
        return {
            "ok": False,
            "source": "fastapi",
            "error": str(exc),
            "password_exposed": False,
        }
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

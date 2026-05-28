from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)
from app.services.registration_notice_link import attach_registration_notice

import hashlib
import os
import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import psycopg
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


ORDINARY_LIMIT = int(os.getenv("NDSP_ORDINARY_TRIAL_LIMIT", "30"))
PROFESSIONAL_LIMIT = int(os.getenv("NDSP_PROFESSIONAL_TRIAL_LIMIT", "10"))
PRIVATE_INVITE_LIMIT = int(os.getenv("NDSP_PRIVATE_INVITE_LIMIT", "10"))
RESERVATION_MINUTES = int(os.getenv("NDSP_TRIAL_RESERVATION_MINUTES", "60"))
TOKEN_EXPIRY_HOURS = int(os.getenv("NDSP_TRIAL_TOKEN_EXPIRY_HOURS", "24"))
IP_HOURLY_LIMIT = int(os.getenv("NDSP_TRIAL_IP_HOURLY_LIMIT", "6"))
PRIVATE_INVITE_CODE = os.getenv("NDSP_PRIVATE_INVITE_CODE", "ELITE-PRIVATE-10")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    return url


def get_conn():
    return psycopg.connect(_database_url())


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def normalize_phone(phone: str) -> str:
    raw = (phone or "").strip()
    digits = re.sub(r"\D+", "", raw)

    if not digits:
        return ""

    # Saudi common normalization
    if digits.startswith("00"):
        digits = digits[2:]

    if digits.startswith("966"):
        return "+" + digits

    if digits.startswith("05") and len(digits) == 10:
        return "+966" + digits[1:]

    if digits.startswith("5") and len(digits) == 9:
        return "+966" + digits

    if raw.startswith("+"):
        return "+" + digits

    return "+" + digits


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def make_token() -> str:
    return secrets.token_urlsafe(32)


def client_ip(request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def user_agent(request) -> str:
    return request.headers.get("user-agent", "")[:500]


def init_schema() -> Dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_trial_registrations (
                    id UUID PRIMARY KEY,
                    category TEXT NOT NULL CHECK (category IN ('ordinary','professional','private_invite')),
                    email TEXT NOT NULL,
                    email_normalized TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    phone_e164 TEXT NOT NULL,
                    name TEXT NOT NULL DEFAULT '',
                    plan TEXT NOT NULL DEFAULT 'Elite',
                    status TEXT NOT NULL,
                    invite_code TEXT,
                    ip_address TEXT NOT NULL DEFAULT '',
                    user_agent TEXT NOT NULL DEFAULT '',
                    activation_token_hash TEXT UNIQUE,
                    token_expires_at TIMESTAMPTZ,
                    activated_at TIMESTAMPTZ,
                    reservation_expires_at TIMESTAMPTZ,
                    review_status TEXT,
                    review_note TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS ux_ndsp_trial_email_normalized
                ON ndsp_trial_registrations (email_normalized);
                """
            )

            cur.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS ux_ndsp_trial_phone_e164
                ON ndsp_trial_registrations (phone_e164);
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_trial_attempts (
                    id BIGSERIAL PRIMARY KEY,
                    category TEXT NOT NULL,
                    email_normalized TEXT,
                    phone_e164 TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    result TEXT NOT NULL,
                    reason TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS ix_ndsp_trial_attempts_ip_created
                ON ndsp_trial_attempts (ip_address, created_at);
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_trial_invite_codes (
                    code TEXT PRIMARY KEY,
                    category TEXT NOT NULL DEFAULT 'private_invite',
                    max_uses INT NOT NULL DEFAULT 1,
                    used_count INT NOT NULL DEFAULT 0,
                    active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            # One shared private invite code with 10 uses for now.
            cur.execute(
                """
                INSERT INTO ndsp_trial_invite_codes (code, category, max_uses, used_count, active)
                VALUES (%s, 'private_invite', %s, 0, TRUE)
                ON CONFLICT (code) DO UPDATE
                SET max_uses = EXCLUDED.max_uses,
                    active = TRUE;
                """,
                (PRIVATE_INVITE_CODE, PRIVATE_INVITE_LIMIT),
            )

        conn.commit()

    return {"ok": True, "schema": "ready"}


def log_attempt(
    conn,
    category: str,
    email_normalized: str,
    phone_e164: str,
    ip_address: str,
    ua: str,
    result: str,
    reason: str = "",
):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ndsp_trial_attempts
            (category, email_normalized, phone_e164, ip_address, user_agent, result, reason)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (category, email_normalized, phone_e164, ip_address, ua, result, reason),
        )


def _cleanup_expired(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE ndsp_trial_registrations
            SET status='EXPIRED',
                updated_at=now()
            WHERE status='ACTIVE'
              AND reservation_expires_at IS NOT NULL
              AND reservation_expires_at < now()
            """
        )


def _ip_rate_limited(conn, ip_address: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT count(*)
            FROM ndsp_trial_attempts
            WHERE ip_address=%s
              AND created_at > now() - interval '1 hour'
            """,
            (ip_address,),
        )
        count = cur.fetchone()[0] or 0
    return count >= IP_HOURLY_LIMIT


def _active_or_reserved_count(conn, category: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT count(*)
            FROM ndsp_trial_registrations
            WHERE category=%s
              AND status IN (
                'ACTIVE',
                'ACTIVE',
                'PENDING_REVIEW',
                'APPROVED_PENDING_ACTIVATION'
              )
            """,
            (category,),
        )
        return cur.fetchone()[0] or 0


def _limit_for(category: str) -> int:
    if category == "ordinary":
        return ORDINARY_LIMIT
    if category == "professional":
        return PROFESSIONAL_LIMIT
    if category == "private_invite":
        return PRIVATE_INVITE_LIMIT
    return 0


def _duplicate_exists(conn, email_normalized: str, phone_e164: str) -> Optional[str]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT email_normalized, phone_e164
            FROM ndsp_trial_registrations
            WHERE email_normalized=%s OR phone_e164=%s
            LIMIT 1
            """,
            (email_normalized, phone_e164),
        )
        row = cur.fetchone()

    if not row:
        return None

    if row[0] == email_normalized:
        return "DUPLICATE_EMAIL"
    if row[1] == phone_e164:
        return "DUPLICATE_PHONE"
    return "DUPLICATE"


def _validate_basic(email: str, phone: str) -> Optional[str]:
    if not email or "@" not in email:
        return "INVALID_EMAIL"
    if not phone or len(re.sub(r"\D+", "", phone)) < 8:
        return "INVALID_PHONE"
    return None


def create_trial_registration(
    *,
    category: str,
    email: str,
    phone: str,
    name: str,
    request,
    invite_code: Optional[str] = None,
) -> Dict[str, Any]:
    init_schema()

    email_n = normalize_email(email)
    phone_n = normalize_phone(phone)
    ip = client_ip(request)
    ua = user_agent(request)

    invalid = _validate_basic(email_n, phone_n)
    if invalid:
        with get_conn() as conn:
            log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", invalid)
            conn.commit()
        return {"ok": False, "code": invalid}

    if category not in ("ordinary", "professional", "private_invite"):
        return {"ok": False, "code": "INVALID_CATEGORY"}

    with get_conn() as conn:
        try:
            with conn.transaction():
                _cleanup_expired(conn)

                if _ip_rate_limited(conn, ip):
                    log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", "IP_RATE_LIMIT")
                    return {"ok": False, "code": "IP_RATE_LIMIT"}

                dup = _duplicate_exists(conn, email_n, phone_n)
                if dup:
                    log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", dup)
                    return {"ok": False, "code": dup}

                limit = _limit_for(category)
                used = _active_or_reserved_count(conn, category)

                if used >= limit:
                    log_attempt(conn, category, email_n, phone_n, ip, ua, "waitlisted", "SEAT_LIMIT_REACHED")
                    return {
                        "ok": False,
                        "code": "SEAT_LIMIT_REACHED",
                        "category": category,
                        "limit": limit,
                        "used": used,
                        "remaining": 0,
                    }

                if category == "private_invite":
                    code = (invite_code or "").strip()
                    if not code:
                        log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", "MISSING_INVITE_CODE")
                        return {"ok": False, "code": "MISSING_INVITE_CODE"}

                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            SELECT max_uses, used_count, active
                            FROM ndsp_trial_invite_codes
                            WHERE code=%s
                            FOR UPDATE
                            """,
                            (code,),
                        )
                        row = cur.fetchone()

                    if not row or not row[2]:
                        log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", "INVALID_INVITE_CODE")
                        return {"ok": False, "code": "INVALID_INVITE_CODE"}

                    if row[1] >= row[0]:
                        log_attempt(conn, category, email_n, phone_n, ip, ua, "blocked", "INVITE_LIMIT_REACHED")
                        return {"ok": False, "code": "INVITE_LIMIT_REACHED"}

                    with conn.cursor() as cur:
                        cur.execute(
                            """
                            UPDATE ndsp_trial_invite_codes
                            SET used_count = used_count + 1
                            WHERE code=%s
                            """,
                            (code,),
                        )

                token = make_token()
                thash = token_hash(token)

                if category == "professional":
                    status = "PENDING_REVIEW"
                    token_expires_at = None
                    reservation_expires_at = None
                    review_status = "PENDING"
                else:
                    status = "ACTIVE"
                    token_expires_at = _now() + timedelta(hours=TOKEN_EXPIRY_HOURS)
                    reservation_expires_at = _now() + timedelta(minutes=RESERVATION_MINUTES)
                    review_status = None

                rid = uuid.uuid4()

                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO ndsp_trial_registrations (
                            id, category, email, email_normalized, phone, phone_e164,
                            name, plan, status, invite_code, ip_address, user_agent,
                            activation_token_hash, token_expires_at, reservation_expires_at,
                            review_status
                        )
                        VALUES (
                            %s,%s,%s,%s,%s,%s,
                            %s,'Elite',%s,%s,%s,%s,
                            %s,%s,%s,%s
                        )
                        """,
                        (
                            rid, category, email, email_n, phone, phone_n,
                            name or "", status, invite_code, ip, ua,
                            thash if category != "professional" else None,
                            token_expires_at,
                            reservation_expires_at,
                            review_status,
                        ),
                    )

                log_attempt(conn, category, email_n, phone_n, ip, ua, "accepted", status)

                response = {
                    "ok": True,
                    "code": status,
                    "registration_id": str(rid),
                    "category": category,
                    "plan": "Elite",
                    "trial_days": 16,
                    "status": status,
                    "message": "Registration accepted.",
                }

                # For now return activation link for testing. In production email only.
                if category != "professional":
                    response["activation_token"] = token
                    response["activation_url"] = f"https://app.ndsp.app/activate?token={token}"

                return attach_registration_notice(response)
        except psycopg.errors.UniqueViolation:
            conn.rollback()
            with get_conn() as c2:
                log_attempt(c2, category, email_n, phone_n, ip, ua, "blocked", "UNIQUE_DUPLICATE")
                c2.commit()
            return {"ok": False, "code": "DUPLICATE_BLOCKED"}
        except Exception as e:
            conn.rollback()
            with get_conn() as c2:
                log_attempt(c2, category, email_n, phone_n, ip, ua, "error", str(e)[:200])
                c2.commit()
            return {"ok": False, "code": "REGISTRATION_ERROR", "message": "Registration failed safely."}


def activate_token(token: str) -> Dict[str, Any]:
    init_schema()

    if not token:
        return {"ok": False, "code": "MISSING_TOKEN"}

    th = token_hash(token)

    with get_conn() as conn:
        with conn.transaction():
            _cleanup_expired(conn)

            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, status, token_expires_at
                    FROM ndsp_trial_registrations
                    WHERE activation_token_hash=%s
                    FOR UPDATE
                    """,
                    (th,),
                )
                row = cur.fetchone()

            if not row:
                return {"ok": False, "code": "INVALID_TOKEN"}

            rid, status, exp = row

            if status == "ACTIVE":
                return {"ok": True, "code": "ALREADY_ACTIVE"}

            if status not in ("ACTIVE", "APPROVED_PENDING_ACTIVATION"):
                return {"ok": False, "code": f"INVALID_STATUS_{status}"}

            if exp and exp < _now():
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE ndsp_trial_registrations
                        SET status='EXPIRED', updated_at=now()
                        WHERE id=%s
                        """,
                        (rid,),
                    )
                return {"ok": False, "code": "TOKEN_EXPIRED"}

            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE ndsp_trial_registrations
                    SET status='ACTIVE',
                        activated_at=now(),
                        updated_at=now()
                    WHERE id=%s
                    """,
                    (rid,),
                )

            return {"ok": True, "code": "ACTIVATED", "registration_id": str(rid)}


def get_trial_status() -> Dict[str, Any]:
    init_schema()

    with get_conn() as conn:
        _cleanup_expired(conn)
        conn.commit()

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT category, status, count(*)
                FROM ndsp_trial_registrations
                GROUP BY category, status
                """
            )
            rows = cur.fetchall()

        counts: Dict[str, Dict[str, int]] = {
            "ordinary": {},
            "professional": {},
            "private_invite": {},
        }

        for category, status, count in rows:
            counts.setdefault(category, {})[status] = int(count)

        def used(category: str) -> int:
            c = counts.get(category, {})
            return sum(c.get(s, 0) for s in [
                "ACTIVE",
                "ACTIVE",
                "PENDING_REVIEW",
                "APPROVED_PENDING_ACTIVATION",
            ])

        ordinary_used = used("ordinary")
        professional_used = used("professional")
        invite_used = used("private_invite")

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT code, max_uses, used_count, active
                FROM ndsp_trial_invite_codes
                ORDER BY created_at DESC
                """
            )
            invites = [
                {
                    "code": r[0],
                    "max_uses": r[1],
                    "used_count": r[2],
                    "remaining": max(r[1] - r[2], 0),
                    "active": r[3],
                }
                for r in cur.fetchall()
            ]

    return {
        "enabled": True,
        "plan": "Elite",
        "trial_days": 16,
        "ordinary_limit": ORDINARY_LIMIT,
        "ordinary_used": ordinary_used,
        "ordinary_remaining": max(ORDINARY_LIMIT - ordinary_used, 0),
        "professional_limit": PROFESSIONAL_LIMIT,
        "professional_used": professional_used,
        "professional_remaining": max(PROFESSIONAL_LIMIT - professional_used, 0),
        "private_invite_limit": PRIVATE_INVITE_LIMIT,
        "private_invite_used": invite_used,
        "private_invite_remaining": max(PRIVATE_INVITE_LIMIT - invite_used, 0),
        "total_capacity": ORDINARY_LIMIT + PROFESSIONAL_LIMIT + PRIVATE_INVITE_LIMIT,
        "total_used": ordinary_used + professional_used + invite_used,
        "total_remaining": max(
            ORDINARY_LIMIT + PROFESSIONAL_LIMIT + PRIVATE_INVITE_LIMIT
            - ordinary_used - professional_used - invite_used,
            0
        ),
        "counts": counts,
        "invite_codes": invites,
        "public_message_ar": "الإطلاق الحالي مخصص لمجموعة محدودة من المستخدمين والمحللين وبكامل ميزات Elite.",
        "public_message_en": "The current launch is limited to selected users and analysts with full Elite features.",
    }


def reset_trial_counters() -> Dict[str, Any]:
    init_schema()
    with get_conn() as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE ndsp_trial_attempts RESTART IDENTITY CASCADE")
                cur.execute("TRUNCATE TABLE ndsp_trial_registrations RESTART IDENTITY CASCADE")
                cur.execute(
                    """
                    UPDATE ndsp_trial_invite_codes
                    SET used_count=0, active=TRUE
                    WHERE code=%s
                    """,
                    (PRIVATE_INVITE_CODE,),
                )
    return {"ok": True, "code": "RESET_DONE", "status": get_trial_status()}

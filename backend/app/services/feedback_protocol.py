from __future__ import annotations
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is missing")
    return url


def get_conn():
    return psycopg.connect(_database_url(), row_factory=dict_row)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


ORDINARY_REGISTRATION_NOTICE_AR = (
    "شكرًا لتسجيلك في تجربة NDSP Elite.\n\n"
    "نرحب بك في تجربة المنظومة. خلال فترة التجربة يمكنك استخدام NDSP واكتشاف السيناريوهات والمخرجات بهدوء.\n\n"
    "في اليوم الأخير من التجربة، سنطلب منك مشاركة رأيك وملاحظاتك حول سهولة استخدام المنظومة ووضوح قراءة السيناريوهات، "
    "وذلك لمساعدتنا على تطوير التجربة وجعلها أوضح وأسهل لجميع المستخدمين، خصوصًا المستخدمين الجدد والمبتدئين."
)

PROFESSIONAL_REGISTRATION_NOTICE_AR = (
    "شكرًا لانضمامك إلى تجربة NDSP Elite المخصصة للمحترفين والمتخصصين.\n\n"
    "نرحب برأيك المهني بعد اكتمال استخدامك للتجربة. في اليوم الأخير من فترة التجربة، سنطلب منك مشاركة تقييمك وملاحظاتك "
    "حول جودة السيناريوهات، وضوح المخرجات، قابلية الاعتماد، وسهولة قراءة النتائج.\n\n"
    "ملاحظاتك ستكون مهمة في تطوير NDSP قبل التوسع في الإطلاق والاستخدام الاحترافي والمؤسسي."
)

ORDINARY_FINAL_DAY_AR = (
    "اليوم هو اليوم الأخير من تجربة NDSP Elite.\n\n"
    "نرجو منك مشاركة رأيك حول تجربتك. هل كانت السيناريوهات واضحة؟ هل فهمت المخرجات بسهولة؟ "
    "هل توجد نقاط تحتاج إلى شرح أبسط أو تحسين في الواجهة؟\n\n"
    "ملاحظاتك مهمة جدًا لتطوير المنظومة وضمان سهولة استخدامها لجميع المستخدمين، خصوصًا المبتدئين."
)

PROFESSIONAL_FINAL_DAY_AR = (
    "اليوم هو اليوم الأخير من تجربة NDSP Elite.\n\n"
    "نرجو منك تقديم تقييمك المهني لتجربة الاستخدام. يهمنا رأيك حول وضوح السيناريوهات، جودة المخرجات، "
    "قابلية الاعتماد، سرعة القراءة، ومدى مناسبة المنظومة للاستخدام الاحترافي أو المؤسسي.\n\n"
    "ملاحظاتك ستكون جزءًا مهمًا من تحسين NDSP قبل التوسع في الإطلاق."
)

ORDINARY_REGISTRATION_NOTICE_EN = (
    "Thank you for registering for the NDSP Elite trial.\n\n"
    "You are welcome to explore the platform and use its scenarios during the trial period.\n\n"
    "On the final day of the trial, we will ask you to share your feedback about ease of use and scenario readability. "
    "Your feedback helps us improve NDSP and make it clearer for all users, especially new and beginner users."
)

PROFESSIONAL_REGISTRATION_NOTICE_EN = (
    "Thank you for joining the NDSP Elite trial for professional and specialized users.\n\n"
    "On the final day of your trial, we will ask for your professional feedback on scenario quality, output clarity, "
    "reliability, and ease of reading the results.\n\n"
    "Your feedback will help improve NDSP before broader professional and institutional expansion."
)

ORDINARY_FINAL_DAY_EN = (
    "Today is the final day of your NDSP Elite trial.\n\n"
    "Please share your feedback about your experience. Were the scenarios clear? Were the outputs easy to understand? "
    "Is there anything that needs simpler explanation or interface improvement?\n\n"
    "Your feedback is important for improving the platform, especially for beginner users."
)

PROFESSIONAL_FINAL_DAY_EN = (
    "Today is the final day of your NDSP Elite trial.\n\n"
    "Please share your professional feedback about scenario clarity, output quality, reliability, speed of reading, "
    "and suitability for professional or institutional use.\n\n"
    "Your feedback will be an important part of improving NDSP before broader expansion."
)


def init_feedback_schema() -> Dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_feedback_entries (
                    id UUID PRIMARY KEY,
                    registration_id TEXT,
                    email TEXT,
                    category TEXT NOT NULL DEFAULT 'ordinary',
                    plan TEXT NOT NULL DEFAULT 'Elite',
                    rating INTEGER,
                    scenario_clarity INTEGER,
                    ease_of_use INTEGER,
                    output_quality INTEGER,
                    professional_reliability INTEGER,
                    message TEXT,
                    source TEXT NOT NULL DEFAULT 'final_trial_day',
                    status TEXT NOT NULL DEFAULT 'new',
                    metadata JSONB,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS ix_ndsp_feedback_email_created
                ON ndsp_feedback_entries (email, created_at DESC);
                """
            )

            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS ix_ndsp_feedback_category_status
                ON ndsp_feedback_entries (category, status, created_at DESC);
                """
            )

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ndsp_feedback_notice_log (
                    id UUID PRIMARY KEY,
                    registration_id TEXT,
                    email TEXT,
                    category TEXT NOT NULL DEFAULT 'ordinary',
                    notice_type TEXT NOT NULL,
                    shown_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    metadata JSONB
                );
                """
            )

        conn.commit()

    return {"ok": True, "schema": "feedback_protocol_ready"}


def _client_ip(request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _user_agent(request) -> str:
    return request.headers.get("user-agent", "")[:500]


def _normalize_category(category: str) -> str:
    c = str(category or "").strip().lower()
    if c in {"professional", "pro", "analyst", "specialist", "specialized"}:
        return "professional"
    if c in {"private", "private_invite", "invite"}:
        return "private_invite"
    return "ordinary"


def registration_notice(category: str = "ordinary") -> Dict[str, Any]:
    init_feedback_schema()
    c = _normalize_category(category)

    if c == "professional":
        ar = PROFESSIONAL_REGISTRATION_NOTICE_AR
        en = PROFESSIONAL_REGISTRATION_NOTICE_EN
        audience = "professional"
    else:
        ar = ORDINARY_REGISTRATION_NOTICE_AR
        en = ORDINARY_REGISTRATION_NOTICE_EN
        audience = c

    return {
        "ok": True,
        "notice_type": "registration_notice_only",
        "audience": audience,
        "ask_feedback_now": False,
        "show_feedback_form_now": False,
        "final_day_feedback_required": True,
        "message_ar": ar,
        "message_en": en,
    }


def final_day_notice(category: str = "ordinary") -> Dict[str, Any]:
    init_feedback_schema()
    c = _normalize_category(category)

    if c == "professional":
        ar = PROFESSIONAL_FINAL_DAY_AR
        en = PROFESSIONAL_FINAL_DAY_EN
        audience = "professional"
    else:
        ar = ORDINARY_FINAL_DAY_AR
        en = ORDINARY_FINAL_DAY_EN
        audience = c

    return {
        "ok": True,
        "notice_type": "final_day_feedback_request",
        "audience": audience,
        "ask_feedback_now": True,
        "show_feedback_form_now": True,
        "message_ar": ar,
        "message_en": en,
        "fields": [
            "rating",
            "scenario_clarity",
            "ease_of_use",
            "output_quality",
            "professional_reliability",
            "message",
        ],
    }


def log_notice(payload: Dict[str, Any]) -> Dict[str, Any]:
    init_feedback_schema()

    registration_id = str(payload.get("registration_id", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    category = _normalize_category(str(payload.get("category", "ordinary")))
    notice_type = str(payload.get("notice_type", "")).strip()

    if notice_type not in {"registration_notice_only", "final_day_feedback_request"}:
        return {"ok": False, "code": "INVALID_NOTICE_TYPE"}

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ndsp_feedback_notice_log (
                    id, registration_id, email, category, notice_type, metadata
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    uuid.uuid4(),
                    registration_id or None,
                    email or None,
                    category,
                    notice_type,
                    Jsonb(payload.get("metadata") or {}),
                ),
            )
        conn.commit()

    return {"ok": True, "notice_logged": True}


def submit_feedback(payload: Dict[str, Any], request) -> Dict[str, Any]:
    init_feedback_schema()

    registration_id = str(payload.get("registration_id", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    category = _normalize_category(str(payload.get("category", "ordinary")))
    plan = str(payload.get("plan", "Elite")).strip() or "Elite"
    message = str(payload.get("message", "")).strip()

    def int_or_none(key: str):
        value = payload.get(key)
        if value in [None, ""]:
            return None
        try:
            n = int(value)
            return max(1, min(n, 5))
        except Exception:
            return None

    rating = int_or_none("rating")
    scenario_clarity = int_or_none("scenario_clarity")
    ease_of_use = int_or_none("ease_of_use")
    output_quality = int_or_none("output_quality")
    professional_reliability = int_or_none("professional_reliability")

    if not email and not registration_id:
        return {"ok": False, "code": "EMAIL_OR_REGISTRATION_REQUIRED"}

    if not message and not any([rating, scenario_clarity, ease_of_use, output_quality, professional_reliability]):
        return {"ok": False, "code": "FEEDBACK_CONTENT_REQUIRED"}

    feedback_id = uuid.uuid4()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ndsp_feedback_entries (
                    id, registration_id, email, category, plan,
                    rating, scenario_clarity, ease_of_use, output_quality,
                    professional_reliability, message, source, status,
                    metadata, ip_address, user_agent
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    feedback_id,
                    registration_id or None,
                    email or None,
                    category,
                    plan,
                    rating,
                    scenario_clarity,
                    ease_of_use,
                    output_quality,
                    professional_reliability,
                    message or None,
                    str(payload.get("source", "final_trial_day")),
                    "new",
                    Jsonb(payload.get("metadata") or {}),
                    _client_ip(request),
                    _user_agent(request),
                ),
            )
        conn.commit()

    return {
        "ok": True,
        "feedback_id": str(feedback_id),
        "status": "new",
        "message": "Feedback submitted.",
    }


def list_feedback(
    status: str = "",
    category: str = "",
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    init_feedback_schema()

    limit = max(1, min(int(limit or 50), 200))
    offset = max(0, int(offset or 0))

    where = []
    params = []

    if status:
        where.append("status=%s")
        params.append(status)

    if category:
        where.append("category=%s")
        params.append(_normalize_category(category))

    where_sql = "WHERE " + " AND ".join(where) if where else ""

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT *
                FROM ndsp_feedback_entries
                {where_sql}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
                """,
                params + [limit, offset],
            )
            items = cur.fetchall()

            cur.execute(
                f"""
                SELECT COUNT(*) AS total
                FROM ndsp_feedback_entries
                {where_sql}
                """,
                params,
            )
            total = cur.fetchone()["total"]

    return {
        "ok": True,
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }


def feedback_summary() -> Dict[str, Any]:
    init_feedback_schema()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM ndsp_feedback_entries")
            total = cur.fetchone()["total"]

            cur.execute(
                """
                SELECT category, COUNT(*) AS count
                FROM ndsp_feedback_entries
                GROUP BY category
                ORDER BY count DESC
                """
            )
            by_category = cur.fetchall()

            cur.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM ndsp_feedback_entries
                GROUP BY status
                ORDER BY count DESC
                """
            )
            by_status = cur.fetchall()

            cur.execute(
                """
                SELECT ROUND(AVG(rating)::numeric, 2) AS avg_rating,
                       ROUND(AVG(scenario_clarity)::numeric, 2) AS avg_scenario_clarity,
                       ROUND(AVG(ease_of_use)::numeric, 2) AS avg_ease_of_use,
                       ROUND(AVG(output_quality)::numeric, 2) AS avg_output_quality,
                       ROUND(AVG(professional_reliability)::numeric, 2) AS avg_professional_reliability
                FROM ndsp_feedback_entries
                """
            )
            averages = cur.fetchone()

    return {
        "ok": True,
        "total": total,
        "by_category": by_category,
        "by_status": by_status,
        "averages": averages,
    }

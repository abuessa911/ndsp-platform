from app.api.ndsp_strict_email_phone_trial_guard import strict_email_phone_trial_guard
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
import psycopg2.extras
from psycopg2 import sql
from app.api.ndsp_duplicate_activation_guard import duplicate_activation_guard
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

router = APIRouter()

REQUIRES_ADMIN_ACTIVATION = {
    "specialist_academic",
    "premium_invite_only",
}

WATCHED_REGISTER_PATHS = {
    "/api/trial/register/professional": "specialist_academic",
    "/api/trial/register/private-invite": "premium_invite_only",
    "/api/trial/private-invite/consume": "premium_invite_only",
    "/api/v6/elite-trial/analyst": "specialist_academic",
    "/api/v6/elite-trial/professional": "specialist_academic",
}


def _get_env_any(*names: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return str(value).strip()
    return ""


def _db_params() -> Dict[str, str]:
    return {
        "host": _get_env_any("PGHOST", "DB_HOST", "POSTGRES_HOST") or "127.0.0.1",
        "port": _get_env_any("PGPORT", "DB_PORT", "POSTGRES_PORT") or "5432",
        "dbname": _get_env_any("PGDATABASE", "DB_NAME", "DB_DATABASE", "POSTGRES_DB", "POSTGRES_DATABASE") or "ndsp_auth",
        "user": _get_env_any("PGUSER", "DB_USER", "DB_USERNAME", "POSTGRES_USER") or "ndsp_auth",
        "password": _get_env_any("PGPASSWORD", "DB_PASSWORD", "POSTGRES_PASSWORD") or "",
    }


def _conn():
    return psycopg2.connect(**_db_params())


def _admin_key() -> str:
    return _get_env_any("NDSP_ADMIN_KEY", "ADMIN_KEY")


def _is_admin_request(request: Request) -> bool:
    expected = _admin_key()
    if not expected:
        return False

    supplied = (
        request.headers.get("x-admin-key")
        or request.headers.get("X-Admin-Key")
        or request.query_params.get("admin_key")
        or request.query_params.get("key")
        or ""
    )

    return bool(supplied and supplied == expected)


def _telegram_token() -> str:
    return _get_env_any(
        "TELEGRAM_BOT_TOKEN",
        "NDSP_TELEGRAM_BOT_TOKEN",
        "TELEGRAM_TOKEN",
        "TG_BOT_TOKEN",
        "BOT_TOKEN",
    )


def _telegram_chat_ids() -> List[str]:
    raw_values = [
        _get_env_any("TELEGRAM_CHAT_ID"),
        _get_env_any("TG_CHAT_ID"),
        _get_env_any("NDSP_TELEGRAM_CHAT_ID"),
        _get_env_any("TELEGRAM_ADMIN_CHAT_ID"),
    ]

    result: List[str] = []
    seen = set()

    for raw in raw_values:
        for part in str(raw or "").replace(";", ",").split(","):
            chat_id = part.strip()
            if chat_id and chat_id not in seen:
                seen.add(chat_id)
                result.append(chat_id)

    return result


def _send_telegram(text: str) -> Dict[str, Any]:
    token = _telegram_token()
    chat_ids = _telegram_chat_ids()

    if not token or not chat_ids:
        return {"ok": False, "error": "telegram_not_configured", "results": []}

    results = []

    for chat_id in chat_ids:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = urllib.parse.urlencode(
                {
                    "chat_id": chat_id,
                    "text": text,
                    "disable_web_page_preview": "true",
                }
            ).encode("utf-8")

            req = urllib.request.Request(url, data=payload, method="POST")
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                parsed = json.loads(body) if body else {}
                results.append(
                    {
                        "chat_id": str(chat_id),
                        "status_code": int(resp.status),
                        "ok": bool(parsed.get("ok")),
                        "message_id": (parsed.get("result") or {}).get("message_id"),
                    }
                )
        except Exception as exc:
            results.append({"chat_id": str(chat_id), "ok": False, "error": str(exc)})

    return {"ok": any(item.get("ok") for item in results), "results": results}


def _safe_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _safe_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_json(v) for v in obj]
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    return obj


def _extract_email(payload: Dict[str, Any]) -> str:
    for key in ("email", "user_email", "mail", "account_email"):
        value = payload.get(key)
        if value:
            return str(value).strip().lower()
    return ""


def _extract_name(payload: Dict[str, Any]) -> str:
    for key in ("name", "full_name", "fullName", "username"):
        value = payload.get(key)
        if value:
            return str(value).strip()
    return ""


def _extract_invite_code(payload: Dict[str, Any]) -> str:
    for key in ("invite_code", "inviteCode", "code", "premium_invite_code", "premiumInviteCode"):
        value = payload.get(key)
        if value:
            return str(value).strip()
    return ""


def _category_from_path_and_payload(path: str, payload: Dict[str, Any]) -> str:
    if path in WATCHED_REGISTER_PATHS:
        return WATCHED_REGISTER_PATHS[path]

    raw = str(
        payload.get("category")
        or payload.get("type")
        or payload.get("plan")
        or payload.get("trial_type")
        or ""
    ).strip().lower()

    if raw in {"specialist", "professional", "academic", "analyst", "specialist_academic"}:
        return "specialist_academic"

    if raw in {"premium", "private", "vip", "premium_invite_only", "private_invite"}:
        return "premium_invite_only"

    return ""


def _table_columns(table_name: str) -> Dict[str, Dict[str, Any]]:
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = %s
                """,
                [table_name],
            )
            rows = cur.fetchall() or []

    return {str(row["column_name"]): dict(row) for row in rows}


def _safe_update_user_column(email: str, column: str, value: Any) -> bool:
    if not email:
        return False

    try:
        with _conn() as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("UPDATE users SET {} = %s WHERE lower(email) = lower(%s)").format(
                        sql.Identifier(column)
                    ),
                    [value, email],
                )
                return cur.rowcount > 0
    except Exception:
        return False


def _apply_user_activation_state(email: str, state: str, days: int = 16) -> Dict[str, Any]:
    result = {
        "email": email,
        "state": state,
        "users_table_exists": False,
        "updated_columns": [],
        "skipped_columns": [],
    }

    if not email:
        result["error"] = "missing_email"
        return result

    try:
        with _conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT to_regclass('public.users') IS NOT NULL")
                users_exists = bool(cur.fetchone()[0])

        result["users_table_exists"] = users_exists

        if not users_exists:
            return result

        columns = _table_columns("users")

        if state == "pending":
            text_value = "pending_admin_review"
            bool_value = False
            subscription_value = "pending_review"
        elif state == "approved":
            text_value = "active"
            bool_value = True
            subscription_value = "trial_active"
        elif state == "rejected":
            text_value = "rejected"
            bool_value = False
            subscription_value = "rejected"
        else:
            text_value = state
            bool_value = False
            subscription_value = state

        text_columns = [
            "status",
            "account_status",
            "activation_status",
            "trial_status",
        ]

        subscription_columns = [
            "subscription_status",
            "plan_status",
        ]

        bool_columns = [
            "is_active",
            "active",
            "enabled",
        ]

        for column in bool_columns:
            if column in columns:
                if _safe_update_user_column(email, column, bool_value):
                    result["updated_columns"].append(column)
                else:
                    result["skipped_columns"].append(column)

        for column in text_columns:
            if column in columns:
                if _safe_update_user_column(email, column, text_value):
                    result["updated_columns"].append(column)
                else:
                    result["skipped_columns"].append(column)

        for column in subscription_columns:
            if column in columns:
                if _safe_update_user_column(email, column, subscription_value):
                    result["updated_columns"].append(column)
                else:
                    result["skipped_columns"].append(column)

        if state == "approved":
            expires_at = datetime.now(timezone.utc) + timedelta(days=days)
            for column in ("trial_ends_at", "trial_expires_at", "subscription_ends_at", "expires_at"):
                if column in columns:
                    if _safe_update_user_column(email, column, expires_at):
                        result["updated_columns"].append(column)
                    else:
                        result["skipped_columns"].append(column)

        if "updated_at" in columns:
            _safe_update_user_column(email, "updated_at", datetime.now(timezone.utc))

    except Exception as exc:
        result["error"] = str(exc)

    return result


def _insert_activation_request(category: str, email: str, name: str, path: str, invite_code: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO ndsp_trial_activation_requests
                  (category, email, name, source_path, invite_code, status, raw_payload, metadata)
                VALUES
                  (%s, %s, %s, %s, %s, 'pending_admin_review', %s::jsonb, %s::jsonb)
                RETURNING *
                """,
                [
                    category,
                    email or None,
                    name or None,
                    path,
                    invite_code or None,
                    json.dumps(payload, ensure_ascii=False),
                    json.dumps({"source": "middleware", "created_ts": int(time.time())}),
                ],
            )
            row = cur.fetchone()
            conn.commit()

    return dict(row or {})


def _find_request(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    request_id = payload.get("id") or payload.get("request_id")
    email = str(payload.get("email") or "").strip().lower()
    category = str(payload.get("category") or "").strip()

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if request_id:
                cur.execute(
                    "SELECT * FROM ndsp_trial_activation_requests WHERE id = %s LIMIT 1",
                    [request_id],
                )
            elif email and category:
                cur.execute(
                    """
                    SELECT *
                    FROM ndsp_trial_activation_requests
                    WHERE lower(email) = lower(%s)
                      AND category = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    [email, category],
                )
            elif email:
                cur.execute(
                    """
                    SELECT *
                    FROM ndsp_trial_activation_requests
                    WHERE lower(email) = lower(%s)
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    [email],
                )
            else:
                return None

            row = cur.fetchone()

    return dict(row) if row else None


class NDSPTrialAdminActivationMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path") or ""
        method = (scope.get("method") or "").upper()

        watch_candidate = path in WATCHED_REGISTER_PATHS or path == "/api/v6/auth/elite-trial"

        if method not in {"POST", "PUT", "PATCH"} or not watch_candidate:
            await self.app(scope, receive, send)
            return

        body = b""
        more_body = True

        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = bool(message.get("more_body", False))

        payload: Dict[str, Any] = {}
        try:
            payload = json.loads(body.decode("utf-8") or "{}")
            if not isinstance(payload, dict):
                payload = {}
        except Exception:
            payload = {}

        category = _category_from_path_and_payload(path, payload)

        if category not in REQUIRES_ADMIN_ACTIVATION:
            async def replay_receive_normal() -> Message:
                return {"type": "http.request", "body": body, "more_body": False}

            await self.app(scope, replay_receive_normal, send)
            return

        sent_messages: List[Message] = []
        status_holder = {"status": 500}

        async def replay_receive() -> Message:
            return {"type": "http.request", "body": body, "more_body": False}

        async def capture_send(message: Message):
            if message.get("type") == "http.response.start":
                status_holder["status"] = int(message.get("status") or 500)
            sent_messages.append(message)

        await self.app(scope, replay_receive, capture_send)

        status_code = int(status_holder.get("status") or 500)

        if 200 <= status_code < 300:
            email = _extract_email(payload)
            name = _extract_name(payload)
            invite_code = _extract_invite_code(payload)

            try:
                req_row = _insert_activation_request(
                    category=category,
                    email=email,
                    name=name,
                    path=path,
                    invite_code=invite_code,
                    payload=payload,
                )

                user_update = _apply_user_activation_state(email, "pending")

                _send_telegram(
                    "🟡 NDSP Admin Activation Required\n\n"
                    f"Category: {category}\n"
                    f"Email: {email or 'غير محدد'}\n"
                    f"Name: {name or 'غير محدد'}\n"
                    f"Path: {path}\n"
                    f"Request ID: {req_row.get('id')}\n\n"
                    "تم استقبال طلب تجربة يحتاج تفعيلًا من لوحة الأدمن.\n"
                    "الحساب يبقى في حالة pending_admin_review إلى أن يتم اعتماده.\n"
                    "ليس توصية مالية ولا إشارة تداول."
                )

                print(f"[NDSP] admin activation request created id={req_row.get('id')} category={category} email={email} user_update={user_update}")

            except Exception as exc:
                print(f"[NDSP] admin activation middleware failed: {exc}")

        for message in sent_messages:
            await send(message)


def _admin_required(request: Request) -> Optional[JSONResponse]:
    if not _is_admin_request(request):
        return JSONResponse(status_code=401, content={"ok": False, "error": "UNAUTHORIZED"})
    return None


def _activation_counts() -> Dict[str, Any]:
    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT
                  category,
                  status,
                  COUNT(*) AS count
                FROM ndsp_trial_activation_requests
                GROUP BY category, status
                ORDER BY category, status
                """
            )
            rows = cur.fetchall() or []

    result: Dict[str, Any] = {
        "specialist_academic": {},
        "premium_invite_only": {},
    }

    for row in rows:
        category = row.get("category")
        status = row.get("status")
        count = int(row.get("count") or 0)
        result.setdefault(category, {})[status] = count

    return result


@router.get("/api/admin/trial-activations/status")
def activation_status(request: Request) -> Dict[str, Any]:
    denied = _admin_required(request)
    if denied:
        return denied

    return {
        "ok": True,
        "policy": {
            "normal_beginner": "can_register_without_admin_activation_policy",
            "specialist_academic": "requires_admin_activation",
            "premium_invite_only": "requires_admin_activation_and_invite_code",
        },
        "code_location": "backend/app/api/ndsp_trial_activation_admin.py",
        "url_namespace": "/api",
        "counts": _activation_counts(),
        "telegram_configured": bool(_telegram_token() and _telegram_chat_ids()),
        "token_exposed": False,
        "password_exposed": False,
    }


@router.get("/api/admin/trial-activations/status")
def activation_status_admin_alias(request: Request) -> Dict[str, Any]:
    return activation_status(request)


@router.get("/api/admin/trial-activations/list")
def activation_list(request: Request, status: str = "", category: str = "", limit: int = 100) -> Dict[str, Any]:
    denied = _admin_required(request)
    if denied:
        return denied

    if limit < 1:
        limit = 1
    if limit > 200:
        limit = 200

    conditions = []
    params: List[Any] = []

    if status:
        conditions.append("status = %s")
        params.append(status)

    if category:
        conditions.append("category = %s")
        params.append(category)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT *
        FROM ndsp_trial_activation_requests
        {where}
        ORDER BY created_at DESC
        LIMIT %s
    """

    params.append(limit)

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall() or []

    return {
        "ok": True,
        "items": [_safe_json(dict(row)) for row in rows],
        "count": len(rows),
    }


@router.get("/api/admin/trial-activations/list")
def activation_list_admin_alias(request: Request, status: str = "", category: str = "", limit: int = 100) -> Dict[str, Any]:
    return activation_list(request, status=status, category=category, limit=limit)


@router.post("/api/admin/trial-activations/approve")
async def activation_approve(request: Request) -> Dict[str, Any]:
    denied = _admin_required(request)
    if denied:
        return denied

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    row = _find_request(payload)

    if not row:
        return {"ok": False, "error": "ACTIVATION_REQUEST_NOT_FOUND"}

    days = int(payload.get("days") or 16)
    note = str(payload.get("note") or "").strip()
    approved_by = str(payload.get("approved_by") or "admin").strip()

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE ndsp_trial_activation_requests
                SET
                  status = 'approved',
                  approved_at = NOW(),
                  approved_by = %s,
                  admin_note = COALESCE(NULLIF(%s, ''), admin_note),
                  updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                [approved_by, note, row["id"]],
            )
            updated = dict(cur.fetchone() or {})
            conn.commit()

    user_update = _apply_user_activation_state(str(updated.get("email") or ""), "approved", days=days)

    _send_telegram(
        "🟢 NDSP Trial Account Approved\n\n"
        f"Category: {updated.get('category')}\n"
        f"Email: {updated.get('email') or 'غير محدد'}\n"
        f"Request ID: {updated.get('id')}\n"
        f"Trial Days: {days}\n\n"
        "تم تفعيل الحساب من لوحة الأدمن."
    )

    return {
        "ok": True,
        "status": "approved",
        "request": _safe_json(updated),
        "user_update": user_update,
        "token_exposed": False,
    }


@router.post("/api/admin/trial-activations/approve")
async def activation_approve_admin_alias(request: Request) -> Dict[str, Any]:
    return await activation_approve(request)


@router.post("/api/admin/trial-activations/reject")
async def activation_reject(request: Request) -> Dict[str, Any]:
    denied = _admin_required(request)
    if denied:
        return denied

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    row = _find_request(payload)

    if not row:
        return {"ok": False, "error": "ACTIVATION_REQUEST_NOT_FOUND"}

    note = str(payload.get("note") or "").strip()
    rejected_by = str(payload.get("rejected_by") or "admin").strip()

    with _conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE ndsp_trial_activation_requests
                SET
                  status = 'rejected',
                  rejected_at = NOW(),
                  rejected_by = %s,
                  admin_note = COALESCE(NULLIF(%s, ''), admin_note),
                  updated_at = NOW()
                WHERE id = %s
                RETURNING *
                """,
                [rejected_by, note, row["id"]],
            )
            updated = dict(cur.fetchone() or {})
            conn.commit()

    user_update = _apply_user_activation_state(str(updated.get("email") or ""), "rejected")

    _send_telegram(
        "🔴 NDSP Trial Account Rejected\n\n"
        f"Category: {updated.get('category')}\n"
        f"Email: {updated.get('email') or 'غير محدد'}\n"
        f"Request ID: {updated.get('id')}\n\n"
        "تم رفض طلب التفعيل من لوحة الأدمن."
    )

    return {
        "ok": True,
        "status": "rejected",
        "request": _safe_json(updated),
        "user_update": user_update,
        "token_exposed": False,
    }


@router.post("/api/admin/trial-activations/reject")
async def activation_reject_admin_alias(request: Request) -> Dict[str, Any]:
    return await activation_reject(request)


@router.post("/api/admin/trial-activations/create-pending")
async def activation_create_pending(request: Request) -> Dict[str, Any]:
    denied = _admin_required(request)
    if denied:
        return denied

    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            payload = {}
    except Exception:
        payload = {}

    category = str(payload.get("category") or "").strip()

    if category not in REQUIRES_ADMIN_ACTIVATION:
        return {
            "ok": False,
            "error": "CATEGORY_MUST_REQUIRE_ADMIN_ACTIVATION",
            "allowed": sorted(REQUIRES_ADMIN_ACTIVATION),
        }

    email = _extract_email(payload)
    name = _extract_name(payload)
    invite_code = _extract_invite_code(payload)
    path = str(payload.get("source_path") or "/api/admin/trial-activations/create-pending")

    row = _insert_activation_request(
        category=category,
        email=email,
        name=name,
        path=path,
        invite_code=invite_code,
        payload=payload,
    )

    user_update = _apply_user_activation_state(email, "pending")

    _send_telegram(
        "🟡 NDSP Manual Pending Activation Created\n\n"
        f"Category: {category}\n"
        f"Email: {email or 'غير محدد'}\n"
        f"Request ID: {row.get('id')}\n\n"
        "تم إنشاء طلب تفعيل يدوي من لوحة الأدمن."
    )

    return {
        "ok": True,
        "status": "pending_admin_review",
        "request": _safe_json(row),
        "user_update": user_update,
        "token_exposed": False,
    }


@router.post("/api/admin/trial-activations/create-pending")
async def activation_create_pending_admin_alias(request: Request) -> Dict[str, Any]:
    return await activation_create_pending(request)


@router.get("/api/trial/activation-policy")
def public_activation_policy() -> Dict[str, Any]:
    return {
        "ok": True,
        "policy": {
            "normal_beginner": {
                "requires_admin_activation": False,
            },
            "specialist_academic": {
                "requires_admin_activation": True,
                "admin_review_required": True,
            },
            "premium_invite_only": {
                "requires_admin_activation": True,
                "requires_invite_code": True,
                "admin_review_required": True,
            },
        },
        "url_namespace": "/api",
        "code_location": "backend/app/api",
    }

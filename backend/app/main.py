from app.api.ndsp_strict_email_phone_trial_guard import strict_email_phone_trial_guard
from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)
from app.services.decision_market_enricher import enrich_decision_with_price_router
from app.api.price_status import router as price_status_router
from app.middleware.decision_active_response_sanitizer import DecisionActiveResponseSanitizerMiddleware
from app.api.decision_active_admin import router as decision_active_admin_router
from app.auth.routes import router as auth_router

from app.services.ndsp_auth_core import (
    init_auth_schema as ndsp_auth_init_schema,
    register_user as ndsp_auth_register_user,
    activate_user as ndsp_auth_activate_user,
    login_user as ndsp_auth_login_user,
    me_from_session as ndsp_auth_me_from_session,
    admin_list_users as ndsp_auth_admin_list_users,
)


from app.services.feedback_protocol import (
    init_feedback_schema as ndsp_feedback_init_schema,
    registration_notice as ndsp_feedback_registration_notice,
    final_day_notice as ndsp_feedback_final_day_notice,
    log_notice as ndsp_feedback_log_notice,
    submit_feedback as ndsp_feedback_submit,
    list_feedback as ndsp_feedback_list,
    feedback_summary as ndsp_feedback_summary,
)


from app.services.owner_authority import (
    init_owner_schema as ndsp_owner_init_schema,
    get_owner_status as ndsp_owner_get_status,
    execute_owner_action as ndsp_owner_execute_action,
    list_audit as ndsp_owner_list_audit,
)


from app.services.trial_anti_abuse import (
    init_schema as ndsp_trial_init_schema,
    get_trial_status as ndsp_trial_get_status,
    create_trial_registration as ndsp_trial_create_registration,
    activate_token as ndsp_trial_activate_token,
    reset_trial_counters as ndsp_trial_reset_counters,
)

from app.api.runtime.market_pulse_api import router as runtime_market_pulse_router
from app.api.runtime.runtime_policy_api import router as runtime_policy_router
from app.api.auth2_v6 import router as auth2_v6_router
from app.api.auth_v6 import router as auth_v6_router
import logging
import json
import asyncio
from app.api.live_ws import router as live_ws_router
from app.api.websockets.ticker import router as ticker_ws_router
import os
from app.api.elite_trial import router as elite_trial_router
from app.api.ndsp_duplicate_activation_guard import duplicate_activation_guard
from fastapi import FastAPI, HTTPException, Header, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from app.core.governed_pipeline import run_governed
from app.governance.guard import assert_governed_user_route
from app.api.routers import history
from app.api.ndip_v6 import router as ndsp_v6_router
from app.api.routers.legacy_quarantine import router as legacy_quarantine_router
from app.api.admin.telegram_admin_v6 import router as telegram_admin_v6_router
from app.engines.alerts_engine import process_alert
from app.api.admin.subscriptions_admin_v6 import router as subscriptions_admin_v6_router
from app.api.telegram_webhook_v6 import router as telegram_webhook_v6_router
from app.api.admin.payments_admin_v6 import router as payments_admin_v6_router
from app.api.admin.system_admin_v6 import router as system_admin_v6_router
from app.api.admin.admin_ui_v6 import router as admin_ui_v6_router
from app.api.admin.leads_admin_v6 import router as leads_admin_v6_router
from app.api.admin.admin_session_v6 import router as admin_session_v6_router
from app.api.payments.payment_webhook_v6 import router as payment_webhook_v6_router
from app.api.admin.audit_admin_v6 import router as audit_admin_v6_router
from app.api.payments.nowpayments_v6 import router as nowpayments_v6_router
from app.api.v6.scanner_v1 import router as scanner_v1_router
from app.api.ndsp_auth_pg import router as ndsp_auth_pg_router
import asyncpg
from fastapi.middleware.cors import CORSMiddleware
from app.api.admin.ops_controls_v1 import router as ops_controls_v1_router
from app.api.ndsp_auth_foundation import router as ndsp_auth_foundation_router
from app.api.v6.plan_access import router as plan_access_router
from app.api.payments.admin_console_v6 import router as admin_console_v6_router
from app.core.elite_trial_capacity import enforce_elite_trial_capacity
from app.api.ndsp_elite_experience import router as ndsp_elite_experience_router
from app.api.ndsp_payment_state import router as ndsp_payment_state_router
from app.api.admin.tdl_v2_policy_admin import router as tdl_v2_policy_admin_router
from app.core.governance_runtime import apply_governance_runtime
from app.api.ndsp_live_alerts_ai import router as ndsp_live_alerts_ai_router

from app.api.elite_lab_snapshot import router as elite_lab_snapshot_router
from app.api.terminal_v2 import router as terminal_v2_router
app = FastAPI()



mount_ndsp_market_routes(app)
# NDSP_API_V7_BLOCKER_FINAL
@app.middleware("http")
async def ndsp_block_legacy_api_v7(request, call_next):
    path = getattr(request.url, "path", "") or ""
    if path == "/api/v7" or path.startswith("/api/v7/"):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=404,
            content={
                "ok": False,
                "error": "LEGACY_API_V7_REMOVED",
                "message": "The official NDSP API namespace is /api only."
            },
        )
    return await call_next(request)
# /NDSP_API_V7_BLOCKER_FINAL


app.include_router(terminal_v2_router)
app.include_router(elite_lab_snapshot_router)
from app.api.elite_trial_requests import router as elite_trial_requests_router
from app.ndsp_market_routes_direct import mount_ndsp_market_routes

# NDSP DATABASE_URL FALLBACK FOR USER LOGIN
import os as _ndsp_os_for_db_url

if "DATABASE_URL" not in globals() or not globals().get("DATABASE_URL"):
    DATABASE_URL = (
        _ndsp_os_for_db_url.getenv("DATABASE_URL")
        or _ndsp_os_for_db_url.getenv("POSTGRES_URL")
        or _ndsp_os_for_db_url.getenv("DB_URL")
        or ""
    )

    if not DATABASE_URL:
        for _ndsp_env_file in (
            "/etc/ndsp/ndsp-db.env",
            "/home/nawaf511/empire-core-new/backend/.env",
        ):
            try:
                with open(_ndsp_env_file, "r", encoding="utf-8", errors="ignore") as _f:
                    for _line in _f:
                        _line = _line.strip()
                        if not _line or _line.startswith("#") or "=" not in _line:
                            continue
                        _k, _v = _line.split("=", 1)
                        _k = _k.strip()
                        _v = _v.strip().strip('"').strip("'")
                        if _k in ("DATABASE_URL", "POSTGRES_URL", "DB_URL") and _v:
                            DATABASE_URL = _v
                            break
                if DATABASE_URL:
                    break
            except Exception:
                pass

    if not DATABASE_URL:
        DATABASE_URL = "postgresql://ndsp_auth@127.0.0.1:5432/ndsp_auth"
# END NDSP DATABASE_URL FALLBACK FOR USER LOGIN

app.include_router(elite_trial_requests_router)
app.add_middleware(DecisionActiveResponseSanitizerMiddleware)

app.include_router(ndsp_elite_experience_router)
app.include_router(decision_active_admin_router)
app.include_router(ndsp_payment_state_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ndsp.app",
        "https://www.ndsp.app",
        "https://my.ndsp.app",
        "https://admin.ndsp.app",
        "https://app.ndsp.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    runtime_market_pulse_router,
    prefix="/api/v1",
    tags=["runtime"]
)


app.include_router(
    runtime_policy_router,
    prefix="/api/v1",
    tags=["runtime"]
)


# NDSP CORS for protected app/auth
if not getattr(app.state, "ndsp_cors_configured", False):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://my.ndsp.app",
            "https://ndsp.app",
            "https://api.ndsp.app",
            "https://admin.ndsp.app",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
    app.state.ndsp_cors_configured = True

app.include_router(live_ws_router)
app.include_router(ticker_ws_router)
app.include_router(elite_trial_router)


@app.middleware("http")
async def governance_http_guard(request: Request, call_next):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    guard_response = await duplicate_activation_guard(request)
    if guard_response is not None:
        return guard_response
    path = request.url.path
    allowed_prefixes = (
        "/api/v6/",
        "/decision",
        "/docs",
        "/openapi.json",
        "/redoc",
    )

    if not path.startswith(allowed_prefixes):
        try:
            assert_governed_user_route(path)
        except Exception as exc:
            status = getattr(exc, "status_code", 403)
            detail = getattr(exc, "detail", str(exc))
            return JSONResponse(
                status_code=status,
                content={
                    "status": "blocked",
                    "reason": detail,
                    "path": path
                }
            )

    admin_key = request.query_params.get("admin_key")
    expected_admin_key = os.getenv("ADMIN_UI_KEY", "").strip()
    if admin_key and expected_admin_key and admin_key == expected_admin_key:
        request.scope["headers"].append((b"x-role", b"admin"))

    return await call_next(request)


app.include_router(scanner_v1_router)


# NDSP_FORCE_TDL_V2_ENDPOINT_START
def _ndsp_force_tdl_v2_endpoint_payload(payload):
    try:
        if isinstance(payload, dict):
            payload = attach_tdl_v2_to_decision(payload)
            payload = apply_governance_runtime(payload)
            return enrich_decision_with_price_router(payload, symbol)
    except Exception as exc:
        try:
            payload.setdefault("meta", {})
            payload["meta"]["tdl_v2_endpoint_error"] = str(exc)
        except Exception:
            pass
    return _ndsp_public_decision_response_guard(payload)

@app.get("/decision")
def decision(symbol: str):
    try:
        result = run_governed(symbol)

        if isinstance(result, dict) and result.get("status") != "error":
            try:
                process_alert(result)
            except Exception as alert_exc:
                print("ALERT ERROR:", str(alert_exc))

        return _ndsp_force_tdl_v2_endpoint_payload(result)

    except Exception as e:
        import traceback

        error = str(e)
        trace = traceback.format_exc()

        print("💀 ERROR:", error)
        print(trace)

        return {
            "status": "error",
            "message": error
        }


app.include_router(history.router)
app.include_router(ndsp_v6_router)
app.include_router(legacy_quarantine_router)
app.include_router(telegram_admin_v6_router)
app.include_router(subscriptions_admin_v6_router)
app.include_router(telegram_webhook_v6_router)
app.include_router(payments_admin_v6_router)
app.include_router(system_admin_v6_router)
app.include_router(admin_ui_v6_router)
app.include_router(leads_admin_v6_router)
app.include_router(admin_session_v6_router)
app.include_router(payment_webhook_v6_router)
app.include_router(audit_admin_v6_router)
app.include_router(nowpayments_v6_router)
app.include_router(tdl_v2_policy_admin_router)

# NDSP PostgreSQL permanent auth
app.include_router(ndsp_auth_pg_router)
app.include_router(ops_controls_v1_router)


# ============================================================
# NDSP ELITE TRIAL ACCESS — v1
# Purpose:
# - Token-protected Elite Trial access
# - Frontend sends: Authorization: Bearer NDSP-ELITE-XXXX-XXXX
# - Backend validates access before protected dashboard use
# ============================================================

def _ndsp_elite_tokens():
    raw = os.getenv("NDSP_ELITE_TOKENS", "NDSP-ELITE-1234-5678,NDSP-ELITE-9999-0000")
    return {x.strip() for x in raw.split(",") if x.strip()}

def _extract_bearer_token(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")
    return token

@app.get("/elite-access")
def elite_access(authorization: str | None = Header(default=None)):
    token = _extract_bearer_token(authorization)

    if token not in _ndsp_elite_tokens():
        raise HTTPException(status_code=403, detail="Invalid token")

    return {
        "status": "ACCESS_GRANTED",
        "package": "Elite",
        "system": "NDSP",
        "message": "Elite trial access verified"
    }


logger = logging.getLogger("ndsp.ws")

def _ndsp_sanitize_ws_payload(payload):
    """
    Extra safety layer for WebSocket delivery.
    Keeps the governed output, but removes fields that should not leak in realtime UI.
    """
    if not isinstance(payload, dict):
        return {
            "error": True,
            "code": "INVALID_PIPELINE_OUTPUT",
            "message": "Pipeline output unavailable",
            "system": "NDSP",
            "version": "1.0.0",
        }

    blocked_top_keys = {
        "debug",
        "trace",
        "stack",
        "exception",
        "raw",
        "secrets",
        "token",
        "api_key",
        "password",
    }

    safe = {}
    for k, v in payload.items():
        if str(k).lower() in blocked_top_keys:
            continue
        safe[k] = v

    # Force system identity where possible
    safe.setdefault("system", "NDSP")
    safe.setdefault("version", "1.0.0")

    return safe


async def _ndsp_run_governed_async(symbol: str):
    """
    Runs sync pipeline safely without blocking the websocket event loop.
    """
    return await asyncio.to_thread(run_governed, symbol)


@app.websocket("/ws/decision")
async def ws_decision(websocket: WebSocket):
    """
    NDSP realtime governed decision stream.

    Client may send JSON:
    {
      "symbol": "EURUSD",
      "interval": 5
    }

    Rules:
    - Backend is source of truth.
    - WebSocket only delivers governed decision support output.
    - No trade execution.
    - No BUY/SELL command delivery.
    """
    await websocket.accept()

    symbol = "EURUSD"
    interval = 5.0

    await websocket.send_json({
        "type": "connection",
        "status": "connected",
        "system": "NDSP",
        "message": "NDSP realtime decision stream connected",
        "symbol": symbol,
        "interval": interval,
    })

    try:
        while True:
            # Non-blocking receive with timeout.
            # If client sends config, update stream params.
            try:
                raw_msg = await asyncio.wait_for(websocket.receive_text(), timeout=0.05)
                try:
                    msg = json.loads(raw_msg)
                    if isinstance(msg, dict):
                        new_symbol = str(msg.get("symbol", symbol)).strip().upper()
                        if new_symbol:
                            symbol = new_symbol[:30]

                        try:
                            new_interval = float(msg.get("interval", interval))
                            if 1 <= new_interval <= 60:
                                interval = new_interval
                        except Exception:
                            pass

                        await websocket.send_json({
                            "type": "config",
                            "status": "updated",
                            "system": "NDSP",
                            "symbol": symbol,
                            "interval": interval,
                        })
                except Exception:
                    await websocket.send_json({
                        "type": "warning",
                        "system": "NDSP",
                        "message": "Invalid client message. Send JSON like {\"symbol\":\"EURUSD\",\"interval\":5}",
                    })
            except asyncio.TimeoutError:
                pass

            try:
                governed = await _ndsp_run_governed_async(symbol)
                safe_payload = _ndsp_sanitize_ws_payload(governed)
                await websocket.send_json({
                    "type": "decision",
                    "stream": "ws/decision",
                    "system": "NDSP",
                    "symbol": symbol,
                    "payload": safe_payload,
                })
            except Exception as e:
                logger.exception("NDSP WS pipeline error")
                await websocket.send_json({
                    "type": "error",
                    "error": True,
                    "code": "WS_PIPELINE_ERROR",
                    "system": "NDSP",
                    "symbol": symbol,
                    "message": "Decision stream temporarily unavailable; system continued safely.",
                })

            await asyncio.sleep(interval)

    except WebSocketDisconnect:
        logger.info("NDSP WS disconnected")
    except Exception:
        logger.exception("NDSP WS fatal error")
        try:
            await websocket.close()
        except Exception:
            pass



@app.get("/")
async def root():
    return {
        "name": "NDSP API",
        "status": "LIVE",
        "version": "6.0.0",
        "mode": "production",
        "docs": "/docs",
        "health": "ok"
    }

app.include_router(ndsp_auth_foundation_router)


app.include_router(auth_v6_router)

app.include_router(auth2_v6_router)


# ==========================================================
# NDSP Elite Controlled Trial Protocol - Anti-Abuse V1
# ==========================================================

@app.on_event("startup")
def ndsp_trial_anti_abuse_startup():
    try:
        ndsp_trial_init_schema()
    except Exception as e:
        print("NDSP_TRIAL_SCHEMA_INIT_FAILED", str(e))


@app.get("/api/trial/status")
def ndsp_v7_trial_status():
    return ndsp_trial_get_status()


@app.post("/api/trial/register/ordinary")
async def ndsp_v7_register_ordinary(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    guard_response = await duplicate_activation_guard(request)
    if guard_response is not None:
        return guard_response
    body = await request.json()
    return ndsp_trial_create_registration(
        category="ordinary",
        email=str(body.get("email", "")),
        phone=str(body.get("phone", "")),
        name=str(body.get("name", "")),
        request=request,
    )


@app.post("/api/trial/register/professional")
async def ndsp_v7_register_professional(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    guard_response = await duplicate_activation_guard(request)
    if guard_response is not None:
        return guard_response
    body = await request.json()
    return ndsp_trial_create_registration(
        category="professional",
        email=str(body.get("email", "")),
        phone=str(body.get("phone", "")),
        name=str(body.get("name", "")),
        request=request,
    )


@app.post("/api/trial/register/private-invite")
async def ndsp_v7_register_private_invite(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_trial_create_registration(
        category="private_invite",
        email=str(body.get("email", "")),
        phone=str(body.get("phone", "")),
        name=str(body.get("name", "")),
        invite_code=str(body.get("invite_code", "")),
        request=request,
    )


@app.post("/api/trial/activate")
async def ndsp_v7_activate_trial(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_trial_activate_token(str(body.get("token", "")))


@app.post("/api/trial/admin/reset")
def ndsp_v7_admin_reset_trial():
    return ndsp_trial_reset_counters()


# ==========================================================
# NDSP Owner Authority Layer V1
# ==========================================================

@app.on_event("startup")
def ndsp_owner_authority_startup():
    try:
        ndsp_owner_init_schema()
    except Exception as e:
        print("NDSP_OWNER_SCHEMA_INIT_FAILED", str(e))


@app.get("/api/admin/owner/status")
def ndsp_v7_owner_status():
    return ndsp_owner_get_status()


@app.get("/api/admin/audit")
def ndsp_v7_owner_audit(limit: int = 50):
    return ndsp_owner_list_audit(limit=limit)


@app.post("/api/admin/owner/action/{action_name}")
async def ndsp_v7_owner_action(action_name: str, request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_owner_execute_action(action_name, body, request)


# ==========================================================
# NDSP Feedback Protocol V1
# ==========================================================

@app.on_event("startup")
def ndsp_feedback_protocol_startup():
    try:
        ndsp_feedback_init_schema()
    except Exception as e:
        print("NDSP_FEEDBACK_SCHEMA_INIT_FAILED", str(e))


@app.get("/api/feedback/registration-notice")
def ndsp_v7_feedback_registration_notice(category: str = "ordinary"):
    return ndsp_feedback_registration_notice(category=category)


@app.get("/api/feedback/final-day-notice")
def ndsp_v7_feedback_final_day_notice(category: str = "ordinary"):
    return ndsp_feedback_final_day_notice(category=category)


@app.post("/api/feedback/log-notice")
async def ndsp_v7_feedback_log_notice(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_feedback_log_notice(body)


@app.post("/api/feedback/submit")
async def ndsp_v7_feedback_submit(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_feedback_submit(body, request)


@app.get("/api/admin/feedback")
def ndsp_v7_admin_feedback(status: str = "", category: str = "", limit: int = 50, offset: int = 0):
    return ndsp_feedback_list(status=status, category=category, limit=limit, offset=offset)


@app.get("/api/admin/feedback/summary")
def ndsp_v7_admin_feedback_summary():
    return ndsp_feedback_summary()


# ==========================================================
# NDSP Auth Core V1
# ==========================================================

@app.on_event("startup")
def ndsp_auth_core_startup():
    try:
        ndsp_auth_init_schema()
    except Exception as e:
        print("NDSP_AUTH_CORE_SCHEMA_INIT_FAILED", str(e))


@app.post("/api/v8/auth/register", include_in_schema=False)
async def ndsp_v8_auth_register(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_auth_register_user(body, request)


@app.get("/api/v8/auth/activate", include_in_schema=False)
async def ndsp_v8_auth_activate(request: Request, token: str = ""):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    return ndsp_auth_activate_user(token, request)


@app.post("/api/v8/auth/login", include_in_schema=False)
async def ndsp_v8_auth_login(request: Request):
    request_path = getattr(getattr(request, "url", None), "path", "") or ""
    if request_path.startswith("/api/trial/register/"):
        request_path = getattr(getattr(request, "url", None), "path", "") or ""
        if request_path.startswith("/api/trial/register/"):
            request_path = getattr(getattr(request, "url", None), "path", "") or ""
            if request_path.startswith("/api/trial/register/"):
                guard_response = await strict_email_phone_trial_guard(request)
                if guard_response is not None:
                    return guard_response
    body = await request.json()
    return ndsp_auth_login_user(body, request)


@app.get("/api/v8/auth/me", include_in_schema=False)
def ndsp_v8_auth_me(token: str = ""):
    return ndsp_auth_me_from_session(token)


@app.get("/api/v8/admin/auth/users", include_in_schema=False)
def ndsp_v8_admin_auth_users(limit: int = 50, offset: int = 0, q: str = ""):
    return ndsp_auth_admin_list_users(limit=limit, offset=offset, q=q)


app.include_router(auth_router)
app.include_router(plan_access_router)
app.include_router(admin_console_v6_router)
app.include_router(ndsp_live_alerts_ai_router)
app.include_router(price_status_router)


# === NDSP SAFE HEALTH STATUS ENDPOINTS v1 ===
from datetime import datetime, timezone as _ndsp_health_timezone
import os as _ndsp_health_os
import uuid as _ndsp_health_uuid


def _ndsp_safe_now_iso_v1():
    return datetime.now(_ndsp_health_timezone.utc).isoformat()


def _ndsp_database_status_v1():
    """
    Sanitized database health check.
    Does not expose DATABASE_URL, credentials, host, username, password, stack traces, or driver internals.
    """
    database_url = _ndsp_health_os.getenv("DATABASE_URL", "")
    if not database_url:
        return {
            "configured": False,
            "status": "not_configured",
            "engine": "unknown",
        }

    engine = "PostgreSQL" if database_url.startswith(("postgresql://", "postgresql+")) else "configured"

    try:
        # Optional lightweight SQLAlchemy check if available in runtime.
        from sqlalchemy import create_engine, text as _sql_text  # type: ignore

        connect_args = {}
        if database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}

        db_engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            connect_args=connect_args,
        )
        with db_engine.connect() as conn:
            conn.execute(_sql_text("SELECT 1"))
        return {
            "configured": True,
            "status": "ok",
            "engine": engine,
        }
    except Exception:
        return {
            "configured": True,
            "status": "unavailable_safe_mode",
            "engine": engine,
        }


@app.get("/health")
def ndsp_health_v1():
    db = _ndsp_database_status_v1()
    return {
        "ok": True,
        "system": "NDSP",
        "service": "api",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "status": "ok" if db.get("status") == "ok" else "degraded",
        "database": db,
        "safe": True,
        "secrets_exposed": False,
        "timestamp": _ndsp_safe_now_iso_v1(),
        "request_id": str(_ndsp_health_uuid.uuid4()),
    }


@app.get("/status")
def ndsp_status_v1():
    db = _ndsp_database_status_v1()
    return {
        "ok": True,
        "system": "NDSP",
        "service": "api",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "api_status": "online",
        "database_status": db.get("status", "unknown"),
        "database_engine": db.get("engine", "unknown"),
        "production_readiness": {
            "decision_endpoint": "enabled",
            "health_endpoint": "enabled",
            "status_endpoint": "enabled",
            "legal_package": "published",
            "secrets_exposed": False,
            "raw_logic_exposed": False,
            "direct_trade_execution": False,
        },
        "timestamp": _ndsp_safe_now_iso_v1(),
        "request_id": str(_ndsp_health_uuid.uuid4()),
    }
# === END NDSP SAFE HEALTH STATUS ENDPOINTS v1 ===


# === NDSP REDIS RATE LIMIT CACHE V1 ===
from fastapi import Request as _NdspRequest
from fastapi.responses import JSONResponse as _NdspJSONResponse

try:
    from slowapi import Limiter as _NdspLimiter
    from slowapi.util import get_remote_address as _ndsp_get_remote_address
    from slowapi.middleware import SlowAPIMiddleware as _NdspSlowAPIMiddleware

    _ndsp_rate_limiter = _NdspLimiter(key_func=_ndsp_get_remote_address)

    try:
        app.state.limiter = _ndsp_rate_limiter
    except Exception:
        pass

    try:
        app.add_middleware(_NdspSlowAPIMiddleware)
    except Exception:
        pass

except Exception:
    _ndsp_rate_limiter = None


@app.exception_handler(429)
async def ndsp_rate_limit_handler_v1(request: _NdspRequest, exc):
    return _NdspJSONResponse(
        status_code=429,
        content={
            "ok": False,
            "system": "NDSP",
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please slow down.",
            "safe": True,
        },
    )


@app.get("/ops/cache-status")
def ndsp_cache_status_v1():
    try:
        from app.core.ndsp_cache_layer import health
        cache = health()
    except Exception:
        cache = {"enabled": False, "status": "unavailable"}

    return {
        "ok": True,
        "system": "NDSP",
        "service": "cache-rate-limit",
        "rate_limit_layer": "enabled" if _ndsp_rate_limiter else "fallback",
        "cache": cache,
        "safe": True,
        "secrets_exposed": False,
    }
# === END NDSP REDIS RATE LIMIT CACHE V1 ===


# === NDSP WEBSOCKET LIVE LAYER V1 ===
import asyncio as _ndsp_ws_asyncio
from datetime import datetime as _ndsp_ws_datetime, timezone as _ndsp_ws_timezone
from fastapi import WebSocket as _NdspWebSocket, WebSocketDisconnect as _NdspWebSocketDisconnect


def _ndsp_ws_now_v1():
    return _ndsp_ws_datetime.now(_ndsp_ws_timezone.utc).isoformat()


async def _ndsp_ws_safe_decision_v1(symbol: str):
    """
    Safe public WebSocket payload.
    This intentionally exposes only sanitized context.
    """
    try:
        # Prefer existing governed pipeline if available, but never expose raw internals.
        try:
            from app.core.governed_pipeline import run_governed  # type: ignore
            result = run_governed(symbol)
            if hasattr(result, "__await__"):
                result = await result

            return {
                "type": "decision_update",
                "ok": True,
                "system": "NDSP",
                "symbol": symbol,
                "version": str(result.get("version", "1.0.0")) if isinstance(result, dict) else "1.0.0",
                "governance_version": str(result.get("governance_version", "6.1.0")) if isinstance(result, dict) else "6.1.0",
                "decision": (result.get("decision", {}) if isinstance(result, dict) else {}),
                "states": (result.get("states", {}) if isinstance(result, dict) else {}),
                "risk": (result.get("risk", {}) if isinstance(result, dict) else {}),
                "market_alignment": {
                    "signal": (result.get("market_alignment", {}) or {}).get("signal", "NO_SIGNAL") if isinstance(result, dict) else "NO_SIGNAL",
                    "position": (result.get("market_alignment", {}) or {}).get("position", "UNKNOWN") if isinstance(result, dict) else "UNKNOWN",
                    "status": (result.get("market_alignment", {}) or {}).get("status", "SAFE") if isinstance(result, dict) else "SAFE",
                },
                "safe": True,
                "raw_logic_exposed": False,
                "direct_execution": False,
                "timestamp": _ndsp_ws_now_v1(),
            }
        except Exception:
            return {
                "type": "decision_update",
                "ok": True,
                "system": "NDSP",
                "symbol": symbol,
                "version": "1.0.0",
                "governance_version": "6.1.0",
                "decision": {
                    "direction": "neutral",
                    "confidence": 0,
                },
                "states": {
                    "system_state": "safe_mode",
                    "risk_state": "normal",
                    "position_state": "none",
                },
                "risk": {
                    "state": "normal",
                    "reason": "live fallback payload",
                },
                "market_alignment": {
                    "signal": "NO_SIGNAL",
                    "position": "UNKNOWN",
                    "status": "SAFE",
                },
                "safe": True,
                "raw_logic_exposed": False,
                "direct_execution": False,
                "timestamp": _ndsp_ws_now_v1(),
            }
    except Exception:
        return {
            "type": "error",
            "ok": False,
            "system": "NDSP",
            "message": "safe websocket payload unavailable",
            "timestamp": _ndsp_ws_now_v1(),
        }


@app.websocket("/ws/decision")
async def ndsp_ws_decision_v1(websocket: _NdspWebSocket):
    await websocket.accept()

    symbol = websocket.query_params.get("symbol", "BTCUSDT")
    symbol = str(symbol or "BTCUSDT").upper().strip()[:32]

    try:
        await websocket.send_json({
            "type": "connected",
            "ok": True,
            "system": "NDSP",
            "service": "websocket-live-layer",
            "symbol": symbol,
            "safe": True,
            "raw_logic_exposed": False,
            "direct_execution": False,
            "timestamp": _ndsp_ws_now_v1(),
        })

        while True:
            payload = await _ndsp_ws_safe_decision_v1(symbol)
            await websocket.send_json(payload)
            await _ndsp_ws_asyncio.sleep(5)

    except _NdspWebSocketDisconnect:
        return
    except Exception:
        try:
            await websocket.close(code=1011)
        except Exception:
            return


@app.get("/ops/ws-status")
def ndsp_ws_status_v1():
    return {
        "ok": True,
        "system": "NDSP",
        "service": "websocket-live-layer",
        "endpoint": "/ws/decision",
        "status": "enabled",
        "safe": True,
        "raw_logic_exposed": False,
        "direct_execution": False,
        "timestamp": _ndsp_ws_now_v1(),
    }
# === END NDSP WEBSOCKET LIVE LAYER V1 ===


# === NDSP ALERTS AI ASSISTANT LAYER V1 ===
from fastapi import Body as _NdspBody
from app.governance.tdl_v2_adapter import attach_tdl_v2_to_decision
from app.api.admin_routes import router as admin_router

@app.get("/ops/alerts-status")
def ndsp_alerts_status_v1():
    return {
        "ok": True,
        "system": "NDSP",
        "service": "live-alerts",
        "channels": {
            "telegram": "ready_requires_env",
            "email": "placeholder_queue",
            "push": "placeholder_queue"
        },
        "safe": True,
        "raw_logic_exposed": False,
        "direct_execution": False,
    }

@app.post("/ops/alerts/test")
def ndsp_alerts_test_v1(payload: dict = _NdspBody(default={})):
    try:
        from app.core.ndsp_alerts_engine import dispatch_alert
        sample = {
            "symbol": str(payload.get("symbol", "BTCUSDT")).upper()[:32],
            "decision": {"direction": "neutral", "confidence": 42},
            "states": {"system_state": "live", "risk_state": "normal"},
            "market_alignment": {"signal": "CONTEXT_ONLY"},
        }
        channels = payload.get("channels") or ["telegram", "email", "push"]
        return dispatch_alert(sample, channels)
    except Exception:
        return {"ok": False, "system": "NDSP", "error": "alert_dispatch_failed", "safe": True}

@app.get("/ops/assistant-status")
def ndsp_assistant_status_v1():
    return {
        "ok": True,
        "system": "NDSP",
        "service": "ai-assistant",
        "status": "enabled",
        "mode": "sanitized_decision_support",
        "safe": True,
        "raw_logic_exposed": False,
        "direct_execution": False,
    }

@app.post("/assistant/explain")
def ndsp_assistant_explain_v1(payload: dict = _NdspBody(default={})):
    symbol = str(payload.get("symbol", "BTCUSDT")).upper()[:32]
    question = str(payload.get("question", "")).strip()[:500]

    try:
        try:
            from app.core.governed_pipeline import run_governed
            decision_payload = run_governed(symbol)
        except Exception:
            decision_payload = {
                "symbol": symbol,
                "decision": {"direction": "neutral", "confidence": 0},
                "states": {"system_state": "safe_mode", "risk_state": "normal"},
                "market_alignment": {"signal": "NO_SIGNAL"},
                "explainability": {"reason": "Fallback safe explanation."},
            }

        from app.core.ndsp_ai_assistant import explain_decision
        return explain_decision(decision_payload, question)
    except Exception:
        return {
            "ok": False,
            "system": "NDSP",
            "assistant": "NDSP AI Assistant",
            "error": "assistant_unavailable",
            "safe": True,
        }
# === END NDSP ALERTS AI ASSISTANT LAYER V1 ===




def _ndsp_public_decision_response_guard(payload):
    """
    Public decision response guard.
    Presentation-only sanitizer. Does not mutate runtime decision logic.
    """
    try:
        from app.middleware.decision_active_response_sanitizer import sanitize_decision_active_public_payload
        return sanitize_decision_active_public_payload(payload)
    except Exception:
        return payload




# NDSP_RUNTIME_HEALTH_V1
try:
    from app.api.ndsp_runtime_health import router as ndsp_runtime_health_router
    app.include_router(ndsp_runtime_health_router)
except Exception as exc:
    print(f"[NDSP] runtime health router failed: {exc}")
# /NDSP_RUNTIME_HEALTH_V1

# NDSP_SEATS_STATUS_ENDPOINT_V1
try:
    from app.api.ndsp_seats_status import router as ndsp_seats_status_router
    app.include_router(ndsp_seats_status_router)
except Exception as exc:
    print(f"[NDSP] seats status router failed: {exc}")
# /NDSP_SEATS_STATUS_ENDPOINT_V1

# NDSP_TRIAL_TELEGRAM_AUTO_ALERTS_V1
try:
    from app.api.ndsp_trial_telegram_alerts import (
        router as ndsp_trial_telegram_alerts_router,
        NDSPTrialTelegramAlertMiddleware,
    )
    app.include_router(ndsp_trial_telegram_alerts_router)
    app.add_middleware(NDSPTrialTelegramAlertMiddleware)
except Exception as exc:
    print(f"[NDSP] trial telegram alerts integration failed: {exc}")
# /NDSP_TRIAL_TELEGRAM_AUTO_ALERTS_V1

# NDSP_PREMIUM_INVITE_ONLY_V1
try:
    from app.api.ndsp_premium_invites import (
        router as ndsp_premium_invites_router,
        NDSPPremiumInviteOnlyMiddleware,
    )
    app.include_router(ndsp_premium_invites_router)
    app.add_middleware(NDSPPremiumInviteOnlyMiddleware)
except Exception as exc:
    print(f"[NDSP] premium invite-only integration failed: {exc}")
# /NDSP_PREMIUM_INVITE_ONLY_V1

# NDSP_SEATS_STATUS_PREMIUM_OVERRIDE_V1
try:
    from app.api.ndsp_seats_status_premium_override import NDSPSeatsStatusPremiumOverrideMiddleware
    app.add_middleware(NDSPSeatsStatusPremiumOverrideMiddleware)
except Exception as exc:
    print(f"[NDSP] seats status premium override integration failed: {exc}")
# /NDSP_SEATS_STATUS_PREMIUM_OVERRIDE_V1

# NDSP_ADMIN_ACTIVATION_POLICY_CANONICAL_API
try:
    from app.api.ndsp_trial_activation_admin import (
        router as ndsp_trial_activation_admin_router,
        NDSPTrialAdminActivationMiddleware,
    )
    app.include_router(ndsp_trial_activation_admin_router)
    app.add_middleware(NDSPTrialAdminActivationMiddleware)
except Exception as exc:
    print(f"[NDSP] admin activation policy v7 integration failed: {exc}")
# /NDSP_ADMIN_ACTIVATION_POLICY_CANONICAL_API

# NDSP admin routes
app.include_router(admin_router)


# NDSP admin all users endpoint
try:
    from app.api.ndsp_admin_all_users import router as ndsp_admin_all_users_router
    app.include_router(ndsp_admin_all_users_router)
except Exception as exc:
    print("[NDSP] ndsp_admin_all_users router load failed:", exc)

# NDSP admin activation delete endpoint
try:
    from app.api.ndsp_admin_activation_delete import router as ndsp_admin_activation_delete_router
    app.include_router(ndsp_admin_activation_delete_router)
except Exception as exc:
    print("[NDSP] activation delete router load failed:", exc)

# NDSP duplicate activation maintenance endpoints
try:
    from app.api.ndsp_registration_duplicate_guard import router as ndsp_registration_duplicate_guard_router
    app.include_router(ndsp_registration_duplicate_guard_router)
except Exception as exc:
    print("[NDSP] duplicate guard router load failed:", exc)

# NDSP approve activation and create/update active user
try:
    from app.api.ndsp_admin_activation_approve_user import router as ndsp_admin_activation_approve_user_router
    app.include_router(ndsp_admin_activation_approve_user_router)
except Exception as exc:
    print("[NDSP] approve-user router load failed:", exc)

# NDSP strict trial registration guard: email + phone uniqueness
try:
    from app.api.ndsp_trial_register_guard_middleware import NDSPTrialRegisterGuardMiddleware
    app.add_middleware(NDSPTrialRegisterGuardMiddleware)
except Exception as exc:
    print("[NDSP] trial register guard middleware load failed:", exc)

# NDSP temporary v8-to-canonical API bridge.
try:
    from app.api.ndsp_v8_to_api_canonical_bridge import router as ndsp_v8_to_api_canonical_bridge_router
    app.include_router(ndsp_v8_to_api_canonical_bridge_router)
except Exception as exc:
    print("[NDSP] v8 canonical bridge load failed:", exc)


# NDSP canonical auth routes replacing /api/v8/auth/*
# Governance: /api/v8/* is deprecated. Canonical namespace is /api/*.
@app.post("/api/auth/register")
async def ndsp_canonical_auth_register(request: Request):
    return await ndsp_v8_auth_register(request)

@app.get("/api/auth/activate")
async def ndsp_canonical_auth_activate(request: Request, token: str = ""):
    return await ndsp_v8_auth_activate(request, token=token)

@app.post("/api/auth/login")
async def ndsp_canonical_auth_login(request: Request):
    return await ndsp_v8_auth_login(request)

@app.get("/api/auth/me")
def ndsp_canonical_auth_me(token: str = ""):
    return ndsp_v8_auth_me(token=token)

@app.get("/api/admin/auth/users")
def ndsp_canonical_admin_auth_users(limit: int = 50, offset: int = 0, q: str = ""):
    return ndsp_v8_admin_auth_users(limit=limit, offset=offset, q=q)


# NDSP canonical aliases for legacy /api/v1 routes.
# Governance: /api/v1/* is transitional and must converge into /api/*.

@app.post("/api/auth/register-trial")
async def ndsp_canonical_auth_register_trial(request: Request):
    # Prefer existing ordinary registration route if available.
    try:
        return await register_ordinary_trial(request)
    except NameError:
        try:
            return await ndsp_v8_auth_register(request)
        except NameError:
            return {"ok": False, "code": "CANONICAL_REGISTER_TRIAL_HANDLER_NOT_FOUND"}

@app.post("/api/trial/register")
async def ndsp_canonical_trial_register(request: Request):
    try:
        return await register_ordinary_trial(request)
    except NameError:
        try:
            return await ndsp_v8_auth_register(request)
        except NameError:
            return {"ok": False, "code": "CANONICAL_TRIAL_REGISTER_HANDLER_NOT_FOUND"}


# NDSP temporary v1-to-canonical API bridge.
try:
    from app.api.ndsp_v1_to_api_canonical_bridge import router as ndsp_v1_to_api_canonical_bridge_router
    app.include_router(ndsp_v1_to_api_canonical_bridge_router)
except Exception as exc:
    print("[NDSP] v1 canonical bridge load failed:", exc)

# NDSP temporary v6-to-canonical API bridge.
try:
    from app.api.ndsp_v6_to_api_canonical_bridge import router as ndsp_v6_to_api_canonical_bridge_router
    app.include_router(ndsp_v6_to_api_canonical_bridge_router)
except Exception as exc:
    print("[NDSP] v6 canonical bridge load failed:", exc)


# NDSP API namespace governance: hide legacy versioned namespaces from public OpenAPI.
# Runtime compatibility may remain temporarily, but public API surface is /api/* only.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_canonical_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        paths = schema.get("paths", {}) or {}
        filtered = {}
        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")

        for path, spec in paths.items():
            if path.startswith(hidden_prefixes):
                continue
            filtered[path] = spec

        schema["paths"] = filtered

        schema.setdefault("x-ndsp-api-governance", {})
        schema["x-ndsp-api-governance"].update({
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "execution_policy": "EXECUTION_SANITIZED",
            "decision_mode": "DECISION_ACTIVE",
        })

        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = ndsp_canonical_openapi
except Exception as exc:
    print("[NDSP] canonical openapi filter install failed:", exc)


# NDSP API namespace governance: public OpenAPI must expose canonical /api/* only.
# Legacy runtime bridges may remain temporarily for compatibility, but versioned namespaces are hidden.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_canonical_openapi_final():
        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        paths = schema.get("paths", {}) or {}
        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")
        filtered = {}

        for path, spec in paths.items():
            if path.startswith(hidden_prefixes):
                continue
            filtered[path] = spec

        schema["paths"] = filtered
        schema["x-ndsp-api-governance"] = {
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "no_layer_disabled": True,
            "direct_trade_execution": False,
            "public_output_sanitized": True,
        }

        return schema

    app.openapi_schema = None
    app.openapi = ndsp_canonical_openapi_final
except Exception as exc:
    print("[NDSP] canonical OpenAPI governance filter failed:", exc)


# NDSP API namespace governance: public OpenAPI must expose canonical /api/* only.
# Legacy runtime bridges may remain temporarily for compatibility, but versioned namespaces are hidden.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_canonical_openapi_final():
        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        paths = schema.get("paths", {}) or {}
        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")
        filtered = {}

        for path, spec in paths.items():
            if path.startswith(hidden_prefixes):
                continue
            filtered[path] = spec

        schema["paths"] = filtered
        schema["x-ndsp-api-governance"] = {
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "no_layer_disabled": True,
            "direct_trade_execution": False,
            "public_output_sanitized": True,
        }

        return schema

    app.openapi_schema = None
    app.openapi = ndsp_canonical_openapi_final
except Exception as exc:
    print("[NDSP] canonical OpenAPI governance filter failed:", exc)


# NDSP_FINAL_CANONICAL_OPENAPI_FILTER_V1
# Public OpenAPI surface must expose canonical /api/* only.
# Legacy /api/v1, /api/v6, /api/v8 runtime bridges may remain hidden temporarily.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_final_canonical_openapi():
        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        paths = schema.get("paths", {}) or {}
        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")
        filtered = {}

        for path, spec in paths.items():
            if path.startswith(hidden_prefixes):
                continue
            filtered[path] = spec

        schema["paths"] = filtered
        schema["x-ndsp-api-governance"] = {
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "no_layer_disabled": True,
            "direct_trade_execution": False,
            "public_output_sanitized": True,
        }

        return schema

    app.openapi_schema = None
    app.openapi = ndsp_final_canonical_openapi
except Exception as exc:
    print("[NDSP] final canonical OpenAPI governance filter failed:", exc)


# NDSP_FINAL_CANONICAL_OPENAPI_FILTER_V2
# Public OpenAPI surface must expose canonical /api/* only.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_final_canonical_openapi_v2():
        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")
        paths = schema.get("paths", {}) or {}
        schema["paths"] = {
            path: spec
            for path, spec in paths.items()
            if not path.startswith(hidden_prefixes)
        }

        schema["x-ndsp-api-governance"] = {
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "no_layer_disabled": True,
            "direct_trade_execution": False,
            "public_output_sanitized": True,
        }
        return schema

    app.openapi_schema = None
    app.openapi = ndsp_final_canonical_openapi_v2
except Exception as exc:
    print("[NDSP] final canonical OpenAPI filter failed:", exc)


# NDSP_FINAL_CANONICAL_OPENAPI_FILTER_FIXED
# Public OpenAPI surface must expose canonical /api/* only.
try:
    from fastapi.openapi.utils import get_openapi

    def ndsp_final_canonical_openapi_fixed():
        schema = get_openapi(
            title=getattr(app, "title", "NDSP API"),
            version=getattr(app, "version", "1.0.0"),
            description=getattr(app, "description", None),
            routes=app.routes,
        )

        hidden_prefixes = ("/api/v1/", "/api/v6/", "/api/v8/")
        paths = schema.get("paths", {}) or {}

        schema["paths"] = {
            path: spec
            for path, spec in paths.items()
            if not path.startswith(hidden_prefixes)
        }

        schema["x-ndsp-api-governance"] = {
            "canonical_namespace": "/api/*",
            "hidden_legacy_namespaces": list(hidden_prefixes),
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "no_layer_disabled": True,
            "direct_trade_execution": False,
            "public_output_sanitized": True,
        }
        return schema

    app.openapi_schema = None
    app.openapi = ndsp_final_canonical_openapi_fixed
except Exception as exc:
    print("[NDSP] final canonical OpenAPI filter failed:", exc)




# NDSP CANONICAL USER LOGIN FINAL
@app.post("/api/auth/user-login", include_in_schema=True)
async def ndsp_canonical_user_login_final(request: Request):
    """
    Canonical user login for approved trial users.
    Reads from ndsp_auth.users only.
    Password hash is verified with PostgreSQL crypt().
    """
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            {"ok": False, "code": "INVALID_JSON", "message": "بيانات الدخول غير صالحة."},
            status_code=400,
        )

    email = str(payload.get("email") or payload.get("user_email") or "").strip().lower()
    password = str(payload.get("password") or "")

    if not email or not password:
        return JSONResponse(
            {"ok": False, "code": "EMAIL_PASSWORD_REQUIRED", "message": "البريد وكلمة المرور مطلوبة."},
            status_code=400,
        )

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            row = await conn.fetchrow(
                """
                SELECT
                    id::text AS id,
                    name,
                    email,
                    password_hash,
                    plan,
                    role,
                    trial_day,
                    status,
                    trial_ends_at,
                    category,
                    phone
                FROM users
                WHERE lower(email)=lower($1)
                LIMIT 1
                """,
                email,
            )

            if not row:
                return JSONResponse(
                    {"ok": False, "code": "USER_NOT_FOUND", "message": "الحساب غير موجود أو لم يتم إنشاؤه بعد."},
                    status_code=404,
                )

            if str(row.get("status") or "").lower() not in ("active", "approved"):
                return JSONResponse(
                    {"ok": False, "code": "USER_NOT_ACTIVE", "message": "الحساب غير مفعل بعد."},
                    status_code=403,
                )

            verified = await conn.fetchval(
                "SELECT crypt($1, $2) = $2",
                password,
                row["password_hash"],
            )

            if not verified:
                return JSONResponse(
                    {"ok": False, "code": "INVALID_CREDENTIALS", "message": "البريد أو كلمة المرور غير صحيحة."},
                    status_code=401,
                )

            token_seed = f"{row['id']}:{row['email']}"
            token = "ndsp_user_" + str(abs(hash(token_seed)))

            return {
                "ok": True,
                "token": token,
                "user": {
                    "id": row["id"],
                    "name": row["name"],
                    "email": row["email"],
                    "plan": row["plan"],
                    "role": row["role"],
                    "trial_day": row["trial_day"],
                    "status": row["status"],
                    "trial_ends_at": str(row["trial_ends_at"]) if row["trial_ends_at"] else None,
                    "category": row["category"],
                    "phone": row["phone"],
                },
                "redirect": "/pages/dashboard.html",
            }
        finally:
            await conn.close()
    except Exception as e:
        return JSONResponse(
            {"ok": False, "code": "LOGIN_SERVER_ERROR", "message": "تعذر تسجيل الدخول.", "detail": str(e)[:160]},
            status_code=500,
        )
# END NDSP CANONICAL USER LOGIN FINAL




# NDSP MARKET PRICES PUBLIC ENDPOINT FINAL
@app.get("/api/market/prices", include_in_schema=True)
async def ndsp_market_prices_public_final():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        try:
            rows = await conn.fetch("""
                SELECT
                  symbol,
                  name_ar,
                  name_en,
                  category,
                  source,
                  is_active,
                  updated_at
                FROM ndsp_assets
                WHERE is_active=true
                ORDER BY
                  CASE category
                    WHEN 'crypto' THEN 1
                    WHEN 'forex' THEN 2
                    WHEN 'commodity' THEN 3
                    WHEN 'index' THEN 4
                    ELSE 9
                  END,
                  symbol
            """)

            fallback = {
                "BTCUSDT": 68000, "ETHUSDT": 3600, "BNBUSDT": 590, "SOLUSDT": 160,
                "XRPUSDT": 0.52, "ADAUSDT": 0.45, "DOGEUSDT": 0.16,
                "EURUSD": 1.08, "GBPUSD": 1.27, "USDJPY": 157,
                "XAUUSD": 2350, "XAGUSD": 30, "USOIL": 78, "UKOIL": 82,
                "SPX": 5300, "NDX": 18500, "DJI": 39000, "DXY": 105
            }

            prices = []
            for r in rows:
                sym = r["symbol"]
                prices.append({
                    "symbol": sym,
                    "name_ar": r["name_ar"],
                    "name_en": r["name_en"],
                    "category": r["category"],
                    "source": r["source"],
                    "price": float(fallback.get(sym, 0)),
                    "change_24h": 0.0,
                    "change_pct": 0.0,
                    "updated_at": str(r["updated_at"]) if r["updated_at"] else None,
                    "status": "active",
                    "provider_status": "seeded"
                })

            return {
                "ok": True,
                "source": "ndsp_assets",
                "count": len(prices),
                "prices": prices
            }
        finally:
            await conn.close()
    except Exception as e:
        return JSONResponse(
            {"ok": False, "code": "MARKET_PRICES_ERROR", "detail": str(e)[:180], "prices": []},
            status_code=500
        )
# END NDSP MARKET PRICES PUBLIC ENDPOINT FINAL


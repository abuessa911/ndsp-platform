from __future__ import annotations

import hmac
import os
import secrets
import time
from typing import Optional

from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

router = APIRouter(prefix="/api/admin", tags=["admin-session"])


SESSION_COOKIE_NAME = "ndsp_admin_session"
SESSION_TTL_SECONDS = 60 * 60 * 8


def _admin_key() -> str:
    key = os.getenv("ADMIN_API_KEY") or os.getenv("NDSP_ADMIN_API_KEY")
    if not key:
        return ""
    return key


def _session_secret() -> str:
    secret = os.getenv("ADMIN_SESSION_SECRET")
    if secret:
        return secret

    fallback = _admin_key()
    if fallback:
        return fallback

    return "ndsp-dev-session-secret-change-me"


def _sign(value: str) -> str:
    import hashlib

    return hmac.new(
        _session_secret().encode("utf-8"),
        value.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def create_session_value() -> str:
    issued_at = str(int(time.time()))
    nonce = secrets.token_urlsafe(24)
    payload = f"{issued_at}.{nonce}"
    signature = _sign(payload)
    return f"{payload}.{signature}"


def is_valid_session(value: Optional[str]) -> bool:
    if not value:
        return False

    parts = value.split(".")
    if len(parts) != 3:
        return False

    issued_at, nonce, signature = parts
    payload = f"{issued_at}.{nonce}"

    expected = _sign(payload)

    if not hmac.compare_digest(signature, expected):
        return False

    try:
        age = int(time.time()) - int(issued_at)
    except Exception:
        return False

    return 0 <= age <= SESSION_TTL_SECONDS


def require_admin_session(request: Request) -> bool:
    return is_valid_session(request.cookies.get(SESSION_COOKIE_NAME))


@router.get("/login", response_class=HTMLResponse)
def admin_login_page():
    return """
<!doctype html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8" />
  <title>NDSP Admin Login</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      background: #08111f;
      color: #e5e7eb;
      font-family: Inter, Arial, sans-serif;
      display: grid;
      place-items: center;
    }
    .card {
      width: min(420px, calc(100vw - 32px));
      background: #0f1b2d;
      border: 1px solid #22314d;
      border-radius: 22px;
      padding: 28px;
      box-shadow: 0 20px 80px rgba(0,0,0,.35);
    }
    h1 {
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: -0.03em;
    }
    p {
      color: #94a3b8;
      margin: 0 0 24px;
      line-height: 1.5;
    }
    input {
      width: 100%;
      box-sizing: border-box;
      background: #07101f;
      color: #e5e7eb;
      border: 1px solid #334155;
      border-radius: 14px;
      padding: 14px 16px;
      font-size: 16px;
      outline: none;
    }
    input:focus {
      border-color: #2563eb;
    }
    button {
      width: 100%;
      margin-top: 14px;
      border: 0;
      border-radius: 14px;
      padding: 14px 16px;
      background: #2563eb;
      color: white;
      font-weight: 700;
      font-size: 16px;
      cursor: pointer;
    }
    .foot {
      margin-top: 18px;
      font-size: 12px;
      color: #64748b;
    }
  </style>
</head>
<body>
  <form class="card" method="post" action="/api/admin/login">
    <h1>NDSP Admin</h1>
    <p>Operational access only. Session expires automatically.</p>
    <input name="admin_key" type="password" placeholder="Admin key" autocomplete="current-password" autofocus />
    <button type="submit">Sign in</button>
    <div class="foot">Do not share screenshots containing credentials.</div>
  </form>
</body>
</html>
"""


@router.post("/login")
def admin_login(admin_key: str = Form(...)):
    expected = _admin_key()

    if not expected or not hmac.compare_digest(admin_key, expected):
        return HTMLResponse(
            """
            <html><body style="background:#08111f;color:#e5e7eb;font-family:Arial;padding:40px">
            <h2>Unauthorized</h2>
            <p>Invalid admin key.</p>
            <a style="color:#60a5fa" href="/api/admin/login">Back to login</a>
            </body></html>
            """,
            status_code=401,
        )

    response = RedirectResponse(url="/api/admin/ui", status_code=303)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        create_session_value(),
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=SESSION_TTL_SECONDS,
        path="/",
    )
    return response


@router.post("/logout")
def admin_logout():
    response = RedirectResponse(url="/api/admin/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return response


@router.get("/session/status")
def admin_session_status(request: Request):
    return JSONResponse(
        {
            "authenticated": require_admin_session(request),
            "ttl_seconds": SESSION_TTL_SECONDS,
        }
    )

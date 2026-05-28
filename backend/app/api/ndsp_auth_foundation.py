from __future__ import annotations

import json
import os
import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Header, HTTPException
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/v6/auth", tags=["ndsp-auth"])

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime"
USERS_FILE = RUNTIME / "ndsp_users.json"
SESSIONS_FILE = RUNTIME / "ndsp_sessions.json"

ALLOWED_PLANS = {"Free", "Pro", "Elite", "SaaS"}


def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def hash_password(password: str, salt: str | None = None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return salt, digest


def verify_password(password: str, salt: str, digest: str):
    _, test = hash_password(password, salt)
    return secrets.compare_digest(test, digest)


@router.post("/register")
def register(payload: dict = Body(default={})):
    email = str(payload.get("email", "")).strip().lower()
    name = str(payload.get("name", "")).strip()
    password = str(payload.get("password", "")).strip()
    plan = str(payload.get("plan", "Free")).strip() or "Free"

    if plan not in ALLOWED_PLANS:
        plan = "Free"

    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="valid email required")

    if len(password) < 6:
        raise HTTPException(status_code=400, detail="password must be at least 6 characters")

    users = load_json(USERS_FILE, {"users": []})

    if any(u.get("email") == email for u in users["users"]):
        raise HTTPException(status_code=409, detail="user already exists")

    salt, digest = hash_password(password)

    user = {
        "id": secrets.token_hex(16),
        "email": email,
        "name": name or email.split("@")[0],
        "plan": plan,
        "status": "active",
        "password_salt": salt,
        "password_hash": digest,
        "created_at": now(),
        "updated_at": now(),
    }

    users["users"].append(user)
    save_json(USERS_FILE, users)

    safe = {k: v for k, v in user.items() if not k.startswith("password_")}
    return {"ok": True, "user": safe}


@router.post("/login")
def login(payload: dict = Body(default={})):
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", "")).strip()

    users = load_json(USERS_FILE, {"users": []})
    user = next((u for u in users["users"] if u.get("email") == email), None)

    if not user or not verify_password(password, user.get("password_salt", ""), user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="invalid email or password")

    if user.get("status") != "active":
        raise HTTPException(status_code=403, detail="user is not active")

    token = secrets.token_urlsafe(48)
    expires = datetime.now(timezone.utc) + timedelta(days=14)

    sessions = load_json(SESSIONS_FILE, {"sessions": []})
    sessions["sessions"].append({
        "token": token,
        "email": email,
        "created_at": now(),
        "expires_at": expires.isoformat(),
    })
    save_json(SESSIONS_FILE, sessions)

    safe = {k: v for k, v in user.items() if not k.startswith("password_")}
    return {"ok": True, "token": token, "user": safe}


@router.get("/me")
def me(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")

    token = authorization.split(" ", 1)[1].strip()

    sessions = load_json(SESSIONS_FILE, {"sessions": []})
    session = next((s for s in sessions["sessions"] if s.get("token") == token), None)

    if not session:
        raise HTTPException(status_code=401, detail="invalid session")

    try:
        expires = datetime.fromisoformat(session["expires_at"])
        if expires < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="session expired")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="invalid session")

    users = load_json(USERS_FILE, {"users": []})
    user = next((u for u in users["users"] if u.get("email") == session.get("email")), None)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    safe = {k: v for k, v in user.items() if not k.startswith("password_")}
    return {"ok": True, "user": safe}

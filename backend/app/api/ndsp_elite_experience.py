from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/api/v6", tags=["ndsp-elite-experience"])

SYSTEM = "NDSP"
VERSION = "1.0.0"
GOVERNANCE_VERSION = os.getenv("NDSP_GOVERNANCE_VERSION", "6.1.0")
MAX_BETA_USERS = int(os.getenv("NDSP_ELITE_TRIAL_MAX", "50"))

DATA_DIR = Path(os.getenv("NDSP_STATE_DIR", "/var/lib/ndsp"))
ELITE_STATE_FILE = DATA_DIR / "elite_experience_state.json"
WAITLIST_FILE = DATA_DIR / "elite_waitlist.json"
AUDIT_FILE = DATA_DIR / "audit_log.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def rid() -> str:
    return str(uuid.uuid4())


def ensure_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not ELITE_STATE_FILE.exists():
        ELITE_STATE_FILE.write_text(
            json.dumps(
                {
                    "max_beta_users": MAX_BETA_USERS,
                    "registered_count": 0,
                    "manual_override_full": False,
                    "updated_at": now_iso(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    if not WAITLIST_FILE.exists():
        WAITLIST_FILE.write_text(json.dumps({"items": []}, ensure_ascii=False, indent=2), encoding="utf-8")

    if not AUDIT_FILE.exists():
        AUDIT_FILE.touch()


def read_json(path: Path, fallback: Dict[str, Any]) -> Dict[str, Any]:
    ensure_files()
    try:
        raw = path.read_text(encoding="utf-8").strip()
        return json.loads(raw) if raw else fallback
    except Exception:
        return fallback


def write_json(path: Path, data: Dict[str, Any]) -> None:
    ensure_files()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)


def audit(event: str, status: str, extra: Optional[Dict[str, Any]] = None) -> None:
    ensure_files()
    record = {
        "timestamp": now_iso(),
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "request_id": rid(),
        "event": event,
        "status": status,
        "extra": extra or {},
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def admin_key_valid(x_admin_key: Optional[str]) -> bool:
    expected = os.getenv("ADMIN_KEY", "").strip()
    return bool(expected and x_admin_key and x_admin_key.strip() == expected)


class WaitlistPayload(BaseModel):
    email: EmailStr
    name: str = Field(default="", max_length=120)
    access_type: str = Field(default="official_launch", max_length=80)
    note: str = Field(default="", max_length=500)


class CapacityUpdatePayload(BaseModel):
    registered_count: Optional[int] = None
    manual_override_full: Optional[bool] = None
    max_beta_users: Optional[int] = None


@router.get("/elite-trial/capacity")
def elite_trial_capacity():
    state = read_json(
        ELITE_STATE_FILE,
        {
            "max_beta_users": MAX_BETA_USERS,
            "registered_count": 0,
            "manual_override_full": False,
            "updated_at": now_iso(),
        },
    )

    max_users = int(state.get("max_beta_users") or MAX_BETA_USERS)
    registered = int(state.get("registered_count") or 0)
    is_full = bool(state.get("manual_override_full")) or registered >= max_users

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "capacity": {
            "max_beta_users": max_users,
            "registered_count": registered,
            "remaining": max(0, max_users - registered),
            "is_full": is_full,
            "hard_stop_url": "/elite/full",
            "message_ar": "مرحلة النخبة مغلقة حالياً" if is_full else "مرحلة النخبة متاحة حالياً",
            "message_en": "Elite phase is currently closed" if is_full else "Elite phase is currently available",
        },
    }


@router.post("/elite-trial/capacity")
def update_elite_capacity(payload: CapacityUpdatePayload, x_admin_key: Optional[str] = Header(None)):
    if not admin_key_valid(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    state = read_json(
        ELITE_STATE_FILE,
        {
            "max_beta_users": MAX_BETA_USERS,
            "registered_count": 0,
            "manual_override_full": False,
            "updated_at": now_iso(),
        },
    )

    if payload.max_beta_users is not None:
        state["max_beta_users"] = max(1, int(payload.max_beta_users))

    if payload.registered_count is not None:
        state["registered_count"] = max(0, int(payload.registered_count))

    if payload.manual_override_full is not None:
        state["manual_override_full"] = bool(payload.manual_override_full)

    state["updated_at"] = now_iso()
    write_json(ELITE_STATE_FILE, state)

    audit("elite_capacity_updated", "completed", {"state": state})

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "state": state,
    }


@router.post("/elite-trial/waitlist")
async def join_waitlist(payload: WaitlistPayload, request: Request):
    data = read_json(WAITLIST_FILE, {"items": []})
    items = data.setdefault("items", [])

    email = str(payload.email).strip().lower()
    existing = next((x for x in items if str(x.get("email", "")).lower() == email), None)

    if existing:
        existing["updated_at"] = now_iso()
        existing["name"] = payload.name.strip()
        existing["access_type"] = payload.access_type.strip()
        existing["note"] = payload.note.strip()
        write_json(WAITLIST_FILE, data)

        audit("waitlist_duplicate_updated", "completed", {"email": email})

        return {
            "ok": True,
            "system": SYSTEM,
            "version": VERSION,
            "governance_version": GOVERNANCE_VERSION,
            "status": "updated",
            "message": "تم تحديث طلبك في قائمة الانتظار.",
        }

    item = {
        "id": rid(),
        "email": email,
        "name": payload.name.strip(),
        "access_type": payload.access_type.strip(),
        "note": payload.note.strip(),
        "source": "elite_hard_stop_page",
        "ip_hint": request.client.host if request.client else None,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "system": SYSTEM,
    }

    items.append(item)
    write_json(WAITLIST_FILE, data)

    audit("waitlist_joined", "completed", {"email": email, "access_type": item["access_type"]})

    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "status": "created",
        "message": "تم تسجيلك في قائمة انتظار الإطلاق الرسمي.",
    }


@router.get("/elite-trial/waitlist")
def list_waitlist(x_admin_key: Optional[str] = Header(None)):
    if not admin_key_valid(x_admin_key):
        raise HTTPException(status_code=401, detail="unauthorized")

    data = read_json(WAITLIST_FILE, {"items": []})
    return {
        "ok": True,
        "system": SYSTEM,
        "version": VERSION,
        "governance_version": GOVERNANCE_VERSION,
        "items": data.get("items", []),
        "count": len(data.get("items", [])),
    }

from __future__ import annotations

import os
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.services.elite_trial_service import close_expired_accounts, create_trial, summary, state
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/v6/elite-trial", tags=["elite-trial"])


class TrialRequest(BaseModel):
    client_ip: str | None = None
    device_fingerprint: str | None = None
    email: str
    name: str = ""


def require_admin(x_admin_key: str | None) -> None:
    expected = os.getenv("NDSP_ADMIN_KEY", "")
    if not expected or x_admin_key != expected:
        raise HTTPException(status_code=401, detail="admin_required")


@router.get("/status")
def elite_trial_status():
    return summary()


@router.get("/admin")
def elite_trial_admin(x_admin_key: str | None = Header(default=None), admin_key: str | None = None):
    key = x_admin_key or admin_key
    require_admin(key)
    close_expired_accounts()
    st = state()
    return {
        "summary": summary(),
        "ordinary": st.get("ordinary", []),
        "analysts": st.get("analysts", []),
        "waitlist": st.get("waitlist", []),
        "closed": st.get("closed", [])
    }


@router.post("/ordinary")
def open_ordinary_trial(payload: TrialRequest):
    return create_trial(
        email=payload.email,
        name=payload.name,
        account_type="ordinary",
        created_by="system"
    )


@router.post("/analyst")
def open_analyst_trial(payload: TrialRequest, x_admin_key: str | None = Header(default=None)):
    require_admin(x_admin_key)
    return create_trial(
        email=payload.email,
        name=payload.name,
        account_type="analyst",
        created_by="admin"
    )


@router.post("/close-expired")
def close_expired(x_admin_key: str | None = Header(default=None)):
    require_admin(x_admin_key)
    return close_expired_accounts()

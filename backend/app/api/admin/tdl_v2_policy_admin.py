from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.core.tdl_v2_policy import read_tdl_v2_policy, write_tdl_v2_policy

router = APIRouter(prefix="/api/admin/timing_model-v2", tags=["admin-timing_model-v2"])


class TdlV2PolicyUpdate(BaseModel):
    tdl_v2_enabled: Optional[bool] = None
    timing_layer_enabled: Optional[bool] = None
    timing_mode: Optional[str] = None
    mon_wed_controller: Optional[str] = None
    thu_fri_controller: Optional[str] = None
    sunday_mode: Optional[str] = None
    output_policy: Optional[str] = None


def _mask(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 12:
        return "***"
    return f"{value[:6]}...{value[-4:]}"


def _expected_keys() -> list[str]:
    keys: list[str] = []
    for name in ("ADMIN_KEY", "NDSP_ADMIN_KEY", "ADMIN_UI_KEY"):
        value = (os.getenv(name) or "").strip().strip('"').strip("'")
        if value and value not in keys:
            keys.append(value)
    return keys


def _require_admin(
    x_admin_key: Optional[str],
    x_admin_key_alt: Optional[str] = None,
    authorization: Optional[str] = None,
) -> None:
    expected = _expected_keys()

    supplied_values = []
    for value in (x_admin_key, x_admin_key_alt):
        v = (value or "").strip().strip('"').strip("'")
        if v:
            supplied_values.append(v)

    auth = (authorization or "").strip()
    if auth.lower().startswith("bearer "):
        supplied_values.append(auth.split(" ", 1)[1].strip())

    if not expected:
        raise HTTPException(status_code=500, detail="admin_key_not_configured")

    for supplied in supplied_values:
        if supplied in expected:
            return

    raise HTTPException(
        status_code=403,
        detail={
            "error": "invalid_admin_key",
            "expected_count": len(expected),
            "supplied_count": len(supplied_values),
            "expected_preview": [_mask(k) for k in expected],
            "supplied_preview": [_mask(k) for k in supplied_values],
        },
    )


@router.get("/auth-debug")
def auth_debug(
    x_admin_key: Optional[str] = Header(default=None),
    x_admin_key_alt: Optional[str] = Header(default=None, alias="x-admin-key"),
    authorization: Optional[str] = Header(default=None),
):
    expected = _expected_keys()
    supplied = (x_admin_key or x_admin_key_alt or authorization or "").strip()
    return {
        "ok": True,
        "expected_count": len(expected),
        "expected_preview": [_mask(k) for k in expected],
        "supplied_preview": _mask(supplied),
        "env_present": {
            "ADMIN_KEY": bool(os.getenv("ADMIN_KEY")),
            "NDSP_ADMIN_KEY": bool(os.getenv("NDSP_ADMIN_KEY")),
            "ADMIN_UI_KEY": bool(os.getenv("ADMIN_UI_KEY")),
        }
    }


@router.get("/policy")
def get_tdl_v2_policy(
    x_admin_key: Optional[str] = Header(default=None),
    x_admin_key_alt: Optional[str] = Header(default=None, alias="x-admin-key"),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, x_admin_key_alt, authorization)
    return {"ok": True, "policy": read_tdl_v2_policy()}


@router.post("/policy")
def update_tdl_v2_policy(
    payload: TdlV2PolicyUpdate,
    x_admin_key: Optional[str] = Header(default=None),
    x_admin_key_alt: Optional[str] = Header(default=None, alias="x-admin-key"),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, x_admin_key_alt, authorization)

    updates: Dict[str, Any] = {
        k: v for k, v in payload.model_dump().items()
        if v is not None
    }

    if "timing_mode" in updates and updates["timing_mode"] not in {"control_days", "bypassed", "experimental"}:
        raise HTTPException(status_code=400, detail="invalid_timing_mode")

    if "output_policy" in updates and updates["output_policy"] != "tdl_v2_only":
        raise HTTPException(status_code=400, detail="output_policy_must_be_tdl_v2_only")

    return {"ok": True, "policy": write_tdl_v2_policy(updates, updated_by="admin")}


@router.post("/timing/enable")
def enable_timing_layer(
    x_admin_key: Optional[str] = Header(default=None),
    x_admin_key_alt: Optional[str] = Header(default=None, alias="x-admin-key"),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, x_admin_key_alt, authorization)
    return {
        "ok": True,
        "policy": write_tdl_v2_policy(
            {"timing_layer_enabled": True, "timing_mode": "control_days"},
            updated_by="admin"
        )
    }


@router.post("/timing/disable")
def disable_timing_layer(
    x_admin_key: Optional[str] = Header(default=None),
    x_admin_key_alt: Optional[str] = Header(default=None, alias="x-admin-key"),
    authorization: Optional[str] = Header(default=None),
):
    _require_admin(x_admin_key, x_admin_key_alt, authorization)
    return {
        "ok": True,
        "policy": write_tdl_v2_policy(
            {"timing_layer_enabled": False, "timing_mode": "bypassed"},
            updated_by="admin"
        )
    }

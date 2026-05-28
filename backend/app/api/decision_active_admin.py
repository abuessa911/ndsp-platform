from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.core.ndsp_governance_mode import (
    governance_mode_public,
    set_timing_layer_enabled,
    save_governance_mode,
)

router = APIRouter(prefix="/api/v6/governance", tags=["NDSP Governance"])


class TimingToggleRequest(BaseModel):
    enabled: bool


def _require_admin(x_admin_key: Optional[str]) -> None:
    expected = os.getenv("ADMIN_KEY") or os.getenv("NDSP_ADMIN_KEY")
    if not expected:
        raise HTTPException(status_code=503, detail="admin_auth_not_configured")
    if not x_admin_key or x_admin_key != expected:
        raise HTTPException(status_code=401, detail="invalid_admin_key")


@router.get("/mode")
def get_governance_mode() -> Dict[str, Any]:
    return governance_mode_public()


@router.post("/decision-active")
def enable_decision_active(x_admin_key: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    _require_admin(x_admin_key)
    return save_governance_mode(
        {
            "mode": "DECISION_ACTIVE",
            "execution_policy": "EXECUTION_SANITIZED",
            "decision_active": True,
            "execution_sanitized": True,
            "all_layers_participate": True,
            "no_layer_disabled": True,
            "tdl_direction_authority": True,
            "direct_trade_execution": False,
            "public_buy_sell_commands": False,
            "public_tp_sl": False,
            "raw_logic_public": False,
        }
    )


@router.post("/timing-layer")
def toggle_timing_layer(
    payload: TimingToggleRequest,
    x_admin_key: Optional[str] = Header(default=None),
) -> Dict[str, Any]:
    _require_admin(x_admin_key)
    return set_timing_layer_enabled(payload.enabled)

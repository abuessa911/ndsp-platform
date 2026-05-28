from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.governance.admin_only import require_admin_role
from app.saas.subscriptions_db import list_audit_events

router = APIRouter(prefix="/api/admin/audit", tags=["audit-admin-v6"])


@router.get("", dependencies=[Depends(require_admin_role)])
def admin_list_audit_events(limit: int = Query(default=200, ge=1, le=1000)):
    return {
        "status": "ok",
        "events": list_audit_events(limit=limit),
    }

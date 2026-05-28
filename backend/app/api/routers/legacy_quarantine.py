from __future__ import annotations
from fastapi import APIRouter, Depends
from app.governance.admin_only import require_admin_role
from app.governance.quarantine import QUARANTINED_FILES

router = APIRouter(prefix="/api/v6/admin", tags=["legacy-quarantine"])

@router.get("/legacy-quarantine", dependencies=[Depends(require_admin_role)])
def get_legacy_quarantine():
    return {
        "status": "ok",
        "quarantined_count": len(QUARANTINED_FILES),
        "files": list(QUARANTINED_FILES),
    }

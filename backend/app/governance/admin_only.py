from __future__ import annotations

import hmac
import os
from typing import Optional

from fastapi import HTTPException, Query


def get_admin_key() -> str:
    return (
        os.getenv("ADMIN_API_KEY")
        or os.getenv("NDSP_ADMIN_API_KEY")
        or os.getenv("ADMIN_UI_KEY")
        or ""
    )


def require_admin_role(
    admin_key: Optional[str] = Query(default=None),
) -> bool:
    expected = get_admin_key()

    if expected and admin_key and hmac.compare_digest(str(admin_key), str(expected)):
        return True

    raise HTTPException(status_code=401, detail="Invalid admin_key")

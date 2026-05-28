from fastapi import HTTPException

FORBIDDEN_USER_PATH_MARKERS = (
    "trade",
    "trading",
    "signal",
    "executor",
    "execution",
    "paper",
    "live_trader",
    "binance",
    "orderflow",
)

def assert_governed_user_route(path: str) -> None:
    lowered = path.lower()
    for marker in FORBIDDEN_USER_PATH_MARKERS:
        if marker in lowered:
            raise HTTPException(
                status_code=403,
                detail="Blocked by NDSP Governance v6: user-facing access to non-governed route is forbidden."
            )

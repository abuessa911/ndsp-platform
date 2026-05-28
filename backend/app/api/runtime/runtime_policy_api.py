from fastapi import APIRouter
from app.runtime.package_policy import get_package_policy

router = APIRouter()


@router.get("/runtime/policy")
async def runtime_policy(
    package: str = "free"
):

    policy = get_package_policy(package)

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "package_runtime": policy,
        "logic_leak": False,
        "protected": True,
    }

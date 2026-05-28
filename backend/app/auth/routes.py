from fastapi import Request, APIRouter

# NDSP_DUPLICATE_GUARD_START
def ndsp_get_client_ip(request: Request) -> str:
    xff = request.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    xrip = request.headers.get("x-real-ip", "")
    if xrip:
        return xrip.strip()
    if request.client:
        return request.client.host
    return "unknown"

def ndsp_get_device_fingerprint(request: Request) -> str:
    fp = request.headers.get("x-ndsp-device-fingerprint", "").strip()
    if fp:
        return fp[:160]
    ua = request.headers.get("user-agent", "unknown")[:180]
    lang = request.headers.get("accept-language", "unknown")[:80]
    return f"ua:{ua}|lang:{lang}"
# NDSP_DUPLICATE_GUARD_END

from app.auth.models import TrialRegister, TokenLogin
from app.auth.storage import create_user, login
from app.core.mailer import send_trial_token, notify_admin
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter()

@router.post("/api/v1/auth/register-trial")
def register_trial(request: Request, data: TrialRegister):


    # NDSP_IP_DEVICE_DUPLICATE_GUARD_START
    client_ip = ndsp_get_client_ip(request)
    device_fingerprint = ndsp_get_device_fingerprint(request)

    try:
        payload.client_ip = client_ip
    except Exception:
        pass

    try:
        payload.device_fingerprint = device_fingerprint
    except Exception:
        pass
    # NDSP_IP_DEVICE_DUPLICATE_GUARD_END
    user = create_user(data.email, data.name)

    send_trial_token(
        data.email,
        user["token"]
    )

    notify_admin(data.email)

    return {
        "ok": True,
        "message": "Token sent",
        "plan": "Elite"
    }

@router.post("/api/v1/auth/token-login")
def token_login(data: TokenLogin):

    user = login(
        data.email,
        data.token
    )

    if not user:
        return {
            "ok": False,
            "message": "Invalid token"
        }

    return {
        "ok": True,
        "email": user["email"],
        "name": user["name"],
        "plan": user["plan"]
    }

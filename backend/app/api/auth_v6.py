from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import json
import secrets
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/v6/auth", tags=["NDSP Auth"])

DB = Path("/home/nawaf511/empire-core-new/backend/runtime/ndsp_users.json")

class AuthRequest(BaseModel):
    client_ip: str | None = None
    device_fingerprint: str | None = None
    email: str
    password: str
    name: str | None = "NDSP User"
    plan: str | None = "Free"

def load_users():
    if not DB.exists():
        DB.write_text(json.dumps({"users": []}))
    return json.loads(DB.read_text())

def save_users(data):
    DB.write_text(json.dumps(data, indent=2))

@router.post("/register")
def register(req: AuthRequest):
    data = load_users()

    for u in data["users"]:
        if u["email"].lower() == req.email.lower():
            return {"ok": False, "detail": "user_already_exists"}

    user = {
        "email": req.email,
        "password": req.password,
        "name": req.name,
        "plan": req.plan,
    }

    data["users"].append(user)
    save_users(data)

    return {
        "ok": True,
        "message": "registered",
        "user": {
            "email": user["email"],
            "name": user["name"],
            "plan": user["plan"],
        }
    }

@router.post("/login")
def login(req: AuthRequest):
    data = load_users()

    for u in data["users"]:
        if (
            u["email"].lower() == req.email.lower()
            and u["password"] == req.password
        ):
            return {
                "ok": True,
                "token": secrets.token_hex(32),
                "user": {
                    "email": u["email"],
                    "name": u["name"],
                    "plan": u["plan"],
                }
            }

    return {
        "ok": False,
        "detail": "user_not_found"
    }

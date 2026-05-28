from app.ndsp_db_env_loader import load_ndsp_db_env
load_ndsp_db_env(force=True)
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import json, secrets
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/v6/auth2", tags=["NDSP Auth2"])

DB = Path("/home/nawaf511/empire-core-new/backend/runtime/ndsp_auth2_users.json")
DB.parent.mkdir(parents=True, exist_ok=True)

class Req(BaseModel):
    client_ip: str | None = None
    device_fingerprint: str | None = None
    email: str
    password: str
    name: str | None = "NDSP User"
    plan: str | None = "Elite"

def load():
    if not DB.exists():
        DB.write_text(json.dumps({"users": [
            {"email":"demo@ndsp.app","password":"123456","name":"NDSP Demo","plan":"Elite","status":"active"}
        ]}, indent=2))
    return json.loads(DB.read_text())

def save(data):
    DB.write_text(json.dumps(data, indent=2, ensure_ascii=False))

@router.post("/register")
def register(req: Req):
    data = load()
    email = req.email.strip().lower()

    for u in data["users"]:
        if u["email"].lower() == email:
            return {"ok": True, "detail": "user_already_exists", "user": {
                "email": u["email"], "name": u["name"], "plan": u["plan"], "status": u.get("status","active")
            }}

    user = {
        "email": email,
        "password": req.password,
        "name": req.name or email,
        "plan": req.plan or "Free",
        "status": "active"
    }
    data["users"].append(user)
    save(data)

    return {"ok": True, "user": {
        "email": user["email"], "name": user["name"], "plan": user["plan"], "status": user["status"]
    }}

@router.post("/login")
def login(req: Req):
    data = load()
    email = req.email.strip().lower()

    for u in data["users"]:
        if u["email"].lower() == email and u["password"] == req.password:
            return {
                "ok": True,
                "token": secrets.token_urlsafe(48),
                "user": {
                    "email": u["email"],
                    "name": u["name"],
                    "plan": u["plan"],
                    "status": u.get("status","active")
                }
            }

    return {"ok": False, "detail": "auth2_user_not_found"}

@router.get("/me")
def me():
    data = load()
    u = data["users"][0]
    return {"ok": True, "user": {
        "email": u["email"], "name": u["name"], "plan": u["plan"], "status": u.get("status","active")
    }}

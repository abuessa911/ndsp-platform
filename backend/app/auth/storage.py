import os
import json
import secrets
from pathlib import Path

BASE = Path("runtime")
BASE.mkdir(exist_ok=True)

DB = BASE / "trial_users.json"

if not DB.exists():
    DB.write_text("[]")

def load_users():
    return json.loads(DB.read_text())

def save_users(data):
    DB.write_text(json.dumps(data, indent=2))

def create_user(email, name):

    users = load_users()

    token = secrets.token_hex(16)

    item = {
        "email": email,
        "name": name,
        "token": token,
        "plan": "Elite",
        "active": True
    }

    users.append(item)

    save_users(users)

    return item

def login(email, token):

    users = load_users()

    for u in users:

        if (
            u["email"] == email and
            u["token"] == token and
            u["active"]
        ):
            return u

    return None

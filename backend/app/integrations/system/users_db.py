import json
import os

DB_FILE = "/home/nawaf511/empire-core-new/backend/data/users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def activate_user(user_id):
    users = load_users()
    users[str(user_id)] = {
        "active": True
    }
    save_users(users)

def is_active(user_id):
    users = load_users()
    return users.get(str(user_id), {}).get("active", False)

from __future__ import annotations
from app.core.mailer import send_trial_token, notify_admin


import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4
from app.core.elite_trial_capacity import enforce_elite_trial_capacity


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "elite_trial_config.json"
STATE_PATH = ROOT / "runtime" / "elite_trial_accounts.json"

AccountType = Literal["ordinary", "analyst"]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def config() -> dict[str, Any]:
    return load_json(CONFIG_PATH, {
        "enabled": True,
        "plan": "Elite",
        "trial_days": 16,
        "ordinary_limit": 30,
        "analyst_manual_limit": 10,
        "ordinary_auto_open": True,
        "analyst_manual_only": True,
        "after_expiry_status": "closed"
    })


def state() -> dict[str, Any]:
    return load_json(STATE_PATH, {
        "ordinary": [],
        "analysts": [],
        "closed": [],
        "waitlist": []
    })


def _find_account(st: dict[str, Any], email: str):
    email_l = email.strip().lower()
    for bucket in ("ordinary", "analysts", "closed", "waitlist"):
        for acc in st.get(bucket, []):
            if str(acc.get("email", "")).lower() == email_l:
                return bucket, acc
    return None, None


def close_expired_accounts() -> dict[str, Any]:
    st = state()
    now = utcnow()
    moved = []

    for bucket in ("ordinary", "analysts"):
        remaining = []
        for acc in st.get(bucket, []):
            expires_at = parse_dt(acc["expires_at"])
            if expires_at <= now:
                acc["status"] = "closed"
                acc["closed_at"] = iso(now)
                acc["close_reason"] = "elite_trial_expired"
                st.setdefault("closed", []).append(acc)
                moved.append(acc)
            else:
                remaining.append(acc)
        st[bucket] = remaining

    save_json(STATE_PATH, st)

    return {"closed_count": len(moved), "closed": moved}


def summary() -> dict[str, Any]:
    cfg = config()
    close_expired_accounts()
    st = state()
    ordinary_limit = int(cfg.get("ordinary_limit", 30))
    analyst_limit = int(cfg.get("analyst_manual_limit", 10))
    return {
        "enabled": bool(cfg.get("enabled")),
        "plan": cfg.get("plan", "Elite"),
        "trial_days": int(cfg.get("trial_days", 14)),
        "ordinary_limit": ordinary_limit,
        "analyst_manual_limit": analyst_limit,
        "ordinary_used": len(st.get("ordinary", [])),
        "analyst_used": len(st.get("analysts", [])),
        "ordinary_remaining": max(0, ordinary_limit - len(st.get("ordinary", []))),
        "analyst_remaining": max(0, analyst_limit - len(st.get("analysts", []))),
        "closed_count": len(st.get("closed", [])),
        "waitlist_count": len(st.get("waitlist", [])),
        "public_message_ar": cfg.get("public_message_ar"),
        "public_message_en": cfg.get("public_message_en")
    }


def create_trial(email: str, name: str = "", account_type: AccountType = "ordinary", created_by: str = "system") -> dict[str, Any]:
    cfg = config()
    if not cfg.get("enabled", True):
        return {"ok": False, "status": "disabled", "reason": "elite_trial_disabled"}

    close_expired_accounts()
    st = state()

    email = email.strip().lower()
    name = name.strip()

    if not email or "@" not in email:
        return {"ok": False, "status": "invalid", "reason": "invalid_email"}

    existing_bucket, existing = _find_account(st, email)
    if existing:
        return {"ok": True, "status": existing.get("status"), "bucket": existing_bucket, "account": existing, "reason": "already_exists"}

    now = utcnow()
    expires_at = now + timedelta(days=int(cfg.get("trial_days", 14)))

    if account_type == "ordinary":
        if len(st.get("ordinary", [])) >= int(cfg.get("ordinary_limit", 30)):
            acc = {
                "id": str(uuid4()),
                "email": email,
                "name": name,
                "type": "ordinary",
                "plan": cfg.get("plan", "Elite"),
                "status": "waitlist",
                "created_at": iso(now),
                "created_by": created_by,
                "reason": "ordinary_trial_limit_reached"
            }
            st.setdefault("waitlist", []).append(acc)
            save_json(STATE_PATH, st)
            return {"ok": False, "status": "waitlist", "account": acc, "reason": "ordinary_trial_limit_reached"}

        bucket = "ordinary"

    elif account_type == "analyst":
        if created_by not in ("admin", "manual_admin"):
            return {"ok": False, "status": "rejected", "reason": "analyst_requires_admin_manual_activation"}

        if len(st.get("analysts", [])) >= int(cfg.get("analyst_manual_limit", 10)):
            return {"ok": False, "status": "full", "reason": "analyst_manual_limit_reached"}

        bucket = "analysts"

    else:
        return {"ok": False, "status": "invalid", "reason": "invalid_account_type"}

    acc = {
        "id": str(uuid4()),
        "email": email,
        "name": name,
        "type": account_type,
        "plan": cfg.get("plan", "Elite"),
        "status": "active",
        "features": "full_elite",
        "created_at": iso(now),
        "expires_at": iso(expires_at),
        "created_by": created_by
    }

    st.setdefault(bucket, []).append(acc)
    save_json(STATE_PATH, st)

    # NDSP_CREATE_TRIAL_MAIL_SEND_START
    try:
        token_value = acc.get("activation_token") or acc.get("token") or acc.get("id")
        send_trial_token(acc.get("email"), token_value)
        notify_admin(acc.get("email"))
    except Exception as e:
        print(f"MAIL PATCH ERROR => {e}")
    # NDSP_CREATE_TRIAL_MAIL_SEND_END

    return {"ok": True, "status": "active", "bucket": bucket, "account": acc}

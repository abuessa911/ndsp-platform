from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Body, Header, HTTPException, Query, Depends
from app.core.elite_trial_capacity import enforce_elite_trial_capacity

router = APIRouter(prefix="/api/admin/ops", tags=["admin-ops"])

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "runtime"
ELITE_STATE = RUNTIME / "elite_trial_accounts.json"
OPS_LOG = RUNTIME / "admin_ops_audit.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _admin_key() -> str:
    return (
        os.getenv("ADMIN_UI_KEY", "").strip()
        or os.getenv("ADMIN_KEY", "").strip()
        or os.getenv("NDSP_ADMIN_KEY", "").strip()
    )


def _require_admin(
    x_admin_key: str | None = Header(default=None, alias="x-admin-key"),
    admin_key: str | None = Query(default=None),
):
    expected = (_admin_key() or "").strip()
    provided = (x_admin_key or admin_key or "").strip()
    if not expected or provided != expected:
        raise HTTPException(status_code=401, detail="Invalid admin_key")
    return True



def _audit(action: str, payload: dict[str, Any] | None = None):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    row = {
        "timestamp": _now(),
        "system": "NDSP",
        "actor": "admin",
        "action": action,
        "payload": payload or {},
    }
    with OPS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_elite_state() -> dict[str, Any]:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    if not ELITE_STATE.exists():
        return {"ordinary": [], "analysts": [], "closed": [], "waitlist": []}
    try:
        return json.loads(ELITE_STATE.read_text(encoding="utf-8"))
    except Exception:
        return {"ordinary": [], "analysts": [], "closed": [], "waitlist": []}


def _save_elite_state(state: dict[str, Any]):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    ELITE_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _find_account(state: dict[str, Any], email: str):
    email = email.strip().lower()
    for bucket in ["ordinary", "analysts", "waitlist", "closed"]:
        for idx, acc in enumerate(state.get(bucket, [])):
            if str(acc.get("email", "")).strip().lower() == email:
                return bucket, idx, acc
    return None, None, None


@router.get("/health")
def ops_health(_: bool = Depends(_require_admin)):
    return {
        "ok": True,
        "system": "NDSP",
        "service": "admin_ops",
        "timestamp": _now(),
        "elite_state_exists": ELITE_STATE.exists(),
        "audit_log": str(OPS_LOG),
    }


@router.post("/elite/status")
def elite_change_status(
    payload: dict[str, Any] = Body(default={}),
    _: bool = Depends(_require_admin),
):
    email = str(payload.get("email", "")).strip().lower()
    status = str(payload.get("status", "")).strip().lower()
    target_bucket = str(payload.get("bucket", "")).strip().lower()

    if not email:
        raise HTTPException(status_code=400, detail="email required")

    if status not in ["active", "pending", "rejected", "expired", "closed", "waitlist"]:
        raise HTTPException(status_code=400, detail="invalid status")

    state = _load_elite_state()
    old_bucket, idx, acc = _find_account(state, email)

    if acc is None:
        raise HTTPException(status_code=404, detail="account not found")

    acc["status"] = status
    acc["updated_at"] = _now()

    if status in ["closed", "expired", "rejected"]:
        acc["close_reason"] = status
        if old_bucket != "closed":
            state[old_bucket].pop(idx)
            state.setdefault("closed", []).append(acc)

    elif status == "waitlist":
        if old_bucket != "waitlist":
            state[old_bucket].pop(idx)
            state.setdefault("waitlist", []).append(acc)

    elif status == "active":
        move_to = "analysts" if target_bucket == "analysts" or acc.get("type") == "analyst" else "ordinary"
        if old_bucket != move_to:
            state[old_bucket].pop(idx)
            state.setdefault(move_to, []).append(acc)

    _save_elite_state(state)
    _audit("elite_change_status", {"email": email, "status": status})

    return {"ok": True, "account": acc, "state": status}


@router.post("/elite/extend")
def elite_extend(
    payload: dict[str, Any] = Body(default={}),
    _: bool = Depends(_require_admin),
):
    from datetime import timedelta

    email = str(payload.get("email", "")).strip().lower()
    days = int(payload.get("days", 7))

    if not email:
        raise HTTPException(status_code=400, detail="email required")

    if days < 1 or days > 365:
        raise HTTPException(status_code=400, detail="days must be 1-365")

    state = _load_elite_state()
    bucket, idx, acc = _find_account(state, email)

    if acc is None:
        raise HTTPException(status_code=404, detail="account not found")

    base = datetime.now(timezone.utc)
    try:
        if acc.get("expires_at"):
            base = datetime.fromisoformat(str(acc["expires_at"]).replace("Z", "+00:00"))
    except Exception:
        base = datetime.now(timezone.utc)

    acc["expires_at"] = (base + timedelta(days=days)).isoformat()
    acc["updated_at"] = _now()

    _save_elite_state(state)
    _audit("elite_extend", {"email": email, "days": days})

    return {"ok": True, "account": acc}


@router.post("/user/package")
def user_package(
    payload: dict[str, Any] = Body(default={}),
    _: bool = Depends(_require_admin),
):
    email = str(payload.get("email", "")).strip().lower()
    package = str(payload.get("package", "")).strip()

    if package not in ["Free", "Pro", "Elite", "SaaS"]:
        raise HTTPException(status_code=400, detail="package must be Free, Pro, Elite, or SaaS")

    _audit("user_package_change_requested", {"email": email, "package": package})

    return {
        "ok": True,
        "message": "Package control request logged. Permanent PostgreSQL user update should be connected in the next DB-auth phase.",
        "email": email,
        "package": package,
    }


@router.post("/payment/manual-confirm")
def payment_manual_confirm(
    payload: dict[str, Any] = Body(default={}),
    _: bool = Depends(_require_admin),
):
    _audit("payment_manual_confirm_requested", payload)
    return {
        "ok": True,
        "message": "Manual payment confirmation request logged. Existing payments endpoint remains source of truth.",
        "payload": payload,
    }


@router.post("/system/health-check")
def system_health_check(_: bool = Depends(_require_admin)):
    checks = {}

    for name, cmd in {
        "disk": ["bash", "-lc", "df -h / | tail -1"],
        "memory": ["bash", "-lc", "free -h | awk 'NR==2{print}'"],
        "backend_port": ["bash", "-lc", "ss -ltnp | grep ':9001' | head -1 || true"],
    }.items():
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=8)
            checks[name] = out.strip()
        except Exception as e:
            checks[name] = f"ERROR: {e}"

    _audit("system_health_check", {})
    return {"ok": True, "checks": checks, "timestamp": _now()}


@router.post("/system/restart-backend")
def system_restart_backend(_: bool = Depends(_require_admin)):
    service = os.getenv("NDSP_BACKEND_SERVICE", "ndsp-api.service")
    allowed = os.getenv("NDSP_ALLOW_ADMIN_RESTART", "false").lower() == "true"

    if not allowed:
        _audit("restart_backend_blocked", {"service": service})
        return {
            "ok": False,
            "blocked": True,
            "message": "Restart blocked by safety. Set NDSP_ALLOW_ADMIN_RESTART=true to enable.",
            "service": service,
        }

    try:
        subprocess.check_output(["sudo", "systemctl", "restart", service], stderr=subprocess.STDOUT, text=True, timeout=30)
        _audit("restart_backend", {"service": service})
        return {"ok": True, "service": service}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/notifications/broadcast")
def notifications_broadcast(
    payload: dict[str, Any] = Body(default={}),
    _: bool = Depends(_require_admin),
):
    message = str(payload.get("message", "")).strip()

    if not message:
        raise HTTPException(status_code=400, detail="message required")

    _audit("notification_broadcast_requested", {"message": message})

    return {
        "ok": True,
        "message": "Broadcast request logged. Telegram sender connection can be attached in next phase.",
        "broadcast": message,
    }

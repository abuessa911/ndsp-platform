from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import os
import datetime
import re

app = FastAPI()
DB = os.environ.get("NDSP_AUTH_DB", "ndsp_auth")

UUID_RE = re.compile(r"^[0-9a-fA-F-]{36}$")

def run_psql(sql: str) -> str:
    cmd = ["sudo", "-u", "postgres", "psql", "-d", DB, "-Atqc", sql]
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "psql_error")
    return p.stdout.strip()

def q(s: str) -> str:
    return s.replace("'", "''")

@app.get("/health")
def health():
    return {"ok": True, "service": "ndsp-admin-user-ops", "mode": "real-delete"}

@app.post("/{user_id}")
def delete_user(user_id: str):
    user_id = (user_id or "").strip()

    if not UUID_RE.match(user_id):
        return JSONResponse({"ok": False, "error": "invalid_user_id", "user_id": user_id}, status_code=400)

    safe_id = q(user_id)

    exists = run_psql(f"select count(*) from public.users where id::text='{safe_id}';")
    if exists != "1":
        return JSONResponse({"ok": False, "error": "user_not_found", "user_id": user_id}, status_code=404)

    backup_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    sql = f"""
    create table if not exists public.users_deleted_backup_all as
      select *, now() as deleted_backup_at, ''::text as deleted_reason
      from public.users
      where false;

    insert into public.users_deleted_backup_all
      select *, now() as deleted_backup_at, 'admin_real_delete_{backup_ts}'::text as deleted_reason
      from public.users
      where id::text='{safe_id}';

    delete from public.user_alert_channels
      where user_id='{safe_id}'
         or user_email in (
           select email from public.users_deleted_backup_all where id::text='{safe_id}'
         );

    delete from public.user_2fa_settings where user_id='{safe_id}';
    delete from public.user_two_factor_settings where user_id::text='{safe_id}';

    delete from public.users where id::text='{safe_id}';

    select count(*) from public.users where id::text='{safe_id}';
    """
    remaining = run_psql(sql)
    return {"ok": remaining == "0", "action": "deleted", "user_id": user_id, "remaining": remaining}

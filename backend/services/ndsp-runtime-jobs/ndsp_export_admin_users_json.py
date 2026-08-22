#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/var/www/ndsp/admin/admin-users.json")

SQL = r"""
SELECT
  id::text,
  COALESCE(name,'') AS name,
  COALESCE(email,'') AS email,
  COALESCE(plan,'') AS plan,
  COALESCE(role,'') AS role,
  COALESCE(status,'') AS status,
  COALESCE(category,'') AS category,
  COALESCE(phone,'') AS phone,
  COALESCE(trial_ends_at::text,'') AS trial_ends_at
FROM users
ORDER BY created_at DESC NULLS LAST, email ASC;
"""

rows = []
try:
    out = subprocess.check_output(
        ["sudo", "-u", "postgres", "psql", "-d", "ndsp_auth", "-AtF", "\t", "-c", SQL],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=20,
    )
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) >= 9:
            rows.append({
                "id": p[0],
                "name": p[1],
                "email": p[2],
                "plan": p[3],
                "role": p[4],
                "status": p[5],
                "category": p[6],
                "phone": p[7],
                "trial_ends_at": p[8],
            })
    payload = {
        "ok": True,
        "count": len(rows),
        "users": rows,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
except Exception as e:
    payload = {
        "ok": False,
        "error": "EXPORT_FAILED",
        "message": str(e)[:300],
        "count": 0,
        "users": [],
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

tmp = OUT.with_suffix(".tmp")
tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
tmp.replace(OUT)

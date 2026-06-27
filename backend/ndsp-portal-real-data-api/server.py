#!/usr/bin/env python3
import json
import re
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

DB = "ndsp_auth"

def run_psql(sql: str):
    cmd = ["psql", "-d", DB, "-t", "-A", "-q", "-c", sql]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=12)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "psql failed")
    return p.stdout.strip()

def json_sql(sql: str):
    out = run_psql("COPY (" + sql + ") TO STDOUT;")
    if not out:
        return None
    return json.loads(out)

def safe_word(v, default=""):
    v = str(v or default).strip()
    if not re.match(r"^[A-Za-z0-9_\-./:@+ ]{0,80}$", v):
        return default
    return v

def table_exists_like(patterns):
    likes = " OR ".join([f"table_name ILIKE '%{p}%'" for p in patterns])
    sql = f"""
    SELECT COALESCE(json_agg(row_to_json(x)), '[]'::json)::text
    FROM (
      SELECT table_schema, table_name
      FROM information_schema.tables
      WHERE table_schema NOT IN ('pg_catalog','information_schema')
        AND table_type='BASE TABLE'
        AND ({likes})
      ORDER BY table_schema, table_name
      LIMIT 20
    ) x
    """
    return json_sql(sql) or []

def column_list(schema, table):
    sql = f"""
    SELECT COALESCE(json_agg(column_name ORDER BY ordinal_position), '[]'::json)::text
    FROM information_schema.columns
    WHERE table_schema = '{schema}' AND table_name = '{table}'
    """
    return json_sql(sql) or []

def quote_ident(v):
    return '"' + str(v).replace('"','""') + '"'

def latest_row_from_candidates(patterns, preferred_cols=None, symbol=None, timeframe=None):
    candidates = table_exists_like(patterns)
    for t in candidates:
        schema = t["table_schema"]
        table = t["table_name"]
        cols = column_list(schema, table)
        lower_cols = [c.lower() for c in cols]

        where = []
        if symbol:
            for c in cols:
                if c.lower() in ("symbol","asset","ticker","instrument","market_symbol"):
                    where.append(f"{quote_ident(c)}::text ILIKE '%{symbol}%'")
                    break

        if timeframe:
            for c in cols:
                if c.lower() in ("timeframe","frame","period","horizon","tf"):
                    where.append(f"{quote_ident(c)}::text ILIKE '%{timeframe}%'")
                    break

        order = ""
        for c in cols:
            if c.lower() in ("created_at","updated_at","timestamp","ts","date"):
                order = f" ORDER BY {quote_ident(c)} DESC"
                break

        where_sql = (" WHERE " + " AND ".join(where)) if where else ""
        sql = f"""
        SELECT row_to_json(r)::text
        FROM (
          SELECT *
          FROM {quote_ident(schema)}.{quote_ident(table)}
          {where_sql}
          {order}
          LIMIT 1
        ) r
        """
        try:
            row = json_sql(sql)
            if row:
                return {
                    "configured": True,
                    "source": f"{schema}.{table}",
                    "columns": cols,
                    "row": row
                }
        except Exception:
            continue

    return {
        "configured": False,
        "source": None,
        "columns": [],
        "row": None,
        "message": "DATA_SOURCE_NOT_CONFIGURED"
    }

def db_map():
    sql = """
    SELECT COALESCE(json_agg(row_to_json(x)), '[]'::json)::text
    FROM (
      SELECT table_schema, table_name,
             (SELECT count(*) FROM information_schema.columns c
              WHERE c.table_schema=t.table_schema AND c.table_name=t.table_name) AS columns_count
      FROM information_schema.tables t
      WHERE table_schema NOT IN ('pg_catalog','information_schema')
        AND table_type='BASE TABLE'
      ORDER BY table_schema, table_name
    ) x
    """
    return json_sql(sql) or []

def users_summary():
    sql = """
    SELECT row_to_json(x)::text
    FROM (
      SELECT
        (SELECT count(*) FROM users) AS users_count,
        (SELECT count(*) FROM users WHERE upper(status)='ACTIVE') AS active_users,
        (SELECT count(*) FROM access_guard_sessions) AS sessions_count
    ) x
    """
    return json_sql(sql) or {}

class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        path = parsed.path

        try:
            if path in ("/health", "/api/portal/health"):
                run_psql("SELECT 1;")
                return self.send_json({"ok": True, "service": "ndsp-portal-real-data-api", "database": "ok", "fake_data": False})

            if path == "/api/portal/db-map":
                return self.send_json({"ok": True, "tables": db_map(), "fake_data": False})

            if path == "/api/portal/user-summary":
                return self.send_json({"ok": True, "summary": users_summary(), "fake_data": False})

            if path == "/api/portal/asset-view":
                symbol = safe_word((qs.get("symbol") or ["XAU"])[0], "XAU")
                timeframe = safe_word((qs.get("timeframe") or ["weekly"])[0], "weekly")
                row = latest_row_from_candidates(
                    ["asset", "market", "reading", "signal", "decision", "level"],
                    symbol=symbol,
                    timeframe=timeframe
                )
                return self.send_json({"ok": True, "page": "asset-view", "symbol": symbol, "timeframe": timeframe, "data": row, "fake_data": False})

            if path == "/api/portal/daily-brief":
                row = latest_row_from_candidates(["brief", "daily", "reading", "decision", "signal"])
                return self.send_json({"ok": True, "page": "daily-brief", "data": row, "fake_data": False})

            if path == "/api/portal/command-center":
                row = latest_row_from_candidates(["command", "decision", "signal", "reading"])
                return self.send_json({"ok": True, "page": "command-center", "data": row, "fake_data": False})

            if path == "/api/portal/settings":
                row = latest_row_from_candidates(["setting", "alert", "preference"])
                return self.send_json({"ok": True, "page": "settings", "data": row, "fake_data": False})

            if path == "/api/portal/account":
                return self.send_json({"ok": True, "page": "account", "summary": users_summary(), "fake_data": False})

            return self.send_json({"ok": False, "error": "NOT_FOUND"}, 404)

        except Exception as e:
            return self.send_json({"ok": False, "error": "REAL_DATA_API_ERROR", "detail": str(e), "fake_data": False}, 500)

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 9047), Handler)
    server.serve_forever()

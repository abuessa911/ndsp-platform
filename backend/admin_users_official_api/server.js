'use strict';

const http = require('http');
const crypto = require('crypto');
const { execFile } = require('child_process');

const HOST = process.env.HOST || '127.0.0.1';
const PORT = Number(process.env.PORT || 9031);
const DB_NAME = process.env.PGDATABASE || process.env.POSTGRES_DB || 'ndsp_auth';
const ADMIN_KEY = String(process.env.NDSP_ADMIN_ACTION_KEY || '').trim();

function send(res, code, obj) {
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff'
  });
  res.end(JSON.stringify(obj));
}

function safeEqual(a, b) {
  const aa = Buffer.from(String(a || ''));
  const bb = Buffer.from(String(b || ''));
  if (!aa.length || !bb.length || aa.length !== bb.length) return false;
  return crypto.timingSafeEqual(aa, bb);
}

function authorized(req) {
  return Boolean(ADMIN_KEY) && safeEqual(req.headers['x-ndsp-admin-key'] || '', ADMIN_KEY);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => {
      data += chunk;
      if (data.length > 1024 * 128) {
        reject(new Error('BODY_TOO_LARGE'));
        req.destroy();
      }
    });
    req.on('end', () => {
      if (!data) return resolve({});
      try { resolve(JSON.parse(data)); }
      catch { reject(new Error('INVALID_JSON')); }
    });
  });
}

function q(s) {
  return "'" + String(s ?? '').replace(/'/g, "''") + "'";
}

function runSql(sql) {
  return new Promise((resolve, reject) => {
    const databaseUrl =
      process.env.DATABASE_URL ||
      process.env.NDSP_DATABASE_URL ||
      process.env.POSTGRES_URL ||
      process.env.DB_URL ||
      '';

    let cmd;
    let args;

    if (databaseUrl) {
      cmd = 'psql';
      args = [databaseUrl, '-X', '-q', '-A', '-t', '-v', 'ON_ERROR_STOP=1', '-c', sql];
    } else {
      cmd = 'sudo';
      args = ['-u', 'postgres', 'psql', '-d', DB_NAME, '-X', '-q', '-A', '-t', '-v', 'ON_ERROR_STOP=1', '-c', sql];
    }

    execFile(cmd, args, { timeout: 20000, maxBuffer: 1024 * 1024 * 10 }, (err, stdout, stderr) => {
      if (err) {
        err.stderr = stderr;
        return reject(err);
      }
      resolve(String(stdout || '').trim());
    });
  });
}

async function listUsers(limit) {
  const safeLimit = Math.max(1, Math.min(Number(limit || 100), 300));

  const sql = `
WITH base AS (
  SELECT to_jsonb(u) AS j
  FROM public.users u
  ORDER BY
    CASE
      WHEN to_jsonb(u) ? 'created_at'
      THEN (to_jsonb(u)->>'created_at')::timestamptz
      ELSE NOW()
    END DESC
  LIMIT ${safeLimit}
)
SELECT COALESCE(json_agg(jsonb_strip_nulls(jsonb_build_object(
  'id', j->>'id',
  'email', j->>'email',
  'phone', j->>'phone',
  'name', COALESCE(j->>'name', j->>'full_name', j->>'display_name'),
  'role', COALESCE(j->>'role', j->>'user_role', j->>'account_role'),
  'status', j->>'status',
  'plan', COALESCE(j->>'plan', j->>'package', j->>'subscription_plan'),
  'trial_status', COALESCE(j->>'trial_status', j->>'review_status'),
  'created_at', j->>'created_at',
  'updated_at', j->>'updated_at'
))), '[]'::json)
FROM base;`;

  const out = await runSql(sql);
  return JSON.parse(out || '[]');
}

async function dumpUsersBeforeAction() {
  return new Promise((resolve) => {
    const stamp = new Date().toISOString().replace(/[-:TZ.]/g, '').slice(0, 14);
    const dir = `/home/nawaf511/ndsp_backups/admin_user_action_${stamp}`;
    const file = `${dir}/public_users_before_action.sql`;

    execFile('mkdir', ['-p', dir], () => {
      const databaseUrl =
        process.env.DATABASE_URL ||
        process.env.NDSP_DATABASE_URL ||
        process.env.POSTGRES_URL ||
        process.env.DB_URL ||
        '';

      let cmd;
      let args;

      if (databaseUrl) {
        cmd = 'pg_dump';
        args = [databaseUrl, '-t', 'public.users', '-f', file];
      } else {
        cmd = 'sudo';
        args = ['-u', 'postgres', 'pg_dump', '-d', DB_NAME, '-t', 'public.users', '-f', file];
      }

      execFile(cmd, args, { timeout: process.env.PORT || process.env.PORT || 30000, maxBuffer: 1024 * 1024 }, (err) => {
        resolve({ ok: !err, file, error: err ? String(err.message || err) : null });
      });
    });
  });
}

async function applyAction(action, targetId) {
  const allowed = {
    activate: 'ACTIVE',
    suspend: 'SUSPENDED',
    pending_review: 'PENDING_REVIEW'
  };

  const newStatus = allowed[action];

  if (!newStatus) {
    const e = new Error('UNSUPPORTED_ACTION');
    e.status = 400;
    throw e;
  }

  if (!targetId || !/^[0-9a-f-]{20,80}$/i.test(String(targetId))) {
    const e = new Error('INVALID_USER_ID');
    e.status = 400;
    throw e;
  }

  const backup = await dumpUsersBeforeAction();
  if (!backup.ok) {
    const e = new Error('BACKUP_BEFORE_ACTION_FAILED');
    e.status = 500;
    e.detail = backup.error;
    throw e;
  }

  const actorHint = ADMIN_KEY ? `${ADMIN_KEY.slice(0, 4)}***${ADMIN_KEY.slice(-4)}` : 'missing';

  const sql = `
DO $do$
DECLARE
  target_text text := ${q(targetId)};
  requested_action text := ${q(action)};
  new_status text := ${q(newStatus)};
  actor_hint text := ${q(actorHint)};
  before_data jsonb;
  after_data jsonb;
  id_column_type text;
  has_status boolean;
  has_updated_at boolean;
BEGIN
  SELECT data_type INTO id_column_type
  FROM information_schema.columns
  WHERE table_schema='public' AND table_name='users' AND column_name='id'
  LIMIT 1;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='public' AND table_name='users' AND column_name='status'
  ) INTO has_status;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_schema='public' AND table_name='users' AND column_name='updated_at'
  ) INTO has_updated_at;

  IF NOT has_status THEN
    RAISE EXCEPTION 'STATUS_COLUMN_MISSING';
  END IF;

  EXECUTE 'SELECT to_jsonb(u) FROM public.users u WHERE u.id::text=$1 LIMIT 1'
  INTO before_data
  USING target_text;

  IF before_data IS NULL THEN
    RAISE EXCEPTION 'USER_NOT_FOUND';
  END IF;

  CREATE TABLE IF NOT EXISTS public.ndsp_admin_user_action_audit (
    id bigserial PRIMARY KEY,
    actor_hint text NOT NULL,
    action text NOT NULL,
    target_user_id text NOT NULL,
    before_data jsonb,
    after_data jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
  );

  IF has_updated_at THEN
    EXECUTE 'UPDATE public.users SET status=$1, updated_at=NOW() WHERE id::text=$2'
    USING new_status, target_text;
  ELSE
    EXECUTE 'UPDATE public.users SET status=$1 WHERE id::text=$2'
    USING new_status, target_text;
  END IF;

  EXECUTE 'SELECT to_jsonb(u) FROM public.users u WHERE u.id::text=$1 LIMIT 1'
  INTO after_data
  USING target_text;

  INSERT INTO public.ndsp_admin_user_action_audit(actor_hint, action, target_user_id, before_data, after_data)
  VALUES(actor_hint, requested_action, target_text, before_data, after_data);
END
$do$;

SELECT json_build_object(
  'ok', true,
  'target_id', ${q(targetId)},
  'action', ${q(action)},
  'new_status', ${q(newStatus)},
  'backup_file', ${q(backup.file)}
);
`;

  const out = await runSql(sql);
  return JSON.parse(out || '{"ok":true}');
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);

    if (req.method === 'OPTIONS') {
      res.writeHead(204, {
        'Access-Control-Allow-Headers': 'Content-Type, X-NDSP-ADMIN-KEY',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
      });
      return res.end();
    }

    if (url.pathname === '/health') {
      return send(res, 200, {
        ok: true,
        service: 'ndsp-admin-users-official',
        db: DB_NAME,
        host: HOST,
        port: PORT,
        protected: true,
        admin_key_configured: Boolean(ADMIN_KEY)
      });
    }

    if (url.pathname === '/api/admin/users/official' && req.method === 'GET') {
      if (!authorized(req)) return send(res, 401, { ok: false, error: 'UNAUTHORIZED' });
      const users = await listUsers(url.searchParams.get('limit') || 100);
      return send(res, 200, {
        ok: true,
        source: 'PostgreSQL / ndsp_auth / public.users',
        users
      });
    }

    if (url.pathname === '/api/admin/users/action' && req.method === 'POST') {
      if (!authorized(req)) return send(res, 401, { ok: false, error: 'UNAUTHORIZED' });
      const body = await readBody(req);
      const result = await applyAction(body.action, body.user_id || body.target_id || body.id);
      return send(res, 200, result);
    }

    return send(res, 404, { ok: false, error: 'NOT_FOUND', path: url.pathname });
  } catch (err) {
    return send(res, err.status || 500, {
      ok: false,
      error: String(err.message || err),
      detail: err.detail || err.stderr || undefined
    });
  }
});

server.on('error', (err) => {
  console.error('SERVER_LISTEN_ERROR', err);
  process.exit(1);
});

server.listen(PORT, HOST, () => {
  console.log(`ndsp-admin-users-official listening on ${HOST}:${PORT}`);
});

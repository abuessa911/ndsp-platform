'use strict';

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const { Pool } = require('pg');

const PORT = Number(process.env.NDSP_ADMIN_ACTIONS_PORT || 9017);
const ADMIN_JSON_PATH = process.env.NDSP_ADMIN_USERS_JSON || '/var/www/ndsp-admin/admin-users.json';

function safeEq(a, b) {
  a = String(a || '');
  b = String(b || '');
  const aa = Buffer.from(a);
  const bb = Buffer.from(b);
  if (aa.length !== bb.length) return false;
  return crypto.timingSafeEqual(aa, bb);
}

function send(res, code, obj) {
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(JSON.stringify(obj));
}

function qident(x) {
  return '"' + String(x).replace(/"/g, '""') + '"';
}

function parseCookies(req) {
  const out = {};
  String(req.headers.cookie || '').split(';').forEach(part => {
    const i = part.indexOf('=');
    if (i > -1) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  });
  return out;
}

function b64urlDecode(v) {
  v = String(v || '').replace(/-/g, '+').replace(/_/g, '/');
  while (v.length % 4) v += '=';
  return Buffer.from(v, 'base64').toString('utf8');
}

function verifyJwtHS256(token, secrets) {
  try {
    const parts = String(token || '').split('.');
    if (parts.length !== 3) return null;
    const [h, p, s] = parts;
    const header = JSON.parse(b64urlDecode(h));
    if (header.alg !== 'HS256') return null;

    for (const secret of secrets.filter(Boolean)) {
      const expected = crypto.createHmac('sha256', secret).update(`${h}.${p}`).digest('base64url');
      if (safeEq(expected, s)) {
        const payload = JSON.parse(b64urlDecode(p));
        if (payload.exp && Date.now() >= Number(payload.exp) * 1000) return null;
        return payload;
      }
    }
  } catch (_) {}
  return null;
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', chunk => {
      raw += chunk;
      if (raw.length > 1024 * 1024) {
        reject(new Error('BODY_TOO_LARGE'));
        req.destroy();
      }
    });
    req.on('end', () => {
      if (!raw.trim()) return resolve({});
      try { resolve(JSON.parse(raw)); }
      catch (_) { reject(new Error('INVALID_JSON')); }
    });
    req.on('error', reject);
  });
}

async function columns(client, table) {
  const r = await client.query(
    `SELECT column_name
     FROM information_schema.columns
     WHERE table_schema='public' AND table_name=$1`,
    [table]
  );
  return new Set(r.rows.map(x => x.column_name));
}

async function tableExists(client, table) {
  const r = await client.query(
    `SELECT 1 FROM information_schema.tables
     WHERE table_schema='public' AND table_name=$1
     LIMIT 1`,
    [table]
  );
  return r.rowCount > 0;
}

function normalizeStatus(row) {
  if (row.status !== undefined && row.status !== null && String(row.status).trim() !== '') {
    const s = String(row.status).trim().toLowerCase();
    if (['active', 'activated', 'enabled', 'true'].includes(s)) return 'active';
    if (['inactive', 'disabled', 'deactivated', 'false', 'suspended'].includes(s)) return 'inactive';
    return s;
  }

  if (row.is_active !== undefined && row.is_active !== null) {
    return row.is_active ? 'active' : 'inactive';
  }

  return 'unknown';
}

function pickSql(cols, candidates, fallbackSql, alias) {
  for (const c of candidates) {
    if (cols.has(c)) return `${qident(c)} AS ${qident(alias)}`;
  }
  return `${fallbackSql} AS ${qident(alias)}`;
}

async function syncAdminUsersJson(client) {
  const ucols = await columns(client, 'users');

  const select = [
    pickSql(ucols, ['id'], `''`, 'id'),
    pickSql(ucols, ['name', 'full_name', 'display_name'], `COALESCE(NULLIF(email,''),'User')`, 'name'),
    pickSql(ucols, ['email'], `''`, 'email'),
    pickSql(ucols, ['plan', 'subscription_plan', 'package', 'tier'], `'Free'`, 'plan'),
    pickSql(ucols, ['role', 'user_role'], `'user'`, 'role'),
    pickSql(ucols, ['status'], `NULL`, 'status'),
    pickSql(ucols, ['is_active', 'active'], `NULL`, 'is_active'),
    pickSql(ucols, ['category', 'trial_category', 'user_category'], `NULL`, 'category'),
    pickSql(ucols, ['created_at', 'created'], `NULL`, 'created_at'),
    pickSql(ucols, ['updated_at', 'updated'], `NULL`, 'updated_at')
  ];

  let orderBy = `id::text DESC`;
  if (ucols.has('updated_at') && ucols.has('created_at')) {
    orderBy = `COALESCE(${qident('updated_at')}, ${qident('created_at')}) DESC`;
  } else if (ucols.has('updated_at')) {
    orderBy = `${qident('updated_at')} DESC`;
  } else if (ucols.has('created_at')) {
    orderBy = `${qident('created_at')} DESC`;
  }

  const r = await client.query(`
    SELECT ${select.join(', ')}
    FROM users
    ORDER BY ${orderBy}
    LIMIT 500
  `);

  const users = r.rows.map(row => ({
    id: String(row.id || ''),
    name: String(row.name || row.email || 'User'),
    email: String(row.email || ''),
    plan: String(row.plan || 'Free'),
    role: String(row.role || 'user'),
    status: normalizeStatus(row),
    category: row.category === null || row.category === undefined ? '' : String(row.category),
    created_at: row.created_at,
    updated_at: row.updated_at
  }));

  const payload = {
    ok: true,
    source: 'postgresql_ndsp_auth',
    generated_at: new Date().toISOString(),
    count: users.length,
    users
  };

  fs.writeFileSync(ADMIN_JSON_PATH, JSON.stringify(payload, null, 2), { mode: 0o644 });
  return { path: ADMIN_JSON_PATH, count: users.length };
}

async function deleteDeps(client, userId) {
  const fk = await client.query(`
    SELECT kcu.table_name, kcu.column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON tc.constraint_name = kcu.constraint_name
     AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage ccu
      ON ccu.constraint_name = tc.constraint_name
     AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type='FOREIGN KEY'
      AND tc.table_schema='public'
      AND ccu.table_name='users'
      AND ccu.column_name='id'
  `);

  for (const row of fk.rows) {
    if (row.table_name === 'users') continue;
    await client.query(
      `DELETE FROM ${qident(row.table_name)} WHERE ${qident(row.column_name)}::text=$1`,
      [userId]
    );
  }

  const known = [
    'notifications',
    'plan_upgrade_requests',
    'feedback_surveys',
    'trial_feedback_surveys',
    'trial_registrations',
    'user_sessions',
    'sessions',
    'payments',
    'subscriptions',
    'nowpayments_payments',
    'audit_logs'
  ];

  for (const table of known) {
    if (await tableExists(client, table)) {
      const cols = await columns(client, table);
      if (cols.has('user_id')) {
        await client.query(`DELETE FROM ${qident(table)} WHERE ${qident('user_id')}::text=$1`, [userId]);
      }
    }
  }
}

async function adminFromDbRole(client, uid) {
  if (!uid) return false;
  const cols = await columns(client, 'users');
  const checks = [];
  if (cols.has('role')) checks.push(`LOWER(COALESCE(role,'')) IN ('admin','super_admin','owner')`);
  if (cols.has('is_admin')) checks.push(`is_admin = true`);
  if (cols.has('admin')) checks.push(`admin = true`);
  if (!checks.length) return false;

  const r = await client.query(
    `SELECT id FROM users WHERE id::text=$1 AND (${checks.join(' OR ')}) LIMIT 1`,
    [String(uid)]
  );
  return r.rowCount > 0;
}

async function authorize(req, pool) {
  const expected = String(process.env.NDSP_ADMIN_ACTION_KEY || '');
  const provided = String(req.headers['x-ndsp-admin-key'] || '');

  if (expected && provided && safeEq(expected, provided)) {
    return { ok: true, via: 'server_side_action_key' };
  }

  const c = parseCookies(req);
  const tokens = Object.values(c).map(String).filter(v => v.length >= 12);
  const auth = String(req.headers.authorization || '');
  if (/^Bearer\s+/i.test(auth)) tokens.unshift(auth.replace(/^Bearer\s+/i, '').trim());

  const secrets = [
    process.env.JWT_SECRET,
    process.env.NDSP_JWT_SECRET,
    process.env.AUTH_JWT_SECRET,
    process.env.SESSION_SECRET,
    process.env.NDSP_SESSION_SECRET
  ].filter(Boolean);

  if (!tokens.length || !secrets.length) {
    return { ok: false, reason: 'ADMIN_AUTH_REQUIRED' };
  }

  const client = await pool.connect();
  try {
    for (const token of tokens) {
      const payload = verifyJwtHS256(token, secrets);
      if (!payload) continue;

      const role = String(payload.role || payload.user_role || '').toLowerCase();
      const uid = payload.id || payload.user_id || payload.sub || null;

      if (['admin','super_admin','owner'].includes(role)) {
        return { ok: true, via: 'jwt_admin_role' };
      }

      if (uid && await adminFromDbRole(client, uid)) {
        return { ok: true, via: 'jwt_db_admin_role' };
      }
    }
  } finally {
    client.release();
  }

  return { ok: false, reason: 'ADMIN_AUTH_REQUIRED' };
}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL || undefined,
  host: process.env.PGHOST || process.env.DB_HOST || undefined,
  port: process.env.PGPORT ? Number(process.env.PGPORT) : (process.env.DB_PORT ? Number(process.env.DB_PORT) : undefined),
  database: process.env.PGDATABASE || process.env.DB_NAME || process.env.POSTGRES_DB || 'ndsp_auth',
  user: process.env.PGUSER || process.env.DB_USER || process.env.POSTGRES_USER || undefined,
  password: process.env.PGPASSWORD || process.env.DB_PASSWORD || process.env.POSTGRES_PASSWORD || undefined
});

const server = http.createServer(async (req, res) => {
  try {
    const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);

    if (req.method === 'GET' && u.pathname === '/api/admin-actions/users/action/health') {
      return send(res, 200, {
        ok: true,
        service: 'ndsp-admin-actions-gateway',
        endpoint: '/api/admin-actions/users/action',
        sync_endpoint: '/api/admin-actions/users/sync-json',
        api_namespace: '/api',
        php: false,
        key_env_configured: Boolean(process.env.NDSP_ADMIN_ACTION_KEY),
        json_sync: ADMIN_JSON_PATH,
        schema_safe: true,
        database: 'PostgreSQL'
      });
    }

    if (req.method === 'POST' && u.pathname === '/api/admin-actions/users/sync-json') {
      const auth = await authorize(req, pool);
      if (!auth.ok) return send(res, 401, { ok: false, error: 'ADMIN_AUTH_REQUIRED' });

      const client = await pool.connect();
      try {
        const synced = await syncAdminUsersJson(client);
        return send(res, 200, { ok: true, synced });
      } finally {
        client.release();
      }
    }

    if (req.method !== 'POST' || u.pathname !== '/api/admin-actions/users/action') {
      return send(res, 404, { ok: false, error: 'NOT_FOUND', path: u.pathname });
    }

    const auth = await authorize(req, pool);
    if (!auth.ok) return send(res, 401, { ok: false, error: 'ADMIN_AUTH_REQUIRED' });

    const body = await readJson(req);
    const action = String(body.action || body.type || '').trim().toLowerCase();
    const userId = String(body.user_id || body.id || '').trim();

    if (!['activate', 'deactivate', 'delete'].includes(action)) {
      return send(res, 400, { ok: false, error: 'INVALID_ACTION' });
    }

    if (!userId || userId === 'PUT_USER_ID_HERE') {
      return send(res, 400, { ok: false, error: 'USER_ID_REQUIRED' });
    }

    const client = await pool.connect();

    try {
      await client.query('BEGIN');

      const exists = await client.query(`SELECT id FROM users WHERE id::text=$1 LIMIT 1`, [userId]);
      if (!exists.rowCount) {
        await client.query('ROLLBACK');
        return send(res, 404, { ok: false, error: 'USER_NOT_FOUND' });
      }

      const ucols = await columns(client, 'users');

      if (action === 'activate' || action === 'deactivate') {
        const active = action === 'activate';
        const sets = [];
        const vals = [];
        let i = 1;

        if (ucols.has('status')) {
          sets.push(`status=$${i++}`);
          vals.push(active ? 'active' : 'inactive');
        }

        if (ucols.has('is_active')) {
          sets.push(`is_active=$${i++}`);
          vals.push(active);
        }

        if (active && ucols.has('activated_at')) sets.push(`activated_at=COALESCE(activated_at, NOW())`);
        if (!active && ucols.has('deactivated_at')) sets.push(`deactivated_at=NOW()`);
        if (ucols.has('updated_at')) sets.push(`updated_at=NOW()`);

        if (!sets.length) {
          await client.query('ROLLBACK');
          return send(res, 500, { ok: false, error: 'NO_USER_STATUS_COLUMNS' });
        }

        vals.push(userId);

        const retStatus = ucols.has('status') ? 'status' : 'NULL AS status';
        const retActive = ucols.has('is_active') ? 'is_active' : 'NULL AS is_active';

        const update = await client.query(
          `UPDATE users SET ${sets.join(', ')} WHERE id::text=$${i} RETURNING id::text AS id, ${retStatus}, ${retActive}`,
          vals
        );

        if (update.rowCount !== 1) {
          await client.query('ROLLBACK');
          return send(res, 409, { ok: false, error: 'NO_ROW_UPDATED' });
        }

        const synced = await syncAdminUsersJson(client);
        await client.query('COMMIT');

        return send(res, 200, {
          ok: true,
          action,
          user_id: userId,
          updated_rows: update.rowCount,
          db_status: normalizeStatus(update.rows[0]),
          json_synced: true,
          synced
        });
      }

      await deleteDeps(client, userId);
      const del = await client.query(`DELETE FROM users WHERE id::text=$1 RETURNING id::text AS id`, [userId]);

      if (del.rowCount !== 1) {
        await client.query('ROLLBACK');
        return send(res, 409, { ok: false, error: 'NO_ROW_DELETED' });
      }

      const synced = await syncAdminUsersJson(client);
      await client.query('COMMIT');

      return send(res, 200, {
        ok: true,
        action: 'delete',
        user_id: userId,
        deleted_rows: del.rowCount,
        json_synced: true,
        synced
      });

    } catch (e) {
      try { await client.query('ROLLBACK'); } catch (_) {}
      return send(res, 500, {
        ok: false,
        error: 'ADMIN_ACTION_FAILED',
        detail: String(e && e.message ? e.message : e)
      });
    } finally {
      client.release();
    }

  } catch (e) {
    return send(res, 500, {
      ok: false,
      error: 'GATEWAY_EXCEPTION',
      detail: String(e && e.message ? e.message : e)
    });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] admin actions gateway listening on 127.0.0.1:${PORT}`);
});

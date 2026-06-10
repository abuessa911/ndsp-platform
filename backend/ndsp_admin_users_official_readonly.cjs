'use strict';

const http = require('http');
const { URL } = require('url');
const fs = require('fs');

function loadEnvFile(file) {
  try {
    if (!fs.existsSync(file)) return;
    const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
    for (const raw of lines) {
      const line = raw.trim();
      if (!line || line.startsWith('#')) continue;
      const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
      if (!m) continue;
      const key = m[1];
      let val = m[2].trim();
      if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
        val = val.slice(1, -1);
      }
      if (!process.env[key]) process.env[key] = val;
    }
  } catch (_) {}
}

[
  '/etc/ndsp/ndsp-db.env',
  '/home/nawaf511/empire-core-new/backend/.env',
  '/home/nawaf511/empire-core-new/backend/auth_api/.env'
].forEach(loadEnvFile);

let pg;
try {
  pg = require('pg');
} catch (e) {
  console.error('[NDSP_ADMIN_USERS_OFFICIAL] pg module missing:', e.message);
  process.exit(1);
}

const PORT = Number(process.env.NDSP_ADMIN_USERS_OFFICIAL_PORT || '9024');

function getConnectionConfig() {
  const url =
    process.env.DATABASE_URL ||
    process.env.NDSP_DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.PG_URI ||
    process.env.PGURL;

  if (url) {
    return {
      connectionString: url,
      ssl: false
    };
  }

  return {
    host: process.env.PGHOST || process.env.POSTGRES_HOST || '127.0.0.1',
    port: Number(process.env.PGPORT || process.env.POSTGRES_PORT || '5432'),
    database: process.env.PGDATABASE || process.env.POSTGRES_DB || 'ndsp_auth',
    user: process.env.PGUSER || process.env.POSTGRES_USER || 'ndsp_auth',
    password: process.env.PGPASSWORD || process.env.POSTGRES_PASSWORD || process.env.DB_PASSWORD || undefined,
    ssl: false
  };
}

const pool = new pg.Pool({
  ...getConnectionConfig(),
  max: 5,
  idleTimeoutMillis: 15000,
  connectionTimeoutMillis: 5000
});

function send(res, code, body) {
  const text = JSON.stringify(body);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
    'Pragma': 'no-cache',
    'X-NDSP-Source': 'official-db-readonly'
  });
  res.end(text);
}

function maskEmail(email) {
  if (!email || typeof email !== 'string' || !email.includes('@')) return '';
  const [a, b] = email.split('@');
  return `${a.slice(0, 3)}***@${b}`;
}

async function getColumns(tableName) {
  const q = `
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name=$1
  `;
  const r = await pool.query(q, [tableName]);
  return new Set(r.rows.map(x => x.column_name));
}

function sqlField(cols, name, alias) {
  if (cols.has(name)) return `"${name}" AS "${alias || name}"`;
  return `NULL::text AS "${alias || name}"`;
}

async function listUsers() {
  const cols = await getColumns('users');

  if (!cols.has('id')) {
    return { ok: false, error: 'USERS_TABLE_ID_COLUMN_MISSING' };
  }

  const selectFields = [
    'id',
    sqlField(cols, 'name', 'name'),
    sqlField(cols, 'email', 'email'),
    sqlField(cols, 'phone', 'phone'),
    sqlField(cols, 'role', 'role'),
    sqlField(cols, 'status', 'status'),
    sqlField(cols, 'plan', 'plan'),
    cols.has('created_at') ? 'created_at' : 'NULL::timestamptz AS created_at',
    cols.has('updated_at') ? 'updated_at' : 'NULL::timestamptz AS updated_at',
    cols.has('last_login_at') ? 'last_login_at' : 'NULL::timestamptz AS last_login_at'
  ].join(', ');

  const orderBy = cols.has('created_at') ? 'created_at DESC NULLS LAST' : 'id DESC';

  const r = await pool.query(`
    SELECT ${selectFields}
    FROM public.users
    ORDER BY ${orderBy}
    LIMIT 200
  `);

  const users = r.rows.map(u => ({
    id: u.id,
    name: u.name || '',
    masked_email: maskEmail(u.email || ''),
    email_present: !!u.email,
    phone_present: !!u.phone,
    role: u.role || '',
    status: u.status || '',
    plan: u.plan || '',
    created_at: u.created_at,
    updated_at: u.updated_at,
    last_login_at: u.last_login_at
  }));

  const counts = {
    total: users.length,
    active: users.filter(u => String(u.status).toUpperCase() === 'ACTIVE' || String(u.status).toLowerCase() === 'active').length,
    admin_or_owner: users.filter(u => /admin|owner/i.test(String(u.role))).length
  };

  return {
    ok: true,
    source: 'public.users',
    mode: 'readonly_masked',
    counts,
    users
  };
}

async function handler(req, res) {
  try {
    const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);

    if (req.method === 'GET' && (u.pathname === '/' || u.pathname === '/health')) {
      return send(res, 200, {
        ok: true,
        service: 'ndsp-admin-users-official-readonly',
        source: 'public.users',
        readonly: true
      });
    }

    if (req.method === 'GET' && u.pathname === '/users') {
      const data = await listUsers();
      return send(res, data.ok ? 200 : 500, data);
    }

    return send(res, 404, { ok: false, error: 'NOT_FOUND', path: u.pathname });
  } catch (e) {
    return send(res, 500, { ok: false, error: 'SERVICE_EXCEPTION', detail: e.message });
  }
}

const server = http.createServer(handler);
server.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP_ADMIN_USERS_OFFICIAL] listening on 127.0.0.1:${PORT}`);
});

process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});

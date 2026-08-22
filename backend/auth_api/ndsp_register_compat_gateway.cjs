'use strict';

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');

function loadEnv(file) {
  try {
    if (!fs.existsSync(file)) return;
    const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
    for (const line of lines) {
      const s = line.trim();
      if (!s || s.startsWith('#') || !s.includes('=')) continue;
      const idx = s.indexOf('=');
      const k = s.slice(0, idx).trim();
      let v = s.slice(idx + 1).trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
      if (!process.env[k]) process.env[k] = v;
    }
  } catch (e) {}
}

loadEnv('/etc/ndsp/ndsp-db.env');
loadEnv('/etc/ndsp/ndsp-session.env');
loadEnv('/home/nawaf511/.config/ndsp/auth_api.env');

const PORT = Number(process.env.NDSP_REGISTER_COMPAT_PORT || 9028);

let Pool;
try {
  Pool = require('pg').Pool;
} catch (e) {
  console.error('MISSING_NODE_MODULE_PG', e.message);
  process.exit(1);
}

let bcrypt = null;
try { bcrypt = require('bcryptjs'); } catch (e) {}
if (!bcrypt) {
  try { bcrypt = require('bcrypt'); } catch (e) {}
}
if (!bcrypt) {
  console.error('MISSING_BCRYPT_MODULE');
  process.exit(1);
}

const pool = new Pool(process.env.DATABASE_URL ? {
  connectionString: process.env.DATABASE_URL,
  ssl: String(process.env.DATABASE_URL).includes('sslmode=require') ? { rejectUnauthorized: false } : undefined
} : {
  host: process.env.PGHOST || process.env.POSTGRES_HOST || '127.0.0.1',
  port: Number(process.env.PGPORT || process.env.POSTGRES_PORT || 5432),
  database: process.env.PGDATABASE || process.env.POSTGRES_DB || process.env.DB_NAME || 'postgres',
  user: process.env.PGUSER || process.env.POSTGRES_USER || process.env.DB_USER || 'postgres',
  password: process.env.PGPASSWORD || process.env.POSTGRES_PASSWORD || process.env.DB_PASSWORD || ''
});

function send(res, status, obj, headers = {}) {
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'POST, OPTIONS, GET',
    'access-control-allow-headers': 'Content-Type, Authorization',
    ...headers
  });
  res.end(body);
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', c => {
      body += c;
      if (body.length > 1024 * 1024) {
        reject(new Error('BODY_TOO_LARGE'));
        req.destroy();
      }
    });
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch (e) { reject(new Error('INVALID_JSON')); }
    });
    req.on('error', reject);
  });
}

function normEmail(v) {
  return String(v || '').trim().toLowerCase();
}

function digits(v) {
  return String(v || '').replace(/\D+/g, '');
}

function publicUser(row) {
  if (!row) return null;
  return {
    id: row.id,
    email: row.email,
    status: row.status || 'ACTIVE',
    role: row.role || 'USER',
    plan: row.plan || row.package || 'Trial',
    is_admin: row.is_admin === true
  };
}

let cachedColumns = null;
async function getUserColumns() {
  if (cachedColumns) return cachedColumns;
  const q = `
    select column_name, is_nullable, column_default, data_type
    from information_schema.columns
    where table_schema = 'public' and table_name = 'users'
    order by ordinal_position
  `;
  const r = await pool.query(q);
  cachedColumns = new Map();
  for (const row of r.rows) cachedColumns.set(row.column_name, row);
  return cachedColumns;
}

function has(cols, name) { return cols.has(name); }

async function duplicateCheck(client, cols, email, phoneDigits) {
  const where = [];
  const vals = [];
  if (has(cols, 'email')) {
    vals.push(email);
    where.push(`lower(email)=lower($${vals.length})`);
  }
  if (phoneDigits) {
    if (has(cols, 'phone_digits')) {
      vals.push(phoneDigits);
      where.push(`phone_digits=$${vals.length}`);
    }
    if (has(cols, 'phone')) {
      vals.push(phoneDigits);
      where.push(`regexp_replace(coalesce(phone,''), '\\D', '', 'g')=$${vals.length}`);
    }
  }
  if (!where.length) return null;
  const r = await client.query(`select * from users where ${where.join(' or ')} limit 1`, vals);
  return r.rows[0] || null;
}

function put(obj, cols, col, val) {
  if (has(cols, col) && val !== undefined) obj[col] = val;
}

async function createUser(payload) {
  const email = normEmail(payload.email);
  const name = String(payload.name || payload.full_name || payload.username || '').trim();
  const phoneRaw = String(payload.phone || payload.mobile || '').trim();
  const phoneDigits = digits(phoneRaw);
  const password = String(payload.password || payload.new_password || '');
  const confirm = String(payload.password_confirm || payload.confirm_password || password);

  if (!email || !email.includes('@')) return { status: 400, body: { ok:false, error:'EMAIL_REQUIRED', message:'أدخل بريدًا إلكترونيًا صحيحًا.' } };
  if (!phoneDigits || phoneDigits.length < 8) return { status: 400, body: { ok:false, error:'PHONE_REQUIRED', message:'أدخل رقم جوال صحيحًا.' } };
  if (!password || password.length < 8) return { status: 400, body: { ok:false, error:'PASSWORD_TOO_SHORT', message:'كلمة المرور يجب ألا تقل عن 8 خانات.' } };
  if (password !== confirm) return { status: 400, body: { ok:false, error:'PASSWORD_CONFIRM_MISMATCH', message:'كلمة المرور وتأكيد كلمة المرور غير متطابقين.' } };

  const client = await pool.connect();
  try {
    const cols = await getUserColumns();
    if (!cols.size) return { status: 500, body: { ok:false, error:'USERS_TABLE_NOT_FOUND', message:'جدول المستخدمين غير متاح.' } };

    await client.query('begin');

    const dup = await duplicateCheck(client, cols, email, phoneDigits);
    if (dup) {
      await client.query('rollback');
      const sameEmail = String(dup.email || '').toLowerCase() === email;
      return {
        status: 409,
        body: {
          ok:false,
          error: sameEmail ? 'EMAIL_ALREADY_EXISTS' : 'PHONE_ALREADY_EXISTS',
          message: sameEmail ? 'البريد الإلكتروني مسجل مسبقًا.' : 'رقم الجوال مسجل مسبقًا.'
        }
      };
    }

    const now = new Date();
    const trialEnds = new Date(now.getTime() + 16 * 24 * 60 * 60 * 1000);
    const passwordHash = await bcrypt.hash(password, 12);
    const id = crypto.randomUUID();

    const row = {};
    put(row, cols, 'id', id);
    put(row, cols, 'email', email);
    put(row, cols, 'name', name || email.split('@')[0]);
    put(row, cols, 'full_name', name || email.split('@')[0]);
    put(row, cols, 'username', email.split('@')[0]);
    put(row, cols, 'phone', phoneRaw || phoneDigits);
    put(row, cols, 'phone_digits', phoneDigits);

    for (const c of ['password_hash','hashed_password','password_digest','pass_hash','pwd_hash']) {
      put(row, cols, c, passwordHash);
    }
    if (!Object.keys(row).some(k => /password|hash|digest|pwd/.test(k)) && has(cols, 'password')) {
      row.password = passwordHash;
    }

    put(row, cols, 'status', 'ACTIVE');
    put(row, cols, 'role', 'USER');
    put(row, cols, 'plan', 'Trial');
    put(row, cols, 'package', 'Trial');
    put(row, cols, 'segment', 'ordinary');
    put(row, cols, 'source', payload.source || 'my.ndsp.app');
    put(row, cols, 'is_admin', false);
    put(row, cols, 'email_verified', false);
    put(row, cols, 'trial_started_at', now.toISOString());
    put(row, cols, 'trial_ends_at', trialEnds.toISOString());
    put(row, cols, 'trial_end_at', trialEnds.toISOString());
    put(row, cols, 'expires_at', trialEnds.toISOString());
    put(row, cols, 'created_at', now.toISOString());
    put(row, cols, 'updated_at', now.toISOString());

    const keys = Object.keys(row).filter(k => has(cols, k));
    const placeholders = keys.map((_, i) => `$${i+1}`);
    const vals = keys.map(k => row[k]);

    const sql = `insert into users (${keys.map(k => `"${k}"`).join(',')}) values (${placeholders.join(',')}) returning *`;
    const ins = await client.query(sql, vals);
    await client.query('commit');

    const user = publicUser(ins.rows[0]);
    return {
      status: 201,
      body: {
        ok:true,
        message:'تم إنشاء الحساب بنجاح.',
        user,
        trial: { enabled:true, duration_days:16, status:'ACTIVE' },
        service:'ndsp-register-compat-gateway'
      }
    };
  } catch (e) {
    try { await client.query('rollback'); } catch (_) {}
    const msg = String(e && e.message || e);
    const isUnique = /duplicate key|unique/i.test(msg);
    return {
      status: isUnique ? 409 : 500,
      body: {
        ok:false,
        error: isUnique ? 'DUPLICATE_USER' : 'REGISTER_FAILED',
        message: isUnique ? 'البريد أو الجوال مسجل مسبقًا.' : 'تعذر إنشاء الحساب.',
        detail: msg.slice(0, 260),
        service:'ndsp-register-compat-gateway'
      }
    };
  } finally {
    client.release();
  }
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://127.0.0.1');
  if (req.method === 'OPTIONS') return send(res, 204, { ok:true });
  if (req.method === 'GET' && (url.pathname === '/health' || url.pathname === '/api/register/health')) {
    return send(res, 200, { ok:true, service:'ndsp-register-compat-gateway', port:PORT, endpoints:['/api/register','/api/auth/register'] });
  }
  if (req.method === 'POST' && (url.pathname === '/api/register' || url.pathname === '/api/auth/register')) {
    try {
      const payload = await readJson(req);
      const out = await createUser(payload);
      return send(res, out.status, out.body);
    } catch (e) {
      return send(res, 400, { ok:false, error:String(e.message || e), message:'طلب غير صالح.' });
    }
  }
  return send(res, 404, { ok:false, error:'NOT_FOUND', path:url.pathname, service:'ndsp-register-compat-gateway' });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`ndsp-register-compat-gateway listening on 127.0.0.1:${PORT}`);
});

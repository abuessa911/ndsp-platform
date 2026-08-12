'use strict';

// NDSP_TRIAL_SURVEY_NOTICE_BACKEND_ONLY_V5
const NDSP_TRIAL_SURVEY_NOTICE = {
  ar: "في نهاية فترة التجربة سيتم تقديم استبيان قصير لتقييم تجربتك مع منصة NDSP. يساعدنا الاستبيان على تحسين جودة القرار وتجربة المستخدم وتحديد أفضل باقة مناسبة لك بعد انتهاء التجربة.",
  en: "At the end of the trial period, a short survey will be provided to evaluate your NDSP experience. The survey helps improve decision quality, user experience, and the best package fit after the trial.",
  timing: "end_of_trial"
};


/* DSP_UNIQUE_CONSTRAINT_HTTP_RESPONSE_NODE_V1 */
/* DSP_REGISTER_FAILED_DIRECT_CLEAN_V1 */
function dspCleanRegisterError(err) {
  const msg = String([
    err && err.constraint,
    err && err.code,
    err && err.detail,
    err && err.message,
    err
  ].filter(Boolean).join(' | '));

  if (
    msg.includes('ux_users_phone_digits') ||
    msg.includes('ux_users_phone_canonical_guard') ||
    msg.includes('DUPLICATE_PHONE')
  ) {
    return { ok:false, code:'DUPLICATE_PHONE', message:'رقم الجوال مستخدم سابقًا' };
  }

  if (
    msg.includes('ux_users_email_lower') ||
    msg.includes('DUPLICATE_EMAIL')
  ) {
    return { ok:false, code:'DUPLICATE_EMAIL', message:'البريد الإلكتروني مستخدم سابقًا' };
  }

  return null;
}


const http = require('http');

const bcrypt = require('bcryptjs');
const crypto = require('crypto');
const { spawnSync } = require('child_process');
/* NDSP_MAIL_NOTIFICATION_PATCH */
const { Pool } = require('pg');

const PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);
const TRIAL_DAYS = Number(process.env.NDSP_TRIAL_DAYS || 16);

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL || undefined,
  host: process.env.PGHOST || process.env.DB_HOST || undefined,
  port: process.env.PGPORT ? Number(process.env.PGPORT) : (process.env.DB_PORT ? Number(process.env.DB_PORT) : undefined),
  database: process.env.PGDATABASE || process.env.DB_NAME || process.env.POSTGRES_DB || 'ndsp_auth',
  user: process.env.PGUSER || process.env.DB_USER || process.env.POSTGRES_USER || undefined,
  password: process.env.PGPASSWORD || process.env.DB_PASSWORD || process.env.POSTGRES_PASSWORD || undefined
});

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

function clean(v) {
  return String(v == null ? '' : v).trim();
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', c => {
      raw += c;
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

async function columnMeta(client, table) {
  const r = await client.query(`
    SELECT column_name, data_type, is_nullable, column_default
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name=$1
  `, [table]);
  return r.rows;
}


function sha256Hex(value) {
  return crypto.createHash('sha256').update(String(value || '')).digest('hex');
}

function publicAppUrl() {
  return (
    process.env.NDSP_PUBLIC_APP_URL ||
    process.env.PUBLIC_APP_URL ||
    process.env.APP_URL ||
    'https://my.ndsp.app'
  ).replace(/\/+$/, '');
}

function createActivationTokenValue() {
  return crypto.randomBytes(32).toString('hex');
}

async function createActivationToken(client, userId) {
  const token = createActivationTokenValue();
  const tokenHash = sha256Hex(token);

  await client.query(
    `INSERT INTO ndsp_auth_activation_tokens (user_id, token_hash, purpose, expires_at)
     VALUES ($1::uuid, $2, 'email_activation', now() + interval '48 hours')`,
    [userId, tokenHash]
  );

  return {
    token,
    activation_url: `${publicAppUrl()}/activate?token=${encodeURIComponent(token)}`
  };
}

async function hashPassword(password) {
  return await bcrypt.hash(String(password || ''), 12);
}

function extractInviteCode(v) {
  v = clean(v);
  if (!v) return '';

  try {
    const u = new URL(v);
    return clean(
      u.searchParams.get('invite') ||
      u.searchParams.get('code') ||
      u.searchParams.get('token') ||
      u.pathname.split('/').filter(Boolean).pop() ||
      v
    );
  } catch (_) {
    return v.replace(/^.*[?&](invite|code|token)=/i, '').split('&')[0].trim();
  }
}

async function ensureInviteTable(client) {
  await client.query(`
    CREATE TABLE IF NOT EXISTS trial_invite_codes (
      code TEXT PRIMARY KEY,
      status TEXT DEFAULT 'active',
      category TEXT DEFAULT 'premium_invite',
      max_uses INTEGER DEFAULT 1,
      used_count INTEGER DEFAULT 0,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      used_at TIMESTAMPTZ
    )
  `);
}

async function validateInvite(client, code) {
  await ensureInviteTable(client);

  const r = await client.query(`
    SELECT code, status, max_uses, used_count
    FROM trial_invite_codes
    WHERE code=$1
    LIMIT 1
  `, [code]);

  if (!r.rowCount) return { ok:false, error:'INVITE_CODE_INVALID' };

  const row = r.rows[0];
  const status = clean(row.status).toLowerCase();

  if (status !== 'active') return { ok:false, error:'INVITE_CODE_INACTIVE' };
  if (Number(row.used_count || 0) >= Number(row.max_uses || 1)) {
    return { ok:false, error:'INVITE_CODE_USED' };
  }

  return { ok:true };
}

async function markInviteUsed(client, code) {
  await client.query(`
    UPDATE trial_invite_codes
    SET used_count = COALESCE(used_count,0) + 1,
        used_at = NOW()
    WHERE code=$1
  `, [code]);
}

function valueForColumn(col, body, mode, id, passwordHash, trialEnds) {
  const name = col.column_name;
  const dt = col.data_type;
  const category =
    mode === 'ordinary' ? 'normal_beginner' :
    mode === 'professional' ? 'specialist_academic' :
    'premium_invite';

  const status =
    mode === 'ordinary' ? 'active' :
    'pending_review';

  const map = {
    id,
    name: body.name || body.full_name || body.display_name || '',
    full_name: body.name || body.full_name || '',
    display_name: body.name || body.display_name || '',
    email: body.email || '',
    phone: body.phone || body.mobile || '',
    mobile: body.phone || body.mobile || '',
    plan: 'Elite',
    package: 'Elite',
    tier: 'Elite',
    role: 'user',
    user_role: 'user',
    status,
    category,
    trial_category: category,
    user_category: category,
    notes: body.notes || body.reason || '',
    reason: body.notes || body.reason || '',
    invite_code: body.invite_code || '',
    invitation_code: body.invite_code || '',
    password_hash: passwordHash,
    password: passwordHash,
    created_at: new Date(),
    updated_at: new Date(),
    trial_ends: trialEnds,
    trial_end: trialEnds,
    trial_ends_at: trialEnds,
    expires_at: trialEnds,
    is_active: mode === 'ordinary',
    active: mode === 'ordinary',
    is_admin: false,
    admin: false
  };

  if (Object.prototype.hasOwnProperty.call(map, name)) return map[name];

  if (col.is_nullable === 'YES' || col.column_default) return undefined;

  if (dt.includes('timestamp') || dt === 'date') return new Date();
  if (dt === 'boolean') return false;
  if (dt.includes('integer') || dt.includes('numeric')) return 0;

  return '';
}

async function insertUser(client, body, mode) {
  const email = clean(body.email).toLowerCase();
  const password = clean(body.password);

  if (!email || !email.includes('@')) return { ok:false, code:400, error:'EMAIL_REQUIRED' };
  if (!password || password.length < 8) return { ok:false, code:400, error:'PASSWORD_MIN_8' };

  const existing = await client.query(`SELECT id FROM users WHERE LOWER(email)=LOWER($1) LIMIT 1`, [email]);

  // NDSP_PHONE_DUPLICATE_CANONICAL_GUARD_V45
  const rawPhoneForGuard = clean(body.phone || body.mobile || body.whatsapp || '');
  const phoneDigitsForGuard = String(rawPhoneForGuard || '').replace(/\D/g, '');
  const phoneKeyForGuard = phoneDigitsForGuard.slice(-9);

  if (phoneKeyForGuard && phoneKeyForGuard.length === 9) {
    const phoneExisting = await client.query(`
      SELECT id, email
      FROM users
      WHERE lower(coalesce(role,'')) NOT IN ('admin','owner','super_admin')
        AND (
          RIGHT(REGEXP_REPLACE(COALESCE(phone,''), '[^0-9]+', '', 'g'), 9) = $1
          OR RIGHT(REGEXP_REPLACE(COALESCE(canonical_phone,''), '[^0-9]+', '', 'g'), 9) = $1
          OR COALESCE(canonical_phone,'') = $1
        )
      LIMIT 1
    `, [phoneKeyForGuard]);

    if (phoneExisting.rowCount) {
      return {
        ok:false,
        code:409,
        error:'PHONE_ALREADY_EXISTS',
        message:'رقم الجوال مستخدم سابقًا'
      };
    }

    body.phone = rawPhoneForGuard;
    body.canonical_phone = phoneKeyForGuard;
  }





  if (existing.rowCount) return { ok:false, code:409, error:'EMAIL_ALREADY_EXISTS' };

  const meta = await columnMeta(client, 'users');
  const cols = new Set(meta.map(x => x.column_name));

  const id = crypto.randomUUID();
  const passwordHash = await bcrypt.hash(String(password || ''), 12);
  const trialEnds = new Date(Date.now() + TRIAL_DAYS * 24 * 60 * 60 * 1000);

  const insertCols = [];
  const values = [];

  for (const col of meta) {
    const v = valueForColumn(col, { ...body, email }, mode, id, passwordHash, trialEnds);
    if (v !== undefined) {
      insertCols.push(col.column_name);
      values.push(v);
    }
  }

  if (!insertCols.includes('email')) return { ok:false, code:500, error:'USERS_EMAIL_COLUMN_MISSING' };

  const placeholders = values.map((_, i) => `$${i + 1}`).join(', ');
  const sql = `
    INSERT INTO users (${insertCols.map(qident).join(', ')})
    VALUES (${placeholders})
    RETURNING ${cols.has('id') ? 'id::text AS id' : "'' AS id"}, ${cols.has('status') ? 'status' : "'' AS status"}
  `;

  const r = await client.query(sql, values);
  return { ok:true, user:r.rows[0], status:r.rows[0].status || null };
}


function sendMailSafe(to, subject, text, html) {
  try {
    const payload = JSON.stringify({ to, subject, text, html: html || '' });
    const r = spawnSync('/usr/local/bin/ndsp_send_mail.py', [], {
      input: payload,
      encoding: 'utf8',
      timeout: 30000,
      env: process.env
    });

    let out = {};
    try { out = JSON.parse(String(r.stdout || '{}')); } catch (_) {}

    return {
      ok: r.status === 0 && out.ok === true,
      status: r.status,
      result: out,
      stderr: String(r.stderr || '').slice(0, 300)
    };
  } catch (e) {
    return { ok: false, error: String(e && e.message ? e.message : e) };
  }
}

function adminMailTo() {
  return (
    process.env.SMTP_ADMIN_TO ||
    process.env.SMTP_TO ||
    process.env.ALERT_EMAIL_TO ||
    'ndsp.app@gmail.com'
  );
}

function registrationEmailTexts(body, mode, result) {
  const name = String(body.name || body.full_name || body.display_name || 'User');
  const email = String(body.email || '').toLowerCase();
  const status = String(result && result.status ? result.status : '');
  const isPending = mode !== 'ordinary';

  const modeLabel =
    mode === 'private' ? 'Premium invite-only / مميز بدعوة خاصة' :
    mode === 'professional' ? 'Professional/Academic / متخصص أو أكاديمي' :
    'Ordinary beginner / مستخدم عادي مبتدئ';

  const adminSubject = `NDSP New Trial Registration - ${modeLabel}`;
  const adminText =
`New NDSP trial registration received.

Name: ${name}
Email: ${email}
Type: ${modeLabel}
Status: ${status || (isPending ? 'pending_review' : 'active')}
Admin activation required: ${isPending ? 'Yes' : 'No'}
Invite required: ${mode === 'private' ? 'Yes' : 'No'}
Time: ${new Date().toISOString()}

Admin console:
https://admin.ndsp.app/
`;

  const userSubject = isPending
    ? 'NDSP — تم استلام طلب التسجيل'
    : 'NDSP — تم إنشاء حساب التجربة';

  const userText = isPending
    ? `مرحبًا ${name},

تم استلام طلب التسجيل في NDSP — منصة نواف لدعم القرار.

نوع الحساب:
${modeLabel}

طلبك الآن بانتظار مراجعة وتفعيل الإدارة. سنقوم بإشعارك بعد اكتمال المراجعة.

تنبيه: NDSP منصة دعم قرار وتحليل سياقي، وليست جهة استثمارية ولا تقدم توصيات مالية ملزمة.

NDSP
`
    : `مرحبًا ${name},

تم إنشاء حساب التجربة في NDSP — منصة نواف لدعم القرار.

يمكنك الآن الدخول إلى بوابة المستخدم:
https://my.ndsp.app/

تنبيه: NDSP منصة دعم قرار وتحليل سياقي، وليست جهة استثمارية ولا تقدم توصيات مالية ملزمة.

NDSP
`;

  return { adminSubject, adminText, userSubject, userText };
}

function notifyRegistrationEmails(body, mode, result) {
  const texts = registrationEmailTexts(body, mode, result);

  const admin = sendMailSafe(
    adminMailTo(),
    texts.adminSubject,
    texts.adminText
  );

  const user = sendMailSafe(
    String(body.email || '').toLowerCase(),
    texts.userSubject,
    texts.userText
  );

  return {
    admin_email_sent: admin.ok,
    user_email_sent: user.ok,
    admin_status: admin.status,
    user_status: (mode === 'ordinary' ? 'ACTIVE' : 'PENDING_REVIEW')
  };
}


async function syncAdminUsersJsonSafe() {
  return await new Promise((resolve) => {
    try {
      const key = String(process.env.NDSP_ADMIN_ACTION_KEY || '');
      if (!key) {
        return resolve({ ok:false, error:'NDSP_ADMIN_ACTION_KEY_MISSING' });
      }

      const payload = '{}';

      const req = http.request({
        hostname: '127.0.0.1',
        port: 9017,
        path: '/api/admin-actions/users/sync-json',
        method: 'POST',
        timeout: 15000,
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload),
          'X-NDSP-ADMIN-KEY': key
        }
      }, (res) => {
        let raw = '';
        res.on('data', chunk => { raw += chunk; });
        res.on('end', () => {
          let body = {};
          try { body = JSON.parse(raw || '{}'); } catch (_) {}
          resolve({
            ok: res.statusCode >= 200 && res.statusCode < 300 && body.ok === true,
            statusCode: res.statusCode,
            body
          });
        });
      });

      req.on('timeout', () => {
        try { req.destroy(); } catch (_) {}
        resolve({ ok:false, error:'ADMIN_JSON_SYNC_TIMEOUT' });
      });

      req.on('error', (e) => {
        resolve({ ok:false, error:String(e && e.message ? e.message : e) });
      });

      req.write(payload);
      req.end();

    } catch (e) {
      resolve({ ok:false, error:String(e && e.message ? e.message : e) });
    }
  });
}


async function activateUserByToken(client, token) {
  const tokenHash = sha256Hex(token);

  const found = await client.query(
    `SELECT t.id AS token_id, t.user_id::text AS user_id, t.used_at, t.expires_at,
            u.status, u.trial_started_at, u.trial_ends_at
     FROM ndsp_auth_activation_tokens t
     JOIN users u ON u.id = t.user_id
     WHERE t.token_hash = $1
     LIMIT 1`,
    [tokenHash]
  );

  if (!found.rowCount) {
    return { ok:false, code:400, error:'INVALID_ACTIVATION_TOKEN' };
  }

  const row = found.rows[0];

  if (row.used_at) {
    return { ok:false, code:409, error:'ACTIVATION_TOKEN_ALREADY_USED' };
  }

  if (new Date(row.expires_at).getTime() < Date.now()) {
    return { ok:false, code:410, error:'ACTIVATION_TOKEN_EXPIRED' };
  }

  await client.query(
    `UPDATE users
     SET status='ACTIVE',
         trial_started_at = COALESCE(trial_started_at, now()),
         trial_ends_at = COALESCE(trial_ends_at, now() + ($2::int || ' days')::interval),
         updated_at = now()
     WHERE id = $1::uuid`,
    [row.user_id, TRIAL_DAYS]
  );

  await client.query(
    `UPDATE ndsp_auth_activation_tokens
     SET used_at = now()
     WHERE id = $1`,
    [row.token_id]
  );

  return { ok:true, user_id:row.user_id, status:'ACTIVE' };
}

const server = http.createServer(async (req, res) => {
  try {
    const u = new URL(req.url, `http://${req.headers.host || '127.0.0.1'}`);


    if (req.method === 'GET' && (u.pathname === '/activate' || u.pathname === '/api/auth/activate' || u.pathname === '/api/trial/activate')) {
      const token = clean(u.searchParams.get('token') || '');
      if (!token) return send(res, 400, { ok:false, error:'TOKEN_REQUIRED' });

      const client = await pool.connect();
      try {
        await client.query('BEGIN');
        const activated = await activateUserByToken(client, token);

        if (!activated.ok) {
          await client.query('ROLLBACK');
          return send(res, activated.code || 400, { ok:false, error:activated.error });
        }

        await client.query('COMMIT');
        await syncAdminUsersJsonSafe();

        return send(res, 200, {
          ok:true,
          message:'ACCOUNT_ACTIVATED_TRIAL_STARTED',
          user_id:activated.user_id,
          status:activated.status,
          trial_days:TRIAL_DAYS
        });
      } catch (e) {
        try { await client.query('ROLLBACK'); } catch (_) {}
        return send(res, 500, { ok:false, error:'ACTIVATION_FAILED', detail:String(e && e.message ? e.message : e) });
      } finally {
        client.release();
      }
    }

    if (req.method === 'GET' && u.pathname === '/api/trial/register/health') {
      return send(res, 200, {
        ok:true,
        service:'ndsp-trial-register-gateway',
        endpoints:[
          '/api/trial/register/ordinary',
          '/api/trial/register/professional',
          '/api/trial/register/private-invite',
          '/api/trial/invites/validate'
        ],
        database:'PostgreSQL',
        admin_panel_sync: true,
        trial_days:TRIAL_DAYS
      });
    }

    if (req.method === 'POST' && u.pathname === '/api/trial/invites/validate') {
      const body = await readJson(req);
      const code = extractInviteCode(body.invite_code || body.invite || body.invitation_link || body.link);
      if (!code) return send(res, 400, { ok:false, error:'INVITE_CODE_REQUIRED' });

      const client = await pool.connect();
      try {
        const v = await validateInvite(client, code);
        return send(res, v.ok ? 200 : 400, v.ok ? { ok:true, invite_code:code } : { ok:false, error:v.error });
      } finally {
        client.release();
      }
    }

    const routes = {
      '/api/trial/register/ordinary': 'ordinary',
      '/api/trial/register/professional': 'professional',
      '/api/trial/register/private-invite': 'private'
    };

    if (req.method !== 'POST' || !routes[u.pathname]) {
      return send(res, 404, { ok:false, error:'NOT_FOUND', path:u.pathname });
    }

    const mode = routes[u.pathname];
    const body = await readJson(req);

    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      let inviteCode = '';
      if (mode === 'private') {
        inviteCode = extractInviteCode(body.invite_code || body.invite || body.invitation_link || body.link);
        if (!inviteCode) {
          await client.query('ROLLBACK');
          return send(res, 400, { ok:false, error:'INVITE_CODE_REQUIRED' });
        }

        const v = await validateInvite(client, inviteCode);
        if (!v.ok) {
          await client.query('ROLLBACK');
          return send(res, 400, { ok:false, error:v.error });
        }

        body.invite_code = inviteCode;
      }

      const result = await insertUser(client, body, mode);

      if (!result.ok) {
        await client.query('ROLLBACK');
        return send(res, result.code || 400, { ok:false, error:result.error });
      }

      if (mode === 'private') await markInviteUsed(client, inviteCode);

      let activation = null;
      if (result.user && result.user.id) {
        activation = await createActivationToken(client, result.user.id);
        body.activation_url = activation.activation_url;
      }

      await client.query('COMMIT');

      const adminJsonSync = await syncAdminUsersJsonSafe();

      const emailNotify = notifyRegistrationEmails(body, mode, result);

      const responsePayload = {
        ok:true,
        message:'REGISTRATION_SUBMITTED',
        mode,
        user_id:result.user.id,
        status:result.status,
        admin_activation_required: mode !== 'ordinary',
        invite_required: mode === 'private',
        email_notifications: emailNotify,
        survey_notice: NDSP_TRIAL_SURVEY_NOTICE,
        trial_starts_on: mode === 'ordinary' ? 'activation' : 'admin_activation',
        trial_day_1_policy: mode === 'ordinary'
          ? 'starts_from_account_activation'
          : 'starts_only_after_admin_approval',
        admin_json_sync: adminJsonSync
      };

      if (String(process.env.NDSP_DEBUG_ACTIVATION_URL || '').toLowerCase() === 'true' && activation) {
        responsePayload.activation_url_debug = activation.activation_url;
      }

      return send(res, 200, responsePayload);

      } catch (e) {
        try { await client.query('ROLLBACK'); } catch (_) {}
        const clean = dspCleanRegisterError(e);
        if (clean) return send(res, 200, clean);
        return send(res, 500, {
          ok:false,
          error:'REGISTER_FAILED',
          detail:String(e && e.message ? e.message : e)
        });
    } finally {
      client.release();
    }

  } catch (e) {
    return send(res, 500, {
      ok:false,
      error:'GATEWAY_EXCEPTION',
      detail:String(e && e.message ? e.message : e)
    });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] trial register gateway listening on 127.0.0.1:${PORT}`);
});

'use strict';

const crypto = require('crypto');

function safeEq(a, b) {
  a = String(a || '');
  b = String(b || '');
  const aa = Buffer.from(a);
  const bb = Buffer.from(b);
  if (aa.length !== bb.length) return false;
  return crypto.timingSafeEqual(aa, bb);
}

function parseCookies(req) {
  const out = {};
  String(req.headers.cookie || '').split(';').forEach(x => {
    const i = x.indexOf('=');
    if (i > -1) out[x.slice(0, i).trim()] = decodeURIComponent(x.slice(i + 1).trim());
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
      const expected = crypto
        .createHmac('sha256', secret)
        .update(`${h}.${p}`)
        .digest('base64url');

      if (safeEq(expected, s)) {
        const payload = JSON.parse(b64urlDecode(p));
        if (payload.exp && Date.now() >= Number(payload.exp) * 1000) return null;
        return payload;
      }
    }
  } catch (_) {}
  return null;
}

function getBrowserToken(req) {
  const auth = String(req.headers.authorization || '');
  if (/^Bearer\s+/i.test(auth)) return auth.replace(/^Bearer\s+/i, '').trim();

  const c = parseCookies(req);
  return (
    c.ndsp_admin_session ||
    c.ndsp_admin_token ||
    c.admin_session ||
    c.admin_token ||
    c.ndsp_session ||
    c.ndsp_token ||
    c.session ||
    c.token ||
    ''
  );
}

function qident(x) {
  return '"' + String(x).replace(/"/g, '""') + '"';
}

async function columns(pool, table) {
  const r = await pool.query(
    `SELECT column_name
     FROM information_schema.columns
     WHERE table_schema='public' AND table_name=$1`,
    [table]
  );
  return new Set(r.rows.map(x => x.column_name));
}

async function tableExists(pool, table) {
  const r = await pool.query(
    `SELECT 1
     FROM information_schema.tables
     WHERE table_schema='public' AND table_name=$1
     LIMIT 1`,
    [table]
  );
  return r.rowCount > 0;
}

async function authorize(req, pool) {
  const expected = String(process.env.NDSP_ADMIN_ACTION_KEY || '');
  const provided = String(req.headers['x-ndsp-admin-key'] || '');

  if (expected && provided && safeEq(expected, provided)) {
    return { ok: true, via: 'NDSP_ADMIN_ACTION_KEY', admin_user_id: null };
  }

  if (req.user) {
    const role = String(req.user.role || req.user.user_role || '').toLowerCase();
    if (role === 'admin' || role === 'super_admin' || role === 'owner') {
      return { ok: true, via: 'req.user', admin_user_id: req.user.id || req.user.user_id || null };
    }
  }

  const token = getBrowserToken(req);
  const secrets = [
    process.env.JWT_SECRET,
    process.env.NDSP_JWT_SECRET,
    process.env.AUTH_JWT_SECRET,
    process.env.SESSION_SECRET,
    process.env.NDSP_SESSION_SECRET
  ].filter(Boolean);

  if (token && secrets.length) {
    const payload = verifyJwtHS256(token, secrets);
    if (payload) {
      const role = String(payload.role || payload.user_role || '').toLowerCase();
      const uid = payload.id || payload.user_id || payload.sub || null;

      if (role === 'admin' || role === 'super_admin' || role === 'owner') {
        return { ok: true, via: 'jwt_role', admin_user_id: uid };
      }

      if (uid) {
        const ucols = await columns(pool, 'users');
        const checks = [];
        if (ucols.has('role')) checks.push(`LOWER(COALESCE(role,'')) IN ('admin','super_admin','owner')`);
        if (ucols.has('is_admin')) checks.push(`is_admin = true`);
        if (ucols.has('admin')) checks.push(`admin = true`);

        if (checks.length) {
          const r = await pool.query(
            `SELECT id FROM users WHERE id::text=$1 AND (${checks.join(' OR ')}) LIMIT 1`,
            [String(uid)]
          );
          if (r.rowCount) return { ok: true, via: 'db_admin_role', admin_user_id: String(uid) };
        }
      }
    }
  }

  return { ok: false, reason: 'ADMIN_AUTH_REQUIRED' };
}

async function deleteUserDependencies(client, userId) {
  const fk = await client.query(`
    SELECT
      kcu.table_name AS table_name,
      kcu.column_name AS column_name
    FROM information_schema.table_constraints tc
    JOIN information_schema.key_column_usage kcu
      ON tc.constraint_name = kcu.constraint_name
     AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage ccu
      ON ccu.constraint_name = tc.constraint_name
     AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_schema = 'public'
      AND ccu.table_name = 'users'
      AND ccu.column_name = 'id'
  `);

  for (const row of fk.rows) {
    const table = row.table_name;
    const col = row.column_name;
    if (table === 'users') continue;
    await client.query(`DELETE FROM ${qident(table)} WHERE ${qident(col)}::text=$1`, [userId]);
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

module.exports = function installNdspAdminActionsAuthoritative(app, pool) {
  if (!app || !pool || app.__ndspAdminActionsAuthoritativeInstalled) return;
  app.__ndspAdminActionsAuthoritativeInstalled = true;

  app.get('/api/admin/users/action/health', function(req, res) {
    res.json({
      ok: true,
      authoritative: true,
      php: false,
      endpoint: '/api/admin/users/action',
      env: 'NDSP_ADMIN_ACTION_KEY',
      header: 'X-NDSP-ADMIN-KEY',
      frontend_secret_required: false
    });
  });

  app.post(['/api/admin/users/action', '/admin/users/action'], async function(req, res) {
    const auth = await authorize(req, pool);

    if (!auth.ok) {
      return res.status(401).json({
        ok: false,
        error: 'ADMIN_AUTH_REQUIRED'
      });
    }

    const action = String((req.body && (req.body.action || req.body.type)) || '').trim().toLowerCase();
    const userId = String((req.body && (req.body.user_id || req.body.id)) || '').trim();

    if (!['activate', 'deactivate', 'delete'].includes(action)) {
      return res.status(400).json({ ok: false, error: 'INVALID_ACTION' });
    }

    if (!userId || userId === 'PUT_USER_ID_HERE') {
      return res.status(400).json({ ok: false, error: 'USER_ID_REQUIRED' });
    }

    if (action === 'delete' && auth.admin_user_id && String(auth.admin_user_id) === userId) {
      return res.status(400).json({ ok: false, error: 'CANNOT_DELETE_SELF' });
    }

    const client = await pool.connect();

    try {
      await client.query('BEGIN');

      const exists = await client.query(`SELECT id FROM users WHERE id::text=$1 LIMIT 1`, [userId]);
      if (!exists.rowCount) {
        await client.query('ROLLBACK');
        return res.status(404).json({ ok: false, error: 'USER_NOT_FOUND' });
      }

      const ucols = await columns(client, 'users');

      if (action === 'activate' || action === 'deactivate') {
        const active = action === 'activate';
        const sets = [];
        const vals = [];
        let i = 1;

        if (ucols.has('status')) {
          sets.push(`status=$${i++}`);
          vals.push(active ? 'ACTIVE' : 'INACTIVE');
        }

        if (ucols.has('is_active')) {
          sets.push(`is_active=$${i++}`);
          vals.push(active);
        }

        if (active && ucols.has('activated_at')) {
          sets.push(`activated_at=COALESCE(activated_at, NOW())`);
        }

        if (!active && ucols.has('deactivated_at')) {
          sets.push(`deactivated_at=NOW()`);
        }

        if (ucols.has('updated_at')) {
          sets.push(`updated_at=NOW()`);
        }

        if (!sets.length) {
          await client.query('ROLLBACK');
          return res.status(500).json({ ok: false, error: 'NO_USER_STATUS_COLUMNS' });
        }

        vals.push(userId);
        await client.query(`UPDATE users SET ${sets.join(', ')} WHERE id::text=$${i}`, vals);

        await client.query('COMMIT');
        return res.json({ ok: true, action, user_id: userId, via: auth.via });
      }

      await deleteUserDependencies(client, userId);
      await client.query(`DELETE FROM users WHERE id::text=$1`, [userId]);

      await client.query('COMMIT');
      return res.json({ ok: true, action: 'delete', user_id: userId, via: auth.via });

    } catch (e) {
      try { await client.query('ROLLBACK'); } catch (_) {}
      return res.status(500).json({
        ok: false,
        error: 'ADMIN_ACTION_FAILED',
        detail: String(e && e.message ? e.message : e)
      });
    } finally {
      client.release();
    }
  });
};

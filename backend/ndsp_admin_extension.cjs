
// NDSP_ADMIN_ACTION_KEY_ALIAS_BEGIN
function ndspAdminActionExpectedKey() {
  return String(
    process.env.NDSP_ADMIN_ACTION_KEY ||
    process.env.NDSP_ADMIN_KEY ||
    process.env.ADMIN_KEY ||
    ''
  ).trim()
}

function ndspAdminActionProvidedKey(req) {
  const auth = String(req.headers.authorization || '')
  const bearer = auth.toLowerCase().startsWith('bearer ') ? auth.slice(7).trim() : ''
  return String(
    req.headers['x-ndsp-admin-key'] ||
    req.headers['x-admin-key'] ||
    req.headers['x-admin-token'] ||
    req.headers['x-api-key'] ||
    req.body?.admin_key ||
    req.query?.admin_key ||
    bearer ||
    ''
  ).trim()
}
// NDSP_ADMIN_ACTION_KEY_ALIAS_END

const express = require('express');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
require('dotenv').config();

const connectionString =
  process.env.DATABASE_URL ||
  process.env.POSTGRES_URL ||
  process.env.POSTGRES_URI ||
  process.env.PG_CONNECTION_STRING ||
  'postgresql://postgres:postgres@127.0.0.1:5432/postgres';

const pool = new Pool({ connectionString });

const jwtSecrets = [
  process.env.JWT_SECRET,
  process.env.AUTH_JWT_SECRET,
  process.env.ACCESS_TOKEN_SECRET,
  process.env.SECRET_KEY,
  process.env.TOKEN_SECRET,
  'ndsp-secret'
].filter(Boolean);

const cache = {
  userColumns: null,
  userPlanColumn: null
};

function cleanText(v, fallback = '') {
  if (v === undefined || v === null) return fallback;
  return String(v).trim();
}

function jsonValue(v, fallback) {
  if (v === undefined || v === null || v === '') return fallback;
  if (typeof v === 'object') return v;
  try {
    return JSON.parse(v);
  } catch {
    return String(v)
      .split('\n')
      .map(x => x.trim())
      .filter(Boolean);
  }
}

async function userColumns() {
  if (cache.userColumns) return cache.userColumns;

  const { rows } = await pool.query(`
    SELECT column_name, udt_name
    FROM information_schema.columns
    WHERE table_schema='public' AND table_name='users'
  `);

  cache.userColumns = new Map(rows.map(r => [r.column_name, r.udt_name]));

  if (cache.userColumns.has('ndsp_plan_id')) {
    cache.userPlanColumn = 'ndsp_plan_id';
  } else if (
    cache.userColumns.has('plan_id') &&
    ['int4', 'int8'].includes(cache.userColumns.get('plan_id'))
  ) {
    cache.userPlanColumn = 'plan_id';
  } else {
    cache.userPlanColumn = null;
  }

  return cache.userColumns;
}

function bearerToken(req) {
  const h = req.headers.authorization || '';
  if (h.toLowerCase().startsWith('bearer ')) return h.slice(7).trim();
  return req.cookies?.token || req.cookies?.jwt || null;
}

function verifyToken(token) {
  let lastErr = null;
  for (const secret of jwtSecrets) {
    try {
      return jwt.verify(token, secret);
    } catch (err) {
      lastErr = err;
    }
  }
  if (process.env.NDSP_ALLOW_UNVERIFIED_ADMIN_JWT === '1') {
    return jwt.decode(token);
  }
  throw lastErr || new Error('Invalid token');
}

async function findUserFromPayload(payload) {
  const cols = await userColumns();
  if (!cols.size) return null;

  const id = payload.id || payload.userId || payload.user_id || payload.sub;
  const email = payload.email || payload.mail || payload.username;

  if (id !== undefined && id !== null) {
    const { rows } = await pool.query(`SELECT * FROM public.users WHERE id::text=$1 LIMIT 1`, [String(id)]);
    if (rows[0]) return rows[0];
  }

  if (email && cols.has('email')) {
    const { rows } = await pool.query(`SELECT * FROM public.users WHERE lower(email)=lower($1) LIMIT 1`, [String(email)]);
    if (rows[0]) return rows[0];
  }

  return null;
}

async function requireAdmin(req, res, next) {
  try {
    const token = bearerToken(req);
    if (!token) return res.status(401).json({ error: 'Missing token' });
    const expectedAdminActionKey = ndspAdminActionExpectedKey();
    if (!expectedAdminActionKey || token !== expectedAdminActionKey) {
      return res.status(403).json({ error: 'Invalid admin key' });
    }
    // NDSP_ADMIN_ACTION_VALIDATE_PATCH

    const payload = verifyToken(token);
    const user = await findUserFromPayload(payload);

    if (!user) return res.status(401).json({ error: 'User not found' });
    if (String(user.status || 'active') !== 'active') return res.status(403).json({ error: 'User inactive' });
    if (String(user.role || '').toLowerCase() !== 'admin') return res.status(403).json({ error: 'Admin only' });

    req.authPayload = payload;
    req.authUser = user;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

async function optionalUser(req, _res, next) {
  try {
    const token = bearerToken(req);
    if (!token) return next();
    const payload = verifyToken(token);
    req.authUser = await findUserFromPayload(payload);
  } catch (_) {}
  next();
}

async function audit(req, action, entity, entityId, beforeData, afterData) {
  try {
    await pool.query(`
      INSERT INTO public.ndsp_audit_log
        (actor_user_id, actor_email, action, entity, entity_id, before_data, after_data, ip, user_agent)
      VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
    `, [
      req.authUser?.id !== undefined ? String(req.authUser.id) : null,
      req.authUser?.email || null,
      action,
      entity,
      entityId !== undefined && entityId !== null ? String(entityId) : null,
      beforeData ? JSON.stringify(beforeData) : null,
      afterData ? JSON.stringify(afterData) : null,
      req.ip || req.headers['x-forwarded-for'] || null,
      req.headers['user-agent'] || null
    ]);
  } catch (err) {
    console.error('audit error:', err.message);
  }
}

async function selectUserById(id) {
  const { rows } = await pool.query(`SELECT * FROM public.users WHERE id::text=$1 LIMIT 1`, [String(id)]);
  return rows[0] || null;
}

function userPublicSelect(planCol) {
  const planSelect = planCol ? `u.${planCol}::text AS plan_id, p.name AS plan_name, p.code AS plan_code,` : `NULL::text AS plan_id, NULL::text AS plan_name, NULL::text AS plan_code,`;
  const join = planCol ? `LEFT JOIN public.ndsp_plans p ON p.id = u.${planCol}` : ``;

  return {
    sql: `
      SELECT
        u.id::text AS id,
        ${planSelect}
        ${'u.email' ? 'u.email AS email,' : ''}
        COALESCE(u.role, 'user') AS role,
        COALESCE(u.status, 'active') AS status,
        u.trial_ends_at,
        u.created_at
      FROM public.users u
      ${join}
      ORDER BY u.created_at DESC NULLS LAST, u.id::text DESC
    `
  };
}

function installNdspAdminExtension(app) {
  const admin = express.Router();
  const pub = express.Router();

  admin.use(express.json({ limit: '2mb' }));
  pub.use(express.json({ limit: '2mb' }));
  admin.use(requireAdmin);

  admin.get('/health', (_req, res) => res.json({ ok: true, service: 'ndsp-admin-api' }));

  admin.get('/users', async (_req, res) => {
    try {
      await userColumns();
      const planCol = cache.userPlanColumn;
      const { sql } = userPublicSelect(planCol);
      const { rows } = await pool.query(sql);
      res.json({ users: rows });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.patch('/users/:id', async (req, res) => {
    try {
      await userColumns();
      const before = await selectUserById(req.params.id);
      if (!before) return res.status(404).json({ error: 'User not found' });

      const sets = [];
      const params = [];
      let i = 1;

      if (Object.prototype.hasOwnProperty.call(req.body, 'role')) {
        const role = cleanText(req.body.role).toLowerCase();
        if (!['admin', 'user'].includes(role)) return res.status(400).json({ error: 'Invalid role' });
        sets.push(`role=$${i++}`);
        params.push(role);
      }

      if (Object.prototype.hasOwnProperty.call(req.body, 'status')) {
        const status = cleanText(req.body.status).toLowerCase();
        if (!['active', 'suspended'].includes(status)) return res.status(400).json({ error: 'Invalid status' });
        sets.push(`status=$${i++}`);
        params.push(status);
      }

      if (Object.prototype.hasOwnProperty.call(req.body, 'plan_id')) {
        if (!cache.userPlanColumn) return res.status(400).json({ error: 'No compatible plan column on users table' });
        const planId = Number(req.body.plan_id);
        if (!Number.isInteger(planId)) return res.status(400).json({ error: 'Invalid plan_id' });
        const plan = await pool.query(`SELECT id FROM public.ndsp_plans WHERE id=$1`, [planId]);
        if (!plan.rows[0]) return res.status(400).json({ error: 'Plan not found' });
        sets.push(`${cache.userPlanColumn}=$${i++}`);
        params.push(planId);
      }

      if (!sets.length) return res.status(400).json({ error: 'Nothing to update' });

      params.push(String(req.params.id));
      const { rows } = await pool.query(`
        UPDATE public.users SET ${sets.join(', ')}
        WHERE id::text=$${i}
        RETURNING *
      `, params);

      await audit(req, 'update_user', 'user', req.params.id, before, rows[0]);
      res.json({ user: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.post('/users/:id/suspend', async (req, res) => {
    req.body.status = 'suspended';
    admin.handle({ ...req, method: 'PATCH', url: `/users/${req.params.id}`, originalUrl: req.originalUrl }, res);
  });

  admin.post('/users/:id/activate', async (req, res) => {
    req.body.status = 'active';
    admin.handle({ ...req, method: 'PATCH', url: `/users/${req.params.id}`, originalUrl: req.originalUrl }, res);
  });

  admin.delete('/users/:id', async (req, res) => {
    try {
      const before = await selectUserById(req.params.id);
      if (!before) return res.status(404).json({ error: 'User not found' });

      if (String(before.id) === String(req.authUser.id)) {
        return res.status(400).json({ error: 'Cannot delete current admin user' });
      }

      await pool.query(`DELETE FROM public.users WHERE id::text=$1`, [String(req.params.id)]);
      await audit(req, 'delete_user', 'user', req.params.id, before, null);
      res.json({ ok: true });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.get('/plans', async (_req, res) => {
    const { rows } = await pool.query(`SELECT * FROM public.ndsp_plans ORDER BY id`);
    res.json({ plans: rows });
  });

  admin.post('/plans', async (req, res) => {
    try {
      const body = req.body || {};
      const { rows } = await pool.query(`
        INSERT INTO public.ndsp_plans
          (code, name, price, description, trial_days, features, limits, is_active)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        RETURNING *
      `, [
        cleanText(body.code).toLowerCase(),
        cleanText(body.name),
        Number(body.price || 0),
        cleanText(body.description),
        Number.parseInt(body.trial_days || 16, 10),
        JSON.stringify(jsonValue(body.features, [])),
        JSON.stringify(jsonValue(body.limits, {})),
        body.is_active !== false
      ]);
      await audit(req, 'create_plan', 'plan', rows[0].id, null, rows[0]);
      res.json({ plan: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.patch('/plans/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_plans WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Plan not found' });

      const body = req.body || {};
      const next = {
        code: Object.prototype.hasOwnProperty.call(body, 'code') ? cleanText(body.code).toLowerCase() : before.code,
        name: Object.prototype.hasOwnProperty.call(body, 'name') ? cleanText(body.name) : before.name,
        price: Object.prototype.hasOwnProperty.call(body, 'price') ? Number(body.price) : before.price,
        description: Object.prototype.hasOwnProperty.call(body, 'description') ? cleanText(body.description) : before.description,
        trial_days: Object.prototype.hasOwnProperty.call(body, 'trial_days') ? Number.parseInt(body.trial_days, 10) : before.trial_days,
        features: Object.prototype.hasOwnProperty.call(body, 'features') ? jsonValue(body.features, []) : before.features,
        limits: Object.prototype.hasOwnProperty.call(body, 'limits') ? jsonValue(body.limits, {}) : before.limits,
        is_active: Object.prototype.hasOwnProperty.call(body, 'is_active') ? Boolean(body.is_active) : before.is_active
      };

      const { rows } = await pool.query(`
        UPDATE public.ndsp_plans
        SET code=$1, name=$2, price=$3, description=$4, trial_days=$5,
            features=$6, limits=$7, is_active=$8, updated_at=now()
        WHERE id=$9
        RETURNING *
      `, [
        next.code, next.name, next.price, next.description, next.trial_days,
        JSON.stringify(next.features), JSON.stringify(next.limits), next.is_active, req.params.id
      ]);

      await audit(req, 'update_plan', 'plan', req.params.id, before, rows[0]);
      res.json({ plan: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.delete('/plans/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_plans WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Plan not found' });

      const { rows } = await pool.query(`
        UPDATE public.ndsp_plans SET is_active=false, updated_at=now()
        WHERE id=$1 RETURNING *
      `, [req.params.id]);

      await audit(req, 'disable_plan', 'plan', req.params.id, before, rows[0]);
      res.json({ plan: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.get('/layers', async (_req, res) => {
    const { rows } = await pool.query(`
      SELECT
        l.*,
        COALESCE(
          json_agg(pl.plan_id ORDER BY pl.plan_id) FILTER (WHERE pl.plan_id IS NOT NULL),
          '[]'
        ) AS plan_ids
      FROM public.ndsp_layers l
      LEFT JOIN public.ndsp_plan_layers pl ON pl.layer_id = l.id
      GROUP BY l.id
      ORDER BY l.sort_order, l.id
    `);
    res.json({ layers: rows });
  });

  admin.post('/layers', async (req, res) => {
    try {
      const body = req.body || {};
      const { rows } = await pool.query(`
        INSERT INTO public.ndsp_layers
          (code, name, description, is_visible, is_sovereign, sort_order)
        VALUES ($1,$2,$3,$4,$5,$6)
        RETURNING *
      `, [
        cleanText(body.code).toLowerCase(),
        cleanText(body.name),
        cleanText(body.description),
        body.is_visible !== false,
        Boolean(body.is_sovereign),
        Number.parseInt(body.sort_order || 0, 10)
      ]);
      await audit(req, 'create_layer', 'layer', rows[0].id, null, rows[0]);
      res.json({ layer: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.patch('/layers/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_layers WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Layer not found' });

      if (before.is_sovereign && req.body.is_sovereign === false) {
        return res.status(409).json({ error: 'Sovereign layer cannot be downgraded' });
      }

      const body = req.body || {};
      const next = {
        code: Object.prototype.hasOwnProperty.call(body, 'code') ? cleanText(body.code).toLowerCase() : before.code,
        name: Object.prototype.hasOwnProperty.call(body, 'name') ? cleanText(body.name) : before.name,
        description: Object.prototype.hasOwnProperty.call(body, 'description') ? cleanText(body.description) : before.description,
        is_visible: Object.prototype.hasOwnProperty.call(body, 'is_visible') ? Boolean(body.is_visible) : before.is_visible,
        is_sovereign: Object.prototype.hasOwnProperty.call(body, 'is_sovereign') ? Boolean(body.is_sovereign) : before.is_sovereign,
        sort_order: Object.prototype.hasOwnProperty.call(body, 'sort_order') ? Number.parseInt(body.sort_order, 10) : before.sort_order
      };

      const { rows } = await pool.query(`
        UPDATE public.ndsp_layers
        SET code=$1, name=$2, description=$3, is_visible=$4,
            is_sovereign=$5, sort_order=$6, updated_at=now()
        WHERE id=$7
        RETURNING *
      `, [
        next.code, next.name, next.description, next.is_visible,
        next.is_sovereign, next.sort_order, req.params.id
      ]);

      await audit(req, 'update_layer', 'layer', req.params.id, before, rows[0]);
      res.json({ layer: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.put('/layers/:id/plans', async (req, res) => {
    const client = await pool.connect();
    try {
      const layer = (await client.query(`SELECT * FROM public.ndsp_layers WHERE id=$1`, [req.params.id])).rows[0];
      if (!layer) return res.status(404).json({ error: 'Layer not found' });

      const planIds = Array.isArray(req.body.plan_ids) ? req.body.plan_ids.map(Number).filter(Number.isInteger) : [];

      await client.query('BEGIN');
      await client.query(`DELETE FROM public.ndsp_plan_layers WHERE layer_id=$1`, [req.params.id]);
      for (const planId of planIds) {
        await client.query(`
          INSERT INTO public.ndsp_plan_layers (plan_id, layer_id)
          VALUES ($1,$2)
          ON CONFLICT DO NOTHING
        `, [planId, req.params.id]);
      }
      await client.query('COMMIT');

      await audit(req, 'link_layer_plans', 'layer', req.params.id, layer, { plan_ids: planIds });
      res.json({ ok: true });
    } catch (err) {
      try { await client.query('ROLLBACK'); } catch (_) {}
      res.status(500).json({ error: err.message });
    } finally {
      client.release();
    }
  });

  admin.delete('/layers/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_layers WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Layer not found' });
      if (before.is_sovereign) return res.status(409).json({ error: 'Sovereign layer is protected' });

      await pool.query(`DELETE FROM public.ndsp_layers WHERE id=$1`, [req.params.id]);
      await audit(req, 'delete_layer', 'layer', req.params.id, before, null);
      res.json({ ok: true });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.get('/assets', async (_req, res) => {
    const { rows } = await pool.query(`SELECT * FROM public.ndsp_assets ORDER BY code`);
    res.json({ assets: rows });
  });

  admin.post('/assets', async (req, res) => {
    try {
      const body = req.body || {};
      const { rows } = await pool.query(`
        INSERT INTO public.ndsp_assets (code, name, is_active)
        VALUES ($1,$2,$3)
        ON CONFLICT (code) DO UPDATE SET
          name=EXCLUDED.name,
          is_active=EXCLUDED.is_active,
          updated_at=now()
        RETURNING *
      `, [
        cleanText(body.code).toUpperCase(),
        cleanText(body.name),
        body.is_active !== false
      ]);

      await audit(req, 'upsert_asset', 'asset', rows[0].code, null, rows[0]);
      res.json({ asset: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.patch('/assets/:code', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_assets WHERE code=$1`, [req.params.code.toUpperCase()])).rows[0];
      if (!before) return res.status(404).json({ error: 'Asset not found' });

      const body = req.body || {};
      const { rows } = await pool.query(`
        UPDATE public.ndsp_assets
        SET name=$1, is_active=$2, updated_at=now()
        WHERE code=$3
        RETURNING *
      `, [
        Object.prototype.hasOwnProperty.call(body, 'name') ? cleanText(body.name) : before.name,
        Object.prototype.hasOwnProperty.call(body, 'is_active') ? Boolean(body.is_active) : before.is_active,
        req.params.code.toUpperCase()
      ]);

      await audit(req, 'update_asset', 'asset', req.params.code.toUpperCase(), before, rows[0]);
      res.json({ asset: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.get('/settings', async (_req, res) => {
    const settings = {};
    const { rows } = await pool.query(`SELECT key, value FROM public.ndsp_settings ORDER BY key`);
    for (const row of rows) settings[row.key] = row.value;
    const coupons = await pool.query(`SELECT * FROM public.ndsp_discount_codes ORDER BY id DESC`);
    res.json({ settings, coupons: coupons.rows });
  });

  admin.put('/settings', async (req, res) => {
    try {
      const allowed = [
        'official_email',
        'trial_days',
        'registration_enabled',
        'payment_enabled',
        'welcome_subject',
        'welcome_message'
      ];

      const beforeRows = await pool.query(`SELECT key, value FROM public.ndsp_settings`);
      const before = Object.fromEntries(beforeRows.rows.map(r => [r.key, r.value]));

      for (const key of allowed) {
        if (Object.prototype.hasOwnProperty.call(req.body, key)) {
          await pool.query(`
            INSERT INTO public.ndsp_settings (key, value, updated_at)
            VALUES ($1,$2,now())
            ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value, updated_at=now()
          `, [key, JSON.stringify(req.body[key])]);
        }
      }

      const afterRows = await pool.query(`SELECT key, value FROM public.ndsp_settings`);
      const after = Object.fromEntries(afterRows.rows.map(r => [r.key, r.value]));

      await audit(req, 'update_settings', 'settings', 'platform', before, after);
      res.json({ settings: after });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.post('/settings/coupons', async (req, res) => {
    try {
      const body = req.body || {};
      const { rows } = await pool.query(`
        INSERT INTO public.ndsp_discount_codes
          (code, percent, amount, is_active, expires_at)
        VALUES ($1,$2,$3,$4,$5)
        RETURNING *
      `, [
        cleanText(body.code).toUpperCase(),
        Number(body.percent || 0),
        Number(body.amount || 0),
        body.is_active !== false,
        body.expires_at || null
      ]);

      await audit(req, 'create_coupon', 'coupon', rows[0].id, null, rows[0]);
      res.json({ coupon: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.patch('/settings/coupons/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_discount_codes WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Coupon not found' });

      const body = req.body || {};
      const { rows } = await pool.query(`
        UPDATE public.ndsp_discount_codes
        SET code=$1, percent=$2, amount=$3, is_active=$4, expires_at=$5, updated_at=now()
        WHERE id=$6
        RETURNING *
      `, [
        Object.prototype.hasOwnProperty.call(body, 'code') ? cleanText(body.code).toUpperCase() : before.code,
        Object.prototype.hasOwnProperty.call(body, 'percent') ? Number(body.percent) : before.percent,
        Object.prototype.hasOwnProperty.call(body, 'amount') ? Number(body.amount) : before.amount,
        Object.prototype.hasOwnProperty.call(body, 'is_active') ? Boolean(body.is_active) : before.is_active,
        Object.prototype.hasOwnProperty.call(body, 'expires_at') ? (body.expires_at || null) : before.expires_at,
        req.params.id
      ]);

      await audit(req, 'update_coupon', 'coupon', req.params.id, before, rows[0]);
      res.json({ coupon: rows[0] });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.delete('/settings/coupons/:id', async (req, res) => {
    try {
      const before = (await pool.query(`SELECT * FROM public.ndsp_discount_codes WHERE id=$1`, [req.params.id])).rows[0];
      if (!before) return res.status(404).json({ error: 'Coupon not found' });

      await pool.query(`DELETE FROM public.ndsp_discount_codes WHERE id=$1`, [req.params.id]);
      await audit(req, 'delete_coupon', 'coupon', req.params.id, before, null);
      res.json({ ok: true });
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
  });

  admin.get('/audit', async (req, res) => {
    const limit = Math.min(Number(req.query.limit || 200), 1000);
    const { rows } = await pool.query(`
      SELECT *
      FROM public.ndsp_audit_log
      ORDER BY created_at DESC
      LIMIT $1
    `, [limit]);
    res.json({ audit: rows });
  });

  pub.get('/plans', async (_req, res) => {
    const { rows } = await pool.query(`
      SELECT id, code, name, price, description, trial_days, features, limits
      FROM public.ndsp_plans
      WHERE is_active=true
      ORDER BY price, id
    `);
    res.json({ plans: rows });
  });

  pub.get('/assets', async (_req, res) => {
    const { rows } = await pool.query(`
      SELECT code, name
      FROM public.ndsp_assets
      WHERE is_active=true
      ORDER BY code
    `);
    res.json({ assets: rows });
  });

  pub.get('/layers', optionalUser, async (req, res) => {
    await userColumns();

    if (req.authUser && String(req.authUser.role || '').toLowerCase() === 'admin') {
      const { rows } = await pool.query(`SELECT * FROM public.ndsp_layers ORDER BY sort_order, id`);
      return res.json({ layers: rows });
    }

    const planCol = cache.userPlanColumn;
    if (req.authUser && planCol && req.authUser[planCol]) {
      const { rows } = await pool.query(`
        SELECT DISTINCT l.*
        FROM public.ndsp_layers l
        JOIN public.ndsp_plan_layers pl ON pl.layer_id = l.id
        WHERE pl.plan_id=$1
          AND l.is_visible=true
          AND l.is_sovereign=false
        ORDER BY l.sort_order, l.id
      `, [req.authUser[planCol]]);
      return res.json({ layers: rows });
    }

    const { rows } = await pool.query(`
      SELECT *
      FROM public.ndsp_layers
      WHERE is_visible=true AND is_sovereign=false
      ORDER BY sort_order, id
    `);
    res.json({ layers: rows });
  });

  app.use('/api/admin', admin);
  app.use('/api', pub);

  console.log('✅ NDSP admin API mounted on /api/admin');
}

module.exports = { installNdspAdminExtension };

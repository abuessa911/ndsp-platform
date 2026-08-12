
/* DSP_UNIQUE_CONSTRAINT_HTTP_RESPONSE_NODE_V1 */
function dspCleanRegisterError(err) {
  const msg = String((err && (err.detail || err.message)) || err || '');
  if (msg.includes('ux_users_phone_digits')) {
    return { ok:false, code:'DUPLICATE_PHONE', message:'رقم الجوال مستخدم سابقًا' };
  }
  if (msg.includes('ux_users_email_lower')) {
    return { ok:false, code:'DUPLICATE_EMAIL', message:'البريد الإلكتروني مستخدم سابقًا' };
  }
  return null;
}


// NDSP_AUTH_FORCE_PORT_9020
process.env.PORT = process.env.NDSP_AUTH_PORT || process.env.AUTH_PORT || '9020';

require('dotenv').config();
const { generateSecret, generateURI, verify } = require('otplib')



function ndspBuildOtpAuthUri(email, secret) {
  return generateURI({
    issuer: 'NDSP',
    label: String(email || 'ndsp-user'),
    secret: String(secret || ''),
    algorithm: 'sha1',
    digits: 6,
    period: 30
  });
}
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');

const app = express();

/* NDSP_TRIAL_INFO_START */
try {
  const { installTrialInfo } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_info.cjs');
  installTrialInfo(app);
} catch (e) {
  console.error('⚠️ NDSP trial info skipped:', e.message);
}
/* NDSP_TRIAL_INFO_END */


/* NDSP_NOWPAYMENTS_START */
try {
  const { installNowPayments } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_nowpayments.cjs');
  installNowPayments(app);
} catch (e) {
  console.error('❌ NDSP NOWPayments failed:', e);
  throw e;
}
/* NDSP_NOWPAYMENTS_END */






/* NDSP_DEVICE_GUARD_START */
try {
  const { installDeviceRegistrationGuard } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_device_guard.cjs');
  installDeviceRegistrationGuard(app);
} catch (e) {
  console.error('❌ NDSP device guard failed:', e);
  throw e;
}
/* NDSP_DEVICE_GUARD_END */


/* NDSP_ADMIN_EXTENSION_START */
try {
  const { installNdspAdminExtension } = require('/home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_extension.cjs');
  installNdspAdminExtension(app);
  console.log('✅ NDSP admin extension mounted early');
} catch (e) {
  console.error('❌ NDSP admin extension failed:', e);
  throw e;
}
/* NDSP_ADMIN_EXTENSION_END */

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const PORT = Number(process.env.PORT || 9010);
const ADMIN_EMAIL = (process.env.ADMIN_EMAIL || 'ndsp.app@gmail.com').toLowerCase();

function ndspCreate2faSecret() {
  try {
    const otplib = require('otplib');
    if (typeof otplib.generateSecret === 'function') {
      try {
        return otplib.generateSecret();
      } catch (e) {
        try {
          return otplib.generateSecret({
            crypto: new otplib.NobleCryptoPlugin(),
            base32: new otplib.ScureBase32Plugin()
          });
        } catch (_) {}
      }
    }
  } catch (_) {}

  // Fallback: RFC-compatible base32-ish secret without external dependency.
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
  let out = '';
  for (let i = 0; i < 32; i++) out += alphabet[Math.floor(Math.random() * alphabet.length)];
  return out;
}

function ndspCreateOtpAuthUrl(email, secret) {
  const issuer = 'NDSP';
  const label = encodeURIComponent(String(email || 'ndsp-user'));
  return 'otpauth://totp/' + encodeURIComponent(issuer) + ':' + label +
    '?secret=' + encodeURIComponent(secret) +
    '&issuer=' + encodeURIComponent(issuer) +
    '&algorithm=SHA1&digits=6&period=30';
}


app.use(helmet());
app.use(cors({ origin: true, credentials: true }));
app.use(express.json({ limit: '1mb' }));

function tokenFor(user) {
  return jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role,
      plan: user.plan
    },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
}

function auth(req, res, next) {
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : '';

  if (!token) return res.status(401).json({ ok: false, error: 'UNAUTHORIZED' });

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    return next();
  } catch {
    return res.status(401).json({ ok: false, error: 'INVALID_TOKEN' });
  }
}

function adminOnly(req, res, next) {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ ok: false, error: 'ADMIN_ONLY' });
  }
  return next();
}

app.get('/health', async (req, res) => {
  const db = await pool.query('SELECT now() AS now');
  res.json({
    ok: true,
    service: 'ndsp-auth-api',
    database: 'ok',
    timestamp: db.rows[0].now
  });
});

app.post('/auth/register', async (req, res) => {
  const name = String(req.body.name || '').trim();
  const email = String(req.body.email || '').trim().toLowerCase();
  const password = String(req.body.password || '');
  const plan = String(req.body.plan || 'insight');

  if (!name || !email || password.length < 6) {
    return res.status(400).json({ ok: false, error: 'INVALID_REGISTER_INPUT' });
  }

  const role = email === ADMIN_EMAIL ? 'admin' : 'user';
  const passwordHash = await bcrypt.hash(password, 12);

  try {
    const result = await pool.query(
      `INSERT INTO users (name, email, password_hash, plan, role)
       VALUES ($1, $2, $3, $4, $5)
       RETURNING id, name, email, plan, role, trial_day, trial_started_at, trial_ends_at, activated_at, created_at`,
      [name, email, passwordHash, plan, role]
    );

    const user = result.rows[0];

    await createNotification(
      user.id,
      'مرحباً بك في NDSP',
      'تم إنشاء حسابك وبدء تجربة الـ 16 يوم. تابع رحلتك من لوحة المستخدم.',
      'success'
    );

    res.json({ ok: true, user, token: tokenFor(user) });
  } catch (err) {
    if (String(err.message).includes('users_email_unique_idx')) {
      return res.status(409).json({ ok: false, error: 'EMAIL_ALREADY_EXISTS' });
    }
    console.error(err);
    res.status(500).json({ ok: false, error: 'REGISTER_FAILED' });
  }
});

app.post('/auth/login', async (req, res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const password = String(req.body.password || '');

  const result = await pool.query(
    `SELECT id, name, email, password_hash, plan, role, trial_day, trial_started_at, trial_ends_at, activated_at, created_at
     FROM users
     WHERE lower(email) = lower($1)
     LIMIT 1`,
    [email]
  );

  const user = result.rows[0];
  if (!user) return res.status(401).json({ ok: false, error: 'INVALID_LOGIN' });

  const ok = await bcrypt.compare(password, user.password_hash);
  if (!ok) return res.status(401).json({ ok: false, error: 'INVALID_LOGIN' });

  delete user.password_hash;

  try {
    await pool.query('SELECT ndsp_start_trial_on_first_login($1::uuid)', [user.id]);

    const refreshed = await pool.query(
      `SELECT id, name, email, plan, role, trial_day, trial_started_at, trial_ends_at, activated_at, created_at
       FROM users
       WHERE id = $1`,
      [user.id]
    );

    if (refreshed.rows && refreshed.rows[0]) {
      user = refreshed.rows[0];
    }
  } catch (e) {
    console.error('[DSP] first-login trial hook failed:', e && e.message ? e.message : e);
  }

  res.json({ ok: true, user, token: tokenFor(user) });
});

app.get('/me', auth, async (req, res) => {
  const result = await pool.query(
    `SELECT id, name, email, plan, role, trial_day, trial_started_at, trial_ends_at, activated_at, created_at
     FROM users
     WHERE id = $1`,
    [req.user.id]
  );

  res.json({ ok: true, user: result.rows[0] || null });
});

app.post('/feedback', auth, async (req, res) => {
  const result = await pool.query(
    `INSERT INTO feedback_surveys
      (user_id, user_type, value_answer, clarity_answer, improvement_answer, upgrade_answer)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING id, created_at`,
    [
      req.user.id,
      req.body.user_type || null,
      req.body.value_answer || null,
      req.body.clarity_answer || null,
      req.body.improvement_answer || null,
      req.body.upgrade_answer || null
    ]
  );

  await createNotification(
    req.user.id,
    'تم استلام الاستبيان',
    'تم حفظ الاستبيان النهائي، وسيتم مراجعته للتأهل للعرض الحصري.',
    'info'
  );

  res.json({
    ok: true,
    feedback: result.rows[0],
    discount_review_status: 'PENDING_ADMIN_REVIEW'
  });
});


app.post('/upgrade-request', auth, async (req, res) => {
  const requestedPlan = String(req.body.requested_plan || '').trim()
  const reason = String(req.body.reason || '').trim()

  const allowed = ['pro', 'elite', 'saas']
  if (!allowed.includes(requestedPlan)) {
    return res.status(400).json({ ok: false, error: 'INVALID_REQUESTED_PLAN' })
  }

  const userResult = await pool.query(
    `SELECT id, plan FROM users WHERE id = $1`,
    [req.user.id]
  )

  const user = userResult.rows[0]
  if (!user) return res.status(404).json({ ok: false, error: 'USER_NOT_FOUND' })

  const result = await pool.query(
    `INSERT INTO plan_upgrade_requests
      (user_id, current_plan, requested_plan, reason)
     VALUES ($1, $2, $3, $4)
     RETURNING id, current_plan, requested_plan, reason, status, created_at`,
    [req.user.id, user.plan, requestedPlan, reason || null]
  )

  await createNotification(
    req.user.id,
    'تم إرسال طلب الترقية',
    'تم استلام طلب ترقية الباقة وسيتم مراجعته من الإدارة.',
    'info'
  )

  res.json({
    ok: true,
    request: result.rows[0],
    message: 'UPGRADE_REQUEST_CREATED'
  })
})

app.get('/upgrade-requests/me', auth, async (req, res) => {
  const result = await pool.query(
    `SELECT id, current_plan, requested_plan, reason, status, admin_note, created_at, reviewed_at
     FROM plan_upgrade_requests
     WHERE user_id = $1
     ORDER BY created_at DESC
     LIMIT 20`,
    [req.user.id]
  )

  res.json({ ok: true, requests: result.rows })
})

app.get('/admin/upgrade-requests', auth, adminOnly, async (req, res) => {
  const result = await pool.query(
    `SELECT r.id, r.current_plan, r.requested_plan, r.reason, r.status,
            r.admin_note, r.created_at, r.reviewed_at,
            u.name, u.email, u.plan, u.role
     FROM plan_upgrade_requests r
     JOIN users u ON u.id = r.user_id
     ORDER BY r.created_at DESC
     LIMIT 100`
  )

  res.json({ ok: true, requests: result.rows })
})

app.post('/admin/upgrade-requests/:id/review', auth, adminOnly, async (req, res) => {
  const id = req.params.id
  const status = String(req.body.status || '').trim()
  const adminNote = String(req.body.admin_note || '').trim()

  if (!['approved', 'rejected'].includes(status)) {
    return res.status(400).json({ ok: false, error: 'INVALID_STATUS' })
  }

  const requestResult = await pool.query(
    `SELECT user_id, requested_plan
     FROM plan_upgrade_requests
     WHERE id = $1`,
    [id]
  )

  const request = requestResult.rows[0]
  if (!request) return res.status(404).json({ ok: false, error: 'REQUEST_NOT_FOUND' })

  await pool.query(
    `UPDATE plan_upgrade_requests
     SET status = $1, admin_note = $2, reviewed_at = now()
     WHERE id = $3`,
    [status, adminNote || null, id]
  )

  if (status === 'approved') {
    await pool.query(
      `UPDATE users SET plan = $1 WHERE id = $2`,
      [request.requested_plan, request.user_id]
    )
  }

  await createNotification(
    request.user_id,
    status === 'approved' ? 'تمت الموافقة على الترقية' : 'تم رفض طلب الترقية',
    status === 'approved'
      ? 'تمت الموافقة على طلب الترقية وتحديث باقتك.'
      : 'تمت مراجعة طلب الترقية ولم تتم الموافقة عليه حالياً.',
    status === 'approved' ? 'success' : 'warning'
  )

  res.json({ ok: true, status })
})


app.get('/trial/status', auth, async (req, res) => {
  const userResult = await pool.query(
    `SELECT id, name, email, plan, role, trial_started_at
     FROM users
     WHERE id = $1`,
    [req.user.id]
  )

  const user = userResult.rows[0]
  if (!user) return res.status(404).json({ ok: false, error: 'USER_NOT_FOUND' })

  const surveyResult = await pool.query(
    `SELECT id, discount_status, created_at
     FROM feedback_surveys
     WHERE user_id = $1
     ORDER BY created_at DESC
     LIMIT 1`,
    [req.user.id]
  )

  const startedAt = new Date(user.trial_started_at)
  const now = new Date()
  const diffMs = now - startedAt
  const currentDay = Math.min(16, Math.max(1, Math.floor(diffMs / (1000 * 60 * 60 * 24)) + 1))
  const completed = currentDay >= 16
  const latestSurvey = surveyResult.rows[0] || null

  res.json({
    ok: true,
    trial: {
      current_day: currentDay,
      total_days: 16,
      progress_percent: Math.round((currentDay / 16) * 100),
      started_at: user.trial_started_at,
      completed,
      survey_submitted: Boolean(latestSurvey),
      discount_status: latestSurvey?.discount_status || 'not_submitted',
      discount_eligible: completed && Boolean(latestSurvey)
    }
  })
})

app.get('/admin/feedback', auth, adminOnly, async (req, res) => {
  const result = await pool.query(
    `SELECT f.id, f.user_type, f.value_answer, f.clarity_answer,
            f.improvement_answer, f.upgrade_answer,
            f.discount_status, f.admin_note, f.created_at, f.reviewed_at,
            u.name, u.email, u.plan, u.role
     FROM feedback_surveys f
     LEFT JOIN users u ON u.id = f.user_id
     ORDER BY f.created_at DESC
     LIMIT 100`
  )

  res.json({ ok: true, feedback: result.rows })
})

app.post('/admin/feedback/:id/review', auth, adminOnly, async (req, res) => {
  const id = req.params.id
  const status = String(req.body.discount_status || '').trim()
  const adminNote = String(req.body.admin_note || '').trim()

  if (!['approved', 'rejected', 'pending'].includes(status)) {
    return res.status(400).json({ ok: false, error: 'INVALID_DISCOUNT_STATUS' })
  }

  const result = await pool.query(
    `UPDATE feedback_surveys
     SET discount_status = $1,
         admin_note = $2,
         reviewed_at = now()
     WHERE id = $3
     RETURNING id, discount_status, admin_note, reviewed_at`,
    [status, adminNote || null, id]
  )

  if (!result.rows[0]) {
    return res.status(404).json({ ok: false, error: 'FEEDBACK_NOT_FOUND' })
  }

  const feedbackUser = await pool.query(
    `SELECT user_id FROM feedback_surveys WHERE id = $1`,
    [id]
  )

  const userId = feedbackUser.rows[0]?.user_id

  if (userId) {
    await createNotification(
      userId,
      status === 'approved' ? 'تم اعتماد الخصم الحصري' : 'تمت مراجعة الخصم',
      status === 'approved'
        ? 'تهانينا، تمت الموافقة على أهليتك للخصم الحصري.'
        : 'تمت مراجعة الاستبيان ولم يتم اعتماد الخصم حالياً.',
      status === 'approved' ? 'success' : 'warning'
    )
  }

  res.json({ ok: true, feedback: result.rows[0] })
})


async function createNotification(userId, title, body, type = 'info') {
  try {
    await pool.query(
      `INSERT INTO notifications (user_id, title, body, type)
       VALUES ($1, $2, $3, $4)`,
      [userId, title, body, type]
    )
  } catch (err) {
    console.error('createNotification failed', err.message)
  }
}

app.get('/notifications', auth, async (req, res) => {
  const result = await pool.query(
    `SELECT id, title, body, type, is_read, created_at
     FROM notifications
     WHERE user_id = $1
     ORDER BY created_at DESC
     LIMIT 50`,
    [req.user.id]
  )

  res.json({ ok: true, notifications: result.rows })
})

app.post('/notifications/:id/read', auth, async (req, res) => {
  await pool.query(
    `UPDATE notifications
     SET is_read = true
     WHERE id = $1 AND user_id = $2`,
    [req.params.id, req.user.id]
  )

  res.json({ ok: true })
})

app.get('/admin/notifications', auth, adminOnly, async (req, res) => {
  const result = await pool.query(
    `SELECT n.id, n.title, n.body, n.type, n.is_read, n.created_at,
            u.name, u.email, u.plan, u.role
     FROM notifications n
     LEFT JOIN users u ON u.id = n.user_id
     ORDER BY n.created_at DESC
     LIMIT 100`
  )

  res.json({ ok: true, notifications: result.rows })
})

app.post('/admin/notifications/send', auth, adminOnly, async (req, res) => {
  const email = String(req.body.email || '').trim().toLowerCase()
  const title = String(req.body.title || '').trim()
  const body = String(req.body.body || '').trim()
  const type = String(req.body.type || 'info').trim()

  if (!email || !title || !body) {
    return res.status(400).json({ ok: false, error: 'INVALID_NOTIFICATION_INPUT' })
  }

  const userResult = await pool.query(
    `SELECT id, name, email FROM users WHERE lower(email) = lower($1) LIMIT 1`,
    [email]
  )

  const user = userResult.rows[0]
  if (!user) return res.status(404).json({ ok: false, error: 'USER_NOT_FOUND' })

  await createNotification(user.id, title, body, type)

  res.json({ ok: true, message: 'NOTIFICATION_SENT' })
})


app.get('/plans', async (req, res) => {
  const plans = await pool.query(
    `SELECT * FROM plans WHERE active = true ORDER BY
      CASE id WHEN 'insight' THEN 1 WHEN 'pro' THEN 2 WHEN 'elite' THEN 3 WHEN 'saas' THEN 4 ELSE 9 END`
  )

  const features = await pool.query(
    `SELECT plan_id, feature, is_hidden, sort_order
     FROM plan_features
     ORDER BY sort_order ASC`
  )

  const layers = await pool.query(
    `SELECT plan_id, layer_key, visible
     FROM plan_layer_access`
  )

  res.json({
    ok: true,
    plans: plans.rows.map(plan => ({
      ...plan,
      features: features.rows.filter(f => f.plan_id === plan.id && !f.is_hidden),
      hidden: features.rows.filter(f => f.plan_id === plan.id && f.is_hidden),
      layers: layers.rows.filter(l => l.plan_id === plan.id && l.visible).map(l => l.layer_key)
    }))
  })
})

app.get('/admin/plans', auth, adminOnly, async (req, res) => {
  const plans = await pool.query(`SELECT * FROM plans ORDER BY id`)
  const features = await pool.query(`SELECT * FROM plan_features ORDER BY plan_id, sort_order`)
  const layers = await pool.query(`SELECT * FROM plan_layer_access ORDER BY plan_id, layer_key`)

  res.json({
    ok: true,
    plans: plans.rows,
    features: features.rows,
    layers: layers.rows
  })
})

app.put('/admin/plans/:id', auth, adminOnly, async (req, res) => {
  const id = req.params.id
  const { name, price, audience, active, trial_days } = req.body

  const result = await pool.query(
    `UPDATE plans
     SET name = COALESCE($1, name),
         price = COALESCE($2, price),
         audience = COALESCE($3, audience),
         active = COALESCE($4, active),
         trial_days = COALESCE($5, trial_days),
         updated_at = now()
     WHERE id = $6
     RETURNING *`,
    [name ?? null, price ?? null, audience ?? null, active ?? null, trial_days ?? null, id]
  )

  if (!result.rows[0]) return res.status(404).json({ ok: false, error: 'PLAN_NOT_FOUND' })
  res.json({ ok: true, plan: result.rows[0] })
})

app.post('/admin/plans/:id/features', auth, adminOnly, async (req, res) => {
  const planId = req.params.id
  const { feature, is_hidden, sort_order } = req.body

  if (!feature) return res.status(400).json({ ok: false, error: 'FEATURE_REQUIRED' })

  const result = await pool.query(
    `INSERT INTO plan_features (plan_id, feature, is_hidden, sort_order)
     VALUES ($1, $2, $3, $4)
     RETURNING *`,
    [planId, feature, Boolean(is_hidden), Number(sort_order || 0)]
  )

  res.json({ ok: true, feature: result.rows[0] })
})

app.delete('/admin/plan-features/:id', auth, adminOnly, async (req, res) => {
  await pool.query(`DELETE FROM plan_features WHERE id = $1`, [req.params.id])
  res.json({ ok: true })
})

app.put('/admin/plans/:id/layers/:layerKey', auth, adminOnly, async (req, res) => {
  const { id, layerKey } = req.params
  const visible = Boolean(req.body.visible)

  const result = await pool.query(
    `INSERT INTO plan_layer_access (plan_id, layer_key, visible)
     VALUES ($1, $2, $3)
     ON CONFLICT (plan_id, layer_key)
     DO UPDATE SET visible = EXCLUDED.visible
     RETURNING *`,
    [id, layerKey, visible]
  )

  res.json({ ok: true, layer: result.rows[0] })
})

app.get('/admin/stats', auth, adminOnly, async (req, res) => {
  const users = await pool.query('SELECT count(*)::int AS count FROM users');
  const surveys = await pool.query('SELECT count(*)::int AS count FROM feedback_surveys');

  res.json({
    ok: true,
    stats: {
      users: users.rows[0].count,
      surveys: surveys.rows[0].count,
      active_assets: ['BTC', 'ETH', 'XRP'],
      system_status: 'stable'
    }
  });
});


app.put('/admin/users/:id', auth, adminOnly, async (req, res) => {
  const id = req.params.id
  const { role, plan, status } = req.body

  if (role && !['user', 'admin'].includes(role)) {
    return res.status(400).json({ ok: false, error: 'INVALID_ROLE' })
  }

  if (status && !['active', 'suspended'].includes(status)) {
    return res.status(400).json({ ok: false, error: 'INVALID_STATUS' })
  }

  const result = await pool.query(
    `UPDATE users
     SET role = COALESCE($1, role),
         plan = COALESCE($2, plan),
         status = COALESCE($3, status)
     WHERE id = $4
     RETURNING id, name, email, plan, role, status, trial_day, trial_started_at, trial_ends_at, activated_at, created_at`,
    [role || null, plan || null, status || null, id]
  )

  if (!result.rows[0]) return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' })
  res.json({ ok:true, user: result.rows[0] })
})

app.delete('/admin/users/:id', auth, adminOnly, async (req, res) => {
  const id = req.params.id

  if (id === req.user.id) {
    return res.status(400).json({ ok:false, error:'CANNOT_DELETE_SELF' })
  }

  const client = await pool.connect()

  try {
    await client.query('BEGIN')

    await client.query(`DELETE FROM notifications WHERE user_id = $1`, [id])
    await client.query(`DELETE FROM plan_upgrade_requests WHERE user_id = $1`, [id])
    await client.query(`DELETE FROM feedback_surveys WHERE user_id = $1`, [id])
    await client.query(`DELETE FROM users WHERE id = $1`, [id])

    await client.query('COMMIT')
    res.json({ ok:true })
  } catch (err) {
    await client.query('ROLLBACK')
    console.error('DELETE_USER_FAILED', err)
    res.status(500).json({ ok:false, error:'DELETE_USER_FAILED', detail: err.message })
  } finally {
    client.release()
  }
})

app.get('/admin/users', auth, adminOnly, async (req, res) => {
  const result = await pool.query(
    `SELECT id, name, email, plan, role, status, trial_day, trial_started_at, trial_ends_at, activated_at, created_at
     FROM users
     ORDER BY created_at DESC
     LIMIT 100`
  );

  res.json({ ok: true, users: result.rows });
});



function ndspConfirmTotpCode(secret, token) {
  try {
    const cleanToken = String(token || '').replace(/\s+/g, '');
    if (!/^\d{6}$/.test(cleanToken)) return false;

    const crypto = require('crypto');
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';

    function base32ToBuffer(base32) {
      const cleaned = String(base32 || '').toUpperCase().replace(/=+$/,'').replace(/[^A-Z2-7]/g,'');
      let bits = '';
      for (const ch of cleaned) {
        const val = alphabet.indexOf(ch);
        if (val < 0) continue;
        bits += val.toString(2).padStart(5, '0');
      }
      const bytes = [];
      for (let i = 0; i + 8 <= bits.length; i += 8) {
        bytes.push(parseInt(bits.slice(i, i + 8), 2));
      }
      return Buffer.from(bytes);
    }

    function hotp(sec, counter) {
      const key = base32ToBuffer(sec);
      const buf = Buffer.alloc(8);
      buf.writeBigUInt64BE(BigInt(counter));
      const hmac = crypto.createHmac('sha1', key).update(buf).digest();
      const offset = hmac[hmac.length - 1] & 0x0f;
      const bin =
        ((hmac[offset] & 0x7f) << 24) |
        ((hmac[offset + 1] & 0xff) << 16) |
        ((hmac[offset + 2] & 0xff) << 8) |
        (hmac[offset + 3] & 0xff);
      return String(bin % 1000000).padStart(6, '0');
    }

    const nowCounter = Math.floor(Date.now() / 1000 / 30);
    for (const drift of [-2, -1, 0, 1, 2]) {
      if (hotp(secret, nowCounter + drift) === cleanToken) return true;
    }
    return false;
  } catch (e) {
    console.error('NDSP_2FA_CONFIRM_HELPER_FAILED', e);
    return false;
  }
}

// NDSP_LIVE_2FA_SETUP_START_ROUTE_FINAL
app.post('/api/auth/2fa/setup/start', async (req, res) => {
  try {
    const email =
      (req.body && req.body.email) ||
      (req.query && req.query.email) ||
      (req.user && req.user.email);

    if (!email) {
      return res.status(400).json({ ok: false, error: 'EMAIL_REQUIRED' });
    }

    const userResult = await pool.query(
      'SELECT id, email FROM users WHERE lower(email)=lower($1) LIMIT 1',
      [email]
    );

    if (!userResult.rows || userResult.rows.length === 0) {
      return res.status(404).json({ ok: false, error: 'USER_NOT_FOUND', email });
    }

    const user = userResult.rows[0];
    const secret = ndspCreate2faSecret();
    const otpauth_url = ndspCreateOtpAuthUrl(user.email, secret);

    await pool.query(`
      CREATE TABLE IF NOT EXISTS user_two_factor_settings (
        user_id uuid PRIMARY KEY,
        email text,
        secret text,
        enabled boolean DEFAULT false,
        verified boolean DEFAULT false,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
      )
    `);

    await pool.query(
      `INSERT INTO user_two_factor_settings (user_id, email, secret, enabled, verified, created_at, updated_at)
       VALUES ($1, $2, $3, false, false, now(), now())
       ON CONFLICT (user_id)
       DO UPDATE SET email=EXCLUDED.email, secret=EXCLUDED.secret, enabled=false, verified=false, updated_at=now()`,
      [user.id, user.email, secret]
    );

    await pool.query(
      `UPDATE users
       SET two_factor_secret=$1,
           two_factor_enabled=false,
           two_factor_setup_required=true,
           two_factor_last_prompt_at=now()
       WHERE id=$2`,
      [secret, user.id]
    );

    return res.json({
      ok: true,
      status: 'setup_started',
      email: user.email,
      secret,
      manual_key: secret,
      otpauth_url
    });
  } catch (err) {
    console.error('TWO_FACTOR_SETUP_START_FAILED', err);
    return res.status(500).json({
      ok: false,
      error: 'TWO_FACTOR_SETUP_START_FAILED',
      detail: err && err.message ? err.message : String(err)
    });
  }
});


// NDSP_LIVE_2FA_CONFIRM_ROUTE_FINAL
app.post('/api/auth/2fa/setup/confirm', async (req, res) => {
  try {
    const email =
      (req.body && req.body.email) ||
      (req.query && req.query.email) ||
      (req.user && req.user.email);

    const token =
      (req.body && (req.body.token || req.body.code || req.body.otp)) ||
      (req.query && (req.query.token || req.query.code || req.query.otp));

    if (!email) return res.status(400).json({ ok:false, error:'EMAIL_REQUIRED' });
    if (!token) return res.status(400).json({ ok:false, error:'TOKEN_REQUIRED' });

    const userResult = await pool.query(
      `SELECT id,email,two_factor_secret
       FROM users
       WHERE lower(email)=lower($1)
       LIMIT 1`,
      [email]
    );

    if (!userResult.rows || userResult.rows.length === 0) {
      return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });
    }

    const user = userResult.rows[0];
    let secret = user.two_factor_secret;

    if (!secret) {
      const s2 = await pool.query(
        `SELECT secret FROM user_two_factor_settings
         WHERE user_id=$1 OR lower(email)=lower($2)
         ORDER BY updated_at DESC NULLS LAST, created_at DESC NULLS LAST
         LIMIT 1`,
        [user.id, user.email]
      );
      if (s2.rows && s2.rows[0]) secret = s2.rows[0].secret;
    }

    if (!secret) {
      return res.status(400).json({ ok:false, error:'TWO_FACTOR_SECRET_MISSING' });
    }

    const valid = ndspConfirmTotpCode(secret, token);

    if (!valid) {
      return res.status(400).json({ ok:false, error:'INVALID_2FA_CODE' });
    }

    await pool.query(
      `UPDATE users
       SET two_factor_enabled=true,
           two_factor_setup_required=false,
           two_factor_confirmed_at=now()
       WHERE id=$1`,
      [user.id]
    );

    await pool.query(
      `UPDATE user_two_factor_settings
       SET enabled=true, verified=true, updated_at=now()
       WHERE user_id=$1 OR lower(email)=lower($2)`,
      [user.id, user.email]
    );

    return res.json({
      ok:true,
      status:'two_factor_enabled',
      email:user.email
    });
  } catch (err) {
    console.error('TWO_FACTOR_CONFIRM_FAILED', err);
    return res.status(500).json({
      ok:false,
      error:'TWO_FACTOR_CONFIRM_FAILED',
      detail: err && err.message ? err.message : String(err)
    });
  }
});









app.use((req, res) => {
  res.status(404).json({ ok: false, error: 'NOT_FOUND', path: req.path });
});

// NDSP_ADMIN_USER_ACTIONS_API_BEGIN
const fs = require('fs')
const { execFile } = require('child_process')

function ndspReadAdminActionKey() {
  try {
    const env = fs.readFileSync('/etc/ndsp/ndsp-admin.env', 'utf8')
    const line = env.split(/\r?\n/).find(x => x.startsWith('NDSP_ADMIN_ACTION_KEY='))
    return line ? line.split('=').slice(1).join('=').trim() : ''
  } catch (e) {
    return ''
  }
}

function ndspRunExporter() {
  try {
    execFile('/usr/bin/python3', ['/usr/local/bin/ndsp_export_admin_users_json.py'], { timeout: 15000 }, () => {})
  } catch (e) {}
}

app.post('/__retired_api_admin_users_action_legacy', async (req, res) => {
  const expected = ndspReadAdminActionKey()
  const provided = String(req.headers['x-ndsp-admin-key'] || req.body?.admin_key || '').trim()

  if (!expected || provided !== expected) {
    return res.status(401).json({ ok:false, error:'UNAUTHORIZED' })
  }

  const action = String(req.body?.action || '').trim()
  const userId = String(req.body?.user_id || '').trim()

  if (!['activate', 'deactivate', 'delete'].includes(action)) {
    return res.status(400).json({ ok:false, error:'INVALID_ACTION' })
  }

  if (!/^[0-9a-fA-F-]{20,80}$/.test(userId)) {
    return res.status(400).json({ ok:false, error:'INVALID_USER_ID' })
  }

  const client = await pool.connect()

  try {
    await client.query('BEGIN')

    const found = await client.query('SELECT id FROM users WHERE id = $1 LIMIT 1', [userId])
    if (!found.rowCount) {
      await client.query('ROLLBACK')
      return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' })
    }

    if (action === 'activate') {
      await client.query(`UPDATE users SET status = 'active' WHERE id = $1`, [userId])
    }

    if (action === 'deactivate') {
      await client.query(`UPDATE users SET status = 'inactive' WHERE id = $1`, [userId])
    }

    if (action === 'delete') {
      await client.query(`DELETE FROM notifications WHERE user_id = $1`, [userId])
      await client.query(`DELETE FROM plan_upgrade_requests WHERE user_id = $1`, [userId])
      await client.query(`DELETE FROM feedback_surveys WHERE user_id = $1`, [userId])
      await client.query(`DELETE FROM users WHERE id = $1`, [userId])
    }

    await client.query('COMMIT')
    ndspRunExporter()

    return res.json({
      ok:true,
      action,
      user_id:userId,
      message:'ACTION_COMPLETED'
    })
  } catch (e) {
    try { await client.query('ROLLBACK') } catch (_) {}
    return res.status(500).json({ ok:false, error:'DB_ACTION_FAILED', detail:String(e.message || e).slice(0,160) })
  } finally {
    client.release()
  }
})
// NDSP_ADMIN_USER_ACTIONS_API_END

/* NDSP_AUTHORITATIVE_ADMIN_ACTIONS_BEGIN */
try {
  require('./ndsp_admin_actions_authoritative.cjs')(app, pool);
  console.log('[NDSP] authoritative admin user actions installed');
} catch (e) {
  console.error('[NDSP] authoritative admin user actions failed:', e && e.message ? e.message : e);
}
/* NDSP_AUTHORITATIVE_ADMIN_ACTIONS_END */

/* NDSP_ADMIN_ACTIONS_BYPASS_OLD_MIDDLEWARE_BEGIN */
try {
  require('./ndsp_admin_actions_bypass_old_middleware.cjs')(app, pool);
  console.log('[NDSP] admin actions bypass old middleware route installed');
} catch (e) {
  console.error('[NDSP] admin actions bypass old middleware route failed:', e && e.message ? e.message : e);
}
/* NDSP_ADMIN_ACTIONS_BYPASS_OLD_MIDDLEWARE_END */

// NDSP_2FA_SETUP_START_COMPAT_ROUTE
app.post('/api/auth/2fa/setup/start', async (req, res) => {
  try {
    const email =
      (req.body && req.body.email) ||
      (req.user && req.user.email) ||
      (req.query && req.query.email);

    if (!email) {
      return res.status(400).json({
        ok: false,
        error: 'EMAIL_REQUIRED'
      });
    }

    const userResult = await pool.query(
      'SELECT id, email FROM users WHERE lower(email)=lower($1) LIMIT 1',
      [email]
    );

    if (!userResult.rows || userResult.rows.length === 0) {
      return res.status(404).json({
        ok: false,
        error: 'USER_NOT_FOUND',
        email
      });
    }

    const user = userResult.rows[0];
    const secret = generateSecret();
    const otpauth_url = ndspBuildOtpAuthUri(user.email, secret);

    await pool.query(
      `CREATE TABLE IF NOT EXISTS user_two_factor_settings (
        user_id uuid PRIMARY KEY,
        email text,
        secret text,
        enabled boolean DEFAULT false,
        verified boolean DEFAULT false,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
      )`
    );

    await pool.query(
      `INSERT INTO user_two_factor_settings (user_id, email, secret, enabled, verified, created_at, updated_at)
       VALUES ($1, $2, $3, false, false, now(), now())
       ON CONFLICT (user_id)
       DO UPDATE SET email=EXCLUDED.email, secret=EXCLUDED.secret, enabled=false, verified=false, updated_at=now()`,
      [user.id, user.email, secret]
    );

    return res.json({
      ok: true,
      status: 'setup_started',
      email: user.email,
      secret,
      otpauth_url,
      manual_key: secret
    });
  } catch (err) {
    console.error('TWO_FACTOR_SETUP_START_FAILED', err);
    return res.status(500).json({
      ok: false,
      error: 'TWO_FACTOR_SETUP_START_FAILED',
      detail: err && err.message ? err.message : String(err)
    });
  }
});














app.listen(PORT, '127.0.0.1', () => {
  console.log(`NDSP Auth API listening on http://127.0.0.1:${PORT}`);
});


// NDSP_TELEGRAM_PACKAGE_ROUTING_FINAL_BLOCK
// Admin Telegram package routing controls.
// Keeps tokens server-side. UI only sends admin key.
const https = require('https');

function ndspReadEnvFileSafe(path) {
  try {
    const fs = require('fs');
    if (!fs.existsSync(path)) return;
    const lines = fs.readFileSync(path, 'utf8').split(/\r?\n/);
    for (const line of lines) {
      if (!line || line.trim().startsWith('#') || !line.includes('=')) continue;
      const idx = line.indexOf('=');
      const k = line.slice(0, idx).trim();
      const v = line.slice(idx + 1).trim().replace(/^['"]|['"]$/g, '');
      if (k && !process.env[k]) process.env[k] = v;
    }
  } catch (e) {}
}

ndspReadEnvFileSafe('/etc/ndsp/ndsp-telegram.env');
ndspReadEnvFileSafe('/etc/ndsp/ndsp-telegram-routing.env');
ndspReadEnvFileSafe('/etc/ndsp/ndsp-db.env');
ndspReadEnvFileSafe('/home/nawaf511/empire-core-new/backend/.env');

function ndspAdminKeyFromReq(req) {
  const auth = req.headers.authorization || '';
  if (auth.toLowerCase().startsWith('bearer ')) return auth.slice(7).trim();
  return (
    req.headers['x-admin-key'] ||
    req.headers['x-ndsp-admin-key'] ||
    req.headers['x-ndsp-admin-action-key'] ||
    req.query.admin_key ||
    ''
  );
}

function ndspAdminOk(req) {
  const got = String(ndspAdminKeyFromReq(req) || '').trim();
  const allowed = [
    process.env.NDSP_ADMIN_ACTION_KEY,
    process.env.NDSP_ADMIN_KEY,
    process.env.ADMIN_KEY,
    process.env.X_ADMIN_KEY
  ].filter(Boolean).map(x => String(x).trim());
  return !!got && allowed.includes(got);
}

function ndspMaskChat(v) {
  if (!v) return null;
  v = String(v);
  if (v.length <= 8) return '********';
  return v.slice(0, 4) + '********' + v.slice(-4);
}

async function ndspEnsureTelegramRoutesTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ndsp_telegram_delivery_routes (
      id SERIAL PRIMARY KEY,
      plan_code TEXT UNIQUE NOT NULL,
      enabled BOOLEAN NOT NULL DEFAULT false,
      target_type TEXT NOT NULL DEFAULT 'channel',
      chat_id TEXT,
      daily_limit INTEGER,
      description TEXT,
      last_test_ok BOOLEAN,
      last_test_at TIMESTAMPTZ,
      last_test_message TEXT,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
  `);

  await pool.query(`
    ALTER TABLE ndsp_telegram_delivery_routes
      ADD COLUMN IF NOT EXISTS last_test_ok BOOLEAN,
      ADD COLUMN IF NOT EXISTS last_test_at TIMESTAMPTZ,
      ADD COLUMN IF NOT EXISTS last_test_message TEXT
  `);

  await pool.query(`
    INSERT INTO ndsp_telegram_delivery_routes
      (plan_code, enabled, target_type, chat_id, daily_limit, description)
    VALUES
      ('free', false, 'none', NULL, 0, 'Free package has no Telegram alerts'),
      ('pro', true, 'channel', '-1003491841685', 25, 'Pro Telegram alerts'),
      ('elite', true, 'channel', '-1003793881886', 250, 'Elite Telegram alerts'),
      ('saas', true, 'channel', '-1003918395339', NULL, 'SaaS Telegram alerts'),
      ('institutional_suite', true, 'channel', '-1003918395339', NULL, 'Institutional Suite Telegram alerts')
    ON CONFLICT (plan_code) DO NOTHING
  `);
}

app.get('/api/admin/telegram-routing/status', async (req, res) => {
  try {
    if (!ndspAdminOk(req)) return res.status(401).json({ ok:false, error:'UNAUTHORIZED' });
    await ndspEnsureTelegramRoutesTable();

    const q = await pool.query(`
      SELECT plan_code, enabled, target_type, chat_id, daily_limit, description,
             last_test_ok, last_test_at, last_test_message, updated_at
      FROM ndsp_telegram_delivery_routes
      ORDER BY CASE plan_code
        WHEN 'pro' THEN 1
        WHEN 'elite' THEN 2
        WHEN 'saas' THEN 3
        WHEN 'institutional_suite' THEN 4
        WHEN 'free' THEN 5
        ELSE 99
      END
    `);

    const routes = q.rows.map(r => ({
      plan_code: r.plan_code,
      enabled: r.enabled,
      target_type: r.target_type,
      chat_id: r.chat_id,
      chat_id_masked: ndspMaskChat(r.chat_id),
      daily_limit: r.daily_limit,
      description: r.description,
      last_test_ok: r.last_test_ok,
      last_test_at: r.last_test_at,
      last_test_message: r.last_test_message,
      updated_at: r.updated_at
    }));

    res.json({
      ok:true,
      summary:{
        enabled_channels: routes.filter(x => x.enabled && x.plan_code !== 'free').length,
        configured_channels: routes.filter(x => x.chat_id && x.plan_code !== 'free').length,
        total_routes: routes.length
      },
      routes
    });
  } catch (e) {
    res.status(500).json({ ok:false, error:'TELEGRAM_ROUTING_STATUS_FAILED', detail:String(e.message || e) });
  }
});

app.post('/api/admin/telegram-routing/update', async (req, res) => {
  try {
    if (!ndspAdminOk(req)) return res.status(401).json({ ok:false, error:'UNAUTHORIZED' });
    await ndspEnsureTelegramRoutesTable();

    const plan = String(req.body.plan_code || '').trim().toLowerCase();
    const allowed = new Set(['free','pro','elite','saas','institutional_suite']);
    if (!allowed.has(plan)) return res.status(400).json({ ok:false, error:'INVALID_PLAN_CODE' });

    const enabled = !!req.body.enabled;
    const chat_id = plan === 'free' ? null : String(req.body.chat_id || '').trim();
    const daily_limit = req.body.daily_limit === null || req.body.daily_limit === '' || typeof req.body.daily_limit === 'undefined'
      ? null
      : Number(req.body.daily_limit);
    const description = String(req.body.description || '');

    if (plan !== 'free' && enabled && !chat_id) {
      return res.status(400).json({ ok:false, error:'CHAT_ID_REQUIRED_WHEN_ENABLED' });
    }

    const q = await pool.query(`
      INSERT INTO ndsp_telegram_delivery_routes
        (plan_code, enabled, target_type, chat_id, daily_limit, description)
      VALUES ($1,$2,$3,$4,$5,$6)
      ON CONFLICT (plan_code) DO UPDATE SET
        enabled=EXCLUDED.enabled,
        target_type=EXCLUDED.target_type,
        chat_id=EXCLUDED.chat_id,
        daily_limit=EXCLUDED.daily_limit,
        description=EXCLUDED.description,
        updated_at=now()
      RETURNING plan_code, enabled, target_type, chat_id, daily_limit, description, updated_at
    `, [
      plan,
      enabled,
      plan === 'free' ? 'none' : 'channel',
      plan === 'free' ? null : chat_id,
      daily_limit,
      description
    ]);

    const r = q.rows[0];
    res.json({ ok:true, route:{
      plan_code:r.plan_code,
      enabled:r.enabled,
      target_type:r.target_type,
      chat_id_masked:ndspMaskChat(r.chat_id),
      daily_limit:r.daily_limit,
      description:r.description,
      updated_at:r.updated_at
    }});
  } catch (e) {
    res.status(500).json({ ok:false, error:'TELEGRAM_ROUTING_UPDATE_FAILED', detail:String(e.message || e) });
  }
});

function ndspTelegramSend(token, chat_id, text) {
  return new Promise((resolve, reject) => {
    const data = new URLSearchParams({
      chat_id: String(chat_id),
      text: String(text),
      disable_web_page_preview: 'true'
    }).toString();

    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${token}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 15000
    }, resp => {
      let body = '';
      resp.on('data', chunk => body += chunk);
      resp.on('end', () => {
        try {
          resolve({ code: resp.statusCode, body: JSON.parse(body) });
        } catch (e) {
          resolve({ code: resp.statusCode, body: { ok:false, raw: body } });
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy(new Error('TELEGRAM_TIMEOUT'));
    });
    req.write(data);
    req.end();
  });
}

app.post('/api/admin/telegram-routing/test', async (req, res) => {
  try {
    if (!ndspAdminOk(req)) return res.status(401).json({ ok:false, error:'UNAUTHORIZED' });
    await ndspEnsureTelegramRoutesTable();

    const token = process.env.TELEGRAM_BOT_TOKEN;
    if (!token) return res.status(500).json({ ok:false, error:'TELEGRAM_BOT_TOKEN_MISSING' });

    const plan = String(req.body.plan_code || '').trim().toLowerCase();
    const q = await pool.query(
      `SELECT enabled, chat_id FROM ndsp_telegram_delivery_routes WHERE plan_code=$1 LIMIT 1`,
      [plan]
    );

    if (!q.rows.length) return res.status(404).json({ ok:false, error:'ROUTE_NOT_FOUND' });

    const row = q.rows[0];
    if (!row.enabled) return res.status(400).json({ ok:false, error:'ROUTE_DISABLED' });
    if (!row.chat_id) return res.status(400).json({ ok:false, error:'CHAT_ID_MISSING' });

    const text = String(req.body.text || `NDSP Admin Telegram Channel Test — ${plan.toUpperCase()} — ${new Date().toISOString()}`);
    const sent = await ndspTelegramSend(token, row.chat_id, text);
    const ok = !!(sent.body && sent.body.ok);
    const detail = ok ? 'تم الإرسال بنجاح' : JSON.stringify(sent.body);

    await pool.query(
      `UPDATE ndsp_telegram_delivery_routes
       SET last_test_ok=$1, last_test_at=now(), last_test_message=$2, updated_at=now()
       WHERE plan_code=$3`,
      [ok, detail.slice(0, 1000), plan]
    );

    if (!ok) return res.status(502).json({ ok:false, error:'TELEGRAM_SEND_FAILED', detail:sent.body });

    res.json({
      ok:true,
      http_code: sent.code,
      plan_code: plan,
      chat_id_masked: ndspMaskChat(row.chat_id),
      message: detail,
      telegram: {
        ok: sent.body.ok,
        message_id: sent.body.result && sent.body.result.message_id
      }
    });
  } catch (e) {
    res.status(500).json({ ok:false, error:'TELEGRAM_ROUTING_TEST_FAILED', detail:String(e.message || e) });
  }
});

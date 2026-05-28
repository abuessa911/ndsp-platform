require('dotenv').config();

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
       RETURNING id, name, email, plan, role, trial_day, trial_started_at, created_at`,
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
    `SELECT id, name, email, password_hash, plan, role, trial_day, trial_started_at, created_at
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
  res.json({ ok: true, user, token: tokenFor(user) });
});

app.get('/me', auth, async (req, res) => {
  const result = await pool.query(
    `SELECT id, name, email, plan, role, trial_day, trial_started_at, created_at
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
     RETURNING id, name, email, plan, role, status, trial_day, created_at`,
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
    `SELECT id, name, email, plan, role, status, trial_day, created_at
     FROM users
     ORDER BY created_at DESC
     LIMIT 100`
  );

  res.json({ ok: true, users: result.rows });
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

app.post('/api/admin/users/action', async (req, res) => {
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







app.listen(PORT, '127.0.0.1', () => {
  console.log(`NDSP Auth API listening on http://127.0.0.1:${PORT}`);
});

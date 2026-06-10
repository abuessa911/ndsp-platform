const express = require('express')
const fs = require('fs')
const https = require('https')
const jwt = require('jsonwebtoken')
const { Pool } = require('pg')

function loadEnvFile(file) {
  try {
    if (!fs.existsSync(file)) return
    const txt = fs.readFileSync(file, 'utf8')
    for (const line of txt.split(/\r?\n/)) {
      const x = line.trim()
      if (!x || x.startsWith('#') || !x.includes('=')) continue
      const i = x.indexOf('=')
      const k = x.slice(0, i).trim()
      let v = x.slice(i + 1).trim()
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1)
      if (!process.env[k]) process.env[k] = v
    }
  } catch (_) {}
}

loadEnvFile('/etc/ndsp/ndsp-db.env')
loadEnvFile('/etc/ndsp/ndsp-telegram.env')
loadEnvFile('/etc/ndsp/ndsp-session.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/auth_api/.env')

const PORT = Number(process.env.NDSP_ADMIN_UI_PROXY_PORT || 9023)
const DATABASE_URL = process.env.DATABASE_URL || process.env.NDSP_DATABASE_URL

const JWT_SECRETS = Array.from(new Set([
  process.env.JWT_SECRET,
  process.env.NDSP_JWT_SECRET,
  process.env.ADMIN_JWT_SECRET,
  process.env.NDSP_ADMIN_JWT_SECRET,
  process.env.SESSION_SECRET
].filter(Boolean)))

const pool = new Pool(DATABASE_URL ? { connectionString: DATABASE_URL } : undefined)
const app = express()
app.use(express.json({ limit: '1mb' }))

function send(res, code, body) {
  res.status(code).json(body)
}

function auth(req) {
  const h = req.headers.authorization || ''
  const token = h.startsWith('Bearer ') ? h.slice(7) : ''
  if (!token) return null
  for (const secret of JWT_SECRETS) {
    try { return jwt.verify(token, secret) } catch (_) {}
  }
  return null
}

function adminOnly(req, res, next) {
  const u = auth(req)
  if (!u) return send(res, 401, { ok:false, error:'AUTH_REQUIRED' })
  if (String(u.role || '').toLowerCase() !== 'admin') return send(res, 403, { ok:false, error:'ADMIN_REQUIRED' })
  req.user = u
  next()
}

async function tableExists(name) {
  const r = await pool.query(`
    SELECT EXISTS (
      SELECT 1 FROM information_schema.tables
      WHERE table_schema='public' AND table_name=$1
    ) ok
  `, [name])
  return !!r.rows[0]?.ok
}

async function columns(table) {
  const r = await pool.query(`
    SELECT column_name FROM information_schema.columns
    WHERE table_schema='public' AND table_name=$1
  `, [table])
  return new Set(r.rows.map(x => x.column_name))
}

function pick(cols, wanted, fallback='NULL') {
  for (const w of wanted) if (cols.has(w)) return w
  return fallback
}

async function safeCount(table) {
  try {
    if (!(await tableExists(table))) return 0
    const r = await pool.query(`SELECT COUNT(*)::int AS n FROM ${table}`)
    return Number(r.rows[0]?.n || 0)
  } catch (_) {
    return 0
  }
}

async function queryExistingTables(tables, limit=200) {
  for (const t of tables) {
    if (await tableExists(t)) {
      try {
        const hasCreated = (await columns(t)).has('created_at')
        const order = hasCreated ? 'ORDER BY created_at DESC NULLS LAST' : ''
        const r = await pool.query(`SELECT * FROM ${t} ${order} LIMIT ${limit}`)
        return { source_table:t, rows:r.rows }
      } catch (_) {
        return { source_table:t, rows:[] }
      }
    }
  }
  return { source_table:null, rows:[] }
}

async function updateByIdentity(table, statusValue, id, email, paymentId) {
  if (!(await tableExists(table))) return { table, updated:0, rows:[] }

  const cols = await columns(table)
  const statusCol = ['status','payment_status','state'].find(c => cols.has(c))
  if (!statusCol) return { table, updated:0, rows:[], skipped:'NO_STATUS_COLUMN' }

  const vals = [statusValue]
  const where = []

  function add(cond, val) {
    vals.push(String(val || ''))
    where.push(cond.replace('?', `$${vals.length}`))
  }

  if (id && cols.has('id')) add('id::text = ?', id)
  if (id && cols.has('user_id')) add('user_id::text = ?', id)
  if (paymentId && cols.has('payment_id')) add('payment_id::text = ?', paymentId)
  if (email && cols.has('email')) add('lower(email) = lower(?)', email)
  if (email && cols.has('user_email')) add('lower(user_email) = lower(?)', email)

  if (!where.length) return { table, updated:0, rows:[], skipped:'NO_MATCHING_IDENTITY_COLUMN' }

  const sql = `
    UPDATE ${table}
    SET ${statusCol} = $1
    WHERE ${where.join(' OR ')}
    RETURNING *
  `
  const r = await pool.query(sql, vals)
  return { table, updated:r.rowCount, rows:r.rows }
}

async function updateUserStatus(statusValue, id, email) {
  const r = await pool.query(`
    UPDATE users
    SET status=$3
    WHERE ($1::text <> '' AND id::text=$1)
       OR ($2::text <> '' AND lower(email)=lower($2))
    RETURNING id,email,role,status,plan
  `, [String(id || ''), String(email || ''), String(statusValue || '')])
  return { table:'users', updated:r.rowCount, rows:r.rows }
}


function ndspTelegramConfig() {
  const token =
    process.env.NDSP_TELEGRAM_BOT_TOKEN ||
    process.env.TELEGRAM_BOT_TOKEN ||
    process.env.TELEGRAM_TOKEN ||
    process.env.BOT_TOKEN ||
    ''

  const chatId =
    process.env.NDSP_TELEGRAM_CHAT_ID ||
    process.env.TELEGRAM_CHAT_ID ||
    process.env.ADMIN_TELEGRAM_CHAT_ID ||
    process.env.CHAT_ID ||
    ''

  return { token: String(token || ''), chatId: String(chatId || '') }
}

function ndspMaskSecret(v) {
  v = String(v || '')
  if (!v) return ''
  if (v.length <= 8) return '***'
  return v.slice(0, 4) + '***' + v.slice(-4)
}

function ndspTelegramRequest(method, body) {
  const cfg = ndspTelegramConfig()
  return new Promise((resolve) => {
    if (!cfg.token) return resolve({ ok:false, error:'TELEGRAM_TOKEN_MISSING' })

    const payload = JSON.stringify(body || {})
    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${cfg.token}/${method}`,
      method: 'POST',
      timeout: 8000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = ''
      res.on('data', chunk => data += chunk)
      res.on('end', () => {
        try {
          resolve(JSON.parse(data))
        } catch (_) {
          resolve({ ok:false, error:'BAD_TELEGRAM_RESPONSE', statusCode:res.statusCode })
        }
      })
    })

    req.on('timeout', () => {
      req.destroy()
      resolve({ ok:false, error:'TELEGRAM_TIMEOUT' })
    })

    req.on('error', (e) => resolve({ ok:false, error:'TELEGRAM_REQUEST_FAILED', message:e.message }))
    req.write(payload)
    req.end()
  })
}


const NDSP_ALERT_STATE_FILE = '/home/nawaf511/empire-core-new/backend/auth_api/ndsp_alert_channels_state.json'

function ndspReadAlertState() {
  try {
    if (!fs.existsSync(NDSP_ALERT_STATE_FILE)) {
      fs.writeFileSync(NDSP_ALERT_STATE_FILE, JSON.stringify({ in_app:true, email:true, telegram:true }, null, 2))
    }
    const raw = JSON.parse(fs.readFileSync(NDSP_ALERT_STATE_FILE, 'utf8'))
    return {
      in_app: raw.in_app !== false,
      email: raw.email !== false,
      telegram: raw.telegram !== false
    }
  } catch (_) {
    return { in_app:true, email:true, telegram:true }
  }
}

function ndspWriteAlertState(next) {
  const current = ndspReadAlertState()
  const merged = {
    in_app: typeof next.in_app === 'boolean' ? next.in_app : current.in_app,
    email: typeof next.email === 'boolean' ? next.email : current.email,
    telegram: typeof next.telegram === 'boolean' ? next.telegram : current.telegram
  }
  fs.writeFileSync(NDSP_ALERT_STATE_FILE, JSON.stringify(merged, null, 2))
  return merged
}

function ndspTelegramConfig() {
  const token =
    process.env.NDSP_TELEGRAM_BOT_TOKEN ||
    process.env.TELEGRAM_BOT_TOKEN ||
    process.env.TELEGRAM_TOKEN ||
    process.env.BOT_TOKEN ||
    ''

  const chatId =
    process.env.NDSP_TELEGRAM_CHAT_ID ||
    process.env.TELEGRAM_CHAT_ID ||
    process.env.ADMIN_TELEGRAM_CHAT_ID ||
    process.env.CHAT_ID ||
    ''

  return { token: String(token || ''), chatId: String(chatId || '') }
}

function ndspEmailConfigured() {
  return !!(
    (process.env.SMTP_HOST || process.env.NDSP_SMTP_HOST) &&
    (process.env.SMTP_USER || process.env.NDSP_SMTP_USER) &&
    (process.env.SMTP_PASS || process.env.NDSP_SMTP_PASS)
  )
}

function ndspTelegramRequest(method, body) {
  const cfg = ndspTelegramConfig()
  return new Promise((resolve) => {
    if (!cfg.token) return resolve({ ok:false, error:'TELEGRAM_TOKEN_MISSING' })

    const payload = JSON.stringify(body || {})
    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${cfg.token}/${method}`,
      method: 'POST',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = ''
      res.on('data', chunk => data += chunk)
      res.on('end', () => {
        try {
          resolve(JSON.parse(data))
        } catch (_) {
          resolve({ ok:false, error:'BAD_TELEGRAM_RESPONSE', statusCode:res.statusCode })
        }
      })
    })

    req.on('timeout', () => {
      req.destroy()
      resolve({ ok:false, error:'TELEGRAM_TIMEOUT' })
    })

    req.on('error', (e) => resolve({ ok:false, error:'TELEGRAM_REQUEST_FAILED', message:e.message }))
    req.write(payload)
    req.end()
  })
}

async function ndspInsertInAppNotification(userId, title, body) {
  try {
    if (!(await tableExists('notifications'))) return { inserted:false, reason:'NO_NOTIFICATIONS_TABLE' }

    const cols = await columns('notifications')
    const fields = []
    const vals = []
    const params = []

    function add(col, val) {
      if (cols.has(col)) {
        fields.push(col)
        vals.push(val)
        params.push(`$${vals.length}`)
      }
    }

    add('user_id', userId || null)
    add('title', title)
    add('message', body)
    add('body', body)
    add('type', 'admin_test')
    add('status', 'sent')
    add('created_at', new Date())

    if (!fields.length) return { inserted:false, reason:'NO_COMPATIBLE_COLUMNS' }

    const sql = `INSERT INTO notifications (${fields.join(',')}) VALUES (${params.join(',')}) RETURNING *`
    const r = await pool.query(sql, vals)
    return { inserted:true, row:r.rows[0] || null }
  } catch (e) {
    return { inserted:false, error:e.message }
  }
}

app.get('/api/admin-ui/health', adminOnly, async (_req, res) => {
  try {
    await pool.query('SELECT 1')
    send(res, 200, {
      ok:true,
      service:'ndsp-admin-ui-proxy',
      mode:'direct_db_safe_admin',
      database:'ok',
      secrets_exposed:false,
      timestamp:new Date().toISOString()
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'DB_ERROR', message:e.message })
  }
})

app.get('/api/admin-ui/summary', adminOnly, async (_req, res) => {
  try {
    const users = await safeCount('users')
    const trialA = await safeCount('ndsp_trial_activation_requests')
    const trialB = await safeCount('ndsp_trial_registrations')
    const paymentsA = await safeCount('ndsp_nowpayments_payments')
    const paymentsB = await safeCount('payments')
    const marketsA = await safeCount('markets')
    const assetsA = await safeCount('assets')

    send(res, 200, {
      ok:true,
      summary:{
        users,
        trials: trialA + trialB,
        payments: paymentsA + paymentsB,
        markets: marketsA,
        assets: assetsA,
        source:'database',
        secrets_exposed:false
      }
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'SUMMARY_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/users', adminOnly, async (_req, res) => {
  try {
    const cols = await columns('users')
    const q = `
      SELECT
        ${pick(cols, ['id'])} AS id,
        ${pick(cols, ['email'])} AS email,
        ${pick(cols, ['phone'])} AS phone,
        ${pick(cols, ['name','full_name'])} AS name,
        ${pick(cols, ['role'])} AS role,
        ${pick(cols, ['status'])} AS status,
        ${pick(cols, ['plan'])} AS plan,
        ${pick(cols, ['category'])} AS category,
        ${pick(cols, ['created_at'])} AS created_at,
        ${pick(cols, ['last_login_at','updated_at'])} AS last_login_at
      FROM users
      ORDER BY created_at DESC NULLS LAST
      LIMIT 300
    `
    const r = await pool.query(q)
    send(res, 200, { ok:true, source_table:'users', users:r.rows })
  } catch (e) {
    send(res, 500, { ok:false, error:'USERS_QUERY_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/payments', adminOnly, async (_req, res) => {
  try {
    const out = await queryExistingTables(['ndsp_nowpayments_payments','payments','payment_requests'], 200)
    send(res, 200, { ok:true, source_table:out.source_table, payments:out.rows })
  } catch (e) {
    send(res, 500, { ok:false, error:'PAYMENTS_QUERY_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/trials', adminOnly, async (_req, res) => {
  try {
    const tables = ['ndsp_trial_activation_requests','ndsp_trial_registrations','trial_requests']
    const out = {}
    for (const t of tables) {
      if (await tableExists(t)) {
        const hasCreated = (await columns(t)).has('created_at')
        const order = hasCreated ? 'ORDER BY created_at DESC NULLS LAST' : ''
        const r = await pool.query(`SELECT * FROM ${t} ${order} LIMIT 200`).catch(() => ({ rows:[] }))
        out[t] = r.rows
      }
    }
    send(res, 200, { ok:true, trials:out })
  } catch (e) {
    send(res, 500, { ok:false, error:'TRIALS_QUERY_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/packages', adminOnly, async (_req, res) => {
  try {
    const out = await queryExistingTables(['packages','plans','subscription_plans'], 200)
    const fallback = [
      { code:'free', name:'Free', status:'configured' },
      { code:'pro', name:'Pro', status:'configured' },
      { code:'elite', name:'Elite', status:'configured' },
      { code:'institutional', name:'Institutional Suite', status:'configured' }
    ]
    send(res, 200, {
      ok:true,
      source_table:out.source_table || 'governance_policy',
      packages:out.rows.length ? out.rows : fallback,
      fallback_used:!out.rows.length
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'PACKAGES_QUERY_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/markets', adminOnly, async (_req, res) => {
  try {
    const markets = await queryExistingTables(['markets'], 300)
    const assets = await queryExistingTables(['assets','market_assets','symbols'], 300)
    send(res, 200, {
      ok:true,
      markets_source_table:markets.source_table,
      assets_source_table:assets.source_table,
      markets:markets.rows,
      assets:assets.rows
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'MARKETS_QUERY_FAILED', message:e.message })
  }
})



app.get('/api/admin-ui/alerts', adminOnly, async (_req, res) => {
  try {
    const cfg = ndspTelegramConfig()
    const channelState = ndspReadAlertState()
    const telegramConfigured = !!(cfg.token && cfg.chatId)
    const emailConfigured = ndspEmailConfigured()
    const notifications = await queryExistingTables(['notifications'], 200)

    send(res, 200, {
      ok:true,
      alerts:{
        channels:{
          in_app:{
            label:'داخل المنصة',
            configured:true,
            enabled:channelState.in_app,
            active:channelState.in_app
          },
          email:{
            label:'البريد',
            configured:emailConfigured,
            enabled:channelState.email,
            active:emailConfigured && channelState.email
          },
          telegram:{
            label:'تيليجرام',
            configured:telegramConfigured,
            enabled:channelState.telegram,
            active:telegramConfigured && channelState.telegram,
            token_present:!!cfg.token,
            chat_present:!!cfg.chatId
          }
        },
        in_app:channelState.in_app,
        email:emailConfigured && channelState.email,
        telegram:telegramConfigured && channelState.telegram,
        telegram_configured:telegramConfigured,
        email_configured:emailConfigured,
        secrets_masked:true,
        source_table:notifications.source_table,
        recent_notifications:notifications.rows
      }
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'ALERTS_QUERY_FAILED', message:e.message })
  }
})

app.post('/api/admin-ui/alerts/channel', adminOnly, async (req, res) => {
  try {
    const channel = String(req.body?.channel || '')
    const enabled = req.body?.enabled === true

    if (!['in_app','email','telegram'].includes(channel)) {
      return send(res, 400, { ok:false, error:'INVALID_CHANNEL' })
    }

    const next = {}
    next[channel] = enabled
    const state = ndspWriteAlertState(next)

    send(res, 200, {
      ok:true,
      channel,
      enabled:state[channel],
      state,
      secrets_masked:true
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'CHANNEL_UPDATE_FAILED', message:e.message })
  }
})

app.post('/api/admin-ui/alerts/test', adminOnly, async (req, res) => {
  try {
    const channel = String(req.body?.channel || '')
    const state = ndspReadAlertState()

    if (!['in_app','email','telegram'].includes(channel)) {
      return send(res, 400, { ok:false, error:'INVALID_CHANNEL' })
    }

    if (channel === 'telegram') {
      const cfg = ndspTelegramConfig()
      if (!cfg.token || !cfg.chatId) {
        return send(res, 400, {
          ok:false,
          error:'TELEGRAM_NOT_CONFIGURED',
          token_present:!!cfg.token,
          chat_present:!!cfg.chatId,
          secrets_masked:true
        })
      }

      if (!state.telegram) {
        return send(res, 400, { ok:false, error:'TELEGRAM_DISABLED', secrets_masked:true })
      }

      const result = await ndspTelegramRequest('sendMessage', {
        chat_id: cfg.chatId,
        text: 'NDSP اختبار تنبيه حقيقي: قناة تيليجرام مفعّلة وتعمل.',
        disable_web_page_preview: true
      })

      if (!result.ok) {
        return send(res, 502, {
          ok:false,
          error:'TELEGRAM_TEST_FAILED',
          telegram_error:result.description || result.error || 'UNKNOWN',
          secrets_masked:true
        })
      }

      return send(res, 200, { ok:true, channel, message:'TELEGRAM_TEST_SENT', secrets_masked:true })
    }

    if (channel === 'in_app') {
      if (!state.in_app) return send(res, 400, { ok:false, error:'IN_APP_DISABLED' })

      const inserted = await ndspInsertInAppNotification(
        req.user?.sub || null,
        'NDSP اختبار تنبيه',
        'تم إرسال اختبار تنبيه داخل المنصة من لوحة الإدارة.'
      )

      return send(res, 200, {
        ok:true,
        channel,
        message:'IN_APP_TEST_DONE',
        inserted,
        secrets_masked:true
      })
    }

    if (channel === 'email') {
      const configured = ndspEmailConfigured()
      if (!configured) {
        return send(res, 400, {
          ok:false,
          error:'EMAIL_SMTP_NOT_CONFIGURED',
          message:'SMTP settings are missing. Email cannot be tested until SMTP is configured.',
          secrets_masked:true
        })
      }

      if (!state.email) return send(res, 400, { ok:false, error:'EMAIL_DISABLED' })

      return send(res, 200, {
        ok:true,
        channel,
        message:'EMAIL_CONFIGURED_BUT_SEND_ADAPTER_NOT_INSTALLED',
        note:'SMTP exists, but no email sender adapter is installed in this proxy.',
        secrets_masked:true
      })
    }
  } catch (e) {
    send(res, 500, { ok:false, error:'ALERT_TEST_FAILED', message:e.message })
  }
})



app.get('/api/admin-ui/backups', adminOnly, async (_req, res) => {
  try {
    const dirs = [
      '/home/nawaf511/ndsp_launch_reports',
      '/home/nawaf511/ndsp_backups',
      '/home/nawaf511/ndsp_snapshots'
    ]
    const out = {}
    for (const d of dirs) {
      try {
        out[d] = fs.readdirSync(d).slice(-40).reverse()
      } catch (_) {
        out[d] = []
      }
    }
    send(res, 200, { ok:true, files:out, secrets_exposed:false })
  } catch (e) {
    send(res, 500, { ok:false, error:'BACKUPS_FAILED', message:e.message })
  }
})

app.get('/api/admin-ui/governance', adminOnly, async (_req, res) => {
  send(res, 200, {
    ok:true,
    governance:{
      platform:'NDSP — منصة نواف لدعم القرار',
      mode:'Decision Active',
      execution:'Execution Sanitized',
      visible_layers:['TDL','NMP',"Devil's Advocate",'Nawaf Golden Alignment'],
      protected_layers_count:12,
      public_output_sanitized:true,
      secrets_exposed:false,
      raw_logic_exposed:false
    }
  })
})

app.post('/api/admin-ui/action', adminOnly, async (req, res) => {
  const { action, id, email, payment_id, plan, status } = req.body || {}

  try {
    if (['activate_user','approve_user','approve','review_approve'].includes(action)) {
      const u = await updateUserStatus('active', id, email)
      const t1 = await updateByIdentity('ndsp_trial_activation_requests', 'approved', id, email, payment_id)
      const t2 = await updateByIdentity('ndsp_trial_registrations', 'approved', id, email, payment_id)
      return send(res, 200, { ok:true, action, results:[u,t1,t2] })
    }

    if (['block_user','reject_user','reject','disable_user','review_reject'].includes(action)) {
      const u = await updateUserStatus('blocked', id, email)
      const t1 = await updateByIdentity('ndsp_trial_activation_requests', 'rejected', id, email, payment_id)
      const t2 = await updateByIdentity('ndsp_trial_registrations', 'rejected', id, email, payment_id)
      return send(res, 200, { ok:true, action, results:[u,t1,t2] })
    }

    if (action === 'set_plan') {
      const r = await pool.query(`
        UPDATE users
        SET plan=$3
        WHERE ($1::text <> '' AND id::text=$1)
           OR ($2::text <> '' AND lower(email)=lower($2))
        RETURNING id,email,role,status,plan
      `, [String(id || ''), String(email || ''), String(plan || '')])
      return send(res, 200, { ok:true, action, updated:r.rows })
    }

    if (action === 'set_status') {
      const u = await updateUserStatus(status || 'active', id, email)
      return send(res, 200, { ok:true, action, results:[u] })
    }

    if (action === 'approve_payment') {
      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'approved', id, email, payment_id)
      const p2 = await updateByIdentity('payments', 'approved', id, email, payment_id)
      const p3 = await updateByIdentity('payment_requests', 'approved', id, email, payment_id)
      return send(res, 200, { ok:true, action, results:[p1,p2,p3] })
    }

    if (action === 'reject_payment') {
      const p1 = await updateByIdentity('ndsp_nowpayments_payments', 'rejected', id, email, payment_id)
      const p2 = await updateByIdentity('payments', 'rejected', id, email, payment_id)
      const p3 = await updateByIdentity('payment_requests', 'rejected', id, email, payment_id)
      return send(res, 200, { ok:true, action, results:[p1,p2,p3] })
    }

    send(res, 400, { ok:false, error:'UNSUPPORTED_ACTION', action })
  } catch (e) {
    send(res, 500, { ok:false, error:'ACTION_FAILED', action, message:e.message })
  }
})

app.use((_req, res) => send(res, 404, { ok:false, error:'NOT_FOUND' }))

app.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] admin ui proxy production routes listening on 127.0.0.1:${PORT}`)
})

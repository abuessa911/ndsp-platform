const express = require('express')
const fs = require('fs')
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
loadEnvFile('/etc/ndsp/ndsp-session.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/auth_api/.env')


const PORT = Number(process.env.NDSP_API_COMPAT_PORT || 9022)
const JWT_SECRET = process.env.JWT_SECRET || process.env.NDSP_JWT_SECRET || process.env.ADMIN_JWT_SECRET || process.env.NDSP_ADMIN_JWT_SECRET || process.env.SESSION_SECRET || 'change-me'
const JWT_SECRETS = Array.from(new Set([process.env.JWT_SECRET, process.env.NDSP_JWT_SECRET, process.env.ADMIN_JWT_SECRET, process.env.NDSP_ADMIN_JWT_SECRET, process.env.SESSION_SECRET, JWT_SECRET].filter(Boolean)))
const DATABASE_URL = process.env.DATABASE_URL || process.env.NDSP_DATABASE_URL

const app = express()
app.use(express.json({ limit: '1mb' }))

const pool = new Pool(DATABASE_URL ? { connectionString: DATABASE_URL } : undefined)

function send(res, code, body) {
  res.status(code).json(body)
}

function maskEmail(email) {
  if (!email || !email.includes('@')) return email || ''
  const [a, b] = email.split('@')
  return `${a.slice(0, 2)}***@${b}`
}

function authOptional(req) {
  const h = req.headers.authorization || ''
  const token = h.startsWith('Bearer ') ? h.slice(7) : ''
  if (!token) return null
  for (const secret of JWT_SECRETS) {
    try { return jwt.verify(token, secret) } catch (_) {}
  }
  return null
}

function authRequired(req, res, next) {
  const user = authOptional(req)
  if (!user) return send(res, 401, { ok:false, error:'AUTH_REQUIRED' })
  req.user = user
  next()
}

async function tableExists(name) {
  const r = await pool.query(
    `SELECT EXISTS (
       SELECT 1 FROM information_schema.tables
       WHERE table_schema='public' AND table_name=$1
     ) AS ok`, [name]
  )
  return !!r.rows[0]?.ok
}

app.get('/health', async (_req, res) => {
  try {
    await pool.query('SELECT 1')
    send(res, 200, {
      ok:true,
      service:'ndsp-api-compat',
      routes:[
        '/api/account/trial',
        '/api/packages',
        '/api/markets',
        '/api/alerts/status',
        '/api/payments/status'
      ]
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'DB_ERROR', message:e.message })
  }
})

app.get('/api/account/trial', authRequired, async (req, res) => {
  try {
    const r = await pool.query(`
      SELECT id,email,role,status,plan,trial_day,trial_started_at,trial_ends_at,activated_at,created_at
      FROM users
      WHERE id::text=$1 OR lower(email)=lower($2)
      LIMIT 1
    `, [String(req.user.sub || ''), String(req.user.email || '')])

    if (!r.rowCount) return send(res, 404, { ok:false, error:'USER_NOT_FOUND' })

    const u = r.rows[0]
    const plan = String(u.plan || '').toLowerCase()
    const started = u.trial_started_at || u.activated_at || new Date().toISOString()
    const ends = u.trial_ends_at || (started ? new Date(new Date(started).getTime() + 16*86400000) : null)
    const now = new Date()
    const daysLeft = ends ? Math.max(0, Math.ceil((new Date(ends).getTime() - now.getTime()) / 86400000)) : null

    send(res, 200, {
      ok:true,
      account:{
        id:u.id,
        email:maskEmail(u.email),
        role:u.role,
        status:u.status,
        plan:u.plan
      },
      trial:{
        active: plan.includes('trial') || String(u.status || '').toLowerCase() === 'active',
        day: u.trial_day || null,
        duration_days:16,
        started_at: started,
        ends_at: ends,
        days_left: daysLeft
      }
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'TRIAL_STATUS_FAILED', message:e.message })
  }
})

app.get('/api/packages', async (_req, res) => {
  try {
    let rows = []
    if (await tableExists('ndsp_plans')) {
      const r = await pool.query(`
        SELECT code,name,price,description,trial_days,features,limits,is_active
        FROM ndsp_plans
        ORDER BY id ASC
      `)
      rows = r.rows
    } else if (await tableExists('plans')) {
      const r = await pool.query(`SELECT * FROM plans ORDER BY id ASC LIMIT 50`)
      rows = r.rows
    }

    if (!rows.length) {
      rows = [
        { code:'free', name:'Free', price:0, is_active:true },
        { code:'pro', name:'Pro', price:99, is_active:true },
        { code:'elite', name:'Elite', price:249, is_active:true },
        { code:'institutional', name:'Institutional Suite', price:null, is_active:true }
      ]
    }

    send(res, 200, { ok:true, packages:rows })
  } catch (e) {
    send(res, 500, { ok:false, error:'PACKAGES_FAILED', message:e.message })
  }
})

app.get('/api/markets', async (_req, res) => {
  try {
    let rows = []
    if (await tableExists('ndsp_market_assets')) {
      const r = await pool.query(`SELECT * FROM ndsp_market_assets ORDER BY 1 ASC LIMIT 300`)
      rows = r.rows
    } else if (await tableExists('ndsp_assets')) {
      const r = await pool.query(`SELECT * FROM ndsp_assets ORDER BY 1 ASC LIMIT 300`)
      rows = r.rows
    }

    send(res, 200, {
      ok:true,
      source: rows.length ? 'database' : 'safe_fallback',
      markets: rows.length ? rows : [
        { market:'crypto', symbol:'BTCUSDT', name:'Bitcoin' },
        { market:'crypto', symbol:'ETHUSDT', name:'Ethereum' },
        { market:'metals', symbol:'XAUUSD', name:'Gold' },
        { market:'forex', symbol:'EURUSD', name:'Euro Dollar' },
        { market:'energy', symbol:'USOIL', name:'US Oil' }
      ]
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'MARKETS_FAILED', message:e.message })
  }
})

app.get('/api/alerts/status', authRequired, async (req, res) => {
  try {
    let notificationCount = 0
    if (await tableExists('notifications')) {
      const r = await pool.query(
        `SELECT count(*)::int AS c FROM notifications WHERE user_id::text=$1`,
        [String(req.user.sub || '')]
      ).catch(() => ({ rows:[{c:0}] }))
      notificationCount = r.rows[0]?.c || 0
    }

    send(res, 200, {
      ok:true,
      alerts:{
        in_app:true,
        email:true,
        telegram:false,
        secrets_masked:true,
        notification_count:notificationCount,
        policy:'sanitized_decision_notifications_only'
      }
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'ALERTS_STATUS_FAILED', message:e.message })
  }
})

app.get('/api/payments/status', authRequired, async (req, res) => {
  try {
    let rows = []
    if (await tableExists('ndsp_nowpayments_payments')) {
      const r = await pool.query(`
        SELECT payment_id, plan, status, created_at
        FROM ndsp_nowpayments_payments
        WHERE lower(email)=lower($1)
        ORDER BY created_at DESC
        LIMIT 10
      `, [String(req.user.email || '')]).catch(() => ({ rows:[] }))
      rows = r.rows
    }

    send(res, 200, {
      ok:true,
      provider:'nowpayments',
      auto_activation:false,
      payments:rows,
      message:'Payments require admin/manual review before activation.'
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'PAYMENTS_STATUS_FAILED', message:e.message })
  }
})

app.use((_req, res) => send(res, 404, { ok:false, error:'NOT_FOUND' }))

app.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] api compat gateway listening on 127.0.0.1:${PORT}`)
})

const express = require('express')
const http = require('http')
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
loadEnvFile('/home/nawaf511/.config/ndsp/backend.env')
loadEnvFile('/home/nawaf511/.config/ndsp/auth_api.env')


const PORT = Number(process.env.NDSP_API_COMPAT_PORT || 9022)
const JWT_SECRET = process.env.JWT_SECRET || process.env.NDSP_JWT_SECRET || process.env.ADMIN_JWT_SECRET || process.env.NDSP_ADMIN_JWT_SECRET || process.env.SESSION_SECRET || 'change-me'
const JWT_SECRETS = Array.from(new Set([process.env.JWT_SECRET, process.env.NDSP_JWT_SECRET, process.env.ADMIN_JWT_SECRET, process.env.NDSP_ADMIN_JWT_SECRET, process.env.SESSION_SECRET, JWT_SECRET].filter(Boolean)))
const DATABASE_URL = process.env.DATABASE_URL || process.env.NDSP_DATABASE_URL
const PUBLIC_PLANS_CONTRACT = process.env.NDSP_PUBLIC_PLANS_CONTRACT || '/home/nawaf511/ndsp-current/contracts/ndsp_public_plans_v1.json'

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

function normalizePublicPlan(value) {
  const s = String(value || '').trim().toLowerCase()

  if (!s) return 'FREE'

  if (['free','starter','basic'].includes(s)) return 'FREE'

  if ([
    'pro',
    'professional',
    'paid_pro'
  ].includes(s)) return 'PRO'

  if ([
    'elite',
    'premium',
    'trial',
    'trial_elite',
    'elite_trial'
  ].includes(s)) return 'ELITE'

  if (
    s === 'saas' ||
    s === 'institutional' ||
    s === 'institutional_suite' ||
    s === 'enterprise' ||
    s.includes('saas') ||
    s.includes('enterprise')
  ) return 'SAAS'

  return 'FREE'
}

function canonicalTrialState(user, ends, daysLeft) {
  const rawPlan = String(user?.plan || '').toLowerCase()
  const rawStatus = String(user?.status || '').toLowerCase()

  const trialSignal =
    rawPlan.includes('trial') ||
    rawStatus.includes('trial')

  const active =
    trialSignal &&
    !!ends &&
    Number(daysLeft || 0) > 0

  return active ? 'ELITE_TRIAL' : 'NONE'
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

function sessionFromLocalAuth(req) {
  return new Promise((resolve) => {
    const headers = {
      accept: 'application/json'
    }

    if (req.headers.cookie) {
      headers.cookie = req.headers.cookie
    }

    const request = http.request(
      {
        hostname: '127.0.0.1',
        port: 9020,
        method: 'GET',
        path: '/api/auth/session',
        headers,
        timeout: 5000
      },
      response => {
        let raw = ''

        response.setEncoding('utf8')

        response.on('data', chunk => {
          if (raw.length < 1024 * 1024) raw += chunk
        })

        response.on('end', () => {
          if (response.statusCode !== 200) {
            resolve(null)
            return
          }

          try {
            const data = JSON.parse(raw)

            const user =
              data?.user && typeof data.user === 'object'
                ? data.user
                : data

            if (!user || typeof user !== 'object') {
              resolve(null)
              return
            }

            const id =
              user.id ||
              user.user_id ||
              user.sub ||
              data?.sub ||
              ''

            const email =
              user.email ||
              user.user_email ||
              data?.email ||
              ''

            if (!id && !email) {
              resolve(null)
              return
            }

            resolve({
              ...user,
              sub: user.sub || id,
              id: id || user.id || '',
              email
            })
          } catch (_) {
            resolve(null)
          }
        })
      }
    )

    request.on('timeout', () => {
      request.destroy()
      resolve(null)
    })

    request.on('error', () => {
      resolve(null)
    })

    request.end()
  })
}

async function authRequired(req, res, next) {
  const bearerUser = authOptional(req)

  if (bearerUser) {
    req.user = bearerUser
    return next()
  }

  const sessionUser = await sessionFromLocalAuth(req)

  if (!sessionUser) {
    return send(res, 401, {
      ok:false,
      error:'AUTH_REQUIRED'
    })
  }

  req.user = sessionUser
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


const NDSP_SAFE_DECISION_INTERNAL_URL =
  'http://127.0.0.1:9082/api/decision/quality-live';

const NDSP_SAFE_CHART_INTERNAL_URL =
  'http://127.0.0.1:9095/api/market/candles';

const NDSP_SAFE_TIMEFRAMES = new Set([
  '1m',
  '5m',
  '15m',
  '30m',
  '1h',
  '4h',
  '1d',
  '1w',
  'daily',
  'weekly'
]);

function ndspSafeSymbol(value) {
  const symbol = String(value || '')
    .trim()
    .toUpperCase();

  if (!/^[A-Z0-9._:-]{2,24}$/.test(symbol)) {
    return null;
  }

  return symbol;
}

function ndspSafeTimeframe(value, fallback) {
  const tf = String(value || fallback || '')
    .trim()
    .toLowerCase();

  return NDSP_SAFE_TIMEFRAMES.has(tf)
    ? tf
    : String(fallback || '1h');
}

function ndspSafeNumber(value) {
  if (
    value === null ||
    value === undefined ||
    value === ''
  ) {
    return null;
  }

  const n = Number(value);

  return Number.isFinite(n)
    ? n
    : null;
}

function ndspLocalJson(url, timeoutMs = 7000) {
  return new Promise((resolve, reject) => {
    const request = http.get(
      url,
      {
        headers: {
          'Accept': 'application/json',
          'User-Agent': 'NDSP-safe-boundary/1.0'
        }
      },
      response => {
        let body = '';

        response.setEncoding('utf8');

        response.on('data', chunk => {
          body += chunk;

          if (body.length > 5 * 1024 * 1024) {
            request.destroy(
              new Error('UPSTREAM_RESPONSE_TOO_LARGE')
            );
          }
        });

        response.on('end', () => {
          const status = Number(
            response.statusCode || 502
          );

          if (status < 200 || status >= 300) {
            reject(
              new Error(
                'UPSTREAM_HTTP_' + status
              )
            );
            return;
          }

          try {
            resolve(JSON.parse(body));
          } catch (_) {
            reject(
              new Error('UPSTREAM_INVALID_JSON')
            );
          }
        });
      }
    );

    request.setTimeout(
      timeoutMs,
      () => {
        request.destroy(
          new Error('UPSTREAM_TIMEOUT')
        );
      }
    );

    request.on(
      'error',
      reject
    );
  });
}

function ndspCanonicalDecisionDto(
  upstream,
  requestedSymbol,
  requestedTimeframe
) {
  const instrument =
    upstream &&
    typeof upstream.instrument === 'object'
      ? upstream.instrument
      : {};

  const decision =
    upstream &&
    typeof upstream.decision === 'object'
      ? upstream.decision
      : {};

  const scenario =
    upstream &&
    typeof upstream.scenario === 'object'
      ? upstream.scenario
      : {};

  const sourceDecision =
    Object.keys(decision).length
      ? decision
      : scenario;

  return {
    ok: true,

    project: 'NDSP — منصة دعم القرار',

    instrument: {
      symbol:
        String(
          instrument.symbol ||
          requestedSymbol
        ).toUpperCase(),

      market:
        instrument.market
          ? String(instrument.market)
          : null,

      timeframe:
        instrument.timeframe
          ? String(instrument.timeframe)
          : requestedTimeframe,

      live_price:
        ndspSafeNumber(
          instrument.live_price
        )
    },

    decision: {
      scenario_state:
        sourceDecision.scenario_state ??
        upstream.scenario_state ??
        null,

      directional_context:
        sourceDecision.directional_context ??
        sourceDecision.scenario_directional_context ??
        upstream.directional_context ??
        null,

      decision_quality:
        ndspSafeNumber(
          upstream.decision_quality ??
          upstream.quality ??
          sourceDecision.decision_quality ??
          sourceDecision.quality
        ),

      levels: {
        activation:
          ndspSafeNumber(
            sourceDecision.activation ??
            sourceDecision.scenario_activation_level ??
            upstream.activation
          ),

        arrival:
          ndspSafeNumber(
            sourceDecision.arrival ??
            sourceDecision.scenario_arrival_level ??
            upstream.arrival
          ),

        review:
          sourceDecision.review ??
          sourceDecision.scenario_review_zone ??
          upstream.review ??
          null,

        invalidation:
          ndspSafeNumber(
            sourceDecision.invalidation ??
            sourceDecision.scenario_invalidation_level ??
            upstream.invalidation
          )
      }
    },

    message:
      'NDSP is a decision-support platform, not a trading or recommendation platform.'
  };
}

function ndspCanonicalChartDto(
  upstream,
  requestedSymbol,
  requestedTimeframe,
  requestedCount
) {
  const source =
    Array.isArray(upstream?.candles)
      ? upstream.candles
      : [];

  const candles = source
    .slice(-requestedCount)
    .map(row => ({
      time:
        ndspSafeNumber(
          row?.time ??
          row?.timestamp
        ),

      open:
        ndspSafeNumber(row?.open),

      high:
        ndspSafeNumber(row?.high),

      low:
        ndspSafeNumber(row?.low),

      close:
        ndspSafeNumber(row?.close),

      volume:
        ndspSafeNumber(row?.volume)
    }))
    .filter(row => row.time !== null);

  return {
    ok: true,
    symbol:
      String(
        upstream?.symbol ||
        requestedSymbol
      ).toUpperCase(),

    timeframe:
      String(
        upstream?.timeframe ||
        requestedTimeframe
      ),

    count:
      candles.length,

    candles
  };
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
    const started = u.trial_started_at || u.activated_at || null

    const ends = u.trial_ends_at || (
      started
        ? new Date(new Date(started).getTime() + 16*86400000)
        : null
    )

    const now = new Date()

    const daysLeft = ends
      ? Math.max(
          0,
          Math.ceil(
            (new Date(ends).getTime() - now.getTime()) / 86400000
          )
        )
      : null

    const publicPlan = normalizePublicPlan(u.plan)
    const trialState = canonicalTrialState(u, ends, daysLeft)

    send(res, 200, {
      ok:true,
      account:{
        id:String(u.id),
        email:maskEmail(u.email),
        role:String(u.role || 'user'),
        status:String(u.status || ''),
        plan:publicPlan
      },
      entitlement:{
        plan:publicPlan,
        state:trialState
      },
      trial:{
        active:trialState === 'ELITE_TRIAL',
        state:trialState,
        duration_days:16,
        started_at:started,
        ends_at:ends,
        days_left:daysLeft
      }
    })
  } catch (e) {
    send(res, 500, { ok:false, error:'TRIAL_STATUS_FAILED', message:e.message })
  }
})

app.get('/api/packages', async (_req, res) => {
  try {
    if (!fs.existsSync(PUBLIC_PLANS_CONTRACT)) {
      return send(res, 503, {
        ok:false,
        error:'PLANS_CONTRACT_UNAVAILABLE'
      })
    }

    const raw = fs.readFileSync(PUBLIC_PLANS_CONTRACT, 'utf8')
    const contract = JSON.parse(raw)

    if (!Array.isArray(contract.plans) || contract.plans.length !== 4) {
      return send(res, 503, {
        ok:false,
        error:'PLANS_CONTRACT_INVALID'
      })
    }

    const expected = ['FREE','PRO','ELITE','SAAS']
    const actual = contract.plans.map(x => String(x.id || '').toUpperCase())

    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      return send(res, 503, {
        ok:false,
        error:'PLANS_CONTRACT_INVALID'
      })
    }

    send(res, 200, {
      ok:true,
      currency:contract.currency || 'SAR',
      trial:contract.trial || null,
      plans:contract.plans
    })
  } catch (_) {
    send(res, 503, {
      ok:false,
      error:'PLANS_CONTRACT_UNAVAILABLE'
    })
  }
})

app.get('/api/markets', async (_req, res) => {
  try {
    let rows = []

    if (await tableExists('ndsp_market_assets')) {
      const r = await pool.query(`
        SELECT id,symbol,name_ar,name_en,category,is_active,sort_order
        FROM ndsp_market_assets
        WHERE is_active=true
        ORDER BY sort_order ASC, id ASC
        LIMIT 300
      `)
      rows = r.rows
    } else if (await tableExists('ndsp_assets')) {
      const r = await pool.query(`
        SELECT id,symbol,name_ar,name_en,category,is_active,sort_order
        FROM ndsp_assets
        WHERE is_active=true
        ORDER BY sort_order ASC, id ASC
        LIMIT 300
      `)
      rows = r.rows
    }

    if (!rows.length) {
      return send(res, 503, {
        ok:false,
        error:'MARKETS_UNAVAILABLE'
      })
    }

    const markets = rows.map(row => ({
      id: String(row.id),
      symbol: row.symbol,
      name_ar: row.name_ar || '',
      name_en: row.name_en || '',
      category: row.category || '',
      is_active: Boolean(row.is_active),
      sort_order: Number(row.sort_order || 0)
    }))

    send(res, 200, {
      ok:true,
      markets
    })
  } catch (_) {
    send(res, 503, {
      ok:false,
      error:'MARKETS_UNAVAILABLE'
    })
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


app.get('/api/decision/live', authRequired, async (req, res) => {
  try {
    const symbol =
      ndspSafeSymbol(req.query.symbol);

    if (!symbol) {
      return send(res, 400, {
        ok:false,
        error:'INVALID_SYMBOL'
      });
    }

    const timeframe =
      ndspSafeTimeframe(
        req.query.timeframe,
        'weekly'
      );

    const url =
      new URL(
        NDSP_SAFE_DECISION_INTERNAL_URL
      );

    url.searchParams.set(
      'symbol',
      symbol
    );

    url.searchParams.set(
      'timeframe',
      timeframe
    );

    const upstream =
      await ndspLocalJson(
        url.toString()
      );

    return send(
      res,
      200,
      ndspCanonicalDecisionDto(
        upstream,
        symbol,
        timeframe
      )
    );

  } catch (_) {
    return send(res, 502, {
      ok:false,
      error:'DECISION_TEMPORARILY_UNAVAILABLE'
    });
  }
});


app.get('/api/chart/candles', authRequired, async (req, res) => {
  try {
    const symbol =
      ndspSafeSymbol(req.query.symbol);

    if (!symbol) {
      return send(res, 400, {
        ok:false,
        error:'INVALID_SYMBOL'
      });
    }

    const timeframe =
      ndspSafeTimeframe(
        req.query.timeframe,
        '1h'
      );

    const parsedCount =
      Number.parseInt(
        String(req.query.count || '100'),
        10
      );

    const count =
      Number.isFinite(parsedCount)
        ? Math.max(
            20,
            Math.min(
              300,
              parsedCount
            )
          )
        : 100;

    const url =
      new URL(
        NDSP_SAFE_CHART_INTERNAL_URL
      );

    url.searchParams.set(
      'symbol',
      symbol
    );

    url.searchParams.set(
      'timeframe',
      timeframe
    );

    url.searchParams.set(
      'count',
      String(count)
    );

    const upstream =
      await ndspLocalJson(
        url.toString()
      );

    return send(
      res,
      200,
      ndspCanonicalChartDto(
        upstream,
        symbol,
        timeframe,
        count
      )
    );

  } catch (_) {
    return send(res, 502, {
      ok:false,
      error:'CHART_TEMPORARILY_UNAVAILABLE'
    });
  }
});

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

    const payments = rows.map(row => ({
      id: String(row.payment_id || ''),
      plan: normalizePublicPlan(row.plan),
      status: String(row.status || ''),
      created_at: row.created_at || null
    }))

    send(res, 200, {
      ok:true,
      auto_activation:false,
      activation_policy:'trusted_server_validation_only',
      payments
    })
  } catch (_) {
    send(res, 500, {
      ok:false,
      error:'PAYMENTS_STATUS_FAILED'
    })
  }
})

app.use((_req, res) => send(res, 404, { ok:false, error:'NOT_FOUND' }))

app.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] api compat gateway listening on 127.0.0.1:${PORT}`)
})

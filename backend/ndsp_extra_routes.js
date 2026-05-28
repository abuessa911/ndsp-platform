// NDSP Extra Routes — Seats + Market Data
// يستخدم pool منفصل لـ ndsp_auth DB
'use strict';
const { Pool } = require('pg');
const crypto   = require('crypto');
const https    = require('https');
const WebSocket = require('ws');

// Pool لـ ndsp_auth (يقرأ من ENV)
const authPool = new Pool({
  host:     process.env.PGHOST     || '127.0.0.1',
  port:     parseInt(process.env.PGPORT || '5432'),
  database: process.env.PGDATABASE || 'ndsp_auth',
  user:     process.env.PGUSER     || 'ndsp_auth',
  password: process.env.PGPASSWORD || process.env.DB_PASSWORD,
});

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Seats Routes
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function installSeatRoutes(app, authFn) {

  // حالة المقاعد — عام
  app.get('/api/seats/status', async (req, res) => {
    try {
      const { rows } = await authPool.query('SELECT * FROM ndsp_seats_status');
      res.json({ ok: true, seats: rows.map(r => ({
        code: r.code, name_ar: r.name_ar, name_en: r.name_en,
        available: r.available_seats, total: r.total_seats,
        fill_pct: r.fill_pct, full: r.available_seats <= 0
      }))});
    } catch(e) { res.status(500).json({ ok: false, error: e.message }); }
  });

  // تسجيل مقعد
  app.post('/api/trial/register', authFn(), async (req, res) => {
    const { segmentCode, invitationCode } = req.body;
    if (!['academic','beginner','premium'].includes(segmentCode))
      return res.status(400).json({ ok: false, error: 'INVALID_SEGMENT' });

    const userEmail = req.user.email;
    const userId    = String(req.user.id);

    try {
      // هل مسجّل مسبقاً؟
      const dup = await authPool.query(
        `SELECT id FROM ndsp_trial_seat_assignments
         WHERE lower(user_email)=lower($1) AND status='reserved'`,
        [userEmail]
      );
      if (dup.rows[0]) return res.status(409).json({ ok: false, error: 'ALREADY_REGISTERED' });

      // مقاعد متاحة؟
      const { rows } = await authPool.query(
        'SELECT available_seats FROM ndsp_seats_status WHERE code=$1', [segmentCode]
      );
      if (!rows[0] || rows[0].available_seats <= 0)
        return res.status(409).json({ ok: false, error: 'SEATS_FULL' });

      // Premium: تحقق من رمز الدعوة
      if (segmentCode === 'premium') {
        if (!invitationCode) return res.status(400).json({ ok: false, error: 'INVITATION_REQUIRED' });
        const inv = await authPool.query(
          `SELECT id FROM ndsp_invitation_codes
           WHERE code=$1 AND cohort_code='premium' AND used_by_email IS NULL
             AND (expires_at IS NULL OR expires_at > NOW())`,
          [invitationCode]
        );
        if (!inv.rows[0]) return res.status(400).json({ ok: false, error: 'INVALID_INVITATION' });
        await authPool.query(
          'UPDATE ndsp_invitation_codes SET used_by_email=$1, used_at=NOW() WHERE code=$2',
          [userEmail, invitationCode]
        );
      }

      // إدراج في ndsp_trial_seat_assignments
      await authPool.query(
        `INSERT INTO ndsp_trial_seat_assignments
           (user_id, user_email, cohort_code, status, notes)
         VALUES ($1,$2,$3,'reserved',$4)`,
        [userId, userEmail, segmentCode, invitationCode ? `inv:${invitationCode}` : '']
      );

      const cnt = await authPool.query(
        `SELECT COUNT(*) AS c FROM ndsp_trial_seat_assignments
         WHERE cohort_code=$1 AND status='reserved'`,
        [segmentCode]
      );
      const seatNumber = parseInt(cnt.rows[0].c, 10);
      const trialEnd   = new Date(Date.now() + 16 * 86400_000);

      res.json({ ok: true, segmentCode, seatNumber, trialEnd });
    } catch(e) { res.status(500).json({ ok: false, error: e.message }); }
  });

  // UI State (trial info)
  app.get('/api/ui-state', authFn(), async (req, res) => {
    try {
      const { rows } = await authPool.query(
        `SELECT a.cohort_code, a.assigned_at,
                p.max_seats,
                EXTRACT(DAY FROM (a.assigned_at + INTERVAL '16 days' - NOW()))::INT AS days_left
         FROM ndsp_trial_seat_assignments a
         JOIN ndsp_trial_seat_policy p ON p.cohort_code = a.cohort_code
         WHERE lower(a.user_email)=lower($1) AND a.status='reserved'`,
        [req.user.email]
      );
      const seat = rows[0];
      const daysLeft = seat ? Math.max(0, seat.days_left) : null;
      res.json({
        ok: true,
        isTrialUser: !!seat,
        segmentCode: seat?.cohort_code || null,
        daysLeft,
        trialEnd: seat ? new Date(new Date(seat.assigned_at).getTime() + 16*86400_000) : null,
        showFeedbackPrompt: daysLeft !== null && daysLeft <= 2,
        showPayment: !seat,
      });
    } catch(e) { res.status(500).json({ ok: false, error: e.message }); }
  });

  // ── Admin Seats ──
  app.get('/api/admin/seats', authFn(), async (req, res) => {
    if (req.user.role !== 'admin') return res.status(403).json({ ok: false, error: 'ADMIN_ONLY' });
    const { rows } = await authPool.query('SELECT * FROM ndsp_seats_status');
    res.json({ ok: true, seats: rows });
  });

  app.post('/api/admin/invitations/create', authFn(), async (req, res) => {
    if (req.user.role !== 'admin') return res.status(403).json({ ok: false, error: 'ADMIN_ONLY' });
    const { segmentCode, count, notes } = req.body;
    const codes = [];
    for (let i = 0; i < Math.min(count||1, 50); i++) {
      const code = `NDSP-${segmentCode.toUpperCase()}-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
      await authPool.query(
        `INSERT INTO ndsp_invitation_codes (code, cohort_code, created_by, notes)
         VALUES ($1,$2,$3,$4)`,
        [code, segmentCode, req.user.email, notes||null]
      );
      codes.push(code);
    }
    res.json({ ok: true, codes });
  });

  app.get('/api/admin/invitations/:segment', authFn(), async (req, res) => {
    if (req.user.role !== 'admin') return res.status(403).json({ ok: false, error: 'ADMIN_ONLY' });
    const { rows } = await authPool.query(
      `SELECT * FROM ndsp_invitation_codes WHERE cohort_code=$1 ORDER BY created_at DESC`,
      [req.params.segment]
    );
    res.json({ ok: true, invitations: rows });
  });

  app.get('/api/admin/users/trial', authFn(), async (req, res) => {
    if (req.user.role !== 'admin') return res.status(403).json({ ok: false, error: 'ADMIN_ONLY' });
    const { rows } = await authPool.query(
      `SELECT a.*, p.cohort_label_ar AS segment_name
       FROM ndsp_trial_seat_assignments a
       JOIN ndsp_trial_seat_policy p ON p.cohort_code = a.cohort_code
       WHERE a.status='reserved' ORDER BY a.assigned_at DESC`
    );
    res.json({ ok: true, users: rows });
  });

  log('[Seats] routes installed ✓');
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Market Routes
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function installMarketRoutes(app) {

  app.get('/api/market/prices', async (req, res) => {
    try {
      const { rows } = await authPool.query(
        `SELECT a.symbol,a.name_ar,a.name_en,a.category,a.source,
                p.price,p.change_24h,p.change_pct,p.high_24h,p.low_24h,p.volume,p.updated_at
         FROM ndsp_market_assets a
         LEFT JOIN ndsp_price_cache p ON p.symbol=a.symbol
         WHERE a.is_active ORDER BY a.sort_order`
      );
      res.json({ ok: true, prices: rows });
    } catch(e) { res.status(500).json({ ok: false, error: e.message }); }
  });

  app.get('/api/market/prices/:category', async (req, res) => {
    try {
      const { rows } = await authPool.query(
        `SELECT a.symbol,a.name_ar,a.name_en,a.category,a.source,
                p.price,p.change_24h,p.change_pct,p.updated_at
         FROM ndsp_market_assets a
         LEFT JOIN ndsp_price_cache p ON p.symbol=a.symbol
         WHERE a.is_active AND a.category=$1 ORDER BY a.sort_order`,
        [req.params.category]
      );
      res.json({ ok: true, prices: rows });
    } catch(e) { res.status(500).json({ ok: false, error: e.message }); }
  });

  app.post('/api/admin/assets', async (req, res) => {
    const { symbol, name_ar, name_en, category, source } = req.body;
    await authPool.query(
      `INSERT INTO ndsp_market_assets (symbol,name_ar,name_en,category,source)
       VALUES ($1,$2,$3,$4,$5)
       ON CONFLICT (symbol) DO UPDATE SET
         name_ar=EXCLUDED.name_ar, name_en=EXCLUDED.name_en,
         category=EXCLUDED.category, source=EXCLUDED.source`,
      [symbol, name_ar, name_en, category, source]
    );
    res.json({ ok: true });
  });

  log('[Market] routes installed ✓');
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Binance Feed
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function startBinanceFeed() {
  const SYMS = ['BTCUSDT','ETHUSDT','XRPUSDT','SOLUSDT','BNBUSDT','ADAUSDT'];
  let rt;
  function connect() {
    const ws = new WebSocket(
      `wss://stream.binance.com:9443/stream?streams=${SYMS.map(s=>s.toLowerCase()+'@ticker').join('/')}`
    );
    ws.on('open',  () => { console.log('[Binance] ✓'); if(rt){clearTimeout(rt);rt=null;} });
    ws.on('close', () => { console.warn('[Binance] retry'); rt=setTimeout(connect,5000); });
    ws.on('error', e  => console.error('[Binance]', e.message));
    ws.on('message', async raw => {
      try {
        const { data: d } = JSON.parse(raw);
        if (!d?.s) return;
        await authPool.query(
          `INSERT INTO ndsp_price_cache(symbol,price,change_24h,change_pct,high_24h,low_24h,volume,source,updated_at)
           VALUES($1,$2,$3,$4,$5,$6,$7,'binance',NOW())
           ON CONFLICT(symbol) DO UPDATE SET
             price=EXCLUDED.price,change_24h=EXCLUDED.change_24h,change_pct=EXCLUDED.change_pct,
             high_24h=EXCLUDED.high_24h,low_24h=EXCLUDED.low_24h,volume=EXCLUDED.volume,
             source='binance',updated_at=NOW()`,
          [d.s,d.c,parseFloat(d.p),parseFloat(d.P),d.h,d.l,d.v]
        );
      } catch(e){ console.error('[Binance msg]', e.message); }
    });
  }
  connect();
  log('[Binance] feed started ✓');
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Yahoo Feed (Gold, Silver, Oil, Indices)
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function startYahooFeed() {
  const SYMS = ['GC=F','SI=F','CL=F','^GSPC','^IXIC','^DJI'];

  function fetchQ(sym) {
    return new Promise(res => {
      const req = https.get({
        hostname: 'query1.finance.yahoo.com',
        path: `/v8/finance/chart/${encodeURIComponent(sym)}?interval=1d&range=1d`,
        headers: { 'User-Agent': 'Mozilla/5.0', Accept: 'application/json' }
      }, r => {
        let b = '';
        r.on('data', c => b += c);
        r.on('end', () => {
          try {
            const m = JSON.parse(b)?.chart?.result?.[0]?.meta;
            if (!m?.regularMarketPrice) return res(null);
            const p = m.regularMarketPrice, pv = m.previousClose || p;
            res({ sym, p, ch: p - pv, pct: ((p-pv)/pv)*100,
                  h: m.regularMarketDayHigh, l: m.regularMarketDayLow, v: m.regularMarketVolume });
          } catch { res(null); }
        });
      });
      req.on('error', () => res(null));
      req.setTimeout(8000, () => { req.destroy(); res(null); });
    });
  }

  async function poll() {
    for (const s of SYMS) {
      const q = await fetchQ(s);
      if (!q) continue;
      await authPool.query(
        `INSERT INTO ndsp_price_cache(symbol,price,change_24h,change_pct,high_24h,low_24h,volume,source,updated_at)
         VALUES($1,$2,$3,$4,$5,$6,$7,'yahoo',NOW())
         ON CONFLICT(symbol) DO UPDATE SET
           price=EXCLUDED.price,change_24h=EXCLUDED.change_24h,change_pct=EXCLUDED.change_pct,
           high_24h=EXCLUDED.high_24h,low_24h=EXCLUDED.low_24h,volume=EXCLUDED.volume,
           source='yahoo',updated_at=NOW()`,
        [q.sym, q.p, q.ch.toFixed(6), q.pct.toFixed(4), q.h, q.l, q.v]
      ).catch(e => console.error('[Yahoo DB]', s, e.message));
    }
  }

  poll(); setInterval(poll, 60_000);
  log('[Yahoo] feed started ✓');
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// FXCM/Yahoo Forex Feed
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
function startFxcmFeed() {
  const PAIRS = { 'EUR/USD':'EURUSD=X','GBP/USD':'GBPUSD=X','USD/JPY':'USDJPY=X','USD/SAR':'USDSAR=X' };

  function fetchFx(pair) {
    const sym = PAIRS[pair];
    return new Promise(res => {
      const req = https.get({
        hostname: 'query1.finance.yahoo.com',
        path: `/v8/finance/chart/${encodeURIComponent(sym)}?interval=1d&range=1d`,
        headers: { 'User-Agent': 'Mozilla/5.0', Accept: 'application/json' }
      }, r => {
        let b = '';
        r.on('data', c => b += c);
        r.on('end', () => {
          try {
            const m = JSON.parse(b)?.chart?.result?.[0]?.meta;
            if (!m?.regularMarketPrice) return res(null);
            const p = m.regularMarketPrice, pv = m.previousClose || p;
            res({ pair, p, ch: (p-pv).toFixed(6), pct: (((p-pv)/pv)*100).toFixed(4),
                  h: m.regularMarketDayHigh, l: m.regularMarketDayLow });
          } catch { res(null); }
        });
      });
      req.on('error', () => res(null));
      req.setTimeout(8000, () => { req.destroy(); res(null); });
    });
  }

  async function poll() {
    for (const pair of Object.keys(PAIRS)) {
      const q = await fetchFx(pair);
      if (!q) continue;
      await authPool.query(
        `INSERT INTO ndsp_price_cache(symbol,price,change_24h,change_pct,high_24h,low_24h,source,updated_at)
         VALUES($1,$2,$3,$4,$5,$6,'fxcm',NOW())
         ON CONFLICT(symbol) DO UPDATE SET
           price=EXCLUDED.price,change_24h=EXCLUDED.change_24h,change_pct=EXCLUDED.change_pct,
           high_24h=EXCLUDED.high_24h,low_24h=EXCLUDED.low_24h,source='fxcm',updated_at=NOW()`,
        [pair, q.p, q.ch, q.pct, q.h, q.l]
      ).catch(e => console.error('[FXCM]', pair, e.message));
    }
  }

  poll(); setInterval(poll, 30_000);
  log('[FXCM/Yahoo] feed started ✓');
}

function log(msg) { console.log('[NDSP-Extra]', msg); }

module.exports = { installSeatRoutes, installMarketRoutes, startBinanceFeed, startYahooFeed, startFxcmFeed };

'use strict'

const express = require('express')
const crypto = require('crypto')
const fs = require('fs')
const path = require('path')
const { Pool } = require('pg')
const jwt = require('jsonwebtoken')

function loadEnvFile(file) {
  try {
    if (!fs.existsSync(file)) return
    const txt = fs.readFileSync(file, 'utf8')
    for (const line of txt.split(/\r?\n/)) {
      const s = line.trim()
      if (!s || s.startsWith('#') || !s.includes('=')) continue
      const idx = s.indexOf('=')
      const k = s.slice(0, idx).trim()
      let v = s.slice(idx + 1).trim()
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1)
      if (!process.env[k]) process.env[k] = v
    }
  } catch (_) {}
}

loadEnvFile('/etc/ndsp/ndsp-db.env')
loadEnvFile('/etc/ndsp/ndsp-auth.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/.env')
loadEnvFile('/home/nawaf511/empire-core-new/backend/auth_api/.env')

const PORT = Number(process.env.NDSP_USER_LOGIN_PORT || process.env.PORT || 9020)
const DATABASE_URL =
  process.env.DATABASE_URL ||
  process.env.NDSP_DATABASE_URL ||
  process.env.POSTGRES_URL ||
  process.env.DB_URL

const JWT_SECRET =
  process.env.JWT_SECRET ||
  process.env.NDSP_JWT_SECRET ||
  process.env.ADMIN_JWT_SECRET ||
  process.env.NDSP_ADMIN_JWT_SECRET

if (!DATABASE_URL) {
  console.error('[NDSP 2FA] DATABASE_URL missing')
}
if (!JWT_SECRET) {
  console.error('[NDSP 2FA] JWT_SECRET missing')
}

const pool = new Pool({ connectionString: DATABASE_URL })

const app = express()


app.use(express.json({ limit: '1mb' }))

function send(res, status, obj) {
  return res.status(status).json(obj)
}

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase()
}

function timingSafeEq(a, b) {
  const aa = Buffer.from(String(a || ''))
  const bb = Buffer.from(String(b || ''))
  if (aa.length !== bb.length) return false
  return crypto.timingSafeEqual(aa, bb)
}

function verifyPassword(password, stored) {
  try {
    if (!password || !stored) return false;
    const raw = String(stored || '');

    if (raw.startsWith('$2a$') || raw.startsWith('$2b$') || raw.startsWith('$2y$')) {
      const bcrypt = require('bcryptjs');
      return bcrypt.compareSync(String(password), raw);
    }

    if (raw.startsWith('pbkdf2_sha256$')) {
      const parts = raw.split('$');
      if (parts.length !== 4) return false;
      const iterations = parseInt(parts[1], 10);
      const salt = parts[2];
      const expected = parts[3];
      const crypto = require('crypto');
      const dk = crypto.pbkdf2Sync(String(password), String(salt), iterations, 32, 'sha256').toString('hex');
      return dk === expected;
    }

    return false;
  } catch (e) {
    return false;
  }
}


function signToken(user) {
  return jwt.sign(
    {
      sub: String(user.id),
      email: user.email,
      role: user.role || 'user',
      plan: user.plan || null,
    },
    JWT_SECRET,
    { expiresIn: '7d' }
  )
}

function auth(req, res, next) {
  const h = String(req.headers.authorization || '')
  const token = h.startsWith('Bearer ') ? h.slice(7) : String(req.headers['x-ndsp-token'] || '')
  if (!token) return send(res, 401, { ok: false, error: 'AUTH_REQUIRED' })
  try {
    req.user = jwt.verify(token, JWT_SECRET)
    return next()
  } catch (_) {
    return send(res, 401, { ok: false, error: 'INVALID_TOKEN' })
  }
}

function base32Encode(buf) {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
  let bits = 0
  let value = 0
  let output = ''
  for (const byte of buf) {
    value = (value << 8) | byte
    bits += 8
    while (bits >= 5) {
      output += alphabet[(value >>> (bits - 5)) & 31]
      bits -= 5
    }
  }
  if (bits > 0) output += alphabet[(value << (5 - bits)) & 31]
  return output
}

function base32Decode(input) {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
  const clean = String(input || '').replace(/=+$/g, '').replace(/\s+/g, '').toUpperCase()
  let bits = 0
  let value = 0
  const out = []
  for (const ch of clean) {
    const idx = alphabet.indexOf(ch)
    if (idx < 0) continue
    value = (value << 5) | idx
    bits += 5
    if (bits >= 8) {
      out.push((value >>> (bits - 8)) & 255)
      bits -= 8
    }
  }
  return Buffer.from(out)
}

function hotp(secretBase32, counter) {
  const key = base32Decode(secretBase32)
  const msg = Buffer.alloc(8)
  msg.writeBigUInt64BE(BigInt(counter))
  const hmac = crypto.createHmac('sha1', key).update(msg).digest()
  const offset = hmac[hmac.length - 1] & 0xf
  const code =
    ((hmac[offset] & 0x7f) << 24) |
    ((hmac[offset + 1] & 0xff) << 16) |
    ((hmac[offset + 2] & 0xff) << 8) |
    (hmac[offset + 3] & 0xff)
  return String(code % 1000000).padStart(6, '0')
}

function verifyTotp(secret, code, window = 1) {
  const c = String(code || '').replace(/\D/g, '')
  if (c.length !== 6) return false
  const step = Math.floor(Date.now() / 1000 / 30)
  for (let i = -window; i <= window; i++) {
    if (timingSafeEq(hotp(secret, step + i), c)) return true
  }
  return false
}

function hashRecovery(code) {
  return crypto.createHash('sha256').update(String(code)).digest('hex')
}

function makeRecoveryCodes() {
  const codes = []
  for (let i = 0; i < 8; i++) {
    codes.push(crypto.randomBytes(5).toString('hex').toUpperCase())
  }
  return codes
}

async function ensure2faRow(userId) {
  await pool.query(
    `INSERT INTO user_2fa_settings (user_id, enabled, method)
     VALUES ($1, false, 'totp')
     ON CONFLICT (user_id) DO NOTHING`,
    [userId]
  )
}

async function getUserByEmail(email) {
  const r = await pool.query(
    `SELECT id,email,name,password_hash,plan,role,status,phone,email_verified,review_status,requested_segment,approved_segment,trial_segment,account_type,trial_started_at,trial_ends_at,trial_days,activated_at,created_at
     FROM users
     WHERE lower(email)=lower($1)
     LIMIT 1`,
    [email]
  )
  return r.rows[0] || null
}

async function getUserById(id) {
  const r = await pool.query(
    `SELECT id,email,name,plan,role,status,phone
     FROM users
     WHERE id=$1
     LIMIT 1`,
    [id]
  )
  return r.rows[0] || null
}

app.get('/api/auth/login/health', (_req, res) => {
  send(res, 200, {
    ok: true,
    service: 'ndsp-user-login',
    two_factor: 'optional_totp',
    timestamp: new Date().toISOString(),
  })
})

app.post('/api/auth/login', async (req, res) => {
  try {
    const email = normalizeEmail(req.body && req.body.email)
    const password = String((req.body && req.body.password) || '')

    if (!email || !password) {
      return send(res, 400, { ok: false, error: 'EMAIL_PASSWORD_REQUIRED', message: 'البريد وكلمة المرور مطلوبة.' })
    }

    const user = await getUserByEmail(email)
    if (!user || !verifyPassword(password, user.password_hash)) {
      return send(res, 401, { ok: false, error: 'INVALID_CREDENTIALS', message: 'البريد أو كلمة المرور غير صحيحة.' })
    }

    if (String(user.status || '').toLowerCase() !== 'active') {
      return send(res, 403, { ok: false, error: 'ACCOUNT_NOT_ACTIVE', message: 'الحساب غير مفعل.' })
    }

    await ensure2faRow(user.id)

    const two = await pool.query(`SELECT enabled FROM user_2fa_settings WHERE user_id=$1 LIMIT 1`, [user.id])
    const twoEnabled = !!(two.rows[0] && two.rows[0].enabled)

    if (twoEnabled) {
      const challenge = crypto.randomBytes(24).toString('hex')
      await pool.query(
        `UPDATE user_2fa_settings
         SET updated_at=now()
         WHERE user_id=$1`,
        [user.id]
      )
      const tmp = jwt.sign(
        { sub: String(user.id), email: user.email, purpose: '2fa_login', challenge },
        JWT_SECRET,
        { expiresIn: '5m' }
      )
      return send(res, 200, {
        ok: true,
        require_2fa: true,
        two_factor_required: ndspUserHas2FA(user),
        method: 'totp',
        challenge_token: tmp,
        message: 'TWO_FACTOR_REQUIRED',
      })
    }

    const token = signToken(user)
    
      try {
        const dspLoginUserId =
          (typeof user !== 'undefined' && user && user.id) ||
          (typeof dbUser !== 'undefined' && dbUser && dbUser.id) ||
          (typeof row !== 'undefined' && row && row.id) ||
          (typeof found !== 'undefined' && found && found.id) ||
          null;

        if (dspLoginUserId && typeof pool !== 'undefined' && pool && typeof pool.query === 'function') {
          await pool.query('SELECT ndsp_start_trial_on_first_login($1::uuid)', [dspLoginUserId]);
        }
      } catch (e) {
        console.error('[DSP] first-login trial hook failed:', e && e.message ? e.message : e);
      }

return send(res, 200, {
      ok: true,
      message: 'LOGIN_OK',
      token,
      user: {
        id: String(user.id),
        email: user.email,
        name: user.name || '',
        role: user.role || 'user',
        plan: user.plan || null,
        status: user.status || null,
      },
      redirect: '/pages/dashboard.html',
    })
  } catch (e) {
    console.error('[NDSP login error]', e)
    return send(res, 500, { ok: false, error: 'LOGIN_FAILED' })
  }
})

app.post('/api/auth/2fa/login/verify', async (req, res) => {
  try {
    const challengeToken = String(req.body && (req.body.challenge_token || req.body.challengeToken) || '')
    const code = String(req.body && req.body.code || '')

    if (!challengeToken || !code) return send(res, 400, { ok: false, error: 'CHALLENGE_AND_CODE_REQUIRED' })

    let payload
    try {
      payload = jwt.verify(challengeToken, JWT_SECRET)
    } catch (_) {
      return send(res, 401, { ok: false, error: 'INVALID_OR_EXPIRED_CHALLENGE' })
    }

    if (payload.purpose !== '2fa_login') return send(res, 401, { ok: false, error: 'INVALID_CHALLENGE_PURPOSE' })

    const user = await getUserById(payload.sub)
    if (!user) return send(res, 404, { ok: false, error: 'USER_NOT_FOUND' })

    const r = await pool.query(`SELECT enabled, totp_secret, recovery_hashes FROM user_2fa_settings WHERE user_id=$1 LIMIT 1`, [user.id])
    const row = r.rows[0]
    if (!row || !row.enabled) return send(res, 400, { ok: false, error: 'TWO_FACTOR_NOT_ENABLED' })

    let ok = verifyTotp(row.totp_secret, code)

    if (!ok) {
      const hashes = Array.isArray(row.recovery_hashes) ? row.recovery_hashes : []
      const h = hashRecovery(code)
      if (hashes.includes(h)) {
        ok = true
        const remaining = hashes.filter(x => x !== h)
        await pool.query(`UPDATE user_2fa_settings SET recovery_hashes=$2::jsonb, updated_at=now() WHERE user_id=$1`, [user.id, JSON.stringify(remaining)])
      }
    }

    if (!ok) return send(res, 401, { ok: false, error: 'INVALID_2FA_CODE' })

    await pool.query(`UPDATE user_2fa_settings SET last_verified_at=now(), updated_at=now() WHERE user_id=$1`, [user.id])

    const token = signToken(user)
    
      try {
        const dspLoginUserId =
          (typeof user !== 'undefined' && user && user.id) ||
          (typeof dbUser !== 'undefined' && dbUser && dbUser.id) ||
          (typeof row !== 'undefined' && row && row.id) ||
          (typeof found !== 'undefined' && found && found.id) ||
          null;

        if (dspLoginUserId && typeof pool !== 'undefined' && pool && typeof pool.query === 'function') {
          await pool.query('SELECT ndsp_start_trial_on_first_login($1::uuid)', [dspLoginUserId]);
        }
      } catch (e) {
        console.error('[DSP] first-login trial hook failed:', e && e.message ? e.message : e);
      }

return send(res, 200, {
      ok: true,
      message: 'LOGIN_OK',
      token,
      user: {
        id: String(user.id),
        email: user.email,
        name: user.name || '',
        role: user.role || 'user',
        plan: user.plan || null,
        status: user.status || null,
      },
      redirect: '/pages/dashboard.html',
    })
  } catch (e) {
    console.error('[NDSP 2FA verify error]', e)
    return send(res, 500, { ok: false, error: 'TWO_FACTOR_VERIFY_FAILED' })
  }
})

app.get('/api/auth/session', auth, async (req, res) => {
  const user = await getUserById(req.user.sub)
  if (!user) return send(res, 404, { ok: false, error: 'USER_NOT_FOUND' })
  return send(res, 200, { ok: true, user })
})

app.post('/api/auth/logout', (_req, res) => {
  return send(res, 200, { ok: true, message: 'LOGOUT_OK' })
})

app.get('/api/auth/2fa/status', auth, async (req, res) => {
  try {
    await ensure2faRow(req.user.sub)
    const r = await pool.query(
      `SELECT enabled, method, created_at, updated_at, last_verified_at
       FROM user_2fa_settings
       WHERE user_id=$1
       LIMIT 1`,
      [req.user.sub]
    )
    const row = r.rows[0] || {}
    return send(res, 200, {
      ok: true,
      two_factor: {
        enabled: !!row.enabled,
        method: row.method || 'totp',
        created_at: row.created_at || null,
        updated_at: row.updated_at || null,
        last_verified_at: row.last_verified_at || null,
      },
    })
  } catch (e) {
    console.error('[NDSP 2FA status error]', e)
    return send(res, 500, { ok: false, error: 'TWO_FACTOR_STATUS_FAILED' })
  }
})

app.post('/api/auth/2fa/setup', auth, async (req, res) => {
  try {
    const user = await getUserById(req.user.sub)
    if (!user) return send(res, 404, { ok: false, error: 'USER_NOT_FOUND' })

    const secret = base32Encode(crypto.randomBytes(20))
    const recoveryCodes = makeRecoveryCodes()
    const hashes = recoveryCodes.map(hashRecovery)
    await pool.query(
      `INSERT INTO user_2fa_settings (user_id, enabled, method, totp_secret, recovery_hashes, updated_at)
       VALUES ($1, false, 'totp', $2, $3::jsonb, now())
       ON CONFLICT (user_id)
       DO UPDATE SET enabled=false, method='totp', totp_secret=$2, recovery_hashes=$3::jsonb, updated_at=now()`,
      [user.id, secret, JSON.stringify(hashes)]
    )

    const issuer = 'NDSP'
    const label = encodeURIComponent(`${issuer}:${user.email}`)
    const uri = `otpauth://totp/${label}?secret=${secret}&issuer=${encodeURIComponent(issuer)}&algorithm=SHA1&digits=6&period=30`

    return send(res, 200, {
      ok: true,
      method: 'totp',
      secret,
      otpauth_uri: uri,
      recovery_codes: recoveryCodes,
      message: 'Scan or enter secret in Google Authenticator / Microsoft Authenticator, then confirm with a 6-digit code.',
    })
  } catch (e) {
    console.error('[NDSP 2FA setup error]', e)
    return send(res, 500, { ok: false, error: 'TWO_FACTOR_SETUP_FAILED' })
  }
})

app.post('/api/auth/2fa/confirm', auth, async (req, res) => {
  try {
    const code = String(req.body && req.body.code || '')
    const r = await pool.query(`SELECT totp_secret FROM user_2fa_settings WHERE user_id=$1 LIMIT 1`, [req.user.sub])
    const row = r.rows[0]
    if (!row || !row.totp_secret) return send(res, 400, { ok: false, error: 'TWO_FACTOR_SETUP_REQUIRED' })
    if (!verifyTotp(row.totp_secret, code)) return send(res, 401, { ok: false, error: 'INVALID_2FA_CODE' })

    await pool.query(
      `UPDATE user_2fa_settings
       SET enabled=true, last_verified_at=now(), updated_at=now()
       WHERE user_id=$1`,
      [req.user.sub]
    )

    return send(res, 200, { ok: true, enabled: true, message: 'TWO_FACTOR_ENABLED' })
  } catch (e) {
    console.error('[NDSP 2FA confirm error]', e)
    return send(res, 500, { ok: false, error: 'TWO_FACTOR_CONFIRM_FAILED' })
  }
})

app.post('/api/auth/2fa/disable', auth, async (req, res) => {
  try {
    const code = String(req.body && req.body.code || '')
    const r = await pool.query(`SELECT enabled, totp_secret FROM user_2fa_settings WHERE user_id=$1 LIMIT 1`, [req.user.sub])
    const row = r.rows[0]
    if (!row || !row.enabled) {
      await ensure2faRow(req.user.sub)
      return send(res, 200, { ok: true, enabled: false, message: 'TWO_FACTOR_ALREADY_DISABLED' })
    }

    if (!verifyTotp(row.totp_secret, code)) return send(res, 401, { ok: false, error: 'INVALID_2FA_CODE' })

    await pool.query(
      `UPDATE user_2fa_settings
       SET enabled=false, updated_at=now()
       WHERE user_id=$1`,
      [req.user.sub]
    )
    return send(res, 200, { ok: true, enabled: false, message: 'TWO_FACTOR_DISABLED' })
  } catch (e) {
    console.error('[NDSP 2FA disable error]', e)
    return send(res, 500, { ok: false, error: 'TWO_FACTOR_DISABLE_FAILED' })
  }
})












// NDSP_2FA_SINGLE_CANONICAL_BEGIN
const ndsp2faOtplib = require('otplib');
const ndsp2faQRCode = require('qrcode');
const ndsp2faAuth = ndsp2faOtplib.authenticator || ndsp2faOtplib.totp || ndsp2faOtplib;

function ndsp2faGenerateSecret() {
  if (ndsp2faAuth && typeof ndsp2faAuth.generateSecret === 'function') {
    return ndsp2faAuth.generateSecret();
  }
  const crypto = require('crypto');
  return crypto.randomBytes(20).toString('hex').toUpperCase();
}

function ndsp2faKeyuri(email, issuer, secret) {
  if (ndsp2faAuth && typeof ndsp2faAuth.keyuri === 'function') {
    return ndsp2faAuth.keyuri(email, issuer, secret);
  }
  const label = encodeURIComponent(`${issuer}:${email}`);
  return `otpauth://totp/${label}?secret=${encodeURIComponent(secret)}&issuer=${encodeURIComponent(issuer)}`;
}

function ndsp2faCheck(code, secret) {
  if (ndsp2faAuth && typeof ndsp2faAuth.check === 'function') {
    return ndsp2faAuth.check(String(code || '').replace(/\s+/g,''), secret);
  }
  return false;
}

function ndsp2faActive(user) {
  return Boolean(
    user &&
    (user.two_factor_enabled === true || user.two_factor_enabled === 'true' || user.two_factor_enabled === 1) &&
    user.two_factor_secret &&
    String(user.two_factor_secret).trim().length >= 8
  );
}

async function ndsp2faEnsureColumns() {
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_enabled boolean DEFAULT false`);
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_secret text`);
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_confirmed_at timestamptz`);
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_setup_required boolean DEFAULT true`);
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_skipped_at timestamptz`);
  await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS two_factor_last_prompt_at timestamptz`);
}

app.post('/api/auth/2fa/status', async (req, res) => {
  try {
    await ndsp2faEnsureColumns();
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    if (!email) return res.status(400).json({ ok:false, error:'EMAIL_REQUIRED' });

    const q = await pool.query(
      `SELECT email,two_factor_enabled,two_factor_secret,two_factor_confirmed_at,two_factor_skipped_at,two_factor_setup_required
       FROM users WHERE lower(email)=lower($1) LIMIT 1`,
      [email]
    );

    if (!q.rows.length) return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });

    const u = q.rows[0];
    return res.json({
      ok:true,
      email,
      two_factor_enabled: ndsp2faActive(u),
      skipped: Boolean(u.two_factor_skipped_at),
      confirmed_at: u.two_factor_confirmed_at || null,
      can_setup_later: true
    });
  } catch(e) {
    return res.status(500).json({ ok:false, error:'TWO_FACTOR_STATUS_FAILED', detail:String(e.message || e) });
  }
});

app.post('/api/auth/2fa/setup/start', async (req, res) => {
  try {
    await ndsp2faEnsureColumns();
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    if (!email) return res.status(400).json({ ok:false, error:'EMAIL_REQUIRED' });

    const q = await pool.query(
      `SELECT id,email,two_factor_enabled,two_factor_secret FROM users WHERE lower(email)=lower($1) LIMIT 1`,
      [email]
    );

    if (!q.rows.length) return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });

    const user = q.rows[0];
    if (ndsp2faActive(user)) return res.json({ ok:true, already_enabled:true });

    const secret = ndsp2faGenerateSecret();
    await pool.query(
      `UPDATE users
       SET two_factor_secret=$1,
           two_factor_enabled=false,
           two_factor_setup_required=true,
           two_factor_last_prompt_at=now()
       WHERE id=$2`,
      [secret, user.id]
    );

    const otpauth = ndsp2faKeyuri(email, 'NDSP', secret);
    const qr_data_url = await ndsp2faQRCode.toDataURL(otpauth);

    return res.json({ ok:true, setup_required:true, secret, otpauth, qr_data_url, can_skip:true });
  } catch(e) {
    return res.status(500).json({ ok:false, error:'TWO_FACTOR_SETUP_START_FAILED', detail:String(e.message || e) });
  }
});

app.post('/api/auth/2fa/setup/confirm', async (req, res) => {
  try {
    await ndsp2faEnsureColumns();
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    const code = String((req.body && req.body.code) || '').replace(/\s+/g,'');

    if (!email || !code) return res.status(400).json({ ok:false, error:'EMAIL_AND_CODE_REQUIRED' });

    const q = await pool.query(
      `SELECT id,email,two_factor_secret FROM users WHERE lower(email)=lower($1) LIMIT 1`,
      [email]
    );

    if (!q.rows.length) return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });

    const user = q.rows[0];
    if (!user.two_factor_secret) return res.status(400).json({ ok:false, error:'TWO_FACTOR_SETUP_NOT_STARTED' });

    if (!ndsp2faCheck(code, user.two_factor_secret)) {
      return res.status(400).json({ ok:false, error:'INVALID_2FA_CODE' });
    }

    await pool.query(
      `UPDATE users
       SET two_factor_enabled=true,
           two_factor_setup_required=false,
           two_factor_skipped_at=NULL,
           two_factor_confirmed_at=now()
       WHERE id=$1`,
      [user.id]
    );

    return res.json({ ok:true, setup_complete:true, two_factor_enabled:true, redirect:'/NDSP_Command_Center.html' });
  } catch(e) {
    return res.status(500).json({ ok:false, error:'TWO_FACTOR_SETUP_CONFIRM_FAILED', detail:String(e.message || e) });
  }
});

app.post('/api/auth/2fa/setup/skip', async (req, res) => {
  try {
    await ndsp2faEnsureColumns();
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    if (!email) return res.status(400).json({ ok:false, error:'EMAIL_REQUIRED' });

    const q = await pool.query(
      `UPDATE users
       SET two_factor_setup_required=false,
           two_factor_skipped_at=now()
       WHERE lower(email)=lower($1)
       RETURNING email`,
      [email]
    );

    if (!q.rows.length) return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });

    return res.json({ ok:true, skipped:true, can_setup_later:true, redirect:'/NDSP_Command_Center.html' });
  } catch(e) {
    return res.status(500).json({ ok:false, error:'TWO_FACTOR_SKIP_FAILED', detail:String(e.message || e) });
  }
});
// NDSP_2FA_SINGLE_CANONICAL_END



// NDSP_2FA_CONFIRM_OVERRIDE_FINAL_SAFE
app.post('/api/auth/2fa/setup/confirm-final', async (req, res) => {
  try {
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    const code = String((req.body && req.body.code) || '').replace(/\s+/g, '');

    if (!email || !code) {
      return res.status(400).json({ ok:false, error:'EMAIL_AND_CODE_REQUIRED' });
    }

    const q = await pool.query(
      `SELECT id,email,two_factor_secret FROM users WHERE lower(email)=lower($1) LIMIT 1`,
      [email]
    );

    if (!q.rows.length) {
      return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });
    }

    const user = q.rows[0];
    const secret = String(user.two_factor_secret || '').replace(/\s+/g, '').toUpperCase();

    if (!secret) {
      return res.status(400).json({ ok:false, error:'TWO_FACTOR_SETUP_NOT_STARTED' });
    }

    const otplib = require('otplib');

    let ok = false;

    try {
      if (typeof otplib.verifySync === 'function') {
        ok = otplib.verifySync({
          token: code,
          secret,
          window: 1,
          algorithm: 'sha1',
          digits: 6,
          period: 30
        }) === true;
      }
    } catch (e) {
      console.warn('NDSP_CONFIRM_FINAL_VERIFYSYNC_FAILED', e && e.message ? e.message : e);
    }

    try {
      if (!ok && typeof otplib.verify === 'function') {
        const r = otplib.verify({
          token: code,
          secret,
          window: 1,
          algorithm: 'sha1',
          digits: 6,
          period: 30
        });
        ok = r === true;
      }
    } catch (e) {
      console.warn('NDSP_CONFIRM_FINAL_VERIFY_FAILED', e && e.message ? e.message : e);
    }

    try {
      if (!ok && typeof otplib.generate === 'function') {
        const generated = String(otplib.generate(secret));
        ok = generated === code;
      }
    } catch (e) {
      console.warn('NDSP_CONFIRM_FINAL_GENERATE_FAILED', e && e.message ? e.message : e);
    }

    if (!ok) {
      return res.status(400).json({
        ok:false,
        error:'INVALID_2FA_CODE',
        hint:'تأكد من ضبط وقت الجوال تلقائيًا، ثم أدخل الكود قبل تغيّره.'
      });
    }

    await pool.query(
      `UPDATE users
       SET two_factor_enabled=true,
           two_factor_setup_required=false,
           two_factor_skipped_at=NULL,
           two_factor_confirmed_at=now()
       WHERE id=$1`,
      [user.id]
    );

    return res.json({
      ok:true,
      setup_complete:true,
      two_factor_enabled:true,
      email:user.email,
      redirect:'/NDSP_Command_Center.html'
    });
  } catch (err) {
    return res.status(500).json({
      ok:false,
      error:'TWO_FACTOR_CONFIRM_FINAL_FAILED',
      detail: err && err.message ? err.message : String(err)
    });
  }
});



// NDSP_2FA_CONFIRM_SPEAKEASY_FINAL
app.post('/api/auth/2fa/setup/confirm-speakeasy', async (req, res) => {
  try {
    const email = String((req.body && req.body.email) || '').trim().toLowerCase();
    const code = String((req.body && req.body.code) || '').replace(/\s+/g, '');

    if (!email || !code) {
      return res.status(400).json({ ok:false, error:'EMAIL_AND_CODE_REQUIRED' });
    }

    const q = await pool.query(
      `SELECT id,email,two_factor_secret FROM users WHERE lower(email)=lower($1) LIMIT 1`,
      [email]
    );

    if (!q.rows.length) {
      return res.status(404).json({ ok:false, error:'USER_NOT_FOUND' });
    }

    const user = q.rows[0];
    const secret = String(user.two_factor_secret || '').replace(/\s+/g, '').toUpperCase();

    if (!secret) {
      return res.status(400).json({ ok:false, error:'TWO_FACTOR_SETUP_NOT_STARTED' });
    }

    const speakeasy = require('speakeasy');

    const verified = speakeasy.totp.verify({
      secret,
      encoding: 'base32',
      token: code,
      step: 30,
      window: 1
    });

    if (!verified) {
      return res.status(400).json({
        ok:false,
        error:'INVALID_2FA_CODE',
        hint:'تأكد من ضبط وقت الجوال تلقائيًا، ثم أدخل الكود قبل تغيّره.'
      });
    }

    await pool.query(
      `UPDATE users
       SET two_factor_enabled=true,
           two_factor_setup_required=false,
           two_factor_skipped_at=NULL,
           two_factor_confirmed_at=now()
       WHERE id=$1`,
      [user.id]
    );

    return res.json({
      ok:true,
      setup_complete:true,
      two_factor_enabled:true,
      email:user.email,
      redirect:'/NDSP_Command_Center.html'
    });
  } catch (err) {
    return res.status(500).json({
      ok:false,
      error:'TWO_FACTOR_CONFIRM_SPEAKEASY_FAILED',
      detail: err && err.message ? err.message : String(err)
    });
  }
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`[NDSP] user login gateway with optional TOTP 2FA listening on 127.0.0.1:${PORT}`)
})

const express = require('express');
const crypto = require('crypto');
const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

const REGISTRATION_PATHS = new Set([
  '/register',
  '/signup',
  '/api/register',
  '/api/signup',
  '/auth/register',
  '/auth/signup',
  '/api/auth/register',
  '/api/auth/signup'
]);

const SALT =
  process.env.NDSP_DEVICE_GUARD_SALT ||
  process.env.JWT_SECRET ||
  process.env.AUTH_JWT_SECRET ||
  'ndsp-device-guard-default-salt-change-me';

function sha256(value) {
  return crypto
    .createHash('sha256')
    .update(`${SALT}:${value}`)
    .digest('hex');
}

function isRegisterPath(req) {
  const path = String(req.path || req.url || '').split('?')[0];
  return req.method === 'POST' && REGISTRATION_PATHS.has(path);
}

function normalizeEmail(email) {
  return String(email || '').trim().toLowerCase();
}

function firstHeader(req, names) {
  for (const name of names) {
    const v = req.headers[name.toLowerCase()];
    if (v) return String(Array.isArray(v) ? v[0] : v);
  }
  return '';
}

function cleanIp(ip) {
  ip = String(ip || '').trim();
  if (!ip) return '';
  ip = ip.split(',')[0].trim();
  ip = ip.replace(/^::ffff:/, '');
  return ip;
}

function isPublicUsableIp(ip) {
  if (!ip) return false;
  if (ip === '127.0.0.1' || ip === '::1') return false;
  if (ip.startsWith('10.')) return false;
  if (ip.startsWith('192.168.')) return false;
  if (/^172\.(1[6-9]|2\d|3[0-1])\./.test(ip)) return false;
  return true;
}

function getClientIp(req) {
  const ip =
    firstHeader(req, ['cf-connecting-ip']) ||
    firstHeader(req, ['x-real-ip']) ||
    firstHeader(req, ['x-forwarded-for']) ||
    req.ip ||
    req.socket?.remoteAddress ||
    '';

  return cleanIp(ip);
}

function maskIp(ip) {
  if (!ip) return '';
  if (ip.includes(':')) {
    return ip.split(':').slice(0, 3).join(':') + ':****';
  }
  const parts = ip.split('.');
  if (parts.length === 4) return `${parts[0]}.${parts[1]}.${parts[2]}.***`;
  return ip;
}

function getFingerprint(req) {
  const fromHeader =
    firstHeader(req, ['x-ndsp-device-fingerprint']) ||
    firstHeader(req, ['x-device-fingerprint']);

  if (fromHeader && fromHeader.length >= 16) {
    return fromHeader.slice(0, 512);
  }

  const ua = firstHeader(req, ['user-agent']);
  const lang = firstHeader(req, ['accept-language']);
  const chUa = firstHeader(req, ['sec-ch-ua']);
  const platform = firstHeader(req, ['sec-ch-ua-platform']);
  const mobile = firstHeader(req, ['sec-ch-ua-mobile']);

  const fallback = [ua, lang, chUa, platform, mobile].filter(Boolean).join('|');
  return fallback.length >= 16 ? fallback.slice(0, 512) : '';
}

async function audit(email, action, reason, req, ipMasked) {
  try {
    await pool.query(`
      INSERT INTO public.ndsp_registration_guard_audit
        (email, action, reason, ip_masked, source_path, user_agent)
      VALUES ($1,$2,$3,$4,$5,$6)
    `, [
      email || null,
      action,
      reason || null,
      ipMasked || null,
      req.originalUrl || req.url || null,
      firstHeader(req, ['user-agent']) || null
    ]);
  } catch (err) {
    console.error('registration guard audit error:', err.message);
  }
}

async function userExists(email) {
  const r = await pool.query(`
    SELECT id::text AS id, email
    FROM public.users
    WHERE lower(email)=lower($1)
    LIMIT 1
  `, [email]);

  return r.rows[0] || null;
}

async function insertLock(email, req, ipHash, fingerprintHash, ipMasked) {
  let user = null;
  try {
    user = await userExists(email);
  } catch (_) {}

  try {
    await pool.query(`
      INSERT INTO public.ndsp_registration_locks
        (email, user_id, ip_hash, fingerprint_hash, ip_masked, user_agent, source_path)
      VALUES ($1,$2,$3,$4,$5,$6,$7)
      ON CONFLICT DO NOTHING
    `, [
      email,
      user?.id || null,
      ipHash || null,
      fingerprintHash || null,
      ipMasked || null,
      firstHeader(req, ['user-agent']) || null,
      req.originalUrl || req.url || null
    ]);
  } catch (err) {
    console.error('registration lock insert error:', err.message);
  }
}

async function installDeviceRegistrationGuard(app) {
  app.set('trust proxy', true);

  const router = express.Router();

  router.use(express.json({ limit: '1mb' }));
  router.use(express.urlencoded({ extended: true, limit: '1mb' }));

  router.use(async (req, res, next) => {
    if (!isRegisterPath(req)) return next();

    const email = normalizeEmail(req.body?.email || req.body?.username);
    const ip = getClientIp(req);
    const ipMasked = maskIp(ip);
    const usableIp = isPublicUsableIp(ip);
    const fingerprint = getFingerprint(req);

    const ipHash = usableIp ? sha256(`ip:${ip}`) : null;
    const fingerprintHash = fingerprint ? sha256(`fp:${fingerprint}`) : null;

    if (!email) return next();

    try {
      const checks = [];
      const params = [email];
      let i = 2;

      if (ipHash) {
        checks.push(`ip_hash=$${i++}`);
        params.push(ipHash);
      }

      if (fingerprintHash) {
        checks.push(`fingerprint_hash=$${i++}`);
        params.push(fingerprintHash);
      }

      if (checks.length) {
        const conflict = await pool.query(`
          SELECT id, email, ip_masked, created_at,
                 CASE
                   WHEN ip_hash = $2 THEN 'IP_ALREADY_REGISTERED'
                   ELSE 'DEVICE_ALREADY_REGISTERED'
                 END AS reason
          FROM public.ndsp_registration_locks
          WHERE is_active = TRUE
            AND lower(email) <> lower($1)
            AND (${checks.join(' OR ')})
          ORDER BY created_at ASC
          LIMIT 1
        `, params);

        if (conflict.rows[0]) {
          const reason = conflict.rows[0].reason || 'DEVICE_ALREADY_REGISTERED';
          await audit(email, 'blocked_register', reason, req, ipMasked);

          return res.status(409).json({
            error: 'DEVICE_ALREADY_REGISTERED',
            message: 'تم استخدام هذا الجهاز أو عنوان الشبكة للتسجيل مسبقاً. يسمح النظام بحساب واحد فقط لكل جهاز أو IP.'
          });
        }
      }

      res.on('finish', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          insertLock(email, req, ipHash, fingerprintHash, ipMasked);
          audit(email, 'registered_lock_created', 'REGISTER_SUCCESS', req, ipMasked);
        }
      });

      return next();
    } catch (err) {
      console.error('registration guard error:', err);
      return res.status(500).json({
        error: 'REGISTRATION_GUARD_ERROR',
        message: 'تعذر التحقق من الجهاز أثناء التسجيل'
      });
    }
  });

  app.use(router);

  console.log('✅ NDSP one-device-one-account guard mounted');
}

module.exports = { installDeviceRegistrationGuard };

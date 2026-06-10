#!/usr/bin/env bash
set -euo pipefail

DOMAIN="https://ndsp.app"
FRONTEND_DIR="/var/www/ndsp-vite"
BACKEND_DIR="/home/nawaf511/empire-core-new/backend/auth_api"
DEPLOY_DIR="/var/www/html"
SERVICE_NAME="ndsp-auth-api"
BACKUP_ROOT="/root/ndsp_device_guard_backup_$(date +%Y%m%d_%H%M%S)"

if [[ "$EUID" -ne 0 ]]; then
  echo "❌ شغّل السكربت بصلاحيات root"
  exit 1
fi

echo "== NDSP One Device / One Account Guard =="
echo "Backup: $BACKUP_ROOT"

mkdir -p "$BACKUP_ROOT"
cp -a "$BACKEND_DIR" "$BACKUP_ROOT/backend" 2>/dev/null || true
cp -a "$FRONTEND_DIR" "$BACKUP_ROOT/frontend" 2>/dev/null || true

cd "$BACKEND_DIR"

echo "== Installing backend dependency =="
npm install pg dotenv express --save

echo "== Creating database table =="
cat > "$BACKEND_DIR/ndsp_device_guard_migrate.cjs" <<'NODE'
require('dotenv').config();
const { Pool } = require('pg');

const pool = new Pool({
  connectionString:
    process.env.DATABASE_URL ||
    process.env.POSTGRES_URL ||
    process.env.POSTGRES_URI ||
    process.env.PG_CONNECTION_STRING ||
    'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
});

async function main() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS public.ndsp_registration_locks (
      id BIGSERIAL PRIMARY KEY,
      email TEXT NOT NULL,
      user_id TEXT NULL,
      ip_hash TEXT NULL,
      fingerprint_hash TEXT NULL,
      ip_masked TEXT NULL,
      user_agent TEXT NULL,
      source_path TEXT NULL,
      is_active BOOLEAN NOT NULL DEFAULT TRUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );

    CREATE INDEX IF NOT EXISTS ndsp_registration_locks_email_idx
      ON public.ndsp_registration_locks (lower(email));

    CREATE UNIQUE INDEX IF NOT EXISTS ndsp_registration_locks_ip_hash_unique
      ON public.ndsp_registration_locks (ip_hash)
      WHERE ip_hash IS NOT NULL AND is_active = TRUE;

    CREATE UNIQUE INDEX IF NOT EXISTS ndsp_registration_locks_fingerprint_hash_unique
      ON public.ndsp_registration_locks (fingerprint_hash)
      WHERE fingerprint_hash IS NOT NULL AND is_active = TRUE;

    CREATE TABLE IF NOT EXISTS public.ndsp_registration_guard_audit (
      id BIGSERIAL PRIMARY KEY,
      email TEXT NULL,
      action TEXT NOT NULL,
      reason TEXT NULL,
      ip_masked TEXT NULL,
      source_path TEXT NULL,
      user_agent TEXT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);

  console.log('✅ Device registration guard tables ready');
}

main()
  .catch(err => {
    console.error('❌ Migration failed:', err);
    process.exit(1);
  })
  .finally(() => pool.end());
NODE

node "$BACKEND_DIR/ndsp_device_guard_migrate.cjs"

echo "== Creating backend guard =="
cat > "$BACKEND_DIR/ndsp_device_guard.cjs" <<'NODE'
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
NODE

echo "== Patching backend entry file =="
python3 - "$BACKEND_DIR" <<'PY'
import pathlib, sys, re, json

base = pathlib.Path(sys.argv[1]).resolve()
pkg_path = base / "package.json"
pkg = {}
if pkg_path.exists():
    pkg = json.loads(pkg_path.read_text())

candidates = []

scripts = pkg.get("scripts", {})
for key in ("start", "serve", "dev"):
    cmd = scripts.get(key, "")
    m = re.search(r"node\s+([^\s]+\.m?c?js)", cmd)
    if m:
        candidates.append(base / m.group(1))

if pkg.get("main"):
    candidates.append(base / pkg["main"])

for name in [
    "server.js", "index.js", "app.js", "main.js",
    "server.cjs", "index.cjs", "app.cjs",
    "src/server.js", "src/index.js", "src/app.js",
    "src/server.cjs", "src/index.cjs", "src/app.cjs"
]:
    candidates.append(base / name)

seen = set()
files = []
for p in candidates:
    p = p.resolve()
    if p.exists() and p not in seen:
        files.append(p)
        seen.add(p)

target = None
app_var = None

for p in files:
    txt = p.read_text(errors="ignore")
    m = re.search(r"(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*express\s*\(\s*\)", txt)
    if m and ".listen" in txt:
        target = p
        app_var = m.group(1)
        break

if not target:
    raise SystemExit("❌ Could not detect Express entry file")

txt = target.read_text()

txt = re.sub(
    r"\n?/\* NDSP_DEVICE_GUARD_START \*/.*?/\* NDSP_DEVICE_GUARD_END \*/\n?",
    "\n",
    txt,
    flags=re.S
)

pkg_type_module = pkg.get("type") == "module"
is_esm = target.suffix == ".mjs" or pkg_type_module or re.search(r"^\s*import\s+", txt, re.M)
guard_path = str(base / "ndsp_device_guard.cjs")

if is_esm:
    block = f"""
/* NDSP_DEVICE_GUARD_START */
try {{
  const {{ installDeviceRegistrationGuard }} = await import('{(base / "ndsp_device_guard.cjs").as_uri()}');
  installDeviceRegistrationGuard({app_var});
}} catch (e) {{
  console.error('❌ NDSP device guard failed:', e);
  throw e;
}}
/* NDSP_DEVICE_GUARD_END */
"""
else:
    block = f"""
/* NDSP_DEVICE_GUARD_START */
try {{
  const {{ installDeviceRegistrationGuard }} = require('{guard_path}');
  installDeviceRegistrationGuard({app_var});
}} catch (e) {{
  console.error('❌ NDSP device guard failed:', e);
  throw e;
}}
/* NDSP_DEVICE_GUARD_END */
"""

pattern = re.compile(r"((?:const|let|var)\s+" + re.escape(app_var) + r"\s*=\s*express\s*\(\s*\)\s*;?)")
m = pattern.search(txt)

if not m:
    raise SystemExit(f"❌ Could not find {app_var}=express() in {target}")

txt = txt[:m.end()] + "\n" + block + txt[m.end():]
target.write_text(txt)

print(f"✅ Patched backend entry: {target}")
PY

echo "== Creating frontend device fingerprint injector =="
mkdir -p "$FRONTEND_DIR/src"

cat > "$FRONTEND_DIR/src/ndsp-device-fingerprint.js" <<'JS'
(() => {
  const REG_PATHS = [
    '/register',
    '/signup',
    '/api/register',
    '/api/signup',
    '/auth/register',
    '/auth/signup',
    '/api/auth/register',
    '/api/auth/signup'
  ];

  function uuid() {
    try {
      return crypto.randomUUID();
    } catch (_) {
      return 'dev-' + Date.now() + '-' + Math.random().toString(16).slice(2);
    }
  }

  async function digest(text) {
    try {
      const data = new TextEncoder().encode(text);
      const hash = await crypto.subtle.digest('SHA-256', data);
      return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
    } catch (_) {
      let h = 0;
      for (let i = 0; i < text.length; i++) h = Math.imul(31, h) + text.charCodeAt(i) | 0;
      return String(h >>> 0);
    }
  }

  function canvasSignal() {
    try {
      const c = document.createElement('canvas');
      c.width = 240;
      c.height = 80;
      const ctx = c.getContext('2d');
      ctx.textBaseline = 'top';
      ctx.font = '16px Arial';
      ctx.fillStyle = '#123456';
      ctx.fillText('NDSP-device-fingerprint-2026', 4, 8);
      ctx.strokeStyle = '#abcdef';
      ctx.strokeRect(2, 2, 200, 40);
      return c.toDataURL();
    } catch (_) {
      return '';
    }
  }

  async function getFingerprint() {
    let deviceId = localStorage.getItem('ndsp_device_id');
    if (!deviceId) {
      deviceId = uuid();
      localStorage.setItem('ndsp_device_id', deviceId);
    }

    const parts = [
      deviceId,
      navigator.userAgent || '',
      navigator.language || '',
      (navigator.languages || []).join(','),
      navigator.platform || '',
      String(navigator.hardwareConcurrency || ''),
      String(navigator.deviceMemory || ''),
      Intl.DateTimeFormat().resolvedOptions().timeZone || '',
      `${screen.width}x${screen.height}x${screen.colorDepth}`,
      canvasSignal()
    ];

    return digest(parts.join('|'));
  }

  function isRegisterUrl(input) {
    try {
      const url = typeof input === 'string'
        ? new URL(input, location.origin)
        : new URL(input.url, location.origin);

      return REG_PATHS.includes(url.pathname);
    } catch (_) {
      return false;
    }
  }

  const originalFetch = window.fetch;
  if (typeof originalFetch === 'function') {
    window.fetch = async function(input, init = {}) {
      if (isRegisterUrl(input)) {
        const fp = await getFingerprint();
        const headers = new Headers(init.headers || (input && input.headers) || {});
        headers.set('X-NDSP-Device-Fingerprint', fp);
        init = { ...init, headers };
      }

      return originalFetch.call(this, input, init);
    };
  }

  const OriginalXHR = window.XMLHttpRequest;
  if (OriginalXHR) {
    const open = OriginalXHR.prototype.open;
    const send = OriginalXHR.prototype.send;

    OriginalXHR.prototype.open = function(method, url) {
      this.__ndspRegisterRequest = String(method || '').toUpperCase() === 'POST' && isRegisterUrl(url);
      return open.apply(this, arguments);
    };

    OriginalXHR.prototype.send = async function() {
      if (this.__ndspRegisterRequest) {
        try {
          this.setRequestHeader('X-NDSP-Device-Fingerprint', await getFingerprint());
        } catch (_) {}
      }
      return send.apply(this, arguments);
    };
  }
})();
JS

echo "== Patching frontend main entry =="
python3 - "$FRONTEND_DIR" <<'PY'
import pathlib, sys

base = pathlib.Path(sys.argv[1])
candidates = [
    base / "src/main.jsx",
    base / "src/main.tsx",
    base / "src/main.js",
    base / "src/main.ts",
    base / "src/index.jsx",
    base / "src/index.tsx",
    base / "src/index.js",
    base / "src/index.ts",
]

target = next((p for p in candidates if p.exists()), None)
if not target:
    raise SystemExit("❌ Could not find frontend main entry")

txt = target.read_text()
line = "import './ndsp-device-fingerprint.js';"

if line not in txt:
    txt = line + "\n" + txt
    target.write_text(txt)

print(f"✅ Patched frontend entry: {target}")
PY

echo "== Building frontend =="
cd "$FRONTEND_DIR"
npm install
export QT_QPA_PLATFORM=offscreen
export CI=true

node <<'NODE'
const fs = require('fs');
const p = 'package.json';
const pkg = JSON.parse(fs.readFileSync(p, 'utf8'));
pkg.scripts = pkg.scripts || {};
if (!pkg.scripts.build || pkg.scripts.build === 'vite build') {
  pkg.scripts.build = 'QT_QPA_PLATFORM=offscreen node ./node_modules/vite/bin/vite.js build';
}
fs.writeFileSync(p, JSON.stringify(pkg, null, 2) + '\n');
NODE

npm run build

echo "== Deploying frontend =="
mkdir -p "$DEPLOY_DIR"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$FRONTEND_DIR/dist/" "$DEPLOY_DIR/"
else
  find "$DEPLOY_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  cp -a "$FRONTEND_DIR/dist/." "$DEPLOY_DIR/"
fi

echo "== Restarting services =="
systemctl restart "$SERVICE_NAME"
systemctl reload nginx

echo "== Checks =="
sleep 2

systemctl is-active --quiet "$SERVICE_NAME" \
  && echo "✅ $SERVICE_NAME active" \
  || { echo "❌ $SERVICE_NAME failed"; systemctl status "$SERVICE_NAME" --no-pager -l; exit 1; }

curl -fsS "http://127.0.0.1:9011/api/plans" >/dev/null \
  && echo "✅ API OK" \
  || echo "⚠️ API /api/plans failed"

echo ""
echo "✅ تم تفعيل منع التسجيل المتكرر"
echo "القاعدة الآن:"
echo "- حساب واحد لكل IP عام"
echo "- حساب واحد لكل Device Fingerprint"
echo "- MAC Address غير مستخدم لأنه غير متاح من المتصفح"
echo ""
echo "Backup saved at: $BACKUP_ROOT"

const http = require("http");
const https = require("https");
const crypto = require("crypto");
const { spawnSync } = require("child_process");
const { Pool } = require("pg");
const jwt = require("jsonwebtoken");
const fs = require("fs");

const ENV_FILE = "/home/nawaf511/.config/ndsp/backend.env";
const HOST = "127.0.0.1";
const PORT = 9062;

function loadEnv(path) {
  try {
    const raw = fs.readFileSync(path, "utf8");
    for (const line0 of raw.split(/\r?\n/)) {
      const line = line0.trim();
      if (!line || line.startsWith("#") || !line.includes("=")) continue;
      const i = line.indexOf("=");
      const k = line.slice(0, i).trim();
      let v = line.slice(i + 1).trim();
      v = v.replace(/^['"]|['"]$/g, "");
      if (k && process.env[k] === undefined) process.env[k] = v;
    }
  } catch (_) {}
}

loadEnv(ENV_FILE);

function env(...names) {
  for (const n of names) {
    const v = process.env[n];
    if (v !== undefined && String(v).trim() !== "") return String(v).trim();
  }
  return "";
}

const pool = new Pool({
  host: env("PGHOST", "POSTGRES_HOST", "DB_HOST") || "127.0.0.1",
  port: Number(env("PGPORT", "POSTGRES_PORT") || 5432),
  database: env("PGDATABASE", "POSTGRES_DB", "POSTGRES_DATABASE", "DB_DATABASE") || "ndsp_auth",
  user: env("PGUSER", "POSTGRES_USER", "DB_USER"),
  password: env("PGPASSWORD", "POSTGRES_PASSWORD", "DB_PASSWORD"),
});

function json(res, code, obj) {
  const body = Buffer.from(JSON.stringify(obj), "utf8");
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Content-Length": body.length
  });
  res.end(body);
}

function parseCookies(req) {
  const h = req.headers.cookie || "";
  const out = {};
  h.split(";").forEach(p => {
    const i = p.indexOf("=");
    if (i > -1) out[p.slice(0, i).trim()] = decodeURIComponent(p.slice(i + 1).trim());
  });
  return out;
}

function sha(v) {
  return crypto.createHash("sha256").update(String(v)).digest("hex");
}

function maskEmail(v) {
  v = String(v || "");
  if (!v.includes("@")) return "";
  const [a, b] = v.split("@");
  return `${a.slice(0,2)}***@${b}`;
}

function maskId(v) {
  v = String(v || "");
  if (v.length <= 8) return "***";
  return v.slice(0,4) + "..." + v.slice(-4);
}

function readBody(req) {
  return new Promise((resolve) => {
    let data = "";
    req.on("data", chunk => { data += chunk; if (data.length > 20000) req.destroy(); });
    req.on("end", () => {
      try { resolve(data ? JSON.parse(data) : {}); }
      catch { resolve({}); }
    });
  });
}

async function findUsersTable() {
  const names = ["users", "ndsp_users", "accounts", "user_accounts"];
  for (const t of names) {
    const r = await pool.query(
      `SELECT table_name FROM information_schema.tables
       WHERE table_schema='public' AND table_name=$1 LIMIT 1`,
      [t]
    );
    if (r.rowCount) return t;
  }
  return null;
}

function normalizeUser(row) {
  if (!row) return null;
  return {
    id: String(row.id || row.user_id || row.uuid || ""),
    email: String(row.email || "").toLowerCase(),
    name: row.name || row.full_name || row.display_name || ""
  };
}

async function userByIdOrEmail(id, email) {
  const t = await findUsersTable();
  if (!t) return null;

  if (id) {
    const r = await pool.query(`SELECT * FROM public.${t} WHERE id::text=$1 LIMIT 1`, [String(id)]);
    if (r.rowCount) return normalizeUser(r.rows[0]);
  }

  if (email) {
    const r = await pool.query(`SELECT * FROM public.${t} WHERE lower(email)=lower($1) LIMIT 1`, [String(email)]);
    if (r.rowCount) return normalizeUser(r.rows[0]);
  }

  return null;
}

function collectTokens(req) {
  const cookies = parseCookies(req);
  const tokens = [];

  const auth = req.headers.authorization || "";
  if (auth.toLowerCase().startsWith("bearer ")) tokens.push(auth.slice(7).trim());

  [
    "ndsp_session","ndsp_session_id","ndsp_token","ndsp_auth",
    "access_token","auth_token","session","session_id","jwt","token"
  ].forEach(k => {
    if (cookies[k]) tokens.push(cookies[k]);
  });

  return [...new Set(tokens.filter(Boolean))];
}

async function userFromJwt(req) {
  const secrets = [
    env("JWT_SECRET"),
    env("AUTH_JWT_SECRET"),
    env("NDSP_JWT_SECRET"),
  ].filter(Boolean);

  for (const token of collectTokens(req)) {
    for (const secret of secrets) {
      try {
        const p = jwt.verify(token, secret);
        const id = p.id || p.userId || p.user_id || p.sub;
        const email = p.email || p.mail || p.username;
        const u = await userByIdOrEmail(id, email);
        if (u && u.id) return u;
      } catch (_) {}
    }

    try {
      const p = jwt.decode(token);
      if (p) {
        const id = p.id || p.userId || p.user_id || p.sub;
        const email = p.email || p.mail || p.username;
        const u = await userByIdOrEmail(id, email);
        if (u && u.id) return u;
      }
    } catch (_) {}
  }

  return null;
}

async function userFromSessions(req) {
  const tokens = collectTokens(req);
  if (!tokens.length) return null;

  const tables = await pool.query(`
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='public'
      AND (
        table_name ILIKE '%session%' OR
        table_name ILIKE '%token%' OR
        table_name ILIKE '%auth%'
      )
    ORDER BY table_name
  `);

  for (const row of tables.rows) {
    const t = row.table_name;
    const colsR = await pool.query(`
      SELECT column_name FROM information_schema.columns
      WHERE table_schema='public' AND table_name=$1
    `, [t]);

    const cols = colsR.rows.map(x => x.column_name);
    const userCol = ["user_id","account_id","uid","owner_id"].find(x => cols.includes(x));
    const tokenCols = ["token","session_token","access_token","refresh_token","token_hash","session_id","id","jti"].filter(x => cols.includes(x));

    if (!userCol || !tokenCols.length) continue;

    for (const tc of tokenCols) {
      for (const tok of tokens) {
        try {
          const r = await pool.query(
            `SELECT ${userCol}::text AS user_id FROM public.${t}
             WHERE ${tc}::text=$1
             LIMIT 1`,
            [String(tok)]
          );
          if (r.rowCount) {
            const u = await userByIdOrEmail(r.rows[0].user_id, null);
            if (u && u.id) return u;
          }
        } catch (_) {}
      }
    }
  }

  return null;
}


// NDSP_AUTH_ME_BRIDGE_V38
function gatewayAuthMe(req) {
  return new Promise((resolve) => {
    const cookie = req.headers.cookie || "";
    const authorization = req.headers.authorization || "";

    const options = {
      hostname: "my.ndsp.app",
      path: "/api/auth/me?alerts_bridge_v38=" + Date.now(),
      method: "GET",
      timeout: 9000,
      headers: {
        "Accept": "application/json",
        "Cookie": cookie,
        "Authorization": authorization,
        "User-Agent": "NDSP-User-Alerts-Auth-Bridge-V38"
      }
    };

    const q = https.request(options, (r) => {
      let data = "";
      r.on("data", c => data += c);
      r.on("end", () => {
        try {
          const j = JSON.parse(data);
          resolve(j);
        } catch (_) {
          resolve(null);
        }
      });
    });

    q.on("error", () => resolve(null));
    q.on("timeout", () => {
      q.destroy();
      resolve(null);
    });

    q.end();
  });
}

async function userFromAuthMe(req) {
  const j = await gatewayAuthMe(req);

  if (!j || j.ok === false) return null;

  const raw =
    j.user ||
    (j.data && j.data.user) ||
    j.account ||
    j.profile ||
    j;

  const id =
    raw.id ||
    raw.user_id ||
    raw.userId ||
    raw.sub ||
    "";

  const email =
    raw.email ||
    raw.mail ||
    raw.username ||
    "";

  const name =
    raw.name ||
    raw.full_name ||
    raw.fullName ||
    raw.display_name ||
    raw.displayName ||
    "";

  const found = await userByIdOrEmail(id, email);
  if (found && found.id) return found;

  if (id || email) {
    return {
      id: String(id || email).toLowerCase(),
      email: String(email || "").toLowerCase(),
      name: String(name || "")
    };
  }

  return null;
}

async function currentUser(req) {
  return (await userFromAuthMe(req)) || (await userFromJwt(req)) || (await userFromSessions(req));
}

async function ensureChannel(user) {
  await pool.query(`
    INSERT INTO public.user_alert_channels (user_id, user_email, email)
    VALUES ($1, $2, $2)
    ON CONFLICT (user_id) DO UPDATE
    SET user_email=EXCLUDED.user_email,
        email=COALESCE(public.user_alert_channels.email, EXCLUDED.email),
        updated_at=NOW()
  `, [user.id, user.email || null]);

  const r = await pool.query(
    `SELECT * FROM public.user_alert_channels WHERE user_id=$1 LIMIT 1`,
    [user.id]
  );
  return r.rows[0];
}

function safePreferences(ch) {
  return {
    alerts_enabled: !!ch.alerts_enabled,
    email_enabled: !!ch.email_enabled,
    telegram_enabled: !!ch.telegram_enabled,
    minimum_severity: ch.minimum_severity || "info",
    cooldown_seconds: Number(ch.cooldown_seconds || 0)
  };
}

function severityRank(value) {
  const ranks = { info:0, warning:1, critical:2 };
  return Object.prototype.hasOwnProperty.call(ranks, value) ? ranks[value] : -1;
}

async function auditDelivery(userId, channel, result) {
  await pool.query(`
    UPDATE public.user_alert_channels
    SET last_delivery_at=NOW(),
        last_delivery_channel=$2,
        last_delivery_result=$3,
        updated_at=NOW()
    WHERE user_id=$1
  `, [userId, channel, result]);
}

async function status(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const ch = await ensureChannel(u);

  return json(res, 200, {
    ok: true,
    user: {
      id: u.id,
      email_masked: maskEmail(u.email)
    },
    telegram: {
      verified: !!ch.telegram_verified,
      linked: !!(ch.telegram_verified && ch.telegram_chat_id),
      username: ch.telegram_username || "",
      chat_id_masked: ch.telegram_chat_id ? maskId(ch.telegram_chat_id) : "",
      link_pending: !!(ch.telegram_link_code_hash && !ch.telegram_verified)
    },
    email: {
      email_masked: maskEmail(ch.email || u.email),
      verified: !!ch.email_verified
    },
    preferences: safePreferences(ch)
  });
}

async function preferencesGet(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const ch = await ensureChannel(u);

  return json(res, 200, {
    ok: true,
    preferences: safePreferences(ch)
  });
}

async function preferencesPatch(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  await ensureChannel(u);

  const body = await readBody(req);

  if (!body || typeof body !== "object" || Array.isArray(body)) {
    return json(res, 400, { ok:false, error:"INVALID_BODY" });
  }

  const allowed = new Set([
    "alerts_enabled",
    "email_enabled",
    "telegram_enabled",
    "minimum_severity",
    "cooldown_seconds"
  ]);

  const keys = Object.keys(body);

  if (!keys.length) {
    return json(res, 400, { ok:false, error:"EMPTY_PATCH" });
  }

  const unknown = keys.filter(k => !allowed.has(k));
  if (unknown.length) {
    return json(res, 400, { ok:false, error:"UNKNOWN_FIELDS" });
  }

  for (const k of ["alerts_enabled", "email_enabled", "telegram_enabled"]) {
    if (Object.prototype.hasOwnProperty.call(body, k) && typeof body[k] !== "boolean") {
      return json(res, 400, { ok:false, error:`INVALID_${k.toUpperCase()}` });
    }
  }

  if (Object.prototype.hasOwnProperty.call(body, "minimum_severity")) {
    if (
      typeof body.minimum_severity !== "string" ||
      !["info", "warning", "critical"].includes(body.minimum_severity)
    ) {
      return json(res, 400, { ok:false, error:"INVALID_MINIMUM_SEVERITY" });
    }
  }

  if (Object.prototype.hasOwnProperty.call(body, "cooldown_seconds")) {
    if (
      !Number.isInteger(body.cooldown_seconds) ||
      body.cooldown_seconds < 0 ||
      body.cooldown_seconds > 86400
    ) {
      return json(res, 400, { ok:false, error:"INVALID_COOLDOWN_SECONDS" });
    }
  }

  const sets = [];
  const values = [u.id];
  let n = 2;

  for (const k of [
    "alerts_enabled",
    "email_enabled",
    "telegram_enabled",
    "minimum_severity",
    "cooldown_seconds"
  ]) {
    if (Object.prototype.hasOwnProperty.call(body, k)) {
      sets.push(`${k}=$${n++}`);
      values.push(body[k]);
    }
  }

  sets.push("updated_at=NOW()");

  const r = await pool.query(`
    UPDATE public.user_alert_channels
    SET ${sets.join(", ")}
    WHERE user_id=$1
    RETURNING *
  `, values);

  if (!r.rowCount) {
    return json(res, 500, { ok:false, error:"PREFERENCES_UPDATE_FAILED" });
  }

  return json(res, 200, {
    ok: true,
    preferences: safePreferences(r.rows[0])
  });
}

function randomCode(prefix) {
  return `${prefix}-${crypto.randomBytes(4).toString("hex").toUpperCase()}`;
}

async function telegramStart(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  await ensureChannel(u);

  const code = randomCode("NDSP");
  await pool.query(`
    UPDATE public.user_alert_channels
    SET telegram_link_code_hash=$2,
        telegram_link_expires_at=NOW() + INTERVAL '15 minutes',
        telegram_link_started_at=NOW(),
        telegram_verified=false,
        updated_at=NOW()
    WHERE user_id=$1
  `, [u.id, sha(code)]);

  return json(res, 200, {
    ok: true,
    code,
    expires_in_minutes: 15,
    instruction: "أرسل هذا الكود إلى بوت NDSP في تيليجرام."
  });
}

async function telegramConfirm(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const ch = await ensureChannel(u);

  if (ch.telegram_verified && ch.telegram_chat_id) {
    return json(res, 200, {
      ok:true,
      linked:true,
      message:"TELEGRAM_LINKED",
      chat_id_masked: maskId(ch.telegram_chat_id),
      username: ch.telegram_username || ""
    });
  }

  return json(res, 200, {
    ok: false,
    linked: false,
    message: "PENDING_TELEGRAM_CODE"
  });
}

function sendEmailViaPython(to, subject, body) {
  const py = `
import os, sys, json, ssl, smtplib
from email.message import EmailMessage

d=json.loads(sys.stdin.read())
host=os.environ.get("SMTP_HOST","")
port=int(os.environ.get("SMTP_PORT","587") or "587")
user=os.environ.get("SMTP_USER","")
pwd=os.environ.get("SMTP_PASS") or os.environ.get("SMTP_PASSWORD","")
sender=os.environ.get("SMTP_FROM") or os.environ.get("MAIL_FROM") or os.environ.get("EMAIL_FROM") or user

if not host or not sender or not d.get("to"):
    raise SystemExit("SMTP_CONFIG_MISSING")

msg=EmailMessage()
msg["Subject"]=d["subject"]
msg["From"]=sender
msg["To"]=d["to"]
msg.set_content(d["body"])

if port == 465:
    ctx=ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=ctx, timeout=20) as s:
        if user and pwd:
            s.login(user, pwd)
        s.send_message(msg)
else:
    with smtplib.SMTP(host, port, timeout=20) as s:
        s.ehlo()
        try:
            s.starttls(context=ssl.create_default_context())
            s.ehlo()
        except Exception:
            pass
        if user and pwd:
            s.login(user, pwd)
        s.send_message(msg)
`;

  const r = spawnSync("python3", ["-c", py], {
    input: JSON.stringify({ to, subject, body }),
    encoding: "utf8",
    env: process.env,
    timeout: process.env.PORT || process.env.PORT || 30000
  });

  if (r.status !== 0) {
    throw new Error((r.stderr || r.stdout || "EMAIL_SEND_FAILED").slice(0, 200));
  }
}

function tgPost(method, params) {
  return new Promise((resolve, reject) => {
    const token = env("TELEGRAM_BOT_TOKEN", "NDSP_TELEGRAM_BOT_TOKEN", "BOT_TOKEN");
    if (!token) return reject(new Error("TELEGRAM_TOKEN_MISSING"));

    const data = new URLSearchParams(params).toString();

    const req = https.request({
      hostname: "api.telegram.org",
      path: `/bot${token}/${method}`,
      method: "POST",
      timeout: 20000,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": Buffer.byteLength(data)
      }
    }, (r) => {
      let body = "";
      r.on("data", c => body += c);
      r.on("end", () => {
        try {
          const j = JSON.parse(body);
          if (j.ok) return resolve(j);
          reject(new Error("TELEGRAM_API_REJECTED"));
        } catch (_) {
          reject(new Error("BAD_TELEGRAM_JSON"));
        }
      });
    });

    req.on("error", reject);
    req.on("timeout", () => req.destroy(new Error("TELEGRAM_TIMEOUT")));
    req.write(data);
    req.end();
  });
}

async function sendTelegram(chatId, text) {
  await tgPost("sendMessage", {
    chat_id: String(chatId),
    text,
    disable_web_page_preview: "true"
  });
}

async function emailStart(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const ch = await ensureChannel(u);
  const target = ch.email || u.email;

  if (!target) return json(res, 400, { ok:false, error:"USER_EMAIL_MISSING" });

  const code = String(Math.floor(100000 + Math.random() * 900000));

  await pool.query(`
    UPDATE public.user_alert_channels
    SET email=$2,
        email_verify_code_hash=$3,
        email_verify_expires_at=NOW() + INTERVAL '10 minutes',
        updated_at=NOW()
    WHERE user_id=$1
  `, [u.id, target, sha(code)]);

  sendEmailViaPython(
    target,
    "NDSP - كود تفعيل البريد",
    `كود تفعيل بريدك في NDSP هو: ${code}\n\nينتهي خلال 10 دقائق.\nهذه رسالة تحقق فقط.`
  );

  return json(res, 200, {
    ok: true,
    email_masked: maskEmail(target),
    expires_in_minutes: 10,
    message: "EMAIL_CODE_SENT"
  });
}

async function emailConfirm(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const body = await readBody(req);
  const code = String(body.code || "").trim();

  if (!/^[0-9]{6}$/.test(code)) {
    return json(res, 400, { ok:false, error:"INVALID_CODE_FORMAT" });
  }

  const r = await pool.query(`
    SELECT * FROM public.user_alert_channels
    WHERE user_id=$1
      AND email_verify_code_hash=$2
      AND email_verify_expires_at > NOW()
    LIMIT 1
  `, [u.id, sha(code)]);

  if (!r.rowCount) {
    return json(res, 400, { ok:false, error:"INVALID_OR_EXPIRED_CODE" });
  }

  await pool.query(`
    UPDATE public.user_alert_channels
    SET email_verified=true,
        email_verify_code_hash=NULL,
        email_verify_expires_at=NULL,
        updated_at=NOW()
    WHERE user_id=$1
  `, [u.id]);

  return json(res, 200, { ok:true, email_verified:true });
}

async function userTest(req, res) {
  const u = await currentUser(req);
  if (!u) return json(res, 401, { ok:false, error:"LOGIN_REQUIRED" });

  const ch = await ensureChannel(u);
  const results = {};

  // A user test notification is informational severity.
  const testSeverity = "info";

  if (!ch.alerts_enabled) {
    results.email = "alerts_disabled";
    results.telegram = "alerts_disabled";

    await pool.query(
      `UPDATE public.user_alert_channels SET last_test_at=NOW(), updated_at=NOW() WHERE user_id=$1`,
      [u.id]
    );

    return json(res, 200, { ok:true, results });
  }

  if (severityRank(testSeverity) < severityRank(ch.minimum_severity || "info")) {
    results.email = "severity_filtered";
    results.telegram = "severity_filtered";

    await pool.query(
      `UPDATE public.user_alert_channels SET last_test_at=NOW(), updated_at=NOW() WHERE user_id=$1`,
      [u.id]
    );

    return json(res, 200, { ok:true, results });
  }

  const cooldown = await pool.query(`
    SELECT CASE
      WHEN cooldown_seconds > 0
       AND last_delivery_at IS NOT NULL
       AND last_delivery_at + (cooldown_seconds * INTERVAL '1 second') > NOW()
      THEN true
      ELSE false
    END AS active
    FROM public.user_alert_channels
    WHERE user_id=$1
    LIMIT 1
  `, [u.id]);

  // Fail closed if the row unexpectedly disappears.
  if (!cooldown.rowCount) {
    return json(res, 500, { ok:false, error:"COOLDOWN_STATE_UNAVAILABLE" });
  }

  const cooldownActive = !!cooldown.rows[0].active;

  if (cooldownActive) {
    results.email = "cooldown";
    results.telegram = "cooldown";

    await pool.query(
      `UPDATE public.user_alert_channels SET last_test_at=NOW(), updated_at=NOW() WHERE user_id=$1`,
      [u.id]
    );

    return json(res, 200, { ok:true, results });
  }

  if (!ch.email_enabled) {
    results.email = "disabled";
  } else if (!(ch.email_verified && ch.email)) {
    results.email = "not_verified";
  } else {
    try {
      sendEmailViaPython(
        ch.email,
        "NDSP - اختبار تنبيه المستخدم",
        "تم إرسال اختبار تنبيه لحسابك في NDSP.\nهذه رسالة اختبار فقط وليست توصية مالية أو أمر تنفيذ."
      );
      results.email = "sent";
      await auditDelivery(u.id, "email", "sent");
    } catch (e) {
      results.email = "failed";
      await auditDelivery(u.id, "email", "failed");
    }
  }

  if (!ch.telegram_enabled) {
    results.telegram = "disabled";
  } else if (!(ch.telegram_verified && ch.telegram_chat_id)) {
    results.telegram = "not_linked";
  } else {
    try {
      await sendTelegram(
        ch.telegram_chat_id,
        "NDSP ✅ اختبار تنبيه المستخدم\nتم إرسال هذا الاختبار لحسابك المرتبط فقط.\nتنبيه: هذه رسالة اختبار وليست توصية مالية أو أمر تنفيذ."
      );
      results.telegram = "sent";
      await auditDelivery(u.id, "telegram", "sent");
    } catch (e) {
      results.telegram = "failed";
      await auditDelivery(u.id, "telegram", "failed");
    }
  }

  await pool.query(
    `UPDATE public.user_alert_channels SET last_test_at=NOW(), updated_at=NOW() WHERE user_id=$1`,
    [u.id]
  );

  return json(res, 200, { ok:true, results });
}

async function handler(req, res) {
  try {
    const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
    const p = url.pathname;

    if (req.method === "OPTIONS") return json(res, 200, { ok:true });

    if (req.method === "GET" && p === "/api/alerts/user/status") return status(req, res);

    if (req.method === "GET" && p === "/api/alerts/preferences") return preferencesGet(req, res);
    if (req.method === "PATCH" && p === "/api/alerts/preferences") return preferencesPatch(req, res);

    if (req.method === "POST" && p === "/api/alerts/telegram/link/start") return telegramStart(req, res);
    if (req.method === "POST" && p === "/api/alerts/telegram/link/confirm") return telegramConfirm(req, res);

    if (req.method === "POST" && p === "/api/alerts/email/verify/start") return emailStart(req, res);
    if (req.method === "POST" && p === "/api/alerts/email/verify/confirm") return emailConfirm(req, res);

    if (req.method === "POST" && p === "/api/alerts/user/test") return userTest(req, res);

    return json(res, 404, { ok:false, error:"NOT_FOUND" });
  } catch (e) {
    return json(res, 500, { ok:false, error:"SERVER_ERROR", message:String(e.message || e).slice(0, 220) });
  }
}

http.createServer(handler).listen(PORT, HOST, () => {
  console.log(`NDSP user alert channels API V37 listening on ${HOST}:${PORT}`);
});

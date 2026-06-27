"use strict";

const http = require("http");
const fs = require("fs");
const crypto = require("crypto");
const cookie = require("cookie");
const bcrypt = require("bcryptjs");
const { Pool } = require("pg");

const PORT = Number(process.env.PORT || 9030);

function readEnvFile(path) {
  const out = {};
  try {
    if (!fs.existsSync(path)) return out;
    for (const line of fs.readFileSync(path, "utf8").split(/\r?\n/)) {
      const m = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)\s*$/);
      if (!m) continue;
      out[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
    }
  } catch (_) {}
  return out;
}

const env = Object.assign(
  {},
  readEnvFile("/etc/ndsp/ndsp-db.env"),
  readEnvFile("/home/nawaf511/empire-core-new/backend/.env"),
  process.env
);

const pool = new Pool(
  env.DATABASE_URL || env.POSTGRES_URL || env.PG_URL
    ? { connectionString: env.DATABASE_URL || env.POSTGRES_URL || env.PG_URL }
    : {
        host: env.PGHOST || env.DB_HOST || "127.0.0.1",
        port: Number(env.PGPORT || env.DB_PORT || 5432),
        user: env.PGUSER || env.DB_USER || "postgres",
        password: env.PGPASSWORD || env.DB_PASSWORD || "",
        database: env.PGDATABASE || env.DB_NAME || "ndsp_auth"
      }
);

const ADMIN_EMAILS = String(env.NDSP_ADMIN_EMAILS || env.ADMIN_EMAILS || "")
  .split(",")
  .map(x => x.trim().toLowerCase())
  .filter(Boolean);

function send(res, code, obj, headers = {}) {
  res.writeHead(code, Object.assign({
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  }, headers));
  res.end(JSON.stringify(obj));
}

function sha256(x) {
  return crypto.createHash("sha256").update(String(x)).digest("hex");
}

function makeToken() {
  return crypto.randomBytes(48).toString("base64url");
}

function tokensFromReq(req) {
  const c = cookie.parse(req.headers.cookie || "");
  const names = [
    "ndsp_session",
    "ndsp_session_id",
    "ndsp_token",
    "ndsp_auth",
    "access_token",
    "auth_token",
    "session",
    "session_id",
    "jwt",
    "token"
  ];

  const arr = [];
  for (const n of names) if (c[n]) arr.push(String(c[n]));

  const auth = String(req.headers.authorization || "");
  const m = auth.match(/^Bearer\s+(.+)$/i);
  if (m) arr.push(m[1].trim());

  return [...new Set(arr.filter(Boolean))];
}

async function cols(table) {
  const r = await pool.query(
    "SELECT column_name FROM information_schema.columns WHERE table_schema='public' AND table_name=$1",
    [table]
  );
  return r.rows.map(x => x.column_name);
}

async function tableExists(t) {
  const r = await pool.query("SELECT to_regclass($1) AS x", [`public.${t}`]);
  return !!(r.rows[0] && r.rows[0].x);
}

async function findUsersTable() {
  for (const t of ["users", "ndsp_users", "accounts", "user_accounts"]) {
    if (await tableExists(t)) return t;
  }
  return null;
}

function normalizeUser(row) {
  const email = String(row.email || "").toLowerCase();
  const role = String(row.role || row.user_role || row.account_role || "").toUpperCase();
  const status = String(row.status || row.state || row.account_status || "").toUpperCase();

  return {
    id: row.id || row.user_id || row.uuid || null,
    email,
    name: row.full_name || row.name || row.display_name || "",
    phone: row.phone || row.mobile || "",
    status: status || "UNKNOWN",
    role,
    plan: row.plan || row.package || row.subscription_plan || "",
    is_admin: !!(
      row.is_admin ||
      row.admin ||
      role.includes("ADMIN") ||
      role.includes("OWNER") ||
      ADMIN_EMAILS.includes(email)
    )
  };
}

function userAllowed(u) {
  const s = String(u.status || "").toUpperCase();
  if (!s || s === "UNKNOWN") return true;
  return ["ACTIVE", "APPROVED", "EMAIL_VERIFIED", "TRIAL_ACTIVE", "ENABLED"].includes(s);
}

function adminAllowed(u) {
  if (!userAllowed(u)) return false;
  if (u.is_admin) return true;
  const r = String(u.role || "").toUpperCase();
  return ["ADMIN", "SUPER_ADMIN", "OWNER", "OPS", "OPERATOR"].some(x => r.includes(x));
}

async function ensureTables() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS access_guard_sessions (
      id BIGSERIAL PRIMARY KEY,
      user_id TEXT NOT NULL,
      token_hash TEXT NOT NULL UNIQUE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      expires_at TIMESTAMPTZ NOT NULL DEFAULT NOW() + INTERVAL '16 hours',
      revoked BOOLEAN NOT NULL DEFAULT FALSE
    )
  `);

  await pool.query(`
    CREATE TABLE IF NOT EXISTS access_guard_credentials (
      id BIGSERIAL PRIMARY KEY,
      user_id TEXT NOT NULL UNIQUE,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      disabled BOOLEAN NOT NULL DEFAULT FALSE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )
  `);
}

async function userById(id) {
  const t = await findUsersTable();
  if (!t) return null;

  const c = await cols(t);
  if (!c.includes("id")) return null;

  const wanted = [
    "id","email","phone","mobile","name","full_name","display_name",
    "status","state","account_status","role","user_role","is_admin","admin",
    "plan","package","subscription_plan","subscription_status","created_at"
  ].filter(x => c.includes(x));

  const q = `SELECT ${wanted.length ? wanted.map(x => `"${x}"`).join(",") : "*"} FROM "${t}" WHERE "id"::text=$1 LIMIT 1`;
  const r = await pool.query(q, [String(id)]);

  return r.rows[0] ? normalizeUser(r.rows[0]) : null;
}

async function userByEmail(email) {
  const t = await findUsersTable();
  if (!t) return null;

  const c = await cols(t);
  if (!c.includes("email")) return null;

  const wanted = [
    "id","email","phone","mobile","name","full_name","display_name",
    "status","state","account_status","role","user_role","is_admin","admin",
    "plan","package","subscription_plan","subscription_status","created_at"
  ].filter(x => c.includes(x));

  const q = `SELECT ${wanted.length ? wanted.map(x => `"${x}"`).join(",") : "*"} FROM "${t}" WHERE lower("email")=lower($1) LIMIT 1`;
  const r = await pool.query(q, [String(email)]);

  return r.rows[0] ? normalizeUser(r.rows[0]) : null;
}

async function findUserFromOwnSessions(tokens) {
  await ensureTables();

  for (const tok of tokens) {
    const h = sha256(tok);
    const r = await pool.query(`
      SELECT user_id
      FROM access_guard_sessions
      WHERE token_hash=$1
        AND revoked=false
        AND expires_at > NOW()
      LIMIT 1
    `, [h]);

    if (r.rows[0] && r.rows[0].user_id) {
      const u = await userById(r.rows[0].user_id);
      if (u) {
        u.session_table = "access_guard_sessions";
        return u;
      }
    }
  }

  return null;
}

async function findUserFromSessions(req) {
  const tokens = tokensFromReq(req);
  if (!tokens.length) return null;
  return await findUserFromOwnSessions(tokens);
}

async function createOwnSession(user) {
  await ensureTables();

  const token = makeToken();

  await pool.query(`
    INSERT INTO access_guard_sessions (user_id, token_hash, expires_at, revoked)
    VALUES ($1, $2, NOW() + INTERVAL '16 hours', false)
  `, [String(user.id), sha256(token)]);

  return token;
}

async function listUsers() {
  const t = await findUsersTable();
  if (!t) return { table: null, rows: [] };

  const c = await cols(t);
  const wanted = [
    "id","email","phone","mobile","name","full_name","status","role",
    "is_admin","plan","package","subscription_plan","subscription_status","created_at","updated_at"
  ].filter(x => c.includes(x));

  const order = c.includes("created_at") ? '"created_at" DESC' : '"id" DESC';
  const q = `SELECT ${wanted.map(x => `"${x}"`).join(", ")} FROM "${t}" ORDER BY ${order} LIMIT 300`;
  const r = await pool.query(q);

  return { table: t, columns: wanted, rows: r.rows };
}

async function updateUserStatus(id, status) {
  const t = await findUsersTable();
  if (!t) throw new Error("USERS_TABLE_NOT_FOUND");
  const c = await cols(t);
  if (!c.includes("status")) throw new Error("STATUS_COLUMN_NOT_FOUND");
  await pool.query(`UPDATE "${t}" SET "status"=$1 WHERE "id"::text=$2`, [status, String(id)]);
}

async function updateUserPlan(id, plan) {
  const t = await findUsersTable();
  if (!t) throw new Error("USERS_TABLE_NOT_FOUND");
  const c = await cols(t);
  const pc = ["plan", "package", "subscription_plan"].find(x => c.includes(x));
  if (!pc) throw new Error("PLAN_COLUMN_NOT_FOUND");
  await pool.query(`UPDATE "${t}" SET "${pc}"=$1 WHERE "id"::text=$2`, [plan, String(id)]);
}

function readBody(req) {
  return new Promise(resolve => {
    let b = "";
    req.on("data", c => (b += c));
    req.on("end", () => {
      try { resolve(JSON.parse(b || "{}")); }
      catch { resolve({}); }
    });
  });
}

async function requireAdmin(req, res) {
  const u = await findUserFromSessions(req);
  if (!u) {
    send(res, 401, { ok: false, error: "LOGIN_REQUIRED" });
    return null;
  }

  if (!adminAllowed(u)) {
    send(res, 403, { ok: false, error: "ADMIN_REQUIRED" });
    return null;
  }

  return u;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://127.0.0.1");

    if (url.pathname === "/" || url.pathname === "/health") {
      let db = "unknown";
      try {
        await pool.query("SELECT 1");
        await ensureTables();
        db = "ok";
      } catch (_) {
        db = "review";
      }

      return send(res, 200, {
        ok: true,
        service: "ndsp-access-guard-final",
        port: PORT,
        database: db,
        direct_credentials: true
      });
    }

    if (url.pathname === "/login" && req.method === "POST") {
      const body = await readBody(req);
      const email = String(body.email || body.username || "").trim().toLowerCase();
      const password = String(body.password || "");

      if (!email) return send(res, 400, { ok: false, error: "EMAIL_REQUIRED" });
      if (!password) return send(res, 400, { ok: false, error: "PASSWORD_REQUIRED" });

      await ensureTables();

      const user = await userByEmail(email);
      if (!user) return send(res, 404, { ok: false, error: "USER_NOT_FOUND_IN_NDSP_AUTH" });
      if (!userAllowed(user)) return send(res, 403, { ok: false, error: "USER_NOT_ACTIVE", status: user.status });

      const cr = await pool.query(`
        SELECT password_hash, disabled
        FROM access_guard_credentials
        WHERE lower(email)=lower($1)
        LIMIT 1
      `, [email]);

      if (!cr.rows[0]) return send(res, 401, { ok: false, error: "CREDENTIAL_NOT_SET" });
      if (cr.rows[0].disabled) return send(res, 403, { ok: false, error: "CREDENTIAL_DISABLED" });

      const ok = await bcrypt.compare(password, cr.rows[0].password_hash);
      if (!ok) return send(res, 401, { ok: false, error: "INVALID_PASSWORD" });

      const token = await createOwnSession(user);

      return send(res, 200, {
        ok: true,
        user: {
          id: user.id,
          email: user.email,
          status: user.status,
          role: user.role,
          plan: user.plan,
          is_admin: user.is_admin
        }
      }, {
        "Set-Cookie": cookie.serialize("ndsp_session", token, {
          httpOnly: true,
          secure: true,
          sameSite: "lax",
          path: "/",
          domain: ".ndsp.app",
          maxAge: 16 * 60 * 60
        })
      });
    }

    if (url.pathname === "/logout" && req.method === "POST") {
      const toks = tokensFromReq(req);
      await ensureTables();

      for (const t of toks) {
        await pool.query("UPDATE access_guard_sessions SET revoked=true WHERE token_hash=$1", [sha256(t)]);
      }

      return send(res, 200, { ok: true }, {
        "Set-Cookie": cookie.serialize("ndsp_session", "", {
          httpOnly: true,
          secure: true,
          sameSite: "lax",
          path: "/",
          domain: ".ndsp.app",
          maxAge: 0
        })
      });
    }

    if (url.pathname === "/auth/user") {
      const u = await findUserFromSessions(req);
      if (!u) return send(res, 401, { ok: false, error: "LOGIN_REQUIRED" });
      if (!userAllowed(u)) return send(res, 403, { ok: false, error: "USER_NOT_ACTIVE", status: u.status });

      res.writeHead(204, {
        "Cache-Control": "no-store",
        "X-NDSP-User": u.email || String(u.id || "")
      });
      return res.end();
    }

    if (url.pathname === "/auth/admin") {
      const u = await findUserFromSessions(req);
      if (!u) return send(res, 401, { ok: false, error: "LOGIN_REQUIRED" });
      if (!adminAllowed(u)) return send(res, 403, { ok: false, error: "ADMIN_REQUIRED" });

      res.writeHead(204, {
        "Cache-Control": "no-store",
        "X-NDSP-Admin": u.email || String(u.id || "")
      });
      return res.end();
    }

    if (url.pathname === "/me") {
      const u = await findUserFromSessions(req);
      if (!u) return send(res, 401, { ok: false, error: "LOGIN_REQUIRED" });
      return send(res, 200, { ok: true, user: u });
    }

    if (url.pathname === "/admin/users" && req.method === "GET") {
      const a = await requireAdmin(req, res);
      if (!a) return;
      return send(res, 200, Object.assign({ ok: true }, await listUsers()));
    }

    if (url.pathname === "/admin/subscriptions" && req.method === "GET") {
      const a = await requireAdmin(req, res);
      if (!a) return;
      return send(res, 200, Object.assign({ ok: true }, await listUsers()));
    }

    let m = url.pathname.match(/^\/admin\/users\/([^/]+)\/status$/);
    if (m && req.method === "POST") {
      const a = await requireAdmin(req, res);
      if (!a) return;
      const b = await readBody(req);
      const status = String(b.status || "").toUpperCase();
      if (!status) return send(res, 400, { ok: false, error: "STATUS_REQUIRED" });
      await updateUserStatus(m[1], status);
      return send(res, 200, { ok: true, id: m[1], status });
    }

    m = url.pathname.match(/^\/admin\/subscriptions\/([^/]+)\/plan$/);
    if (m && req.method === "POST") {
      const a = await requireAdmin(req, res);
      if (!a) return;
      const b = await readBody(req);
      const plan = String(b.plan || "");
      if (!plan) return send(res, 400, { ok: false, error: "PLAN_REQUIRED" });
      await updateUserPlan(m[1], plan);
      return send(res, 200, { ok: true, id: m[1], plan });
    }

    return send(res, 404, { ok: false, error: "NOT_FOUND", path: url.pathname });
  } catch (e) {
    return send(res, 500, {
      ok: false,
      error: "GUARD_ERROR",
      message: String(e.message || e)
    });
  }
});

server.on("error", e => {
  console.error("ndsp-access-guard-final server error:", e);
  process.exit(1);
});

server.listen(PORT, "127.0.0.1", () => {
  console.log("ndsp-access-guard-final listening on", PORT);
});

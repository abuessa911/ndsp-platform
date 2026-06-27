"use strict";

const http = require("http");
const fs = require("fs");
const bcrypt = require("bcryptjs");
const { Pool } = require("pg");

const PORT = Number(process.env.PORT || 9041);
const UPSTREAM = process.env.NDSP_REGISTER_UPSTREAM || "http://127.0.0.1:9019";

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

function sendJson(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let chunks = [];
    req.on("data", c => {
      chunks.push(c);
      if (Buffer.concat(chunks).length > 1024 * 1024) {
        reject(new Error("BODY_TOO_LARGE"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

async function ensureCredential({ userId, email, password }) {
  if (!userId || !email || !password) return { synced: false, reason: "MISSING_REQUIRED_FIELDS" };
  if (String(password).length < 8) return { synced: false, reason: "PASSWORD_MIN_8" };

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

  const u = await pool.query(
    "SELECT id,email,status,role,plan FROM users WHERE id::text=$1 OR lower(email)=lower($2) LIMIT 1",
    [String(userId), String(email)]
  );

  if (!u.rows[0]) return { synced: false, reason: "USER_NOT_FOUND_AFTER_REGISTER" };

  const hash = await bcrypt.hash(String(password), 12);

  await pool.query(`
    INSERT INTO access_guard_credentials (user_id, email, password_hash, disabled, updated_at)
    VALUES ($1, lower($2), $3, false, NOW())
    ON CONFLICT (user_id)
    DO UPDATE SET
      email=excluded.email,
      password_hash=excluded.password_hash,
      disabled=false,
      updated_at=NOW()
  `, [String(u.rows[0].id), String(email).toLowerCase(), hash]);

  return {
    synced: true,
    user_id: String(u.rows[0].id),
    email: String(u.rows[0].email),
    status: String(u.rows[0].status || ""),
    role: String(u.rows[0].role || ""),
    plan: String(u.rows[0].plan || "")
  };
}

async function proxyRegister(req, res) {
  const rawBody = await readBody(req);
  let payload = {};
  try { payload = rawBody ? JSON.parse(rawBody) : {}; } catch (_) {}

  const password =
    payload.password ||
    payload.confirm_password && payload.password ||
    payload.password_confirm && payload.password ||
    "";

  const email = String(payload.email || "").trim().toLowerCase();

  if (req.method === "POST" && req.url.includes("/api/trial/register/")) {
    if (!email) return sendJson(res, 400, { ok: false, error: "EMAIL_REQUIRED" });
    if (!password || String(password).length < 8) {
      return sendJson(res, 400, { ok: false, error: "PASSWORD_MIN_8" });
    }
  }

  const target = new URL(req.url, UPSTREAM);
  const headers = Object.assign({}, req.headers);
  headers.host = target.host;
  headers["content-length"] = Buffer.byteLength(rawBody);

  const upstreamResp = await fetch(target.toString(), {
    method: req.method,
    headers,
    body: ["GET", "HEAD"].includes(req.method) ? undefined : rawBody,
    redirect: "manual"
  });

  const text = await upstreamResp.text();
  let data = null;
  try { data = JSON.parse(text); } catch (_) {}

  let credentialSync = null;

  if (
    req.method === "POST" &&
    upstreamResp.status >= 200 &&
    upstreamResp.status < 300 &&
    data &&
    data.ok === true &&
    data.user_id &&
    email &&
    password
  ) {
    try {
      credentialSync = await ensureCredential({
        userId: data.user_id,
        email,
        password
      });
      data.credential_sync = credentialSync;
    } catch (e) {
      data.credential_sync = { synced: false, reason: String(e.message || e) };
      data.warning = "REGISTERED_BUT_CREDENTIAL_SYNC_FAILED";
    }
  }

  const outBody = data ? JSON.stringify(data) : text;
  const outHeaders = {
    "Content-Type": data ? "application/json; charset=utf-8" : (upstreamResp.headers.get("content-type") || "text/plain"),
    "Cache-Control": "no-store"
  };

  res.writeHead(upstreamResp.status, outHeaders);
  res.end(outBody);
}

const server = http.createServer(async (req, res) => {
  try {
    if (req.url === "/health" || req.url === "/api/trial/register/health") {
      return sendJson(res, 200, {
        ok: true,
        service: "ndsp-trial-register-canonical-wrapper",
        port: PORT,
        upstream: UPSTREAM,
        credentials_sync: true,
        database: "ndsp_auth"
      });
    }

    if (req.url.startsWith("/api/trial/register/")) {
      return await proxyRegister(req, res);
    }

    return sendJson(res, 404, { ok: false, error: "NOT_FOUND" });
  } catch (e) {
    return sendJson(res, 500, {
      ok: false,
      error: "WRAPPER_FAILED",
      detail: String(e.message || e)
    });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`ndsp-trial-register-canonical-wrapper listening on ${PORT}, upstream=${UPSTREAM}`);
});

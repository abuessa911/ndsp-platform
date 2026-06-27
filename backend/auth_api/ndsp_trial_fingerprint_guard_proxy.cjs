"use strict";

const http = require("http");
const crypto = require("crypto");
const { Pool } = require("pg");

const PORT = Number(process.env.NDSP_FP_GUARD_PORT || 9070);
const TARGET_HOST = process.env.NDSP_TRIAL_REGISTER_HOST || "127.0.0.1";
const TARGET_PORT = Number(process.env.NDSP_TRIAL_REGISTER_PORT || 9019);

function dbConfig() {
  const cs = process.env.DATABASE_URL || process.env.POSTGRES_URL || process.env.NDSP_DATABASE_URL;
  if (cs) return { connectionString: cs };
  return {
    host: process.env.PGHOST || process.env.POSTGRES_HOST || "127.0.0.1",
    port: Number(process.env.PGPORT || process.env.POSTGRES_PORT || 5432),
    database: process.env.PGDATABASE || process.env.POSTGRES_DB || "ndsp_auth",
    user: process.env.PGUSER || process.env.POSTGRES_USER || "postgres",
    password: process.env.PGPASSWORD || process.env.POSTGRES_PASSWORD || undefined
  };
}

const pool = new Pool(dbConfig());

function sendJson(res, status, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "content-length": Buffer.byteLength(body)
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let chunks = [];
    let size = 0;
    req.on("data", (c) => {
      size += c.length;
      if (size > 1024 * 1024) {
        reject(new Error("BODY_TOO_LARGE"));
        req.destroy();
        return;
      }
      chunks.push(c);
    });
    req.on("end", () => resolve(Buffer.concat(chunks)));
    req.on("error", reject);
  });
}

function tryJson(buf) {
  try { return JSON.parse(buf.toString("utf8") || "{}"); }
  catch { return {}; }
}

function extractFingerprint(req, body) {
  const h = req.headers || {};
  const candidates = [
    body && body.fingerprint,
    body && body.device_fingerprint,
    body && body.browser_fingerprint,
    body && body.client_fingerprint,
    body && body.fingerprint_hash,
    body && body.device_id,
    body && body.visitor_id,
    h["x-ndsp-fingerprint"],
    h["x-device-fingerprint"],
    h["x-browser-fingerprint"],
    h["x-client-fingerprint"],
    h["x-fingerprint"],
    h["x-device-id"],
    h["x-visitor-id"]
  ];

  for (const v of candidates) {
    const s = String(v || "").trim();
    if (s && s.length >= 8) return s.slice(0, 512);
  }
  return "";
}

function fingerprintHash(raw) {
  return crypto.createHash("sha256").update(String(raw), "utf8").digest("hex");
}

function modeFromPath(pathname) {
  if (pathname.endsWith("/ordinary")) return "ordinary";
  if (pathname.endsWith("/professional")) return "professional";
  if (pathname.endsWith("/private-invite")) return "private-invite";
  return "unknown";
}

async function claimFingerprint(hash, email, mode, ip) {
  const r = await pool.query(
    `INSERT INTO public.ndsp_trial_fingerprint_guard
      (fingerprint_hash, first_email, first_mode, first_ip, status)
     VALUES ($1,$2,$3,$4,'PENDING')
     ON CONFLICT (fingerprint_hash) DO NOTHING
     RETURNING id`,
    [hash, email || null, mode || null, ip || null]
  );

  if (r.rowCount === 0) return { ok: false };
  return { ok: true, id: r.rows[0].id };
}

async function releaseClaim(id) {
  if (!id) return;
  await pool.query(
    `DELETE FROM public.ndsp_trial_fingerprint_guard
     WHERE id=$1 AND status='PENDING'`,
    [id]
  ).catch(() => null);
}

async function acceptClaim(id, userId) {
  if (!id) return;
  await pool.query(
    `UPDATE public.ndsp_trial_fingerprint_guard
     SET status='ACCEPTED', first_user_id=$2, accepted_at=now()
     WHERE id=$1`,
    [id, userId ? String(userId) : null]
  ).catch(() => null);
}

function forwardToTrialGateway(req, rawBody) {
  return new Promise((resolve, reject) => {
    const headers = { ...req.headers };
    delete headers.host;
    headers["content-length"] = Buffer.byteLength(rawBody);

    const upstream = http.request({
      hostname: TARGET_HOST,
      port: TARGET_PORT,
      method: req.method,
      path: req.url,
      headers
    }, (up) => {
      const chunks = [];
      up.on("data", (c) => chunks.push(c));
      up.on("end", () => {
        resolve({
          statusCode: up.statusCode || 502,
          headers: up.headers || {},
          body: Buffer.concat(chunks)
        });
      });
    });

    upstream.on("error", reject);
    upstream.write(rawBody);
    upstream.end();
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://127.0.0.1");

  if (req.method === "GET" && url.pathname === "/health") {
    try {
      await pool.query("SELECT 1");
      return sendJson(res, 200, { ok: true, service: "ndsp-trial-fingerprint-guard", target: `${TARGET_HOST}:${TARGET_PORT}` });
    } catch (e) {
      return sendJson(res, 500, { ok: false, error: "DB_NOT_READY" });
    }
  }

  const isRegister =
    req.method === "POST" &&
    /^\/api\/trial\/register\/(ordinary|professional|private-invite)$/.test(url.pathname);

  if (!isRegister) {
    return sendJson(res, 404, { ok: false, error: "NOT_FOUND" });
  }

  let raw;
  try {
    raw = await readBody(req);
  } catch (e) {
    return sendJson(res, 413, { ok: false, error: "BODY_TOO_LARGE" });
  }

  const body = tryJson(raw);
  const email = String(body.email || body.username || "").trim().toLowerCase();
  const fp = extractFingerprint(req, body);
  const mode = modeFromPath(url.pathname);
  const ip = String(req.headers["x-forwarded-for"] || req.socket.remoteAddress || "").split(",")[0].trim();

  let claim = null;

  try {
    if (fp) {
      const hash = fingerprintHash(fp);
      claim = await claimFingerprint(hash, email, mode, ip);

      if (!claim.ok) {
        return sendJson(res, 409, {
          ok: false,
          error: "FINGERPRINT_ALREADY_EXISTS",
          message: "Device fingerprint already used for a trial registration."
        });
      }
    }

    const up = await forwardToTrialGateway(req, raw);
    let parsed = {};
    try { parsed = JSON.parse(up.body.toString("utf8") || "{}"); } catch {}

    const accepted = up.statusCode >= 200 && up.statusCode < 300 && parsed && parsed.ok === true;

    if (claim && claim.ok) {
      if (accepted) {
        await acceptClaim(claim.id, parsed.user_id || parsed.id || null);
      } else {
        await releaseClaim(claim.id);
      }
    }

    const ct = up.headers["content-type"] || "application/json; charset=utf-8";
    res.writeHead(up.statusCode, {
      "content-type": ct,
      "cache-control": "no-store"
    });
    res.end(up.body);
  } catch (e) {
    if (claim && claim.ok) await releaseClaim(claim.id);
    return sendJson(res, 502, { ok: false, error: "FINGERPRINT_GUARD_UPSTREAM_FAILED" });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[NDSP] trial fingerprint guard listening on 127.0.0.1:${PORT}, target=${TARGET_HOST}:${TARGET_PORT}`);
});

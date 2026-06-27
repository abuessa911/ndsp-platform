const http = require("http");
const fs = require("fs");
const { Pool } = require("pg");

const ENV_FILE = "/home/nawaf511/empire-core-new/backend/.env";
const HOST = "127.0.0.1";
const PORT = 9064;

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

function sendJson(res, code, obj) {
  const raw = Buffer.from(JSON.stringify(obj), "utf8");
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Content-Length": raw.length
  });
  res.end(raw);
}

function n(v, fallback) {
  const x = Number(v);
  return Number.isFinite(x) ? x : fallback;
}

async function getLimits() {
  const defaults = { ordinary: 25, specialist: 10, private: 15 };

  try {
    const r = await pool.query(`
      SELECT lower(cohort_code::text) AS code, max_seats
      FROM public.ndsp_trial_seat_status
      WHERE is_active IS DISTINCT FROM false
    `);

    for (const row of r.rows) {
      const code = String(row.code || "").toLowerCase();
      const seats = n(row.max_seats, null);
      if (!seats) continue;

      if (["beginner", "ordinary", "s1"].includes(code)) defaults.ordinary = seats;
      if (["academic", "specialist", "professional", "s2"].includes(code)) defaults.specialist = seats;
      if (["premium", "private", "private_invite", "s3"].includes(code)) defaults.private = seats;
    }
  } catch (_) {}

  return defaults;
}


async function getUserCounts() {
  const r = await pool.query(`
    SELECT
      COUNT(*) FILTER (
        WHERE lower(coalesce(trial_segment,'')) IN ('ordinary','beginner','normal_beginner','ordinary_beginner','s1')
           OR lower(coalesce(approved_segment,'')) IN ('ordinary','beginner','normal_beginner','ordinary_beginner','s1')
           OR lower(coalesce(requested_segment,'')) IN ('ordinary','beginner','normal_beginner','ordinary_beginner','s1')
           OR lower(coalesce(category,'')) IN ('ordinary','beginner','normal_beginner','ordinary_beginner','s1')
           OR lower(coalesce(account_type,'')) IN ('ordinary','beginner','normal_beginner','ordinary_beginner','s1')
      )::int AS ordinary,

      COUNT(*) FILTER (
        WHERE lower(coalesce(trial_segment,'')) IN ('professional','specialist','academic','specialist_academic','s2')
           OR lower(coalesce(approved_segment,'')) IN ('professional','specialist','academic','specialist_academic','s2')
           OR lower(coalesce(requested_segment,'')) IN ('professional','specialist','academic','specialist_academic','s2')
           OR lower(coalesce(category,'')) IN ('professional','specialist','academic','specialist_academic','s2')
           OR lower(coalesce(account_type,'')) IN ('professional','specialist','academic','specialist_academic','s2')
      )::int AS specialist,

      COUNT(*) FILTER (
        WHERE lower(coalesce(trial_segment,'')) IN ('private','private_invite','premium','private_premium','s3')
           OR lower(coalesce(approved_segment,'')) IN ('private','private_invite','premium','private_premium','s3')
           OR lower(coalesce(requested_segment,'')) IN ('private','private_invite','premium','private_premium','s3')
           OR lower(coalesce(category,'')) IN ('private','private_invite','premium','private_premium','s3')
           OR lower(coalesce(account_type,'')) IN ('private','private_invite','premium','private_premium','s3')
      )::int AS private
    FROM public.users
    WHERE lower(coalesce(role,'')) NOT IN ('admin','owner','super_admin');
  `);

  const row = r.rows[0] || {};
  return {
    ordinary: Number(row.ordinary) || 0,
    specialist: Number(row.specialist) || 0,
    private: Number(row.private) || 0
  };
}


async function getPayload() {
  const limits = await getLimits();
  const used = await getUserCounts();

  const totalCapacity = limits.ordinary + limits.specialist + limits.private;
  const totalUsed = used.ordinary + used.specialist + used.private;

  return {
    ok: true,
    source: "public.users",
    ordinary: used.ordinary,
    specialist: used.specialist,
    private: used.private,

    s1: used.ordinary,
    s2: used.specialist,
    s3: used.private,

    total: totalCapacity,
    seatTotal: totalCapacity,

    used_total: totalUsed,
    limits: {
      ordinary: limits.ordinary,
      specialist: limits.specialist,
      private: limits.private,
      total: totalCapacity
    },
    remaining: {
      ordinary: Math.max(limits.ordinary - used.ordinary, 0),
      specialist: Math.max(limits.specialist - used.specialist, 0),
      private: Math.max(limits.private - used.private, 0),
      total: Math.max(totalCapacity - totalUsed, 0)
    },
    generated_at: new Date().toISOString()
  };
}

async function handler(req, res) {
  try {
    const url = new URL(req.url, "http://127.0.0.1");

    if (req.method === "OPTIONS") {
      return sendJson(res, 200, { ok: true });
    }

    if (req.method === "GET" && url.pathname === "/api/trial/seats") {
      return sendJson(res, 200, await getPayload());
    }

    return sendJson(res, 404, { ok: false, error: "NOT_FOUND", path: url.pathname });
  } catch (e) {
    return sendJson(res, 500, {
      ok: false,
      error: "SERVER_ERROR",
      message: String(e.message || e).slice(0, 180)
    });
  }
}

http.createServer(handler).listen(PORT, HOST, () => {
  console.log(`NDSP trial seats API V40 listening on ${HOST}:${PORT}`);
});

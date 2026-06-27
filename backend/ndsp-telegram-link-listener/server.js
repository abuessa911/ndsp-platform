const https = require("https");
const fs = require("fs");
const crypto = require("crypto");
const { Pool } = require("pg");

const ROOT = "/home/nawaf511/empire-core-new";
const ENV_FILE = `${ROOT}/backend/.env`;
const OFFSET_FILE = `${ROOT}/backend/ndsp-telegram-link-listener/offset.json`;

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

const TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", "NDSP_TELEGRAM_BOT_TOKEN", "BOT_TOKEN");

const pool = new Pool({
  host: env("PGHOST", "POSTGRES_HOST", "DB_HOST") || "127.0.0.1",
  port: Number(env("PGPORT", "POSTGRES_PORT") || 5432),
  database: env("PGDATABASE", "POSTGRES_DB", "POSTGRES_DATABASE", "DB_DATABASE") || "ndsp_auth",
  user: env("PGUSER", "POSTGRES_USER", "DB_USER"),
  password: env("PGPASSWORD", "POSTGRES_PASSWORD", "DB_PASSWORD"),
});

function sha(v) {
  return crypto.createHash("sha256").update(String(v)).digest("hex");
}

function readOffset() {
  try {
    const j = JSON.parse(fs.readFileSync(OFFSET_FILE, "utf8"));
    return Number(j.offset || 0);
  } catch (_) {
    return 0;
  }
}

function writeOffset(offset) {
  try {
    fs.writeFileSync(OFFSET_FILE, JSON.stringify({ offset, updated_at: new Date().toISOString() }, null, 2));
  } catch (_) {}
}

function tgApi(method, params = {}) {
  return new Promise((resolve, reject) => {
    if (!TELEGRAM_BOT_TOKEN) return reject(new Error("TELEGRAM_BOT_TOKEN_MISSING"));

    const qs = new URLSearchParams(params).toString();
    const path = `/bot${TELEGRAM_BOT_TOKEN}/${method}${qs ? "?" + qs : ""}`;

    const req = https.request({
      hostname: "api.telegram.org",
      method: "GET",
      path,
      timeout: 35000,
    }, (res) => {
      let data = "";
      res.on("data", chunk => data += chunk);
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error("BAD_TELEGRAM_JSON"));
        }
      });
    });

    req.on("error", reject);
    req.on("timeout", () => {
      req.destroy(new Error("TELEGRAM_TIMEOUT"));
    });

    req.end();
  });
}

async function sendMessage(chatId, text) {
  try {
    await tgApi("sendMessage", {
      chat_id: String(chatId),
      text,
      disable_web_page_preview: "true",
    });
  } catch (e) {
    console.error("SEND_MESSAGE_FAILED", String(e.message || e).slice(0, 120));
  }
}

function extractCode(text) {
  text = String(text || "").trim().toUpperCase();

  const patterns = [
    /\bNDSP-[A-F0-9]{8}\b/,
    /\bNDSP-LINK-[A-Z0-9]{4,16}\b/,
    /\bNDSP-[A-Z0-9]{4,16}\b/
  ];

  for (const p of patterns) {
    const m = text.match(p);
    if (m) return m[0];
  }

  return "";
}

async function linkCodeToChat(code, msg) {
  const chat = msg.chat || {};
  const from = msg.from || {};
  const chatId = String(chat.id || "");
  const username = String(from.username || chat.username || "");
  const firstName = String(from.first_name || "");
  const lastName = String(from.last_name || "");

  if (!chatId) return false;

  const codeHash = sha(code);

  const r = await pool.query(`
    SELECT id, user_id, user_email, email
    FROM public.user_alert_channels
    WHERE telegram_link_code_hash=$1
      AND telegram_link_expires_at > NOW()
      AND telegram_verified=false
    ORDER BY telegram_link_started_at DESC NULLS LAST
    LIMIT 1
  `, [codeHash]);

  if (!r.rowCount) {
    await sendMessage(
      chatId,
      "NDSP ❌ الكود غير صحيح أو منتهي.\nارجع للمنصة واضغط ربط تيليجرام للحصول على كود جديد."
    );
    return false;
  }

  const row = r.rows[0];

  await pool.query(`
    UPDATE public.user_alert_channels
    SET telegram_chat_id=$2,
        telegram_username=$3,
        telegram_verified=true,
        telegram_link_code_hash=NULL,
        telegram_link_expires_at=NULL,
        updated_at=NOW()
    WHERE id=$1
  `, [row.id, chatId, username || `${firstName} ${lastName}`.trim() || null]);

  await sendMessage(
    chatId,
    "NDSP ✅ تم ربط تيليجرام بحسابك بنجاح.\nستصلك التنبيهات الخاصة بحسابك فقط.\nتنبيه: إشعارات NDSP ليست توصيات مالية أو أوامر تنفيذ."
  );

  console.log("LINK_OK user_id=", row.user_id, "chat_id_masked=", chatId.slice(0, 4) + "..." + chatId.slice(-4));
  return true;
}

async function handleMessage(msg) {
  const text = String(msg.text || msg.caption || "").trim();
  const chatId = msg.chat && msg.chat.id;

  if (!text) return;

  if (text === "/start" || text.toLowerCase() === "start") {
    await sendMessage(
      chatId,
      "أهلًا بك في بوت NDSP.\nلربط حسابك: افتح صفحة إعدادات التنبيهات في المنصة، اضغط ربط تيليجرام، ثم أرسل الكود هنا."
    );
    return;
  }

  const code = extractCode(text);

  if (!code) {
    return;
  }

  await linkCodeToChat(code, msg);
}

async function pollOnce() {
  const offset = readOffset();

  const data = await tgApi("getUpdates", {
    timeout: "25",
    offset: String(offset || 0),
    allowed_updates: JSON.stringify(["message"])
  });

  if (!data || data.ok !== true) {
    console.error("GET_UPDATES_NOT_OK");
    return;
  }

  let nextOffset = offset;

  for (const upd of data.result || []) {
    if (upd.update_id >= nextOffset) nextOffset = upd.update_id + 1;

    try {
      if (upd.message) await handleMessage(upd.message);
    } catch (e) {
      console.error("HANDLE_UPDATE_FAILED", String(e.message || e).slice(0, 180));
    }
  }

  if (nextOffset !== offset) writeOffset(nextOffset);
}

async function main() {
  if (!TELEGRAM_BOT_TOKEN) {
    console.error("TELEGRAM_BOT_TOKEN_MISSING");
    process.exit(1);
  }

  await pool.query("SELECT 1");
  console.log("NDSP Telegram link listener V36 started");

  while (true) {
    try {
      await pollOnce();
    } catch (e) {
      console.error("POLL_FAILED", String(e.message || e).slice(0, 160));
      await new Promise(r => setTimeout(r, 5000));
    }
  }
}

main().catch(e => {
  console.error("FATAL", String(e.message || e).slice(0, 200));
  process.exit(1);
});

const express = require('express');
const crypto = require('crypto');
const bcrypt = require('bcrypt');
const nodemailer = require('nodemailer');
const { Pool } = require('pg');

const PORT = 9027;
const DATABASE_URL = process.env.DATABASE_URL || process.env.POSTGRES_URL;

const pool = new Pool(
  DATABASE_URL
    ? { connectionString: DATABASE_URL }
    : {
        host: process.env.PGHOST || '127.0.0.1',
        port: Number(process.env.PGPORT || 5432),
        database: process.env.PGDATABASE || 'ndsp_auth',
        user: process.env.PGUSER || 'postgres',
        password: process.env.PGPASSWORD || process.env.POSTGRES_PASSWORD,
      }
);

const mailer = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.SMTP_USER || 'ndsp.app@gmail.com',
    pass: process.env.SMTP_PASS || process.env.SMTP_PASSWORD,
  },
});

const app = express();
app.use(express.json({ limit: '256kb' }));

function token() {
  return crypto.randomBytes(32).toString('hex');
}

function html(name, link) {
  return `
<!doctype html>
<html lang="ar" dir="rtl">
<body style="margin:0;background:#070A10;color:#fff;font-family:Arial,sans-serif;padding:24px">
  <div style="max-width:620px;margin:auto;border:1px solid #D9B65A;border-radius:10px;overflow:hidden">
    <div style="background:#D9B65A;color:#070A10;text-align:center;padding:24px">
      <h1 style="margin:0">NDSP</h1>
    </div>
    <div style="padding:28px">
      <p>مرحباً ${name || 'NDSP User'},</p>
      <p>طلبت إعادة تعيين كلمة المرور لحسابك في NDSP.</p>
      <p>Hello ${name || 'NDSP User'}, you requested to reset your password.</p>
      <p style="text-align:center;margin:30px 0">
        <a href="${link}" style="background:#D9B65A;color:#070A10;padding:14px 28px;border-radius:6px;text-decoration:none;font-weight:bold">
          Reset Password / إعادة تعيين كلمة المرور
        </a>
      </p>
      <p style="color:#F2D27A">الرابط صالح لمدة ساعة واحدة فقط.</p>
      <p style="direction:ltr;word-break:break-all;background:#0a0d14;padding:12px;border:1px solid #333">${link}</p>
    </div>
  </div>
</body>
</html>`;
}

app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ ok: true, service: 'ndsp-password-reset-gateway', db: true });
  } catch (e) {
    res.status(500).json({ ok: false, service: 'ndsp-password-reset-gateway', error: 'DB_ERROR' });
  }
});

app.post('/api/auth/forgot-password', async (req, res) => {
  try {
    const email = String((req.body || {}).email || '').toLowerCase().trim();
    if (!email) return res.status(400).json({ success: false, message: 'Email is required' });

    const safe = { success: true, message: 'If this email exists, a reset link has been sent' };

    const q = await pool.query(
      'SELECT id, name, email FROM users WHERE LOWER(email) = $1 LIMIT 1',
      [email]
    );

    if (!q.rows.length) return res.json(safe);

    const user = q.rows[0];
    const resetToken = token();
    const expires = new Date(Date.now() + 60 * 60 * 1000);

    await pool.query(
      `UPDATE users
       SET password_reset_token=$1,
           password_reset_expires_at=$2
       WHERE id=$3`,
      [resetToken, expires, user.id]
    );

    const frontend = process.env.FRONTEND_URL || 'https://ndsp.app';
    const link = `${frontend}/reset-password.html?token=${resetToken}&email=${encodeURIComponent(user.email)}`;

    await mailer.sendMail({
      from: process.env.SMTP_FROM || 'NDSP <ndsp.app@gmail.com>',
      to: user.email,
      subject: 'NDSP — Reset Your Password / إعادة تعيين كلمة المرور',
      html: html(user.name, link),
    });

    res.json(safe);
  } catch (e) {
    console.error('forgot-password error:', e);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

app.post('/api/auth/reset-password', async (req, res) => {
  try {
    const email = String((req.body || {}).email || '').toLowerCase().trim();
    const resetToken = String((req.body || {}).token || '').trim();
    const newPassword = String((req.body || {}).newPassword || '');

    if (!email) return res.status(400).json({ success: false, message: 'Email is required' });
    if (!resetToken) return res.status(400).json({ success: false, message: 'Invalid or missing reset token' });
    if (newPassword.length < 8) return res.status(400).json({ success: false, message: 'Password must be at least 8 characters' });

    const q = await pool.query(
      `SELECT id, email, password_reset_expires_at
       FROM users
       WHERE LOWER(email)=$1
         AND password_reset_token=$2
       LIMIT 1`,
      [email, resetToken]
    );

    if (!q.rows.length) {
      return res.status(400).json({ success: false, message: 'Invalid reset token or email' });
    }

    const user = q.rows[0];

    if (!user.password_reset_expires_at || new Date(user.password_reset_expires_at) < new Date()) {
      return res.status(400).json({ success: false, message: 'Reset token has expired. Please request a new one.' });
    }

    const hash = await bcrypt.hash(newPassword, 10);

    await pool.query(
      `UPDATE users
       SET password_hash=$1,
           password_reset_token=NULL,
           password_reset_expires_at=NULL
       WHERE id=$2`,
      [hash, user.id]
    );

    res.json({ success: true, message: 'Password has been reset successfully. You can now log in.' });
  } catch (e) {
    console.error('reset-password error:', e);
    res.status(500).json({ success: false, message: 'Internal server error' });
  }
});

app.listen(PORT, '127.0.0.1', () => {
  console.log(`NDSP password reset gateway listening on ${PORT}`);
});

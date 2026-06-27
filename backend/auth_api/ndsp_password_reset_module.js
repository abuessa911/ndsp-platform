const crypto = require('crypto');
const nodemailer = require('nodemailer');
const bcrypt = require('bcrypt');

const emailTransporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.SMTP_USER || 'ndsp.app@gmail.com',
    pass: process.env.SMTP_PASS || process.env.SMTP_PASSWORD,
  },
});

emailTransporter.verify((err, success) => {
  if (err) {
    console.error('❌ Email transporter error:', err.message);
  } else {
    console.log('✅ Email transporter ready');
  }
});

function generateResetToken() {
  return crypto.randomBytes(32).toString('hex');
}

function getResetEmailHTML(userName, resetLink) {
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>body{font-family:'Sora',sans-serif;background:#070A10;color:#fff;margin:0;padding:0}.container{max-width:600px;margin:0 auto;background:#070A10;border:1px solid #D9B65A;border-radius:8px}.header{background:linear-gradient(135deg,#D9B65A 0%,#F2D27A 100%);padding:24px;text-align:center;border-bottom:2px solid #070A10}.header h1{color:#070A10;margin:0;font-size:28px}.content{padding:32px 24px}.footer{background:#0a0d14;padding:20px;text-align:center;border-top:1px solid #D9B65A;font-size:12px;color:#888}.cta-button{display:inline-block;background:linear-gradient(135deg,#D9B65A 0%,#F2D27A 100%);color:#070A10;padding:14px 32px;border-radius:6px;text-decoration:none;font-weight:700;margin:24px 0}.warning{background:rgba(217,182,90,0.1);border-left:4px solid #D9B65A;padding:12px 16px;margin:20px 0;border-radius:4px}</style></head><body><div class="container"><div class="header"><h1>NDSP</h1></div><div class="content"><p>مرحباً ${userName},</p><p>طلبت إعادة تعيين كلمة المرور.</p><p><strong>Hello ${userName},</strong></p><p>You requested to reset your password.</p><p style="text-align:center;margin:32px 0"><a href="${resetLink}" class="cta-button">Reset Password</a></p><div class="warning">⚠️ This link expires in <strong>1 hour</strong>.</div></div><div class="footer"><p>© 2026 NDSP Platform. All rights reserved.</p></div></div></body></html>`;
}

async function handleForgotPassword(req, res, db) {
  try {
    const { email } = req.body;
    if (!email || typeof email !== 'string' || email.trim() === '') {
      return res.status(400).json({ success: false, message: 'Email is required' });
    }
    const normalizedEmail = email.toLowerCase().trim();
    const userResult = await db.query('SELECT id, name, email FROM users WHERE LOWER(email) = $1', [normalizedEmail]);
    if (userResult.rows.length === 0) {
      return res.status(200).json({ success: true, message: 'If this email exists, a reset link has been sent' });
    }
    const user = userResult.rows[0];
    const resetToken = generateResetToken();
    const expiresAt = new Date(Date.now() + 60 * 60 * 1000);
    await db.query('UPDATE users SET password_reset_token = $1, password_reset_expires_at = $2 WHERE id = $3', [resetToken, expiresAt, user.id]);
    const resetLink = `${process.env.FRONTEND_URL || 'https://ndsp.app'}/reset-password.html?token=${resetToken}&email=${encodeURIComponent(user.email)}`;
    const mailOptions = {
      from: process.env.SMTP_FROM || 'NDSP <ndsp.app@gmail.com>',
      to: user.email,
      subject: 'NDSP — Reset Your Password',
      html: getResetEmailHTML(user.name, resetLink),
    };
    await emailTransporter.sendMail(mailOptions);
    console.log(`✅ Password reset email sent to: ${user.email}`);
    return res.status(200).json({ success: true, message: 'If this email exists, a reset link has been sent' });
  } catch (error) {
    console.error('❌ Forgot password error:', error);
    return res.status(500).json({ success: false, message: 'Internal server error' });
  }
}

async function handleResetPassword(req, res, db) {
  try {
    const { token, email, newPassword } = req.body;
    if (!token || typeof token !== 'string') {
      return res.status(400).json({ success: false, message: 'Invalid or missing reset token' });
    }
    if (!email || typeof email !== 'string') {
      return res.status(400).json({ success: false, message: 'Email is required' });
    }
    if (!newPassword || typeof newPassword !== 'string' || newPassword.length < 8) {
      return res.status(400).json({ success: false, message: 'Password must be at least 8 characters' });
    }
    const normalizedEmail = email.toLowerCase().trim();
    const now = new Date();
    const userResult = await db.query('SELECT id, name, email, password_reset_token, password_reset_expires_at FROM users WHERE LOWER(email) = $1 AND password_reset_token = $2', [normalizedEmail, token]);
    if (userResult.rows.length === 0) {
      return res.status(400).json({ success: false, message: 'Invalid reset token or email' });
    }
    const user = userResult.rows[0];
    if (!user.password_reset_expires_at || new Date(user.password_reset_expires_at) < now) {
      return res.status(400).json({ success: false, message: 'Reset token has expired. Please request a new one.' });
    }
    const passwordHash = await bcrypt.hash(newPassword, 10);
    await db.query('UPDATE users SET password_hash = $1, password_reset_token = NULL, password_reset_expires_at = NULL WHERE id = $2', [passwordHash, user.id]);
    console.log(`✅ Password reset successful for user: ${user.email}`);
    return res.status(200).json({ success: true, message: 'Password has been reset successfully. You can now log in.' });
  } catch (error) {
    console.error('❌ Reset password error:', error);
    return res.status(500).json({ success: false, message: 'Internal server error' });
  }
}

module.exports = { handleForgotPassword, handleResetPassword, generateResetToken, emailTransporter };

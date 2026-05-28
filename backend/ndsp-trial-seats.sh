#!/bin/bash

# NDSP canonical DB env loader
if [ -f /etc/ndsp/ndsp-db.env ]; then
  set -a
  . /etc/ndsp/ndsp-db.env
  set +a
fi
DB_NAME="${DB_NAME:-ndsp_auth}"
PGDATABASE="${PGDATABASE:-ndsp_auth}"
# /NDSP canonical DB env loader

# ═══════════════════════════════════════════════════════════════════
# NDSP — نظام مقاعد التجربة
# 10 أكاديمي + 25 مبتدئ + 15 مميز = 50 مقعداً
# ═══════════════════════════════════════════════════════════════════

set -e

PROJECT_ROOT="/var/www/ndsp"
FRONTEND_DIR="${PROJECT_ROOT}/frontend"
BACKEND_DIR="${PROJECT_ROOT}/backend"
DB_NAME="${DB_NAME:-ndsp_auth}"
DB_USER="ndsp_user"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1) Database — جدول المقاعد + segments للمستخدمين
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
log "[1/5] إعداد قاعدة البيانات..."

cat > /tmp/ndsp_seats.sql << 'SQL'
-- جدول أنواع المقاعد
CREATE TABLE IF NOT EXISTS trial_segments (
  id SERIAL PRIMARY KEY,
  code VARCHAR(20) UNIQUE NOT NULL,
  name_ar VARCHAR(100) NOT NULL,
  name_en VARCHAR(100) NOT NULL,
  total_seats INTEGER NOT NULL,
  used_seats INTEGER DEFAULT 0,
  description TEXT,
  trial_days INTEGER DEFAULT 16,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- إدراج الـ Segments الثلاثة
INSERT INTO trial_segments (code, name_ar, name_en, total_seats, description, trial_days)
VALUES
  ('academic', 'متخصص أكاديمي', 'Academic Specialist', 10,
   'مقاعد للباحثين والأكاديميين المتخصصين في الأسواق المالية', 16),
  ('beginner', 'مستخدم مبتدئ', 'Beginner User', 25,
   'مقاعد للمستخدمين الجدد لاختبار وضوح المنصة', 16),
  ('premium', 'خاص مميز', 'Premium Invited', 15,
   'مقاعد بدعوة خاصة للمستخدمين المختارين', 16)
ON CONFLICT (code) DO NOTHING;

-- إضافة segment لجدول المستخدمين
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS segment_code VARCHAR(20) REFERENCES trial_segments(code),
  ADD COLUMN IF NOT EXISTS seat_number INTEGER,
  ADD COLUMN IF NOT EXISTS invitation_code VARCHAR(50);

CREATE INDEX IF NOT EXISTS idx_users_segment ON users(segment_code);
CREATE INDEX IF NOT EXISTS idx_users_invitation ON users(invitation_code);

-- جدول رموز الدعوة (للمقاعد المميزة)
CREATE TABLE IF NOT EXISTS invitation_codes (
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  segment_code VARCHAR(20) REFERENCES trial_segments(code),
  used_by INTEGER REFERENCES users(id),
  used_at TIMESTAMP,
  created_by INTEGER REFERENCES users(id),
  expires_at TIMESTAMP,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inv_code ON invitation_codes(code);
CREATE INDEX IF NOT EXISTS idx_inv_segment ON invitation_codes(segment_code);

-- View لإحصائيات المقاعد
CREATE OR REPLACE VIEW trial_seats_status AS
SELECT
  s.code,
  s.name_ar,
  s.name_en,
  s.total_seats,
  COUNT(u.id) AS used_seats,
  s.total_seats - COUNT(u.id) AS available_seats,
  ROUND(100.0 * COUNT(u.id) / NULLIF(s.total_seats, 0), 1) AS fill_percentage
FROM trial_segments s
LEFT JOIN users u ON u.segment_code = s.code
WHERE s.is_active = TRUE
GROUP BY s.id, s.code, s.name_ar, s.name_en, s.total_seats
ORDER BY s.id;
SQL

if command -v psql >/dev/null 2>&1; then
  PGPASSWORD="${DB_PASSWORD:-}" psql -U "$DB_USER" -d "$DB_NAME" -f /tmp/ndsp_seats.sql && log "Schema تم تطبيقه"
else
  warn "psql غير موجود — شغّل /tmp/ndsp_seats.sql يدوياً"
fi

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2) Backend — Service لإدارة المقاعد
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
log "[2/5] إنشاء seatsService.js..."

mkdir -p "$BACKEND_DIR/services"
cat > "$BACKEND_DIR/services/seatsService.js" << 'JS'
const db = require('../db');
const crypto = require('crypto');

class SeatsService {

  // الحصول على حالة المقاعد
  async getSeatsStatus() {
    const { rows } = await db.query('SELECT * FROM trial_seats_status');
    return rows;
  }

  // التحقق من توفر مقعد في segment معيّن
  async hasAvailableSeat(segmentCode) {
    const { rows } = await db.query(
      'SELECT total_seats, used_seats FROM trial_segments WHERE code = $1 AND is_active = TRUE',
      [segmentCode]
    );
    if (!rows[0]) return false;
    const used = await this.countSegmentUsers(segmentCode);
    return used < rows[0].total_seats;
  }

  async countSegmentUsers(segmentCode) {
    const { rows } = await db.query(
      'SELECT COUNT(*) AS c FROM users WHERE segment_code = $1',
      [segmentCode]
    );
    return parseInt(rows[0].c, 10);
  }

  // حجز مقعد للمستخدم
  async assignSeat(userId, segmentCode, invitationCode = null) {
    const available = await this.hasAvailableSeat(segmentCode);
    if (!available) {
      throw new Error(`SEATS_FULL:${segmentCode}`);
    }

    // إذا كان segment = premium، يجب رمز دعوة صالح
    if (segmentCode === 'premium') {
      if (!invitationCode) throw new Error('INVITATION_REQUIRED');
      const valid = await this.validateInvitation(invitationCode, 'premium');
      if (!valid) throw new Error('INVALID_INVITATION');
    }

    const seatNumber = await this.countSegmentUsers(segmentCode) + 1;

    await db.query(
      'UPDATE users SET segment_code = $1, seat_number = $2, invitation_code = $3 WHERE id = $4',
      [segmentCode, seatNumber, invitationCode, userId]
    );

    await db.query(
      'UPDATE trial_segments SET used_seats = used_seats + 1 WHERE code = $1',
      [segmentCode]
    );

    if (invitationCode) {
      await db.query(
        'UPDATE invitation_codes SET used_by = $1, used_at = NOW() WHERE code = $2',
        [userId, invitationCode]
      );
    }

    return { segmentCode, seatNumber };
  }

  // التحقق من رمز الدعوة
  async validateInvitation(code, segmentCode) {
    const { rows } = await db.query(
      `SELECT * FROM invitation_codes
       WHERE code = $1 AND segment_code = $2
         AND used_by IS NULL
         AND (expires_at IS NULL OR expires_at > NOW())`,
      [code, segmentCode]
    );
    return rows.length > 0;
  }

  // إنشاء رموز دعوة جديدة (للأدمن)
  async createInvitations(segmentCode, count, createdBy, notes = null) {
    const codes = [];
    for (let i = 0; i < count; i++) {
      const code = `NDSP-${segmentCode.toUpperCase()}-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
      await db.query(
        `INSERT INTO invitation_codes (code, segment_code, created_by, notes, expires_at)
         VALUES ($1, $2, $3, $4, NOW() + INTERVAL '30 days')`,
        [code, segmentCode, createdBy, notes]
      );
      codes.push(code);
    }
    return codes;
  }

  // قائمة رموز الدعوة لـ segment
  async listInvitations(segmentCode) {
    const { rows } = await db.query(
      `SELECT ic.*, u.email AS used_by_email
       FROM invitation_codes ic
       LEFT JOIN users u ON ic.used_by = u.id
       WHERE ic.segment_code = $1
       ORDER BY ic.created_at DESC`,
      [segmentCode]
    );
    return rows;
  }

  // إلغاء/إعادة تفعيل مقعد
  async revokeSeat(userId) {
    const { rows } = await db.query('SELECT segment_code FROM users WHERE id = $1', [userId]);
    if (!rows[0]?.segment_code) return false;

    await db.query(
      'UPDATE users SET segment_code = NULL, seat_number = NULL WHERE id = $1',
      [userId]
    );
    await db.query(
      'UPDATE trial_segments SET used_seats = GREATEST(0, used_seats - 1) WHERE code = $1',
      [rows[0].segment_code]
    );
    return true;
  }
}

module.exports = new SeatsService();
JS
log "seatsService.js مكتمل"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3) Backend Routes — المقاعد والدعوات
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
log "[3/5] إنشاء routes/seatsRoutes.js..."

cat > "$BACKEND_DIR/routes/seatsRoutes.js" << 'JS'
const express = require('express');
const router = express.Router();
const seatsService = require('../services/seatsService');
const { authenticate, isAdmin } = require('../middleware/auth');
const telegram = require('../services/telegram');

// عام — حالة المقاعد المتاحة (لعرضها في صفحة التسجيل)
router.get('/api/seats/status', async (req, res) => {
  try {
    const status = await seatsService.getSeatsStatus();
    res.json(status.map(s => ({
      code: s.code,
      name_ar: s.name_ar,
      name_en: s.name_en,
      available: s.available_seats,
      total: s.total_seats,
      full: s.available_seats <= 0
    })));
  } catch (err) {
    res.status(500).json({ error: 'failed' });
  }
});

// تسجيل في segment معيّن
router.post('/api/trial/register', authenticate, async (req, res) => {
  try {
    const { segmentCode, invitationCode } = req.body;

    if (!['academic', 'beginner', 'premium'].includes(segmentCode)) {
      return res.status(400).json({ error: 'invalid_segment' });
    }

    const result = await seatsService.assignSeat(req.user.id, segmentCode, invitationCode);

    await telegram.sendMessage(
      `🎯 تسجيل تجربة جديد\nالمستخدم: ${req.user.email}\nالنوع: ${segmentCode}\nالمقعد: #${result.seatNumber}`
    );

    res.json({ success: true, ...result });
  } catch (err) {
    const msg = err.message || '';
    if (msg.startsWith('SEATS_FULL'))      return res.status(409).json({ error: 'seats_full' });
    if (msg === 'INVITATION_REQUIRED')     return res.status(400).json({ error: 'invitation_required' });
    if (msg === 'INVALID_INVITATION')      return res.status(400).json({ error: 'invalid_invitation' });
    res.status(500).json({ error: 'failed' });
  }
});

// ── Admin routes ──
router.get('/api/admin/seats', authenticate, isAdmin, async (req, res) => {
  const status = await seatsService.getSeatsStatus();
  res.json(status);
});

router.post('/api/admin/invitations/create', authenticate, isAdmin, async (req, res) => {
  const { segmentCode, count, notes } = req.body;
  const codes = await seatsService.createInvitations(segmentCode, count, req.user.id, notes);
  res.json({ codes });
});

router.get('/api/admin/invitations/:segment', authenticate, isAdmin, async (req, res) => {
  const invs = await seatsService.listInvitations(req.params.segment);
  res.json(invs);
});

router.post('/api/admin/seats/revoke/:userId', authenticate, isAdmin, async (req, res) => {
  const ok = await seatsService.revokeSeat(parseInt(req.params.userId, 10));
  res.json({ success: ok });
});

module.exports = router;
JS
log "seatsRoutes.js مكتمل"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4) Frontend — صفحة اختيار نوع المقعد
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
log "[4/5] إنشاء pages/trial-register.html..."

cat > "$FRONTEND_DIR/pages/trial-register.html" << 'HTML'
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>اختر نوع التجربة — NDSP</title>
  <link rel="stylesheet" href="/css/ndsp-fixes.css">
  <style>
    body { background:#0d0d1a; color:#fff; font-family:system-ui,sans-serif; margin:0; }
    .seats-page { padding:2rem 1.5rem; direction:rtl; max-width:900px; margin:0 auto; }
    .seats-page h1 { font-size:24px; font-weight:500; margin-bottom:.5rem; }
    .seats-page > p { font-size:13px; color:#94a3b8; margin-bottom:2rem; }
    .seats-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:1rem; }
    .seat-card { background:#111827; border:0.5px solid rgba(255,255,255,.08); border-radius:10px; padding:1.5rem; cursor:pointer; transition:all .2s; }
    .seat-card:hover:not(.full) { border-color:#00CED1; transform:translateY(-2px); }
    .seat-card.full { opacity:.5; cursor:not-allowed; }
    .seat-card.selected { border-color:#00CED1; background:rgba(0,206,209,.05); }
    .seat-icon { font-size:32px; margin-bottom:1rem; }
    .seat-name { font-size:18px; font-weight:500; margin-bottom:.5rem; }
    .seat-name-en { font-size:11px; color:#6b7280; margin-bottom:1rem; }
    .seat-desc { font-size:12px; color:#94a3b8; line-height:1.6; margin-bottom:1rem; min-height:50px; }
    .seat-counter { display:flex; align-items:center; justify-content:space-between; padding-top:1rem; border-top:0.5px solid rgba(255,255,255,.07); }
    .seat-progress { height:4px; background:rgba(255,255,255,.05); border-radius:2px; overflow:hidden; margin-top:.5rem; }
    .seat-progress-fill { height:100%; background:linear-gradient(90deg,#00CED1,#3FDD00); transition:width .3s; }
    .available { font-size:13px; color:#00CED1; font-weight:500; }
    .full-tag  { font-size:11px; color:#ef4444; background:rgba(239,68,68,.1); padding:2px 8px; border-radius:3px; }
    .invitation-input { display:none; margin-top:1rem; }
    .invitation-input.show { display:block; }
    .invitation-input input { width:100%; padding:10px 14px; background:#0d0d1a; border:0.5px solid rgba(255,255,255,.1); border-radius:6px; color:#fff; direction:ltr; text-align:center; font-family:monospace; }
    .submit-area { margin-top:2rem; text-align:center; }
    .submit-btn { background:linear-gradient(90deg,#00CED1,#3FDD00); color:#000; padding:12px 36px; border-radius:5px; font-size:14px; font-weight:600; border:none; cursor:pointer; }
    .submit-btn:disabled { opacity:.5; cursor:not-allowed; }
    .legal-note { display:inline-block; background:rgba(255,215,0,.12); color:#FFD700; border:0.5px solid rgba(255,215,0,.25); padding:4px 14px; border-radius:4px; font-size:11px; margin-bottom:1.5rem; }
  </style>
</head>
<body>

<section class="seats-page">
  <div class="legal-note">⚠️ أداة تعليمية — ليست نصائح استثمارية</div>
  <h1>اختر نوع التجربة المناسب</h1>
  <p>المقاعد محدودة وتخضع للمراجعة. مدة كل تجربة 16 يوماً.</p>

  <div class="seats-grid" id="seatsGrid"></div>

  <div class="invitation-input" id="invitationBox">
    <label style="font-size:12px;color:#94a3b8;display:block;margin-bottom:6px">رمز الدعوة (للمقاعد المميزة)</label>
    <input type="text" id="invitationCode" placeholder="NDSP-PREMIUM-XXXXXXXX">
  </div>

  <div class="submit-area">
    <button class="submit-btn" id="submitBtn" disabled onclick="register()">ابدأ التجربة</button>
  </div>
</section>

<script>
const segments = {
  academic: { icon: '🎓', desc: 'مقاعد للباحثين والأكاديميين المتخصصين في تحليل الأسواق المالية' },
  beginner: { icon: '🌱', desc: 'مقاعد للمستخدمين الجدد لاختبار وضوح المنصة وتجربة دعم القرار' },
  premium:  { icon: '✦',  desc: 'مقاعد بدعوة خاصة. تتطلب رمز دعوة من إدارة المنصة' }
};

let selectedSegment = null;

async function loadSeats() {
  try {
    const res = await fetch('/api/seats/status');
    const data = await res.json();
    const grid = document.getElementById('seatsGrid');
    grid.innerHTML = data.map(s => {
      const meta = segments[s.code] || {};
      const pct = Math.round(100 * (s.total - s.available) / s.total);
      return `
        <div class="seat-card ${s.full ? 'full' : ''}" data-code="${s.code}" onclick="selectSeat('${s.code}', ${s.full})">
          <div class="seat-icon">${meta.icon || '◆'}</div>
          <div class="seat-name">${s.name_ar}</div>
          <div class="seat-name-en">${s.name_en}</div>
          <div class="seat-desc">${meta.desc || ''}</div>
          <div class="seat-counter">
            ${s.full
              ? '<span class="full-tag">المقاعد مكتملة</span>'
              : `<span class="available">${s.available} / ${s.total} متاح</span>`}
          </div>
          <div class="seat-progress"><div class="seat-progress-fill" style="width:${pct}%"></div></div>
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error(e);
  }
}

function selectSeat(code, isFull) {
  if (isFull) return;
  selectedSegment = code;
  document.querySelectorAll('.seat-card').forEach(c => c.classList.remove('selected'));
  document.querySelector(`[data-code="${code}"]`).classList.add('selected');
  document.getElementById('invitationBox').classList.toggle('show', code === 'premium');
  document.getElementById('submitBtn').disabled = false;
}

async function register() {
  const invCode = document.getElementById('invitationCode').value.trim();
  if (selectedSegment === 'premium' && !invCode) {
    alert('رمز الدعوة مطلوب للمقاعد المميزة');
    return;
  }
  try {
    const res = await fetch('/api/trial/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ segmentCode: selectedSegment, invitationCode: invCode || null })
    });
    const data = await res.json();
    if (res.ok) {
      alert(`✅ تم حجز مقعدك #${data.seatNumber}\nتجربتك تبدأ الآن — 16 يوماً`);
      location.href = '/dashboard';
    } else {
      const errors = {
        seats_full: 'هذا النوع مكتمل، اختر نوعاً آخر',
        invitation_required: 'رمز الدعوة مطلوب',
        invalid_invitation: 'رمز الدعوة غير صالح',
      };
      alert('❌ ' + (errors[data.error] || 'حدث خطأ'));
      loadSeats();
    }
  } catch (e) {
    alert('خطأ في الاتصال');
  }
}

loadSeats();
</script>

</body>
</html>
HTML
log "trial-register.html مكتمل"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5) Admin Panel — إدارة المقاعد والدعوات
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
log "[5/5] إنشاء pages/admin-seats.html..."

cat > "$FRONTEND_DIR/pages/admin-seats.html" << 'HTML'
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>إدارة المقاعد — Admin</title>
  <link rel="stylesheet" href="/css/ndsp-fixes.css">
  <style>
    body { background:#0d0d1a; color:#fff; font-family:system-ui,sans-serif; margin:0; padding:2rem; direction:rtl; }
    h1 { font-size:22px; font-weight:500; margin-bottom:1.5rem; }
    .summary { display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; margin-bottom:2rem; }
    .stat-card { background:#111827; border:0.5px solid rgba(255,255,255,.08); border-radius:8px; padding:1rem; }
    .stat-label { font-size:11px; color:#6b7280; text-transform:uppercase; margin-bottom:6px; }
    .stat-value { font-size:24px; font-weight:500; color:#00CED1; }
    .stat-sub { font-size:11px; color:#94a3b8; margin-top:4px; }
    .section { background:#111827; border:0.5px solid rgba(255,255,255,.08); border-radius:8px; padding:1.5rem; margin-bottom:1.5rem; }
    .section h2 { font-size:16px; font-weight:500; margin-bottom:1rem; }
    .invite-form { display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
    .invite-form select, .invite-form input { background:#0d0d1a; border:0.5px solid rgba(255,255,255,.1); border-radius:6px; padding:8px 12px; color:#fff; font-size:13px; }
    .invite-form button { background:#00CED1; color:#000; padding:8px 20px; border-radius:5px; border:none; font-weight:500; cursor:pointer; }
    .codes-list { background:#0d0d1a; padding:1rem; border-radius:6px; margin-top:1rem; font-family:monospace; font-size:12px; max-height:200px; overflow-y:auto; }
    .codes-list div { padding:4px 0; border-bottom:0.5px solid rgba(255,255,255,.05); display:flex; justify-content:space-between; }
    .codes-list div:last-child { border:none; }
    .used { color:#6b7280; text-decoration:line-through; }
  </style>
</head>
<body>

<h1>📊 إدارة مقاعد التجربة</h1>

<div class="summary" id="summary"></div>

<div class="section">
  <h2>إنشاء رموز دعوة (Premium)</h2>
  <div class="invite-form">
    <select id="invSegment">
      <option value="premium">خاص مميز (Premium)</option>
      <option value="academic">أكاديمي (Academic)</option>
      <option value="beginner">مبتدئ (Beginner)</option>
    </select>
    <input type="number" id="invCount" placeholder="العدد" min="1" max="50" value="5">
    <input type="text" id="invNotes" placeholder="ملاحظات (اختياري)">
    <button onclick="createInvitations()">إنشاء</button>
  </div>
  <div class="codes-list" id="newCodes" style="display:none"></div>
</div>

<div class="section">
  <h2>الرموز الموجودة</h2>
  <select id="listSegment" onchange="loadInvitations()" style="background:#0d0d1a;border:0.5px solid rgba(255,255,255,.1);border-radius:6px;padding:8px 12px;color:#fff;margin-bottom:1rem">
    <option value="premium">Premium</option>
    <option value="academic">Academic</option>
    <option value="beginner">Beginner</option>
  </select>
  <div class="codes-list" id="existingCodes"></div>
</div>

<script>
async function loadSummary() {
  const res = await fetch('/api/admin/seats');
  const data = await res.json();
  document.getElementById('summary').innerHTML = data.map(s => `
    <div class="stat-card">
      <div class="stat-label">${s.name_ar}</div>
      <div class="stat-value">${s.used_seats} / ${s.total_seats}</div>
      <div class="stat-sub">${s.available_seats} متاح — ${s.fill_percentage}% ممتلئ</div>
    </div>
  `).join('');
}

async function createInvitations() {
  const segmentCode = document.getElementById('invSegment').value;
  const count = parseInt(document.getElementById('invCount').value, 10);
  const notes = document.getElementById('invNotes').value;

  const res = await fetch('/api/admin/invitations/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ segmentCode, count, notes })
  });
  const data = await res.json();

  const el = document.getElementById('newCodes');
  el.style.display = 'block';
  el.innerHTML = '<strong style="color:#00CED1">✓ تم إنشاء ' + data.codes.length + ' رمز:</strong>' +
    data.codes.map(c => `<div>${c} <button onclick="navigator.clipboard.writeText('${c}')" style="background:none;border:none;color:#00CED1;cursor:pointer;font-size:11px">نسخ</button></div>`).join('');

  loadSummary();
  loadInvitations();
}

async function loadInvitations() {
  const seg = document.getElementById('listSegment').value;
  const res = await fetch('/api/admin/invitations/' + seg);
  const data = await res.json();
  document.getElementById('existingCodes').innerHTML = data.length
    ? data.map(i => `<div class="${i.used_by ? 'used' : ''}">
        <span>${i.code}</span>
        <span>${i.used_by_email || 'متاح'}</span>
      </div>`).join('')
    : '<div style="color:#6b7280">لا توجد رموز</div>';
}

loadSummary();
loadInvitations();
</script>

</body>
</html>
HTML
log "admin-seats.html مكتمل"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo ""
echo "═══════════════════════════════════════════════════════════════════"
log "تم تركيب نظام المقاعد بنجاح ✅"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "  📊 المقاعد:  10 أكاديمي  +  25 مبتدئ  +  15 مميز  =  50 مقعداً"
echo ""
warn "الخطوات اليدوية المتبقية:"
echo ""
echo "  1) في app.js (Backend):"
echo "     app.use(require('./routes/seatsRoutes'));"
echo ""
echo "  2) أضف الصفحات الجديدة للـ routing:"
echo "     /trial-register  →  pages/trial-register.html"
echo "     /admin/seats     →  pages/admin-seats.html (Admin only)"
echo ""
echo "  3) ربط زر التسجيل في Hero ليتجه إلى /trial-register"
echo ""
echo "  4) إنشاء رموز Premium الأولى عبر Admin Panel:"
echo "     /admin/seats  →  إنشاء 15 رمزاً لـ Premium"
echo ""
echo "  5) أعد تشغيل السيرفر:"
echo "     pm2 restart ndsp"
echo ""
echo "═══════════════════════════════════════════════════════════════════"

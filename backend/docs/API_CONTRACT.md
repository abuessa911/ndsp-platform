# NDSP API Contract

**Base URL:** `https://api.ndsp.app`  ·  **Prefix:** `/api/v1`  ·  **Format:** JSON (UTF-8)

كل ردود النجاح ملفوفة بـ `{ "data": ... }`. كل ردود الخطأ بالشكل الموحّد أدناه.

## مغلّف الخطأ الموحّد (Error format)

```json
{ "error": { "code": "STRING_CODE", "message_ar": "نص عربي", "message_en": "English text" } }
```

أكواد شائعة: `UNAUTHENTICATED` · `INVALID_CREDENTIALS` · `PENDING_REVIEW` · `FORBIDDEN` ·
`VALIDATION_ERROR` · `RATE_LIMITED` · `NOT_FOUND` · `NO_TRIAL` · `BAD_SIGNATURE` ·
`FORBIDDEN_LOCALE` · `LIMIT_REACHED` · `INTERNAL_ERROR`.

أكواد الحالة: `200` نجاح · `400` طلب خاطئ · `401` غير مصرّح · `403` ممنوع ·
`404` غير موجود · `422` تحقّق · `429` تجاوز المعدّل · `500` خطأ داخلي.

---

## النظام (System)

### GET /health
**200** → `{ "data": { "status": "ok", "service": "ndsp-api", "mode": "DECISION_ACTIVE", "sanitized": true } }`

### GET /governance
**200** → أعلام الحوكمة (مصدر القرار، العرض فقط، لا تنفيذ، لا نصيحة، إلخ).

---

## المصادقة (Auth) — `/api/v1/auth`

### POST /auth/register
إشارات آمنة فقط؛ معادلة الخطر داخلية.
**Request**
```json
{ "email": "user@x.com", "name": "Sara", "seat_type": "ordinary", "locale": "ar", "password": "********" }
```
`seat_type ∈ ordinary|specialist|private`
**200** → `{ "data": { "decision": "PENDING_REVIEW", "ref": "NDSP-T-XXXX" } }`
`decision ∈ ALLOW|PENDING_REVIEW|BLOCK_DUPLICATE|RATE_LIMITED|HIGH_RISK_DUPLICATE`

### POST /auth/login
**Request** `{ "email": "...", "password": "..." }`
**200** → `{ "data": { "access_token": "...", "refresh_token": "...", "token_type": "bearer" } }`
**401** `INVALID_CREDENTIALS` · **403** `PENDING_REVIEW`

### POST /auth/2fa/verify
**Request** `{ "email": "...", "code": "123456" }` → **200** TokenOut

### POST /auth/refresh
**Request** `{ "refresh_token": "..." }` → **200** TokenOut · **401** `UNAUTHENTICATED`

### GET /auth/me  *(auth)*
**200** → `{ "data": { "id", "email", "name", "locale", "role", "status" } }`

---

## الحساب والتجربة (Account) — `/api/v1/account`

> التجربة ١٦ يومًا تبدأ عند التفعيل، لكل مستخدم، تُحسب في الخادم.

### POST /account/activate  *(auth)*
يضبط ساعة التجربة مرة واحدة (idempotent).
**200** → `{ "data": { "trial_day": 1, "total": 16, "started_at": "...", "ends_at": "...", "expired": false } }`

### GET /account/trial  *(auth)*
**200** → نفس شكل TrialOut أعلاه. **404** `NO_TRIAL`

---

## الباقات والأسواق (Catalog)

### GET /packages
**200** → `{ "data": [ { "code": "free", "name_ar": "...", "name_en": "Free", "limits": { ... } } ] }`

### GET /markets
**200** → `{ "data": [ { "code": "fx", "name_ar": "...", "name_en": "FX", "state": "live", "audit_class": "VISIBLE_BY_PACKAGE" } ] }`

### GET /assets?market=fx  *(auth)*
**200** → `{ "data": [ { "id": "XAU", "symbol": "XAU/USD", "market": "commodities", "name_ar": "...", "name_en": "Gold" } ] }`

### GET /assets/{id}/decision  *(auth)* — مخرجة منقّحة
**200** → `data` يحوي **فقط**:
```json
{
  "asset_id": "XAU", "symbol": "XAU/USD",
  "bias": "up", "horizon": "extended", "horizon_strength": 72, "decision_quality": 74,
  "market_state": "trending", "liquidity": "good", "risk": "moderate",
  "volatility": "moderate", "sentiment": "positive",
  "named_layers": ["TDL","NMP","Devil's Advocate","Nawaf Golden Alignment"],
  "golden_alignment": { "active": true, "note_ar": "...", "note_en": "..." },
  "devil_advocate": [ { "reason_ar": "...", "reason_en": "..." } ],
  "scenario": {
    "scenario_state": "forming",
    "scenario_directional_context": "constructive",
    "scenario_activation_level": 2398.0,
    "scenario_arrival_level": 2425.0,
    "scenario_invalidation_level": 2380.0,
    "scenario_review_zone": "2440-2452",
    "scenario_time_horizon": "extended",
    "scenario_confidence_band": "moderate",
    "scenario_risk_note": "...",
    "scenario_follow_up_note": "...",
    "scenario_status_label": "active",
    "scenario_last_updated": "...",
    "governance_note": "مراجع سياقية لدعم القرار فقط، وليست نصيحة مالية."
  },
  "summary_ar": "...", "summary_en": "..."
}
```
`named_layers` تُفلتر حسب الباقة (Free: لا شيء · Pro: TDL, NMP · Elite/Institutional: الأربعة).
**ممنوع** ظهور: معادلات/أوزان/تسجيل داخلي/أسماء مخفية/بصمات خام/شراء/بيع/دخول/جني/وقف/هدف مضمون.

### GET /assets/{id}/chart?timeframe=1h  *(auth)*
**200** → `{ "data": { "symbol", "timeframe", "series": [], "reference_zones": [ {"type":"activation","level":...} ], "horizon_cone": {"upper":...,"lower":...} } }`
بيانات سوق + مناطق مرجعية فقط. **لا** دخول/جني/وقف.

---

## المدفوعات (Payments) — لا تفعيل تلقائي

### POST /payments/checkout  *(auth)*
**Request** `{ "package_code": "elite", "cycle": "monthly", "method": "crypto" }`
**200** → `{ "data": { "subscription_id": "...", "state": "pending", "ref": "NDSP-P-XXXX", "instructions_ar": "...", "instructions_en": "..." } }`
`state = manual_review_required` عند التحويل البنكي.

### POST /payments/webhook
من المزوّد فقط؛ يُتحقّق من التوقيع (`x-nowpayments-sig`).
**200** → `{ "data": { "received": true } }` · **400** `BAD_SIGNATURE`

### GET /me/subscription  *(auth)*
**200** → `{ "data": { "plan": "elite", "state": "confirmed", "ref": "...", "renews_at": "..." } }`

---

## التنبيهات (Alerts) — `/api/v1/me`

> إشعارات قرار منقّحة فقط — لا تنبيهات شراء/بيع.

### GET /me/alert-prefs  *(auth)* → تفضيلات التنبيه
### PUT /me/alert-prefs  *(auth)*
**Request**
```json
{ "events": { "bias": true, "golden": true, "scenario": true, "caution": true, "horizon": false },
  "dq_threshold": 70, "brief_time": "07:30", "digest": "daily", "quiet_from": "22:00", "quiet_to": "07:00" }
```
**200** → `{ "data": { "saved": true } }`

### POST /me/channels/telegram/link  *(auth)*
**200** → `{ "data": { "code": "NDSP-LINK-XXXX", "expires_in": 600 } }`
يُعاد الرمز لمرة واحدة فقط — **لا** يُعرض توكن البوت إطلاقًا.

---

## الإدارة (Admin) — `/api/v1/admin` *(admin role من قاعدة البيانات)*

### GET /admin/registrations?status=pending_review
**200** → إشارات آمنة فقط (بريد مقنّع، حالة، تاريخ) — لا درجة خطر خام.

### POST /admin/registrations/{user_id}/decision
**Request** `{ "decision": "allow" }`  (`allow` يفعّل الحساب ويبدأ ساعة التجربة) · `{ "decision": "block" }`
**200** → `{ "data": { "id": "...", "status": "active" } }`

### GET /admin/payments · POST /admin/payments/{id}/approve · POST /admin/payments/{id}/reject
اعتماد/رفض يدوي + تسجيل تدقيق.

### GET /admin/trials
**200** → لكل مستخدم: `{ "user_id", "seat_type", "trial_day", "total", "started_at", "ends_at" }`

### GET /admin/layers
**200** → `{ "data": { "visible": ["Devil's Advocate","NMP","Nawaf Golden Alignment","TDL"], "hidden_count": 12 } }`
**لا** يعيد معادلات/أوزان/أسماء مخفية أبدًا.

### GET /admin/health
**200** → `{ "data": { "api": "ok", "sanitizer": "on", "mode": "DECISION_ACTIVE" } }`

---

## CORS واللغات
- CORS للدومينات الرسمية فقط: `ndsp.app`, `my.ndsp.app`, `admin.ndsp.app`.
- العبرية محجوبة: أي `Accept-Language` يحوي `he/iw/he-IL` → **400** `FORBIDDEN_LOCALE`.

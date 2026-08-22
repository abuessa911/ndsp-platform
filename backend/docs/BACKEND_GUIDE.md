# NDSP Backend — دليل التنفيذ الشامل (BACKEND_GUIDE)

دليل عملي لتركيب وتشغيل خادم NDSP داخل `/home/nawaf511/empire-core-new/backend`.

---

## 1) بنية الباك إند

```
app/
├─ main.py            ← FastAPI: CORS (دومينات رسمية), rate limit, أخطاء آمنة, حارس اللغة (حجب العبرية)
├─ bootstrap.py       ← إنشاء الجداول + بيانات أولية (باقات/أسواق/أصول/أعلام حوكمة) + أول أدمن
├─ core/
│  ├─ config.py       ← كل الإعدادات من .env (لا أسرار في الكود)
│  └─ security.py     ← JWT (access/refresh), Argon2 لكلمات المرور, Fernet للأسرار المخزّنة
├─ db/session.py      ← المحرّك + الجلسات
├─ models/            ← كل الجداول (ORM) — تطابق db/schema.sql
├─ schemas/           ← Pydantic + مغلّف الأخطاء الموحّد
├─ services/
│  └─ sanitizer.py    ← ★ المنقّح: البوابة الوحيدة لكل مخرجة عامة
└─ api/
   ├─ deps.py         ← المستخدم الحالي + صلاحية الأدمن من قاعدة البيانات
   └─ routes/         ← auth, account, catalog, payments, alerts, admin
```

**القاعدة:** المحرّك الداخلي قد يحسب أي شيء، لكن لا مخرجة تخرج إلا عبر `sanitize_decision`. أي حقل خارج قائمة المسموح يُسقَط تلقائيًا (ويرفع استثناءً في غير الإنتاج لاكتشاف الأخطاء مبكرًا).

---

## 2) إنشاء أول أدمن بأمان

كلمة المرور لا توضع في أي ملف. تُطلب تفاعليًا أو من متغيّر بيئة مؤقّت.

```sh
cd /home/nawaf511/empire-core-new/backend
. .venv/bin/activate

# الطريقة الآمنة (تفاعلية):
python -m app.bootstrap --email admin@ndsp.app
# تُطلب كلمة المرور بدون طباعتها. الحد الأدنى ١٠ أحرف.

# أو عبر متغيّر مؤقّت (يُحذف من الجلسة بعدها):
ADMIN_BOOTSTRAP_PASSWORD='CHANGE_ME_ADMIN_PASSWORD' python -m app.bootstrap --email admin@ndsp.app
```

- صلاحية الأدمن تُقرأ من عمود `role` في قاعدة البيانات — **ليست** من التوكن وحده.
- إعادة تشغيل السكربت آمنة: لا يُنشئ أدمن مكرّرًا بنفس البريد.

---

## 3) تشغيل الـ migrations

**خيار أ — Alembic (مُفضّل):**
```sh
cd /home/nawaf511/empire-core-new/backend && . .venv/bin/activate
alembic revision --autogenerate -m "initial schema"   # بعد ضبط DATABASE_URL
alembic upgrade head
```

**خيار ب — تطبيق المخطّط مباشرة:**
```sh
psql "$DATABASE_URL_PSQL" -f db/schema.sql
# DATABASE_URL_PSQL = نفس الرابط بدون +psycopg
```

> `app.bootstrap` ينشئ الجداول تلقائيًا أيضًا (`create_all`) كبديل سريع للتطوير.

---

## 4) تشغيل السيرفر

**تطوير:**
```sh
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**إنتاج (مثال خدمة systemd):** `/etc/systemd/system/ndsp-api.service`
```ini
[Unit]
Description=NDSP API
After=network.target postgresql.service

[Service]
User=nawaf511
WorkingDirectory=/home/nawaf511/empire-core-new/backend
EnvironmentFile=/home/nawaf511/empire-core-new/backend/.env
ExecStart=/home/nawaf511/empire-core-new/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```
```sh
sudo systemctl daemon-reload && sudo systemctl enable --now ndsp-api
```

---

## 5) ربط nginx مع api.ndsp.app

`/etc/nginx/sites-available/api.ndsp.app`
```nginx
server {
    listen 443 ssl;
    server_name api.ndsp.app;

    # ssl_certificate ... ;  (Let's Encrypt / certbot)
    # ssl_certificate_key ... ;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```sh
sudo ln -s /etc/nginx/sites-available/api.ndsp.app /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d api.ndsp.app
```

> `/var/www` مخرجات نشر فقط — لا يُستخدم كمصدر كود.

---

## 6) اختبار المسارات

```sh
# صحة
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/governance

# تسجيل
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"sara@x.com","password":"strongpass12","seat_type":"private","locale":"ar"}'

# دخول (بعد اعتماد الأدمن للحساب)
curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' -d '{"email":"sara@x.com","password":"strongpass12"}'

# قراءة منقّحة (بالتوكن)
TOKEN=CHANGE_ME_ACCESS_TOKEN; curl -s http://127.0.0.1:8000/api/v1/assets/XAU/decision -H "Authorization: Bearer $TOKEN"

# تأكيد حجب العبرية
curl -s -H 'Accept-Language: he-IL' http://127.0.0.1:8000/health   # يجب 400 FORBIDDEN_LOCALE
```

اختبار المنقّح آليًا (يفشل لو تسرّب حقل ممنوع):
```sh
python - <<'PY'
from app.services.sanitizer import sanitize_decision, assert_clean
out = sanitize_decision({"asset_id":"XAU","bias":"up","weights":{"l1":0.3},"internal_score":0.9}, "elite")
assert_clean(out); print("sanitizer OK:", out.keys())
PY
```

---

## 7) إنشاء تقرير بعد التركيب

- سكربت التركيب يكتب تقريرًا تلقائيًا في `/home/nawaf511/ndsp_launch_reports/install_report_<TS>.txt`.
- سكربت الفحص يكتب `/home/nawaf511/ndsp_launch_reports/verify_report_<TS>.txt`.
- لإنشاء تقرير فحص يدوي في أي وقت:
```sh
sh scripts/verify_ndsp_backend.sh
```

> التقارير الرسمية فقط في `/home/nawaf511/ndsp_launch_reports` — لا تُكتب داخل المشروع.
> النسخ الاحتياطية الرسمية فقط في `/home/nawaf511/ndsp_backups`.

---

## 8) الباقات والطبقات والسيناريو (مرجع سريع)

- الباقات: **Free · Pro · Elite · Institutional Suite** (الحدود في `packages.limits`، تُفرض في الخادم).
- التجربة: ١٦ يومًا · ٥٠ مقعد (٢٥ ordinary · ١٠ specialist · ١٥ private). الساعة لكل مستخدم تبدأ بالتفعيل.
- الطبقات الظاهرة بالاسم (حسب الباقة): TDL · NMP · Devil's Advocate · Nawaf Golden Alignment. ما عداها مخفي.
- مخرجات السيناريو المسموحة فقط: `scenario_state, scenario_directional_context, scenario_activation_level, scenario_arrival_level, scenario_invalidation_level, scenario_review_zone, scenario_time_horizon, scenario_confidence_band, scenario_risk_note, scenario_follow_up_note, scenario_last_updated, scenario_status_label, governance_note`.

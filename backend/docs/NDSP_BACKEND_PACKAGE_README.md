# NDSP Backend — حزمة التطوير الجاهزة للتركيب

**NDSP — منصة نواف لدعم القرار · Nawaf Decision Support Platform**
**هذا تطوير دعم قرار محكوم — ليس بوت تداول، ولا تنفيذ، ولا نصيحة مالية.**

---

## ما هذه الحزمة؟

خدمة Backend مبنية بـ **FastAPI + SQLAlchemy + PostgreSQL**، جاهزة للدمج داخل المشروع الرسمي:

```
/home/nawaf511/empire-core-new/backend
```

تطبّق قواعد الحوكمة في الكود: **Backend هو مصدر القرار، والواجهة عرض فقط**، وكل المخرجات العامة تمرّ من **المنقّح (sanitizer)** — لا تُكشف معادلات ولا أوزان ولا تسجيل داخلي ولا أسماء الطبقات المخفية ولا أسرار.

## التقنية المستخدمة

- **Python 3.11+ · FastAPI · SQLAlchemy 2 · Alembic · PostgreSQL 15+**
- المصادقة: JWT (access + refresh) · كلمات المرور Argon2 (مع دعم bcrypt)
- تشفير الأسرار عند التخزين: Fernet · تحديد المعدّل: SlowAPI

## المتطلبات

- Python ≥ 3.11، PostgreSQL ≥ 15
- nginx (لربط `api.ndsp.app`)
- مفتاح مزوّد بيانات الأسواق (يوضع في `.env` لاحقًا — ليس داخل الحزمة)

## التركيب السريع

```sh
# 1) فك الضغط بجانب المشروع، ثم:
sh scripts/install_ndsp_backend.sh        # آمن: نسخة احتياطية + دمج + تقرير
# 2) املأ الأسرار الحقيقية:
nano /home/nawaf511/empire-core-new/backend/.env
# 3) أنشئ أول أدمن (يطلب كلمة المرور تفاعليًا):
cd /home/nawaf511/empire-core-new/backend && . .venv/bin/activate
python -m app.bootstrap --email admin@ndsp.app
# 4) شغّل الخدمة:
uvicorn app.main:app --host 127.0.0.1 --port 8000
# 5) تحقّق:
sh scripts/verify_ndsp_backend.sh
```

> السكربت **لا يحذف شيئًا**، يأخذ نسخة احتياطية قبل أي تعديل، ويكتب تقريرًا في `/home/nawaf511/ndsp_launch_reports`.

## بنية الحزمة

```
ndsp-backend/
├─ backend/
│  ├─ app/
│  │  ├─ main.py              ← تطبيق FastAPI (CORS, rate limit, أخطاء آمنة, حارس اللغة)
│  │  ├─ bootstrap.py         ← إنشاء الجداول + بيانات أولية + أول أدمن
│  │  ├─ core/                ← config + security (JWT/Argon2/Fernet)
│  │  ├─ db/session.py        ← المحرّك والجلسات
│  │  ├─ models/              ← كل الجداول (ORM)
│  │  ├─ schemas/             ← Pydantic + مغلّف الأخطاء الموحّد
│  │  ├─ services/sanitizer.py← ★ المنقّح: البوابة الوحيدة للمخرجات
│  │  └─ api/routes/          ← auth, account, catalog, payments, alerts, admin
│  ├─ db/schema.sql           ← مخطّط PostgreSQL كامل (بديل عن Alembic)
│  ├─ migrations/             ← Alembic
│  ├─ requirements.txt
│  ├─ .env.example            ← أسماء المتغيّرات فقط (بدون أسرار)
│  └─ .gitignore
├─ scripts/
│  ├─ install_ndsp_backend.sh ← تركيب آمن
│  └─ verify_ndsp_backend.sh  ← فحص فقط (بدون تعديل)
└─ docs/
   ├─ API_CONTRACT.md · openapi.yaml
   ├─ BACKEND_GUIDE.md · SECURITY_CHECKLIST.md
```

## الحوكمة (ملخّص)

- `MODE=DECISION_ACTIVE` · `DIRECT_TRADE_EXECUTION=False` · `PUBLIC_OUTPUT_SANITIZED=True`
- الطبقات المسموح ظهور اسمها (حسب الباقة): **TDL · NMP · Devil's Advocate · Nawaf Golden Alignment**. ما عداها مخفي الاسم والمنطق.
- مخرجات السيناريو المسموحة فقط (راجع `API_CONTRACT.md`).
- كل تعديل عبر السكربت ينتج **نسخة احتياطية + تقرير**.

> اقرأ `docs/BACKEND_GUIDE.md` للتفاصيل الكاملة، و`docs/SECURITY_CHECKLIST.md` قبل الإطلاق.

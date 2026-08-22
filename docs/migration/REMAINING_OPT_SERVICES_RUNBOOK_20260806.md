# NDSP Remaining /opt Services Migration Runbook

## الهدف

إزالة الاعتماد التشغيلي المتبقي على `/opt/ndsp-*` ونقل مصادر التطبيقات إلى:

`/home/nawaf511/empire-core-new/apps/`

مع إبقاء وحدات systemd داخل `/etc/systemd/system/`، وملفات البيئة والأسرار داخل `/etc/`، وبيانات التشغيل خارج Git.

## قواعد إلزامية

- ترحيل خدمة واحدة في كل مرة.
- عدم نسخ `.venv` أو `venv` أو `__pycache__`.
- بناء بيئة Python جديدة داخل مجلد التطبيق عند الحاجة.
- عدم نسخ أو طباعة ملفات `.env` أو ملفات `/etc/ndsp/*.env`.
- الحفاظ على المستخدم والمجموعة والمنفذ وخصائص الحماية الحالية.
- اختبار الخدمة قبل نقل المسار القديم.
- نقل المسار القديم إلى `/opt/quarantine-project-migration-20260806/`.
- خدمات المصادقة والدفع والتسجيل وكلمات المرور تنفذ أخيرًا وبموافقة يدوية.
- استخدام Git لمسارات محددة فقط؛ يمنع `git add .`.

## الحالة الحالية

### جاهزة للترحيل

1. `ndsp-v3-portal-gateway.service`
   - المستخدم: `www-data`
   - المجموعة: `www-data`
   - المصدر الفعلي: `/opt/ndsp-v3-portal-gateway/app.py`
   - لا تُنقل نسخ `before_restore` أو `broken_truth`.

### حساسة — المرحلة الأخيرة

2. `ndsp-current-user-display.service`
   - المنفذ: `9074`
   - المستخدم: `postgres`
   - مرتبطة بقاعدة `ndsp_auth`.

3. `ndsp-admin-user-ops.service`
   - المنفذ: `9068`
   - عمليات إدارية على المستخدمين.
   - المصدر الفعلي يحتاج تحديدًا بين `app.py` و`server.py`.

4. `ndsp-auth-core-clean.service`
   - المستخدم: `ndsp-auth`
   - تعتمد على `/etc/ndsp/ndsp-auth-core-clean.env`.
   - تستخدم بنية `releases/current`.
   - `ProtectHome=yes`.

5. `ndsp-change-password-gateway.service`
   - المنفذ: `9069`
   - المستخدم والمجموعة: `postgres`.
   - يجب بناء venv جديدة.

6. `ndsp-commercial-auth-payment-staging.service`
   - تعتمد على `/etc/ndsp/commercial-auth-payment-staging.env`.
   - تستخدم بنية releases وسكربت `run-staging.sh`.
   - `ProtectHome=read-only`.

7. `ndsp-registration-mailer-v12-1.service`
   - خدمة static/inactive تعمل كـ job.
   - المصدر: `mailer.py`.
   - لا تعامل كخدمة HTTP دائمة.

### توثيق فقط

8. `ndsp-enterprise-api.service`
   - معطلة وبدون مسار مصدر موجود.
   - المنفذ `9088` مملوك لخدمة أخرى داخل المشروع.
   - لا تُفعّل ولا تُهاجر.

## تسلسل التنفيذ

1. ترحيل `ndsp-v3-portal-gateway`.
2. مراجعة واختبار خدمات العرض والإدارة المرتبطة بالمستخدمين.
3. ترحيل بوابة تغيير كلمة المرور.
4. ترحيل mailer كـ job.
5. ترحيل auth core.
6. ترحيل commercial auth/payment staging أخيرًا.
7. جرد نهائي لأي مسارات `/opt/ndsp-*` متبقية.
8. إعادة بناء حزمة handoff والـGit bundle بعد اكتمال جميع الخدمات.

## نمط rollback

عند فشل أي خدمة بعد cutover:

1. إعادة drop-in إلى المسار السابق.
2. `systemctl daemon-reload`.
3. إعادة المسار من quarantine إذا نُقل.
4. إعادة تشغيل الخدمة.
5. التحقق من المنفذ وhealth قبل متابعة أي خدمة أخرى.

# NDSP Current Reality Lock — تثبيت الواقع الحالي

DATE=2026-07-07
SOURCE_AUDIT_REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_AUDIT_REPORT_20260707_090724.md

## Project Paths

PROJECT_DIR=/home/nawaf511/empire-core-new
FRONTEND_DIR=/var/www/ndsp-my
BACKEND_DIR=/home/nawaf511/empire-core-new

FRONTEND_BASE=https://my.ndsp.app
API_BASE=https://api.ndsp.app

## Audit Result

FINAL_STATUS=AUDIT_DONE

## Public Routes Confirmed 200

- https://my.ndsp.app/
- https://my.ndsp.app/index.html
- https://my.ndsp.app/decision-support.html
- https://my.ndsp.app/NDSP_Asset_View.html
- https://my.ndsp.app/NDSP_Command_Center.html
- https://my.ndsp.app/NDSP_Daily_Brief.html
- https://my.ndsp.app/NDSP_Settings_Alerts.html

## Decision API Reality

GET https://api.ndsp.app/api/health = 200
GET https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT = 200

Required fields confirmed:
- decision_quality
- scenario_state
- live_price

Observed ETHUSDT sample:
- live_price=1779.11
- decision_quality=86
- scenario_state=UNDER_MONITORING
- nmp_status=AVAILABLE
- nmp_level=1583.4

Rule:
NMP is computed by backend. The frontend must not invent NMP.

## Service Reality

systemd:
- nginx = active
- ndsp-api = activating
- ndip-api-new = failed
- ndsp-next = not found
- market-bridge = not found

PM2:
- ndsp-portal = online
- ndsp-backend = online but restart count is very high

Decision:
Do not restart or repair services before backup and diagnostics.

## Nginx Reality

nginx service is active.

Audit nginx -t failed because it was run without sufficient permission:
open() "/run/nginx.pid" failed (13: Permission denied)

Next check must be:
sudo nginx -t

Do not edit nginx before backup.

## Protected UI Elements

RADAR_FILE_COUNT=24
SIDEBAR_FILE_COUNT=24
DISCLAIMER_FILE_COUNT=17

Protected:
- Radar
- Sidebar
- Disclaimer
- Official page links

## Forbidden Wording

Audit first scan found no obvious forbidden wording.

Still forbidden:
- Buy Now
- Sell Now
- اشتر الآن
- بيع الآن
- ادخل صفقة
- ربح مضمون
- توصية مباشرة
- أمر تنفيذ

## Resource Snapshot

Disk usage:
- root around 82%

Memory:
- acceptable

Decision:
No cleanup before backup and report.

## Locked Rule

No frontend/backend patch is allowed before:

1. Backup
2. Service diagnostics
3. Post-patch test baseline
4. Clear patch scope
5. Rollback path

## Current Judgment

The public system is alive:
- pages respond
- API responds
- decision fields exist
- radar/sidebar/disclaimer exist

But runtime is inconsistent:
- systemd backend services show alerts
- PM2 appears to be serving active runtime
- backend PM2 restart count is high

First technical target:
Lock runtime reality before touching UI or backend logic.

---

## Runtime Governance Lock — 2026-07-07

تم تثبيت قفل التشغيل بعد نجاح اختبار ما بعد التعديل.

- POST_PATCH_STATUS=POST_PATCH_TEST_OK
- PM2 الرسمي: ndsp-portal فقط
- ndsp-backend تم عزله لأنه خدمة قديمة/مكسورة وغير مستخدمة في المسار العام
- API Gateway الرسمي: 127.0.0.1:9001
- Decision Quality Live الرسمي: 127.0.0.1:9082
- Nginx لا يحتاج تعديل
- أي تعديل جديد يجب أن يمر عبر: Backup → Patch صغير → Test → Report → Rollback path

Reference:
docs/05-runbooks/NDSP_RUNTIME_GOVERNANCE_LOCK_AR.md

---

## Disclaimer Gate Lock — 2026-07-07

تم تركيب بوابة إخلاء المسؤولية قبل دخول المنصة بنجاح.

- DISCLAIMER_GATE_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_DISCLAIMER_GATE_V1_20260707_094240.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_094334.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK
- disclaimer.html أصبح صفحة حقيقية وليس fallback
- تم حقن ndsp-disclaimer-gate.js داخل صفحات الواجهة الموجودة
- لا تعديل على Nginx
- لا تعديل على Runtime
- لا كسر للرادار أو القائمة أو API

Rule:
أي مستخدم جديد يجب أن يوافق على إخلاء المسؤولية قبل دخول المنصة.

---

## Menu Canonical Page Match Lock — 2026-07-07

تمت مطابقة أسماء الصفحات في القائمة مع المسارات الرسمية بنجاح.

- MENU_CANONICAL_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_MENU_CANONICAL_PAGE_MATCH_V1_20260707_094821.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_094957.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

الصفحات الرسمية أصبحت ملفات حقيقية وليست fallback:

- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html

تم تحديث القائمة لاستخدام المسارات الرسمية مع إبقاء الملفات القديمة كـ legacy.

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- تصميم الرادار

Rule:
أي تعديل لاحق على القائمة يجب أن يحافظ على المسارات الرسمية أعلاه، ولا يرجع إلى fallback أو أسماء legacy كمسار أساسي.

---

## Command Center Radar Bind Lock — 2026-07-07

تم ربط مركز القيادة والرادار بالقراءة الحية من الباك إند بنجاح.

- COMMAND_CENTER_RADAR_BIND_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_COMMAND_CENTER_RADAR_BIND_V24_20260707_100000.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_100110.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

تم تفعيل عرض الحقول التالية داخل مركز القيادة/الرادار:

- السعر الحي
- حالة السيناريو
- جودة القراءة
- سياق الاتجاه
- أفق المتابعة
- NMP
- مستوى التفعيل
- مستوى الوصول
- منطقة المراجعة
- مستوى الإلغاء

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- بوابة الإخلاء
- المسارات الرسمية

Rule:
مركز القيادة يعرض فقط الحقول المحسوبة من الباك إند، ولا يخترع مستويات أو NMP من الواجهة.

---

## Decision Support Bind Lock — 2026-07-07

تم ربط صفحة دعم القرار بالقراءة الحية من الباك إند بنجاح.

- DECISION_SUPPORT_BIND_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_DECISION_SUPPORT_BIND_V1_20260707_100626.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_100627.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

تم تفعيل عرض الحقول التالية داخل صفحة دعم القرار:

- الأصل
- السعر الحي
- جودة القراءة
- حالة السيناريو
- سياق الاتجاه
- أفق المتابعة
- NMP
- مستوى التفعيل
- مستوى الوصول
- منطقة المراجعة
- مستوى الإلغاء
- سبب التحفظ
- ملخص منقح من الباك إند

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- مركز القيادة
- الرادار
- بوابة الإخلاء
- المسارات الرسمية

Rule:
صفحة دعم القرار تعرض فقط الحقول المحسوبة من الباك إند، ولا تخترع مستويات أو NMP من الواجهة.

---

## Asset View Live Bind Lock — 2026-07-07

تم ربط صفحة الأسواق والأصول بالقراءة الحية من الباك إند بنجاح.

- ASSET_VIEW_LIVE_BIND_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_ASSET_VIEW_LIVE_BIND_V1_20260707_101304.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_101404.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

تم تفعيل عرض الحقول التالية داخل صفحة الأسواق والأصول:

- الأصل
- السوق
- السعر الحي
- جودة القراءة
- حالة السيناريو
- سياق الاتجاه
- NMP
- مستوى التفعيل
- مستوى الوصول
- منطقة المراجعة
- مستوى الإلغاء
- روابط دعم القرار ومركز القيادة لكل أصل

مصادر البيانات:

- /assets/ndsp-assets.json
- /api/decision/quality-live?symbol=...

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- مركز القيادة
- الرادار
- دعم القرار
- بوابة الإخلاء
- المسارات الرسمية

Rule:
صفحة الأسواق والأصول تعرض فقط الحقول المحسوبة من الباك إند، ولا تخترع مستويات أو NMP من الواجهة.

---

## Daily Brief Live Bind Lock — 2026-07-07

تم ربط صفحة الموجز اليومي بالقراءة الحية من الباك إند بنجاح.

- DAILY_BRIEF_LIVE_BIND_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_DAILY_BRIEF_LIVE_BIND_V1_20260707_102950.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_102951.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

تم تفعيل عرض الحقول التالية داخل صفحة الموجز اليومي:

- أهم الأصول اليومية
- السعر الحي
- جودة القراءة
- حالة السيناريو
- سياق الاتجاه
- NMP
- سبب التحفظ
- آخر تحديث
- متوسط جودة القراءة
- أعلى قراءة في الموجز

الأصول الأساسية في الموجز:

- ETHUSDT
- BTCUSDT
- XAUUSD
- USOIL

مصدر البيانات:

- /api/decision/quality-live?symbol=...

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- مركز القيادة
- الرادار
- دعم القرار
- الأسواق والأصول
- بوابة الإخلاء
- المسارات الرسمية

Rule:
صفحة الموجز اليومي تعرض فقط الحقول المحسوبة من الباك إند، ولا تخترع مستويات أو NMP من الواجهة.

---

## Settings Alerts Bind Lock — 2026-07-07

تم ربط صفحة الإعدادات والتنبيهات بالقراءة الحية من الباك إند بنجاح.

- SETTINGS_ALERTS_BIND_STATUS=INSTALLED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_SETTINGS_ALERTS_BIND_V1_20260707_103642.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103643.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

تم تفعيل عرض الحقول التالية داخل صفحة الإعدادات والتنبيهات:

- الأصل المراقب
- السعر الحي
- جودة القراءة
- حالة السيناريو
- سياق الاتجاه
- NMP
- حد جودة التنبيه
- وضع العرض
- حالة التفعيل
- قناة التنبيه
- قاعدة الإرسال
- حالة الحماية
- ملخص حالة التنبيه

مصدر البيانات:

- /api/decision/quality-live?symbol=...

لم يتم تعديل:

- Nginx
- Runtime
- PM2
- API
- مركز القيادة
- الرادار
- دعم القرار
- الأسواق والأصول
- الموجز اليومي
- بوابة الإخلاء
- المسارات الرسمية

Rule:
صفحة الإعدادات والتنبيهات تعرض حالة مراقبة وتنبيه فقط، ولا ترسل توصيات مالية أو أوامر تنفيذ، ولا تخترع مستويات أو NMP من الواجهة.

---

## Final Release Sweep Lock — 2026-07-07

تم تنفيذ فحص الإصدار النهائي بعد إغلاق جميع صفحات البوابة الأساسية.

- FINAL_RELEASE_SWEEP_STATUS=PASSED
- FINAL_RELEASE_SWEEP_REPORT=docs/05-runbooks/NDSP_FINAL_RELEASE_SWEEP_20260707_103944.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_20260707_103951.md
- POST_PATCH_STATUS=POST_PATCH_TEST_OK

نتائج الفحص النهائي:

- جميع الصفحات الرسمية تعمل HTTP 200
- صفحة الإخلاء تعمل HTTP 200
- جميع ملفات الربط الحية تعمل HTTP 200
- API القرار الحي يعمل للأصول الأساسية
- الحقول المطلوبة من API موجودة
- الرادار موجود
- القائمة الجانبية موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- PM2 يحتوي runtime رسمي واحد فقط: ndsp-portal
- ndsp-portal online
- لا توجد إعادة تشغيل في PM2

الصفحات المقفلة:

- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html
- /disclaimer.html

ملفات الربط المقفلة:

- /assets/ndsp-radar-safe-clean.js
- /assets/ndsp-decision-support-bind.js
- /assets/ndsp-asset-view-live-bind.js
- /assets/ndsp-daily-brief-live-bind.js
- /assets/ndsp-settings-alerts-bind.js
- /assets/ndsp-disclaimer-gate.js
- /assets/ndsp-global-menu.js

الأصول التي تم اختبارها في الفحص النهائي:

- ETHUSDT
- BTCUSDT
- XAUUSD
- USOIL

Rule:
هذه الحالة هي خط الأساس النهائي للإصدار الحالي. أي تعديل لاحق يجب أن يحافظ على الصفحات الرسمية، ملفات الربط، الرادار، القائمة، بوابة الإخلاء، ونظافة ألفاظ الواجهة العامة.

---

## Production Snapshot Lock — 2026-07-07

تم إنشاء لقطة إنتاج كاملة بعد إغلاق الإصدار النهائي.

- PRODUCTION_SNAPSHOT_STATUS=CREATED
- SNAPSHOT_REPORT=docs/05-runbooks/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.md
- SNAPSHOT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_PRODUCTION_SNAPSHOT_20260707_105055.tar.gz
- SNAPSHOT_SHA256=ab006cc5201bbde45da508366a78a23b7ec66cbc78db10fcaad881f43a6118ef

محتويات اللقطة:

- نسخة مضغوطة من /var/www/ndsp-my
- Reality Lock
- Final Release Sweep
- Release Handoff
- Post Patch Test
- تقارير ربط الصفحات
- أدلة Runtime
- PM2 evidence
- Nginx status
- API samples
- Checksums للواجهة

نتيجة التحقق:

- جميع الصفحات الرسمية HTTP 200
- جميع ملفات الربط HTTP 200
- API يعمل للأصول الأساسية
- ndsp-portal online
- لا توجد مشاكل في اختبار ما بعد التعديل

Rule:
هذه اللقطة هي نسخة الرجوع الرسمية للإصدار المقفل الحالي.

---

## External Tool Guardrails Lock — 2026-07-07

تم إنشاء ملف حوكمة إلزامي لأي أداة خارجية أو مطور أو أتمتة تعمل على NDSP بعد الإصدار المقفل.

- EXTERNAL_TOOL_GUARDRAILS_STATUS=CREATED
- GUARDRAILS_DOC=docs/05-runbooks/NDSP_EXTERNAL_TOOL_GUARDRAILS_20260707_110424.md
- RELEASE_STATUS=LOCKED
- PRODUCTION_SNAPSHOT_STATUS=CREATED
- FINAL_RELEASE_SWEEP_STATUS=PASSED

القواعد الإلزامية للأدوات الخارجية:

- لا تعديل على Nginx
- لا تعديل على PM2 runtime
- لا تعديل على API gateway
- لا تعديل على /api/decision/quality-live
- لا إزالة لبوابة الإخلاء
- لا إزالة للقائمة الجانبية
- لا حذف أو كسر للرادار
- لا استبدال للمسارات الرسمية بصفحات fallback
- لا كشف لأسماء الطبقات المحمية
- لا كشف للطبقات المخفية
- لا اختراع NMP من الواجهة
- لا اختراع مستويات سيناريو من الواجهة
- لا استخدام ألفاظ توصية مالية أو تنفيذ

أي تعديل لاحق يجب أن يمر عبر:

- Backup قبل التعديل
- Patch report
- Post patch test
- FINAL_STATUS=POST_PATCH_TEST_OK

Rule:
أي أداة خارجية يجب أن تقرأ ملف Guardrails قبل التعديل. إذا كانت غير متأكدة، تنشئ Audit Report فقط ولا تعدل الواجهة أو Runtime.

---

## External Tool Prompt Lock — 2026-07-07

تم إنشاء Prompt مختصر إلزامي لأي أداة خارجية تعمل على NDSP بعد الإصدار المقفل.

- EXTERNAL_TOOL_PROMPT_STATUS=CREATED
- PROMPT_DOC=docs/05-runbooks/NDSP_EXTERNAL_TOOL_PROMPT_SHORT_20260707_110632.md
- GUARDRAILS_DOC=docs/05-runbooks/NDSP_EXTERNAL_TOOL_GUARDRAILS_20260707_110424.md
- RELEASE_STATUS=LOCKED
- PRODUCTION_SNAPSHOT_STATUS=CREATED
- FINAL_RELEASE_SWEEP_STATUS=PASSED

الغرض من الملف:

- إعطاء أي أداة خارجية ملخصًا سريعًا لحالة الإصدار
- منع تعديل Nginx أو PM2 أو API
- منع كسر الرادار أو القائمة أو بوابة الإخلاء
- منع استبدال الصفحات الرسمية بصفحات fallback
- منع كشف الطبقات المحمية أو المخفية
- منع اختراع NMP أو مستويات السيناريو من الواجهة
- إلزام أي تعديل لاحق بعمل backup و patch report و post patch test

Rule:
أي أداة خارجية تبدأ من ملف Prompt المختصر، ثم تقرأ Guardrails و Reality Lock قبل أي تعديل.

---

## Codex External Audit Lock — 2026-07-07

تم تشغيل Codex CLI بوضع Audit فقط بعد قفل الإصدار.

- CODEX_EXTERNAL_AUDIT_STATUS=DONE
- CODEX_AUDIT_REPORT=docs/05-runbooks/NDSP_CODEX_EXTERNAL_AUDIT_20260707_111805.md
- MODIFICATIONS=None
- RESULT=Locked release intact from audit artifacts

Rule:
لا يتم تشغيل /review أو أي تعديل عبر Codex إلا بعد موافقة صريحة على Patch محدد مع Backup و Post Patch Test.

---

## Browser QA Closeout Lock — 2026-07-07

تم تنفيذ فحص خارجي من Kali بعد إغلاق الإصدار.

- BROWSER_SMOKE_TEST_STATUS=DONE
- BROWSER_SMOKE_REPORT=docs/05-runbooks/NDSP_BROWSER_SMOKE_TEST_20260707_153720.md
- FORBIDDEN_CONTEXT_SCAN_STATUS=DONE
- FORBIDDEN_CONTEXT_REPORT=docs/05-runbooks/NDSP_FORBIDDEN_CONTEXT_SCAN_20260707_154022.md
- BROWSER_QA_CLOSEOUT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_BROWSER_QA_CLOSEOUT_20260707_154205.tar.gz

نتائج الفحص:

- جميع الصفحات العامة HTTP 200
- جميع ملفات الربط المقفلة HTTP 200
- API القرار الحي يعمل للأصول الأساسية
- الحزم المحلية محفوظة
- الكلمات الحساسة ظهرت فقط داخل سياق النفي والإخلاء
- لا توجد أوامر شراء أو بيع أو تنفيذ في الواجهة العامة

Rule:
نتائج فحص الألفاظ الحساسة تعتبر False Positive مقبولة عندما تظهر داخل سياق الإخلاء أو النفي فقط مثل: ليست توصية مالية، ليست أمر شراء أو بيع، ليست نظام تنفيذ.

---

## Mobile Polish Audit Lock — 2026-07-07

تم تنفيذ فحص Mobile Polish Audit من Kali بدون أي تعديل على السيرفر.

- MOBILE_POLISH_AUDIT_STATUS=DONE
- MOBILE_POLISH_AUDIT_REPORT=docs/05-runbooks/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
- MOBILE_POLISH_AUDIT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
- MODE=AUDIT_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- ملفات CSS البصرية موجودة
- viewport meta موجود في الصفحات
- RTL و Arabic lang موجودة
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

ملاحظات التحسين الآمن مستقبلًا:

- premium.css هو المرشح الأول لتحسينات الجوال
- markets-hq.css هو المرشح الثاني لتحسينات الجداول والشبكات
- يفضل أن تكون أي تحسينات قادمة CSS-only قدر الإمكان
- لا يتم لمس radar/menu/disclaimer JS بدون موافقة صريحة

Rule:
Mobile polish القادم إن حصل يجب أن يكون CSS-only قدر الإمكان، مع Backup و Patch Report و Post Patch Test، وبدون تعديل Nginx أو PM2 أو API أو ملفات JS المحمية.

---

## Mobile Polish Audit Lock — 2026-07-07

تم تنفيذ فحص Mobile Polish Audit من Kali بدون أي تعديل على السيرفر.

- MOBILE_POLISH_AUDIT_STATUS=DONE
- MOBILE_POLISH_AUDIT_REPORT=docs/05-runbooks/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
- MOBILE_POLISH_AUDIT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
- MODE=AUDIT_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- ملفات CSS البصرية موجودة
- viewport meta موجود في الصفحات
- RTL و Arabic lang موجودة
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

ملاحظات التحسين الآمن مستقبلًا:

- premium.css هو المرشح الأول لتحسينات الجوال
- markets-hq.css هو المرشح الثاني لتحسينات الجداول والشبكات
- يفضل أن تكون أي تحسينات قادمة CSS-only قدر الإمكان
- لا يتم لمس radar/menu/disclaimer JS بدون موافقة صريحة

Rule:
Mobile polish القادم إن حصل يجب أن يكون CSS-only قدر الإمكان، مع Backup و Patch Report و Post Patch Test، وبدون تعديل Nginx أو PM2 أو API أو ملفات JS المحمية.

---

## Mobile Polish Audit Lock — 2026-07-07

تم تنفيذ فحص Mobile Polish Audit من Kali بدون أي تعديل على السيرفر.

- MOBILE_POLISH_AUDIT_STATUS=DONE
- MOBILE_POLISH_AUDIT_REPORT=docs/05-runbooks/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
- MOBILE_POLISH_AUDIT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
- MODE=AUDIT_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- ملفات CSS البصرية موجودة
- viewport meta موجود في الصفحات
- RTL و Arabic lang موجودة
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

ملاحظات التحسين الآمن مستقبلًا:

- premium.css هو المرشح الأول لتحسينات الجوال
- markets-hq.css هو المرشح الثاني لتحسينات الجداول والشبكات
- يفضل أن تكون أي تحسينات قادمة CSS-only قدر الإمكان
- لا يتم لمس radar/menu/disclaimer JS بدون موافقة صريحة

Rule:
Mobile polish القادم إن حصل يجب أن يكون CSS-only قدر الإمكان، مع Backup و Patch Report و Post Patch Test، وبدون تعديل Nginx أو PM2 أو API أو ملفات JS المحمية.

---

## Mobile Polish Audit Lock — 2026-07-07

تم تنفيذ فحص Mobile Polish Audit من Kali بدون أي تعديل على السيرفر.

- MOBILE_POLISH_AUDIT_STATUS=DONE
- MOBILE_POLISH_AUDIT_REPORT=docs/05-runbooks/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
- MOBILE_POLISH_AUDIT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
- MODE=AUDIT_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- ملفات CSS البصرية موجودة
- viewport meta موجود في الصفحات
- RTL و Arabic lang موجودة
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

ملاحظات التحسين الآمن مستقبلًا:

- premium.css هو المرشح الأول لتحسينات الجوال
- markets-hq.css هو المرشح الثاني لتحسينات الجداول والشبكات
- يفضل أن تكون أي تحسينات قادمة CSS-only قدر الإمكان
- لا يتم لمس radar/menu/disclaimer JS بدون موافقة صريحة

Rule:
Mobile polish القادم إن حصل يجب أن يكون CSS-only قدر الإمكان، مع Backup و Patch Report و Post Patch Test، وبدون تعديل Nginx أو PM2 أو API أو ملفات JS المحمية.

---

## Mobile Polish Audit Lock — 2026-07-07

تم تنفيذ فحص Mobile Polish Audit من Kali بدون أي تعديل على السيرفر.

- MOBILE_POLISH_AUDIT_STATUS=DONE
- MOBILE_POLISH_AUDIT_REPORT=docs/05-runbooks/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.md
- MOBILE_POLISH_AUDIT_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_MOBILE_POLISH_AUDIT_20260707_154749.tar.gz
- MODE=AUDIT_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- ملفات CSS البصرية موجودة
- viewport meta موجود في الصفحات
- RTL و Arabic lang موجودة
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

ملاحظات التحسين الآمن مستقبلًا:

- premium.css هو المرشح الأول لتحسينات الجوال
- markets-hq.css هو المرشح الثاني لتحسينات الجداول والشبكات
- يفضل أن تكون أي تحسينات قادمة CSS-only قدر الإمكان
- لا يتم لمس radar/menu/disclaimer JS بدون موافقة صريحة

Rule:
Mobile polish القادم إن حصل يجب أن يكون CSS-only قدر الإمكان، مع Backup و Patch Report و Post Patch Test، وبدون تعديل Nginx أو PM2 أو API أو ملفات JS المحمية.

---

## Mobile Menu CSS-only Patch Lock — 2026-07-07

تم تنفيذ تعديل بصري محدود على القائمة لمعالجة التداخل والشريط الأبيض داخل واجهة القائمة.

- MOBILE_MENU_CSS_ONLY_PATCH_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_MOBILE_MENU_CSS_ONLY_V1_20260707_172212.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_MOBILE_MENU_CSS_ONLY_V1_20260707_172212.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_MOBILE_MENU_CSS_ONLY_V1_20260707_172212
- MODIFIED_FILE=/var/www/ndsp-my/assets/ndsp-global-menu.css
- MODE=CSS_ONLY
- POST_PATCH_STATUS=OK

نطاق التعديل:

- تحسين احتواء القائمة بصريًا
- جعل Scrollbar داخل القائمة داكنًا ورفيعًا
- تقليل بروز الشريط الأبيض
- تحسين الفصل بين القائمة والخلفية
- ضبط عرض القائمة على الجوال والشاشات الضيقة
- تحديث cache-busting للصفحات الرسمية

لم يتم تعديل:

- Nginx
- PM2
- API gateway
- /api/decision/quality-live
- Radar JS
- Menu JS
- Disclaimer JS
- Backend runtime

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- PM2 يحتوي ndsp-portal فقط
- ndsp-portal online
- PM2 restarts = 0

Rule:
هذا التعديل معتمد كتعديل CSS-only بصري. أي تعديل بصري لاحق يجب أن يبدأ من Backup و Patch Report و Post Patch Test، ولا يلمس JS أو Runtime إلا بموافقة صريحة.

---

## Mobile Menu Text Readability V3 Lock + Deferred Visual Issue — 2026-07-07

تم تنفيذ V3 كتعديل CSS-only لتحسين وضوح نصوص القائمة في وضع اللغة الإنجليزية.

- MOBILE_MENU_TEXT_READABILITY_V3_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_MOBILE_MENU_TEXT_READABILITY_V3_20260707_181813.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_MOBILE_MENU_TEXT_READABILITY_V3_20260707_181813.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_MOBILE_MENU_TEXT_READABILITY_V3_20260707_181813
- MODIFIED_FILE=/var/www/ndsp-my/assets/ndsp-global-menu.css
- MODE=CSS_ONLY
- POST_PATCH_STATUS=OK

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

ملاحظة مؤجلة:

- ما زالت هناك ملاحظة بصرية في القائمة في بعض أوضاع اللغة/الصفحات.
- لا يتم تنفيذ V4 الآن حتى لا يتعطل مسار المشروع.
- يتم تأجيل إصلاح القائمة إلى مرحلة Menu DOM Audit لاحقة.
- لا يتم السماح لـ Codex بتنفيذ تعديل تلقائي على القائمة.
- Codex مسموح له لاحقًا بعمل Audit فقط أو اقتراح Patch، ولا يطبق أي تعديل إلا بموافقة صريحة.

Rule:
تم تأجيل إصلاح القائمة البصري. يمنع تكديس CSS إضافي الآن. نكمل بقية المشروع، وأي عودة للقائمة لاحقًا تبدأ بتشخيص DOM/Browser واضح ثم Patch واحد محسوب.

---

## Routes Inventory Audit Lock — 2026-07-07

تم تنفيذ جرد شامل لمسارات HTML العامة من Kali بدون أي تعديل على السيرفر.

- ROUTES_INVENTORY_AUDIT_STATUS=DONE
- ROUTES_INVENTORY_AUDIT_REPORT=docs/05-runbooks/NDSP_ROUTES_INVENTORY_AUDIT_20260707_210030.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الجرد:

- جميع صفحات HTML الموجودة على /var/www/ndsp-my تعمل HTTP 200
- جميع الصفحات الأساسية المقفلة تعمل HTTP 200
- جميع الصفحات الإضافية تعمل HTTP 200
- أغلب الصفحات تحتوي menu refs و disclaimer refs
- صفحة disclaimer.html مستثناة طبيعيًا لأنها صفحة الإخلاء نفسها
- لم يتم تعديل السيرفر
- لم يتم تعديل Runtime

الصفحات الأساسية المقفلة:

- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html
- /disclaimer.html

الصفحات الإضافية العاملة:

- alerts-log.html
- asset-selector.html
- completed-decisions.html
- daily-brief.html
- decision-center.html
- decision-guide.html
- decision-modes-guide.html
- decision-radar.html
- dollar-impact.html
- dollar-news.html
- my-watchlist.html
- nmp.html
- pro-guide.html
- settings.html
- support-center.html
- usd-pulse.html
- user-guide.html

Rule:
لا يتم حذف أو دمج أو إعادة تسمية أي صفحة من الصفحات العاملة إلا بعد قرار صريح. المرحلة القادمة تكون تصنيف تحسينات فقط، وليست حذف أو rebuild.

---

## Page Priority Matrix Lock — 2026-07-07

تم إنشاء مصفوفة أولويات الصفحات بعد جرد المسارات العامة.

- PAGE_PRIORITY_MATRIX_STATUS=CREATED
- PAGE_PRIORITY_MATRIX_REPORT=docs/05-runbooks/NDSP_PAGE_PRIORITY_MATRIX_20260707_210713.md
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

نتيجة التصنيف:

Priority 1 — Core User Journey:

- index.html
- NDSP_Asset_View.html / asset-selector.html
- decision-support.html / decision-center.html
- NDSP_Command_Center.html / decision-radar.html
- NDSP_Daily_Brief.html / daily-brief.html
- NDSP_Settings_Alerts.html / settings.html
- disclaimer.html

Priority 2 — User Education / Trust Pages:

- decision-guide.html
- decision-modes-guide.html
- user-guide.html
- pro-guide.html
- support-center.html

Priority 3 — Market Context Pages:

- usd-pulse.html
- dollar-impact.html
- dollar-news.html
- nmp.html

Priority 4 — History / Tracking Pages:

- my-watchlist.html
- alerts-log.html
- completed-decisions.html

ملاحظة مؤجلة:

- مشكلة القائمة البصرية مؤجلة.
- لا يتم تكديس CSS إضافي الآن.
- أي عودة للقائمة لاحقًا تبدأ بـ DOM/Browser Audit ثم Patch واحد محسوب.

Rule:
المرحلة القادمة هي تحسين محتوى وتوضيح صفحات Priority 1 فقط. لا حذف، لا دمج، لا إعادة تسمية، لا rebuild، ولا تعديل على API أو PM2 أو Nginx أو ملفات JS المحمية.

---

## Priority 1 Content Plan Lock — 2026-07-07

تم إنشاء خطة محتوى لصفحات Priority 1 بعد قفل مصفوفة أولويات الصفحات.

- PRIORITY1_CONTENT_PLAN_STATUS=CREATED
- PRIORITY1_CONTENT_PLAN_REPORT=docs/05-runbooks/NDSP_PRIORITY1_CONTENT_PLAN_20260707_211231.md
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تحديد تحسينات المحتوى والتوضيح لصفحات رحلة المستخدم الأساسية
- منع أي تعديل عشوائي على Runtime أو API أو JS المحمي
- تجهيز ترتيب عمل واضح قبل أي Patch لاحق

صفحات Priority 1:

- index.html
- NDSP_Asset_View.html / asset-selector.html
- decision-support.html / decision-center.html
- NDSP_Command_Center.html / decision-radar.html
- NDSP_Daily_Brief.html / daily-brief.html
- NDSP_Settings_Alerts.html / settings.html
- disclaimer.html

ترتيب العمل المعتمد:

1. decision-support.html / decision-center.html
2. NDSP_Asset_View.html / asset-selector.html
3. NDSP_Daily_Brief.html / daily-brief.html
4. NDSP_Command_Center.html / decision-radar.html
5. NDSP_Settings_Alerts.html / settings.html
6. index.html
7. disclaimer.html فقط عند موافقة صريحة

Rule:
الخطوة القادمة تكون Content-only Patch Plan لصفحة decision-support.html فقط. لا يتم تنفيذ Patch قبل اعتماد الخطة، ولا يتم تعديل API أو PM2 أو Nginx أو Radar JS أو Menu JS أو Disclaimer JS.

---

## Decision Support Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحة دعم القرار الرئيسية.

- DECISION_SUPPORT_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- DECISION_SUPPORT_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_DECISION_SUPPORT_CONTENT_ONLY_PATCH_PLAN_20260707_212057.md
- TARGET_PAGES=decision-support.html, decision-center.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحة دعم القرار قبل أي تعديل فعلي
- توضيح جودة القرار
- توضيح حالة السيناريو
- توضيح السياق الاتجاهي
- توضيح حالة NMP
- توضيح سبب الحذر
- تثبيت أن NDSP منصة دعم قرار فقط

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- API changes
- PM2 changes
- Nginx changes
- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. الخطوة التالية إما اعتماد Content-only Patch صغير لصفحات decision-support.html و decision-center.html، أو الانتقال لتخطيط صفحة Priority 1 التالية.

---

## Decision Support Content Patch V1A Lock — 2026-07-07

تم تنفيذ تحسين محتوى محدود ومحكوم لصفحات دعم القرار، ثم تنفيذ Hotfix لإزالة ألفاظ كانت ترفع تنبيه الحوكمة.

- DECISION_SUPPORT_CONTENT_V1_STATUS=PATCHED_WITH_ALERTS_THEN_FIXED
- DECISION_SUPPORT_CONTENT_V1A_HOTFIX_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_DECISION_SUPPORT_CONTENT_V1A_HOTFIX_20260707_203428.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_DECISION_SUPPORT_CONTENT_V1A_HOTFIX_20260707_203428.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_DECISION_SUPPORT_CONTENT_V1A_HOTFIX_20260707_203428
- TARGET_PAGES=decision-support.html, decision-center.html
- MODE=HTML_CONTENT_TEXT_HOTFIX_ONLY
- POST_PATCH_STATUS=OK

ما تم تعديله:

- إضافة/تثبيت محتوى توضيحي لصفحة دعم القرار
- توضيح جودة القرار
- توضيح حالة السيناريو
- توضيح السياق الاتجاهي
- توضيح حالة NMP
- توضيح سبب الحذر
- تثبيت أن الصفحة للفهم والمتابعة ضمن دعم القرار فقط
- إزالة العبارات التي رفعت تنبيه الحوكمة في الفحص

لم يتم تعديل:

- API
- PM2
- Nginx
- Radar JS
- Menu JS
- Disclaimer JS
- Backend runtime
- Routes

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

Rule:
صفحات decision-support.html و decision-center.html معتمدة الآن بتحسين محتوى V1A. أي تحسين لاحق على هذه الصفحات يكون Content-only أو CSS-only فقط، وبعد Backup و Patch Report و Post Patch Test.

---

## Asset View Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات اختيار الأصل والأسواق.

- ASSET_VIEW_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- ASSET_VIEW_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_ASSET_VIEW_CONTENT_ONLY_PATCH_PLAN_20260707_213943.md
- TARGET_PAGES=NDSP_Asset_View.html, asset-selector.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات اختيار الأصل قبل أي تعديل فعلي
- توضيح أن اختيار الأصل يحدد نطاق القراءة فقط
- توضيح مجموعات الأسواق
- توضيح معنى السعر الحي
- توضيح جودة القرار
- توضيح حالة السيناريو
- توضيح الخطوة التالية نحو صفحة دعم القرار

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- API changes
- PM2 changes
- Nginx changes
- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. الخطوة التالية إما اعتماد Content-only Patch صغير لصفحات NDSP_Asset_View.html و asset-selector.html، أو الانتقال لتخطيط صفحة Priority 1 التالية.

---

## Asset View Content Patch V1 Lock — 2026-07-07

تم تنفيذ تحسين محتوى محدود ومحكوم لصفحات اختيار الأصل والأسواق.

- ASSET_VIEW_CONTENT_V1_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_ASSET_VIEW_CONTENT_V1_20260707_204602.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_ASSET_VIEW_CONTENT_V1_20260707_204602.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_ASSET_VIEW_CONTENT_PATCH_V1_20260707_204602
- TARGET_PAGES=NDSP_Asset_View.html, asset-selector.html
- MODE=HTML_CONTENT_ONLY
- POST_PATCH_STATUS=OK

ما تم تعديله:

- إضافة محتوى توضيحي لاختيار الأصل
- توضيح أن اختيار الأصل يحدد نطاق القراءة فقط
- توضيح مجموعات الأسواق
- توضيح معنى السعر الحي
- توضيح جودة القرار
- توضيح حالة السيناريو
- توضيح الخطوة التالية نحو صفحة دعم القرار
- إضافة تنبيه حوكمة آمن للفهم والمتابعة

لم يتم تعديل:

- API
- PM2
- Nginx
- Radar JS
- Menu JS
- Disclaimer JS
- Backend runtime
- Routes

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

Rule:
صفحات NDSP_Asset_View.html و asset-selector.html معتمدة الآن بتحسين محتوى V1. أي تحسين لاحق يكون Content-only أو CSS-only فقط، وبعد Backup و Patch Report و Post Patch Test.

---

## Daily Brief Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات الموجز اليومي.

- DAILY_BRIEF_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- DAILY_BRIEF_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_DAILY_BRIEF_CONTENT_ONLY_PATCH_PLAN_20260707_215051.md
- TARGET_PAGES=NDSP_Daily_Brief.html, daily-brief.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات الموجز اليومي قبل أي تعديل فعلي
- توضيح أن الموجز اليومي ملخص متابعة وليس قرارًا مكتملًا
- توضيح السياق اليومي
- توضيح الفرق بين قوة القراءة واكتمال القراءة
- توضيح معنى تحت المتابعة
- توضيح سبب الحذر
- توضيح ما يجب مراقبته للفهم والمتابعة

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- API changes
- PM2 changes
- Nginx changes
- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. الخطوة التالية إما اعتماد Content-only Patch صغير لصفحات NDSP_Daily_Brief.html و daily-brief.html، أو الانتقال لتخطيط صفحة Priority 1 التالية.

---

## Daily Brief Content Patch V1 Lock — 2026-07-07

تم تنفيذ تحسين محتوى محدود ومحكوم لصفحات الموجز اليومي.

- DAILY_BRIEF_CONTENT_V1_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_DAILY_BRIEF_CONTENT_V1_20260707_205606.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_DAILY_BRIEF_CONTENT_V1_20260707_205606.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_DAILY_BRIEF_CONTENT_PATCH_V1_20260707_205606
- TARGET_PAGES=NDSP_Daily_Brief.html, daily-brief.html
- MODE=HTML_CONTENT_ONLY
- POST_PATCH_STATUS=OK

ما تم تعديله:

- إضافة محتوى توضيحي للموجز اليومي
- توضيح أن الموجز اليومي ملخص متابعة وليس قرارًا مكتملًا
- توضيح السياق اليومي
- توضيح الفرق بين قوة القراءة واكتمال القراءة
- توضيح معنى تحت المتابعة
- توضيح سبب الحذر
- توضيح ما يجب مراقبته اليوم
- إضافة تنبيه حوكمة آمن للفهم والمتابعة

لم يتم تعديل:

- API
- PM2
- Nginx
- Radar JS
- Menu JS
- Disclaimer JS
- Backend runtime
- Routes

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

Rule:
صفحات NDSP_Daily_Brief.html و daily-brief.html معتمدة الآن بتحسين محتوى V1. أي تحسين لاحق يكون Content-only أو CSS-only فقط، وبعد Backup و Patch Report و Post Patch Test.

---

## Command Center Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات مركز القيادة ورادار القرار.

- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_20260707_220358.md
- TARGET_PAGES=NDSP_Command_Center.html, decision-radar.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات مركز القيادة قبل أي تعديل فعلي
- توضيح دور الرادار كعرض متابعة وسياق مخاطر
- توضيح دلالة الألوان
- توضيح توازن المخاطر
- توضيح الفرق بين قوة القراءة واكتمال القراءة
- تثبيت أن الصفحة للفهم والمتابعة ضمن إطار دعم القرار فقط

مكونات محمية لا يتم لمسها:

- Radar JS
- Radar safe-clean asset
- Menu JS
- Disclaimer JS
- API gateway
- PM2 runtime
- Nginx
- Backend runtime

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- API changes
- PM2 changes
- Nginx changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. أي تعديل لاحق على صفحات مركز القيادة يكون Content-only أو CSS-only فقط، ولا يلمس الرادار أو ملفاته المحمية.

---

## Command Center Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات مركز القيادة ورادار القرار.

- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_20260707_220358.md
- TARGET_PAGES=NDSP_Command_Center.html, decision-radar.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات مركز القيادة قبل أي تعديل فعلي
- توضيح دور الرادار كعرض متابعة وسياق مخاطر
- توضيح دلالة الألوان
- توضيح توازن المخاطر
- توضيح الفرق بين قوة القراءة واكتمال القراءة
- تثبيت أن الصفحة للفهم والمتابعة ضمن إطار دعم القرار فقط

مكونات محمية لا يتم لمسها:

- Radar JS
- Radar safe-clean asset
- Menu JS
- Disclaimer JS
- API gateway
- PM2 runtime
- Nginx
- Backend runtime

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- API changes
- PM2 changes
- Nginx changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. أي تعديل لاحق على صفحات مركز القيادة يكون Content-only أو CSS-only فقط، ولا يلمس الرادار أو ملفاته المحمية.

---

## Command Center Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات مركز القيادة ورادار القرار.

- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_COMMAND_CENTER_CONTENT_ONLY_PATCH_PLAN_20260707_220358.md
- TARGET_PAGES=NDSP_Command_Center.html, decision-radar.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات مركز القيادة قبل أي تعديل فعلي
- توضيح دور الرادار كعرض متابعة وسياق مخاطر
- توضيح دلالة الألوان
- توضيح توازن المخاطر
- توضيح الفرق بين قوة القراءة واكتمال القراءة
- تثبيت أن الصفحة للفهم والمتابعة ضمن إطار دعم القرار فقط

مكونات محمية لا يتم لمسها:

- Radar JS
- Radar safe-clean asset
- Menu JS
- Disclaimer JS
- API gateway
- PM2 runtime
- Nginx
- Backend runtime

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- API changes
- PM2 changes
- Nginx changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. أي تعديل لاحق على صفحات مركز القيادة يكون Content-only أو CSS-only فقط، ولا يلمس الرادار أو ملفاته المحمية.

---

## Command Center Content Patch V1 Lock — 2026-07-07

تم تنفيذ تحسين محتوى محدود ومحكوم لصفحات مركز القيادة ورادار القرار.

- COMMAND_CENTER_CONTENT_V1_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_COMMAND_CENTER_CONTENT_V1_20260707_214346.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_COMMAND_CENTER_CONTENT_V1_20260707_214346.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_COMMAND_CENTER_CONTENT_PATCH_V1_20260707_214346
- TARGET_PAGES=NDSP_Command_Center.html, decision-radar.html
- MODE=HTML_CONTENT_ONLY
- POST_PATCH_STATUS=OK
- RADAR_JS_STATUS=UNCHANGED
- RADAR_SHA=ca07216a5346403af56ca23cdaef4f4425ac6fdf2a95340b6844451dc85c93ff

ما تم تعديله:

- إضافة محتوى توضيحي لمركز القيادة
- توضيح دور رادار القرار
- توضيح دلالة الألوان
- توضيح توازن المخاطر
- توضيح الفرق بين قوة القراءة واكتمالها
- توضيح ما يجب مراقبته الآن
- إضافة تنبيه حوكمة آمن للفهم والمتابعة

لم يتم تعديل:

- Radar JS
- API
- PM2
- Nginx
- Menu JS
- Disclaimer JS
- Backend runtime
- Routes

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

Rule:
صفحات NDSP_Command_Center.html و decision-radar.html معتمدة الآن بتحسين محتوى V1. أي تحسين لاحق يكون Content-only أو CSS-only فقط، وبعد Backup و Patch Report و Post Patch Test، ولا يتم لمس Radar JS إلا بموافقة صريحة.

---

## Settings & Alerts Content-only Patch Plan Lock — 2026-07-07

تم إنشاء خطة تحسين محتوى آمنة لصفحات الإعدادات والتنبيهات.

- SETTINGS_ALERTS_CONTENT_ONLY_PATCH_PLAN_STATUS=CREATED
- SETTINGS_ALERTS_CONTENT_ONLY_PATCH_PLAN_REPORT=docs/05-runbooks/NDSP_SETTINGS_ALERTS_CONTENT_ONLY_PATCH_PLAN_20260707_224918.md
- TARGET_PAGES=NDSP_Settings_Alerts.html, settings.html
- MODE=PLANNING_ONLY
- MODIFICATIONS=None

الغرض:

- تجهيز تحسين محتوى صفحات الإعدادات والتنبيهات قبل أي تعديل فعلي
- توضيح أن التنبيهات أدوات متابعة وليست قرارات مكتملة
- توضيح تفضيلات المتابعة
- توضيح الأصول المراقبة
- توضيح تنبيه جودة القراءة
- توضيح تنبيه حالة السيناريو
- توضيح تنبيه سبب الحذر
- تثبيت أن الصفحة للفهم والمتابعة ضمن إطار دعم القرار فقط

نطاق التعديل المستقبلي المسموح بعد الموافقة:

- HTML text blocks
- static explanatory cards
- CSS-only polish إذا لزم
- cache-busting للصفحات المستهدفة إذا لزم

غير مسموح بدون موافقة صريحة:

- API changes
- PM2 changes
- Nginx changes
- Radar JS changes
- Menu JS changes
- Disclaimer JS changes
- Backend runtime changes
- route deletion or rename

Rule:
لا يتم تنفيذ Patch الآن. الخطوة التالية اعتماد Content-only Patch صغير لصفحات NDSP_Settings_Alerts.html و settings.html فقط، مع Backup و Patch Report و Post Patch Test.

---

## Settings & Alerts Content Patch V1 Lock — 2026-07-07

تم تنفيذ تحسين محتوى محدود ومحكوم لصفحات الإعدادات والتنبيهات.

- SETTINGS_ALERTS_CONTENT_V1_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_SETTINGS_ALERTS_CONTENT_V1_20260707_215551.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_SETTINGS_ALERTS_CONTENT_V1_20260707_215551.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_SETTINGS_ALERTS_CONTENT_PATCH_V1_20260707_215551
- TARGET_PAGES=NDSP_Settings_Alerts.html, settings.html
- MODE=HTML_CONTENT_ONLY
- POST_PATCH_STATUS=OK

ما تم تعديله:

- إضافة محتوى توضيحي للإعدادات والتنبيهات
- توضيح أن التنبيهات أدوات متابعة وليست قراءات مكتملة
- توضيح تفضيلات المتابعة
- توضيح الأصول المراقبة
- توضيح تنبيه جودة القراءة
- توضيح تنبيه حالة السيناريو
- توضيح تنبيه سبب الحذر
- إضافة تنبيه حوكمة آمن للفهم والمتابعة

لم يتم تعديل:

- API
- PM2
- Nginx
- Radar JS
- Menu JS
- Disclaimer JS
- Backend runtime
- Routes

نتائج Post Patch Test:

- جميع الصفحات الرسمية HTTP 200
- حقول API المطلوبة موجودة
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

Rule:
صفحات NDSP_Settings_Alerts.html و settings.html معتمدة الآن بتحسين محتوى V1. أي تحسين لاحق يكون Content-only أو CSS-only فقط، وبعد Backup و Patch Report و Post Patch Test.

---

## V1 Functional Audit Read-only Lock — 2026-07-07

تم تنفيذ فحص وظيفي قراءة فقط لمنصة NDSP بعد تحسين محتوى صفحات Priority 1 الداخلية.

- V1_FUNCTIONAL_AUDIT_READONLY_STATUS=DONE
- AUDIT_RESULT=OK_WITH_NOTES
- REPORT=docs/05-runbooks/NDSP_V1_FUNCTIONAL_AUDIT_READONLY_20260707_220125.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- جميع صفحات Alias الأساسية HTTP 200
- صفحة login.html تعمل HTTP 200
- صفحة register.html تعمل HTTP 200
- API health يعمل HTTP 200
- API status يعمل HTTP 200
- Decision API يعمل على ETHUSDT و BTCUSDT و XAUUSD و USOIL
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- جميع Content V1 markers موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

ملاحظات لا تعتبر فشلًا في صفحات Priority 1:

- /login يعطي 404 بينما /login.html يعمل
- /register يعطي 404 بينما /register.html يعمل
- /forgot-password يعطي 404
- /reset-password يعطي 404
- XAUUSD و USOIL يعيدان nmp_status=UNAVAILABLE و nmp_level=None

تفسير الملاحظات:

- ملاحظات /login و /register و forgot/reset هي ملاحظات Routing/Auth Candidate Pages وتحتاج خطة Route Alias أو Auth Routes منفصلة.
- حالة NMP غير المتاحة لبعض الأصول تعتبر حالة بيانات/قراءة وليست فشل واجهة إذا تم عرضها كغير متاحة.
- الفحص لم يغيّر ملفات الموقع ولم يغيّر API أو PM2 أو Nginx أو Backend.

Rule:
V1 Functional Audit معتمد بنتيجة OK_WITH_NOTES. أي إصلاح لاحق لمسارات الدخول أو التسجيل أو استعادة كلمة المرور يجب أن يبدأ بخطة منفصلة، ثم Backup، ثم Patch Report، ثم Post Patch Test، دون لمس الصفحات الداخلية المكتملة إلا بموافقة صريحة.

---

## V1 Functional Audit Read-only Lock — 2026-07-07

تم تنفيذ فحص وظيفي قراءة فقط لمنصة NDSP بعد تحسين محتوى صفحات Priority 1 الداخلية.

- V1_FUNCTIONAL_AUDIT_READONLY_STATUS=DONE
- AUDIT_RESULT=OK_WITH_NOTES
- REPORT=docs/05-runbooks/NDSP_V1_FUNCTIONAL_AUDIT_READONLY_20260707_220125.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- جميع الصفحات الرسمية HTTP 200
- جميع صفحات Alias الأساسية HTTP 200
- صفحة login.html تعمل HTTP 200
- صفحة register.html تعمل HTTP 200
- API health يعمل HTTP 200
- API status يعمل HTTP 200
- Decision API يعمل على ETHUSDT و BTCUSDT و XAUUSD و USOIL
- الرادار موجود
- القائمة موجودة
- بوابة الإخلاء موجودة
- جميع Content V1 markers موجودة
- لا توجد ألفاظ ممنوعة في الواجهة العامة
- ndsp-portal online
- PM2 restarts = 0

ملاحظات لا تعتبر فشلًا في صفحات Priority 1:

- /login يعطي 404 بينما /login.html يعمل
- /register يعطي 404 بينما /register.html يعمل
- /forgot-password يعطي 404
- /reset-password يعطي 404
- XAUUSD و USOIL يعيدان nmp_status=UNAVAILABLE و nmp_level=None

تفسير الملاحظات:

- ملاحظات /login و /register و forgot/reset هي ملاحظات Routing/Auth Candidate Pages وتحتاج خطة Route Alias أو Auth Routes منفصلة.
- حالة NMP غير المتاحة لبعض الأصول تعتبر حالة بيانات/قراءة وليست فشل واجهة إذا تم عرضها كغير متاحة.
- الفحص لم يغيّر ملفات الموقع ولم يغيّر API أو PM2 أو Nginx أو Backend.

Rule:
V1 Functional Audit معتمد بنتيجة OK_WITH_NOTES. أي إصلاح لاحق لمسارات الدخول أو التسجيل أو استعادة كلمة المرور يجب أن يبدأ بخطة منفصلة، ثم Backup، ثم Patch Report، ثم Post Patch Test، دون لمس الصفحات الداخلية المكتملة إلا بموافقة صريحة.

---

## Auth Source Resolution Read-only Lock — 2026-07-07

تم تنفيذ فحص قراءة فقط لتحديد مصدر صفحات الدخول والتسجيل واستعادة كلمة المرور.

- AUTH_SOURCE_RESOLUTION_READONLY_STATUS=DONE
- REPORT=docs/05-runbooks/NDSP_AUTH_SOURCE_RESOLUTION_READONLY_20260707_224027.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- /login.html يعمل HTTP 200
- /register.html يعمل HTTP 200
- /forgot-password.html يعمل HTTP 200
- /reset-password.html يعمل HTTP 200
- /password-reset يعمل HTTP 200
- /password-reset.html يعمل HTTP 200
- /login يعطي HTTP 404
- /register يعطي HTTP 404
- /forgot-password يعطي HTTP 404
- /reset-password يعطي HTTP 404
- ndsp-portal online
- PM2 restarts = 0
- مصدر PM2 الحالي: /home/nawaf511/empire-core-new/apps/user-portal

الاستنتاج:

- صفحات auth ذات امتداد .html تعمل.
- المسارات المختصرة بدون .html تحتاج Route Alias منفصل.
- لم يتم تعديل Nginx أو PM2 أو Backend أو API أو ملفات الموقع.
- لا يتم إنشاء static aliases داخل /var/www/ndsp-my قبل تحديد آلية التوجيه النهائية.

Rule:
أي إصلاح لمسارات /login أو /register أو /forgot-password أو /reset-password يجب أن يكون ضمن Patch منفصل باسم Auth Route Alias، مع Backup و Patch Report و Post Patch Test. لا يتم لمس صفحات Priority 1 الداخلية المكتملة.

---

## Auth Route Alias Patch V1 Lock — 2026-07-07

تم تنفيذ إصلاح آمن لمسارات الدخول والتسجيل واستعادة كلمة المرور المختصرة.

- AUTH_ROUTE_ALIAS_V1_STATUS=APPLIED
- PATCH_REPORT=docs/05-runbooks/NDSP_PATCH_AUTH_ROUTE_ALIAS_V1_20260707_225005.md
- POST_PATCH_TEST=docs/05-runbooks/NDSP_POST_PATCH_TEST_AUTH_ROUTE_ALIAS_V1_20260707_225005.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_AUTH_ROUTE_ALIAS_PATCH_V1_20260707_225005
- MODE=STATIC_ROUTE_ALIAS_ONLY
- POST_PATCH_STATUS=OK

المسارات التي تم إصلاحها:

- /login -> /login.html
- /register -> /register.html
- /forgot-password -> /forgot-password.html
- /reset-password -> /reset-password.html

نتائج الفحص بعد الإصلاح:

- /login يعمل HTTP 200
- /register يعمل HTTP 200
- /forgot-password يعمل HTTP 200
- /reset-password يعمل HTTP 200
- /login.html يعمل HTTP 200
- /register.html يعمل HTTP 200
- /forgot-password.html يعمل HTTP 200
- /reset-password.html يعمل HTTP 200
- /password-reset يعمل HTTP 200
- /password-reset.html يعمل HTTP 200
- Post Patch Test = OK
- لا توجد ألفاظ ممنوعة
- ndsp-portal online
- PM2 restarts = 0

ما لم يتم تعديله:

- Nginx
- PM2
- API
- Backend
- صفحات Priority 1 الداخلية المكتملة
- Radar JS
- Menu JS
- Disclaimer JS

Rule:
Auth Route Alias V1 معتمد. أي تعديل لاحق على مسارات الدخول أو التسجيل أو استعادة كلمة المرور يجب أن يكون ضمن Patch منفصل مع Backup و Patch Report و Post Patch Test.

---

## Final V1 Release Readiness Lock — 2026-07-07

تم تنفيذ فحص الجاهزية النهائي لإصدار NDSP V1 بعد تحسين الصفحات الداخلية وإصلاح مسارات الدخول والتسجيل واستعادة كلمة المرور.

- FINAL_V1_RELEASE_READINESS_STATUS=OK
- RELEASE_RESULT=READY_WITH_GOVERNANCE_LOCK
- REPORT=docs/05-runbooks/NDSP_FINAL_V1_RELEASE_READINESS_AUDIT_20260707_225738.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص النهائي:

- Official Priority Pages HTTP 200
- Alias Pages HTTP 200
- Auth Routes HTTP 200
- API Health HTTP 200
- API Status HTTP 200
- Decision API Required Fields موجودة
- Protected UI markers موجودة
- Content V1 markers موجودة
- Auth Route Alias markers موجودة
- Forbidden public wording count = 0
- ndsp-portal online
- PM2 restarts = 0

الصفحات الرسمية المعتمدة:

- /
- /index.html
- /decision-support.html
- /NDSP_Asset_View.html
- /NDSP_Command_Center.html
- /NDSP_Daily_Brief.html
- /NDSP_Settings_Alerts.html
- /disclaimer.html

صفحات Alias المعتمدة:

- /decision-center.html
- /asset-selector.html
- /decision-radar.html
- /daily-brief.html
- /settings.html

مسارات Auth المعتمدة:

- /login
- /login.html
- /register
- /register.html
- /forgot-password
- /forgot-password.html
- /reset-password
- /reset-password.html
- /password-reset
- /password-reset.html

حالة الحوكمة:

- NDSP يعمل كمنصة دعم قرار فقط.
- لا توجد ألفاظ عامة مخالفة للحوكمة.
- لا توجد صياغات توصية مالية أو وعود ربح أو أوامر مباشرة.
- بوابة الإخلاء موجودة.
- الرادار موجود.
- القائمة موجودة.
- صفحات Priority 1 الداخلية مكتملة.

ما لم يتم تعديله أثناء الفحص النهائي:

- Nginx
- PM2
- API
- Backend
- Radar JS
- Menu JS
- Disclaimer JS
- صفحات Priority 1

Rule:
NDSP V1 Release Readiness معتمد بنتيجة READY_WITH_GOVERNANCE_LOCK. أي تعديل لاحق يجب أن يكون ضمن Patch منفصل مع Backup و Patch Report و Post Patch Test. لا يتم لمس runtime أو Nginx أو API أو PM2 أو الملفات المحمية إلا بموافقة صريحة.

---

## NDSP V1 Release Package Lock — 2026-07-07

تم إنشاء حزمة إصدار NDSP V1 النهائية بعد اعتماد Final V1 Release Readiness.

- V1_RELEASE_PACKAGE_STATUS=CREATED
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V1_RELEASE_PACKAGE_20260707_230119.tar.gz.sha256
- SHA256=1021596e6cc4fd1e36e375b1c4f67fe77426463902ad4c23c6020c1041671144
- PACKAGE_SIZE=116K
- REPORT=docs/05-runbooks/NDSP_V1_RELEASE_PACKAGE_REPORT_20260707_230119.md
- MODE=PACKAGE_ONLY
- MODIFICATIONS=None

محتويات الحزمة:

- Reality Lock
- Runbooks وتقارير 2026-07-07
- Final V1 Release Readiness Audit
- Route Status Manifest
- API samples
- Runtime PM2 snapshot
- Live file checksums
- Version Summary Arabic

حالة الإصدار:

- FINAL_V1_RELEASE_READINESS_STATUS=OK
- RELEASE_RESULT=READY_WITH_GOVERNANCE_LOCK
- V1_RELEASE_PACKAGE_STATUS=CREATED

Rule:
هذه الحزمة تمثل لقطة إصدار NDSP V1 المعتمدة. أي تعديل بعد هذه النقطة يجب أن ينتج عنه Patch مستقل أو حزمة إصدار جديدة مع Backup و Patch Report و Post Patch Test و Reality Lock update.

---

## Governance Docs Normalization P0 Lock — 2026-07-07

تم تنفيذ P0 Governance Docs Normalization لإنشاء وتثبيت مستندات التحكم الناقصة داخل المشروع.

- GOVERNANCE_DOCS_NORMALIZATION_P0_STATUS=APPLIED
- DOCS_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_GOVERNANCE_DOCS_NORMALIZATION_P0_20260707_232113.md
- BACKUP=/home/nawaf511/ndsp_backups/NDSP_GOVERNANCE_DOCS_NORMALIZATION_P0_20260707_232113
- MODE=DOCS_ONLY
- MODIFICATIONS=docs_and_optional_README_only

النتائج:

- MISSING_CONTROL_DOCS_AFTER=0
- GOVERNING_SENTENCE_COUNT_AFTER=20
- SEVEN_CONTRACTS_MENTION_COUNT_AFTER=45

تم إنشاء/تثبيت مستندات التحكم التالية:

- NDSP_MASTER_GOVERNANCE_RULES.md
- NDSP_PAGE_REGISTRY.md
- NDSP_API_CONTRACT.md
- NDSP_DATABASE_SCHEMA.md
- NDSP_DECISION_ENGINES_SPEC.md
- NDSP_SECURITY_POLICY.md
- NDSP_TEST_PLAN.md
- NDSP_DEPLOYMENT_RUNBOOK.md
- NDSP_ROLLBACK_PLAN.md
- NDSP_PROTECTED_FILES_AND_RULES.md
- NDSP_AI_BUILDER_PROMPT.md

كما تم إنشاء:

- NDSP_V1_FREEZE_EN.md
- NDSP_LEGAL_DISCLAIMER_MASTER_EN.md
- NDSP_IMPLEMENTATION_TASKS_EN.md
- NDSP_DECISION_ROOM_24_AXES_LOCK_CHECKLIST_AR.md
- docs/README.md
- تحديث README.md بالجملة الحاكمة عند الحاجة

ما لم يتم تعديله:

- Nginx
- PM2
- API
- Backend runtime
- Live frontend
- Radar JS
- Menu JS
- Disclaimer JS

Rule:
P0 Governance Docs Normalization معتمد. أي تعديل لاحق يجب أن يكون Patch مستقل مع Backup وReport وPost Patch Test وReality Lock update.

---

## Post P0 Governance Verification Lock — 2026-07-07

تم تنفيذ فحص قراءة فقط بعد P0 Governance Docs Normalization للتأكد من اكتمال مستندات التحكم والحكم العام.

- POST_P0_GOVERNANCE_VERIFICATION_STATUS=OK
- GOVERNANCE_DOCS_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_POST_P0_GOVERNANCE_VERIFICATION_20260707_232444.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج التحقق:

- MISSING_CONTROL_DOCS_AFTER=0
- GOVERNING_SENTENCE_COUNT_AFTER=20
- SEVEN_CONTRACTS_MENTION_COUNT_AFTER=45
- AXES_24_MENTION_COUNT_AFTER=5
- ROUTES_OK=1
- API_OK=1

تم تأكيد وجود مستندات التحكم التالية:

- NDSP_MASTER_GOVERNANCE_RULES.md
- NDSP_PAGE_REGISTRY.md
- NDSP_API_CONTRACT.md
- NDSP_DATABASE_SCHEMA.md
- NDSP_DECISION_ENGINES_SPEC.md
- NDSP_SECURITY_POLICY.md
- NDSP_TEST_PLAN.md
- NDSP_DEPLOYMENT_RUNBOOK.md
- NDSP_ROLLBACK_PLAN.md
- NDSP_PROTECTED_FILES_AND_RULES.md
- NDSP_AI_BUILDER_PROMPT.md

تم تأكيد:

- الجملة الحاكمة موجودة
- العقود السبعة مذكورة
- محاور غرفة القرار موثقة
- الصفحات الرسمية تعمل HTTP 200
- مسارات Auth تعمل HTTP 200
- Decision API يعمل على ETHUSDT و BTCUSDT

ما لم يتم تعديله:

- Nginx
- PM2
- API
- Backend
- Live frontend
- Radar JS
- Menu JS
- Disclaimer JS

Rule:
P0 مكتمل ومثبت. المرحلة التالية هي P1 Controlled Auth Functional Test، ويجب أن تبدأ بفحص/اختبار مستقل مع تقرير منفصل دون كسر V1 Release Lock.

---

## P1 Auth Functional Discovery Read-only Lock — 2026-07-07

تم تنفيذ فحص قراءة فقط لمسارات التسجيل والدخول واستعادة كلمة المرور قبل إنشاء أي مستخدم اختبار.

- P1_AUTH_FUNCTIONAL_DISCOVERY_READONLY_STATUS=DONE
- REPORT=docs/05-runbooks/NDSP_P1_AUTH_FUNCTIONAL_DISCOVERY_READONLY_20260707_232843.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- صفحات Auth الأمامية تعمل.
- /api/trial/status يشير إلى registration_endpoint=/api/trial/register/ordinary
- /api/auth/login ظاهر في Nginx ويذهب إلى 127.0.0.1:9020
- /api/auth/register ظاهر في Nginx ويذهب إلى 127.0.0.1:9028
- /api/trial/register/ ظاهر في Nginx ويذهب إلى 127.0.0.1:9019
- /api/auth/me غير مؤكد ويعطي 404 سابقاً
- ndsp-portal online
- PM2 restarts = 0

الاستنتاج:

- أفضل مسار تسجيل لاختبار P1 هو /api/trial/register/ordinary
- أفضل مسار دخول لاختبار P1 هو /api/auth/login
- لا يتم اختبار reset password الكامل قبل وجود مسار token مؤكد أو بريد اختبار قابل للقراءة.

Rule:
الاختبار التالي يجب أن يكون Controlled Auth Functional Test بمستخدم اختبار واحد فقط، مع تقرير مستقل، وعدم تعديل Nginx أو PM2 أو API أو Backend.

---

## P1 Controlled Auth Functional Test Lock — 2026-07-07

تم تنفيذ اختبار وظيفي مضبوط لمسارات التسجيل والدخول واستعادة كلمة المرور باستخدام مستخدم اختبار واحد فقط.

- P1_CONTROLLED_AUTH_FUNCTIONAL_TEST_STATUS=OK
- AUTH_FUNCTIONAL_STATUS=OK_WITH_RESET_TOKEN_FLOW_PENDING_IF_FORGOT_NOT_CONFIRMED
- REPORT=docs/05-runbooks/NDSP_P1_CONTROLLED_AUTH_FUNCTIONAL_TEST_20260707_233231.md
- MODE=CONTROLLED_WRITE_TEST
- MODIFICATIONS=One generated test account only

نتائج الاختبار:

- PAGES_OK=1
- REGISTER_OK=1
- DUPLICATE_OK=1
- LOGIN_OK=1
- BAD_LOGIN_OK=1
- FORGOT_OK=1

تم تأكيد:

- صفحات Auth تعمل HTTP 200
- التسجيل التجريبي يعمل عبر /api/trial/register/ordinary
- منع التكرار يعمل 409
- الدخول يعمل عبر /api/auth/login
- كلمة المرور الخاطئة مرفوضة 401
- طلب forgot-password مقبول 200
- ndsp-portal online
- PM2 restarts = 0

ملاحظات:

- تم إخفاء كلمة مرور الاختبار من التقرير.
- اختبار reset token الكامل لا يزال يحتاج بريد اختبار قابل للقراءة أو مسار token داخلي موثق.

ما لم يتم تعديله:

- Nginx
- PM2
- API
- Backend runtime
- Live frontend
- Radar JS
- Menu JS
- Disclaimer JS

Rule:
P1 Auth Functional Test معتمد. أي اختبار reset-token كامل أو تعديل لاحق يجب أن يكون Patch/Test مستقل مع تقرير منفصل.

---

## P1 Disclaimer Gate Functional Test Lock — 2026-07-07

تم تنفيذ فحص وظيفي قراءة فقط لبوابة إخلاء المسؤولية داخل واجهة NDSP.

- P1_DISCLAIMER_GATE_FUNCTIONAL_TEST_STATUS=OK
- DISCLAIMER_GATE_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P1_DISCLAIMER_GATE_FUNCTIONAL_TEST_FIXED_20260707_235929.md
- MODE=READ_ONLY_FRONTEND_CONTRACT_TEST
- MODIFICATIONS=None

نتائج الاختبار:

- DISCLAIMER_PAGE_CODE=200
- ASSET_OK=1
- REF_OK=1
- SCRIPT_OK=1
- CONTENT_OK=1
- FORBIDDEN_WORDING_COUNT=0

تم تأكيد:

- صفحة disclaimer.html تعمل HTTP 200
- ملف /assets/ndsp-disclaimer-gate.js موجود
- جميع الصفحات الرسمية تشير إلى بوابة الإخلاء
- سكربت البوابة يحتوي localStorage و disclaimer و accept و location و disclaimer.html
- صفحة الإخلاء تحتوي: ليست توصية، دعم قرار، إخلاء، أوافق، NDSP
- لا توجد ألفاظ مخالفة مثل اشتر الآن / بيع الآن / ربح مضمون
- ndsp-portal online
- PM2 restarts = 0

ما لم يتم تعديله:

- Nginx
- PM2
- API
- Backend runtime
- Live frontend
- Radar JS
- Menu JS
- Disclaimer JS

Rule:
P1 Disclaimer Gate معتمد. أي تعديل لاحق على الإخلاء أو البوابة يجب أن يكون Patch مستقل مع Backup وReport وPost Patch Test وReality Lock update.

---

## V1.2 Scenario Levels Discovery Read-only Lock — 2026-07-08

تم تنفيذ فحص قراءة فقط لاكتشاف حالة مستويات السيناريو داخل Decision API والواجهة.

- V12_SCENARIO_LEVELS_DISCOVERY_STATUS=DONE
- SCENARIO_LEVELS_CURRENT_STATUS=ALREADY_PRESENT
- REPORT=docs/05-runbooks/NDSP_V12_SCENARIO_LEVELS_DISCOVERY_READONLY_20260708_000331.md
- MODE=READ_ONLY
- MODIFICATIONS=None

نتائج الفحص:

- MISSING_LEVELS_SYMBOL_COUNT=0
- SOURCE_MATCH_COUNT=1050
- FRONTEND_MATCH_COUNT=48
- ndsp-scenario-levels-adapter.service active running
- quality-live route يمر عبر 127.0.0.1:9082 حسب Nginx الحالي
- PM2 ndsp-portal online
- PM2 restarts = 0

العقد المطلوب لمستويات السيناريو:

- scenario_levels.activation
- scenario_levels.arrival
- scenario_levels.review
- scenario_levels.invalidation

Rule:
لا يتم تنفيذ Patch لإضافة مستويات السيناريو قبل تشغيل Strict Contract Validator للتأكد من جودة الحقول وليس مجرد وجودها.

---

## V1.2 Scenario Levels Strict Validator Lock — 2026-07-08

تم تنفيذ Strict Contract Validator لعقد مستويات السيناريو داخل /api/decision/quality-live.

- V12_SCENARIO_LEVELS_STRICT_VALIDATOR_STATUS=WITH_ALERTS
- SCENARIO_LEVELS_STRICT_STATUS=CHECK_ALERTS
- REPORT=docs/05-runbooks/NDSP_V12_SCENARIO_LEVELS_STRICT_VALIDATOR_20260708_000702.md
- MODE=READ_ONLY_CONTRACT_VALIDATION
- MODIFICATIONS=None

نتائج التحقق:

- VALID_ALL=0
- ETHUSDT=FAIL
- BTCUSDT=FAIL
- XAUUSD=FAIL
- USOIL=FAIL

سبب التنبيه:

- scenario_levels/reference_levels object غير موجود داخل مخرجات /api/decision/quality-live العامة.
- يوجد scenario key عام، لكن لا يحتوي عقد levels المطلوب.
- discovery السابق كان غير كافٍ لأنه أثبت وجود مؤشرات/مصادر أو خدمات، وليس اكتمال العقد النهائي.

العقد المطلوب لاحقًا:

- scenario_levels.activation.price
- scenario_levels.activation.label_ar
- scenario_levels.activation.source
- scenario_levels.arrival.price
- scenario_levels.arrival.label_ar
- scenario_levels.arrival.source
- scenario_levels.review.price
- scenario_levels.review.label_ar
- scenario_levels.review.source
- scenario_levels.invalidation.price
- scenario_levels.invalidation.label_ar
- scenario_levels.invalidation.source

Rule:
لا يتم تعديل API أو Nginx أو wrapper قبل تنفيذ Source Resolver Read-only لتحديد مكان خدمة السيناريو الحالية ومسار دمجها الصحيح في quality-live.

---

## V1.2 Scenario Levels Source Resolver Read-only Lock — 2026-07-08

تم تنفيذ Source Resolver قراءة فقط لتحديد مصدر مستويات السيناريو ومسار دمجها في /api/decision/quality-live.

- V12_SCENARIO_LEVELS_SOURCE_RESOLVER_STATUS=DONE
- REPORT=docs/05-runbooks/NDSP_V12_SCENARIO_LEVELS_SOURCE_RESOLVER_READONLY_20260708_001039.md
- MODE=READ_ONLY_SOURCE_AND_ROUTE_RESOLUTION
- MODIFICATIONS=None

نتائج الفحص:

- PUBLIC_QUALITY_LIVE_LEVELS=ABSENT_FROM_STRICT_VALIDATOR
- الحقول موجودة داخل scenario بصيغة مسطحة:
  - scenario_activation_level
  - scenario_arrival_level
  - scenario_review_zone
  - scenario_invalidation_level
- لا يوجد top-level scenario_levels
- لا يوجد top-level reference_levels
- Nginx public quality-live route يمر عبر 127.0.0.1:9082
- 9082 هو ndsp-quality-live-nmp-wrapper
- upstream للـ 9082 هو 9067
- 9067 يعيد الحقول المسطحة داخل scenario
- ndsp-scenario-levels-adapter.service يعمل على port 9034 لكنه ليس مدمجًا في public quality-live النهائي

الاستنتاج:

أقل Patch آمن هو تعديل wrapper 9082 لإضافة عقد scenario_levels مشتقة من الحقول الموجودة أصلًا داخل scenario، بدون اختراع أرقام وبدون تغيير Nginx.

Rule:
Patch V1.2 يجب أن يحافظ على كل حقول V1 الحالية، ويضيف scenario_levels فقط كعقدة إضافية، مع Backup وReport وPost Patch Test وReality Lock.

---

## V1.2 Scenario Levels Contract Patch Lock — 20260708_003202

تم تنفيذ Patch مضبوط على ndsp-quality-live-nmp-wrapper لإضافة عقد scenario_levels إلى /api/decision/quality-live.

- V12_PATCH_SCENARIO_LEVELS_CONTRACT_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V12_PATCH_SCENARIO_LEVELS_CONTRACT_REMOTE_ONLY_20260708_003202.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V12_PATCH_SCENARIO_LEVELS_CONTRACT_REMOTE_ONLY_20260708_003202
- TARGET=backend/app/runtime/ndsp_quality_live_nmp_wrapper.py
- SERVICE=ndsp-quality-live-nmp-wrapper.service
- MODE=ROOT_REMOTE_SCRIPT

نتائج Post Patch Test:

- VALID_ALL=1
- ETHUSDT=OK
- BTCUSDT=OK
- XAUUSD=OK
- USOIL=OK
- top-level scenario_levels موجود
- V1 flat scenario fields محفوظة
- Nginx لم يتم تعديله
- Frontend لم يتم تعديله
- ndsp-quality-live-nmp-wrapper.service restarted
- PM2 ndsp-portal بقي online

Rule:
V1.2 Scenario Levels Contract معتمد. أي تعديل لاحق على عرض الواجهة أو أسماء الحقول يجب أن يكون Patch مستقل مع Backup وReport وPost Patch Test.

---

## V1.2 Frontend Display Verification Read-only Lock — 2026-07-08

تم تنفيذ فحص قراءة فقط للتأكد من عرض مستويات السيناريو في الواجهة بعد Patch V1.2.

- V12_FRONTEND_DISPLAY_VERIFICATION_STATUS=DONE
- REPORT=docs/05-runbooks/NDSP_V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_20260708_003607.md
- MODE=READ_ONLY_FRONTEND_DISPLAY_VERIFICATION
- MODIFICATIONS=None

نتائج API:

- API_CONTRACT_STATUS=OK
- ETHUSDT scenario_levels=OK
- BTCUSDT scenario_levels=OK
- XAUUSD scenario_levels=OK
- USOIL scenario_levels=OK

نتائج الواجهة:

- FRONTEND_MATCH_COUNT=27
- HAS_NEW_SCENARIO_LEVELS_CONTRACT_BINDING=0
- HAS_OLD_FLAT_SCENARIO_BINDING=1
- HAS_AR_LEVEL_LABELS=1
- FRONTEND_DISPLAY_BINDING_STATUS=LIKELY_PRESENT

الملفات التي تعرض المستويات حاليًا:

- /var/www/ndsp-my/assets/ndsp-radar-safe-clean.js
- /var/www/ndsp-my/assets/ndsp-decision-support-bind.js
- /var/www/ndsp-my/assets/ndsp-asset-view-live-bind.js

حالة الصفحات:

- /decision-support.html HTTP 200
- /NDSP_Asset_View.html HTTP 200
- /NDSP_Command_Center.html HTTP 200
- /NDSP_Daily_Brief.html HTTP 200
- /index.html HTTP 200

Runtime:

- ndsp-portal online
- PM2 restarts=0
- No frontend patch required at this stage

Decision:

V1.2 Scenario Levels is approved at API contract level and display-compatible through preserved V1 flat fields. A future cleanup may migrate frontend bindings to top-level scenario_levels, but it is not required for current V1.2 release safety.

Rule:
لا يتم تعديل الواجهة الآن. أي ترقية لاحقة لقراءة scenario_levels مباشرة يجب أن تكون Patch مستقل مع Backup وReport وPost Patch Test وReality Lock.

---

## V1.2 Release Package Lock — 20260708_004432

تم إنشاء حزمة إصدار V1.2 بعد نجاح Final Acceptance Audit.

- V12_RELEASE_PACKAGE_STATUS=CREATED
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz
- SHA256=/home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz.sha256
- REPORT=docs/05-runbooks/NDSP_V12_RELEASE_PACKAGE_REPORT_20260708_004432.md
- MODE=RELEASE_PACKAGE_CREATE
- MODIFICATIONS=Package files only; no runtime changes

Included:

- NDSP_CURRENT_REALITY_LOCK_AR.md
- NDSP_V12_PATCH_SCENARIO_LEVELS_CONTRACT_REMOTE_ONLY_20260708_003202.md
- NDSP_V12_FRONTEND_DISPLAY_VERIFICATION_READONLY_20260708_003607.md
- NDSP_V12_FINAL_ACCEPTANCE_AUDIT_20260708_004202.md
- backend/app/runtime/ndsp_quality_live_nmp_wrapper.py

Decision:
V1.2 Release Package is ready for download and external archive.

---

## P2 Monitoring & Startup Safety Audit Lock — 2026-07-08

تم تنفيذ فحص P2 قراءة فقط لحالة التشغيل والإقلاع والمراقبة.

- P2_MONITORING_STARTUP_SAFETY_AUDIT_STATUS=WITH_ALERTS
- REPORT=docs/05-runbooks/NDSP_P2_MONITORING_STARTUP_SAFETY_AUDIT_READONLY_20260708_005254.md
- MODE=READ_ONLY_MONITORING_STARTUP_SAFETY
- MODIFICATIONS=None

النتائج الجيدة:

- nginx active/enabled
- ndsp-quality-live-nmp-wrapper.service active/enabled
- ndsp-quality-live-golden-wrapper.service active/enabled
- ndsp-live-decision-quality.service active/enabled
- ndsp-scenario-levels-adapter.service active/enabled
- PM2 ndsp-portal online
- PM2_DUMP_EXISTS=1
- pm2-nawaf511.service enabled
- Public HTTP checks = 200
- V12_API_CONTRACT_STATUS=OK
- V1.2 release package exists
- V1.2 SHA matches server package

التنبيهات:

- يوجد 12 failed systemd units
- pm2-nawaf511.service enabled لكنه inactive/dead وقت الفحص
- nginx -t تم تشغيله بدون sudo وظهر permission denied على /run/nginx.pid
- certbot.service failed
- logrotate.service failed
- بعض الخدمات الفاشلة قد تكون قديمة أو خارج نطاق NDSP الحالي وتحتاج تصنيف

Decision:
لا يتم تنفيذ reboot أو startup fix أو حذف خدمات قبل P2 Alerts Resolver Read-only.

---

## P2 Root Diagnostics Read-only Lock — 2026-07-08

تم تنفيذ Root Diagnostics قراءة فقط لتشخيص تنبيهات P2.

- P2_ROOT_DIAGNOSTICS_STATUS=DONE_WITH_ACTIONS_REQUIRED
- REPORT=docs/05-runbooks/NDSP_P2_ROOT_DIAGNOSTICS_READONLY_20260708_010319.md
- MODE=ROOT_READ_ONLY_DIAGNOSTICS
- MODIFICATIONS=None

النتائج:

- nginx -t successful
- nginx active
- ndsp-quality-live-nmp-wrapper active
- API_HEALTH_HTTP=200
- QUALITY_LIVE_HTTP=200
- NDSP runtime critical health OK

التشخيص:

- Nginx لا يحتاج إصلاح الآن.
- Certbot failure مرتبط بشهادات nawafo.shop وليس بشهادات NDSP الأساسية الحالية.
- logrotate failed بسبب duplicate log entry for /var/log/nginx/nawafo_access.log.
- ndsp-real-feeds-sync و ndsp-tradingview-calendar يفشلان بسبب PermissionError داخل /var/www/ndsp-my/data.
- /var/www/ndsp-my/data مملوك root:root بصلاحية 755.
- real data timer services تعمل كمستخدم nawaf511.
- PM2 startup service enabled ونجح في resurrect عند boot، لكنه inactive بعد إيقاف PM2 لاحقًا؛ يحتاج تثبيت إدارة مستقل لاحقًا.

Action Order:

1. P2 Fix A: إصلاح صلاحيات /var/www/ndsp-my/data للـ real feeds.
2. P2 Fix B: إصلاح logrotate duplicate entry.
3. P2 Fix C: معالجة certbot للنطاقات القديمة nawafo.shop أو استبعادها إن كانت خارج نطاق NDSP.
4. P2 Fix D: تثبيت PM2 startup/save بشكل نظيف بعد التأكد من التطبيقات المطلوبة فقط.
5. تصنيف الخدمات القديمة قبل تعطيل أي خدمة.

Rule:
لا يتم reboot ولا تعطيل خدمات ولا تعديل Nginx. كل Fix يجب أن يكون مستقلًا مع Backup وReport وPost Fix Test وReality Lock.

---

## P2 Fix A Real Feeds Permissions Lock — 20260708_052909

تم تنفيذ إصلاح صلاحيات مضبوط لمجلد real feeds.

- P2_FIX_A_REAL_FEEDS_PERMISSIONS_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_A_REAL_FEEDS_PERMISSIONS_20260708_052909.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_A_REAL_FEEDS_PERMISSIONS_20260708_052909
- TARGET=/var/www/ndsp-my/data
- MODE=CONTROLLED_PERMISSION_FIX

التعديل:

- تم تغيير مالك /var/www/ndsp-my/data إلى nawaf511:nawaf511
- تم ضبط صلاحية المجلد إلى 775
- لم يتم تعديل Nginx
- لم يتم تعديل Frontend
- لم يتم تعديل API
- لم يتم تنفيذ reboot

نتائج الاختبار:

- WRITE_SMOKE_TEST=OK
- ndsp-real-feeds-sync.service start OK
- ndsp-tradingview-calendar.service start OK
- Critical API health OK
- quality-live OK
- ndsp-portal بقي online

Rule:
P2 Fix A معتمد. أي تعديل لاحق على real feeds أو data directory يجب أن يكون Patch مستقل مع Backup وReport وPost Fix Test.

---

## P2 Fix B2 Logrotate Duplicate Lock — 20260708_054419

تم تنفيذ إصلاح B2 لتعارض logrotate duplicate entry.

- P2_FIX_B2_LOGROTATE_DUPLICATE_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_B2_LOGROTATE_MOVE_DISABLED_OUT_20260708_054419
- MODE=CONTROLLED_LOGROTATE_FIX_B2

سبب الإصلاح:

- P2 Fix B الأول نقل /etc/logrotate.d/nawafo إلى اسم يحتوي disabled، لكنه بقي داخل /etc/logrotate.d وتمت قراءته كملف إعداد.
- logrotate استمر في إظهار duplicate log entry for /var/log/nginx/nawafo_access.log.

التعديل:

- تم نقل ملفات nawafo* التي تحتوي تعريف nawafo nginx logs خارج /etc/logrotate.d إلى مجلد Backup.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

نتائج الاختبار:

- logrotate debug test OK
- logrotate.service start OK
- duplicate log entry لم يعد موجودًا
- nginx active
- nginx -t successful
- API health OK
- quality-live OK
- ndsp-portal بقي online

Rule:
P2 Fix B2 معتمد. أي تعديل لاحق على logrotate يجب أن يكون Patch مستقل مع Backup وReport وPost Fix Test.

---

## P2 Fix C Disable Old Nawafo Renewals Lock — 20260708_060441

تم تنفيذ إصلاح مضبوط لنطاق Certbot renewal scope.

- P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_C_DISABLE_OLD_NAWAFO_RENEWALS_20260708_060441
- MODE=CONTROLLED_CERTBOT_RENEWAL_SCOPE_FIX

سبب الإصلاح:

- certbot.service كان يفشل بسبب شهادات nawafo.shop القديمة:
  - api.nawafo.shop
  - dashboard.nawafo.shop
  - nawafo.shop
- نطاقات NDSP الأساسية سليمة وصالحة.
- Nginx النشط لا يعتمد على شهادات nawafo.shop في تشغيل NDSP الحالي.

التعديل:

- تم نقل renewal configs القديمة الخاصة بـ nawafo.shop خارج /etc/letsencrypt/renewal إلى Backup.
- لم يتم حذف أي شهادة.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

نتائج الاختبار:

- certbot renew --dry-run OK للـ renewal set المتبقي.
- certbot.timer active.
- nginx active.
- nginx -t successful.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- ndsp-portal بقي online.

Rule:
P2 Fix C معتمد. أي رجوع لاستخدام nawafo.shop لاحقًا يجب أن يتم كمسار مستقل بإعداد DNS/Nginx/Certbot واضح.

---

## P2 Fix D3 PM2 Oneshot Bootstrap Lock — 20260708_061553

تم تنفيذ إصلاح مضبوط لخدمة PM2 startup باستخدام oneshot bootstrap بدل Type=forking/PIDFile.

- P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061553.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_D3_PM2_ONESHOT_BOOTSTRAP_20260708_061553
- MODE=CONTROLLED_PM2_SYSTEMD_ONESHOT_BOOTSTRAP_FIX

سبب D3:

- P2 Fix D2 أثبت أن pm2-nawaf511.service يفشل مع Type=forking/PIDFile بسبب protocol/PIDFile ownership.
- ndsp-portal كان online، لكن systemd service كان failed.
- تم اعتماد oneshot + RemainAfterExit لتشغيل pm2 resurrect عند الإقلاع بدون الاعتماد على PIDFile.

التعديل:

- تم حفظ PM2 dump قبل التعديل.
- تم أخذ Backup من pm2-nawaf511.service السابق.
- تم تحويل pm2-nawaf511.service إلى Type=oneshot مع RemainAfterExit=yes.
- تم تنفيذ pm2 save --force كمستخدم nawaf511.
- تم enable/start لخدمة pm2-nawaf511.service.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

نتائج الاختبار:

- pm2-nawaf511.service enabled.
- pm2-nawaf511.service active.
- ndsp-portal online.
- nginx active.
- nginx -t successful.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.

Rule:
P2 Fix D3 معتمد. أي تغيير لاحق على PM2/systemd startup يجب أن يكون Patch مستقل مع Backup وReport وPost Fix Test.

---

## P2 Fix E Disable Legacy Failed Services Lock — 20260708_063422

تم تنفيذ تعطيل مضبوط للخدمات القديمة الفاشلة التي لا تحتوي مراجع مشروع أو Nginx.

- P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_E_DISABLE_LEGACY_FAILED_SERVICES_20260708_063422
- MODE=CONTROLLED_DISABLE_LEGACY_FAILED_SERVICES

الخدمات التي تم تعطيلها:

- fanno-comments.service
- marketpulse.service
- redis-replica.service
- redis-sentinel.service

الخدمات التي لم يتم لمسها:

- ndip-api-new.service
- signal-engine.service
- subscription-watcher.service
- testapp.service

التعديل:

- تم أخذ Backup من ملفات الوحدات المستهدفة.
- تم تنفيذ systemctl disable للخدمات الأربع فقط.
- تم تنفيذ systemctl reset-failed للخدمات الأربع فقط.
- لم يتم حذف أي unit file.
- لم يتم mask لأي خدمة.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

نتائج الاختبار:

- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.

Rule:
P2 Fix E معتمد. أي تعطيل إضافي للخدمات المتبقية يحتاج Patch مستقل بعد مراجعة مراجع المشروع.

---

## P2 Final Health + Release Package Lock — 20260708_064314

تم تنفيذ فحص P2 النهائي وإنشاء حزمة P2.

- P2_FINAL_HEALTH_STATUS=OK
- P2_RELEASE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_P2_FINAL_HEALTH_AUDIT_20260708_064314.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_RELEASE_PACKAGE_20260708_064314.tar.gz.sha256

نتائج الفحص:

- Reality Lock يحتوي مفاتيح Fix A/B2/C/D3/E.
- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- logrotate debug OK.
- Certbot renewal scope نظيف من nawafo configs.
- تم إنشاء حزمة P2 الرسمية.

Rule:
P2 مقفول تشغيليًا. أي تعامل مع الخدمات المتبقية للمراجعة يجب أن يكون Patch مستقل بعد تحليل مراجع المشروع.

---

## P2 Fix F Disable Two Hold-Review Legacy Services Lock — 20260708_220447

تم تنفيذ تعطيل مضبوط لخدمتين من خدمات Hold Review بعد Deep Audit وDecision Matrix.

- P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_F_DISABLE_TWO_HOLD_REVIEW_LEGACY_20260708_220447
- MODE=CONTROLLED_DISABLE_TWO_HOLD_REVIEW_LEGACY_SERVICES

الخدمات التي تم تعطيلها:

- signal-engine.service
- subscription-watcher.service

الخدمات التي لم يتم لمسها:

- ndip-api-new.service
- testapp.service

سبب التعديل:

- signal-engine.service بلا مراجع مشروع وبلا مراجع Nginx.
- subscription-watcher.service بلا مراجع مشروع وبلا مراجع Nginx.
- ndip-api-new.service لديه مراجع مشروع ويحتاج مراجعة مستقلة.
- testapp.service لديه مراجع مشروع كثيرة ويحتاج مراجعة مستقلة.

التعديل:

- تم أخذ Backup من ملفات الوحدات المستهدفة.
- تم تنفيذ systemctl disable للخدمتين فقط.
- تم تنفيذ systemctl reset-failed للخدمتين فقط.
- لم يتم حذف أي unit file.
- لم يتم mask لأي خدمة.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

نتائج الاختبار:

- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.

Rule:
أي تعامل مع ndip-api-new.service أو testapp.service يجب أن يكون Patch مستقل بعد مراجعة مراجع المشروع.

---

## P2 Fix G testapp Disable + ndip reset-failed Lock — 20260708_222645

تم تنفيذ Patch مضبوط بعد D3 Strict Separation Audit.

- P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P2_FIX_G_TESTAPP_DISABLE_NDIP_RESET_FAILED_20260708_222645
- MODE=CONTROLLED_TESTAPP_DISABLE_NDIP_RESET_FAILED

الإجراءات:

- تم تعطيل testapp.service فقط.
- تم تنفيذ reset-failed لـ testapp.service.
- تم تنفيذ reset-failed لـ ndip-api-new.service فقط بدون start/restart/enable.
- لم يتم حذف أي unit file.
- لم يتم mask لأي خدمة.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تنفيذ reboot.

سبب القرار:

- testapp.service لا يملك active Nginx refs.
- testapp.service لا يملك port 8521 listening.
- testapp.service لديه مسارات ناقصة: /srv/testapp/app.py و /srv/testapp/venv/bin/streamlit.
- ndip-api-new.service مرتبط بمراجعة mapping لأن Nginx يستخدم 9001 وPort 9001 listening عبر Node gateway، لذلك لم يتم تعطيله أو تشغيله؛ فقط تنظيف failed state.

نتائج الاختبار:

- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- systemctl --failed أصبح نظيفًا أو بدون الخدمات المعالجة.

Rule:
أي إعادة تصميم لعلاقة ndip-api-new.service مع platform gateway 9001 يجب أن يكون Patch مستقل، ولا يتم start/enable لها بدون خريطة خدمة واضحة.

---

## P2 Post-G Final Clean Audit + Release Package Lock — 20260708_223115

تم تنفيذ فحص P2 النهائي بعد Fix G وإنشاء حزمة Release محدثة.

- P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK
- P2_POST_G_FINAL_RELEASE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_P2_POST_G_FINAL_CLEAN_AUDIT_20260708_223115.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223115.tar.gz.sha256

نتائج الفحص:

- Reality Lock يحتوي Fix A/B2/C/D3/E/F/G.
- systemctl --failed count = 0.
- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- testapp.service disabled/inactive/inactive.
- ndip-api-new.service disabled/inactive/inactive بعد reset-failed فقط.
- logrotate debug OK.
- تم إنشاء حزمة P2 النهائية بعد Fix G.

Rule:
P2 مغلق نهائيًا بعد Fix G. أي إعادة تصميم لعلاقة ndip-api-new.service مع platform gateway 9001 يجب أن تكون Patch مستقل مع خريطة خدمة واضحة.

---

## P2 Post-G Final Clean Audit + Release Package Lock — 20260708_223425

تم تنفيذ فحص P2 النهائي بعد Fix G وإنشاء حزمة Release محدثة.

- P2_POST_G_FINAL_CLEAN_HEALTH_STATUS=OK
- P2_POST_G_FINAL_RELEASE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_P2_POST_G_FINAL_CLEAN_AUDIT_20260708_223425.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223425.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P2_POST_G_FINAL_RELEASE_PACKAGE_20260708_223425.tar.gz.sha256

نتائج الفحص:

- Reality Lock يحتوي Fix A/B2/C/D3/E/F/G.
- systemctl --failed count = 0.
- nginx active.
- nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- testapp.service disabled/inactive/inactive.
- ndip-api-new.service disabled/inactive/inactive بعد reset-failed فقط.
- logrotate debug OK.
- تم إنشاء حزمة P2 النهائية بعد Fix G.

Rule:
P2 مغلق نهائيًا بعد Fix G. أي إعادة تصميم لعلاقة ndip-api-new.service مع platform gateway 9001 يجب أن تكون Patch مستقل مع خريطة خدمة واضحة.

---

## P3 Boot Readiness Audit Lock — 20260708_224326

تم تنفيذ فحص جاهزية الإقلاع قبل أي reboot.

- P3_BOOT_READINESS_STATUS=READY_FOR_CONTROLLED_REBOOT_DRILL
- REPORT=docs/05-runbooks/NDSP_P3_BOOT_READINESS_AUDIT_READONLY_20260708_224326.md
- MODE=READ_ONLY
- NO_REBOOT=1
- NO_RUNTIME_MODIFICATION=1

نتائج الفحص:

- Reality Lock يحتوي إغلاق P2 Post-G Final.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- ndsp-portal online.
- PM2 dump موجود.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- legacy disabled services نظيفة.
- port 9001 listening.
- logrotate debug OK.
- certbot renewal scope OK.
- data dir ownership OK.
- disk usage acceptable.

Rule:
يجوز الانتقال إلى Controlled Reboot Drill بمستند مستقل فقط. لا يتم تنفيذ reboot عشوائي.

---

## P3 Controlled Reboot Drill Preflight Lock — 20260708_224943

تم تنفيذ Preflight لإعادة تشغيل مضبوطة.

- P3_CONTROLLED_REBOOT_PREFLIGHT_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P3_CONTROLLED_REBOOT_DRILL_PREFLIGHT_20260708_224943.md
- MARKER=docs/05-runbooks/NDSP_P3_CONTROLLED_REBOOT_MARKER_20260708_224943.env
- WILL_REBOOT=1

نتائج ما قبل reboot:

- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- PM2 dump موجود ومحدث.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- الخدمات المعطلة بقيت غير فاشلة.

Rule:
بعد عودة السيرفر يجب تنفيذ P3 Post-Reboot Verification قبل أي تعديل آخر.

---

## P3 Fix I Contain ndip Loop + Stabilize Market Updater Lock — 20260708_230607

تم تنفيذ Patch مضبوط بعد H.

- P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_230607.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_230607

الإجراءات:

- تم إضافة drop-in لخدمة ndsp-market-prices-updater.service لانتظار postgresql.service و network-online.target قبل التنفيذ.
- لم يتم تعطيل ndsp-market-prices-updater.timer.
- تم إضافة drop-in لخدمة ndip-api-new.service يجعل Restart=no لأنها disabled وlegacy mapping تحت المراجعة.
- تم إيقاف وتعطيل reverse dependency services المرتبطة بـ ndip-api-new:
  - ndip-health-monitor.service
  - ndip-telegram-decision-worker.service
- تم إيقاف ndip-api-new.service وتنظيف failed state.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تعديل PM2.
- لم يتم حذف أو mask لأي خدمة.
- لم يتم reboot.

نتائج الاختبار:

- systemctl --failed = 0.
- ndip-api-new.service لم يعد في activating/auto-restart.
- ndsp-market-prices-updater.timer بقي active.
- ndsp-market-prices-updater.service غير failed.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.

Rule:
أي إعادة تفعيل مستقبلية لـ ndip-api-new.service أو reverse dependency services يجب أن تكون Patch مستقل بعد إصلاح import path وخريطة خدمة واضحة.

---

## P3 Fix I Contain ndip Loop + Stabilize Market Updater Lock — 20260708_231351

تم تنفيذ Patch مضبوط بعد H.

- P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_P3_FIX_I_CONTAIN_NDIP_LOOP_AND_STABILIZE_MARKET_UPDATER_20260708_231351

الإجراءات:

- تم إضافة drop-in لخدمة ndsp-market-prices-updater.service لانتظار postgresql.service و network-online.target قبل التنفيذ.
- لم يتم تعطيل ndsp-market-prices-updater.timer.
- تم إضافة drop-in لخدمة ndip-api-new.service يجعل Restart=no لأنها disabled وlegacy mapping تحت المراجعة.
- تم إيقاف وتعطيل reverse dependency services المرتبطة بـ ndip-api-new:
  - ndip-health-monitor.service
  - ndip-telegram-decision-worker.service
- تم إيقاف ndip-api-new.service وتنظيف failed state.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل Frontend.
- لم يتم تعديل PM2.
- لم يتم حذف أو mask لأي خدمة.
- لم يتم reboot.

نتائج الاختبار:

- systemctl --failed = 0.
- ndip-api-new.service لم يعد في activating/auto-restart.
- ndsp-market-prices-updater.timer بقي active.
- ndsp-market-prices-updater.service غير failed.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.

Rule:
أي إعادة تفعيل مستقبلية لـ ndip-api-new.service أو reverse dependency services يجب أن تكون Patch مستقل بعد إصلاح import path وخريطة خدمة واضحة.

---

## P3 Reboot After Fix I Preflight Lock — 20260708_232114

تم تنفيذ Preflight بعد Fix I لإعادة تشغيل مضبوطة.

- P3_REBOOT_AFTER_FIX_I_PREFLIGHT_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P3_REBOOT_AFTER_FIX_I_PREFLIGHT_20260708_232114.md
- MARKER=docs/05-runbooks/NDSP_P3_REBOOT_AFTER_FIX_I_MARKER_20260708_232114.env
- WILL_REBOOT=1

نتائج ما قبل reboot:

- systemctl --failed = 0.
- ndip-api-new.service inactive وليس activating.
- ndip-api-new Restart=no.
- ndsp-market-prices-updater.timer active.
- ndsp-market-prices-updater.service غير failed.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- PM2 dump تم تحديثه.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.

Rule:
بعد عودة السيرفر يجب تنفيذ P3 Post-Reboot After Fix I Verification قبل أي تعديل آخر.

---

## P3 Controlled Reboot After Fix I Lock — 20260708_232520

تم تنفيذ فحص ما بعد reboot بعد Fix I بنجاح.

- P3_CONTROLLED_REBOOT_AFTER_FIX_I_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_P3_POST_REBOOT_AFTER_FIX_I_VERIFICATION_20260708_232520.md
- MODE=POST_REBOOT_VERIFICATION
- NO_RUNTIME_MODIFICATION=1

نتائج ما بعد reboot:

- systemctl --failed = 0.
- ndip-api-new.service inactive وليس activating.
- ndip-api-new Restart=no.
- ndip reverse dependency services بقيت inactive.
- ndsp-market-prices-updater.timer active.
- ndsp-market-prices-updater.service غير failed.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- port 9001 listening.

Rule:
P3 Controlled Reboot بعد Fix I ناجح. يجوز الانتقال إلى P3 Final Release Package.

---

## P3 Final Clean Audit + Release Package Lock — 20260708_233209

تم تنفيذ فحص P3 النهائي وإنشاء حزمة الإصدار النهائية.

- P3_FINAL_CLEAN_HEALTH_STATUS=OK
- P3_FINAL_RELEASE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_P3_FINAL_CLEAN_AUDIT_20260708_233209.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_P3_FINAL_RELEASE_PACKAGE_20260708_233209.tar.gz.sha256

نتائج الفحص:

- Reality Lock يحتوي إغلاق P2 Post-G Final.
- Reality Lock يحتوي P3 Boot Readiness.
- Reality Lock يحتوي Fix I.
- Reality Lock يحتوي Controlled Reboot After Fix I.
- systemctl --failed = 0.
- ndip-api-new.service inactive وليس activating.
- ndip-api-new Restart=no.
- ndsp-market-prices-updater.timer active.
- ndsp-market-prices-updater.service غير failed.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- ndsp-portal online.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- port 9001 listening.
- logrotate debug OK.
- nawafo renewal configs absent.
- تم إنشاء حزمة P3 النهائية مع sha256.

Rule:
P3 مغلق نهائيًا. أي عمل لاحق يجب أن يكون V1.3 أو P4 بخطة مستقلة وBackup وReport وPost Patch Test.

---

## V1.3 Scope Freeze + Implementation Plan Lock — 20260708_235303

تم إنشاء مستندات تجميد نطاق V1.3 وخطة التنفيذ بدون أي تعديل Runtime.

- V13_SCOPE_FREEZE_STATUS=CREATED
- V13_IMPLEMENTATION_PLAN_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_V13_SCOPE_FREEZE_AND_PLAN_DOCS_ONLY_20260708_235303.md
- SCOPE_AR=docs/05-runbooks/NDSP_V13_SCOPE_FREEZE_AR_20260708_235303.md
- SCOPE_EN=docs/05-runbooks/NDSP_V13_SCOPE_FREEZE_EN_20260708_235303.md
- PLAN=docs/05-runbooks/NDSP_V13_IMPLEMENTATION_PLAN_20260708_235303.md
- BASELINE=docs/05-runbooks/NDSP_V13_PLANNING_BASELINE_AUDIT_READONLY_20260708_234638.md

Rule:
لا يتم تنفيذ أي Patch في V1.3 قبل الالتزام بملفات Scope Freeze وخطة التنفيذ.

---

## V1.3-A Release Evidence Page Lock — 20260709_000110

تم تنفيذ Patch V13-A بنجاح.

- V13_A_RELEASE_EVIDENCE_PAGE_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_A_RELEASE_EVIDENCE_PAGE_20260709_000110.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_A_RELEASE_EVIDENCE_PAGE_20260709_000110
- PAGE=/var/www/ndsp-my/release-evidence.html
- JSON=/var/www/ndsp-my/data/release-evidence.json

الإجراءات:

- تم إنشاء صفحة release-evidence.html للقراءة فقط.
- تم إنشاء data/release-evidence.json للقراءة فقط.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.

نتائج الاختبار:

- release-evidence.html HTTP 200.
- release-evidence.json HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- Governance scan للملفات الجديدة OK.

Rule:
أي توسيع لاحق لصفحة الأدلة يجب أن يبقى read-only ولا يتحول إلى لوحة تحكم تشغيلية.

---

## V1.3-B Data Freshness and Trust Panel Lock — 20260709_001015

تم تنفيذ Patch V13-B بنجاح.

- V13_B_DATA_FRESHNESS_TRUST_PANEL_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_B_DATA_FRESHNESS_TRUST_PANEL_20260709_001015.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_B_DATA_FRESHNESS_TRUST_PANEL_20260709_001015
- PAGE=/var/www/ndsp-my/data-freshness.html
- JSON=/var/www/ndsp-my/data/data-freshness-panel.json

الإجراءات:

- تم إنشاء صفحة data-freshness.html للقراءة فقط.
- تم إنشاء data/data-freshness-panel.json للقراءة فقط.
- تم عرض عمر ملفات البيانات وصحة JSON والملكية.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.
- لا يتم تزوير حداثة البيانات.
- stale data يظهر للمستخدم بدل إخفائه.

نتائج الاختبار:

- data-freshness.html HTTP 200.
- data-freshness-panel.json HTTP 200.
- release-evidence.html بقي HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- Governance scan للملفات الجديدة OK.

Rule:
أي تطوير لاحق للوحة الثقة يجب أن يبقى read-only ولا يتحول إلى مصدر توصية أو ضمان دقة مالي.

---

## V1.3-B1 D2 Safe Ownership Stabilizer Lock — 20260709_003057

تم تنفيذ Patch V13-B1 D2 بنجاح بعد فشل B1 عند محاولة تشغيل market updater يدويًا.

- V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_B1_D2_SAFE_OWNERSHIP_STABILIZER_NO_UPDATER_RUN_20260709_003057
- TARGET=/var/www/ndsp-my/data/command-center-real.json
- DROPIN=/etc/systemd/system/ndsp-market-prices-updater.service.d/50-ndsp-v13-command-center-owner.conf

الإجراءات:

- تم أخذ Backup من command-center-real.json.
- تم أخذ Backup من drop-in الجزئي إن وجد.
- تم استبدال drop-in بصيغة best-effort لا تجعل الخدمة تفشل إذا تعذر chown/chmod.
- تم تصحيح ملكية command-center-real.json الحالي مباشرة إلى nawaf511:nawaf511.
- تم تنفيذ daemon-reload.
- تم تنظيف failed state لخدمة ndsp-market-prices-updater.service إن وجدت.
- لم يتم تشغيل ndsp-market-prices-updater.service يدويًا.
- تم إعادة توليد data-freshness-panel.json.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لم يتم تعديل الملفات المحمية.

نتائج الاختبار:

- command-center-real.json أصبح nawaf511:nawaf511.
- ownership_warnings=0 في لوحة حداثة البيانات.
- data-freshness.html HTTP 200.
- data-freshness-panel.json HTTP 200.
- release-evidence.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-market-prices-updater.timer active.
- Governance scan OK.

Rule:
لا يتم تشغيل market updater يدويًا داخل Patch واجهة إلا إذا كان ذلك جزءًا من Patch خدمة مستقل. تصحيح الملكية مستقبلاً يبقى best-effort ولا يسبب فشل الخدمة.

---

## V1.3-B2 Data Freshness Stabilization Audit Lock — 20260709_003752

تم تنفيذ فحص استقرار بعد V13-B1 D2 بنجاح.

- V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_B2_DATA_FRESHNESS_STABILIZATION_AUDIT_READONLY_20260709_003752.md
- MODE=READ_ONLY

نتائج الفحص:

- systemctl --failed = 0.
- ndsp-market-prices-updater.service ليس failed ولا activating بعد الانتظار.
- ndsp-market-prices-updater.timer active.
- command-center-real.json ملكيته nawaf511:nawaf511.
- ownership_warnings=0.
- read_errors=0.
- data-freshness.html HTTP 200.
- data-freshness-panel.json HTTP 200.
- release-evidence.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- protected assets checksums unchanged.

Rule:
يجوز الانتقال إلى V13-C Decision Room UX Copy Cleanup بعد هذا الفحص.

---

## V1.3-C Decision Room UX Copy Guide Lock — 20260709_004632

تم تنفيذ Patch V13-C بنجاح.

- V13_C_DECISION_ROOM_UX_COPY_GUIDE_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_C_DECISION_ROOM_UX_COPY_GUIDE_20260709_004632.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_C_DECISION_ROOM_UX_COPY_GUIDE_20260709_004632
- PAGE=/var/www/ndsp-my/decision-room-guide.html
- JSON=/var/www/ndsp-my/data/decision-room-copy.json

الإجراءات:

- تم إنشاء صفحة decision-room-guide.html للقراءة فقط.
- تم إنشاء data/decision-room-copy.json للقراءة فقط.
- تم توضيح حالات القراءة ومفهوم القوة مقابل الجاهزية.
- لم يتم تعديل منطق TDL/NMP/Golden/Risk/Devil.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.
- لم يتم تعديل الملفات المحمية.

نتائج الاختبار:

- decision-room-guide.html HTTP 200.
- decision-room-copy.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- data-freshness-panel.json HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.

Rule:
أي تعديل لاحق على نصوص غرفة القرار يجب أن يبقى تفسيريًا ولا يغير محركات القرار أو يحول NDSP إلى نظام تنفيذ.

---

## V1.3-D Completed Decisions Viewer Hardening Lock — 20260709_005409

تم تنفيذ Patch V13-D بنجاح.

- V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_20260709_005409.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_20260709_005409
- PAGE=/var/www/ndsp-my/completed-decisions-review.html
- JSON=/var/www/ndsp-my/data/completed-decisions-viewer-config.json

الإجراءات:

- تم إنشاء صفحة completed-decisions-review.html للقراءة فقط.
- تم إنشاء data/completed-decisions-viewer-config.json للقراءة فقط.
- تم إضافة فلاتر محلية للأصل والحالة والجودة.
- تم عرض readiness/strength/why_not_completed/levels عند توفرها.
- تم توفير empty/error states عند عدم توفر endpoint للمتصفح.
- لم يتم تعديل completed decisions API.
- لم يتم تعديل DB schema.
- لم يتم تعديل Nginx.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.
- لم يتم تعديل الملفات المحمية.

نتائج الاختبار:

- completed-decisions-review.html HTTP 200.
- completed-decisions-viewer-config.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- decision-room-guide.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.

Rule:
أي تطوير لاحق لعارض القرارات المكتملة يجب أن يبقى read-only ولا يضيف أزرار تشغيل أو يغير API/DB بدون خطة مستقلة.

---

## V1.3-C Decision Room UX Copy Guide Lock — 20260709_013021

تم تنفيذ Patch V13-C بنجاح.

- V13_C_DECISION_ROOM_UX_COPY_GUIDE_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_C_DECISION_ROOM_UX_COPY_GUIDE_20260709_013021.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_C_DECISION_ROOM_UX_COPY_GUIDE_20260709_013021
- PAGE=/var/www/ndsp-my/decision-room-guide.html
- JSON=/var/www/ndsp-my/data/decision-room-copy.json

الإجراءات:

- تم إنشاء صفحة decision-room-guide.html للقراءة فقط.
- تم إنشاء data/decision-room-copy.json للقراءة فقط.
- تم توضيح حالات القراءة ومفهوم القوة مقابل الجاهزية.
- لم يتم تعديل منطق TDL/NMP/Golden/Risk/Devil.
- لم يتم تعديل Nginx.
- لم يتم تعديل API.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.
- لم يتم تعديل الملفات المحمية.

نتائج الاختبار:

- decision-room-guide.html HTTP 200.
- decision-room-copy.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- data-freshness-panel.json HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.

Rule:
أي تعديل لاحق على نصوص غرفة القرار يجب أن يبقى تفسيريًا ولا يغير محركات القرار أو يحول NDSP إلى نظام تنفيذ.

---

## V1.3-D Completed Decisions Viewer Hardening Lock — 20260709_013406

تم تنفيذ Patch V13-D بنجاح.

- V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_20260709_013406.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_D_COMPLETED_DECISIONS_VIEWER_HARDENING_20260709_013406
- PAGE=/var/www/ndsp-my/completed-decisions-review.html
- JSON=/var/www/ndsp-my/data/completed-decisions-viewer-config.json

الإجراءات:

- تم إنشاء صفحة completed-decisions-review.html للقراءة فقط.
- تم إنشاء data/completed-decisions-viewer-config.json للقراءة فقط.
- تم إضافة فلاتر محلية للأصل والحالة والجودة.
- تم عرض readiness/strength/why_not_completed/levels عند توفرها.
- تم توفير empty/error states عند عدم توفر endpoint للمتصفح.
- لم يتم تعديل completed decisions API.
- لم يتم تعديل DB schema.
- لم يتم تعديل Nginx.
- لم يتم تعديل PM2.
- لم يتم تنفيذ build.
- لم يتم تنفيذ reboot.
- لا توجد أزرار تحكم بالخدمات.
- لا يوجد shell من المتصفح.
- لم يتم تعديل الملفات المحمية.

نتائج الاختبار:

- completed-decisions-review.html HTTP 200.
- completed-decisions-viewer-config.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- decision-room-guide.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.

Rule:
أي تطوير لاحق لعارض القرارات المكتملة يجب أن يبقى read-only ولا يضيف أزرار تشغيل أو يغير API/DB بدون خطة مستقلة.

---

## V1.3-E D2 Visual Polish Hub + Link Integrity Finalizer Lock — 20260709_033000

تم تنفيذ Finalizer بعد توقف V13-E عند grep/no-match مع pipefail.

- V13_E_D2_FINALIZER_STATUS=OK
- V13_E_VISUAL_POLISH_HUB_AND_LINK_INTEGRITY_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_E_D2_FINALIZE_AFTER_SAFE_GREP_EXIT_20260709_033000.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_E_D2_FINALIZE_AFTER_SAFE_GREP_EXIT_20260709_033000
- PAGE=/var/www/ndsp-my/v13-experience.html
- JSON=/var/www/ndsp-my/data/v13-experience-hub.json

سبب D2:

- Patch V13-E الأصلي أنشأ الصفحة والـ JSON ونجحت روابطه.
- توقف قبل Final Evaluation لأن grep لم يجد global scripts، وهذا يرجع exit status 1.
- في هذا السياق عدم وجود matches هو النتيجة المطلوبة، وليس فشلًا تشغيليًا.

نتائج D2:

- v13-experience.html HTTP 200.
- v13-experience-hub.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- decision-room-guide.html HTTP 200.
- completed-decisions-review.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.
- لا يوجد global script stacking في الصفحة الجديدة.

Rule:
يجوز الانتقال إلى V1.3 Final Audit + Release Package بعد D2.

---

## V1.3-E D2 Visual Polish Hub + Link Integrity Finalizer Lock — 20260709_033345

تم تنفيذ Finalizer بعد توقف V13-E عند grep/no-match مع pipefail.

- V13_E_D2_FINALIZER_STATUS=OK
- V13_E_VISUAL_POLISH_HUB_AND_LINK_INTEGRITY_STATUS=OK
- REPORT=docs/05-runbooks/NDSP_V13_E_D2_FINALIZE_AFTER_SAFE_GREP_EXIT_20260709_033345.md
- BACKUP_DIR=/home/nawaf511/ndsp_backups/NDSP_V13_E_D2_FINALIZE_AFTER_SAFE_GREP_EXIT_20260709_033345
- PAGE=/var/www/ndsp-my/v13-experience.html
- JSON=/var/www/ndsp-my/data/v13-experience-hub.json

سبب D2:

- Patch V13-E الأصلي أنشأ الصفحة والـ JSON ونجحت روابطه.
- توقف قبل Final Evaluation لأن grep لم يجد global scripts، وهذا يرجع exit status 1.
- في هذا السياق عدم وجود matches هو النتيجة المطلوبة، وليس فشلًا تشغيليًا.

نتائج D2:

- v13-experience.html HTTP 200.
- v13-experience-hub.json HTTP 200.
- release-evidence.html HTTP 200.
- data-freshness.html HTTP 200.
- decision-room-guide.html HTTP 200.
- completed-decisions-review.html HTTP 200.
- API health OK.
- quality-live OK.
- my.ndsp.app OK.
- admin.ndsp.app OK.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- ndsp-market-prices-updater.timer active.
- Governance scan للملفات الجديدة OK.
- لا يوجد global script stacking في الصفحة الجديدة.

Rule:
يجوز الانتقال إلى V1.3 Final Audit + Release Package بعد D2.

---

## V1.3 Final D5 Audit + Release Package Lock — 20260709_080303

- V13_FINAL_D5_CLEAN_HEALTH_STATUS=OK
- V13_FINAL_RELEASE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_V13_FINAL_D5_CANONICAL_ROOT_WRITER_POLICY_AND_REPACKAGE_20260709_080303.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D5_RELEASE_PACKAGE_20260709_080303.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D5_RELEASE_PACKAGE_20260709_080303.tar.gz.sha256

D5 decision:
command-center-real.json is accepted as root:root with mode 0644 because it is generated by a root-owned writer and served as read-only static JSON.

V1.3 مغلق نهائيًا على حزمة D5. الحزم السابقة CREATED_OR_PARTIAL لا تستخدم كمرجع إغلاق.
أي عمل لاحق يجب أن يكون V1.4 أو P4 بخطة مستقلة وBackup وReport وPost Patch Test.

---

## V1.3 Final D5 Lock Reconciled by V14-D0 — 20260709_082445

تمت إعادة تثبيت قفل V1.3 D5 في Reality Lock بناءً على أدلة الحزمة والتحقق الحالي.

- V13_FINAL_D5_CLEAN_HEALTH_STATUS=OK
- V13_FINAL_RELEASE_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V13_FINAL_D5_AUDIT_AND_PACKAGE_OK
- RECONCILED_BY=V14_D0
- D5_PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D5_RELEASE_PACKAGE_20260709_080303.tar.gz
- D5_SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V13_FINAL_D5_RELEASE_PACKAGE_20260709_080303.tar.gz.sha256
- D5_SHA256=8adf2bfce727797de7e466b97ba4566fc4c031ac7d7b3593f33198360cbdbbcb
- D5_REPORT=docs/05-runbooks/NDSP_V13_FINAL_D5_CANONICAL_ROOT_WRITER_POLICY_AND_REPACKAGE_20260709_080303.md

سبب reconcile:

- V14 kickoff السابق توقف لأن مفاتيح D5 غير موجودة في Reality Lock.
- الحزمة D5 موجودة على السيرفر.
- SHA256 مطابق.
- runtime الحالي نظيف.
- endpoints الأساسية و V1.3 pages تعمل.

Rule:
V1.3 مغلق على D5. أي عمل جديد يكون V1.4 أو P4 فقط.

---

## V1.4 D0-D2 Kickoff Lock — 20260709_083510

تم إغلاق D0-D2 وفتح V1.4/P4 بشكل صحيح.

- V14_D0_RECONCILE_D5_LOCK_STATUS=OK
- V14_D0_GOVERNANCE_FALSE_POSITIVE_FINALIZER_STATUS=OK
- V14_D0_KICKOFF_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V14_D0_RECONCILE_D5_LOCK_AND_KICKOFF_OK
- REPORT=docs/05-runbooks/NDSP_V14_D0_D2_GOVERNANCE_FALSE_POSITIVE_FINALIZER_20260709_083510.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_D0_D2_KICKOFF_PACKAGE_20260709_083510.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_D0_D2_KICKOFF_PACKAGE_20260709_083510.tar.gz.sha256

قرار D2:

- تنبيه D0 كان false positive.
- السبب: scan قرأ raw discovery baseline وليس user-facing copy.
- controlled docs scan نظيف.
- V1.3 يبقى مغلق على D5.

Rule:
الخطوة التالية فقط: V14-A Completed Decisions Source Discovery READ ONLY.
لا يتم تعديل Nginx/API/PM2 قبل V14-A.

---

## V1.4-A D2 Completed Decisions Source Discovery Lock — 20260709_084807

تم تنفيذ V14-A D2 كفحص قراءة فقط سريع ومحدود بزمن.

- V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_STATUS=OK
- V14_A_D2_EVIDENCE_PACKAGE_STATUS=CREATED
- REPORT=docs/05-runbooks/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_READONLY_FAST_20260709_084807.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_FAST_20260709_084807.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_A_D2_COMPLETED_DECISIONS_SOURCE_DISCOVERY_FAST_20260709_084807.tar.gz.sha256

Findings:

- PUBLIC_COMPLETED_DECISIONS_200_COUNT=0
- LOCAL_COMPLETED_DECISIONS_200_COUNT=0
- NGINX_COMPLETED_DECISIONS_REFS=123
- PROJECT_COMPLETED_DECISIONS_REFS=400
- FILE_COMPLETED_DECISIONS_CANDIDATES=12
- DATA_STORE_CANDIDATES=34
- DISCOVERY_RECOMMENDATION=STATIC_OR_FILE_ADAPTER_CANDIDATE
- NEXT_PATCH_RECOMMENDATION=V14-B_STATIC_JSON_ADAPTER_AFTER_MANUAL_REVIEW

Rule:
لا يتم تنفيذ V14-B قبل مراجعة V14-A D2 Decision Matrix.

---

## V1.4 BCDE-D2 Static Completion + Final Package Lock — 20260709_090710

تم إغلاق المتبقي من V1.4 بعد reconcile لقفل V14-A D2.

- V14_A_D2_LOCK_RECONCILE_STATUS=OK
- V14_B_STATIC_COMPLETED_DECISIONS_ADAPTER_STATUS=OK
- V14_C_PORTAL_HUB_STATUS=OK
- V14_D_EMPTY_ERROR_STATE_POLISH_STATUS=OK
- V14_E_FINAL_AUDIT_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V14_BCDE_D2_STATIC_COMPLETION_FINAL_PACKAGE_OK
- REPORT=docs/05-runbooks/NDSP_V14_BCDE_D2_RECONCILE_A_D2_LOCK_AND_FINAL_PACKAGE_20260709_090710.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V14_BCDE_D2_FINAL_PACKAGE_20260709_090710.tar.gz.sha256

ما تم:

- إنشاء completed-decisions-v14.html للقراءة فقط.
- إنشاء data/completed-decisions-v14-adapter.json.
- إنشاء v14-experience.html.
- إنشاء data/v14-experience.json.
- إنشاء data/v14-error-states.json.
- إنشاء v14-final-evidence.html.
- إنشاء data/v14-final-evidence.json.
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- protected assets unchanged.
- Governance scan لملفات V1.4 الجديدة OK.
- لا يوجد global script stacking.
- تم إنشاء حزمة V1.4 النهائية D2.

Rule:
V1.4 مغلق على هذا المسار الثابت. أي ربط live/API لاحق يكون V1.5 أو P5 بخطة مستقلة.

---

## V1.5 / P5 D2 Read-only API Bridge Final Lock — 20260709_094155

تم إغلاق V1.5/P5 D2 بعد تصحيح Nginx target.

- V15_P5_D2_READONLY_PUBLIC_API_BRIDGE_STATUS=OK
- V15_P5_D2_NGINX_API_ROUTE_STATUS=OK
- V15_P5_D2_FINAL_AUDIT_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V15_P5_D2_READONLY_API_BRIDGE_FINAL_PACKAGE_OK
- REPORT=docs/05-runbooks/NDSP_V15_P5_D2_FIX_API_BRIDGE_NGINX_TARGET_FINAL_PACKAGE_20260709_094155.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V15_P5_D2_API_BRIDGE_FINAL_PACKAGE_20260709_094155.tar.gz.sha256

ما تم:

- تصحيح Nginx target للـ api.ndsp.app.
- تشغيل endpoints:
  - /api/completed-decisions
  - /api/completed-decisions/latest
  - /api/v15/completed-decisions
- systemctl --failed = 0.
- nginx active و nginx -t successful.
- pm2-nawaf511 active/enabled.
- protected assets unchanged.
- Governance scan OK.
- no global script stacking.
- تم إنشاء حزمة V1.5/P5 D2 النهائية.

Rule:
هذا endpoint قراءة فقط ومبني على V1.4 static adapter. أي live DB/backend adapter حقيقي لاحق يكون V1.6/P6 بخطة مستقلة.

---

## V1.6 / P6 One-Shot Live Read-only Adapter Final Lock — 20260709_101523

تم إغلاق V1.6/P6 بعد إثبات مصدر قراءة حي/ملفي.

- V16_P6_LIVE_READONLY_ADAPTER_STATUS=OK
- V16_P6_NGINX_LIVE_ROUTE_STATUS=OK
- V16_P6_FINAL_AUDIT_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_OK
- REPORT=docs/05-runbooks/NDSP_V16_P6_ONE_SHOT_LIVE_READONLY_ADAPTER_FINAL_PACKAGE_20260709_101523.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_P6_ONE_SHOT_LIVE_ADAPTER_FINAL_PACKAGE_20260709_101523.tar.gz.sha256

المسارات:
- /api/v16/completed-decisions
- /api/completed-decisions-live
- /api/completed-decisions-live/latest

Rule:
هذا adapter قراءة فقط. أي live write/DB schema/engine integration لاحق يكون V1.7/P7 بخطة مستقلة.

---

## V1.6-F / P6-F Architecture Map Static Page Lock — 20260709_115257

تم نشر خريطة NDSP المعمارية كصفحة Static بديلة عن Figma.

- V16_F_ARCHITECTURE_MAP_STATIC_PAGE_STATUS=OK
- V16_F_ARCHITECTURE_MAP_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V16_F_ARCHITECTURE_MAP_STATIC_PAGE_OK
- REPORT=docs/05-runbooks/NDSP_V16_F_ARCHITECTURE_MAP_STATIC_PAGE_20260709_115257.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V16_F_ARCHITECTURE_MAP_PACKAGE_20260709_115257.tar.gz.sha256

الملفات:
- /architecture-map.html
- /assets/ndsp-v16-architecture-map.svg
- /data/ndsp-architecture-map.json

Rule:
هذه صفحة توثيقية فقط. لا تغير runtime ولا API ولا محركات القرار.

---

## V1.7 / P7 Release Registry + Launch Readiness Final Lock — 20260709_121842

تم إغلاق P7 كمرحلة سجل الإصدارات وجاهزية الإطلاق الداخلية.

- V17_P7_RELEASE_REGISTRY_STATUS=OK
- V17_P7_LAUNCH_READINESS_CENTER_STATUS=OK
- V17_P7_FINAL_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_OK
- REPORT=docs/05-runbooks/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_20260709_121842.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V17_P7_RELEASE_REGISTRY_LAUNCH_READINESS_FINAL_PACKAGE_20260709_121842.tar.gz.sha256

الصفحات:
- /launch-readiness.html
- /release-registry.html

البيانات:
- /data/launch-readiness.json
- /data/release-registry.json

الحالة:
- systemctl --failed = 0
- nginx active و nginx -t successful
- pm2-nawaf511 active/enabled
- endpoints المهمة HTTP 200
- package SHA mismatch = 0
- governance scan OK
- no global script stacking
- protected assets unchanged

Rule:
P7 يغلق الجاهزية الداخلية. ما بعده ليس تعديل محركات أو صفحات أساسية؛ ما بعده launch operations: UAT, monitoring, payments/subscriptions, legal/disclaimer final review, support runbooks.

---

## V1.8 / P8-D3 Golden Visual Skin Preview Lock — 20260709_132128

تم نشر Preview معزول للتصميم الذهبي بعد إصلاح مسار التقرير.

- V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_STATUS=OK
- V18_P8_PREVIEW_URL=https://my.ndsp.app/v18-golden-preview/
- V18_P8_D3_FINAL_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_OK
- REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_132128.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D3_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_132128.tar.gz.sha256

ما تم:
- تحويل الهوية اللونية من السيان/الأزرق إلى ذهب NDSP الفخم.
- تنظيف مظهر radial/radar visual.
- نشر preview فقط في /v18-golden-preview/.
- عدم لمس الإنتاج أو Nginx أو API أو PM2 أو DB أو assets المحمية.

Rule:
هذا Preview فقط. لا يتم اعتماده على واجهة الإنتاج إلا بعد مراجعة بصرية يدوية وموافقة صريحة.

---

## V1.8 / P8-D5 Adopt Golden Design To Production Links Lock — 20260709_140821

تم اعتماد التصميم الذهبي على روابط الإنتاج المحددة.

- V18_P8_D5_PRODUCTION_LINKS_ADOPTION_STATUS=OK
- V18_P8_D5_PRODUCTION_ASSETS_STATUS=OK
- V18_P8_D5_AUTH_PAGES_EXCLUDED_STATUS=OK
- V18_P8_D5_ROLLBACK_STATUS=AVAILABLE
- V18_P8_D5_FINAL_PACKAGE_STATUS=CREATED
- FINAL_STATUS=V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_OK
- REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821.md
- PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz
- SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_PACKAGE_20260709_140821.tar.gz.sha256
- ROLLBACK=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D5_ADOPT_GOLDEN_DESIGN_TO_PRODUCTION_LINKS_20260709_140821/ROLLBACK_V18_P8_D5.sh

ما تم:
- نشر assets التصميم الجديد في /v18-production/.
- ربط صفحات الإنتاج القديمة بنسخة التصميم الذهبي.
- إضافة route aliases حتى لا تظهر 404 داخل React.
- إضافة عربي/English والعربية default.
- عدم لمس login/register/reset/forgot/admin.
- عدم لمس Nginx أو API أو PM2 أو DB أو assets المحمية.

Rule:
أي رجوع يتم فقط عبر rollback الموثق أعلاه.

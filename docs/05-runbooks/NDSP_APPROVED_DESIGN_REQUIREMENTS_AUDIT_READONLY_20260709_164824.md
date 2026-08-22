# NDSP — Approved Design Requirements Audit READ-ONLY

DATE=2026-07-09T16:48:24+02:00
MODE=READ_ONLY_REQUIREMENTS_AUDIT
LIVE=/var/www/ndsp-my
SRC_ZIP=/tmp/ndsp_approved_design_requirements_audit_source.zip
NO_HTML_CHANGE=1
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_DB_CHANGE=1
NO_SERVICE_CONTROL=1
NO_BUILD=1
NO_DELETE=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_20260709_164824.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz

## 1) Runtime reference only
FAILED_UNITS_COUNT=0
NGINX_ACTIVE=active
PM2_ACTIVE=active
PM2_ENABLED=enabled
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
2026/07/09 16:48:24 [warn] 4168047#4168047: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
2026/07/09 16:48:24 [warn] 4168047#4168047: conflicting server name "my.ndsp.app" on 0.0.0.0:80, ignored
2026/07/09 16:48:24 [warn] 4168047#4168047: conflicting server name "my.ndsp.app" on [::]:80, ignored
2026/07/09 16:48:24 [warn] 4168047#4168047: conflicting server name "my.ndsp.app" on 0.0.0.0:443, ignored
2026/07/09 16:48:24 [warn] 4168047#4168047: conflicting server name "my.ndsp.app" on [::]:443, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
2026/07/09 16:48:24 [emerg] 4168047#4168047: open() "/run/nginx.pid" failed (13: Permission denied)
nginx: configuration file /etc/nginx/nginx.conf test failed

## 2) Source extraction
SOURCE_AVAILABLE=0
SOURCE_WARNING=ZIP_NOT_PROVIDED

## 3) Route and page map audit

| ID | Requirement | Status | Source hits | Live hits / HTTP | Action |
|---|---|---:|---:|---:|---|
| P01 | صفحة الهبوط / Home | OK | 0 | 200 | READ_ONLY |
| P02 | صفحة الأسواق والأصول | OK | 0 | 200 | READ_ONLY |
| P03 | قائمة الأسواق كلها | OK | 0 | 200 | READ_ONLY |
| P04 | رادار القرار | OK | 0 | 200 | READ_ONLY |
| P05 | دعم/شرح القرار | OK | 0 | 200 | READ_ONLY |
| P06 | NMP / نقطة التقاء نواف | OK | 0 | 200 | READ_ONLY |
| P07 | دليل قراءة القرار | OK | 0 | 200 | READ_ONLY |
| P08 | القرارات المكتملة | OK | 0 | 200 | READ_ONLY |
| P09 | مركز القيادة / التسلسل العام | OK | 0 | 200 | READ_ONLY |
| P10 | الإعدادات والتنبيهات | OK | 0 | 200 | READ_ONLY |
| P11 | جاهزية الإطلاق | OK | 0 | 200 | READ_ONLY |
| P12 | سجل الإصدارات | OK | 0 | 200 | READ_ONLY |
| A01 | صفحة التسجيل | OK | 0 | 200 | READ_ONLY |
| A02 | صفحة الدخول | OK | 0 | 200 | READ_ONLY |
| A03 | استعادة/إعادة تعيين كلمة المرور | OK | 0 | 200 | READ_ONLY |
| A04 | صفحة الإدارة | OK | 0 | 200 | READ_ONLY |

## 4) Feature and content audit

| ID | Requirement | Status | Source hits | Live hits | Action |
|---|---|---:|---:|---:|---|
| F01 | رادار اكتمال وحدات القرار | OK | 0 | 892 | يجب أن يظهر كمؤشر اكتمال/جاهزية وليس إشارة دخول |
| F02 | المستويات المرجعية | OK | 0 | 153 | إظهارها كمستويات مرجعية: تفعيل/وصول/مراجعة/إلغاء |
| F03 | NMP / نقطة التقاء نواف | OK | 0 | 103 | يبقى ظاهرًا كطبقة قراءة عامة |
| F04 | السيناريوهات البديلة | OK | 0 | 186 | للبسيط: سيناريو حاكم فقط + بدائل مطوية. للمحترف: جدول احتمالات |
| F05 | شرح القرار للمستخدم البسيط | OK | 0 | 9 | لازم لغة مختصرة: ماذا يعني؟ لماذا؟ متى تتغير القراءة؟ |
| F06 | شرح القرار للمستخدم المحترف | OK | 0 | 298 | يعرض التفاصيل والطبقات والمساهمة |
| F07 | أنماط القراءة: استثماري/مضاربي | OK | 0 | 119 | تسمى أنماط قراءة لا أنماط تداول |
| F08 | دليل قراءة القرار | OK | 0 | 77 | صفحة أو قسم يشرح الرموز والحالات |
| F09 | كل الأسواق وكل الأصول | OK | 0 | 862 | تأكيد وجود تغطية الأسواق الأساسية |
| F10 | تسلسل الأقسام حتى القسم الأخير | OK | 0 | 275 | التسلسل يجب يكون ثابت في القائمة |
| F11 | القرارات المكتملة | OK | 0 | 87 | يجب تكون صفحة/قسم قراءة مكتملة وليس تنفيذ |
| F12 | محامي الشيطان / المخاطر | OK | 0 | 139 | لازم قبل التأكيد النهائي |
| F13 | USD / Macro filter | OK | 0 | 173 | مهم للقراءة الكلية |
| F14 | Data freshness / وقت التحديث | OK | 0 | 170 | مهم للثقة وعدم تضليل المستخدم |
| F15 | إخلاء مسؤولية / ليس توصية | OK | 0 | 72 | لازم ظاهر أو gate قبل الاستخدام |
| F16 | Golden Signal كحالة متابعة لا أمر | OK | 0 | 20 | لا تظهر كأمر شراء/بيع |
| F17 | الخصوصية: لا أسرار أو مفاتيح | OK | 0 | 11 | أي ظهور يحتاج مراجعة. التقرير لا يعرض القيم |
| F18 | تنظيف أسماء المزودين الداخلية | OK | 0 | 28 | يجب أن تكون صفر في الواجهة العامة |

## 5) Approved design marker and current live marker
APPROVED_MARKER_LIVE_HITS=0
STABLE_SHELL_LIVE_HITS=37
OLD_DESIGN_LIVE_DIRS_COUNT=2
AUTH_ADMIN_APPROVED_MARKER_HITS=0
AUTH_ADMIN_DESIGN_STATUS=WARN_EXISTS_BUT_NOT_ALL_APPROVED_DESIGN

## 6) Source route files and high-value files
SOURCE_FILES_INDEX=SKIPPED_NO_SOURCE

## 7) Opinion on alternative scenarios
RECOMMENDATION_ALTERNATIVE_SCENARIOS:
- لا تعرض السيناريوهات البديلة للمستخدم البسيط كخيارات متساوية.
- واجهة البسيط تعرض: السيناريو الحاكم + سبب مختصر + مستوى الإلغاء/المراجعة.
- البدائل تكون مطوية تحت: "ما الذي قد يغير القراءة؟"
- واجهة المحترف تعرض البدائل كجدول احتمالات: حاكم / بديل / شرط التحول / أثره على الجاهزية.
- لا تستخدم عبارة "مستويات بديلة" في الواجهة العامة؛ استخدم "مستويات مرجعية" و"شرط مراجعة السيناريو".

## 8) Missing items to remember
CHECKLIST_EXTRA_ITEMS:
- بوابة إخلاء المسؤولية قبل دخول البوابة.
- Beginner default + Advanced toggle.
- Risk Radar legend.
- USD/Macro panel قبل Devil's Advocate.
- Data freshness / آخر تحديث / UTC.
- Completed Reading Seal / Under Monitoring Seal / Caution Seal.
- صفحة الدعم أو مركز المساعدة.
- سجل التنبيهات.
- صفحة تجربة الجوال ومقاسات iPhone.
- عدم ظهور أي Buy/Sell أو LONG/SHORT في الواجهة العامة.
- عدم ظهور أسماء المزودين أو مصادر البيانات الداخلية.

## 9) Final read-only package
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz.sha256
e84b10fd2c9eb6d963df0e96ab28ac7c4665f55350be1281e07f3667852c053d  /home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz

## 10) Final status
READ_ONLY_AUDIT_STATUS=OK
DESIGN_FILES_CHANGED=0
NGINX_CHANGED=0
API_CHANGED=0
PM2_RESTARTED=0
DB_CHANGED=0
FINAL_STATUS=NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_OK
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_20260709_164824.md
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz
SHA256_FILE=/home/nawaf511/ndsp_release_packages/NDSP_APPROVED_DESIGN_REQUIREMENTS_AUDIT_READONLY_PACKAGE_20260709_164824.tar.gz.sha256

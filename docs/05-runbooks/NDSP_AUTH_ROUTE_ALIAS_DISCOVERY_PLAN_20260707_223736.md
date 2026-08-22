# NDSP Auth Route Alias Discovery + Plan
DATE=2026-07-07T22:37:36+02:00
MODE=DISCOVERY_AND_PLANNING_ONLY
MODIFICATIONS=None
LIVE=/var/www/ndsp-my
FRONTEND_BASE=https://my.ndsp.app

## 1) Current HTTP Status
[404] https://my.ndsp.app/login
[200] https://my.ndsp.app/login.html
[404] https://my.ndsp.app/register
[200] https://my.ndsp.app/register.html
[404] https://my.ndsp.app/forgot-password
[200] https://my.ndsp.app/forgot-password.html
[404] https://my.ndsp.app/reset-password
[200] https://my.ndsp.app/reset-password.html
[200] https://my.ndsp.app/password-reset
[200] https://my.ndsp.app/password-reset.html

## 2) Live Auth-related Files

## 3) Live Auth-related Directories

## 4) Auth Links Found in HTML

## 5) Safe Route Alias Plan
الهدف:
- جعل /login يفتح login.html بدون تغيير Nginx
- جعل /register يفتح register.html بدون تغيير Nginx
- فحص صفحات forgot/reset قبل أي إنشاء أو تعديل

الخطة الآمنة المقترحة:
1. إذا كان login.html موجودًا، يتم إنشاء /login/index.html كنسخة آمنة أو تحويل HTML داخلي.
2. إذا كان register.html موجودًا، يتم إنشاء /register/index.html كنسخة آمنة أو تحويل HTML داخلي.
3. لا يتم إنشاء forgot/reset إلا بعد التأكد هل توجد ملفات HTML أصلية لها.
4. لا يتم لمس API أو PM2 أو Nginx أو Backend.
5. أي Patch لاحق يجب أن يكون Static Route Alias فقط مع Backup و Patch Report و Post Patch Test.

غير مسموح بدون موافقة:
- Nginx rewrite changes
- PM2 restart
- API changes
- Backend changes
- Auth backend behavior changes
- تغيير صفحات Priority 1 الداخلية المكتملة

## 6) Recommendation
ابدأ بإصلاح /login و /register فقط لأن ملفات login.html و register.html تعمل HTTP 200.
اجعل forgot-password/reset-password مرحلة منفصلة بعد اكتشاف الملفات أو تحديد المسار الصحيح.

FINAL_STATUS=AUTH_ROUTE_ALIAS_DISCOVERY_PLAN_CREATED
REPORT=docs/05-runbooks/NDSP_AUTH_ROUTE_ALIAS_DISCOVERY_PLAN_20260707_223736.md

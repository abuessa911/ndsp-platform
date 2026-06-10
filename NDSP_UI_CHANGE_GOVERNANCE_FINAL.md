# NDSP UI Change Governance — حوكمة تعديلات الواجهة

المشروع: NDSP — منصة نواف لدعم القرار  
الحالة: Final / إلزامي  
النطاق: صفحات الموقع العام، بوابة المستخدم، لوحة الإدارة، JavaScript، Nginx، النشر، والرجوع الآمن.

---

## 1) سبب السياسة

تم اعتماد هذه السياسة بعد تكرار كسر واجهات NDSP بسبب:
- حقن JavaScript داخل صفحات حساسة.
- تعديل عدة ملفات دفعة واحدة.
- اختيار مكان العرض تلقائيًا داخل Layout.
- تعديل مسارات غير نشطة أو نسخ احتياطية.
- التعامل مع /var/www كمصدر كود.
- ظهور بيانات Demo في الإنتاج.

الخطأ لم يكن من قاعدة البيانات، بل من أسلوب تعديل الواجهة.

---

## 2) القاعدة الذهبية

أي تعديل UI يجب أن يمر بهذا التسلسل:

تشخيص Read-only  
تحديد المصدر النشط  
نسخة احتياطية  
تعديل محدود  
اختبار  
تحقق بصري ومنطقي  
نشر تدريجي  
اعتماد  

يمنع التعديل المباشر على الإنتاج بدون هذه الخطوات.

---

## 3) ممنوعات صارمة

يمنع التالي:
- حقن JavaScript عام داخل صفحات حساسة.
- تعديل أكثر من ملف HTML بدون ضرورة.
- تعديل /var/www كمصدر كود.
- استخدام grep/replace واسع على كامل المشروع.
- إضافة أزرار حذف أو تعديل بدون API محمي.
- عرض مستخدمين Demo في الإنتاج.
- تعديل ملفات داخل /etc/nginx/backup_* إلا للقراءة فقط.

---

## 4) المصدر النشط

قبل تعديل أي صفحة يجب تحديد المسار النشط من Nginx:

sudo nginx -T | grep -nE "server_name|root|alias|admin.ndsp.app|ndsp.app|my.ndsp.app"

المصادر المعتمدة:
- /home/nawaf511/empire-core-new/apps/public-landing
- /home/nawaf511/empire-core-new/apps/public-site
- /home/nawaf511/empire-core-new/apps/user-portal
- /home/nawaf511/empire-core-new/apps/admin-console

المسار /var/www يعتبر مخرجات نشر فقط وليس مصدر تعديل.

---

## 5) الميزات الجديدة

أي ميزة UI جديدة تبدأ كصفحة مستقلة أولًا.

أمثلة:
- NDSP_Admin_Users_Official.html
- NDSP_Admin_System_Health.html
- NDSP_Admin_User_Actions_Test.html

لا يتم دمجها داخل لوحة الإدارة الرئيسية إلا بعد ثباتها واختبارها.

---

## 6) سياسة JavaScript

أي سكربت واجهة يجب أن يركب داخل Anchor واضح فقط، مثل:

<div id="ndsp-safe-mount"></div>

إذا لم يجد السكربت هذا العنصر، يجب أن يتوقف ولا يحقن نفسه داخل body أو أول div.

ممنوع استخدام منطق عشوائي مثل:

document.querySelector("section") || document.body

---

## 7) إدارة المستخدمين

المصدر الرسمي للمستخدمين:

PostgreSQL / ndsp_auth / public.users

يمنع عرض مستخدمين وهميين في الإنتاج مثل:
- Sara Al-Q
- Faisal R
- Noura S
- Khalid M

أزرار إدارة المستخدمين لا يتم تفعيلها إلا بعد وجود API رسمي محمي يشمل:
- صلاحية صاحب النظام فقط.
- منع حذف آخر Admin.
- منع حذف المستخدم الحالي.
- Audit log.
- Backup قبل العمليات الحساسة.
- عدم كشف الأسرار.

---

## 8) النسخ الاحتياطي والتقارير

أي سكربت تعديل يجب أن ينشئ:
- BACKUP_DIR
- REPORT

ويجب أن يحتوي التقرير على:
- FINAL_STATUS
- FAIL_COUNT
- WARN_COUNT
- BACKUP_DIR
- OPEN_THIS_URL

إذا كان FAIL_COUNT أكبر من صفر، فالتعديل غير معتمد.

---

## 9) اختبار الواجهة

بعد أي تعديل UI يجب التحقق من:
- HTTP_CODE=200
- NGINX_CONFIG_OK=True
- الخدمات الأساسية Active
- عدم وجود Demo data
- عدم وجود سكربتات مكسورة
- عدم وجود أسرار في الملفات العامة
- عدم كسر Layout

---

## 10) Green Gate قبل الإطلاق

لا يعتمد أي تعديل واجهة قبل تحقق التالي:
- FAIL_COUNT=0
- NGINX_CONFIG_OK=True
- SERVICE_ACTIVE=nginx.service
- SERVICE_ACTIVE=ndsp-api.service
- SERVICE_ACTIVE=ndsp-auth-api.service
- HTTP_CODE=200
- STRICT_SECRET_LEAK=False
- DEMO_DATA_VISIBLE=False
- LAYOUT_BROKEN=False

---

## 11) Rollback

كل تعديل يجب أن يكون قابلًا للرجوع.

مثال:
rsync -a /home/nawaf511/ndsp_backups/<backup>/admin-console/ /home/nawaf511/empire-core-new/apps/admin-console/
sudo nginx -t && sudo systemctl reload nginx

---

## 12) القرار الملزم

من الآن في NDSP:
- لا حقن عام.
- لا تعديل واسع.
- لا Demo في الإنتاج.
- لا تعديل /var/www كمصدر.
- لا أزرار خطرة بدون API محمي.
- لا إطلاق بدون Green Gate.
- أي ميزة جديدة تبدأ مستقلة.
- أي تعديل يجب أن يكون محدودًا وقابلًا للرجوع.

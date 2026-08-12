# حزمة النسخ الاحتياطي والاستعادة لـ NDSP — الإصدار V1

## الأساس الذي بُنيت عليه الحزمة

بُنيت هذه الحزمة من تقرير **Backup Readiness Preflight** بتاريخ 11 يوليو 2026، وبصمة الحزمة المصدرية:

```text
4076f964a0fb2f2459b8e23e28e62be3e37aab2e107bff22cbcc0dee407268b1
```

الواقع المثبت يشمل:

- المشروع الحاكم: `/home/nawaf511/empire-core-new` بحجم تقريبي 2.4GB.
- مساحة حرة كانت قرابة 154GB وقت الفحص.
- PostgreSQL محلي 16/main على 5432، ومن قواعده `ndsp_auth`.
- PostgreSQL داخل Docker باسم `ndip_postgres` على 5433.
- Redis محلي على 6379.
- PM2 يشغل `ndsp-portal`.
- Nginx صالح وقت الفحص.
- عشرات خدمات systemd وملفات EnvironmentFile موزعة بين `/etc/ndsp` والمشروع.
- Git worktree غير نظيف ويحتوي تعديلات وملفات غير متتبعة؛ لذلك النسخة تلتقط الشجرة الفعلية ولا تعتمد على Git وحده.

## الملفات

- `ndsp_create_backup_passphrase_v1.sh`: ينشئ ملف عبارة مرور بصلاحية 600.
- `ndsp_backup_runtime_precheck_v1.sh`: يتحقق من أدوات وبيئة النسخ دون إنشاء نسخة.
- `ndsp_full_backup_v1.sh`: ينشئ نسخة كاملة مشفرة.
- `ndsp_backup_verify_v1.sh`: يتحقق من فك التشفير والبصمات والأرشيفات وقواعد البيانات.
- `ndsp_restore_drill_v1.sh`: اختبار استعادة غير مدمر، ويمكنه استعادة PostgreSQL داخل حاوية مؤقتة.
- `NDSP_BACKUP_SCOPE_V1.json`: نطاق النسخة والحقائق التي بُنيت عليها.

## مكونات النسخة

1. شجرة المشروع كاملة، بما فيها `.git` والتعديلات غير الملتزم بها وملفات البيئة الموجودة داخلها.
2. مجلدات التشغيل المنزلية وPM2.
3. التطبيقات الحية تحت `/opt` و`/var/www`.
4. Nginx وsystemd وبيئات NDSP وPostgreSQL وRedis وCron وLet’s Encrypt.
5. نسخ PostgreSQL المنطقية بصيغة Custom Format، مع Globals.
6. نسخ SQLite المتسقة عبر Online Backup API.
7. لقطة Redis بصيغة RDB.
8. Docker metadata والـvolumes غير النشطة الخاصة بـNDSP/NDIP/Empire.
9. حالة الخدمات والمنافذ والحزم وPM2 وDocker.
10. بصمات SHA-256 داخلية وخارجية.

## الأمان

- النسخة تحتوي أسرارًا، لذلك لا تُنتج بصيغة نهائية غير مشفرة.
- التشفير: GPG symmetric AES-256.
- ملف عبارة المرور لا يدخل النسخة.
- يجب حفظ عبارة المرور خارج السيرفر. فقدانها يعني فقدان القدرة على الاستعادة.
- النسخ لا يعيد تشغيل الخدمات ولا يغير Nginx ولا يقصد أي كتابة في قواعد الإنتاج.

## التشغيل

### 1. إنشاء عبارة المرور

```bash
bash scripts/backup/ndsp_create_backup_passphrase_v1.sh
```

المسار الافتراضي:

```text
/home/nawaf511/.config/ndsp-backup/backup-passphrase.txt
```

### 2. فحص التشغيل قبل النسخ

```bash
bash scripts/backup/ndsp_backup_runtime_precheck_v1.sh \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"
```

الحالة المطلوبة:

```text
FINAL_STATUS=NDSP_BACKUP_RUNTIME_PRECHECK_OK
```

### 3. إنشاء النسخة

```bash
bash scripts/backup/ndsp_full_backup_v1.sh \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"
```

الحالة المطلوبة:

```text
FINAL_STATUS=NDSP_FULL_BACKUP_ENCRYPTED_READY
```

### 4. التحقق

```bash
bash scripts/restore/ndsp_backup_verify_v1.sh \
  --archive /home/nawaf511/ndsp_full_backups_v2/NDSP_FULL_BACKUP_<HOST>_<TS>.tar.gpg \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"
```

### 5. اختبار الاستعادة

```bash
bash scripts/restore/ndsp_restore_drill_v1.sh \
  --archive /home/nawaf511/ndsp_full_backups_v2/NDSP_FULL_BACKUP_<HOST>_<TS>.tar.gpg \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt" \
  --keep
```

الحالة المطلوبة:

```text
FINAL_STATUS=NDSP_RESTORE_DRILL_OK
```

## سياسة الاستعادة الإنتاجية

لا تنفذ الحزمة استعادة تلقائية فوق الإنتاج. بعد نجاح الاختبار، تُكتب خطة استعادة إنتاجية مرتبطة بمعرف النسخة، وتتضمن:

1. نافذة صيانة معلنة.
2. نسخة Rollback جديدة قبل الاستعادة.
3. إيقاف الخدمات المحددة فقط.
4. استعادة الملفات إلى مسارات مؤقتة أولًا ومقارنتها.
5. استعادة قواعد البيانات بأسماء مؤقتة والتحقق منها.
6. Cutover صريح بموافقة المالك.
7. اختبارات Nginx وsystemd وPM2 وواجهات Health.
8. رجوع فوري عند فشل أي بوابة.

**الحالة:** `NDSP_BACKUP_RESTORE_PACK_V1_READY`

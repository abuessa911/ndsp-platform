#!/bin/bash

# --- إعدادات البيئة المدارة لـ NDSP ---
ENV_FILE="/etc/ndsp/ndsp-db.env"
REDIS_HOST="127.0.0.1"
REDIS_PORT="6379"

echo "========================================"
echo "  NDSP Data Normalization & Cleanup Tools"
echo "========================================"

# 1. التحقق من صلاحيات الـ sudo لقراءة ملف البيئة المركزي
if [ "$EUID" -ne 0 ]; then
    echo "[!] تنبيه: يفضل تشغيل السكربت باستخدام sudo لجلب إعدادات قاعدة البيانات المحمية تلقائياً."
    echo "مثال: sudo ./normalize_and_clean.sh"
    echo "----------------------------------------"
fi

# 2. قراءة متغيرات قاعدة البيانات ديناميكياً من المسار المعتمد
if [ -f "$ENV_FILE" ]; then
    echo "[*] جاري تحميل إعدادات قاعدة البيانات من المسار المركزي..."
    # استخراج القيم مع إزالة علامات الاقتباس إن وجدت
    DB_NAME=$(grep -E "^DB_NAME=" $ENV_FILE | cut -d'=' -f2 | tr -d '"'\')
    DB_USER=$(grep -E "^DB_USER=" $ENV_FILE | cut -d'=' -f2 | tr -d '"'\')
    export PGPASSWORD=$(grep -E "^DB_PASSWORD=" $ENV_FILE | cut -d'=' -f2 | tr -d '"'\')
    
    # في حال لم تكن المتغيرات مسبوقة بـ DB_NAME واستخدمت صيغة أخرى
    [ -z "$DB_NAME" ] && DB_NAME=$(grep -E "^DB_DATABASE=" $ENV_FILE | cut -d'=' -f2 | tr -d '"'\')
    [ -z "$DB_USER" ] && DB_USER=$(grep -E "^DB_USERNAME=" $ENV_FILE | cut -d'=' -f2 | tr -d '"'\')
else
    # قيم احتياطية بناءً على ملف الـ .env الخاص بالمشروع
    DB_NAME="ndsp_auth"
    DB_USER="ndsp_auth"
    echo "[!] لم يتم العثور على الملف المركزي، تم استخدام القيم الافتراضية للمشروع."
fi

# التأكد من ملء المتغيرات الأساسية
DB_NAME=${DB_NAME:-"ndsp_auth"}
DB_USER=${DB_USER:-"ndsp_auth"}

# 3. استقبال رقم الجوال من المستخدم
read -p "الرجاء إدخال رقم الجوال المراد تنظيفه وتوحيده: " INPUT_PHONE

if [ -z "$INPUT_PHONE" ]; then
    echo "[-] خطأ: لم يتم إدخال رقم جوال."
    exit 1
fi

# 4. معالجة وتوحيد صيغة الرقم (Normalization) إلى E.164
CLEANED=$(echo "$INPUT_PHONE" | tr -d '[:space:]()+-')

if [[ $CLEANED =~ ^05[0-9]{8}$ ]]; then
    FINAL_PHONE="+966${CLEANED:1}"
elif [[ $CLEANED =~ ^5[0-9]{8}$ ]]; then
    FINAL_PHONE="+966${CLEANED}"
elif [[ $CLEANED =~ ^966[0-9]{9}$ ]]; then
    FINAL_PHONE="+${CLEANED}"
else
    FINAL_PHONE="+${CLEANED}"
fi

echo "[+] الصيغة الموحدة المعتمدة في النظام: $FINAL_PHONE"
echo "----------------------------------------"

# 5. تنظيف الكاش في Redis
echo "[*] جاري البحث عن مفاتيح التحقق في Redis..."
REDIS_KEYS=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT KEYS "*${CLEANED}*")

if [ -z "$REDIS_KEYS" ]; then
    echo "[i] لا توجد مفاتيح معلقة لهذا الرقم في Redis."
else
    echo "[!] تم العثور على المفاتيح التالية في Redis وحذفها:"
    echo "$REDIS_KEYS"
    echo "$REDIS_KEYS" | xargs redis-cli -h $REDIS_HOST -p $REDIS_PORT DEL > /dev/null
    echo "[+] تم تنظيف كاش الـ OTP بنجاح."
fi

echo "----------------------------------------"

# 6. تنظيف وحذف السجل من قاعدة البيانات (PostgreSQL)
echo "[*] جاري فحص وحذف السجلات المتعارضة في PostgreSQL..."
echo "[*] الاتصال بقاعدة البيانات: $DB_NAME عبر المستخدم: $DB_USER"

psql -h 127.0.0.1 -U $DB_USER -d $DB_NAME -c "DELETE FROM users WHERE phone = '$FINAL_PHONE';"

if [ $? -eq 0 ]; then
    echo "[+] تم تنظيف مسار الجداول بنجاح، الرقم متاح للتسجيل الآن كمستخدم جديد."
else
    echo "[-] فشل تنظيف قاعدة البيانات. يرجى التحقق من صحة كلمة المرور أو تشغيل السكربت بـ sudo."
fi

echo "========================================"

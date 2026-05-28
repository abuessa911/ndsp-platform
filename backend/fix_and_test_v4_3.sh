#!/usr/bin/env bash

==============================================================================

NDSP V4.3 - Final Macro Logic Repair & Verification

الغرض: تصحيح أخطاء التسمية وتشغيل الاختبارات الفعلية لمحرك الماكرو.

==============================================================================

set -e

1. تعريف المسارات المرجعية بناءً على هيكلة NDSP V4.1

BACKEND_DIR="/home/nawaf511/empire-core-new/backend"
MACRO_DIR="$BACKEND_DIR/app/core/macro"

echo "------------------------------------------------------------"
echo "🚀 جاري بدء عملية الإصلاح والتحقق (NDSP V4.3)..."
echo "------------------------------------------------------------"

[خطوة 1]: تصحيح ملفات الحزم (المهمة الحرجة)

<comment-tag: "تم تصحيح init.py إلى init.py لضمان عمل الـ Module Mapping">

echo " [1/3] إنشاء ملفات init.py الصحيحة..."
touch "$BACKEND_DIR/app/init.py"
touch "$BACKEND_DIR/app/core/init.py"
touch "$MACRO_DIR/init.py"

[خطوة 2]: ضبط البيئة

echo " [2/3] تصدير مسار PYTHONPATH..."
export PYTHONPATH=$BACKEND_DIR

[خطوة 3]: التنفيذ الفعلي للاختبارات

echo " [3/3] تشغيل اختبارات unittest (Macro Surprise Engine)..."
echo "------------------------------------------------------------"

cd "$BACKEND_DIR"

تشغيل الاختبار وطباعة النتائج للطرفية

python3 -m unittest app.core.macro.test_macro_logic -v

التحقق من حالة الخروج (Exit Code)

if [ $? -eq 0 ]; then
echo "------------------------------------------------------------"
echo "✅ تم التحقق من منطق الماكرو بنجاح."
echo "📍 المسار المثبت: app.core.macro"
else
echo "------------------------------------------------------------"
echo "❌ فشلت الاختبارات. يرجى مراجعة ملف macro_engine.py"
exit 1
fi

#!/bin/bash

STREAMING_CHUNK: Initializing colors and interface...

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=======================================================${NC}"
echo -e "${YELLOW}   NDSP V4.1 Auto-Refactor Prep Tool (Governance)      ${NC}"
echo -e "${BLUE}=======================================================${NC}"

STREAMING_CHUNK: Creating secure backup of core logic...

CORE_DIR="backend/app/core"
BACKUP_DIR="backend/app/core_backup_V4_$(date +%Y%m%d_%H%M%S)"

if [ -d "$CORE_DIR" ]; then
echo -e "${YELLOW}[1] جاري إنشاء نسخة احتياطية آمنة للملفات...${NC}"
cp -r $CORE_DIR $BACKUP_DIR
echo -e "${GREEN}✅ تم حفظ النسخة الاحتياطية في: $BACKUP_DIR${NC}"
else
echo -e "${RED}❌ لم يتم العثور على مجلد $CORE_DIR. تأكد أنك في المسار الصحيح.${NC}"
exit 1
fi

echo ""

STREAMING_CHUNK: Neutralizing obsolete files...

echo -e "${YELLOW}[2] جاري تحييد الملفات المنتهية الصلاحية (Obsolete Files)...${NC}"
OBSOLETE_FILE="$CORE_DIR/decision_engine.py"

if [ -f "$OBSOLETE_FILE" ]; then
cat << 'EOF' > $OBSOLETE_FILE
"""
[OBSOLETE IN NDSP V4.1]
تم إيقاف هذا الملف بناءً على قوانين الحوكمة V4.1.
سلطة تحديد الاتجاه (Direction Authority) محصورة الآن فقط في الطبقة 6 
داخل المنسق الرئيسي (governed_pipeline.py).
"""
def run_decision(*args, kwargs):
return {
"status": "deprecated_in_v4.1",
"message": "Decision Engine is obsolete. Handled by Dominant Timed Direction (Layer 6)."
}
EOF
echo -e "${GREEN}✅ تم تعطيل decision_engine.py وتغليفه بقوانين V4.1.${NC}"
else
echo -e "${BLUE}ℹ️ ملف decision_engine.py غير موجود، لا حاجة للتعطيل.${NC}"
fi

echo ""

STREAMING_CHUNK: Gathering critical files for AI processing...

echo -e "${YELLOW}[3] جاري تجميع ملفات الطبقات الخطرة (التي تحتاج نزع سلطة الاتجاه)...${NC}"

TARGET_FILES=(
"$CORE_DIR/black_layer.py"
"$CORE_DIR/momentum_dual.py"
"$CORE_DIR/tdl_router.py"
"$CORE_DIR/conflict_engine.py"
)

OUTPUT_BATCH="ndsp_v4_batch_1.txt"
echo "--- NDSP V4.1 REFACTOR BATCH 1 ---" > $OUTPUT_BATCH

for file in "${TARGET_FILES[@]}"; do
if [ -f "$file" ]; then
echo -e "\n========================================" >> $OUTPUT_BATCH
echo "FILE_PATH: $file" >> $OUTPUT_BATCH
echo "========================================" >> $OUTPUT_BATCH
cat "$file" >> $OUTPUT_BATCH
echo -e "${GREEN}✅ تم استخراج: $file${NC}"
else
echo -e "${RED}❌ الملف غير موجود: $file${NC}"
fi
done

echo ""

STREAMING_CHUNK: Finalizing script and printing next steps...

echo -e "${BLUE}=======================================================${NC}"
echo -e "${GREEN}🎉 اكتملت العملية بنجاح!${NC}"
echo -e "${YELLOW}تم تجميع الملفات التي تنتهك قوانين V4.1 في ملف واحد باسم: ${NC}$OUTPUT_BATCH"
echo -e "لإكمال الهيكلة، قم بتنفيذ هذا الأمر وانسخ الناتج لي بالكامل:"
echo -e "${BLUE}cat $OUTPUT_BATCH${NC}"
echo -e "${BLUE}=======================================================${NC}"

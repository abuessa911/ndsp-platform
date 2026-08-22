#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="$HOME/empire-core-new/frontend/public-site"
cd "$TARGET_DIR"

echo "=================================================="
echo "    FORCE INTEGRATION OF DECISION FLOW COMPONENT   "
echo "=================================================="

HOME_FILE="src/pages/Home.tsx"

if [ -f "$HOME_FILE" ]; then
    echo "📝 جاري تعديل $HOME_FILE لاستدعاء المكون بصرياً..."
    
    # التأكد من وجود الـ Import
    if ! grep -q "import { DecisionFlow }" "$HOME_FILE"; then
        sed -i '1i import { DecisionFlow } from "../components/DecisionFlow";' "$HOME_FILE"
    fi

    # إنشاء نسخة احتياطية
    cp "$HOME_FILE" "${HOME_FILE}.bak"

    echo "✅ تم تحديث الاستدعاء. يرجى التحقق من مكان المكون."
fi

# تنظيف الكاش القديم بالكامل
echo "🧹 تنظيف Vite Cache ومجلد dist..."
rm -rf node_modules/.vite dist

# إعادة البناء
echo "🚀 جاري إعادة البناء..."
npm run build

# إجبار Nginx على إعادة التنشيط
echo "🔄 إعادة تحميل Nginx..."
sudo systemctl reload nginx || true

echo "=================================================="
echo "✨ تم إعادة البناء! يرجى تحديث المتصفح بـ Ctrl + F5"
echo "=================================================="

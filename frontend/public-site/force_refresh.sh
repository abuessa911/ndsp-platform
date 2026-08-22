#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="$HOME/empire-core-new/frontend/public-site"
cd "$TARGET_DIR"

echo "=================================================="
echo "    FORCE REBUILD & NGINX CACHE PURGE             "
echo "=================================================="

# 1. إزالة مجلد dist القديم بالكامل وبناء حزمة جديدة
rm -rf dist node_modules/.vite
npm run build

# 2. إعادة تحميل Nginx لتحديث الملفات الثابتة
echo "🔄 إعادة تحميل Nginx..."
sudo systemctl reload nginx || sudo service nginx reload

echo "=================================================="
echo "✨ تم إعادة البناء وتحديث Nginx بنجاح!"
echo "=================================================="

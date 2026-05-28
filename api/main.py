"""
تطبيق Empire Core API الرئيسي
نقطة الدخول الرئيسية لتشغيل الخادم
"""

import uvicorn
import logging
from pathlib import Path
import sys
import os

# إضافة مسار الوحدات
sys.path.insert(0, str(Path(__file__).parent))

# استيراد الإعدادات
from config import settings

# إعداد Logging
logging.basicConfig(
    level=settings.log_level,
    format=settings.log_format
)
logger = logging.getLogger(__name__)


def run_server():
    """تشغيل خادم FastAPI"""
    
    logger.info("=" * 60)
    logger.info("🚀 جاري بدء Empire Core API")
    logger.info("=" * 60)
    
    # طباعة الإعدادات (بدون معلومات حساسة)
    logger.info(f"📋 الإعدادات:")
    logger.info(f"   - Host: {settings.api_host}")
    logger.info(f"   - Port: {settings.api_port}")
    logger.info(f"   - Debug: {settings.debug}")
    logger.info(f"   - Log Level: {settings.log_level}")
    logger.info(f"   - Safe Mode: {settings.safe_mode}")
    logger.info(f"   - Dry Run: {settings.dry_run}")
    logger.info(f"   - Log Path: {settings.log_path}")
    logger.info(f"   - Backend API: {settings.backend_api_url}")
    
    logger.info("=" * 60)
    
    # التحقق من المجلدات
    log_path = Path(settings.log_path)
    if not log_path.exists():
        logger.warning(f"⚠️ مجلد الـ Logs غير موجود: {settings.log_path}")
    else:
        json_files = list(log_path.glob("*.json"))
        logger.info(f"✅ مجلد الـ Logs يحتوي على {len(json_files)} ملفات")
    
    # تشغيل الخادم
    try:
        uvicorn.run(
            "server:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=settings.debug,
            log_level=settings.log_level.lower(),
            access_log=True,
            use_colors=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف الخادم بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل الخادم: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_server()

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
from pathlib import Path
import os
from datetime import datetime

# إعداد Logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# إنشاء التطبيق
app = FastAPI(
    title="Empire Core API",
    description="API لتداول العملات والأسهم بذكاء اصطناعي",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إضافة CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# الإعدادات
LOG_PATH = Path(os.getenv("LOG_PATH", "/home/nawaf511/empire-core-new/logs"))
SECRET_TOKEN = os.getenv("API_SECRET_TOKEN", "empire-core-secret-token")

# إعداد الأمان
security = HTTPBearer()


async def verify_token(credentials = Depends(security)) -> str:
    """
    التحقق من صحة الـ Token
    
    Args:
        credentials: بيانات المصادقة
    
    Returns:
        str: الـ Token إذا كان صحيحاً
    
    Raises:
        HTTPException: إذا كان الـ Token غير صحيح
    """
    token = credentials.credentials
    if token != SECRET_TOKEN:
        logger.warning(f"⚠️ محاولة وصول بـ token خاطئ")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired token"
        )
    return token


def load_json_file(filename: str) -> dict:
    """
    تحميل ملف JSON مع معالجة الأخطاء
    
    Args:
        filename (str): اسم الملف (مثل: fused_signals.json)
    
    Returns:
        dict: محتوى الملف
    
    Raises:
        HTTPException: في حالة حدوث خطأ
    """
    file_path = LOG_PATH / filename
    
    logger.info(f"📂 جاري قراءة الملف: {file_path}")
    
    # التحقق من وجود الملف
    if not file_path.exists():
        logger.error(f"❌ الملف غير موجود: {file_path}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File '{filename}' not found"
        )
    
    # التحقق من أنه ملف صحيح
    if not file_path.is_file():
        logger.error(f"❌ '{filename}' ليس ملف صحيح")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"'{filename}' is not a valid file"
        )
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"✅ تم قراءة الملف بنجاح: {filename}")
        return data
    
    except json.JSONDecodeError as e:
        logger.error(f"❌ الملف يحتوي على JSON معطوب: {filename} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File '{filename}' contains invalid JSON"
        )
    
    except UnicodeDecodeError as e:
        logger.error(f"❌ خطأ في ترميز الملف: {filename} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File encoding error: {filename}"
        )
    
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع في قراءة الملف: {filename} - {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading file: {str(e)}"
        )


# ==================== Routes ====================

@app.get("/health", tags=["System"])
async def health_check():
    """
    فحص صحة الخادم
    
    Returns:
        dict: حالة الخادم
    """
    logger.info("🏥 فحص صحة الخادم")
    return {
        "status": "healthy",
        "timestamp": str(datetime.utcnow()),
        "service": "Empire Core API",
        "version": "1.0.0"
    }


@app.get("/signals", tags=["Trading Signals"])
async def get_signals(token: str = Depends(verify_token)):
    """
    الحصول على إشارات التداول المدمجة
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: بيانات الإشارات
    """
    logger.info("📊 طلب الحصول على إشارات التداول")
    return load_json_file("fused_signals.json")


@app.get("/scanner", tags=["Market Scanner"])
async def get_scanner(token: str = Depends(verify_token)):
    """
    الحصول على نتائج المسح العام للسوق
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: نتائج المسح
    """
    logger.info("🔍 طلب الحصول على نتائج المسح")
    return load_json_file("global_scan.json")


@app.get("/trades", tags=["Trade Journal"])
async def get_trades(token: str = Depends(verify_token)):
    """
    الحصول على دفتر التداول والعمليات المنفذة
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: بيانات التداولات
    """
    logger.info("📈 طلب الحصول على دفتر التداول")
    return load_json_file("trade_journal.json")


@app.get("/market-brain", tags=["Market Analysis"])
async def get_market_brain(token: str = Depends(verify_token)):
    """
    الحصول على تحليل السوق من المحرك الذكي
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: تحليل السوق
    """
    logger.info("🧠 طلب الحصول على تحليل السوق")
    return load_json_file("market_brain.json")


@app.get("/liquidity", tags=["Market Analysis"])
async def get_liquidity(token: str = Depends(verify_token)):
    """
    الحصول على بيانات السيولة والفرص
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: بيانات السيولة
    """
    logger.info("💧 طلب الحصول على بيانات السيولة")
    return load_json_file("liquidity_hunter.json")


@app.get("/analysis", tags=["Market Analysis"])
async def get_analysis(token: str = Depends(verify_token)):
    """
    الحصول على التحليل متعدد الأطر الزمنية
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: بيانات التحليل
    """
    logger.info("📊 طلب الحصول على التحليل متعدد الأطر")
    return load_json_file("multi_tf_analysis.json")


@app.get("/status", tags=["System"])
async def get_status(token: str = Depends(verify_token)):
    """
    الحصول على حالة النظام بالكامل
    
    Args:
        token: الـ Token للمصادقة (إلزامي)
    
    Returns:
        dict: حالة النظام الشاملة
    """
    logger.info("⚙️ طلب حالة النظام")
    
    try:
        return {
            "timestamp": str(datetime.utcnow()),
            "api_status": "running",
            "log_path": str(LOG_PATH),
            "available_files": [
                f.name for f in LOG_PATH.glob("*.json")
            ] if LOG_PATH.exists() else [],
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"❌ خطأ في الحصول على حالة النظام: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting system status: {str(e)}"
        )


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """معالج أخطاء HTTP"""
    logger.error(f"❌ HTTP Error {exc.status_code}: {exc.detail}")
    return {
        "error": True,
        "status_code": exc.status_code,
        "detail": exc.detail,
        "timestamp": str(datetime.utcnow())
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """معالج الأخطاء العامة"""
    logger.error(f"❌ Unexpected error: {exc}", exc_info=True)
    return {
        "error": True,
        "status_code": 500,
        "detail": "Internal server error",
        "timestamp": str(datetime.utcnow())
    }


# ==================== Startup & Shutdown ====================

@app.on_event("startup")
async def startup_event():
    """عند بدء التطبيق"""
    logger.info("🚀 جاري بدء تطبيق Empire Core API")
    logger.info(f"📂 مسار الـ Logs: {LOG_PATH}")
    
    if not LOG_PATH.exists():
        logger.warning(f"⚠️ مجلد الـ Logs غير موجود: {LOG_PATH}")
    else:
        logger.info(f"✅ مجلد الـ Logs موجود ويحتوي على {len(list(LOG_PATH.glob('*.json')))} ملفات")


@app.on_event("shutdown")
async def shutdown_event():
    """عند إيقاف التطبيق"""
    logger.info("🛑 جاري إيقاف تطبيق Empire Core API")


# ==================== Root ====================

@app.get("/", tags=["Root"])
async def root():
    """الصفحة الرئيسية"""
    return {
        "message": "Welcome to Empire Core API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    logger.info(f"🌐 بدء الخادم على {host}:{port}")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=debug,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )

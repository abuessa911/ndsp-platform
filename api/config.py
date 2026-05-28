from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """
    إعدادات تطبيق Empire Core API
    
    جميع الإعدادات قابلة للتخصيص من خلال:
    1. ملف .env
    2. متغيرات البيئة (Environment Variables)
    3. القيم الافتراضية (Defaults)
    """
    
    # ==================== API Settings ====================
    
    api_title: str = "Empire Core API"
    api_description: str = "API لتداول العملات والأسهم بذكاء اصطناعي"
    api_version: str = "1.0.0"
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # ==================== Security Settings ====================
    
    api_secret_token: str = os.getenv(
        "API_SECRET_TOKEN",
        "empire-core-secret-token"
    )
    
    # ⚠️ تحذير: غيّر هذا الـ Token في الإنتاج!
    # استخدم أداة قوية مثل: python -c "import secrets; print(secrets.token_urlsafe(32))"
    
    # ==================== CORS Settings ====================
    
    cors_origins: List[str] = (
        os.getenv("CORS_ORIGINS", "*").split(",")
        if os.getenv("CORS_ORIGINS")
        else ["*"]
    )
    
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: List[str] = ["*"]
    
    # ==================== Logging Settings ====================
    
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== Path Settings ====================
    
    log_path: str = os.getenv("LOG_PATH", "/home/nawaf511/empire-core-new/logs")
    data_path: str = os.getenv("DATA_PATH", "/home/nawaf511/empire-core-new/data")
    backup_path: str = os.getenv("BACKUP_PATH", "/home/nawaf511/empire-core-new/backups")
    
    # ==================== API Endpoints ====================
    
    backend_api_url: str = os.getenv(
        "BACKEND_API",
        "http://127.0.0.1:8001"
    )
    
    # ==================== Timeout Settings ====================
    
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    binance_timeout: int = int(os.getenv("BINANCE_TIMEOUT", "5"))
    
    # ==================== Trading Settings ====================
    
    default_symbol: str = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
    default_interval: str = os.getenv("DEFAULT_INTERVAL", "1h")
    
    # ==================== Binance Settings ====================
    
    binance_api_key: Optional[str] = os.getenv("BINANCE_API_KEY")
    binance_secret_key: Optional[str] = os.getenv("BINANCE_SECRET_KEY")
    binance_testnet: bool = os.getenv("BINANCE_TESTNET", "False").lower() == "true"
    
    # ==================== Database Settings ====================
    
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    database_echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"
    
    # ==================== Email Settings ====================
    
    smtp_server: Optional[str] = os.getenv("SMTP_SERVER")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: Optional[str] = os.getenv("SMTP_USER")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    # ==================== Telegram Settings ====================
    
    telegram_bot_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    
    # ==================== PayPal Settings ====================
    
    paypal_client_id: Optional[str] = os.getenv("PAYPAL_CLIENT_ID")
    paypal_client_secret: Optional[str] = os.getenv("PAYPAL_CLIENT_SECRET")
    paypal_mode: str = os.getenv("PAYPAL_MODE", "sandbox")  # sandbox أو live
    
    # ==================== Feature Flags ====================
    
    enable_trading: bool = os.getenv("ENABLE_TRADING", "False").lower() == "true"
    enable_notifications: bool = os.getenv("ENABLE_NOTIFICATIONS", "True").lower() == "true"
    enable_telegram: bool = os.getenv("ENABLE_TELEGRAM", "False").lower() == "true"
    safe_mode: bool = os.getenv("SAFE_MODE", "False").lower() == "true"
    dry_run: bool = os.getenv("DRY_RUN", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_paths()
        self._validate_settings()
    
    def _validate_paths(self):
        """التحقق من وجود المجلدات الضرورية"""
        paths = [
            (self.log_path, "Logs"),
            (self.data_path, "Data"),
            (self.backup_path, "Backup")
        ]
        
        for path_str, name in paths:
            path = Path(path_str)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"✅ تم إنشاء مجلد {name}: {path}")
                except Exception as e:
                    print(f"⚠️ تحذير: لم يتمكن من إنشاء مجلد {name}: {e}")
    
    def _validate_settings(self):
        """التحقق من صحة الإعدادات"""
        if not self.api_secret_token or self.api_secret_token == "your-secret-token":
            print("⚠️ تحذير: استخدم Secret Token قوي في الإنتاج!")
        
        if self.binance_api_key is None:
            print("⚠️ تحذير: Binance API Key غير مستخدمة")
        
        if self.cors_origins == ["*"]:
            print("⚠️ تحذير: CORS مفتوح لكل المصادر - غيّره في الإنتاج!")
    
    @property
    def is_production(self) -> bool:
        """هل التطبيق في بيئة الإنتاج؟"""
        return not self.debug and not self.dry_run
    
    @property
    def is_testing(self) -> bool:
        """هل التطبيق في وضع الاختبار؟"""
        return self.binance_testnet or self.dry_run
    
    def get_binance_url(self) -> str:
        """الحصول على URL Binance الصحيح"""
        if self.binance_testnet:
            return "https://testnet.binance.vision"
        else:
            return "https://api.binance.com"
    
    def to_dict(self) -> dict:
        """تحويل الإعدادات إلى dictionary (بدون كلمات سرية)"""
        config_dict = self.model_dump()
        
        # أزل المعلومات الحساسة
        sensitive_keys = [
            "api_secret_token",
            "binance_secret_key",
            "smtp_password",
            "paypal_client_secret",
            "telegram_bot_token"
        ]
        
        for key in sensitive_keys:
            if key in config_dict:
                config_dict[key] = "***HIDDEN***"
        
        return config_dict


# إنشاء instance واحد من الإعدادات
settings = Settings()

# يمكن استخدامه في أي مكان بهذه الطريقة:
# from config import settings
# print(settings.api_port)

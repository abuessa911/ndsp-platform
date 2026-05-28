# NDSP Architecture Implementation - V4.1
# Reference File: "الملخص التنفيذي والمعماري الكامل_43.txt"

class NDSPTimezoneAdapter:
    def __init__(self):
        # مراجع المنطقة الزمنية لضمان عدم وجود فجوات حدودية
        self.configs = {
            "CRYPTO": "UTC",              # معيار Binance الرسمي[cite: 2]
            "TRADITIONAL": "BROKER_TZ"    # توقيت خادم FXCM/MT4[cite: 2]
        }

    def resolve_reference_time(self, symbol, market_type):
        """تثبيت التوقيت المرجعي لكل أصل لضمان اتساق مستويات الـ Weekly Open"""
        tz_type = self.configs.get(market_type, "UTC")
        
        if tz_type == "UTC":
            # الكريبتو يعمل بنظام توقيت عالمي موحد لضمان تطابق الشموع[cite: 2]
            return "Reference: UTC+00:00 (Global Alignment)"
        else:
            # الأسواق التقليدية ترتبط بساعة إغلاق نيويورك أو وقت الخادم[cite: 2]
            return "Reference: Broker Server Time (Liquidity Alignment)"

    def get_weekly_open_gate(self, market_type):
        """تحديد بوابة الافتتاح الأسبوعي لضمان دقة Layer 8.3"""
        if market_type == "CRYPTO":
            return "Monday 00:00 UTC" # معيار ثابت للكريبتو[cite: 2]
        else:
            # يعتمد على ساعات المنتج لتجنب الـ fake expansion عند الافتتاح
            return "Sunday/Monday Session Start (Asset Specific)"

# --- منطق التشغيل والتحقق ---
adapter = NDSPTimezoneAdapter()
gold_ref = adapter.resolve_reference_time("XAUUSD", "TRADITIONAL")
btc_ref = adapter.resolve_reference_time("BTCUSDT", "CRYPTO")

print(f"XAUUSD Reference: {gold_ref}")
print(f"BTCUSDT Reference: {btc_ref}")

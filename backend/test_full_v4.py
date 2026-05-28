import json
import time
from app.core.ndsp_v4_pipeline import run_ndsp_v4_pipeline

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def test_full_pipeline():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=======================================================")
    print(" 🚀 بدء محاكاة المنسق الرئيسي NDSP V4.1 (Live Data Pipeline)")
    print("======================================================={Colors.RESET}\n")

    # لم نعد نستخدم mock_cot الوهمية!
    # المنسق سيسحب البيانات الحقيقية من ملف الـ JSON
    target_symbol = "EURUSD"

    # محاكاة حالة سوق خطر (Flash Crash) لغرض اختبار دمج COT وتأثير الطبقة السوداء 12
    mock_market = {"volatility_spike": True, "low_liquidity": True}
    
    # محاكاة صحة البيانات
    mock_health = {"cot_age_hours": 24}

    print(f"{Colors.CYAN}➔ جاري سحب بيانات [{target_symbol}] الحقيقية ومعالجتها عبر جميع طبقات V4.1...{Colors.RESET}\n")
    
    # تشغيل المنسق الرئيسي بدون تمرير بيانات وهمية
    final_contract = run_ndsp_v4_pipeline(
        symbol=target_symbol, 
        data_health=mock_health,
        market_conditions=mock_market
    )

    print(f"{Colors.BOLD}[العقد النهائي المُصدر - Final Decision Contract]{Colors.RESET}")
    print(json.dumps(final_contract, indent=2, ensure_ascii=False))
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}=======================================================")
    print(" ✅ الفحوصات المعمارية للعقد النهائي (البيانات الحية):")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}=======================================================")
    print(" ✅ الفحوصات المعمارية للعقد النهائي:")
    
    decision = final_contract["decision"]
    
    # 1. فحص المادة 11 (منع التنفيذ المباشر)
    if decision["execution_allowed"] == False and decision["execution_mode"] == "decision_support_only":
        print(f" {Colors.GREEN}[Pass]{Colors.RESET} المادة 11: التنفيذ المباشر محظور بشكل سليم (Decision Support Only).")
    else:
        print(f" {Colors.RED}[Fail]{Colors.RESET} المادة 11: تم اختراق قواعد التنفيذ!")

    # 2. فحص العقوبات (يجب أن تنخفض الثقة بسبب الصراع والسوق الخطر)
    if decision["confidence"] < 50:
        print(f" {Colors.GREEN}[Pass]{Colors.RESET} الطبقة 13: الثقة تأثرت بشكل صحيح بالعقوبات (الثقة الحالية: {decision['confidence']}% / Grade: {decision['grade']}).")
    else:
        print(f" {Colors.RED}[Fail]{Colors.RESET} الطبقة 13: لم يتم تطبيق عقوبات الثقة بشكل صحيح!")
        
    # 3. فحص المخاطر (الطبقة 12 و 14)
    if decision["risk_state"] == "caution" or decision["decision_state"] == "ACTIVE_CAUTION":
        print(f" {Colors.GREEN}[Pass]{Colors.RESET} الطبقة 12/14: حالة الخطر تم رفعها بنجاح بناءً على بيانات السوق.")
    else:
        print(f" {Colors.RED}[Fail]{Colors.RESET} الطبقة 12/14: فشل النظام في التعرف على مخاطر السوق!")

    print("======================================================={Colors.RESET}\n")

if __name__ == "__main__":
    test_full_pipeline()

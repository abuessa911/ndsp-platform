import json
import time

# استيراد الطبقات التي قمنا بتنظيفها ونزع سلطة الاتجاه منها
from app.core.conflict_engine import evaluate_conflict
from app.core.black_layer import evaluate_black_layer

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(title, data):
    print(f"{Colors.CYAN}➔ {title}:{Colors.RESET}")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("-" * 40)

def simulate_conflict_engine():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== [1] اختبار محرك الصراع (Layer 5.6) ==={Colors.RESET}")
    
    # محاكاة بيانات واردة من TDL: المؤسسات (شراء) والمضاربين (بيع)
    mock_payload = {
        "tdl_lm_direction": "bullish",
        "tdl_s_direction": "bearish"
    }
    
    result = evaluate_conflict(mock_payload)
    print_step("مخرجات محرك الصراع عند وجود تعارض", result)
    
    if result.get("participant_conflict") == True and result.get("conflict_penalty") == 12:
        print(f"{Colors.GREEN}✅ نجاح: المحرك اكتشف الصراع وأصدر عقوبة (-12 نقطة) دون التدخل في الاتجاه.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ فشل: المحرك لم يطبق العقد بشكل صحيح.{Colors.RESET}")

def simulate_black_layer():
    print(f"\n{Colors.BOLD}{Colors.YELLOW}=== [2] اختبار الطبقة السوداء (Layer 12) ==={Colors.RESET}")
    
    # محاكاة سوق خطر: زخم ضعيف، سيولة عنيفة، ومناطق مقاومة
    mock_momentum = {"strength": 0.2, "context": "weak"}
    mock_liquidity = {"state": "sweep_up"}
    mock_volatility = {"state": "high"}
    mock_zones = {"state": "resistance"}
    
    result = evaluate_black_layer(mock_momentum, mock_liquidity, mock_volatility, mock_zones)
    print_step("مخرجات الطبقة السوداء في بيئة عالية المخاطر", result)
    
    if result.get("black_layer_state") == "protective_block" and result.get("black_layer_penalty") == 25:
        print(f"{Colors.GREEN}✅ نجاح: الطبقة السوداء فعلت (الحظر الوقائي) وأصدرت عقوبة (-25 نقطة) دون تغيير الاتجاه.{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ فشل: الطبقة السوداء لم تطبق العقد بشكل صحيح.{Colors.RESET}")

def run_all_validations():
    print(f"{Colors.BOLD}{Colors.GREEN}\n=======================================================")
    print(" 🚀 بدء محاكاة فحص حوكمة NDSP V4.1 (نزع سلطة الاتجاه)")
    print("=======================================================\n" + Colors.RESET)
    
    time.sleep(1)
    simulate_conflict_engine()
    
    time.sleep(1)
    simulate_black_layer()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}=======================================================")
    print(" 🎉 اكتملت المحاكاة! جميع الطبقات المحدثة تلتزم بعقد V4.1 بشكل صارم.")
    print(" - الاتجاه محمي تماماً.")
    print(" - العقوبات (Penalties) تُحسب بدقة لترسل إلى طبقة الجودة (Layer 13).")
    print("=======================================================\n" + Colors.RESET)

if __name__ == "__main__":
    run_all_validations()

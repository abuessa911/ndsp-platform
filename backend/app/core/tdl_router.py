from app.engines.tdl_cot_engine import calculate_cot_tdl

def run_tdl(symbol: str, data: dict, profile: dict):
    """
    💀 NDSP LAYER 5: timing_model ROUTER
    [GOVERNANCE V4.1 ENFORCED]
    - timing_model يحسب الاتجاهين (L&M و S) بشكل مستقل.
    - لا يحق لـ timing_model إصدار صفة "Dominant". الكلمة النهائية تعود للطبقة 6 (Timing).
    """
    try:
        result = calculate_cot_tdl(data)
        
        # 💀 المادة 7: تجريد سلطة الاتجاه المسيطر
        # يتم إزالة حقل dominant لمنع أي طبقة سابقة من فرض رأيها
        if "dominant" in result:
            del result["dominant"]
            
        return result
        
    except Exception as e:
        return {
            "layer_metadata": {
                "layer_name": "Layer 5: timing_model Core",
                "authority": "Direction Computation (Non-Dominant)",
                "error": True
            },
            "tdl_lm_score": 0,
            "tdl_s_score": 0,
            "tdl_lm_direction": "neutral",
            "tdl_s_direction": "neutral",
            "error": str(e),
        }

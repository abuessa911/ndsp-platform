"""
💀 NDSP LAYER 5.6: Participant Conflict State Layer
[GOVERNANCE V4.1 ENFORCED]
- لا يحق لمحرك الصراع تحديد الاتجاه.
- وظيفته مقارنة L&M مع S وإصدار عقوبة ثقة (Confidence Penalty) في حال التعارض.
"""

def evaluate_conflict(payload: dict = None):
    """
    يقوم بتحليل مخرجات timing_model وتحديد ما إذا كان هناك صراع بين الفئات الكبيرة والصغيرة.
    """
    payload = payload or {}
    
    # محاولة استخراج بيانات timing_model من الهيكلة القديمة أو الجديدة
    tdl_data = payload.get("timing_model", payload)
    
    lm_dir = str(tdl_data.get("tdl_lm_direction", tdl_data.get("weekly", {}).get("lm_direction", "neutral"))).lower()
    s_dir = str(tdl_data.get("tdl_s_direction", tdl_data.get("weekly", {}).get("s_direction", "neutral"))).lower()

    # التضارب يحدث إذا كان كلاهما نشطاً ولكن في اتجاهين متعاكسين
    conflict_active = (lm_dir != s_dir) and (lm_dir != "neutral") and (s_dir != "neutral")
    
    if conflict_active:
        state = "conflict"
        penalty = 12 # خصم 12 نقطة من نسبة الثقة (Layer 13)
        summary = f"Participant Conflict Detected: L&M ({lm_dir.upper()}) vs S ({s_dir.upper()})"
    elif lm_dir == s_dir and lm_dir != "neutral":
        state = "aligned"
        penalty = 0
        summary = "Participants are aligned (Golden Alignment active)."
    else:
        state = "neutral"
        penalty = 0
        summary = "No conflicting momentum detected."

    return {
        "layer_metadata": {
            "layer_name": "Layer 5.6: Participant Conflict State",
            "authority": "Quality Context Authority",
            "version": "4.1"
        },
        "status": "context_evaluated",
        "participant_conflict": conflict_active,
        "alignment_state": state,
        "conflict_penalty": penalty, # Consumed by Layer 13
        "score": penalty, # Legacy support
        "summary": summary,
    }

def run(payload=None, **kwargs):
    """نقطة الدخول المتوافقة مع الاستدعاءات القديمة"""
    return evaluate_conflict(payload or kwargs)

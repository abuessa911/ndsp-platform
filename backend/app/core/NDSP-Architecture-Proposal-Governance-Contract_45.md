# NDSP Layer 13: Decision Quality Stack Implementation
# Reference: الملخص التنفيذي والمعماري الكامل_45.txt

class DecisionQualityStack:
    def __init__(self):
        # أوزان الطبقات الإثرائية (Weights) وفقاً للهيكلة V4.1
        self.weights = {
            "golden_alignment": 25,    # وزن إضافي عند تطابق السيولة
            "weekly_open_gravity": 15, # قوة جذب الافتتاح الأسبوعي[cite: 2]
            "momentum_dual": 10,       # توافق الزخم[cite: 2]
            "macro_alignment": 20      # التوافق المايكرو (الفيدرالي/الأخبار)[cite: 2]
        }

    def calculate_final_quality(self, tdl_base_conf, effects):
        """
        تجميع التأثيرات لإنتاج عقد القرار النهائي (Final Decision Contract)[cite: 4]
        """
        score = tdl_base_conf
        
        # تطبيق التأثيرات الإيجابية والسلبية[cite: 2, 4]
        if effects.get("golden_alignment_active"):
            score += self.weights["golden_alignment"]
        
        if effects.get("above_weekly_open"):
            score += self.weights["weekly_open_gravity"]
            
        # كبحة الأمان (Penalty) من Black Layer
        if effects.get("black_layer_danger"):
            score -= 40 # خصم كبير عند رصد سلوك شاذ[cite: 2]

        # حصر النتيجة بين 0 و 100[cite: 2]
        final_confidence = max(0, min(100, score))
        
        # تحديد الدرجة (Grade) بناءً على نطاقات الجودة[cite: 2]
        grade = self._assign_grade(final_confidence)
        
        return {
            "final_confidence": final_confidence,
            "grade": grade,
            "quality_label": self._get_label(grade)
        }

    def _assign_grade(self, conf):
        if conf >= 80: return "A"
        if conf >= 65: return "B"
        if conf >= 50: return "C"
        return "D"

    def _get_label(self, grade):
        labels = {"A": "Institutional Strong", "B": "High Probability", "C": "Neutral/Caution", "D": "Avoid/Blocked"}
        return labels.get(grade, "Unknown")

# --- محاكاة إصدار القرار النهائي (Final Decision) ---
stack = DecisionQualityStack()
# مثال: اتجاه شرائي من TDL بخصم أساسي 50% مع تفعيل Golden Alignment[cite: 2, 5]
results = stack.calculate_final_quality(50, {"golden_alignment_active": True, "above_weekly_open": True})

print(f"Final Decision Confidence: {results['final_confidence']}%")
print(f"Decision Grade: {results['grade']} ({results['quality_label']})")

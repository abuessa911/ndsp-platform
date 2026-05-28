"""
NDSP Layer 16: Scenario & Explainability Engine

Authority:
    Narrative Authority only.

Purpose:
    Consume Final Decision Contract and produce safe human-readable scenarios,
    explanations, and user-facing decision-support narrative.

Hard Rules:
    - Does not change direction.
    - Does not change confidence.
    - Does not change risk_state.
    - Does not change decision_state.
    - Does not create trade execution instructions.
    - Does not expose internal sensitive layer logic to public/user outputs.

This layer is a post-decision consumer. It must never become a source for
Final Decision.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping, Optional


DecisionDict = Dict[str, Any]


@dataclass(frozen=True)
class ScenarioReport:
    """
    Safe narrative output generated from the final decision contract.

    This dataclass is immutable to prevent accidental mutation after creation.
    """

    headline: str
    narrative_summary: str
    primary_scenario: str
    alternative_scenario: str
    invalidation_context: str
    risk_warnings: List[str] = field(default_factory=list)
    decision_support_guidance: str = ""
    public_notice: str = (
        "NDSP provides decision-support analysis only. This output is not "
        "financial advice, not a trading recommendation, and not an execution instruction."
    )

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary representation."""
        return asdict(self)


class NarrativeEngine:
    """
    Layer 16 Narrative Engine.

    It reads the final decision contract and produces safe scenario text.
    It has no authority to change the decision contract.
    """

    SAFE_DIRECTIONS = {"bullish", "bearish", "neutral"}

    def generate_report(
        self,
        final_decision: Mapping[str, Any],
        *,
        language: str = "ar",
        audience: str = "user",
    ) -> ScenarioReport:
        """
        Generate a safe scenario report from a Final Decision contract.

        Args:
            final_decision:
                Final decision payload. Expected shape:
                {"decision": {...}}
            language:
                "ar" or "en".
            audience:
                "public", "user", or "admin_owner".

        Returns:
            ScenarioReport

        Raises:
            ValueError:
                If language or audience is unsupported.
        """
        language = self._normalize_language(language)
        audience = self._normalize_audience(audience)

        decision = dict(final_decision.get("decision", {}) or {})

        direction = str(decision.get("direction", "neutral")).lower()
        if direction not in self.SAFE_DIRECTIONS:
            direction = "neutral"

        confidence = self._safe_number(decision.get("confidence", 0), default=0)
        grade = str(decision.get("grade", "N/A"))
        risk_state = str(decision.get("risk_state", "normal"))
        decision_state = str(decision.get("decision_state", "review"))
        execution_allowed = bool(decision.get("execution_allowed", False))
        timing_controller = str(decision.get("timing_controller", "market_context"))

        direction_label = self._direction_label(direction, language)
        risk_label = self._risk_label(risk_state, language)
        state_label = self._state_label(decision_state, language)
        controller_label = self._controller_label(timing_controller, language, audience)

        headline = self._headline(direction_label, grade, confidence, language)
        narrative = self._narrative(
            direction_label=direction_label,
            confidence=confidence,
            grade=grade,
            risk_label=risk_label,
            state_label=state_label,
            controller_label=controller_label,
            language=language,
        )

        primary, alternative, invalidation = self._scenario_text(direction, language)

        warnings = self._risk_warnings(
            risk_state=risk_state,
            decision_state=decision_state,
            execution_allowed=execution_allowed,
            language=language,
        )

        guidance = self._guidance(
            decision_state=decision_state,
            execution_allowed=execution_allowed,
            language=language,
        )

        notice = self._notice(language)

        return ScenarioReport(
            headline=headline,
            narrative_summary=narrative,
            primary_scenario=primary,
            alternative_scenario=alternative,
            invalidation_context=invalidation,
            risk_warnings=warnings,
            decision_support_guidance=guidance,
            public_notice=notice,
        )

    def attach_report(
        self,
        final_decision: Mapping[str, Any],
        *,
        language: str = "ar",
        audience: str = "user",
    ) -> Dict[str, Any]:
        """
        Return a copied decision payload with scenario_report attached.

        This method does not mutate the original decision object.
        """
        cloned = deepcopy(dict(final_decision))
        report = self.generate_report(cloned, language=language, audience=audience)
        cloned["scenario_report"] = report.to_dict()
        cloned["scenario_layer_contract"] = {
            "layer": "scenario_explainability",
            "authority": "Narrative Authority",
            "can_modify_direction": False,
            "can_modify_confidence": False,
            "can_modify_risk": False,
            "can_modify_decision_state": False,
            "post_decision_consumer": True,
        }
        return cloned

    def assert_no_decision_mutation(
        self,
        before: Mapping[str, Any],
        after: Mapping[str, Any],
    ) -> bool:
        """
        Verify that Layer 16 did not mutate the decision contract.

        It compares the original decision object with the decision object
        inside the output after scenario attachment.
        """
        before_decision = dict(before.get("decision", {}) or {})
        after_decision = dict(after.get("decision", {}) or {})
        return before_decision == after_decision

    @staticmethod
    def _normalize_language(language: str) -> str:
        lang = str(language or "ar").strip().lower()
        if lang in {"ar", "arabic"}:
            return "ar"
        if lang in {"en", "english"}:
            return "en"
        raise ValueError("language must be 'ar' or 'en'")

    @staticmethod
    def _normalize_audience(audience: str) -> str:
        aud = str(audience or "user").strip().lower()
        if aud in {"public", "user", "admin_owner"}:
            return aud
        raise ValueError("audience must be 'public', 'user', or 'admin_owner'")

    @staticmethod
    def _safe_number(value: Any, default: float = 0) -> float:
        try:
            return round(float(value), 2)
        except Exception:
            return default

    @staticmethod
    def _direction_label(direction: str, language: str) -> str:
        if language == "ar":
            return {
                "bullish": "انحياز إيجابي",
                "bearish": "انحياز سلبي",
                "neutral": "حياد تحليلي",
            }.get(direction, "حياد تحليلي")
        return {
            "bullish": "Positive Bias",
            "bearish": "Negative Bias",
            "neutral": "Neutral Bias",
        }.get(direction, "Neutral Bias")

    @staticmethod
    def _risk_label(risk_state: str, language: str) -> str:
        risk_state = risk_state.lower()
        if language == "ar":
            mapping = {
                "normal": "طبيعية",
                "caution": "حذر",
                "elevated": "مرتفعة",
                "blocked": "مقيدة",
                "market_closed": "السوق غير مناسب",
                "data_warning": "تحذير بيانات",
            }
            return mapping.get(risk_state, risk_state)
        mapping = {
            "normal": "Normal",
            "caution": "Caution",
            "elevated": "Elevated",
            "blocked": "Restricted",
            "market_closed": "Market Not Suitable",
            "data_warning": "Data Warning",
        }
        return mapping.get(risk_state, risk_state)

    @staticmethod
    def _state_label(decision_state: str, language: str) -> str:
        decision_state = decision_state.lower()
        if language == "ar":
            mapping = {
                "active": "نشطة",
                "active_caution": "نشطة بحذر",
                "blocked": "محجوبة",
                "review": "قيد المراجعة",
                "safe_mode": "وضع آمن",
            }
            return mapping.get(decision_state, decision_state)
        mapping = {
            "active": "Active",
            "active_caution": "Active With Caution",
            "blocked": "Blocked",
            "review": "Under Review",
            "safe_mode": "Safe Mode",
        }
        return mapping.get(decision_state, decision_state)

    @staticmethod
    def _controller_label(controller: str, language: str, audience: str) -> str:
        if audience != "admin_owner":
            return "السياق الزمني للسوق" if language == "ar" else "Market Timing Context"

        if language == "ar":
            return controller
        return controller

    @staticmethod
    def _headline(
        direction_label: str,
        grade: str,
        confidence: float,
        language: str,
    ) -> str:
        if language == "ar":
            return f"تقييم NDSP: {direction_label} | الدرجة: {grade} | الثقة: {confidence}%"
        return f"NDSP Assessment: {direction_label} | Grade: {grade} | Confidence: {confidence}%"

    @staticmethod
    def _narrative(
        *,
        direction_label: str,
        confidence: float,
        grade: str,
        risk_label: str,
        state_label: str,
        controller_label: str,
        language: str,
    ) -> str:
        if language == "ar":
            return (
                f"بناءً على {controller_label}، يظهر السوق في حالة {direction_label}. "
                f"جودة القراءة مصنفة بدرجة {grade} مع مستوى ثقة {confidence}%. "
                f"حالة المخاطر الحالية: {risk_label}. "
                f"حالة القرار: {state_label}. "
                "هذه قراءة سياقية لدعم القرار وليست توصية مالية أو أمر تنفيذ."
            )

        return (
            f"Based on the {controller_label}, the market currently shows a "
            f"{direction_label}. The analytical quality is graded {grade} with "
            f"{confidence}% confidence. Current risk state: {risk_label}. "
            f"Decision state: {state_label}. This is contextual decision-support "
            "analysis, not financial advice or an execution instruction."
        )

    @staticmethod
    def _scenario_text(direction: str, language: str) -> tuple[str, str, str]:
        if language == "ar":
            if direction == "bullish":
                return (
                    "السيناريو الأساسي: استمرار التحسن السعري بشرط بقاء السياق الداعم قائمًا.",
                    "السيناريو البديل: ضعف الاستجابة السعرية أو فقدان المنطقة الهيكلية قد يحول القراءة إلى حذر.",
                    "سياق الإبطال: فقدان البنية الداعمة أو ارتفاع المخاطر التشغيلية أو ضعف جودة البيانات.",
                )
            if direction == "bearish":
                return (
                    "السيناريو الأساسي: استمرار الضغط السلبي ما دام السياق العام غير داعم.",
                    "السيناريو البديل: استعادة المناطق الهيكلية المهمة قد تخفف القراءة السلبية.",
                    "سياق الإبطال: تحسن واضح في البنية السعرية أو تراجع المخاطر أو تغير جودة السياق.",
                )
            return (
                "السيناريو الأساسي: استمرار التذبذب والانتظار حتى تتضح بيئة القرار.",
                "السيناريو البديل: خروج واضح من النطاق الحالي قد يغير جودة القراءة.",
                "سياق الإبطال: ظهور اتجاه واضح مدعوم بجودة بيانات وسياق سوق أفضل.",
            )

        if direction == "bullish":
            return (
                "Primary scenario: continued constructive price behavior while supportive context remains intact.",
                "Alternative scenario: weak price response or loss of structure may shift the reading toward caution.",
                "Invalidation context: loss of supportive structure, elevated operational risk, or degraded data quality.",
            )
        if direction == "bearish":
            return (
                "Primary scenario: continued negative pressure while the broader context remains unsupportive.",
                "Alternative scenario: reclaiming important structural areas may reduce the negative reading.",
                "Invalidation context: improved structure, reduced risk, or better contextual quality.",
            )
        return (
            "Primary scenario: continued range-bound behavior until the decision environment becomes clearer.",
            "Alternative scenario: a clear break from the current range may improve the quality of the reading.",
            "Invalidation context: emergence of a clear directional environment supported by better data and context.",
        )

    @staticmethod
    def _risk_warnings(
        *,
        risk_state: str,
        decision_state: str,
        execution_allowed: bool,
        language: str,
    ) -> List[str]:
        warnings: List[str] = []

        risk_state_l = risk_state.lower()
        decision_state_l = decision_state.lower()

        if language == "ar":
            if not execution_allowed:
                warnings.append("المنظومة تعمل بوضع دعم القرار فقط ولا تصدر أوامر تنفيذ.")
            if decision_state_l == "blocked":
                warnings.append("حالة القرار مقيدة بسبب ارتفاع المخاطر أو ضعف ملاءمة السياق.")
            if decision_state_l == "active_caution":
                warnings.append("القراءة نشطة ولكنها تتطلب حذرًا بسبب تعارض أو ضعف جزئي في الجودة.")
            if risk_state_l not in {"normal", "stable"}:
                warnings.append(f"حالة المخاطر ليست طبيعية: {risk_state}.")
            return warnings

        if not execution_allowed:
            warnings.append("The platform is operating in decision-support mode only and does not issue execution orders.")
        if decision_state_l == "blocked":
            warnings.append("Decision state is restricted due to elevated risk or unsuitable context.")
        if decision_state_l == "active_caution":
            warnings.append("The reading is active but requires caution due to partial conflict or lower quality.")
        if risk_state_l not in {"normal", "stable"}:
            warnings.append(f"Risk state is not normal: {risk_state}.")
        return warnings

    @staticmethod
    def _guidance(
        *,
        decision_state: str,
        execution_allowed: bool,
        language: str,
    ) -> str:
        decision_state_l = decision_state.lower()

        if language == "ar":
            if decision_state_l == "blocked":
                return "إرشاد دعم القرار: يفضل التعامل مع هذه القراءة كتحذير سياقي وليس كفرصة قابلة للتصرف."
            if decision_state_l == "active_caution":
                return "إرشاد دعم القرار: القراءة قابلة للمراقبة مع ضرورة رفع مستوى الحذر والانضباط."
            if not execution_allowed:
                return "إرشاد دعم القرار: استخدم القراءة لفهم السياق فقط؛ لا تمثل أمر شراء أو بيع."
            return "إرشاد دعم القرار: القراءة توضح حالة السوق ولا تمثل توصية مالية."

        if decision_state_l == "blocked":
            return "Decision-support guidance: treat this reading as a contextual warning, not an actionable opportunity."
        if decision_state_l == "active_caution":
            return "Decision-support guidance: monitor the reading with increased caution and discipline."
        if not execution_allowed:
            return "Decision-support guidance: use this reading for context only; it is not a buy or sell instruction."
        return "Decision-support guidance: this reading describes the market state and is not financial advice."

    @staticmethod
    def _notice(language: str) -> str:
        if language == "ar":
            return (
                "تنويه: تستخدم NDSP تسميات عامة ومبسطة لحماية منطق المنظومة وخصوصية مصادرها. "
                "هذه القراءة لدعم القرار فقط ولا تمثل توصية مالية أو تنفيذ تداول."
            )
        return (
            "Notice: NDSP uses generalized labels to protect internal logic and data-source privacy. "
            "This is decision-support analysis only and does not represent financial advice or trade execution."
        )

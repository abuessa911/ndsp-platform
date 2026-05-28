import unittest

from app.core.scenario.scenario_engine import ScenarioEngine, ScenarioInput


class TestScenario(unittest.TestCase):
    def setUp(self):
        self.engine = ScenarioEngine()

    def test_blocked_scenario_narration(self):
        report = self.engine.generate_report(
            ScenarioInput(
                direction="BULLISH",
                grade="F_BLOCKED",
                confidence=0.0,
                decision_state="blocked",
                risk_state="high",
                execution_allowed=False,
                reasons=["HIGH_SPREAD_RISK"],
                macro_sentiment="HAWKISH",
                symbol="XAUUSD",
                timeframe="1h",
            )
        )

        self.assertIn("محجوب بواسطة صمام الأمان", report.summary)
        self.assertIn("البقاء في وضع المراقبة", report.next_expectation)
        self.assertIn("HIGH_SPREAD_RISK", report.safety_alerts)
        self.assertTrue(report.sanitized)
        self.assertFalse(report.metadata["execution_allowed"])

    def test_active_scenario_does_not_say_ready_to_execute(self):
        report = self.engine.generate_report(
            ScenarioInput(
                direction="BEARISH",
                grade="A",
                confidence=92.0,
                decision_state="active",
                risk_state="normal",
                execution_allowed=False,
                reasons=[],
                macro_sentiment="DOVISH",
                symbol="BTCUSDT",
            )
        )

        self.assertIn("دعم قرار فقط", report.summary)
        self.assertNotIn("جاهز للتنفيذ", report.summary)
        self.assertFalse(report.metadata["execution_allowed"])
        self.assertEqual(report.metadata["execution_mode"], "decision_support_only")

    def test_active_caution_scenario(self):
        report = self.engine.generate_report(
            ScenarioInput(
                direction="BULLISH",
                grade="C",
                confidence=55.0,
                decision_state="active_caution",
                risk_state="caution",
                execution_allowed=False,
                reasons=["SAFETY_CAUTION"],
                macro_sentiment="NEUTRAL",
            )
        )

        self.assertIn("نشط بحذر", report.summary)
        self.assertIn("مراقبة", report.next_expectation)
        self.assertIn("SAFETY_CAUTION", report.safety_alerts)

    def test_scenario_does_not_modify_direction_or_confidence(self):
        report = self.engine.generate_report(
            ScenarioInput(
                direction="BEARISH",
                grade="B",
                confidence=77.7,
                decision_state="active",
                risk_state="normal",
                execution_allowed=False,
                reasons=[],
                macro_sentiment="NEUTRAL",
            )
        )

        self.assertIn("هابط", report.summary)
        self.assertIn("77.70%", report.summary)
        self.assertFalse(hasattr(report, "direction_override"))
        self.assertFalse(hasattr(report, "confidence_override"))

    def test_generate_from_decision_dict(self):
        report = self.engine.generate_report_from_decision_dict(
            {
                "direction": "BULLISH",
                "grade": "A",
                "confidence": 88.0,
                "decision_state": "active",
                "risk_state": "normal",
                "execution_allowed": False,
                "reasons": [],
                "macro_sentiment": "HAWKISH",
                "symbol": "EURUSD",
                "timeframe": "4h",
            }
        )

        self.assertIn("EURUSD", report.summary)
        self.assertIn("4h", report.summary)
        self.assertTrue(report.sanitized)

    def test_pretty_report_runs(self):
        report = self.engine.generate_report(
            ScenarioInput(
                direction="NEUTRAL",
                grade="D",
                confidence=35.0,
                decision_state="active",
                risk_state="normal",
                execution_allowed=False,
                reasons=[],
                macro_sentiment="UNKNOWN",
            )
        )

        self.engine.print_pretty_report(report)


if __name__ == "__main__":
    unittest.main()

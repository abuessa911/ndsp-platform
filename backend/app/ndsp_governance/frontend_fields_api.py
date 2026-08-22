from __future__ import annotations

from typing import Any, Dict, Optional

try:
    from fastapi import Query
except Exception:
    Query = None

try:
    from app.ndsp_governance.decision_output_policy import govern_decision_output
except Exception:
    from ndsp_governance.decision_output_policy import govern_decision_output


def install_ndsp_frontend_fields_routes(app: Any) -> None:
    installed = getattr(app.state, "ndsp_frontend_fields_routes_installed", False)
    if installed:
        return

    @app.get("/api/ndsp/frontend-fields/probe")
    def ndsp_frontend_fields_probe(
        package: str = "elite",
        symbol: str = "BTCUSDT",
        market: str = "crypto",
        timeframe: str = "1h",
        lm_direction: str = "UPWARD",
        s_direction: str = "UPWARD",
        side_relation: str = "DIFFERENT",
        activation_level: Optional[float] = None,
        arrival_level: Optional[float] = None,
        invalidation_level: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload = {
            "ok": True,
            "symbol": symbol,
            "market": market,
            "timeframe": timeframe,
            "package": package,
            "direction": "bullish" if str(lm_direction).upper() == "UPWARD" else "bearish",
            "lm_direction": lm_direction,
            "s_direction": s_direction,
            "side_relation": side_relation,
            "activation_level": activation_level if activation_level is not None else 101000,
            "arrival_level": arrival_level if arrival_level is not None else 104000,
            "invalidation_level": invalidation_level if invalidation_level is not None else 99000,
            "market_state": "سياق سوق تحت المتابعة",
            "liquidity_state": "سيولة تحتاج مراقبة",
            "risk_state": "مخاطر سياقية قائمة",
            "volatility_state": "تذبذب قابل للتغير",
            "sentiment_state": "حياد يميل للحذر",
            "decision_quality": "جودة سياقية قابلة للتحسن",
            "caution_reason": "تتم متابعة السيناريو دون اعتبار القراءة أمر تنفيذ.",
            "summary": "قراءة سياقية صادرة من الباك إند."
        }

        return govern_decision_output(payload, package=package)

    app.state.ndsp_frontend_fields_routes_installed = True

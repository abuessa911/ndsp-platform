from copy import deepcopy

from backend.app.core.public_response_sanitizer import (
    sanitize_public_payload,
    public_payload_has_leak,
    should_sanitize_path,
)


def test_sanitizer_removes_forbidden_fields_and_preserves_decision_values():
    raw = {
        "decision": {
            "direction": "bullish",
            "confidence": 81,
            "risk_state": "normal",
            "timing_controller": "S",
            "decision_authority": "timing_controller",
        },
        "tdl": {"version": "2.0"},
        "nmp": {"state": "raw"},
        "public_note": "Decision Environment Updated",
    }
    original = deepcopy(raw)

    safe = sanitize_public_payload(raw)

    assert raw == original
    assert safe["decision"]["direction"] == "bullish"
    assert safe["decision"]["confidence"] == 81
    assert safe["decision"]["risk_state"] == "normal"
    assert "timing_controller" not in safe["decision"]
    assert "decision_authority" not in safe["decision"]
    assert "tdl" not in safe
    assert "nmp" not in safe


def test_sanitizer_replaces_sensitive_terms_in_strings_only():
    raw = {
        "message": "TDL v2 and NMP produced a Buy Signal without Trade Execution.",
        "decision": {"direction": "bearish", "confidence": 55},
    }
    safe = sanitize_public_payload(raw)
    text = str(safe)

    assert "TDL" not in text
    assert "NMP" not in text
    assert "Buy Signal" not in text
    assert "Trade Execution" not in text
    assert "Directional Framework" in text
    assert "Structural Framework" in text
    assert "Positive Market Bias" in text
    assert "User Controlled Action" in text
    assert safe["decision"]["direction"] == "bearish"
    assert safe["decision"]["confidence"] == 55


def test_leak_detector_and_path_policy():
    assert public_payload_has_leak({"tdl": {"x": 1}}) is True
    assert public_payload_has_leak({"message": "Black Layer active"}) is True
    assert public_payload_has_leak({"message": "Decision Environment Updated"}) is False

    assert should_sanitize_path("/decision") is True
    assert should_sanitize_path("/api/v6/decision") is True
    assert should_sanitize_path("/admin") is False
    assert should_sanitize_path("/docs") is False

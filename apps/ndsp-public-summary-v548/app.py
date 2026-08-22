#!/usr/bin/env python3
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import urlopen
import json
import os
import time

BACKEND = "http://127.0.0.1:9084/api/decision/quality-contract-v53"

def label(code):
    if code in ("TIMING_CORRECTION", "CORRECTION"):
        return "CORRECTION", "تصحيح"
    if code in ("NONE", "WITH_TREND", "NO_CORRECTION"):
        return "NO_CORRECTION", "لا يوجد تصحيح"
    return "UNKNOWN", "غير مؤكد"

def view(v):
    v = v or {}
    status, label_ar = label(v.get("correction_type"))
    return {
        "name_ar": v.get("public_name_ar") or "النمط",
        "direction_ar": v.get("controlling_direction_ar") or "غير مؤكد",
        "correction_status": status,
        "correction_ar": label_ar,
        "timing_ar": v.get("decision_timing_label_ar") or "غير مؤكد",
    }

def fetch_raw(symbol):
    url = BACKEND + "?symbol=" + quote(symbol)
    with urlopen(url, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))

def build(symbol):
    raw = fetch_raw(symbol)
    profile = raw.get("decision_profile_direction_contract") or {}
    status, label_ar = label(raw.get("correction_type"))

    return {
        "ok": True,
        "version": "V5.4.8",
        "symbol": (raw.get("instrument") or {}).get("symbol") or symbol,
        "privacy_mode": "PUBLIC_RESULT_ONLY",
        "final_state_ar": ((raw.get("scenario_interpretation") or {}).get("final_state_ar") or "غير مؤكد"),
        "correction": {"status": status, "label_ar": label_ar},
        "investor_view": view(profile.get("investor_view")),
        "tactical_view": view(profile.get("tactical_view")),
        "risk_ar": ((raw.get("radar_nodes") or {}).get("risk") or {}).get("label_ar") or "غير مؤكد",
        "advocate_ar": ((raw.get("radar_nodes") or {}).get("devil") or {}).get("label_ar") or "غير مؤكد",
        "nmp_ar": ((raw.get("radar_nodes") or {}).get("nmp_check") or {}).get("label_ar") or "غير مؤكد",
        "golden_signal_ar": (raw.get("golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "enhanced_golden_signal_ar": (raw.get("enhanced_golden_signal") or {}).get("label_ar") or "غير مؤكد",
        "notice_ar": "قراءة دعم قرار فقط، وليست توصية مالية ولا أمر تنفيذ.",
        "updated_at": int(time.time()),
    }

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path not in ("/api/decision/public-summary", "/api/decision/public-contract-v548", "/health"):
            self.send_json(404, {"ok": False, "error": "not_found"})
            return
        if parsed.path == "/health":
            self.send_json(200, {"ok": True, "service": "ndsp-public-summary-v548"})
            return
        symbol = parse_qs(parsed.query).get("symbol", ["BTCUSDT"])[0].upper()
        try:
            self.send_json(200, build(symbol))
        except Exception as e:
            self.send_json(502, {"ok": False, "error": "upstream_error", "detail": str(e)[:160]})

    def log_message(self, *_):
        return

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(os.getenv("NDSP_PUBLIC_SUMMARY_PORT", "9092"))), Handler).serve_forever()

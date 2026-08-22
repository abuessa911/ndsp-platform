#!/usr/bin/env python3
import json
import time
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


from backend.platform.canonical_v1.live_public_providers import (
    build_live_overview,
    read_authorized_core,
    read_market_context,
    read_public_evidence,
)

PORT = 9002

ASSETS = [
    {"symbol":"BTCUSDT","name_ar":"بيتكوين","name_en":"Bitcoin","category":"CRYPTO"},
    {"symbol":"ETHUSDT","name_ar":"إيثريوم","name_en":"Ethereum","category":"CRYPTO"},
    {"symbol":"SOLUSDT","name_ar":"سولانا","name_en":"Solana","category":"CRYPTO"},
    {"symbol":"XAUUSD","name_ar":"الذهب","name_en":"Gold","category":"METAL"},
    {"symbol":"EURUSD","name_ar":"اليورو / الدولار","name_en":"EUR/USD","category":"FX"},
    {"symbol":"GBPUSD","name_ar":"الجنيه / الدولار","name_en":"GBP/USD","category":"FX"},
    {"symbol":"USOIL","name_ar":"النفط الأمريكي","name_en":"WTI Crude Oil","category":"COMMODITY"},
]

FALLBACK_PRICES = {
    "BTCUSDT": 0,
    "ETHUSDT": 0,
    "SOLUSDT": 0,
    "XAUUSD": 0,
    "EURUSD": 0,
    "GBPUSD": 0,
    "USOIL": 0,
}

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def live_quality(symbol):
    url = "https://api.ndsp.app/api/decision/quality-live?symbol=" + urllib.parse.quote(symbol)
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"ndsp-9002-recovery/1.0"})
        with urllib.request.urlopen(req, timeout=2.5) as r:
            if r.status != 200:
                return None
            return json.loads(r.read().decode("utf-8", "ignore"))
    except Exception:
        return None

def asset_payload(symbol):
    symbol = (symbol or "BTCUSDT").upper()
    q = live_quality(symbol) or {}
    inst = q.get("instrument") or {}
    scenario = q.get("scenario") or {}

    price = inst.get("live_price")
    if price is None:
        price = FALLBACK_PRICES.get(symbol, 0)

    return {
        "ok": True,
        "source_mode": "ndsp_platform_gateway_9002_recovery",
        "live_probe": bool(q),
        "asset": {
            "symbol": symbol,
            "name_ar": next((a["name_ar"] for a in ASSETS if a["symbol"] == symbol), symbol),
            "category": next((a["category"] for a in ASSETS if a["symbol"] == symbol), "UNKNOWN"),
            "live_price": price,
            "market": inst.get("market") or next((a["category"] for a in ASSETS if a["symbol"] == symbol), "UNKNOWN"),
            "timeframe": inst.get("timeframe") or "UNSPECIFIED",
            "updated_at": now_iso(),
        },
        "decision": {
            "scenario_state": scenario.get("scenario_state") or q.get("scenario_state") or "UNDER_MONITORING",
            "directional_context": scenario.get("scenario_directional_context") or q.get("directional_context") or "قراءة تحت المراقبة",
            "decision_quality": q.get("decision_quality") or q.get("quality") or None,
            "caution_reason": q.get("caution_reason") or "دعم قرار فقط — ليست توصية مالية أو دعوة لاتخاذ إجراء.",
        },
        "reference_levels": {
            "activation": scenario.get("scenario_activation_level"),
            "arrival": scenario.get("scenario_arrival_level"),
            "review": scenario.get("scenario_review_zone"),
            "invalidation": scenario.get("scenario_invalidation_level"),
        },
        "governance": {
            "message": "NDSP is a decision-support platform, not a trading or recommendation platform.",
            "ar": "منصة دعم قرار فقط — ليست منصة تداول ولا توصية مالية.",
        }
    }

def assets_payload():
    out = []
    for a in ASSETS:
        q = live_quality(a["symbol"]) or {}
        inst = q.get("instrument") or {}
        scenario = q.get("scenario") or {}
        out.append({
            **a,
            "live_price": inst.get("live_price", FALLBACK_PRICES.get(a["symbol"], 0)),
            "scenario_state": scenario.get("scenario_state") or "UNDER_MONITORING",
            "quality": q.get("decision_quality") or q.get("quality") or None,
            "updated_at": now_iso(),
            "source": "quality_live_probe" if q else "gateway_recovery",
        })
    return {
        "ok": True,
        "source_mode": "ndsp_platform_gateway_9002_recovery",
        "count": len(out),
        "assets": out,
        "updated_at": now_iso(),
    }

def trial_status():
    return {
        "ok": True,
        "source_mode": "ndsp_platform_gateway_9002_recovery",
        "trial": {
            "enabled": True,
            "duration_days": 16,
            "status": "ACTIVE",
            "registration_endpoint": "/api/trial/register/ordinary",
        },
        "message": "NDSP trial gateway is reachable.",
        "updated_at": now_iso(),
    }

def completed_decisions():
    return {
        "ok": True,
        "source_mode": "ndsp_platform_gateway_9002_recovery",
        "items": [],
        "message": "No completed decision ledger items exposed from recovery gateway.",
        "updated_at": now_iso(),
    }

def daily_brief():
    return {
        "ok": True,
        "source_mode": "ndsp_platform_gateway_9002_recovery",
        "brief": {
            "title": "الإيجاز اليومي",
            "summary": "المصدر المحلي عاد للعمل. يتم عرض قراءة دعم قرار فقط دون توصيات أو أوامر.",
            "status": "ACTIVE",
        },
        "updated_at": now_iso(),
    }

class Handler(BaseHTTPRequestHandler):
    server_version = "NDSP9002/1.0"

    def _send(self, code, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = urllib.parse.parse_qs(parsed.query)
        symbol = (qs.get("symbol") or ["BTCUSDT"])[0].upper()

        if path in ["/", "/api/status", "/status", "/health"]:
            return self._send(200, {
                "ok": True,
                "service": "ndsp-platform-gateway-9002",
                "status": "LISTENING",
                "port": PORT,
                "updated_at": now_iso(),
            })

        if path == "/api/public/overview":
            return self._send(
                200,
                build_live_overview(),
            )

        if path == "/api/public/core":
            core_result = read_authorized_core()

            if not core_result.available or core_result.payload is None:
                return self._send(
                    503,
                    {
                        "ok": False,
                        "error": "public_core_temporarily_unavailable",
                    },
                )

            return self._send(
                200,
                core_result.payload,
            )

        if path == "/api/public/market-context":
            market_result = read_market_context()

            if not market_result.available or market_result.payload is None:
                return self._send(
                    503,
                    {
                        "ok": False,
                        "error": "public_market_context_temporarily_unavailable",
                    },
                )

            return self._send(
                200,
                market_result.payload,
            )

        if path == "/api/public/evidence":
            evidence_result = read_public_evidence()

            if not evidence_result.available or evidence_result.payload is None:
                return self._send(
                    503,
                    {
                        "ok": False,
                        "error": "public_evidence_temporarily_unavailable",
                    },
                )

            return self._send(
                200,
                evidence_result.payload,
            )

        if path == "/api/trial/status":
            return self._send(200, trial_status())

        if path == "/api/ndsp/assets":
            return self._send(200, assets_payload())

        if path.startswith("/api/ndsp/decision/"):
            sym = path.split("/")[-1].upper()
            return self._send(200, asset_payload(sym))

        if path.startswith("/api/ndsp/asset/"):
            sym = path.split("/")[-1].upper()
            return self._send(200, asset_payload(sym))

        if path == "/api/ndsp/completed-decisions":
            return self._send(200, completed_decisions())

        if path == "/api/ndsp/daily-brief":
            return self._send(200, daily_brief())

        if path == "/api/ndsp/settings":
            return self._send(200, {
                "ok": True,
                "settings": {
                    "language": "ar",
                    "risk_radar": True,
                    "notifications": False,
                    "governance_disclaimer": True,
                },
                "updated_at": now_iso(),
            })

        return self._send(404, {
            "ok": False,
            "error": "NOT_FOUND",
            "path": path,
            "service": "ndsp-platform-gateway-9002",
        })

    def log_message(self, fmt, *args):
        return

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"NDSP 9002 recovery gateway listening on 127.0.0.1:{PORT}", flush=True)
    server.serve_forever()

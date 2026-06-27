#!/usr/bin/env python3
import json
import os
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

UPSTREAM = os.environ.get("NDSP_QUALITY_LIVE_UPSTREAM", "http://127.0.0.1:9057").rstrip("/")
HOST = os.environ.get("NDSP_GOLDEN_WRAPPER_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_GOLDEN_WRAPPER_PORT", "9067"))

RUNTIME = Path("/home/nawaf511/empire-core-new/backend/runtime")
TDL_FILES = [
    RUNTIME / "tdl_active_direction.json",
    RUNTIME / "tdl_ml_direction.json",
]

def now_ms():
    return int(time.time() * 1000)

def safe_text(v, default="غير معلن"):
    if v is None:
        return default
    s = str(v).strip()
    return s if s else default

def flatten(obj):
    rows = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            rows.append((str(k), v))
            rows.extend(flatten(v))
    elif isinstance(obj, list):
        for v in obj:
            rows.extend(flatten(v))
    return rows

def find_first(obj, key_patterns):
    pats = [p.lower() for p in key_patterns]
    for k, v in flatten(obj):
        lk = k.lower()
        if any(p in lk for p in pats):
            if isinstance(v, (str, int, float, bool)) and str(v).strip() != "":
                return v
    return None

def parse_quality(v):
    try:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.replace("%", "").replace("٪", "").strip()
        q = float(v)
        if q <= 1:
            q *= 100
        return max(0.0, min(100.0, q))
    except Exception:
        return None

def truthy(v):
    if isinstance(v, bool):
        return v
    if v is None:
        return None
    s = str(v).strip().lower()
    if s in {"true", "1", "yes", "active", "enabled", "golden", "complete", "completed"}:
        return True
    if s in {"false", "0", "no", "inactive", "disabled", "none", "null"}:
        return False
    return None

def load_runtime_golden(symbol):
    result = {}
    for p in TDL_FILES:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue

        blob_symbol = safe_text(find_first(data, ["symbol", "asset"]), "").upper()
        if blob_symbol and symbol and blob_symbol not in {symbol.upper(), symbol.upper().replace("USDT", "")}:
            pass

        sig = find_first(data, ["golden_signal", "golden_alignment_active"])
        name = find_first(data, ["golden_name"])
        boost = find_first(data, ["golden_boost"])
        version = find_first(data, ["version"])

        if sig is not None:
            result["golden_signal"] = truthy(sig)
        if name is not None:
            result["golden_name"] = safe_text(name, "")
        if boost is not None:
            result["golden_boost"] = truthy(boost)
        if version is not None:
            result["version"] = safe_text(version, "")
    return result

def inject_golden(data, symbol):
    if not isinstance(data, dict):
        return data

    q = parse_quality(find_first(data, [
        "decision_quality", "quality_score", "quality", "dq", "score"
    ]))

    scenario_state = safe_text(find_first(data, [
        "scenario_state", "scenario_status", "decision_state", "state", "status"
    ]), "غير معلن")

    direction = safe_text(find_first(data, [
        "directional_context", "direction", "trend", "bias", "market_state"
    ]), "غير معلن")

    caution = safe_text(find_first(data, [
        "caution_reason", "risk_note", "scenario_risk_note", "guard_reason", "warning"
    ]), "")

    existing_signal = truthy(find_first(data, [
        "golden_signal", "golden_alignment_active"
    ]))

    runtime = load_runtime_golden(symbol)
    runtime_signal = runtime.get("golden_signal", None)

    raw_blob = json.dumps(data, ensure_ascii=False).lower()
    blocked_terms = [
        "blocked", "محجوب", "ممنوع", "تحت المعالجة", "under_processing",
        "halted", "disabled", "not allowed"
    ]
    blocked = any(t in raw_blob for t in blocked_terms)

    active = False
    if runtime_signal is True or existing_signal is True:
        active = True

    if blocked:
        status = "blocked"
    elif active:
        status = "active"
    elif q is not None and q >= 65:
        status = "partial"
    else:
        status = "inactive"

    if status == "active":
        reason = "تحققت محاذاة سياقية عالية الجودة ضمن قراءة NDSP المحكومة. هذه إشارة جودة وليست أمر شراء أو بيع."
        label = "مفعّلة"
    elif status == "partial":
        reason = "بعض شروط المحاذاة عالية الجودة متوفرة، لكن الإشارة لم تكتمل بالكامل لهذا الأصل."
        label = "جزئية / تحت المراقبة"
    elif status == "blocked":
        reason = "الإشارة محجوبة حوكميًا أو غير قابلة للتفعيل بسبب حالة القراءة الحالية."
        label = "محجوبة حوكميًا"
    else:
        reason = "لم تكتمل شروط إشارة نواف الذهبية لهذا الأصل حاليًا."
        label = "غير مفعّلة"

    evidence = [
        {
            "label": "جودة القرار",
            "value": "غير معلنة" if q is None else f"{round(q)} / 100"
        },
        {
            "label": "حالة السيناريو",
            "value": scenario_state
        },
        {
            "label": "سياق الاتجاه",
            "value": direction
        }
    ]

    if caution:
        evidence.append({
            "label": "سبب التحفظ",
            "value": caution
        })

    golden = {
        "golden_signal": bool(active),
        "golden_alignment_active": bool(active),
        "golden_status": status,
        "golden_label_public": label,
        "golden_name": runtime.get("golden_name") or "NDSP_GOLDEN_ALIGNMENT",
        "golden_name_public": "إشارة نواف الذهبية",
        "golden_reason_public": reason,
        "golden_evidence_public": evidence,
        "golden_effect_public": "معزّز لجودة القرار فقط، وليس توصية مالية ولا أمر تنفيذ.",
        "not_recommendation": True,
        "no_buy_sell": True,
        "protected_layers_masked": True,
        "source_mode": "quality_live_governed_output_runtime_alignment",
        "wrapper_version": "1.0.0-ndsp-golden-explainability"
    }

    data["golden_signal"] = golden["golden_signal"]
    data["golden_alignment_active"] = golden["golden_alignment_active"]
    data["golden_status"] = golden["golden_status"]
    data["golden_name"] = golden["golden_name"]
    data["golden_reason_public"] = golden["golden_reason_public"]
    data["golden_evidence_public"] = golden["golden_evidence_public"]
    data["golden_alignment"] = golden
    data["golden_spotlight"] = {
        "title": "إشارة نواف الذهبية",
        "status": status,
        "label": label,
        "summary": reason,
        "quality_effect": golden["golden_effect_public"],
        "evidence": evidence
    }

    explain = data.get("explainability")
    if not isinstance(explain, dict):
        explain = {}

    explain["golden_signal_exposed"] = True
    explain["golden_signal"] = bool(active)
    explain["golden_status"] = status
    explain["golden_reason_public"] = reason
    explain["evidence_trace"] = True
    explain["reason_codes"] = True
    explain["engine_coverage"] = "masked_public_trace"
    explain["protected_layers_masked"] = True
    explain["no_internal_formula_exposure"] = True
    explain["not_recommendation"] = True

    data["explainability"] = explain

    public_explainability = data.get("public_explainability")
    if not isinstance(public_explainability, dict):
        public_explainability = {}

    public_explainability["golden_alignment"] = {
        "title": "إشارة نواف الذهبية",
        "status": status,
        "label": label,
        "reason": reason,
        "evidence": evidence,
        "notice": "هذه قراءة سياقية داعمة لجودة القرار فقط، وليست توصية مالية."
    }

    data["public_explainability"] = public_explainability
    data["_ndsp_golden_explainability_injected_at_ms"] = now_ms()

    return data

class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPGoldenExplainabilityWrapper/1.0"

    def log_message(self, fmt, *args):
        return

    def _headers(self, code=200, ctype="application/json; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        url = UPSTREAM + self.path

        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=20) as r:
                code = getattr(r, "status", 200)
                body = r.read()
                ctype = r.headers.get("Content-Type", "application/json")
        except HTTPError as e:
            code = e.code
            body = e.read()
            ctype = e.headers.get("Content-Type", "application/json")
        except URLError as e:
            self._headers(502)
            self.wfile.write(json.dumps({
                "ok": False,
                "error": "upstream_unreachable",
                "detail": str(e),
                "golden_signal": False,
                "golden_status": "blocked",
                "golden_reason_public": "تعذر الوصول لمصدر القراءة الحي مؤقتًا."
            }, ensure_ascii=False).encode("utf-8"))
            return

        symbol = "ETHUSDT"
        try:
            from urllib.parse import parse_qs
            qs = parse_qs(parsed.query)
            symbol = (qs.get("symbol") or qs.get("asset") or ["ETHUSDT"])[0]
        except Exception:
            pass

        try:
            data = json.loads(body.decode("utf-8", errors="ignore"))
            if isinstance(data, dict):
                data = inject_golden(data, symbol)
                body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
                ctype = "application/json; charset=utf-8"
        except Exception:
            pass

        self._headers(code, ctype)
        self.wfile.write(body)

def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"NDSP Golden Explainability Wrapper listening on {HOST}:{PORT}, upstream={UPSTREAM}", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    main()

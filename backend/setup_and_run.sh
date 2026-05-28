#!/usr/bin/env bash
set -Eeuo pipefail

echo "============================================================="
echo "NDSP V4.1 - Production Setup Script (Fixed Version)"
echo "Author: NDSP Architect"
echo "============================================================="

echo ""
echo "1. تنظيف البيئة من أي مخلفات سابقة"
echo "Cleaning old artifacts"
echo "------------------------------------------------"
echo "NDSP System: Starting Clean Installation..."
echo "------------------------------------------------"

rm -f ndsp_contract.py direction_engine.py quality_stack.py

echo ""
echo "2. التأكد من المكتبات المطلوبة"
echo "Dependency Check"
echo "------------------------------------------------"
echo "[1/4] Checking Pydantic..."

python3 -m pip install pydantic --quiet

echo ""
echo "3. توليد عقد القرار Decision Contract"
echo "Generating the Decision Contract Model"
echo "------------------------------------------------"

cat > ndsp_contract.py <<'PY'
#!/usr/bin/env python3
import sys
from typing import List

from pydantic import BaseModel, Field


class NDSPDecisionContract(BaseModel):
    trace_id: str
    symbol: str
    timestamp: str
    session_state: str
    dominant_direction: str = Field(..., pattern="^(bullish|bearish|neutral)$")
    direction_source: str
    timing_controller: str
    confidence_score: float = Field(default=0.0, ge=0, le=100)
    grade: str = "D"
    applied_effects: List[str] = Field(default_factory=list)
    risk_state: str = "Normal"
    decision_state: str = "Blocked"
    execution_allowed: bool = False


if __name__ == "__main__":
    example_data = {
        "trace_id": "NDSP-V4.1-STABLE",
        "symbol": "BTCUSDT",
        "timestamp": "2023-10-27T10:00:00Z",
        "session_state": "Open",
        "dominant_direction": "bullish",
        "direction_source": "Weekly_LM",
        "timing_controller": "L&M",
        "confidence_score": 88.5,
        "grade": "A",
        "applied_effects": ["Golden_Alignment"],
        "risk_state": "Normal",
        "decision_state": "Ready",
        "execution_allowed": False,
    }

    try:
        contract = NDSPDecisionContract(**example_data)
        print("\n[SUCCESS] Contract Integrity Validated:")
        print(contract.model_dump_json(indent=2))
    except Exception as exc:
        print(f"\n[ERROR] Validation Failed: {exc}")
        sys.exit(1)
PY

echo ""
echo "4. توليد محرك الاتجاه Direction Engine"
echo "Generating the Direction Engine"
echo "------------------------------------------------"

cat > direction_engine.py <<'PY'
#!/usr/bin/env python3
import json
from typing import Tuple


def calculate_direction(controller: str, lm_dir: str, s_dir: str) -> Tuple[str, str]:
    if controller == "L&M":
        return lm_dir, "Weekly_LM"

    return s_dir, "Weekly_S"


if __name__ == "__main__":
    res_dir, res_source = calculate_direction("L&M", "bullish", "bearish")
    print(json.dumps({"direction": res_dir, "source": res_source}, indent=2))
PY

echo ""
echo "5. توليد مجمع الجودة Quality Stack"
echo "Generating the Quality Stack"
echo "------------------------------------------------"

cat > quality_stack.py <<'PY'
#!/usr/bin/env python3
import json


def get_grade(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


if __name__ == "__main__":
    score = 88.5
    print(json.dumps({"score": score, "grade": get_grade(score)}, indent=2))
PY

echo ""
echo "6. ضبط الصلاحيات والتشغيل النهائي"
echo "Final Permissions and Execution"
echo "------------------------------------------------"

chmod +x ndsp_contract.py direction_engine.py quality_stack.py

echo ""
echo "[2/4] Files generated successfully."
echo "[3/4] Running internal integrity tests..."
echo "------------------------------------------------"

python3 ndsp_contract.py

echo "------------------------------------------------"
python3 direction_engine.py

echo "------------------------------------------------"
python3 quality_stack.py

echo "------------------------------------------------"
echo "[4/4] Setup Process Completed."
echo "FINAL_STATUS=NDSP_V4_1_SETUP_COMPLETED"

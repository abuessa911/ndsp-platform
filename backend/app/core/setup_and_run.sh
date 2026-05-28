#!/bin/bash

1. تنظيف شامل وإعادة تهيئة

echo "Cleaning up files..."
rm -f ndsp_contract.py direction_engine.py quality_stack.py

2. حل جذري لمشكلة NVM و NPM Prefix

echo "Fixing Node/NVM configuration..."

إزالة الـ prefix الذي يعطل عمل nvm

npm config delete prefix 2>/dev/null
npm config set prefix $HOME/.npm-global 2>/dev/null
nvm use --delete-prefix v24.15.0 --silent

3. إنشاء ملف ndsp_contract.py مع ضمان المسافات

echo "Generating ndsp_contract.py..."
cat << 'EOF' > ndsp_contract.py
#!/usr/bin/env python3
from pydantic import BaseModel, Field
from typing import List
import json
import sys

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
applied_effects: List[str] = []
risk_state: str = "Normal"
decision_state: str = "Blocked"
execution_allowed: bool = False

if name == "main":
example_data = {
"trace_id": "NDSP-12345", "symbol": "BTCUSDT", "timestamp": "2023-10-27T10:00:00Z",
"session_state": "Open", "dominant_direction": "bullish", "direction_source": "Weekly_LM",
"timing_controller": "L&M", "confidence_score": 85.5, "grade": "A",
"applied_effects": ["Golden_Alignment"], "risk_state": "Normal",
"decision_state": "Ready", "execution_allowed": False
}
try:
contract = NDSPDecisionContract(example_data)
print(f"Contract Validated: {contract.json(indent=2)}")
except Exception as e:
print(f"Contract Error: {e}")
sys.exit(1)
EOF

4. إنشاء ملف direction_engine.py

echo "Generating direction_engine.py..."
cat << 'EOF' > direction_engine.py
#!/usr/bin/env python3
import json

def calculate_dominant_direction(timing_data, tdl_data):
controller = timing_data.get('controller')
if controller == "L&M":
return tdl_data.get('weekly_lm_direction'), "Weekly_LM"
return tdl_data.get('weekly_s_direction'), "Weekly_S"

if name == "main":
sample_timing = {"controller": "L&M"}
sample_tdl = {"weekly_lm_direction": "bullish", "weekly_s_direction": "bearish"}
direction, source = calculate_dominant_direction(sample_timing, sample_tdl)
print(json.dumps({"dominant_direction": direction, "direction_source": source}))
EOF

5. إنشاء ملف quality_stack.py

echo "Generating quality_stack.py..."
cat << 'EOF' > quality_stack.py
#!/usr/bin/env python3
import json

def apply_quality_logic(base_confidence, effects, direction):
score = base_confidence
applied = []
if effects.get('golden_alignment'):
score += 15
applied.append("Golden_Alignment_Boost")
if effects.get('price_above_weekly_open') and direction == "bullish":
score += 10
applied.append("Weekly_Open_Support")
final_score = max(0, min(score, 100))
grade = "A" if final_score >= 85 else "B" if final_score >= 70 else "C" if final_score >= 50 else "D"
return final_score, applied, grade

if name == "main":
final_s, applied_list, final_g = apply_quality_logic(60, {"golden_alignment": True, "price_above_weekly_open": True}, "bullish")
print(json.dumps({"final_confidence": final_s, "grade": final_g, "applied": applied_list}, indent=2))
EOF

6. ضبط الصلاحيات والتشغيل

chmod +x ndsp_contract.py direction_engine.py quality_stack.py

echo -e "\n------------------------------------------------"
echo "Running Validations..."
echo "------------------------------------------------"

echo "[1/3] Testing Direction Engine..."
python3 direction_engine.py

echo -e "\n[2/3] Testing Quality Stack..."
python3 quality_stack.py

echo -e "\n[3/3] Validating Final Event Contract..."
python3 ndsp_contract.py

echo -e "\n------------------------------------------------"
echo "Process Completed."
echo "------------------------------------------------"

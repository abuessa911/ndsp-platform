# PR-062 COT Direction and Time Backend Audit

Read-only audit of backend COT direction, timing, category, CORE/EXPANDED, and result-integration logic.

Run:

```bash
python3 scripts/governance/build_pr062_cot_direction_time_backend_audit.py .
python3 scripts/governance/validate_pr062_cot_direction_time_backend_audit.py .
node --test scripts/governance/tests/pr062-cot-direction-time-backend-audit.test.cjs
```

============================================================
NDSP — COT MODE ACTIVATION V1
MODE=OFFICIAL_DATA_REFRESH_THEN_FRONTEND_CONTRACT_ACTIVATION
DATE=2026-07-26T08:34:57+02:00
CORE=/home/nawaf511/empire-core-new
============================================================

== 1) Strict preflight ==
TOOL_bash=PASS
TOOL_curl=PASS
TOOL_python3=PASS
TOOL_jq=PASS
TOOL_sha256sum=PASS
TOOL_systemctl=PASS
TOOL_tar=PASS
TOOL_stat=PASS
RAW_SERVICE_ACTIVE=YES
FINAL_SERVICE_ACTIVE=YES
RAW_HEALTH_HTTP=200
RAW_DATA_DIR=/home/nawaf511/empire-core-new/backend/data/raw_cot

== 2) Backup current raw COT runtime data ==
RAW_BEFORE_BTCUSDT_HTTP=200
RAW_BEFORE_ETHUSDT_HTTP=200
RAW_DATA_BACKUP_GATE=PASS
BACKUP=/home/nawaf511/empire-core-new/backups/cot-mode-activation-v1/20260726_083456

== 3) Qualify current official CFTC TFF file ==
OFFICIAL_COT_GATE=PASS symbol=BTCUSDT report_date=2026-07-21 age_days=5 am_overall=bullish am_weekly=bearish lf_weekly=bearish
OFFICIAL_COT_GATE=PASS symbol=ETHUSDT report_date=2026-07-21 age_days=5 am_overall=bearish am_weekly=bearish lf_weekly=bullish
OFFICIAL_CFTC_TFF_QUALIFICATION_GATE=PASS
OFFICIAL_REPORT_DATE=2026-07-21

== 4) Import current official COT data through canonical gateway ==
RAW_IMPORT_CURRENT_HTTP=200
RAW_IMPORT_RESPONSE_GATE=PASS

== 5) Validate canonical COT fields after import ==
RAW_AFTER_BTCUSDT_HTTP=200
RAW_CANONICAL_GATE=PASS symbol=BTCUSDT report_date=2026-07-21 age_days=5 am_overall=bullish am_weekly=bearish lf_weekly=bearish
RAW_AFTER_ETHUSDT_HTTP=200
RAW_CANONICAL_GATE=PASS symbol=ETHUSDT report_date=2026-07-21 age_days=5 am_overall=bearish am_weekly=bearish lf_weekly=bullish
RAW_COT_REFRESH_GATE=PASS

== 6) Validate V203 mode contract after fresh COT ==
FINAL_BTCUSDT_1h_speculative_HTTP=200
V203_MODE_GATE=PASS context=BTCUSDT_1h_speculative mode=speculative direction=bearish score=71.88 status=CALCULATED_GOVERNED
FINAL_BTCUSDT_1h_investment_HTTP=200
V203_MODE_GATE=PASS context=BTCUSDT_1h_investment mode=investment direction=bullish score=68.37 status=CALCULATED_GOVERNED
FINAL_BTCUSDT_weekly_investment_HTTP=200
V203_MODE_GATE=PASS context=BTCUSDT_weekly_investment mode=investment direction=bullish score=64.34 status=CALCULATED_GOVERNED
MODE_OUTPUT_DIFFERENCE_GATE=PASS spec_direction=bearish investment_direction=bullish spec_score=71.88 investment_score=68.37
V203_FRESH_MODE_CONTRACT_GATE=PASS

== 7) Activate authoritative frontend consumption ==
AUTHORITATIVE_FRONTEND_ACTIVATION_GATE=PASS

FINAL_STATUS=NDSP_COT_MODE_ACTIVATION_V1_COMPLETE
OFFICIAL_REPORT_DATE=2026-07-21
RAW_COT_REFRESHED=YES
V203_MODE_CONTRACT_READY=YES
AUTHORITATIVE_FRONTEND_ACTIVATED=YES
BACKEND_SOURCE_CHANGED=NO
BACKEND_RUNTIME_DATA_CHANGED=YES
SERVICE_RESTARTED=NO
NGINX_CHANGED=NO
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COT_MODE_ACTIVATION_V1_20260726_083456.md
BACKUP=/home/nawaf511/empire-core-new/backups/cot-mode-activation-v1/20260726_083456

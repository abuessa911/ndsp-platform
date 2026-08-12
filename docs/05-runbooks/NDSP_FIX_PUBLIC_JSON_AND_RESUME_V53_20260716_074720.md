# NDSP Fix Public JSON And Resume V53

- Date: 2026-07-16T07:47:20+02:00
- Project: /home/nawaf511/empire-core-new
- Live: /var/www/ndsp-my
- Portal: v50
- Mode: EXACT_JSON_STATIC_LOCATIONS_OPTIONAL_QUALITY_BRIDGE_RESUME_GATE
- Backup: /home/nawaf511/ndsp_launch_backups/fix_public_json_and_resume_v53_20260716_074720
- Output: /home/nawaf511/ndsp_launch_reports/NDSP_FIX_PUBLIC_JSON_AND_RESUME_V53_20260716_074720
- Report: /home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_FIX_PUBLIC_JSON_AND_RESUME_V53_20260716_074720.md

== 1) Diagnose the public responses that stopped V52 ==
PROBE_QUALITY_BEFORE_HTTP=200
PROBE_QUALITY_BEFORE_CONTENT_TYPE=application/json; charset=utf-8
PROBE_QUALITY_BEFORE_JSON=YES
PROBE_QUALITY_BEFORE_TOP_KEYS=ok,source_mode,project,package,instrument,scenario,allowed_public_outputs,live_market_analysis,live_price_bound,data_provider,provider_sources,generated_at
PROBE_ASSETS_BEFORE_HTTP=200
PROBE_ASSETS_BEFORE_CONTENT_TYPE=application/json
PROBE_ASSETS_BEFORE_JSON=YES
PROBE_ASSETS_BEFORE_TOP_KEYS=document_id,normalized_by,source_file,market_count,asset_count,markets
PROBE_LAYERS_BEFORE_HTTP=403
PROBE_LAYERS_BEFORE_CONTENT_TYPE=text/html
PROBE_LAYERS_BEFORE_JSON=NO
PROBE_LAYERS_BEFORE_ERROR=JSONDecodeError: Expecting value: line 1 column 1 (char 0)
PROBE_LAYERS_BEFORE_PREFIX=<html>  <head><title>403 Forbidden</title></head>  <body>  <center><h1>403 Forbidden</h1></center>  <hr><center>nginx/1.24.0 (Ubuntu)</center>  </body>  </html>  
PROBE_CAPABILITIES_BEFORE_HTTP=403
PROBE_CAPABILITIES_BEFORE_CONTENT_TYPE=text/html
PROBE_CAPABILITIES_BEFORE_JSON=NO
PROBE_CAPABILITIES_BEFORE_ERROR=JSONDecodeError: Expecting value: line 1 column 1 (char 0)
PROBE_CAPABILITIES_BEFORE_PREFIX=<html>  <head><title>403 Forbidden</title></head>  <body>  <center><h1>403 Forbidden</h1></center>  <hr><center>nginx/1.24.0 (Ubuntu)</center>  </body>  </html>  

== 2) Normalize static file permissions ==
BACKUP: /var/www/ndsp-my/portal-v50/config
OK: static JSON permissions normalized.

== 3) Locate the active HTTPS Nginx server ==
ACTIVE_CONF=/etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf
BACKUP: /etc/nginx/conf.d/000-000-my-ndsp-app-clean-golden.conf

== 4) Public quality endpoint already returns JSON ==
No quality proxy change is required.

== 5) Install exact JSON locations without touching landing/auth ==
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
OK: nginx -t passed.
OK: Nginx reloaded.

== 6) Verify all public contracts as real JSON ==
PROBE_QUALITY_AFTER_HTTP=200
PROBE_QUALITY_AFTER_CONTENT_TYPE=application/json; charset=utf-8
PROBE_QUALITY_AFTER_JSON=YES
PROBE_QUALITY_AFTER_TOP_KEYS=ok,source_mode,project,package,instrument,scenario,allowed_public_outputs,live_market_analysis,live_price_bound,data_provider,provider_sources,generated_at
PROBE_ASSETS_AFTER_HTTP=200
PROBE_ASSETS_AFTER_CONTENT_TYPE=application/json
PROBE_ASSETS_AFTER_JSON=YES
PROBE_ASSETS_AFTER_TOP_KEYS=document_id,normalized_by,source_file,market_count,asset_count,markets
PROBE_LAYERS_AFTER_HTTP=200
PROBE_LAYERS_AFTER_CONTENT_TYPE=application/json
PROBE_LAYERS_AFTER_JSON=YES
PROBE_LAYERS_AFTER_TOP_KEYS=document_id,version,status,effective_date,notes,families,layers
PROBE_CAPABILITIES_AFTER_HTTP=200
PROBE_CAPABILITIES_AFTER_CONTENT_TYPE=application/json
PROBE_CAPABILITIES_AFTER_JSON=YES
PROBE_CAPABILITIES_AFTER_TOP_KEYS=registry_id,version,governing_rule,decision_layer_registry,capabilities
QUALITY_SYMBOL=ETHUSDT
QUALITY_TIMEFRAME=weekly
LIVE_LAYER_COUNT=16
LIVE_CAPABILITY_COUNT=28

== 7) Resume the comprehensive V52 browser gate with safe JSON diagnostics ==
node:internal/modules/cjs/loader:1450
  throw err;
  ^

Error: Cannot find module 'playwright'
Require stack:
- /tmp/ndsp_resume_comprehensive_gate_v53_20260716_074720.js
    at Function._resolveFilename (node:internal/modules/cjs/loader:1447:15)
    at defaultResolveImpl (node:internal/modules/cjs/loader:1057:19)
    at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1062:22)
    at Function._load (node:internal/modules/cjs/loader:1233:25)
    at wrapModuleLoad (node:internal/modules/cjs/loader:256:19)
    at Module.require (node:internal/modules/cjs/loader:1544:12)
    at require (node:internal/modules/helpers:147:16)
    at Object.<anonymous> (/tmp/ndsp_resume_comprehensive_gate_v53_20260716_074720.js:3:22)
    at Module._compile (node:internal/modules/cjs/loader:1798:14)
    at Object..js (node:internal/modules/cjs/loader:1930:10) {
  code: 'MODULE_NOT_FOUND',
  requireStack: [ '/tmp/ndsp_resume_comprehensive_gate_v53_20260716_074720.js' ]
}

Node.js v22.23.1

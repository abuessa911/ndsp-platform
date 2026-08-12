# NDSP V1.8 / P8-D2 Golden Visual Skin Preview Fixed
DATE=2026-07-09T13:07:49+02:00
MODE=ISOLATED_VISUAL_PREVIEW_ONLY_D2_FIXED_ABSOLUTE_REPORT_PATH
ZIP_SOURCE=/tmp/ndsp_v18_golden_skin_source.zip
PREVIEW_DIR=/var/www/ndsp-my/v18-golden-preview
NO_NGINX_CHANGE=1
NO_API_CHANGE=1
NO_PM2_RESTART=1
NO_PRODUCTION_BUILD_CHANGE=1
NO_REBOOT=1
NO_SERVICE_CONTROL=1
NO_PROTECTED_ASSET_CHANGE=1
NO_DB_SCHEMA_CHANGE=1
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V18_P8_D2_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_130749.md
BACKUP=/home/nawaf511/ndsp_backups/NDSP_V18_P8_D2_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_130749
PACKAGE=/home/nawaf511/ndsp_release_packages/NDSP_V18_P8_D2_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_PACKAGE_20260709_130749.tar.gz

## 1) Required P7 final lock
V17_P7_FINAL_LOCK=OK

## 2) Preflight runtime
FAILED_UNITS_COUNT_BEFORE=0
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
NGINX_ACTIVE_BEFORE=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
PM2_ACTIVE_BEFORE=active
PM2_ENABLED_BEFORE=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3406     │ 13h    │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 75.8mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m11.6%[39m | [1mram usage[22m: [32m8.2%[39m | [1mlo[22m: ⇓ [32m0.002mb/s[39m ⇑ [32m0.002mb/s[39m | [1meth0[22m: ⇓ [32m0.025mb/s[39m ⇑ [32m0.002mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.349mb/s[39m [90m/[39m [1m[33m82.45%[39m[22m |
MARKET_UPDATER_SERVICE_FAILED_BEFORE=inactive

## 3) Baseline endpoints
HTTP_BASE_completed_live=200
HTTP_BASE_api_health=200
HTTP_BASE_quality_live=200
HTTP_BASE_launch_readiness=200
HTTP_BASE_my_home=200
HTTP_BASE_release_registry=200
HTTP_BASE_architecture_map=200
HTTP_BASE_v16_completed=200
BASE_ENDPOINTS_OK=1

## 4) Backup existing preview if any
BACKUP_PREVIEW=NO_EXISTING_PREVIEW

## 5) Extract and detect Vite project
DETECTED_PROJECT_DIR=/tmp/NDSP_V18_P8_D2_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_130749/extract/empire-core-ndip
WORKING_PROJECT=/tmp/NDSP_V18_P8_D2_GOLDEN_VISUAL_SKIN_PREVIEW_FIXED_20260709_130749/work/source

## 6) Apply NDSP golden skin patch
PATCHED=src/index.css CHANGED=1
PATCHED=src/index.css APPENDED_GOLDEN_RADAR_CSS=1
PATCHED=src/App.css CHANGED=1
PATCHED=vite.config.ts BASE=/v18-golden-preview/
PATCHED=src/pages/PhaseEngine.tsx RADIAL_CLEAN=1
TEXT_CLEANED=src/pages/Governance.tsx
TEXT_CLEANED=src/pages/DataInfra.tsx
TEXT_CLEANED=src/pages/Architecture.tsx
TEXT_CLEANED=src/pages/StrategyLab.tsx
TEXT_CLEANED=src/pages/Decisions.tsx
TEXT_CLEANED=src/pages/Index.tsx
TEXT_CLEANED=src/components/ui/sidebar.tsx
TEXT_CLEANED=src/components/ui/StateBadges.tsx
TEXT_CLEANED=src/components/layout/AppLayout.tsx
TEXT_CLEANED=src/data/mockData.ts
PATCH_NOTES_CREATED=1

## 7) Build preview
NODE_VERSION=v22.22.2
NPM_VERSION=10.9.8
NPM_INSTALL_MODE=npm_ci
npm error code EUSAGE
npm error
npm error `npm ci` can only install packages when your package.json and package-lock.json or npm-shrinkwrap.json are in sync. Please update your lock file with `npm install` before continuing.
npm error
npm error Missing: @testing-library/jest-dom@6.9.1 from lock file
npm error Missing: @testing-library/react@16.3.2 from lock file
npm error Missing: @testing-library/dom@10.4.1 from lock file
npm error Missing: framer-motion@12.42.2 from lock file
npm error Missing: jsdom@20.0.3 from lock file
npm error Invalid: lock file's recharts@2.15.4 does not satisfy recharts@2.15.0
npm error Missing: vitest@3.2.7 from lock file
npm error Missing: @babel/code-frame@7.29.7 from lock file
npm error Missing: @types/aria-query@5.0.4 from lock file
npm error Missing: aria-query@5.3.0 from lock file
npm error Missing: dom-accessibility-api@0.5.16 from lock file
npm error Missing: lz-string@1.5.0 from lock file
npm error Missing: pretty-format@27.5.1 from lock file
npm error Missing: @babel/helper-validator-identifier@7.29.7 from lock file
npm error Missing: @adobe/css-tools@4.5.0 from lock file
npm error Missing: css.escape@1.5.1 from lock file
npm error Missing: dom-accessibility-api@0.6.3 from lock file
npm error Missing: redent@3.0.0 from lock file
npm error Missing: dequal@2.0.3 from lock file
npm error Missing: motion-dom@12.42.2 from lock file
npm error Missing: motion-utils@12.39.0 from lock file
npm error Missing: abab@2.0.6 from lock file
npm error Missing: acorn-globals@7.0.1 from lock file
npm error Missing: cssom@0.5.0 from lock file
npm error Missing: cssstyle@2.3.0 from lock file
npm error Missing: data-urls@3.0.2 from lock file
npm error Missing: decimal.js@10.6.0 from lock file
npm error Missing: domexception@4.0.0 from lock file
npm error Missing: escodegen@2.1.0 from lock file
npm error Missing: form-data@4.0.6 from lock file
npm error Missing: html-encoding-sniffer@3.0.0 from lock file
npm error Missing: http-proxy-agent@5.0.0 from lock file
npm error Missing: https-proxy-agent@5.0.1 from lock file
npm error Missing: is-potential-custom-element-name@1.0.1 from lock file
npm error Missing: nwsapi@2.2.24 from lock file
npm error Missing: parse5@7.3.0 from lock file
npm error Missing: saxes@6.0.0 from lock file
npm error Missing: symbol-tree@3.2.4 from lock file
npm error Missing: tough-cookie@4.1.4 from lock file
npm error Missing: w3c-xmlserializer@4.0.0 from lock file
npm error Missing: webidl-conversions@7.0.0 from lock file
npm error Missing: whatwg-encoding@2.0.0 from lock file
npm error Missing: whatwg-mimetype@3.0.0 from lock file
npm error Missing: whatwg-url@11.0.0 from lock file
npm error Missing: ws@8.21.0 from lock file
npm error Missing: xml-name-validator@4.0.0 from lock file
npm error Missing: acorn-walk@8.3.5 from lock file
npm error Missing: cssom@0.3.8 from lock file
npm error Missing: esprima@4.0.1 from lock file
npm error Missing: source-map@0.6.1 from lock file
npm error Missing: asynckit@0.4.0 from lock file
npm error Missing: combined-stream@1.0.8 from lock file
npm error Missing: es-set-tostringtag@2.1.0 from lock file
npm error Invalid: lock file's hasown@2.0.2 does not satisfy hasown@2.0.4
npm error Missing: mime-types@2.1.35 from lock file
npm error Missing: delayed-stream@1.0.0 from lock file
npm error Missing: es-errors@1.3.0 from lock file
npm error Missing: get-intrinsic@1.3.0 from lock file
npm error Missing: has-tostringtag@1.0.2 from lock file
npm error Missing: call-bind-apply-helpers@1.0.2 from lock file
npm error Missing: es-define-property@1.0.1 from lock file
npm error Missing: es-object-atoms@1.1.2 from lock file
npm error Missing: get-proto@1.0.1 from lock file
npm error Missing: gopd@1.2.0 from lock file
npm error Missing: has-symbols@1.1.0 from lock file
npm error Missing: math-intrinsics@1.1.0 from lock file
npm error Missing: dunder-proto@1.0.1 from lock file
npm error Missing: @tootallnate/once@2.0.1 from lock file
npm error Missing: agent-base@6.0.2 from lock file
npm error Missing: mime-db@1.52.0 from lock file
npm error Missing: entities@6.0.1 from lock file
npm error Missing: ansi-regex@5.0.1 from lock file
npm error Missing: ansi-styles@5.2.0 from lock file
npm error Missing: react-is@17.0.2 from lock file
npm error Missing: indent-string@4.0.0 from lock file
npm error Missing: strip-indent@3.0.0 from lock file
npm error Missing: xmlchars@2.2.0 from lock file
npm error Missing: min-indent@1.0.1 from lock file
npm error Missing: psl@1.15.0 from lock file
npm error Missing: universalify@0.2.0 from lock file
npm error Missing: url-parse@1.5.10 from lock file
npm error Missing: querystringify@2.2.0 from lock file
npm error Missing: requires-port@1.0.0 from lock file
npm error Missing: @types/chai@5.2.3 from lock file
npm error Missing: @vitest/expect@3.2.7 from lock file
npm error Missing: @vitest/mocker@3.2.7 from lock file
npm error Missing: @vitest/pretty-format@3.2.7 from lock file
npm error Missing: @vitest/runner@3.2.7 from lock file
npm error Missing: @vitest/snapshot@3.2.7 from lock file
npm error Missing: @vitest/spy@3.2.7 from lock file
npm error Missing: @vitest/utils@3.2.7 from lock file
npm error Missing: chai@5.3.3 from lock file
npm error Invalid: lock file's debug@4.3.7 does not satisfy debug@4.4.3
npm error Missing: expect-type@1.4.0 from lock file
npm error Missing: magic-string@0.30.21 from lock file
npm error Missing: pathe@2.0.3 from lock file
npm error Missing: picomatch@4.0.5 from lock file
npm error Missing: std-env@3.10.0 from lock file
npm error Missing: tinybench@2.9.0 from lock file
npm error Missing: tinyexec@0.3.2 from lock file
npm error Missing: tinyglobby@0.2.17 from lock file
npm error Missing: tinypool@1.1.1 from lock file
npm error Missing: tinyrainbow@2.0.0 from lock file
npm error Missing: vite-node@3.2.4 from lock file
npm error Missing: why-is-node-running@2.3.0 from lock file
npm error Missing: @types/deep-eql@4.0.2 from lock file
npm error Missing: assertion-error@2.0.1 from lock file
npm error Missing: estree-walker@3.0.3 from lock file
npm error Missing: strip-literal@3.1.0 from lock file
npm error Missing: tinyspy@4.0.4 from lock file
npm error Missing: loupe@3.2.1 from lock file
npm error Missing: check-error@2.1.3 from lock file
npm error Missing: deep-eql@5.0.2 from lock file
npm error Missing: pathval@2.0.1 from lock file
npm error Invalid: lock file's @jridgewell/sourcemap-codec@1.5.0 does not satisfy @jridgewell/sourcemap-codec@1.5.5
npm error Missing: js-tokens@9.0.1 from lock file
npm error Missing: fdir@6.5.0 from lock file
npm error Missing: picomatch@4.0.5 from lock file
npm error Missing: cac@6.7.14 from lock file
npm error Missing: es-module-lexer@1.7.0 from lock file
npm error Missing: iconv-lite@0.6.3 from lock file
npm error Missing: safer-buffer@2.1.2 from lock file
npm error Missing: tr46@3.0.0 from lock file
npm error Missing: siginfo@2.0.0 from lock file
npm error Missing: stackback@0.0.2 from lock file
npm error
npm error Clean install a project
npm error
npm error Usage:
npm error npm ci
npm error
npm error Options:
npm error [--install-strategy <hoisted|nested|shallow|linked>] [--legacy-bundling]
npm error [--global-style] [--omit <dev|optional|peer> [--omit <dev|optional|peer> ...]]
npm error [--include <prod|dev|optional|peer> [--include <prod|dev|optional|peer> ...]]
npm error [--strict-peer-deps] [--foreground-scripts] [--ignore-scripts] [--no-audit]
npm error [--no-bin-links] [--no-fund] [--dry-run]
npm error [-w|--workspace <workspace-name> [-w|--workspace <workspace-name> ...]]
npm error [-ws|--workspaces] [--include-workspace-root] [--install-links]
npm error
npm error aliases: clean-install, ic, install-clean, isntall-clean
npm error
npm error Run "npm help ci" for more info
npm error A complete log of this run can be found in: /root/.npm/_logs/2026-07-09T11_07_52_767Z-debug-0.log

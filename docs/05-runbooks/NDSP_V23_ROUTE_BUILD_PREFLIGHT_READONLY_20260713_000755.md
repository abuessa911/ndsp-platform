============================================================
NDSP — V23 Route and Production Build Preflight
MODE=READ_ONLY
DATE=2026-07-13T00:07:55+02:00
PROJECT=/home/nawaf511/empire-core-new
FRONTEND=/home/nawaf511/empire-core-new/frontend/user-portal-vite
LIVE=/var/www/ndsp-my
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V23_ROUTE_BUILD_PREFLIGHT_READONLY_20260713_000755.md
============================================================

== 1) النسخة الحية وملف البناء المحلي ==
LIVE_INDEX_SHA256=a9cff279574863b4b3e94d1137f729a0a754384c45e7eb9d426a27b547754b8b
DIST_INDEX_SHA256=0c6d613215a623a6423f0b1a60ad1ecc9784af3a1e58e4726cf2510032297315
SOURCE_INDEX_SHA256=4288c563df6c800c8c5ff742d30aa1992d1665a26b0e28c7c9d3f5217dad34e9

--- LIVE ASSET REFERENCES ---
href="/assets/index-OGqS1LGt.css"
href="/assets/ndsp-mobile-chart-spacing-fix.css?v=20260710_120639"
href="/assets/ndsp-mobile-ui-normalize-v1.css?v=20260711_005643"
href="/assets/ndsp-pages-routes-safe-v13.css?v=20260710_165834"
href="/assets/ndsp-portal-chart-ar-hotfix.css?v=20260710_115828"
href="/assets/ndsp-single-ui-controller-v1.css?v=20260710_195033"
src="/assets/index-DCTFTCAz.js?v=20260710_195033"
src="/assets/ndsp-mobile-chart-spacing-fix.js?v=20260710_120639"
src="/assets/ndsp-pages-routes-safe-v13.js?v=20260710_165834"
src="/assets/ndsp-single-ui-controller-v1.js?v=20260710_195033"

--- LOCAL DIST ASSET REFERENCES ---
href="/assets/index-CB5D1TQG.css"
src="/assets/index-BX9FubtP.js"

== 2) ملفات الراوتر الفعلية ==
ROUTER_FILE_COUNT=0

== 3) محتوى App الحالي ==

== 4) تسجيل الصفحات والقائمة الجانبية ==
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx:100:    governanceRisk: "الحوكمة والمخاطر",
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx:203:    governanceRisk: "Governance & Risk",

== 5) ملفات صفحات القرار والحوكمة الحالية ==
PAGE_FILE_MISSING=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Decisions.tsx
PAGE_FILE_MISSING=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Decisions.jsx
PAGE_FILE_MISSING=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Governance.tsx
PAGE_FILE_MISSING=/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/pages/Governance.jsx

== 6) اكتشاف جلب السعر وطلبات API ==
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/hooks/useMarket.js:6:  /api/...  --->  https://api.ndsp.app/api/...
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/hooks/useMarket.js:22:      const res = await fetch(url, {
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/hooks/useMarket.js:46:      const url = `${BASE_URL}/api/market/prices?symbol=${encodeURIComponent(normalizedSymbol)}`;
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/hooks/useMarket.js:63:      console.error("PRICE FETCH ERROR:", err);
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/hooks/useMarket.js:76:      const url = `${BASE_URL}/api/scenario/levels?symbol=${encodeURIComponent(normalizedSymbol)}`;
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/core/services/marketService.js:1:import request from "../api/apiClient";
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/core/services/marketService.js:4:  const data = await request(`/api/market/prices?symbol=${symbol}`);
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/core/services/scenarioService.js:1:import request from "../api/apiClient";
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/core/services/scenarioService.js:4:  const data = await request(`/api/scenario/levels?symbol=${symbol}`);
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/core/api/apiClient.js:6:  const res = await fetch(url, {
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx:443:  const endpoint = `/api/scenario/levels?symbol=${encodeURIComponent(symbol)}`;
/home/nawaf511/empire-core-new/frontend/user-portal-vite/src/main.jsx:446:    const response = await fetch(endpoint, {

== 7) أسماء متغيرات البيئة بدون كشف القيم ==
ENV_FILE_COUNT=0

== 8) إعدادات Vite وpackage.json ==
--- PACKAGE SCRIPTS ---
{
  "name": "ndsp-user-portal-vite",
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5173",
    "build": "vite build",
    "preview": "vite preview --host 0.0.0.0 --port 4173"
  },
  "dependencies": {
    "vite": "^6.0.7"
  }
}

VITE_CONFIG=/home/nawaf511/empire-core-new/frontend/user-portal-vite/vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    host: "0.0.0.0",
    port: 5173,
    strictPort: true,

    proxy: {
      "/api": {
        target: "https://api.ndsp.app",
        changeOrigin: true,
        secure: true
      }
    }
  },

  preview: {
    host: "0.0.0.0",
    port: 4173,
    strictPort: true
  }
});

== 9) تحليل الحزمة الحية حول PRICE FETCH ERROR ==
LIVE_JS_FILE_COUNT=4

LIVE_JS=/var/www/ndsp-my/assets/index-DCTFTCAz.js
LIVE_JS_SHA256=1b5eaa999dc4dc259ec5274a11a866080552da31e9f4e7f476edb3877d49e3cd
MARKER_PRICE_FETCH_ERROR=-1
MARKER_quality-live=-1
MARKER_VITE_NDSP=-1
DISCOVERED_API_PATHS_BEGIN
http://fb.me/use-check-prop-types
http://www.w3.org/1998/Math/MathML
http://www.w3.org/1999/xhtml
http://www.w3.org/1999/xlink
http://www.w3.org/2000/svg
http://www.w3.org/XML/1998/namespace
https://reactjs.org/docs/error-decoder.html?invariant=
DISCOVERED_API_PATHS_END

LIVE_JS=/var/www/ndsp-my/assets/ndsp-mobile-chart-spacing-fix.js
LIVE_JS_SHA256=513c344e0f8c42934fe54d085e22e32b89a545cd6f38187b3e940a9328f60083
MARKER_PRICE_FETCH_ERROR=-1
MARKER_quality-live=-1
MARKER_VITE_NDSP=-1
DISCOVERED_API_PATHS_BEGIN
DISCOVERED_API_PATHS_END

LIVE_JS=/var/www/ndsp-my/assets/ndsp-pages-routes-safe-v13.js
LIVE_JS_SHA256=a866c8987cfd72bc28ff4d6b17d7c51356d566ae8ce23049189062c19346d387
MARKER_PRICE_FETCH_ERROR=-1
MARKER_quality-live=-1
MARKER_VITE_NDSP=-1
DISCOVERED_API_PATHS_BEGIN
DISCOVERED_API_PATHS_END

LIVE_JS=/var/www/ndsp-my/assets/ndsp-single-ui-controller-v1.js
LIVE_JS_SHA256=25cd4e3f9ee81c6ee2901bea46a565d96ec8e1e2284fcfc3bb8d177c40dcc7b5
MARKER_PRICE_FETCH_ERROR=-1
MARKER_quality-live=-1
MARKER_VITE_NDSP=-1
DISCOVERED_API_PATHS_BEGIN
DISCOVERED_API_PATHS_END

== 10) مقارنة وجود علامات V20 ==
V20_MARKER_PRESENT=/home/nawaf511/empire-core-new/frontend/user-portal-vite/index.html
V20_MARKER_PRESENT=/home/nawaf511/empire-core-new/frontend/user-portal-vite/dist/index.html
V20_MARKER_PRESENT=/var/www/ndsp-my/index.html

============================================================
READ_ONLY=true
FILES_CHANGED=0
SERVICES_RESTARTED=0
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_V23_ROUTE_BUILD_PREFLIGHT_READONLY_20260713_000755.md
FINAL_STATUS=NDSP_V23_ROUTE_BUILD_PREFLIGHT_READONLY_OK
============================================================

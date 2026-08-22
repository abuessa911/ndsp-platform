#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

printf '[1/9] Checking merged and authentication source files...\n'
for FILE in \
  src/pages/HomePage.tsx \
  src/pages/MethodologyPage.tsx \
  src/pages/AnalysisPage.tsx \
  src/pages/DocumentationPage.tsx \
  src/pages/SignInPage.tsx \
  src/pages/AccountRecoveryPage.tsx \
  src/api/auth.ts \
  src/auth/AuthContext.tsx \
  src/auth/RequireAdmin.tsx \
  src/pages/admin/AdminPages.tsx \
  src/components/PublicLayout.tsx \
  src/components/AdminLayout.tsx \
  src/components/GovernanceDialog.tsx \
  public/assets/decision-convergence.png; do
  test -s "$FILE"
done

printf '[2/9] Checking public and account routes...\n'
for ROUTE in \
  'Route index element={<DomainRootPage />}' \
  'path="methodology"' \
  'path="analysis"' \
  'path="documentation"' \
  'path="login"' \
  'path="sign-in"' \
  'path="forgot-password"' \
  'path="reset-password"'; do
  rg -Fq "$ROUTE" src/App.tsx
done

printf '[3/9] Checking administration routes...\n'
for ROUTE in \
  'path="admin/cot"' \
  'path="overview"' \
  'path="reports"' \
  'path="daily-control"' \
  'path="experiments"' \
  'path="comparisons"' \
  'path="governance"' \
  'path="audit-logs"' \
  'path="contracts"' \
  'path="settings"'; do
  rg -Fq "$ROUTE" src/App.tsx
done

printf '[4/9] Checking real authentication contract and fail-closed guard...\n'
rg -Fq 'credentials: "include"' src/api/auth.ts
for ENDPOINT in \
  '/api/auth/session' \
  '/api/auth/login' \
  '/api/auth/2fa/login/verify' \
  '/api/auth/logout' \
  '/api/auth/forgot-password' \
  '/api/auth/reset-password'; do
  rg -Fq "$ENDPOINT" src/api/auth.ts
done
rg -Fq '<Route element={<RequireAdmin />}>' src/App.tsx
rg -Fq 'if (!auth.isAdmin)' src/auth/RequireAdmin.tsx
if rg -Fq 'window.setTimeout(() => navigate("/admin/cot/overview")' src/pages/SignInPage.tsx; then
  printf 'ERROR=MOCK_LOGIN_REDIRECT_PRESENT\n' >&2
  exit 1
fi

printf '[5/9] Checking shared theme and navigation...\n'
rg -Fq '{ label: "الرئيسية", path: "/" }' src/data.ts
rg -Fq 'to="/" aria-label="العودة إلى الرئيسية"' src/components/PublicLayout.tsx
rg -Fq 'to="/login?intent=elite-trial"' src/components/PublicLayout.tsx
rg -Fq -- '--gold:' src/styles.css
rg -Fq -- '--blue:' src/styles.css
rg -Fq 'IBM Plex Sans Arabic' src/styles.css
rg -Fq 'Inter' src/styles.css
if rg -Fq '../hooks/useEliteTrial' src; then
  printf 'ERROR=ORPHANED_ELITE_TRIAL_IMPORT_PRESENT\n' >&2
  exit 1
fi
if rg -Fq '<a href="#forgot-password"' src/pages/SignInPage.tsx; then
  printf 'ERROR=NESTED_RECOVERY_ANCHOR_PRESENT\n' >&2
  exit 1
fi

printf '[6/9] Type checking...\n'
node node_modules/typescript/bin/tsc --noEmit

printf '[7/9] Building production files...\n'
node node_modules/vite/bin/vite.js build
node scripts/prepare-sites-build.mjs

printf '[8/9] Testing Sites worker...\n'
node --test tests/sites-worker.test.mjs

printf '[9/9] Checking packaged build outputs...\n'
test -s dist/client/index.html
test -s dist/server/index.js
test -s dist/.openai/hosting.json

printf 'PUBLIC_ROUTES=/,/methodology,/analysis,/documentation\n'
printf 'AUTH_ROUTES=/login,/sign-in,/forgot-password,/reset-password\n'
printf 'ADMIN_ROUTES=/admin/cot/overview,/admin/cot/reports,/admin/cot/daily-control,/admin/cot/experiments,/admin/cot/comparisons,/admin/cot/governance,/admin/cot/audit-logs,/admin/cot/contracts,/admin/cot/settings\n'
printf 'LANDING_PAGE=RETAINED\n'
printf 'ADMIN_SECTION=RETAINED\n'
printf 'THEME=SOVEREIGN_MERIDIAN_RETAINED\n'
printf 'AUTH_INTEGRATION=SAME_ORIGIN_SESSION_AND_ADMIN_GUARD\n'
printf 'USER_PORTAL_PAGES=MISSING_NOT_SAFE_TO_DELETE_EXISTING_PORTAL\n'
printf 'PAGE_DATA=MOCK_REQUIRES_REAL_DATA_MIGRATION\n'
printf 'FINAL_STATUS=MERGED_UI_VERIFICATION_PASS\n'

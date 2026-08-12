# Frontend TypeScript Migration Plan

## Scope

- Current application: `frontend/user-portal-vite`
- Migration mode: Incremental
- Runtime changes: None by default
- Public API contract changes: Require separate approval

## Objective

Migrate the current React/Vite JavaScript frontend to TypeScript without a
high-risk rewrite. Preserve current behavior, RTL/LTR support, API contracts,
and strict CORE/EXPANDED separation.

## Governing Rules

1. New frontend components, hooks, API clients, schemas, and tests use TypeScript.
2. Existing JavaScript may remain temporarily when it is not modified.
3. A modified JavaScript module should be migrated in the same PR when bounded.
4. EXPANDED must never be exposed through the Public API or public UI.
5. API payloads require explicit TypeScript types and runtime validation with Zod.
6. Loading, empty, error, success, and permission-denied states are mandatory.
7. RTL and LTR behavior must be tested.
8. Mock data must not replace real production data.

## Phase 0 — Configuration and Baseline

Add TypeScript, React type packages, `tsconfig.json`, optional
`tsconfig.app.json`, and `vite-env.d.ts`.

Initial settings should support incremental migration:

```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "noEmit": true,
    "strict": true,
    "jsx": "react-jsx",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "skipLibCheck": true
  }
}
```

Exit criteria:

- Existing Vite production build passes.
- `tsc --noEmit` passes.
- Runtime behavior is unchanged.

## Phase 1 — Contracts and Data Access

Migrate API clients, request/response models, Zod schemas, TanStack Query
hooks, authentication state, CORE public models, and EXPANDED internal models.

Required boundary:

```text
CORE models -> Public API client -> Public UI
EXPANDED models -> Internal Admin API client -> Admin UI
```

Exit criteria:

- API boundaries are explicitly typed.
- Untrusted payloads are runtime validated.
- Public code cannot import EXPANDED payloads.

## Phase 2 — Shared Components

Migrate layouts, forms, dialogs, status badges, table adapters, chart adapters,
and localization helpers.

Exit criteria:

- Props are typed.
- Sensitive actions use explicit labels.
- RTL/LTR tests pass.

## Phase 3 — Public Portal

Migrate Home, Methodology, Current Analysis, Documentation, and Sign In.

Exit criteria:

- Public UI exposes CORE only.
- No shadow metadata appears.
- Loading, empty, error, and success states are tested.

## Phase 4 — Admin Governance UI

Migrate Overview, Reports, Daily Control, Experiments, Comparisons, Governance,
Audit Logs, Contracts, and Settings.

Exit criteria:

- Permissions are typed and tested.
- Promotion creates a Governance Promotion Request.
- Sensitive actions generate audit events.
- No direct Official Result Store mutation exists.

## Phase 5 — Strict Completion

- Convert remaining `.js` and `.jsx`.
- Remove `allowJs`.
- Enable stricter compiler checks.
- Make governed frontend warnings fail CI.
- Record human confirmation and Traceability completion.

## Recommended Conversion Order

1. `src/api/**`
2. `src/contracts/**`
3. `src/schemas/**`
4. `src/hooks/**`
5. `src/components/shared/**`
6. public pages
7. admin pages
8. entry points
9. remaining utilities

## Required CI Checks

- TypeScript type check
- Vite production build
- Vitest and Testing Library
- Playwright for critical flows
- governance policy validator
- CORE/EXPANDED public-separation test
- RTL/LTR tests

## Pull Request Rules

Each migration PR must be bounded, tested, reversible, and free of unrelated
visual redesign or production-data mutation. Exceptions require an ADR, owner,
expiration date, remediation issue, and approval.

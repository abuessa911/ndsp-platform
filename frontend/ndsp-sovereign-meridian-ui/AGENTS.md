# Prototype Instructions

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Before making substantial visual changes, use the Product Design plugin's `get-context` skill when the visual source is unclear or no longer matches the current goal. When the user gives durable prototype-specific design feedback, preferences, or decisions, record them in `AGENTS.md`.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.

## NDSP design decisions

- The selected visual truth is **Sovereign Meridian**, in a 16:9 presentation, using Carbon Black, Meridian Gold, Intelligence Blue, and restrained semantic colors.
- The public experience is Arabic RTL and exposes official `CORE` results only. Internal experiment names or shadow results must not appear on public routes.
- The admin experience may compare `CORE · OFFICIAL` with `EXPANDED · SHADOW`, while keeping `Public Exposure · Disabled` visible.
- Arabic UI uses IBM Plex Sans Arabic; Latin labels, versions, JSON, dates, and code use Inter in LTR blocks.
- All sensitive actions use an explicit governance dialog that explains changed/unchanged scope, impact, versions, approver, and UTC execution time.
- Preserve the supplied NDSP decision-convergence raster. The legacy lockup contained an obsolete personal-name subtitle, so use the cleaned geometric NDSP mark plus live NDSP/Decision Support Platform text instead of retaining that lockup.

- Public mobile navigation uses a scroll-contained drawer with safe-area support, focus restoration, Escape/backdrop close, and background scroll lock.
- The merged delivery keeps the complete landing and `/admin/cot/*` route families from the full package, while retaining the public methodology, analysis, documentation, and sign-in pages without duplicate route sources.
- Authentication uses only same-origin `/api/auth/*` contracts with `credentials: include`; never place server secrets, database credentials, or privileged headers in frontend code.
- Administration routes must fail closed: an authenticated session and an explicit administrator/owner role are both required before rendering the admin layout.
- This package still has mock analysis and administration records and does not include the historical user-portal page family. Do not delete or replace the existing production user portal until those pages and real data contracts are migrated and tested.

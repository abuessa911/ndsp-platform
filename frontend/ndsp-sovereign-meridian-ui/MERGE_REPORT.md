# NDSP Sovereign Meridian UI — Merge Report

## Inputs

- Full package SHA256: `8fcf2480147b28ed45a2485cc1b5881a7eef1dbe1317bbfac3aa0c9d790208b0`
- No-landing/no-admin package SHA256: `98ccd6ca12dd01902d4d4992b6cdca15cbaf1457bb0af8582a6743783bc78f15`

## Merge policy

- The full package is authoritative for the Sovereign Meridian theme, landing page, administration pages, shared navigation, assets, and routing.
- The second package is a subset derived from the full package. Its retained methodology, analysis, and documentation pages are byte-identical to the corresponding full-package pages and therefore require no duplicate copies.
- The useful recovery-control cleanup from the second package was incorporated into the sign-in page while preserving the existing administration redirect.
- The unused `EliteTrialGate` source was excluded because it referenced a missing hook and was not mounted by any route.
- A single route source is retained for every page; no duplicate landing or administration trees were created.

## Final route families

- Public: `/`, `/methodology`, `/analysis`, `/documentation`, `/sign-in`
- Administration: `/admin/cot/overview`, `/admin/cot/reports`, `/admin/cot/daily-control`, `/admin/cot/experiments`, `/admin/cot/comparisons`, `/admin/cot/governance`, `/admin/cot/audit-logs`, `/admin/cot/contracts`, `/admin/cot/settings`

## Scope note

The original merge was a frontend prototype. A later integration pass connected its account routes to the audited same-origin authentication contracts and added a fail-closed administration guard. It still does not modify backend services, databases, Nginx, Systemd, Docker, or PM2, and its page data remains presentational.

# COT Governance UI Requirements

## Public interface

Public users see CORE only.

Required fields:

- Official direction.
- Analysis mode.
- Effective week.
- Report date.
- Direction label.
- Dominance delta.
- Weekly support status.
- Last updated UTC.

EXPANDED and experiment status must not be exposed.

## Admin interface

Route group:

`/admin/cot`

Sections:

- Overview.
- Reports.
- Daily Control.
- Experiments.
- Comparisons.
- Governance.
- Audit Logs.
- Contracts.
- Settings.

## References

- Stripe: public landing and CTA.
- Linear: sidebar, tables, filters, speed.
- Vercel: projects, cards, settings.
- Figma: forms, dialogs, UX, typography.
- Notion: documentation, navigation, empty states.

## Technology

Preferred for new governance UI:

- React.
- Vite.
- TypeScript.
- shadcn/ui and Radix UI.
- React Hook Form and Zod.
- TanStack Query.
- AG Grid for large admin tables.
- Recharts for simple charts.
- ECharts for advanced analytics.
- Vitest and Testing Library.
- Playwright.
- RTL Arabic and LTR English at component level.

## Sensitive actions

Promotion must create a Governance Promotion Request.

A button must not directly switch EXPANDED into CORE.

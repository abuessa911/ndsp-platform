# COT-GOV-1.0.0 — Master Handoff

## العربية

الوثيقة العربية الكاملة:

`reports/COT_GOVERNANCE_REPORT_AR.md`

اتجاه النص الرسمي: RTL.

## English

The complete English document is located at:

`reports/COT_GOVERNANCE_REPORT_EN.md`

Official text direction: LTR.

## Authoritative implementation files

- `config/cot-engine.config.json`
- `contracts/`
- `src/`
- `tests/`
- `fixtures/`
- `integration/`
- `deploy/path-migration/`

## Critical status

This package is a reference implementation and controlled handoff.

It must not be copied blindly over the current production service before reviewing:

- Current `main.cjs`.
- Existing TDL-M&L logic.
- Existing TDL-S logic.
- Existing database and result stores.
- Current public and internal API routes.
- systemd and Nginx runtime dependencies.

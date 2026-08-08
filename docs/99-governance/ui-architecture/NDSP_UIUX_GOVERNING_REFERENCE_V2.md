# NDSP UI/UX Governing Reference V2

**Status:** ACTIVE / MANDATORY  
**Effective:** 2026-08-08  
**Scope:** UI/UX, visual identity, customer terminology exposure, subscription presentation, trial exposure, confidentiality boundaries.  
**Baseline preserved:** `UI_BACKEND_GOVERNANCE_POLICY.yaml` remains mandatory for all non-conflicting technical and engineering requirements.

## 1. Precedence

This document and `NDSP_UIUX_GOVERNANCE_SUPERSESSION_V2.yaml` are the controlling V2 overlay for the design/exposure areas listed above.

The governing merge rule is:

> **MERGE, NOT REWRITE. Preserve unique content. Consolidate only true duplication.**

No business logic, backend ownership, database ownership, service boundary, canonical dataset, existing contract, runtime evidence, or technical-freeze requirement is changed by this V2 overlay.

## 2. Public repository safety

This GitHub repository is public. The full master UI/UX governance report contains confidential architecture and proprietary analytical material and therefore **must not be committed to this public repository**.

The full private artifacts are retained in the owner's persistent private file library. This repository freezes their integrity hashes and the public-safe governing rules only.

## 3. Approved visual identity

NDSP is a **Governed Institutional Decision Intelligence Platform**, not a retail trading dashboard, crypto exchange, gaming interface, or generic AI product.

Approved design direction:

- Logo complexity: **3/10**.
- Dominant foundation: **Deep Charcoal / Near Black**.
- Premium authority accent: **Warm Refined Metallic Gold**.
- Analytical secondary accent: **Controlled Sky Blue**.
- Supporting neutral: **White / Off-White**.
- Indigo/Violet is no longer the primary brand accent.
- Purple remains available only as a controlled semantic color for Review/Experimental states where appropriate.
- Motion is subtle only; Reduced Motion support is mandatory.
- Continuous glow, particle systems, heavy gold gradients, casino/gaming aesthetics, and crypto-exchange visual language are forbidden.

Gold is an authority/brand accent, not a universal status color. Semantic status colors remain separate.

## 4. Architecture invariants

The V2 design decision does not change:

- ONE Canonical COT Dataset.
- 16 logical Decision Layers.
- 28 logical Capabilities.
- Backend ownership.
- Database ownership.
- Service boundaries.
- Governance authority.
- Existing contracts.
- Existing technical-freeze / TBD items.

## 5. Customer-visible terminology — NAME-ONLY

The system preserves 16 logical Decision Layers internally, but customer-facing surfaces may expose **only five approved names**, and only according to entitlement:

1. **TDL**
2. **NMP**
3. **Nawaf Golden Signal**
4. **Enhanced Nawaf Golden Signal**
5. **Devil's Advocate**

These are customer display abstractions. Their appearance does **not** prove or define a 1:1 mapping to internal Decision Layer numbering.

The remaining **11 internal names are protected and must not be exposed**.

## 6. Name visibility does not disclose implementation

Showing an approved name never authorizes disclosure of:

- formulas or algorithms;
- weights;
- internal inputs;
- internal state;
- raw values;
- layer-level outputs/results;
- producers or internal sources;
- internal contracts;
- dependencies;
- internal relationships;
- database/service structure;
- hidden layer or capability names.

The same prohibition applies to API payloads, DOM, hidden routes, HTML IDs, CSS classes, accessibility labels, alt text, metadata, SEO, analytics event names, client logs, error messages, and frontend bundles.

**Sending a secret to the browser and hiding it with CSS, blur, masking, or a lock icon is forbidden.** Authorization and entitlement must be enforced server-side.

## 7. Public vs authenticated customer experience

Anonymous Landing/Public stays **CORE-first** and must not become a map of internal analytical architecture.

The public-safe narrative is:

**Official Decision Context → Authorized Market Context → Authorized Evidence → Freshness → Governance Trust → Methodology/Transparency**

The authenticated Customer Workspace is where plan entitlement controls approved NAME-ONLY visibility and authorized customer-facing analytical depth.

Admin/Review authorization remains separate from customer subscription entitlement.

## 8. Four customer-facing subscription plans

The customer-facing plan presentation is standardized to:

- **Free**
- **Pro**
- **Elite**
- **Institutional**

Prices, asset limits, API allowances, user limits, retention, SLA, and other commercial boundaries must come from approved billing/subscription contracts or configuration. Unverified values must not be hard-coded into the UI.

## 9. 16-Day Trial and entitlement matrix

The approved naming exposure is:

| Context / Plan | Approved visible names | Protection rule |
|---|---|---|
| **16-Day Trial** | TDL + NMP + Nawaf Golden Signal + Enhanced Nawaf Golden Signal + Devil's Advocate | Names only; no formulas, logic, secrets, raw values, or layer-level outputs |
| **Free** | TDL | Name-only baseline after trial when no approved paid upgrade exists |
| **Pro** | TDL + NMP | Name-only; enforced server-side |
| **Elite** | All five approved names | Name-only; premium access does not equal IP disclosure |
| **Institutional** | All five approved names | Name-only plus contracted institutional features; internal logic remains confidential |

Entitlement changes authorized customer visibility and output depth only. It does not grant access to proprietary implementation.

## 10. Locked / protected states

A locked customer card must never contain the real protected name behind blur, asterisks, hidden markup, metadata, or client-side state.

Approved neutral wording includes:

- **Protected Intelligence**
- **Additional Analytical Depth**
- **Advanced Decision Intelligence**

The protected value must never reach the frontend unless the governing server-side authorization explicitly allows that public-safe representation.

## 11. Responsive, RTL/LTR and accessibility

- Arabic: RTL.
- English: LTR.
- Accessibility is mandatory.
- Color-only status is forbidden.
- Admin desktop analytical grid: 12 columns.
- Tablet: 8 columns.
- Mobile: 4 columns.
- Base spacing: 4px.
- Public whitespace: generous.
- Admin density: controlled high density.

## 12. Frozen private master artifacts

The complete confidential master report is retained privately with the following frozen hashes:

| Artifact | SHA-256 |
|---|---|
| `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.md` | `806be2bb2fbc72ae4192ec68d14d5b0e52162af4b5a9238ca9932b96c08c9d70` |
| `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.pdf` | `43ee65c41ee4451e7956c8242cc637ae80c2e3b28a72a27cf74593281365b3e5` |
| `NDSP_FINAL_MASTER_UIUX_ARCHITECTURE_GOVERNANCE_AR_V2_CONFIDENTIALITY_SUBSCRIPTIONS.docx` | `f6f7cdf097c827faa58c9a71e1a06cb4104fbe9ee0417d1bad6aa9ad0dff1bd8` |

These hashes are the integrity anchors for the owner-approved private reference set.

## 13. Final governing rule

> **NDSP must communicate the depth of its intelligence without exposing the secrets of its intelligence.**

Any future UI/UX change that conflicts with this V2 reference requires a new explicit governance revision rather than an informal design override.

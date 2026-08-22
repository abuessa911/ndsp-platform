# NDSP Sovereign Meridian — Design QA

## Comparison target

- Source visual truth: `/workspace/scratch/0403f2922e57/generated_images/NDSP_SOVEREIGN_MERIDIAN_16x9_1920x1080.png`
- Supporting full landing reference: `/workspace/scratch/0403f2922e57/upload/image-edit-target-24d4818552f0d81d.png`
- Public implementation screenshot: `/workspace/scratch/0403f2922e57/ndsp-sovereign-meridian-ui/qa/home-implementation.jpg`
- Admin implementation screenshot: `/workspace/scratch/0403f2922e57/ndsp-sovereign-meridian-ui/qa/admin-implementation.jpg`
- Governance dialog screenshot: `/workspace/scratch/0403f2922e57/ndsp-sovereign-meridian-ui/qa/dialog-implementation.jpg`
- Browser CSS viewport: `1363 × 936`, `devicePixelRatio: 1`
- Browser screenshot pixels: `1348 × 926`
- State: public home (RTL, logged out) and admin overview (mock authenticated), dark theme

## Normalization and evidence

- The 1487 × 1058 landing reference was center-normalized to 1348 × 926 for the full-view comparison.
- The 1920 × 1080 design-board public hero and the rendered hero were cropped and fit into equal 760 × 520 regions for focused comparison.
- Full-view public comparison: `qa/home-comparison.jpg`
- Focused public hero comparison: `qa/home-focused-comparison.jpg`
- Admin comparison: `qa/admin-comparison.jpg`
- Important small UI was checked in the focused admin comparison and the governance-dialog screenshot; no further focused crop was needed.

## Findings

No actionable P0, P1, or P2 differences remain.

- Fonts and typography: IBM Plex Sans Arabic and Inter match the design board's specified pairing. Weight, headline scale, Latin tracking, line height, and RTL/LTR separation are consistent with the reference.
- Spacing and layout rhythm: the public hero preserves the right-copy/left-evidence composition, authority rail, header proportions, restrained borders, and dark negative space. The admin screen preserves the fixed right sidebar, compact cards, dense table, and toolbar hierarchy.
- Colors and visual tokens: Carbon Black, Meridian Gold, Intelligence Blue, and semantic green/amber/red/purple states map directly to CSS tokens. Status always includes an icon and label instead of color alone.
- Image quality and asset fidelity: the supplied NDSP logo and decision-convergence motif are real raster assets cropped from the selected sources. They remain sharp at the rendered size and are not replaced with custom CSS or SVG art.
- Copy and content: the public hero follows the final Sovereign Meridian concept (`الأدلة تتقاطع. القرار يتجه.`). Public routes expose CORE only. CORE/EXPANDED comparison copy is confined to admin routes.
- Icons: Phosphor outline icons provide consistent stroke weight and alignment across navigation, status chips, tables, cards, and dialogs.
- Accessibility: semantic navigation, headings, buttons, labels, alt text, visible focus, reduced-motion handling, and practical touch targets are present.

## Comparison history

### Pass 1

- [P2] Public hero consumed 720px below the header, pushing the next section almost entirely below the first 936px viewport and drifting from the selected landing composition.
- Fix: reduced the desktop hero frame to 650px, reduced the convergence asset to 520px, tightened vertical padding, and reduced the maximum display-heading size.

### Pass 2

- Post-fix evidence: `qa/home-comparison.jpg` and `qa/home-focused-comparison.jpg`.
- The first viewport now retains the intended hero hierarchy while exposing the start of the Decision Meridian section. No P0/P1/P2 mismatch remains.

## Primary interactions tested in the cloud browser

- Public navigation and CTA to current analysis.
- Instrument selection updates the official direction and evidence.
- Documentation search filters the hierarchy and opens the selected document.
- Mock sign-in reaches `/admin/cot/overview`.
- Admin agreement filter reduces the table from four rows to two disagreement rows.
- Governance dialog opens, blocks `Promote to CORE` until a reason is entered, then enables it.
- Settings tab selection updates the active section and renders six service cards.
- Application console errors/warnings for `terminal.local`: none.

## Follow-up polish

- [P3] The selected browser surface had a fixed desktop viewport, so tablet and phone layouts were reviewed from the implemented 1180px, 900px, and 680px media-query rules rather than separate browser screenshots.

## Implementation checklist

- [x] TypeScript check passes.
- [x] Production build passes.
- [x] Browser-rendered routes and core interactions pass.
- [x] Public/admin governance boundary is visible and preserved.
- [x] Real supplied brand assets are used.

final result: passed

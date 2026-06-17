You are researching the Grid component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Grid /
CSS-Grid layout primitive is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop choices
field leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Grid is THE SECOND LAYOUT ENGINE — the two-dimensional (CSS Grid) layout
component, the third Layout brief, and the component that CLOSES the
Box → Stack → Grid layout-engine triad (Box the substrate, Stack the 1D
engine, Grid the 2D engine). It STANDS ON Box and is the SIBLING of Stack:
- IT STANDS ON BOX (components/box.md): it inherits the polymorphic
  as/asChild Slot model, the spacing-token scale (its `gap` resolves against
  it), the zero-runtime styling delivery, and the logical-property RTL
  mapping. Don't re-derive Box — name it and record only the delta.
- IT IS THE 2D SIBLING OF STACK (components/stack.md): Stack is one axis
  (a column OR a row, even when it wraps); Grid manages rows AND columns
  simultaneously via tracks. Resolve the Stack-vs-Grid boundary from Grid's
  side (when you genuinely need two-dimensional alignment vs when a Stack
  or a wrapping Stack suffices). Stack also owns the gap per Box's
  no-external-margin principle — Grid inherits that same no-margin discipline.
It is COMPOSED BY card galleries, PageLayout/AppShell, forms (label/field
column alignment), and data displays.

THE DEFINING GRID-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE 12-COLUMN LEGACY vs NATIVE CSS GRID (the headline historical divide):
  the float/flexbox 12-column responsive grid system (Bootstrap's Row/Col,
  Ant's 24-column, the `<Col span={6}>` fraction-of-N model, gutters,
  nesting) vs NATIVE CSS GRID (grid-template-columns, repeat()/minmax(),
  fr units, auto-fit/auto-fill, grid-template-areas). Resolve the practice's
  POV: ship a CSS-Grid-based component, not a reimplemented float system —
  but acknowledge the 12-column mental model persists (some keep a Grid/Col
  span API as a familiar layer over CSS Grid). Note the MUI Grid→Grid2
  (flexbox→CSS Grid) migration as the worked example.
- THE THREE GRID GENRES (the genre split, parallel to Stack's direction):
  (1) the LAYOUT / COLUMN grid — the page-level N-column responsive system
  (Bootstrap Row/Col, Braid Columns/Column, Polaris columns); (2) the
  AUTO-GRID / "RAM" pattern — repeat(auto-fit, minmax(min, 1fr)), a
  self-responsive grid of equal cells that reflows WITHOUT media queries
  (the card gallery that goes 4→3→2→1 on its own; Chakra SimpleGrid
  minChildWidth) — the modern killer feature; (3) the NAMED-AREAS /
  TEMPLATE grid — grid-template-areas for explicit 2D placement (the
  app-shell header/sidebar/main/footer; PageLayout). Resolve how one Grid
  (or a small family) serves all three.
- THE CONTAINER-QUERY INFLECTION (the big modern platform shift Box and
  Stack deferred — like Select's appearance:base-select or Box's
  zero-runtime): Grid's responsiveness is moving from VIEWPORT media queries
  to CONTAINER QUERIES (@container — a grid that responds to its CONTAINER's
  width, not the viewport; shipped ~2023, broadly supported 2023–2024). The
  auto-fit/minmax RAM pattern is intrinsic-responsiveness-without-queries;
  true container queries are the explicit version. Resolve the practice's
  POV (prefer intrinsic / container-query over viewport-breakpoint props
  where possible) and DATE it; it's volatile. Also cover SUBGRID
  (grid-template-columns: subgrid — a nested grid aligning to its parent's
  tracks; ~2023–2024) for the card-content-aligning-across-cards case.
- THE `gap` + THE ROW/COLUMN GAP (and the history contrast): Grid `gap`
  resolves against Box's spacing-token scale (like Stack); note the contrast
  that grid `gap` shipped FIRST (~2018, before flex gap's Safari-14.1/2021
  arrival) — Grid is where `gap` started. row-gap/column-gap.
- ITEM PLACEMENT + SPANNING + THE 2D ALIGNMENT MATRIX: the per-item API
  (Grid.Item/Cell with colSpan/rowSpan, gridColumn/gridRow, gridArea), and
  the FOUR-WAY alignment matrix Grid has that Stack doesn't (justify-items/
  align-items = cells within tracks; justify-content/align-content = tracks
  within the container).
- THE DOM-ORDER-vs-VISUAL-ORDER A11Y TRAP (sharper than Stack's): Grid is a
  presentational div (no role — and beware the NAMING COLLISION: CSS
  display:grid is NOT ARIA role=grid, which is the interactive DATA-GRID
  pattern). grid-template-areas and explicit placement (grid-column/grid-row/
  order) make visual reordering TRIVIAL — so the meaningful-sequence (WCAG
  1.3.2) + focus-order (2.4.3) trap is even sharper than Stack's. Resolve the
  no-reorder rule for Grid (source order must match visual order; place via
  the DOM, not by scattering items with grid-column).

Field-leader systems to survey (web): CSS Grid spec (grid-template-columns/
rows/areas, repeat/minmax/auto-fit/auto-fill, fr, subgrid, gap), Chakra UI
(Grid + GridItem, SimpleGrid minChildWidth/columns — the RAM pattern), MUI
(Grid — the v5 flexbox 12-column → Grid v2/Grid2 CSS-Grid migration; size/
offset), Radix Themes (Grid — columns/rows/areas/gap/flow), Braid/Seek
(Columns/Column + Tiles — the column system + the auto-grid), Shopify Polaris
(Grid + Grid.Cell, InlineGrid — columns per breakpoint), GitHub Primer
(PageLayout + grid utilities), Adobe Spectrum (Grid — areas, the explicit
CSS-Grid mapping), IBM Carbon (Grid/Column — the CSS-Grid + flexbox 16-column
grids), Ant Design (Row/Col — the 24-column grid), Bootstrap (Row/Col — the
12-column legacy reference), Tailwind (grid utilities — grid-cols-N, the
no-component position), Base Web (Uber). WAI-ARIA / HTML (CSS display:grid is
a presentational div — no role; the role=grid COLLISION with the interactive
data-grid pattern; the DOM-order-vs-visual-order meaningful-sequence trap).
Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Box substrate — the as/asChild
Slot, the spacing-token scale, the styling delivery, the logical-property
RTL; note the Stack sibling boundary and the Card/PageLayout/forms hosts;
flag unverified/volatile platform claims under notes.unverified).

1. Framing — what it is (the 2D CSS-Grid layout engine that closes the
   Box→Stack→Grid triad) and what it isn't (Box — the neutral substrate;
   Stack — the 1D engine; an interactive ARIA data grid); the 12-column-vs-
   CSS-Grid divide + the three genres + the container-query inflection up
   front; why systems disagree.
2. Anatomy and parts — the grid container (tracks: columns/rows), the gap,
   the grid items/cells (with span/placement), the template areas, the
   (absence of) visual chrome; subgrid.
3. Properties / API — columns/rows (count or template), gap/rowGap/columnGap
   (→ Box's scale), areas (template), autoFlow, the alignment matrix
   (justify/align items + content), the item API (colSpan/rowSpan/gridArea),
   as/asChild (inherited), responsive vs intrinsic (auto-fit/minmax) vs
   container queries.
4. States and variants — Grid has no interaction states; the genres
   (column-grid / auto-grid-RAM / named-areas), fixed-column vs intrinsic,
   with subgrid; the responsive/container-query variants.
5. Usage guidance — Grid (2D, rows AND columns) vs Stack (1D — reach for
   Stack first; Grid only when you need two-dimensional alignment) vs Box;
   when the column-grid vs the auto-grid vs named-areas; the
   don't-use-Grid-for-1D rule; the intrinsic-over-breakpoint preference.
6. Accessibility — CSS display:grid is a presentational div (inherits Box's
   a11y: the element it renders via as); THE role=grid NAMING COLLISION
   (display:grid ≠ ARIA role=grid / the interactive data grid); THE
   DOM-order-vs-visual-order meaningful-sequence trap (sharper than Stack's
   — areas/grid-column/order make reordering trivial; WCAG 1.3.2 + 2.4.3);
   the no-reorder rule; semantic as where the grid is a list/region.
7. Content guidelines — Grid holds layout, not content; the don't-scatter-
   source-order note; the semantic-markup-for-meaningful-grids rule.
8. Motion and transition — minimal; grid item add/remove/reflow (FLIP),
   reduce-motion; the grid-template animation caveat; Grid ships none.
9. Internationalization — grid flows inline-start→inline-end so it flips
   under RTL via logical properties (inherited from Box); named areas +
   logical placement; column-grid mirroring; no hardcoded left/right
   placement.
10. Naming — Grid / GridItem / Cell / SimpleGrid / Columns+Column / Row+Col /
    InlineGrid / Tiles; the one-Grid-with-genres vs the column-system split;
    the practice's default; aliases; the role=grid collision in naming.
11. Implementation notes — CSS Grid over the reimplemented 12-column float
    system; the auto-fit/minmax RAM idiom; the named-areas template; subgrid;
    container queries over viewport-breakpoint props (+ the @container
    support/date); grid gap (the 2018 head-start over flex gap); the
    item-placement API; the no-reorder enforcement; inheriting Box's Slot +
    scale + logical properties; headless vs opinionated; the MUI Grid→Grid2
    migration.
12. Related and alternative components — typed relationships (STANDS ON Box;
    the 2D SIBLING of Stack; COMPOSED BY Card-galleries/PageLayout-AppShell/
    forms/data-displays; the no-margin discipline shared with Stack; the
    role=grid interactive-data-grid boundary (Table, when briefed); the
    grid-utility-class alternative).
13. Field POV evolution — the 12-column float/flexbox grid → native CSS Grid
    (template-columns/fr/areas); grid `gap` first (2018) then flex gap
    (2021); the auto-fit/minmax RAM pattern → intrinsic responsiveness; the
    container-query shift (~2023) → component-responds-to-container; subgrid
    (~2023–24); the MUI Grid→Grid2 migration; the DOM-order a11y settling.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Grid is — explain the
12-column-legacy-vs-native-CSS-Grid divide (and the MUI Grid→Grid2
migration), the three genres (column-grid / auto-grid-RAM / named-areas) +
how one component serves them, the container-query inflection (+ subgrid)
that is reshaping layout responsiveness, the gap/row-gap (and grid gap's
2018 head-start), the item-placement + 2D alignment matrix, the role=grid
naming collision, and the DOM-order-vs-visual-order meaningful-sequence trap
that is even sharper in Grid than Stack.

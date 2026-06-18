---
okf_version: "0.1"
type: component-brief
title: Grid
description: The 2D CSS-Grid layout engine that closes the Box → Stack → Grid triad — a field-truth study of the 12-column-legacy-vs-native-CSS-Grid divide (layout defined on children vs the parent container; the MUI Grid→Grid2 migration), the three genres (column-grid / auto-grid-RAM / named-areas) and how one component serves them, the container-query inflection (+ subgrid) reshaping layout responsiveness, the gap/row-gap (and grid gap's 2018 head-start over flex gap), the item-placement + 2D alignment matrix (items-within-cells vs tracks-within-container + per-item self-alignment), the role=grid naming collision (CSS display:grid ≠ ARIA role=grid / the interactive data grid), the minmax(0,1fr) blowout guard, and the DOM-order-vs-visual-order meaningful-sequence a11y trap (sharper than Stack's) — standing on Box, the 2D sibling of Stack, with the practice's defaults.
tags: [components, layout]
category: Layout
status: stable
aliases: [GridItem, Grid.Cell, SimpleGrid, Columns, Column, Row, Col, InlineGrid, Tiles, PageLayout, AppShell]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Grid

> A Grid is the **two-dimensional (CSS Grid) layout engine** — it arranges children into explicit **tracks** (columns *and* rows simultaneously) with a token-scaled gap, and it **closes the Box → Stack → Grid layout-engine triad** (Box the neutral substrate, Stack the 1D engine, Grid the 2D engine). Where Stack flows along one axis, Grid places items in a true matrix where horizontal and vertical coordinates stay aligned: a card gallery whose cells align to both a row and a column rhythm, an app shell with a header/sidebar/main/footer template, a form whose labels and fields line up in two columns. It stands on **Box** (inheriting the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, and the logical-property RTL mapping — all inherited, not re-derived; see box), is the **2D sibling of Stack** (see stack), and inherits Stack's **no-external-margin discipline** (Grid owns the gap; children stay flush). Three things define it: **the 12-column legacy vs native CSS Grid** (the float/flexbox `Row`/`Col` fraction-of-N system — layout defined on the *children* — vs native `grid-template-columns`/`-areas`/`fr`/`repeat`/`minmax` defined on the *parent container*; the MUI `Grid`→`Grid2` migration is the worked example); **the three genres** (the column grid, the auto-grid "RAM" pattern, the named-areas template); and **the container-query inflection** (responsiveness moving from the viewport to the container). What it *isn't*: a **Box** (the neutral substrate — Grid *is* the 2D opinion), a **Stack** (the 1D engine — reach for Stack first; Grid only for genuine two-dimensional alignment), or an **interactive ARIA data grid** (`role="grid"` — a *naming collision*: CSS `display: grid` is presentational and has nothing to do with the interactive data-grid pattern).

---

## 1. Framing
Grid manages two-dimensional relationships simultaneously, solving the structural alignment a Stack can't: where items in row 2 must line up vertically with items in row 1. It inherits Box's substrate and Stack's no-margin discipline, and adds the track model.

Three defining concerns, each a place systems diverge:
- **The 12-column legacy vs native CSS Grid.** The historical dividing line is *where the layout is defined*: the **12-column float/flexbox system** (Bootstrap `Row`/`Col`, Ant's 24-column, MUI v5) defines layout on the **children** (`<Col span={6}>`, percentage widths, gutters via negative margins + child padding, nested `Row` wrappers); **native CSS Grid** defines tracks centrally on the **parent container** (`grid-template-columns`, flat markup, native `gap`). The practice ships a CSS-Grid-based component — but the 12-column *mental model* persists, and a `span`-of-N API can survive as a familiar layer over CSS Grid. **MUI's `Grid`→`Grid2`** (flexbox-with-negative-margin-gutters → native CSS Grid + `gap`) is the worked migration: it eliminated the negative-margin overflow bugs, removed the wrapper elements, and added subgrid/auto-track support.
- **The three genres.** (1) the **column grid** (the page-level N-column system, explicit responsive spans); (2) the **auto-grid / "RAM" pattern** (`repeat(auto-fit, minmax(min, 1fr))` — a self-responsive grid that reflows 4→3→2→1 *without media queries*); (3) the **named-areas / template grid** (`grid-template-areas` for explicit 2D placement — the app shell).
- **The container-query inflection.** Grid's responsiveness is moving from *viewport* media queries to *container* queries — the same Grid renders 3 columns in a wide main area and 1 in a narrow sidebar at the *same viewport width* (§11).

What it *isn't*: a **Box** (reach for the constrained engine, not a bare `Box display="grid"`; see box), a **Stack** (the 1D engine — most layouts are 1D; reach for Stack first — see stack), or an **interactive ARIA data grid** (§6). Why systems disagree: the 12-column-vs-CSS-Grid model, the genre coverage, and the responsive mechanism.

## 2. Anatomy and parts
Grid is an invisible structural orchestrator (no chrome of its own — that's Card); two element types and the track model:
- **the grid container** — `display: grid` (or `inline-grid`) establishing a 2D formatting context; holds the **tracks** (`grid-template-columns`/`-rows`) and the gap. Structurally invisible; a semantically neutral `div` (inherits Box's neutrality — §6).
- **the tracks** — the columns and rows: fixed (`200px`), fractional (`1fr`, guarded as `minmax(0, 1fr)` — §11), content-based (`auto`/`min-content`/`max-content`), or generated (`repeat(auto-fit, minmax(…, 1fr))`). The defining structure, declared centrally on the container.
- **the gap** — the space *between* tracks (`gap`/`row-gap`/`column-gap`), resolving against Box's spacing-token scale; like Stack, Grid owns it so children need no margins.
- **the grid items / cells** — the children placed into tracks; a direct child not using an explicit cell is *auto-placed* per `grid-auto-flow`. An optional **`Grid.Item`/`Cell`** controls spanning (`colSpan`), explicit placement (`colStart`/`colEnd`, `area`), and self-alignment overrides. A cell creates no new nesting context unless it declares `display: grid` (or `subgrid`).
- **the template areas** — `grid-template-areas` ASCII-art naming regions (`"header header" "sidebar main"`) for explicit, readable 2D placement.
- **subgrid** — a nested grid using `grid-template-{columns,rows}: subgrid` to align its items to the *parent* grid's tracks (the card-content-aligning-across-cards case — §11).
- **the (absence of) visual chrome** — no background/border/elevation (that's Card); pure layout.

## 3. Properties / API
**Container props (`Grid`):**
- **`columns` / `templateColumns`** — the column tracks: a count (`columns={3}` → `repeat(3, minmax(0, 1fr))`), a template string (`"200px 1fr"`), or the auto-grid (`columns="auto-fit"` + `minChildWidth`/`minItemWidth` → `repeat(auto-fit, minmax(<min>, 1fr))`); **responsive** (`columns={{ base: 1, md: 3 }}`). The headline prop.
- **`rows` / `templateRows`** — the row tracks (often implicit/`auto`; explicit for the named-areas/template case).
- **`gap` / `rowGap` / `columnGap`** — the inter-track space, a token-scale index (resolving against Box's scale). Grid `gap` is where `gap` *started* (~2018 — §13).
- **`areas` / `templateAreas`** — the named-areas template, responsive (areas redefine per breakpoint/container — the sidebar stacks under main when narrow).
- **`autoFlow`** — `row` / `column` / `row dense` / `column dense` — how auto-placed items flow; the `dense` variants backfill gaps (with a reading-order caveat — §6).
- **the alignment matrix (the four-way axis Grid has that Stack doesn't):** `justifyItems`/`alignItems` (each *cell's* content within its track — inline/block) and `justifyContent`/`alignContent` (the *tracks* within the container when they don't fill it). Stack has one cross-axis `align` + one main-axis `justify`; Grid has both pairs.
- **`as` / `asChild`** — inherited from Box (the polymorphic Slot): render the right element (`ul`/`section`/`main`) for semantics (§6).

**Item props (`Grid.Item`):**
- **`colSpan` / `rowSpan`** — span N tracks (`colSpan={2}` → `grid-column: span 2`); `'full'` → `1 / -1` (span all tracks).
- **`colStart` / `colEnd` / `rowStart` / `rowEnd`** — explicit line placement (`grid-column-start`/`-end`).
- **`area`** — place in a named area (`grid-area`).
- **`justifySelf` / `alignSelf`** — per-item alignment overrides (vs the container's `justifyItems`/`alignItems`).

**Responsive vs intrinsic vs container-query (the load-bearing API choice)** — three ways to be responsive: *viewport-breakpoint props* (`columns={{base, md}}` — re-derives media queries), *intrinsic* (`auto-fit`/`minmax` — no breakpoints at all), or *container queries* (`@container` — responds to the container). The practice **prefers intrinsic/container-query over breakpoint props** where the layout allows (§11). Placement on the item, track definition on the container; no margin (the parent's gap), no chrome (Card).

## 4. States and variants
- **States: none.** Grid is layout-only — no hover/focus/active/disabled (inherits Box's statelessness). An interactive element rendered via `as`/`asChild` carries the states.
- **Variants (genres + mechanisms, not visual variants):**
  - **genre:** column-grid (page-level N columns, explicit spans) / auto-grid (the RAM `auto-fit`/`minmax` pattern, for uniform card galleries) / named-areas (the app-shell template).
  - **track sizing:** fixed-column (explicit count/template) vs **intrinsic** (`auto-fit`/`minmax`, content-driven).
  - **responsive mechanism:** viewport-breakpoint props / intrinsic / container queries.
  - **with subgrid** (nested track alignment) vs independent nested grids.
  - **rendered element:** the `as` target (`div`/`ul`/`section`/`main`).

## 5. Usage guidance
- **Use a Grid for genuine two-dimensional alignment:** a gallery of cards aligning to both row and column rhythm; an app shell (header/sidebar/main/footer); a form whose labels and fields align in columns across rows; a dashboard of tiles. The test: *if items in row 2 must align vertically with items in row 1, it's a Grid.*
- **Stack-first (the load-bearing rule):** **reach for Stack before Grid.** Most layouts are one-dimensional — a column of sections, a row of buttons, a wrapping row of tags — and a Stack is simpler and more robust. **The anti-pattern: no 1D Grid.** A `<Grid columns={1}>` wrapping a list is over-engineering — it duplicates Stack's job and adds layout-calculation cost; use `<Stack>` (see stack).
- **Genre selection:**
  - uniform, self-reflowing cells (a card gallery, product matrix, search results) → the **auto-grid** (`auto-fit`/`minmax`) — no breakpoints needed.
  - a fixed page-level column count that changes at breakpoints (a landing-page hero grid) → the **column grid** or container queries.
  - a fixed asymmetric structure with named regions (app bars, consoles, page shells) → **named areas**.
- **The intrinsic-over-breakpoint preference:** prefer `auto-fit`/`minmax` (and container queries) over hand-authored viewport columns where the content allows — the grid then responds to *available space*, surviving being dropped into a narrow sidebar (which viewport breakpoints don't).
- **Don't scatter source order** — never use `area`/`colStart`/`order` to place *meaningful* items visually away from their DOM order (§6); arrange the DOM, then let the grid place in source order.
- **Don't add chrome to a Grid** — background/border/elevation means nesting a styled container *inside* the Grid (or a **Card**), not styling the Grid itself (§7).

## 6. Accessibility
Grid inherits Box's a11y story — **a presentational `div` (no role, no name), so the accessibility surface is the element it renders via `as`/`asChild`** (see box). Two Grid-specific points:

- **The `role="grid"` naming collision (flag it loudly).** CSS **`display: grid` is purely presentational** and has **nothing to do with ARIA `role="grid"`** — which is the *interactive data-grid* pattern (a spreadsheet-like widget of focusable `gridcell`s in `row`s, arrow-key cell navigation; the pattern Tag's removable-token group borrows and Table will use). A layout Grid must **never** carry `role="grid"` — a false role promises a keyboard interaction model that isn't there. Keep layout containers presentationally neutral. (CSS `display: grid` ≠ ARIA `role=grid`.)
- **The DOM-order-vs-visual-order trap — sharper than Stack's.** Grid makes visual reordering *trivial*: `grid-template-areas`, explicit placement (`colStart`/`rowStart`), `order`, and `grid-auto-flow: dense` can put any item anywhere on screen regardless of its DOM position. But screen readers and the Tab key follow the **DOM**, so a grid that scatters items visually away from source order produces a reading/focus order that mismatches the visual order — a **WCAG 1.3.2 (Meaningful Sequence)** + **2.4.3 (Focus Order)** failure, and *easier to commit* in Grid than in Stack because placement-anywhere is one prop away. **The rule (the no-reorder discipline, applied harder):** *the visual layout order of focusable items must match their source order in the DOM* — if an item should appear first visually, declare it first in the DOM. Reserve explicit-placement-away-from-source for purely-presentational, no-meaning arrangements; `grid-auto-flow: dense` reorders to backfill, so use it only where order is meaningless.
- **Semantic `as`** — a grid that is a *list* → `as="ul"` with `Grid.Item as="li"`; an app-shell grid → real landmark elements as the items (`main`/`aside`/`header`). Don't leave a meaningful structure a neutral `div` (1.3.1).
- **WCAG SCs:** **1.3.2** (meaningful sequence — the no-reorder rule, the sharp one), **2.4.3** (focus order), **1.3.1** (info & relationships — semantic `as`), **4.1.2** (a false `role=grid` is worse than none). The light a11y of a layout primitive, with the two real caveats.

## 7. Content guidelines
- Grid **holds layout, not content** — no copy of its own (like Box/Stack).
- **Separate layout from styling — don't style the Grid.** A Grid's sole responsibility is the track structure and spacing; it must not carry borders, backgrounds, shadows, or scroll behavior. If a region needs visual chrome, **nest a styled container (or a Card) inside the grid item**, don't put the chrome on the Grid (`<Grid><div className="card-surface">…</div></Grid>`, not `<Grid className="card-surface">`).
- **Don't scatter source order** — the DOM content order should be the intended reading order; don't rely on grid placement to "fix" a DOM authored in the wrong order (it fixes the eye, not the screen reader — §6).
- **Semantic markup for meaningful grids** — a list/regions/app-shell grid → encode it (`as="ul"`/`<li>`, landmarks), not visual-only.

## 8. Motion and transition
- Grid ships **no motion of its own** (like Box/Stack) — track calculation and placement execute at layout/paint.
- **Item add/remove/reflow** — when items enter/leave/reorder, the grid reflows; animate the *child elements'* transition paths with **FLIP** (the same technique Stack and Tag use — see stack, tag), **not the grid tracks directly**; applied by the consumer or an animation primitive via `asChild`.
- **The grid-template animation constraint** — transitioning `grid-template-columns`/`-rows` (a collapsing sidebar track) is *not* smoothly supported across all engines and can jitter; for resizing panels, animate the child's `width`/`transform` rather than the tracks.
- **Reduce-motion** — gate any reflow/track animation behind `prefers-reduced-motion: reduce` (instant layout); Grid is motion-neutral.

## 9. Internationalization
- **Grid flows inline-start → inline-end**, so a column grid mirrors under RTL automatically: with `dir="rtl"` the first column sits on the right and columns flow left, and the `gap` (logical) applies along the flow — **no JS**.
- **Logical placement over physical** — track alignment maps to logical equivalents (`justifyItems: start` → left in LTR, right in RTL automatically), and `grid-column: 1 / -1` scales correctly because track lines start from the logical inline-start. A grid placing by *line number / named area* is RTL-correct; one positioning by physical pixel offset is not (Box's logical-property mapping, inherited, handles offsets).
- **Named areas mirror** — `grid-template-areas` follow the writing direction; an app-shell `"navigation main"` puts the navigation inline-start (right in RTL) automatically. Name areas by *semantic role*, not physical position.
- Grid is otherwise i18n-neutral (no text of its own).

## 10. Naming
- **The field set:** **`Grid`** + **`Grid.Item`/`Grid.Cell`** (the unified pattern — Radix Themes, MUI, Polaris, Spectrum, Carbon, Base Web); **`Grid`/`SimpleGrid`** + **`GridItem`** (Chakra — the auto-grid split out as `SimpleGrid` with `minChildWidth`); **`Row`/`Col`** (Bootstrap 12-column, Ant 24-column — the legacy fraction-of-N); **`Columns`/`Column`** + **`Tiles`** (Braid — the column system + the auto-grid); **`InlineGrid`** (Polaris); **`PageLayout`** (Primer — the app-shell template as a named component).
- **The practice's default — `Grid` + `Grid.Item`** for the explicit CSS-Grid engine (columns/rows/areas/gap + per-item span/placement/self-alignment), plus a **`minChildWidth`/`minItemWidth` convenience** on `Grid` for the auto-grid RAM pattern (friendlier than authoring `repeat(auto-fit, minmax(…))` — Chakra ships this as a separate `SimpleGrid`, but a prop keeps it one component). The page-level **column system** is the same `Grid` with a `columns` count (one fewer concept than a separate `Columns`); the **app shell** is a composed *pattern* (a Grid with named areas), though a named `PageLayout` earns its place at the app level.
- **The `role=grid` collision in naming** — name the *component* `Grid` (CSS layout) but never emit `role="grid"` (ARIA data grid); the unified `Grid` + `Grid.Item` naming also cleanly avoids colliding with an interactive `DataGrid`/`Table` (§6).
- **Aliases to map:** GridItem, Grid.Cell, SimpleGrid, Columns, Column, Row, Col, InlineGrid, Tiles, PageLayout, AppShell.

## 11. Implementation notes
- **CSS Grid over the reimplemented 12-column float system.** Build on native `grid-template-columns`/`-rows`/`-areas` + `fr`/`minmax`/`repeat`, not a float/flexbox `Row`/`Col` reimplementation. A `span`-of-N API can survive as a *familiar layer* mapping to `grid-column: span N` over a 12/16-track grid. **MUI's `Grid`→`Grid2`** (flexbox-negative-margin-gutters → CSS Grid + native `gap`) is the worked migration — it killed the horizontal-overflow bugs, removed the padding-reset wrapper elements, and added subgrid/auto-track support.
- **The `minmax(0, 1fr)` blowout guard (the recurring trap).** Map `columns={N}` to **`repeat(N, minmax(0, 1fr))`**, *not* `repeat(N, 1fr)`. A bare `1fr` has an implicit `min-width: auto` (= the content's min-size), so a long unbreakable string or a wide child **blows out the track** and overflows the grid; `minmax(0, 1fr)` lets the track shrink below its content. The single most common CSS-Grid bug.
- **The auto-grid / RAM idiom** — `grid-template-columns: repeat(auto-fit, minmax(min(<min>, 100%), 1fr))` reflows the column count to fit the available width *with no media queries*; the `min(<min>, 100%)` guard prevents overflow when the container is narrower than `<min>`. Expose as `minChildWidth`/`minItemWidth`. **`auto-fit`** (collapse empty tracks so items stretch to fill) vs **`auto-fill`** (keep empty tracks) is the one real knob.
- **The named-areas template** — `grid-template-areas` is the most readable 2D placement for fixed structures; items reference areas by name (`area="sidebar"`). Pair with responsive/container-query area redefinition (the sidebar stacks under main on narrow containers).
- **Subgrid** — `grid-template-{columns,rows}: subgrid` lets a nested grid (e.g., a Card spanning rows) align its internal tracks to the parent grid's, so content *across* sibling cards lines up (titles, body, CTA rows). Achieved **universal browser support ~early 2024**; a real capability for card galleries (flag for support-dating).
- **Container queries over viewport-breakpoint props (the inflection).** Prefer `@container` (the grid responds to its *container's* width) over `columns={{base, md}}` (viewport media queries) — a container-query grid survives being dropped into a narrow sidebar, where viewport breakpoints guess wrong. Setup: the parent declares `container-type: inline-size` (+ optional `container-name`), the grid keys off `@container`. Container queries reached broad support **~early 2023**; the auto-fit/minmax RAM pattern is the intrinsic, query-less version of the same goal. *Date this — it's the volatile claim, like Box's zero-runtime.*
- **Grid `gap`'s head-start** — grid `gap` shipped ~**2018**, well before flex `gap` (Safari 14.1 / 2021 — see stack); Grid never needed the lobotomized-owl margin hacks or the negative-margin gutter calc Stack/12-column systems did.
- **The item-placement API** — `Grid.Item` maps `colSpan`→`grid-column: span N` (`'full'`→`1 / -1`), `area`→`grid-area`, `colStart/End`→explicit lines, `justifySelf/alignSelf`→self-alignment, with responsive values. Placement on the item, track definition on the container.
- **The no-reorder enforcement** — a lint/review rule against `area`/`colStart`/`order`/`dense` placing meaningful content away from DOM order (§6).
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL all come from Box (see box); Grid adds only the 2D track + gap + areas + placement + alignment-matrix delta.
- **Headless vs opinionated** — a thin opinionated layer on CSS Grid + the token scale (no state, no a11y machinery beyond `as`); ship as a styled layout primitive — the value is the constrained, token-bound, intent-revealing API (and the `minChildWidth` convenience + the `minmax(0,1fr)` guard) over raw grid.

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, the logical-property RTL — all inherited; see box).
- **2D sibling of:** **Stack** (the 1D engine — Stack is one axis, Grid is rows × columns; reach for Stack first, Grid only for genuine 2D alignment; the two close the Box→Stack→Grid triad — see stack). Grid inherits Stack's **no-external-margin discipline** (it owns the gap).
- **Composed by / hosts:** **card galleries** (the auto-grid of Cards, aligned equal-height via subgrid — see card), **PageLayout/AppShell** (the named-areas template), **forms** (label/field column alignment), and **data displays** (dashboards of tiles).
- **Boundary (the naming collision):** the **interactive ARIA data grid** (`role="grid"`) / **Table** — a tabular widget with cell navigation and explicit semantic roles (the pattern Tag's removable-token group borrows; Table not yet briefed). A layout Grid is *not* that and must not claim its role (§6).
- **Alternative to:** a bare **Box** (`display="grid"` by hand — the constrained-over-open smell; see box), a **Stack** (for 1D — the simpler reach), and **grid utility classes** (Tailwind's `grid grid-cols-3 gap-4` — the no-component position).

(The second Layout engine — the 2D CSS-Grid component that closes the Box→Stack→Grid triad. It stands on Box (inheriting the Slot, the scale, the RTL), is the 2D sibling of Stack (reach for Stack first), and is composed by card galleries / PageLayout / forms. See box for the substrate, stack for the 1D sibling + the FLIP reflow it shares, card for the gallery cell (+ subgrid equal-height), section/table when briefed for the hosts + the role=grid data-grid boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The 12-column float/flexbox grid → native CSS Grid (the engine realignment).** The responsive-grid-system era defined layout on the *children* (Bootstrap `Row`/`Col`, percentage widths, the float then flexbox 12/24-column systems with negative-margin gutters); native CSS Grid moved the definition to the *parent container* (`grid-template-columns`/`-areas`, `fr`, `repeat`/`minmax`) with flat markup. **MUI's `Grid`→`Grid2`** rebuild captures the migration.
2. **Grid `gap` first (2018), then flex `gap` (2021).** `gap` shipped in CSS Grid years before flexbox got it (Safari 14.1) — Grid never needed the lobotomized-owl hacks or negative-margin gutter calc the earlier systems carried.
3. **The auto-fit/minmax RAM pattern → intrinsic responsiveness.** `repeat(auto-fit, minmax(…, 1fr))` let grids reflow their column count with *zero* media queries — the column count became a function of available space, not a guessed breakpoint.
4. **The container-query shift (~early 2023).** `@container` moved responsiveness from the viewport to the *container* — a component now responds to where it's placed, not the window size; the biggest layout-responsiveness change since CSS Grid itself, and the natural successor to viewport-breakpoint props.
5. **Subgrid (~early 2024).** `subgrid` reached universal support and let nested grids align to their parent's tracks, solving the long-standing card-content-alignment problem.
6. **The DOM-order-vs-visual-order a11y settling.** As with Stack, the recognition that explicit placement breaks meaningful sequence (1.3.2) + focus order (2.4.3) hardened the no-reorder rule — sharper in Grid because placement-anywhere is one prop away.

## 14. Sources cited
(Conservative; reconcile with external — and the container-query/subgrid support dates are volatile, so platform-state claims are flagged unverified.) **CSS Grid Layout Module Level 1 & 2** (W3C, updated 2023/2024) — `grid-template-columns`/`-rows`/`-areas`, `repeat`/`minmax`/`auto-fit`/`auto-fill`, `fr`, `subgrid`, `gap`; **Chakra UI** — `Grid` + `GridItem`, `SimpleGrid` (`minChildWidth`/`columns` — the RAM pattern) (2024–2026); **MUI** — `Grid` (the v5 flexbox 12-column → `Grid2`/`Grid v2` CSS-Grid migration; `size`/`offset`) (2024–2026); **Radix Themes** — `Grid` (`columns`/`rows`/`areas`/`gap`/`flow`; `asChild`/Slot) (2024–2026); **Braid / Seek** — `Columns`/`Column` + `Tiles` (the column system + the auto-grid; 1D-vs-2D logic) (2024–2026); **Shopify Polaris** — `Grid` + `Grid.Cell`, `InlineGrid` (columns per breakpoint) (2024–2026); **GitHub Primer** — `PageLayout` + grid utilities (2024–2026); **Adobe Spectrum** — `Grid` (areas, the explicit CSS-Grid mapping) (2024–2026); **IBM Carbon** — `Grid`/`Column` (the CSS-Grid + flexbox 16-column grids) (2024–2026); **Ant Design** — `Row`/`Col` (the 24-column grid) (2024–2026); **Bootstrap** — `Row`/`Col` (the 12-column legacy reference); **Tailwind** — `grid` utilities (`grid-cols-N` — the no-component position) (2024–2026); **Base Web (Uber)** — the responsive grid (2024); **WAI-ARIA / HTML** — CSS `display: grid` is a presentational `div` (no role); the **`role="grid"` collision** with the interactive data-grid pattern; the DOM-order-vs-visual-order meaningful-sequence trap. WCAG 2.2 (W3C Recommendation, Oct 2023) — 1.3.2, 2.4.3, 1.3.1, 4.1.2. CSS — grid `gap` (~2018); container queries `@container` (~early 2023); `subgrid` (~early 2024).

## 15. Agent-consumable schema

```yaml
identity:
  id: grid
  name: Grid
  aliases: [GridItem, Grid.Cell, SimpleGrid, Columns, Column, Row, Col, InlineGrid, Tiles, PageLayout, AppShell]
  category: layout
  status: stable
description: >
  The two-dimensional (CSS Grid) layout engine — arranges children into explicit
  tracks (columns AND rows) with a token-scaled gap; closes the Box → Stack → Grid
  layout-engine triad (Box substrate, Stack 1D, Grid 2D). NOT a Box (the neutral
  substrate — Grid IS the 2D opinion), NOT a Stack (the 1D engine — reach for Stack
  first; Grid only for genuine two-dimensional alignment), NOT an interactive ARIA
  data grid (role=grid — a naming collision; CSS display:grid is presentational).
  Stands on Box (the as/asChild Slot, the spacing-token scale, the styling delivery,
  the logical-property RTL); the 2D sibling of Stack; inherits Stack's no-external-
  margin discipline; composed by card galleries/PageLayout/forms/data displays.
anatomy:
  parts:
    - "the grid container: display:grid (or inline-grid) establishing a 2D formatting context; holds the tracks + gap; structurally invisible; a semantically neutral div"
    - "the tracks (columns/rows): fixed (200px) / fractional (1fr, guarded minmax(0,1fr)) / content (auto/min-content) / generated (repeat(auto-fit, minmax)); declared centrally on the CONTAINER (vs the 12-column legacy's per-child definition)"
    - "the gap (gap/row-gap/column-gap): the space BETWEEN tracks, resolving against Box's spacing-token scale; Grid owns it (children need no margins)"
    - "the grid items/cells: auto-placed (per grid-auto-flow) or an explicit Grid.Item/Cell controlling span/placement/self-alignment; a cell creates no nesting context unless it declares display:grid/subgrid"
    - "the template areas: grid-template-areas ASCII-art region naming for explicit readable 2D placement (the app shell)"
    - "subgrid: a nested grid (grid-template-{columns,rows}:subgrid) aligning its items to the PARENT grid's tracks (card-content-alignment; ~early 2024 universal support)"
    - "(absence of) visual chrome: no bg/border/elevation (that's Card); pure layout"
api:
  inherits:
    - box        # the as/asChild Slot, the spacing-token scale (gap resolves against it), the zero-runtime delivery, the logical-property RTL
  container-props:
    - {name: columns/templateColumns, type: "number | template | responsive | auto-grid(minChildWidth)", default: ~, required: false, description: "the column tracks: count (->repeat(N, minmax(0,1fr))) / template string / auto-grid (columns='auto-fit' + minChildWidth -> repeat(auto-fit, minmax)); responsive (columns={{base:1,md:3}})"}
    - {name: rows/templateRows, type: "number | template", default: auto, required: false, description: "the row tracks (often implicit/auto; explicit for named-areas)"}
    - {name: gap/rowGap/columnGap, type: "token-scale", default: ~, required: false, description: "the inter-track space, a token index (resolving against Box's scale); Grid is where gap STARTED (~2018)"}
    - {name: areas/templateAreas, type: "responsive string[]", default: ~, required: false, description: "named-areas template (the app-shell genre); redefines per breakpoint/container"}
    - {name: autoFlow, type: "'row'|'column'|'row dense'|'column dense'", default: row, required: false, description: "how auto-placed items flow; 'dense' backfills (reading-order caveat — a11y)"}
    - {name: "justifyItems/alignItems", type: enum, default: stretch, required: false, description: "each CELL's content within its track (inline/block) — the matrix Stack lacks"}
    - {name: "justifyContent/alignContent", type: enum, default: "start (+ space-between/around/evenly)", required: false, description: "the TRACKS within the container when they don't fill it"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — render the right element (ul/section/main) for semantics"}
  item-props:
    - {name: "colSpan/rowSpan", type: "number | 'full' | responsive", default: ~, required: false, description: "span N tracks (->grid-column:span N); 'full' -> 1 / -1 (all tracks)"}
    - {name: "colStart/colEnd/rowStart/rowEnd", type: "number | 'auto' | responsive", default: auto, required: false, description: "explicit line placement (grid-column-start/-end)"}
    - {name: area, type: "responsive string", default: ~, required: false, description: "place in a named area (grid-area)"}
    - {name: "justifySelf/alignSelf", type: enum, default: ~, required: false, description: "per-item alignment override (vs the container's justifyItems/alignItems)"}
  responsive-mechanism: "VIEWPORT-breakpoint props (columns={{base,md}} — re-derives media queries) vs INTRINSIC (auto-fit/minmax — no breakpoints) vs CONTAINER QUERIES (@container — responds to the container). Practice PREFERS intrinsic/container-query over breakpoint props where the layout allows"
  withholds: "no margin (parent's gap), no chrome (Card — nest a styled container inside)"
states:
  runtime: []   # NONE — layout-only, inherits Box's statelessness; an interactive element via as/asChild carries the states
variants:
  genre: [column-grid, auto-grid-RAM, named-areas]
  track-sizing: [fixed-column, intrinsic]   # explicit count/template vs auto-fit/minmax content-driven
  responsive-mechanism: [viewport-breakpoint-props, intrinsic, container-queries]
  subgrid: [with-subgrid, independent-nested]
  rendered-element: "the as target (div/ul/section/main)"
accessibility:
  inherits: [box (presentational div; the element it renders via as is the whole story)]
  wcag-criteria: ["1.3.2", "2.4.3", "1.3.1", "4.1.2"]
  role-grid-COLLISION: "CSS display:grid is PRESENTATIONAL and has NOTHING to do with ARIA role=grid (the interactive DATA-GRID pattern — spreadsheet-like focusable gridcells in rows, arrow-key nav; Tag's removable-token group borrows it, Table uses it). A layout Grid must NEVER carry role=grid (a false role promises an interaction model that isn't there)"
  DOM-vs-visual-order-trap: "SHARPER than Stack's — grid-template-areas/colStart/rowStart/order/auto-flow:dense make placing any item anywhere TRIVIAL; SR + Tab follow the DOM, so scattering items visually away from source order breaks reading/focus order (WCAG 1.3.2 + 2.4.3) and is EASIER to commit than in Stack (one prop away)"
  no-reorder-rule: "the visual layout order of focusable items MUST match their source order in the DOM; if an item should appear first visually, declare it first in the DOM. Reserve explicit-placement-away-from-source for purely-presentational no-meaning arrangements; auto-flow:dense only where order is meaningless"
  semantic-as: "a grid that's a LIST -> as='ul' + Grid.Item as='li'; an app-shell grid -> real landmark elements as items (main/aside/header); don't leave a meaningful structure a neutral div (1.3.1)"
content:
  holds-layout-not-content: "no copy of its own (like Box/Stack)"
  no-style-the-grid: "a Grid's sole job is tracks + spacing — NO borders/bg/shadow/scroll on the Grid; nest a styled container (or a Card) INSIDE the grid item (<Grid><div class='surface'>...) not <Grid class='surface'>"
  no-scatter-source-order: "the DOM content order = the intended reading order; don't use grid placement to 'fix' a wrongly-ordered DOM (fixes the eye, not the SR)"
  semantic-markup: "a list/regions/app-shell grid -> encode it (as='ul'/li, landmarks), not visual-only"
motion:
  own: none   # track calc + placement execute at layout/paint
  reflow: "items add/remove/reorder -> grid reflows; FLIP on the CHILD elements (not the tracks directly), same as Stack/Tag, applied by the consumer/an animation primitive via asChild"
  grid-template-animation-constraint: "transitioning grid-template-columns/rows is NOT smoothly supported across all engines + can jitter; for resizing panels animate the child's width/transform, not the tracks"
  reduce-motion: "gate any reflow/track animation behind prefers-reduced-motion -> instant layout; Grid is motion-neutral"
i18n:
  flows-inline-start-to-end: "a column grid mirrors under RTL automatically (dir=rtl: first column on the right, columns flow left; the logical gap applies along the flow) — no JS"
  logical-placement: "track alignment maps to logical (justifyItems:start -> left in LTR, right in RTL); grid-column:1/-1 scales (lines start from inline-start); place by line/area not physical offset (Box's logical-property mapping handles offsets)"
  named-areas-mirror: "grid-template-areas follow the writing direction (an app-shell 'navigation main' puts navigation inline-start = right in RTL automatically); name areas by semantic role not physical position"
  otherwise: "i18n-neutral (no text of its own)"
implementation:
  - "CSS Grid over the reimplemented 12-column FLOAT system: native grid-template-columns/-rows/-areas + fr/minmax/repeat, not a float/flexbox Row/Col reimpl. A span-of-N API can survive as a FAMILIAR LAYER over CSS Grid. MUI's Grid->Grid2 (flexbox negative-margin gutters -> CSS Grid + gap) is the worked migration (killed overflow bugs, removed wrapper elements, added subgrid)"
  - "the minmax(0,1fr) BLOWOUT GUARD (the recurring trap): map columns={N} to repeat(N, minmax(0,1fr)) NOT repeat(N,1fr) — a bare 1fr has implicit min-width:auto (= content min-size), so a long unbreakable string/wide child blows out the track + overflows; minmax(0,1fr) lets it shrink. The most common CSS-Grid bug"
  - "the auto-grid/RAM idiom: repeat(auto-fit, minmax(min(<min>,100%),1fr)) reflows column count to fit WITH NO media queries; the min(,100%) guard prevents overflow when narrower than <min>; expose as minChildWidth/minItemWidth. auto-fit (collapse empty tracks, items stretch) vs auto-fill (keep them) is the one knob"
  - "the named-areas template: grid-template-areas = the most readable 2D placement for fixed structures; items reference by name (area='sidebar'); pair with responsive/container-query area redefinition"
  - "subgrid (grid-template-{columns,rows}:subgrid): a nested grid aligns its tracks to the parent's so content ACROSS sibling cards lines up; ~early 2024 universal support (flag dating)"
  - "container queries over viewport-breakpoint props (the inflection): prefer @container (responds to the CONTAINER's width) over columns={{base,md}} (viewport media queries) — survives a narrow sidebar. Setup: parent sets container-type:inline-size (+ container-name), grid keys off @container. ~early 2023 broad support; auto-fit/minmax is the intrinsic query-less version. DATE IT (volatile, like Box's zero-runtime)"
  - "grid gap's head-start: grid gap shipped ~2018, before flex gap (Safari 14.1/2021) — Grid never needed the lobotomized-owl hacks or negative-margin gutter calc"
  - "the item-placement API: Grid.Item maps colSpan->grid-column:span N ('full'->1/-1), area->grid-area, colStart/End->lines, justifySelf/alignSelf->self-alignment, responsive; placement on the item, tracks on the container"
  - "no-reorder enforcement: a lint/review rule against area/colStart/order/dense placing meaningful content away from DOM order"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Grid adds only the 2D track + gap + areas + placement + alignment-matrix delta"
  - "headless vs opinionated: a thin opinionated layer on CSS Grid + the token scale (no state, no a11y beyond as); ship as a styled layout primitive — the value is the constrained token-bound intent-revealing API + the minChildWidth convenience + the minmax(0,1fr) guard over raw grid"
composition:
  stands-on: [box]
  sibling-of: [stack]                      # 1D vs 2D; closes the Box->Stack->Grid triad; reach for Stack first
  inherits-discipline: "Stack's no-external-margin (Grid owns the gap)"
  composed-by: [card, "PageLayout/AppShell", "forms", "data displays"]   # card galleries, app shells, label/field alignment, dashboards
  boundary: ["interactive ARIA data grid (role=grid)", table]   # the naming collision; a layout Grid is NOT a data grid (Table not yet briefed)
  alternative-to: ["bare Box display=grid (the constrained-over-open smell)", stack, "grid utility classes (Tailwind no-component position)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the 12-column legacy API (Row/Col span-of-N, layout-on-children — Bootstrap/Ant/MUI-v5) vs native CSS Grid (template-columns/fr/areas, layout-on-parent — practice default); a span API can survive as a familiar layer over CSS Grid"
    - "one Grid serving all three genres (columns count / auto-grid via minChildWidth / named-areas) vs a split (SimpleGrid + Columns/Column + PageLayout)"
    - "responsive mechanism: viewport-breakpoint props vs intrinsic (auto-fit/minmax) vs container queries (practice: prefer intrinsic/container-query)"
    - "N for the column system (12 Bootstrap/MUI, 24 Ant, 16 Carbon) — or skip a fixed N for fr/auto-fit"
  trap:
    - "carrying role=grid onto a layout Grid (it's the INTERACTIVE data-grid ARIA pattern — CSS display:grid != ARIA role=grid)"
    - "the DOM-order-vs-visual-order trap, SHARPER than Stack's: areas/colStart/rowStart/order/dense scattering meaningful content away from source order (WCAG 1.3.2 + 2.4.3) — arrange the DOM, place in source order"
    - "repeat(N, 1fr) without the minmax(0,1fr) guard -> track blowout/overflow on long content (the most common CSS-Grid bug)"
    - "auto-fit/minmax without the min(,100%) guard -> overflow when the container is narrower than the min"
    - "styling the Grid itself (border/bg/shadow) -> nest a styled container/Card inside; putting margin on grid children -> use gap (the no-external-margin principle)"
    - "using Grid for 1D work (a single column / a row that should just wrap) -> Stack; a bare Box display=grid by hand (the constrained-over-open smell)"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL, the presentational-div a11y; Stack's no-external-margin discipline"
  role-in-family: "the second Layout engine — the 2D CSS-Grid component that closes the Box->Stack->Grid triad; stands on Box, the 2D sibling of Stack (reach for Stack first), composed by card galleries/PageLayout/forms"
  evolution:
    - "the 12-column float/flexbox grid (layout-on-children) -> native CSS Grid (template-columns/fr/areas, layout-on-parent); MUI Grid->Grid2"
    - "grid gap first (~2018) then flex gap (Safari 14.1/2021)"
    - "the auto-fit/minmax RAM pattern -> intrinsic responsiveness without media queries"
    - "the container-query shift (~early 2023) -> component-responds-to-container (the natural successor to viewport-breakpoint props)"
    - "subgrid (~early 2024) -> nested-grid track alignment"
    - "the DOM-order-vs-visual-order a11y settling (the no-reorder rule, sharper in Grid)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "container-query (@container, ~early 2023) + subgrid (~early 2024) support dates — verify against current baseline"
    - "the MUI Grid->Grid2 migration/default state; per-system column-count N + genre coverage"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-grid/` (16 June 2026), the thirty-seventh brief and the **second Layout engine** — the 2D CSS-Grid component that **closes the Box → Stack → Grid layout-engine triad** (the third Layout brief). It stands on Box (inheriting the `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime delivery, and the logical-property RTL — not re-derived), is the 2D sibling of Stack (reach for Stack first), and inherits Stack's no-external-margin discipline. The two passes converged with no genuine fork — the 12-column-legacy-vs-native-CSS-Grid divide, the three genres (column / auto-grid-RAM / named-areas), the container-query inflection, the gap/row-gap, the item-placement + 2D alignment matrix, the `role=grid` naming collision, and the DOM-order-vs-visual-order trap (sharper than Stack's). The external pass sharpened with concrete detail: the **defined-on-children-vs-parent** framing of the 12-column divide, the precise **MUI `Grid`→`Grid2`** mechanics (negative-margin gutters → native `gap`), the fuller **item-placement API** (`colStart`/`colEnd`/`rowStart`/`rowEnd` line placement, `colSpan="full"`→`1 / -1`, per-item `justifySelf`/`alignSelf`), the **`minmax(0, 1fr)` blowout guard** (the most common CSS-Grid bug — `1fr`'s implicit `min-width: auto` overflowing on long content), the **nest-a-styled-container-inside-the-Grid** content rule (don't style the Grid), the **`container-type: inline-size`** setup, and the **container-query ~early-2023 / subgrid ~early-2024** dating. Claude-pass contributions: the triad-closing framing, the substrate-and-sibling inheritance map (Box delta + Stack discipline), the Stack-first / no-1D-Grid usage rule, the genre-selection framework, and the `role=grid`-collision discipline. The container-query/subgrid support dates and the MUI migration state are flagged unverified (the volatile platform claim, like Box's zero-runtime and Stack's Safari-14.1). Conformant to `components/_schema.md`. **With Grid, the Box → Stack → Grid layout-engine triad is complete** — the cleanest sub-system closure since the three-loading-patterns triad, and the layout foundation Card and Section will be built on.*

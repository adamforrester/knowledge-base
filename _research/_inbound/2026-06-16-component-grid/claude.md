# Grid — field-truth study (Claude pass)

## 1. Framing
A Grid is the **two-dimensional (CSS Grid) layout engine** — it arranges children into explicit **tracks** (columns *and* rows simultaneously) with a token-scaled gap, and it **closes the Box → Stack → Grid layout-engine triad** (Box the neutral substrate, Stack the 1D engine, Grid the 2D engine). Where Stack flows along one axis, Grid places items in a true matrix: a card gallery whose cells align to both a row and a column rhythm regardless of content height, an app shell with a header/sidebar/main/footer template, a form whose labels and fields line up in two columns.

Three things define it and are where systems diverge:
- **The 12-column legacy vs native CSS Grid.** The historical divide: the float/flexbox **12-column responsive grid system** (Bootstrap `Row`/`Col`, Ant's 24-column, the `<Col span={6}>` fraction-of-N model with gutters and nesting) vs **native CSS Grid** (`grid-template-columns`, `repeat()`/`minmax()`, `fr` units, `auto-fit`/`auto-fill`, `grid-template-areas`). The practice ships a *CSS-Grid-based* component, not a reimplemented float system — but the 12-column *mental model* persists (MUI's `Grid`→`Grid2` migration from flexbox to CSS Grid is the worked example).
- **The three genres.** (1) the **layout / column grid** (the page-level N-column system); (2) the **auto-grid / "RAM" pattern** (`repeat(auto-fit, minmax(min, 1fr))` — a self-responsive grid that reflows 4→3→2→1 *without media queries*); (3) the **named-areas / template grid** (`grid-template-areas` for explicit 2D placement — the app shell).
- **The container-query inflection.** Grid's responsiveness is moving from *viewport* media queries to *container* queries (a grid that responds to its container's width) — the big modern layout shift (§ below, §11).

It stands on **Box** (inheriting the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, and the logical-property RTL mapping — all inherited, not re-derived; see box), is the **2D sibling of Stack** (see stack), and inherits Stack's **no-external-margin discipline** (Grid owns the gap; children stay flush). It is composed by card galleries, PageLayout/AppShell, forms, and data displays. What it *isn't*: a **Box** (the neutral, layout-agnostic substrate — Grid *is* the 2D opinion), a **Stack** (the 1D engine — reach for Stack first; Grid only when you genuinely need two-dimensional alignment), or an **interactive ARIA data grid** (`role="grid"` — a *naming collision*: CSS `display: grid` is presentational and has nothing to do with the interactive data-grid ARIA pattern — §6). Why systems disagree: the 12-column-vs-CSS-Grid model, the genre coverage, and the responsive mechanism (breakpoint props vs intrinsic vs container queries).

## 2. Anatomy and parts
Grid is an invisible structural orchestrator (no chrome of its own — that's Card); its parts are the track model:
- **the grid container** — `display: grid` establishing a grid formatting context; defines the **tracks** (`grid-template-columns` / `grid-template-rows`) and the gap. Semantically a neutral `div` (inherits Box's neutrality — §6).
- **the tracks** — the columns and rows: fixed (`200px`), fractional (`1fr`), content-based (`auto`/`min-content`/`max-content`), or generated (`repeat(auto-fit, minmax(…, 1fr))`). The defining structure.
- **the gap** — the space *between* tracks (`gap`/`row-gap`/`column-gap`), resolving against Box's spacing-token scale; like Stack, Grid owns it so children need no margins.
- **the grid items / cells** — the children placed into the tracks; each can **span** (`grid-column: span 2`) or be explicitly **placed** (`grid-column: 1 / 3`, `grid-area: header`). Often a `Grid.Item`/`Cell` with `colSpan`/`rowSpan`/`gridArea` props.
- **the template areas** — `grid-template-areas` ASCII-art naming regions (`"header header" "sidebar main"`) for explicit, readable 2D placement.
- **subgrid** — a nested grid using `grid-template-columns: subgrid` to align its items to the *parent* grid's tracks (the card-content-aligning-across-cards case — §11).
- **the (absence of) visual chrome** — no background/border/elevation (that's Card); pure layout.

## 3. Properties / API
- **`columns` / `templateColumns`** — the column tracks: a count (`columns={3}` → `repeat(3, 1fr)`), a template string (`"200px 1fr"`), or the auto-grid (`minChildWidth` → `repeat(auto-fit, minmax(<min>, 1fr))`); **responsive** (`columns={{ base: 1, md: 3 }}`). The headline prop.
- **`rows` / `templateRows`** — the row tracks (often implicit/`auto`; explicit for the named-areas/template case).
- **`gap` / `rowGap` / `columnGap`** — the inter-track space, a token-scale index (resolving against Box's scale). Grid `gap` is where `gap` *started* (§13).
- **`areas` / `templateAreas`** — the named-areas template (the app-shell genre).
- **`autoFlow`** — `row`/`column`/`dense` — how auto-placed items flow (and `dense` backfilling — with a reading-order caveat, §6).
- **the alignment matrix (the four-way axis Grid has that Stack doesn't):** `justifyItems`/`alignItems` (each *cell's* content within its track — inline/block) and `justifyContent`/`alignContent` (the *tracks* within the container when they don't fill it). Stack has one cross-axis `align` + one main-axis `justify`; Grid has both, per axis.
- **the item API** — `Grid.Item`/`Cell` with `colSpan`/`rowSpan` (span N tracks), `gridColumn`/`gridRow` (explicit lines), `gridArea` (a named area). The per-item placement surface.
- **`as` / `asChild`** — inherited from Box (the polymorphic Slot): render the right element (`ul`/`section`/`main`) for semantics (§6).
- **responsive vs intrinsic vs container-query (the load-bearing API choice)** — three ways to be responsive: *viewport-breakpoint props* (`columns={{base, md}}` — re-derives media queries), *intrinsic* (`auto-fit`/`minmax` — no breakpoints at all), or *container queries* (`@container` — responds to the container). The practice **prefers intrinsic/container-query over breakpoint props** where the layout allows (§11).
- **what it withholds** — no margin (the parent's gap), no visual chrome (Card).

## 4. States and variants
- **States: none.** Grid is layout-only — no hover/focus/active/disabled (inherits Box's statelessness). An interactive element rendered via `as`/`asChild` carries the states.
- **Variants (genres + mechanisms, not visual variants):**
  - **genre:** column-grid (page-level N columns) / auto-grid (the RAM `auto-fit`/`minmax` pattern) / named-areas (the app-shell template).
  - **track sizing:** fixed-column (explicit count/template) vs **intrinsic** (`auto-fit`/`minmax`, content-driven).
  - **responsive mechanism:** viewport-breakpoint props / intrinsic / container queries.
  - **with subgrid** (nested track alignment) vs independent nested grids.
  - **rendered element:** the `as` target (`div`/`ul`/`section`/`main`).

## 5. Usage guidance
- **Use a Grid for genuine two-dimensional alignment:** a gallery of cards aligning to both row and column rhythm; an app shell (header/sidebar/main/footer); a form whose labels and fields align in columns across rows; a dashboard of tiles; any layout where items must line up in *both* axes regardless of content size.
- **Stack-first (the load-bearing rule):** **reach for Stack before Grid.** Most layouts are one-dimensional — a column of sections, a row of buttons — and a Stack (or a wrapping Stack) is simpler and more robust. Use Grid *only* when you need two-dimensional alignment that a Stack can't give. A Grid forced to do 1D work (a single column, or a row that should just wrap) is over-engineering. (See stack for the 1D case.)
- **Genre selection:**
  - equal, self-reflowing cells (a card gallery) → the **auto-grid** (`auto-fit`/`minmax`) — no breakpoints needed.
  - a fixed page-level column count that changes at breakpoints → the **column grid** (`columns={{base, md}}`) or container queries.
  - a fixed named structure (app shell) → **named areas**.
- **The intrinsic-over-breakpoint preference:** prefer `auto-fit`/`minmax` (and container queries) over hand-authored viewport-breakpoint columns where the content allows — the grid then responds to *available space*, not a guessed viewport, and survives being placed in a narrow sidebar (which viewport breakpoints don't).
- **Don't scatter source order** — never use `grid-area`/`grid-column`/`order` to place items visually away from their DOM order for *meaningful* content (§6); arrange the DOM, then let the grid place in source order.
- **Don't add chrome to a Grid** — background/border/elevation means a **Card** (not yet briefed).

## 6. Accessibility
Grid inherits Box's a11y story — **a presentational `div` (no role, no name), so the accessibility surface is the element it renders via `as`/`asChild`** (see box). Two Grid-specific points:

- **The `role="grid"` naming collision (flag it loudly).** CSS **`display: grid` is purely presentational** and has **nothing to do with ARIA `role="grid"`** — which is the *interactive data-grid* pattern (a tabular widget with arrow-key cell navigation, the pattern Tag's removable-token group borrows and Table will use). A layout Grid must **never** carry `role="grid"`; doing so promises a keyboard interaction model that isn't there. (CSS `display: grid` ≠ ARIA `role=grid`.)
- **The DOM-order-vs-visual-order trap — sharper than Stack's.** Grid makes visual reordering *trivial*: `grid-template-areas`, explicit placement (`grid-column`/`grid-row`), `order`, and `grid-auto-flow: dense` can all put any item anywhere on screen regardless of its DOM position. But screen readers and the Tab key follow the **DOM**, so a grid that scatters items visually away from source order produces a reading/focus order that mismatches the visual order — a **WCAG 1.3.2 (Meaningful Sequence)** + **2.4.3 (Focus Order)** failure, and *easier to commit* in Grid than in Stack because explicit placement invites it. **The rule (the no-reorder discipline, applied harder):** arrange the **DOM in the intended reading order** and let the grid place items in source order; reserve explicit-placement-away-from-source for purely-presentational, no-meaning arrangements. `grid-auto-flow: dense` specifically can reorder items to backfill gaps — use it only where order is meaningless.
- **Semantic `as`** — a grid that is a *list* of items → `as="ul"` with `<li>` children; an app-shell grid → `as` the right landmarks (`main`/`aside`/`header`), or place real landmark elements as the grid items. Don't leave a meaningful structure a neutral `div` (1.3.1).
- **WCAG SCs:** **1.3.2** (meaningful sequence — the no-reorder rule, the sharp one), **2.4.3** (focus order), **1.3.1** (info & relationships — semantic `as`); plus the **don't-misuse-`role=grid`** caveat (4.1.2 — a false role is worse than none). The light a11y of a layout primitive, with the two real caveats.

## 7. Content guidelines
- Grid **holds layout, not content** — no copy of its own (like Box/Stack).
- **Don't scatter source order** — the content order in the DOM should be the intended reading order; don't rely on grid placement to "fix" a DOM authored in the wrong order (it fixes the eye, not the screen reader — §6).
- **Semantic markup for meaningful grids** — if the grid lays out a list, a set of regions, or an app shell, encode it (`as="ul"`/`<li>`, landmark elements), don't leave it visual-only.

## 8. Motion and transition
- Grid ships **no motion of its own** (like Box/Stack) — track calculation and placement execute at layout/paint.
- **Item add/remove/reflow** — when items enter/leave/reorder, the grid reflows; a **FLIP** animation smooths it (the same technique Stack and Tag use — see stack, tag), applied by the consumer or an animation primitive via `asChild`, not by Grid.
- **The grid-template animation caveat** — animating `grid-template-columns`/`rows` (e.g., a sidebar collapsing a track to `0`) is now animatable in modern engines but historically wasn't; prefer `transform` where possible, and gate any track animation behind reduce-motion.
- **Reduce-motion** — the consumer's concern on any reflow/track animation; Grid is motion-neutral.

## 9. Internationalization
- **Grid flows inline-start → inline-end**, so a column grid mirrors under RTL automatically: with `dir="rtl"` the first column sits on the right and columns flow left, and the `gap` (logical) applies along the flow — **no JS**.
- **Logical placement over physical** — explicit placement and named areas should use logical line names / the natural flow, not hardcoded physical positions; Box's logical-property mapping (inherited) handles directional offsets. A grid that hardcodes `grid-column: 1` for "leftmost" is RTL-correct (column 1 is inline-start = right in RTL); one that positions by physical pixel offset is not.
- **Named areas mirror** — `grid-template-areas` follow the writing direction; an app-shell `"sidebar main"` puts the sidebar inline-start (right in RTL) automatically.
- Grid is otherwise i18n-neutral (no text of its own).

## 10. Naming
- **The field set:** **`Grid`** + **`GridItem`/`Grid.Cell`** (the explicit CSS-Grid component — Chakra, Radix Themes, Spectrum, Polaris); **`SimpleGrid`** (Chakra — the auto-grid/RAM convenience with `minChildWidth`/`columns`); **`Columns`/`Column`** + **`Tiles`** (Braid — the column system + the auto-grid); **`Row`/`Col`** (Bootstrap 12-column, Ant 24-column — the legacy fraction-of-N); **`InlineGrid`** (Polaris); **`PageLayout`** (Primer — the app-shell template as a named component).
- **The practice's default — `Grid` + `Grid.Item`** for the explicit CSS-Grid engine (columns/rows/areas/gap + per-item span/placement), plus a **`SimpleGrid`/auto-grid convenience** for the RAM pattern (the most common gallery case, where `minItemWidth` is friendlier than authoring `repeat(auto-fit, minmax(…))`). The page-level **column system** can be the same `Grid` with a `columns` count rather than a separate `Columns` component (one fewer concept), though a named `Columns` is a defensible intent-revealing alternative. The **app-shell** is a composed *pattern* (a Grid with named areas), not necessarily its own primitive — but a named `PageLayout` earns its place at the app level.
- **The `role=grid` naming collision** — name the *component* `Grid` (the CSS layout) but never emit `role="grid"` (the ARIA data-grid); the collision lives in the name, not the output (§6).
- **Aliases to map:** GridItem, Grid.Cell, SimpleGrid, Columns, Column, Row, Col, InlineGrid, Tiles, PageLayout, AppShell.

## 11. Implementation notes
- **CSS Grid over the reimplemented 12-column float system.** Build on native `grid-template-columns`/`-rows`/`-areas` + `fr`/`minmax`/`repeat`, not a float/flexbox `Row`/`Col` reimplementation. The 12-column span API (`<Col span={6}>`) can survive as a *familiar layer* mapping to `grid-column: span 6` over a 12-track grid, but the engine underneath is CSS Grid. **MUI's `Grid`→`Grid2` migration** (from a flexbox 12-column grid to a CSS-Grid implementation) is the worked cautionary tale of carrying a float-era API into the CSS-Grid era.
- **The auto-grid / RAM idiom** — `grid-template-columns: repeat(auto-fit, minmax(min(<min>, 100%), 1fr))` reflows the column count to fit the available width *with no media queries*; the `min(<min>, 100%)` guard prevents overflow when the container is narrower than `<min>`. Expose it as `minItemWidth`/`minChildWidth` so consumers don't hand-author the incantation. `auto-fit` (collapse empty tracks) vs `auto-fill` (keep them) is the one real knob.
- **The named-areas template** — `grid-template-areas` is the most readable 2D placement for fixed structures (app shells); the items reference areas by name (`gridArea="sidebar"`). Pair with responsive/container-query area redefinition (the sidebar stacks under main on narrow containers).
- **Subgrid** — `grid-template-columns: subgrid` lets a nested grid (e.g., a Card) align its internal tracks to the parent grid's columns, so content *across* sibling cards lines up (titles, metadata rows). Shipped broadly ~2023–2024; a real capability for card galleries, flagged for support-dating.
- **Container queries over viewport-breakpoint props (the inflection).** Prefer `@container` (the grid responds to its *container's* width) over `columns={{base, md}}` (viewport media queries) — a container-query grid survives being dropped into a narrow sidebar, where viewport breakpoints guess wrong. Container queries shipped ~2023 and were broadly supported by 2023–2024; the auto-fit/minmax RAM pattern is the intrinsic, query-less version of the same goal. *Date this — it's the volatile claim, like Box's zero-runtime.*
- **Grid `gap`'s head-start** — grid `gap` shipped ~**2018**, well before flex `gap` (Safari 14.1 / 2021 — see stack); Grid is where `gap` started, so Grid never needed the lobotomized-owl margin hacks Stack did.
- **The item-placement API** — `Grid.Item` mapping `colSpan`→`grid-column: span N`, `gridArea`→`grid-area`, with responsive span values. Keep placement on the item, track definition on the container.
- **The no-reorder enforcement** — a lint/review rule against `grid-area`/`grid-column`/`order`/`dense` placing meaningful content away from DOM order (§6).
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL all come from Box (see box); Grid adds only the 2D track + gap + areas + placement + alignment-matrix delta.
- **Headless vs opinionated** — a thin opinionated layer on CSS Grid + the token scale (no state, no a11y machinery beyond `as`); ship as a styled layout primitive — the value is the constrained, token-bound, intent-revealing API (and the `minItemWidth` convenience) over raw grid.

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, the logical-property RTL — all inherited; see box).
- **2D sibling of:** **Stack** (the 1D engine — Stack is one axis, Grid is rows × columns; reach for Stack first, Grid only for genuine 2D alignment; the two close the Box→Stack→Grid triad — see stack). Grid inherits Stack's **no-external-margin discipline** (it owns the gap).
- **Composed by / hosts:** **card galleries** (the auto-grid of Cards — Card not yet briefed), **PageLayout/AppShell** (the named-areas template), **forms** (label/field column alignment), and **data displays** (dashboards of tiles).
- **Boundary (the naming collision):** the **interactive ARIA data grid** (`role="grid"`) — a *Table*-family widget with cell navigation (the pattern Tag's removable-token group borrows; Table not yet briefed). A layout Grid is *not* that and must not claim its role (§6).
- **Alternative to:** a bare **Box** (`display="grid"` by hand — the smell the constrained-over-open principle warns about; see box), a **Stack** (for 1D — the simpler reach), and **grid utility classes** (Tailwind's `grid grid-cols-3 gap-4` — the no-component position).

(The second Layout engine — the 2D CSS-Grid component that closes the Box→Stack→Grid triad. It stands on Box (inheriting the Slot, the scale, the RTL), is the 2D sibling of Stack (reach for Stack first), and is composed by card galleries / PageLayout / forms. See box for the substrate, stack for the 1D sibling + the FLIP reflow it shares, card/section/table when briefed for the hosts + the role=grid data-grid boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The 12-column float/flexbox grid → native CSS Grid.** The responsive-grid-system era (Bootstrap `Row`/`Col`, the float then flexbox 12/24-column systems) gave way to native CSS Grid (`grid-template-columns`/`-areas`, `fr`, `repeat`/`minmax`) — explicit 2D placement without nesting `Row`s. **MUI's `Grid`→`Grid2`** rebuild captures the migration.
2. **Grid `gap` first (2018), then flex `gap` (2021).** `gap` shipped in CSS Grid years before flexbox got it (Safari 14.1) — Grid never needed the lobotomized-owl hacks Stack carried.
3. **The auto-fit/minmax RAM pattern → intrinsic responsiveness.** `repeat(auto-fit, minmax(…, 1fr))` let grids reflow their column count with *zero* media queries — the column count became a function of available space, not a guessed breakpoint.
4. **The container-query shift (~2023).** `@container` moved responsiveness from the viewport to the *container* — a component now responds to where it's placed, not the window size; the biggest layout-responsiveness change since CSS Grid itself, and the natural successor to viewport-breakpoint props.
5. **Subgrid (~2023–2024).** `subgrid` let nested grids align to their parent's tracks, solving the long-standing card-content-alignment problem.
6. **The DOM-order-vs-visual-order a11y settling.** As with Stack, the recognition that explicit placement breaks meaningful sequence (1.3.2) + focus order (2.4.3) hardened the no-reorder rule — sharper in Grid because placement-anywhere is trivial.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- CSS Grid spec — `grid-template-columns`/`-rows`/`-areas`, `repeat`/`minmax`/`auto-fit`/`auto-fill`, `fr`, `subgrid`, `gap`.
- Chakra UI — `Grid` + `GridItem`, `SimpleGrid` (`minChildWidth`/`columns` — the RAM pattern).
- MUI — `Grid` (the v5 flexbox 12-column → `Grid2` CSS-Grid migration; `size`/`offset`).
- Radix Themes — `Grid` (`columns`/`rows`/`areas`/`gap`/`flow`).
- Braid / Seek — `Columns`/`Column` + `Tiles` (the column system + the auto-grid).
- Shopify Polaris — `Grid` + `Grid.Cell`, `InlineGrid` (columns per breakpoint).
- GitHub Primer — `PageLayout` + grid utilities.
- Adobe Spectrum — `Grid` (areas, the explicit CSS-Grid mapping).
- IBM Carbon — `Grid`/`Column` (the CSS-Grid + flexbox 16-column grids).
- Ant Design — `Row`/`Col` (the 24-column grid).
- Bootstrap — `Row`/`Col` (the 12-column legacy reference).
- Tailwind — `grid` utilities (`grid-cols-N` — the no-component position).
- Base Web (Uber) — the responsive grid.
- WAI-ARIA / HTML — CSS `display: grid` is a presentational `div` (no role); the **`role="grid"` collision** with the interactive data-grid pattern; the DOM-order-vs-visual-order meaningful-sequence trap.
- WCAG 2.2 — 1.3.2, 2.4.3, 1.3.1, 4.1.2.
- CSS — grid `gap` (~2018); container queries `@container` (~2023); `subgrid` (~2023–2024).

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
    - "the grid container: display:grid establishing a grid formatting context; defines the tracks + gap; a semantically neutral div (inherits Box's neutrality)"
    - "the tracks (columns/rows): fixed (200px) / fractional (1fr) / content (auto/min-content) / generated (repeat(auto-fit, minmax(...,1fr))); the defining structure"
    - "the gap (gap/row-gap/column-gap): the space BETWEEN tracks, resolving against Box's spacing-token scale; Grid owns it (children need no margins)"
    - "the grid items/cells: children placed into tracks; each can span (grid-column: span 2) or be placed (grid-column:1/3, grid-area:header); often a Grid.Item/Cell with colSpan/rowSpan/gridArea"
    - "the template areas: grid-template-areas ASCII-art region naming for explicit readable 2D placement (the app shell)"
    - "subgrid: a nested grid (grid-template-columns:subgrid) aligning its items to the PARENT grid's tracks (card-content-alignment)"
    - "(absence of) visual chrome: no bg/border/elevation (that's Card); pure layout"
api:
  inherits:
    - box        # the as/asChild Slot, the spacing-token scale (gap resolves against it), the zero-runtime delivery, the logical-property RTL
  props:
    - {name: columns/templateColumns, type: "number | template | responsive | auto-grid(minItemWidth)", default: ~, required: false, description: "the column tracks: count (->repeat(N,1fr)) / template string / auto-grid (->repeat(auto-fit,minmax)); responsive (columns={{base:1,md:3}})"}
    - {name: rows/templateRows, type: "number | template", default: auto, required: false, description: "the row tracks (often implicit/auto; explicit for named-areas)"}
    - {name: gap/rowGap/columnGap, type: "token-scale", default: ~, required: false, description: "the inter-track space, a token index (resolving against Box's scale); Grid is where gap STARTED (~2018)"}
    - {name: areas/templateAreas, type: "template", default: ~, required: false, description: "named-areas template (the app-shell genre)"}
    - {name: autoFlow, type: "'row'|'column'|'dense'", default: row, required: false, description: "how auto-placed items flow; 'dense' backfills (with a reading-order caveat — a11y)"}
    - {name: "justifyItems/alignItems", type: enum, default: stretch, required: false, description: "each CELL's content within its track (inline/block) — the matrix Stack lacks"}
    - {name: "justifyContent/alignContent", type: enum, default: start, required: false, description: "the TRACKS within the container when they don't fill it"}
    - {name: "Grid.Item: colSpan/rowSpan/gridColumn/gridRow/gridArea", type: "number | line | area-name", default: ~, required: false, description: "the per-item placement/span surface; placement on the item, tracks on the container"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — render the right element (ul/section/main) for semantics"}
  responsive-mechanism: "VIEWPORT-breakpoint props (columns={{base,md}} — re-derives media queries) vs INTRINSIC (auto-fit/minmax — no breakpoints) vs CONTAINER QUERIES (@container — responds to the container). Practice PREFERS intrinsic/container-query over breakpoint props where the layout allows"
  withholds: "no margin (parent's gap), no chrome (Card)"
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
  role-grid-COLLISION: "CSS display:grid is PRESENTATIONAL and has NOTHING to do with ARIA role=grid (the interactive DATA-GRID pattern with arrow-key cell nav — Tag's removable-token group borrows it, Table uses it). A layout Grid must NEVER carry role=grid (a false role promises an interaction model that isn't there)"
  DOM-vs-visual-order-trap: "SHARPER than Stack's — grid-template-areas/grid-column/grid-row/order/auto-flow:dense make placing any item anywhere TRIVIAL; SR + Tab follow the DOM, so scattering items visually away from source order breaks reading/focus order (WCAG 1.3.2 + 2.4.3) and is EASIER to commit than in Stack"
  no-reorder-rule: "arrange the DOM in the intended READING order + let the grid place in source order; reserve explicit-placement-away-from-source for purely-presentational no-meaning arrangements; auto-flow:dense reorders to backfill — use only where order is meaningless"
  semantic-as: "a grid that's a LIST -> as='ul'/<li>; an app-shell grid -> the right landmarks (main/aside/header) or real landmark elements as items; don't leave a meaningful structure a neutral div (1.3.1)"
content:
  holds-layout-not-content: "no copy of its own (like Box/Stack)"
  no-scatter-source-order: "the DOM content order = the intended reading order; don't use grid placement to 'fix' a wrongly-ordered DOM (fixes the eye, not the SR)"
  semantic-markup: "a list/regions/app-shell grid -> encode it (as='ul'/li, landmarks), not visual-only"
motion:
  own: none   # track calc + placement execute at layout/paint
  reflow: "items add/remove/reorder -> grid reflows; FLIP smooths it (same as Stack/Tag), applied by the consumer/an animation primitive via asChild"
  grid-template-animation: "animating grid-template-columns/rows (a collapsing sidebar track to 0) is now animatable but historically wasn't; prefer transform; gate behind reduce-motion"
  reduce-motion: "the consumer's concern on any reflow/track animation; Grid is motion-neutral"
i18n:
  flows-inline-start-to-end: "a column grid mirrors under RTL automatically (dir=rtl: first column on the right, columns flow left; the logical gap applies along the flow) — no JS"
  logical-placement: "explicit placement + named areas use logical line names / the natural flow, not hardcoded physical positions; grid-column:1 is inline-start (right in RTL) = correct; a physical-pixel-offset placement is not (Box's logical-property mapping handles offsets)"
  named-areas-mirror: "grid-template-areas follow the writing direction (an app-shell 'sidebar main' puts the sidebar inline-start = right in RTL automatically)"
  otherwise: "i18n-neutral (no text of its own)"
implementation:
  - "CSS Grid over the reimplemented 12-column FLOAT system: build on native grid-template-columns/-rows/-areas + fr/minmax/repeat, not a float/flexbox Row/Col reimplementation. A 12-column span API (Col span=6 -> grid-column:span 6) can survive as a FAMILIAR LAYER over a CSS-Grid engine. MUI's Grid->Grid2 (flexbox 12-col -> CSS Grid) is the worked migration"
  - "the auto-grid/RAM idiom: grid-template-columns: repeat(auto-fit, minmax(min(<min>,100%),1fr)) reflows column count to fit WITH NO media queries; the min(,100%) guard prevents overflow when narrower than <min>; expose as minItemWidth/minChildWidth. auto-fit (collapse empty tracks) vs auto-fill (keep them) is the one knob"
  - "the named-areas template: grid-template-areas = the most readable 2D placement for fixed structures (app shells); items reference areas by name (gridArea='sidebar'); pair with responsive/container-query area redefinition"
  - "subgrid (grid-template-columns:subgrid): a nested grid aligns its tracks to the parent's columns so content ACROSS sibling cards lines up; ~2023-2024 support (flag dating)"
  - "container queries over viewport-breakpoint props (the inflection): prefer @container (responds to the CONTAINER's width) over columns={{base,md}} (viewport media queries) — survives being dropped into a narrow sidebar; ~2023 ship, broadly supported 2023-24; auto-fit/minmax is the intrinsic query-less version. DATE IT (volatile, like Box's zero-runtime)"
  - "grid gap's head-start: grid gap shipped ~2018, before flex gap (Safari 14.1/2021) — Grid never needed the lobotomized-owl hacks Stack did"
  - "the item-placement API: Grid.Item maps colSpan->grid-column:span N, gridArea->grid-area, with responsive spans; placement on the item, track definition on the container"
  - "no-reorder enforcement: a lint/review rule against grid-area/grid-column/order/dense placing meaningful content away from DOM order"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Grid adds only the 2D track + gap + areas + placement + alignment-matrix delta"
  - "headless vs opinionated: a thin opinionated layer on CSS Grid + the token scale (no state, no a11y beyond as); ship as a styled layout primitive — the value is the constrained token-bound intent-revealing API + the minItemWidth convenience over raw grid"
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
    - "the 12-column legacy API (Row/Col span-of-N — Bootstrap/Ant/MUI-v5) vs native CSS Grid (template-columns/fr/areas — practice default); a span API can survive as a familiar layer over CSS Grid"
    - "one Grid serving all three genres (columns count / auto-grid / named-areas) vs a column-system split (Columns/Column) + a SimpleGrid + a PageLayout"
    - "responsive mechanism: viewport-breakpoint props vs intrinsic (auto-fit/minmax) vs container queries (practice: prefer intrinsic/container-query)"
    - "N for the column system (12 Bootstrap/MUI, 24 Ant, 16 Carbon) — or skip a fixed N for fr/auto-fit"
  trap:
    - "carrying role=grid onto a layout Grid (it's the INTERACTIVE data-grid ARIA pattern — CSS display:grid != ARIA role=grid)"
    - "the DOM-order-vs-visual-order trap, SHARPER than Stack's: areas/grid-column/grid-row/order/dense scattering meaningful content away from source order (WCAG 1.3.2 + 2.4.3) — arrange the DOM, place in source order"
    - "putting margin on grid children to adjust spacing (use gap — the no-external-margin principle)"
    - "adding chrome (bg/border/elevation) to a Grid (that's a Card)"
    - "using Grid for 1D work (a single column / a row that should just wrap) -> Stack; a bare Box display=grid by hand (the constrained-over-open smell)"
    - "auto-fit/minmax without the min(,100%) guard (overflow when the container is narrower than the min)"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL, the presentational-div a11y; Stack's no-external-margin discipline"
  role-in-family: "the second Layout engine — the 2D CSS-Grid component that closes the Box->Stack->Grid triad; stands on Box, the 2D sibling of Stack (reach for Stack first), composed by card galleries/PageLayout/forms"
  evolution:
    - "the 12-column float/flexbox grid -> native CSS Grid (template-columns/fr/areas); MUI Grid->Grid2"
    - "grid gap first (~2018) then flex gap (Safari 14.1/2021)"
    - "the auto-fit/minmax RAM pattern -> intrinsic responsiveness without media queries"
    - "the container-query shift (~2023) -> component-responds-to-container (the natural successor to viewport-breakpoint props)"
    - "subgrid (~2023-2024) -> nested-grid track alignment"
    - "the DOM-order-vs-visual-order a11y settling (the no-reorder rule, sharper in Grid)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "container-query (@container) + subgrid support dates (~2023 / ~2023-2024) — verify against current baseline"
    - "the MUI Grid->Grid2 migration state; per-system column-count N + genre coverage"
```

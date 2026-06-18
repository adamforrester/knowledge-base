---
okf_version: "0.1"
type: component-brief
title: Table
description: The keystone of the Data category and the catalogue's biggest convergence point — a field-truth study of the data-table-vs-data-grid genre split + the native-<table>/role=grid/div-soup decision (the entire a11y model hinges on it; the virtualization-forces-complete-ARIA-grid exception), the column-model + headless-vs-batteries-included architecture (TanStack's headless turn), sorting (aria-sort + the header button) + selection (the checkbox column + the select-all indeterminate-via-ref), sticky headers/frozen columns + virtualization (the aria-rowcount/rowindex semantics tension + the variable-height cost), the responsive-table problem (scroll/stack/hide — no clean winner), and the composition convergence (Checkbox/Pagination/Empty-State/Skeleton/Menu/Tag/Badge/Avatar) — where Grid's role=grid boundary lands, with the practice's defaults.
tags: [components, data]
category: Data
status: stable
aliases: [DataTable, DataGrid, Grid (data-grid sense), IndexTable, TableView, DynamicTable]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Table

> A Table presents **tabular data** — information with genuine row × column relationships, where a cell's meaning depends on *both* its column header and its row. It is the **keystone of the Data category** (the first Data brief), the catalogue's **biggest convergence point**, and the hardest component in the set: the structural chassis where Checkbox (selection), Pagination (paging), Empty State + Skeleton (the no-data/loading states), Menu (row actions), and Tag/Badge/Avatar/Button/Link/Tooltip (cell content) all integrate — the brief where the whole catalogue pays off. It is where **Grid's `role=grid` boundary lands**: CSS `display: grid` is *presentational* and is *not* the interactive ARIA data-grid pattern; `role=grid` (and `role=treegrid`) live here (see grid). The headline that decides the entire technical, interactive, and a11y model is the **data-table vs data-grid genre split**, and the **native-`<table>` / `role=grid` / div-soup** decision that follows. What it *isn't*: a **CSS Grid layout** (`role=grid` ≠ `display: grid`), a **List** (1D records, no column relationships — not yet briefed), or a **layout table** (the dead anti-pattern — a layout table lies to assistive tech). Why systems disagree: the genre split, the headless-vs-batteries-included architecture, and the responsive-table problem (no clean winner).

---

## 1. Framing
A Table is the structural chassis of the Data category, and the practice must first establish the **genre split** that dictates everything downstream:
- **The data table (static)** — for *scanning, reading, comparing*. Displays tabular data, supports pagination, often sortable/filterable, may contain links/buttons/toggles *in cells*, but is **not navigable as a single keyboard widget** — the user Tabs linearly through focusable children. Relies on **native `<table>` semantics**. *Reading* mode. **The vast majority of "tables" are this**, and the practice default.
- **The interactive data grid** — an *application-mode widget* mimicking a spreadsheet: omnidirectional **arrow-key cell navigation**, editable cells, draggable column resize/reorder, complex keyboard selection. The **entire grid is one tab stop**; once focus enters, navigation is intercepted in JS. Requires the WAI-ARIA **`role="grid"`/`treegrid"`** pattern with complex focus management. *Application* mode.

The **`<table>` / `role=grid` / div-soup decision** that follows:
- **Native `<table>`** (`<caption>`/`<thead>`/`<th scope>`/`<tbody>`/`<td>`) — the default for tabular data; the structure conveys relationships to AT for free.
- **`role=grid`** — *only* for the genuine interactive widget. The recurring trap is **architectural over-reach** — slapping grid roles on a data table, creating barriers for screen-reader users who expect document-reading behavior.
- **Div-soup** (`role=table/row/cell` on `<div>`s) — recreating table semantics when native `<table>` can't be used. **Partial div-soup is a catastrophe**; the *one legitimate case* is heavy virtualization, which can *force* the complete-ARIA-grid route off native `<table>` (§6).

The other axis is the **deployment architecture**: **headless** (TanStack Table — the sort/filter/paginate/select *logic* separated from the markup, the DS owns the DOM) vs **batteries-included** (MUI X DataGrid, AG Grid — opinionated DOM + enterprise features out of the box, at the cost of bundle size and brand-alignment friction). The practice ships a **headless engine + an opinionated a11y-correct skin**. What it *isn't*: a CSS Grid layout (the naming collision Grid named — see grid), a **List** (1D — not yet briefed), a **layout table** (dead).

## 2. Anatomy and parts
The outermost layer is the **table container** (managing horizontal overflow, border-radius, the scroll context). Within it:
- **`<caption>`** — the table's **accessible name** (visible or visually-hidden); the first child of `<table>`.
- **the toolbar** — above the table: global search, density toggle, column-visibility menu, and the **bulk-action bar** that surfaces on selection.
- **`<thead>` + the header row** — `<th scope="col">` cells; a **sortable header** composes a `<button>` inside the `<th>` (with the sort indicator + `aria-sort`); the first header often composes the **select-all Checkbox**. May be **sticky**.
- **`<tbody>` + the data rows** — `<tr>` records of `<td>` cells; a row may compose an expand trigger (hierarchical), a selection **Checkbox** cell, and a trailing row-actions **Menu**; a `<th scope="row">` row-header (often a frozen first column).
- **`<td>` (the cell)** — the atomic canvas: the injection point for **Tag / Badge / Avatar / Button / Link**, or truncated text + a **Tooltip**.
- **`<tfoot>` / footer** — aggregation rows (totals/averages) and/or the **Pagination** controls.
- **sticky / frozen regions** — via `position: sticky`, with a box-shadow/pseudo-element **elevation shadow** signalling the z-layer (§11).
- **terminal-state regions** — overlays/replacements in the `<tbody>` area per the data lifecycle: **Skeleton** rows (loading), **Empty State** (zero results), the error boundary (§4; see empty-state, skeleton).
- **the data model (not visual):** the **column definitions** + the **row data** — the headless heart (§3).

## 3. Properties / API
The foundation is the **"columns-as-config" + "rows-as-data"** model: developers pass typed configuration objects, *not* raw JSX children (passing JSX makes sorting/filtering impossible without parsing the DOM).

**The column model (the central nervous system):** each column definition carries:
- **`accessor`/`key`** — the data field (a string or function).
- **`header`** — the `<th>` content.
- **`cell` (the renderer)** — a render function returning the `<td>` UI; **the exact injection point where Tag/Badge/Avatar/Button/Menu compose** (§12).
- **`sortable` / `filterable`** — per-column logic flags.
- **`width` / `align`** — layout (numeric → end / right-aligned); `minWidth`, fixed vs dynamic.
- **`pin` / `sticky`** — freeze to the inline-start/end edge.
- **`enableHiding`** — for column-priority responsive (§5).

**Other core props:** `data`/`rows`; `sortBy` (single/multi) + `onSortChange`; the selection model (`selectionMode` none/single/multiple + `selectedKeys` + `onSelectionChange`); pagination (`page`/`pageSize`/`onPageChange`); `density`; sticky/pin; virtualization.

**Server-vs-client data (the load-bearing architecture choice):** *client-side* ingests the full dataset and sorts/filters/paginates in browser memory — instant, but scales poorly past a few thousand rows; *server-side* makes the table a presentation layer emitting `onSortChange`/`onPaginationChange` callbacks while the host refetches windowed slices. The API must transition between them **without changing the visual implementation** (the headless engine's `manualSorting`/`manualPagination` flags: the engine manages state, delegates the work).

**Headless vs batteries-included:** **headless** (TanStack Table — outputs raw state + functions like `row.getVisibleCells()`, the DS wires them to the semantic DOM; **v9's modular `TFeatures` generic** cut TypeScript instantiation from ~1.1M to ~158K — an ~86% type-check speedup, fixing the monolithic-type overhead) vs **batteries-included** (MUI X DataGrid, AG Grid — massive prop surfaces, Excel export / cell editors / charting, but heavier bundles >100KB gzipped and CSS you fight for brand alignment). The practice: a headless engine + an opinionated skin.

## 4. States and variants
- **The macro terminal-states machine** (the data lifecycle): **loading** (Skeleton rows matching the anticipated row height/column widths to prevent CLS — see skeleton) → **content** (populated) → **empty** (an **Empty State** replacing `<tbody>`, *differentiating inherently-empty from filtered-to-zero* — see empty-state) → **error** (a network/logic failure with a localized retry). The data-container terminal-states machine Empty State described.
- **Micro states:** **column** (unsorted / ascending / descending — `aria-sort`; resizable; hidden); **row** (hover / focus [grid mode] / **selected** [primary-tint background + `aria-selected`] / **expanded** [detail row / treegrid] / disabled); **selection** (none / **some [select-all indeterminate]** / all); **header** (the sort-indicator flip).
- **The AI-presence state (an emerging 2026 finding)** — IBM Carbon styles **AI-generated rows/cells** with specific linear gradients + inner shadows to *disclose* the AI's intervention to the user (trust/transparency). A novel state worth tracking as AI-populated tables proliferate.
- **Variants:** **genre** (data table `<table>` / interactive data grid `role=grid` / treegrid); **density** (**comfortable** ~16px padding / 48–56px rows; **compact/condensed** ~4–8px padding / ~32px rows for analytical density); **selection** (none/single/multiple); **layout** (scroll / sticky-header / frozen-column / virtualized); **responsive** (scroll / stacked-card / column-priority).

## 5. Usage guidance
- **Use a Table for genuine two-dimensional data** — records the user cross-references *across columns* and *down rows*. The test: does a cell's meaning depend on *both* its column and its row? Yes → Table.
- **Table vs the alternatives (by data dimensionality):**
  - **vs a List** — *1D* records (a directory of names, no comparative attributes) → a **List** (not yet briefed); don't build a single-column table.
  - **vs a Grid / Card gallery** — heterogeneous, heavily visual (product thumbnails, varying metadata), browse-mode → a **Grid of Cards** (see grid, card); homogeneous, dense, comparable → a Table.
  - **vs a description list (`<dl>`)** — single-entity key-value pairs (a detail panel) → a `<dl>`, not a one-row table.
- **The data-table-vs-data-grid decision (the most critical call):** **default to the data table** for the vast majority of cases (reading, selecting, navigating to a detail view). **Escalate to an interactive data grid only** when building a focus-managed application where users edit data inline as rapidly as a native spreadsheet — its keyboard model is a real cost.
- **When to virtualize** — only for *large* (thousands of rows) unpaginated datasets; it adds a11y complexity (§6), so don't default it for a 50-row table (pagination/plain rendering is simpler and more robust).
- **Never use a table for layout** — it breaks the logical reading order for screen readers and violates web standards; layout is Box/Stack/Grid (see box, stack, grid).
- **The responsive approach is a deliberate choice** (§ responsive) — pick scroll / stack / hide per the data and the a11y cost.

## 6. Accessibility
The a11y model **hinges entirely on the genre** (§1) — the most technically demanding terrain in the catalogue.

- **The native `<table>` contract (the default, and the most robust).** `<caption>` is the accessible name (announced before navigation); `<th scope="col">`/`<th scope="row">` let the browser natively associate header cells with their column/row, so a screen reader announces "Status, Active" (header + cell). In reading mode the user navigates with the screen reader's table cursor, cell by cell. These relationships are *free* with a real `<table>` and near-impossible to fully replicate in ARIA — *the* reason to use one.
- **Sorting — `aria-sort` + the header button.** A sortable header wraps its label in a **`<button>`** (focusable, Enter/Space); the `<th>` carries **`aria-sort="ascending|descending|none"`** (only the *currently-sorted* column gets a direction). On sort, a polite **`aria-live`** region announces the new order/pagination ("Sorted by Name, ascending") without stealing focus.
- **The interactive data grid (`role=grid`/`treegrid`).** Native table semantics are *overridden* by application semantics: `role="grid"` (or `treegrid`) + `role="row"` + `role="gridcell"`/`columnheader`/`rowheader`; the grid is **one tab stop**; arrow-key navigation is JS-managed via one of two focus strategies — **roving tabindex** (the focused cell `tabindex="0"`, others `-1`, JS moves it + calls `.focus()`; **preferred when cells contain interactive children** like inputs/checkboxes/buttons) or **`aria-activedescendant`** (DOM focus stays on the grid container; the attribute points at the active cell's id; **for virtualized/readonly grids** where moving real focus is expensive). `treegrid` adds `aria-expanded`/`aria-level` (the Tree sibling). This is the APG Grid pattern — a *lot*; don't take it on unless the interaction demands it.
- **Selection — `aria-selected` + the select-all indeterminate.** Selected rows carry `aria-selected` (grid) or the checkbox state; the header select-all **Checkbox** shows the **indeterminate** state for some-but-not-all (a *DOM property, not an attribute* — set via ref; the Checkbox brief — see checkbox), named "Select all".
- **The semantic cost of virtualization (the sharp trap, and the div-soup exception).** Windowing removes off-screen DOM nodes, so AT (which only sees rendered nodes) would announce "Table, 15 rows" for a 10,000-row dataset. The fix: declare **`aria-rowcount`** (true total) + **`aria-rowindex`** per rendered row (its absolute position) + `aria-colcount`/`aria-colindex`. **But** applying these ARIA attributes to native `<table>` elements can trigger **HTML validation violations and unpredictable screen-reader behavior** — so heavily-virtualized grids are frequently *forced to abandon native `<table>`* for `<div>`s with the **complete** ARIA grid spec. This is the *one legitimate* non-`<table>` route — and it must be the **full** role set, never partial div-soup.
- **The responsive stacked-view semantics loss** — turning rows into stacked cards (`display: block`) **breaks the native table associations** (the roles flatten); either re-apply the ARIA table roles or treat/label it as a *list of records*. The horizontal-scroll approach **keeps the semantics** — its key a11y advantage.
- **WCAG SCs:** **1.3.1** (info & relationships — the structure), **2.1.1** (keyboard — sort/select/grid-nav), **4.1.2** (name/role/value — `aria-sort`/`aria-selected`/the grid roles), **1.4.10** (reflow — the responsive approach at 320px), **2.4.7** (focus visible — the cell/row focus), **4.1.3** (status messages — the sort/selection announcements).

## 7. Content guidelines
- **Column headers** — exceptionally concise (they're the sort/filter target; long headers make awkward touch targets, force wrapping, clutter scanning); a noun or short phrase; consistent capitalization.
- **Alignment + `tabular-nums`** — alphabetic text left (right in RTL); **numeric/financial/percentage/date data right-aligned (inline-end)** with **`font-variant-numeric: tabular-nums`** so digits occupy equal width and decimals align for vertical scanning (the digit-alignment discipline Pagination used — see pagination).
- **Units & formatting** — format via `Intl` (§9); put the unit in the *header* ("Size (MB)") not every cell.
- **Truncation + Tooltip** — the preferred default is single-line truncation (`text-overflow: ellipsis; white-space: nowrap`) + a **Tooltip** revealing the full text on hover/focus (see tooltip); multi-line wrapping kills vertical density, disrupts zebra-striping, and complicates row virtualization.
- **The empty-state copy** — explain *why* it's empty ("No transactions found for the selected date range") and give a recovery path ("Clear all filters") — the Empty State first-use-vs-no-results distinction (see empty-state); never an unexplained empty body.
- **Don't overload columns** — 20 columns is unreadable; use column-priority/hiding, a detail row, or a different view.

## 8. Motion and transition
- **Conservative by default** — the sheer DOM-node volume makes motion a 60fps risk. **Don't use FLIP on large-table sort reorders** — it causes layout thrashing and painting bottlenecks; row reordering should be **instantaneous** on large datasets (a FLIP can smooth a *small* table — the technique Stack/Grid/Tag share — see stack — but not at scale).
- **The native-CSS-transitions trend** — leading systems (React Aria, HeroUI) strip heavy JS animation runtimes (Framer Motion) for **native CSS transitions** on row expand/hover, reducing main-thread blocking + leveraging GPU acceleration.
- **The loading→content swap** — a seamless **cross-fade** from Skeleton to content, *given strict geometric parity* between skeleton and data rows (no CLS — see skeleton).
- **Row expand/collapse** (treegrid/detail) — a height transition (the Accordion discipline — see accordion).
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops sort/reflow/expand to instant; the data is the information, not the motion.

## 9. Internationalization
- **RTL — the column order mirrors automatically** under `dir="rtl"` (native with `<table>` markup, or via logical properties — `margin-inline-start` not `margin-left` — inherited from Box; see box): the first column on the right, sort indicators + the frozen row-header column flip to the inline-start. Numeric columns align to the logical start edge.
- **Number / date / currency formatting** — via **`Intl.NumberFormat`/`DateTimeFormat`** for locale digits, grouping, decimal separators, and date order (no hardcoded string manipulation).
- **Header + caption translation** — column headers/caption localize; translations run **30–50% longer** (German/Russian), so the column-sizing algorithm (`minmax()` / TanStack's grow-collapse sizing) must adapt to expansion without forcing isolated-column horizontal scroll or breaking the UI — variable header/row height.

## 10. Naming
- **The field set (a schism reflecting the genre split):** **`Table`** (the basic presentational `<table>` — Chakra, Base Web, Ant); **`DataTable`** (a table *with* built-in sort/pagination but still reading-mode — Primer, Carbon); **`DataGrid`/`Grid`** (the interactive focus-managed widget — MUI X, AG Grid); **`IndexTable`** (Polaris — viewing/selecting a homogeneous collection, e.g. Orders, distinct from a generic display); **`TableView`** (React Aria/Spectrum); **`DynamicTable`** (Atlassian).
- **The practice's default — name by the genre split:** **`Table`** (or `DataTable`) for the native, reading-mode display table (sortable/selectable/paginated — the common case, the default reach), and a separate, heavier **`DataGrid`** *exclusively* for the interactive `role=grid` focus-managed widget. Naming them apart *is* the genre split made legible — it stops teams from reaching for the grid's weight when a `<table>` would serve. Build both on a shared **headless engine** with different skins + a11y models.
- **Aliases to map:** DataTable, DataGrid, Grid (the data-grid sense — distinct from the layout Grid), IndexTable, TableView, DynamicTable.

## 11. Implementation notes
- **Build on a real `<table>` (the a11y foundation).** `<table>`/`<caption>`/`<thead>`/`<th scope>`/`<tbody>`/`<td>` give the relationships for free. The CSS friction: `display: grid`/`flex`/`block` on table elements **removes the table semantics** (the classic trap — `display: block` for sticky/scroll silently strips the roles). Prefer `position: sticky` on `<th>` + a scroll container over `display`-hacking; if you must restyle, re-apply `role="table/row/cell"`.
- **The sticky-header sub-pixel gap bug** — `position: sticky` on `<thead>` works, but table border sub-pixel rendering causes a **transparent ~1px gap** between the sticky header and the scrolling rows, through which data text "bleeds". Fix: a **solid background on `<th>`** + a pseudo-element/box-shadow covering the gap (which also serves as the sticky elevation shadow).
- **The headless engine** — separate the *logic* (column model + sort/filter/paginate/select/group/expand state — TanStack Table) from the *markup* (the DS's a11y-correct `<table>`); the same engine drives the display table and the data grid; `manual*` flags for server-side data.
- **Virtualization** (TanStack Virtual / react-window) — `aria-rowcount`/`aria-rowindex` for the true position (§6); **fixed-height rows = O(1)** random access, **variable-height rows = O(log n)** (prefix-sum arrays) — and rapid scroll mounts/unmounts components fast, so **`React.memo` row/cell renderers** to keep GC sweeps off the main thread. (And the div-soup-forcing tension — §6.)
- **The select-all indeterminate wiring** — `indeterminate` is a **DOM property, not an HTML attribute**; set it imperatively via a ref (`input.indeterminate = true`) — the Table exposes the Checkbox ref to govern it (the Checkbox brief — see checkbox): checked = all, indeterminate = some, unchecked = none.
- **The sortable-header button + `aria-sort`** — the header label is a `<button>`; the `<th>` gets `aria-sort`; a polite live region announces the new sort.
- **The responsive transform (no clean winner):** **scroll** (`overflow-x: auto` wrapper — preserves the `<table>` + ARIA semantics, the safest, the opinionated enterprise default); **stack** (media-query `tr/td { display: block }` → each row a card, `<th>` labels injected via `::before { content: attr(data-label) }` — looks great on mobile but **destroys the table semantics** for AT); **hide** (column-priority — progressively hide low-priority columns — preserves semantics but risks hiding vital data). **Horizontal scroll is the most robust, accessible default.**
- **Cell renderers compose the cluster** — the `cell` render fn returns Tag/Badge/Avatar/Button/Link/Menu (see those briefs); the Table provides the cell, the renderer fills it — the convergence in code.
- **The DataGrid-as-a-product reality** — the full interactive grid (MUI X DataGrid, AG Grid) is a *heavyweight, often commercially-licensed product* (MUI X Pro/Premium, AG Grid Enterprise; >100KB gzipped); many teams should compose a headless engine + a `<table>` instead.
- **Headless vs opinionated** — ship the headless engine (logic) + an opinionated a11y-correct default skin (the `<table>` markup + styling); the engine is the reusable value, the skin is the DS's contract.

## 12. Related and alternative components
- **The `role=grid` boundary from Grid** — Table is where the interactive ARIA data-grid pattern lives; CSS `display: grid` is the *layout* Grid and is presentational (the naming collision Grid named — see grid).
- **Composes (the convergence — the brief where the catalogue pays off):** **Checkbox** (selection + the select-all indeterminate — see checkbox), **Pagination** (paging — see pagination), **Empty State** (the no-data zero-state — see empty-state) + **Skeleton** (the loading rows — see skeleton) (the terminal-states machine), **Menu** (row actions — see menu), and cell content — **Tag** / **Badge** / **Avatar** / **Button** / **Link** / **Tooltip** (see tag, badge, avatar, button, link, tooltip).
- **Borders (siblings):** **List** (the 1D simpler sibling — records without column relationships — not yet briefed), **Tree** (the hierarchical sibling; `role=treegrid` = table + tree, with parent-child keyboard nav — not yet briefed).
- **Responsive boundary:** the stacked-card view turns each row into a **Card** (see card) — the responsive transform (with the semantics caveat — §6).
- **Alternative to:** a **List** (1D records), a **Grid of Cards** (heterogeneous/visual/browse), a **description list `<dl>`** (single-entity key-value).

(The keystone of the Data category — the tabular-data display + the interactive data grid, the catalogue's biggest convergence point. It is where Grid's `role=grid` boundary lands, and it composes Checkbox/Pagination/Empty-State/Skeleton/Menu/Tag/Badge/Avatar/Button/Link/Tooltip. See grid for the role=grid boundary, checkbox/pagination/empty-state/skeleton/menu for the composed machinery, tag/badge/avatar/button for the cell content, card for the responsive row→card, list/tree when briefed for the siblings. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The layout-table anti-pattern → tables-for-data-only.** The web spent a decade unwinding `<table>`-for-layout; tables now convey *data relationships* to AT, and layout is Box/Stack/Grid.
2. **The batteries-included heavy grid (AG Grid, early MUI DataGrid).** The first answer to SPA-scale performance — aggressive internal virtualization + state management — at the cost of massive bundles, rigid APIs, and visual inflexibility.
3. **The headless turn (TanStack Table).** Separating the sort/filter/select *state machines* from the markup let design systems keep pristine control over a11y/CSS/DOM while reusing the algorithms — the dominant modern architecture (and v9's `TFeatures` cut the TypeScript cost).
4. **The `<table>`-vs-`role=grid` clarification (React Aria).** Adobe's React Aria explicitly separated the passive reading `<table>` from the focus-managed `role="grid"`, providing low-level hooks (`useTable`/`useGridList`) for the correct keyboard contract — raising the interactive-table a11y bar.
5. **Virtualization + `aria-rowindex`** kept huge windowed tables honest to AT (and forced the complete-ARIA-grid-off-`<table>` route at scale).
6. **The current consensus — the hybrid.** Headless engine + DS skin for standard tables (semantic + visual purity); heavy commercial data grids reserved for specialized high-density spreadsheet use. Plus emerging **AI-presence** disclosure (Carbon) for AI-generated cells.

## 14. Sources cited
(Conservative; reconcile with external — 2026 version/licensing claims are volatile, flagged unverified.) **TanStack Table** (v9, ~June 2026 — the headless engine; modular `TFeatures`; ~1.1M→158K type instantiations) **+ TanStack Virtual** (windowing); **MUI** — `Table` (compose-your-own) + the **X `DataGrid`** (v9, ~April 2026 — the enterprise grid; charts/AI-assistant; Pro/Premium tiers); **AG Grid** (v35, ~May 2026 — the enterprise gold standard; virtualization/pivoting; Community/Enterprise); **Ant Design** — `Table` (sort/filter/select/expand/fixed-columns/virtual); **Shopify Polaris** — `DataTable` + `IndexTable` (the selectable index table; the `s-table` web-component migration; ~v2026-04); **GitHub Primer** — `DataTable` (the `aria-sort` + live-region reference; React ~v38.24, May 2026); **IBM Carbon** — `DataTable` (sortable/selectable/expandable/batch-actions; the "AI Presence" states; v11/React ~v1.110) — a strong a11y reference; **Adobe Spectrum / React Aria** — `TableView` / `useTable` / `useGridList` (the gold-standard accessible interactive table; the `aria-rowindex` virtualization handling; ~v3.49); **Atlassian** — `DynamicTable`; **Chakra UI** — `Table`; **Base Web (Uber)** — `Table`/`DataTable`. **WAI-ARIA APG** — the Table / Grid / Treegrid / sortable-table patterns; `<table>` semantics (`<caption>`, `<th scope>`); `aria-sort`; `aria-rowcount`/`aria-rowindex`. WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 1.4.10, 2.4.7, 4.1.3.

## 15. Agent-consumable schema
```yaml
identity:
  id: table
  name: Table
  aliases: [DataTable, DataGrid, Grid (data-grid sense), IndexTable, TableView, DynamicTable]
  category: data
  status: stable
description: >
  The tabular-data display (and the interactive data grid) — the KEYSTONE of the Data
  category and the catalogue's BIGGEST CONVERGENCE POINT. Presents data with genuine
  row × column relationships (a cell's meaning depends on BOTH its column and row). It
  is where Grid's role=grid boundary lands (CSS display:grid is presentational; role=grid
  is the interactive data grid = Table), and it composes Checkbox/Pagination/EmptyState/
  Skeleton/Menu/Tag/Badge/Avatar/Button/Link/Tooltip. NOT a CSS Grid layout (role=grid !=
  display:grid), NOT a List (1D, no columns), NOT a layout table (the dead anti-pattern).
  The headline: the data-table (reading mode, native <table>) vs data-grid (application
  mode, role=grid) genre split decides the entire a11y model.
anatomy:
  parts:
    - "table container: manages horizontal overflow / radius / the scroll context"
    - "<caption>: the table's accessible name (visible or hidden); first child of <table>"
    - "toolbar: global search, density toggle, column-visibility menu, the bulk-action bar (on selection)"
    - "<thead> + header row: <th scope=col>; a sortable header composes a <button> (sort indicator + aria-sort); the first header composes the select-all Checkbox; may be sticky"
    - "<tbody> + data rows: <tr> of <td>; a row composes an expand trigger / a selection Checkbox / a trailing row-actions Menu; <th scope=row> (often a frozen first column)"
    - "<td> (the cell): the injection point for Tag/Badge/Avatar/Button/Link or truncated text + Tooltip"
    - "<tfoot>/footer: aggregation rows (totals) + Pagination"
    - "sticky/frozen regions: position:sticky + a box-shadow/pseudo-element elevation shadow"
    - "terminal-state regions: Skeleton rows (loading) / Empty State (zero results) / error boundary"
    - "the DATA MODEL (not visual): column definitions + row data — the headless heart"
api:
  composes: [checkbox, pagination, empty-state, skeleton, menu, tag, badge, avatar, button, link, tooltip]
  role-grid-boundary-from: [grid]
  model: "columns-as-config + rows-as-data (NOT raw JSX children — that makes sort/filter impossible without DOM parsing)"
  column-def:
    - "accessor/key (the data field)"
    - "header (the <th> content)"
    - "cell (the renderer — THE injection point where Tag/Badge/Avatar/Button/Menu compose)"
    - "sortable/filterable"
    - "width/align (numeric->end) / minWidth"
    - "pin/sticky (freeze inline-start/end)"
    - "enableHiding (column-priority responsive)"
  props:
    - {name: data/rows, type: "Row[]", default: ~, required: true}
    - {name: sorting, type: "sortBy (single|multi) + onSortChange", default: ~, required: false, description: "drives aria-sort"}
    - {name: selection, type: "selectionMode (none|single|multiple) + selectedKeys + onSelectionChange", default: none, required: false}
    - {name: pagination, type: "page/pageSize/onPageChange", default: ~, required: false, description: "composes Pagination"}
    - {name: density, type: "'comfortable'|'compact'|'condensed'", default: comfortable, required: false}
    - {name: virtualization, type: boolean, default: false, required: false, description: "window large datasets + the aria-rowcount/rowindex it requires"}
    - {name: server-vs-client, type: "manualSorting/manualPagination flags", default: client, required: false, description: "client (in-browser over the full dataset) vs SERVER (emit callbacks, refetch windowed slices); transition without changing the visual implementation"}
  headless-vs-batteries: "HEADLESS (TanStack Table — outputs raw state + functions (row.getVisibleCells()); v9's modular TFeatures cut type instantiations ~1.1M->158K (~86% faster type-check); the DS wires it to the semantic DOM) vs BATTERIES-INCLUDED (MUI X DataGrid, AG Grid — massive prop surfaces, export/editing/charting, heavier >100KB gzipped + CSS you fight). Practice: a headless engine + an opinionated a11y-correct skin"
states:
  macro-terminal-machine: [loading, content, empty, error]   # Skeleton rows -> populated -> Empty State (differentiate inherently-empty vs filtered-to-zero) -> error+retry
  column: [unsorted, ascending, descending, resizable, hidden]
  row: [default, hover, focus, selected, expanded, disabled, ai-generated]   # ai-generated = Carbon's AI-presence (gradient/inner-shadow disclosure)
  selection: [none, some-indeterminate, all]
variants:
  genre: [data-table, interactive-data-grid, treegrid]   # <table> reading / role=grid application / hierarchical
  density: [comfortable, compact, condensed]              # ~16px/48-56px row vs ~4-8px/32px row
  selection: [none, single, multiple]
  layout: [scroll, sticky-header, frozen-column, virtualized]
  responsive: [scroll, stacked-card, column-priority]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "1.4.10", "2.4.7", "4.1.3"]
  genre-decides-the-model: "native <table> for tabular data, role=grid ONLY for the genuine interactive widget, NEVER PARTIAL div-soup (the one legit non-<table> route = COMPLETE-ARIA-grid for heavy virtualization)"
  native-table-contract: "<caption> = the accessible name; <th scope=col>/<th scope=row> natively associate headers with cells (SR: 'Status, Active'); free with a real <table>, near-impossible in ARIA — THE reason to use one"
  sorting: "a sortable header wraps its label in a <button>; the <th> carries aria-sort=ascending|descending|none (only the sorted column); a polite aria-live announces the new order without stealing focus"
  interactive-grid: "role=grid/treegrid OVERRIDES native semantics: role=grid/row/gridcell/columnheader/rowheader; ONE tab stop; arrow-key nav via ROVING TABINDEX (focused cell tabindex=0 others -1 + .focus(); preferred when cells have interactive children) or ARIA-ACTIVEDESCENDANT (focus stays on the container, attr points at the active cell; for virtualized/readonly). treegrid adds aria-expanded/aria-level. The APG Grid pattern — a LOT; only when the interaction demands it"
  selection: "aria-selected (grid) or the checkbox state; the header select-all Checkbox shows INDETERMINATE for some-but-not-all (a DOM PROPERTY set via ref, not an attribute — the Checkbox brief), named 'Select all'"
  virtualization-tension: "windowing removes off-screen nodes -> AT says 'Table, 15 rows' for 10,000. FIX: aria-rowcount (true total) + aria-rowindex per rendered row (+ colcount/colindex). BUT these ARIA attrs on native <table> elements can trigger HTML-validation/SR issues -> heavy virtualization is often FORCED off native <table> to <div>+COMPLETE-ARIA-grid (the one legit non-<table> route; never PARTIAL div-soup)"
  responsive-stacked-loss: "the stacked-card view (display:block) BREAKS the native table associations (roles flatten) — re-apply ARIA roles or label as a list of records; horizontal scroll KEEPS the semantics (its a11y advantage)"
content:
  column-headers: "exceptionally concise (the sort/filter target; long headers = awkward targets + wrapping + clutter); a noun/short phrase; consistent capitalization"
  alignment: "text left (right in RTL); numeric/financial/%/date RIGHT-aligned (inline-end) + font-variant-numeric:tabular-nums (equal digit width, aligned decimals)"
  units-formatting: "format via Intl; put the unit in the HEADER ('Size (MB)') not every cell"
  truncation: "single-line ellipsis + a Tooltip (full text on hover/focus) PREFERRED over multi-line wrapping (kills density, disrupts zebra-striping, complicates virtualization)"
  empty-copy: "explain WHY ('No transactions for the selected date range') + a recovery path ('Clear all filters'); Empty State first-use-vs-no-results; never an unexplained empty body"
  dont-overload: "20 columns is unreadable -> column-priority/hiding, a detail row, or a different view"
motion:
  restraint: "DOM-node volume = a 60fps risk; DON'T FLIP large-table sort reorders (layout thrashing/painting bottlenecks) — reorder instantly at scale (FLIP only smooths a SMALL table)"
  native-css-trend: "leading systems (React Aria, HeroUI) strip JS animation runtimes (Framer Motion) for native CSS transitions on row expand/hover (less main-thread blocking, GPU-accelerated)"
  loading-swap: "a seamless cross-fade Skeleton->content, GIVEN strict geometric parity (no CLS)"
  expand-collapse: "treegrid/detail-row height transition (the Accordion discipline)"
  reduce-motion: "drop sort/reflow/expand to instant; the data is the information, not the motion"
i18n:
  rtl: "the column order MIRRORS automatically (native with <table>, or via logical properties — margin-inline-start — inherited from Box): first column on the right, sort indicators + the frozen row-header column flip to inline-start; numeric columns align to the logical start"
  number-date-currency: "via Intl.NumberFormat/DateTimeFormat (locale digits/grouping/decimal/date-order); no hardcoded string manipulation"
  expansion: "headers/caption +30-50% (DE/RU) -> the column-sizing algorithm (minmax()/TanStack grow-collapse) must adapt without forcing isolated-column scroll; variable header/row height"
implementation:
  - "build on a REAL <table> (the a11y foundation): caption/thead/th-scope/tbody/td -> relationships for free. CSS friction: display:grid/flex/block on table elements REMOVES the semantics (the classic trap — display:block for sticky/scroll silently strips the roles). Prefer position:sticky on <th> + a scroll container; if you must restyle, re-apply role=table/row/cell"
  - "the sticky-header SUB-PIXEL GAP BUG: position:sticky on <thead> leaves a transparent ~1px gap (border sub-pixel rendering) through which data text bleeds; fix with a SOLID bg on <th> + a pseudo-element/box-shadow covering it (doubles as the sticky elevation shadow)"
  - "the headless engine: separate the LOGIC (column model + sort/filter/paginate/select/group/expand — TanStack) from the MARKUP (the DS's a11y-correct <table>); drives both genres; manual* flags for server-side"
  - "virtualization (TanStack Virtual/react-window) + aria-rowcount/rowindex; FIXED-height rows = O(1) random access, VARIABLE-height = O(log n) (prefix-sum arrays); React.memo row/cell renderers (rapid mount/unmount on scroll -> keep GC off the main thread)"
  - "the select-all indeterminate: a DOM PROPERTY (input.indeterminate=true via ref), NOT an HTML attribute — the Table exposes the Checkbox ref to govern it (the Checkbox brief): checked=all, indeterminate=some, unchecked=none"
  - "the sortable-header <button> (Enter/Space) + aria-sort on the <th> + a polite live region announcing the new sort"
  - "the responsive transform (NO CLEAN WINNER): SCROLL (overflow-x:auto wrapper — preserves <table>+ARIA, the safest, the opinionated enterprise default) / STACK (display:block per row -> a card + <th> labels via ::before content:attr(data-label) — great on mobile but DESTROYS the table semantics) / HIDE (column-priority — preserves semantics, risks hiding vital data). Horizontal scroll is the most robust default"
  - "cell renderers compose the cluster: the cell render fn returns Tag/Badge/Avatar/Button/Link/Menu — the Table provides the cell, the renderer fills it (the convergence in code)"
  - "the DataGrid-as-a-product reality: the full grid (MUI X DataGrid, AG Grid) is a HEAVYWEIGHT, often commercially-licensed product (Pro/Premium, Enterprise; >100KB gzipped) — many teams should compose a headless engine + a <table> instead"
  - "headless vs opinionated: ship the headless engine (logic) + an opinionated a11y-correct default skin (the <table> markup + styling); the engine is the reusable value, the skin is the DS's contract"
composition:
  role-grid-boundary-from: [grid]
  composes: [checkbox, pagination, empty-state, skeleton, menu, tag, badge, avatar, button, link, tooltip]
  borders: [list, tree]                    # 1D sibling / hierarchical sibling (treegrid = table + tree) — not yet briefed
  responsive-to: [card]                    # the stacked row -> Card transform
  alternative-to: [list, "grid-of-cards", "description-list <dl>"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "data-table (<table>, reading mode — the practice default) vs data-grid (role=grid, application mode — only when the spreadsheet interaction is genuinely needed)"
    - "headless engine + DS skin (practice) vs a batteries-included DataGrid product (MUI X / AG Grid)"
    - "Table/DataTable (display) vs DataGrid (interactive) as separate named components (practice — the genre split made legible)"
    - "the responsive approach: scroll vs stack vs hide — NO CLEAN WINNER (framework, not a winner; scroll is the safest default)"
    - "client-side vs server-side data model"
  trap:
    - "architectural over-reach: role=grid on a display table (promises a keyboard model that isn't there)"
    - "PARTIAL div-soup (role=table without the FULL role set) — the only legit non-<table> route is COMPLETE-ARIA-grid for heavy virtualization"
    - "display:grid/flex/block on table elements stripping the table semantics (the classic CSS trap)"
    - "the sticky-header sub-pixel gap (text bleeds through — solid bg + pseudo-element)"
    - "virtualization breaking the row count (needs aria-rowcount/rowindex; can force off native <table>); focus lost / GC stalls (React.memo)"
    - "the stacked-responsive view losing the <table> semantics; the select-all indeterminate set as an attribute not a DOM property"
    - "using a table for layout (lies to AT); a single-column table (-> List); 20 columns (-> hide/priority); FLIP on large reorders (jank)"
  inherited: "composes the whole briefed cluster (Checkbox/Pagination/Empty-State/Skeleton/Menu/Tag/Badge/Avatar/Button/Link/Tooltip); the role=grid boundary from Grid; the data-container terminal-states machine from Empty State/Skeleton; tabular-nums from Pagination"
  role-in-family: "the keystone of the Data category — the tabular-data display + the interactive data grid, the catalogue's biggest convergence point; where Grid's role=grid boundary lands; borders List (1D) + Tree (treegrid)"
  evolution:
    - "the layout-table anti-pattern -> tables-for-data-only"
    - "the batteries-included heavy grid (AG Grid, early MUI DataGrid) -> the headless turn (TanStack; v9 TFeatures)"
    - "the <table>-vs-role=grid clarification (React Aria useTable/useGridList)"
    - "virtualization + aria-rowcount/rowindex (forcing the complete-ARIA-grid route at scale)"
    - "the responsive-table approaches (scroll/stack/hide — no clean winner)"
    - "React-Aria/Spectrum raising the interactive-table a11y bar; the DataGrid-as-a-product (MUI X/AG Grid) heavyweight; emerging AI-presence disclosure (Carbon)"
  unverified:
    - "external 2026 version numbers (TanStack Table v9/Virtual, MUI X DataGrid v9, AG Grid v35, Polaris v2026-04/s-table, Primer v38.24, Carbon v11/React v1.110, React Aria v3.49)"
    - "the TanStack v9 TFeatures type-instantiation figures (~1.1M->158K, ~86%) — verify"
    - "MUI X / AG Grid commercial-licensing tiers + the MUI X AI-assistant / Carbon AI-presence features — verify current"
    - "React 19 / concurrent-mode impact on highly-virtualized grid re-renders"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-table/` (16 June 2026), the fortieth brief — the **keystone of the Data category** (the first Data brief), the **catalogue's biggest convergence point**, and the hardest component in the set: the structural chassis where Checkbox, Pagination, Empty State, Skeleton, Menu, Tag, Badge, Avatar, Button, Link, and Tooltip integrate, and where **Grid's `role=grid` boundary lands** (CSS `display:grid` is presentational; `role=grid` is the interactive data grid = here). The two passes converged with no genuine fork — the data-table-vs-data-grid genre split + the native-`<table>`/`role=grid`/never-partial-div-soup decision (which decides the entire a11y model), the column-model + headless-vs-batteries-included architecture, sorting (`aria-sort` + the header button) + selection (the checkbox column + the select-all indeterminate-via-ref), sticky headers/frozen columns + virtualization, the responsive-table problem (scroll/stack/hide — no clean winner, scroll the safest), and the composition convergence. The external pass sharpened with decisive concrete detail: the **virtualization-forces-complete-ARIA-grid exception** (applying `aria-rowindex` to native `<table>` elements can trigger validation/SR issues, so heavy virtualization is often forced off `<table>` — the one legitimate non-`<table>` route, never *partial* div-soup), the **roving-tabindex-vs-`aria-activedescendant`** focus-strategy split (interactive-children vs virtualized/readonly), the **sticky-header sub-pixel-gap bug** (text bleed-through; solid-bg + pseudo-element), the **variable-height O(log n) + `React.memo`** virtualization cost, **TanStack v9's `TFeatures`** (~1.1M→158K type instantiations, ~86% faster), and IBM Carbon's novel **"AI Presence" cell states** (gradient/inner-shadow disclosure of AI-generated data). Claude-pass contributions: the Data-keystone/convergence framing, the genre-split-decides-the-a11y-model thesis, the composition map back into the whole briefed cluster, the Table-vs-List-vs-Grid-of-Cards-vs-`<dl>` boundary set, and the headless-engine-plus-skin resolution. The 2026 version numbers, the TanStack type figures, the commercial-licensing tiers, and the AI features are flagged unverified. Conformant to `components/_schema.md`. **The Data category is open** — Table the keystone; List and Tree are its siblings still to come.*

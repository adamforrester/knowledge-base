# Table — field-truth study (Claude pass)

## 1. Framing
A Table presents **tabular data** — information with genuine row × column relationships, where a cell's meaning depends on *both* its column header and its row. It is the **keystone of the Data category** (the first Data brief) and the **catalogue's biggest convergence point**: a Table composes Checkbox (selection), Pagination (paging), Empty State + Skeleton (the no-data/loading states), Menu (row actions), and Tag/Badge/Avatar/Button/Link/Tooltip (cell content) — the brief where the whole catalogue pays off. It is also where **Grid's `role=grid` boundary lands**: Grid established that CSS `display: grid` is *presentational* and is *not* the interactive ARIA data-grid pattern — Table is where `role=grid` (and `role=treegrid`) actually lives.

The headline that decides everything else is the **data-table vs data-grid genre split**, and the **`<table>` / `role=grid` / div-soup** decision that follows from it:
- **The static / data table** — displays tabular data, maybe sortable + paginated, with links/buttons in cells, but **not arrow-key-navigable**. *Reading* mode. A native **`<table>`** (`<caption>`/`<thead>`/`<th scope>`/`<tbody>`/`<td>`). **The vast majority of "tables" are this**, and the practice default.
- **The interactive data grid** — a spreadsheet-like *widget*: arrow-key cell navigation (one tab stop + roving focus / `aria-activedescendant`), editable cells, column resize/reorder, the full APG **`role=grid`/`treegrid`** pattern. *Application* mode. Powerful, heavy, and **over-reached for** — teams reach for a data grid when a sortable `<table>` would serve.
- **The div-soup trap** — recreating table semantics with `role=table/row/cell` when native `<table>` can't be used (CSS-layout flexibility). A last resort needing the *full, exact* ARIA role set; partial div-soup is an a11y catastrophe.

The genre split *is* the accessibility model: native `<table>` for tabular data, `role=grid` **only** for the genuine interactive widget, never partial div-soup. What it *isn't*: a **CSS Grid layout** (`role=grid` ≠ `display: grid` — the naming collision Grid named; see grid), a **List** (1D records, no column relationships — not yet briefed), or a **layout table** (the dead anti-pattern — tables are for *data*, never visual layout). Why systems disagree: the genre split, the headless-vs-batteries-included architecture, and the responsive-table problem (which has no clean winner).

## 2. Anatomy and parts
- **`<caption>`** — the table's **accessible name** (and visible title); the first child of `<table>`.
- **`<thead>` + the header row** — `<th scope="col">` cells; a **sortable header** is a `<button>` *inside* the `<th>` carrying `aria-sort` (§6). The header may be **sticky** (§ sticky).
- **`<tbody>` + the data rows** — `<tr>` rows of `<td>` cells; a row may have a **`<th scope="row">`** row-header (the row's label, often a sticky/frozen first column).
- **the selection column** — a leading column of **Checkbox**es (row select) with a **select-all Checkbox** in the header (its **indeterminate** state when some-but-not-all rows are selected — the Checkbox brief's indeterminate; see checkbox).
- **the row-actions cell** — a trailing column with a per-row overflow **Menu** (edit/delete/…) (see menu).
- **the toolbar** — above the table: search/filter, the bulk-action bar (appears on selection), column visibility, density toggle.
- **the pagination / footer** — **Pagination** controls or a load-more / infinite scroll (see pagination).
- **the empty / loading / error regions** — the no-data **Empty State**, the **Skeleton** loading rows, the error state (§ states; see empty-state, skeleton).
- **the data model (not visual):** the **column definitions** (accessor/header/cell-renderer/sortable/width/align/pin) + the **row data** — the headless heart of the API (§3).

## 3. Properties / API
**The column model is the heart of the API.** A Table is configured by **column definitions** + **row data**, not by hand-written markup:
- **`columns`** — each: `accessor`/`key` (the data field), `header` (the column label), **`cell`** (a render function — where Tag/Badge/Avatar/Button/Menu compose — §12), `sortable`, `width`/`minWidth`, `align` (start/end/center — numeric → end), `pin`/`sticky` (frozen column), `enableHiding`.
- **`data` / `rows`** — the row array (or a paginated/virtualized slice).
- **sorting** — `sortBy` (single or **multi-column**), `onSortChange`; the sort state drives `aria-sort` on the header (§6).
- **the selection model** — `selectionMode` (none/single/multiple), `selectedKeys`, `onSelectionChange`; the select-all + indeterminate (§ selection).
- **pagination** — `page`/`pageSize`/`onPageChange` (composes Pagination — see pagination), or virtualization for the unpaginated case.
- **sticky / pin** — sticky header (default-on for scroll), pinned columns (frozen first/last).
- **virtualization** — windowing for large datasets (§ virtualization) + the `aria-rowcount`/`aria-rowindex` it requires.
- **density** — comfortable / compact / condensed (row height).
- **server-vs-client data (the load-bearing architecture choice)** — *client-side* (sort/filter/paginate in the browser over the full dataset — simple, bounded by what fits in memory) vs *server-side* (the table emits sort/filter/page *requests*; the server returns the slice — required for large/remote data). The API must support both: the headless engine either *does* the work or *delegates* it via `manualSorting`/`manualPagination` flags.
- **the headless-vs-batteries-included split** — **headless** (TanStack Table: the sort/filter/paginate/select/group *logic* + the column model, *no markup/styles* — you render) vs **batteries-included** (MUI X DataGrid, AG Grid: a full component with built-in everything). The practice ships a **headless engine + an opinionated default skin** (the logic is reusable; the markup is the DS's a11y-correct `<table>`).

## 4. States and variants
- **States:**
  - **column:** sortable / sorted-ascending / sorted-descending / unsorted (`aria-sort`); resizable; hidden.
  - **row:** default / hover / **selected** (`aria-selected` + a selected background) / **expanded** (a detail row / `treegrid` child); disabled.
  - **selection:** none / some (**select-all indeterminate**) / all.
  - **table:** **loading** (Skeleton rows — see skeleton) / **empty** (Empty State — see empty-state) / **error** / populated — the **data-container terminal-states machine** (loading → content | empty | error) Empty State described.
- **Variants:**
  - **genre:** data table (`<table>`, reading mode) / interactive data grid (`role=grid`, application mode) / treegrid (hierarchical/expandable rows).
  - **density:** comfortable / compact / condensed.
  - **selection:** none / single / multiple (+ the bulk-action bar).
  - **layout:** scroll / sticky-header / frozen-column / virtualized.
  - **responsive:** scroll / stacked-card / column-priority (§ responsive).

## 5. Usage guidance
- **Use a Table for genuine tabular data** — records with consistent attributes the user compares *across rows* and *down columns* (a transactions list, a users admin, a metrics report). The test: does a cell's meaning depend on *both* its column and its row? Yes → table.
- **Table vs the alternatives:**
  - **vs a List** — a List is *1D* records (a feed, a settings list, a menu) with no column relationships; reach for a List (not yet briefed) when there are no columns to compare. (Don't build a single-column table.)
  - **vs a Grid / Card gallery** — heterogeneous, image-heavy, browse-mode content → a **Grid of Cards** (see grid, card); homogeneous, dense, scannable, comparable records → a Table (the Card-vs-row boundary, from the table side).
  - **vs a description list (`<dl>`)** — key-value pairs for a *single* entity (a detail panel) → a `<dl>`, not a one-row table.
- **The data-table-vs-data-grid decision (the load-bearing one):** is the user *reading/scanning* data (sort, paginate, click a link) → a **`<table>`** (reading mode, simpler, more accessible). Is the user *operating* a spreadsheet-like surface (arrow-key cell navigation, in-cell editing, bulk reorganization) → a **`role=grid`** data grid (application mode, heavy). **Default to the table; reach for the grid only when the spreadsheet interaction is genuinely needed** — the grid's keyboard model is a real cost.
- **When to virtualize** — only for *large* datasets (thousands of rows) that aren't paginated; virtualization adds a11y complexity (§6) and should not be the default for a 50-row table (pagination or plain rendering is simpler and more robust).
- **Don't use a table for layout** — the dead anti-pattern; tables convey *data relationships* to AT, so a layout table lies to screen readers. Layout is Box/Stack/Grid (see box, stack, grid).
- **The responsive approach is a deliberate choice** (§ responsive) — pick scroll / stack / hide per the data and the a11y cost, not by default.

## 6. Accessibility
The accessibility model **hinges entirely on the genre** (§1), and Table is one of the most a11y-laden components in the catalogue.

- **The native `<table>` contract (the default, and the most robust).** A real `<table>` gives AT the row/column structure for free: **`<caption>`** is the accessible name; **`<th scope="col">`** / **`<th scope="row">`** associate header cells with their column/row so a screen reader announces "Status, Active" (column header + cell) as it navigates; the structure lets AT users query "what column am I in?". This is *the* reason to use a real `<table>` over div-soup — you get the relationships for free, and they're nearly impossible to fully replicate with ARIA.
- **Sorting — `aria-sort` + the header button.** A sortable column header wraps its label in a **`<button>`** (the sort is an action); the `<th>` carries **`aria-sort="ascending|descending|none"`** (only the *currently-sorted* column has ascending/descending; others `none`). The sort change should announce (a polite live region: "Sorted by Name, ascending") since the visual reorder isn't otherwise conveyed.
- **The interactive data grid (`role=grid`/`treegrid`).** Only when it's a genuine grid widget: **one tab stop** into the grid, then **arrow-key cell navigation** (roving tabindex or `aria-activedescendant`), `role="grid"` + `role="row"` + `role="gridcell"`/`columnheader`/`rowheader`, `aria-rowindex`/`aria-colindex`, and the editable-cell model (Enter to edit, Escape to cancel). **`treegrid`** adds row expansion (`aria-expanded`/`aria-level`) — the hierarchical sibling (relates to Tree). This is the APG Grid pattern, and it's a *lot* — don't take it on unless the interaction demands it.
- **Selection — `aria-selected` + the select-all indeterminate.** Selected rows carry `aria-selected="true"` (in a grid) or use the checkbox column's state; the **header select-all Checkbox** shows the **indeterminate** state when some-but-not-all rows are selected (the Checkbox brief's indeterminate-as-DOM-property — see checkbox), and its accessible name is "Select all". The bulk-action bar appearing on selection should be announced.
- **Virtualization — the `aria-rowcount`/`aria-rowindex` tension (the sharp trap).** Windowing renders only visible rows, which **breaks the native `<table>`'s implicit row count** — AT would announce "row 5 of 12" when there are really 10,000. The fix: declare **`aria-rowcount`** (the true total) on the table and **`aria-rowindex`** on each rendered row (its true position), plus `aria-colcount`/`aria-colindex` if columns virtualize. Manage focus when the focused row unmounts on scroll (the row the user was on disappears — restore focus sensibly). Virtualization is where the `<table>` semantics and performance genuinely conflict.
- **The responsive stacked-view semantics loss** — turning rows into stacked cards (§ responsive) usually **breaks the `<table>` semantics** (the `display: block` flattening removes the table roles); either re-apply ARIA table roles, or accept that the stacked view is a *list of records* (and label it as such). The horizontal-scroll approach keeps the semantics intact — its a11y advantage.
- **WCAG SCs:** **1.3.1** (info & relationships — the table/header structure), **2.1.1** (keyboard — sorting, selection, grid navigation), **4.1.2** (name/role/value — `aria-sort`, `aria-selected`, the grid roles), **1.4.10** (reflow — the responsive approach at 320px), **2.4.7** (focus visible — the cell/row focus in a grid), **4.1.3** (status messages — the sort/selection announcements). Table is the brief where a11y depth is greatest.

## 7. Content guidelines
- **Column headers** — concise, scannable, and the sort target; a noun or short phrase ("Last active", not "The date this user was last active"). Consistent capitalization.
- **Numeric alignment + `tabular-nums`** — right-align (inline-end) numeric columns and use `font-variant-numeric: tabular-nums` so digits align in a column (the same digit-width discipline Pagination used — see pagination); left-align text, and align the header to its column's content.
- **Units & formatting** — format numbers/dates/currency consistently (via `Intl` — §9); put the unit in the *header* ("Size (MB)") rather than repeating it in every cell.
- **Truncation + Tooltip** — long cell content truncates with ellipsis + the full text in a **Tooltip**/`title` (the Tag/Avatar truncation discipline — see tooltip); don't let one long cell blow out a column.
- **The empty-state copy** — the no-data state uses an **Empty State** with genre-appropriate copy (first-use vs no-results — see empty-state); never an empty table body with no explanation.
- **Don't overload columns** — a table with 20 columns is unreadable; use column-priority/hiding, a detail row, or a different view. The caption/header should make the table self-describing.

## 8. Motion and transition
- **Restrained by default** — large tables + motion is a performance and distraction risk. Sorting *reorders* rows; a **FLIP** animation can smooth a *small* table's reorder (the technique Stack/Grid/Tag share — see stack), but **don't animate large/virtualized table reorders** (jank + the rows may be windowed). The default is an instant reorder.
- **Row expand/collapse** (treegrid / detail row) — a height transition for the detail row (the Accordion height-animation discipline — see accordion); gate behind reduce-motion.
- **The loading→content swap** — Skeleton rows crossfade to real rows on load (see skeleton); row insert/remove can fade, sparingly.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops sort/reflow/expand animation to instant; the data is the information, not the motion.

## 9. Internationalization
- **RTL — the column order mirrors.** Under `dir="rtl"` the columns run right-to-left (the first column on the right), the sort indicators and the row-header (frozen first column) flip to the inline-start (right), and the selection/actions columns move accordingly — handled by logical properties inherited from Box (see box), no JS. Numeric columns still align to their logical edge.
- **Number / date / currency formatting** — via **`Intl.NumberFormat`/`DateTimeFormat`** for locale digits, grouping, decimal separators, and date order; the formatting is locale-driven, not hardcoded.
- **Header + caption translation** — column headers and the caption localize; translated headers run longer (German/Russian +30%), so column widths must tolerate wrapping/expansion (variable header height) — don't hardcode header widths that clip translations.
- **Variable row height** from text expansion — rows must grow with wrapped content (and equal-height isn't expected across rows the way it is across cards).

## 10. Naming
- **The field set:** **`Table`** (the basic styled `<table>` — Chakra, MUI's base, the semantic display table); **`DataTable`** (Polaris, Primer, Carbon, Base Web — the *featured* display table: sortable/selectable/paginated, still `<table>`-based); **`DataGrid`** (MUI X, AG Grid — the *interactive* `role=grid` enterprise widget); **`IndexTable`** (Polaris — the selectable index table); **`TableView`** (React Aria/Spectrum — the accessible interactive collection table); **`DynamicTable`** (Atlassian).
- **The practice's default — name by the genre split:** **`Table`** for the semantic display table (`<table>`-based, sortable/selectable/paginated — the common case, the default reach), and a separate, heavier **`DataGrid`** for the interactive `role=grid` widget (arrow-key navigation, editing, virtualization at scale). Naming them apart *is* the genre split made legible — it stops teams from reaching for the grid's weight when they need the table. Build both on a shared **headless engine** (the column model + sort/filter/select logic) with different skins + a11y models.
- **Aliases to map:** DataTable, DataGrid, Grid (the data-grid sense — distinct from the layout Grid), IndexTable, TableView, DynamicTable.

## 11. Implementation notes
- **Build on a real `<table>` (the a11y foundation).** Use `<table>`/`<caption>`/`<thead>`/`<th scope>`/`<tbody>`/`<td>` for the display table — you get the row/column relationships for free. The CSS friction: `display: grid`/`flex` on table elements *removes the table semantics* (the classic trap — styling a `<table>` with `display: block` for sticky headers/scroll silently strips the roles, requiring ARIA re-application). Prefer `position: sticky` on `<th>` + a scroll container over `display`-hacking the table; if you must restyle, re-apply `role="table/row/cell"`.
- **The headless engine.** Separate the *logic* (the column model, sort/filter/paginate/select/group/expand state — TanStack Table is the reference) from the *markup* (the DS's a11y-correct `<table>`). This lets the same engine drive the display table and the data grid with different renderers, and supports `manual*` flags for server-side data (the engine delegates the work, manages only the state).
- **Sticky header + frozen column + the alignment problem.** Sticky header: `position: sticky; top: 0` on `<th>` (within a scroll container). Frozen column: `position: sticky; inset-inline-start: 0` on the first column's cells + a separating shadow on scroll. **The header-body column-alignment problem** (when header and body are separate scroll areas — the old two-table approach) is why the single-`<table>` + `position: sticky` approach is preferred (alignment is automatic).
- **Virtualization + `aria-rowindex`.** Window the rows (TanStack Virtual / react-window); declare `aria-rowcount` (true total) + `aria-rowindex` per rendered row so AT reports the real position; manage focus when the focused row scrolls out of the window. (The virtualization-vs-`<table>`-semantics tension — §6.)
- **The select-all indeterminate wiring.** The header Checkbox's `indeterminate` is a **DOM property, not an attribute** (set via ref — the Checkbox brief's note; see checkbox): `checked` when all selected, `indeterminate` when some, unchecked when none.
- **The sortable-header button + `aria-sort`.** The header label is a `<button>` (Enter/Space sorts); the `<th>` gets `aria-sort`; a polite live region announces the new sort.
- **The responsive transform.** Three implementations: **scroll** (wrap the table in an `overflow-x: auto` container — keeps semantics, the safest); **stack** (CSS `display: block` per row → a card, with the column header injected via `::before`/`data-label` for the th-scope-row flip — *loses table semantics*, re-apply ARIA or treat as a list); **hide** (column-priority — hide low-priority columns at breakpoints, a detail row/expand for the rest). No clean winner — choose per data + a11y cost.
- **Cell renderers compose the cluster** — the `cell` render function returns Tag/Badge/Avatar/Button/Link/Menu (see those briefs); the Table provides the cell, the renderer fills it. This is the convergence in code.
- **The DataGrid-as-a-product reality** — the full interactive grid (MUI X DataGrid, AG Grid) is a *heavyweight product* (virtualization + editing + pivoting + grouping + column management), often commercially licensed (MUI X Pro/Premium, AG Grid Enterprise). The practice's `DataGrid` is a real cost; many teams should compose a headless engine + a `<table>` instead of adopting an enterprise grid.
- **Headless vs opinionated** — ship the headless engine (logic) + an opinionated, a11y-correct default skin (the `<table>` markup + the styling); the engine is the reusable value, the skin is the DS's contract.

## 12. Related and alternative components
- **The `role=grid` boundary from Grid** — Table is where the interactive ARIA data-grid pattern lives; CSS `display: grid` is the *layout* Grid and is presentational (the naming collision Grid named — see grid).
- **Composes (the convergence — the brief where the catalogue pays off):** **Checkbox** (row selection + the select-all indeterminate — see checkbox), **Pagination** (the page controls — see pagination), **Empty State** (the no-data zero-state — see empty-state) + **Skeleton** (the loading rows — see skeleton) (the data-container terminal-states machine), **Menu** (the row-actions overflow — see menu), and cell content — **Tag** / **Badge** / **Avatar** / **Button** / **Link** / **Tooltip** (see tag, badge, avatar, button, link, tooltip).
- **Borders (siblings):** **List** (the 1D simpler sibling — records without column relationships — not yet briefed), **Tree** (the hierarchical sibling; `role=treegrid` = table + tree — not yet briefed).
- **Responsive boundary:** the stacked-card view turns each row into a **Card** (see card) — the responsive transform (with the semantics caveat — §6).
- **Alternative to:** a **List** (1D records), a **Grid of Cards** (heterogeneous/visual/browse), a **description list `<dl>`** (single-entity key-value).

(The keystone of the Data category — the tabular-data display + the interactive data grid, and the catalogue's biggest convergence point. It is where Grid's `role=grid` boundary lands, and it composes Checkbox/Pagination/Empty-State/Skeleton/Menu/Tag/Badge/Avatar/Button/Link/Tooltip. See grid for the role=grid boundary, checkbox/pagination/empty-state/skeleton/menu for the composed machinery, tag/badge/avatar/button for the cell content, card for the responsive row→card, list/tree when briefed for the siblings. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The layout-table anti-pattern → tables-for-data-only.** Tables were once the layout mechanism of the web; CSS layout (and the recognition that a layout table lies to AT) ended that — tables now convey *data relationships*, and layout is Box/Stack/Grid.
2. **The headless-table turn.** TanStack Table (née react-table) separated the table *logic* (sort/filter/paginate/select/group) from the *markup*, letting design systems own the a11y-correct `<table>` while reusing the engine — the dominant modern architecture.
3. **The `<table>`-vs-`role=grid` clarification.** The field separated the *data table* (reading mode, `<table>`) from the *data grid* (application mode, `role=grid` APG pattern) — and learned not to slap `role=grid` on a display table (it promises a keyboard model that isn't there).
4. **Virtualization + `aria-rowindex`.** Windowing made huge tables performant, and the `aria-rowcount`/`aria-rowindex` discipline emerged to keep virtualized tables honest to AT.
5. **React Aria / Spectrum raising the interactive-table a11y bar.** Reference implementations of the accessible interactive table (the collection/selection model, the keyboard nav, the focus management) set the standard the rest of the field measures against.
6. **The DataGrid-as-a-product.** The full enterprise grid (MUI X, AG Grid) became a heavyweight, often-commercial *product* — clarifying that the interactive data grid is a major undertaking distinct from a sortable `<table>`.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- TanStack Table + TanStack Virtual — the headless table (column model, sort/filter/paginate/group/select) + virtualization.
- MUI — `Table` (compose-your-own) + the **X `DataGrid`** (the enterprise interactive grid; Pro/Premium tiers).
- AG Grid — the enterprise data-grid gold standard (virtualization, pivoting; Community/Enterprise).
- Ant Design — `Table` (sorting/filtering/selection/expandable/fixed-columns/virtual).
- Shopify Polaris — `DataTable` + `IndexTable` (selectable/sortable; the responsive).
- GitHub Primer — `DataTable` (the newer accessible table).
- IBM Carbon — `DataTable` (sortable/selectable/expandable/batch-actions — a strong a11y reference).
- Adobe Spectrum / React Aria — `TableView` (the gold-standard accessible interactive table; the collection/selection model).
- Atlassian — `DynamicTable`.
- Chakra UI — `Table` (the basic styled table).
- Base Web (Uber) — `Table` / `DataTable`.
- WAI-ARIA APG — the Table pattern, the Grid pattern, the Treegrid pattern, the sortable-table; `<table>` semantics (`<caption>`, `<th scope>`); `aria-sort`; `aria-rowcount`/`aria-rowindex` for virtualization.
- WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 1.4.10, 2.4.7, 4.1.3.

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
    - "<caption>: the table's accessible name (+ visible title); first child of <table>"
    - "<thead> + header row: <th scope=col> cells; a SORTABLE header is a <button> inside the <th> carrying aria-sort; may be sticky"
    - "<tbody> + data rows: <tr> of <td>; a row may have <th scope=row> (the row label, often a frozen first column)"
    - "the selection column: leading Checkboxes (row select) + a header select-all Checkbox with the INDETERMINATE state (some-but-not-all)"
    - "the row-actions cell: a trailing per-row overflow Menu (edit/delete)"
    - "the toolbar: search/filter, the bulk-action bar (on selection), column visibility, density"
    - "the pagination/footer: Pagination controls or load-more/infinite scroll"
    - "the empty/loading/error regions: Empty State (no data), Skeleton (loading rows), error"
    - "the DATA MODEL (not visual): column definitions (accessor/header/cell/sortable/width/align/pin) + row data — the headless heart"
api:
  composes: [checkbox, pagination, empty-state, skeleton, menu, tag, badge, avatar, button, link, tooltip]
  role-grid-boundary-from: [grid]   # CSS display:grid (layout) vs ARIA role=grid (interactive data grid = here)
  props:
    - {name: columns, type: "ColumnDef[]", default: ~, required: true, description: "each: accessor/key, header, CELL (render fn — where Tag/Badge/Avatar/Button/Menu compose), sortable, width/minWidth, align (numeric->end), pin/sticky, enableHiding — the heart of the API"}
    - {name: data/rows, type: "Row[]", default: ~, required: true, description: "the row array (or a paginated/virtualized slice)"}
    - {name: sorting, type: "sortBy (single|multi) + onSortChange", default: ~, required: false, description: "drives aria-sort on the header"}
    - {name: selection, type: "selectionMode (none|single|multiple) + selectedKeys + onSelectionChange", default: none, required: false, description: "the checkbox column + select-all + indeterminate"}
    - {name: pagination, type: "page/pageSize/onPageChange", default: ~, required: false, description: "composes Pagination; or virtualization for the unpaginated case"}
    - {name: "sticky/pin", type: "boolean | column-pin", default: "sticky header on", required: false, description: "sticky header + frozen first/last column"}
    - {name: virtualization, type: boolean, default: false, required: false, description: "window large datasets + the aria-rowcount/rowindex it requires"}
    - {name: density, type: "'comfortable'|'compact'|'condensed'", default: comfortable, required: false}
    - {name: "server-vs-client", type: "manualSorting/manualPagination flags", default: client, required: false, description: "client (sort/filter/paginate in-browser over the full dataset) vs SERVER (emit requests, the server returns the slice — for large/remote data)"}
  headless-vs-batteries: "HEADLESS (TanStack Table — the sort/filter/paginate/select/group LOGIC + the column model, no markup) vs BATTERIES-INCLUDED (MUI X DataGrid, AG Grid — a full component). Practice: a headless engine + an opinionated a11y-correct <table> skin"
states:
  column: [sortable, sorted-ascending, sorted-descending, unsorted, resizable, hidden]
  row: [default, hover, selected, expanded, disabled]
  selection: [none, some-indeterminate, all]
  table: [loading, empty, error, populated]   # the data-container terminal-states machine (loading->content|empty|error)
variants:
  genre: [data-table, interactive-data-grid, treegrid]   # <table> reading mode / role=grid application mode / hierarchical
  density: [comfortable, compact, condensed]
  selection: [none, single, multiple]
  layout: [scroll, sticky-header, frozen-column, virtualized]
  responsive: [scroll, stacked-card, column-priority]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "1.4.10", "2.4.7", "4.1.3"]
  genre-decides-the-model: "the a11y model HINGES on the genre — native <table> for tabular data, role=grid ONLY for the genuine interactive widget, NEVER partial div-soup"
  native-table-contract: "a real <table> gives the row/column structure for free: <caption> = the accessible name; <th scope=col>/<th scope=row> associate headers with cells (SR announces 'Status, Active'); near-impossible to fully replicate in ARIA — THE reason to use a real <table>"
  sorting: "a sortable header wraps its label in a <button>; the <th> carries aria-sort=ascending|descending|none (only the sorted column); announce the sort change (polite live region: 'Sorted by Name, ascending')"
  interactive-grid: "role=grid/treegrid ONLY for a genuine widget: ONE tab stop + arrow-key cell nav (roving tabindex / aria-activedescendant), role=grid/row/gridcell/columnheader/rowheader, aria-rowindex/colindex, editable cells (Enter/Escape); treegrid adds aria-expanded/aria-level (the Tree sibling). It's a LOT — don't take it on unless the interaction demands it"
  selection: "aria-selected on rows (grid) or the checkbox state; the header select-all Checkbox shows INDETERMINATE for some-but-not-all (the Checkbox brief's indeterminate-as-DOM-property), named 'Select all'; announce the bulk-action bar"
  virtualization-tension: "windowing BREAKS the native <table>'s implicit row count (AT would say 'row 5 of 12' when there are 10,000). FIX: aria-rowcount (true total) on the table + aria-rowindex per rendered row (+ aria-colcount/colindex if columns window); manage focus when the focused row unmounts on scroll"
  responsive-stacked-loss: "the stacked-card view (display:block flattening) usually BREAKS the <table> semantics — re-apply ARIA table roles or treat/label it as a list of records; the horizontal-scroll approach KEEPS the semantics (its a11y advantage)"
content:
  column-headers: "concise, scannable, the sort target (a noun/short phrase); consistent capitalization"
  numeric-alignment: "right-align (inline-end) numeric columns + font-variant-numeric:tabular-nums (digit alignment, cf. pagination); left-align text"
  units-formatting: "format numbers/dates/currency via Intl; put the unit in the HEADER ('Size (MB)') not every cell"
  truncation: "long cells truncate + the full text in a Tooltip/title; don't let one cell blow out a column"
  empty-copy: "the no-data state uses Empty State with genre-appropriate copy (first-use vs no-results); never an unexplained empty body"
  dont-overload: "20 columns is unreadable — use column-priority/hiding, a detail row, or a different view"
motion:
  restraint: "large tables + motion = perf/distraction risk; FLIP can smooth a SMALL table's sort reorder, but DON'T animate large/virtualized reorders (jank + windowed rows) — default to instant"
  expand-collapse: "treegrid/detail-row height transition (the Accordion discipline); gate behind reduce-motion"
  loading-swap: "Skeleton rows crossfade to real rows; row insert/remove fades sparingly"
  reduce-motion: "drop sort/reflow/expand to instant; the data is the information, not the motion"
i18n:
  rtl: "the column order MIRRORS (first column on the right), sort indicators + the frozen row-header column flip to inline-start, selection/actions columns move — logical properties inherited from Box, no JS"
  number-date-currency: "via Intl.NumberFormat/DateTimeFormat (locale digits/grouping/decimal/date-order) — not hardcoded"
  header-translation: "column headers + caption localize; translations run +30% (DE/RU) -> columns tolerate wrapping/expansion (variable header height), don't hardcode widths that clip"
  variable-row-height: "rows grow with wrapped content"
implementation:
  - "build on a REAL <table> (the a11y foundation): caption/thead/th-scope/tbody/td -> the row/column relationships for free. CSS friction: display:grid/flex on table elements REMOVES the table semantics (the classic trap — display:block for sticky/scroll silently strips the roles). Prefer position:sticky on <th> + a scroll container over display-hacking; if you must restyle, re-apply role=table/row/cell"
  - "the headless engine: separate the LOGIC (column model + sort/filter/paginate/select/group/expand state — TanStack Table) from the MARKUP (the DS's a11y-correct <table>); drives the display table AND the data grid with different renderers; manual* flags for server-side data"
  - "sticky header (position:sticky;top:0 on <th> in a scroll container) + frozen column (position:sticky;inset-inline-start:0 + a scroll shadow); the single-<table>+position:sticky approach auto-solves the header-body alignment problem the old two-table approach had"
  - "virtualization (TanStack Virtual/react-window) + aria-rowcount (true total) + aria-rowindex per rendered row; manage focus when the focused row scrolls out"
  - "the select-all indeterminate: a DOM PROPERTY not an attribute (set via ref — the Checkbox brief): checked=all, indeterminate=some, unchecked=none"
  - "the sortable-header <button> (Enter/Space) + aria-sort on the <th> + a polite live region announcing the new sort"
  - "the responsive transform: SCROLL (overflow-x:auto wrapper — keeps semantics, safest) / STACK (display:block per row -> a card + the column header via ::before/data-label for the th-scope-row flip — LOSES semantics, re-apply ARIA or treat as a list) / HIDE (column-priority + a detail row). No clean winner"
  - "cell renderers compose the cluster: the cell render fn returns Tag/Badge/Avatar/Button/Link/Menu — the Table provides the cell, the renderer fills it (the convergence in code)"
  - "the DataGrid-as-a-product reality: the full interactive grid (MUI X DataGrid, AG Grid) is a HEAVYWEIGHT, often commercially-licensed product (Pro/Premium, Enterprise) — many teams should compose a headless engine + a <table> instead"
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
    - "Table (display) vs DataGrid (interactive) as separate named components (practice — the genre split made legible) vs one component"
    - "the responsive approach: scroll vs stack vs hide — NO CLEAN WINNER (framework, not a winner)"
    - "client-side vs server-side data model"
  trap:
    - "role=grid on a display table (promises a keyboard model that isn't there); partial div-soup (role=table without the FULL role set)"
    - "display:grid/flex/block on table elements stripping the table semantics (the classic CSS trap)"
    - "virtualization breaking the row count (needs aria-rowcount/rowindex); focus lost when the focused row unmounts"
    - "the stacked-responsive view losing the <table> semantics (re-apply ARIA or label as a list)"
    - "the select-all indeterminate set as an attribute not a DOM property; a sortable header that's not a real button / missing aria-sort"
    - "using a table for layout (lies to AT); a single-column table (-> List); 20 columns (-> hide/priority)"
    - "animating large/virtualized table reorders (jank)"
  inherited: "composes the whole briefed cluster (Checkbox/Pagination/Empty-State/Skeleton/Menu/Tag/Badge/Avatar/Button/Link/Tooltip); the role=grid boundary from Grid; the data-container terminal-states machine from Empty State/Skeleton; tabular-nums from Pagination"
  role-in-family: "the keystone of the Data category — the tabular-data display + the interactive data grid, the catalogue's biggest convergence point; where Grid's role=grid boundary lands; borders List (1D) + Tree (treegrid)"
  evolution:
    - "the layout-table anti-pattern -> tables-for-data-only"
    - "the headless-table turn (TanStack — logic/markup separation)"
    - "the <table>-vs-role=grid clarification (data table vs data grid)"
    - "virtualization + aria-rowcount/rowindex for windowed rows"
    - "the responsive-table approaches (scroll/stack/hide — no clean winner)"
    - "React-Aria/Spectrum raising the interactive-table a11y bar"
    - "the DataGrid-as-a-product (MUI X / AG Grid) heavyweight, often-commercial"
  unverified:
    - "external 2026 version numbers across the surveyed systems (TanStack Table/Virtual, MUI X DataGrid tiers, AG Grid, React Aria TableView)"
    - "the per-system responsive-table default + the virtualization a11y specifics — verify against current implementations"
    - "MUI X / AG Grid commercial-licensing tiers — verify current"
```

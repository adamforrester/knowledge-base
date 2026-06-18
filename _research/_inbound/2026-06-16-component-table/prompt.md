You are researching the Table component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Table /
data grid is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Table is THE KEYSTONE OF THE DATA CATEGORY — the first Data brief, the
catalogue's BIGGEST CONVERGENCE POINT, and the hardest component in the set.
It is where many briefed components meet, and where Grid's role=grid
boundary lands. DO NOT re-derive the components it composes; reference them
and concentrate on the Table-specific substance:
- IT IS THE role=grid BOUNDARY GRID DEFERRED TO IT (components/grid.md):
  Grid established that CSS display:grid is PRESENTATIONAL and is NOT the
  interactive ARIA role=grid data-grid pattern — Table is where role=grid
  (and role=treegrid) actually lives. Resolve the native-<table> vs
  role=grid vs div-with-ARIA-roles decision.
- IT COMPOSES the briefed cluster: Checkbox (row selection + select-all,
  the select-all INDETERMINATE state the Checkbox brief established —
  components/checkbox.md); Pagination (the page controls —
  components/pagination.md); Empty State (the no-data zero-state) + Skeleton
  (the loading rows) — the data-container terminal-states machine
  (loading->content->empty->error) Empty State described
  (components/empty-state.md, skeleton.md); Menu (the row-actions overflow —
  components/menu.md); and cell content — Tag/Badge/Avatar/Button/Link/
  Tooltip (components/tag.md, badge.md, avatar.md, button.md, link.md,
  tooltip.md). This is the brief where the whole catalogue pays off.
- IT BORDERS List (the 1D simpler sibling — not yet briefed) and Tree (the
  hierarchical sibling; role=treegrid = table + tree — not yet briefed);
  and its responsive STACKED view turns each row into a Card
  (components/card.md). Forward-reference List/Tree.

THE DEFINING TABLE-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE DATA-TABLE vs DATA-GRID GENRE SPLIT + THE <table>/role=grid/div-soup
  DECISION (the headline — it decides the entire a11y model): (1) the
  STATIC/DATA TABLE — displays tabular data, maybe sortable + paginated,
  with links/buttons in cells, but NOT arrow-key-navigable; READING mode;
  native <table> (<caption>/<thead>/<tbody>/<th scope>/<td>). (2) the
  INTERACTIVE DATA GRID — a spreadsheet-like widget: arrow-key cell
  navigation (one tab stop + roving focus/aria-activedescendant), editable
  cells, column resize/reorder, the full role=grid/treegrid APG pattern;
  APPLICATION mode. Most "tables" are the former; teams over-reach for the
  latter. And the div-soup trap (role=table/row/cell when you can't use
  native <table> — a last resort needing the FULL ARIA role set, easy to
  get wrong). Resolve: native <table> for tabular data; role=grid ONLY for
  the full interactive widget; never partial div-soup.
- THE COLUMN MODEL + THE HEADLESS-TABLE API (the architecture): columns-as-
  config (column definitions: accessor/key, header, cell renderer,
  sortable, width, align, pin) + rows-as-data; the HEADLESS table
  (TanStack Table — sorting/filtering/pagination/grouping/selection logic
  separated from markup, framework-agnostic) vs the batteries-included
  DataGrid (MUI X DataGrid, AG Grid). The cell renderer is where Tag/Badge/
  Avatar/Button/Menu compose. The server-side-vs-client-side data model
  (sort/filter/paginate on the server vs in the browser).
- SORTING + SELECTION (the two core interactions): SORTING — single + multi-
  column, the aria-sort attribute (ascending/descending/none) on the <th>,
  the sortable-header-IS-a-button pattern, the sort indicator + the sort
  announcement. SELECTION — the checkbox column (composes Checkbox), the
  header select-all + its INDETERMINATE state (the Checkbox brief's
  indeterminate), the single/multi selection model, aria-selected, the
  bulk-action bar that appears on selection.
- STICKY HEADERS / STICKY (FROZEN) COLUMNS + VIRTUALIZATION (the
  performance/scroll crux): position:sticky headers (header stays while body
  scrolls) + sticky first/row-header column + the frozen-column shadow + the
  header-body alignment problem; and VIRTUALIZATION (windowing 10k+ rows —
  TanStack Virtual/react-window) and ITS A11Y COST — virtualizing breaks the
  native <table>'s row structure, so aria-rowcount/aria-rowindex (+
  aria-colcount/colindex) must declare the TRUE total to AT, and focus
  management when rows unmount. Resolve the virtualization-vs-<table>-
  semantics tension.
- THE RESPONSIVE-TABLE PROBLEM (the hard layout problem, a framework-not-a-
  winner case): a wide table on a narrow screen — the approaches: horizontal
  SCROLL (safest, keeps the table + the role intact), the STACKED/CARD view
  (each row -> a Card, the th-scope-row label-value flip), the COLUMN-
  PRIORITY/hide-columns progressive disclosure. No clean winner; give the
  framework + the a11y cost of each (the stacked view loses the table
  semantics).
- STATES + DENSITY + CELL TYPES: the EMPTY/LOADING/ERROR states (composing
  Empty State + Skeleton rows — the terminal-states machine); density
  (comfortable/compact/condensed row height); cell types + alignment
  (numeric right-aligned + tabular-nums, text left, the row-actions Menu,
  the Tag/Badge/Avatar cell, the truncated-cell + Tooltip); the <caption>
  as the table's accessible name.

Field-leader systems to survey (web): TanStack Table + TanStack Virtual (the
headless table + virtualization — the dominant headless approach), MUI
(Table — compose-your-own — AND the X DataGrid — the enterprise interactive
grid: sorting/filtering/selection/virtualization/editing/Pro-Premium tiers),
AG Grid (the enterprise data-grid gold standard — virtualization/pivoting),
Ant Design (Table — sorting/filtering/selection/expandable/fixed-columns/
virtual), Shopify Polaris (DataTable + IndexTable — selectable/sortable, the
responsive), GitHub Primer (DataTable — the newer accessible table), IBM
Carbon (DataTable — sortable/selectable/expandable/batch-actions — a strong
a11y reference), Adobe Spectrum / React Aria (TableView — the gold-standard
accessible interactive table; the collection/selection model), Atlassian
(DynamicTable), Chakra UI (Table — the basic styled table), Base Web (Uber)
(Table/DataTable). WAI-ARIA APG (the Table pattern, the Grid pattern, the
Treegrid pattern, the sortable-table; <table> semantics — caption/th-scope;
aria-sort; aria-rowcount/rowindex for virtualization). Cite each with a
version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits:/composes for the Checkbox/Pagination/
Empty-State/Skeleton/Menu/Tag/Badge/Avatar cluster and the role=grid
boundary from Grid; note the List/Tree siblings; flag unverified/volatile
platform claims under notes.unverified).

1. Framing — what it is (the tabular-data display + the interactive data
   grid; the Data-category keystone + convergence point) and what it isn't
   (a CSS Grid layout — role=grid != display:grid; a List — 1D; a layout
   table — the dead anti-pattern); the data-table-vs-data-grid genre split +
   the <table>/role=grid/div-soup decision + the headless-vs-batteries-
   included architecture up front; why systems disagree.
2. Anatomy and parts — caption, thead/th(scope)/sortable-header-button,
   tbody/tr/td, the checkbox-selection column, the row-actions cell, the
   sticky header / frozen column, the pagination/toolbar, the empty/loading
   row regions; the column-def + row-data model.
3. Properties / API — the column model (columns def: accessor/header/cell/
   sortable/width/align/pin), the row data, sorting (single/multi), the
   selection model, pagination, sticky/pin, virtualization, density,
   server-vs-client; headless vs batteries-included.
4. States and variants — sortable/sorted columns; selected rows + select-all
   indeterminate; expandable rows (treegrid); loading (skeleton rows) /
   empty (empty state) / error; density (comfortable/compact); sticky /
   virtualized; the data-table vs data-grid variants.
5. Usage guidance — Table (tabular data) vs a List (1D records — when
   briefed) vs a Grid/Card-gallery (heterogeneous/visual) vs a description
   list; the data-table-vs-data-grid decision (reading vs application mode);
   when to virtualize; the don't-use-a-table-for-layout rule; the
   responsive approach choice.
6. Accessibility — the native <table> contract (caption = accessible name,
   th scope=col/row, the header associations), aria-sort on sortable
   headers, the interactive grid (role=grid/treegrid + roving tabindex/
   aria-activedescendant + arrow-key nav + one-tab-stop), selection
   (aria-selected + the select-all indeterminate), VIRTUALIZATION (aria-
   rowcount/rowindex/colcount/colindex for windowed rows), the responsive
   stacked-view semantics loss, WCAG SCs (1.3.1 info+relationships, 2.1.1
   keyboard, 4.1.2, 1.4.10 reflow, 2.4.7 focus).
7. Content guidelines — column headers (concise, the sort target), numeric
   alignment + tabular-nums, truncation + Tooltip, the empty-state copy, the
   caption, don't-overload-columns, the units/formatting.
8. Motion and transition — the sort reorder (FLIP/avoid), the row
   expand/collapse, the loading->content swap (skeleton), row
   insert/remove, reduce-motion; the don't-animate-large-tables rule.
9. Internationalization — RTL (the column order mirrors, numeric columns,
   logical properties inherited from Box); number/date/currency formatting
   via Intl; the column-header + caption translation; the
   variable-row-height from text expansion.
10. Naming — Table / DataTable / DataGrid / Grid / IndexTable / TableView;
    the data-table vs data-grid naming split; the practice's default
    (Table for the display table + DataGrid for the interactive widget?);
    aliases.
11. Implementation notes — native <table> + the CSS (display issues, the
    sticky header/column, the header-body alignment); the headless engine
    (column defs + the sort/filter/paginate/select state); virtualization +
    aria-rowindex; the select-all indeterminate wiring; the sortable-header
    button + aria-sort; the responsive transform (scroll/stack/hide); server
    vs client data; cell renderers compose the cluster; the DataGrid-as-a-
    product (MUI X / AG Grid) heaviness; headless vs opinionated.
12. Related and alternative components — typed relationships (COMPOSES
    Checkbox [selection + indeterminate] / Pagination / Empty State /
    Skeleton / Menu [row actions] / Tag/Badge/Avatar/Button/Link/Tooltip
    [cells]; the role=grid boundary from Grid; the List [1D] + Tree
    [treegrid] siblings; the responsive row->Card; the description-list
    alternative).
13. Field POV evolution — the layout-table anti-pattern -> tables-for-data;
    the headless-table turn (TanStack — logic/markup separation); the
    <table>-vs-role=grid clarification; virtualization + aria-rowindex; the
    responsive-table approaches (no clean winner); React-Aria/Spectrum
    raising the interactive-table a11y bar; the DataGrid-as-a-product (MUI X/
    AG Grid) heavyweight.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Table is — explain the
data-table-vs-data-grid genre split + the <table>/role=grid/div-soup
decision (the entire a11y model hinges on it), the column-model + headless-
vs-batteries-included architecture, sorting (aria-sort + the header button)
+ selection (the checkbox column + the select-all indeterminate), sticky
headers/frozen columns + virtualization (+ the aria-rowindex semantics
tension), the responsive-table problem (scroll/stack/hide — no clean
winner), and the composition convergence (Checkbox/Pagination/Empty-State/
Skeleton/Menu/Tag/Badge/Avatar) that makes Table the catalogue's keystone.

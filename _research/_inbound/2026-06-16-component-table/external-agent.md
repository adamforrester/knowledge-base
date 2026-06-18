# Table

## Framing
The Table component functions as the architectural keystone of the Data visualization and management category within mature design systems. It represents the catalog's most significant convergence point—the structural chassis where typography, interactive states, selection controls, pagination algorithms, overflow menus, and terminal-state containers seamlessly integrate into a unified interface. Because of its extreme density and structural complexity, the Table is universally recognized by design system practitioners as the most difficult component in the repository to build, maintain, and scale effectively.

To architect a robust Table component, the practice must first establish a critical genre split that dictates the entire technical, interactive, and accessibility model. The field diverges sharply between two distinct paradigms: the Data Table and the Interactive Data Grid.

The Data Table, or static table, is designed primarily for scanning, reading, and basic data comparison. It displays tabular data, supports pagination, and often allows basic column sorting or filtering. It may contain interactive elements within its individual cells—such as anchor links, action buttons, or status toggles—but it is not navigable as a singular, cohesive widget via the keyboard. Users navigate through a Data Table sequentially using the Tab key, moving linearly through focusable children. This pattern relies entirely on native HTML <table> semantics to communicate structural relationships to assistive technologies.

The Interactive Data Grid, conversely, is an application-mode widget built to mimic the behavior of a spreadsheet. It features omnidirectional arrow-key cell navigation, editable cells, draggable column resizing, row reordering, and complex keyboard selection models. In this paradigm, the entire grid acts as a single tab stop on the page. Once focus enters the grid, internal navigation is intercepted and managed via JavaScript. This pattern requires the explicit implementation of the WAI-ARIA role="grid" or role="treegrid" specifications, utilizing highly complex focus management techniques to maintain state.

A recurring implementation trap across the industry is architectural over-reach. Teams frequently attempt to apply Data Grid interactions and ARIA roles to simple Data Tables, creating severe accessibility barriers for screen reader users who expect standard document-reading behaviors. Furthermore, the reliance on "div-soup"—the practice of using generic <div> elements heavily laden with ARIA roles instead of native <table> elements to circumvent CSS styling limitations—represents a dangerous fallback. This is often confused with CSS Grid; however, CSS display: grid is strictly a presentational layout mechanism, whereas ARIA role="grid" defines an interactive widget pattern. The practice's opinionated default must be resolved clearly: utilize native <table> markup for all standard tabular data displays, reserving role="grid" strictly for complex, interactive spreadsheet-like applications. Partial div-soup implementations must be aggressively avoided unless absolute virtualization necessity forces the complete replication of the ARIA grid structure.

Architecturally, the field is further divided between two primary deployment strategies: the headless engine and the batteries-included component. Headless architectures, dominated by libraries like TanStack Table, separate all mathematical state logic (sorting, filtering, pagination, selection) from the visual markup, allowing the design system to retain total control over the Document Object Model (DOM) and styling layer. Alternatively, batteries-included grids, exemplified by MUI X DataGrid and AG Grid, ship highly opinionated DOM structures to support enterprise features like pivoting, aggregation, and virtualization out of the box, trading customization flexibility for out-of-the-box power.

## Anatomy and Parts
The physical anatomy of the Table reflects its role as a composition boundary, requiring precise orchestration of nested elements and semantic HTML regions. The outermost layer is the Table Container, a wrapping element responsible for managing horizontal overflow, border radii, and responsive scrolling contexts.

Within this container, the component breaks down into several distinct structural regions:

| Anatomical Region | Semantic Tag | Primary Function and Composition |
| --- | --- | --- |
| Caption | <caption> | A visually hidden or displayed title that serves as the accessible name for the entire table. It must be the first child of the <table> element. |
| Toolbar | <div> | A structural region sitting above the table, composing global controls such as global search inputs, density toggles, column-visibility menus, and the bulk-action bar that surfaces when rows are selected. |
| Table Head | <thead> | The container for column headers. Contains <tr> elements which in turn house <th> elements. |
| Column Header | <th> | Defines the column. In interactive tables, this cell composes the Sortable Header Button, displaying an ascending/descending indicator. The first column header frequently composes a Checkbox to manage the "select-all" interaction. |
| Table Body | <tbody> | The primary container for the data rows. Multiple <tbody> tags can be used to group related rows logically. |
| Table Row | <tr> | Represents a single data record. It may include an expandable trigger icon for hierarchical data, a selection Checkbox cell, standard data cells, and a terminal row actions Menu. |
| Table Cell | <td> | The atomic container for data. Cells act as the primary canvas for composed components, frequently housing Tags, Badges, Avatars, Buttons, Links, or truncated text paired with Tooltips. |
| Table Footer | <tfoot> | The bottom boundary of the table, often used for aggregation rows (e.g., totals, averages) or composing the Pagination component to manage data sets that exceed the viewport. |

Beyond the semantic tags, the anatomy encompasses specific layout features. Sticky or frozen columns are specialized anatomical regions created via CSS position: sticky. Because sticky elements often blend into the scrolling content beneath them, they utilize a pseudo-element or box-shadow to create a visual elevation shadow, indicating that the z-index hierarchy has changed.

Finally, the anatomy must account for terminal state regions. These are structural overlays or replacements that occupy the <tbody> area depending on the data lifecycle. This includes Skeleton rows for the initial loading state, the Empty State component when queries return zero results, and localized error boundaries when data fetching fails.

## Properties and API
The foundation of modern Table architecture relies on the "columns-as-config" and "rows-as-data" API model. Rather than forcing developers to pass raw JSX elements as children—which makes sorting and filtering mathematically impossible without parsing the DOM—developers pass strictly typed configuration objects that dictate how underlying data should be mapped and rendered.

### The Column Model
The column definition array acts as the central nervous system of the API. Each column configuration object dictates both the behavior and the presentation of a specific data field. A mature column definition API accepts several key properties:
- Accessor / Key: The string or function mapping the column to the specific key in the underlying row data object.
- Header: The string, function, or React node to render within the <th> element.
- Cell Renderer: A functional component or render prop returning the formatted UI for the <td>. This is the exact injection point where atomic components like Tags, Badges, and Avatars are instantiated.
- Sortable / Filterable: Boolean flags enabling or disabling column-specific logic.
- Width and Alignment: Layout directives determining if a column behaves dynamically, aligns to the right (for tabular numeric data), or adheres to a fixed width constraint.
- Pinning: Directives indicating whether the column should be frozen to the left or right edge of the scroll container.

### Headless versus Batteries-Included Architecture
The API design is heavily influenced by the chosen architectural paradigm. Headless engines, such as TanStack Table, provide maximum design system flexibility by entirely separating the algorithmic logic from the visual rendering. In its V9 architecture (released mid-2026), TanStack Table revolutionized this model by introducing the TFeatures generic. Previous versions baked all possible features (sorting, grouping, filtering) into a single monolithic type, causing severe TypeScript compilation overhead. By making features modular, TanStack V9 reduced type instantiation counts from over 1.1 million down to roughly 158,000, improving type-checking performance by up to 86%. The resulting API outputs raw state and mathematical functions (e.g., row.getVisibleCells()), leaving the design system entirely responsible for wiring these outputs to the semantic DOM.

Conversely, batteries-included data grids, such as MUI X DataGrid and AG Grid, expose massive, highly opinionated property surfaces on a single root component (e.g., paginationMode, disableColumnMenu, checkboxSelection). These systems provide immense out-of-the-box functionality, including Excel exporting, complex cell editors, and integrated charting, but they dictate the underlying DOM structure. This approach often results in heavier bundle sizes—sometimes exceeding 100KB gzipped—and requires the design system to fight against the grid's internal CSS architecture to achieve brand alignment.

### Server-Side versus Client-Side Data Modeling
The API must elegantly handle data locality. In client-side modes, the table ingests the entire dataset upfront, executing all sorting, filtering, and pagination algorithms directly within the browser's memory. This offers instantaneous interactions but scales poorly beyond a few thousand rows.

In server-side modes, the table functions strictly as a presentation and interaction layer. It relies on callback functions (e.g., onSortChange, onPaginationChange) to emit state updates to the host application, which then refetches windowed slices of data from the backend. A robust design system API must seamlessly transition between these two modes without requiring the developer to alter the visual component implementation.

## States and Variants
The Table component manages an intricate matrix of states, operating simultaneously at the macro (table-wide) and micro (row/cell) levels. Managing the intersection of these states ensures a predictable user experience.

### The Terminal-States Machine
The macro state of the table relies on a terminal-states machine encompassing four sequential phases:
- Loading: The initial data-fetching state. Rather than a global spinner, modern tables compose Skeleton rows. To prevent layout thrashing and Cumulative Layout Shift (CLS), these skeleton rows must exactly mirror the anticipated row height and column widths of the impending data.
- Content: The populated, interactive data state.
- Empty: The zero-data state. This replaces the <tbody> with an Empty State component. The visual presentation must clearly differentiate between an inherently empty dataset (e.g., a new account with no records) and a dataset that yields no results due to aggressive filtering.
- Error: A disruptive state indicating a network failure or logic exception, typically providing a localized action to retry the data fetch.

### Density and Scale Variants
Design systems universally converge on providing density variants to accommodate varying contextual requirements and user preferences.
- Comfortable (Default): Features generous padding (e.g., 16px vertical padding, 48px to 56px row height) optimized for optimal readability, standard text wrapping, and accessible touch targets on hybrid devices.
- Compact / Condensed: Features drastically reduced padding (e.g., 4px to 8px vertical padding, 32px row height). This variant is specifically designed for high-density, analytical applications where power users must parse maximum information density without excessive scrolling.

### Micro-States: Rows, Cells, and Headers
At the micro-level, rows exhibit specific interaction states: Hover, Focus (when operating in a grid model), Selected (typically highlighted with a subtle primary-color background), and Disabled (where interactions and selection are explicitly blocked). Advanced enterprise systems, such as IBM Carbon, have introduced "AI Presence" states. When rows or individual cells are generated by artificial intelligence, they are styled with specific linear gradients and inner shadows to visually disclose the AI's intervention to the user, maintaining trust and transparency.

Header cells manifest distinct sorting states—unsorted, ascending, and descending. Interaction with a sortable header must visually flip the sort indicator icon and programmatically update the underlying accessibility attributes without jarring the user's visual tracking.

## Usage Guidance
Deploying a Table correctly requires strict adherence to usability guidelines, which often means knowing when to utilize alternative patterns.

The fundamental rule of modern web development is that native <table> elements must never be used to construct page layouts. This archaic practice fundamentally breaks the logical reading order for screen readers and violates core web standards.

When deciding between a Table and a List, the dimensionality of the data is the deciding factor. If the dataset consists of single-dimensional records—such as a simple directory of user names without secondary comparative attributes—the 1D List component is the appropriate choice. Tables must be reserved exclusively for two-dimensional data where cross-referencing values across columns is necessary for analysis.

Similarly, if the dataset is highly heterogeneous, heavily visual (e.g., product thumbnails with varying metadata lengths), or unstructured, a Card gallery mapped to a CSS Grid layout should be utilized instead of forcing the content into rigid table cells.

The most critical usage decision a practitioner must make is the choice between the Data Table and the Data Grid. The design system must enforce strict guidance here: default to the standard Data Table for the vast majority of use cases involving reading, selecting, and navigating to detailed views. Escalate to an Interactive Data Grid only when building a highly interactive, focus-managed application where users are expected to edit data inline as rapidly as they would in a native spreadsheet application.

## Accessibility
Accessibility within the Table component represents the most contested, technically demanding, and structurally complex terrain in design systems. The entire interaction model hinges entirely on the divergence between native document semantics and ARIA application patterns.

### The Native <table> Contract
For a standard Data Table, the accessibility model relies implicitly on native HTML. The <caption> element serves as the accessible name for the table, ensuring that screen readers announce the table's purpose and context before the user begins navigating its contents. The complex associations between header columns and data cells are managed natively by the browser using the scope="col" and scope="row" attributes on <th> elements. In this reading mode, users navigate utilizing their screen reader's standard virtual cursor, moving linearly cell by cell.

When a column is sortable, the header content must be wrapped in a <button> element to make it focusable via the keyboard. The parent <th> element must then receive the aria-sort attribute, which toggles dynamically between ascending, descending, and none. When a sorting action occurs, an ARIA live region (typically configured with aria-live="polite") should announce the new sort order or updated pagination state. This informs non-visual users of the DOM mutation without forcefully stealing their focus or interrupting their current task.

### The Interactive Grid (role="grid")
If the component is escalated to an interactive Data Grid, the accessible contract changes fundamentally. The native table semantics are overridden by application semantics. The container requires role="grid" (or role="treegrid" for hierarchical data), rows require role="row", and cells require role="gridcell" or role="columnheader".

Crucially, the grid acts as a single tab stop on the page. Once focus enters the grid, native Tab key navigation is suppressed, and keyboard navigation is intercepted and managed manually via JavaScript. Two established patterns govern this focus management:

| Focus Management Strategy | Mechanism of Action | Ideal Use Case |
| --- | --- | --- |
| Roving tabindex | The currently focused cell receives tabindex="0", while all other cells are set to tabindex="-1". JavaScript updates these attributes on arrow-key presses and calls element.focus() on the new target. | Preferred when grid cells contain interactive child elements (like text inputs, checkboxes, or action buttons) that require their own focus handling. |
| aria-activedescendant | DOM focus remains on the grid container element itself. The aria-activedescendant attribute is dynamically updated to point to the ID of the currently active "virtual" cell, while styling simulates visual focus. | Useful for highly virtualized or readonly grids where moving actual DOM focus is computationally expensive or unnecessary. |

### The Semantic Cost of Virtualization
Virtualization (or windowing) solves performance bottlenecks by removing DOM nodes that scroll out of the viewport, but it severely degrades the native accessibility of tables. Because the browser and the accessibility tree only perceive the nodes currently rendered in the DOM, a screen reader interpreting a 10,000-row virtualized table might erroneously announce "Table, 15 rows".

To mitigate this semantic destruction, developers must explicitly map the true dimensions of the dataset to the accessibility tree. This requires injecting aria-rowcount (the true total number of rows), aria-colcount (total columns), aria-rowindex (the absolute index of the currently rendered row relative to the total dataset), and aria-colindex onto the respective elements.

However, explicitly applying these ARIA roles to elements within a native <table> structure can trigger HTML validation violations and cause unpredictable side effects in specific screen reader software. Consequently, highly virtualized data grids are frequently forced to abandon native <table> tags entirely, relying on <div> elements mapped comprehensively with the ARIA grid specification to satisfy WCAG Success Criteria (SC 1.3.1 Info and Relationships, and SC 4.1.2 Name, Role, Value).

## Content Guidelines
The effectiveness of a Table is predicated heavily on the visual clarity of its content parsing and typographic discipline.

Column headers must be exceptionally concise. Because headers serve as the interactive target for sorting and filtering actions, excessively long headers create awkward touch targets, force unnecessary text wrapping, and generate visual clutter that inhibits vertical scanning.

Alignment rules must be strictly enforced. Alphabetic text should universally align to the left (or to the right in RTL languages). However, numeric data, financial figures, percentages, and dates must be strictly right-aligned. This allows users to accurately scan decimal places and compare magnitudes vertically. Furthermore, numeric data columns should utilize the CSS property font-variant-numeric: tabular-nums to ensure all digits occupy the exact same monospace width, preventing jagged, unreadable vertical columns.

Design systems must offer standardized strategies for handling overflowing data. The preferred default is single-line text truncation (text-overflow: ellipsis; white-space: nowrap;) paired with a composed Tooltip component to reveal the full content upon hover or keyboard focus. Multi-line wrapping is technically supported but drastically impacts vertical density, disrupts zebra-striping rhythms, and significantly complicates the mathematics required for row virtualization.

Within the Empty State component, microcopy must clearly explain why the table is empty (e.g., "No transactions found for the selected date range") and provide a clear, actionable recovery path (e.g., "Clear all filters").

## Motion and Transition
Due to the sheer volume of DOM nodes present in a heavily populated Table, motion must be applied with extreme conservatism to maintain a 60fps performance baseline.

While it is tempting for designers to utilize FLIP (First, Last, Invert, Play) animations to physically slide rows into new positions when a user triggers a sort action, this approach causes severe layout thrashing and painting bottlenecks on large datasets. Row reordering should generally be instantaneous.

The leading performance trend, adopted by systems like React Aria and HeroUI in their latest major releases, involves stripping out heavy JavaScript animation runtimes (such as Framer Motion) in favor of native CSS transitions for simple row expansion and hover states. This drastically reduces main-thread blocking and leverages GPU acceleration.

When transitioning from the Loading state to the Content state, the swap should utilize a seamless cross-fade. This avoids jarring layout shifts, provided the system enforces strict geometric parity between the Skeleton rows and the incoming data rows. All animations must respect the user's OS-level preferences via the prefers-reduced-motion media query.

## Internationalization
Tables must inherently support internationalization (i18n) through logical CSS properties and native browser formatting APIs.

In Right-to-Left (RTL) languages, the entire column order must mirror automatically. This is achieved natively by the browser if the table utilizes standard <table> markup or if the system relies on logical CSS properties (margin-inline-start instead of margin-left). Numeric columns may retain their specific LTR formatting rules depending on the locale, but the column itself should align to the starting edge of the RTL layout.

The cell renderers must utilize the Intl.NumberFormat and Intl.DateTimeFormat APIs to ensure currencies, decimals, and dates conform precisely to the user's localized locale, avoiding brittle, hardcoded string manipulations.

Text expansion poses a significant layout challenge. Translations into languages like German or Russian frequently require 30-50% more horizontal space than their English equivalents. The column layout algorithms—such as minmax() functions in CSS Grid layouts or TanStack's growCollapse sizing strategies—must dynamically adapt to this text expansion without breaking the UI or forcing unwanted horizontal scrolling on isolated columns.

## Naming
The field exhibits a notable schism in component nomenclature, directly reflecting the structural divergence between native tables and interactive widgets. Standardizing this taxonomy is crucial for developer experience.

| Component Name | Industry Usage and Rationale | Examples |
| --- | --- | --- |
| Table | The standard name for a basic, presentational tabular data display. | Chakra UI, Base Web, Ant Design. |
| DataTable | Used to denote a table equipped with built-in sorting and pagination capabilities, but which still operates conceptually in reading mode. | Primer React, Carbon Design System. |
| DataGrid / Grid | Reserved specifically for the highly interactive, focus-managed, spreadsheet-like widget. | MUI X DataGrid, AG Grid. |
| IndexTable | A specialized nomenclature utilized to differentiate a table built for viewing and selecting a homogenous collection of objects (e.g., an index of Orders) from a generic data display. | Shopify Polaris. |

The practice's default should enforce strict semantic naming: Table or DataTable for native, reading-mode data displays, and DataGrid exclusively for the complex, focus-managed interactive widget.

## Implementation Notes
Tables contain several notorious implementation traps that consistently recur across codebases.

### The Sticky Header Alignment Problem
Implementing position: sticky on the <thead> allows column headers to remain visible while the <tbody> scrolls vertically. However, because table borders in CSS are prone to sub-pixel rendering discrepancies across different browsers, a common bug occurs where a transparent 1px gap appears between the sticky header and the scrolling rows beneath it, causing data text to "bleed" through the gap. Implementing a solid background color on the <th> and utilizing a strategically placed pseudo-element or box-shadow is required to cover this sub-pixel gap and maintain visual integrity.

### The Select-All Indeterminate Wiring
The Checkbox component situated in the primary column header allows users to select or deselect all currently visible rows. When a user selects some, but not all, rows, the header Checkbox must enter an "indeterminate" state. Because standard HTML does not possess an indeterminate attribute that can be set declaratively, this state can only be applied via JavaScript by manipulating the DOM element directly (input.indeterminate = true). The implementation must expose a ref to the Checkbox component to allow the Table's internal logic to govern this imperative state update.

### Virtualization Overhead
When implementing virtualized rows via libraries like TanStack Virtual, fixed-height rows calculate efficiently, offering O(1) random access. However, variable-height rows—often necessitated by multi-line text cells—require the virtualizer to maintain complex prefix sum arrays, leading to O(log n) lookup times during scroll events. Furthermore, rapid scrolling causes rapid mounting and unmounting of React components; developers must rigorously employ React.memo on row and cell renderers to prevent garbage collection sweeps from stalling the main thread.

### Responsive Layout Transforms
Handling wide tables on narrow mobile screens yields no perfect solutions; frameworks must choose their compromises:
- Horizontal Scroll: Wrapping the table in a container with overflow-x: auto. This is visually cumbersome but preserves the structural integrity of the <table> and its ARIA semantics.
- Stacked / Card View: Using CSS media queries to change tr { display: block; } and td { display: block; }, essentially turning each row into a Card. The <th> headers are hidden, and their labels are injected into the <td> using pseudo-elements (content: attr(data-label)). This approach looks excellent on mobile but completely destroys the table's semantic reading logic for assistive technologies, as the native table associations are broken.
- Column Priority Hide: Progressively hiding less critical columns as the viewport shrinks. This preserves semantics but risks hiding vital data from mobile users.

Horizontal scrolling remains the most robust, accessible, and opinionated default for enterprise systems.

## Related and Alternative Components
The Table component does not exist in isolation; it sits atop a complex network of composed elements and borders several structural siblings:
- Composed Cluster: The Table acts as the macro-container orchestration layer for the Checkbox (selection and indeterminate states), Pagination (navigation), Empty State and Skeleton (terminal states), Menu (row actions), and atomic data cells (Tags, Badges, Avatars, Buttons, Tooltips).
- List: The simpler, one-dimensional sibling. Use the List component when the data lacks comparable columns or is highly heterogenous.
- Tree: The hierarchical sibling. When a Table incorporates collapsible nested rows, it crosses into the treegrid pattern, inheriting complex parent-child keyboard navigation semantics.
- Card Gallery: The alternative layout for highly visual or heterogeneous datasets, typically deployed when the responsive "Stacked Card" table transform becomes the primary viewing mode.

## Field POV Evolution
Historically, the web relied heavily on <table> elements for general page layout—a disastrous anti-pattern that the industry spent a decade unwinding. Once tables were relegated strictly to tabular data, the field struggled with performance bottlenecks when rendering thousands of DOM nodes in modern Single Page Application (SPA) frameworks like React and Angular.

The initial response was the rise of the "Batteries-Included" heavy grid (such as AG Grid and early iterations of MUI DataGrid). These tools solved performance issues through aggressive internal virtualization and state management but resulted in massive bundle sizes, rigid APIs, and visual inflexibility.

The modern evolution, pioneered heavily by TanStack Table, is the "Headless" turn. By separating the mathematical sorting, filtering, and selection state machines from the markup, headless engines allow design systems to maintain pristine control over accessibility, CSS, and DOM structures without reinventing complex data algorithms.

Concurrently, accessibility standards have radically improved. This shift has been driven by libraries like Adobe's React Aria, which explicitly clarified the distinction between the passive reading <table> and the heavily engineered, focus-managed role="grid", providing low-level hooks to ensure teams deploy the correct keyboard contract without compromising custom visual design. The current consensus dictates a hybrid approach: leverage headless engines for standard design system tables to ensure visual and semantic purity, while reserving heavy, commercial data grids strictly for specialized, high-density spreadsheet use cases.

## Field Survey and Version Landscape
An analysis of the leading design systems and tools in 2026 reveals a mature, highly segmented approach to tabular data management.

At the forefront of the headless movement, TanStack Table (v9, June 2026) represents the dominant architectural choice for systems building custom tables. Its transition to modular TFeatures and TanStack Store atoms drastically reduced TypeScript instantiation overhead while preserving complete markup independence. It pairs tightly with TanStack Virtual for complex windowing tasks.

In the enterprise widget space, MUI X DataGrid (v9, April 2026) and AG Grid (v35, May 2026) remain the gold standards. Both frameworks recently expanded their heavy-duty offerings. MUI X v9 stabilized its in-grid Charts integration and introduced an AI Assistant capable of manipulating data views via natural language, alongside sophisticated server-side pagination and edit modes. AG Grid continues to dominate in performance for high-frequency financial data, refining its roving tabindex keyboard navigation and virtualization architectures.

Shopify Polaris (v2026-04) illustrates a distinct semantic approach by splitting its offering into a DataTable (for statistical comparison) and an IndexTable (optimized for bulk selection and actions on homogeneous lists like products or orders). Polaris recently completed a massive migration of these components from React-specific implementations to framework-agnostic web components (s-table), emphasizing cross-platform consistency.

IBM Carbon (v11 / React v1.110.0) serves as the industry's strongest accessibility reference for tabular data, standardizing complex batch-action architectures and pioneering "AI Presence" visual states (using gradients and shadows) to indicate when table cells are generated by artificial intelligence. Similarly, GitHub Primer (React v38.24.0, May 2026) provides an exceptional reference for applying aria-sort and ARIA live regions correctly within a standard, non-grid DataTable.

Finally, React Aria / Adobe Spectrum (v3.49.0, 2024-2026) continues to raise the bar for interactive grid accessibility. Their useTable and useGridList hooks elegantly handle the mathematically complex aria-rowindex injection required for virtualized rows, and effectively manage the complex roving tabindex required for WCAG-compliant spreadsheet interactions.

## Agent-Consumable Schema
```yaml
identity:
  name: Table
  aliases: [DataTable, DataGrid, IndexTable, Grid]
  category: Data Display
  role: Keystone tabular data container; boundaries depend on reading vs. application mode.
description: |
  A component for displaying and managing two-dimensional tabular data. Represents the largest composition point in the system. Splits into two sub-genres: the static Data Table (reading mode, native table markup) and the Interactive Data Grid (application mode, role=grid, roving tabindex).
anatomy:
  - Table Container (overflow scroll manager)
  - Toolbar (search, density, bulk actions)
  - thead > tr > th (sortable header button, select-all checkbox)
  - tbody > tr > td (data cells, row selection checkbox, row actions menu)
  - tfoot / Pagination controls
  - Terminal States (Skeleton overlay, Empty State container)
api:
  architecture: |
    Favors "columns-as-config" (accessor, header, cellRenderer, sortable, width, pin) and "rows-as-data".
  data_locality: Supports client-side (internal sorting/pagination) and server-side (callback-driven windowing).
  core_props:
    - columns (array of column definitions)
    - data (array of row objects)
    - selectionMode (single, multi, none)
    - sortModel (controlled sorting state)
    - pagination (offset, limit)
states:
  macro_states: [Loading (Skeleton), Content, Empty (Empty State), Error]
  density: [Comfortable (default), Compact/Condensed]
  row_states: [Hover, Focus, Selected, Disabled, AI-Generated]
  header_states: [Unsorted, Ascending, Descending]
accessibility:
  genre_split: |
    - Data Table: Uses native <table>, <caption>, <thead>, <th scope>. Navigated via standard Tab sequence.
    - Data Grid: Uses role="grid". Acts as a single tab stop. Arrow-key navigation via roving tabindex or aria-activedescendant.
  attributes:
    - aria-sort on sorted column headers (ascending/descending/none).
    - aria-live="polite" for sorting announcements.
  virtualization_cost: |
    If DOM nodes are removed for performance, aria-rowcount, aria-colcount, aria-rowindex, and aria-colindex MUST be applied to map the true dataset size to screen readers.
content:
  alignment: Text left; numeric/financial data right-aligned with tabular-nums.
  truncation: Single-line truncation with Tooltip preferred over multi-line wrapping for vertical density preservation.
motion:
  transitions: CSS transitions preferred for row expansion/hover.
  restrictions: Avoid FLIP animations on large table sorting to prevent main-thread layout thrashing.
  state_swaps: Cross-fade Skeleton to Content.
i18n:
  rtl: Mirror column order logically. Numeric formats align to start edge.
  formatting: Use Intl.NumberFormat and Intl.DateTimeFormat.
  expansion: Column sizing must accommodate 30-50% text expansion in languages like German/Russian.
implementation:
  - headless_vs_monolith: Prefer headless engines (TanStack) for UI flexibility; reserve monoliths (AG Grid, MUI X) for enterprise spreadsheet use-cases.
  - sticky_headers: Requires position: sticky and background colors/pseudo-elements to mask sub-pixel rendering gaps.
  - indeterminate_checkbox: Must be set via JavaScript ref (input.indeterminate = true), not HTML attribute.
  - responsive: Horizontal scroll is the most semantically stable fallback. Stacked Card views break screen reader table contexts.
composition:
  inherits: [Checkbox, Pagination, Empty State, Skeleton, Menu, Tooltip]
  cell_composition: [Tag, Badge, Avatar, Button, Link]
notes:
  - Do not use tables for page layout.
  - Avoid partial "div-soup" implementations; either use native <table> or fully conformant ARIA role="grid" structures.
  unverified: |
    Impact of React 19 / concurrent mode on highly virtualized grid re-renders.
```

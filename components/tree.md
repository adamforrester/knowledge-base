---
okf_version: "0.1"
type: component-brief
title: Tree
description: The hierarchical sibling that closes the Data category — a field-truth study of the role=tree-vs-treegrid-vs-disclosure-nav decision (the over-reach trap), the full APG tree keyboard model (Up/Down visible nodes, Right/Left expand-collapse-into-out, *, typeahead), the aria-level/setsize/posinset + the virtualization-forces-flattening tension, the tri-state cascading checkbox tree (aria-checked=mixed on the treeitem, the checkbox presentational; the two-pass up-and-down propagation), the lazy-load-on-expand + node anatomy, and the RTL Right/Left key-swap trap — inheriting the Accordion disclosure model recursively, being List + expand/collapse, resolving Table's treegrid, composing Icon/Checkbox/Empty-State/Skeleton, with the practice's defaults.
tags: [components, data]
category: Data
status: stable
aliases: [TreeView, TreeViewItem, TreeGrid, DirectoryTree, RichTreeView, SimpleTreeView, FileTree]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Tree

> A Tree (TreeView) is the **hierarchical data widget** — the user expands/collapses, arrow-navigates, and selects/operates on a nested hierarchy. It is the third and final Data brief and **closes the Data category**, completing the triad: **Table** (2D matrix), **List** (1D sequence), **Tree** (hierarchical). It inherits the most prior work in the catalogue: it *is* **List** + expand/collapse (the node is a List item + indentation + a disclosure twisty), it applies the **Accordion** disclosure model recursively, and it resolves **Table's `treegrid`** (a tree with columns). The headline that decides the accessibility model — the over-reach trap parallel to Table's `role=grid`, Menu's `role=menu`, and List's listbox-vs-gridlist — is the **`role=tree` vs `role=treegrid` vs disclosure-nav decision**: `role=tree` is for a *data-tree widget* (select/move/check/browse a hierarchy — a file browser, a permissions picker, a layers panel; the APG Tree pattern, a single tab stop with arrow-key traversal); `role=treegrid` is a tree *with columns* (the hierarchical Table row); and a *navigation* hierarchy (a docs sidebar, an app nav) is **disclosure** (`<nav>` + nested `<ul>` + `button aria-expanded`), **never `role=tree`**. The rule (from Side Navigation): **`role=tree` only for data-tree widgets** — a nav that *looks* like a tree is still nav, and imposing `role=tree` on it breaks standard page-navigation a11y (it forces an unexpected application key-interception mode). What it *isn't*: a **nav hierarchy** (disclosure / Side Navigation — see side-navigation), an **Accordion** (a *flat* set of independent disclosure panels — not a nested arrow-navigable widget — see accordion), or a **Menu** (commands — see menu). Why systems disagree: the role=tree-vs-disclosure over-reach, the tri-state checkbox cascade, and the virtualization-vs-hierarchy tension.

---

## 1. Framing
Of all components, the Tree carries the most architectural debt and is the most prone to structural over-reach and accessibility failure. The core tension is the **misapplication of `role="tree"` to website hierarchies, docs sidebars, and app menus** — conflating *navigation* with *data interaction*:
- **The disclosure-navigation model** — if the user is *navigating* (clicking changes the URL / renders a page): a **Side Navigation** built from nested `<ul>`/`<li>` + semantic `<a>` + `button aria-expanded` disclosure. Every link is a tab stop; standard browser tab-key site discovery works. **No `role=tree`, no `treeitem`, no tree arrow-key handling** (see side-navigation).
- **The `role="tree"` data-widget model** — if the user is *selecting/checking/dragging/operating* on a hierarchy within an app (a file directory, a permissions picker, a category manager): a **data tree widget** — `role="tree"`, a single focusable tab stop, roving tabindex / `aria-activedescendant`, complex directional keyboard traversal.

Three conceptual pillars define the widget:
- **The APG keyboard model** — "widget mode": the tree captures arrow keys to expand/collapse/traverse *visible* nodes, exposing **one tab stop** to the document (§6).
- **The tri-state cascading checkbox tree** — child selections propagate *up* to set parents checked/unchecked/**indeterminate**, and a parent's check cascades *down* — synchronized bottom-up and top-down passes (§6/§11).
- **The virtualization-vs-hierarchy tension** — high-performance trees **flatten** the nested structure into a linear array of *visible* nodes for DOM virtualization, which destroys the natural DOM nesting and forces AT to rely *entirely* on programmatic `aria-level`/`aria-setsize`/`aria-posinset` on every node (§6).

What it *isn't*: a nav hierarchy (disclosure — see side-navigation), an Accordion (a flat disclosure set — see accordion), a Menu (commands — see menu). Why systems disagree: the over-reach, the cascade, and the flattening tension.

## 2. Anatomy and parts
The DOM differs sharply between non-virtualized (true nesting) and virtualized (flattened siblings) — but the ARIA model is identical.
- **the tree container** — `role="tree"` (single-column widget) or `role="treegrid"` (with columns); owns the global model (`aria-multiselectable`) and is the **single interactive tab stop**.
- **the group container** (`role="group"`) — in non-virtualized markup, wraps an expanded parent's children, communicating nesting transitions to AT. (Stripped in the flattened/virtualized DOM — the hierarchy then lives in the ARIA attributes — §6.)
- **the tree node** (`role="treeitem"`) — the focal element; a List item + hierarchy chrome:
  - **the indentation / guide-line region** — an inline-start channel scaling with `aria-level` (often with vertical guide lines).
  - **the expand/collapse twisty** — a chevron disclosure toggle on parent nodes (rotates 90° on expand); the `aria-expanded` carrier (the Accordion disclosure per node — see accordion). Leaves have none.
  - **the leading Icon** — a folder (parent) / file (leaf) icon (see icon).
  - **the (tri-state) Checkbox** — for a checkbox-tree; **presentational** (`aria-hidden`) — the *treeitem* carries the selection state (§6; see checkbox).
  - **the label** — the node text (the accessible name).
  - **the trailing actions / badges** — an overflow Menu, a count Badge (on hover/focus).
- **the loading / empty regions** — a lazy-loading node renders a Skeleton/spinner child with **`aria-busy="true"`** on the parent; an empty tree uses Empty State (see skeleton, empty-state).
- **the flattened-visible model** (not visual) — the visible (expanded) nodes flatten to an absolute-positioned list for virtualization; `aria-level`/`setsize`/`posinset` preserve the hierarchy (§6/§11).

## 3. Properties / API
The API separates the raw hierarchical data from the navigation/selection/virtualization state. The recommendation: a **normalized flat-map** internally (even if the consumer passes nested JSON) for O(1) lookups and mutation:
```ts
interface TreeNode { id: string; label: string; children?: string[]; isBranch?: boolean; icon?: ReactNode; isDisabled?: boolean; value?: unknown }
type TreeDataMap = Record<string, TreeNode>   // child references, not nesting
```
- **`data`** — nested or flattened nodes.
- **`expandedKeys` / `defaultExpandedKeys`** (controlled/uncontrolled) + `onNodeExpand`/`onNodeCollapse`; `expandAll`/`collapseAll`.
- **`selectionMode`** — none / single / multiple; `selectedKeys` + `onSelectionChange`; `selectionBehavior` (toggle/replace).
- **`checkboxMode`** — none / **cascade** (the tri-state up-and-down propagation) / independent (no cascade).
- **`loadOnExpand(nodeId): Promise`** — async lazy-load children + the loading node state.
- **`role` / kind** — `tree` (single-column) / `treegrid` (with columns — a Table mode).
- **the node renderer** — icon/label/actions (where Icon/Checkbox/Badge/Menu compose); the leaf-vs-branch distinction (`isBranch` forces branch behavior even with empty children — for lazy nodes).
- **`virtualize`** — windowing the flattened visible nodes (+ `aria-level`/`setsize`/`posinset`).
- **`dragAndDrop`** — drag-to-reparent + the keyboard alternative (§11) — the hardest reorder.
- **`density`** — compact (24–28px) / comfortable (32–40px); the per-level indentation.
- **what it withholds** — Tree is the *widget*; a nav hierarchy uses disclosure markup, not this.

## 4. States and variants
- **Node states:** **expanded** (`aria-expanded=true`) / **collapsed** (`aria-expanded=false`) / **leaf** (no twisty, *no* `aria-expanded`); **focused** (roving — only the active node has the focus outline / `tabindex=0`; with `aria-activedescendant` the container owns focus and the node is styled `is-active`); **selected** (`aria-selected`); **loading** (lazy children — `aria-busy=true` + a spinner/Skeleton); **disabled** (disables the node *and its descendants*).
- **The checkbox propagation states:** **checked** (all descendants checked) / **unchecked** (none) / **indeterminate** (some — the Checkbox tri-state).
- **Variants:**
  - **checkbox tree** — multiselect with the cascade (selecting a node toggles its descendants + updates the ancestor indeterminate chain).
  - **directory tree (file-explorer mode)** — click-anywhere-on-the-row toggles *expansion* (Finder/VS Code), with a twin-selection model (single-click highlights, double-click executes).
  - **treegrid** — a tree *with columns* (financial sheets, file details: name/size/modified): two-axis navigation — *row mode* (Left/Right collapse/expand) and *grid mode* (Left/Right cell navigation).
  - **density:** compact (24–28px, asset managers / layers panels) / comfortable (32–40px, permissions/category trees).
  - **lazy** (load-on-expand) vs eager; **with guide-lines** vs indentation-only.

## 5. Usage guidance
The component-selector decision (by core task):
- **Page navigation** ("go to /path", a docs sidebar, an app nav) → **Side Navigation** (nested `<ul>` + `<a>` + disclosure; **no tree roles**). Using `role=tree` here breaks tab-key site discovery and forces an unexpected key-interception mode (see side-navigation).
- **Read-only hierarchical content** → a nested **List** (semantic nested `<ul>` — see list).
- **Data manipulation** (select, reorder, check, browse a hierarchy) → the **Tree widget** (`role=tree`, single focus).
- **Independent disclosure panels** (a flat set, not a hierarchy) → an **Accordion** (see accordion); don't nest Accordions >2 levels for hierarchy — use a Tree.
- **A parent-child hierarchy needing metadata columns** (sort/filter/evaluate by size/owner/status) → a **`treegrid`** (a tree with columns — see table), not a `role=tree`.
- **Commands** → a **Menu** (see menu).
- **When to virtualize** — >~150–200 simultaneous nodes (rendering hundreds of nested DOM elements degrades scroll/toggle performance); flatten + window (§6/§11).
- **Don't over-nest** — cap practical depth at ~4–5 levels; deeper nesting squashes horizontal space and creates layout fatigue on narrow viewports.

## 6. Accessibility
Tree is **one of the most complex accessibility challenges in component engineering** — and the genre (tree vs treegrid vs disclosure-nav) decides the model (§1).

- **The ARIA role taxonomy** — `role="tree"` (the root, with `aria-label`/`labelledby`) > `role="treeitem"` (every interactive node — branch *and* leaf; **focus styles target the `treeitem`, not nested wrappers**) > `role="group"` (a child-node container, declaring nesting transitions). Each `treeitem` exposes four structural properties:
  - **`aria-expanded`** (true/false on branches; **absent on leaves** — adding it to a leaf tricks AT into announcing an empty branch),
  - **`aria-level`** (1-based depth, scaling sequentially),
  - **`aria-setsize`** (sibling count at this level/group),
  - **`aria-posinset`** (1-based position among siblings).
- **The APG keyboard model (the full contract — a single-tab-stop widget; only the active node has `tabindex=0`, others `-1`, or use `aria-activedescendant`):**
  - **Down/Up** — next/previous *visible* node (the flattened expanded list; skips collapsed-away nodes).
  - **Right** — collapsed parent → **expand** (focus stays); expanded parent → **first child**; leaf → nothing.
  - **Left** — expanded parent → **collapse** (focus stays); collapsed node / leaf → **parent**.
  - **Home/End** — first/last visible node; **typeahead** — next visible node matching typed chars; **`*`** — expand all sibling branches at the level; **Enter/Space** — activate/select.
  - **(RTL: Right and Left swap — §9.)**
- **The treegrid** — `role="treegrid"` + `role="row"`/`role="gridcell"`; two-axis nav (Up/Down rows, Left/Right cells, with Left/Right *also* collapsing/expanding at the row's first cell) — the tree model crossed with the grid (the Table interlock — see table).
- **The checkbox-tree (the sharp a11y resolution)** — **don't put the selection role on the checkbox element**; the visual checkbox is **presentational (`aria-hidden`)** inside the node, and the **`role="treeitem"` carries `aria-checked="true|false|mixed"`** (`mixed` = the indeterminate parent — the Checkbox tri-state; see checkbox). Checking a node **cascades down** to descendants and the parent's state **derives up** from its children (§11).
- **Virtualization — the flattened-tree paradox.** Windowing replaces nested elements with a flat list of absolute-positioned nodes, *stripping the `role="group"` containers entirely* — so the **`aria-level`/`aria-setsize`/`aria-posinset` injected on every flattened node ARE the hierarchy** (AT relies on them, ignoring the flat DOM). The tree analogue of Table's `aria-rowindex` / List's `aria-posinset`.
- **The disclosure-nav-is-not-a-tree rule** — a nav hierarchy uses `<nav>` + nested `<ul>` + `button aria-expanded` (no tree roles, no roving arrow-key model); `role=tree` on nav imposes a keyboard contract nav users don't expect (see side-navigation).
- **WCAG SCs:** **1.3.1** (info & relationships — the level/group structure, even when virtualized), **2.1.1** (keyboard — every toggle/select/action), **4.1.2** (name/role/value — `aria-expanded`/`level`/`selected`/`checked` updating instantly), **4.1.3** (status messages — the expand/select/load announcements), **2.5.7** (the drag-reorder keyboard alternative).

## 7. Content guidelines
- **The node label** — concise, the accessible name (a file/folder name); truncate with ellipsis + the full text in a tooltip on hover.
- **Don't over-nest** — limit hierarchies to ~4–5 levels; deeper nesting increases visual noise, squashes horizontal space, and creates layout fatigue on narrow viewports.
- **The expand/collapse affordance** — the twisty must read as interactive (a chevron); in a directory tree, distinguish *expand* (the row/twisty) from *select* clearly (the twin-selection model — §4).
- **Counts / badges** — a node's item count (e.g., unread messages) renders in a trailing Badge, with SR-only context (`aria-label="Folder Inbox, 14 unread items"`).
- **Action accessibility** — node action buttons (Delete / Add Item) **must not steal focus during arrow-key navigation**; the user reaches them with **Tab** once focused on the node (arrow keys traverse the tree; Tab enters the node's actions).
- **Empty/loading copy** — an empty tree uses an Empty State; a lazy node shows a Skeleton/spinner + a "Loading…" label.

## 8. Motion and transition
- **The expand/collapse height reveal (inherited from Accordion)** — animate the group container `height: 0 → auto` with the platform solution Accordion landed (**`interpolate-size: allow-keywords`** unlocking the `0→auto` transition, or `::details-content`, or a measured-height/JS transition — see accordion).
- **The twisty rotation** — rotate the chevron 90° on expand (`transition: transform ~180ms ease`).
- **The lazy-load** — a brief spinner/Skeleton on the expanding node while children fetch (see skeleton).
- **The large-trees exception (the performance guard)** — **don't run expand height animations on virtualized trees or trees >~100 nodes**: virtualization mounts/unmounts nodes on the fly, and height calculations during those lifecycle changes cause layout thrashing/stutter — toggle **instantly** at scale.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the reveal + twisty rotation to instant; the hierarchy is the information, not the motion.

## 9. Internationalization
- **RTL — the indentation, twisty, and guide-lines flip to the inline-start (the right)**; the chevron mirrors (`▶`→`◀`), via logical properties (`padding-inline-start: calc(level × inset)` — inherited from Box; see box); no JS.
- **The RTL Right/Left key swap (the sharp trap)** — in LTR `ArrowRight` expands / `ArrowLeft` collapses; **in RTL they swap** (`ArrowLeft` expands, `ArrowRight` collapses) — the keys follow the *visual* direction children appear. Failing to swap creates a disorienting, counter-intuitive keyboard experience for RTL users — the classic RTL tree bug. Map the *logical* expand/collapse to physical keys by `dir`, don't hardcode.
- **Label expansion + depth** — translated labels run longer and deep indentation eats horizontal space; the combination forces wrapping/scroll — budget for it.
- **Leading folder/file icons** are direction-agnostic (don't mirror file-type glyphs; the chevron does mirror).

## 10. Naming
- **The field set:** **`TreeView`** (Spectrum/React Aria, Carbon, Fluent, Primer, Base Web — the dominant name); **`Tree`** / **`Tree.DirectoryTree`** (Ant); **`RichTreeView` / `SimpleTreeView`** (MUI X — the featured vs basic split); **`@atlaskit/tree`** (Atlassian — drag-and-drop); the headless libs **`react-arborist`** / **`react-complex-tree`**. Node naming: `TreeItem` (MUI X, Fluent), `TreeView.Item` (Primer), `TreeViewItem` (React Aria), `TreeNode` (Carbon).
- **The practice's default — `TreeView`** (or `Tree`) for the `role=tree` data-tree widget, with **`TreeViewItem`** (the node) and **`TreeViewGroup`** (the sub-group container). Expose a **`checkable`** mode (the checkbox-tree), a **`directory`** variant (folder icons + the file-explorer twin-selection), and `treegrid` as a *mode of the Table* (the expandable/hierarchical-rows Table — see table), not a separate component. The nav hierarchy is **Side Navigation** (disclosure), not a Tree. Don't ship a separate `DirectoryTree` component — it's a `TreeView` with folder icons + a directory selection model.
- **Aliases to map:** TreeView, TreeViewItem, TreeViewGroup, TreeGrid, DirectoryTree, RichTreeView, SimpleTreeView, FileTree.

## 11. Implementation notes
- **`role=tree` + recursive disclosure** — render `role="tree"` > `role="treeitem"` (+ `role="group"` for children); each parent node *is* a Disclosure (the Accordion `button aria-expanded` + reveal) applied recursively — reuse the Disclosure primitive, don't hand-roll per node (see accordion).
- **Roving tabindex over a flattened visible list** — maintain a flat list of *visible* (expanded) nodes; Up/Down move the roving `tabindex=0` through it (`getVisibleNodesList(data, expandedKeys)` → index ± 1 → `focus()`); Right/Left branch (expand/collapse/into/out); `*` expands the level; typeahead matches labels. This state machine is the bulk of the cost.
- **The flatten-the-visible-tree for virtualization** — compute the flat list of visible nodes, window it (TanStack Virtual / the headless tree libs render absolute-positioned siblings), and stamp **`aria-level`/`aria-setsize`/`aria-posinset`** on each rendered node so the hierarchy survives the stripped DOM nesting (Fluent's "flat tree" renders a flattened DOM by default for perf).
- **The tri-state cascade (two directional passes)** — on a node check: **(1) downward** — set the node + all descendants to the new state (descendants are never indeterminate after an override); **(2) upward** — ascend the parent chain, and for each parent inspect its children: all-checked → checked, none-checked-and-none-indeterminate → unchecked, else → **indeterminate**; recurse to the root. The `indeterminate` is a *DOM property set via ref* (the Checkbox brief — see checkbox), recomputed every change.
- **Lazy-load-on-expand + the async node state** — on first expand of a branch with `loadOnExpand`, add the node to a loading set (Skeleton/spinner + `aria-busy`), fetch, update the store + flag loaded, handle error/empty; cache loaded children.
- **The RTL Right/Left key swap** — map the *logical* expand/collapse to physical Arrows by `dir` (LTR Right=expand; RTL Right=collapse) — a direction-aware key handler, not hardcoded keys (§9).
- **The indentation / guide-line CSS** — `padding-inline-start: calc(var(--level) × var(--inset))`; optional guide lines via a border/pseudo-element on the group; keep the click target full-width regardless of indent.
- **Headless vs opinionated** — the keyboard state machine + the flatten/virtualize + the tri-state cascade are the heavy headless logic (react-arborist / react-complex-tree / React Aria's tree / MUI X RichTreeView own this); the node styling/icons/guide-lines are theme. **Build on a headless engine** — the APG keyboard model is too intricate to re-implement reliably.

## 12. Related and alternative components
- **Inherits:** the **Accordion/Disclosure** expand/collapse model (the `button aria-expanded` + the height-reveal, applied recursively per node — see accordion); the **List** item anatomy + vertical-collection styling (Tree = List + expand/collapse — see list).
- **Resolves:** **Table's `treegrid`** (the hierarchical/expandable Table row = a tree with columns — see table).
- **Closes:** the **Data category** (Table 2D + List 1D + Tree hierarchical).
- **Composes:** **Icon** (the twisty chevron + folder/file icons — see icon), **Checkbox** (the tri-state cascading selection — see checkbox), **Empty State** + **Skeleton** (empty/lazy-loading — see empty-state, skeleton), the **Menu** (per-node actions — see menu).
- **Borders:** **Side Navigation** (the nav hierarchy — disclosure, *not* `role=tree`; the boundary SideNav drew — see side-navigation), **Accordion** (the flat disclosure set — see accordion), **Menu** (commands — see menu).
- **Alternative to:** a nested **List** (static hierarchical content), a **Side Navigation** disclosure (a nav hierarchy), an **Accordion** (a flat disclosure set).

(The hierarchical sibling that closes the Data category — the `role=tree` data-tree widget completing Table (2D) + List (1D) + Tree (hierarchical). It inherits the Accordion disclosure model (recursively), is List + expand/collapse, resolves Table's `treegrid`, and composes Icon/Checkbox/Empty-State/Skeleton. See accordion for the disclosure model, list for the 1D sibling + node anatomy, table for the treegrid, side-navigation for the disclosure-nav boundary, checkbox for the tri-state cascade, icon for the twisty. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **From over-allocated roles → the disclosure-nav-is-not-a-tree clarification.** Early systems slapped `role="menu"`/`role="tree"` on standard nav menus, turning off browser navigation shortcuts for SR users; modern systems draw a clear line — navigation uses native links inside disclosures; `role=tree` is reserved for data-tree widgets (the Side Navigation boundary + APG).
2. **The `treegrid` for hierarchical tables** standardized the expandable/nested Table row (tree + columns).
3. **High-performance virtualization + the flattened render loop.** Older libraries nested the DOM recursively (poor at scale); modern libraries (react-arborist, Fluent's flat tree) convert the nesting into a flat visual array for virtualization while preserving accessibility via precise `aria-level`/`setsize`/`posinset`.
4. **The tri-state cascading checkbox tree** settled as the permissions/folder-selection pattern (the up-and-down propagation + the indeterminate parent).
5. **Highly accessible headless libraries** (React Aria, react-arborist, headless tree libs) made the intricate arrow-key traversal / roving focus / SR announcements reusable, letting DS engineers focus on styling — and Primer's TreeView (GitHub's file browser) / React Aria raised the accessible-tree reference bar.

## 14. Sources cited
(Conservative; reconcile with external — 2026 versions flagged unverified.) **WAI-ARIA APG** — the **Tree View pattern** + the **Treegrid pattern** (the canonical keyboard model + roles; `aria-expanded`/`level`/`setsize`/`posinset`; ~Aug 2024); **Adobe Spectrum / React Aria** — `TreeView`/`TreeViewItem` (the accessible collection-model tree; ~Oct 2024); **GitHub Primer** — `TreeView`/`TreeView.Item` (the repo file-tree — a strong accessible reference; 2024); **Microsoft Fluent** — `Tree`/`TreeItem` (the "flat tree" perf engine; v9); **MUI X** — `RichTreeView`/`SimpleTreeView` (selection/checkbox/lazy-loading/virtualization; the Pro tier; ~v7/v8); **Ant Design** — `Tree`/`Tree.DirectoryTree` (checkable/draggable/virtual); **IBM Carbon** — `TreeView`/`TreeNode` (selectable/with-icons); **Atlassian** — `@atlaskit/tree` (drag-and-drop); **react-arborist / react-complex-tree** — the headless virtualized tree libraries; **Base Web (Uber)** — `TreeView`. WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 4.1.3, 2.5.7.

## 15. Agent-consumable schema
```yaml
identity:
  id: tree
  name: Tree
  aliases: [TreeView, TreeViewItem, TreeViewGroup, TreeGrid, DirectoryTree, RichTreeView, SimpleTreeView, FileTree]
  category: data
  status: stable
description: >
  The hierarchical data-tree widget — the user expands/collapses, arrow-navigates, and
  selects/operates on a nested hierarchy; the third Data brief, which CLOSES the Data
  category (Table 2D + List 1D + Tree hierarchical). It IS List + expand/collapse (the
  node = a List item + indentation + a twisty), inherits the Accordion disclosure model
  (recursively), and resolves Table's treegrid (a tree with columns). NOT a nav hierarchy
  (that's disclosure / Side Navigation — role=tree ONLY for data-tree widgets; role=tree on
  nav breaks tab-key site discovery), NOT an Accordion (a flat disclosure set), NOT a Menu
  (commands). The headline: the role=tree vs role=treegrid vs disclosure-nav decision (the
  over-reach trap) decides the a11y model; the APG keyboard model is the hardest after the
  data grid. Composes Icon/Checkbox/Empty-State/Skeleton.
anatomy:
  parts:
    - "the tree container: role=tree (single-column widget) or role=treegrid (with columns); owns aria-multiselectable; the SINGLE interactive tab stop"
    - "the group container (role=group): wraps an expanded parent's children (non-virtualized); STRIPPED in the flattened/virtualized DOM (hierarchy then lives in the ARIA attrs)"
    - "the tree node (role=treeitem): a List item + hierarchy chrome — indentation/guide-lines (scales with aria-level) + the TWISTY (chevron on branches, aria-expanded; absent on leaves) + a folder/file Icon + the (presentational, aria-hidden) Checkbox + the label + trailing actions/Badge"
    - "the loading/empty regions: a lazy node renders a Skeleton/spinner child + aria-busy=true on the parent; an empty tree uses Empty State"
    - "the flattened-visible model (not visual): the visible (expanded) nodes flatten to an absolute-positioned list for virtualization; aria-level/setsize/posinset preserve the hierarchy"
api:
  inherits:
    - accordion    # the expand/collapse disclosure model (button aria-expanded + the height-reveal), applied recursively
    - list         # the hierarchical sibling — the node is a List item + indentation + a twisty
    - table        # resolves the treegrid (a tree with columns)
  composes: [icon, checkbox, empty-state, skeleton, menu]
  data-model: "a normalized FLAT-MAP internally (Record<id, {id,label,children:[ids],isBranch,icon,...}>) for O(1) lookups/mutation, even if the consumer passes nested JSON"
  props:
    - {name: data, type: "TreeNode[] | TreeDataMap", default: "[]", required: true}
    - {name: "expandedKeys (+ defaultExpandedKeys / onNodeExpand / onNodeCollapse)", type: "Key[]", default: ~, required: false, description: "controlled/uncontrolled; expandAll/collapseAll"}
    - {name: selectionMode, type: "'none'|'single'|'multiple'", default: none, required: false, description: "+ selectedKeys + onSelectionChange + selectionBehavior(toggle/replace)"}
    - {name: checkboxMode, type: "'none'|'cascade'|'independent'", default: none, required: false, description: "cascade = the tri-state up-and-down propagation"}
    - {name: loadOnExpand, type: "(id)=>Promise", default: ~, required: false, description: "async lazy-load children + the loading node state (Skeleton/spinner + aria-busy)"}
    - {name: role/kind, type: "'tree'|'treegrid'", default: tree, required: false, description: "single-column widget vs with-columns (a Table mode); a disclosure-nav is NOT a tree role"}
    - {name: node-renderer, type: "render fn", default: ~, required: false, description: "icon/label/actions; isBranch forces branch behavior even with empty children (lazy nodes)"}
    - {name: virtualize, type: boolean, default: false, required: false, description: "window the flattened visible nodes (+ aria-level/setsize/posinset)"}
    - {name: dragAndDrop, type: boolean, default: false, required: false, description: "drag-to-reparent + the keyboard alternative (the hardest reorder)"}
    - {name: density, type: "'compact'|'comfortable'", default: comfortable, required: false, description: "24-28px / 32-40px; the per-level indentation"}
  withholds: "Tree is the WIDGET; a nav hierarchy uses disclosure markup, not this"
states:
  node: [expanded, collapsed, leaf, focused, selected, loading, disabled]   # leaf = no twisty + NO aria-expanded; disabled cascades to descendants; loading = aria-busy + spinner/Skeleton
  checkbox-propagation: [checked, unchecked, indeterminate]   # all/none/some descendants (the Checkbox tri-state)
  tree: [loading, empty, populated]
variants:
  role: [tree, treegrid]
  selection: [none, single, multiple, checkbox-tree]
  kind: [data-tree, directory-tree]    # directory = click-row-toggles-expand (Finder/VS Code) + twin-selection (single-click highlights / double-click executes)
  treegrid-nav: [row-mode, grid-mode]  # row mode: Left/Right collapse/expand; grid mode: Left/Right cell nav
  density: [compact, comfortable]
  loading: [lazy, eager]
  guides: [guide-lines, indentation-only]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "4.1.3", "2.5.7"]
  role-taxonomy: "role=tree (root + aria-label) > role=treeitem (every node, branch AND leaf; focus styles target the treeitem not nested wrappers) > role=group (child container, declares nesting transitions)"
  structural-attrs: "each treeitem: aria-expanded (true/false on branches; ABSENT on leaves — adding it tricks AT into an empty branch), aria-level (1-based depth, sequential), aria-setsize (sibling count in the group), aria-posinset (1-based position)"
  apg-keyboard-model: "a single-tab-stop widget (active node tabindex=0, others -1, or aria-activedescendant). Down/Up = next/prev VISIBLE node; RIGHT = collapsed parent->expand, expanded parent->first child, leaf->nothing; LEFT = expanded parent->collapse, collapsed/leaf->parent; Home/End; typeahead; * = expand all siblings at the level; Enter/Space = activate/select. (RTL: Right/Left SWAP)"
  treegrid: "role=treegrid + role=row/gridcell; two-axis nav (Up/Down rows, Left/Right cells + Left/Right collapse/expand at the row's first cell) — the tree model crossed with the grid (the Table interlock)"
  checkbox-tree: "DON'T put the selection role on the checkbox — the visual checkbox is PRESENTATIONAL (aria-hidden); the role=treeitem carries aria-checked=true|false|MIXED (mixed = indeterminate parent — the Checkbox tri-state). Checking cascades down + derives up"
  virtualization-flattened-paradox: "windowing replaces nested elements with a flat list of absolute-positioned nodes, STRIPPING role=group entirely -> the aria-level/setsize/posinset injected on every flattened node ARE the hierarchy (AT relies on them, ignoring the flat DOM). The tree analogue of Table's aria-rowindex / List's aria-posinset"
  disclosure-nav-not-a-tree: "a nav hierarchy uses <nav> + nested <ul> + button aria-expanded (NO tree roles, NO roving arrow-key model); role=tree on nav imposes a keyboard contract nav users don't expect + breaks tab-key site discovery"
content:
  node-label: "concise, the accessible name (a file/folder name); truncate + the full text on hover"
  dont-over-nest: "cap ~4-5 levels; deeper = visual noise + squashed horizontal space + narrow-viewport fatigue"
  expand-affordance: "the twisty reads as interactive (a chevron); in a directory tree distinguish EXPAND (the row/twisty) from SELECT (the twin-selection model)"
  counts-badges: "a node's count in a trailing Badge + SR-only context (aria-label='Folder Inbox, 14 unread items')"
  action-accessibility: "node action buttons MUST NOT steal focus during arrow-key nav; reach them with TAB once focused on the node (arrows traverse the tree, Tab enters the node's actions)"
  empty-loading: "empty tree -> Empty State; a lazy node -> Skeleton/spinner + a 'Loading…' label"
motion:
  expand-reveal: "the group container height 0->auto (the Accordion solution — interpolate-size:allow-keywords unlocking the 0->auto transition, or ::details-content, or measured-height/JS)"
  twisty-rotation: "rotate the chevron 90deg on expand (transition: transform ~180ms ease)"
  lazy-load: "a brief spinner/Skeleton on the expanding node while children fetch"
  large-trees-exception: "DON'T run expand height animations on virtualized trees or >~100 nodes (mount/unmount + height calc = layout thrashing/stutter) — toggle INSTANTLY at scale"
  reduce-motion: "drop the reveal + twisty rotation to instant; the hierarchy is the information, not the motion"
i18n:
  rtl: "the indentation + twisty + guide-lines flip to the inline-start (right); the chevron mirrors; via logical properties (padding-inline-start: calc(level x inset), inherited from Box); no JS"
  rtl-key-swap: "the SHARP trap — LTR Right=expand/Left=collapse; RTL they SWAP (Left=expand/Right=collapse) — keys follow the visual direction children appear. Map the LOGICAL expand/collapse to physical keys by dir, don't hardcode (the classic RTL tree bug)"
  label-expansion: "translated labels run longer + deep indentation eats horizontal space -> budget for wrapping/scroll"
  icons: "leading folder/file icons are direction-agnostic (don't mirror file-type glyphs; the chevron does mirror)"
implementation:
  - "role=tree + RECURSIVE disclosure: role=tree > role=treeitem (+ role=group for children); each parent IS a Disclosure (the Accordion button aria-expanded + reveal) applied recursively — reuse the Disclosure primitive"
  - "roving tabindex over a FLATTENED visible list: getVisibleNodesList(data, expandedKeys); Up/Down move tabindex=0 through it (index +-1 -> focus()); Right/Left branch (expand/collapse/into/out); * expands the level; typeahead matches labels. This state machine is the bulk of the cost"
  - "flatten-the-visible-tree for virtualization: compute the flat visible list, window it (absolute-positioned siblings), stamp aria-level/setsize/posinset on each rendered node (the hierarchy survives the stripped DOM nesting); Fluent's 'flat tree' renders a flattened DOM by default"
  - "the tri-state cascade (TWO directional passes): (1) DOWNWARD — set the node + all descendants (descendants never indeterminate after an override); (2) UPWARD — ascend parents, for each: all-checked->checked, none-checked-and-none-indeterminate->unchecked, else->INDETERMINATE; recurse to root. indeterminate is a DOM property set via ref (the Checkbox brief), recomputed every change"
  - "lazy-load-on-expand + async node state: on first expand with loadOnExpand, add to a loading set (Skeleton/spinner + aria-busy), fetch, update the store + flag loaded, handle error/empty, cache"
  - "the RTL Right/Left key swap: map logical expand/collapse to physical Arrows by dir (LTR Right=expand; RTL Right=collapse) — a direction-aware handler, not hardcoded keys"
  - "indentation/guide-line CSS: padding-inline-start: calc(var(--level) x var(--inset)); optional guide lines (border/pseudo-element on the group); keep the click target full-width regardless of indent"
  - "headless vs opinionated: the keyboard state machine + flatten/virtualize + tri-state cascade are the heavy HEADLESS logic (react-arborist / react-complex-tree / React Aria tree / MUI X RichTreeView); node styling/icons/guides are theme. BUILD ON A HEADLESS ENGINE — the APG keyboard model is too intricate to re-implement reliably"
composition:
  inherits: [accordion, list, table]       # the disclosure model / the 1D sibling + node anatomy / the treegrid
  closes: "the Data category (Table 2D + List 1D + Tree hierarchical)"
  composes: [icon, checkbox, empty-state, skeleton, menu]
  borders: [side-navigation, accordion, menu]   # the nav hierarchy (disclosure, not role=tree) / the flat disclosure set / commands
  alternative-to: ["nested list (static hierarchical content)", side-navigation, accordion]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "role=tree (a data-tree widget — the practice default) vs disclosure-nav (a nav hierarchy — NOT role=tree, the Side Navigation boundary) vs role=treegrid (a tree with columns — a Table mode)"
    - "DirectoryTree as a separate component (Ant) vs a TreeView variant (practice — folder icons + the twin-selection directory model)"
    - "the checkbox cascade — selecting a parent auto-selects descendants (usually yes for permissions); cascade vs independent checkboxMode"
    - "build-on-a-headless-engine (react-arborist/RichTreeView/React Aria) vs hand-roll (the keyboard model is too intricate to hand-roll)"
    - "naming: TreeView/TreeViewItem (React Aria/Primer; the practice default) vs Tree/TreeItem (Fluent/MUI X)"
  trap:
    - "role=tree on a NAV hierarchy (breaks tab-key site discovery + imposes an unexpected key-interception mode — use disclosure)"
    - "the RTL Right/Left key swap (hardcoding LTR keys breaks RTL — the classic RTL tree bug)"
    - "virtualization losing the hierarchy (needs aria-level/setsize/posinset on the flattened nodes; role=group is stripped)"
    - "aria-expanded on a LEAF (tricks AT into an empty branch); the selection role on the checkbox instead of aria-checked on the treeitem"
    - "the tri-state cascade computed one direction only (must propagate both up and down); indeterminate set as an attribute not a DOM property"
    - "animating expand/collapse on large/virtualized trees (>~100 nodes — layout thrashing); over-nesting (>5 levels indents off-screen); node action buttons stealing arrow-key focus (reach via Tab)"
  inherited: "the Accordion/Disclosure expand-collapse model (recursively); the List item anatomy + hierarchical-sibling relationship; Table's treegrid; the Checkbox tri-state/indeterminate; the role=X over-reach discipline from Table/Menu/List; aria-setsize/posinset from List"
  role-in-family: "the hierarchical sibling that CLOSES the Data category — the role=tree data-tree widget completing Table (2D) + List (1D) + Tree (hierarchical); inherits the Accordion disclosure model, is List + expand/collapse, resolves Table's treegrid; borders Side Navigation (disclosure-nav)"
  evolution:
    - "over-allocated roles -> the disclosure-nav-is-not-a-tree clarification (Side Nav + APG)"
    - "the treegrid for hierarchical tables"
    - "high-perf virtualization + the flatten-the-visible-tree + aria-level/setsize/posinset (Fluent flat tree, react-arborist)"
    - "the tri-state cascading checkbox tree settling (permissions/folder selection)"
    - "highly accessible headless libraries (React Aria/react-arborist) + Primer/React-Aria raising the a11y bar"
  unverified:
    - "external 2026 version numbers (MUI X RichTreeView tier, React Aria tree, Ant, Primer TreeView, Fluent flat tree)"
    - "the React Aria / APG treegrid keyboard specifics + the Fluent flat-tree details — verify against current implementations"
    - "MUI X RichTreeView commercial-licensing tier — verify current"
```

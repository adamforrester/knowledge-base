# Tree — field-truth study (Claude pass)

## 1. Framing
A Tree (TreeView) is the **hierarchical data widget** — it presents a nested hierarchy of nodes the user expands/collapses, navigates with arrow keys, and selects/operates on. It is the third and final Data brief and **closes the Data category**, completing the set: **Table** (2D matrix), **List** (1D sequence), **Tree** (hierarchical). It leans on more prior work than anything else in the catalogue — it *is* List + expand/collapse, the node is a List item + indentation + a disclosure twisty, and it inherits the disclosure model Accordion landed, applied recursively.

The headline that decides the accessibility model — the over-reach trap parallel to Table's `role=grid`, Menu's `role=menu`, and List's listbox-vs-gridlist — is the **`role=tree` vs `role=treegrid` vs disclosure-nav decision**:
- **`role=tree` (the tree widget)** — a single-column hierarchical *selection/operation* widget: a file tree, a folder picker, a layers panel. The APG Tree pattern (the full arrow-key model — §6). The genuine "operate on a data hierarchy" case.
- **`role=treegrid`** — a tree *with columns* (the hierarchical/expandable Table row Table deferred to here): multi-column hierarchical data, two-axis arrow navigation.
- **The nested-`<ul>` + `aria-expanded` disclosure (a NAV hierarchy)** — a docs sidebar, a file-browser nav: `<nav>` + nested `<ul>` + per-parent `button aria-expanded` *disclosure*, **not** a `role=tree` widget. This is the Side Navigation pattern (which drew the boundary: "Disclosure-not-`role=menu`" and "`role=tree`-only-for-data-trees").

The resolution (the load-bearing call): **`role=tree` only for a genuine data-tree *widget*** (you select/operate on the hierarchy with the full keyboard model); a *navigation* hierarchy is disclosure (`<nav>` + nested `<ul>` + `aria-expanded`), **never `role=tree`** — the most-misused ARIA pattern after `role=grid`, because a docs sidebar *looks* like a tree but isn't a tree widget. What it *isn't*: a **nav hierarchy** (disclosure / Side Navigation — see side-navigation), an **Accordion** (a *flat* set of independent disclosure sections — no hierarchy, not arrow-navigable as one widget — see accordion), or a **Menu** (commands — see menu). Why systems disagree: the role=tree-vs-disclosure over-reach, the tri-state checkbox-tree cascade, and the virtualization-vs-hierarchy tension.

## 2. Anatomy and parts
- **the tree container** — `role="tree"` (single-column widget) or `role="treegrid"` (with columns); single tab stop + roving focus (§6). The nav-hierarchy alternative is a plain `<nav>`/`<ul>` (no tree role).
- **the tree node** (`role="treeitem"`) — the unit; a List item + hierarchy chrome:
  - **the indentation / guide-lines** — depth visualized by inset per level (+ optional vertical guide lines); the `aria-level` conveys it to AT (§6).
  - **the expand/collapse twisty** — a chevron/triangle disclosure toggle on parent nodes (rotates on expand); the `aria-expanded` carrier (the Accordion disclosure, per node — see accordion). Leaf nodes have none.
  - **the leading Icon** — folder/file/type icon (see icon); a folder icon often reflects open/closed.
  - **the label** — the node text (the accessible name).
  - **the trailing** — actions (an overflow Menu), a Badge/count, a Switch.
  - **the (tri-state) Checkbox** — for a checkbox-tree (the selection; checked/unchecked/**indeterminate** — see checkbox; §6).
- **the group** — `role="group"` wrapping a node's children (the nested level).
- **the loading / empty node regions** — a **Skeleton** node (lazy children loading) and the **Empty State** (an empty tree / an empty folder — see skeleton, empty-state).
- **the flattened-visible model** (not visual) — internally the *visible* (expanded) nodes flatten to a list for rendering/virtualization, with `aria-level`/`setsize`/`posinset` preserving the hierarchy (§6/§11).

## 3. Properties / API
- **the tree data** — `nodes` (a recursive `{ id, label, children, icon, … }` structure) + `expandedKeys` (controlled/uncontrolled) + `selectedKeys`.
- **`role` / kind** — `tree` (single-column) / `treegrid` (with columns) / a disclosure-nav (not a tree role — §5).
- **selection** — `selectionMode` (none / single / multiple) + the **checkbox-tree** mode (`checkable` + the tri-state cascade — §6); `aria-selected` (tree) vs the checkbox state (checkbox-tree).
- **expand/collapse** — `expandedKeys` + `onExpandedChange`, `defaultExpandedKeys`, `expandAll`/`collapseAll`; the expand-on-select option.
- **lazy-load children** — `loadChildren(node)` (async load-on-expand) + the loading node state (a Skeleton/spinner child while fetching).
- **the node renderer** — a render function for the node content (icon/label/actions — where Icon/Checkbox/Badge/Menu compose); the leaf-vs-parent distinction.
- **virtualization** — windowing the flattened visible nodes (+ the `aria-level`/`setsize`/`posinset` — §6).
- **`draggable` / reorder** — drag-to-move a node to a new parent (re-parenting) + the keyboard alternative (§11) — the hardest reorder.
- **density** — comfortable/compact node height; the indentation size per level.
- **what it withholds** — Tree is the *widget*; a nav hierarchy uses disclosure markup, not this.

## 4. States and variants
- **States:**
  - **node:** expanded / collapsed / **leaf** (no children, no twisty); **loading** (lazy children fetching); **focused** (roving — one node has `tabindex=0`); **selected** (single/multi — `aria-selected`); **disabled**.
  - **the tri-state parent (checkbox-tree):** **checked** (all descendants checked) / **unchecked** (none) / **indeterminate** (some — the Checkbox brief's indeterminate; §6).
  - **tree:** loading (initial) / empty (Empty State) / populated.
- **Variants:**
  - **role:** tree (single-column) / treegrid (with columns).
  - **selection:** none / single / multiple / checkbox-tree (tri-state cascade).
  - **directory tree** (folder/file icons, expand-on-twisty) vs a plain data tree.
  - **with guide-lines** vs indentation-only.
  - **density:** comfortable / compact.
  - **lazy** (load-on-expand) vs eager.

## 5. Usage guidance
- **Use a `role=tree` Tree for operating on a genuine data hierarchy** — a file/folder tree, a layers/outline panel, a category picker, a permissions tree, an org chart's nodes. The signal: the user *selects or operates on* nested data with expand/collapse and arrow-key navigation.
- **Tree vs the alternatives (the boundary set):**
  - **vs a nav hierarchy / Side Navigation** — a navigation menu with expandable sections (a docs sidebar, a file-browser *nav*) is **disclosure** (`<nav>` + nested `<ul>` + `aria-expanded`), **not** `role=tree`. The rule (from Side Navigation): **`role=tree` only for data-tree widgets** — a nav that *looks* like a tree is still nav. Don't build navigation as a `role=tree` (it imposes a keyboard model — arrow-to-expand — that nav users don't expect; see side-navigation).
  - **vs an Accordion** — an Accordion is a *flat* set of independent expand/collapse sections (no nesting, each header its own tab stop, no arrow-key tree navigation); a Tree is a *nested hierarchy* navigated as one widget (see accordion).
  - **vs a nested List** — a *static, read-only* hierarchical content list (no widget keyboard model) can be a nested `<ul>` (the disclosure-content case); a Tree is the *interactive* widget version (see list).
  - **vs a Menu** — commands → a **Menu** (see menu); a Tree selects/operates on data.
  - **vs a Table** — when the hierarchy needs *columns* (a file tree with size/modified columns) → **`role=treegrid`** (a tree with columns — see table).
- **When to virtualize** — large trees (file systems, big org data) — windowing the flattened visible nodes (§6/§11); not needed for a small tree.
- **Don't over-nest** — deep hierarchies are hard to navigate and indent off-screen; cap practical depth, or use breadcrumb + drill-in for very deep data.

## 6. Accessibility
Tree has the **hardest keyboard model in the catalogue after the data grid**, and the genre (tree vs treegrid vs disclosure-nav) decides it (§1).

- **The `role=tree` structure** — `role="tree"` on the container, `role="treeitem"` on each node, `role="group"` wrapping a parent's children. Each treeitem carries **`aria-expanded`** (true/false — *absent* on leaves), **`aria-level`** (1-based depth), **`aria-setsize`** (sibling count at this level), **`aria-posinset`** (1-based position among siblings), and **`aria-selected`** (selection). The container is **one tab stop** with roving tabindex (or `aria-activedescendant`).
- **The APG Tree keyboard model (the full contract):**
  - **Down/Up** — move to the next/previous *visible* node (the flattened expanded tree — moving *across* levels, not within one).
  - **Right** — on a *collapsed* parent: expand (stay on it); on an *expanded* parent: move to its first child; on a *leaf*: nothing.
  - **Left** — on an *expanded* parent: collapse; on a *collapsed* node or a leaf: move to its parent.
  - **Home/End** — first/last visible node; **typeahead** — focus the next node matching typed characters; **`*`** — expand all sibling nodes at the current level; **Enter/Space** — activate/select (and toggle in a checkbox-tree).
  - **(RTL: Right and Left swap — §9, the key trap.)**
- **The `treegrid`** — `role="treegrid"` + `role="row"`/`role="gridcell"`; two-axis navigation (Up/Down rows, Left/Right cells, with Left/Right *also* collapsing/expanding at the row's first cell) — the tree keyboard model crossed with the grid's (the Table interlock — see table).
- **The checkbox-tree (the tri-state crux)** — the **Checkbox is the selection mechanism, the treeitem the structure**: each node has a Checkbox with `aria-checked="true|false|mixed"` (**mixed** = the indeterminate parent — the Checkbox brief's tri-state; see checkbox); checking a parent **cascades** to all descendants, and a parent's state is **derived** from its children (all→checked, none→unchecked, some→mixed) — the propagation runs *both* directions (§11). The treeitem may carry `aria-checked` directly (the multi-select tree) rather than `aria-selected`.
- **Virtualization — the flatten + `aria-level`/`setsize`/`posinset`.** Windowing renders only visible nodes, so the **`aria-level`/`aria-setsize`/`aria-posinset`** on each rendered node *are* the hierarchy for AT (they don't depend on the DOM nesting being complete) — the flattened-visible-tree technique keeps the structure honest despite windowing (the tree analogue of Table's `aria-rowindex` / List's `aria-posinset`).
- **The disclosure-nav-is-not-a-tree rule** — a nav hierarchy uses `<nav>` + nested `<ul>` + `button aria-expanded` (no tree roles, no roving arrow-key model) — imposing `role=tree` on nav gives users a keyboard contract they don't expect (see side-navigation).
- **WCAG SCs:** **1.3.1** (info & relationships — the level/group structure), **2.1.1** (keyboard — the full APG model), **4.1.2** (name/role/value — `aria-expanded`/`level`/`selected`/`checked`), **4.1.3** (status messages — the expand/select/load announcements), **2.5.7** (the drag-reorder keyboard alternative). Tree is the deepest a11y brief in Data after Table.

## 7. Content guidelines
- **The node label** — concise, the accessible name; for a file tree, the file/folder name; truncate with ellipsis + the full name on hover (the List/Tag discipline).
- **Don't over-nest** — deep trees indent off-screen and are hard to navigate; keep the practical depth shallow, or provide a drill-in/breadcrumb for very deep data. The indentation must stay legible (cap the per-level inset on deep trees).
- **The expand/collapse affordance** — the twisty must read as interactive (a chevron, not just an indent); the whole node-row may toggle expand, but distinguish *expand* from *select* (clicking the label selects; clicking the twisty expands — or define one clearly).
- **The checkbox-tree labels** — each checkbox's accessible name is its node label; the tri-state parent announces "mixed"/"partially checked".
- **Counts/badges** — a parent may show a child count or a status Badge; keep it from competing with the twisty/label.
- **Empty/loading copy** — an empty tree uses an Empty State; a loading/lazy node shows a Skeleton/spinner with a label ("Loading…").

## 8. Motion and transition
- **The expand/collapse reveal (inherited from Accordion)** — the children region animates open/closed; use the platform height-animation Accordion landed (`calc-size()`/`interpolate-size`, or `::details-content`, or a measured-height transition — see accordion); the **twisty rotates** (a chevron 90°).
- **The lazy-load** — a brief spinner/Skeleton on the expanding node while children fetch (see skeleton).
- **Restraint on large trees** — **don't animate expand/collapse on large/virtualized trees** (reflowing thousands of windowed nodes janks); instant expand at scale. Node insert/remove can FLIP on a small tree (the Stack/List discipline).
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops the expand reveal + twisty rotation to instant; the hierarchy is the information, not the motion.

## 9. Internationalization
- **RTL — the indentation and the twisty/guide-lines flip to the inline-start (the right)**, the chevron mirrors (`▶`→`◀`), via logical properties (`padding-inline-start` for the depth inset — inherited from Box; see box); no JS.
- **The Right/Left key swap (the sharp RTL trap)** — in RTL, **Right collapses and Left expands** (the keys follow the *visual* direction: the expand-arrow points toward where children appear, which is inline-start = left in RTL). The APG model's Right=expand/Left=collapse is *logical*, mapped to physical keys by direction — getting this backwards is the classic RTL tree bug.
- **Label expansion + depth** — translated labels run longer and deep indentation eats horizontal space; the combination can force wrapping/scroll — budget for it.
- **The leading folder/file icons** are direction-agnostic (don't mirror file-type glyphs).

## 10. Naming
- **The field set:** **`Tree` / `TreeView`** (the dominant name — Spectrum/React Aria, Carbon, Fluent, Primer, Base Web); **`RichTreeView` / `SimpleTreeView`** (MUI X — the featured vs basic split); **`Tree` + `Tree.DirectoryTree`** (Ant — the file-tree variant); **`@atlaskit/tree`** (Atlassian — the drag-and-drop tree); the headless libs **`react-arborist`** / **`react-complex-tree`**.
- **The practice's default — `Tree` (or `TreeView`)** for the `role=tree` data-tree widget, with a **`checkable`** mode for the checkbox-tree and a **`directory`** variant for the file/folder tree. The **`treegrid`** is a *mode of the Table* (the expandable/hierarchical-rows Table — see table), not a separate component — name it as Table's hierarchical variant. The nav hierarchy is **Side Navigation** (disclosure), not a Tree. Don't ship a separate `DirectoryTree` component — it's a `Tree` with folder icons + a directory selection model.
- **Aliases to map:** TreeView, TreeGrid, DirectoryTree, RichTreeView, SimpleTreeView, FileTree.

## 11. Implementation notes
- **The `role=tree` + recursive disclosure** — render `role="tree"` > `role="treeitem"` (+ `role="group"` for children); each parent node *is* a Disclosure (the Accordion `button aria-expanded` + the reveal), applied recursively — Tree is disclosure all the way down (see accordion). Don't hand-roll disclosure per node; reuse the Disclosure primitive.
- **The full APG keyboard model + roving/activedescendant** — maintain a *flattened list of visible nodes* (the expanded tree); Up/Down move the roving `tabindex=0` through it; Right/Left implement the expand/collapse/into/out branching (§6); `*` expands the level; typeahead matches labels. This state machine is the bulk of the implementation cost.
- **The flatten-the-visible-tree for virtualization** — compute the flat list of *visible* (expanded) nodes, window it (TanStack Virtual / the headless tree libs), and stamp **`aria-level`/`aria-setsize`/`aria-posinset`** on each rendered node so the hierarchy survives windowing (the structure lives in the ARIA attributes, not the DOM nesting). Fluent's "flat tree" renders a flattened DOM for perf with the same ARIA-attribute hierarchy.
- **The tri-state cascade (the checkbox-tree logic)** — propagation runs *both* directions: checking a parent **cascades down** (set all descendants), and a node's check state **derives up** from its children (all→checked, none→unchecked, some→`indeterminate`); the indeterminate is a *DOM property set via ref* (the Checkbox brief — see checkbox), recomputed on every change. Decide whether selecting a parent auto-selects descendants in the data model (it usually should for permissions trees).
- **Lazy-load-on-expand + the async node state** — on first expand of a parent with `loadChildren`, show a loading node (Skeleton/spinner), fetch, then render children; cache loaded children; handle the empty-children and error cases.
- **The RTL Right/Left key swap** — map the *logical* expand/collapse to physical Arrow keys by `dir`: in LTR Right=expand/Left=collapse; in RTL Right=collapse/Left=expand. A direction-aware key handler, not hardcoded keys (§9).
- **The indentation / guide-line CSS** — `padding-inline-start` per level (a depth × inset), optional vertical guide lines via a border/pseudo-element on the group; keep the click target full-width regardless of indent.
- **Headless vs opinionated** — the keyboard state machine + the flatten/virtualize + the tri-state cascade are the heavy headless logic (react-arborist / React Aria's tree / MUI X RichTreeView own this); the node styling/icons/guide-lines are theme. This is a *build-on-a-headless-engine* component, not a hand-roll — the APG keyboard model is too intricate to re-implement.

## 12. Related and alternative components
- **Inherits:** the **Accordion/Disclosure** expand/collapse model (the `button aria-expanded` + the height-reveal animation, applied recursively per node — see accordion).
- **The hierarchical sibling of:** **List** (Tree = List + expand/collapse; the node is a List item + indentation + a twisty — see list) — completing Table (2D) + List (1D) + Tree (hierarchical), **closing the Data category**.
- **Resolves:** **Table's `treegrid`** (the hierarchical/expandable Table row = a tree with columns — see table).
- **Composes:** **Icon** (the twisty chevron + folder/file icons — see icon), **Checkbox** (the tri-state cascading selection — see checkbox), **Empty State** + **Skeleton** (empty/lazy-loading — see empty-state, skeleton), the **Menu** (per-node actions — see menu).
- **Borders:** **Side Navigation** (the nav hierarchy — disclosure, *not* `role=tree`; the boundary SideNav drew — see side-navigation), **Accordion** (the flat disclosure set — see accordion), **Menu** (commands — see menu).
- **Alternative to:** a nested **List** (static hierarchical content), a **Side Navigation** disclosure (a nav hierarchy), an **Accordion** (a flat disclosure set).

(The hierarchical sibling that closes the Data category — the `role=tree` data-tree widget completing Table (2D) + List (1D) + Tree (hierarchical). It inherits the Accordion disclosure model (recursively), is List + expand/collapse, resolves Table's `treegrid`, and composes Icon/Checkbox/Empty-State/Skeleton. See accordion for the disclosure model, list for the 1D sibling + node anatomy, table for the treegrid, side-navigation for the disclosure-nav boundary, checkbox for the tri-state cascade, icon for the twisty. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The `role=tree` over-reach → the disclosure-nav-is-not-a-tree clarification.** Teams slapped `role=tree` on nav sidebars (it *looks* like a tree); the field — via Side Navigation guidance and APG — clarified that **`role=tree` is for data-tree widgets**, and a nav hierarchy is disclosure (`<nav>` + nested `<ul>` + `aria-expanded`), restoring the keyboard contract nav users expect.
2. **The `treegrid` for hierarchical tables.** The expandable/nested Table row standardized on `role=treegrid` (tree + columns), connecting Tree and Table.
3. **Virtualization + the flatten-the-visible-tree.** Large file trees forced windowing; the flatten-visible-nodes + `aria-level`/`setsize`/`posinset` technique (and Fluent's "flat tree") kept the hierarchy honest to AT despite a windowed DOM.
4. **The tri-state cascading checkbox tree** settled as the permissions/folder-selection pattern — the Checkbox indeterminate + the up-and-down cascade.
5. **The headless virtualized tree libs + raised a11y bar.** react-arborist / react-complex-tree / MUI X RichTreeView / React Aria's tree made the intricate keyboard state machine + virtualization reusable, and Primer's TreeView (GitHub's file browser) / React Aria raised the accessible-tree reference bar.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- WAI-ARIA APG — the **Tree View pattern** + the **Treegrid pattern** (the canonical keyboard model + roles; `aria-expanded`/`level`/`setsize`/`posinset`).
- MUI X — `RichTreeView` / `SimpleTreeView` (selection/multi-select/checkbox/lazy-loading/virtualization; the Pro tier).
- Ant Design — `Tree` (checkable/draggable/virtual) + `Tree.DirectoryTree`.
- Adobe Spectrum / React Aria — `Tree`/`TreeView` (the accessible collection-model tree).
- GitHub Primer — `TreeView` (the repo file-tree — a strong accessible reference).
- Microsoft Fluent — `Tree`/`TreeItem` (the "flat tree" perf approach).
- IBM Carbon — `TreeView` (selectable/with-icons).
- Atlassian — `@atlaskit/tree` (the drag-and-drop tree).
- react-arborist / react-complex-tree — the headless virtualized tree libraries.
- Base Web (Uber) — `TreeView`.
- WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 4.1.3, 2.5.7.

## 15. Agent-consumable schema
```yaml
identity:
  id: tree
  name: Tree
  aliases: [TreeView, TreeGrid, DirectoryTree, RichTreeView, SimpleTreeView, FileTree]
  category: data
  status: stable
description: >
  The hierarchical data-tree widget — the user expands/collapses, arrow-navigates, and
  selects/operates on a nested hierarchy; the third Data brief, which CLOSES the Data
  category (Table 2D + List 1D + Tree hierarchical). It IS List + expand/collapse (the
  node = a List item + indentation + a twisty), inherits the Accordion disclosure model
  (recursively), and resolves Table's treegrid (a tree with columns). NOT a nav hierarchy
  (that's disclosure / Side Navigation — role=tree is ONLY for data-tree widgets), NOT an
  Accordion (a flat disclosure set, not arrow-navigable as one widget), NOT a Menu
  (commands). The headline: the role=tree vs role=treegrid vs disclosure-nav decision (the
  over-reach trap) decides the a11y model; the APG keyboard model is the hardest after the
  data grid. Composes Icon/Checkbox/Empty-State/Skeleton.
anatomy:
  parts:
    - "the tree container: role=tree (single-column widget) or role=treegrid (with columns); ONE tab stop + roving focus; the nav-hierarchy alternative is a plain <nav>/<ul> (no tree role)"
    - "the tree node (role=treeitem): a List item + hierarchy chrome — indentation/guide-lines (depth; aria-level conveys it) + the expand/collapse TWISTY (a chevron on parents, aria-expanded; absent on leaves) + a leading folder/file Icon + the label + trailing (actions/Badge/Switch)"
    - "the (tri-state) Checkbox: for a checkbox-tree — checked/unchecked/INDETERMINATE (the selection)"
    - "the group: role=group wrapping a node's children (the nested level)"
    - "the loading/empty regions: a Skeleton node (lazy children) + the Empty State (empty tree/folder)"
    - "the flattened-visible model (not visual): the visible (expanded) nodes flatten to a list for render/virtualization; aria-level/setsize/posinset preserve the hierarchy"
api:
  inherits:
    - accordion    # the expand/collapse disclosure model (button aria-expanded + the height-reveal), applied recursively
    - list         # the hierarchical sibling — the node is a List item + indentation + a twisty
    - table        # resolves the treegrid (a tree with columns)
  composes: [icon, checkbox, empty-state, skeleton, menu]
  props:
    - {name: nodes, type: "recursive {id,label,children,icon,...}", default: ~, required: true, description: "the tree data"}
    - {name: "expandedKeys (+ onExpandedChange / defaultExpandedKeys)", type: "Key[]", default: ~, required: false, description: "controlled/uncontrolled expand state; expandAll/collapseAll"}
    - {name: role/kind, type: "'tree'|'treegrid'", default: tree, required: false, description: "single-column widget vs with-columns (a Table mode); a disclosure-nav is NOT a tree role"}
    - {name: selection, type: "selectionMode (none|single|multiple) + checkable (the tri-state checkbox-tree)", default: none, required: false, description: "aria-selected (tree) vs the checkbox state (checkbox-tree); the cascade"}
    - {name: loadChildren, type: function, default: ~, required: false, description: "async load-on-expand + the loading node state (Skeleton/spinner child)"}
    - {name: node-renderer, type: "render fn", default: ~, required: false, description: "icon/label/actions — where Icon/Checkbox/Badge/Menu compose; leaf-vs-parent"}
    - {name: virtualization, type: boolean, default: false, required: false, description: "window the flattened visible nodes (+ aria-level/setsize/posinset)"}
    - {name: draggable, type: boolean, default: false, required: false, description: "drag-to-reparent + the keyboard alternative (the hardest reorder)"}
    - {name: density, type: "'comfortable'|'compact'", default: comfortable, required: false, description: "node height; the indentation size per level"}
  withholds: "Tree is the WIDGET; a nav hierarchy uses disclosure markup, not this"
states:
  node: [expanded, collapsed, leaf, loading, focused, selected, disabled]
  tri-state-parent: [checked, unchecked, indeterminate]   # checkbox-tree — all/none/some descendants (the Checkbox brief's tri-state)
  tree: [loading, empty, populated]
variants:
  role: [tree, treegrid]
  selection: [none, single, multiple, checkbox-tree]
  kind: [directory-tree, data-tree]
  guides: [guide-lines, indentation-only]
  density: [comfortable, compact]
  loading: [lazy, eager]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "4.1.3", "2.5.7"]
  role-tree-structure: "role=tree (container) + role=treeitem (node) + role=group (children); each treeitem carries aria-expanded (true/false, ABSENT on leaves), aria-level (1-based depth), aria-setsize (sibling count), aria-posinset (1-based among siblings), aria-selected. ONE tab stop + roving tabindex (or aria-activedescendant)"
  apg-keyboard-model: "Down/Up = next/prev VISIBLE node (the flattened expanded tree); RIGHT = collapsed parent->expand, expanded parent->first child, leaf->nothing; LEFT = expanded parent->collapse, collapsed/leaf->parent; Home/End; typeahead; * = expand all siblings at the level; Enter/Space = activate/select. (RTL: Right/Left SWAP)"
  treegrid: "role=treegrid + role=row/gridcell; two-axis nav (Up/Down rows, Left/Right cells + Left/Right collapse/expand at the row's first cell) — the tree model crossed with the grid (the Table interlock)"
  checkbox-tree: "the CHECKBOX is the selection, the treeitem the STRUCTURE: each node's checkbox aria-checked=true|false|MIXED (mixed = indeterminate parent — the Checkbox tri-state); checking a parent CASCADES down + a parent derives up (all->checked/none->unchecked/some->mixed); the treeitem may carry aria-checked directly (multi-select tree)"
  virtualization: "windowing renders only visible nodes -> the aria-level/setsize/posinset on each rendered node ARE the hierarchy for AT (independent of DOM nesting completeness) — the flatten-the-visible-tree technique (the tree analogue of Table's aria-rowindex / List's aria-posinset)"
  disclosure-nav-not-a-tree: "a nav hierarchy uses <nav> + nested <ul> + button aria-expanded (NO tree roles, NO roving arrow-key model); imposing role=tree on nav gives a keyboard contract users don't expect (the Side Navigation boundary)"
content:
  node-label: "concise, the accessible name (a file/folder name); truncate + full name on hover"
  dont-over-nest: "deep trees indent off-screen + are hard to navigate; cap practical depth or use drill-in/breadcrumb; cap the per-level inset"
  expand-affordance: "the twisty reads as interactive (a chevron); distinguish EXPAND (the twisty) from SELECT (the label)"
  checkbox-labels: "each checkbox's name = its node label; the tri-state parent announces 'mixed'/'partially checked'"
  empty-loading: "empty tree -> Empty State; a lazy node -> Skeleton/spinner + a 'Loading…' label"
motion:
  expand-reveal: "the children region animates open/closed (the Accordion height-animation — calc-size/interpolate-size / ::details-content / measured-height); the TWISTY rotates (chevron 90deg)"
  lazy-load: "a brief spinner/Skeleton on the expanding node while children fetch"
  restraint: "DON'T animate expand/collapse on large/virtualized trees (reflowing windowed nodes janks) — instant at scale; node insert/remove FLIP on a SMALL tree"
  reduce-motion: "drop the expand reveal + twisty rotation to instant; the hierarchy is the information, not the motion"
i18n:
  rtl: "the indentation + twisty/guide-lines flip to the inline-start (right); the chevron mirrors; via logical properties (padding-inline-start for the depth inset, inherited from Box); no JS"
  rtl-key-swap: "the SHARP trap — in RTL, RIGHT collapses + LEFT expands (the keys follow the visual direction children appear, inline-start=left in RTL); map the LOGICAL expand/collapse to physical keys by dir, don't hardcode"
  label-expansion: "translated labels run longer + deep indentation eats horizontal space -> budget for wrapping/scroll"
  icons: "leading folder/file icons are direction-agnostic (don't mirror file-type glyphs)"
implementation:
  - "role=tree + RECURSIVE disclosure: render role=tree > role=treeitem (+ role=group for children); each parent IS a Disclosure (the Accordion button aria-expanded + reveal) applied recursively — reuse the Disclosure primitive, don't hand-roll per node"
  - "the full APG keyboard model + roving/activedescendant: maintain a FLATTENED list of visible nodes; Up/Down move the roving tabindex=0 through it; Right/Left branch (expand/collapse/into/out); * expands the level; typeahead matches labels. This state machine is the bulk of the cost"
  - "flatten-the-visible-tree for virtualization: compute the flat list of visible nodes, window it, stamp aria-level/setsize/posinset on each rendered node (the hierarchy lives in the ARIA attributes, not the DOM nesting); Fluent's 'flat tree' renders a flattened DOM for perf"
  - "the tri-state cascade (checkbox-tree): propagation BOTH directions — checking a parent cascades DOWN (all descendants) + a node derives UP from children (all->checked/none->unchecked/some->indeterminate); indeterminate is a DOM property set via ref (the Checkbox brief), recomputed on every change; decide if selecting a parent auto-selects descendants in the data model (usually yes for permissions)"
  - "lazy-load-on-expand + the async node state: on first expand with loadChildren, show a loading node (Skeleton/spinner), fetch, render children, cache; handle empty-children + error"
  - "the RTL Right/Left key swap: map logical expand/collapse to physical Arrows by dir (LTR Right=expand; RTL Right=collapse) — a direction-aware handler, not hardcoded keys"
  - "the indentation/guide-line CSS: padding-inline-start per level (depth x inset) + optional guide lines (border/pseudo-element on the group); keep the click target full-width regardless of indent"
  - "headless vs opinionated: the keyboard state machine + flatten/virtualize + tri-state cascade are the heavy HEADLESS logic (react-arborist / React Aria tree / MUI X RichTreeView own this); node styling/icons/guides are theme. BUILD ON A HEADLESS ENGINE — the APG keyboard model is too intricate to re-implement"
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
    - "DirectoryTree as a separate component (Ant) vs a Tree variant (practice — folder icons + a directory selection model)"
    - "selecting a parent auto-selects descendants (the cascade) — usually yes for permissions trees"
    - "build-on-a-headless-engine (react-arborist/RichTreeView/React Aria) vs hand-roll (the keyboard model is too intricate to hand-roll)"
  trap:
    - "role=tree on a NAV hierarchy (imposes a keyboard model nav users don't expect — use disclosure)"
    - "the RTL Right/Left key swap (hardcoding LTR keys breaks RTL — the classic RTL tree bug)"
    - "virtualization losing the hierarchy (needs aria-level/setsize/posinset on the flattened nodes)"
    - "the tri-state cascade computed one direction only (must propagate both up and down); indeterminate set as an attribute not a DOM property"
    - "animating expand/collapse on large/virtualized trees (jank); over-nesting (indents off-screen)"
    - "conflating expand (the twisty) with select (the label)"
  inherited: "the Accordion/Disclosure expand-collapse model (recursively); the List item anatomy + the hierarchical-sibling relationship; Table's treegrid; the Checkbox tri-state/indeterminate; the role=X over-reach discipline from Table/Menu/List; aria-setsize/posinset from List"
  role-in-family: "the hierarchical sibling that CLOSES the Data category — the role=tree data-tree widget completing Table (2D) + List (1D) + Tree (hierarchical); inherits the Accordion disclosure model, is List + expand/collapse, resolves Table's treegrid; borders Side Navigation (disclosure-nav)"
  evolution:
    - "the role=tree over-reach -> the disclosure-nav-is-not-a-tree clarification (Side Nav + APG)"
    - "the treegrid for hierarchical tables"
    - "virtualization + the flatten-the-visible-tree + aria-level/setsize/posinset (Fluent flat tree)"
    - "the tri-state cascading checkbox tree settling (permissions/folder selection)"
    - "the headless virtualized tree libs (react-arborist/react-complex-tree) + React-Aria/Primer raising the a11y bar"
  unverified:
    - "external 2026 version numbers across the surveyed systems (MUI X RichTreeView tier, React Aria tree, Ant, Primer TreeView)"
    - "the React Aria / APG treegrid keyboard specifics + the Fluent flat-tree details — verify against current implementations"
    - "MUI X RichTreeView commercial-licensing tier — verify current"
```

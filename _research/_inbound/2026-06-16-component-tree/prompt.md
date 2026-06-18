You are researching the Tree (TreeView) component for a senior design
systems practitioner at a digital agency. The output is a field-truth study
of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Tree /
TreeView is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Tree is THE HIERARCHICAL SIBLING that CLOSES the Data category — the third
and final Data brief, the one that completes Table (2D) + List (1D) + Tree
(hierarchical). It leans on more prior work than anything in the catalogue;
DON'T re-derive the components/patterns it builds on — reference them and
concentrate on the Tree-specific substance:
- IT INHERITS THE EXPAND/COLLAPSE DISCLOSURE MODEL from Accordion/Disclosure
  (components/accordion.md): the per-parent `button aria-expanded` toggle,
  the controlled/uncontrolled expanded state, and the height/reveal
  animation (the calc-size/interpolate-size / native <details> solution
  Accordion landed). Don't re-derive disclosure — apply it recursively.
- IT IS THE HIERARCHICAL SIBLING OF LIST + RESOLVES TABLE'S treegrid
  (components/list.md, table.md): Tree = List + expand/collapse (the node is
  a List item + indentation + a twisty); and role=treegrid (the expandable/
  nested Table row Table deferred to here) = a tree WITH columns. Resolve
  the role=tree vs role=treegrid split from Tree's side.
- IT BORDERS Side Navigation (components/side-navigation.md, which drew the
  boundary): SideNav established "Disclosure-not-role=menu" for nav and the
  role=tree-ONLY-for-data-trees rule. A NAV hierarchy (a docs sidebar, a
  file-browser nav) is <nav> + nested <ul> + aria-expanded DISCLOSURE, NOT
  role=tree. Resolve this from Tree's side: role=tree is for a DATA-tree
  WIDGET (select/operate on a hierarchy), not navigation.
- IT COMPOSES Icon (the twisty chevron + folder/file icons), Checkbox (the
  tri-state cascading selection), Empty State + Skeleton (loading/empty),
  and the List item anatomy (components/icon.md, checkbox.md, empty-state.md,
  skeleton.md).

THE DEFINING TREE-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE role=tree vs role=treegrid vs DISCLOSURE-NAV DECISION (the headline —
  the over-reach trap, parallel to Table's role=grid / Menu's role=menu /
  List's listbox-vs-gridlist): (1) role=tree — a single-column hierarchical
  selection/operation WIDGET (a file tree, a folder picker), the APG Tree
  pattern; (2) role=treegrid — a tree WITH columns (the hierarchical/
  expandable Table row), two-axis nav; (3) the nested-<ul> + aria-expanded
  DISCLOSURE (a NAV hierarchy — NOT a role=tree widget; the Side Navigation
  pattern). Resolve: role=tree ONLY for a genuine data-tree widget; a nav
  hierarchy is disclosure, never role=tree (the most-misused-after-role=grid).
- THE APG TREE KEYBOARD MODEL (the deepest part — the hardest keyboard model
  after the data grid): ONE tab stop + roving tabindex/aria-activedescendant;
  Up/Down move through the VISIBLE (expanded, flattened) nodes; RIGHT
  (collapsed -> expand; expanded -> first child; leaf -> nothing); LEFT
  (expanded -> collapse; collapsed/leaf -> parent); Home/End; typeahead; `*`
  (expand all sibling nodes); Enter/Space (activate/select). Resolve the full
  contract.
- THE ARIA HIERARCHY PROPERTIES + VIRTUALIZATION (the structure-to-AT crux):
  aria-expanded (parent state), aria-level (depth), aria-setsize/
  aria-posinset (position within siblings) on each treeitem — and how
  VIRTUALIZATION forces FLATTENING the visible/expanded tree into a windowed
  list while the aria-level/setsize/posinset preserve the hierarchy for AT
  (the flatten-the-visible-tree technique; the Fluent "flat tree" perf
  approach). Resolve the virtualization-vs-hierarchy tension.
- SELECTION + THE TRI-STATE CASCADING CHECKBOX TREE (the selection crux):
  single-select (a picker) vs multi-select (aria-multiselectable) vs the
  CHECKBOX TREE where a parent reflects its children — checked / unchecked /
  INDETERMINATE (the Checkbox brief's indeterminate) — and checking a parent
  CASCADES to descendants (the classic permissions/folder tree). Resolve the
  cascade + tri-state propagation logic + the a11y (the checkbox is the
  selection, the treeitem the structure).
- THE NODE ANATOMY + EXPAND MECHANICS: the tree node (indentation/guide-lines
  per level, the expand/collapse twisty/chevron, the leading folder/file
  Icon, the label, trailing actions/badge), the LAZY-LOADING of children
  (load-on-expand + the async/loading node state), the expand-all/collapse-
  all, and the depth-indentation + guide-line model.

Field-leader systems to survey (web): WAI-ARIA APG (the Tree View pattern +
the Treegrid pattern — the canonical keyboard model + roles), MUI X
(RichTreeView / SimpleTreeView — selection/multi-select/checkbox/lazy-
loading/virtualization; the Pro tier), Ant Design (Tree — checkable/
draggable/virtual + Tree.DirectoryTree), Adobe Spectrum / React Aria (Tree /
TreeView — the accessible collection-model tree), GitHub Primer (TreeView —
the repo file-tree, a strong accessible reference), Microsoft Fluent (Tree/
TreeItem — the "flat tree" perf approach), IBM Carbon (TreeView — selectable/
with-icons), Atlassian (@atlaskit/tree — the drag-and-drop tree),
react-arborist / react-complex-tree (the headless virtualized tree
libraries), Base Web (Uber) (TreeView). Reference VS Code / GitHub file
trees where relevant. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits for the Accordion/Disclosure expand-collapse
model, the List-item anatomy + hierarchical-sibling relationship, the Table
treegrid; composes for Icon/Checkbox/Empty-State/Skeleton; note the Side
Navigation disclosure-nav boundary; flag unverified/volatile platform claims
under notes.unverified).

1. Framing — what it is (the hierarchical data-tree widget — select/operate
   on a hierarchy; the Data-category closer completing Table+List+Tree) and
   what it isn't (a nav hierarchy — that's disclosure/Side-Navigation, not
   role=tree; an Accordion — a flat disclosure set, not arrow-navigable; a
   Menu — commands); the role=tree-vs-treegrid-vs-disclosure decision + the
   APG keyboard model + the tri-state checkbox tree up front; why systems
   disagree.
2. Anatomy and parts — the tree container (role=tree/treegrid), the tree
   node (indentation/guide-lines + the twisty/chevron + leading Icon + label
   + trailing), the expand/collapse toggle, the checkbox (tri-state), the
   loading/empty node regions; the flattened-visible model.
3. Properties / API — the tree data (nodes + children, controlled/
   uncontrolled expanded), selection (single/multi/checkbox-cascade),
   expand/collapse + expand-all, lazy-load children, the node renderer
   (icon/label/actions), virtualization, the role (tree/treegrid),
   draggable/reorder.
4. States and variants — node expanded/collapsed/leaf; selected (single/
   multi) + the tri-state parent (checked/unchecked/indeterminate); loading
   (lazy children) / empty; focused (roving); disabled; the directory-tree /
   checkbox-tree / treegrid variants; density.
5. Usage guidance — Tree (a data hierarchy widget — select/operate) vs a
   nested List (static hierarchical content) vs Accordion (a flat disclosure
   set) vs Side Navigation (a nav hierarchy — disclosure) vs Menu (commands);
   the role=tree-only-for-data-trees rule; when treegrid (hierarchical
   columns); when to virtualize; don't-build-nav-as-a-tree.
6. Accessibility — the role=tree/treeitem/group + aria-expanded/level/setsize/
   posinset + aria-selected; the full APG keyboard model (Up/Down visible
   nodes, Right/Left expand-collapse-into-out, Home/End, typeahead, *,
   Enter/Space); the treegrid (role=treegrid + two-axis nav); the checkbox-
   tree (the checkbox is the selection, treeitem the structure, the
   tri-state); virtualization (the flattened tree + aria-level/setsize/
   posinset); the disclosure-nav-is-not-a-tree rule; WCAG SCs (1.3.1, 2.1.1,
   4.1.2, 4.1.3).
7. Content guidelines — the node label, the depth/nesting discipline (don't
   over-nest), the expand/collapse affordance clarity, the checkbox-tree
   labels, the empty/loading copy, the count/badge.
8. Motion and transition — the expand/collapse height/reveal (inherited from
   Accordion — calc-size/interpolate-size), the twisty rotation, the
   lazy-load spinner, reduce-motion; the don't-animate-large-trees rule.
9. Internationalization — RTL (the indentation + the twisty/guide-lines flip
   to the inline-start, the chevron mirrors, logical properties), the label
   expansion + depth, the expand/collapse direction keys (Right/Left swap
   meaning in RTL — the key trap).
10. Naming — Tree / TreeView / TreeGrid / DirectoryTree / RichTreeView /
    SimpleTreeView; the tree-vs-treegrid naming; the practice's default;
    aliases.
11. Implementation notes — the role=tree + the recursive disclosure (the
    Accordion model applied per node); the full APG keyboard model + roving/
    activedescendant; the flatten-the-visible-tree for virtualization +
    aria-level/setsize/posinset; the tri-state cascade (checked/indeterminate
    propagation up + down); lazy-load-on-expand + the async node state; the
    RTL Right/Left key swap; the indentation/guide-line CSS; headless vs
    opinionated (react-arborist / RichTreeView).
12. Related and alternative components — typed relationships (INHERITS the
    Accordion/Disclosure expand-collapse; the hierarchical sibling of List;
    resolves Table's treegrid; COMPOSES Icon/Checkbox/Empty-State/Skeleton;
    the Side-Navigation disclosure-nav boundary; the Menu commands boundary).
13. Field POV evolution — the role=tree over-reach -> the disclosure-nav-is-
    not-a-tree clarification (Side Nav); the treegrid for hierarchical tables;
    virtualization + the flatten-the-visible-tree + aria-level/setsize/
    posinset; the tri-state cascading checkbox tree; the headless virtualized
    tree libs (react-arborist); React-Aria/Primer raising the tree a11y bar.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Tree is — explain the
role=tree-vs-treegrid-vs-disclosure-nav decision (the over-reach trap), the
full APG tree keyboard model (Up/Down visible nodes, Right/Left expand-
collapse-into-out, *, typeahead), the aria-level/setsize/posinset + the
virtualization-forces-flattening tension, the tri-state cascading checkbox
tree (indeterminate propagation up and down), the lazy-load-on-expand + node
anatomy, and the RTL Right/Left key-swap trap — the substance that makes
Tree the hierarchical sibling closing the Data category.

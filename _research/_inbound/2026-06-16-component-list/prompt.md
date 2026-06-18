You are researching the List component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a List /
listbox is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

List is THE 1D SIBLING OF TABLE — the second Data brief, the simpler
one-dimensional counterpart to Table's two-dimensional matrix. It is also
the content the overlay surfaces already host. DON'T re-derive the
components it composes; reference them and concentrate on the List-specific
substance:
- IT IS THE 1D SIBLING OF TABLE (components/table.md, which deferred to it):
  Table = 2D (a cell's meaning depends on column AND row); List = 1D
  records (each item is a self-contained unit; no cross-column comparison).
  Resolve the list-vs-table boundary from List's side (don't build a
  single-column table; don't force a multi-attribute comparison into a
  list). A list item can be RICH (avatar + title + metadata + actions) and
  still be 1D.
- IT IS THE CONTENT OF THE LISTBOX the overlay surfaces host
  (components/select.md, combobox.md, popover.md): the Select/Combobox
  dropdown listbox IS a selection List in a Popover. Reference that; the
  interactive selection-list genre is the same role=listbox pattern.
- IT COMPOSES the briefed cluster: Avatar/Icon (the leading visual), Badge/
  Tag (trailing metadata), Button/Switch (trailing actions), Checkbox
  (selection), Divider (between items — the Stack divider-between), Empty
  State (no items) + Skeleton (loading items — the terminal-states machine),
  Link (navigation items) (components/avatar.md, icon.md, badge.md, tag.md,
  button.md, switch.md, checkbox.md, divider.md, empty-state.md, skeleton.md,
  link.md). And it BORDERS Menu (the action list — the do/go/choose/read
  disambiguation), Side Navigation (the navigation list), and Tree (the
  hierarchical list — Tree = a List with expand/collapse — not yet briefed).

THE DEFINING LIST-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE SEMANTIC GENRE SPLIT + THE do/go/choose/read DISAMBIGUATION (the
  headline — it decides the a11y model, parallel to Table's <table>/role=grid):
  (1) the STATIC/CONTENT list — <ul>/<ol>/<li> (or <dl>/<dt>/<dd> for
  description/term-definition lists); a list the user READS/scrolls, items
  may contain links/buttons; READING mode; the default. (2) the INTERACTIVE
  SELECTION list (LISTBOX) — role=listbox/option, a keyboard-navigable
  single/multi-select widget (arrow-key nav, roving focus/aria-
  activedescendant, aria-selected); the APG Listbox pattern; "CHOOSE". (3)
  the NAVIGATION list — a <nav> of links ("GO" — see side-navigation). (4)
  the ACTION list — a list of commands, role=menu ("DO" — see menu).
  Resolve the do/go/choose/read decision (the same disambiguation Menu drew,
  applied to lists).
- THE list-style:none SEMANTICS-REMOVAL TRAP (the List-specific a11y crux,
  parallel to Table's display-strips-semantics): in Safari/VoiceOver,
  `list-style: none` on a <ul> REMOVES the list semantics (VoiceOver stops
  announcing "list, N items") — the Scott O'Hara finding. The fix:
  re-assert role="list" on the styled <ul> (you must add back the role you
  styled away). Resolve the rule (design systems strip bullets universally,
  so they MUST re-assert role=list).
- THE LISTBOX-CANT-CONTAIN-INTERACTIVES -> THE GRIDLIST PATTERN (the modern
  finding, parallel to Tag's grid pattern + Table's role=grid): a
  role=listbox/option CANNOT contain interactive children (a button/link
  inside an option is invalid — the same prohibition Tag's grid pattern and
  Table named). So a "list with actions" that is ALSO selectable/navigable
  must use the GRIDLIST pattern (role=grid, each item a row, the interactive
  children in gridcells — React Aria's GridList). Resolve when a list is a
  plain <ul>, a listbox, or a gridlist.
- THE RICH LIST-ITEM ANATOMY (the "media object" / list-with-actions): the
  classic item — leading visual (Avatar/Icon/Checkbox) + primary/secondary
  text (title + description) + trailing (metadata/Badge, actions/Button,
  a chevron, a Switch) — Material's ListItem (ListItemAvatar/ListItemText/
  ListItemSecondaryAction), Primer's ActionList.Item. Resolve the slot model
  + the single/two/three-line density + the leading-visual inset alignment.
- VIRTUALIZATION + SELECTION (shared with Table): long lists (feeds, chat,
  10k items) -> windowing (TanStack Virtual/react-window) + the aria-setsize/
  aria-posinset tension (the list equivalent of Table's aria-rowcount/
  rowindex — declare the TRUE total when items are windowed); and the
  multi-select + bulk-action list (checkbox per item + select-all,
  aria-multiselectable).
- GROUPING / DIVIDERS / DRAG-TO-REORDER: grouped lists (section headers, the
  sticky A/B/C group headers in a contacts list), dividers between items
  (composing Divider — inset vs full-bleed), and the REORDERABLE list
  (drag-to-reorder + the keyboard-reorder alternative — the 2.5.1/2.5.7
  pointer-alternative + the move announcement). The empty/loading states
  (Empty State + Skeleton items — the terminal-states machine).

Field-leader systems to survey (web): Material 3 / MUI (List + ListItem/
ListItemButton/ListItemText/ListItemAvatar/ListItemIcon/
ListItemSecondaryAction — the rich item model + dense), Chakra UI (List/
ListItem/ListIcon), Ant Design (List — meta/pagination/loadmore/grid mode),
Shopify Polaris (ResourceList + ResourceItem — selectable/filterable +
bulk actions; ActionList for menus), GitHub Primer (ActionList — the
links/buttons/selection workhorse + ActionList.Item leading/trailing
visuals — a strong do/go/choose reference), IBM Carbon (structured/
unordered/ordered lists, ContainedList, list of links), Adobe Spectrum /
React Aria (ListBox [selection] + ListView/GridList [the actionable+
selectable GRIDLIST pattern]), Atlassian, Base Web (Uber) (List/ListItem).
WAI-ARIA APG (the Listbox pattern, the list role, the GridList pattern for
lists-with-actions; the list-style:none / role=list trap; aria-setsize/
posinset for virtualization). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use composes for the Avatar/Icon/Badge/Tag/Button/
Switch/Checkbox/Divider/Empty-State/Skeleton/Link cluster, the listbox-
content relationship with Select/Combobox/Popover, and the Table 1D-sibling
boundary; note the Menu/Side-Navigation/Tree borders; flag unverified/
volatile platform claims under notes.unverified).

1. Framing — what it is (the 1D record list — content/selection/navigation/
   action; the simpler sibling of Table) and what it isn't (a Table — 2D; a
   Menu — the action list; a CSS-Grid layout); the semantic genre split +
   the do/go/choose/read disambiguation + the list-style:none trap up front;
   why systems disagree.
2. Anatomy and parts — the list container (ul/ol/dl or role=listbox/grid),
   the list item (leading visual + primary/secondary text + trailing
   metadata/actions/chevron), the group header + divider, the empty/loading
   regions; the selection checkbox.
3. Properties / API — the item model (leading/primary/secondary/trailing
   slots), ordered/unordered/description, the genre (content/listbox/
   gridlist/nav), selection (single/multi), density (1/2/3-line), dividers/
   grouping, virtualization, the item-as-link/button/option, as/asChild.
4. States and variants — content vs listbox vs gridlist vs nav; selected
   (listbox/gridlist) + select-all; item hover/focus/active/disabled;
   loading (skeleton) / empty (empty state); ordered/unordered/description;
   density; grouped; reorderable.
5. Usage guidance — List (1D records) vs Table (2D comparison — the boundary
   from List's side) vs Menu (do — the action list) vs Nav (go) vs a
   description list; the do/go/choose/read decision; when listbox vs gridlist
   vs plain ul; rich-item-still-1D; when to virtualize.
6. Accessibility — the semantic list (ul/ol/li + the list-style:none ->
   role=list re-assertion trap), the listbox pattern (role=listbox/option +
   roving/activedescendant + aria-selected + the no-interactive-children
   rule), the GRIDLIST pattern (role=grid for lists-with-actions — why a
   listbox can't hold a button), the description list (dl/dt/dd),
   virtualization (aria-setsize/posinset), the nav list, WCAG SCs (1.3.1,
   2.1.1, 4.1.2, 2.5.1/2.5.7 for drag-reorder).
7. Content guidelines — the primary/secondary text hierarchy, truncation +
   the line-clamp, the empty-state copy, the group headers, ordered-when-
   sequence-matters, the item accessible name.
8. Motion and transition — item insert/remove/reorder (FLIP), the
   loading->content swap (skeleton), the expand (if hierarchical -> Tree),
   reduce-motion; the don't-animate-long-lists rule.
9. Internationalization — RTL (the leading/trailing slots flip via logical
   properties, the chevron mirrors, ordered-list numerals via Intl); the
   primary/secondary text expansion; the group-header collation.
10. Naming — List / ListBox / ListView / ActionList / ResourceList /
    GridList / List.Item; the content-vs-listbox-vs-gridlist naming; the
    practice's default; aliases.
11. Implementation notes — the ul/ol + the list-style:none -> role=list
    re-assertion; the listbox (roving/activedescendant + the no-interactive-
    children rule) vs the gridlist (role=grid for actionable items); the rich
    item slot model; virtualization + aria-setsize/posinset; the grouped/
    sticky-header list; drag-to-reorder + the keyboard alternative; the
    item-as-link/button polymorphism (asChild); composes the cluster;
    headless vs opinionated.
12. Related and alternative components — typed relationships (COMPOSES
    Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/
    Skeleton/Link; the listbox content of Select/Combobox/Popover; the 1D
    sibling of Table; the Menu [do] / Side-Navigation [go] / Tree
    [hierarchical] borders; the GridList pattern).
13. Field POV evolution — the list-style:none semantics-removal discovery
    (Scott O'Hara) -> role=list re-assertion; the listbox-cant-contain-
    interactives -> the GridList pattern (React Aria); virtualization +
    aria-setsize/posinset; the rich-list-item/media-object standardization;
    the do/go/choose/read disambiguation hardening.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a List is — explain the
semantic genre split + the do/go/choose/read disambiguation (content/listbox/
nav/action), the list-style:none -> role=list re-assertion trap, the listbox-
cant-contain-interactives -> GridList pattern (role=grid for actionable
items), the rich list-item / media-object anatomy + density, virtualization
+ aria-setsize/posinset, and the list-vs-table boundary from List's side
that makes List the 1D sibling.

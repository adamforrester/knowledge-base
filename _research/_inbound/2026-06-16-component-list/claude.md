# List — field-truth study (Claude pass)

## 1. Framing
A List presents a **one-dimensional sequence of records** — items the user reads, scans, selects, or navigates, where each item is a *self-contained unit* (no cross-column comparison). It is the second Data brief and the **simpler 1D sibling of Table**: where Table is a 2D matrix (a cell's meaning depends on its column *and* its row), a List is a single axis of items — even when each item is *rich* (an avatar + a title + metadata + actions), it's still 1D. It is also the content the overlay surfaces host: the **Select/Combobox dropdown listbox is a selection List in a Popover** (see select, combobox, popover).

The headline that decides the accessibility model — parallel to Table's `<table>`/`role=grid` split — is the **semantic genre split and the do/go/choose/read disambiguation** (the same axis Menu drew):
- **The static / content list (READ)** — `<ul>`/`<ol>`/`<li>` (or `<dl>`/`<dt>`/`<dd>` for term-definition); a list the user reads/scrolls, items may contain links/buttons. The default.
- **The selection list / listbox (CHOOSE)** — `role=listbox`/`option`, a keyboard-navigable single/multi-select widget (arrow-key nav, roving focus / `aria-activedescendant`, `aria-selected`). The APG Listbox pattern; the Select/Combobox dropdown content.
- **The navigation list (GO)** — a `<nav>` of links (see side-navigation).
- **The action list (DO)** — a list of commands, `role=menu` (see menu).

Two sharp List-specific traps follow: the **`list-style: none` semantics-removal** trap (styling away the bullets removes the list role in Safari/VoiceOver — §6) and the **listbox-can't-contain-interactives → GridList** rule (a list with *actions* that's also selectable can't be a plain listbox — §6). What it *isn't*: a **Table** (2D comparison — the boundary from List's side: don't build a single-column table, don't force a multi-attribute comparison into a list), a **Menu** (the action list — `role=menu`; see menu), or a **CSS Grid layout**. Why systems disagree: the genre split, the rich-item slot model, and the listbox-vs-gridlist choice for actionable items.

## 2. Anatomy and parts
- **the list container** — `<ul>`/`<ol>` (content), `<dl>` (description), `role="listbox"` (selection), or `role="grid"` (the GridList — actionable items); carries the list semantics (and the `role=list` re-assertion when bullets are styled off — §6).
- **the list item** — the unit; the "media object" slot model:
  - **leading visual** — an **Avatar** / **Icon** / a selection **Checkbox** / a drag handle.
  - **primary + secondary text** — the title + an optional description (the 1/2/3-line density — §4).
  - **trailing** — metadata (a timestamp, a **Badge**/**Tag**), actions (a **Button**, an overflow **Menu**), a **Switch** (a settings row), or a **chevron** (navigates/expands).
- **the group header + divider** — a section heading for a grouped list (sticky A/B/C headers in a contacts list) + **Divider**s between items (inset vs full-bleed — see divider).
- **the empty / loading regions** — the **Empty State** (no items) and **Skeleton** loading items (the terminal-states machine — see empty-state, skeleton).
- **the (absence of) chrome** — a List is structure, not a surface; a list *of* Cards is a Grid/Stack of Cards, not a List's job (a list item is a row, not a card — though the responsive stacked-table row blurs this).

## 3. Properties / API
- **the item model (the slot API)** — `leading` (avatar/icon/checkbox) + `primary`/`secondary` (title/description) + `trailing` (metadata/actions/switch/chevron); MUI's `ListItemAvatar`/`ListItemText`/`ListItemSecondaryAction`, Primer's `ActionList.Item` with leading/trailing visuals.
- **`as` / element** — `ul` / `ol` / `dl` (the semantic container); ordered when sequence matters (§ content).
- **the genre** — content / **listbox** (selection) / **gridlist** (actionable+selectable) / nav (links); drives the role + the keyboard model (§6).
- **the item-as** — each item is a **link** (`<a>` — navigation), a **button** (`<button>` — action), an **option** (`role=option` — selection), or **static** (text/read) — the per-item interactivity (the `do/go/choose/read` applied per item).
- **selection** — `selectionMode` (none/single/multiple), `selectedKeys`, `onSelectionChange`; the per-item Checkbox + select-all (composes Checkbox — see checkbox).
- **density** — single-line / two-line / three-line (Material) — the item height + the leading-visual inset.
- **dividers / grouping** — `dividers` (between items, composing Divider), `sections`/groups (a heading per group), sticky group headers.
- **virtualization** — windowing for long lists + the `aria-setsize`/`aria-posinset` it requires (§6).
- **reorderable** — drag-to-reorder + the keyboard-reorder alternative (§6/§11).
- **`asChild`** — inherited polymorphism (the item-as-link/button — see box, button, link).
- **what it withholds** — no chrome (that's Card), no 2D columns (that's Table).

## 4. States and variants
- **States:** **item** — default / hover / focus (roving in a listbox/gridlist) / **selected** (`aria-selected` + a tint, listbox/gridlist) / active / disabled; **list** — **loading** (Skeleton items) / **empty** (Empty State) / populated (the terminal-states machine); **selection** — none / some / all (select-all).
- **Variants:**
  - **genre:** content (`<ul>`/`<ol>`) / listbox (selection) / gridlist (actionable+selectable) / nav (links) / description (`<dl>`).
  - **order:** unordered (`<ul>`) / ordered (`<ol>`).
  - **density:** single-line / two-line / three-line; comfortable / compact.
  - **grouped** (section headers, sticky) vs flat.
  - **with-dividers** vs dividerless (spacing-only).
  - **reorderable** vs static.

## 5. Usage guidance
- **Use a List for 1D records** — a feed, a settings list, an inbox, a contacts list, search results, a notifications list, the options in a dropdown. The test: is each item a *self-contained unit* the user scans/selects/acts-on individually (not compared across columns)? Yes → List.
- **List vs the alternatives:**
  - **vs Table** — the boundary from List's side: Table is 2D (cross-column comparison — sortable columns, aligned attributes); List is 1D (self-contained items). **Don't build a single-column table** (use a List); **don't force a multi-attribute comparison into a list** (use a Table). A rich list item (avatar + title + metadata + actions) is still 1D — richness isn't 2D-ness.
  - **vs a Grid of Cards** — heterogeneous, visual, browse-mode → a Grid of Cards (see grid, card); homogeneous, dense, scannable, linear → a List.
  - **vs a Menu** — a list of *commands* the user invokes (do) → a **Menu** (`role=menu`; see menu); a list the user *reads/selects* → a List.
  - **vs a description list** — single-entity key-value/term-definition pairs → `<dl>`/`<dt>`/`<dd>`.
- **The do/go/choose/read decision (the load-bearing one):** *read* → a plain `<ul>`/`<ol>`; *choose* (select a value) → a **listbox**; *go* (navigate) → a **nav** of links; *do* (invoke a command) → a **Menu**. Pick the role from the *intent*, the same disambiguation Menu and Side Navigation drew.
- **Listbox vs gridlist vs plain `<ul>`:** plain `<ul>` for read-only content (even with links/buttons inside — they're individually tabbable); **listbox** for selecting from non-interactive options; **gridlist** when items are *both* selectable/navigable *and* contain their own actions (§6).
- **When to virtualize** — only for *long* lists (hundreds+); it adds the `aria-setsize`/`posinset` discipline (§6), so don't default it for a short list.

## 6. Accessibility
The genre decides the model (§1), and List has two sharp, List-specific traps.

- **The semantic content list + the `list-style: none` trap (the headline a11y crux).** A `<ul>`/`<ol>` conveys "list, N items" to AT. But **Safari/VoiceOver removes the list semantics when `list-style: none` is applied** (the bullets *are* the semantic cue to WebKit — Scott O'Hara's finding). Since design systems strip bullets *universally*, they **must re-assert `role="list"`** on the styled `<ul>` (and `role="listitem"` if the children are also restyled away) — you add back the role you styled away. The single most common List a11y bug.
- **The listbox pattern (selection).** `role="listbox"` + `role="option"` children; **one tab stop** + arrow-key navigation (roving tabindex or `aria-activedescendant`), `aria-selected` per option, `aria-multiselectable` for multi-select. **The no-interactive-children rule:** an `option` **cannot contain** interactive elements (a button/link inside an option is invalid — the same prohibition Tag's grid pattern and Table named). So a listbox option is a *leaf* — selectable text, not a mini-toolbar.
- **The GridList pattern (the modern finding — lists with actions).** When a list item is *both* part of a selectable/navigable collection *and* contains its own interactive children (a "remove" button, a secondary link, a Switch), it **can't be a listbox** (no interactives in options) — it uses the **GridList** pattern: `role="grid"` (single column), each item a `role="row"`, the item's content + actions in `role="gridcell"`s, arrow-key navigation between rows + into the cells (React Aria's GridList). The same `role=grid` trick Tag's removable group and Table use — for the same reason. *This is the resolution of "how does a list-with-actions stay keyboard-navigable."*
- **The description list** — `<dl>`/`<dt>`/`<dd>` for term-definition / key-value pairs (a detail panel); AT announces the term/definition association.
- **Virtualization — `aria-setsize`/`aria-posinset` (shared with Table's `aria-rowcount`/`rowindex`).** Windowing renders only visible items, so AT would announce "1 of 15" for a 10,000-item list; declare **`aria-setsize`** (the true total) + **`aria-posinset`** (each item's true position) on the items; manage focus when the focused item unmounts on scroll.
- **The navigation list** — `<nav aria-label>` + a `<ul>` of links (the `aria-current` for the active item — see side-navigation).
- **Drag-to-reorder** — the pointer drag needs a **keyboard alternative** (a move-up/down action or a grab-then-arrow model — WCAG 2.5.1 Pointer Gestures / 2.5.7 Dragging Movements) and a polite announcement of the new position.
- **WCAG SCs:** **1.3.1** (info & relationships — the list structure, the role=list re-assertion), **2.1.1** (keyboard — listbox/gridlist nav, reorder), **4.1.2** (name/role/value — `aria-selected`, the option/gridcell roles), **2.5.1 / 2.5.7** (the drag-reorder keyboard alternative), **4.1.3** (status messages — the reorder/selection announcement).

## 7. Content guidelines
- **The primary/secondary hierarchy** — the title (primary, the scannable identity) + an optional description (secondary, muted); keep the primary short and front-loaded.
- **Truncation** — single-line items truncate with ellipsis; multi-line items use `-webkit-line-clamp` (the Table/Card discipline); long content shouldn't blow out the row.
- **The item accessible name** — for a selectable/navigable item, the accessible name is the primary text (+ key secondary context); don't bury it under a leading-visual `alt` or leave it to a vague "item".
- **Group headers** — a grouped list's section headings are real headings (or `aria-label` on the group); specific, not "Group 1".
- **Ordered when sequence matters** — `<ol>` for steps/rankings/sequence; `<ul>` when order is incidental; the choice is semantic, not visual.
- **The empty-state copy** — the no-items state uses an **Empty State** with genre-appropriate copy (see empty-state); never a blank list.

## 8. Motion and transition
- **Item insert / remove / reorder** — a list mutating (an item added/deleted/reordered) reflows; a **FLIP** animation smooths a *short* list (the technique Stack/Grid/Table/Tag share — see stack), but **don't animate long/virtualized lists** (jank + windowed items) — the same restraint Table uses.
- **The loading→content swap** — Skeleton items crossfade to real items on load (shape-matched, no CLS — see skeleton).
- **Expand/collapse** — a hierarchical list (nested `<ul>`) expanding is the Tree/Accordion height-animation (see accordion); plain lists don't expand.
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops insert/reorder/expand to instant; the content is the information, not the motion.

## 9. Internationalization
- **RTL** — the leading/trailing slots flip via logical properties (the leading avatar moves to the right, trailing actions to the left), and the navigates/expands **chevron mirrors** (inherited from Box's logical-property substrate — see box); no JS.
- **Ordered-list numerals** — `<ol>` markers localize (Eastern Arabic numerals, etc.) per the locale.
- **Primary/secondary text expansion** — translated titles/descriptions run longer; the item height must tolerate wrapping (and the line-clamp must not clip mid-word).
- **Group-header collation** — alphabetical group headers (the A/B/C contacts split) must use locale-aware collation (`Intl.Collator`), not ASCII sort.

## 10. Naming
- **The field set:** **`List` + `ListItem`** (the content list — MUI, Chakra, Carbon, Base Web); **`ListBox`** (Spectrum/React Aria — the selection list); **`ListView` / `GridList`** (React Aria — the actionable+selectable list, the GridList pattern); **`ActionList`** (GitHub Primer — the links/buttons/selection workhorse, a strong do/go/choose reference); **`ResourceList` + `ResourceItem`** (Polaris — the selectable/filterable resource list with bulk actions; + `ActionList` for menus); the basic `List` with a `grid`/`pagination`/`loadmore` mode (Ant).
- **The practice's default — name by the genre:** **`List`** (+ `List.Item`) for the semantic content list (the default), **`ListBox`** (+ `ListBox.Option`) for the selection widget (the Select/Combobox content), and recognize the **GridList** as the pattern for actionable+selectable items (it can be a `List` variant with the grid role under the hood, or a named `GridList`). The action list is **Menu** (`role=menu`, named separately — see menu); the navigation list is **Side Navigation** / a `<nav>`. Polaris's `ResourceList` (a featured, selectable, filterable List) is a defensible composed pattern on top of `List`.
- **Aliases to map:** ListBox, ListView, GridList, ActionList, ResourceList, ResourceItem, List.Item, ListItem.

## 11. Implementation notes
- **The `<ul>`/`<ol>` + the `list-style: none` → `role=list` re-assertion** (the foundational a11y fix): when the DS strips bullets (`list-style: none`), re-add `role="list"` to the `<ul>` (Safari/VoiceOver drops the semantics otherwise); if the `<li>`s are also restyled with `display` that strips their role, re-assert `role="listitem"`. Bake this into the base List so consumers can't forget.
- **The listbox vs the gridlist (the interactivity fork):** a **listbox** (`role=listbox`/`option`, roving tabindex or `aria-activedescendant`) for selecting from *leaf* options (no interactive children); a **gridlist** (`role=grid`/`row`/`gridcell`) the moment items contain their own actions — because an `option` can't hold a button (the same nested-interactive prohibition Tag/Table named). Pick by whether the item has inner interactives.
- **The rich-item slot model** — `leading`/`primary`/`secondary`/`trailing` slots; the leading-visual inset aligns the text column across items (a fixed leading-column width so titles line up regardless of avatar/icon presence); the 1/2/3-line density sets the item min-height.
- **Virtualization + `aria-setsize`/`posinset`** — window the items (TanStack Virtual / react-window); declare `aria-setsize` (true total) + `aria-posinset` per rendered item; manage focus when the focused item scrolls out. (The list equivalent of Table's `aria-rowcount`/`rowindex`.)
- **Grouped / sticky-header lists** — a `<ul>` per group with a heading, or one `<ul>` with `role="group"` sections; sticky group headers via `position: sticky` (the contacts A/B/C pattern).
- **Drag-to-reorder + the keyboard alternative** — the pointer drag (a drag handle) must have a keyboard equivalent (grab with Space/Enter, move with arrows, drop with Space/Enter — or explicit move-up/down actions) and a polite live-region announcement of the new position (WCAG 2.5.1/2.5.7).
- **The item-as-link/button polymorphism** — an item that navigates is a real `<a href>` (a nav list); an item that acts is a `<button>`; use the `asChild`/Slot polymorphism (see box, link) so the item renders the right element. A whole-item-clickable list row uses the same care as a clickable Card (don't nest interactives — the stretched-link or the gridlist).
- **Composes the cluster** — the slots host Avatar/Icon/Badge/Tag/Button/Switch/Checkbox; dividers are Divider; the empty/loading states are Empty State/Skeleton (see those briefs).
- **Headless vs opinionated** — the selection model, the roving/gridlist keyboard nav, and the virtualization are the headless logic worth owning (shared with Table's engine); the item styling/density is theme.

## 12. Related and alternative components
- **The 1D sibling of:** **Table** (the 2D matrix — Table deferred to List; the list-vs-table boundary is dimensionality: 1D self-contained items vs 2D cross-column comparison — see table).
- **The content of:** the **listbox** the **Select** / **Combobox** dropdowns and **Popover** surfaces host (a selection List in a Popover — see select, combobox, popover).
- **Composes (the cluster):** **Avatar** / **Icon** (leading visual — see avatar, icon), **Badge** / **Tag** (trailing metadata — see badge, tag), **Button** / **Switch** (trailing actions — see button, switch), **Checkbox** (selection — see checkbox), **Divider** (between items — see divider), **Empty State** (no items — see empty-state) + **Skeleton** (loading items — see skeleton), **Link** (navigation items — see link).
- **Borders:** **Menu** (the action list — `role=menu`, "do" — see menu), **Side Navigation** (the navigation list — "go" — see side-navigation), **Tree** (the hierarchical list — Tree = a List with expand/collapse / `role=tree` — not yet briefed).
- **Alternative to:** a **Table** (2D), a **Grid of Cards** (visual/heterogeneous — see grid, card), a **description list `<dl>`** (single-entity key-value).

(The 1D sibling of Table — the one-dimensional record list across content/selection/navigation/action genres, and the content the overlay listboxes host. It composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link. See table for the 2D sibling + the list-vs-table boundary, select/combobox/popover for the listbox-host relationship, avatar/badge/tag/checkbox/divider for the composed parts, menu/side-navigation for the do/go borders, tree when briefed for the hierarchical sibling. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The `list-style: none` semantics-removal discovery → `role=list` re-assertion.** Scott O'Hara's finding that WebKit/VoiceOver drops list semantics when bullets are styled off forced design systems (which strip bullets universally) to re-assert `role="list"` — now a settled baseline.
2. **The listbox-can't-contain-interactives → the GridList pattern.** The recognition that an `option` can't hold a button/link (nested-interactive) drove React Aria's **GridList** (`role=grid` for actionable+selectable lists) — the same `role=grid` resolution Tag's removable group and Table reached, generalized to lists.
3. **Virtualization + `aria-setsize`/`posinset`.** Windowing made huge lists (feeds, chat) performant, and the set-size/position discipline emerged to keep them honest to AT.
4. **The rich-list-item / media-object standardization.** The leading-visual + primary/secondary + trailing slot model (Material's ListItem, Primer's ActionList.Item) became the shared anatomy.
5. **The do/go/choose/read disambiguation hardening.** The field separated the content list (read), the listbox (choose), the nav list (go), and the action menu (do) — the same intent-based disambiguation Menu and Side Navigation drew, applied to lists.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Material 3 / MUI — `List` + `ListItem`/`ListItemButton`/`ListItemText`/`ListItemAvatar`/`ListItemIcon`/`ListItemSecondaryAction` (the rich item model + `dense`).
- Chakra UI — `List`/`ListItem`/`ListIcon`.
- Ant Design — `List` (`meta`, pagination/load-more, grid mode).
- Shopify Polaris — `ResourceList` + `ResourceItem` (selectable/filterable + bulk actions); `ActionList` (menus).
- GitHub Primer — `ActionList` (the links/buttons/selection workhorse; `ActionList.Item` leading/trailing visuals) — a strong do/go/choose reference.
- IBM Carbon — structured/unordered/ordered lists; `ContainedList`; the list of links.
- Adobe Spectrum / React Aria — `ListBox` (selection) + `ListView`/`GridList` (the actionable+selectable GridList pattern).
- Atlassian — list patterns.
- Base Web (Uber) — `List` / `ListItem`.
- Scott O'Hara — the `list-style: none` semantics-removal finding (the `role=list` re-assertion).
- WAI-ARIA APG — the Listbox pattern, the `list` role, the **GridList pattern** (lists with actions); `aria-setsize`/`aria-posinset` for virtualization.
- WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 2.5.1, 2.5.7, 4.1.3.

## 15. Agent-consumable schema
```yaml
identity:
  id: list
  name: List
  aliases: [ListBox, ListView, GridList, ActionList, ResourceList, ResourceItem, List.Item, ListItem]
  category: data
  status: stable
description: >
  The one-dimensional sequence of records — items the user reads/selects/navigates/acts-on,
  each a self-contained unit (no cross-column comparison); the simpler 1D SIBLING of Table
  (Table = 2D matrix; List = 1D, even when items are rich). Also the content the overlay
  surfaces host (the Select/Combobox dropdown listbox is a selection List in a Popover).
  NOT a Table (2D comparison), NOT a Menu (the action list, role=menu), NOT a CSS Grid
  layout. The headline: the semantic genre split + the do/go/choose/read disambiguation
  (content <ul>/listbox/nav/menu) decides the a11y model; two sharp traps — list-style:none
  removes the list role (re-assert role=list), and a listbox can't hold interactives (-> the
  GridList pattern). Composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/
  Empty-State/Skeleton/Link.
anatomy:
  parts:
    - "the list container: <ul>/<ol> (content), <dl> (description), role=listbox (selection), or role=grid (GridList — actionable items); carries the list semantics (+ the role=list re-assertion when bullets are styled off)"
    - "the list item (the 'media object' slots): leading visual (Avatar/Icon/Checkbox/drag-handle) + primary+secondary text (title/description, 1/2/3-line) + trailing (metadata/Badge/Tag, actions/Button/Menu, a Switch, or a chevron)"
    - "the group header + divider: a section heading (sticky A/B/C) + Dividers between items (inset vs full-bleed)"
    - "the empty/loading regions: Empty State (no items) + Skeleton loading items (the terminal-states machine)"
    - "the (absence of) chrome: structure not a surface (a list OF Cards is a Grid/Stack of Cards, not a List's job)"
api:
  composes: [avatar, icon, badge, tag, button, switch, checkbox, divider, empty-state, skeleton, link]
  listbox-content-of: [select, combobox, popover]
  props:
    - {name: "item model (leading/primary/secondary/trailing slots)", type: slots, default: ~, required: false, description: "MUI ListItemAvatar/Text/SecondaryAction; Primer ActionList.Item leading/trailing"}
    - {name: as, type: "'ul'|'ol'|'dl'", default: ul, required: false, description: "the semantic container; ol when sequence matters"}
    - {name: genre, type: "'content'|'listbox'|'gridlist'|'nav'", default: content, required: false, description: "drives the role + keyboard model (the do/go/choose/read disambiguation)"}
    - {name: item-as, type: "'link'|'button'|'option'|'static'", default: static, required: false, description: "per-item interactivity (go/do/choose/read) — a real <a>/<button>/role=option"}
    - {name: selection, type: "selectionMode (none|single|multiple) + selectedKeys + onSelectionChange", default: none, required: false, description: "per-item Checkbox + select-all (composes Checkbox)"}
    - {name: density, type: "'single-line'|'two-line'|'three-line' | 'comfortable'|'compact'", default: comfortable, required: false}
    - {name: "dividers/grouping", type: "boolean | sections", default: false, required: false, description: "dividers between items (Divider); grouped sections + sticky headers"}
    - {name: virtualization, type: boolean, default: false, required: false, description: "window long lists + the aria-setsize/posinset it requires"}
    - {name: reorderable, type: boolean, default: false, required: false, description: "drag-to-reorder + the keyboard-reorder alternative"}
    - {name: asChild, type: boolean, default: false, required: false, description: "the item-as-link/button polymorphism"}
  withholds: "no chrome (that's Card), no 2D columns (that's Table)"
states:
  item: [default, hover, focus, selected, active, disabled]   # focus = roving in a listbox/gridlist; selected = aria-selected + tint
  list: [loading, empty, populated]                           # the terminal-states machine
  selection: [none, some, all]
variants:
  genre: [content, listbox, gridlist, nav, description]
  order: [unordered, ordered]
  density: [single-line, two-line, three-line, comfortable, compact]
  grouping: [flat, grouped-sticky]
  dividers: [with-dividers, dividerless]
  reorderable: [static, reorderable]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "2.5.1", "2.5.7", "4.1.3"]
  list-style-none-trap: "Safari/VoiceOver REMOVES the list semantics when list-style:none is applied (the bullets ARE the cue to WebKit — Scott O'Hara). Design systems strip bullets UNIVERSALLY, so they MUST re-assert role=list on the styled <ul> (+ role=listitem if the <li>s are restyled). The single most common List a11y bug"
  listbox-pattern: "role=listbox + role=option; ONE tab stop + arrow-key nav (roving tabindex / aria-activedescendant); aria-selected per option; aria-multiselectable for multi. NO-INTERACTIVE-CHILDREN: an option CANNOT contain a button/link (the nested-interactive prohibition Tag/Table named) — an option is a LEAF"
  gridlist-pattern: "the modern finding — when an item is BOTH selectable/navigable AND contains its own actions (a remove button/secondary link/Switch), it CAN'T be a listbox -> role=grid (single column), each item a row, content+actions in gridcells, arrow-key nav between rows + into cells (React Aria GridList). The same role=grid trick Tag's removable group + Table use — the resolution of 'how a list-with-actions stays keyboard-navigable'"
  description-list: "<dl>/<dt>/<dd> for term-definition / key-value pairs (the term/definition association announced)"
  virtualization: "windowing -> AT says '1 of 15' for 10,000; declare aria-setsize (true total) + aria-posinset (true position) per item; manage focus when the focused item unmounts (the list equivalent of Table's aria-rowcount/rowindex)"
  nav-list: "<nav aria-label> + a <ul> of links + aria-current for the active item (see side-navigation)"
  drag-reorder: "the pointer drag needs a KEYBOARD alternative (grab+arrows or move-up/down) + a polite position announcement (WCAG 2.5.1/2.5.7)"
content:
  primary-secondary: "the title (primary, scannable, front-loaded) + an optional muted description (secondary)"
  truncation: "single-line ellipsis / multi-line -webkit-line-clamp; long content doesn't blow out the row"
  item-name: "the accessible name is the primary text (+ key secondary); don't bury it under a leading-visual alt or a vague 'item'"
  group-headers: "real headings (or aria-label on the group); specific, not 'Group 1'"
  ordered-when-sequence: "<ol> for steps/rankings/sequence; <ul> when order is incidental — a SEMANTIC choice"
  empty-copy: "the no-items state uses Empty State with genre-appropriate copy; never a blank list"
motion:
  insert-remove-reorder: "a mutating list reflows; FLIP smooths a SHORT list (shared with Stack/Grid/Table/Tag), but DON'T animate long/virtualized lists (jank + windowed items)"
  loading-swap: "Skeleton items crossfade to real items (shape-matched, no CLS)"
  expand: "a hierarchical list (nested <ul>) expanding is the Tree/Accordion height-animation; plain lists don't expand"
  reduce-motion: "drop insert/reorder/expand to instant; the content is the information, not the motion"
i18n:
  rtl: "the leading/trailing slots flip via logical properties (leading avatar -> right, trailing actions -> left); the chevron mirrors (inherited from Box); no JS"
  ordered-numerals: "<ol> markers localize (Eastern Arabic numerals etc.) per locale"
  text-expansion: "translated primary/secondary run longer; item height tolerates wrapping, line-clamp doesn't clip mid-word"
  group-collation: "alphabetical group headers use locale-aware Intl.Collator, not ASCII sort"
implementation:
  - "the <ul>/<ol> + the list-style:none -> role=list re-assertion: re-add role=list to the styled <ul> (Safari/VoiceOver drops the semantics); re-assert role=listitem if the <li>s are display-restyled; bake into the base List so consumers can't forget"
  - "listbox vs gridlist (the interactivity fork): listbox (role=listbox/option, roving/activedescendant) for LEAF options (no interactive children); gridlist (role=grid/row/gridcell) the moment items contain their own actions (an option can't hold a button — the nested-interactive prohibition). Pick by whether the item has inner interactives"
  - "the rich-item slot model: leading/primary/secondary/trailing; a fixed leading-column width aligns the text column across items; the 1/2/3-line density sets the item min-height"
  - "virtualization + aria-setsize/posinset (TanStack Virtual/react-window): true total + true position per rendered item; manage focus when the focused item scrolls out"
  - "grouped/sticky-header lists: a <ul> per group with a heading (or one <ul> + role=group sections); sticky headers via position:sticky (the contacts A/B/C pattern)"
  - "drag-to-reorder + the keyboard alternative: pointer drag (a handle) + a keyboard equivalent (grab Space/Enter, move arrows, drop) + a polite position announcement (WCAG 2.5.1/2.5.7)"
  - "the item-as-link/button polymorphism: a navigating item is a real <a href>, an acting item a <button> (asChild/Slot); a whole-item-clickable row uses the Card stretched-link care (don't nest interactives) or the gridlist"
  - "composes the cluster: the slots host Avatar/Icon/Badge/Tag/Button/Switch/Checkbox; dividers are Divider; empty/loading are Empty State/Skeleton"
  - "headless vs opinionated: the selection model + the roving/gridlist keyboard nav + virtualization are the headless logic (shared with Table's engine); the item styling/density is theme"
composition:
  sibling-of: [table]                      # the 1D vs 2D boundary (Table deferred to List)
  listbox-content-of: [select, combobox, popover]
  composes: [avatar, icon, badge, tag, button, switch, checkbox, divider, empty-state, skeleton, link]
  borders: [menu, side-navigation, tree]   # do (action list) / go (nav list) / hierarchical (Tree = List + expand/collapse) — Tree not yet briefed
  alternative-to: [table, "grid-of-cards", "description-list <dl>"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the genre naming: List (content) / ListBox (selection) / GridList (actionable+selectable) / ActionList (Primer's links/buttons/selection workhorse) — the practice names by genre (List + ListBox + recognize GridList; the action list is Menu)"
    - "listbox vs gridlist for actionable items (the no-interactive-children rule forces gridlist)"
    - "ResourceList (Polaris — featured selectable/filterable) as a composed pattern on List"
    - "the rich-item slot model (leading/primary/secondary/trailing) vs a monolithic item"
  trap:
    - "list-style:none removing the list semantics (re-assert role=list) — the most common List a11y bug"
    - "a button/link inside a listbox option (nested-interactive invalid -> use the gridlist)"
    - "virtualization breaking the set size (needs aria-setsize/posinset); focus lost when the focused item unmounts"
    - "building a single-column table (-> List) / forcing a 2D comparison into a list (-> Table); a list OF Cards as a List (-> Grid/Stack of Cards)"
    - "drag-to-reorder with no keyboard alternative (2.5.1/2.5.7); animating a long/virtualized list (jank)"
    - "a whole-item-clickable row nesting interactives (stretched-link care or the gridlist)"
  inherited: "composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link; the listbox content of Select/Combobox/Popover; the terminal-states machine from Empty State/Skeleton; the role=grid trick from Tag/Table; the do/go/choose/read disambiguation from Menu"
  role-in-family: "the 1D sibling of Table — the one-dimensional record list across content/selection/navigation/action genres; the content the overlay listboxes host; borders Menu (do)/Side-Navigation (go)/Tree (hierarchical)"
  evolution:
    - "the list-style:none semantics-removal discovery (Scott O'Hara) -> role=list re-assertion"
    - "the listbox-cant-contain-interactives -> the GridList pattern (React Aria; the same role=grid trick as Tag/Table)"
    - "virtualization + aria-setsize/posinset"
    - "the rich-list-item / media-object slot standardization (Material ListItem, Primer ActionList.Item)"
    - "the do/go/choose/read disambiguation hardening (shared with Menu/Side-Navigation)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the React Aria GridList role details + the per-system listbox-vs-gridlist split — verify against current implementations"
    - "the exact Safari/VoiceOver list-style:none behavior across current versions — verify"
```

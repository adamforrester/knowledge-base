---
okf_version: "0.1"
type: component-brief
title: List
description: The 1D sibling of Table — a field-truth study of the semantic genre split + the do/go/choose/read disambiguation (content <ul> / listbox / nav / menu — decides the a11y model), the list-style:none → role=list re-assertion trap (Scott O'Hara, 2018), the listbox-can't-contain-interactives → GridList pattern (role=grid for actionable items — the same trick Tag/Table use), the rich list-item / media-object slot anatomy + density, virtualization + aria-setsize/posinset, the aria-selected-vs-aria-current-by-genre nuance, and the list-vs-table boundary from List's side — the content the overlay listboxes host, composing Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link, with the practice's defaults.
tags: [components, data]
category: Data
status: stable
aliases: [ListBox, ListView, GridList, ActionList, ResourceList, ResourceItem, List.Item, ListItem, ContainedList]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# List

> A List presents a **one-dimensional sequence of records** — items the user reads, scans, selects, or navigates, where each item is a *self-contained, independent visual record*. It is the second Data brief and the **simpler 1D sibling of Table**: where Table manages a 2D matrix (a cell's meaning relies on the intersection of its row *and* column), a List manages a linear sequence. A list item can be *rich* (an avatar + structured typography + badges + trailing actions) without violating its 1D nature — *provided the user doesn't scan down vertical columns to compare attributes across rows*; if cross-record column comparison is the task, it's a **Table** (see table). It is also the content the overlay surfaces host: the **Select/Combobox dropdown listbox is a selection List in a Popover** (see select, combobox, popover). The headline that decides the accessibility model — parallel to Table's `<table>`/`role=grid` split — is the **do/go/choose/read disambiguation** (the same axis Menu and Side Navigation drew): **read** (a static content `<ul>`/`<ol>`/`<dl>`), **choose** (a `role=listbox` selection widget), **go** (a `<nav>` of links — see side-navigation), **do** (a `role=menu` action list — see menu). Two sharp List-specific traps follow: the **`list-style: none` semantics-removal** trap (styling away the bullets strips the list role in WebKit/VoiceOver — re-assert `role="list"`) and the **listbox-can't-contain-interactives → GridList** rule (a list with *actions* that's also selectable can't be a plain listbox). What it *isn't*: a **Table** (2D comparison), a **Menu** (the action list — `role=menu`), or a **CSS Grid layout**. Why systems disagree: the genre split, the rich-item slot model, and the listbox-vs-gridlist choice for actionable items.

---

## 1. Framing
A List is the primary 1D record container. Building a resilient one starts by resolving the **do/go/choose/read** disambiguation — a visual "list of items" maps to one of four distinct semantic + keyboard models:
- **READ (static / content list):** semantic `<li>` wrappers a user reads/scrolls/scans. Items may contain nested interactives (a profile link, an edit button), but the list is *not* a monolithic keyboard widget — focus moves sequentially via Tab. The default.
- **CHOOSE (selection list / listbox):** `role="listbox"` + `role="option"` — a single focusable widget in the tab sequence, internal arrow-key navigation (roving tabindex or `aria-activedescendant`), selecting an option updates a value. The APG Listbox pattern; the Select/Combobox dropdown content.
- **GO (navigation list):** a `<nav>` landmark of links, each structurally bound to a URL (see side-navigation).
- **DO (action / menu list):** `role="menu"` + `role="menuitem"` — action dispatch / context menus, with menu-key behaviors (typeahead, Escape — see menu).

Two structural traps define the rest:
- **The `list-style: none` semantics-removal bug** — in WebKit/Safari/VoiceOver, applying `list-style: none` to a `<ul>`/`<ol>` *strips the list role* from the accessibility tree (VoiceOver stops announcing "list, N items"). Since design systems strip bullets universally, they **must re-assert `role="list"`** (§6).
- **The listbox interactive constraint** — a `role="option"` is a *leaf*; it **cannot contain** focusable interactive children (a button/switch inside an option breaks SR navigation — the same prohibition Tag's grid pattern and Table named). A list needing *both* list-level selection *and* nested child actions must upgrade to the **GridList** pattern (`role="grid"`) (§6).

What it *isn't*: a **Table** (2D — the boundary from List's side: don't build a single-column table, don't force a multi-attribute comparison into a list), a **Menu** (the action list), or a **CSS Grid layout**. Why systems disagree: the genre split, the slot model, and the listbox-vs-gridlist choice.

## 2. Anatomy and parts
- **the list container** — `<ul>`/`<ol>` (content), `<dl>` (description), or a `div`/`ul` carrying `role="listbox"` / `role="grid"` (interactive); carries the list semantics (+ the `role=list` re-assertion when bullets are styled off — §6).
- **the group / section header** (`List.Section`/`List.Subheader`) — labels a subset; can stick to the container's top edge on scroll (the contacts A/B/C pattern).
- **the list item** (`List.Item` — `<li>` / `role=option` / `role=row`) — the "media object" slot model along a horizontal axis:
  - **leading slot** — an **Avatar** / **Icon** / a selection **Checkbox** / a drag handle; a *rigid structural width* enforces vertical alignment of the text column across sibling items.
  - **content block** — primary text (the headline, single-line-truncated or wrapped) + optional secondary text (metadata, 2-/3-line clamp).
  - **trailing slot** — status (**Badge**/**Tag**), timestamp, interactive controls (**Button**/**Switch**), or a **chevron** (navigates/expands).
- **the divider** — a **Divider** between items, full-bleed or **inset** to the content-block boundary (leaving the leading visual un-bisected — see divider).
- **the skeleton / empty regions** — **Skeleton** items matching the rich-item layout (loading) and the **Empty State** block (no items) — the terminal-states machine (see skeleton, empty-state).
- **the (absence of) chrome** — a List is structure, not a surface; a list *of* Cards is a Grid/Stack of Cards, not a List's job.

## 3. Properties / API
**Container (`List` / `ListBox` / `GridList`):**
- **`genre`** — `read` / `choose` / `go` / `do` (default `read`); determines the semantic tags, interactive roles, and keyboard manager. The headline prop.
- **`selectionMode`** — `none` / `single` / `multiple` (valid for `choose`, or a `read` list upgraded to a selection interface); the per-item Checkbox + select-all (composes Checkbox — see checkbox).
- **`density`** — `compact` (~32px) / `normal` (~48px) / `spacious` (~64–72px) — row padding/height.
- **`virtualized`** — windowing for long lists (+ the `aria-setsize`/`posinset` it requires — §6).
- **`as` / `asChild`** — polymorphism (`<ul>`→`<ol>`/`<nav>`, or the item-as-link/button — see box).

**Item (`List.Item`):**
- **`selected`** — binds to **`aria-selected`** (listbox/gridlist) *or* **`aria-current="page"`** (nav list) depending on the container's `genre` (the load-bearing nuance — the selected-state attribute *is* genre-dependent).
- **`disabled`** — `aria-disabled` + dimmed + non-focusable.
- **`interactive`** — on a static list, applies focusable hover/active cues.
- **`lines`** — 1 / 2 / 3 (the content-block clamp + the item height).
- **the slots** — `leading` / `primary` / `secondary` / `trailing` (MUI's `ListItemAvatar`/`Text`/`SecondaryAction`; Primer's `ActionList.Item` leading/trailing).
- **the item-as** — a **link** (`<a>`, go), a **button** (action), an **option** (`role=option`, choose), or **static** (read) — per-item interactivity via `asChild`.
- **what it withholds** — no chrome (that's Card), no 2D columns (that's Table).

## 4. States and variants
- **States:** **item** — default / interactive-hover (a ~4% neutral tint) / focus-visible (the ring; roving in listbox/gridlist) / **selected** (`aria-selected`/`aria-current` + an accent track + tint) / active / disabled (~40–50% opacity, `pointer-events: none`); **list** — **loading** (Skeleton items) / **empty** (Empty State) / populated (the terminal-states machine); **selection** — none / some / all.
- **Variants:**
  - **genre:** content (`<ul>`/`<ol>`) / listbox (selection) / gridlist (actionable+selectable) / nav (links) / description (`<dl>`).
  - **order:** unordered (`<ul>`) / ordered (`<ol>`).
  - **density:** compact / normal / spacious; lines 1/2/3.
  - **grouped** (sticky section headers) vs flat.
  - **with-dividers** (inset/full-bleed) vs dividerless.
  - **reorderable** vs static.

## 5. Usage guidance
- **Use a List for 1D records** — a feed, settings, an inbox, contacts, search results, notifications, dropdown options. The test: is each item a *self-contained block* the user scans/selects/acts-on individually (not compared across columns)? Yes → List.
- **List vs the alternatives:**
  - **vs Table** — Table when users compare attributes *down structured columns* (Price / Status / Date side-by-side); List when each record reads like an isolated paragraph or card (details presented as a *nested stack* of secondary lines / metadata tags, not aligned column cells). **Don't build a single-column table; don't force a 2D comparison into a list.** A rich item is still 1D — richness isn't 2D-ness (see table).
  - **vs a Grid of Cards** — heterogeneous/visual/browse → a Grid of Cards (see grid, card); homogeneous/dense/scannable/linear → a List.
  - **vs Menu** — a List (with selection) *selects data records*; a **Menu** *dispatches actions/commands* (`role=menu`). Don't use a Listbox as a system dropdown menu (see menu).
  - **vs a description list** — strict label-value/term-definition pairs for a single entity → `<dl>`/`<dt>`/`<dd>`.
- **The do/go/choose/read decision (the load-bearing one):** pick the role from the *intent* — read → `<ul>`/`<ol>`; choose → listbox; go → nav of links; do → Menu.
- **Listbox vs gridlist vs plain `<ul>`:** plain `<ul>` for read-only content (links/buttons inside are individually tabbable); **listbox** for selecting *leaf* options; **gridlist** when items are *both* selectable/navigable *and* contain their own actions (§6).
- **When to virtualize** — when list size exceeds **~200 items** (rendering hundreds of deep DOM trees with avatars/menus/states degrades scroll perf); it adds the `aria-setsize`/`posinset` discipline (§6), so don't default it for short lists.

## 6. Accessibility
The genre decides the model (§1); two sharp List-specific traps anchor it.

- **The semantic content list + the `list-style: none` trap (the headline crux).** A `<ul>`/`<ol>` conveys "list, N items" + the count to AT. But **WebKit/Safari strips the list role when `list-style: none` is applied** (the bullets *are* the cue to WebKit — Scott O'Hara, 2018). Since design systems strip bullets *universally*, they **must re-assert `role="list"`** on the styled `<ul>` (and `role="listitem"` on the children if those are `display`-restyled away). Bake it into the base List so consumers can't forget. The single most common List a11y bug.
- **The listbox pattern (choose).** `role="listbox"` + `role="option"`; the container is **one tab stop** (`tabindex="0"`); arrow keys cycle (Up/Down), Home/End jump to first/last, Space/Enter select; focus via **roving tabindex** or **`aria-activedescendant`**; `aria-selected="true"`/`"false"` per option (explicit *false* for clarity), `aria-multiselectable="true"` on the container for multi-select. **The interactive constraint:** an `option` is a **leaf** — it cannot contain a button/link/switch (those get stripped of their keyboard roles).
- **The GridList escape hatch (the modern finding — lists with actions).** When a list needs *both* selection/arrow-navigation *and* embedded interactive controls (a button *inside* a row), it **can't be a listbox** — upgrade to **`role="grid"`**: each item a `role="row"`, the row's content + each action wrapped in `role="gridcell"`s; arrow keys navigate two-dimensionally (Up/Down between rows, Left/Right between the row's cells/controls). React Aria's **GridList**. The same `role=grid` resolution Tag's removable group and Table reached — the answer to "how a list-with-actions stays keyboard-navigable."
- **The description list** — `<dl>`/`<dt>`/`<dd>` for term-definition / key-value (the association announced).
- **Virtualization — `aria-setsize`/`aria-posinset`** (shared with Table's `aria-rowcount`/`rowindex`): windowing renders only visible items, so AT would announce "1 of 15" for a 10,000-item set; declare **`aria-setsize`** (true total) + **`aria-posinset`** (true position) on each rendered item; manage focus when the focused item unmounts on scroll.
- **The navigation list** — `<nav aria-label>` + a `<ul>` of links + **`aria-current="page"`** for the active item (the genre-dependent selected attribute — §3; see side-navigation).
- **Accessible naming for actionable items** — a row's "Edit" button needs context: `aria-describedby` linking it to the row's primary-text id, or an explicit `aria-label="Edit user John Smith"` (no ambiguous bare "Edit").
- **Drag-to-reorder** — the pointer drag needs a **keyboard alternative** (§11) + a polite live-region position announcement (WCAG 2.5.1 Pointer Gestures / 2.5.7 Dragging Movements).
- **WCAG SCs:** **1.3.1** (info & relationships — the list structure / the `role=list` re-assertion), **2.1.1** (keyboard — listbox/gridlist nav, reorder), **4.1.2** (name/role/value — `aria-selected`/`aria-current`, the option/gridcell roles), **2.5.1 / 2.5.7** (the drag-reorder keyboard alternative), **4.1.3** (status messages — the reorder/selection announcement).

## 7. Content guidelines
- **Typography hierarchy** — bold, high-contrast primary title; smaller, muted secondary line; keep the primary short and front-loaded (the scannable identity).
- **Truncation** — primary: single-line ellipsis (`text-overflow: ellipsis; white-space: nowrap`) to keep row heights consistent; secondary: `-webkit-line-clamp: 2` for multi-line, with layouts that adapt gracefully when lines wrap (no overlap).
- **The item accessible name** — for selectable/navigable items it's the primary text (+ key secondary); for nested actions, link the control to the row title (`aria-describedby`/explicit label — §6).
- **Group headers** — real headings (or `aria-label` on the group); specific, not "Group 1".
- **Ordered when sequence matters** — `<ol>` for steps/rankings/sequence; `<ul>` when order is incidental — a *semantic* choice.
- **Empty-state copy** — guide the user to populate the list ("No active integrations. Click 'Add Integration' to get started."), not a bare "No items" (see empty-state).

## 8. Motion and transition
- **Item insert / remove / reorder** — use **FLIP** (the technique Stack/Grid/Table/Tag share — see stack) to smooth layout shifts on a *short* list, but **don't animate individual item entry sequentially on long/virtualized lists** (lag + windowed items) — the same restraint Table uses.
- **The loading→content swap** — Skeleton items crossfade to real items (`opacity: 0→1` over ~150ms ease-out), shape-matched (no CLS — see skeleton).
- **Restraint** — keep transitions brief (~150–250ms); expand/collapse of a *hierarchical* list is the Tree/Accordion height-animation (plain lists don't expand — see accordion).
- **Reduce-motion** — `prefers-reduced-motion: reduce` drops insert/reorder/expand and the skeleton pulse to instant; the content is the information, not the motion.

## 9. Internationalization
- **RTL** — use logical properties (`margin-inline-start`, `padding-inline-end`, `text-align: start`); the leading/trailing slots flip (the leading avatar to the right, trailing actions to the left), and the **directional chevron mirrors** (`chevron-right`→`chevron-left`) while brand icons don't (inherited from Box — see box); no JS.
- **Ordered-list numerals** — don't hardcode; CSS counter styles or `Intl.NumberFormat` per locale (Eastern Arabic / Arabic-Indic numerals).
- **Text expansion** — EN→DE/FR can run +30%; item layouts must absorb longer primary/secondary strings without breaking alignment or pushing trailing actions out of view (the line-clamp must not clip mid-word).
- **Group-header collation** — alphabetical group headers (the A/B/C split) use locale-aware `Intl.Collator`, not ASCII sort.

## 10. Naming
- **The field set:** **`List` / `ListItem`** (the static content list — MUI/Material 3, Chakra, Base Web) + **`ListItemButton`** (MUI's interactive item); **`ListBox`** (Spectrum/React Aria — selection); **`ListView` / `GridList`** (React Aria/Spectrum — the actionable+selectable GridList pattern); **`ActionList`** (GitHub Primer — the links/buttons/selection workhorse; a strong do/go/choose reference); **`ResourceList` / `ResourceItem`** (Polaris — selectable/filterable + bulk actions; + `ActionList` for menus); **`UnorderedList` / `ContainedList`** (IBM Carbon).
- **The practice's default — name by the genre:** **`List`** (+ `List.Item`, `List.ItemText`/`Content`, `List.Divider`) for the static content list (the default); **`ListBox`** (+ `ListBox.Option`) for the selection widget (the Select/Combobox content); **`GridList`** for the actionable+selectable pattern (it can be a `List` variant carrying the grid role, or a named `GridList`). The action list is **Menu** (`role=menu`, named separately — see menu); the navigation list is **Side Navigation** / a `<nav>`. Polaris's `ResourceList` (a featured, selectable, filterable List) is a defensible composed pattern on top of `List`.
- **Aliases to map:** ListBox, ListView, GridList, ActionList, ResourceList, ResourceItem, ListItem, List.Item, ContainedList, UnorderedList.

## 11. Implementation notes
- **The `<ul>`/`<ol>` + the `list-style: none` → `role=list` re-assertion** (the foundational fix): when the DS strips bullets/margins/padding, re-add `role="list"` to the `<ul>` and `role="listitem"` to the `<li>`s (WebKit drops the semantics otherwise); bake it into the base List so consumers can't forget.
- **The listbox vs the gridlist (the interactivity fork):** a **listbox** (`role=listbox`/`option`, roving tabindex or `aria-activedescendant`, Home/End/Space/Enter) for *leaf* options; a **gridlist** (`role=grid`/`row`/`gridcell`, 2D arrow nav) the moment items contain their own actions — because an `option` can't hold a button (the nested-interactive prohibition). Pick by whether the item has inner interactives.
- **The rich-item slot model** — `leading`/`primary`/`secondary`/`trailing`; a *fixed leading-column width* aligns the text column across items regardless of avatar/icon presence; `lines` (1/2/3) sets the item min-height.
- **Virtualization + `aria-setsize`/`posinset`** (TanStack Virtual / react-window) — beyond ~200 items; declare `aria-setsize` (true total) + `aria-posinset` (true position) per rendered item; manage focus when the focused item scrolls out. (The list equivalent of Table's `aria-rowcount`/`rowindex`.)
- **Grouped / sticky-header lists** — a `<ul>` per group with a heading (or one `<ul>` + `role="group"` sections); sticky headers via `position: sticky`.
- **Drag-to-reorder + the keyboard alternative (the pattern):** a focusable **drag-handle button** in the row → Space/Enter enters "reorder mode" → Up/Down arrows move the focused item within the array → a polite **`aria-live`** announcement ("Moved [item], now in position 3 of 10") → Space/Enter commits, Escape cancels (WCAG 2.5.1/2.5.7).
- **The item-as-link/button polymorphism** — a navigating item is a real `<a href>`, an acting item a `<button>` — via `asChild`/Slot (Radix `Slot`: `const Comp = asChild ? Slot : 'li'`; see box, link); a whole-item-clickable row uses the Card stretched-link care (don't nest interactives) or the gridlist.
- **Composes the cluster** — the slots host Avatar/Icon/Badge/Tag/Button/Switch/Checkbox; dividers are Divider; the empty/loading states are Empty State/Skeleton.
- **Headless vs opinionated** — the selection model, the roving/gridlist keyboard nav, and virtualization are the headless logic (shared with Table's engine); the item styling/density is theme.

## 12. Related and alternative components
- **The 1D sibling of:** **Table** (the 2D matrix — Table deferred to List; the boundary is dimensionality: 1D self-contained items vs 2D cross-column comparison — see table).
- **The content of:** the **listbox** the **Select** / **Combobox** dropdowns and **Popover** surfaces host (a selection List in a Popover — see select, combobox, popover).
- **Composes (the cluster):** **Avatar** / **Icon** (leading visual — see avatar, icon), **Badge** / **Tag** (trailing metadata — see badge, tag), **Button** / **Switch** (trailing actions — see button, switch), **Checkbox** (selection — see checkbox), **Divider** (between items — see divider), **Empty State** (no items — see empty-state) + **Skeleton** (loading items — see skeleton), **Link** (navigation items — see link).
- **Borders:** **Menu** (the action list — `role=menu`, "do" — see menu), **Side Navigation** (the navigation list — "go" — see side-navigation), **Tree** (the hierarchical list — Tree = a List with expand/collapse / `role=tree` — not yet briefed).
- **Alternative to:** a **Table** (2D), a **Grid of Cards** (visual/heterogeneous — see grid, card), a **description list `<dl>`** (single-entity key-value).

(The 1D sibling of Table — the one-dimensional record list across content/selection/navigation/action genres, and the content the overlay listboxes host. It composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link. See table for the 2D sibling + the list-vs-table boundary, select/combobox/popover for the listbox-host relationship, avatar/badge/tag/checkbox/divider for the composed parts, menu/side-navigation for the do/go borders, tree when briefed for the hierarchical sibling. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The `list-style: none` semantics-removal discovery → `role=list` re-assertion.** Scott O'Hara's **2018** finding that WebKit/Safari strips the list role when bullets are styled off forced design systems (which strip bullets universally) to programmatically re-assert `role="list"`/`role="listitem"` — now a settled baseline.
2. **The move to GridList for actionable items.** Interactive lists were long built as nested HTML inside listbox options; the strict ARIA prohibition (options can't hold interactives) drove **Adobe Spectrum / React Aria (2020+)** to pioneer the **GridList** (`role=grid`) — the same `role=grid` resolution Tag's removable group and Table reached, generalized to lists.
3. **Virtualization + `aria-setsize`/`posinset`** kept huge windowed lists (feeds, chat) honest to AT.
4. **The rich-list-item / media-object standardization** — the leading-visual + primary/secondary + trailing slot model (Material's ListItem, Primer's ActionList.Item) became the shared anatomy.
5. **The do/go/choose/read separation hardening.** Early libraries shipped one generic `List` for everything (nav links to form inputs); modern systems enforce the strict separation — static content (read), selection (choose), nav (go), command menus (do) — via distinct sub-components or an explicit `genre`.

## 14. Sources cited
*(External-pass version dates reconciled; platform-state claims flagged unverified.)*
- Adobe Spectrum / React Aria (v3, 2024) — `ListBox` + `ListView`/`GridList`; the GridList pattern, keyboard navigation.
- Material 3 / MUI (v5.15, 2024) — `List` + `ListItem`/`ListItemButton`/`ListItemText`/`ListItemAvatar`/`ListItemIcon`/`ListItemSecondaryAction`; the rich item model + `dense`.
- GitHub Primer (v36, 2024) — `ActionList` (the links/buttons/selection workhorse; leading/trailing visuals).
- Shopify Polaris (v12, 2024) — `ResourceList` / `ResourceItem` (selectable/filterable + bulk actions); `ActionList` (menus).
- IBM Carbon (v11, 2023) — `UnorderedList` / `OrderedList` / `ContainedList`; the structural list guidelines.
- Chakra UI — `List`/`ListItem`/`ListIcon`.
- Ant Design — `List` (`meta`, pagination/load-more, grid mode).
- Base Web (Uber) — `List` / `ListItem`.
- Scott O'Hara — "Fixing Lists" (the `list-style: none` semantics-loss in WebKit; 2018, updated 2023).
- WAI-ARIA APG — the Listbox pattern, the `list` role, the **GridList pattern** (lists with actions); `aria-setsize`/`aria-posinset` for virtualization.
- WCAG 2.2 — 1.3.1, 2.1.1, 4.1.2, 2.5.1, 2.5.7, 4.1.3.

## 15. Agent-consumable schema
```yaml
identity:
  id: list
  name: List
  aliases: [ListBox, ListView, GridList, ActionList, ResourceList, ResourceItem, List.Item, ListItem, ContainedList]
  category: data
  status: stable
description: >
  The one-dimensional sequence of records — items the user reads/selects/navigates/acts-on,
  each a self-contained block (no cross-column comparison); the simpler 1D SIBLING of Table
  (Table = 2D matrix; List = 1D, even when items are rich). Also the content the overlay
  surfaces host (the Select/Combobox dropdown listbox is a selection List in a Popover).
  NOT a Table (2D comparison), NOT a Menu (the action list, role=menu), NOT a CSS Grid
  layout. The headline: the do/go/choose/read disambiguation (content <ul>/listbox/nav/menu)
  decides the a11y model; two sharp traps — list-style:none removes the list role (re-assert
  role=list), and a listbox option can't hold interactives (-> the GridList role=grid pattern).
  Composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link.
anatomy:
  parts:
    - "the list container: <ul>/<ol> (content), <dl> (description), or role=listbox / role=grid (interactive); carries the list semantics (+ the role=list re-assertion when bullets are styled off)"
    - "the group/section header (List.Section/Subheader): labels a subset; can stick to the container top on scroll (the contacts A/B/C pattern)"
    - "the list item (List.Item — <li>/role=option/role=row), the 'media object' slots: LEADING (Avatar/Icon/Checkbox/drag-handle; rigid width aligns the text column) + CONTENT (primary headline single-line-truncated + secondary 2/3-line clamp) + TRAILING (Badge/Tag, timestamp, Button/Switch, or a chevron)"
    - "the divider: a Divider between items, full-bleed or INSET to the content-block boundary (leaving the leading visual un-bisected)"
    - "the skeleton/empty regions: Skeleton items matching the rich-item layout (loading) + the Empty State block (no items) — the terminal-states machine"
    - "the (absence of) chrome: structure not a surface (a list OF Cards is a Grid/Stack of Cards, not a List's job)"
api:
  composes: [avatar, icon, badge, tag, button, switch, checkbox, divider, empty-state, skeleton, link]
  listbox-content-of: [select, combobox, popover]
  container-props:
    - {name: genre, type: "'read'|'choose'|'go'|'do'", default: read, required: false, description: "determines the semantic tags + interactive roles + keyboard manager (the do/go/choose/read disambiguation) — the headline prop"}
    - {name: selectionMode, type: "'none'|'single'|'multiple'", default: none, required: false, description: "valid for choose (or a read list upgraded to selection); the per-item Checkbox + select-all"}
    - {name: density, type: "'compact'|'normal'|'spacious'", default: normal, required: false, description: "row padding/height ~32 / ~48 / ~64-72px"}
    - {name: virtualized, type: boolean, default: false, required: false, description: "window long lists (+ aria-setsize/posinset)"}
    - {name: as/asChild, type: "ElementType/boolean", default: ul, required: false, description: "polymorphism (ul->ol/nav, or the item-as-link/button)"}
  item-props:
    - {name: selected, type: boolean, default: false, required: false, description: "binds to aria-selected (listbox/gridlist) OR aria-current='page' (nav) depending on the container genre — the genre-dependent selected attribute"}
    - {name: disabled, type: boolean, default: false, required: false, description: "aria-disabled + dimmed + non-focusable"}
    - {name: interactive, type: boolean, default: false, required: false, description: "on a static list, focusable hover/active cues"}
    - {name: lines, type: "1|2|3", default: 1, required: false, description: "the content-block clamp + item height"}
    - {name: item-as, type: "'link'|'button'|'option'|'static'", default: static, required: false, description: "per-item interactivity (go/do/choose/read) via asChild"}
  withholds: "no chrome (that's Card), no 2D columns (that's Table)"
states:
  item: [default, interactive-hover, focus-visible, selected, active, disabled]   # hover ~4% tint; focus = roving in listbox/gridlist; selected = aria-selected/aria-current + accent track; disabled ~40-50% opacity + pointer-events:none
  list: [loading, empty, populated]                                               # the terminal-states machine
  selection: [none, some, all]
variants:
  genre: [content, listbox, gridlist, nav, description]
  order: [unordered, ordered]
  density: [compact, normal, spacious]
  lines: [1, 2, 3]
  grouping: [flat, grouped-sticky]
  dividers: [with-dividers-inset, with-dividers-full-bleed, dividerless]
  reorderable: [static, reorderable]
accessibility:
  wcag-criteria: ["1.3.1", "2.1.1", "4.1.2", "2.5.1", "2.5.7", "4.1.3"]
  list-style-none-trap: "WebKit/Safari REMOVES the list role when list-style:none is applied (the bullets ARE the cue — Scott O'Hara, 2018). DS strip bullets UNIVERSALLY -> MUST re-assert role=list on the styled <ul> (+ role=listitem if the <li>s are display-restyled). Bake into the base List. The single most common List a11y bug"
  listbox-pattern: "role=listbox + role=option; container is ONE tab stop (tabindex=0); Up/Down cycle, Home/End jump, Space/Enter select; focus via roving tabindex / aria-activedescendant; aria-selected true/false per option (explicit false), aria-multiselectable on the container for multi. CONSTRAINT: an option is a LEAF — it CANNOT contain a button/link/switch (stripped of keyboard roles)"
  gridlist-pattern: "the escape hatch — when a list needs BOTH selection/arrow-nav AND embedded interactive controls, it CAN'T be a listbox -> role=grid; each item a role=row, content+each action in role=gridcell; 2D arrow nav (Up/Down rows, Left/Right cells). React Aria GridList — the same role=grid trick Tag's removable group + Table use"
  description-list: "<dl>/<dt>/<dd> for term-definition / key-value (the association announced)"
  virtualization: "windowing -> AT says '1 of 15' for 10,000; declare aria-setsize (true total) + aria-posinset (true position) per rendered item; manage focus when the focused item unmounts (the list equivalent of Table's aria-rowcount/rowindex)"
  nav-list: "<nav aria-label> + a <ul> of links + aria-current='page' for the active item (the genre-dependent selected attribute)"
  actionable-naming: "a row's 'Edit' button needs context: aria-describedby -> the row's primary-text id, or an explicit aria-label='Edit user John Smith' (no bare 'Edit')"
  drag-reorder: "the pointer drag needs a KEYBOARD alternative + a polite live-region position announcement (WCAG 2.5.1/2.5.7)"
content:
  hierarchy: "bold high-contrast primary title + a smaller muted secondary; keep the primary short + front-loaded"
  truncation: "primary single-line ellipsis (consistent row height); secondary -webkit-line-clamp:2 (layouts adapt when lines wrap, no overlap)"
  item-name: "the accessible name = the primary text (+ key secondary); for nested actions link the control to the row title (aria-describedby/explicit label)"
  group-headers: "real headings (or aria-label on the group); specific, not 'Group 1'"
  ordered-when-sequence: "<ol> for steps/rankings/sequence; <ul> when order is incidental — a SEMANTIC choice"
  empty-copy: "guide the user to populate ('No active integrations. Click Add Integration to get started'), not a bare 'No items'"
motion:
  insert-remove-reorder: "FLIP smooths a SHORT list (shared with Stack/Grid/Table/Tag), but DON'T animate individual item entry sequentially on long/virtualized lists (lag + windowed items)"
  loading-swap: "Skeleton items crossfade to real items (opacity 0->1 ~150ms ease-out), shape-matched (no CLS)"
  restraint: "~150-250ms; expand/collapse of a HIERARCHICAL list is the Tree/Accordion height-animation (plain lists don't expand)"
  reduce-motion: "drop insert/reorder/expand + the skeleton pulse to instant; the content is the information, not the motion"
i18n:
  rtl: "logical properties (margin-inline-start, padding-inline-end, text-align:start); leading/trailing slots flip; the DIRECTIONAL chevron mirrors (chevron-right->left) while brand icons don't (inherited from Box); no JS"
  ordered-numerals: "<ol> markers via CSS counter styles / Intl.NumberFormat per locale (Eastern Arabic/Arabic-Indic) — not hardcoded"
  text-expansion: "EN->DE/FR +30%; item layouts absorb longer primary/secondary without breaking alignment or pushing trailing actions out of view; line-clamp doesn't clip mid-word"
  group-collation: "alphabetical group headers use locale-aware Intl.Collator, not ASCII sort"
implementation:
  - "the <ul>/<ol> + the list-style:none -> role=list re-assertion: re-add role=list to the styled <ul> + role=listitem to the <li>s (WebKit drops the semantics); bake into the base List so consumers can't forget"
  - "listbox vs gridlist (the interactivity fork): listbox (role=listbox/option, roving/activedescendant, Home/End/Space/Enter) for LEAF options; gridlist (role=grid/row/gridcell, 2D arrow nav) the moment items contain their own actions (an option can't hold a button). Pick by whether the item has inner interactives"
  - "the rich-item slot model: leading/primary/secondary/trailing; a FIXED leading-column width aligns the text column across items; lines (1/2/3) sets the min-height"
  - "virtualization + aria-setsize/posinset (TanStack Virtual/react-window): beyond ~200 items; true total + true position per rendered item; manage focus when the focused item scrolls out"
  - "grouped/sticky-header lists: a <ul> per group with a heading (or one <ul> + role=group sections); sticky headers via position:sticky"
  - "drag-to-reorder + the keyboard alternative: a focusable drag-handle button -> Space/Enter enters reorder mode -> Up/Down move the item in the array -> a polite aria-live announcement ('Moved [item], now in position 3 of 10') -> Space/Enter commits, Escape cancels (WCAG 2.5.1/2.5.7)"
  - "the item-as-link/button polymorphism: a navigating item is a real <a href>, an acting item a <button> (asChild/Slot: const Comp = asChild ? Slot : 'li'); a whole-item-clickable row uses the Card stretched-link care or the gridlist"
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
    - "list-style:none removing the list role (re-assert role=list) — the most common List a11y bug"
    - "a button/link/switch inside a listbox option (nested-interactive invalid -> use the gridlist)"
    - "virtualization breaking the set size (needs aria-setsize/posinset); focus lost when the focused item unmounts"
    - "building a single-column table (-> List) / forcing a 2D comparison into a list (-> Table); a list OF Cards as a List (-> Grid/Stack of Cards)"
    - "drag-to-reorder with no keyboard alternative (2.5.1/2.5.7); animating a long/virtualized list (jank)"
    - "a bare 'Edit' button with no row context (aria-describedby/explicit label); a whole-item-clickable row nesting interactives"
  inherited: "composes Avatar/Icon/Badge/Tag/Button/Switch/Checkbox/Divider/Empty-State/Skeleton/Link; the listbox content of Select/Combobox/Popover; the terminal-states machine from Empty State/Skeleton; the role=grid trick from Tag/Table; the do/go/choose/read disambiguation from Menu/Side-Navigation"
  role-in-family: "the 1D sibling of Table — the one-dimensional record list across content/selection/navigation/action genres; the content the overlay listboxes host; borders Menu (do)/Side-Navigation (go)/Tree (hierarchical)"
  evolution:
    - "the list-style:none semantics-removal discovery (Scott O'Hara, 2018) -> role=list re-assertion"
    - "the move to GridList for actionable items (React Aria/Spectrum 2020+; the same role=grid trick as Tag/Table)"
    - "virtualization + aria-setsize/posinset"
    - "the rich-list-item / media-object slot standardization (Material ListItem, Primer ActionList.Item)"
    - "the do/go/choose/read separation hardening (one generic List -> distinct genres)"
  unverified:
    - "external 2024-2026 version numbers across the surveyed systems"
    - "the React Aria GridList role details + the per-system listbox-vs-gridlist split — verify against current implementations"
    - "the exact Safari/VoiceOver list-style:none behavior across current versions — verify"
```

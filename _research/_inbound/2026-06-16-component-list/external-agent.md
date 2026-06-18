## 1. Framing
At the systems level, a **List** is the primary one-dimensional (1D) record container. While the Table component manages two-dimensional (2D) tabular data—where the semantic meaning of any given cell relies on the intersection of its row and column coordinates—the List manages a linear sequence of self-contained, independent visual records.

A List item can exhibit high complexity (e.g., containing an avatar, structured typography, multiple interactive states, badges, and trailing action buttons) without violating its 1D nature, provided that the user does not need to scan down vertical columns to compare discrete cell attributes across rows. If cross-record attribute scanning is a core user task, the layout must be modeled as a Table.

To build a resilient List component, a design system must first resolve a deep structural split: the **Do/Go/Choose/Read** disambiguation. A visual design that looks like a "list of items" actually maps to one of four distinct technical, semantic, and keyboard interaction models:

```
                  ┌────────────────────────────────────────┐
                  │          Is the List Visual?           │
                  └───────────────────┬────────────────────┘
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [ INTERACTIVE / WIDGET ]                       [ STATIC / CONTENT ]
  Does it manage a focused option?               Does it serve as navigation?
               │                                             │
      ┌────────┴────────┐                           ┌────────┴────────┐
      ▼                 ▼                           ▼                 ▼
   [ CHOOSE ]        [ DO ]                      [ GO ]            [ READ ]
    Listbox          Menu                       Navigation          Static
  (Selection)      (Actions)                     (Links)            (Content)
```

1. **READ (Static / Content List):** A structural list that a user reads, scrolls, or scans. Items are semantic `<li>` wrappers. While individual items can contain nested interactive elements (e.g., a link to a profile, a button to edit), the list itself is not a monolithic keyboard widget. Focus moves sequentially via the Tab key from one interactive element to the next.
2. **CHOOSE (Interactive Selection List / Listbox):** A selection widget mapped to `role="listbox"` and `role="option"`. The entire list represents a single focusable widget in the page tab sequence. Keyboard navigation inside the widget is handled via arrow keys (managing focus via a roving `tabindex` or `aria-activedescendant`), and selecting an option updates an underlying value.
3. **GO (Navigation List):** A structural list nested within a `<nav>` landmark, where each item is structurally linked to a unique URL.
4. **DO (Action / Menu List):** A list of commands mapped to `role="menu"` and `role="menuitem"`. It is designed for action dispatching and context menus, using specific menu-key behaviors (e.g., matching character keys, Escape key closures).

```
┌────────────────────────────────────────────────────────────────────────┐
│                              DESIGN TRAP:                              │
│             The `list-style: none` Semantics-Removal Bug               │
├────────────────────────────────────────────────────────────────────────┤
│ In Safari/VoiceOver (WebKit), applying `list-style: none` to a `<ul>`  │
│ or `<ol>` to strip default browser bullets strips the underlying list  │
│ semantics. VoiceOver ceases to announce "List, N items".               │
│                                                                        │
│ CRITICAL RESOLUTION: Design systems must programmatically re-assert   │
│ `role="list"` on the element whenever default styling is stripped.     │
└────────────────────────────────────────────────────────────────────────┘
```

Additionally, the **Listbox Interactive Constraint** represents a common implementation trap. By ARIA specification rules, a `role="listbox"` containing `role="option"` elements **cannot** contain focusable, interactive children (such as buttons, switches, or checkboxes). Placing interactive children inside an option element breaks screen reader navigation, as those nested interactive elements are stripped of their keyboard roles and made inaccessible.

If a list must support both list-level selection/keyboard navigation *and* nested child interactive actions, the system must abandon `role="listbox"` and upgrade to the **GridList** pattern (`role="grid"` with structured grid cells).

---
## 2. Anatomy and Parts
The structural layout of a List is defined by a nested composite tree:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [1] List Container: <ul> / <role="listbox"> / <role="grid">                  │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ [2] Group / Section Header                                             │  │
│  ├────────────────────────────────────────────────────────────────────────┤  │
│  │ [3] List Item / Row (rich inline layout)                               │  │
│  │  [a] Leading Slot (Avatar, Icon, Checkbox)                             │  │
│  │  [b] Content Block (Primary Text / Secondary Text)                     │  │
│  │  [c] Trailing Slot (Badge/Tag, Metadata, Button/Switch, Drag Handle,   │  │
│  │      Chevron Indicator)                                                │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│  ────────────────── [4] Divider (Inset / Full-Bleed) ──────────────────────  │
│  [5] Skeleton State / Loading Skeleton Row                                   │
│  [6] Empty State Region                                                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Element Breakdown
1. **List Container (`List`):** The structural outer wrapper. For static lists, this is an HTML `<ul>` or `<ol>`. For interactive lists, it is a `div` or `ul` carrying `role="listbox"` or `role="grid"`.
2. **Group / Section Header (`List.Subheader` / `List.Section`):** Grouping elements that label a subset of list items. When list navigation scrollports are long, this element can be configured to stick to the top of the container viewport.
3. **List Item (`List.Item`):** The structural item wrapper (`<li>` or `role="option"` / `role="row"`). It organizes elements along a horizontal axis using three primary layout zones:
   * **Leading Slot (`List.ItemIcon` / `List.ItemAvatar`):** A reserved visual area for a leading Icon, Avatar, Checkbox, or Drag Handle. It has a rigid structural width to enforce vertical alignment across sibling items.
   * **Content Block (`List.ItemText` / `List.ItemContent`):** A vertical stack containing the Primary Text (headline, truncated to a single line or wrapped) and optional Secondary Text (supporting metadata, supporting a 2-line or 3-line structural clamp).
   * **Trailing Slot (`List.ItemSecondaryAction` / `List.ItemDetail`):** A right-aligned visual container housing status indicators (Badges, Tags), timestamps, explicit interactive controls (Buttons, IconButtons, Switches), or standard structural indicators (such as a chevron to denote a detail-navigation panel).
4. **Divider (`Divider` / `List.Divider`):** A physical rule separating items. It can be applied as a full-bleed horizontal line or styled with an inset that matches the boundary of the Content Block (leaving the leading visual un-bisected).
5. **Skeleton State (`List.ItemSkeleton`):** A placeholder component that matches the layout of a rich list item. It uses layout-mimicking shapes with animated background sweeps to maintain structural stability during initial data loads.
6. **Empty State (`List.EmptyState`):** A full-width block rendered in place of list items when the record dataset is empty. It includes a structured illustration, descriptive header text, and an action button.

---
## 3. Properties / API
To accommodate the Do/Go/Choose/Read classification, the List component's API must balance granular layout control with runtime safety.

### Container Component (`List` / `ListView` / `ListBox`)
| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `genre` | `"read" \| "choose" \| "go" \| "do"` | `"read"` | Determines the underlying semantic tags, interactive roles, and keyboard navigation managers. |
| `selectionMode` | `"none" \| "single" \| "multiple"` | `"none"` | Valid only when `genre` is `"choose"` or `"read"` upgraded to a grid-like selection interface. |
| `density` | `"compact" \| "normal" \| "spacious"` | `"normal"` | Sets row-level padding and vertical margins across all nested child items. |
| `virtualized` | `boolean` | `false` | When true, prepares the list wrapper to handle absolute positioning offsets and windowed data bounds. |
| `as` / `asChild` | `ElementType \| boolean` | `false` | Standard polymorphic API override (e.g., swapping a generic `<ul>` for an `<ol>` or `<nav>`). |

### Item Component (`List.Item` / `ListItem`)
| Property | Type | Default | Description |
| --- | --- | --- | --- |
| `selected` | `boolean` | `false` | Sets selection states. Binds to `aria-selected` or `aria-current="page"` depending on the list container's `genre`. |
| `disabled` | `boolean` | `false` | Disables interactive focus, visually dims the item, and applies `aria-disabled="true"`. |
| `interactive` | `boolean` | `false` | When `true` on static lists, applies standard focusable hover/active styling cues and interactions. |
| `density` | `"compact" \| "normal" \| "spacious"` | `undefined` | Inherits container density unless overridden on an individual item. |
| `lines` | `1 \| 2 \| 3` | `1` | Enforces height constraints and activates multi-line line-clamp styles on the inner content block. |

```tsx
// Typical React / JSX Design System Architecture Pattern
import * as List from '@ds/list';
const RichListExample = () => (
  <List.Root genre="read" density="normal">
    <List.Section title="System Settings">
      {/* 2-line Rich Navigation List Item with Leading Avatar and Trailing Switch */}
      <List.Item interactive lines={2}>
        <List.ItemLeading>
          <Avatar src="/user-avatar.png" alt="Profile" size="md" />
        </List.ItemLeading>
        <List.ItemContent>
          <List.ItemPrimary>Account Status</List.ItemPrimary>
          <List.ItemSecondary>Manage sign-in settings and security defaults</List.ItemSecondary>
        </List.ItemContent>
        <List.ItemTrailing>
          <Switch aria-label="Enable Account Status" defaultChecked />
        </List.ItemTrailing>
      </List.Item>
      <List.Divider inset />
      {/* Standard List Item with Trailing Metadata and Link behavior */}
      <List.Item interactive asChild>
        <a href="/billing">
          <List.ItemLeading><Icon name="credit-card" /></List.ItemLeading>
          <List.ItemContent><List.ItemPrimary>Billing Cycle</List.ItemPrimary></List.ItemContent>
          <List.ItemTrailing>
            <Badge tone="warning">Due Soon</Badge>
            <Icon name="chevron-right" />
          </List.ItemTrailing>
        </a>
      </List.Item>
    </List.Section>
  </List.Root>
);
```

---
## 4. States and Variants
### Visual States Matrix
- **Default (Static):** `li` — Base style, neutral text.
- **Interactive Hover:** `[interactive]:hover` — Subtle background tint (e.g., 4% neutral overlay).
- **Focus:** `li:focus-visible` — Outer focus-ring offset.
- **Selected:** `[aria-selected="true"]` — High-contrast accent track, tinted fill background.
- **Disabled:** `[aria-disabled="true"]` — 40-50% opacity scale, `pointer-events: none`.

### Key Variations
* **Static List (`genre="read"`) vs Selection List (`genre="choose"`):** Static lists show standard web cursor behaviors and sequential tab stops. Selection lists use pointer styles and interactive keyboard patterns, using arrow keys to cycle focus through item rows.
* **Density Variants:** `compact` (e.g., `32px` line-height/padding bounds, optimized for high-density dashboards, sidebars, nested menus); `normal` (e.g., `48px` minimum height, desktop/touch-friendly); `spacious` (e.g., `64px` to `72px`, mobile, content-heavy feeds, onboarding wizards).
* **Grouped (Sticky Group Headers):** When scrolling long lists, section headers lock to the top edge of the list's viewport (`position: sticky`) until pushed out of view by the subsequent section header.
* **Empty & Loading Skeleton Variants:** The container switches its contents when loading states are active. Skeleton elements are injected as temporary, non-interactive items. When empty datasets are detected, standard structural layouts are replaced by centered empty-state illustrations and messages.

---
## 5. Usage Guidance
To maintain visual and technical consistency across complex apps, layout components must adhere to strict boundary rules.

```
  [ 2D Tabular Comparison ] ── columns contain distinct variables ──> [ TABLE ]
  [ 1D Sequential Data ] ── each item self-contained ──> is it interactive?
     INTERACTIVE: structural intent? CHOOSE -> Listbox / DO -> Menu / GO -> Navigation
     STATIC: grouped? YES -> Definition List (<dl>) / NO -> Standard List (<ul>)
```

### Boundary Definitions
* **List vs. Table:** Choose **Table** when users must compare attributes down structured columns (e.g., comparing Price, Status, and Date side-by-side). Choose **List** when each record reads like an isolated paragraph or standard visual card. A list item can contain multiple details, but they are presented as a nested stack of secondary lines or metadata tags, not as aligned column cells.
* **List vs. Menu:** A **List** (with selection enabled) exists to select data records from a collection. A **Menu** exists to dispatch actions, execute page commands, or navigate interfaces. Do not use an interactive Listbox in place of a system dropdown menu.
* **Description List (`<dl>`) vs. Standard List (`<ul>`):** Use a Description List when content maps strictly to label-and-value key pairings (e.g., metadata sidebars showing `Author: Jane Doe`, `Published: 2026`). Use standard lists for sequential items containing identical visual templates.
* **When to Virtualize:** Implement virtualization (windowed rendering) when list sizes exceed **200 items**. Rendering hundreds of deep DOM trees (especially those with avatars, menus, and complex interactive states) can degrade scroll performance and cause noticeable rendering lag.

---
## 6. Accessibility (A11y)
### Semantic Recovery of Stripped Lists
Design systems almost universally strip default HTML list margins, padding, and bullets. However, applying `list-style: none` to `<ul>` or `<ol>` elements causes WebKit-based browsers (including Safari on macOS and iOS) to strip the structural list role from the accessibility tree. As a result, screen readers fail to announce list items as a structured group or report the item count to the user.

To restore this critical context, **systems must programmatically inject `role="list"` onto the list element, and `role="listitem"` onto its child elements** whenever default styles are stripped.

```html
<ul class="ds-list--stripped" role="list">
  <li class="ds-list-item" role="listitem">Item 1</li>
  <li class="ds-list-item" role="listitem">Item 2</li>
</ul>
```

### The Interactive Listbox Pattern (`role="listbox"`)
For choice-selection components (like dropdown menus, select elements, and combobox lists), the component must implement the WAI-ARIA Listbox Pattern.
* **Keyboard Navigation Requirements:** The container must be a single tab stop (`tabindex="0"`). Focus within the listbox must be managed dynamically, either using **Roving tabindex** (moving `tabindex="0"` to the active item while other options use `tabindex="-1"`) or **`aria-activedescendant`** pointing to the ID of the currently focused child item. Up/Down Arrow keys cycle focus; Home/End jump to first/last; Space/Enter select. When multi-select is active, `aria-multiselectable="true"` is declared on the container, and selected options carry `aria-selected="true"` (unselected `aria-selected="false"`).

```html
<div role="listbox" aria-label="Select an active environment" tabindex="0" aria-activedescendant="opt-2">
  <div id="opt-1" role="option" aria-selected="false">Production</div>
  <div id="opt-2" role="option" aria-selected="true">Staging</div>
  <div id="opt-3" role="option" aria-selected="false">Development</div>
</div>
```

### The Interactive Constraint & The GridList Escape Hatch
According to the HTML and ARIA specifications, elements carrying `role="option"` are **leaf nodes**. They cannot contain focusable, interactive child elements (such as buttons, links, or switches). If an interactive element is placed inside an option, screen readers will either ignore its presence or strip its interactive capabilities entirely, rendering it unusable for keyboard users.

If your list requires both **selection** (arrowing through rows) and **embedded interactive controls** (clicking a button *inside* a row), you must upgrade the structure to a **GridList pattern** (`role="grid"`):
* The container uses `role="grid"` (and optional `aria-multiselectable="true"`).
* Each list item acts as a row and uses `role="row"`.
* Interactive elements and text blocks inside the row are wrapped in cells using `role="gridcell"`.
* Arrow keys navigate in two dimensions (up/down between rows, and left/right to move focus between the row item and its inner interactive buttons).

```html
<div role="grid" aria-label="System Users">
  <div role="row" aria-selected="true" id="row-1">
    <div role="gridcell"><span id="user-1-label">Jane Doe (Admin)</span></div>
    <div role="gridcell"><button aria-describedby="user-1-label" aria-label="Edit settings">Edit</button></div>
  </div>
  <div role="row" aria-selected="false" id="row-2">
    <div role="gridcell"><span id="user-2-label">John Smith (Member)</span></div>
    <div role="gridcell"><button aria-describedby="user-2-label" aria-label="Edit settings">Edit</button></div>
  </div>
</div>
```

### WCAG Success Criteria Mapping
* **SC 1.3.1 - Info and Relationships:** Enforced through list elements (`<ul>`/`<li>`), or explicit programmatic re-assertions (`role="list"`/`role="listitem"`).
* **SC 2.1.1 - Keyboard:** Ensures arrow key navigation in Listbox and GridList variants.
* **SC 4.1.2 - Name, Role, Value:** Correct implementation of `aria-selected` and `aria-current` properties.
* **SC 2.5.1 / 2.5.7 - Pointer Gestures & Drag-to-Reorder:** If a list supports drag-and-drop sorting, it must provide a keyboard-accessible alternative (e.g., action buttons to move items up or down).

---
## 7. Content Guidelines
* **Typography Hierarchy:** Keep a distinct visual separation between primary and secondary copy. Use bold, high-contrast text for the Primary Title, and a smaller, muted color for supporting lines.
* **Truncation and Wrapping Rules:** Primary text — truncate with an ellipsis after a single line. Secondary text — support multi-line descriptions using `-webkit-line-clamp: 2`. Ensure layout containers adapt gracefully when lines wrap.
* **Accessible Naming:** If a list item contains multiple lines of text along with nested buttons, the interactive element's accessible name must be explicitly defined. Avoid ambiguous buttons like "Edit" without context. Use `aria-describedby` to link the button to the row's primary title, or construct an explicit label like `aria-label="Edit user John Smith"`.
* **Empty State Copy:** Ensure empty state messages provide clear instructions (e.g., "No active integrations. Click 'Add Integration' below to get started.").

---
## 8. Motion and Transition
* **FLIP Animation Technique:** When list items are inserted, removed, or reordered, use the **FLIP** (First, Last, Invert, Play) technique to play a smooth, hardware-accelerated transform animation, rather than letting elements abruptly snap into place.
* **Skeleton Loading Fade-Ins:** Transition the loading placeholder state to the real list content using a smooth opacity fade (`opacity: 0` to `opacity: 1` over `150ms` ease-out).
* **Animate with Restraint:** Keep animations brief (`150ms`–`250ms`). For long lists, do not animate individual item entry animations sequentially (lag/performance bottlenecks).
* **Respect Accessibility Preferences:**

```css
@media (prefers-reduced-motion: reduce) {
  .ds-list-item, .ds-skeleton-pulse { animation: none !important; transition: none !important; }
}
```

---
## 9. Internationalization (I18n)
* **RTL Support:** Avoid directional CSS properties (`margin-right`/`padding-left`). Use logical properties (`margin-inline-start`, `padding-inline-end`, `text-align: start`).
* **Mirroring Icons & Chevrons:** Brand icons remain un-mirrored; directional UI indicators (disclosure chevrons) must mirror horizontally in RTL.
* **Numbered List Formatting:** For ordered lists, avoid hardcoding numeric indicators; use CSS counter styles or `Intl.NumberFormat` (e.g., Arabic-Indic / Eastern Arabic numerals).
* **Dynamic Text Expansion:** Translation EN→German/French can increase length by up to 30%. Ensure list item layouts handle longer strings without breaking alignment or pushing trailing actions out of view.

---
## 10. Naming
| System | Static List | Selection List | Grid-capable Action List |
| --- | --- | --- | --- |
| **MUI (Material 3)** | `List` / `ListItem` | `ListItemButton` | — |
| **GitHub Primer** | — | `ActionList` | `ActionList` |
| **Adobe Spectrum** | `ListView` | `ListBox` | `ListView` (GridList) |
| **Shopify Polaris** | `List` | `ActionList` | `ResourceList` |
| **IBM Carbon** | `UnorderedList` | `ContainedList` | — |

### Naming Recommendation
1. **`List` (or `List.Root`):** The general, top-level static container.
2. **`ListBox` (or `List.Box`):** The selection-specific widget wrapper (`role="listbox"`).
3. **`GridList` (or `List.Grid`):** The advanced list layout supporting both selection and embedded interactive children.
4. **`List.Item`:** The base row element.
5. **`List.ItemText` / `List.ItemContent`:** The inner block containing typography.
6. **`List.Divider`:** The separator rule.

---
## 11. Implementation Notes
### Polymerizing Interactive Items (The `asChild` Pattern)
A robust list item must support diverse underlying HTML elements (`<li>`, `<a>`, custom Router links). Implement Radix-style polymorphism using an `asChild` prop.

```tsx
import { Slot } from '@radix-ui/react-slot';
export const ListItem = React.forwardRef(({ asChild, interactive, className, ...props }, ref) => {
  const Component = asChild ? Slot : 'li';
  return <Component ref={ref} className={clsx('ds-list-item', { 'is-interactive': interactive }, className)} {...props} />;
});
ListItem.displayName = 'List.Item';
```

### Virtualization & The `aria-setsize` Tension
When using windowed list rendering engines (`react-window`, `@tanstack/react-virtual`), only a small subset of list items are rendered in the DOM. This breaks screen readers' default ability to calculate and announce total item counts. **Systems must programmatically calculate and pass total dataset bounds using `aria-setsize` and `aria-posinset`** directly to each rendered row.

```html
<div role="listbox" aria-label="Dataset view">
  <div role="option" aria-setsize="10000" aria-posinset="500" id="item-500">Item 500</div>
  <div role="option" aria-setsize="10000" aria-posinset="501" id="item-501">Item 501</div>
  <div role="option" aria-setsize="10000" aria-posinset="502" id="item-502">Item 502</div>
</div>
```

### Keyboard-Accessible Reordering (Drag-and-Drop)
If a list supports drag-and-drop item sorting, you must provide a keyboard-accessible alternative:
1. **Drag Handle Button:** Focusable button inside the item row.
2. **Triggering Mode:** User presses Space or Enter on the drag handle to enter "Reorder Mode".
3. **Navigation:** Pressing Up or Down Arrow moves the physically focused item within the dataset array.
4. **Aria Announcement:** Announce positions dynamically to screen readers using an aria-live region (e.g., "Moved account element, now in position 3 of 10").
5. **Commit:** Press Space or Enter again to lock in the new order, or Escape to cancel.

---
## 12. Related and Alternative Components
* **Composes:** Avatar / Icon (leading slots), Checkbox / Radio (selection), Badge / Tag (trailing metadata), Button / Switch (actions/settings inside rows), Divider (separators), Empty State / Skeleton (loading and fallback states).
* **Borders & Transitions:** Menu (Do — popup command layouts, `role="menu"`), Side Navigation (Go — navigation trees mapping to URLs), Tree (Hierarchical — expandable nesting), Table (2D Matrix — comparison across structured columns).

---
## 13. Field POV Evolution
### 1. Stripping Semantics and the Discovery of the WebKit Bug
Historically, design systems stripped default browser list styles as a standard reset. However, in **2018**, accessibility researcher **Scott O'Hara** discovered that WebKit/Safari stripped list accessibility roles whenever `list-style: none` was applied. This established a new standard: design systems must programmatically re-apply `role="list"` and `role="listitem"`.

### 2. The Move to GridList for Actionable Items
For a long time, interactive lists were built using simple nested HTML inside standard list options. As web applications grew more complex, systems needed lists supporting both selection and internal actions (like editing a row). To resolve the strict ARIA limitation, **Adobe Spectrum and React Aria (2020+)** pioneered the **GridList pattern** (`role="grid"`).

### 3. Clear Separation of Do/Go/Choose/Read Tasks
Early component libraries often shipped a single, generic `List` component handling everything from navigation links to form inputs. Modern systems now enforce a strict separation of concerns — static content (Read), selection widgets (Choose), navigation links (Go), and command menus (Do).

---
## 14. Sources Cited
* **Adobe Spectrum / React Aria** *(v3, 2024)* — GridList & ListBox Patterns; Keyboard Navigation Guidelines.
* **Material Design 3 (MUI)** *(v5.15, 2024)* — Nested list sub-components and layout density specifications.
* **GitHub Primer** *(v36, 2024)* — ActionList patterns and layout structure for actionable lists.
* **Shopify Polaris** *(v12, 2024)* — ResourceList patterns, selection controls, and multi-item bulk actions.
* **IBM Carbon** *(v11, 2023)* — ContainedList architecture and structural list guidelines.
* **Scott O'Hara A11y Research** *(2018, updated 2023)* — "Fixing Lists" accessibility findings on `list-style: none` semantics loss in WebKit.
* **W3C WAI-ARIA Authoring Practices Guide (APG)** *(2024 updates)* — Listbox design pattern, GridList specifications, and virtualized list management.

---
## 15. Agent-Consumable Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ListComponentSchema",
  "type": "object",
  "properties": {
    "name": { "type": "string", "enum": ["List", "ListBox", "GridList"] },
    "description": { "type": "string", "default": "A one-dimensional structural or interactive container for displaying collections of content rows." },
    "anatomy": { "type": "array", "items": { "type": "string" }, "default": ["ListContainer", "ListItem", "ListItemLeadingSlot", "ListItemContentBlock", "ListItemPrimaryText", "ListItemSecondaryText", "ListItemTrailingSlot", "ListSubheader", "ListDivider", "ListEmptyState", "ListItemSkeleton"] },
    "properties": {
      "type": "object",
      "properties": {
        "genre": { "type": "string", "enum": ["read", "choose", "go", "do"], "default": "read" },
        "selectionMode": { "type": "string", "enum": ["none", "single", "multiple"], "default": "none" },
        "density": { "type": "string", "enum": ["compact", "normal", "spacious"], "default": "normal" },
        "virtualized": { "type": "boolean", "default": false }
      }
    },
    "accessibility": {
      "type": "object",
      "properties": {
        "role_mapping": { "type": "object", "properties": { "read": { "type": "string", "default": "list" }, "choose": { "type": "string", "default": "listbox" }, "gridlist": { "type": "string", "default": "grid" } } },
        "critical_requirements": { "type": "array", "items": { "type": "string" }, "default": [
          "Programmatic re-assertion of role='list' on styled <ul> elements with list-style: none.",
          "Listbox option elements must not contain interactive focusable children.",
          "Upgrade to GridList (role='grid') if selection elements must contain sub-actions like buttons.",
          "Inject aria-setsize and aria-posinset on items in virtualized lists."
        ] }
      }
    }
  }
}
```

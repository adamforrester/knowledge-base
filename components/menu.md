---
okf_version: "0.1"
type: component-brief
title: Menu
description: A transient overlay of application commands — and the catalogue's sharpest semantic boundary, since role=menu is the most-misused ARIA pattern on the web. A field-truth study of the menu-vs-listbox-vs-navigation disambiguation (commands vs values vs links), the roving-tabindex focus model (real focus moves into the menu — the opposite of Combobox's aria-activedescendant), the menu-button aria-haspopup/expanded/controls contract, the submenu safe-triangle, disabled-but-focusable items, stateful menuitemcheckbox/menuitemradio, and the dropdown/context-menu/menubar surfaces — standing on the Button trigger and the overlay-positioning substrate Select and Combobox established.
tags: [components, overlay]
category: Overlay
status: stable
aliases: [dropdown-menu, action-menu, action-list, overflow-menu, kebab-menu, popup-menu, context-menu, menubar]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Menu

> A Menu is a transient surface of **application commands** — the desktop app-menu idiom on the web (Duplicate, Delete, the kebab "⋮", a row's action list). It is the first brief to inherit the **overlay/positioning substrate** as an explicit dependency — the anchored-popup machinery Select and Combobox established (collision/flip, portal, Popover API + CSS Anchor Positioning, dismiss) — with its **trigger inheriting Button** (`aria-haspopup` + `aria-expanded` + `aria-controls`). What's left, once those are inherited, is the part the field actually fights over: the single defining decision is that `role="menu"` is for **commands**, not navigation and not value-selection. A dropdown of *links* is a `<nav>` + disclosure + links (never `role=menu`); choosing a *value* is a Listbox/Select. Get that wrong — the near-universal "dropdown-nav-is-a-menu" mistake — and you impose application-widget keyboard semantics on users who just wanted a list of links. The mechanical signature of a real Menu is that **DOM focus moves into it** (roving tabindex), the exact opposite of Combobox.

---

## 1. Framing

A Menu presents a list of **executable commands or application-state toggles** invoked from a button, a kebab/overflow trigger, or a right-click. The "go / choose / do" test fixes the boundary, and resolving it is *the* architectural decision because `role="menu"` is the most-misused ARIA pattern on the web:

- **Menu = "do something."** Commands ("Export", "Invite", "Delete") and in-place state toggles ("Show grid", a theme). `role="menu"`/`menuitem`; focus moves in; actions fire.
- **Not navigation ("go somewhere").** A dropdown of *links* to URLs — the ubiquitous marketing-site "nav dropdown", an account menu of page links — is a **Disclosure**: a `<button aria-expanded>` revealing a `<nav>`/list of `<a href>`. Applying `role="menu"` here is the cardinal anti-pattern: it strips link semantics and imposes roving-tabindex arrow-key navigation on users who expected ordinary tabbable links. **`role="menu"` must never be applied to site navigation.**
- **Not value-selection ("choose a value").** Picking a value to submit, filter, or persist (a country, a status, a sort order) is a **Listbox/Select** (see select) — `aria-selected` options holding a value, with focus staying put via `aria-activedescendant`. A Select's trigger *reflects the chosen value*; a Menu's trigger is a static label ("Actions", "⋮").
- **Not a text-filtered picker** — that's Combobox (see combobox).

Structurally the Menu stands on two briefed substrates so the brief can spend its attention on the Menu-specific mechanics: the **trigger inherits Button** (see button), and the **overlay/positioning machinery is inherited from the substrate Select and Combobox established** (anchored popup, collision-aware flip/shift, portal, Popover API / CSS Anchor Positioning / Floating UI, outside-dismiss — see select, combobox; the eventual home is Popover/Dialog, not yet briefed). Menu is also the overflow affordance Breadcrumbs leans on (see breadcrumbs). Why systems still disagree: exactly where the menu/nav/listbox lines fall, the submenu hover mechanics, whether menus carry stateful items, and the menubar's relevance to web (vs. native) apps.

## 2. Anatomy and parts

The field has abandoned the monolithic `<Menu items={…}/>` for **composable parts** (Radix/Ariakit as the reference):

- **Trigger / menu button** — a `<button>` with `aria-haspopup="menu"` (or `true`), `aria-expanded`, `aria-controls` → the surface id (see button). Radix's `asChild` merges these onto a consumer's Button without an extra wrapper node. A kebab/overflow `⋮`, a "More" button, a split/combo button, or a right-click target.
- **Portal** — lifts the surface to `document.body` to escape `overflow:hidden`/stacking-context clipping (inherited from the overlay substrate, §11).
- **Content / surface** — `role="menu"` (or `role="menubar"`); owns positioning + the internal roving-tabindex state.
- **`menuitem`** — the action row (the default item).
- **`menuitemcheckbox` / `menuitemradio`** — stateful items (`aria-checked`); a `menuitemradio` set sits in a `role="group"` (mutual-exclusion boundary). An **ItemIndicator** (a checkmark/dot) renders when checked.
- **group + label** — `role="group"` + a non-focusable label associated via `aria-labelledby` (semantic section boundary).
- **separator** — `role="separator"` between groups (see divider).
- **leading icon** (decorative, `aria-hidden` — see icon), **trailing shortcut hint** ("⌘N" — visual only, `aria-hidden`, §7), **submenu trigger** (a `menuitem` that *also* carries `aria-haspopup` and opens a **SubContent** instead of firing).
- **menubar** (`role="menubar"`) — the persistent horizontal app-menu bar (rich apps only, §5).

Primer/Polaris compose the menu from a lower-level **ActionList** primitive (a generic vertical list of interactives) that takes on the `role=menu` + roving-tabindex behaviour only when wrapped in an ActionMenu/Popover — maximising reuse while keeping the semantic lanes separate. Carbon ships density-specific macro-patterns (`OverflowMenu`, `ComboButton`); the underlying nodes are the same.

## 3. Properties / API

The split is headless composition (Radix/Ariakit — discrete parts, context through the tree) vs. a collection API (React Aria/Spectrum — an `items` array or `<Item>` children parsed for internal state). **The practice default favours composable parts** (DOM structure divorced from logical state, maximum layout freedom) with a convenience `items`/`actions` array for the data-driven case.

- **Parts:** `Menu` (root; owns `open`/`defaultOpen`/`onOpenChange`) / `MenuTrigger` (`asChild`) / `MenuContent` / `MenuItem` / `MenuGroup` + `MenuLabel` / `MenuSeparator` / `MenuCheckboxItem` (`checked`/`onCheckedChange`) / `MenuRadioGroup` (`value`/`onValueChange`) + `MenuRadioItem` / `MenuSub` + `MenuSubTrigger` + `MenuSubContent`.
- **`onAction` / `onSelect`** — the core callback, keyed by item id. **Abstract DOM `click` into a synthetic `onAction`** so pointer-click, Enter, Space, *and* type-ahead activation all run the same path (fire → close → restore focus to the trigger). Per-item `onSelect` is the alternative.
- **Stateful items keep the menu open** — toggling a `MenuCheckboxItem`/`MenuRadioItem` does *not* dismiss the surface (so the user can flip several settings), unlike a plain `MenuItem` which fires-and-closes.
- **Positioning props** — `side`/`align`/`sideOffset`/`alignOffset`/`avoidCollisions` — **inherited from the overlay substrate** (see select/combobox), not re-derived here.
- **Per-item:** `disabled` (but still focusable — §6), `destructive`/`danger`, `icon`, `shortcut`, and `href` only when the item *legitimately* navigates (rare — see the nav-vs-menu rule, §5).

## 4. States and variants

- **Item states:** rest / **highlighted** (hover *and* keyboard focus are unified — moving the pointer over an item makes it the focused item; headless libs expose `data-highlighted`/`data-active-item` rather than relying on `:focus` rings that flicker during fast arrow traversal) / active (pressed) / **disabled** (focusable, `aria-disabled` — §6) / **danger/destructive** (critical token) / **checked** (stateful items).
- **Menu states:** closed / open / submenu-open.
- **Surface variants:**
  - **Dropdown menu** — anchored to a button (the common case).
  - **Context menu** — invoked by the `contextmenu` event (right-click / long-press), anchored to the pointer's `clientX`/`clientY`, no persistent visible trigger.
  - **Menubar** — a persistent `role="menubar"`; opening one menu and pressing Left/Right walks to adjacent menus without re-clicking (rich app only, §5).
  - **Split / combo button** — a primary action segment + an adjacent caret menu trigger (Carbon ComboButton; Material 3 expressive); the caret opens the alternatives.
  - **Content variants:** with-icons / with-shortcuts / with-selection (stateful).

## 5. Usage guidance

- **Use a Menu** for a list of **actions/commands** from a button, kebab/overflow, or right-click — especially when there are too many actions to surface inline (the overflow/kebab pattern; Carbon's `OverflowMenu` is the dense-table specialisation).
- **Don't use a Menu for:**
  - **Navigation** (links to URLs) → `<nav>` + disclosure + a list of links. *The most important boundary.* If the items are `<a href>`s that route, it is not a `role=menu`.
  - **Selecting a value** → Select/Listbox (see select).
  - **Text-filtering a long list** → Combobox (see combobox).
  - **A few always-relevant actions** → render Buttons / a Toolbar; a menu needlessly hides them behind a click.
- **Decision frameworks:**
  - **Menu vs. nav vs. listbox:** the "do / go / choose" test.
  - **Menu vs. Select:** does the row *fire an action* (Menu) or *set a persisted value the trigger then reflects* (Select)?
  - **Split/combo button:** when one action dominates but alternatives must stay reachable.
  - **Menubar or not:** a persistent `menubar` is a desktop-app affordance (IDE, design tool, Docs). Most web apps **don't** want one — it imports two-dimensional arrow-key semantics for little gain. Default to dropdown menus.
  - **Nesting:** discourage submenus deeper than **one level** — deep flyouts demand fine motor control through the safe-triangle and degrade fast. For genuinely hierarchical choices reach for a Tree, a multi-step Dialog, or page routing instead.

## 6. Accessibility

The custom-menu failure rate is notoriously high — coordinating roving tabindex, portals, and dismissal is exactly what's easy to get subtly wrong.

- **Roles:** `role="menu"` (surface) containing `menuitem` / `menuitemcheckbox` / `menuitemradio`, grouped by `role="group"` (+ label) and divided by `role="separator"`; `role="menubar"` for the persistent bar. **Correct only for actual application command menus** — applying them to navigation is the headline error (§5).
- **The menu-button contract:** trigger is a `<button>` with `aria-haspopup="menu"` (or `true`), `aria-expanded` tracking open state, `aria-controls` → the surface id.
- **The roving-tabindex focus model (the defining mechanic, and the explicit contrast with Combobox):** when the menu opens, **DOM focus physically moves into the surface** — to the first non-disabled item (keyboard-opened) or the container. Arrow keys *move real focus* between items via roving tabindex (active item `tabindex="0"`, the rest `-1`, with `.focus()` called on the new item), so AT announces each item's label/role/position. **Escape closes and returns focus to the trigger** — failing to restore focus drops it to `<body>` and is catastrophic for screen-reader orientation. **Tab closes the menu and moves focus on** — a menu is *not* a focus-trap (that's Dialog, §11). This is the opposite of **Combobox**, where DOM focus *stays on the input* and the active option is tracked virtually by `aria-activedescendant` (see combobox): Menu = real focus moves; Combobox = virtual focus.
- **Keyboard:** Down/Up cycle items (wrapping); Home/End jump; **type-ahead** focuses the next item matching a transient keystroke buffer (cleared after ~500ms); Enter/Space activate **and close**; Escape closes; Right opens a submenu / moves to the next menubar menu; Left closes a submenu / moves to the previous menubar menu. (RTL reverses the submenu arrows — §9.)
- **Disabled items stay focusable** (APG, for discoverability — a screen-reader user arrowing the list should learn the action *exists but is unavailable*, not have it silently skipped). The mechanism: keep the item in the roving cycle and set **`aria-disabled="true"`** rather than the native `disabled`/removing it — Ariakit's `accessibleWhenDisabled`, Radix's `[data-disabled]` styling hook. The practice default follows APG: **focusable + `aria-disabled`, skipped only for activation.**
- **Stateful items** carry `aria-checked`; use them for *toggles/modes within an action menu*, not as a Select substitute (a surface that's really choosing a value belongs to listbox).
- **WCAG SCs:** 4.1.2 (name/role/value), 2.1.1 / 2.1.2 (keyboard, no trap), 2.4.3 (focus order — return to trigger), 1.4.13 (content on hover/focus — submenus dismissable/persistent), plus the trigger's Button SCs.

## 7. Content guidelines

- **Action-verb labels** for commands ("Export document", "Move to folder"); a trailing **"…"** signals the action opens a further dialog / needs more input. Stateful items use the noun/adjective of the *state* applied ("Dark mode", "Show grid", "Compact spacing").
- **Order & group** by frequency/domain; frequent actions at the top (least pointer travel); group related actions with a separator + optional label.
- **Isolate the destructive action** at the bottom, in its own group, behind a separator, styled with the danger token **and** its position/label (colour is never the only carrier) — never adjacent to the most-used action.
- **Shortcut hints** are right-aligned, formatted to the user's OS (⌘N vs Ctrl+N), and **`aria-hidden`** — they're a visual aid; the actual binding lives globally (`aria-keyshortcuts`/app help), and announcing them inline is verbose noise.
- **Icon discipline** — leading icons are decorative (`aria-hidden`); if any item in a group has an icon, reserve the icon column for the whole group (clean text reading-edge); never ship icon-only menu items (they need text labels).
- **Keep menus shallow and short** — a long menu wants to be a Listbox/search; deep submenus signal an IA problem.

## 8. Motion and transition

Motion is a **spatial orienter**, so it must be **origin-aware**: the surface scales/fades from the trigger edge (~120–150ms, `transform-origin` at the anchor). Because the positioning engine may flip the menu above/left to avoid collisions, a hardcoded top origin looks broken when flipped — Radix exposes a computed `--radix-…-transform-origin` custom property so the `@keyframes` always grow out of the trigger wherever it landed. Submenus reveal with a short fade behind a **hover-intent delay** (the safe-triangle, §11). Material 3's expressive update moves toward spring/physics-based curves. Under `prefers-reduced-motion: reduce`, fall back to instant toggles (opacity only). No motion on item hover beyond the background change. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL inverts the geometry and the keys.** The surface mirrors: trailing shortcut hints move to the left edge, leading icons to the right; preferred alignment flips (a right-aligned LTR menu defaults left in RTL — the overlay substrate's placement mirrors automatically). Critically, **the submenu arrow keys reverse**: under `dir="rtl"`, **Left** opens a submenu and **Right** closes it — hardcoding the directional keys without reading `dir` is a major i18n failure.
- **Type-ahead** must match composed characters (non-Latin scripts, IME composition), not raw keystrokes.
- **Text expansion** (+30–50%): avoid rigid max-widths that force ugly wrapping; size intrinsically (`min/max-content`) up to a sensible cap, then truncate with a tooltip fallback. (See 13-internationalization-and-rtl.)

## 10. Naming

Nomenclature is fragmented: **`Menu`** (React Aria, Material, Base Web, Carbon — the clean mapping to `role="menu"`), **`DropdownMenu`** (Radix, Atlassian, shadcn — distinguishing it from `ContextMenu`/`Menubar`), **`ActionMenu`**/**`ActionList`** (Primer/Polaris — list primitive + Popover), **`OverflowMenu`**/kebab (Carbon), **`ContextMenu`** (right-click), **`Menubar`** (persistent bar). **The practice default: `Menu`** as the umbrella with composable parts (`MenuTrigger`/`MenuContent`/`MenuItem`/…), surfacing **`ContextMenu`** and **`Menubar`** as sibling triggers/variants of the same content primitive, and treating **overflow/kebab** as a `Menu` with an icon-button trigger rather than a separate component. Aliases to map: `DropdownMenu`, `ActionMenu`, `ActionList`, `OverflowMenu`, `KebabMenu`, `PopupMenu`, `ContextMenu`, `Menubar`.

## 11. Implementation notes

- **Don't hand-roll — Radix `DropdownMenu`/`ContextMenu`/`Menubar`, React Aria `Menu`/`useMenu`, or Ariakit are the references.** They solve roving tabindex, type-ahead, submenu timing, portal/positioning, and dismissal — the high-failure surface. Skin the headless core.
- **Positioning is inherited** from the overlay substrate (see select/combobox): portal to escape `overflow:hidden`/stacking traps; collision-aware flip/shift; z-index becomes a global token, not a local property. The **Popover API + CSS Anchor Positioning** are eroding the Floating-UI/portal machinery (the same current-platform shift flagged in select — verify support; progressive-enhance).
- **The submenu safe-triangle** is the marquee trap (the "Amazon dropdown problem"): moving the pointer diagonally from a parent item toward its open submenu crosses sibling items; naively closing on the sibling's `mouseenter` makes flyouts unusable. The fix is a **safe polygon** (Floating UI `safePolygon`) — an invisible geometric bridge from the cursor's exit point to the SubContent corners that keeps the submenu open while the pointer aims at it — or, more simply, a **~150–200ms `setTimeout` close delay** giving a grace period without the polygon's secondary `pointer-events` bugs (a polygon node with `pointer-events:auto` can block underlying clicks/scroll).
- **Roving tabindex, not a focus trap.** Restore focus to the trigger on close (Escape/select/outside-click); close on Tab. Misapplying a Dialog-style trap prevents power users from tabbing through a form that contains menu triggers.
- **The nav-dropdown is a different component.** A navigation flyout is a disclosure `<button aria-expanded>` revealing a `<nav>`/`<ul>` of `<a href>` links — **no `role=menu`, no roving tabindex**; Tab walks the links normally. Document it as a separate pattern (Primer forks its primitives precisely to force this lane) so teams don't reach for `Menu`.
- **Context menu** — intercept/augment the native `contextmenu` event, anchor at the pointer, and provide a **keyboard route** (Shift+F10 / the context-menu key), since right-click isn't keyboard-accessible alone.

## 12. Related and alternative components

- **Stands on:** Button (the trigger — see button), the overlay/positioning substrate (collision/flip, portal, dismiss — established by select and combobox; eventual home Popover/Dialog), Icon (leading icons, kebab, submenu chevron — see icon), Divider (the `role=separator` — see divider).
- **Alternative to:** Select/Listbox (choosing a value — see select), Combobox (text-filtered picker — see combobox), a **Navigation disclosure** (links — *not* a `role=menu`; the structural foil), a Toolbar / inline Buttons (few, always-visible actions).
- **Composed by:** Breadcrumbs (the overflow/collapse menu — see breadcrumbs), Table/row actions, the split/combo button.
- **Superseded by:** Listbox/Select when the surface is really value-selection; a nav disclosure when the items are links; a Tree / multi-step Dialog / routing when the hierarchy is deep.

(The first brief to inherit the overlay/positioning substrate as an explicit dependency — the machinery Select and Combobox established, now reused — and the roving-tabindex counterpart to Combobox's `aria-activedescendant` virtual-focus model. See button for the trigger, select/combobox for the overlay substrate + the listbox-vs-menu line, breadcrumbs for the overflow consumer, divider for the separator, icon for the glyphs. 03-component-library; 29 for the docs template. Popover and Dialog are the unbriefed overlay primitives this forward-references — when they land, the inherited positioning substrate formalises there.)

## 13. Field POV evolution

1. **Monolithic → composable parts.** The `<Menu items={data}/>` config object gave way to discrete parts (`Menu.Root`/`Trigger`/`Item`/`Separator`, Radix/Ariakit) — consumers inject custom icons/layout/router wrappers without breaking the ARIA contract or state machine.
2. **The "nav-is-not-a-menu" correction hardened into law.** Automated audits flag `role="menu"` on navigation; systems (Primer) now fork their primitives — ActionList for command menus, separate list structures for nav — forcing the correct semantic lane by default.
3. **The overlay substrate is being rebuilt on the platform.** The Popover API + CSS Anchor Positioning are eroding reliance on Floating UI / manual portals — menus bind content to trigger via `anchor()`, delegating collision/flip to the browser (smaller bundles, no layout thrash) (cross-brief, current-platform-state — verify).
4. **ActionList-composes-a-menu** — Primer/Polaris separate presentation (a reusable list) from behaviour (overlay + roving focus), rather than a bespoke Menu.
5. **Disabled-but-focusable converged** (Ariakit `accessibleWhenDisabled`, Radix `[data-disabled]`) — `aria-disabled` over native `disabled` for discoverability.

## 14. Sources cited

(Conservative; the external pass cited Radix v1.x, React Aria v3.x, Ariakit v0.4.x, Primer v31.x, Carbon v11/v12, Material 3 "Expressive" 2026, Floating UI v1.x — held loosely and flagged unverified; `last-audited` is the re-run trigger.)

- **WAI-ARIA APG** — Menu/Menubar pattern, Menu Button pattern (roles, roving-tabindex focus model, keyboard, disabled-item focusability, the application-menu-vs-disclosure-navigation disambiguation) (APG 1.2, 2021–2026).
- **Radix UI** — `DropdownMenu`/`ContextMenu`/`Menubar` (the de facto headless reference; composable parts, `asChild`, collision-aware `transform-origin`, `[data-disabled]`) (2024–2026).
- **Adobe Spectrum / React Aria** — `Menu`/`MenuTrigger`/`SubmenuTrigger`, `useMenu`, the collection API (2024–2026).
- **Ariakit** — `accessibleWhenDisabled`, roving-tabindex/focus retention (2024–2026).
- **GitHub Primer** — `ActionMenu`/`ActionList`, the nav-vs-menu fork (2024–2026).
- **Shopify Polaris** — `ActionList` + `Popover` (menu composed from a list) (2024–2026).
- **IBM Carbon** — `Menu`/`MenuButton`/`OverflowMenu`/`ComboButton` (2024–2026).
- **Atlassian** `DropdownMenu`; **Base Web (Uber)** `Menu`/`StatefulMenu`; **Microsoft Fluent** `Menu`; **Google Material 3** Menu + Split/Combo button (expressive motion) (2024–2026).
- **Floating UI** — `safePolygon` / hover-intent, the submenu safe-triangle (2024–2026).
- **Apple HIG** — pull-down & pop-up buttons, context menus / `UIMenu` (2024–2026).
- WCAG 2.2 (W3C Recommendation, Oct 2023) — SC 4.1.2, 2.1.1, 2.1.2, 2.4.3, 1.4.13.

## 15. Agent-consumable schema

```yaml
identity:
  id: menu
  name: Menu
  aliases: [dropdown-menu, action-menu, action-list, overflow-menu, kebab-menu, popup-menu, context-menu, menubar]
  category: overlay
  status: stable
description: >
  A transient overlay of application COMMANDS / state toggles (the app-menu
  idiom). role=menu is for ACTIONS — NOT navigation (a dropdown of links is
  nav+disclosure+links, never role=menu — the most-misused ARIA pattern),
  NOT value-selection (→ listbox/Select), NOT text-filter (→ combobox). The
  go/choose/do test. Mechanically signed by DOM focus MOVING into the menu
  (roving tabindex) — the opposite of Combobox.
anatomy:
  parts:
    - "trigger: <button> aria-haspopup=menu + aria-expanded + aria-controls (inherits button; asChild merges onto a custom Button)"
    - "portal: lifts surface to document.body (escapes overflow:hidden / stacking; inherited)"
    - "content: role=menu (or menubar); owns positioning + roving-tabindex state"
    - "menuitem: the action row (default)"
    - "menuitemcheckbox / menuitemradio: stateful items (aria-checked); radio set in role=group; ItemIndicator (check/dot) when checked"
    - "group + label: role=group + non-focusable label via aria-labelledby"
    - "separator: role=separator (see divider)"
    - "leading icon (aria-hidden) / trailing shortcut hint (aria-hidden) / submenu trigger (menuitem + aria-haspopup -> SubContent)"
    - "menubar: role=menubar (persistent app bar — rich apps only)"
api:
  inherits:
    - "button (trigger mechanics, states, focus ring)"
    - "overlay-positioning-substrate (collision/flip, portal, Popover API + CSS Anchor Positioning, dismiss — established by select/combobox; eventual home popover/dialog)"
  shape: "composable parts (practice default) + convenience items/actions array"
  parts: [Menu(root: open/defaultOpen/onOpenChange), MenuTrigger(asChild), MenuContent, MenuItem, MenuGroup, MenuLabel, MenuSeparator, "MenuCheckboxItem(checked/onCheckedChange)", "MenuRadioGroup(value/onValueChange)+MenuRadioItem", MenuSub+MenuSubTrigger+MenuSubContent]
  callback: "onAction/onSelect keyed by item id — abstract DOM click so click + Enter + Space + type-ahead share one path (fire -> close -> restore focus to trigger)"
  stateful-items: "toggling a checkbox/radio item does NOT close the menu (vs plain item fires-and-closes)"
  positioning: "side/align/sideOffset/alignOffset/avoidCollisions — INHERITED from the overlay substrate, not re-derived"
  per-item: [disabled (still focusable), destructive/danger, icon, shortcut, "href (only when it legitimately navigates — rare)"]
states:
  item: [rest, "highlighted (hover AND keyboard focus unified — data-highlighted; avoid :focus rings that flicker on fast traversal)", active, "disabled (focusable + aria-disabled)", danger, "checked (stateful)"]
  menu: [closed, open, submenu-open]
variants:
  dropdown: "anchored to a button (common case)"
  context: "contextmenu event (right-click/long-press); anchored to pointer clientX/clientY; no persistent trigger"
  menubar: "persistent role=menubar; Left/Right walk adjacent menus (rich app only)"
  split-combo: "primary action segment + caret menu trigger (Carbon ComboButton / M3 expressive)"
  content: [with-icons, with-shortcuts, with-selection]
accessibility:
  wcag-criteria: ["4.1.2", "2.1.1", "2.1.2", "2.4.3", "1.4.13"]
  roles: "role=menu/menuitem/menubar — ONLY for application command menus; on navigation it is the cardinal anti-pattern"
  trigger-contract: "button + aria-haspopup=menu (or true) + aria-expanded + aria-controls"
  focus-model: "ROVING TABINDEX — DOM focus physically moves into the menu (first non-disabled item / container; active item tabindex=0, rest -1, .focus() called). Escape closes + RETURNS focus to trigger (else drops to body). Tab closes (NOT a focus-trap). Opposite of combobox's aria-activedescendant virtual focus."
  keyboard: "Down/Up cycle (wrap); Home/End; type-ahead (buffer cleared ~500ms); Enter/Space activate+close; Escape close; Right open-submenu / next-menubar; Left close-submenu / prev-menubar (RTL reverses the submenu arrows)"
  disabled-items: "FOCUSABLE for discoverability (APG) — keep in roving cycle + aria-disabled (Ariakit accessibleWhenDisabled / Radix [data-disabled]), not native disabled; skipped only for activation"
  stateful-items: "aria-checked; use for toggles/modes within an action menu, NOT as a Select substitute"
content:
  labels: "action verbs for commands; trailing '…' = opens further dialog/needs input; stateful items use the state noun/adjective"
  order: "frequency/domain; frequent at top; group with separator+label"
  destructive: "isolated at bottom, own group behind a separator, danger token PLUS position/label (never colour-only)"
  shortcuts: "right-aligned, OS-formatted (⌘N vs Ctrl+N), aria-hidden (binding lives globally / aria-keyshortcuts)"
  icons: "leading icons decorative (aria-hidden); reserve the icon column per group; never icon-only items"
motion:
  open: "ORIGIN-AWARE scale/fade from the trigger edge ~120-150ms (transform-origin at anchor; Radix --radix-…-transform-origin so it grows correctly even when collision-flipped)"
  submenu: "short fade behind a hover-intent delay (safe-triangle)"
  reduce-motion: "instant toggles, opacity only"
i18n:
  rtl: "surface mirrors (shortcut/icon edges swap, alignment flips); SUBMENU ARROWS REVERSE — Left opens / Right closes under dir=rtl (reading dir is mandatory)"
  type-ahead: "match composed characters (non-Latin / IME), not raw keystrokes"
  expansion: "+30–50% — intrinsic sizing (min/max-content) to a cap, then truncate w/ tooltip; no rigid max-width"
implementation:
  - "don't hand-roll — Radix DropdownMenu/ContextMenu/Menubar, React Aria useMenu, or Ariakit; skin the headless core"
  - "positioning inherited (portal escapes overflow:hidden/stacking; z-index a global token; Popover API + CSS Anchor Positioning eroding Floating-UI/portals — verify support)"
  - "submenu SAFE-TRIANGLE ('Amazon dropdown problem'): Floating UI safePolygon (bridge from cursor exit to SubContent corners) OR a simpler ~150-200ms setTimeout close-delay (avoids the polygon's pointer-events side bugs)"
  - "roving tabindex NOT a focus-trap — restore focus to trigger on close, close on Tab (a Dialog-style trap blocks tabbing through a form with menu triggers)"
  - "the nav-dropdown is a DIFFERENT component — disclosure button + <nav>/<ul> of <a href>, no role=menu, no roving tabindex, Tab walks links; document separately (Primer forks primitives to enforce)"
  - "context menu: intercept contextmenu event, anchor at pointer, provide a keyboard route (Shift+F10 / context-menu key)"
composition:
  stands-on: [button, overlay-positioning-substrate (select/combobox; eventual popover/dialog), icon, divider]
  alternative-to: [select, listbox, combobox, nav-disclosure (links — NOT role=menu), toolbar, inline-buttons]
  composed-by: [breadcrumbs (overflow menu), table-row-actions, split-combo-button]
  superseded-by: [select/listbox (value-selection), nav-disclosure (links), tree/dialog/routing (deep hierarchy)]
notes:
  contested:
    - "exactly where the menu-vs-nav-vs-listbox line falls (the defining call)"
    - "disabled-item focusable (APG/Ariakit/Radix default) vs hard-skip"
    - "menubar's relevance to web apps (desktop-app affordance; default to dropdowns)"
    - "stateful menuitemcheckbox/radio vs promoting to a listbox"
  trap:
    - "role=menu on navigation (the cardinal anti-pattern — strips link semantics, imposes roving tabindex)"
    - "missing submenu safe-triangle (premature close on diagonal traversal)"
    - "focus-trapping a menu like a dialog (blocks Tab-through)"
    - "non-origin-aware open animation that breaks when collision-flipped"
    - "hardcoded submenu arrow keys (must reverse in RTL)"
  inherited: "trigger from button; the entire overlay/positioning substrate from select/combobox (eventual popover/dialog)"
  evolution: "monolithic->composable parts; nav-is-not-a-menu hardened into law; Popover API + anchor positioning rebuilding the substrate; ActionList-composes-a-menu; disabled-but-focusable converged"
  unverified:
    - "external-supplied 2026 version numbers (Radix v1.x, React Aria v3.x, Ariakit v0.4.x, Primer v31.x, Carbon v11/v12, etc.)"
    - "Popover API / CSS Anchor Positioning support state (cross-brief, shared with select/combobox)"
    - "Material 3 'Expressive' spring-motion system (external claim; needs _source-text)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-menu/` (16 June 2026), the first brief to inherit the overlay/positioning substrate (established by select and combobox) as an explicit dependency, with the trigger inheriting button. The two passes converged almost completely — the menu-vs-listbox-vs-navigation disambiguation (the "do / go / choose" test; `role=menu` is for commands, never navigation links, never value-selection — the most-misused ARIA pattern), the roving-tabindex focus model (real DOM focus moves into the menu, Escape returns it to the trigger, Tab closes — the explicit opposite of Combobox's `aria-activedescendant` virtual focus), the menu-button `aria-haspopup`/`expanded`/`controls` contract, the submenu safe-triangle, disabled-but-focusable items, the stateful `menuitemcheckbox`/`menuitemradio` boundary, the dropdown/context-menu/menubar surfaces, composable parts over a monolithic items array, and `Menu` as the naming default. External-pass contributions folded in: the concrete disabled-but-focusable mechanism (Ariakit `accessibleWhenDisabled`, Radix `[data-disabled]`), the origin-aware-motion `--radix-…-transform-origin` technique, the safe-polygon-vs-`setTimeout` trade and the polygon's `pointer-events` side bug, the split/combo button pattern, the "Amazon dropdown problem" name, the type-ahead buffer timeout, the stateful-items-keep-the-menu-open rule, the RTL submenu-arrow reversal, and the ActionList-composes-a-menu architecture. Claude-pass contributions: the framing as the first overlay-substrate inheritor, the "do/go/choose" framing, and the forward-reference discipline toward Popover/Dialog. The 2026 version numbers, the Popover-API/anchor-positioning support state (shared with select/combobox), and the Material 3 expressive-motion claim are flagged unverified. Filed under Overlay rather than Navigation precisely because its central thesis is that a menu is not navigation. Conformant to `components/_schema.md`. Closes the application-command-overlay lane; Popover and Dialog are the overlay primitives it forward-references.*

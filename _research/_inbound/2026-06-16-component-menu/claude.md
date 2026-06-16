# Menu — field-truth study (Claude pass)

## 1. Framing
A Menu is a popup list of **commands/actions** in an application — the desktop app-menu idiom ported to the web (File, Edit, "Duplicate", "Delete", the kebab/overflow "⋮", the row-action menu). It stands on two briefed substrates: the **trigger is a Button** (`aria-haspopup` + `aria-expanded` + `aria-controls` — see button) and the **anchored-popup/positioning machinery is the overlay substrate Select and Combobox already established** (collision/flip, CSS Anchor Positioning / Popover API / Floating UI, focus return, outside-dismiss — see select, combobox; forward-ref Popover/Dialog when briefed). Menu is also the overflow affordance Breadcrumbs leans on (see breadcrumbs).

**What it is** — a transient list of actions the user invokes. **What it isn't**, and this is the defining decision because `role=menu` is the **most-misused ARIA pattern on the web**:
- **Not navigation.** A dropdown of *links* (a site-nav flyout, an account menu of page links) is a **`<nav>` + disclosure button + a plain list of links**, NOT `role=menu`. `role=menu`/`menuitem` is an *application* widget — it strips the links of their link semantics and imposes arrow-key-only focus that confuses AT users expecting a list of links. The "dropdown-nav-is-a-`role=menu`" pattern is the cardinal anti-pattern.
- **Not value selection.** Choosing a *value* (sort order, a country, a filter) is a **Listbox/Select** (see select) — `aria-selected` options that hold a value. A Menu *fires actions*; it doesn't hold a selected value (except the stateful-item exception, §below).
- **Not a text-filtered picker** — that's Combobox (see combobox).

The one-line test: **Menu = "do something" (commands); Listbox/Select = "choose a value"; Navigation = "go somewhere" (links).** Why systems disagree: where the menu-vs-nav-vs-listbox line falls, the **submenu** hover mechanics, whether menus carry **stateful items**, and the menubar's relevance to web (vs. native) apps.

## 2. Anatomy and parts
- **Trigger / menu button** — a `<button>` with `aria-haspopup="menu"` (or `true`), `aria-expanded`, `aria-controls` (see button). A kebab/overflow `⋮`, a "More actions" button, a split/combo button, or a right-click target (context menu).
- **Menu surface** — the popup container (`role="menu"`), portalled + positioned by the overlay substrate.
- **`menuitem`** — the action row (the default item).
- **`menuitemcheckbox` / `menuitemradio`** — stateful items (a menu that toggles a setting / picks one of a set in place, §4/§6).
- **group + group label** — `role="group"` + `aria-label`/`aria-labelledby` for a labelled section.
- **separator** — `role="separator"` between groups (decorative divider; see divider).
- **leading icon** (decorative — see icon), **trailing keyboard-shortcut hint** ("⌘C", visually-shown, programmatically associated or `aria-keyshortcuts`), **submenu indicator** (a trailing chevron on a parent `menuitem` with `aria-haspopup`).
- **destructive/danger item** — a "Delete" styled with the danger token (still a `menuitem`; the colour is not the only signal — §7).
- **menubar** (`role="menubar"`) — the persistent horizontal app-menu bar (rich desktop-style apps only, §5).

## 3. Properties / API
- **Composition (the converged shape, Radix-style parts):** `Menu` (root, owns open state) / `MenuTrigger` (or `MenuButton`) / `MenuContent` (the surface) / `MenuItem` / `MenuGroup` + `MenuLabel` / `MenuSeparator` / `MenuCheckboxItem` / `MenuRadioGroup` + `MenuRadioItem` / `MenuSub` + `MenuSubTrigger` + `MenuSubContent`. The practice default mirrors this composable parts API (with a convenience `items`/`actions` array for the data-driven case — React Aria's `Menu` + `items`).
- **`onAction` / `onSelect`** — fires with the chosen item's key/id (the menu's core callback — actions, not a bound value). Per-item `onSelect`/`onClick` is the alternative.
- **Controlled open** — `open`/`defaultOpen`/`onOpenChange` (inherits the overlay substrate).
- **Stateful items** — `MenuCheckboxItem` (`checked`/`onCheckedChange`) and `MenuRadioGroup` (`value`/`onValueChange`) + `MenuRadioItem`.
- **Submenu** — `MenuSub`/`MenuSubTrigger`/`MenuSubContent`.
- **Per-item:** `disabled`, `destructive`/`danger`, `icon`, `shortcut`, `href` (when a menu item legitimately navigates — but see the nav-vs-menu rule, §5).
- **Positioning props** — `placement`/`align`/`offset`/`collision` **inherited from the overlay substrate** (see select/combobox); not re-derived here.

## 4. States and variants
- **Item states:** rest / hover / focus (the active item — note hover and keyboard focus are unified in a menu: moving the mouse over an item makes it the focused item) / disabled (focusable but not actionable — §6) / danger/destructive / checked (stateful items).
- **Menu states:** closed / open / submenu-open.
- **Variants:**
  - **Dropdown menu** — opens from a button (the common case).
  - **Context menu** — opens at the pointer on right-click / long-press (`contextmenu` event); same `role=menu` content, different trigger + positioning.
  - **Menubar** — a persistent `role="menubar"` of top-level menus (rich app only).
  - **With-icons / with-shortcuts / with-selection (stateful)** — content variants.
  - **Split / combo button** — a primary action + an adjacent menu trigger (Carbon ComboButton).

## 5. Usage guidance
- **Use a Menu** for a list of **actions/commands** triggered from a button, a kebab/overflow, or right-click — especially when there are too many actions to surface inline (the overflow pattern).
- **Don't use a Menu for:**
  - **Navigation** (links to pages) → a `<nav>` + disclosure + a list of links. *This is the most important boundary.* If the items are `<a href>`s that go places, it's not a `role=menu`.
  - **Selecting a value** (sort, filter, a form field) → Select/Listbox (see select) — `aria-selected` options, a bound value.
  - **Text-filtering a long list** → Combobox (see combobox).
  - **A handful of always-visible actions** → just render Buttons/a Toolbar; a menu hides actions behind a click.
- **Decision frameworks:**
  - **Menu vs. Navigation vs. Listbox:** actions → Menu; links → nav+disclosure; values → Listbox. (The "go / choose / do" test.)
  - **Menu vs. Select:** does the row *fire an action* (Menu) or *set a persisted value shown on the trigger* (Select)? A Select's trigger reflects the current value; a Menu's trigger is a static label ("Actions", "⋮").
  - **Menubar or not:** a persistent `menubar` is a desktop-app affordance (an IDE, a design tool, Google Docs). Most web apps **don't** want one — it imports complex two-dimensional arrow-key semantics for little benefit. Default to dropdown menus.

## 6. Accessibility
- **Roles:** `role="menu"` (surface) containing `menuitem` / `menuitemcheckbox` / `menuitemradio`, optionally grouped by `role="group"` (+ label) and divided by `role="separator"`; `role="menubar"` for the persistent bar. **These roles are only correct for actual application command menus** — applying them to navigation is the headline a11y error (§5).
- **The menu-button contract:** the trigger is a `<button>` with `aria-haspopup="menu"` (or `true`), `aria-expanded` reflecting open state, and `aria-controls` pointing at the menu.
- **The focus model (the roving-tabindex side of the combobox fork):** when the menu opens, **DOM focus moves into the menu** — onto the first item (keyboard-opened) or the menu container — and arrow keys *move actual focus* between items via **roving tabindex** (one item is `tabindex="0"`, the rest `-1`). **Escape closes and returns focus to the trigger.** **Tab closes the menu** and moves focus on (a menu is not a focus-trap like a dialog — it dismisses on Tab). This is the explicit contrast with **Combobox**, where DOM focus *stays on the input* and the active option is tracked by `aria-activedescendant` (see combobox). Menu = real focus moves; Combobox = virtual focus.
- **Keyboard:** Up/Down move between items (wrapping), Home/End jump, **type-ahead** focuses the next item matching typed characters, Enter/Space activate **and close**, Escape closes, Right opens a submenu / moves to the next menubar menu, Left closes a submenu / moves to the previous menubar menu.
- **Disabled items are conventionally focusable** in menus (APG allows it, unlike most widgets) so they're discoverable by keyboard/AT — `aria-disabled="true"`, skipped for activation, not removed from arrow navigation. (Some systems hard-skip them; the practice default follows APG — focusable + `aria-disabled`.)
- **Stateful items:** `menuitemcheckbox`/`menuitemradio` carry `aria-checked`; a menu that's really *selecting a value* in place may be better as a listbox — use stateful items for *toggles/modes within an action menu*, not as a Select substitute.
- **WCAG SCs:** 4.1.2 (name/role/value), 2.1.1 / 2.1.2 (keyboard, no trap), 2.4.3 (focus order — return to trigger), 1.4.13 (content on hover/focus — submenus dismissable/persistent), 2.5.3, plus the trigger's Button SCs.

## 7. Content guidelines
- **Action-verb labels** — menu items are commands: "Duplicate", "Move to…", "Delete" (a trailing "…" signals the action opens a further dialog/needs more input). Title or sentence case per the system's convention, applied consistently.
- **Ordering & grouping** — order by frequency/importance or logical grouping; group related actions with a separator + optional group label; keep the **destructive action separated** (its own group at the bottom) so it isn't fat-fingered, and style it with the danger token *plus* its position/label (colour is not the only carrier — see the badge/contrast discipline).
- **Shortcut hints** — right-aligned, formatted per platform (⌘ vs Ctrl); they *display* the shortcut (the actual binding lives globally / via `aria-keyshortcuts`).
- **Icon discipline** — leading icons are decorative (`aria-hidden`); don't rely on icon-only menu items (they need text labels).
- **Keep menus shallow and short** — a long menu is a sign it should be a Listbox/search; deep submenus are a sign of an IA problem.

## 8. Motion and transition
Origin-aware open/close: the surface scales/fades from the trigger edge (~120–150ms, `transform-origin` at the anchor), consistent with the overlay substrate (see select/combobox/popover). Submenus reveal with a short fade; respect a small **hover-intent delay** before opening/closing a submenu (the safe-triangle, §11) so a diagonal mouse path doesn't thrash. Under `prefers-reduced-motion: reduce`, snap open/closed (opacity only). No motion on item hover beyond a background change. (See 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** flips the whole surface: submenus open to the **left**, the submenu chevron mirrors, leading icons and trailing shortcut hints swap edges (logical properties; the overlay substrate's placement logic mirrors automatically). Context-menu positioning anchors from the opposite corner.
- **Type-ahead** must handle non-Latin scripts and IME composition (match on composed characters, not keystrokes).
- **Text expansion** (+30–50%) — menu min/max-width must accommodate longer labels + the shortcut hint without truncation; avoid fixed-width menus. (See 13-internationalization-and-rtl.)

## 10. Naming
The popup-of-actions is most often **`Menu`** (React Aria, Base Web, Material, Carbon) or **`DropdownMenu`** (Radix, Atlassian, shadcn); the action-list framing is **`ActionMenu`**/**`ActionList`** (Primer, Polaris build the menu from a list primitive + Popover); the icon-overflow specialisation is **`OverflowMenu`** (Carbon) / kebab menu; the right-click surface is **`ContextMenu`**; the persistent bar is **`Menubar`**. **The practice default: `Menu`** as the umbrella with composable parts (`MenuTrigger`/`MenuContent`/`MenuItem`/…), surfacing **`ContextMenu`** and **`Menubar`** as sibling triggers/variants of the same content primitive, and treating **overflow/kebab** as a `Menu` with an icon-button trigger rather than a distinct component. Aliases to map: `DropdownMenu`, `ActionMenu`, `ActionList`, `OverflowMenu`, `PopupMenu`, `ContextMenu`, `Menubar`.

## 11. Implementation notes
- **Don't hand-roll — Radix `DropdownMenu`/`ContextMenu`/`Menubar` or React Aria `Menu`/`useMenu` are the references.** They solve the roving tabindex, type-ahead, submenu timing, portal/positioning, and dismiss semantics that are easy to get subtly wrong. Skin the headless core.
- **Positioning is inherited** from the overlay substrate (see select/combobox): portal to escape `overflow:hidden`/stacking-context traps, collision-aware flip/shift, anchor to the trigger; the Popover API + CSS Anchor Positioning are collapsing the portal/z-index machinery (the same current-platform shift flagged in select — verify support, treat as progressive enhancement).
- **The submenu safe-triangle** — when the pointer moves diagonally from a parent item toward its open submenu, it briefly crosses sibling items; naively closing the submenu on `mouseleave` of the parent makes flyouts unusable. The fix: a **hover-intent delay** + tracking the pointer's trajectory toward the submenu's bounding box (the "safe triangle"), keeping the submenu open while the pointer aims at it. Radix/React Aria implement this; hand-rolled menus almost always miss it.
- **Focus management:** roving tabindex within the menu, restore focus to the trigger on close (Escape/select/outside-click), close on Tab. Not a focus trap (that's Dialog).
- **The nav-dropdown is built differently:** a navigation flyout is a disclosure `<button aria-expanded>` revealing a `<nav>`/`<ul>` of `<a href>` links — **no `role=menu`**, no roving tabindex; Tab moves through the links normally. Document this as a separate pattern so teams don't reach for `Menu` for nav.
- **Context menu** — suppress/augment the native `contextmenu` event, position at the pointer, and provide a keyboard route (Shift+F10 / the context-menu key) since right-click isn't keyboard-accessible on its own.

## 12. Related and alternative components
- **Composes with / stands on:** Button (the trigger — see button), Popover/Dialog (the overlay/positioning substrate — forward-ref), Icon (leading icons, kebab, submenu chevron — see icon), Divider (the `role=separator` — see divider), the framework router (when a menu item legitimately navigates).
- **Alternative to:** Select/Listbox (choosing a value — see select), Combobox (text-filtered picker — see combobox), a Navigation disclosure (links — *not* a `role=menu`), a Toolbar (always-visible actions), inline Buttons (few actions, no need to hide them).
- **Composed by:** Breadcrumbs (the overflow/collapse menu — see breadcrumbs), Table/row actions, Select (its listbox is a *sibling* overlay, not a menu), the split/combo button.
- **Superseded by:** Listbox/Select when the surface is really value-selection; a nav disclosure when the items are links.

(The first brief to stand on the overlay/positioning substrate as an explicit inheritance — the machinery Select and Combobox established, now reused. The roving-tabindex counterpart to Combobox's `aria-activedescendant` virtual-focus model. See button for the trigger, select/combobox for the overlay substrate + the listbox-vs-menu line, breadcrumbs for the overflow consumer, divider for the separator, icon for the glyphs. 03-component-library; 29 for the docs template. Popover and Dialog are the unbriefed overlay primitives this forward-references.)

## 13. Field POV evolution
1. **The "dropdown-nav-is-not-a-`role=menu`" correction hardened** — a11y practice now firmly separates application menus (`role=menu`) from navigation flyouts (disclosure + links); using `role=menu` for site nav is a documented anti-pattern.
2. **Composable parts converged** (Radix `DropdownMenu.*`) — over the old monolithic `items`-array menu — giving consumers control of item rendering while the library owns focus/keyboard/positioning.
3. **The overlay substrate is being rebuilt on the platform** — Popover API + CSS Anchor Positioning are collapsing the portal/z-index/Floating-UI machinery menus share with Select/Combobox (cross-brief, current-platform-state — verify).
4. **ActionList-composes-a-menu** — Primer/Polaris build menus from a list primitive + Popover rather than a bespoke Menu, separating presentation (list) from behaviour (overlay + roving focus).

## 14. Sources cited
(Conservative; reconcile with external.) **WAI-ARIA APG** — Menu/Menubar pattern, Menu Button pattern (roles, the roving-tabindex focus model, keyboard, disabled-item focusability); **Radix UI** `DropdownMenu`/`ContextMenu`/`Menubar` (the de facto headless reference; safe-triangle submenu, composable parts) (2024–2026); **Adobe Spectrum / React Aria** `Menu`/`MenuTrigger`/`SubmenuTrigger`, `useMenu` (2024–2026); **Shopify Polaris** `ActionList` + `Popover` (menu composed from a list) (2024–2026); **GitHub Primer** `ActionMenu`/`ActionList` (2024–2026); **IBM Carbon** `Menu`/`MenuButton`/`OverflowMenu`/`ComboButton` (2024–2026); **Atlassian** `DropdownMenu` (2024–2026); **Base Web (Uber)** `Menu`/`StatefulMenu` (2024); **Microsoft Fluent** `Menu` (2024–2026); **Ariakit** `Menu` (2024–2026); **Google Material 3** Menu (2024); **Apple HIG** — pull-down & pop-up buttons, context menus / `UIMenu` (2024–2026). WCAG 2.2 (Oct 2023) — 4.1.2, 2.1.1, 2.1.2, 2.4.3, 1.4.13.

## 15. Agent-consumable schema (conform to _schema.md in menu.md)
identity(Menu; aliases DropdownMenu/ActionMenu/ActionList/OverflowMenu/PopupMenu/ContextMenu/Menubar; overlay/navigation-adjacent; stable)/description(a popup list of COMMANDS/ACTIONS — the app-menu idiom; NOT navigation (links → nav+disclosure), NOT value-selection (→ listbox/Select), NOT text-filter (→ combobox); the go/choose/do test)/anatomy(trigger=button[aria-haspopup]; surface role=menu; menuitem/menuitemcheckbox/menuitemradio; group+label; separator; leading icon; trailing shortcut; submenu trigger; menubar)/api(inherits: button (trigger), overlay-positioning-substrate (select/combobox); composable parts Menu/Trigger/Content/Item/Group/Label/Separator/CheckboxItem/RadioGroup+RadioItem/Sub+SubTrigger+SubContent; onAction/onSelect by key; controlled open; per-item disabled/danger/icon/shortcut; positioning props inherited)/states(item rest/hover=focus/disabled(focusable)/danger/checked; menu closed/open/submenu-open; variants dropdown/context/menubar/split-combo/with-icons/with-shortcuts/with-selection)/accessibility(role=menu/menuitem/menubar ONLY for app commands; menu-button aria-haspopup+expanded+controls; ROVING TABINDEX — real focus moves into menu, Esc returns to trigger, Tab closes (not a trap); contrast combobox aria-activedescendant virtual focus; type-ahead; disabled items focusable+aria-disabled per APG; menuitemcheckbox/radio aria-checked; SC 4.1.2/2.1.1/2.1.2/2.4.3/1.4.13)/content(action-verb labels, '…' for further-input; group + separate destructive at bottom w/ danger token NOT colour-only; shortcut hints right-aligned; decorative icons; keep shallow)/motion(origin-aware open ~120-150ms from trigger edge; submenu hover-intent delay; reduce-motion snaps)/i18n(RTL flips surface + submenu opens left + chevron mirror + icon/shortcut edge swap; type-ahead handles non-Latin/IME; text expansion → no fixed-width)/implementation(don't hand-roll — Radix DropdownMenu/ContextMenu/Menubar or RA useMenu; positioning inherited (portal, collision-flip, Popover API + anchor positioning shift); submenu SAFE-TRIANGLE hover-intent; roving focus + restore-to-trigger, close on Tab; nav-dropdown = disclosure+links NOT role=menu; context menu needs keyboard route Shift+F10)/composition(stands-on button + overlay substrate; composes-with icon, divider, router; alternative-to select/listbox, combobox, nav-disclosure, toolbar, inline buttons; composed-by breadcrumbs overflow + row-actions; superseded-by listbox/select when value-selection, nav-disclosure when links)/notes(contested: menu-vs-nav-vs-listbox line (the defining call); disabled-item focusable (APG) vs hard-skip; menubar relevance to web; stateful-items vs listbox. trap: role=menu on navigation (the cardinal anti-pattern); missing safe-triangle; focus-trapping a menu like a dialog. evolution: nav-is-not-a-menu hardened; composable parts converged; Popover API + anchor positioning rebuild; ActionList-composes-a-menu. unverified: external 2026 version numbers; Popover API / anchor-positioning support state (cross-brief).)

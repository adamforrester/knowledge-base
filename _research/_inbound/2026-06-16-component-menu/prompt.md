You are researching the Menu component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what menus are,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Menu is an Overlay/Navigation-adjacent brief that STANDS ON two already-
briefed substrates:
- THE TRIGGER inherits the BUTTON component (components/button.md) — the
  menu button is a <button> with aria-haspopup + aria-expanded +
  aria-controls. Don't re-derive Button.
- THE OVERLAY / POSITIONING MACHINERY is the same substrate Select and
  Combobox already established (components/select.md, components/combobox.md):
  the anchored popup, collision/flip, the CSS Anchor Positioning / Popover
  API / Floating UI stack, focus return, scroll/dismiss behaviour. Treat
  that positioning substrate as INHERITED (forward-reference Popover/Dialog,
  not yet briefed) and concentrate on what is Menu-specific. Menu is also
  the overflow affordance Breadcrumbs leans on (components/breadcrumbs.md).

THE DEFINING MENU-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE MENU-vs-LISTBOX-vs-NAV DISAMBIGUATION (the defining decision, and
  the most-misused ARIA pattern on the web): role=menu/menuitem is for a
  list of COMMANDS/ACTIONS in an application (the desktop app-menu
  idiom) — NOT for navigation (a dropdown of links is a <nav> +
  disclosure + links, NOT role=menu) and NOT for value selection (that's
  listbox/Select). Resolve the rule: when is it a Menu (actions), when is
  it Navigation (links in a disclosure), when is it a Listbox (selecting a
  value). The "dropdown-nav-is-not-a-menu" anti-pattern.
- THE FOCUS MODEL — focus MOVES INTO the menu (roving tabindex; DOM focus
  lands on the active menuitem), Escape closes and RETURNS focus to the
  trigger, Tab closes the menu and moves on. Contrast explicitly with
  Combobox (DOM focus stays on the input, aria-activedescendant) — Menu is
  the roving-tabindex side of that fork.
- THE MENU BUTTON / TRIGGER PATTERN — button aria-haspopup="menu" (or
  true) + aria-expanded + aria-controls; open on click/Enter/Space/Down;
  the first-item-focused-on-open vs trigger-focused question.
- KEYBOARD — Up/Down arrows, Home/End, type-ahead, Enter/Space activate +
  close, Escape close, Left/Right for submenus and menubar.
- STATEFUL ITEMS — menuitemcheckbox and menuitemradio (the menu that
  holds togg*able* state, not just fires actions); when a "menu" should
  actually be a listbox instead.
- SUBMENUS / FLYOUTS — aria-haspopup on the parent menuitem, the
  diagonal-mouse-path / "safe triangle" hover-intent problem, the
  open/close delay, deep-nesting discouragement.
- CONTEXT MENU (right-click / contextmenu event) vs DROPDOWN MENU vs
  MENUBAR (persistent desktop-style bar) — the three menu surfaces and
  when each applies.
- DISABLED ITEMS — menus conventionally allow FOCUSING disabled items
  (aria-disabled, focusable) unlike most widgets; resolve the practice's
  stance.
- ANATOMY EXTRAS — sections/groups, separators (role=separator), group
  labels/headers, leading icons, trailing keyboard-shortcut hints,
  destructive/danger items.

Field-leader systems to survey (web): Radix UI (DropdownMenu / ContextMenu
/ Menubar — the de facto headless reference), Adobe Spectrum / React Aria
(Menu, MenuTrigger, SubmenuTrigger), Shopify Polaris (ActionList + Popover
— note Polaris composes menus from a list primitive), GitHub Primer
(ActionMenu, ActionList), IBM Carbon (Menu, MenuButton, OverflowMenu,
ComboButton), Atlassian (DropdownMenu), Base Web (Uber) (Menu /
StatefulMenu), Microsoft Fluent, Ariakit, Google Material 3 (Menu). Mobile
reference where relevant: Apple HIG (context menus / UIMenu / pull-down &
pop-up buttons), Material 3. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Button trigger and the
overlay/positioning substrate; flag unverified claims under
notes.unverified).

1. Framing — what it is, what it isn't, why systems disagree; the
   menu-vs-listbox-vs-nav disambiguation up front.
2. Anatomy and parts — trigger (menu button), the popup menu surface,
   menuitem / menuitemcheckbox / menuitemradio, group + group label,
   separator, leading icon, trailing shortcut hint, submenu trigger.
3. Properties / API — the trigger + content composition (Radix-style
   parts), items vs children, onAction/onSelect, controlled open state,
   stateful items, submenu API, positioning props (inherited).
4. States and variants — item states (rest/hover/focus/disabled/danger),
   open/closed; dropdown vs context menu vs menubar variants; with-icons /
   with-shortcuts / with-selection.
5. Usage guidance — Menu (actions) vs Navigation (links) vs Listbox/Select
   (values) vs Combobox; the overflow/kebab menu; when a menubar is
   warranted (rich app) vs not (most web apps).
6. Accessibility — role=menu/menuitem/menubar, the menu-button
   aria-haspopup/expanded/controls contract, the roving-tabindex focus
   model + Escape-returns-focus, type-ahead, disabled-item focusability,
   the nav-is-not-a-menu rule, WCAG SCs.
7. Content guidelines — action-verb labels, ordering, grouping,
   destructive-item placement, shortcut-hint formatting, icon discipline.
8. Motion and transition — open/close (origin-aware), submenu reveal,
   reduce-motion.
9. Internationalization — RTL (submenu side flip, shortcut + icon side),
   type-ahead in non-Latin scripts, text expansion.
10. Naming — Menu / DropdownMenu / ActionMenu / OverflowMenu / Menubar /
    ContextMenu / ActionList; the practice's default; aliases.
11. Implementation notes — the headless-vs-opinionated split (Radix as the
    reference), positioning inherited from the overlay substrate, the
    submenu safe-triangle, focus trap vs roving, portal/z-index, the
    nav-dropdown built as disclosure+links not role=menu.
12. Related and alternative components — typed relationships (Button
    trigger, Popover/Dialog overlay substrate, Select/Combobox/Listbox,
    Tabs, the nav disclosure, Toolbar, Breadcrumbs overflow).
13. Field POV evolution — recent shifts (Popover API + anchor positioning,
    the ActionList-composes-a-menu approach, the nav-is-not-a-menu
    correction hardening).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a menu is — explain the
menu-vs-listbox-vs-nav disambiguation, the roving-tabindex focus model
(and how it differs from combobox), the menu-button aria contract, the
submenu safe-triangle problem, the stateful-item (menuitemcheckbox/radio)
boundary, and the dropdown-nav-is-not-a-role=menu correction that field
leaders and a11y practice now enforce.

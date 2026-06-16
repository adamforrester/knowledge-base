# Menu — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/menu.md`; version numbers and the Material 3 expressive-motion claim flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Menu Component: Field-Truth Analysis and Implementation Standard

## 1. Framing
The Menu component represents one of the most mechanically dense and theoretically overloaded UI paradigms. A "Menu" invokes the WAI-ARIA role="menu" model: a transient surface presenting a list of commands/executable actions. The colloquial "dropdown menu" has conflated three different patterns: the application menu (executing actions), the listbox (selecting values), and disclosure navigation (routing). Resolving this disambiguation is the defining architectural decision; misapplying role="menu" is the most pervasive accessibility anti-pattern on the web.

A component qualifies as a Menu exclusively when it presents executable commands or application state toggles ("Duplicate", "Delete", "Print", "Show Sidebar"). Selecting a value for a form/filter/dataset is a Listbox/Select. Selecting a value while typing to filter is a Combobox. A transient popup of navigational hyperlinks (the "nav dropdown") must NOT use role="menu" — assistive technologies expect roving tabindex and arrow-key bindings for menus, which standard nav suffers from. The field-leader standard for nav dropdowns is the Disclosure pattern: <button aria-expanded="true"> + <nav> + <a> list, preserving sequential tabbing. role="menu" must never be applied to site navigation.

The Menu stands on two substrates: the trigger inherits Button (aria-haspopup, aria-expanded, aria-controls), and the overlay/positioning machinery is the substrate Select/Combobox established (anchored popup, collision, flip, CSS Anchor Positioning, Floating UI, native Popover API). This frees focus on Menu-specifics: roving-tabindex focus, submenu safe-triangles, disabled-item focusability, and stateful items.

## 2. Anatomy and Parts
Modular compositional APIs (Radix UI, Ariakit are the de facto reference) separate triggers from floating content, wrappers, and item variants. Parts: Trigger (button; aria-haspopup="menu", aria-expanded, aria-controls; Radix asChild; React Aria MenuTrigger); Portal (extracts content to document.body, escapes z-index/overflow:hidden); Content/Overlay (role=menu or menubar; positioning + roving tabindex); Item (menuitem); CheckboxItem (menuitemcheckbox; aria-checked; bypasses close-on-interact); RadioGroup (group; mutual exclusion); RadioItem (menuitemradio; aria-checked); Group (group; organizational); Label/Header (non-focusable; aria-labelledby); Separator (separator or aria-hidden); Sub (nested wrapper); SubTrigger (menuitem + aria-haspopup); SubContent (nested menu; safe polygons); ItemIndicator (checkmark/dot when checked); Shortcut Hint (trailing; aria-hidden="true").

GitHub Primer / Shopify Polaris compose the Menu from a lower-level ActionList primitive that takes on role=menu + roving tabindex when wrapped in ActionMenu/Popover. IBM Carbon ships OverflowMenu and ComboButton macro-patterns; underlying nodes are consistent.

## 3. Properties / API
Headless DOM composition (Radix/Ariakit) vs data-driven collection rendering (React Aria). Practice default favors headless composition. Radix: DropdownMenu.Root (open, onOpenChange, defaultOpen); DropdownMenu.Trigger (asChild merges ARIA + listeners onto a custom Button without extra wrappers); decoupled content. React Aria: Collection API (items array or <Item> children parsed for internal state, disabled keys, focus). Selection callback diverges: onClick vs onSelect (Radix) vs onAction (React Aria/Polaris). Standard practice: abstract DOM click into a synthetic onAction/onSelect so Enter/Space/type-ahead and pointer click share one path (act, close, restore focus to trigger). Positioning props (side, sideOffset, align, alignOffset, avoidCollisions) inherited from the overlay substrate (Floating UI / CSS Anchor Positioning). Stateful: CheckboxItem/RadioItem with checked (boolean | 'indeterminate') + onCheckedChange; interacting maintains open state for rapid toggling.

## 4. States and Variants
Item states: Rest; Highlighted/Focused (roving tabindex or hover; data-highlighted/data-active-item/data-focused, not native :focus rings); Active/Pressed; Danger/Destructive (critical token); Disabled (focusability debate).

Disabled Item Focusability Controversy: removing disabled items from focus order means screen reader users arrowing the list skip them entirely, unaware the action exists. APG: when discoverability matters, disabled items should remain focusable during arrow navigation. Ariakit accessibleWhenDisabled retains the item in the roving cycle with aria-disabled rather than native disabled; Radix styles via [data-disabled] while keeping it accessible. Practice default: disabled items must receive virtual/DOM focus during arrow navigation, communicating state via aria-disabled.

Surface variants: Dropdown Menu (left-click/tap on a Menu Button, anchored to trigger rect); Context Menu (contextmenu event, anchored to clientX/clientY, no persistent trigger); Menubar (persistent horizontal File/Edit/View array; arrow left/right opens adjacent dropdowns).

## 5. Usage Guidance
Menu vs Listbox: Menu for items that trigger actions/commands/state toggles; Listbox/Select for picking a value to submit/filter. Menu = application command center; Listbox = data input. Menu vs Navigation: hyperlinks routing to URLs must use Disclosure (nav + toggle button), not Menu. Overflow/Kebab Menu (vertical three-dot) for exhausted horizontal space in toolbars/table rows/cards; Carbon OverflowMenu optimizes dense tables; destructive actions isolated at the bottom. Combo/Split Button: a primary action + adjacent caret menu (Material 3 expressive). Deep nesting limits: discourage nesting deeper than one level; safe hover polygons demand fine motor dexterity; for deep hierarchy use Tree View, multi-step Dialog, or full-page routing.

## 6. Accessibility
ARIA contract: trigger role=button + aria-haspopup="menu" (or true); aria-expanded toggles; aria-controls -> menu content id. Container role=menu; items role=menuitem.

Roving Tabindex Focus Model: contrast with Combobox (focus stays on the input; aria-activedescendant highlights options). A Menu physically moves DOM focus into the floating surface. On open the focus manager finds the first non-disabled item, sets it tabindex=0 and others tabindex=-1; ArrowDown intercepts, prevents scroll, moves tabindex and calls .focus() on the new item, so screen readers announce label/role/position.

Keyboard: Enter/Space (trigger: opens + focuses first item; item: executes, closes, returns focus to trigger); ArrowDown (opens/moves to first; cycles down with wrap); ArrowUp (optional opens to last; cycles up); ArrowRight (next menubar item; on SubTrigger opens submenu + focuses first); ArrowLeft (previous menubar item; in submenu closes + returns to parent SubTrigger); Escape (closes menu + parent submenus; MUST restore focus to the trigger — else catastrophic disorientation); Alphanumeric type-ahead (keystroke buffer, ~500ms timeout).

## 7. Content Guidelines
Action verbs ("Export document", "Invite users"); state toggles use nouns/adjectives ("Dark Mode", "Show Grid"). Group by domain; frequent actions at top; destructive actions at the bottom, isolated by a Separator, styled with danger/critical token, never adjacent to the primary action. Icon discipline: leading icons optional but consistent within a group; reserve the icon column for the group. Shortcut hints: trailing, right-aligned, OS-native (⌘ N macOS, Ctrl+N Windows), hidden from screen readers via aria-hidden="true".

## 8. Motion and Transition
Origin-aware: menu scales/slides from the trigger corner; collision flips must not break the origin. Radix computes --radix-dropdown-menu-content-transform-origin in real time from collision boundaries, consumed in @keyframes so the menu grows organically out of the trigger regardless of where Popover rendered it. Material 3 introduces expressive motion-physics (spatial springs replacing linear curves). All transitions obey prefers-reduced-motion (instant zero-ms toggles).

## 9. Internationalization
RTL: geometry inverts — trailing shortcuts shift left, leading icons right; collision boundaries and preferred alignments invert (right-align LTR -> left-align RTL). Submenu traversal logic must inspect dir: under dir="rtl", ArrowLeft opens a submenu and ArrowRight closes it. Hardcoding directional keys without the localization context is a major i18n failure. Text expansion: translated verbs need 30–50% more width; use intrinsic sizing (min-content/max-content) up to a viewport limit, then truncate with ellipsis + tooltip.

## 10. Naming
Fragmented. React Aria / Material 3 / Base Web: Menu (cleanest mapping to role=menu). Radix UI / Atlassian: DropdownMenu (differentiates from ContextMenu/Menubar). GitHub Primer: ActionMenu (composed under ActionList). Shopify Polaris: ActionList + Popover. IBM Carbon: OverflowMenu, ComboButton. Recommended standard: expose the root as Menu; expose ContextMenu/Menu.Overflow as named sub-variants on the same primitive + focus engine.

## 11. Implementation Notes
Submenu Safe-Triangle: hovering a SubTrigger opens SubContent adjacently; reaching it requires diagonal traversal over sibling items; naive mouseenter closes the submenu prematurely (the "Amazon dropdown menu problem"). Floating UI resolves via a safe polygon connecting cursor exit coords to SubContent corners; while the pointer stays inside, the submenu refuses to close. Secondary bug: a polygon DOM node with pointer-events:auto blocks underlying clicks/scroll — managed via requireIntent, cursor velocity, selective pointer-events negation; or a simpler 150–200ms setTimeout close delay bypassing SVG polygons.

Focus Trapping vs Roving Tabindex: Dialogs use a Focus Trap (inert background, Tab swept back). Menus use Roving Tabindex only; Tab closes the menu and moves focus to the next tabbable element. Misapplying a focus trap prevents power users from tabbing through a form with menu triggers.

Portals and Z-Index: menus inside overflow:hidden / narrow sidebars / absolute cards clip if rendered inline; the Portal extracts the node to document.body; z-index becomes a global token.

## 12. Related and Alternative Components
Button (trigger); Popover/Dialog (overlay substrate — collision, portal, flip, outer-click dismissal); Select/Listbox (form values; aria-activedescendant, focus stays on input); Combobox (text input + listbox, type-to-filter); Disclosure Navigation (Button + <nav>; the accessible replacement for routing dropdowns).

## 13. Field POV Evolution
Monolithic block components (<Menu items={data}/>) -> headless compositional primitives (Radix, React Aria; Menu.Root/Trigger/Item/Separator). "Nav-is-not-a-menu" hardening into non-negotiable law (audits flag role=menu on nav; Primer forks ActionList for menus vs separate list structures for nav). CSS Anchor Positioning + native Popover API eroding reliance on Floating UI (anchor() functions delegate collision/flip to the browser; smaller bundles, no thrash).

## 14. Sources cited
Radix UI Primitives (v1.x, 2024–2026). React Aria / Adobe Spectrum (v3.x, 2024–2026). Ariakit (v0.4.x, 2024–2026; accessibleWhenDisabled). GitHub Primer (v31.x, 2024–2026). Shopify Polaris (2024–2026). IBM Carbon (v11/v12, 2024–2026). Material Design 3 (Expressive Update, 2026). Floating UI (v1.x, 2024–2026; safe polygon). W3C ARIA APG (v1.2, 2021–2026).

## 15. Agent-consumable schema

```yaml
component:
  name: Menu
  aliases:
  description: A transient overlay presenting a list of executable commands or application state toggles, governed strictly by a roving-tabindex focus model.
  role: menu
  inherits:
    - Button (trigger mechanics, interactive states, focus rings)
    - Popover (positioning, viewport collision, portal injection, overlay substrate)
  anatomy:
    - Trigger (button, aria-haspopup="menu", aria-expanded="true/false", aria-controls)
    - Portal (DOM repositioning to document.body)
    - Content (role="menu" or "menubar", position tracking, boundary collision)
    - Item (role="menuitem", focusable via roving tabindex)
    - CheckboxItem (role="menuitemcheckbox", toggle state, aria-checked)
    - RadioGroup (role="group", mutual exclusion boundary)
    - RadioItem (role="menuitemradio", aria-checked)
    - Group (role="group", aria-labelledby)
    - Label (non-interactive header, id mapping)
    - Separator (role="separator", visual and semantic break)
    - Sub (nested menu wrapper state)
    - SubTrigger (menuitem with aria-haspopup="menu")
    - SubContent (nested floating surface, relies on safe polygon)
    - ItemIndicator (checkmark/dot when checked)
  states:
    - rest
    - highlighted (DOM focused/hovered, data-highlighted)
    - active (transient pointer depression)
    - disabled (aria-disabled="true", must remain focusable for discoverability)
    - danger (destructive semantic, visually isolated)
  accessibility:
    focus_model: roving-tabindex (DOM focus physically moves into the surface)
    trigger_contract: aria-haspopup="menu", aria-expanded, aria-controls
    keyboard_navigation:
      - ArrowDown/ArrowUp (cycles items sequentially, wraps at boundaries)
      - Enter/Space (executes action, closes menu, restores focus)
      - Escape (closes menu, returns focus directly to trigger)
      - ArrowRight/ArrowLeft (opens/closes submenus, contextually RTL aware)
      - Type-ahead (alphanumeric jumping via transient keystroke buffer)
  disambiguation:
    - rule: DO NOT use for navigation. Use standard Nav + Disclosure pattern to preserve tabbing.
    - rule: DO NOT use for value selection. Use Listbox or Select to maintain activedescendant.
  implementation_notes:
    - safe_triangle: Required for submenus to prevent premature closure during diagonal pointer traversal. Floating UI useHover safePolygon recommended.
    - disabled_focusability: Disabled items must receive virtual/DOM focus via aria-disabled to ensure screen reader discoverability.
    - portal_injection: Must escape overflow hidden via Portals, managing global z-index tokens.
```

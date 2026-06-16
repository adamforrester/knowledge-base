# Tooltip — field-truth study (Claude pass)

## 1. Framing
A Tooltip is a small **plain-text description** that appears on **hover or focus** of an interactive element, supplementing (not replacing) its visible affordance. It is the cleanest close to the Overlay arc because it is a **specialisation of Popover**: a tooltip is a Popover whose content is `role=tooltip` — specifically the **`popover="hint"`** layer Popover established (the hint layer that doesn't close an open `auto` popover, fixing the tooltip-inside-menu collapse). It inherits Popover's whole positioning substrate (placement/flip/shift/arrow, CSS Anchor Positioning, the top layer, origin-aware motion — see popover) and adds the one thing genuinely its own: the **WCAG 1.4.13 hover/focus contract** and the constraints that follow from being transient and touch-inaccessible.

What it *isn't* — three boundaries the brief must hold:
- **Not a Popover / "rich tooltip"** — a tooltip holds *plain text and no interactive content* and is not itself focusable. The moment it needs a link, a button, or focusable content, it's a Popover (Material 3 calls this the rich tooltip; it's a Popover, not a tooltip — see popover).
- **Not a Toggletip** — a tooltip is **hover/focus-triggered and *describes*** its trigger (`aria-describedby`); a **toggletip** is **click/tap-triggered**, *discloses* supplementary info, is announced via a live region, and **works on touch**. (The sharp, often-missed distinction — §5.)
- **Not the `title` attribute** — the native `title` is *not* an accessible tooltip (no touch, unreliable keyboard, unstyleable, inconsistent timing/SR support); the design-system Tooltip exists to replace it.

The two realities that shape everything: **WCAG 1.4.13** (dismissable, hoverable, persistent) and **touch has no hover** — so a **tooltip must never carry essential information**. Why systems disagree: the touch story, the tooltip-vs-toggletip line, the icon-button-label pattern, and the delay/timing model.

## 2. Anatomy and parts
- **trigger** — the **focusable interactive element** the tooltip describes (a Button, an icon-only Button, a link). *Must be focusable* — a tooltip on a non-focusable element is keyboard-unreachable (§6).
- **tooltip surface** — the floating panel, `role="tooltip"`, in the top layer (inherited from Popover); **not focusable**, **not interactive**.
- **arrow** — optional caret to the trigger (inherited Popover positioning).
- **content** — a short plain-text string. No links, buttons, or focusable content.

## 3. Properties / API
- **trigger composition** — `Tooltip`/`TooltipTrigger` wrapping the trigger (Radix/React Aria); the tooltip is wired to the trigger via `aria-describedby` automatically (§6).
- **`open` / `defaultOpen`** — usually uncontrolled (hover/focus-driven); controlled for edge cases.
- **placement / offset / arrow** — **inherited from Popover** (side/align/flip/shift, `showArrow`), not re-derived (§ popover).
- **delay** — `delayDuration` (open delay, ~300–700ms, to avoid flicker on pointer transit) + close delay; a **provider-level `skipDelayDuration`** so once one tooltip in a group has shown, siblings show instantly (the warm-up/cool-down timer, §11).
- **labelling mode** — `aria-describedby` (default — the tooltip *supplements*) vs `aria-labelledby` (the tooltip *is* the name — the icon-only-button case, §6).
- **plain-text constraint** — content is text; interactive content is a Popover, not a Tooltip (enforced by API/lint, §5).

## 4. States and variants
- **States:** hidden / showing (+ a brief animating transition). The tooltip itself has no interactive states; it rides the trigger's hover/focus.
- **Variants:**
  - **plain tooltip** (the default — short description on hover/focus).
  - **icon-button label** — the tooltip of an icon-only Button doubling as its label (but see §6: an `aria-label` on the button is usually the more robust primary, with the tooltip as the *visible* echo).
  - **with-arrow / without.**
  - **toggletip** (a sibling pattern, often shipped alongside — click/tap-triggered, live-region-announced, touch-OK — §5; arguably its own component).
  - (**rich tooltip** = a Popover, explicitly out of scope — see popover.)

## 5. Usage guidance
- **Use a Tooltip** for a brief, **supplementary** hint on hover/focus of an interactive control — clarifying an icon-only button, expanding a truncated label, explaining a control's effect — where the information is **non-essential** (the UI must be fully usable without ever seeing it).
- **Don't use a Tooltip for:**
  - **Essential information** — it's transient and **invisible on touch**; essential info goes in visible text/help text.
  - **Interactive content** (links/buttons/forms) → a **Popover** (see popover).
  - **Click-to-reveal supplementary info, or anything that must work on touch** → a **Toggletip**.
  - **A persistent field hint** → visible **helper text** (see text-field).
  - **Everything** — tooltip overuse (a tooltip on every control) is noise; reserve them for genuine clarification.
- **Decision frameworks:**
  - **Tooltip vs. Toggletip:** does it *describe* the trigger on hover/focus (Tooltip — `aria-describedby`, `role=tooltip`) or *disclose* extra info on click/tap (Toggletip — click-triggered, `role=status`/live-region, touch-accessible)? The toggletip is the accessible answer to "I need a tooltip on touch" or "this is more than a word."
  - **Tooltip vs. Popover:** plain text + hover/focus (Tooltip) vs. interactive content + click (Popover). One link inside makes it a Popover.
  - **Tooltip vs. label/help text:** if the user *needs* it to operate the control, make it **visible** (a label or help text), not a tooltip.
  - **Tooltip vs. `aria-label`:** for an icon-only button, the **`aria-label` is the robust accessible name**; the tooltip is the *visible* affordance for sighted mouse/keyboard users. Don't rely on the tooltip alone for the name.

## 6. Accessibility
- **WCAG 1.4.13 (Content on Hover or Focus) — the defining rule.** A tooltip (content shown on hover/focus) must be:
  - **Dismissable** — closeable with **Escape** *without moving the pointer* (and without moving focus), so it can't permanently obscure content.
  - **Hoverable** — the pointer can move *off the trigger and onto the tooltip* without it disappearing (so a user can read/scroll it); this forbids tooltips that vanish the instant the pointer leaves the trigger.
  - **Persistent** — it stays visible until the user dismisses it, moves the pointer/focus away, or the info is no longer valid (no auto-timeout-hide).
- **`role="tooltip"` + the description relationship:** the tooltip is referenced from its trigger via **`aria-describedby`** (the default — it *supplements* the trigger's name) — *not* `aria-labelledby` unless the tooltip **is** the trigger's name (the icon-only-button case, and even then a real `aria-label` is more robust). `role=tooltip` is not a landmark and isn't navigated to; it's announced *through* the `describedby`/`labelledby` relationship when the trigger is focused.
- **The trigger MUST be focusable** — a tooltip on a non-interactive/non-focusable element is unreachable by keyboard (and fails the focus half of 1.4.13). If you must annotate a static element, make it focusable (`tabindex="0"`) or rethink it.
- **The disabled-control trap** — a `disabled` element is **not focusable and fires no pointer events**, so its tooltip is unreachable (and "why is this disabled?" is exactly when the user wants the tooltip). Fix: **wrap the disabled control in a focusable element** that carries the tooltip, or use **`aria-disabled="true"`** + a focusable-but-inert control (the focusable-inactive pattern from button §4) so the tooltip remains reachable.
- **Hover + focus parity** — the tooltip must appear on **both** hover *and* keyboard focus; a hover-only tooltip strands keyboard users.
- **The touch story** — touch has no hover and (often) no persistent focus, so tooltips are **effectively inaccessible on touch**; never put essential info in one. For touch-relevant supplementary info, use a **Toggletip** (tap → live-region announcement).
- **The `title`-attribute anti-pattern** — `title` is not an accessible tooltip (no touch, unreliable keyboard exposure, unstyleable, ~uncontrollable timing, inconsistent SR support); the component replaces it.
- **WCAG SCs:** **1.4.13** (the headline), 4.1.2 (name/role/value — `role=tooltip` + the relationship), 1.4.4 (it reflows/zooms), 2.1.1 (keyboard — focus parity + Escape), plus the trigger's own SCs.

## 7. Content guidelines
- **Short and supplementary** — a few words to a short phrase; if it needs a paragraph or formatting, it's a toggletip/popover.
- **No interactive content** — no links/buttons (the boundary).
- **Never essential** — the control must be fully operable without it (touch users never see it).
- **Icon-button labels** — the tooltip names the icon button's action ("Delete", "Add filter"); pair with a real `aria-label` so the name is robust (§6).
- **Style** — sentence case, no terminal period for a fragment; concise and literal (it's a clarification, not marketing).
- **Don't repeat the visible label** — a tooltip that just echoes the button's own text is noise.

## 8. Motion and transition
Minimal, inherited from Popover: a quick origin-aware fade/scale from the trigger edge (~100–150ms), `@starting-style`/`allow-discrete`/`overlay` via the Popover/Dialog substrate. The meaningful timing is the **open delay** (avoid flicker as the pointer transits controls) and the **warm-up/cool-down** group timer (§11), not the animation. Under `prefers-reduced-motion: reduce`, snap/opacity-only. No motion on the tooltip beyond appear/disappear. (See popover §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — placement and the arrow flip, **inherited from Popover** (logical `position-area` values); the tooltip mirrors with the trigger.
- **Text expansion** — tooltips are short but still expand (+30–50% in de/ru); size to content, **don't truncate a tooltip** (truncating the thing whose job is to clarify is self-defeating) and don't fix its width.
- **Localised content** — the string localises like any UI copy. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Tooltip`** is universal (Radix, React Aria, Material, Carbon, Polaris, Primer, Atlassian, Fluent, Ariakit, Base Web). **`Toggletip`** is the emerging name for the click/tap-triggered, live-region-announced sibling (Carbon ships it; the term is Heydon Pickering's). **The practice default: `Tooltip`** (the hover/focus description, `role=tooltip`, a Popover-`hint` specialisation) + **`Toggletip`** as the distinct click/touch-accessible disclosure (a small Popover with a live region), with the rich-content case routed to **`Popover`**. Aliases to map: `Hint`, `InfoTip`, `title` (the attribute it replaces), `Toggletip` (sibling).

## 11. Implementation notes
- **Inherit Popover's positioning + top layer + `popover="hint"`** — don't re-derive anchor positioning/flip/shift/arrow; the tooltip is a hint Popover (the hint layer specifically avoids closing an open `auto` popover, so a tooltip inside an open menu/dialog doesn't dismiss it — see popover §11).
- **The hover + focus + touch event model** — show on `pointerenter` *and* `focus` (focus parity), hide on `pointerleave`/`blur`/Escape — but implement **hoverable** (1.4.13): a close delay / a "safe" bridge so moving the pointer from trigger to tooltip doesn't hide it. Suppress on touch (no hover) or route to a toggletip.
- **The warm-up / cool-down global timer** — an open **delay** (~300–700ms) prevents tooltips flashing as the pointer crosses a toolbar; a provider-level **`skipDelayDuration`** makes sibling tooltips show *instantly* once one has shown (and resets after a cool-down gap). Radix `TooltipProvider` (`delayDuration`/`skipDelayDuration`) is the reference.
- **`aria-describedby` wiring** — the headless lib links trigger→tooltip and toggles it with visibility; default `describedby`, `labelledby` only for the is-the-name case.
- **The disabled-control wrap** — to tooltip a disabled control, wrap it in a focusable element (or use `aria-disabled` + focusable-inactive) so the tooltip is reachable (§6).
- **Never the `title` attribute** — for any real tooltip; lint against it.
- **Toggletip implementation** — a click-toggled small Popover whose content is injected into a **live region** (`role=status`/`aria-live`) so it's announced on open, and which works on touch.
- **Don't hand-roll** — Radix `Tooltip`, React Aria `Tooltip`/`TooltipTrigger`, or Ariakit handle the hover/focus/Escape/1.4.13/delay/positioning; skin them. (Primer's tooltip-v2 rebuild is a cautionary tale of how hard the a11y is to retrofit.)

## 12. Related and alternative components
- **Stands on:** Popover (the anchored-surface + positioning + top-layer + `popover="hint"` substrate — a tooltip is a Popover with `role=tooltip` — see popover), the focusable trigger (often Button / icon-only Button — see button), Icon (the icon a tooltip frequently clarifies — see icon).
- **Alternative to / boundary with:** Popover / "rich tooltip" (interactive content + click — see popover; the sharpest boundary, paired from Popover's side), **Toggletip** (click/tap, live-region, touch-accessible — the answer to tooltip-on-touch), visible **helper text** / **Label** (essential info that must always be visible — see text-field), the `title` attribute (the inaccessible native thing it replaces), `aria-label` (the robust accessible name for an icon button, which the tooltip visibly echoes).
- **Is a specialisation of:** Popover (with Menu, the Select/Combobox listbox — the role-typed siblings).

(The cleanest close to the Overlay arc — a `role=tooltip` specialisation of Popover that adds the WCAG-1.4.13 hover/focus contract and the never-essential/touch constraints. The fourth Overlay brief (Menu, Dialog, Popover, Tooltip); with it the overlay family's roles are all covered — `menu`, `dialog`/`alertdialog`, the generic surface, and `tooltip`. See popover for the substrate and the rich-tooltip boundary, button for the icon-button-label + disabled-control patterns, text-field for the visible-help-text boundary, icon for what tooltips clarify. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The death of the `title` attribute** as a tooltip — a11y practice and design systems replaced it with a real `role=tooltip` component (touch/keyboard/styling/timing all failed in `title`).
2. **WCAG 1.4.13 hardened the contract** (SC added in WCAG 2.1, 2018) — dismissable/hoverable/persistent became table stakes, killing the vanish-on-pointer-leave tooltip.
3. **The toggletip emerged** as the accessible, touch-capable, click-triggered sibling (Heydon Pickering / Carbon) — separating "describe on hover" from "disclose on click."
4. **`popover="hint"`** gave tooltips a platform layer that stacks correctly (doesn't close an open `auto` popover) — the cross-brief platform shift.
5. **The icon-button-label clarification** — `aria-label` for the robust name, the tooltip as the *visible* echo, rather than relying on the tooltip alone.

## 14. Sources cited
(Conservative; reconcile with external.) **WAI-ARIA APG** — Tooltip pattern (`role=tooltip`, `aria-describedby`, Escape, hover+focus); **WCAG 2.2** (W3C Recommendation, Oct 2023; SC 1.4.13 added in 2.1, 2018) — 1.4.13, 4.1.2, 1.4.4, 2.1.1; **Radix UI** `Tooltip` + `TooltipProvider` (`delayDuration`/`skipDelayDuration`) (2024–2026); **Adobe Spectrum / React Aria** `Tooltip`/`TooltipTrigger`, `useTooltip` (2024–2026); **Google Material 3** plain vs rich tooltips (2024–2026); **IBM Carbon** `Tooltip` / icon / definition tooltip + the **Toggletip** (2024–2026); **Shopify Polaris** `Tooltip` (2024–2026); **GitHub Primer** `Tooltip` (the v2 a11y rebuild) (2024–2026); **Atlassian** `Tooltip` (2024–2026); **Microsoft Fluent** `Tooltip` (2024–2026); **Ariakit** `Tooltip` (2024–2026); **Base Web (Uber)** `StatefulTooltip` (2024); **Heydon Pickering** — "Tooltips & Toggletips" (the distinction); the native `title` attribute (the anti-pattern). The positioning substrate is inherited from popover (CSS Anchor Positioning / Popover API — the volatile platform claim lives there).

## 15. Agent-consumable schema (conform to _schema.md in tooltip.md)
identity(Tooltip; aliases Hint/InfoTip/Toggletip(sibling); overlay; stable)/description(a short PLAIN-TEXT description on hover/focus of a focusable control, supplementary + NEVER essential; a role=tooltip specialisation of Popover (the popover=hint layer); NOT a Popover/rich-tooltip (interactive content), NOT a Toggletip (click/touch/live-region), NOT the title attribute, NOT a label)/anatomy(focusable trigger (Button/icon-button/link — MUST be focusable); surface role=tooltip in top layer, NOT focusable/interactive; arrow (inherited Popover); plain-text content)/api(inherits: popover (anchored surface + positioning placement/offset/flip/shift/arrow + top layer + popover=hint + origin-aware motion); Tooltip/TooltipTrigger wrapping the trigger; open/defaultOpen mostly uncontrolled (hover/focus); delayDuration (open ~300-700ms) + close delay + provider skipDelayDuration (warm-up/cool-down); aria-describedby DEFAULT vs aria-labelledby (is-the-name); plain-text constraint (interactive => Popover))/states(hidden/showing(+animating); rides the trigger's hover/focus, no own interactive states; variants plain tooltip / icon-button-label / with-arrow / toggletip(sibling) / rich-tooltip=Popover(out of scope))/accessibility(WCAG 1.4.13 — DISMISSABLE (Escape w/o moving pointer), HOVERABLE (pointer can move onto it w/o vanishing), PERSISTENT (no auto-hide); role=tooltip referenced via aria-describedby (default, supplements) vs aria-labelledby (is the name — icon-button, but real aria-label more robust); trigger MUST BE FOCUSABLE (else keyboard-unreachable); DISABLED-CONTROL TRAP — disabled isn't focusable/fires no events -> wrap in focusable el or aria-disabled+focusable-inactive; HOVER+FOCUS parity (hover-only strands keyboard); TOUCH has no hover -> tooltips touch-inaccessible, NEVER essential info -> use Toggletip; title attribute is NOT an accessible tooltip; SC 1.4.13/4.1.2/1.4.4/2.1.1)/content(short supplementary; no interactivity; NEVER essential; icon-button label + real aria-label; sentence case no period; don't echo the visible label)/motion(minimal origin-aware fade/scale ~100-150ms inherited from Popover; the real timing is open-delay + warm-up/cool-down not animation; reduce-motion snaps)/i18n(RTL placement+arrow flip inherited from Popover (logical position-area); text expansion — size to content, NEVER truncate a tooltip, no fixed width; localise content)/implementation(inherit Popover positioning + top layer + popover=hint (doesn't close an open auto popover — tooltip-in-menu safe); hover+focus+touch event model — show on pointerenter AND focus, hide on leave/blur/Escape, hoverable bridge/close-delay; warm-up/cool-down global timer (delayDuration + skipDelayDuration, Radix TooltipProvider); aria-describedby wiring; disabled-control wrap; NEVER the title attribute (lint); toggletip = click-toggled small Popover injected into a role=status live region, touch-OK; don't hand-roll — Radix/React Aria/Ariakit)/composition(stands-on popover (role=tooltip specialisation, popover=hint), focusable trigger (button/icon-button), icon; alternative-to popover/rich-tooltip (interactive+click — sharpest boundary), toggletip (click/touch/live-region), helper-text/label (essential visible info), title attribute (replaced), aria-label (robust icon-button name the tooltip echoes); is-a-specialisation-of popover (with menu, select/combobox listbox))/notes(contested: tooltip-vs-toggletip line; icon-button tooltip-as-label vs aria-label; the touch story (suppress vs long-press vs toggletip); delay durations. trap: hover-only (strands keyboard); tooltip on a disabled/non-focusable control (unreachable); essential info in a tooltip (touch-invisible); the title attribute; vanish-on-pointer-leave (fails 1.4.13 hoverable); truncating a tooltip. inherited: the entire Popover anchored-surface + positioning + top-layer + hint substrate. role-in-family: a role=tooltip specialisation of Popover — the fourth Overlay brief, completing the role coverage (menu/dialog/generic/tooltip). evolution: title-attribute death; WCAG 1.4.13 hardening; toggletip-for-touch emerged; popover=hint stacking; icon-button-label clarification. unverified: external 2026 version numbers; CSS-anchor/Popover-API support state inherited from popover.)

---
okf_version: "0.1"
type: component-brief
title: Tooltip
description: The cleanest close to the Overlay arc — a role=tooltip specialisation of Popover (the popover=hint layer) that adds the one thing genuinely its own. A field-truth study of the WCAG 1.4.13 hover/focus contract (dismissable, hoverable, persistent), the hover-AND-focus trigger and the touch/no-hover reality (the never-essential-info rule), role=tooltip + aria-describedby-vs-labelledby and the trigger-must-be-focusable / disabled-control trap, the plain-text/no-interactive-content boundary with Popover (the rich-tooltip rejection), the tooltip-vs-toggletip distinction, the title-attribute anti-pattern, and the warm-up/cool-down delay timer — with the practice's defaults.
tags: [components, overlay]
category: Overlay
status: stable
aliases: [hint, infotip, info-tip]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Tooltip

> Tooltip is the cleanest close to the Overlay arc, because it is a **specialisation of Popover**: a tooltip is a Popover whose content is `role=tooltip` — specifically the **`popover="hint"`** layer Popover established (the hint layer that doesn't close an open `auto` popover, so a tooltip inside an open menu doesn't dismiss it). It inherits the whole positioning substrate (placement/flip/shift/arrow, CSS Anchor Positioning, the top layer, origin-aware motion — see popover) and re-derives none of it. What's genuinely its own is the part that makes tooltips one of the most constrained components in front-end: the **WCAG 1.4.13 hover/focus contract** (dismissable, hoverable, persistent) and the two hard realities that follow — a tooltip appears on **hover AND focus**, and **touch has no hover**, so a tooltip is invisible on touch and must therefore **never carry essential information**. Three boundaries define it by negation: it is not a Popover (no interactive content — a "rich tooltip" is a Popover), not a Toggletip (that's the click/touch-accessible, live-region sibling), and not the `title` attribute (the inaccessible native thing it exists to replace).

---

## 1. Framing

A Tooltip is a short **plain-text description** shown on **hover or focus** of an interactive element, supplementing — never replacing — its visible affordance. It stands on **Popover** (the anchored surface + positioning + top layer + the `popover="hint"` layer — see popover); its definition lives not in *how it's positioned* (inherited) but in its severe behavioural and content constraints.

What it *isn't* — three boundaries the brief holds:
- **Not a Popover / "rich tooltip"** — a tooltip holds *plain text, no interactive content*, and is not itself focusable. The moment it needs a link/button/form, it's a Popover. **Material 3's "rich tooltip" (subheads, links, up to two buttons in a hover surface) is rejected by the broad consensus** (Carbon, Polaris, Primer, WAI-ARIA): because focus must stay on the trigger to keep the tooltip open, focus entering an interactive child fires the trigger's `blur` and destroys the surface — an inaccessible trap. Interactivity escalates the component to a Popover or Toggletip.
- **Not a Toggletip** — a tooltip is **hover/focus-triggered and *describes*** its trigger (`aria-describedby`); a **toggletip** is **click/tap-triggered**, *discloses* supplementary info via a live region, and **works on touch** (§5).
- **Not the `title` attribute** — the native `title` is *not* an accessible tooltip (no touch, unreliable keyboard, unstyleable, vendor-dependent timing, inconsistent SR support); the component exists to replace it.

The two realities: **WCAG 1.4.13** and **touch has no hover** → a tooltip **must never carry essential information** (if the user needs it to operate the UI, the UI is broken for touch). Why systems disagree: the rich-tooltip split (M3 vs everyone), the touch story, the icon-button-label wiring, and delay timing.

## 2. Anatomy and parts

- **trigger** — the **focusable interactive element** the tooltip describes (`<button>`/`<a>`/`<input>`, often an icon-only Button). *Must be focusable* — a tooltip on a static `<div>`/`<span>` is keyboard-unreachable (§6).
- **surface** — the floating container, **`role="tooltip"`**, in the top layer (inherited from Popover; often `popover="hint"`); **not focusable, not interactive**.
- **content** — a short plain-text node; **zero interactive children**; drives the surface's fluid dimensions (capped by a max-width then wraps — §9).
- **arrow** — optional caret, its geometry driven by Popover's collision math (inverts when the surface flips).

## 3. Properties / API

- **trigger composition** — `Tooltip`/`TooltipTrigger` wrapping the trigger (Radix/React Aria); `aria-describedby` (or `labelledby`) is wired automatically (§6).
- **`open` / `defaultOpen`** — usually uncontrolled (hover/focus-driven); controlled for edge cases.
- **placement / offset / arrow** — **inherited from Popover** (side/align/flip/shift, `showArrow`), not re-derived.
- **delay timing (the Tooltip-specific surface):** `delayDuration`/`openDelay` (the **warm-up** — pointer must rest before the surface mounts; React Aria defaults a conservative ~1500ms, Radix a snappier ~700ms), `closeDelay` (the **cool-down**, ~300–500ms — lets the pointer transit to the surface), and a provider-level **`skipDelayDuration`** (~300ms — once one tooltip has shown, siblings open *instantly*). Crucially, **keyboard focus bypasses the warm-up delay** (it mounts immediately; only hover waits).
- **labelling mode** — `aria-describedby` (default — *supplements*) vs `aria-labelledby`/`type="label"` (the tooltip *is* the name — icon-only button, §6).
- **`disableHoverableContent`** — a Radix-style escape hatch turning off the 1.4.13 hover-bridge (forces close on trigger exit); use sparingly, it trades away the *hoverable* guarantee.
- **plain-text constraint** — content is text; interactive content is a Popover (enforced by API/lint).

## 4. States and variants

- **States:** **hidden** (unmounted — the surface shouldn't exist in the DOM until warm-up completes) / **delayed-open** (warm-up timer counting, DOM unaffected) / **showing** (mounted; stays while the trigger has focus, the pointer hovers the trigger, *or* the pointer has transited onto the surface) / **closing** (cool-down; re-entering either zone reverts to showing). The tooltip has no interactive states — it rides the trigger's hover/focus.
- **Variants:**
  - **plain tooltip** (the default — short description on hover/focus).
  - **icon-button label** — the tooltip of an icon-only Button doubling as its visible label (semantic switch to `labelledby`, §6).
  - **definition tooltip** — a dotted-underline term whose tooltip defines it (the trigger must still be focusable/interactive).
  - **with-arrow / without.**
  - (**rich tooltip** = a Popover, rejected/out of scope; **toggletip** = the click/touch sibling, §5.)

## 5. Usage guidance

- **Use a Tooltip** for a brief, **supplementary** hint on hover/focus of an interactive control — naming an icon-only button, revealing a string truncated by layout (a long filename in a dense table), a short non-critical definition — where the information is **non-essential** (the UI is fully usable without it).
- **Don't use a Tooltip for:**
  - **Essential information** — transient and **invisible on touch**. Password rules / validation errors / status / anything workflow-critical goes in **visible text** (helper text, an `aria-live` error block — see text-field).
  - **Interactive content** → a **Popover** (the rich-tooltip rejection).
  - **Click-to-reveal or touch-required info** → a **Toggletip**.
  - **Static, non-interactive text** — a keyboard user can't focus a `<span>` to trigger it (and no one hovers a paragraph); if a term needs a tooltip, wrap it in a focusable element first.
  - **Everything / walls of text** — tooltip overuse is noise; Polaris caps content at one–two short sentences.
- **Decision frameworks:**
  - **Tooltip vs. Toggletip:** *describe on hover/focus* (Tooltip — `aria-describedby`, `role=tooltip`, desktop-only) vs. *disclose on click/tap* (Toggletip — `role=status`/live-region, touch-accessible, can hold interactive content). "I need a tooltip on mobile" / "this is more than a word" → Toggletip.
  - **Tooltip vs. Popover:** plain text + hover/focus vs. interactive content + click. One link inside makes it a Popover.
  - **Tooltip vs. label/help text:** if the user *needs* it to operate the control, make it **visible**, not a tooltip.
  - **Tooltip vs. `aria-label`:** for an icon button, the `aria-label`/`labelledby` is the robust accessible name; the tooltip is the *visible* echo for sighted users — don't ship a tooltip-less name or a nameless tooltip.

## 6. Accessibility

- **WCAG 1.4.13 (Content on Hover or Focus) — the defining rule.** Content shown on hover/focus must be:
  - **Dismissable** — closeable with **Escape** *without moving the pointer or focus* (a global keydown listener), so it can't permanently obscure content.
  - **Hoverable** — the pointer can move *off the trigger onto the surface* without it vanishing (critical for magnifier users panning over the text). Implemented with a **hover bridge / "safe triangle"** + the `closeDelay` so the trigger's `mouseleave` doesn't instantly unmount when the pointer heads toward the tooltip.
  - **Persistent** — stays until the user dismisses it or moves pointer/focus away; **an arbitrary auto-hide `setTimeout` is a direct 1.4.13 violation.**
- **`role="tooltip"` + the description relationship:** referenced from the trigger via **`aria-describedby`** (default — *supplements* the name) — *not* `aria-labelledby` unless the tooltip **is** the name (icon-only button). `role=tooltip` isn't a landmark and isn't navigated to; it's announced *through* the relationship when the trigger is focused.
- **The trigger MUST be focusable** — a tooltip on a non-focusable element fails the focus half of 1.4.13 and is keyboard-unreachable; make it `tabindex="0"` + an appropriate role, or rethink.
- **The disabled-control trap** — a native `disabled` element is removed from the accessibility tree and tab order *and fires no pointer events*, so its tooltip is unreachable — exactly when "why is this disabled?" is wanted. The fix: **`aria-disabled="true"`** (keeps it focusable + firing `mouseenter`/`focus`) + JS suppression of `onClick`/`onKeyDown` (the focusable-inactive pattern, button §4); wrapping the disabled control in a focusable element is the cruder fallback.
- **Hover + focus parity** — appears on **both**; hover-only strands keyboard users.
- **The touch reality** — touch has no hover (and long-press collides with native text-selection/context menus, so it's not a fix); tooltips are **inaccessible on touch** → never essential; route touch-relevant info to a **Toggletip**.
- **The dual-announcement bug** — an icon button with both `aria-label="Edit"` *and* a `describedby` tooltip "Edit" announces "Edit, button, Edit." Consolidate: route the tooltip string to the button's *naming* tree (Primer's `type="label"`) so there's one clean announcement plus the visible hover reveal.
- **Never the `title` attribute** (the anti-pattern); lint/sanitise it off triggers to prevent double tooltips.
- **WCAG SCs:** **1.4.13** (headline), 4.1.2 (name/role/value), 1.4.4 (reflow/zoom), 2.1.1 (keyboard — focus parity + Escape), plus the trigger's own SCs.

## 7. Content guidelines

- **Short and supplementary** — a few words to one–two short sentences (Polaris's cap); anything longer is a toggletip/popover.
- **No interactive content; never essential** (the boundaries).
- **Icon-button labels** — name the action ("Print document"); a label fragment takes **no terminal period**, a descriptive sentence takes sentence case + punctuation.
- **Don't duplicate the visible label** — a tooltip echoing the button's own text is redundant noise for SR users.

## 8. Motion and transition

Minimal and inherited from Popover: a rapid origin-aware opacity fade + micro-scale (95→100%, ~150ms) from the trigger edge (`@starting-style`/`allow-discrete`/`overlay` via the Popover/Dialog substrate). The meaningful timing is the **delay** logic, not the animation: during the `skipDelayDuration` window, sibling tooltips **bypass the entry animation** and appear instantly for a seamless tracking feel. Under `prefers-reduced-motion: reduce`, drop the scale — instant appearance or a ~50ms crossfade. (See popover §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL** — placement and the arrow flip, **inherited from Popover** via logical `position-area` values (a `bottom-start` tooltip aligns its leading edge to the trigger in both directions); the tooltip mirrors with the trigger.
- **Text expansion** — strings can grow ~300% (de) over English; the surface uses a **max-width cap then wraps** (Carbon ~288px, Atlassian ~240px) with **fluid height** — and a tooltip must **never truncate its own content** (truncating the thing whose job is to clarify is self-defeating). (See 13-internationalization-and-rtl.)

## 10. Naming

**`Tooltip`** is universal (Radix, React Aria, Material, Carbon, Polaris, Primer, Atlassian, Fluent, Ariakit, Base Web). **`Toggletip`** is the established name (Heydon Pickering; Carbon ships it) for the click/tap-triggered, live-region-announced, touch-accessible sibling. **The practice default: `Tooltip`** (hover/focus description, `role=tooltip`, a Popover-`hint` specialisation) + **`Toggletip`** as the distinct click/touch-accessible disclosure (a small Popover wired to a live region), with rich content routed to **`Popover`**. "Rich Tooltip" is discouraged outside Material as a confusing name for what is a Popover. Aliases to map: `Hint`, `InfoTip`, `definition tooltip` (a variant), `title` (the attribute it replaces).

## 11. Implementation notes

- **Inherit Popover's positioning + top layer + `popover="hint"`** — don't re-derive anchor positioning/flip/shift/arrow. `popover="hint"` is the right native substrate specifically because a hint renders *without* force-closing an open `auto` popover (so a tooltip inside an open menu/select doesn't dismiss it — the z-index/portal wars it retires).
- **The event model + global timers** — show on `pointerenter` *and* `focus`; **focus bypasses the warm-up delay** (instant) while hover waits `delayDuration`; on `mouseleave`/`blur` start the `closeDelay`; if the pointer enters the surface before it expires, clear it (satisfying *hoverable*). A centralised provider/hook (React Aria `useTooltipTriggerState`, Radix `TooltipProvider`) tracks intent across the DOM so `skipDelayDuration` can make siblings open instantly after the first.
- **`aria-describedby` wiring** — the headless lib links trigger→surface and toggles with visibility; default `describedby`, `labelledby`/naming-tree only for the is-the-name case (and consolidate to avoid the dual-announcement bug).
- **The disabled-control wrap** — `aria-disabled` + JS event suppression (keeps the trigger focusable + firing events), not native `disabled` (§6).
- **Never the `title` attribute** for a real tooltip; sanitise it off triggers (lint).
- **Toggletip implementation** — a click-toggled small Popover whose content is injected into a **live region** (`role=status`/`aria-live`) so it's announced on open; works on touch; can hold interactive content with managed focus.
- **Don't hand-roll** — Radix `Tooltip`, React Aria `Tooltip`/`TooltipTrigger`, or Ariakit handle the hover/focus/Escape/1.4.13/hover-bridge/delay/positioning; skin them. (Primer's tooltip-v2 rebuild shows how hard the a11y is to retrofit.)

## 12. Related and alternative components

- **Stands on:** Popover (the anchored-surface + positioning + top-layer + `popover="hint"` substrate — a tooltip is a Popover with `role=tooltip` — see popover), the focusable trigger (often Button / icon-only Button — see button), Icon (what a tooltip frequently clarifies — see icon).
- **Alternative to / boundary with:** Popover / "rich tooltip" (interactive content + click — see popover; the sharpest boundary, paired from Popover's side), **Toggletip** (click/tap, live-region, touch-accessible — the answer to tooltip-on-touch and tooltip-with-interactivity), visible **helper text** / **Label** (essential info that must always be visible — see text-field), the `title` attribute (the inaccessible native thing it replaces), `aria-label` (the robust accessible name for an icon button, which the tooltip visibly echoes).
- **Is a specialisation of:** Popover (with Menu and the Select/Combobox listbox — the role-typed siblings).

(The cleanest close to the Overlay arc — a `role=tooltip` specialisation of Popover that adds the WCAG-1.4.13 hover/focus contract and the never-essential/touch constraints. The fourth Overlay brief (Menu, Dialog, Popover, Tooltip); with it the overlay family's content roles are all covered — `menu`, `dialog`/`alertdialog`, the generic surface, and `tooltip`. See popover for the substrate and the rich-tooltip boundary, button for the icon-button-label + disabled-control patterns, text-field for the visible-help-text boundary, icon for what tooltips clarify. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The eradication of the `title` attribute** as a tooltip — once the unquestioned standard, now a documented accessibility failure; systems sanitise rogue `title`s and replace them with `role=tooltip` surfaces.
2. **WCAG 1.4.13 hardening** (SC added in WCAG 2.1, 2018) — dismissable/hoverable/persistent forced the abandonment of simple CSS `:hover` tooltips for JS state machines that track pointer intent, build hover bridges, and capture Escape.
3. **The mobile/touch fork** — the field stopped trying to make hover tooltips "work" on touch (long-press collides with text-selection/context menus) and accepted they're desktop-centric → the never-essential rule + the formal **Toggletip** bifurcation.
4. **`popover="hint"`** gave tooltips a platform top-layer that stacks correctly (doesn't close an open `auto` popover) — shedding heavy JS portal/z-index machinery.
5. **The icon-button-label clarification** — route the name to the naming tree (Primer `type="label"`) rather than risk the dual-announcement bug.

## 14. Sources cited

(Conservative; the external pass cited React Aria v3.49.0, Radix Tooltip, Primer React v38, Carbon v11 (June 2026), Atlassian v22.6.3, Ariakit v0.4.29 — held loosely and flagged unverified.)

- **WAI-ARIA APG** — Tooltip pattern (`role=tooltip`, `aria-describedby`, Escape, hover+focus) (2024–2026).
- **WCAG 2.2** (W3C Recommendation, Oct 2023; SC 1.4.13 added in 2.1, 2018) — 1.4.13, 4.1.2, 1.4.4, 2.1.1.
- **Radix UI** `Tooltip` + `TooltipProvider` (`delayDuration` ~700ms / `skipDelayDuration` ~300ms / `disableHoverableContent`) (2024–2026).
- **Adobe Spectrum / React Aria** `Tooltip`/`TooltipTrigger`, `useTooltipTrigger(State)` (the ~1500ms default, focus-bypasses-delay) (2024–2026).
- **Google Material 3** plain vs rich tooltips (the rejected rich variant) (2024–2026); **IBM Carbon** `Tooltip` / icon / definition tooltip + the **Toggletip** + the ~288px max-width (2024–2026); **GitHub Primer** `Tooltip` v2 rebuild + `type="label"` (2024–2026); **Shopify Polaris** `Tooltip` (one–two sentences, `interestFor` wiring) (2024–2026); **Atlassian** `Tooltip` (~240px, the disabled-control directive) (2024–2026); **Microsoft Fluent** `Tooltip` (the disabled-control trap) (2024–2026); **Ariakit** `Tooltip` (`timeout`/`hideTimeout`) (2024–2026); **Base Web (Uber)** `StatefulTooltip` (prompted vs unprompted) (2024).
- **Heydon Pickering** — "Tooltips & Toggletips" (the distinction); the native `title` attribute (the anti-pattern); the positioning substrate inherited from popover (CSS Anchor Positioning / Popover API / `popover="hint"` — the volatile platform claim lives there). Apple HIG — touch-first contrast.

## 15. Agent-consumable schema

```yaml
identity:
  id: tooltip
  name: Tooltip
  aliases: [hint, infotip, info-tip]
  category: overlay
  status: stable
description: >
  A short PLAIN-TEXT description shown on hover/focus of a focusable control,
  supplementary and NEVER essential. A role=tooltip specialisation of Popover
  (the popover=hint layer). NOT a Popover/rich-tooltip (interactive content),
  NOT a Toggletip (click/touch/live-region), NOT the title attribute, NOT a
  label. Touch has no hover -> tooltips are touch-inaccessible by definition.
anatomy:
  parts:
    - "trigger: FOCUSABLE interactive element (button/a/input; often icon-only Button) — tooltip on a static div/span is keyboard-unreachable"
    - "surface: role=tooltip, top layer (popover=hint), NOT focusable/interactive"
    - "content: short plain-text node, ZERO interactive children"
    - "arrow: optional, geometry from Popover collision math (inverts on flip)"
api:
  inherits: popover   # anchored surface + positioning (placement/offset/flip/shift/arrow) + top layer + popover=hint + origin-aware motion
  props:
    - {name: trigger, type: "Tooltip/TooltipTrigger wrap", description: "aria-describedby/labelledby wired automatically"}
    - {name: open/defaultOpen, type: boolean, description: "mostly uncontrolled (hover/focus)"}
    - {name: placement/offset/arrow, type: inherited, description: "from Popover, not re-derived"}
    - {name: delayDuration/openDelay, type: number, description: "WARM-UP (~700ms Radix / ~1500ms React Aria); FOCUS BYPASSES it (instant), only hover waits"}
    - {name: closeDelay, type: number, description: "COOL-DOWN ~300-500ms (lets pointer transit to surface — hoverable)"}
    - {name: skipDelayDuration, type: number, description: "~300ms — after one shows, siblings open instantly (provider-level)"}
    - {name: labelling, type: "describedby (default) | labelledby/type=label", description: "supplements vs IS the name (icon button)"}
    - {name: disableHoverableContent, type: boolean, default: false, description: "Radix escape hatch — turns off the 1.4.13 hover-bridge; use sparingly"}
  constraint: "plain text only — interactive content => Popover"
states:
  runtime: [hidden (unmounted until warm-up), delayed-open (timer counting, DOM unaffected), showing (mounted; while trigger focused / pointer on trigger / pointer transited onto surface), closing (cool-down; re-entry reverts)]
  note: "no interactive states — rides the trigger's hover/focus"
variants:
  plain: "short description on hover/focus (default)"
  icon-button-label: "tooltip of an icon-only Button = its visible label; semantic switch to labelledby/naming-tree"
  definition: "dotted-underline term whose tooltip defines it (trigger still focusable)"
  arrow: [with, without]
  rejected: "rich-tooltip = Popover (out of scope); toggletip = the click/touch sibling"
accessibility:
  wcag-criteria: ["1.4.13", "4.1.2", "1.4.4", "2.1.1"]
  wcag-1413: "DISMISSABLE (Escape w/o moving pointer/focus) + HOVERABLE (pointer can move onto surface w/o vanishing — hover bridge/safe-triangle + closeDelay) + PERSISTENT (no auto-hide setTimeout — a direct violation)"
  role-relationship: "role=tooltip referenced via aria-describedby (default, supplements) vs aria-labelledby (IS the name — icon button); not a landmark, announced through the relationship on trigger focus"
  focusable-trigger: "trigger MUST be focusable (else keyboard-unreachable + fails focus half of 1.4.13); static text needs tabindex=0 + role"
  disabled-trap: "native disabled = no a11y tree / no tab order / NO pointer events -> tooltip unreachable; fix = aria-disabled=true + JS suppress onClick/onKeyDown (focusable-inactive), or wrap in a focusable el"
  hover-focus-parity: "appears on BOTH hover and focus; hover-only strands keyboard"
  touch: "no hover (long-press collides w/ text-selection/context-menu) -> touch-inaccessible -> NEVER essential info -> Toggletip"
  dual-announcement: "aria-label + describedby tooltip of same text = 'Edit, button, Edit'; consolidate via the naming tree (Primer type=label)"
  title-attr: "NOT an accessible tooltip; sanitise it off triggers (anti-pattern)"
content:
  short: "few words to 1-2 short sentences (Polaris cap)"
  no-interactive: "plain text only"
  never-essential: "UI fully usable without it (touch-invisible)"
  casing: "label fragment = no terminal period; descriptive sentence = sentence case + punctuation"
  no-duplicate: "don't echo the trigger's visible text"
motion:
  transition: "origin-aware opacity fade + micro-scale (95->100% ~150ms) from trigger edge (inherits Popover @starting-style/allow-discrete/overlay)"
  skip-delay: "during skipDelayDuration window, siblings BYPASS the entry animation (instant tracking)"
  reduce-motion: "drop scale; instant / ~50ms crossfade"
i18n:
  rtl: "placement + arrow flip inherited from Popover (logical position-area; bottom-start aligns leading edge both directions)"
  expansion: "strings grow ~300% (de); max-width cap then wrap (Carbon ~288px / Atlassian ~240px) + fluid height; NEVER truncate a tooltip"
implementation:
  - "inherit Popover positioning + top layer + popover=hint (hint renders WITHOUT closing an open auto popover — tooltip-in-menu safe; retires z-index/portal wars)"
  - "event model: show on pointerenter AND focus; FOCUS BYPASSES warm-up (instant), hover waits delayDuration; on leave/blur start closeDelay; entering the surface clears it (hoverable); centralised provider/hook tracks intent for skipDelayDuration"
  - "aria-describedby wiring (default); labelledby/naming-tree only for is-the-name (consolidate to avoid dual-announcement)"
  - "disabled-control: aria-disabled + JS event suppression, NOT native disabled"
  - "NEVER the title attribute (sanitise/lint)"
  - "toggletip = click-toggled small Popover injected into a role=status live region, touch-OK, can hold interactive content w/ managed focus"
  - "don't hand-roll — Radix/React Aria(useTooltipTrigger)/Ariakit (hover/focus/Escape/1.4.13/hover-bridge/delay/positioning)"
composition:
  stands-on: [popover (role=tooltip specialisation, popover=hint), focusable-trigger (button/icon-button), icon]
  alternative-to: [popover/rich-tooltip (interactive+click — sharpest boundary), toggletip (click/touch/live-region), helper-text/label (essential visible info), title-attribute (replaced), aria-label (robust icon-button name the tooltip echoes)]
  is-a-specialisation-of: popover   # with menu, select/combobox listbox
notes:
  contested:
    - "the rich-tooltip split (Material 3 allows interactive content; Carbon/Polaris/Primer/WAI-ARIA reject -> it's a Popover)"
    - "icon-button tooltip-as-label vs a real aria-label (naming-tree consolidation)"
    - "the touch story (suppress vs route to toggletip)"
    - "delay durations (Radix 700ms vs React Aria 1500ms)"
  trap:
    - "hover-only (strands keyboard) — must be hover AND focus"
    - "tooltip on a disabled/non-focusable control (unreachable)"
    - "essential info in a tooltip (touch-invisible)"
    - "the title attribute"
    - "vanish-on-pointer-leave / auto-hide setTimeout (fails 1.4.13 hoverable/persistent)"
    - "truncating a tooltip; dual-announcement (label + describedby)"
  inherited: "the entire Popover anchored-surface + positioning + top-layer + hint substrate"
  role-in-family: "a role=tooltip specialisation of Popover — the fourth Overlay brief, completing the content-role coverage (menu/dialog/generic/tooltip)"
  evolution: "title-attribute eradication; WCAG 1.4.13 hardening (CSS :hover -> JS state machines); mobile/touch fork -> toggletip bifurcation; popover=hint stacking; icon-button-label naming-tree clarification"
  unverified:
    - "external-supplied 2026 version numbers (React Aria v3.49.0, Primer v38, Carbon v11, Atlassian v22.6.3, Ariakit v0.4.29; the cited Radix 'v0.1.6' looks stale)"
    - "CSS-anchor/Popover-API/popover=hint support state — inherited from popover, the catalogue's most volatile platform claim"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-tooltip/` (16 June 2026), the cleanest close to the Overlay arc — a `role=tooltip` specialisation of Popover (the `popover="hint"` layer), inheriting the whole positioning substrate and re-deriving none of it. The two passes converged almost completely — the WCAG 1.4.13 hover/focus contract (dismissable/hoverable/persistent, with the hover-bridge "safe triangle" and the no-auto-hide rule), the hover-AND-focus trigger and the touch/no-hover reality (the never-essential-info rule), `role=tooltip` + `aria-describedby` (default, supplements) vs `aria-labelledby` (is-the-name, icon button), the trigger-must-be-focusable requirement and the disabled-control trap (`aria-disabled` + event suppression, not native `disabled`), the plain-text/no-interactive boundary with Popover (the rejected Material 3 "rich tooltip" — it's a Popover), the tooltip-vs-toggletip distinction (hover-describes vs click-discloses-via-live-region, the touch-accessible sibling), the `title`-attribute anti-pattern, the warm-up/cool-down delay timer, and `Tooltip` (+ `Toggletip`) as the naming default. External-pass contributions folded in: the concrete delay defaults (React Aria ~1500ms / Radix ~700ms / skip ~300ms / close ~300–500ms), the **focus-bypasses-the-warm-up-delay** rule, the max-width caps (Carbon ~288px / Atlassian ~240px) then-wrap with no truncation, the `disableHoverableContent` escape hatch, the dual-announcement bug + Primer's `type="label"` naming-tree consolidation, the definition-tooltip variant, and the long-press-collides-with-text-selection touch detail. Claude-pass contributions: the framing as the arc-closing `popover="hint"` specialisation, the three-boundary definition-by-negation (Popover/Toggletip/`title`), and the never-essential rule as the load-bearing constraint. The 2026 version numbers (and the stale-looking Radix figure) and the CSS-anchor/Popover-API/`popover="hint"` support state (inherited from popover, the catalogue's most volatile platform claim) are flagged unverified. Conformant to `components/_schema.md`. The fourth Overlay brief, completing the content-role coverage of the overlay family (Menu = `menu`, Dialog = `dialog`/`alertdialog`, Popover = the generic surface, Tooltip = `tooltip`); only Drawer remains in the Overlay category.*

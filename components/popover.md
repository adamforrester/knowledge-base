---
okf_version: "0.1"
type: component-brief
title: Popover
description: The generic anchored transient surface, the third Overlay pole, and the brief that formalises the positioning substrate Select, Combobox, and Menu have referenced since Select. A field-truth study of the native Popover API (auto/manual/hint), CSS Anchor Positioning (anchor()/position-area/position-try/anchor-size — displacing Floating UI) and its Containing-Block Trap, the positioning model the whole overlay family inherits, the light-dismiss + non-trapping focus contract (vs Dialog's trap), the native-popover accessibility gap (popovertarget wires behaviour not semantics), role-by-content, and the popover-vs-tooltip-vs-menu-vs-dialog boundaries — with the practice's defaults.
tags: [components, overlay]
category: Overlay
status: stable
aliases: [popup, overlay, anchored-overlay, floating-panel, flyout]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Popover

> Popover is the **generic anchored transient surface** — a floating panel tethered to a trigger, dismissed by clicking outside or Escape, that does *not* trap focus — and the pivotal Overlay brief, because it is where the **positioning substrate** Select, Combobox, and Menu have been forward-referencing since Select finally gets formalised. It stands on Button (the trigger) and Dialog (the top layer + the `@starting-style`/`allow-discrete`/`overlay` exit-animation machinery), and it is itself the substrate the rest of the family sits on: Menu is a Popover whose content is `role=menu`; the Select/Combobox listbox is a Popover whose content is `role=listbox`; Tooltip is a (hint) Popover whose content is `role=tooltip`. Two decisions define a from-scratch build. First, the **native Popover API + CSS Anchor Positioning** platform-first move (paired with Dialog's native-`<dialog>`): the `popover` attribute gives light-dismiss + Escape + top layer for free, and CSS Anchor Positioning (`anchor()`/`position-area`/`position-try`) gives declarative collision-aware placement that is **displacing Floating UI** for the whole family — the catalogue's most volatile, highest-impact platform claim. Second, **light-dismiss + non-trapping** — the contrast with Dialog: it supplements the page, it doesn't block it.

---

## 1. Framing

A Popover is a small, transient, **contextual surface anchored to a trigger** that the user opens deliberately and dismisses by clicking away — supplementary info, a small form, a picker, a profile card, a settings cluster. It stands on **Button** (the trigger — see button) and **Dialog** (the top layer + the exit-animation substrate — see dialog), and is itself **the substrate the overlay family sits on**: Menu, the Select listbox, the Combobox listbox, and Tooltip are all Popovers specialised by content role + focus model. Popover is the base; the others are the specialisations.

**The two defining decisions:**
- **Native Popover API + CSS Anchor Positioning (platform-first).** The **`popover` attribute** + `popovertarget` + `showPopover()`/`togglePopover()` give light-dismiss, Escape, and the top layer (`popover="auto"`); **CSS Anchor Positioning** (`anchor-name`/`position-anchor`, `anchor()`, `position-area`, `position-try`, `anchor-size()`) gives declarative, collision-aware positioning that **replaces the Floating UI / Popper JS layer** the rest of the family leaned on. This is the catalogue's most volatile platform claim — date it, note the verification path, keep Floating UI as the fallback.
- **Light-dismiss + non-trapping** — the contrast with Dialog: dismisses on outside-click/Escape, is *not* focus-trapped, and (when generic) does *not* auto-move focus in.

What it *isn't*: a **Tooltip** (a hover/focus *description*, `role=tooltip`, no interactive content, WCAG 1.4.13 — the sharpest line), a **Menu** (`role=menu` commands + roving — see menu), a **Dialog** (modal, focus-trapped — see dialog; though an interactive popover *is* a non-modal `role=dialog`, the overlap), or a **Drawer** (edge-anchored sheet). Why systems disagree: native-vs-Floating-UI (and the Containing-Block Trap), the focus model for interactive popovers, the trigger↔popover accessibility wiring, and where the popover/tooltip/menu/dialog lines fall.

## 2. Anatomy and parts

- **trigger / anchor** — the Button (or any element) the popover is positioned against and toggled from; in the anchor-positioning era it has a **dual identity**: the semantic invoker *and* the mathematical reference point (carries `anchor-name` / `popovertarget`, plus `aria-expanded` + an accessible relationship to the surface — §6). The anchor may differ from the trigger.
- **popover surface** — the floating panel rendered into the **top layer** (escaping `overflow:hidden`/stacking clipping); its `role` comes from content (§6).
- **arrow / caret** — an optional pointer connecting surface to anchor; must stay attached to the trigger's centre even as the surface shifts on the cross-axis (§11); used when the visual association is ambiguous, omitted for large panels.
- **content** — content-dependent header / body / footer (a non-modal-dialog popover may use all three; a rich tooltip just a body).
- **close affordance** — an optional explicit close (icon Button) for dense/interactive popovers; light-dismiss + Escape are the baseline.

## 3. Properties / API

- **`open` / `defaultOpen` + `onOpenChange`** — controlled/uncontrolled (fires on light-dismiss/Escape so external state syncs).
- **trigger/anchor composition** — `PopoverTrigger`/`asChild` (Radix merges ARIA + listeners onto a real button without a wrapper node); React Aria extracts via `usePopover`. Emerging declarative wiring: `interestfor`/`commandfor` attributes aiming to replace JS event listeners.
- **placement** — `side` (top/bottom/left/right) + `align` (start/center/end) + `sideOffset`/`alignOffset` (Fluent uses `positioning` shorthand strings like `above-start`); maps to the CSS `position-area` 3×3 grid (§11).
- **collision** — `avoidCollisions` + `collisionBoundary`/`collisionPadding`; the two strategies are **flip** (invert across the main axis) and **shift** (slide along the cross-axis to stay visible); maps to `position-try`/`position-try-fallbacks`.
- **arrow** — `showArrow` + arrow size/element.
- **same-width** — match the trigger width (the Select/Combobox listbox case) — Ariakit's `--popover-anchor-width`, or natively **`anchor-size(width)`** (§11).
- **light-dismiss** — `closeOnEscape` (default true) + `closeOnInteractOutside`/`dismissable` (default true); `modal` (a **false** default — a popover is non-modal; raising it to trap+scrim shades into Dialog).
- **focus** — `initialFocus` (only when interactive — §6), `restoreFocus` (return to trigger, default true), **`trapFocus` defaults false** (the Dialog difference).
- **role/aria** — `role` + `aria-labelledby`/`aria-describedby` per content; the trigger wiring (§6).

## 4. States and variants

- **States:** closed / open / **animating** (inherits Dialog's exit solution — §8).
- **Variants:**
  - **trigger:** **click** (default — interactive workflows) vs **hover/focus** (a rich tooltip / `popover="hint"`, with `onMouseEnter/LeaveDelay` to avoid flashing — but interactive content must not be hover-only, per 1.4.13).
  - **with-arrow / without.**
  - **generic vs role-typed** — info/content (generic; `role=dialog` if interactive) / listbox (Select/Combobox) / menu (Menu) / tooltip (Tooltip). The role-typed ones are the specialisations.
  - **same-width-as-trigger** (listbox) vs **content-width** (generic).
  - **non-modal (default) vs modal** (the Dialog boundary).

## 5. Usage guidance

- **Use a Popover** for a small, transient, contextual surface anchored to a trigger that the user opens deliberately and dismisses by clicking away — supplementary info, a small form, a picker, a settings cluster, a profile card. It supplements the page without blocking it.
- **Don't use a Popover for:** a passive **description on hover/focus** (→ Tooltip — no interactive content, `role=tooltip`, 1.4.13), a **list of commands** (→ Menu — `role=menu` + roving), a **blocking decision or long/multi-step work** (→ Dialog — modal, focus-trapped; a popover's light-dismiss makes it dangerous for work the user could lose to an errant background click), **edge-anchored content/nav** (→ Drawer), or **critical/transient feedback** (→ Toast/Banner).
- **Decision frameworks:**
  - **Popover vs. Tooltip (the sharpest line; Material 3 frames it as Rich vs. Plain):** interactive content + click-to-open (Popover/Rich) vs. a passive text description + hover/focus (Tooltip/Plain). A tooltip can't contain a link or button; the moment it does, it's a popover — putting a link in a hover tooltip is a severe usability failure for magnifier/alternative-pointer users.
  - **Popover vs. Menu:** generic container (Popover) vs. a list of `menuitem` commands with roving tabindex (Menu).
  - **Popover vs. Dialog:** does it **supplement** (non-modal, light-dismiss, not trapped — Popover) or **block + demand resolution** (modal, trapped — Dialog)? An interactive popover is essentially a *non-modal dialog* (`role=dialog`); the only real difference is modality + the trap. Carbon's rule: reach for the non-modal popover when the user must reference on-page information *while* interacting with the overlay.
  - **When to move focus into a popover:** move focus in for an **interactive** popover (form/listbox — the user will operate it); do *not* for a hint/info popover (focus stays on the trigger). Always return focus to the trigger on close.

## 6. Accessibility

- **The native-popover accessibility GAP (the critical, non-obvious point):** `popovertarget` wires *behaviour* (toggle + light-dismiss + Escape) but **not the full semantic relationship**. It establishes an *implicit* `aria-details` from trigger to popover and an implicit `aria-expanded` — but **`aria-details` is inconsistently supported** by proprietary screen readers (many ignore it or treat it differently from `aria-controls`), and the `[popover]` element defaults to a generic `group` role with **no meaningful implicit semantics**. So the practice mandate is to add three things explicitly: **`aria-expanded`** on the trigger (guaranteed cross-browser state announcement), **`aria-controls`** linking trigger → popover id, and an explicit **`role`** on the surface. `popovertarget` alone ships an inaccessible overlay.
- **Role-by-content:** a popover has no meaningful implicit role — the role comes from content: **`role="dialog"`** (interactive/non-modal — labelled by a heading), **`listbox`** (Select/Combobox), **`menu`** (Menu), **`tooltip`** (Tooltip). The generic interactive popover defaults to a **non-modal `role="dialog"`**. Don't put `role=dialog` on a tooltip or a menu — match the content.
- **The non-trapping focus model (the Dialog contrast):** a popover is **not focus-trapped** — Tab moves *through* it and *out* into the page. Focus management depends on interactivity: **interactive** popover → move focus to the first focusable/designated element on open; **hint/info** popover → focus does *not* move in (the surface is read on trigger focus, or reachable via the relationship). **Always return focus to the trigger on close.** The background stays interactive — that's the point.
- **Plain vs. Rich hints** (`popover="hint"`): a **Plain Hint** is flattened to a text string in the accessibility tree (the SR reads it on trigger focus, doesn't navigate in); a **Rich Hint** (interactive content) toggles `aria-expanded` so the SR knows a new surface appeared and can navigate into it.
- **WCAG 1.4.13 (content on hover or focus)** — for hover/focus popovers and tooltips, the content must be **dismissable** (Escape without moving the pointer), **hoverable** (the pointer can move onto it without it vanishing), and **persistent** (stays until dismissed/focus-lost). The recurring hover failure.
- **WCAG SCs:** 4.1.2 (name/role/value — the trigger relationship + content role), 1.4.13 (hover/focus content), 2.1.1 / 2.1.2 (keyboard, **no trap** — a popover must not trap), 2.4.3 (focus return), 2.4.7 (focus visible), plus the content's own SCs (listbox/menu/dialog).

## 7. Content guidelines

- **Concise, self-contained content** — a popover is supplementary; keep it scannable. Never use it for long-form data entry or multi-step work the user could lose to an accidental light-dismiss (→ Dialog or a page route).
- **A heading labels the surface** (`aria-labelledby`); interactive popovers benefit from an explicit **close** (icon Button) beyond light-dismiss.
- **The trigger's accessible name should convey what the popover holds** ("Account menu", "Filters", "More info about X").
- **Arrow** — use a caret when the visual association to the anchor would otherwise be ambiguous (a small popover near several controls, or one shifted off-centre by collision); omit for large panels where placement is obvious.

## 8. Motion and transition

Origin-aware open/close — the surface scales/fades **from the anchored edge** (`transform-origin` at the trigger; ~120–180ms), exactly the Dialog substrate: `@starting-style` + `transition-behavior: allow-discrete` + the `overlay` property, inherited from Dialog (see dialog §8), not re-derived. Because collision detection may flip the surface, the origin must update with placement — Radix injects a computed `--radix-popover-content-transform-origin` (top-centre when placed below, bottom-centre when flipped above) so the scale always emerges from the trigger. The arrow fades with the surface; hover popovers use a small open/close intent delay. Under `prefers-reduced-motion: reduce`, snap/opacity-only. (See dialog §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization

- **RTL** flips placement, alignment, and the arrow — and CSS Anchor Positioning handles it **declaratively via logical values**: `position-area` uses logical axes (`block-start`/`block-end`/`inline-start`/`inline-end`), so a popover at `inline-start` flips from the left of the trigger to the right when `dir` changes, with no JS, observers, or recalculation. The `position-try` fallbacks and the arrow's offset must also be expressed logically so they mirror.
- **Text expansion** — popover content (forms/labels) expands; size to content within min/max bounds, no fixed widths. (See 13-internationalization-and-rtl.)

## 10. Naming

Rare field-wide consensus on **`Popover`** (Radix, React Aria, Fluent, Carbon, Polaris, Ariakit, Base Web — ~80%+); Atlassian uses **`Popup`**; Primer abstracts the substrate as **`Overlay`** / **`AnchoredOverlay`** (the positioning primitive). **The practice default: `Popover`** (mirroring the native `popover` attribute) as the generic anchored-surface primitive, with **Menu / Select / Combobox / Tooltip as the role-typed specialisations built on it** (not re-implementing positioning), the trigger via `PopoverTrigger`/`asChild`. Surface the positioning machinery as a shared primitive (an `Overlay`/`useAnchorPosition` layer) the whole family consumes. Aliases to map: `Popup`, `Overlay`, `AnchoredOverlay`, `FloatingPanel`, `Flyout`.

## 11. Implementation notes

- **Native Popover API first.** `popover="auto"` (light-dismiss + Escape + top layer + **one-open-per-ancestor** auto-close) / `popover="manual"` (no light-dismiss, no auto-close — persistent, you control it) / **`popover="hint"`** (a secondary ephemeral stacking layer that does *not* close an open `auto` popover — which resolves the long-standing bug where hovering a tooltip inside an open menu collapsed the menu). Emerging `interestfor`/`commandfor` attributes wire triggers declaratively.
- **CSS Anchor Positioning displaces Floating UI.** `anchor-name: --x` on the trigger + `position-anchor: --x` + a `position-area` grid coordinate on the surface; `@position-try` + `position-try-fallbacks: flip-block` for collision; **`anchor-size(width)`** to inherit the trigger's width (the listbox same-width case).
- **The Containing-Block Trap (the sharp CSS-anchor limitation — verify before relying):** the anchor must be **laid out before** the anchored element, and a positioned ancestor establishes an **Inset-Modified Containing Block (IMCB)** that makes the positioning math **fail silently** (popover misaligned or invisible); a positioned element also can't reference an anchor outside its containing block or in a higher top layer. The consequence: anchor-positioned popovers want a **strict DOM hierarchy** (trigger + popover as adjacent siblings). For deep/nested composition, Shadow DOM, or unsupported browsers, fall back — Atlassian's `shouldRenderToParent` (render in place rather than portal-to-body), the Oddbird positioning polyfill, or a headless Floating UI layer. **The practice default: CSS-anchor-first, progressively enhanced, Floating UI as the fallback** during the transition (Primer's feature-flagged migration is the enterprise tipping-point signal).
- **The trigger↔popover accessible wiring** native leaves out — add `aria-expanded` + `aria-controls` + the content role (§6).
- **The focus model** — not trapped; move focus in only for interactive content; return to the trigger on close.
- **The arrow** — position via anchor positioning (anchor the arrow to the trigger too) or a legacy absolutely-positioned pseudo-element; keep it out of the accessibility tree.
- **Nested popovers + the light-dismiss stack** — `popover="auto"` auto-manages a stack (opening a non-descendant `auto` popover closes the previous; Escape closes the top); the top layer stacks like Dialog.
- **The formalisation note (the loop this brief closes):** Select, Combobox, and Menu's "positioning inherited from the overlay substrate" now resolves **here** — their listbox/menu surfaces *are* Popovers with a specific content role. Build the positioning once (native anchor positioning + a Floating-UI fallback) and have the family consume it.
- **Don't hand-roll** — Radix `Popover`, React Aria `Popover`/`usePopover`, or Ariakit; they increasingly delegate to the native API + anchor positioning. Skin them.

## 12. Related and alternative components

- **Stands on:** Button (the trigger — see button), Dialog (the top-layer + `@starting-style`/`allow-discrete`/`overlay` animation substrate — see dialog), Icon (the close/arrow glyphs — see icon).
- **Is the substrate for (specialisations sitting on Popover):** Menu (`role=menu` content — see menu), the Select listbox (`role=listbox` — see select), the Combobox listbox (see combobox), Tooltip (`role=tooltip`, hint — see tooltip), the Date Picker calendar (a `role=grid` of days — see date-picker). These inherit Popover's anchored-surface + positioning machinery and add their content role + focus model.
- **Alternative to / boundary with:** Tooltip (passive description, hover/focus, no interactive content — the sharpest line), Menu (commands), Dialog (modal trap — but an interactive Popover *is* a non-modal `role=dialog`), Drawer (edge sheet — see drawer when briefed).

(The pivotal Overlay brief — the generic anchored transient surface that formalises the positioning + light-dismiss substrate Select, Combobox, and Menu have referenced since Select. The light-dismiss + non-trapping + anchored counterpart to Dialog's modal trap; together Dialog and Popover are the overlay substrate, with Menu/Select/Combobox/Tooltip as specialisations. See button for the trigger, dialog for the top-layer/animation substrate and the modal boundary, menu/select/combobox for the specialisations that resolve their positioning here, tooltip for the description boundary. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution

1. **The Portal/z-index Era → the Headless/JS-physics Era → the Platform Era.** Early libs portalled to `<body>` to dodge `overflow:hidden` clipping (z-index wars); headless hooks (`usePopover`, Radix) then decoupled Floating-UI/Popper positioning from styling; now the **native top layer** resolves portals + z-index and **CSS Anchor Positioning displaces the JS physics engine** (the catalogue's most volatile, highest-impact shift — verify support).
2. **The native Popover API arrived** (`popover`/`popovertarget`, Baseline ~early 2025; `popover="hint"` via Interop 2026) — light-dismiss, Escape, and one-open-per-ancestor in the platform.
3. **`popover="hint"` fixed the tooltip-inside-menu collapse bug** with a separate stacking layer.
4. **Role-by-content discipline hardened** — practice stopped treating "popover" as a role (and stopped assuming `aria-haspopup` suffices), assigning `dialog`/`listbox`/`menu`/`tooltip` by content and surfacing the native a11y gap.
5. **Popover-as-base** — design systems build Menu/Select/Tooltip on one Popover/positioning primitive rather than re-implementing anchoring per component.

## 14. Sources cited

(Conservative; reconcile with external — and treat all CSS-anchor-positioning / Popover-API support claims as the catalogue's most volatile, `last-audited`-gated. The external pass cited React Aria v3.0+, the Popover API Baseline ~early 2025, `popover="hint"` via Interop 2026 — held loosely.)

- **Native Popover API** (`popover`, `popovertarget`, `showPopover`/`hidePopover`/`togglePopover`, `popover="auto"|"manual"|"hint"`, the emerging `interestfor`/`commandfor`) + **CSS Anchor Positioning** (`anchor-name`/`position-anchor`, `anchor()`, `position-area`, `position-try`/`@position-try`/`position-try-fallbacks`, `anchor-size()`, the IMCB/containing-block rules) — MDN / W3C CSS Anchor Positioning L1 Editor's Draft / CSS-Tricks almanac / Oddbird (polyfill + IMCB) / Chrome Developers / WebKit Interop 2026, 2024–2026, current-platform-state.
- **Floating UI** (the JS incumbent being displaced — flip/shift/arrow middleware) (2024–2026).
- **Radix UI** `Popover` (the headless reference; `asChild`, `--radix-popover-content-transform-origin`) (2024–2026); **Adobe Spectrum / React Aria** `Popover`/`usePopover` (v3.0+) (2024–2026); **GitHub Primer** `Overlay`/`AnchoredOverlay` (the feature-flagged anchor-positioning migration) (2024–2026); **IBM Carbon** `Popover` (the reference-while-interacting non-modal rule) (2024–2026); **Shopify Polaris** `Popover` (the ActionList host) (2024–2026); **Atlassian** `Popup` (`shouldRenderToParent`) (2024–2026); **Microsoft Fluent** `Popover` + positioning shorthand (2024–2026); **Ariakit** `Popover` (`--popover-anchor-width`) (2024–2026); **Base Web (Uber)** `Popover` (2024); **Google Material 3** rich vs plain tooltips (2024–2026); **Apple HIG** popovers/popups (2024–2026); **WAI-ARIA APG** — no generic popover pattern (Tooltip / Dialog(non-modal) / Disclosure / Menu by content). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.2, 1.4.13, 2.1.1, 2.1.2, 2.4.3, 2.4.7.

## 15. Agent-consumable schema

```yaml
identity:
  id: popover
  name: Popover
  aliases: [popup, overlay, anchored-overlay, floating-panel, flyout]
  category: overlay
  status: stable
description: >
  The GENERIC anchored transient surface — a floating panel tethered to a
  trigger, light-dismiss, NOT focus-trapped. The substrate Menu, the
  Select/Combobox listbox, and Tooltip sit on (specialised by content role).
  Native Popover API + CSS Anchor Positioning first (displacing Floating UI).
  NOT a tooltip (passive description), NOT a menu (role=menu commands), NOT a
  dialog (modal trap) — though an interactive popover IS a non-modal role=dialog.
anatomy:
  parts:
    - "trigger/anchor: Button (dual identity — semantic invoker + positioning reference; anchor-name/popovertarget + aria-expanded + accessible relationship; anchor may differ from trigger)"
    - "surface: floating panel in the TOP LAYER (escapes overflow:hidden/stacking); role by content"
    - "arrow/caret: optional, anchored to trigger centre even as surface shifts; out of a11y tree"
    - "content: header/body/footer per content (non-modal-dialog uses all; rich tooltip just body)"
    - "close affordance: optional explicit close for dense/interactive; light-dismiss is the baseline"
api:
  inherits:
    - "button (trigger)"
    - "dialog (top layer + @starting-style/allow-discrete/overlay exit animation)"
  props:
    - {name: open/defaultOpen, type: boolean, description: controlled/uncontrolled}
    - {name: onOpenChange, type: function, description: fires on light-dismiss/Escape}
    - {name: trigger, type: "PopoverTrigger/asChild", description: "merges ARIA onto a real button; emerging interestfor/commandfor declarative wiring"}
    - {name: placement, type: "side + align + offset", description: "maps to CSS position-area 3x3 grid"}
    - {name: collision, type: "avoidCollisions + boundary/padding", description: "flip (invert main axis) + shift (slide cross axis); maps to position-try"}
    - {name: showArrow, type: boolean}
    - {name: same-width, type: boolean, description: "match trigger width — Ariakit --popover-anchor-width or native anchor-size(width)"}
    - {name: closeOnEscape/closeOnInteractOutside, type: boolean, default: true}
    - {name: modal, type: boolean, default: false, description: "non-modal; true shades to Dialog"}
    - {name: initialFocus, type: ref, description: "interactive content only"}
    - {name: restoreFocus, type: boolean, default: true, description: return to trigger}
    - {name: trapFocus, type: boolean, default: false, description: "THE Dialog difference — popover does NOT trap"}
    - {name: role, type: enum, values: [dialog, listbox, menu, tooltip], description: "by content"}
states:
  runtime: [closed, open, "animating (inherits Dialog exit solution)"]
variants:
  trigger: "click (default, interactive) vs hover/focus (rich tooltip / popover=hint, with enter/leave delay; interactive content not hover-only per 1.4.13)"
  arrow: [with-arrow, without]
  role-typed: "generic (dialog if interactive) / listbox (select-combobox) / menu / tooltip"
  width: "same-width-as-trigger (listbox) vs content-width"
  modality: "non-modal (default) vs modal (Dialog boundary)"
accessibility:
  wcag-criteria: ["4.1.2", "1.4.13", "2.1.1", "2.1.2", "2.4.3", "2.4.7"]
  native-gap: "popovertarget wires BEHAVIOUR not semantics — implicit aria-details (inconsistently supported) + implicit aria-expanded; [popover] defaults to generic group role (no meaningful semantics). MANDATE: add explicit aria-expanded (trigger) + aria-controls (trigger->id) + role (surface)"
  role-by-content: "no meaningful implicit role — dialog (interactive/non-modal) / listbox (select-combobox) / menu / tooltip; NEVER role=dialog on a tooltip/menu"
  focus-model: "NON-TRAPPING — Tab moves through+out (vs Dialog). Interactive: move focus to first focusable/designated on open. Hint/info: focus does NOT move in. ALWAYS return focus to trigger on close. Background stays interactive."
  hints: "Plain Hint = flattened text string (SR reads on trigger focus, doesn't navigate in); Rich Hint = interactive, toggles aria-expanded so SR can navigate in"
  hover: "WCAG 1.4.13 — dismissable (Escape, no pointer move) + hoverable (pointer can reach surface) + persistent (until dismissed/blur)"
content:
  concise: "supplementary + scannable; NEVER long-form/multi-step work (light-dismiss data-loss risk) -> Dialog/page route"
  labelling: "heading labels surface (aria-labelledby); explicit close for dense/interactive"
  trigger: "accessible name conveys what the popover holds ('Account menu', 'Filters')"
  arrow: "when association ambiguous (near several controls, or shifted off-centre); omit for large panels"
motion:
  open: "ORIGIN-AWARE scale/fade from anchored edge ~120-180ms; inherits Dialog @starting-style + allow-discrete + overlay; transform-origin updates with placement on flip (Radix --radix-popover-content-transform-origin)"
  arrow: "fades with surface"
  hover: "open/close intent delay"
  reduce-motion: "snap / opacity-only"
i18n:
  rtl: "placement+align+arrow flip DECLARATIVELY via logical position-area values (block/inline-start/end); inline-start flips left->right on dir change, no JS; position-try fallbacks + arrow offset must be logical"
  expansion: "content sizes within min/max bounds; no fixed widths"
implementation:
  - "native Popover API: popover=auto (light-dismiss+Escape+top-layer+one-open-per-ancestor) / manual (persistent) / HINT (separate stacking layer that doesn't close an open auto popover — fixes tooltip-inside-menu collapse); emerging interestfor/commandfor"
  - "CSS Anchor Positioning displaces Floating UI: anchor-name + position-anchor + position-area; @position-try/position-try-fallbacks for collision; anchor-size(width) for same-width"
  - "THE CONTAINING-BLOCK TRAP (verify before relying): anchor must be laid out BEFORE the anchored el; a positioned ancestor makes an Inset-Modified Containing Block (IMCB) and positioning FAILS SILENTLY; can't reference an anchor outside the containing block or in a higher top layer -> wants strict DOM hierarchy (trigger+popover adjacent siblings). Fallback: Atlassian shouldRenderToParent / Oddbird polyfill / Floating UI. Practice: CSS-anchor-first, progressive enhancement, Floating UI fallback"
  - "trigger<->popover wiring native leaves out: add aria-expanded + aria-controls + role"
  - "focus: not trapped; move in only when interactive; return to trigger"
  - "arrow via anchor positioning (anchor it to the trigger too) or legacy pseudo-element; out of a11y tree"
  - "nested popovers + auto light-dismiss stack + top-layer stacking"
  - "FORMALISATION: Select/Combobox/Menu positioning resolves HERE — their surfaces are Popovers with a content role; build positioning once, family consumes it"
  - "don't hand-roll — Radix/React Aria(usePopover)/Ariakit on the native API"
composition:
  stands-on: [button, dialog (top-layer/animation)]
  is-substrate-for: [menu (role=menu), select-listbox (role=listbox), combobox-listbox, tooltip (role=tooltip)]
  alternative-to: [tooltip (description), menu (commands), dialog (modal trap; interactive popover = non-modal dialog), drawer (edge)]
  role-in-family: "the generic anchored surface — Dialog=modal trap, Popover=light-dismiss+anchor; Menu/Select/Combobox/Tooltip are Popover specialisations; formalises the positioning substrate the family inherited"
notes:
  contested:
    - "native-vs-Floating-UI (CSS-anchor-first, but the Containing-Block Trap + uneven support keep the JS fallback)"
    - "focus model for interactive popovers (move-in) vs hint (stay)"
    - "trigger<->popover wiring (aria-details implicit but insufficient -> aria-controls)"
    - "popover/tooltip/menu/dialog lines (interactive+click vs description+hover the sharpest)"
  trap:
    - "popovertarget without the explicit accessible relationship (button that 'does nothing' to a SR)"
    - "role=dialog on a tooltip/menu (role must match content)"
    - "focus-trapping a popover (it must NOT trap)"
    - "interactive content in a hover tooltip (1.4.13)"
    - "the IMCB/Containing-Block Trap — positioned ancestor breaks anchor positioning silently"
    - "long-form/multi-step work in a light-dismiss popover (data-loss)"
  inherited: "Button trigger; Dialog top-layer + @starting-style/allow-discrete/overlay animation"
  evolution: "portal/z-index -> headless+Floating-UI -> platform (native top layer + CSS Anchor Positioning); native Popover API (auto/manual/hint); hint fixed tooltip-in-menu collapse; role-by-content hardened; popover-as-base"
  unverified:
    - "external-supplied 2026 version numbers (React Aria v3.0+, etc.)"
    - "CSS Anchor Positioning + Popover API support state + the IMCB layout rules + popover=hint/interestfor/commandfor a11y mappings — THE MOST VOLATILE platform claim in the catalogue, last-audited-gated, shared with select/combobox/menu/dialog"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-popover/` (16 June 2026), the pivotal Overlay brief — the generic anchored transient surface that formalises the positioning + light-dismiss substrate Select, Combobox, and Menu have referenced since Select. It stands on Button (trigger) and Dialog (top layer + `@starting-style`/`allow-discrete`/`overlay` animation), and is itself the substrate Menu/Select-listbox/Combobox-listbox/Tooltip sit on. The two passes converged almost completely — the native-Popover-API (`auto`/`manual`/`hint`) + CSS-Anchor-Positioning platform-first decision displacing Floating UI, the positioning model the family inherits (placement/offset/flip/shift/arrow/same-width via `anchor-size()`), the light-dismiss + non-trapping focus contract (move focus in only for interactive content; return to trigger; vs Dialog's trap), the native-popover accessibility gap (`popovertarget` wires behaviour not semantics — add `aria-expanded`/`aria-controls`/role), role-by-content (`dialog`/`listbox`/`menu`/`tooltip`), the popover-vs-tooltip-vs-menu-vs-dialog boundaries (the rich-vs-plain interactive/hover line being the sharpest), and `Popover` as the naming default with Menu/Select/Combobox/Tooltip as specialisations. External-pass contributions folded in: the **Containing-Block Trap / Inset-Modified Containing Block (IMCB)** (the sharp CSS-anchor limitation — positioned ancestor breaks positioning silently, wants strict sibling DOM, fall back via `shouldRenderToParent`/Oddbird polyfill/Floating UI), `anchor-size(width)` for same-width, `popover="hint"` resolving the tooltip-inside-menu collapse, the emerging `interestfor`/`commandfor`, the `aria-details`-is-implicit-but-insufficient nuance, the plain-vs-rich-hint a11y mapping, the `--radix-popover-content-transform-origin` origin-aware motion, and the Primer feature-flagged migration as the enterprise tipping point. Claude-pass contributions: the framing as the substrate-formalising pivot, the Popover-as-base relationship to the specialisations, and the loop-closing note that Select/Combobox/Menu's positioning resolves here. The 2026 version numbers and the CSS-Anchor-Positioning/Popover-API support state (the most volatile platform claim, shared across the overlay family) are flagged unverified. Conformant to `components/_schema.md`. The third Overlay brief, completing the Menu/Dialog/Popover trio that formalises the positioning + dismissal substrate Select, Combobox, and Menu inherit.*

# Popover — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/popover.md`; version numbers and the CSS-Anchor-Positioning / Popover-API platform-state (the catalogue's most volatile claim) flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Popover Component Research Report: The Anchored Surface Substrate

## 1. Framing
The overlay taxonomy is anchored by three poles: modal Dialog, edge-aligned Drawer, element-anchored Popover. The Popover is the most structurally pivotal — the definitive generic anchored transient surface, the formalized positioning substrate that Select listboxes, Combobox dropdowns, Menus, and Tooltips rely on to tether transient content to a trigger. It stands on Button (trigger identity + focus) and Dialog (Top Layer + @starting-style exit animation), diverging from Dialog via a non-trapping focus model + light-dismiss.

The landscape is in extreme formalization/volatility. Historically positioning + light-dismiss needed JS (Floating UI / Popper). As of early 2026 the native HTML Popover API (Baseline early 2025; popover="hint" via Interop 2026) + CSS Anchor Positioning have rewritten the architecture. The Popover API natively handles Top Layer, z-index, Escape. CSS Anchor Positioning declaratively tethers/repositions elements in CSS, bypassing JS layout thrashing. The mandate: CSS-anchor-first, JS physics engine strictly as fallback for unsupported environments / nested shadow DOM edge cases, while managing the layout constraints and containing-block anomalies the spec introduces.

## 2. Anatomy and Parts
Trigger/Anchor: interactive gateway inheriting Button; dual identity — semantic invoker + mathematical reference point; instrumented with anchor-name / popovertarget; emerging interestfor / commandfor declarative wiring. Popover Surface: transient container in the Top Layer (isolated from z-index stacking, no overflow:hidden clipping); non-trapping + light-dismiss. Arrow/Caret: optional directional affordance; must stay attached to the trigger center even as the body shifts on the cross-axis. Internal slots: Header/Body/Footer (content-dependent — non-modal dialog uses all; rich tooltip just a body). Close Affordance: explicit close in header/footer for cognitive accessibility (deterministic dismissal beyond background clicks).

## 3. Properties / API
open/defaultOpen + onOpenChange. asChild trigger composition (Radix/Base Web) merges listeners/ARIA into a custom child without wrapper nodes; React Aria usePopover decouples state/positioning. Positioning model (three vectors): Placement/Alignment (Radix side+align; Fluent positioning shorthand 'above-start'; Base Web concatenated 'topRight'; CSS position-area 3x3 grid). Main/Cross-axis offset (sideOffset/alignOffset; CSS anchor() inset/margin). Collision (avoidCollisions; Fluent flipBoundary/overflowBoundary; Base Web ignoreBoundary; CSS @position-try + position-try-fallbacks like flip-block). Two strategies: flipping (invert across main axis) + shifting (slide along cross axis). Light-dismiss: closeOnEscape + closeOnInteractOutside (implicit with popover="auto"). Focus: initialFocus + trapFocus (default false — a generic popover is non-modal; focus moves in but is not trapped).

## 4. States and Variants
Binary open/closed + ephemeral animating. Trigger: Hover vs Click. Click = intentional/interactive. Hover = delayed presentation (onMouseEnterDelay/onMouseLeaveDelay to avoid flashing); strictly descriptive/read-only content (requiring a motor-impaired user to navigate a pointer into a vanishing surface violates a11y heuristics). Role-typed variants by enclosed content: dialog (non-modal form), listbox (Select/Combobox), menu (commands), tooltip (hints). showArrow variant adds caret-position complexity (independent of the surface during shift). same-width variant (Combobox/Select dropdown): historically JS width measurement; Ariakit --popover-anchor-width; native anchor-size() (width: anchor-size(width)).

## 5. Usage Guidance
Sharpest line: Popover vs Tooltip (Material 3: Rich vs Plain Tooltips). Tooltip/Plain Hint: hover/focus only, purely descriptive non-interactive text, the visual manifestation of aria-label/description. Popover/Rich Hint: click, interactive elements, persistent until dismissed. Blurring (a hyperlink in a hover tooltip) = severe failure for screen-magnification/alternative-pointer users. Menu: strictly role=menu commands + arrow-key nav; generic Popover is structurally agnostic. Popover vs Dialog/Drawer: modality + focus trapping. Dialog = modal, background inert; Popover = non-modal, background interactive, focus not trapped. Carbon: non-modal popovers when the user must reference on-page info while interacting. Drawer = modal but viewport-edge anchored. Focus framework: interactive content -> focus moves in on open; informational -> focus stays on trigger; always return focus to the trigger on dismiss.

## 6. Accessibility
The native Popover API introduced a critical accessibility gap. popovertarget wires light-dismiss + Esc but does NOT auto-generate comprehensive semantic relationships. It implicitly establishes aria-details (trigger->popover) + implicit aria-expanded, but aria-details is often insufficient (proprietary screen readers ignore or handle it inconsistently vs aria-controls), and the [popover] element has no mandated implicit role (defaults to generic group). Relying solely on declarative popovertarget ships inaccessible overlays. Mandate three: explicit aria-expanded on the trigger Button, explicit aria-controls to the popover id, explicit role on the surface. Role-by-content: dialog/listbox/menu by content. Plain vs Rich hints (popover="hint"): Plain Hints map as flattened text strings (SR reads on trigger focus, doesn't navigate in); Rich Hints toggle aria-expanded (new surface announced, navigable). Hover popovers: WCAG 1.4.13 — dismissable (Esc, no pointer move), hoverable (pointer can move to surface without it vanishing), persistent (until hover removed/dismissed).

## 7. Content Guidelines
Transient + light-dismiss = susceptible to accidental closure. Never for long-form data entry / multi-step workflows / progress-loss risk — that belongs in a full-page route or focus-trapping Dialog. Dense content -> explicit Close/Cancel affordance. Arrow when the popover is distanced from its trigger by collision shifting, or when multiple triggers are in close proximity (ambiguity).

## 8. Motion and Transition
Inherits Dialog's @starting-style + transition-behavior: allow-discrete (native Top Layer removal). Origin-aware: animation must originate from the trigger. Radix injects --radix-popover-content-transform-origin (top-center when below; flips to bottom-center when collision flips it above) so scaling/opacity emerge from the anchor. Respect prefers-reduced-motion.

## 9. Internationalization
RTL-aware via CSS Logical Properties — hardcoded top/right/bottom/left fail in mirrored interfaces. CSS Anchor Positioning replaces physical alignments with the position-area grid using logical axes (block-start/end, inline-start/end). inline-start auto-flips left->right on dir change, no JS/observers/recalculation. Logical properties also govern arrow offset padding + content expansion.

## 10. Naming
Field-wide consensus on Popover (Radix, React Aria, Fluent, Carbon, Polaris, Ariakit, Base Web). Atlassian = Popup (identical mechanics). Primer = Overlay / AnchoredOverlay (topological abstraction). Practice default: Popover (mirrors the native popover attribute; ~80%+), establishing the generic positioning base so Tooltip/Menu are clearly semantic specializations.

## 11. Implementation Notes
Platform-first: the [popover] attribute promotes to Top Layer + manages light-dismiss across three modes. popover="auto" = one-open-per-ancestor (opening a new auto popover closes other unrelated auto popovers). popover="manual" = no light-dismiss (persistent notifications). popover="hint" = secondary ephemeral stacking; opening a hint does NOT close an open auto popover — resolving the long-standing bug where hovering a tooltip inside a dropdown menu collapsed the menu.

CSS Anchor Positioning displaces Floating UI: anchor-name: --x on trigger; position-anchor: --x + position-area on the absolute surface; @position-try (position-try-fallbacks: flip-block); anchor-size() for trigger-width inheritance.

LIMITATIONS — the Containing Block Trap: the anchor must be fully laid out before the anchored element. If the anchor is a parent of the popover with any position other than static, it establishes an Inset-Modified Containing Block (IMCB) and the positioning math fails silently (misaligned/invisible). A positioned element cannot reference an anchor outside its containing block, nor one in a higher Top Layer. Consequence: enforce strict DOM hierarchies (trigger + popover adjacent siblings). Atlassian handles placement via shouldRenderToParent (rather than blindly portaling to body). For nested Shadow DOM / unsupported browsers, a polyfill (Oddbird) or headless Floating UI fallback remains necessary. Headless (Radix/React Aria) decouples positioning hooks + ARIA from styling.

## 12. Related and Alternative Components
Button (trigger substrate). Dialog (modal counterpart; shared Top Layer + exit-animation; non-modal dialogs are structurally Popovers with role=dialog but no trap). Tooltip (specialized popover; hover/focus, plain text, popover="hint"). Menu (specialized popover, role=menu, menuitem command lists, arrow-key nav). Select/Combobox (specialized popovers, role=listbox, anchor-size(width) to align edges). Drawer (modal, viewport-edge anchored).

## 13. Field POV Evolution
Era 1 — Portals + Z-Index (append to <body> to dodge overflow:hidden clipping; z-index wars). Era 2 — Headless Abstraction + JS Physics (usePopover; Popper.js/Floating UI decoupled from styling). Era 3 — The Platform Era (native Top Layer resolves portals + z-index; popover="hint" gives reliable stacking; CSS Anchor Positioning displaces JS physics — collision math + tethering in the CSS engine; Primer's feature-flagged migration is the enterprise tipping point). Abandoned the assumption that aria-haspopup suffices -> strict role-by-content mandate.

## 14. Sources Cited
HTML Popover API + popover="hint" (Chrome Developers, WebKit Interop 2026). CSS Anchor Positioning (CSS-Tricks almanac, MDN, W3C Editor's Draft CSS Anchor Positioning L1, Oddbird IMCB + polyfill). Radix UI + Adobe React Aria v3.0+. Material 3 (tooltip boundaries). W3C/Open UI GitHub issues (popovertarget gap, interestfor, APG patterns). Verified through mid-2026.

## 15. Agent-Consumable Schema

```yaml
component_id: popover
name: Popover
description: A generic anchored transient surface providing mathematical positioning, light-dismiss, and Top Layer management. Serves as the structural substrate for Tooltip, Menu, Select, and Combobox.
inherits:
  - components/button.md (Trigger element identity and baseline focus)
  - components/dialog.md (Top Layer isolation, @starting-style exit animations)
api:
  properties:
    open: {type: boolean}
    defaultOpen: {type: boolean}
    onOpenChange: {type: function(boolean)}
    placement: {type: string | position-area value, description: 'e.g. block-start, top span-left'}
    offset: {type: number | string, description: main-axis distance}
    crossOffset: {type: number | string, description: cross-axis shift}
    avoidCollisions: {type: boolean, default: true, description: flip/shift via position-try-fallbacks or JS}
    trapFocus: {type: boolean, default: false, description: 'generics non-modal; focus moves in but not trapped'}
    closeOnEscape: {type: boolean, default: true}
    closeOnInteractOutside: {type: boolean, default: true}
  slots:
    trigger: {description: interactive invoker / positioning anchor}
    content: {description: Top Layer surface}
    arrow: {description: optional directional indicator tethered to trigger center}
accessibility:
  roles: [dialog, listbox, menu, tooltip] # MUST be mapped dynamically via enclosed content
  attributes:
    trigger: {aria-expanded: required, aria-controls: 'required (bypass native gaps)', popovertarget: 'required (native top layer + light-dismiss)'}
    content: {popover: 'auto | manual | hint', role: 'required (content-dependent)'}
  focus_contract: |
    Focus shifts into the popover on opening ONLY IF it contains interactive elements.
    Plain hint/tooltip: focus remains on the trigger. On unmount, focus MUST return to the trigger.
notes:
  unverified: |
    - CSS Anchor Positioning (position-area, position-try-fallbacks) is volatile. Verify IMCB layout rules before removing JS polyfills.
    - popover="hint" + interestfor/commandfor reaching Interop 2026 Baseline; verify Rich-vs-Plain hint a11y mappings across proprietary screen readers.
```

# Drawer (Sheet) — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/drawer.md`; version numbers and the inherited no-native-detents / `@starting-style` platform-state flagged unverified. The two passes converged almost completely — no substantive disagreement.*

---

Drawer (Sheet) Component: Field-Truth Study and Implementation Substrate

## 1. Framing
The Drawer (aliased Sheet, Side Panel, Flyout) is the terminal overlay execution — edge-anchored, unlike the centered Dialog. The modal Drawer is not a distinct primitive: it inherits the entire modal overlay machinery of the Dialog (focus-trap, scrim, top-layer via <dialog>/showModal(), scroll-lock), diverging by establishing a continuous spatial relationship with the viewport edge. The critical fork is modal vs non-modal (persistent): modal renders a scrim, traps focus, halts background scroll (a Dialog at the perimeter); non-modal ("push"/"squeeze"/inline) retains background interactivity, no scrim, lets focus exit, often squeezes the main content sideways. The field is fractured: Chakra discourages non-modal (focus/orientation hazards — if mandated, disable pointer-events on the wrapper, override modal); Fluent ships InlineDrawer for side-by-side enterprise workflows; Carbon uses non-modal "Side Panels"; Material 3 taxonomizes Modal / Standard(Permanent) / Dismissible. The practice default must decouple the non-modal variant from native showModal() (which enforces top-layer inertness + backdrop). Mobile: drawers collapse to a bottom sheet (Apple HIG / Vaul) — a distinct environment of swipe velocities, spring physics, safe-area insets, partial-height detents.

## 2. Anatomy and Parts
Scrim (modal only; ::backdrop). Edge-anchored surface (logical inset properties; own stacking context; max-width/height tokens). Drag handle/grabber (mobile sheet; Material 48dp hit target). Header (title + close; aria-labelledby; sticky). Scrollable body (overflow-y scoped here). Footer (transactional actions; Fluent dictates primary inline-start, others inline-end; sticky).

## 3. Properties / API
open/isOpen (controlled). onOpenChange/onClose. placement/direction (logical inline-start/end/top/bottom). modal (default true — toggles overlay, focus trap, scroll lock; false pushes sibling content / rests inline). size/width (Atlassian narrow/medium/wide/extended/full). dismissible (scrim click / Escape / downward drag). push (Ant nested — primary drawer translates back e.g. {distance:180}). Mobile detents/snap points: Vaul snapPoints (array of px / vh% / fractions e.g. ["148px","355px",1]), activeSnapPoint, fadeFromIndex (detent at which the scrim begins to fade — lower detents non-modal, higher modal), snapToSequentialPoint (force adjacent-detent snap regardless of velocity). Apple HIG: medium/large system detents.

## 4. States and Variants
Behavioral: Modal Navigation Drawer (mobile/tablet, hamburger, left/inline-start, traps focus); Utility/Detail Inspector (right/inline-end; Carbon "Side Panel" — edit while referencing); Bottom Sheet (mobile, bottom edge, gesture states). Physical/temporal: Animating (DOM exists, interaction throttled); Dragging (breaks fixed layout, tracks pointer Y-delta via rAF / motion); Detent/Resting (iOS 15+ — locked to a Y coordinate, still interactive).

## 5. Usage Guidance
Drawer preserves peripheral context (reference a table/chart behind while filling a form -> non-modal right-aligned). Total cognitive isolation (destructive confirm) -> centered Dialog. Drawer vs Dialog: edge-anchored/context-preserving vs centered/context-destroying. Drawer vs Side Navigation: transient overlay vs permanent structural DOM; on shrink, Side Nav -> Modal Drawer. Drawer vs Popover: viewport-edge-anchored vs reference-element-anchored (floating). Fluent: never invoke multiple overlay drawers simultaneously (nested focus-trap labyrinth); limit multi-step to 2-3, else escalate to a page route.

## 6. Accessibility
Modal: WAI-ARIA Dialog pattern — role="dialog" + aria-modal="true" (AT ignores DOM outside), focus trap (move to first interactive/close on open, Tab cycles looping, Escape dismisses + returns focus to trigger). Non-modal/persistent: cannot use aria-modal, must never trap focus (traps user inside a panel they can see past); acts as a sibling landmark — role=region/complementary (supports main) or navigation (routing links); focus Tabs naturally out. Gesture (WCAG 2.5.7 Dragging Movements, AA, new in 2.2): any dragging functionality must provide a single-pointer alternative without dragging — sip-and-puff / tremor users can't velocity-swipe. A gesture-only sheet is non-compliant: provide a visible Close button + programmatic Expand/Collapse buttons or arrow support for detents. Gestures are an enhancement, not the sole pathway.

## 7. Content Guidelines
Title: succinct, sentence case, no terminal punctuation, aria-labelledby. Body: scannable, labeled inputs; long text (privacy policies) -> dedicated pages. Footer: Fluent primary inline-start; labels = verb response to title ("Delete Account" -> "Delete" not "Submit"). Drag handle: distinct but neutral; Material 48dp hit target.

## 8. Motion and Transition
Edge slide via native <dialog>: @starting-style (initial translate offset) + transition-behavior: allow-discrete (animate display) + ::backdrop fade. Spring physics + drag velocity engine (motion/react, Vaul): maps pointer Y-delta to a reactive motion value; on release computes predictedEndTranslation + velocity; if velocity exceeds ~-500px/s, dismiss (overpower detent magnets); else snap to nearest snapPoint (inertia with bounceStiffness/bounceDamping, iOS-like). Background scaling illusion (Vaul [data-vaul-drawer-wrapper]): scale() the background to 0.93 + border-radius for depth — BUG: on deep-scroll pages (20,000px) scaling the body offsetHeight jumps the background by thousands of px; use a localized wrapper div, not the raw body. prefers-reduced-motion respected.

## 9. Internationalization
Anchoring is susceptible to RTL corruption with physical properties (left/right/translateX) — animations fire from the wrong side / off-canvas. Enforce CSS logical properties: inset-inline-start/end (resolves to right/left in RTL), margin-inline-start, inset-block-start (stays top), border-inline-start. Zero JS — the layout engine mirrors off dir="rtl". Bottom sheet (inset-block-end) is direction-neutral, though inner content respects inline-start.

## 10. Naming
Drawer (Material/Ant/Chakra — canonical web). Sheet (Apple HIG; shadcn — distinguishes from centered dialogs). Side Panel (Carbon — semantic position + context-preserving). Panel/Drawer (Fluent — historically Panel, consolidated to Drawer). Drawer (Base Web — aliases flyout, tray, junk drawer). Practice default: Drawer for vertical edge-anchored (left/right); reserve Sheet for bottom-anchored gesture-driven detent surfaces.

## 11. Implementation Notes
The <dialog> top-layer trap: showModal() gives native focus-trap, escape dismissal, top-layer (escapes z-index wars), ::backdrop — but ONLY for modal. It is structurally impossible to use showModal() for a non-modal push drawer (the spec enforces background interactivity blocking). So a robust component conditionally renders a portalled <div> for non-modal and a native <dialog> for modal, with seamless prop parity across two DOM structures. Squeeze/push: cannot float via position:fixed — wrap <main> and apply margin-inline-end / translateX = drawer width when open; needs global state. Lack of native detents: no native HTML/CSS spec for detents or velocity snapping — requires PointerDown/Move/Up polling, bounding boxes to prevent scroll-chaining (sheet internal scroll vs background), optimized rAF velocity. Vaul/React Aria provide the physics headlessly. Focus loss/portal loop bug: Modal Drawer + Combobox/Select/Popover inside — the inner control portals its dropdown to document.body (outside the Drawer DOM), the Drawer's focus trap detects focus "escaped" and yanks it back, closing the dropdown before interaction. Fix: focus-trap exemptions, or render the portal inside the Drawer's boundary.

## 12. Related and Alternative Components
Dialog (centered substrate; Drawer inherits role=dialog + modal mechanics, shifts placement). Side Navigation (permanent structural; collapses into a Modal Drawer on shrink). Popover (reference-element-anchored, floats to avoid collision; Drawer is viewport-edge-anchored). Toast/Snackbar (slides from edge but no focus trap, no scrim, auto-dismiss).

## 13. Field POV Evolution
Headless UI (Radix/React Aria/Ark) decoupled behavior from styling — practitioners consume a headless Dialog primitive and bind it to the edge with tokens. Bottom Sheet democratization — Vaul standardized touch gestures + spring physics + background scaling into a consumable package, closing the native-mobile-vs-web uncanny valley. Gesture accessibility hardening — WCAG 2.2 SC 2.5.7 forced hybrid surfaces with explicit single-pointer button alternatives for every drag action.

## 14. Sources Cited
Ant Design Drawer (v4-6; placement, nested push, sizing). Apple HIG Sheets/Detents (iOS 15/16). Atlassian Drawer (v12.1.4; sizing tokens). Base Web Drawer (aliases). Carbon Side Panel / UI Shell (v10/v12; non-modal context preservation). Chakra UI Drawer/Dialog (v2/v3; accessibility warnings vs non-modal). Microsoft Fluent UI Drawer/Panel (overlay vs inline). Material 3 Navigation Drawer / Bottom Sheet (taxonomy, 48dp handle). React Aria Modal/Sheet (headless physics). shadcn/ui Sheet/Drawer (Radix Dialog substrate). Vaul (v0.4.1/v1.1.2, Dec 2025; snap points, spring physics, scaling bugs). W3C WCAG 2.2 SC 2.5.7. WAI-ARIA APG Dialog/Landmarks.

## 15. Agent-Consumable Schema

```yaml
name: Drawer
aliases: [Sheet, Side Panel, Panel, Flyout, Tray, Bottom Sheet]
description: An edge-anchored overlay or inline panel for secondary content, configuration forms, or hierarchical navigation. Closes the overlay component arc.
inherits: Dialog (modal overlay machinery, top-layer elevation, focus-trap physics, escape-to-dismiss)
anatomy:
  - root: positioning container or <dialog> substrate (stacking context)
  - backdrop: scrim (modal=true only) capturing outside clicks
  - surface: edge-anchored container (bg, radii)
  - handle: drag grabber (bottom sheets; 48dp hit target)
  - header: sticky top (title + close)
  - title: aria-labelledby link
  - closeButton: dismiss affordance (required for WCAG 2.5.7 as drag alternative)
  - body: overflow-y:auto scoped region
  - footer: sticky bottom actions (primary inline-start per Fluent)
props:
  open: {type: boolean, default: false}
  onOpenChange: {type: function(open)}
  placement: {type: enum [inline-start, inline-end, top, bottom], default: inline-end, note: logical for RTL}
  modal: {type: boolean, default: true, note: scrim+trap+scroll-lock; false pushes sibling content}
  size: {type: enum [xs,sm,md,lg,xl,full] | string | number, default: md}
  dismissible: {type: boolean, default: true}
  snapPoints: {type: array<string|number>, note: detent altitudes for bottom sheets}
  activeSnapPoint: {type: string|number}
accessibility:
  role: {modal: 'dialog (+ aria-modal=true)', non-modal: 'region | complementary | navigation (NOT aria-modal)'}
  focusModel: {modal: 'strict trap, returns focus to trigger', non-modal: 'no trap; Tab exits to main document'}
  gestureCompliance: visible operable button alternatives to any drag-to-dismiss / swipe-to-snap (WCAG 2.5.7)
motion:
  transition: transform + opacity (@starting-style + allow-discrete for native dialogs)
  physics: velocity inertia + spring dampening for drag (bottom sheets)
  logical_properties: inset-inline-start/end to mirror in RTL without JS
notes:
  unverified: "Background scaling on deep-scroll pages causes offsetHeight recalculation bugs; scale localized wrappers, not document.body."
```

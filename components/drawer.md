---
okf_version: "0.1"
type: component-brief
title: Drawer (Sheet)
description: The edge-anchored Overlay that closes the Overlay arc — a modal drawer is structurally a Dialog anchored to a viewport edge, a non-modal/persistent drawer pushes content and stays interactive. A field-truth study of the modal-vs-non-modal (overlay-vs-push) decision, edge anchoring via logical placement (RTL mirrors), the bottom-sheet detents/snap-points + drag-to-dismiss (and the mandatory button alternative — WCAG 2.5.1/2.5.7), the focus model (trap when modal, complementary/navigation landmark when persistent), the native-dialog-can't-do-non-modal split, the focus-loss/portal-loop trap, and the drawer-vs-dialog-vs-side-nav-vs-popover boundaries — with the practice's defaults.
tags: [components, overlay]
category: Overlay
status: stable
aliases: [sheet, side-panel, panel, bottom-sheet, tray, flyout]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Drawer (Sheet)

> Drawer is the edge-anchored Overlay and the fifth brief that **closes the Overlay arc** (Menu, Dialog, Popover, Tooltip, Drawer). A *modal* drawer is, structurally, **a Dialog anchored to a viewport edge** — it inherits the focus-trap contract, the scrim, the top layer, scroll-lock, the native `<dialog>`+`showModal()` path, the `@starting-style`/`allow-discrete`/`overlay` exit animation, and the close/footer Buttons (see dialog), changing only the anchoring (an edge, not centred) and the motion (a slide, not a scale). It is also the real form of the **mobile bottom sheet** Dialog gestured at. The defining decision is **modal vs. non-modal/persistent — overlay vs. push**: a modal drawer overlays with a scrim, traps focus, and locks scroll; a non-modal/persistent drawer *pushes or squeezes* the page, leaves the background interactive, and does not trap or scrim. The bottom sheet adds its own substance — detents/snap points, drag physics, and the hard rule that any drag gesture has a button alternative (WCAG 2.5.7). What it isn't: a centred Dialog, a *persistent* Side Navigation structure (a drawer is its temporary/mobile form), or a small anchored Popover.

---

## 1. Framing

A Drawer is an **edge-anchored overlay panel** sliding in from a viewport edge (inline-start/end, block-start/end) to hold a focused task, a detail inspector, a filter set, or mobile navigation. It stands on **Dialog** for the modal case (see dialog) and is the form Dialog's mobile-sheet transform takes.

**The defining decision is modal vs. non-modal/persistent (overlay-vs-push):**
- **Modal drawer** — scrim, **focus trap**, scroll-lock (a Dialog at the edge): a focused task, or mobile nav behind a hamburger.
- **Non-modal / persistent drawer** — **pushes/squeezes** the page sideways, background stays **interactive**, no trap, no scrim: a filter panel that updates results live, a detail inspector edited against the list behind it, a desktop nav rail. This is the **reference-while-working** case — the main reason to pick a non-modal drawer over a modal Dialog.

The field is **genuinely fractured** on the non-modal case: **Chakra** discourages it (focus/orientation hazards — if you must, you disable pointer-events on the wrapper and override `modal`), while **Fluent** ships a first-class `InlineDrawer` and **Carbon** a non-modal "Side Panel" precisely for editing-while-referencing enterprise workflows. **Material 3** taxonomises three archetypes: **modal** (scrimmed) / **standard/permanent** (inline, part of the layout) / **dismissible** (non-modal but closeable).

What it *isn't*: a **Dialog** (centred, destroys spatial context — see dialog), a **Side Navigation** (a *persistent structural* part of the page; a drawer is its temporary/mobile form — see side-navigation), or a **Popover** (a small surface anchored to a *trigger*, not the viewport edge — see popover). Why systems disagree: the non-modal philosophy, the bottom-sheet detent model, and the Drawer-vs-Sheet naming line.

## 2. Anatomy and parts
- **scrim / backdrop** — modal only (inherited Dialog `::backdrop`); absent for the non-modal push.
- **edge-anchored surface** — the panel pinned to an edge via CSS **logical inset** properties (full-height side / partial-height bottom sheet); top layer when modal; carries max-width/height tokens so it doesn't overwhelm wide/tall viewports.
- **drag handle / grabber** — the bottom-sheet swipe/resize affordance; Material mandates a **48dp hit target** around the visual pill.
- **header** — title (`aria-labelledby`) + close button; sticky (immune to body scroll).
- **body** — the `overflow-y:auto` region (overflow scoped *here* so header/footer stay put).
- **footer** — action Buttons, sticky; primary aligned inline-end by the practice default (Fluent is the outlier, dictating inline-**start** — §7).

## 3. Properties / API
- **`open` / `defaultOpen` + `onOpenChange`** — controlled/uncontrolled (inherited Dialog).
- **`placement` / `direction`** — `inline-start`/`inline-end`/`block-start`/`block-end` (logical, so RTL mirrors — §9); default inline-end for utility, inline-start for nav, block-end for the mobile sheet.
- **`modal`** — modal (scrim + trap + scroll-lock — the `<dialog>` path) vs non-modal/persistent (push, interactive background); default modal for temporary drawers.
- **`size` / `width`** — semantic tokens (Atlassian's `narrow`/`medium`/`wide`/`extended`/`full`) or a value; full-bleed on small viewports.
- **`dismissible`** — whether scrim-click / Escape / downward-drag close it (off for blocking flows).
- **bottom-sheet detents** — **`snapPoints`** (an array of px / viewport-% / fractions, e.g. `["148px", 0.5, 1]`), **`activeSnapPoint`**, **`fadeFromIndex`** (the detent at which the scrim starts fading in — lower detents stay non-modal, higher become modal), **`snapToSequentialPoint`** (forbid velocity skipping over intermediate detents).
- **`push`** (Ant) — for the discouraged-but-supported nested case: the parent drawer translates back (~180px) to give depth (§5).
- **focus** — `initialFocus`/`restoreFocus` (inherited Dialog); `trapFocus` true for modal, false for persistent.
- **role/aria** — `role=dialog`+`aria-modal` (modal) vs `complementary`/`navigation` landmark (non-modal — §6).

## 4. States and variants
- **States:** closed / open / **animating** (slide; exit inherits Dialog) / **dragging** (bottom sheet — breaks fixed layout to track the pointer's Y-delta frame-by-frame) / per-**detent/resting** (locked to a snap altitude, still interactive).
- **Variants:**
  - **modal** (scrim, trap) vs **non-modal/persistent** (push, interactive) — Material's temporary / dismissible / permanent.
  - **by content:** **navigation drawer** (hamburger panel / nav rail, inline-start) vs **utility/detail drawer** ("Side Panel" — filters/inspector/edit, inline-end) vs **bottom sheet** (mobile, block-end, detents).
  - **placement** — inline-start / inline-end / block-start / block-end.
  - **size** — narrow…full.

## 5. Usage guidance
- **Use a modal Drawer** for a focused secondary task or mobile navigation — when the user should deal with the panel before returning, and the edge anchoring suits a tall list/form or the mobile idiom.
- **Use a non-modal / persistent Drawer** when the user must **reference or act on the main page while the panel is open** — a live filter panel, a detail inspector edited against the list behind it, a desktop nav rail. (The reference-while-working case — the main reason to pick non-modal over a modal Dialog.)
- **Don't use a Drawer for:** content with **no edge relationship** that belongs centred (→ Dialog), a **persistent primary navigation structure** (→ Side Navigation — a drawer is its temporary/mobile form), or a **small contextual surface anchored to a control** (→ Popover/Menu).
- **Decision frameworks:**
  - **Modal vs. non-modal:** finish-with-the-panel-first (modal, trap + scrim) vs. work-the-page-alongside (non-modal, push, no trap).
  - **Drawer vs. Dialog:** edge-anchored + tall/list/nav/reference-while-working (Drawer) vs. centred + total cognitive isolation, e.g. a destructive confirm (Dialog). On mobile a Dialog often *becomes* a bottom sheet.
  - **Drawer vs. Side Nav:** transient/toggled panel (Drawer) vs. persistent layout structure (Side Nav); the mobile transform is side-nav → modal drawer behind a hamburger.
  - **Constraints:** **never stack simultaneous overlay drawers** (a labyrinth of nested traps — Fluent); cap in-drawer flows at **two–three steps**, else escalate to a page route; if nesting is unavoidable, use Ant's `push` (parent translates back).

## 6. Accessibility
The Drawer's a11y model **splits completely on modality.**

- **Modal drawer:** inherits the **Dialog** pattern wholesale — `role="dialog"` + **`aria-modal="true"`** (AT ignores the rest of the DOM), the focus trap (focus moves in, Tab cycles, Escape closes + **returns focus to the invoker**, initial focus never on a destructive button, the lost-invoker fallback), scroll-lock + scrollbar compensation, labelling via `aria-labelledby`.
- **Non-modal / persistent drawer:** must **not** use `aria-modal` and must **not** trap focus (trapping in a non-modal panel strands the user inside a panel they can see *past*). It's a sibling **landmark** — **`complementary`** (a detail/filter aside supporting the main content) or **`navigation`** (a nav drawer), labelled, left in the normal flow so Tab exits naturally into the page.
- **Gesture accessibility (the Drawer-specific rule):** drag/swipe must **never be the only way** — **WCAG 2.5.1 (Pointer Gestures)** requires a single-pointer alternative to any path/multipoint gesture, and **2.5.7 (Dragging Movements, AA, new in 2.2)** requires a *non-dragging* alternative to any drag (users with tremor / sip-and-puff switches can't fling-to-dismiss). So a swipe-to-dismiss sheet **must also** have a visible **Close button** (+ tap-scrim), and multi-detent sheets need **buttons / arrow-key support** to move between detents without the drag engine. Gestures are an *enhancement*, never the sole pathway.
- **WCAG SCs:** **2.5.1 / 2.5.7** (the gesture rules — the headline addition over Dialog), plus the modal drawer's inherited Dialog SCs (2.4.3, 2.1.2, 4.1.2, 1.4.13, 2.4.11) and the landmark SCs (1.3.1, 2.4.1) for the non-modal case.

## 7. Content guidelines
- **Title** — succinct, sentence-case, no terminal punctuation, `aria-labelledby`-linked; names the panel's purpose ("Filters", "Order details").
- **Body** — prioritise scannability and discrete interactions; relegate long-form text (T&Cs, policies) to a page, not a constrained overlay.
- **Footer actions** — labels are a direct verb response to the title ("Delete account" → "Delete", not "Submit"); a filter drawer often applies live (no footer). **Footer order**: the practice default is primary inline-**end** (consistent with Dialog §9); **Fluent is the documented outlier** placing primary inline-**start** — pick one and apply it consistently, mirrored under RTL.
- **Drag handle** — visually distinct but neutral; the 48dp hit target (the visible affordance for the swipe, paired with the close button per §6).

## 8. Motion and transition
Slide from the anchored edge — a `translate` from off-screen + the Dialog substrate (`@starting-style`/`allow-discrete`/`overlay`, scrim fading for the modal variant). The non-modal push **animates the page margin/transform** alongside the drawer's slide. The **bottom sheet** is a JS spring engine: it maps the pointer's Y-delta to a motion value 1:1 during drag, and on release computes a `predictedEndTranslation` from position + **velocity** — a hard fling past a threshold (~−500px/s) **dismisses** (overpowering the detent magnets), a slow release **springs to the nearest snap** (inertia with `bounceStiffness`/`bounceDamping`, iOS-like). The optional **background-scaling illusion** (vaul: `transform: scale(0.93)` + `border-radius` on the app wrapper for depth) is a documented trap — scaling `document.body` on a tall page (a 20,000px feed) makes the background **jump by thousands of px**; scale a *localised wrapper*, not the raw body. Under `prefers-reduced-motion: reduce`, drop the slide/scale to a fade or snap. (See dialog §8, 18-motion-foundations, 19-motion-implementation-web.)

## 9. Internationalization
- **RTL** — placement uses **CSS logical properties** (`inset-inline-start`/`inset-inline-end`, `margin-inline-start`, `border-inline-start`) so a start-edge drawer flips from left (LTR) to right (RTL) with **zero JS** — the layout engine mirrors purely off `dir="rtl"`. Hardcoded `left`/`right`/`translateX` is the corruption trap (animations fire from the wrong side / render off-canvas). The slide direction and chevrons mirror; the bottom sheet (`inset-block-end`) is **direction-neutral** in anchor, though its inner content still respects inline alignment.
- **Text expansion** — drawer content (forms, nav labels) expands; size to content, fluid height. (See 13-internationalization-and-rtl.)

## 10. Naming
**`Drawer`** (Material, Ant, Chakra, Base Web, vaul) and **`Sheet`** (Apple HIG; shadcn's Radix-Dialog edge panel) are the two names; **`Side Panel`** (Carbon) / **`Panel`** (Fluent, historically) is the non-modal framing. **The practice default: `Drawer`** for the edge-anchored overlay (vertical inline-start/end side panels), with **`placement`** + **`modal`** as props — and reserve **`Sheet`** specifically for the **bottom-anchored, gesture-driven, detent** mobile variant (the meaningful behavioural distinction). The persistent navigation case routes to **`Side Navigation`** (a drawer is its temporary/mobile form). Aliases to map: `Sheet`, `SidePanel`, `Panel`, `Tray`, `Flyout`, `BottomSheet`, `junk drawer` (Base Web's wry internal alias).

## 11. Implementation notes
- **A modal drawer is a Dialog at the edge** — reuse the Dialog implementation (native `<dialog>`+`showModal()`, top layer, focus-trap, scroll-lock + scrollbar compensation, `@starting-style` animation, close/footer); the *only* delta is the edge anchoring + the slide translate.
- **The native-`<dialog>` can't do non-modal — so you render two DOM structures under one API.** `showModal()` aggressively enforces top-layer inertness + a backdrop, which is *exactly wrong* for a push drawer. So a robust component **conditionally renders a native `<dialog>` for `modal`** and **a portalled `<div>` for non-modal**, keeping prop parity across two different DOM paths. Don't try to force one element to do both.
- **The non-modal push is a layout shift, not an overlay** — the app shell wraps `<main>` and applies `margin-inline-end`/`transform: translateX`/a grid-column equal to the drawer width on open, so content **pushes/squeezes**; background interactive, no scrim/scroll-lock/trap. Needs global state so the layout reacts to the drawer lifecycle.
- **Bottom-sheet detents + drag physics** — `snapPoints` + `activeSnapPoint` + `fadeFromIndex` + `snapToSequentialPoint`; the surface follows the finger 1:1 and springs by position+velocity (§8). **There is no native CSS detent/snap primitive** — it's pointer-event polling + `requestAnimationFrame` velocity math + **scroll-chaining prevention** (the sheet's internal scroll must not bleed into the background). vaul (on Radix Dialog) and React Aria provide the physics headlessly; iOS sheets have native detents the web mimics. (Current-platform-state — verify.)
- **The focus-loss / portal-loop trap (a sharp recurring bug):** a modal drawer traps focus; a **Combobox/Select/Popover opened *inside* it portals its listbox to `document.body`** — *outside* the drawer's DOM — so the trap sees focus "escape" and **yanks it back, slamming the dropdown shut** before the user can pick. Fix: render the inner overlay **inside the drawer's boundary** (Popover's `shouldRenderToParent`/in-place rendering — see popover) or configure focus-trap exemptions for the descendant portal.
- **Gesture + button alternative — always** (WCAG 2.5.1/2.5.7, §6); never gesture-only.
- **Don't hand-roll** — vaul (bottom sheet), Radix `Dialog`/shadcn `Sheet` (side drawer), React Aria, or Fluent `Drawer`; skin them.

## 12. Related and alternative components
- **Stands on:** Dialog (the modal-overlay substrate — focus-trap, scrim, top layer, scroll-lock, native `<dialog>`, `@starting-style` animation, close/footer; a modal drawer is a Dialog at the edge — see dialog), Button (footer/close — see button), Icon (close/handle — see icon).
- **Alternative to / boundary with:** Dialog (centred, total isolation; the edge + reference-while-working case picks Drawer — see dialog), **Side Navigation** (a persistent nav structure; a drawer is its temporary/mobile form — see side-navigation), Popover (small surface anchored to a trigger, not the viewport edge — see popover), Toast/Snackbar (slides from an edge like a drawer but no trap/scrim, auto-dismisses — see toast when briefed).
- **Specialises into:** the navigation drawer, the utility/detail drawer ("Side Panel"), the bottom **Sheet**.

(The edge-anchored overlay that closes the Overlay arc — a modal drawer is a Dialog anchored to an edge; a non-modal drawer is a pushing/squeezing panel. The fifth and final Overlay brief (Menu, Dialog, Popover, Tooltip, Drawer), completing the category. See dialog for the modal substrate and the centred boundary, popover for the small-anchored boundary and the portal-loop fix, side-navigation for the persistent-nav boundary, button for the controls. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The native `<dialog>` made the modal drawer trivial** — `showModal()` + edge positioning + a slide, inheriting the top layer / focus / inertness — while *forcing* the modal/non-modal DOM split (the native element can't do non-modal).
2. **Headless decoupled behaviour from style** — practitioners stopped writing focus-trap/portal/Escape logic and consume a headless Dialog primitive, binding it to an edge with tokens.
3. **vaul + iOS detents democratised the bottom sheet** — snap points, 1:1 drag tracking, and velocity spring-to-snap became the expected web pattern (a JS model; no native CSS detents).
4. **The modal-vs-non-modal philosophy stayed fractured** — Chakra discourages non-modal; Fluent/Carbon embrace the inline panel for enterprise reference-while-working; Material formalised temporary/dismissible/permanent.
5. **Gesture accessibility hardened** — WCAG 2.2's SC 2.5.7 made the button-alternative-to-swipe non-negotiable, shifting the field from gesture-only sheets to hybrid surfaces.

## 14. Sources cited
(Conservative; the external pass cited Ant v4–v6, Atlassian v12.1.4, vaul v0.4.1–v1.1.2 (Dec 2025), Apple HIG iOS 15/16 detents, Material 3 / Compose 1.1.0 — held loosely and flagged unverified.)

- **vaul** (Emil Kowalski — the de facto bottom-sheet Drawer on Radix Dialog; `snapPoints`/`fadeFromIndex`/`snapToSequentialPoint`, spring physics, the background-scaling bug) (2024–2026).
- **Material 3** navigation drawer (modal / standard-permanent / dismissible) + bottom sheet (standard vs modal), the 48dp handle (2024–2026).
- **Ant Design** `Drawer` (`placement`, nested `push`, sizing) (2024–2026).
- **Microsoft Fluent** `Drawer`/`InlineDrawer`/`Panel` (overlay vs inline; the inline-start primary-action footer; never-simultaneous-overlay rule) (2024–2026).
- **IBM Carbon** "Side Panel" (non-modal, context-preserving) (2024–2026); **Chakra UI** `Drawer` (the discouraged non-modal + pointer-events workaround) (2024–2026); **Atlassian** `Drawer` (sizing tokens) (2024–2026); **shadcn/ui** `Drawer` (vaul) + `Sheet` (Radix Dialog) (2024–2026); **Base Web (Uber)** `Drawer` (flyout/tray aliases) (2024); **Adobe React Aria** Modal/Sheet (headless physics) (2024–2026).
- Native HTML **`<dialog>`** (the modal-drawer substrate) + the **lack of native detents** (current-platform-state); **WAI-ARIA APG** — no formal drawer pattern (Dialog pattern, or `complementary`/`navigation` landmark by modality); **Apple HIG** sheets + detents (iOS 15+). WCAG 2.2 (W3C Recommendation, Oct 2023) — **2.5.1, 2.5.7**, plus Dialog's SCs (2.4.3, 2.1.2, 4.1.2, 1.4.13, 2.4.11) and 1.3.1/2.4.1.

## 15. Agent-consumable schema

```yaml
identity:
  id: drawer
  name: Drawer
  aliases: [sheet, side-panel, panel, bottom-sheet, tray, flyout]
  category: overlay
  status: stable
description: >
  An edge-anchored overlay panel sliding from a viewport edge. A MODAL drawer
  is a Dialog anchored to an edge (scrim + focus-trap + scroll-lock); a
  NON-MODAL/persistent drawer PUSHES/squeezes content and stays interactive
  (no trap/scrim) — the reference-while-working case. Closes the Overlay arc;
  the real form of Dialog's mobile bottom sheet. NOT a centred Dialog, NOT a
  persistent Side Navigation (a drawer is its temporary/mobile form), NOT a
  trigger-anchored Popover.
anatomy:
  parts:
    - "scrim/backdrop (modal only; inherited ::backdrop)"
    - "edge-anchored surface (logical inset; full-height side / partial bottom-sheet; top layer when modal; max-width/height tokens)"
    - "drag handle/grabber (bottom sheet; 48dp hit target)"
    - "header: title (aria-labelledby) + close button (sticky)"
    - "body: overflow-y:auto scoped here (header/footer stay put)"
    - "footer: action Buttons (sticky); primary inline-end (Fluent outlier: inline-start)"
api:
  inherits: dialog   # modal overlay machinery — focus-trap, scrim, top layer, scroll-lock, native <dialog>, @starting-style animation, close, footer
  props:
    - {name: open/defaultOpen, type: boolean}
    - {name: onOpenChange, type: function}
    - {name: placement/direction, type: enum, values: [inline-start, inline-end, block-start, block-end], description: "LOGICAL so RTL mirrors; nav=inline-start, utility=inline-end, sheet=block-end"}
    - {name: modal, type: boolean, default: true, description: "scrim+trap+scroll-lock (<dialog> path) vs non-modal/persistent (push, interactive bg)"}
    - {name: size/width, type: "enum|value", description: "narrow/medium/wide/extended/full (Atlassian)"}
    - {name: dismissible, type: boolean, default: true, description: "scrim-click / Escape / downward-drag"}
    - {name: snapPoints, type: "array<px|fraction|%>", description: "bottom-sheet detents e.g. ['148px', 0.5, 1]"}
    - {name: activeSnapPoint, type: "string|number"}
    - {name: fadeFromIndex, type: number, description: "detent at which the scrim fades in (lower detents non-modal, higher modal)"}
    - {name: snapToSequentialPoint, type: boolean, description: "forbid velocity skipping intermediate detents"}
    - {name: push, type: "boolean|object", description: "Ant nested case — parent translates back ~180px"}
    - {name: initialFocus/restoreFocus, type: ref, description: inherited Dialog}
    - {name: trapFocus, type: boolean, description: "true modal / false persistent"}
    - {name: role, type: enum, values: [dialog, complementary, navigation]}
states:
  runtime: [closed, open, "animating (slide; exit inherits Dialog)", "dragging (sheet — tracks pointer Y-delta frame-by-frame)", "detent/resting (locked to a snap altitude, still interactive)"]
variants:
  modality: "modal (scrim, trap) vs non-modal/persistent (push, interactive) — Material temporary/dismissible/permanent"
  by-content: "navigation drawer (hamburger/rail, inline-start) / utility-detail drawer ('Side Panel', inline-end) / bottom Sheet (block-end, detents)"
  placement: [inline-start, inline-end, block-start, block-end]
  size: [narrow, medium, wide, extended, full]
accessibility:
  wcag-criteria: ["2.5.1", "2.5.7", "2.4.3", "2.1.2", "4.1.2", "1.4.13", "2.4.11", "1.3.1", "2.4.1"]
  modal: "inherits Dialog wholesale — role=dialog + aria-modal=true (AT ignores rest of DOM), focus trap (moves in, Tab cycles, Escape closes + returns to invoker, initial focus not destructive, lost-invoker fallback), scroll-lock + scrollbar compensation, aria-labelledby"
  non-modal: "must NOT aria-modal, must NOT trap (else strands the user in a panel they can see past) — a landmark: complementary (detail/filter aside) or navigation (nav drawer), labelled, normal flow (Tab exits)"
  gesture: "drag/swipe NEVER the only way — WCAG 2.5.1 (pointer gestures) + 2.5.7 (dragging movements, AA): single-pointer/non-drag alternative required (Close button + tap-scrim + non-drag detent buttons/arrows). Gestures are an enhancement."
content:
  title: "succinct, sentence-case, no terminal punctuation, aria-labelledby"
  body: "scannable; long-form text -> a page, not a constrained overlay"
  footer: "labels = verb response to title ('Delete'); filter drawer applies live (no footer); primary inline-end (Fluent outlier inline-start)"
  handle: "neutral, 48dp hit target; paired with the close button"
motion:
  slide: "translate from edge + Dialog @starting-style/allow-discrete/overlay (scrim fades for modal); non-modal animates page margin/transform"
  sheet-physics: "1:1 finger-follow during drag; on release predictedEndTranslation from position+velocity — fling past ~-500px/s dismisses, slow release springs to nearest snap (bounceStiffness/bounceDamping, iOS-like)"
  scaling-trap: "vaul background scale(0.93)+radius for depth — scaling document.body on a tall page (20000px) jumps it; scale a LOCALISED wrapper not the raw body"
  reduce-motion: "fade/snap"
i18n:
  rtl: "CSS logical properties (inset-inline-start/end, margin-inline-start, border-inline-start) -> flips off dir=rtl with ZERO JS; hardcoded left/right/translateX is the corruption trap; slide + chevrons mirror; bottom sheet (inset-block-end) direction-neutral in anchor"
  expansion: "content expands — size to content, fluid height"
implementation:
  - "modal drawer = Dialog at the edge — reuse showModal/top-layer/focus-trap/scroll-lock+scrollbar-comp/@starting-style/close/footer; delta is edge anchoring + slide"
  - "NATIVE <dialog> CAN'T DO NON-MODAL (showModal forces inertness+backdrop) -> render two DOM structures under one API: native <dialog> for modal, portalled <div> for non-modal, prop parity"
  - "non-modal push = LAYOUT SHIFT not overlay: app shell applies margin-inline-end/translateX/grid-column = drawer width on open; bg interactive, no scrim/scroll-lock/trap; needs global state"
  - "bottom-sheet detents: snapPoints + activeSnapPoint + fadeFromIndex + snapToSequentialPoint; NO native CSS detent -> pointer-event polling + rAF velocity + scroll-chaining prevention; vaul (Radix Dialog) / React Aria headless; iOS native detents"
  - "FOCUS-LOSS/PORTAL-LOOP TRAP: a Combobox/Select/Popover inside a modal drawer portals to body (outside the trap) -> trap yanks focus back + slams the dropdown shut; fix = render the inner overlay INSIDE the drawer boundary (Popover shouldRenderToParent) or focus-trap exemption for the descendant portal"
  - "gesture + button alternative ALWAYS (2.5.1/2.5.7); never gesture-only; never simultaneous overlay drawers; cap in-drawer flows at 2-3 steps else page route"
  - "don't hand-roll — vaul / Radix Dialog (shadcn Sheet) / React Aria / Fluent Drawer"
composition:
  stands-on: [dialog (modal substrate — a drawer is a Dialog at the edge), button (footer/close), icon]
  alternative-to: [dialog (centred, total isolation), side-navigation (persistent structure; drawer is its temporary/mobile form), popover (trigger-anchored small surface), toast (edge slide but no trap/scrim, auto-dismiss)]
  specialises-into: [navigation-drawer, utility-detail-drawer (Side Panel), bottom-sheet (Sheet)]
notes:
  contested:
    - "modal vs non-modal/persistent (Chakra discourages non-modal; Fluent InlineDrawer + Carbon Side Panel embrace it; Material temporary/dismissible/permanent)"
    - "Drawer vs Sheet naming (practice: Drawer=side, Sheet=bottom-detent)"
    - "footer primary order (practice inline-end; Fluent inline-start)"
    - "the bottom-sheet detent/scaling model"
  trap:
    - "gesture-only dismissal (fails 2.5.1/2.5.7 — needs a button)"
    - "trapping focus in a non-modal/persistent drawer (strands the user)"
    - "forcing native <dialog> to do non-modal (showModal enforces inertness)"
    - "FOCUS-LOSS/PORTAL-LOOP: inner Combobox/Select portal escapes the trap and gets slammed shut"
    - "vaul body-scaling jump on tall pages (scale a wrapper, not body)"
    - "hardcoded left/right (breaks RTL)"
    - "nested/simultaneous overlay drawers"
  inherited: "the entire Dialog modal-overlay substrate (focus-trap, scrim, top layer, scroll-lock, native <dialog>, @starting-style animation, close, footer)"
  role-in-family: "an edge-placement of Dialog — the fifth and final Overlay brief, closing the arc (Menu/Dialog/Popover/Tooltip/Drawer)"
  evolution: "native <dialog> made modal drawers trivial (+ forced the modal/non-modal DOM split); headless decoupled behaviour from style; vaul/iOS detents democratised the bottom sheet; modal-vs-non-modal philosophy still fractured; WCAG 2.5.7 hardened gesture a11y"
  unverified:
    - "external-supplied 2026 version numbers (Ant v4-6, Atlassian v12.1.4, vaul v0.4.1-1.1.2, Material/Compose, iOS 15/16)"
    - "no-native-CSS-detents + the @starting-style/overlay support state (inherited from dialog/popover — the volatile platform claim)"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-drawer/` (16 June 2026), the edge-anchored Overlay that closes the Overlay arc — a modal drawer is structurally a Dialog anchored to a viewport edge (inheriting the focus-trap, scrim, top layer, scroll-lock, native `<dialog>`, `@starting-style` animation, close/footer), a non-modal/persistent drawer is a pushing/squeezing layout panel. The two passes converged almost completely — the modal-vs-non-modal (overlay-vs-push) decision (and the fractured field philosophy: Chakra discourages non-modal, Fluent/Carbon embrace the inline panel, Material taxonomises temporary/dismissible/permanent), edge anchoring via CSS logical placement (RTL mirrors with zero JS), the bottom-sheet detents/snap-points + 1:1 drag + velocity spring-to-snap and the mandatory button alternative (WCAG 2.5.1/2.5.7), the focus model split (modal traps + returns to invoker; non-modal is a complementary/navigation landmark, never trapped), the role-by-modality semantics, scrim/scroll-lock for modal only, and `Drawer` (+ `Sheet` for the bottom-detent variant) naming. External-pass contributions folded in: the **native-`<dialog>`-can't-do-non-modal split** (render a `<dialog>` for modal, a portalled `<div>` for non-modal, under one API), the **focus-loss/portal-loop trap** (an inner Combobox/Select portal escaping the drawer's trap and getting slammed shut — fixed by rendering the inner overlay inside the drawer boundary), the vaul **background-scaling deep-scroll `offsetHeight` jump** (scale a localised wrapper), the `snapPoints`/`fadeFromIndex`/`snapToSequentialPoint` detent API and the velocity threshold, Ant's nested `push`, the Fluent never-simultaneous-overlay + 2–3-step rule and its inline-start footer outlier, and the 48dp handle hit target. Claude-pass contributions: the framing as the arc-closing edge-placement of Dialog, the non-modal-as-layout-shift (not overlay) distinction, and the reference-while-working decision criterion. The 2026 version numbers and the no-native-CSS-detents + `@starting-style`/`overlay` support state (inherited from dialog/popover, the catalogue's volatile platform claim) are flagged unverified. Conformant to `components/_schema.md`. The fifth and final Overlay brief — with Menu, Dialog, Popover, Tooltip, and Drawer, the Overlay category is complete.*

You are researching the Drawer (Sheet) component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a drawer /
sheet is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Drawer is the edge-anchored Overlay, and it CLOSES the Overlay arc
(Menu / Dialog / Popover / Tooltip / Drawer). It STANDS ON one briefed
substrate:
- THE MODAL OVERLAY MACHINERY inherits DIALOG (components/dialog.md): a
  MODAL drawer is, structurally, a Dialog anchored to a viewport edge —
  it inherits the focus-trap contract, the scrim/backdrop, the top layer,
  scroll-lock, the native <dialog>+showModal() path, the @starting-style/
  allow-discrete/overlay exit animation, the close affordance, and the
  footer action Buttons. Don't re-derive these — reference them as
  inherited and concentrate on what is Drawer-specific. The Drawer is also
  the real form of the mobile bottom-sheet Dialog gestured at.
It FORWARD-REFERENCES two siblings: Side Navigation (the PERSISTENT
nav structure — not yet briefed; draw the drawer-vs-side-nav boundary) and
Popover (the small anchored transient surface — see components/popover.md;
draw the drawer-vs-popover boundary).

THE DEFINING DRAWER-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE MODAL vs NON-MODAL / PERSISTENT decision (the headline,
  overlay-vs-push): a MODAL drawer overlays the page with a scrim, traps
  focus, and locks scroll (a Dialog at the edge — for a focused task or
  mobile nav); a NON-MODAL / PERSISTENT drawer PUSHES or squeezes the page
  content sideways, leaves the background interactive, does NOT trap focus
  or scrim (filter panels, detail inspectors, desktop nav rails). Resolve
  the decision framework and Material's temporary / dismissible / permanent
  (standard) drawer taxonomy.
- EDGE ANCHORING / PLACEMENT — left / right / top / bottom, expressed via
  LOGICAL properties (inline-start/end, block-start/end) so RTL mirrors;
  the start-vs-end-edge conventions (nav left/inline-start; detail/utility
  right/inline-end; bottom-sheet on mobile).
- THE BOTTOM SHEET + DETENTS / SNAP POINTS + DRAG-TO-DISMISS (the mobile
  story, the real form of Dialog's mobile-sheet): partial vs full-height
  detents/snap points, the drag handle / grabber affordance, swipe/drag-
  to-dismiss with velocity, and the hard requirement that any drag gesture
  has an accessible button alternative (no gesture-only dismissal). vaul
  (the de facto bottom-sheet reference) and iOS sheet detents.
- THE FOCUS MODEL — modal drawer TRAPS focus and returns it to the invoker
  (inherits Dialog); non-modal/persistent drawer does NOT trap (focus may
  move in but Tab exits to the page); the Escape/dismiss + focus-return
  rules; the persistent-drawer-as-landmark question.
- THE DRAWER vs DIALOG vs SIDE-NAV vs POPOVER boundaries — edge-anchored
  vs centered (Dialog), reference-the-page-while-interacting (a key reason
  to pick a non-modal drawer over a modal Dialog), transient panel vs a
  PERSISTENT navigation structure (Side Navigation), large surface vs a
  small anchored transient surface (Popover). The mobile transform
  (Dialog -> bottom sheet; side-nav -> modal drawer behind a hamburger).
- ROLE / SEMANTICS — role=dialog + aria-modal for the modal drawer;
  complementary / navigation landmark (or just region) for the non-modal/
  persistent drawer; the labelling.
- SCRIM / SCROLL-LOCK — present for modal (inherited from Dialog), absent
  for the non-modal push variant.
- GESTURE ACCESSIBILITY — swipe/drag to open/close must never be the only
  way (WCAG 2.5.1 pointer gestures / 2.5.7 dragging movements); always a
  button/affordance alternative.

Field-leader systems to survey (web): vaul (Emil Kowalski's Drawer, built
on Radix Dialog — the de facto bottom-sheet reference), Material 3
(navigation drawer: modal vs standard/permanent; bottom sheet: standard vs
modal), Ant Design (Drawer — placement left/right/top/bottom, the
canonical API), Microsoft Fluent (Drawer / Panel — overlay vs inline),
Atlassian Design System (Drawer), Chakra UI (Drawer), shadcn/ui (Drawer
[vaul] + Sheet [Radix Dialog]), Base Web (Uber) (Drawer), Carbon (side
panel / the absence of a formal Drawer — a finding). The native HTML
<dialog> (the modal-drawer substrate) and the lack of native detents (a
finding). WAI-ARIA APG (no formal drawer pattern — it is the Dialog
pattern, or a complementary/navigation landmark by modality). Mobile
reference where relevant: Apple HIG (sheets + detents), Material 3 (bottom
sheets). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Dialog modal-overlay substrate;
flag unverified claims under notes.unverified — especially the platform-
state features inherited from Dialog/Popover).

1. Framing — what it is (an edge-anchored overlay/panel) and what it isn't
   (a centered Dialog / a persistent Side Nav / a small Popover); the
   modal-vs-non-modal decision up front; why systems disagree.
2. Anatomy and parts — the scrim (modal), the edge-anchored surface, the
   drag handle/grabber (sheet), header/title + close, scrollable body,
   footer actions.
3. Properties / API — open/onOpenChange, placement (left/right/top/bottom,
   logical), modal (vs non-modal/persistent), size/width, dismissible
   (closeOnEscape/closeOnOutsideClick), snapPoints/detents + activeSnap,
   the drag/swipe enablement, role/aria.
4. States and variants — open/closed/animating; modal vs non-modal/
   persistent; navigation drawer vs utility/detail drawer vs bottom sheet;
   placement variants; the detent/snap states; temporary/dismissible/
   permanent.
5. Usage guidance — modal drawer (focused task, mobile nav) vs non-modal/
   persistent drawer (reference-while-working, desktop nav rail, filters)
   vs Dialog (centered, no edge relationship) vs Side Nav (persistent
   structure) vs Popover (small/anchored); the boundaries + the mobile
   transforms.
6. Accessibility — role=dialog+aria-modal (modal) vs complementary/
   navigation landmark (non-modal), the focus model (trap vs not),
   Escape/dismiss + focus-return, scroll-lock (modal), gesture
   accessibility (WCAG 2.5.1/2.5.7 — button alternative to swipe), WCAG SCs.
7. Content guidelines — title, body, the close affordance, footer actions,
   the drag-handle affordance.
8. Motion and transition — slide from the edge (inherits Dialog
   @starting-style/allow-discrete/overlay + a translate), the
   drag-tracking/spring for sheets, reduce-motion.
9. Internationalization — RTL (logical placement so left/right mirror),
   text expansion, the bottom-sheet (direction-neutral).
10. Naming — Drawer / Sheet / Side Panel / Panel; the practice's default;
    aliases; the Drawer-as-edge-anchored-Dialog relationship.
11. Implementation notes — modal drawer = Dialog at the edge (inherits
    showModal/top-layer/focus-trap/scroll-lock/animation), the non-modal
    push/squeeze layout (margin/translate of the page vs overlay), the
    bottom-sheet detents + drag physics (vaul) + the no-native-detents
    note, the gesture+button-alternative, headless (vaul/Radix/React Aria)
    vs opinionated.
12. Related and alternative components — typed relationships (Dialog as
    the modal substrate + the edge-vs-centered boundary, Side Navigation
    the persistent boundary, Popover the small-anchored boundary, the
    bottom-sheet = Dialog mobile transform, Button footer/close).
13. Field POV evolution — recent shifts (vaul/bottom-sheet detents, the
    modal-vs-non-modal clarity, the native <dialog> modal-drawer substrate,
    gesture-accessibility hardening).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a drawer is — explain the
modal-vs-non-modal (overlay-vs-push) decision, the edge-anchoring/logical-
placement model, the bottom-sheet detents/snap-points + drag-to-dismiss
(with the mandatory button alternative), the focus model (trap when modal,
not when persistent), the drawer-vs-dialog-vs-side-nav-vs-popover
boundaries, and the gesture-accessibility (WCAG 2.5.1/2.5.7) rules that
field leaders still diverge on.

You are researching the Dialog (Modal) component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a dialog /
modal is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Dialog is THE focus-trap overlay primitive — and the foundational Overlay
brief. It is the counterpart the catalogue has already pointed at from the
other side: the Menu brief (components/menu.md) established that a menu
uses roving tabindex and is NOT a focus trap — "that's Dialog." Dialog
owns the focus-trap contract. It STANDS ON one briefed substrate:
- THE FOOTER ACTIONS + CLOSE BUTTON inherit BUTTON
  (components/button.md) — the confirm/cancel/close controls are Buttons.
  Don't re-derive Button.
It FORWARD-REFERENCES two overlay siblings not yet briefed: Popover (the
NEXT brief — the light-dismiss, non-trapping overlay; draw the
dialog-vs-popover boundary clearly) and Drawer (the edge-anchored sheet —
draw the dialog-vs-drawer/sheet boundary).

THE DEFINING DIALOG-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE NATIVE <dialog> + showModal() PLATFORM-FIRST DECISION (the headline,
  like Accordion's native-<details>-first): the native <dialog> element
  with showModal() gives the top layer (no z-index wars), the ::backdrop
  pseudo-element, free Escape-to-close, automatic focus handling, and
  inertness of the background — vs. the legacy custom div+portal+manual
  focus-trap+aria-modal approach. Resolve the practice's default
  (native-first) and exactly what the native element still does NOT solve
  (initial-focus nuance, scroll-lock, light-dismiss/backdrop-click,
  animation, focus-return edge cases). Date the platform-state claims.
- THE FOCUS-TRAP CONTRACT (the defining mechanic): on open, focus MOVES
  INTO the dialog; Tab/Shift+Tab CYCLE within it (the background is inert);
  Escape closes; on close, focus RETURNS to the invoking element.
  Contrast explicitly with Menu (roving tabindex, Tab closes, NOT trapped)
  and with Popover (light-dismiss, focus NOT trapped). aria-modal="true"
  vs the inert attribute on the background for the custom path.
- INITIAL FOCUS PLACEMENT — where focus lands on open: the first
  focusable element / a specifically-designated element / the dialog
  container or heading; and the rule that it must NOT land on a
  destructive/confirm button. Plus focus RETURN to the invoker on close
  (and the invoker-was-removed edge case).
- role=dialog vs role=alertdialog — the alertdialog variant for
  confirmations and destructive/interrupting messages (focus, the
  assertive announcement, the constrained content).
- LIGHT-DISMISS / BACKDROP — click-outside-to-close and Escape-to-close,
  and WHEN TO DISABLE them (unsaved data / in-progress work → require an
  explicit choice, or confirm-on-dismiss). The scrim/backdrop and
  ::backdrop styling.
- SCROLL LOCKING — locking background scroll while open, and the
  scrollbar-width compensation (layout shift when the scrollbar
  disappears); scrolling WITHIN a tall dialog (sticky header/footer,
  scrollable body).
- MODAL vs NON-MODAL (modeless) — showModal() vs show(); when a
  non-modal dialog is appropriate vs a Popover.
- THE DIALOG vs DRAWER vs POPOVER vs SHEET boundaries — modal centered
  dialog vs edge-anchored drawer vs light-dismiss popover vs mobile
  bottom-sheet; the mobile full-screen / bottom-sheet transform.
- ANIMATION — entry/exit, the long-notorious exit-animation problem
  (animating to display:none), now addressed by @starting-style +
  transition-behavior: allow-discrete + animating the top-layer/::backdrop;
  reduce-motion. Date the platform-state.
- ANATOMY — header/title + close button, body (scrollable), footer action
  buttons, the backdrop; sizing (sm/md/lg/full); the dismissible-vs-
  required (no close affordance) variants.

Field-leader systems to survey (web): Radix UI (Dialog + AlertDialog —
the headless reference), Adobe Spectrum / React Aria (Dialog, Modal,
DialogTrigger), IBM Carbon (Modal, ComposedModal, the danger modal),
Shopify Polaris (Modal), GitHub Primer (Dialog), Atlassian Design System
(Modal Dialog), Microsoft Fluent (Dialog), Ariakit (Dialog), Base Web
(Uber) (Modal), Google Material 3 (Dialog — basic vs full-screen). The
native HTML <dialog> element + the platform features (top layer,
::backdrop, @starting-style, inert). WAI-ARIA APG Modal Dialog pattern +
Alert Dialog pattern. Mobile reference where relevant: Apple HIG (sheets /
alerts / action sheets), Material 3 (dialogs / bottom sheets). Cite each
with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Button footer/close controls;
flag unverified claims under notes.unverified — especially the platform-
state features).

1. Framing — what it is, what it isn't; the focus-trap definition; the
   native-<dialog>-first decision up front; why systems disagree.
2. Anatomy and parts — backdrop/scrim, the dialog surface, header/title +
   close button, scrollable body, footer action buttons.
3. Properties / API — open/defaultOpen + onOpenChange (controlled), the
   trigger composition, modal vs non-modal, size, dismissible
   (closeOnEscape / closeOnOutsideClick), initialFocus / finalFocus /
   restoreFocus, role=dialog|alertdialog, the title/description wiring.
4. States and variants — open/closed/animating; dialog vs alertdialog;
   modal vs non-modal; size (sm/md/lg/full-screen); dismissible vs
   required; mobile sheet.
5. Usage guidance — when a modal dialog is warranted (interrupting,
   focus-demanding) vs not (use inline / a non-modal / a popover / a
   drawer / a toast); the dialog-vs-drawer-vs-popover-vs-toast decision;
   the modal-overuse anti-pattern.
6. Accessibility — role=dialog/alertdialog, aria-modal, aria-labelledby +
   aria-describedby, the focus-trap + initial-focus + focus-return
   contract, Escape, the inert background, scroll-lock, the
   no-focus-on-destructive rule, WCAG SCs.
7. Content guidelines — title as a question/clear noun, body concision,
   button labels (action-specific not OK/Cancel), the destructive-confirm
   pattern, the close affordance.
8. Motion and transition — entry/exit (scale+fade from center, backdrop
   fade), the exit-animation problem (@starting-style / allow-discrete /
   top-layer), reduce-motion, the mobile sheet slide.
9. Internationalization — RTL (close button + footer button order flip),
   text expansion (title/body/buttons), the footer-button-order locale
   question.
10. Naming — Dialog / Modal / AlertDialog; the practice's default;
    aliases.
11. Implementation notes — native <dialog>+showModal() vs custom
    portal+inert+focus-trap, what native still doesn't solve (scroll-lock,
    light-dismiss, initial focus, animation), scroll-lock + scrollbar
    compensation, focus-trap + return, nested/stacked dialogs
    (discouraged), the top layer / z-index, headless (Radix/React Aria)
    vs opinionated.
12. Related and alternative components — typed relationships (Button
    footer/close, Popover [next] light-dismiss boundary, Drawer/Sheet edge
    boundary, Toast/Alert non-interrupting boundary, the alertdialog
    confirm pattern, Tooltip).
13. Field POV evolution — recent shifts (native <dialog> adoption, the top
    layer + ::backdrop, @starting-style exit animations, modal-overuse
    correction).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a modal is — explain the
native-<dialog>+showModal()-first decision (and what it still doesn't
solve), the focus-trap contract (and how it differs from Menu's roving
tabindex and Popover's light-dismiss), the initial-focus + focus-return
rules, the role=dialog-vs-alertdialog boundary, the when-to-disable-
light-dismiss (data-loss) decision, scroll-lock + scrollbar compensation,
and the exit-animation problem the platform has finally solved — the
things field leaders still diverge on.

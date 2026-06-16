You are researching the Toast component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a toast is,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Toast OPENS the Feedback category, and it is the non-interrupting
counterpart the Overlay arc kept pointing at (Dialog, Tooltip, and Drawer
all routed "non-interrupting feedback" here). It is the OPPOSITE of a
Dialog: transient, auto-dismissing, and it must announce WITHOUT stealing
focus. As the first Feedback brief it ESTABLISHES the ARIA live-region
announcement pattern that the rest of the category (Banner/Alert, Inline
Message, Progress) will reuse. It STANDS ON two briefed substrates:
- THE ACTION + CLOSE CONTROLS inherit BUTTON (components/button.md) — an
  optional action (e.g. Undo) and the dismiss control are Buttons. Don't
  re-derive Button.
- THE SEVERITY ICON inherits ICON (components/icon.md) — the info/success/
  warning/error glyph (decorative; color-not-sole-carrier). Don't
  re-derive Icon.
It FORWARD-REFERENCES the sibling Feedback components: Banner/Alert (the
PERSISTENT, in-flow message — not yet briefed; draw the toast-vs-banner
boundary), Inline Message (field/section-level — not yet briefed), and the
Dialog (the interrupting, focus-stealing boundary — see components/dialog.md).

THE DEFINING TOAST-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE NON-INTERRUPTING / TRANSIENT / NO-FOCUS-STEAL CONTRACT (the headline,
  the Dialog opposite): a toast appears at a screen edge/corner, conveys a
  brief confirmation or status, auto-dismisses after a timeout, and must
  NOT move focus or block the page. Resolve the contract and the contrast
  with Dialog (modal, focus-trapped) and Banner (persistent, in-flow).
- THE ARIA LIVE-REGION ANNOUNCEMENT (the accessibility crux, and the
  category-defining pattern): the toast must be announced to assistive
  technology WITHOUT moving focus, via a live region — role=status /
  aria-live=polite for informational/success, role=alert / aria-live=
  assertive for errors/critical. Resolve the polite-vs-assertive decision
  and the critical implementation trap that the live region container must
  ALREADY EXIST in the DOM before the toast text is injected (AT won't
  announce content added simultaneously with the region). The single
  shared live region / toast viewport.
- AUTO-DISMISS TIMING vs WCAG (the central tension): auto-dismiss collides
  with WCAG 2.2.1 (Timing Adjustable). Resolve the "enough time to read"
  problem — recommended minimum durations (and that they should scale with
  content length / reading speed), PAUSE-ON-HOVER and pause-on-focus, the
  no-auto-dismiss-while-hovered/focused rule, and the hard rule that an
  ACTIONABLE or ERROR toast should not auto-dismiss (or needs a much longer
  / infinite timeout).
- THE ACTION-IN-TOAST PROBLEM (the hardest case — e.g. "Undo"): a toast
  with an interactive control sits on a transient, non-focus-stealing
  surface, so reaching the action by keyboard is hard (focus isn't moved
  there) and auto-dismiss races the user. Resolve: actionable toasts should
  not auto-dismiss (or pause generously), the keyboard route to the toast
  region (a hotkey / F6-style jump — Radix uses an F8 hotkey; React Aria
  uses a focusable landmark), and WHEN an action belongs in a persistent
  Banner/Inline message instead of a toast.
- THE QUEUE / STACKING / LIMIT (the toaster): multiple toasts — stack vs
  queue, a max-visible limit (collapse the rest), the order
  (newest-on-top/bottom), the single toaster/viewport that owns the queue
  and the live region. Sonner's stacked/expand-on-hover model.
- PLACEMENT — the corner/edge regions (top-right, bottom-center, etc.),
  one region per app, the safe-area/responsive placement, the
  bottom-center mobile (snackbar) convention.
- SEVERITY / VARIANTS — info / success / warning / error; the
  color-not-sole-carrier rule (icon + text, not colour alone); and the
  POV (e.g. Polaris) that toasts should NOT carry errors (errors are
  persistent/inline) — resolve whether error toasts are legitimate.
- SWIPE-TO-DISMISS + THE BUTTON ALTERNATIVE — swipe to dismiss on
  touch/pointer must have a non-gesture alternative (the close button;
  WCAG 2.5.1/2.5.7, inherited from the Drawer gesture rule).

Field-leader systems to survey (web): Sonner (Emil Kowalski — the de facto
React toast; stacked/expand-on-hover, promise toasts), Radix UI (Toast —
the headless reference; swipe, the hotkey-to-region, the duration/pause
model), Adobe Spectrum / React Aria (Toast / ToastRegion — the focusable
landmark approach), Google Material 3 (Snackbar — bottom, single, one
action), IBM Carbon (Notification — toast / inline / actionable), Shopify
Polaris (Toast — minimal, bottom-center, the no-error-toasts POV), GitHub
Primer (Toast / the inline Flash boundary), Atlassian (Flag — the toast
equivalent), Microsoft Fluent (Toast / MessageBar), Base Web (Uber)
(Toast / Snackbar), Ant Design (message / notification). WAI-ARIA APG (no
formal "toast" pattern — the Alert pattern + live regions; the ongoing
toast-pattern discussions). Mobile reference where relevant: Apple HIG,
Material 3 (Snackbar). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Button action/close controls and
the Icon severity glyph; flag unverified claims under notes.unverified).

1. Framing — what it is (a non-interrupting transient notification) and
   what it isn't (a Dialog / a persistent Banner / an Inline Message); the
   non-interrupting + live-region + auto-dismiss realities up front; why
   systems disagree.
2. Anatomy and parts — the toast viewport/region (the live region), the
   toast surface, the severity icon, the title/message, the optional
   action button, the dismiss/close button, the progress/timeout indicator.
3. Properties / API — the imperative toast() API (Sonner-style) vs the
   declarative provider; severity/variant, duration (+ Infinity for
   persistent), action, dismissible/onDismiss, position, the promise toast,
   the queue/limit.
4. States and variants — entering/showing/paused/exiting; info/success/
   warning/error; with-action / with-close / with-progress; the snackbar
   (single, bottom) vs the stacked corner toaster; loading/promise.
5. Usage guidance — toast (brief, non-critical, transient confirmation)
   vs Banner/Alert (persistent, in-flow, important) vs Inline Message
   (field/section) vs Dialog (must-act, blocking); the never-essential /
   actionable-shouldn't-auto-dismiss rules; the boundaries.
6. Accessibility — the live region (role=status/polite vs role=alert/
   assertive), the pre-existing-region trap, no-focus-steal, the
   auto-dismiss-vs-WCAG-2.2.1 timing + pause-on-hover/focus, the
   action-in-toast keyboard route (hotkey/landmark), swipe + button
   alternative, color-not-sole-carrier, WCAG SCs.
7. Content guidelines — concise message, the action label, no errors-as-
   toast (POV), title vs message, the dismiss affordance.
8. Motion and transition — slide/fade in from the edge, the stack reflow /
   expand-on-hover, swipe, the timeout/progress, reduce-motion.
9. Internationalization — RTL (corner placement + slide direction flip),
   text expansion (toasts are short but expand → wrap, and reading-time/
   duration scaling), the action-label.
10. Naming — Toast / Snackbar / Notification / Flag / Flash; the practice's
    default; aliases.
11. Implementation notes — the single toaster/viewport owning the queue +
    the pre-existing live region, the imperative toast() store, duration +
    pause-on-hover + actionable-no-auto-dismiss, the hotkey/landmark to
    reach the region, swipe + button, headless (Sonner/Radix/React Aria)
    vs opinionated.
12. Related and alternative components — typed relationships (Button
    action/close, Icon severity, Banner/Alert persistent boundary, Inline
    Message boundary, Dialog interrupting boundary, the Notification
    Center, Progress for loading toasts).
13. Field POV evolution — recent shifts (Sonner's stacked model, the
    live-region + pre-existing-region hardening, the actionable-toast /
    auto-dismiss-WCAG correction, no-error-toasts).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a toast is — explain the
non-interrupting + no-focus-steal contract, the live-region announcement
(role=status/polite vs role=alert/assertive + the pre-existing-region
trap), the auto-dismiss-vs-WCAG-2.2.1 timing tension (pause-on-hover,
minimums, actionable-shouldn't-auto-dismiss), the action-in-toast keyboard-
reachability problem (the hotkey/landmark route), the queue/stacking/limit
model, and the toast-vs-banner-vs-inline-vs-dialog boundaries that field
leaders still diverge on.

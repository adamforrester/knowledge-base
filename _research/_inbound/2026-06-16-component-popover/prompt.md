You are researching the Popover component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a popover
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Popover is the THIRD Overlay pole, and the PIVOTAL one: it owns
light-dismiss + anchoring (non-trapping), and it is where the POSITIONING
SUBSTRATE that Select, Combobox, and Menu have all referenced finally gets
formalised. This brief closes that deferred loop. It STANDS ON two briefed
substrates:
- THE TRIGGER inherits BUTTON (components/button.md) — the popover trigger
  is a Button with aria-expanded + an accessible relationship to the
  popover. Don't re-derive Button.
- THE TOP LAYER + EXIT-ANIMATION SUBSTRATE inherits DIALOG
  (components/dialog.md): the top layer (no z-index), and the
  @starting-style + transition-behavior: allow-discrete + overlay
  exit-animation solution. Don't re-derive these — reference them as the
  shared overlay substrate and concentrate on what is Popover-specific.
And it is itself THE substrate the catalogue has been forward-referencing:
Menu, the Select listbox, the Combobox listbox, and Tooltip all sit on
Popover's anchored-surface + positioning machinery. Make that explicit —
Popover is the GENERIC anchored transient surface; Menu/Select/Combobox/
Tooltip are specialisations with specific roles.

THE DEFINING POPOVER-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE NATIVE POPOVER API (the platform-first decision, paired with Dialog's
  native-<dialog>): the popover attribute + popovertarget + showPopover()/
  hidePopover()/togglePopover(). Resolve popover="auto" (light-dismiss +
  Escape + one-open-per-ancestor auto-close) vs popover="manual" (no
  light-dismiss, no auto-close) vs popover="hint" (the newer hover/hint
  layer). The top layer (shared with Dialog). Date the platform-state.
- CSS ANCHOR POSITIONING (the formalisation of the positioning substrate —
  the headline): anchor-name / position-anchor, the anchor() function,
  position-area, position-try / position-try-fallbacks / @position-try
  (the declarative flip/shift), anchor-size. Resolve how this REPLACES the
  JS positioning incumbent (Floating UI / Popper) that Select/Combobox/Menu
  leaned on, what it still doesn't cover, and the practice's default
  (CSS-anchor-first, Floating-UI fallback). Date the platform-state and
  note the verification path — this is the most volatile platform claim in
  the catalogue.
- THE POSITIONING MODEL itself (the machinery the whole overlay family
  inherits): placement (top/bottom/left/right + start/center/end), offset,
  the collision-aware flip + shift, the arrow/caret, the anchor element,
  same-width-as-trigger. This is the substrate — resolve it once, here.
- LIGHT-DISMISS + NON-TRAPPING (the defining behavioural contract, the
  contrast with Dialog): popover="auto" gives click-outside + Escape
  dismissal for free; the popover is NOT focus-trapped and (for a generic
  popover) focus does NOT auto-move in. Resolve the focus model: when
  focus SHOULD move in (an interactive popover / a form — a non-modal
  dialog) vs NOT (a hint/info popover); the focus-return-to-trigger rule;
  Tab moving out of the popover (not trapped).
- THE NATIVE-POPOVER ACCESSIBILITY GAP (a critical, non-obvious point):
  the native Popover API does NOT establish an accessible relationship
  between the trigger and the popover — popovertarget wires behaviour, not
  semantics. Resolve what you must add (aria-expanded on the trigger, and
  aria-details / aria-controls / role on the popover) and that role
  depends on CONTENT.
- ROLE-BY-CONTENT — a popover has no implicit ARIA role; the role comes
  from its content: role=dialog (interactive/non-modal dialog),
  listbox (Select/Combobox), menu (Menu), tooltip (Tooltip). Resolve the
  generic-popover default and the non-modal-dialog overlap with Dialog.
- THE POPOVER vs TOOLTIP vs MENU vs DIALOG vs DRAWER boundaries — generic
  anchored container vs hover/focus description (Tooltip, role=tooltip,
  WCAG 1.4.13, no interactive content) vs command list (Menu, role=menu) vs
  modal trap (Dialog) vs edge sheet (Drawer). The popover-vs-tooltip line
  (interactive content + click vs description + hover) is the sharpest.
- THE ARROW / CARET — positioning the arrow (CSS anchor positioning vs the
  legacy pseudo-element/JS approach); when to use an arrow vs not.

Field-leader systems to survey (web): the native Popover API + CSS Anchor
Positioning (the platform — the headline), Floating UI / Popper (the JS
incumbent being displaced), Radix UI (Popover), Adobe Spectrum / React
Aria (Popover, the positioning hooks), GitHub Primer (Overlay /
AnchoredOverlay), IBM Carbon (Popover), Shopify Polaris (Popover),
Atlassian Design System (Popup), Microsoft Fluent (Popover / Positioning
shorthand), Ariakit (Popover), Base Web (Uber) (Popover), Google Material
3 (menus / rich tooltips). WAI-ARIA APG (there is no generic "popover"
pattern — it is the Tooltip / Dialog (non-modal) / Disclosure / Menu
patterns by content). Mobile reference where relevant: Apple HIG (popovers
/ popups), Material 3. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Button trigger and the Dialog
top-layer/animation substrate; flag unverified claims under
notes.unverified — especially the CSS Anchor Positioning / Popover API
platform-state, the most volatile claim in the catalogue).

1. Framing — what it is (the generic anchored transient surface) and what
   it isn't; Popover as the substrate Menu/Select/Combobox/Tooltip sit on;
   the native-Popover-API + CSS-anchor-positioning decision up front; why
   systems disagree.
2. Anatomy and parts — trigger (anchor), the popover surface, the arrow/
   caret, the (content-dependent) header/body, the close affordance.
3. Properties / API — open/defaultOpen + onOpenChange, the trigger/anchor
   composition (asChild), placement/offset/align, collision (flip/shift),
   the arrow, light-dismiss (closeOnEscape/closeOnInteractOutside),
   role/aria wiring, focus management (initialFocus / non-trapping).
4. States and variants — open/closed/animating; hover vs click trigger;
   with-arrow / without; generic vs role-typed (info/dialog/listbox/menu/
   tooltip); same-width-as-trigger.
5. Usage guidance — Popover (generic anchored surface) vs Tooltip
   (description) vs Menu (commands) vs Dialog (modal) vs Drawer (sheet);
   when to move focus in (interactive) vs not; the boundaries.
6. Accessibility — the native-popover accessibility GAP (no automatic
   trigger↔popover relationship; add aria-expanded + aria-details/controls
   + role), role-by-content, light-dismiss + Escape, the non-trapping
   focus model + when to move focus in + focus-return, WCAG 1.4.13 for
   hover popovers, WCAG SCs.
7. Content guidelines — concise anchored content, the close affordance,
   the trigger relationship, when an arrow helps.
8. Motion and transition — origin-aware open/close (inherits Dialog's
   @starting-style/allow-discrete/overlay), the arrow, reduce-motion.
9. Internationalization — RTL (placement + arrow + alignment flip), the
   logical-property positioning, text expansion.
10. Naming — Popover / Popup / Overlay / AnchoredOverlay; the practice's
    default; aliases; the Popover-as-base relationship to Menu/Tooltip.
11. Implementation notes — native Popover API + CSS Anchor Positioning vs
    Floating UI fallback, what CSS anchor positioning doesn't yet cover,
    the trigger↔popover accessible wiring, the focus model, the arrow,
    nested popovers + the light-dismiss stack, headless (Radix/React Aria)
    vs opinionated, and the formalisation note (this is the substrate
    Select/Combobox/Menu inherit).
12. Related and alternative components — typed relationships (Button
    trigger, Dialog top-layer/animation substrate + the non-modal-dialog
    overlap, Tooltip/Menu/Select/Combobox as specialisations sitting on
    Popover, Drawer boundary).
13. Field POV evolution — recent shifts (the native Popover API, CSS
    Anchor Positioning displacing Floating UI, the top layer, role-by-
    content discipline).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a popover is — explain the
native-Popover-API (auto/manual/hint) + CSS-anchor-positioning decision
(and what anchor positioning still doesn't cover), the positioning model
the whole overlay family inherits, the light-dismiss + non-trapping focus
contract (vs Dialog's trap), the native-popover accessibility gap (no
automatic trigger↔popover relationship), role-by-content, and the
popover-vs-tooltip-vs-menu-vs-dialog boundaries that field leaders still
diverge on.

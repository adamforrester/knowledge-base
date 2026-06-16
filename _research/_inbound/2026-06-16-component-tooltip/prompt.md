You are researching the Tooltip component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a tooltip
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Tooltip is the CLEANEST close to the Overlay arc: it is a SPECIALISATION
of Popover. It STANDS ON one briefed substrate:
- THE ANCHORED SURFACE + POSITIONING + TOP LAYER inherit POPOVER
  (components/popover.md): a tooltip is a Popover whose content is
  role=tooltip — specifically the popover="hint" layer Popover established
  (the hint layer that does NOT close an open auto popover). It inherits
  the positioning model (placement/offset/flip/shift/arrow, CSS Anchor
  Positioning), the top layer, and origin-aware motion. Don't re-derive
  the positioning substrate — reference it as inherited and concentrate on
  what is Tooltip-specific.
The trigger is whatever FOCUSABLE interactive element the tooltip
describes (often a Button or an icon-only Button — see components/button.md).

THE DEFINING TOOLTIP-SPECIFIC SUBSTANCE to resolve and go deep on:
- WCAG 1.4.13 (Content on Hover or Focus) — THE defining tooltip rule:
  content shown on hover/focus must be DISMISSABLE (Escape without moving
  the pointer), HOVERABLE (the pointer can move onto the tooltip without
  it vanishing), and PERSISTENT (stays until hover/focus leaves or it's
  dismissed). Resolve exactly what each requires and the implementation
  obligations.
- THE HOVER-AND-FOCUS TRIGGER + THE TOUCH PROBLEM — a tooltip must appear
  on BOTH hover AND keyboard focus (focus-only-on-hover strands keyboard
  users). And the hard truth: touch devices have NO hover — resolve the
  touch story (long-press, or no tooltip, or a tap-toggletip) and the rule
  that a tooltip must NEVER carry essential information (it is transient
  and touch-inaccessible).
- role=tooltip + THE DESCRIPTION RELATIONSHIP — the tooltip is wired to
  its trigger via aria-describedby (it SUPPLEMENTS), vs aria-labelledby
  (it IS the name — the icon-only-button case). Resolve the
  describedby-default rule, and the trigger-MUST-BE-FOCUSABLE requirement
  (a tooltip on a non-focusable element is keyboard-unreachable).
- PLAIN TEXT ONLY / NO INTERACTIVE CONTENT (the Popover boundary, the
  sharpest line, paired from Popover's side): a tooltip holds a short
  text description and NO interactive content (no links/buttons) and is
  not itself focusable; the moment it needs interactivity it is a Popover
  (a "rich tooltip" is a Popover). Material 3's plain-vs-rich tooltip
  split.
- THE ICON-BUTTON TOOLTIP-AS-LABEL PATTERN + THE DISABLED-CONTROL TRAP —
  an icon-only Button whose tooltip is effectively its label (resolve
  aria-label-on-the-button vs tooltip-as-labelledby), and the recurring
  trap that a tooltip on a DISABLED control is unreachable (disabled
  elements aren't focusable / don't fire pointer events) — the wrap /
  aria-disabled workaround.
- TOOLTIP vs TOGGLETIP (the sharp, often-missed distinction): a TOOLTIP
  is hover/focus-triggered and DESCRIBES its trigger (aria-describedby,
  role=tooltip); a TOGGLETIP is CLICK/tap-triggered, discloses
  supplementary info, is typically announced via a live region
  (role=status), and works on touch. Resolve when each applies (the
  toggletip is the accessible answer to "tooltip on touch / tooltip with
  more than a word").
- THE title ATTRIBUTE ANTI-PATTERN — why the native title attribute is
  not an accessible tooltip (no touch, no keyboard reliability, no
  styling, inconsistent timing, screen-reader-inconsistent) and the
  design-system tooltip exists to replace it.
- DELAY / TIMING — open delay (avoid flicker on pointer transit), close
  delay, and the "warm-up / cool-down" global tooltip timer (once one
  tooltip has shown, sibling tooltips show instantly).

Field-leader systems to survey (web): Radix UI (Tooltip + TooltipProvider
delayDuration/skipDelayDuration), Adobe Spectrum / React Aria (Tooltip,
TooltipTrigger), Google Material 3 (plain vs rich tooltips), IBM Carbon
(Tooltip, icon/definition tooltip, the Toggletip distinction), Shopify
Polaris (Tooltip), GitHub Primer (Tooltip / the tooltip-v2 a11y rebuild),
Atlassian Design System (Tooltip), Microsoft Fluent (Tooltip), Ariakit
(Tooltip), Base Web (Uber) (StatefulTooltip). The native title attribute
(the anti-pattern). WAI-ARIA APG Tooltip pattern. Mobile reference where
relevant: Apple HIG, Material 3 (and the touch/no-hover reality). Cite
each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Popover anchored-surface/
positioning substrate; flag unverified claims under notes.unverified).

1. Framing — what it is (a hint Popover, role=tooltip) and what it isn't
   (a Popover / a Toggletip / a label / the title attribute); the
   WCAG-1.4.13 + touch realities up front; why systems disagree.
2. Anatomy and parts — the focusable trigger, the tooltip surface
   (role=tooltip), the arrow, the (plain-text) content.
3. Properties / API — the trigger composition, open/defaultOpen +
   controlled, placement/offset (inherited Popover), delay (open/close,
   provider-level skipDelay), describedby vs labelledby wiring, plain
   text constraint.
4. States and variants — hidden/showing; the trigger states it rides on;
   plain tooltip vs (rich tooltip = Popover, out of scope) vs toggletip;
   with-arrow; the icon-button-label variant.
5. Usage guidance — when a tooltip (supplementary hover/focus hint, never
   essential) vs a toggletip (click, supplementary, touch-OK) vs visible
   help text / a label / a Popover; the never-essential-info rule; the
   don't-tooltip-everything discipline.
6. Accessibility — WCAG 1.4.13 (dismissable/hoverable/persistent),
   role=tooltip, aria-describedby (default) vs aria-labelledby, the
   trigger-must-be-focusable rule, the disabled-control trap, hover+focus
   parity, the title-attribute anti-pattern, the touch story, WCAG SCs.
7. Content guidelines — short supplementary text, no interactivity, the
   icon-button label, sentence case / no period, never essential info.
8. Motion and transition — minimal fade/scale (inherits Popover
   origin-aware), the delay, reduce-motion.
9. Internationalization — RTL (placement + arrow flip, inherited),
   text expansion (tooltips are short but expand), no truncation.
10. Naming — Tooltip / Toggletip; the practice's default; aliases; the
    Tooltip-as-Popover-specialisation relationship.
11. Implementation notes — inherits Popover positioning + top layer +
    popover="hint"; the hover+focus+touch event model and the
    warm-up/cool-down timer; aria-describedby wiring; the
    disabled-control wrap; never the title attribute; headless
    (Radix/React Aria) vs opinionated.
12. Related and alternative components — typed relationships (Popover as
    the substrate + the rich-tooltip boundary, Button/icon-button trigger,
    Toggletip, visible help text / Label, the title attribute it replaces).
13. Field POV evolution — recent shifts (the title-attribute death, WCAG
    1.4.13 hardening, the toggletip-for-touch pattern, popover="hint",
    the icon-button-label clarification).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a tooltip is — explain the
WCAG-1.4.13 (dismissable/hoverable/persistent) contract, the
hover-AND-focus trigger + the touch/no-hover reality (and the
never-essential-info rule), role=tooltip + aria-describedby-vs-labelledby
+ the trigger-must-be-focusable / disabled-control trap, the plain-text /
no-interactive-content boundary with Popover, and the tooltip-vs-toggletip
distinction that field leaders and a11y practice now enforce.

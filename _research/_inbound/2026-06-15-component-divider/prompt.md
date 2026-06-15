You are researching the Divider component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is a foundational primitive; the field largely converges, so this
is a claude-only run. The 15-section spine still ships, but per the
component-prompt-template deviation rule, sections that have little to
say for a primitive (states/variants, motion) collapse to a paragraph.

Concentrate the brief on the genuinely contested points:
- presentational vs. semantic separator — when a divider should carry
  role="separator" and when it must be aria-hidden / purely decorative,
  and the orientation attribute that goes with the role
- horizontal vs. vertical, and the height-inheritance trap for vertical
  dividers in flex/grid
- inset / middle-inset / full-bleed variants and where the inset is
  measured from
- the divider-vs-spacing decision (when whitespace is the better
  separator and a line is visual noise)
- the divider-with-content / labelled-divider pattern ("OR" in the
  middle of a rule)
- the <hr> element vs. a styled div, and the token model (a divider is
  often the thinnest test of a border/hairline token)

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum,
Google Material 3, IBM Carbon, GitHub Primer, Atlassian Design System,
Base Web. Mobile reference where relevant: Apple HIG, Material 3.

Cite each system with a version date. Follow the 15-section spine
(framing, anatomy, properties/API, states and variants, usage guidance,
accessibility, content guidelines, motion, internationalization, naming,
implementation notes, related and alternative components, field POV
evolution, sources cited, agent-consumable schema). The reader is an
expert; do not explain that a divider is a line. Explain the
separator-role decision, the vertical-divider sizing trap, and the
divider-vs-spacing judgment.

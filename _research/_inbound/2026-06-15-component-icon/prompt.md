You are researching the Icon component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is a foundational primitive, run claude-only. The 15-section spine
still ships; sections with little to say for a primitive may collapse to
a paragraph.

Concentrate the brief on the genuinely contested points:
- semantic vs. decorative — the accessible-name vs. aria-hidden
  decision, and why a decorative icon next to a text label must be
  hidden from AT (the redundant-announcement problem)
- the icon-only-button anti-pattern — an Icon is not a button; the
  accessible name and hit target belong to the wrapping control, not
  the glyph
- the sizing model — fixed px grid (16/20/24) vs. em-relative sizing,
  optical alignment with adjacent text, and the optical-sizing /
  variable-icon-font trend
- color — currentColor inheritance vs. explicit tone props, and the
  two-tone / duotone / variable-fill direction
- delivery — inline SVG vs. SVG sprite vs. icon font, the tree-shaking
  and caching trade-offs, and why icon fonts are now an anti-pattern
- the title/aria-label vs. role=img vs. aria-hidden matrix, and how a
  standalone meaningful icon gets an accessible name
- naming and taxonomy — the icon set as a named, versioned vocabulary,
  aliasing, and the deprecation/rename problem when a glyph changes

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum,
Google Material (Material Symbols), IBM Carbon, GitHub Primer (Octicons),
Atlassian Design System, Base Web. Mobile reference where relevant:
Apple HIG (SF Symbols), Material 3.

Cite each system with a version date. Follow the 15-section spine
(framing, anatomy, properties/API, states and variants, usage guidance,
accessibility, content guidelines, motion, internationalization, naming,
implementation notes, related and alternative components, field POV
evolution, sources cited, agent-consumable schema). The reader is an
expert; do not explain that an icon is a small picture. Explain the
semantic-vs-decorative decision, the icon-only-button trap, the sizing
and currentColor model, and the delivery trade-offs that field leaders
still disagree on.

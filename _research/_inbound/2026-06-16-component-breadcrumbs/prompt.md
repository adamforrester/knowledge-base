You are researching the Breadcrumbs component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what
breadcrumbs are, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Breadcrumbs is a Navigation-category brief that BUILDS ON the already-
briefed LINK component (components/link.md). A breadcrumb trail is a set
of Links (each crumb navigates to an ancestor URL) with the current page
marked aria-current. Do NOT re-derive Link's substance (the <a href>
contract, the underline discipline, the framework-router asChild
polymorphism, link-vs-button) — reference it as inherited and concentrate
on what is Breadcrumbs-specific.

THE DEFINING BREADCRUMBS-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE STRUCTURE + LANDMARK CONTRACT — a <nav aria-label="Breadcrumb">
  wrapping an ordered list (<ol>/<li>) of crumb Links. Resolve the
  ordered-list semantics, the nav-landmark labelling, and why this is the
  APG breadcrumb pattern.
- THE CURRENT / LAST CRUMB — is the final (current-page) crumb a Link
  with aria-current="page", or non-interactive static text? Resolve the
  practice's default and the aria-current value (page vs location).
- SEPARATORS — the "/" or ">" or chevron between crumbs must be
  DECORATIVE (aria-hidden / CSS ::before pseudo-element), never read as
  content or as a list item; the slash-vs-chevron choice; RTL flip.
- TRUNCATION / OVERFLOW — long or deep trails: collapse the MIDDLE crumbs
  into an ellipsis/"…" overflow menu (revealing the hidden ancestors),
  keep first (home/root) + last (current) + sometimes parent; vs.
  per-label truncation; the mobile pattern (show only the parent /
  "back-one-level"). Resolve the practice's overflow model.
- THE HOME/ROOT CRUMB — icon-only home vs. a "Home" text crumb and its
  accessible name.
- SEO / STRUCTURED DATA — the schema.org BreadcrumbList (JSON-LD)
  structured data for search rich-results; whether the design system
  emits it or leaves it to the consumer.
- the breadcrumb-vs-back-button, breadcrumb-vs-tabs, and
  breadcrumb-vs-stepper boundaries; breadcrumbs as a SECONDARY wayfinding
  aid (never the primary nav).

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum
(React Aria Breadcrumbs), Google Material 3, IBM Carbon, GitHub Primer,
Atlassian Design System, Base Web (Uber). Mobile reference where relevant:
Apple HIG, Material 3. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for Link where the crumb is a Link;
flag unverified claims under notes.unverified).

1. Framing — what it is, what it isn't, why systems disagree.
2. Anatomy and parts — nav landmark, ordered list, crumb (Link),
   separator, overflow/collapse affordance, current marker.
3. Properties / API — items/children, separator, maxItems/itemsBefore
   /itemsAfterCollapse (overflow), the current-crumb handling, router
   integration (inherits Link).
4. States and variants — crumb states (inherit Link: rest/hover/focus/
   current); collapsed/overflow; with-home-icon; condensed/mobile.
5. Usage guidance — when to use (deep hierarchy) vs. not (flat sites,
   primary nav, linear flows); the boundaries.
6. Accessibility — nav[aria-label] + ol/li, aria-current on the current
   crumb, decorative separators (aria-hidden), the overflow-menu a11y,
   the WCAG SC it participates in.
7. Content guidelines — concise crumb labels matching page titles,
   truncation + tooltip, the home label.
8. Motion and transition — minimal (overflow menu open); reduce-motion.
9. Internationalization — RTL (separator glyph + order flip), text
   expansion, truncation.
10. Naming — Breadcrumbs / Breadcrumb / BreadcrumbItem; the practice's
    default; aliases.
11. Implementation notes — decorative separators via CSS not DOM, the
    overflow-collapse logic, router integration (inherits Link asChild),
    optional JSON-LD structured-data emission, headless-vs-opinionated.
12. Related and alternative components — typed relationships (Link, the
    nav landmark, Tabs, Stepper, Menu for the overflow, back button).
13. Field POV evolution — recent shifts.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what breadcrumbs are — explain the
nav/ol/li + aria-current contract, the current-crumb (link vs text)
decision, the decorative-separator rule, the truncation/overflow collapse
model, and the SEO structured-data question that field leaders still
diverge on.

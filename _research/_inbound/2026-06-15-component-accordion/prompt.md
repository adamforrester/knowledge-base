You are researching the Accordion component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what an
accordion is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Accordion is a Navigation/disclosure brief, the vertical cousin of TABS
(components/tabs.md). Resolve that boundary crisply rather than re-derive
it: Tabs show ONE panel at a time in a HORIZONTAL row and use the
tablist/tab/tabpanel + roving-tabindex pattern; an Accordion is a
VERTICAL stack of expand/collapse sections that can often show MANY (or
zero) at once and uses a fundamentally different ARIA pattern (heading +
button[aria-expanded] + region — NOT tablist). State the accordion-vs-tabs
boundary up front, then spend the brief on accordion-specific substance.

THE DEFINING ACCORDION-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE DISCLOSURE-PRIMITIVE DECOMPOSITION — a single expand/collapse
  section is a "Disclosure"; an Accordion is a SET of disclosures with
  optional cross-coordination. Is Disclosure a separate exposed primitive
  the Accordion composes from (paralleling the practice's
  atomic-vs-group decompositions in checkbox/segmented-control)? Resolve
  how many components ship and where the boundary sits.
- SINGLE-OPEN vs. MULTI-OPEN — exclusive (one section open at a time,
  opening one closes the others) vs. independent (any number open). Plus
  the "allow all closed" vs. "always keep one open" sub-decision. Resolve
  the practice's default and how the API expresses it.
- THE ARIA PATTERN — each header is a native <button> with aria-expanded
  and aria-controls, WRAPPED IN A HEADING (h2/h3...) of the correct
  document-outline level; the button controls a region (role=region +
  aria-labelledby, or the panel). This is NOT tablist/tab/tabpanel.
  Resolve the heading-level contract (don't break the outline) and the
  keyboard model (Enter/Space toggle; each header is its OWN tab stop —
  the key difference from tabs' roving tabindex; the APG-optional
  Up/Down/Home/End arrow navigation between headers).
- NATIVE <details>/<summary> vs. CUSTOM ARIA — when to use the native
  element; the new platform features (the `name` attribute for exclusive
  single-open accordions; ::details-content; interpolate-size:
  allow-keywords + calc-size(auto) for animating to content height).
  Resolve the native-vs-custom decision (parallel to the select brief).
- THE HEIGHT-ANIMATION PROBLEM — animating from 0 to auto/content height:
  grid-template-rows 0fr->1fr, calc-size/interpolate-size, the max-height
  hack, or JS measurement; the reduce-motion contract; the chevron
  rotation.
- expand-all / collapse-all controls; nested accordions (discouraged);
  scroll-into-view on expand; deep-linking a section open via URL.

Field-leader systems to survey (web): Shopify Polaris, Adobe Spectrum
(React Aria Disclosure/Accordion), Google Material 3, IBM Carbon, GitHub
Primer, Atlassian Design System, Base Web (Uber). Mobile reference where
relevant: Apple HIG, Material 3 (Compose). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; flag unverified claims under notes.unverified).
Represent the Disclosure/Accordion decomposition and the
single-vs-multi-open model explicitly.

1. Framing — what it is, what it isn't, why systems disagree.
2. Anatomy and parts — the disclosure/accordion decomposition; header,
   trigger button, heading wrapper, region/panel, indicator.
3. Properties / API — single vs. multi (allowMultiple / selectionMode),
   expandedKeys/defaultExpandedKeys, allow-all-closed, the composition.
4. States and variants — collapsed / expanded / focus-visible / hover /
   disabled section; flush vs. contained/boxed, with-icon, nested.
5. Usage guidance — when to use, when not to use, what to use instead
   (the accordion-vs-tabs and accordion-vs-disclosure and
   accordion-vs-tree decisions; the mobile tabs->accordion transform).
6. Accessibility — the heading+button[aria-expanded]+region contract,
   heading-level outline, each-header-its-own-tab-stop (vs tabs' roving),
   the APG arrow-key option, the WCAG SC it participates in.
7. Content guidelines — header labels, the whole-header hit target.
8. Motion and transition — the height-expand animation problem, chevron
   rotation, reduce-motion.
9. Internationalization — RTL (chevron side + direction), text
   expansion of headers.
10. Naming — Accordion / AccordionItem / Disclosure; the practice's
   default; aliases.
11. Implementation notes — native <details> vs custom, the height
   animation, controlled expandedKeys, scroll-into-view, deep-linking,
   headless-vs-opinionated.
12. Related and alternative components — typed relationships incl. Tabs,
   Disclosure, Tree, Card/Section.
13. Field POV evolution — recent shifts (the CSS calc-size/interpolate-size
   and <details name> platform features).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what an accordion is — explain the
disclosure decomposition, the single-vs-multi-open model, the
heading+button+region ARIA (and why it's not a tablist), the
native-<details>-vs-custom decision, and the height-animation problem
that field leaders still disagree on.

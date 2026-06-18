You are researching the Section component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Section /
sectioning element is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the choices field
leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Section is THE SEMANTIC REGION — the fifth and FINAL Layout brief, the one
that CLOSES the Layout category, and the SEMANTIC counterpart to Card's
VISUAL surface (Card is a styled chrome surface; Section is a meaning-
bearing document region — a landmark + a heading-level contract, often with
no chrome at all). It STANDS ON the layout primitives and draws a boundary
with Card:
- IT STANDS ON BOX (components/box.md): it inherits the polymorphic
  as/asChild Slot (rendering <section>/<article>/<aside>/<nav>), the
  spacing-token scale, the zero-runtime delivery, and the logical-property
  RTL. The visual/full-bleed-band form lightly uses Box's surface tokens.
  Don't re-derive Box — name it and record the delta (the semantics + the
  heading-level contract + the constrained-width concern).
- IT COMPOSES STACK + HOSTS GRID/CARD (components/stack.md, grid.md,
  card.md): a Section's content is typically a Stack (a section header +
  body) and/or a Grid of Cards. Reference them; don't re-derive.
- IT IS THE SEMANTIC COUNTERPART TO CARD (components/card.md, which already
  drew the boundary from its side): Card = a visually-bounded in-flow OBJECT
  with chrome; Section = a SEMANTIC document REGION (a landmark spanning the
  layout, usually no chrome). Resolve the boundary from Section's side.

THE DEFINING SECTION-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE NAMELESS-SECTION / LANDMARK CONTRACT (the headline + the accessibility
  crux): the HTML <section> element is ONLY a landmark (role="region",
  navigable by AT landmark navigation) WHEN IT HAS AN ACCESSIBLE NAME
  (aria-labelledby pointing at its heading, or aria-label). A NAMELESS
  <section> is a generic container with NO landmark value — the single most
  common Section misuse (wrapping everything in <section> for "semantics"
  that does nothing). Resolve the rule: a Section earns its landmark by
  having a name (a heading), and don't over-landmark (too many regions =
  landmark noise — the inverse over-semantic trap, cf. Divider/Banner).
- THE HEADING-LEVEL CONTRACT + THE DOCUMENT-OUTLINE-ALGORITHM MYTH (the
  load-bearing point): HTML5 PROMISED that sectioning elements would
  auto-compute heading levels (an <h1> inside a <section> would become an h2
  in the outline) — but NO BROWSER EVER IMPLEMENTED IT and it was REMOVED
  from the spec. So heading levels are NOT automatic; a flat sea of <h1>s
  "fixed by the outline" is broken for AT. Resolve the practice's answer:
  manual level discipline (h1 -> h2 -> h3) AND/OR a HEADING-LEVEL CONTEXT
  component (a Section provides an auto-incrementing level to a nested
  Heading/<H> — the react-headings / Heydon Pickering <H> pattern), so
  nesting Sections deepens the heading level automatically and correctly.
- THE GENRE SPLIT — SEMANTIC SECTION vs VISUAL/LAYOUT SECTION (the naming +
  scope question, parallel to Stack's direction / Grid's genres): (1) the
  SEMANTIC Section (a landmark region + heading-level context — the
  document-structure concern); (2) the VISUAL/LAYOUT "section" — a full-
  bleed page band (a background color/image edge-to-edge) with a
  CONSTRAINED/centered content column inside (the marketing-page section).
  And the CONSTRAINED-WIDTH primitive (Container / max-width content column —
  MUI/Chakra/Bootstrap Container) that the visual section pairs with.
  Resolve how the practice models these (one Section + a Container? a
  Section that does both? Container as a separate primitive?).
- THE SECTIONING-ELEMENT DECISION: <section> (a thematic grouping, needs a
  name) vs <article> (self-contained, syndicatable — a post/card/comment)
  vs <aside> (tangential/complementary -> role=complementary) vs <nav>
  (-> see side-navigation) vs <main> (the one main region) vs <div> (no
  semantics — the right default when there's no landmark value). Resolve
  the decision tree and the "don't reach for <section> by default; <div> is
  fine" rule.
- THE FULL-BLEED-BACKGROUND / CONSTRAINED-CONTENT CSS PATTERN: the
  background spans the viewport edge-to-edge while the content stays in a
  centered max-width column — the breakout pattern (the
  `[full] minmax(0,1fr) [content] minmax(0, var(--max)) [content] ...` grid
  trick, or the full-width-background + inner-container pattern). The
  recurring marketing-layout trap.
- THE SECTION HEADER + THE app-shell/landmark COMPOSITION: the section
  header slot (a heading + optional description + section-level actions —
  "Settings" / "Manage your account" / an Edit button); and Section's role
  in the app shell / PageLayout (the page as a tree of landmark regions:
  banner/main/complementary/contentinfo — relating to Grid's named-areas
  and Side Navigation's nav landmark).

Field-leader systems to survey (web): note that MANY systems DON'T ship a
"Section" component (it's semantic HTML + a layout primitive + a heading
discipline) — that itself is a finding. Survey: GitHub Primer (PageLayout —
Header/Content/Pane/Footer landmark regions), Shopify Polaris (Page +
Layout + Layout.Section; BlockStack; the section-as-grouping), Atlassian
(PageLayout — Banner/TopNavigation/LeftSidebar/Main landmark slots), MUI
(Container — the max-width constrained content; no Section), Chakra UI
(Container; as="section"), Bootstrap (Container — the constrained-width
lineage), Adobe Spectrum / React Aria (the landmark utilities — useLandmark,
landmark navigation; the View), IBM Carbon (the grid + semantic sectioning),
Material 3 (the layout regions). Heading-level-context references:
react-headings, Heydon Pickering's <H> / heading-level-context pattern,
the abandoned HTML5 document outline algorithm. Accessibility: WAI-ARIA
landmark roles (region/complementary/main/banner/contentinfo), the
<section>-needs-a-name rule, the heading-outline reality. Cite each with a
version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Box substrate — the as/asChild
Slot, the spacing-token scale, the styling delivery, the logical-property
RTL; note the Stack-content / Grid-Card-hosting composition and the Card
visual-surface boundary; flag unverified/volatile platform claims under
notes.unverified).

1. Framing — what it is (the semantic document region — landmark +
   heading-level contract, the semantic counterpart to Card's visual
   surface; the category-closing Layout brief) and what it isn't (Card — a
   visual chrome surface; Box — a neutral non-semantic container; a default
   wrapper — <div> is fine); the nameless-section/landmark contract + the
   heading-level/outline-myth + the semantic-vs-visual genre split up front;
   why systems disagree (and why many don't ship one).
2. Anatomy and parts — the sectioning element (the rendered tag), the
   section header (heading + description + actions), the body (a Stack /
   Grid of Cards), the (optional, visual variant) full-bleed background +
   constrained content column; the (absence of) chrome by default.
3. Properties / API — as (section/article/aside/div), the accessible name
   (aria-labelledby the heading / aria-label), headingLevel (or the
   heading-level context), the header slot, the visual variant (full-bleed
   background) + maxWidth/Container, padding/spacing, asChild (inherited).
4. States and variants — Section has no interaction states; the semantic
   variants (region/article/aside/generic); the visual variants (plain /
   full-bleed-band / constrained); with/without a header.
5. Usage guidance — Section (a semantic region with a name + heading) vs
   Card (a visual surface) vs Box/div (no semantics — the default, don't
   over-section) vs main/nav/aside (the specific landmarks); when a region
   earns a landmark; the don't-over-landmark rule; the heading-level
   discipline; the visual-section/Container case.
6. Accessibility — the nameless-<section>-is-not-a-landmark rule (name via
   aria-labelledby->heading or aria-label); the landmark model (region/
   complementary/main/banner/contentinfo) + don't-over-landmark; THE
   HEADING-LEVEL CONTRACT (the outline-algorithm myth, manual levels, the
   heading-level context); the one-h1 / one-main rule; WCAG SCs (1.3.1
   info+relationships, 2.4.1 bypass blocks / landmarks, 2.4.6 headings+labels,
   2.4.10 section headings).
7. Content guidelines — the section heading (the accessible name, specific
   not generic), the description, the heading hierarchy, don't-skip-levels,
   don't-wrap-everything-in-section.
8. Motion and transition — minimal/none of its own (a semantic container);
   scroll-into-view / scroll-snap sections as a composition; reduce-motion.
9. Internationalization — RTL (logical properties inherited from Box; the
   section header + actions mirror); the heading/landmark name translated;
   the full-bleed background direction-agnostic.
10. Naming — Section / Container / Region / Layout.Section / PageLayout /
    Panel; the semantic-Section vs the constrained-Container split; the
    practice's default; aliases; note many systems ship Container not
    Section.
11. Implementation notes — the as -> sectioning element + the name->landmark
    wiring (aria-labelledby the heading id); the heading-level context
    (auto-incrementing nested levels, the <H> pattern) over the dead outline
    algorithm; the full-bleed-background/constrained-content CSS (the grid
    breakout / the inner-container pattern + max-width tokens); the
    don't-over-landmark lint; inheriting Box's Slot + scale + logical
    properties; headless vs opinionated; why a Container primitive often
    suffices.
12. Related and alternative components — typed relationships (STANDS ON Box;
    COMPOSES Stack [content] + hosts Grid/Card; the Card visual-surface
    boundary [semantic region vs visual object]; the main/nav/aside/header/
    footer landmark siblings; Side Navigation's nav landmark; the Container/
    max-width alternative; the Heading heading-level relationship).
13. Field POV evolution — the document-outline-algorithm myth -> its removal
    -> manual heading levels -> the heading-level-context component; the
    <section>-needs-a-name landmark settling; landmark navigation raising
    region correctness; the full-bleed-background/constrained-content CSS
    pattern; many systems shipping Container/PageLayout not Section.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Section is — explain the
nameless-<section>-is-not-a-landmark contract (the most common misuse), the
heading-level contract + the document-outline-algorithm myth (it never
shipped; manual levels or a heading-level context), the semantic-Section-vs-
visual/Container genre split, the sectioning-element decision tree
(section/article/aside/main/div — and "div is fine, don't over-section"),
the full-bleed-background/constrained-content CSS pattern, and the
don't-over-landmark rule that field leaders still get wrong.

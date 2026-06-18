You are researching the Card component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Card is,
knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop/slot choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Card is THE FIRST STYLED SURFACE — the fourth Layout brief, the component
where Box's deliberate neutrality ENDS and visual chrome (background,
border, radius, elevation) begins, and the convergence host WHERE THE
FOUNDATIONS CLUSTER MEETS LAYOUT. It STANDS ON the layout primitives and
COMPOSES the briefed Foundations components:
- IT STANDS ON BOX + STACK (components/box.md, components/stack.md): the
  SURFACE is a Box (the polymorphic as/asChild Slot, the token-mapped
  background/border/radius, the padding from the spacing scale, the
  zero-runtime delivery, the logical-property RTL); the BODY LAYOUT is a
  Stack (header/media/body/footer stacked with gap, owning the no-external-
  margin discipline). Card is literally the answer to Box's "if you're
  adding chrome to a Box, you want a Card." Don't re-derive Box/Stack —
  name them and record the delta (the chrome + the slots + the
  interactivity).
- IT COMPOSES THE FOUNDATIONS CLUSTER: a Card hosts Avatar (the author),
  Badge (a status), Tag (categories), Skeleton (the loading card), Button
  (actions), Heading/Text, and Image/Media (components/avatar.md, badge.md,
  tag.md, skeleton.md, button.md, link.md). This is the brief where the
  Foundations work pays off — reference those hosts, don't re-derive them.
- IT IS THE CELL OF A GRID GALLERY (components/grid.md): cards tile in the
  auto-grid RAM pattern; EQUAL-HEIGHT cards align their internal rows via
  SUBGRID (the Grid brief's subgrid case). Reference Grid; don't re-derive.

THE DEFINING CARD-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE SURFACE / ELEVATION MODEL (the headline — what makes a Card a Card):
  Card formalises the SURFACE that Box/Stack/Grid deliberately lack —
  background, border, radius, and ELEVATION (shadow). Resolve the variant
  model: Material 3's three cards — ELEVATED (shadow) / FILLED (tonal
  background) / OUTLINED (border) — and the elevation-token system + the
  hover-elevation-change for interactive cards. The surface-token / Material
  "Surface" concept.
- THE SLOT MODEL (the compositional anatomy): header / media / body /
  footer (+ actions). Resolve the SLOTTED / COMPOUND-COMPONENT API
  (Card.Header/Card.Body/Card.Footer/Card.Media — MUI CardHeader/CardMedia/
  CardContent/CardActions; Chakra CardHeader/Body/Footer; Ant Card.Meta) vs
  a monolithic Card-with-props, and the FULL-BLEED MEDIA problem (an image
  that breaks the card's padding to go edge-to-edge — the media-slot-
  outside-padding / negative-margin pattern). This is the bundled-vs-
  composed tension (cf. Text Field) applied to a surface.
- THE INTERACTIVE-CARD PROBLEM (the accessibility crux, and genuinely
  contested): the WHOLE-CARD-CLICKABLE vs ACTIONS-INSIDE decision, and the
  NESTED-INTERACTIVE TRAP — a clickable card (a/button) containing a button
  or link is INVALID HTML (interactive-in-interactive), the same trap Tag's
  grid pattern and Box's polymorphism named. Resolve the settled accessible
  pattern: THE STRETCHED-LINK / "block link" pattern (one primary link
  inside the card carries a ::after pseudo-element stretched over the whole
  card surface, so the entire card is clickable but only ONE real link
  exists; secondary actions sit ABOVE it in z-index and remain
  independently clickable) — Heydon Pickering's Inclusive Components "Cards"
  — vs MUI's CardActionArea (a button wrapping the clickable region) vs
  making the whole card a single <a>/<button> (valid ONLY when there are no
  other interactive elements inside). Resolve the accessible name (the
  card's heading/title), the focus ring on the whole card, the
  text-selection cost of stretched-link, and the "don't bury secondary
  actions under the stretched link" rule.
- EQUAL-HEIGHT + CARD-AS-GRID-CELL + CONTENT OVERFLOW: cards in a gallery
  (the Grid auto-grid); equal-height cards (SUBGRID aligning the title/body/
  footer rows across a row of cards — the Grid brief's subgrid case); the
  footer-pinned-to-the-bottom pattern (the body grows, the footer sticks);
  content truncation within a fixed card.
- PADDING / DENSITY + MEDIA-BLEED: the card's internal padding/inset (from
  the spacing scale), the density variants, and the full-bleed media that
  must break the padding (edge-to-edge cover image) — the recurring
  layout trap.

Field-leader systems to survey (web): Google Material 3 (Card — elevated/
filled/outlined; the elevation system; clickable cards), MUI (Card +
CardHeader/CardMedia/CardContent/CardActions/CardActionArea — the slot model
+ the clickable-region button), Chakra UI (Card + CardHeader/Body/Footer;
variants elevated/outline/filled), Shopify Polaris (Card — the workhorse
surface; sectioned cards; the recent web-component s-card), GitHub Primer
(the Box-based card; link previews), Adobe Spectrum / React Aria (Card —
selectable cards / card collections), IBM Carbon (Tile — the Card-equivalent:
ClickableTile / SelectableTile / ExpandableTile — note the naming), Ant
Design (Card — Card.Meta, cover, actions, tabs), Atlassian (Card — link-
preview cards), Base Web (Uber) (Card). Accessibility references: Heydon
Pickering's Inclusive Components "Cards" (the stretched-link/pseudo-content
pattern), the nested-interactive (interactive-in-interactive) HTML-validity
rule, Sara Soueidan / WAI on block links. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Box surface + the Stack body, and
note the Foundations-cluster composition (Avatar/Badge/Tag/Skeleton/Button/
Text/Media) and the Grid-cell/subgrid relationship; flag unverified/volatile
platform claims under notes.unverified).

1. Framing — what it is (the first styled surface, the elevation/container,
   the Foundations-meets-Layout convergence host) and what it isn't (Box —
   the neutral substrate; Section — a semantic region not a surface; Dialog/
   Popover — overlay surfaces, Card is in-flow); the surface/elevation model
   + the slot model + the interactive-card problem up front; why systems
   disagree.
2. Anatomy and parts — the surface (Box: bg/border/radius/elevation/
   padding), the slots (header/media/body/footer/actions), the body Stack,
   the full-bleed media, the (optional) interactive layer; the
   composed Foundations contents.
3. Properties / API — variant (elevated/filled/outlined), the slot
   components (Card.Header/Media/Body/Footer/Actions) vs props, padding/
   density, interactive/clickable (+ the href/onClick), as/asChild
   (inherited from Box), elevation token.
4. States and variants — elevated/filled/outlined; default vs interactive
   (hover/focus/active elevation change, the focus ring); selected (card
   collections); loading (Skeleton); the with-media / sectioned variants.
5. Usage guidance — Card (a styled in-flow surface grouping related
   content) vs Box (no chrome — the constrained-over-open reach) vs Section
   (a semantic region) vs Dialog/Popover (overlay surfaces); when a card vs
   a list row vs a table row; the don't-nest-cards / card-overuse rule; the
   whole-card-clickable-vs-actions decision.
6. Accessibility — the interactive-card nested-interactive trap + the
   stretched-link pattern (one real link + ::after, secondary actions
   z-indexed above; the accessible name from the heading; the whole-card
   focus ring; the text-selection cost) vs CardActionArea vs whole-card-<a>;
   the card is a generic container by default (no implicit role — group/
   region/article/listitem via as when meaningful); heading structure
   inside the card; WCAG SCs (2.1.1 keyboard, 2.4.7 focus visible, 4.1.2,
   1.3.1, 2.5.5/2.5.8 target size for the stretched link).
7. Content guidelines — the card title (the accessible name + the
   stretched-link target), scannable content, truncation, the actions
   (primary/secondary), don't-overload-the-card.
8. Motion and transition — the hover-elevation lift (interactive cards),
   the loading→content swap (Skeleton), the enter/reflow in a gallery
   (FLIP), reduce-motion.
9. Internationalization — RTL (the surface/padding via logical properties,
   the media/header mirroring, the actions flipping to the leading edge —
   inherited from Box/Stack); content expansion + the equal-height impact.
10. Naming — Card / Tile (Carbon) / Panel / Well / Surface; the slot naming
    (Header/Body/Footer/Media/Actions vs Content); the practice's default;
    aliases.
11. Implementation notes — the surface on Box (token bg/border/radius/
    elevation); the slot/compound API; the full-bleed media (negative-margin
    / media-outside-padding); the stretched-link (::after + position
    relative on the card + z-index for secondary actions + the
    user-select fix); equal-height via subgrid + the footer-pinned pattern;
    the interactive elevation/focus; inheriting Box's Slot + scale + logical
    properties and Stack's gap; headless vs opinionated.
12. Related and alternative components — typed relationships (STANDS ON Box
    [surface] + Stack [body]; COMPOSES Avatar/Badge/Tag/Skeleton/Button/Text/
    Media; the CELL of a Grid gallery [auto-grid + subgrid equal-height];
    the Link stretched-link relationship; the Dialog/Popover overlay-surface
    boundary; the Section semantic-region boundary; the Carbon Tile alias).
13. Field POV evolution — the monolithic card → the slotted/compound card;
    Material's three-variant elevation model settling; the interactive-card
    a11y settling (the stretched-link pattern over the whole-card-button);
    subgrid enabling equal-height card content; cards-as-collections
    (selectable card grids).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Card is — explain the
surface/elevation model (elevated/filled/outlined + the elevation tokens),
the slot model (compound Card.Header/Body/Footer/Media vs props + the
full-bleed media trap), the interactive-card nested-interactive problem +
the stretched-link pattern (one real link + ::after, secondary actions
z-indexed above) vs CardActionArea vs whole-card-<a>, the equal-height /
card-as-Grid-cell / subgrid case, and the padding/media-bleed trap that
field leaders still diverge on.

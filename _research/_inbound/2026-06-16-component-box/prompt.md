You are researching the Box component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Box/View
primitive is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the architectural decisions still contested, the
implementation traps that recur across codebases.

Box is THE LAYOUT SUBSTRATE — the foundational, lowest-level primitive that
OPENS the Layout category, the way Text Field opened Form and Popover
formalised the Overlay positioning substrate. It is the polymorphic,
token-aware, style-prop-bearing element that Stack, Grid, Card, and Section
will all STAND ON. Get the substrate right because the rest of the category
inherits it. It also formalises a mechanic already referenced by briefed
components:
- THE POLYMORPHIC asChild / Slot + `as` MODEL is shared with Button and Link
  (components/button.md, components/link.md already lean on asChild/Slot
  polymorphism for the link-vs-button and router cases). Box is where this
  substrate is formalised; don't re-derive it — name it and resolve it.
- THE SPACING-TOKEN SCALE Box owns is what Stack's `gap`, Grid's `gap`, and
  Card's padding will all reference (Stack/Grid/Card/Section not yet
  briefed — forward-reference them as the inheritors).

THE DEFINING BOX-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE HEADLINE — SHOULD A DESIGN SYSTEM EVEN SHIP A BOX? The central,
  genuinely contested question. Two philosophies: (1) THE STYLE-PROP BOX
  (Chakra, Theme UI, MUI Box/sx, Radix Themes, Polaris) — a polymorphic
  primitive exposing a large surface of style props (p/m/bg/display/flex…)
  mapping to tokens, the "everything is a Box" / React-Native-View /
  Styled-System lineage; (2) THE CONSTRAINED / NO-BOX TURN (Braid's
  Stack/Inline/Columns, Tailwind+shadcn's utility-classes-no-Box) — skip the
  god-Box, ship intent-revealing constrained layout components + bare
  elements, on the argument that a Box with 100 style props is inline styles
  with extra steps that leak the constraint system and breed unmaintainable
  one-offs. Resolve the practice's POV: is Box the SUBSTRATE (the low-level
  escape hatch Stack/Grid are built on) but NOT the recommended authoring
  surface (reach for constrained layout first)? The "constrained over open"
  principle.
- THE POLYMORPHIC `as` vs `asChild`/Slot MODEL (the headline mechanic):
  `as="section"` (render a different element) vs `asChild` (Radix Slot —
  merge props/behaviour onto the consumer's child). The notorious
  TypeScript cost of a fully-generic polymorphic `as` (forwardRef +
  polymorphic typing is one of the hardest typing problems in React DS
  land) and asChild/Slot as the modern answer that sidesteps the typing
  explosion. The accessibility trap: `as`/polymorphism can produce wrong or
  invalid semantics (an `as="button"` with no button behaviour) — Box is
  semantically neutral (a div, no role) and the consumer must pick the
  right element.
- STYLE PROPS vs sx vs className vs UTILITY CLASSES + THE ZERO-RUNTIME
  RECKONING (the big platform inflection, like Select's appearance:base-
  select): how much CSS to expose as props; the responsive array/object
  breakpoint syntax (p={[2,3,4]} — Styled System); the sx prop (MUI); vs
  Tailwind utility classes vs CSS Modules. The RUNTIME CSS-IN-JS PERF +
  RSC-COMPATIBILITY RECKONING that is killing runtime style-prop engines
  and pushing the field to ZERO-RUNTIME (Vanilla Extract, Panda CSS,
  Tailwind) and CSS Modules — and Primer's worked sx-deprecation as the
  cautionary tale. Date this; it's volatile.
- THE SPACING-TOKEN SCALE (what the whole Layout category inherits): the
  4/8px base grid, the numeric vs t-shirt scale, primitive vs semantic
  spacing tokens, the responsive scale. Box owns it; Stack/Grid `gap` and
  Card padding reference it.
- THE BOX MODEL EXPOSURE + THE "NO EXTERNAL MARGIN" PRINCIPLE: padding /
  margin / display / size / overflow / position as props — and the strong,
  near-settled POV that COMPONENTS SHOULD NOT OWN THEIR EXTERNAL MARGIN
  (margins break encapsulation; spacing between siblings belongs to the
  PARENT layout via Stack/Grid `gap`, not the child's margin). Resolve the
  margin-considered-harmful position and what Box should and shouldn't
  expose.

Field-leader systems to survey (web): Chakra UI (Box — the canonical
style-prop polymorphic primitive, `as`, style props), Theme UI (Box — the
Styled System lineage, `sx`, responsive arrays), MUI (Box — the `sx` prop,
`component` prop, system props), Radix Themes + Radix Primitives (Box +
the `asChild` Slot pattern — the polymorphic substrate), Braid/Seek (Box +
the Stack/Inline/Columns constrained-layout philosophy — the no-margin,
constrained-over-open school), Tailwind + shadcn/ui (the
utility-classes-no-Box position), GitHub Primer (Box — and the sx-
deprecation migration toward CSS Modules), Shopify Polaris (Box — token
props, the layout primitive), Adobe Spectrum / React Aria (View — the
RN-style primitive), Base Web (Uber) (Block), Styled System (the historical
prop→token-mapping lineage), Vanilla Extract / Panda CSS (the zero-runtime
successors). WAI-ARIA / HTML (Box is a semantically-neutral div — no role;
the `as`-produces-wrong-semantics trap). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: where relevant; note the polymorphic
asChild/Slot substrate shared with Button/Link, and that Box is the
substrate Stack/Grid/Card/Section will inherit; flag unverified/volatile
platform claims under notes.unverified).

1. Framing — what it is (the polymorphic token-aware layout substrate, the
   "open canvas") and what it isn't (a styled component, a layout engine —
   that's Stack/Grid); the should-a-DS-ship-a-Box debate + the constrained-
   over-open principle + the polymorphic model up front; why systems disagree.
2. Anatomy and parts — there is barely a visual anatomy (it's a div); the
   "anatomy" is the PROP SURFACE: the rendered element (`as`), the
   token-mapped style props, the box-model props, the (absence of)
   semantics.
3. Properties / API — `as`/`asChild`, the style-prop surface (p/m/bg/
   display/flex/grid/…), the responsive syntax, sx-vs-props, the
   spacing-token scale, what to expose vs withhold (the margin question).
4. States and variants — Box has no interaction states (no hover/focus of
   its own); the "variants" are the rendered element + the styling-engine
   delivery (style-prop / sx / className / zero-runtime); the
   display/layout modes it can take (and why those belong to Stack/Grid).
5. Usage guidance — Box (the low-level escape hatch / substrate) vs Stack/
   Grid (the constrained layout engines — reach for these first) vs a
   styled component vs bare HTML+className; when a Box is the right tool and
   when it's a smell; the constrained-over-open rule.
6. Accessibility — Box is a semantically-neutral div (no role, no name);
   the WHOLE a11y story is the element it renders (`as`/`asChild`) and the
   trap of producing wrong/invalid semantics; the "primitive has no
   inherent semantics, don't let it emit the wrong ones" rule.
7. Content guidelines — minimal; Box holds content/children, it doesn't
   author it; the no-bare-Box-for-text note.
8. Motion and transition — minimal/none of its own; it's a container others
   animate.
9. Internationalization — logical properties (padding-inline/margin-block)
   over physical so the spacing props flip under RTL with no JS; the
   token scale's logical mapping.
10. Naming — Box / View / Block / Frame / Primitive; the practice's default;
    the group/layout descendants (Stack/Grid/Flex/Inline); aliases.
11. Implementation notes — the polymorphic `as` TypeScript explosion +
    forwardRef + asChild/Slot as the escape; the style-prop→token engine
    (runtime CSS-in-JS vs zero-runtime Vanilla-Extract/Panda vs Tailwind vs
    CSS Modules) + the RSC/perf reckoning; the responsive prop
    implementation; the spacing scale; the no-external-margin enforcement;
    headless vs opinionated.
12. Related and alternative components — typed relationships (Box is the
    SUBSTRATE for Stack/Grid/Card/Section; the asChild/Slot polymorphism
    shared with Button/Link; the spacing-token scale shared with the whole
    Layout category; the styled-component / utility-class alternatives).
13. Field POV evolution — Styled System → runtime CSS-in-JS style-prop Box
    (Chakra/Theme UI/MUI sx) → the perf + RSC reckoning → zero-runtime
    (Vanilla Extract/Panda/Tailwind) + the constrained-layout (Stack/Inline
    over Box) turn; asChild/Slot settling over the `as`-typing nightmare;
    the no-external-margin principle hardening.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Box is — explain the should-
a-DS-ship-a-Box debate (style-prop Box vs the constrained/no-Box turn) +
the constrained-over-open principle, the polymorphic `as`-vs-asChild/Slot
model (the TypeScript explosion + the wrong-semantics a11y trap), the style-
props vs sx vs utility-classes question + the zero-runtime / RSC perf
reckoning that is reshaping the whole category, the spacing-token scale the
Layout category inherits, and the no-external-margin principle that field
leaders increasingly enforce.

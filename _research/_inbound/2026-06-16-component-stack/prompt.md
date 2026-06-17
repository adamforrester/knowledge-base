You are researching the Stack component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they converge
on, where they diverge, and what the practice's opinionated default
should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a Stack /
flex-layout primitive is, knows what a design system is, and has shipped
multiple component libraries. Explain the non-obvious — the prop choices
field leaders disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

Stack is THE FIRST LAYOUT ENGINE — the one-dimensional (flexbox) layout
component, the second Layout brief after Box, and the component the
no-external-margin principle most directly implies. It STANDS ON Box and
COMPOSES a briefed primitive:
- IT STANDS ON BOX (components/box.md): it inherits the polymorphic
  as/asChild Slot model, the spacing-token scale (its `gap` resolves
  against it), the zero-runtime styling delivery, and the logical-property
  RTL mapping. Don't re-derive Box — name it and record only the delta.
- IT IS THE ANSWER TO BOX'S NO-EXTERNAL-MARGIN PRINCIPLE: Box established
  that components must not own their external margin; Stack is the canonical
  mechanism that OWNS THE SPACE BETWEEN SIBLINGS via `gap`, so children
  never carry margins. This is the load-bearing thesis — Stack is "the
  component that owns the gap."
- IT COMPOSES DIVIDER (components/divider.md): the divider-between-children
  feature (MUI `divider`, Chakra `StackDivider`, Braid `dividers`) — n-1
  separators between but not around items. Reference Divider; don't
  re-derive it.
It is the 1D SIBLING of Grid (the 2D engine — not yet briefed;
forward-reference the boundary), and is COMPOSED BY Card / forms / lists /
nav and nested recursively (a Stack of Stacks).

THE DEFINING STACK-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE GAP MECHANISM + THE FLEX-GAP INFLECTION (the headline): modern Stack
  owns the space between children via CSS flexbox `gap`, resolving against
  Box's spacing-token scale. Cover the history that makes this non-obvious:
  the "lobotomized owl" (`* + *` margin) and the margin-bottom/negative-
  margin hacks Stack used BEFORE flex `gap` shipped, and the FLEX-GAP
  BROWSER-SUPPORT INFLECTION (Safari 14.1, ~2021) that made `gap` the
  viable default. Date it; it's why old Stacks look the way they do.
- THE DIRECTION QUESTION + THE NAMING MORASS: is it ONE Stack with a
  `direction`/`orientation` prop (MUI), or TWO named components
  (Chakra VStack/HStack; Braid Stack[vertical]/Inline[horizontal]; Polaris
  BlockStack/InlineStack)? Resolve the practice's model — and note the
  RESPONSIVE-DIRECTION SWITCH (column on mobile → row on desktop,
  direction={{base:'column', md:'row'}}) as the killer argument that often
  decides it. Also resolve LOGICAL vs PHYSICAL axis naming (Polaris's
  Block/Inline = logical, RTL-correct; vs Vertical/Horizontal or row/column
  = physical).
- THE ALIGN / JUSTIFY MATRIX (the props after gap): `align` (cross-axis:
  start/center/end/stretch — and the stretch-default question) and
  `justify` (main-axis: start/center/end/space-between/around). The
  most-used props after gap; resolve the defaults and the naming.
- WRAPPING (the Inline/horizontal problem): a horizontal stack must WRAP
  when it overflows (`flex-wrap`), and wrapping reintroduces the cross-axis
  gap (row-gap as well as column-gap) — the wrap + two-axis-gap interaction
  flex `gap` finally makes clean. Resolve when Stack wraps and how gap
  behaves across wrapped lines.
- THE DOM-ORDER-vs-VISUAL-ORDER A11Y TRAP (the accessibility crux):
  Stack is layout-only and semantically neutral (a flex div, no role — it
  inherits Box's a11y story), BUT flexbox `row-reverse`/`order`/wrap can
  make VISUAL order diverge from DOM/reading/tab order — a real WCAG 1.3.2
  (Meaningful Sequence) + 2.4.3 (Focus Order) violation. Resolve the rule:
  Stack must not reorder content visually away from DOM order; the
  no-reorder discipline.
- THE RECURSIVE / NESTED MODEL + per-item flex: layouts are built as a TREE
  of Stacks (a vertical Stack of horizontal Stacks) — the
  whitespace-is-systematic principle. And the question of whether Stack
  exposes per-item flex (grow/shrink) or keeps it simple (gap/align/justify/
  direction only) and leaves per-item control to the child or a Spacer.

Field-leader systems to survey (web): Chakra UI (Stack / VStack / HStack,
spacing→gap, StackDivider, align/justify), MUI (Stack — direction, spacing,
divider, useFlexGap), Braid/Seek (Stack[vertical] + Inline[horizontal],
dividers, the no-margin origin), Radix Themes (Flex — direction/align/
justify/gap/wrap; the Flex-not-Stack naming), Shopify Polaris (BlockStack /
InlineStack — the LOGICAL-axis naming, gap, align), GitHub Primer (Stack +
PageLayout), Adobe Spectrum / React Aria (Flex — the layout component),
IBM Carbon (Stack — gap, orientation), Atlassian (Stack / Inline /
@atlaskit/primitives — Box+Stack+Inline+Flex with xcss), Tailwind (flex +
gap utilities — the no-Stack position), Base Web (Uber). WAI-ARIA / HTML
(Stack is a semantically-neutral flex div — no role; the DOM-order-vs-
visual-order meaningful-sequence trap). Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Box substrate — the as/asChild
Slot, the spacing-token scale, the styling delivery, the logical-property
RTL; note the Divider composition and the Grid sibling boundary; flag
unverified/volatile platform claims under notes.unverified).

1. Framing — what it is (the 1D flexbox layout engine that owns the gap, the
   answer to the no-external-margin principle) and what it isn't (Box — the
   neutral substrate; Grid — the 2D engine); the gap-mechanism + the
   direction/naming question + the no-reorder a11y rule up front; why
   systems disagree.
2. Anatomy and parts — the flex container, the gap (between children), the
   optional dividers-between (composing Divider), the (absence of) visual
   chrome; the children as flex items.
3. Properties / API — direction/orientation (or VStack/HStack), gap/spacing
   (→ Box's scale), align (cross), justify (main), wrap, dividers, as/
   asChild (inherited from Box), responsive direction/gap.
4. States and variants — Stack has no interaction states; the variants are
   direction (vertical/horizontal/responsive), with-dividers, wrap/no-wrap,
   the align/justify combinations.
5. Usage guidance — Stack (1D, owns the gap — reach for it over a bare Box)
   vs Box (the neutral escape hatch) vs Grid (2D — when you need rows AND
   columns); when Stack vs Inline (vertical vs horizontal); the
   nest-Stacks-recursively model; the no-margin-on-children rule.
6. Accessibility — Stack is a neutral flex div (inherits Box's a11y: the
   element it renders via as); THE DOM-order-vs-visual-order meaningful-
   sequence trap (no row-reverse/order/wrap that diverges visual from DOM/
   reading/tab order — WCAG 1.3.2 + 2.4.3); the as="ul"/"ol"/"nav" semantic
   wrapping; the no-reorder discipline.
7. Content guidelines — Stack holds layout, not content; the
   list-semantics note (as="ul" + li children); don't fake a list visually
   without the semantics.
8. Motion and transition — minimal; the reflow/reorder animation when items
   add/remove (FLIP), reduce-motion; Stack itself ships none.
9. Internationalization — the gap is direction-agnostic; RTL flips the main
   axis of a horizontal Stack via logical properties / flex (inherited from
   Box); the LOGICAL-axis naming (Block/Inline) as the RTL-correct model;
   no hardcoded row direction.
10. Naming — Stack / VStack / HStack / Inline / BlockStack / InlineStack /
    Flex; one-direction-prop vs two-components; logical vs physical axis
    naming; the practice's default; aliases.
11. Implementation notes — flex `gap` over the lobotomized owl (and the
    Safari 14.1 inflection + the legacy fallback); the direction prop +
    responsive direction; align/justify mapping; wrap + two-axis gap; the
    divider-between (n-1, composing Divider); the no-reorder enforcement;
    inheriting Box's Slot + scale + logical properties; headless vs
    opinionated.
12. Related and alternative components — typed relationships (STANDS ON Box;
    COMPOSES Divider; the 1D SIBLING of Grid; COMPOSED BY Card/forms/lists/
    nav; the recursive Stack-of-Stacks; the Spacer alternative for flexible
    gaps; the flex-utility-class alternative).
13. Field POV evolution — the lobotomized owl → flex `gap` (the Safari
    14.1/2021 inflection) → Stack-owns-the-space; the no-margin principle
    making Stack canonical; logical-axis naming (Polaris Block/Inline) for
    RTL; the DOM-order-vs-visual-order a11y settling.
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a Stack is — explain the gap
mechanism + the flex-gap inflection (the lobotomized-owl history + Safari
14.1), the direction question + the naming morass (one direction prop vs
VStack/HStack vs Stack/Inline vs BlockStack/InlineStack; logical vs physical
axis naming) + the responsive-direction switch that decides it, the align/
justify matrix, the wrap + two-axis-gap interaction, the DOM-order-vs-
visual-order meaningful-sequence a11y trap (the no-reorder rule), and the
recursive Stack-of-Stacks model that field leaders build layouts from.

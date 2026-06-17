# Stack — field-truth study (Claude pass)

## 1. Framing
A Stack is the **one-dimensional layout engine** — a flexbox container that arranges its children along a single axis (vertical by default) with a uniform, token-scaled **gap** between them. It is the second Layout brief after Box, and it is the component the **no-external-margin principle most directly implies**: Box established that components must not own their external margin; Stack is the canonical mechanism that **owns the space between siblings**, so the children never carry margins. That is the load-bearing thesis — **Stack is the component that owns the gap**.

Three things define it and are where systems diverge:
- **The gap mechanism + the flex-gap inflection.** Modern Stack owns inter-child spacing via CSS flexbox `gap`, resolving against Box's spacing-token scale. This is non-obvious because it's *recent*: before `gap` worked in flexbox (Safari shipped it in **14.1, ~April 2021**), Stacks used the **"lobotomized owl"** (`* + *` margin) or margin-bottom-plus-negative-margin hacks — which is why older Stack implementations look the way they do. The flex-gap inflection is what made "Stack owns the gap" clean.
- **The direction question + the naming morass.** Is it *one* Stack with a `direction` prop (MUI), or *two* named components (Chakra `VStack`/`HStack`; Braid `Stack`/`Inline`; Polaris `BlockStack`/`InlineStack`)? And logical (`Block`/`Inline`) vs physical (`Vertical`/`Horizontal`, `row`/`column`) axis naming. The **responsive-direction switch** (column on mobile → row on desktop) is the argument that usually decides it.
- **The DOM-order-vs-visual-order a11y rule.** Stack is layout-only and semantically neutral, but flexbox can divorce *visual* order from *DOM* order — a real accessibility trap (§6).

It stands on **Box** (the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, the logical-property RTL mapping — all inherited, not re-derived — see box), composes **Divider** (the divider-between-children feature — see divider), is the **1D sibling of Grid** (the 2D engine — not yet briefed), and is composed by Card, forms, lists, and nav, nested recursively (a Stack of Stacks). What it *isn't*: a **Box** (the neutral substrate with no layout opinion — Stack *is* the opinion: flex + gap + a direction; see box) or a **Grid** (the 2D engine — when you need rows *and* columns simultaneously, not a single axis). Why systems disagree: the direction/naming model, the align/justify defaults, and whether to expose per-item flex.

## 2. Anatomy and parts
- **the flex container** — the Stack itself: `display: flex` + a `flex-direction` (column default) + `gap`. Semantically a neutral `div` (inherits Box's neutrality — §6).
- **the gap** — the uniform space *between* children (not around them — that's the parent's padding), resolving against Box's spacing-token scale. The defining "part," though it's whitespace, not an element.
- **the children as flex items** — the content Stack arranges; each becomes a flex item. Stack mostly doesn't style them (the per-item-flex question — §3).
- **the optional dividers-between** — interleaved separators between children (composing Divider — see divider): **n−1** dividers for n children (between, never around — §11). A composition, not a default.
- **the (absence of) visual chrome** — no background, border, radius, or elevation of its own (that's Card); Stack is pure layout. If you're adding chrome to a Stack, you want a Card (§5).

## 3. Properties / API
- **`direction` / `orientation`** (or the two-component split) — vertical (default) / horizontal; **responsive** (`direction={{ base: 'column', md: 'row' }}`). The headline axis decision (§10). Prefer **logical** values (block/inline, or column/row mapped to logical) for RTL-correctness.
- **`gap` / `spacing`** — the inter-child space, a token-scale index (inherits Box's scale — `gap={4}` → the 4th spacing token). The defining prop. (MUI calls it `spacing`; the field is converging on `gap` to match the CSS property.)
- **`align`** — the **cross-axis** alignment (`flex-align-items`): start / center / end / **stretch**. The stretch-default question: a vertical Stack defaulting `align: stretch` makes children full-width (often desired); `start` leaves them intrinsic-width. Resolve the default per direction.
- **`justify`** — the **main-axis** distribution (`justify-content`): start / center / end / space-between / space-around / space-evenly.
- **`wrap`** — whether items wrap to new lines when they overflow (`flex-wrap`); load-bearing for horizontal/Inline (§ wrapping). Off for vertical Stacks (no overflow axis), often **on by default for Inline**.
- **`dividers`** — render Divider between children (boolean or a divider element — MUI `divider`, Chakra `StackDivider`, Braid `dividers`); composes Divider (§11).
- **`as` / `asChild`** — inherited from Box (the polymorphic Slot): render the right element (`as="ul"`/`"ol"`/`"nav"`/`"section"`) for semantics (§6); don't re-derive.
- **per-item flex (the scope question)** — does Stack expose item `grow`/`shrink`/`basis`? Most keep Stack *simple* (direction/gap/align/justify/wrap only) and leave per-item flex to the child (or a **Spacer** — a flexible gap-pusher). The practice default: keep Stack simple; per-item flex is the child's concern.
- **what it withholds** — no margin (the no-external-margin principle — that's the *parent's* gap), no visual chrome (that's Card), no 2D track definition (that's Grid).

## 4. States and variants
- **States: none.** Stack is layout-only — no hover/focus/active/disabled (it inherits Box's statelessness). If it renders an interactive element via `as`/`asChild`, that element carries the states.
- **Variants (axes, not visual variants):**
  - **direction:** vertical (default) / horizontal / responsive (the column→row switch).
  - **with-dividers** vs plain.
  - **wrap** vs no-wrap (horizontal/Inline).
  - **align × justify** combinations (the alignment matrix).
  - **rendered element:** the `as` target (`div`/`ul`/`ol`/`nav`/`section`).

## 5. Usage guidance
- **Use a Stack for:** *any* group of elements laid out along one axis with consistent spacing — form fields, button rows, list items, card bodies, page sections, nav items. It is the **default reach** over a bare Box (the constrained-over-open principle from Box — Stack reveals the layout *intent*; see box).
- **Stack vs the alternatives:**
  - **vs Box** — Box is the neutral, layout-agnostic escape hatch; **reach for Stack first** whenever you're spacing siblings along an axis (a `Box display="flex" gap` by hand is the smell Box warned about; see box).
  - **vs Grid** — Stack is **one** axis (a column *or* a row, even when it wraps); use **Grid** when you need rows *and* columns aligned in two dimensions simultaneously (a true grid of cards, a form with aligned label/field columns — Grid not yet briefed).
  - **vs Inline** (if split) — vertical flow → Stack; horizontal, wrapping flow → Inline. (If one `direction`-prop component, the same call is `direction="row"` + `wrap`.)
- **The recursive model (the load-bearing usage pattern):** build layouts as a **tree of Stacks** — a vertical Stack of horizontal Stacks of vertical Stacks. Whitespace becomes systematic (every gap is a token), and the layout reads as a nesting of one-axis decisions. Most page layouts are a Stack tree with the occasional Grid.
- **The no-margin-on-children rule:** never put `margin` on a Stack's children to adjust spacing — change the Stack's `gap`, or nest another Stack. Margins on children fight the gap and break the systematic-whitespace model (the no-external-margin principle, applied — see box).
- **Don't add chrome to a Stack** — if it needs a background/border/elevation, it's a **Card** (Card not yet briefed).

## 6. Accessibility
Stack inherits Box's a11y story — **a semantically-neutral flex `div` (no role, no name), so the accessibility surface is the element it renders via `as`/`asChild`** (see box). But Stack adds **one sharp, Stack-specific trap**:

- **The DOM-order-vs-visual-order trap (the meaningful-sequence rule).** Flexbox can divorce *visual* order from *DOM* order — `flex-direction: row-reverse`/`column-reverse`, the `order` property, and **wrapping** can all make what the eye sees diverge from what's in the DOM. Screen readers and the **Tab order follow the DOM**, not the visual layout — so a Stack that reverses or reorders its children visually produces a **reading order and focus order that mismatch the visual order**, a **WCAG 1.3.2 (Meaningful Sequence)** and **2.4.3 (Focus Order)** failure. **The rule: Stack must not reorder content visually away from DOM order** — if the visual order should differ, change the *DOM* order (the source), not `row-reverse`/`order`. Reserve `reverse`/`order` for the rare case where the reorder is purely presentational and the sequence carries no meaning (and even then, prefer fixing the source).
- **Semantic wrapping via `as`.** A Stack rendering a *list* of items should be `as="ul"`/`"ol"` with `<li>` children (a navigation Stack `as="nav"`); a Stack of sections `as="section"`. Don't leave a meaningful group as a neutral `div` when an element conveys the relationship (1.3.1 info & relationships — the same as-is-the-whole-story rule as Box).
- **No focus management of its own** — Stack is not focusable and manages no focus; if it renders an interactive element, that element owns the contract.
- **WCAG SCs:** **1.3.2** (meaningful sequence — the no-reorder rule), **2.4.3** (focus order — the same), **1.3.1** (info & relationships — semantic `as`); nothing attaches to a plain layout Stack directly. The light a11y of a layout primitive, with the one real reorder caveat.

## 7. Content guidelines
- Stack **holds layout, not content** — it has no copy of its own (like Box).
- **The list-semantics note** — when a Stack lays out what is *semantically a list* (menu items, tags, search results), render it `as="ul"`/`"ol"` with `<li>` children so the relationship and the item count reach assistive tech; don't fake a list visually as a stack of `<div>`s (it reads as unrelated content).
- **Don't fake structure visually** — if the spacing implies a grouping or a sequence that carries meaning, encode it (`as`, a heading, list semantics), don't leave it as visual-only whitespace.

## 8. Motion and transition
- Stack ships **no motion of its own** (like Box) — it's a layout container.
- **The reflow/reorder animation** — when items are added/removed/reordered in a Stack, the siblings reflow to the new `gap`-spaced positions; a **FLIP** animation (First-Last-Invert-Play) smooths the reflow (the same technique Tag's group reflow uses — see tag), applied by the consumer or an animation primitive composed via `asChild`, not by Stack itself.
- **Reduce-motion** — the consumer's concern on any reflow animation they attach; Stack is motion-neutral.

## 9. Internationalization
- **The gap is direction-agnostic** (a symmetric token rhythm), so it needs no RTL handling.
- **A horizontal Stack's main axis flips under RTL** — the first item moves to the right in RTL; flexbox `flex-direction: row` already mirrors with `dir="rtl"` (and `row-reverse` should be avoided — §6), and Box's logical-property mapping (inherited) handles any directional offsets, so a horizontal Stack flips with **zero JS**.
- **Logical-axis naming is the RTL-correct model** — Polaris's **`BlockStack`/`InlineStack`** (block = the vertical/cross axis, inline = the text-flow axis) names the axes *logically*, which is inherently direction-correct; physical names (Vertical/Horizontal, row/column) are fine if they map to logical properties underneath. The practice should prefer logical semantics even if it keeps familiar names.
- **Vertical Stacks are RTL-neutral** (the block axis doesn't flip for RTL — it flips for vertical writing modes, which logical properties also handle).

## 10. Naming
- **The field set:** **`Stack`** + a `direction` prop (MUI, Carbon, Primer); **`VStack`/`HStack`** (Chakra — physical, two components); **`Stack`** (vertical) + **`Inline`** (horizontal) (Braid, Atlassian — intent-revealing); **`BlockStack`/`InlineStack`** (Polaris — *logical* axis, RTL-correct); **`Flex`** (Radix Themes, Spectrum, React Aria — names the CSS mechanism, a more general flex primitive with `direction`).
- **The practice's default — one `Stack` with a `direction` prop, defaulting to vertical**, because the **responsive-direction switch** (`direction={{ base: 'column', md: 'row' }}`) is a first-class need that two separate components (VStack/HStack, Stack/Inline) handle awkwardly (you'd swap components across breakpoints). Prefer **logical axis values** under the hood (so RTL is correct) even while exposing familiar `row`/`column` (or, following Polaris, expose `block`/`inline`). The intent-revealing two-component split (Stack/Inline) is the valid alternative for systems that don't need responsive direction and prize legibility.
- **`gap` over `spacing`** — name the prop after the CSS property it sets (`gap`), not the legacy `spacing` (MUI's term from the margin era).
- **`Flex` is the more general primitive** — if a system wants raw flexbox (per-item flex, all the alignment knobs), `Flex` is a reasonable lower-level layer between Box and Stack; Stack is the *opinionated, gap-first* subset. The practice can ship Stack alone and treat raw flex as a Box escape hatch.
- **Aliases to map:** VStack, HStack, Inline, BlockStack, InlineStack, Flex, FlexStack, Row/Column.

## 11. Implementation notes
- **Flex `gap` over the lobotomized owl (and the Safari 14.1 inflection).** Modern Stack is `display: flex; flex-direction: …; gap: <token>`. This was only viable after **flexbox `gap` shipped in Safari 14.1 (~April 2021)** — before that, Stacks used the **lobotomized owl** (`& > * + * { margin-block-start: <token> }` — margin on all-but-the-first child) or margin-bottom + a negative wrapper margin. The owl is the legacy fallback (and still appears in systems supporting old Safari); the modern default is `gap`. *Date this — it's why old Stack code carries margin hacks.*
- **The direction prop + responsive direction** — `flex-direction` from the `direction` prop, with the responsive object generating per-breakpoint `flex-direction` (inherits Box's responsive syntax — object over array; see box). The responsive switch is the implementation argument for one component over two.
- **`align`/`justify` mapping** — `align` → `align-items` (cross), `justify` → `justify-content` (main); the names abstract the flex axis so the consumer doesn't track which is which per direction (a Stack's `align` is always "the cross axis," regardless of vertical/horizontal).
- **Wrap + two-axis gap** — `wrap` → `flex-wrap: wrap`; the win of flex `gap` here is that it applies to **both** axes (row-gap *and* column-gap) on a wrapped Inline, so wrapped lines get the same spacing — clean in a way the margin era never was (margins double up or need `:last-child` resets across wrapped lines).
- **The divider-between (n−1, composing Divider)** — interleave a Divider *between* children, never around: for n children render n−1 dividers (`children.flatMap((c, i) => i ? [<Divider/>, c] : [c])`); the divider inherits the Stack's direction (a vertical Stack → horizontal dividers, a horizontal Stack → vertical dividers — see divider for the orientation). Don't render a divider before the first or after the last child.
- **The no-reorder enforcement** — avoid `flex-direction: *-reverse` and the `order` property for anything sequence-meaningful; the no-reorder discipline is a lint/review rule, not a runtime one (§6).
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime styling delivery, and the logical-property RTL all come from Box (see box); Stack adds only the flex + gap + direction + align/justify + wrap + dividers delta.
- **Headless vs opinionated** — Stack is a thin, opinionated layer on flexbox + the token scale; there's little headless logic (no state, no a11y machinery beyond `as`). Ship it as a styled layout primitive; the value is the constrained, token-bound, intent-revealing API over raw flex.

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, the logical-property RTL — all inherited; see box).
- **The answer to:** Box's **no-external-margin principle** — Stack owns the inter-sibling gap so children never carry margins (see box).
- **Composes:** **Divider** (the divider-between-children, n−1 separators inheriting the Stack's direction — see divider).
- **1D sibling of:** **Grid** (the 2D engine — Stack is one axis, Grid is rows × columns; reach for Grid when you need two-dimensional alignment — Grid not yet briefed).
- **Composed by / nested:** **Card** (the card body is a Stack — Card not yet briefed), forms, lists, nav, and **recursively** (a Stack of Stacks — the layout tree).
- **Alternative to / boundary with:** a bare **Box** (`display="flex"` by hand — the smell Stack replaces), a **Spacer** (a flexible gap-pusher for the one-off push-apart, vs Stack's uniform gap), and **flex utility classes** (Tailwind's `flex gap-4` — the no-Stack-component position).

(The first Layout engine — the 1D flexbox component that owns the gap, the answer to Box's no-external-margin principle. It stands on Box (inheriting the Slot, the scale, the RTL), composes Divider (the divider-between), is the 1D sibling of Grid, and is nested recursively into the layout tree. See box for the substrate, divider for the divider-between, grid/card/section when briefed for the sibling + the hosts, tag for the FLIP reflow it shares. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **The lobotomized owl → flex `gap` (the Safari 14.1 inflection).** Stacks were built on margin hacks (`* + *`, margin-bottom + negative wrapper margins) until flexbox `gap` shipped across browsers (Safari 14.1, ~2021); `gap` then became the clean, two-axis-correct default, and "Stack owns the gap" became literally true rather than a margin simulation.
2. **The no-margin principle making Stack canonical.** As the field hardened the rule that components don't own their external margin (Box), Stack became *the* answer — the designated owner of inter-sibling space — moving from a convenience to a foundational layout primitive.
3. **Logical-axis naming for RTL.** Polaris's `BlockStack`/`InlineStack` named the axes *logically* (block/inline) rather than physically (vertical/horizontal), making RTL and vertical-writing-mode correctness inherent rather than bolted on.
4. **The DOM-order-vs-visual-order a11y settling.** The recognition that flexbox `reverse`/`order`/wrap can break meaningful sequence (1.3.2) and focus order (2.4.3) hardened the no-reorder discipline — change the DOM, not the visual order.
5. **The Stack-tree mental model.** "Build every layout as a tree of Stacks (with the occasional Grid)" became the dominant authoring model, displacing ad-hoc margins and floats — whitespace as a systematic, token-bound, nested decision.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Chakra UI — `Stack` / `VStack` / `HStack` (`spacing`→`gap`, `StackDivider`, `align`/`justify`).
- MUI — `Stack` (`direction`, `spacing`, `divider`, `useFlexGap`).
- Braid / Seek — `Stack` (vertical) + `Inline` (horizontal), `dividers` (the no-margin origin).
- Radix Themes — `Flex` (`direction`/`align`/`justify`/`gap`/`wrap` — the Flex-not-Stack naming).
- Shopify Polaris — `BlockStack` / `InlineStack` (the logical-axis naming, `gap`, `align`).
- GitHub Primer — `Stack` + `PageLayout`.
- Adobe Spectrum / React Aria — `Flex` (the layout component).
- IBM Carbon — `Stack` (`gap`, `orientation`).
- Atlassian — `Stack` / `Inline` (`@atlaskit/primitives` — Box+Stack+Inline+Flex with `xcss`).
- Tailwind — `flex` + `gap` utilities (the no-Stack-component position).
- Base Web (Uber) — the flex/block layout primitives.
- WAI-ARIA / HTML — Stack is a semantically-neutral flex `div` (no role); the DOM-order-vs-visual-order meaningful-sequence trap.
- WCAG 2.2 — 1.3.2, 2.4.3, 1.3.1.
- CSS — flexbox `gap` browser support (Safari 14.1, ~April 2021).

## 15. Agent-consumable schema
```yaml
identity:
  id: stack
  name: Stack
  aliases: [VStack, HStack, Inline, BlockStack, InlineStack, Flex, FlexStack, Row, Column]
  category: layout
  status: stable
description: >
  The one-dimensional (flexbox) layout engine — arranges children along a single axis
  (vertical by default) with a uniform, token-scaled GAP between them. The second
  Layout brief and the answer to Box's no-external-margin principle: Stack OWNS THE
  SPACE BETWEEN SIBLINGS via gap, so children never carry margins ('the component that
  owns the gap'). NOT a Box (the neutral, layout-agnostic substrate — Stack IS the
  opinion: flex + gap + direction), NOT a Grid (the 2D engine — Stack is one axis even
  when it wraps). Stands on Box (the as/asChild Slot, the spacing-token scale, the
  styling delivery, the logical-property RTL); composes Divider (the divider-between);
  the 1D sibling of Grid; composed by Card/forms/lists/nav and nested recursively.
anatomy:
  parts:
    - "the flex container: display:flex + flex-direction (column default) + gap; a semantically neutral div (inherits Box's neutrality)"
    - "the gap: the uniform space BETWEEN children (not around — that's the parent's padding), resolving against Box's spacing-token scale; the defining 'part' though it's whitespace"
    - "children as flex items: the content Stack arranges; mostly unstyled by Stack (the per-item-flex question)"
    - "optional dividers-between: interleaved separators composing Divider — n-1 for n children (between, never around)"
    - "(absence of) visual chrome: no background/border/radius/elevation (that's Card); pure layout"
api:
  inherits:
    - box        # the as/asChild Slot, the spacing-token scale (gap resolves against it), the zero-runtime delivery, the logical-property RTL
  composes:
    - divider    # the divider-between-children (n-1, inherits the Stack's direction)
  props:
    - {name: direction/orientation, type: "'vertical'|'horizontal' | responsive", default: vertical, required: false, description: "the axis; responsive (direction={{base:'column',md:'row'}}) is the killer arg for ONE component over two; prefer LOGICAL values for RTL"}
    - {name: gap/spacing, type: "token-scale", default: ~, required: false, description: "the inter-child space, a token index (gap={4} -> 4th spacing token); 'gap' (CSS-matching) preferred over legacy 'spacing'"}
    - {name: align, type: "'start'|'center'|'end'|'stretch'", default: "stretch (vertical) / center (horizontal) — resolve per direction", required: false, description: "CROSS-axis (align-items)"}
    - {name: justify, type: "'start'|'center'|'end'|'space-between'|'space-around'|'space-evenly'", default: start, required: false, description: "MAIN-axis (justify-content)"}
    - {name: wrap, type: boolean, default: "off (vertical) / often on (Inline/horizontal)", required: false, description: "flex-wrap; load-bearing for horizontal — wrapped lines get the SAME gap (two-axis)"}
    - {name: dividers, type: "boolean | element", default: false, required: false, description: "render Divider between children (MUI divider, Chakra StackDivider, Braid dividers)"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — render the right element (ul/ol/nav/section) for semantics"}
  per-item-flex: "the scope question — most keep Stack SIMPLE (direction/gap/align/justify/wrap only) and leave grow/shrink/basis to the child or a Spacer; practice default: keep it simple"
  withholds: "no margin (parent's gap), no chrome (Card), no 2D tracks (Grid)"
states:
  runtime: []   # NONE — layout-only, inherits Box's statelessness; an interactive element via as/asChild carries the states
variants:
  direction: [vertical, horizontal, responsive]
  dividers: [plain, with-dividers]
  wrap: [no-wrap, wrap]
  alignment: "align (cross) x justify (main) combinations"
  rendered-element: "the as target (div/ul/ol/nav/section)"
accessibility:
  inherits: [box (semantically-neutral div; the element it renders via as is the whole story)]
  wcag-criteria: ["1.3.2", "2.4.3", "1.3.1"]
  DOM-vs-visual-order-trap: "the Stack-specific crux — flex row-reverse/column-reverse/order/WRAP can divorce VISUAL order from DOM order; SR + Tab order follow the DOM, so a reordered Stack mismatches reading/focus order (WCAG 1.3.2 Meaningful Sequence + 2.4.3 Focus Order). RULE: Stack must NOT reorder visually away from DOM order — change the DOM (the source), not row-reverse/order; reserve reverse/order for purely-presentational no-meaning sequences"
  semantic-as: "a Stack laying out a LIST -> as='ul'/'ol' + <li> children (nav -> as='nav'); don't leave a meaningful group a neutral div (1.3.1)"
  focus: "not focusable, manages no focus; an interactive rendered element owns its contract"
content:
  holds-layout-not-content: "no copy of its own (like Box)"
  list-semantics: "a Stack of semantically-list items (menu/tags/results) -> as='ul'/'ol' + <li> so the relationship + count reach AT; don't fake a list as a stack of divs"
  no-fake-structure: "if spacing implies a meaningful grouping/sequence, encode it (as/heading/list), don't leave it visual-only"
motion:
  own: none   # a layout container, ships no animation
  reflow: "items add/remove/reorder -> siblings reflow to new gap-spaced positions; FLIP smooths it (same as Tag's group reflow), applied by the consumer/an animation primitive via asChild, not Stack"
  reduce-motion: "the consumer's concern on any attached reflow animation; Stack is motion-neutral"
i18n:
  gap-direction-agnostic: "the gap is a symmetric token rhythm — no RTL handling needed"
  horizontal-flips: "a horizontal Stack's main axis flips under RTL — flex-direction:row already mirrors with dir=rtl (avoid row-reverse); Box's logical-property mapping handles offsets — zero JS"
  logical-axis-naming: "Polaris BlockStack/InlineStack (block=cross/vertical, inline=text-flow) is the RTL-correct model; physical names fine if they map to logical underneath — prefer logical semantics"
  vertical-rtl-neutral: "vertical Stacks don't flip for RTL (block axis); they flip for vertical writing modes, which logical properties handle"
implementation:
  - "flex GAP over the lobotomized owl (the Safari 14.1 inflection): modern Stack = display:flex + flex-direction + gap:<token>; only viable after flexbox gap shipped in Safari 14.1 (~Apr 2021). Before: the lobotomized owl (& > * + * {margin-block-start}) or margin-bottom + negative wrapper margin (the legacy fallback). DATE IT — it's why old Stack code carries margin hacks"
  - "direction prop -> flex-direction; responsive object -> per-breakpoint flex-direction (inherits Box's object-over-array syntax); the responsive switch is the arg for one component over two"
  - "align -> align-items (cross), justify -> justify-content (main); the names abstract the axis so align is always 'the cross axis' regardless of direction"
  - "wrap -> flex-wrap:wrap; flex gap's win: it applies to BOTH axes (row + column gap) on a wrapped Inline, so wrapped lines get the same spacing (the margin era couldn't do this cleanly)"
  - "divider-between (n-1, composing Divider): interleave between children never around (children.flatMap((c,i)=> i?[<Divider/>,c]:[c])); the divider inherits the Stack's direction (vertical Stack -> horizontal dividers); none before first / after last"
  - "no-reorder enforcement: avoid flex *-reverse + the order property for sequence-meaningful content (a lint/review rule, not runtime)"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Stack adds only the flex+gap+direction+align/justify+wrap+dividers delta"
  - "headless vs opinionated: a thin opinionated layer on flexbox + the token scale (no state, no a11y machinery beyond as); ship as a styled layout primitive — the value is the constrained, token-bound, intent-revealing API over raw flex"
composition:
  stands-on: [box]
  answer-to: "box's no-external-margin principle (Stack owns the inter-sibling gap)"
  composes: [divider]
  sibling-of: [grid]                       # 1D vs 2D (not yet briefed)
  composed-by: [card, "forms", "lists", "nav"]   # + recursively (the Stack-of-Stacks layout tree)
  alternative-to: ["bare Box display=flex (the smell Stack replaces)", spacer, "flex utility classes (Tailwind no-Stack position)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "ONE Stack + direction prop (MUI — the practice default, for the responsive-direction switch) vs TWO components (Chakra VStack/HStack; Braid Stack/Inline; Polaris BlockStack/InlineStack)"
    - "LOGICAL (Block/Inline — Polaris, RTL-correct) vs PHYSICAL (Vertical/Horizontal, row/column) axis naming"
    - "the align default per direction (stretch makes vertical children full-width vs start = intrinsic)"
    - "gap vs spacing prop naming (practice: gap, matching CSS)"
    - "expose per-item flex (grow/shrink) vs keep Stack simple + a Spacer (practice: keep simple)"
    - "Stack vs Flex naming (Flex = the more general lower-level primitive; Stack = the gap-first opinionated subset)"
  trap:
    - "the DOM-order-vs-visual-order trap: row-reverse/order/wrap diverging visual from DOM/reading/tab order (WCAG 1.3.2 + 2.4.3) — change the DOM not the visual order"
    - "putting margin on a Stack's children to adjust spacing (fights the gap; change gap or nest a Stack — the no-external-margin principle)"
    - "adding chrome (bg/border/elevation) to a Stack (that's a Card)"
    - "faking a list visually as a stack of divs without as='ul'/li (loses the relationship + count)"
    - "the lobotomized-owl margin hack in modern code (use flex gap); a divider before the first / after the last child (n-1 between only)"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL, the semantically-neutral-div a11y"
  role-in-family: "the first Layout engine — the 1D flexbox component that owns the gap, the answer to Box's no-external-margin principle; stands on Box, composes Divider, the 1D sibling of Grid, nested recursively into the layout tree"
  evolution:
    - "the lobotomized owl (* + * margin) -> flex gap (the Safari 14.1/~2021 inflection) -> Stack-owns-the-space"
    - "the no-margin principle making Stack canonical (the designated owner of inter-sibling space)"
    - "logical-axis naming (Polaris Block/Inline) for RTL/writing-mode correctness"
    - "the DOM-order-vs-visual-order a11y settling (the no-reorder rule)"
    - "the Stack-tree mental model (build layouts as a tree of Stacks + the occasional Grid)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the exact Safari flex-gap version/date (14.1, ~April 2021) — verify"
    - "per-system align defaults + the gap-vs-spacing naming state"
```

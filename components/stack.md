---
okf_version: "0.1"
type: component-brief
title: Stack
description: The 1D flexbox layout engine that owns the gap — a field-truth study of the gap mechanism + the flex-gap inflection (the Heydon-Pickering lobotomized-owl history, the @supports feature-detection trap, the Safari 14.1 / April 2021 inflection), the direction question + the naming morass (one direction-prop vs VStack/HStack vs Stack/Inline vs Polaris's logical BlockStack/InlineStack) decided by the responsive-direction switch + the React remount/state-loss argument, the align/justify matrix + the stretch-default question, the wrap + two-axis-gap (rowGap/columnGap) interaction + the divider+wrap incompatibility, the DOM-order-vs-visual-order meaningful-sequence a11y trap (the no-reorder rule; reverse the node array not the CSS), and the recursive Stack-of-Stacks layout tree — standing on Box and composing Divider, with the practice's defaults.
tags: [components, layout]
category: Layout
status: stable
aliases: [VStack, HStack, Inline, BlockStack, InlineStack, Flex, FlexStack, Row, Column]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Stack

> A Stack is the **one-dimensional (flexbox) layout engine** — it arranges children along a single axis (vertical by default) with a uniform, token-scaled **gap** between them. It is the second Layout brief after Box, and the component the **no-external-margin principle most directly implies**: Box established that components must not own their external margin (a button with a baked-in `margin-right` fractures the moment it lands in a modal or a table cell); Stack is the canonical mechanism that **owns the space between siblings** via `gap`, so children stay flush and portable. That is the load-bearing thesis — **Stack is the component that owns the gap**. It stands on **Box** (inheriting the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, and the logical-property RTL mapping — all inherited, not re-derived; see box), composes **Divider** (the divider-between-children, n−1 separators; see divider), is the **1D sibling of Grid** (the 2D engine — not yet briefed), and is composed by Card, forms, lists, and nav, nested recursively (a Stack of Stacks). Three things define it: **the gap mechanism + the flex-gap inflection** (CSS flexbox `gap`, viable only since Safari 14.1 / ~April 2021 — before which Stacks used the "lobotomized owl" margin hack), **the direction question + the naming morass** (one `direction`-prop component vs VStack/HStack vs Stack/Inline vs logical BlockStack/InlineStack), and **the DOM-order-vs-visual-order a11y rule** (flexbox can divorce visual from reading/focus order — the no-reorder discipline). What it *isn't*: a **Box** (the neutral, layout-agnostic substrate — Stack *is* the opinion: flex + gap + a direction) or a **Grid** (the 2D engine — Stack is one axis even when it wraps).

---

## 1. Framing
A Stack introduces an inherently *relational* paradigm over Box's single-node neutrality: where Box is a semantically-neutral container, Stack defines the spatial rules of engagement *between* two or more children along one continuous axis. It fulfils the no-external-margin mandate by asserting total ownership of the **interstitial** space — children require **zero contextual awareness of their siblings**, which is exactly what makes them portable.

Three defining concerns, each a place systems diverge:
- **The gap mechanism + the flex-gap inflection.** Stack owns inter-child space via CSS flexbox `gap`, resolving against Box's spacing-token scale so the layout rhythm stays consistent with type and padding. This is *recent*: flexbox `gap` only shipped across all engines with **Safari 14.1 (macOS Big Sur / iOS 14.5, ~April 2021)** — before which Stacks emulated it with the **"lobotomized owl"** (`* + *` margin, Heydon Pickering 2014) or margin + negative-wrapper hacks. The inflection is why "Stack owns the gap" is now literally true rather than a margin simulation, and why legacy Stack code still carries margin hacks.
- **The direction question + the naming morass.** One `Stack` with a `direction` prop (MUI, Primer, Carbon), two physical components (Chakra `VStack`/`HStack`), the intent-revealing split (Braid `Stack`/`Inline`), the logical split (Polaris `BlockStack`/`InlineStack`), or the general flex primitive (Radix Themes / Spectrum `Flex`). The **responsive-direction switch** usually decides it (§10).
- **The DOM-order-vs-visual-order a11y rule.** Stack is layout-only and semantically neutral, but flexbox can decouple *visual* order from *DOM* order — a real WCAG trap (§6).

What it *isn't*: a **Box** (reach for Stack whenever spacing siblings along an axis — a `Box display="flex"` by hand is the smell Box warned about; see box) or a **Grid** (when you need rows *and* columns aligned in two dimensions simultaneously, not a single wrapping axis). Why systems disagree: the direction/naming model, the align/justify defaults, and whether to expose per-item flex.

## 2. Anatomy and parts
Stack is an invisible structural orchestrator — no background, border, radius, or elevation of its own (that's Card); its parts are spatial, not decorative:
- **the flex container** — a block-level node establishing a flex formatting context; all immediate children become flex items, subjugating their sizing/positioning to the Stack. Semantically a neutral `div` (inherits Box's neutrality — §6).
- **the gap** — the strictly-measured whitespace *between* flex items (not around them — that's the parent's padding), mapping to the spacing-token scale. The defining "part," though it's whitespace; the Stack owns it so children need no margins.
- **the children as flex items** — the content Stack arranges; mostly unstyled by Stack (the per-item-flex question — §3).
- **the optional dividers-between** — programmatically injected separators composing Divider (see divider): for n children, exactly **n−1** dividers (between, never around), rendered across the cross-axis (vertical lines in a horizontal Stack, horizontal lines in a vertical Stack — §11).
- **the polymorphic slot** — inherited from Box: the container renders a `div` by default but can be cast `as` a `ul`/`ol`/`nav`/`section`/`fieldset` for semantics, without altering the flex mechanics (§6).

## 3. Properties / API
A curated, strongly-typed subset of the CSS Box Alignment Module — tokens and predictable keywords over raw CSS strings:
- **`direction` / `orientation`** (or the two-component split) — the main axis: vertical (default) / horizontal; **responsive** (`direction={{ base: 'column', md: 'row' }}` → `flex-direction`). The headline decision (§10); prefer **logical** values for RTL-correctness.
- **`gap` / `spacing`** — the inter-child space, a token-scale index (`gap={4}` → the 4th spacing token), resolving against Box's scale. The defining prop; the field is converging on **`gap`** (matching the CSS property) over the legacy `spacing` (MUI's margin-era term). For wrapped layouts needing distinct gutters, expose **`rowGap`/`columnGap`** (§11).
- **`align`** — **cross-axis** alignment (`align-items`): start / center / end / **stretch**. **The stretch-default question:** CSS defaults `align-items: stretch`, which forces children to fill the cross-axis — a button can warp to a multi-line neighbour's height. Many mature systems override the default to **`start`** to prevent the warp, requiring an explicit opt-in to stretch. (Resolve per direction.)
- **`justify`** — **main-axis** distribution (`justify-content`): start / center / end / space-between / space-around / space-evenly.
- **`wrap`** — `flex-wrap`; load-bearing for horizontal/Inline (overflow → new lines); off for vertical Stacks, often **on by default for Inline** (tag groups, galleries).
- **`dividers`** — render Divider between children (boolean or element — MUI `divider`, Chakra `StackDivider`, Braid `dividers`); composes Divider (§11). **Incompatible with `wrap`** (§11).
- **`as` / `asChild`** — inherited from Box (the polymorphic Slot): render the right element (`ul`/`ol`/`nav`/`section`) for semantics (§6).
- **per-item flex (the scope question)** — does Stack expose item `grow`/`shrink`/`basis`? Most keep Stack *simple* (direction/gap/align/justify/wrap only) and leave per-item flex to the child (or a **Spacer** — a `flex-grow` node that absorbs free space to push sibling clusters apart). The practice default: keep Stack simple.
- **the alignment-prop naming fork** — `align`/`justify` (concise, axis-abstracted — Chakra/Radix Themes/Braid) vs the full native `alignItems`/`justifyContent` (lower cognitive friction for CSS-fluent devs — MUI/Spectrum). The practice leans **`align`/`justify`** (concise, and `align` always means "the cross axis" regardless of direction — §11); the native-CSS naming is the valid alternative.
- **what it withholds** — no margin (the parent's gap), no visual chrome (Card), no 2D tracks (Grid).

## 4. States and variants
- **States: none.** Stack lacks interaction states (no hover/focus/active/disabled; inherits Box's statelessness) and responds to no pointer/keyboard events directly. An interactive element rendered via `as`/`asChild` carries the states.
- **Variants (structural, dictated by the layout-prop matrix):**
  - **direction:** vertical (column block — page structure, document flow) / horizontal (toolbars, nav, pagination, inline groups) / responsive (the column→row switch).
  - **wrap** vs no-wrap (the horizontal multiline case — tag groups, galleries; introduces the two-axis-gap calculation).
  - **with-dividers** vs plain — *single-line only* (the divider+wrap incompatibility — §11).
  - **align × justify** combinations (the alignment matrix).
  - **rendered element:** the `as` target (`div`/`ul`/`ol`/`nav`/`section`/`fieldset`).

## 5. Usage guidance
- **Use a Stack for:** *any* group of elements flowing along one axis with consistent spacing — form fields, button rows, list items, card bodies, page sections, nav, toolbars, pagination. It is the **default reach** over a bare Box (the constrained-over-open principle — Stack reveals the layout intent; see box).
- **The no-margin-on-children rule (strict):** never apply `margin-top`/`margin-left` to a Stack's children to adjust spacing — components stay **flush**, relying exclusively on the parent's `gap`. Change the `gap`, or nest another Stack. This keeps components portable and whitespace systematic (the no-external-margin principle, applied — see box).
- **Stack vs the alternatives:**
  - **vs Box** — Box is the neutral, layout-agnostic escape hatch; reach for Stack first whenever spacing siblings along an axis (see box).
  - **vs Grid** — Stack is **one** axis (a column *or* a row, even when it wraps); use **Grid** when elements must align to rows *and* columns simultaneously regardless of content size. Forcing a Stack to behave like a grid (fixed percentage widths + flex wrap) is extremely fragile across viewports (Grid not yet briefed).
  - **vs Inline** (if split) — vertical flow → Stack; horizontal wrapping flow → Inline (or `direction="row"` + `wrap`).
- **The recursive model (the load-bearing pattern):** build layouts as a **tree of Stacks** — a vertical page-level Stack containing horizontal card-level Stacks containing vertical text-level Stacks. The "Stack of Stacks" reinforces that whitespace is managed through a rigorous parent-child hierarchy, not ad-hoc component margins. Most layouts are a Stack tree with the occasional Grid.
- **Don't add chrome to a Stack** — if it needs a background/border/elevation, it's a **Card** (not yet briefed).

## 6. Accessibility
Stack inherits Box's a11y story — **a semantically-neutral flex `div` (no role, no name), so the accessibility surface is the element it renders via `as`/`asChild`** (see box). It adds **one sharp, Stack-specific trap**:

- **The DOM-order-vs-visual-order trap (the meaningful-sequence rule).** The flexbox spec lets visual rendering fully decouple from the DOM: `flex-direction: row-reverse`/`column-reverse`, the `order` property, and **wrapping** can all make what the eye sees diverge from the DOM sequence. A screen reader parses the DOM (announcing items in their original, unreversed order); a keyboard user's Tab follows the DOM (the focus indicator jumps erratically against the visual flow). That violates **WCAG 1.3.2 (Meaningful Sequence)** — sequence affecting meaning must be programmatically determinable — and **WCAG 2.4.3 (Focus Order)** — focus order must match the logical/operable meaning. **The rule (the no-reorder discipline):** `reverse`/`order` are deprecated/linted-against/banned in primary layout primitives; if a visual reversal is genuinely required (e.g., moving a primary action to the top of a stack on mobile), **reverse the node array programmatically before DOM injection** so the visual order, the screen-reader sequence, and the tab order stay permanently synchronized. Change the *source*, not the CSS.
- **Semantic wrapping via `as`.** A Stack laying out a *list* should be `as="ul"`/`"ol"` with `<li>` children (a nav Stack `as="nav"`), so the screen reader gets the item count and the grouping relationship; a Stack of sections `as="section"`. Don't leave a meaningful group a neutral `div` (1.3.1 info & relationships).
- **No focus management of its own** — Stack is not focusable and manages no focus; an interactive rendered element owns its contract.
- **WCAG SCs:** **1.3.2** (meaningful sequence — the no-reorder rule), **2.4.3** (focus order — the same), **1.3.1** (info & relationships — semantic `as`). The light a11y of a layout primitive, with the one real reorder caveat.

## 7. Content guidelines
- Stack is **strictly an architectural mechanism** — devoid of content logic; it holds layout elements, not intrinsic data, and dictates no typography/color/iconography of its own (like Box).
- **Don't visually emulate semantics without the markup** — a vertical Stack of text nodes that *looks* like a list but isn't `as="ul"`/`<li>` reads to a screen reader as an arbitrary sequence of text with no indication it's a cohesive list (no count, no relationship). The structural presentation must always map to semantic markup via `as` — the visual grouping matches the programmatic grouping.

## 8. Motion and transition
- Stack ships **no motion of its own** — gap calculation and flex distribution execute instantly during layout/paint.
- **The reflow/reorder animation** — when items are added/removed/reordered, the siblings reflow to the new gap-spaced positions; animate it with **FLIP** (First-Last-Invert-Play): capture the initial and final geometry and bridge with hardware-accelerated `transform` (translate/scale), *not* by animating `width`/`margin`/`gap` directly (which forces expensive reflows). The same technique Tag's group reflow uses (see tag), applied by the consumer or an animation primitive composed via `asChild` — not by Stack itself.
- **Reduce-motion** — any wrapping animation library must intercept `prefers-reduced-motion: reduce` and revert to instant layout; Stack is motion-neutral.

## 9. Internationalization
- **The gap is direction-agnostic** (a symmetric token rhythm) — no RTL handling needed.
- **A horizontal Stack's main axis flips under RTL natively** — `dir="rtl"` at the document root commands the flexbox engine to reverse the visual flow of the main axis: the first item sits on the far right, subsequent items flow left, and the `gap` (intrinsically logical) applies along the dynamically-determined axis — **no JS, no RTL-specific CSS overrides** (and `row-reverse` is avoided — §6). Box's logical-property mapping (inherited) handles any directional offsets.
- **Logical-axis naming is the RTL-correct model** — Polaris's **`BlockStack`/`InlineStack`** (block = the stacking/vertical axis, inline = the text-flow/reading axis) names the axes *logically*, so the vocabulary inherently respects the localized direction; physical names (`row`/`column`, Vertical/Horizontal) are fine if they map to logical properties underneath. The field is moving away from rigid physical terminology toward logical — the practice should prefer logical semantics.
- **Vertical Stacks are RTL-neutral** (the block axis doesn't flip for RTL; it flips for vertical writing modes, which logical properties also handle).

## 10. Naming
- **The field set:** **`Stack`** + a `direction` prop (MUI, Primer — physical; Carbon); **`VStack`/`HStack`** (Chakra — physical, two components); **`Stack`**/**`Inline`** (Braid, Atlassian — intent-revealing); **`BlockStack`/`InlineStack`** (Polaris — *logical*, RTL-correct; + the `<s-stack>` web component); **`Flex`** (Radix Themes, Spectrum, React Aria — names the CSS mechanism, the general flex primitive with `direction`).
- **The practice's default — one `Stack` with a `direction` prop, defaulting to vertical**, decided by two arguments:
  1. **The responsive-direction switch** (`direction={{ base: 'column', md: 'row' }}`) — a first-class need that two separate components handle awkwardly.
  2. **The React remount/state-loss argument (the decisive one):** a two-component split (VStack↔HStack) can't fluidly transition across breakpoints — React can't swap one component *type* for another without destroying and remounting the DOM node, **losing local state**. Two-component systems work around this with conditional render logic or proprietary props (Braid's `collapseBelow`); one component with a responsive `direction` array sidesteps it entirely.
  Prefer **logical axis values** under the hood (RTL-correct) even while exposing familiar `row`/`column` (or, following Polaris, `block`/`inline`). The intent-revealing two-component split (Stack/Inline) is the valid alternative for systems that don't need responsive direction.
- **`gap` over `spacing`** — name the prop after the CSS property, not MUI's margin-era `spacing`.
- **`align`/`justify` vs `alignItems`/`justifyContent`** — the practice leans concise `align`/`justify`; native CSS names are the valid alternative (§3).
- **`Flex` is the more general lower-level primitive** — a reasonable layer between Box and Stack for raw flexbox; Stack is the *gap-first, opinionated* subset. The practice can ship Stack alone and treat raw flex as a Box escape hatch.
- **Aliases to map:** VStack, HStack, Inline, BlockStack, InlineStack, Flex, FlexStack, Row, Column.

## 11. Implementation notes
- **Flex `gap` over the lobotomized owl (the Safari 14.1 inflection).** Modern Stack is `display: flex; flex-direction: …; gap: <token>`. This was only viable after flexbox `gap` shipped in **Safari 14.1 (macOS Big Sur / iOS 14.5, ~April 2021)** — grid `gap` had shipped in 2018, but WebKit delayed *flex* gap. Before that, Stacks used the **lobotomized owl** (`& > * + * { margin-block-start: <token> }` — Heydon Pickering, 2014; margin on all-but-the-first child) or margin-bottom + negative wrapper margins. The owl broke on **wrapped** layouts (a uniform adjacent margin produces jagged edges the moment items flow to a new line) and fought high-specificity cascades — which is why `gap` obsoleted it. **The `@supports` trap:** you *cannot* feature-detect flex gap with `@supports (gap: 1em)` — the browser returns `true` based on *grid* gap support, so detection is unreliable; systems gated on version, not feature query. MUI shipped a **`useFlexGap`** opt-in to migrate consumers off its legacy nested-selector spacing without a hard break. The owl remains the legacy fallback only for ancient-Safari support. *Date this — it's why old Stack code carries margin hacks.*
- **The direction prop + responsive direction** — `flex-direction` from `direction`; the responsive object generates per-breakpoint `flex-direction` (inherits Box's object-over-array syntax; Radix Themes compiles the responsive object to CSS custom properties so breakpoint shifts are the browser's job, not runtime JS). The responsive switch + the remount argument decide one component over two (§10).
- **`align`/`justify` mapping** — `align` → `align-items` (cross), `justify` → `justify-content` (main); the names abstract the axis so `align` is *always* "the cross axis" regardless of direction. Consider overriding the CSS `stretch` default to `start` (§3).
- **Wrap + two-axis gap** — `wrap` → `flex-wrap: wrap`; flex `gap`'s win is it applies to **both** axes (row-gap *and* column-gap) on a wrapped Inline, so wrapped lines get the same spacing — clean where the margin era couldn't be (margins double up / need `:last-child` resets across wrapped lines). Expose **`rowGap`/`columnGap`** when distinct gutters are needed.
- **The divider-between (n−1, composing Divider) — and the wrap incompatibility.** Intercept `children`, map over valid nodes, inject a Divider *between* each (`children.flatMap((c, i) => i ? [<Divider/>, c] : [c])`) → 2n−1 total items; the divider inherits the Stack's direction (vertical Stack → horizontal dividers; see divider); none before the first / after the last. **Dividers are structurally incompatible with `flex-wrap`:** a wrapped line treats the divider as a normal flex item, so it can render orphaned at a line's start/end and destroy the rhythm — high-quality implementations **warn against or disable dividers when `wrap` is active**.
- **The no-reorder enforcement** — avoid `flex-direction: *-reverse` and `order` for sequence-meaningful content; reverse the node *array* before injection if a visual reversal is needed (§6). A lint/review rule, not runtime.
- **Inherit Box, don't re-derive** — the `as`/`asChild` Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL all come from Box (see box); Stack adds only the flex + gap + direction + align/justify + wrap + dividers delta.
- **Headless vs opinionated** — a thin opinionated layer on flexbox + the token scale (no state, no a11y machinery beyond `as`); ship as a styled layout primitive — the value is the constrained, token-bound, intent-revealing API over raw flex (the abstraction utility classes like Tailwind's `flex gap-4` deliberately forgo).

## 12. Related and alternative components
- **Stands on:** **Box** (the polymorphic `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime styling delivery, the logical-property RTL — all inherited; see box).
- **The answer to:** Box's **no-external-margin principle** — Stack owns the inter-sibling gap so children stay flush and portable (see box).
- **Composes:** **Divider** (the divider-between-children, n−1 separators inheriting the Stack's direction — see divider).
- **1D sibling of:** **Grid** (the 2D engine — Stack is one axis; reach for Grid when you need rows × columns simultaneously — not yet briefed).
- **Composed by / nested:** **Card** (the card body is a Stack — not yet briefed), forms, lists, nav, toolbars, and **recursively** (the Stack-of-Stacks layout tree).
- **Alternative to / boundary with:** a bare **Box** (`display="flex"` by hand — the smell Stack replaces), a **Spacer** (a `flex-grow` node absorbing free space to push clusters apart — for the one-off push, vs Stack's uniform gap), and **flex utility classes** (Tailwind's `flex gap-4 md:flex-row` — the no-Stack-component position, trading the enforced scale + a11y abstraction for raw flexibility).

(The first Layout engine — the 1D flexbox component that owns the gap, the answer to Box's no-external-margin principle. It stands on Box (inheriting the Slot, the scale, the RTL), composes Divider (the divider-between), is the 1D sibling of Grid, and is nested recursively into the layout tree. See box for the substrate, divider for the divider-between, grid/card/section when briefed for the sibling + the hosts, tag for the FLIP reflow it shares. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Self-contained-margins → the no-margin principle.** Early component-driven development made components own their external margins (a button's right margin, a paragraph's bottom margin), producing fragile systems where novel combinations caused margin collapse and cascading overrides. The field stripped external margins from components — the no-external-margin principle — which *necessitated* a mechanism to own the removed space.
2. **The lobotomized owl → flex `gap` (the Safari 14.1 inflection).** The first-generation answer was the lobotomized owl (`* + *` margin); it solved the immediate problem but broke on wrapping and fought specificity. **Safari 14.1 (2021)** unlocked native flex `gap` across all engines, and Stacks shed the CSS hackery — the layout engine assumed full native control of interstitial space, with flawless multiline wrapping and zero cascade side-effects. (MUI's `useFlexGap` opt-in marks the migration moment.)
3. **The no-margin principle making Stack canonical** — Stack moved from a convenience to *the* designated owner of inter-sibling space, the foundational layout primitive.
4. **Logical-axis naming for RTL** — Polaris's `BlockStack`/`InlineStack` named the axes logically, making RTL and writing-mode correctness inherent; the field is deprecating physical terminology (`row`/`left`/`right`) for logical (`inline`/`start`/`end`).
5. **Strict accessibility governance — the no-reorder rule** — the rigid enforcement of meaningful-sequence (1.3.2) and focus-order (2.4.3) effectively eliminated visual DOM-reordering (`reverse`/`order`) from layout primitives; reverse the source array, not the CSS.
6. **The Stack-tree mental model** — "build every layout as a tree of Stacks (with the occasional Grid)" became the dominant authoring model, displacing ad-hoc margins and floats.

## 14. Sources cited
(Conservative; reconcile with external.) **Chakra UI** — `Stack`/`VStack`/`HStack` (`spacing`→`gap`, `StackDivider`, `align`/`justify`; v2/v3) (2024–2026); **MUI** — `Stack` (`direction`, `spacing`, `divider`, the `useFlexGap` opt-in; v5+) (2024–2026); **Braid / Seek** — `Stack` (vertical) + `Inline` (horizontal), `dividers`, `collapseBelow` (the no-margin origin) (2024–2026); **Radix Themes** — `Flex` (`direction`/`align`/`justify`/`gap`/`wrap`; responsive object → CSS custom properties; v3) (2024–2026); **Shopify Polaris** — `BlockStack`/`InlineStack` + `<s-stack>` (the logical-axis naming; v12+/2025-10) (2024–2026); **GitHub Primer** — `Stack` + `PageLayout` (single component, physical naming; React v36+) (2024–2026); **Adobe Spectrum / React Aria** — `Flex` (native CSS naming; v3) (2024–2026); **IBM Carbon** — `Stack` (`gap`, `orientation`, default vertical; v11) (2024–2026); **Atlassian** — `Stack`/`Inline` (`@atlaskit/primitives`, `xcss`, strict no-reverse a11y) (2024–2026); **Tailwind** — `flex`/`gap` utilities (the no-Stack-component position) (2024–2026); **Base Web (Uber)** — `FlexGrid` (2024); **Heydon Pickering** — the lobotomized owl (`* + *`, 2014); **WAI-ARIA / HTML** — Stack is a semantically-neutral flex `div` (no role); the DOM-order-vs-visual-order meaningful-sequence trap. **CSS Box Alignment Module** — flexbox `gap` (Safari 14.1, ~April 2021; grid gap since 2018; the `@supports` feature-detection trap). WCAG 2.2 (W3C Recommendation, Oct 2023) — 1.3.2, 2.4.3, 1.3.1.

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
  SPACE BETWEEN SIBLINGS via gap, so children stay flush + portable ('the component
  that owns the gap'). NOT a Box (the neutral layout-agnostic substrate — Stack IS the
  opinion: flex + gap + direction), NOT a Grid (the 2D engine — Stack is one axis even
  when it wraps). Stands on Box (the as/asChild Slot, the spacing-token scale, the
  styling delivery, the logical-property RTL); composes Divider (the divider-between);
  the 1D sibling of Grid; composed by Card/forms/lists/nav and nested recursively.
anatomy:
  parts:
    - "the flex container: a block node establishing a flex formatting context; children become flex items; a semantically neutral div (inherits Box's neutrality)"
    - "the gap: the measured whitespace BETWEEN flex items (not around — that's parent padding), mapping to the spacing-token scale; the Stack owns it so children need no margins"
    - "children as flex items: the content arranged; mostly unstyled by Stack (the per-item-flex question)"
    - "optional dividers-between: injected Divider, n-1 for n children (between never around), across the cross-axis (vertical Stack -> horizontal dividers)"
    - "the polymorphic slot (inherited from Box): renders div by default, cast as ul/ol/nav/section/fieldset for semantics without altering flex mechanics"
api:
  inherits:
    - box        # the as/asChild Slot, the spacing-token scale (gap resolves against it), the zero-runtime delivery, the logical-property RTL
  composes:
    - divider    # the divider-between-children (n-1, inherits the Stack's direction)
  props:
    - {name: direction/orientation, type: "'vertical'|'horizontal' | responsive", default: vertical, required: false, description: "the main axis -> flex-direction; responsive (direction={{base:'column',md:'row'}}) decided by the responsive switch + the React remount/state-loss argument; prefer LOGICAL values for RTL"}
    - {name: gap/spacing, type: "token-scale", default: ~, required: false, description: "the inter-child space, a token index (gap={4}); 'gap' (CSS-matching) over legacy 'spacing'; rowGap/columnGap for distinct wrapped gutters"}
    - {name: align, type: "'start'|'center'|'end'|'stretch'", default: "start (override the CSS stretch default to avoid warping) — resolve per direction", required: false, description: "CROSS-axis (align-items)"}
    - {name: justify, type: "'start'|'center'|'end'|'space-between'|'space-around'|'space-evenly'", default: start, required: false, description: "MAIN-axis (justify-content)"}
    - {name: wrap, type: boolean, default: "off (vertical) / often on (Inline)", required: false, description: "flex-wrap; wrapped lines get the SAME gap (two-axis); INCOMPATIBLE with dividers"}
    - {name: dividers, type: "boolean | element", default: false, required: false, description: "render Divider between children (n-1); single-line ONLY (orphans on wrap)"}
    - {name: as/asChild, type: "ElementType/boolean", default: div, required: false, description: "inherited from Box — render the right element (ul/ol/nav/section) for semantics"}
  per-item-flex: "the scope question — most keep Stack SIMPLE (direction/gap/align/justify/wrap) and leave grow/shrink/basis to the child or a Spacer (a flex-grow free-space absorber); practice: keep simple"
  alignment-naming-fork: "align/justify (concise, axis-abstracted — practice default) vs native alignItems/justifyContent (CSS-fluent — MUI/Spectrum)"
  withholds: "no margin (parent's gap), no chrome (Card), no 2D tracks (Grid)"
states:
  runtime: []   # NONE — layout-only, no pointer/keyboard response; inherits Box's statelessness; an interactive element via as/asChild carries the states
variants:
  direction: [vertical, horizontal, responsive]
  wrap: [no-wrap, wrap]
  dividers: [plain, with-dividers]   # single-line only
  alignment: "align (cross) x justify (main) combinations"
  rendered-element: "the as target (div/ul/ol/nav/section/fieldset)"
accessibility:
  inherits: [box (semantically-neutral div; the element it renders via as is the whole story)]
  wcag-criteria: ["1.3.2", "2.4.3", "1.3.1"]
  DOM-vs-visual-order-trap: "the Stack-specific crux — flexbox lets visual decouple from DOM: row-reverse/column-reverse/order/WRAP make visual diverge from DOM. SR parses the DOM (original order); Tab follows the DOM (focus jumps against the visual flow). Violates 1.3.2 Meaningful Sequence + 2.4.3 Focus Order"
  no-reorder-rule: "reverse/order deprecated/linted/banned in layout primitives; if a visual reversal IS needed (primary action to top on mobile), REVERSE THE NODE ARRAY before DOM injection so visual/SR/tab order stay synced — change the source, not the CSS"
  semantic-as: "a Stack laying out a LIST -> as='ul'/'ol' + <li> children (nav -> as='nav') so the count + relationship reach AT; don't leave a meaningful group a neutral div (1.3.1)"
  focus: "not focusable, manages no focus; an interactive rendered element owns its contract"
content:
  holds-layout-not-content: "strictly architectural — no typography/color/icon/data of its own (like Box)"
  no-fake-semantics: "a vertical Stack of text that LOOKS like a list but isn't as='ul'/li reads as an arbitrary text sequence (no count/relationship); the structural presentation must map to semantic markup via as"
motion:
  own: none   # gap calc + flex distribution execute instantly at layout/paint
  reflow: "items add/remove/reorder -> siblings reflow to new gap-spaced positions; FLIP (capture initial+final geometry, bridge with hardware-accelerated transform, NOT animating width/margin/gap directly which forces reflows); same as Tag's group reflow, applied by the consumer/an animation primitive via asChild"
  reduce-motion: "any wrapping animation lib must intercept prefers-reduced-motion -> instant layout; Stack is motion-neutral"
i18n:
  gap-direction-agnostic: "the gap is a symmetric token rhythm — no RTL handling needed"
  horizontal-flips-natively: "dir=rtl commands the flexbox engine to reverse the main-axis visual flow (first item far right, flow left); the gap (intrinsically logical) applies along the dynamic axis — NO JS, no RTL CSS overrides (avoid row-reverse)"
  logical-axis-naming: "Polaris BlockStack/InlineStack (block=stacking/vertical, inline=text-flow/reading) is the RTL-correct model; physical names fine if mapped to logical underneath — prefer logical semantics"
  vertical-rtl-neutral: "vertical Stacks don't flip for RTL (block axis); they flip for vertical writing modes, which logical properties handle"
implementation:
  - "flex GAP over the lobotomized owl (the Safari 14.1 inflection): modern Stack = display:flex + flex-direction + gap:<token>; viable only since Safari 14.1 (macOS Big Sur/iOS 14.5, ~Apr 2021; grid gap since 2018, WebKit delayed flex gap). Before: the lobotomized owl (& > * + * {margin-block-start}; Heydon Pickering 2014) — broke on WRAP (jagged edges) + fought specificity. The @supports TRAP: can't feature-detect flex gap (@supports(gap) returns true for GRID gap) -> gate on version. MUI's useFlexGap opt-in = the migration moment. DATE IT"
  - "direction prop -> flex-direction; responsive object -> per-breakpoint flex-direction (inherits Box's object-over-array; Radix Themes compiles to CSS custom properties); the responsive switch + the React remount/state-loss argument decide one component over two"
  - "align -> align-items (cross), justify -> justify-content (main); names abstract the axis (align is ALWAYS the cross axis); consider overriding the CSS stretch default to start (avoid warping)"
  - "wrap -> flex-wrap:wrap; flex gap applies to BOTH axes (row+column gap) on a wrapped Inline (the margin era couldn't); expose rowGap/columnGap for distinct gutters"
  - "divider-between (n-1, composing Divider): children.flatMap((c,i)=> i?[<Divider/>,c]:[c]) -> 2n-1 items; inherits the Stack's direction; none before first/after last. INCOMPATIBLE WITH WRAP (orphaned dividers at line ends) — warn/disable when wrap active"
  - "no-reorder enforcement: avoid flex *-reverse + order for sequence-meaningful content; reverse the node ARRAY before injection if needed (a lint/review rule, not runtime)"
  - "inherit Box, don't re-derive: the as/asChild Slot, the spacing-token scale, the zero-runtime delivery, the logical-property RTL; Stack adds only the flex+gap+direction+align/justify+wrap+dividers delta"
  - "headless vs opinionated: a thin opinionated layer on flexbox + the token scale (no state, no a11y beyond as); ship as a styled layout primitive — the value is the constrained token-bound intent-revealing API over raw flex (what Tailwind utilities forgo)"
composition:
  stands-on: [box]
  answer-to: "box's no-external-margin principle (Stack owns the inter-sibling gap)"
  composes: [divider]
  sibling-of: [grid]                       # 1D vs 2D (not yet briefed)
  composed-by: [card, "forms", "lists", "nav", "toolbars"]   # + recursively (the Stack-of-Stacks layout tree)
  alternative-to: ["bare Box display=flex (the smell Stack replaces)", spacer, "flex utility classes (Tailwind no-Stack position)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "ONE Stack + direction prop (MUI/Primer/Carbon — the practice default, for the responsive switch + the React remount/state-loss problem) vs TWO components (Chakra VStack/HStack; Braid Stack/Inline; Polaris BlockStack/InlineStack)"
    - "LOGICAL (Block/Inline — Polaris, RTL-correct) vs PHYSICAL (Vertical/Horizontal, row/column) axis naming"
    - "align/justify (concise, axis-abstracted — practice default) vs native alignItems/justifyContent (CSS-fluent — MUI/Spectrum)"
    - "the align default per direction (override the CSS stretch default to start to avoid warping)"
    - "gap vs spacing prop naming (practice: gap, matching CSS)"
    - "expose per-item flex (grow/shrink) vs keep Stack simple + a Spacer (practice: keep simple)"
    - "Stack vs Flex naming (Flex = the more general lower-level primitive; Stack = the gap-first opinionated subset)"
  trap:
    - "the DOM-order-vs-visual-order trap: row-reverse/order/wrap diverging visual from DOM/reading/tab order (WCAG 1.3.2 + 2.4.3) — reverse the node ARRAY not the CSS"
    - "putting margin on a Stack's children to adjust spacing (fights the gap; change gap or nest a Stack — the no-external-margin principle)"
    - "adding chrome (bg/border/elevation) to a Stack (that's a Card)"
    - "faking a list visually as a stack of divs without as='ul'/li (loses the count + relationship)"
    - "the lobotomized-owl margin hack in modern code (use flex gap); the @supports(gap) feature-detection trap (returns true for grid gap)"
    - "dividers with wrap (orphaned at line ends — n-1 single-line only); a divider before the first / after the last child"
  inherited: "Box's as/asChild Slot, the spacing-token scale, the zero-runtime styling delivery, the logical-property RTL, the semantically-neutral-div a11y"
  role-in-family: "the first Layout engine — the 1D flexbox component that owns the gap, the answer to Box's no-external-margin principle; stands on Box, composes Divider, the 1D sibling of Grid, nested recursively into the layout tree"
  evolution:
    - "self-contained-margins -> the no-margin principle (necessitating a space-owner)"
    - "the lobotomized owl (* + * margin, Pickering 2014) -> flex gap (the Safari 14.1/~2021 inflection; MUI useFlexGap) -> Stack-owns-the-space"
    - "the no-margin principle making Stack canonical"
    - "logical-axis naming (Polaris Block/Inline) for RTL/writing-mode correctness"
    - "strict a11y governance — the no-reorder rule (reverse the source array, not the CSS)"
    - "the Stack-tree mental model (build layouts as a tree of Stacks + the occasional Grid)"
  unverified:
    - "external 2026 version numbers across the surveyed systems"
    - "the exact Safari flex-gap version/date (14.1, macOS Big Sur/iOS 14.5, ~April 2021) — verify"
    - "per-system align defaults + the gap-vs-spacing / align-vs-alignItems naming state"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-stack/` (16 June 2026), the thirty-sixth brief and the **first Layout engine** — the 1D flexbox component that owns the gap and the answer to Box's no-external-margin principle (the second Layout brief after the substrate). It stands on Box (inheriting the `as`/`asChild` Slot, the spacing-token scale its `gap` resolves against, the zero-runtime delivery, and the logical-property RTL — not re-derived), composes Divider (the divider-between-children, n−1), and is the 1D sibling of Grid (not yet briefed). The two passes converged with no genuine fork — the gap mechanism + the flex-gap inflection, the direction question + the naming morass, the align/justify matrix, the wrap + two-axis-gap interaction, the DOM-order-vs-visual-order meaningful-sequence a11y trap, and the recursive Stack-of-Stacks model. The external pass sharpened with concrete field detail: the **lobotomized-owl attribution** (Heydon Pickering, 2014) and its wrap-breakage, the **`@supports (gap)` feature-detection trap** (it returns true for grid gap), the precise **Safari 14.1 / macOS Big Sur / iOS 14.5 / April 2021** dating (grid gap since 2018), **MUI's `useFlexGap` opt-in** as the migration moment, the **React remount/state-loss argument** as the decisive case for one-component-with-`direction` (you can't swap VStack↔HStack across breakpoints without destroying the node and its state — Braid's `collapseBelow` the workaround), the **divider + wrap structural incompatibility** (2n−1 items, orphaned dividers), **`rowGap`/`columnGap`** for distinct wrapped gutters, the **stretch-default warping** problem (override to `start`), and the reverse-the-node-array a11y remedy. The one mild divergence — `align`/`justify` (the concise, axis-abstracted shorthand the Claude pass and Chakra/Radix/Braid use) vs the external pass's lean to native `alignItems`/`justifyContent` (MUI/Spectrum) — is recorded as a contested naming choice, resolved toward the concise shorthand. Claude-pass contributions: the owns-the-gap framing as the no-margin answer, the substrate-inheritance map (Box delta only), the Stack-vs-Box-vs-Grid boundary, and the recursive-layout-tree model. The 2026 version numbers and the exact Safari date are flagged unverified. Conformant to `components/_schema.md`. With Stack, Box's no-external-margin principle has its mechanism, and the layout tree has its trunk.*

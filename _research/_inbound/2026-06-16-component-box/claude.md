# Box — field-truth study (Claude pass)

## 1. Framing
A Box is the **polymorphic, token-aware layout substrate** — the lowest-level primitive in the Layout category, a semantically-neutral element (a `div` by default) that exposes the design system's constraints (the spacing scale, color tokens, the box model) through a prop surface. It is the "open canvas" the rest of the category stands on: Stack, Grid, Card, and Section are all *specializations* of Box. As the brief that **opens Layout**, its job is to get the substrate right — the spacing-token scale, the polymorphic `as`/`asChild` model, and the style-prop POV — so the four descendants inherit rather than re-derive (the same role Text Field played for Form and Popover for the Overlay positioning substrate).

The headline is a genuinely contested question that the practice must answer up front: **should a design system even ship a Box?** Two philosophies:
- **The style-prop Box** (Chakra, Theme UI, MUI `Box`/`sx`, Radix Themes, Polaris) — a polymorphic primitive with a large surface of style props (`p`, `m`, `bg`, `display`, `flex`…) mapping to tokens; the "everything is a Box" lineage (React Native's `View`, Styled System). Maximally flexible.
- **The constrained / no-Box turn** (Braid's `Stack`/`Inline`/`Columns`, Tailwind + shadcn's utility-classes-and-bare-elements) — *skip* the god-Box; ship intent-revealing, constrained layout components and use plain elements + classes for the rest. The argument: a Box with 100 style props is **inline styles with extra steps** — it leaks the constraint system, invites unmaintainable one-offs, and hides layout *intent* behind generic styling.

The practice's resolution (the **constrained-over-open principle**): **Box exists as the substrate — the low-level escape hatch Stack/Grid/Card are built on — but it is *not* the recommended authoring surface.** Day-to-day, reach for the constrained layout components (Stack/Grid) that reveal intent; drop to a bare Box only for the genuine one-off the constrained set doesn't cover. Box is the primitive you build *with*, not the one you reach for *first*.

What it *isn't*: a **styled component** (Box is unstyled/neutral — it carries no visual identity of its own, unlike Card), a **layout engine** (the flex/grid *intent* belongs to Stack/Grid — a bare Box doing `display: flex` via props is the smell the constrained turn warns about), or a **semantic region** (that's Section, with a landmark role). Why systems disagree: the should-we-ship-it question, the styling-engine delivery (runtime style-props vs zero-runtime vs utility classes), and the polymorphism mechanic.

## 2. Anatomy and parts
Box has almost no *visual* anatomy — it's a `div`. Its anatomy is the **prop surface** and the rendered element:
- **the rendered element** — what HTML element Box becomes (`as`/`asChild`); default `div`, semantically neutral. The single most consequential "part" (§6).
- **the token-mapped style props** — the spacing props (`p`/`m`/`px`/`py`…), color (`bg`/`color`), display/layout (`display`/`flex`/`grid`), sizing (`w`/`h`/`maxW`), `overflow`/`position` — each value resolving against a design token, not a raw CSS value.
- **the box-model surface** — padding, (debated) margin, border, radius, size — the CSS box model exposed as constrained props.
- **the (absence of) semantics** — Box has no role, no accessible name, no interaction states; it is deliberately empty of meaning so the consumer supplies it via `as`.
- **children** — Box is a container; it holds content but authors none.

## 3. Properties / API
- **`as` / `asChild`** — the polymorphic element control. `as="section"` renders a different tag; `asChild` (Radix Slot) merges Box's props onto the consumer's child element instead of rendering its own (§11). The headline mechanic, shared with Button/Link (see button, link).
- **the style-prop surface** — token-mapped shorthands: **spacing** (`p`, `px`, `py`, `pt/pr/pb/pl`, `m`…), **color** (`bg`, `color`, `borderColor`), **display/layout** (`display`, `flexDirection`, `alignItems`, `gap`), **sizing** (`width`/`w`, `height`/`h`, `minW`, `maxW`), **`overflow`**, **`position`**, **`borderRadius`**, **`boxShadow`**. Each value is a token index (`p={4}` → the 4th spacing token), not a raw px.
- **the responsive syntax** — array (`p={[2, 3, 4]}` → base/sm/md, Styled System) or object (`p={{ base: 2, md: 4 }}`, Chakra) breakpoint mapping. (The field is shifting toward container queries + CSS over runtime responsive props — §13.)
- **`sx` vs discrete props** — MUI's `sx` is an escape-hatch object prop (`sx={{ p: 2, bg: 'primary' }}`) vs Chakra's flat discrete props (`p={2} bg="primary"`). Same token resolution, different ergonomics.
- **what to expose vs withhold (the margin question)** — expose padding, display, size, color, radius; **withhold or discourage external margin** (the no-external-margin principle — §11). Don't expose every CSS property as a prop (that's just inline styles); expose the *constrained, tokenized* subset.
- **the spacing-token scale** — the underlying scale all spacing props resolve against (4/8px base, numeric or t-shirt); Box owns it, Stack/Grid `gap` and Card padding reference it (§ implementation).

## 4. States and variants
- **States:** **none** — Box has no hover/focus/active/disabled of its own (it's a neutral container). If it renders an interactive element via `as`/`asChild`, the *consumer's* element carries the states, not Box.
- **"Variants" (not visual variants — delivery + element axes):**
  - **rendered element:** the `as` target (`div`/`section`/`span`/`ul`/…) or `asChild`.
  - **styling-engine delivery:** runtime style-props (Chakra/Theme UI) / `sx` (MUI) / `className` + utility classes (Tailwind) / zero-runtime (Vanilla Extract, Panda) / CSS Modules — the same component contract, very different build/perf profiles (§11/§13).
  - **display/layout mode:** block / flex / grid (which Box *can* take via props, but which the practice routes to Stack/Grid — §5).

## 5. Usage guidance
- **Use a Box for:** a genuine **one-off container** the constrained layout set doesn't cover — a wrapper needing a specific token-mapped padding/background/radius, a positioning context, an escape hatch where Stack/Grid don't fit. As the **substrate** other components are built on (internal use).
- **Don't use a Box for (reach for the right tool):**
  - **Arranging children with spacing between them** → a **Stack** (1D) or **Grid** (2D) — they reveal the layout *intent* and own the `gap` (Stack/Grid not yet briefed). A bare Box doing `display: flex; gap` by hand is the smell.
  - **A visual surface** (elevation/border/padding holding content) → a **Card** (Card not yet briefed).
  - **A semantic region / landmark** → a **Section** (with the right role/heading — Section not yet briefed), or `as="section"` deliberately.
  - **Text** → a **Text/Heading** component, not a bare Box.
  - **One-off arbitrary styling** → if you're spreading 15 style props on a Box, that's inline styles with extra steps; reconsider whether a constrained component or a named styled component fits.
- **The constrained-over-open rule (the load-bearing guidance):** reach for the *intent-revealing, constrained* component first (Stack/Grid/Card); drop to a bare Box only when none fits. Box is the floor, not the default. This keeps layout intent legible and the constraint system intact.

## 6. Accessibility
Box's a11y story is unusually short and unusually important: **Box is a semantically-neutral `div` — no role, no name, no states — and the entire accessibility surface is the element it renders.**
- **The `as`/`asChild` is the whole contract.** Box defaults to `div` (correctly meaningless). When it should be semantic — a region, a list, a nav — the consumer sets `as="section"`/`"ul"`/`"nav"` (or `asChild` onto the right element). The primitive has no inherent semantics *by design*.
- **The wrong-semantics trap (the one real risk).** Polymorphism lets a Box render the *wrong* or *invalid* element: `as="button"` produces a `<button>` with **no button behavior** (no keyboard, no role expectations met), `as="h2"` injects a heading into the outline with no thought to level, nesting interactives invalidly. The rule: **the primitive has no inherent semantics, so don't let it emit the wrong ones** — `as` is for choosing the *correct* element, not for faking a component (a real button is the Button component, not `as="button"`).
- **No focus management, no labeling** — a bare Box is not focusable and needs no name; if it becomes interactive via `as`, it inherits that element's full a11y contract (and should usually be the actual component — Button/Link — not a hand-rolled `as`).
- **WCAG:** Box itself triggers nothing directly; the relevant criteria attach to whatever it renders (4.1.2 name/role/value if it's made interactive; 1.3.1 info-and-relationships if `as` is used for structure). The lightest a11y in the catalogue — but with the sharp polymorphism-produces-wrong-semantics caveat. (Compare Divider's "thinnest component" a11y — see divider.)

## 7. Content guidelines
- Box **holds** content; it doesn't author it. There are no content patterns of its own (no label, no copy).
- **No bare Box for text** — text belongs in a Text/Heading component (for the type scale, the semantic element, the truncation/i18n handling), not dumped as children of a styling `div`.
- If a Box is wrapping content that has *meaning as a group* (a list, a region), that's a signal to give it the right `as` (or use Section/Stack) rather than leaving it a neutral `div`.

## 8. Motion and transition
- Box has **no motion of its own** — it's a container. It can *carry* a transition (a consumer animating its token-mapped properties), and it's frequently the element a layout animation (FLIP, a height/`gap` transition) is applied to, but the Box primitive ships no animation.
- Reduce-motion is the consumer's concern on whatever animation they attach; Box is motion-neutral.

## 9. Internationalization
- **Logical properties over physical (the load-bearing i18n rule).** Box's spacing/position props should map to **CSS logical properties** (`padding-inline`/`padding-block`, `margin-inline-start`, `inset-inline`) — not physical `padding-left`/`right` — so a `pl`/`ps` prop flips correctly under `dir="rtl"` with zero JS. The field has largely shifted prop naming toward logical (`ps`/`pe` = padding-start/end over `pl`/`pr`); a Box still exposing only physical props is a latent RTL bug factory.
- The **spacing-token scale** is direction-agnostic (a 4/8px rhythm), but its *application* must be logical.
- Box is otherwise i18n-neutral (no text of its own — §7).

## 10. Naming
- **The field set:** **`Box`** dominates (Chakra, Theme UI, MUI, Radix Themes, Primer, Polaris); **`View`** (React Native, Adobe Spectrum — the RN lineage); **`Block`** (Base Web/Uber); occasionally `Frame`/`Primitive`.
- **The practice's default — `Box`** (the dominant, unambiguous name for the neutral polymorphic primitive). The **layout descendants** are the named, constrained components built on it: **`Stack`** (1D), **`Grid`** (2D), **`Flex`**/**`Inline`** (Braid's row-flow), **`Card`**, **`Section`** — these carry the intent Box deliberately lacks.
- **Don't overload Box** — resist making Box *also* the Stack (a `Box display="flex"` convenience) or *also* the Card; keep Box neutral and let the named components carry meaning (the constrained-over-open principle, expressed in naming).
- **Aliases to map:** View, Block, Frame, Primitive, `<div>` (the thing it abstracts).

## 11. Implementation notes
- **The polymorphic `as` TypeScript explosion (the headline implementation problem).** A fully-generic polymorphic `as` prop — correctly typing the element's props for *any* tag, plus `ref` forwarding (`forwardRef` + generics) — is one of the hardest typing problems in React DS land (the `PolymorphicComponentPropsWithRef` machinery, the slow type-check, the broken inference). **The modern escape is `asChild` / the Radix `Slot`**: instead of Box accepting `as` and re-typing every element, the consumer passes their *own* element as the single child and Box's `Slot` **merges props/behavior onto it** — sidestepping the generic-typing explosion entirely and composing cleanly with other components (this is the same Slot pattern Button/Link use for the link-vs-button and router-`<Link>` cases — see button, link). The practice default: **`asChild`/Slot as the primary polymorphism mechanism**, with `as` as a lighter convenience for simple tag swaps where the typing cost is bounded.
- **The styling-engine delivery + the zero-runtime / RSC reckoning (the big inflection).** The classic style-prop Box ran on **runtime CSS-in-JS** (Styled System → Emotion/styled-components under Chakra/Theme UI/MUI), which resolves token props to styles *in the browser on every render* — a measurable perf cost and, critically, **incompatible with React Server Components** (runtime CSS-in-JS can't run in RSC). The field is moving decisively to **zero-runtime** engines — **Vanilla Extract**, **Panda CSS** (the Chakra team's own successor), **Tailwind** utility classes, and **CSS Modules** — that extract styles at build time. **Primer's `sx`-prop deprecation** (toward CSS Modules) is the worked cautionary tale: the style-prop Box that defined an era is being unwound for perf and RSC-compatibility. **The practice POV: build the spacing-scale/token-prop ergonomics on a zero-runtime engine** (the token-prop *authoring* experience can survive; the *runtime* must not). Date this — it's the most volatile claim in the brief.
- **The spacing-token scale (what the category inherits).** A 4px or 8px base rhythm, exposed as a numeric scale (`1`=4px, `2`=8px…) or t-shirt (`xs`/`sm`/`md`); primitive tokens (the raw scale) vs semantic (`space.inset.md`). Box owns the scale; **Stack/Grid `gap` and Card padding resolve against the same scale** — so it must be defined here, once, for the category.
- **The no-external-margin principle (enforce it).** **Components — including Box — should not own their external margin.** Margins break encapsulation (a component can't be safely reused if it carries `margin-bottom`), collapse unpredictably, and fight the parent's spacing. Spacing *between* siblings belongs to the **parent layout** (Stack/Grid `gap`). So Box should expose **padding (internal) freely** but **discourage or omit margin props** — push inter-element spacing to the layout parent. (This is why Stack exists: it owns the gap so the children don't.)
- **The responsive prop implementation** — the array/object→breakpoint mapping (media queries generated per prop). Increasingly superseded by **container queries** (the component responds to its container, not the viewport) + CSS, which the runtime responsive-prop syntax can't express well.
- **Headless vs opinionated** — Box is the *most* substrate-like component: ship the token-prop ergonomics + the polymorphic Slot + the scale, themed by the consumer's tokens. But the delivery mechanism (zero-runtime) is the load-bearing engineering choice, not the prop names.

## 12. Related and alternative components
- **Substrate FOR (the inheritors):** **Stack** (1D flex, owns `gap`), **Grid** (2D, tracks/areas/`gap`), **Card** (a styled surface), **Section** (a semantic region) — all built on Box, all inheriting the spacing-token scale + the polymorphic `as`/`asChild` (Stack/Grid/Card/Section not yet briefed; this brief is their substrate).
- **Shares (the polymorphic substrate):** the **`asChild`/Slot** polymorphism is the same mechanism **Button** and **Link** use (the link-vs-button and router-`<Link>` cases — see button, link); Box formalizes it for the Layout category.
- **Shares (the spacing-token scale):** the whole **Layout category** + every component with padding (the scale is a design-token-system concern — see 00-principles / the token files).
- **Alternative to:** a **styled component** (a Box with a fixed, named style — when the styling is reused and meaningful, name it), **bare HTML + `className`/utility classes** (the Tailwind/no-Box position — for teams that reject the style-prop primitive), and the **constrained layout components** (Stack/Grid — the recommended authoring surface over a bare Box).

(The Layout substrate — the polymorphic, token-aware, semantically-neutral primitive that opens the category. It is built *with*, not reached for first (the constrained-over-open principle). It is the substrate Stack/Grid/Card/Section inherit, it formalizes the asChild/Slot polymorphism Button/Link use, and it owns the spacing-token scale the category shares. See button/link for the shared Slot polymorphism, stack/grid/card/section when briefed for the inheritors, divider for the comparably-thin a11y, 00-principles for the token system. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **Styled System → the runtime style-prop Box.** The 2018–2021 era established the polymorphic, token-mapped style-prop primitive (Styled System → Chakra, Theme UI, MUI `sx`) as the way to build UIs — "everything is a Box," responsive array props, the `sx` escape hatch.
2. **The perf + RSC reckoning.** Runtime CSS-in-JS's per-render cost and its **incompatibility with React Server Components** turned the runtime style-prop Box from best-practice into legacy — Primer's `sx`-deprecation, the broad migration toward **zero-runtime** (Vanilla Extract, **Panda CSS** — built by Chakra's own team as the successor) and Tailwind/CSS Modules.
3. **The constrained-layout turn (Stack/Inline over Box).** Braid/Seek and others pushed back on the god-Box: ship **intent-revealing constrained components** (Stack, Inline, Columns) and treat the bare Box as an escape hatch, not the default — the constrained-over-open principle.
4. **`asChild`/Slot settling over the `as`-typing nightmare.** Radix's `asChild`/Slot displaced the fully-generic polymorphic `as` prop as the composition mechanism, sidestepping the TypeScript explosion (and now shared across Button/Link/Box).
5. **The no-external-margin principle hardening.** "Components don't own their external margin; the parent layout owns the gap" went from a nicety to a near-settled rule — and is *why* Stack exists.

## 14. Sources cited
*(External-pass version dates to be reconciled against the external-agent pass; flag any unverified under notes.unverified.)*
- Chakra UI — `Box` (the canonical style-prop polymorphic primitive, `as`, style props); and **Panda CSS** (the Chakra team's zero-runtime successor).
- Theme UI — `Box` (the Styled System lineage, `sx`, responsive arrays).
- MUI — `Box` (the `sx` prop, `component` prop, system props).
- Radix Themes + Radix Primitives — `Box` + the **`asChild` Slot** pattern (the polymorphic substrate).
- Braid / Seek — `Box` + `Stack`/`Inline`/`Columns` (the constrained-over-open, no-external-margin school).
- Tailwind + shadcn/ui — the utility-classes-no-Box position.
- GitHub Primer — `Box` + the **`sx`-prop deprecation** toward CSS Modules (the worked cautionary tale).
- Shopify Polaris — `Box` (token props, the layout primitive).
- Adobe Spectrum / React Aria — `View` (the RN-style primitive).
- Base Web (Uber) — `Block`.
- Styled System — the historical prop→token-mapping lineage.
- Vanilla Extract / Panda CSS — the zero-runtime successors.
- WAI-ARIA / HTML — Box is a semantically-neutral `div` (no role); the `as`-produces-wrong-semantics trap.

## 15. Agent-consumable schema
```yaml
identity:
  id: box
  name: Box
  aliases: [View, Block, Frame, Primitive]
  category: layout
  status: stable
description: >
  The polymorphic, token-aware, semantically-neutral LAYOUT SUBSTRATE — the lowest-
  level primitive that opens the Layout category and that Stack/Grid/Card/Section
  stand on. A div by default, exposing the design system's constraints (the spacing
  scale, color tokens, the box model) through a token-mapped prop surface. The
  headline contested question: should a DS even ship a Box? Resolved via the
  CONSTRAINED-OVER-OPEN principle — Box is the SUBSTRATE / low-level escape hatch,
  NOT the recommended authoring surface (reach for the intent-revealing Stack/Grid
  first). NOT a styled component (it's neutral), NOT a layout engine (that's
  Stack/Grid), NOT a semantic region (that's Section). Formalises the asChild/Slot
  polymorphism Button/Link use; owns the spacing-token scale the category inherits.
anatomy:
  parts:
    - "the rendered element (as/asChild): default div, semantically neutral — the most consequential 'part'"
    - "token-mapped style props: spacing (p/m/px/py), color (bg/color), display/layout, sizing (w/h/maxW), overflow, position — each value a TOKEN index, not raw CSS"
    - "the box-model surface: padding, (debated) margin, border, radius, size as constrained props"
    - "the (absence of) semantics: no role, no accessible name, no states — deliberately empty so the consumer supplies it via as"
    - "children: it holds content, authors none"
api:
  shares:
    - button/link    # the asChild/Slot polymorphism (the link-vs-button + router cases)
  substrate-for:
    - stack          # 1D flex, owns gap (not yet briefed)
    - grid           # 2D, tracks/areas/gap (not yet briefed)
    - card           # a styled surface (not yet briefed)
    - section        # a semantic region (not yet briefed)
  props:
    - {name: as, type: "ElementType", default: div, required: false, description: "render a different tag (a lighter convenience; bounded typing cost)"}
    - {name: asChild, type: boolean, default: false, required: false, description: "Radix Slot — merge props/behaviour onto the consumer's child instead of rendering own; the PRIMARY polymorphism mechanism (sidesteps the as-typing explosion)"}
    - {name: "style-props (p/m/px/py/bg/color/display/flex/gap/w/h/maxW/overflow/position/borderRadius/boxShadow)", type: "token | responsive", default: ~, required: false, description: "token-mapped shorthands; each value a token index (p={4} -> the 4th spacing token), not raw px"}
    - {name: responsive-syntax, type: "array | object", default: ~, required: false, description: "p={[2,3,4]} (Styled System) or p={{base:2,md:4}} (Chakra) breakpoint mapping; shifting toward container queries + CSS"}
    - {name: sx, type: object, default: ~, required: false, description: "MUI's escape-hatch object prop (sx={{p:2}}) vs Chakra's flat discrete props — same token resolution, different ergonomics"}
  expose-vs-withhold: "expose padding/display/size/color/radius; WITHHOLD or discourage external MARGIN (the no-external-margin principle); expose the CONSTRAINED tokenized subset, not every CSS property (else it's just inline styles)"
  spacing-scale: "the 4/8px scale all spacing props resolve against; Box OWNS it, Stack/Grid gap + Card padding REFERENCE it"
states:
  runtime: []   # NONE — no hover/focus/active/disabled of its own; if it renders an interactive element via as/asChild, the CONSUMER's element carries the states
variants:
  rendered-element: "the as target (div/section/span/ul/...) or asChild"
  styling-engine-delivery: [runtime-style-props, sx, className-utility, zero-runtime, css-modules]   # same contract, very different build/perf
  display-mode: [block, flex, grid]   # Box CAN take these but the practice routes flex/grid to Stack/Grid
accessibility:
  wcag-criteria: []   # nothing direct; criteria attach to whatever it RENDERS (4.1.2 if made interactive, 1.3.1 if as is used for structure)
  semantics: "a semantically-neutral div — NO role, NO name, NO states; the WHOLE a11y story is the element it renders (as/asChild)"
  wrong-semantics-trap: "polymorphism can emit the WRONG/invalid element (as='button' = a button with no button behaviour; as='h2' = an unconsidered heading level). The rule: the primitive has no inherent semantics, so don't let it emit the wrong ones — as is for the CORRECT element, not for faking a component (a real button is the Button component)"
  focus: "a bare Box is not focusable + needs no name; if interactive via as it inherits that element's full contract (and should usually be the actual Button/Link component)"
  note: "the lightest a11y in the catalogue (cf. Divider) but with the sharp polymorphism-produces-wrong-semantics caveat"
content:
  holds-not-authors: "Box holds content, authors none — no label/copy patterns"
  no-bare-box-for-text: "text belongs in a Text/Heading component (type scale, semantic element, truncation/i18n), not a styling div's children"
  signal: "wrapping content with group meaning (a list/region) is a signal to set the right as (or use Section/Stack), not leave it a neutral div"
motion:
  own: none   # a container, ships no animation
  carries: "frequently the element a consumer's layout animation (FLIP, height/gap transition) is applied to; reduce-motion is the consumer's concern"
i18n:
  logical-properties: "spacing/position props MUST map to CSS logical properties (padding-inline/margin-inline-start/inset-inline), not physical (padding-left), so ps/pe flip under dir=rtl with no JS; a Box exposing only physical props is a latent RTL bug factory"
  scale: "the spacing-token scale is direction-agnostic (a 4/8px rhythm) but its APPLICATION must be logical"
  otherwise: "i18n-neutral (no text of its own)"
implementation:
  - "the polymorphic `as` TypeScript explosion: a fully-generic as + forwardRef (PolymorphicComponentPropsWithRef) is one of React DS's hardest typing problems (slow check, broken inference). ESCAPE: asChild/Radix Slot — the consumer passes their own element as the single child, Box merges props onto it (the same Slot pattern Button/Link use). Practice default: asChild/Slot PRIMARY, as a bounded convenience"
  - "the styling-engine delivery + zero-runtime/RSC reckoning (the big inflection): classic style-prop Box ran on RUNTIME CSS-in-JS (Styled System/Emotion) — per-render cost + INCOMPATIBLE WITH RSC. Field moving to ZERO-RUNTIME (Vanilla Extract, Panda CSS [Chakra team's successor], Tailwind, CSS Modules); Primer's sx-deprecation is the worked cautionary tale. Practice POV: build the token-prop ergonomics on a zero-runtime engine (authoring survives, runtime must not). VOLATILE — date it"
  - "the spacing-token scale: 4/8px base, numeric (1=4px) or t-shirt; primitive vs semantic tokens; defined ONCE here for the whole category (Stack/Grid gap + Card padding reference it)"
  - "the no-external-margin principle: components (incl. Box) should NOT own external margin (breaks encapsulation, collapses unpredictably, fights the parent). Expose padding freely, discourage/omit margin props; inter-sibling spacing belongs to the parent layout's gap (this is WHY Stack exists)"
  - "responsive prop impl (array/object -> media queries per prop) increasingly superseded by CONTAINER QUERIES + CSS"
  - "headless vs opinionated: the MOST substrate-like component — ship token-prop ergonomics + the Slot + the scale, themed by consumer tokens; the zero-runtime DELIVERY is the load-bearing engineering choice, not the prop names"
composition:
  substrate-for: [stack, grid, card, section]
  shares-polymorphism-with: [button, link]      # asChild/Slot
  shares-scale-with: [layout-category, "every padded component"]   # the spacing-token scale (a token-system concern)
  alternative-to: [styled-component, "bare HTML + className/utility classes", stack, grid]   # the no-Box position + the constrained-over-open recommendation
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "SHOULD a DS even ship a Box? style-prop Box (Chakra/Theme UI/MUI/Radix Themes/Polaris) vs the constrained/no-Box turn (Braid Stack/Inline; Tailwind+shadcn). Practice: Box is the SUBSTRATE not the authoring surface (constrained-over-open)"
    - "as vs asChild/Slot polymorphism (practice: asChild primary)"
    - "style-props vs sx vs className/utility vs zero-runtime — and the RSC/perf reckoning forcing the move OFF runtime CSS-in-JS"
    - "how much CSS to expose as props (constrained subset vs everything = inline styles)"
    - "margin: expose vs withhold (the no-external-margin principle says withhold)"
  trap:
    - "the polymorphism wrong-semantics trap (as='button' with no button behaviour; unconsidered as='h2' heading levels; nested-interactive invalidity)"
    - "the fully-generic `as` TypeScript explosion (use asChild/Slot)"
    - "runtime CSS-in-JS perf cost + RSC-incompatibility (move to zero-runtime)"
    - "a Box with 15 style props = inline styles with extra steps (reconsider a constrained/named component)"
    - "exposing physical (padding-left) not logical (padding-inline-start) props -> RTL bugs"
    - "components owning external margin (breaks encapsulation; use the parent's gap)"
    - "using a bare Box where Stack/Grid/Card/Section reveal the intent (the constrained-over-open smell)"
  inherited: []   # Box is the substrate; it inherits little, the category inherits FROM it
  role-in-family: "the Layout substrate — the polymorphic, token-aware, semantically-neutral primitive that opens the category; built WITH not reached-for-first; the substrate Stack/Grid/Card/Section inherit; formalises the asChild/Slot polymorphism Button/Link use; owns the spacing-token scale"
  evolution:
    - "Styled System -> the runtime style-prop Box (Chakra/Theme UI/MUI sx; everything-is-a-Box)"
    - "the perf + RSC reckoning -> zero-runtime (Vanilla Extract/Panda/Tailwind/CSS Modules); Primer's sx-deprecation"
    - "the constrained-layout turn (Stack/Inline over Box; constrained-over-open)"
    - "asChild/Slot settling over the as-typing nightmare (shared with Button/Link)"
    - "the no-external-margin principle hardening (why Stack exists)"
  unverified:
    - "external 2026 version numbers + the exact state of each system's CSS-in-JS migration (volatile)"
    - "Primer's sx-deprecation status + Panda CSS adoption — verify against current releases"
    - "the degree to which container queries have displaced responsive props in each system"
```

---
okf_version: "0.1"
type: component-brief
title: Box
description: The polymorphic, token-aware layout substrate that opens the Layout category — a field-truth study of the should-a-DS-even-ship-a-Box debate (the style-prop Box vs the constrained/no-Box turn) resolved via the constrained-over-open principle (Box is the substrate, not the authoring surface), the polymorphic as-vs-asChild/Slot model (the TypeScript megamorphic explosion + the wrong-semantics a11y trap in both directions), the style-props-vs-sx-vs-utility-classes question + the zero-runtime/RSC reckoning (runtime CSS-in-JS's V8-JIT de-opt + RSC-incompatibility → Vanilla Extract/Panda/Tailwind/CSS Modules; Primer v38 the worked deprecation), the three-tier spacing-token scale (numeric/t-shirt/semantic) the whole category inherits, and the no-external-margin principle — with the practice's defaults.
tags: [components, layout]
category: Layout
status: stable
aliases: [View, Block, Frame, Primitive]
last-audited: 2026-06-16
timestamp: 2026-06-16
---

# Box

> A Box is the **polymorphic, token-aware layout substrate** — the lowest-level primitive that opens the Layout category, a semantically-neutral element (a `<div>` by default) exposing the design system's constraints (the spacing scale, color tokens, the box model) through a token-mapped prop surface. It is the substrate Stack, Grid, Card, and Section all stand on (the same role Text Field played for Form and Popover for the Overlay positioning substrate), and it formalises the **`asChild`/Slot polymorphism** Button and Link already lean on (see button, link). The headline is a genuinely contested question the practice must answer first: **should a design system even ship a Box?** The **style-prop Box** (Chakra, Theme UI, MUI `sx`, Radix Themes, Polaris — the "everything is a Box" / Styled System / RN-`View` lineage) vs the **constrained / no-Box turn** (Braid's `Stack`/`Inline`/`Columns`, Tailwind + shadcn's utility-classes-and-bare-elements) — the argument being that a Box with a hundred style props is *inline styles with extra steps* that leak the constraint system. The resolution is the **constrained-over-open principle**: Box exists as the *substrate / low-level escape hatch* Stack/Grid/Card are built on, but it is **not** the recommended authoring surface — reach for the intent-revealing constrained components first; drop to a bare Box only for the genuine one-off. What it *isn't*: a **styled component** (Box is neutral, no visual identity), a **layout engine** (flex/grid intent belongs to Stack/Grid), or a **semantic region** (that's Section). Two platform inflections define the current moment: the **`asChild`/Slot** model displacing the TypeScript-melting generic `as` prop, and the **zero-runtime / RSC reckoning** unwinding runtime CSS-in-JS (Primer v38 the worked cautionary tale).

---

## 1. Framing
A Box is bound to one job: be the neutral, token-aware container the rest of the category specialises. As the brief that **opens Layout**, its task is to settle the substrate — the spacing-token scale, the polymorphic model, the styling-engine delivery, the no-margin principle — so Stack/Grid/Card/Section inherit rather than re-derive.

The headline debate is real and the practice must take a side:
- **The style-prop Box** ships a polymorphic primitive with a large surface of token-mapped style props (`p`, `m`, `bg`, `display`, `flex`…). The argument *for*: developers inevitably hit bespoke layouts the constrained components don't cover, and a token-bound Box is a *controlled escape hatch* that keeps even one-offs tethered to the system's scales rather than hardcoded CSS.
- **The constrained / no-Box turn** argues that a god-component with a hundred style props *is* the problem: it's inline styles with extra steps, it leaks the constraint system, and it hides layout *intent* behind generic styling. Ship intent-revealing constrained components (Stack/Inline/Columns) + bare elements instead.

**The resolution — the constrained-over-open principle:** Box is the **substrate**, not the **authoring surface**. It is the low-level mechanism the system *authors* use to build Stack/Grid/Card; it is heavily restricted or de-emphasised in the *public* authoring surface. Day-to-day, reach for the constrained component that reveals intent; drop to a bare Box only when none fits. This reached a watershed in **GitHub Primer v38**, which removed the `Box` component and the `sx` prop outright, forcing CSS Modules for bespoke overrides — the clearest signal that the developer-facing Box is diminishing even as the substrate mechanism endures.

What it *isn't*: a **styled component** (neutral, no visual identity — unlike Card), a **layout engine** (the flex/grid intent belongs to Stack/Grid — a bare `Box display="flex"` doing manual spacing is the smell the constrained turn warns about), or a **semantic region** (Section, with a landmark). Why systems disagree: the should-we-ship-it question, the styling-engine delivery, and the polymorphism mechanic.

## 2. Anatomy and parts
Box has almost no *visual* anatomy — it's a `<div>` with no border, background, type, or states by default. Its anatomy is three invisible operational layers:
- **the rendering layer** — what DOM node / React element is injected (`as` legacy; **`asChild`/Slot** modern, merging props onto a consumer-provided child). The most consequential "part" (§6).
- **the box-model property layer** — the *intentionally limited* subset of CSS exposed as props: internal **padding**, dimensional constraints (`width`/`height`/`min`/`max`), **display** (restricted to `block`/`inline-block`/`none` in a well-architected Box — flex/grid are reserved for Stack/Grid), **overflow**, **position**, **border/radius**. Crucially *excludes external margin* (§3).
- **the token-translation engine** — intercepts systemic props (`px="gutter"`, `bg="surface-subtle"`) and resolves them to CSS. Its form is the load-bearing engineering choice (§11): a runtime CSS-in-JS evaluator (legacy MUI/Chakra on Emotion), a build-time static extractor → atomic classes (Panda CSS, Vanilla Extract), or a zero-runtime mapping to CSS Modules (Primer v38).
- **the (absence of) semantics** — no role, no accessible name, no states; deliberately empty so the consumer supplies meaning via `as`/`asChild`. A Box has no `:hover` unless polymorphed into an interactive element — and even then the state belongs to that element, not the Box.

## 3. Properties / API
The API *is* the governance mechanism — the props it exposes define the exact freedom permitted. The trend is toward rigidly bounded, strongly-typed utility props over unbounded style objects.

- **`as` vs `asChild`/Slot (the polymorphic model).** `as="section"` renders a different tag — conceptually simple but **disastrous for TypeScript** (it forces the checker to intersect Box's props with every attribute of the dynamic element — §11). The convergent modern answer is **`asChild`** (Radix Slot): Box renders no `<div>`, instead **merging its classes/styles/handlers onto the consumer's child** — `<Box asChild><button>…</button></Box>`. The type signature stays static and the consumer owns the semantics. The practice default: **`asChild`/Slot primary**, `as` a bounded convenience for simple tag swaps.
- **the style-prop surface** — token-mapped shorthands: spacing (`p`/`px`/`py`/`pt`…), color (`bg`/`color`/`borderColor`), sizing (`w`/`h`/`minW`/`maxW`), `borderRadius`, `overflow`, `position`, restricted `display`. Each value is a **token index** (`p={4}` → the 4th spacing token), never raw px.
- **the responsive syntax** — the field shifted from **array** (`p={[1,2,3]}` → sequential breakpoints; terse but obscures intent, forces memorising the breakpoint order) to **explicit object** (`p={{ mobile: 'small', tablet: 'medium' }}` — Braid, Radix Themes). The practice default: **object syntax** for readability and maintainability. (Both increasingly superseded by container queries + CSS — §13.)
- **`sx` vs discrete props** — MUI's `sx` is an escape-hatch object (`sx={{ p: 2 }}`); Chakra's flat discrete props (`p={2}`) resolve the same tokens with different ergonomics. The `sx` prop is in retreat (perf + RSC — §11).
- **what to expose vs withhold — the no-external-margin principle (the most contested API decision).** Expose padding/display/size/color/radius; **withhold margin** (`m`/`mt`/`mb`/`ml`/`mr`). Components must not own their external margin: a `marginTop="large"` bakes an assumption about *context* into the component, breaks encapsulation when it's moved, and triggers unpredictable **margin-collapsing**. Spacing *between* siblings belongs to the **parent layout's `gap`** (Stack/Grid) — which is *why* Stack exists (see stack). Field leaders (Braid, Polaris) mechanically omit margin props so the compiler rejects them.
- **the spacing-token scale** — every spacing prop resolves against the category's scale (§11); Box owns it, Stack/Grid `gap` and Card padding reference it.

## 4. States and variants
- **States: none.** Box is architecturally **stateless** — no `:hover`/`:focus`/`:active`/`:disabled` of its own. If it renders an interactive element via `asChild`, the state mechanics belong to that rendered element. (Zero-runtime engines like Panda offer conditional style props — `_hover={{ bg: … }}` — but these *extract to a static CSS class at build time*, so the React component stays stateless at runtime.)
- **Variants are an anti-pattern on Box.** A Box is a neutral canvas; introducing a `highlighted`/`elevated` variant *conflates layout mechanics with semantic presentation*. If a styling composition (a background + radius + shadow) recurs, **formalise it into a higher-order component** (Card, Callout, Section), don't add a Box variant. The real axes are not visual variants:
  - **rendered element:** the `as` target or `asChild`.
  - **styling-engine delivery:** runtime style-props / `sx` / utility classes / zero-runtime / CSS Modules — the same component contract, very different build/perf/RSC profiles (§11/§13).

## 5. Usage guidance
The governance model is the **constrained-over-open principle**: exhaust the intent-revealing layout options before defaulting to a bare Box.

- **Use a Box when** no higher-order layout engine fits:
  - a **custom composition** that isn't a Card/Callout but still needs token-bound padding/color/border;
  - a **decorative wrapper** needing a specific token background or border treatment;
  - the **polymorphic foundation** of a custom component (the base that accepts `asChild` + token props).
- **A Box is a code smell when** (prohibit these):
  - **manual spacing orchestration** — a `Box display="flex"` with hand-set spacing to push elements apart → use **Stack/Inline/Columns** (they own the `gap`).
  - **typographic styling** — a Box wrapping text to apply font size/weight/color → use **Text/Heading** (they own the type scale, line-height, responsive typography).
  - **recreating existing semantics** — padding + a subtle border + a shadow on a Box is a hand-rolled **Card**; it bypasses the system's ability to update cards globally and fragments the UI.
- A high incidence of bare Box in a codebase signals either developers bypassing constraints or the system *missing* a needed specialised primitive. Box is the floor, not the default.

## 6. Accessibility
Box's a11y story is short and sharp: **a default Box is a semantically-neutral `<div>` — no role, no name, not in the focus order — so the entire accessibility surface is the element it renders** (`as`/`asChild`).

- **The polymorphic trap works in both directions.**
  - *Forward:* `<Box as="button" onClick={fn}>` renders a `<button>`, but the Box doesn't know to wire keyboard handling, `aria-expanded`, or `disabled` — if the consumer doesn't, it's a button missing its contract.
  - *Reverse:* `<Box as="div" onClick={fn}>` is an **inaccessible click target** — not Tab-reachable, no Space/Enter, no announced role — and the semantically-agnostic Box will happily render the violation.
- **The rule:** the primitive has no inherent semantics, so it must not *obscure* the consumer's ability to author the correct ones — and `as` is for choosing the *correct* element, not for faking a component (a real button is the **Button** component, not `as="button"`).
- **`asChild` is the most robust mitigation.** By forcing the consumer to write the fully-formed, semantically-correct element as the child — `<Box asChild><button aria-pressed={…} disabled={…}>…</button></Box>` — the consumer retains full control over (and responsibility for) the semantics; the Box is just a token-resolving conduit. (Attempting to enforce semantics at the *type* level — "if `as="button"` then `onClick` is required and `href` forbidden" — rapidly hits the TS compiler's perf limits and produces opaque errors; `asChild` sidesteps it.)
- **WCAG:** nothing attaches to Box directly; the criteria attach to whatever it renders — **4.1.2** (name/role/value) if made interactive, **1.3.1** (info & relationships) if `as` is used for structure. The lightest a11y in the catalogue (cf. Divider — see divider), with the sharp polymorphism caveat.

## 7. Content guidelines
- Box **holds** content; it authors none — no label or copy patterns of its own.
- **The no-bare-text rule (inviolable).** Text, strings, or numbers must **never** be a direct child of a Box — `<Box>Unauthorized text</Box>` bypasses the typographic scale entirely. Wrap it: `<Box><Text>…</Text></Box>`. Typography (line-height, font tokens, responsive type scale) is owned by **Text/Heading**, not a styling `div`. Box wraps *components and explicit elements*, not raw text.
- If a Box wraps content with *group meaning* (a list, a region), that's a signal to give it the right `as` (or use Section/Stack), not leave it a neutral `div`.

## 8. Motion and transition
- Box ships **no motion of its own** — adding `animate`/`transition` to the base primitive is an anti-pattern (it bloats the bundle for the static-layout majority and violates separation of concerns).
- When motion is needed, **compose via `asChild`** onto a purpose-built animation primitive — `<Box asChild p="medium" bg="surface"><motion.div layout animate={…}>…</motion.div></Box>` — so the Box resolves the tokens and the `motion.div` owns the animation lifecycle. The `asChild` pattern makes this seamless and eliminates the need for a heavy dedicated `MotionBox` variant.
- Reduce-motion is the consumer's concern on whatever animation they attach; Box is motion-neutral.

## 9. Internationalization
- **Logical properties over physical (the systemic i18n role).** Box's spacing/position props must compile to **CSS logical properties** — `pl`/`paddingLeft` → `padding-inline-start`, `pr` → `padding-inline-end`, `mt` → `margin-block-start` — not physical `padding-left`/`right`. The engine intercepts shorthand/physical props and emits logical equivalents, so a layout flips correctly under `dir="rtl"` with **zero JS** (no `[dir="rtl"]` override stylesheets, no recalculation). Because Box is the substrate, **the whole Layout category inherits automated bidirectional support** — every Stack/Grid/Card built on it mirrors for free. A Box exposing only physical props is a latent RTL bug factory.
- The spacing-token scale is direction-agnostic (a 4/8px rhythm); its *application* is logical. Box is otherwise i18n-neutral (no text of its own — §7).

## 10. Naming
- **The field set:** **`Box`** is the canonical web name (Chakra, MUI, Radix Themes, Braid, Polaris, legacy Primer) — it references the CSS box model, an immediate cognitive link for web developers; **`View`** (React Native, Adobe Spectrum, React Aria — the cross-platform "viewable container" lineage); **`Block`** (Base Web/Uber — aligned with `display: block`, now fading as flex/grid dominate); occasionally `Frame`/`Primitive`.
- **The practice's default — `Box`.** The **layout descendants** are named for the display mechanics they enforce: **`Stack`** (vertical flow / 1D flex), **`Inline`** (horizontal flex), **`Grid`** (2D CSS grid), **`Columns`**, occasionally **`Flex`** (raw flexbox); plus **`Card`**/**`Section`** for the semantic surfaces — all carrying the intent Box deliberately lacks.
- **Don't overload Box** — resist making Box *also* a Stack (a `display="flex"` convenience) or *also* a Card; keep it neutral and let the named components carry meaning (the constrained-over-open principle expressed in naming).
- **Aliases to map:** View, Block, Frame, Primitive, `<div>` (the thing it abstracts).

## 11. Implementation notes
- **The polymorphic `as` TypeScript explosion (the headline).** A fully-generic `as` prop — typing the chosen element's attributes for *any* tag, plus `ref` forwarding (`PolymorphicComponentPropsWithRef`, the `Omit`/`ComponentPropsWithRef` chains) — forces the compiler to compute massive type intersections at **every Box instantiation** ("megamorphic call sites"), producing catastrophic slowdowns (5000ms+ inference per file) and **OOM errors in CI**. The convergent escape is **`asChild` + the Radix `Slot`**: when `asChild`, Box renders `Slot` instead of `<div>` and uses `cloneElement` to merge its props onto the single child — concatenating `className`, deep-merging `style`, and chaining event handlers so both parent and child `onClick` fire. The type signature stays **static**, eliminating the intersection cost. (`const Comp = asChild ? Slot : "div"`.) Shared with Button/Link (see button, link).
- **The styling-engine delivery + the zero-runtime / RSC reckoning (the big, volatile inflection).** Classic style-prop Boxes ran on **runtime CSS-in-JS** (Emotion under MUI/Chakra): evaluate props in the browser, hash a class, inject a `<style>` tag. Two fatal flaws now: (1) **V8 JIT de-optimisation** — dynamically-shaped style objects cause hidden-class transitions / megamorphic call sites that block the JIT's optimisation path; (2) **RSC-incompatibility** — runtime evaluation can't run in React Server Components (no client context, must serialise to static HTML). The field bifurcated: **build-time static extraction** (Panda CSS — the Chakra team's own successor — and Vanilla Extract: AST-analyse `p={4}` → emit `.p_4{padding:1rem}` to a `.css` file before the browser), or a **hard pivot to CSS Modules / utility classes** (**Primer v38** deprecated the Box + `sx` + styled-components; Tailwind/shadcn skip the Box entirely). **The practice POV: build the token-prop ergonomics on a zero-runtime engine** — the authoring experience can survive; the runtime must not. *Date this; it's the most volatile claim in the brief.*
- **The spacing-token scale (defined once, for the category).** Three paradigms: **numeric base** (4/8px multipliers — `1`=4px; MUI/Tailwind; predictable but tempts pixel-thinking), **t-shirt** (`none`/`xs`/`sm`/`md`/`lg` — Braid/Base Web/Radix Themes; enforces relational thinking), **semantic/intent** (`gutter`, `stack-gap-condensed` — Primer; the highest constraint, a token bound to its purpose). Box owns whichever scale; **Stack/Grid `gap` + Card padding resolve against the same one**.
- **The no-external-margin enforcement** — mechanically **omit `m`/`mt`/`mb`/… from the `BoxProps` type** so the compiler rejects `marginTop`; inter-sibling spacing is forced onto the parent layout's `gap`, guaranteeing encapsulation and eliminating margin-collapse unpredictability.
- **The responsive prop implementation** (array/object → media queries per prop) is increasingly superseded by **container queries + CSS** (the component responds to its container, not the viewport) — which the runtime responsive-prop syntax can't express well.
- **Headless vs opinionated** — Box is the *most* substrate-like component: ship the token-prop ergonomics + the Slot + the scale, themed by the consumer's tokens; the **zero-runtime delivery is the load-bearing engineering choice**, not the prop names.

## 12. Related and alternative components
- **Substrate FOR (the inheritors):** **Stack** (1D flex, owns `gap`), **Inline** (horizontal flex), **Grid**/**Columns** (2D, tracks/areas/`gap`), **Card** (a Box pre-binding background/radius/padding tokens), **Section** (a semantic region) — all built on Box, all inheriting the spacing-token scale + the `asChild` polymorphism (Stack/Grid/Card briefed — see stack/grid/card; Section not yet briefed; this brief is their substrate).
- **Shares (the polymorphic substrate):** the **`asChild`/Slot** mechanism is identical to the one **Button** and **Link** use (the link-vs-button and router-`<Link>` cases — see button, link); Box formalises it for Layout, ensuring composition mechanics are uniform across the system.
- **Shares (the spacing-token scale):** the whole **Layout category** + every padded component (a design-token-system concern — see 00-principles / the token files).
- **Alternative to:** a **styled component** (when a styling composition is reused and meaningful, *name* it), **bare HTML + utility classes** (the Tailwind/shadcn no-Box position — token-mapped classes on plain elements, bypassing the proprietary substrate), and the **constrained layout components** (Stack/Grid — the recommended authoring surface over a bare Box).

(The Layout substrate — the polymorphic, token-aware, semantically-neutral primitive that opens the category. Built *with*, not reached for first (the constrained-over-open principle). The substrate Stack/Grid/Card/Section inherit; it formalises the `asChild`/Slot polymorphism Button/Link use and owns the spacing-token scale the category shares. See button/link for the shared Slot polymorphism, stack/grid/card for the inheritors, section when briefed for the last inheritor, divider for the comparably-thin a11y, 00-principles for the token system. 03-component-library; 29 for the docs template.)

## 13. Field POV evolution
1. **2018–2020 — the era of infinite freedom.** Styled System popularised the Box as a direct prop→token mapping; "everything is a Box," responsive array props, the `sx` escape hatch (Chakra, MUI, Theme UI). Maximum developer velocity; encapsulation and perf frequently sacrificed.
2. **2021–2023 — the TypeScript and margin reckoning.** Enterprise scale exposed the flaws: the generic polymorphic `as` buckled the TS compiler (slow CI, OOM, opaque errors), and ad-hoc margins made layouts fragile. Braid/Seek pioneered the strict **no-margin** philosophy and the push from the unbounded Box toward constrained engines (Stack/Inline).
3. **2024–2026 — the zero-runtime / RSC inflection.** React Server Components rendered runtime CSS-in-JS obsolete and the god-Box a liability. The field bifurcated: **static extraction** (Panda CSS, Vanilla Extract — preserve the style-prop DX without the runtime cost) vs a **hard pivot** to CSS Modules / utility classes (**Primer v38** deprecating the Box + `sx`; the shadcn/ui ecosystem). Today, if a Box ships at all, it must be zero-runtime-compiled, forbid external margins, and manage polymorphism via `asChild`/Slot.
4. **`asChild`/Slot settled** over the `as`-typing nightmare as the composition mechanism (now shared across Button/Link/Box).
5. **The no-external-margin principle hardened** from a nicety to a near-settled rule — and is *why* Stack exists.

## 14. Sources cited
(Conservative; reconcile with external — and the styling-engine landscape is volatile, so platform-state claims are flagged unverified.) **Chakra UI** — `Box` (the canonical style-prop polymorphic primitive, `as`, style props) + **Panda CSS** (the Chakra team's zero-runtime successor) (2024–2026); **Theme UI** — `Box` (the Styled System lineage, `sx`, responsive arrays) (2024–2026); **MUI** — `Box` (the `sx` prop, `component` prop, system props; Emotion runtime) (2024–2026); **Radix Themes + Radix Primitives** — `Box` + the **`asChild` Slot** pattern (the polymorphic substrate) (2024–2026); **Braid / Seek** — `Box` + `Stack`/`Inline`/`Columns` (the constrained-over-open, no-external-margin school; object responsive syntax; t-shirt scale) (2024–2026); **Tailwind + shadcn/ui** — the utility-classes-no-Box position (2024–2026); **GitHub Primer** — `Box` + the **v38 deprecation** of Box/`sx`/styled-components toward CSS Modules (the worked cautionary tale) (2024–2026); **Shopify Polaris** — `Box` (token props, the layout primitive; withholds margin) (2024–2026); **Adobe Spectrum / React Aria** — `View` (the RN-style primitive) (2024–2026); **Base Web (Uber)** — `Block` (2024); **Styled System** — the historical prop→token-mapping lineage (2018–2021); **Vanilla Extract / Panda CSS** — the zero-runtime static-extraction successors (2024–2026); **WAI-ARIA / HTML** — Box is a semantically-neutral `<div>` (no role); the `as`-produces-wrong-semantics trap (both directions). WCAG 2.2 (W3C Recommendation, Oct 2023) — 4.1.2, 1.3.1 (attach to whatever Box renders).

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
  stand on. A <div> by default, exposing the design system's constraints (the spacing
  scale, color tokens, the box model) through a token-mapped prop surface. The
  headline contested question — should a DS even ship a Box? — is resolved via the
  CONSTRAINED-OVER-OPEN principle: Box is the SUBSTRATE / low-level escape hatch, NOT
  the recommended authoring surface (reach for the intent-revealing Stack/Grid first;
  Primer v38 removed the Box+sx outright). NOT a styled component (neutral), NOT a
  layout engine (that's Stack/Grid), NOT a semantic region (that's Section).
  Formalises the asChild/Slot polymorphism Button/Link use; owns the spacing-token
  scale the category inherits.
anatomy:
  parts:
    - "rendering layer: the injected DOM node / React element (as legacy; asChild/Slot modern — merges props onto a consumer child). The most consequential 'part'"
    - "box-model layer: the INTENTIONALLY LIMITED CSS subset — padding, size (w/h/min/max), display (restricted to block/inline-block/none; flex/grid reserved for Stack/Grid), overflow, position, border/radius; EXCLUDES external margin"
    - "token-translation engine: intercepts systemic props (px='gutter', bg='surface-subtle') -> CSS; form is the load-bearing choice (runtime CSS-in-JS / static-extraction / CSS Modules)"
    - "the (absence of) semantics: no role/name/states — deliberately empty so the consumer supplies meaning via as/asChild; no :hover unless polymorphed (and then the state is the rendered element's)"
api:
  shares:
    - button/link    # the asChild/Slot polymorphism (the link-vs-button + router cases)
  substrate-for:
    - stack          # 1D flex, owns gap (not yet briefed)
    - grid           # 2D, tracks/areas/gap (not yet briefed)
    - card           # a Box pre-binding bg/radius/padding tokens (the styled surface)
    - section        # a semantic region (not yet briefed)
  props:
    - {name: asChild, type: boolean, default: false, required: false, description: "Radix Slot — render no div, merge props/style/handlers onto the consumer's child via cloneElement; the PRIMARY polymorphism mechanism (static type sig, sidesteps the as-explosion)"}
    - {name: as, type: ElementType, default: div, required: false, description: "render a different tag; a bounded convenience — the fully-generic form melts the TS compiler (use asChild)"}
    - {name: "style-props (p/px/py/pt.../bg/color/borderColor/w/h/minW/maxW/borderRadius/overflow/position)", type: "token | responsive", default: ~, required: false, description: "token-mapped shorthands; each value a TOKEN index (p={4} -> 4th spacing token), not raw px"}
    - {name: display, type: "'block' | 'inline-block' | 'none'", default: block, required: false, description: "RESTRICTED; flex/grid mechanics reserved for Stack/Grid (the constrained-over-open principle)"}
    - {name: responsive-syntax, type: object, default: ~, required: false, description: "object (p={{mobile:'small',tablet:'medium'}}) PREFERRED over array (p={[1,2,3]}) for readability; both superseded by container queries + CSS"}
    - {name: sx, type: object, default: ~, required: false, description: "MUI's escape-hatch object (sx={{p:2}}) vs Chakra's flat discrete props — same tokens, different ergonomics; in RETREAT (perf + RSC)"}
    - {name: margin, type: "FORBIDDEN", default: ~, required: false, description: "external margin (m/mt/mb/ml/mr) is OMITTED from the type (compiler rejects it) — the no-external-margin principle; inter-sibling spacing belongs to the parent's gap (this is WHY Stack exists)"}
  spacing-scale: "the category scale all spacing props resolve against; Box OWNS it, Stack/Grid gap + Card padding REFERENCE it"
states:
  runtime: []   # NONE — architecturally stateless; if it renders an interactive element via asChild, the state is that element's
  zero-runtime-conditionals: "Panda-style _hover={{bg:...}} EXTRACT to a static CSS class at build time — the React component stays stateless at runtime"
variants:
  anti-pattern: "variants on Box (highlighted/elevated) CONFLATE layout with semantic presentation — formalise a recurring composition into Card/Callout/Section instead"
  rendered-element: "the as target (div/section/span/ul/...) or asChild"
  styling-engine-delivery: [runtime-css-in-js, sx, utility-classes, static-extraction, css-modules]   # same contract, very different build/perf/RSC profiles
accessibility:
  wcag-criteria: ["4.1.2", "1.3.1"]   # nothing direct; criteria attach to whatever it RENDERS
  semantics: "a semantically-neutral div — NO role/name/states/focus; the WHOLE a11y story is the element it renders (as/asChild)"
  polymorphic-trap-both-directions:
    forward: "as='button' renders a <button> but Box doesn't wire keyboard/aria-expanded/disabled — inaccessible if the consumer doesn't"
    reverse: "as='div' onClick = an inaccessible click target (not Tab-reachable, no Space/Enter, no role) — Box renders the violation happily"
  rule: "the primitive has no inherent semantics, so it must not OBSCURE the consumer's correct ones; as is for the CORRECT element, not for faking a component (a real button is the Button component)"
  asChild-mitigation: "force the consumer to write the fully-formed semantic element as the child (<Box asChild><button aria-pressed disabled>); type-level enforcement (require onClick if as=button) hits the TS perf wall — asChild sidesteps it"
  note: "the lightest a11y in the catalogue (cf. Divider) with the sharp polymorphism caveat"
content:
  holds-not-authors: "Box holds content, authors none — no label/copy patterns"
  no-bare-text: "INVIOLABLE — text/strings/numbers must NEVER be a direct child of a Box (bypasses the type scale); wrap in Text/Heading. Box wraps components/elements, not raw text"
  signal: "wrapping content with group meaning (a list/region) is a signal to set the right as (or use Section/Stack)"
motion:
  own: none   # adding animate/transition to the base primitive is an anti-pattern (bundle bloat, separation-of-concerns)
  compose: "via asChild onto an animation primitive (<Box asChild p='medium'><motion.div layout animate={...}>) — Box resolves tokens, motion.div owns the animation lifecycle; no heavy MotionBox variant needed"
  reduce-motion: "the consumer's concern on the attached animation; Box is motion-neutral"
i18n:
  logical-properties: "spacing/position props COMPILE to CSS logical properties (pl/paddingLeft -> padding-inline-start, pr -> padding-inline-end, mt -> margin-block-start), NOT physical — so layouts flip under dir=rtl with ZERO JS"
  category-inheritance: "because Box is the substrate, the WHOLE Layout category (Stack/Grid/Card) inherits automated bidirectional support for free"
  scale: "the spacing-token scale is direction-agnostic (4/8px rhythm); its APPLICATION is logical"
  otherwise: "i18n-neutral (no text of its own)"
implementation:
  - "the polymorphic `as` TypeScript explosion (the headline): a fully-generic as + ref (PolymorphicComponentPropsWithRef, Omit/ComponentPropsWithRef chains) forces massive type intersections at EVERY instantiation (megamorphic call sites) -> 5000ms+ inference/file + OOM in CI. ESCAPE: asChild + Radix Slot — render Slot not div, cloneElement merges props onto the single child (concat className, deep-merge style, chain handlers); the type sig stays STATIC. const Comp = asChild ? Slot : 'div'"
  - "the zero-runtime/RSC reckoning (the big, VOLATILE inflection): runtime CSS-in-JS (Emotion) has two fatal flaws — V8 JIT de-optimisation (dynamic style-object shapes -> hidden-class transitions / megamorphic call sites block the JIT) and RSC-incompatibility (can't run server-side). Field bifurcated: STATIC EXTRACTION (Panda CSS [Chakra's successor], Vanilla Extract — AST -> atomic .css at build) vs a HARD PIVOT to CSS Modules/utility classes (Primer v38 deprecated Box+sx+styled-components; Tailwind/shadcn skip the Box). Practice: build the token-prop ergonomics on a zero-runtime engine. DATE IT"
  - "the spacing-token scale (defined once for the category): NUMERIC (4/8px multipliers — MUI/Tailwind; predictable, tempts pixel-thinking), T-SHIRT (none/xs/sm/md/lg — Braid/Base Web/Radix Themes; relational), SEMANTIC/INTENT (gutter, stack-gap-condensed — Primer; highest constraint). Stack/Grid gap + Card padding resolve against the same one"
  - "the no-external-margin enforcement: OMIT m/mt/mb/... from BoxProps so the compiler rejects marginTop; inter-sibling spacing forced onto the parent's gap (encapsulation + no margin-collapse)"
  - "responsive prop impl (array/object -> media queries per prop) increasingly superseded by CONTAINER QUERIES + CSS"
  - "headless vs opinionated: the MOST substrate-like component — ship token-prop ergonomics + the Slot + the scale, themed by consumer tokens; the zero-runtime DELIVERY is the load-bearing engineering choice"
composition:
  substrate-for: [stack, inline, grid, columns, card, section]
  shares-polymorphism-with: [button, link]      # asChild/Slot
  shares-scale-with: [layout-category, "every padded component"]   # the spacing-token scale (a token-system concern)
  alternative-to: [styled-component, "bare HTML + utility classes (Tailwind/shadcn no-Box)", stack, grid]   # + the constrained-over-open recommendation
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "SHOULD a DS even ship a Box? style-prop Box (Chakra/Theme UI/MUI/Radix Themes/Polaris) vs the constrained/no-Box turn (Braid Stack/Inline; Tailwind+shadcn; Primer v38 removed it). Practice: Box is the SUBSTRATE not the authoring surface (constrained-over-open)"
    - "as vs asChild/Slot polymorphism (practice: asChild primary)"
    - "style-props vs sx vs utility-classes vs zero-runtime — the RSC/perf reckoning forcing the move OFF runtime CSS-in-JS"
    - "spacing scale paradigm: numeric vs t-shirt vs semantic/intent"
    - "margin: expose vs withhold (the no-external-margin principle says withhold)"
  trap:
    - "the polymorphism wrong-semantics trap BOTH directions (as='button' with no button behaviour; as='div' onClick = unreachable click target)"
    - "the fully-generic `as` TypeScript explosion -> megamorphic call sites, 5000ms+ inference, CI OOM (use asChild/Slot)"
    - "runtime CSS-in-JS: V8 JIT de-opt + RSC-incompatibility (move to zero-runtime)"
    - "a Box with 15 style props = inline styles with extra steps; recreating a Card (padding+border+shadow) by hand; manual spacing via display=flex (use Stack); wrapping bare text (use Text)"
    - "exposing physical (padding-left) not logical (padding-inline-start) props -> RTL bugs"
    - "components owning external margin (breaks encapsulation + margin-collapse; use the parent's gap)"
    - "adding variants to Box (conflates layout with presentation -> Card/Callout/Section)"
  inherited: []   # Box is the substrate; the category inherits FROM it
  role-in-family: "the Layout substrate — the polymorphic, token-aware, semantically-neutral primitive that opens the category; built WITH not reached-for-first (constrained-over-open); the substrate Stack/Grid/Card/Section inherit; formalises the asChild/Slot polymorphism Button/Link use; owns the spacing-token scale"
  evolution:
    - "2018-20 infinite freedom (Styled System; everything-is-a-Box; sx; velocity over encapsulation/perf)"
    - "2021-23 the TS + margin reckoning (the generic-as compiler buckle; Braid's no-margin + constrained-layout turn)"
    - "2024-26 the zero-runtime/RSC inflection -> static extraction (Panda/Vanilla Extract) vs hard pivot to CSS Modules/utility (Primer v38; shadcn)"
    - "asChild/Slot settled over the as-typing nightmare (shared with Button/Link)"
    - "the no-external-margin principle hardened (why Stack exists)"
  unverified:
    - "external 2026 version numbers + the exact state of each system's CSS-in-JS migration (VOLATILE — the styling-engine landscape moves fast)"
    - "Primer v38 removing Box/sx/styled-components — verify the exact version against current releases"
    - "Panda CSS adoption + the degree container queries have displaced responsive props per system"
```

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-16-component-box/` (16 June 2026), the thirty-fifth brief and the one that **opens the Layout category** — the polymorphic, token-aware layout substrate Stack/Grid/Card/Section will stand on (the same substrate-first move that opened Form with Text Field and the Overlay positioning substrate with Popover). It formalises the `asChild`/Slot polymorphism Button and Link already lean on, and owns the spacing-token scale the whole category inherits. The two passes converged almost completely — the should-a-DS-even-ship-a-Box debate (the style-prop Box vs the constrained/no-Box turn) resolved via the constrained-over-open principle (Box is the substrate, not the authoring surface), the polymorphic `as`-vs-`asChild`/Slot model, the style-props/`sx`/utility-classes question + the zero-runtime/RSC reckoning, the spacing-token scale, and the no-external-margin principle. There was no genuine fork; the external pass mostly **sharpened and dated** the Claude pass with concrete field detail — **Primer v38** as the worked deprecation milestone (Box + `sx` + styled-components removed for CSS Modules), the **V8 JIT de-optimisation** mechanism behind runtime CSS-in-JS (megamorphic call sites / hidden-class transitions, not merely per-render cost) and the **5000ms+ inference / CI OOM** cost of the generic `as`, the **three-tier spacing scale** (numeric / t-shirt / semantic-intent), the **object-over-array** responsive resolution, the **restriction of `display` to block/inline-block/none** (flex/grid reserved for Stack/Grid), the **reverse a11y trap** (`as="div" onClick` = an unreachable click target alongside the `as="button"` forward trap), the `cloneElement`/Slot merge detail (`const Comp = asChild ? Slot : "div"`), and the Framer-Motion-via-`asChild` composition. Claude-pass contributions: the substrate framing and the constrained-over-open resolution, the substrate/inheritance map, the Box-vs-styled-component-vs-layout-engine boundary, and the no-bare-text content rule. The styling-engine landscape is the most volatile claim in the catalogue (cf. Select's `appearance: base-select`); the 2026 version numbers, Primer v38, Panda adoption, and the container-query displacement are flagged unverified. Conformant to `components/_schema.md`. The first Layout brief — Stack, Grid, Card, and Section now have their substrate.*

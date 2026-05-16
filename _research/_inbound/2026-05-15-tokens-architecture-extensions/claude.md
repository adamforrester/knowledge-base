# Tokens architecture — spec depth, computed tokens, density

> Research synthesis for the layer underneath the practice's established token positions. Three threads: the DTCG specification at practitioner depth, the relational/computed-token frontier, and density as a token concern. Web verification was unavailable for this run — claims about live tool/spec state are flagged with verification paths so they can be re-checked against the source before being promoted into the numbered files.

---

## 1. The DTCG specification at practitioner depth

### 1.1 The shape of the spec as of mid-2026

The W3C Design Tokens Community Group has been working in a hands-off draft mode since its formation in 2020. There is no Recommendation track candidate; what the field calls "DTCG-compliant" is conformance to the **Editor's Draft** of the Design Tokens Format Module. Treat that as load-bearing context: every claim about what the spec "says" is really a claim about what the current editor's draft says, and the draft is a moving target.

The stable core — the parts that have not changed materially since the 2023 consolidation and that every serious tool now implements — is small:

- The file format is JSON. Tokens are objects with `$value`, optional `$type`, optional `$description`, optional `$extensions`. Groups are nested objects without those `$`-prefixed keys.
- Aliases are strings of the form `"{group.subgroup.token}"` resolved against the root of the merged token set.
- The reserved key prefix is `$`. Anything else at the same nesting level is either a token (if it has `$value`) or a group.
- The primitive `$type`s — `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number` — are stable enough that round-tripping primitives between tools is no longer a known failure mode.

The contested or under-specified layer, which is where most real architectural decisions live, is much larger. The honest framing for the senior practitioner is that DTCG is **a JSON shape and a set of `$type` definitions, plus a list of things the spec has deliberately punted on**.

What is genuinely settled (verification path: DTCG Editor's Draft, Format Module sections on file format, types, and aliases):

- File format and group/token distinction.
- The reserved `$`-prefix namespace.
- Alias syntax and the requirement that aliases be lazily resolved (i.e. the consumer resolves at use time, not at write time).
- The primitive type list above.
- `color`'s representation as either a hex string or — added in the 2024 colour work — a structured object with `colorSpace` and `components` to support wide-gamut workflows. This is where the spec started honouring the CSS Color Module Level 4 reality.

What is **drafted but not stable** — implementations diverge and the spec language is still moving:

- The full set of composite types and especially the exact shape of `typography`, `border`, `shadow`, `transition`, `gradient`, `strokeStyle`.
- The behaviour of aliases that point into the *components* of a composite (i.e. is `{color.brand}` legal as the `color` sub-value of a `border` token, and is the resulting token still a `border` token or something else).
- The treatment of `$type` inheritance from groups. Some tools propagate, some require explicit declaration on every token.
- The shape of `$extensions` namespacing — convention is reverse-DNS keys (`com.tokens-studio.modify`), but conformance does not require it.

What is **explicitly out of scope** in the current draft — the spec punts and tells implementers to handle it via `$extensions` or a sibling spec:

- Modes/themes. The spec has no concept of a value-set that varies by mode. The Figma Variables data model exposes modes as a first-class concept and most tools have followed, but DTCG itself encodes a single value per token and lets tooling express the mode dimension out-of-band.
- Conditional values (light/dark, density, breakpoint).
- Math expressions in `$value`.
- Validation rules beyond JSON parseability and `$type` shape conformance.
- Token deprecation lifecycle (`$deprecated` has been discussed but is not in the stable surface as of mid-2026 — verification path: DTCG GitHub issue tracker, specifically the deprecation-metadata issue thread).

This shape is the practical answer to "is DTCG enough on its own": it is enough for the *transport* problem (a file you can hand to any compliant consumer and have it round-trip primitives faithfully), and it is not enough for the *architecture* problem (how the system varies across modes, how values relate to each other, how the system evolves). The architecture problem is the job of the layer above DTCG — Tokens Studio's resolvers, Style Dictionary's transforms, the consuming pipeline.

### 1.2 `$value`, `$type`, `$description`, `$extensions`

`$value` is the only required key on a token object. Its allowed shape depends on `$type`. For primitives, `$value` is either a string (`"#0066cc"`, `"16px"`, `"600"`), a number, or an alias reference. For composites, `$value` is an object whose sub-keys are themselves either primitive values or alias references.

The under-specified behaviour in `$value`:

- **Unit ambiguity.** `dimension` allows pixel and rem strings (`"16px"`, `"1rem"`); the editor's draft has added unit metadata in recent iterations, but tools historically parsed and stripped units inconsistently. The pragmatic position: keep dimensions in a single unit at the primitive layer, do the unit conversion in the build step (Style Dictionary transforms are the canonical place), and don't rely on every consumer respecting the unit string. Verification path: DTCG Editor's Draft, `dimension` type definition; Style Dictionary `size/px`, `size/rem` transforms.
- **Number vs. dimension for unitless cases.** Line-height `1.5` is a `number`, line-height `24px` is a `dimension`. The composite `typography` token has to allow both, and not every tool handles the polymorphism. Tokens Studio and Style Dictionary do; some Figma plugin layers don't, which is the most common round-trip failure in our experience.
- **Alias-as-value vs. literal-as-value at the same nesting level.** Inside a composite, `{color.brand}` and `"#0066cc"` both have to be legal in the same slot. This is fine in spec, but tools that do schema validation often have to special-case the union type.

`$type` is optional in spec — the consumer can infer from `$value` shape — but every production toolchain treats it as effectively required because shape inference fails on alias-heavy token sets (you can't tell whether `{color.brand}` resolves to a colour or a dimension until you walk the alias graph). **Mandate `$type` on every leaf token at the primitive layer** as a non-negotiable practice rule.

`$type` *inheritance* from groups is where the spec is loosest. The editor's draft permits a group to declare a `$type` that propagates to descendants that omit it. In practice:

- Tokens Studio writes `$type` on every leaf. Style Dictionary respects inheritance. Figma Variables doesn't have an equivalent.
- If your write tool (Tokens Studio) is explicit and your read tool (Style Dictionary) supports inheritance, you never hit the divergence. If you have a hand-edited token set that uses group-level `$type`, you will hit it the first time you point a non-Style-Dictionary consumer at it.

The conservative rule: don't rely on `$type` inheritance for portability. Write it on every leaf. The cost is verbosity in source files; the benefit is that the file is unambiguous to any compliant parser.

`$description` is free-form text and tools treat it as a string field. There is no spec guidance on length, markup, or audience. Three competing uses fight for that field:

1. Designer-facing intent ("Primary brand colour, use only for top-level CTAs").
2. Engineer-facing constraint ("Maps to `--color-brand-primary` in CSS, do not alias from outside the brand collection").
3. Machine-readable metadata (deprecation reason, replacement target, JSDoc-style annotations).

The field has not converged on a convention. The practitioner's call: pick one audience per system and put the other audiences in `$extensions`. If you're shipping to Figma MCP consumers, `$description` is increasingly the *machine-readable intent* field because LLMs read it directly, and the other audiences move to `$extensions.your-org.docs` or similar.

`$extensions` is the spec's escape hatch and the practitioner's load-bearing surface. The convention is reverse-DNS namespacing (`com.tokens-studio.modify`, `org.w3.dtcg.deprecated`) but the spec doesn't enforce it and not every tool follows. What tools write into `$extensions` today (verification path: Tokens Studio docs on the `studio.tokens` extension namespace; Style Dictionary docs on the `_originalValue` extension; Figma's tokens export plugins each invent their own):

- **Tokens Studio**: `studio.tokens.modify` for math operations applied to a value (the `modify` block holds the operation, the operand, and the input token reference).
- **Style Dictionary**: original values, transform metadata, file-of-origin tracking.
- **Figma Token Studio plugin**: extra metadata about which Figma variable/collection a token corresponds to.
- **Custom extensions**: deprecation status, owner, contribution metadata, theme-applicability hints, ARIA pairing (the pair-token references in our 14-accessibility file are a natural `$extensions` candidate).

The practitioner risk in `$extensions` is silent breakage. There is no validation, so a consumer that doesn't recognise a namespace ignores it without warning, and a producer that changes its extension shape between versions can break downstream tooling that read the old shape. **Treat `$extensions` consumption as a soft contract** — defensive parsing, fallback to the canonical `$value`, log unknown namespaces in CI rather than failing.

### 1.3 Composite tokens — what the spec says vs. what tools do

Composite tokens are the part of DTCG where the round-trip claim breaks down most often. They are also the part where the spec is most likely to change in the next year.

**Typography**. The spec defines a `typography` composite with sub-keys for `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`. Recent draft work has added `fontStyle` and the question of whether to include `textTransform`, `textDecoration`. The fault line:

- Figma's text style model includes properties that map cleanly to the composite (family, size, weight, line height, letter spacing).
- CSS doesn't have a single `font` shorthand that takes all of these — line-height-in-font is a constraint, `letter-spacing` lives separately, `text-transform` and `text-decoration` are properties on the element, not the font.
- Native platforms (iOS UIFont, Android Typeface, Compose TextStyle) each have a different decomposition.

The practical consequence: `typography` round-trips between Tokens Studio and Style Dictionary correctly. It does *not* round-trip cleanly between Figma and code without an opinionated mapping layer, because Figma stores the values per-variable and as text-style properties, and the question of which is canonical is a workflow decision, not a spec decision. Our position: **the typography composite is a useful authoring shape for designers, and a poor consumption shape for engineers** — flatten on export, emit individual CSS custom properties, and treat the composite as an editorial convenience rather than a runtime artefact.

**Shadow**. The spec defines a `shadow` composite with `offsetX`, `offsetY`, `blur`, `spread`, `color`, and (in recent draft work) an `inset` boolean. The under-specified part is *layered* shadows. CSS `box-shadow` accepts a comma-separated list; the DTCG composite as a single object can't express that without making `$value` an array. The current draft handling — `$value` may be an array of shadow objects — was a 2024 addition and is what most tools now implement, though older Style Dictionary versions and older Tokens Studio exports flatten to a single shadow. Verification path: DTCG Editor's Draft, `shadow` type; Style Dictionary 4.x release notes for shadow array support.

**Border**. The composite is `color`, `width`, `style`. The spec's `style` is constrained to a `strokeStyle` enum (`solid`, `dashed`, `dotted`, etc.) plus a draft proposal for a structured `strokeStyle` object that expresses dash patterns. The pragmatic problem: CSS doesn't have a token-shaped border the way it has a token-shaped colour. Engineers consume the components individually (`border-color`, `border-width`, `border-style`) more often than they consume the shorthand. Same advice as typography: useful for authoring, flatten for consumption.

**Transition**. `duration`, `delay`, `timingFunction`, `property`. The under-specified part is `property` — what does it mean to ship a transition token that bakes in which CSS property it animates? Most production token sets ship `duration` and `cubicBezier` as separate primitives and let the consumer compose. The composite is in the spec but is the least-used composite in practice (verification path: anecdotal — Tokens Studio default export, Style Dictionary examples, surveying a handful of public token sets like GitHub Primer, Atlassian, Adobe Spectrum).

**Gradient**. Recent addition. `$value` is an array of colour stops. Round-trip fidelity is the weakest of the composites because CSS gradient syntax is far richer than the composite (angle vs. position, multiple gradient functions, colour-stop hints) and the spec does not yet cover the full surface.

The principle that holds across all four: **composite tokens are authoring conveniences for the design tool side and decomposition targets for the engineering side**. Treat the composite as the canonical *intent* and the individual primitives as the canonical *output*. Where Style Dictionary or your pipeline gives you a choice, emit both — the composite for tools that consume it (some Figma plugins, some documentation rendering), and the decomposed primitives for application code.

### 1.4 Alias resolution semantics

The spec rules on aliases, as of the current draft:

- An alias is a string of the form `"{path.to.token}"` where the path is dot-separated and resolves against the root of the merged token set.
- Resolution is lazy — the consumer resolves at evaluation time, not at write time. A token file with unresolved aliases is still a valid DTCG file.
- Alias chains are permitted. `a -> b -> c` resolves `a` to whatever `c` resolves to.
- Circular references are forbidden but the spec does not prescribe a detection algorithm; consumers are expected to detect and error.

Where the spec is under-specified in practice:

**Cross-file and cross-collection aliasing.** DTCG defines a single JSON file. A real system has multiple files (one per collection, often one per theme). Whether `{brand.color.primary}` in `theme-dark.json` can reference a token defined in `primitives.json` depends entirely on the merge step the consumer performs *before* alias resolution. Style Dictionary merges all source files into a single object before resolving; Tokens Studio's multi-set model is more constrained because sets have explicit visibility rules. The practitioner consequence: **the merge order is a spec gap that you must own in your pipeline**. Document which files merge into which, in which order, with what conflict resolution.

**Alias to a deleted token.** The spec says nothing prescriptive. Style Dictionary errors at build time; Tokens Studio shows a broken-reference warning in the UI; Figma Variables shows the reference as broken and falls back to the last-known value. The recommended practice: fail the build, never ship a broken alias to runtime. The CI gate is a one-line check — walk every alias, ensure the target exists.

**Alias to a token of a different `$type`.** `{color.brand}` used as the value of a `dimension` token. The spec position is that the resolved value must conform to the consumer's expected type; mismatch is an error. Tools enforce inconsistently. Style Dictionary 4.x added stricter type checking; Tokens Studio is more permissive because designers routinely use the dot-path syntax as a string and recover the type at the consumer.

**Partial aliasing into composites.** Discussed above — legal in spec, fragile in tooling.

**Alias resolution under modes.** Genuinely contested. If `color.surface.primary` aliases `color.neutral.100` in light mode and `color.neutral.900` in dark mode, where does the conditional live? Three options the field is split across:

1. **Mode lives in the consumer.** The token file has a single value (an alias to `color.neutral.100`), and the dark-mode override is encoded in a sibling token file (`theme-dark.json`) that re-aliases. This is the Style Dictionary norm, and it's what the DTCG spec implicitly supports because the spec has no mode concept.
2. **Mode lives in `$extensions`.** A single token file with `$extensions.modes.dark = "{color.neutral.900}"`. This is the Tokens Studio Themes feature, dressed in extension clothes.
3. **Mode lives in the value.** `$value` becomes an object keyed by mode name. This is the Figma Variables shape and the most ergonomic for designers, but it is *not* in the DTCG spec and the spec authors have signalled they don't want it there (verification path: DTCG GitHub discussions on the "modes" topic, around 2024-2025).

The convergent answer in 2026 is option 1 for *interchange* (the file you ship to consumers) and option 3 for *authoring* (the editor experience), with the pipeline doing the conversion. This is also where the gap between Figma Variables and DTCG bites hardest — the export step has to flatten modes into multiple files or into an `$extensions` block, and there is no canonical answer.

### 1.5 The `$type` allowlist

The required types in the current editor's draft:

- `color`
- `dimension`
- `fontFamily`
- `fontWeight`
- `duration`
- `cubicBezier`
- `number`

The composite/recent additions:

- `strokeStyle`
- `border`
- `transition`
- `shadow`
- `gradient`
- `typography`

Plus more recent or contested additions:

- `fontStyle` — drafted, not universally implemented.
- `lineHeight` and `letterSpacing` as standalone primitives — used in practice but not always distinct from `dimension`/`number` in tool implementations.
- `opacity` — sometimes a `number`, sometimes its own type depending on the tool.
- `zIndex` — proposed; not in the stable surface.

What tools default differently: Tokens Studio is permissive about which types it accepts and writes. Style Dictionary historically accepted any string as `$type` and only special-cased the ones it knew about for transforms; recent versions are stricter. Figma Variables has its own enum (COLOR, FLOAT, STRING, BOOLEAN) which does not map 1:1 to DTCG — the BOOLEAN type has no DTCG equivalent, and FLOAT collapses what DTCG separates into `number`, `dimension`, `duration`. The export-from-Figma step is the most lossy in the pipeline, and the loss is structural, not configuration.

### 1.6 What the spec leaves out — and why that's load-bearing

The deliberate omissions from DTCG are the design surface of the practitioner's job:

- **Modes / theming.** Covered above. The spec stays out; tools fill in.
- **Conditional values.** Beyond modes, the field wants conditions on breakpoint, density, OS theme, user preferences. None of this is in DTCG and there is no draft to add it.
- **Math expressions.** Covered in section 2 — `$value` is a literal, not an expression. Tools that allow expressions do so via `$extensions` or a parallel resolver.
- **Validation rules.** Beyond shape, the spec has nothing to say about constraint validation. "This colour must have a contrast ratio of at least 4.5:1 against this other colour" is not expressible. Tooling layered above DTCG handles this — and our 14-accessibility position on pair tokens is exactly this kind of constraint, encoded in `$extensions` because DTCG doesn't have a slot for it.
- **Deprecation and lifecycle.** Discussed above. `$deprecated` is community-proposed, not stable. Practitioners encode in `$extensions` and live with the lack of standardisation.

The right framing for the senior practitioner: **DTCG is the interchange format, not the architecture format**. Treating it as the architecture format is a category error — it gets you procurement-grade portability but it does not get you the constraints, conditions, and lifecycle metadata that a real system needs. Those live in extensions, in your build pipeline, and in conventions you enforce in CI.

---

## 2. Relational and computed tokens

### 2.1 The frontier

"Computed token" is overloaded. Three distinct things hide under the term:

1. **Aliases**. `spacing.md = {spacing.base}`. Already in DTCG. Not computed in any meaningful sense — it's substitution.
2. **Mathematical relationships**. `spacing.md = {spacing.base} * 1.5`. Not in DTCG. Implemented by tools as an extension.
3. **Composed values**. `padding-block = {spacing.md} + {spacing.sm}`. Not in DTCG. Possibly expressible at runtime via CSS `calc()` rather than at build time.

The frontier is in (2) and (3). The question is whether expressions belong at the token authoring layer, the build layer, or the runtime layer — and the answer is genuinely context-dependent.

### 2.2 What tools support today (verification paths below)

**Style Dictionary** (verification path: Style Dictionary docs, transforms reference, hooks/parsers documentation, version 4.x release notes):

- Does not natively parse expressions in `$value`.
- Provides a `transitive` transform layer and `parsers` hooks that let you intercept token values before resolution. Teams use this to plug in `mathjs` or a custom evaluator.
- Community packages (`sd-math`, custom transforms) do this commonly enough that it's almost a built-in expectation.
- The `transitive` flag is the bit that makes computed transforms compose — without it, transforms ran only on raw values and not on alias-resolved values, which broke the math-on-alias case.

**Tokens Studio** (verification path: Tokens Studio docs on math operations; the `studio.tokens.modify` extension block):

- Supports inline math in token values. `* 1.5`, `+ 4`, `roles(...)` syntax.
- Stores the operation in `$extensions.studio.tokens.modify` so the operation survives round-trip if the consumer respects the extension.
- The DTCG export flattens to a resolved literal `$value` by default, which loses the relationship.

**Specify and similar token platforms**: typically resolve at the platform layer, not the token layer — you author primitives, the platform computes derived values via transforms, and the output is literal-valued DTCG.

**Figma Variables**: as of mid-2026, supports basic arithmetic on numeric variables (verification path: Figma release notes on Variable expressions, rolled out incrementally through 2024–2025) but has not exposed the full algebraic capability of Tokens Studio. Most practitioner use of variable math in Figma is still simple aliasing plus one-level scaling.

**The DTCG spec position**: the editor's draft has no `$expression` field and no syntax for inline math. The community has discussed adding one; there is no active proposal as of mid-2026 that has consensus. Verification path: DTCG GitHub issue tracker, the math-expressions and computed-values threads.

### 2.3 The T-shirt / numeric / mathematical scale debate

Three encodings of scale at the primitive layer:

- **T-shirt**: `xs / sm / md / lg / xl / 2xl`. Human-meaningful sizes. Strong at the semantic layer ("padding-md"), weaker at the primitive layer ("space-md doesn't tell me what's bigger than what without consulting a key").
- **Numeric**: `100 / 200 / 300 / 400 / 500`. Material's and Tailwind's approach. Ordered, expandable (insert `150` between `100` and `200` without renaming).
- **Mathematical**: a base value and a ratio (`base * 1.125^n`). Modular scale. Compact and lossless — the scale is regenerable from two numbers.

The convergent answer the field has been moving toward:

- **Primitive layer should be numeric or mathematical.** It exists to be enumerated and looked up; ordering and extensibility matter more than human-readability.
- **Semantic layer should be T-shirt.** It exists to be consumed by component authors and designers; meaning matters more than precise size.
- **The mathematical relationship lives between them.** Primitives are the generated set; the semantic layer aliases into specific primitives by name.

The mathematical-scale trap: tokens generated from a ratio are *brittle to design intent*. The ratio gives you `16, 18, 20.25, 22.78...`. The designer wants `16, 20, 24`. The system that generates from the ratio always loses to the system that generates the ratio's nearest-clean-number, then either codifies the rounded values as primitives or accepts the irrational outputs.

The practitioner's call: use a modular ratio as a *generator* and the *design discussion*, not as a runtime computation. The output of the generator is a literal table of values that ships in the token file. This way the values are predictable (rule 1 of token consumption: a consumer should be able to read the value without resolving an expression), and the rationale is documentable in a `$description` or extension.

### 2.4 Composable units and density multipliers

The seductive case for computed tokens is density. `spacing.comfortable.md = {spacing.base.md} * 1` and `spacing.compact.md = {spacing.base.md} * 0.75`. Conceptually elegant; in practice, a trap.

The trap has three parts:

1. **The multiplier is a lie at small values.** `4 * 0.75 = 3`. `2 * 0.75 = 1.5`, which rounds to 2 — meaning the compact mode and comfortable mode produce the same value at the small end. The relationship visible in the token file ("compact is 75% of comfortable") is not what the consumer sees ("compact and comfortable are the same below 4px"). The intent and the runtime diverge silently.
2. **Designers don't want a linear scaling.** Real density tokens are *non-linear* — small values change less, large values change more, and certain values (target sizes, touch targets) are pinned to accessibility minimums and don't scale at all.
3. **The multiplier hides the override.** If `spacing.compact.lg = base * 0.75` resolves to `18` but the design system needs `20` for a specific reason, the override fights the formula. Now the consumer has to know whether the value is computed or specified.

The convergent answer: **author density as discrete value sets, not as multipliers.** Compute the values once, during the design discussion, with a multiplier as the *generator*. Then commit the values to the token file as literals. The design tool reads literals, the consumer reads literals, and the relationship is documented in `$description` or `$extensions.org.density.factor`. This is the same pattern as the modular type scale.

The multiplier-as-runtime-thing makes sense in one and only one place: **density mode is exposed as a runtime CSS variable, and individual values are not the design system's concern**. Material You and some recent Compose work treat `LocalDensity` as a runtime multiplier; the design system ships base values and the platform scales. If your consumers are like that, the multiplier is fine. If your consumers are CSS, native iOS, native Android, and a CMS, the multiplier is a build-time concern and should be resolved before the file ships.

### 2.5 The intent-vs-predictability trade-off

The fundamental trade-off of computed tokens: an expression captures intent better than a literal, but a literal is more predictable.

`spacing.layout.section = {spacing.base} * 8` tells the reader *why* the value is what it is. The reader has to resolve to know *what* the value is. If `spacing.base` changes from 4 to 5 next quarter, every dependent value moves, which is either a feature (the system rescales coherently) or a bug (every consuming component now has a one-pixel shift in production).

The field has not fully converged but the practitioner consensus, observable in the public token sets of GitHub Primer, Adobe Spectrum, Atlassian, and Shopify Polaris (verification path: each system's published token sources), is:

- **Source of truth in the design tool authors the value with the expression visible.** Tokens Studio's `studio.tokens.modify` extension is exactly this.
- **DTCG export flattens to literals.** Consumers see only the resolved value. The relationship is metadata.
- **Build pipeline regenerates from authoring source when the relationship changes.** The expression is a design-tool artefact, not a runtime artefact.

This is the same architecture as compile-time vs. runtime more generally: keep computation at authoring time, ship literals to runtime, accept that the literal output is the contract and the expression is the rationale.

### 2.6 Style Dictionary's extension points for computed values

Where teams actually plug in math in 2026 (verification path: Style Dictionary docs, hooks reference, version 4.x examples):

- **Custom `parsers`** intercept token values before resolution. A parser can read `"= {spacing.base} * 1.5"` and rewrite the value to the resolved literal. This is where `sd-math` and similar community plugins live.
- **Custom `transforms`** with `transitive: true` can run math on alias-resolved values. The `transitive` flag is essential — without it, the transform sees the alias string, not the resolved value, and can't compute.
- **Custom `formats`** can emit computed CSS — for instance, emit `var(--spacing-base) * 1.5` directly into the CSS, letting the browser do the math at runtime via `calc()`.

The third option is increasingly attractive because it pushes computation to where the value is consumed. The cost is that the token file no longer round-trips to non-CSS targets without a recompilation step.

### 2.7 The platform is absorbing what tokens used to encode

CSS native features have moved enough that some of what tokens used to compute, CSS now computes at runtime:

- **`calc()`** is universally supported. `--spacing-md: calc(var(--spacing-base) * 1.5)` is a perfectly valid token output and lets the browser do the math.
- **Custom properties** are dynamic in a way SASS variables weren't. Cascading a `--density-scale: 0.75` on a container scales every dependent custom property.
- **`clamp(min, preferred, max)`** lets a single token express a responsive value without a media query. `font-size: clamp(1rem, 2.5vw, 1.5rem)`. This compresses what used to need breakpoint-mode tokens into a single value.
- **`color-mix()`** lets a token derive a tint or shade from a base colour at runtime, which used to require generating a full palette at build time.
- **Container queries and `@container` style queries** mean some "mode" decisions can move from the token layer to the layout layer.

The architectural implication: **the token file is shrinking, not growing**. The set of things that genuinely need to be encoded at the token layer is narrower in 2026 than it was in 2022, because more is expressible in CSS at runtime. For web-first systems, this is a quiet but significant shift — the token file's job is increasingly to ship *primitives* and let CSS compose them, rather than to ship every derived value.

This story breaks for non-web platforms. iOS, Android, Compose, Flutter don't have `calc()` or `clamp()` in the same form. The token file has to ship literal values to those platforms. The pipeline has to do for native what CSS does for web, which is one of the reasons Style Dictionary's transforms-per-platform architecture has outlasted its critics: the work hasn't gone away, it's just moved.

The practitioner decision framework for "where does the computation live":

| Computation type | Best location | Why |
| --- | --- | --- |
| Scale generation (modular ratio) | Authoring time, baked to literals | Predictable, portable, documentable |
| Density variants | Authoring time, discrete value sets | Avoids small-value rounding traps |
| Light/dark colour pairs | Authoring time, separate token files | Spec-aligned (separate sources merge per mode) |
| Responsive sizing | CSS runtime via `clamp()` | Native platform feature, no token explosion |
| Theme tinting | CSS runtime via `color-mix()` where supported | Reduces palette generation, fails gracefully |
| Component-state derivation | CSS runtime via cascading custom props | Keeps system small, lets components own state logic |

---

## 3. Density and the responsive-density story

### 3.1 Density as a theming dimension

Curtis names density as one of the seven theming dimensions; it is also the dimension the field has converged on least. The reasons are structural:

- Density is not a binary or a small enum the way light/dark is. It's a continuum that the design tool flattens to a few named steps.
- Density interacts with *everything* dimensional in the system — spacing, line-height, target size, component height, icon size — and not always in the same direction (target size has accessibility floors, font size has readability floors, spacing has visual-density preference).
- Density is not just a designer preference. It's a context — touch vs. mouse, casual vs. professional, mobile vs. desktop, data-dense vs. marketing-prose.

The result is that "ship density tokens" means very different things in different systems. Atlassian's compact/default in Jira is a UI-density toggle for the professional power user. Material's density tooling on Compose is a runtime scaling pivot for adaptive layouts. Salesforce's Lightning has density as part of the user-preference layer. Each is internally coherent; none translate directly.

### 3.2 Density multipliers vs. density-specific token sets

Two encodings:

**Multiplier**. One set of base tokens; a density factor multiplies. The token system ships one value per token plus a multiplier.

**Discrete sets**. Multiple value-sets per token, one per density step. The token system ships one value per token per density.

The trade-offs:

| | Multiplier | Discrete sets |
|---|---|---|
| File size | Small | Larger (N × density) |
| Author effort | Low | Higher per density |
| Override granularity | Coarse — overrides break the formula | Fine — every value is independently editable |
| Small-value rounding | Silent failure at 1–4px | None |
| Accessibility floor pinning | Hard — multiplier overrides floor | Easy — value is just specified |
| Runtime scaling | Trivial (one CSS var changes everything) | Requires mode switching |
| Round-trip with design tool | Lossy (the multiplier is a build construct) | Lossless |

The convergent answer that has emerged across practitioner writing (verification path: Curtis's EightShapes "Density" writing; Atlassian's design system docs; Material's density guidance) is **discrete sets at the token layer, with the multiplier as an authoring-time generator**. The literal values ship; the relationship is metadata.

The exception: web-only systems that explicitly want runtime density (a "compact mode" toggle that doesn't require a stylesheet reload). For those, a runtime multiplier on a small set of CSS variables is the right architecture, and the token system ships base values plus a documented multiplier — but the multiplier applies to a *deliberately small* surface (a handful of spacing primitives), not the entire system. This bounds the silent-failure surface.

### 3.3 Density's relationship to other token families

Density does not scale all dimensional tokens uniformly. The fault lines:

**Spacing.** Scales most cleanly with density. Compact = tighter padding, gaps, gutters. The non-linearity is mild — large spacings scale more than small ones — but linear-ish in the middle.

**Type scale.** Scales much less than spacing. Compact density does *not* mean smaller body text — accessibility minimums (16px body, 1.5 line-height) pin the small end. What scales with density at the type level is usually *line-height* and sometimes *display-size* type, not body sizes.

**Target size.** Does not scale below an accessibility floor. WCAG 2.5.5 / 2.5.8 sets a 24×24 CSS pixel minimum (with exceptions); the spirit of the practice is 44×44 for touch. Compact mode cannot violate this regardless of the multiplier. **Target-size tokens should be either constant across density or floor-clamped.**

**Component sizing.** Scales with spacing more than with type. A compact button has tighter padding around the same-size label. A compact input has a shorter row but the same input text size. This is the principle that makes density coherent: it scales the *frame*, not the *content*.

The implication for the token architecture: density should not be a single multiplier across all dimensional tokens. It is a set of related, but separately-tuned, scaling decisions per token family. Encoding it as one multiplier produces visually broken output at the small end and at accessibility floors. Encoding it as separate per-family decisions (spacing scales 0.75×, line-height scales 0.9×, target size doesn't scale) produces the desired output but is more authoring work.

### 3.4 Compact / Comfortable / Spacious — is the canonical three-tier still right?

Three named steps were the default convention for a decade. The field is moving past it in two directions:

**Down**: many systems now ship two steps — Default and Compact — and treat Spacious as a marketing-page concern that lives outside the component system. The reasoning: data-dense UI needs Compact, the rest of the product needs Default, and Spacious adds a third surface that few components were ever tuned for. (Verification path: surveying production token files of Atlassian, Linear, Notion, GitHub Primer — most carry two density steps.)

**Up and continuous**: some systems are exposing density as a numeric scale (Compose's `Density` is the canonical version) and rendering at any density factor in the supported range. This is less common at the token layer and more common at the platform-rendering layer.

The right call for an enterprise engagement: **default to two steps for the design-system surface, treat additional density as a downstream rendering concern**. Three steps is over-investment for most systems. The cost of supporting three steps is not just the token tripling — it's the QA tripling, the documentation tripling, and the consuming team's choice fatigue tripling.

### 3.5 Density across touch / mouse / pen — the responsive question

Density is correlated with input modality but not equivalent to it:

- Touch wants larger target sizes, more spacing, fewer items per screen.
- Mouse wants tighter spacing, more density, more items per screen.
- Pen sits between, closer to touch on target size and closer to mouse on density tolerance.

The naive architecture says "ship a `density.touch`, `density.mouse`, `density.pen` set of tokens". This is wrong, for two reasons:

1. The same user moves between modalities on the same device. A laptop with a touchscreen needs to behave well under both. Locking density to detected modality breaks the dual-input case.
2. Density and modality are not 1:1. A touch-only data table for a warehouse operator still needs density; a mouse-driven marketing dashboard still wants generous space. Modality is a *default* signal, not a determinant.

The right architecture: **density is a user-controllable or context-controllable axis; modality is the signal that picks the default**. The token system ships density variants. The application picks the default density based on modality (and screen size, and user preference, and feature context). The token system does not encode the modality decision — that's an application concern.

Where this surfaces in the token file:

- Touch-target-size tokens are *not* part of density. They are a separate token family pinned by accessibility, with values that don't scale.
- Spacing-density tokens *are* part of density and are the primary lever.
- Type-size tokens are *mostly not* part of density (they're part of the type scale and respond to user font preferences).

### 3.6 Where density fits in the mode-multiplication problem

The mode-multiplication problem (covered in `12-figma-practice`): every mode axis multiplies the cardinality of the token set. Brand × theme × density × locale × platform produces an exploding surface that becomes unmaintainable.

Density's place in this multiplication is a decision, not a given. Three options:

1. **Density as a mode dimension.** Compact tokens and Comfortable tokens live in separate value-sets on the same token name, switched by mode. This is the Figma Variables native shape. Multiplies the mode surface.
2. **Density as an axis of the spacing tokens themselves.** No mode switch; the token name carries the density (`spacing.compact.md`, `spacing.comfortable.md`). Doesn't multiply mode surface but does grow the token set.
3. **Density as a runtime concern.** One set of tokens with a runtime CSS multiplier. No design-time mode, no token-set growth; cost is runtime fragility.

The decision framework:

- If density needs to be designable per-screen in Figma, it has to be a mode dimension (1). Designers can't toggle a CSS runtime variable in Figma; they need a mode.
- If density is product-wide and consistent (compact mode in a power-user product, comfortable everywhere else), encoding it in the token names (2) is fine and avoids the mode multiplication.
- If density is a user preference at runtime and the system is web-only, the runtime multiplier (3) is the cleanest.

For most enterprise engagements the answer is (1) or a hybrid of (1) and (2): density is a mode dimension in Figma to support per-screen design exploration, but the *output* ships as separate token files keyed by density and consumed via the application's density-context provider. The Figma authoring shape and the runtime consumption shape diverge — which is exactly the pattern of section 1.4's mode resolution discussion.

Density's interaction with the other six theming dimensions deserves naming: density tends to be **the cheapest dimension to vary** (it's almost entirely numeric, no colour decisions involved) and **the most cross-cutting** (every spacing, sizing, line-height token has a density opinion). This is the opposite shape of brand, which is expensive to vary (colour decisions everywhere) and less cross-cutting (some token families are brand-agnostic). The two should not be modelled the same way.

---

## References

Primary spec, tools, and practitioner writing. Where verification was needed for spec/tool state, the verification path is named in the body of the document.

- W3C Design Tokens Community Group — Format Module Editor's Draft. <https://tr.designtokens.org/format/> and <https://github.com/design-tokens/community-group>.
- W3C Design Tokens Community Group — issue tracker for in-flight discussions: <https://github.com/design-tokens/community-group/issues>. Particularly: modes/theming, deprecation metadata, math expressions threads.
- Style Dictionary v4 documentation — transforms, hooks, parsers, formats: <https://styledictionary.com>.
- Tokens Studio documentation — math operations and the `studio.tokens.modify` extension: <https://docs.tokens.studio>.
- Nathan Curtis (EightShapes) — token taxonomy and density writing. Specifically: "Naming Tokens in Design Systems" (2020 and subsequent updates), the density-tier articles.
- Brad Frost — atomic-design-era token writing, the practical-overlay material on multi-brand systems.
- Robin Rendle — `calc()`-era CSS writing on custom properties and the platform-absorbing-tokens argument.
- Figma — Variables release notes and the Variables / DTCG export feature documentation. <https://help.figma.com>.
- Public token sets used as cross-checks for convention claims: GitHub Primer (<https://primer.style>), Adobe Spectrum (<https://spectrum.adobe.com>), Atlassian Design System (<https://atlassian.design>), Shopify Polaris (<https://polaris.shopify.com>), Material Design 3 (<https://m3.material.io>).
- WCAG 2.2 — target size criteria (2.5.5 enhanced, 2.5.8 minimum). <https://www.w3.org/TR/WCAG22/>.

**Verification note**: this synthesis run did not have working WebSearch or WebFetch access. Claims about live tool versions, specific draft section content, and recent (mid-2025–mid-2026) spec movement should be re-checked against the primary sources above before being promoted into the numbered files in the vault. The claims most likely to drift are: exact composite-type field lists, Figma Variables math capability, Style Dictionary v4 parser/transform API surface, and the status of `$deprecated` and math-expression proposals in the DTCG issue tracker.

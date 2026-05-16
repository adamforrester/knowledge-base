# Typography Tokenisation — Depth Research

> A practitioner-level synthesis of typography tokenisation in mid-2026: composite vs. atomic, modular scales, fluid type, variable fonts, line-height, multi-script, native platform translation, and AI-readable descriptions. Assumes the reader knows the basics; argues the architectural decisions.

---

## 1. The shape of a typography token set

Typography is the most under-tokenised foundation in design systems because it is the only one where the *unit* of intent isn't a primitive. Color tokens want a single value. Spacing tokens want a single value. A typography token wants — minimally — seven values to be meaningful at the application surface, and the question of whether to ship those seven as a bundle or as a constellation is the architectural fork that decides whether a typography token set survives contact with real product work.

### The minimum viable token set

Seven dimensions describe a usable typography token across web and native:

- **font-family** — the family stack, including fallbacks. Always required.
- **font-size** — the t-shirt position on the scale. Always required.
- **line-height** — leading, usually unit-less. Always required.
- **font-weight** — numeric (100–900) or named (`regular`, `medium`, `semibold`). Required for any system with more than one weight.
- **letter-spacing** — tracking, usually in `em` or `%`. Optional for body, mandatory for display and all-caps labels.
- **font-style** — `normal` / `italic`. Optional if italics are never used; recommended to encode explicitly when they are, because italic in a variable font may be a `slnt` axis value rather than a separate file.
- **text-transform** — `none` / `uppercase` / `lowercase` / `capitalize`. Optional, but encoding it on tokens that *intend* uppercase (e.g. `label-caps`) is the only way to stop application code from re-implementing the convention inconsistently.

Optional but worth encoding when the brand demands it:

- **font-feature-settings** / **font-variant-numeric** — tabular figures for tables, contextual alternates for display, fractions for editorial. These are typography decisions, not application decisions, and belong on the token.
- **font-variation-settings** — for variable font axes the brand uses semantically (e.g. `GRAD` or `opsz`) beyond what `font-weight` and `font-stretch` cover.
- **font-stretch** / **font-width** — distinct from `wdth` axis only in the static-font case; in variable fonts they map to the `wdth` axis.

A token set that ships only `font-size` and `line-height` (still common in 2026 audits) is not a typography token set; it is a size scale with leading attached. It cannot express the difference between a body paragraph and a UI label without further code-side decisions, which is exactly the slop the system was meant to prevent.

### DTCG composite typography tokens

The W3C Design Tokens Community Group format defines `typography` as a composite type whose `$value` is an object bundling `fontFamily`, `fontSize`, `fontWeight`, `letterSpacing`, and `lineHeight` (the spec also names optional members like `fontStyle`). The composite form looks like this:

```json
"heading-large": {
  "$type": "typography",
  "$value": {
    "fontFamily": "{font.family.display}",
    "fontSize": "{font.size.800}",
    "fontWeight": "{font.weight.semibold}",
    "lineHeight": "{font.line-height.tight}",
    "letterSpacing": "{font.letter-spacing.tight}"
  },
  "$description": "Primary marketing headline. Use once per hero. Pair with body-large."
}
```

The values inside the composite *should* be references to atomic tokens (the `{...}` aliases) rather than raw values; this is what makes the composite a true semantic layer and not a duplication of the primitive scale. Tools that resolve the composite at build time — Style Dictionary's `transformGroup: 'css'` with the `typography/css/shorthand` formatter, Terrazzo, the Tokens Studio Figma plugin — produce per-platform output that respects the references.

Where the composite breaks down:

- **Partial overrides.** A composite is atomic from the consumer's perspective. If a designer wants `heading-large` with `font-style: italic` for a single editorial layout, the composite forces them either to introduce a new token (`heading-large-italic`) or to apply `font-style: italic` adjacent to the composite — defeating the contract. The DTCG spec doesn't define partial overrides; tool behaviour is inconsistent.
- **Platform translation.** SwiftUI's `Font` and Compose's `TextStyle` are also composite, but they encode line-height and letter-spacing in different units (points vs. sp; `em` vs. fractional `sp`) and don't accept a partial set the same way. Style Dictionary transforms have to either emit a single composite output or destructure to atomic fields — which means the composite is a *source* convenience, not an end-to-end abstraction.
- **Tooling churn.** As of mid-2026, Tokens Studio supports DTCG composites; Figma's native Variables do not (Variables remain primitive-typed: float, color, string, boolean). Composite typography in Figma is approximated via Text Styles that reference variable-backed properties — see section 7 and the 12-figma-practice file for the Figma round-trip detail.

The right reading: DTCG composite typography is a *semantic surface* over an atomic substrate. Ship both. The composite is what designers and consumers reach for; the atomic scale is what the composite resolves to.

### Atomic vs. composite — when each is appropriate

The dichotomy is false in practice. Mature systems ship a three-tier stack:

1. **Primitive (atomic) typography tokens** — `font.size.500`, `font.line-height.normal`, `font.weight.500`. Pure scale. Numeric or t-shirt names. These are not used directly in component code.
2. **Semantic composite tokens** — `heading-large`, `body-medium`, `label-caps`. Compose the primitives and name an intent. Used by application code and Figma Text Styles.
3. **Component-tier typography references** — `button.label.typography`, `card.heading.typography`. Reference a semantic composite. Used by component implementations.

The composite-vs-atomic argument is really an argument about *which tier the application is allowed to consume*. The answer is: only the semantic and component tiers. Direct primitive consumption is a smell — it means the system hasn't told the consumer what the value is *for*, only what it *is*.

### Brand fonts vs. system fonts

The fallback stack is encoded in `fontFamily` as an ordered list — DTCG accepts a string or an array — and the build pipeline serialises to the platform's stack syntax. The brand decision (custom variable font, custom static font set, system stack only, system stack with brand-tuned weights) is encoded in the *primitive* family tokens, not the composite. A system that ships one family token per role (`font.family.sans`, `font.family.serif`, `font.family.mono`, `font.family.display`) is composing brand fonts on top of system fallbacks for free.

The variable vs. static distinction is exposed two ways:

- A boolean on the family primitive (`"$extensions": { "variable": true, "axes": ["wght", "opsz"] }`), used by tooling to decide whether to emit `font-variation-settings` or `font-weight`.
- A separate primitive scale for axis values (`font.axis.wght.500`) when the variable font is consumed beyond the standard `font-weight` axis. See section 4.

### Many composites vs. few atomic

The trade-off is governance load. A system with 22 semantic typography tokens (`heading-1` through `heading-6`, `body-large/medium/small`, `caption`, `overline`, `label-large/medium/small`, `button-large/medium/small`, `display-1/2/3`, `code`) has codified a complete hierarchy and given product teams nowhere to drift. It also has 22 tokens to maintain through every brand refresh and a long tail of "which body do I use here" decisions that the system can answer but the docs must explain.

A system with six atomic primitives (`font.size.100–600`) plus a handful of weights, line-heights, and letter-spacings — and no semantic composites — costs less to maintain but pushes typography decisions into product code. The MUI / Tailwind philosophy. In an agency context where the system is also a brand artefact, this is the wrong default: brand expression *is* the hierarchy.

**Heuristic.** If the product surface is one website, ship many composites (≥ 15) and few atomics consumed directly. If the product surface is a multi-product platform with strong divisional brand variance, ship fewer composites (8–12) and more atomic primitives, and let division-tier theme overrides re-bind the composites.

---

## 2. Modular scales — the math, the trade-offs, the choice

The canonical musical / typographic ratios are well-known: 1.067 (minor second), 1.125 (major second), 1.200 (minor third), 1.250 (major third), 1.333 (perfect fourth), 1.414 (augmented fourth, √2), 1.500 (perfect fifth), 1.618 (golden), 1.667 (major sixth), 1.778 (minor seventh), 2.000 (octave).

### Which ratio for which context

In practice the field has converged on a much narrower band:

- **1.125 (major second)** — utility-dominant systems. The whole scale fits in a 1.5× range across ten steps. Adjacent sizes are visibly distinct but not dramatic. Default for SaaS, internal tools, admin interfaces, anything where 80% of the type is body and labels.
- **1.200 (minor third)** — the most common general-purpose ratio. Enough drama for a marketing site, enough restraint for product UI. The 8pt-grid-friendly default.
- **1.250 (major third)** — editorial-leaning systems with strong heading hierarchy. The Material 3 type scale (display / headline / title / body / label) sits in this neighbourhood.
- **1.333 (perfect fourth)** — strong hierarchy systems where headings need to assert against image-heavy layouts. Common for publishing and editorial brands.
- **1.500 / 1.618 / 1.778** — expressive editorial brands, agency portfolio sites, anything where typography is doing brand work above functional work. These ratios produce gaps so large that they only function with display-tier steps the body scale doesn't share — which is the "1.250 at small sizes, 1.500 at display" pattern.
- **2.000 (octave)** — never for a full scale. Useful for the gap between the largest body size and the smallest display size when those are deliberately separated.

The ratios below 1.067 are too tight to be perceived as a scale; the ratios above 2.000 are too wide to be perceived as a continuum.

### When to break the scale

A strict ratio across the full scale is mathematically pure and visually wrong. Three breaks are standard:

- **Body floor.** Body sizes between roughly 14px and 18px should be tuned by eye to the font's rendering at that size, not generated by ratio. A 1.200 scale stepped down three times from 16px gives 9.26px — unusable. Below the body anchor, switch to manual values or a tighter sub-scale (1.067 or 1.125).
- **Display ceiling.** Above the largest body size, switch to a wider ratio. The most common pattern is 1.250 (or 1.200) for the body scale and 1.500 (or 1.333) for display sizes. This is sometimes encoded as two scales — `font.size.body.*` and `font.size.display.*` — that meet at a shared anchor.
- **Round to grid.** Generated sizes (15.625px, 26.04px) should round to integer pixels at the rendering resolution, and to multiples of 2 or 4 where the typographic grid demands it. The ratio is a generator, not a tyrant.

### Modular vs. T-shirt vs. numeric scales

These name three different things and shouldn't be conflated.

- **The ratio (1.200, 1.250, …)** is the mathematical generator. It produces raw values.
- **The naming scheme (T-shirt, numeric, semantic)** is the addressing layer over those values. T-shirt (`xs/sm/md/lg/xl/2xl/…`) is fine for primitives that consumers won't see; numeric (`100/200/…/900`) scales further with less argument over "what comes after xl"; semantic (`body-medium`, `heading-large`) lives at the composite tier and never on primitives.
- **The tier** decides which names go where. Primitives — numeric. Semantics — descriptive. Component-tier — namespaced by component.

The Tailwind v4 / Material 3 / Adobe Spectrum systems all converge on numeric primitives with semantic composites on top.

### Ratio and brand personality

Ratio is brand expression. The tightness of the scale signals what the brand thinks of its own typography:

- **1.125–1.200** says "we trust the content to do the work; type is functional."
- **1.250–1.333** says "we have a hierarchy and we want you to see it."
- **1.500+** says "type is part of the visual identity; we will use scale as expression."

When a brand workshop produces a moodboard heavy on editorial layouts, magazine spreads, expressive cover typography, the system probably needs a split-scale (1.200 body / 1.500 display). When it produces SaaS dashboards and component-library screenshots, 1.125 or 1.200 single-scale is the right answer. Treat ratio choice as a brand decision and document the reasoning in the system's principles, not just the tokens.

### Tools

- **Typescale.com / type-scale.com** — single-ratio preview, ships CSS.
- **Modularscale.com** — multi-ratio composition, the older but still useful tool.
- **Utopia.fyi** — fluid-type scale generator with viewport-range math built in; the de-facto practitioner tool in 2025–2026 for marketing-tier responsive systems. Outputs CSS custom properties and clamp() expressions, and (as of the 2024 redesign) exposes a JSON export that maps cleanly to a primitive scale.
- **Type Scale Clamp Generator** — narrower tool focused on emitting clamp() expressions for a min/max ratio pair.
- **Figma plugins (Typescales, Set Type Styles)** — generate Text Styles from a ratio; useful for the initial scaffold but always replaced by hand-tuning before launch.

---

## 3. Fluid type, `clamp()`, and container queries

Fluid typography in 2026 is no longer a maturity flex; it's the default for marketing-tier surfaces and a deliberate non-default for product-tier surfaces. The distinction matters and the system needs to encode both.

### The math

`clamp(min, preferred, max)` returns the `preferred` value clamped between `min` and `max`. For viewport-scaled type, `preferred` is a linear expression in `vw` (or, since the container-query era, `cqi` / `cqw`). The Utopia formulation:

```css
font-size: clamp(1rem, 0.875rem + 0.625vw, 1.5rem);
```

The slope (`0.625vw`) is derived from `(maxSize - minSize) / (maxViewport - minViewport) × 100`, and the intercept (`0.875rem`) is whatever puts the line through the desired min anchor. The full Utopia method extends this to a two-anchor scale: a min ratio (e.g. 1.200) at a min viewport (e.g. 320px), and a max ratio (e.g. 1.333) at a max viewport (e.g. 1240px), generating a clamp expression per step.

Two non-negotiables:

- **The `min` must be readable.** A `min` below ~14px on a body token is an accessibility regression. WCAG 2.2 doesn't set a hard minimum but UAs and user overrides assume body text doesn't drop below it. (Verify against the latest WCAG draft; the practitioner consensus has not changed.)
- **The slope must use `rem`-based intercepts, not raw `px`.** A clamp expression that's `clamp(16px, 1vw + 8px, 24px)` ignores the user's browser font-size setting; one that's `clamp(1rem, 0.5vw + 0.5rem, 1.5rem)` respects it. WCAG 1.4.4 (Resize text up to 200%) requires the latter behaviour to be functional.

### Container queries and `cqi` / `cqw`

Container queries reached Baseline in late 2023 across Chromium, Safari (16.4), and Firefox (110), and have been broadly stable since. (Verification path: caniuse.com/css-container-queries, MDN Baseline badge on `@container`.) The container-relative inline-size unit `cqi` is what makes fluid type respond to *layout context* rather than viewport:

```css
.card h2 {
  font-size: clamp(1.25rem, 1rem + 2cqi, 2rem);
}
```

This is the unlock. A card that lives in a sidebar at 320px wide and the same card in a hero at 960px wide can have the same component code and different rendered typography, without media queries, without prop drilling, without a `size` variant. The tokenisation question: do you ship two clamp expressions per semantic token (one viewport-relative, one container-relative), or do you ship the math and let the consumer pick the unit?

The practitioner consensus in 2026 is that **viewport-relative is the default for marketing-tier, container-relative is the default for product-tier**, and the system should expose both as separate tokens (`heading-large` / `heading-large-fluid` / `heading-large-container`) rather than overloading the semantic name. The naming compromise — many systems use `-fluid` suffix for viewport-relative and `-responsive` for container-relative — is not yet settled.

### When fluid type is the wrong answer

Three categories:

- **Long-form reading.** A reading column should be a fixed comfortable size (60–75 characters at a font tuned for that measure). Fluid type on a reading body undermines the deliberate measure decision. Use container-bounded body sizing instead — fix the column width, fix the body size, let the layout do the responsive work.
- **Locale-aware sizing.** When the same component needs to be 10% larger in Arabic than in Latin (see section 6), fluid type fights with locale tokens. The locale dimension wins; encode the size step, not the fluid expression, and let the locale theme rebind the step's value.
- **Accessibility-constrained contexts.** When the user has set a 200% browser zoom or a custom user stylesheet, fluid type that uses viewport units doesn't always compound the zoom intuitively. The `rem`-based intercepts mitigate this but don't eliminate it for users on text-only-zoom in Firefox. For a system that prioritises accessibility-first product UI, fixed-step `rem` tokens are safer than fluid clamp expressions.

### Encoding fluid type in tokens

Three options, in increasing order of architectural cost and decreasing order of consumer ergonomics:

1. **Single `clamp()` string token.** `"$value": "clamp(1rem, 0.875rem + 0.625vw, 1.5rem)"`. Easy to consume, opaque to refactor, can't be re-mathed at theme time, can't be platform-translated to anything that isn't CSS.
2. **Primitive triplet** — `font.size.body-medium.min`, `…preferred`, `…max` — that the CSS layer composes into `clamp()` via a build transform. Style Dictionary supports this with a custom format. Platform-translatable: iOS and Android can choose between min and max based on size class, or interpolate.
3. **Function in code** — the system ships a `fluid(min, max, minVW, maxVW)` mixin or JS function, and tokens carry only min/max/range references. Most flexible, most opinionated, highest coupling between token consumer and system implementation.

In 2026, option 2 is the cleanest for cross-platform systems; option 1 is acceptable for web-only marketing systems; option 3 is for in-house systems with a single CSS framework target.

### Accessibility implications — WCAG 1.4.4

WCAG 1.4.4 requires text to scale to 200% without loss of content or function. Fluid type *helps* this by keeping `rem`-based intercepts that respond to user font-size, *hurts* it when:

- The `max` cap is too low (text stops growing at, say, 1.5rem when the user wants 2× their preferred body).
- The `vw` slope is steep enough that text grows visibly with viewport width but the cap clamps before user zoom can multiply it further.
- The fluid expression mixes `px` and `vw` in ways that break the user's font-size adjustment.

Practitioner rule: every fluid type token should pass a manual "200% browser zoom" test before shipping. Automation via Playwright + a visual diff is feasible and not commonly done.

---

## 4. Variable fonts as a tokenisation problem

Variable fonts cracked the typography token model. Pre-variable, weight was a discrete set: 100, 300, 400, 500, 700, 900, and the available weights were whichever the type designer had drawn. Post-variable, `font-weight: 437` is meaningful — it's the interpolated position on the `wght` axis 437/1000ths of the way between the axis minimum and maximum (or between the closest named instances, depending on font). Token systems built around discrete weights can't express this; tokens systems that expose continuous axes lose the semantic anchoring.

### The axes worth tokenising

- **`wght` (weight)** — universal, mapped to CSS `font-weight`. The boring axis.
- **`wdth` (width)** — mapped to `font-stretch` / `font-width`. Under-used in product systems, common in editorial. Useful for fitting display type to a measure without changing size.
- **`opsz` (optical size)** — the most under-used axis in 2026 and the one that visibly improves type quality when used. See below.
- **`slnt` (slant)** — slant in degrees, distinct from italic (which is a stylistic redrawing, not a geometric slant). Some fonts ship both `slnt` and a separate italic; some ship one or the other; some ship `ital` as a binary axis (0/1) controlling italic stylistics.
- **`GRAD` (grade)** — weight-without-width adjustment. Used by Roboto Flex, Recursive, and Google's variable system fonts for fine-tuning weight against dark vs. light backgrounds without changing layout. Almost no design systems tokenise it; the ones that do (Google's own, a handful of editorial brands) get meaningful contrast / inversion gains.
- **Custom axes** — fonts can define any axis (e.g. Recursive's `MONO`, Roboto Flex's `XOPQ`, `YOPQ`). Tokenise only what you use.

### Tokenising axis values

For a variable-only system the cleanest model is:

- One primitive scale per axis: `font.axis.wght.{light, regular, medium, semibold, bold, ...}` with numeric values.
- Composite typography tokens reference axis primitives, not raw numbers.
- The CSS output emits both `font-weight` (legacy fallback) and `font-variation-settings` (forward path), with `font-variation-settings` consuming the same numeric values.

For a mixed static / variable system the model degrades: the primitive scale only resolves to legal static weights for the static-font composites, and the composites carry an axes-supported flag in `$extensions` so the build pipeline knows which output to emit.

### Optical size

`opsz` adjusts letterform proportions (x-height, contrast, spacing) for the size at which the font is being rendered. At display sizes, fonts get tighter spacing, thinner hairlines, taller x-heights compressed. At text sizes, the inverse. CSS supports automatic optical sizing via `font-optical-sizing: auto` (Baseline since ~2022), which slaves `opsz` to `font-size`. This is the right default — but tokens should also be able to override it: a display token with explicit `font-variation-settings: 'opsz' 144` will use the display optical regardless of the rendered size, useful for cases where the body of a hero is actually rendered at body-size but the brand wants display-size letterforms.

Practitioner heuristic: if the chosen variable font has an `opsz` axis, the system's default should be `font-optical-sizing: auto` everywhere; the system should expose an explicit-opsz override only on display and editorial tokens.

### Delivery in 2026

WOFF2 remains the universal delivery format. A single variable font file with three axes (`wght`, `opsz`, `slnt`) typically delivers in 80–180 KB after subsetting to Latin Extended, which is competitive with three to five static weight files. The story changes for CJK: a CJK variable font is 1.5–4 MB per file even subsetted, and the math of variable-vs-static delivery for those scripts is dominated by which subsets the consumer actually needs.

`font-display` strategy:

- `swap` for body text (FOUT, but readable text immediately).
- `optional` for display where layout shift is unacceptable.
- `block` only when the brand demands the custom font's first frame — rare.

Subsetting: ship a Latin-Extended subset by default, lazy-load CJK / Arabic / Devanagari subsets via `unicode-range` declarations. A single `@font-face` block per script segment, all pointing at the same variable font file with different `unicode-range` filters, is the modern delivery pattern.

### Variable fonts in Figma

As of mid-2026 Figma supports variable font axes natively at the Text Style and Type Detail level — `wght`, `wdth`, `slnt` are first-class properties in the Type panel for any variable font, and custom axes are surfaced when the font defines them. (Verification: Figma changelog / release notes; this support has matured incrementally since 2023 and was largely stable by early 2025.) Figma Variables, however, do not yet accept axis numbers as variable-bound values; Text Styles can encode a fixed axis value, but bind-to-variable for `wght` requires the workaround of a separate Text Style per weight position. This is the round-trip pain: a DTCG token with `font.axis.wght.500` resolves cleanly in code, but in Figma it lands as a discrete Text Style rather than a continuous Variable. The 12-figma-practice file covers the round-trip and the Code Connect implications.

### The continuous-vs-named trade-off

Variable fonts unlock continuous design. Tokens are by definition discrete naming. The reconciliation:

- The system ships a finite, semantically-named ladder of axis positions (`wght.100`, `wght.200`, … `wght.900`).
- Designers in Figma can deviate from the ladder for one-off display work, but the deviation is flagged by the linter as a "non-token usage."
- The published system docs include a "why these positions" explainer — usually: stops at 100/regular, 50/medium-or-emphasis, 75/strong-emphasis-or-display, with named-instance fallbacks to the font's static instances for browsers / contexts that need them.

The principle: continuous design at the *tool* layer; named tokens at the *system* layer; named ladder positions chosen with intent, not at-equal-intervals.

---

## 5. Line-height, leading, and the relationship to font-size

Line-height is the most tightly coupled typography value to font-size and the one most often mis-tokenised. The pattern is well-known: at small sizes you need proportionally more leading for readability; at large sizes you need proportionally less to keep the headline from breathing apart.

### The convergent ratios

- **Body (14–20px / 0.875–1.25rem)** — line-height 1.4–1.6 (consensus: 1.5 for paragraph text, 1.4 for UI prose).
- **Small (≤ 13px)** — line-height 1.4–1.5 (push higher for legibility).
- **Display (24–48px / 1.5–3rem)** — line-height 1.2–1.3.
- **Hero / poster (> 48px)** — line-height 1.0–1.2 (often 1.05–1.1 for tight editorial display).

These are convergent across Apple HIG, Material 3, and most published agency systems. The drift point is the middle of the range: headings at 24–32px sit awkwardly between body and display ratios and the right number is usually around 1.25.

### Unit-less vs. dimensional

Unit-less line-height (`line-height: 1.5`) computes against the element's own `font-size` and is inherited as the multiplier. Dimensional line-height (`line-height: 24px` or `line-height: 1.5rem`) is inherited as a fixed value, which breaks the moment a descendant element has a different font-size.

The token implication: line-height primitives should be unit-less. Multiplier values, not pixel values. The composite typography token can resolve to a px-equivalent in the build output if the platform demands it (some Android setups, some legacy Style Dictionary configurations), but the *source* must be unit-less or the system will break on every override.

### Optical leading

For brand fonts where the typeface's intrinsic line gap (the `sTypoLineGap` / `usWinAscent` metrics in the font file) is well-tuned to the design, the better approach is to express line-height as a *multiplier of the font's natural line metric* rather than a hard ratio of font-size. CSS doesn't directly support this on the web — `line-height: normal` uses the font's metric but is not directly tokenisable as a numeric multiplier — but the emerging `text-box-trim` / `text-box-edge` properties (see below) are the spec path toward making line-gap-relative leading addressable.

In practice in 2026, optical leading is a Figma / native concern, not a web concern. SwiftUI's `lineSpacing` modifier adds to the font's natural gap; Compose's `lineHeight` overrides it but `lineHeightStyle.Trim` controls the trim against the font's metric.

### Composite vs. separate scale

Two patterns:

1. **Line-height baked into the composite.** `heading-large` is a single token whose `lineHeight` resolves to the right unit-less multiplier for that size. Consumers can't get the wrong leading for a given size because they can't address line-height independently.
2. **Separate line-height scale.** `font.line-height.{tight, normal, loose}` exists as a primitive, and the composite references it. Allows the same line-height multiplier to be reused across sizes that share a leading regime (display sizes share `tight`, body sizes share `normal`).

The mature pattern is *both*: a primitive line-height scale (tight 1.1 / snug 1.25 / normal 1.4 / relaxed 1.5 / loose 1.6) with semantic composite tokens referencing the right primitive for each size, and no direct primitive consumption from application code. This is the same three-tier structure as the font-size scale.

### `text-box-trim` / `text-box-edge` — Baseline status

As of May 2026, `text-box-trim` and `text-box-edge` are **not Baseline** — MDN lists them as Limited Availability, supported in Safari (since 16.4 for the older `leading-trim` syntax; the renamed `text-box-trim` since 18.2) and in Chromium behind a flag. Firefox has not shipped. (Verification path: MDN browser compatibility table on `text-box-trim`, caniuse.com/text-box-trim, as of 2026-05.) The capability — trimming the over- and under-line metric space to align text to its actual glyph bounds — is the web's catch-up with iOS's leading-trim (which has shipped since iOS 15) and Compose's `LineHeightStyle.Trim.Both`. When it does reach Baseline, it removes one of the most persistent CSS frustrations: a heading set to `line-height: 1.2` is rendered with visible space above the cap height and below the baseline, which forces every system to add per-component negative margins to align text to bounding-box edges. Until Baseline, the practitioner workaround is the well-known negative-margin hack derived from the font's metrics, encoded as a token or component-level mixin.

The system implication: don't bet the architecture on `text-box-trim` yet. Build the line-height scale as if it shipped (multiplier values, composite tokens referencing primitives), and emit per-token trim offsets as `$extensions` metadata that can be consumed by iOS / Compose today and by `text-box-trim` when Firefox lands it.

---

## 6. Multi-script and multi-locale typography

The single largest under-handled area in DS typography. Most published systems test their type scale in English Latin and ship it; the cracks appear when the same scale renders Arabic, Hindi, Thai, or Japanese.

### When one scale works, when it doesn't

A single token set works across Latin, Cyrillic, Greek, Vietnamese, and most Latin-extended scripts with comparable x-height ratios. It does not work across:

- **Arabic / Persian / Urdu.** Arabic letterforms are typically rendered ~10–15% larger than Latin at the same readability, because the script's optical mass is concentrated below the baseline and the perceived size is smaller per em. Arabic line-height also needs to be larger (typically 1.6–1.8 vs. Latin's 1.4–1.5) because diacritics extend significantly above and below the baseline.
- **CJK (Chinese, Japanese, Korean).** CJK glyphs fill the em box; the perceived size is larger per em than Latin. CJK typically uses smaller font-size (~90% of Latin equivalent) and tighter line-height (~1.5–1.7, but the math is different because there are no descenders to speak of). Mixed Latin-CJK runs need separate font-family declarations or carefully chosen CJK fonts with bundled Latin.
- **Devanagari / Bengali / Tamil.** Indic scripts have above-baseline and below-baseline marks that need extra leading. Typically ~15% larger line-height than Latin.
- **Thai / Lao / Khmer.** Above-baseline vowel marks and below-baseline tone marks need significant vertical space; line-height needs to be ~1.7–1.9.

### Locale-aware type scales

The DS contract decision: does the system ship locale-specific token sets, or does it expose an API the application layer overrides per locale?

Three patterns:

1. **Single set, application overrides.** The system ships one type scale (Latin-tuned). The application's locale layer overrides specific composite tokens per locale (e.g. `body-medium` gets a larger size in Arabic). High flexibility, high inconsistency risk, hard to audit.
2. **Locale-themed token sets.** The system ships the same composite-token names, but each locale theme rebinds the primitives. `body-medium` in the `ar-SA` theme resolves to a different font-family, larger size, and larger line-height than in the `en-US` theme. Aligns with modern CSS `@media (lang)` and Style Dictionary theming.
3. **Per-script primitive scales, single composite layer.** The system ships separate primitive scales (`font.size.latin.*`, `font.size.arabic.*`, `font.size.cjk.*`), and the composite tokens reference the script-appropriate primitive based on a locale variable. This is the cleanest model and the heaviest to maintain.

The 13-internationalization-and-rtl file argues for option 2 as the default; option 3 is appropriate when a single product surface ships in five or more scripts.

### Variable fonts as a multi-script tool

Variable fonts that ship multi-script in a single binary (Noto Sans Variable, the Google Sans variable family, IBM Plex Sans Variable) are the cleanest delivery story when they exist. But:

- The axis design is Latin-first. `wght` on Noto Sans Arabic doesn't always interpolate identically to `wght` on Noto Sans (the same numeric value renders perceptually different weights).
- Custom variable fonts commissioned for brand work rarely ship multi-script. The brand decision becomes: pay 5× to extend the variable font to Arabic / CJK, or use a script-matched system font (Geeza Pro, Hiragino, Noto) for non-Latin and accept the brand drift.
- Variable font tooling for non-Latin scripts (especially CJK) lags Latin tooling by years. Subsetting CJK variable fonts is non-trivial; many production setups still ship static CJK alongside variable Latin.

### Relationship to 13-internationalization-and-rtl

13- covers logical properties, RTL component mirroring, multi-script font stacks at the architectural level. This document's contribution is the *tokenisation* of the multi-script type scale — the decision of whether the size primitives are shared, per-script, or per-locale. Treat the locale-aware decision as a tier-of-the-token-architecture decision, not an i18n afterthought.

---

## 7. Native platform translation

The token pipeline emits per-platform output via Style Dictionary (or Terrazzo, or Knapsack, or in-house). Typography is the place this gets hardest because each platform has its own composite type and its own accessibility-text-scale contract.

### iOS (SwiftUI / UIKit)

Style Dictionary emits Swift extensions on `Font` (SwiftUI) or `UIFontDescriptor` (UIKit). The shape:

```swift
extension Font {
  static let headingLarge = Font.custom("BrandSans", size: 28)
    .weight(.semibold)
    .leading(.tight)
}
```

This is the naive translation and it loses the Dynamic Type story. The correct pattern is to map each composite token to the closest `Font.TextStyle` (`largeTitle`, `title`, `title2`, `headline`, `body`, `callout`, `footnote`, `caption`, etc.) and use `Font.custom(_, size:, relativeTo:)` so the custom font scales with Dynamic Type:

```swift
extension Font {
  static let headingLarge = Font.custom("BrandSans", size: 28, relativeTo: .title)
    .weight(.semibold)
}
```

The token's job is to carry the `relativeTo:` text style as metadata (`$extensions": { "ios": { "textStyle": "title" } }`), not just the px value. Without this, the iOS output is broken for Dynamic Type. See 16-mobile-accessibility-implementation for the depth on how Dynamic Type bridges work and where they fail.

### Android Compose

Compose's `Typography` in `MaterialTheme` is a fixed set of `TextStyle` slots (`displayLarge`, `displayMedium`, …, `bodyLarge`, …, `labelSmall`). The token pipeline emits a `Typography(...)` constructor:

```kotlin
val AppTypography = Typography(
  headlineLarge = TextStyle(
    fontFamily = BrandSans,
    fontSize = 28.sp,
    lineHeight = 36.sp,
    fontWeight = FontWeight.SemiBold,
    letterSpacing = (-0.5).sp
  ),
  // ...
)
```

`sp` (scale-independent pixel) respects the user's Android system font scale setting (`fontScale` in `Configuration`). `lineHeight` in `sp` is unit-dimensional — the unit-less line-height multiplier from the source token must be resolved at build time. `lineHeightStyle = LineHeightStyle(alignment = Center, trim = Both)` is the equivalent of `text-box-trim: trim-both` and has shipped in stable Compose since 1.5 (2023). Use it; the trim is what aligns Compose text to bounding-box edges the way iOS leading-trim does.

The Compose typography slot system is opinionated. A custom-named token (`heading-display-1`) has to be mapped to a slot or shipped outside the `Typography` object as a custom extension. The slot fit is usually negotiable — `displayLarge`, `displayMedium`, `displaySmall`, `headlineLarge/Medium/Small`, `titleLarge/Medium/Small`, `bodyLarge/Medium/Small`, `labelLarge/Medium/Small` covers 15 slots, which is enough for most systems.

### Flutter

`TextTheme` is similar to Compose's `Typography` and equally slot-shaped. `TextStyle` carries `fontFamily`, `fontSize`, `height` (line-height as a multiplier — the only platform where unit-less line-height ships natively), `letterSpacing`, `fontWeight`. `MaterialTextScaler` controls scaling — since Flutter 3.16 / Material 3 the `textScaler` API replaced the older `textScaleFactor` and supports both linear and non-linear scaling (matching iOS's behaviour where Dynamic Type ramps non-linearly at the extremes). The token pipeline emits a `TextTheme` with `height` as the unit-less multiplier and `fontSize` in logical pixels.

### React Native

The hardest target. RN doesn't have a typography theme primitive; community conventions use a `StyleSheet`-based theme object or a context-provided design tokens module. There is no native Dynamic Type integration — RN respects iOS's `UIAccessibility` font-scale via `allowFontScaling` on `<Text>` (defaults true), but the scaling ramp is linear and doesn't map to the same step-set as native iOS Dynamic Type. On Android, RN scales via `sp` automatically when `allowFontScaling` is true.

The implication: a token system targeting RN ships typography as a flat JS / TS object (`fonts.headingLarge = { fontFamily, fontSize, lineHeight, fontWeight, letterSpacing }`), with a separate metadata layer that the application layer can use to bridge to Dynamic Type via a native module if accessibility is a priority. The RN library `react-native-dynamic-type` and similar provide this bridge; most agency RN work skips it and accepts the accessibility cost. (See 16-mobile-accessibility-implementation for the cost.)

### Dynamic Type / text-scale story summarised

| Platform | Native accessibility text-scale | Token-system requirement |
|---|---|---|
| iOS (SwiftUI/UIKit) | Dynamic Type (non-linear, 12 size classes) | Tokens must carry `relativeTo:` text style metadata |
| Android (Views/Compose) | `fontScale` (linear multiplier 0.85–1.3 in Settings, larger via accessibility) | Use `sp` units in token output |
| Flutter | `MaterialTextScaler` (linear or non-linear, configurable) | Use `height` multiplier and logical px in `TextStyle` |
| React Native | `allowFontScaling` (linear, no class system) | Tokens flat; bridge via native module if required |
| Web | User browser font-size + zoom | Tokens use `rem`, line-height unit-less, fluid type with `rem` intercepts |

The system that handles this well treats Dynamic Type / text-scale as a *first-class architectural concern* of the token pipeline, not as a per-platform afterthought.

---

## 8. AI-readable token descriptions

Typography is the token category that benefits *most* from descriptions, because the visual differences between two typography tokens are subtle, and the intent behind a typography token is rarely deducible from the values.

### Why typography needs descriptions

Consider `body-medium` vs. `body-default`. Both might be 16px / 1.5 / regular. The difference: `body-medium` is for component-internal prose (card descriptions, modal body); `body-default` is for top-level page prose (article body, marketing paragraphs). An AI agent generating component code from a Figma frame cannot infer this from the token values — the values are identical or near-identical. Without a description, the agent picks the first match, or randomises, or invents a third token.

The same applies to: `label-caps` vs. `overline`; `heading-large` vs. `display-small`; `body-link` vs. `body-medium` with a link variant. The visual distance is small; the semantic distance is large.

### What a good typography description contains

Five fields, in order of importance:

1. **Purpose.** One sentence stating the intent. "Primary page-level marketing headline, used once per hero." Not a description of the values; a description of the use.
2. **Where to use.** Two or three concrete contexts. "Hero sections, campaign landing pages, top of post-detail pages."
3. **Where not to use.** The two or three places this token gets misapplied. "Do not use for section headings inside an article (use `heading-large`). Do not use for card titles (use `heading-medium`)."
4. **Hierarchy position.** Explicit ordering. "Outranks `heading-display-2`. Pair with `body-large` for hero subhead."
5. **Anti-patterns.** Combinations that look right but aren't. "Do not stack two `heading-display-1` tokens on the same view. Do not use with `text-transform: uppercase` (the typeface's default-case display is intentional)."

The DTCG `$description` field carries plain text; richer description content (use-cases, pairings, anti-patterns as discrete fields) lives in `$extensions` under a system-specific namespace. The 15-ai-in-ds and the AI-component-description skill cover the broader description format; for typography specifically, the five fields above are the minimum.

### Role in Figma MCP context and AI-generated code

When Figma's MCP server serves a frame to an AI agent for code generation, the agent reads the Text Style names *and* their associated DS metadata (where the Code Connect / metadata bridge has been set up). If the metadata includes typography token descriptions, the generated component code references the right semantic token. If it doesn't, the agent either:

- Picks the wrong semantic token (visually identical, semantically wrong, hierarchy implications hidden until the next brand refresh).
- Inlines the raw values (defeating the system entirely).
- Invents a token name (`heroHeadline`, `pageTitle`) that doesn't exist in the codebase.

Description quality compounds with token cardinality. A six-token system can survive without descriptions; a 22-token semantic typography set without descriptions is functionally a 22-way coin flip for any AI agent generating from a Figma frame.

### What practical depth costs

Writing five-field descriptions for 20 semantic typography tokens is a one-afternoon job at system inception and a 30-minute job at every brand refresh. Auditing the existing system's typography descriptions for the five fields is the highest-leverage AI-readiness work most agency-built systems can do — it costs less than a Code Connect setup and yields a larger improvement in AI-generated code quality, particularly for the typography hierarchy decisions that the agent cannot infer from values.

---

## References and verification paths

Primary specs:

- W3C CSS Fonts Module Level 4 — `font-variation-settings`, `font-optical-sizing`. https://www.w3.org/TR/css-fonts-4/
- W3C CSS Containment Module Level 3 — container queries. https://www.w3.org/TR/css-contain-3/
- W3C CSS Inline Layout Module Level 3 — `text-box-trim`, `text-box-edge`. https://www.w3.org/TR/css-inline-3/
- W3C Design Tokens Format Module (DTCG) — composite `typography` token type. https://tr.designtokens.org/format/
- WCAG 2.2 — 1.4.4 Resize Text, 1.4.12 Text Spacing. https://www.w3.org/TR/WCAG22/

Browser / spec state (verify dated):

- MDN `text-box-trim` — Limited availability as of 2026-05; Safari 18.2+, Chromium flagged, Firefox not shipped. https://developer.mozilla.org/en-US/docs/Web/CSS/text-box-trim
- MDN `@container` and `container-type` — Baseline Widely Available as of late-2023 across Chromium, Safari 16.4+, Firefox 110+. https://developer.mozilla.org/en-US/docs/Web/CSS/@container
- caniuse.com for live verification: caniuse.com/css-container-queries, caniuse.com/text-box-trim, caniuse.com/variable-fonts

Platform docs:

- Apple HIG — Typography. https://developer.apple.com/design/human-interface-guidelines/typography
- Apple Developer — Scaling fonts automatically (Dynamic Type custom fonts). https://developer.apple.com/documentation/uikit/uifont/scaling_fonts_automatically
- Material 3 — Typography. https://m3.material.io/styles/typography
- Compose `Typography` / `TextStyle` / `LineHeightStyle`. https://developer.android.com/jetpack/compose/text
- Flutter `TextTheme` and `textScaler`. https://api.flutter.dev/flutter/painting/TextTheme-class.html
- React Native `<Text>` and `allowFontScaling`. https://reactnative.dev/docs/text

Practitioner tools and writing:

- Utopia.fyi — fluid type scale generator. https://utopia.fyi
- Typescale.com / type-scale.com — modular scale preview.
- Modularscale.com — multi-ratio scale composition.
- Tokens Studio for Figma — DTCG typography composite support. https://tokens.studio
- Style Dictionary v4 — typography transforms. https://styledictionary.com
- Terrazzo — DTCG-native pipeline. https://terrazzo.app
- Roel Nieskens on variable font subsetting. https://pixelambacht.nl
- Adam Argyle / Una Kravets — CSS fluid type and container queries primers on web.dev.

Internal cross-references in this vault:

- 02-design-foundations — token architecture, the foundation layer this document deepens.
- 12-figma-practice — Figma Variables, Text Styles, variable font support, the Figma round-trip.
- 13-internationalization-and-rtl — multi-script type treatment at the architectural level.
- 14-accessibility — pair tokens, ARIA encapsulation, the four-layer accessibility model.
- 16-mobile-accessibility-implementation — Dynamic Type, Compose text-scale, Flutter `textScaler`, RN `allowFontScaling`.
- 15-ai-in-ds — components-as-data, MCP architecture, the role of descriptions.

---
type: practice-area
title: Token Architecture Extensions
description: Spec-and-architecture layer beneath 02. DTCG 2025.10 at practitioner depth, composite-token fidelity gap, computed/relational tokens, density as a theming dimension, web-vs-native asymmetry.
tags: [extension, tokens, dtcg, theming, density]
timestamp: 2026-05-16
---

# 22 — Token Architecture Extensions

> The DTCG specification reached its first stable version (2025.10) in October 2025. Our practice has been treating DTCG as procurement-grade for over a year — 02-design-foundations names it, our pitches commit to it. What 02 does not reach is the spec-level depth a senior architect needs once the easy decisions are made: how composite tokens actually round-trip across tools, where computed and relational tokens belong in the pipeline, and how density gets encoded without inflating the surface to unmanageable. This file is that layer. It assumes the reader already accepts the three-tier taxonomy and the DTCG-as-standard position. It picks up where 02 stops being prescriptive.

---

## What this file extends, and what it doesn't

02-design-foundations is the spine of our token POV. The three-tier taxonomy (Primitive / Semantic / Component + DTCG Composite), the seven-dimension theming ladder, surface-as-inheritance-unit, the Figma → DTCG → Style Dictionary → platforms pipeline, and the multi-theme-from-day-one stance — those positions are settled and this file does not re-derive them. 12-figma-practice covers the Figma side of the pipeline (Variables, modes, scoping, the cross-file alias risk), and this file does not re-derive that either.

What this file adds is the layer underneath those positions. **DTCG at the depth a senior architect needs when the spec has stable answers, partial answers, and deliberate omissions.** **Computed and relational tokens at the point where the field has converged on what belongs at authoring time vs. runtime, and what the web platform has absorbed.** **Density as the most under-specified theming dimension in the field, and the encoding patterns the 2025–2026 practice has stabilised on.**

Typography is excluded from this file by design — its depth justifies its own file (23-typography-tokenisation). Multi-brand portfolios and validation are excluded for the same reason (24-tokens-at-scale).

---

## The DTCG 2025.10 stable specification

The Design Tokens Community Group published the first stable version of the Design Tokens Format Module on **28 October 2025** (`designtokens.org/tr/2025.10/format/`). This is the version our materials should now name explicitly. The earlier "draft" framing in our existing 02 file is out of date and should be updated.

The stable release is significant for procurement reasons more than technical ones. **DTCG as a draft was an architectural commitment; DTCG as a stable spec is a procurement commitment.** Clients can now reference the version-of-record (`2025.10`) in contracts, RFPs, and conformance claims. Tool vendors (Style Dictionary, Tokens Studio, Figma, Penpot, Sketch, Framer, Terrazzo) have either shipped support or are in active implementation against the stable target. The interoperability promise that justified the procurement-grade pitch is now backed by a stable spec with a release date.

### What the stable spec actually defines

The stable Format Module nails down the structure of a token file but stops well short of being a full design-token architecture. **Treat DTCG as an interchange format, not an architecture format.** It defines what a token *is*; it deliberately does not define how an enterprise system should *organise* its tokens. This distinction is load-bearing for everything else in this file.

The stable, settled parts of the spec are:

- **The file shape.** JSON, media type `application/design-tokens+json`, file extension `.tokens` or `.tokens.json`.
- **The `$` prefix for built-in properties.** `$value`, `$type`, `$description`, `$extensions` — all mandatory `$`-prefixed. The earlier inconsistency (some tools accepted unprefixed) is closed.
- **The terminal-node rule.** Any object containing a `$value` property is definitively a design token. **A token cannot simultaneously serve as a group or parent to other tokens.** This rules out the ambiguity that plagued earlier token sets where a color group held both a base value and child variants.
- **The `$type` allowlist.** `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number`, `strokeStyle`, `border`, `transition`, `shadow`, `gradient`, `typography`. Tools are forbidden from guessing the type from the value; missing `$type` is a validation error in conformant parsers.
- **Alias resolution.** The `{path.to.token}` curly-brace syntax for references, with chained-alias recursion and circular-reference detection as required parser behaviours.
- **The `$extensions` preservation rule.** Tools must preserve `$extensions` keys even when they don't recognise them. This is what makes vendor-specific data (Figma scope info, Tokens Studio math expressions, custom platform flags) survive a tool-to-tool round trip.

### What the spec deliberately omits

The omissions are not accidents. The DTCG community made explicit decisions to leave certain concerns to the implementer:

- **Modes and theming.** The Format Module does not define how a token resolves to different values based on context (theme, brand, density). The work-in-progress **Resolver Module** addresses this but is not part of the stable 2025.10 release. Practitioners encode modes in `$extensions` (Tokens Studio's mode syntax, Style Dictionary's set logic, Figma's mode metadata) and accept that the encoding is not yet portable across tools.
- **Mathematical expressions.** No computed values in the spec — no `{spacing.base} * 1.5`, no modular-scale formulae. Tooling fills the gap (Tokens Studio's math, Style Dictionary's preprocessors).
- **Conditional values.** No media-query-driven token values inside the JSON. The spec assumes the runtime resolves context.
- **Validation rules for `$extensions`.** Tools must preserve them but the spec defines no schema for their contents. This means `$extensions` is a vendor-specific wild west.
- **Deprecation metadata.** No `$deprecated` flag in the stable spec. Practitioners use `$extensions.<vendor>.deprecated` and accept the per-tool inconsistency.

**The practitioner takeaway from the omission list.** The DTCG spec gives you a clean, stable interchange format and explicitly leaves you to architect the modes, math, conditionals, and deprecations on top of it. Most enterprise architecture decisions happen in the layer the spec doesn't cover. This is the right division of labour — a spec that tried to standardise theming and math in 2025 would have frozen the wrong abstractions — but it means our practice has to be honest with clients about where DTCG ends and where our own architecture begins.

### Composite tokens — the implementation-fidelity gap

Composite tokens (typography, shadow, border, transition) are the part of the stable spec where the gap between specification and tool behaviour is largest. The spec defines a typography token as a structured object with sub-properties (`fontFamily`, `fontSize`, `lineHeight`, etc.), each of which **can itself be an alias to another token.** This "property-level aliasing" is the spec's intent. It is not what most tools currently implement.

The fidelity gap shows up at three boundaries:

1. **Figma → DTCG export.** Figma's typography style export typically flattens composite sub-properties to literal values rather than preserving alias references. A composite typography token whose `fontSize` should reference `font-size/medium` exports with the literal value (e.g. `16px`) instead. Round-tripping back into the source loses the relationship.
2. **DTCG → native platform output.** Style Dictionary v4 handles the composite type but the output formats are not symmetric across platforms. CSS gets the composite as a utility class or set of custom properties; SwiftUI gets it as a `Font` extension with the line-height applied separately; Compose gets it as a `TextStyle`. Each platform's output is faithful in isolation; the conceptual unity of the composite is preserved at the source only.
3. **Tool-to-tool round trip.** A composite shadow exported from Tokens Studio, imported into Figma, then re-exported back to Tokens Studio is unlikely to preserve every sub-property alias intact.

**The practical implication.** Authoring composites is correct for designer ergonomics — a single named token captures a complete design decision. **Consuming composites is where the fidelity gap forces a compromise: flatten the composite at the build pipeline into the platform-specific atomic outputs each runtime expects, and treat the composite as an authoring-time convenience rather than a runtime contract.** This is not a defeat of the spec; it is how the spec was designed to be used. The DTCG composite is the source-of-truth representation; the build pipeline's job is to produce the per-platform output that runtime can actually consume.

### Alias resolution semantics

The `{token.path}` syntax is settled; the edge cases are where most practitioner errors happen. Three behaviours matter at the architecture layer:

- **Chained aliases.** `A` references `B` references `C`. Conformant parsers recursively resolve to the terminal value. There is no spec-defined depth limit, but production pipelines should fail loudly on cycles.
- **Circular detection.** `A → B → A` is a parser error. Style Dictionary and Tokens Studio both detect cycles and refuse to build; the spec requires this behaviour.
- **Cross-file resolution.** The spec uses an array-order merge strategy across files within a set: **if the same token is declared in multiple sources, the last declaration wins.** This is what makes per-brand override files work — a brand-specific file can selectively replace values from a global core simply by being later in the array.

The cross-file behaviour is the one architects underweight. **In a multi-brand or multi-theme system, the order of token files in the build pipeline is part of the architecture, not an incidental.** A misordered build can resolve brand overrides to the wrong values without throwing any errors. The fix is to make the order explicit in the build configuration and to validate that brand overrides resolve to brand values in CI (see 24).

---

## Relational and computed tokens

The shift from declarative tokens (every value spelled out) to computed tokens (values derived from rules) is the single largest architectural development since the three-tier taxonomy stabilised. **The convergent practitioner position: compute at authoring time, ship literals at runtime.** Both halves of that sentence matter.

### What computed tokens actually are

A computed token's value is derived from other tokens via an expression. The canonical examples:

- A modular type scale: `font-size-step-4 = font-size-base × ratio-modular^4`
- A density-aware spacing: `padding-button-md = spacing-inline-sm × density-multiplier`
- A composable layout dimension: `gutter-md = (spacing-inline-md + spacing-block-sm)`

The DTCG spec does not define an expression syntax. Tokens Studio has the most-adopted implementation (math expressions inside `$value` strings, resolved at export); Style Dictionary v4 supports expression resolution through preprocessors and custom transforms. Either path produces the same downstream artefact: a JSON file where the formerly-computed token now holds a literal value, ready for platform output.

### The convergent compromise — compute at authoring, ship literals

Computed tokens at authoring time produce three real benefits:

1. **Architectural resilience.** Updating `spacing-base` from 8 to 4 cascades through every spacing token automatically. The system reshapes from a single edit.
2. **Mathematical harmony.** Scales feel consistent because they *are* consistent — every step is the same ratio above the last, not a hand-picked value that approximates the ratio.
3. **New-brand efficiency.** A brand defined by 5–10 core primitives plus a standardised computation set can spin up its semantic layer mechanically rather than being hand-aliased token-by-token (see the Generative Token pattern in 24).

Computed tokens at *runtime* — that is, shipping the expression to the consumer instead of the resolved value — introduce two problems that outweigh those benefits in most cases:

1. **Resolution opacity.** A developer inspecting a CSS variable or a Swift constant sees an expression they cannot evaluate by eye. The mental model that "the token is the value" breaks; debugging becomes a graph traversal.
2. **Cross-platform fragility.** Web has `calc()` and accepts dynamic expressions; native platforms do not have a portable equivalent. Shipping expressions to runtime forces a per-platform decision about what to compute when, and the resulting variability undermines the cross-platform consistency the token system was supposed to provide.

**The practitioner answer: compute at authoring time inside Tokens Studio or Style Dictionary, validate the resolved literals in CI, and ship the resolved values to every consumer.** The expression is a build-time artefact; the runtime artefact is the literal. This collapses the runtime mental model back to "token equals value" while keeping the authoring-time benefits of relational logic intact.

### The scaling vocabulary — T-shirt vs. numeric vs. mathematical

The three competing naming conventions for scales express different priorities:

| Scale | Form | Strength | Weakness |
|---|---|---|---|
| T-shirt | `xs / sm / md / lg / xl` | Semantic, intuitive at small counts | Doesn't extend cleanly past 5–7 steps |
| Numeric | `100 / 200 / 300 / 400 / 500` | Extends indefinitely in both directions | The "meaning" of 200 is opaque without a reference |
| Mathematical | `step-(-1) / step-0 / step-1 / step-2` | Direct expression of the modular relationship | Designer-unfriendly; nobody reaches for `step-3` by intuition |

**The convergent 2026 pattern is a three-layer composite.** A mathematical scale defines the primitive values via a modular ratio. A numeric scale (`scale-100`, `scale-200`) names those values for internal reference. A T-shirt or functional semantic scale (`spacing-inline-md`, `font-size-body`) exposes them to component authors. Each layer serves a different audience: mathematical for the architect, numeric for the system internals, semantic for the consumer.

This is the same primitive → semantic split that 02 already names, with the addition that the primitive layer should now be understood as the *output of a mathematical expression* rather than as a hand-picked set of values. The token file's primitive values are literals (they have to be — the spec doesn't accept expressions in `$value`), but their provenance is mathematical.

### What CSS has absorbed, and what it hasn't

A meaningful shift in the 2024–2026 period: **the CSS platform has absorbed several capabilities that previously required token tooling to encode.** This narrows what the token pipeline is responsible for on web — but it does not narrow what the token pipeline is responsible for on native.

| CSS feature | Status | What it absorbs |
|---|---|---|
| `calc()` | Stable, universal | Build-time math; tokens supply the variables, CSS runs the arithmetic. |
| `clamp()` | Stable, universal | Fluid-value bounds; tokens define min/preferred/max, CSS handles the interpolation. |
| `color-mix()` | Baseline 2024 | Computed color blends without a build step. |
| Custom properties (`--var`) | Stable, universal | Token name → token value, with cascade and inheritance. |
| `:has()`, container queries | Stable, broadly supported | Context-aware token resolution at the consumer side. |

**The web architectural shift:** tokens increasingly store the *parameters* of a calculation (min/max bounds, ratios, base values) while the platform runs the *execution*. The token system maintains the single source of truth; the platform leverages its native performance.

This shift does not extend to native platforms. SwiftUI, Compose, Flutter, and React Native each have their own equivalents to some of these capabilities (Compose's `animateContentSize`, Flutter's `MediaQuery.textScalerOf`), but none of them is a portable substitute for CSS `clamp()` or `calc()`. **The practitioner consequence: the build pipeline still has to compute platform-appropriate outputs for native, even when the web side of the pipeline is doing less work than it used to.** The asymmetry is real and growing.

### Style Dictionary v4 as the platform engine

Style Dictionary v4 (released late 2024) is the load-bearing piece of the build pipeline in our practice's stack. The v4 changes that matter at the architecture level:

- **Native DTCG support.** v4 reads `.tokens.json` directly without a translation layer. The earlier era of "Style Dictionary format vs. DTCG format" is over.
- **Async transforms and preprocessors.** Computation, validation, and brand-specific overrides can run inside the pipeline rather than being external steps.
- **Improved composite-type handling.** Typography, shadow, border, and transition composites have well-defined output paths for each platform.
- **Custom format APIs** that produce idiomatic per-platform outputs (Swift, Kotlin, Dart, CSS, SCSS, TS).

The architect's role with Style Dictionary v4 is no longer "configure the pipeline"; it is "decide what computes where." Tokens Studio resolves math at authoring time; Style Dictionary v4 resolves brand overrides, density modes, and platform-specific units at build time; the runtime consumes literals. This division of labour is the convergent 2026 stack.

---

## Density and the responsive-density story

Density is the most under-specified theming dimension in the field. Curtis named it as one of the seven dimensions in the cost ladder we cite in 02. The field has not converged on a canonical encoding, and our existing materials are thin on what the practice should ship.

### Why density is harder than dark mode

Dark mode is a value substitution — every color token's `dark` mode value replaces its `light` mode value. The substitution is one-to-one and the math is straightforward.

Density is relational. A 20% reduction in spacing affects the relationships between every spaced element. Reducing `spacing/md` from 16 to 12 also implies reducing `spacing/lg` from 24 to 18 — if you don't, the visual hierarchy collapses. Reducing every spacing token proportionally is *not* the same as reducing them by intelligent amounts (a 20% drop on `spacing/xs` produces sub-pixel values that round inconsistently; a 20% drop on `spacing/3xl` produces visible distortion that a hand-tuned value would have avoided).

**Density is the dimension where naive multipliers fail and discrete sets win.** Both halves of this sentence have been litigated in the field; both halves are now settled enough to commit to in the practice's POV.

### Multiplier strategy vs. discrete-set strategy

The two extreme approaches:

**Global multiplier.** One token (`density-multiplier`) holds a scalar (0.8 / 1.0 / 1.2 for compact / comfortable / spacious). Every spacing, sizing, and type token references it. Pros: tiny token surface, easy to switch globally, easy to add a new density mode. Cons: a single multiplier cannot encode the per-token tuning that real density modes require (typography needs different treatment from spacing; small values need different treatment from large; accessibility floors must not be crossed).

**Discrete token set.** Each spacing and sizing token has explicit values for each density mode (`spacing-md = 8 / 12 / 16` for compact / comfortable / spacious). Pros: precise tuning at every step, accessibility floors can be pinned at every token. Cons: token-surface explosion, every new density mode requires touching every token.

**The convergent answer is the Hybrid Variable Mode Model.** Discrete values for each density step, but the values are *generated from a multiplier at authoring time and committed as literals*. The architect uses a multiplier to draft the discrete set; the design team tunes individual tokens where the multiplier produces wrong values; the resulting literals ship to runtime. Density is a mode dimension at the runtime layer (one `data-density` attribute switches the resolution) while the values themselves are hand-tunable in source.

This is the same compute-at-authoring-ship-literals pattern as for modular scales — applied to density, it solves the discrete-vs-multiplier debate by refusing to pick one and instead using each at the layer it works best.

### How many density steps

The legacy default is three: Compact / Comfortable / Spacious. This is the canonical encoding in Material 3, Adobe Spectrum, and Carbon. The field is moving on from it.

**Practice recommendation: two density steps as the default, three only when product analytics justify the middle tier.** The case for two (Compact / Comfortable, or Comfortable / Spacious depending on the surface): most products do not have a use case for all three, and the middle tier accumulates inconsistencies because designers cannot decide which of the adjacent tiers to defer to. Material 3's *Expressive* update (2024) implicitly endorses fewer-and-more-meaningful density steps via the way it treats density across the new component set.

The emerging pattern is **continuous density via a computed token** — density as a parameter in a spacing formula rather than a switch between named modes. This is the third option in the matrix; it is not yet a practice default because the tooling around it is immature and most clients cannot articulate a use case that justifies the architectural overhead. Flag it in client conversations; do not yet ship it as the default.

### Density as an axis the application picks, not a runtime contract

A subtle but load-bearing position: **density should be an axis the application picks its default on, using modality (touch vs. mouse vs. pen) as a signal, not as a determinant.** The token system exposes the density modes; the application's startup code consults the input modality (and any user preference) and selects a default; the user can override. The token system does *not* bind density to modality at the runtime level.

The reason: input modality is not deterministic. A laptop with a touchscreen accepts both touch and mouse input. A user with a stylus on a tablet wants high precision in some contexts and accessibility-grade target sizes in others. Binding density to a modality detection at runtime produces a system that defaults wrong as often as it defaults right. Exposing density as an application-level decision puts the contextual judgement where the contextual knowledge lives (in the product team), not where the token system can guess.

The starting heuristic the application should consult — not contract on:

| Input context | Target-size floor | Default density |
|---|---|---|
| Touch (mobile, tablet) | 44–48px minimum | Spacious or Comfortable |
| Mouse (desktop) | 24–32px minimum | Comfortable or Compact |
| Pen (Surface, Pencil) | 24px minimum (precision is high) | Comfortable |

The DS exposes the density modes; the application reads modality and product context; the user can override. **Target-size tokens (`size-interactive-min`) are a separate concern from density tokens** — they exist as accessibility floors that hold across density modes, not as values that scale with density.

### The mode-multiplication problem

The accumulating cost of every new theming dimension is exponential. Three brands × two themes × three densities = eighteen mode combinations. **The architectural fix is the same as the one 12-figma-practice already names for Figma Variables: one mode dimension per collection.** Color themes in the color collection. Brand in the brand collection. Density in the spacing-and-sizing collection. Components inherit each. The cost stays additive instead of multiplicative.

This works at the Figma layer and it works at the Style Dictionary build layer. At the runtime layer, the consumer composes the modes via attribute switching (`<html data-theme="dark" data-brand="x" data-density="compact">`) and the CSS variables (or native theme tokens) resolve accordingly. The architecture is recursive — one-dimension-per-collection at the source, one-attribute-per-dimension at the consumer.

---

## Strategic decision framework

The practice's defaults, after this synthesis:

1. **DTCG 2025.10 is the version-of-record.** Name it explicitly in proposals and tooling. Earlier "draft" language in practice materials should be updated.
2. **Authoring tools own the intent; the build pipeline owns the resolution.** Tokens Studio for math, modes-as-extensions, and designer authoring; Style Dictionary v4 for brand overrides, platform-specific units, and runtime output. Runtime consumes literals.
3. **Composite tokens are an authoring convenience, not a runtime contract.** Flatten composites at the build pipeline into the platform-specific atomic outputs the runtime expects. Carry the DTCG composite as the source-of-truth representation.
4. **Compute at authoring time, ship literals at runtime.** Modular scales, density-aware spacing, brand-derived semantic layers — all computed, all shipped as resolved values.
5. **Density is a discrete set generated from a multiplier at authoring time, hand-tuned where needed, committed as literals.** Two steps as the default; three only when product analytics justify; continuous density as the emerging pattern to watch.
6. **Density is application-default, modality-as-signal, not runtime-contract.** Target-size tokens are a separate accessibility-floor concern.
7. **Forward-compatible `$extensions` over proprietary spec deviations.** Use `$extensions` with a documented internal schema for modes, deprecations, and math. When the W3C Resolver Module stabilises, the migration path should be a key rename, not a structural rewrite.
8. **Unitless primitives, units applied at the transform layer.** A primitive value of `16` becomes `16px` for iOS (in points), `1rem` for web, `16dp` for Android, `16` for Flutter logical pixels. The primitive layer of the source remains platform-agnostic.

---

## Failure modes

- **Composite tokens shipped to runtime.** A CSS class that bundles `font-family / font-size / line-height / letter-spacing` looks tidy but breaks the moment one sub-property needs to vary independently (responsive line-height, locale-specific letter-spacing). Flatten at the build pipeline.
- **Computed expressions shipped to runtime.** A consumer-facing token whose value is `{spacing-base} * 1.5` puts the expression resolution in the runtime, which produces inconsistent results across platforms and obscures the value from debugging. Resolve at build time.
- **One mode dimension carrying multiple axes.** A "Compact-Dark-BrandA" mode collapses three independent concerns into one switch. Decompose into three modes across three collections.
- **Density encoded as a global multiplier with no per-token override.** Sub-pixel rounding at small values, visible distortion at large. Encode as discrete values generated from a multiplier, then tuned.
- **Three density steps with no analytics justification.** The middle tier accumulates inconsistencies. Two steps until evidence requires three.
- **DTCG `$extensions` used as a proprietary dumping ground without a documented schema.** Survives the round trip but defeats the interchange promise. Document the schema the practice uses inside `$extensions` and treat it as forward-compatible scaffolding for whatever the Resolver Module standardises.
- **Brand overrides relying on implicit file order in the build.** Array-order merge is correct behaviour, but undocumented ordering produces silent wrong resolution. Make the build order explicit and validate brand overrides in CI.
- **Treating the DTCG stable release as a full architecture.** The spec is interchange, not architecture. Modes, math, deprecations, and validation live in the layer above the spec — that is where most enterprise decisions are made.

---

## Tensions and open questions

1. **Tokens Studio math syntax vs. Style Dictionary preprocessors as the practice default for computed tokens.** Tokens Studio's math is more designer-accessible; Style Dictionary's preprocessors are more engineering-accessible. The practice has not yet committed to one. The pragmatic answer is to compute *at the layer closest to the source of the intent* — modular scales in Tokens Studio at authoring time, brand-specific value derivations in Style Dictionary at build time. The split is honest but not yet codified.

2. **The Resolver Module's eventual shape.** Modes-and-themes work-in-progress at the DTCG community group will eventually land. Practitioners encoding modes in `$extensions` today are betting that the migration will be a key rename. That bet is probably safe but is not yet validated. Watch the Resolver Module drafts closely through 2026.

3. **OKLCH / Display P3 / color-mix() in the token pipeline.** The DTCG Color Module is moving toward modern color spaces. Tools support OKLCH; native platforms do not consistently. The practice's color tokens should probably be defined in OKLCH at the primitive layer with sRGB / Display P3 fallbacks generated at build time, but the field has not converged on the canonical pattern. Treat as an open architecture question for the year ahead.

4. **APCA vs. WCAG 2.x contrast as the validation target.** APCA is the perceptually-correct successor; WCAG 2.x is the regulatory standard. Validation pipelines in 2026 typically support both; the practice should validate against WCAG for procurement claims and against APCA for actual readability. Flag both in client conversations.

5. **Continuous density vs. discrete steps.** The continuous-density-via-computed-tokens pattern is emerging but not yet a practice default. Most clients cannot articulate a use case that justifies the overhead. Watch for the use case to surface; do not lead with the pattern.

6. **Whether `$deprecated` should be a spec-level property.** The community is debating it; practitioners are using `$extensions.<vendor>.deprecated` in the meantime. A spec-level property would simplify validation and codemod tooling; the absence is felt at the operational layer (see 24).

---

## See also

- **02-design-foundations** — the spine of our token POV. This file is the depth layer beneath 02's positions on three-tier taxonomy, DTCG, and the build pipeline.
- **12-figma-practice** — the Figma-side mechanics of Variables, modes, scoping, and composite types. The "verify before recommending" flag on composite types and expression tokens in 12 is partially closed by this file: composite types are stable, expression tokens remain Tokens Studio + preprocessor territory.
- **18-motion-foundations** — composite motion tokens follow the same authoring-vs-runtime discipline as composite typography and shadow tokens.
- **23-typography-tokenisation** — the typography-specific deep dive that this file's DTCG composite treatment hands off to.
- **31-color-systems** — the color-specific deep dive that this file's DTCG, mode, and computed-token machinery applies to color. The OKLCH/P3 colorSpace question, the `color-mix()` round-trip gap, the `on-X` foreground tokens for multi-brand, and the AI-readable color schema all live there.
- **24-tokens-at-scale** — multi-brand portfolio architecture, governance, validation, versioning, and the Generative Token pattern that builds on this file's computed-tokens discipline.
- **14-accessibility** — pair tokens for contrast as the per-token validation pattern; this file's discrete-density discipline preserves accessibility floors.

---

*Provenance: DTCG 2025.10 as the first stable release of the Design Tokens Format Module (W3C Design Tokens Community Group, 28 October 2025, `designtokens.org/tr/2025.10/format/`) — verified May 2026. The terminal-node rule, `$type` allowlist, alias resolution semantics, and array-order cross-file merge are from the 2025.10 Format Module specification. The compute-at-authoring-ship-literals discipline, the composite-tokens-as-authoring-convenience position, the Hybrid Variable Mode Model for density, the two-step density default, the application-default-modality-as-signal density framing, the three-layer composite scale (mathematical → numeric → semantic), and the CSS-platform-absorption-on-web-not-native asymmetry are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-architecture-extensions/` (May 2026). Style Dictionary v4 release (late 2024) and feature set are from `styledictionary.com` documentation. Tokens Studio math syntax is from the Tokens Studio plugin documentation. Density as theming dimension is from Nathan Curtis (EightShapes, *Design Tokens* Nov 2024), already cited in 02. The three-tier taxonomy and the seven-dimension theming cost ladder are aligned with 02-design-foundations.*

You are researching design token architecture for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice already ships W3C DTCG-compliant token sets on every engagement, treats Curtis's three-tier taxonomy (Primitive / Semantic / Component + DTCG Composite) as the default, ships multi-theme architecture from day one, and runs the Figma → DTCG → Style Dictionary → platforms pipeline. We have well-established positions on naming, theming dimensions (Curtis's seven), surface-as-inheritance, the manual-vs-automation tension, and component-tokens debate. This research is the layer *underneath* that established practice — the spec-level depth, the relational/computed-token frontier, and density as a token concern — that our existing materials are thin on. Specifically not in scope: re-deriving the three-tier taxonomy, the DTCG procurement-grade argument, or the basic theming-from-day-one position. Those are settled. We need depth where the field has moved and our positions are thin or out of date.

This is not an introductory tokens guide — assume the reader knows DTCG, knows what primitive/semantic tokens are, knows Style Dictionary's job, has shipped tokens to production, and is familiar with Figma Variables. Explain token architecture at the level a senior DS lead needs to make architectural decisions on enterprise engagements where the easy answers are already known.

Research scope — cover all of the following. Use these as the section spine of the output.

1. The DTCG specification at practitioner depth

   - The current state of the W3C Design Tokens Community Group specification as of mid-2026 — what is stable, what is draft, what is contested.
   - `$value`, `$type`, `$description`, `$extensions` — what each allows, what each forbids, where the spec is under-specified in practice.
   - Composite tokens — typography, shadow, border, transition. What the spec says vs. what tools actually implement. Where round-trip fidelity holds and where it breaks.
   - Alias resolution semantics — `{token.path}` references, the rules for circular reference detection, cross-collection / cross-file alias behaviour, what happens when an alias targets a deleted token.
   - The `$type` allowlist (color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography, etc.) — what's required, what's optional, what tools default differently.
   - What the spec leaves out: modes/theming, conditional values, math expressions, validation rules.

2. Relational and computed tokens

   - Mathematical relationships between tokens — `spacing-md = spacing-base * 1.5`. What Style Dictionary supports today, what DTCG supports in spec vs. extensions, what tools (Tokens Studio, Specify, others) implement.
   - The T-shirt scale (xs/sm/md/lg/xl) vs. numeric scale (100/200/300) vs. mathematical scale (modular ratio) debate — when each is appropriate, how they interact at the semantic layer.
   - Composable units — `padding = spacing-inline-md + spacing-block-sm`, density multipliers, ratio-based scales.
   - The trade-off: computed tokens express intent more precisely but reduce predictability for consumers (the value isn't visible without resolution). Where the field has converged on the right balance.
   - Style Dictionary's transform/format extension points and how teams encode computed values today.
   - The relationship to CSS native features — `calc()`, custom properties, `clamp()` — and whether the platform is absorbing what tokens previously had to encode.

3. Density and the responsive-density story

   - Density as a theming dimension — Curtis names it; the field has not converged on the right encoding.
   - Density multipliers vs. density-specific token sets — the trade-off and the convergent answer.
   - The relationship between density and spacing tokens, type scales, target-size tokens, and component sizing.
   - Compact / Comfortable / Spacious as the canonical three-tier, or whether the field has moved past it.
   - Density on touch vs. mouse vs. pen contexts — the responsive question and how a token system can encode it without exploding the surface.
   - Where density fits in the mode multiplication problem (covered in our 12-figma-practice file) — when density is a mode dimension and when it's an axis of the spacing tokens themselves.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus, state it; where decisions are context-dependent (computed-token use, density encoding strategy), give a decision framework rather than declaring a winner. Flag where the DTCG spec is genuinely under-specified vs. where it's stable. Where claims depend on spec or tool state — feature names, version numbers, what's shipped vs. drafted — date them and note the verification path (W3C DTCG editor's draft, Tokens Studio docs, Style Dictionary docs, Figma release notes). Include a references section linking to primary sources (the W3C Design Tokens Community Group editor's draft, Style Dictionary docs, Tokens Studio docs, Nathan Curtis's EightShapes writing, practitioner write-ups by Brad Frost, Robin Rendle, and others at this depth).

Depth: Expert audience. Do not explain what a token is, what semantic vs. primitive means, what DTCG is for, or what Style Dictionary does. Explain the spec depth, the computed-token trade-offs, and the density encoding decisions at the level a senior DS architect needs to advise an enterprise engagement.

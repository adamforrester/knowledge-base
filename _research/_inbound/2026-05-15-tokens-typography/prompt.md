You are researching typography tokenisation for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice ships typography in its W3C DTCG-compliant token set on every engagement, but our existing materials treat typography as a token category at the same depth as color and spacing — which is wrong. Typography is the most under-tokenised foundation in most design systems we audit, and the 2025–2026 web platform has shipped capabilities (fluid type via `clamp()`, container queries, variable fonts as first-class CSS, Dynamic Type bridges on iOS) that change what good typography tokenisation looks like. This research is the typography-specific depth our existing 02-design-foundations and 12-figma-practice files don't reach.

Specifically not in scope: re-deriving why a type scale is useful, why semantic naming beats poetic naming, or why typography belongs in tokens at all. Those positions are settled.

This is not an introductory typography guide — assume the reader knows what a modular scale is, what `font-feature-settings` does, what a variable font is at a high level, what `rem` and `em` mean for tokenisation, and what Dynamic Type does on iOS. Explain typography tokenisation at the level a senior DS lead needs to make architectural decisions on engagements where typography is a brand-critical surface (most agency work).

Research scope — cover all of the following. Use these as the section spine of the output.

1. The shape of a typography token set

   - The minimum viable set of typography tokens (font-family, font-size, line-height, font-weight, letter-spacing, font-style, text-transform) and what's optional.
   - DTCG composite typography tokens — bundling the above into a single named token (`heading-large`, `body-medium`). What the spec defines, what tools implement, where the composite breaks down.
   - Atomic typography tokens vs. composite — when each is appropriate. The argument for shipping both.
   - Brand fonts vs. system fonts as tokens — how the fallback stack is encoded, how the variable / static font distinction is exposed.
   - The trade-off between many composite tokens (heading-1 through heading-6, body-large/medium/small, caption, label, button, etc.) and few atomic tokens consumers compose themselves.

2. Modular scales — the math, the trade-offs, the choice

   - The canonical modular ratios (1.067 / 1.125 / 1.200 / 1.250 / 1.333 / 1.414 / 1.500 / 1.618 / 1.667 / 1.778 / 2.000). Which work for which contexts.
   - When a strict modular scale should be broken — display sizes, body text legibility, the "1.250 at small sizes, 1.500 at display" pattern.
   - Modular scales vs. T-shirt scales (xs/sm/md/lg/xl) vs. numeric scales (100/200/300). Where each lives in the token tier.
   - The relationship between scale ratio and brand personality (tight 1.125 for utility-dominant systems, expressive 1.500+ for editorial brands).
   - Tools and resources that practitioners reach for (Typescale, Modularscale, Utopia, Type Scale Clamp Generator).

3. Fluid type, `clamp()`, and container queries

   - Fluid type via `clamp(min, preferred, max)` — the math (the viewport-based calculation, the accessibility-safe minimum, the responsive cap).
   - The 2026 state of fluid-type tooling — Utopia, fluid-typography generators, the math behind viewport-relative units in fluid expressions.
   - Container queries (Baseline 2023+) and how they change the responsive-type calculus — type that responds to its container, not the viewport.
   - When fluid type is the wrong answer — long-form reading, locale-aware sizing, accessibility-constrained contexts where users override the system font size.
   - How fluid-type tokens are encoded — as a single `clamp()` string token, as a primitive triplet (min/preferred/max), as a function in code.
   - The accessibility implications — WCAG 1.4.4 text scaling, the 200% requirement, where fluid type helps and where it hurts.

4. Variable fonts as a tokenisation problem

   - Variable font axes — wght (weight), wdth (width), opsz (optical size), slnt (slant), GRAD (grade), and the named instance system.
   - Tokenising axis values — `font-weight: 450` is meaningful in a variable font, meaningless in a static one.
   - Optical size (opsz) as the single most under-used variable axis — display vs. text-size optical adjustments.
   - The OTF/WOFF2 delivery story in 2026 — file-size impact, subsetting, font-display strategy.
   - Variable fonts in Figma — what Figma supports, what it doesn't, what the round-trip to DTCG looks like.
   - The trade-off: variable fonts unlock continuous design but require named-token tiers (mapping continuous axis values to semantic tokens) to remain useful at the DS layer.

5. Line-height, leading, and the relationship to font-size

   - Line-height as a function of font-size — the convergent ratios (1.4–1.6 for body, 1.1–1.3 for display).
   - Unit-less vs. dimensional line-height in tokens — the case for unit-less.
   - Optical leading — when line-height should be expressed as a multiplier of the font's intrinsic line gap rather than a hard ratio.
   - Tokenising line-height per font-size token (composite typography) vs. as a separate scale.
   - The mobile vs. web divergence — iOS's leading-trim, Compose's `lineHeightStyle.Alignment`, web's emerging `text-box-trim` / `text-edge` (Baseline status as of mid-2026 — verify).

6. Multi-script and multi-locale typography

   - Tokenising fonts across writing systems — when a single token set works (Latin + similar scripts) and when separate scales are required (CJK, Arabic, Devanagari, Thai).
   - Locale-aware type scales — Arabic typically needs ~10% larger font-size than Latin at the same readability; CJK needs different line-height ratios.
   - The DS contract — does the DS ship locale-specific token sets, or expose a typography token API the application layer overrides per locale.
   - Variable fonts as a multi-script tool — single-binary multi-script fonts, the limits of the current variable-font tooling for non-Latin scripts.
   - The relationship to our existing 13-internationalization-and-rtl file's multi-script type treatment.

7. Native platform translation

   - Style Dictionary outputs for typography on iOS (SwiftUI / UIKit) — `Font` extensions, `UIFontDescriptor`, the relationship to Dynamic Type.
   - Android Compose — `Typography` in MaterialTheme, the relationship to sp units and accessibility text-scale.
   - Flutter — `TextTheme`, `TextStyle`, `MaterialTextScaler`.
   - React Native — typography token packages, the absence of native Dynamic Type integration without bridging.
   - The Dynamic Type / accessibility-text-scale story — how a typography token system respects (or fails to respect) the system text scale on each platform. Cross-reference to our 14-accessibility and 16-mobile-accessibility-implementation files where this is partially covered.

8. The relationship to AI-readable token descriptions

   - Why typography tokens benefit most from descriptions (the visual differences are subtle; AI agents cannot infer intent from the values alone).
   - What a good typography token description contains — purpose, use cases, hierarchy position, what NOT to use it for.
   - The role of token descriptions in Figma MCP context and AI-generated component code that respects typography hierarchy.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus (modular scales, unit-less line-height, fluid type for marketing-tier responsive design), state it; where decisions are context-dependent (composite vs. atomic, fluid vs. static, when to break a modular scale), give a decision framework. Flag platform / spec / tool state — `text-box-trim` Baseline status, container query support, Figma variable-font support — and date claims with the verification path (caniuse.com, MDN, Figma release notes). Include a references section linking to primary sources (W3C CSS specs, MDN typography docs, Apple HIG typography, Material 3 typography, Utopia documentation, primary practitioner writing on type systems).

Depth: Expert audience. Do not explain what a font is or what `rem` means. Explain what a sufficient typography tokenisation looks like in 2026 across web and native, where the field has converged, and what design system architects should standardise on.

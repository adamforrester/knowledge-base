You are researching color systems in design systems for a senior design
systems practitioner at a digital agency. The output is a structured
knowledge document. Color is one of the largest topics in design
systems and one of the most under-architected — most systems we audit
ship a palette and a few semantic aliases and stop there. The
2024–2026 platform shifts (OKLCH and the perceptual-scale era, P3
wide-gamut becoming default on modern displays, the WCAG-2-vs-APCA
contrast debate going live, Material 3 dynamic color, Tailwind v4 +
Radix Colors raising the bar on generated ramps, `color-scheme` and
forced-colors maturing, DTCG's color-token treatment stabilising) have
changed what good color tokenisation and theming look like. This
research is the depth our existing 02-design-foundations,
22-token-architecture-extensions, and 24-tokens-at-scale files don't
reach.

This is not an introductory guide — assume the reader knows what a
design system is, knows tokenisation, knows WCAG, and is fluent in
modern CSS color (`oklch()`, `color-mix()`, relative color syntax,
P3). Don't explain what `oklch()` is — explain why the field has
converged on it for ramp authoring, what it doesn't fix, and where the
trade-offs are.

Research scope — cover all of the following:

1. The shape of a color token system

- Three-tier architecture (primitive / semantic / component) applied
  to color specifically: where the boundaries fall, what each tier
  actually contains, what leaks across.
- The numeric-scale-vs-named-step naming debate (50/100/200 …; 50/60/70
  half-steps per Couldwell; named-only per Radix; surface/text/border
  semantic-only per Stripe). What each conveys, what each costs.
- Token volume — how many primitives, how many semantics, how many
  component-tier color tokens is the right shape for a production-grade
  agency engagement.
- The "color-by-context" model (Perez-Cruz: 4 background contexts × N
  groups, vs. enumerating every shade). Where it pays off, where it
  doesn't.
- The role of `color-mix()` and relative color syntax in *reducing*
  the number of tokens a system has to ship.

2. Color spaces — sRGB, P3, OKLCH, HCT

- Why OKLCH became the default for ramp authoring (perceptual
  uniformity, predictable lightness math) and what it doesn't solve
  (it's not a gamut, brand fidelity still requires source-color anchoring).
- P3 wide-gamut: when to ship P3 alongside sRGB, the
  `@media (color-gamut: p3)` and `display-p3` paths, gamut-mapping
  strategies, the iOS/macOS/Android wide-gamut display reality.
- HCT (Material 3) and how it differs from OKLCH and from CIELAB; whether
  HCT-anchored ramps interop with non-Material systems.
- The CSS Color 4/5 surface — relative color syntax, `color-mix()`,
  `oklch()`/`oklab()`, `color()` function with named spaces.
- Conversion and round-trip fidelity (Figma → tokens → CSS → runtime):
  where color drifts, what tools faithfully preserve OKLCH/P3, where
  conversions silently quantise back to sRGB hex.

3. Accessible contrast — WCAG 2 vs. APCA, and the live debate

- What WCAG 2.x contrast actually measures, where it's known to fail
  (the dark-mode under-prediction, the small-text trap, the
  yellow-on-white over-prediction).
- APCA (Lc-based, perceptual) — the model, the threshold tables (Lc
  60/75/90), where it's been adopted (Adobe Spectrum's research,
  GitHub Primer, others), where it hasn't, and the WCAG 3 status as of
  mid-2026.
- How systems are anchoring contrast on a generated ramp (e.g., "step
  6 ↔ step 11 = AA on white" type rules — Radix's contrast-pair
  guarantees, Tailwind v4's contrast-aware shades).
- The disabled-state contrast exemption (WCAG 2.2 1.4.3 and 1.4.11)
  and how systems are handling it without leaning on the exemption.
- The forced-colors / Windows High Contrast Mode contract — why most
  design tokens are *bypassed* in this mode and what the system can
  still control.

4. Theming architecture

- Light / dark / brand themes as orthogonal axes vs. as compounded
  themes; multi-brand × dark/light × density.
- Dark-mode surface elevation — the "lift" pattern (Material), the
  shadow-fade-becomes-surface-lighten swap, why dark-mode dark-on-dark
  is harder than the inverse.
- The semantic→primitive aliasing chain: how a `color/surface/raised`
  token resolves through theme to a primitive, where the chain breaks,
  how composite tokens (DTCG) handle this.
- Theme switching mechanics: CSS custom properties + `color-scheme`,
  `prefers-color-scheme`, runtime override; the FOUC / theme-flash
  problem, server-rendered theme decisions.
- Multi-brand at the color layer (the T-Mobile/Metro, Ford/Lincoln
  pattern from VML's library): single semantic surface, swappable
  primitive tier; what breaks when brand B's "primary" doesn't pass
  contrast on brand A's neutrals.
- Density and theme — what density costs at the color layer (border
  contrast, divider visibility, focus ring on a denser layout).

5. Palette generation — tools and methods

- Contrast-anchored ramp methods (Leonardo / Adobe; the
  contrast-pair-as-source-of-truth approach).
- Perceptually-uniform OKLCH ramps (the
  fixed-chroma / lightness-step pattern).
- Curated/hand-tuned ramps (Radix Colors, Open Color, Tailwind v4):
  what they trade off, when they're the right answer for an agency
  engagement.
- Material 3 dynamic color (HCT-based, monet/wallpaper-derived) — what
  this means for systems that don't ship on Android.
- Brand-anchored vs. system-anchored ramps: when the brand color is
  step 9 vs. when it's step 6; the
  contrast-step-vs-brand-step alignment problem.
- Tooling depth (Leonardo, Tints.dev, Atmos, Material Theme Builder,
  Radix Colors, Tailwind v4 generator) — what each is good at, what
  none of them are good at.

6. Brand color vs. UI color — the unity/cohesion tension

- The Perez-Cruz framing: brand expression vs. UI legibility, where
  unity (one strict palette) over-constrains and where cohesion
  (related-but-distinct palettes) collapses into chaos.
- Status / semantic carve-outs (success / warning / error / info):
  why semantic colors are an *exception* to brand expression, the
  red-can't-mean-brand problem, the "system green" stability rule.
- Editorial / marketing color vs. product UI color — when to ship two
  palettes (brand-display + product-UI), when one is enough.
- The brand-color-against-its-own-system trap: when a brand's signature
  color fails contrast on its own neutrals and the system has to either
  shift the brand color or carve out a non-brand "primary action" color.

7. Data-visualisation palettes

- Categorical / sequential / diverging — why each needs its own
  palette and why a system's UI palette almost never serves any of
  them.
- Color-blind safety (the
  Viridis/IBM-Carbon-charts/Tableau-color-blind-safe approach) and
  the color-not-sole-carrier rule applied to charts.
- Perceptual ordering — why a sequential palette derived from OKLCH
  steps reads more accurately than one derived from HSL.
- Where the data-vis palette lives in the token architecture: a
  separate primitive scale (`viz-categorical/1..12`) vs. mappings off
  the UI palette.
- The 12-color limit, the categorical-as-pattern alternative, the
  table-fallback contract.

8. Native platform translation + AI-readable color descriptions

- iOS UIKit/SwiftUI semantic colors (`.systemBackground`, `.label`,
  the dynamic-color contract); how DS color tokens map to or replace
  the system palette.
- Material 3 dynamic color on Android (HCT, the wallpaper-derived
  scheme), Compose color roles, the `MaterialTheme.colorScheme` API;
  what a third-party DS does on Android in 2026.
- React Native / Flutter color theming — `useColorScheme`, theme
  providers, the platform-divergence cost.
- AI-readable color descriptions — the `when_to_use`, `avoid_when`,
  `paired_with`, `meaning`, `contrast_with` fields a color token needs
  to be agent-consumable (per the practice's 15-ai-in-ds AI-readable
  metadata patterns and 23-typography-tokenisation §AI-readable).
  Which fields move the needle for AI, which are nice-to-have.

Output format: Structured markdown. Use section headings that match
the numbered scope above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather
than declaring a winner. Flag areas where DS tools (Figma Variables,
Style Dictionary, Tokens Studio, Leonardo, code pipelines, etc.) have
known gaps that practitioners work around. Where claims depend on
current platform state — feature names, version flags, percentage
figures, browser support — date them and note the verification path.
Include a references section linking to primary sources (W3C CSS Color
4/5, WCAG 2.2, APCA spec / wcag3 status, Radix Colors, Tailwind v4
docs, Material 3 / HCT, Apple HIG color, Leonardo, DTCG color-token
spec, Adobe Spectrum / GitHub Primer color docs).

Depth: Expert audience. Do not explain what OKLCH is, what a
contrast ratio is, what dark mode is, what `color-scheme` does —
explain why the field's converged on the architecture it has, what
the live trade-offs are, and where current tooling silently fails to
preserve what the system encoded.

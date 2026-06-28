---
type: practice-area
title: Color Systems
description: Three-tier color architecture, the committed semantic vocabulary (background/foreground/action-states/border, not surface) decided against a seven-system field survey, OKLCH-as-authoring + sRGB/P3 as render targets, the WCAG-2-as-floor / APCA-as-quality-bar discipline, the orthogonal-axes theming model with the dark-mode lift pattern and forced-colors transparent-border trick, contrast-anchored ramp generation, the brand-vs-UI carve-out, isolated data-vis namespaces, native platform translation as integration not mapping, and the five-field AI-readable color schema.
tags: [extension, color, tokens, oklch, p3, apca, theming, dtcg]
timestamp: 2026-06-28
---

# 31 — Color Systems

> Color is the most-shipped, least-architected foundation in the design systems our practice audits. Most ship a palette and a few semantic aliases and stop there; the architecture problems — gamut, contrast model, theming axes, brand-vs-UI carve-outs, data-vis isolation, native-platform integration, AI consumability — are deferred to "we'll fix it later," which translates to "we'll fix it in the second engagement, expensively." The 2024–2026 platform shifts have made deferral costly: OKLCH is the field-default authoring space, P3 ships on most modern displays, the WCAG-2-vs-APCA debate is live and unresolved, Material 3's HCT-based dynamic color has redrawn the Android contract, contrast-aware generated ramps (Tailwind v4, Radix, Leonardo) have raised the bar on what a "color system" delivers, and AI agents are now first-class consumers of color tokens. This file is the depth our existing 02-design-foundations, 22-token-architecture-extensions, and 24-tokens-at-scale files don't reach: the shape of a color token system, color spaces and round-trip fidelity, the contrast model, theming architecture, palette generation, the brand-vs-UI tension, data-vis as a separate problem, native platform translation, and the AI-readable description schema color tokens specifically benefit from.

---

## Why color needs its own file

02-design-foundations sketches the role-based color group model (Perez-Cruz) against numeric scales (Couldwell) and treats color, type, space, and motion as peer foundations. 22 and 24 cover the token architecture, DTCG modes, and multi-brand portfolio — color is named, but the color-specific depth (color spaces, contrast model, theming axes, data-vis isolation, native integration, AI fields) lives nowhere. 14 and 28 cover contrast as accessibility law; the *system architecture* the contrast model implies (anchoring contrast on the ramp, not at the consumer site) is unaddressed. 23-typography-tokenisation.md's argument — that the foundation needs its own file once the platform has moved further than the foundations file can carry — applies to color one-to-one.

What this file extends: 02's role-based color framing; 22's DTCG composite-token mechanics applied to color; 24's multi-brand validation matrix at the color layer; 14's WCAG contract pushed further into APCA territory; 28's web-accessibility implementation depth; 16's mobile-accessibility translation; 11's cross-platform native-color integration. What it doesn't replace: any of those. This is the color-specific layer on top.

---

## 1. The shape of a color token system

### Three-tier architecture, applied to color

The same primitive / semantic / component spine that holds for typography and spacing applies to color, with a sharper definition than for the other foundations. Both research agents converged on this without dispute; the live debate is *where the boundaries fall and what's permitted to leak across them*.

**Primitive tier.** The ramps themselves — hue scales (`blue/1..12`, `neutral/50..950`, etc.), alpha/transparency siblings, anchor colors (true black, true white, an explicit "natural" warm-neutral if the system has one). Primitives carry zero contextual meaning: `blue/9` is just blue at step 9, not "primary action." This is *the* tier where gamut, color space, and ramp math live.

**Semantic tier.** Intent bound to primitives via aliasing — `color/foreground/primary`, `color/background/raised`, `color/border/subtle`, `color/action/default`, `color/foreground/danger` (the committed vocabulary; see *The semantic role vocabulary* below). The semantic tier is the *contract* layer; consumers reach for it, not for primitives. Mode resolution (light/dark/brand/density) happens at the semantic→primitive alias, never at the consumer site.

**Component tier.** Per-component overrides where divergence is genuine — a `Badge` whose background is heavier than the equivalent `Tag`'s, a focus ring tuned to a contrast-specific blue distinct from the action blue. **Component-tier color tokens should be the smallest of the three sets — typically <10 across an entire system, not per-component.** Both passes are emphatic on this; the external pass goes further and treats component-tier color tokens as a sign of architectural failure to be designed out wherever possible. The rule of three from component design applies: if three components diverge from the semantic, promote a new semantic; if only one does, ship a component-tier override.

**Where boundaries leak.** The dominant failure is consumers reaching past semantics for primitives — `var(--blue-9)` in component CSS — which breaks both theming and branding. The fix is twofold: ship a *complete* semantic tier so consumers don't have to reach past it, and lint primitives out of consumer-facing CSS at build time. Tailwind v4 still ships primitives as utility classes, which a system either accepts (with discipline) or constrains via an internal preset.

### The naming debate — five paradigms, one practitioner shape

Both passes converge on five distinct paradigms, each with a different cognitive cost.

| Paradigm | Example | Underlying logic | Trade-off |
|---|---|---|---|
| **Tailwind / Material numeric** | `blue-50`, `blue-500`, `blue-900` | Abstract lightness increments, 10 steps. | "500" doesn't carry the same lightness across hues; the role of each step is convention, not contract. |
| **Couldwell half-step** | `blue-50`, `blue-55`, `blue-60` | Two-digit increments to allow 5% half-steps for subtle UI shifts. | Token-volume explosion; high cognitive load on when to reach for a half-step. |
| **OKLCH-perceptual** | `blue-45`, `blue-90` | Step number = OKLCH lightness × 100. `blue-45` is literally L=0.45. | Absolute predictability; demands committing to OKLCH end-to-end and breaking from the legacy 100–900 grammar. |
| **Radix 1–12 (semantically-bound)** | `blue-1`..`blue-12` | Each step has a *named role*: 1 = app background, 9 = solid, 11 = low-contrast text, 12 = high-contrast text. | Production-quality out of the box, contrast guarantees baked in; opinionated to Radix's product-UI assumptions, low-resolution for fine-tuned text contrasts beyond 12 steps. |
| **Stripe semantic-only** | `surface`, `text-subtle`, `border-muted` | Primitives are private to the build; only semantics are published. | Resilient to theming and re-branding; demands strict governance to prevent designers from introducing one-off undocumented values. |

**The convergent practitioner shape: numeric scale at primitives, role-aligned step grid behind it, semantic tier as the public surface.** Consumers see semantics. Behind the curtain, the primitive ramps use a numeric scale where step N has the same *contrast role* across every hue (the Radix discipline applied to the math). This buys role-step alignment without forcing the Radix vocabulary on the consumer surface, and lets the system choose the numeric grammar (`50..950`, `1..12`, `45/90`-OKLCH-coupled) based on engagement preference.

### The semantic role vocabulary — background/foreground, not surface

The grammar above governs primitives; the semantic tier needs its own committed vocabulary, and the field does not hand us a clean one. A seven-system survey (Material 3, Radix, Tailwind, GitHub Primer, Shopify Polaris, IBM Carbon, Adobe Spectrum) splits almost evenly on the container term: **`background`** (Primer's `bgColor`, Carbon, Spectrum, Tailwind/shadcn, and Radix's page layer) against **`surface`** (Material 3, Polaris, and Radix's component layer) — roughly five to three. There is no dominant convention to defer to, so the tie-breaker is internal: **our consuming brands name the page `background` and its contents `foreground`** (the New Balance shape), and a matched antonym pair reads more honestly than `surface` paired with nothing. We commit to it. *This supersedes the `surface/*` examples used illustratively elsewhere in this file (carried over from the source research pass); where this file describes an external system's roles — Material's `surface` tiers, the dark-mode lift — that system's own term stands.*

**The container/content split carries the interactivity rule.** Backgrounds are inert — page, cards, overlays, wells, semantic tints. Foregrounds sit on top and *may* be interactive; a link is an interactive foreground. The one case the pair doesn't resolve by itself is the button fill, which is both an interactive element and a surface for its own label. Polaris answers it by separating an interactive **fill** role from the inert container, and we take the same move: interactive fills live under the `action` role, never under `background`, so "backgrounds aren't interactive" holds literally.

**On the one point the field is unanimous, defer to it: the `on-*` pair token.** Every surveyed system ships a paired-contrast foreground — `on-primary` (M3), `fgColor-onEmphasis` (Primer), `text-*-on-bg-fill` (Polaris), `text-on-color` (Carbon), `*-foreground` (shadcn), `--accent-contrast` (Radix), `static-white/black` (Spectrum). The name varies; the mechanism is universal. We name ours `foreground/on-*` and treat it as non-negotiable — the forced-foreground luminance flip (§3) is how it stays compliant across a brand swap.

**Interactivity is states on roles, not a dedicated namespace.** Six of the seven express interaction as state variants of an existing role — M3 state-layer opacities, Radix step numbers, Tailwind/Spectrum/Polaris/Primer `-hover`/`-pressed`/`-focus` (Spectrum's `-down`/`-key-focus`) suffixes. Only Carbon ships a standalone `interactive`/`button-*`/`link-*` tree, and New Balance made the same call — but it pays for it in token volume and in duplicating text/icon/border across both a content group and an interactive group. We take the majority shape: `action/{default,hover,pressed,focus,inactive}`, with `inactive` (contrast-preserved) as the default disabled treatment per §3. One caveat the gamut enforces: **text on a saturated fill targets AA, not the escalated high-contrast bar** — a vivid mid-tone is bounded, no pure black or white label reaches 7:1 on it, so HC escalation applies to text-on-neutral-surface, not text-on-vivid-fill. (See 28-web-accessibility-implementation §7 on the surface-floor rule that the same saturated foregrounds are validated against.)

### Token volume — measuring the same thing

Both research passes appear to disagree on token volume; they're actually measuring different units. The external pass cites "10–15 primitive scales, 40–60 core semantic tokens, virtually zero component-level"; the Claude pass cites "80–170 primitive *tokens* (10–14 hues × 10–12 steps)." Twelve ramps × twelve steps ≈ 144 — they agree. The synthesis:

- **Primitives:** 10–14 hue ramps (neutrals, brand, brand-secondary, 4–6 status/accent hues) × 10–12 steps each, with parallel alpha siblings (per-hue or a shared 8–10-value alpha set) and optional P3 siblings for brand-critical primitives. ~120–170 atomic primitive color tokens at the high end.
- **Semantics:** 30–60 semantic color tokens. Text 4–6, surface 4–8, border 3–5, action 4–6 × states, status 4 hues × 4–6 roles each. The shape that fails is the one shipping hundreds of semantic tokens trying to anticipate every state of every component — that is component-tier work mistakenly elevated.
- **Components:** <10 across the system. If the count climbs, the semantic tier is incomplete.

**Smaller systems ship 60% of these numbers; brand-heavy editorial systems exceed them.** The shape is a target, not a quota.

### Color-by-context (Perez-Cruz)

The "15 pinks → 4 contexts" framing — tokens defined by the background context they sit on, not by every theoretical pairing — pays off where the system has multiple background contexts that fundamentally change which colors work: editorial / marketing-led systems with brand-saturated heroes, dark-image-overlay surfaces, and inverse sections; multi-brand systems where each brand has its own dominant surface; systems with a strong "inverse" mode (dark-on-light header inside a light-on-dark page).

Where it doesn't pay off: product-UI systems with one or two surface contexts. Over-engineered context-grouped palettes for a default surface and a sunken card surface produce tokens for contexts the product never uses.

**The rule:** enumerate the contexts the *product* actually has before building the context-grouped palette. Three or fewer surfaces dominating the product → flat semantic tier is enough. Four or more, especially with brand-saturated or inverse contexts → context grouping pays for itself.

The external pass goes further and treats the context matrix as the *primary* mechanism for keeping token volume sane — primitive selection is dynamically restricted by the surface a token sits on, so the system can't ship a text color that fails contrast on its declared context. This is a stronger position than the Claude pass and the practice should adopt it where the engagement has the surface variety to justify it.

### `color-mix()` and relative color syntax — token-volume reduction

CSS Color Module Level 5 (`color-mix()`, relative color syntax — `oklch(from var(--brand-9) calc(l - 0.05) c h)`) lets the system *derive* states from a base color rather than ship every state as a separate token:

```css
--color-action-primary-rest: var(--brand-9);
--color-action-primary-hover: color-mix(in oklch, var(--brand-9), black 8%);
--color-action-primary-pressed: color-mix(in oklch, var(--brand-9), black 16%);
--color-action-primary-disabled: color-mix(in oklch, var(--brand-9), var(--surface) 60%);
```

One source, all states derived. Stripe-class systems with 80+ semantic tokens can collapse to 30–40 if state derivation is committed to.

**The tooling-fidelity catch.** Style Dictionary 4.x (mid-2026) doesn't natively preserve `color-mix()`/relative-color expressions — its build pipeline emits the resolved value, not the expression. To preserve runtime composition you bypass Style Dictionary's color transforms or treat the expression as a string token, surrendering cross-platform translation. **The practitioner who reduces token volume via `color-mix()` accepts that the build pipeline won't generate the iOS/Android equivalents** — the relative-color logic stays web-only, and platforms get explicit state tokens. The community has open issues asking for a `color-mix` transform; not in core as of Q2 2026 (verification path: Style Dictionary changelog).

Relative color syntax has the same gap in design tools: Figma Variables can express it as a literal string but doesn't *resolve* it on the design canvas as of mid-2026. Design ↔ code parity breaks; the value the engineer sees is not the value the designer authored. The pragmatic mitigation: compute derived colors in Figma manually and ship as named tokens, accept the redundancy, hold the runtime composition as a future cleanup once tooling catches up.

---

## 2. Color spaces — sRGB, P3, OKLCH, HCT

### HSL is dead for ramp authoring

Both passes are emphatic. HSL's lightness scale is a mechanical RGB midpoint, not a perceptual quantity — HSL `60 100% 50%` (yellow) reads dramatically brighter than `240 100% 50%` (blue), even though both are nominally "50% lightness." The implication compounds across every downstream operation: dark-mode inversion produces inconsistent perceived weights, algorithmic ramp generation produces non-uniform contrast, gradient interpolation passes through dead-grey midpoints. The 2024–2026 field has moved off HSL for ramp authoring; treat HSL as a legacy encoding, not an authoring space.

### Why OKLCH won

Three reasons.

**Predictable lightness math.** L=0.5 in OKLCH is roughly 50% perceptually lighter than L=0; L=0.7 is about 70%. Designers wanting step 6 of every hue ramp to *look the same lightness* get it for free.

**Chroma-independent hue rotation.** Rotating hue while holding L and C constant produces "same color, different hue." A single (L, C) grid applied to every hue produces visually consistent ramps.

**A native CSS function.** `oklch()` ships in stable Safari/Chrome/Firefox since 2023. No library, no preprocessor, no compile step.

**What OKLCH doesn't solve.**

- *It's a color space, not a gamut.* OKLCH can describe colors outside sRGB and P3 — and outside *every* renderable display. Whether the color *renders* depends on display + gamut-mapping strategy. An OKLCH ramp at chroma 0.30 may be in-gamut on P3 displays and clipped to a duller shade on sRGB; the clipping may be perceptually inconsistent across the ramp. (External names this; Claude does too. Both right.)
- *Brand fidelity still requires source-color anchoring.* "OKLCH ramp from this hue" doesn't guarantee step 9 matches the brand's signature color. The brand color is a fixed point; the ramp generates *around* it. Fitting the brand to the ramp's perceptually-uniform spacing trades perceptual uniformity for brand fidelity. This is the engagement-level conflict §6 is named for.
- *Per-hue chroma tuning is mandatory for vivid colors.* Pure yellow doesn't exist at chroma 0.20 — it's outside every modern gamut. A fixed-chroma ramp produces clamped, dingy yellows. Practitioners tune chroma per hue (yellow caps at ~0.18, blues go to ~0.25) or accept yellows look less vivid at the same step number.

### P3 wide-gamut

P3 is roughly 25–40% wider than sRGB in the green-red axis (the external pass cites 25%; both within range). Modern hardware ships it: every iPhone since the 7, every iPad Pro, every M-series Mac, modern OLED Android flagships, modern Windows OLEDs. The mid-2026 default: assume P3 on modern phones and tablets, mixed sRGB/P3 on desktops.

**When to ship P3.** Brand-critical surfaces — heroes, accent surfaces, marketing photography color treatment — benefit. The P3 version of a brand red is genuinely more saturated, not just perceptually nudged.

**The CSS path** — two patterns:

```css
/* Gamut-conditional declaration, modern */
.brand-hero { background: oklch(0.6 0.20 25); }
@supports (color: color(display-p3 1 0 0)) {
  .brand-hero { background: oklch(0.6 0.30 25); }
}

/* Or via @media + explicit color() function */
.brand-primary { background-color: rgb(0, 122, 255); /* sRGB fallback */ }
@media (color-gamut: p3) {
  .brand-primary { background-color: color(display-p3 0 0.478 1); }
}
```

The architecture move: ship two primitive layers — sRGB-clamped values and P3-extended values — and emit per-target CSS. Tokens Studio supports this via mode declarations as of mid-2026; Style Dictionary does it via per-platform transforms. Most pipelines don't ship P3 by default; the practitioner opts in. The DTCG Color Module 2025.10 enumerates `display-p3` as one of fourteen valid `colorSpace` values (alongside `srgb`, `srgb-linear`, `oklch`, `oklab`, `rec2020`, `xyz-d65`, and others); the field on a `$type: "color"` token sits inside `$value` next to `components`, `alpha`, and an optional `hex` fallback. The schema makes wide-gamut authoring explicit at the token level. (Source: `_source-text/ext-dtcg-format-module.txt`.)

**Gamut-mapping** (when an OKLCH color is outside the target gamut):

- *Per-channel clamping* — clamp R, G, B independently to [0, 1]. Worst result: hue shift. Browsers used to do this; modern browsers do better.
- *Relative colorimetric* — preserve in-gamut colors, clip the rest. Clean for in-gamut content, harsh at edges.
- *Perceptual* — compress the entire space to fit. Smooth gradients, in-gamut colors lose vibrancy.
- *CSS Color 4 chroma reduction* — keep L and H, reduce C until the color is in gamut. CSS Color 4 §14.2 specifies three sibling algorithms (`Binary Search Gamut Mapping with Local MINDE`, `EdgeSeeker Gamut Mapping`, `Ray Trace Gamut Mapping`) and explicitly delegates the choice to the implementation: *"Implementations may choose any of the three algorithms based on their quality and runtime efficiency tradeoffs, and must use their chosen algorithm wherever CSS mandates that gamut mapping be performed."* All three aim at constant-lightness, constant-hue chroma reduction in OkLCh under a relative colorimetric intent, so in-gamut colors pass through unchanged. The spec also clamps the lightness extrema before chroma reduction runs: L ≥ 1.0 returns destination-space white, L ≤ 0.0 returns destination-space black. The Binary Search with Local MINDE algorithm uses ΔE_OK as its distance metric (1 JND in OkLCh = 0.02) and is implemented in the Coloraide (Python) and color.js (JavaScript) libraries. There is no single normative CSS default; which algorithm a given browser ships is a per-engine, per-version question, tracked through the spec's WPT report at `wpt.fyi/results/css/css-color/`. (Source: `_source-text/ext-css-color-4-gamut-mapping.txt`.)

The practical rule: author in OKLCH, declare your fallback strategy explicitly for brand-critical primitives, test in sRGB and P3 separately, and accept some visual drift on out-of-gamut steps.

### HCT (Material 3)

HCT — Hue, Chroma, Tone — is Google's Material 3 color space, anchored on CAM16 (a more sophisticated color appearance model than CIELAB or Oklab; accounts for surround/adaptation effects).

**HCT's contribution: tone-pinned contrast.** Two colors at the same Tone have the same perceptual lightness regardless of hue. M3 uses this property to *guarantee contrast pairs across the entire palette* by tone difference: `Tone 90` on `Tone 10` always passes WCAG AA, regardless of which hue each is. Tonal palettes (40, 50, 60, 70…) become a contrast grid.

**HCT vs. OKLCH.** Both are perceptually based; HCT is more sophisticated (accounts for surround), OKLCH is simpler/faster and good enough for most authoring. HCT-anchored ramps are just colors — they interop fine with non-Material systems as values. But the *guarantees* (tone-pinned contrast) hold only within the HCT framework. A ramp generated in HCT and exported as hex doesn't preserve the tone-pinned property when the consumer system reasons about it in OKLCH or sRGB.

**Cost.** HCT requires the Material library or a port — `material-color-utilities` is open-source with TS, Swift, Dart ports. OKLCH is native CSS. **For a system that doesn't ship on Android, HCT is a useful *technique* but rarely a worthwhile dependency.** Bridging Web (OKLCH) and Android (HCT) means maintaining dual mathematical models or accepting measurable chromatic shifts at the boundary.

### CSS Color 4/5 surface — currency note (mid-2026)

| Feature | Status | Note |
|---|---|---|
| `oklch()`, `oklab()`, `lch()`, `lab()` | Stable across Safari/Chrome/Firefox 18+ months. | Safe without polyfill. |
| `color-mix(in oklch, …)` | Well-supported across all three engines. | Safe. |
| Relative color syntax (`oklch(from var(--brand) calc(l - 0.1) c h)`) | Safari late 2023, Chrome 2024, Firefox 2024. | Least mature of the four; known parser inconsistencies for nested calc expressions. Verify caniuse.com/css-relative-colors before committing. |
| `color()` with named spaces (`color(display-p3 …)`, `color(rec2020 …)`) | Well-supported. | Safe. |
| `color-scheme: light dark` | Well-supported. | Safe. |
| `forced-colors` media query / `forced-color-adjust` | Well-supported. | Safe. |

Verification: caniuse.com/css-oklab-oklch, caniuse.com/css-relative-colors, MDN's color page. A practitioner who's been away from CSS for two years should re-check relative color syntax specifically before committing the architecture to it.

### Round-trip fidelity — where color silently drifts

The agency reality both passes name: **most token pipelines silently quantise to sRGB hex on export.**

- **Figma → tokens.** Figma Variables (mid-2026) supports OKLCH and P3 internally for color values, but export adapters (Tokens Studio, Figma's own Variables-to-tokens emitter, plugin-based exporters) often quantise to hex during handoff. The wide-gamut vibrancy is irrevocably stripped. Verifying the exported color in OKLCH-aware tooling reveals the drift. Specialised plugins (Color Scales I/O, Atmos) compute natively in OKLCH/P3 and store via DTCG `colorSpace` schema fields, bypassing Figma's internal rendering — the practical workaround for engagements where fidelity matters.
- **Tokens Studio → JSON.** Depends on export configuration. The DTCG JSON spec preserves color expressions if the source declared them as `oklch()` strings; quantisation happens at the platform-output step.
- **Style Dictionary → CSS.** Default color transforms convert to hex. Preserving OKLCH requires the platform configuration to declare a custom transform or use raw value passthrough. Most teams don't, and the runtime ends up with hex even though the source was OKLCH.
- **Style Dictionary → iOS/Android.** Native platforms have no OKLCH equivalent; values convert to the platform's RGB or RGBA color, with the corresponding gamut clamp.

**The practitioner consequence:** declare a platform-by-platform fidelity contract. On web, preserve OKLCH end-to-end and let the runtime do gamut mapping. On iOS/Android, convert at build time, accept the drift, and *test the converted colors against the design source* before shipping. The test is non-negotiable; nominally-equivalent colors after a hex round-trip frequently differ enough to read as a different shade.

| Color space | Primary architectural application | Key advantage | Limitation |
|---|---|---|---|
| **sRGB (hex)** | Legacy web, basic UI, native fallback | Universal hardware/tooling support | Severely limited gamut; perceptual math fails |
| **Display P3** | Modern web, Apple ecosystem, brand-critical surfaces | ~25–40% more vibrancy than sRGB; matches modern displays | Requires CSS fallbacks, gamut-mapping discipline |
| **OKLCH** | CSS ramp authoring, design tokens | Perceptual lightness; uniform gradients; native CSS | Unbounded; describes colors no display can render |
| **HCT** | Android native, Material 3 dynamic color | Tone-pinned contrast guarantees | Computationally heavier; isolated from web standards |

---

## 3. Accessible contrast — WCAG 2 vs. APCA, and the live debate

### What WCAG 2.x measures, and where it fails

WCAG 2.1/2.2's contrast ratio is the relative-luminance ratio `(L1 + 0.05) / (L2 + 0.05)`, with L computed from sRGB R/G/B via a piecewise gamma function. Thresholds: 4.5:1 normal text, 3:1 large text and non-text UI components, 7:1 AAA. The formula assumes a CRT-era sRGB display model; both passes call this out.

**Three documented failure modes** (both passes name the same three):

- *Dark-mode under-prediction.* A 4.5:1 white-on-`#1A1A1A` passes; in practice it reads as harsh, with bloom around glyph edges. The luminance ratio doesn't model the eye's response to bright objects on dark fields ("halation"). Designers compensate by lowering foreground luminance — `#E0E0E0` instead of pure white — but the formula doesn't *demand* it.
- *Small-text trap.* The threshold is binary by font size (the "large text" cutoff at 18pt or 14pt bold). Font weight, stroke contrast, and the actual continuous reading-distance / size relationship are not modelled. A thin-weight 18pt at 4.5:1 is illegible; a heavy-weight 13pt at 4.5:1 is fine. The formula passes both.
- *Yellow-on-white over-prediction.* A vibrant yellow can yield a luminance ratio meeting 3:1 for non-text — perceptual contrast is near zero. The eye's wavelength response peaks around yellow-green; high luminance there doesn't translate to high perceptual contrast.

These aren't edge cases — they show up in audits regularly. The legal standard is what it is; the formula is acknowledged (including by the WAI itself) as a coarse approximation.

### APCA — the perceptual replacement

APCA (Accessible Perceptual Contrast Algorithm) returns an Lc value, not a ratio. It's *asymmetric* — light text on dark and dark text on light yield different Lc because perceptual contrast is direction-dependent. The asymmetry sits inside the equation (different exponents per polarity); the *threshold table* is read by absolute Lc value either way. The 2026 canonical thresholds, sampled from the APCA Readability Criterion's published font-size × weight matrix:

| Lc tier | Intended UI application | Approximate typography minimum |
|---|---|---|
| **Lc 90+** | Critical UI, super-bold text — the highest tier. | 14px @ 500–600 weight; 16px @ 400. |
| **Lc 75–90** | Body-text minimum (analogous to WCAG AA but perceptually grounded). | 18px @ 400 or 14px @ 700. |
| **Lc 60–75** | Large or non-essential text, UI labels. | 24px @ 400, 18px @ 600, 16px @ 700. |
| **Lc 45–60** | Large headings, decorative. | 36px @ 400 or 24px @ 700. |
| **Lc <45 / Lc 30 floor** | Non-text interactive UI components, borders, icons, focus rings. | The Lc 30 floor for non-text UI is practitioner shorthand; APCA's published Non-Text Contrast guideline is still a placeholder as of mid-2026, so the value is supported by the Silver/Gold tiers' "in no case below Lc 30" floor for non-fluent text rather than a dedicated non-text-UI table. |

APCA models the things WCAG 2 misses: dark-mode halation, font-weight contribution, the wavelength response. The result: APCA grades a yellow-on-white pair as failing even though WCAG 2 passes; APCA grades white-on-`#202020` as more demanding than the equivalent ratio in light mode would suggest.

**Adoption as of mid-2026.**

- *Adopted* — Adobe Spectrum's research and design tools (parts of the system), GitHub Primer's contrast linting, parts of IBM Carbon (charts especially), Tailwind v4's contrast utilities (reportedly APCA-aware), several practitioner ramp generators (Atmos, recent Tints.dev versions).
- *Not adopted* — WCAG 2.2 (the legal/procurement standard); EN 301 549 (EU); Section 508 (US Federal). These mandate WCAG 2.x. APCA is *additive*, not substitutive.
- *WCAG 3 ("Silver") status* — the W3C has not finalised. APCA was the proposed contrast model in 2022 working drafts; the spec has been a perpetual working draft through mid-2026, currently operating via a draft Bronze/Silver/Gold tiering system. The published thresholds live at the APCA Readability Criterion (`readtech.org/ARC/`), with the canonical font-size × weight matrix dated 22 May 2022 and tier rules covering Bronze (fluent body text only, Lc 75 minimum / Lc 90 preferred), Silver (fluent + sub-fluent + non-fluent, look-up-table based, must satisfy at least one exchange rule), and Gold (all text, must satisfy at least two exchange rules; body-text rule that any Lc < 75 must be increased by ≥ 15). The Bronze tier is the Lc-75-as-body-text-floor we cite when sketching APCA in workshops; Silver and Gold extend coverage but require tooling. The verification path: `readtech.org/ARC/` for tier rules, the Myndex/SAPC-APCA repo for the formula and version stamp, and `w3.org/TR/wcag-3.0/` for WCAG 3's eventual disposition. (Source: `_source-text/ext-apca-thresholds.txt`.)

**The practice's stance.** Ship WCAG 2.x as the procurement floor — it's what audits and accessibility certifications test against. Use APCA in the *design-tool linting and ramp-generation layer* as the quality bar above the floor. A ramp passing WCAG 2 at the rated steps but failing APCA is a ramp that will *look wrong even when it passes audit*. Conversely, a ramp tuned to APCA almost always passes WCAG 2 at the same steps. WCAG 2 is the law; APCA is the standard the design has to meet for the law to actually mean something. (32 §2.3 names this as the "WCAG-passes-but-fails-real-users" pattern in the accessibility audit's lane methodology — automated tools pass the DOM structure while the rendered component fails real users; the audit's evidence is real-user testing or the auditor's perceptual-contrast read.)

### Anchoring contrast on a generated ramp

The 2024–2026 architectural move: bake contrast into the ramp's structure so consumers don't compute it.

**Radix's contrast pairs.** Step 9 (the "solid" step) is contrast-paired with white text — `white on step-9 = AA at 4.5:1` for every hue. Step 11 is paired with the surface for low-contrast text; step 12 for high-contrast text. These are guarantees, hue by hue. Step 9 isn't the same OKLCH lightness for every hue (yellow's step 9 is darker than blue's), because contrast against white isn't constant across hues.

**Tailwind v4's contrast-aware shades.** Each numeric step has a documented contrast rating against the system surface. Authors who pick `bg-blue-600 text-white` get a known contrast guarantee.

**Adobe Leonardo's contrast-anchored generation.** The user declares the target contrast curve (AA on white at step 6, AAA at step 9), Leonardo generates the ramp's colors to *hit* the curve. Brand color is a constraint, not the source of truth — if the brand color doesn't fit, Leonardo shifts it.

**The shared idea: the ramp's step is a contrast role, not a lightness coordinate.** Consumers picking `color/text/primary` (which resolves to step 11 or 12 of the appropriate hue) get the contrast guarantee for free. The discipline this implies: a system can declare a rule like *"a token-step differential of ≥ 50 (e.g., step 60 minus step 10) guarantees APCA Lc 75 across all hues"* — and the ramp generator enforces it. **The ramp has to be built contrast-aware; you can't bolt the property on.** If the primitive layer is naive numeric steps without per-hue contrast tuning, the semantic→primitive aliasing chain doesn't produce these guarantees.

### The disabled-state contrast exemption — the practice's harder line

WCAG 2.2 SC 1.4.3 and 1.4.11 explicitly exempt disabled controls from contrast requirements. The exemption exists because disabled state is conventionally signaled by lower contrast, and demanding WCAG-compliant contrast on a disabled control would erase the visual difference between disabled and enabled.

**The trap.** Leaning on the exemption produces inaccessible UIs that pass audit. A user can't tell whether a disabled control is "disabled" or "broken"; the AT user can't tell why the control is unreachable.

**The practice's position** (the external pass's stronger framing, which the practice adopts): **eliminate naive disabled controls wherever possible.** Keep the control fully rendered and operable, use real-time inline validation or `aria-disabled="true"` paired with a visible, contextual error state explaining the blockage. This aligns with the Button brief's focusable-inactive position (components/button.md §4) — the "relevant but blocked" pattern is the better default.

The system's color tokens should support both options: a `color/action/disabled` that intentionally fails contrast (for legacy patterns the engagement may have to ship) and a `color/action/inactive` that doesn't (for the better pattern). **Default to the latter.** Document the former as the legacy fallback for codebases that can't yet adopt aria-disabled with reasoning.

### Forced-colors / Windows High Contrast Mode — the transparent-border trick

Forced-colors mode is a user accessibility setting (Windows, supported across browsers) where the OS replaces author colors with system-defined keywords: `Canvas`, `CanvasText`, `LinkText`, `ButtonText`, `ButtonFace`, `Highlight`, `HighlightText`, `GrayText`, plus a few more. The user picks a high-contrast theme; their entire system uses the chosen palette.

**What forced-colors does to your tokens.** Most of them. The browser swaps `background-color`, `color`, `border-color`, etc. with system keywords for any element where it can determine intent. Only specific properties (background-images, gradients, shadows) and elements opted in via `forced-color-adjust: none` retain author colors.

**What the system can still control.**

- *Structure.* The token `color/border/default` is overridden, but the *fact* of a border is preserved. UI depending on borders (form fields, table dividers) survives. UI depending on subtle background-color differences (a divider implemented as a 1px row with a faint background) doesn't.
- *Focus indicators.* `outline` and box-shadow-based focus rings get system-color treatment. Designs relying on color-only focus differentiation fail; outline-based focus rings work.
- ***The transparent-border trick*** (the external pass surfaces this; worth naming as the technique). Components communicating structure via `box-shadow` or opaque background-color overlays vanish in WHCM — shadows aren't redrawn, the divs collapse against the system canvas. The fix is to declare a **transparent border** on those components (`border: 1px solid transparent`). In standard mode the border is invisible; in forced-colors mode the OS forcibly illuminates *all* borders with a system color, so the structure re-emerges. Apply this to cards, modals, dropdowns, and any component whose visual structure depends on a non-border signal.
- *forced-color-adjust: none.* Use *very* sparingly — typically logos and brand-critical hero imagery only. Setting it on UI controls is an accessibility regression dressed up as control.

**The design discipline.** Assume the entire palette will be replaced. Ensure structure, focus, and state are communicated by *non-color* signals (borders, text, icons, focus outline, transparent-border-as-structure). The token system itself doesn't help in this mode; the *components* have to be authored to survive without their colors.

---

## 4. Theming architecture

### Light / dark / brand / density as orthogonal axes

In theory orthogonal: any combination of (light|dark) × (brand-A|brand-B|brand-C) × (compact|comfortable|spacious) is valid. In practice compounded — components ship validated values for each combination, and the matrix grows fast. Two brands × two color schemes × two densities = 8 theme combinations; every component-tier color token has 8 validated values.

**The architectural rule** (both passes converge): treat the axes as *strictly orthogonal* at the token level. Dark-mode logic is abstracted from brand logic; brand logic is abstracted from density logic. A `color/surface/raised` semantic token resolves through a cascading chain — never through a monolithic per-combination file.

**DTCG modes** are the architectural answer:

```json
"$modes": ["color-scheme", "brand", "density"],
"color/surface/raised": {
  "$value": {
    "color-scheme:light brand:a density:comfortable": "{neutral.50}",
    "color-scheme:dark  brand:a density:comfortable": "{neutral.900}"
    /* … */
  }
}
```

Tokens Studio and Figma Variables both support multi-dimensional modes as of mid-2026; Style Dictionary's mode support is via separate config files per mode, less ergonomic but workable. The build pipeline emits per-target outputs (a `.dark.css` and `.light.css`, or a single CSS file with class-based selectors per mode).

**The cost:** declaring the matrix is the easy part; *validating* it is the hard part. Every combination needs visual review. Most systems ship one combination as the validated default and the others as derived/inherited, with known drift on edge cases. This is the layer 24-tokens-at-scale's multi-brand validation matrix lives at; the color-specific extension is that validation has to include APCA-on-the-actual-rendered-pair, not just primitive-step-equality.

### Dark-mode surface elevation — the lift pattern

In light mode, elevation is signaled by a drop shadow against a white surface. In dark mode that pattern fails — a black shadow on a black surface is invisible. **The convergent answer: elevation is signaled by a *lighter* surface, not a shadow.**

Material 3's lift pattern: `surface-1` through `surface-5`, each at a progressively higher overlay over the base surface (M3's documented values: 5%, 8%, 11%, 12%, 14% white overlay over the base dark surface, plus tint shifts toward `surfaceTint`).

**The semantic implication.** A `color/surface/raised` token in dark mode resolves to a lighter-by-some-amount surface, not just a different primitive. Components shipping "elevation tokens" (a card with `elevation-2`) read the surface from the elevation level, not the base surface. The practice's preferred encoding: a semantic alias for elevation (`surface-raised`, `surface-overlay`) that maps to *shadow tokens* in light mode and to a *lighter background primitive* in dark mode — preserving the component's API contract without conditional logic in the component layer.

**The shadow-fade-becomes-surface-lighten swap.** In light mode `shadow/large` is a soft drop shadow. In dark mode the equivalent token is *the same shadow plus a surface lift*, or — if the system commits — the shadow disappears entirely and the surface lift carries the elevation. Both patterns are in the field; M3 keeps a faint shadow plus surface lift; some systems (Vercel's, Stripe's) use surface-only.

**The implication for tokens.** Composite shadow tokens have to be mode-aware (the dark-mode value may be null or different). Surface tokens have to be elevation-aware. Component authors ask not just "what's my surface" but "what's my surface at this elevation in this mode." Token volume in dark-mode-aware systems is meaningfully larger.

### Shadow tokens — shape, colour, and the elevation lever

The lift pattern settles the *dark-mode* half; the shadow ramp itself has its own settled shape, and a ten-system survey (M3, Carbon, Atlassian, Polaris, Primer, Fluent, Spectrum, Tailwind, Radix, Apple) converges more than the noise suggests.

**Six steps, two layers.** The convergent step count is **six** (M3 levels 0–5, Radix 1–6, Fluent 2/4/8/16/28/64, Tailwind sm–2xl) plus a separate inset. Each step is best built from **two layers — a tight directional "key" shadow that defines the edge and a soft diffuse "ambient" shadow that implies distance** (Fluent names this explicitly; Tailwind's defaults and most brand systems ship it). One layer reads flat at high elevation; the 3–6-layer "smooth shadow" technique (Radix, Comeau's shadow-palette method) is higher fidelity but heavier than tokens that must round-trip to Figma usually want — reserve it for marketing-expressive work. Across every system the offsets behave the same: **`offsetX` is 0** (light directly above), `offsetY` and blur grow with elevation, and **spread goes negative and grows** to keep large shadows from ballooning.

**Tint, don't reach for pure black.** The lazy default is `rgba(0,0,0,…)`; the better systems tint the shadow toward the surface or brand hue — Polaris ships `rgba(26,26,26)` not `#000`, Radix mixes a theme-hued `gray-a*`, Fluent offers brand-tinted shadow variants, and the field's generation advice (Comeau) is "match the hue, drop the lightness." A pure-black shadow over a tinted surface reads as a dead grey smudge; a near-black tinted toward the palette reads as light. **The practice default: a tinted near-black, with pure black as the explicit opt-out**, and the tint hue exposed as an expressive lever for brand-hued marketing shadows.

**Two axes, one semantic token.** Elevation is *two* token families — a surface ladder and a shadow ladder — and the cleanest architecture (Atlassian's) keeps them explicit (`elevation.surface.*` and `elevation.shadow.*`) and **pairs them through a single semantic `elevation.N`** that resolves per mode: in light the shadow does the work, in dark the surface lift does (per the lift pattern above). Components reference the semantic level (`card`, `dropdown`, `dialog`), never the raw step — so the light/dark swap lives in the token layer, not in component logic. (This is the same primitive→semantic discipline §The semantic→primitive aliasing chain describes, applied across the surface/shadow boundary.)

**The generation lever.** When a system generates its shadows rather than hand-drawing them, the one knob worth exposing is **softness — the blur-to-offset ratio** — which moves the whole ramp from crisp/product (Carbon, Fluent) to soft/marketing (Stripe, Comeau-style). Offsets grow geometrically with the step, blur is `offset × softness`, spread is negative and growing, opacity drifts up at the top, and the key/ambient pair is derived from the same step index. Softness plus the tint hue are the two dials that make one engine produce a Carbon-crisp neutral ramp or a soft brand-hued one. (Sourced from the shadow/elevation research run, `_research/_inbound/2026-06-28-shadow-elevation-tokens`.)

### The semantic→primitive aliasing chain — and where it breaks

The chain: consumer reads `color/surface/raised/default` → semantic resolves (theme-mode-aware) → `color/neutral/0` (light) or `color/neutral/100` + lift (dark) → primitive value.

**Where the chain breaks.**

- *Composite token round-trip.* DTCG composite tokens (typography, shadow) can include color sub-properties. Most tools as of mid-2026 don't faithfully preserve property-level aliasing inside composites on round-trip — the `fontColor` sub-property of a typography composite resolves to a value at export time, losing the alias. (See 22's composite-fidelity-gap discussion.) Mitigation: carry composites as source-of-truth, flatten on export, accept the round-trip loss.
- *Brand-mode primitive gaps.* If the system has multiple brands and brand B's primitive ramp lacks a role brand A's has (no "step 12 neutral", no "warning amber"), the semantic falls back to generic — which may not contrast on brand B's surface. The fix is upstream: validate every brand's primitive tier covers every role the semantic tier needs.
- *Density adds a dimension.* Component-tier color tokens varying by density (a denser layout's border color is darker for legibility) double the validation matrix.

### Theme switching mechanics — and the FOUC/theme-flash

The 2026 baseline:

- **CSS custom properties on `:root` or `[data-theme="…"]`** — universal pattern. Semantic tokens become custom property declarations; primitive tokens scope to the theme.
- **`prefers-color-scheme` media query** for system-preference detection.
- **`color-scheme` property** on `:root` — **architecturally crucial** (the external pass is sharp on this). Declares which schemes the page supports; the browser uses this to render form controls, scrollbars, and other UA-styled elements appropriately. Without it, dark-mode pages get light scrollbars and the browser UI clashes with the system tokens.
- **Runtime override** via class or data-attribute on `<html>` — `data-theme="dark"` or `class="dark"`; the theme cascades from `:root`.

**The FOUC / theme-flash problem.** A SSR'd page renders with the default theme markup, the JS hydrates, reads stored preference, swaps the theme. The user sees a flash of the wrong mode. Both passes converge on the patterns:

- *Server-rendered theme decision* — read cookie/session on the server, set `data-theme` on the server-rendered HTML. Eliminates the flash entirely. Requires server-side state.
- *Inline blocking script in `<head>`* — small synchronous script reads `localStorage`/cookie and sets `data-theme` before body renders. Standard, works without server state. Cost: a render-blocking script, ~1ms but blocking. **The default for SPA-shaped agency engagements.**
- *`color-scheme: light dark` + `prefers-color-scheme`* — for systems where system preference is the only source. Trivially flash-free; loses user control.

### Multi-brand at the color layer — the contrast-failure trap

The T-Mobile/Metro and Ford/Lincoln pattern: single semantic surface, swappable primitive tier. The semantic `color/action/primary` resolves to brand A's pink or brand B's purple depending on the active brand. Implementation: scoped CSS custom properties (`[data-brand="metro"] :root { … }`), or runtime CSS-in-JS theme injection.

**What breaks.** Brand B's primary doesn't pass contrast on brand A's neutrals. The semantic has a contract ("AA on the default surface"); the contract holds only if the *primitive ramp is contrast-aligned to the same step grid* across brands. If brand B's primary is OKLCH lightness 0.65 and brand A's is 0.55, white text on brand B's primary may fail.

**The two mitigations.** Both passes name the same techniques:

- **Contrast-tier-named-step rule.** Semantic tokens reference *contrast-tier names*, not numeric steps. Define the role as "step where Lc 60 contrast on light surface is guaranteed" (not "step 9 of the brand ramp"). Force ramp authors across brands to align contrast at the same role. This is the discipline Radix encodes in its 12-step grid; multi-brand systems encode it themselves.
- ***Forced-foreground-color tokenisation.*** The external pass surfaces this as the load-bearing technique: an `on-primary` semantic token (controlling text color *inside* the button) is mathematically computed to flip between black and white depending on the luminance of the swapped brand primitive. This is the cleanest mechanism for keeping `color/action/primary` and `color/action/primary/foreground` *both* compliant as the underlying primitive swaps. The practice adopts it as the default for multi-brand engagements; the contrast-tier rule is the primitive-side discipline, the `on-X` token is the semantic-side discipline, and they compose.

### Density at the color layer

Compact density compresses spatial structure; the color tokens signaling structure (borders, dividers, focus rings) have to compensate by being darker/more contrasting. The pattern: density-aware border tokens (`color/border/default` is one step darker in compact density), or component-level density tokens with their own values. **Most systems don't do this and ship density-aware *spacing* tokens with mode-naive *color* tokens; the result is compact layouts where dividers visually disappear.** This is a real failure mode in data-heavy admin UIs and is worth flagging in any engagement that ships a compact density.

---

## 5. Palette generation — tools and methods

### Contrast-anchored ramps (Adobe Leonardo)

The user declares a target contrast curve — "step 6 = AA on white (4.5:1), step 9 = AAA on white (7:1)". The generator produces colors hitting the curve. The brand color is a constraint (the ramp passes through it), not the source of truth.

**Strengths.** Contrast guarantees are absolute. Every step does what it says. **Heavily used in high-compliance environments** (government, healthcare) where guaranteed-by-construction accessibility is a procurement requirement.

**Trade-offs.** Brand fidelity is bounded by the contrast curve — if the brand color falls short of "step 6 AA," Leonardo shifts the brand color to the nearest passing value. Desirable for accessibility-first systems, unwelcome for brand-led ones. UI is less intuitive for rapid visual iteration than perceptually-uniform tooling.

**The pragmatic role for agency work:** use Leonardo to *validate* a hand-tuned ramp against a contrast curve, not to *generate* the ramp from scratch. Most engagements with a strong brand color land here.

### Perceptually-uniform OKLCH ramps (Atmos, Tints.dev)

Pattern: pick a hue, fix chroma at e.g. 0.18, set lightness at fixed steps (0.10, 0.18, 0.30, 0.42, 0.55, 0.65, 0.75, 0.85, 0.92, 0.96, 0.98). Each step's perceptual jump is uniform. Generate all hues from the same (L, C) grid.

**Strengths.** Visually consistent ramps; trivial to implement; no library required. Dark-mode inversion is mathematically clean — step N in dark mode is the perceptual-mirror of step (max−N) in light mode, so the inversion produces a credible result without manual tuning. P3-aware tools (Atmos) extend the approach to the wide gamut.

**Trade-offs.** Per-hue chroma tuning is mandatory for vivid colors (yellow at chroma 0.18 looks dingy, needs lower; greens and blues go higher without clamping). Contrast is *not* guaranteed at fixed steps — step 9 of one hue may pass AA on white, step 9 of another may fail. Strict mathematical focus can yield aesthetically sterile palettes that lack the subtle hue-shifts of natural lighting (yellow shifting toward orange as it darkens).

This is the Tailwind v4 pattern (Tailwind v4's default palette is OKLCH-based and per-hue chroma-tuned), and the pattern most practitioner ramp generators emit.

### Curated and hand-tuned ramps (Radix Colors, Open Color, Tailwind v4)

Each step has a named role; the color is hand-tuned to fit. Radix in particular is a "designed" system — every step is the result of deliberate authoring, not a generated curve.

**Strengths.** Production-quality out of the box. Contrast guarantees baked in. Light/dark/alpha siblings shipped. Free for open-source palettes. The subtle hue-shifting (mimicking natural lighting / shadow) that pure OKLCH math doesn't produce is in the curation.

**Trade-offs.** Role definitions are opinionated and reflect Radix's product-UI assumptions. Brand-driven systems wanting conventions outside the model (a step 13 for marketing surfaces, a step 0 for special "off-app" backgrounds) extend manually. Over-constrains unique brand requirements; difficult to heavily customise without breaking the palette's intent.

**When right for an agency engagement:** when the brand is willing to adopt the role-based grid (most are once they see the contrast guarantees); when the team needs a fast, stable starting point without committing to a generation toolchain. Radix as the primitive layer with custom semantic aliases on top is a productive default for brand-light product systems.

### Material 3 dynamic color (HCT-based)

Wallpaper-derived scheme: extract a "source color" from the user's wallpaper → expand to tonal palettes via HCT → map to M3 color roles (`primary`, `onPrimary`, `surface`, etc.). The user's phone wallpaper drives the app's color scheme.

**For systems that don't ship on Android:** the *technique* generalises. The Material Theme Builder Figma plugin produces tonal palettes from a source color. The HCT-anchored tonal-palette method is a legitimate ramp-generation approach regardless of whether the output ships on Android.

**Cost for non-Material systems.** Bringing in Material's color utilities (or porting them) is overhead. Most non-Material systems use OKLCH instead and accept a slightly less sophisticated appearance model. Web translation from HCT is poor; if the same engagement ships both web and Android, parallel mathematical models are unavoidable.

### Brand-anchored vs. system-anchored ramps — the alignment problem

**Brand-anchored.** Brand color is fixed at a known step (typically 9, the "solid" step). The ramp is generated to fit around it. The system's identity is rooted in the brand's exact rendering.

**System-anchored.** The ramp is generated to system rules (contrast targets, perceptual uniformity); the brand color is the closest match within the rules. Identity is rooted in consistent contrast and perceptual behaviour.

**The contrast-step-vs-brand-step alignment problem.** If brand sits at step 9 and step 9 must be AA-paired with white, the brand color has to pass that test. If it doesn't (a brand yellow on white fails AA at any reasonable chroma), the system has three choices:

- **Move brand to a different step** (yellow at step 11, with light gray text on top) — usually unacceptable to the brand team.
- **Use a non-brand color for "primary action"** — carve out a separate "action" hue. Common; the brand color shows up in headers, accents, illustrations.
- **Restrict brand-on-light usage** to large text and non-essential UI — works for brands willing to commit.

**The agency role.** Surface this in Foundations — *before* the component library is in flight. Discovering brand-on-its-own-system contrast failures during component review is too late. The fix is architectural (separate "Brand Token" from "System Interaction Token"), not cosmetic. Both passes are emphatic this is the most under-anticipated decision in agency-led engagements.

### Tooling depth (mid-2026) — what each is good at, what none is

| Tool | Strength | Weakness |
|---|---|---|
| **Adobe Leonardo** | Contrast-anchored generation; gold standard for guaranteed-contrast outputs. Free, web-based. | Steep learning curve; less intuitive for rapid visual iteration; weak on perceptual uniformity. |
| **Atmos** | OKLCH manipulation; visual curves; P3 support; better mode/dark support than Tints.dev. Paid. | Strict math can yield sterile palettes lacking natural hue-shift. |
| **Tints.dev** | OKLCH ramp generator, free, fast, export-ready Tailwind/JSON output. | Weak on multi-mode export and contrast validation. |
| **Material Theme Builder** | HCT-native, perfect dynamic-wallpaper extraction. Free, Figma plugin. | Tied to Material role mapping; poor web (OKLCH) translation. |
| **Radix Colors** | Pre-curated, copy-paste, contrast pairs guaranteed. Free. | No customisation — that's the point; over-constrains unique brand work. |
| **Tailwind v4 generator** | OKLCH-based default palette is excellent; custom palette generation through configuration. Free, code-driven. | Tailwind opinion baked in; awkward for non-Tailwind consumers. |
| **Tokens Studio (Figma plugin)** | OKLCH, color-mix, multi-mode authoring/sync. Paid. | Authoring tool, not a generator. |

**What none of them does well** (the practice-relevant gaps):

- *Bridging contrast-anchored and perceptually-uniform.* No mainstream tool takes a brand color and produces both a contrast-anchored *and* a perceptually-uniform ramp aligning at the same numeric step. Practitioners bridge by hand — author in Leonardo for contrast pairs, then visually tune chroma per hue for perceptual consistency. The integration is manual and the source of truth is ambiguous.
- *Forced-colors mapping.* No tool helps the system declare what each token should be in forced-colors mode (most resolving to system keywords; a few brand-critical ones needing `forced-color-adjust: none`). Hand-rolled in runtime CSS.
- *Cross-platform fidelity testing.* No tool renders the same token on web (sRGB / P3 / OKLCH), iOS, and Android side-by-side and reports the perceptual delta. Practitioners sample manually.

---

## 6. Brand color vs. UI color — the unity/cohesion tension

### The Perez-Cruz framing, pushed deeper

*Unity* — strict palette, every element drawn from one ramp. Risks: editorial flatness; brand expression suppressed because the ramp doesn't have the chroma range.

*Cohesion* — related-but-distinct palettes, a display palette and a UI palette sharing a hue at a shared step. Risks: drift over time; the relationship becomes implicit; eventually it's two palettes pretending to be related.

**The middle ground: shared primitives, separate semantic roles.** Display semantics (`color/editorial/heading`, `color/editorial/lede`) reference brand-display primitives — wider chroma, more saturated. UI semantics (`color/text/primary`, `color/action/primary`) reference UI-tuned ramps — narrower chroma, contrast-anchored. Both share a brand hue at step 9 (so the system *recognisably* belongs to the brand). The semantic layer enforces the discipline; consumers can't accidentally use a display color in a UI surface. **This is the Claude pass's architecture and the practice's default for most engagements** — the primitive set stays singular, the semantic layer doubles to express the two-mode intent.

The external pass takes a stronger position: ship **parallel primitive packages** (a "brand display" package and a "product UI" package), share the *structural chassis* (component architecture, DTCG definitions, naming taxonomy), and let the engagement consume one or both. **Use this when the engagement has genuinely two-brand-scale separation between marketing and product** — separate teams, separate roadmaps, separate validation cycles. In a typical single-product agency engagement, the parallel-primitives approach over-engineers; in a multi-property engagement (e.g., a holding-company portfolio with separate marketing and product properties), it's the right architectural call.

### Status / semantic carve-outs — "system green" stability

Status colors — success, warning, error, info — are **architectural exceptions to brand expression.** Both passes are emphatic. The reasons:

- *Cultural and convention-bound meaning.* Red for error, green for success, yellow for warning. Disrupting the convention costs comprehension. A brand whose primary is red faces a fundamental conflict.
- *The "system green" stability rule.* `color/status/success` is perceptually similar across themes, brands, and densities — it's a *signal*, not a brand expression. Stripe's success-green, Carbon's success-green, GitHub's success-green look similar because the meaning is shared.
- *Contrast obligations are non-negotiable.* Status colors carry information; failing contrast on a status icon means failing the user. The brand can't override.

**The red-can't-mean-brand problem.** When a brand's primary is red (Netflix, Target, Vodafone — both passes name examples), the system needs:

- a separate "destructive" red visually distinguishable from brand-red, *or*
- the brand has to accept that destructive actions look like brand actions (rarely acceptable).

**The convergent answer:** carve out a non-brand "primary action" color for standard interactive components (often a neutral deep blue, or a heavily darkened shade of the brand color) to preserve the semantic integrity of error states. The brand color appears in headers, accents, illustrations, marketing surfaces — the places where its identity carries without competing with destructive-action signalling. This is a place where the DS POV needs to assert itself: status colors are infrastructure, not brand assets, and the system needs the freedom to ship a working destructive color even when the brand's red sits in adjacent territory.

### Editorial / marketing color vs. product UI color — when to ship two palettes

Two palettes when:
- Brand's signature color is too saturated or vivid to use as UI primary.
- The system serves both marketing and product surfaces.
- The engagement scope explicitly covers both.

One palette when:
- The system is product-only or marketing-only.
- The brand's hue is forgiving enough to do both jobs (true for many fintech / SaaS brands with mid-saturation primaries).

The architectural pattern (per §6 above): shared primitives with separate semantic roles for most cases; parallel primitive packages with shared chassis for genuinely two-property work.

### The brand-against-its-own-system trap

Concrete: brand color is signature yellow; primary action button needs WCAG AA on white; yellow doesn't pass at any reasonable chroma. The traps:

- *Shifting brand* — move yellow toward darker yellow / amber to pass contrast. Brand says no.
- *Brand as accent, not action* — yellow is used for accents (highlights, key data, status), not action surfaces. A defensible pattern, but it changes how the brand is *seen* — brand becomes an emphasis, not a presence.
- *Brand-on-dark-only* — brand-yellow appears only on dark surfaces (where contrast against white text passes); light theme uses a different primary. Unbalanced; the brand looks weaker in light mode.
- *Carving out non-brand "primary action"* — use brand's secondary color (often blue or charcoal) for action; keep brand-yellow for headers and accents. Costs brand presence on the most-visible UI element.

The agency's job: surface the trap in Foundations, with explicit examples of the brand color tested against the system's surface and text colors at WCAG and APCA. Ship the workshop output as a written architectural decision, not a verbal nod. The fix is architectural; discovering it during component review is too late. (See 02-design-foundations for the foundation-phase framing of this kind of decision.)

---

## 7. Data-visualisation palettes

### Categorical / sequential / diverging — distinct problems

Each requires a different palette structure. Both passes converge on the IBM Carbon Charts framing as the practitioner reference.

| Palette type | Core purpose | Architectural rules |
|---|---|---|
| **Categorical (qualitative)** | Distinguish discrete, *unrelated* data categories (market share by country). | Maximise contrast between adjacent colors. Sequence intentionally to avoid visual grouping. 8–12 distinguishable hues; viewers can't reliably distinguish more without heavy cognitive load. |
| **Sequential** | Represent numeric ranges or density (heatmaps, choropleths). | Monochromatic or analogous. Light mode: darker = higher values. Dark mode: lighter = higher values. |
| **Diverging** | Two-hue ramp meeting at neutral midpoint, used for values diverging from a central norm (profit/loss, anomaly vs. baseline). | Two contrasting hues converging on a neutral, low-chroma midpoint. Red/blue is the convention; red/green fails for color-blind users; orange/teal is the typical CB-safe alternative. |

**A UI palette serves none of them.** Hue selection, lightness curves, and chroma values are tuned for product UI — contrast roles, not data encoding. Trying to derive a data-vis palette from the UI palette's hues is a recurring failure mode.

### Color-blind safety

Forms of color-vision deficiency to plan for:

- *Deuteranomaly* — green-weakness; ~5% of males. Reds and greens become harder to distinguish.
- *Protanomaly* — red-weakness; ~1%. Similar effect.
- *Tritanomaly* — blue-weakness; <1%. Yellows and blues become harder.
- *Achromatopsia* — full color-blindness; rare. Grayscale-equivalence is the test.

Established palettes:

- **Viridis** (matplotlib's default sequential) — perceptually uniform, color-blind safe, grayscale-safe.
- **IBM Carbon Charts** — curated 14-color categorical palette tested across deuteranomaly/protanomaly/tritanomaly.
- **Tableau color-blind safe** — practitioner default since 2016; 10-color categorical.
- **ColorBrewer** — Cynthia Brewer's research-grade palettes for cartography; sequential, diverging, and categorical sets, all CB-tested.

**The discipline that survives the test: color is never the sole carrier.** Even with a CB-safe palette, charts must encode the data redundantly (line shape, marker shape, label, pattern, value annotation). The Chart-component gap from 09 is precisely this — most charts default to color-only and fail color-blind users.

### Perceptual ordering — why OKLCH-derived sequential ramps win

An HSL-derived sequential ramp has uneven perceptual steps (constant H, varying L and S — but L doesn't track perception in HSL). Readers misread the ordering: values intended to read as "third-largest" read as "second-largest" because the perceptual jump from step 6 to step 7 is larger than from step 7 to step 8. **A sudden jump in perceived lightness reads as a data spike that doesn't exist in the data.**

An OKLCH-derived ramp has even perceptual steps. Readers correctly order values. The matplotlib team's adoption of Viridis was driven by exactly this evidence; multiple data-vis-literature studies confirm.

**The implication:** data-vis sequential ramps in the system should be OKLCH-derived. Re-using the UI ramp (which is contrast-anchored, not perceptually-uniform) is a comprehension regression — the chart will literally lie to the reader.

### Where data-vis lives in the token architecture — the isolation rule

**Data-visualisation tokens must never alias UI tokens.** Both passes are emphatic. If a designer alters `color/brand/primary` to accommodate a marketing shift, it could unknowingly destroy the sequential contrast or categorical differentiation of a critical dashboard chart. Data-viz colors live in a completely isolated namespace:

```
color/viz/categorical/1..12
color/viz/sequential/blue/100..900
color/viz/sequential/heat/100..900
color/viz/diverging/coolwarm/100..900
```

These primitives are not derived from the UI palette. They're independently tuned for the data-vis problem. The system's UI semantics (text, surface, action, status) don't reference the viz primitives, and vice versa.

**Where UI semantics do show up in charts:** annotations, axis labels, gridlines, the status-colored callout for a critical threshold. These use UI tokens. Data series themselves use viz primitives.

**Token volume.** A system shipping data-vis as a first-class concern adds 50–100 viz primitives on top of UI ones. Most agency engagements treat data-vis as out-of-scope or ship a minimal categorical-only palette; full data-vis token coverage is a distinct sub-project, often charged separately.

### The 12-color limit, table-fallback contract

Beyond ~8–12 categorical hues, viewers can't reliably distinguish; the encoding fails. Alternatives:

- *Categorical-as-pattern.* Hue + texture/pattern (stripes, dots, dashes); expands distinguishability beyond pure hue. Works in print; less well in interactive UI where patterns can shimmer.
- *Hierarchical grouping.* Sub-group similar series under a parent color (5 series in a "blue family," distinguishable within the family but visually grouped against other families).
- ***Table-fallback contract.*** Any chart exceeding ~8 series must have a table view. The table is the accessible primary; the chart is the visual layer. This is the convergent answer in accessible data-vis practice — Carbon Charts ships this, Spectrum's data-vis docs require it, the practice should default to it for any data-heavy engagement.

---

## 8. Native platform translation

The 2026 truth both passes name: **a design system is not a CSS library.** Color tokens have to translate natively into iOS and Android — and the translation is *integration into opinionated native rendering engines*, not a 1:1 hex mapping.

### iOS UIKit / SwiftUI semantic colors

Apple's system palette ships with built-in dynamic-color behaviour: each system color resolves to (light, dark) × (regular, high-contrast) × (regular, larger) automatically. The named tokens:

- *Background* — `.systemBackground`, `.secondarySystemBackground`, `.tertiarySystemBackground` (and grouped variants).
- *Foreground* — `.label`, `.secondaryLabel`, `.tertiaryLabel`, `.quaternaryLabel`. Plus `.placeholderText`, `.linkColor`.
- *Separators* — `.separator`, `.opaqueSeparator`.
- *Tints / accents* — `.systemBlue`, `.systemRed`, etc.
- *Standard fills* — `.systemFill`, `.secondarySystemFill`, `.tertiarySystemFill`, `.quaternarySystemFill`.

**A third-party DS on iOS — two patterns.**

- *Map.* DS tokens *replace* `.label` only on the third-party app's surfaces; system colors are still used for system-rendered UI (alerts, action sheets). Loses brand fidelity in system-controlled regions.
- *Replace.* The DS ships its own full palette and ignores the system palette except inheriting accessibility behaviour at primitive level. Loses free dark-mode/high-contrast handling unless the DS palette is itself dynamic.

**The architectural rule** (the external pass surfaces this as the load-bearing technique): tokens are initialized as **dynamic `Color` objects** that utilise `traitCollection` or environment values to resolve the light/dark variant *at the OS level*. Don't pass a raw hex code to the runtime. Generate a native Swift Asset Catalog or `AppColor.surface` enum that maps directly to the SwiftUI environment, avoiding fragile manual state tracking. **A third-party DS that hardcodes hex values into iOS gives up dark-mode/HC handling for free; the integration discipline is to map tokens to `Color` objects with the OS-resolution behaviour preserved.**

Most agency engagements: replace the primary palette (text, surface, action, brand status) with DS tokens; *retain* system colors for interactions (system blue for default-tint where the brand doesn't override) and for OS-level UI. The trade-off is brand fidelity vs. native feel; agency engagements typically err toward brand.

### Android — Material 3 dynamic color, and the opt-out reality

Material 3's dynamic color: the user's wallpaper is the source. The OS extracts a "source color," generates tonal palettes via HCT, and maps to M3 color roles. The app's color theme adapts to the user's wallpaper.

Color roles: `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `secondary`, `onSecondary`, `tertiary`, `onTertiary`, `error`, `onError`, `errorContainer`, `surface`, `onSurface`, `surfaceVariant`, `onSurfaceVariant`, `outline`. Each accessed via `MaterialTheme.colorScheme.<role>` in Compose.

**The architectural rule.** Google's ecosystem is fiercely opinionated via the `MaterialTheme.colorScheme` API. **A third-party DS that bypasses this by hardcoding custom variables breaks native components** — Switches, Cards, AppBars, ripple effects, text-selection highlights, disabled states all default to fallback colors and the UI fundamentally breaks. The DS must map its semantic tokens *into the M3 slots* (the engagement's `color/action/primary` becomes `MaterialTheme.colorScheme.primary`, etc.). This is integration into Material's contract, not replacement of it.

A third-party DS on Android in 2026 typically *opts out of dynamic color* (`dynamicColor = false`) and ships its own scheme via `lightColorScheme()` / `darkColorScheme()`. The trade-off:

- *Dynamic color is a user-pleasing OS feature.* Opting out means the app doesn't theme to the user's wallpaper — a small but visible loss.
- *Brand fidelity is non-negotiable.* Brands generally accept the trade. Exception: consumer apps where wallpaper-themed UI is part of the brand pitch (rare).

The semantic mapping: DS's `color/action/primary` maps to `MaterialTheme.colorScheme.primary` for components reading from the M3 surface (third-party Material components), and to a direct token reference for in-house components.

### React Native, Flutter

**React Native** — `useColorScheme()` returns 'light'|'dark'|null from system; small `PlatformColor` API. Theming is via React Context with a theme provider exposing the DS's tokens. The DS reimplements its color machinery as a JS theme object. **Relying entirely on `useColorScheme` produces a UI that feels slightly alien on both iOS and Android** (the external pass calls this out); deep provider-level theming that intercepts OS signals and maps them back to the shared token architecture is the practitioner-grade pattern.

**Flutter** — `MaterialColor`, `ColorScheme` are strongly tied to Material. Opting out is verbose; the convention is to layer DS tokens *over* the Material `ColorScheme` (set the ColorScheme's primary, secondary, etc., to your token values; let Material components inherit; ship custom widgets reading from your theme).

### The platform-divergence cost

A DS shipping across iOS, Android, web, RN, Flutter must reimplement its theming machinery in each platform's idiom. **This is the largest "platform tax" in cross-platform DS work** — meaningfully more than the equivalent for spacing or typography, because each platform's color system is opinionated and the DS has to either fight or merge.

DTCG modes + Style Dictionary translators reduce the cost by automating mode → platform-output translation, but don't eliminate per-platform theming integration work. Each platform's theme provider still has to be built, tested, maintained.

---

## 9. AI-readable color descriptions

The most material 2024–2026 shift: AI agents are first-class consumers of color tokens. An agent analysing a traditional JSON file sees `color-primary-600` with value `oklch(0.45 0.15 250)` and has zero understanding of whether this is a background, text color, or destructive action. Prompted to build a component, the agent hallucinates hex values or mis-uses semantic tokens entirely. **The token's name and value carry zero behavioural contract** — the agent has to infer everything, and inference at this depth is unreliable.

The fields a color token needs to be agent-consumable (synthesising both passes; the practice extends 23-typography-tokenisation.md's five-field schema with two color-specific additions):

- **`$description`** — what this color *is* in plain terms. "Destructive background surface." Reads to a human reviewer as well as the agent.
- **`when_to_use`** — contexts where the token is correct. "Apply as `background-color` for destructive actions, error banners, or deletion confirmations." Answers *the affirmative case*.
- **`avoid_when`** — contexts where the token is wrong. "Do not use for text. Do not use for standard warnings." The pair with `when_to_use`/`$description` is what helps the agent rule out incorrect picks.
- **`paired_with`** — which tokens compose with this one. For a foreground, the surface tokens it's tested against; for a surface, the text colors passing contrast on it. *This is the load-bearing field for AI:* a model picking text-on-surface needs the foreground that's been validated against the chosen surface; without `paired_with`, the agent has to compute contrast itself, which it does poorly.
- **`contrast_with`** — explicit guaranteed-accessible pairings. `"contrast_with": [{ token: "color/text/primary", min_contrast: "AA", surface: "default" }]`. Converts a compliance check the agent would have to compute into a lookup.
- **`mode_overrides`** — how the token resolves in light/dark/HC/forced-colors. Lets the agent reason about cross-mode behaviour without having to query the catalogue per mode.
- **`meaning`** *(optional but high-leverage)* — what this color signifies semantically. "Destructive action," "elevated surface in dark mode," "subtle background for inactive UI." Highest-ROI field for an agent picking a color for a use case it hasn't seen — answers *what is this for*. A model picking a color for "delete account button" needs to know which token means "destructive"; without `meaning`, it infers from name (`color/status/error` is hopeful; `color/red-9` is hopeless).

```json
{
  "semantic": {
    "surface": {
      "danger": {
        "$type": "color",
        "$value": "{primitive.red.600}",
        "$description": "Destructive background surface.",
        "meaning": "Destructive action signalling.",
        "when_to_use": "Background for destructive actions, error banners, deletion confirmations.",
        "avoid_when": "Do not use for text. Do not use for standard warnings or info states.",
        "paired_with": "{semantic.text.on-danger}",
        "contrast_with": [{ "token": "{semantic.text.on-danger}", "min_contrast": "APCA Lc 75" }],
        "mode_overrides": { "dark": "{primitive.red.500}", "forced-colors": "Canvas" }
      }
    }
  }
}
```

**Which fields move the needle.**

- `meaning` and `paired_with` are the highest leverage — they answer the two questions a model picking a color most needs to answer ("is this the right color for this purpose?" and "what should I put with it?").
- `contrast_with` is the third — converts a compliance check the agent would otherwise compute (poorly) into a lookup.
- `when_to_use` / `avoid_when` are valuable but lower leverage; the model can often infer them from `meaning`.
- `mode_overrides` matters most for agents generating dark-mode-aware code; otherwise nice-to-have.

**Nice-to-have fields.** `tonal_palette_siblings` (linking each color in a ramp to its neighbours in the same hue, so a model picking step 9 can reach for step 8 hover and step 11 text without re-querying); `forced_colors_mapping` (the system keyword the token resolves to); `gamut_clamps` (the sRGB and P3 versions when the source is OKLCH).

**The architectural shift.** This is the same argument 15-ai-in-ds.md makes about components-as-data: the `.ai.json` file is the agent surface, and the per-component schema is what makes the system actually agent-consumable. Color is the foundation where the argument has the highest leverage today — agents pick colors in nearly every generation, and a color-rich AI-readable schema converts the system from passive storage into an active, agent-orchestrated semantic ruleset. This is where AI-readable design tokens stop being a nice-to-have and become the apex deliverable.

---

## Failure modes

1. **Component-tier color tokens proliferate.** Every component ships its own background, text, border, and state tokens. Symptom: hundreds of color tokens, brittle theming, multi-day re-brand work. Cause: missing or incomplete semantic tier. Fix: ship a complete semantic tier; lint primitives out of consumer CSS; promote three-component duplications to new semantics.
2. **HSL ramps in a 2026 system.** Symptom: dark-mode inversion produces inconsistent perceived weights; algorithmically generated contrast pairs fail; gradients show dead grey midpoints. Fix: re-author primitives in OKLCH, verify with APCA in the design tool, accept the migration cost. Don't let "we're already shipping HSL" defer the work.
3. **`var(--blue-9)` in component CSS.** Consumers reach past semantics for primitives. Theming and re-branding break. Fix: ship a complete semantic tier; lint primitives out at build; treat primitive references in consumer CSS as a lint error.
4. **Disabled-by-contrast-exemption.** UI passes WCAG audit while being unusable for AT users. Fix: ship `color/action/inactive` (preserved contrast) as the default; reserve `color/action/disabled` for legacy patterns the engagement can't shed.
5. **Forced-colors mode strips structure.** Components vanish in WHCM because they relied on `box-shadow` or background-color overlays. Fix: declare transparent borders on all structural components; verify the entire system in WHCM during QA, not just at component review.
6. **Multi-brand contrast failure.** Brand B's primary fails AA on shared-surface neutral. Fix: contrast-tier-named-step rule at the primitive level + forced-foreground `on-X` token at the semantic level. Validate every brand against the contrast contract during foundations, not during component review.
7. **Data-vis aliased off UI tokens.** A brand-color shift silently destroys a dashboard's sequential contrast. Fix: isolated `color/viz/*` namespace; never alias UI tokens into viz; ship 50–100 viz primitives if data-vis is in scope, scope it out otherwise.
8. **Hex round-trip strips OKLCH/P3.** The exported color is duller than the design source; the engineer sees one value, the designer authored another. Fix: per-platform fidelity contract; preserve OKLCH end-to-end on web; test converted iOS/Android colors against design source before shipping.
9. **Theme flash on every page load.** Symptom: visible mode swap during hydration. Fix: server-rendered theme decision *or* inline blocking script in `<head>` that sets `data-theme` before body renders. Both are well-understood patterns; ship one in the foundation, not as a last-mile retrofit.
10. **Brand-against-its-own-system trap unsurfaced.** Brand yellow can't be primary action on white; the engagement discovers it during component review and the budget for foundations is already spent. Fix: surface brand-on-system contrast tests in Foundations; ship a written architectural decision ("brand as accent, deep blue as action," etc.); the workshop output is the deliverable, not a verbal nod.

---

## Tensions and open questions

1. **OKLCH preservation in the design pipeline.** Most pipelines silently quantise to hex on export. Tokens Studio, recent Figma plugins, and DTCG `colorSpace` schema fields exist to preserve OKLCH end-to-end, but no mainstream commercial pipeline (Figma → Style Dictionary → CSS) does it without manual configuration. The practice's recommendation is configure-it-and-ship; the catalogue-tier discipline (verifying the exported color in OKLCH-aware tooling) is what actually catches drift.

2. **APCA adoption pace.** Adobe Spectrum, GitHub Primer, IBM Carbon Charts, and Tailwind v4 have moved; legal/procurement standards have not. Engagements requiring WCAG 2.x compliance can't substitute APCA, so the practice runs both. Whether WCAG 3 finalises on APCA or pivots to a successor is unresolved through mid-2026 — verification path: w3.org/TR/wcag-3.0/ tracking. The practice's stance (WCAG 2 as floor, APCA as quality bar) holds regardless of how WCAG 3 lands.

3. **`color-mix()` vs. explicit state tokens.** Reduces token volume by 30–50%, breaks Style Dictionary's cross-platform translation, breaks Figma resolution. Until tooling catches up, the choice is web-only state derivation vs. explicit cross-platform state tokens. The practice currently ships explicit tokens for cross-platform engagements and is watching tooling movement quarterly.

4. **HCT for non-Material engagements.** Material 3's tonal-palette method is mathematically elegant and produces guaranteed-contrast palettes; the cost is a Material dependency. The practice's stance (OKLCH for non-Material, accept the marginally less sophisticated appearance model) is provisional — if Material's `material-color-utilities` matures into a portable, dependency-light HCT library, reconsider.

5. **Editorial vs. product palettes — shared-semantics vs. parallel-primitives.** The practice defaults to shared primitives + separate semantic roles for single-product engagements. Genuinely two-property engagements should ship parallel primitive packages with a shared chassis. The boundary between "single-product with editorial surfaces" and "two-property" is a judgment call; the engagement's marketing/product team separation is the practical signal.

6. **Forced-colors as a first-class theme axis.** Most systems treat it as a constraint to design around. The transparent-border trick, system-keyword fallbacks, and structure-via-non-color-signals could be encoded as a first-class theme axis (`forced-colors:active` mode in DTCG), with the system declaring per-token resolution rather than relying on browser default behaviour. The pattern is emerging; not yet standard.

7. **AI-readable description fields — the verification gap.** No tool currently *validates* that a token's `paired_with` and `contrast_with` claims hold under the system's actual primitives. Manual checks today; ripe for a build-time validator.

8. **Cross-platform fidelity testing.** No mainstream tool renders the same token on web (sRGB/P3/OKLCH), iOS, and Android side-by-side and reports the perceptual delta. Practitioners sample manually. The discipline is to declare the per-platform fidelity contract explicitly and accept manual verification for now.

---

## See also

- **02-design-foundations** — the foundation-layer treatment of color this file extends with the spec-and-platform depth (color spaces, contrast model, theming axes, native integration).
- **22-token-architecture-extensions** — DTCG composite-token mechanics; this file applies the same architecture to color tokens specifically.
- **24-tokens-at-scale** — the multi-brand portfolio and validation matrix this file's color tokens consume; the contrast-tier-named-step rule and `on-X` foreground tokens are the color-layer extension of 24's discipline.
- **14-accessibility** — WCAG contract; this file's APCA quality-bar position and the disabled-state harder line are the architectural depth on top.
- **28-web-accessibility-implementation** — implementation depth; the forced-colors transparent-border trick lives here at the component layer.
- **15-ai-in-ds** — components-as-data and AI-readable descriptions; this file applies the same argument to color tokens specifically with the seven-field schema.
- **23-typography-tokenisation** — the parallel foundation file; the architecture, voice, and depth match.
- **11-mobile-and-cross-platform** — the platform-tax cost; this file extends with the color-specific integration discipline (dynamic Color on iOS, M3 colorScheme integration on Android).
- **16-mobile-accessibility-implementation** — per-platform Dynamic Type / sp / Compose coverage; this file's iOS dynamic-Color and Android `MaterialTheme.colorScheme` coverage is the color-specific extension.
- **09-gaps-and-open-questions** — the Chart-component gap (§5.2) is the data-vis-palette concern this file's §7 addresses architecturally.
- **components/_schema.md** — the §15 schema discipline this file's AI-readable color schema parallels.

---

*Provenance: dual-agent research run, `_research/_inbound/2026-06-15-color-systems/` (15 June 2026). Both passes converged on the three-tier architecture with component-tier color tokens minimised, OKLCH as authoring default with HSL declared dead, P3 dual-track CSS strategy, HCT as Material-only, the three documented WCAG-2.x failure modes (dark-mode under-prediction, small-text trap, yellow-on-white over-prediction), APCA as the perceptual quality bar above WCAG 2's legal floor, the orthogonal-axes theming model, the dark-mode lift pattern, the FOUC/theme-flash mitigations, multi-brand contrast failure as the primary risk in primitive-swap architectures, the brand-vs-system contrast-step alignment problem with three documented mitigations, the three data-viz palette types and the 8–12 categorical limit, the data-vis-tokens-must-not-alias-UI-tokens isolation rule, OKLCH-derived sequential ramps as a comprehension upgrade, native iOS/Android integration as opinionated rather than 1:1 mapping, the AI-readable seven-field color schema (with `paired_with`, `meaning`, and `contrast_with` as the highest-leverage fields), the five-paradigm naming framing, the `color-mix()`/relative-color-syntax token-volume reduction with the Style-Dictionary-doesn't-preserve-it tooling gap, and `color-scheme: light dark` as architecturally crucial. The external pass moved three calls: it landed the harder line on disabled-state contrast (eliminate naive disabled controls; default to `aria-disabled` + visible reasoning, with `color/action/disabled` reserved as a legacy fallback) — the practice adopts this aligned with the Button brief's focusable-inactive position; it surfaced the **forced-foreground `on-X` luminance-flip token** as the load-bearing technique for multi-brand `on-primary` discipline (Claude pass had it implicitly via contrast-tier rules; external named the mechanism); and it surfaced the **transparent-border trick** as the positive structural-preservation pattern in forced-colors mode (Claude pass treated forced-colors as constraint-only). The external pass also offered a stronger position on editorial vs. product palettes (parallel primitive packages with shared chassis, vs. Claude's shared-primitives-with-separate-semantic-roles); reconciled as Claude's path for most single-product engagements and external's path for genuinely two-property engagements (multi-property holding-company portfolios). The Claude pass moved one call: it surfaced the `color-mix()`/Style-Dictionary fidelity gap as a tooling-decision the engagement has to make explicitly (web-only state derivation vs. explicit cross-platform state tokens), which the external pass treated as a clean win without naming the gap. Both passes converged on the AI-readable schema; the synthesis adds `meaning` as a seventh field beyond the external pass's six, paralleling 23-typography-tokenisation.md's discipline. Apparent disagreement on token volume (external "10–15 primitive scales, 40–60 semantic, near-zero component"; Claude "80–170 primitive tokens, 30–60 semantic, <10 component") is resolved by recognising the units: external counted ramps, Claude counted atomic tokens; ~12 ramps × 10–12 steps reconciles to Claude's number — synthesis names this explicitly. The HeroUI cite (external) and the Color Scales I/O / Atmos plugin specifics are folded in but not load-bearing. Browser-support claims for `oklch()`, `color-mix()`, relative color syntax, and `color()` are dated mid-2026 and verified against caniuse.com and MDN per-feature pages; re-check before relying on them more than six months from this timestamp.*

*Provenance (June 2026 source-text pass — 09 §1.27 closure): all four flags surfaced by the original run are now closed with primary-source captures. (1) **APCA Lc threshold table** — captured at `_source-text/ext-apca-thresholds.txt` from `readtech.org/ARC/tests/visual-readability-contrast/`; the §3 tier table now reflects the canonical font-size × weight × Lc lookup matrix, including the correction that the "14px @ 400 weight" figure is Lc 80–85, not Lc 90+. The Lc 30 floor for non-text UI is flagged as practitioner shorthand pending Myndex's published Non-Text Contrast guideline. (2) **DTCG `colorSpace: "display-p3"`** — captured at `_source-text/ext-dtcg-format-module.txt` from the Color Module 2025.10 (13 June 2026 preview draft); fourteen colorSpace values enumerated, `display-p3` confirmed; §1 line de-hedged. (3) **Style Dictionary `color-mix()` watch item** — captured at `_source-text/ext-style-dictionary-changelog.txt` (current version 5.4.4); no native preservation; recommendation in §1 holds; next quarterly check 2026-09-15. (4) **CSS Color 4 §14.2 algorithm attribution** — captured in full at `_source-text/ext-css-color-4-gamut-mapping.txt` via firecrawl_scrape against the Editor's Draft (7 May 2026). The spec's load-bearing sentence: *"Implementations may choose any of the three algorithms based on their quality and runtime efficiency tradeoffs, and must use their chosen algorithm wherever CSS mandates that gamut mapping be performed."* There is no single normative CSS default — the three §14.2 algorithms (Binary Search with Local MINDE, EdgeSeeker, Ray Trace) are siblings, all aiming at constant-L, constant-H chroma reduction in OkLCh under a relative colorimetric intent. The §1 line previously read "CSS Color 4 default (chroma-reduction)" with hedging on which §14.2 algorithm was default; corrected to "CSS Color 4 chroma reduction" naming the spec's frame faithfully and noting that browser choice is a per-engine, per-version question tracked via WPT.*

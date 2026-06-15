---
type: practice-area
title: Typography Tokenisation
description: Three-tier mandatory typography stack, modular scales with the display pivot, fluid type with clamp() + container queries + rem-floor accessibility rule, variable fonts as tokenisation, multi-script as DTCG modes.
tags: [extension, typography, tokens, dtcg, fluid-type, variable-fonts]
timestamp: 2026-05-16
---

# 23 — Typography Tokenisation

> Typography is the most under-tokenised foundation in the design systems our practice audits — colors and spacing are usually tokenised; typography is usually a list of styles with one or two ratios behind them and no architecture. The 2024–2026 platform shifts (DTCG 2025.10 composite typography, fluid type with `clamp()`, container queries reaching wide support, variable fonts as first-class, native Dynamic Type / sp / `LineHeightStyle.Trim`) have changed what good typography tokenisation looks like. This file is the depth our existing 02-design-foundations and 12-figma-practice files don't reach: the shape of a typography token set, modular scales with the display pivot, fluid type and container queries, variable fonts as a tokenisation problem, line-height discipline, multi-script, native platform translation, and the AI-readable description schema typography benefits from most.

---

## Why typography needs its own file

Color and spacing are the easy tokens — atomic values, one tier of names, mostly platform-agnostic. Typography is *composite by default*: a usable typography token names a family, a size, a weight, a line-height, a tracking value, and often a case treatment, all bundled together. Atomic typography tokens are necessary at the primitive layer; composite tokens are what consumers actually reach for at the component layer. **The architecture has to ship both, and most systems we audit ship one or the other but not both.**

The platform's underneath has also moved further on typography than on most other token categories. The 2024–2026 web ships `clamp()` for fluid type, container queries (`cqi`) for component-relative sizing, full variable font axis support, `font-optical-sizing: auto`, and (partially) `text-box-trim` for cap-height alignment. Native platforms have caught up on text scaling — iOS Dynamic Type, Android `sp`, Compose `LineHeightStyle`, Flutter's `MaterialTextScaler`. **The practical depth a typography token system has to encode in 2026 is larger than what 02 currently treats**, and the gap shows up most acutely on brand-critical surfaces — which is most of our agency work.

What this file extends: 02's atomic-tokens-and-modular-scale framing; 12-figma-practice's Variables-and-modes treatment; 13-internationalization-and-rtl's multi-script positioning; 14-accessibility's text-scaling architecture; 16-mobile-accessibility-implementation's Dynamic Type / sp coverage. What it doesn't replace: any of those. This is the typography-specific layer on top.

---

## The shape of a typography token set

### The minimum viable atomic primitives

Below the composite layer, the atomic primitives a production-grade typography token set ships:

| Property | DTCG `$type` | Notes |
|---|---|---|
| Font family | `fontFamily` | Brand fonts with system-font fallback stacks. Variable fonts identified explicitly. |
| Font size | `dimension` | `rem` on web; `sp` (or equivalent) on Android. Fluid sizes are a separate concern — see below. |
| Font weight | `fontWeight` | Continuous numeric values (`100`–`1000`) when variable fonts are in use; named keywords (`regular`, `bold`) only for static-font fallback. |
| Line height | `number` (preferred) or `dimension` | Unit-less multipliers in every case where the system allows it. See the line-height section below. |
| Letter spacing | `dimension` | `em` or `rem`-relative to track optically with font-size changes. |
| Font style | `string` | `normal`, `italic`, or — for variable fonts with a `slnt` axis — the specific slant value. |
| Text transform | `string` | `none`, `uppercase`, `lowercase`. Not a brand-personality decision; a semantic-role decision. |

Optional but increasingly standard:

- `textDecoration` — for systems where underline weight and offset are part of the typographic identity.
- `fontFeatureSettings` — stylistic sets, alternate ligatures, contextual alternates. Variable-font-era systems use this to expose typographic features that previously required separate font files.
- Variable font axes other than `wght` and `slnt` — `wdth` (width), `opsz` (optical size), `GRAD` (grade). See the variable fonts section.

### DTCG composite typography tokens

DTCG 2025.10 defines a typography token as a composite type. The token bundles family, size, weight, line-height, tracking, etc. into a single named entity (`heading/large`, `body/medium`). The composite is what designers and component authors actually reach for; the atomic primitives sit underneath as the source of the composite's sub-property values.

The spec supports property-level aliasing inside the composite: the `fontSize` sub-property of a composite can reference an atomic `font-size/medium` token. **Most tools as of mid-2026 do not faithfully preserve property-level aliases on round-trip** (see 22 for the broader composite-fidelity-gap discussion). The practitioner consequence is the same as for shadow and transition composites: **carry composites as the source-of-truth representation, flatten them at the build pipeline into per-platform atomic outputs that runtime can consume.** The composite is an authoring convenience; the atomic outputs are the runtime contract.

### Atomic, composite, or both

The decision has been litigated and the 2026 answer is settled: **ship both, in a three-tier stack.**

- **Atomic primitive tier.** Family, size, weight, line-height, tracking — each a named token. These are the building blocks; consumers reach for them directly only when the composite layer doesn't cover the use case.
- **Semantic composite tier.** Named composites that bundle the atomic primitives into role-based tokens (`body/medium`, `heading/large`, `label/small`, `code/inline`). These are what 90% of UI authoring reaches for.
- **Component tier.** Per-component overrides where a component's typography legitimately diverges from the semantic default (a `Badge` whose weight is heavier than the equivalent `Label`). Used sparingly; the rule of three from 03-component-library applies.

**Atomic-only architectures** force consumers to compose typography themselves, which produces the "token soup" failure mode — every component picks its own combination of atomic values, consistency collapses, the system's typographic identity fragments.

**Composite-only architectures** are precise but inflexible. Designers who need a heading at body weight (an editorial pattern) or body text at a heading's line-height (a tabular-content pattern) have to invent a new composite, and the composite catalog accumulates one-offs.

The hybrid — three-tier with the semantic composite layer doing the work for the common case — is the convergent answer.

### Token volume — how many composites

The empirical heuristic across mature 2026 systems: **15–25 composite typography tokens** is the right scale for an agency engagement covering both product and marketing surfaces. Fewer leaves too much composition to consumers; more produces a catalog designers can't internalise.

A typical shape:

- 5–8 heading tokens (`heading/xxl`, `xl`, `l`, `m`, `s`, plus optionally `xs` and a display-tier `display/xl`, `display/l`).
- 3–4 body tokens (`body/large`, `medium`, `small`).
- 2–3 label / caption tokens (`label/medium`, `label/small`, `caption`).
- 2–3 specialised tokens (`code/inline`, `button/medium`, `link/inline`).

Brand-critical surfaces sometimes justify additional editorial composites (`pull-quote`, `kicker`, `byline`); product-focused systems usually don't.

### Brand fonts, system fonts, fallback stacks

The fallback stack lives in the `fontFamily` token's value, not in consumer CSS. The token encodes the brand font, the closest system fallback, and the generic family terminator:

```json
"font-family/brand-display": {
  "$type": "fontFamily",
  "$value": ["BrandDisplay Variable", "system-ui", "-apple-system", "BlinkMacSystemFont", "sans-serif"]
}
```

The `system-ui` family name engages the host OS's native font (San Francisco on iOS, Roboto on Android, Segoe on Windows), which produces faster first paint and better accessibility integration than naming each platform explicitly. The generic family terminator (`sans-serif`, `serif`, `monospace`) is the floor of the stack.

Variable fonts are tagged explicitly in the family name or in `$extensions`; the build pipeline reads the tag to know whether to emit weight tokens as continuous numerics or as named keywords.

---

## Modular scales: math, trade-offs, the display pivot

The modular scale is the math of the system. The 2026 position has stabilised on one practitioner pattern that the field-converged-on language confirms: **a single ratio is wrong for most brand-critical engagements; the system needs a split scale that pivots at the display tier.**

### Canonical ratios

The named ratios and the brand contexts they fit:

| Ratio | Value | Fits |
|---|---|---|
| Minor Second | 1.067 | High-density utility, dashboards, technical interfaces |
| Major Second | 1.125 | Enterprise SaaS, dense product interfaces |
| Minor Third | 1.200 | General product design, consumer apps |
| Major Third | 1.250 | Marketing sites, product landing pages |
| Perfect Fourth | 1.333 | Editorial brands, marketing-heavy surfaces |
| Augmented Fourth | 1.414 | Expressive editorial |
| Perfect Fifth | 1.500 | High-style editorial, magazine-tier |
| Golden Ratio | 1.618 | Luxury, high-contrast, sparse with maximum impact |

These are not aesthetic preferences. They are functional decisions about how much hierarchical contrast the system has between adjacent type sizes, and which contrast level the brand can carry without the small sizes becoming illegible or the large sizes becoming visually overwhelming.

### The display pivot

A strict modular scale fails at the extremes. A `1.500` ratio applied uniformly produces captions too small to read and headlines that step too aggressively past usable display sizes. A `1.125` ratio applied uniformly produces no visible distinction between an H1 and an H2 in a brand-expressive context.

**The practitioner pattern: two ratios, one for text sizes and one for display.** The token system ships two multipliers:

```
scale-ratio-text     → 1.200 (Minor Third) for body, captions, labels, small headings
scale-ratio-display  → 1.414 (Augmented Fourth) for display-tier headings and hero typography
```

Body and metadata sit on the conservative scale; display headlines sit on the expressive scale. The pivot point is engagement-dependent — typically somewhere between `heading/m` and `heading/l`. The token names mask the pivot from consumers; what designers see is a coherent hierarchy that has the right rhythm at small sizes and the right impact at large.

### Mapping the math to names

Three competing naming conventions for size scales — all three have their place in a three-tier stack:

| Layer | Convention | Use |
|---|---|---|
| Primitive | Mathematical (`step-(-1)`, `step-0`, `step-1`) | Architect-facing; expresses the modular relationship directly. Source of the values. |
| Numeric internal | Numeric (`size-100`, `200`, `300`) | System-internal references; extends cleanly past 5–7 steps when needed. |
| Semantic surface | T-shirt or role-based (`size-xs/sm/md/lg/xl` or `font-size/body`, `font-size/heading-l`) | Consumer-facing; the layer component authors reach for. |

This is the same primitive → semantic split that 02 already names, applied to typography specifically. The primitive layer is mathematical; the consumer-facing layer is semantic. The numeric internal tier is a convenience the architect can omit on smaller systems.

### Tooling

Practitioner tools that produce these scales mechanically:

- **Utopia** (`utopia.fyi`) — generates fluid-type scales with the `clamp()` math precomputed and exportable as CSS custom properties or a DTCG-compatible token file. The canonical tool for marketing-tier responsive systems.
- **Type Scale Clamp Generator** — the lighter-weight alternative when the system needs only a few fluid tokens rather than a full responsive scale.
- **Modularscale** and **Typescale** — visual exploration of ratios; useful for designer-architect conversations before committing to a scale.

These tools produce the values; the practitioner's job is to map them into the three-tier token stack with the right naming.

---

## Fluid type, `clamp()`, and container queries

The 2024–2026 web platform has changed how responsive typography is encoded. Breakpoint-driven type scales (the 2015–2020 pattern of media queries that swap font sizes at named widths) have been largely superseded by fluid type for marketing-tier surfaces.

### The `clamp()` mechanic

`clamp(min, preferred, max)` is the engine. The `min` value floors the size on small viewports; the `max` ceils it on large viewports; the `preferred` value interpolates linearly between them using a viewport-relative or container-relative unit.

```css
font-size: clamp(1rem, 0.875rem + 0.625vw, 1.25rem);
```

This token reads as 16px at a 320px viewport, scales linearly with the viewport, and caps at 20px at 960px. The math behind the `preferred` value is the part that practitioners get wrong most often — it requires solving a linear equation across the min-viewport-width / max-viewport-width pair to produce the right interpolation coefficient. The named tools (Utopia and the Type Scale Clamp Generator) exist primarily to do this math correctly.

### Container queries change the calculus

Container queries reached wide support in 2023 and have become a default of the 2026 web platform. The practical implication for typography: **type can now scale relative to its container, not the viewport.** A `ProductCard` component's typography responds to the card's width when the card is placed in a narrow sidebar (300px wide) vs. a full-width hero (1200px wide). The same component is portable across layouts.

The unit for this is `cqi` (container query inline) — analogous to `vw` but measured against the nearest container query parent rather than the viewport:

```css
font-size: clamp(1rem, 0.875rem + 0.5cqi, 1.25rem);
```

**The token system should ship two parallel fluid-type sets — viewport-relative and container-relative — and let component authors choose.** Page-level typography (hero headlines, section titles on marketing pages) usually wants viewport-relative; component-level typography (card titles, sidebar labels) usually wants container-relative. Shipping only viewport-relative locks consumers into the page-as-context model that the platform has moved past.

### When fluid type is the wrong answer

Fluid type is a marketing-tier default, not a universal default. Three contexts where static type is correct:

- **Long-form reading.** Continuous prose benefits from stable line lengths and predictable rhythm; a font-size that shifts continuously across viewport changes interferes with the reader's eye. Articles, documentation, and book-tier reading should use static type scales.
- **Locale-aware sizing.** Arabic, Thai, CJK, and Devanagari each have script-specific sizing requirements that a generic `vw` interpolation cannot encode. Fluid type with a single ratio produces wrong sizes in non-Latin scripts. See the multi-script section below.
- **Accessibility-constrained contexts.** Users who have set a custom font size at the browser level expect that size to be honoured. Fluid type that relies too heavily on viewport units can defeat user preferences — see the accessibility rule below.

### The accessibility rule for `clamp()`

The single non-negotiable rule for fluid type: **the `preferred` value must always include a `rem` component, never `vw` alone.** A token whose preferred value is `2vw` does not scale when the user zooms the browser, because zooming changes the viewport in CSS-pixel terms; it scales `rem` values but not `vw` values. A `preferred` value of `1rem + 1vw` scales correctly under user zoom because the `rem` component carries the zoom factor.

This is WCAG 1.4.4 (Resize Text) at the implementation layer. A typography token system that ships `vw`-only preferred values fails the 200% text-resize requirement and creates a regression vector for accessibility conformance.

### Token encoding strategies for fluid type

Three ways to encode a fluid-type token, with descending cross-platform utility:

| Encoding | Form | Strength | Weakness |
|---|---|---|---|
| Single string | `clamp(1rem, 0.875rem + 0.5vw, 1.25rem)` | Direct CSS consumer | Useless on native platforms; requires a parser |
| Primitive triplet | `{ min: "1rem", preferred: "0.875rem + 0.5vw", max: "1.25rem" }` | Build pipeline can emit `clamp()` for web and a static fallback for native | More verbose; requires Style Dictionary transform |
| Runtime function | A JS helper that computes the value at runtime | Maximum flexibility | Off-spec (no DTCG path); generally discouraged |

**The practitioner answer is the primitive triplet.** The build pipeline generates the `clamp()` string for web from the triplet; for native platforms (which have no `clamp()` equivalent), the pipeline emits a static value — typically the `preferred` value at a reference viewport, or a dynamic equivalent if the framework supports one (Compose's `derivedStateOf` of the screen width). The triplet preserves the design intent; the per-platform output is correct for each platform's capabilities.

---

## Variable fonts as a tokenisation problem

Variable fonts have been first-class in the 2024–2026 web platform and have substantially changed what a typography token system can express. They also introduce a tokenisation problem the field has only partially solved: **continuous axes do not naturally map to discrete tokens.**

### The axes that matter

Variable fonts expose registered axes:

- **`wght` (weight)** — continuous from 100 to 1000. Variable-font weight is not a closed set of named weights; it is a slider. The token system has to decide whether to expose the slider or to lock in a discrete set.
- **`wdth` (width)** — character width adjustment. Useful for copyfitting (compressing a headline to a narrower container) and for stylistic variation.
- **`opsz` (optical size)** — automatic adjustment of letterforms for the intended rendering size. Display sizes get higher contrast and finer details; small sizes get thicker stems and wider counters. The single most under-used axis.
- **`slnt` (slant)** — continuous slant for italic-feeling variation without a separate italic font file.
- **`ital` (italic)** — binary or continuous italic axis.

Custom axes (per-typeface) exist on some fonts — `GRAD` (grade), `XHGT` (x-height), and others. Brand-critical engagements often use these.

### The named-instance discipline

The architectural answer to the continuous-axis problem is **named instances**: the typography token system exposes a finite semantic ladder over the continuous range. Instead of letting consumers reach for `font-weight: 437`, the system ships `font-weight/regular` → `450`, `font-weight/medium` → `550`, `font-weight/semibold` → `650`. The continuous range is collapsed into a discrete, designable set.

The principle: **the variable font's continuous design is realised at authoring time and frozen at the token layer.** The architect picks the specific values that produce the system's typographic identity; consumers reach for the names. The flexibility of the underlying font is not exposed to authoring; the discipline of the token system is.

### Optical size as the under-used axis

`opsz` deserves its own callout. Few systems use it; the ones that do produce visibly better typography at the extremes. CSS exposes it via `font-optical-sizing: auto`, which automatically maps the axis to the current `font-size`. The browser interpolates the optical-size axis to match the rendering size. This produces:

- Display headlines with the contrast and finesse the typeface designer drew for display sizes.
- Body text with the thicker stems and wider counters that maintain legibility at small sizes.

**The practice should set `font-optical-sizing: auto` as a global CSS default in every engagement using a variable font with an `opsz` axis.** The token system can ship explicit overrides for cases where the automatic mapping is wrong (a marketing hero that needs the display-grade design at body size for a stylistic effect), but the default is auto.

### Delivery and performance

A single variable WOFF2 file replaces 10+ static weight files. The bandwidth reduction is real and consequential — typical savings of 50–70% on font payload for systems that previously shipped multiple static weights. The trade-off is that variable fonts are large files (one variable font is often 200–400KB), so the savings appear only when the system would otherwise have shipped many static files.

The 2026 delivery discipline:

- **Subsetting.** Strip the axes and Unicode ranges the system doesn't use. A variable font with all 5 axes and all Unicode ranges may be 600KB; subsetted to `wght` + `opsz` + Latin only, it's often under 100KB.
- **`font-display: swap`.** Layout shift is a worse failure than slow font load. Swap (or `optional` for marketing-tier surfaces where missing the brand font for a moment is acceptable) is the default.
- **Self-hosted, not Google Fonts.** Self-hosting via the `@font-face` declaration with the brand font on the same origin avoids the third-party request, the cookie/privacy implications, and the FOUT/FOIT timing variability of CDN-hosted fonts.

### Variable fonts in Figma

Figma's variable font support has matured through 2024–2025 and is robust by mid-2026 for design-tool use. The export-to-DTCG round trip remains imperfect: Figma exports specific weight instances (typically as static-font-equivalents) rather than the axis-and-value pair that would survive a round trip back into the variable font. The Tokens Studio plugin closes most of this gap; Penpot's native DTCG support handles it cleanly.

The discipline: **author with the variable font in Figma; export named instances at the system's chosen axis values; the build pipeline maps the named instances to the variable font's axis values in the runtime CSS.** The token layer holds the named ladder (`weight/regular` → axis value `450`); the runtime CSS uses `font-variation-settings: 'wght' 450` to render.

---

## Line-height, leading, and the discipline of the multiplier

Line-height is the most poorly tokenised typography property in most systems we audit. It is usually a single global value (`1.5`), occasionally a per-token override hardcoded in pixels (`24px`), and never a structured part of the typography scale. The 2026 discipline is straightforward and the practice should adopt it as a default.

### Unit-less multipliers

**Line-height should always be expressed as a unit-less number** (`1.4`, `1.55`, `1.2`). A unit-less multiplier scales with the element's `font-size` automatically. A dimensional line-height (`24px`) does not — it stays fixed when the font-size changes, producing the "collapsing" and "exploding" text failures that are visible across the field.

The CSS spec has always supported unit-less line-height; the field's slow adoption is a habits problem, not a platform problem. The practice's default should be unit-less in every case the system allows.

### Body vs. display ratios

The convergent reading-research-backed ratios:

- **Body text.** 1.4 to 1.6 times the font-size. Sufficient air for the eye to track long lines.
- **Display text.** 1.1 to 1.3 times the font-size. Larger text has a stronger visual presence and reads better with tighter leading.

The token system encodes these as named primitives:

```
line-height/tight       → 1.15 (display)
line-height/snug        → 1.3  (sub-display, large headings)
line-height/normal      → 1.5  (body)
line-height/relaxed     → 1.65 (long-form reading)
```

Composite typography tokens reference the appropriate primitive. The semantic composite `body/medium` references `line-height/normal`; `heading/xl` references `line-height/tight`.

### Optical leading

A more sophisticated approach available on the modern platform: expressing line-height relative to the font's intrinsic line gap (the metrics-defined space between descenders and ascenders) rather than as a flat multiplier of font-size. Different typefaces with different x-heights and ascender/descender ratios produce different visual rhythm at the same `1.5` multiplier; expressing leading optically (relative to the intrinsic gap) produces consistent visual rhythm across typeface changes.

Browser support for optical leading is partial; the field has not converged on a canonical way to encode it in tokens. Flag as a watch-list item; do not yet ship as a default.

### `text-box-trim` — the alignment-baseline story

`text-box-trim` (and the longhand `text-box-edge`) is the CSS property that removes the leading "slug" at the top and bottom of a text block, enabling cap-height or x-height alignment. It is the web platform's equivalent to iOS's `leading-trim` and Compose's `LineHeightStyle.Trim`. When it works, it dramatically simplifies the spacing tokens applied around typography — designers can align text to its caps without compensating for the slug.

**As of mid-May 2026, `text-box-trim` is Limited Availability, not Baseline.** Shipped in Chrome 133+ (February 2025), Safari 18.2+ (December 2024), and Edge 133+. **Firefox has implemented the property but keeps it disabled by default through at least Firefox 149.** This is a structural gap — without Firefox, the property cannot be a load-bearing part of a cross-browser typography system.

Verification path: `caniuse.com/mdn-css_properties_text-box-trim` and the MDN `text-box-trim` reference.

The practical consequence for cross-platform typography systems: **iOS leading-trim and Compose `LineHeightStyle.Trim` remain the only currently-working trim story across the full web/native matrix.** The web side can opt-in progressively (using `@supports` to detect availability), but the design system cannot rely on trim being present everywhere. Cap-height alignment as a system-level feature is a 2027+ commitment, not a 2026 one.

When `text-box-trim` does reach Baseline, the change will be substantial — spacing tokens currently compensating for the slug will need a re-derivation, and the design tooling around vertical rhythm will reset. Track Firefox's progress as the gating item.

---

## Multi-script and multi-locale typography

Typography for a global product is not a single token set scaled across languages. Each writing system has its own optical and metric requirements. Naive application of a Latin-tuned token set to non-Latin scripts produces consistently wrong typography.

### What the scripts actually need

- **Arabic** typically reads at 10–15% larger font sizes than Latin to achieve the same perceived readability — the script's stroke complexity and diacritic positioning require more pixels per glyph. Line-height ratios are also typically larger.
- **CJK (Chinese, Japanese, Korean)** uses tighter line-height ratios than Latin (often 1.4–1.5 for body where Latin uses 1.5–1.65). CJK fonts do not benefit from the same modular scales — the small-size end of a Latin scale produces unreadable CJK glyphs.
- **Thai** requires significant vertical breathing room for the script's tall ascenders and deep descenders. Line-height ratios in the 1.7+ range are common.
- **Devanagari** also needs vertical room for the script's shirorekha (the connecting line above letters) and below-the-line marks.

A single `body/medium` composite token cannot encode all of these. The token system has to either ship locale-specific composites or expose the composite as a resolver that selects script-appropriate values.

### The DS contract — modes, not separate files

The architectural answer: **DTCG modes carrying script-specific values, not separate token files per script.** A single semantic composite (`body/medium`) resolves to different sub-property values when the active mode is `script-arabic` vs. `script-latin`. The consumer (the application's typography provider) sets the mode based on the active locale; the token layer handles the resolution.

This extends 13-internationalization-and-rtl's existing position that locale-awareness is a mode dimension, not a separate set. The token system stays single-source-of-truth; the locale resolves at the build or runtime layer.

### Variable fonts as a multi-script tool

Single-binary multi-script variable fonts are a reality in 2026 — fonts that ship both Latin and Arabic glyphs in one file, with shared axis controls. The advantage is delivery efficiency (one font request instead of two); the limitation is that the `opsz` and `wght` axes may need to behave differently for each script. Current variable-font tooling does not always handle per-script axis curves cleanly; the design system may need to ship script-specific axis overrides via `font-feature-settings` or `font-variation-settings`.

This is an emerging-pattern watch-list item rather than a 2026 default. Most agency engagements still ship script-specific font files for non-Latin scripts; the single-binary path is right when the engagement has both the budget for the more-complex font choice and the typography lead with the expertise to validate it.

---

## Native platform translation

The translation from DTCG composite to native code is the single highest-stakes part of the typography token pipeline. **Native platforms have their own text-scaling architectures (iOS Dynamic Type, Android `sp`, Compose `LineHeightStyle`, Flutter `MaterialTextScaler`); typography tokens that ignore these architectures fail accessibility by construction.**

### The translation matrix

| Platform | Output format | Scaling mechanism | The discipline |
|---|---|---|---|
| Web (CSS) | CSS custom properties, utility classes | `rem`, `clamp()`, `text-box-trim` (where available) | Every fluid-type token includes a `rem` floor; consumer respects user font-size preference |
| iOS (SwiftUI) | `Font` extensions, `UIFontDescriptor` | Dynamic Type via `.font(.body)` and `relativeTo:` parameters | Every composite must bridge to a Dynamic Type style — see below |
| Android (Views and Compose) | `Typography` in MaterialTheme, `TextStyle` | `sp` units; `LineHeightStyle` and `LineHeightStyle.Trim` | Every dimension token emits `sp` not `dp`; line-height respects system text scale |
| Flutter | `TextTheme` / `TextStyle` | `MaterialTextScaler` | Every text widget uses `MediaQuery.textScalerOf` for system scaling |
| React Native | Style objects, typography token package | Often requires a native module to bridge to Dynamic Type | Either bridge to native scaling or accept the cost of an accessibility gap |

### Dynamic Type and `relativeTo:` — the iOS discipline

iOS users can scale text up to 310% via Dynamic Type. A typography token system on iOS that uses fixed point sizes (`Font.system(size: 16)`) ignores Dynamic Type entirely; users see their text at 16 points regardless of their accessibility settings.

**The discipline: every composite typography token on iOS bridges to a Dynamic Type style.** SwiftUI's `Font` API exposes the bridge via `relativeTo:`:

```swift
Font.custom("BrandSans", size: 16, relativeTo: .body)
```

This maps the brand font, sized at 16 points at the default scale, to scale relative to the `.body` Dynamic Type style. When the user increases their text size, the brand-font text scales correspondingly. The Style Dictionary transform for iOS typography composites must emit the `relativeTo:` parameter for every composite; without it, the system ships fixed-size typography that fails Apple's Human Interface Guidelines and the App Store accessibility expectations.

### `sp` not `dp` — the Android discipline

Android exposes two unit systems: `dp` (density-independent pixels, fixed across user preferences) and `sp` (scale-independent pixels, scaled by the user's font-size preference). Typography uses `sp`; non-typography sizing uses `dp`.

A typography token system that emits `dp` for font sizes ignores the user's text scale. The Style Dictionary transform for Android must emit font-size tokens as `sp` and line-height tokens with `LineHeightStyle` that scales correspondingly. Compose 1.6+ exposes the controls (`TextStyle.lineHeightStyle.alignment`, `LineHeightStyle.Trim`) that make this reliable; earlier Compose versions have line-height-scaling failures that the design system should test for explicitly.

### React Native — bridge or accept the gap

React Native ships without native Dynamic Type integration. Without a bridge module, RN typography stays at the developer-specified size regardless of the user's accessibility settings. This is the largest accessibility gap in the cross-platform mobile story.

The practice's default position: **require a Dynamic Type bridge module for any RN engagement past prototype tier.** Several open-source modules exist (`react-native-dynamic-type`, vendor-specific bridges); the modules are not always well-maintained. The cost of building or commissioning a bridge is meaningful but one-time per engagement.

When the bridge is not available, the design system should ship typography tokens with explicit accessibility-scaling logic (a multiplier read from `AccessibilityInfo.getRecommendedTimeoutMillis` or similar signal) and document the gap explicitly to the client. The accessibility gap exists either way; the question is whether the practice surfaces it or hides it.

### The cross-platform discipline

The single load-bearing claim: **every typography composite, on every platform, respects the system's text-scaling architecture.** This is non-negotiable for accessibility conformance. The Style Dictionary transforms for each platform encode the discipline; the build fails if a composite produces a fixed-pixel-output on a platform that has a scaling architecture.

This extends 14-accessibility's text-scaling architecture and 16-mobile-accessibility-implementation's per-platform Dynamic Type / sp treatment into the typography token layer specifically. **The token pipeline is the enforcement mechanism for the architectural commitment.**

---

## AI-readable typography descriptions

The 2026 reality: AI coding agents reach for typography tokens by name and description. The visual difference between `heading/large` and `heading/xl` may be 4 points of size and 50 units of weight; an AI agent cannot infer the intended hierarchy from the values alone. **Typography tokens benefit more from AI-readable descriptions than any other token category** because the values do not communicate intent.

### The five-field description schema

A token description that gives AI agents (and human consumers) enough to select correctly:

| Field | Content |
|---|---|
| **Purpose** | "Primary heading for marketing landing pages." |
| **Use cases** | "Use for the H1 on hero sections; the page-title slot in marketing layouts." |
| **Hierarchy position** | "Top of the editorial hierarchy; nothing larger than this in normal flow." |
| **Anti-patterns** | "Do not use for long-form body copy. Do not use in dense data tables. Do not use as a button label." |
| **Notes** | "Pairs with `body/large` for marketing introductions. Bridges to iOS `.largeTitle`." |

Five fields is the right scale — fewer leaves room for AI mis-selection; more produces description bloat that nobody reads. The Anti-patterns field is the highest-leverage of the five; the "do not use for X" language is what most reliably prevents AI-generated code from misapplying the token.

### Surfacing the descriptions

The descriptions live in the DTCG `$description` field, which is preserved across the build pipeline and surfaced to AI agents through:

- **Figma MCP** — agents reading a Figma file via the Model Context Protocol receive the typography token descriptions inline with the layer metadata.
- **`AGENTS.md` / `CLAUDE.md`** — the descriptions are surfaced to agents working in the consuming codebase via the project context files.
- **MCP servers exposing the token catalog** — agents can query "what typography token is right for a marketing H1" and receive the matching token with its description.

This extends 15-ai-in-ds's components-as-data argument into the token layer specifically. **The investment in five-field token descriptions is the highest-ROI single piece of AI-readiness work** for a typography token set, and the practice should ship it as a default deliverable on any engagement that has AI-assisted authoring in scope (which by mid-2026 should be most engagements).

---

## Failure modes

- **Composite typography tokens shipped to runtime instead of flattened.** A bundled `font-family / size / weight / line-height` class breaks the moment one sub-property needs to vary independently (responsive line-height, locale-specific letter-spacing). Flatten at the build pipeline.
- **`vw`-only preferred values in fluid type.** Fails the WCAG 1.4.4 text-resize requirement under user zoom. Always include a `rem` component.
- **Single ratio across the whole type scale.** Captions too small or headlines too small, depending on the ratio choice. Use the display pivot.
- **Dimensional line-height (`24px`) instead of unit-less (`1.5`).** Collapses or explodes when font-size changes. Unit-less in every case the system allows.
- **Variable fonts without a named-instance ladder.** Consumers reach for arbitrary weight values (`437`, `462`, `503`); typographic identity fragments. Lock the ladder.
- **`opsz` axis ignored.** Display text loses the contrast and finesse the typeface designer intended; small text loses legibility. `font-optical-sizing: auto` as a global default.
- **iOS typography without `relativeTo:`.** Ignores Dynamic Type; fails Apple's HIG and the App Store accessibility expectations. Every composite bridges to a Dynamic Type style.
- **Android typography in `dp` not `sp`.** Ignores the user's text scale. Every font-size token emits `sp`.
- **React Native typography without a Dynamic Type bridge.** Ignores iOS accessibility settings on the RN target. Bridge or document the gap.
- **`text-box-trim` shipped as a load-bearing layout primitive.** Limited Availability as of mid-2026; Firefox blocks. Progressive enhancement only.
- **Locale-aware sizing as separate token files.** Encourages drift; doubles maintenance. Use DTCG modes carrying script-specific values.
- **Vague token descriptions.** "Heading large" tells an AI agent nothing about when to use it. Five-field descriptions with explicit anti-patterns.

---

## Tensions and open questions

1. **`text-box-trim` Baseline timeline.** The trim story closes the moment Firefox enables the property by default. Until then, the cross-platform alignment-baseline gap persists. Track Firefox releases through 2026.

2. **Single-binary multi-script variable fonts as a default.** The technology works; the tooling around per-script axis curves does not yet handle non-Latin scripts cleanly. Treat as emerging-pattern through 2026; revisit by end of year.

3. **Container queries vs. viewport queries as the system default for fluid type.** The 2026 platform supports both; the field has not converged on which is the system default. The pragmatic answer in this file is "ship both; let component authors choose"; whether one becomes the convergent default is a 2027 question.

4. **APCA-aware typography contrast.** The contrast-validation work in 24 is mostly color-on-color; typography-specific contrast (text on a brand-colored background at small sizes) is an underexplored corner. Worth a focused look in a future engagement.

5. **Optical leading tooling.** The platform supports relative-to-intrinsic-line-gap line-height in some implementations but the tooling around it is thin. Flag as watch-list.

6. **Variable fonts and AI-agent description discipline.** AI agents asked to pick a weight from a variable font's continuous range produce inconsistent results across runs. The named-instance ladder helps; the description fields telling the agent which instance to use for which context help more. Expect this to be a meaningful lift in agent-generated typography quality over the next year.

7. **The Dynamic Type bridge for React Native.** Several open-source modules exist; none has emerged as the convergent answer. The practice should either commit to maintaining its own bridge for RN engagements or commit to a specific upstream module and document the dependency. Currently undecided.

---

## See also

- **02-design-foundations** — the foundation-layer treatment of typography this file extends with the spec-and-platform depth.
- **12-figma-practice** — Figma Variables, modes, and the round-trip story for composite types.
- **13-internationalization-and-rtl** — multi-script typography as an i18n architecture question; this file extends with the script-specific tokenisation depth.
- **14-accessibility** — text-scaling architecture; this file's `clamp()` accessibility rule and the iOS Dynamic Type / Android `sp` / RN-bridge discipline are the implementation layer.
- **16-mobile-accessibility-implementation** — per-platform Dynamic Type / sp / Compose `LineHeightStyle` coverage; this file's typography-specific extension lives on top.
- **15-ai-in-ds** — components-as-data and the AI-readable description discipline; this file applies the same argument to typography tokens specifically with the five-field schema.
- **22-token-architecture-extensions** — DTCG 2025.10 composite-token mechanics, the compute-at-authoring-ship-literals discipline that this file's modular scales and fluid-type triplets implement.
- **24-tokens-at-scale** — the multi-brand portfolio and validation layer this file's typography tokens consume.
- **31-color-systems** — the parallel foundation file. Same 2024–2026-platform-shift treatment, same three-tier architecture, same AI-readable-description discipline applied to color (with `paired_with`, `meaning`, and `contrast_with` as the highest-leverage fields). The architecture, voice, and depth match.

---

*Provenance: DTCG composite typography token shape, the property-level aliasing fidelity gap, and the flatten-at-build discipline are from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-architecture-extensions/` (May 2026) and aligned with 22. The three-tier mandatory stack (atomic primitive / semantic composite / component-tier), the modular-scale-with-display-pivot pattern, the `cqi` container-relative fluid-type encoding alongside `vw`, the `rem`-floor accessibility rule, the primitive triplet encoding for fluid-type tokens, the named-instance ladder for variable fonts, the `opsz`-auto default, the unit-less line-height multiplier discipline, the body-vs-display line-height ratios, the multi-script DS-contract-as-modes-not-files position, the iOS `relativeTo:` discipline, the Android `sp` discipline, the RN Dynamic Type bridge as a non-negotiable for accessibility, and the five-field AI-readable description schema (purpose / use / hierarchy / anti-patterns / notes) are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-typography/` (May 2026). The `text-box-trim` Limited Availability status (Chrome 133+, Safari 18.2+, Edge 133+; Firefox implemented but disabled by default through Firefox 149) is verified against `caniuse.com/mdn-css_properties_text-box-trim` and the MDN reference as of May 2026. Utopia (`utopia.fyi`) and the Type Scale Clamp Generator are referenced from their published documentation. Modular scale ratios and brand-personality mappings are aligned with practitioner writing including Tim Brown (*Modular Scale*) and Robin Rendle. Apple HIG Dynamic Type guidance and Material 3 typography are the per-platform native references.*

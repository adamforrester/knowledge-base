# Typography deepening — type pairing, font loading and performance, brand voice, baseline rhythm, heading-vs-scale

The three deep topics in scope (pairing, loading, brand voice in type) are areas where the field's principles are mature but the *system encoding* of those principles is still hand-rolled. The two lighter topics (vertical rhythm, heading-level-vs-visual-scale) are settled questions the literature keeps re-litigating; the practitioner answer in 2026 is short and confident. This document treats the five sections in order, naming consensus where it exists, decision frameworks where the answer is context-dependent, and tooling gaps where the system has to do work the platform won't.

---

## 1. Type pairing as a system

### The triad and the editorial fourth

The 2026 default for an agency-scale design system is the **display / text / mono triad**, and the field has converged on this shape for reasons that survive scrutiny. Display covers macro-typography — page titles, section headers, marketing heroes, quotation pulls — at sizes where character matters more than reading stamina. Text covers micro-typography — body paragraphs, labels, captions, table cells, form values — at sizes where x-height, counter aperture, and rhythm dominate. Mono covers tabular structure — code, transactional values, log lines, addresses, anywhere column-aligned figures are the readable form — at any size, with the unique constraint that every glyph occupies the same advance width.

The triad's stability is empirical. Audited mature systems (Material, Carbon, Spectrum, Polaris, Primer, Atlassian Design System, Cloudscape, the major platform-vendor systems) all ship at least these three roles. Systems that don't ship a mono role aren't doing tabular UI, and systems that collapse display into text either have no editorial surface or are visually flat. The triad maps cleanly onto the three legibility regimes a multi-surface agency engagement has to cover.

**A fourth face is rare and the bar is high.** The typical fourth role is *editorial* (a face used for long-form reading or for distinct-from-product editorial surfaces — brand magazines, content-marketing properties, published research) or *expressive* (a face used for hero treatments where the system's display face isn't expressive enough on its own — campaign hero copy, illustration-adjacent typography, brand-statement surfaces). The fourth-face cost is real:

- Token volume increases by ~20–40% — every composite that could plausibly use the editorial face needs a sibling.
- Loading cost — each additional family is ~30–80 KB compressed per weight in `woff2`, plus connection setup, plus subsetting overhead.
- Pairing complexity — the third face has to pair coherently with both display and text, multiplying the "does this work together" surface.
- Maintenance — every script-extension, every weight-addition, every brand revision touches three faces instead of two.

The fourth face is justified when (a) the engagement's surfaces are categorically distinct enough that one display face can't serve both (a SaaS dashboard plus an editorial publishing surface plus a marketing site), (b) the brand's voice is genuinely bifurcated (a parent brand serving multiple consumer-facing sub-brands with one strict utilitarian tone and one expressive tone), or (c) a long-form reading surface needs a face purposely tuned for reading and the display face is a pure display cut (no text master, no `opsz` axis low end). Outside those, the fourth is decoration the system pays for forever.

### Contrast of personality, not contrast of category

The classical rule — pair a serif with a sans, or a humanist with a grotesque — is correct as a starting heuristic and wrong as the ending discipline. The 2026 articulation: **pairings work on contrast of personality; they fail on contrast of category that doesn't carry through to personality.**

The failure modes are predictable.

*Categorical collapse.* Two neo-grotesques, even from different foundries, read as "the same typeface, slightly different proportions." Inter at 32pt next to Söhne at 16pt is a hierarchy collapse — the visible difference is size, not voice. The brand-design move (these two are in the same conceptual family, they should harmonise) produces a system that reads as monotonous. Helvetica Now Display next to Helvetica Now Text *can* work because the two cuts are explicitly drawn for different roles and the size pivot is large enough to register; two sibling neo-grotesques without that explicit role-tuning don't.

*Double novelty.* A confident display serif (modulated, high stroke contrast, idiosyncratic terminal treatment) paired with a characterful humanist sans (wide apertures, subtle modulation, calligraphic terminals) — both faces want the eye, neither yields. The result reads as *busy*, not as *expressive*. Reading velocity drops; users perceive friction without identifying its source.

*Personality conflict.* A geometric sans (engineered, precise, mechanical) next to an old-style humanist serif (warm, modulated, organic) — the personalities argue. The brand can't decide whether it's "engineered" or "humane," and the typography enforces the indecision.

*Brittle balance.* A pairing that reads coherently at a single weight pair (display Bold + text Regular) but breaks under variation (display Black + text Light reveals categorical mismatch the medium weights hid). Mature systems test pairings across the full weight matrix, not just the marketing comp.

The discipline that works: **one face does the heavy lifting for brand expression; the other supports.** If the display face is novel — bespoke, expressive, character-forward — the text face is rationalised, neutral, work-horse. If the text face is the brand carrier (rare but legitimate, especially for editorial brands), the display face is structured restraint. Two carriers compete; one carrier and one carrier-of-water cooperate. The contrast that does the work is *role contrast*, encoded as personality, not surface category.

A useful mental model: imagine each face speaking aloud. Display speaks slowly and emphatically; text speaks quickly and quietly. If both faces speak the same way, the user can't tell which voice is the headline.

### Pairing as a token-system decision

The pairing has to live in the token layer or it doesn't survive. The shape:

- **Primitive tier.** `font-family/display`, `font-family/text`, `font-family/mono`. Each maps to a font stack: brand face + script-specific siblings + system fallback + generic-family terminator. The roles are abstract; the *names* of the families are values, not roles.
- **Composite tier.** Every composite typography token (`heading/large`, `body/medium`, `code/inline`, `display/xl`, `caption`) declares which family role it consumes. `display/xl` consumes `font-family/display`. `body/medium` consumes `font-family/text`. `code/inline` consumes `font-family/mono`. The composite's `fontFamily` sub-property aliases to the role primitive; consumers never see the literal family name.
- **Component tier.** Per-component typography overrides exist but are rare; the rule of three from component design applies. A `KpiNumber` component might consume `font-family/mono` for the figure and `font-family/text` for the unit suffix; the system encodes both inheritances at the component-tier composite, not in component CSS.

The architectural pay-off: rebranding a system, swapping the brand face, or adding a multi-script sibling is a primitive-tier change. No composite is rewritten; no component is re-templated. Pairings that aren't tokenised in this shape get rewritten by every consumer that touches them.

**Multi-script fallbacks are the under-named cost.** A brand's display face is, at best, a Latin / Latin-Extended cut; at worst, it's Latin-only. The brand's text face is more likely to ship Cyrillic, Greek, and possibly Hebrew or Arabic. CJK is almost never in the brand face — CJK fonts are categorically distinct (different file format demands, far larger glyph counts, different licensing markets) and almost no Latin foundry ships them. The pairing's *Latin* harmony doesn't carry through localisation.

The token treatment: encode script-specific family overrides explicitly.

```json
"font-family/display/cyrillic": {
  "$type": "fontFamily",
  "$value": ["BrandDisplay", "PT Serif Pro", "Noto Serif", "serif"]
},
"font-family/display/cjk": {
  "$type": "fontFamily",
  "$value": ["Noto Serif CJK SC", "Source Han Serif", "serif"]
}
```

The build pipeline emits per-script `@font-face` rules with `unicode-range` (covered in §2), and the runtime resolves the family per character. The pairing relationship — Latin display matches Latin text — has to be *re-validated for every script* the system ships. Visual cohesion in CJK is its own engagement; do not assume the Latin pairing's harmony transfers.

**Where most systems lose the thread.** The composite-token specification preserves the family alias on round-trip; tools largely don't. Figma Variables (mid-2026) supports font-family variables but not full composite typography tokens with per-script overrides; Tokens Studio has the most complete support and ships custom transforms; Style Dictionary preserves the alias if the platform output accepts it but flattens to the resolved value for native platforms. The practitioner consequence: source-of-truth is the composite with its aliases; the build pipeline emits resolved values per platform; per-platform fidelity has to be tested separately because the alias has been collapsed.

### Variable-font triads and the `opsz` pivot

The variable-font era changed pairing economics. A single variable family with a credible `opsz` (optical size) axis can plausibly cover both display and text — the same DNA, optically retuned for size. Inter's optical-size variant, Roboto Flex's `opsz`, Recursive's blended axes, and a growing list of foundry releases (Editorial New, Söhne Mono variants, IBM Plex's variable cuts) all ship workable display + text from one source.

**Where a single variable family is the right call:**

- **Brand voice doesn't require pairing contrast.** The brand reads coherently as one voice, and the display work is "the text face but bigger and more confident." Most B2B SaaS brands are here — Stripe's Söhne, Linear's Inter Display + Inter, Vercel's Geist + Geist Mono. The display face *is* the text face, optically tuned.
- **Performance budget is binding.** Two families means two sets of weights, two sets of subsets, two licensing transactions. If the engagement's LCP budget can't accommodate two web-font families on the critical path, the architecture has to choose.
- **Localisation is the dominant constraint.** A single variable family with broad script coverage simplifies the multi-script fallback story. Two families multiplies the work.

**Where two families are still warranted:**

- **Brand voice requires real category contrast.** The display face is a serif and the text face is a sans; the display face is geometric and the text face is humanist; the display face is a commissioned bespoke face and the text face is a workhorse. The brand's identity needs the contrast.
- **Display work is *display* work.** A pull-quote, an editorial hero, a brand statement — the display face is doing typographic work that an `opsz`-tuned text face cannot, even at large sizes. A high-contrast modulated serif at 64pt is qualitatively different from a low-contrast neo-grotesque at 64pt; `opsz` retunes proportions, not category.
- **Editorial / publishing surfaces.** Long-form reading benefits from a text face genuinely tuned for reading (humanist sans, transitional serif), and the display surface benefits from a face tuned for display impact. The two are different design briefs.

The `opsz` axis is the system's lever for making the same family read as display vs. text. A typical implementation:

```css
/* Text role — opsz tuned for body sizes */
--font-text-style: "opsz" 16, "wght" 400;
font-variation-settings: var(--font-text-style);

/* Display role — opsz tuned for display sizes */
--font-display-style: "opsz" 96, "wght" 600;
font-variation-settings: var(--font-display-style);
```

The browser's `font-optical-sizing: auto` (the default for variable fonts that declare an `opsz` axis) ties `opsz` to `font-size` automatically — a 14pt text uses `opsz: 14`, a 96pt display uses `opsz: 96`. Manual override via `font-variation-settings` is for cases where the system wants `opsz` to *not* track `font-size` — a marketing surface that uses a small-size composite at large proportions through transform scaling, or a print-derived workflow where the optical size is decoupled from the rendered size.

A subtle gotcha: `font-variation-settings` overrides *all* axes, not just the one named, which means setting `font-variation-settings: "wght" 700` on an element silently disables `font-optical-sizing: auto`. The 2026 practitioner pattern is `font-variation-settings: "wght" var(--wght), "opsz" var(--opsz)` — declare every axis the font supports at every consumer site, or use the higher-level CSS properties (`font-weight`, `font-stretch`, `font-optical-sizing`) and let the browser compose the variation string.

### Tooling gaps in pairing architecture

The discipline is articulable; the tools to enforce it as system constraints are not. The gaps:

- **Figma's font-pairing surface.** Figma's font picker is a flat search; pairings happen by recommendation, not by constraint. There is no equivalent of the colour-step grid Radix encodes — no tool that says "if `font-family/display` is X, only these `font-family/text` values are validated pairings." Designers can pair anything; the validation lives in review.
- **Google Fonts pairing recommendations.** Google's "Pairings" surface in the Fonts UI is co-occurrence-based — what other people use together — not structurally compatibility-based. It will recommend pairings that fail the contrast-of-personality test because lots of people use them. The recommendation has limited signal beyond popularity.
- **Adobe Fonts (Typekit) pairings.** Editorial-led, pairings curated by humans, more reliable than Google's algorithm but limited to Adobe's catalogue and not exposed as constraints in design tools.
- **Fontstand and Fonts In Use.** What practitioners actually use. Fontstand is the rental-licensing surface that lets foundries' production-quality faces be tested at full quality without commissioning; Fonts In Use is the editorial archive of how typefaces have been deployed in real publishing contexts. Both are reference material for human judgement; neither is a system constraint.
- **Practitioner-curated libraries.** Most senior typography-aware DS practitioners maintain a private list of pairings they've validated for production use — a tacit-knowledge artefact, not a tooled artefact. The practice ships this in slide decks and Figma libraries but rarely in code.

The largest gap: **no major tool encodes pairing as a system constraint the way Radix encodes colour steps.** Pairings remain hand-tuned and review-validated. The closest thing is the per-component documentation pattern — declare which composites a component is allowed to consume, and which faces those composites resolve to — but that's downstream of the pairing decision. The pairing itself is a brand-foundation call made once per engagement and inherited.

A second gap: **multi-script pairings are unverified by default.** No tool renders the same composite token across Latin, Cyrillic, CJK, Arabic, and Hebrew side-by-side and reports the pairing's coherence. Practitioners sample manually, and most sample only the locales the launch market uses, with the rest discovered in production by users who notice their language reads differently.

The verification path for the pairing itself stays artisanal — pair candidates rendered side-by-side at the system's actual scales and weight matrix, on the actual surfaces (light mode, dark mode, mobile, desktop, print preview where it matters), with the actual content (sample paragraphs at production line lengths, headlines at production breakpoints, captions at the smallest legible size). The system encodes the *outcome* of that work, not the work itself.

---

## 2. Font loading and performance

### The `font-display` matrix

The `font-display` decision is not a single answer; it is a per-role decision tied to the role's relationship with brand fidelity, layout stability, and the rendering critical path. The 2026 practitioner default has bifurcated, and the bifurcation is stable across the metrics-instrumented industry leaders:

| Role | `font-display` | Reasoning |
|---|---|---|
| Body, UI labels, form values, table cells | `optional` | LCP/INP-protective. Browser gives the font ~100 ms to load (cache or network); if it misses, the fallback font is used permanently for that page render and the web font loads quietly into cache for the next navigation. Eliminates layout shift; minimises blocking. The user sees fallback for one navigation and brand on the second; metrics protect immediately. |
| Display, hero, marketing copy, headings on brand-critical surfaces | `swap` | Brand fidelity is non-negotiable on display surfaces. Browser renders fallback immediately, swaps to web font when ready (no timeout). FOUT is visible; the swap causes layout shift unless paired with metric-matched fallback (below). LCP is protected; CLS is mitigated, not eliminated. |
| Iconography (icon fonts, glyph-bearing brand marks) | `block` | A missing icon glyph rendered as a fallback character (a square, a question mark, a Latin letter) is worse than a brief FOIT. Block waits up to 3 s, then renders fallback. Used only for icon fonts where the alternative is broken-icon UI; the SVG-icon-system answer (see 11/12 / icon brief) is the better path. |
| Anything not on the LCP critical path that the system would prefer to show in brand even at the cost of a slow swap | `swap` (with metric matching) | Default for "show brand whenever it arrives." |
| Anywhere the answer is "I don't know" | `swap` | Conservative default; favours brand over metrics. Practitioners who haven't audited should ship `swap` and instrument before optimising. |

The `optional` value's aggression is under-appreciated. Browsers give the font roughly the duration of a typical paint frame (Chrome and Edge: ~100 ms; Safari and Firefox: similar) and then commit to the fallback. On a cold cache and a slow network, every body composite renders in fallback for the first navigation; only on subsequent navigations (font cached) does the brand face appear. The metrics rationale: late font swaps are CLS events, late paints are LCP events, and a fallback render is faster than waiting. The brand cost: first impression is fallback. The mitigation: ship a metric-matched fallback (below) so the typography reads as deliberate, not as broken.

A common configuration error: `font-display: optional` without metric matching. The user sees fallback at one set of metrics, then refreshes and sees brand at different metrics, and the fallback render reads as a draft. The pattern only works when fallback metrics match brand metrics so the typography looks intentional in either state.

`font-display: fallback` (a 100 ms timeout *plus* a 3 s swap window) is rarely the right answer in 2026; either `optional` (commit to fallback if too slow) or `swap` (commit to brand whenever it arrives) is more decisive. Practitioners who reach for `fallback` are usually trying to avoid making the call.

**Currency note (mid-2026):** `font-display` is universally supported across modern browsers (Chrome, Edge, Safari, Firefox); the values' semantics have been stable since 2020. Verification: caniuse.com/css-font-rendering-controls, MDN's `@font-face/font-display` page. The Core Web Vitals thresholds — LCP ≤ 2.5 s "good," INP ≤ 200 ms "good," CLS ≤ 0.1 "good" — are the 2026 baseline; the field expects INP to remain the primary mover for font-loading optimisation through 2026–2027 as the metric continues to shape Chrome ranking signals.

### Subsetting via `unicode-range`

A complete brand font can carry 1,000–10,000+ glyphs; a typical web product uses 200–500. Shipping the full font is bandwidth wasted on glyphs the page will never render. `unicode-range` partitions the font into subsets and lets the browser fetch only the subsets the page's content needs.

The standard partition:

```css
@font-face {
  font-family: "BrandText";
  src: url("brandtext-latin.woff2") format("woff2");
  unicode-range: U+0000-007F, U+0080-00FF, U+0100-017F;
}
@font-face {
  font-family: "BrandText";
  src: url("brandtext-cyrillic.woff2") format("woff2");
  unicode-range: U+0400-04FF;
}
@font-face {
  font-family: "BrandText";
  src: url("brandtext-greek.woff2") format("woff2");
  unicode-range: U+0370-03FF;
}
/* CJK in larger files; typically further partitioned by frequency */
```

The browser's text shaper checks the page's content against `unicode-range` declarations and fetches only the matching subsets. A page in English fetches `latin.woff2` and nothing else; a page in Russian fetches `cyrillic.woff2`; a multi-language page fetches both lazily as the relevant text appears. The same `font-family` name binds the subsets together; the browser composes the glyphs across files transparently.

**The toolchain.** Subsetting was a manual `pyftsubset` invocation in 2018; in 2026 it's automated.

- **Glyphhanger** — Node-based; spiders the production site, extracts the actual character set used, generates subset definitions. Best for static sites; inadequate for dynamic content where the character set isn't fully discoverable at build time.
- **fonttools / pyftsubset** — Python; the industrial-strength tool. More configurable than Glyphhanger; produces smaller outputs because of finer-grained control over OpenType tables.
- **Fontsource** — Curates subsetted Google Fonts as NPM packages with `@font-face` declarations pre-written and `unicode-range` partitioning baked in. The 2026 default for self-hosted Google Fonts; saves the pipeline work for the common case.
- **Fontaine** — Auto-generates fallback declarations with metric overrides (more on this below).

**The over-subsetting failure mode.** A subset that excludes a character the runtime needs causes the browser to fall back through the `font-family` stack mid-glyph. The result: a single character renders in the fallback font, visibly different from the surrounding text — different proportions, different x-height, different spacing. The typography "breaks" in a way that reads as a bug, not a fallback. Common offenders: typographic punctuation (em-dash U+2014, en-dash U+2013, ellipsis U+2026, smart quotes U+2018-201D), the non-breaking space (U+00A0), currency symbols (U+20AC Euro, U+00A3 Pound), accented characters in user-generated content the build pipeline didn't see.

The defensive shape: include the *Latin Extended* range (U+0080–017F) and the typographic punctuation block (U+2000–206F, U+2070–209F, U+2150–218F) in the base subset by default, even if Glyphhanger says the static site doesn't use them. The bytes are cheap insurance; the alternative is a per-incident bug-fix loop discovered in production.

A second gotcha: **CMS-injected content is subset-blind.** A subsetting pipeline that runs on the static site code and not on the CMS database will miss every special character editorial has used in articles. Real practice: subset against the CMS database export, not just the codebase.

### The `<link rel="preload">` discipline

Preload is a rendering-priority hint that tells the browser to fetch the asset before the renderer would have discovered it. Misused, it produces network contention on the critical path; used correctly, it saves a single round-trip on the LCP-critical font.

**The single rule:** preload only the fonts on the rendering critical path of the LCP element. For most pages, that is one to two font files: the brand text font for above-the-fold body copy if `font-display: swap` is in effect, and possibly the brand display font for the hero heading. Beyond that, every preloaded font is fighting CSS, JS, and images for bandwidth on the critical path.

**What not to preload:**

- Body fonts marked `font-display: optional` — the value declares the font as non-critical to the first paint; preloading contradicts the declaration and introduces metric noise.
- Every weight in a static font family — the page will use one or two weights at first paint; preloading all four wastes ~100–250 KB of critical-path bandwidth.
- Variable fonts with axes the page doesn't use at first paint — preload the variable file as a single asset (it covers all weights in one fetch); don't preload multiple per-weight files.

**The HTML syntax that matters:**

```html
<link
  rel="preload"
  href="/fonts/BrandText-latin.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

- `as="font"` — required. Tells the preload scanner this is a font; without it the preload is downgraded.
- `type="font/woff2"` — required for the scanner to skip non-supporting browsers without a wasted fetch.
- `crossorigin` — *required even for same-origin fonts*. The fetch a preload triggers and the fetch the CSS triggers must use the same CORS mode; CSS-driven font requests are CORS-anonymous by default, so the preload must be too. Without `crossorigin` the browser fetches the font twice — once via preload (uncached because of mode mismatch), once via CSS — and the optimisation backfires into a regression.
- `href` — the absolute or root-relative path. Use the same path the CSS will use; otherwise the cache key differs and the preloaded font isn't reused.

The `crossorigin` requirement is the most-missed detail. The first time a practitioner ships `<link rel="preload" as="font">` without it, the metrics get worse and the cause is not obvious; the network panel shows two requests for the same asset.

**Preload + variable font.** A single preload of the variable file gets the browser the entire weight range in one fetch — typically the right shape. Preload the variable file; let the CSS reference weights through `font-weight` and the variable engine compose them.

### Variable-font byte economics

The break-even between a variable font and multiple static-weight files is straightforward arithmetic but commonly mis-modelled.

**The naive model:** "variable fonts include all weights in one file, so they're always cheaper than shipping multiple statics." Wrong — a variable font carries the full interpolation deltas, which is a fixed overhead independent of how many weights you use.

**The actual break-even:**

- A typical static `woff2` weight: ~30–50 KB compressed. A weight pair (Regular + Bold) is ~60–100 KB.
- A typical `wght`-only variable `woff2`: ~80–120 KB compressed for the same family. The variable file pays a one-time cost for the deltas, then every weight in the range is "free" (the file is a single fetch).
- **Break-even at 2–3 weights.** If the system uses two static weights (Regular + Bold), variable and static are roughly equivalent in bytes. At three weights (Regular + Medium + Bold), variable wins on bytes. At one weight, static wins. At four or more weights, variable wins decisively.

**Per-axis cost is non-linear.** The variable file's overhead depends on which axes ship.

- `wght` only — the cheapest variable axis. Most variable fonts are `wght`-only; the deltas are 1-D and the file is a small overhead over a single static weight.
- `wght` + `wdth` — adds 2-D delta tables. File grows by 30–60% over `wght`-only.
- `wght` + `wdth` + `opsz` — adds another set of masters because optical size is qualitatively different from weight or width (different x-heights, different stroke contrast at the masters); the file grows another 30–80% over the two-axis case. A `wght` + `wdth` + `opsz` variable can be ~250–400 KB, which approaches the cost of shipping 5–6 static weight pairs.
- Custom axes (foundry-specific axes — `MONO`, `slnt` for slant, `GRAD` for grade, `CASL` for casualness in Recursive, `XOPQ`/`XTRA` in Roboto Flex's parametric set) — each axis adds delta tables; the costs compound.

**The decision shape:**

- Use a single-axis (`wght`) variable font when the system uses ≥3 weights. Default for most engagements.
- Use a multi-axis variable font when the additional axes do real design work (`opsz` for true display/text in one family, `wdth` for compressed-display variants, `slnt` for proper italics-as-axis behaviour). Audit the file size; budget accordingly.
- Use static weights when the system is genuinely restrained to 1–2 weights (rare in production systems; more common in marketing-only deployments).

**OpenType feature settings have a secondary cost.** Discretionary ligatures, stylistic sets, alternate figures — each set is glyphs in the font file plus substitution-table machinery. A font shipping 5 stylistic sets and tabular numerals carries ~5–20% more bytes than the same font with the features stripped. The 2026 tooling (`pyftsubset --no-layout-closure`, `fonttools subset --layout-features=...`) lets pipelines strip features the system doesn't use, but the discipline of declaring which features to ship is its own audit. **Wakamai Fondue** (wakamaifondue.com) is the practitioner standard for inspecting which axes and features a `woff2` actually carries; run any incoming font binary through it before committing to feature-dependent tokens.

### CLS mitigation via fallback metric matching

`font-display: swap` causes a layout shift the moment the brand font loads — the brand font's intrinsic line height and glyph proportions differ from the fallback's, the text reflows, and CLS spikes. The 2026 mitigation: **a metric-matched fallback** that occupies the same vertical and horizontal space as the brand font, so the swap is a typographic-texture change, not a layout change.

The mechanism is the `@font-face` descriptors `size-adjust`, `ascent-override`, `descent-override`, and `line-gap-override` applied to a *named local fallback*:

```css
@font-face {
  font-family: "BrandText Fallback";
  src: local("Arial"), local("Helvetica"), local("system-ui");
  size-adjust: 107.4%;
  ascent-override: 92%;
  descent-override: 23%;
  line-gap-override: 0%;
}
@font-face {
  font-family: "BrandText";
  src: url("brandtext.woff2") format("woff2");
  font-display: swap;
}
:root {
  --font-text: "BrandText", "BrandText Fallback", "Arial", sans-serif;
}
```

The chain: `BrandText` is the brand font with `font-display: swap`. `BrandText Fallback` is a *named* `@font-face` whose `src` is the system font (Arial / Helvetica / Liberation Sans), not the brand font. The descriptors warp Arial's metrics to match `BrandText`'s metrics — same x-height, same ascender, same descender, same effective line-height. When the brand face loads and swaps in, the bounding boxes don't change; only the glyph shapes do.

**The four descriptors, in order of impact:**

- `size-adjust` — global glyph scale. Multiplies the rendered size of the fallback. If the brand font's x-height is 510/1000 units and the fallback's is 480/1000, `size-adjust: ~106%` makes the fallback's x-height match. This is the single highest-impact descriptor; everything else is fine-tuning.
- `ascent-override` — the font's ascender height as a percentage of `1em`. Typically the brand font's `OS/2` `usWinAscent` divided by `unitsPerEm`. If the fallback has a different ascender, layout above each line shifts.
- `descent-override` — the descender depth, same calculation. Shifts the baseline; affects line-to-line spacing.
- `line-gap-override` — the leading the font requests for itself. Most modern web fonts ship `line-gap: 0` (rely on CSS `line-height`); align the fallback to the same.

**Tooling.** Calculating these by hand is error-prone. Practitioner tools:

- **Fontaine** (`https://github.com/unjs/fontaine`) — auto-generates the `@font-face` fallback declarations from the brand font's metrics. Nuxt/Vite/Webpack integration. The 2026 standard for the common case.
- **Fontsource** — ships pre-computed metric-matched fallbacks for many open-source fonts; install the package, the fallback is in the bundle.
- **Capsize** (`https://seek-oss.github.io/capsize/`) — extracts metrics from a font file and renders the override CSS. Useful for one-offs and for understanding the calculation before automating.

**The expected CLS impact.** A correctly metric-matched fallback brings text-driven CLS to ~0 across the swap. An unmatched fallback can produce CLS in the 0.05–0.20 range depending on layout — enough to fail the "good" threshold (0.1) and degrade Core Web Vitals scoring. The mitigation is straightforward; the failure to ship it is usually inattention, not technical difficulty.

### Self-hosted vs. third-party hosting

The 2026 baseline: **self-host brand fonts.** Third-party hosting (Google Fonts, Adobe Fonts / Typekit, Monotype's hosted services, smaller foundry-hosted CDNs) is reserved for prototypes, internal tools, and engagements where the brand cost of self-hosting exceeds the fidelity cost of third-party.

The drivers of the shift are three:

**Privacy.** A January 2022 ruling by the Munich Regional Court in Germany held that embedding Google Fonts via the live `fonts.googleapis.com` URL violated GDPR by transmitting visitors' IP addresses to Google without consent. The ruling was narrow (a German court, a particular case, single-defendant) but the legal exposure for EU operators was widely interpreted as material. The practitioner consensus through 2022–2023 was to self-host Google Fonts (which is permitted under Google's licence) and remove the `googleapis.com` linkage. As of mid-2026 the issue has not produced new legal-precedent surface but the migration is essentially complete in EU-facing engagements.

**Performance.** Connecting to a third-party origin requires DNS resolution, TCP handshake, TLS handshake, and HTTP request — all on the critical path before the font can be requested. The CSS file itself is on the third-party origin, so the chain is: first request fetches the CSS (DNS+TCP+TLS+HTTP for `fonts.googleapis.com`), CSS parses to discover the `woff2` URLs (typically on `fonts.gstatic.com`, a different origin requiring its own DNS+TCP+TLS), then the woff2 fetches. Self-hosting collapses this to a single origin (the application origin) with one already-warm connection (HTTP/2 or HTTP/3 multiplexing). The latency saving is typically 100–400 ms on cold loads.

**Stability and provenance.** A self-hosted font binary is version-locked to the deployment. A `googleapis.com` font URL serves whatever Google currently has at that URL — including silently-updated metrics that can shift layout and break metric-matched fallbacks. Self-hosted is the only path to deterministic typography across deploys.

**The toolchain for self-hosting:**

- **Fontsource** (`https://fontsource.org/`) — Google Fonts (and a growing list of other open-source fonts) packaged as NPM dependencies with `@font-face` declarations and subsets pre-written. The 2026 default; install `@fontsource/inter`, import in CSS, done. Version-locked.
- **Foundry-direct licensing.** Independent foundries — Klim Type Foundry, Commercial Type, Grilli Type, Production Type, OH no Type Co., Pangram Pangram — license web `woff2` files directly. The licensee self-hosts; the licence terms govern usage (typically pageview-based or domain-based).
- **Adobe Fonts (Typekit).** Still uses the `use.typekit.net` CDN; self-hosting an Adobe-licensed font is generally not permitted under the Adobe Fonts service. Engagements with Adobe-licensed faces typically license direct from the foundry (where the font is also separately available) or ship Adobe Fonts on third-party with the trade-offs.
- **Monotype Fonts.** Similar third-party-CDN model with paid tiers; self-hosting is licence-dependent.

**What stays third-party:** rapid prototyping, internal tools where the privacy and performance trade-offs are immaterial, engagements where licensing economics make self-hosting infeasible (some enterprise foundry contracts price self-hosting at a premium).

### Font features as authoring decisions

OpenType feature settings — small caps, tabular numerals, oldstyle figures, stylistic sets, discretionary ligatures, contextual alternates — are tokenisable typographic decisions, not consumer-site overrides. The 2026 token shape ships them.

**The CSS surface, in priority order:**

```css
/* Preferred — high-level properties */
font-variant-numeric: tabular-nums;
font-variant-caps: small-caps;
font-variant-ligatures: discretionary-ligatures;
font-variant-numeric: oldstyle-nums;

/* Lower-level — feature tags directly */
font-feature-settings: "tnum", "smcp", "dlig", "onum";

/* Composed — multiple features at once */
font-feature-settings: "tnum" 1, "kern" 1, "liga" 1;
```

The high-level `font-variant-*` properties are preferred for two reasons:

1. **Semantic clarity in the cascade.** `font-variant-numeric: tabular-nums` is self-describing in DevTools, in computed-style inspection, in CSS-in-JS debugging. `font-feature-settings: "tnum"` requires the reader to know the four-letter OpenType tag.
2. **Cascade composition.** `font-feature-settings` is a *single property* — declaring it overrides any previous declaration. A component that sets `font-feature-settings: "ss01"` for a stylistic set and inherits a parent's `font-feature-settings: "tnum"` for tabular numerals will lose the `tnum`. The high-level properties cascade independently — `font-variant-numeric` and `font-variant-caps` and `font-variant-ligatures` don't fight each other.

The practitioner pattern: tokenise feature decisions at the composite level.

```json
"typography/numeric/tabular": {
  "$type": "typography",
  "$value": {
    "fontFamily": "{font-family.text}",
    "fontVariantNumeric": "tabular-nums lining-nums",
    "fontFeatureSettings": "'kern' 1"
  }
},
"typography/numeric/oldstyle-prose": {
  "$type": "typography",
  "$value": {
    "fontFamily": "{font-family.text}",
    "fontVariantNumeric": "oldstyle-nums proportional-nums",
    "fontFeatureSettings": "'kern' 1, 'liga' 1"
  }
}
```

Component briefs reach for the composite that matches the role: a data table consumes `typography/numeric/tabular`; a long-form article body consumes `typography/numeric/oldstyle-prose` (where the brand text face supports oldstyle figures).

**Verification before tokenising.** A feature in the CSS that the font doesn't support is a no-op — silently. Wakamai Fondue is the inspection tool; the audit is "does this font binary actually carry the features the tokens reference?" Subsetted variable fonts are common offenders — a build pipeline that strips layout features to save bytes will silently disable the tokens that depend on them.

A design-tool gap: **Figma's typography surface doesn't fully expose `font-variant-*`.** OpenType features are accessible via the type panel's feature toggles, but the design-token export round-trip can lose them. Tokens Studio handles them; native Figma Variables typography is incomplete on this surface as of mid-2026.

---

## 3. Brand voice in type choices

### Tone as a property of category, but not deterministically

Type categories carry connotations the literate reader assimilates without effort. The convergent-but-not-determinate vocabulary:

- **Humanist sans** — warm, approachable, contemporary, human-centred. Open apertures, calligraphic traces, modulated stroke weight. Frutiger, Open Sans, Lato, Source Sans, Fira Sans, Plex Sans.
- **Neo-grotesque sans** — neutral, modern, institutional, professional. Closed apertures, low stroke contrast, geometric uprightness. Helvetica, Akzidenz Grotesk, Inter, Söhne, Aktiv Grotesk, Neue Haas Grotesk.
- **Geometric sans** — engineered, precise, technical, contemporary. Constructed from circles and lines, low warmth, high regularity. Futura, Avenir, Circular, DM Sans, Geist.
- **Slab serif** — solid, editorial, mechanical, weighty. Heavy bracketed or unbracketed serifs, even stroke weight, structural feel. Rockwell, Roboto Slab, Tiempos Slab, Caslon Slab.
- **Modulated serif** — authoritative, traditional, intellectual, classical. High thick-thin contrast, modulated stroke, calligraphic origins. Garamond, Didot, Bodoni, Tiempos, Source Serif, Editorial New.
- **Monoline / rounded** — casual, friendly, contemporary, soft. Even strokes, rounded terminals, low contrast. Avenir's lighter weights, Nunito, Quicksand, DM Sans (in some readings).

The vocabulary is useful as a starting heuristic and dangerous as a final answer. **The same category can read differently across cuts.** A 1957 neo-grotesque (Akzidenz Grotesk) reads as historical and weighted; a 2017 neo-grotesque (Inter) reads as contemporary and software-y. A humanist sans designed for screens (Source Sans) reads differently from a humanist sans designed for print (Frutiger). The category is a coarse signal; the specific cut is the precise one.

A second caveat: **typographic literacy varies.** The reader who reads typography as voice is the design-aware reader; the typical user reads typography as competence — "does the typography look professional / appropriate / on-brand?" The tone signal that matters in the user's response is "does this typography fit the surface I'm using?" not "what is this typography saying about the brand?" Practitioners over-index on the connotation game and under-index on the fit-for-surface judgement.

The failure modes the connotation discipline does prevent:

- **A legacy financial institution using a rounded humanist sans.** Reads as a fintech startup; signals "we're new" when the brand needs to signal "we've been here for a century." Reader's response: "is this a legitimate bank?"
- **A consumer-facing playful product using an austere neo-grotesque.** Reads as enterprise software; signals "we're professional" when the brand needs to signal "we're approachable." Reader's response: "is this for me?"
- **A heritage editorial brand using a contemporary geometric sans.** Reads as tech blog; signals "we're new" when the brand's value is in "we've been the authority since 1850."
- **A trustworthy government service using a high-contrast modulated serif at body size.** Reads as ornamental; signals "we're decorative" when the brand needs to signal "we're efficient."

The category-signal alignment is the floor, not the ceiling. The right cut within the right category is the systemic decision; choosing Inter when Söhne would have signalled "more deliberate craft" is a real difference even though both are neo-grotesques.

### Voice as a system constraint

The distinction between *brand voice in type as a system concern* and *brand voice in type as art direction* is the distinction between what the system encodes and what the system enables consumers to do. The system carries the voice in the *category-and-cut decision* (the families chosen), the *scale ratio* (the modular scale's interval), the *line-height discipline* (tight-and-tall vs. open-and-low), the *optical size pivot* (where display typography starts and how it differs from text), and the *feature-set defaults* (which OpenType features are on by default). These are foundation decisions, made once, locked into the token tree, inherited by every consumer.

What the system enables consumers to do — *and explicitly does not encode* — is the per-surface art direction:

- A campaign hero with custom kerning on a single word.
- A drop-cap treatment in long-form editorial.
- An expressive headline with negative tracking and stretched height.
- A logotype-adjacent moment where a brand mark is rendered in a non-system face.

These are not failures of the system; they are the surfaces where the system *yields* to art direction because the cost of encoding every campaign-specific moment as a token is higher than the value of the consistency that encoding would buy. The practitioner discipline: the system documents the boundary explicitly. Component-level overrides are acceptable in marketing surfaces; component-level overrides are not acceptable in product UI.

**The line where voice stops being a system concern.** When the typographic decision is per-instance — this hero, this campaign, this article — the system supplies primitives (the families, the weights, the scale, the colour) and the consumer composes. When the typographic decision is per-class — every heading, every body paragraph, every numeric column — the system supplies the composite and the consumer applies it. The system encodes classes, not instances.

A common system-degradation pattern: instance decisions seeping into class definitions. The marketing team adds a campaign-specific tracking value to a hero composite; the value sticks because no one removed it; six months later every page using that composite reads with the campaign-era tracking. The discipline that prevents this: composites version, and instance-specific overrides ship as composition deltas at the consumer site, not as edits to the composite.

### Translating brand brief into typographic tokens

A brand brief like *"approachable but expert, contemporary but grounded, confident but not aggressive"* translates to typographic decisions through a series of compounded choices. The translation is not deterministic — multiple typographic outcomes can satisfy the same brief — but the *space of viable outcomes* is constrained by the brief's vocabulary.

A worked example: "approachable but expert."

- **Text family.** Approachable → humanist sans with open apertures, slight calligraphic warmth (rules out neo-grotesque coldness, rules out geometric precision). Expert → competent humanist with rigour at small sizes, no excessive flourish (rules out the warmest humanist cuts that read as casual). Candidates: Source Sans 3, Inter (the warmer end of neo-grotesque), Söhne Buch, Public Sans, Plex Sans. The expert lean nudges toward the more rigorous-feeling cuts; the approachable lean nudges toward open apertures.
- **Display family.** Expert → modulated serif (intellectual, traditional, authoritative — rules out geometric, rules out slab). Approachable → modern modulated serif rather than historical (rules out Bodoni's coldness, Garamond's archaism). Candidates: Tiempos Headline, Editorial New, Source Serif, Söhne Schmal (a neo-grotesque condensed used as display, the "approachable expert" direction), Reckless. The pairing's contrast (humanist text + modulated serif display) reads as the brief.
- **Mono family.** Lower-stakes; the mono is rarely a brand-voice carrier. Pick a face that reads as system-compatible (JetBrains Mono, IBM Plex Mono, Söhne Mono, Geist Mono) and matches the text family's metrics where possible.
- **Modular scale ratio.** Approachable → moderate ratio (1.200 minor third, 1.250 major third). Expert → enough difference between scale steps for clear hierarchy (rules out too-small ratios; 1.125 minor second reads as undifferentiated). The ratio sets the reading rhythm.
- **Line-height discipline.** Approachable → generous (1.5–1.6 for body; "breathing room"). Expert → controlled (heading line-heights tighter than body, signal of intent).
- **Letter-spacing.** Approachable → default (zero tracking adjustments). Expert → tight at display sizes (negative tracking on display composites; signals deliberateness and craft). Tabular numerals on data tables (signals competence).
- **Optical size pivot.** Display starts at the system's `display/m` or `display/l` step; the text family's `opsz` axis (if available) tracks `font-size`. The brief's "expert" lean justifies the pivot — display-tier work optically distinct from text-tier work.

The token output is a small set of primitives (3 family roles, 9 weight values, 12-step scale, 6 line-height multipliers, 3 letter-spacing values, 4 OpenType feature sets) and a derived composite tier (15–25 composites consuming combinations). The brief is encoded; consumers compose against it.

A useful reference: **the same brief can be satisfied by multiple plausible typographic outcomes.** The translation is not a pure function. The practitioner's job is to pick a viable outcome and defend it against the brief's vocabulary, not to find *the* outcome that satisfies the brief uniquely.

### Display tone vs. text tone — the asymmetric pattern

The most common 2026 pattern: **monumental display + invisible text.** The display face carries 100% of the brand's expressive weight. The text face is neutral, work-horse, optimised for reading.

Examples:

- Stripe — Söhne (display, bespoke, idiosyncratic) + Söhne Mono + a quiet text cut from the same family (or Inter).
- Linear — Inter Display (display) + Inter (text); both from the Inter family but with `opsz` retuning the display cut.
- Vercel / Geist — Geist (display, geometric, contemporary) + Geist Mono + Geist (text, optically retuned).
- Wired — Cooper (display, distinctive, brand-defining) + a clean text cut.
- Bloomberg Businessweek — Neue Haas Grotesk Display (commissioned display revival) + a workhorse text cut + a custom Agate Mono for tabular financial data.

The pattern works because the display face is where the user spends the milliseconds of brand-impression formation, and the text face is where the user spends the minutes of reading. The display face must signal; the text face must disappear. The asymmetry is the point.

**The inverse pattern — neutral display + characterful text — is rare.** It surfaces in long-form editorial, academic publishing, and brands whose value is in reading rather than impression. The display face is restrained because the surface's hero is the article body; the text face carries the brand because the user spends most of their time in it.

**Multi-brand systems push the asymmetry further.** A holding-company system with N consumer brands typically unifies the *text face* (one workhorse, often neo-grotesque, optimised for performance and legibility) and varies the *display face* per brand. The text face carries the system's operational coherence; the display face carries each brand's identity. The token shape:

```json
"font-family/text": { "$value": ["Inter", "system-ui", "sans-serif"] },
"font-family/display/brand-a": { "$value": ["BrandA Display", "Söhne", "sans-serif"] },
"font-family/display/brand-b": { "$value": ["BrandB Editorial", "Tiempos Headline", "serif"] },
"font-family/display/brand-c": { "$value": ["BrandC Sans", "Inter Display", "sans-serif"] }
```

The semantic composites resolve `display/xl` to whichever brand-specific display family is active. The text face is invariant across brands. Engagements past three brands almost always settle into this shape; the full-asymmetric (every brand has its own display *and* text) is too expensive to maintain at portfolio scale.

### Type as brand asset vs. type as commodity

The decision matrix:

**Commissioned / bespoke.** The brand commissions a foundry to draw a face specifically for the brand. Cost: typically $80,000–$300,000+ for a 3–5 weight family with web licensing; 6–18 months timeline. Examples: Stripe's Söhne (Klim, originally licensed; now broadly used and identified with Stripe), Wired's Cooper (commissioned revival), Bloomberg Businessweek's Neue Haas Grotesk revival (Commercial Type), Apple's San Francisco (in-house), Google's Roboto (in-house), IBM's Plex (in-house), Netflix's Netflix Sans, Airbnb's Cereal. Reserved for brands where typographic distinctiveness is part of the brand's competitive position and where the budget and horizon support the commitment. The asset compounds — a commissioned face becomes a recognisable brand element decoupled from logo and colour.

**Licensed independent foundry.** The brand licenses an existing face from a respected independent foundry — Klim Type Foundry, Commercial Type, Grilli Type, Production Type, OH no Type Co., Pangram Pangram, Typotheque, Lineto, Dinamo. Cost: typically $5,000–$50,000 for a 2–4 weight family with web licensing on a domain or pageview tier; days to weeks to license. The optimal sweet spot for most agency engagements — the face has craft and distinctiveness; the licensing is tractable; the foundry is a partner for future expansion (script extensions, additional weights, custom alternates).

**Open-source (Google Fonts, Fontsource catalogue).** The brand uses an open-source face. Cost: zero licensing; days to integrate. Examples: Inter, Source Sans, IBM Plex, JetBrains Mono, DM Sans, Geist (Vercel-released, open-source), Public Sans (US government), Plex (IBM-released). Reserved for engagements where the brand's typographic distinctiveness isn't a competitive lever, for low-budget engagements, for internal tooling, and for the text/UI/mono roles in a hybrid setup where the display face is licensed and the rest are open-source.

**The "brand smell" rule.** Relying entirely on commodity Google Fonts for a brand-critical agency engagement signals under-investment in typographic identity. The senior practitioner's read: a brand that hasn't invested in its display face hasn't decided what its typography should say. The exception is engagements where Inter, IBM Plex, or Geist *is* the deliberate choice — these faces have enough craft and recognition that using them is a positive choice, not a default.

**The hybrid pattern — licensed display + open-source text.** The 2026 default for agency-budget engagements. The display face is licensed from an independent foundry (carrying the brand's distinctiveness); the text face is open-source (carrying the workhorse load). The licensing budget is concentrated where it produces brand value; the operational budget covers the rest. Most B2B SaaS brands shipping in 2024–2026 have settled here.

### Where brand voice gets suppressed — the "system green" of typography

Status colours have a property the system protects: a `success` token reads as success regardless of brand. The same property holds in typography for surfaces where comprehension dominates over expression.

**The suppression zones:**

- **Form labels and inputs.** The user is parsing a structured form, not appreciating brand. Labels read as labels; inputs read as inputs. The brand text face carries the labels; no expressive moves; tracking and weight defaults; the user's attention is on the input value.
- **Data tables and tabular data.** The data is the content; the typography is infrastructure. Tabular numerals are mandatory (column alignment); the text face is the system's text face with `font-variant-numeric: tabular-nums`; weight is regular; size is the smallest legibly comfortable. No brand expression.
- **Code blocks and monospace surfaces.** The mono face is rarely a brand asset. JetBrains Mono, IBM Plex Mono, Geist Mono, Söhne Mono, Inconsolata — the field uses a small canon. The mono's job is to preserve column alignment and code legibility; it carries the brand only by metric compatibility with the text face, not by expressive distinction.
- **Microscopic metadata.** Captions, timestamps, version numbers, byline footnotes, helper text under inputs. The text face at the smallest size; no expressive moves; the content is reference, not statement.
- **Tooltips, toast notifications, system messages.** The system is communicating; the user is receiving information. The text face carries the message; brand expression would distract from the communication.
- **Long-form data-dense reading where comprehension dominates.** Financial dashboards, scientific papers, log streams, terminal output. The text face is tuned for reading stamina; the display face appears only at section headers, if at all.

The principle: **brand voice in type is selective, not pervasive.** A system that imposes the brand's expressive typography on every surface degrades both the brand (the expressive moves become wallpaper) and the user (every surface demands the same level of typographic attention). The system's typographic identity is in the *families chosen* and the *scale*; the *expression of those families* varies by surface.

A second principle: **the mono face does not have to be a brand asset.** The system can ship JetBrains Mono or IBM Plex Mono and brand the surfaces around it (color, layout, content) without loss. Custom or commissioned monospace is a luxury, justified only when tabular alignment with the brand text face's metrics requires a custom mono cut (Bloomberg Businessweek's commissioned Agate Mono is the canonical example — drawn specifically to align with their custom Neue Haas Grotesk text cut at the financial-table sizes). For most engagements, a credible open-source mono is the right call.

---

## 4. Vertical rhythm and the baseline grid — where this stands

The strict baseline grid — every line of text, every UI element, every spatial block aligned to a pixel-perfect global rhythm — is **mostly dead as a web enforcement mechanism** in 2026.

The architectural reasons it doesn't survive:

- **Mixed type scales.** A page with `display/xl` at line-height 1.05, `body/medium` at line-height 1.5, `caption` at line-height 1.4, and `code/inline` at line-height 1.2 doesn't align to a single base unit. The browser computes each composite's line-box from its intrinsic line-height; the line-boxes don't share a divisor.
- **Fluid type via `clamp()` and container queries.** A composite whose `font-size` is `clamp(1rem, 2vi, 1.5rem)` has a fluid line-box; the rhythm changes across the viewport. A baseline grid that's exact at 1280 px isn't exact at 1440 px.
- **Differing intrinsic font metrics.** A serif display face and a sans body face have different `OS/2` ascender/descender values; the line-box computation differs. The baseline doesn't align even if line-height multipliers do.
- **Mixed UI elements.** A button with `padding: 0.5em 1em` is a fluid box; an icon at 24×24 is a fixed box; an image at intrinsic dimensions is its own box. None of them align to the typographic baseline.

**Where the baseline grid survives:**

- **Print-derived clients.** Publishing houses, editorial brands, and brand books arrive with InDesign-shaped expectations. The discipline is real in print; the discipline does not transfer to the web. The practitioner's job is to translate — *line-height tokens land at clean multiples of the spatial base unit; the system's vertical rhythm reads as deliberate without enforcing the grid mechanically.*
- **Long-form reading surfaces.** A single body face at a single line-height in a column of text reads as rhythmic if the line-height is tuned to the body's metrics. The discipline is per-component, not global.
- **Design tools.** Figma and similar offer optical baseline-grid snapping at the design-tool layer. Useful for designer alignment review; not enforced in code. The grid in Figma is a visual aid, not a system constraint.

**The 2026 practitioner answer:** *don't enforce a baseline grid in CSS code; do tune line-height tokens per typographic role so they resolve to clean multiples of the system's base spatial unit.*

A worked example: if the spatial base unit is 8 px (a `--space-1: 8px` system), tune body `line-height` so its computed pixel value is a multiple of 8. At `font-size: 16px`, `line-height: 1.5` produces 24 px (3 × 8), which lands. At `font-size: 14px`, `line-height: 1.71` (≈ 24/14) produces 24 px, which also lands. The composite tokens carry these tuned line-height values; the math stays per-composite; the rhythm reads as deliberate without machinery.

**Document the inheritance for print-derived clients.** A short section in the typography documentation explaining "we don't enforce a baseline grid; here's why; here's the rhythm we do enforce" prevents the per-engagement re-litigation. The print client's expectation is reasonable; the discipline doesn't transfer; the substitute discipline (clean-multiple line-heights) is the substitute, not a compromise.

---

## 5. Heading semantics vs. visual scale — where this stands

**The DOM heading level (`<h1>`–`<h6>`) and the visual scale (`display/xl`, `heading/large`, `heading/medium`, etc.) are independent.** This is a settled question; the system's job is to encode the independence and document it.

The DOM level is a structural decision:

- **Accessibility.** Screen readers expose heading structure as a navigable outline. A user who navigates by headings (a common AT pattern) reads the semantic structure of the document. `<h1>` is the page's primary subject; `<h2>`s are sections; `<h3>`s are subsections.
- **SEO.** Search engines parse heading hierarchy to understand document structure. Skipping levels (`<h1>` → `<h3>`) or stuffing headings degrades the signal.
- **Document semantics.** Some HTML parsers and outline-extraction tools rely on heading hierarchy.

The visual scale is a presentation decision:

- **Hierarchy on the page.** Which element is visually prominent. The user's eye lands on the largest text first; the visual scale carries the visible hierarchy.
- **Brand expression.** Display-tier composites carry the brand's display tone; heading-tier composites carry the brand's section tone. The visual scale is where the typography speaks.

**The two are not coupled.** A page can ship an `<h1>` styled with `heading/medium` (visually restrained for a tertiary surface) and an `<h2>` styled with `display/xl` (visually dominant for a marketing section). The semantic structure is one decision; the visual emphasis is another.

**The practitioner pattern in component briefs:**

- Heading components accept a `level` prop (semantic — 1–6, defaults to 2 typically) and a `size` prop (visual — references a typography composite token). The two are decoupled at the API.
- The component documentation surfaces which level/size combinations are appropriate for which contexts (page title, section header, card header, dialog title, etc.). Per-component briefs (Heading, Page Title, Section Header, Card Title, Dialog Header) carry the combinatorics.
- Lint rules and accessibility checks validate the level structure (no skipped levels, exactly one `<h1>` per page where the convention applies); they do not validate the visual size.

**The token-system implication:** the type-scale composites — `display/xl`, `display/l`, `heading/xl` through `heading/s`, `body/large` through `body/small` — are not bound to specific DOM heading levels. They are typographic composites; the consumer applies them to whatever DOM element is structurally correct. Documentation that says "use `heading/large` for `<h2>`" is wrong; documentation that says "use `heading/large` for the visual prominence appropriate to a section subtitle, with the DOM level determined by document structure" is right.

A common system-degradation pattern: composite naming that conflates the two. A `h2` token that resolves to a specific size encourages consumers to bind size to level. The naming discipline: composites are named for visual role (`display/xl`, `heading/large`, `subheading/medium`) and the consumer applies them to the structurally-correct DOM element.

---

## References

Primary sources, dated to mid-2026.

**Specifications**

- W3C CSS Fonts Module Level 4 — https://www.w3.org/TR/css-fonts-4/ (covers `@font-face` descriptors including `size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`)
- W3C CSS Fonts Module Level 5 — https://www.w3.org/TR/css-fonts-5/ (covers `font-format`, `font-tech`, additional `@font-face` features)
- W3C CSS Text Module Level 4 — https://www.w3.org/TR/css-text-4/
- W3C HTML Resource Hints — https://html.spec.whatwg.org/multipage/links.html#link-type-preload
- DTCG Format Module — https://tr.designtokens.org/format/ (typography composite type, modes; spec status mid-2026)

**Performance and rendering**

- web.dev font-loading guides — https://web.dev/articles/font-best-practices, https://web.dev/articles/codelab-preload-web-fonts, https://web.dev/articles/optimize-webfont-loading
- web.dev / Core Web Vitals — https://web.dev/articles/vitals (LCP, INP, CLS thresholds; INP became a Core Web Vital in March 2024)
- HTTP Archive Web Almanac, Fonts chapter — https://almanac.httparchive.org/en/2024/fonts (latest available as of mid-2026; verification path for usage statistics)

**Variable fonts and font features**

- v-fonts.com — variable font catalogue and demo surface
- variable-fonts.dev — practitioner reference
- Wakamai Fondue — https://wakamaifondue.com/ (font feature inspector)
- Glyphhanger — https://github.com/zachleat/glyphhanger
- fonttools / pyftsubset — https://github.com/fonttools/fonttools

**Hosting and tooling**

- Fontsource — https://fontsource.org/ (self-hosted Google Fonts and other open-source fonts as NPM packages)
- Fontaine — https://github.com/unjs/fontaine (auto-generated fallback metric matching)
- Capsize — https://seek-oss.github.io/capsize/ (font metric extraction and override calculation)
- Adobe Fonts (Typekit) — https://fonts.adobe.com/
- Google Fonts — https://fonts.google.com/

**Type pairing references**

- Fonts In Use — https://fontsinuse.com/
- Typewolf — https://www.typewolf.com/
- Fontstand — https://fontstand.com/
- Practical Typography (Matthew Butterick) — https://practicaltypography.com/

**Independent foundries (representative, not exhaustive)**

- Klim Type Foundry — https://klim.co.nz/
- Commercial Type — https://commercialtype.com/
- Grilli Type — https://www.grillitype.com/
- Production Type — https://www.productiontype.com/
- OH no Type Co. — https://ohnotype.co/
- Pangram Pangram — https://pangrampangram.com/
- Typotheque — https://www.typotheque.com/
- Lineto — https://lineto.com/
- Dinamo — https://abcdinamo.com/

**Platform typography references**

- Apple Human Interface Guidelines — Typography — https://developer.apple.com/design/human-interface-guidelines/typography
- Material 3 Typography — https://m3.material.io/styles/typography/overview
- Microsoft Fluent 2 Typography — https://fluent2.microsoft.design/

**Case studies and editorial**

- Bloomberg Businessweek's Neue Haas Grotesk revival — Commercial Type's case writeup at https://commercialtype.com/catalog/neue_haas_grotesk
- Stripe's typography (Söhne) — Klim's case writeup at https://klim.co.nz/blog/sohne-overview/
- Wired's Cooper revival — practitioner coverage; primary sources at the foundry releasing the revival
- IBM Plex — https://www.ibm.com/plex/

**Verification notes.** All "as of mid-2026" claims about browser support and CWV thresholds should be re-checked at caniuse.com and MDN before relying on them. The Munich Regional Court Google Fonts ruling (January 2022) is the load-bearing legal precedent for self-hosting in EU contexts; subsequent rulings may have refined the doctrine and should be checked for engagements with EU exposure. The DTCG specification's typography composite-type treatment continues to evolve; verify against the current spec at tr.designtokens.org/format/ before committing token shapes to the spec's edge cases.

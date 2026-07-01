---
type: practice-area
title: Typography Tokenisation
description: Three-tier mandatory typography stack, brand voice as a system constraint, type pairing as a token-system decision, modular scales with the display pivot, function-named weight ladders (not appearance, not relative comparatives) as the white-label-safe naming, fluid type with clamp() + container queries + rem-floor accessibility rule, variable fonts as tokenisation, font loading and CWV-tuned font-display, metric-matched fallbacks, multi-script as DTCG modes.
tags: [extension, typography, tokens, dtcg, fluid-type, variable-fonts, type-pairing, font-loading, brand-voice]
timestamp: 2026-07-01
---

# 23 — Typography Tokenisation

> Typography is the most under-tokenised foundation in the design systems our practice audits — colors and spacing are usually tokenised; typography is usually a list of styles with one or two ratios behind them and no architecture. The 2024–2026 platform shifts (DTCG 2025.10 composite typography, fluid type with `clamp()`, container queries reaching wide support, variable fonts as first-class, native Dynamic Type / sp / `LineHeightStyle.Trim`, font-loading metrics-instrumented around LCP/INP/CLS, metric-matched fallbacks closing the FOUT gap) have changed what good typography tokenisation looks like. This file is the depth our existing 02-design-foundations and 12-figma-practice files don't reach: the shape of a typography token set, brand voice as a system constraint, type pairing as a token-system decision (not an art-direction one), modular scales with the display pivot, fluid type and container queries, variable fonts as a tokenisation problem, font loading and performance, line-height discipline, multi-script, native platform translation, and the AI-readable description schema typography benefits from most.

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

The spec supports property-level aliasing inside the composite: the `fontSize` sub-property of a composite can reference an atomic `font-size/medium` token. **The 2025.10 spec is explicit about the alias mechanic: property-level references require JSON Pointer syntax (`$ref`) and cannot be expressed using curly-brace syntax.** A composite typography token's `fontFamily` sub-property aliasing an atomic family token must be written `{ "$ref": "#/font-family/text/$value" }`, not `{font-family.text}` — the curly-brace alias works only at the whole-token level. **Most tools as of mid-2026 do not faithfully preserve property-level aliases on round-trip** regardless of which syntax the spec mandates (see 22 for the broader composite-fidelity-gap discussion). The practitioner consequence is the same as for shadow and transition composites: **carry composites as the source-of-truth representation, flatten them at the build pipeline into per-platform atomic outputs that runtime can consume.** The composite is an authoring convenience; the atomic outputs are the runtime contract. (Source: `_source-text/ext-dtcg-format-module.txt`.)

**Composite typography tokens carry voice intent in their `$description`.** The token spec ships the type spec in `$value` (font family, size, line height, weight); the discipline this practice adds is to ship the voice constraint in `$description`. A composite typography token for `text/body/error` carries not just its dimensions but its tone-context binding: *"Used in error states. Voice: calm, never blaming. Tone: direct without alarm. Per voice-and-tone matrix §Error."* The description binds the typography-side voice (the brand-voice-as-immutable-system-constraint framing in §Brand voice in type choices below) to the content-side voice (per 04 §Content as a system layer's voice-and-tone matrix). Both flow from the same matrix; the typography token is the design-side expression, the content token is the content-side expression, both share the same voice intent in their descriptions. This is the tokens-with-descriptions discipline applied at the typography / content boundary. (See 04 §Content as a system layer for the matrix and the content-token catalogue authoring layer.)

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

### Heading semantics vs. visual scale — the type-scale-vs-DOM-tag decoupling

The DOM heading level (`<h1>`–`<h6>`) and the typography composite that styles it are independent decisions. The DOM level is a structural and accessibility decision — it dictates the document outline screen readers expose, and the SEO and outline-extraction tools that parse heading hierarchy. The visual scale is a presentation decision — which typography composite carries the visible hierarchy. **The two are decoupled, and the token system has to encode the decoupling explicitly.**

A page can ship an `<h1>` styled with `heading/medium` (visually restrained for a tertiary surface) and an `<h2>` styled with `display/xl` (visually dominant for a marketing section). The semantic structure satisfies the AT navigation contract; the visual scale carries the eye-tracking hierarchy for sighted users. Both are correct; neither is determined by the other.

The practitioner pattern in component briefs: heading components accept a `level` prop (semantic — `1`–`6`) and a `size` prop (visual — references a typography composite). The two are decoupled at the API. Per-component briefs (Heading, Page Title, Section Header, Card Title, Dialog Header) carry the level/size combinatorics and the contexts each combination is appropriate for. Lint rules and accessibility checks validate the level structure (no skipped levels; one `<h1>` per page where the convention applies); they don't validate the visual size.

The token-naming consequence: the type-scale composites (`display/xl`, `display/l`, `heading/xl` through `heading/s`, `body/large` through `body/small`) **are not bound to specific DOM heading levels and must not be named for them.** A composite called `h2` encourages consumers to bind size to level; a composite called `heading/large` encourages the structural decision the system actually wants. Documentation that says "use `heading/large` for `<h2>`" is wrong; documentation that says "use `heading/large` for the visual prominence appropriate to a section subtitle, with the DOM level determined by document structure" is right.

---

## Brand voice in type choices

Typography is the single largest carrier of brand voice in an interface. Color and spacing express tone at the margin; type expresses it on every surface, in every word, at every size. The system has to encode the voice as a foundation decision, not leave it to consumers to express art-direction-style on every surface — and equally has to know where the system's voice stops and per-instance art direction begins.

### Tone as a property of category — and where the vocabulary breaks

The literature offers a connotation vocabulary the design-aware reader has assimilated:

- **Humanist sans** — warm, approachable, contemporary, human-centred. Open apertures, calligraphic traces, modulated stroke weight. Frutiger, Open Sans, Lato, Source Sans, Fira Sans, Plex Sans.
- **Neo-grotesque sans** — neutral, modern, institutional. Closed apertures, low stroke contrast, geometric uprightness. Helvetica, Akzidenz Grotesk, Inter, Söhne, Aktiv Grotesk, Neue Haas Grotesk.
- **Geometric sans** — engineered, precise, technical. Constructed from circles and lines, low warmth, high regularity. Futura, Avenir, Circular, DM Sans, Geist.
- **Slab serif** — solid, editorial, mechanical, weighty. Heavy bracketed or unbracketed serifs, even stroke weight. Rockwell, Roboto Slab, Tiempos Slab.
- **Modulated serif** — authoritative, traditional, intellectual, classical. High thick-thin contrast, calligraphic origins. Garamond, Didot, Bodoni, Tiempos, Source Serif, Editorial New.
- **Monoline / rounded** — casual, friendly, contemporary, soft. Even strokes, rounded terminals. Nunito, Quicksand, the lighter Avenir cuts.

The vocabulary is a useful starting heuristic and a dangerous final answer. **The same category reads differently across cuts.** A 1957 neo-grotesque (Akzidenz Grotesk) reads as historical and weighted; a 2017 neo-grotesque (Inter) reads as contemporary and software-y. A humanist sans designed for screens (Source Sans) reads differently from a humanist sans designed for print (Frutiger). The category is a coarse signal; the specific cut is the precise one. A second caveat that practitioners over-index away from: **typographic literacy varies, and the typical user reads typography as competence ("does this look professional / appropriate / on-brand?"), not as voice.** The fit-for-surface judgement matters more than the connotation game.

The category-signal alignment is the floor, not the ceiling. The failure modes the discipline does prevent are real and visible: a legacy financial institution using a rounded humanist sans reads as a fintech startup; a consumer-facing playful product using an austere neo-grotesque reads as enterprise software; a heritage editorial brand using a contemporary geometric sans reads as a tech blog. **The typographic category must align with the brand's positioning; the cut within the category is the systemic decision the practice owns.**

### Voice as an immutable system constraint

The system carries the voice in the *category-and-cut decision* (the families chosen), the *scale ratio* (the modular scale's interval), the *line-height discipline* (tight-and-tall vs. open-and-low), the *optical size pivot* (where display typography starts and how it differs from text), and the *feature-set defaults* (which OpenType features are on by default). These are foundation decisions, made once, locked into the token tree, inherited by every consumer. A developer building a card component does not choose a typeface or a weight; they reach for `typography/card-title`, which inherits the system's encoded tone.

The discipline that prevents typographic drift: subjective decisions move out of the component layer and into the foundation token layer. **Brand voice in type ceases to be a system concern when the typographic decision is per-instance** — this hero, this campaign, this article. There the system supplies primitives (the families, the weights, the scale, the colour) and the consumer composes. Where the decision is per-class — every heading, every body paragraph, every numeric column — the system supplies the composite and the consumer applies it. The system encodes classes, not instances.

A common system-degradation pattern: instance decisions seeping into class definitions. The marketing team adds a campaign-specific tracking value to a hero composite; the value sticks because no one removed it; six months later every page using that composite reads with the campaign-era tracking. The discipline that prevents this: composites version, and instance-specific overrides ship as composition deltas at the consumer site, not as edits to the composite.

### Translating brand brief into typographic tokens

A brand brief like *"approachable but expert, contemporary but grounded"* translates to typographic decisions through compounded choices. The translation is not deterministic — multiple typographic outcomes can satisfy the same brief — but the *space of viable outcomes* is constrained by the brief's vocabulary.

A worked example: "approachable but expert."

- **Text family.** Approachable → humanist sans with open apertures and subtle warmth (rules out neo-grotesque coldness, rules out geometric precision). Expert → competent humanist with rigour at small sizes (rules out the warmest cuts that read as casual). Candidates: Source Sans 3, Inter (the warmer end of neo-grotesque), Söhne Buch, Public Sans, Plex Sans.
- **Display family.** Expert → modulated serif (intellectual, authoritative). Approachable → modern modulated serif rather than historical (rules out Bodoni's coldness, Garamond's archaism). Candidates: Tiempos Headline, Editorial New, Source Serif, Reckless.
- **Mono family.** Lower-stakes; the mono is rarely a brand-voice carrier. Pick a credible system-compatible face that aligns metrically with the text family (JetBrains Mono, IBM Plex Mono, Söhne Mono, Geist Mono).
- **Modular scale ratio.** Approachable → moderate ratio (1.200 minor third). Expert → enough difference between scale steps for clear hierarchy (rules out 1.125 minor second's undifferentiation).
- **Line-height discipline.** Approachable → generous body line-height (1.5–1.6). Expert → controlled headings (heading line-heights tighter than body; signals deliberateness).
- **Letter-spacing.** Tight at display sizes (negative tracking on display composites); default at body sizes; tabular numerals on data tables.

The token output is a small set of primitives (3 family roles, 9 weight values, 12-step scale, 6 line-height multipliers, 3 letter-spacing values, 4 OpenType feature sets) and a derived composite tier (15–25 composites). The brief is encoded; consumers compose against it. The same brief can be satisfied by multiple plausible outcomes; the practitioner's job is to pick a viable outcome and defend it against the brief's vocabulary, not to find *the* unique answer.

### Display tone vs. text tone — the asymmetric pattern

The most common 2026 pattern: **monumental display + invisible text.** The display face carries 100% of the brand's expressive weight; the text face is neutral, work-horse, optimised for reading. Examples track the field's leading systems:

- **Stripe** — Söhne (display, bespoke-feel, idiosyncratic) plus Söhne Mono and a quiet text cut.
- **Linear** — Inter Display (display) plus Inter (text); both from the Inter family but with `opsz` retuning the display cut.
- **Vercel / Geist** — Geist (display, geometric, contemporary) plus Geist Mono plus Geist (text, optically retuned).
- **Wired** — Cooper (display, distinctive, brand-defining) plus a clean text cut.
- **Bloomberg Businessweek** — Neue Haas Grotesk Display (commissioned revival) plus a workhorse text cut plus a custom Agate Mono drawn for tabular financial data.

The pattern works because the display face is where the user spends the milliseconds of brand-impression formation, and the text face is where the user spends the minutes of reading. The display face must signal; the text face must disappear. The asymmetry is the point.

The inverse pattern — neutral display plus characterful text — is rare and surfaces in long-form editorial, academic publishing, and brands whose value is in reading rather than impression. **In multi-brand systems, the asymmetry pushes further:** the text face unifies across brands (one workhorse, optimised for performance and legibility), and only the display face varies per brand. The text face carries operational coherence; the display face carries each brand's identity. Engagements past three brands almost always settle here; the full-asymmetric (every brand has its own display *and* text) is too expensive to maintain at portfolio scale and is rarely justified by user-perceived brand differentiation.

### Type as brand asset vs. type as commodity

The decision matrix:

- **Commissioned / bespoke.** A foundry draws a face specifically for the brand. Cost typically $80,000–$300,000+ for a 3–5 weight family with web licensing; 6–18 months timeline. Examples: Stripe's Söhne (Klim, originally licensed and now broadly identified with Stripe), Wired's Cooper revival, Bloomberg Businessweek's Neue Haas Grotesk revival (Commercial Type), Apple's San Francisco, Google's Roboto, IBM's Plex, Netflix Sans, Airbnb Cereal. Reserved for brands where typographic distinctiveness is a competitive position. The asset compounds — a commissioned face becomes a recognisable brand element decoupled from logo and colour.
- **Licensed independent foundry.** The brand licenses an existing face from a respected independent foundry — Klim, Commercial Type, Grilli Type, Production Type, OH no Type Co., Pangram Pangram, Typotheque, Lineto, Dinamo. Cost typically $5,000–$50,000 for a 2–4 weight family on a domain or pageview tier; days to weeks. **The optimal sweet spot for most agency engagements** — the face has craft and distinctiveness; licensing is tractable; the foundry is a partner for future expansion (script extensions, additional weights, custom alternates).
- **Open-source.** Inter, IBM Plex, JetBrains Mono, DM Sans, Geist (Vercel-released), Public Sans (US government), Source Sans. Zero licensing; days to integrate. Reserved for engagements where typographic distinctiveness isn't a competitive lever, for low-budget engagements, for internal tooling, and for the text/UI/mono roles in a hybrid setup where the display face is licensed.

The convergent agency-budget pattern is **licensed display + open-source text.** The display face carries the brand's distinctiveness; the text face carries the workhorse load; the licensing budget concentrates where it produces brand value. Most B2B SaaS brands shipping in 2024–2026 have settled here. **The "brand smell" rule:** relying entirely on commodity Google Fonts for a brand-critical engagement signals under-investment in typographic identity. The senior practitioner's read is that the brand hasn't decided what its typography should say. The exception is engagements where Inter, IBM Plex, or Geist *is* the deliberate choice — these faces have enough craft and recognition that using them is a positive choice, not a default.

### Where brand voice gets suppressed — the "system green" of typography

Status colours have a property the system protects: a `success` token reads as success regardless of brand. The same property holds in typography for surfaces where comprehension dominates over expression. **Brand voice in type is selective, not pervasive.** A system that imposes the brand's expressive typography on every surface degrades both the brand (the expressive moves become wallpaper) and the user (every surface demands the same level of typographic attention).

The suppression zones:

- **Form labels and inputs.** The user is parsing a structured form, not appreciating brand. The text face carries labels at default tracking, default weight, default size. The user's attention is on the input value, not the label's typography.
- **Data tables and tabular data.** Tabular numerals are mandatory for column alignment; the text face is the system's text face with `font-variant-numeric: tabular-nums`; weight is regular; size is the smallest legibly comfortable. No brand expression.
- **Code blocks and monospace surfaces.** The mono face is rarely a brand asset — JetBrains Mono, IBM Plex Mono, Geist Mono, Söhne Mono. The mono's job is column alignment and code legibility; it carries the brand by metric compatibility with the text face, not by expressive distinction. **Custom or commissioned monospace is a luxury** — Bloomberg Businessweek's commissioned Agate Mono (drawn specifically to align metrically with their custom Neue Haas Grotesk text cut at financial-table sizes) is the canonical example, justified only when tabular alignment with the brand text face's metrics requires a custom cut.
- **Microscopic metadata, tooltips, system messages.** The text face at the smallest size; no expressive moves; the content is reference, not statement.
- **Long-form data-dense reading where comprehension dominates.** Financial dashboards, scientific papers, log streams. The text face is tuned for reading stamina; the display face appears only at section headers, if at all.

The principle the system carries forward: the system's typographic identity is in the *families chosen* and the *scale*; the *expression of those families* varies by surface. Most expressive moves live in display and hero contexts; the rest of the system is quiet on purpose.

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

## Type pairing as a system

Pairing typefaces is the most-published topic in typography and the least-tooled. The principles are mature; the *system encoding* of those principles is hand-rolled. The 2026 articulation: **pairing is a token-system decision, not an art-direction decision, and the system has to encode it as such or it doesn't survive contact with consumers.**

### The triad and the editorial fourth

The agency-scale default is the **display / text / mono triad.** Display covers macro-typography — page titles, section headers, marketing heroes, pull quotes — at sizes where character matters more than reading stamina. Text covers micro-typography — body paragraphs, labels, captions, table cells, form values — at sizes where x-height, counter aperture, and rhythm dominate. Mono covers tabular structure — code, transactional values, log lines, addresses, anywhere column-aligned figures are the readable form.

The triad's stability is empirical. Audited mature systems (Material, Carbon, Spectrum, Polaris, Primer, Atlassian, Cloudscape, the major platform-vendor systems) all ship at least these three roles. Systems that don't ship a mono role aren't doing tabular UI; systems that collapse display into text either have no editorial surface or are visually flat. The triad maps onto the three legibility regimes a multi-surface agency engagement has to cover.

A fourth face is rare and the bar is high. The typical fourth role is *editorial* (a face used for long-form reading or for distinct-from-product editorial surfaces — brand magazines, content-marketing properties) or *expressive* (a face used for hero treatments where the system's display face isn't expressive enough on its own — campaign hero copy, illustration-adjacent typography). The fourth-face cost is real: token volume increases by 20–40%, every composite that could plausibly use the editorial face needs a sibling, every additional family is ~30–80 KB compressed per weight in `woff2` plus connection setup, and the third face has to pair coherently with both display and text. The fourth is justified when (a) the engagement's surfaces are categorically distinct enough that one display face can't serve both (a SaaS dashboard plus an editorial publishing surface plus a marketing site), (b) the brand's voice is genuinely bifurcated, or (c) a long-form reading surface needs a face purposely tuned for reading and the display face is a pure display cut with no text master. Outside those, the fourth is decoration the system pays for forever.

### Contrast of personality, not contrast of category

The classical rule — pair a serif with a sans, or a humanist with a grotesque — is correct as a starting heuristic and wrong as the ending discipline. **Pairings work on contrast of personality; they fail on contrast of category that doesn't carry through to personality.**

The failure modes are predictable.

- **Categorical collapse.** Two neo-grotesques, even from different foundries, read as "the same typeface, slightly different proportions." Inter at 32pt next to Söhne at 16pt is a hierarchy collapse — the visible difference is size, not voice. Helvetica Now Display next to Helvetica Now Text *can* work because the cuts are explicitly drawn for different roles and the size pivot is large enough; two sibling neo-grotesques without that explicit role-tuning don't.
- **Double novelty.** A confident display serif (modulated, high stroke contrast, idiosyncratic terminals) paired with a characterful humanist sans (wide apertures, calligraphic terminals) — both faces want the eye, neither yields. The result reads as *busy*, not as *expressive*. Reading velocity drops; users perceive friction without identifying its source.
- **Personality conflict.** A geometric sans (engineered, mechanical) next to an old-style humanist serif (warm, organic) — the personalities argue. The brand can't decide whether it's "engineered" or "humane"; the typography enforces the indecision.
- **Brittle balance.** A pairing that reads coherently at one weight pair (display Bold + text Regular) but breaks under variation (display Black + text Light reveals categorical mismatch the medium weights hid). Mature systems test pairings across the full weight matrix, not just the marketing comp.

The discipline that works: **one face does the heavy lifting for brand expression; the other supports.** If the display face is novel — bespoke, expressive, character-forward — the text face is rationalised, neutral, work-horse. If the text face is the brand carrier (rare but legitimate, especially for editorial brands), the display face is structured restraint. **Two carriers compete; one carrier and one carrier-of-water cooperate.** A useful mental model: imagine each face speaking aloud. Display speaks slowly and emphatically; text speaks quickly and quietly. If both faces speak the same way, the user can't tell which voice is the headline.

### Pairing as a token-system decision

The pairing has to live in the token layer or it doesn't survive. The shape:

- **Primitive tier.** `font-family/display`, `font-family/text`, `font-family/mono`. Each maps to a font stack: brand face plus script-specific siblings plus system fallback plus generic-family terminator. The roles are abstract; the *names* of the families are values, not roles.
- **Composite tier.** Every composite typography token (`heading/large`, `body/medium`, `code/inline`, `display/xl`, `caption`) declares which family role it consumes. `display/xl` consumes `font-family/display`. `body/medium` consumes `font-family/text`. `code/inline` consumes `font-family/mono`. Consumers never see the literal family name.
- **Component tier.** Per-component overrides exist but are rare; the rule of three from component design applies. A `KpiNumber` that consumes `font-family/mono` for the figure and `font-family/text` for the unit suffix encodes both inheritances at the component-tier composite, not in component CSS.

The architectural pay-off: rebranding a system, swapping the brand face, or adding a multi-script sibling is a primitive-tier change. No composite is rewritten; no component is re-templated. Pairings that aren't tokenised in this shape get rewritten by every consumer that touches them.

**Multi-script fallbacks are the under-named cost.** A brand's display face is, at best, a Latin / Latin-Extended cut; at worst, it's Latin-only. The brand's text face is more likely to ship Cyrillic, Greek, and possibly Hebrew or Arabic. CJK is almost never in the brand face — CJK fonts are categorically distinct (different file format demands, far larger glyph counts, different licensing markets) and almost no Latin foundry ships them. **The pairing's *Latin* harmony does not carry through localisation.**

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

The build pipeline emits per-script `@font-face` rules with `unicode-range` (see the font loading section below), and the runtime resolves the family per character. The pairing relationship — Latin display matches Latin text — has to be *re-validated for every script the system ships.* Visual cohesion in CJK is its own engagement; do not assume the Latin pairing's harmony transfers. Google's Noto family (coverage for over 150 scripts) is the routine source for fallback siblings; advanced engagements commission per-script display siblings from foundries that specialise (Latinotype for Latin-American typography; Sandoll for Korean; FontWorks for Japanese).

### Variable-font triads and the `opsz` pivot

The variable-font era changed pairing economics. A single variable family with a credible `opsz` axis can plausibly cover both display and text — the same DNA, optically retuned for size. Inter's optical-size variant, Roboto Flex's `opsz`, Recursive's blended axes, and a growing list of foundry releases (Editorial New, IBM Plex's variable cuts) ship workable display + text from one source.

A single variable family is the right call when:

- **Brand voice doesn't require pairing contrast.** The brand reads as one voice; display work is "the text face but bigger and more confident." Most B2B SaaS brands sit here — Stripe's Söhne, Linear's Inter Display + Inter, Vercel's Geist + Geist Mono.
- **Performance budget is binding.** Two families means two sets of weights, two sets of subsets, two licensing transactions. If the engagement's LCP budget can't accommodate two web-font families on the critical path, the architecture has to choose.
- **Localisation is the dominant constraint.** A single variable family with broad script coverage simplifies the multi-script fallback story.

Two families remain warranted when:

- **Brand voice requires real category contrast.** The display face is a serif and the text face is a sans; the display face is geometric and the text face is humanist; the brand's identity needs the contrast.
- **Display work is *display* work.** A pull-quote, an editorial hero, a brand statement — the display face is doing typographic work that an `opsz`-tuned text face cannot, even at large sizes. A high-contrast modulated serif at 64pt is qualitatively different from a low-contrast neo-grotesque at 64pt; `opsz` retunes proportions, not category.
- **Editorial / publishing surfaces.** Long-form reading benefits from a text face genuinely tuned for reading, and the display surface benefits from a face tuned for display impact. Two different design briefs.

A subtle implementation gotcha: **`font-variation-settings` overrides every axis the font supports, not just the one named.** Setting `font-variation-settings: "wght" 700` on an element silently disables `font-optical-sizing: auto`. The 2026 practitioner pattern is `font-variation-settings: "wght" var(--wght), "opsz" var(--opsz)` declaring every axis at every consumer site, or — preferred — using the higher-level CSS properties (`font-weight`, `font-stretch`, `font-optical-sizing`) and letting the browser compose the variation string. The token system should ship the higher-level form by default; reach for `font-variation-settings` only when the system needs `opsz` decoupled from `font-size` (a marketing surface that uses a small-size composite at large proportions through transform scaling, or a print-derived workflow).

### Tooling gaps in pairing architecture

The discipline is articulable; the tools to enforce it as system constraints are not.

- **Figma's font-pairing surface.** Figma's font picker is a flat search; pairings happen by recommendation, not by constraint. There is no equivalent of the colour-step grid Radix encodes — no tool that says "if `font-family/display` is X, only these `font-family/text` values are validated pairings." Designers can pair anything; validation lives in review.
- **Google Fonts pairing recommendations.** Co-occurrence-based — what other people use together — not structurally compatibility-based. Useful for popular pairings; uninformative for system-design decisions.
- **Adobe Fonts pairings.** Editorial-led, pairings curated by humans, more reliable than Google's algorithm but limited to Adobe's catalogue and not exposed as constraints in design tools.
- **Fontstand and Fonts In Use.** Fontstand is the rental-licensing surface that lets foundries' production-quality faces be tested at full quality without commissioning; Fonts In Use is the editorial archive of how typefaces have been deployed in real publishing contexts. Both are reference material for human judgement; neither is a system constraint.
- **Practitioner-curated libraries.** What senior typography-aware DS practitioners actually use — private, tacit-knowledge artefacts maintained per practice. The closest the practice has to a tooled pairing constraint is the per-component documentation pattern (declare which composites a component is allowed to consume, which faces those composites resolve to), but that's downstream of the pairing decision.

The largest gap: **no major tool encodes pairing as a system constraint the way Radix encodes color steps.** Pairings remain hand-tuned and review-validated. A second gap: **multi-script pairings are unverified by default.** No tool renders the same composite token across Latin, Cyrillic, CJK, Arabic, and Hebrew side-by-side and reports the pairing's coherence. Practitioners sample manually, and most sample only the locales the launch market uses, with the rest discovered in production by users who notice their language reads differently.

The verification path for the pairing itself stays artisanal — pair candidates rendered side-by-side at the system's actual scales and weight matrix, on the actual surfaces (light mode, dark mode, mobile, desktop), with the actual content (sample paragraphs at production line lengths, headlines at production breakpoints, captions at the smallest legible size). The system encodes the *outcome* of that work, not the work itself.

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

**The token system should ship two parallel fluid-type sets — viewport-relative and container-relative — and let component authors choose.** Page-level typography (hero headlines, section titles on marketing pages) usually wants viewport-relative; component-level typography (card titles, sidebar labels) usually wants container-relative. Shipping only viewport-relative locks consumers into the page-as-context model that the platform has moved past. This is the typographic half of a larger division of labour: viewport breakpoints own the page shell, container queries own component responsiveness. The page-shell side — breakpoints, the column grid, gutter/margin — is its own foundation. (See 35-layout-grid-and-breakpoints.)

### When fluid type is the wrong answer

Fluid type is a marketing-tier default, not a universal default. Three contexts where static type is correct:

- **Long-form reading.** Continuous prose benefits from stable line lengths and predictable rhythm; a font-size that shifts continuously across viewport changes interferes with the reader's eye. Articles, documentation, and book-tier reading should use static type scales.
- **Locale-aware sizing.** Arabic, Thai, CJK, and Devanagari each have script-specific sizing requirements that a generic `vw` interpolation cannot encode. Fluid type with a single ratio produces wrong sizes in non-Latin scripts. See the multi-script section below.
- **Accessibility-constrained contexts.** Users who have set a custom font size at the browser level expect that size to be honoured. Fluid type that relies too heavily on viewport units can defeat user preferences — see the accessibility rule below.

### How much to shrink — the mobile↔desktop relationship

`clamp()` answers *how* type interpolates; it doesn't answer *how far* — what the mobile floor should be relative to the desktop ceiling. **The instinct to apply one shrink factor across the scale is wrong, and it's the most common mistake we see.** A uniform factor (mobile = desktop × 0.8) keeps the ratio between steps constant and slides the whole scale down; no mature responsive system does this. The field shrinks **bigger sizes more** — body barely moves, the hero collapses. IBM Carbon's fluid set is the clearest published evidence: its small fluid heading runs ~83–88% of desktop on the narrow viewport, while `fluid-display-04` is **40→176px — the mobile size is 23% of desktop** (Carbon `_styles.scss` / `_scale.scss`, 2026). Utopia reaches the same shape by a different route: two scale ratios, calmer at the min viewport and punchier at the max, so the hierarchy *compresses* on mobile rather than scaling uniformly (Utopia, 2026).

The rule that falls out, in three bands:

- **Body and UI text stay constant.** ~16px web (17pt iOS) at every viewport. This is near-unanimous — Carbon holds productive type fixed, Polaris collapsed its mobile and desktop scales into one after finding the difference was "often a difference of 1px… users often didn't even realise a change happened" (Polaris v10, 2026), and Apple uses the same Dynamic Type sizes on iPhone and iPad (Apple HIG, 2026). Reading comfort tracks reading *distance*, not viewport width, and we sit about the same distance from a phone and a laptop.
- **Headings shrink gently** — roughly one scale step on mobile, and never below ~20px or they stop reading as headings.
- **Display shrinks hard and *progressively*** — the larger the desktop size, the more it gives up, converging to a **~40–48px mobile "hero band"** no matter how large the desktop hero is. The driver is line count: a 160px headline on a 360px phone fits ~3 characters per line and wraps a two-word headline to three lines; at ~48px it fits ~9–11 and reads as a headline. **A 160px desktop hero belongs at ~48px on mobile, not ~120px** — the single error a flat factor guarantees.

**Floors that bound the mobile endpoint:** body ≥ ~16px (below it mobile Safari auto-zooms inputs), any heading ≥ ~20px, and the hard platform floor of 11pt on iOS (Apple HIG). Whatever the floor, the `clamp()` must still survive 200% resize — see the rule below. The practical encoding is a size-dependent curve, not a factor: body static, titles a single step down, display interpolated against the field's published fluid-display curve. (Sourced from the responsive-type research run, `_research/_inbound/2026-06-28-responsive-type-scaling`.)

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

### Naming the weight ladder — function, not appearance

Named instances settle *how many* weights to expose; they leave *what to call them* open, and the conventional answer — the `regular` / `medium` / `semibold` labels used above for familiarity — is quietly wrong for white-label and multi-brand work. **Naming weights by appearance bakes a promise the brand can't keep across a portfolio.** One brand's "bold" is 700, another's is 600, a third ships only two weights and has no "semibold" at all. The name asserts an absolute the font may not contain, and the assertion breaks the moment the family is swapped — the exact event a token system exists to survive.

The relative-comparative escape hatch — `thin` / `thinner`, `thick` / `thicker` — fails differently and worse. It encodes *direction* without an *anchor*: "thicker than what?" has no answer, and nothing in the ladder names the resting body weight, so consumers cannot tell which rung is the default. We have tried it in practice; it reads as confusing because it is genuinely under-determined.

**The discipline that holds: name weights by function, the same way we name colour roles.** A semantic colour token says `action/primary`, not `blue` — it names what the token is *for* and lets each brand map the hue. Weight roles work identically. A small, bounded emphasis ladder — `weight/default` (resting body and UI), `weight/emphasis` (mild lift: strong inline text, active states), `weight/strong` (headings, primary actions), with an optional `weight/subtle` below default — names *purpose*, stays stable across brands, and lets each brand map the role to whatever numeric its font ships. A two-weight brand collapses `emphasis` and `strong` onto one value; a five-weight brand spreads them across the range. The role is the stable contract; the numeric mapping is the brand-variable part. Because the set is small and bounded, t-shirt-style semantic naming is correct here — the same rule that lets radius stay `sm/md/lg` while an open-ended axis like the spacing scale goes numbered (see 02 §Naming principles, and 22 on the numbered-vs-t-shirt decision).

This sits in the three-tier stack exactly where the size scale does: a **reference tier** of numeric primitives (`weight/100`–`900`, the literal axis values the brand ships — the white-label-variable layer), a **semantic tier** of function-named roles aliasing into them, and the composites that consume the roles.

**Weight is an orthogonal axis, not a property of the size token — and naming it by function is what keeps it orthogonal.** Because `weight/strong` is independent of `heading/large`, a composite carries a *default* weight role but any size can be rendered at any weight role without minting a new token. This is what dissolves the "multiple weights per size" problem that otherwise drives a catalogue toward `heading-bold` / `heading-regular` explosion: there is no explosion, because weight is applied, not baked. The composite references the weight *role* — property-level alias where the toolchain preserves it, flattened at build where it doesn't (per the composite-fidelity discipline above) — so re-mapping a brand's weights reflows every composite at once, the same primitive-tier-change payoff the pairing section claims for font families.

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

**Declare the weight-role → named-instance map once.** There is a materialisation trap hiding under that discipline: fonts disagree not only on which numeric a weight is, but on the *spelling* of its named instance — one family ships "Semi Bold", another "Semibold", a third "SemiBold". Figma binds a text style's `fontStyle` as an exact string that must match the family's own instance name, so a spelling hardcoded per component breaks the moment the family is swapped — the same swap the function-named ladder exists to survive. The fix mirrors the role-versus-value split above: **declare the weight-role → named-instance map once, in the brand brief** (the `design.md`-class front door — see 15), and *resolve* it against the font Figma has actually loaded at materialisation time, rather than baking a spelling into each style. The role (`weight/strong`) stays the stable contract; the concrete instance name ("Semi Bold") is a brand-and-font-variable value looked up once, exactly like the numeric axis value. (See 12-figma-practice for the Figma variable-and-style mechanics this resolves against.)

---

## Font loading and performance

Typography is the most layout-critical asset in an interface. How fonts are requested, parsed, and rendered dictates Core Web Vitals — LCP, INP, CLS — and through them the user's first-paint experience and the site's ranking signal in metrics-aware search. The 2026 baseline has stabilised into a small set of decisions the system makes once and inherits across composites.

### The `font-display` matrix

`font-display` is per-role, not global. The decision is tied to each role's relationship with brand fidelity, layout stability, and the rendering critical path:

| Role | `font-display` | Reasoning |
|---|---|---|
| Body, UI labels, form values, table cells | `optional` | LCP/INP-protective. Browser gives the font ~100 ms to load (cache or network); if it misses, the fallback is used permanently for that page render and the web font loads quietly into cache for the next navigation. Eliminates layout shift; minimises blocking. The user sees fallback for one navigation and brand on the second; metrics protect immediately. |
| Display, hero, marketing copy, headings on brand-critical surfaces | `swap` | Brand fidelity is non-negotiable on display surfaces. Browser renders fallback immediately, swaps to web font when ready (no timeout). FOUT is visible; the swap causes layout shift unless paired with a metric-matched fallback (below). LCP is protected; CLS is mitigated, not eliminated. |
| Iconography (icon fonts, glyph-bearing brand marks) | `block` | A missing icon glyph rendered as a fallback character (a square, a question mark, a Latin letter) is worse than a brief FOIT. Block waits up to 3s, then falls back. Used only for icon fonts where the alternative is broken-icon UI; the SVG-icon-system answer is the better path where it's available. |

The `optional` value's aggression is under-appreciated. Browsers give the font roughly the duration of a typical paint frame and then commit to the fallback. On a cold cache and a slow network, every body composite renders in fallback for the first navigation; only on subsequent navigations (font cached) does the brand face appear. The metrics rationale: late font swaps are CLS events, late paints are LCP events, a fallback render is faster than waiting. The brand cost: first impression is fallback. **The mitigation is a metric-matched fallback** (below) so the typography reads as deliberate, not as broken. A common configuration error: `font-display: optional` without metric matching. The user sees fallback at one set of metrics, refreshes and sees brand at different metrics, and the fallback render reads as a draft. The pattern only works when fallback metrics match brand metrics so the typography looks intentional in either state.

`font-display: fallback` (a 100 ms timeout *plus* a 3-second swap window) is rarely the right answer in 2026; either `optional` (commit to fallback if too slow) or `swap` (commit to brand whenever it arrives) is more decisive. Practitioners who reach for `fallback` are usually trying to avoid making the call.

`font-display` is universally supported across modern browsers; the values' semantics have been stable since 2020. Verification: `caniuse.com/css-font-rendering-controls`, MDN's `@font-face/font-display` page. The Core Web Vitals thresholds — LCP ≤ 2.5s "good," INP ≤ 200 ms "good," CLS ≤ 0.1 "good" — are the 2026 baseline; the field expects INP to remain the primary mover for font-loading optimisation through 2026–2027.

### Subsetting via `unicode-range`

A complete brand font carries 1,000–10,000+ glyphs; a typical web product uses 200–500. Shipping the full font is bandwidth wasted on glyphs the page will never render. `unicode-range` partitions the font into subsets and lets the browser fetch only the subsets the page's content needs.

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

The browser's text shaper checks the page's content against `unicode-range` declarations and fetches only the matching subsets. A page in English fetches `latin.woff2` and nothing else; a page in Russian fetches `cyrillic.woff2`; a multi-language page fetches both lazily. The same `font-family` name binds the subsets together; the browser composes the glyphs across files transparently.

The toolchain in 2026:

- **Glyphhanger** — Node-based; spiders the production site, extracts the actual character set used, generates subset definitions. Best for static sites; inadequate for dynamic content where the character set isn't fully discoverable at build time.
- **fonttools / pyftsubset** — Python; the industrial-strength tool. More configurable than Glyphhanger; produces smaller outputs because of finer-grained control over OpenType tables.
- **Fontsource** — curates subsetted Google Fonts as NPM packages with `@font-face` declarations pre-written and `unicode-range` partitioning baked in. The 2026 default for self-hosted Google Fonts; saves the pipeline work for the common case.

**The over-subsetting failure mode.** A subset that excludes a character the runtime needs causes the browser to fall back through the `font-family` stack mid-glyph. A single character renders in the fallback font, visibly different from the surrounding text. Common offenders: typographic punctuation (em-dash U+2014, en-dash U+2013, ellipsis U+2026, smart quotes U+2018-201D), the non-breaking space (U+00A0), currency symbols (U+20AC Euro, U+00A3 Pound), and accented characters in user-generated content the build pipeline didn't see. The defensive shape: include the *Latin Extended* range (U+0080–017F) and the typographic punctuation block (U+2000–206F, U+2070–209F) in the base subset by default, even if the static-site scan says they aren't used. The bytes are cheap insurance; the alternative is per-incident bug-fix loops discovered in production.

A second gotcha: **CMS-injected content is subset-blind.** A subsetting pipeline that runs on the static site code and not on the CMS database will miss every special character editorial has used in articles. Real practice: subset against the CMS database export, not just the codebase.

### `<link rel="preload">` discipline

Preload is a rendering-priority hint that tells the browser to fetch the asset before the renderer would have discovered it. Misused, it produces network contention on the critical path; used correctly, it saves a single round-trip on the LCP-critical font. **The single rule:** preload only the fonts on the rendering critical path of the LCP element. For most pages, that is one to two font files: the brand text font for above-the-fold body copy if `font-display: swap` is in effect, and possibly the brand display font for the hero heading. Beyond that, every preloaded font is fighting CSS, JS, and images for bandwidth on the critical path.

What not to preload: body fonts marked `font-display: optional` (the value declares the font as non-critical to first paint; preloading contradicts the declaration); every weight in a static font family (the page will use one or two weights at first paint; preloading all four wastes ~100–250 KB of critical-path bandwidth); variable fonts beyond a single asset (the variable file covers all weights in one fetch).

The HTML syntax that matters:

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
- `crossorigin` — **required even for same-origin fonts.** The fetch a preload triggers and the fetch the CSS triggers must use the same CORS mode; CSS-driven font requests are CORS-anonymous by default, so the preload must be too. Without `crossorigin` the browser fetches the font twice — once via preload (uncached because of mode mismatch), once via CSS — and the optimisation backfires into a regression.
- `href` — use the same path the CSS will use; otherwise the cache key differs and the preloaded font isn't reused.

The `crossorigin` requirement is the most-missed detail. The first time a practitioner ships `<link rel="preload" as="font">` without it, the metrics get worse and the cause is not obvious; the network panel shows two requests for the same asset.

### Variable-font byte economics

The break-even between a variable font and multiple static-weight files is straightforward arithmetic but commonly mis-modelled. The naive model — "variable fonts include all weights in one file, so they're always cheaper than shipping multiple statics" — is wrong. A variable font carries the full interpolation deltas, which is a fixed overhead independent of how many weights are used.

The actual break-even:

- A typical static `woff2` weight: ~30–50 KB compressed. A weight pair (Regular + Bold) is ~60–100 KB.
- A typical `wght`-only variable `woff2`: ~80–120 KB compressed for the same family. The variable file pays a one-time cost for the deltas; every weight in the range is "free" (a single fetch).
- **Break-even at 2–3 weights.** Two static weights ≈ variable on bytes. Three weights → variable wins. One weight → static wins. Four or more → variable wins decisively.

**Per-axis cost is non-linear.** `wght` only is the cheapest variable axis; the deltas are 1-D and the file is a small overhead over a single static weight. `wght` + `wdth` adds 2-D delta tables — file grows ~30–60% over `wght`-only. `wght` + `wdth` + `opsz` adds another set of masters because optical size is qualitatively different from weight or width (different x-heights, different stroke contrast at the masters); the file grows another ~30–80% over the two-axis case. A `wght` + `wdth` + `opsz` variable can be ~250–400 KB, which approaches the cost of shipping 5–6 static weight pairs. (These ranges are practitioner-observed; verify against the specific font binary via Wakamai Fondue before committing budget figures to client-facing artefacts — see provenance.) Custom axes (foundry-specific axes — `MONO`, `slnt`, `GRAD`, `CASL` in Recursive, `XOPQ`/`XTRA` in Roboto Flex's parametric set) compound the cost; each axis adds delta tables.

The decision shape: **single-axis (`wght`) variable when the system uses ≥3 weights** (the default for most engagements). **Multi-axis variable when the additional axes do real design work** (`opsz` for true display/text in one family, `wdth` for compressed-display variants, `slnt` for proper italics-as-axis behaviour); audit the file size and budget accordingly. **Static weights when the system is genuinely restrained to 1–2 weights** (rare in production systems; more common in marketing-only deployments).

OpenType feature settings have a secondary cost. Discretionary ligatures, stylistic sets, alternate figures — each set is glyphs in the font file plus substitution-table machinery. A font shipping 5 stylistic sets and tabular numerals carries ~5–20% more bytes than the same font with the features stripped. The 2026 tooling (`pyftsubset --no-layout-closure`, `fonttools subset --layout-features=...`) lets pipelines strip features the system doesn't use. **Wakamai Fondue** (`wakamaifondue.com`) is the practitioner standard for inspecting which axes and features a `woff2` actually carries; run any incoming font binary through it before committing to feature-dependent tokens.

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

`BrandText` is the brand font with `font-display: swap`. `BrandText Fallback` is a *named* `@font-face` whose `src` is the system font (Arial / Helvetica / Liberation Sans), not the brand font. The descriptors warp Arial's metrics to match `BrandText`'s metrics — same x-height, same ascender, same descender, same effective line-height. When the brand face loads and swaps in, the bounding boxes don't change; only the glyph shapes do.

The four descriptors, in order of impact:

- `size-adjust` — global glyph scale. Multiplies the rendered size of the fallback. If the brand font's x-height is 510/1000 units and the fallback's is 480/1000, `size-adjust: ~106%` makes the fallback's x-height match. The single highest-impact descriptor; everything else is fine-tuning.
- `ascent-override` — the font's ascender height as a percentage of `1em`. Typically the brand font's `OS/2` `usWinAscent` divided by `unitsPerEm`. If the fallback has a different ascender, layout above each line shifts.
- `descent-override` — the descender depth, same calculation. Shifts the baseline; affects line-to-line spacing.
- `line-gap-override` — the leading the font requests for itself. Most modern web fonts ship `line-gap: 0` (rely on CSS `line-height`); align the fallback to the same.

Tooling: **Fontaine** (`github.com/unjs/fontaine`) auto-generates the `@font-face` fallback declarations from the brand font's metrics, with Nuxt/Vite/Webpack integration; the 2026 standard for the common case. **Fontsource** ships pre-computed metric-matched fallbacks for many open-source fonts; install the package, the fallback is in the bundle. **Capsize** (`seek-oss.github.io/capsize/`) extracts metrics from a font file and renders the override CSS; useful for one-offs and for understanding the calculation before automating. A correctly metric-matched fallback brings text-driven CLS to ~0 across the swap; an unmatched fallback can produce CLS in the 0.05–0.20 range — enough to fail the "good" threshold and degrade Core Web Vitals scoring. The mitigation is straightforward; the failure to ship it is usually inattention, not technical difficulty.

### Self-hosted vs. third-party hosting

The 2026 baseline: **self-host brand fonts.** Third-party hosting (Google Fonts via `fonts.googleapis.com`, Adobe Fonts / Typekit, Monotype's hosted services, smaller foundry-hosted CDNs) is reserved for prototypes, internal tools, and engagements where the brand cost of self-hosting exceeds the fidelity cost of third-party.

Three drivers of the shift:

- **Privacy.** The Landgericht München I (Munich Regional Court I), third civil chamber, ruled on 20 January 2022 (Az. 3 O 17493/20) that a website embedding Google Fonts via the live `fonts.googleapis.com` URL had passed the plaintiff's IP address to Google without authorisation, violating the plaintiff's general right of personality (informational self-determination) under § 823 Abs. 1 BGB. The court awarded €100 in damages and threatened €250,000 per future violation. The ruling explicitly cited self-hosting Google Fonts (permitted under Google's licence) as the remedy. The narrowness matters: it is a single ruling, single defendant, single plaintiff, by a court of first instance — Regional Court rulings do not bind other Landgerichte, and contemporaneous press did not establish appellate or higher-court refinement. The "loading remote Google Fonts is illegal under EU privacy guidelines" framing common in the field overstates this precedent's scope (it is not binding across the EU; it is a single Landgericht ruling with operative weight via threat-of-litigation, not via stare decisis). The legal exposure was concrete enough that the practitioner consensus through 2022–2023 became self-host and remove the `googleapis.com` linkage; as of mid-2026 the migration is essentially complete in EU-facing engagements. (Source: `_source-text/ext-munich-google-fonts-ruling.txt`.)
- **Performance.** Connecting to a third-party origin requires DNS resolution, TCP handshake, TLS handshake, and HTTP request — all on the critical path before the font can be requested. The CSS file is on the third-party origin; the woff2 binaries it references are typically on a different origin (`fonts.gstatic.com`), requiring its own DNS+TCP+TLS chain. Self-hosting collapses this to a single origin (the application origin) with one already-warm connection (HTTP/2 or HTTP/3 multiplexing). The latency saving is typically 100–400 ms on cold loads.
- **Stability and provenance.** A self-hosted font binary is version-locked to the deployment. A `googleapis.com` font URL serves whatever Google currently has at that URL — including silently-updated metrics that can shift layout and break metric-matched fallbacks. Self-hosted is the only path to deterministic typography across deploys.

The toolchain: **Fontsource** (`fontsource.org`) packages Google Fonts (and a growing list of other open-source fonts) as NPM dependencies with `@font-face` declarations and subsets pre-written; install `@fontsource/inter`, import in CSS, done. Version-locked. **Foundry-direct licensing** for licensed faces — Klim, Commercial Type, Grilli Type, Production Type, OH no Type Co., Pangram Pangram all license web `woff2` files directly; the licensee self-hosts under licence terms (typically pageview-based or domain-based). **Adobe Fonts (Typekit)** still uses the `use.typekit.net` CDN; self-hosting an Adobe-licensed font is generally not permitted under the Adobe Fonts service. Engagements with Adobe-licensed faces typically license direct from the foundry (where the font is also separately available) or accept the third-party trade-offs. **Monotype Fonts** — similar third-party-CDN model with paid tiers; self-hosting is licence-dependent.

What stays third-party: rapid prototyping, internal tools where the privacy and performance trade-offs are immaterial, engagements where licensing economics make self-hosting infeasible (some enterprise foundry contracts price self-hosting at a premium).

### Font features as authoring decisions

OpenType feature settings — small caps, tabular numerals, oldstyle figures, stylistic sets, discretionary ligatures, contextual alternates — are tokenisable typographic decisions, not consumer-site overrides. The 2026 token shape ships them.

The CSS surface, in priority order:

```css
/* Preferred — high-level properties */
font-variant-numeric: tabular-nums;
font-variant-caps: small-caps;
font-variant-ligatures: discretionary-ligatures;
font-variant-numeric: oldstyle-nums;

/* Lower-level — feature tags directly */
font-feature-settings: "tnum", "smcp", "dlig", "onum";
```

The high-level `font-variant-*` properties are preferred for two reasons:

1. **Semantic clarity in the cascade.** `font-variant-numeric: tabular-nums` is self-describing in DevTools, in computed-style inspection, in CSS-in-JS debugging. `font-feature-settings: "tnum"` requires the reader to know the four-letter OpenType tag.
2. **Cascade composition.** `font-feature-settings` is a single property — declaring it overrides any previous declaration. A component that sets `font-feature-settings: "ss01"` for a stylistic set and inherits a parent's `font-feature-settings: "tnum"` for tabular numerals will lose the `tnum`. The high-level properties cascade independently — `font-variant-numeric`, `font-variant-caps`, and `font-variant-ligatures` don't fight each other.

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

**Verification before tokenising.** A feature in the CSS that the font doesn't support is a no-op — silently. Wakamai Fondue is the inspection tool; the audit is "does this font binary actually carry the features the tokens reference?" Subsetted variable fonts are common offenders — a build pipeline that strips layout features to save bytes will silently disable the tokens that depend on them. A design-tool gap: **Figma's typography surface doesn't fully expose `font-variant-*`.** OpenType features are accessible via the type panel's feature toggles, but the design-token export round-trip can lose them. Tokens Studio handles them; native Figma Variables typography is incomplete on this surface as of mid-2026.

---

## Line-height, leading, and the discipline of the multiplier

Line-height is the most poorly tokenised typography property in most systems we audit. It is usually a single global value (`1.5`), occasionally a per-token override hardcoded in pixels (`24px`), and never a structured part of the typography scale. The 2026 discipline is straightforward and the practice should adopt it as a default.

### Unit-less multipliers

**Line-height should always be expressed as a unit-less number** (`1.4`, `1.55`, `1.2`). A unit-less multiplier scales with the element's `font-size` automatically. A dimensional line-height (`24px`) does not — it stays fixed when the font-size changes, producing the "collapsing" and "exploding" text failures that are visible across the field.

The CSS spec has always supported unit-less line-height; the field's slow adoption is a habits problem, not a platform problem. The practice's default should be unit-less in every case the system allows.

**The one place this discipline hits a hard wall is Figma.** A Figma Text Style *can* bind line-height to a variable, but only as **pixels** — a bound value is always px, never a unit-less multiplier or a percentage (Figma Plugin API, 2026). Bind a canonical `1.5` and Figma renders 1.5px. The resolution is to keep the token unit-less (correct for code) and let the pipeline materialise a px value *per role and per mode* for Figma to bind — which also means the desktop/mobile size split must ride the size and line-height variables together, since a literal `%` won't move with the size. The same ceiling forces underlined and all-caps roles into *separate* Text Styles, because `textDecoration` and `textCase` aren't bindable at all. (See 12-figma-practice, *Variables vs. Styles, and the code → Figma round-trip*, for the eight bindable text fields and the full set of limits.)

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

### Vertical rhythm and the baseline grid — where this stands

The strict baseline grid — every line of text, every UI element, every spatial block aligned to a pixel-perfect global rhythm — is **mostly dead as a web enforcement mechanism in 2026.** Mixed type scales (display at line-height 1.05 next to body at line-height 1.5 next to caption at line-height 1.4) don't share a divisor; fluid type via `clamp()` and container queries makes the rhythm change across the viewport; differing intrinsic font metrics across families break the alignment even when line-height multipliers agree; mixed UI elements (a button, an icon, an image) don't align to a typographic baseline anyway. The discipline is real in print and does not transfer.

Where it survives: print-derived clients (publishing houses, editorial brands, brand books) arrive with InDesign-shaped expectations; long-form reading surfaces with a single body face at a single line-height read as rhythmic if line-height is tuned to the body's metrics; Figma offers optical baseline-grid snapping at the design-tool layer as a visual aid for designer alignment review (not enforced in code).

**The 2026 practitioner answer:** *don't enforce a baseline grid in CSS code; do tune line-height tokens per typographic role so they resolve to clean multiples of the system's base spatial unit.* If the spatial base unit is 8 px, tune body `line-height` so its computed pixel value lands on a multiple of 8 — at `font-size: 16px`, `line-height: 1.5` produces 24 px (3 × 8); at `font-size: 14px`, `line-height: 1.71` (≈ 24/14) also produces 24 px. The composite tokens carry these tuned values; the math stays per-composite; the rhythm reads as deliberate without machinery. **Document the inheritance for print-derived clients** — a short section in the typography documentation explaining "we don't enforce a baseline grid; here's why; here's the rhythm we do enforce" prevents per-engagement re-litigation. The print client's expectation is reasonable; the discipline doesn't transfer; the substitute discipline (clean-multiple line-heights) is the substitute, not a compromise.

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
- **Categorical-collapse pairings.** Two neo-grotesques from different foundries, paired at different sizes. Reads as one face at two sizes, not as a typographic system. Pair on contrast of personality; don't assume two sibling faces in the same category produce hierarchy.
- **Pairing decisions made in component CSS.** A component author picks `font-family: "BrandSerif"` directly; the token system's pairing logic is bypassed; the multi-script fallback chain is gone. Pairings live in the primitive tier; composites consume role tokens; consumers never see literal family names.
- **Latin pairings assumed to transfer to non-Latin scripts.** A brand display face with no Cyrillic / CJK / Arabic coverage falls through to a generic system font; the carefully tuned Latin harmony evaporates the moment a user sets a non-Latin locale. Encode script-specific family overrides explicitly; validate cohesion per script.
- **`font-variation-settings` overriding every axis.** Setting `font-variation-settings: "wght" 700` silently disables `font-optical-sizing: auto` and any other axis the font supports. Use the higher-level CSS properties (`font-weight`, `font-stretch`, `font-optical-sizing`) and let the browser compose the variation string; reach for `font-variation-settings` only when the system needs an axis decoupled from its high-level property and declare every axis at the consumer site.
- **`font-display: swap` without metric-matched fallback.** The brand font swaps in and the layout shifts; CLS regresses; metrics fail "good." Always pair `swap` with a `size-adjust` / `ascent-override` / `descent-override` / `line-gap-override` fallback declaration via Fontaine, Fontsource, or Capsize.
- **`font-display: optional` without metric-matched fallback.** The user sees the fallback render at one set of metrics, then refreshes and sees the brand at different metrics; the fallback render reads as a draft. The pattern only works when fallback metrics match brand metrics; otherwise revert to `swap` with metric matching or accept the visible quality regression.
- **Preload without `crossorigin`.** The browser fetches the font twice — once via preload (uncached because of CORS-mode mismatch), once via CSS — and the optimisation backfires. Always include `crossorigin` on `<link rel="preload" as="font">`, even for same-origin fonts.
- **Preloading every weight or every variable file.** Preload contention degrades LCP; the preload's purpose is the LCP-critical font, not the entire font payload. Preload one or two files maximum; let the rest load via CSS discovery.
- **Over-subsetting that misses CMS-injected characters.** Editorial inserts an em-dash, a smart quote, an obscure currency symbol; the subset doesn't include it; that single glyph falls through to the system font and breaks the typographic colour mid-paragraph. Include Latin Extended (U+0080–017F) and the typographic punctuation block (U+2000–206F, U+2070–209F) in the base subset by default; subset against the CMS database, not just the codebase.
- **`font-feature-settings` overriding sibling features.** `font-feature-settings` is a single property; declaring it stomps any inherited features. A component setting `font-feature-settings: "ss01"` for a stylistic set loses the inherited `"tnum"` for tabular numerals. Prefer `font-variant-*` properties (`font-variant-numeric`, `font-variant-caps`, `font-variant-ligatures`); they cascade independently.
- **Tokenising features the font binary doesn't carry.** A subsetting pipeline strips discretionary ligatures or stylistic sets to save bytes; the `font-feature-settings: "dlig"` token is silently a no-op. Inspect the binary via Wakamai Fondue before tokenising feature-dependent decisions.
- **Third-party font hosting in EU-facing engagements.** `fonts.googleapis.com` linked from production HTML transmits visitor IPs to Google; the legal exposure post-2022 Munich ruling is material enough that practitioner consensus is to self-host. Use Fontsource for open-source fonts, foundry-direct licensing for licensed fonts, and reserve third-party hosting for prototypes and internal tools.
- **Composite tokens named for DOM heading levels (`h1`, `h2`).** Encourages consumers to bind size to level, defeating the type-scale-vs-DOM-tag decoupling. Name composites for visual role (`heading/large`, `display/xl`); document that the DOM level is determined by document structure, not by the composite chosen.
- **Brand voice imposed on every surface.** Every label, every tooltip, every metadata caption styled with the display face's expressive treatment. The brand voice becomes wallpaper; the user can't tell what's important. Suppress brand voice in form labels, data tables, mono surfaces, microscopic metadata, and long-form data-dense reading; the system's typographic identity is in the families chosen and the scale, not in pervasive expression.

---

## Tensions and open questions

1. **`text-box-trim` Baseline timeline.** The trim story closes the moment Firefox enables the property by default. Until then, the cross-platform alignment-baseline gap persists. Track Firefox releases through 2026.

2. **Single-binary multi-script variable fonts as a default.** The technology works; the tooling around per-script axis curves does not yet handle non-Latin scripts cleanly. Treat as emerging-pattern through 2026; revisit by end of year.

3. **Container queries vs. viewport queries as the system default for fluid type.** The 2026 platform supports both; the field has not converged on which is the system default. The pragmatic answer in this file is "ship both; let component authors choose"; whether one becomes the convergent default is a 2027 question.

4. **APCA-aware typography contrast.** The contrast-validation work in 24 is mostly color-on-color; typography-specific contrast (text on a brand-colored background at small sizes) is an underexplored corner. Worth a focused look in a future engagement.

5. **Optical leading tooling.** The platform supports relative-to-intrinsic-line-gap line-height in some implementations but the tooling around it is thin. Flag as watch-list.

6. **Variable fonts and AI-agent description discipline.** AI agents asked to pick a weight from a variable font's continuous range produce inconsistent results across runs. The named-instance ladder helps; the description fields telling the agent which instance to use for which context help more. Expect this to be a meaningful lift in agent-generated typography quality over the next year.

7. **The Dynamic Type bridge for React Native.** Several open-source modules exist; none has emerged as the convergent answer. The practice should either commit to maintaining its own bridge for RN engagements or commit to a specific upstream module and document the dependency. Currently undecided.

8. **Pairing as a tooled system constraint.** No major design tool encodes type pairing the way Radix encodes color steps — pairings remain hand-tuned and review-validated. The closest the practice has is the per-component documentation pattern (declaring which composites a component is allowed to consume); that's downstream of the pairing decision itself. Whether a tool emerges that treats `font-family/text` × `font-family/display` as a constrained join is a 2027+ question.

9. **Multi-script pairing validation tooling.** No tool renders the same composite token across Latin, Cyrillic, CJK, Arabic, and Hebrew side-by-side and reports the pairing's coherence. Practitioners sample manually, and most sample only the locales the launch market uses. The cohesion gap is discovered in production by users who notice their language reads differently.

10. **`font-display: optional` on body for first-load brand fidelity.** The metrics case for `optional` is strong (LCP/INP/CLS protective); the brand case is weak (first navigation renders in fallback). A metric-matched fallback closes most of the gap, but the practice has not yet committed to `optional` as the body-text default for client-facing engagements where brand is non-negotiable. Watch through 2026–2027 as Core Web Vitals weighting in search and the metric-matching tooling continue to evolve.

11. **Variable-font byte budgets at multi-axis configurations.** Per-axis cost is non-linear and varies materially per typeface. Practitioner-observed ranges (`+wdth` adds 30–60%, `+opsz` adds another 30–80%) are useful for budgeting but not authoritative. Run incoming font binaries through Wakamai Fondue and confirm against the foundry's published metrics before committing budget figures to client-facing artefacts.

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

*Provenance (May 2026): DTCG composite typography token shape, the property-level aliasing fidelity gap, and the flatten-at-build discipline are from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-architecture-extensions/` and aligned with 22. The three-tier mandatory stack (atomic primitive / semantic composite / component-tier), the modular-scale-with-display-pivot pattern, the `cqi` container-relative fluid-type encoding alongside `vw`, the `rem`-floor accessibility rule, the primitive triplet encoding for fluid-type tokens, the named-instance ladder for variable fonts, the `opsz`-auto default, the unit-less line-height multiplier discipline, the body-vs-display line-height ratios, the multi-script DS-contract-as-modes-not-files position, the iOS `relativeTo:` discipline, the Android `sp` discipline, the RN Dynamic Type bridge as a non-negotiable for accessibility, and the five-field AI-readable description schema (purpose / use / hierarchy / anti-patterns / notes) are synthesised from the dual-agent research outputs in `_research/_inbound/2026-05-15-tokens-typography/`. The `text-box-trim` Limited Availability status (Chrome 133+, Safari 18.2+, Edge 133+; Firefox implemented but disabled by default through Firefox 149) is verified against `caniuse.com/mdn-css_properties_text-box-trim` and the MDN reference as of May 2026. Utopia (`utopia.fyi`) and the Type Scale Clamp Generator are referenced from their published documentation. Modular scale ratios and brand-personality mappings are aligned with practitioner writing including Tim Brown (*Modular Scale*) and Robin Rendle. Apple HIG Dynamic Type guidance and Material 3 typography are the per-platform native references.*

*Provenance (June 2026 deepen pass): the brand-voice-in-type, type-pairing-as-a-system, and font-loading-and-performance sections plus the lighter heading-vs-scale and vertical-rhythm-where-this-stands additions are synthesised from the dual-agent research outputs in `_research/_inbound/2026-06-15-typography-deepen/` (claude.md and external-agent.md, both run from `prompt.md`). Convergence was clean across both passes on every load-bearing claim — the triad-with-rare-fourth, the contrast-of-personality-not-category discipline, the categorical-collapse / double-novelty / personality-conflict / brittle-balance failure modes, the one-carrier-one-supporter rule, the primitive/composite/component pairing token shape, the multi-script fallback pattern, the single-vs-two-variable-family decision logic around `opsz`, the no-Radix-equivalent-for-pairing tooling gap (both passes), the `optional` for body / `swap` for display / `block` for icons bifurcation, the metric-matched-fallback discipline with the four `@font-face` descriptors and Fontaine / Capsize / Fontsource toolchain, the `crossorigin` preload requirement, the variable-font 2–3-weight break-even, the per-axis non-linear cost, the `font-feature-settings`-overrides-siblings cascade gotcha (Claude only — the rationale for `font-variant-*` preference), the OpenType-feature audit via Wakamai Fondue, the self-hosted-as-2026-default position with Fontsource and foundry-direct licensing, the monumental-display-plus-invisible-text asymmetric pattern, the unify-text-vary-display multi-brand pattern, the commissioned / licensed / commodity asset matrix with named foundries, the "brand smell" framing, the brand-voice-suppression principle for forms / tables / mono / metadata, the type-scale-vs-DOM-tag decoupling, and the don't-enforce-baseline-grid-in-CSS / tune-line-heights-to-base-unit-multiples discipline.*

*Provenance (June 2026 source-text pass — 09 §1.27 closure): all three primary-source flags are now closed and the watch item produced its first quarterly check. (1) **Munich Regional Court ruling** — captured at `_source-text/ext-munich-google-fonts-ruling.txt` from contemporaneous press (The Register, Jan 2022) and Wikipedia cross-reference; the Self-hosted vs. third-party hosting line is now tightened with the case-number, court chamber, legal basis (§ 823 Abs. 1 BGB), damages (€100 plus €250,000-per-future-violation threat), and the narrowness caveats (single ruling, court of first instance, no appellate refinement established in contemporaneous press). (2) **HTTP Archive `wght`-axis utilisation** — captured at `_source-text/ext-web-almanac-fonts.txt` from the Web Almanac 2024 fonts chapter; the ~60% external-pass figure does not land — actual figures are 99% file-level and 75–78% page-level CSS use. The body text never quoted the figure (footer-only flag), so no inline correction needed; the §1.27e flag closes. (3) **Per-axis variable-font byte cost ranges** — captured at `_source-text/ext-variable-font-axis-byte-costs.txt`; per-axis costs are genuinely per-typeface (master count, hint table size, glyph compounding, compression-friendliness all vary), so no canonical primary-source ranges exist. The existing hedging at line 528 and the Tensions item are correct; the verification procedure (foundry binary → Wakamai Fondue → foundry's published metrics) is preserved as the practice's load-bearing recommendation. Watch item — **DTCG typography composite-type spec** captured at `_source-text/ext-dtcg-format-module.txt` from the Format Module 2025.10 (13 June 2026 preview draft); the property-level-aliasing-via-JSON-Pointer rule is the load-bearing 2025.10 mechanic and is now landed inline in §DTCG composite typography tokens (sub-property references need `$ref`, not `{alias}`). Multi-mode resolution and per-script family overrides remain uncaptured from the spec; watch continues, next check 2026-09-15. Named-cut attributions in the brand-voice section (Stripe / Söhne via Klim, Linear / Inter Display via Rasmus Andersson, Vercel / Geist, Wired / Cooper, Bloomberg Businessweek / Neue Haas Grotesk via Commercial Type, IBM / Plex, Apple / SF, Google / Roboto, Netflix Sans, Airbnb Cereal) are publicly documented brand-typography case studies and aligned with the foundries' published case writeups; verify the specific licensing or commission narrative before quoting in client artefacts.*

You are researching three deepening topics in typography for design
systems for a senior design systems practitioner at a digital agency.
The output is a structured knowledge document that will be folded back
into an existing typography-tokenisation file (23-typography-tokenisation
in the practice's knowledge base), not promoted to a sibling. The
practitioner's existing 23 is strong on tokenisation, modular scales,
fluid type with `clamp()` and container queries, variable fonts as a
tokenisation problem, line-height and the unit-less multiplier
discipline, multi-script and multi-locale typography (with the DTCG
modes pattern), native platform translation (iOS Dynamic Type, Android
`sp`, Compose `LineHeightStyle`, Flutter `MaterialTextScaler`), and the
AI-readable description schema. Three subtopics remain thin in 23 and
warrant a deepening pass: type pairing as a system, font loading and
performance, and brand voice in type choices. Two further topics are
implicit-but-not-named in 23 and warrant a one-paragraph "where this
stands" treatment alongside the three deeper sections: vertical rhythm
/ baseline grid (mostly dead on the web but still asked about by
print-design clients) and heading semantics (H1–H6) vs. visual scale
(the type-scale-vs-DOM-tag decoupling). The 2024–2026 platform shifts
that have reshaped this territory — variable fonts as the default,
`font-display` and the FOIT/FOUT trade matured, subsetting via
unicode-range routine, the `<link rel="preload">` + `font-display:
optional` discipline, INP/LCP-driven font-loading guidance, the
display-vs-text optical-sizing axis (`opsz`) — change what good
practice looks like.

This is not an introductory guide — assume the reader knows what a
design system is, knows tokenisation, knows modular scales, is fluent
in modern CSS typography (`clamp()`, container queries, variable font
axes, `font-display`, `font-feature-settings`), and has read 23. Don't
explain what a variable font is, what `font-display: swap` does, what
FOIT/FOUT means, what humanist vs. grotesque means — explain why the
field has converged on the patterns it has, what the live trade-offs
are, what tooling silently fails to encode, and where the soft side
(brand voice in type) becomes a system concern rather than an
art-direction one.

Research scope — cover all of the following:

1. Type pairing as a system

- Display + text + mono triads as the default agency-engagement
  shape: where each is used, what makes the triad cohere, where adding
  a fourth (an accent / editorial face) is justified.
- The contrast-of-personality discipline — humanist vs. grotesque,
  modulated vs. monoline, neo-grotesque vs. geometric. What pairings
  *fail* and why (two grotesques at similar weights collapsing into
  visual sameness; a strong display serif paired with a humanist sans
  fighting for the same eye); the rules-of-thumb practitioners use
  (one face does the heavy lifting, the other supports; pair on
  contrast of *personality* not contrast of *category*; reserve novelty
  for one face, never two).
- Pairing decisions as token-system decisions, not art-direction
  decisions. Where the pairing lives in the token tree (`fontFamily/
  display`, `fontFamily/text`, `fontFamily/mono`); how the semantic
  composite tier encodes which face each composite uses; what the
  cross-language / multi-script implications are when one face has full
  Cyrillic + CJK fallback support and the other doesn't.
- Variable-font triads — when the display and text axes can come from
  *one* variable font with different `opsz` settings, vs. when two
  separate families are warranted. The `opsz` axis as the
  display-vs-text pivot; what the field has learned about it since
  variable fonts shipped.
- Tooling for pairing: what Figma's font-pairing surface offers and
  doesn't, what Google Fonts' pairing recommendations are worth, what
  practitioners actually use (Fontstand, Fonts In Use, custom
  practitioner libraries). The gap: no major tool encodes pairing as a
  *system constraint* the way Radix encodes color steps; this remains
  hand-tuned territory.

2. Font loading and performance

- The 2024–2026 baseline: what `font-display` value is the practitioner
  default and why (`swap` vs. `optional` vs. `block` — the trade-off
  between LCP/INP, FOIT, and brand fidelity; why `optional` is winning
  for body fonts on metrics-instrumented sites and `swap` for display
  fonts where brand fidelity is non-negotiable on first paint).
- Subsetting strategy — `unicode-range`, the Latin / extended-Latin /
  CJK / icon-glyphs separation, the routine subsetting pipeline
  (glyphhanger / fonttools / Fontsource / build-time subsetting per
  language), the cost of over-subsetting (missing glyphs at runtime).
- `<link rel="preload">` discipline — when to preload (the LCP-blocking
  font, on hero text), when *not* to (every weight in a variable
  family, body fonts that aren't render-blocking), the `crossorigin`
  attribute pitfall, the `as="font"` and `type="font/woff2"`
  requirements.
- Variable-font cost vs. multiple weight files — the variable font's
  fixed file size vs. the static-font-per-weight strategy; the
  break-even (typically 2–3 weights, after which variable wins on
  bytes); the per-axis cost (a font with `wght` + `wdth` + `opsz` axes
  is meaningfully larger than a `wght`-only variable font); the
  font-feature cost (`fontFeatureSettings` toggles add to the file's
  effective complexity).
- The Core Web Vitals connection — LCP, INP, CLS as font-loading
  consequences. The "FOUT-with-`font-display: optional` plus the system
  fallback that stays" pattern Google recommends since 2023. The
  font-fallback-metric-matching discipline (`size-adjust`,
  `ascent-override`, `descent-override`, `line-gap-override`) for
  reducing CLS when the brand font swaps in.
- Self-hosted vs. third-party hosted (Google Fonts, Adobe Fonts /
  Typekit, Monotype Fonts) — the privacy and performance reasons
  practitioners moved to self-hosted post-GDPR, the licence tax for
  enterprise type foundries, the routine practice of self-hosting
  Google Fonts' files locally (Fontsource) for better caching and
  privacy.
- The `font-feature-settings` and `font-variant-*` performance and
  authoring story — when a system ships discretionary ligatures,
  stylistic sets, tabular numerals as token-encoded settings; the
  small-caps and oldstyle-figures decisions; the multi-axis variable
  font's interaction with feature settings.

3. Brand voice in type choices

- How tone is encoded in type-category decisions — humanist sans
  reads as warm and human, grotesque reads as neutral and modern,
  geometric reads as engineered and precise, slab-serif reads as solid
  and editorial, modulated serif reads as authoritative and traditional,
  monoline reads as clean and contemporary. The continuum, the failure
  modes (a "trustworthy bank" using a humanist sans reads as a startup;
  a "playful consumer brand" using a neo-grotesque reads as
  enterprise-software).
- Brand voice as a system constraint — how the system carries a
  brand's voice without micro-managing every text style. The token
  layer encodes the *typographic identity* (the family choices, the
  scale, the line-height discipline, the optical sizing pivot); the
  consumer composes within those constraints. Where "brand voice in
  type" stops being a foundations decision and becomes an
  art-direction one; where the system has to defend its choices.
- The visual-tone vocabulary — refined vs. utilitarian, formal vs.
  casual, classical vs. contemporary, soft vs. precise. How the
  practice translates a brand brief ("we want to read as approachable
  but expert") into typographic decisions, and how those decisions
  survive the token system.
- Display-face tone vs. text-face tone — where they should agree and
  where they should diverge. The pattern of a confident display face
  paired with a quiet, work-horse text face (the "monumental display +
  invisible text" combination); the inverse pattern (a neutral display
  + a more characterful text face) and where it's used; multi-brand
  systems where display tone diverges across brands while text tone
  unifies.
- Type-as-brand-asset vs. type-as-system-asset — the strongest brand
  expressions ship custom or licensed display faces (Wired's
  Cooper, Bloomberg Businessweek's BW Haas Grot, Stripe's Sohne, the
  rest of the field's commissioned-typeface era). The system has to
  carry these as first-class tokens; commodity Google Fonts in a
  brand-critical engagement is a brand smell. When commissioned vs.
  curated-licensed vs. open-source is the right call.
- The "system green" equivalent for type — places where brand voice is
  *suppressed* in service of legibility (form labels, inputs, tabular
  data, code blocks). The system's monospace face is rarely a brand
  expression; it's infrastructure. The system's text face on a
  data-dense surface should be quiet enough that the data leads. Brand
  voice in type is *selective*, not pervasive.

4. Vertical rhythm / baseline grid — where this stands (lighter
   treatment, one-paragraph "where this stands")

- Vertical rhythm / baseline grids are mostly dead as a web
  enforcement mechanism — the variable line-heights of mixed type
  scales, the fluid sizing, the differing intrinsic line-heights of
  different fonts, all break the discipline.
- Where it survives: print-derived clients (publishing, editorial,
  brand books) who arrive with a baseline-grid expectation from
  InDesign; long-form reading surfaces where the rhythm of a single
  body face can be tuned to a grid-like cadence; design-tool snapping
  inside Figma for visual review (not code enforcement).
- The practitioner answer in 2026 — *don't enforce a baseline grid in
  code*; *do* tune line-height per type role to land at clean
  multiples of a base unit (which gives a rhythm-like effect without
  the baseline-grid machinery); *do* document the inheritance for
  print-derived clients and explain why the discipline doesn't carry
  over.

5. Heading semantics (H1–H6) vs. visual scale — where this stands
   (lighter treatment, one-paragraph "where this stands")

- The two are decoupled. The DOM heading level (`<h1>`–`<h6>`) is an
  accessibility / document-structure decision. The visual size is a
  type-scale decision (which composite token does this heading use).
- The practitioner pattern: components and authoring tools accept a
  *level* prop (semantic) and a *size* prop (visual) independently; a
  page can have an `<h1>` styled as `display/large` for the page title
  and an `<h2>` styled as `heading/large` for a section, with the
  visual scale carrying the visible hierarchy and the DOM levels
  carrying the AT navigation.
- The token-system implication: the type-scale composites
  (`heading/xxl`…`heading/s`, `display/xl`…`display/s`) are *not*
  bound to specific DOM heading levels. Documentation should make this
  explicit so component authors don't conflate visual scale with
  semantic level. Per-component briefs (Heading, Section Title, Page
  Header) carry the level/size combinatorics.

Output format: Structured markdown. Use section headings that match
the numbered scope above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather
than declaring a winner. Flag areas where DS tools (Figma Variables,
Style Dictionary, Tokens Studio, Fontsource, Google Fonts, the variable
font tooling chain, code pipelines) have known gaps that practitioners
work around. Where claims depend on current platform state — feature
names, version flags, percentage figures, browser support, INP/LCP
thresholds — date them and note the verification path. Include a
references section linking to primary sources (W3C CSS Fonts /
CSS Text / CSS Color Adjustment, MDN, web.dev font-loading guidance,
Fontsource, the variable-fonts.dev resource, Apple HIG typography,
Material 3 typography, Google Fonts API docs, Practical Typography,
practitioner-blog references for type pairing — Fonts In Use,
Typewolf, the Adobe Fonts editorial — and the leading commissioned-
typeface case studies where relevant).

Depth: Expert audience. Do not explain what a variable font is, what
`font-display: swap` does, what FOIT/FOUT means, what humanist vs.
grotesque means, what `unicode-range` is — explain why the field's
converged on the patterns it has, what the live trade-offs are, what
tooling silently fails to encode, where the soft side (brand voice in
type) becomes a system concern, and where current tooling has gaps.

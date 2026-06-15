# Color systems in design systems — a 2026 practitioner survey

The 2024–2026 platform shifts have moved color from the most-tokenised foundation (every system has a palette) to one of the most-architecturally-contested. OKLCH is now the field-default authoring space, P3 is shipping on most modern displays, the WCAG-2-vs-APCA debate is live and unresolved, Material 3's HCT-anchored dynamic color has redrawn the Android contract, and contrast-aware generated ramps (Tailwind v4, Radix, Leonardo) have raised the bar on what a "color system" is supposed to deliver. The depth a color token system has to encode in 2026 is materially larger than what most agency-built systems currently ship.

This survey treats the eight scope sections in order. Where the field has converged, the convergence is named. Where it hasn't, decision frameworks replace winners.

---

## 1. The shape of a color token system

### Three-tier architecture, applied to color

The same primitive / semantic / component spine that holds for typography and spacing applies to color, but each tier has a sharper definition than for the other foundations.

**Primitive tier** is the ramp itself — the hue scales (`blue/1..12`, `neutral/50..950`, etc.) plus alpha/transparency siblings and any anchor colors (true black, true white, an explicit "natural" warm-neutral if the system has one). Primitives have no semantic intent: `blue/9` is just blue at step 9, not "primary action." The primitive tier is *the* place gamut, color space, and ramp math live.

**Semantic tier** binds intent to primitives via aliasing. The semantic tier is the contract layer — `color/text/primary`, `color/surface/raised`, `color/border/subtle`, `color/action/primary/rest`, `color/status/error`. A consumer authoring a button reaches for `color/action/primary/background/rest`, not for `blue/9`. The semantic tier is also where mode resolution happens (light/dark/brand resolve at the semantic→primitive alias, never at the consumer site).

**Component tier** is per-component overrides where a component genuinely diverges. Used sparingly. A `Badge` whose `background` is heavier than the equivalent `Tag`'s, or a focus ring that uses a contrast-tuned blue distinct from the action blue, are legitimate component-tier tokens. Component-tier color tokens are the smallest of the three sets — typically <10 across an entire system, not per-component. The "rule of three" from component design applies: if three components diverge from semantic, promote a new semantic; if only one does, ship a component-tier override.

**Where boundaries leak.** The most common failure is consumers reaching past semantics for primitives — `var(--blue-9)` directly in component CSS. This breaks theming and breaks branding. The fix is twofold: ship a *complete* semantic tier (consumers shouldn't have to reach past it), and lint primitives out of consumer-facing CSS at build time. Tailwind v4 still ships primitives as utility classes, which the system has to either accept (with discipline) or constrain by an internal preset.

### The naming debate

Three coherent positions, each with a different cost.

**Numeric scales (50, 100, 200…900, 950).** The Tailwind / Material lineage. Conveys ordering by lightness and that's all; the role of step 600 in one ramp is the same as step 600 in another. Couldwell's 50/60/70 variant uses two-digit increments to allow 5% half-steps. Cost: the role of each step is implicit; consumers have to learn the convention (typically "500 is the default brand step, 700 is hover, 200 is subtle background"). When the convention isn't documented, every component re-litigates.

**Step-based with role-baked-in (Radix's 1–12).** Each step has a *named role*: 1 = app background, 2 = subtle background, 3 = UI element background, 4 = hover, 5 = active, 6 = subtle border, 7 = UI border, 8 = hover border, 9 = solid (the saturated step), 10 = hover-solid, 11 = low-contrast text, 12 = high-contrast text. The role is the same across every hue. Consumers learn the *role-step grid* once. Cost: the roles are opinionated and reflect Radix's product-UI assumptions; brand-driven palettes that want, say, a step 13 (super-saturated for marketing surfaces) have to extend the system. The 12-step grid is also low-resolution for fine-tuned typography color where you might want 14–16 distinct text contrasts.

**Semantic-only (Stripe / GOV.UK).** Primitives are private to the build pipeline; consumers see only `color/text/primary`, `color/text/secondary`, `color/surface/default`, etc. The discipline is enforced — you can't reach past semantics because primitives aren't published. Cost: every novel use case has to be enrolled in the semantic tier first; the catalog of semantic tokens grows large (Stripe ships ~80+ semantic color tokens); designers and engineers feel the indirection.

The pragmatic shape: **numeric scale at primitives + role-baked-in step alignment + semantic-tier as the public surface.** Consumers see semantics. Behind the curtain, the primitives use a numeric scale where step N has the same contrast role across every hue (the Radix discipline applied to the math). This gives the role-step alignment Radix bought without forcing the Radix vocabulary on the consumer surface.

### Token volume — the right shape

**Primitives.** A mature 2026 system ships:

- 8–14 hue ramps (neutrals, brand, brand-secondary, plus 4–6 status/accent hues) × 10–12 steps each = 80–170 primitive color tokens.
- A parallel alpha/transparency ramp per hue, or a smaller shared set (8–10 alpha values).
- Optionally a wide-gamut P3 sibling for brand-critical primitives (see §2).

**Semantics.** 30–60 semantic color tokens is the convergent shape.

- Text: 4–6 (`primary`, `secondary`, `subtle`, `disabled`, `inverse`, optionally `link`).
- Surface: 4–8 (`default`, `raised`, `sunken`, `overlay`, `inverse`, plus 1–2 brand-tinted surfaces).
- Border: 3–5 (`subtle`, `default`, `strong`, `focus`, `inverse`).
- Action: 4–6 × states — `primary`, `secondary`, `tertiary`, `destructive`, each with `rest`/`hover`/`pressed`/`disabled`.
- Status: 4 hues (`success`, `warning`, `error`, `info`) × 4–6 roles each (`background`, `border`, `text`, `icon`, `surface-subtle`).

**Components.** <10 across the system, only where divergence is real.

Smaller systems ship 60% of these numbers; brand-heavy editorial systems exceed them. The shape that fails is the one that ships hundreds of semantic tokens trying to anticipate every state of every component — that's component-tier work mistakenly elevated to semantic.

### Color-by-context (Perez-Cruz)

The "15 pinks → 4 contexts" framing is right where the system has multiple background contexts that fundamentally change which colors work. Four contexts in the Perez-Cruz model: default surface, brand-saturated surface, dark/inverse surface, image-overlay surface. Each context has its own usable subset of the palette.

Where the model pays off: editorial / marketing-led systems where brand-saturated heroes, dark hero overlays, and image-backed sections are routine; multi-brand systems where each brand has its own dominant surface; systems with a strong "inverse" mode (dark-on-light header inside a light-on-dark page).

Where it doesn't: product-UI systems with one or two surface contexts (a default app surface and a sunken card surface) — over-engineering that produces tokens for contexts the product never uses.

The rule: enumerate the contexts the *product* actually has before building the context-grouped palette. If three or fewer surfaces dominate the product, a flat semantic tier is enough.

### `color-mix()` and relative color syntax — token-volume reduction

The 2024+ CSS surface lets the system *derive* states from a base color rather than ship every state as a separate token.

A button's hover/pressed/disabled states can be:

```css
--color-action-primary-rest: var(--brand-9);
--color-action-primary-hover: color-mix(in oklch, var(--brand-9), black 8%);
--color-action-primary-pressed: color-mix(in oklch, var(--brand-9), black 16%);
--color-action-primary-disabled: color-mix(in oklch, var(--brand-9), var(--surface) 60%);
```

One source, all states derived. Or with relative color syntax:

```css
--color-action-primary-hover: oklch(from var(--color-action-primary-rest) calc(l - 0.05) c h);
```

The token volume reduction: the system can ship one `rest` semantic per role and derive the rest at runtime. Stripe-class systems with 80+ semantic tokens can collapse to 30–40 if state derivation is committed to.

**Tooling fidelity is the catch.** Style Dictionary doesn't natively preserve `color-mix()` — its build pipeline emits the token's resolved value, not the expression. To preserve runtime composition you have to bypass Style Dictionary's color transforms or treat the `color-mix()` expression as a string token, which surrenders cross-platform translation. The result: most pipelines that ship `color-mix()` do so by writing custom emitters or skipping Style Dictionary's color layer for these tokens. **A practitioner who wants to reduce token volume via `color-mix()` accepts that the build pipeline won't generate the iOS/Android equivalents** — the relative-color logic stays web-only, and platforms get explicit state tokens. (Verification path: Style Dictionary 4.x changelog; mid-2026 status. The community is asking for a `color-mix` transform; not in core as of Q2 2026.)

Relative color syntax has a similar story: well-supported in browsers (Safari/Chrome/Firefox, 2024+), poorly supported in design tools (Figma Variables can express it as a literal string but doesn't *resolve* it for the design canvas as of mid-2026). The design ↔ code parity is broken: the value the engineer sees is not the value the designer authored. Practitioners typically resolve this by computing the derived colors in Figma manually and shipping them as named tokens, accepting the redundancy.

---

## 2. Color spaces — sRGB, P3, OKLCH, HCT

### Why OKLCH became the default for ramp authoring

OKLCH won the authoring war for three reasons.

**Predictable lightness math.** L=0.5 in OKLCH looks roughly 50% perceptually lighter than L=0; L=0.7 looks about 70%. HSL doesn't do this — pure yellow at HSL `60 100% 50%` reads far brighter than pure blue at `240 100% 50%`, even though both are nominally "50% lightness." A designer who wants step 6 of every hue ramp to *look the same lightness* gets it for free in OKLCH and has to fight for it in HSL.

**Chroma-independent hue rotation.** Rotating the hue while holding L and C constant produces a color that reads as "the same color, different hue." HSL hue rotation produces wildly different perceived saturation across the wheel. The implication for ramp generation: a single set of (L, C) pairs can be applied to every hue and produce visually consistent ramps.

**A native CSS function.** `oklch()` ships in stable Safari/Chrome/Firefox since 2023; no library, no preprocessor, no compile step. Authors can write the design tokens in the color space they actually reason in.

**What OKLCH doesn't solve.**

- *It's not a wider gamut by itself.* OKLCH can express colors outside sRGB (and outside P3). Whether those colors *render* depends on the display and the gamut-mapping strategy. An OKLCH ramp that hits step 9 at chroma 0.30 may be in-gamut on P3 displays and clipped to a duller shade on sRGB displays — and the clipping might be perceptually inconsistent across the ramp.
- *Brand fidelity still requires source-color anchoring.* You can't say "OKLCH ramp from this hue" and trust that step 9 matches the brand's signature color. The brand color is a fixed point; the ramp generates *around* it. If the brand color happens to land at step 8 or step 10 in the perceptually-uniform spacing, the ramp has to either compress or stretch to make the brand color land at step 9 — which trades perceptual uniformity for brand fidelity.
- *Per-hue chroma tuning is mandatory for vivid colors.* Pure yellow simply doesn't exist at chroma 0.20 — it's outside every modern gamut. A ramp authored with fixed chroma 0.20 across every hue produces a yellow ramp that's clamped and looks dingy. Practitioners either tune chroma per hue (yellow caps at 0.18, blues go to 0.25) or accept that yellows will look less vivid than other hues on the same step.

### P3 wide-gamut

P3 is roughly 40% wider than sRGB in the green-red axis. Modern displays — every iPhone since the 7, every iPad Pro, every M-series Mac, the latest MacBooks, modern OLED Android flagships, modern Windows OLEDs — support it. As of mid-2026, the practitioner default is to assume P3 on modern phones and tablets, and a mix of sRGB and P3 on desktops.

**When to ship P3.** Brand-critical surfaces — hero backgrounds, accent surfaces, marketing photography color treatment — benefit from P3. The P3 version of a brand red is genuinely more saturated, not just perceptually nudged.

**The CSS path.** Two patterns:

```css
/* Gamut-conditional declaration */
.brand-hero { background: oklch(0.6 0.20 25); }
@supports (color: color(display-p3 1 0 0)) {
  .brand-hero { background: oklch(0.6 0.30 25); }
}

/* Or via @media */
@media (color-gamut: p3) {
  .brand-hero { background: color(display-p3 0.95 0.10 0.20); }
}
```

The token-architecture move: ship two primitive layers — sRGB-clamped values and P3-extended values — and let the build emit per-target CSS. Tokens Studio supports this via mode declarations; Style Dictionary does it via per-platform transforms. Most pipelines as of mid-2026 don't ship P3 by default; the practitioner has to opt in.

**Gamut-mapping strategies** (when an OKLCH color is outside the target gamut):

- *Per-channel clamping* — clamp R, G, B independently to [0, 1]. Worst result: hue shift. A vivid red clamps to a different red. Browsers used to do this; modern browsers do better.
- *Relative colorimetric* — preserve the in-gamut colors exactly, clip the rest. Clean for in-gamut content, harsh at the edges.
- *Perceptual* — compress the entire space to fit. Smooth gradients, but in-gamut colors lose vibrancy.
- *CSS Color 4 default (`gamut-map`)* — a chroma-reduction algorithm: keep L and H, reduce C until the color is in gamut. The default behaviour for `oklch()` colors that fall out of gamut. As of mid-2026 implementations are converging but not uniform.

The practical rule: author in OKLCH, declare your fallback strategy explicitly for brand-critical primitives (test in sRGB and P3 separately), and accept that auto-mapping will produce some visual drift on out-of-gamut steps.

### HCT (Material 3)

HCT — Hue, Chroma, Tone — is Google's color space for Material 3, anchored on CAM16 (a more sophisticated color appearance model than CIELAB or Oklab; accounts for surround/adaptation effects).

**HCT's contribution: tone-pinned contrast.** Two colors at the same Tone value have the same perceptual lightness regardless of hue. This is the property M3 uses to *guarantee contrast pairs across the entire palette* by tone difference: `Tone 90` on `Tone 10` always passes WCAG AA, regardless of which hue each is. Tonal palettes (40, 50, 60, 70…) become a contrast grid.

**HCT vs. OKLCH.** Both are perceptually-based; HCT is more sophisticated (accounts for surround), OKLCH is simpler/faster and good enough for most authoring. HCT-anchored ramps are just colors — they interop fine with non-Material systems. But the *guarantees* (tone-pinned contrast) hold only within the HCT framework. A ramp generated in HCT and exported as hex doesn't preserve the tone-pinned property when the consumer system reasons about the colors in OKLCH or sRGB.

**Cost.** HCT requires the Material library (or a port — `material-color-utilities` is open-source, ports exist in TS, Swift, Dart). OKLCH is native CSS. For a system that doesn't ship on Android, HCT is a useful *technique* but rarely a worthwhile dependency.

### CSS Color 4/5 surface — currency note

As of mid-2026:

- `oklch()`, `oklab()`, `lch()`, `lab()` — stable in Safari/Chrome/Firefox for 18+ months. Safe to use without polyfill.
- `color-mix(in oklch, …)` — well-supported across all three engines.
- Relative color syntax (`oklch(from var(--brand) calc(l - 0.1) c h)`) — Safari shipped late 2023, Chrome 2024, Firefox 2024; widespread support but the *least* mature of the four. Still has known parser inconsistencies for nested calc expressions.
- `color()` function with named spaces (`color(display-p3 …)`, `color(rec2020 …)`) — well-supported.
- `color-scheme: light dark` — well-supported.
- `forced-colors` media query and the `forced-color-adjust` property — well-supported.

The verification path: caniuse.com/css-oklab-oklch, caniuse.com/css-relative-colors, MDN's color page. The practitioner who's been away from CSS for two years should re-check relative color syntax specifically before committing a token architecture to it.

### Round-trip fidelity — where color drifts

The agency reality: most token pipelines silently quantise to sRGB hex on export.

- **Figma → tokens.** Figma Variables (mid-2026) supports OKLCH and P3 internally for color values, but the export adapters (Tokens Studio, Figma's own Variables-to-tokens emitter, plugin-based exporters) often quantise to hex. Verifying the exported color in OKLCH-aware tooling reveals the drift.
- **Tokens Studio → JSON.** Depends on the export configuration. The JSON spec preserves color expressions if the source declared them as `oklch()` strings; quantisation happens at the platform-output step.
- **Style Dictionary → CSS.** Style Dictionary's default color transforms convert to hex. To preserve OKLCH, the platform configuration must declare a custom transform or use the `css/variables` format with raw value passthrough. Most teams don't, and the runtime ends up with hex even though the source was OKLCH.
- **Style Dictionary → iOS/Android.** Native platforms don't have an OKLCH equivalent in their color types; the value gets converted to the platform's RGB or RGBA color, with the corresponding gamut clamp.

The practitioner consequence: declare a platform-by-platform fidelity contract. On web, preserve OKLCH end-to-end and let the runtime do gamut mapping. On iOS/Android, convert at build time, accept the drift, and *test the converted colors against the design source* before shipping. The test is non-negotiable; nominally-equivalent colors after a hex round-trip frequently differ enough to read as a different shade.

---

## 3. Accessible contrast — WCAG 2 vs. APCA, and the live debate

### What WCAG 2.x measures, and where it fails

WCAG 2.1/2.2's contrast ratio is the relative luminance ratio `(L1 + 0.05) / (L2 + 0.05)` with L computed from the sRGB R/G/B channels via a piecewise gamma function. Thresholds: 4.5:1 normal text, 3:1 large text and non-text UI components, 7:1 AAA.

**Where it's known to fail.**

*Dark-mode under-prediction.* A 4.5:1 white-on-`#1A1A1A` passes; the same text in practice reads as harsh, with bloom around glyph edges. The luminance ratio doesn't model the eye's response to bright objects on dark fields (the "halation" effect). Designers compensate by lowering the foreground luminance — `#E0E0E0` instead of pure white — but the formula doesn't *demand* it.

*Small-text trap.* The ratio threshold is binary by font size (the "large text" cutoff at 18pt or 14pt bold). It doesn't model font weight, stroke contrast, or the actual continuous reading-distance / size relationship. A thin-weight 18pt at 4.5:1 is illegible; a heavy-weight 13pt at 4.5:1 is fine. The formula gives both a pass.

*Yellow-on-white over-prediction.* A vibrant yellow (`#FFEE00`) against white can yield a luminance ratio that meets 3:1 for non-text — but the *perceptual* contrast is near zero. The eye's wavelength response peaks around yellow-green; high luminance in that band doesn't translate to high perceptual contrast. WCAG 2 doesn't model the wavelength response.

*The smaller-than-large binary.* The 18pt / 14pt-bold cutoff is a step function; perception is continuous.

These failures are not edge cases — they show up in audits regularly. The legal standard is what it is, but the formula is acknowledged (including by the WAI itself) as a coarse approximation.

### APCA — the perceptual replacement

APCA (Accessible Perceptual Contrast Algorithm) returns an Lc value rather than a ratio. It's *asymmetric*: light text on dark and dark text on light yield different Lc because perceptual contrast is direction-dependent. Lc thresholds:

- **Lc 90+** — critical UI, super-bold text (the highest tier).
- **Lc 75–90** — body text minimum (analogous to WCAG AA at 4.5:1 but perceptually grounded).
- **Lc 60–75** — large or non-essential text.
- **Lc 45–60** — large headings, decorative.
- **Lc <45** — fails for any text.

APCA models the things WCAG 2 misses: dark-mode halation, font-weight contribution, the wavelength response. The result: APCA grades a yellow-on-white pair as failing even though WCAG 2 passes it; APCA grades white-on-#202020 as more demanding than the equivalent ratio in light mode would suggest.

**Adoption as of mid-2026.**

- *Adopted* — Adobe Spectrum's research and design tools internally (some teams), GitHub Primer's contrast linting, parts of IBM Carbon (charts especially), Tailwind v4's contrast utilities reportedly use APCA-aware tuning, and several practitioner ramp generators (Atmos, recent Tints.dev versions).
- *Not adopted* — WCAG 2.2 (the legal/procurement standard); EN 301 549 (EU); Section 508 (US Federal). These mandate WCAG 2.x. APCA is *additive*, not substitutive.
- *WCAG 3 ("Silver") status* — as of mid-2026, WCAG 3 is a perpetual working draft. APCA was the proposed contrast model in 2022 working drafts; the W3C has not finalised. There is no shippable WCAG 3 to point procurement at. The verification path: w3.org/TR/wcag-3.0/ and the APCA project repo (myndex/SAPC-APCA).

**The practitioner stance.** Ship WCAG 2.x as the procurement floor — it's what audits and accessibility certifications test against. Use APCA in the *design-tool linting and ramp-generation layer* as the quality bar above the floor. A ramp that passes WCAG 2 at the rated steps but fails APCA is a ramp that will look wrong even when it passes audit. Conversely, a ramp tuned to APCA almost always passes WCAG 2 at the same steps.

### Anchoring contrast on a generated ramp

The 2024–2026 move: bake contrast into the ramp's structure so consumers don't have to compute it.

**Radix's contrast pairs.** Step 9 (the "solid" step) is contrast-paired with white text — `white on step-9 = AA at 4.5:1` for every hue. Step 11 is paired with the surface for low-contrast text; step 12 for high-contrast text. These are guarantees, hue by hue. The ramp's step-9 isn't the same OKLCH lightness for every hue (yellow's step 9 is darker than blue's), because contrast against white isn't constant across hues.

**Tailwind v4's contrast-aware shades.** Each numeric step has a documented contrast rating against the system surface. Authors who pick `bg-blue-600 text-white` get a known contrast guarantee.

**Adobe Leonardo's contrast-anchored generation.** The user declares the target contrast curve (e.g., AA on white at step 6, AAA at step 9), and Leonardo generates the ramp's colors *to hit* the curve. Brand color is a constraint, not the source of truth — if the brand color doesn't fit the curve, Leonardo shifts it.

The shared idea: **the ramp's step is a contrast role**, not a lightness coordinate. Consumers who pick `color/text/primary` (which resolves to step 11 or 12 of the appropriate hue) get the contrast guarantee for free.

The catch: if your primitive layer is naive numeric steps without per-hue contrast tuning, the semantic→primitive aliasing chain doesn't produce these guarantees. The ramp has to be *built* contrast-aware; you can't bolt the property on.

### The disabled-state exemption

WCAG 2.2 SC 1.4.3 and 1.4.11 explicitly exempt disabled controls from contrast requirements. The exemption exists because disabled state is conventionally signaled by lower contrast, and demanding WCAG-compliant contrast on a disabled control would erase the visual difference between disabled and enabled.

**The trap.** Leaning on the exemption produces inaccessible UIs that pass audit. A user can't tell whether a disabled control is "disabled" or "broken"; the AT user can't tell why the control is unreachable.

**The mitigation.** Two patterns, both better than naive disabled:

- *aria-disabled + maintained contrast.* The control is focusable and announceable; on activation, it explains why it's unavailable (a tooltip, an inline message). Contrast meets WCAG.
- *Focusable inactive state.* The control is in a "not currently actionable" state but reachable, contrast-compliant, and explained. (See the Button brief's treatment of native-disabled vs. focusable inactive.)

The system's color tokens should support both: a `color/action/disabled` that intentionally fails contrast (for legacy disabled UIs) and a `color/action/inactive` that doesn't (for the better pattern).

### Forced-colors / Windows High Contrast Mode

Forced-colors mode is a user accessibility setting (Windows, but supported across browsers) where the OS replaces author colors with system-defined keywords: `Canvas`, `CanvasText`, `LinkText`, `ButtonText`, `ButtonFace`, `Highlight`, `HighlightText`, `GrayText`, plus a few more. The user picks a high-contrast theme; their entire system uses the chosen palette.

**What forced-colors does to your tokens.** Most of them. The browser swaps `background-color`, `color`, `border-color`, etc. with the system keywords for any element where it can determine the intent. Only specific properties (background-images, gradients, shadows) and elements opted in via `forced-color-adjust: none` retain author colors.

**What the system can still control.**

- *Structure.* Borders survive, but their color becomes a system color. The system token `color/border/default` is overridden, but the *fact* of a border is preserved. UI that depends on borders (form fields, table dividers) survives. UI that depends on subtle background-color differences (a divider implemented as a 1px row with a faint background) doesn't.
- *Focus indicators.* `outline` and box-shadow-based focus rings get system-color treatment. Designs that rely on color-only focus differentiation fail; designs with outline-based focus rings work.
- *forced-color-adjust: none.* Use *very* sparingly — typically on logos and brand-critical hero imagery. Setting it on UI controls is an accessibility regression dressed up as control.

**The design discipline.** Assume the entire palette will be replaced. Ensure structure, focus, and state are communicated by *non-color* signals (borders, text, icons, focus outline). The token system itself doesn't help in this mode; the *components* have to be authored to survive without their colors.

---

## 4. Theming architecture

### Light / dark / brand / density as orthogonal axes

In theory orthogonal: any combination of (light|dark) × (brand-A|brand-B|brand-C) × (compact|comfortable|spacious) is a valid theme. In practice compounded — components ship validated values for each combination, and the matrix grows fast. Two brands × two color schemes × two densities = 8 theme combinations; every component-tier color token has 8 validated values.

**DTCG modes** are the architectural answer. A token declares its mode dimensions:

```json
"$modes": ["color-scheme", "brand", "density"],
"color/surface/raised": {
  "$value": {
    "color-scheme:light brand:a density:comfortable": "{neutral.50}",
    "color-scheme:dark  brand:a density:comfortable": "{neutral.900}",
    /* … */
  }
}
```

Tokens Studio and Figma Variables both support multi-dimensional modes as of mid-2026; Style Dictionary's mode support is via separate config files per mode, less ergonomic but workable. The build pipeline emits per-target outputs (a `.dark.css` and a `.light.css`, or a single CSS file with class-based selectors per mode).

The cost: declaring the matrix is the easy part; *validating* it is the hard part. Every combination needs visual review. Most systems ship one combination as the "validated default" and the others as derived/inherited, with a known drift on edge cases.

### Dark-mode surface elevation — the lift pattern

In light mode, elevation is signaled by a drop shadow against a white surface. In dark mode, that pattern fails — a black shadow on a black surface is invisible. The convergent answer: **elevation is signaled by a *lighter* surface, not a shadow.**

Material 3's lift pattern: `surface-1` through `surface-5`, each at a progressively higher overlay over the base surface (M3's documented values: 5%, 8%, 11%, 12%, 14% white overlay over the base dark surface, plus tint shifts toward `surfaceTint`).

The semantic implication: a `color/surface/raised` token in dark mode resolves to a lighter-by-some-amount surface, not just a different primitive. Components that ship "elevation tokens" (a card with `elevation-2`) read the surface from the elevation level, not the base surface.

**The shadow-fade-becomes-surface-lighten swap.** In light mode, `shadow/large` is a soft drop shadow. In dark mode, the equivalent token is *the same shadow plus a surface lift*, or — if the system commits — the shadow disappears entirely and the surface lift carries the elevation. Both patterns are in the field; Material 3 keeps a faint shadow plus the surface lift; some systems (Vercel's, Stripe's) use surface-only.

**The implication for tokens.** Composite shadow tokens have to be mode-aware (the dark-mode value may be null or different). Surface tokens have to be elevation-aware. Component authors have to ask not just "what's my surface" but "what's my surface at this elevation in this mode." The token volume in dark-mode-aware systems is meaningfully larger.

### The semantic→primitive aliasing chain

The chain: consumer reads `color/surface/raised/default` → semantic resolves to (theme-mode-aware) → `color/neutral/0` (light) or `color/neutral/100` + lift (dark) → primitive value.

**Where the chain breaks.**

- *Composite token round-trip.* DTCG composite tokens (typography, shadow) can include color sub-properties. Most tools as of mid-2026 don't faithfully preserve property-level aliasing inside composites on round-trip — the `fontColor` sub-property of a typography composite resolves to a value at export time, losing the alias. (See 22's composite-fidelity gap discussion.) The mitigation: carry composites as source-of-truth, flatten on export, accept the round-trip loss.
- *Brand-mode primitive gaps.* If the system has multiple brands and brand B's primitive ramp doesn't have the role brand A's does (no "step 12 neutral", no "warning amber"), the semantic falls back to the generic — which may not contrast on brand B's surface. The fix is upstream: validate every brand's primitive tier covers every role the semantic tier needs.
- *Density adds a dimension.* Component-tier color tokens that vary by density (a denser layout's border color is darker for legibility) double the validation matrix.

### Theme switching mechanics

The 2026 baseline:

- **CSS custom properties on `:root` or `[data-theme="…"]`** — the universal pattern. The semantic tokens become custom property declarations; the primitive tokens are scoped to the theme.
- **`prefers-color-scheme` media query** for system-preference detection.
- **`color-scheme` property** on `:root` — declares which color schemes the page supports; the browser uses this to render form controls, scrollbars, and other UA-styled elements appropriately. Without it, dark-mode pages get light scrollbars.
- **Runtime override** via class or data-attribute on `<html>` — `data-theme="dark"` or `class="dark"`; the theme cascades from `:root`.

**The FOUC / theme-flash problem.** A SSR'd page renders with the default theme markup, the JS hydrates and reads the user's stored preference, the theme swaps. The user sees a flash. Patterns that solve it:

- *Server-rendered theme decision.* Read the cookie or session on the server, set `data-theme` on the server-rendered HTML. Eliminates the flash entirely. Requires server-side state.
- *Inline blocking script in `<head>`.* A small synchronous script reads `localStorage`/cookie and sets `data-theme` before the body renders. Standard pattern; works without server-side state. Cost: a render-blocking script, ~1ms but blocking.
- *`color-scheme: light dark` + `prefers-color-scheme`* — for systems where system preference is the only source, no runtime override needed. Trivially flash-free; loses user control.

**Multi-brand at the color layer.** The T-Mobile/Metro and Ford/Lincoln pattern: single semantic surface, swappable primitive tier. The semantic `color/action/primary` resolves to brand A's pink or brand B's purple depending on the active brand. Implementation: scoped CSS custom properties (`[data-brand="metro"] :root { … }`), or runtime CSS-in-JS theme injection.

What breaks: when brand B's primary doesn't pass contrast on brand A's neutrals. The semantic has a contract ("AA on the default surface"), but the contract holds only if the *primitive ramp is contrast-aligned to the same step grid* across brands. If brand B's "primary" is at OKLCH lightness 0.65 and brand A's is at 0.55, white text on brand B's primary may fail.

**Solution.** Semantic tokens should reference *contrast-tier names*, not numeric steps. Define the role as "step where Lc 60 contrast on light surface is guaranteed" (not "step 9 of the brand ramp"). Force ramp authors across brands to align contrast at the same role. This is the discipline Radix encodes in its 12-step grid; multi-brand systems have to encode it themselves.

**Density at the color layer.** Compact density compresses spatial structure; the color tokens that signal structure (borders, dividers, focus rings) have to compensate by being darker/more contrasting. Pattern: density-aware border tokens (`color/border/default` is one step darker in compact density), or component-level density tokens with their own values. Most systems don't do this and ship density-aware *spacing* tokens with mode-naive *color* tokens; the result is compact layouts where dividers visually disappear.

---

## 5. Palette generation — tools and methods

### Contrast-anchored ramps (Leonardo / Adobe)

The user declares a target contrast curve — e.g., "step 6 = AA on white (4.5:1), step 9 = AAA on white (7:1)". The generator produces the colors that hit the curve. The brand color is a constraint (the ramp passes through it), not the source of truth.

**Strengths.** Contrast guarantees are absolute. Every step does what it says.

**Trade-offs.** Brand fidelity is bounded by the contrast curve — if the brand color is at "step 6" but step 6 needs to be AA, and the brand color falls short, Leonardo will shift the brand color to the nearest passing value. This is desirable for accessibility-first systems and unwelcome for brand-led ones.

The Leonardo workflow is the gold standard for guaranteed-contrast outputs but is a poor fit for systems that need to match an existing brand color exactly. A common compromise: use Leonardo to *validate* a hand-tuned ramp against a contrast curve, not to *generate* the ramp.

### Perceptually-uniform OKLCH ramps

Pattern: pick a hue, fix chroma at e.g. 0.18, set lightness at fixed steps (0.10, 0.18, 0.30, 0.42, 0.55, 0.65, 0.75, 0.85, 0.92, 0.96, 0.98). Each step's perceptual jump is uniform. Generate all hues from the same (L, C) grid.

**Strengths.** Visually consistent ramps; trivial to implement; no library required.

**Trade-offs.** Per-hue chroma tuning is mandatory for vivid colors (yellow at chroma 0.18 looks dingy; needs to be lower; greens and blues can go higher without clamping). Contrast is *not* guaranteed at fixed steps — step 9 of one hue may pass AA on white, step 9 of another may fail.

This is the Tailwind v4 pattern (Tailwind v4's default palette is OKLCH-based and per-hue chroma-tuned), and the pattern most practitioner ramp generators (Tints.dev, Atmos) emit.

### Curated/hand-tuned ramps (Radix Colors, Open Color, Tailwind v4)

Each step has a named role and the color is hand-tuned to fit. Radix in particular is a "designed system" — every step's color is the result of deliberate authoring, not a generated curve.

**Strengths.** Production-quality out of the box. Contrast guarantees baked in. Light/dark/alpha siblings shipped. Free-tier for the open-source palettes.

**Trade-offs.** The role definitions are opinionated. Brand-driven systems with conventions outside the Radix model (a step 13 for marketing surfaces, a step 0 for special "off-app" backgrounds) have to extend the system manually. Radix's choice of which hue is "iris" vs "indigo" vs "blue" is canonical Radix; rebranding to your own naming creates two source-of-truth artifacts.

When right for an agency engagement: when the brand is willing to adopt the role-based grid (most are, once they see the contrast guarantees); when the team needs a fast, stable starting point without committing to a generation toolchain. Radix as the primitive layer, custom semantic aliases on top, is a productive default for brand-light product systems.

### Material 3 dynamic color (HCT-based)

The wallpaper-derived scheme is the headline: extract a "source color" from the user's wallpaper → expand to a set of tonal palettes via HCT → map to M3 color roles (`primary`, `onPrimary`, `surface`, etc.). The user's phone wallpaper drives the app's color scheme.

For systems that don't ship on Android: the *technique* generalises. The Material Theme Builder Figma plugin produces tonal palettes from a source color. The HCT-anchored tonal-palette method is a legitimate approach to ramp generation regardless of whether the output ships on Android.

**Cost for non-Material systems.** Bringing in Material's color utilities (or porting them) for ramp generation is overhead. Most non-Material systems use OKLCH instead and accept the slightly less sophisticated appearance model.

### Brand-anchored vs. system-anchored ramps

**Brand-anchored.** The brand color is fixed at a known step (typically 9, the "solid" step). The rest of the ramp is generated to fit around it. The system's identity is rooted in the brand color's exact rendering.

**System-anchored.** The ramp is generated according to system rules (contrast targets, perceptual uniformity); the brand color is the closest match within the rules. The system's identity is rooted in consistent contrast and perceptual behaviour.

**The contrast-step-vs-brand-step alignment problem.** If brand is at step 9 and step 9 must be AA-paired with white, the brand color has to pass that test. If it doesn't (brand yellow on white fails AA at any reasonable chroma), the system has three choices:

- Move brand to a different step (yellow at step 11, with light gray text on top) — usually unacceptable to the brand team.
- Use a non-brand color for "primary action" (carve out a separate "action" hue) — common; the brand color shows up in headers, accents, illustrations.
- Restrict brand-on-light usage to large text and non-essential UI — works for brands willing to commit.

The agency role is to surface this in Foundations — *before* the component library is in flight. Discovering brand-on-its-own-system contrast failures during component review is too late.

### Tooling depth (mid-2026)

The major tools, what they're good at, what none are good at:

- **Adobe Leonardo** — contrast-anchored ramps; gold standard for guaranteed-contrast outputs; weak on perceptual uniformity. Free, web-based.
- **Tints.dev** — OKLCH ramp generator, free, fast, produces export-ready Tailwind/JSON output. Weak on multi-mode export and contrast validation.
- **Atmos** — OKLCH-based, targeted at Tailwind users. Better mode/dark support than Tints.dev. Paid.
- **Material Theme Builder** — HCT, Figma plugin. Tied to Material role mapping. Free.
- **Radix Colors** — pre-curated, copy-paste. No customisation; that's the point. Free.
- **Tailwind v4 generator** — OKLCH-based; default palette is excellent; custom palette generation through configuration. Free, code-driven.
- **Tokens Studio plugin (for Figma)** — supports OKLCH, color-mix, multi-mode; primarily an authoring/sync tool, not a generator. Paid.

**What none of them does well:** *bridging.* No mainstream tool takes a brand color and produces both a contrast-anchored *and* a perceptually-uniform ramp that aligns at the same numeric step. Practitioners typically bridge by hand — author in Leonardo for contrast pairs, then visually tune chroma per hue for perceptual consistency. The integration is manual and the source of truth is ambiguous.

A second gap: *forced-colors mapping.* No tool helps the system declare what each token should be in forced-colors mode (most should resolve to system keywords; a few brand-critical ones need `forced-color-adjust: none` opt-out). This is hand-rolled in the runtime CSS.

A third gap: *cross-platform fidelity testing.* No tool renders the same token on web (sRGB / P3 / OKLCH), iOS, and Android side-by-side and reports the perceptual delta. Practitioners sample manually.

---

## 6. Brand color vs. UI color — the unity/cohesion tension

### The Perez-Cruz framing, pushed deeper

*Unity* — strict palette, every element drawn from one ramp. Risks: editorial flatness, brand expression suppressed; the brand can't *do* anything visually distinctive because the ramp doesn't have the chroma range.

*Cohesion* — related-but-distinct palettes (a display palette and a UI palette that share a hue at a shared step). Risks: drift over time; the relationship becomes implicit; eventually it's two palettes pretending to be related.

The middle ground: **shared primitives, separate semantic roles.** Display semantics (`color/editorial/heading`, `color/editorial/lede`) reference brand-display primitives — wider chroma, more saturated. UI semantics (`color/text/primary`, `color/action/primary`) reference UI-tuned ramps — narrower chroma, contrast-anchored. Both share a brand hue at step 9 (so the system *recognisably* belongs to the brand). The semantic layer enforces the discipline; consumers can't accidentally use a display color in a UI surface.

### Status / semantic carve-outs

Status colors — success, warning, error, info — are **exceptions to brand expression**. The reasons:

- *Cultural and convention-bound meaning.* Red for error, green for success, yellow for warning. Disrupting the convention costs comprehension. A brand whose primary is red has to choose between brand expression and signal clarity.
- *The "system green" stability rule.* `color/status/success` should be perceptually similar across themes, brands, and densities — it's a *signal*, not a brand expression. Stripe's success-green and Carbon's success-green look similar because the meaning is shared.
- *Contrast obligations are non-negotiable.* Status colors carry information; failing contrast on a status icon means failing the user. The brand can't override.

**The red-can't-mean-brand problem.** When a brand's primary is red, the system needs a separate "destructive" red that's visually distinguishable from brand-red, OR the brand has to accept that destructive actions look like brand actions. The latter is rarely acceptable. The former requires careful tuning — a destructive-red that's distinguishable but still legibly "red," typically warmer or darker.

This is a common engagement issue and a place where brand and DS teams conflict. The DS POV: status colors are infrastructure, not brand assets, and the system needs the freedom to ship a working destructive color even when the brand's red sits in adjacent territory.

### Editorial / marketing color vs. product UI color

When to ship two palettes:

- *Brand-display* — for hero, marketing surfaces, editorial pages. Wider chroma range, more saturated, often P3-anchored. Tuned for impact, not legibility.
- *Product UI* — for forms, dashboards, transactional flows. Narrower chroma, contrast-tuned, typically sRGB-anchored. Tuned for legibility and consistency at small sizes.

When one is enough: the system is product-only or marketing-only; the brand's hue is forgiving enough to do both jobs (true for many fintech / SaaS brands with mid-saturation primaries).

When to ship two: brand's signature color is too saturated or too vivid to use as UI primary; the system serves both marketing and product surfaces; the engagement scope explicitly covers both.

The architectural pattern: shared primitives with separate semantic roles (above). The build pipeline emits one stylesheet with both semantic tiers; consumers pick by surface context.

### The brand-against-its-own-system trap

Concrete: brand color is signature yellow; primary action button needs WCAG AA on white; yellow doesn't pass at any reasonable chroma. The traps:

- *Shifting brand.* Move yellow toward darker yellow / amber to pass contrast. Brand says no.
- *Carving out non-brand "primary action".* Use brand's secondary color (often blue or charcoal) for action; keep brand-yellow for accents and headers. Costs brand presence on the most-visible UI element.
- *Brand-on-dark-only.* Brand-yellow appears only on dark surfaces (where contrast against white text passes); light theme uses a different primary. Unbalanced; the brand looks weaker in light mode.
- *Brand as accent, not action.* Yellow is used for accents (highlights, key data, status), not for action surfaces. A defensible pattern but it changes how the brand is *seen* — brand becomes an emphasis, not a presence.

The agency's job: surface the trap in Foundations — explicitly, with examples of the brand color tested against the system's surface and text colors at WCAG and APCA. Discovering the trap during component review is too late; the fix is architectural, not cosmetic.

---

## 7. Data-visualisation palettes

### Categorical / sequential / diverging — distinct problems

Each requires a different palette structure.

- *Categorical.* 8–12 distinguishable hues, used to differentiate *unrelated* values (e.g., series in a multi-line chart). Requires perceptually equidistant hue spacing. Requires color-blind safety. The UI palette's hue selection is brand-driven, not perceptually-spaced — it doesn't serve.
- *Sequential.* A single-hue ramp from light to dark, used for *ordered/quantitative* values (heatmaps, choropleth maps). OKLCH-derived ramps with monotonic lightness produce accurate ordering. UI ramps don't — they're tuned for contrast roles, not perceptual ordering.
- *Diverging.* Two-hue ramp meeting at a neutral midpoint, used for values diverging from a central norm (temperature anomaly, change vs. baseline). Requires careful hue-pair selection — red/blue is the convention, but red/green fails for color-blind users; orange/teal is the typical color-blind-safe alternative.

A UI palette serves none of them. Its hue selection, lightness curves, and chroma values are tuned for product UI, not data encoding. Trying to derive a data-vis palette by re-using the UI palette's hues is a recurring failure.

### Color-blind safety

Forms of color-vision deficiency to plan for:

- *Deuteranomaly* — green-weakness; ~5% of males. Reds and greens become harder to distinguish.
- *Protanomaly* — red-weakness; ~1%. Similar effect.
- *Tritanomaly* — blue-weakness; <1%. Yellows and blues become harder.
- *Achromatopsia* — full color-blindness; very rare. Grayscale-equivalence is the test.

Established palettes:

- **Viridis** (matplotlib's default sequential) — perceptually uniform, color-blind safe, grayscale-safe.
- **IBM Carbon Charts** — a curated 14-color categorical palette tested across deuteranomaly/protanomaly/tritanomaly.
- **Tableau color-blind safe** — practitioner default since 2016; 10-color categorical.
- **ColorBrewer** — Cynthia Brewer's research-grade palettes for cartography; sequential, diverging, and categorical sets, all color-blind tested.

The discipline that survives the color-blind test: **color is never the sole carrier.** Even with a color-blind safe palette, charts must encode the data redundantly (line shape, marker shape, label, pattern, value annotation). The Chart-component gap (see 09) is precisely this — most charts default to color-only and fail color-blind users.

### Perceptual ordering

An HSL-derived sequential ramp has uneven perceptual steps (constant H, varying L and S — but L doesn't track perception in HSL). Readers misread the ordering — values that the chart author intended to read as "third-largest" read as "second-largest" because the perceptual jump from step 6 to step 7 is larger than from step 7 to step 8.

An OKLCH-derived ramp has even perceptual steps. Readers correctly order values. Empirically, viewers rank OKLCH-derived sequential ramps significantly more accurately than HSL-derived (multiple studies in the data-vis literature; the matplotlib team's adoption of Viridis was driven by this evidence).

The implication: the data-vis sequential ramps in the system should be OKLCH-derived. Re-using the UI ramp (which is contrast-anchored, not perceptually-uniform) is a comprehension regression.

### Where data-vis lives in the token architecture

A separate primitive scale is the right answer:

```
color/viz/categorical/1..12
color/viz/sequential/blue/100..900
color/viz/sequential/heat/100..900
color/viz/diverging/coolwarm/100..900
```

These primitives are not derived from the UI palette. They're independently tuned for the data-vis problem. The system's UI semantics (text, surface, action, status) don't reference the viz primitives, and vice versa.

Where the UI semantics *do* show up in charts: annotations, axis labels, gridlines, the status-colored callout for a critical threshold. These use UI tokens. The data series use viz primitives.

The token volume: a system that ships data-vis as a first-class concern adds 50–100 viz primitives on top of the UI ones. Most agency engagements treat data-vis as out-of-scope or ship a minimal categorical-only palette; full data-vis token coverage is a distinct sub-project, often charged separately.

### The 12-color limit and alternatives

Beyond ~8–12 categorical hues, viewers can't reliably distinguish; the chart's encoding fails. The alternatives:

- *Categorical-as-pattern.* Hue + texture/pattern (stripes, dots, dashes); expands distinguishability beyond pure hue. Works well in print, less well in interactive UI where patterns can shimmer.
- *Hierarchical grouping.* Sub-group similar series under a parent color (5 series in "blue family" all in shades of blue, distinguishable within the family but visually grouped against other families).
- *Table-fallback contract.* Any chart that exceeds ~8 series must have a table view. The table is the accessible primary, the chart is the visual layer. This is the convergent answer in accessible data-vis practice — Carbon Charts ships this, Spectrum's data-vis docs require it.

---

## 8. Native platform translation + AI-readable color descriptions

### iOS UIKit/SwiftUI semantic colors

Apple's system palette ships with built-in dynamic-color behaviour: each system color resolves to (light, dark) × (regular, high-contrast) × (regular, larger) automatically. The named tokens:

- *Background* — `.systemBackground`, `.secondarySystemBackground`, `.tertiarySystemBackground` (and the grouped variants for table/grouped backgrounds).
- *Foreground* — `.label`, `.secondaryLabel`, `.tertiaryLabel`, `.quaternaryLabel`. Plus `.placeholderText`, `.linkColor`.
- *Separators* — `.separator`, `.opaqueSeparator`.
- *Tints / accents* — `.systemBlue`, `.systemRed`, etc. (the "system" hues).
- *Standard fills* — `.systemFill`, `.secondarySystemFill`, `.tertiarySystemFill`, `.quaternarySystemFill`.

A third-party DS on iOS has two patterns:

- *Map* — a brand-aligned `color/text/primary` *replaces* `.label` only on the third-party app's surfaces. The system colors are still used for system-rendered UI (alerts, action sheets, etc.). Loses some brand fidelity in system-controlled regions.
- *Replace* — the DS ships its own full color palette and ignores the system palette except for inheriting accessibility behaviour at primitive level. Loses free dark-mode/high-contrast handling unless the DS's palette is itself dynamic.

Most agency engagements: replace the primary palette (text, surface, action, brand status) with DS tokens; *retain* system colors for interactions (system blue for default-tint where the brand doesn't override) and for OS-level UI. The trade-off is brand fidelity vs. native feel; agency engagements typically err toward brand.

### Material 3 dynamic color (Android)

Material 3's dynamic color: the user's wallpaper is the source. The OS extracts a "source color," generates tonal palettes via HCT, and maps to M3 color roles. The result: the app's color theme adapts to the user's wallpaper.

Color roles: `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `secondary`, `onSecondary`, `tertiary`, `onTertiary`, `error`, `onError`, `errorContainer`, `surface`, `onSurface`, `surfaceVariant`, `onSurfaceVariant`, `outline`. Each is accessed via `MaterialTheme.colorScheme.<role>` in Compose.

A third-party DS on Android in 2026 typically *opts out of dynamic color* (`dynamicColor = false`) and ships its own scheme via `lightColorScheme()` / `darkColorScheme()`. The trade-off:

- *Dynamic color is a user-pleasing OS feature.* Opting out means the app doesn't theme to the user's wallpaper — a small but visible loss for users who like the personalisation.
- *Brand fidelity is non-negotiable.* Brands generally accept the trade. The exception is consumer apps where wallpaper-themed UI is part of the brand's pitch (rare).

The semantic mapping: the DS's `color/action/primary` maps to `MaterialTheme.colorScheme.primary` for components that read from the M3 surface (third-party Material components), and to a direct token reference for in-house components.

### React Native, Flutter

**React Native** — `useColorScheme()` returns 'light'|'dark'|null from system; no built-in semantic palette beyond a small `PlatformColor` API. Theming is via React Context, conventionally with a theme provider that exposes the DS's tokens. The DS reimplements its color machinery as a JS theme object.

**Flutter** — `MaterialColor`, `ColorScheme` — strongly tied to Material. Opting out of Material is verbose; the convention is to layer your DS tokens *over* the Material `ColorScheme` (set the ColorScheme's primary, secondary, etc., to your token values; let Material components inherit; ship custom widgets that read from your theme).

**The platform-divergence cost.** A DS that ships across iOS, Android, web, RN, Flutter must reimplement its theming machinery in each platform's idiom. This is the largest "platform tax" in cross-platform DS work — meaningfully more work than the equivalent for spacing or typography, because each platform's color system is opinionated and the DS has to either fight or merge.

DTCG modes + Style Dictionary translators reduce the cost by automating the mode → platform-output translation, but don't eliminate the per-platform theming integration work. Each platform's theme provider still has to be built, tested, and maintained.

### AI-readable color descriptions

The fields a color token needs to be agent-consumable:

- **`meaning`** — what this color signifies semantically. "Destructive action," "success state," "elevated surface in dark mode," "subtle background for inactive UI." This is the highest-ROI field for AI: it answers *what is this for*. A model picking a color for "delete account button" needs to know which token means "destructive" — without `meaning`, the model has to infer from name (`color/status/error` is hopeful; `color/red-9` is hopeless).
- **`when_to_use`** — contexts where the token is correct. "Use for primary actions on default surfaces." "Use for success status indicators."
- **`avoid_when`** — contexts where the token is wrong. "Avoid for non-destructive actions." "Avoid for low-contrast contexts." The pair with `meaning` is what helps the AI rule out incorrect picks.
- **`paired_with`** — which tokens compose with this one. For a foreground color, the surface tokens it's tested against. For a surface, the text colors that pass contrast on it. This answers "what should I put on top" — a model picking text-on-surface needs the foreground that's been validated against the chosen surface.
- **`contrast_with`** — explicit pairings that are guaranteed accessible. `"contrast_with": [{ token: "color/text/primary", min_contrast: "AA", surface: "default" }]`. Answers compliance questions an agent would otherwise have to compute.
- **`mode_overrides`** — how the token resolves in light/dark/HC/forced-colors. `"mode_overrides": { "dark": "{neutral.50}", "forced-colors": "Canvas" }`. Lets the agent reason about cross-mode behaviour.

**Which fields move the needle.** `meaning` and `paired_with` are the highest leverage — they answer the two questions a model picking a color most needs to answer ("is this the right color for this purpose?" and "what should I put with it?"). `contrast_with` is the third — it converts a compliance check the model would have to compute into a lookup. `when_to_use`/`avoid_when` are valuable but lower leverage; the model can often infer them from `meaning`.

**Nice-to-have.** `tonal_palette_siblings` (linking each color in a ramp to its neighbours in the same hue, so a model that picks step 9 of a ramp can reach for step 8 hover and step 11 text without re-querying the catalogue). `forced_colors_mapping` (the system keyword the token resolves to in forced-colors mode). `gamut_clamps` (the sRGB and P3 versions when the source is OKLCH).

---

## References

Primary sources, dated to mid-2026:

- W3C CSS Color Module Level 4 — https://www.w3.org/TR/css-color-4/ (REC, with continuing errata)
- W3C CSS Color Module Level 5 — https://www.w3.org/TR/css-color-5/ (CR; relative color, color-mix)
- W3C WCAG 2.2 — https://www.w3.org/TR/WCAG22/ (REC, October 2023; SC 1.4.3, 1.4.11, exemptions)
- W3C WCAG 3.0 working draft — https://www.w3.org/TR/wcag-3.0/ (perpetual WD as of mid-2026; APCA proposed but not finalised)
- APCA / SAPC reference implementation — https://github.com/Myndex/SAPC-APCA
- DTCG color-token specification — https://tr.designtokens.org/format/ (composite token types, modes; spec status mid-2026)
- Radix Colors documentation — https://www.radix-ui.com/colors/docs/overview/scales (12-step grid, contrast pairs)
- Tailwind CSS v4 documentation — https://tailwindcss.com/docs/colors (OKLCH-based default palette)
- Adobe Leonardo — https://leonardocolor.io and the Adobe Spectrum color research
- GitHub Primer color documentation — https://primer.style/foundations/primitives/color
- IBM Carbon color and contrast — https://carbondesignsystem.com/elements/color/
- IBM Carbon Charts color palettes — https://carbondesignsystem.com/data-visualization/color-palettes/
- Material 3 color system — https://m3.material.io/styles/color/system/overview
- Material 3 dynamic color — https://m3.material.io/styles/color/dynamic/overview
- material-color-utilities — https://github.com/material-foundation/material-color-utilities
- Apple HIG color — https://developer.apple.com/design/human-interface-guidelines/color
- Apple system colors (UIKit/SwiftUI) — https://developer.apple.com/documentation/uikit/uicolor/standard_colors
- Cynthia Brewer's ColorBrewer — https://colorbrewer2.org/
- Viridis / matplotlib colormap research — https://bids.github.io/colormap/
- W3C `color-scheme` / `forced-colors` — CSS Color Adjustment Module Level 1
- Yesenia Perez-Cruz, *Expressive Design Systems* (2021) — color groups by background context
- Andrew Couldwell, *Laying the Foundations* (2019) — numeric scales, 50/60/70 half-steps
- Nathan Curtis, EightShapes — Design Tokens (Nov 2024), color-token treatment

Verification notes: all "as of mid-2026" claims about browser support should be re-checked at caniuse.com and MDN's per-feature pages before relying on them. The APCA / WCAG 3 status is unstable; the Myndex repo and the W3C WCAG 3 working-draft page are the canonical references.

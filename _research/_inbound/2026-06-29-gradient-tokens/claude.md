# Tokenizing gradients — DTCG, the field, and Figma

*Claude's run of the brief. Researched 2026-06-29 against the DTCG spec (Format
Module 2025.10), primary docs for 10 design systems, and the Figma Plugin/REST
API references. Confidence: [S] sourced/exact, [J] judgement.*

## TL;DR

- **Gradients are the most-skipped token category.** Of ten systems surveyed,
  the majority ship **no gradient tokens at all** — gradients are treated as
  component-level compositions over semantic colour tokens. [S]
- **DTCG `gradient` is a real composite type, but stops-only.** `$value` is an
  array of `{ color, position }` stops; stop colours may be token references. It
  **does not encode kind (linear/radial/conic), angle/direction, or interpolation
  space** — a known, still-open gap (issue #101). [S]
- **Where systems do tokenize gradients well, they decompose** (geometry + stops)
  and **alias stops to the colour ramp** (Fluent, Carbon's mixins, Primer's
  removed set). Raw CSS-string gradient tokens (Polaris, SLDS) are treated as
  legacy and don't theme. [S]
- **In Figma a gradient is a Paint, never a variable.** It lives in a **Paint
  Style** (a separate object class, like Effect/Text styles). Only stop **colours**
  bind to colour variables; kind, angle and stop positions are baked. Paint Styles
  are **plugin-only** to create (REST can neither write nor read their values). [S]
- **Figma interpolates gradients in sRGB only** — no OKLCH. CSS Color 4's
  `linear-gradient(in oklch, …)` is Baseline-widely-available and avoids the sRGB
  "grey dead zone," so a portable gradient should carry an OKLCH definition **plus**
  a pre-sampled multi-stop sRGB approximation for Figma. [S]

---

## 1. The DTCG gradient type

`gradient` is a composite type in the **Design Tokens Format Module 2025.10** (the
first stable CG draft, 28 Oct 2025). `$value` is an **array of gradient stops**,
each with exactly two fields: [S]

- **`color`** — a colour value *or a reference to a colour token*;
- **`position`** — a number (or number-token ref) in **[0, 1]** (clamped; missing
  end stops extend the nearest colour).

```json
{ "$type": "gradient", "$value": [
  { "color": "{brand.primary}", "position": 0 },
  { "color": "#ff0000",          "position": 1 }
]}
```

**The gap:** there is **no field for kind (linear/radial/conic), angle/direction,
radial centre/size, or interpolation colour space.** [S] The spec author's own tool
(Cobalt) notes it assumes `linear`. Issue **#101 "Gradient type feedback"** (open
since 2022, active into 2026, labelled *Next Draft Priority*) collects exactly these
gaps: maintainers propose adding `type: linear|radial|conic`, an `angle`, radial
`size`, OKLCH **interpolation space**, independent opacity stops, and eased/absolute
stops. The 2025.10 release added OKLCH/Display-P3 to the **colour** type but did
**not** touch gradient. [S]

**Aliasing works at both levels:** a stop's `color` may be a `{…}` reference, and a
whole gradient may be aliased — the hook for theming. [S]

## 2. The field (10 systems)

| System | Ships gradient tokens? | Model | Stops alias the ramp? |
|---|---|---|---|
| **Material 3** | No — abstains [S] | flat tonal roles | n/a |
| **IBM Carbon** | No tokens — SCSS mixins [S] | `ai-gradient()` etc., `linear-gradient()` | yes — stops use theme tokens |
| **Atlassian** | No dedicated category [S] | gradients composed in components | n/a (would alias) |
| **Adobe Spectrum** | Limited — decomposed [S] | `gradient-stop` = position ratio only; colours tracked separately; composite type deliberately avoided | positions are bare numbers |
| **Shopify Polaris** | Was `bg-gradient`; **removed** [S] | single CSS `linear-gradient()` string | **no — raw rgba** |
| **Salesforce SLDS** | SLDS 1 deprecated; SLDS 2 abstains [S] | CSS string token | **no — raw rgba** |
| **Primer (GitHub)** | No (removed legacy) [S] | per-endpoint colour tokens | yes — `accent.subtle` etc. |
| **Microsoft Fluent** | **Yes** — decomposed composite [S] | `start`/`end` points + `stops[]` of `{position, value\|aliasOf}` (linear only) | **yes — `aliasOf`** |
| **Tailwind** | No token — utility-composed [S] | direction class + `from/via/to` palette stops; **OKLCH/Oklab interpolation in v4** | yes — palette |
| **USWDS** | No — abstains [S] | solid colour only | n/a |

**Reading:** the dominant signal is **abstention** (Material, Carbon, Primer, USWDS,
Salesforce, Atlassian as a category) — gradients are judged too contextual to
standardise as primitives. Among those that do tokenize: **Fluent** is the mature
model (decomposed composite, stops alias colour tokens, fixing the gaps DTCG left);
**Polaris/SLDS** are the cautionary case (opaque CSS strings, raw colours, since
deprecated); **Tailwind** is the rendering benchmark (palette-aliased stops + OKLCH
interpolation by default). No system ships a W3C-DTCG-shaped composite in production. [S/J]

## 3. Figma

- **A gradient is a `Paint`** (`GRADIENT_LINEAR/RADIAL/ANGULAR/DIAMOND`) — never a
  standalone object. It carries `gradientStops` ({color, position}) and a
  **direction encoded as a matrix** (`gradientTransform`, Plugin API) or **handle
  vectors** (`gradientHandlePositions`, REST). There is **no degrees field** — an
  angle must be computed into the transform. [S]
- **A variable cannot hold a gradient.** Figma variables resolve only to
  COLOR/FLOAT/STRING/BOOLEAN; "gradient as a variable type" is an open, unshipped
  request. [S]
- **Only stop colours bind.** `ColorStop.boundVariables.color` can alias a COLOR
  variable (Plugin API Update 92, Apr 2024). Stop **position** and gradient
  **angle/kind** are **not** bindable — baked. [S]
- **Paint Styles are the home** (a separate object class beside Effect/Text styles).
  Create/write is **Plugin API only** (`figma.createPaintStyle()`); the **REST API
  cannot create styles and cannot even read their paint values** (style endpoints
  return metadata only). The REST Variables API touches variables only. [S]
- **Interpolation is sRGB only** in Figma — no OKLCH/perceptual option in the UI or
  API (open request). CSS, by contrast, supports `linear-gradient(in oklch, …)`
  (Baseline widely available since mid-2023; CSS now defaults to Oklab). The
  mismatch: an OKLCH gradient won't reproduce in Figma — its midpoint differs
  (greyer). The fix is to **pre-sample the OKLCH curve into N baked sRGB stops** for
  the Figma Paint Style. [S]

**Materialization recipe (code → Figma):** emit stop colours as COLOR variables;
build the gradient as a `GradientPaint` inside a Paint Style via a plugin; bind each
stop's colour to its variable; **bake** kind, direction (transform) and positions;
lay down the pre-sampled sRGB stops so the sRGB-linear segments approximate the
OKLCH curve. [S/J]

## 4. Accessibility

No dedicated W3C gradient-a11y guidance; it falls under WCAG 1.4.3/1.4.11. The
practitioner rule: **text over a gradient must meet its contrast ratio at the
worst-case (lowest-contrast) point under the text**, not the average — so constrain
the gradient's lightness range, add a scrim, or put text in a solid container. APCA
(WCAG 3 direction) models this better. For dark mode, **don't author separate
light/dark gradients** — alias each stop to a theme-aware semantic colour token and
the gradient flips automatically (DTCG supports this via stop colour references).
Watch silent gamut clipping with high-chroma OKLCH interpolation. [S/J]

## Recommendation (engine + practice)

**Tokenize gradients thinly and opt-in.** Most of the field abstains, so don't make
gradients a derived-for-everyone axis; ship them only when a brand declares them.
When you do:

1. **DTCG `gradient` composite as the spine** — array of `{ color, position }`,
   stop colours **aliasing the colour ramp** (Fluent/Carbon), never raw hex (the
   deprecated Polaris/SLDS trap).
2. **Carry kind/angle/interpolation in `$extensions`** (DTCG omits them — issue
   #101); default interpolation to **OKLCH** and emit CSS `in oklch`.
3. **Pre-sample the OKLCH curve into N sRGB stops** for Figma (sRGB-only), and
   materialize as a **Figma Paint Style** where only stop colours bind.
4. **Compute a worst-case-stop contrast** so text-on-gradient is gated at its worst
   point — a check no surveyed system performs.

## Sources
DTCG Format Module 2025.10 (designtokens.org/tr) · gradient issue #101
(github.com/design-tokens/community-group/issues/101) · Cobalt gradient docs
(cobalt-ui.pages.dev/tokens/gradient) · Fluent token pipeline
(microsoft.github.io/fluentui-token-pipeline/json.html) · Tailwind v4 gradients
(tailwindcss.com/docs/background-image, blog/tailwindcss-v4) · Spectrum
spectrum-design-data (github.com/adobe/spectrum-design-data) · Polaris v11 tokens
(polaris-react.shopify.com/previous-releases/version-11-tokens) · SLDS 2 transition
(lightningdesignsystem.com) · Primer primitives removed.json (github.com/primer/primitives)
· Material tokens (github.com/material-foundation/material-tokens) · Carbon
ai-gradient (github.com/carbon-design-system/carbon) · USWDS tokens
(designsystem.digital.gov/design-tokens) · Figma Plugin Paint/GradientPaint +
Update 92 (developers.figma.com/docs/plugins) · REST Variables types/endpoints +
PaintStyle (developers.figma.com, figma.com/plugin-docs) · CSS color-interpolation-method
(MDN) · OKLCH in CSS (evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl).

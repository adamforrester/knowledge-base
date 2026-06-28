# Tokenizing Elevation / Shadow Across Mature Design Systems

*Claude's run of the dual-agent brief. Researched 2026-06-28 against M3, IBM Carbon
source, Atlassian, Shopify Polaris, GitHub Primer, Microsoft Fluent 2, Adobe
Spectrum, Tailwind v3, Radix Themes, Apple HIG, and the Comeau/Ahlin layered-shadow
method. Confidence: [S] sourced with exact numbers; [S~] long-published standard,
primary page didn't render cleanly; [J] judgement/synthesis.*

## TL;DR — recommendation for a white-label shadow generator

- **6 steps** (`xs–2xl`) — the convergent count (M3, Radix, Fluent, NB) — plus a single inset.
- **2 layers per step (key + ambient)** — the field's centre of gravity (Fluent, Tailwind, NB). Optional 3–4-layer "high-fidelity" profile for marketing.
- **Light/dark: LIFT-primary, shadow retained-but-reduced** — the convergent 2026 pattern (M3 + Atlassian). Dark elevation is carried mainly by a *lighter surface*; the shadow is **reduced, not nulled** (M3/Atlassian retain a faint one at the top) and **not heavier** (rejecting NB/Fluent's dark-heavier branch — the minority, and it muddies dark UIs).
- **Tinted near-black, not pure black** (Polaris `rgba(26,26,26)`, Radix `gray-a*`, Comeau's hue-match) — with a `tint` knob (hue + amount) for brand-hued marketing shadows.
- **Two primitive axes (surface ladder + shadow ladder) joined by a semantic `elevation.N` token** that resolves per mode to `{surface-lift, shadow}` (Atlassian's split); components alias the semantic level.
- **Generation lever = `softness`** (blur:offset ratio — crisp product ↔ soft marketing) + `tint` (hue + amount); `offsetX 0`, spread negative-and-growing, opacity drifting up at the top.

---

## Comparison table

| System | Steps + naming | Layers | Colour | Light vs dark | Surface↔shadow | Inset? |
|---|---|---|---|---|---|---|
| **Material 3** | levels 0–5 (dp) [S~] | 2 (key+ambient) [S~] | black-alpha [S~] | **LIFT**: dark = tonal surface overlay, shadow de-emphasised; overlay % 0/5/7/8/9/11/12/14/15/16 [S~] | one elevation concept → shadow (light) + tonal surface (dark) [S~] | — |
| **Atlassian** | 5 semantic (sunken/default/raised/overlay) [S] | layered [J] | black-alpha [J] | **LIFT + retained shadow** on raised/overlay [S] | **explicit split** `elevation.surface.*` vs `elevation.shadow.*`, "always pair" [S] | — |
| **Polaris** | 100–600 numeric [S] | **1** [S] | **tinted** `rgba(26,26,26)` [S] | surface-led + bevel [S] | bevel + shadow combined [S] | **yes** (inset/bevel/border-inset) [S] |
| **Primer** | sm/md/lg + semantic [S] | multi (DTCG composite) [S] | black-alpha [J] | theme-swapped [J] | shadow separate from canvas [J] | via composites [S] |
| **Fluent 2** | 2/4/8/16/28/64 [S] | **2** (key+ambient) [S] | black-alpha; **brand-tinted variants** [S] | **HEAVIER in dark** (14%→28%) [S] | shadow tokens + `shadow{n}Brand` [S] | — |
| **Spectrum** | drop-shadow tied to elevation [S~] | 1–2 [J] | black-alpha [J] | token-swapped [J] | shadow indicates elevation [S~] | tooling [S~] |
| **Tailwind v3** | sm/DEFAULT/md/lg/xl/2xl/inner [S] | 2 (sm/2xl=1) [S] | black-alpha [S] | no dark variant [S] | none [S] | **yes** `shadow-inner` [S] |
| **Radix** | shadow-1…6 [S] | **3–5 + hairline** [S] | **tinted** `gray-a*`+`black-a*` [S] | alpha → auto-adapts [S] | own outline layer; panels separate [S] | shadow-1 inset [S] |
| **Apple HIG** | materials (not numeric tokens) [S~] | system-rendered | system | materials/vibrancy, not author shadows [S~] | materials [S~] | n/a |

---

## Per-question synthesis (condensed)

**Q1 — layers.** Three tiers: single (Carbon, Polaris, Tailwind sm/2xl); **2-layer key+ambient** (Fluent explicit, Tailwind defaults, NB — the pragmatic centre [J]); multi-layer 3–6 "smooth shadow" (Radix, Comeau/Ahlin). 2 layers is mainstream; 5–6 is high-fidelity but heavy for tokens that round-trip to Figma.

**Q2 — steps + naming.** **6 is convergent** (M3, Radix, Fluent, NB). Numeric/t-shirt for the primitive ramp + **semantic component aliases** (card→md, dropdown→lg, dialog→xl) is the landing [J].

**Q3 — light/dark (central).** Three patterns, all sourced: (a) M3 surface-tint LIFT (overlay %s above; keeps shadow *and* adds tonal lift; overlay is the primary dark signal because shadows are hard to see in dark); (b) heavier shadow in dark (Fluent 14%→28%, NB); (c) surface-only (Radix alpha-adaptive; Vercel/Stripe). **Convergent/recommended 2026 [J, high]: LIFT-primary with a retained-but-reduced shadow** — M3 + Atlassian. Resolves the NB↔practice tension: side with the lift POV (it matches M3/Atlassian), but don't *null* the shadow at the top steps; reject heavier-in-dark as the default (it's the minority and fights the physics).

**Q4 — colour.** Pure black (Tailwind) is the lazy default. The better systems **tint**: Polaris `rgba(26,26,26)`, Radix `gray-a*` (theme-hued), Fluent brand-shadows, Comeau "match the hue, reduce saturation/lightness." For agency/marketing, **tinting toward the brand/surface hue is the realism lever that matters most.** Opacity per step (Polaris 7→28%, Tailwind ~10% with a 25% top, Fluent 14/28).

**Q5 — two-axis.** M3 = one elevation concept resolving per theme; **Atlassian = the cleanest explicit split** (`elevation.surface.*` ⊕ `elevation.shadow.*`, "always pair"); component mapping card→raised, dialog→overlay. The right architecture [J]: two primitive axes joined by a semantic `elevation.N` that picks `{surface-step, shadow-step}` per mode.

**Q6 — real numbers.** Tailwind: `md = 0 4px 6px -1px /.1, 0 2px 4px -2px /.1` … `2xl = 0 25px 50px -12px /.25` (offsetY≈blur×0.7, spread negative-growing). Polaris (1-layer, tinted): `300 = 0 4px 6px -2px rgba(26,26,26,.20)` … `600 = 0 20px 20px -8px rgba(26,26,26,.28)`. Radix (multi + outline, alpha-tinted). All: **offsetX 0**, offsetY/blur grow, spread negative to keep big shadows tight, opacity drifts up at the top.

**Q7 — inset + focus.** Inset is tokenized but secondary (Tailwind `shadow-inner`, Polaris inset/bevel, Radix shadow-1). **Focus rings are kept separate everywhere** — a distinct token family; keep them out of the shadow ramp.

**Q8 — generation lever.** Comeau's blueprint: one global light source (offsetX 0 = light above, which is what NB/Polaris/Radix/Tailwind all do); offset + blur grow with elevation; spread negative-growing; **tint, don't use pure black.** The right knob [J]: a **`softness`** (blur:offset ratio) personality dial — low = crisp/product (Carbon, Fluent), high = soft/marketing (Comeau, Stripe) — plus a **`tint`** (hue + amount). Two layers from the same step index: a tight high-alpha key + a soft low-alpha ambient.

---

## Recommendation (full)

**Steps:** 6 (`xs–2xl`) + inset; semantic component aliases on top. **Layers:** 2 (key + ambient); optional high-fidelity profile later. **Light/dark:** LIFT-primary, shadow retained-but-reduced — drive dark elevation via the tinted neutral surface ladder + white-alpha lift overlays (seed on M3's 5/7/8/9/11/12/14% curve), keep a reduced shadow at the top steps (not null, not heavier); expose heavier-in-dark as a non-default toggle. **Colour:** tinted near-black by default (surface hue), `tint` knob for brand-hued shadows; alpha from a black-alpha ramp, re-resolving per mode. **Architecture:** two primitive axes joined by one semantic `elevation.{step}` (Atlassian split); components alias the level. **Lever:** `softness` (the personality dial) + `tint` (hue+amount), fed through deterministic per-step functions (offsetX 0; offsetY geometric in index; blur = offsetY×softness; spread negative-growing; key+ambient split from the same index).

**Sourced vs judgement:** sourced — the 6-step convergence, 2-layer centre of gravity, M3 overlay curve, the lift-primary direction, tinting precedent, the offset/blur/spread shape, focus-stays-separate. Judgement (anchored) — exact per-step offsets/opacity, the dark reduction curve, the softness function.

## Sources
- M3 elevation/tokens + dark overlay: m3.material.io/styles/elevation/tokens; m2.material.io/design/color/dark-theme.html [S~]
- Tailwind v3 box-shadow: v3.tailwindcss.com/docs/box-shadow [S]
- Polaris shadow tokens (values, tint, inset/bevel): polaris-react.shopify.com/tokens/shadow [S]
- Atlassian elevation split + dark lift: atlassian.design/foundations/elevation [S]
- Fluent 2 key+ambient, light/dark opacity, brand shadows: fluent2.microsoft.design/elevation [S]
- Radix shadows (multi-layer, alpha-tint, inset): radix-ui.com/themes/docs/theme/shadows [S]
- Carbon box-shadow: github.com/carbon-design-system/carbon …/_box-shadow.scss [S]
- Primer box-shadow + DTCG composite: primer.style/product/css-utilities/box-shadow [S]
- Comeau / Ahlin layered shadows + generation: joshwcomeau.com/css/designing-shadows [S]
- Apple HIG materials/depth (system-rendered): developer.apple.com/design/human-interface-guidelines/foundations/materials [S~]

**Gaps:** Spectrum and exact M3 *shadow* (not overlay) px didn't render from primary pages [gap]; M3 overlay %s are the long-published standard, corroborated but not re-pulled live [S~]; Atlassian/Primer don't publish raw px [gap].

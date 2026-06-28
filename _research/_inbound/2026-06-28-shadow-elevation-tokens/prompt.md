You are researching **how mature design systems tokenize elevation / shadow** for
a senior design systems practitioner at a digital agency. The output is a
structured knowledge document.

This designs a white-label shadow generator and resolves a concrete tension: the
reference brands ship 6 sizes × 2 modes of 2-layer black-rgba shadows whose *dark*
shadows are HEAVIER than light, while the practice's existing POV (dark mode =
lighter surface, shadow fades) is the opposite. We need the field's verdict, the
real numbers, and the right generation model — for product AND marketing-expressive
work.

This is not an introductory guide — assume the reader knows design tokens, DTCG
composite shadows, the umbra/penumbra idea, and dark mode. Explain the *model*
(layers, light/dark, colour, the surface↔shadow architecture, the generation
lever) and the *numbers*, not the basics.

Research scope — cover all of the following; verify load-bearing claims against
current primary docs/source; date version-dependent claims; flag confidence.

1. **Shape: single vs multi-layer.** The key-light + ambient-light (umbra/
   penumbra) model; the modern "layered/smooth shadow" technique; how many layers
   shipping systems use per elevation.
2. **Step count + naming** — numeric/dp vs t-shirt vs semantic (card/dialog).
3. **Light vs dark — the central question.** Lift (M3 surface-tint) vs heavier
   shadow in dark vs surface-only. Which is convergent in 2026, and why. Get M3's
   dark overlay values and whether it retains a shadow in dark.
4. **Shadow colour** — pure black-alpha vs tinted/brand-hued; real opacity per step.
5. **The two-axis relationship** — surface ladder + shadow joined by a semantic
   elevation token (Atlassian's `elevation.surface.*` vs `elevation.shadow.*`).
6. **Real numbers** — per-step offsetY/blur/spread/opacity from 2–3 systems.
7. **Inset/inner shadows + focus** — do systems tokenize inset; keep focus separate.
8. **Generation lever** — the right knob to derive a shadow ramp from a small input
   (softness / ambient intensity / light angle), and the deterministic functions.

Output format: comparison table across ≥8 systems (M3/Material, Carbon, Atlassian,
Polaris, Primer, Fluent, Spectrum, Tailwind, Radix, Apple HIG) first; then per-
question synthesis; then a concrete recommendation for a white-label generator
(step count + names, layer count, light/dark model, shadow colour, surface↔shadow
pairing, generation lever) with rationale and citations. Flag sourced vs judgement.

Depth: Expert audience. Resolve the heavier-shadow-in-dark vs lift tension with
evidence; give numbers a generator can be validated against.

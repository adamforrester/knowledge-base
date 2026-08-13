# Follow-up queue — gradient tokens (one outstanding run)

> A single-item follow-up to the 2026-06-28 Prism3 research batch (now archived,
> promoted). The gradient run was filed **after** that batch was promoted, so it
> was not part of it. This note carries it forward. Move to `_archive/` once
> promoted.

## The run
`_research/_inbound/2026-06-29-gradient-tokens/` (`prompt.md` + `claude.md`).
Single-sided (claude.md only); heavily primary-sourced (DTCG 2025.10 + issue #101,
10-system field survey, Figma Plugin/REST API). Either run the external agent on
the same `prompt.md` and reconcile, or accept `claude.md` (it already drove a
shipped engine axis — low-risk to single-source). State which path you took.

## Why it isn't already covered
`12-figma-practice` (just promoted) covers the Figma Styles **mechanism** — Paint
is one of the four style types, a gradient can't be a variable, styles are
plugin-only to create. That's the plumbing. What's still missing is the gradient
**tokenization POV**:

- Gradients are the **most-skipped token category** — most mature systems abstain
  (Material/Carbon/Atlassian/Primer/USWDS); Polaris/SLDS deprecated theirs; only
  Fluent ships a real composite. So the practice stance is "thin and opt-in," not
  "every system needs gradient tokens."
- The **DTCG `gradient` type is stops-only** — `{color, position}` array; stop
  colours can be references; **kind/angle/interpolation are omitted** (issue #101).
- Where it's done well, **stops alias the colour ramp** (Fluent/Carbon), never raw
  CSS strings (the deprecated Polaris/SLDS trap) → themeable, dark-mode-via-
  semantic-stops.
- **OKLCH interpolation** (CSS Color 4, Baseline) avoids the grey dead zone; since
  **Figma interpolates in sRGB only**, a portable gradient carries an OKLCH
  definition **plus** a pre-sampled multi-stop sRGB approximation for the Paint Style.
- **Text-on-gradient** must clear contrast at the **worst-case stop**, not the average.

## Where to promote
- A gradient subsection in **`12-figma-practice`** (extends its Variables-vs-Styles
  material — gradients are the Paint Style case: only stop colours bind, kind/angle/
  positions baked, sRGB-only interpolation).
- A short note in **`31-color-systems`** (gradients as colour-adjacent: stops alias
  the ramp, OKLCH interpolation, worst-case-stop contrast for text overlays).
- Cross-ref from **`22-token-architecture-extensions`** (it already lists `gradient`
  in the DTCG `$type` allowlist; tie to the materialization-directive pattern).

## Engineering context (optional)
The Prism3 engine shipped an opt-in gradient axis on this run — see
`Prism3/docs/05-token-coverage-roadmap.md` (Gradients = Done) and the engine
`README` "Gradient axis" section in the *prism3-tokens* repo, same branch.

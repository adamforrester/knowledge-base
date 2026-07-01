# Build validation — the extract→generate pipeline, run end-to-end

*Recorded 2026-07-01. This note is the build-side evidence backing the "Validated,
not just proposed" paragraph promoted into `15-ai-in-ds.md` (§Extract vs. generate).
The research run beside it (`claude.md`) is the desk POV; this is what happened when
the POV was actually built and run. Source of record lives in the Prism3 repo
(`adamforrester/prism3-tokens`, branch `claude/prism3-e2e-integration-8fwul4`):
`Prism3/engine/spike-wendys.ts`, `Prism3/engine/classify-colors.ts`,
`Prism3/engine/standard-design-md.ts`, and the generated
`Prism3/engine/wendys-fidelity-report.md`.*

---

## What was run

A real, spec-conformant `design.md` produced by the `brand-skills` extractor (a
full Wendy's brand: 24 colour swatches, 25 typography roles, spacing, radius, and
elevation) was fed through the Prism3 generation engine end-to-end. Three additive
spike pieces bridged the two tools without touching either's shipped pipeline:

- a **standard-`design.md` reader** — reads the open-spec frontmatter shape (flat
  `colors` hex map + structured `typography`/`rounded`/`spacing`/`elevation`), a
  different shape from the engine's own brand-input frontmatter;
- a **colour-role classifier** — the one genuinely new parser the bridge needed:
  it reads the flat `colors:` map into engine anchors by naming convention
  (`primary` → pinned anchor; `secondary`/`tertiary` → additional brand palettes;
  `neutral-<step>` → a derived neutral hue/chroma; `success`/`warning`/`error` →
  status, with `error` mapped to the engine's internal `danger` role);
- a **runner** that classifies, maps the optional `x-prism3` levers, generates the
  full system, and writes the fidelity report.

## Measured results (the evidence)

- **Exact-anchor preservation held.** The pinned brand red reproduced at **ΔE00
  0.00** against the observed value — the anchor is never shifted.
- **Generation diverges from extraction, on purpose, and the report surfaces it.**
  The generated ramp, status, and neutral steps sat at an **aggregate ΔE00 ≈ 2.0**
  from the observed swatches (individual neutrals mostly under 1.5; a bright cyan
  secondary tint diverged ~7.6 where the engine tapered chroma toward gamut). The
  engine *places* steps by contrast role and generates a status ramp from hue +
  chroma rather than copying the observed lightness — so divergence is expected,
  and the report is the artefact that puts each deviation to a decision instead of
  hiding it. This is the extract-vs-generate split, measured.
- **The namespaced extension round-tripped.** An `x-prism3` block (engine-only
  levers — `radiusScale`, `typeScale`, density, motion tempo, action palette,
  icon contrast, surface overrides, gradients), invisible to the base spec, was
  emitted by the extractor from `surfaces.md` and consumed by the engine. Neither
  tool forks the format. The real Wendy's file carried no block, so it compiled on
  engine defaults — the "a plain spec file just works" guarantee, confirmed.
- **Accessibility lives in generation — demonstrated, not asserted.** The brief's
  own prose claimed its brand red cleared "~4.6:1" on white and told authors to
  use a darker shade for small text. The engine *measured* the real ratio at
  **5.88:1** — the brief's stated contrast was stale for its own hex (it fit a
  different red the brand also documents). A describer stated a contrast that was
  wrong; only per-contract measurement in the generator caught it. The brief also
  shipped a destructive red identical to a brand shade and an `info` colour
  identical to its `secondary`; the engine carved a distinct danger ramp and
  synthesised an accessible `info` role the brand never supplied.

## Gates

The engine's contracts held on the generated Wendy's system: every DTCG alias
resolved (627/627) and every cross-mode contrast contract passed (248/248), with
the engine's own regression + unit gates unchanged (189/189, NB regression,
aurora/harbor). The extractor side (`brand-skills`) landed the matching alignment
— type-role vocabulary, the colour-role naming contract, and the optional
`x-prism3` block — with its suite green (159 → 162).

## What this changes upstream

The POV in `15-ai-in-ds` and gap `09 §1.34` were written as synthesised direction
with a standing "re-verify before anything is built" caveat. The build is now
done: extract-vs-generate, the fidelity report, and the namespaced-extension
discipline are validated with numbers. The remaining watch-item is unchanged and
external — `design.md` is still an alpha standard; re-verify its version and
stability before naming it in a client proposal.

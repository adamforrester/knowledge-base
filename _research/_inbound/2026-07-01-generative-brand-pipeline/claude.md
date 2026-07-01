# The generative brand pipeline — design.md interop & the extract→generate split

*Claude's run of the dual-agent brief. Researched 2026-07-01 against the primary
`design.md` repository (`github.com/google-labs-code/design.md`, fetched today),
the W3C DTCG 2025.10 spec, and the practice's own token/contrast positions.
design.md facts are version-dependent (the spec is **alpha**) and dated/flagged.*

---

## 1. The design brief as an interchange format (the design.md question)

**What it is.** `design.md` is an open format spec — the repo's own words — "for
describing a visual identity to coding agents." A file is two layers in one
document: **YAML front matter** carrying machine-readable tokens (`name`,
`version`, `description`, `colors`, `typography`, `rounded`, `spacing`, and a
`components` block with per-component properties) and a **Markdown body** carrying
human-readable rationale in a canonical section order — Overview, Colors,
Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts.
Humans author it; **AI coding/design agents consume it.** It ships a CLI
(`lint`, `diff`, `export`, `spec`) and a programmatic linter. Licence Apache-2.0.
Status: **version `alpha`**, "under active development, changes expected as it
matures" (design.md repo, fetched 2026-07-01 — re-verify version/stability).

**Where it sits relative to DTCG — the load-bearing framing.** design.md and
DTCG are not competitors; they occupy different layers of the same pipeline.
**DTCG is interchange for the *tokens* — the resolved, downstream values.
design.md is interchange for the *brief* — the design intent, upstream, before a
complete token system exists.** The spec confirms the relationship in code: its
tokens are "inspired by the W3C Design Token Format," and its CLI has an `export`
command that converts to DTCG (and Tailwind). So the natural pipeline is
`design.md (brief) → generate → DTCG (tokens) → Style Dictionary → platforms`.
The design.md file is the *source*; the DTCG file is a *compiled artifact* of it.
This is the same shape the practice already commits to elsewhere — the component
data file as source (30), the voice-and-tone matrix as the verbal-identity brief
that parameterises generation (04) — extended to the *visual*-identity brief. It
is the two-audiences principle (human prose + machine tokens, one source)
applied to the brief itself.

**Adopt or endorse? Apply the procurement test.** The practice's DTCG position
is explicit: a draft is an architectural commitment; a *stable* spec is a
procurement commitment you can name in a contract (per the practice's token
architecture POV). design.md fails that test *today* on one axis only: it is
**alpha**, so it cannot go into a client contract as a named standard the way
DTCG 2025.10 can. On every other axis it is safe to lean into — Apache-2.0
(no legal risk to building on it), export-to-DTCG (low lock-in; if it stalls you
keep the tokens), and a shape that matches where the practice already is
(agent-consumed, prose-plus-data, brief-as-file). **Recommended position:** adopt
it now as an *internal* authoring and interchange convention and as the front
door to a generative engine; pilot it on a real brand; track the spec's march
toward stability — but do **not** yet name it in proposals as a procurement-grade
standard. It is the first credible open standard for the brief layer, which is
worth saying out loud even while it is alpha.

**The extension discipline.** The spec is *lenient*: it accepts unknown section
headings and unknown token names without error — "custom extension keys stay
silent." It does **not** define a formal namespace (`x-`) mechanism. Silent
tolerance is convenient and dangerous: an extension key that one tool ignores and
another treats as load-bearing is a drift vector that no validator will catch.
The practice's discipline should be the one it already applies to DTCG's
`$extensions` — **namespace extensions explicitly and document their schema**
rather than relying on silence. Prefix tool-specific keys (an `x-` or a vendor
key), write down what they mean, and treat conformance-plus-namespaced-extension
as the way to add the engine's needs without forking the spec. That gives the
interoperability the silent-unknowns rule only pretends to.

## 2. The extract → generate split (descriptive vs generative)

These are two fundamentally different operations, and conflating them is the
central mistake. **Extraction is descriptive**: a tool ingests real brand assets
(a site, a logo, a PDF) and emits a *snapshot* of what is observably there —
these colours, this type, this spacing. **Generation is generative**: an engine
takes a few *anchors* from that snapshot and produces a *complete, accessible,
moded* system — the full ramp, the semantic layer, the light/dark modes, the
`on-*` pairs.

**The accessibility value lives in generation, not extraction — this is the POV.**
An extractor can only observe what exists, and what exists is almost always
incomplete and often inaccessible: a brand ships a primary and two accents, not a
contrast-verified eleven-step ramp; it has no dark-mode surface tokens; its
primary rarely passes contrast on white, so a naïvely extracted `on-primary`
would fail. You cannot *observe* your way to an accessible system. The generator
is what *produces* the accessibility: the contrast-anchored ramp, the modes, the
luminance-flipped `on-*` foreground pairs, the role completeness. This is exactly
the practice's existing Generative Token pattern (a handful of primitives produce
the semantic layer mechanically — 24) and its contrast-anchored ramp discipline
(31), named as a pipeline stage: **extraction gives you anchors; generation gives
you the system.**

**The anchor concept.** The discipline is knowing what the generator legitimately
takes as *fixed* versus what it *computes*. Fixed anchors: the brand's actual
primary value, the real display and text faces, perhaps a spacing base — the
things that are genuinely the brand and must not be invented. Computed: the ramp
steps, the semantic mappings, the contrast pairs, the modes, the dark surfaces.
Pin the anchors; generate the rest.

## 3. The fidelity-report pattern

Generating from anchors introduces a specific risk: the generated value silently
diverges from the brand's observed value — the generator's "step 5" is not quite
the brand blue anyone actually uses. The pattern that closes this: **pin the exact
brand anchor, generate the ramp, then emit a report of every place the generated
value diverges from the observed/extracted one.** Nothing changes behind the
practitioner's back; every deviation is surfaced for a decision.

The right framing is a **regression artifact** — a diff, in the same family as a
test snapshot or the practice's Cascade Report (the CI artifact that shows what a
token change moves — 24). It belongs at **build time**, as a reviewable output and
ideally a CI gate: a generation run that diverges from the pinned brand beyond a
threshold fails or warns, exactly as a contrast violation does. The fidelity
report is what makes "generate the system from anchors" safe to run repeatedly —
it converts silent drift into an explicit, reviewable delta.

## 4. The "one generator" / standalone-vs-pipeline completeness principle

When a tool is one stage of a larger owned pipeline, it must still be
**independently useful**. Two consequences that look contradictory but aren't:
the extractor stays a *complete descriptive tool* — a user who runs only the
extractor and stops still gets a usable brand snapshot — *and* the engine does
**not trust** the extractor's derived ramps as final; it regenerates from the
anchors. The extractor is honest about what it is (a describer); the engine owns
the generation.

The general principle for an owned multi-tool toolchain: **one source of
computation.** Each tool stands alone at its own job, but any given piece of logic
is *derived in exactly one place*. The failure mode is two tools each re-deriving
the same thing — an extractor that "helpfully" generates a ramp and an engine that
also generates one, now drifting apart, so the output depends on which tool ran
last. Design so the extractor describes and the engine generates, and the boundary
between them is a clean handoff (anchors), not two overlapping brains.

## 5. Owned-toolchain architecture — consolidation and the portable core

**The tool-switching cost.** A designer who must open a theming plugin, then a
text-style-binding plugin, then a style-guide-generator plugin, in sequence, to
get one system materialised, pays a real friction-and-error tax — and worse, each
plugin that re-implements shared logic is a drift source. The consolidation
question is not "fewer tools is better" but "do these tools share a core
computation?" When they do, collapse them to **one surface over a shared engine**;
when they are genuinely different jobs, keep them separate.

**The portable-core / thin-adapter pattern is the enabler.** The engine core is
the brain — framework-agnostic, testable, one implementation of the generation
and materialisation logic. A Figma plugin, a CLI, and a web app are then **thin
materialisation adapters** over that core, not second brains. The plugin's job is
to *translate the core's output into Figma API calls*, nothing more; it does not
re-derive the ramp or re-decide the semantic mapping. This is the structural fix
for the drift the practice already warns about when designers hand-reassemble
Figma styles that then diverge from the tokens: **plugin-as-materialization-adapter
means there is nothing to reassemble — the plugin materialises what the one brain
already computed.** "One brain, many surfaces."

## 6. Naming-convention contracts as the interoperability layer

For tools in a pipeline to understand each other, they need **shared vocabularies**,
and naming is that integration contract — not a style preference. If the extractor
emits `brand-blue` and the engine expects `primary`, they cannot compose without a
translation layer nobody maintains. The two vocabularies that have to be shared
across extraction, generation, and code: a **colour-role vocabulary**
(`primary` / `secondary` / `tertiary` / `neutral-<step>` / `success` / `warning` /
`error` / `info`) and a **single type-role vocabulary** (the function-named ladder,
not appearance names). Agreed once, they are the contract every stage reads and
writes against; drifting them per-tool re-introduces exactly the translation
tax the pipeline was meant to remove. This connects the pipeline back to the
practice's existing naming POV (foundations naming; token architecture) — naming
discipline is not just for the token file, it is the seam that lets an owned
toolchain interoperate at all.

## References

- **design.md** — `github.com/google-labs-code/design.md` (format spec, CLI,
  schema; Apache-2.0; version **alpha**, fetched 2026-07-01 — re-verify).
- **W3C DTCG 2025.10** — `designtokens.org/tr/2025.10/format/` (the token-
  interchange layer design.md exports to and sits above).
- **Contrast** — WCAG 2.2 (SC 1.4.3/1.4.11) and APCA (the accessibility the
  generation step produces and the fidelity/contrast gate enforces).
- **Generative-ramp precedent** — Adobe Leonardo (contrast-anchored ramp
  generation) and Material 3 HCT dynamic colour (anchor→system generation) as
  prior art for "generation creates the accessible ramp."
- **Vault connections (for synthesis, not external sources):** 15 §Brand-book to
  token architecture (the AI extract→propose→validate flow this refines); 24
  §Generative Token pattern and §Cascade Report (the generation mechanics and the
  regression-artifact family); 31 (contrast-anchored ramps, `on-X` pairs); 30
  (data file as source); 04 (voice-and-tone matrix as the verbal-identity brief);
  02 §3 / 22 (naming as architecture).

## Confidence ledger

- **VERIFIED (primary, fetched today):** design.md's structure (YAML front matter
  + prose sections), its stated purpose (visual identity for coding agents), the
  CLI verbs, Apache-2.0, the DTCG-inspired tokens + export-to-DTCG, the alpha
  status, the silent-unknown-keys tolerance.
- **PRACTICE POV (not a field survey):** the brief-interchange-vs-token-interchange
  layering; the procurement test verdict (adopt-internally / don't-yet-name);
  the namespace-your-extensions discipline; accessibility-lives-in-generation;
  the fidelity-report-as-CI-artifact; one-brain-many-surfaces; naming-as-contract.
  These are the practice's reasoning grounded in real engine-building (the Prism3
  E2E work) and existing vault positions, not claims of external consensus.
- **DATE-SENSITIVE:** design.md is alpha and moving; the version, the extension
  mechanism, and the CLI surface should be re-checked before anything load-bearing
  is built or promised on them.

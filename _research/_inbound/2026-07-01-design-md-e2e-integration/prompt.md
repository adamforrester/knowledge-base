# Research intake — design.md interop & the extract→generate brand pipeline

> **Source:** gaps surfaced while building the Prism3 token engine's E2E pipeline
> (the `prism3-tokens` repo, `Prism3/docs/07-e2e-journey.md` §11). Logged here so the
> practice POV isn't lost. These are candidate research runs / new-file topics — none
> is authoritative yet. Durable POV, once synthesised, lands in a numbered file
> (likely `05-development-support`, `15-ai-in-design-systems`, `22-token-architecture-
> extensions`, or a new numbered file) and/or `09-gaps-and-open-questions`.
>
> Not written by the dual-agent run convention yet — this is a **brief** enumerating the
> gaps so the KB agent can scope prompts and pick up the work.

---

## Context (one paragraph)

Prism3 is a generative token engine (small brand input → a complete, contrast-verified,
moded token system). Its authoring front door is a **`design.md`** file. The owner also
built a **brand-extraction tool** (`brand-skills`) that ingests brand assets and emits a
`design.md` that follows the open **[`google-labs-code/design.md`](https://github.com/google-labs-code/design.md)**
standard, plus a Figma **Token Press** exporter and three *separate* Figma plugins (theming,
text-style binding, style-guide generation). Wiring these owner-built tools into one E2E
pipeline surfaced several POV gaps the vault does not yet cover.

## The gaps (each a candidate research run / POV note)

1. **`design.md` as a design-system interchange standard.** The vault has **no committed
   POV** on a design-brief-as-a-file that drives generation (confirmed in a prior KB sweep;
   closest are §30 "component data file is source" and §04 "voice-and-tone matrix as system
   prompt"). Now there's an *open standard* (`google-labs-code/design.md`). Questions: should
   the practice adopt/endorse it as the brand→system interchange format? How does it relate
   to DTCG (interchange for *tokens*) — `design.md` is interchange for the *brief*, upstream
   of tokens? Conformance-plus-extension (namespaced `x-*` keys) as the pattern for
   tool-specific needs without forking the spec.

2. **The extract → generate split (descriptive vs generative).** A brand *extractor* produces
   a **descriptive** snapshot (observed colours/type/space); a *generative engine* turns a few
   **anchors** from that snapshot into a complete, accessible, moded system. POV: the
   generation step is where the accessibility value lives (contrast contracts, modes, on-*
   pairs) — extraction alone can't produce it. Includes the **fidelity-report pattern**:
   generate from anchors, pin the exact brand anchor, then report where the generated ramp
   diverges from the observed values so nothing changes silently (a regression-style artifact).

3. **The "one generator" principle + standalone-vs-pipeline completeness.** When a tool is one
   stage of a larger owned pipeline, it must still be **independently useful**. Concretely:
   the extractor stays a complete descriptive tool (a user who stops there still gets usable
   output); the engine simply doesn't *trust* the extractor's ramps as final — it regenerates.
   POV on designing an owned multi-tool toolchain so each tool stands alone *and* composes.

4. **Tool consolidation — minimising designer tool-switching.** Multiple single-purpose Figma
   plugins (theme variables / bind text styles / generate a style guide) that a designer opens
   in sequence → one plugin over a shared, portable engine core ("one brain, many surfaces").
   A dev-support / tooling POV: when to consolidate vs keep separate; the portable-core
   pattern as the consolidation enabler; the **plugin-as-materialization-adapter** idea (the
   engine core is the brain; the plugin is a thin Figma-facing adapter, not a second brain —
   avoids the drift the vault already warns about for hand-reassembled Figma styles).

5. **Cross-tool naming-convention contracts as the interoperability layer.** For tools to
   "understand each other," they need shared vocabularies: colour-role names
   (`primary`/`secondary`/`tertiary`/`neutral-<step>`/`success`/`warning`/`error`/`info`) and
   a single **type-role vocabulary** across extraction, generation, and code. POV on naming as
   the integration contract (connects to §02 foundations naming + §22 token architecture).

6. **Font-weight named-instance mapping (declare once).** Custom fonts vary in weight *and* in
   the *spelling* of named instances ("Semi Bold" vs "Semibold"); declaring the weight-role →
   named-instance map once (in the brief) and resolving it against Figma's loaded fonts at
   materialization. A Figma-pipeline POV (connects to the Figma variables/styles round-trip
   research already in `_inbound/2026-06-28-figma-variables-styles-roundtrip`).

## Suggested priority

(2) and (4) are the most reusable practice POVs (they generalise beyond Prism3). (1) is
timely (an open standard is emerging). (3), (5), (6) are supporting notes that can fold into
(2)/(4) or a numbered file rather than standalone runs.

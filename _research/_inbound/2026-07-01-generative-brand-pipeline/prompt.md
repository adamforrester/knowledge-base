You are researching the generative brand pipeline — a `design.md`-style brand
brief that drives a generative token engine — for a senior design systems
practitioner at a digital agency. The output is a structured knowledge document.

The gap this fills: the practice's vault has a committed POV on tokens as an
interchange format (DTCG) and on the component data file as a source of truth,
but no committed POV on a *design brief as a file that drives generation*, on
the split between *extracting* an existing brand and *generating* a complete
system from a few anchors, or on how to architect an owned multi-tool
generative toolchain. An open standard has just emerged in this space
(`google-labs-code/design.md`, Apache-2.0, alpha as of mid-2026), and generative
token engines (small brand input → a complete, contrast-verified, moded token
system) are now real. This research should let the practice take a position.

This is not an introductory guide — assume the reader knows what design tokens,
DTCG, and a design system are, and knows the difference between a primitive and
a semantic token. Explain the non-obvious: where a brief-as-file belongs
relative to tokens, why generation (not extraction) is where accessibility
value is created, and how an owned toolchain stays coherent.

Research scope — cover all of the following:

1. The design brief as an interchange format (the `design.md` question)
- What a `design.md`-class file is: machine-readable tokens plus human-readable
  rationale in one file, authored by humans, consumed by coding/design agents.
  Its actual structure and status (version, licence, stability).
- Where it sits relative to DTCG: is it interchange for the *brief* (upstream,
  the design intent) versus DTCG as interchange for the *tokens* (downstream,
  the resolved values)? Do they compete or compose (e.g. export-to-DTCG)?
- Should a practice adopt or endorse an alpha open standard? The
  procurement-grade test the practice applies to DTCG, applied here.
- The extension discipline: how a tool adds its own needs without forking the
  spec — namespaced/`x-`-style keys, the spec's own tolerance for unknown keys,
  and whether "silent unknown keys" is safe or needs a documented schema.

2. The extract → generate split (descriptive vs generative)
- The two fundamentally different operations: a brand *extractor* produces a
  *descriptive* snapshot (observed colours, type, spacing from real assets); a
  generative *engine* turns a few *anchors* from that snapshot into a complete,
  accessible, moded system.
- Why the accessibility value lives in generation, not extraction: contrast
  contracts, light/dark modes, `on-*` foreground pairs, and role completeness
  are *produced* by the generator; an extractor can only observe what exists,
  which is usually incomplete and often inaccessible.
- The anchor concept: what a generator legitimately takes as fixed input (the
  brand's actual primary, a real display face) versus what it computes.

3. The fidelity-report pattern
- Generating from anchors risks silently changing brand values. The pattern:
  pin the exact brand anchor, generate the ramp, then emit a report of where
  the generated values diverge from the observed/extracted values.
- The framing as a regression artifact — a diff nothing changes silently
  behind — and where it belongs in the pipeline (a build-time artifact, a
  reviewable output, a CI gate).

3. The "one generator" / standalone-vs-pipeline completeness principle
- When a tool is one stage of a larger owned pipeline, it must still be
  independently useful. The extractor stays a complete descriptive tool (a user
  who stops there gets usable output); the engine simply does not *trust* the
  extractor's derived ramps as final — it regenerates from anchors.
- The general principle for designing an owned multi-tool toolchain so each tool
  stands alone *and* composes; the single-source-of-computation ("one brain")
  idea and its inverse failure (two tools each re-deriving the same thing and
  drifting).

4. Owned-toolchain architecture — consolidation and the portable core
- The tool-switching cost: multiple single-purpose plugins a user opens in
  sequence versus one surface over a shared engine. When to consolidate and when
  to keep separate.
- The portable-core / thin-adapter pattern: the engine core is the brain; a
  Figma plugin (or a CLI, or a web app) is a thin materialisation adapter, not a
  second brain. How this avoids the drift that comes from re-implementing logic
  per surface.

5. Naming-convention contracts as the interoperability layer
- For tools to understand each other they need shared vocabularies: colour-role
  names and a single type-role vocabulary shared across extraction, generation,
  and code. Naming as the integration contract, not just a style choice.

Output format: Structured markdown. Use section headings that match the numbered
scope above. Synthesize findings — do not list sources mechanically. Where the
field has consensus, state it clearly; where decisions are context-dependent,
provide decision frameworks rather than declaring a winner. Flag where the tools
(the `design.md` spec, Figma's variable/style write surface, Style Dictionary,
generative engines) have known gaps that practitioners work around. Where claims
depend on current platform state — spec version, licence, feature flags — date
them and note the verification path. Include a references section linking to
primary sources (the `design.md` repo and spec, DTCG, generative-token tooling,
contrast/accessibility specs).

Depth: Expert audience. Do not explain what a design token or DTCG is — explain
where a brief-as-file belongs in the pipeline, why generation creates the
accessibility value extraction cannot, and how an owned toolchain stays coherent.

# Prompt — how do shipping design systems encode inverse / on-emphasis surface context?

Run date: 2026-08-23. Filed for prism3's two-collection colour split.

**Single-agent run.** No second pass. `_research/README.md` defines a run as one prompt against two
agents so convergence can count as evidence; that corroboration is absent here. What partly offsets
it: the load-bearing findings are reads of **published token source and vendor documentation**, so
they are re-checkable rather than merely agreed-with. Read the confidence accordingly.

---

## The architecture under test

Prism3 splits colour into two Figma collections:

```
color.appearance — the VALUES,   4 modes: light, dark, hc-light, hc-dark
color.surface    — the POINTERS, 2 modes: default, inverse
```

A component binds once to a pointer (`color/background/primary`) and gets the right value in any
appearance × surface combination without knowing which. **Surface context is encoded as a MODE on a
pointer tier, not as distinct token names.**

## The question

Find out what shipping design systems actually do about inverse / on-emphasis surface contexts, and
whether anyone encodes it this way.

**DO NOT SET OUT TO CONFIRM THIS.** *"Nobody does this"* is a completely acceptable and useful
finding — it would say we are either ahead or solving a constraint others do not have, and both are
worth knowing. A confirmation-shaped answer is worse than useless here, because it will be checked by
a skeptical developer.

## Priority order

1. **Adobe Spectrum**, and Adobe's AEM / Experience Cloud surfaces built on it. Spectrum ships
   `static-white`/`static-black` as its paired-contrast foreground — find out whether it ALSO has a
   surface-context or inverse concept, how it is encoded (token names? sets? Spectrum 2's colour
   system?), and whether Spectrum ships Figma variables with modes.
2. **Systems shipping Figma Variables with multi-dimensional modes and a strong inverse context** —
   Material 3, Primer, Polaris, Carbon, Fluent, Atlassian.
3. **Anyone who splits collections BY AXIS rather than by tier.** The sharpest version:
   Material/Tokens-Studio's ref-vs-sys split is a TIER split and is well documented; an AXIS split
   (one collection per varying dimension) is what we did and is what we cannot find precedent for.

## For each system, answer specifically

- Is there an inverse / on-emphasis / on-color surface context at all?
- Is it a MODE, a separate token set, a name segment, or a runtime computation?
- **Does a component binding change when the context changes, or does the same binding resolve
  differently?**
- If they ship Figma variables: how many collections, split by what?

**That third bullet is the crux.** Our claim is that the same binding resolving differently is what
makes components context-agnostic. If other systems make the component swap bindings instead, say so
plainly — that is a real alternative and the developer's objection may be exactly it.

## Already held — cite, do not re-derive

- KB `31-color-systems.md` §1 (the `on-*` pair token is universal across seven systems, with
  per-system names) and §4 (orthogonal axes; mode resolution at the alias, never the consumer).
- prism3 `docs/06` §7b (the locked two-tier decision, grounded in the Material / Tokens-Studio
  ref-vs-sys split).
- prism3 `docs/00-progress.md`, #1082 entry (our own measurement: 2560/0 vs 1050/1510).

## Sourcing rules

Primary sources only — published documentation, token repositories, public Figma libraries. Date
every claim; several of these systems changed materially in 2025–26 and stale specifics are the main
risk. Where you cannot verify something, say so and flag it as needing a source rather than inferring
it from a system's general reputation. **If a system's public docs and its shipped tokens disagree,
that disagreement is itself a finding.**

## Output

A research run under `_research/_inbound/`. If it produces a durable position, note what belongs in
`31-color-systems.md` and open an issue for the promotion — do not edit the numbered file in the same
run. If it turns up a genuine gap in the practice's POV, that is a `09` entry.

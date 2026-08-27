# Prompt — Figma extended collections, the undocumented-behaviour claim, and closing the survey

Run date: 2026-08-23. Second run, following `_research/_inbound/2026-08-21-inverse-surface-context-encoding/`
(KB PR #26, promotion issue #27, gap #28).

**Single-agent run**, as the first was. The corroboration the dual-agent convention exists to produce
is absent. Offsetting it: nearly every load-bearing claim here is a quote from vendor API
documentation, which is re-checkable rather than merely agreed-with.

---

## Standing rule, carried from the first run

**A confirmation-shaped answer is worse than useless.** *"Nobody does this"* and *"we were wrong"*
are both acceptable and useful findings.

## Priority 1 — Figma extended collections. The new thread.

The owner raised it and neither of us can vouch for how it works. It is potentially a **third
option**: a Figma-native mechanism for *"override these tokens to their inverse"*, where the
overriding collection is connected to a parent.

From primary sources only — Figma's own documentation, changelog and release notes:

- What exactly is an extended collection? When did it ship?
- Can a collection extend another and override individual values?
- **Do modes compose across the extension boundary, or does the child get its own independent modes?**
- Is it library-scoped only, or usable within one file?
- **What happens to a component bound to a token in the parent when the child overrides it — does the
  binding follow?**

That last question is the one that matters. If an extension gives component-agnosticism **without**
depending on undocumented cross-collection alias resolution, it beats what prism3 ships on the one
axis where prism3 is exposed.

**Do not speculate.** If Figma's documentation does not answer a question, say so — *"undocumented"*
is itself a finding here, since it is exactly what the first run discovered about cross-collection
mode resolution.

## Priority 2 — the undocumented behaviour prism3 depends on

The first run's strongest finding was that Figma does not document how a cross-collection alias
resolves when two collections' modes are set independently on one frame. **Hunt for a primary source
that confirms or denies it** — docs, changelog, developer forum posts from Figma staff, the plugin API
typings. If it genuinely is undocumented, say so **with the searches that were run**, so the claim is
durable rather than an absence of evidence.

## Priority 3 — close the survey

- **Spectrum's shipped token files, not docs.** The first run read docs for three of four systems;
  this is where a docs/tokens disagreement would show. Also settle whether Spectrum ships Figma
  variables at all, which priority 1 of the first run left open.
- **Polaris, Fluent, Atlassian** — the three never reached. Same four questions per system, especially
  **whether the component binding changes when the ground changes.**

Then #27's caveat resolves: either the claim covers seven systems, or it stays scoped to four and says
so.

## Context

An engine lane is measuring the internal cost in parallel — how many of the 128 pointer roles actually
flip, and how many component variants name-encoding would add. **That measurement, not this survey, is
likely to decide the question.** This run's job is to make sure the decision is not taken in ignorance
of a Figma feature that would change the options.

## Output

A research run under `_research/_inbound/`. Note what belongs in `31-color-systems.md` and open a
promotion issue; do not edit the numbered file in the same run. Post the extended-collections finding
to prism3 **#1127** as well, since that is where the decision lives.

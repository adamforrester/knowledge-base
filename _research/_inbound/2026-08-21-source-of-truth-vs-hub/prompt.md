# Prompt — one source with many projections, or a hub that reconciles many origins?

Run date: 2026-08-21. Filed for prism3 issue #876.

**Two agents were run against this brief**: Claude (in-repo, `claude.md`, 2026-08-21) and Gemini
(`gemini.md`, captured 2026-08-23). **Read `PROVENANCE.md` first** — the second run arrived two days
after the first synthesis was published, and what was reconciled against in the interim was a report
whose provenance could not be established.

---

## The brief, as issued

> I need a research report on a design-system architecture decision: whether a design system should
> treat ONE artifact as the source that everything else is generated from, or run a HUB that
> normalizes and reconciles intent expressed in several places.

### Context, written so the agent needs no prior knowledge of the system

A team builds a design-system engine. Its token layer (colors, spacing, typography) is GENERATED from
a small brand input — a few parameters in, a complete token set out. For tokens there is genuinely one
origin, so "one source, many projections" is not a philosophy there, it is a fact.

Their component layer works differently. A component definition is AUTHORED by a person — its
anatomy, its variants, its states, its token bindings. From that definition they generate a Figma
component, design-tool metadata, documentation, and (soon) a code projection consisting of semantic
CSS classes over server-rendered HTML.

**The problem.** A component definition is authored, not generated. So the moment a designer changes
something in Figma, or an engineer discovers a behavior gap or an accessibility fix while
implementing, design intent has been expressed somewhere OTHER than the definition. The architecture
currently has no way to absorb either — there is no Figma-to-definition path and no code-to-definition
path. Today that is fine because nobody authors in those places. The decision is what happens when
they do.

**The alternative posture.** A respected practitioner (Nathan Curtis, "Spec-driven UI component
development", Aug 2026) argues for the opposite: a specs layer that is not THE source of truth but a
place that "normalizes, synchronizes, and versions the intent expressed across the many
origins-of-truth." He explicitly includes engineers as authors of design intent: "Engineers express
design intent, too. As they work, they'll evolve and extend API, identify and resolve accessibility
issues, and fill behavior gaps designers hadn't considered. That's design work, just not done by a
designer." He is building four sync edges — Figma-to-specs, specs-to-Figma, specs-to-prototype,
prototype-to-specs — rather than one.

### What I need answered

Six questions, priority order. Cite sources with URLs and dates. State plainly what you could not
determine.

1. **What actually breaks in single-source design systems when authorship turns out to be
   multi-origin?** Find real accounts — postmortems, conference talks, engineering blogs, maintainer
   retrospectives. I want the failure MODE described concretely, not the theory. Does the source
   artifact go stale? Do people stop using it? Does a shadow source emerge? How long does it take?
2. **What does a hub actually cost to run?** Find teams that built bidirectional sync between design
   tools and code. What did they spend, what broke, and is it still running? I am especially
   interested in systems that were ABANDONED — a hub that was built and then retired tells you more
   than one that is still being promoted by the team that built it.
3. **The round-trip problem specifically.** Bidirectional Figma-to-code sync has been attempted many
   times. What is the actual state of the art in 2026? Where does it succeed (tokens? simple
   components?) and where does it reliably fail (layout? behavior? composition?)? Is there a
   principled line between what round-trips and what does not?
4. **Conflict resolution.** In any multi-origin system, two origins eventually disagree. How do real
   systems handle that — automatic merge, last-write-wins, human reconciliation queue, origin
   precedence rules? What do practitioners say actually works versus what sounds good in a diagram?
5. **The documentation question**, which is a live disagreement. Curtis argues that "how to use" docs
   should originate from CODED IMPLEMENTATIONS rather than from specs, because code is where the real
   API lives. The single-source position is that docs generate from the definition. Which do real
   teams do, and what goes wrong with each? Is there evidence either way about docs drifting from
   reality?
6. **The middle path, if one exists.** Is there a documented posture between "one source, everything
   generated" and "a hub with N bidirectional edges"? Specifically: a single source that accepts
   IMPORTS from other origins but requires a human to reconcile them, rather than merging
   automatically. Has anyone built that, and what is it called? If it is a known pattern I want its
   name and its tradeoffs.

### Format

A section per question. Open with a one-paragraph direct answer to "should a system whose token layer
is genuinely single-origin, but whose component layer is authored, plan to become a hub — and if so,
when?" Then the evidence. Then a section on what you could NOT determine.

### Standing constraint

Do not resolve this toward whichever option sounds more modern. Both postures are internally
consistent and the question is empirical — what actually happens to teams over time. **If the evidence
is thin or mostly vendor marketing, say that plainly; that itself is the finding.**

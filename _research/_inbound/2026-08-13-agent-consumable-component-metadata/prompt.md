# Research intake — what has gone wrong for systems publishing machine-readable component data

> Standalone research pass, feeding a POV document the owner is writing in parallel. **Findings, not
> recommendations.** Run per `_research/README.md`; this folder holds the brief and the raw outputs.

---

**The question:** what has actually gone wrong for systems that publish structured, machine-readable
component data for agents and tools to consume? Not what they built — what their users complain about,
what they had to change, and what they regret.

**Candidates worth reading, not exhaustive:** Supernova, Astryx (Meta), zeroheight, Specs / Directed
Edges, Backlight, Knapsack, Storybook's docgen and metadata surfaces, Radix/Ark/Zag where they publish
component metadata, and any design-token or design-system MCP servers now shipping. Read GitHub issues,
changelogs, migration guides, community threads — the same method that found the Style Dictionary and
Edge Delivery answers.

**Four things specifically:**

1. **Context and payload size.** Has anyone shipped a component metadata surface an agent could not usefully consume because it was too large? What did they do — tiering, retrieval, summarization? Any published numbers at all.
2. **Schema churn.** Where structured component data is versioned and consumers depend on it, what broke? Did anyone version their component name surface separately from their content, the way this repo splits engine version from contract version?
3. **The metadata-versus-implementation split.** Do these systems keep one file per component or several? If several, what determined the split — and did anyone start with one and have to split it, or vice versa?
4. **Consistency across a catalogue.** Anything on enforcing that components in one system share prop vocabularies, state names and API shape — automated, reviewed, or not at all. This is the part with the least evidence and the least expected to be written about.

**Method:** fetch and cite with dates, say plainly where a claim can't be verified, and flag where a
vendor's marketing and its issue tracker disagree — that gap was the most useful signal in the AEM pass.

**One caution.** Most of this category positions itself as agent-ready right now. Read the positioning
as a claim to check, not a finding. The gap between "agentic platform" on a landing page and a working
agent surface is the gap this repo spent months closing for itself.

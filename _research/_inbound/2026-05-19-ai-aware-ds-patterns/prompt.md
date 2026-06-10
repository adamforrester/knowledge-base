You are researching AI-aware design system patterns and conversational-UI primitives for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: in 2024–2026 a number of mainstream design systems began publishing patterns and components for AI features — chat input, streaming response rendering, source attribution, refusal UI, conversation primitives, agent affordances. The field is in a transitional state: some publishers (Carbon Labs, eBay MIND) treat AI as an explicit pattern library; others have shipped one or two AI-specific components inside an otherwise general DS; others are alleged to have AI-aware patterns but on inspection do not. This research is the field survey that distinguishes the three. The reader is scoping engagements where clients ask for "AI features" and needs to know which patterns are mature enough to adopt vs. invent, where the field is converging vs. diverging, and where the hidden complexity sits (governance, evaluation, content) beyond the component layer.

This is not an introductory guide — assume the reader knows what a design system is, what a token is, what an MCP server is, what RAG is at a high level, and what a "human-in-the-loop" pattern is. Explain the *patterns shipped by these systems* and the *architectural decisions behind them*, not what an AI assistant is.

Specifically not in scope: introducing what conversational UI is, defending why DS practices should care about AI, recapping LLM mechanics. Those positions are settled. The question this research answers is: "given the 18 listed sources plus anything else the field has published, what patterns are actually shipping, what is mature vs. emerging, and where is the field converging vs. diverging?"

## Sources to investigate

The following 18 systems were cited in a recent LinkedIn post as having published AI-aware patterns. The post may have overclaimed; treat the list as a starting set, not a confirmed inventory. For each source, navigate the site to locate the AI content (likely places: Patterns or Components index, What's New / changelog / blog, an explicit AI / GenAI / Copilot / Assistant subsection). For deep-linked URLs, treat the linked page as the entry point first.

- shadcn/ui — https://ui.shadcn.com/
- HeroUI — https://heroui.com/
- Mantine — https://mantine.dev/
- Elisa Design System — https://designsystem.elisa.fi/9b207b2c3/p/155e65-elisa-design-system *(deep link)*
- Amazon Cloudscape — https://cloudscape.design/
- ServiceNow Horizon — https://horizon.servicenow.com/
- SAP — https://www.sap.com/design-system
- Tailwind — https://tailwindcss.com/
- Power Apps Playbook — https://playbook.powerapp.cloud/
- New York State Design System — https://designsystem.ny.gov/ *(public-sector outlier — treat separately)*
- MUI — https://mui.com/
- Fluent UI — https://developer.microsoft.com/en-us/fluentui#/
- daisyUI — https://daisyui.com/
- Lightning (Salesforce) — https://www.lightningdesignsystem.com/2e1ef8501/p/85bd85-lightning-design-system-2 *(deep link)*
- Paste (Twilio) — https://paste.twilio.design/
- Carbon — https://carbondesignsystem.com/ *(also see Carbon Labs at https://github.com/carbon-design-system/carbon-labs — the explicit AI incubation space; high-priority target)*
- Primer (GitHub) — https://primer.style/
- eBay MIND Patterns — https://ebay.gitbook.io/mindpatterns *(MIND is specifically positioned as an AI pattern library — high priority)*

If a system on this list does not appear to publish AI-specific patterns, say so plainly and move on rather than fabricating coverage. The negative finding is itself a research output. State at the end: which of the 18 you accessed, which you couldn't, and which appear not to publish AI patterns despite the post's claim.

If your research surfaces *additional* systems not on the list that have published meaningful AI patterns (e.g. Atlassian's Compass / Rovo Atlassian Intelligence work, Vercel's AI SDK UI primitives, Shopify Polaris updates, OpenAI's published design guidance, Google's Gemini-related Material 3 updates), include them and flag where they came from. The goal is field accuracy, not source-list compliance.

## Research scope — cover all of the following. Use these as the section spine of the output.

1. **The shape of the field — what "AI-aware" actually means in 2026**

   - The distinction between (a) AI-features the DS *operates* (token critique, codegen, MCP-served metadata) and (b) AI-features the DS *ships as patterns to consumers* (chat input, streaming response, citation rendering, refusal UI). This research is scoped to (b).
   - Why these patterns started landing in mainstream DSs in 2024–2026. The forcing functions (Copilot enablement, agent platforms, conversational product surfaces moving from experimental to first-class).
   - The spectrum of publisher posture: pattern library (eBay MIND), incubation space (Carbon Labs), single-component ships (most), prose-only principles (some), no published AI content (some, despite claims).

2. **Landscape survey — the 18 plus extensions, grouped by maturity tier**

   - Production-grade: explicit AI pattern coverage, multiple shipped components, governance / principles documentation. Name names; cite the published patterns directly.
   - Emerging: one or two AI-specific components in an otherwise general DS, often labelled experimental / beta.
   - Experimental / labs: pattern fragments, blog posts, design explorations not yet promoted to the published library.
   - Principles-only: prose / guidelines without component-level expression.
   - Not-actually-publishing: systems on the source list that do not, on inspection, ship AI-aware patterns. Distinguish "could not access" from "accessed and not present."
   - Treat New York State separately as a public-sector outlier — the constraints (Section 508 / WCAG legal exposure, AI disclosure laws beginning to land at state level, civic-trust framing, FOIL / open-records obligations on AI-assisted decisions) sit under a different governance regime than the SaaS systems and deserve their own short treatment.

3. **The pattern taxonomy — clusters that emerge from the source material**

   Initial hypothesis (let the source material reshape this — if three systems converge on a category that isn't named here, name it; if a hypothesised cluster turns out empty, drop it):

   - **Prompt input** — text affordances, slash commands, context attachment, suggestion chips, quote/cite-back from conversation context.
   - **Generative response rendering** — streaming, structured / tool-result rendering, "show your work" panels, code blocks with run/copy affordances, multi-block composition.
   - **Trust, transparency, attribution** — AI disclosure, confidence indicators, source citations, refusal / "I cannot do that" patterns, "AI-generated" badges, watermarking.
   - **Feedback and correction** — thumbs / rating, regenerate, edit-prompt, correct-the-output, report-issue, structured feedback for evals.
   - **Conversation primitives** — message threading, multi-turn affordances, context windows, agent handoff, tool-use disclosure, tool-call result rendering.
   - **Governance / principles** — prose docs that sit alongside the components: when to show disclosure, what counts as a refusal, content policy linkage, evaluation criteria.

   For each cluster: anatomy notes (what the pattern minimally contains), which systems exemplify it best, and where the field is *converging* (most systems agree on the shape) vs. *diverging* (multiple incompatible approaches in production at the same time). The divergence is the strategically interesting territory; flag it explicitly.

4. **Tooling and implementation reality — what's available off-the-shelf vs. what needs custom work**

   - Open-source primitives: Vercel AI SDK UI (`useChat`, streaming), shadcn/ui's chat components if they exist, Tailwind UI, the Carbon Labs React components, eBay MIND's published references. State what each actually ships.
   - Where the OSS layer ends and bespoke work begins — multi-modal input, agent-step rendering, tool-call UX, source attribution UX, evaluation hooks.
   - The gap between Figma kits and code primitives — which systems publish AI patterns in Figma at all, and where the round-trip breaks.
   - The role of MCP / structured metadata in serving AI-aware components to AI agents (the meta-recursion: AI patterns that are themselves AI-readable).

5. **Architecture and governance — what shipping AI patterns actually requires**

   - The four-prerequisite minimum that turns AI-pattern shipping into more than UI cosmetics: components-as-data, structured metadata, evaluation contracts, content / safety governance.
   - The eval loop — what makes a refusal pattern *correct*, what makes a citation *correct*, how this gets validated in CI.
   - The content-governance seam — AI patterns presume a content layer (sources, retrieval corpus, allowed tool surfaces) that the DS does not own. Where the DS contract ends.
   - Disclosure regimes — voluntary disclosure (industry pattern), legally-required disclosure (EU AI Act tiers, US state AI disclosure laws beginning 2024–2026, public-sector obligations). Verify against current regulatory state.

6. **Failure modes — common ways AI-in-DS goes wrong**

   - Assumed maturity — clients believe the published patterns are mature when they are emerging or experimental.
   - Component-level shipping without governance / eval — the visible UI works, the back-end behaviour is undefined.
   - Design-led patterns without engineering buy-in on the eval / safety side.
   - Disclosure theatre — a badge that satisfies a checklist without changing user understanding.
   - Streaming-as-novelty — a streaming UI that doesn't actually carry information faster than a structured non-streaming response.
   - Citation patterns that surface sources without the user being able to verify them.
   - Refusal patterns that are inconsistent across the same product surface.
   - One-off agent UIs that diverge from the rest of the DS — the AI surface as its own walled DS.

7. **Open questions and contested territory**

   - Where the field has not converged as of mid-2026 — flag these as decision territory rather than declaring a winner.
   - Where the published patterns lag what frontier products (ChatGPT, Claude, Gemini, Cursor, Copilot) are shipping — and what that gap implies for DS adoption strategy.
   - Where governance / regulation is moving faster than the pattern library — and what that means for systems being scoped today.

Output format: Structured markdown using the numbered scope above as the section spine. Synthesize across sources — do not list one system at a time. Where the field has clear consensus, state it; where decisions are context-dependent, give a decision framework. Cite specific systems / specific URLs inline when a claim is load-bearing — every claim about a system must be traceable to a fetched source. Where claims depend on platform / spec / regulatory state — feature names, version flags, statute numbers, EU AI Act tier definitions, US state AI disclosure laws — date the claim and note the verification path (the system's changelog, the regulator's publication, the W3C / ISO spec). Where the source survey produces a negative finding (a system on the list that doesn't actually publish AI patterns), state it plainly. Include a references section linking to primary sources.

Depth: Expert audience. Do not explain what conversational UI is or what an LLM does. Explain the architectural decisions behind the published patterns, where the field is converging vs. diverging, and what scoping implications fall out of the survey for someone building an AI-feature engagement on top of an existing or new DS.

End with three short statements:
(a) Which of the 18 listed sources you couldn't access or didn't actually have AI patterns published.
(b) Which clusters in the proposed taxonomy you reshaped (added, merged, dropped, renamed) and why.
(c) Anything that surprised you — convergence where you expected divergence, divergence where you expected convergence, a publisher posture you didn't anticipate.

You are researching how AI tools, agents, and workflows are changing design systems practice from end to end — from token creation through component build, documentation, developer handoff, and ongoing governance. The audience is a senior design systems practitioner at a digital agency. The output is a structured knowledge document. This is not a survey of AI tools in general — it is specifically about how AI integrates into and accelerates design system work.

Research scope — cover all of the following:

1. AI in token creation and validation

Using AI to generate, validate, and critique token taxonomies — naming conventions, semantic layer structure, hierarchy completeness
AI-assisted contrast and accessibility checking during token definition
Automated token audit: tools or prompts that identify missing semantic tokens, naming inconsistencies, or orphaned primitives
Using AI to translate a brand book or style guide into a structured token architecture

2. AI in Figma — design operations

Figma's native AI features as of 2025/2026: what they do, what they're useful for in DS work, and what they don't do well
Figma MCP (Model Context Protocol) server: what it exposes to AI agents, practical use cases for DS work (inspecting component structure, reading variables, generating design context)
Figma Console MCP: what it is and how it extends AI interaction with Figma
AI-assisted component creation in Figma: generating variants, adjusting properties, applying tokens
Limits of current Figma AI for DS work — where human judgment is still required

3. AI in component development

Using AI coding assistants (Claude Code, Cursor, Copilot) to generate component code from Figma specs or design tokens
Nathan Curtis's Specs CLI (https://github.com/DirectedEdges/specs) and his "Components as Data" article (https://medium.com/@nathanacurtis/components-as-data-2be178777f21): the components-as-data POV — that a component definition is structured data (YAML/JSON), platform-neutral, with anatomy / props / default / variants, and that Figma assets, code, and documentation are outputs generated from that data rather than independently authored. How Specs CLI bridges Figma component specs to developer context for AI-assisted coding.
Prompt strategies for generating accessible, token-compliant component code
AI-assisted variant generation: generating component states and variants from a base implementation
Code review and quality assurance: using AI to validate generated component code for token compliance, accessibility issues, naming consistency

4. AI in documentation generation

Generating component usage guidelines from component structure and properties
AI-assisted writing of usage guidelines, avoid-when documentation, prop tables
Keeping documentation in sync with component changes — AI as a documentation maintenance tool
Storybook and AI: generating stories from component implementations

5. AI in design-to-development handoff

Current state of AI-powered design-to-code: Figma to component code, Figma to token pipeline
Code Connect (Figma's feature linking design components to code): current maturity, integration with AI workflows
How MCP servers (Figma MCP, Specs CLI, custom DS MCP servers) give AI coding assistants access to DS context — the architecture and the practical workflow
The difference between AI that generates code from a screenshot vs. AI that generates code with full DS context

6. AI in governance and ongoing maintenance

Using AI to detect design drift: components in production that deviate from DS specifications
AI-assisted coverage analysis: identifying UI patterns in a product that aren't yet in the DS
Automated changelog and versioning assistance
AI for contribution workflow: reviewing proposed components against DS standards

7. AI-ready DS architecture

Components-as-data as the architectural prerequisite. The argument that AI-in-DS workflows fail or succeed on whether the component is defined as structured data — anatomy, props, variants, slots, metadata — that AI agents can query, reason about, and generate from. Without this layer, AI tools are extracting whatever they can infer from a Figma file or a code snippet, which is "stochastic, incomplete, and imprecise" (Curtis on Dev Mode MCP, 2024). With this layer, AI tools have a contract to generate against. Cover what the structured data layer must contain and how it relates to Figma Variables, DTCG tokens, and component code.
What makes a design system "AI-readable" — metadata, structured documentation, token semantics, component schemas
W3C DTCG token format as an AI-parseable structure
Component card / metadata schema patterns for giving AI agents structured DS knowledge
MCP server architecture for a design system: exposing DS knowledge to AI tools in a structured, queryable way

8. Current limits and honest assessment

Where AI in DS work is genuinely useful today vs. where it is aspirational
Quality and consistency issues in AI-generated components
Organizational and governance challenges of AI-assisted contribution
What still requires human judgment and will for the foreseeable future

Output format: Structured markdown. Use section headings that match the numbered scope above. Prioritize what is shipping and usable today over what is announced or experimental. When tools are named, note their current maturity level (GA, beta, preview, experimental, deprecated). Where the field has consensus, state it clearly; where decisions are context-dependent (e.g., MCP-first vs. screenshot-first design-to-code, custom DS MCP server vs. relying on Figma MCP alone, AI as contribution gate vs. advisory), provide decision frameworks rather than declaring a winner. Flag areas where the tooling has known gaps practitioners work around. This topic is fast-moving — every specific feature name, plan-tier capability, MCP tool surface, and AI assistant integration claim should be dated and marked with a verification path; specifics that read as confident assertions today will be inaccurate within months. Include a references section covering: Figma AI documentation, Figma MCP documentation, Nathan Curtis's Specs CLI (github.com/DirectedEdges/specs) and "Components as Data" (medium.com/@nathanacurtis/components-as-data-2be178777f21), relevant MCP server implementations, and practitioner writeups on AI in DS workflows.

Particular focus: The end-to-end workflow connecting components-as-data → MCP-exposed DS context → AI coding assistant → token-compliant component code → documentation is a high-priority area. Synthesize the current state of this workflow with honest assessment of where it works, where the gaps are, and what minimum DS architecture (specifically: components-as-data plus DTCG-compliant tokens plus structured component metadata) is required for it to work at all. The contention to evaluate: AI-in-DS workflows that don't sit on a components-as-data foundation are extracting design intent from artifacts that weren't built to express it, and produce inconsistent results as a consequence.

Depth: Expert audience. Do not survey AI tools in general or explain how AI coding assistants work — explain how DS context is exposed to them, what minimum architecture the DS must provide, and what consumers do with the result.

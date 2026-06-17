# MCPs as practitioner tooling for design-systems work — the workstation stack at agency scale

The practitioner-MCP story is two stories. The first — *MCPs as architecture* — is about a custom DS MCP server that exposes a specific client's components-as-data through a structured tool surface. That story is substantially closed by the field's existing literature and by this practice's prior work (15-ai-in-ds names the seven-tool conceptual surface — `list_components`, `get_component`, `search_components`, `get_token_catalog`, `get_composition_rules`, `get_usage_guidelines`, `validate_implementation`; 30-generated-from-data-documentation prices the build-out at 40–80 hours and locates it in Phase 3 of the AI-readiness adoption arc). It's the *system-as-data* dimension of the broader MCP question; the customary answer is well-shaped.

The second story — *MCPs as practitioner tooling* — is about the off-the-shelf MCP servers that sit on a senior DS practitioner's workstation and turn their MCP-capable AI clients (Claude Code, Cursor, Windsurf, the agentic surfaces of 2026) into useful collaborators on day-to-day DS work. This story is mostly undocumented. The senior practitioners who use Figma Console MCP routinely, who reach for firecrawl when WebFetch truncates, who have axe-core wired into their Storybook addon stack and read it through the AI client — these practitioners are operating the workstation stack as a discipline. The discipline is not articulated.

This document closes that gap. Seven sections in order: why the workstation stack is its own discipline (and not the custom-DS-MCP build-out); the Figma-side MCPs; the component-side MCPs; the accessibility-scanner MCPs; the token-side MCPs; the web-research MCPs; and the default workstation config as the practice's standardisation IP.

A note on currency before anything else. This space rotates faster than any other DS topic in this vault — faster than 15 even, because practitioner MCPs are mostly third-party or first-generation tooling and the maintainers ship weekly. Specific tool surfaces, plan-tier dependencies, and capability claims below reflect mid-2026 platform state; verify against current docs before treating any specific claim as load-bearing in client work. The architectural shape — workstation MCPs are general-purpose, custom DS MCPs are engagement-specific, both compose, the workstation stack standardises practitioner velocity — is more durable than the tool names attached to it. Bet on the architecture, not on the tool.

---

## 1. Why the practitioner-MCP stack is a discipline of its own

### Two layers, two questions, two payback shapes

The practitioner-workstation MCP stack and the custom-DS-MCP-server architecture are different axes of the broader MCP story. Both involve MCP servers. Both deliver leverage to MCP-capable AI clients. They answer different questions and pay back along different curves.

The **custom DS MCP server** answers the question: *how does a specific client's design system expose itself to AI clients as a structured contract?* The answer is the seven-tool surface 15 names — the AI client calls `get_component`, gets the structured data shape, calls `get_composition_rules`, learns what this component composes with, calls `validate_implementation`, gets back a structural conformance check. The server is built once per client (or per portfolio when the practice's white-label or multi-brand work permits — per 24's tokens-at-scale framing). The shape is system-specific; the IP transfers to the client at handoff (per 32 §1's failure-mode catalogue, the client owns the system's instance from day one — and the system's MCP server is part of the instance).

The **practitioner-workstation MCP stack** answers a different question: *what tools should a senior DS practitioner have configured by default on their workstation, regardless of which client they're currently working with?* The answer is a stack of general-purpose, off-the-shelf (or lightly-wrapped) MCP servers — Figma MCP, Storybook MCP, axe-core MCP, design-token MCP, firecrawl MCP — that read whatever Figma file, whatever Storybook, whatever component library, whatever spec is currently in front of the practitioner. The stack is engagement-agnostic; the IP is the practitioner's, not the client's.

The two layers compose. The senior practitioner who has both configured can move fluidly between them within a single session. The Figma MCP reads the *current engagement's* Figma file generically. The custom DS MCP reads the same engagement's components-as-data shape with the client's opinionated contract. The practitioner asks the AI client to compare a contributed component against the contract; the AI client calls the custom DS MCP for the contract, calls Figma MCP for the design source, calls Storybook MCP for the implementation reality, and returns a three-way reconciliation. None of the three MCPs alone produces this — the composition is what produces the practitioner's leverage.

The **payback curves are different and worth naming**. The custom DS MCP server pays back per-engagement: it's a 40–80-hour line item in the SOW (per 30); it produces deliverables (the structured contract becomes the AI-readability evidence); it transfers to the client at handoff. The investment is amortised against the engagement's revenue. The workstation stack pays back across the practitioner's *career*: every engagement benefits from the same configured stack; every audit moves faster because the AI client has the right tools wired up; every primary-source verification is one firecrawl call instead of fifteen browser tabs. The investment is amortised against the practitioner's lifetime work.

This payback distinction matters commercially. The agency that prices custom DS MCP servers as billable line items and treats workstation MCPs as "tooling overhead" gets the commercial relationship right. The agency that conflates the two — bills clients for workstation-stack setup, or worse, treats workstation-stack expertise as a per-engagement build — loses on both ends: clients see workstation tooling as agency-internal hygiene and resent the bill; the agency loses the commercial wedge of the custom DS MCP server because it's been blurred together with general workstation work.

### What the workstation stack delivers in concrete day-to-day DS work

The cost-of-not-having the workstation stack is calculable, and naming a few of the routine workflows makes the case concrete.

**Per-component documentation generation.** A senior designer has finished a component in Figma; the implementation has shipped to Storybook; the docs page hasn't been written. Without the stack: the designer reads the Figma file, walks the Storybook story, opens the per-component docs template (29's seventeen-section spine), and writes the page in roughly two to four hours. With the stack: the designer asks the AI client to read the Figma file via Figma MCP, read the Storybook story via Storybook MCP, and emit a docs page following the 29 template. The AI client returns a draft in fifteen to thirty minutes; the designer reviews, edits the parts the AI got wrong (typically the usage guidance and the design-rationale sections), and ships in roughly an hour. Speed-up is 2–4×; the bottleneck shifts from authoring to review.

**Token-tree dead-token detection.** The practitioner is auditing a multi-brand token system at the start of an engagement. Without the stack: the practitioner exports the Style Dictionary build output, exports the consumer codebase, writes a custom script (or asks an engineer to write one) that cross-references the token catalogue against the consumer's import statements, runs the script, reads the output, structures the findings. Half a day to a full day. With the stack: the AI client calls the Style Dictionary MCP for the token catalogue, walks the consumer codebase via the AI client's existing file-reading tools, and produces the structured dead-token list. Twenty to forty-five minutes. Speed-up is 6–10×; the practitioner moves to the next audit lane while the previous one's output is being reviewed.

**Primary-source verification.** The practitioner is preparing the §1.27a closure on CSS Color 4 §14.2 (the worked example in this vault's history). Without the stack: WebFetch retrieves a truncated version of the spec; the practitioner manually fetches the spec via browser, reads through the truncation point, copies the relevant body text, structures the citation. Half an hour to an hour, with the additional cost that WebFetch's truncation isn't visible — the practitioner doesn't know what they're missing until they read the full source. With the stack: firecrawl MCP retrieves the full 495K-character document on the first try; the AI client reads the relevant sections; the practitioner reviews the body text and lands the inline correction. Fifteen minutes, with confidence the source is complete. The §1.27a closure was the first worked example of this pattern; the practice's residual cluster (§1.26a–§1.26d + §1.28a–§1.28d, eight items) is the next.

**Bulk Figma operations.** The client has decided to rename a brand-tier token from `color/brand/primary` to `color/brand/accent` across the entire Figma library. Without the stack: the senior designer opens each component, finds each variable reference, updates each one manually. Across a 100-component library with 5,000 references: a week of senior designer time at a minimum, with high error rate. With the stack: Figma Console MCP runs the migration in minutes via a single agent invocation, with the agent's output reviewed before merge. Hours of senior designer time, near-zero error rate. Speed-up is 20–40×.

**Storybook + axe-core PR review.** A product team has contributed a new component variant to the system. Without the stack: the system-team reviewer walks the PR's Storybook story, runs axe DevTools manually against each variant, notes the violations, structures the review comment. Twenty minutes per PR. With the stack: the AI client calls Storybook MCP to read the new stories, calls axe-core MCP to scan each story, structures the review against the contribution-model checklist, drafts the comment. Five minutes per PR; the reviewer edits and posts. Speed-up is 4×; the contribution-model SLA per 07 holds under load that without the stack would force SLA slippage.

These are five examples. The workstation stack delivers similar speed-ups across most of the practitioner's day-to-day work. The aggregate effect across a career is the practice's compounding asset.

### The miscategorisation cost

Two miscategorisations show up in agency proposals and are worth naming.

**Pricing the architecture and skipping the standardisation.** The agency proposes a custom DS MCP server (priced correctly per 30, 40–80 hours), and the proposal is silent on the workstation stack. The senior practitioners on the engagement use the workstation stack anyway — they have it configured personally — but the practice doesn't ship the stack as a standardisation artefact. Two costs: junior practitioners on the engagement don't have the same speed-up; cross-engagement velocity isn't standardised. The agency that produces strong work in the senior tier and inconsistent work in the junior tier is often suffering from this gap.

**Pricing the standardisation and skipping the architecture.** The agency invests in workstation-stack training, runs an internal stack-setup runbook, ensures every senior practitioner has the same MCPs configured. The proposals don't include the custom DS MCP server because the practice hasn't separated the two layers. Result: the practitioner's day-to-day velocity is high; the client's AI-readiness commercial deliverable doesn't ship; the AI-readiness commercial wedge per 30 is missed. The agency that has strong workstation discipline and weak commercial-IP packaging is often suffering from this gap.

The fix is the explicit articulation: workstation stack is *practice IP, agency-internal, career-amortised, never billed to a single client*. Custom DS MCP server is *practice-IP-applied-to-the-client, billable per engagement, amortised against engagement revenue, transferred to the client at handoff*. Both are needed; they're priced differently because they pay back differently.

---

## 2. The Figma-side MCPs — Dev Mode MCP, Console MCP

### Two distinct servers, two distinct surfaces

Figma's MCP story splits into two servers that compose. The official **Figma Dev Mode MCP** is read-only; the third-party **Figma Console MCP** (Southleft) is write-enabled. The senior practitioner has both configured.

**Figma Dev Mode MCP.** Ships with Figma's paid tiers (verify the current tier requirement; mid-2026 places it on Organization and Enterprise plans, with some surface available on Professional). Exposes node structure, variables, Code Connect mappings, layout data, and screenshot retrieval. The AI client calling Dev Mode MCP can read a frame's structure, query the variable collections, follow the Code Connect map to the implementation, and retrieve a rendered image of the node. The surface is the canonical *design-as-source* surface for AI-driven design-to-code work.

**Figma Console MCP** (Southleft). Third-party, write-enabled via a Desktop Bridge plugin. Exposes project-wide context (Dev Mode MCP is per-file; Console MCP can reach across files in a project) and write access — the AI client can create frames, instantiate components, configure variable collections, apply token migrations across thousands of node references, generate exemplar pages from component metadata. The "bootloader" architecture means the plugin loads enough Figma context for the agent to operate against the canvas with structural awareness, not just at the JSON-API level.

### Day-to-day workflows each enables

**Dev Mode MCP workflows.**

- **Design-to-code with structured context.** The dominant workflow as of 2026. The AI client reads the selected node via Dev Mode MCP, follows the Code Connect mapping to the production component, reads the variables consumed by the design, and generates code that imports the real component, uses the real tokens, and respects the system's API contract. The output is what 15 §The practical MCP workflow names as "context-first" code generation — production-ready rather than approximate.
- **Design-token audit (Figma side).** The AI client walks the Figma Variables collections via Dev Mode MCP and reports drift against a stated token catalogue (typically the Style Dictionary build output cross-referenced via the Style Dictionary MCP per §5). The audit surface is the Figma half of the cross-platform output integrity check per 32 §2.1.
- **Component-anatomy extraction.** The AI client reads a component frame and emits a structured anatomy description for documentation. Useful for the per-component docs page generation per 29's template, particularly the anatomy section that without MCP would be hand-authored from the Figma file.
- **Variable-collection inventory.** The AI client walks every Variables collection in the file and produces the inventory for a Discovery audit (per 32 §2.1). The inventory at scale (50+ collections, hundreds of variables) is intractable manually; it's a fifteen-minute query with Dev Mode MCP.

**Console MCP workflows.**

- **Bulk migrations.** The canonical Console MCP workflow. A token rename, a component-property reshuffle, a variable-collection split — operations that touch thousands of node references and that without Console MCP take a senior designer days of manual work. Console MCP runs the migration via a single agent invocation in minutes; the agent's output appears in a Figma branch (or directly in main, depending on configuration; see governance below).
- **Exemplar-page generation.** Given a stated component composition, the AI client generates a usage-example page directly in the Figma file. Useful for documentation and for stakeholder-review surfaces. The generated page is a starting point — the senior designer reviews and refines — but the speed-up is meaningful.
- **Variable-collection authoring.** Given a stated theme spec (typically extracted from a brand-guidelines document or a token JSON file), the AI client creates and configures a multi-mode collection. Mid-2026 reality: the surface works for straightforward color/spacing/typography collections; complex composite types (typography composites with per-script overrides, motion composites with cross-platform spring parameters) are at the edge of what works reliably and benefit from senior review before landing.
- **Template instantiation.** The AI client spawns a frame from a stated component composition — useful for repetitive layout work, particularly in marketing surfaces where the practitioner needs N variants of a hero or card layout.

### Governance — the question Console MCP forces

Write access to the design source raises governance questions that read access doesn't. The MCP-equipped agent can change the design-tool source-of-truth at the speed of generation; without governance discipline, agent-authored changes destabilise the library before human review catches them.

The disciplines that work:

- **Branch-only writes.** Configure Console MCP (or the workflow around it) so agent-authored changes land in a Figma branch, never directly in the main library. The senior designer reviews the branch before merging. The friction is real (branches add a review step) and is appropriate — the alternative is agent-authored chaos in main.
- **Senior review on token migrations.** Agent-authored bulk operations on tokens or core components require explicit senior-designer review before merge. The senior designer reads the full set of changes, not a sample; the speed-up of the operation makes the comprehensive review tractable that wouldn't be tractable manually.
- **Approval-required operations.** Where Console MCP's configuration supports it (verify against current docs), require explicit approval for write operations. The agent proposes the change; the human approves or rejects; the change lands only on approval.
- **The per-engagement Console MCP scope decision.** Some engagements — particularly early-stage ones where the design source is in flux — should not have Console MCP write access enabled. The risk-of-bad-write outweighs the speed-up. The practice's discipline: the senior practitioner makes the scope decision per engagement and documents it.

The pattern that fails: senior practitioner runs Console MCP with default permissions, the agent makes a well-intentioned but incorrect token migration (interpreting the rename request differently than the designer intended), the Figma library is destabilised, the recovery is non-trivial because the operation touched thousands of nodes. Real incidents shape this discipline; the practice that has lived through one such incident enforces the branch-only discipline thereafter.

### Tooling reality and gaps as of mid-2026

- **Variables modes coverage.** Figma Dev Mode MCP doesn't expose Variables modes uniformly across paid tiers. Mid-2026 reality: Organization and Enterprise plans expose modes; Professional may have partial exposure. Verify against current docs.
- **Console MCP installation overhead.** The Desktop Bridge plugin is a workstation-configuration step that adds friction to onboarding. Senior practitioners install it once per machine and forget; junior practitioners encountering it for the first time often need walkthrough. The runbook should cover it explicitly (per §7).
- **Code Connect surface depth.** Both MCPs know there's a Code Connect map but expose it at varying depths. The AI client gets the mapping (this Figma component → this code component) but not always the full template surface (the prop transformations, the import paths, the prop-to-variable bindings). Where the mapping is thin, the AI client falls back to inference, which works less reliably.
- **Prototype layer is largely invisible.** Neither MCP exposes the deep prototype layer — interactions, motion specs, conditional logic — usefully. The AI client gets layout but not behaviour. For motion-heavy work (per 18-21's motion-foundation framing) the practitioner falls back to manual extraction or Figma plugin-based scraping.
- **Console MCP is third-party.** The Console MCP is maintained by Southleft, not Figma. The practice's risk surface includes the maintainer's bus factor; the workstation stack should not depend on Console MCP being available indefinitely. Native Figma write-MCP capability is the durable answer; the practice should track Figma's roadmap for native write-MCP support.

The verification-path discipline is load-bearing: name the capability with a date, verify against current docs before treating as fixed in client work. This applies to all the Figma-side MCPs more strongly than to most other tooling because the surface evolves quarterly.

---

## 3. The component-side MCPs — Storybook MCP and the testing surface

### The canonical practitioner MCP for component-side context

Storybook MCP exposes the component library's published surface to AI clients: the stories, the CSF (Component Story Format) metadata, the args / argTypes / parameters surface, the docs blocks, and the addon-driven integrations (a11y addon, viewport addon, interactions addon, links addon). The AI client reading Storybook MCP knows what components exist in the system, what props they accept, what variants ship, what the documented usage patterns are.

Storybook 8.x ships an MCP surface; Storybook 9 (2025–2026) extended it. The surface evolves quickly; the senior practitioner's discipline is to track the Storybook release notes for MCP-relevant changes and update the workstation config accordingly.

### Day-to-day workflows

- **Component documentation generation.** The dominant workflow. The AI client reads the stories via Storybook MCP and emits a per-component docs page following 29's seventeen-section template. The args-table surface drives the properties section; the play-function surface drives the interaction-states section; the docs-block surface seeds the usage section. The output is a draft; the senior designer or DS lead reviews and edits.
- **API consistency audit.** The AI client compares prop shapes across the component library and flags inconsistencies — `size="small"` on Button vs. `size="sm"` on Input; `tone` vs. `intent` vs. `variant` for semantically equivalent props. The output is the per-prop matrix per 32 §2.2's component-audit lane. Manually constructing the matrix takes hours; with Storybook MCP it's twenty minutes.
- **Migration-codemod authoring.** When the system ships a major release with API changes, the AI client reads the v1 stories and the v3 stories via Storybook MCP, identifies the prop renames / removals / semantic shifts, and emits a codemod that migrates consumer code. The codemod is reviewed and refined; the AI client's output is roughly 70–80% correct on first pass for straightforward additive migrations and lower (40–60%) for breaking migrations that require human judgment about semantic equivalence.
- **Test-coverage analysis.** The AI client cross-references the stories with the test files (visible through the file system, not strictly via Storybook MCP) and flags components without state-coverage stories. The component audit's state-machine-completeness check per 32 §2.2 leans on this output.
- **Implementation-vs-design reconciliation.** The AI client reads Storybook MCP (the implementation reality) and Figma Dev Mode MCP (the design source) and reports drift between the two. The design specifies a 12px gap; the implementation ships an 8px gap. The design specifies a focus indicator with these colours; the implementation ships those colours. The reconciliation is the per-component audit's design-to-code-faithfulness check.
- **Stakeholder-readout assembly.** The AI client reads Storybook MCP for the component surface, reads the Cascade Report (per 24 §3) for the cross-brand impact of recent changes, and structures the executive readout per 08's quarterly governance review template. Useful for the recurring readout that every engagement at Stage 2+ ships.

### The Storybook MCP vs. custom DS MCP distinction — re-stated for the component lane

Storybook MCP is general-purpose: every Storybook ships with the same MCP surface (or close to; tooling caveats apply). The AI client reading Storybook MCP knows what's *shipping* — the implementation reality.

The custom DS MCP server (per 15) is system-specific: exposes the system's *opinionated contract* — composition rules (`get_composition_rules`), usage guidance (`get_usage_guidelines`), validation tools (`validate_implementation`). The AI client reading the custom DS MCP knows what *should be shipping* — the system's intent.

The senior practitioner with both knows the AI client can read both and produce the reconciliation. The reconciliation is itself a useful audit signal: where the Storybook reality matches the system's intent, the system is operating cleanly; where it diverges, the system has accumulated drift that the audit's component lane should surface (per 32 §2.2).

### Tooling reality and gaps as of mid-2026

- **Docs-block content depth.** The args-table surface is excellent; the play-function surface is excellent; the docs-block content is exposed but not always parsed cleanly into structured form. MDX docs blocks with rich custom content can come back as text-blob output that the AI client struggles to structure. The practitioner workflow: prefer args-table-driven docs over heavily-custom MDX where AI consumption is a goal.
- **linkTo and cross-story navigation.** Variable. Some Storybook versions expose linkTo metadata cleanly; others don't. The AI client trying to traverse component-to-component relationships via Storybook MCP may need the practitioner's help.
- **Visual-regression baselines are not exposed.** Chromatic snapshots, Percy baselines, Playwright visual baselines all live in their own surfaces. Storybook MCP knows the stories exist but not the baseline images. The AI client doing visual-regression analysis needs separate Chromatic / Percy / Playwright MCPs (or custom wrapping; mid-2026 vendor-native MCP surfaces are limited).
- **Storybook composition (multi-Storybook setups).** Where the practice ships multiple Storybooks (per-platform: web Storybook, mobile Storybook, marketing Storybook), the AI client needs to know which Storybook to read. Storybook composition's MCP behaviour is worth verifying per setup.
- **Addon-driven extensions.** Each Storybook addon (a11y, viewport, interactions, links, docs, controls, actions, themes, designs, measure, outline) may or may not expose its surface via MCP. The a11y addon's surface is typically well-exposed; others vary. The practitioner's discipline: query the AI client's tool surface to confirm what's available, rather than assuming addon-MCP coverage.

---

## 4. The accessibility-scanner MCPs — automated scanning surfaced as a tool the AI client can call

### The accessibility-side MCPs

- **axe-core MCP** (or equivalents wrapping Deque's axe-core). The canonical scanner. Exposes the rule surface to the AI client; the client calls `scan(url)` or `scan(component_story)` and receives a structured violations list with rule ID, severity, affected element, and remediation guidance.
- **Pa11y MCP.** Wraps Pa11y, which itself wraps axe-core, for CI-friendly use. Exposes the scan surface plus configuration options (rule subsets, viewport sizing, viewport-injected scripts). Useful where the practitioner wants the same surface as the CI pipeline rather than an ad-hoc browser-based scan.
- **Lighthouse MCP.** Broader than a11y but includes the a11y category. Useful for the cross-domain audit (a11y + performance + best practices + SEO) where the practitioner wants a single tool covering multiple lanes.
- **Storybook a11y addon (via Storybook MCP).** Already mentioned in §3 — the per-story a11y rule surface is the canonical practitioner workflow when the system has Storybook stories for every component.

### Day-to-day workflows

- **Per-component a11y scanning during contribution.** The PR review's first pass. The AI client calls Storybook MCP to read the new stories, calls axe-core MCP to scan each story, structures the violations, drafts a review comment. Catches the easy failures (missing labels, contrast regressions in automated cases, heading-hierarchy issues) before the PR opens for human review. The contribution-model SLA per 07 holds because the easy violations are caught at PR-submission time, not at review time.
- **Cross-component a11y pattern audit.** During a Discovery audit (per 32 §2.3), the AI client scans a sample of components and surfaces the recurring patterns — components missing focus-trap implementations, components without `aria-label` on icon-only variants, components with contrast regressions in the dark theme. The pattern-level read informs the audit's accessibility lane findings.
- **Pre-engagement a11y baseline.** Before a productised audit kicks off, the AI client runs a baseline scan against the client's current component surface. The output is the input data for Day 3 of the 5-day audit shape per 32 §3 (the accessibility lane day). The audit's first day gains capacity because the baseline already exists.
- **Conformance-evidence collection.** For regulated-industry audits (EAA, Section 508, ADA Title III per 32 §2.3), the AI client compiles per-criterion test results across the sampled components for the report's regulatory section. The structured violations list maps to WCAG success criteria; the AI client cross-references and compiles. What without MCP is hours of manual evidence-collation becomes a 30-minute compilation.

### The boundary the scanner MCPs do not cross

Automated scanning catches roughly 30–40% of WCAG conformance issues (per Deque's published self-assessment of axe-core's coverage; verify the current figure and the methodology — the "30–40%" is a widely-cited but not-trivially-verified number that deserves source-text backing before client use). The remaining 60–70% require manual AT testing — the four-engine × four-AT matrix per 32 §2.3 plus 28's web-accessibility-implementation framing.

The discipline:

- **Use scanner MCPs for breadth and speed.** The 30–40% the automated scanners catch is the easy-win surface. Catching it at PR-submission time, at Discovery baseline time, at conformance-evidence time — the speed-up is real, the catch rate is consistent.
- **Use real AT testing for depth and authority.** The remaining 60–70% — semantic-structure failures, keyboard-trap issues, focus-management failures, the WCAG-passes-but-fails-real-users pattern per 31 — requires human AT testing across the matrix. No MCP substitutes for it.
- **Don't conflate the two.** The audit that ships automated-scan output as the entire a11y deliverable is failing the audience that pays for accessibility (regulators, AT users, legal). The practice's discipline: every productised audit's a11y lane includes both the scanner-MCP output (breadth) and the manual-matrix output (depth); the report names which evidence comes from which source.

### Tooling gaps

- **Real-AT-testing MCPs do not exist in mid-2026.** No practical MCP server exposes a JAWS / NVDA / VoiceOver / TalkBack surface to an AI client at the depth required for real conformance testing. The cross-AT testing remains manual. The practitioner's bet: this gap closes in 2026–2027 as the AT vendors and the AI-tooling vendors converge; until then, the manual matrix is the practice's discipline.
- **BrowserStack / Sauce Labs do not ship MCP-native surfaces.** They expose programmatic APIs that an MCP wrapper can consume; the wrapping is custom work (typically 8–16 hours for a workstation MCP that covers a single VM-based AT-driven test). Most practitioners run the matrix manually with the remote-desktop surface rather than wrapping it.
- **Per-rule severity calibration drifts.** axe-core's rule severities update with each release; rules deprecate; new rules land; the practitioner's audit-template severity model (per 32 §4) needs to track. The audit-the-audit discipline per 32 §5's silent-failure modes covers this — the threshold drift failure mode applies to scanner-MCP rule sets specifically.
- **Multi-rule-set wrangling.** A regulated-industry audit may need to scan against WCAG 2.1 AA (the EAA baseline) *and* WCAG 2.0 AA (the Section 508 baseline) *and* WCAG 2.2 AA (the practice's working standard). Scanner MCPs configure per-scan; running multi-ruleset scans requires multiple scan invocations. The practitioner's workflow: configure the scan rule-set explicitly per regulatory context.

---

## 5. The token-side MCPs — design-token authoring, validation, audit

### The token-side MCPs

- **Style Dictionary MCP wrapper** (custom). Style Dictionary v4 (late 2024 / early 2025) and v5 (2025–2026) expose enough of the resolver and dependency-graph surface that custom MCP wrapping is straightforward. The wrapper exposes the build pipeline's dependency graph: the AI client can walk from any token to its primitive root, identify dead tokens, surface alias-resolution failures, generate the Cascade Report per 24 §3 on primitive changes.
- **Tokens Studio MCP** (or Tokens Studio API exposed via custom MCP). Tokens Studio's API has been stable enough to wrap since 2024–2025. The MCP surface exposes the design-tool side of the token tree — the AI client can read the Figma Variables structure, read the Tokens Studio JSON, validate against DTCG conformance, audit composite-typography-token fidelity per 23's typography framing.
- **Specify MCP**, **Knapsack MCP**, **Supernova MCP**. Each design-token-platform vendor exposes a programmatic API; MCP wrappers exist (custom or community) at varying maturity. None ships native MCP as of mid-2026; verify against current vendor docs as the surfaces may have shifted by the time anyone reads this. The practitioner's bet: native MCP surfaces will land in 2026–2027 from these vendors specifically because the AI-readiness commercial pressure is on them.
- **The Tokens Studio graph engine specifically.** Tokens Studio's visual graph view of token dependencies is the practitioner-visible surface; the API behind it is what an MCP wrapper exposes programmatically. The AI client with graph-engine access can trace any token's full dependency surface in milliseconds — the operation a senior practitioner does manually in minutes. The leverage compounds on multi-brand systems (per 24's tokens-at-scale framing) where the manual operation is intractable.

### Day-to-day workflows

- **Token-tier discipline audit.** The AI client walks the token tree and reports tokens consumed at the wrong tier — primitives consumed by components that should reach for semantics (per 32 §2.1's token-audit lane). The discipline-failure findings are structured against the system's stated tier rules (where the system has them) or against the field's general convention (where the system hasn't articulated rules).
- **Dead-token detection.** The AI client cross-references the token catalogue (via Style Dictionary MCP) with build-time consumer scans (via the AI client's file-reading tools) and reports unreferenced tokens. The dead-token list is the deprecation-candidate list; the audit's recommendation pairs the two per 32 §2.1.
- **Alias-chain health audit.** The AI client traverses the alias graph and surfaces broken chains (alias resolves to undefined), circular references (A → B → A), deprecated-token-still-aliased cases (an active alias points to a token marked deprecated). The output is the per-chain health matrix; chains with deep depth (4+ levels) are flagged for review separately because deep chains are fragile.
- **Cross-platform fidelity check.** The AI client compares Style Dictionary outputs across platforms — web CSS, web JS, iOS Swift, Android Kotlin, Compose, Flutter, RN — and flags silent flattening per 32 §2.1's cross-platform-output-integrity check. The composite-typography-token-flattening pattern is the canonical case: composite tokens designed in DTCG resolve correctly to web CSS but flatten on one of the native platforms; cross-platform fidelity degrades silently.
- **DTCG conformance check.** The AI client validates the source against the 2025.10 Format Module spec — token types correctly declared, composite tokens use property-level-aliasing-via-`$ref` rather than `{alias}` notation, mode declarations conform, color-space declarations correct (`srgb`, `oklch`, `display-p3`, etc.). Pre-2024 systems often shipped pre-DTCG token shapes that need migration; the conformance check produces the migration-target list.
- **Multi-brand orthogonality audit.** Per 24's tokens-at-scale framing — the AI client walks a multi-brand token system and verifies that the theming dimensions (mode, density, brand, contrast preference, motion preference) compose orthogonally rather than collapsing into a single "theme" axis. Where dimensions have collapsed, the audit's recommendation is the dimensional split.

### Tooling reality and gaps as of mid-2026

- **Style Dictionary v4 and v5 expose enough surface for custom MCP wrapping.** The wrapping is custom work (4–8 hours for a workstation MCP, more if shipped as a reusable tool with broad coverage). v5's improved resolver makes the wrapping more straightforward than v4's.
- **Tokens Studio's API is stable enough to wrap.** The API's surface has been steady since 2024; wrapping for MCP is custom work but well-trodden territory.
- **No major design-token vendor ships native MCP as of mid-2026.** Specify, Knapsack, Supernova, Backlight all have APIs that an MCP wrapper can consume; none ships MCP natively. The practice's bet: native MCP lands in 2026–2027 — the AI-readiness pressure is real, the engineering work is bounded, the commercial signal is clear.
- **Wrapping work is non-zero but bounded.** A senior DS engineer can stand up the workstation token-MCP layer in a day. The wrapping is the practice's bridge investment; once shipped, it persists across engagements until the vendors ship native MCP and the practice migrates.
- **Composite-token fidelity is the lane's hard case.** Simple primitives (color values, dimension values, font-family strings) wrap cleanly; composite types (typography composites with per-script overrides, motion composites with cross-platform spring parameters) hit the DTCG spec's edge cases. The practitioner's discipline: trust the MCP for primitive-level audits; spot-check composite-level audits manually until the tooling matures.

---

## 6. The web-research MCPs — primary-source verification and the firecrawl pattern

### The web-research MCPs

- **firecrawl MCP.** Wraps Firecrawl's web-scrape and search surface; exposes structured retrieval to AI clients. The dominant practitioner MCP for web-research work as of mid-2026. Handles large documents (the 495K-character CSS Color 4 spec retrieved on the first try in the §1.27a closure); supports markdown / HTML / structured output formats; supports search-then-scrape workflows.
- **fetch MCP.** Simpler — single-URL retrieval. Exposes the underlying HTTP fetch surface. Useful where the practitioner has a known URL and wants the lowest-overhead retrieval.
- **Search-engine MCPs.** Brave Search MCP, Kagi MCP, DuckDuckGo MCP, and others. Different search engines, different result-quality profiles, different rate-limit policies. The practitioner typically picks one and stays with it; cycling between search engines mid-research wastes context-window space.
- **Perplexity MCP.** Wraps Perplexity's research surface. Useful for the research-question-as-input pattern (give me a synthesis on this topic with citations); less useful for the verify-this-specific-claim pattern where targeted retrieval matters more.
- **WebFetch (Claude Code's native tool).** Not an MCP per se but occupies the same role for the practitioner. The 30K-character ceiling is the failure mode; firecrawl is the practitioner's escape hatch when WebFetch truncates.

### Day-to-day workflows

- **Primary-source verification.** The dominant workflow. The practitioner asks the AI client to verify a claim against a spec, an RFC, a W3C document, vendor docs. The AI client runs the fetch (via firecrawl or fetch MCP), returns the body text, the practitioner reads the source rather than relying on training-data recall. The §1.27a worked example is canonical — the practice's WebFetch hit the truncation ceiling on CSS Color 4; firecrawl pulled the full document; the substantive correction landed in 31 §1. The pattern: when WebFetch truncates, default to firecrawl_scrape with `formats: ["markdown"]`; parse the persisted output; grep for the section.
- **Multi-source comparison on a contested claim.** The AI client fetches multiple sources on a contested claim (the contribution-vs-participation distinction; the source-mix-overtime formula; the WebAIM screen-reader survey results) and surfaces the convergence and divergence. Useful for the §1.27-style housekeeping cluster work where multiple sources need to be reconciled.
- **Citation-grade research for client artefacts.** The AI client gathers and structures the primary-source evidence the practitioner cites. Specific URLs, specific quoted body text, specific dates, specific authors. The output is the input for the client artefact's citations footer or footnotes.
- **Spec-evolution tracking.** The AI client checks the current state of a spec the practice depends on — DTCG Format Module, CSS Color 4, ARIA APG, WCAG. The practitioner doesn't have to manually re-fetch every quarter; the AI client runs the check on a stated cadence and reports changes. The practice's standing-watch items (per 09 §1.27 — Style Dictionary `color-mix()` watch, DTCG typography composite-type watch) lean on this.
- **Vendor-positioning verification.** The AI client checks vendor-published positioning claims (Supernova's "AI-ready design systems" framing flagged in §1.28d; firecrawl's own capability surface) before the practice references them in client work.

### The §1.27a worked example, generalised

The §1.27a closure is the canonical reference. WebFetch truncated the CSS Color 4 spec at the 30K-character ceiling; the practice's prior framing of "CSS Color 4 default (chroma-reduction)" was a factual inaccuracy because the truncated capture didn't reach §14.2's algorithm-attribution body text. firecrawl_scrape pulled the full 495K characters on the first try; §14.2's body text was extracted verbatim; the practice's framing was corrected (three sibling algorithms with implementation choice; no single normative CSS default).

The pattern generalises to any spec that exceeds WebFetch's window:

1. WebFetch the URL first; check the response length and the relevant section's content.
2. If the response is truncated or the relevant section is missing, default to firecrawl_scrape with `formats: ["markdown"]`.
3. Parse the persisted output (the harness writes scrape responses to a file in the session tool-results directory).
4. Grep for the section heading; read the relevant body text.
5. Cite verbatim where the claim is load-bearing; date the capture.

The §1.26a–§1.26d + §1.28a–§1.28d residual cluster is the next worked application — eight follow-ups across the team-and-discipline and auditing closures, each requiring primary-source verification before client artefacts. firecrawl is the workstation MCP that makes the residual cluster a half-day pass rather than a multi-day one.

### Tooling reality and gaps

- **firecrawl is the most-used in this practice.** Its scrape and search surfaces are robust at mid-2026. The API key management is non-trivial (the senior practitioner has to maintain credentials; the workstation runbook should cover it). The pricing tier matters for high-volume work; verify against current pricing before treating as cost-free.
- **fetch MCPs are simpler, lower-overhead.** Fine for known-URL retrieval where the practitioner doesn't need search or large-document handling. The practitioner often has both fetch MCP and firecrawl MCP configured; fetch for the simple case, firecrawl for the depth case.
- **Search MCPs vary in quality.** Brave Search MCP is the most-used in practitioner reports; Kagi has a strong following among practitioners who pay for Kagi anyway. DuckDuckGo MCP is free but result quality is lower for technical queries. The practitioner picks one and learns it deeply.
- **Perplexity MCP for the research-question pattern.** Useful for "give me a synthesis on $topic with citations" work; less useful for "verify this specific claim against this specific source." The practitioner has both Perplexity MCP and firecrawl MCP configured for different question shapes.
- **The harness-side persistence behaviour.** When firecrawl returns a large document, the harness writes the response to a file in the session tool-results directory. The practitioner may need to parse the persisted file (a short Python block with `json.load`) rather than receive the full content inline. The pattern is workable but adds a step; verify against current harness behaviour as it evolves.

---

## 7. The default workstation config — what every DS practitioner should have configured

### The recommended stack

The practitioner-workstation MCP stack a senior DS practitioner should have configured by default:

| MCP | Source | Purpose |
|---|---|---|
| **Figma MCP (Dev Mode MCP)** | Figma official | Read access to the design source; design-to-code with structured context; design-token audit (Figma side) |
| **Figma Console MCP** | Southleft (third-party) | Write access for bulk operations; exemplar-page generation; variable-collection authoring |
| **Storybook MCP** | Storybook official | Read access to component-side reality; documentation generation; API consistency audit |
| **axe-core MCP / Pa11y MCP** | Deque / open-source community | Automated a11y scanning; per-component PR review; conformance-evidence collection |
| **Style Dictionary MCP wrapper** | Custom | Token-tree audit; dead-token detection; alias-chain health; cross-platform fidelity check |
| **firecrawl MCP** | Firecrawl | Primary-source retrieval at depth; the §1.27a-style worked-example workflow |
| **One search MCP** (Brave or Kagi) | Brave / Kagi | Broad retrieval; multi-source comparison |
| **Custom DS MCP** (active engagement) | Per-engagement build (per 15 / 30) | System-specific contract surface; the seven-tool surface from 15 |

Plus the AI client itself — Claude Code as the practice's default; Cursor and Windsurf as alternatives the senior practitioner should be fluent in for client-context work where the client has standardised on a different IDE-based AI surface.

### The configuration shape

The practice's discipline: a documented workstation-setup runbook that the new senior practitioner follows on day one. The runbook covers:

- The MCPs in the default stack (per the table above).
- Installation steps per MCP (where to install from, version pinning where the surface is unstable).
- Credential setup (Figma API tokens, firecrawl API keys, vendor API tokens for token-side wrappers).
- Recommended default configurations (which axe-core rule set, which firecrawl scrape format, which Storybook MCP version pinning).
- Known gotchas (the Console MCP Desktop Bridge plugin requirement; Figma MCP's paid-tier dependency; firecrawl API-key management).
- Update cadence (the runbook is reviewed quarterly; MCP version updates are tracked).

The runbook is itself practice IP. It compounds the senior practitioner's time-to-effective on every new engagement, on every new client codebase, on every new agency machine. New senior hires onboard against the runbook rather than building their stack ad-hoc; cross-engagement collaboration is friction-free because every senior has the same configured stack.

### The cost of not having the default config

The senior practitioner who joins an engagement without the workstation stack is doing the same work manually:

- Reading Figma files visually (an hour per component vs. fifteen minutes with Figma MCP).
- Walking Storybook stories one at a time (per-PR review at twenty minutes vs. five with Storybook MCP + axe-core MCP).
- Running axe-core scans through browser DevTools (per-component manual scan vs. automated scan via AI client).
- Fetching primary sources through the browser (the §1.27a-style workflow at half a day per spec vs. fifteen minutes with firecrawl).
- Walking token trees manually (multi-brand audit at multi-day pace vs. half-day pace with Style Dictionary MCP wrapping).

The aggregate cost is roughly 30–50% of the work's wall-clock time, with the additional cost that the practitioner's fatigue rises faster (manual operations are more error-prone and more cognitively expensive than supervising the AI client's MCP calls). The agency that under-invests in workstation standardisation pays in senior-practitioner velocity and retention.

### The cost of having too much MCP config

The opposite failure mode is real and worth naming. The practitioner who has configured fifteen MCPs, half of which they never call, half of which conflict on tool naming or context-window budget, has a workstation that's actively worse than the minimal default.

Symptoms:

- The AI client's context fills with tool definitions; the actual prompt has less room.
- The agent picks the wrong MCP for a task because two MCPs have overlapping tool names.
- The practitioner forgets which MCP does what; the workflow gains a "which tool do I reach for" decision step that wasn't there before.
- Maintenance burden grows; updates across fifteen MCPs become a quarterly afternoon rather than a quick check.

The discipline: keep the default config minimal. Add MCPs only when the day-to-day workflow demands them. Remove MCPs that haven't been called in a quarter. The runbook reviews are the moment to prune; the practitioner audits their own MCP set against actual usage and trims.

### The cross-practice standardisation argument

Every senior practitioner with the same workstation config produces work at predictable speed and quality. The argument's components:

- **Onboarding.** New senior hires onboard against a documented config rather than building their stack from scratch. Time-to-first-engagement-contribution drops from weeks to days.
- **Cross-engagement collaboration.** Practitioners can read each other's AI-client transcripts without disorientation. The shared tool surface means the same prompt produces the same output structure across practitioners.
- **Practice-level training.** The runbook is the basis for practice-internal training. Senior practitioners run sessions on advanced workflows (the firecrawl-scrape-when-WebFetch-truncates pattern; the Console-MCP-with-branch-only-writes discipline; the Style-Dictionary-MCP-for-multi-brand-audits workflow) against a shared baseline.
- **Cross-agency mobility.** A senior practitioner moving to a different agency takes the runbook with them as career IP. The discipline transfers; the senior practitioner's effective tier holds.

The agency's compounding asset is the standardised workstation. The practice's IP is the runbook.

### How the workstation stack relates to the custom DS MCP server

The relationship, restated explicitly:

- **Workstation stack: general-purpose, career-amortised, agency-internal.** The same MCPs serve every engagement. The senior practitioner configures once, updates quarterly, never bills a client for them.
- **Custom DS MCP server: engagement-specific, engagement-amortised, billable.** Built once per client (or per portfolio at multi-brand scale per 24). Exposes the system's structured contract via the seven-tool surface from 15. Transfers to the client at handoff (per 32 §1's failure-mode catalogue — the client owns the system's instance from day one; the system's MCP server is part of the instance).

The senior practitioner's day-to-day workflow uses both layers fluidly. The Figma MCP reads the current engagement's Figma file generically; the custom DS MCP exposes the same engagement's components-as-data with the client's contract; the AI client composes calls across both. None of the workstation MCPs alone produces the leverage; the composition does.

The practice that articulates both layers explicitly — workstation stack as agency-internal IP; custom DS MCP server as billable per-engagement deliverable — gets the commercial relationship right and the IP-handoff discipline right. The practice that conflates them under-invests in standardisation, over-invests in per-engagement build-out, or transfers IP that should have been retained.

---

## References

The MCP-as-practitioner-tooling literature is sparse — this is first-generation tooling; most documentation is vendor docs and practitioner blogs. The references below organise primary sources by section.

### MCP specification and clients

- **Model Context Protocol specification** — `modelcontextprotocol.io`. The protocol's canonical reference. The spec evolves; verify against the current revision.
- **Claude Code documentation** — `docs.claude.com/en/docs/claude-code`. MCP integration, tool surface, configuration.
- **Cursor documentation** — `docs.cursor.com`. MCP integration via the Cursor MCP surface.
- **Windsurf documentation** — `codeium.com/windsurf` (or successor URL post-Windsurf-rebrand events). MCP integration.

### Figma-side MCPs

- **Figma Dev Mode MCP documentation** — `help.figma.com` (search for Dev Mode MCP). Plan-tier requirements, capability surface, current limitations.
- **Figma Console MCP** (Southleft) — `github.com/southleft/figma-console-mcp` or the maintainer's current URL. Desktop Bridge plugin documentation, write-access surface.
- **Figma's Variables and Code Connect documentation** — broader context for what the MCPs expose. `help.figma.com`.

### Storybook MCP

- **Storybook MCP documentation** — `storybook.js.org/docs` (search for MCP). Version-specific surface; verify the current Storybook version's MCP capability.
- **Storybook addons relevant to MCP work** — a11y addon (`storybook.js.org/addons/@storybook/addon-a11y`), interactions addon, viewport addon, links addon, docs addon.
- **Component Story Format (CSF) reference** — `storybook.js.org/docs/api/csf`. The structured story shape MCP exposes.

### Accessibility-scanner MCPs

- **axe-core documentation** — `github.com/dequelabs/axe-core`. Rule reference, severity model, CI integration patterns.
- **Pa11y documentation** — `pa11y.org`. CI-friendly axe-core wrapping.
- **Lighthouse documentation** — `developer.chrome.com/docs/lighthouse`. Broader audit surface including a11y.
- **Deque's coverage assessment** — Deque's published self-assessment of axe-core's WCAG coverage (the "30–40%" figure). Verify the current self-assessment and the methodology before quoting.
- **WebAIM resources for the boundary** — the cross-AT-testing matrix that scanner MCPs do not substitute for. `webaim.org`.

### Token-side MCPs

- **Style Dictionary documentation** — `styledictionary.com`. v4 / v5 resolver and dependency-graph surfaces.
- **Tokens Studio documentation** — `tokens.studio`. API surface, graph engine, DTCG conformance.
- **Specify documentation** — `specifyapp.com`. API surface for MCP wrapping.
- **Knapsack documentation** — `knapsack.cloud`. Programmatic surfaces.
- **Supernova documentation** — `supernova.io`. Programmatic surfaces; "AI-ready design systems" positioning (verify current framing).
- **DTCG Format Module** — `tr.designtokens.org/format`. The 2025.10 module's spec; verify current version.

### Web-research MCPs

- **Firecrawl documentation** — `docs.firecrawl.dev`. Scrape, search, structured-output surfaces.
- **Brave Search documentation** — `api.search.brave.com/docs`. Search-engine MCP wrapping.
- **Kagi documentation** — `kagi.com`. Practitioner-paid search surface.
- **Perplexity documentation** — `docs.perplexity.ai`. Research-question MCP surface.

### Practitioner writing on MCPs in DS work

- **Brad Frost's blog** — `bradfrost.com`. Occasional MCP-relevant posts; verify current writing.
- **Nathan Curtis / EightShapes catalogue** — `medium.com/@nathanacurtis`. MCP-relevant entries where they exist.
- **Design Systems Podcast** — `thedesignsystem.guide/podcast` (or successor URL). Search the catalogue for MCP-focused episodes.
- **Clarity Conference back catalogue** — `clarityconf.com`. MCP and AI-tooling talks scattered through 2024–2026.
- **Config (Figma) talks** — Figma's annual conference. MCP-relevant talks since 2024.
- **Smashing Conference and Smashing Magazine** — `smashingmagazine.com`. Practitioner-level MCP coverage.
- **Into Design Systems** — `intodesignsystems.com`. Newsletter and conference; MCP-relevant content surfaces regularly.

### Verification notes

- All "as of mid-2026" claims about MCP tool surfaces, plan-tier dependencies, and version-specific capabilities should be re-checked against current docs. This space rotates faster than any other DS topic in this vault; specific feature claims may be stale within a quarter of writing.
- The "30–40% WCAG coverage" figure attributed to axe-core's self-assessment is widely cited in the field but not trivially verified against a single source. Verify against Deque's current published methodology before quoting in client work.
- Native MCP support from major design-token vendors (Specify, Knapsack, Supernova, Backlight) is the practice's bet for 2026–2027; track vendor announcements quarterly.
- The Console MCP's third-party-maintainer status (Southleft) means the workstation stack's risk surface includes the maintainer's bus factor. The practice's discipline: treat Console MCP as a productivity tool with a graceful-degradation plan; don't depend on it indefinitely; track Figma's roadmap for native write-MCP capability as the durable answer.
- Pricing claims for any vendor (firecrawl, Kagi, Specify, etc.) reflect mid-2026 observation; verify against current pricing pages before treating as load-bearing.

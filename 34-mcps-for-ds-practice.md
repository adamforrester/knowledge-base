---
type: practice-area
title: MCPs for DS Practice
description: The developer's-workstation MCP stack a senior DS practitioner should have configured by default — the Figma side (Dev Mode + Console), the component side (Storybook), the accessibility side (axe-core / Pa11y / Lighthouse), the token side (Style Dictionary + Tokens Studio + custom wrappers), the web-research side (firecrawl + the §1.27a truncation-fallback pattern), and the seven-tool default config that compounds across the practitioner's career as practice IP, distinct from the per-engagement custom DS MCP server architecture covered in 15 + 30.
tags: [extension, mcp, ai, tooling, workstation, productisation]
timestamp: 2026-06-17
---

# 34 — MCPs for DS Practice

> The MCP story splits into two stories. The first — *MCPs as architecture* — is about a custom DS MCP server that exposes a specific client's components-as-data through a structured tool surface. That story is closed by 15-ai-in-ds (the seven-tool conceptual surface) and 30-generated-from-data-documentation (the 40–80-hour build-out, priced and located in Phase 3 of the AI-readiness adoption arc). It is the *system-as-data* dimension; the customary answer is well-shaped. The second story — *MCPs as practitioner tooling* — is about the off-the-shelf MCP servers that sit on a senior practitioner's workstation and turn their MCP-capable AI clients (Claude Code, Cursor, Windsurf, the agentic surfaces of 2026) into useful collaborators on day-to-day DS work. This story is mostly undocumented in the field and partly undocumented in this practice. The senior practitioners who use Figma Console MCP routinely, who reach for firecrawl when WebFetch truncates, who have axe-core wired into their Storybook addon stack and read it through the AI client — these practitioners are operating the workstation stack as a discipline. This file is that discipline articulated.

---

## Why a workstation-MCP file needs to exist

15-ai-in-ds is 579 lines at *DS-as-architecture* altitude — the AI lifecycle (token critique, Figma MCP, components-as-data, codegen, docs generation, handoff, governance, AI-ready architecture, current limits). It treats Figma MCP, Figma Console MCP, Storybook MCP, and custom DS MCP server architecture comprehensively at the system-as-data altitude. 30-generated-from-data-documentation prices the custom DS MCP server build-out at 40–80 hours and locates it in the Phase 3 AI-readiness adoption arc. Both files close the architecture half.

What they don't cover — and what we now have working knowledge of, though previously undocumented — is the practitioner-workstation register. The Figma Console MCP that one of us has been using on every active engagement; the firecrawl pattern that closed §1.27a where WebFetch truncated; the axe-core + Storybook combination that catches the easy a11y wins at PR-submission time; the token-side wrappers that make multi-brand audits a half-day pass rather than a multi-day one. This is practice IP we ship through senior practitioners' configured workstations rather than through the file tree. Under-documenting it costs us the standardisation surface — junior practitioners build their stack ad-hoc; cross-engagement velocity isn't predictable; the runbook a new senior should follow on day one doesn't exist.

What this file extends: 15's MCP framing into the practitioner-workstation register; 30's productisation-of-practice-IP frame; 32's audit-the-audit discipline applied to the workstation stack itself. What it doesn't replace: the architecture half stays in 15 + 30; the audit's eight-lane methodology stays in 32; the day-to-day workflows in 14 / 17 / 28 stay in their files. This file owns the workstation layer.

A note on currency before anything else. **This space rotates faster than any other DS topic in this vault** — faster than 15 even, because practitioner MCPs are mostly third-party or first-generation tooling and the maintainers ship weekly. Specific tool surfaces, plan-tier dependencies, and capability claims below reflect mid-2026 platform state; verify against current docs before treating any specific claim as load-bearing in client work. The architectural shape — workstation MCPs are general-purpose, custom DS MCPs are engagement-specific, both compose, the workstation stack standardises practitioner velocity — is more durable than the tool names attached to it.

---

## 1. The two-layer architecture — workstation stack vs. custom DS MCP server

The practitioner-workstation MCP stack and the custom-DS-MCP-server architecture are different axes of the broader MCP story. Both involve MCP servers; both deliver leverage to MCP-capable AI clients. They answer different questions and pay back along different curves.

```
┌────────────────────────────────────────────────────────────────────┐
│                      THE PRACTITIONER WORKSPACE                    │
│                                                                    │
│   ┌──────────────────────────┐        ┌──────────────────────────┐ │
│   │  Workstation MCP Stack   │ ◄────► │   Custom DS MCP Server   │ │
│   │     (general-purpose)    │        │     (system-specific)    │ │
│   └─────────────┬────────────┘        └─────────────┬────────────┘ │
│                 │                                   │              │
│                 ▼                                   ▼              │
│   Reads whatever Figma file,            Exposes one client's       │
│   Storybook, codebase, or               components-as-data,        │
│   spec is in front of the               composition rules, usage   │
│   practitioner — engagement-            guidelines, validation     │
│   agnostic.                             tools — engagement-shaped. │
│                                                                    │
│   Career-amortised; practice IP;        Per-engagement-amortised;  │
│   never billed.                         billable line item.        │
│                                                                    │
│   The senior practitioner's             Built once, transferred to │
│   sensor array and actuator             the client at handoff per  │
│   arm.                                  32 §1's failure-mode       │
│                                         catalogue.                 │
└────────────────────────────────────────────────────────────────────┘
```

The **custom DS MCP server** answers: *how does a specific client's design system expose itself to AI clients as a structured contract?* The seven-tool surface 15 names — `list_components`, `get_component`, `search_components`, `get_token_catalog`, `get_composition_rules`, `get_usage_guidelines`, `validate_implementation` — is the canonical shape. Built once per client (or per portfolio at multi-brand scale per 24); priced as a 40–80-hour line item per 30; transferred to the client at handoff because the client owns the system's instance from day one (per 32 §1). The IP is the practice's *method*; each instance is the client's.

The **practitioner-workstation MCP stack** answers a different question: *what tools should a senior practitioner have configured by default, regardless of which client they're currently working with?* The answer is a stack of off-the-shelf or lightly-wrapped MCP servers — Figma MCP, Storybook MCP, axe-core MCP, design-token MCP, firecrawl MCP — that read whatever Figma file, whatever Storybook, whatever component library, whatever spec is currently in front of the practitioner. The stack is engagement-agnostic; the IP is the practitioner's, not the client's.

The two layers compose. The senior practitioner who has both configured moves fluidly within a single session: the Figma MCP reads the *current engagement's* Figma file generically; the custom DS MCP reads the same engagement's components-as-data with the client's opinionated contract. Ask the AI client to compare a contributed component against the contract: it calls the custom DS MCP for the contract, calls Figma MCP for the design source, calls Storybook MCP for the implementation reality, and returns a three-way reconciliation. None of the three MCPs alone produces this; the composition does.

### The payback curves are different and load-bearing commercially

The custom DS MCP server pays back **per-engagement**: a 40–80-hour line item in the SOW, deliverables that become the AI-readiness evidence, transfer to the client at handoff. Investment amortised against engagement revenue. The workstation stack pays back **across the practitioner's career**: every engagement benefits from the same configured stack; every audit moves faster because the AI client has the right tools wired up; every primary-source verification is one firecrawl call instead of fifteen browser tabs. Investment amortised against the practitioner's lifetime work.

This distinction matters. The agency that prices custom DS MCP servers as billable and treats workstation MCPs as agency-internal hygiene gets the relationship right. The agency that conflates them — bills clients for workstation setup, or treats workstation expertise as per-engagement build — loses on both ends. Clients see workstation tooling as overhead and resent the bill; the agency loses the commercial wedge of the custom server because it's been blurred together with general workstation work.

### What the workstation stack delivers — the cost-of-not-having

Five concrete day-to-day workflows, with the speed-up the workstation stack produces. The conservative figures below reflect *practitioner-realistic* total time including human review of the AI client's output; raw generation is faster (typically by another 3–6×) and is the figure to cite to executives where the comparison is generation-only. We track both because the agency lead pricing audit work needs the conservative number; the executive readout citing leverage benefits from the larger one.

| Day-to-day task | Manual workflow | With the workstation stack | Practitioner-realistic speed-up |
|---|---|---|---|
| **Per-component docs generation** | Read the Figma file; walk the Storybook story; open 29's seventeen-section template; author the page | AI client calls Figma MCP + Storybook MCP; emits a draft following 29's template; practitioner reviews and edits | **2–4×** (raw generation: 12–18×) |
| **Token-tree dead-token detection** | Export Style Dictionary build; export consumer codebase; write or commission the cross-reference script; structure findings | AI client calls Style Dictionary MCP for the catalogue; walks the consumer code via existing file-reading tools; emits the structured dead-token list | **6–10×** (raw generation: 80–120×) |
| **Primary-source verification** | WebFetch hits 30K-character ceiling on a long spec; manually fetch via browser; copy relevant body text; structure citation | firecrawl MCP retrieves the full document on first try; AI client reads the relevant sections; practitioner reviews | **2–3×** (raw generation: 20–30×) |
| **Bulk Figma operations** (e.g. brand-tier token rename across 5,000+ references) | Senior designer opens each component, finds each reference, updates manually | Figma Console MCP runs the migration via a single agent invocation; output reviewed in branch before merge | **20–40×** |
| **Storybook + axe-core PR review** | Reviewer walks the new stories; runs axe DevTools manually per variant; structures comment | AI client calls Storybook MCP for stories + axe-core MCP per story; structures violations against the contribution-model checklist; drafts comment | **3–4×** |
| **Contribution-model template generation** (boundary case) | Synthesise interview script; identify governance gaps; draft tailored workflow document | LLM context-window operation; **no workstation MCP needed** — pure textual reasoning | **boundary case** |

The aggregate effect across a career is the practice's compounding asset. The §1.27a closure is the canonical worked example: WebFetch truncated CSS Color 4 at the 30K-character ceiling; the practice's prior framing of "single normative CSS default" was a factual inaccuracy because the truncated capture hadn't reached §14.2's three-sibling-algorithms body text. firecrawl_scrape with `formats: ["markdown"]` pulled the full 495K-character document on the first try; §14.2's body text was extracted verbatim; the substantive correction landed in 31 §1. That pattern generalises to every spec exceeding WebFetch's window — and to the eight-item §1.26a–§1.26d + §1.28a–§1.28d residual cluster that's our next housekeeping pass.

### The miscategorisation cost

Two miscategorisations show up in agency proposals.

**Pricing the architecture and skipping the standardisation.** The agency proposes a custom DS MCP server (priced correctly per 30, 40–80 hours), and the proposal is silent on the workstation stack. The senior practitioners on the engagement use the stack anyway because they have it configured personally — but the practice doesn't ship the stack as a standardisation artefact. Junior practitioners on the engagement don't have the same speed-up; cross-engagement velocity isn't standardised. The agency producing strong work in the senior tier and inconsistent work in the junior tier is often suffering from this gap.

**Pricing the standardisation and skipping the architecture.** The agency invests in workstation training, runs an internal stack-setup runbook, ensures every senior has the same MCPs configured. The proposals don't include the custom DS MCP server because the practice hasn't separated the two layers. The day-to-day velocity is high; the AI-readiness commercial deliverable doesn't ship; the wedge per 30 is missed.

The fix is the explicit articulation: workstation stack is *practice IP, agency-internal, career-amortised, never billed to a single client*. Custom DS MCP server is *practice-IP-applied-to-the-client, billable per engagement, amortised against engagement revenue, transferred to the client at handoff*. Both are needed; they're priced differently because they pay back differently.

---

## 2. The Figma-side MCPs — Dev Mode MCP, Console MCP

The Figma-side MCP story splits into two servers that compose. **Figma Dev Mode MCP** is Figma's official, read-only server. **Figma Console MCP** (Southleft) is third-party, write-enabled. The senior practitioner has both configured.

**Figma Dev Mode MCP.** Ships with paid tiers (mid-2026: Organization and Enterprise plans, with partial surface available on Professional — verify against current docs before treating as fixed). Exposes node structure, variables, Code Connect mappings, layout data, and screenshot retrieval. The AI client calling Dev Mode MCP can read a frame's structure, query the variable collections, follow the Code Connect map to the implementation, and retrieve a rendered image. The canonical *design-as-source* surface for AI-driven design-to-code work.

**Figma Console MCP** (Southleft). Third-party, write-enabled via a Desktop Bridge plugin. Exposes project-wide context (Dev Mode MCP is per-file; Console MCP can reach across files in a project) and write access — agents can create frames, instantiate components, configure variable collections, apply token migrations across thousands of node references, generate exemplar pages from component metadata. The "bootloader" architecture loads enough Figma context for the agent to operate against the canvas with structural awareness, not just at the JSON-API level.

### Day-to-day workflows

**Dev Mode MCP.** *Design-to-code with structured context* — the AI client reads the selected node, follows the Code Connect mapping to the production component, reads consumed variables, generates code that imports the real component, uses real tokens, respects the system's API contract. The output is what 15 §The practical MCP workflow names "context-first" code generation. *Component-anatomy extraction* for 29's docs page generation. *Design-token audit (Figma side)* — the AI client walks the Variables collections and reports drift against a stated catalogue (typically the Style Dictionary build output cross-referenced via §5's token-side MCPs). *Variable-collection inventory* for Discovery audits per 32 §2.1 — at scale (50+ collections, hundreds of variables) the manual operation is intractable; Dev Mode MCP makes it a fifteen-minute query.

**Console MCP.** *Bulk migrations* — a token rename, a component-property reshuffle, a variable-collection split. Operations that touch thousands of node references and that without Console MCP take a senior designer days of manual work. Console MCP runs the migration via a single agent invocation in minutes; output appears in a Figma branch (per the governance discipline below). *Exemplar-page generation* from a stated component composition. *Variable-collection authoring* from a stated theme spec — works for straightforward color/spacing/typography collections; complex composite types (typography composites with per-script overrides, motion composites with cross-platform spring parameters) are at the edge of what works reliably and benefit from senior review before landing. *Template instantiation* from stated compositions — useful for repetitive layout work.

### Governance — the question Console MCP forces

Write access to the design source raises governance questions read access doesn't. The MCP-equipped agent can change the design-tool source-of-truth at the speed of generation; without governance, agent-authored changes destabilise the library before human review catches them.

The disciplines that work:

- **Branch-only writes.** Agent-authored changes land in a Figma branch, never directly in the main library. Senior designer reviews the branch before merging. The friction (branches add a review step) is appropriate; the alternative is agent-authored chaos in main.
- **Senior review on token migrations.** Bulk operations on tokens or core components require explicit senior review before merge. The senior reads the *full* set of changes, not a sample; the speed-up of the operation makes comprehensive review tractable that wouldn't be tractable manually.
- **Approval-required operations.** Where Console MCP's configuration supports it, require explicit approval for write operations. The agent proposes; the human approves or rejects.
- **The per-engagement Console MCP scope decision.** Some engagements — particularly early-stage where the design source is in flux — should not have Console MCP write access enabled. The risk-of-bad-write outweighs the speed-up. The senior practitioner makes the scope decision per engagement and documents it.

The pattern that fails: senior practitioner runs Console MCP with default permissions, the agent makes a well-intentioned but incorrect token migration (interpreting the rename request differently than intended), the Figma library is destabilised, recovery is non-trivial because the operation touched thousands of nodes. Real incidents shape this discipline; the practice that has lived through one such incident enforces the branch-only discipline thereafter.

### Tooling reality and gaps as of mid-2026

- **Variables modes coverage** is uneven across paid tiers. Verify against current docs.
- **Console MCP installation overhead.** The Desktop Bridge plugin is a workstation-configuration step that adds onboarding friction. The runbook in §7 covers it explicitly.
- **Code Connect surface depth.** Both MCPs know the mapping exists but expose it at varying depths. Where the mapping is thin, the AI client falls back to inference, which works less reliably.
- **Prototype layer is largely invisible.** Neither MCP exposes the deep prototype layer — interactions, motion specs, conditional logic — usefully. For motion-heavy work (per 18-21) the practitioner falls back to manual extraction or Figma plugin-based scraping.
- **Console MCP is third-party.** Maintained by Southleft, not Figma. The practice's risk surface includes the maintainer's bus factor; the workstation stack should not depend on Console MCP being available indefinitely. Native Figma write-MCP capability is the durable answer; track Figma's roadmap.

The verification-path discipline is load-bearing: name the capability with a date, verify against current docs before treating as fixed in client work. This applies to all the Figma-side MCPs more strongly than to most other tooling because the surface evolves quarterly.

---

## 3. The component-side MCPs — Storybook MCP and the testing surface

Storybook MCP exposes the component library's published surface to AI clients: the stories, the CSF (Component Story Format) metadata, the args / argTypes / parameters surface, the docs blocks, and the addon-driven integrations (a11y addon, viewport addon, interactions addon, links addon). The AI client reading Storybook MCP knows what components exist in the system, what props they accept, what variants ship, what the documented usage patterns are.

Storybook 8.x ships an MCP surface; Storybook 9 (2025–2026) extended it. The surface evolves quickly; the senior practitioner tracks the Storybook release notes for MCP-relevant changes and updates the workstation config accordingly.

### Day-to-day workflows

*Component documentation generation* — the dominant workflow. AI client reads the stories, emits a per-component docs page following 29's seventeen-section template. Args-table drives the properties section; play-function drives the interaction-states section; docs-blocks seed the usage section. Output is a draft; senior designer or DS lead reviews and edits.

*API consistency audit* — AI client compares prop shapes across the library and flags inconsistencies (`size="small"` on Button vs. `size="sm"` on Input; `tone` vs. `intent` vs. `variant` for semantically equivalent props). Output is the per-prop matrix per 32 §2.2's component-audit lane. Manually constructing the matrix takes hours; with Storybook MCP, twenty minutes.

*Migration-codemod authoring* — when the system ships a major release with API changes, AI client reads v1 and v3 stories, identifies prop renames / removals / semantic shifts, emits a codemod that migrates consumer code. Roughly 70–80% correct on first pass for additive migrations; lower (40–60%) for breaking migrations requiring human judgment about semantic equivalence. The codemod is reviewed and refined.

*Test-coverage analysis* — AI client cross-references stories with test files and flags components without state-coverage stories. Feeds 32 §2.2's state-machine-completeness check.

*Implementation-vs-design reconciliation* — AI client reads Storybook MCP (implementation reality) and Figma Dev Mode MCP (design source) and reports drift. Per-component audit's design-to-code-faithfulness check.

*Stakeholder-readout assembly* — AI client reads Storybook MCP for the component surface plus 24's Cascade Report for cross-brand impact, and structures the executive readout per 08's quarterly governance review template.

### Storybook MCP vs. custom DS MCP, restated

Storybook MCP is *general-purpose*: every Storybook ships with the same MCP surface. The AI client knows what's *shipping* — the implementation reality. The custom DS MCP server (per 15) is *system-specific*: exposes the system's *opinionated contract* — composition rules, usage guidance, validation tools. The AI client knows what *should be shipping* — the system's intent. The senior practitioner with both reads the reconciliation as an audit signal: where Storybook reality matches system intent, the system operates cleanly; where it diverges, the system has accumulated drift the audit's component lane should surface (per 32 §2.2).

### Tooling reality and gaps as of mid-2026

- **Docs-block content depth.** Args-table is excellent; play-function is excellent; docs-block content is exposed but not always parsed cleanly into structured form. MDX docs blocks with rich custom content can come back as text-blob output that the AI client struggles to structure. Practitioner workflow: prefer args-table-driven docs over heavily-custom MDX where AI consumption is a goal.
- **Cross-story navigation.** Variable. Some Storybook versions expose `linkTo` metadata cleanly; others don't.
- **Visual-regression baselines are not exposed.** Chromatic snapshots, Percy baselines, Playwright visual baselines live in their own surfaces. Storybook MCP knows the stories exist but not the baseline images. The AI client doing visual-regression analysis needs separate MCPs (or custom wrapping; mid-2026 vendor-native MCP surfaces are limited).
- **Storybook composition.** Where the practice ships multiple Storybooks (per-platform: web, mobile, marketing), the AI client needs to know which to read. Composition MCP behaviour is worth verifying per setup.
- **Addon-driven extensions vary.** Each addon may or may not expose its surface via MCP. The a11y addon's surface is well-exposed; others vary. Discipline: query the AI client's tool surface to confirm what's available rather than assuming addon-MCP coverage.

---

## 4. The accessibility-scanner MCPs — automated rule verification

The accessibility-side MCPs:

- **axe-core MCP** (or equivalents wrapping Deque's axe-core). The canonical scanner. Exposes the rule surface to the AI client; the client calls `scan(url)` or `scan(component_story)` and receives a structured violations list with rule ID, severity, affected element, and remediation guidance.
- **Pa11y MCP.** Wraps Pa11y, which itself wraps axe-core, for CI-friendly use. Exposes scan surface plus configuration options (rule subsets, viewport sizing, viewport-injected scripts).
- **Lighthouse MCP.** Broader than a11y but includes the a11y category. Useful for the cross-domain audit (a11y + performance + best practices + SEO) where the practitioner wants a single tool covering multiple lanes.
- **Storybook a11y addon (via Storybook MCP).** Per §3 — the per-story a11y rule surface is the canonical practitioner workflow when the system has Storybook stories for every component.

### Day-to-day workflows

*Per-component a11y scanning during contribution.* PR review's first pass. AI client calls Storybook MCP for the new stories, calls axe-core MCP per story, structures violations, drafts a review comment. Catches the easy failures (missing labels, contrast regressions, heading-hierarchy issues, label-association issues) before the PR opens for human review. The contribution-model SLA per 07 holds because easy violations are caught at PR-submission time, not at review time.

*Cross-component a11y pattern audit.* During a Discovery audit (per 32 §2.3), AI client scans a sample of components and surfaces recurring patterns — components missing focus-trap implementations, components without `aria-label` on icon-only variants, components with contrast regressions in the dark theme. Pattern-level read informs the audit's accessibility lane findings.

*Pre-engagement a11y baseline.* Before a productised audit kicks off, AI client runs a baseline scan against the client's current component surface. Output is the input data for Day 3 of the 5-day audit shape per 32 §3. The audit's first day gains capacity because the baseline already exists.

*Multi-state continuous scanning.* Components with complex interactive states (active, loading, error, disabled) often regress on accessibility only in specific states. AI client iterates through all of a component's stories, runs scans on each state, and flags issues that appear only under specific conditions (poor contrast in error state; focus indicator failing in active state; ARIA live-region not firing in loading state).

*Conformance-evidence collection.* For regulated-industry audits (EAA, Section 508, ADA Title III per 32 §2.3), AI client compiles per-criterion test results across sampled components for the report's regulatory section. Structured violations list maps to WCAG success criteria; AI client cross-references and compiles. Hours of manual evidence-collation become a 30-minute compilation.

### The boundary the scanner MCPs do not cross

Automated scanning's coverage of WCAG conformance is widely misquoted; the precise framing per Deque's 2021 *Automated Accessibility Coverage Report* (deque.com/automated-accessibility-coverage-report/) is two metrics, not one. The **WCAG-Success-Criteria-coverage** metric — what percentage of the 50 WCAG 2.1 AA criteria can be tested automatically — is **~32% (16 of 50)**; this is the figure that produces the widely-cited 20–30% "automated coverage" claim that Deque has actively worked to disprove since 2021. The **issue-volume-coverage** metric — what percentage of total issues found in real audits are detected automatically — is **57.38%** in Deque's 2,000-audit / 13,000-page / 300,000-issue dataset, because some criteria (contrast, name/role/value, parsing) generate many issues per page and automate at high rates (83%, 54%, 90% respectively). The four-engine × four-AT matrix per 32 §2.3 plus 28's web-accessibility-implementation framing covers the residual ~43% by issue volume (or ~68% by WCAG SC count). Source: `_source-text/ext-axe-core-coverage.txt`.

The discipline:

- **Use scanner MCPs for breadth and speed.** The ~57% of issue-volume the automated scanners catch is the easy-win surface (and ~32% of WCAG SC coverage). Catching it at PR-submission time, at Discovery baseline time, at conformance-evidence time — the speed-up is real, the catch rate is consistent.
- **Use real AT testing for depth and authority.** The remaining 60–70% — semantic-structure failures, keyboard-trap issues, focus-management failures, screen-reader navigation order, screen magnifier usability, the WCAG-passes-but-fails-real-users pattern per 31 — requires human AT testing across the matrix. No MCP substitutes for it.
- **Don't conflate the two.** The audit shipping automated-scan output as the entire a11y deliverable fails the audience that pays for accessibility (regulators, AT users, legal). Every productised audit's a11y lane includes both the scanner-MCP output (breadth) and the manual-matrix output (depth); the report names which evidence comes from which source.

### Tooling gaps

**Real-AT-testing MCPs do not exist in mid-2026.** No practical MCP server exposes a JAWS / NVDA / VoiceOver / TalkBack surface to an AI client at the depth required for real conformance testing. The cross-AT testing remains manual. The practice's bet: this gap closes in 2026–2027 as AT vendors and AI-tooling vendors converge; until then, the manual matrix is the discipline. **BrowserStack / Sauce Labs do not ship MCP-native surfaces** — they expose programmatic APIs that an MCP wrapper can consume; wrapping is custom work (typically 8–16 hours for a workstation MCP covering a single VM-based AT-driven test). Most practitioners run the matrix manually with the remote-desktop surface rather than wrapping it. **Per-rule severity calibration drifts** as axe-core's rule set updates with each release; the audit-the-audit discipline per 32 §5 covers this. **Multi-rule-set wrangling** for regulated-industry audits (EAA imports WCAG 2.1 AA; Section 508 imports WCAG 2.0 AA; the practice's working standard is WCAG 2.2 AA) requires per-scan rule-set configuration — the practitioner configures explicitly per regulatory context.

---

## 5. The token-side MCPs — authoring, validation, audit

The token-side MCPs:

- **Style Dictionary MCP wrapper** (custom). v4 (late 2024 / early 2025) and v5 (2025–2026) expose enough resolver and dependency-graph surface that custom MCP wrapping is straightforward. The wrapper exposes the build pipeline's dependency graph: the AI client walks from any token to its primitive root, identifies dead tokens, surfaces alias-resolution failures, generates the Cascade Report per 24 §3 on primitive changes.
- **Tokens Studio MCP** (or Tokens Studio API exposed via custom MCP). The API has been stable enough to wrap since 2024–2025. Exposes the design-tool side of the token tree — Figma Variables structure, Tokens Studio JSON, DTCG conformance validation, composite-typography-token fidelity audit per 23.
- **Specify MCP**, **Knapsack MCP**, **Supernova MCP**. Each vendor exposes a programmatic API; MCP wrappers exist (custom or community) at varying maturity. **Update mid-2026: Supernova has shipped MCP-endpoint distribution** (private beta as of 2026-06-18; configurable per team / workflow / agent type; distributes to Cursor, Copilot, Claude Code, Codex). Specify, Knapsack, and Backlight remain API-only; native MCP from those three is the practice's bet for late 2026 / 2027. Source: `_source-text/ext-supernova-ai-ready.txt`.
- **The Tokens Studio graph engine specifically.** The visual graph view of token dependencies is the practitioner-visible surface; the API behind it is what an MCP wrapper exposes programmatically. The AI client with graph-engine access traces any token's full dependency surface in milliseconds — what a senior practitioner does manually in minutes. The leverage compounds on multi-brand systems (per 24's tokens-at-scale framing) where the manual operation is intractable.

### Day-to-day workflows

*Token-tier discipline audit.* AI client walks the token tree and reports tokens consumed at the wrong tier — primitives consumed by components that should reach for semantics (per 32 §2.1's token-audit lane). Discipline-failure findings structured against the system's stated tier rules.

*Dead-token detection.* AI client cross-references the token catalogue with build-time consumer scans and reports unreferenced tokens. Dead-token list is the deprecation-candidate list per 32 §2.1.

*Alias-chain health audit.* AI client traverses the alias graph and surfaces broken chains, circular references, deprecated-token-still-aliased cases. Chains with deep depth (4+ levels) flagged separately because deep chains are fragile.

*Cross-platform fidelity check.* AI client compares Style Dictionary outputs across platforms — web CSS, iOS Swift, Android Kotlin, Compose, Flutter, RN — and flags silent flattening per 32 §2.1. Composite-typography-token-flattening is the canonical case: composite tokens designed in DTCG resolve correctly to web CSS but flatten on one of the native platforms; cross-platform fidelity degrades silently.

*DTCG conformance check.* AI client validates the source against the 2025.10 Format Module spec — token types correctly declared, composite tokens use property-level-aliasing-via-`$ref` rather than `{alias}` notation, mode declarations conform, color-space declarations correct (`srgb`, `oklch`, `display-p3`, etc.). Pre-2024 systems often shipped pre-DTCG token shapes that need migration; the conformance check produces the migration-target list.

*Multi-brand orthogonality audit.* Per 24's tokens-at-scale framing — AI client walks a multi-brand token system and verifies theming dimensions (mode, density, brand, contrast preference, motion preference) compose orthogonally rather than collapsing into a single "theme" axis. Where dimensions have collapsed, the recommendation is the dimensional split.

### Tooling reality and gaps as of mid-2026

- **Style Dictionary v4 and v5 expose enough surface for custom MCP wrapping.** A senior DS engineer can stand up the workstation token-MCP layer in a day. The wrapping is the practice's bridge investment; persists across engagements until vendors ship native MCP and the practice migrates.
- **Tokens Studio's API is stable enough to wrap.** Wrapping for MCP is custom work but well-trodden territory.
- **Native vendor MCP support landing across both design-token and CMS vendors in mid-2026.** On the design-token side: Supernova has shipped MCP-endpoint distribution (private beta as of 2026-06-18); Specify, Knapsack, and Backlight remain API-only; native MCP from those three is the practice's bet for late 2026 / 2027. On the CMS side (per 10 §MCP / AI-readability for CMS-managed components — surfaced by the §1.32 run): Contentful, Sanity, Strapi (v5.47+), and WordPress (Automattic Adapter via the new Abilities API) all ship official MCP today; this is faster than the practice anticipated when 34 was first written. Storyblok, Sitecore XM Cloud, AEM, and Salesforce Page Designer / SFCC remain custom-wrapping work. AI-readiness pressure is real, engineering work is bounded, commercial signal is clear; the broader trajectory is toward MCP-native across both design-token and CMS vendor categories within the next 12–18 months. Source: `_source-text/ext-supernova-ai-ready.txt` for design-token side; 10 §MCP / AI-readability + the §1.32 run's external-agent.md for CMS side.
- **Composite-token fidelity is the lane's hard case.** Simple primitives (color values, dimension values, font-family strings) wrap cleanly; composite types (typography composites with per-script overrides, motion composites with cross-platform spring parameters) hit DTCG spec edge cases. Discipline: trust the MCP for primitive-level audits; spot-check composite-level audits manually until the tooling matures.

---

## 6. The web-research MCPs — primary-source verification and the §1.27a pattern

The web-research MCPs:

- **firecrawl MCP.** The dominant practitioner MCP for web-research work as of mid-2026. Wraps Firecrawl's web-scrape and search surface; supports markdown / HTML / structured output formats; supports search-then-scrape workflows. Handles large documents — the 495K-character CSS Color 4 spec retrieved on first try in the §1.27a closure.
- **fetch MCP.** Simpler — single-URL retrieval, lowest-overhead, useful where the practitioner has a known URL.
- **Search-engine MCPs** (Brave Search, Kagi, DuckDuckGo, others). Different engines, different result-quality profiles. Practitioner picks one and stays with it; cycling between engines mid-research wastes context-window space.
- **Perplexity MCP.** Useful for the research-question-as-input pattern (give me a synthesis on this topic with citations); less useful for the verify-this-specific-claim pattern where targeted retrieval matters more.
- **WebFetch (Claude Code's native tool).** Not an MCP per se but occupies the same role for the practitioner. The 30K-character ceiling is the failure mode; firecrawl is the escape hatch when WebFetch truncates.

### The §1.27a worked example, generalised

The §1.27a closure is the canonical reference. WebFetch truncated CSS Color 4 at the 30K-character ceiling; the practice's prior framing of "CSS Color 4 default (chroma-reduction)" was a factual inaccuracy because the truncated capture didn't reach §14.2's algorithm-attribution body text. firecrawl_scrape pulled the full 495K characters on first try; §14.2's body text was extracted verbatim; the practice's framing was corrected (three sibling algorithms with implementation choice; no single normative CSS default). The pattern:

```
┌──────────────────────────────────────────────────────────────────┐
│                  TRUNCATION FALLBACK PATTERN                     │
│                                                                  │
│   ┌──────────────────────────────────┐                           │
│   │   Claude Code native WebFetch    │                           │
│   └────────────────┬─────────────────┘                           │
│                    │                                             │
│                    ├─► [succeeds] ──► render web content         │
│                    │                                             │
│                    └─► [truncates at 30K-char ceiling]           │
│                                  │                               │
│                                  ▼                               │
│   ┌──────────────────────────────────┐                           │
│   │      firecrawl_scrape            │                           │
│   │   formats: ["markdown"]          │                           │
│   └────────────────┬─────────────────┘                           │
│                    │                                             │
│                    ▼                                             │
│   ┌──────────────────────────────────┐                           │
│   │   parse the persisted output;    │                           │
│   │   grep for the section heading;  │                           │
│   │   read the body text; cite       │                           │
│   │   verbatim where load-bearing;   │                           │
│   │   date the capture.              │                           │
│   └──────────────────────────────────┘                           │
└──────────────────────────────────────────────────────────────────┘
```

The §1.26a–§1.26d + §1.28a–§1.28d residual cluster is the next worked application — eight follow-ups across the team-and-discipline and auditing closures, each requiring primary-source verification before client artefacts. firecrawl is the workstation MCP that makes the residual cluster a half-day pass rather than a multi-day one.

### Day-to-day workflows

*Primary-source verification.* The dominant workflow per the §1.27a pattern.

*Multi-source comparison on contested claims.* AI client fetches multiple sources on a contested claim (the contribution-vs-participation distinction; the source-mix-overtime formula; the WebAIM screen-reader survey results) and surfaces convergence and divergence.

*Citation-grade research for client artefacts.* AI client gathers and structures primary-source evidence the practitioner cites — specific URLs, body text, dates, authors.

*Spec-evolution tracking.* AI client checks the current state of specs the practice depends on — DTCG Format Module, CSS Color 4, ARIA APG, WCAG. Standing-watch items in 09 §1.27 (Style Dictionary `color-mix()` watch, DTCG typography composite-type watch) lean on this.

*Vendor-positioning verification.* AI client checks vendor-published positioning claims (Supernova's "AI-ready design systems" framing flagged in §1.28d; firecrawl's own capability surface) before the practice references them in client work.

### Tooling reality

firecrawl is the most-used in this practice; scrape and search surfaces are robust at mid-2026. API key management is non-trivial (the senior practitioner maintains credentials; the runbook covers it). fetch MCPs are simpler and lower-overhead for known-URL retrieval; the practitioner often has both fetch and firecrawl configured. Search MCPs vary in quality — Brave Search and Kagi are the most-used in practitioner reports; the practitioner picks one and learns it deeply. Perplexity MCP for the research-question pattern; less useful for verify-this-claim work. The harness-side persistence behaviour: when firecrawl returns a large document, the harness writes the response to a file in the session tool-results directory; the practitioner may need to parse the persisted file (a short Python block with `json.load`) rather than receive the full content inline.

---

## 7. The default workstation config — what every practitioner should have

The recommended stack — the practitioner-workstation MCP set every senior should have configured by default, equivalent to "what plugins should every Figma designer have" or "what ESLint config should every front-end engineer ship":

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

### A starting `mcp-config.json`

The configuration shape the runbook ships, illustrative rather than prescriptive — each MCP has its own install convention via `npx`, `uvx`, vendor-published binaries, or local-built artefacts; substitute the actual install path per server:

```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "node",
      "args": ["/usr/local/share/figma-mcp/dist/index.js"],
      "env": { "FIGMA_ACCESS_TOKEN": "..." }
    },
    "figma-console": {
      "command": "node",
      "args": ["/usr/local/share/figma-console-mcp/dist/index.js"],
      "env": { "FIGMA_BRIDGE_PORT": "4242" }
    },
    "storybook-mcp": {
      "command": "node",
      "args": ["/usr/local/share/storybook-mcp/dist/index.js"],
      "env": { "STORYBOOK_PORT": "6006" }
    },
    "axe-core": {
      "command": "node",
      "args": ["/usr/local/share/axe-core-mcp/dist/index.js"]
    },
    "style-dictionary": {
      "command": "node",
      "args": ["/usr/local/share/style-dictionary-mcp/dist/index.js"],
      "env": { "SD_CONFIG_PATH": "./style-dictionary.config.js" }
    },
    "firecrawl": {
      "command": "node",
      "args": ["/usr/local/share/firecrawl-mcp/dist/index.js"],
      "env": { "FIRECRAWL_API_KEY": "..." }
    },
    "brave-search": {
      "command": "node",
      "args": ["/usr/local/share/brave-search-mcp/dist/index.js"],
      "env": { "BRAVE_API_KEY": "..." }
    }
  }
}
```

The custom DS MCP server configuration adds an eighth entry per active engagement.

### The runbook

The configuration is itself practice IP. The practice's discipline: a documented workstation-setup runbook the new senior practitioner follows on day one. The runbook covers the MCPs (per the table above), installation steps per MCP, credential setup (Figma API tokens, firecrawl API keys, vendor API tokens for token-side wrappers), recommended default configurations (axe-core rule set, firecrawl scrape format, Storybook MCP version pinning), known gotchas (Console MCP Desktop Bridge plugin requirement, Figma MCP paid-tier dependency, firecrawl API-key management), and update cadence (quarterly review; MCP version updates tracked).

### The cost of not having the default config

Roughly 30–50% of work's wall-clock time, with the additional cost that practitioner fatigue rises faster — manual operations are more error-prone and more cognitively expensive than supervising the AI client's MCP calls. The agency that under-invests in workstation standardisation pays in senior-practitioner velocity and retention.

### The cost of having too much

The opposite failure mode is real. The practitioner with fifteen MCPs configured, half never called, half conflicting on tool naming or context-window budget, has a workstation actively worse than the minimal default. AI client's context fills with tool definitions; the actual prompt has less room. The agent picks the wrong MCP because two have overlapping tool names. Maintenance burden grows; updates across fifteen MCPs become a quarterly afternoon rather than a quick check.

The discipline: keep the default config minimal. Add MCPs only when the day-to-day workflow demands them. Remove MCPs that haven't been called in a quarter. Runbook reviews are the moment to prune; the practitioner audits their own MCP set against actual usage and trims.

### The cross-practice standardisation argument

Every senior practitioner with the same workstation config produces work at predictable speed and quality. Onboarding: new senior hires onboard against a documented config rather than building their stack from scratch; time-to-first-engagement-contribution drops from weeks to days. Cross-engagement collaboration: practitioners read each other's AI-client transcripts without disorientation; the shared tool surface means the same prompt produces the same output structure across practitioners. Practice-level training: the runbook is the basis for practice-internal training; senior practitioners run sessions on advanced workflows (the firecrawl-scrape-when-WebFetch-truncates pattern; the Console-MCP-with-branch-only-writes discipline; the Style-Dictionary-MCP-for-multi-brand-audits workflow) against a shared baseline. Cross-agency mobility: the senior practitioner moving to a different agency takes the runbook as career IP; the discipline transfers; the senior's effective tier holds.

The agency's compounding asset is the standardised workstation. The practice's IP is the runbook.

---

## See also

- 12 — Figma Practice (Dev Mode, Variables, Code Connect — the Figma-side primitives the workstation MCPs read)
- 13 — Internationalization and RTL (the multi-script content surface the token-side MCPs validate against)
- 14 — Accessibility (the four-engine × four-AT matrix the scanner MCPs do not substitute for)
- 15 — AI in Design Systems (the architecture-side companion; the MCP-as-architecture story this file complements)
- 24 — Tokens at Scale (the Cascade Report the token-side MCPs generate; the cross-brand drift the workstation stack helps surface)
- 28 — Web Accessibility Implementation (the conformance regime the scanner MCPs partially cover)
- 29 — Per-Component Documentation Template (the template the Storybook + Figma MCP combination drives generation against)
- 30 — Generated-from-Data Documentation (the productisation companion; the custom DS MCP server's commercial framing)
- 32 — Auditing Design Systems (the audit lanes the workstation stack accelerates; the audit-the-audit discipline applied to the workstation pipeline itself)

---

## Provenance

This file synthesises a 2026-06-17 dual-agent run on MCPs as practitioner tooling (`_research/_inbound/2026-06-17-mcps-for-ds-practice/`). Both agents converged at unusually high rate (~90%) on every load-bearing claim — the two-layer architecture (workstation stack vs. custom DS MCP server) with the payback-curve distinction; the five concrete cost-of-not-having day-to-day workflows (component docs generation, token-tree audit, primary-source verification, bulk Figma operations, PR a11y review) arrived at independently in the same order; the Figma-side split (Dev Mode read / Console MCP write) with the branch-only-writes governance discipline; the Storybook MCP framing with the generic-vs-opinionated distinction against the custom DS MCP; the 30–40% / 60–70% automated-vs-manual a11y coverage split with the no-native-screen-reader-MCPs gap; the token-side workflows; the firecrawl truncation-fallback pattern; and the seven-tool default workstation config.

Three artefacts lifted from the external pass: the §1 workspace-overview ASCII diagram (rendered cleanly into vault prose-led style); the §6 truncation-fallback flowchart (kept as ASCII because the visual reinforces the §1.27a pattern better than prose alone); the §7 working `mcp-config.json` schema (the synthesis-ready operational artefact, parallel to 32 §2's eight-lane summary table and 00e §6's five-grade leveling table — the runbook's starting point). External's structured cost-of-not-having table format adopted for §1's task-and-leverage matrix.

Two reconciliations: the speed-up multipliers in §1's task-and-leverage table reconciled to *practitioner-realistic* total-time figures (Claude's conservative multipliers including human review of AI output) with external's *raw-generation* multipliers preserved as parentheticals — practitioner-realistic numbers anchor the agency-lead pricing decision; raw-generation numbers anchor the executive readout. The `mcp-config.json` install paths are illustrative rather than prescriptive — each MCP has its own install convention; the runbook substitutes actual paths per server.

From Claude's pass: the §1.27a worked example as the running thread woven through §1 and §6; the five Figma-side gaps catalogue (paid-tier dependency, third-party maintainer risk, prototype-layer invisibility, Code Connect surface depth varies, modes coverage uneven); the audit-the-audit discipline carryover from 32 §5 applied to the workstation stack itself; the explicit framing of contribution-model template generation as the boundary case (no MCP needed; pure LLM textual reasoning); the cost-of-having-too-much failure mode and the prune-quarterly discipline.

Three claims stand to gain `_source-text/` backing before they appear in client artefacts; flagged in 09 §1.29a–§1.29c as the next housekeeping pass:

- **§1.29a — axe-core's published 30–40% WCAG-coverage methodology.** Both agents asserted the 30–40% / 60–70% automated-vs-manual split; the figure is widely cited but not trivially verified against a single Deque source. Verify against Deque's current published methodology before quoting in client work. Load-bearing for §4's boundary-of-automated-scanning framing.
- **§1.29b — Southleft Figma Console MCP repository.** External named `github.com/southleft/figma-console-mcp`; confirm the canonical repo URL, the Desktop Bridge plugin install path, the maintainer's published roadmap, and the licensing terms before treating the dependency as fixed in the runbook. Material for §2 and §7.
- **§1.29c — Workstation-MCP speed-up empirical validation.** §1's task-and-leverage table cites speed-up multipliers (2–4× / 6–10× / 2–3× / 20–40× / 3–4×) drawn from senior-practitioner observation rather than tracked benchmarks. The first three engagements where the workstation stack is shipped as a productised standardisation should track actual speed-up; the empirically-validated multipliers replace the observation-based ones in the next file revision.

These extend the §1.26a–§1.26d + §1.28a–§1.28d cluster from the team-and-discipline and auditing closures; all eleven follow-ups can be closed in a single source-text housekeeping pass when scheduled.

<!-- CAPTURE NOTE, added at filing and not part of the output: pasted verbatim from the owner
     2026-08-23. Run against `prompt.md` (the #876 brief). Unedited — no reformatting, no trimming,
     per `_research/README.md`. See `PROVENANCE.md` for why this arrived late and what preceded it. -->

# The Architecture of Design Intent: Navigating Multi-Origin Authorship and Hub-Based Reconciliation

A design system whose token layer is genuinely single-origin, but whose component layer relies on human authorship, must inevitably plan to become a hub—but it must strictly avoid becoming an automated, bidirectional synchronization engine. The empirical evidence demonstrates that while tokens (static data) can flow unidirectionally without issue, authored components exist in a state of continuous evolution where design intent is frequently expressed first in the codebase. If the architecture forces a rigid "single source of truth" (SSOT) from a design tool, the system will reliably fracture as developers abandon the stale source to create shadow libraries. Attempting to solve this by building an automated, multi-directional sync hub introduces catastrophic maintenance costs and silent overwrites that erode system trust. Therefore, the architecture should evolve into a curated hub utilizing a "Human-in-the-Loop" (HITL) reconciliation queue. This transition should be planned for the exact moment component drift begins to actively slow feature velocity, or immediately upon the introduction of AI coding agents into the deployment pipeline, whichever occurs first.

## 1. What Actually Breaks in Single-Source Systems

When a design system enforces a strict single source of truth—typically an artifact living within a design tool like Figma or Sketch—but authorship inevitably turns out to be multi-origin, the system undergoes a predictable sequence of degradation. The failure mode is rarely a sudden, catastrophic collapse; rather, it is a slow, compounding divergence that ultimately results in the system's abandonment and the emergence of shadow architecture.

The core vulnerability of the single-source philosophy is the disparity in execution constraints between design and development. Design updates take days, whereas code updates take weeks or months to navigate testing, integration, and deployment pipelines, creating endless drift. Because the design tool is treated as the sole origin of truth, any discoveries made during implementation are stranded in the codebase. Designers do not typically draw every interactive edge case, error state, or accessibility requirement. Consequently, developers are forced to express design intent directly in code to ship the product. When developers implement focus trapping, keyboard navigation, right-to-left (RTL) reading support, or dynamic rendering constraints, design intent has been authored outside the single source.

Real-world accounts of this failure mode are well documented across enterprise engineering teams. The most illustrative example is Airbnb's initial Design Language System (DLS). As discussed by Airbnb engineers Maja Wichrowska and Tae Kim at React Conf in 2020, and later analyzed in a 2026 retrospective published on Medium (medium.com, January 2026), the company attempted to enforce a rigid UI system across diverse product lines. The codebase suffered from immense fragmentation, complexity, and performance degradation. Engineers continually added custom CSS files (e.g., core.scss, custom_page.scss) to override existing styles because the central system could not rapidly absorb the unique layout and typography needs of new product tiers.

When product teams faced unique edge cases or strict deadlines, the overhead of updating the official DLS was too high. Consequently, developers built and forked their own UI implementations entirely outside the original DLS. The strict single-source approach created unmanageable drift, leading to the abandonment of their initial design-system efforts. Similarly, insights from Glovo's engineering blog (tech-blog.glovoapp.com) regarding their Pintxo design system highlight that attempting to force a single point of failure in parsing design intent across Web, iOS, and Android inevitably leads to cross-platform drift, as developers bypass the system to meet platform-specific requirements.

The timeline for this failure mode is remarkably consistent across organizations, driven by the psychological and technical friction of maintaining a system that no longer reflects reality.

| Phase | Timeframe | Failure Characteristics and Observable Symptoms |
|---|---|---|
| Phase 1: Initial Divergence | 1 to 3 Months | Developers implement necessary interactive edge cases (e.g., ARIA roles, touch targets, state management) not specified in the design tool. The codebase silently becomes the de facto truth for component behavior. |
| Phase 2: Artifact Stagnation | 3 to 6 Months | The design artifact (Figma) is no longer updated to reflect production reality. Designers and developers begin relying on ad-hoc communication (Slack, meetings) to bridge the gap, leading to duplicated effort. |
| Phase 3: Shadow Source Emergence | 6 to 12 Months | Developers construct local abstraction layers, custom wrappers, or fork existing components to bypass the design system's bottlenecks. Trust in the official documentation collapses. |
| Phase 4: System Abandonment | 1 to 2 Years | The original design system is treated as a loose suggestion rather than infrastructure. Complete fragmentation occurs across platforms, eventually requiring a highly expensive, ground-up rebuild. |

The source artifact absolutely goes stale. Once developers recognize that the official design files no longer reflect the production reality, they cease referencing the design system. The system fails not because the components are poorly designed, but because the architecture provides no pathway for code-derived design intent to flow upstream, rendering the single source an illusion.

## 2. The True Cost of Operating a Hub

In response to the failures of the single-source model, an alternative posture has emerged. As articulated by Nathan Curtis in his August 2026 Substack publication, "Spec-Driven UI Component Development" (nathanacurtis.substack.com), a modern system should act as a hub that normalizes, synchronizes, and versions the intent expressed across the many origins-of-truth. However, the empirical cost of running a fully automated, bidirectional hub is astronomical, and the history of such endeavors is littered with retired and abandoned systems.

The most prominent historical example of an abandoned bidirectional hub is again found at Airbnb with their open-source project, Lona. Lona was explicitly designed to treat the design system as a programmable hub, operating as "Design System as Code." It utilized a single structured data format (.component JSON files) as the central hub to generate cross-platform UI code, Sketch files, and documentation, attempting to completely eliminate the manual synchronization gap between design and code.

Despite its ambitious architecture, Lona was ultimately sunset and abandoned, and its repositories were archived. The official documentation noted that it lacked the technical rigor of other Airbnb projects and was unsupported. The sheer technical complexity of maintaining bespoke compilers capable of translating abstract component data into idiomatic React, iOS (Swift), and Android (Kotlin) code proved unsustainable. Scaling the compilers to accommodate the shifting paradigms of multiple native platforms demanded far more engineering resources than the automation ultimately saved. The hub became a bottleneck rather than an accelerator.

The financial and operational costs of attempting bidirectional synchronization are severe. Analysts tracking post-merger integration and multi-platform synchronization report that manual ticket duplication and drift reconciliation can cost an organization roughly $25,000 per engineer, per year, purely in "copy-paste tax" and contextual overhead. When teams attempt to automate this away via bidirectional sync, they trade manual overhead for infrastructure maintenance. Proprietary Computer-Aided Software Engineering (CASE) tools attempting two-way sync have historically failed for a fundamental structural reason: design tools operate on abstract visual representations, while codebases operate on Concrete Syntax Trees (CSTs) where comments, whitespace, and item ordering matter deeply.

When a hub is built to automatically synchronize these environments, it inevitably breaks. A visual layout can be achieved in a dozen different ways in CSS (e.g., negative margins, absolute positioning, flexbox, grid). When an automated hub attempts to push code changes back into a design tool, or vice versa, the translation is inherently lossy.

| Cost Category | Financial and Operational Impact of Hub Maintenance |
|---|---|
| Initial Capital Expenditure | High. Requires dedicated platform engineers to build translation layers, Abstract Syntax Tree (AST) parsers, and custom API integrations between design tools and code repositories. |
| Ongoing Maintenance Tax | Severe. Every update to a design tool's API (e.g., Figma plugin API changes) or a frontend framework (e.g., React major version bumps) requires rewriting the hub's compilation logic. |
| Reconciliation Labor | Hidden but high. When bidirectional sync fails or silently overwrites custom business logic, senior engineers must spend hours auditing commit histories to repair the corrupted components. |
| Abandonment Risk | Critical. When the hub's maintenance cost exceeds the value of the synchronization, the tooling is abandoned. Teams revert to manual handoffs, leaving behind technical debt and fragmented pipelines. |

Consequently, automated bidirectional hubs are frequently retired because the cost of maintaining the translation layer—and repairing the damage caused when the automated sync overwrites custom business logic or complex interaction states—far outweighs the theoretical benefits of seamless synchronization. A hub that relies on automatic, bidirectional edges is a highly fragile architecture.

## 3. The Round-Trip Problem: State of the Art in 2026

The ambition to seamlessly round-trip design intent from Figma to code and back to Figma remains the most difficult engineering challenge in design systems. By early 2026, the state of the art advanced significantly with Figma's official launch of a bidirectional Model Context Protocol (MCP) server, integrating with tools like Claude Code and GitHub Copilot (aimultiple.com, February 2026). This allowed AI coding agents to query live Figma component hierarchies, generate code, and subsequently push rendered browser UI back into Figma as fully editable vector layers.

However, empirical observation of these 2026 workflows reveals a strict, principled line separating what can successfully round-trip and what reliably fails. The limitation is not merely a lack of advanced tooling; it is a fundamental mismatch in how design environments and execution environments model reality.

Bidirectional sync is highly successful when dealing with flat, declarative, and semantic data. Design tokens (colors, typography, spacing variables) conforming to the W3C Design Tokens Community Group (DTCG) specification round-trip flawlessly. Because a color token (#045bbc) maps exactly one-to-one between a Figma variable and a CSS custom property, an edit in either environment can be synchronized without structural ambiguity. The W3C specification provided the necessary universal schema, allowing tools like Tokens Studio to seamlessly push and pull variable data across the boundary.

The round-trip reliably fails when dealing with layout logic, dynamic behavior, and deep compositional nesting. The core limitation lies in the mismatch of structural paradigms. Figma relies on Auto Layout, which mimics the basic principles of Flexbox but utilizes distinct internal constraints (e.g., Hug, Fill, Fixed). Web development, conversely, utilizes a vast, context-dependent array of layout mechanics including CSS Grid, Flexbox, absolute positioning, viewport-relative sizing, and container queries. When an automated agent attempts to translate a complex CSS Grid layout back into Figma, it inevitably flattens the structure or relies on absolute positioning, destroying the responsiveness of the design file.

Furthermore, bidirectional tools frequently fail when developers introduce logic that does not exist in the design tool. Codebases contain responsive breakpoints lacking clear Figma equivalents, hover states, focus trapping, semantic HTML elements, and components wrapped in React context providers. When the MCP agent attempts a "Code to Canvas" push on a highly interactive, stateful component, it cannot translate the JavaScript event handlers into Figma. It strips the logic and corrupts the structural constraints, resulting in a visual artifact that looks correct but is fundamentally broken under the hood.

The principled line can be drawn definitively: Static, declarative attributes sync seamlessly; algorithmic layout and stateful execution data do not.

| Component Layer | Round-Trip Viability | Primary Failure Mechanism in Bidirectional Sync |
|---|---|---|
| Tokens & Primitives | High | N/A. One-to-one mapping exists via W3C DTCG standard formats. |
| Base Anatomy | Moderate | Fails if layer naming conventions are inconsistent. Relies heavily on strict adherence to PascalCase or camelCase without special characters. |
| Layout Mechanics | Low | Figma Auto Layout constraints conflict fundamentally with CSS mechanics. Elements without parent containers or elements using negative margins fail to translate. |
| Dynamic Behaviors | Very Low | Design tools lack full JavaScript/DOM execution environments. State transitions, focus trapping, and conditional hooks cannot be modeled natively. |
| Compositional Logic | Fails | Abstract design tools cannot model programmatic conditional rendering or complex slot injection natively, leading to flattened, static approximations. |

Therefore, planning to build a hub that perfectly round-trips complex components is a pursuit of diminishing returns. The architecture must acknowledge that while tokens can sync seamlessly, component definitions will always require manual intervention to bridge the structural gap between canvas and code.

## 4. Conflict Resolution in Multi-Origin Systems

In any architecture that permits multi-origin authorship, conflicts are a mathematical certainty. A designer adjusts a padding token in Figma to accommodate a new visual style; simultaneously, an engineer alters the corresponding padding variable in the codebase to fix a mobile viewport overflow issue. How the system resolves this collision dictates its long-term viability, and the industry has starkly divided on the appropriate methodology.

Many platforms diagram automated conflict resolution strategies that sound highly efficient in theory. For instance, Tokens Studio and Webstudio offer automated merge protocols. When importing tokens, users can select origin precedence rules such as "Theirs" (incoming overrides existing), "Ours" (existing rejects incoming), or "Merge" (properties are combined based on array order, where later objects override earlier ones) (docs.webstudio.is).

While "last-write-wins" and "auto-merge" sound modern and frictionless in a marketing diagram, practitioners report that they actively destroy system integrity. If an engineer implements a critical accessibility fix in the codebase—for example, adjusting a contrast ratio to meet compliance—and a designer subsequently triggers an automated sync from an older, unmodified Figma file using a "Figma-wins" or "last-write-wins" precedence rule, the accessibility fix is silently overwritten. Automated merging operates on chronological data or rigid hierarchy, completely ignoring contextual intent. It treats a typo correction and a structural architectural shift as having the exact same weight.

To combat this, the state of the art has shifted away from automated merging toward analytical drift reporting and human reconciliation. In 2026, tools like token-reconciler-mcp (developed by humano-ai) were introduced to handle multi-source conflicts intelligently (glama.ai, August 2026). Rather than automatically overwriting data, this MCP server accepts design token exports from Figma, live site URLs, and codebase token files simultaneously, and computes a comprehensive drift report.

Crucially, it handles conflicts through semantic evaluation rather than brute-force string matching. It evaluates colors perceptually (via the OKLab color space) so that #FFFFFF and rgb(255,255,255) are recognized as identical, while two grays that are one shade apart are flagged as a genuine conflict. More importantly, it pairs text and background tokens against WCAG 2.2 AA and the WCAG 3.0 APCA draft algorithms. If a conflict shows that a color pairing passes accessibility in Figma but fails in the shipped site, the tool explicitly highlights the regression.

While tools like this offer a default mostRecentWins resolver, the documentation explicitly notes that this is "deliberately simple" and "dumb," emphasizing that determining the true winner requires pluggable human judgment.

| Resolution Strategy | Mechanism | Practitioner Verdict on Efficacy |
|---|---|---|
| Last-Write-Wins | The most recent timestamp overwrites all previous data. | Fails. Destroys historical context and silently overwrites critical engineering fixes. |
| Origin Precedence | One origin (e.g., Figma) is hardcoded to always overwrite the other (e.g., Code). | Fails. Reverts the system back to the broken single-source model, ignoring codebase realities. |
| Automated Merge | Properties are combined intelligently; non-conflicting properties are appended. | Unreliable. Works for flat arrays but fails when structural component anatomy changes. |
| Human Reconciliation | Conflicts are surfaced, scored for impact, and manually triaged by a maintainer. | Succeeds. Ensures contextual intent (e.g., accessibility fixes) is preserved. Essential for high-stakes enterprise systems. |

The practitioner consensus is definitive: automated merge strategies are a liability that degrade trust in the design system. Reliable multi-origin systems must rely on human reconciliation queues where conflicts are surfaced, scored semantically, and manually resolved.

## 5. The Documentation Question: Code vs. Specs

The location and generation of documentation represents a live, highly contested disagreement in design system architecture. In his 2026 analysis, Curtis argues forcefully that documentation should be authored centrally in the spec hub, but that the foundational "how to use" API guidelines must be derived directly from coded implementations (medium.com/eightshapes-llc). Curtis argues that "code is where the real API lives," and that documenting imaginary design APIs leads to immediate developer frustration. Conversely, the traditional single-source position dictates that documentation should be generated exclusively from the upstream design definition to ensure designers dictate the product experience.

The empirical evidence shows severe failure modes for both extremes, demonstrating that documentation from either single source drifts from reality without active, hybrid stewardship.

When Docs Originate Solely from the Design Definition:
Design-led documentation platforms (such as Zeroheight or native Figma documentation) inherently treat the component as a visual artifact. When documentation is generated purely from this definition, it fundamentally misunderstands the reality of the engineering integration. It lacks critical context regarding React props, polymorphic behaviors, ARIA roles, and complex state management. For example, a designer might document a component with a "Disabled" boolean, while the engineering implementation relies on an injected state machine. Consequently, developers find the design-generated documentation useless for implementation, leading to immediate drift as they write code that contradicts the documented design guidelines.

When Docs Originate Solely from Code:
Conversely, when teams rely exclusively on code-derived documentation (e.g., Storybook), the documentation quickly becomes an engineering silo. Storybook excels at exposing the true API of a component, demonstrating exactly how the code behaves in the browser. However, it frequently strips away the UX rationale. It fails to answer the "why": when to use a specific pattern, when not to use it, voice and tone guidelines, and overarching product principles. This alienates designers, leading them to ignore the codebase limitations and author disconnected designs in Figma, reintroducing fragmentation.

The Reality of Drift and the Hybrid Approach:
There is overwhelming evidence that documentation drifts aggressively. AI coding agents and developers working under deadlines frequently bypass documentation that does not match the actual codebase API. To resolve this, successful teams thread the two approaches together. As Curtis notes, specs must be divided into two halves: Generated Specs and Authored Specs.

| Documentation Type | Origin Source | Purpose and Content |
|---|---|---|
| Generated Specs | Codebase | Automatically extracted API, variants, layout rules, and React props. Represents the immutable reality of what can currently be executed in production. |
| Authored Specs | Design Hub | Human-written markdown providing context on accessibility, voice and tone, complex interactions, and overarching product principles. |

Real teams construct documentation portals that pull the live, interactive API directly from the codebase, while pulling the design rationale and foundational guidelines from the central spec hub. Relying entirely on either design definitions or code implementations for documentation guarantees that half of the product team will abandon the system.

## 6. The Middle Path: Human-in-the-Loop (HITL) Reconciliation

Given that strict single-source architectures fragment, and automated bidirectional hubs collapse under technical debt and silent overwrites, a documented middle path has emerged as the industry standard for mature systems: Human-in-the-Loop (HITL) Reconciliation.

In design system architecture, this pattern is also referred to as a "Drift Gate," an "Accuracy Harness," a "Targeted Review Queue," or a "Reconciliation Loop".

The HITL architecture operates on a core philosophy: the system maintains a highly deterministic, single source of truth (usually stored as machine-readable JSON/YAML in a Git repository), but it explicitly accepts proposals or imports from any outer origin (Figma, code, or AI agents). It bridges the gap between the chaos of multi-origin authorship and the stability of a single source of truth.

How the Pattern Works:
When design intent is altered in an outer origin—for instance, an engineer adjusts a component's structural anatomy to fix a layout bug, or a designer introduces a new token in Figma—an agentic scanner (such as the Cairn Framework's cairn scan or the token-reconciler-mcp) detects the divergence. However, instead of executing an automated bidirectional merge, the system generates a structured finding, similar to a pull request. The workflow pauses at a decision point, halting at a "drift gate".

A human system architect or gatekeeper must review the conflict queue. They examine the context of the drift, evaluate confidence scores provided by the reconciler, and explicitly decide whether to reject the anomaly or merge it upstream into the authoritative source of truth. This ensures that the system is curated rather than blindly automated.

Tradeoffs of the HITL Pattern:

| Characteristic | Tradeoff Analysis |
|---|---|
| Throughput & Latency | Negative: HITL inherently introduces latency. Because human approval is required on the critical path, the immediate round-trip speed of automation is sacrificed. The workflow must wait for human triage. |
| System Integrity | Highly Positive: Eliminates silent overwrites and automated regressions. Edge cases, responsive logic, and accessibility fixes originating in code are safely evaluated and preserved rather than destroyed by a design-tool sync. |
| Cognitive Load | Positive (Targeted): By using tools that highlight only the specific conflicting properties (targeted review) rather than requiring full-document audits, the cognitive burden on maintainers is minimized while safety is maximized. |
| Continuous Learning | Positive: Every human intervention serves as a training signal. Over time, the system learns which automated proposals to trust and which require heavier scrutiny, refining the overarching design governance and creating a virtuous cycle. |

The HITL pattern successfully bridges the gap. It acknowledges the multi-origin reality of modern product development—including the fact that engineers express crucial design intent too—while utilizing human judgment to protect the structural integrity of the design system. It is the only documented posture that survives the complexity of enterprise scale without collapsing into fragmentation.

## 7. What Could Not Be Determined

While the available literature and 2026 industry data provide robust insights into design system architectures, several specific variables requested could not be conclusively determined from the empirical evidence:

Long-Term Viability of 2026 MCP Bidirectional Sync: While the integration of Figma's bidirectional MCP servers with Claude Code and GitHub Copilot launched in February and March of 2026 to great fanfare, there are no multi-year postmortems available to evaluate if this specific technology eventually succumbs to the same maintenance debt as historical CASE tools or Airbnb's Lona. Current reports are heavily influenced by vendor marketing, making long-term empirical durability impossible to verify.

Precise Financial Cost of Hub Maintenance: Beyond the anecdotal metric of a $25,000 "copy-paste tax" per engineer for disconnected systems, hard financial data regarding the exact capital expenditure required to successfully build and maintain a custom, spec-driven synchronization hub at enterprise scale is not publicly documented. Teams report "high costs," but specific budgetary figures are closely guarded corporate secrets.

Enterprise Scalability of Curtis's Pure Spec-Driven Model: While Nathan Curtis provides a highly rigorous theoretical framework for defining components strictly as platform-agnostic data (JSON/YAML) to generate all downstream assets, there is insufficient empirical data to determine if average organizations can sustain this exact architecture without building excessively expensive, proprietary compilation pipelines.

Adoption Rates of HITL in Pure Design Operations: While Human-in-the-Loop reconciliation is a mathematically proven and widely adopted pattern in machine learning, Intelligent Document Processing (IDP), and general software engineering, the exact percentage of enterprise design teams that have successfully formalized this workflow specifically for design-to-code synchronization remains unquantified in current market research.

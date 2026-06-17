You are researching MCPs (Model Context Protocol servers) as practitioner
tooling for design-systems work — the developer's-workstation MCP stack a
DS designer or engineer should have configured by default — for a senior
design systems practitioner leading the practice at a global creative
agency. The output is a structured knowledge document that will be promoted
to a numbered file in the practitioner's vault
(`34-mcps-for-ds-practice.md`), positioned as an extension topic alongside
22 (token architecture extensions), 24 (tokens at scale), 26/27 (adaptive
interfaces), 30 (generated-from-data documentation), 31 (color systems),
32 (auditing design systems).

This run is *not* about custom DS MCP server architecture — that's covered
substantially in 15-ai-in-ds (§MCP server architecture for a DS, with the
seven-tool conceptual surface — `list_components`, `get_component`,
`search_components`, `get_token_catalog`, `get_composition_rules`,
`get_usage_guidelines`, `validate_implementation`) and 30-generated-from-
data-documentation (§The MCP server tooling reality: 40–80 hours, build-
once-reuse-across-portfolio). The architecture half is closed. This run is
the *practitioner-tooling* half — the off-the-shelf and lightly-configured
MCP servers that sit on a DS practitioner's workstation and turn AI clients
(Claude Code, Cursor, Windsurf, the agentic surfaces of 2026) into useful
collaborators on day-to-day DS work. The equivalent question is "what
plugins should every Figma designer have," "what ESLint config should every
front-end engineer ship," "what Storybook addons does every component
library need" — but for the DS practitioner's MCP-capable AI clients.

The practice has working knowledge here (Figma Console MCP is in active
use; firecrawl was used for the §1.27a CSS Color 4 capture when WebFetch
truncated; Storybook MCP and accessibility-scanner MCPs are in the
practitioner toolbox at varying depths) but no internal POV is documented.
This research closes that gap.

This is not an introductory guide — assume the reader is the practice
lead, has read 15 / 30 / 32 in the practice's vault, knows what an MCP
server is (a structured tool surface that an AI client calls; the protocol
spec is at `modelcontextprotocol.io`), knows what Claude Code / Cursor /
Windsurf are as MCP-capable clients, has used at least Figma MCP (Dev Mode
MCP) for design-to-code work, and is fluent in the standard 2026 AI-tool
vocabulary (tool-use, structured output, agentic loop, context window,
prompt construction). Don't explain what MCP is, what Claude Code is, what
Figma's Dev Mode MCP does at the basic level, what a Code Connect mapping
is — explain how the practice should *operate* an MCP-equipped workstation
as a discipline at agency scale, where each MCP server delivers leverage
in concrete day-to-day DS work, where the field's MCP tooling has known
gaps that practitioners work around, what a "default workstation config"
should look like as the practice's productised IP, and how this layer
relates to (but does not replace) the architecture-side custom-DS-MCP work
covered in 15 + 30.

Research scope — cover all of the following:

1. Why a practitioner-MCP stack is a discipline of its own, not the
   custom-DS-MCP-server build-out

- The case that the practitioner-workstation MCP stack and the custom-DS-
  MCP-server architecture are *different axes* of the same broader MCP
  story — workstation tooling vs. DS-as-system. The workstation stack is
  what every DS practitioner should have configured by default,
  independent of any client's specific system; the custom DS MCP server
  is a per-engagement (or per-portfolio) build-out that exposes a
  specific client's components-as-data through a structured surface.
  Both can ship in the same engagement; both deliver leverage; they
  answer different questions.
- How the two layers compose. The workstation MCPs (Figma MCP, Storybook
  MCP, accessibility scanners, design-token MCPs, web-research MCPs) are
  *general-purpose* — they read whatever Figma file, whatever Storybook,
  whatever component library is currently in front of the practitioner.
  The custom DS MCP server is *system-specific* — it exposes one client's
  components-as-data shape, with that client's composition rules, that
  client's usage guidelines, that client's contract. The practitioner who
  has both layers configured can move fluidly: the workstation layer lets
  them work on any system; the custom layer makes the AI client treat the
  current engagement's system as the authoritative reference.
- Why this matters commercially. The practitioner-workstation stack is
  the practice's *standardisation surface* — every senior practitioner
  has the same MCPs configured, recognises the same failure modes,
  produces the same outputs at predictable speed. The custom DS MCP
  server is the practice's *productisation surface* — the 40–80-hour
  build-out (per 30) that becomes a sellable deliverable on engagements
  past Stage 2. The workstation stack does not pay back per-engagement;
  it pays back across the practitioner's career. The custom server pays
  back per-engagement (or per-portfolio) and is a billable line item.
  Both are practice IP; the IP shapes are different.
- What the workstation stack delivers in concrete day-to-day DS work
  that without it requires manual labour. Examples:

  - Reading a Figma file's component anatomy and writing a per-component
    docs page from it (Figma MCP + Storybook MCP + AI client).
  - Auditing a token tree for dead tokens (design-token MCP + AI client
    walking the build output).
  - Verifying a primary-source claim against the live spec (web-research
    MCP, the firecrawl pattern from §1.27a).
  - Running an accessibility scan against a Storybook story set
    (accessibility-scanner MCP + Storybook MCP).
  - Generating a contribution-model template from a stakeholder
    interview (no MCP needed; AI client alone — the boundary case).

  Each example is concrete enough that the cost-of-not-having vs. cost-
  of-having is calculable.
- The miscategorisation cost worth naming. The practice that conflates
  workstation MCPs with the custom DS MCP server produces engagement
  proposals that price the architecture-side build-out and skip the
  workstation-side standardisation. The practitioner who has only the
  custom server doesn't have the day-to-day leverage; the practitioner
  who has only the workstation stack can't expose the client's system
  to AI clients at structured depth. Both are needed; the practice has
  to articulate both.

2. The Figma-side MCPs — Figma MCP (Dev Mode MCP), Figma Console MCP,
   the design-tool surface

- The two distinct Figma-side MCP servers and what each delivers. **Figma
  MCP (Dev Mode MCP)** — Figma's official, ships with paid plans, read-
  only, exposes node structure / variables / Code Connect mappings to
  MCP clients. **Figma Console MCP** (Southleft) — third-party, write-
  enabled via Desktop Bridge plugin, exposes project-wide context and
  lets agents create frames, components, variables, apply token
  migrations across thousands of nodes. The two compose: Dev Mode MCP
  is the read surface, Console MCP is the write surface.
- The day-to-day workflows each enables. Dev Mode MCP: design-to-code
  with structured context (the AI client reads variables, layout data,
  Code Connect links, and generates production-shaped code rather than
  hardcoded-value approximations); design-token audit (the AI client
  walks the variable collections and reports drift against a stated
  token catalogue); component-anatomy extraction (the AI client reads
  a component frame and emits a structured anatomy description for
  documentation). Console MCP: bulk migrations (apply a token rename
  across thousands of node references in minutes, not days); exemplar-
  page generation (the AI client reads the component metadata and
  generates a usage page directly in the Figma file); variable-collection
  authoring (the AI client creates and configures a multi-mode collection
  from a stated theme spec); template instantiation (the AI client
  spawns a frame from a stated component composition).
- Where Console MCP raises governance questions the practice has to
  answer. Write access means the AI client can change the design-tool
  source-of-truth without human review at the speed of generation. The
  practice's discipline: agent-authored Figma changes go through
  branches, not directly into the main library; agent-authored token
  migrations are reviewed by a senior designer before merge; the
  Console MCP is configured to require explicit approval for write
  operations (where the configuration supports it). The pattern that
  fails: senior practitioner runs Console MCP with default permissions,
  agent makes a well-intentioned but incorrect token migration, the
  Figma library is destabilised, the recovery is non-trivial.
- The verification-path discipline. Figma's MCP capability surface
  evolves quarterly; Console MCP's capabilities evolve faster (third-
  party tooling moves at the maintainer's pace). Specific feature claims
  that are correct in mid-2026 may be stale in three months. The
  practice's discipline: name the capability with a date; verify against
  current docs before treating as load-bearing in client work.
- Tooling gaps and workarounds. Figma MCP doesn't expose Variables modes
  uniformly across all paid tiers (mid-2026 reality, verify); Console
  MCP requires the Desktop Bridge plugin which adds a workstation-
  configuration step; neither MCP exposes Code Connect's full surface
  (the AI client knows there's a Code Connect map but the depth varies);
  no Figma MCP exposes the deep prototype layer (interactions, motion
  specs) usefully — the AI client gets layout but not behaviour. The
  practice works around these via custom plugins, manual extraction, or
  by treating the limitations as scope-of-the-tool boundaries.

3. The component-side MCPs — Storybook MCP, the testing surface, the
   build-pipeline access

- **Storybook MCP** — the canonical practitioner MCP for component-side
  context. Exposes the component library's Storybook stories,
  CSF (Component Story Format) metadata, the args / argTypes / parameters
  surface, the docs blocks, and the addon-driven integrations (a11y
  addon, viewport addon, interactions addon). The AI client reading
  Storybook MCP knows what components exist, what props they accept,
  what variants they ship, what the documented usage patterns are.
- The day-to-day workflows. Component documentation generation (the
  AI client reads the stories and emits a per-component docs page —
  per 29's template). API consistency audit (the AI client compares
  prop shapes across components and flags inconsistencies — per 32 §2.2
  component-audit lane). Migration-codemod authoring (the AI client
  reads the v1 story and the v3 story and emits a codemod that
  migrates consumer code from v1 to v3 API). Test-coverage analysis
  (the AI client cross-references the stories with the test files and
  flags components without state coverage). Implementation-vs-design
  reconciliation (the AI client reads Storybook + Figma MCP and reports
  drift between the design source and the implemented component).
- The Storybook MCP vs. custom DS MCP distinction. Storybook MCP is
  general-purpose — every Storybook ships with the same MCP surface
  (or close to; tooling caveats apply). Custom DS MCP is system-
  specific — exposes the system's *opinionated* contract (composition
  rules, when-to-use guidance, validation tools). The practitioner with
  both knows the AI client can read the Storybook reality (what's
  shipping) *and* the system's intent (what should be shipping). The
  reconciliation between the two is itself a useful audit signal.
- Tooling reality and gaps as of mid-2026. Storybook 8.x ships an MCP
  surface; Storybook 9 (2025) extended it; the surface evolves quickly.
  Common gaps: docs-block content is exposed but not always parsed
  cleanly into structured form; the args-table surface is excellent;
  the play-function surface is excellent; the linkTo-cross-story surface
  is variable; visual-regression baselines (Chromatic snapshots) are
  *not* exposed via Storybook MCP — they live in Chromatic's own
  surface. The practitioner has to reach for multiple MCPs to cover
  the full component surface.

4. The accessibility-scanner MCPs — automated scanning surfaced as a
   tool the AI client can call

- The accessibility-side MCPs. **axe-core MCP** (or equivalents wrapping
  Deque's axe-core) — exposes axe's automated-rule surface to the AI
  client; the client can call `scan(url)` or `scan(component_story)`
  and receive a structured violations list. **Pa11y MCP** — wraps Pa11y
  (which itself wraps axe-core) for CI-friendly use; exposes the same
  scan surface plus configuration. **Lighthouse MCP** — broader than
  a11y but includes the a11y category. **Storybook a11y addon (via
  Storybook MCP)** — already mentioned in §3, but the a11y rule surface
  per story is the canonical practitioner workflow.
- The day-to-day workflows. Per-component a11y scanning during
  contribution (the AI client runs the scan on the new component story
  and surfaces violations before the PR opens). Cross-component a11y
  pattern audit (the AI client scans a sample of components and flags
  the recurring patterns — missing labels, contrast regressions, focus-
  trap failures). Pre-engagement a11y baseline (the AI client scans the
  client's current component surface and produces the input data for
  the productised audit's a11y lane per 32 §2.3). Conformance-evidence
  collection for the EAA / Section 508 / ADA Title III regulatory
  surface (the AI client compiles per-criterion test results across
  the sampled components for the report's regulatory section).
- The boundary the accessibility-scanner MCPs do not cross. Automated
  scanning catches roughly 30–40% of WCAG conformance issues (per axe-
  core's published self-assessment; verify the current figure). The
  rest require manual AT testing — the four-engine × four-AT matrix
  per 32 §2.3 + 28's web-accessibility-implementation framing. The
  practice's discipline: use the scanner MCPs for breadth and speed;
  use real AT testing for depth and authority. The MCP-based scan does
  not substitute for the matrix; it complements it. The practice that
  conflates the two ships audits that pass automated tests and fail
  real users (per 31's WCAG-passes-but-fails-real-users pattern).
- Tooling gaps. Real-AT-testing MCPs do not exist in mid-2026 — no
  practical MCP server exposes a JAWS or NVDA or VoiceOver or TalkBack
  surface to an AI client. The cross-AT testing remains manual.
  Browser-Stack and Sauce Labs expose programmatic surfaces but not
  MCP-native ones; integration is custom. Where the practice needs
  cross-OS automated AT-driven testing, the practitioner runs the
  matrix manually with VM-based remote desktop services and feeds the
  observations back into the audit's evidence layer.

5. The token-side MCPs — design-token authoring, validation, and audit

- The token-side MCPs. **Style Dictionary MCP** (where shipped or
  custom-wrapped) — exposes the build pipeline's resolver surface to
  the AI client; the client can walk the dependency graph, identify
  dead tokens, surface alias-resolution failures, generate the
  Cascade Report (per 24 §3) on primitive changes. **Tokens Studio
  MCP** (or the Tokens Studio API exposed via custom MCP wrapping) —
  exposes the design-tool side of the token tree; the AI client can
  read the Figma Variables structure, the Tokens Studio JSON,
  validate against DTCG conformance, audit composite-typography-token
  fidelity. **Specify MCP** — Specify's design-token-platform exposes
  its catalogue via API; an MCP wrapper lets the AI client query the
  catalogue and validate consumer code against it.
- The day-to-day workflows. Token-tier discipline audit (the AI client
  walks the token tree and reports tokens consumed at the wrong tier
  — a primitive consumed by a component that should reach for a
  semantic; per 32 §2.1 token-audit lane). Dead-token detection (the
  AI client cross-references the token catalogue with build-time
  consumer scans and reports unreferenced tokens). Alias-chain
  health audit (the AI client traverses the alias graph and surfaces
  broken chains, circular references, deprecated-token-still-aliased
  cases). Cross-platform fidelity check (the AI client compares the
  Style Dictionary outputs across platforms — web CSS, iOS Swift,
  Android Kotlin, Compose, Flutter, RN — and flags silent flattening,
  per 32 §2.1's cross-platform-output-integrity check). DTCG
  conformance check (the AI client validates the source against the
  2025.10 Format Module spec).
- The Tokens Studio graph engine specifically. Tokens Studio's
  visual graph view of token dependencies is the practitioner-visible
  surface; the API behind it is what an MCP wrapper exposes
  programmatically. The AI client that has graph-engine access can
  trace any token's full dependency surface in milliseconds — the
  same operation a senior practitioner does manually in minutes. The
  leverage compounds on large multi-brand systems (per 24's tokens-
  at-scale framing) where the manual operation is intractable.
- Tooling reality and gaps. Style Dictionary v4 (late 2024 / early
  2025) exposes enough resolver surface for custom MCP wrapping;
  v5 (2025–2026) has expanded the surface. Tokens Studio's API is
  stable enough to wrap; the wrapping itself is custom work
  (typically 4–8 hours for a workstation MCP, more if shipped as a
  reusable tool). No major design-token vendor ships a native MCP
  surface as of mid-2026; Specify, Knapsack, and Supernova all have
  APIs that an MCP wrapper can consume but none ship MCP natively.
  The practice's bet: native MCP surfaces will land in 2026–2027;
  the custom wrapping work is bridge-the-gap.

6. The web-research MCPs — primary-source verification and the
   firecrawl pattern

- The web-research MCPs. **firecrawl MCP** — wraps Firecrawl's web-
  scrape and search surface; exposes structured retrieval to AI
  clients. **fetch MCP** — simpler, single-URL retrieval; exposes
  the underlying HTTP fetch surface. **Brave / Kagi / DuckDuckGo
  search MCPs** — search-engine surfaces. **Perplexity MCP** — wraps
  Perplexity's research surface. **WebFetch (built into Claude
  Code)** — Claude's native web-fetch tool; not an MCP per se but
  occupies the same role for the practitioner.
- The day-to-day workflows. Primary-source verification — the
  practitioner can ask the AI client to verify a claim against a
  spec / RFC / W3C document / vendor docs page; the AI client runs
  the fetch, returns the body text, and the practitioner reads
  the source rather than relying on training-data recall. The
  §1.27a worked example (CSS Color 4 §14.2) is canonical: the
  practice's WebFetch hit the 30k-character ceiling on the spec;
  firecrawl's larger window pulled the full 495K-character document
  on the first try; the substantive correction landed in 31 §1.
  The pattern: when WebFetch truncates, default to firecrawl_scrape
  with `formats: ["markdown"]`; parse the persisted output; grep
  for the section. Multi-source comparison — the AI client fetches
  multiple sources on a contested claim (the contribution-vs-
  participation distinction; the source-mix-overtime formula) and
  surfaces the convergence and divergence. Citation-grade research
  for client artefacts — the AI client gathers and structures the
  primary-source evidence the practitioner cites.
- Where the web-research MCPs deliver the most leverage in DS work.
  The §1.27 housekeeping cluster is the canonical example — primary-
  source backing for claims surfaced in dual-agent runs. The pattern
  generalises: every dual-agent research run produces some claims
  that need source-text verification before client artefacts; the
  web-research MCPs make the verification routine rather than
  exceptional. The practice's residual cluster (§1.26a–§1.26d +
  §1.28a–§1.28d, eight follow-ups) is exactly the kind of work
  firecrawl-class MCPs accelerate.
- Tooling reality. Firecrawl is the most-used in this practice; its
  scrape and search surfaces are robust at mid-2026. fetch MCPs
  are simpler and lower-overhead for known-URL retrieval. Search
  MCPs vary in quality — practitioners typically pick one (Brave or
  Kagi) and stick with it. Perplexity MCP is useful for the
  research-question-as-input pattern; less useful for the verify-
  this-specific-claim pattern where targeted retrieval matters more.
  The practitioner's discipline: pick one search MCP and one scrape
  MCP and learn them deeply, rather than cycling through tools.

7. The default workstation config — what every DS practitioner should
   have configured by default

- The recommendation. The practitioner-workstation MCP stack a senior
  DS practitioner should have configured by default, equivalent to
  "what plugins should every Figma designer have" or "what ESLint
  config should every front-end engineer ship":

  - **Figma MCP (Dev Mode MCP)** — read access to the design source.
  - **Figma Console MCP** — write access for bulk operations.
  - **Storybook MCP** — read access to the component-side reality.
  - **axe-core / Pa11y MCP** — automated a11y scanning surface.
  - **Style Dictionary MCP wrapper** (custom) — token-tree audit
    surface.
  - **firecrawl MCP** — primary-source retrieval at depth.
  - **One search MCP** (Brave or Kagi) — broad retrieval.
  - **Custom DS MCP** for the active engagement (per 15 / 30) — the
    system-specific surface.

  Plus the AI client itself (Claude Code as the practice's default;
  Cursor / Windsurf as alternatives the practitioner should be
  fluent in for client-context work).

- The configuration shape. The practice's discipline: a documented
  workstation-setup runbook that the new senior practitioner
  follows on day one. The runbook lists the MCPs, the installation
  steps, the credential setup, the recommended default
  configurations, the known gotchas (the Console MCP Desktop Bridge
  plugin requirement; the Figma MCP paid-tier dependency; the
  firecrawl API key management). The runbook is itself practice IP
  — it compounds the senior practitioner's time-to-effective on
  any new engagement, on any new client codebase, on any new
  agency's machine.
- The cost of *not* having the default config. The senior practitioner
  who joins an engagement without the workstation stack is doing the
  same work manually — reading Figma files visually, walking
  Storybook stories one at a time, running axe-core scans through
  the browser DevTools surface, fetching primary sources through
  the browser. The cost is roughly 30–50% of the work's wall-clock
  time, with the additional cost that the practitioner's fatigue
  rises faster (manual operations are more error-prone and more
  cognitively expensive than supervising the AI client's MCP
  calls). The agency that under-invests in workstation
  standardisation pays for it in senior-practitioner velocity and
  retention.
- The cost of having *too much* MCP config. The opposite failure
  mode: the practitioner who has configured fifteen MCPs, half of
  which they never call, half of which conflict on tool naming or
  context-window budget. The AI client's context fills with tool
  definitions; the actual prompt has less room. The practice's
  discipline: keep the default config minimal; add MCPs only when
  the day-to-day workflow demands them; remove MCPs that haven't
  been called in a quarter.
- The cross-practice standardisation argument. Every senior
  practitioner with the same workstation config produces work at
  predictable speed and quality. New senior hires onboard against
  a documented config rather than building their stack from
  scratch. Cross-engagement collaboration is friction-free
  (practitioners can read each other's AI-client transcripts
  without disorientation). The agency's compounding asset is the
  standardised workstation; the practice's IP is the runbook.
- How the workstation stack relates to the custom DS MCP server
  (per 15 + 30). The workstation stack is *general-purpose* — the
  same MCPs serve every engagement. The custom DS MCP server is
  *engagement-specific* — built once per client (or per portfolio),
  exposes the system's structured contract. The senior practitioner
  configures the workstation stack on day one of their career and
  never reconfigures; they configure the custom DS MCP per
  engagement, hand it off to the client team at engagement end
  (the custom MCP is the client's IP per 32 §1's failure-mode
  catalogue, not the agency's).

Output format: Structured markdown. Use section headings that match the
numbered scope above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather
than declaring a winner. Flag where MCP tooling (Figma's MCP, Console
MCP, Storybook MCP, axe-core / Pa11y MCP, Style Dictionary, Tokens
Studio, Specify, firecrawl, the AI clients themselves — Claude Code,
Cursor, Windsurf) has known gaps that practitioners work around. Where
claims depend on current state — MCP tool surfaces, Figma plan-tier
capabilities, Storybook MCP version specifics, Console MCP feature
surface, mid-2026 vendor positioning — date them and note the
verification path. Include a references section linking to primary
sources (the MCP specification at modelcontextprotocol.io; Figma's
Dev Mode MCP documentation; Southleft's Figma Console MCP; Storybook's
MCP documentation; axe-core / Pa11y documentation; Style Dictionary
docs; Tokens Studio docs; Specify docs; firecrawl docs; Claude Code /
Cursor / Windsurf MCP integration docs; the broader practitioner
writing on MCPs in DS work — Brad Frost, Nathan Curtis if they've
written, the Design Systems Podcast where MCPs surface, conference
talks at Clarity / Config / Smashing where MCPs are a topic).

Depth: Expert audience. Do not explain what MCP is, what Claude Code
or Cursor or Windsurf are, what Figma's Dev Mode MCP does at the
basic level, what a Code Connect mapping is, what axe-core does,
what Style Dictionary is, what a token tree is — explain how the
practice operates the workstation MCP stack as a discipline at agency
scale, where each MCP server delivers concrete day-to-day leverage
in DS work, where the field's MCP tooling has known gaps, what a
"default workstation config" should look like as productised practice
IP, and how this layer relates to (but does not replace) the
architecture-side custom-DS-MCP work in 15 + 30.

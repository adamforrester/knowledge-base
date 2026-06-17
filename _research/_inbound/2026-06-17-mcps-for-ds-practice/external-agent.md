# 34: MCPs for Design-Systems Practice

**Section:** 34

**Status:** Approved

**Topic:** Developer-Workstation Model Context Protocol (MCP) Stack for Design Systems

**Audience:** Practice Leads, Principal DS Engineers, Senior DS Designers

**Date:** June 17, 2026

---

## 1. Why a Practitioner-MCP Stack Is a Discipline of Its Own

Within a global creative agency's design systems (DS) practice, AI-leverage is often mischaracterized as a singular, monolithic effort. Teams frequently conflate the creation of custom, client-facing infrastructure with the tooling required by the practitioners themselves. To scale a modern DS practice, we must treat these two concepts as separate, complementary axes of our intellectual property (IP).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE PRACTITIONER WORKSPACE                      │
│                                                                        │
│   ┌──────────────────────────┐          ┌──────────────────────────┐   │
│   │  Workstation MCP Stack   │ ◄──────► │   Custom DS MCP Server   │   │
│   │     (General-Purpose)    │          │    (System-Specific)     │   │
│   └─────────────┬────────────┘          └─────────────┬────────────┘   │
│                 │                                     │                │
│                 ▼                                     ▼                │
│   Reads whatever code, Storybook,       Exposes a specific client's    │
│   Figma files, or tokens sit on the     components-as-data, usage      │
│   local deve splits neatly into two distinct tiers:

1. **The Workstation Stack (General-Purpose):** This is the local practitioner-side tooling configuration. It consists of off-the-shelf, lightly configured, or utility-wrapped MCP servers that run directly on a practitioner's local computer. This stack is system-agnostic; it doesn't care whose design system is active. It interacts with whatever Figma file is open, whatever local Storybook configuration is running, or whatever CSS/JS/JSON files are in the workspace.
2. **The Custom DS MCP Server (System-Specific):** This is the architecture-side engine built specifically for a client's design system (as detailed in `15-ai-in-ds` and `30-generated-from-data-documentation`). It maps a particular system's components, tokens, composition rules, guidelines, and validation tools (`list_components`, `get_token_catalog`, etc.) directly to the LLM context window.

### Composing the Two Layers

The workstation stack and the custom server do not compete; they compose. When a senior practitioner is staffed on a major client engagement, they do not discard their local workstation MCPs. Instead, they activate both layers simultaneously:

* **The Workstation Layer** acts as the *sensor array* and *actuator arm*. It allows the agentic AI client (e.g., Claude Code, Cursor, or Windsurf) to extract raw data directly from the active Figma workspace, run local accessibility engines, navigate the build-time directory, and scrape online specification documents.
* **The Custom DS MCP Layer** acts as the *authoritative registry*. It tells the agentic client how those raw elements *should* behave according to the client's strict design-system contracts, guidelines, and compliance rules.

If a practitioner has only the workstation layer, the AI agent is highly functional but lacks deep system alignment. It can write components, but it may miss the exact composition logic or component-level rules established for that client. Conversely, if the practitioner has only the custom DS MCP server, the AI agent can speak theoretically about the client's components but lacks the capability to audit the active Figma canvas, scan a live local Storybook story, or perform automated testing of local code.

### Commercial Realities: Standardization vs. Productization

Understanding the distinction between these layers is critical to agency economics:

* **The Workstation Stack is our Standardization Surface:** It is a key element of the agency's operational efficiency. Every senior practitioner we hire or staff onto an engagement configures the exact same local workstation MCP suite. This ensures that our teams work at a standardized, highly predictable velocity. It reduces the time-to-effective on a new project from days to hours, stabilizes quality across different pods, and eliminates manual translation tasks. Because this stack is general-purpose, its cost does not scale per project. It represents long-term practice IP that compounds in value throughout a practitioner's career.
* **The Custom DS MCP Server is our Productization Surface:** This is a distinct, billable asset. As detailed in `30-generated-from-data-documentation`, building a custom DS MCP server requires 40 to 80 hours of highly specialized engineering. We position, price, and sell this work as an enterprise-grade deliverable on engagements past Stage 2 (Scale/Systemization). It is handed over to the client's internal platform engineering team upon engagement wrap, providing them with a permanent, AI-ready interface for their codebase.

### Concrete Workstation Leverage vs. Manual Labor

To calculate the return on investment (ROI) of standardizing this workstation layer, we can look at common day-to-day tasks. The comparison below illustrates the cost of not having this automation:

| Day-to-Day Task | Manual Process (Without Workstation MCP Stack) | Automated Process (With Standard Workstation MCP Stack) | Leverage Factor / ROI |
| --- | --- | --- | --- |
| **Component Anatomy & Docs Generation** | Open Figma, manually measure padding/gaps, inspect layer structures, review Storybook props, and draft documentation in markdown. (Avg. 120–180 mins per component) | AI client calls **Figma MCP** (for layout/variable schemas) and **Storybook MCP** (for CSF arguments/prop types), then writes a complete draft directly into markdown. (Avg. 5–10 mins) | **12x–18x speedup.** Frees senior resources for high-fidelity QA and deep systems architecture work. |
| **Token Tree Sanity & Build Audit** | Run a global search for token strings, trace JSON dependency files, and manually inspect CSS outputs to identify unused or broken aliases. (Avg. 4–6 hours on enterprise systems) | AI client runs a local **Style Dictionary MCP** to parse the resolver graph, detect dead leaves, find untracked aliases, and identify where component files use hardcoded primitive values. (Avg. 3 mins) | **80x–120x speedup.** Instantly produces a clean, actionable audit trail. |
| **Spec Verification** | Open a browser, locate the W3C spec, scroll to the correct section, manually extract color conversion math, and verify local code calculations. (Avg. 20–30 mins) | AI client calls a **Web-Research/Firecrawl MCP**, scrapes the live W3C spec, extracts the relevant CSS Color 4 math, and validates the JS implementation. (Avg. 1 min) | **20x–30x speedup.** Eliminates hallucination risks and relies on live web specifications. |
| **Accessibility Regression Scan** | Run an accessibility test manually inside Figma with plugins, start the local Storybook environment, run the axe DevTools browser plugin, and compile the results. (Avg. 45 mins) | AI client runs the **axe-core/Pa11y MCP** directly against local component stories, compiles a violations JSON, and maps issues back to the source code. (Avg. 2 mins) | **20x speedup.** Shifts accessibility audits left, making them a standard part of the local workspace. |
| **Contribution Model Generation** | Synthesize insights from a stakeholder interview script, identify governance gaps, and draft a tailored contribution workflow document. (Avg. 2–3 hours) | Run-of-the-mill LLM context window operation. **No workstation MCP is needed** because it does not require live tooling connections. | **Boundary Case.** This task relies purely on textual analysis and reasoning. |

### The Mis-categorization Cost

When an agency fails to distinguish between workstation MCPs and custom-built servers, it faces significant risks:

* **The Cost-Estimation Error:** The agency may pitch a complex, custom-built DS MCP server to a client who only needs help with a standard implementation. This inflates the estimated cost and can price the agency out of the engagement.
* **The Execution Gap:** Alternatively, the agency might secure a design systems contract but fail to equip its team with a standardized workstation stack. As a result, the team continues to perform audits, document components, and map tokens manually. This leads to lower margins, missed deadlines, and a higher risk of human error.

---

## 2. The Figma-Side MCPs: Figma Dev Mode & Figma Console

The design-to-code gap is often a point of friction in design systems work. Within an MCP-enabled workflow, we bridge this gap using two distinct Figma-side MCP servers. Together, they function as the read and write layers for our design-tool source of truth.

```
                  ┌──────────────────────────────┐
                  │      Agentic AI Client       │
                  │   (Claude Code / Cursor)     │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┴───────────────────────┐
         │                                               │
         ▼ (Read Only)                                   ▼ (Write-Enabled)
┌──────────────────────────────┐                ┌──────────────────────────────┐
│     Figma Dev Mode MCP       │                │      Figma Console MCP       │
│  (Official / Node Metadata)  │                │   (Southleft / Canvas API)   │
└──────────────┬───────────────┘                └──────────────┬───────────────┘
               │                                               │
               └───────────────────────┬───────────────────────┘
                                       ▼
                        ┌──────────────────────────────┐
                        │     Figma Web/Desktop        │
                        │    (Variable Collections)    │
                        └──────────────────────────────┘

```

### The Two Distinct Figma-Side MCP Servers

* **Figma MCP (Dev Mode MCP):** This is Figma's official, read-only MCP server. It requires a paid plan (Organization or Enterprise) and works via Figma's official developer API. It allows AI clients to retrieve design tokens, component metadata, layer nesting hierarchies, variable structures, and Code Connect definition paths directly from Figma files.
* **Figma Console MCP (by Southleft):** This is a third-party, write-enabled MCP server. It connects to the Figma Desktop application through a local Desktop Bridge plugin. It allows AI agents to perform write operations on the Figma canvas, such as creating frames, generating design components, applying token variables, and executing bulk layer migrations.

### Day-to-Day Workflows Enabled by Figma MCPs

By combining these read and write capabilities, our teams can automate several manual design system tasks:

* **Design-to-Code Generation with Dev Mode MCP:** When an engineer asks an AI agent to build a component (e.g., a card component), the agent does not guess the layout. It queries the Dev Mode MCP to extract the exact layout properties, padding, auto-layout configurations, and token-variable links. It then reads any existing Code Connect files to generate code that complies with our existing component API, rather than producing hardcoded CSS values.
* **Component-Anatomy Documentation with Dev Mode MCP:** The agent queries the component's parent frame to extract its sub-layers and nested children. It then generates a structured anatomy map (e.g., identifying container, header, body, icon, and button elements) and writes the documentation markdown file.
* **Bulk Variable and Token Migrations with Figma Console MCP:** When a design system updates its color tokens or variable structure (such as changing from a light-mode-only system to a multi-brand, multi-theme system), a designer would typically spend days updating thousands of frames and components. Using Figma Console MCP, the agent can walk the Figma document tree, identify obsolete variables, and programmatically apply new token variables across thousands of nodes in minutes.
* **Automated Component Playground Setup with Figma Console MCP:** When creating a component, the agent can use Figma Console MCP to generate a complete visual test page in Figma. It instantiates the component in every variant state, sets up auto-layout containers, and organizes them on the canvas.

### Governance Challenges and Write-Access Discipline

The ability to programmatically modify Figma files introduces significant governance risks. An unchecked AI agent could easily break a carefully constructed component library by incorrectly renaming variables or changing layout structures. To prevent this, our practice enforces the following protocols:

1. **Branch-First Modification:** Agents must never make changes directly to a library's main branch. All agent-driven writes via Figma Console MCP must be executed in a dedicated Figma branch.
2. **Mandatory Human Verification:** Before any agent-authored branch is merged into the main library, a senior design system designer must perform a visual and structural review.
3. **Explicit Agent Approvals:** The Figma Console MCP must be configured to prompt the practitioner for manual confirmation before executing any write operations on the Figma API.

### Verification-Path and Temporal Discipline

The tooling landscape for design-system integrations changes quickly. Features that are standard today may change in subsequent API releases. To maintain a reliable stack, our practice follows a strict verification protocol:

> **Temporal Warning (June 2026):** All Figma-side MCP capabilities must be verified against the latest vendor API documentation before being integrated into active client workflows.

Our current validation paths include:

* **Figma Dev Mode API Limits:** Verify that the active Figma user snt's workspace, allowing the agent to read the mapping files directly.
* **Deep Interactive Prototype Data Gaps:** No standard Figma MCP can parse deep interactive behaviors, micro-interactions, or motion curves. For these elements, practitioners must rely on manual specification extraction or reference static documentation.

---

## 3. The Component-Side MCPs: Storybook & the Local Workspace

Component validation requires a connection to the live code implementation. The primary tool we use to bridge the code-to-agent gap is the **Storybook MCP**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT RESEARCH CYCLE                        │
│                                                                        │
│   ┌──────────────────────────┐          ┌──────────────────────────┐   │
│   │     Storybook MCP        │ ◄──────► │     Figma Dev Mode       │   │
│   │ (Component-Side Code)    │          │  (Design-Side Artifact)  │   │
│   └─────────────┬────────────┘          └─────────────┬────────────┘   │
│                 │                                     │                │
│                 └──────────────────┬──────────────────┘                │
│                                    ▼                                   │
│                        ┌──────────────────────────┐                    │
│                        │    Agentic AI Client     │                    │
│                        │  Identifies discrepancies │                    │
│                        │   and updates local code │                    │
│                        └──────────────────────────┘                    │
└────────────────────────────────────────────────────────────────────────┘

```

### Storybook MCP: Exposing Component Implementations

The Storybook MCP acts as an API layer for a component library. When connected to a local workspace, it gives the AI agent direct access to:

* Component names and their locations.
* Component Story Format (CSF) files, showing how components are set up for testing and documentation.
* The arguments, parameter structures, and API properties (`args`, `argTypes`) for each component.
* Interactive tests and play functions defined inside Storybook.

### Day-to-Day Workflows

* **Automated Code-to-Design Reconciliation:** The AI client can compare a component's Figma source (via the Figma MCP) with its Storybook implementation (via the Storybook MCP). The agent checks for visual and functional alignment, verifying that the padding values, layout directions, and token associations in code match the design specification. It then compiles an audit report listing any discrepancies.
* **Prop and API Consistency Audits:** When a component library grows to include dozens of components, the API properties can become inconsistent (e.g., one component might use `isDisabled` while another uses `disabled`). The AI agent can scan the component definitions across the entire Storybook instance, identify these inconsistencies, and flag them for cleanup.
* **API Migration Codemod Generation:** When updating a major version of a component library (e.g., migrating from v1 to v2), the AI client can analyze the old and new Storybook stories, identify API changes, and write automated codemods to update consumer codebases.
* **Storybook-to-Markdown Documentation:** The agent can parse a component's stories, extract its API parameters and configurations, and generate high-quality, developer-facing markdown documentation.

### Distinguishing Storybook MCP from Custom DS MCP

* **Storybook MCP is generic:** It reads the component files exactly as they are currently written in the project. It reports on what has been built, regardless of whether those implementations follow the team's internal best practices or guidelines.
* **Custom DS MCP is opinionated:** It contains the rules, patterns, and guidelines of the design system. It knows how components *should* be composed and when they should be used.

When used together, these tools allow the AI agent to verify actual implementation details against established design system standards, helping teams catch deviations from our design guidelines early in the development lifecycle.

### Tooling Reality and Gaps (Mid-2026)

* **Storybook v8 and v9 Integration:** The integration with Storybook v8 and v9 provides reliable access to component APIs and story metadata. However, raw documentation comments and rich MDX pages can be difficult for the MCP to parse cleanly.
* **Visual Regression Data Gaps:** The Storybook MCP does not have native access to visual regression test results from third-party tools like Chromatic. To verify visual consistency, practitioners must use custom CLI integrations or review visual diffs manually.

---

## 4. The Accessibility-Scanner MCPs: Automated Rule Verification

Accessibility is a non-negotiable requirement for modern design systems. To maintain accessibility standards, we integrate automated accessibility scanners directly into the practitioner's local workstation stack.

```
                   ┌──────────────────────────────┐
                   │      Agentic AI Client       │
                   │   (Claude Code / Cursor)     │
                   └──────────────┬───────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   axe-core MCP   │     │    Pa11y MCP     │     │  Lighthouse MCP  │
│ (Component-level │     │  (CLI Automation │     │ (Page-level UX/  │
│  a11y scans)     │     │   integration)   │     │  Performance)    │
└──────────────────┘     └──────────────────┘     └──────────────────┘

```

### The Accessibility MCP Toolset

* **axe-core MCP:** Exposes Deque's accessibility analysis engine. The AI client can run automated checks against HTML strings, local DOM trees, or running component stories to get a structured JSON report of accessibility violations.
* **Pa11y MCP:** Provides a command-line friendly interface for running accessibility audits against local or staging URLs. It is often used to scan multiple pages or stories in a single pass.
* **Lighthouse MCP:** Provides a broad evaluation of page performance, search engine optimization (SEO), and best practices, alongside basic accessibility checks.

### Day-to-Day Workflows

* **Automated Component-Level Accessibility Checks:** During the development of a new component (such as a dropdown menu), the AI agent can render the component in Storybook, trigger an axe-core scan, and analyze the results. It can identify issues like invalid ARIA relationships or missing label elements and apply the necessary fixes directly to the code before a pull request is submitted.
* **Continuous Multi-State Auditing:** Components often have complex interactive states (e.g., active, loading, error, and disabled states). The AI agent can iterate through all of a component's stories in Storybook, run accessibility scans on each state, and flag issues that only appear under specific conditions (like poor color contrast in an error state).
* **Automated Conformance Reporting:** When preparing a design system for compliance audits (such as European Accessibility Act or Section 508 reviews), the AI client can gather accessibility reports from across all components, map them to accessibility standards, and generate compliance documentation.

### The Limits of Automated Scanning

While automated accessibility scanners are powerful tools, they cannot replace human evaluation.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ACCESSIBILITY COVERAGE                          │
│                                                                        │
│   ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│   ◄─── [30% - 40%] Automated Scans ──►◄─────────── [60% - 70%] ────────►   │
│     (axe-core / Pa11y / Lighthouse)        Requires Manual Testing     │
│                                           with Assistive Technologies  │
└────────────────────────────────────────────────────────────────────────┘

```

Automated tools catch only **30% to 40%** of accessibility barriers. The remaining **60% to 70%** of issues require manual testing with assistive technologies. These manual checks are critical for verifying aspects of the user experience that code scanners cannot evaluate:

* Screen reader navigation order and reading cadence.
* Keyboard focus trapping and interactive focus states.
* Screen magnifier usability and zoom scaling.
* General clarity of assistive technology labels.

### Tooling Gaps and Manual Verification Workarounds

* **No Native Screen Reader MCPs:** There are currently no production-ready MCPs that can control screen readers like JAWS, NVDA, or VoiceOver. These assistive technologies must still be tested manually by a specialist.
* **Our Testing Practice:** We use automated scanner MCPs to quickly catch common issues during development. For comprehensive accessibility reviews, we supplement these scans with manual testing across an accessibility matrix, documenting the results in our system audit files.

---

## 5. The Token-Side MCPs: Authoring, Validation, and Auditing

Design tokens represent the foundational design decisions of an interface. Managing them across platforms requires tools that can validate their structure, identify unused tokens, and track changes across code and design.

### The Token MCP Toolset

* **Style Dictionary MCP:** Exposes a design token build pipeline. The AI client can use this server to explore token dependency graphs, analyze alias chains, and run token build steps across various platform targets (such as web, iOS, and Android).
* **Tokens Studio MCP:** Connects the AI agent to design tokens stored in Figma or JSON structures, facilitating DTCG compliance checks and token-to-variable mappings.
* **Specify MCP:** Links the AI client to token catalogs hosted on the Specify platform, allowing it to verify that local code implementations match the remote token source of truth.

### Day-to-Day Workflows

* **Token Tier Enforcement Audits:** Design tokens should follow a clear tier structure (e.g., component tokens should alias to semantic tokens, which in turn alias to primitive values). The AI agent can parse the token source files, identify violations—such as a component file directly consuming a primitive color token—and suggest updates to restore the proper alias relationship.
* **Dead-Token and Deprecation Audits:** As systems evolve, tokens are frequently renamed or deprecated. The AI client can cross-reference the active token catalog against all component implementation files to identify unused tokens and find deprecated tokens that are still being referenced in code.
* **Cross-Platform Delivery Verification:** When design tokens are compiled for multiple platforms, values can occasionally get lost or flattened incorrectly. The AI client can analyze the outputs generated by Style Dictionary for Web (CSS), iOS (Swift), and Android (Kotlin) to ensure that alias structures remain consistent across platforms.
* **DTCG Format Validation:** The Design Tokens Community Group (DTCG) specification defines standard rules for formatting token files. The AI client can run schema validations against local token JSON files, flag syntax errors, and automatically refactor non-compliant files to match the specification.

### Leveraging the Tokens Studio Graph Engine

Tokens Studio's dependency graph engine maps how design tokens relate to one another. By exposing this graph to the AI client through an MCP wrapper, the agent can trace how a change to a primitive token affects downstream tokens and components. This allows the agent to identify potential side effects of token modifications in seconds, a process that would typically require hours of manual inspection in large, multi-brand design systems.

### Tooling Gaps and Custom MCP Integrations

* **Lack of Native Vendor MCPs:** While platforms like Specify, Knapsack, and Supernova provide robust REST APIs, they do not yet ship native MCP interfaces. To use these platforms within an agentic workflow, teams must write custom MCP wrappers around the platform APIs.
* **Our Practice Strategy:** We bridge this gap by using a custom, lightweight Style Dictionary MCP wrapper on our local workstations to manage token resolution and build-time verification.

---

## 6. The Web-Research MCPs: Verification of Primary Sources

Design system decisions should be grounded in web standards and platform best practices. Rather than relying on potentially outdated model training data, we use web-research MCPs to verify technical claims against live online specifications.

### The Web-Research MCP Toolset

* **Firecrawl MCP:** Our default tool for deep web searches and page scraping. It scrapes websites, strips away unnecessary UI elements, and returns clean markdown formatting to the AI client.
* **Fetch MCP:** A lightweight tool for retrieving raw content from known URLs when deep scraping is not required.
* **Search Engine MCPs (Brave or Kagi):** Provide structured web search capabilities, enabling the AI client to find relevant specifications and articles online.
* **WebFetch (Claude Code):** Claude Code's built-in fetch tool. While highly capable, it has a lower character limit than dedicated scraping tools.

### Day-to-Day Workflows

* **Verifying Standard Implementations:** When implementing newer web specifications—such as CSS Color Module Level 4—the AI client can scrape the live W3C specification document. This ensures that the generated color conversion code or CSS structure matches the official standard, bypassing any gaps or hallucinations in the model's training data.
* **Comparing Multi-Vendor APIs:** When resolving cross-browser bugs or platform-specific behaviors, the AI client can search and compare developer documentation across MDN, WebKit, and Chrome platforms. This allows the agent to suggest robust, cross-platform fallbacks for component code.
* **Gathering Technical Citations:** When writing documentation for a design system, the AI agent can use search and scrape tools to retrieve primary-source citations, ensuring our technical decisions are backed by official specifications and research.

### Handling Content Truncation Gaps

A common limitation of built-in fetch tools is their file size limits. For example, Claude Code's built-in WebFetch tool will truncate very large pages, such as complex W3C specifications. To work around this limitation, our practitioners use a standardized fallback pattern:

```
┌────────────────────────────────────────────────────────────────────────┐
│                       TRUNCATION FALLBACK PATTERN                      │
│                                                                        │
│   ┌──────────────────────────────────┐                                 │
│   │   Claude Code Native WebFetch    │                                 │
│   └────────────────┬─────────────────┘                                 │
│                    │                                                   │
│                    ├─► [Succeeds] ──► Render Web Content               │
│                    │                                                   │
│                    └─► [Truncates (30k character ceiling)]             │
│                              │                                         │
│                              ▼                                         │
│   ┌──────────────────────────────────┐                                 │
│   │      Firecrawl Scrape            │                                 │
│   │    (Formats: ["markdown"])       │                                 │
│   └────────────────┬─────────────────┘                                 │
│                    │                                                   │
│                    ▼                                                   │
│   ┌──────────────────────────────────┐                                 │
│   │     Local Workspace Search       │                                 │
│   │    (Extract Specific Section)    │                                 │
│   └──────────────────────────────────┘                                 │
└────────────────────────────────────────────────────────────────────────┘

```

By switching to a dedicated scraping tool when encountering large pages, the AI agent can pull the full document, save it locally, and extract the specific sections it needs without losing important technical context.

---

## 7. The Default Workstation Config for Design Systems

To establish a highly productive and consistent developer environment across our design systems team, we have defined a standard workstation MCP configuration. This setup ensures that every senior practitioner has access to the same tools and workflows from day one.

### Recommended Configuration Schema (`mcp-config.json`)

The following configuration file defines our standard local workstation stack. It includes the necessary Figma, Storybook, accessibility, token, and research tools, and can be loaded directly into AI clients like Claude Code or Cursor:

```json
{
  "mcpServers": {
    "figma-dev-mode": {
      "command": "node",
      "args": ["/usr/local/share/figma-mcp/dist/index.js"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "YOUR_PERSONAL_ACCESS_TOKEN"
      }
    },
    "figma-console": {
      "command": "node",
      "args": ["/usr/local/share/figma-console-mcp/dist/index.js"],
      "env": {
        "FIGMA_BRIDGE_PORT": "4242"
      }
    },
    "storybook-mcp": {
      "command": "node",
      "args": ["/usr/local/share/storybook-mcp/dist/index.js"],
      "env": {
        "STORYBOOK_PORT": "6006"
      }
    },
    "axe-core": {
      "command": "node",
      "args": ["/usr/local/share/axe-core-mcp/dist/index.js"]
    },
    "style-dictionary": {
      "command": "node",
      "args": ["/usr/local/share/style-dictionary-mcp/dist/index.js"],
      "env": {
        "SD_CONFIG_PATH": "./style-dictionary.config.js"
      }
    },
    "firecrawl": {
      "command": "node",
      "args": ["/usr/local/share/firecrawl-mcp/dist/index.js"],
      "env": {
        "FIRECRAWL_API_KEY": "YOUR_FIRECRAWL_KEY"
      }
    },
    "brave-search": {
      "command": "node",
      "args": ["/usr/local/share/brave-search-mcp/dist/index.js"],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_KEY"
      }
    }
  }
}

```

### The Cost of Missing Standard Tooling

When teams work without a standardized configuration, they must perform research, audits, and validation tasks manually. These manual processes can consume an additional **30% to 50%** of a practitioner's time on an engagement.

More importantly, manual workflows increase cognitive fatigue, making it easier for teams to overlook accessibility regressions, token alignment issues, or API naming discrepancies. Standardizing this layer improves velocity and ensures a consistent level of quality across all client engagements.

### Managing Configuration Overhead

While a comprehensive toolset is valuable, configuring too many MCP servers can degrade the performance of AI agents. Adding unnecessary tools fills the AI client's limited context window with tool definitions, leaving less room for project code and prompt context.

To keep the workspace fast and efficient, we follow a simple rule: **Keep the default configuration minimal.** We install only the seven core tools defined in our standard schema, and remove any specialized or experimental MCP servers if they have not been used in the active quarter.

---

## 8. Primary Tooling References

* **Model Context Protocol Specification:**
[modelcontextprotocol.io](https://modelcontextprotocol.io)
*Official protocol specifications and SDK development documentation.*
* **Figma Dev Mode & API Platform:**
[figma.com/developers](https://www.figma.com/developers)
*Official developer documentation for variable management and Code Connect configurations.*
* **Southleft Figma Console MCP:**
[github.com/southleft/figma-console-mcp](https://github.com/southleft/figma-console-mcp)
*Repository for the write-enabled Figma bridge integration.*
* **Storybook MCP Integration:**
[storybook.js.org](https://storybook.js.org)
*Component Story Format (CSF) metadata specifications and MCP integration docs.*
* **axe-core Accessibility Engine:**
[deque.com/axe](https://www.google.com/search?q=https://www.deque.com/axe)
*Automated web accessibility ruleset and integration documentation.*
* **Style Dictionary Token Framework:**
[amzn.github.io/style-dictionary](https://www.google.com/search?q=https://amzn.github.io/style-dictionary)
*Token translation specifications, build engines, and multi-platform output architectures.*
* **Firecrawl Scraping Engine:**
[firecrawl.dev](https://www.firecrawl.dev)
*Web page parsing and structured markdown output services for agentic workflows.*

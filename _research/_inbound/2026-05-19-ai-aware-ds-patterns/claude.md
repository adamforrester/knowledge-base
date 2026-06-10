# AI-Aware Design System Patterns and Conversational-UI Primitives — Field Survey, May 2026

A pattern-level survey of the eighteen design systems cited as AI-aware, plus extensions surfaced during research, organised against the brief's seven-section spine. All claims are tied to a fetched URL, dated 2026-05-20. Where a source on the list does not in fact publish AI-aware patterns on inspection, that is recorded as a finding rather than papered over.

---

## 1. The shape of the field — what "AI-aware" means in 2026

The brief's distinction between (a) AI features the design system *operates internally* (token critique, codegen, MCP servers) and (b) AI features the system *ships as patterns to consumers* (chat input, streaming, citation, refusal) is load-bearing in 2026 because several systems on the source list publish (a) but not (b). Mantine is the clearest example: it publishes an MCP server (`@mantine/mcp-server`), `llms.txt` files and "skills for AI agents," but ships zero consumer-facing AI components — no chat surface, no prompt input, no message primitives (source: https://mantine.dev/, fetched 2026-05-20). Confusing the two is the most common category error in scoping conversations.

Three forcing functions converged in 2024–2026 to push (b) into the mainstream:

- **Conversational surfaces moved from experimental to first-class** in flagship products (ChatGPT, Claude, Gemini, Copilot, Cursor). Enterprise design systems can no longer treat chat as a curiosity.
- **Agent platforms shipped under existing brands** — Atlassian Rovo, Salesforce Agentforce, ServiceNow Now Assist, SAP Joule, Microsoft Copilot — each demanding consistent in-product AI chrome.
- **Regulatory disclosure requirements crystallised**: the EU AI Act Article 50 chatbot and synthetic-content obligations enter full applicability 2 August 2026 (source: https://artificialintelligenceact.eu/article/50/, fetched 2026-05-20), and a wave of US state laws — Utah's Artificial Intelligence Policy Act, California AB 2013, AB 2355, AB 3030 and SB 942, Colorado SB 24-205 — pushed disclosure from optional to required for specific surfaces (source: https://www.ncsl.org/technology-and-communication/artificial-intelligence-2024-legislation, fetched 2026-05-20).

The publisher posture spectrum that emerges from inspection runs across five rungs:

1. **Production-grade pattern publishers** with explicit AI sections, multiple components, principles documentation. Cloudscape, Atlassian, Twilio Paste.
2. **Single-component-plus-principles** ships. Carbon Design System (the AI Label component sits in the published library; richer chat patterns are isolated to Carbon Labs).
3. **Incubation labs** — explicit AI-pattern research alongside a more conservative published library. Carbon Labs.
4. **Principles-only** (prose without component-level expression). Atlassian's "AI interaction guidelines" sit alongside their Rovo pattern set, but for some publishers principles are *all* that is published.
5. **No published AI content despite list claims.** HeroUI, Mantine (component side), MUI, daisyUI (general chat-bubble only), Tailwind, Power Playbook, NY State, Lightning, MIND, SAP, ServiceNow, Elisa, Primer, Fluent UI, shadcn/ui core. Some of these may publish externally (Microsoft via `@fluentui-copilot/*` npm packages; Salesforce via Agentforce product docs) but not on the design-system surface itself.

This survey treats the (b) ship-to-consumers axis as authoritative. A system that publishes an MCP server but no chat affordance is a developer-tools publisher, not an AI-pattern publisher.

---

## 2. Landscape survey — the eighteen plus extensions, grouped by maturity tier

### 2.1 Production-grade

**Amazon Cloudscape — `/gen-ai/`** (source: https://cloudscape.design/gen-ai/, fetched 2026-05-20). The most complete AI section on a public design-system site. Six purpose-built generative-AI components (Avatar, Chat bubble, Loading bar, Prompt input, Support prompt group, Button group), fifteen patterns (Generative AI chat, Pattern abstraction, Ingress, Generative AI output label, Generative AI loading states, Progressive steps, Follow-up questions, User authorized actions, Variables, Shortcut menus, Response regeneration, Artifact previews, Conversational history, Support prompts, Thinking), three foundation pages (Visual affordance, Colors, Iconography), six principles (use-case evaluation, reliability, security/privacy, user control, transparency/error communication, bias/feedback). LLMs.txt files are also published as an AI tool. Several of the deeper detail URLs returned 404 on direct fetch but the index pages enumerate what is shipped.

**Atlassian Design System — Rovo and AI patterns** (source: https://atlassian.design/, fetched 2026-05-20; https://atlassian.design/patterns, fetched 2026-05-20; https://atlassian.design/patterns/rovo-ai, fetched 2026-05-20; https://atlassian.design/patterns/ai-interaction-guidelines, fetched 2026-05-20). Atlassian organises AI work under two top-level patterns — "AI interaction guidelines" (eight principles) and "Rovo and AI" (a pattern catalogue). The Rovo set is unusually expansive: hexagonal Rovo logo, sparkle-augmented AI icons, AI telepointers (always black/white to differentiate from human collaborators), AI-generation borders with the standardised disclaimer "Uses AI. Verify results.", Rovo button and nudges, Ask Rovo and prompt-starter cues, slash-prefixed Skills tags, an inline floating prompt input, and three explicit chat layouts — full-page (AI create), sidebar, and floating chat — each with chat-message-card primitives. The eight principles ("make workflows proactive," "keep the flow state," "content and form are dynamic," "make it easy to 'pop the hood'," "promote collective intelligence," "expand to multi-player and multi-intelligence," "weave a bit of Atlassian into the experience," "always accelerate responsibly") frame disclosure under "pop the hood" and accountability under "accelerate responsibly." The note that "more patterns are developing" is itself revealing — the system is shipping deliberately.

**Twilio Paste — Artificial Intelligence experience** (source: https://paste.twilio.design/, fetched 2026-05-20; https://paste.twilio.design/components/ai-chat-log, fetched 2026-05-20; https://paste.twilio.design/experiences/artificial-intelligence, fetched 2026-05-20). A top-level "Artificial Intelligence" experience guide, three chat components — `AIChatLog` (with `role="log"` for assistive announcement), `ChatLog` for human-to-human, `ChatComposer` for input. The AI Chat Log decomposes into `AIChatMessage`, `AIChatMessageAuthor`, `AIChatMessageBody` (with optional `animated` prop for typewriter streaming), `AIChatMessageActionGroup` and `AIChatMessageActionCard`, `AIChatMessageLoading` (with explicit guidance that "no user input should be accepted" while loading) and a paired `useAIChatLogger` hook. Markdown rendering is delegated to `markdown-to-jsx`. Citation and refusal are not first-class sub-components — the guidance is to compose them from Callout, Anchor, Help Text. The experience guide cites three governing trust principles ("Transparent, Responsible, Accountable"), prescribes a `decorative20` Badge with the ArtificialIntelligenceIcon as the disclosure mark, and requires a Privacy Impact Assessment before AI shipping. A working chatbot ("Paste Assistant") demonstrates the assembly.

### 2.2 Emerging — single-component or partial coverage

**Carbon Design System (main library) — AI Label / AI Presence**. The main Carbon site appears to publish an AI Label component (formerly known as Slug) but the inspection paths returned 404 across `/components/AI-label/usage`, `/components/AI-presence/usage` and `/all-about-ai/`. The signal that AI Label is shipped comes from the Carbon Labs README's positioning of `@carbon-labs/ai-tag` as the labs counterpart. Negative finding: I could not directly load a Carbon AI Label spec page on 2026-05-20.

**daisyUI — Chat bubble** (source: https://daisyui.com/, fetched 2026-05-20; https://daisyui.com/components/chat/, fetched 2026-05-20). One generic `chat-bubble` component with `chat-start`/`chat-end` placement, `chat-image`, `chat-header`, `chat-footer` and eight semantic colour variants. Pattern-level only — no AI-specific affordance for streaming, citation, refusal, feedback. Useful for chat *layout*, not for AI semantics.

**Carbon Labs — `@carbon-labs/ai-chat`** (source: https://github.com/carbon-design-system/carbon-labs, fetched 2026-05-20). The chat web component decomposes into 24 sub-component folders: `cardElement`, `carouselElement`, `chartElement`, `chat` (container), `codeElement`, `diagramElement`, `editableTextElement`, `errorElement`, `fileUploadElement`, `footer`, `formulaElement`, `header`, `historyViewer`, `imageElement`, `linkListElement`, `listElement`, `loadingElement`, `message`, `messages`, `molecularElement`, `popupElement`, `tableElement`, `tagListElement`, `textElement`. The breadth of element types — molecule renderer, formula, diagram, chart — is unusual; this is built for IBM scientific/enterprise content. A second labs package, `@carbon-labs/ai-tag`, ships an AI-content tag. Status: the repo positions itself as "a community-driven incubation space," sits at v0.13.x, and does not label individual packages alpha/beta/stable; treat as pre-1.0 incubation.

### 2.3 Extensions surfaced (not on the original list)

**Vercel AI SDK + AI Elements — `npx ai-elements`** (source: https://ai-sdk.dev/, fetched 2026-05-20; https://ai-sdk.dev/docs/ai-sdk-ui/overview, fetched 2026-05-20; https://elements.ai-sdk.dev/overview, fetched 2026-05-20). Despite not being a "design system" in the conventional sense, AI Elements is functionally the most comprehensive open AI pattern library on inspection in 2026. Five pillars:

- **Chatbot pillar** — Attachments, Chain of Thought, Checkpoint, Confirmation, Context, Conversation, Inline Citation, Message, Model Selector, Plan, Prompt Input, Queue, Reasoning, Shimmer, Sources, Suggestion, Task, Tool.
- **Code pillar** — Agent, Artifact, Code Block, Commit, Environment Variables, File Tree, JSX Preview, Package Info, Sandbox, Schema Display, Snippet, Stack Trace, Terminal, Test Results, Web Preview.
- **Voice pillar** — Audio Player, Mic Selector, Persona, Speech Input, Transcription, Voice Selector.
- **Workflow pillar** — Canvas, Connection, Controls, Edge, Node, Panel, Toolbar.
- **Utilities** — Image, Open In Chat.

Built on shadcn/ui — which itself ships zero AI primitives in core (source: https://ui.shadcn.com/docs/components, fetched 2026-05-20) — AI Elements effectively *is* the shadcn AI extension. The hooks layer (`useChat`, `useCompletion`, `useObject`) is framework-agnostic across React, Vue, Svelte, Angular, Solid (source: https://ai-sdk.dev/docs/ai-sdk-ui/overview, fetched 2026-05-20).

**Microsoft `@fluentui-copilot/react`** — referenced by Microsoft's Fluent UI React v9 ecosystem but the package itself returned 403 / 404 on direct inspection. The main Fluent UI surface (https://developer.microsoft.com/en-us/fluentui#/, fetched 2026-05-20) does not surface AI content in its main navigation. Documenting this as: published as code, not surfaced on the DS site. The `microsoft/fluentui` repo includes `.agents/skills`, `.claude/skills` and `AGENTS.md` files — these are agent-onboarding artefacts for contributors, not consumer-facing AI patterns (source: https://github.com/microsoft/fluentui, fetched 2026-05-20).

### 2.4 Experimental / labs-only

**Carbon Labs** as a whole — see above. The packages exist on npm and Storybook but do not appear in the main carbondesignsystem.com navigation, so they sit one tier below the published library by Carbon's own internal taxonomy.

### 2.5 Principles-only

**Atlassian's AI interaction guidelines** sit alongside the Rovo components and are therefore part of a production-grade ship. The interesting principles-only candidates would be sources that publish prose without components — none of the eighteen on the list does so cleanly; either both layers are present (Cloudscape, Atlassian, Paste) or neither is.

### 2.6 Not actually publishing AI patterns (negative findings)

Confirmed by direct inspection on 2026-05-20:

- **shadcn/ui** — no AI components in the core registry; community registry may contain some (source: https://ui.shadcn.com/docs/components, fetched 2026-05-20).
- **HeroUI** — homepage references "chat" as a *demo category* but no AI primitives in the component library on inspection (source: https://heroui.com/, fetched 2026-05-20).
- **Mantine** — operator-side AI tooling (MCP, llms.txt, skills); no consumer-side AI components (source: https://mantine.dev/, fetched 2026-05-20).
- **MUI** — homepage and component lists contain no AI primitives (source: https://mui.com/, fetched 2026-05-20).
- **Fluent UI** — main DS surface does not expose AI patterns; AI work is in adjacent npm packages (source: https://developer.microsoft.com/en-us/fluentui#/, fetched 2026-05-20).
- **Tailwind / Tailwind Plus** — no AI components surfaced on the homepage or marketing; AI companies are sponsors, not pattern outputs (source: https://tailwindcss.com/, fetched 2026-05-20).
- **Primer** — no public AI section; one internal `CopilotAnimation` exists but is not part of the public component catalogue (source: https://primer.style/components, fetched 2026-05-20). GitHub has shipped AI UI in product (Copilot Chat) but Primer does not surface those patterns publicly.
- **eBay MIND Patterns** — *despite the LinkedIn post claim*, MIND is an accessibility pattern library (Messaging, Input, Navigation, Disclosure, the source of the acronym). The "Messaging" section covers Alert Dialog, Toast Dialog, Inline Notice, Tourtip, etc. — not AI/chat (source: https://ebay.gitbook.io/mindpatterns, fetched 2026-05-20; https://ebay.gitbook.io/mindpatterns/messaging, fetched 2026-05-20). This is a meaningful negative finding given the post positioned MIND as the AI pattern library.
- **Power Apps Playbook** — the URL on the list (`playbook.powerapp.cloud/`) belongs to **Power**, an unrelated open-source design system (powerhome/playbook). It publishes 200+ general components, none AI-specific (source: https://playbook.powerapp.cloud/, fetched 2026-05-20). The list URL appears mis-attributed.
- **Power / Microsoft Copilot Studio** — design guidance pages returned 404 on inspection.

Inaccessible (could not verify content; treat as unverified, not negative):

- **Lightning Design System 2** — the deep-link URL is a Zeroheight-hosted SPA; WebFetch consistently returned only the page title across multiple sub-paths. Cannot confirm or deny AI-pattern publishing on the SLDS 2 surface (sources: https://www.lightningdesignsystem.com/2e1ef8501/p/85bd85-lightning-design-system-2, fetched 2026-05-20, plus four sub-paths). Salesforce's Agentforce product docs sit on help.salesforce.com but are not part of the design system surface.
- **Elisa Design System** — also Zeroheight-hosted; the deep-linked URL and four sub-paths returned only the title. Cannot verify AI patterns (source: https://designsystem.elisa.fi/9b207b2c3/p/155e65-elisa-design-system, fetched 2026-05-20, plus four sub-paths).
- **ServiceNow Horizon** — homepage returned 403 on direct fetch (source: https://horizon.servicenow.com/, fetched 2026-05-20). Could not access. Now Assist patterns may exist but are not visible to anonymous fetch.
- **SAP design system** — `sap.com/design-system` returned 403. Legacy `experience.sap.com/fiori-design-web/conversational-ai/` redirects to the same 403 surface. Cannot verify Joule pattern publishing on inspection (source: https://www.sap.com/design-system/, fetched 2026-05-20).
- **NY State Design System** — accessible, but no AI patterns on the homepage or in the change log. The system focuses on tokens, web components, accessibility, Figma libraries (source: https://designsystem.ny.gov/, fetched 2026-05-20). Treat as a public-sector outlier with deliberate non-coverage as of 2026-05-20.

### 2.7 Public-sector outlier — New York State

NYS sits under a different governance regime than the SaaS systems — Section 508 / ADA legal exposure, FOIL / open-records obligations on AI-assisted decisions, the wave of state AI disclosure laws beginning to land in 2024–2026. The fact that NYS publishes no AI patterns on its DS surface in May 2026 is itself a finding: public-sector design systems are running behind their private-sector counterparts on AI pattern coverage at a moment when public-sector AI deployments are increasingly subject to disclosure regulation. The likely path forward is a separate AI guidance layer (under the agency CIO / Chief Information Security Officer) coordinating with the DS, not the DS owning AI guidance directly.

---

## 3. The pattern taxonomy — clusters that emerge from the source material

The brief's six initial clusters survive inspection with two refinements: a new **Tool-call and agent affordance** cluster (separable from generic conversation primitives because it has its own state machine and is most developed in AI Elements and Cursor); and a **Citation and source attribution** cluster broken out from "Trust, transparency, attribution" because the published implementations now diverge sharply on inline-vs-trailing rendering.

### 3.1 Prompt input

**Anatomy at minimum**: a multiline auto-resizing textarea, a submit affordance whose icon reflects status (idle, streaming, error), a model/context selector, an attachment surface, and an action menu for non-default invocations (screenshot, file, voice).

**Convergence**: every production publisher ships a dedicated Prompt Input distinct from the generic Textarea. Cloudscape's `Prompt input` (source: https://cloudscape.design/components/, fetched 2026-05-20), Twilio Paste's `ChatComposer` (source: https://paste.twilio.design/components/ai-chat-log, fetched 2026-05-20), AI Elements `<PromptInput>` (source: https://elements.ai-sdk.dev/components/prompt-input, fetched 2026-05-20), Atlassian's "Prompt inline" with floating arrow submit and microphone button. Auto-resize is universal. Enter-submits / Shift+Enter-newlines is universal.

**Divergence**: rich auxiliary affordances are still inconsistent. AI Elements ships the densest assembly — `PromptInputActionAddAttachments`, `PromptInputActionAddScreenshot`, `PromptInputSelect` model picker, `PromptInputCommand` (slash-command surface), Tabs, HoverCard, native Web Speech API mic. Cloudscape and Atlassian implement subsets. Carbon Labs' `chat/footer` is the input host but the README is sparse on its features. Slash-command surfaces are *named differently across systems* — Atlassian's "Skills tags" (slash-prefixed lozenges), AI Elements' `PromptInputCommand`, Cloudscape's "Shortcut menus." These are the same primitive named three ways.

### 3.2 Generative response rendering

**Anatomy at minimum**: a typed message wrapper that distinguishes user from assistant, a streaming-aware text renderer, a code-block primitive with copy/run, a way to render structured non-text content (tables, charts, images, files).

**Convergence**: assistant/user differentiation by alignment and surface colour is universal (daisyUI's `chat-start`/`chat-end`, AI Elements `Message from="user"|"assistant"`, Paste's `AIChatMessageAuthor`). Streaming via typewriter / shimmer / progressive markdown is universal. Code-block-with-copy is universal.

**Divergence**: how *much* structured content the message can hold. Carbon Labs `ai-chat` decomposes into 24 element types including chart, diagram, formula, molecular, table, image, carousel — a one-message-many-elements model. AI Elements treats most of these as siblings inside the conversation rather than nested in the message. Cloudscape's "Artifact previews" pattern is the closest analogue to AI Elements' Code/Sandbox/WebPreview pillar but ships less framework-level support.

A subtle but important divergence: **branched/regenerated alternatives**. AI Elements ships `MessageBranch` / `MessageBranchSelector` / `MessageBranchPrevious` / `MessageBranchNext` / `MessageBranchPage` as a first-class pattern (source: https://elements.ai-sdk.dev/components/message, fetched 2026-05-20). Cloudscape names "Response regeneration" as a pattern but does not appear to publish a branch-traversal component. Paste does not ship branching. Branching is the *convergence target* and the *current divergence point* simultaneously.

### 3.3 Trust, transparency, attribution (subdivided)

**3.3.a AI disclosure / labelling.** Cloudscape ships a "Generative AI output label" pattern (source: https://cloudscape.design/gen-ai/, fetched 2026-05-20). Twilio Paste prescribes a `decorative20` Badge with the ArtificialIntelligenceIcon (source: https://paste.twilio.design/experiences/artificial-intelligence, fetched 2026-05-20). Carbon ships an AI Label / AI Tag pair (`@carbon-labs/ai-tag`). Atlassian uses a colourful generation border plus the standardised disclaimer "Uses AI. Verify results." (source: https://atlassian.design/patterns/rovo-ai, fetched 2026-05-20). This is the pattern with the widest cross-publisher coverage — and the widest *visual divergence*. There is no design-system-level convergence on what an "AI badge" looks like.

**3.3.b Citation / source attribution.** AI Elements is alone in publishing a fully decomposed citation primitive — `<InlineCitation>` with `Trigger`, `CardBody`, `Carousel`, `Source`, `Quote` — that renders an inline pill with a hover card, hostname-and-count display, and a carousel for multi-source citations (source: https://elements.ai-sdk.dev/components/inline-citation, fetched 2026-05-20). It also ships a separate `<Sources>` collapsible-list pattern for trailing attribution (source: https://elements.ai-sdk.dev/components/sources, fetched 2026-05-20). Twilio Paste documents that citations should be composed from Callout/Anchor/Help Text — i.e. no first-class primitive. Cloudscape's pattern catalogue does not name citations explicitly. The field has not converged here, and inline-vs-trailing is the strategic divergence: inline citations imply the LLM is grounded with a span-aligned retrieval signal; trailing citations only require a list of URLs at message end. The choice cascades back into the model-side architecture.

**3.3.c Refusal.** No publisher ships a first-class refusal component. Paste documents error states (Callout in body, Help Text on actions, Alert above composer for system errors) but explicitly does not call any of them "refusal." Atlassian's principles touch refusal indirectly via "always accelerate responsibly" without prescribing UI. Cloudscape's pattern list does not name refusal. This is the largest published-pattern gap relative to what frontier products (ChatGPT, Claude) actually ship — both major vendors have refined refusal UIs that no DS has yet codified.

### 3.4 Feedback and correction

**Convergence**: every production system ships a message-level action group for thumbs / copy / regenerate. AI Elements `<MessageActions>` / `<MessageAction>` (source: https://elements.ai-sdk.dev/components/message, fetched 2026-05-20). Paste `AIChatMessageActionGroup` / `AIChatMessageActionCard`. Cloudscape's `Button group` is documented as the message-action carrier. Atlassian has feedback affordances inside chat-message cards.

**Divergence**: structured feedback for evaluation. None of the inspected systems publish a "structured feedback for evals" pattern — i.e. a UI that captures the *reason* for a thumbs-down in a way that flows to an evaluation harness. Cloudscape's principles mention "feedback loops" for bias mitigation but this is not surfaced as a component. This is a clean publisher gap: the eval contract that distinguishes a usable AI feature from a demo (see §5.2) has no published UI.

### 3.5 Conversation primitives

**Anatomy at minimum**: a message container with auto-scroll, an empty state, message-thread continuity, a way to anchor the prompt input to the bottom of a scrolling region.

**Convergence**: auto-scroll-to-bottom with a "scroll to latest" button is universal. AI Elements `<Conversation>` with `ConversationContent`, `ConversationEmptyState`, `ConversationScrollButton`, `ConversationDownload` (and a `messagesToMarkdown` exporter) is the most decomposed implementation (source: https://elements.ai-sdk.dev/components/conversation, fetched 2026-05-20). Paste's `useAIChatLogger` hook with push/pop/clear is the equivalent state model.

**Divergence**: chat *layout* primitives. Atlassian explicitly ships three layouts as first-class patterns — full-page (AI create), sidebar, floating — each with different positioning rules (source: https://atlassian.design/patterns/rovo-ai, fetched 2026-05-20). Cloudscape leaves layout to the consumer. Paste publishes a single composer pattern. Carbon Labs is single-layout. The Atlassian three-layout taxonomy is the strongest cross-context layout vocabulary in the field and the convergence candidate worth watching.

### 3.6 Tool-call and agent affordance (new cluster, broken out from §3.5)

**Anatomy at minimum**: tool-call rendering with state (pending, running, completed, errored, denied, approval-requested), input/output formatted display, an approval workflow when the tool is privileged.

This is the cluster where AI Elements moves furthest ahead of every named DS publisher. `<Tool>` decomposes into `ToolHeader`, `ToolContent`, `ToolInput`, `ToolOutput`, with seven defined states — `input-streaming`, `input-available`, `approval-requested`, `approval-responded`, `output-available`, `output-error`, `output-denied` — and a paired `<Confirmation>` component for the approval workflow (`ConfirmationRequest`, `ConfirmationAccepted`, `ConfirmationRejected`, `ConfirmationActions`) (source: https://elements.ai-sdk.dev/components/tool, fetched 2026-05-20; https://elements.ai-sdk.dev/components/confirmation, fetched 2026-05-20). `<Plan>` and `<ChainOfThought>` handle the reasoning trace; `<Reasoning>` handles single-block reasoning streams (source: https://elements.ai-sdk.dev/components/reasoning, fetched 2026-05-20; https://elements.ai-sdk.dev/components/chain-of-thought, fetched 2026-05-20). Cloudscape names "Thinking," "Progressive steps," "User authorized actions" as patterns but does not publish equivalent component decomposition. Atlassian leaves tool-call UX to product implementations. This is a 12-month-ahead gap.

### 3.7 Governance / principles

**Convergence**: every production publisher ships an AI principles document. Cloudscape's six principles, Atlassian's eight, Paste's three (Transparent, Responsible, Accountable) plus seven base design principles. The principles overlap considerably — transparency, control, error handling, accountability appear in all three — but the specificity of *attached* governance differs: Paste prescribes a Privacy Impact Assessment; Atlassian prescribes the standardised disclaimer string "Uses AI. Verify results."; Cloudscape attaches the principles to specific patterns. Where principles are attached to enforceable artefacts (a required disclaimer string, a required PIA, a CI lint), they bite. Where they are prose only, they are decorative.

---

## 4. Tooling and implementation reality

### 4.1 What the OSS layer ships

**Vercel AI SDK + AI Elements** — the de facto open AI UI primitive layer in 2026. Hooks (`useChat`, `useCompletion`, `useObject`) are framework-agnostic across React, Vue, Svelte, Angular, Solid (source: https://ai-sdk.dev/docs/ai-sdk-ui/overview, fetched 2026-05-20). AI Elements components are installed via `npx ai-elements` and are shadcn-compatible (source: https://ai-sdk.dev/, fetched 2026-05-20). Coverage spans chat, code, voice, workflow.

**shadcn/ui core** ships zero AI components (source: https://ui.shadcn.com/docs/components, fetched 2026-05-20). The community registry path means "shadcn/ui has chat components" can be true (via AI Elements installed *as* a shadcn registry) and false (in core) at the same time — a common source of scoping confusion.

**Carbon Labs** — `@carbon-labs/ai-chat` (web component) with the rich element decomposition above; pre-1.0 incubation status. Distribution per-package on npm.

**Twilio Paste** — `AIChatLog` and dependents in the published Paste React library; `useAIChatLogger` hook for state.

**Cloudscape** — six GenAI-category components in the `@cloudscape-design/components` package. Stable.

**Atlassian** — Rovo components are shipped via internal Figma library and product implementation; the public DS surface documents patterns rather than exposing the components as installable npm packages outside Atlassian product.

**Microsoft `@fluentui-copilot/*`** — published as code; not surfaced on the Fluent UI DS site. Treat as an adjacency rather than a DS deliverable.

### 4.2 Where bespoke work begins

Three durable seams where the OSS layer ends:

- **Multi-modal input beyond attachments**. Voice input is in AI Elements' Voice pillar (Speech Input, Mic Selector, Persona) and Atlassian's microphone button, but neither expects to handle live transcription, diarisation, or interruption semantics — those remain bespoke.
- **Citation correctness, not just citation rendering**. AI Elements renders an `<InlineCitation>`. Whether the citation actually points to a span the model used is an evaluation problem owned outside the DS. The pattern can be present and broken simultaneously (see §6).
- **Refusal as a product surface.** No published primitive. Refusal copy, refusal categories, refusal-to-recovery handoffs are bespoke product work.
- **Evaluation-instrumented feedback.** Every system ships thumbs/regenerate. None ships a flow that connects the thumbs-down to a structured eval log (rubric tag, severity, follow-up question to the user).

### 4.3 Figma–to–code round-trip

The publishers that ship both Figma kits and code primitives — Paste, Cloudscape, Atlassian (internal-only) — surface AI components in both. Carbon Labs' Figma kit appears separately on the Figma Community but I could not load it on inspection. AI Elements ships React-only with no Figma counterpart, which means anyone using AI Elements in a non-trivial product needs a separate Figma kit; this is a known gap and a place engagements quietly sink time.

### 4.4 MCP and AI-readable patterns (the meta-recursion)

Mantine ships an MCP server that exposes its component metadata to AI agents (source: https://mantine.dev/, fetched 2026-05-20). Cloudscape publishes LLMs.txt files as part of its GenAI section. shadcn-style registries are increasingly fetched by codegen agents. The pattern *that AI patterns are themselves AI-readable* is real but mostly applies to the (a) operator-side: making components-as-data so a coding agent can produce conformant assemblies. Where this becomes load-bearing for (b) ship-to-consumers patterns is when the consumer-side AI surface composes itself dynamically — the AI SDK's "Generative UI" idea — and that composition needs to draw from the DS without a human in the loop. AI Elements' tight coupling to the `UIMessage` type and ToolUIPart shape is the visible artefact of this: the pattern primitives are designed for an AI to assemble.

---

## 5. Architecture and governance

### 5.1 The four-prerequisite minimum

The prerequisite list — components-as-data, structured metadata, evaluation contracts, content/safety governance — holds up against the published material. Where it bites:

- **Components-as-data** is implicit in AI Elements' design (the components consume `UIMessage` directly) and in Cloudscape's six explicit GenAI components. Carbon Labs' web-component approach is consistent with this. Paste's components consume hook state. None of the systems lacking AI primitives have a pathway to ship them without first making the rest of their library data-shaped.
- **Structured metadata** is where Carbon Labs' element decomposition (chart, diagram, table, formula, molecular) is interesting: those are typed message parts, not free text. Pattern publishing without typed message parts collapses to "we shipped a div with Markdown."
- **Evaluation contracts** are absent from every published library. This is the biggest gap.
- **Content / safety governance** is partially addressed by Twilio Paste's PIA requirement and Atlassian's "verify results" disclaimer; entirely absent elsewhere.

### 5.2 The eval loop

A published refusal pattern is *correct* only if the underlying classifier-or-router is reliably triggering it; a published citation pattern is *correct* only if the citation resolves to the source the model used. None of the inspected DSs publish CI hooks for either. Cloudscape comes closest by naming "evaluating use cases" as principle one but does not connect it to component CI.

The closest published implementation of an eval-aware UI primitive is AI Elements' `<Tool>` state machine with `output-error` and `output-denied` as first-class states — these correspond to evaluatable outcomes (denial reasons, error categories) and are wired into the SDK's tool-result types. This is the architectural pattern other systems will need to copy.

### 5.3 The content-governance seam

Every chat pattern presumes a content layer the DS does not own — sources for retrieval, allowed tool surfaces, system prompt content, safety filters. Twilio Paste explicitly documents the seam by requiring a Privacy Impact Assessment and partnership with Legal (source: https://paste.twilio.design/experiences/artificial-intelligence, fetched 2026-05-20). Atlassian's principles point at the seam ("permissions" appear under "promote collective intelligence") without naming an artefact. The DS contract ends where the corpus begins; engagements should treat that handoff as a named scope boundary.

### 5.4 Disclosure regimes

- **Voluntary industry pattern**: AI badges (Cloudscape's output label, Paste's `decorative20` Badge, Atlassian's generation border, Carbon AI Tag). No cross-system convergence on visual.
- **EU AI Act Article 50** (full applicability 2 August 2026): synthetic content must be "marked in a machine-readable format and detectable as artificially generated or manipulated"; chatbot interactions must be disclosed; deepfakes must be disclosed by deployers; AI-generated text on matters of public interest must disclose origin unless human-edited under editorial responsibility (source: https://artificialintelligenceact.eu/article/50/, fetched 2026-05-20). The "machine-readable" requirement is the bit DS publishers have not yet operationalised — current AI badges are visual disclosure to humans, not machine-readable provenance.
- **US state laws (2024–2026)**: California SB 942 (the California AI Transparency Act) mandates a free AI-detection tool plus a "latent disclosure" of provenance for covered providers; AB 2355 mandates political-ad disclosure; AB 3030 mandates patient-communication disclaimers; Colorado SB 24-205 covers high-risk-system disclosures; Utah's Artificial Intelligence Policy Act establishes baseline disclosure obligations (source: https://www.ncsl.org/technology-and-communication/artificial-intelligence-2024-legislation, fetched 2026-05-20).
- **Public-sector**: Section 508 / WCAG conformance and FOIL / open-records exposure when AI is used in decisions affecting the public sit on top of the federal/state framework. NYS does not publish AI patterns yet, which means each agency is currently inventing.

The verification path: regulatory state changes faster than design-system documentation. For any client engagement, the citable artefacts are the regulator's published text (eur-lex for EU; state code citations for US) — not the DS principles document.

---

## 6. Failure modes

**Assumed maturity.** A client will read "Carbon ships AI components" and conflate a stable AI Label badge with the Carbon Labs incubation chat. The labs/main distinction is meaningful and gets dropped in scoping conversations.

**Component-level shipping without governance / eval.** Most named systems are here. The visible UI works, the back-end behaviour is undefined. A `<MessageActions>` thumbs-up button with no eval pipeline is the canonical instance.

**Design-led patterns without engineering buy-in on safety / eval.** The Atlassian principles ship as design direction; whether engineering ships the corresponding evaluation harness is a separate question. The principles document is high-leverage only if engineering is contractually bound to it.

**Disclosure theatre.** A `decorative20` Badge that satisfies the UI checklist without changing user understanding. The EU AI Act's machine-readable provenance requirement raises the bar — a visual badge alone does not satisfy Article 50(2) for synthetic content.

**Streaming-as-novelty.** AI Elements' `MessageResponse` and Paste's `animated` typewriter prop both render incrementally. Whether the streamed content is faster than a structured non-streaming JSON response is a backend question; novelty cost is real (typewriters delay information), and the DS-level pattern does not litigate the choice.

**Citation patterns without verification.** AI Elements' `<InlineCitation>` renders pills with sources — but if the model invented the source, the pattern surfaces fabrication confidently. The published primitive is a UI; the verification is missing.

**Inconsistent refusals.** Without a refusal primitive, the same product surface ships three different refusal copies depending on which engineer wrote the path. Every system inspected has this problem.

**One-off agent UIs that diverge from the rest of the DS.** The risk Atlassian explicitly addresses by anchoring AI experiences to the brand thread ("weave a bit of Atlassian") and by using Rovo as a unifier; the risk other publishers are likely to hit when an AI feature ships under a different brand than the DS.

---

## 7. Open questions and contested territory

**Inline vs trailing citations.** No convergence. AI Elements ships both; most DS publishers ship neither as a first-class primitive. The choice is upstream of UI — it constrains the retrieval architecture.

**Refusal as a published primitive.** Frontier products have refined refusal patterns (graceful explanation, alternative offer, escape hatch). No DS in this survey publishes one. This is the largest open gap.

**Branched/regenerated alternatives.** AI Elements ships them; most don't. The product question is whether end users want branching or whether it confuses the conversation model. Cursor does not surface branches; ChatGPT does. The DS field will follow the frontier-product convergence.

**Standardised AI badge.** No cross-system visual convergence. The EU AI Act's machine-readable provenance requirement may force convergence on a *technical* spec (e.g. C2PA-style content credentials) before the visual converges.

**Feedback-to-eval flow.** A thumbs-down primitive that captures rubric and severity and writes to an eval log. Nobody publishes one.

**Multi-agent / agent handoff.** Atlassian's principle "expand to multi-player and multi-intelligence" is the only published pointer. The pattern is not yet shipped.

**Voice-first chat surfaces.** AI Elements has a voice pillar; no other inspected DS does. Atlassian has an audio telepointer for Rovo. Whether voice belongs in the chat surface or is a separate input mode is unsettled.

**Where DS patterns lag frontier products.** Cursor's plan-then-act flow (plan mode, parallel agents, Slack/CLI integrations), Claude's artifact rendering, ChatGPT's branched conversations and the "edit message" flow — these are 12–18 months ahead of every DS-level published pattern (source: https://www.cursor.com/, fetched 2026-05-20). The implication for adoption strategy: do not promise clients that their AI feature will look like ChatGPT-current using DS-published primitives. Either build bespoke ahead of the DS, or accept the lag.

**Where governance is moving faster than the library.** Article 50 enters full applicability 2 August 2026. State laws are accumulating monthly. The published DS surface is months-to-years behind the regulatory clock. Any engagement scoped today against a DS that does not publish AI patterns is on the hook for the disclosure layer itself.

---

## References

Production-grade publishers:
- Cloudscape Gen AI hub: https://cloudscape.design/gen-ai/
- Cloudscape Components index: https://cloudscape.design/components/
- Atlassian DS homepage: https://atlassian.design/
- Atlassian Patterns index: https://atlassian.design/patterns
- Atlassian Rovo and AI: https://atlassian.design/patterns/rovo-ai
- Atlassian AI interaction guidelines: https://atlassian.design/patterns/ai-interaction-guidelines
- Twilio Paste homepage: https://paste.twilio.design/
- Twilio Paste AI Chat Log: https://paste.twilio.design/components/ai-chat-log
- Twilio Paste Artificial Intelligence experience: https://paste.twilio.design/experiences/artificial-intelligence

Emerging / single-component:
- daisyUI Chat bubble: https://daisyui.com/components/chat/
- Carbon Labs repo: https://github.com/carbon-design-system/carbon-labs
- Carbon Labs ai-chat element index: https://github.com/carbon-design-system/carbon-labs/tree/main/packages/web-components/src/components/chat/components

Extensions surfaced:
- Vercel AI SDK: https://ai-sdk.dev/
- AI SDK UI overview: https://ai-sdk.dev/docs/ai-sdk-ui/overview
- AI Elements overview: https://elements.ai-sdk.dev/overview
- AI Elements Conversation: https://elements.ai-sdk.dev/components/conversation
- AI Elements Message: https://elements.ai-sdk.dev/components/message
- AI Elements Prompt Input: https://elements.ai-sdk.dev/components/prompt-input
- AI Elements Inline Citation: https://elements.ai-sdk.dev/components/inline-citation
- AI Elements Sources: https://elements.ai-sdk.dev/components/sources
- AI Elements Reasoning: https://elements.ai-sdk.dev/components/reasoning
- AI Elements Chain of Thought: https://elements.ai-sdk.dev/components/chain-of-thought
- AI Elements Tool: https://elements.ai-sdk.dev/components/tool
- AI Elements Confirmation: https://elements.ai-sdk.dev/components/confirmation
- AI Elements Plan: https://elements.ai-sdk.dev/components/plan
- AI Elements Suggestion: https://elements.ai-sdk.dev/components/suggestion
- AI Elements Checkpoint: https://elements.ai-sdk.dev/components/checkpoint
- Cursor product surface: https://www.cursor.com/

Negative or inaccessible:
- shadcn/ui components: https://ui.shadcn.com/docs/components
- HeroUI: https://heroui.com/
- Mantine: https://mantine.dev/
- MUI: https://mui.com/
- Fluent UI: https://developer.microsoft.com/en-us/fluentui#/
- microsoft/fluentui repo: https://github.com/microsoft/fluentui
- Tailwind CSS: https://tailwindcss.com/
- Primer components: https://primer.style/components
- eBay MIND: https://ebay.gitbook.io/mindpatterns
- eBay MIND messaging section: https://ebay.gitbook.io/mindpatterns/messaging
- Power Playbook: https://playbook.powerapp.cloud/
- NY State Design System: https://designsystem.ny.gov/
- Lightning DS 2 deep link: https://www.lightningdesignsystem.com/2e1ef8501/p/85bd85-lightning-design-system-2 (inaccessible to anonymous fetch)
- Elisa DS deep link: https://designsystem.elisa.fi/9b207b2c3/p/155e65-elisa-design-system (inaccessible to anonymous fetch)
- ServiceNow Horizon: https://horizon.servicenow.com/ (403)
- SAP design system: https://www.sap.com/design-system/ (403)
- Shopify Polaris: https://polaris-react.shopify.com/

Regulatory and governance:
- EU AI Act Article 50: https://artificialintelligenceact.eu/article/50/
- EU AI Act tier definitions: https://artificial-intelligence-act.com/
- NCSL state AI legislation 2024: https://www.ncsl.org/technology-and-communication/artificial-intelligence-2024-legislation

---

## Footer

**(a) Sources I couldn't access or that did not have AI patterns.** Inaccessible to anonymous WebFetch on 2026-05-20: Lightning Design System 2, Elisa Design System (both Zeroheight-hosted SPAs returning page-title only), ServiceNow Horizon (403), SAP design system (403). Accessed but no AI patterns published: shadcn/ui core, HeroUI, Mantine (consumer-side; AI tooling for agents is shipped), MUI, Fluent UI (AI work lives in adjacent npm packages, not on the DS surface), Tailwind, daisyUI (only a generic chat bubble), Primer (one internal CopilotAnimation; nothing public), eBay MIND (an accessibility pattern library — Messaging/Input/Navigation/Disclosure — not AI; this is the post's clearest overclaim), Power Playbook (the URL belongs to "Power" the agency DS, not Microsoft Power Apps Playbook; no AI), NY State Design System.

**(b) Taxonomy clusters reshaped.** Kept all six initial clusters. Added a seventh, "Tool-call and agent affordance," because the published material — overwhelmingly led by AI Elements but also visible in Cloudscape's "User authorized actions" and "Progressive steps" — has its own state machine, approval workflow primitive, and reasoning-trace components that don't fit cleanly inside generic conversation primitives. Also subdivided cluster 3 ("Trust, transparency, attribution") into 3.3.a Disclosure / labelling, 3.3.b Citation / source attribution, 3.3.c Refusal, because the field has converged on disclosure, diverged sharply on citation (inline-vs-trailing), and not converged at all on refusal.

**(c) Surprises.** Three. First, eBay MIND is not an AI pattern library; the LinkedIn list mis-attributed it. The MIND acronym refers to Messaging, Input, Navigation, Disclosure — accessibility patterns. Second, Vercel AI Elements (functionally an open AI pattern library shipped as a shadcn-compatible registry) is materially ahead of every named "design system" on the source list in component decomposition, especially for tool-call rendering, branched messages, citations, and reasoning traces. The strategic implication is that the OSS AI primitive layer leads the DS layer in 2026, inverting the usual relationship. Third, the largest *published-pattern gap* is refusal — frontier products like ChatGPT and Claude have spent two years refining refusal UX and no inspected DS publishes a refusal primitive. That is the open territory most exposed to regulatory and trust pressure.

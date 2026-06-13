---
type: practice-area
title: AI-Aware Patterns and Conversational UI
description: AI patterns the DS ships to consumers (chat, streaming, citation, refusal, tool-call). Field survey, production-grade triad (Cloudscape / Rovo / Paste), AI Elements as primitives, EU AI Act Article 50.
tags: [extension, ai, conversational-ui, patterns, governance]
timestamp: 2026-06-10
---

# 25 — AI-Aware Patterns and Conversational UI

> An "AI-aware" design system is two things at once. It is a system that is *operated on* by AI tools (the territory of 15-ai-in-ds — token critique, codegen, MCP-served metadata, AI-readable docs). It is also a system that *ships AI patterns to consumers* (chat input, streaming response, citation, refusal, conversation primitives, agent affordances). Confusing the two is the most common category error in scoping conversations. This file covers the second axis. The architecture that makes either work — components-as-data, structured metadata, evaluation contracts, content/safety governance — is shared, but the audiences, deliverables, and failure modes diverge sharply. Both axes belong inside the system. Neither subsumes the other.

---

## The (a)/(b) split is the load-bearing distinction

The split runs through every scoping conversation we have about AI in 2026, and most of the confusion in those conversations comes from collapsing the two axes:

- **(a) AI operates the system.** Tokens get audited by AI; documentation gets emitted in machine-readable form; coding agents call MCP servers to retrieve component metadata; designers reach for Figma Make to scaffold patterns from prompts. The system is the *target* of AI work. Mantine is the cleanest current example of this posture in isolation: it ships an MCP server (`@mantine/mcp-server`), `llms.txt` files, and "skills for AI agents," but ships zero consumer-facing AI components — no chat surface, no prompt input, no message primitives. (See 15-ai-in-ds for the depth on the (a) axis: components-as-data, MCP architecture, token critique, codegen, the four-prerequisite minimum.)

- **(b) The system ships AI patterns to consumers.** Chat input fields, streaming response containers, AI disclosure badges, inline citations, refusal states, tool-call rendering, multi-turn conversation primitives. The system is the *publisher* of AI work consumed by product teams who are themselves shipping AI features. Cloudscape, Atlassian Rovo, and Twilio Paste are the production-grade examples of this posture as of mid-2026.

The two axes share architectural prerequisites and diverge on audience, deliverable, and failure mode. A team that excels at (a) and ignores (b) ships an AI-readable design system that has nothing to say when a client asks "what should our Copilot look like?" A team that excels at (b) and ignores (a) ships a beautiful chat UI that no AI agent can correctly assemble against the rest of the design system. The mature posture is to ship both layers and treat them as a *single architecture, two surfaces*. (See 15-ai-in-ds for the (a) layer; the rest of this file is (b).)

A scoping signal: when a client says "we want AI features," they almost always mean (b). When they say "we want our design system to be AI-ready," they may mean (a), (b), or both — and rarely know the difference until it's surfaced. Surfacing it is the first thing to do in scoping.

There is a third axis adjacent to (a) and (b) that is increasingly worth distinguishing in the same conversation: **adaptive interfaces that *reshape themselves* in real time** around user, moment, and task — covered in 26-adaptive-interfaces-foundations and 27-adaptive-interfaces-implementation. The chat patterns documented in this file are one *posture* (in Clark & Kindred's vocabulary) of the adaptive-interface category; the bespoke-UI / intelligent-canvas / call-and-response surfaces in 26 and 27 are another. The shared substrate is components-as-data plus semantic intent metadata; the shared governance load is variant logging and outcome-based eval. When clients arrive asking for "AI features," the diagnostic question is not just (a) vs. (b) but also *which posture* — chat, agent, copilot, or bespoke surface — and *which adaptive-UI rung* (rule-based / catalog / template / structured-output / code-emit). 25 covers chat at depth; 26 covers the broader pattern set the chat surface sits inside; 27 covers the engineering reality of all of it.

---

## The state of the (b) field in 2026

Three forcing functions converged across 2024–2026 to push consumer-facing AI patterns into the mainstream. Conversational surfaces moved from experimental to first-class in flagship products (ChatGPT, Claude, Gemini, Copilot, Cursor) — enterprise design systems can no longer treat chat as a curiosity. Agent platforms shipped under existing brands — Atlassian Rovo, Salesforce Agentforce, ServiceNow Now Assist, SAP Joule, Microsoft Copilot — each demanding consistent in-product AI chrome. And regulatory disclosure requirements crystallised: the EU AI Act Article 50 chatbot and synthetic-content obligations enter full applicability **2 August 2026** (verify against the regulator's text — eur-lex / artificialintelligenceact.eu — before quoting in client work; the date and the article number are both worth re-confirming at the moment of citing), and a wave of US state laws — Utah's Artificial Intelligence Policy Act, California SB 942 (the AI Transparency Act), AB 2013, AB 2355, AB 3030, Colorado SB 24-205 — pushed disclosure from optional to required for specific surfaces.

These forcing functions are why the field looks the way it does in mid-2026: a small number of publishers shipping production-grade AI sections; a larger number with one or two AI-specific components in an otherwise general system; a third group with prose-only principles and no component-level expression; and — the surprise of the survey behind this file — a meaningfully large number of systems that have been *claimed* to publish AI patterns but on inspection do not. We will name names below. Field accuracy matters here because the wrong claim survives in scoping decks and turns into client expectations that the actual library cannot meet.

---

## Landscape — production-grade publishers

Three publishers stand out as having shipped genuine AI sections, with multiple components, principles documentation, and the seams to product engineering that suggest the patterns will survive contact with real work.

**Amazon Cloudscape** (`cloudscape.design/gen-ai/`). The most complete public AI section on a public design-system site. Six purpose-built generative-AI components — Avatar, Chat bubble, Loading bar, Prompt input, Support prompt group, Button group — and roughly fifteen named patterns: Generative AI chat, Pattern abstraction, Ingress, Generative AI output label, Generative AI loading states, Progressive steps, Follow-up questions, User authorized actions, Variables, Shortcut menus, Response regeneration, Artifact previews, Conversational history, Support prompts, and Thinking. Foundation pages cover Visual affordance, Colors, and Iconography. Six explicit principles (use-case evaluation, reliability, security/privacy, user control, transparency/error communication, bias/feedback). LLMs.txt files are also published as an AI tool. Cloudscape is the convergence target — when a publisher's AI section is described as "production-grade," what they generally mean is "structured like Cloudscape's."

**Atlassian Design System — Rovo and AI patterns** (`atlassian.design/patterns/rovo-ai`, `atlassian.design/patterns/ai-interaction-guidelines`). Atlassian organises AI work under two top-level patterns — eight AI interaction guidelines and a Rovo pattern catalogue. The Rovo set is unusually expansive: a hexagonal Rovo logo, sparkle-augmented AI icons, AI telepointers (always black/white to differentiate from human collaborators), AI-generation borders with the standardised disclaimer string `Uses AI. Verify results.`, Rovo button and nudges, Ask Rovo and prompt-starter cues, slash-prefixed Skills tags, an inline floating prompt input, and three explicit chat layouts — full-page (AI create), sidebar, and floating chat — each with chat-message-card primitives. The eight principles ("make workflows proactive," "keep the flow state," "content and form are dynamic," "make it easy to 'pop the hood'," "promote collective intelligence," "expand to multi-player and multi-intelligence," "weave a bit of Atlassian into the experience," "always accelerate responsibly") frame disclosure under "pop the hood" and accountability under "accelerate responsibly." The three-layout taxonomy (full-page / sidebar / floating) is the strongest cross-context layout vocabulary in the published field and is worth borrowing wholesale on engagements that need a layout grammar before they have any chat content.

**Twilio Paste — Artificial Intelligence experience** (`paste.twilio.design/experiences/artificial-intelligence`, `paste.twilio.design/components/ai-chat-log`). A top-level "Artificial Intelligence" experience guide, three chat components — `AIChatLog` (with `role="log"` for assistive announcement), `ChatLog` for human-to-human, `ChatComposer` for input. The AI Chat Log decomposes into `AIChatMessage`, `AIChatMessageAuthor`, `AIChatMessageBody` (with optional `animated` prop for typewriter streaming), `AIChatMessageActionGroup` and `AIChatMessageActionCard`, `AIChatMessageLoading` (with explicit guidance that "no user input should be accepted" while loading) and a paired `useAIChatLogger` hook. Markdown rendering is delegated to `markdown-to-jsx`. Citation and refusal are not first-class sub-components — the guidance is to compose them from Callout, Anchor, Help Text. The experience guide cites three governing trust principles ("Transparent, Responsible, Accountable"), prescribes a `decorative20` Badge with the ArtificialIntelligenceIcon as the disclosure mark, and *requires a Privacy Impact Assessment before AI shipping*. A working chatbot ("Paste Assistant") demonstrates the assembly. The PIA requirement is the most interesting governance artefact in the production-grade triad — it is the only place a published DS turns the disclosure principle into a procurement-grade required artefact.

A pattern across the three: where principles are attached to *enforceable artefacts* (Atlassian's required disclaimer string, Paste's required PIA, Cloudscape's principle-to-pattern attachments), they bite. Where they are prose only, they are decorative. Treat this as the design rule for principles documentation in (b)-axis work.

---

## Landscape — emerging, experimental, and adjacent

**Carbon Design System (main library) — AI Label / AI Presence**. The Carbon main library is reported to ship an AI Label component (formerly Slug), but inspection paths returned 404 across `/components/AI-label/usage`, `/components/AI-presence/usage`, and `/all-about-ai/`. The signal that AI Label is shipped comes indirectly via the Carbon Labs README's positioning of `@carbon-labs/ai-tag` as the labs counterpart. Treat AI Label as shipped on the Carbon main surface but verify before quoting specifics; the doc paths were unstable on inspection.

**Carbon Labs** (`github.com/carbon-design-system/carbon-labs`). The chat web component (`@carbon-labs/ai-chat`) decomposes into 24 sub-component folders covering card, carousel, chart, code, diagram, editable text, error, file upload, footer, formula, header, history viewer, image, link list, list, loading, message, messages, molecular, popup, table, tag list, and text elements. The breadth of element types — molecule renderer, formula, diagram, chart — is unusual and reflects Carbon's IBM scientific/enterprise content lineage. Status: the repo positions itself as "a community-driven incubation space," sits at v0.13.x, does not label individual packages alpha/beta/stable. Treat as pre-1.0 incubation. The labs/main distinction matters in scoping conversations: a client reading "Carbon ships AI components" will conflate the stable AI Label badge with the incubation chat. The labs work is incubation, not production.

**daisyUI** ships one generic `chat-bubble` component with `chat-start` / `chat-end` placement, `chat-image`, `chat-header`, `chat-footer` and eight semantic colour variants (`daisyui.com/components/chat/`). Pattern-level only — no AI-specific affordances for streaming, citation, refusal, feedback. Useful for chat *layout*, not for AI semantics.

**Microsoft `@fluentui-copilot/*`**. Published as code in adjacent npm packages but not surfaced on the Fluent UI design-system site (`developer.microsoft.com/en-us/fluentui`). The `microsoft/fluentui` repo includes `.agents/skills`, `.claude/skills`, and `AGENTS.md` files — these are agent-onboarding artefacts for contributors, not consumer-facing AI patterns. Treat Microsoft's AI work as an adjacency to Fluent UI rather than a Fluent UI deliverable. This matters for client conversations where Microsoft platform alignment is presumed to deliver AI patterns "for free" through Fluent.

**The OSS lead — Vercel AI SDK and AI Elements** (`ai-sdk.dev`, `elements.ai-sdk.dev`). The most consequential adjacent finding of this survey. Vercel AI Elements — installed via `npx ai-elements` and shadcn-compatible — is functionally the most decomposed open AI-pattern library in 2026. Five pillars: a Chatbot pillar (Attachments, Chain of Thought, Checkpoint, Confirmation, Context, Conversation, Inline Citation, Message, Model Selector, Plan, Prompt Input, Queue, Reasoning, Shimmer, Sources, Suggestion, Task, Tool); a Code pillar (Agent, Artifact, Code Block, Commit, Environment Variables, File Tree, JSX Preview, Package Info, Sandbox, Schema Display, Snippet, Stack Trace, Terminal, Test Results, Web Preview); a Voice pillar (Audio Player, Mic Selector, Persona, Speech Input, Transcription, Voice Selector); a Workflow pillar (Canvas, Connection, Controls, Edge, Node, Panel, Toolbar); and Utilities. The hooks layer (`useChat`, `useCompletion`, `useObject`) is framework-agnostic across React, Vue, Svelte, Angular, Solid. Built on shadcn/ui — which itself ships zero AI primitives in its core registry — AI Elements effectively *is* the shadcn AI extension.

The strategic implication is uncomfortable: in 2026, the OSS AI-primitive layer materially leads the design-system layer. Inline citations with hover cards and source carousels (`<InlineCitation>` with `Trigger`, `CardBody`, `Carousel`, `Source`, `Quote`); branched message alternatives (`MessageBranch` / `MessageBranchSelector` / `MessageBranchPrevious` / `MessageBranchNext`); a tool-call state machine with seven defined states (`input-streaming`, `input-available`, `approval-requested`, `approval-responded`, `output-available`, `output-error`, `output-denied`) plus a paired `<Confirmation>` approval workflow; a Plan/ChainOfThought/Reasoning trio for reasoning surfaces — none of the named eighteen design systems on the source list ship pattern decomposition at this resolution. The OSS layer leading the DS layer inverts the usual relationship and is the single thing most likely to re-shape (b)-axis scoping conversations through 2027. Clients asking for "AI features" on top of an existing DS likely want the AI Elements layer composed onto the DS, not the DS to invent the primitives itself.

---

## The public-sector outlier — New York State

The New York State Design System (`designsystem.ny.gov`) sits under a different governance regime than the SaaS systems: Section 508 / ADA legal exposure, FOIL / open-records obligations on AI-assisted decisions, the wave of state AI disclosure laws beginning to land in 2024–2026. NYS publishes no AI patterns on its DS surface as of mid-2026. The system focuses on tokens, web components, accessibility, Figma libraries — deliberate non-coverage of AI.

The non-coverage is itself the finding. Public-sector design systems are running behind their private-sector counterparts on AI pattern coverage at exactly the moment when public-sector AI deployments are increasingly subject to disclosure regulation. The likely path forward is a *separate* AI guidance layer — owned by an agency CIO or Chief Information Security Officer — coordinating with the DS rather than the DS owning AI guidance directly. Engagements scoping public-sector AI features should expect to deliver against three artefact streams: the DS's existing accessibility-and-tokens contract, an AI-disclosure layer authored against state law, and an evaluation harness owned by whichever office bears the FOIL exposure. Treat this as a multi-artefact engagement shape, not a "we'll just extend the DS" shape.

---

## Negative findings — where the LinkedIn post overclaimed

The source list that prompted this research named eighteen design systems as having "published AI-aware patterns." On direct inspection, most do not. The negative findings are themselves the deliverable, because they show up in client conversations as folkloric claims that the actual systems do not back.

**The clearest overclaim: eBay MIND.** MIND (`ebay.gitbook.io/mindpatterns`) is an accessibility pattern library — the acronym stands for **M**essaging, **I**nput, **N**avigation, **D**isclosure. The "Messaging" section covers Alert Dialog, Toast Dialog, Inline Notice, Tourtip, and similar accessibility-grade messaging patterns. There are no chat, prompt, generative-response, or AI-disclosure patterns. The list positioned MIND as "specifically positioned as an AI pattern library — high priority"; this is wrong, and is the kind of claim that survives in scoping decks until someone fetches the URL. (Two independent agents in this research run reached the same conclusion without coordinating — the strongest possible signal that the original list was simply mistaken on this entry.)

**Accessed and confirmed not publishing AI patterns** (each verified by direct inspection in mid-2026, paths given so the confirmation can be repeated):

- **shadcn/ui core** — no AI components in the core registry (`ui.shadcn.com/docs/components`). Community / third-party registries may contain AI primitives, and AI Elements installs *as* a shadcn-compatible registry, but that is the AI Elements story, not a shadcn one. The phrase "shadcn ships chat components" can be true and false simultaneously and is a frequent source of scoping confusion.
- **HeroUI** — no AI primitives in the component library on inspection (`heroui.com/`).
- **Mantine** — operator-side AI tooling (MCP, llms.txt, agent skills) is shipped; no consumer-side AI components. The clearest single example of (a)-axis publishing without (b)-axis publishing.
- **MUI** — no AI primitives in the component lists (`mui.com/`).
- **Fluent UI (the DS surface)** — AI work lives in adjacent npm packages (`@fluentui-copilot/*`), not on the DS site.
- **Tailwind / Tailwind Plus** — no AI components on the homepage or marketing surface.
- **Primer** — no public AI section. One internal `CopilotAnimation` exists but is not part of the public component catalogue. GitHub has shipped substantial AI UI in product (Copilot Chat) but Primer does not surface those patterns publicly.
- **Power Apps Playbook** — the URL on the original list (`playbook.powerapp.cloud/`) belongs to "Power," an unrelated open-source design system from Power Home Remodeling, not Microsoft Power Apps. It publishes 200+ general components, none AI-specific. The original list was mis-attributed.

**Inaccessible** — could not verify content; treat as unverified, not negative.

- **Lightning Design System 2** (deep link `lightningdesignsystem.com/2e1ef8501/p/85bd85-…`) — Zeroheight-hosted SPA; anonymous fetches return only the page title across multiple sub-paths. Cannot confirm or deny AI-pattern publishing on the SLDS 2 surface. Salesforce's Agentforce product docs sit on `help.salesforce.com` but are not part of the design-system surface.
- **Elisa Design System** (deep link `designsystem.elisa.fi/9b207b2c3/p/155e65-…`) — also Zeroheight-hosted; same SPA-rendering problem. Cannot verify AI patterns by anonymous fetch.
- **ServiceNow Horizon** (`horizon.servicenow.com`) — 403 to anonymous fetch. Now Assist patterns may exist but are not visible.
- **SAP design system** (`sap.com/design-system`) — 403. Joule pattern publishing cannot be confirmed by anonymous fetch.

A practical lesson: any DS on Zeroheight behind anonymous-fetch barriers is effectively *closed* to research-by-fetching. For client engagements where one of these closed systems is the target, expect to scope a manual walkthrough — the kind of audit that Discovery normally captures — because the public surface won't reveal what's been published.

---

## The pattern taxonomy — what is shipping, where it converges, where it diverges

Six clusters survive cross-publisher inspection with two refinements relative to the starting hypothesis: a separate **Tool-call and agent affordance** cluster (broken out from generic conversation primitives because it has its own state machine and is most developed in AI Elements and Cursor); and a **Citation and source attribution** cluster broken out from "Trust, transparency, attribution" because the published implementations diverge sharply on inline-vs-trailing rendering.

### Prompt input

**Anatomy at minimum.** A multiline auto-resizing textarea, a submit affordance whose icon reflects status (idle, streaming, error), a model/context selector, an attachment surface, an action menu for non-default invocations (screenshot, file, voice).

**Convergence.** Every production publisher ships a dedicated Prompt Input distinct from a generic Textarea. Cloudscape's `Prompt input`, Twilio Paste's `ChatComposer`, AI Elements' `<PromptInput>`, Atlassian's "Prompt inline" with floating arrow submit and microphone button — auto-resize is universal; Enter-submits / Shift+Enter-newlines is universal.

**Divergence.** Rich auxiliary affordances are still inconsistent. AI Elements ships the densest assembly (`PromptInputActionAddAttachments`, `PromptInputActionAddScreenshot`, `PromptInputSelect` model picker, `PromptInputCommand` slash-command surface, Tabs, HoverCard, native Web Speech API mic). Cloudscape and Atlassian implement subsets. Slash-command surfaces are *named differently across systems* — Atlassian's "Skills tags" (slash-prefixed lozenges that *restrict execution scope* rather than simply prefilling), AI Elements' `PromptInputCommand`, Cloudscape's "Shortcut menus." These are the same primitive named three ways, with one meaningful semantic divergence: Atlassian's Skills tags are *scope-restricting context controllers*, while Cloudscape's Support prompts are *intent-prefilling chips*. Treat the two as different patterns, not as variant names for the same thing.

### Generative response rendering

**Anatomy.** A typed message wrapper that distinguishes user from assistant, a streaming-aware text renderer, a code-block primitive with copy/run, a way to render structured non-text content (tables, charts, images, files).

**Convergence.** Assistant/user differentiation by alignment and surface colour is universal (daisyUI's `chat-start`/`chat-end`, AI Elements' `Message from="user"|"assistant"`, Paste's `AIChatMessageAuthor`). Streaming via typewriter / shimmer / progressive markdown is universal. Code-block-with-copy is universal.

**Divergence.** How *much* structured content the message can hold. Carbon Labs' `ai-chat` decomposes into 24 element types including chart, diagram, formula, molecular, table, image, carousel — a one-message-many-elements model. AI Elements treats most of these as siblings inside the conversation rather than nested in the message. Cloudscape's "Artifact previews" pattern is the closest analogue to AI Elements' Code/Sandbox/WebPreview pillar but ships less framework-level support.

A subtle but important divergence: **branched / regenerated alternatives**. AI Elements ships `MessageBranch` / `MessageBranchSelector` / `MessageBranchPrevious` / `MessageBranchNext` / `MessageBranchPage` as a first-class pattern. Cloudscape names "Response regeneration" as a pattern but does not publish a branch-traversal component. Paste does not ship branching. Branching is the *convergence target* and the *current divergence point* simultaneously: ChatGPT ships branches; Cursor does not. The DS field will follow whichever frontier-product convergence wins.

### Trust, transparency, attribution — the cluster that subdivides

**Disclosure / labelling.** Cloudscape ships a "Generative AI output label" pattern. Twilio Paste prescribes a `decorative20` Badge with the ArtificialIntelligenceIcon. Carbon ships an AI Label / AI Tag pair. Atlassian uses a colourful generation border plus the standardised disclaimer string `Uses AI. Verify results.`. This is the pattern with the widest cross-publisher coverage — and the widest *visual divergence*. There is no design-system-level convergence on what an AI badge looks like, and the EU AI Act Article 50's requirement that synthetic content be "marked in a machine-readable format and detectable as artificially generated or manipulated" raises a different bar: visual badges alone do not satisfy a machine-readable provenance requirement. The likely convergence path is a *technical* spec (C2PA-style content credentials embedded at generation time) before the visual converges.

Carbon's AI Label, taken alone, is the most architecturally interesting disclosure pattern in the field. It is restricted by design to non-actionable, explainability-focused popovers — the system explicitly forbids mapping AI Label to action triggers like "regenerate." This is a deliberate decoupling of *the disclosure* from *the action surface*; the badge means "this was produced by AI and here is why" rather than "this is an AI control." Most other systems collapse the two and end up with badges that double as buttons, which is exactly the disclosure-theatre failure mode the EU AI Act is responding to.

**Citation / source attribution.** AI Elements is alone in publishing a fully decomposed citation primitive — `<InlineCitation>` with `Trigger`, `CardBody`, `Carousel`, `Source`, `Quote` — that renders an inline pill with a hover card, hostname-and-count display, and a carousel for multi-source citations. It also ships a separate `<Sources>` collapsible-list pattern for trailing attribution. Twilio Paste documents that citations should be composed from Callout / Anchor / Help Text — i.e. no first-class primitive. Cloudscape's pattern catalogue does not name citations explicitly. The field has not converged here, and **inline-vs-trailing is the strategic divergence**: inline citations imply the LLM is grounded with a span-aligned retrieval signal; trailing citations only require a list of URLs at message end. The choice cascades back into the model-side architecture, which is why the design-system layer cannot make it unilaterally — the citation pattern has to be co-designed with the retrieval layer the DS does not own.

**Refusal.** No publisher in the survey ships a first-class refusal component. Paste documents error states (Callout in body, Help Text on actions, Alert above composer for system errors) but explicitly does not call any of them "refusal." Atlassian's principles touch refusal indirectly via "always accelerate responsibly" without prescribing UI. Cloudscape's pattern list does not name refusal. **This is the largest published-pattern gap relative to what frontier products actually ship.** ChatGPT and Claude have spent two years refining refusal UIs — graceful explanation, alternative offer, escape hatch — and no inspected DS has codified any of it. Every regulated-industry AI engagement in 2026 will need a refusal pattern; almost no engagement will have one available off-the-shelf. Treat this as a default custom-build line item.

### Feedback and correction

**Convergence.** Every production system ships a message-level action group for thumbs / copy / regenerate. AI Elements' `<MessageActions>` / `<MessageAction>`, Paste's `AIChatMessageActionGroup` / `AIChatMessageActionCard`, Cloudscape's `Button group` documented as the message-action carrier, Atlassian's feedback affordances inside chat-message cards. Binary feedback inside the bubble, persistent on touch, no hover-only — this is the converged shape.

**Divergence.** Structured feedback for evaluation. None of the inspected systems publishes a "structured feedback for evals" pattern — i.e. a UI that captures the *reason* for a thumbs-down in a way that flows to an evaluation harness. Cloudscape's principles mention "feedback loops" for bias mitigation but this is not surfaced as a component. This is a clean publisher gap: the eval contract that distinguishes a usable AI feature from a demo (see the architecture section below) has no published UI primitive across the field.

A second divergence: **state restoration**. Carbon's documented "Revert" pattern — when a user edits an AI suggestion, the AI styling is removed and the label is replaced with an icon-only "Revert to AI" button that restores the original suggestion — is a stateful interaction model the rest of the field treats as static. The Revert pattern is the most architecturally interesting feedback primitive in the (b) field; treat it as a candidate primitive for any client engagement where AI suggestions land inside form fields the user can edit.

### Conversation primitives

**Anatomy.** A message container with auto-scroll, an empty state, message-thread continuity, a way to anchor the prompt input to the bottom of a scrolling region.

**Convergence.** Auto-scroll-to-bottom with a "scroll to latest" button is universal. AI Elements' `<Conversation>` with `ConversationContent`, `ConversationEmptyState`, `ConversationScrollButton`, `ConversationDownload` (and a `messagesToMarkdown` exporter) is the most decomposed implementation. Paste's `useAIChatLogger` hook with push/pop/clear is the equivalent state model.

**Divergence.** Chat *layout* primitives. Atlassian explicitly ships three layouts as first-class patterns — full-page (AI create), sidebar, floating — each with different positioning rules. Cloudscape leaves layout to the consumer. Paste publishes a single composer pattern. Carbon Labs is single-layout. The Atlassian three-layout taxonomy is the convergence candidate worth watching; on engagements without a layout grammar, borrowing it directly is the strongest available default.

### Tool-call and agent affordance — the new cluster

**Anatomy at minimum.** Tool-call rendering with state (pending, running, completed, errored, denied, approval-requested), input/output formatted display, an approval workflow when the tool is privileged.

This is the cluster where AI Elements moves furthest ahead of every named DS publisher. `<Tool>` decomposes into `ToolHeader`, `ToolContent`, `ToolInput`, `ToolOutput`, with seven defined states (`input-streaming`, `input-available`, `approval-requested`, `approval-responded`, `output-available`, `output-error`, `output-denied`), and a paired `<Confirmation>` component for the approval workflow (`ConfirmationRequest`, `ConfirmationAccepted`, `ConfirmationRejected`, `ConfirmationActions`). `<Plan>` and `<ChainOfThought>` handle the reasoning trace; `<Reasoning>` handles single-block reasoning streams. Cloudscape names "Thinking," "Progressive steps," and "User authorized actions" as patterns but does not publish equivalent component decomposition. Atlassian leaves tool-call UX to product implementations. This is a 12-month-ahead gap and the cluster where the OSS-leads-DS inversion is most visible.

### Governance / principles

**Convergence.** Every production publisher ships an AI principles document. Cloudscape's six, Atlassian's eight, Paste's three (Transparent, Responsible, Accountable) plus seven base design principles. The principles overlap considerably — transparency, control, error handling, accountability appear in all three. **Where they bite is where they attach to enforceable artefacts.** Paste's required PIA, Atlassian's standardised disclaimer string, Cloudscape's principle-to-pattern attachments — these are the patterns the system actually enforces. A principles doc that lists eight virtues and connects to nothing is a marketing artefact.

---

## Tooling reality — what's available off-the-shelf vs. what's bespoke

### What the OSS layer actually ships

**Vercel AI SDK + AI Elements** is the de facto open AI-UI primitive layer in 2026. Hooks (`useChat`, `useCompletion`, `useObject`) are framework-agnostic across React, Vue, Svelte, Angular, Solid. AI Elements components install via `npx ai-elements` and are shadcn-compatible. Coverage spans chat, code, voice, workflow.

**shadcn/ui core** ships zero AI components. The community-registry path means "shadcn ships chat components" can be true (via AI Elements installed as a shadcn-compatible registry) and false (in core) at the same time. Be precise about which when scoping.

**Carbon Labs** — `@carbon-labs/ai-chat` (web component) with the rich element decomposition above; pre-1.0 incubation status. Distribution per-package on npm.

**Twilio Paste** — `AIChatLog` and dependents in the published Paste React library; `useAIChatLogger` hook for state.

**Cloudscape** — six GenAI-category components in `@cloudscape-design/components`. Stable.

**Atlassian** — Rovo components are shipped via internal Figma library and product implementation; the public DS surface documents patterns rather than exposing the components as installable npm packages outside Atlassian product.

**Microsoft `@fluentui-copilot/*`** — published as code, not surfaced on the Fluent UI DS site. Adjacency, not deliverable.

### Where the OSS layer ends and bespoke begins

Four durable seams.

**Multi-modal input beyond attachments.** Voice input is in AI Elements' Voice pillar (Speech Input, Mic Selector, Persona) and Atlassian's microphone button, but neither expects to handle live transcription, diarisation, or interruption semantics. Those are bespoke product work.

**Citation correctness, not just citation rendering.** AI Elements renders an `<InlineCitation>`. Whether the citation actually points to a span the model used is an evaluation problem owned outside the DS. The pattern can be present and broken simultaneously — the rendered citation is confidently displayed regardless of whether the underlying retrieval is grounded. This is the place where shipping the UI without shipping the eval becomes a trust failure rather than a UI failure.

**Refusal as a product surface.** No published primitive. Refusal copy, refusal categories, refusal-to-recovery handoffs are bespoke product work. Every regulated-industry engagement should expect to scope this.

**Evaluation-instrumented feedback.** Every system ships thumbs / regenerate. None ships a flow that connects the thumbs-down to a structured eval log (rubric tag, severity, follow-up question to the user). Connecting feedback to an eval pipeline is bespoke.

### The Figma-to-code round-trip

Publishers that ship both Figma kits and code primitives — Paste, Cloudscape, Atlassian (internal-only) — surface AI components in both. Carbon Labs' Figma kit appears separately on the Figma Community. AI Elements ships React-only with no Figma counterpart, which means anyone using AI Elements in a non-trivial product needs a separate Figma kit. This is a known gap and the place where engagements quietly sink time. Scope for it explicitly when the architecture is "AI Elements components on a non-AI-Elements DS."

### MCP and the AI-readable-pattern recursion

Mantine's MCP server, Cloudscape's published `llms.txt`, shadcn-style registries that codegen agents fetch directly — these are the (a)-axis tools that make (b)-axis patterns assemble correctly. Where this becomes load-bearing for (b) is when the consumer-side AI surface composes itself dynamically (the "Generative UI" idea — an LLM choosing components from the DS and assembling a layout at runtime), which requires the patterns themselves to be machine-discoverable. AI Elements' tight coupling to the `UIMessage` type and `ToolUIPart` shape is the visible artefact: the pattern primitives are designed to be assembled by an AI agent, not just consumed by a human developer. This is the sense in which the (a) and (b) axes meet — and the architectural reason a system that ignores (a) cannot fully deliver (b) at the depth modern products are reaching for. (See 15-ai-in-ds for the (a) layer; see 04-documentation for the AI-readable docs angle.)

---

## Architecture and governance — what shipping (b) actually requires

The four-prerequisite minimum that turns AI-pattern shipping into more than UI cosmetics is shared with the (a) axis: components-as-data, structured metadata, evaluation contracts, content/safety governance. (15-ai-in-ds covers the architecture in depth; this section calls out where the (b) axis bites differently.)

**Components-as-data** is implicit in AI Elements' design (the components consume `UIMessage` directly) and in Cloudscape's six explicit GenAI components. Carbon Labs' web-component approach is consistent with this. Paste's components consume hook state. None of the systems lacking AI primitives have a pathway to ship them without first making the rest of their library data-shaped. A client engagement that scopes "we'll add chat to the existing system" without auditing whether the system is data-shaped is scoping cosmetic chat that won't carry tool-call rendering, branched messages, or streaming structured output.

**Structured metadata** is where Carbon Labs' element decomposition (chart, diagram, table, formula, molecular) is interesting: those are typed message parts, not free text. Pattern publishing without typed message parts collapses to "we shipped a div with Markdown."

**Evaluation contracts** are the largest gap. None of the inspected libraries publish CI hooks for refusal correctness, citation grounding, or tool-output verification. A published refusal pattern is *correct* only if the underlying classifier-or-router is reliably triggering it; a published citation pattern is *correct* only if the citation resolves to the source the model used. The eval contract is the part that distinguishes a usable AI feature from a demo, and the design-system field as of mid-2026 simply does not publish it. The closest published implementation is AI Elements' `<Tool>` state machine with `output-error` and `output-denied` as first-class states — these correspond to evaluatable outcomes (denial reasons, error categories) and are wired into the SDK's tool-result types. This is the architectural pattern other systems will need to copy.

**Content / safety governance** is partially addressed by Twilio Paste's PIA requirement and Atlassian's "verify results" disclaimer; entirely absent elsewhere. Every chat pattern presumes a content layer the DS does not own — sources for retrieval, allowed tool surfaces, system prompt content, safety filters. The DS contract ends where the corpus begins; engagements should treat that handoff as a named scope boundary in the SOW, not as a footnote.

### Disclosure regimes in 2026

The voluntary industry-pattern layer (AI badges) is the visible part. Underneath it, three regulatory layers compound:

- **EU AI Act Article 50** (full applicability 2 August 2026 — verify before quoting). Synthetic content must be "marked in a machine-readable format and detectable as artificially generated or manipulated"; chatbot interactions must be disclosed; deepfakes must be disclosed by deployers; AI-generated text on matters of public interest must disclose origin unless human-edited under editorial responsibility. The "machine-readable" requirement is the bit DS publishers have not yet operationalised — current AI badges are visual disclosure to humans, not machine-readable provenance.

- **US state laws (2024–2026).** California SB 942 (the California AI Transparency Act) mandates a free AI-detection tool plus a "latent disclosure" of provenance for covered providers; AB 2355 mandates political-ad disclosure; AB 3030 mandates patient-communication disclaimers; Colorado SB 24-205 covers high-risk-system disclosures; Utah's Artificial Intelligence Policy Act establishes baseline disclosure obligations. The list lengthens monthly; cite the regulator's published text directly, not a DS principles document.

- **Public-sector overlay.** Section 508 / WCAG conformance and FOIL / open-records exposure when AI is used in decisions affecting the public sit on top of the federal/state framework. NYS does not publish AI patterns yet, which means each agency is currently inventing.

The verification path matters: regulatory state changes faster than design-system documentation. For any client engagement, the citable artefacts are the regulator's published text (eur-lex for EU; state code citations for US) — not the DS principles document. (See 07-governance-and-adoption for the governance phase implications; this file's scope is the (b) pattern surface, not the governance phase.)

---

## Scoping implications

Two practical recommendations fall out of the survey for any engagement whose scope includes AI features on top of an existing or new DS.

**One.** Default to the OSS-leads-DS inversion. When a client says "we want AI features on our DS," the most-likely-correct architectural answer in 2026 is "we will install AI Elements (or an equivalent OSS primitive layer) into your DS, theme it against your tokens, and add the bespoke layer for refusal, eval-instrumented feedback, citation verification, and any client-specific governance." This is *not* "we will invent AI primitives inside your DS." Inventing primitives is one to two years of work to catch up to AI Elements; theming AI Elements is days to weeks. Reserve invented primitives for places the OSS layer is genuinely insufficient — multi-agent handoff (where nothing has converged), domain-specific structured rendering (Carbon Labs' molecular/formula content for scientific contexts), bespoke agent UX that is itself a brand surface.

**Two.** Make the (a) axis a co-deliverable, not a phase-2 add-on. The (b)-axis patterns assume the (a)-axis architecture (components-as-data, MCP, structured metadata) is in place. Trying to ship (b) on top of a system that has not done the (a) work produces patterns that *visually* match the published exemplars but break the moment a tool agent or a generative-UI feature tries to assemble against them. (See 15-ai-in-ds for the (a) phase shape and 04-documentation for the documentation seam.)

**Where the hidden complexity sits** — and what to put in the SOW:

- **Content and corpus governance.** Whose corpus is the model retrieving against? Who curates it? What's the change-management process? This is not a DS deliverable, but the DS contract has to explicitly *not* claim it. Name it as an out-of-scope dependency.
- **Eval harness.** Refusal correctness, citation grounding, tool-output verification. Either commit to building one as part of the engagement or name it as out of scope and flag the consequences.
- **Disclosure compliance.** Article 50 enters full applicability mid-2026. State laws continue to land. Bake disclosure-pattern review into the engagement and re-review at every release.
- **Refusal as a default custom-build line item.** No DS ships one. Every regulated-industry engagement needs one.
- **Bespoke Figma counterpart for OSS components.** AI Elements ships React-only. If the engagement uses AI Elements and the client expects Figma parity, scope the Figma kit explicitly.

---

## Failure modes

**Assumed maturity.** A client reads "Carbon ships AI components" and conflates a stable AI Label badge with the Carbon Labs incubation chat. The labs/main distinction is meaningful and gets dropped in scoping conversations. Same shape: "shadcn has chat" — true via AI Elements, false in core.

**Component-level shipping without governance / eval.** Most of the named systems are here. The visible UI works; the back-end behaviour is undefined. A `<MessageActions>` thumbs-up button with no eval pipeline is the canonical instance.

**Design-led patterns without engineering buy-in on safety / eval.** The Atlassian principles ship as design direction; whether engineering ships the corresponding evaluation harness is a separate question. The principles document is high-leverage only if engineering is contractually bound to it.

**Disclosure theatre.** A `decorative20` Badge that satisfies the UI checklist without changing user understanding. The EU AI Act's machine-readable provenance requirement raises the bar — a visual badge alone does not satisfy Article 50 for synthetic content.

**Streaming-as-novelty.** AI Elements' `MessageResponse` and Paste's `animated` typewriter prop both render incrementally. Whether the streamed content is faster than a structured non-streaming JSON response is a backend question; novelty cost is real (typewriters delay information for users who scan) and the DS-level pattern does not litigate the choice.

**Citation patterns without verification.** AI Elements' `<InlineCitation>` renders pills with sources — but if the model invented the source, the pattern surfaces fabrication confidently. The published primitive is a UI; the verification is missing. This is the failure mode that turns trust patterns into trust failures.

**Inconsistent refusals.** Without a refusal primitive, the same product surface ships three different refusal copies depending on which engineer wrote the path. Every system inspected has this problem.

**ARIA live-region saturation.** Configuring live screen-reader regions to announce every incoming token in a real-time stream produces an unusable auditory experience — the screen reader reads each word as it renders and blocks the user from executing other navigation. The right pattern is quiet status updates and announce-on-paragraph-complete, not announce-on-token. (See 14-accessibility for the architectural framing of live regions.)

**Walled-garden custom agent UIs.** Individual product squads building ad-hoc conversational widgets that bypass the central DS — inconsistent layouts, varying feedback icons, non-standard visual styles across the product suite. Atlassian explicitly addresses this risk by anchoring AI experiences to brand thread ("weave a bit of Atlassian") and using Rovo as a unifier. Other publishers leave the risk to product teams to solve.

**Backend contract drift.** Designers create elaborate mockups of inline annotations and structured feedback inputs without aligning with engineering on whether the backend can return structured token indexes, parse citation targets, or store granular multi-attribute feedback. The frontend remains a non-functional mockup. This is the classic visual-first failure mode the (a)/(b) split is trying to prevent — surface the data shape *before* the visual.

---

## Open questions and contested territory

**Inline vs trailing citations.** No convergence. AI Elements ships both; most DS publishers ship neither as a first-class primitive. The choice is upstream of UI — it constrains the retrieval architecture.

**Refusal as a published primitive.** Frontier products have refined refusal patterns (graceful explanation, alternative offer, escape hatch). No DS in this survey publishes one. The largest open gap, and the one most exposed to regulatory and trust pressure.

**Branched / regenerated alternatives.** AI Elements ships them; most don't. The product question is whether end users want branching or whether it confuses the conversation model. ChatGPT ships branches; Cursor does not. The DS field will follow the frontier-product convergence.

**Standardised AI badge.** No cross-system visual convergence. The EU AI Act's machine-readable provenance requirement may force convergence on a *technical* spec (C2PA-style content credentials) before the visual converges.

**Feedback-to-eval flow.** A thumbs-down primitive that captures rubric and severity and writes to an eval log. Nobody publishes one.

**Multi-agent / agent handoff.** Atlassian's principle "expand to multi-player and multi-intelligence" is the only published pointer. The pattern is not yet shipped. Primer's accessibility-first guidance on announcing agent transitions to screen readers is the only piece of the multi-agent puzzle that has been published anywhere as concrete technique.

**Voice-first chat surfaces.** AI Elements has a voice pillar; no other inspected DS does. Atlassian has an audio telepointer for Rovo. Whether voice belongs in the chat surface or is a separate input mode is unsettled.

**Generative UI as a runtime architecture.** The AI SDK's "Generative UI" idea — an LLM choosing components from the DS and assembling layouts at runtime, drawing from the component library directly via MCP — challenges the traditional concept of a design system as a static library. Instead, the DS functions as a generative *runtime* that can safely render layout changes on the fly. None of the inspected publishers ship this as a coherent runtime architecture. It is the convergence target the most-aggressive engagements should be tracking; it is also the territory most likely to outrun governance.

**Where DS patterns lag frontier products.** Cursor's plan-then-act flow (plan mode, parallel agents, Slack/CLI integrations), Claude's artifact rendering, ChatGPT's branched conversations and "edit message" flow — these are 12–18 months ahead of every DS-level published pattern. The implication for adoption strategy: do not promise clients that their AI feature will look like ChatGPT-current using DS-published primitives. Either build bespoke ahead of the DS, or accept the lag.

**Where governance is moving faster than the library.** Article 50 enters full applicability mid-2026. State laws are accumulating monthly. The published DS surface is months-to-years behind the regulatory clock. Any engagement scoped today against a DS that does not publish AI patterns is on the hook for the disclosure layer itself. This is the reason the (b) axis cannot be deferred indefinitely as "a phase-2 concern." Phase 2 arrived; the regulators do not wait.

---

## Practice positions to commit to

Three positions the practice should commit to coming out of this survey:

1. **Default to OSS-led primitives, theme rather than invent.** AI Elements is the convergent OSS layer; Cloudscape, Atlassian, and Paste are the DS reference points for what the integrated surface looks like. Commercial proposals should default to "install AI Elements (or equivalent), theme against the client's tokens, scope the bespoke layer for refusal / eval / citation verification" rather than "invent AI primitives inside the existing DS."

2. **Treat (a) and (b) as a single architecture with two surfaces.** Scope the (a) work — components-as-data audit, MCP server, structured metadata, AI-readable docs — as a co-deliverable when (b) is in scope. Name them separately on the SOW so the client sees the architectural dependency rather than reading the (a) work as scope creep.

3. **Make refusal, eval-instrumented feedback, and disclosure-compliance review default custom-build line items on regulated-industry AI engagements.** The DS field does not ship these. Pretending it does in scoping conversations costs the engagement at delivery. (See 13-trust-governance-liability under 09-gaps for the broader field gap on indemnification, audit trails, and provenance.)

---

*Provenance: synthesised 2026-05-19 from a dual-agent research run against eighteen named design systems plus extensions surfaced during inspection. Raw outputs are in `_research/_inbound/2026-05-19-ai-aware-ds-patterns/`. Where the two agents diverged on a factual claim, this file follows the agent that cited a fetched URL; where neither agent could verify (Lightning, Elisa, ServiceNow, SAP), the file says so. The "OSS-leads-DS" framing, the 24-element decomposition for Carbon Labs, the seven-state tool-call machine for AI Elements, and the EU AI Act Article 50 (vs. Article 52) date are claims that came from the URL-cited agent and should be re-verified at the moment of citing in client work. The eBay MIND negative finding was reached independently by both agents — the strongest cross-agent confirmation in the run.*

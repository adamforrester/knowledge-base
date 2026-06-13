---
type: practice-area
title: Adaptive Interfaces - Implementation
description: Engineering companion to 26. Five-rung spectrum (rule-based to code-emit), tool-calls as UI primitive, RAG, multi-step agentic flows, four-tier memory, streaming UI, eval-driven QA, cost modelling.
tags: [extension, ai, adaptive-ui, agents, rag, memory, streaming]
timestamp: 2026-06-10
---

# 27 — Adaptive Interfaces (Implementation)

> The companion to 26-adaptive-interfaces-foundations. Where that file covered *what and why* — the lineages, the postures, the personalization-versus-adaptation distinction, the evidence base, the ethics, the four-postures-and-fourteen-patterns scaffold — this one covers *how it actually works*: architecture, integration patterns, memory and governance, streaming UI, evaluation and QA, cost and latency, authoring tooling, and the design-systems implications that fall out. It is written for someone who needs to have informed strategic conversations about this work without building it personally — the engineering reality behind the vendor pitches, where the real engineering risk sits, and what a vendor is eliding when they say "generative UI."

---

## Three things to flag at the top

1. **The generative end of the spectrum is nearly empty in production.** The vivid demo — an AI writes a fresh React interface for each user, each request — describes almost nothing that ships to consumers on web or mobile in 2026. v0, Lovable, Bolt, and their peers are *build-time* tools used by developers, not runtime systems serving model-authored code to end users. Every credible production "adaptive UI" sits well short of that. **The action is in the middle of the spectrum, and the middle is more boring and more buildable than the pitch.**

2. **The architecture that named "generative UI" is in an ambiguous state — not dead, not the standard.** Vercel's AI SDK RSC, which introduced streaming-React-components-from-the-model in 2024, is officially marked experimental in Vercel's own documentation ("we recommend using AI SDK UI for production"), has a published RSC-to-UI migration guide, and a GitHub discussion confirming RSC development is paused. It was also extracted into a maintained `@ai-sdk/rsc` package in v5 (July 2025), and `streamUI` still exists. Treat it as *experimental, officially deprioritized for production, with a published migration path — maintained, not removed.* Production work has moved to the typed `message.parts` model; the RSC approach is a maintained side road, not the highway and not a ruin.

3. **There is no design tool for this.** Designing a fixed screen has Figma. Designing a system that renders differently every time has nothing mature — no tool lets a designer specify a space of possible outputs and review the *distribution* of what comes out. The workflow is patched together from Figma, Storybook, prompt-to-code tools, and code. §8 below does not pretend this is solved.

A note on method: where the dual-agent research passes disagreed, verification against primary sources decided. The polished agent and the more-cited agent were each right about things the other got wrong. Polish is not evidence; hedging is not rigor. (See the provenance footer for the full method.)

---

## The decision-tree-to-generative spectrum — the engineering scaffold

26-adaptive-interfaces-foundations adopts the Sentient Triangle as the *experiential* scaffold (four postures: tools, chat, agents, copilots). This file uses a parallel *engineering* scaffold — five rungs that pull apart what "generative UI" actually means as architecture. Each rung has a different cost model, latency profile, safety surface, and answer to *can you QA this.* Vendor copy collapses the five into a single word; the practical discipline for a buyer is to refuse the word and ask which rung is in play.

| Rung | Core mechanism | Latency profile | Safety / brand risk | Where it ships |
|---|---|---|---|---|
| **1. Pure rule-based** | Conditional routing on edge or client flags | <50 ms | Very low; deterministic | Localization, A/B tests, targeted content — **dominant by deployment volume** |
| **2. Catalog selection** | LLM picks a pre-built component or variant ID from a closed set | 100–500 ms | Low; model routes, does not style | Transactional screens, checkout, dashboard panels |
| **3. Template composition** | LLM populates slots in strict component templates | 500 ms–1.5 s | Medium; clipping/overflow risk | **Contextual workspaces, AI-assisted canvases — where most real work is** |
| **4. Deterministic shell** | LLM emits schema-conforming JSON; a deterministic renderer takes over | 500 ms–3 s | Medium; needs client-side validation | **Live reporting, data viz, form builders — where most real work is** |
| **5. Direct code emission** | LLM generates executable front-end code at runtime | 2–8 s | High; arbitrary code, breakage, silent a11y regressions | Prototyping sandboxes; runtime ≈ unshipped |

Rungs 3 and 4 are bolded because that is where genuine production work concentrates. Engineering teams rarely build at the extremes: pure rule-based systems are too rigid for real context, and runtime code generation is too slow, costly, and unpredictable for core application paths. **The book's "slot-based generation" framing — a hand-designed shell, hand-defined slot types, generated content, and a context-inferred selection of which slots appear (Clark & Kindred, 2026, Ch 6) — is Rungs 3–4 expressed as a programming model.** Granola, Linear's Triage Intelligence, the Salesforce generative canvas, Cisco's AI Canvas, and Ask Amplitude all live here.

Two cautions about the spectrum as a model. First, real systems are hybrids — "a rule-based shell with one Rung-4 structured-output panel inside it," not a single architectural choice. Second, "generative UI" as a vendor term spans Rungs 2 through 5, which inflates claims by design. The disciplined buyer's question: *does the model select, compose, emit data, or emit code — and does it do so at build time or at runtime?* Four answers, wildly different consequences.

On Rung 5 specifically: research is pushing on it — Leviathan et al.'s *Generative UI: LLMs are Effective UI Generators* (Google Research, 2025; generativeui.github.io) demonstrated an architecture in which an LLM with tools emits a full HTML/CSS/JS page, with results human raters preferred over plain model text. But that is a research result with an evaluation dataset attached, not a shipped consumer product. Anthropic's *Imagine with Claude* research demo (2025) pushed runtime generation further still — generating UI elements click-by-click rather than in advance — and Clark & Kindred's frank verdict on it (Ch 6) is the practitioner's: *"remarkable but unruly … click-by-click generation felt a little bit more acid trip than user journey."* Runtime code emission is viable as build-time tooling and risky as a runtime, and that distinction does a lot of work that marketing copy collapses.

---

## LLM integration patterns

If the spectrum says *how generative* a system is, this section covers the mechanics — how a model's output becomes an interface. Five patterns, and they compose. The coordination layer that bridges non-deterministic model output to deterministic client rendering looks, in the abstract, like this:

```
  ┌───────────────┐   1. user input     ┌──────────────┐
  │  Client UI    │ ──────────────────► │  Server +    │
  │  (renderer)   │ ◄────────────────── │  LLM         │
  └───────────────┘  4. streamed JSON   └──────────────┘
        │  ▲                                   │  ▲
        │  │ 2. tool catalog (schemas)         │  │ 3. execute
        ▼  │                                   ▼  │   (DB / API)
  ┌───────────────┐                     ┌──────────────┐
  │ Registered    │                     │ Tool         │
  │ components    │                     │ functions    │
  └───────────────┘                     └──────────────┘
```

### 2.1 Tool calls as a UI primitive

The headline pattern is the idea that an LLM "decides what UI to render" by calling a tool. Stripped of mystique: the developer defines a set of tools and, for each, writes the component that will display its result. The model is given the tool definitions and, during a response, emits a *function call* — a tool name and arguments — exactly as it would to call a weather API. The application intercepts the call, runs the tool (which returns structured data), maps the tool name to the pre-written component, and renders it with the tool's output as props. **The model never emits an interface. It emits a *decision*; the rendering is deterministic code a human wrote in advance.**

This relocates the design control surface: the model's freedom is bounded by the tool catalogue and the argument schemas. Constrain what can appear by constraining the catalogue. The Vercel AI SDK is the canonical reference because it has shipped two generations and publicly preferred the second. The production-recommended model (AI SDK 5, July 2025; AI SDK 6, December 2025) exposes a typed `message.parts` array; tool calls appear as typed parts with an explicit lifecycle — `input-streaming`, `input-available`, `output-available`, `output-error` — and the client switches on part type and state, showing a loading skeleton at `input-available` and the real component at `output-available`. The earlier RSC approach (`streamUI`) sits in the experimental-but-maintained state described in the preface. (The seven-state tool-call machine in Vercel's AI Elements ships this exact pattern as published primitives — see 25-ai-aware-patterns-and-conversational-ui §3.6 for the chat-side decomposition.)

This pattern is what *call-and-response UI* (Clark & Kindred, 2026, Ch 6) actually is under the hood. The book's worked example — a system prompt that instructs the LLM to "act as a lightweight interface designer" and respond with structured JSON containing `intent`, `UI`, `rationale`, and `data` fields, populated against a catalogue of available UI components and the user-intent each is for — is the most accessible published walkthrough we have of how a designer specifies the constraint envelope. **The system prompt becomes a hybrid artefact: part design spec, part requirements doc, part programming language.**

### 2.2 Structured outputs and schema enforcement

Structured outputs are the mechanism underneath Rung 4: the model emits schema-conforming JSON, guaranteed by *constrained decoding*, and a deterministic renderer takes it from there. OpenAI's Structured Outputs (released August 2024) uses constrained sampling so "the model cannot produce output that violates your schema." Anthropic compiles a JSON schema into a grammar that restricts token generation at inference time; it has reached general availability with documented limits worth knowing (no recursive schemas, a cap on strict tools per request). The Vercel AI SDK wraps both behind `generateObject` / `streamObject` keyed to a Zod schema.

The architectural payoff is a clean separation of concerns. **The model owns content and structure within the schema's bounds. The renderer owns pixels, accessibility, responsiveness, and brand.** You test the renderer exhaustively once, then fuzz the schema. This is the cleanest available answer to "how do you QA a generative interface" — make most of the interface not generative, and make the generative part a data contract. OpenAI's Apps SDK (previewed November 2025) is Rung 4 at scale: a tool returns `structuredContent`, ChatGPT renders a developer-authored component, and the recommended pattern explicitly separates "data tools" from "render tools."

### 2.3 RAG as context grounding

Retrieval-augmented generation's role is upstream and easy to misplace. RAG renders nothing; it injects retrieved context — user history, account data, documents — into the prompt, and that context shapes what the model emits, which shapes the UI. In a Rung-4 system, retrieved user data becomes the context a structured-output call turns into JSON, then UI. The 2025 framing trend renames this the "context layer," which is more honest about its function — and a reminder, from the foundations file's ethics section, that the retrieval layer is also *an attack surface*: option and decoy injection into retrieved context steers the model itself (Cherep, Maes & Singh, 2025; Liou et al., 2025; Liu & He, 2024). See 26-adaptive-interfaces-foundations §7.3 for the manipulation framing this implies, and §6.3 below for the red-teaming response.

### 2.4 Multi-step and agentic flows

Adaptive interfaces increasingly interleave UI and action: show a component, take input, perform an action, show another component. The AI SDK's agent abstractions run complete tool-execution loops, and because tool parts can render UI mid-loop, a flow can paint an interface, wait for a person, and continue. LangGraph emits UI components from graph nodes and persists UI state across steps with explicit human-in-the-loop checkpoints; LangChain and LlamaIndex provide the orchestration for multi-agent routing. **The design consequence: the interface is no longer a destination but a series of surfaces materialised along a process** — which is the engineering shape of Clark & Kindred's *Manager Experience* (Ch 7) and the agent typology of Taskers, Alchemists, Stewards, Conductors (Ch 8).

The architectural choice that matters most for an agent engagement is **workflow vs. notebook** (Clark & Kindred, 2026, Ch 8). A *workflow* is a deterministic if-then process where the user pre-specifies every branch and the agent's autonomy is low; the surface is the **Workflow Canvas** UI pattern (Lindy is the cleanest published exemplar — drag triggers, conditions, actions, and data sources onto a canvas and connect them, with optional *agent steps* as scoped LLM moments inside the otherwise deterministic flow). A *notebook* is a probabilistic procedure described in natural language where the agent applies its own reasoning to figure out what to do; the surface is the **Agent Notebook** UI pattern (Fin's customer-service procedures are the published exemplar, and the emerging *agent skills* standard — Claude and Copilot both expose user-supplied skills — is the formalisation). Workflows give predictability at the cost of brittleness in unexpected scenarios; notebooks give adaptability at the cost of less predictable outcomes. **The choice cascades into how the engagement gets QA-ed (§6 below), how the human-in-the-loop ritual is designed, and how drift gets bounded.** Bring this axis into agent-engagement scoping the way the personalization-vs-adaptation diagnostic (26 §3) gets brought into experience-engagement scoping.

The book's three rules of thumb for taskers transfer directly into engineering scope: **3–6 tools is the sweet spot** for a focused tasker (agents wobble past a dozen); permission rituals belong at *transitional seams* with the **Action Guard** functional pattern (the cost-of-being-wrong of action-guarding too rarely is much higher than action-guarding too often, but watch for dialog fatigue); and long-running agents drift, which is bounded by **visibility** (the *Activity Stream* UI pattern), **memory hygiene** (instruct the agent to consolidate its own history and discard failed attempts; some systems use a dedicated tasker for this), and **course correction** (mid-mission check-ins that let the user revise mission and plan before drift turns into derailment).

A note on *interface agents* — agents that drive someone else's UI by typing into forms, clicking buttons, and making phone calls. **This is the path of most resistance, not the future** (Clark & Kindred, 2026, Ch 8). Phone calls are "APIs for humans," not for machines; the throughput is low and the failure rate high. When no agent-native channel exists, the interface agent is a stopgap — Big Medium's old fax-machine-bridged hotel-booking system is the structural analogue. The work to invest in is *agent-native* channels (structured product data, machine-legible APIs, accessibility-tree quality) on the receiving end of the agentic-commerce traffic shift in 26 §5. The deterministic, well-structured, semantically-labelled data layer that makes Rung-4 generation work is the same layer that makes a product legible to a buying agent — invest there, not in retrofitting agents to navigate hostile human UIs.

### 2.5 Streaming and an emerging interop layer

The streaming primitive — partial structured output a renderer can paint from incomplete-but-valid data — is large enough for its own section (§5 below). On standardisation: an interop layer is forming beneath all of this. The Model Context Protocol (MCP) standardises how applications expose context and tools to models; an extension, MCP Apps (SEP-1865), standardises interactive UI delivered *from* an MCP server; the AG-UI protocol (CopilotKit, 2025) aims to standardise the event stream between an agent backend and a frontend. Clark & Kindred (2026, Ch 6) flag *A2UI* as another emerging candidate. **None is settled** — treat "MCP will be the standard" as `*[speculative]*` — but the industry is trying to agree on a wire format for "a model produced something that should become UI," and which format wins is a live question to track, not bet on. Clients in this space should expect to refactor at least once.

---

## Multimodal considerations

Web and mobile no longer assume one input shape. **An adaptive UI that adapts only its *content* while assuming a mouse is adapting along the wrong axis.**

| Modality | Core challenge | Interface response |
|---|---|---|
| Pointer & keyboard | Eroding default; hover-only affordances | Density OK, but never hover-gate a function; treat form factor as a weak proxy for input |
| Touch & gesture | Invisible affordances; no haptic confirmation | ≥44 pt targets; every gesture needs a visible non-gesture path; immediate visual feedback |
| Conversational / typed NL | The blank-prompt problem | Hybrid surfaces — NL alongside GUI controls, chips, slot-filling forms |
| Voice | Turn-taking, transcription error | Real-time transcription feedback; confirm consequential actions |
| Vision / camera | High bandwidth, high ambiguity | A grounding step — surface what the system believes it sees |
| Ambient / proactive | Disruption, alert frequency | Event-driven; batch into a quiet inbox-style stream, not a chat |

### 3.1 Pointer, touch, conversation

Pointer and keyboard remain the implicit assumption of nearly every web framework, but they are now one modality among several. WCAG 2.2 codified the response — Success Criterion 2.5.8 requires interactive targets of at least 24×24 CSS pixels — and it is legally load-bearing in the EU under the European Accessibility Act, and increasingly in adaptive contexts where the renderer cannot pre-screen every generated DOM. (See 14-accessibility on the architecture, 16-mobile-accessibility-implementation on the framework-level treatment.) Touch contributes directness; its cost is discoverability, since a gesture is an invisible affordance, and the settled guidance is that **every gesture needs a visible non-gesture alternative.**

Typed natural language is shipped at scale; its failure mode is the *blank-prompt problem* — an empty box communicates nothing about capability — and the shipped mitigation is hybrid surfaces, not conversation-as-interface. (Saarinen, *Design for the AI Age*, Linear, 2025: *"a chat interface is a very weak and generic form."*) Clark & Kindred's *minimum viable personality* (Ch 5) and the NPC pattern (Ch 6) are the design discipline for the cases where natural language *is* the right surface — give the assistant a scoped, intentional character, not the full surface area of an "ask me anything" agent.

### 3.2 Voice and vision

Voice quality and latency have crossed the usability threshold: OpenAI's `gpt-realtime` (August 2025) collapses the speech-to-text → LLM → text-to-speech pipeline into a single model with sub-second voice-to-voice latency; Gemini Live ships real-time voice with camera and screen-sharing across Android and iOS. **But genuinely overlapping, listen-while-speaking dialogue has not shipped** — Advanced Voice Mode is still turn-based; the user finishes, the model processes, the model responds; an interjection stops the model rather than letting it adapt. The most-promised adaptive voice surface, a personalised context-aware Siri, has been announced and repeatedly delayed (TechCrunch, February 2026 — and this connects directly to the Apple Intelligence cautionary case in 26-adaptive-interfaces-foundations §8). Camera input *is* shipped — Apple's Visual Intelligence (iOS 18.2, December 2024) does text capture and translation, object identification, and event creation; Google's Search Live (Project Astra, May 2025) brings continuous live-feed multimodal understanding to Search. The defining requirement is a *grounding step*: the interface must surface what it believes it sees, because misrecognition is otherwise silent and the user has no error signal until it is too late.

### 3.3 Cross-device handoff — the under-solved one

Cross-device continuity matters disproportionately for retail and SaaS clients, and it is where the architectural gap is widest. **There is no single mechanism. There are three incompatible ones.**

The first is **OS-level proximity continuity**, exemplified by Apple's Handoff and Universal Clipboard. These work by *local device-to-device transfer*, not cloud sync: same account, Bluetooth and Wi-Fi on, devices physically near each other, with separate end-to-end-encrypted pairwise connections. The architectural consequence is that this continuity is *ephemeral and proximity-bound* — it passes a live activity state between two nearby devices and breaks when they are apart.

The second is **cloud account sync**, the model behind a retail "save cart across devices" feature. State is persisted server-side and reloaded on login from any device; modern implementations use event-driven architectures to propagate changes across channels in near-real-time. This is the most mature cross-device pattern, and it is mature because the unit being synced — a cart, a list — is a well-defined data structure.

The third is **partial sync**, the model the AI assistants actually use, and the one most likely to surprise. ChatGPT syncs its *memory* across devices but does not sync *live conversation threads* in real time — the desktop app does not refresh an open thread without a restart, and switching devices mid-conversation loses live context. So "AI continuity" today is, precisely, eventual-consistency thread history plus persistent memory — not live session handoff.

The gap this exposes is structural and citable. **There is no cross-vendor standard for handing off an *adaptive or generative UI state* between devices,** and the reason is structural: a generative UI state is not a document — it is a tuple of prompt, context, model output, and render, and nothing standard serialises that tuple. A retailer can sync a cart because a cart is data; nobody can yet sync "the in-progress generated interface you were looking at" because that interface has no canonical, transferable form. **For a client whose customers move between devices mid-task, this is a real constraint to design around, not a solved feature to assume.** The honest engineering answer today is *re-generation from synced context* on the second device, not *transfer of the rendered state*.

### 3.4 Ambient surfaces and the agent as a new entry point

The distinction between ambient/proactive and user-initiated surfaces is architectural: a user-initiated surface is request/response; an ambient surface is event-driven, runs continuously, and surfaces only when a threshold is met. LangChain's *Introducing ambient agents* (January 2025) is the clearest articulation: an ambient surface needs a fundamentally different container — a chat window assumes one active conversation; an ambient system has many concurrent open loops, so the proposed container is an *inbox*, modelled on email and ticketing, with explicit notify/ask/review interaction patterns because the user is not present at the moment of action. **Ambient agents are an emerging pattern with reference implementations, not a mainstream consumer-shipped UI;** the strongest production case is narrow — clinical documentation scribes. (Continuous copilots in Clark & Kindred's framing — Granola, Apple's Notification Summary, Dia's Morning Brief — share the architectural shape.)

One adjacent development changes what surface you are even building for. The agentic-commerce traffic shift documented in 26-adaptive-interfaces-foundations §5 — Adobe's ~693% YoY jump in AI-referred retail traffic, with ~31% conversion premium — has implementation-side consequences. Building "adaptive UI for commerce" now quietly includes building a surface — structured product data, clean semantics, machine-legible product information, a high-quality accessibility tree — that an *agent* can read and act on, not only one a human can see. The good news: the same data layer that makes Rung-4 generation work is what an agent reads. The deterministic, well-structured, semantically-labelled data we are already building for adaptive UI is also what makes the product legible to a buying agent. **The unglamorous middle of the spectrum is also the strategically correct place to invest, and that convergence is the most plausible reason to bet on it.**

---

## Memory and context architecture

An interface can only adapt to what it remembers. Where user state lives is not a back-end detail — it determines what adaptation is possible, what it costs, and what legal obligations attach. The architecture is layered, and the layers trade off volatility against durability and governance load:

```
┌────────────────────────────────────────────────────────────┐
│ Active context window — ephemeral payload sent to model    │
│ ┌────────────────────────────────────────────────────────┐ │
│ │ Semantic memory — vector store (turbopuffer / pgvector)│ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Persistent profile — CDP / profile graph            │ │ │
│ │ │ ┌──────────────────────────────────────────────┐    │ │ │
│ │ │ │ Session-only — local state / sessionStorage  │    │ │ │
│ │ │ └──────────────────────────────────────────────┘    │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
 innermost: cheapest, most volatile, lowest compliance risk
 outermost: most durable, highest latency + governance load
```

### 4.1 The tiers

**Session-only.** State exists for one visit and is discarded. React/Redux state, `sessionStorage`. Trivial, privacy-friendly, shallow. The baseline against which every "memory" feature is defined.

**Persistent profile — the CDP.** A customer data platform unifies known and anonymous data into a single profile usable across channels in real time. Adobe's Real-Time CDP runs personalization at the network edge, evaluating a user's context in milliseconds against a localised edge profile store to avoid round-trips to a central hub. The profile is *structured and human-readable* — attributes, audience memberships, computed traits — which, as 4.3 shows, makes it the most legally tractable place to keep personalization data.

**Vector store — semantic memory.** Past interactions, preferences, and content are converted to embeddings and stored; on a new interaction the system embeds the current context and retrieves the most semantically similar prior items. This is what "semantic memory" means in practice. The relevant property — and the relevant problem — is that an embedding is not human-readable: you cannot read a phone number out of a vector, which sounds privacy-friendly and is in fact the opposite, for reasons in §4.3.

**The context window.** The simplest "memory": the conversation transcript, re-sent to the model each turn. Its limits are severe and routinely understated. The "lost in the middle" effect (Liu et al., Stanford) means models attend well to the start and end of their context and poorly to the middle, with accuracy drops exceeding 30% when relevant information sits mid-context. A 2025 study testing eighteen leading models (Chroma Research) found every one degraded as input grew — a phenomenon now called *context rot* — with effective recall falling well below advertised maximums. **The context window is working memory, not durable memory,** and an architecture that treats a long context as a substitute for a real memory store will quietly lose information.

**Hybrid.** Every shipped consumer memory feature combines the above: a structured store for durable attributes, a vector store for semantic recall, pre-computed summaries injected into the context window for cheap continuity, and the live transcript for the current turn.

### 4.2 How shipped memory features actually work, and what scaling one looks like

The shipped implementations are not what most people assume. ChatGPT's memory is *not* RAG. Independent reverse-engineering by Simon Willison (May 2025) shows it maintains a frequently-updated, structured summary — a dossier covering response preferences, past-conversation highlights, user insights, and interaction metadata — and injects that summary into the system prompt of *every new chat*. There is no retrieval step; the memory invisibly conditions every output, including outputs where the user would not expect it. Claude's memory periodically distils durable facts from conversation history into a synthesised summary and announces when it draws on a memory; its Projects feature auto-loads instructions and documents into every conversation in a workspace. Gemini's personalization is different again — it is retrieval over a *pre-existing* data store (the user's Google account history), used only when the model judges it would help. **Three vendors, three architectures.** A leader should not assume "memory" means one thing.

Notion's vector-search infrastructure is the clearest published worked example of scaling the semantic-memory tier, and the specifics matter. Per Notion's engineering account *Two years of vector search at Notion: 10x scale, 1/10th cost* (February 2026): Notion decoupled storage from compute by moving to **turbopuffer** — a vector database built on object storage — rather than running vector indexes on bundled storage-plus-compute pods; DynamoDB handles intelligent page-state caching; Apache Spark runs offline batch indexing while Kafka consumers handle real-time updates; embeddings were brought in-house, self-hosted on Ray/Anyscale after migrating off external APIs. The reported results are useful for client conversations: roughly **90% cost reduction, 10× capacity scale, query latency cut from 70–100 ms to 50–70 ms, and a 70% reduction in data volume.** The honest counterpoint — the gap between real-time serving and offline processing (memory maintenance, knowledge-graph precomputation, batch flywheels) is still largely unsolved; turbopuffer-class systems make the serving side cheap and scalable, not the whole problem.

### 4.3 The architecture choice is a governance choice

This is genuinely non-obvious, and it should change decisions. Under GDPR's right to erasure, a user can demand deletion of their personal data. **For a structured profile this is tractable:** delete a row. **For a vector store it is hard** — the difficulty is *discovery*, not deletion mechanics: a user's information may have been embedded into vectors created from documents written *about* them, scattering their data in forms no index will surface by name. Deletion is possible but requires deliberate engineering to find every touchpoint, de-index the vectors, and propagate through backups. **And for data baked into model *weights* through fine-tuning, erasure is effectively unsolved** — *machine unlearning* research through 2025 (arXiv 2505.23270, *Does Machine Unlearning Truly Remove Knowledge?*) repeatedly found that unlearning does not truly remove knowledge from a trained network.

The architectural rule that follows is concrete and should be stated to any client fine-tuning on user data: **never let raw personal data enter training data; keep personalization in retrievable, deletable stores** — a profile database, a vector store you control — not in weights. The same logic argues against the ChatGPT-style "remember everything" dossier: under GDPR's data-minimisation and purpose-limitation principles, broad capture is harder to defend than scoped capture.

The regulatory perimeter has other non-obvious edges. California's finalised CCPA/CPRA regulations govern "automated decisionmaking technology" but the definition is *narrow* — it covers technology that *replaces or substantially replaces* human decision-making in *significant* decisions (finance, housing, employment, healthcare, education) and *explicitly excludes advertising* (Skadden, October 2025). The consequence: most adaptive-UI personalization — layout, content, recommendations — falls *outside* that regime, but an adaptive UI that gates a loan application or a job flow pulls the entire system into scope. The EU AI Act's Article 50 transparency obligations, fully applicable from 2 August 2026, break into three provisions a design team must hold separately:

- **Article 50(1) — direct interaction.** Users must be informed they are interacting with an AI system, unless that is obvious to a reasonably well-informed person. For an AI helpdesk or assistant: a persistent label or clear disclaimer.
- **Article 50(2) — synthetic content.** AI-generated text, audio, image, or video must be marked in a machine-readable format so it is detectable as AI-generated. **An open and consequential interpretive question: does this attach to an AI-*generated interface*, not just AI-generated media?** No published regulator guidance settles this as of May 2026.
- **Article 50(4) — public-interest text.** AI-generated text published to inform the public on matters of public interest must be disclosed as artificially generated, unless it underwent human editorial review.

(See 26-adaptive-interfaces-foundations §7 for the manipulation regime under Article 5, and 25-ai-aware-patterns-and-conversational-ui §7 for the chatbot-side breakdown.)

Finally, **data residency is no longer free.** Anthropic prices US-only inference at a roughly 1.1× multiplier; regional cloud endpoints carry roughly a 10% premium. Every adaptive render that ships personal context to a model API is therefore both a compliance decision and a measurable line item. The memory architecture is chosen by engineers, but it writes the privacy, residency, and portability story the legal and design teams will have to live with — **it should be a deliberate, cross-functional decision, and it rarely is.**

---

## Streaming UI as a primitive

Most teams still hold a binary mental model of UI: it is either rendered or it is not, and the gap between is a spinner. Progressive UI materialisation — interfaces that become visible and usable *while they are still being generated* — breaks that model, and it is novel enough to deserve treatment as a design primitive in its own right.

```
Traditional:  [blank] ─────────── wait ─────────── [fully rendered]

Streaming:    [blank] → [skeleton] → [partial cards] →
              [streaming content] → [hydrated + interactive]
```

### 5.1 What it is

Three technical layers underpin streaming UI. **Token streaming plus partial structured output** — because a model emits tokens sequentially, a stream of progressively-completing, schema-valid objects can be exposed to the renderer (the AI SDK's `streamObject` and `partialObjectStream`). A telling refinement: AI SDK 3.4 added a mode that streams *complete objects* rather than individual tokens, specifically because token-level partials produced layout shift — even the streaming primitive moved toward more structure. **Server-side component streaming** — React Server Components serialise a component tree over a chunked response, with Suspense boundaries declaring which subtrees may be deferred, so the server flushes each subtree as it resolves, out of document order. **Optimistic rendering** — paint the expected end-state immediately, reconcile when the real data arrives.

### 5.2 What it looks like, shipped

The pattern is now visible across every major AI product. Anthropic's Artifacts render generated code and documents live, in a side-by-side panel, inside a sandboxed iframe with strict content-security policies. Anthropic's *Live Artifacts* (April 2026) extended this to persistent, auto-refreshing dashboards that re-pull current data on open. ChatGPT Canvas opens an editable document beside the chat, edits it in place, and exposes a diff view and version history. Gemini Canvas creates collaborative documents including code files that you can preview and run inline (Clark & Kindred, 2026, Ch 6 — the *Severance office* example). v0 streams JSX into a live preview while a post-processor scans for errors during generation. GitHub Copilot renders dimmed "ghost text" inline as the user types. **The shared shape is unmistakable: generation is something the user *watches*, and increasingly something they can *edit alongside* and *interrupt*.**

### 5.3 What it changes

Streaming UI changes three things about interaction.

It changes **latency tolerance.** The perceived-performance literature is consistent in direction: visible progress makes identical wait times feel shorter — skeleton screens are perceived as faster than spinners. (The specific percentages that circulate — "20% faster," "300ms" — are hard to trace to primary studies and should be cited as direction, not magnitude.) The principle transfers directly: a streamed reasoning trace or progressively-materialising layout buys a multi-second generation budget that an opaque spinner would never be granted.

It changes **interaction expectations.** Streaming reframes generation as a process the user observes and can abort — which is why every one of these products has a "Stop generating" control. The user is no longer waiting for a result; they are watching one form, and may decide early that it is not the one they wanted.

It changes the **visual language of "in progress."** "Pending" and "partial" become first-class UI states with their own vocabulary: skeletons and shimmer, token-by-token text reveal, staged Suspense-driven reveals where independent regions appear out of order as they resolve, and — newly — *reasoning traces shown as UI*, the collapsible "thinking" panels that turn latency into transparency. Linear's *Agent Interaction Guidelines* (July 2025) codify this into six published principles including explicit state transparency and disclosure of agency. **Diff-streaming**, where changes arrive as an accept/reject diff rather than a silent replacement, is becoming the default for anything that edits existing content.

### 5.4 The design consequence

The deepest consequence is for what a designer is designing. **The unit is no longer "the finished screen." It is the screen's *trajectory* through partial states** — empty, skeleton, partial, streaming, complete, and (with live artefacts) re-streaming on refresh. A component must be valid and legible at every intermediate state, not only at completion. This is a genuine expansion of the design surface, and it is the clearest example in this file of an implementation reality that most design practice has not yet absorbed: the binary mental model is wrong now, and a design system that only specifies end-states is specifying a fraction of what ships. (See §9 below for the design-system implications.)

---

## Evaluation, QA, and governance

If the interface is generative, you cannot review every state — the set is unbounded or at least uncountable. The traditional model of design QA, a designer signing off on every screen, does not degrade gracefully here; it breaks. The replacement is borrowed wholesale from machine-learning evaluation, is genuinely shipping at some companies, and is **immature in exactly the place that matters most to a design-systems leader.**

### 6.1 Eval-driven development replaces screen-by-screen QA

Anthropic's published methodology is the most rigorous available primary source, and its structure is now widely shared (Grace, Hadfield, Olivares, De Jonghe, *Demystifying evals for AI agents*, January 2026). It uses three layers of grading: **code-based graders** (deterministic checks — does the output parse, do imports resolve, does a static accessibility scan pass), **model-based graders** (an LLM judging subjective dimensions against a rubric), and **human graders** (the gold standard, used to calibrate the LLM judges rather than to review everything). Golden datasets are built incrementally — start with twenty to fifty tasks drawn from real observed failures. **Evals check *outcomes* — the final state — rather than asserting intermediate steps.** Non-determinism is measured rather than wished away, with metrics like `pass@k` (succeeds in k attempts) and the stricter `pass^k` (succeeds in all k). The overall posture is a "Swiss cheese" model: automated evals, production monitoring, A/B testing, user feedback, and manual transcript review, each layer catching what the others miss.

In practice an eval is a config-plus-assertions file run in CI as a quality gate, comparing outputs across models and prompt versions:

```yaml
# promptfooconfig.yaml
prompts:
  - "Generate an interactive dashboard layout for: {{userInput}}"
providers:
  - openai:gpt-5.4
  - anthropic:claude-sonnet-4.6
tests:
  - vars: { userInput: "Track quarterly SaaS subscription metrics" }
    assert:
      - type: is-json                       # valid JSON syntax
      - type: javascript                    # required layout blocks exist
        value: |
          const d = JSON.parse(output);
          return d.charts?.length >= 2 && d.hasOwnProperty('summary');
      - type: llm-rubric                    # LLM-as-judge on subjective quality
        value: "Layout is coherent, on-brand, and free of formatting errors"
```

The tooling is real and largely generally available: Anthropic's developer console eval tool, OpenAI Evals (open-source framework plus platform product), Braintrust (used by Notion), LangSmith and Langfuse, DeepEval, Ragas (the standard for RAG evaluation), and Inspect from the UK's AI Security Institute. **One market event belongs here: OpenAI acquired Promptfoo, the leading open-source LLM evaluation and red-teaming tool, announced 9 March 2026** (corroborated by OpenAI and Promptfoo announcements and contemporaneous press). It is a meaningful consolidation signal — a frontier lab absorbing the open-source eval layer that production teams had been treating as neutral infrastructure. Teams standardising on Promptfoo should treat its independence as a question, not an assumption.

The gap a design leader must not miss: **none of these frameworks is purpose-built for generative UI.** They evaluate text and agent outputs. Teams building generative interfaces adapt them by treating rendered output — generated code, a component tree, a DOM — as the artefact to grade. It works, but the QA infrastructure for adaptive UI is a retrofit, not a native tool.

| Evaluation layer | Tooling | Objective | Honest status |
|---|---|---|---|
| Schema validation | Zod / Valibot / `is-json` | Output matches the layout/data contract | Solved; deterministic |
| Semantic consistency | LLM-as-judge / embedding similarity | Output matches intent and system instructions | Workable; ~85% judge-human correlation |
| Security / red-team | Promptfoo red-team, injection suites | No prompt-injection or data-leak paths | Maturing |
| Operational telemetry | OpenTelemetry GenAI conventions | Tool-success rate, latency, user resets | Workable; spec still experimental |
| **Accessibility** | **axe-core / Pa11y in-pipeline** | **WCAG conformance of generated output** | **Partial — see §6.2; not solved** |

### 6.2 The weakest link — accessibility QA at scale

This is the most important correction in this file because one source draft from the dual-agent run got it flatly wrong. Accessibility QA for generative UI is **not** solved by running axe-core in CI, and presenting it as a "zero critical violations" checklist item misrepresents the state of the art.

The evidence is unambiguous. **Automated accessibility tools catch roughly 25–40% of WCAG violations**; the remaining 60–75% requires manual review with humans and assistive technology (Deque Systems and TestParty analyses, 2025). Stricter analyses are harsher: by one assessment only about **13% of WCAG criteria can be reliably flagged by automated scans, and roughly 42% cannot be detected by automation at all** — they require evaluator judgment (Accessible.org, 2025). The baseline before variability is bleak: **the WebAIM Million 2026 analysis found 95.9% of the top one million home pages have detectable WCAG 2 A/AA failures, averaging 56.1 errors per page** — *static* UI failing the bar at scale. WCAG 3.0 will make this harder, not easier: it introduces qualitative and percentage-based tests explicitly designed to require human judgment. axe-core is the industry-standard tool *within* the automation ceiling — excellent at what it covers — but it does not solve the problem.

For generative UI this compounds: when every render differs, you cannot pre-scan every screen. Running axe-core against each generated DOM inside the pipeline, as a code-based eval gate, is the right move — but it inherits the automation ceiling. **It catches the 25–40%, not the rest.**

This produces a real strategic tension worth stating to clients directly rather than hiding. **The foundations file establishes that the single strongest, best-evidenced use case for adaptive UI is accessibility — ability-based design, the Gajos lineage. This file has to report that the QA infrastructure to verify accessibility is least mature exactly for the variable-surface case.** Adaptive UI's most defensible use case is also the one where you can least automatically confirm it is working. This is not a reason to avoid the work — it is a reason to scope it correctly: budget for ongoing manual accessibility testing with assistive technology as a standing cost of any generative-UI engagement, treat automated scanning as a floor rather than a finish line, and do not let a green CI check stand in for an accessibility guarantee. (See 14-accessibility on the four-layer architecture; 16-mobile-accessibility-implementation on framework-level; 17-accessibility-annotation-contract on what designers should be specifying so engineers can implement faithfully.)

### 6.3 Human-in-the-loop, telemetry, red-teaming

*Human-in-the-loop review at thresholds* — escalating to human review only when an automated check flags risk or confidence is low — is well-articulated in research as "oversight-by-design" but thinly documented in production with concrete numbers; specific threshold configurations are rarely published. Notion's runtime guardrails are a shipped example: higher-risk agent actions trigger pop-up confirmations and, during execution, sensitive mutations (deleting database items, sending external email) halt for explicit owner confirmation.

*Telemetry* becomes the primary post-ship signal. Notion has said roughly 80% of its AI team's work is driven by feedback and traces (Sachs, via Braintrust, 2025). The signal taxonomy is worth knowing: **explicit feedback** (thumbs, ratings, bug reports) and **implicit feedback** (abandonment, query reformulation, time-on-answer, and *regret signals* — a user editing every output despite a thumbs-up reveals a trust gap an explicit rating missed). The instrumentation layer is being standardised through OpenTelemetry's GenAI semantic conventions, though that spec is still marked experimental.

*Red-teaming* is comparatively mature. Promptfoo generates adversarial inputs by vulnerability class and reports against frameworks like the OWASP LLM Top 10. Microsoft's *Lessons from Red Teaming 100 Generative AI Products* (January 2025) is the definitive published account, with the central lesson that testing has shifted from the model alone to the *whole system*. **For adaptive UI specifically, red-teaming now has to cover the second manipulation vector** documented in 26-adaptive-interfaces-foundations §7.3 — LLM agents are hypersensitive to choice-architecture nudges and option injection, so an adaptive system that retrieves and acts on external content must red-team the *retrieval and option surface*, not only the prompt. The Cherep, Maes & Singh result and the Liou et al. *OI-Bench* benchmark are operational findings, not theoretical concerns.

The **critic / evaluator / ensemble** triad is the internal-architecture response Clark & Kindred surface in Ch 11. *Critic models* (e.g., OpenAI's CriticGPT) are prompted to act like editors and look for flaws, inconsistencies, fuzzy reasoning. *Evaluator models* (e.g., DoorDash's customer-service response auditor) score or classify output against a checklist, issuing good/bad/uncertain judgments. *Ensemble methods* compare answers across multiple models or runs — convergence is a confidence proxy; disagreement is a red flag. The book pairs each with a UI pattern: **thermometer** (visualise high/medium/low confidence), **citation** (connect generated claims to sources — Perplexity is the canonical instance), and **consensus meter** (visualise agreement across sources or models — Consensus.ai for science papers; the same pattern works for LLM ensembles). We adopt all three with attribution.

### 6.4 Governance under-formalisation

The governance shift the foundations file anticipated — from "did we follow the design system" to "did the system produce acceptable outcomes" — is real as a direction of travel and **under-formalised as practice**. No design-system-specific, outcomes-based governance framework has been published. Governance for generative UI is currently assembled from general AI-governance practice plus eval and red-team tooling. Two companies have published enough to learn from — Notion in detail (an "AI Data Specialist" role blending QA, prompt engineering, and product thinking; regression evals against prior models; frontier evals for new ones), and Vercel on eval-driven development for v0 specifically. Two foundations-paper exemplars — Linear and Granola — have published little on how they QA their AI features. **That silence is itself a finding: the operational discipline of QA-ing generative UI is being practiced ahead of being documented, and a buyer should be skeptical of any vendor who describes their evals but cannot show them.**

The governance gap our practice can fill — and should — is **variant logging as default infrastructure** (foreshadowed in 26-adaptive-interfaces-foundations §7.5). EU Article 5 enforces on *effect*, and the only credible defence is the ability to demonstrate, post hoc, which generated variants were surfaced to which user and why. No vendor has published a reference implementation. The deliverable is concrete: what is logged, who holds it, who can audit it, retention. This is a real opportunity. (See 07-governance-and-adoption on the broader governance framing.)

---

## Cost, latency, and performance reality

Adaptive UI runs on tokens, and tokens cost money and time. **This is the layer design conversations ignore most completely, and ignoring it produces business cases that collapse on contact with a finance review.**

### 7.1 The token cost model and how it compounds

Current per-million-token pricing for the frontier and mid-tier models, as of May 2026, spans a wide range. Anthropic: Claude Opus 4.7 ≈ $5 in / $25 out, Sonnet 4.6 ≈ $3 / $15, Haiku 4.5 ≈ $1 / $5. OpenAI: GPT-5.5 ≈ $5 / $30, GPT-5.4 ≈ $2.50 / $15, with Mini and Nano tiers far below. Google: Gemini 3.1 Pro ≈ $2 / $12, Gemini 2.5 Flash ≈ $0.30 / $2.50, Flash-Lite lower still. **These figures move; the *ratios* are the durable insight.**

Here is the compounding, made concrete. Take one modest adaptive render: 4,000 input tokens (system prompt, user profile, retrieved context) and 1,000 output tokens. At ten renders per session and one million sessions per month: about **$37,000 per month on Gemini 2.5 Flash and about $450,000 per month on Claude Opus 4.7**. **Model choice swings cost by roughly twelve times for an identical user experience.** That single fact should be in every adaptive-UI business case and almost never is.

A complementary per-day frame: one million interactions per day at 4,000 input + 500 output tokens, at a mid-tier $2.50/$10 per-million rate, runs about **$15,000 per day** in inference. Either framing, the lesson is the same: per-render generation at consumer scale is a six-to-seven-figure-monthly line item, and the model decision dominates it.

### 7.2 Latency budgets

The interaction-design thresholds are old and stable: under ~200 ms feels instant, under ~500 ms feels responsive, beyond ~1 s is noticed, beyond ~2 s frustrates. Generative UI runs straight into them. A full model completion commonly takes 2–8 seconds; a reasoning model can take 45–120 seconds merely to *begin* responding. **A generative UI that blocks first paint on a full completion violates the interaction budget by an order of magnitude.** There are only three ways out, all from §5: stream (so the user sees progress and the budget that matters becomes time-to-first-token), render optimistically or with skeletons (so something appears immediately), or pre-compute (so the common cases were generated in advance).

One contrarian note worth holding lightly: at least one vendor study suggests a *slightly* slower agent response can read as "more thoughtful" — latency perception is not perfectly linear — but this is a single study and should not be built on.

### 7.3 Caching and model choice

**Caching is the main lever, and its realities are less rosy than vendor copy.** Exact-match caching (key on a hash of the prompt) catches only a small fraction of redundant calls (one analysis put it near 18%) because users rephrase. Semantic caching — embed the query, retrieve a cached response if similarity clears a threshold — does better, but realistic production hit rates land in the 20–45% range, not the 95% sometimes claimed; FAQ-style traffic reaches the higher end. **Provider-side prompt caching is the most reliable win:** it caches a stable *prefix* of the prompt, and the discounts are real — OpenAI prices cached input at roughly half, Anthropic prices a cache *read* at about a tenth of the base input rate. The design-relevant consequence is concrete: **order the prompt so the *stable* parts come first** — system instructions, design tokens, component schemas — and the *volatile* per-user context comes last, so the stable prefix hits the cache on every request.

On model choice: not every render needs a frontier model. Across enterprise workloads, only an estimated 25–35% of queries genuinely require frontier capability. Two patterns exploit this: *routing* (send each query to one appropriately-sized model) and *cascading* (try a small model first, escalate only if its output fails a quality bar). Reported savings run 45–85% with most of the quality retained. Notion has described doing exactly this in production — routing by task category, sending long-form reasoning to frontier models while high-volume tasks like database field auto-population go to small, fine-tuned, cost-efficient ones (*Speed, Structure, and Smarts: The Notion AI Way*, May 2025).

**The strongest cost lever for adaptive UI specifically is the one a designer controls:** *do not generate UI when you do not have to*. Pre-compute and template-cache the common layouts; reserve live generation for the genuinely novel states. **An adaptive interface that generates every surface from scratch is not sophisticated — it is unbudgeted.**

---

## Authoring tooling and the design workflow

When the output is not a fixed screen, what does the design tool look like? **The honest answer, stated plainly because the brief asked for honesty: there is no mature design tool for variable output, and every current approach is a workaround.** Designers still author fixed artefacts; the generative layer is bolted on afterward.

### 8.1 The current workarounds

**Figma plus prompts.** Figma announced its AI suite in mid-2024; the layout-generation feature was suspended shortly after launch when it produced output strikingly close to an existing Apple app. Figma Make, a prompt-to-code tool, reached general availability in July 2025. Its limits are admitted: the exported code is not tied to a production design system, it is commonly described as non-production-grade, credit limits cap iteration, and once a user makes a manual edit, prompt-based editing breaks. Most important: **Figma Make generates a *fixed prototype per prompt*. It is a faster way to produce one artefact. It is not a tool for designing a system that renders variably.** (See 12-figma-practice for the broader Figma practice context.)

**Storybook plus an eval suite.** This is the most credible *component-driven* generative workflow shipping today. Storybook now positions itself explicitly for AI agents: components, props, stories, and docs define what an agent is allowed to build; Storybook's test runner executes generated stories in a real browser and sends failures back to the agent to fix; an MCP add-on exposes the design system to agents as a set of selectable, documented tools. This is genuinely useful — it makes Storybook both a *constraint* (reuse real components) and a *feedback loop* (tests as evals). **But note what it governs: which components an agent uses. It does not help a designer specify and review variability.**

**v0-style prompt-to-UI tools.** v0, Lovable, Bolt, and Replit Agent generate UI or whole apps from prompts. They are real and useful for prototyping. Their shared shortfall for design teams is what practitioners call the **"70% problem"**: users hit a complexity ceiling and must drop into hand-editing code, and the tools are single-shot generators of fixed artefacts, not authoring environments for variable systems.

### 8.2 The component-prompt pair as the emerging artefact

The genuine new artefact emerging is a **component bundled with a machine-readable description of when and how to use it** — code, schema, and semantic prompt as one atomic unit:

```typescript
export const InfoCard = {
  component: InfoCardReact,
  schema: z.object({
    title: z.string(),
    body: z.string(),
    severity: z.enum(["info","warning","error"])
  }),
  semanticPrompt:
    "Use to surface a single alert, warning, or short text summary. " +
    "Not for primary content or multi-field data — use DataPanel for that.",
};
```

A model queries a catalogue of these to know what is available and how to populate it. The book's worked example in Ch 6 — the city-tour application's UI-component catalogue inside the system prompt — is the same pattern at sketch fidelity. **No design tool authors this pairing as a first-class object;** the "prompt/spec" half is improvised in code or markdown today. We see this as a real opportunity for our practice — the artefact is concrete and authorable, and a Prism2 extension that ships the pairing for our component library would be a defensible differentiator. (See 03-component-library on components-as-data, 04-documentation on the docs side, and 15-ai-in-ds on the operator-side architecture this builds on.)

### 8.3 The unsolved problem — designing for variability

Designing for variability is genuinely unsolved, and the clearest vocabulary for it comes not from industry but from academic HCI. A recent systematic review names it **"variability by design"** and describes the shift it demands — a designer moves from *visual authorship* (drawing the screen) to **architectural intent** (specifying modular components, behavioural rules, and interface policies, and letting the system compose) (Lee, *Towards a Working Definition of Designing Generative User Interfaces*, arXiv 2505.15049 / DIS '25 Companion). What is missing is the tool. **No design tool lets a designer specify a *space* of possible outputs and review the *distribution* of what that space produces.** Review today is sampling individual generations by eye — which, for an unbounded output space, is closer to spot-checking than to QA.

The academic field has at least identified the missing review primitive: **UICrit**, a UIST 2024 dataset of professional design critiques over hundreds of mobile UIs (Duan et al., arXiv 2407.08850), was explicitly proposed as a reward model for evaluating generated interfaces — the kind of automated-critique infrastructure that practitioner tooling does not yet have. Chen et al.'s *Generative Interfaces for Language Models* (Stanford, arXiv 2508.19227, 2025) is the strongest published contribution on *how to evaluate* generative UI multidimensionally.

A leader should budget and plan with this gap in full view: the design workflow for adaptive UI is currently code-first, with designers participating through prompts, component contracts, and the eval loop rather than through a canvas. **That may change. It has not changed yet,** and a 2026 client engagement that assumes a Figma-like authoring tool exists for variable interfaces is mis-scoped.

---

## Design system implications

26-adaptive-interfaces-foundations §10 argues the design system survives the shift to adaptive UI and becomes *more* load-bearing, not less. The implementation reality bears that out, and sharpens it into four concrete shifts. **This is where our practice's core capability lands.**

**1. Primitives over composed components.** The industry has moved decisively toward headless primitives, and the move is partly driven by what LLMs compose well. Radix UI and, especially, shadcn/ui — primitives plus Tailwind, distributed as copy-paste source rather than an installed package — have become, in one analyst's phrase, *the default UI library of LLMs*, and v0, Bolt, and Lovable all build on that base (Holterhoff, RedMonk, April 2025). The reason is mechanical: **when the model can see and shape all the code, it composes more reliably than when it must work through the fixed API and theming constraints of an opinionated library.** The implication for a design system is clear — a system architected as a closed catalogue of heavily-composed components (the MUI model) is *less* adaptable to LLM composition than one architected as open, primitive-level, fully-visible code (the headless / Tailwind / shadcn model). (See 03-component-library on the component model and 22-token-architecture-extensions on the token-side architecture this assumes.)

**2. Semantic component contracts.** For an LLM to select a component, the component must describe *what it does* — its intent, the context it needs, its alternatives — not merely how it looks. **This is the "intent metadata" the practice has been building toward.** Each component should expose:

- A precise JSON Schema for its required inputs and property types.
- A semantic description explaining its visual purpose, layout expectations, and proper usage context.
- A set of accessibility and spacing rules the renderer enforces during composition.

The mechanism is emerging through MCP — tool selection mediated by natural-language descriptions interpreted at inference time — and Storybook's MCP add-on is the concrete shipped example of a design system exposed to agents as documented, selectable tools. **There is no ratified standard for component intent metadata yet.** Building toward one — even informally, as structured descriptions attached to each component — is the highest-leverage design-system investment for adaptive UI. (See 04-documentation on the four-layer AI documentation stack — tokens with descriptions, `.ai.json` plus registry, agent-instructions files, the Figma pipeline — that this layer extends; and 15-ai-in-ds on the components-as-data thesis underneath.)

**3. Evals replace screen-by-screen QA.** Covered in §6 above. Continuous automated evaluation as the QA function, with humans calibrating the judges rather than reviewing every screen. **The practice gap is a deliverable category for AI evaluation infrastructure** (test sets, automated checks, telemetry-driven detection of issues, accessibility verification on variable surfaces). This is genuinely new work, and it is exactly where our DS practice can lead — six to nine months of focused investment, through real client work plus targeted hires, closes the gap. The tooling (Promptfoo / OpenAI Evals / Anthropic's eval frameworks) is mature and rapidly improving.

**4. Governance shifts from compliance to outcomes.** The question moves from *"did this screen follow the system"* to *"did the system produce an acceptable outcome."* This is a real change in what governance *means*, and — as §6.4 noted — it is under-formalised; no purpose-built framework exists. The implementation notes that follow stand: the system prompt becomes a versioned, reviewed design artefact (Linear's "Additional Guidance" surface is the production exemplar), and **variant logging becomes infrastructure** — a record of which generated variant was served to which user, and why — both for debugging and for the auditability the EU AI Act's effect-based enforcement will eventually require. **No vendor has published a good reference implementation of variant logging.** That is a genuine gap, and it is the place we can lead. (See 07-governance-and-adoption on the governance framing.)

**The synthesis: the components stay consistent; the compositions vary, within rules the design system encodes; "consistency" comes to mean *the user can predict and trust the surface they see* rather than *every user sees the same surface*.** The design system does not shrink. It moves *up* a level — from specifying pixels to specifying the space of acceptable outcomes — and that is more demanding work, not less. (See 25-ai-aware-patterns-and-conversational-ui §7 on the parallel pattern set the DS ships to consumers, and the way variant-logging infrastructure underwrites both that file's chat patterns and this file's adaptive surfaces.)

---

## Where this might be headed *[speculative]*

Everything in this section is labelled speculation because it is.

*[speculative]* **The middle of the spectrum stays where the work is.** Rungs 3–4 — slot-based generation, structured output rendered by deterministic components — remain the dominant production shape for the next two to three years. Runtime code generation (Rung 5) does not become a mass-market pattern in that window because the QA, cost, latency, and safety problems are not close to solved and the constrained patterns keep working well enough.

*[speculative]* **An interop standard consolidates — but which one is genuinely open.** MCP and its UI extensions, AG-UI, A2UI, and the AI SDK's `message.parts` are the contenders. Some convergence on a wire format for "a model produced something that should become UI" is likely within two to three years, because the fragmentation is expensive for everyone. Betting on the *winner* now is premature; tracking the race is not.

*[speculative]* **The authoring-tool gap gets filled — or it doesn't, and that is itself the answer.** Either someone ships the missing tool — one that lets a designer specify a variability space and review the distribution of its outputs — because the gap is too obvious to leave open, or the workflow stays permanently code-first and the design role reshapes around prompts, contracts, and evals rather than a canvas. The second is the current trajectory, and trajectories are sticky.

*[speculative]* **Falling token prices weaken the economic objection to live generation without removing it.** Model prices have fallen steadily, and a render that costs a fraction of a cent today may cost a tenth of that in two years. That makes more live generation affordable. It does not touch the QA, accessibility, and governance costs, which are human and structural and do not fall with token prices. The economic case for pre-computing and caching common layouts survives even cheap tokens.

*[speculative]* **Recommendation practice and generative practice converge at the layout level.** The fifteen-year-old, bandit-driven personalization stack and the new generative stack are converging — first on content, increasingly on *layout*. Spotify Research's *Prompt-to-Slate: Diffusion Models for Prompt-Conditioned Slate Generation* (RecSys 2025) is a leading indicator. Expect the incumbent personalization vendors (Adobe, Optimizely, Sitecore) to ship layout-generation primitives, and expect the resulting systems to look like Rung 3–4 with a recommendation engine doing the selection.

*[speculative]* **Agentic commerce compounds.** If the trajectory in 26-adaptive-interfaces-foundations §5 holds, a meaningful share of retail discovery becomes agent-mediated within a couple of years, and *"build a surface an agent can read and act on"* becomes a named implementation discipline alongside *"build a surface a human can see."* The deterministic, well-structured, semantically-labelled data layer — the same one that makes Rung-4 generation work — turns out to also be what makes a product legible to a buying agent. **That convergence is the most plausible reason the unglamorous middle of the spectrum is also the strategically correct place to invest.**

*[speculative]* **Regulatory enforcement of EU Article 5 against a high-profile adaptive-UI deployment lands within 2–3 years** and pushes variant-logging infrastructure toward being a default. We should be ready to ship variant-logging primitives before the enforcement arrives, not after.

What is **hype**: that "AI will design the interface" describes Rung 5 at runtime, which this file has shown is nearly empty in production; that design systems become irrelevant — they become the load-bearing constraint. The durable shape is less dramatic and more buildable: deterministic shells, constrained generation inside them, evals where QA used to be, and a design system doing more work than ever.

---

## Open questions

1. **Will an interoperability standard consolidate, and which one?** MCP / MCP Apps, AG-UI, A2UI, and `message.parts` are competing informally. If fragmentation persists, every adaptive-UI project pays an integration tax indefinitely; if one wins, the timing of that win is a real strategic variable.

2. **Is accessibility QA at scale solvable with current tooling, or does it need something new?** In-pipeline DOM scanning inherits the automation ceiling (25–40%). Whether generative UI can ever meet the accessibility bar that is its own strongest justification is the most important unresolved question in this file.

3. **What does good variant logging look like?** The foundations file flagged this; the implementation research confirms that no vendor or industry body has published a reference design — what is logged, who holds it, who can audit it, how long it is retained. The EU AI Act's effect-based enforcement will eventually demand it. The deliverable is concrete and available to the practice that builds it first.

4. **Does the authoring tool get built?** Section 8's gap is real and unfilled. Whether it is a fillable gap — whether *"specify a variability space and review its output distribution"* is even a coherent tool concept — or whether the design role simply migrates into the code-and-eval workflow is unresolved, and the answer reshapes the design profession either way.

5. **Can generative UI state be made portable across devices?** §3.3's cross-device gap traces to a serialisation problem: a generative UI state is a prompt-context-output-render tuple with no canonical transferable form. Whether anyone defines such a form — or whether cross-device adaptive UI is simply re-generated from synced context on each device — is open, and it matters most for exactly the retail and SaaS clients who care most about continuity.

6. **How much does the cost curve actually change the architecture?** If tokens get cheap enough, does the spectrum's centre of gravity drift toward Rung 5, or do the non-token costs (QA, accessibility, governance) hold it in the middle permanently? This file bets on the latter, but it is a bet.

7. **Does the OpenAI–Promptfoo acquisition reshape the eval layer?** A frontier lab now owns the leading open-source eval and red-team tool. Whether that accelerates the eval layer or compromises its perceived neutrality is an open governance question for any team standardising on it.

8. **Should our practice ship variant logging as a Prism2 extension?** §6.4 and §9 both suggest yes. The design and engineering work is non-trivial but not blocked by external dependencies. Worth deciding rather than letting it emerge.

---

*Provenance: This file is the implementation companion to 26-adaptive-interfaces-foundations and is synthesised from the same dual-agent research run (`_research/_inbound/2026-05-21-adaptive-ui-implementation/` plus the per-track synthesis at `_research/_synthesis/2026-05-21-adaptive-ui-implementation.md`) and the Clark & Kindred *Sentient Design* book read at `_source-text/sentient-design-2026/`. The book contributes vocabulary and the four-postures-and-fourteen-patterns scaffold (used here for the call-and-response prompt example, the critic / evaluator / ensemble triad, the thermometer / citation / consensus meter UI patterns, and the system-prompt-as-design-artefact framing); it is light on engineering depth, which the dual-agent run carries (the five-rung spectrum, integration patterns, memory architecture and GDPR consequences, streaming primitive technical layers, eval methodology, cost modelling). All architectural and engineering claims are dated to May 2026 and are platform-state-dependent. Specific platform claims (Vercel AI SDK 5/6 status, OpenAI Apps SDK preview, Anthropic Live Artifacts, Notion turbopuffer, OpenAI Promptfoo acquisition March 2026) and per-million-token pricing reflect publicly verifiable state at synthesis time and will change; verify against primary sources before client-facing recommendation. The accessibility QA correction in §6.2 was the cleanest factual error in either source draft and inverts a comfortable assumption — automated tools catch only 25–40% of WCAG violations, axe-core in CI is a floor not a finish line, and adaptive UI's strongest evidence base (Gajos, Wobbrock — covered in 26-adaptive-interfaces-foundations §4.1 and 14-accessibility) is also its hardest property to verify once the surface is variable. The Notion vector-search infrastructure depth (90% cost reduction, 10× scale, turbopuffer) is from Notion Engineering's *Two years of vector search at Notion* (February 2026); the figures are vendor-published and the corroborating Zilliz analysis flags the real-time-vs-offline gap as still unsolved. The OpenAI–Promptfoo acquisition (9 March 2026) is corroborated across multiple primary sources. Where the two original agent passes disagreed, verification against primary documentation decided — the verification, not the prose quality, was load-bearing every time. See 26-adaptive-interfaces-foundations for the empirical, regulatory, and practice-positioning material this file does not duplicate.*

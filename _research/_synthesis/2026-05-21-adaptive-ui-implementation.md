# Implementing Adaptive Interfaces: Architecture, Operational Reality, and Design Systems Strategy

*A senior design-systems leader's survey of how adaptive and generative UIs actually get built — for web and mobile. Synthesis edition — May 2026.*

---

## Preface — How to read this

This is the companion to the foundation paper. Where that paper covered *what and why* — the lineages, the personalization-versus-adaptation distinction, the evidence base, the ethics — this one covers *how it actually works*: architecture, design decisions, operational reality. It is the same kind of document — a long-form analytical essay, weighted to shipped reality, speculation labeled `*[speculative]*` — and it is written for someone who needs to have informed strategic conversations about this work without building it personally.

This edition is a **synthesis**. It integrates two independent research passes and applies a round of verified corrections. That process mattered here more than in the foundation paper, because implementation claims — versions, prices, acquisitions, infrastructure — are exactly where confident-but-wrong and hedged-but-incomplete both do real damage. Three corrections in particular reversed or sharpened a claim in one of the source drafts; they are folded in below and called out in the closing "What surprised you" section.

Three things to flag at the top:

1. **The generative end of the spectrum is nearly empty in production.** The vivid demo — an AI writes a fresh interface for each user, each request — describes almost nothing that ships to consumers on web or mobile. Tools like v0 are *build-time* tools used by developers, not runtime systems serving model-authored code to end users. Every credible production "adaptive UI" sits well short of that. The action is in the middle of the spectrum, and the middle is more buildable than the pitch.

2. **The architecture that named "generative UI" is in an ambiguous state — not dead, not the standard.** Vercel's AI SDK RSC, which introduced streaming-React-components-from-the-model in 2024, is officially marked experimental in Vercel's own documentation ("we recommend using AI SDK UI for production"), has a published RSC-to-UI migration guide, and a GitHub discussion confirming RSC development is paused. But it was also extracted into a dedicated, maintained `@ai-sdk/rsc` package in v5 (July 2025), and `streamUI` still exists. Treat it as *experimental, officially deprioritized for production, with a published migration path — maintained, not removed.* Production work has moved to the typed `message.parts` model; the RSC approach is a maintained side road, not the highway and not a ruin.

3. **There is no design tool for this.** Designing a fixed screen has Figma. Designing a system that renders differently every time has nothing mature — no tool lets a designer specify a space of possible outputs and review the *distribution* of what comes out. The workflow is patched together from Figma, Storybook, prompt-to-code tools, and code. Section 8 does not pretend this is solved.

A note on method: where the two research passes disagreed, verification against primary sources decided. The polished pass and the hedged pass were each right about things the other got wrong. Polish is not evidence; hedging is not rigor.

---

## 1. The decision-tree-to-generative spectrum

"Adaptive UI" is not one architecture. It is a spectrum, and the most common analytical error — made by vendors and buyers alike — is to talk about the whole spectrum with a word ("generative") that properly belongs only to its far end. Pull the rungs apart first, because each has a different cost model, latency profile, safety surface, and answer to "can you QA this."

| Rung | Core mechanism | Latency profile | Safety / brand risk | Where it ships |
|---|---|---|---|---|
| **1. Pure rule-based** | Conditional routing on edge or client flags | <50 ms | Very low; deterministic | Localization, A/B tests, targeted content — dominant by volume |
| **2. Catalog selection** | LLM picks a pre-built component/variant ID from a closed set | 100–500 ms | Low; model routes, does not style | Transactional screens, checkout, dashboard panels |
| **3. Template composition** | LLM populates slots in strict component templates | 500 ms–1.5 s | Medium; clipping/overflow risk | **Contextual workspaces, AI-assisted canvases** |
| **4. Deterministic shell** | LLM emits schema-conforming JSON; a deterministic renderer takes over | 500 ms–3 s | Medium; needs client-side validation | **Live reporting, data viz, form builders** |
| **5. Direct code emission** | LLM generates executable front-end code at runtime | 2–8 s | High; arbitrary code, breakage, silent a11y regressions | Prototyping sandboxes; runtime ≈ unshipped |

Rungs 3 and 4 are bolded because that is where genuine production work concentrates. Engineering teams rarely build at the extremes: pure rule-based systems are too rigid for real context, and runtime code generation is too slow, too costly, and too unpredictable for core application paths. The foundation paper called this shape *slot-based generation* — a hand-designed shell, hand-defined slot types, generated content, and a context-inferred selection of which slots appear. Granola, Linear, and Dia all live here.

Two cautions about the spectrum as a model. First, real systems are hybrids — "a rule-based shell with one Rung-4 structured-output panel inside it," not a single architectural choice. Second, "generative UI" as a vendor term spans Rungs 2 through 5, which inflates claims by design. The disciplined buyer's question: *does the model select, compose, emit data, or emit code — and at build time or at runtime?* Four answers, wildly different consequences.

On Rung 5 specifically: research is pushing on it — a 2025 Google Research paper demonstrated an architecture in which an LLM with tools emits a full HTML/CSS/JS page, with results human raters preferred over plain model text.[^1] But that is a research result with an evaluation dataset attached, not a shipped consumer product. Runtime code emission is viable as build-time tooling and risky as a runtime, and that distinction is doing work that marketing copy collapses.

---

## 2. LLM integration patterns

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

The headline pattern is the idea that an LLM "decides what UI to render" by calling a tool. Stripped of mystique: the developer defines a set of tools and, for each, writes the component that will display its result. The model is given the tool definitions and, during a response, emits a *function call* — a tool name and arguments — exactly as it would to call a weather API. The application intercepts the call, runs the tool (which returns structured data), maps the tool name to the pre-written component, and renders it with the tool's output as props. The model never emits an interface. It emits a *decision*; the rendering is deterministic code a human wrote in advance.

This relocates the design control surface: the model's freedom is bounded by the tool catalog and the argument schemas. Constrain what can appear by constraining the catalog. The Vercel AI SDK is the canonical reference, and it is instructive because it has shipped two generations and publicly preferred the second. The production-recommended model (AI SDK 5, July 2025; AI SDK 6, December 2025) exposes a typed `message.parts` array; tool calls appear as typed parts with an explicit lifecycle — `input-streaming`, `input-available`, `output-available`, `output-error` — and the client switches on part type and state, showing a loading skeleton at `input-available` and the real component at `output-available`.[^2][^3] The earlier RSC approach (`streamUI`) sits in the experimental-but-maintained state described in Preface flag 2.[^4]

### 2.2 Structured outputs and schema enforcement

To stop model hallucinations from breaking downstream rendering, the model is forced to schema-conforming JSON. The mechanism — *constrained decoding* — matured quietly in 2024–2025: OpenAI's Structured Outputs uses constrained sampling so "the model cannot produce output that violates your schema";[^5] Anthropic compiles a JSON schema into a grammar that restricts token generation, now generally available;[^6] the Vercel AI SDK wraps both behind `generateObject` / `streamObject` keyed to a Zod schema.[^7] The architectural payoff is a clean separation of concerns: the model owns content and structure *within the schema*; the deterministic renderer owns pixels, accessibility, responsiveness, and brand. You test the renderer exhaustively once, then fuzz the schema. This is the cleanest available answer to "how do you QA a generative interface" — make most of the interface not generative, and make the generative part a data contract. OpenAI's Apps SDK (previewed November 2025) is Rung 4 at scale: a tool returns `structuredContent`, ChatGPT renders a developer-authored component, and the recommended pattern explicitly separates "data tools" from "render tools."[^8]

### 2.3 RAG as context grounding

Retrieval-augmented generation's role is upstream and easy to misplace. RAG renders nothing; it injects retrieved context — user history, account data, documents — into the prompt, and that context shapes what the model emits, which shapes the UI.[^9] In a Rung-4 system, retrieved user data becomes the context a structured-output call turns into JSON, then UI. The 2025 framing renames this the "context layer," which is more honest about its function — and a reminder, from the foundation paper's ethics section, that the retrieval layer is also an *attack surface*: option and decoy injection into retrieved context steers the model itself.

### 2.4 Multi-step and agentic flows

Adaptive interfaces increasingly interleave UI and action: show a component, take input, perform an action, show another component. The AI SDK's agent abstractions run complete tool-execution loops, and because tool parts can render UI mid-loop, a flow can paint an interface, wait for a person, and continue.[^3] LangGraph emits UI components from graph nodes and persists UI state across steps with explicit human-in-the-loop checkpoints; LangChain and LlamaIndex provide the orchestration for multi-agent routing.[^10] The design consequence: the interface is no longer a destination but a series of surfaces materialized along a process.

### 2.5 Streaming and an emerging interop layer

The streaming primitive — partial structured output a renderer can paint from incomplete-but-valid data — is large enough for its own section (Section 5). On standardization: an interop layer is forming beneath all of this. The Model Context Protocol (MCP) standardizes how applications expose context and tools to models; an extension, MCP Apps, standardizes interactive UI delivered *from* an MCP server; the AG-UI protocol aims to standardize the event stream between an agent backend and a frontend.[^11] None is settled — treat "MCP will be the standard" as `*[speculative]*` — but the industry is trying to agree on a wire format for "a model produced something that should become UI," and which format wins is a live question to track, not bet on.

---

## 3. Multimodal considerations

Web and mobile no longer assume one input shape. An adaptive UI that adapts only its *content* while assuming a mouse is adapting along the wrong axis.

| Modality | Core challenge | Interface response |
|---|---|---|
| Pointer & keyboard | Eroding default; hover-only affordances | Density OK, but never hover-gate a function; treat form factor as a weak proxy for input |
| Touch & gesture | Invisible affordances; no haptic confirmation | ≥44 pt targets; every gesture needs a visible non-gesture path; immediate visual feedback |
| Conversational / typed NL | The blank-prompt problem | Hybrid surfaces — NL alongside GUI controls, chips, slot-filling forms |
| Voice | Turn-taking, transcription error | Real-time transcription feedback; confirm consequential actions |
| Vision / camera | High bandwidth, high ambiguity | A grounding step — surface what the system believes it sees |
| Ambient / proactive | Disruption, alert frequency | Event-driven; batch into a quiet inbox-style stream, not a chat |

### 3.1 Pointer, touch, conversation

Pointer and keyboard remain the implicit assumption of nearly every web framework, but they are now one modality among several. WCAG 2.2 codified the response — Success Criterion 2.5.8 requires interactive targets of at least 24×24 CSS pixels — and it is legally load-bearing in the EU under the European Accessibility Act.[^12] Touch contributes directness; its cost is discoverability, since a gesture is an invisible affordance, and the settled guidance is that every gesture needs a visible non-gesture alternative. Typed natural language is shipped at scale; its failure mode is the *blank-prompt problem* — an empty box communicates nothing about capability — and the shipped mitigation is hybrid surfaces, not conversation-as-interface.

### 3.2 Voice and vision

Voice quality and latency have crossed the usability threshold: OpenAI's `gpt-realtime` (August 2025) collapses the speech-to-text → LLM → text-to-speech pipeline into a single model with sub-second voice-to-voice latency; Gemini Live ships real-time voice with camera and screen-sharing.[^13] But genuinely overlapping, listen-while-speaking dialogue has not shipped — Advanced Voice Mode is still turn-based — and the most-promised adaptive voice surface, a personalized context-aware Siri, has been announced and repeatedly delayed. Camera input *is* shipped — Apple's Visual Intelligence, Google's Search Live — and its defining requirement is a grounding step, because misrecognition is otherwise silent.

### 3.3 Cross-device handoff — the under-solved one

Cross-device continuity matters disproportionately for retail and SaaS clients, and it is where the architectural gap is widest. There is no single mechanism; there are three incompatible ones. **OS-level proximity continuity** (Apple Handoff) works by local, end-to-end-encrypted device-to-device transfer — ephemeral, proximity-bound, passing a live activity state. **Cloud account sync** (a retail "save cart across devices" feature) persists state server-side and reloads it on login anywhere; it is the most mature pattern because the unit synced — a cart — is a well-defined data structure. **Partial sync** is what the AI assistants actually do: ChatGPT syncs its *memory* across devices but not *live conversation threads* in real time. So "AI continuity" today is eventual-consistency history plus persistent memory — not live session handoff.

The gap is structural: there is no cross-vendor standard for handing off an *adaptive or generative UI state*, because such a state is not a document — it is a tuple of prompt, context, model output, and render, and nothing standard serializes that tuple. A retailer can sync a cart because a cart is data; nobody can yet sync "the in-progress generated interface you were looking at." For a client whose customers move between devices mid-task, this is a real constraint to design around, not a solved feature to assume. The honest engineering answer today is *re-generation from synced context* on the second device, not *transfer of the rendered state*.

### 3.4 Ambient surfaces — and the agent as a new entry point

The distinction between ambient/proactive and user-initiated surfaces is architectural: a user-initiated surface is request/response; an ambient surface is event-driven, running continuously and surfacing only on a threshold. LangChain's "ambient agents" framing argues an ambient surface needs a different container — an inbox, modeled on email, with explicit notify/ask/review patterns, because the user is not present at the moment of action.[^14] Ambient agents are an emerging pattern with reference implementations, not a mainstream consumer-shipped UI; the strongest production case is narrow — clinical documentation scribes.

One adjacent development changes what surface you are even building for. Adobe's analysis of the 2025 holiday season found retail traffic arriving *from* generative-AI sources — users acting on a recommendation from ChatGPT, Claude, or Perplexity — up roughly **693% year over year**, with those AI-referred shoppers converting about **31% higher** than traffic from traditional channels.[^15][^16] The share is still small, but the trajectory is the implementation-relevant point: the agent is becoming the *referrer*, sometimes the buyer. Building "adaptive UI for commerce" now quietly includes building a surface — structured data, clean semantics, machine-legible product information — that an *agent* can read and act on, not only one a human can see. The foundation paper treats this market shift in full; here it is a directive about what to instrument and expose.

---

## 4. Memory and context architecture

An interface can only adapt to what it remembers. Where user state lives is not a back-end detail — it determines what adaptation is possible, what it costs, and what legal obligations attach. The architecture is layered, and the layers trade off volatility against durability and governance load:

```
┌───────────────────────────────────────────────────────────┐
│ Active context window — ephemeral payload sent to model    │
│ ┌───────────────────────────────────────────────────────┐ │
│ │ Semantic memory — vector store (turbopuffer / pgvector)│ │
│ │ ┌───────────────────────────────────────────────────┐ │ │
│ │ │ Persistent profile — CDP / profile graph          │ │ │
│ │ │ ┌───────────────────────────────────────────────┐ │ │ │
│ │ │ │ Session-only — local state / sessionStorage   │ │ │ │
│ │ │ └───────────────────────────────────────────────┘ │ │ │
│ │ └───────────────────────────────────────────────────┘ │ │
│ └───────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
 innermost: cheapest, most volatile, lowest compliance risk
 outermost: most durable, highest latency + governance load
```

### 4.1 The tiers

**Session-only** state (React/Redux state, `sessionStorage`) is erased on tab close — trivial, privacy-friendly, shallow. **Persistent profile** state lives in a CDP or profile graph; Adobe's Real-Time CDP runs edge segmentation in milliseconds against a localized profile store. The profile is structured and human-readable, which — as 4.3 shows — makes it the most legally tractable place to keep personalization data. **Semantic memory** stores embeddings in a vector database and retrieves by similarity; the relevant property is that an embedding is not human-readable, which sounds privacy-friendly and is the opposite. **The context window** is the simplest "memory" — the transcript re-sent each turn — and its limits are routinely understated: the "lost in the middle" effect and "context rot" mean effective recall falls well below the advertised maximum. The context window is working memory, not durable memory. Every shipped consumer memory feature is a **hybrid** of these.

### 4.2 How shipped memory features actually work, and what scaling one looks like

The shipped implementations are not what most people assume. ChatGPT's memory is *not* RAG: it maintains a structured summary — a dossier of preferences, past-conversation highlights, and interaction metadata — and injects it into the system prompt of *every* new chat, with no retrieval step, invisibly conditioning every output. Claude's memory periodically distills durable facts from history and announces when it uses one; Gemini's personalization is retrieval over a pre-existing data store (the user's Google account). Three vendors, three architectures.

Notion's vector-search infrastructure is the clearest published worked example of scaling the semantic-memory tier, and it is worth getting the specifics right. Per Notion's engineering account *Two years of vector search at Notion* (February 2026): Notion decoupled storage from compute by moving to **turbopuffer** — a vector database built on object storage — rather than running vector indexes on bundled storage-plus-compute pods; DynamoDB handles intelligent page-state caching; Apache Spark runs offline batch indexing while Kafka consumers handle real-time updates; and embeddings were brought in-house, self-hosted on Ray/Anyscale after migrating off external APIs. Notion also consolidated a dual-path system into a unified turbopuffer architecture. The reported results are useful for client conversations: roughly **90% cost reduction, 10× capacity scale, query latency cut from 70–100 ms to 50–70 ms, and a 70% reduction in data volume**.[^17] The honest counterpoint, noted in Zilliz's analysis of vector infrastructure, is that the gap between real-time serving and offline processing — memory maintenance, knowledge-graph precomputation, batch flywheels — is still largely unsolved; turbopuffer-class systems make the serving side cheap and scalable, not the whole problem.[^18]

### 4.3 The architecture choice is a governance choice

This is genuinely non-obvious, and it should change decisions. Under GDPR's right to erasure, a user can demand deletion. For a structured profile this is tractable — delete a row. For a vector store it is hard, and the difficulty is *discovery*, not deletion mechanics: a user's information may be embedded into vectors created from documents written *about* them, scattering their data in forms no index surfaces by name.[^19] For data baked into model *weights* through fine-tuning, erasure is effectively unsolved — "machine unlearning" research through 2025 repeatedly found unlearning does not truly remove knowledge.[^20] The architectural rule that follows is concrete: **never let raw personal data enter training data; keep personalization in retrievable, deletable stores.**

The regulatory perimeter has other edges. California's finalized CCPA/CPRA rules govern "automated decisionmaking technology" narrowly — technology that *substantially replaces* human decision-making in *significant* decisions, explicitly excluding advertising — so most adaptive-UI personalization sits outside that regime, but an adaptive UI gating a loan or job flow pulls the whole system in.[^21] The EU AI Act's Article 50 transparency obligations, enforceable from 2 August 2026, break into three provisions a design team must hold separately:[^22][^23]

- **Article 50(1) — direct interaction.** Users must be informed they are interacting with an AI system, unless that is obvious to a reasonably well-informed person. For an AI helpdesk or assistant this means a persistent label or clear disclaimer.
- **Article 50(2) — synthetic content.** AI-generated text, audio, image, or video must be marked in a machine-readable format so it is detectable as AI-generated. An open and consequential interpretive question: does this attach to an AI-*generated interface*, not just AI-generated media?
- **Article 50(4) — public-interest text.** AI-generated text published to inform the public on matters of public interest must be disclosed as artificially generated, unless it underwent human editorial review.

Finally, data residency is no longer free: Anthropic prices US-only inference at a 1.1× multiplier, and regional cloud endpoints carry roughly a 10% premium.[^24] Every adaptive render that ships personal context to a model API is both a compliance decision and a measurable line item. The memory architecture is chosen by engineers, but it writes the privacy, residency, and portability story the legal and design teams must live with — it should be a deliberate, cross-functional decision, and it rarely is.

---

## 5. Streaming UI as a primitive

Most teams hold a binary mental model of UI: it is either rendered or not, and the gap is a spinner. Progressive materialization breaks that model, and it is novel enough to be a design primitive in its own right.

```
Traditional:  [blank] ─────────── wait ─────────── [fully rendered]

Streaming:    [blank] → [skeleton] → [partial cards] →
              [streaming content] → [hydrated + interactive]
```

### 5.1 What it is

Three technical layers underpin it. **Token streaming plus partial structured output** — because a model emits tokens sequentially, a stream of progressively-completing, schema-valid objects can be exposed to the renderer (`streamObject`'s `partialObjectStream`).[^25] A telling refinement: the AI SDK added a mode that streams *complete objects* rather than individual tokens, specifically because token-level partials caused layout shift — even the streaming primitive moved toward more structure.[^26] **Server-side component streaming** — React Server Components serialize a tree over a chunked response, with Suspense boundaries declaring deferrable subtrees flushed out of document order.[^27] **Optimistic rendering** — paint the expected end-state immediately, reconcile on arrival.

### 5.2 What it looks like, and what it changes

The pattern is visible across every major AI product: Anthropic's Artifacts render generated code live in a sandboxed side-by-side panel; ChatGPT's Canvas opens an editable document with a diff view; v0 streams JSX into a live preview; Copilot renders dimmed "ghost text" inline.[^28][^29] Streaming changes three things. **Latency tolerance** — visible progress makes identical waits feel shorter; users tolerate 2–8 second generations they would never grant an opaque spinner. (The direction is well-established; the specific percentages that circulate are hard to trace to primary studies — cite the direction, not the magnitude.) **Interaction expectations** — generation becomes something the user watches and can abort, which is why every product has a "Stop generating" control. **The visual language of "in progress"** — "pending" and "partial" become first-class states with their own vocabulary: skeletons and shimmer, token-by-token reveal, staged Suspense reveals, and reasoning traces shown as UI.

The deepest consequence is for what a designer designs. The unit is no longer "the finished screen" but the screen's *trajectory* through partial states — empty, skeleton, partial, streaming, complete. A component must be valid and legible at every intermediate state. This is a genuine expansion of the design surface, and the clearest example in this paper of an implementation reality most design practice has not absorbed: a design system that specifies only end-states specifies a fraction of what ships.

---

## 6. Evaluation, QA, and governance

If the interface is generative, you cannot review every state — the set is unbounded. The traditional model of design QA, a designer signing off on every screen, does not degrade gracefully; it breaks. The replacement is borrowed wholesale from machine-learning evaluation, is genuinely shipping at some companies, and is immature in exactly the place that matters most.

### 6.1 Eval-driven development replaces screen-by-screen QA

Anthropic's published methodology is the most rigorous primary source, and its structure is now widely shared: three layers of grading — code-based graders (deterministic checks), model-based graders (an LLM judging against a rubric), and human graders (the gold standard, used to calibrate the LLM judges).[^30] Golden datasets are built incrementally — start with twenty to fifty tasks drawn from real observed failures. Evals check *outcomes*, not intermediate steps. Non-determinism is measured, not wished away, with metrics like `pass@k` and the stricter `pass^k`. The posture is "Swiss cheese": automated evals, production monitoring, A/B tests, user feedback, and manual transcript review, each layer catching what the others miss.

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

The tooling is real and largely generally available: Anthropic's developer console eval tool, OpenAI Evals (open-source framework plus platform product), Braintrust, LangSmith and Langfuse, DeepEval, Ragas, and Inspect from the UK's AI Security Institute.[^31][^32] One market event belongs here: **OpenAI acquired Promptfoo, the leading open-source LLM evaluation and red-teaming tool, announced 9 March 2026** (corroborated by OpenAI's and Promptfoo's own announcements and contemporaneous press).[^33] It is a meaningful consolidation signal — a frontier lab absorbing the open-source eval layer that production teams had been treating as neutral infrastructure. Teams standardizing on Promptfoo should treat its independence as now a question, not an assumption.

The gap a design leader must not miss: **none of these frameworks is purpose-built for generative UI.** They evaluate text and agent outputs. Teams building generative interfaces adapt them by treating rendered output — generated code, a component tree, a DOM — as the artifact to grade. It works, but the QA infrastructure for adaptive UI is a retrofit, not a native tool.

| Evaluation layer | Tooling | Objective | Honest status |
|---|---|---|---|
| Schema validation | Zod / Valibot / `is-json` | Output matches the layout/data contract | Solved; deterministic |
| Semantic consistency | LLM-as-judge / embedding similarity | Output matches intent and system instructions | Workable; ~85% judge-human correlation |
| Security / red-team | Promptfoo red-team, injection suites | No prompt-injection or data-leak paths | Maturing |
| Operational telemetry | OpenTelemetry GenAI conventions | Tool-success rate, latency, user resets | Workable; spec still experimental |
| **Accessibility** | **axe-core / Pa11y in-pipeline** | **WCAG conformance of generated output** | **Partial — see 6.2; not solved** |

### 6.2 The weakest link: accessibility QA at scale

This is the most important correction in this synthesis, because one source draft got it flatly wrong. Accessibility QA for generative UI is **not** solved by running axe-core in CI, and presenting it as a "zero critical violations" checklist item misrepresents the state of the art.

The evidence is unambiguous. Automated accessibility tools catch roughly **25–40% of WCAG violations**; the remaining 60–75% requires manual review with humans and assistive technology.[^34] Stricter analyses are harsher still: by one assessment only about **13% of WCAG criteria can be reliably flagged by automated scans, and roughly 42% cannot be detected by automation at all** — they require evaluator judgment.[^35] And the baseline is bleak before variability even enters: the WebAIM Million 2026 analysis found **95.9% of the top one million home pages have detectable WCAG 2 A/AA failures, averaging 56.1 errors per page** — *static* UI failing the bar at scale.[^36] WCAG 3.0 will make this harder, not easier: it introduces qualitative and percentage-based tests explicitly designed to require human judgment. axe-core is the industry-standard tool *within* the automation ceiling — it is excellent at what it covers — but it does not solve the problem, and manual testing remains required.[^37]

For generative UI this compounds: when every render differs, you cannot pre-scan every screen. Running axe-core against each generated DOM inside the pipeline, as a code-based eval gate, is the right move — but it inherits the automation ceiling. It catches the 25–40%, not the rest.

This produces a real strategic tension, and it is worth stating to clients directly rather than hiding. The foundation paper establishes that the single strongest, best-evidenced use case for adaptive UI is accessibility — ability-based design, the Gajos lineage. This paper has to report that the QA infrastructure to *verify* accessibility is least mature exactly for the variable-surface case. So adaptive UI's most defensible use case is also the one where you can least automatically confirm it is working. This is not a reason to avoid the work — it is a reason to *scope it correctly*: budget for ongoing manual accessibility testing with assistive technology as a standing cost of any generative-UI engagement, treat automated scanning as a floor rather than a finish line, and do not let a green CI check stand in for an accessibility guarantee.

### 6.3 Human-in-the-loop, telemetry, red-teaming, governance

*Human-in-the-loop review at thresholds* — escalating to human review only when an automated check flags risk — is well-articulated in research as "oversight-by-design" but thinly documented in production with concrete numbers. Notion's runtime guardrails are a shipped example: higher-risk agent actions trigger pop-up confirmations and, during execution, sensitive mutations (deleting database items, sending external email) halt for explicit owner confirmation. *Telemetry* becomes the primary post-ship signal — Notion has said roughly 80% of its AI team's work is driven by feedback and traces — spanning explicit feedback (thumbs, ratings) and implicit signals (abandonment, reformulation, and *regret signals*, such as a user editing every output despite a thumbs-up).[^38] *Red-teaming* is comparatively mature: Microsoft's published study of red-teaming a hundred generative AI products is the definitive account, with the central lesson that testing has shifted from the model alone to the whole system.[^39] Red-teaming for adaptive UI now has to cover a second manipulation vector the foundation paper documents: LLM agents are hypersensitive to choice-architecture nudges and option injection,[^40] so an adaptive system that retrieves and acts on external content must red-team the *retrieval and option surface*, not only the prompt.

The *governance* shift the foundation paper anticipated — from "did we follow the design system" to "did the system produce acceptable outcomes" — is real as a direction of travel and under-formalized as practice. No design-system-specific, outcomes-based governance framework has been published; governance for generative UI is assembled from general AI-governance practice plus eval and red-team tooling. Two companies have published enough to learn from — Notion in detail, Vercel on eval-driven development for v0 — and a buyer should be skeptical of any vendor who describes their evals but cannot show them.

---

## 7. Cost, latency, and performance reality

Adaptive UI runs on tokens, and tokens cost money and time. This is the layer design conversations ignore most completely.

### 7.1 The token cost model

Current per-million-token pricing (May 2026) spans a wide range: Claude Opus 4.7 ≈ $5 in / $25 out, Sonnet 4.6 ≈ $3 / $15, Haiku 4.5 ≈ $1 / $5; OpenAI GPT-5.5 ≈ $5 / $30, GPT-5.4 ≈ $2.50 / $15, with Mini and Nano tiers far below; Google Gemini 3.1 Pro ≈ $2 / $12, 2.5 Flash ≈ $0.30 / $2.50.[^24][^41][^42] Figures move; ratios are the durable insight.

The compounding, made concrete two ways. A per-render frame: 4,000 input tokens (system prompt, profile, retrieved context) and 1,000 output tokens, at ten renders per session and one million sessions per month, costs about **$37,000/month on Gemini 2.5 Flash and about $450,000/month on Claude Opus 4.7** — model choice swings cost roughly **twelvefold for an identical user experience**. A per-day frame: one million interactions/day at 4,000 input + 500 output tokens, at a mid-tier $2.50/$10 per-million rate, runs about **$15,000/day in inference**. Either way, the lesson is the same and belongs in every adaptive-UI business case: per-render generation at consumer scale is a six-to-seven-figure monthly line item, and the model decision dominates it.

### 7.2 Latency budgets

The interaction thresholds are old and stable: under ~200 ms feels instant, under ~500 ms responsive, beyond ~1 s noticed, beyond ~2 s frustrating. Generative UI runs straight into them — a full completion is commonly 2–8 seconds, a reasoning model 45–120 seconds merely to begin. A generative UI that blocks first paint on a full completion violates the budget by an order of magnitude. There are three ways out, all from Section 5: stream (so the budget that matters becomes time-to-first-token), render optimistically or with skeletons, or pre-compute.

### 7.3 Caching and model choice

Caching is the main lever. Exact-match caching catches only a small fraction of redundant calls because users rephrase. Semantic caching — embed the query, return a cached response above a similarity threshold — does better, but realistic production hit rates land at 20–45%, not the 95% sometimes claimed. Provider-side **prompt caching** is the most reliable win: it caches a stable *prefix*, with OpenAI pricing cached input at roughly half and Anthropic a cache read at about a tenth of base input.[^43] The design-relevant consequence: order the prompt so stable parts come first — system instructions, design tokens, component schemas — and volatile per-user context last, so the prefix hits the cache every request. On model choice, only an estimated 25–35% of queries genuinely need a frontier model;[^44] *routing* (size each query to a model) and *cascading* (try a small model, escalate on failure) cut cost 45–85% with most quality retained. The strongest cost lever for adaptive UI specifically is the one a designer controls: *do not generate UI when you do not have to* — pre-compute and template-cache the common layouts, reserve live generation for genuinely novel states.

---

## 8. Authoring tooling and the design workflow

When the output is not a fixed screen, what does the design tool look like? Honestly: there is no mature design tool for variable output, and every current approach is a workaround.

**Figma plus prompts.** Figma's AI suite shipped through 2024–2025; Figma Make, a prompt-to-code tool, reached general availability in July 2025.[^45] Its limits are admitted: exported code is not tied to a production design system, credit limits cap iteration, and once a user makes a manual edit, prompt-based editing breaks. Figma Make generates a *fixed prototype per prompt* — a faster way to produce one artifact, not a tool for designing a system that renders variably.

**Storybook plus an eval suite.** The most credible component-driven workflow shipping today. Storybook now positions itself for AI agents: components, props, stories, and docs define what an agent may build; the test runner executes generated stories in a real browser and feeds failures back; an MCP add-on exposes the design system to agents as documented, selectable tools.[^46] It makes Storybook both a *constraint* and a *feedback loop* — but it governs *which components an agent uses*, not how a designer specifies variability.

**v0-style tools.** v0, Lovable, Bolt, Replit Agent generate UI from prompts; their shared shortfall for design teams is the "70% problem" — users hit a complexity ceiling and must drop into hand-editing code — and they are single-shot generators of fixed artifacts.

**The component-prompt pair.** The genuine new artifact emerging is a component bundled with a machine-readable description of when and how to use it — code, schema, and semantic prompt as one atomic unit:

```typescript
export const InfoCard = {
  component: InfoCardReact,
  schema: z.object({ title: z.string(), body: z.string(), severity: z.enum(["info","warning","error"]) }),
  semanticPrompt: "Use to surface a single alert, warning, or short text summary. " +
                  "Not for primary content or multi-field data — use DataPanel for that.",
};
```

A model queries a catalog of these to know what is available and how to populate it. No design tool authors this pairing as a first-class object — the "prompt/spec" half is improvised in code or markdown.

**The unsolved problem.** Designing for variability is genuinely unsolved, and the clearest vocabulary for it comes from academic HCI: a recent systematic review names it "variability by design" and describes the shift it demands — a designer moves from *visual authorship* (drawing the screen) to *architectural intent* (specifying components, behavioral rules, and interface policies, and letting the system compose).[^47] What is missing is the tool: nothing lets a designer specify a *space* of possible outputs and review the *distribution* of what that space produces. Review today is sampling individual generations by eye. Academic work points at one missing primitive — automated design critique; UICrit, a UIST 2024 dataset of professional design critiques, was explicitly proposed as a reward model for evaluating generated UI.[^48] The design workflow for adaptive UI is currently code-first, with designers participating through prompts, component contracts, and the eval loop rather than a canvas. That may change; it has not yet.

---

## 9. Design system implications

The foundation paper argued the design system survives the shift to adaptive UI and becomes *more* load-bearing. The implementation reality sharpens that into four concrete shifts.

**Primitives over composed components.** The industry has moved decisively toward headless primitives — Radix UI and, especially, shadcn/ui (primitives plus Tailwind, distributed as copy-paste source) have become the de facto base for v0, Bolt, and Lovable.[^49] The reason is mechanical: when a model can see and shape all the code, it composes more reliably than when it must work through the fixed API and theming of an opinionated library. A design system architected as a closed catalog of heavily-composed components is *less* adaptable to LLM composition than one architected as open, primitive-level code.

**Semantic component contracts.** For a model to select a component, the component must describe *what it does* — its intent, the context it needs, its alternatives — not merely how it looks. Each component should expose a precise JSON Schema for its inputs, a semantic description of its purpose and proper use, and the accessibility and spacing rules the renderer enforces. The mechanism is emerging through MCP; Storybook's MCP add-on is the concrete shipped example. There is no ratified standard for component intent metadata yet — building toward one is the highest-leverage design-system investment for adaptive UI.

**Evals replace QA.** Covered in Section 6 — continuous automated evaluation as the QA function, with humans calibrating the judges rather than reviewing every screen.

**Governance shifts from compliance to outcomes.** The question moves from "did this screen follow the system" to "did the system produce an acceptable outcome." This is a real change in what governance *means*, and it is under-formalized. The implementation notes that follow stand: the system prompt becomes a versioned, reviewed design artifact, and variant logging — a record of which generated variant reached which user, and why — becomes infrastructure, both for debugging and for the auditability the EU AI Act's effect-based enforcement will eventually require. No vendor has published a good reference implementation of variant logging; that is a genuine gap, and possibly an opportunity.

The synthesis: components stay consistent; compositions vary within rules the design system encodes; "consistency" comes to mean *the user can predict and trust the surface* rather than *every user sees the same surface*. The design system does not shrink — it moves up a level, from specifying pixels to specifying the space of acceptable outcomes, which is more demanding work, not less.

---

## 10. Where this might be headed *[speculative]*

*[speculative]* The middle of the spectrum stays where the work is. Rungs 3–4 — slot-based generation, structured output rendered by deterministic components — remain the dominant production shape for the next two to three years; runtime code generation does not become a mass-market pattern, because the QA, cost, latency, and safety problems are not close to solved.

*[speculative]* An interop standard consolidates, but which one is genuinely open — MCP and its UI extensions, AG-UI, and the AI SDK's `message.parts` are the contenders, and some convergence is likely within two to three years because the fragmentation is expensive for everyone.

*[speculative]* The authoring-tool gap gets filled — or it does not, and the design role permanently reshapes around prompts, contracts, and evals rather than a canvas. The second is the current trajectory, and trajectories are sticky.

*[speculative]* Falling token prices weaken the economic objection to live generation without removing it — the QA, accessibility, and governance costs are human and structural and do not fall with token prices.

*[speculative]* Agentic commerce compounds. If the trajectory in §3.4 holds, a meaningful share of retail discovery becomes agent-mediated within a couple of years, and "build a surface an agent can read and act on" becomes a named implementation discipline alongside "build a surface a human can see." The deterministic, well-structured, semantically-labeled data layer — the same one that makes Rung-4 generation work — turns out to also be what makes a product legible to a buying agent. That convergence is the most plausible reason the unglamorous middle of the spectrum is also the strategically correct place to invest.

What is **hype**: that "AI will design the interface" — that describes Rung 5 at runtime, which is nearly empty in production; and that design systems become irrelevant — they become the load-bearing constraint. The durable shape is less dramatic and more buildable: deterministic shells, constrained generation inside them, evals where QA used to be, and a design system doing more work than ever.

---

## Open questions

1. **Will an interoperability standard consolidate, and which one?** MCP/MCP Apps, AG-UI, and `message.parts` are competing informally. Fragmentation means every project pays an integration tax indefinitely; a winner's timing is a real strategic variable.
2. **Is accessibility QA at scale solvable with current tooling, or does it need something new?** In-pipeline DOM scanning inherits the automation ceiling (25–40%). Whether generative UI can ever meet the accessibility bar that is its own strongest justification is the most important unresolved question in this paper.
3. **What does good variant logging look like?** No vendor or industry body has published a reference design — what is logged, who holds it, who audits it, how long it is retained. The EU AI Act's effect-based enforcement will eventually demand it.
4. **Does the authoring tool get built?** Whether "specify a variability space and review its output distribution" is even a coherent tool concept is unresolved, and the answer reshapes the design profession.
5. **Can generative UI state be made portable across devices?** A prompt-context-output-render tuple has no canonical transferable form; whether anyone defines one, or whether cross-device adaptive UI is simply re-generated from synced context, is open.
6. **Does the OpenAI–Promptfoo acquisition reshape the eval layer?** A frontier lab now owns the leading open-source eval and red-team tool. Whether that accelerates the eval layer or compromises its perceived neutrality is an open governance question for any team standardizing on it.

---

## What to read next — ranked

1. **Anthropic, *Demystifying evals for AI agents*** (January 2026). The most rigorous published methodology for QA-ing generative systems.[^30]
2. **Vercel, AI SDK documentation** — the *RSC-to-UI migration guide* and the AI SDK 5 release notes. The primary record of the architecture's actual, nuanced status.[^2][^4]
3. **Notion Engineering, *Two years of vector search at Notion: 10x scale, 1/10th cost*** (February 2026). The clearest published account of scaling the semantic-memory tier.[^17]
4. **Linear, *How we built Triage Intelligence*** (September 2025). The most concrete published account of shipping an adaptive AI feature end to end.[^50]
5. **WebAIM, *The WebAIM Million 2026*** with Deque/axe-core documentation. The evidence base for what automated accessibility testing can and cannot do.[^36][^37]
6. **OpenAI Apps SDK documentation** (2025–2026). The build documentation for the largest-scale Rung-4 deployment in existence.[^8]
7. **EU AI Act, Article 50** (transparency obligations, enforceable August 2026). Required reading on AI-interaction labeling and synthetic-content marking.[^22]
8. **Chen et al. (Stanford), *Generative Interfaces for Language Models*** (2025). The strongest contribution on *how to evaluate* generative UI.[^51]
9. **LangChain, *Introducing ambient agents*** (January 2025). The clearest articulation of the ambient-versus-user-initiated architectural split.[^14]
10. **Kyungho Lee, *Towards a Working Definition of Designing Generative User Interfaces*** (DIS 2025). The vocabulary the industry lacks for the authoring problem.[^47]

---

## What surprised me — in this synthesis pass

Findings that emerged specifically from integrating two research passes and verifying their disputed claims.

1. **The acquisition flagged as "likely fabricated" was real.** The post-comparison verification had treated the OpenAI–Promptfoo acquisition skeptically because only the more polished, less-cited research pass reported it. It checked out — announced 9 March 2026, corroborated across multiple primary sources. The better-cited pass had simply missed a real market event. Citation density measures diligence, not coverage; a confident claim from the "less rigorous" agent can be true, and the synthesis has to weight evidence, not posture.

2. **The accessibility claim was the cleanest factual error in either source — and it inverts a comfortable assumption.** One draft presented accessibility QA as essentially solved by axe-core in CI. Verification showed automated tools catch only 25–40% of WCAG issues, that roughly 42% of criteria cannot be automated at all, and that 95.9% of *static* top-million pages already fail. The synthesis-pass surprise is the tension this creates with the foundation paper: accessibility is the best-evidenced reason to build adaptive UI and the hardest property to verify once the surface is variable. The same surface is the strongest argument for the work and the weakest point of its QA.

3. **Neither agent was simply "better."** The polished agent contributed the real Promptfoo event, the Notion infrastructure depth, and the cleaner architectural artifacts (diagrams, the EU AI Act sub-provision breakdown, runnable snippets). The hedged agent contributed the citation discipline, the RSC nuance, and — correctly — the accessibility skepticism. The Notion architecture itself was a half-correction: the high-level storage/compute-decoupling narrative was right, but the specific mechanism was turbopuffer, not raw S3. Synthesis here was not "pick the winner" but "verify claim by claim" — and the verification, not the prose quality, was load-bearing every time.

4. **The RSC question had no clean answer, and forcing one would have been wrong.** Both source drafts took a side — "industry standard" or "active retreat." Verification showed the truth was a maintained-but-deprioritized middle state that neither agent's framing captured. Some load-bearing facts are genuinely "it's complicated," and a synthesis that flattens them to match a confident source is worse than one that holds the nuance.

---

## Bibliography

[^1]: Leviathan, Y., Valevski, D., Kalman, M., et al. (2025). *Generative UI: LLMs are Effective UI Generators.* Google Research / arXiv. https://generativeui.github.io

[^2]: Vercel. (2025, July 31). *AI SDK 5.* Vercel Blog. https://vercel.com/blog/ai-sdk-5

[^3]: Vercel. (2025, December 22). *AI SDK 6.* Vercel Blog. https://vercel.com/blog/ai-sdk-6

[^4]: Vercel. (2025–2026). *AI SDK RSC — Migrating from RSC to UI* [Documentation]; `@ai-sdk/rsc` package (extracted in v5, July 2025); RSC-pause discussion on GitHub. https://ai-sdk.dev/docs/ai-sdk-rsc/migrating-to-ui

[^5]: OpenAI. (2024, August 6). *Introducing Structured Outputs in the API.* https://openai.com/index/introducing-structured-outputs-in-the-api/

[^6]: Anthropic. (accessed 2026, May). *Structured outputs.* Claude Developer Platform Documentation. https://platform.claude.com/docs/en/build-with-claude/structured-outputs

[^7]: Vercel. (accessed 2026, May). *AI SDK Core: Generating Structured Data.* https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data

[^8]: OpenAI. (2025, November 13). *Introducing apps in ChatGPT and the Apps SDK*; *Build your ChatGPT UI — Apps SDK* [Documentation]. https://developers.openai.com/apps-sdk/

[^9]: *A Systematic Literature Review of Retrieval-Augmented Generation.* (2025, August). arXiv:2508.06401. https://arxiv.org/pdf/2508.06401

[^10]: LangChain. (accessed 2026, May). *How to implement generative user interfaces with LangGraph* [Documentation]. https://docs.langchain.com

[^11]: Model Context Protocol. (2025–2026). *Specification* and *MCP Apps (SEP-1865)*. https://modelcontextprotocol.io ; CopilotKit. (2025). *Introducing AG-UI.* https://copilotkit.ai

[^12]: W3C. (2023, October). *Understanding Success Criterion 2.5.8: Target Size (Minimum).* WCAG 2.2 Recommendation. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

[^13]: OpenAI. (2025, August 28). *Introducing gpt-realtime and Realtime API updates for production voice agents.* https://openai.com/index/introducing-gpt-realtime/ ; Google. (2025, May). *Gemini Live: in-depth two-way conversations.* Google Workspace Updates.

[^14]: LangChain. (2025, January 14). *Introducing ambient agents.* LangChain Blog. https://blog.langchain.com/introducing-ambient-agents/

[^15]: Adobe. (2026, January). *Adobe Analytics: 2025 Holiday Shopping Report* [AI-driven traffic and conversion data]. https://business.adobe.com/resources/holiday-shopping-report.html

[^16]: Braze. (2026). *2026 Customer Engagement Review.* https://www.braze.com/resources/reports-and-guides/customer-engagement-review

[^17]: Notion Engineering. (2026, February). *Two years of vector search at Notion: 10x scale, 1/10th cost.* Notion Blog. https://www.notion.com/blog

[^18]: Zilliz. (2025–2026). *Vector database infrastructure analysis: the real-time-serving vs. offline-processing gap.* https://zilliz.com/blog

[^19]: Amazon Web Services. (2024). *Implementing Knowledge Bases for Amazon Bedrock in support of GDPR (right to be forgotten) requests.* AWS Machine Learning Blog. https://aws.amazon.com/blogs/machine-learning/

[^20]: *Does Machine Unlearning Truly Remove Knowledge?* (2025). arXiv:2505.23270. https://arxiv.org/abs/2505.23270

[^21]: Skadden, Arps, Slate, Meagher & Flom. (2025, October). *California Finalizes CCPA Regulations for Automated Decision-Making Technology.* https://www.skadden.com/insights/publications/2025/10/california-finalizes-cppa-regulations

[^22]: European Union. (2024). *Artificial Intelligence Act, Article 50 — Transparency obligations* [Enforceable 2 August 2026]. https://artificialintelligenceact.eu/article/50/

[^23]: Covington & Burling (Inside Global Tech). (2026, May 12). *10 Takeaways: European Commission Draft Guidelines on AI Transparency under the EU AI Act.* https://www.insideglobaltech.com

[^24]: Anthropic. (accessed 2026, May). *Pricing.* Claude Developer Platform Documentation. https://platform.claude.com/docs/en/about-claude/pricing

[^25]: Vercel. (2025). *AI SDK Core: streamObject* [Documentation]. https://ai-sdk.dev

[^26]: Vercel. (2024). *AI SDK 3.4.* Vercel Blog. https://vercel.com/blog/ai-sdk-3-4

[^27]: React. *<Suspense> reference* (https://react.dev/reference/react/Suspense); React Working Group, *New Suspense SSR Architecture in React 18* (https://github.com/reactwg/react-18/discussions/37).

[^28]: Orosz, G. (2024). *How Anthropic built Artifacts.* The Pragmatic Engineer. https://newsletter.pragmaticengineer.com/p/how-anthropic-built-artifacts

[^29]: OpenAI. (2024, October 3). *Introducing canvas.* https://openai.com/index/introducing-canvas/

[^30]: Grace, M., Hadfield, J., Olivares, R., & De Jonghe, J. (2026, January 9). *Demystifying evals for AI agents.* Anthropic Engineering. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

[^31]: Anthropic. (2024, July 9). *Evaluate prompts in the developer console.* https://www.anthropic.com/news/evaluate-prompts ; OpenAI. *Evals* [Open-source framework and platform product]. https://github.com/openai/evals

[^32]: UK AI Security Institute. (2024, April; ongoing). *Inspect: An open-source framework for large language model evaluations.* https://github.com/UKGovernmentBEIS/inspect_ai

[^33]: OpenAI. (2026, March 9). *OpenAI acquires Promptfoo* [Announcement]. Corroborated by Promptfoo's own announcement and contemporaneous reporting (TechCrunch, CNBC). https://openai.com/index/

[^34]: Deque Systems and TestParty analyses (2025) on automated accessibility coverage — automated tools detect roughly 25–40% of WCAG violations; the remainder requires manual and assistive-technology review. https://www.deque.com ; https://www.testparty.ai

[^35]: Accessible.org. (2025). *Automated accessibility testing: what scans can and cannot detect* (≈13% of WCAG criteria reliably flagged by automation; ≈42% not detectable by automation at all). https://accessible.org

[^36]: WebAIM. (2026). *The WebAIM Million: An annual accessibility analysis of the top 1,000,000 home pages.* https://webaim.org/projects/million/

[^37]: Deque Systems. *axe-core* [Documentation]. https://github.com/dequelabs/axe-core ; Groves, K. *WCAG testability research.* See also Forrester, *The Forrester Wave: Digital Accessibility Platforms, Q4 2025.*

[^38]: Sachs, S. (Notion), via Braintrust. (2025). *How Notion evaluates AI at scale.* Braintrust Blog. https://www.braintrust.dev/blog/notion

[^39]: Microsoft. (2025, January 13). *Lessons from Red Teaming 100 Generative AI Products.* Microsoft Security Blog / arXiv:2501.07238. https://arxiv.org/abs/2501.07238

[^40]: Cherep, M., Maes, P., & Singh, P. (2025). *LLM Agents Are Hypersensitive to Nudges.* arXiv:2505.11584. https://arxiv.org/abs/2505.11584 ; see also Liou et al. (2025). *OI-Bench: An Option Injection Benchmark for Directive Interference in LLMs.* National Yang Ming Chiao Tung University.

[^41]: OpenAI. (accessed 2026, May). *API Pricing.* OpenAI Developers. https://developers.openai.com/api/docs/pricing

[^42]: Google. (accessed 2026, May). *Gemini Developer API pricing.* Google AI for Developers. https://ai.google.dev/gemini-api/docs/pricing

[^43]: OpenAI. (2024). *Prompt Caching in the API.* https://openai.com/index/api-prompt-caching/ ; Anthropic. *Prompt caching* [Pricing documentation]. https://platform.claude.com/docs/en/about-claude/pricing

[^44]: TianPan. (2025, November). *LLM Routing and Model Cascades.* https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades

[^45]: Figma. (2025, July 24). *Figma Make is now available to all users.* Figma Blog. https://www.figma.com/blog/figma-make-general-availability/

[^46]: Storybook. (accessed 2026, May). *Storybook for AI.* https://storybook.js.org/ai

[^47]: Lee, K. (2025, May). *Towards a Working Definition of Designing Generative User Interfaces.* arXiv:2505.15049 / DIS '25 Companion. https://arxiv.org/abs/2505.15049

[^48]: Duan, P., et al. (2024, October). *UICrit: Enhancing Automated Design Evaluation with a UI Critique Dataset.* Proceedings of UIST '24 / arXiv:2407.08850. https://arxiv.org/abs/2407.08850

[^49]: Holterhoff, K. (2025, April 22). *UI Component Libraries, shadcn/ui, and the Revenge of Copypasta.* RedMonk. https://redmonk.com

[^50]: Linear. (2025, September 3). *How we built Triage Intelligence.* https://linear.app/blog/how-we-built-triage-intelligence

[^51]: Chen, J., Zhang, Y., Zhang, Y., Shao, Y., & Yang, D. (2025). *Generative Interfaces for Language Models.* arXiv:2508.19227. https://arxiv.org/abs/2508.19227

---

*End of implementation paper (synthesis edition).*

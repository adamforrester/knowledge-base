# Implementing Adaptive Interfaces: An Implementation Paper

*A senior design-systems leader's survey of how adaptive and generative UIs actually get built — architecture, design decisions, and operational reality, for web and mobile. Written May 2026.*

---

## Preface — How to read this

This is the companion to the foundation paper. Where that paper covered *what and why* — the lineages, the personalization-versus-adaptation distinction, the evidence base, the ethics — this one covers *how it actually works*. It is the same kind of document: a long-form analytical essay, weighted to shipped reality, with speculation labeled inline as `*[speculative]*` or sequestered in a closing section. It deliberately sits with tensions rather than resolving them, because the implementation landscape is younger and messier than the marketing implies, and pretending otherwise would be the wrong service to a reader trying to tell hype from substance.

It is written for someone who needs to have informed strategic conversations about this work — not to build it personally, but to know which architectural claims hold weight, where the real engineering risk sits, and what a vendor is eliding when they say "generative UI."

Three things to flag at the top, in order of how much they should change your priors:

1. **The generative end of the spectrum is nearly empty in production.** The vivid demo — an AI writes a fresh React interface for each user, each request — describes almost nothing that ships to consumers on web or mobile today. v0 and its peers are *build-time* tools used by developers, not runtime systems serving model-authored code to end users. Every credible production "adaptive UI" sits well short of that: rule engines, constrained selection, structured data rendered by hand-built components. If you remember one thing, remember that the action is in the middle of the spectrum, and the middle is more boring and more buildable than the pitch.

2. **The company that named the field walked its own architecture back.** Vercel introduced "generative UI" as a developer term in March 2024 with AI SDK 3.0 and an RSC-based primitive that streamed React components straight from the model.[^4] By 2025 Vercel had flagged that primitive "experimental," documented its specific failure modes, and published a migration guide pointing developers to a *less* generative pattern — structured tool calls rendered by components the developer wrote in advance.[^11] The replacement is more robust precisely because it is more constrained. That direction of travel — toward constraint — is the single most important implementation fact in this paper.

3. **There is no design tool for this.** Designing a fixed screen has Figma. Designing a system that renders differently every time has nothing — no mature tool lets a designer specify a space of possible outputs and review the *distribution* of what comes out. The workflow is patched together from Figma, Storybook, prompt-to-code tools, and code. Section 8 does not pretend this is solved, because it isn't, and a leader who budgets as though it were will be wrong.

A note on scope and method: this paper covers web and mobile only. It does not cite Josh Clark's unreleased book, for the reasons the foundation paper gave. Where a figure comes from a vendor's own blog, a single study, or a secondary source, it is flagged. The research behind it leaned on primary sources — official documentation, engineering blogs, release notes, regulator guidance, and recent HCI papers — and several widely-repeated industry statistics did not survive contact with their supposed origins; those are named as unverified rather than quietly dropped.

---

## 1. The decision-tree-to-generative spectrum

"Adaptive UI" is not one architecture. It is a spectrum of them, and the most common analytical error — made by vendors and buyers alike — is to talk about the whole spectrum using a word ("generative") that properly belongs only to its far end. Pulling the rungs apart is the first move, because each rung has a different cost model, a different safety profile, and a different answer to the question "can you QA this."

### 1.1 The five rungs

**Rung 1 — Pure rule-based personalization (no LLM).** This is the overwhelming majority of shipped adaptive UI, and it predates large language models entirely. Optimizely's Feature Experimentation evaluates an ordered ruleset per flag — experiments first, then targeted deliveries, then a catch-all — top to bottom, halting the moment a user qualifies for a rule and receives a variation.[^1] Adobe Target's rules-based decisioning works the same way, targeting on demographic, device, behavioral, or profile attributes, and can even push the compiled rule artifact down to the device so the decision executes locally with no network round-trip.[^2][^3] The engine never *creates* anything; it *selects* from pre-authored variations. The tradeoff is stark and favorable on most axes: total control, deterministic output, fully QA-able, near-zero latency, no inference cost, no hallucination surface. What it costs is authoring — every variation is hand-built, and the rule tree grows brittle as it grows large.

**Rung 2 — The LLM picks from a catalog of pre-built variants.** Here the model is a classifier or router: it chooses among whole, human-built components or layouts. The output space is finite and known. Safety is high because every possible output was designed and reviewed; QA is tractable because the set is enumerable; latency is one model round-trip. The LLM contributes routing intelligence and nothing else — it cannot produce a variant a designer did not build.

**Rung 3 — The LLM modifies or composes pre-built templates.** The model now parameterizes and arranges known components: choosing props, ordering, filling content slots, deciding which of several modules appear and in what sequence. The Vercel AI SDK's typed tool parts enable exactly this — a tool returns structured output that is spread into a React component, so the model controls the component's *content and configuration* without touching its markup.[^12] LangGraph's generative-UI feature emits structured UI components from graph nodes alongside messages.[^14] This is the rung the foundation paper called *slot-based generation*: a hand-designed shell, hand-defined slot types, generated content, and a selection of which slots appear inferred from context.

**Rung 4 — The LLM emits structured data; a deterministic renderer takes over.** The model never produces markup. It emits JSON conforming to a schema, and a deterministic, separately-tested renderer turns that JSON into UI. This is the load-bearing pattern for serious production work, and the reason is a piece of infrastructure that matured quietly in 2024–2025: *constrained decoding*. OpenAI's Structured Outputs, released August 2024, uses constrained sampling so that "the model cannot produce output that violates your schema" — a stronger guarantee than the older JSON mode, which promised valid JSON but not schema conformance.[^5] Anthropic shipped an equivalent, compiling the JSON schema into a grammar that restricts token generation at inference time; it has since reached general availability, with documented limits worth knowing (no recursive schemas, a cap on strict tools per request).[^6] The Vercel AI SDK wraps both behind a single `generateObject` / `streamObject` interface keyed to a schema.[^7] The payoff for adaptive UI is architectural: the schema is the contract, the renderer is deterministic and unit-testable, and visual risk is capped by the renderer no matter what the model emits. OpenAI's Apps SDK — the framework for third-party apps inside ChatGPT, previewed November 2025 — is essentially Rung 4 at scale: a tool returns `structuredContent`, and ChatGPT renders a developer-authored component, with the recommended pattern explicitly separating "data tools" from "render tools."[^8][^9]

**Rung 5 — The LLM generates code directly.** The model emits React, HTML, JSX. This is what most people picture when they hear "generative UI," and it is the rung with the least production reality. v0 (Vercel's prompt-to-code product) generates React, Tailwind, and shadcn/ui code and reports millions of developers.[^10] But v0 is a *design and build-time tool* — a developer-in-the-loop code generator — not a runtime that ships freshly-generated, freshly-executed component code to end users on each request. The research behind this paper found no verified mainstream consumer web or mobile product that does that in production. Rung 5 at runtime remains experimental. The tradeoffs explain why: maximum flexibility, minimum control, high latency, high cost, near-impossible QA (the output space is unbounded), and a genuine safety surface (arbitrary code, layout breakage, silent accessibility regressions). Research is actively pushing on this rung — a 2025 Google Research paper demonstrated an architecture in which an LLM equipped with tools emits a full HTML/CSS/JS page, with results human raters preferred over plain model text and a purpose-built evaluation dataset attached — but that is a research result, not a shipped consumer product.[^75] It is viable as build-time tooling and risky as a runtime, and that distinction is doing a lot of work that marketing copy collapses.

### 1.2 Where production work actually sits

| Rung | Pattern | Control | QA-ability | Latency | Inference cost | Production reality |
|---|---|---|---|---|---|---|
| 1 | Rule-based selection | Total | Full | ~0 | None | Dominant by deployment volume |
| 2 | LLM picks a variant | High | High (finite set) | One round-trip | Low | Common, growing |
| 3 | LLM composes templates | Medium-high | Moderate | One round-trip | Moderate | **Where most real work is** |
| 4 | LLM emits schema'd data | Medium-high | Good (test the renderer) | One round-trip | Moderate | **Where most real work is** |
| 5 | LLM generates code | Low | Near-impossible | High | High | Build-time only; runtime ~unshipped |

The brief that commissioned this paper hypothesized that most genuine adaptive-UI work happens in the middle, not at either end. The evidence supports it, and supports it more strongly than expected. The two highest-profile "generative UI" platforms to ship in 2025 — OpenAI's Apps SDK and the Vercel AI SDK's tool-rendering model — are both Rung 3–4: structured output rendered by developer-authored, deterministic components. Neither generates code at runtime. Vercel's documented retreat from its RSC primitive is, quite literally, a move *down* the spectrum from Rung 5 toward Rung 4. And Rung 1 still dominates by raw deployment volume — Adobe Target and Optimizely-class targeting runs on tens of thousands of sites, with the LLM-driven rungs a thin, fast-growing layer on top.

Two cautions about the spectrum as a model. First, real systems are hybrids, not points. The honest production picture is "a rule-based shell with one Rung-4 structured-output panel inside it," not a single architectural choice for a whole product. Second, "generative UI" as a vendor term is used to mean anything from Rung 2 to Rung 5, which inflates claims by design. The practical discipline for a buyer is to refuse the word and ask the decomposing question: *does the model select, compose, emit data, or emit code — and does it do so at build time or at runtime?* Four answers, and they have wildly different consequences.

---

## 2. LLM integration patterns

If the spectrum says *how generative* a system is, this section covers the mechanics — the actual integration patterns by which a model's output becomes an interface. There are five worth knowing, and they compose.

### 2.1 Tool calls as a UI primitive

The headline pattern, and the one most worth understanding conceptually, is the idea that an LLM "decides what UI to render" by calling a tool.

Here is what that actually means, stripped of mystique. The application developer defines a set of tools and, for each, writes the component that will display its result. The model is given the tool definitions. During a response, the model emits a *function call* — a tool name and a set of arguments — exactly as it would to call a weather API. The application intercepts that call, runs the tool (which returns structured data), maps the tool name to the pre-written component, and renders the component with the tool's output as its props. The model never emits an interface. It emits a *decision*: which tool, with which arguments. The rendering is entirely deterministic code the developer wrote in advance. "The LLM renders a component" is a convenient shorthand for "the LLM picks a function, and the function is bound to a component by a human."

This matters because it relocates the design control surface. The model's freedom is bounded by the catalog of tools and the schemas of their arguments. A designer who wants to constrain what can appear constrains the tool catalog. This is Rung 3–4 expressed as a programming model, and it is why those rungs are buildable and QA-able: the variability is real but enumerable.

The canonical reference is the Vercel AI SDK, which is instructive precisely because it has shipped two generations of this pattern and publicly preferred the second. The first generation, AI SDK RSC, used a `streamUI` primitive that streamed React Server Components directly from the model.[^4] The second generation — the production-recommended one as of AI SDK 5 (July 2025) and AI SDK 6 (December 2025) — exposes a typed `message.parts` array.[^12][^13] Tool calls appear as typed parts with an explicit lifecycle: `input-streaming`, `input-available`, `output-available`, `output-error`. The client switches on the part type and then on its state, showing a loading affordance at `input-available` and the real component at `output-available`. Vercel's own migration guide is unusually candid about why it walked the RSC approach back: streams could not be cleanly aborted, components flickered and remounted on completion, multiple Suspense boundaries could crash the app, and one streaming helper caused quadratic data transfer.[^11] The lesson is not that the RSC idea was foolish; it is that the more generative integration pattern was *less robust*, and a serious vendor chose reliability over the more impressive demo. A design-systems leader should read that as the shape of the whole field in miniature.

### 2.2 Structured outputs

Structured outputs are the mechanism underneath Rung 4, covered above: the model emits schema-conforming JSON, guaranteed by constrained decoding, and a deterministic renderer takes it from there.[^5][^6][^7] The pattern worth naming separately here is the *separation of concerns* it enforces. The model owns content and structure within the schema's bounds. The renderer owns pixels, accessibility, responsiveness, and brand. You test the renderer exhaustively once, then fuzz the schema. This is the cleanest available answer to "how do you QA a generative interface" — you make most of the interface not generative, and you make the generative part a data contract.

### 2.3 RAG as context grounding

Retrieval-augmented generation's role in adaptive UI is upstream and easy to misplace. RAG does not render anything. It injects retrieved context — user history, account data, documents, prior interactions — into the prompt, and that context shapes what the model emits, which in turn shapes the UI.[^17] In a Rung-4 system, retrieved user data becomes the context that a structured-output call turns into JSON, then UI. The 2025 framing trend renames this the "context layer" or "context engine," which is more honest about its function: RAG is the plumbing that makes an adaptive interface adaptive *to a specific person*, and it is where most of the personalization risk and most of the privacy exposure actually live (see Section 4). It is conceptually sound and thinly evidenced in published production case studies — a gap worth noting.

### 2.4 Multi-step and agentic flows

Adaptive interfaces increasingly interleave UI and action: show a component, take user input, perform an action, show another component. The AI SDK's agent abstractions run complete tool-execution loops, and because tool parts can render UI mid-loop, a flow can paint an interface, wait for a person, and continue.[^13] LangGraph emits UI components from graph nodes and persists UI state across steps, with explicit support for human-in-the-loop checkpoints.[^14] The design consequence is that the interface is no longer a destination; it is a series of surfaces materialized along the path of a process, some of them waiting for the user, some of them just reporting progress.

### 2.5 Streaming and progressive materialization

The final pattern — UI that builds up visibly while it is being generated — is large enough to be its own section, and gets one (Section 5). At the integration level the relevant primitive is partial structured output: the AI SDK's `streamObject` exposes a stream of progressively-completing, schema-valid objects, so a renderer can paint from incomplete-but-valid data.[^42] A telling refinement: AI SDK 3.4 added a mode that streams *by complete object* rather than by token, specifically because token-level partials caused layout shift.[^43] Even within streaming, the field is converging on more structure, not less.

### 2.6 The other SDKs, and an emerging interop layer

Vercel's AI SDK is the most complete first-class path for tool-call-to-component, but it is not alone. OpenAI contributes function calling plus the Apps SDK's widget layer, where the runtime is ChatGPT itself and the component runs in a sandboxed iframe bridged to the model over a message protocol.[^8] Anthropic's SDK provides tool use and strict structured outputs but no first-party UI renderer — you bring your own.[^6] LangChain and LangGraph provide graph-emitted UI. LlamaIndex contributes structured extraction that feeds a renderer but no native UI primitive.

The more strategically interesting development is a standardization layer forming underneath all of this. The Model Context Protocol (MCP) standardizes how applications expose context and tools to models, with tool selection mediated by natural-language descriptions interpreted at inference time; an extension, MCP Apps, standardizes interactive UI delivered *from* an MCP server.[^16] Separately, the AG-UI protocol aims to standardize the event stream between an agent backend and a frontend.[^15] None of these is settled, and a reader should treat "MCP will be the standard" as a *[speculative]* claim. But the direction is real: the industry is trying to agree on a wire format for "a model produced something that should become UI," and which format wins is a live question a leader should track rather than bet on.

---

## 3. Multimodal considerations

Web and mobile interfaces no longer assume a single input shape. An adaptive UI that adapts only its *content* while assuming a mouse is adapting along the wrong axis. This section walks the input modalities, what each contributes, what it costs, and — the part most discussions skip — how an interface should respond when the modality shifts mid-use.

### 3.1 Pointer and keyboard — the eroding default

Pointer and keyboard remain the implicit assumption of nearly every web framework, but they are now one modality among several rather than the baseline. The concrete failure this produces is *hover dependency*: affordances revealed only on hover — tooltips, hover menus, reveal-on-hover controls — have no touch equivalent. WCAG 2.2, a W3C Recommendation since October 2023, codified the response: Success Criterion 2.5.8 requires interactive targets of at least 24×24 CSS pixels (or equivalent spacing), and 2.5.7 constrains dragging-only interactions.[^18] This is now legally load-bearing in the EU, where the European Accessibility Act came into force in June 2025. The deeper point for adaptive UI is that *form factor is a weak proxy for input modality* — a touchscreen laptop is neither cleanly "desktop" nor "mobile" — yet most responsive systems still infer one from the other. An adaptive interface should treat modality as a signal to detect, not a fact to assume.

### 3.2 Touch and gesture

Touch contributes directness and spatial manipulation; gesture (swipe, pinch, pull-to-refresh) contributes screen economy. The dominant cost is discoverability: a gesture is an invisible affordance with no persistent signifier. The settled guidance, consistent across Apple's and Google's platform conventions, is that every gesture action must have a visible, non-gesture alternative, and that touch targets should be larger than the WCAG floor — Apple recommends 44×44 points, Material Design 48×48 dp.[^19] A second, subtler cost is the loss of haptic confirmation: without a physical detent, users distrust whether an action registered, which makes immediate visual feedback non-optional. When an adaptive UI detects a shift to touch, the right responses are mechanical: swap hover-reveal for tap-reveal or persistent controls, enlarge hit areas, and never leave a gesture as the only path to a function.

### 3.3 Conversational and typed natural language

Typed natural language is genuinely shipped at scale, and its contribution is real: it lets a user express intent without navigating an information architecture. Its failure mode is the *blank-prompt problem* — an empty text box communicates nothing about what the system can do or how to ask, shifting the entire discovery cost onto the user. The shipped mitigation is consistent across mature products: hybrid surfaces, where natural-language input sits alongside GUI controls — suggested prompts, chips, slot-filling forms — rather than replacing them. Conversation is an input modality, not an interface. Treating it as the whole interface is the most common design error in this space, and the foundation paper documented the practitioner voices who reject it — Karri Saarinen of Linear most bluntly, arguing that chat is "a very weak and generic form" and advocating a structured "workbench" that the AI augments rather than replaces.[^73]

### 3.4 Voice

Voice is where demo reality and shipped reality diverge most sharply, so precision matters. What *has* shipped: OpenAI's `gpt-realtime`, released as a production speech-to-speech model in August 2025, collapses the older speech-to-text → LLM → text-to-speech pipeline into a single model, cutting latency and preserving prosody, with reported figures around 500ms time-to-first-byte and 800ms voice-to-voice when well-configured.[^20] Google's Gemini Live shipped real-time voice with camera and screen-sharing across Android and iOS in mid-2025, on free and paid tiers, and handles interruptions.[^22] What has *not* shipped: genuinely overlapping, listen-while-speaking dialogue. OpenAI's Advanced Voice Mode is still turn-based — the user finishes, the model processes, the model responds; an interjection stops the model rather than letting it adapt.[^21] And the most-promised adaptive voice surface, a personalized context-aware Siri, has been announced, repeatedly delayed, and as of early 2026 remained unshipped.[^23] The honest summary for a client conversation: voice quality and latency have crossed the threshold of usability, but voice *turn-taking* — the thing that would make voice feel like conversation rather than walkie-talkie — is a 2026 roadmap item, not a shipped capability.

### 3.5 Vision and camera input

Camera input is genuinely shipped on both mobile platforms. Apple's Visual Intelligence (from iOS 18.2, December 2024) does text capture and translation, object identification, and event creation from what the camera sees, routing harder queries to external models.[^24] Google's Search Live, built on Project Astra, brings continuous live-feed multimodal understanding to Search.[^25] The architectural distinction worth holding onto: Google Lens operates on a *still image*, Astra-class systems on a *continuous feed* — a different latency and processing profile. Vision input is high-bandwidth and high-ambiguity, and its defining design requirement is a *grounding step*: the interface must surface what it believes it sees, because misrecognition is otherwise silent and the user has no error signal until it is too late.

### 3.6 Cross-device handoff — the under-discussed one

Cross-device continuity matters disproportionately for retail and SaaS clients — a customer starts on a phone and finishes on a desktop, or the reverse — and it is the area where the architectural gap is widest. There is no single mechanism. There are three incompatible ones.

The first is **OS-level proximity continuity**, exemplified by Apple's Handoff and Universal Clipboard. These work by *local device-to-device transfer*, not cloud sync: same account, Bluetooth and Wi-Fi on, devices physically near each other, with separate end-to-end-encrypted pairwise connections.[^26] The architectural consequence is that this continuity is *ephemeral and proximity-bound* — it passes a live activity state between two nearby devices and breaks when they are apart.

The second is **cloud account sync**, the model behind a retail "save cart across devices" feature. State is persisted server-side and reloaded on login from any device, anywhere; modern implementations use event-driven architectures to propagate changes across channels in near-real-time.[^28] This is the most mature cross-device pattern, and it is mature because the unit being synced — a cart, a list — is a well-defined data structure.

The third is **partial sync**, the model the AI assistants actually use, and the one most likely to surprise. ChatGPT syncs its *memory* across devices but does not sync *live conversation threads* in real time — the desktop app does not refresh an open thread without a restart, and switching devices mid-conversation loses live context.[^27] So "AI continuity" today is, precisely, eventual-consistency thread history plus persistent memory — not live session handoff.

The gap this exposes is genuine and citable. There is no cross-vendor standard for handing off an *adaptive or generative UI state* between devices, and the reason is structural: a generative UI state is not a document. It is a tuple of prompt, context, model output, and render. Nothing standard serializes that tuple. A retailer can sync a cart because a cart is data; nobody can yet sync "the in-progress generated interface you were looking at" because that interface has no canonical, transferable form. For a client whose customers move between devices mid-task, this is a real constraint to design around, not a solved feature to assume.

### 3.7 Ambient and proactive surfaces versus user-initiated

The last distinction is not an input modality but a *trigger model*, and it is architectural. A user-initiated surface is request/response: a user action starts a turn. An ambient or proactive surface is event-driven: the system runs continuously, watches signals — emails, calendar, logs, sensors — and surfaces only when a threshold is met. LangChain's articulation of "ambient agents" is the clearest available framing, and it makes a sharp claim: an ambient surface needs a fundamentally different container.[^29] A chat window assumes one active conversation; an ambient system has many concurrent open loops, so the proposed container is an *inbox*, modeled on email and ticketing, with explicit notify / ask / review interaction patterns because the user is not present at the moment of action. The shipped reality should be stated plainly: ambient agents are an emerging pattern with reference implementations, not a mainstream consumer-shipped UI; the strongest genuine production case is narrow — clinical documentation scribes. For an adaptive UI, the design implication of all of this is a single discipline: *name which mode the user is in, and do not change the interface in the wrong one*.

---

## 4. Memory and context architecture

An interface can only adapt to what it remembers. Where user state lives is therefore not a back-end detail — it determines what adaptation is possible, what it costs, and what legal and ethical obligations attach. There are five architectural options, they are usually combined, and the combination has consequences a design conversation rarely reaches.

### 4.1 The five places state can live

**Session-only.** State exists for one visit and is discarded. Architecturally trivial, privacy-friendly by default, and shallow — the system cannot recognize a returning user. It is the baseline against which every "memory" feature is defined.

**Persistent profile — the CDP.** A customer data platform unifies known and anonymous data into a single profile usable across channels in real time. Adobe's Real-Time CDP runs personalization at the network edge, evaluating a user's context in milliseconds against a localized edge profile store to avoid round-trips to a central hub.[^30] The profile is *structured and human-readable* — attributes, audience memberships, computed traits — which, as we will see, makes it the most legally tractable place to keep personalization data.

**Vector store — semantic memory.** Past interactions, preferences, and content are converted to embeddings and stored; on a new interaction the system embeds the current context and retrieves the most semantically similar prior items. This is what "semantic memory" means in practice. The relevant property — and the relevant problem — is that an embedding is not human-readable: you cannot read a phone number out of a vector, which sounds privacy-friendly and is in fact the opposite, for reasons in 4.3.

**The context window.** The simplest "memory": the conversation transcript, re-sent to the model each turn. Its limits are severe and routinely understated. The "lost in the middle" effect means models attend well to the start and end of their context and poorly to the middle, with accuracy drops exceeding 30% when relevant information sits mid-context.[^31] A 2025 study testing eighteen leading models found every one degraded as input grew — a phenomenon now called "context rot" — with effective recall falling well below advertised maximums.[^32] The context window is working memory, not durable memory, and an architecture that treats a long context as a substitute for a real memory store will quietly lose information.

**Hybrid.** Every shipped consumer memory feature combines the above: a structured store for durable attributes, a vector store for semantic recall, pre-computed summaries injected into the context window for cheap continuity, and the live transcript for the current turn.

### 4.2 How shipped memory features actually work

It is worth being concrete, because the shipped implementations are not what most people assume. ChatGPT's memory is *not* RAG. Independent reverse-engineering shows it maintains a frequently-updated, structured summary — a dossier covering response preferences, past-conversation highlights, user insights, and interaction metadata — and injects that summary into the system prompt of *every new chat*.[^33] There is no retrieval step; the memory invisibly conditions every output, including outputs where the user would not expect it.[^34] Claude's memory periodically distills durable facts from conversation history into a synthesized summary and announces when it draws on a memory; its Projects feature auto-loads instructions and documents into every conversation in a workspace. Gemini's personalization is different again — it is retrieval over a *pre-existing* data store (the user's Google account history), used only when the model judges it would help.[^35] Three vendors, three architectures. A leader should not assume "memory" means one thing.

### 4.3 Why the architecture choice is a governance choice

This is the part that is genuinely non-obvious, and it should change decisions.

Under GDPR's right to erasure, a user can demand deletion of their personal data. For a structured profile this is tractable: you delete a row. For a vector store it is hard, and the difficulty is not deletion mechanics but *discovery* — a user's information may have been embedded into vectors created from documents written *about* them, not by them, scattering their data across the store in forms no index will surface by name. Deletion is possible but requires deliberate engineering to find every touchpoint, de-index the vectors, and propagate through backups.[^36] And for data baked into model *weights* — through fine-tuning — erasure is, in the current state of the art, effectively unsolved: "machine unlearning" research through 2025 repeatedly found that unlearning does not truly remove knowledge from a trained network.[^37] The architectural rule that follows is concrete and should be stated to any client fine-tuning on user data: **never let raw personal data enter training data; keep personalization in retrievable, deletable stores** — a profile database, a vector store you control — not in weights. The same logic argues against the ChatGPT-style "remember everything" dossier: under GDPR's data-minimization and purpose-limitation principles, broad capture is harder to defend than scoped capture.

The regulatory perimeter has other non-obvious edges. California's finalized CCPA/CPRA regulations govern "automated decisionmaking technology," but the definition is narrow — it covers technology that *replaces or substantially replaces* human decision-making in *significant* decisions (finance, housing, employment, healthcare, education) and *explicitly excludes advertising*.[^38][^39] The consequence: most adaptive-UI personalization — layout, content, recommendations — falls *outside* that regime, but an adaptive UI that gates a loan application or a job flow pulls the entire system into scope. The EU AI Act's Article 50 transparency obligations, applying from August 2026, require disclosure when a user interacts with an AI system unless that fact is obvious; an open and unresolved interpretive question is whether content-marking obligations attach to an AI-*generated interface*, not just AI-generated media.[^40] And data residency is no longer free: Anthropic prices US-only inference at a 1.1× multiplier, and regional endpoints on the major clouds carry roughly a 10% premium.[^41] Every adaptive render that ships personal context to a model API is therefore both a compliance decision and a measurable line item.

The summary for a strategy conversation: the memory architecture is chosen by engineers, but it writes the privacy, residency, and portability story the legal and design teams will have to live with. It should be a deliberate, cross-functional decision, and it rarely is.

---

## 5. Streaming UI as a primitive

Most teams still hold a binary mental model of UI: it is either rendered or it is not, and the gap between is a spinner. Progressive UI materialization — interfaces that become visible and usable *while they are still being generated* — breaks that model, and it is novel enough to deserve treatment as a design primitive in its own right.

### 5.1 What it is and how it works

Three technical layers underpin streaming UI. The first is token streaming plus partial structured output: because a model emits tokens sequentially, a stream of progressively-completing, schema-valid objects can be exposed to the renderer, which paints from incomplete-but-valid data.[^42] The second is server-side component streaming: React Server Components serialize a component tree over a chunked response, with Suspense boundaries declaring which subtrees may be deferred, so the server flushes each subtree as it resolves — out of document order.[^44] The third is optimistic rendering: paint the expected end-state immediately, reconcile when the real data arrives.

The refinement mentioned earlier bears repeating because it is so telling. Vercel's AI SDK added a mode that streams *complete objects* rather than individual tokens, specifically because token-level partials produced layout shift — components were being asked to render from structurally-incomplete data and jumping around as it filled in.[^43] Even the streaming primitive is moving toward more structure, because structure is what makes the intermediate states legible.

### 5.2 What it looks like, shipped

The pattern is now visible across every major AI product. Anthropic's Artifacts render generated code and documents live, in a side-by-side panel, inside a sandboxed iframe with strict content-security policies; the design originated, by the team's own account, from the question "what if I could just see it right away."[^45] In April 2026 Anthropic extended this to Live Artifacts — persistent, auto-refreshing dashboards that re-pull current data on open.[^46] ChatGPT's Canvas opens an editable document beside the chat, edits it in place, and exposes a diff view and version history.[^47] Vercel's v0 streams JSX into a live preview while a post-processor scans for errors during generation. GitHub Copilot renders dimmed "ghost text" inline as the user types.[^48] The shared shape is unmistakable: generation is something the user *watches*, and increasingly something they can *edit alongside* and *interrupt*.

### 5.3 What it changes

Streaming UI changes three things about interaction.

It changes **latency tolerance**. The perceived-performance literature is consistent in direction: visible progress makes identical wait times feel shorter — skeleton screens are perceived as faster than spinners.[^49] (The specific percentages that circulate — "20% faster," "300ms" — are hard to trace to primary studies and should be cited as direction, not magnitude.) The principle transfers directly: a streamed reasoning trace or progressively-materializing layout buys a multi-second generation budget that an opaque spinner would never be granted.

It changes **interaction expectations**. Streaming reframes generation as a process the user observes and can abort — which is why every one of these products has a "Stop generating" control. The user is no longer waiting for a result; they are watching one form, and may decide early that it is not the one they wanted.

It changes the **visual language of "in progress."** "Pending" and "partial" become first-class UI states with their own vocabulary: skeletons and shimmer, token-by-token text reveal, staged Suspense-driven reveals where independent regions appear out of order as they resolve, and — newly — *reasoning traces shown as UI*, the collapsible "thinking" panels that turn latency into transparency. Linear has gone as far as codifying this into published Agent Interaction Guidelines — six principles that include explicit state transparency (an agent's thinking, waiting, and executing states must be inspectable) and disclosure of agency.[^74] Diff-streaming, where changes arrive as an accept/reject diff rather than a silent replacement, is becoming the default for anything that edits existing content.

### 5.4 The design consequence

The deepest consequence is for what a designer is designing. The unit is no longer "the finished screen." It is the screen's *trajectory* through partial states — empty, skeleton, partial, streaming, complete, and (with live artifacts) re-streaming on refresh. A component must be valid and legible at every intermediate state, not only at completion. This is a genuine expansion of the design surface, and it is the clearest example in this paper of an implementation reality that most design practice has not yet absorbed: the binary mental model is simply wrong now, and a design system that only specifies end-states is specifying a fraction of what ships.

---

## 6. Evaluation, QA, and governance

If the interface is generative, you cannot review every state, because the set of states is unbounded or at least uncountable. The traditional model of design QA — a designer signs off on every screen — does not degrade gracefully here; it breaks. The honest question is what replaces it, and the honest answer is that the replacement is borrowed wholesale from machine-learning evaluation, is genuinely shipping at some companies, and is immature in exactly the places that matter most to a design-systems leader.

### 6.1 The problem is real and acknowledged

Vercel states it directly: traditional software testing is insufficient for AI systems because their outputs are probabilistic — identical inputs produce varying outputs.[^50] A test that asserts "the button is at this position with this label" cannot express "the generated interface is acceptable." The replacement model the field has converged on is *eval-driven development*.

### 6.2 Evals as the replacement for screen-by-screen QA

Anthropic's published methodology is the most rigorous available primary source, and its structure is now widely shared.[^51] It uses three layers of grading: code-based graders (deterministic checks — does the output parse, do imports resolve, does a static accessibility scan pass), model-based graders (an LLM judging subjective dimensions against a rubric), and human graders (the gold standard, used to calibrate the LLM judges rather than to review everything). Golden datasets are built incrementally — the guidance is to start with twenty to fifty tasks drawn from real observed failures, not to wait for a comprehensive set. Evals check *outcomes* — the final state — rather than asserting intermediate steps. Non-determinism is measured rather than wished away, with metrics like `pass@k` (succeeds in k attempts) and the stricter `pass^k` (succeeds in all k). And the overall posture is a "Swiss cheese" model: automated evals, production monitoring, A/B testing, user feedback, and manual transcript review, each layer catching what the others miss.

The tooling is real and largely generally available. Anthropic's developer console has shipped an evaluation tool since 2024.[^52] OpenAI Evals exists as both an open-source framework and a platform product, with a documented set of grader types — string checks, text-similarity metrics, model-graded scores and labels, and arbitrary Python.[^53] A healthy open-source ecosystem surrounds them: Promptfoo (strong on red-teaming), Braintrust (used by Notion), LangSmith and Langfuse, DeepEval, Ragas (the standard for RAG evaluation), and Inspect, the rigorous framework from the UK's AI Security Institute.[^54][^56]

But here is the gap a design leader must not miss: **none of these frameworks is purpose-built for generative UI.** They evaluate text and agent outputs. Teams building generative interfaces adapt them by treating rendered output — generated code, a component tree, a DOM — as the artifact to grade. That works, but it means the QA infrastructure for adaptive UI is a retrofit, not a native tool. There is no "Figma for reviewing the distribution of generated interfaces," and the absence is felt.

### 6.3 The weakest link: accessibility at scale

This is the most important finding in the section, and it carries an irony the foundation paper sets up. That paper concluded the strongest *evidence* for adaptive UI is accessibility — the Gajos and Wobbrock work showing adaptive interfaces genuinely help users with motor and vision differences. This paper has to report that accessibility is the *weakest-tooled* part of generative-UI QA. Static accessibility scanners (axe-core, Pa11y) are mature for CI pipelines, but they assume a fixed set of screens to scan. When every render differs, you cannot pre-scan them all. The emerging answer — run an accessibility scan against each generated DOM inside the generation pipeline, as a code-based eval gate — is a logical extension but not yet a widely-published shipped practice, and academic work presented at ACM DIS 2025 treats accessible generative UI as an open research problem.[^59] The uncomfortable synthesis: the best reason to build adaptive UI is the hardest property to guarantee once it is generative. A leader making the accessibility case for adaptive UI should make it with that tension stated, not hidden.

### 6.4 Human-in-the-loop, telemetry, and red-teaming

Three more pieces complete the picture. *Human-in-the-loop review at thresholds* — escalating to human review only when an automated check flags risk or confidence is low — is well-articulated in research as "oversight-by-design" but thinly documented in production with concrete numbers; specific threshold configurations are rarely published.[^60] *Telemetry* becomes the primary post-ship signal: Notion has said roughly 80% of its AI team's work is driven by feedback and traces.[^57] The signal taxonomy is worth knowing — explicit feedback (thumbs, ratings, bug reports) and implicit feedback (abandonment, query reformulation, time-on-answer, and *regret signals*, such as a user editing every output despite a thumbs-up, which reveals a trust gap an explicit rating missed). The instrumentation layer is being standardized through OpenTelemetry's GenAI semantic conventions, though that spec is still marked experimental.[^58] *Red-teaming* — adversarial testing for manipulation, bias, and harmful output — is comparatively mature: Promptfoo generates adversarial inputs by vulnerability class and reports against frameworks like the OWASP LLM Top 10, and Microsoft's published study of red-teaming a hundred generative AI products is the definitive account, with the central lesson that testing has shifted from the model alone to the whole system.[^55]

### 6.5 Governance

The governance shift the foundation paper anticipated — from "did we follow the design system" to "did the system produce acceptable outcomes" — is real as a direction of travel and under-formalized as practice. The research found no design-system-specific, outcomes-based governance framework published. Governance for generative UI is currently assembled from general AI-governance practice plus eval and red-team tooling. Two companies have published enough to learn from: Notion, in detail (an "AI Data Specialist" role blending QA, prompt engineering, and product thinking; regression evals that catch breakage against prior models; frontier evals that assess new ones), and Vercel, on eval-driven development for v0 specifically. Two that the foundation paper held up as production exemplars — Linear and Granola — have published little or nothing on how they QA their AI features. That silence is itself a finding: the operational discipline of QA-ing generative UI is being practiced ahead of being documented, and a buyer should be skeptical of any vendor who describes their evals but cannot show them.

---

## 7. Cost, latency, and performance reality

Adaptive UI runs on tokens, and tokens cost money and time. This is the layer design conversations ignore most completely, and ignoring it produces business cases that collapse on contact with a finance review.

### 7.1 The token cost model, and how it compounds

Current per-million-token pricing for the frontier and mid-tier models, as of May 2026, spans a wide range. Anthropic: Claude Opus 4.7 at roughly $5 input / $25 output, Sonnet 4.6 at $3 / $15, Haiku 4.5 at $1 / $5.[^41] OpenAI: GPT-5.5 at roughly $5 / $30, GPT-5.4 at $2.50 / $15, and the Mini and Nano tiers far below that.[^61] Google: Gemini 3.1 Pro at roughly $2 / $12, Gemini 2.5 Flash at $0.30 / $2.50, Flash-Lite lower still.[^62] These figures move; the *ratios* are the durable insight.

Here is the compounding, made concrete. Take one modest adaptive render: 4,000 input tokens (a system prompt, the user's profile, retrieved context) and 1,000 output tokens. On Gemini 2.5 Flash that is roughly $0.0037 per render. At ten renders per session and one million sessions per month, that is about $37,000 per month — on the *cheapest viable* model. The identical workload on Claude Opus 4.7 is roughly $0.045 per render, or about $450,000 per month. **Model choice swings cost by roughly twelve times for an identical user experience.** That single fact should be in every adaptive-UI business case and almost never is.

### 7.2 Latency budgets

The interaction-design thresholds are old and stable: under ~200ms feels instant, under ~500ms feels responsive, beyond ~1s is noticed, beyond ~2s frustrates. Generative UI runs straight into them. A full model completion commonly takes two to eight seconds; a reasoning model can take 45 to 120 seconds merely to *begin* responding. A generative UI that blocks first paint on a full completion therefore violates the interaction budget by an order of magnitude. There are only three ways out, and they are the patterns from Section 5: stream (so the user sees progress and the budget that matters becomes time-to-first-token), render optimistically or with skeletons (so something appears immediately), or pre-compute (so the common cases were generated in advance). One contrarian note worth holding lightly: at least one vendor study suggests a *slightly* slower agent response can read as "more thoughtful" — latency perception is not perfectly linear — but this is a single study and should not be built on.

### 7.3 Caching

Caching is the main lever, and its realities are less rosy than vendor copy. Exact-match caching — key on a hash of the prompt — catches only a small fraction of redundant calls (one analysis put it near 18%) because users rephrase.[^63] Semantic caching — embed the query, retrieve a cached response if similarity clears a threshold — does better, but realistic production hit rates land in the 20–45% range, not the 95% sometimes claimed; FAQ-style traffic reaches the higher end.[^63] Provider-side prompt caching is the most reliable win: it caches a stable *prefix* of the prompt, and the discounts are real — OpenAI prices cached input at roughly half, Anthropic prices a cache *read* at about a tenth of the base input rate.[^64][^41] The design-relevant consequence is concrete: order the prompt so the *stable* parts come first — system instructions, design tokens, component schemas — and the *volatile* per-user context comes last, so the stable prefix hits the cache on every request.

### 7.4 Model choice and the "good enough" calculus

Not every render needs a frontier model. Across enterprise workloads, only an estimated 25–35% of queries genuinely require frontier capability.[^65] Two patterns exploit this: *routing* (send each query to one appropriately-sized model) and *cascading* (try a small model first, escalate only if its output fails a quality bar). Reported savings run 45–85% with most of the quality retained. Notion has described doing exactly this in production — routing by task category, sending long-form reasoning to frontier models while high-volume tasks like database field auto-population go to small, fine-tuned, cost-efficient ones.[^78] The "good enough" calculus that production teams actually run treats quality, cost, and latency as a single joint optimization: use the smallest model that clears the bar for each class of query, reserve frontier models for the hard minority, layer caching on top, and stream to stay inside the latency budget. And the strongest cost lever of all, for adaptive UI specifically, is the one a designer controls: *do not generate UI when you do not have to*. Pre-compute and template-cache the common layouts; reserve live generation for the genuinely novel states. An adaptive interface that generates every surface from scratch is not sophisticated — it is unbudgeted.

---

## 8. Authoring tooling and the design workflow

When the output is not a fixed screen, what does the design tool look like? The honest answer, stated plainly because the brief asked for honesty: there is no mature design tool for variable output, and every current approach is a workaround. Designers still author fixed artifacts; the generative layer is bolted on afterward.

### 8.1 The current workarounds

**Figma plus prompts.** Figma announced its AI suite in mid-2024; the layout-generation feature was suspended shortly after launch when it produced output strikingly close to an existing Apple app, exposing that the model reproduced training data rather than designing.[^66] Figma Make, a prompt-to-code tool, reached general availability in July 2025.[^67] Its limits are admitted and instructive: the exported code is not tied to a production design system, it is commonly described as non-production-grade, credit limits cap iteration, and — tellingly — once a user makes a manual edit, prompt-based editing breaks. Most important: Figma Make generates a *fixed prototype per prompt*. It is a faster way to produce one artifact. It is not a tool for designing a system that renders variably.

**Storybook plus an eval suite.** This is the most credible *component-driven* generative workflow shipping today. Storybook now positions itself explicitly for AI agents: components, props, stories, and docs define what an agent is allowed to build; Storybook's test runner executes generated stories in a real browser and sends failures back to the agent to fix; and an MCP add-on exposes the design system to agents as a set of selectable, documented tools.[^68] This is genuinely useful — it makes Storybook both a *constraint* (reuse real components) and a *feedback loop* (tests as evals). But note what it governs: *which components an agent uses*. It does not help a designer *specify and review variability*.

**v0-style prompt-to-UI tools.** v0, Lovable, Bolt, and Replit Agent generate UI or whole apps from prompts. They are real and useful for prototyping. Their shared shortfall for design teams is what practitioners call the "70% problem": users hit a complexity ceiling and must drop into hand-editing code, and the tools are single-shot generators of fixed artifacts, not authoring environments for variable systems.[^69]

### 8.2 The unsolved problem

The genuinely unsolved problem is *designing for variability*. The clearest vocabulary for it comes not from industry but from academic HCI: a recent systematic review names it "variability by design" and describes the shift it demands — a designer moves from *visual authorship* (drawing the screen) to *architectural intent* (specifying modular components, behavioral rules, and interface policies, and letting the system compose).[^70] What is missing is the tool. No design tool lets a designer specify a *space* of possible outputs and review the *distribution* of what that space produces. Review today is sampling individual generations by eye — which, for an unbounded output space, is closer to spot-checking than to QA. There is no equivalent of a design spec for non-deterministic rendering. The academic field has at least identified the missing review primitive: UICrit, a UIST 2024 dataset of several thousand professional design critiques over hundreds of mobile UIs, was explicitly proposed as a reward model for evaluating generated interfaces — the kind of automated-critique infrastructure that practitioner tooling does not yet have.[^77] The idea sometimes floated as the new design artifact — a "component-prompt-pair," the component bundled with a machine-readable description of when and how to use it — is a reasonable direction and has no established literature or tooling behind it yet; it is a proposal, not a practice. A leader should budget and plan with this gap in full view: the design workflow for adaptive UI is currently code-first, with designers participating through prompts, component contracts, and the eval loop rather than through a canvas. That may change. It has not changed yet.

---

## 9. Design system implications

The design system is one consideration in this paper, not its spine — but it is the consideration most likely to land on a design-systems leader's desk, so it earns a focused section. The foundation paper argued the design system survives the shift to adaptive UI and becomes *more* load-bearing, not less. The implementation reality bears that out, and sharpens it into four concrete shifts.

**Primitives over composed components.** The industry has moved decisively toward headless primitives, and the move is partly driven by what LLMs compose well. Radix UI and, especially, shadcn/ui — primitives plus Tailwind, distributed as copy-paste source rather than an installed package — have become, in one analyst's phrase, the default UI library of LLMs, and v0, Bolt, and Lovable all build on that base.[^71] The reason is mechanical: when the model can see and shape all the code, it composes more reliably than when it must work through the fixed API and theming constraints of an opinionated library. The implication for a design system is uncomfortable but clear — a system architected as a closed catalog of heavily-composed components (the MUI model) is *less* adaptable to LLM composition than one architected as open, primitive-level, fully-visible code (the headless/Tailwind model).

**Semantic component contracts.** For an LLM to select a component, the component must describe *what it does* — its intent, the context it needs, its alternatives — not merely how it looks. This is the "intent metadata" the foundation paper named. The mechanism is emerging through MCP: tool selection is mediated by natural-language descriptions interpreted at inference time, and Storybook's MCP add-on is the concrete shipped example of a design system exposed to agents as documented, selectable tools.[^68][^16] There is no ratified standard for component intent metadata yet. Building toward one — even informally, as structured descriptions attached to each component — is the highest-leverage design-system investment for adaptive UI.

**Evals replacing QA.** Covered in Section 6, and it is the operational answer to "how does a design system enforce quality when output varies." It enforces it the way Notion does: continuous, automated evaluation as the QA function, with humans calibrating the judges rather than reviewing every screen.

**Governance shifts from compliance to outcomes.** The question a design system asks moves from "did this screen follow the system" to "did the system produce an acceptable outcome." This is a real change in what governance *means*, and — as Section 6 noted — it is under-formalized; no purpose-built framework exists. The foundation paper's recommendation stands and belongs here as the implementation note: the system prompt becomes a versioned, reviewed design artifact, and variant logging — a record of which generated variant was served to which user, and why — becomes infrastructure, both for debugging and for the auditability that the EU AI Act's effect-based enforcement will eventually require. No vendor has published a good reference implementation of variant logging. That remains a genuine gap, and possibly an opportunity.

The synthesis: the components stay consistent; the compositions vary, within rules the design system encodes; and "consistency" comes to mean *the user can predict and trust the surface* rather than *every user sees the same surface*. The design system is the constraint set that keeps adaptive UI from collapsing into chaos. It does not shrink. It moves up a level — from specifying pixels to specifying the space of acceptable outcomes — and that is more demanding work, not less.

---

## 10. Where this might be headed *[speculative]*

Everything in this section is labeled speculation because it is. It is distinguished from the evidence above deliberately.

*[speculative]* **The middle of the spectrum stays where the work is.** Rung 3–4 — slot-based generation, structured output rendered by deterministic components — remains the dominant production shape for the next two to three years. Runtime code generation (Rung 5) does not become a mass-market pattern in that window, because the QA, cost, latency, and safety problems are not close to solved and the constrained patterns keep working well enough. The brief that commissioned this paper guessed the action was in the middle; the safest forecast is that it stays there.

*[speculative]* **An interop standard consolidates — but which one is genuinely open.** The strongest standardization signal is MCP and its UI extensions, with AG-UI and the AI SDK's `message.parts` as the other contenders. Some convergence on a wire format for "a model produced something that should become UI" is likely within two to three years, because the fragmentation is expensive for everyone. Betting on the *winner* now is premature; tracking the race is not.

*[speculative]* **The authoring-tool gap gets filled — or it doesn't, and that is itself the answer.** Either someone ships the missing tool — one that lets a designer specify a variability space and review the distribution of its outputs — because the gap is too obvious to leave open, or the workflow stays permanently code-first and the design role reshapes around prompts, contracts, and evals rather than a canvas. Both are plausible. The second is the current trajectory, and trajectories are sticky.

*[speculative]* **Falling token prices weaken the economic objection without removing it.** Model prices have fallen steadily, and a render that costs a fraction of a cent today may cost a tenth of that in two years. That makes more live generation affordable. It does not touch the QA, accessibility, and governance costs, which are human and structural and do not fall with token prices. The economic case for pre-computing and caching common layouts survives even cheap tokens.

*[speculative]* **Recommendation practice and generative practice converge at the layout level.** The fifteen-year-old, bandit-driven personalization stack and the new generative stack are converging — first on content, increasingly on *layout*. Expect the incumbent personalization vendors to ship layout-generation primitives, and expect the resulting systems to look like Rung 3–4 with a recommendation engine doing the selection.

What is hype, stated as plainly as the speculation: the framing that "every interface will be unique to every user" remains, as the foundation paper argued, destructive for any product where people discuss, share, or teach the interface to one another — and that framing will not survive the cost model in Section 7 even where it survives the social objection. The framing that "AI will design the interface" describes Rung 5 at runtime, which this paper has shown is nearly empty in production. The durable shape is less dramatic and more buildable: deterministic shells, constrained generation inside them, evals where QA used to be, and a design system doing more work than ever.

---

## Open questions

1. **Will an interoperability standard actually consolidate, and which one?** MCP and MCP Apps, AG-UI, and the AI SDK's `message.parts` are competing, informally, to be the wire format for model-produced UI. The research could not establish a clear front-runner. If fragmentation persists, every adaptive-UI project pays an integration tax indefinitely; if one wins, the timing of that win is a real strategic variable. Unresolved.

2. **Is accessibility-at-scale for generative UI solvable with current tooling, or does it need something new?** In-pipeline DOM scanning is the obvious extension of existing scanners, but it only catches what automated scanners catch — and automated scanners miss the judgment-dependent failures (meaningful alt text, cognitive load, assistive-technology behavior). Whether generative UI can ever meet the accessibility bar that is its own strongest justification is genuinely open, and it is the most important unresolved question in this paper.

3. **What does good variant logging look like?** The foundation paper flagged this; the implementation research confirms that no vendor or industry body has published a reference design — what is logged, who holds it, who can audit it, how long it is retained. The EU AI Act's effect-based enforcement will eventually demand it. Nobody has built the obvious version of it in public.

4. **Does the authoring tool get built?** Section 8's gap is real and unfilled. Whether it is a fillable gap — whether "designing a variability space and reviewing its output distribution" is even a coherent tool concept — or whether the design role simply migrates into the code-and-eval workflow is unresolved, and the answer reshapes the design profession either way.

5. **Can generative UI state be made portable across devices?** Section 3's cross-device gap traces to a serialization problem: a generative UI state is a prompt-context-output-render tuple with no canonical transferable form. Whether anyone defines such a form — or whether cross-device adaptive UI is simply re-generated from synced context on each device — is open, and it matters most for exactly the retail and SaaS clients who care most about continuity.

6. **How much does the cost curve actually change the architecture?** If tokens get cheap enough, does the spectrum's center of gravity drift toward Rung 5, or do the non-token costs (QA, accessibility, governance) hold it in the middle permanently? This paper bets on the latter, but it is a bet.

---

## What to read next — ranked

1. **Anthropic, *Demystifying evals for AI agents*** (Grace, Hadfield, Olivares, De Jonghe; January 2026). The most rigorous published methodology for QA-ing generative systems. Read first if you need to know what replaces design QA.[^51]
2. **Vercel, *Migrating from RSC to UI*** (AI SDK documentation) and the **AI SDK 5** release post (July 2025). The candid, technical account of the architecture walk-back that defines this paper's central finding.[^11][^12]
3. **Linear, *How we built Triage Intelligence*** (September 2025). The most concrete published account of shipping an adaptive AI feature end to end — model evolution, the search/rank/reason pipeline, the explicit latency-for-capability trade.[^72]
4. **Vercel, *Eval-driven development: Build better AI faster*** (October 2024). The clearest published account of QA for an actual generative-UI product, v0.[^50]
5. **OpenAI, Apps SDK documentation** (2025–2026). The build documentation for the largest-scale Rung-4 deployment in existence; the data-tool/render-tool separation is the pattern to internalize.[^8]
6. **Chen et al. (Stanford), *Generative Interfaces for Language Models*** (arXiv, 2025). The strongest contribution on *how to evaluate* generative UI — multidimensional, comparative, benchmark-backed.[^76]
7. **LangChain, *Introducing ambient agents*** (January 2025). The clearest articulation of the ambient-versus-user-initiated architectural split and the inbox-shaped container it implies.[^29]
8. **Simon Willison, *I really don't like ChatGPT's new memory dossier*** (May 2025). A careful reverse-engineering of how a shipped memory feature actually works — system-prompt injection, not RAG.[^33]
9. **Kyungho Lee, *Towards a Working Definition of Designing Generative User Interfaces*** (arXiv / DIS '25, May 2025). The vocabulary the industry lacks for the authoring problem — "variability by design," architectural intent over visual authorship.[^70]
10. **Microsoft, *Lessons from Red Teaming 100 Generative AI Products*** (January 2025). The definitive published account of adversarial testing for generative systems.[^55]

---

## What surprised me

Eight findings that shifted my view in the course of this research.

1. **The generative end of the spectrum is nearly empty in production.** I expected Rung 5 — runtime code generation — to be a small but real category. It is essentially not a category at all on consumer web and mobile. v0 and its peers are build-time tools. The vivid demo that names the whole field describes almost nothing that ships.

2. **The company that coined "generative UI" walked its own architecture back, toward less generation.** Vercel's retreat from AI SDK RSC to typed tool parts is documented, technical, and candid — and the replacement is more robust *because* it is more constrained. The most important implementation fact in this paper is a vendor choosing reliability over its own best demo.

3. **The cost gap between models is roughly twelve-to-one for an identical user experience.** I knew model choice mattered. I did not expect the spread to be that wide, or for per-render generation at consumer scale to land in the six-to-seven-figure-monthly range so easily. This belongs in every business case and is in almost none.

4. **"Right to be forgotten" is structurally near-impossible for model weights and genuinely hard for embeddings.** Machine-unlearning research keeps finding that unlearning does not actually remove knowledge. This should be changing memory-architecture decisions — keep personalization in deletable stores, never in weights — and mostly it has not.

5. **Shipped memory features are not RAG.** ChatGPT injects a structured dossier into the system prompt of every chat. There is no retrieval step. The memory invisibly conditions every output. I had assumed semantic retrieval; the reality is closer to a always-on profile paragraph.

6. **The QA toolchain is borrowed wholesale from ML evaluation.** There is no UI-native QA infrastructure for generative interfaces. Teams retrofit text-and-agent eval frameworks by treating rendered code as the artifact to grade. It works, but the absence of a purpose-built tool is conspicuous.

7. **Authoring tooling genuinely does not exist as a category — and academia has the better vocabulary for the problem.** "Variability by design," "architectural intent over visual authorship" — the HCI literature has named the problem more precisely than industry has, while industry has shipped no tool that addresses it. That is an unusual gap.

8. **Accessibility is simultaneously the strongest argument for adaptive UI and the hardest thing to QA once it is generative.** The foundation paper found accessibility is the load-bearing evidence base for adaptive UI. This paper found accessibility-at-scale is the weakest-tooled part of generative-UI QA. The best reason to build the thing is the hardest property to guarantee in the thing. That tension should be stated in every conversation, not resolved away.

---

## Bibliography

[^1]: Optimizely. (accessed 2026, May). *Interactions between flag rules* and *Manage rules in Optimizely Feature Experimentation.* Optimizely Developer Documentation. https://docs.developers.optimizely.com

[^2]: Adobe. (accessed 2026, May). *Rules-based personalisation for better targeting.* Adobe Business. https://business.adobe.com

[^3]: Adobe. (accessed 2026, May). *What is On-Device Decisioning?* Adobe Experience League. https://experienceleague.adobe.com

[^4]: Vercel. (2024, March). *Introducing AI SDK 3.0 with Generative UI support.* Vercel Blog. https://vercel.com/blog/ai-sdk-3-generative-ui

[^5]: OpenAI. (2024, August 6). *Introducing Structured Outputs in the API.* OpenAI. https://openai.com/index/introducing-structured-outputs-in-the-api/

[^6]: Anthropic. (accessed 2026, May). *Structured outputs.* Claude Developer Platform Documentation. https://platform.claude.com/docs/en/build-with-claude/structured-outputs

[^7]: Vercel. (accessed 2026, May). *AI SDK Core: Generating Structured Data.* AI SDK Documentation. https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data

[^8]: OpenAI. (accessed 2026, May). *Build your ChatGPT UI — Apps SDK.* OpenAI Developers. https://developers.openai.com/apps-sdk/build/chatgpt-ui

[^9]: OpenAI. (2025, November 13). *Introducing apps in ChatGPT and the Apps SDK.* OpenAI. https://openai.com/index/introducing-apps-in-chatgpt/

[^10]: Vercel. (accessed 2026, May). *v0.* https://v0.app

[^11]: Vercel. (accessed 2026, May). *Migrating from RSC to UI.* AI SDK Documentation. https://ai-sdk.dev/docs/ai-sdk-rsc/migrating-to-ui

[^12]: Vercel. (2025, July 31). *AI SDK 5.* Vercel Blog. https://vercel.com/blog/ai-sdk-5

[^13]: Vercel. (2025, December 22). *AI SDK 6.* Vercel Blog. https://vercel.com/blog/ai-sdk-6

[^14]: LangChain. (accessed 2026, May). *How to implement generative user interfaces with LangGraph.* LangChain Documentation. https://docs.langchain.com

[^15]: CopilotKit. (2025). *Introducing AG-UI: The Agent–User Interaction Protocol.* CopilotKit. https://copilotkit.ai

[^16]: Model Context Protocol. (2025–2026). *Specification* and *MCP Apps (SEP-1865).* https://modelcontextprotocol.io

[^17]: *A Systematic Literature Review of Retrieval-Augmented Generation.* (2025, August). arXiv. https://arxiv.org/pdf/2508.06401

[^18]: W3C. (2023, October). *Understanding Success Criterion 2.5.8: Target Size (Minimum).* Web Content Accessibility Guidelines 2.2. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

[^19]: UXPin. (2025). *Responsive Design for Touch Devices.* UXPin Studio Blog. https://www.uxpin.com/studio/blog/responsive-design-touch-devices/

[^20]: OpenAI. (2025, August 28). *Introducing gpt-realtime and Realtime API updates for production voice agents.* OpenAI. https://openai.com/index/introducing-gpt-realtime/

[^21]: Datastudios. (2025, June). *ChatGPT's Advanced Voice Mode Upgrade.* Datastudios. https://www.datastudios.org/post/chatgpt-s-advanced-voice-mode-upgrade-june-2025

[^22]: Google Workspace Updates. (2025, May). *Conduct in-depth two-way conversations with Gemini Live.* https://workspaceupdates.googleblog.com/2025/05/gemini-live-in-depth-two-way-conversations.html

[^23]: TechCrunch. (2026, February 11). *Apple's Siri revamp reportedly delayed again.* https://techcrunch.com/2026/02/11/apples-siri-revamp-reportedly-delayed-again/

[^24]: Apple. (2025). *Use visual intelligence on iPhone.* Apple Support. https://support.apple.com/guide/iphone/use-visual-intelligence-iph12eb1545e/ios

[^25]: TechCrunch. (2025, May 20). *Project Astra comes to Google Search, Gemini, and developers.* https://techcrunch.com/2025/05/20/project-astra-comes-to-google-search-gemini-and-developers/

[^26]: Apple. (2024–2025). *Use Handoff to continue tasks* and *Continuity features and requirements.* Apple Support. https://support.apple.com/en-us/102426

[^27]: OpenAI Developer Community. (2025). *Real-Time Conversation Sync Across Devices for Seamless Multi-Device Use.* https://community.openai.com/t/real-time-conversation-sync-across-devices-for-seamless-multi-device-use/1021452

[^28]: Adobe Commerce. (2025). *Cart persistence.* Adobe Experience League. https://experienceleague.adobe.com/en/docs/commerce-admin/stores-sales/point-of-purchase/cart/cart-persistent

[^29]: LangChain. (2025, January 14). *Introducing ambient agents.* LangChain Blog. https://blog.langchain.com/introducing-ambient-agents/

[^30]: Adobe. (accessed 2026, May). *Real-Time Customer Data Platform Overview* and *The architecture behind Adobe Real-Time CDP.* Adobe Experience League / Adobe Business. https://business.adobe.com/blog/the-architecture-behind-adobe-real-time-cdp

[^31]: Liu, N. F., et al. *Lost in the Middle: How Language Models Use Long Contexts.* (Discussed via Morph, *Context Rot,* accessed 2026, May. https://morphllm.com/context-rot)

[^32]: Chroma Research. (2025). *Context Rot* study of 18 LLMs. (Summarized via Morph and Product Talk, accessed 2026, May.)

[^33]: Willison, S. (2025, May 21). *I really don't like ChatGPT's new memory dossier.* simonwillison.net. https://simonwillison.net/2025/May/21/chatgpt-new-memory/

[^34]: OpenAI. (2025, April). *Memory and new controls for ChatGPT.* OpenAI. https://openai.com/index/memory-and-new-controls-for-chatgpt/

[^35]: Google. (2025, March). *Gemini gets personal, with tailored help from your Google apps.* Google Blog. https://blog.google/products-and-platforms/products/gemini/gemini-personalization/

[^36]: Amazon Web Services. (2024). *Implementing Knowledge Bases for Amazon Bedrock in support of GDPR (right to be forgotten) requests.* AWS Machine Learning Blog. https://aws.amazon.com/blogs/machine-learning/

[^37]: *Does Machine Unlearning Truly Remove Knowledge?* (2025). arXiv:2505.23270. https://arxiv.org/abs/2505.23270

[^38]: California Privacy Protection Agency. (2025, September). *California Finalizes Regulations to Strengthen Consumers' Privacy.* CPPA. https://cppa.ca.gov/announcements/2025/

[^39]: Skadden, Arps, Slate, Meagher & Flom. (2025, October). *California Finalizes CCPA Regulations for Automated Decision-Making Technology.* Skadden Insights. https://www.skadden.com/insights/publications/2025/10/california-finalizes-cppa-regulations

[^40]: Covington & Burling (Inside Global Tech). (2026, May 12). *10 Takeaways: European Commission Draft Guidelines on AI Transparency under the EU AI Act.* https://www.insideglobaltech.com

[^41]: Anthropic. (accessed 2026, May). *Pricing.* Claude Developer Platform Documentation. https://platform.claude.com/docs/en/about-claude/pricing

[^42]: Vercel. (2025). *AI SDK Core: streamObject.* AI SDK Documentation. https://ai-sdk.dev

[^43]: Vercel. (2024). *AI SDK 3.4.* Vercel Blog. https://vercel.com/blog/ai-sdk-3-4

[^44]: React. *<Suspense> reference* (https://react.dev/reference/react/Suspense) and React Working Group, *New Suspense SSR Architecture in React 18* (https://github.com/reactwg/react-18/discussions/37).

[^45]: Orosz, G. (2024). *How Anthropic built Artifacts.* The Pragmatic Engineer. https://newsletter.pragmaticengineer.com/p/how-anthropic-built-artifacts

[^46]: Anthropic. (2026, April 20). *Use live artifacts in Claude Cowork.* Claude Help Center. https://support.claude.com

[^47]: OpenAI. (2024, October 3). *Introducing canvas.* OpenAI. https://openai.com/index/introducing-canvas/

[^48]: Visual Studio Code. (2025, February 12). *Copilot Next Edit Suggestions* and *Inline suggestions from GitHub Copilot.* https://code.visualstudio.com/docs/copilot/ai-powered-suggestions

[^49]: LogRocket. (2024). *Skeleton loading screen design.* LogRocket Blog. https://blog.logrocket.com/ux-design/skeleton-loading-screen-design/

[^50]: Vercel. (2024, October 17). *Eval-driven development: Build better AI faster.* Vercel Blog. https://vercel.com/blog/eval-driven-development-build-better-ai-faster

[^51]: Grace, M., Hadfield, J., Olivares, R., & De Jonghe, J. (2026, January 9). *Demystifying evals for AI agents.* Anthropic Engineering. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

[^52]: Anthropic. (2024, July 9). *Evaluate prompts in the developer console.* Anthropic. https://www.anthropic.com/news/evaluate-prompts

[^53]: OpenAI. (accessed 2026, May). *Graders* and *Evaluating model performance.* OpenAI Developers. https://developers.openai.com/api/docs/guides/graders

[^54]: Promptfoo. (accessed 2026, May). *Red teaming.* Promptfoo Documentation. https://www.promptfoo.dev/docs/red-team/

[^55]: Microsoft. (2025, January 13). *Lessons from Red Teaming 100 Generative AI Products.* Microsoft Security Blog / arXiv:2501.07238. https://arxiv.org/abs/2501.07238

[^56]: UK AI Security Institute. (2024, April; ongoing). *Inspect: An open-source framework for large language model evaluations.* https://github.com/UKGovernmentBEIS/inspect_ai

[^57]: Sachs, S. (Notion), via Braintrust. (2025). *How Notion evaluates AI at scale.* Braintrust Blog. https://www.braintrust.dev/blog/notion

[^58]: OpenTelemetry. (accessed 2026, May). *Semantic conventions for generative AI.* OpenTelemetry Documentation. https://opentelemetry.io/docs/specs/semconv/gen-ai/

[^59]: *Good Accessibility, Handcuffed Creativity: AI-Generated UIs Between Accessibility Guidelines and Practitioners' Expectations.* (2025). Proceedings of ACM DIS 2025. https://dl.acm.org/doi/10.1145/3715336.3735691

[^60]: *Human Oversight-by-Design for Accessible Generative Intelligent User Interfaces.* (2026). arXiv:2602.13745.

[^61]: OpenAI. (accessed 2026, May). *API Pricing.* OpenAI Developers. https://developers.openai.com/api/docs/pricing

[^62]: Google. (accessed 2026, May). *Gemini Developer API pricing.* Google AI for Developers. https://ai.google.dev/gemini-api/docs/pricing

[^63]: TianPan. (2026, April). *Semantic Caching for LLM Applications: What the Benchmarks Don't Tell You.* tianpan.co. https://tianpan.co/blog/2026-04-09-semantic-caching-llm-production

[^64]: OpenAI. (2024). *Prompt Caching in the API.* OpenAI. https://openai.com/index/api-prompt-caching/

[^65]: TianPan. (2025, November). *LLM Routing and Model Cascades.* tianpan.co. https://tianpan.co/blog/2025-11-03-llm-routing-model-cascades

[^66]: Figma. (2024, June 26). *Meet Figma AI: Empowering Designers with Intelligent Tools.* Figma Blog. https://www.figma.com/blog/introducing-figma-ai/

[^67]: Figma. (2025, July 24). *Figma Make is now available to all users.* Figma Blog. https://www.figma.com/blog/figma-make-general-availability/

[^68]: Storybook. (accessed 2026, May). *Storybook for AI.* https://storybook.js.org/ai

[^69]: Osmani, A. (2025). *AI-Driven Prototyping: v0, Bolt, and Lovable.* addyo.substack.com. https://addyo.substack.com

[^70]: Lee, K. (2025, May 21). *Towards a Working Definition of Designing Generative User Interfaces.* arXiv:2505.15049 / DIS '25 Companion. https://arxiv.org/abs/2505.15049

[^71]: Holterhoff, K. (2025, April 22). *UI Component Libraries, shadcn/ui, and the Revenge of Copypasta.* RedMonk. https://redmonk.com

[^72]: Linear. (2025, September 3). *How we built Triage Intelligence.* Linear. https://linear.app/now/how-we-built-triage-intelligence

[^73]: Saarinen, K. (2025, April 7). *Design for the AI age.* Linear. https://linear.app/now/design-for-the-ai-age

[^74]: Linear. (2025, July). *Agent Interaction Guidelines.* Linear Developers. https://linear.app/developers/aig

[^75]: Leviathan, Y., Valevski, D., Kalman, M., et al. (2025). *Generative UI: LLMs are Effective UI Generators.* arXiv / Google Research. https://generativeui.github.io

[^76]: Chen, J., Zhang, Y., Zhang, Y., Shao, Y., & Yang, D. (2025). *Generative Interfaces for Language Models.* arXiv:2508.19227. https://arxiv.org/abs/2508.19227

[^77]: Duan, P., et al. (2024, October). *UICrit: Enhancing Automated Design Evaluation with a UI Critique Dataset.* Proceedings of UIST '24 / arXiv:2407.08850. https://arxiv.org/abs/2407.08850

[^78]: Notion. (2025, May 29). *Speed, Structure, and Smarts: The Notion AI Way.* Notion Blog. https://www.notion.com/blog

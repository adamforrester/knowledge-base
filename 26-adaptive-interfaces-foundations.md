---
type: practice-area
title: Adaptive Interfaces - Foundations
description: Six lineages of adaptive UI, Sentient Design as adopted vocabulary, the Sentient Triangle, four-tier pattern catalogue, agent typology, personalization vs. adaptation, EU AI Act Article 5.
tags: [extension, ai, adaptive-ui, sentient-design, governance]
timestamp: 2026-06-10
---

# 26 — Adaptive Interfaces (Foundations)

> Adaptive UI is not one thing. Six overlapping lineages — sentient design, generative UI, personalization-incumbent practice, malleable software, academic ability-based design, and agentic UX — currently compete for the same vocabulary, and clients increasingly arrive at our door asking for "AI features" in language that flattens the distinctions. This file is the foundations layer: what each lineage actually claims, what the evidence supports, where the field is converging vs. diverging in 2026, and the strategic shape an agency practice should take. The companion file is 27-adaptive-interfaces-implementation, which covers how the architecture actually gets built. Together they are the (b)-axis sibling to 15-ai-in-ds (AI operating the DS) and 25-ai-aware-patterns-and-conversational-ui (AI patterns the DS ships). Adaptive interfaces are the third axis — interfaces that *reshape themselves* in real time around the user, the moment, and the task.

---

## A note on currency before anything else

This file dates fast in the same way 15-ai-in-ds does, and for the same reasons. Specific products (Vercel v0, Linear AI, Notion, Granola, Dia, Apple Intelligence), regulatory dates (EU AI Act Article 5 effective 2 February 2025; Article 50 fully applicable 2 August 2026; California SB 942 and AB 2013 operative January 2026; Colorado SB24-205 operative February 2026), and headline claims (Adobe's 2025 holiday-season AI-referred-traffic figure, the OpenAI–Promptfoo acquisition of March 2026) reflect platform and policy state at the time of synthesis. Where claims are platform- or policy-state-dependent, we date them and flag the verification path. **The architectural shape — the Sentient Triangle, the four postures, the personalization-vs-adaptation distinction, the deferential-design contract, the variant-logging-as-infrastructure stance — is more durable than any tool name attached to it.** Bet on the architecture, not the platform.

---

## Why this file exists

Three forcing functions converge in 2026 to push adaptive interfaces from research and demos into client conversations:

**Conversational, generative, and agentic surfaces have moved from experimental to first-class** in flagship products (ChatGPT, Claude, Gemini, Copilot, Cursor) and increasingly into enterprise platforms (Atlassian Rovo, Salesforce Agentforce, ServiceNow Now Assist, SAP Joule, Microsoft Copilot). 25-ai-aware-patterns-and-conversational-ui covers the pattern surface itself; 26- and 27- cover the broader category that pattern set sits inside.

**Commerce is shifting upstream.** Adobe's analysis of the 2025 holiday season reported retail traffic from generative-AI sources (ChatGPT, Claude, Perplexity, Gemini referrals) up roughly 693% year over year, with AI-referred shoppers converting about 31% higher than traffic from traditional channels (Adobe Analytics, January 2026; corroborated in Braze's 2026 Customer Engagement Review). The volume is small today; the trajectory is the point. Within 18 months, "is our product legible to the agent recommending it?" becomes a real question for every commerce client we have.

**Regulation has crystallised.** EU AI Act Article 5(1)(a)–(b) — the manipulation prohibition — entered into force on 2 February 2025, with Recital 29 clarifying that effect, not intent, is the test (artificialintelligenceact.eu/article/5; eur-lex). Article 50's transparency obligations become fully applicable 2 August 2026. US state laws — Colorado SB24-205, California SB 942, California AB 2013, Utah's Artificial Intelligence Policy Act — accumulate operative dates through 2026. The "we'll figure out ethics later" posture has expired.

This is the field as we actually find it in May 2026. The reader is assumed to know what an LLM is, what a design system is, and what RAG and personalization platforms do. We are not introducing those concepts; we are mapping the terrain that sits on top of them.

---

## Six lineages, and why naming them is the first move

Six intellectual and engineering lineages converge on what is loosely called "adaptive UI" today. They use overlapping vocabulary, cite different authorities, optimize for different metrics, and frequently talk past each other. **Naming them clearly is the first move,** because every hard design decision downstream is really a decision about *which lineage's framing applies here*.

| Lineage | Primary driver | Locus of agency | Conceptual stance | Technical substrate |
|---|---|---|---|---|
| **Sentient Design** | Experience quality | The system, deferring to the user | AI as a responsive *design material* | Prompt rules, runtime design systems, constraint engines |
| **Generative UI** | Developer velocity | The system | Programmatic streaming of components | AI SDK, RSC / typed message parts, schemas |
| **Personalization (incumbent)** | Conversion optimization | The system, within a closed candidate set | Select a pre-built variant for a profile or context | Adobe Target, Optimizely, Sitecore, rule + bandit engines |
| **Malleable software** | User agency | The user as creator | Software as user-editable clay | Local-first data, dynamic documents |
| **Adaptive interfaces (academic HCI)** | Physical and cognitive accessibility | The system, against a measured ability model | Optimize layout to measured ability | Mathematical optimization, integer programming |
| **Agentic UX** | Goal execution | A third party — the agent — acting on the user's behalf | The agent operates the interface for you | LLMs, tools, browser/accessibility-tree parsers |

The axis these six disagree on is **who holds final agency.** Sentient Design and Generative UI place agency with the system, which interprets intent and compiles the layout. Malleable software insists agency must stay with the human, warning that automatic layout engines turn computing into un-inspectable black boxes. Agentic UX delegates agency to a third party — the agent — acting on the user's behalf. Personalization and academic adaptive interfaces sit in between: the system acts, but within a closed candidate set or against a measured ability model. A leader who treats "adaptive UI" as one thing will keep collapsing this axis.

### 1.1 Sentient Design (Josh Clark, Veronika Kindred, Big Medium)

Designer-facing, experience-led. Defined publicly in *Say Hello to Sentient Design* (Clark & Kindred, June 2024) as "the already-here future of intelligent interfaces: experiences that feel almost self-aware in their response to user needs," and given full book-length treatment in *Sentient Design* (Clark & Kindred, 2026, ISBN 9781959029182), which is the canonical reference for the framework. The book frames the practice around seven attributes: aware, radically adaptive, emergent, collaborative, individualized, deferential, and continuous (Clark & Kindred, 2026, Ch 1). Generation is one of five "machine-learning superpowers" alongside recommendation, prediction, classification, and clustering (Ch 2) — Sentient Design is therefore broader than generative UI and broader than personalization, framed as "form, framework, and philosophy" above the level of any single technique.

Vocabulary worth knowing, taken from the book and the wider Big Medium catalogue: *radically adaptive*, *aware* and *deferential*, AI as *design material* in its *awkward adolescence*, *call-and-response UI* ("the LLM talks to the interface, not the user," Clark & Kindred, 2026, Ch 6), *frozen formats* and *thawing* them, the designer as *creative director* setting rules and pattern libraries for AI to compose against, *bespoke UI* and the *intelligent canvas*, *productive humility*, *spaghetti scenarios* (Clark & Kindred, 2026, Ch 11). Where the lineage has sharpened over time is the design-systems thesis: by *Wiring Interface to Intent* (Clark, October 2025) and Ch 9 of the book, design systems are explicitly the substrate adaptive UI runs on — the LLM "can only assemble what designers have already built and documented."

A note on attribution: the phrase "molten UX" is sometimes attributed to Clark in secondary sources. We could not verify it in the book's index, in the catalogue of Big Medium essays, or in any of the public talks reviewed for this synthesis. Clark's vocabulary owns *thawing frozen formats* and *radically adaptive*; if you have seen *molten UX* cited as his, treat the attribution with caution. (This is one of the cleanest negative findings from the dual-agent research run.)

### 1.2 Generative UI (Vercel et al.)

Engineering-facing, narrower. The term was popularized by Vercel in *AI SDK 3.0 with Generative UI Support* (March 2024) — a user asks "What is the weather in SF?", the model invokes a `get_city_weather` tool, a spinner streams in, then a `<Weather/>` component renders inline in the conversation.

The shipped reality is narrower than the term suggests, and the architecture's status is genuinely mixed. The original RSC-based generative-UI primitives are flagged "experimental" in Vercel's own docs, with a published RSC-to-UI migration guide pointing developers to AI SDK UI's typed `message.parts` model for production (ai-sdk.dev/docs/ai-sdk-rsc/migrating-to-ui). RSC development is paused per Vercel's own GitHub discussion. *And yet* the code persists in a maintained `@ai-sdk/rsc` package extracted in v5 (July 2025), and `streamUI` still exists. The honest framing is *experimental, officially deprioritized for production, with a published migration path — maintained, not removed.* The term is louder in the discourse than in shipped engineering, but it is not dead. NN/g's broader academic definition (Moran & Gibbons, March 2024) — "a user interface that is dynamically generated in real time by artificial intelligence" — describes an aspiration; the shipped pattern is closer to "constrained component selection within a chat surface." (For the engineering depth on what actually ships, see 27-adaptive-interfaces-implementation.)

### 1.3 Personalization (Adobe, Sitecore, Optimizely, Salesforce, Dynamic Yield)

Older, originally rule-based, the incumbent. Every major platform now offers two flavors: rule-based (*if segment X then offer Y* — the marketer is the decision-maker, the system executes) and ML-driven (*here is the candidate set and the goal metric, you pick* — Adobe's Auto-Target / Automated Personalization runs Random Forest models retrained every 24 hours, with multi-armed bandits and Thompson Sampling fallback; Optimizely uses MABs and is roadmapping contextual bandits; Sitecore exposes "analytical models" inside a decision canvas).

The unit of personalization is remarkably narrow across all of them: an Offer slotted into an Experience inside an Activity (AEM's vocabulary, but the shape generalizes). What varies per user is hero/banner content, teaser images, recommendation strips, occasional layout swaps — almost nothing varies *structurally*. Nav doesn't restructure. IA doesn't change. Forms don't compose themselves. Fifteen years of production practice has refined fine-grained content swapping inside a fixed page skeleton — which is precisely what makes today's "generative UI" pitch feel both incremental and threatening to incumbents.

Where LLMs are entering the incumbent stack is the *authoring* layer, not the decisioning layer. Sitecore's Code Assistant turns natural-language prompts into JavaScript decision logic. Adobe Target ships an in-product AI Assistant and an MCP server exposing Target operations to Claude / Cursor / ChatGPT. Dynamic Yield's "Shopping Muse" is a conversational front-end on top of legacy decisioning. The model that *picks the variant* is still a Random Forest or a bandit. **This is the opposite of what "AI-driven personalization" press usually implies,** and clients who already own AEM, Sitecore, or Optimizely seats are in a much stronger starting position than they realize. (See 10-cms-and-platform-integration on the broader CMS context.)

### 1.4 Malleable software (Ink & Switch, Litt, Appleton, Matuschak)

Research/philosophical, and structurally in tension with the dominant generative-UI narrative. Generative UI is *system-generated*: the AI produces an interface in real time based on inferred user context. Malleable software argues software should be *user-authored*, with AI as a collaborator inside a medium the user controls.

Litt's hybrid model (March 2023) is direct manipulation in the inner loop, LLM as "local developer" in the outer loop, and "the user's reliance on the AI gently *decreases* over time as they become more comfortable in the medium." The Ink & Switch position essay *Malleable Software: Restoring User Agency in a World of Locked-Down Apps* (Litt, Horowitz, van Hardenberg, Matthews; June 2025) extends this to four properties — software ecosystem, anyone, adapting tools, minimal friction — and warns that "AI code generation alone does not address all the barriers to malleability." Without composable architectures and shared data, AI coding inside today's app stores is "a talented sous chef in a food court." Appleton's *Squish Meets Structure* (2023) argues language models are "organic, opaque, unpredictable" and we keep wrapping them in conventions designed for predictability. By 2025, Litt had publicly shifted toward HUD-style interfaces over chatty copilots (*Enough AI copilots! We need AI HUDs*, July 2025).

The distinction matters: generative UI optimizes for *the user not having to think about the interface;* malleable software optimizes for *the user being able to reshape it.* One is convenience, the other is agency. They can coexist, but they imply different power structures, and senior leaders should not let them collapse into each other.

### 1.5 Adaptive interfaces — academic HCI (Gajos, Wobbrock, Findlater)

The academic root, with twenty years of empirical work, almost entirely uncited in current practitioner discourse. Gajos's SUPPLE work (2004 onward) framed automatic UI generation as constrained optimization: given an abstract specification and a model of the user's device and abilities, search the space of renderings to minimize estimated effort. Concretely, SUPPLE treats interface construction as an integer-programming problem — minimizing a cost function summed over interactive elements, weighted by each element's expected frequency of use and the motor or visual difficulty it imposes given the user's measured ability profile.

By 2007–2008, Gajos, Wobbrock, and Weld had shown that SUPPLE-generated interfaces matched to a user's measured motor abilities significantly outperformed default interfaces for users with motor impairments — *and* those users *preferred* the adapted UI (CHI 2008). Preference and performance moved together, which is rare in adaptive-UI research. The canonical Wobbrock et al. *Ability-Based Design* paper (TACCESS 2011, CACM 2018) articulates the philosophy: design for ability rather than disability; let systems adapt to the person rather than asking the person to adapt to the system. iOS VoiceOver gestures are a direct descendant. Findlater & McGrenere's CHI 2004 study is the cautionary anchor: *adaptable* (user-controlled) menus outperformed *adaptive* (system-controlled) ones on satisfaction, and many participants preferred the static baseline outright for spatial-memory reasons. Findlater & Gajos's 2009 *AI Magazine* survey is the field's accumulated humility: benefits are real but conditional on prediction accuracy, stability, and the cost-of-error model.

**This is the single strongest empirical evidence base in the field, and it is almost never cited by current practitioners.** Senior leaders making the inclusivity argument for adaptive UI should cite Wobbrock and Gajos, not Vercel. (See 14-accessibility on ability-based design as architecture, and §6.1 below for the verification gap that comes with this.)

### 1.6 Agentic UX (Nielsen Norman Group, Replit Agent, computer-use models)

The agent-does-the-work framing. NN/g's Sponheim (April 2026) defines an AI agent as "a system that pursues a goal by iteratively taking actions, evaluating progress, and deciding its own next steps." Gibbons & Moran (April 2026) argue agents *are becoming users* of digital interfaces — "'user' is no longer synonymous with 'human'" — and that some businesses (ad-supported, regulated, competitive-data holders) have legitimate reasons to *resist* agent access: "not all friction in an interface is a design failure." Liu & Rosala's Qwen study (NN/g, May 2026, n=6) is the only original empirical agentic-UX study from NN/g this synthesis found: 5 of 6 participants defaulted to traditional delivery apps over an integrated agent; data-leak alarm surfaced at the authorization moment; abandoned tasks when the agent hid decision-relevant data. The empirical base is thinner than the volume of articles suggests.

### 1.7 What we'll call this in our practice

We commit to **Sentient Design** as the strategic vocabulary for our practice, attributed to Clark & Kindred. There are three reasons: it is the only lineage that gives designers language for the *full* surface area (recommendation + prediction + classification + clustering + generation, not just generation); its insistence on *deferential* design is the right ethical posture; and the Sentient Triangle and the four postures are the most coherent organising scaffold currently published in the field. We adopt the book's vocabulary — *radically adaptive*, *aware* and *deferential*, *call-and-response UI*, *productive humility*, *bespoke UI*, *intelligent canvas*, *spaghetti scenarios* — with attribution, and we name the book in client-facing materials rather than launder its terms.

Three correctives stay close to hand. **Personalization-incumbent practice** is the engineering baseline, because the bandit-driven, slot-based, A/B-tested infrastructure already running at Adobe, Optimizely, and Sitecore scale is what most organizations should compose with, not replace. **Ability-based design** (Gajos, Wobbrock) is the empirical conscience, because it is the body of evidence most likely to keep teams honest about whether their adaptive UI actually helps anyone. **Saarinen's *workbench* counter-position** (Linear, 2025–2026) is the corrective for the chat-as-default reflex — for power-user productivity tools and professional contexts, a stable conventional UI with AI layered on top remains the right shape, and *Output Isn't Design* (April 2026) is a direct rebuttal we should be ready for.

Generative UI gives engineering primitives but smaller scope than its name (see 27-adaptive-interfaces-implementation). Malleable software is the right long-term direction for *some* product categories — notes, end-user computation, creative tools — but is not yet a mass-market pattern. Agentic UX is moving fastest but has the thinnest empirical base.

---

## The Sentient Triangle as our organising scaffold

The Sentient Triangle (Clark & Kindred, 2026, Ch 3) is the strongest currently published framework for organising adaptive-UI experiences, and we adopt it as our scaffold. The triangle, originally informed by Matt Webb's mapping of the gen-AI product landscape (interconnected.org/home/2024/07/19/ai-landscape, July 2024), plots experiences against three pillar attributes:

- **Grounded.** The system has the training and information it needs to deliver reliably accurate results.
- **Interoperable.** The system can work across systems, formats, and tools.
- **Radically adaptive.** The system morphs in real time to meet user intent and context.

Of these, *radically adaptive* is the genuinely new pillar for interaction design — interfaces that can practically design themselves. *Grounded* and *interoperable* are not new in themselves, but recent leaps in capability have changed their nature: enough grounding in a specific domain produces relevant, even creative output; enough interoperability with other services and formats produces autonomous agents that work independently on the user's behalf.

At a high altitude, the triangle reveals **four postures** that organise all Sentient Design experiences (Clark & Kindred, 2026, Ch 3):

| Posture | Relationship | Triangle home | Where it shows up in the wild |
|---|---|---|---|
| **Tools** | People *use* tools | Grounded corner | DeepL, Photomath, Shazam, Midjourney as a coin-slot interface |
| **Chat** | People *talk to* chat | Radically adaptive corner | ChatGPT, Claude, Gemini, all the bespoke UI patterns |
| **Agents** | People *delegate to* agents | Interoperable corner | Linear Agent, Notion Custom Agents, Replit Agent, taskers & alchemists |
| **Copilots** | People *are backed by* copilots | Centre, equally all three | GitHub Copilot, Apple Intelligence Writing Tools, Granola, Linear Triage Intelligence |

Posture is not just functionality — it determines the system's *manner* and *relationship* with the user. The four are not mutually exclusive; the unblended distillations are often stunted (chat at the radically-adaptive tip is glib but unreliable; tools at the grounded tip are precise but isolated). **The interesting things happen between the corners** — the hybrid zones where the triangle's three pillars combine to produce *collaborative* (radically adaptive + interoperable), *autonomous* (interoperable + grounded), and *iterative* (radically adaptive + grounded) experiences.

This is more compass than map. It will not be strictly correct in every case — the triangle's claim that radically adaptive experiences trade off against grounding and interoperability has clear exceptions. But it is directionally accurate, and it is the most useful published prompt we have for asking *"what happens when I make this experience more adaptable, more grounded, more interoperable?"*

(See 27-adaptive-interfaces-implementation §1 for the parallel engineering scaffold — the five-rung decision-tree-to-generative spectrum — that maps the same territory from a different angle.)

---

## The pattern catalogue at four tiers

Inside the four postures, Clark & Kindred (2026) name *forty-six* patterns across **four tiers** — and the four-tier *layering* is itself a contribution worth surfacing, because most published pattern libraries flatten everything into a single list and lose the architectural distinction. The tiers and counts (Clark & Kindred, 2026, Appendix: Pattern Library):

- **Experience patterns** (14) — the high-level archetypes that inhabit the four postures: dedicated tools, workflow tools, inline tools, sculptors; characters, assistants, NPCs, bespoke UIs (with three sub-flavours), intelligent canvases; taskers, alchemists, stewards, conductors; copilots.
- **Functional patterns** (8) — cross-cutting behaviours that show up across multiple experience patterns: Action Guard, Feedback Loop, Inpainting, Mission Staging, Personalization Daemon, Pinocchio, Spaghetti Scenarios, Version Vault.
- **Interaction patterns** (7) — the ways users invoke and shape AI behaviour: Canvas Command, Circle Gesture, Companion Dialogue, Inline Correction, Progressive Scaffolding, Prompt Refinement, Second Thought.
- **UI patterns** (17) — the rendered components: Activity Stream, Agent Notebook, Citation, Comparative Selection, Consensus Meter, Contextual Menu, Kanban Board, List-Detail, Mad Libs, Nudge Prompt, Parameter, Simple Rating, Structured Flags, Table List, Thermometer, Trait Tags, Workflow Canvas.

We adopt this whole catalogue as our practice vocabulary because no other published framework names patterns at this level of specificity *and* layers them at four tiers. The layering matters in scoping — when a client asks for "an AI feature" we now have a way to ask which experience pattern, what functional behaviours it needs, what interaction patterns invoke it, and which UI patterns render it. The Citation UI pattern shows up inside both Bespoke UI and Assistant experiences; the Action Guard functional pattern shows up across Taskers, Stewards, and Conductors; the Companion Dialogue interaction pattern is how a user drives a Composition Canvas as much as how they drive an Assistant. **Patterns at one tier compose with patterns at other tiers, and that's the catalogue's real architectural claim.**

The fourteen experience patterns are the entry point. Where we extend or qualify, we say so.

**Tools (grounded corner).**

- **Dedicated tools.** Stand-alone single-purpose utilities — DeepL, Photomath, Shazam, Midjourney's image generator. The feature *is* the product; coin-slot interaction; near-zero ambient adaptivity.
- **Workflow tools.** Dedicated tools wired into a multi-step process — Descript's transcription, edit-by-text, retake-removal, eye-contact, all piped together for media editing.
- **Inline tools.** Contextual machine intelligence embedded directly inside an existing interface — Google Forms suggesting answer types as you write the question; Apple Intelligence Writing Tools; Figma's Adjust Tone grid.
- **Sculptors.** Iterative refiners of generated content — image generators with edit-and-resample loops, Adobe Firefly Boards, the conversational flavour of Midjourney.

**Chat (radically adaptive corner).**

- **Characters.** Personas with intentional design — Replika, Character.ai, Duolingo's role-play partners. Character is not just dialogue tone; it is voice, visual treatment, and the *boundaries* of what the character will and won't do.
- **Assistants.** Goal-oriented helpers — ChatGPT, Claude, Gemini, Anthropic's general-purpose assistants. The book's *minimum viable personality* framing (Ch 5) is the design discipline: assistants need consistent, intentional character, but *not* the full surface area of a fictional Character.
- **Non-Player Characters (NPCs).** Specialist personas summoned into a workflow — Miro's named board-side collaborators (a brainstormer, a critic, a synthesiser). The book treats this as a distinct pattern from generic Assistants because the character is *scoped to a context*.
- **Bespoke layering.** Adaptive panels grafted onto an otherwise stable interface — Salesforce's generative canvas dashboards inside the Lightning shell; Hills Pet's adaptive product comparison block inside an otherwise fixed PDP. The conservative end of bespoke UI; brand-friendly because the surface stays mostly fixed.
- **Call-and-response UI.** A single, request-bound interface fragment generated to answer the moment — *Ask Amplitude*'s "chat with charts" returning bespoke data visualisations per question; Cisco's AI Canvas. The LLM speaks UI to the interface engine, not text to the user (Clark & Kindred, 2026, Ch 6 — the *Wiring Interface to Intent* pattern, with a worked system-prompt example).
- **Fully bespoke UI** in three flavours: **composition canvas** (Miro, Adobe Firefly Boards — gather, synthesise, compose); **document canvas** (ChatGPT Canvas, Anthropic Artifacts, Gemini Canvas — the conversation thread plus the artefact); **interface canvas** (iPad Math Notes, tldraw Make Real, Microsoft Power Apps, Anthropic's *Imagine with Claude* research demo — the user draws or describes the interface they want and the system manifests it).

**Agents (interoperable corner) — Clark & Kindred's typology in Ch 8.** The book's framing is that **taskers are the baseline; the others are specialisations** — alchemists are taskers tuned for transformation, stewards are taskers tuned for caretaking, conductors are taskers tuned for orchestration. The three rules-of-thumb that govern all of them: agents *use tools* (the agent never gathers raw data itself; it chooses tools that do); agents *need permission* (delegation is an onboarding ritual, not a generic consent click — see the Action Guard functional pattern in §4.5); agents *keep after it* (persistence is their strength and their drift surface).

- **Taskers.** Single-purpose execution agents — invoice classifiers, sentiment processors, ticket buyers, comment moderators. The simplest end of the spectrum. Often act *as* tools to the rest of the system. Practical rule of thumb from the book: 3–6 tools is the sweet spot for a focused tasker; agents start to wobble past a dozen tools.
- **Alchemists.** Content-transformation agents — a meeting transcript becoming a structured PRD, an audio file becoming captions becoming a translated post becoming a thumbnail. The book's framing is that alchemists liberate trapped content into new channels.
- **Stewards.** Long-running, accountable agents that take ownership of a recurring responsibility — a release-notes steward that watches the changelog and drafts publishable summaries; a triage steward that watches incoming issues and proposes labels and assignees (Linear Triage Intelligence is the canonical example). Stewards sit closest to the *system-level user* framing — a teammate with independent responsibilities rather than a tool a user invokes.
- **Conductors.** Agents that orchestrate teams of other agents — a project conductor that delegates research to one agent, drafting to another, fact-checking to a third. The book treats this as the most ambitious and least mature point on the spectrum.

The axis these four are arranged along — and the one we should bring into agent-engagement scoping — is **workflow vs. notebook** (Clark & Kindred, 2026, Ch 8). A *workflow* is a deterministic if-then process where the user pre-specifies every branch; the agent's autonomy is low and the surface that authors it is the Workflow Canvas UI pattern. A *notebook* is a probabilistic procedure described in natural language where the agent applies its own reasoning to figure out what to do; the surface is the Agent Notebook UI pattern, formalised through the emerging *agent skills* standard. Workflows give you predictability at the cost of brittleness; notebooks give you adaptability at the cost of less predictable outcomes. **The choice between them is itself a design decision** and it cascades into how the engagement gets QA-ed, how the human-in-the-loop ritual is designed, and how the agent's drift gets bounded. (See 27-adaptive-interfaces-implementation §6.3 on the eval consequences.)

A practitioner-aware note from the book worth carrying: when an interface agent ends up using human-facing channels (filling out web forms, making phone calls, navigating someone else's UI) to get its work done, **that is the *path of most resistance*, not the future** — it is a stopgap for environments where no agent-native channel exists. The agentic-commerce traffic shift in §5 is the same forcing function in reverse: the agent-native data layer (structured product data, machine-legible inventory, accessibility-tree quality) is the surface we should be building toward, not retrofitting agents to navigate human UIs.

**Copilots (centre).**

- **Situational copilots.** Surface in a specific context, then disappear — autocomplete suggestions in an email composer, a "summarise this thread" affordance that appears when a thread crosses a length threshold.
- **Session copilots.** Active across a working session — GitHub Copilot during a coding session; Apple Intelligence Smart Replies during a messaging session.
- **Continuous copilots.** Ambient, always-on — Granola listening to every meeting; Apple's Notification Summary; Dia's Morning Brief. The cost-of-being-wrong is highest here, which is why deferential design (§4 below) bites hardest in this row.

**Why this catalogue matters.** When a client says "we want AI features," the diagnostic question is not "what model?" but *"which posture and which pattern?"* — and the answer cascades into latency budgets, eval scope, governance load, brand risk, and team composition. We carry this taxonomy into Discovery and refuse to start scoping without it.

---

## Personalization vs. adaptation — the load-bearing distinction

Marketing copy and platform pitches conflate these two. **Pulling them apart explicitly is the highest-leverage diagnostic move in any client conversation.** It changes the architecture, the metric set, the privacy regime, and the governance model.

| Vector | Personalization | Adaptation |
|---|---|---|
| Unit of analysis | Demographic / behavioural cohort | Real-time situational intent and capability |
| Temporal model | Latency-tolerant; computed asynchronously from profiles | Real-time; compiled in the interaction loop |
| Architecture | Deterministic rule engines, bandits, static variants | Generation guided by dynamic constraint envelopes |
| What changes | Copy, media, promo blocks within a fixed grid | Structural and layout-level transformation |
| Primary failure | Stale cohort data, misprofiling, cookie/privacy loss | Hallucinated controls, disorientation, broken muscle memory |
| Failure timing | *Between* sessions | *Within* a session |

**Personalization** is segment-driven: *user is in cohort X, show variant Y.* The cohort may be authored by a marketer or learned by a model, but the unit of variation is *which pre-built variant gets served*. The candidate set is closed; the design system is intact. **Adaptation** is context-driven: *user is doing Z right now.* The candidate is constructed, or selected from a much larger latent space, for this moment for this user. Granola's meeting templates change because the calendar event title says "user research" rather than "1-on-1." Linear's Triage Intelligence pulls a different set of suggestions because the workspace's "Additional Guidance" prompt steers it that way.

The two failure modes differ. Personalization fails *between* sessions — a one-time gift purchase poisons your recommendations for months — and mature recommenders all expose an explicit *escape hatch* (TikTok's "Not Interested," YouTube's history pause, NN/g's "View as…" pattern; Schade, NN/g, 2016). Adaptation fails *within* a session: the interface guesses wrong about what you're doing right now and surfaces the wrong tool, the wrong layout, the wrong content. The repair has to happen in seconds, not weeks.

The cleanest tell that the two are different categories: in the academic literature, preference and performance often move *together* for ability-based personalization (Gajos, Wobbrock — where the cohort is "users with this measurable motor accuracy") but often move *apart* for system-driven within-session adaptation (Findlater & McGrenere — users preferred the static menu). Personalization rewards stability across time; adaptation rewards responsiveness within time. **Confusing them is the most common diagnostic error in the discourse.**

The book's complementary framing is *personalized vs. individualized* (Clark & Kindred, 2026, Ch 1): *personalized* uses stale profile data ("your preferred PDF format"); *individualized* uses immediate context ("you're commuting to a meeting in 30 minutes — here's a 5-minute audio summary"). The People Inc D/Cipher case study in the same chapter is worth carrying into client conversations: *audience* behaviour at the current moment in the current context can outperform individual profile-tracking for most use cases, with no surveillance and no cookie dependency. *"You don't have to know a person's whole history to build a strong theory of the user based on how everyone behaves in the specific context."*

For commerce and content clients, the practical synthesis is: server-side personalization decides which content library is injected; client-side adaptation restructures the live layout for touch, glare, motion, accessibility, or task. Both can coexist; both should be named explicitly when they do. (See 10-cms-and-platform-integration on the CMS-side seam.)

---

## What problems this actually solves

The hard, evidence-based section. We break out four use cases where the case for adaptive UI is genuinely well-evidenced, and three where the case is weaker than the marketing implies.

### 4.1 Accessibility — the strongest empirical case

The Gajos / Wobbrock work is the load-bearing evidence base in the entire field. Motor-impaired participants completed tasks significantly faster, made fewer errors, and *preferred* the adapted UI (Gajos, Wobbrock & Weld, CHI 2008). Ability-based design is now embedded in iOS VoiceOver gestures and a generation of accessibility infrastructure (Wobbrock et al., CACM 2018). The signal is robust and specific: when *abilities are measurable* (motor accuracy, vision, working memory) and the system *actually models them* before adapting, adaptive UI delivers — for the population that needs it most.

**The corollary cuts the other way.** Most "AI personalization" today is correlational; it learns what users tend to choose, not what they're *able* to do well. The marketing case for "AI improves accessibility" is much weaker than the academic case for *ability-based design improves accessibility*. (See 14-accessibility on the architecture, 16-mobile-accessibility-implementation on the framework-level treatment, and 27-adaptive-interfaces-implementation §6.2 on the verification gap that makes this the *hardest* property to guarantee once the surface is variable.)

### 4.2 Discovery and cognitive load for occasional or novice users

Recommendation-system practice has fifteen years of evidence that personalized discovery surfaces measurably improve engagement. Netflix's 2016 *Power of a Picture* disclosure — 82% of browsing focus is on artwork during a ~90-second decision window, with artwork variants A/B-tested per title — remains the canonical proof that the *same content* shown *differently per user* is a decade-old production practice, not a 2024 generative-UI invention. Spotify's Daily Mix (2018) clusters listener history into daily-refreshed playlists. Moran's *The Most Exciting Development in GenUI: Buttons and Checkboxes* (NN/g, March 2026) is the clearest 2026 finding in the same vein: chat-embedded checkboxes and buttons (Google AI Mode's hotel chips, Claude's `AskUserQuestion` widget) measurably reduce friction over text-only follow-ups.

The strongest discovery wins are for users who *don't yet know* what they want — which makes cold start a first-class design problem and means any adaptive UI without an explicit "I don't know you yet" mode degrades for every new user, every cleared cookie, every shared device.

### 4.3 Onboarding and time-to-value

Genuine but conditional gains. Granola's adapt-to-meeting-title pattern is the cleanest example — users get useful structured notes from the first meeting because the system inferred the meeting type from the calendar event title. Linear's Triage Intelligence reduces the manual triage tax that would otherwise be a multi-week onboarding tax for a new PM joining a workspace. Salesforce's generative canvas (Clark & Kindred, 2026, Ch 1) reorders dashboard tiles around the upcoming sales meeting on the user's calendar. **The pattern is to *use the user's existing context* (calendar, workspace, tabs) rather than ask new users to fill profile fields** — a real shift from the personalization-incumbent paradigm, and one that lands well with privacy-conscious clients.

Adaptive UIs can also progressively disclose complexity: a clean onboarding layout that exposes dense panels and shortcuts as the user demonstrates mastery. Ada Health's symptom-questionnaire flow (Clark & Kindred, 2026, Ch 1) is a healthcare-specific instance — the questionnaire adapts as the patient describes what they're experiencing, slimming a one-size-fits-all form into a focused conversation.

### 4.4 E-commerce — the case that breaks the binary

Both "strong fit" and "ambiguous fit" verdicts on e-commerce are wrong, because the evidence is strong on *both* sides simultaneously. The ROI case is well-evidenced: McKinsey's *Next in Personalization* (2021) puts typical revenue uplift from well-executed personalization at 10–15%, up to ~25% best-case; real-time personalization outperforms batch by roughly 20% on conversion across vendor case studies; documented retailer migrations from rules to ML show CTR lifts averaging ~41% across dozens of cases; Wayfair has reported conversion improvements around 40% with measurable return-rate reductions.

The risk case is *equally* well-evidenced. A growing cluster of 2024–2025 PLS-SEM studies (Indonesian, Turkish, and fashion-e-commerce samples) document the Personalization-Privacy Paradox empirically — perceived overreach, data-misuse fear, and algorithmic-manipulation perception drive measurable backlash, with privacy-violation perception the central psychological pathway from surveillance to reduced purchase intention, and brand trust acting as the moderator.

**The variable that decides the outcome is not the industry — it is execution quality:** brand-trust capital, transparency-by-default architecture, governance maturity, and willingness to invest in privacy-preserving infrastructure (federated learning, differential privacy, on-device personalization, audience-not-individual modelling à la People Inc). The honest verdict for a client conversation: **e-commerce is simultaneously the highest-evidenced use case for measured ROI and the highest-evidenced use case for failure modes.** Whether to recommend it turns on trust capital and privacy infrastructure, not on the sector label.

### 4.5 Where it underperforms or backfires

- **Power users.** Findlater & McGrenere 2004 — many prefer static menus. Saarinen's blunt rejection — *"a chat interface is a very weak and generic form"* — is a power-user voice arguing the workbench beats the conversation for anyone who knows the domain (*Design for the AI Age*, Linear, April 2025). Saarinen's *Output Isn't Design* (April 2026) is the corollary: "the risk is mistaking generated form for solved problems."
- **Regulated UIs.** Anywhere disclosure, audit trails, or anti-discrimination obligations apply — lending decisions, employment screening, insurance underwriting, healthcare diagnosis, government services. Adaptive UI that varies the *path* a user takes through a regulated decision is a compliance-perimeter problem, not a UX one. (See §5 below.)
- **Brand-led marketing surfaces.** When the surface itself is the brand artefact, varying it per user erodes the consistency the brand is paying for.
- **Professional tools where consistency is a feature.** Power-user productivity tools, technical authoring environments, code editors — Linear's "workbench" framing is the right pattern.
- **Anything where shared reference matters.** Collaborative tools, teaching tools, anywhere users discuss or share the interface.

---

## The agentic-commerce traffic shift

One development belongs here that neither of the original research passes surfaced, and it reframes what "adaptive UI for e-commerce" even means. Adobe Analytics's analysis of the 2025 holiday season found traffic arriving at US retail sites *from* generative-AI sources — users following a recommendation from ChatGPT, Claude, Perplexity, Gemini — up roughly **693% year over year**, with those AI-referred shoppers converting about **31% higher** than traffic from traditional channels (Adobe Analytics, January 2026; Braze 2026 Customer Engagement Review).

The number is still a small share of total traffic. The trajectory is the point. It marks the early shape of *agentic commerce*: the customer increasingly reaches the retailer through an AI agent's recommendation rather than through search or direct navigation. The agent is not only adapting the on-site experience — it is becoming the *referrer*, and sometimes the buyer. For any client with consumer-facing commerce, this changes the question. **"Adaptive UI for e-commerce" has quietly stopped meaning only "a smarter product page" and started also meaning "being legible, and persuasive, to the agent that decides whether your product is shown at all."**

The implementation work this implies — structured product data, machine-readable inventory, semantic content, agent-friendly APIs, accessibility-tree quality (because that's what agents parse) — is concrete and inside our reach today. It connects directly to NN/g's *AI Agents as Users* (Gibbons & Moran, April 2026): agents are becoming users, and increasingly customers' proxies. (See 27-adaptive-interfaces-implementation §3.4 for the implementation directives, and 25-ai-aware-patterns-and-conversational-ui on the chat-side surface this often arrives through.)

---

## Trust, mental model, and the deferential design contract

Adaptive UI lives or dies on whether users trust it. Three forces shape that trust, and the design discipline for each is reasonably well-understood.

### 6.1 The trust-and-creepiness tension

The historical anchor is not Clippy, it is *Lumiere*. Eric Horvitz's UAI 1998 paper on Bayesian user modelling was more cautious than Clippy's launch behaviour implied. Clippy's failure was a *productization* decision — an always-visible animated agent — imposed on a probabilistic system that was modest about itself. Horvitz had already articulated the rule that would have prevented it: *Principles of Mixed-Initiative User Interfaces* (CHI 1999) — an agent should act only when expected utility of acting exceeds expected utility of inaction, and should always preserve the user's ability to reject the action cheaply.

Luke Swartz's 2003 Stanford retrospective names the breakdown a *consistency* failure: an agent's name, appearance, voice, and behaviour must align with each other and with users' expectations. Both diagnoses are still operative and they are compatible: Clippy breached social expectation (Reeves & Nass's *Media Equation* mechanism) *and* was inconsistent between its friendly face and its modest capability. Clark's *Sparkles Are Fizzling* (Big Medium, September 2024) makes the same argument in 2026 vocabulary — the purple-gradient AI cliché now overpromises exactly as the animated paperclip did.

### 6.2 The mental-model cost

Findlater & McGrenere 2004 remains the reference experiment: adaptive (system-controlled) menus underperformed adaptable (user-controlled) menus on satisfaction, and a meaningful subset of users preferred the static baseline for spatial stability. Findlater et al.'s *Ephemeral Adaptation* (CHI 2009) showed gradual onset of adapted items improves performance without harming spatial memory. **The implication is uncomfortable: muscle memory is a feature, not a bug.** Christopher Butler's *Consistency Is Primitive* (2026) takes the contrary view — consistency is "civilizational infancy" dissolved by AI infrastructure — and NN/g's Moran is the direct counter: most users *cannot articulate* what interface they need, so genUI carries a *higher* design burden than vibe coding, not a lower one (*GenUI vs. Vibe Coding*, NN/g, March 2026). This debate is live; we land closer to Moran than Butler, and we will not flatten the disagreement when it shows up in client conversations.

### 6.3 The deferential design contract

Three patterns recur across mature adaptive-UI implementations, and we adopt them as our default.

**Visible thinking surfaces.** Linear's Triage Intelligence shows a thinking panel with a timer and a full reasoning trace; Vercel's AI SDK 4.2 added typed `reasoning` parts to messages; ChatGPT and Claude both surface chains of thought when relevant. Generative UI is making *what the model is doing* itself a UI element. Spinners no longer suffice.

**Cheap dismissal.** Horvitz's 1999 principle of *efficient invocation and dismissal* is now the determinant of perceived intelligence. Arc's hover-Shift previews are cheap to summon and cheap to ignore; Clippy's animated paperclip was expensive on both sides. An affordance that is cheap to summon and cheap to ignore reads as intelligent; one that is hard to escape reads as adversarial.

**Side-by-side over in-line.** Anthropic Artifacts, ChatGPT Canvas, Gemini Canvas, v0's Design mode, Comet, Dia's Splits all converge on the same shape: chat on one side, generated/editable artefact on the other. The chat thread becomes the *log of intent*; the panel becomes the *artefact of work*. This is now the dominant shape for human-in-the-loop generation.

The book's *productive humility* pattern is the through-line we want to internalise (Clark & Kindred, 2026, Ch 11). The system should be clear about what it knows, what it doesn't, and when it's just working on a hunch. *"I don't know" is better than a wrong answer.* For uncertain results, share the uncertainty in the same surface as the result — "this might perhaps maybe could be an elephant?" — because the strongest available finding from the 2016 hallucination research the book cites is that **strong, clear language is most effective in engaging appropriate skepticism**. "I have absolutely no idea, but…" works better than "There's a 10% chance." The book offers a vocabulary scale for confidence we recommend our practice adopt as default copy guidance: *very likely / almost certainly / it's clear that* for high; *seems to be / possibly / it appears* for medium; *take this with a grain of salt / there's a tiny chance / I'm not at all sure but* for low.

The book also names a catalogue of *smoke signals* — anti-patterns we should avoid in client work:

- **Raw confidence scores.** Numbers ("72% match") offer the illusion of precision without understanding. Netflix retired its match-score labels for exactly this reason.
- **General disclaimers.** "AI can make mistakes" footers have no measurable effect on user behaviour (the book cites a 2023 study where users followed AI medical advice at the same rate with or without the disclaimer).
- **One-true-answer presentation.** Google's featured snippets and AI overviews — confidently stated answers to "do reptiles make good pets?" and "do reptiles make poor pets?" returning opposite advice — show what happens when adaptive systems present hedged probabilistic output as declarative fact.

For the cases where the evidence genuinely is ambiguous or contested, the book's **spaghetti scenarios** functional pattern is the right answer: present multiple plausible threads together rather than a single confident conclusion (*"are reptiles bad pets" automatically including results for "are reptiles good pets"*; YouTube's "people also watched" alongside "up next"; Metacritic's individual-critic scores alongside the aggregate). Three UI patterns make this concrete: the **thermometer** for visualising confidence levels (high/medium/low as a meter or icon), the **citation** pattern for connecting generated claims to source data (Perplexity's inline citations are the canonical example), and the **consensus meter** for visualising agreement across sources or models (Consensus.ai for science papers; the same pattern works for LLM ensemble methods, see 27-adaptive-interfaces-implementation §6.3). We adopt all three with attribution.

The agent counterpart of productive humility is the **Action Guard** functional pattern (Clark & Kindred, 2026, Ch 8) — a permission checkpoint at the *transitional seams* where control shifts between agent and user, before any action that commits the user (sending, spending, deleting), reads or writes sensitive data, or sits at a moment of genuine ambiguity. Alexa's reorder-paper-towels confirmation that names the exact product, total, and arrival date before asking "should I buy it?" is the canonical instance. **The two design rules that bite:** make the user the *final decision-maker, not a micromanager* — interrupt at the commit moment, not every step (Alexa shouldn't ask before adding the towels to the cart, only before purchasing); and watch for *dialog fatigue* — too many action guards too often produces uncritical Continue-button mashing, which is worse than no guard at all. GitHub Copilot's session/workspace/always permission scope is a defensible default for tool-permission rituals: explain *why* the confirmation is needed and let the user pick the duration. (See 27-adaptive-interfaces-implementation §6.3 on how this connects to red-teaming the second manipulation vector — the agent itself is hypersensitive to nudges in retrieved content, so an Action Guard at the *retrieval* seam matters as much as one at the *action* seam.)

---

## Ethics and the manipulation regime

The strongest non-vague critique of adaptive UI is structural and arrives in four layers. **The "we'll figure out ethics later" posture has expired.**

### 7.1 The EU AI Act's manipulation prohibition is live

EU AI Act Article 5(1)(a)–(b) entered into force on 2 February 2025 (artificialintelligenceact.eu/article/5; eur-lex). It prohibits AI systems that "deploy subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques" with the objective or effect of "materially distorting the behaviour of a person … by appreciably impairing their ability to make an informed decision," causing or reasonably likely to cause significant harm. Article 5(1)(b) extends this to exploitation of vulnerabilities tied to age, disability, or specific social or economic situation.

Recital 29 contains the load-bearing line for adaptive UI specifically: subliminal stimuli include cases where users "are aware of them, [but] can still be deceived or are not able to control or resist them" — and *intent is not required, effect is sufficient*. **Adaptive UI that materially distorts behaviour and causes significant harm is illegal in the EU regardless of whether the design team intended manipulation.** The first hard-law instrument that names adaptive AI manipulation as such has already taken effect.

Article 50 — the transparency obligations covering chatbot disclosure, synthetic content marking, and public-interest text disclosure — is fully applicable from 2 August 2026. (See 25-ai-aware-patterns-and-conversational-ui §7 for the chatbot-side breakdown; 27-adaptive-interfaces-implementation §4.3 for the open interpretive question of whether content-marking obligations attach to AI-generated *interfaces*, not just generated media.)

### 7.2 US state-level disclosure regimes

Three pressure points are on the books, all operative or compliance-deadline by early 2026:

- **Colorado SB24-205** (operative February 2026) mandates consumer disclosure for any AI system "intended to interact with consumers" and triggers impact assessments, human-review rights, and discrimination-risk reporting whenever AI is a substantial factor in a *consequential* decision (employment, lending, housing, education, healthcare, insurance, legal).
- **California SB 942** — the California AI Transparency Act (operative January 2026) — requires latent provenance disclosure embedded in generative content from large providers (>1M monthly users in California), plus a public AI-detection tool. Civil penalty: $5,000 per violation per day.
- **California AB 2013** (compliance January 2026, retroactive to systems released on or after January 2022) requires developers to publish a "high-level summary of the datasets" used in training.
- Adjacent: **Utah's Artificial Intelligence Policy Act** establishes baseline disclosure obligations.

For any client engagement, the citable artefacts are the regulator's published text, not the marketing summary. We track these dates and verification paths on every commerce, healthcare, and HR engagement.

### 7.3 The second manipulation vector — LLM hypersensitivity to nudges

This is the single most important empirical finding in this file, and it sits outside the dark-patterns lineage most designers have read. **LLM agents are *more* susceptible to choice-architecture manipulation than humans** (Cherep, Maes & Singh, *LLM Agents Are Hypersensitive to Nudges*, MIT/Dartmouth, arXiv 2505.11584, 2025). Tested against canonical choice-architecture nudges — defaults, decoys, framing — across GPT-3.5, GPT-4o, o3-Mini, Gemini 1.5 Flash and Pro, and Claude 3 Haiku and Sonnet, models showed *much higher susceptibility to the nudges than human baselines.* Liou et al.'s *OI-Bench* (option-injection benchmark, 2025) found similar substantial vulnerabilities and heterogeneous robustness across twelve LLMs. (See also Liu & He's earlier *Decoy Dilemma in Online Medical Information Evaluation*, arXiv 2411.15396, November 2024, which produced the same finding in a medical-misinformation setting.)

The consequence is concrete and changes how we scope agentic-commerce engagements (§5 above). As agents become the intermediaries that read pages, compare options, and act on the user's behalf, the manipulation target shifts from the human's psychology to the *agent's*. An adversary no longer has to nudge you; they nudge the agent shopping for you, by arranging the content or options it ingests. **The same RAG and retrieval layers that make an interface adaptive to a specific person are an attack surface against the agent acting on their behalf.** Decoy injection into retrieved context is not theoretical, and any adaptive UI that exposes its retrieval surface to attacker-controlled content needs to red-team that surface explicitly. (See 27-adaptive-interfaces-implementation §6.3 on red-teaming maturity.)

### 7.4 The epistemic critique

Maggie Appleton's *Expanding Dark Forest* talk (Causal Islands, April 2023; expanded through 2024) supplies the content-level critique: as adaptive interfaces train on model-generated data, "that tenuous link to the real world becomes completely divorced from it." Butler's *Consistency Is Primitive* supplies the social corollary: when each user inhabits a bespoke interface, shared reference points dissolve, and so does the ability to recognise manipulation collectively. **Manipulation becomes invisible because there is no peer experience to compare against.**

### 7.5 What designers can concretely do

Four moves, in order of leverage:

1. **Make the system prompt a design artefact.** Linear's "Additional Guidance" surface is the early production example — the prompt is exposed to workspace operators, version-controlled, and reviewable. The prompt is the rule set; rule sets need design review, content review, and accessibility audit.
2. **Default to deferential UI.** Visible thinking, cheap dismissal, side-by-side artefacts, productive humility, the smoke-signals avoidance list. Not sparkles that overpromise.
3. **Audit for choice-architecture exposure on both vectors.** Treat the retrieved-context layer as an attack surface against the model (the new vector); audit the optimization objective for emergent dark patterns against the user (the classical vector).
4. **Maintain an auditable variant log.** Article 5 enforces on *effect*. The only credible defence is the ability to demonstrate, post hoc, that the variants surfaced to a user did not materially distort their decisions. **Design systems that don't keep variant logs aren't compliant; they just haven't been audited yet.** No vendor or industry body has published a reference design for variant logging in 2026, which is both a genuine gap and a place we can lead. (See 07-governance-and-adoption on the governance framing this implies, and 27-adaptive-interfaces-implementation §6 on how the eval and telemetry infrastructure underneath this ought to be built.)

---

## Industries — strategic fit

Adaptive UI's viability is highly dependent on the vertical, but not in the way a simple binary fit table implies.

**Strong fit.** *Media and entertainment* (Netflix, Spotify, the long-running pre-LLM baseline; recommendation plus visible escape hatches plus contextual signals is the dominant shape). *Productivity SaaS* (Linear, Notion, Granola, Dia; the agent-over-a-stable-workbench pattern is mature enough to ship). *Education* (adaptive UI as scaffolding for the learner's authentic work; high variance in learning speed). *Healthcare on specific surfaces only* — patient education content, accessibility surfaces, and ability-based adaptation for clinicians with measurable workflow variation; anything touching diagnosis, treatment, or consequential decisions sits in the weak-fit list.

**Ambiguous fit.** *Search* (Google AI Mode's query fan-out adapts what queries to issue, not what UI to render). *Browsers* — Arc's quiet retraction of *Browse for Me* and *Ask on Page* and The Browser Company's pivot to Dia (which markets as *"a browser that works with you"* rather than *"an AI browser"*) is the empirical answer for now: aggressive adaptive UI in the browsing surface failed to find product-market fit; context-aware assistance with a conventional surface is the surviving pattern. Perplexity Comet's *CometJacking* prompt-injection disclosure (LayerX Security, August 2025) is the cautionary tail. *Mobile platform shells* — Apple Intelligence is the cautionary case. The personal-context Siri, onscreen-awareness, and cross-app intent features promised in 2024 were still labelled "in development" 18 months later, drove the *Landsheft v. Apple* class action (settled December 2025), and are now reportedly being rerouted through a multi-billion-dollar Apple-Google Gemini deal (Bloomberg, January 2026). The platform-shell surface is uniquely hard for adaptive UI: high cost-of-wrong, strongest possible muscle memory.

**Weak fit.** Regulated UIs (per §7.2 above). Brand-controlled marketing surfaces. Professional tools where consistency is a feature. Anything where shared reference matters — collaborative tools where users discuss the interface with each other; teaching tools where one user is showing another. Bespoke-per-user UI breaks the social fabric of these products.

**E-commerce — the case that breaks the binary.** Covered in §4.4 above. Whether to recommend it turns on trust capital and privacy infrastructure, not on the sector label. This is more useful guidance than either pure verdict.

---

## What our practice should commit to

We carry these positions into client conversations and proposals.

**1. Adopt the Sentient Triangle and the four-postures vocabulary as our default scaffolding.** Attributed to Clark & Kindred (2026). When clients say "we want AI features," we map their request onto a posture and one or more experience patterns before scoping. We refuse to start a Discovery without that mapping.

**2. Default to deferential UI and the productive-humility pattern.** Visible thinking, cheap dismissal, side-by-side artefacts, structured-output rendering over streaming-prose, the smoke-signals avoidance list. We treat *Sparkles Are Fizzling* as a design directive, not a critique.

**3. Treat the system prompt as a versioned design artefact.** Reviewed alongside the visual design, accessibility annotations, and content guidelines. (See 04-documentation on docs implications, 07-governance-and-adoption on the governance gate this creates.)

**4. Maintain auditable variant logs as default infrastructure on every adaptive engagement.** No vendor has published a reference implementation; we can lead here. The deliverable is what gets logged, who holds it, who can audit it, and the retention period — practical answers to questions Article 5 will eventually demand.

**5. Lead with ability-based design when making the inclusivity case.** Cite Wobbrock and Gajos, not Vercel. Scope accessibility verification as ongoing manual testing with assistive technology, not as a CI check. (See 14-accessibility on the four-layer architecture; 27-adaptive-interfaces-implementation §6.2 on the verification gap.)

**6. Pull personalization and adaptation apart in every Discovery.** The diagnostic table in §3 is the single highest-leverage move in client conversations. The escape-hatch requirement is non-negotiable for personalization; the within-session-repair budget is non-negotiable for adaptation.

**7. Treat the EU AI Act's effect-based enforcement as a real compliance perimeter.** Variant logging, retrieval-context red-teaming, and a documented choice-architecture review are not optional for EU-facing clients. The US state regimes (Colorado, California SB 942 + AB 2013, Utah) compound the obligation.

**8. Position our design-systems practice as the load-bearing capability for adaptive work.** Adaptive UI does not survive without a design system that can be composed against — primitive components, semantic intent metadata, machine-readable usage rules, structured layout templates with named slots. (See 03-component-library on the components-as-data thesis; 04-documentation on the docs side; 15-ai-in-ds on the operator-side architecture this builds on.) **The clients that arrive at our door asking for adaptive features will get the work we can actually deliver only if their DS is ready for it — and that readiness is a deliverable category in our scoping, not an aspirational add-on.**

---

## Open questions

1. **Is "personalization" recoverable as a term, or has it been so overloaded that it now actively obscures?** Forrester's Jessica Liu has been arguing since April 2025 that the word needs qualifiers (program / capability / tactic / moment) before it means anything. NN/g still uses it broadly. The Sentient Design lineage folds it in as one tactic. The personalization-incumbent vendors use it for both rule-based and ML-driven systems indiscriminately. We have used *personalization* narrowly and *adaptation* for context-driven within-session behaviour in this file. Whether the field consolidates around that distinction is unresolved.

2. **What does *consistency* mean operationally when surfaces vary?** Butler argues consistency is "civilizational infancy"; Moran argues users cannot articulate their interface and need conventions; Clark argues design systems are more important than ever. All three may be right at different time horizons. The practical guidance differs sharply by which side a leader takes, and we do not have a stable POV across that split.

3. **How much of the genuine adaptive-UI value is captured by accessibility specifically?** The Gajos evidence is the strongest in the field. If accessibility is doing most of the load-bearing work, much of the surrounding genUI marketing is overpromising on weaker evidence. We do not have a defensible answer for whether the broader adaptive-UI thesis has comparably strong evidence somewhere we missed.

4. **Who governs variant logging?** EU Article 5 enforces on effect. No vendor or industry-body proposal exists for what good variant logging looks like, who should hold the logs, who should be able to audit them, or how long they should be retained. This is a major open question and possibly its own deliverable; see 27-adaptive-interfaces-implementation §6.

5. **How does the second manipulation vector get defended?** If LLM agents are hypersensitive to nudges and option injection, and agents increasingly mediate commerce and decisions, what is the defensive discipline — and whose job is it, the model provider's or the deploying designer's? We currently scope both into our work; whether the model providers absorb the obligation over the next two years is unclear.

6. **Does agentic commerce make on-site adaptive UI more or less important?** If the agent is increasingly the referrer and the comparison-shopper, the retailer's own adaptive surface may matter less than its legibility to agents — or may matter more, as the place a hard-won agent-referred visit is converted. We do not have evidence either way at scale, and the trajectory is moving fast enough that this should be re-asked quarterly.

7. **Is Saarinen's "workbench" position generalizable, or specific to professional tools?** Linear is a productivity tool with power users. The same logic applied to consumer surfaces would either reverse (consumer users have less domain expertise) or hold (because the underlying claim about chat being "weak and generic" is medium-independent). Open.

8. **How quickly does the malleable-software lineage move from research to product?** Litt, Appleton, and Matuschak's position essays are unusually substantive for research output, but the production examples remain narrow. Whether this lineage produces a mass-market product in the next three years, finds vertical product-market fit only, or remains primarily research is unresolved.

---

*Provenance: This file is synthesised from a dual-agent research run (foundations 2026-05-20, implementation 2026-05-21; both prompts, raw outputs, and per-track syntheses preserved in `_research/_inbound/2026-05-20-adaptive-ui-foundations/`, `_research/_inbound/2026-05-21-adaptive-ui-implementation/`, and `_research/_synthesis/`) plus a primary-source read of Josh Clark and Veronika Kindred, *Sentient Design* (2026, Rosenfeld Media, ISBN 9781959029182) — `_source-text/sentient-design-2026/`. The book leads on patterns, vocabulary, and the Sentient Triangle scaffold, attributed throughout to Clark & Kindred. Empirical evidence (Gajos, Wobbrock, Findlater, Cherep et al.), regulatory state (EU AI Act, US state laws), market data (Adobe Analytics, McKinsey), and field-survey claims (Vercel AI SDK status, Linear AI, Apple Intelligence) are sourced from the dual-agent run and verified against primary publications. The Sentient Triangle attribution to Matt Webb (*Mapping the Landscape of Gen-AI Product UX*, July 2024) is preserved per Clark & Kindred's own credit. The "molten UX" non-finding — the phrase does not appear in the book, in the Big Medium catalogue surveyed, or in the verified talk transcripts — is preserved as a deliberate negative finding from the foundation-paper synthesis. The agentic-commerce traffic data (Adobe ~693% YoY, ~31% conversion premium) and the second manipulation vector (Cherep, Maes & Singh; Liou et al.; Liu & He) are findings the dual-agent run surfaced through its verification step that neither original agent pass had as load-bearing. The companion file is 27-adaptive-interfaces-implementation. The leadership-brief framing of this file's commercial implications is preserved separately at `_research/_synthesis/2026-05-21-adaptive-ui-leadership-brief.md`. Where claims depend on platform / spec / regulatory state — Vercel's AI SDK RSC status, EU AI Act dates, US state AI law operative dates, specific Adobe / Notion / Linear / Apple feature names — verify against the primary source before client-facing recommendation; this field rotates fast.*

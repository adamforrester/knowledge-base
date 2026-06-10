# Adaptive Interfaces: A Foundation Paper

*A senior design-systems leader's survey of sentient design, generative UI, agentic UX, and what's actually shipped. Synthesis edition — May 2026.*

---

## Preface — How to read this

This is a long-form analytical essay, not a reference document. It is meant to be read straight through, then mined later for citations. It is weighted to shipped reality; speculation is labeled inline with `*[speculative]*` or sequestered in a "Where this might be headed" subsection. It deliberately sits with tensions rather than resolving them prematurely, because the field is too young and the disagreements are too productive to flatten.

This edition is a **synthesis**. It integrates two independent research passes on the same brief and applies a round of corrections from a verification step that checked the load-bearing claims against primary sources. That process is worth one sentence of method, because it changed the paper: neither pass was uniformly right. The more hedged pass missed a real market event; the more confident pass overstated a technical retreat and got an accessibility claim flatly wrong. Where the two disagreed, the verification — not the tone — decided.

Three things to flag at the top, in order of how much they should change your priors:

1. **The "molten UX" phrase commonly attributed to Josh Clark could not be verified** in any public Big Medium article, talk transcript, or podcast appearance reviewed for this paper. The Sentient Design vocabulary owns *radically adaptive*, *thawing frozen formats*, and *call-and-response UI* — but not *molten UX*. If you have seen it cited, treat the attribution with caution.

2. **The strongest empirical case for adaptive UIs lives in accessibility research that contemporary generative-UI marketing rarely cites.** Krzysztof Gajos's work at Harvard is the load-bearing evidence base for "adaptive UIs actually help users." Most product teams reaching for that claim have not read it — and, as the companion implementation paper documents, the QA infrastructure to *verify* an accessible adaptive interface is the least mature part of the whole stack. The best-evidenced reason to build this is also the hardest thing to prove you have built correctly.

3. **"Generative UI" sits in a more ambiguous place than either celebration or obituary.** Vercel popularized the term in March 2024 with an architecture — AI SDK RSC — that streamed React components straight from the model. As of 2026 that architecture is officially marked experimental in Vercel's own documentation ("we recommend using AI SDK UI for production"), has a published RSC-to-UI migration guide, and a GitHub discussion confirming RSC development is paused. But it was also extracted into its own maintained `@ai-sdk/rsc` package in v5 (July 2025), and `streamUI` still exists. The honest framing is *experimental, officially deprioritized for production, with a published migration path — maintained, not removed.* The term is louder in the discourse than in shipped production engineering, but it is not dead.

If you remember nothing else from this paper, remember that ordering of warnings.

---

## 1. Defining the territory

Six lineages converge on what is loosely called "adaptive UI" today. They use overlapping vocabulary, cite different authorities, optimize for different metrics, and frequently talk past each other. Naming them clearly is the first move.

| Lineage | Primary driver | Locus of interaction | Conceptual stance | Technical substrate |
|---|---|---|---|---|
| **Sentient Design** | Experience quality | The human user | AI as a responsive *design material* | Prompt rules, runtime design systems, constraint engines |
| **Generative UI** | Developer velocity | The client architecture | Programmatic streaming of components | AI SDK, RSC / typed message parts, Zod schemas |
| **Personalization (incumbent)** | Conversion optimization | Segmented cohorts | Select a pre-built variant for a profile | Adobe Target, Optimizely, Sitecore, rule + bandit engines |
| **Malleable software** | User agency | The human as creator | Software as user-editable clay | Local-first data, dynamic documents |
| **Adaptive interfaces (academic HCI)** | Physical & cognitive accessibility | The individual's abilities | Optimize layout to measured ability | Mathematical optimization, integer programming |
| **Agentic UX** | Goal execution | The agent as intermediary | The agent operates the interface for you | LLMs, tools, browser/accessibility-tree parsers |

### 1.1 Sentient Design (Josh Clark / Veronika Kindred / Big Medium)

Designer-facing, experience-led. Defined publicly in *Say Hello to Sentient Design* (Clark & Kindred, June 2024) as "the already-here future of intelligent interfaces: experiences that feel almost self-aware in their response to user needs," organized around two attributes — *aware* and *radically adaptive* — supported by collaborative, multimodal, continuous/ambient, and deferential characteristics.[^1]

The key move in this lineage is *scope*. Clark explicitly refuses to let "making stuff" (generation) define the practice. Generation is one of five "machine-learning superpowers" alongside recommendation, prediction, classification, and clustering. Sentient Design is therefore broader than generative UI (which it treats as one pattern) and broader than personalization (one tactic for adaptation).[^1] The framing is "form, framework, and philosophy" — above the level of any single technique. Vocabulary worth knowing: *radically adaptive*, *aware* and *deferential*, AI as *design material* in its *awkward adolescence*, *call-and-response UI* ("the LLM talks to the interface, not the user")[^2], *frozen formats* and *thawing* them, the designer as *creative director* setting rules and pattern libraries for AI to compose against.[^2]

Where the lineage has sharpened: design systems. In 2024 essays they were largely implicit. By "Wiring Interface to Intent" (Clark, October 2025) they are explicitly the substrate on which adaptive UI runs: "Clean, context-based design systems are more important than ever."[^2] The LLM "can only assemble what designers have already built and documented."

### 1.2 Generative UI (Vercel et al.)

Engineering-facing, narrower. The term was popularized by Vercel in *AI SDK 3.0 with Generative UI Support* (March 2024).[^3] The canonical demo: a user asks "What is the weather in SF?", the model invokes a `get_city_weather` tool, a spinner streams in, then a `<Weather/>` component renders inline.

The shipped reality is narrower than the term, and the architecture's status is genuinely mixed — see Preface flag 3. The original RSC-based primitives are flagged experimental in Vercel's own docs, with a migration guide steering production developers to AI SDK UI's typed `message.parts` model; RSC development is paused; yet the code persists in a dedicated `@ai-sdk/rsc` package.[^4] NN/g's broader definition by Moran and Gibbons (March 2024) — "a user interface that is dynamically generated in real time by artificial intelligence to provide an experience customized to fit the user's needs and context"[^5] — describes an aspiration. The shipped pattern is closer to "constrained component selection within a chat surface." Neither "industry-standard developer model" nor "active retreat" is accurate; the middle position is.

### 1.3 Personalization (Adobe, Sitecore, Optimizely, Salesforce, Dynamic Yield)

Older, originally rule-based, the incumbent. Every major platform now offers two flavors: rule-based ("if segment X then offer Y" — the marketer decides, the system executes) and ML-driven ("here is the candidate set and the goal metric, you pick"). Adobe's Auto-Target / Automated Personalization runs Random Forest models retrained every 24 hours, with multi-armed bandits and Thompson Sampling fallback;[^6] Optimizely uses multi-armed bandits and is roadmapping contextual bandits;[^7] Sitecore exposes "analytical models" inside a decision canvas.[^8]

The unit of personalization is remarkably narrow across all of them: an Offer slotted into an Experience inside an Activity. What varies per user is hero/banner content, teaser images, recommendation strips — almost nothing varies *structurally*. Fifteen years of production practice has refined fine-grained content swapping inside a fixed page skeleton. Where LLMs are entering the incumbent stack, it is the *authoring* layer, not the decisioning layer: Sitecore's Code Assistant turns natural language into decision logic; Adobe Target ships an in-product AI Assistant and an MCP server. The model that *picks the variant* is still a Random Forest or a bandit.[^6][^9]

### 1.4 Malleable software (Ink & Switch, Litt, Appleton, Matuschak)

Research/philosophical, and structurally in tension with the dominant generative-UI narrative. Generative UI is *system-generated*: the AI produces an interface from inferred context. Malleable software argues software should be *user-authored*, with AI as a collaborator inside a medium the user controls. The Ink & Switch position essay *Malleable Software: Restoring User Agency in a World of Locked-Down Apps* (Litt, Horowitz, van Hardenberg, Matthews; June 2025) frames mass-produced apps as locked-down "appliances" and argues "AI code generation alone does not address all the barriers to malleability."[^10] Litt's earlier hybrid model (March 2023) put direct manipulation in the inner loop and the LLM as "local developer" in the outer loop, with the user's reliance on AI *decreasing* over time.[^11] By 2025 Litt had shifted toward HUD-style interfaces over chatty copilots.[^12]

The distinction matters: generative UI optimizes for *the user not having to think about the interface*; malleable software optimizes for *the user being able to reshape it*. One is convenience; the other is agency.

### 1.5 Adaptive interfaces — academic HCI (Gajos, Wobbrock, Findlater)

The academic root, twenty years of empirical work, almost entirely uncited in current practitioner discourse. Gajos's SUPPLE work (2004 onward) framed automatic UI generation as constrained optimization: given an abstract specification and a model of the user's device and abilities, search the space of renderings to minimize estimated effort.[^13] Concretely, SUPPLE treats interface construction as an integer-programming problem — minimizing a cost function summed over interactive elements, weighted by each element's expected frequency of use and the motor or visual difficulty it imposes given the user's measured ability profile. By 2007–2008, Gajos, Wobbrock, and Weld had shown that SUPPLE-generated interfaces matched to a user's measured motor abilities significantly outperformed default interfaces for users with motor impairments — *and* those users *preferred* the adapted UI.[^14][^15] Preference and performance moved together, which is rare in adaptive-UI research.

The canonical Wobbrock et al. *Ability-Based Design* paper (TACCESS 2011; CACM 2018) articulates the philosophy: design for ability rather than disability; let systems adapt to the person rather than asking the person to adapt to the system.[^16][^17] Findlater & McGrenere's CHI 2004 study is the cautionary anchor: *adaptable* (user-controlled) menus outperformed *adaptive* (system-controlled) ones on satisfaction, and many participants preferred the static baseline outright.[^18] Findlater & Gajos's 2009 *AI Magazine* survey is the field's accumulated humility: benefits are real but conditional on prediction accuracy, stability, and the cost-of-error model.[^19]

### 1.6 Agentic UX (NN/g, Replit Agent, computer-use models)

The agent-does-the-work framing. NN/g's Sponheim (April 2026) defines an AI agent as "a system that pursues a goal by iteratively taking actions, evaluating progress, and deciding its own next steps."[^20] Gibbons & Moran (April 2026) argue agents *are becoming users* of digital interfaces — "'user' is no longer synonymous with 'human'" — and that some businesses have legitimate reasons to resist agent access: "not all friction in an interface is a design failure."[^21] Liu & Rosala's Qwen study (NN/g, May 2026, n=6) is the only original empirical agentic-UX study from NN/g this paper found: 5 of 6 participants defaulted to traditional apps over an integrated agent; data-leak alarm surfaced at the authorization moment; abandoned tasks when the agent hid decision-relevant data.[^22]

### 1.7 The axis the lineages disagree on — and which framings to use

These six do not reconcile, and it is worth naming precisely why: **they disagree on who holds final agency.** Sentient Design and Generative UI place agency with the system, which interprets intent and compiles the layout. Malleable software insists agency must stay with the human, warning that automatic layout engines turn computing into un-inspectable black boxes. Agentic UX delegates agency to a third party — the agent — acting on the user's behalf. Personalization and academic adaptive interfaces sit in between: the system acts, but within a closed candidate set or against a measured ability model. A senior leader who treats "adaptive UI" as one thing will keep collapsing this axis; every hard design decision downstream is really a decision about where agency sits.

For making decisions in mid-2026, three framings carry the most weight. **Sentient Design** as the strategic vocabulary, because it is the only lineage that gives designers language for the full surface area and insists on *deferential* design. **Personalization-incumbent practice** as the engineering baseline, because the bandit-driven, slot-based infrastructure already running at scale is what most organizations should compose with, not replace. **Ability-based design** as the empirical conscience, because it is the body of evidence most likely to keep teams honest about whether their adaptive UI helps anyone. The other three are best treated as correctives: generative UI gives engineering primitives but smaller scope than its name; malleable software is the right long-term direction for *some* categories; agentic UX moves fastest but has the thinnest empirical base.

---

## 2. Personalization vs. adaptation — a critical distinction

Pull these apart explicitly, because the marketing copy does not.

| Vector | Personalization | Adaptation |
|---|---|---|
| Unit of analysis | Demographic / behavioral cohort | Real-time situational intent and capability |
| Temporal model | Latency-tolerant; computed asynchronously from profiles | Real-time; compiled in the interaction loop |
| Architecture | Deterministic rule engines, bandits, static variants | Generation guided by dynamic constraint envelopes |
| What changes | Copy, media, promo blocks within a fixed grid | Structural and layout-level transformation |
| Primary failure | Stale cohort data, misprofiling, cookie/privacy loss | Hallucinated controls, disorientation, broken muscle memory |

**Personalization** is segment-driven: *user is in cohort X, show variant Y.* The cohort may be authored by a marketer or learned by a model, but the unit of variation is *which pre-built variant gets served*. The candidate set is closed; the design system is intact. **Adaptation** is context-driven: *user is doing Z right now.* The candidate is constructed, or selected from a much larger latent space, for this moment for this user. Granola's meeting templates change because the calendar event says "user research." Dia's Morning Brief composes from this morning's Slack, calendar, and inbox.

The failure modes differ. Personalization fails *between* sessions — a one-time gift purchase poisons recommendations for months; mature recommenders therefore all expose an escape hatch (TikTok's "Not Interested," YouTube history pause).[^23] Adaptation fails *within* a session — the interface guesses wrong about the current task and the repair has to happen in seconds, not weeks. Both can coexist: server-side personalization can decide which content library is injected, after which client-side adaptation restructures the live layout for touch, glare, or motion. The cleanest tell that the two are different: the academic literature finds preference and performance move *together* for ability-based personalization but often move *apart* for system-driven within-session adaptation.[^14][^18] Personalization rewards stability across time; adaptation rewards responsiveness within it. Confusing them is the most common diagnostic error in the discourse.

---

## 3. The user experience of adaptive UI

### 3.1 Trust and the "creepiness" tension

The historical anchor is not Clippy, it is *Lumiere*. Eric Horvitz's UAI 1998 paper on Bayesian user modeling was more cautious than Clippy's launch behavior implied.[^24] Clippy's failure was a productization decision — an always-visible animated agent — imposed on a probabilistic system that was modest about itself. Horvitz had already articulated, in *Principles of Mixed-Initiative User Interfaces* (CHI 1999), the rule that would have prevented it: an agent should act only when the expected utility of acting exceeds that of inaction, and should always preserve the user's ability to reject the action cheaply.[^25] Luke Swartz's 2003 Stanford retrospective names the breakdown a *consistency* failure — an agent's name, appearance, voice, and behavior must align with each other and with users' expectations.[^26] Both diagnoses are still operative, and they are compatible: Clippy breached social expectation (the Reeves & Nass *Media Equation* mechanism) *and* was inconsistent between its friendly face and its modest capability. Clark's *Sparkles Are Fizzling* (2024) makes the same argument in current vocabulary — the purple-gradient AI cliché now overpromises exactly as the animated paperclip did.[^27]

### 3.2 The mental-model cost

Findlater & McGrenere 2004 remains the reference experiment: adaptive (system-controlled) menus underperformed adaptable (user-controlled) menus on satisfaction, and a meaningful subset of users preferred the static baseline for spatial stability.[^18] The cost lives largely in the perceptual layer — spatial memory, surprise — not the inference layer. Classic cognitive laws (Hick's, Fitts's) explain why: any layout change resets learned motor paths and forces visual re-evaluation. Findlater et al.'s 2009 *Ephemeral Adaptation* showed gradual onset of adapted items improves performance without harming spatial memory.[^28] The implication for genUI is uncomfortable: *muscle memory is a feature, not a bug.* Christopher Butler's *Consistency Is Primitive* (2026) takes the contrary view — consistency is "civilizational infancy" dissolved by AI infrastructure[^29] — and NN/g's Moran is the direct counter: most users "cannot articulate what interface they need," so genUI carries a *higher* design burden than vibe coding.[^30] This debate is live; which side a team takes determines whether their product looks like Linear or like a bespoke-per-user surface no one shares vocabulary about.

### 3.3 Disclosure, agency, and control

Three patterns recur across mature implementations. **Visible thinking surfaces** — Linear's Triage Intelligence shows a reasoning trace and timer; Vercel's AI SDK added typed `reasoning` parts; generative UI is making "what the model is doing" a UI element. **Cheap dismissal** — Horvitz's "efficient invocation and dismissal" is now the determinant of perceived intelligence; an affordance that is cheap to summon and cheap to ignore reads as intelligent. **Side-by-side over in-line** — Artifacts, ChatGPT Canvas, v0's design mode, Dia's Splits converge on chat-as-log-of-intent beside artifact-as-work.

### 3.4 When users want adaptation vs. predictability

The empirical cut is cleaner than the discourse suggests. Users want adaptation when the cost of getting the interface right manually is high (accessibility, unfamiliar tasks), the consequences of the system being wrong are low (browsing, ambient surfaces), and the user has no strong prior model of the surface. Users want predictability when they are doing something familiar with built muscle memory (professional tools), the consequences of error are high (regulated, transactional flows), or they share the surface with others and need a common reference. Most products span both regimes; the design move is *naming which mode the user is in* and not changing the interface in the wrong one.

### 3.5 The empirical thinness should be named

NN/g's empirical base on agentic UX is thinner than the volume of articles suggests: one definitional piece, one n=6 study.[^20][^22] The most concrete positive genUI finding is modest — chat-embedded checkboxes and buttons measurably reduce friction over text-only follow-ups.[^31] Beyond that, the field runs largely on demos and small qualitative studies. The Gajos accessibility evidence remains the cleanest empirical case for adaptive UI, and is almost never cited by current practitioners.

---

## 4. What problems does this actually solve

### 4.1 Accessibility — the strongest case

The Gajos / Wobbrock work is the load-bearing evidence base. Motor-impaired participants completed tasks significantly faster, made fewer errors, and preferred the adapted UI.[^15] Ability-based design is now embedded in iOS VoiceOver gestures and a generation of accessibility infrastructure.[^17] The signal is robust and specific: when *abilities are measurable* (motor accuracy, vision, working memory) and the system *actually models them* before adapting, adaptive UI delivers — for the population that needs it most.

The corollary cuts the other way. Most "AI personalization" is correlational — it learns what users tend to choose, not what they are *able* to do well. The marketing case for "AI improves accessibility" is much weaker than the academic case for *ability-based design improves accessibility*. And, as the companion implementation paper details, the QA tooling to verify an accessible *variable* surface is the least mature part of the stack. Senior leaders making the inclusivity argument should cite Wobbrock and Gajos, not Vercel — and should scope accessibility verification as real, manual, ongoing work, not a checkbox.

### 4.2 Discovery and cognitive load for occasional/novice users

Recommendation-system practice has fifteen years of evidence that personalized discovery surfaces improve engagement. Netflix's 2016 disclosure that 82% of browsing focus is on artwork during a ~90-second decision window, with artwork variants A/B-tested per title, is the canonical proof.[^32] Spotify's Daily Mix clusters listener history into daily-refreshed playlists.[^33] The strongest discovery wins are for users who *don't yet know* what they want — which makes cold start a first-class design problem, and means any adaptive UI without an explicit "I don't know you yet" mode degrades for every new user and cleared cookie.

### 4.3 Onboarding and time-to-value

Genuine but conditional gains. Granola's adapt-to-meeting-title pattern is the cleanest example — users get useful structured notes from the first meeting because the system inferred the meeting type from the calendar event.[^34] Linear's Triage Intelligence reduces the manual triage tax for a new PM joining a workspace.[^35] The trend is to *use the user's existing context* (calendar, workspace, tabs) rather than ask new users to fill profile fields — a real shift from the personalization-incumbent paradigm. Adaptive interfaces can also progressively disclose complexity: a clean onboarding layout that exposes dense panels and shortcuts as the user demonstrates mastery.

### 4.4 Where it underperforms or backfires

Power users (Findlater & McGrenere — many prefer static menus[^18]; Saarinen's "a chat interface is a very weak and generic form"[^36]). Regulated UIs, where varying the *path* through a consequential decision is a compliance-perimeter problem. Brand-led marketing surfaces, where the surface itself is the brand artifact and varying it erodes the consistency the brand pays for. Professional tools where consistency is a feature — Linear's "workbench" framing is the right pattern for this class: keep the deterministic UI stable, layer AI on top with full auditability.[^36] Saarinen's *Output Isn't Design* (April 2026) — "the risk is mistaking generated form for solved problems"[^37] — is a direct rebuttal to the designer-as-creative-director-of-AI-output posture.

---

## 5. Ethics, dark patterns, manipulation

The strongest non-vague critique of adaptive UI is structural and arrives in four layers.

### 5.1 The EU AI Act's manipulation prohibition is live

EU AI Act Article 5(1)(a)–(b) entered into force on 2 February 2025.[^38] It prohibits AI systems that "deploy subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques" with the objective or effect of "materially distorting the behaviour of a person … by appreciably impairing their ability to make an informed decision," causing or reasonably likely to cause significant harm. Recital 29 contains the load-bearing line for adaptive UI: subliminal stimuli include cases where users "are aware of them, [but] can still be deceived or are not able to control or resist them" — and *intent is not required; effect is sufficient.*[^39] Adaptive UI that materially distorts behavior and causes significant harm is illegal in the EU regardless of whether the team intended manipulation.

### 5.2 US state-level disclosure regimes are arriving

Three pressure points are on the books. **Colorado SB24-205** (operative February 2026) mandates consumer disclosure for AI systems "intended to interact with consumers" and triggers impact assessments and discrimination-risk reporting in consequential decisions.[^40] **California SB 942** (operative January 2026) requires latent provenance disclosure in generative content from large providers, with a $5,000-per-violation-per-day penalty.[^41] **California AB 2013** (compliance January 2026) requires a published "high-level summary of the datasets" used in training.[^42] Together they form a real compliance perimeter; the "figure out ethics later" posture has expired.

### 5.3 The manipulation surface has two vectors — and the second is new

Classical dark-pattern research covers the first vector: a *designer* manipulates a *user*, now with AI as the tool. A metric-driven adaptive engine sharpens this — if an algorithm learns that a low-contrast, oddly-placed cancel button raises retention, a purely metric-optimizing engine will deploy that pattern autonomously, with no human ever explicitly designing the dark pattern. That alone is a governance problem.

The second vector is newer, and verification for this synthesis made it load-bearing: **the LLM itself is a manipulation target.** Cherep, Maes & Singh's *LLM Agents Are Hypersensitive to Nudges* (MIT/Dartmouth, 2025) tested GPT-3.5, GPT-4o, o3-Mini, Gemini 1.5 Flash and Pro, and Claude 3 Haiku and 3.5 Sonnet against canonical choice-architecture nudges (defaults, decoys, framing) and found "much higher susceptibility to the nudges" than human baselines.[^43] Liou et al.'s *OI-Bench*, an option-injection benchmark, tested twelve LLMs on directive interference and found "substantial vulnerabilities and heterogeneous robustness across models."[^44] The finding is consequential because of where the Agentic UX lineage is heading: as agents become the intermediaries that read pages, compare options, and act on the user's behalf, the manipulation target shifts from the human's psychology to the *agent's*. An adversary no longer has to nudge you; they nudge the agent shopping for you, by arranging the content or options it ingests. This complicates the agentic UX framing directly — the same RAG and retrieval layers that make an interface adaptive are an attack surface, and decoy or option injection into retrieved context is not theoretical.

### 5.4 The epistemic critique

Maggie Appleton's *Expanding Dark Forest* talk supplies the content-level critique: as adaptive interfaces train on model-generated data, "that tenuous link to the real world becomes completely divorced from it."[^45] Butler's *Consistency Is Primitive* supplies the corollary: when each user inhabits a bespoke interface, shared reference points dissolve, and so does the ability to recognize manipulation collectively.[^29] Manipulation becomes invisible because there is no peer experience to compare against.

### 5.5 What designers can do

Four moves. **Make the system prompt a design artifact** — Linear's "Additional Guidance" surface exposes the prompt to workspace operators; rule sets need design review and version control.[^35] **Default to deferential UI** — visible thinking plus cheap dismissal, not sparkles that overpromise.[^27] **Audit for choice-architecture exposure on both vectors** — treat the retrieved-context layer as an attack surface against the model, and audit the optimization objective for emergent dark patterns against the user. **Maintain an auditable variant log** — Article 5 enforces on *effect*; the only credible defense is the ability to demonstrate, post hoc, which variants were surfaced to a user and why.

---

## 6. Industries and use cases

The viability of adaptive UI is highly dependent on the vertical — but not in the way a simple fit table implies.

**Strong fit.** *Media* — Netflix and Spotify are the proof; recommendation plus visible escape hatches plus contextual signals is the dominant adaptive-UI shape on the consumer web. *Productivity SaaS* — Linear, Notion, Granola, Dia; the "agent over a stable workbench" pattern is mature enough to ship. *Education* — adaptive UI as scaffolding for the learner's authentic work, with high variance in learning speed to absorb. *Healthcare, specific surfaces only* — patient-education content and accessibility surfaces; anything touching diagnosis or consequential decisions belongs in the weak-fit list.

**Ambiguous fit.** *Search* — Google AI Mode's query fan-out adapts what queries to issue, not what UI to render. *Browsers* — Arc's quiet retraction of *Browse for Me* and The Browser Company's pivot to Dia is the empirical answer: aggressive adaptive UI in the browsing surface failed to find product-market fit; context-aware assistance with a conventional surface survived. *Mobile platform shells* — Apple Intelligence is the cautionary case; the highest-muscle-memory surface with the highest cost-of-wrong.

**Weak fit.** Regulated UIs; brand-controlled marketing surfaces; professional tools where consistency is a feature; anything where shared reference matters (collaborative and teaching tools).

**E-commerce — the case that breaks the binary.** Both "strong fit" and "ambiguous fit" are wrong as verdicts, because the evidence is strong on *both* sides. The ROI case is well-evidenced: McKinsey's personalization research puts typical revenue uplift at 10–15%, up to ~25% best-case;[^46] real-time personalization outperforms batch by roughly 20% on conversion; documented rules-to-ML migrations show CTR lifts averaging ~41% across dozens of cases; individual retailers (Wayfair among them) report conversion improvements around 40% and meaningful return-rate reductions.[^47] The risk case is *equally* well-evidenced: a growing cluster of 2024–2025 PLS-SEM studies (across Indonesian, Turkish, and fashion e-commerce samples) document the Personalization-Privacy Paradox empirically — perceived overreach, data-misuse fear, and algorithmic-manipulation perception drive measurable backlash, with privacy-violation perception the central psychological pathway from surveillance to reduced purchase intent, and brand trust acting as the moderator.[^48]

So the variable that decides the outcome is not the industry — it is *execution quality*: brand-trust capital, transparency-by-default architecture, governance maturity, and willingness to invest in privacy-preserving infrastructure (federated learning, differential privacy, on-device personalization). The honest verdict for a client conversation: e-commerce is simultaneously the **highest-evidenced use case for measured ROI and the highest-evidenced for failure modes.** Whether to recommend it turns on trust capital and privacy infrastructure, not on the sector label. That is more useful guidance than either pure verdict.

---

## 7. Examples in production today

Concrete and cited.

**Vercel v0 and the AI SDK.** v0.app today is best described as agentic application generation — "Agentic by default. Prompt. Build. Publish." The durable contribution is the AI SDK underneath: typed `message.parts` (`text`, `source`, `reasoning`, `tool-invocation`, `file`), MCP client support, tool-call streaming. The RSC-based generative-UI primitives sit in the experimental-but-maintained state described in §1.2.[^3][^4]

**Linear AI.** Triage Intelligence (September 2025) — duplicate/related-issue suggestions, a thinking panel with a reasoning trace, a workspace-level "Additional Guidance" prompt. Linear Agent, Skills and Automations, an AI filter, AI-generated release notes, Mobile Agent Sessions.[^35][^49] The throughline matches Saarinen's "workbench" thesis: stable conventional UI, AI layered on top with full auditability.

**Notion AI.** Notion Agent, Custom Agents with credit budgeting, AI Meeting Notes, Enterprise Search, Research Mode, inline AI blocks, database autofill — AI interacting with discrete block units rather than mutating a global canvas.[^50]

**Anthropic Artifacts and ChatGPT Canvas.** Both solve the "chat bubble bottleneck" by splitting the surface — conversation on one side, an executable/editable artifact on the other, rendered in a client-side sandbox. Artifacts reached GA in August 2024; Canvas launched October 2024.[^51][^52]

**Granola.** The cleanest production example of slot-based adaptive UI: a hand-designed shell, hand-defined section types, generated section *content*, and the *which sections* selected by inferring the meeting type from the calendar event title.[^34]

**Spotify and Netflix.** The long-running pre-LLM baseline — homepages that personalize which rows appear, which titles, and their ordering, on a grid skeleton that stays familiar.[^32][^33] Treating per-user artwork variation as a 2024 generative-UI invention misreads a decade-old inheritance.

**Apple Intelligence.** The cautionary case — onscreen awareness, personal-context Siri, and cross-app actions were still labeled "in development" eighteen months after announcement. The platform-shell surface is uniquely hard: high cost-of-wrong, strongest possible muscle memory.

### 7.1 The agentic-commerce traffic shift — the signal both research passes missed

One development belongs here that neither original research pass surfaced, and it reframes what "adaptive UI for e-commerce" even means. Adobe's analysis of the 2025 holiday season found traffic arriving at US retail sites *from* generative-AI sources — users following a recommendation from ChatGPT, Claude, Perplexity, and similar — up roughly **693% year over year**, and those AI-referred shoppers converting about **31% higher** than traffic from traditional channels.[^53][^54]

The number is still a small share of total traffic, but the trajectory is the point. It marks the early shape of *agentic commerce*: the customer increasingly reaches the retailer through an AI agent's recommendation rather than through search or direct navigation. The agent is not only adapting the on-site experience — it is becoming the *referrer*, and sometimes the buyer. For any client with consumer-facing commerce, this changes the question. "Adaptive UI for e-commerce" has quietly stopped meaning only "a smarter product page" and started also meaning "being legible, and persuasive, to the agent that decides whether your product is shown at all." That is a foundation-level shift, and it connects directly to §1.6's observation that agents are becoming users — here they are becoming *customers' proxies*.

---

## 8. Where this might be headed *[speculative]*

*[speculative]* Clark's *What Happens When Agents Meet?* (February 2026) makes the most concrete prediction: "the unit of design is no longer only the agent or even the user; it's the population and the systems it affects." Multiple agents acting on users' behalf will encounter each other and negotiate — and almost nothing is designed for that. Saarinen's *Output Isn't Design* makes the contrarian prediction: the designers and tools that survive will produce *fewer, more considered* surfaces, not more bespoke ones.[^37] Both can be true: adaptive UI expands into ambient and contextual surfaces while the deliberate, designed surface becomes *more* valuable by contrast.

*[speculative]* The slot-based generation pattern (Granola, Linear, Dia) becomes the dominant shape; free-form per-user UI generation does not become a mass-market pattern in 2–3 years. *[speculative]* Recommendation practice and generative-UI practice converge at the *layout* level — Spotify's *Prompt-to-Slate* research is a leading indicator. *[speculative]* Agentic commerce (§7.1) compounds: by 2027 a meaningful share of retail discovery is agent-mediated, and "optimize for the agent" becomes a named discipline. *[speculative]* Regulatory enforcement of EU Article 5 against a high-profile adaptive-UI deployment lands within 2–3 years and pushes variant-logging infrastructure toward being a default.

What is **hype**: that "every interface will be unique per user" — destructive for any product where users discuss, share, or teach the interface, and unlikely to survive the workplace. That "design systems will become irrelevant" — every credible voice locates them as *more* central. That prompting is the future of HCI — Litt, Saarinen, and Appleton all argue from different directions that text prompting is a transitional pattern.

---

## 9. Brief design systems thread

Does a design system survive this paradigm? Yes — the genuine question is what it constrains. The traditional design system constrains *what gets built*: a closed catalog of components and tokens. The adaptive-UI design system constrains *what gets generated*: the catalog, plus the rule set the LLM composes from, plus the variant-logging infrastructure that makes the generation auditable. It shifts from a library of static blocks to a system of rules and constraints — abstract token schemas, declarative component definitions, structural layout templates with slots.

Three concrete shifts. **The system prompt becomes a design artifact** — Linear's "Additional Guidance" surface is the early production example; rule sets need design review and version control. **Component metadata grows** — beyond visual specification, components need machine-readable descriptions of *when to render this*, *what context it requires*, *what alternatives it has*; a design system without intent metadata cannot participate in generation. **Variant logging becomes infrastructure** — EU Article 5 enforces on effect, and the only credible defense is demonstrating which variants reached which user and why.

"Consistency" shifts meaning — from *every user sees the same surface* to *every user can predict and trust the surface they see*. The components stay consistent; the compositions vary within rules the design system enforces. The detailed implementation work — component APIs, intent metadata, variant logging, compliance instrumentation — belongs in the companion implementation paper. Conceptually, the design system not only survives but becomes the load-bearing constraint that keeps adaptive UI from collapsing into chaos.

---

## Open questions

1. **Is "personalization" recoverable as a term, or so overloaded it now obscures?** This paper used it narrowly (segment-driven, profile-based) and used *adaptation* for context-driven within-session behavior. Whether the field consolidates around that distinction is unresolved.
2. **What does *consistency* mean operationally when surfaces vary?** Butler, Moran, and Clark may each be right at different time horizons; the practical guidance differs sharply by which a leader believes.
3. **How much of the genuine value is captured by accessibility specifically?** Gajos's evidence is the strongest in the field. If accessibility is doing most of the load-bearing work, much surrounding genUI marketing is overpromising on weaker evidence.
4. **Who governs variant logging?** EU Article 5 enforces on effect. No vendor or industry-body proposal exists for what good variant-logging looks like, who holds the logs, or how long they are retained. Possibly its own paper.
5. **How does the second manipulation vector get defended?** If LLM agents are hypersensitive to nudges and option injection, and agents increasingly mediate commerce and decisions, what is the defensive discipline — and whose job is it, the model provider's or the deploying designer's?
6. **Does agentic commerce make on-site adaptive UI more or less important?** If the agent is increasingly the referrer and the comparison-shopper, the retailer's own adaptive surface may matter less than its legibility to agents — or may matter more, as the place a hard-won agent-referred visit is converted.

---

## What to read next — ranked

1. **Wobbrock, Kane, Gajos, Harada & Froehlich (2011), *Ability-Based Design*** (TACCESS), and its CACM 2018 revisit. The empirical foundation; read first for a defensible accessibility position.[^16][^17]
2. **Clark & Kindred, *Say Hello to Sentient Design*** (Big Medium, June 2024). The clearest single piece in the lineage; defines the territory.[^1]
3. **Saarinen, *Design for the AI Age*** (Linear, April 2025). The strongest counter-position to chat-as-default.[^36]
4. **Horvitz, *Principles of Mixed-Initiative User Interfaces*** (CHI 1999). The cost-of-being-wrong framework underneath every copilot decision and failure.[^25]
5. **Cherep, Maes & Singh, *LLM Agents Are Hypersensitive to Nudges*** (2025). The verified basis for the second manipulation vector; required for anyone designing agent-mediated experiences.[^43]
6. **Litt et al., *Malleable Software*** (Ink & Switch, June 2025), with Litt's 2023 *Malleable software in the age of LLMs*. The clearest articulation of the user-authorship counter-lineage.[^10][^11]
7. **Findlater & Gajos, *Design Space and Evaluation Challenges of Adaptive Graphical User Interfaces*** (*AI Magazine*, 2009). The field's accumulated humility, and its most useful single survey.[^19]
8. **Moran & Gibbons, *Generative UI and Outcome-Oriented Design*** (NN/g, March 2024) and Moran, *GenUI vs. Vibe Coding* (March 2026).[^5][^30]
9. **Adobe Analytics, *2025 Holiday Shopping Report*** (with the Braze *2026 Customer Engagement Review*). The early data on agentic-commerce traffic.[^53][^54]
10. **Bret Victor, *Magic Ink*** (2006). Two decades old, and predicted today's inference hierarchy with more clarity than most contemporary writing.[^55]

---

## What surprised me — in this synthesis pass

Findings that emerged specifically from integrating two research passes and verifying their disputed claims — not present in either original.

1. **Confidence and correctness did not correlate the way the comparison expected.** The post-comparison verification flagged the more polished pass's surprising claims as "likely fabricated." On the load-bearing one — a market acquisition — the polished pass was *right* and the more hedged, more heavily-cited pass had simply missed a real event. Heavy citation is a measure of diligence, not of completeness. A confident assertion can be true; a well-hedged one can be a gap.

2. **Both passes were wrong about e-commerce, in opposite directions, and the truth was not the midpoint.** One called it a strong fit, the other ambiguous. Verification showed both bodies of evidence — the ROI case and the privacy-backlash case — are *strong*. The resolution was not "somewhere in between" but a reframe: the deciding variable is execution quality, not the industry. Averaging two verdicts would have produced a worse answer than discarding both.

3. **The manipulation story has a second vector that neither pass treated as load-bearing.** The original framing was designers manipulating users via AI. The verified nudge-hypersensitivity research moves the AI agent itself into the target position. That is not a footnote — it changes the agentic UX section from "agents are becoming users" to "agents are becoming *manipulable* users, acting on your behalf."

4. **The agentic-commerce traffic shift was invisible to both passes.** A ~693% year-over-year jump in AI-referred retail traffic is the kind of structural signal a foundation paper exists to catch, and neither research pass surfaced it. It is a reminder that synthesis is not just reconciliation of what was found — it sometimes has to add what was collectively missed.

5. **The strongest use case and the weakest verification capability are the same surface.** Accessibility is the best-evidenced reason to build adaptive UI (Gajos) and — per the companion paper's verified accessibility-QA correction — the hardest property to confirm once the surface is variable. That tension was implicit in both passes; the verification pass made it explicit, and it should shape how accessibility work is scoped on real engagements rather than being treated as a paralysis.

---

## Bibliography

[^1]: Clark, J., & Kindred, V. (2024, June 12). *Say Hello to Sentient Design.* Big Medium. https://bigmedium.com/ideas/hello-sentient-design.html

[^2]: Clark, J. (2025, October 2). *Wiring Interface to Intent.* Big Medium. https://bigmedium.com/ideas/wiring-interface-to-intent.html

[^3]: Vercel. (2024, March 1). *AI SDK 3.0 with Generative UI Support.* https://vercel.com/blog/ai-sdk-3-generative-ui

[^4]: Vercel. (2025–2026). *AI SDK RSC* [Documentation, RSC-to-UI migration guide, and `@ai-sdk/rsc` package notes]. https://ai-sdk.dev/docs/ai-sdk-rsc/migrating-to-ui ; RSC-pause discussion: https://github.com/vercel/ai/discussions

[^5]: Moran, K., & Gibbons, S. (2024, March 22). *Generative UI and Outcome-Oriented Design.* Nielsen Norman Group. https://www.nngroup.com/articles/generative-ui/

[^6]: Adobe. (n.d.). *Adobe Target — Automated Personalization activities* [Documentation]. https://experienceleague.adobe.com/en/docs/target/using/activities/automated-personalization/automated-personalization

[^7]: Optimizely. (n.d.). *Personalization using AI and experimentation.* https://www.optimizely.com/products/personalization/

[^8]: Sitecore. (n.d.). *Sitecore Personalize* [Product documentation]. https://doc.sitecore.com/personalize/en/users/sitecore-personalize/index-en.html

[^9]: Dynamic Yield. (n.d.). *Experience OS.* https://www.dynamicyield.com/

[^10]: Litt, G., Horowitz, J., van Hardenberg, P., & Matthews, T. (2025, June). *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch. https://www.inkandswitch.com/essay/malleable-software/

[^11]: Litt, G. (2023, March 25). *Malleable software in the age of LLMs.* https://www.geoffreylitt.com/2023/03/25/llm-end-user-programming

[^12]: Litt, G. (2025, July 27). *Enough AI copilots! We need AI HUDs.* https://geoffreylitt.com/2025/07/27/enough-ai-copilots-we-need-ai-huds

[^13]: Gajos, K. Z., & Weld, D. S. (2004). SUPPLE: Automatically Generating User Interfaces. *Proceedings of IUI '04.* https://doi.org/10.1145/964442.964461

[^14]: Gajos, K. Z., Wobbrock, J. O., & Weld, D. S. (2007). Automatically generating user interfaces adapted to users' motor and vision capabilities. *Proceedings of UIST '07.* https://doi.org/10.1145/1294211.1294253

[^15]: Gajos, K. Z., Wobbrock, J. O., & Weld, D. S. (2008). Improving the performance of motor-impaired users with automatically-generated, ability-based interfaces. *Proceedings of CHI '08.* https://doi.org/10.1145/1357054.1357250

[^16]: Wobbrock, J. O., Kane, S. K., Gajos, K. Z., Harada, S., & Froehlich, J. (2011). Ability-Based Design: Concept, principles and examples. *ACM TACCESS, 3*(3). https://doi.org/10.1145/1952383.1952384

[^17]: Wobbrock, J. O., Gajos, K. Z., Kane, S. K., & Vanderheiden, G. C. (2018). Ability-based design. *Communications of the ACM, 61*(6). https://doi.org/10.1145/3148051

[^18]: Findlater, L., & McGrenere, J. (2004). A comparison of static, adaptive, and adaptable menus. *Proceedings of CHI '04.* https://doi.org/10.1145/985692.985704

[^19]: Findlater, L., & Gajos, K. Z. (2009). Design space and evaluation challenges of adaptive graphical user interfaces. *AI Magazine, 30*(4). https://ojs.aaai.org/index.php/aimagazine/article/view/2268

[^20]: Sponheim, C. (2026, April 3). *A Concrete Definition of an AI Agent.* Nielsen Norman Group. https://www.nngroup.com/articles/definition-ai-agent/

[^21]: Gibbons, S., & Moran, K. (2026, April 10). *AI Agents as Users.* Nielsen Norman Group. https://www.nngroup.com/articles/ai-agents-as-users/

[^22]: Liu, F., & Rosala, M. (2026, May 8). *Designing AI Agents: 4 Lessons from China's Qwen Agent.* Nielsen Norman Group. https://www.nngroup.com/articles/designing-ai-agents/

[^23]: Schade, A. (2016, July 10). *Customization vs. Personalization in the User Experience.* Nielsen Norman Group. https://www.nngroup.com/articles/customization-personalization/

[^24]: Horvitz, E., Breese, J., Heckerman, D., Hovel, D., & Rommelse, K. (1998). The Lumiere project: Bayesian user modeling for inferring the goals and needs of software users. *Proceedings of UAI '98.* https://arxiv.org/abs/1301.7385

[^25]: Horvitz, E. (1999). Principles of mixed-initiative user interfaces. *Proceedings of CHI '99.* https://doi.org/10.1145/302979.303030

[^26]: Swartz, L. (2003). *Why People Hate the Paperclip: Labels, Appearance, Behavior, and Social Responses to User Interface Agents* [Honors thesis]. Stanford University.

[^27]: Clark, J. (2024, September 28). *Your Sparkles Are Fizzling.* Big Medium. https://bigmedium.com/ideas/your-sparkles-are-fizzling.html

[^28]: Findlater, L., Moffatt, K., McGrenere, J., & Dawson, J. (2009). Ephemeral adaptation: The use of gradual onset to improve menu selection performance. *Proceedings of CHI '09.* https://doi.org/10.1145/1518701.1518956

[^29]: Butler, C. (2026, February 19). *Consistency Is Primitive.* https://chrbutler.com/consistency-is-primitive

[^30]: Moran, K. (2026, March 27). *GenUI vs. Vibe Coding: Who's Designing?* Nielsen Norman Group. https://www.nngroup.com/articles/genui-vs-vibe/

[^31]: Moran, K. (2026, March 6). *The Most Exciting Development in GenUI: Buttons and Checkboxes.* Nielsen Norman Group. https://www.nngroup.com/articles/genui-buttons-and-checkboxes/

[^32]: Nelson, N. (2016, May 3). *The Power of a Picture.* Netflix. https://about.netflix.com/en/news/the-power-of-a-picture

[^33]: Spotify Newsroom. (2018, May 18). *How Your Daily Mix 'Just Gets You.'* https://newsroom.spotify.com/2018-05-18/how-your-daily-mix-just-gets-you/

[^34]: Granola. (n.d.). *Granola — The AI notepad for people in back-to-back meetings.* https://www.granola.ai/

[^35]: Linear. (2025, September 3). *How we built Triage Intelligence.* https://linear.app/blog/how-we-built-triage-intelligence

[^36]: Saarinen, K. (2025, April 7). *Design for the AI Age.* Linear. https://linear.app/now/design-for-the-ai-age

[^37]: Saarinen, K. (2026, April 17). *Output Isn't Design.* Linear. https://linear.app/now/output-isn-t-design

[^38]: European Union. (2024). *Artificial Intelligence Act, Article 5* [Effective February 2, 2025]. https://artificialintelligenceact.eu/article/5/

[^39]: European Union. (2024). *Artificial Intelligence Act, Recital 29.* https://artificialintelligenceact.eu/recital/29/

[^40]: Colorado General Assembly. (2024, May 17). *Senate Bill 24-205 — Consumer Protections for Artificial Intelligence.* https://leg.colorado.gov/bills/sb24-205

[^41]: California Legislature. (2024, September 19). *Senate Bill 942 — California AI Transparency Act.* https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB942

[^42]: California Legislature. (2024, September 28). *Assembly Bill 2013 — Generative AI: Training Data Transparency.* https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013

[^43]: Cherep, M., Maes, P., & Singh, P. (2025). *LLM Agents Are Hypersensitive to Nudges.* arXiv:2505.11584. https://arxiv.org/abs/2505.11584

[^44]: Liou, et al. (2025). *OI-Bench: An Option Injection Benchmark for Directive Interference in LLMs.* National Yang Ming Chiao Tung University.

[^45]: Appleton, M. (2023, April; expanded 2024). *The Expanding Dark Forest and Generative AI* [Talk + transcript]. Causal Islands. https://maggieappleton.com/forest-talk

[^46]: McKinsey & Company. (2021, November 12). *The value of getting personalization right—or wrong—is multiplying* [Next in Personalization Report]. https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/the-value-of-getting-personalization-right-or-wrong-is-multiplying

[^47]: Industry case-study data on e-commerce personalization ROI, 2024–2025 (aggregated vendor case studies, including Wayfair conversion and return-rate reporting, and rules-to-ML migration case sets). Figures reported during the verification pass for this synthesis.

[^48]: Representative empirical work on the Personalization-Privacy Paradox in e-commerce, 2024–2025 — a cluster of PLS-SEM studies across Indonesian, Turkish, and fashion e-commerce samples modeling privacy-violation perception as the pathway from perceived surveillance to reduced purchase intention, with brand trust as moderator. Identified during the verification pass; see also Schade, NN/g personalization guidance [^23].

[^49]: Linear. (2026). *Changelog.* https://linear.app/changelog

[^50]: Notion. (n.d.). *Notion AI.* https://www.notion.com/product/ai

[^51]: Anthropic. (2024, August 27). *Artifacts are now generally available.* https://www.anthropic.com/news/artifacts

[^52]: OpenAI. (2024, October 3). *Introducing Canvas.* https://openai.com/index/introducing-canvas/

[^53]: Adobe. (2026, January). *Adobe Analytics: 2025 Holiday Shopping Report* [AI-driven traffic and conversion data]. https://business.adobe.com/resources/holiday-shopping-report.html

[^54]: Braze. (2026). *2026 Customer Engagement Review.* https://www.braze.com/resources/reports-and-guides/customer-engagement-review

[^55]: Victor, B. (2006). *Magic Ink: Information Software and the Graphical Interface.* https://worrydream.com/MagicInk/

---

### Additional sources consulted

- Clark, J., & Kindred, V. (2025, September 30). *When Interfaces Design Themselves.* Big Medium.
- Clark, J. (2026, February 4). *What Happens When Agents Meet?* Big Medium. https://bigmedium.com/ideas/what-happens-when-agents-meet.html
- Saarinen, K. (2025, December 19). *Design Is More Than Code.* Linear. https://linear.app/now/design-is-more-than-code
- Appleton, M. (2023). *Squish Meets Structure: Designing with Language Models* [Talk + transcript]. https://maggieappleton.com/squish-structure
- Spotify Research. (2025, September 9). *Prompt-to-Slate: Diffusion Models for Prompt-Conditioned Slate Generation* [RecSys 2025].
- Hardesty, L. (2019, November 22). *The history of Amazon's recommendation algorithm.* Amazon Science.
- Google. (2025, May 20). *Google Search AI Mode update.* https://blog.google/products/search/google-search-ai-mode-update/
- The Browser Company. (n.d.). *Arc Max* and *Dia.* https://arc.net/max ; https://www.diabrowser.com/
- Weiser, M. (1991, September). The Computer for the 21st Century. *Scientific American, 265*(3) — calm/ubiquitous computing, invoked as foundational framing.
- Yocco, V. (2026). *Designing For Agentic AI: Practical UX Patterns for Control, Consent, and Accountability.* Smashing Magazine.

*End of foundation paper (synthesis edition).*

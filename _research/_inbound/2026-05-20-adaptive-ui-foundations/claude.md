# Adaptive Interfaces: A Foundation Paper

*A senior design-systems leader's survey of sentient design, generative UI, agentic UX, and what's actually shipped — written May 2026.*

---

## Preface — How to read this

This is a long-form analytical essay, not a reference document. It is meant to be read straight through, then mined later for citations. It is weighted to shipped reality; speculation is labeled inline with `*[speculative]*` or sequestered in a "Where this might be headed" subsection. It deliberately sits with tensions rather than resolving them prematurely, because the field is too young and the disagreements are too productive to flatten.

Three things to flag at the top:

1. **The "molten UX" phrase commonly attributed to Josh Clark could not be verified in any public Big Medium article, talk transcript, or podcast appearance reviewed for this paper.** The Sentient Design vocabulary owns *radically adaptive*, *thawing frozen formats*, and *call-and-response UI* — but not *molten UX*. If you have seen the phrase cited, it likely traces to the unreleased book or to a secondary source paraphrasing it. Treat with caution.
2. **The strongest empirical case for adaptive UIs lives in accessibility research that contemporary genUI marketing rarely cites.** Krzysztof Gajos's work at Harvard is the load-bearing evidence base for "adaptive UIs actually help users" — and most product teams reaching for that claim haven't read it.
3. **Vercel walked back its own coinage.** The "AI SDK RSC" package that introduced the term *generative UI* in March 2024 is now flagged "experimental" in Vercel's own documentation, with a migration guide pointing developers back to AI SDK UI for production. The term is louder in the discourse than it is in shipped engineering.

If you remember nothing else from this paper, remember that ordering of warnings.

---

## 1. Defining the territory

Six lineages converge on what is loosely called "adaptive UI" today. They use overlapping vocabulary, cite different authorities, optimize for different metrics, and frequently talk past each other. Naming them clearly is the first move.

### 1.1 Sentient Design (Josh Clark / Veronika Kindred / Big Medium)

Designer-facing, experience-led. Defined publicly in *Say Hello to Sentient Design* (Clark & Kindred, June 2024) as "the already-here future of intelligent interfaces: experiences that feel almost self-aware in their response to user needs," organized around two attributes — *aware* and *radically adaptive* — supported by collaborative, multimodal, continuous/ambient, and deferential characteristics.[^1]

The key move in this lineage is *scope*. Clark explicitly refuses to let "making stuff" (generation) define the practice. Generation is one of five "machine-learning superpowers" alongside recommendation, prediction, classification, and clustering. So Sentient Design is broader than generative UI (which it treats as one pattern under "intelligent canvas") and broader than personalization (one tactic for adaptation).[^1] The framing is "form, framework, and philosophy" — explicitly above the level of any single technique.

Key vocabulary to know: *radically adaptive*, *aware* and *deferential*, AI as *design material* in its *awkward adolescence*, the *Sentient Triangle* (grounded / interoperable / radically adaptive)[^2], *call-and-response UI* ("the LLM talks to the interface, not the user")[^3], *frozen formats* and *thawing* them[^4], *Data Whisperer* and *Pinocchio* patterns, *dream machines* (vs. answer machines)[^5], the designer as *creative director* setting rules and pattern libraries for AI to compose against[^6].

Where the lineage has sharpened over time: design systems. In 2024 essays they were largely implicit. By "Wiring Interface to Intent" (Clark, October 2025) they are explicitly the substrate on which adaptive UI runs: "Clean, context-based design systems are more important than ever, as is clear communication about what they do."[^3] The LLM "can only assemble what designers have already built and documented."

### 1.2 Generative UI (Vercel et al.)

Engineering-facing, narrower. The term was popularized by Vercel in *AI SDK 3.0 with Generative UI Support* (March 2024)[^7]. The canonical demo: a user asks "What is the weather in SF?", the model invokes a `get_city_weather` tool, a spinner streams in, then a `<Weather/>` component renders inline in the conversation. Vercel framed this as moving "beyond plaintext and markdown chatbots to give LLMs rich, component-based interfaces."

The shipped reality is narrower than the term suggests. By March 2025, Vercel's own AI SDK RSC documentation flagged the original generative-UI primitives as "experimental" and pointed developers to AI SDK UI's typed `message.parts` model for production[^8]. By May 2026, v0.app's homepage no longer leads with "generative UI" — the framing has shifted to "Agentic by default. Prompt. Build. Publish."[^9] The term is, increasingly, a 2024 artifact in active retreat by the company that coined it.

NN/g's broader academic definition by Moran and Gibbons (March 2024) — "a user interface that is dynamically generated in real time by artificial intelligence to provide an experience customized to fit the user's needs and context"[^10] — describes an aspiration. The shipped pattern is closer to "constrained component selection within a chat surface."

### 1.3 Personalization (Adobe, Sitecore, Optimizely, Salesforce, Dynamic Yield)

Older, originally rule-based, the incumbent. Every major platform now offers two flavors: rule-based ("if segment X then offer Y" — the marketer is the decision-maker, the system executes) and ML-driven ("here is the candidate set and the goal metric, you pick" — Adobe's Auto-Target / Automated Personalization runs Random Forest models retrained every 24 hours, with multi-armed bandits and Thompson Sampling fallback[^11]; Optimizely uses MABs and is roadmapping contextual bandits[^12]; Sitecore exposes "analytical models" inside a decision canvas[^13]).

The unit of personalization is remarkably narrow across all of them: an Offer slotted into an Experience inside an Activity (AEM's vocabulary, but the shape generalizes). What varies per user is hero/banner content, teaser images, recommendation strips, cross-sell modules, occasional layout swaps — almost nothing varies *structurally*. Nav doesn't restructure. IA doesn't change. Forms don't compose themselves. Fifteen years of production practice has refined fine-grained content swapping inside a fixed page skeleton — which is precisely what makes today's "generative UI" pitch feel both incremental and threatening to incumbents.

Where LLMs are entering the incumbent stack: the *authoring* layer, not the decisioning layer. Sitecore's Code Assistant turns natural-language prompts into JavaScript decision logic[^13]. Adobe Target ships an in-product AI Assistant and an MCP server exposing Target operations to Claude / Cursor / ChatGPT[^11]. Dynamic Yield's "Shopping Muse" is a conversational front-end on top of legacy decisioning[^14]. The model that *picks the variant* is still a Random Forest or a bandit. This is the opposite of what "AI-driven personalization" press usually implies.

### 1.4 Malleable software (Ink & Switch, Geoffrey Litt, Maggie Appleton, Andy Matuschak)

Research/philosophical. The lineage argues something structurally different from — and in tension with — the dominant generative-UI narrative. Generative UI is *system-generated*: the AI produces an interface in real time based on inferred user context. Malleable software argues software should be *user-authored*, with the AI as collaborator inside a medium the user controls.

Litt's hybrid model (March 2023) is direct manipulation in the inner loop, LLM as "local developer" in the outer loop, and "the user's reliance on the AI gently *decreases* over time as they become more comfortable in the medium."[^15] The Ink & Switch position essay *Malleable Software: Restoring User Agency in a World of Locked-Down Apps* (Litt, Horowitz, van Hardenberg, Matthews; June 2025) extends this to four properties — software ecosystem, anyone, adapting tools, minimal friction — and warns that "AI code generation alone does not address all the barriers to malleability."[^16] Without composable architectures and shared data, AI coding inside today's app stores is "a talented sous chef in a food court."

Appleton's *Squish Meets Structure* (2023) argues language models are "organic, opaque, unpredictable" and we keep wrapping them in conventions designed for predictability, mismatching expectations[^17]. Her recommendation: "tiny, sharp, specific tools with models" — decompose, expose, let users see and own the work. By 2025, Litt had publicly shifted from copilot enthusiasm to copilot critique, arguing "anyone serious about designing for AI should consider non-copilot form factors that more directly extend the human mind" — HUD-style interfaces (spellcheck-style red squigglies) over chatty assistants[^18].

The distinction matters: generative UI optimizes for *the user not having to think about the interface*; malleable software optimizes for *the user being able to reshape the interface*. One is convenience; the other is agency. They can coexist, but they imply different power structures, and senior leaders should not let them collapse into each other.

### 1.5 Adaptive interfaces (academic HCI — Krzysztof Gajos, Wobbrock, Findlater)

The academic root, with twenty years of empirical work, almost entirely uncited in current practitioner discourse. Gajos's SUPPLE work (2004 onward) framed automatic UI generation as constrained optimization — given an abstract specification and a model of the user's device and abilities, search over renderings to minimize estimated effort[^19]. By 2007–2008, Gajos, Wobbrock, and Weld had shown that SUPPLE-generated interfaces matched to a user's measured motor abilities significantly outperformed default interfaces for users with motor impairments — *and* those users *preferred* the adapted UI[^20][^21]. Preference and performance moved together, which is rare in adaptive-UI research.

The canonical Wobbrock et al. *Ability-Based Design* paper (TACCESS 2011, CACM 2018; cited 794+ times) articulates the design philosophy: design for ability rather than disability; let systems adapt to the person rather than asking the person to adapt to the system[^22][^23]. iOS VoiceOver gestures are a direct descendant.

Findlater & McGrenere's CHI 2004 study (456+ citations) is the cautionary anchor: *adaptable* (user-controlled) menus outperformed *adaptive* (system-controlled) ones on satisfaction, and many participants preferred the static baseline outright for spatial-memory reasons[^24]. Findlater & Gajos's 2009 *AI Magazine* survey is the field's accumulated humility: benefits are real but conditional on prediction accuracy, stability, and the cost-of-error model[^25].

### 1.6 Agentic UX (Nielsen Norman Group, Replit Agent, computer-use models)

The agent-does-the-work framing. NN/g's Sponheim (April 2026) defines an AI agent as "a system that pursues a goal by iteratively taking actions, evaluating progress, and deciding its own next steps."[^26] Gibbons & Moran (April 2026) argue agents *are becoming users* of digital interfaces — "a core assumption needs updating: 'user' is no longer synonymous with 'human.'" Some businesses (ad-supported, regulated, competitive-data holders) have legitimate reasons to *resist* agent access: "not all friction in an interface is a design failure."[^27]

Liu & Rosala's Qwen study (NN/g, May 2026, n=6) is the only original empirical agentic-UX study from NN/g this paper found. The findings are sharper than the literature acknowledges: 5 of 6 participants defaulted to traditional delivery apps over an integrated agent; perceived data-leak alarm at the moment of authorization ("I feel like my address was leaked"); pricing opacity (¥1.6 → ¥10.2 with no explanation); abandoned tasks when the agent hid decision-relevant data (baggage allowance)[^28].

### 1.7 Which framings are most useful for web and mobile work today

For a senior design-systems leader trying to make decisions in mid-2026, three framings carry the most weight:

- **Sentient Design** as the strategic vocabulary — because it is the only lineage that has done the work of giving designers language for the *full* surface area (recommendation + prediction + classification + clustering + generation), and because its insistence on *deferential* design is the right ethical posture.
- **Personalization-incumbent practice** as the engineering baseline — because the bandit-driven, slot-based, A/B-tested infrastructure that's already running at Adobe/Optimizely/Sitecore scale is what most organizations should compose with, not replace.
- **Ability-based design** as the empirical conscience — because it is the body of evidence most likely to keep teams honest about whether their adaptive UI actually helps anyone.

The other three lineages remain critical but are best treated as correctives. Generative UI gives engineering primitives but smaller scope than its name implies. Malleable software is the right long-term direction for *some* product categories (notes, end-user computation, creative tools) but is not yet a mass-market pattern. Agentic UX is moving fastest but has the thinnest empirical base.

---

## 2. Personalization vs. adaptation — a critical distinction

Pull these apart explicitly because the marketing copy doesn't.

**Personalization** is segment-driven. *User is in cohort X, show variant Y.* Slow, profile-based, deterministic in its branching even when the branching rule is learned. The cohort can be authored by a marketer (rule-based) or learned by a model (Adobe Auto-Target, Optimizely MABs, Netflix homepage rows), but the unit of variation is *which pre-built variant gets served*. The candidate set is closed. The design system is intact. The user's session is one observation among many that the model uses to refine its policy across the population.

**Adaptation** is context-driven. *User is doing Z right now.* Fast, contextual, often generative. The candidate is constructed (or selected from a much larger latent space) for *this* moment for *this* user. Granola's meeting templates change because the calendar event title says "user research" rather than "1-on-1." Linear's Triage Intelligence pulls a different set of suggestions because the workspace's "Additional Guidance" prompt steers it that way. Dia's Morning Brief composes from this morning's Slack, calendar, and inbox — not from a stored preference about what kind of brief you like.

The two failure modes are different.

Personalization fails *between* sessions. A one-time gift purchase poisons your recommendations for months. NN/g's Schade is direct about this: personalization "should not be used as a fix for a broken site," and any production personalization needs an explicit *escape hatch* — TikTok's "Not Interested," YouTube's history pause, NN/g's "View as…" pattern[^29]. Mature recommenders all expose a way for the user to override the model's inference, because the model *will* be wrong about people whose context just changed.

Adaptation fails *within* a session. The interface guesses wrong about what you're doing right now and surfaces the wrong tool, the wrong layout, the wrong content. The cost is immediate distraction and immediate trust erosion. The repair has to happen in seconds, not weeks.

Both can coexist in one experience — and increasingly do. Spotify's Home is personalization (Discover Weekly, Daily Mix, Release Radar are profile-driven). Spotify's AI DJ is adaptation (it reads your current listening session, time of day, mood signals from recent skips). Google's AI Mode "query fan-out" pattern[^30] is adaptation grafted onto fifteen years of personalized search results.

The cleanest signal that the two are different: the academic empirical literature says preference and performance often move *together* for ability-based personalization (where the cohort is "users with this measurable motor accuracy")[^20], but they often move *apart* for system-driven within-session adaptation (Findlater & McGrenere 2004 — users preferred the static menu)[^24]. Personalization rewards stability across time. Adaptation rewards responsiveness within time. Confusing them is the most common diagnostic error in the discourse.

---

## 3. The user experience of adaptive UI

What does it feel like? What do users notice, expect, distrust?

### 3.1 The trust and "creepiness" tension

The historical anchor is not Clippy, it is *Lumiere*. Eric Horvitz's UAI 1998 paper on Bayesian user modeling is more cautious than Clippy's launch behavior implied[^31]. Clippy's failure was a productization decision (always-visible animated agent) imposed on a probabilistic system that was modest about itself. Horvitz had already articulated, in the CHI 1999 *Principles of Mixed-Initiative User Interfaces*, the rule that would have prevented it: an agent should act only when *expected utility* of acting exceeds expected utility of inaction — and should always preserve user agency to reject the action cheaply[^32].

Luke Swartz's 2003 Stanford retrospective — the most-cited primary source on Clippy's failure — names the breakdown as a *consistency* failure: an agent's name, appearance, voice, and behavior must align with each other and with users' expectations[^33]. Clippy's friendly anthropomorphic visual triggered social-response expectations (per the Reeves & Nass *Media Equation* research it was built on) that its actual capabilities couldn't meet.

Both diagnoses are still operative. Clark's *Sparkles Are Fizzling* essay (September 2024) makes the same argument in 2024 vocabulary — sparkle/purple-gradient AI cliché is the new "always-visible animated agent," promising more capability than the underlying system can deliver, and now reading as the new badge for "beta"[^34]. Saarinen's "skepticism has to be part of the brief"[^35] and Clark's "we want to delegate decisions to AI, not abdicate them"[^36] are 2026 restatements of Horvitz's 1999 cost-of-being-wrong principle.

### 3.2 The mental-model cost

Findlater & McGrenere 2004 is still the reference experiment[^24]. Adaptive (system-controlled) menus underperformed adaptable (user-controlled) menus on satisfaction, and the static baseline was preferred by a meaningful subset of users who valued spatial stability. The cost is largely in the *perceptual* layer (spatial memory, surprise) rather than in the inference layer — Findlater et al.'s 2009 *Ephemeral Adaptation* showed that gradual onset of adapted items improves performance without harming spatial memory[^37]. The implication for genUI is clear and uncomfortable: *muscle memory is a feature, not a bug,* and surfaces that vary too aggressively will degrade for the population that uses them most.

Christopher Butler's *Consistency Is Primitive* (February 2026) takes the contrary position: consistency is "civilizational infancy," an artifact of manufacturing economics that AI infrastructure dissolves[^38]. NN/g's Moran is the direct counter: most users "cannot articulate what interface they need" — which is why genUI carries a *higher* design burden than vibe coding, not a lower one[^39]. The white-paper reader should not collapse this debate; it is genuinely live, and which side a team takes determines whether their product looks like Linear or like a bespoke-per-user surface that no one shares vocabulary about.

### 3.3 Disclosure, agency, and the user's sense of control

Three concrete patterns recur across mature implementations:

- **Visible thinking surfaces.** Linear's Triage Intelligence shows a thinking panel with a timer and a full reasoning trace; Vercel's AI SDK 4.2 added typed `reasoning` parts to messages[^40]; Comet exposes the agent sidebar; Dia shows reports with sources. Generative UI is making "what the model is doing" itself a UI element. Spinners no longer suffice — Yocco at Smashing argues sustained latency without rich progress information is the chief trust failure of agentic experiences[^41].
- **Cheap dismissal.** Horvitz's 1999 principle of "efficient invocation and dismissal" is now the determinant of perceived intelligence. Arc's hover-Shift previews are cheap to summon and cheap to ignore; Clippy's animated paperclip was expensive on both sides.
- **Side-by-side over in-line.** Anthropic Artifacts[^42], ChatGPT Canvas, Comet, v0's Design mode, Dia's Splits all converge on the same shape: chat on one side, generated/editable artifact on the other. The chat thread becomes the *log of intent*; the panel becomes the *artifact of work*. This is now the dominant shape for human-in-the-loop generation.

### 3.4 When users want adaptation vs. when they want predictability

The empirical cut is cleaner than the discourse suggests. Users want adaptation when (a) the cost of getting the interface right manually is high (accessibility, unfamiliar tasks, novel domains), (b) the consequences of the system being wrong are low (browsing, ambient surfaces, recommendations), and (c) the user has no strong prior model of what the surface should look like. Users want predictability when (a) they are doing something they have done before and have built muscle memory for (productivity tools, professional software), (b) the consequences of the system being wrong are high (regulated UIs, transactional flows), or (c) they share the surface with others and need a common reference (collaborative tools, brand-led marketing). Most products span both regimes; the design move is naming which mode the user is in and not changing the interface in the wrong one.

### 3.5 The empirical thinness should be named

NN/g's empirical base on agentic UX is thinner than the volume of articles suggests. Sponheim supplies a definition[^26]; Liu & Rosala supply one n=6 study[^28]; Moran's GenUI work draws on "hundreds of user-research sessions" but is not formally reported. The most concrete genUI finding is positive: chat-embedded checkboxes and buttons (Google AI Mode's hotel chips, Claude's `AskUserQuestion` widget) measurably reduce friction over text-only follow-ups (Perplexity's plain-text numbered lists)[^43]. Beyond that, the field is operating largely on demos and small qualitative studies. The Gajos accessibility evidence remains the cleanest empirical case for adaptive UI — and is almost never cited by current practitioners.

---

## 4. What problems does this actually solve

The hard, evidence-based section.

### 4.1 Accessibility — the strongest case

The Gajos / Wobbrock work is the load-bearing evidence base. Motor-impaired participants completed tasks significantly faster, made fewer errors, and reported preferring the adapted UI[^21]. The ability-based design philosophy is now embedded in iOS VoiceOver gestures and a generation of accessibility infrastructure[^23]. The empirical signal is robust and specific: when *abilities are measurable* (motor accuracy, vision, working memory) and the system *actually models them* before adapting, adaptive UI delivers — for the population that needs it most.

The corollary cuts the other way. Most "AI personalization" today is correlational — it learns what users tend to choose, not what they're *able* to do well. That is a different problem, with a different evidence base, and the genUI marketing case for "AI improves accessibility" is much weaker than the academic case for *ability-based design improves accessibility*. Senior leaders who want to make the inclusivity argument should cite Wobbrock and Gajos, not Vercel.

### 4.2 Discovery and reducing cognitive load for occasional/novice users

Recommendation-system practice has fifteen years of evidence that personalized discovery surfaces measurably improve engagement. Netflix's 2016 disclosure that 82% of browsing focus is on artwork during a ~90-second decision window, and that artwork variants per title are A/B-tested[^44], is the canonical proof. Spotify's Daily Mix clusters listener history into up to six daily-refreshed playlists[^45]; Discover Weekly remains the most-cited example of net-new value created by personalization. NN/g's Moran on chat-embedded form widgets reducing cognitive load in genUI conversations[^43] is the clearest 2026 finding in the same vein.

The pattern: the strongest discovery wins are for users who *don't yet know* what they want. Cold start is a first-class design problem (TikTok's interest picker, Spotify's editorial seeding, Amazon's 2014 reframe to predicting near-future behavior[^46]) — adaptive UIs that don't have an explicit "I don't know you yet" mode degrade for every new user, every cleared cookie, every shared device.

### 4.3 Onboarding and time-to-value

Genuine but conditional gains. Granola's adapt-to-meeting-title pattern is the cleanest example: users get useful structured notes from the first meeting because the system inferred what kind of meeting it was from the calendar event title[^47]. Linear's Triage Intelligence reduces the manual triage workload that would otherwise be a multi-week onboarding tax for a new PM joining a workspace[^48]. The trend is to *use the user's existing context* (calendar, workspace, browser tabs) rather than ask new users to fill in profile fields — which is a real shift from the personalization-incumbent paradigm.

### 4.4 Where it underperforms or backfires

- **Power users.** Findlater & McGrenere 2004 — many users prefer static menus[^24]. Saarinen's blunt rejection — "a chat interface is a very weak and generic form" and structured outputs are "a band-aid"[^35] — is a power-user voice arguing that the workbench beats the conversation for anyone who knows the domain.
- **Regulated UIs.** Colorado SB24-205 (operative February 2026) requires impact assessments, human-review rights, and discrimination-risk reporting whenever AI is a substantial factor in a "consequential decision" (employment, lending, housing, education, healthcare, insurance, legal)[^49]. Adaptive UI that varies the *path* a user takes through a regulated decision is a compliance-perimeter problem, not a UX one.
- **Brand-led marketing surfaces.** When the surface itself is the brand artifact, varying it per user erodes the consistency the brand is paying for. Butler's "civilizational infancy" thesis treats this as a temporary economic constraint[^38]; in shipping reality it remains a hard constraint and probably will for years.
- **Professional tools where consistency is a feature.** Linear's "workbench" framing[^35] is the right pattern for this class — keep the deterministic UI stable, layer AI on top with full auditability. Saarinen's *Output Isn't Design* (April 2026) — "the risk is mistaking generated form for solved problems"[^50] — reads as a direct rebuttal to the *designer-as-creative-director-of-AI-output* posture.

---

## 5. Ethics, dark patterns, manipulation

The strongest non-vague critique of adaptive UI today is structural and arrives in three layers.

### 5.1 The EU AI Act's manipulation prohibition is live

EU AI Act Article 5(1)(a)–(b) entered into force on 2 February 2025[^51]. It prohibits AI systems that "deploy subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques" with the objective or effect of "materially distorting the behaviour of a person or a group of persons by appreciably impairing their ability to make an informed decision," causing or reasonably likely to cause significant harm. Article 5(1)(b) extends this to exploitation of vulnerabilities tied to age, disability, or specific social/economic situation.

Recital 29 contains the load-bearing line for adaptive UI specifically: subliminal stimuli include cases "where they are aware of them, [but] can still be deceived or are not able to control or resist them" — and *intent is not required, effect is sufficient*[^52]. The first hard-law instrument that names adaptive AI manipulation as such has already taken effect. Adaptive UI that materially distorts behavior and causes significant harm is illegal in the EU regardless of whether the design team intended manipulation.

### 5.2 US state-level disclosure regimes are arriving in 2026

Three pressure points are on the books:

- **Colorado SB24-205** (signed May 2024, operative February 2026) mandates consumer disclosure for any AI system "intended to interact with consumers" and triggers impact assessments, human-review rights, and discrimination-risk reporting whenever AI is a substantial factor in a consequential decision[^49].
- **California SB 942** (signed September 2024, operative January 2026) requires latent provenance disclosure embedded in generative content from large providers (>1M monthly users in California), plus a public AI-detection tool. Civil penalty: $5,000 per violation per day[^53].
- **California AB 2013** (signed September 2024, compliance deadline January 2026, retroactive to systems released on or after January 2022) requires developers to publish a "high-level summary of the datasets" used in training[^54].

Together these form a real compliance perimeter. Design teams shipping adaptive UI by 2026 face disclosure, provenance, impact-assessment, and manipulation-prohibition obligations across the EU and at least three US states, with deceptive-trade-practice liability as the enforcement teeth. The "we'll figure out ethics later" posture has expired.

### 5.3 LLMs are *more* susceptible to choice-architecture manipulation than humans

This is the single most important empirical finding in this paper. Liu & He's November 2024 paper *The Decoy Dilemma in Online Medical Information Evaluation* tested whether LLMs exhibit human-style cognitive biases and found that the *decoy effect* — a classic choice-architecture manipulation — appears in LLM credibility judgments *more* prevalently than in human judgments across COVID-19 misinformation tasks[^55]. Newer, larger LLMs were more accurate in absolute terms but "more likely to give higher ratings for misinformation due to the presence of a more salient, decoy misinformation result."

This is a manipulation surface that classical dark-patterns research (Brignull lineage) does not cover. The model itself is the manipulation target, not the user. Adversarial *content arrangement* — placing a decoy in retrieved context — steers the LLM's judgment, which then shapes what the adaptive interface presents to the user. Senior leaders who think they've internalized dark-pattern risk by reading deceptive.design have not yet internalized this surface.

### 5.4 The Appleton epistemic critique

Maggie Appleton's *Expanding Dark Forest* talk (Causal Islands, April 2023; expanded through November 2024) supplies the strongest content-level critique[^56]: as adaptive interfaces train on model-generated data, "that tenuous link to the real world becomes completely divorced from it." She names the epistemic risk *human centipede epistemology* — models trained on model output progressively divorce from lived reality.

Butler's *Consistency Is Primitive* supplies the corollary[^38]: when each user inhabits a bespoke interface, shared reference points dissolve, and so does the ability to recognize manipulation collectively. Manipulation becomes invisible because there is no peer experience to compare to.

### 5.5 What designers can do

Concretely, four moves:

1. **Make the system prompt a design artifact.** Saarinen and Clark both treat the system prompt as a shared design/product/engineering specification — Linear's Triage Intelligence ships an "Additional Guidance" surface that exposes the prompt to workspace operators[^48]. The prompt is the rule set; rule sets need design review.
2. **Default to deferential UI.** Clark's "deferential" principle and Yocco's transparency patterns argue against sparkles, gradients, and animated agents that overpromise[^34][^41]. The visible thinking surface plus cheap dismissal is the right pattern.
3. **Audit for choice-architecture exposure.** Given Liu & He, any RAG-style adaptive UI should treat the retrieved-context layer as an attack surface. Decoy injection is not theoretical.
4. **Maintain an auditable variant log.** EU Article 5 enforces on *effect*, not *intent*. The only credible defense is the ability to demonstrate, post hoc, that the variants surfaced to a user did not materially distort their decisions. Design systems that don't keep variant logs aren't compliant — they just haven't been audited yet.

---

## 6. Industries and use cases

Strong fit, ambiguous fit, weak fit.

### 6.1 Strong fit

- **E-commerce.** The fifteen-year personalization story (Amazon's item-to-item collaborative filtering[^46], Adobe Target's bandit-driven Automated Personalization, Dynamic Yield's PDP modules) is the prototype. Adaptive layers on top — Granola-style context-aware product discovery, conversational shopping (Dynamic Yield's Shopping Muse, Google AI Mode's shopping with virtual try-on[^57]) — are net additive. The slot-based generation pattern fits e-commerce naturally because the surface is already merchandising, not authoritative reference.
- **Media.** Netflix and Spotify are the proof. Recommendation systems plus visible escape hatches (Not Interested, history pause) plus contextual signals (time of day, device, session) compose into the dominant adaptive-UI shape on the consumer web. Spotify's RecSys 2025 paper *Prompt-to-Slate: Diffusion Models for Prompt-Conditioned Slate Generation* is a strong signal that recommendation and generation are converging at the *layout* level, not just the content level[^58].
- **Productivity SaaS.** Linear, Notion, Granola, Dia. The "agent over a stable workbench" pattern — visible thinking, slot-based generation, optional invocation — is mature enough to ship. Saarinen's framing is the operating playbook.
- **Healthcare (specific surfaces only).** Patient-education content, accessibility surfaces, and ability-based adaptation for clinicians with measurable variation in workflow. Anything touching diagnosis, treatment, or consequential decisions sits in section 6.3.
- **Education.** Andy Matuschak's *How might we learn?* (May 2024) is the right framing[^59]: keep the learner's authentic creative project at the center, weave in just-in-time guidance and dynamic media exactly where cognition demands it. Adaptive UI as scaffolding for the actual work, not as chatbot tutor.
- **Fintech consumer apps.** Personalized financial summaries, transaction categorization, anomaly explanations. With strong escape hatches and no automated decisioning. The line is consequential decisions.

### 6.2 Ambiguous fit

- **Search.** Google AI Mode's query fan-out[^30] adapts at the layer of *what queries to issue*, not at the layer of *what UI to render*. The user-visible surface remains a familiar results page with an AI Overview pinned on top. Whether this is a meaningful shift or a Trojan horse for replacing the open web with summarized re-presentations is the live debate; senior leaders should not assume either side.
- **Browsers.** Arc's quiet retraction of *Browse for Me* and *Ask on Page* from the current Max page[^60], and The Browser Company's pivot to Dia (which markets as "a browser that works with you" rather than "an AI browser")[^61], is the empirical answer for now: aggressive adaptive UI in the browsing surface failed to find product-market fit; context-aware assistance with a conventional surface is the surviving pattern. Comet's CometJacking exposure[^62] is the cautionary tail.
- **Mobile platform shells.** Apple Intelligence is the cautionary case. Personal-context Siri, onscreen awareness, and cross-app intent — the headline 2024 promises — were still labeled "in development" 18 months later, drove a class-action lawsuit (*Landsheft v. Apple*, settled December 2025), and are now being rerouted through a multi-billion-dollar Google Gemini deal[^63]. The platform-shell surface is uniquely hard for adaptive UI because the cost-of-wrong is high and the user has the strongest possible muscle memory.

### 6.3 Weak fit

- **Regulated UIs.** Anywhere disclosure, audit trails, or anti-discrimination obligations apply: lending decisions, employment screening, insurance underwriting, healthcare diagnosis, government services. Section 5.2 covers the legal perimeter; the design corollary is that these surfaces should be deterministic, auditable, and the same for every user inside their cohort.
- **Brand-controlled marketing surfaces.** The brand is the artifact. Varying per user erodes the consistency the brand is paying for. This is a hard constraint, not a temporary one.
- **Professional tools where consistency is a feature.** Power-user productivity tools, technical authoring environments, code editors. Adaptive UI in these surfaces fights muscle memory, which is the user's most valuable asset.
- **Anything where shared reference matters.** Collaborative tools where users discuss the interface with each other; teaching tools where one user is showing another. Bespoke-per-user UI breaks the social fabric of the product.

---

## 7. Examples in production today

Concrete and cited. Not "Linear has AI features" but specifically what they ship and what users see.

### 7.1 Vercel v0 and AI SDK

What v0.app ships today is best described as *agentic application generation*, not generative UI in the original 2024 sense. The homepage leads with "Agentic by default — v0 plans, creates tasks, and connects to databases as it builds"[^9]. Categories: Apps and Games, Landing Pages, Components, Dashboards. Includes Design mode (visual controls, live preview), Design systems primitive, GitHub sync, one-click deploy, an iOS app. The flow is visible: Web → Plan → DB → API → Deploy → LLM. The term *generative UI* no longer appears.

The AI SDK underneath is the more durable contribution. AI SDK 4.2 (March 2025) replaced flat-text messages with typed `message.parts` (`text`, `source`, `reasoning`, `tool-invocation`, `file`)[^40]. MCP client support, image generation as `file` parts, tool-call streaming graduated from experimental to stable. The original RSC-based generative-UI primitives are flagged "experimental" with a migration guide pointing back to AI SDK UI[^8]. This is the engineering reality vs. marketing reality gap in concentrated form.

### 7.2 Linear AI

Specific shipped features as of May 2026[^64]:

- **Triage Intelligence** (September 2025) — duplicates, related issues, label and assignee suggestions in the triage view; thinking panel with timer; full reasoning trace; "Additional Guidance" workspace-level prompt[^48].
- **Linear Agent** (March 2026) — Cmd/Ctrl+J chat panel, `@Linear` mentions in comments/Slack/Teams.
- **Skills and Automations** (March 2026) — saved workflows, slash-command skills, triage automations.
- **Code Intelligence beta** (May 2026) — agent reads connected GitHub repos.
- **MCP support for the agent** (April 2026).
- **AI filter** (February 2026) — natural-language filter builder.
- **AI-generated release notes** (April 2026).
- **Mobile Agent Sessions** (March 2026) — visible reasoning, queued follow-ups.
- **Deeplink to AI Coding Tools** (February 2026) — launches Claude Code, Codex, Cursor, Copilot, Replit, Zed, Amp, Devin, Warp, Windsurf, Lovable.

The throughline matches Saarinen's "workbench" thesis[^35]: stable conventional UI, AI layered on top with full auditability.

### 7.3 Notion AI

Notion Agent ("anything you can do in Notion, your Notion Agent can do for you"); Custom Agents with trigger/schedule-based automations and credit budgeting ($10 per 1,000 credits, auto-pause when credits run out — a real budget surface for end users); AI Meeting Notes (no bot, transcribes computer audio); Enterprise Search (Slack, GitHub, Google Drive); Research Mode (multi-step reports); inline AI Blocks; database autofill and formula generation[^65].

### 7.4 Anthropic Artifacts

GA August 2024 across Free, Pro, Team plans plus iOS/Android. Output types: code snippets, flowcharts, SVG, websites, interactive dashboards. Side-by-side panel pattern. Free/Pro users can publish and remix; Team users share within Projects. By GA, "tens of millions of Artifacts" had been created since the June preview[^42].

### 7.5 ChatGPT Canvas

Launched October 2024. Side-by-side editor opens next to the chat. Inline editing plus a shortcut menu offering writing tools (suggest edits, change length, reading level, polish) and code tools (review, add logs, fix bugs, port to language). Originally GPT-4o; now spans GPT-4.x and GPT-5 tiers[^66].

### 7.6 Granola

"The AI notepad for people in back-to-back meetings"[^47]. The user types raw shorthand notes during the meeting; Granola transcribes computer audio (no bot joins the call). Meeting title/type drives template selection — customer discovery, 1-on-1, user interview, pitch, standup. Post-meeting "Enhanced notes" arrive structured into sections (Overview, Requirements, Budget & Timeline, Decision Criteria, Next Steps). "Ask Granola anything" chat queries the transcript.

The cleanest production example of slot-based adaptive UI: the shell is hand-designed, the section types are hand-defined, the section *content* is generated, the *which sections* is selected by inferring the meeting type from the calendar event title.

### 7.7 Arc Max and Dia

Arc Max ships 5 Second Previews (hover + Shift), Ask ChatGPT (type "ChatGPT" in command bar + Tab), Tidy Tab Titles, Tidy Downloads. Browse for Me and Ask on Page have been quietly removed from the current Max page[^60].

Dia (The Browser Company's successor) markets as "A browser that works with you" / "Dia reads between the tabs"[^61]. Notably does *not* use "AI browser." Shipped: Morning Brief, Proactive Suggestions, cross-tool answering ("Ask once. Dia digs into your full context, across GSuite, Slack, tabs, and more"), Reports, Live Work, Better Meetings, Splits, Organized Tabs, Profiles. macOS 14+ on M1+ only.

### 7.8 Apple Intelligence

Shipped to date[^63]:

- iOS 18.1 (October 2024): Writing Tools, redesigned Siri + Type to Siri, Smart Replies, Notification Summary, Photos Clean Up, Reduce Interruptions Focus.
- iOS 18.2 (December 2024): Image Playground, Genmoji, Image Wand, ChatGPT integration, Mail Categorization, Visual Intelligence (iPhone 16 only).
- iOS 18.4 (March 2025): Priority Notifications, Visual Intelligence to iPhone 15 Pro/16e, Vision Pro support.
- iOS 26.0 (September 2025): Live Translation, Foundation Models Framework, Workout Buddy.
- iOS 26.4 (March 2026): Playlist Playground.

Still labeled "in development" on apple.com as of May 2026: onscreen awareness, personal-context Siri, in-app and cross-app actions. The class-action *Landsheft v. Apple* (filed March 2025, settlement notice December 2025) and the Bloomberg-reported $1B/year Apple-Google Gemini deal (announced January 2026) are the empirical record of the gap between marketing and shipped reality.

### 7.9 Spotify and Netflix as the long-running adaptive UI baseline

Spotify shipped AI DJ in February 2023 — combining existing personalization with OpenAI tooling and a Sonantic-acquired voice model — as a card on Music Feed with spoken commentary between songs[^67]. Personalized surfaces named on Spotify's own recommendations explainer: Home feed, Search results, Release Radar, Discover Weekly, Genre/Mood/Decade Mixes, AI Playlist, Smart Shuffle, Autoplay, AI DJ[^68]. Discovery Mode (paid signal injection) is explicitly disclosed.

Netflix's homepage personalizes (1) which rows appear, (2) which titles in each row, (3) ordering within rows. The 2016 *Power of a Picture* disclosure remains the canonical proof that the *same content* shown *differently per user* (artwork variants tested per title) is a decade-old production practice[^44]. Treating that as a 2024 generative-UI invention misreads the inheritance.

### 7.10 Google AI Mode

Launched broadly in US May 2025 as a new tab in Search and the Google app search bar, powered by a custom Gemini 2.5[^57]. Architecturally distinctive: the *query fan-out* technique issues "multiple related searches concurrently across subtopics and multiple data sources." Subsequent additions: Deep Search, Search Live (camera-based via Project Astra), agentic actions via Project Mariner (Ticketmaster, StubHub, Resy, Vagaro), AI Mode shopping with virtual try-on and agentic Google Pay checkout, optional Gmail-context personalization, custom charts/graphs. Google's own framing acknowledges the failure mode: "we won't always get it right" / responses may "unintentionally appear to take on a persona."

### 7.11 Perplexity Comet

Chromium-based, Comet Assistant on the right side[^69]. Can summarize articles, compose emails, make purchases on behalf of the user. Launched macOS/Windows July 2025, Android November 2025, iOS March 2026. *CometJacking* — LayerX Security disclosed a prompt-injection technique potentially exfiltrating personal data to attacker-controlled servers in August 2025; Perplexity reportedly dismissed as "no security impact / not applicable." Generative UI delegations of authority to the model are running ahead of disclosure norms.

---

## 8. Where this might be headed *[speculative]*

Three plausible trajectories given current evidence, with clear labels.

### 8.1 What thoughtful practitioners predict

Clark's *What Happens When Agents Meet?* (February 2026) makes the most concrete prediction[^70]: "the unit of design is no longer only the agent or even the user; it's the population and the systems it affects." The next inflection is agent-population dynamics — multiple agents acting on a user's behalf, encountering each other, negotiating, generating cascades of unintended interaction. This is plausible from current trajectories (NN/g's "AI Agents as Users"[^27] is already there) and almost entirely undesigned for.

Saarinen's *Output Isn't Design* (April 2026) makes the contrarian prediction[^50]: "the hard part of design is rarely generating the form. It is understanding the problem well enough to know what and how something should exist at all. The risk is mistaking generated form for solved problems." If he is right, the next two years see a correction in which the designers and tools that survive are the ones that produce *fewer*, *more considered* surfaces — not more bespoke ones.

Both can be true. Adaptive UI continues to expand into ambient, recommendation, and contextual surfaces; the deliberate, designed surface becomes more valuable, not less, by contrast. The net effect on design systems: they become *more* important as the constraint set, not less.

### 8.2 What is plausible given current trajectories *[speculative]*

- *[speculative]* The slot-based generation pattern (Granola, Linear, Dia) becomes the dominant shape. Free-form per-user UI generation does not become a mass-market pattern in the next 2–3 years.
- *[speculative]* The malleable-software lineage (Litt, Matuschak) finds product-market fit in narrow vertical surfaces — notes, end-user computation, creative tools — but does not displace the application model broadly. The ladder from user to creator remains real but steep.
- *[speculative]* Recommendation-system practice and generative-UI practice converge at the *layout* level. Spotify's *Prompt-to-Slate*[^58] is a leading indicator; expect Adobe, Optimizely, and Sitecore to ship similar primitives by 2027.
- *[speculative]* Regulatory enforcement of EU Article 5 against a high-profile adaptive-UI deployment lands within 2–3 years, sharpens the design bar industry-wide, and pushes design systems to ship variant-logging infrastructure as a default.
- *[speculative]* The "AI [thing]" branding category reaches exhaustion. Dia's avoidance of "AI browser" is an early signal. By 2027 the strongest products lead with what the user does, not with the model under it.

### 8.3 What is hype *[speculative]*

- The framing that "every interface will be unique per user" elides the cost: for any product where users discuss, share, or teach the interface to each other, bespoke-per-user is destructive, not novel. This framing will not survive contact with the workplace.
- The framing that "design systems will become irrelevant" is the strongest piece of hype to ignore. Every credible voice in this paper — Clark, Saarinen, Moran, Wobbrock — locates design systems as *more* central, not less. The genuine shift is what they constrain.
- The framing that prompting is the future of human-computer interaction. Multiple lineages already disagree: Litt's "chat will never feel like driving a car"[^15], Saarinen's "very weak and generic form"[^35], Appleton's "lazy solution"[^71], Lee's "AI as creative collaborator"[^72] all argue from different directions that text prompting is a transitional pattern.

---

## 9. Brief design systems thread

Does a design system survive in this paradigm? Yes. The genuine question is what it constrains.

The traditional design system constrains *what gets built*: a closed catalog of components, tokens, and patterns that designers and engineers compose into pages. The adaptive-UI design system constrains *what gets generated*: the same catalog, plus the rule set the LLM uses to compose from it, plus the variant-logging infrastructure that makes the generation auditable.

Three concrete shifts:

1. **The system prompt becomes a design artifact.** Linear's "Additional Guidance" surface is the early production example[^48]. The prompt is the rule set; rule sets need design review, version control, and accessibility audit. This is the operational answer to Clark's "creative director" framing[^6] — the design system supplies the brief and the constraint set the LLM composes against.
2. **Component metadata grows.** Beyond visual specification, components need machine-readable descriptions of *when to render this*, *what context this requires*, *what alternatives this has*. Clark's *Wiring Interface to Intent* is explicit: "Constrain the outputs, map them to intents, and let the LLM handle the translation"[^3]. A design system without intent metadata cannot participate in adaptive UI generation.
3. **Variant logging becomes infrastructure.** EU Article 5 enforces on effect, not intent. The only credible defense is the ability to demonstrate which variants were surfaced to which user and why. Design systems that don't keep variant logs aren't compliant; they just haven't been audited.

What "consistency" means in this paradigm shifts from *every user sees the same surface* to *every user can predict and trust the surface they see*. The components stay consistent. The compositions vary, within rules the design system enforces. Muscle memory gets located one level up — at the level of *the kinds of things that can happen*, not at the pixel level. This is closer to the affordance vocabulary of physical product design than to the screen-level consistency of pre-AI digital design.

The implementation work — component APIs, intent metadata, variant logging, compliance instrumentation — belongs in the companion paper. Conceptually, the design system not only survives but becomes the load-bearing constraint that keeps adaptive UI from collapsing into chaos. Clark, Saarinen, Wobbrock, and Moran agree on this even when they disagree on everything else.

---

## Open questions

1. **Is "personalization" recoverable as a term, or has it been so overloaded that it now actively obscures?** Forrester's Jessica Liu has been arguing since April 2025 that the word needs qualifiers (program / capability / tactic / moment) before it means anything[^73]. NN/g still uses it broadly. The Sentient Design lineage folds it in as one tactic. The personalization-incumbent vendors use it for both rule-based and ML-driven systems indiscriminately. I do not have a defensible answer for whether to keep using the word or replace it; for this paper I have used it narrowly (segment-driven, profile-based) and used *adaptation* for context-driven within-session behavior. Whether the field consolidates around that distinction is unresolved.

2. **What does *consistency* mean operationally when surfaces vary?** Butler argues consistency is "civilizational infancy"; Moran argues users cannot articulate their interface and need conventions; Clark argues design systems are more important than ever. All three may be right at different time horizons (Moran in the next 2 years, Clark in the next 5, Butler at 10+), but I cannot resolve the disagreement from public evidence and the practical guidance differs sharply by which side a leader lands on.

3. **How much of the genuine adaptive-UI value is captured by accessibility specifically?** Gajos's evidence is the strongest in the field. If the empirical center of the case is ability-based design, then much of the surrounding genUI marketing is overpromising on weaker evidence. I cannot resolve whether the broader adaptive-UI thesis has comparably strong evidence somewhere I missed, or whether accessibility is genuinely doing most of the load-bearing work.

4. **What is the right governance model for variant logging?** EU Article 5 enforces on effect. The technical infrastructure to log every adaptive variant served to every user is real engineering work. I have not surfaced any vendor or industry-body proposal for what good variant-logging looks like, who should hold the logs, who should be able to audit them, or how long they should be retained. This is a major open question and possibly its own paper.

5. **Is Saarinen's "workbench" position generalizable, or specific to professional tools?** Linear is a productivity tool with power users. Saarinen's framing reads as universal but his evidence is narrow. The same logic applied to consumer surfaces would either reverse (because consumer users have less domain expertise to apply to a workbench) or hold (because the underlying claim about chat being "weak and generic" is medium-independent). I do not have evidence either way.

6. **How quickly does the malleable-software lineage move from research to product?** The Ink & Switch / Litt / Matuschak position essays are unusually substantive for research output, but the production examples remain narrow. Whether this lineage produces a mass-market product in the next 3 years, finds vertical product-market fit only, or remains primarily research is unresolved.

---

## What I should read next — ranked top 10

1. **Wobbrock, Kane, Gajos, Harada & Froehlich (2011), *Ability-Based Design*** (TACCESS) and its CACM 2018 revisit. The empirical foundation. Read this first if you want a defensible accessibility position.[^22][^23]
2. **Clark & Kindred, *Say Hello to Sentient Design*** (Big Medium, June 2024). The clearest single piece of writing in the lineage; defines the territory.[^1]
3. **Saarinen, *Design for the AI Age*** (Linear, April 2025). The strongest counter-position to chat-as-default; required reading for anyone who'll defend a workbench-shaped product.[^35]
4. **Horvitz, *Principles of Mixed-Initiative User Interfaces*** (CHI 1999). The cost-of-being-wrong framework still operates underneath every Copilot decision and every Copilot failure.[^32]
5. **Moran & Gibbons, *Generative UI and Outcome-Oriented Design*** (NN/g, March 2024) and Moran, *GenUI vs. Vibe Coding* (March 2026). NN/g's most useful definitional pieces.[^10][^39]
6. **Litt, *Malleable software in the age of LLMs*** (March 2023) and the Ink & Switch *Malleable Software* essay (June 2025). The clearest articulation of the user-authorship counter-lineage.[^15][^16]
7. **Findlater & Gajos, *Design Space and Evaluation Challenges of Adaptive Graphical User Interfaces*** (*AI Magazine* 2009). The field's accumulated humility, and the most useful single survey.[^25]
8. **Clark, *Wiring Interface to Intent*** (Big Medium, October 2025). The clearest statement of where design systems sit in the adaptive-UI stack.[^3]
9. **Liu & He, *The Decoy Dilemma in Online Medical Information Evaluation*** (arXiv, November 2024). The single most important empirical finding on adaptive-UI manipulation surface.[^55]
10. **Bret Victor, *Magic Ink*** (2006). Two decades old, and predicted today's inference hierarchy with more clarity than most contemporary writing.[^74]

---

## What surprised me

Eight findings that genuinely shifted my view:

1. **The "molten UX" attribution does not check out.** I expected to find Clark using the phrase as a signature term across his Big Medium catalog. He doesn't. He owns *radically adaptive* and *thawing frozen formats*, not *molten UX*. If you've been citing it as Clark's, double-check the original source.

2. **Vercel walked back its own coinage.** AI SDK RSC — the package that introduced "generative UI" as a developer term in March 2024 — is now flagged "experimental" in Vercel's own docs, with an explicit migration guide pointing to AI SDK UI for production[^8]. v0.app's homepage no longer uses the term[^9]. The phrase is louder in discourse than in shipped engineering.

3. **Personalization incumbents are more sophisticated than the "personalization vs. adaptation" framing implies.** Adobe Target's Automated Personalization runs Random Forests retrained every 24 hours with multi-armed bandits and Thompson Sampling fallback[^11]. Optimizely uses MABs with contextual bandits roadmapped[^12]. This is more statistically sophisticated than most "AI-powered" startups in the adaptive-UI space currently ship — and the incumbents are now grafting LLMs onto the *authoring* layer, not the decisioning layer.

4. **The Gajos accessibility evidence is the strongest empirical case for adaptive UI — and it's almost never cited in current generative-UI discourse.** This was the most striking gap. Practitioners advocating genUI for inclusivity rarely cite the work that actually proves adaptive UIs *can* improve outcomes for the population that needs them most[^20][^21][^22].

5. **Findlater & McGrenere 2004 shows users often *prefer* the static baseline.** This contradicts the assumption baked into contemporary genUI marketing that personalization is inherently better[^24]. Spatial memory is a feature, not a bug.

6. **LLMs are *more* susceptible to choice-architecture manipulation than humans.** Liu & He's decoy-effect finding (November 2024) is the single most important empirical claim in this paper, and it sits outside the dark-pattern lineage most designers have read[^55]. Adversarial content arrangement steers the model itself, which then shapes what the adaptive interface presents.

7. **Regulatory teeth are arriving faster than industry framing acknowledges.** EU AI Act Article 5 was *live* by February 2025; Colorado, California SB 942, California AB 2013 all become operative January–February 2026[^51][^49][^53][^54]. The "we'll figure out ethics later" stance has expired.

8. **Saarinen's *Output Isn't Design* (April 2026) reads as a direct rebuttal to Clark's *When Interfaces Design Themselves* (September 2025).** He doesn't name Clark, but the rebuttal is unmistakable: "the risk is mistaking generated form for solved problems"[^50]. The two most-cited designer-facing voices in this lineage are publicly disagreeing about the central thesis. A senior leader who collapses them into a unified "adaptive UI" position is missing the live debate.

---

## Bibliography

[^1]: Clark, J., & Kindred, V. (2024, June 12). *Say Hello to Sentient Design.* Big Medium. https://bigmedium.com/ideas/hello-sentient-design.html

[^2]: Clark, J. (2024, July 28). *The Shape of Sentient Design.* Big Medium. https://bigmedium.com/ideas/shape-of-sentient-design.html

[^3]: Clark, J. (2025, October 2). *Wiring Interface to Intent.* Big Medium. https://bigmedium.com/ideas/wiring-interface-to-intent.html

[^4]: Clark, J. (2024, September 27). *Data Whisperers, Pinocchios, and Sentient Design.* Big Medium. https://bigmedium.com/ideas/data-whisperer-pinocchio-sentient-design.html

[^5]: Clark, J. (2024, May 22). *Sentient Design: AI and the Next Chapter of UX* [Talk]. Friends of Figma Miami. https://bigmedium.com/speaking/sentient-design-josh-clark-talk.html

[^6]: Clark, J., & Kindred, V. (2025, September 30). *When Interfaces Design Themselves.* Big Medium. https://bigmedium.com/ideas/when-interfaces-draw-themselves.html

[^7]: Vercel. (2024, March 1). *AI SDK 3.0 with Generative UI Support.* https://vercel.com/blog/ai-sdk-3-generative-ui

[^8]: Vercel. (2025–2026). *AI SDK RSC — Generative UI State* [Documentation]. https://ai-sdk.dev/docs/ai-sdk-rsc/generative-ui-state

[^9]: Vercel. (2026). *v0.app* [Product homepage]. https://v0.app/

[^10]: Moran, K., & Gibbons, S. (2024, March 22). *Generative UI and Outcome-Oriented Design.* Nielsen Norman Group. https://www.nngroup.com/articles/generative-ui/

[^11]: Adobe. (n.d.). *Adobe Target — Automated Personalization activities* [Documentation]. https://experienceleague.adobe.com/en/docs/target/using/activities/automated-personalization/automated-personalization

[^12]: Optimizely. (n.d.). *Personalization using AI and experimentation.* https://www.optimizely.com/products/personalization/

[^13]: Sitecore. (n.d.). *Sitecore Personalize* [Product documentation]. https://doc.sitecore.com/personalize/en/users/sitecore-personalize/index-en.html

[^14]: Dynamic Yield. (n.d.). *Experience OS.* https://www.dynamicyield.com/

[^15]: Litt, G. (2023, March 25). *Malleable software in the age of LLMs.* https://www.geoffreylitt.com/2023/03/25/llm-end-user-programming

[^16]: Litt, G., Horowitz, J., van Hardenberg, P., & Matthews, T. (2025, June). *Malleable Software: Restoring User Agency in a World of Locked-Down Apps.* Ink & Switch. https://www.inkandswitch.com/essay/malleable-software/

[^17]: Appleton, M. (2023). *Squish Meets Structure: Designing with Language Models* [Talk + transcript]. Smashing Conference. https://maggieappleton.com/squish-structure

[^18]: Litt, G. (2025, July 27). *Enough AI copilots! We need AI HUDs.* https://geoffreylitt.com/2025/07/27/enough-ai-copilots-we-need-ai-huds

[^19]: Gajos, K. Z., & Weld, D. S. (2004). SUPPLE: Automatically Generating User Interfaces. *Proceedings of IUI '04.* https://doi.org/10.1145/964442.964461

[^20]: Gajos, K. Z., Wobbrock, J. O., & Weld, D. S. (2007). Automatically generating user interfaces adapted to users' motor and vision capabilities. *Proceedings of UIST '07.* https://doi.org/10.1145/1294211.1294253

[^21]: Gajos, K. Z., Wobbrock, J. O., & Weld, D. S. (2008). Improving the performance of motor-impaired users with automatically-generated, ability-based interfaces. *Proceedings of CHI '08.* https://doi.org/10.1145/1357054.1357250

[^22]: Wobbrock, J. O., Kane, S. K., Gajos, K. Z., Harada, S., & Froehlich, J. (2011). Ability-Based Design: Concept, principles and examples. *ACM TACCESS, 3*(3). https://doi.org/10.1145/1952383.1952384

[^23]: Wobbrock, J. O., Gajos, K. Z., Kane, S. K., & Vanderheiden, G. C. (2018). Ability-based design. *Communications of the ACM, 61*(6). https://doi.org/10.1145/3148051

[^24]: Findlater, L., & McGrenere, J. (2004). A comparison of static, adaptive, and adaptable menus. *Proceedings of CHI '04.* https://doi.org/10.1145/985692.985704

[^25]: Findlater, L., & Gajos, K. Z. (2009). Design space and evaluation challenges of adaptive graphical user interfaces. *AI Magazine, 30*(4). https://ojs.aaai.org/index.php/aimagazine/article/view/2268

[^26]: Sponheim, C. (2026, April 3). *A Concrete Definition of an AI Agent.* Nielsen Norman Group. https://www.nngroup.com/articles/definition-ai-agent/

[^27]: Gibbons, S., & Moran, K. (2026, April 10). *AI Agents as Users.* Nielsen Norman Group. https://www.nngroup.com/articles/ai-agents-as-users/

[^28]: Liu, F., & Rosala, M. (2026, May 8). *Designing AI Agents: 4 Lessons from China's Qwen Agent.* Nielsen Norman Group. https://www.nngroup.com/articles/designing-ai-agents/

[^29]: Schade, A. (2016, July 10). *Customization vs. Personalization in the User Experience.* Nielsen Norman Group. https://www.nngroup.com/articles/customization-personalization/

[^30]: Google. (2025, March 5). *AI Mode in Search: A new way to explore.* https://blog.google/products/search/ai-mode-search/

[^31]: Horvitz, E., Breese, J., Heckerman, D., Hovel, D., & Rommelse, K. (1998). The Lumiere project: Bayesian user modeling for inferring the goals and needs of software users. *Proceedings of UAI '98.* https://arxiv.org/abs/1301.7385

[^32]: Horvitz, E. (1999). Principles of mixed-initiative user interfaces. *Proceedings of CHI '99.* https://doi.org/10.1145/302979.303030

[^33]: Swartz, L. (2003). *Why People Hate the Paperclip: Labels, Appearance, Behavior, and Social Responses to User Interface Agents* [Honors thesis]. Stanford University.

[^34]: Clark, J. (2024, September 28). *Your Sparkles Are Fizzling.* Big Medium. https://bigmedium.com/ideas/your-sparkles-are-fizzling.html

[^35]: Saarinen, K. (2025, April 7). *Design for the AI Age.* Linear. https://linear.app/now/design-for-the-ai-age

[^36]: Clark, J., & Kindred, V. (2026, April 11). *Sentient Design* [Podcast]. Commit & Push, hosted by Damien Filiatrault. https://bigmedium.com/speaking/commit-push-josh-clark-veronika-kindred.html

[^37]: Findlater, L., Moffatt, K., McGrenere, J., & Dawson, J. (2009). Ephemeral adaptation: The use of gradual onset to improve menu selection performance. *Proceedings of CHI '09.* https://doi.org/10.1145/1518701.1518956

[^38]: Butler, C. (2026, February 19). *Consistency Is Primitive.* https://chrbutler.com/consistency-is-primitive

[^39]: Moran, K. (2026, March 27). *GenUI vs. Vibe Coding: Who's Designing?* Nielsen Norman Group. https://www.nngroup.com/articles/genui-vs-vibe/

[^40]: Vercel. (2025, March 21). *AI SDK 4.2.* https://vercel.com/blog/ai-sdk-4-2

[^41]: Yocco, V. (2026, Feb–May). *Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability.* Smashing Magazine. https://www.smashingmagazine.com/

[^42]: Anthropic. (2024, August 27). *Artifacts are now generally available.* https://www.anthropic.com/news/artifacts

[^43]: Moran, K. (2026, March 6). *The Most Exciting Development in GenUI: Buttons and Checkboxes.* Nielsen Norman Group. https://www.nngroup.com/articles/genui-buttons-and-checkboxes/

[^44]: Nelson, N. (2016, May 3). *The Power of a Picture.* Netflix. https://about.netflix.com/en/news/the-power-of-a-picture

[^45]: Spotify Newsroom. (2018, May 18). *How Your Daily Mix 'Just Gets You.'* https://newsroom.spotify.com/2018-05-18/how-your-daily-mix-just-gets-you/

[^46]: Hardesty, L. (2019, November 22). *The history of Amazon's recommendation algorithm.* Amazon Science. https://www.amazon.science/the-history-of-amazons-recommendation-algorithm

[^47]: Granola. (n.d.). *Granola — The AI notepad for people in back-to-back meetings.* https://www.granola.ai/

[^48]: Linear. (2025, September 3). *How we built Triage Intelligence.* https://linear.app/blog/how-we-built-triage-intelligence

[^49]: Colorado General Assembly. (2024, May 17). *Senate Bill 24-205 — Consumer Protections for Artificial Intelligence.* https://leg.colorado.gov/bills/sb24-205

[^50]: Saarinen, K. (2026, April 17). *Output Isn't Design.* Linear. https://linear.app/now/output-isn-t-design

[^51]: European Union. (2024). *Artificial Intelligence Act, Article 5* [Effective February 2, 2025]. https://artificialintelligenceact.eu/article/5/

[^52]: European Union. (2024). *Artificial Intelligence Act, Recital 29.* https://artificialintelligenceact.eu/recital/29/

[^53]: California Legislature. (2024, September 19). *Senate Bill 942 — California AI Transparency Act.* https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240SB942

[^54]: California Legislature. (2024, September 28). *Assembly Bill 2013 — Generative AI: Training Data Transparency.* https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2013

[^55]: Liu, J., & He, J. (2024, November 23). *The Decoy Dilemma in Online Medical Information Evaluation.* arXiv. https://arxiv.org/abs/2411.15396

[^56]: Appleton, M. (2023, April; expanded 2024). *The Expanding Dark Forest and Generative AI* [Talk + transcript]. Causal Islands. https://maggieappleton.com/forest-talk

[^57]: Google. (2025, May 20). *Google Search AI Mode update.* https://blog.google/products/search/google-search-ai-mode-update/

[^58]: Spotify Research. (2025, September 9). *Prompt-to-Slate: Diffusion Models for Prompt-Conditioned Slate Generation* [RecSys 2025]. https://research.atspotify.com/publications/

[^59]: Matuschak, A. (2024, May 8). *How might we learn?* [Talk + essay]. UCSD Design@Large. https://andymatuschak.org/hmwl

[^60]: The Browser Company. (n.d.). *Arc Max.* https://arc.net/max

[^61]: The Browser Company. (n.d.). *Dia.* https://www.diabrowser.com/

[^62]: LayerX Security. (2025, August). *CometJacking* [Disclosure]. Reported via secondary press; primary disclosure URL not captured.

[^63]: Apple. (n.d.). *Apple Intelligence* [Product page]. https://www.apple.com/apple-intelligence/

[^64]: Linear. (2026). *Changelog.* https://linear.app/changelog

[^65]: Notion. (n.d.). *Notion AI.* https://www.notion.com/product/ai

[^66]: OpenAI. (2024, October 3). *Introducing Canvas.* (Primary URL not retrievable in research; details triangulated from secondary sources.)

[^67]: Spotify Newsroom. (2023, February 22). *Spotify debuts a new AI DJ, right in your pocket.* https://newsroom.spotify.com/2023-02-22/spotify-debuts-a-new-ai-dj-right-in-your-pocket/

[^68]: Spotify. (n.d.). *Understanding recommendations.* https://www.spotify.com/safetyandprivacy/understanding-recommendations

[^69]: Wikipedia. (2026). *Comet (web browser).* https://en.wikipedia.org/wiki/Comet_(web_browser)

[^70]: Clark, J. (2026, February 4). *What Happens When Agents Meet?* Big Medium. https://bigmedium.com/ideas/what-happens-when-agents-meet.html

[^71]: Appleton, M. (2023). *Language Model Sketchbook, or Why I Hate Chatbots.* https://maggieappleton.com/lm-sketchbook

[^72]: Lee, L. (2021, November 16). *AI as a creative collaborator.* https://thesephist.com/posts/ai-collaborator/

[^73]: Liu, J. (2025, April 29 / October 2 / November 7). *Personalization* [Blog series]. Forrester. https://www.forrester.com/blogs/category/personalization/

[^74]: Victor, B. (2006). *Magic Ink: Information Software and the Graphical Interface.* https://worrydream.com/MagicInk/

### Additional sources cited or consulted

- Clark, J., & Kindred, V. (2025, March 9). *Sentient Design: AI and Radically Adaptive Interfaces* [SXSW talk transcript]. https://bigmedium.com/speaking/sentient-design-sxsw.html
- Clark, J., & Kindred, V. (2025, June 26). *Josh Clark and Veronika Kindred* [Podcast]. Design Better Podcast. https://designbetterpodcast.com/p/josh-clark-and-veronika-kindred
- Clark, J. (2026, April 10). *Look Up from Your Tools: AI for Product over Production.* Big Medium. https://bigmedium.com/ideas/look-up-from-your-tools.html
- Saarinen, K. (2025, December 19). *Design Is More Than Code.* Linear. https://linear.app/now/design-is-more-than-code
- Butler, C. (2025, June 13). *The Best Interfaces We Never Built.* https://chrbutler.com/the-best-interfaces-we-never-built
- Butler, C. (2026, March 31). *Craft Is Untouchable.* https://chrbutler.com/craft-is-untouchable
- Lee, L. (2022, January 2). *Notational Intelligence.* https://thesephist.com/posts/notation/
- Matuschak, A. (2026, March 3). *Apps and programming: two accidental tyrannies* [MIT HCI Seminar]. https://andymatuschak.org/tat
- Appleton, M. (2024, in progress). *A Future of Home-Cooked Software and Barefoot Developers.* https://maggieappleton.com/home-cooked-software
- Norman, D. (2023). *Design for a Better World: Meaningful, Sustainable, Humanity Centered.* MIT Press.
- Nielsen, J. (2023, June 18). *AI: First New UI Paradigm in 60 Years.* Nielsen Norman Group. https://www.nngroup.com/articles/ai-paradigm/
- Pariser, E. (2011, March). *Beware online "filter bubbles"* [TED Talk]. https://www.ted.com/talks/eli_pariser_beware_online_filter_bubbles
- Schade, A. (2016, October 2). *6 Tips for Successful Personalization.* Nielsen Norman Group. https://www.nngroup.com/articles/personalization/
- Vercel. (2024, March 1). *AI SDK 3.0.* https://vercel.com/blog/ai-sdk-3-generative-ui
- TikTok Newsroom. (2020, June 18). *How TikTok recommends videos #ForYou.* https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- Goodrow, C. (2021, September 15). *On YouTube's recommendation system.* YouTube Blog. https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
- Spotify Engineering. (2021, December 2). *How Spotify Uses ML to Create the Future of Personalization.* https://engineering.atspotify.com/2021/12/how-spotify-uses-ml-to-create-the-future-of-personalization/
- Weiser, M. (1991, September). The Computer for the 21st Century. *Scientific American, 265*(3).
- Weiser, M., & Brown, J. S. (1996). Designing Calm Technology. *PowerGrid Journal, 1.01.* https://calmtech.com/papers/designing-calm-technology.html
- Victor, B. (2011, November 8). *A Brief Rant on the Future of Interaction Design.* https://worrydream.com/ABriefRantOnTheFutureOfInteractionDesign/
- Lim, B. Y., Dey, A. K., & Avrahami, D. (2009). Why and why not explanations improve the intelligibility of context-aware intelligent systems. *Proceedings of CHI '09.* https://doi.org/10.1145/1518701.1519023
- Vaithilingam, P., Glassman, E. L., Inala, J. P., et al. (2024). DynaVis: Dynamically Synthesized UI Widgets for Visualization Editing. *Proceedings of CHI '24.* https://doi.org/10.1145/3613904.3642639
- Feng, K. J. K., Liao, Q. V., Xiao, Z., et al. (2025). Canvil: Designerly Adaptation for LLM-Powered User Experiences. *Proceedings of CHI '25.* https://doi.org/10.1145/3706598.3713139

---

*End of paper.*


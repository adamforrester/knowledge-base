# The Adaptive Interfaces Opportunity

*A leadership brief for VML — May 2026*

---

## The short version

The way customers interact with brands online is starting to bend in a way that affects every commerce and experience client in our book. Interfaces are becoming **adaptive** — composing themselves around the customer in the moment, rather than serving the same page to everyone in a segment. And customers are increasingly arriving at our clients' products through AI agents acting on their behalf, not through search or direct navigation.

This is not the next "personalization 2.0" buzz. The infrastructure is shipping, the production examples are real, and the early commerce data is striking. Adobe's 2025 holiday-season analysis showed retail traffic from AI sources (ChatGPT, Claude, Perplexity, Gemini) up roughly **693% year-over-year**, with those AI-referred shoppers converting **31% higher** than traditional channels. The volume is small today. The trajectory is the point.

VML is well-positioned to lead here, but the window to define how we lead is open now and will be closing inside 12 months as agency competitors catch up. This brief lays out what's actually happening, what it means for our clients, where the real opportunities sit, what it would take to capitalize, and what we'd recommend doing next.

---

## What "adaptive interfaces" actually means

The traditional design model is: design a screen, ship it, every user gets the same screen. Personalization (Adobe Target, Sitecore, Optimizely) added a layer on top: swap the hero image and the promo block based on which cohort the user is in.

Adaptive interfaces go further. The interface itself — what shows up, where it sits, what it focuses on — adapts to the user's *current context* rather than their pre-built profile. A few examples already in market:

- **Granola** (AI notepad for meetings) reads your calendar event, infers the meeting type, and produces a structured note template that matches — research interview, client check-in, board prep all get different scaffolding.
- **Linear's Triage Intelligence** watches what your team triages and surfaces duplicates, related issues, and a visible reasoning trace as you work.
- **Spotify's Daily Mix and Netflix's homepage** have done this for a decade, varying not just content but layout. They're the proof that the pattern works at consumer scale.
- **Anthropic's Artifacts and ChatGPT's Canvas** split the surface into conversation-plus-artifact, where the artifact (a doc, a chart, an app) is composed on demand from what you ask.

The technical pattern that ships most often is more modest than the demos suggest: a **fixed shell with adaptive slots inside it**. The brand surface stays consistent; what fills it varies. That matters because it means this is buildable on top of design systems clients already have — not a rip-and-replace.

---

## Why this matters to our clients now

Three forces converging at once:

**Commerce is shifting upstream.** Customers are starting to reach retailers through AI agents that compare options and recommend products, rather than through Google. The Adobe holiday data is the early signal — small volume, large trajectory. Within 18 months, "is our product legible to the agent recommending it?" becomes a real question for every commerce client we have.

**Personalization gets a serious upgrade.** McKinsey's research puts well-executed AI personalization at **10–15% revenue uplift typical, up to 25% best-case**. Documented case studies show 40% conversion improvements at retailers like Wayfair. The technology has moved from rules-based ("if cohort then offer") to context-driven ("user is doing this right now") — and the second is meaningfully better, but it requires real infrastructure.

**Risk has matured too.** The Personalization-Privacy Paradox is now documented in dozens of empirical studies — over-personalize without trust, and customers feel surveilled and disengage. The EU AI Act's manipulation prohibition is live (since February 2025), with enforcement on *effect*, not intent. State-level US disclosure laws (Colorado, California) are operative as of early 2026. Clients that move into adaptive work without governance get exposed.

The window for thoughtful early movement is open. Clients want guidance from partners who have a defensible position, not just enthusiasm.

---

## Where the real opportunities sit

Five categories of work, ordered by immediate viability for our portfolio:

**1. Adaptive personalization layered on existing CMS infrastructure.** Almost all our commerce and content clients run AEM, Sitecore, or Optimizely. These platforms have shipped LLM-aware authoring and decisioning layers in the last year. Most clients haven't activated them. The work: connect their existing personalization infrastructure to context-driven adaptation, with our design systems practice making sure the variable surfaces still feel branded. Low risk, immediate evidence base, scopable in weeks.

**2. AI-aware design systems.** Most client design systems can't support adaptive work as-built. They're catalogs of finished components rather than systems of composable primitives with semantic descriptions a model can reason over. Updating them — semantic component contracts, intent metadata, variant logging for compliance — is genuinely new work, and **it's exactly where our DS practice is strongest**. Few agency competitors can do this at scale. This is the highest-leverage capability investment we could make.

**3. Agentic commerce readiness.** Making client products legible to AI agents that increasingly act as customers' proxies. Structured product data, machine-readable inventory, semantic content, agent-friendly APIs. Less glamorous than generative UI, but every commerce client will need it within the year, and we can deliver it inside SOWs that are already in motion.

**4. Adaptive accessibility experiences.** The strongest-evidenced use case for adaptive UI is accessibility — adapting to a user's measured motor, vision, and cognitive abilities. Twenty years of academic research backs it; almost no agency talks about it. Healthcare, government, education clients with accessibility mandates are natural fits. This is the use case where the ROI argument is hardest to argue with.

**5. Conversational and agent surfaces on stable products.** The Linear and Notion pattern — AI layered on top of a stable, predictable interface, with full auditability. Mature enough to ship, easy for clients to recognize the value, naturally extends existing engagements without requiring a leap of faith.

---

## Can we actually do this?

Honestly yes, with one specific gap to close.

**What we already have:**

- A design systems practice that few agency competitors can match — and DS is the load-bearing capability for adaptive work, full stop. The systems that can support this are the ones built as primitives with semantic descriptions, not catalogs of finished components. That's the direction we're already pushing.
- Existing commerce, retail, healthcare, and CPG relationships where this lands — Hills Pet, New Balance, CareCentrix are the kind of clients these patterns are made for.
- Cross-disciplinary teams (strategy, design, engineering) that can scope and deliver end-to-end engagements rather than handing off between specialist shops.
- Prism2, which can be extended into an adaptive-aware kit and become a real differentiator in pitches.

**What we'd need to build:**

The QA and governance side is genuinely new. Testing a generative interface is not the same as testing a fixed one — you can't QA every state, so you need *evaluation infrastructure* (test sets, automated checks, telemetry-driven detection of issues). Accessibility verification on variable surfaces is partly unsolved and requires ongoing manual work, not just CI checks. Variant logging — recording which adaptive variant reached which customer, for compliance and debugging — is infrastructure no agency has standardized yet.

These are learnable capabilities, not strategic moats held by competitors. Six to nine months of focused investment, through real client work plus a small targeted hire or two, closes the gap. The tooling (Promptfoo, OpenAI Evals, Anthropic's eval frameworks) is mature and rapidly improving.

---

## How VML could lead this

Three positions, any of which is defensible. The strongest case is to combine all three:

**The trusted adaptive experience partner.** Most agencies will pitch generative UI as inevitable and exciting. We can pitch it with the evidence — strong ROI where execution is right, real failure modes when it isn't, and the governance discipline to protect both client brand and customer trust. This is a differentiated voice in a market that's mostly evangelism right now.

**The design-systems-first firm that actually ships adaptive work.** The DS-for-adaptive-UI capability most clients can't build alone is the foundation everything else sits on. We bring the methodology, the patterns, and the tooling. This repositions our DS practice from "commodity foundational work" to "essential strategic capability." It's true; we should say it.

**The accessibility-led adaptive UI specialist.** The strongest evidence base in this whole field is accessibility research that almost no agency cites. Leading with it — and being honest about the verification gap — is an evidence-led position no competitor currently holds. It's also genuinely the right thing to do, which matters for the kinds of clients (healthcare, education, public sector) where reputation is durable.

---

## What's real vs. what's hype

Leadership respects honest framing. So:

**Real and shipping today:**
- Slot-based adaptive UI (Granola, Linear, Notion, Dia)
- AI-assisted personalization (every major CMS, with measurable revenue lift when done well)
- The agentic commerce traffic shift (Adobe data, real and trending)
- Conversational and canvas surfaces (Claude, ChatGPT, in production)
- RAG-grounded experiences (the entire enterprise AI assistant category)

**Real but earlier than the marketing implies:**
- "Generative UI" in its pure form — most production work sits in a middle ground where deterministic shells host LLM-composed content. The pure version (AI writes the interface from scratch each time) is still mostly demos.
- Agentic UX — the pattern is emerging but the empirical research base is thin, and the user-experience challenges (trust, control, when does the agent ask vs. act) are not solved.

**Hype:**
- "Every user will see a unique interface" — destructive for any product where users discuss, share, or teach the experience to each other. Won't survive the workplace.
- "Design systems become irrelevant" — every credible voice in the field says the opposite. They become more central, not less.
- "This replaces designers" — the design role expands to include behavior authorship and system design. The role grows; it doesn't shrink.

---

## What we'd recommend doing in the next 90 days

If leadership wants to move on this, four concrete moves that compound:

**1. Pilot engagement.** Pick one current commerce or experience client where adaptive UI maps to a real customer problem we can articulate. Scope a focused 6–8 week engagement testing slot-based adaptive UI in one surface. This produces a concrete proof point and a real case study, and it stress-tests our delivery model before we pitch this broadly.

**2. Internal capability sprint.** Stand up two specific capabilities: AI evaluation infrastructure (how we QA generative output) and adaptive accessibility verification (how we test that adaptive UIs serve the people they're supposed to). Both can be built through targeted internal projects with selective external advisory. Three to four months to a working internal practice.

**3. Prism2 extension.** Begin work on adaptive-aware additions to our kit — semantic component contracts, intent metadata, variant logging primitives. Even a partial version we can demo in pitches differentiates us materially. The deeper version becomes the basis for new SOW work.

**4. Point-of-view publication.** The research we have (and continue to develop) is the substrate for genuinely defensible thought leadership. Two or three signed pieces from our practice leadership across the next quarter, anchored in real evidence and real client work, positions VML as serious rather than bandwagon. The conversations these pieces start become pipeline.

---

## What we'd be saying yes to

This is a six-to-twelve month investment of design and engineering time, with measurable client revenue at the end of the runway and a defensible market position throughout. The honest tradeoffs:

**The cost of waiting:** Vercel, OpenAI, Anthropic, and the platform companies are setting the technical patterns now; agency competitors will copy the obvious moves within the year. Clients we already serve are starting to have these conversations — Hills Pet, New Balance, CareCentrix-type customers will be asking inside 12 months. Showing up without a point of view means letting someone else frame the conversation.

**The cost of moving:** Some of the patterns the industry is converging on will change as the field matures. A fraction of our investment will land in patterns that get superseded. This is the cost of being early; the alternative is being late.

**Our read:** the case for moving is materially stronger than the case for waiting. VML has the design systems practice this work requires, the client relationships where it lands, and the cross-disciplinary capability to ship it. The capability gap (evaluations, governance, variant logging) is real but closable in months. And the differentiated position (evidence-led, DS-anchored, accessibility-aware) is genuinely available right now — and won't be for long.

The recommendation is to move, and to move with a point of view rather than a feature checklist. That's how VML wins this conversation.

---

*Companion documents available: the foundation and implementation research synthesis papers contain the full evidence base, citations, and technical detail this brief draws from.*

# Notes: AI cluster + Multi-Brand Governance

Source set: ext-infrastructure (Anderson, Nov 2024), ext-figma-ai (Figma DS x AI ebook, 2025), ext-obello (Obello State of AI Design 2026), ext-ai-tools (AI Tools comprehensive overview, May 2025), ext-wolosin (Wolosin metadata article, Jun 2025), ext-multibrand (Governance Strategies for Multi-Brand DS, Apr 2025).

This is the forward-edge cluster of the knowledge base. The internal practice has its own AI-Compatible POV (4-layer stack: tokens-with-descriptions, .ai.json + registry, AGENTS.md/CLAUDE.md, Figma pipeline). These external sources both validate and extend that POV in specific ways noted in dedicated sections below.

---

## Per-doc reading log

- **ext-infrastructure.txt (24 lines)** — Sam Anderson (Director of Design, Intuit), Nov 27 2024. Very short essay (essentially the opening paragraphs of a longer Medium piece, but the thesis is fully stated in the excerpt). Establishes the core re-framing: design systems as infrastructure, not products.
- **ext-figma-ai.txt (~963 lines)** — Figma's house ebook "How design systems power the new pace of product development." Three sections: (1) Making your DS AI-ready, (2) Setting your DS up for scale, (3) Pushing teams further. Voiced through Figma leaders (Paige Costello VP Product, Yuhki Yamashita CPO, Zoe Adelman PM, Yarden Katz PM, Wayne Sun Designer, Ana Boyer Designer Advocate) plus practitioner voices (Samira Rahimi/Uber, Tali Krakowsky Apel/Coinbase, Cherin Yoo/LinkedIn).
- **ext-obello.txt (~1183 lines, very layout-distorted)** — Obello "State of AI Design 2026 Report." Vendor-authored but cites Wharton's October 2025 AI Adoption Report and an MIT research report. Three trends. Survey context: 100+ company demos and discovery calls.
- **ext-ai-tools.txt (~1446 lines)** — vendor/tooling-neutral comparative overview, May 2025. 16 tools profiled across feature comparison + lifecycle map: Vercel, V0.dev, Lovable, Galileo AI, Relume, Cursor, Bolt.new, Uizard, Figma Make, Figma Sites, Penpot, Builder.io, Anima, Locofy.ai, GitHub Copilot, Amazon CodeWhisperer.
- **ext-wolosin.txt (~753 lines)** — Diana Wolosin (Indeed DS designer), Jun 29 2025, in Design Systems Collective. First-person practitioner narrative. Articulates an AI-ready metadata schema and a four-tier metadata loop. References TJ Pitre and Murphy Trueman ("Your next design system user is an agent").
- **ext-multibrand.txt (~161 lines)** — short structured doc, Apr 2025, written for "Hub" (organization name appears once). Frameworks for governance models, contribution and intake processes, documentation governance, accessibility governance.

---

## Sam Anderson "Design Systems are Infrastructure" (Nov 2024) — full extraction

This article is excerpted in the source file (24 lines, opening only) but the thesis is complete. Verbatim arc:

> "In the past decade, design systems have transformed the way organizations create digital experiences, moving us from interpreting static style guides to a practice of regularly released and supported libraries of design + code. In many ways we have realized Nathan Curtis' vision of the design system becoming a 'product, serving other products' with Jina Anne's plea for customer-centricity ('design systems are for people') as a core truth of our practice."

> "But lately, as I've sat with design systems leaders from other companies, I've been somewhat befuddled that we are still explaining the ROI of design systems, fighting to keep resources, and worried about the future of our design systems practice."

> "I believe this can be traced back to this major technological inflection point (a similarly disruptive inflection point we saw with mobile and cloud that gave rise to the current state of design systems), and I believe that in this rapidly evolving design and technology landscape, fueled by artificial intelligence, the idea of a design system as a product may no longer be enough."

> "Design systems are no longer just projects, tools, frameworks, or even products — design systems are infrastructure."

**Why the reframing matters (interpretation; the essay excerpt only states the thesis):**

1. *Product framing implies optionality.* If a DS is a product, customers choose to consume it; teams ROI-justify it; resources can be argued away. Infrastructure is non-optional — it's the substrate everything else is built on.
2. *Product framing optimizes for human consumers.* Infrastructure framing acknowledges multiple consumer types — humans, AI agents, downstream systems, brand extensions — and forces standards, contracts, and uptime thinking.
3. *Mobile/cloud parallel.* Anderson explicitly aligns this inflection with the mobile and cloud waves. Mobile forced responsive thinking and DS librarification. Cloud forced API-first thinking. AI is forcing infrastructure-grade thinking — versioning, machine-readable contracts, observability, governance.
4. *Implicit consequence:* If DS is infrastructure, then the ROI conversation Anderson is "befuddled" by becomes obsolete. You don't ROI-justify electricity; you fund it because nothing works without it.

This is a load-bearing framing for the practice's POV. The internal VML deck's "DS as infrastructure" line traces directly here.

---

## AI cluster — synthesized themes

Cross-reading Figma DS x AI, Obello, AI Tools overview, and Wolosin reveals strong consensus on five themes.

### 1. AI is a new consumer of the design system

This phrase, or a near-synonym, appears in every source:

- Figma (Zoe Adelman): "We're seeing a shift where AI also becomes a consumer of the design system and designers and developers increasingly work with what AI produces."
- Wolosin: "AI is becoming a real user of our systems. It doesn't care if a component is pretty; it cares if it's structured and labeled and can read, understand, and act on the intent behind it."
- Murphy Trueman quoted by Wolosin: "Your next design system user is an agent."
- Obello (Trend 3): designers shift from making assets to making tools that AI will use.

The implication is uniform: documentation, naming, structure, and metadata that was previously "nice to have" because humans could fill gaps with intuition is now load-bearing because AI cannot.

### 2. Tokens must be machine-readable and intent-bearing

- **Figma:** "Structure design tokens clearly. Store tokens in machine-readable formats (like JSON or YAML) with consistent naming so colors, spacing, and typography map predictably to production variables." Also: "Preserve logic through tokens and metadata. Keep tokens and variables tightly linked to component behavior so AI has reliable cues for spacing, color, and typography."
- **Wolosin** doesn't deeply address tokens but treats them as Tier 1 of the metadata loop ("Structured Metadata → MCP server").
- **Obello:** brand rules (logo clearspace, color pairings, typography hierarchy, gradients, approved combinations) become the system's encoded constraint surface — what their platform calls "Brand Rules."
- **Figma's "AGENTS guide" implication** (in their MCP framing): tokens as JSON/YAML with consistent naming, mapped to production variables, are the floor — the level beneath which AI cannot generate sensibly.

The cross-source pattern: tokens alone aren't enough. Tokens + descriptions of intent (what is `surface-elevated-2` *for*?) become the unit AI reasons over.

### 3. Components need metadata, not just variants

This is where Wolosin is sharpest. Her schema (extracted in detail below) treats every component as a node in a labeled dataset.

- **Figma echoes:** "Add higher-order compositions—blocks and patterns that capture layout, color, and spacing logic—gives AI the context it needs to generate those interfaces." Smaller atomic pieces are *too small* for AI to compose into coherent layouts. Card-as-block beats button + text + image + container because the relationships are encoded.
- **Figma:** "Expose component relationships. Make it clear how components, patterns, and variants relate across design and code—through naming, hierarchy, or metadata—so AI can understand how parts fit together."
- **Obello (Trend 1):** "Tools that only generate assets bump into limitations quickly. Instead, brand teams trust tools that they can encode with brand rules, workflows, and governance." This maps to component metadata at the brand-rule layer.

### 4. New artifacts the field is converging on

Cross-source synthesis of named artifacts/standards:

| Artifact | Sources naming it | What it does |
|---|---|---|
| **MCP (Model Context Protocol)** | Figma (extensive), Wolosin (extensive), AI-tools (referenced via Cursor) | Server that gives AI structured real-time access to DS components, tokens, docs. Wolosin: "An MCP connects your metadata-rich assets to your AI solutions." |
| **Component metadata schema** (JSON-shaped) | Wolosin (full schema), Obello (brand rules), Figma (descriptions, usage guidelines) | Per-component structured fields capturing purpose, when-to-use, avoid-when, content slots, semantic role, trigger keywords. |
| **Code Connect** | Figma | Maps Figma components to real code components so AI references production code, not generic snippets. |
| **Higher-order blocks/compositions** | Figma | Cards, headers, carousels — pre-composed patterns that close the gap between atomic components and full layouts. |
| **AI-readable design tokens** (JSON/YAML) | Figma, Wolosin (Tier 1) | Tokens with predictable naming, machine-parseable, tied to component behavior. |
| **Brand rules / governance encoding** | Obello (extensive), Figma (less explicit) | Logo clearspace, approved color pairings, typography hierarchy, tone of voice — encoded so AI can enforce automatically. |
| **AGENTS.md / CLAUDE.md / instruction files** | Implicit in Figma ("Providing complete instructions alongside a design system gives AI the context it needs"). NOT explicitly named in these sources. | Sets reasoning rules, conventions, do/don't for the agent. |
| **Figma Make / Figma Sites** | Figma, AI-tools | Figma's pipeline product — design system as live executable substrate. |

The internal practice's 4-layer stack (tokens-with-descriptions / .ai.json + registry / AGENTS.md+CLAUDE.md / Figma pipeline) maps to most of this. The notable gap: **none of these external sources explicitly name an AGENTS.md-style instruction file.** That artifact appears to come from the engineering side (Cursor/Claude Code conventions) more than the design-systems-discourse side.

### 5. Tooling landscape — where each tool fits

From ext-ai-tools, the consensus mapping for a DS practice:

**For the design phase:**
- **Galileo AI, Uizard** — text/sketch → UI generation. Useful for ideation, not DS rigor.
- **Relume** — sitemap → wireframe → style guide pipeline. Useful for marketing/site work, less so for product DS.
- **Figma Make** — prompt-based design generation inside Figma. Most relevant to DS work because outputs respect Figma styles/variables.
- **Figma Sites** — design-to-publish for marketing surfaces.
- **Penpot** — open-source, designs natively expressed as SVG/CSS/HTML. Differentiator for on-prem/regulated clients.

**For design-to-code:**
- **Anima** — Figma/XD/Sketch → React/Vue/HTML. GenAI code personalization (e.g., "use arrow functions"). Maps Figma components to code components.
- **Locofy.ai** — Figma → React/RN/Next/Flutter. Mobile cross-coverage. Live prototype previews.
- **Builder.io / Visual Copilot** — Figma → multi-framework (React, Vue, Qwik, Angular, Svelte, Flutter). Headless CMS layer too. Custom instructions for code gen alignment.
- **V0.dev** — text → React/Next.js/Tailwind/shadcn. Best for greenfield prototypes, not DS-bound work.

**For full-stack agent generation:**
- **Lovable.dev** — full-stack from prompt or Figma import. Stripe/Supabase/Clerk integrations. Agency MVP play.
- **Bolt.new** — StackBlitz + Claude. Browser-based, runs immediately. Prototype play.

**For code assistance (developer-side):**
- **Cursor** — full IDE with agent mode. Most cited as the Wolosin-class tool for MCP-driven DS workflows.
- **GitHub Copilot** — autocomplete + chat. Broad-language. Enterprise tier.
- **Amazon CodeWhisperer** — AWS-tilted, free for individuals, security scan + reference tracking.

**For deployment:**
- **Vercel** — preview-per-commit, AI SDK, host for V0/Lovable outputs.

**Role assignments for DS practice specifically:**
- *Cursor* is the daily driver if the team is doing DS work via code (matches internal practice POV).
- *Anima / Builder Visual Copilot / Locofy* are the bridge tools when designers own Figma and devs need clean output that respects the DS.
- *Figma Make + Figma Sites* are the "Figma's house view" tools — most clients will encounter these first because they live where the design lives.
- *Lovable / V0 / Bolt* are not DS-aligned tools; they are greenfield generators that *ignore* most DS infrastructure unless explicitly fed it. Treat as risk surface for off-brand drift.

### 6. Risks and failure modes named across sources

- **"AI look" / generic outputs.** Obello: AI-generated images had "an obvious 'AI look' that seemed generic or synthetic." Figma's Ana Boyer (paraphrased): if everyone uses AI without DS, "we don't all end up shipping the same generic UIs cobbled together from the same pool of AI-generated parts."
- **Legal/compliance liability.** Obello (Trend 2): "Will this pass legal?" 64% of orgs have AI data security policies; 53% have privacy policies; 50% ethical use policies; 48% human oversight policies. 70% of executives select AI vendors based on workflow understanding.
- **Implicit-knowledge gap.** Figma (Zoe Adelman): "What many designers and developers can infer just from understanding the brand and the business as a whole, AI doesn't inherently know."
- **Drift / hallucinated workarounds.** Figma (Zoe): "tracking how AI interprets components, logging where it breaks rules or invents workarounds."
- **Missing accessibility / animation expectations.** Figma (Zoe): "A component that exists only in design might look fine in an AI-generated mockup but miss accessibility features or expected animations."
- **Over-reliance.** Figma (Ana): "It's important to avoid relying on AI as the absolute expert—you need to check its outputs before confidently shipping something."
- **Tool fragmentation.** Obello (closing): "the AI design landscape is fragmenting rapidly. Companies launch new tools every week... companies are also shutting down, getting acquired, or pivoting." This is a real planning risk for client recommendations.

### 7. Predictions about 2026–2027

- **Figma:** AI moves from consumer to *co-author*. "I think we're going to see that AI plays a bigger role in building alongside design system teams, so they will co-author alongside humans." (Zoe Adelman)
- **Figma research stat:** 42% expected growth in time spent collaborating/co-creating/reviewing AI outputs in next 12 months.
- **Figma:** 56% of non-designers participating frequently in design tasks. 55% of product builders taking on out-of-scope tasks. 57% of product builders spending more time on high-value work (vision, strategy).
- **Obello:** Designers' role shifts decisively from making assets to making tools. "Designers will set the rules in the tools by defining what 'on-brand' means, in systematic terms that AI can understand." Designers do strategic work (testing narratives, customer insights, creative directions); AI handles production.
- **Obello (Wharton 2025):** 65% of respondents used AI for marketing content creation — most popular use case.
- **Obello (MIT):** 70%+ of executives now select AI vendors by workflow fit, not feature lists.
- **Wolosin:** Metadata becomes training data — "I'm not just building components. I'm building the foundation for intelligent systems." Implicit prediction: design systems become labeled datasets that train domain-specific models.
- **AI-tools (vendor predictions, more speculative):** Continuous deepening of design-to-code automation; multi-framework generation becomes table stakes; MCP becomes the lingua franca for AI/DS integration.

**What's tested vs. speculative:**
- *Tested now:* Tokens-as-JSON, Code Connect, MCP servers (Cursor + Figma), component metadata schemas (Wolosin/Indeed), "Figma Make" prompt-to-prototype, governance frameworks at large orgs.
- *In active rollout:* Figma Make + Figma Sites (beta as of mid-2025), Builder Visual Copilot (live), Anima GenAI personalization (live), MCP standard (still emerging).
- *Speculative / 2026-2027 horizon:* AI as co-author of the DS itself, AI auto-generating component variants from a single source asset, AI auto-flagging DS inconsistencies as "diagnostic data" (Zoe Adelman's framing), DS-as-trained-model.

---

## Wolosin metadata model (Jun 2025) — extract in detail

Diana Wolosin is a UX designer at Indeed, ~8 years experience, formed in Colombia and Spain, based in San Diego. The article is a first-person reflection on her shift "from designing for humans to designing for AI." It builds on conversations with TJ Pitre.

### Core thesis

> "AI is becoming a real user of our systems. It doesn't care if a component is pretty; it cares if it's structured and labeled and can read, understand, and act on the intent behind it."

> "I'm not just building components. I'm building the foundation for intelligent systems."

Reframe of what DS work *is*, per ChatGPT's response to her "what am I doing?": Information Architecture / Knowledge Management / ML Ops applied to design / Data Labeling for Supervised Learning / Semantic Systems Design / AI-Ready Component Architecture / Taxonomy Engineering / Metadata Strategy.

### The metadata schema (verbatim)

```json
{
  "component_id": "",
  "primary_purpose": "",
  "when_to_use": "",
  "avoid_when": "",
  "required_content": "",
  "optional_content": "",
  "common_partners": "",
  "generation_priority": "",
  "layout_behavior": "",
  "semantic_role": "",
  "trigger_keywords": "",
  "responsive_support": ""
}
```

### Per-field interpretation

- `component_id` — stable identifier; the join key across Figma / Storybook / code / docs.
- `primary_purpose` — one-sentence statement of what the component does. "This is a navigation primitive."
- `when_to_use` — positive selection rule. AI uses this to pick between similar components.
- `avoid_when` — negative selection rule. Crucial because AI defaults to using whatever it finds. Wolosin (paraphrasing Figma): the most cited gap in AI-generated outputs is wrong-component-for-job.
- `required_content` — slot contract. What MUST be present (label, icon, etc.).
- `optional_content` — what MAY be present.
- `common_partners` — components this one typically appears alongside. Encodes composition logic. (E.g., a Toolbar's common_partners = [Button, IconButton, Divider].)
- `generation_priority` — rank/weight for AI to prefer this over alternatives. Wolosin doesn't fully define this, but the implication is a tiebreaker for the model.
- `layout_behavior` — how it lays itself out (fill, hug, fixed, responsive grid behavior). This is what Figma calls "auto-layout intent."
- `semantic_role` — ARIA-like semantic intent. "navigation," "form-control," "alert."
- `trigger_keywords` — words in a prompt that should call this component. ("checkout button" → Button with primary intent variant.) This is the explicit prompt-to-component mapping.
- `responsive_support` — which breakpoints/devices it's valid on.

### The four-tier metadata loop (Wolosin's most important contribution)

> "Here's how we're tying it all together:"

1. **Tier 1 — Structured Metadata.** Metadata → MCP server. The schema above, served via MCP.
2. **Tier 2 — Embedded Metadata in Figma.** Native Figma metadata and tagging. Component descriptions, variant labels, variable names.
3. **Tier 3 — Embedded Metadata in React.** Through component structure — prop types, JSDoc, semantic naming.
4. **Tier 4 — Cross-linking via Figma↔Storybook.** Figma's native dev link.

> "Each tier closes the loop between tools. Figma serves designers, React serves developers, and the AI-ready metadata serves AI."

### Use cases the metadata enables

- A Figma plugin that generates layouts from prompts
- A prototype generator
- A QA tool that flags non-compliant accessibility
- An assistant that recommends patterns based on intent
- A translation layer between design and dev that reduces friction

### Key claim

> "Supervised machine learning relies on labeled data. And that's exactly what I've started doing... Every time I tag a component with usage context or define what the 'business_context' field means, I'm not just documenting, I'm training the system. I'm creating a labeled dataset for future models to learn from."

> "Metadata isn't busywork. It's training data for the future of design."

### Closing frame (citing Murphy Trueman)

> "You need to start treating your component architecture like an API — clear contracts, explicit inputs and outputs, and semantics that work for humans and machines alike."

> "Once we treat our components like data, we stop thinking about just usage and start thinking about interpretability."

### Wolosin's stated foundation

She is explicit that this work *only* happens because of the foundational, conventional DS work her team at Indeed has done: standardized component library, structured Figma files, mirrored Storybook structure, dev-design alignment, rich documentation. The AI-ready layer "stands on the shoulders of the traditional design system." This is important to note — she's not claiming AI-readiness replaces fundamentals; it requires them.

---

## Figma DS x AI (2025) — extract

### Headline framing

> "In the age of AI, design systems are a context coefficient — the clearer and more complete a system is, the more likely AI is to produce on-brand results."

This is Figma's central thesis. "Context coefficient" is a useful phrase — the DS multiplies the quality of any AI output that touches it.

### Key voices and what they say

- **Yuhki Yamashita (CPO):** "Instead of discouraging contributions from PMs or other non-designers who want to design, what if we welcomed them into the process? Designers can even empower these collaborators by sharing their quality standards and sense of taste. Design systems—which codify these standards and taste—play a crucial role in making this possible."
- **Paige Costello (VP Product):** "The whole product development process used to start at the beginning and it was very linear. Now, you can start in the middle then go back to the beginning, or start at the end then go back to the middle. The whole lifecycle has both collapsed and shifted in terms of where you can start."
- **Zoe Adelman (PM):** "Authors should be prioritizing getting as much context into the system as possible. What many designers and developers can infer just from understanding the brand and the business as a whole, AI doesn't inherently know." Also: "It's going to be more on authors to see what kind of outputs are coming from their systems."
- **Yarden Katz (PM):** "If we really want to maximize the power of AI in product development, we need to give it the same knowledge our best people have. The model needs to understand how we work, what we value, and what makes our product distinct. The results should feel native to us."
- **Wayne Sun (Designer):** "Design decisions like how interface building blocks are defined, how components are wired, and how they're used represent the DNA of how a product is built and understood. There's a lot of buried treasure there. When models can tap into that structure, they can generate interfaces that align with the system out of the box."
- **Ana Boyer (Designer Advocate):** "[Design systems] help make sure we don't all end up shipping the same generic UIs cobbled together from the same pool of AI-generated parts."
- **Cherin Yoo (LinkedIn Product Designer):** "We were trying to get more deterministic outputs that would accurately abide by not just our components and styles, but our product patterns as well. LLMs make choices within the boundaries we give them, and this template helps us narrow those boundaries."
- **Samira Rahimi (Uber):** "It doesn't matter how big or small, the most important part [of a design system] is treating it like a product. A design system won't succeed if it's just a thing. It should be a product with clear OKRs, a roadmap, customers, and output."

### Six concrete prescriptions for AI-readiness

From the "In short" callouts:

1. **Structure tokens and variables predictably.**
2. **Document usage rules and intent.**
3. **Add higher-order compositions, clarify relationships, maintain clean file structures.**
4. **Connect design and code through tools like Code Connect and MCP.**
5. **Add larger, reusable blocks** (headers, cards, carousels) for AI to draw from when generating layouts.
6. **Include accessibility details** (color contrast, keyboard navigation) inline so AI builds them in by default.

### Documentation standards Figma names

- Explain the "why" — purpose and when-to-use, not just appearance
- Keep structure consistent across components
- Show right and wrong examples — explicit do/don't
- Maintain layer hygiene — no unnecessary groups/frames; AI parses cleaner files better
- Document behavior and states — hover, focus, error
- Include accessibility details

### LinkedIn case study (in-practice)

LinkedIn used Figma Make to build a starter template grounded in their design system. Generates on-brand layouts across devices including light/dark modes. Quote: "more deterministic outputs that would accurately abide by not just our components and styles, but our product patterns as well." This is the canonical "Figma Make + DS" pattern.

### MCP framing (Figma's house view)

> "Through tools like Figma Make, MCP also connects design artifacts to the code that powers them. AI can reference the real structure and logic behind a file, keeping generated outputs consistent with established standards and helping teams move from prototype to production more quickly."

Three specific MCP use cases Figma names:
- **Connecting design to code** — generated code references real components and variables
- **Automating token work** — AI suggests where tokens should be applied; helps write scripts for token workflows
- **Auditing design-code alignment** — AI agents flag prop misalignment, audit token usage, suggest layer name improvements

### Skills shift

Figma's section 3 is about how DS team *roles* change:
- Authors will spend more time looking at AI usage patterns ("treating AI's activity as diagnostic data")
- Authors will need to understand AI's behavior — where it excels, where it drifts
- Prompting becomes a core skill: break down complex concepts, include design context, use plain specific language ("use a 16px button" not "make it bold"), provide good examples, ask AI to explain reasoning
- "AI will help automate some aspects of overhead and operations... This shift will free up more time to work on the high-level vision of the overarching design of a product." (Ana Boyer)

### Figma Make + Code Connect specifics

- Figma Make will allow prototyping with DS components via React code imports from public or private npm packages.
- Code Connect ties Figma and the codebase together so developers see real production code without leaving Figma.
- Both reduce context switching and keep designs and implementations aligned.

---

## Obello 2026 AI Design Report — extract

The PDF text is heavily layout-distorted (it is a richly designed report rendered as text). I extracted the readable narrative below. Vendor-authored (Obello sells an AI-powered design platform with brand-rules encoding) but cites Wharton (Oct 2025 AI Adoption Report) and an MIT research report. Sample size: "product demos and discovery calls with designers and marketers on brand teams at more than 100 companies."

### Headline finding

Brand teams have moved past experimentation. "What began as tests with image generators has evolved into systematic evaluation: which AI tools can actually fit into production workflows?"

### Three trends

#### Trend 1: Shift from Generation to Systems

> "Tools that only generate assets bump into limitations quickly. Instead, brand teams trust tools that they can encode with brand rules, workflows, and governance."

Generative tools (Midjourney, DALL-E, Stable Diffusion) were "just a starting point." Output had "an obvious AI look that seemed generic or synthetic." Beyond visual quality, the killer question savvy designers ask is: "Will this pass legal?"

**What this means (their three actionables):**
1. Design the system, let it execute on your behalf.
2. Take AI adoption from solo experiment to team conversation.
3. Map your design intuition. "If I had to explain my design system's logic to someone tomorrow, could I do it clearly enough for them to make consistent decisions? Where do I have clarity, and where am I still relying on intuition that hasn't been codified yet?"

#### Trend 2: Trust, Governance, Liability Become Non-Negotiable

Survey numbers (Wharton AI Adoption Report, Oct 2025):
- **64%** of organizations now have data security policies defining what info can be fed into AI tools
- **53%** strict usage policies around data privacy
- **50%** policies around ethical use
- **48%** policies around human oversight
- **70%** of executives select AI vendors based on workflow understanding (MIT research report)

Trust questions brand teams now ask:
- Clear ownership and liability — who is responsible when something goes wrong?
- Indemnification and risk boundaries
- Brand-safe generation — can the system prevent off-brand outputs?
- Governance and oversight
- Auditability — can we track creation provenance?
- Brand consistency
- Reviewability
- Permissioning

> "Trust isn't a secondary consideration when AI moves into production, it is now the main constraint to making production possible."

**Actionables:**
1. Make trust your competitive advantage.
2. Define your governance requirements before evaluating tools. "What does 'brand-safe' mean for you?"
3. Establish your permission structure early.

#### Trend 3: Designer's Role Shifts from Making Assets to Making Tools

Wharton 2025: 65% used AI for marketing content creation — most popular use case.

The shift:
> "Designers will train systems, so menial reviews are no longer required."

> "Designers will set the rules in the tools by defining what 'on-brand' means, in systematic terms that AI can understand. Designers will need to teach the system to enforce rules such as acceptable color combinations, tone of voice, and visual styles for product photography. They will also train the system with examples, by providing reference images, as well as approving layouts and art direction, so the system learns what good looks like for their specific brand."

The new workflow: designer sets a moodboard → system understands the rules for the campaign → designer asks system to generate creative directions (not final assets) → designer picks a strong concept → anyone creating assets stays aligned with that vision.

> "This ambiguity is where brand designers remain indispensable. Storytelling is nuanced. Things need to feel right; rules constantly need updating in a dynamic world. What may have felt right six months ago might feel tone-deaf in the present moment."

> "The designer's taste becomes the calibration mechanism that makes the entire system work."

**Actionables:**
1. Step into creative direction.
2. Consider how AI fits into your responsive workflow.
3. Identify your unique perspective. "What parts of my current work actually require my taste and judgment, and what could be systematized?"

### Closing observation (Obello-specific but useful)

> "The AI design landscape is fragmenting rapidly. Companies launch new tools every week. Some promise to generate assets, others claim to be your design copilot, a handful focus on brand systems, while (still!) others layer on top of your existing workflows. At the same time, companies are also shutting down, getting acquired, or pivoting."

This is real. Any client recommendation needs to factor tool-survival risk.

---

## AI Tools comprehensive overview (May 2025) — extract

The full feature comparison and per-tool deep dive is in the source. Synthesized DS-relevant view:

### Tool taxonomy

**Idea/UX generation (low DS rigor):**
- Galileo AI — text/sketch → UI; Figma export
- Uizard — text/sketch → multi-screen; React snippets
- Relume — sitemap → wireframe → style guide; Webflow/Figma/React export

**Figma-native AI (high DS relevance):**
- Figma Make — prompt → high-fidelity prototype in Figma (beta)
- Figma Sites — design → live site (beta)
- Penpot — open-source, designs natively SVG/CSS/HTML; AI plugins emerging

**Design-to-code bridges (highest DS relevance):**
- Anima — Figma/XD/Sketch → React/Vue/HTML; GenAI code personalization (prompt to customize generated code)
- Locofy.ai — Figma → React/RN/Next/Flutter; supports design tokens; live prototypes
- Builder.io / Visual Copilot — Figma → React/Vue/Qwik/Angular/Svelte/Flutter; headless CMS; custom instructions for codegen alignment

**Full-stack AI generators (low DS rigor unless explicitly fed):**
- Lovable.dev — full-stack from prompt; Figma import; Stripe/Supabase/Clerk integrations
- V0.dev (Vercel) — text → React/Next/Tailwind/shadcn (beta)
- Bolt.new — StackBlitz + Claude; in-browser; multi-framework

**Code assistance:**
- Cursor — full IDE, agent mode, MCP-friendly. Most DS-aligned dev tool.
- GitHub Copilot — autocomplete + chat; Copilot for Business
- Amazon CodeWhisperer — AWS-tilted, free for individuals, security scan

**Hosting/deployment:**
- Vercel — preview-per-commit, AI SDK

### Lifecycle map (paraphrased)

- **Ideation & UX** — Galileo, Uizard, Relume (sitemaps), Figma Make
- **UI Design & Prototyping** — Figma Make, Penpot, Relume style guides, Figma Sites, Galileo, Uizard
- **Design System & Handoff** — Relume export, Penpot inspect, Builder Visual Copilot
- **Development (codegen)** — V0, Lovable, Bolt, Anima, Locofy, Builder
- **Development (assist)** — Cursor, Copilot, CodeWhisperer
- **Deployment** — Vercel, Figma Sites, Lovable/Bolt one-click deploy

### Agency recommendation pattern (from this source)

- *Small business client:* Galileo/Uizard for UI options + Lovable/V0 for prototype/MVP + Vercel or Figma Sites
- *Enterprise client:* Penpot (if on-prem needed) or Figma Make/Sites; Anima/Locofy for DS-faithful codegen; Copilot/CodeWhisperer for dev productivity; Relume's style guide for in-brand concepting
- *Across all:* AI coding assistants for repetitive work; humans validate

### Notable verbatim from this source

> "Builder.io is the only platform that weaves together an AI design-to-code tool, visual editing, and CMS."

> "Anima... claims to save 50–70% of developers' UI coding time by automating the grunt work."

> "Cursor... runs as a desktop app on Mac/Windows... Agent mode is especially unique – it can handle multi-step tasks (writing code, running it, debugging) autonomously."

---

## Multi-Brand Governance (Apr 2025) — extract in detail

Short doc (161 lines), clearly written, addressed at one point to "Hub" (likely the implementation org). Surprisingly orthodox — it does NOT engage with AI at all. This is strictly a governance framework piece.

### Definition

> "A multi-brand design system is a centralized set of guidelines, assets, and rules that enables consistent user interfaces across multiple brands or sub-brands within a larger organization. Unlike standard design systems, multi-brand systems are optimized for flexibility, allowing product teams to leverage an existing component library while adapting it to different brand identities."

### Frameworks proposed

Three governance models named:

1. **Centralized.** "A dedicated team responsible for the design system's development and maintenance. This approach provides clear ownership and accountability but may sometimes disconnect from day-to-day product needs if not carefully managed."

2. **Hybrid.** "Many organizations ultimately adopt a hybrid approach, combining centralized oversight with distributed contribution. This balances consistency with practical implementation concerns and offers flexibility as the organization grows."

3. **Federated** (referenced but not fully defined). "Documentation responsibilities should be clearly assigned, whether to a centralized team, component owners, or through a federated model where representatives from each brand maintain their specific sections."

### Decision rules (when each fits)

The doc is light on explicit decision rules. It states the centralized model is the "recommended governance model" but the hybrid is "ultimately adopted" by many. Inferred rules:
- *Centralized fits* when the org needs maximum consistency, has a dedicated team, and can tolerate slower distributed product velocity.
- *Hybrid fits* most growing organizations — central oversight + distributed contribution.
- *Federated fits* multi-brand orgs where each brand has enough scale to maintain its own section/sub-system.

### Best-practice elements named

1. **Defining clear roles** — who owns, decides, contributes.
2. **Establishing contribution processes** — who can contribute, what qualifies, how to progress from proposal to implementation.
3. **Implementing version control** — semantic versioning, changelog, deprecation strategy.
4. **Regular reviews and communications** — design/eng/product meetings; monthly or quarterly org-wide updates.

### Component governance (most actionable section)

**Component Qualification Process** — four criteria for what qualifies as a system component:
1. The problem it solves
2. How it differs from existing components
3. Reusability potential across brands
4. Technical feasibility and accessibility compliance

**Component Request and Intake Process — 9 steps:**
1. Initial Inquiry (review catalog first)
2. Communication Channel (Slack/Jira/GitHub)
3. Assessment and Guidance
4. Qualification Review (cross-brand reusability, system alignment, feasibility, scalability)
5. Prototyping and Initial Concept
6. Review and Approval
7. Prioritization and Backlog Entry
8. Formal Development and Testing
9. Documentation and Release

**Component Testing Process — 10 steps:**
1. Content (lengthy/i18n text)
2. Accessibility
3. Cross-browser/device
4. Responsive across resolution spectrum
5. Functionality unit tests
6. Stress test examples in workshop (common, edge, stress)
7. Internal code review
8. Internal design review
9. Trial in applications (pre-release with user devs)
10. Other internal QA

### Contribution workflow (7 steps)

Proposal → design/dev specs → peer review → cross-brand testing → docs → final approval → distribution & announcement.

### Documentation governance

Standards required:
1. Writing guidelines for tone and style
2. Required information for each component
3. Example formats and implementation details
4. Accessibility requirements
5. Brand-specific variations

### Accessibility governance

- WCAG 2.0 AA = legal baseline; strive for 2.1 AA or 2.2
- Centralized accessibility testing for consistency, but individual brand implementations also test
- Required: testing procedures, accessibility feature documentation, issue-resolution process, regular cross-brand audits

### Failure modes named

- Without governance: "this enthusiasm can quickly erode confidence in the system, making decisions seem arbitrary rather than methodical."
- Centralized risk: "may sometimes disconnect from day-to-day product needs if not carefully managed."
- Component bloat: prevented by qualification criteria.
- Inconsistent contribution: prevented by structured workflow.

### Notable verbatim language

> "Governing a multi-brand design system requires balancing consistency with flexibility, maintaining quality while enabling efficient contributions, and ensuring accessibility while supporting brand individuality."

> "The most effective governance strategies combine clear processes, defined roles, regular communication, and measurable outcomes."

> "Governance is a critical factor determining whether they truly deliver on their promise of unified, consistent experiences across multiple brands while still allowing each brand's unique personality to shine."

### What's notably ABSENT from this doc

- No discussion of AI or AI consumers of the DS.
- No discussion of tokens or token architecture for multi-brand (e.g., theme primitives + brand semantics split, which is the standard 2024-2025 pattern).
- No discussion of composition-based brand extension (the internal POV approach).
- No discussion of automated checks/CI for governance.
- No 5-dimension brand-alignment rubric or analogous evaluation framework.
- No measurement/metrics framework for governance effectiveness.

This means the doc is foundational but stops well short of the practice's internal multi-brand POV. It's a useful canonical reference for *process governance* but not for *technical governance* of multi-brand systems.

---

## Phase-tagged findings (canonical 8 phases)

### Foundations (tokens for AI)
- **Tokens must be machine-readable** (JSON/YAML), with consistent naming, predictable hierarchy. (Figma)
- **Tokens need descriptions/intent** — beyond key/value, AI needs to know what `surface-elevated-2` is *for*. (Cross-source)
- **Higher-order tokens** — gradients, color pairings, approved combinations are tokens too. (Obello brand rules)
- **Token-component coupling** — keep tokens tightly linked to component behavior so AI has reliable cues for spacing/color/type. (Figma)
- **Multi-brand foundation:** primitive tokens + brand-semantic tokens layered separately (NOT explicitly in multi-brand source — comes from internal POV).

### Component Library (metadata)
- **Wolosin's 12-field schema** as a starting template (component_id, primary_purpose, when_to_use, avoid_when, required_content, optional_content, common_partners, generation_priority, layout_behavior, semantic_role, trigger_keywords, responsive_support).
- **avoid_when is uniquely important** — AI defaults to using whatever it finds; negative selection rules are load-bearing.
- **trigger_keywords** as the explicit prompt-to-component map.
- **common_partners** encodes composition logic (the gap Figma also names: AI struggles to compose atomic components into layouts).
- **Higher-order blocks** (cards, headers, carousels) are the right unit for AI generation — not buttons + inputs. (Figma)
- **Component qualification criteria** — problem solved, differentiation, cross-brand reusability, accessibility. (Multi-brand)
- **Code Connect / Figma↔code linking** as part of component metadata. (Figma)

### Documentation (machine-readable layer)
- **Make implicit explicit** — what humans can infer from brand context, AI cannot. (Figma/Zoe)
- **Standard format per component:** purpose, usage, behavior, accessibility, do/don't examples. (Figma)
- **Layer hygiene** — keep file hierarchies clean of unnecessary groups/frames. (Figma)
- **Documentation as training data** — each tagged component is a labeled data point. (Wolosin)
- **AI-accessible doc formats** — `.ai.json`, MCP server, embedded Figma metadata, embedded React metadata, Figma↔Storybook crosslinks. (Wolosin's 4 tiers; internal POV's .ai.json artifact extends this.)
- **Provide examples of "what good looks like"** — for AI to align style. (Figma prompting section)

### Governance (multi-brand)
- **Three governance models:** centralized, hybrid (most common), federated. (Multi-brand)
- **Component qualification + intake + testing** — 9-step intake, 10-step testing, 7-step contribution. (Multi-brand)
- **Trust as primary constraint** for AI adoption: ownership, indemnification, brand-safety, auditability, permissioning. (Obello)
- **Governance encoding** — brand rules (logo clearspace, color pairings, typography hierarchy) become *enforced* by the system, not just documented. (Obello)
- **Designer as system trainer** — designers calibrate the system rather than approving every asset. (Obello)
- **Accessibility governance** — WCAG 2.1/2.2 AA target, centralized + brand-level testing. (Multi-brand)

### Ongoing Maintenance (measurement, freshness)
- **Treat AI activity as diagnostic data** — log where AI breaks rules, invents workarounds, picks wrong components. (Figma/Zoe)
- **Track consumption patterns** — which components AI uses vs. ignores. (Figma)
- **Version the system as a product** — backlog, OKRs, customers, output. (Figma/Samira)
- **AI flywheel** — each cycle of AI + humans builds fluency for next cycle. (Figma)
- **Brand evolution requires retraining** — what felt right 6 months ago may feel tone-deaf now. (Obello)
- **Quarterly org-wide updates** — governance communication. (Multi-brand)
- **Continuous component testing** — content edge cases, i18n, accessibility audits, cross-browser. (Multi-brand)

### Component Library (Phase 4 in canonical 8) overlaps heavily with Foundations in this cluster — most insights cut across.

### Phases NOT directly addressed by these sources
- **Discovery** — the multi-brand and AI sources mostly assume the DS exists.
- **Strategy/scoping** — Anderson's "infrastructure" framing is the closest, but no concrete strategy guidance.
- **Tooling/setup** — covered tangentially by AI-tools but not as DS-build-step guidance.

---

## Where these sources VALIDATE the practice's internal AI-Compatible POV

Internal POV (per the prompt): 4-layer AI stack — (1) tokens with descriptions / .ai.json + registry, (2) AGENTS.md+CLAUDE.md, (3) Figma pipeline; brand extension via composition patterns; 5-dimension brand-alignment rubric.

### Strong validations

- **Tokens with descriptions** → Figma explicitly: "Preserve logic through tokens and metadata. Keep tokens and variables tightly linked to component behavior so AI has reliable cues."
- **.ai.json / registry** → Wolosin's Tier 1 ("Structured Metadata → MCP server") plus her 12-field schema. The internal `.ai.json` is essentially Wolosin's schema serialized at component scope.
- **Figma pipeline** → Figma DS x AI is essentially a 30-page validation of this. Code Connect, MCP, Figma Make, machine-readable variables. LinkedIn case study is the "Figma + DS template" pattern.
- **Component metadata as load-bearing** → Wolosin and Figma both name this. Wolosin: "Once we treat our components like data, we stop thinking about just usage and start thinking about interpretability."
- **Documentation must encode intent, not just appearance** → Figma's "Explain the why," Obello's brand rules encoding, Wolosin's primary_purpose / when_to_use / avoid_when.
- **Higher-order composition** → Figma's blocks/cards/headers framing maps closely to the internal "composition patterns for brand extension" — atomic + composable scaffolds AI can recombine.
- **Designer-as-system-trainer role shift** → Obello Trend 3 directly: "designers will set the rules in the tools." Figma: "more on authors to see what kind of outputs are coming from their systems."
- **DS as infrastructure** → Anderson's thesis explicitly. Internal POV's "DS as infrastructure" line traces here.

### Notable: AGENTS.md / CLAUDE.md is NOT validated by these sources

None of the four AI-cluster sources explicitly names an instruction-file artifact like AGENTS.md or CLAUDE.md. The closest is Figma's prompting-best-practices section ("providing complete instructions alongside a design system"), but it's framed as user-side prompting, not a persistent agent-instruction artifact.

This is a gap the internal POV fills that the public discourse hasn't caught up to. The artifact is well-known in the dev/Cursor world (`.cursorrules`, AGENTS.md conventions) but hasn't crossed into DS discourse yet. **This is a defensible POV differentiator** — the practice can claim the instruction-file layer as part of its forward POV.

---

## Where these sources CHALLENGE or EXTEND internal POV

### Extensions

1. **Wolosin's 4-tier metadata loop** is more granular than the internal 4-layer stack. Tiers 2 (Figma-native metadata) and 3 (React component structure) are emphasized as separate from the .ai.json/registry layer (Tier 1) and the Figma↔Storybook crosslink (Tier 4). The internal POV may be collapsing these. Worth distinguishing: metadata *embedded in the design tool* vs. *embedded in code* vs. *external to both* (registry/.ai.json) vs. *crosslinks between tools* — these are four different surfaces with different update mechanics.

2. **Obello's "trust as production constraint" framing** is an extension — internal POV is mostly about quality/consistency. Obello adds compliance, indemnification, auditability, permissioning. This matters for enterprise client conversations and may need to enter the practice's POV explicitly.

3. **Figma's "AI as diagnostic data"** framing extends the maintenance phase. The practice's maintenance POV should incorporate logging where AI drifts, and using that telemetry to prioritize DS updates.

4. **Multi-brand governance — process layer.** The internal POV (composition-based brand extension, 5-dimension rubric) is technical. The Multi-brand source is process. Both are needed. The intake/qualification/testing process (9 + 4 + 10 + 7 steps) is well-articulated and should probably map into the practice's governance phase.

5. **Component qualification criteria (multi-brand)** — the four criteria (problem, differentiation, cross-brand reusability, accessibility) extend the internal POV's likely-implicit qualification heuristics. Worth making explicit.

### Tensions / challenges

1. **Figma's "blocks" framing vs. atomic decomposition.** Figma actively pushes higher-order blocks (cards, headers, carousels) as the unit AI works best with. The internal POV emphasizes composition primitives that *combine* into blocks. Both are right at different layers — but the practice should be clear that AI generates better from blocks AND that blocks should be composed from primitives. If the .ai.json registry only describes primitives, AI will struggle with layout. Fix: register both atomic *and* compositional units.

2. **Wolosin's "metadata as training data" claim** is stronger than what the internal POV typically claims. She is explicit: this is a labeled dataset for supervised learning. The internal POV stops at "AI uses metadata at inference time." If the practice wants to claim long-term advantage, the training-data framing is stronger but also more speculative — agencies can't realistically train models on per-client data unless they're at significant scale. Keep the framing but be careful with where it lands.

3. **Obello's "AI handles production, designers handle calibration"** is a stronger version of the role shift than what internal POV usually says. It's also vendor-narrative-flavored (Obello sells the platform that does this). Worth tracking the prediction but skeptical of timing — the role shift will be real but uneven and slow at most companies.

4. **Multi-brand source skips technical governance entirely.** The doc is purely process — no token architecture, no theme primitives + brand semantics split, no composition patterns for brand extension. The internal POV's technical governance fills a real gap in this source. Don't treat the multi-brand source as authoritative on technical multi-brand strategy.

5. **No source named the 5-dimension brand-alignment rubric or anything like it.** The closest is Obello's "brand rules" (logo, color, typography, tone, photography style) but Obello doesn't formalize evaluation of brand-alignment quality — only rule encoding. The internal rubric is novel relative to these sources.

---

## Notable verbatim quotes (with source + year)

### On DS as infrastructure
> "Design systems are no longer just projects, tools, frameworks, or even products — design systems are infrastructure." — Sam Anderson, Director of Design @ Intuit, Nov 2024

### On AI as a new consumer
> "We're seeing a shift where AI also becomes a consumer of the design system and designers and developers increasingly work with what AI produces." — Zoe Adelman, PM Figma, 2025

> "AI is becoming a real user of our systems. It doesn't care if a component is pretty; it cares if it's structured and labeled and can read, understand, and act on the intent behind it." — Diana Wolosin, Indeed, Jun 2025

> "You need to start treating your component architecture like an API — clear contracts, explicit inputs and outputs, and semantics that work for humans and machines alike." — Murphy Trueman, quoted by Wolosin, Jun 2025

### On context as multiplier
> "In the age of AI, design systems are a context coefficient — the clearer and more complete a system is, the more likely AI is to produce on-brand results." — Figma DS x AI, 2025

> "What many designers and developers can infer just from understanding the brand and the business as a whole, AI doesn't inherently know." — Zoe Adelman, Figma, 2025

> "Design decisions like how interface building blocks are defined, how components are wired, and how they're used represent the DNA of how a product is built and understood. There's a lot of buried treasure there. When models can tap into that structure, they can generate interfaces that align with the system out of the box." — Wayne Sun, Figma designer, 2025

### On the role shift
> "[Design systems] help make sure we don't all end up shipping the same generic UIs cobbled together from the same pool of AI-generated parts." — Ana Boyer, Figma Designer Advocate, 2025

> "Designers will set the rules in the tools by defining what 'on-brand' means, in systematic terms that AI can understand." — Obello State of AI Design 2026

> "The designer's taste becomes the calibration mechanism that makes the entire system work." — Obello State of AI Design 2026

### On metadata as training data
> "Metadata isn't busywork. It's training data for the future of design." — Diana Wolosin, Jun 2025

> "I'm not just building components. I'm building the foundation for intelligent systems." — Diana Wolosin, Jun 2025

### On product mindset
> "It doesn't matter how big or small, the most important part [of a design system] is treating it like a product. A design system won't succeed if it's just a thing. It should be a product with clear OKRs, a roadmap, customers, and output." — Samira Rahimi, Head of Platform Experience, Uber, 2025

### On trust as constraint
> "Trust isn't a secondary consideration when AI moves into production, it is now the main constraint to making production possible." — Obello State of AI Design 2026

### On governance
> "Governance is a critical factor determining whether they truly deliver on their promise of unified, consistent experiences across multiple brands while still allowing each brand's unique personality to shine." — Multi-Brand Governance, Apr 2025

### On the LLM constraint frame
> "LLMs make choices within the boundaries we give them, and this template helps us narrow those boundaries." — Cherin Yoo, LinkedIn Product Designer, 2025

---

## Topics for the gaps file

These surface in the external sources but are NOT yet adequately addressed in the internal practice docs (or are addressed implicitly and should be made explicit):

1. **Trust / governance / liability for AI-generated brand assets.** Obello Trend 2 is a full agenda the practice's POV mostly does not engage. Specifically: indemnification language for AI outputs, audit trails for brand-asset provenance, permissioning models for who can prompt vs. publish, brand-safety enforcement at output time.

2. **AI activity as diagnostic data — measurement framework.** Figma's framing of "logging where AI breaks rules or invents workarounds" implies a measurement layer. The practice's maintenance phase should specify: what to log, how to surface drift, how to feed it back into DS updates.

3. **Higher-order blocks vs. atomic primitives — both must be in the registry.** The internal POV likely emphasizes primitives. AI generation works better from blocks. Both layers should be registered with metadata. Make this explicit.

4. **Wolosin's per-component fields the internal `.ai.json` may not yet cover:**
   - `avoid_when` (negative selection)
   - `common_partners` (composition graph)
   - `trigger_keywords` (prompt → component mapping)
   - `generation_priority` (tiebreaker)
   These are concrete additions to the schema.

5. **Component qualification process (4-criterion + 9-step intake).** The multi-brand source's process layer is well-developed and may be missing or under-developed in the practice's governance docs.

6. **Multi-brand decision rules.** When does a client get centralized vs. hybrid vs. federated? The multi-brand source under-specifies this. The practice should articulate explicit decision rules.

7. **Tool fragmentation / vendor-survival risk.** Obello flags this but doesn't resolve it. Client recommendations need a stance: how does the practice handle the volatility of the AI tooling landscape? What are the bedrock vs. experimental tools in any client recommendation?

8. **Penpot and on-prem AI.** Underexplored across all sources. For regulated/government clients, the open-source path matters. Practice POV likely doesn't have a stance.

9. **"Designer trains the system" — the actual workflow.** Obello asserts this strongly but is vague on operational specifics. What does "training the system" look like day-to-day? Does it mean updating .ai.json files? Curating example sets? Adjusting AGENTS.md? Concrete day-in-the-life of a DS-team-member-as-trainer would extend the practice's POV usefully.

10. **AGENTS.md / CLAUDE.md remains undertheorized in design discourse.** Practice has an opportunity here: the instruction-file layer is the part of the AI stack the public DS discourse has not yet absorbed. This is a defensible POV differentiator but should be articulated more carefully — what goes in it, how does it relate to .ai.json, how does it version, who owns it.

11. **Brand-alignment rubric (5 dimensions).** No external source presents anything analogous. Either the rubric is genuinely novel and worth publishing, or it should be benchmarked against an analog the practice hasn't yet found. Worth a literature scan.

12. **Token architecture for multi-brand.** None of the sources gets this right. Primitive tokens + brand-semantic tokens + theme tokens — the layered approach — is the standard 2024-2025 pattern but is curiously absent from the multi-brand source. Practice should claim this clearly.

13. **Designer-tool dependency on Figma.** All AI-cluster sources are Figma-centric. If clients are on other tools (Sketch, XD, Penpot), the AI-readiness story changes. Practice should think through cross-tool AI-readiness.

14. **Prompt engineering as a DS-team skill.** Figma names this as essential. The practice may need a documented prompting-conventions artifact that ships alongside the DS for client teams.

15. **Wolosin's 4-tier metadata loop as a teaching frame.** This is a clearer pedagogical frame than the internal "4-layer stack" framing. Worth considering whether to adopt or remap.

---

## End notes

- Strongest single source: **Wolosin** for component metadata POV; **Figma DS x AI** for ecosystem framing; **Anderson** for thesis.
- Weakest source: the multi-brand governance doc — orthodox, useful for process language but misses both technical multi-brand patterns and AI entirely.
- Most over-claimed source: **Obello** — vendor-authored, useful trend framing, but Trend 3's confidence about role-shift timing should be discounted.
- Most useful for client conversations: **Figma DS x AI** because it speaks Figma's language and most clients live there.
- Most useful for the practice's forward POV: **Wolosin + Anderson** — together they articulate the "DS as infrastructure for intelligent systems" story.

# Notes: Foundational External Books (Atomic Design 2016 / Laying the Foundations 2019 / Hack the Design System 2019)

These three books are the canonical mid-2010s practitioner texts our internal vocabulary inherits from. They predate the modern token/Variables era but still define the language of "atoms/molecules/organisms," "foundations/components/patterns," and the consultancy framing of "philosophy + assets + tools." Read selectively for original framings, not for current best practice.

---

## Per-doc reading log

**Atomic Design — Brad Frost, 2016 — 6,567 lines**
Read: Front matter + Ch.1 "Designing Systems" (lines ~150–1280), Ch.2 "Atomic Design Methodology" (1280–2030) in full, Ch.3 "Tools of the Trade / Pattern Lab" (2030–2280, sampled), Ch.5 "Maintaining Design Systems" (4719–5500). Skimmed Ch.4 (workflow) via grep.
Summary: Frost argues the page metaphor has run its course; design systems must be built bottom-up from a finite set of UI primitives. The atoms→molecules→organisms→templates→pages taxonomy is offered as a *mental model*, not a folder structure or technical architecture. Chapter 5 is more durable than people remember — it covers governance, the maker/user relationship, deprecation, and the "make it official" pitch path.
Authority: HIGH for taxonomy and vocabulary (this is the source). MEDIUM for tooling (Pattern Lab era is over). LOW for tokens (barely mentioned). The book is canonical because the language won, not because the prescriptions are still all correct.

**Laying the Foundations — Andrew Couldwell, 2019 — 8,324 lines**
Read: Contents + Foreword (1–250), Ch.4 "Foundations Model" (2560–3010), Ch.8 "Systematising the design" — naming, colour, tokens (4750–5750), Ch.9 "Document everything" opening (5900–6300), Ch.11 "Maintaining" (7920–8120). Located audits content and MVP framing via grep.
Summary: Couldwell is a working practitioner (WeWork, Adobe Portfolio) writing in the voice of a senior IC. He proposes the "Foundations Model" — Foundations / Components / Patterns / Templates / Pages — as a friendlier, less metaphor-laden alternative to atomic design. The book is opinionated about naming (numeric scales, semantic over poetic), about tokens vs. Sass variables, and about the "guardian / ambassador / lead" governance model. Strong on documentation-as-you-go and audits.
Authority: HIGH for naming conventions, audits, and the foundations/components/patterns split (which our internal materials echo). HIGH for the human/diplomatic side of governance. MEDIUM-LOW for tooling (Sketch + Sass; pre-Figma-Variables, pre-W3C DTCG).

**Hack the Design System — Idean (in partnership with Adobe), 2019 — 5,560 lines**
Read: Intro + definitions (180–650), Governance & impact section (1340–1750), "Becoming part of everyday operations" + portfolio scope (2540–2940). Sampled the ABB and Adobe case studies.
Summary: A consultancy POV book — Idean is the agency, Adobe is the partner, and the case studies (ABB, IBM Carbon, AT&T, Dell, Mozilla, Crédit Agricole) are interview-driven. The framing is "two complementary approaches" (UX vs. Transformation) and "five stages" for both system curators and system makers. Heavy emphasis on people, change management, and the "trojan horse" cultural impact of a design system. Light on technical specifics; deliberately so.
Authority: MEDIUM as agency-comparable thinking — useful as a peer benchmark to VML's consultancy posture. LOW as a how-to. Best read for language to use with C-level stakeholders ("operating system for user experiences," "trojan horse for cultural change").

---

## Atomic Design (Frost, 2016) — key extractions

### The five-stage taxonomy verbatim

From Ch.2, summing it up in Frost's own words (p.55 / lines 1767–1777):

> - **Atoms** are UI elements that can't be broken down any further and serve as the elemental building blocks of an interface.
> - **Molecules** are collections of atoms that form relatively simple UI components.
> - **Organisms** are relatively complex components that form discrete sections of an interface.
> - **Templates** place components within a layout and demonstrate the design's underlying content structure.
> - **Pages** apply real content to templates and articulate variations to demonstrate the final UI and test the resilience of the design system.

The canonical example: a label atom + input atom + button atom = search-form molecule; that molecule + logo atom + nav molecule = header organism; that organism (and others) placed in layout = homepage template; layout + real content = page.

### Frost's reasoning — why the chemistry metaphor

- He needed names that *imply hierarchy*. "Components" and "modules" don't — they're flat. Atoms/molecules/organisms inherit a built-in mental sequence (line 1911–1914: "the issue with terms like components and modules is that a sense of hierarchy can't be deduced from the names alone").
- The metaphor surfaces a finite-set logic: just as all matter reduces to ~118 elements, all UIs reduce to a finite set of HTML primitives (he cites Josh Duck's "Periodic Table of HTML Elements").
- Atomic design is **a mental model, not a linear process**. He repeats this. "Atomic design is not a linear process, but rather a mental model to help us think of our user interfaces as both a cohesive whole and a collection of parts at the same time" (line 1429–1431).

### What Frost says the metaphor gets right

- The "part and the whole" duality — designers can zoom between abstract and concrete. He invokes Frank Chimero's painter-at-the-canvas image (lines 1803–1814).
- Clean separation between **structure (templates)** and **content (pages)**, while acknowledging they influence each other. Templates show "the design's underlying content structure rather than the page's final content" (lines 1643–1648). He quotes Mark Boulton: "You can create good experiences without knowing the content. What you can't do is create good experiences without knowing your content structure."

### Common misuses Frost calls out

- **Treating it as a linear process.** "Don't interpret the five stages of atomic design as 'Step 1: atoms; Step 2: molecules; …'" (lines 1843–1846).
- **Treating it as a CSS/JS architecture.** "Atomic design has nothing to do with web-specific subjects like CSS or JavaScript architecture" (lines 2000–2002). It is a UI-design mental model that applies equally to Instagram, Word, an ATM.
- **Treating the names as dogma.** He explicitly approves the GE team renaming the levels to "Principles, Basics, Components, Templates, Features, Applications" (lines 1923–1937) and adds: "the most important consideration is to establish naming and categorization that is most effective for your team."
- **Static deliverables.** He quotes Nathan Curtis: "A style guide is an artifact of design process. A design system is a living, funded product with a roadmap & backlog, serving an ecosystem" (lines 4743–4747).

### Frost on tokens

Almost nothing. The word "token" does not appear meaningfully in the atomic design book. Atoms in Frost's framing are **HTML elements** (button, input, label) — not design decisions like colour or spacing. The "subatomic" framing (treating colour/spacing tokens as below-atom) is a later VML/industry overlay onto Frost's vocabulary, not Frost's idea. This is important: when our internal materials use "subatomic" for tokens, that is a VML extension, not a Frost extension.

### Frost on documentation, governance, adoption

The maintenance chapter (Ch.5) is the most often-overlooked part of the book. Highlights:

**Make it official — the three-step adoption path** (lines 4933–4937):
1. Make a thing.
2. Show that it's useful.
3. Make it official.

**Ten qualities of a maintainable design system** (lines 4899–4908): Make it official / adaptable / maintainable / cross-disciplinary / approachable / visible / bigger / context-agnostic / contextual / last.

**Makers vs. users distinction** (lines 5009–5060): "The design system makers are the ones who create, maintain, and govern the system… The design system users are the teams across the organization who will take the system and employ its interface patterns to specific applications." He quotes Jina Bolton (Salesforce): "The Design System informs our Product Design. Our Product Design informs the Design System."

**Governance questions every team must answer** (lines 5223–5239) — modify / add / retire patterns, who approves, who docs, how to deploy, how people find out. Modification, addition, removal are the three change types.

**The "holy grail"** (lines 5396–5413): the pattern library and live applications stay perfectly in sync — change in one updates the other. He names Lonely Planet's Rizzo as an early implementation. (This is now table-stakes via Storybook + Code Connect, but in 2016 it was aspirational.)

### Notable quotes — Frost

- "We're not designing pages, we're designing systems of components." (line 566)
- "An artifact is something you'd find on an archaeological dig… A style guide can provide documentation… but the simple existence of a style guide doesn't guarantee long-term success for the underlying design system." (lines 4750–4760)
- "The biggest existential threat to any system is neglect." — Alex Schleifer, Airbnb (line 5379, quoted by Frost)
- "Ask forgiveness, not permission." (line 4922)
- "A successful design system needs to become part of an organization's DNA." (line 5114)

---

## Laying the Foundations (Couldwell, 2019) — key extractions

### The Foundations Model

Couldwell explicitly invents this as a friendlier alternative to atomic design (line 2560–2570: "While researching a design system model and terminology to use, I was confused by the many different terms — and jargon — I found… so I created my own!").

Five layers, bottom up:
1. **Foundations** — brand values, identity, typography, colour, icons, photography, illustration, tone of voice, formatting, accessibility, responsive grids, animation. Anything that holds across digital properties.
2. **Components** — small, distinctive UI elements: buttons, inputs, selects, toggles, avatars, tooltips. "There's rarely a need to reinvent the wheel" (line 2702).
3. **Patterns** — larger building blocks: navigation, footers, modals, cards, carousels, breadcrumbs. Often modular, often combining foundations + components.
4. **Templates** — for content-driven websites: consistent layouts populated with different content.
5. **Pages** — final application; either a template instance or a bespoke one-off.

For product design specifically, he swaps the top two layers to **Features** and **Screens**, with **User Journeys** mapping the multi-step flows (lines 2889–2960). This is one of the more useful insights — it explicitly recognises that product design needs different upper layers than marketing-site design.

### Decision rule: how many templates?

> "It's good practice to have as few templates as possible, so people can familiarise themselves with the interface as quickly as possible." (line 2810)

### Couldwell on naming conventions

His position is opinionated and nearly verbatim usable as policy:

- The name in the design library must match the name in the code must match the name in the documentation. (line 4806–4814)
- **Semantic > poetic.** "Title 1" through "Title 5" beats "Daisy" or "Yosemite" (line 4817). Names "need to make sense to more people than just you and your friends on your team."
- **Scalable naming.** "If you have a colour named 'Ocean Blue', what happens when you need to add a second blue?… You need a more semantic (i.e. logical) approach to naming." (lines 4853–4858)
- **Numeric scales for colour** following Material's lead. He proposes `$blue50` as base, `$blue60/70/80` darker, `$blue40/30/20` lighter, in 10% increments. He uses two digits ("50" not "5") explicitly so you can fit 5% half-steps (`$blue55`) later without breaking the scale (lines 5061–5074).
- Token/Sass-variable names should match between design and code. "I like to name colours (exactly) the same as they appear in the code, as Sass variables" (lines 5048–5049).

### Couldwell on tokens vs. Sass variables

This is one of the clearest pre-DTCG explanations of the *semantic vs. primitive* token split, even though he uses Sass variables as the primitive layer.

- **Sass variable = generic, reusable value.** `$white: #ffffff;` — used dozens of places, from text to SVG fills.
- **Design token = more specific, scoped to purpose.** `$color-background-light: #ffffff;` — only for backgrounds.
- The reason this matters (lines 5526–5547): if you want to change the site background to off-white, the design token is safe to repoint; the Sass variable is not, because changing `$white` would break text and icons too.
- His recommended pattern is **combine them** (line 5593+): primitive Sass variables hold raw values, semantic design tokens reference the primitives. `$color-background-light: $white;`. This is exactly the modern primitive→semantic two-tier model, just expressed in Sass.

He quotes Salesforce Lightning's definition (line 5405): "Design tokens are the visual design atoms of the design system — specifically, they are named entities that store visual design attributes."

### Couldwell on documentation

> "If a simple style guide is like a diagram of all the elements that make up a piece of IKEA furniture without the instructions telling you how to assemble them, you might build something that resembles the picture on the box, or you might create something entirely different." (lines 5911–5913, 6000–6008)

Decision rules verbatim:
- **Document as you go.** "Don't leave documentation until the end, or as an afterthought." (line 5974)
- **The guidelines are no good in your head.** "The guidelines and decisions you make when designing a system are no good just in your head. They shouldn't be communicated on a 'need to know' basis. Everybody needs to know." (lines 5969–5971, repeated as a pull-quote)
- **What to document, minimum**: do's & don'ts, colour, brand identity, typography, copywriting, components, patterns, "the small things," grid/layout/spacing, design tokens. (Ch.9 contents)
- For colour, document not only hex/name but **intent**: "Why did you choose these brand colours? When and why would you use X colour over Y colour?" (lines 6184–6186)
- He uses Adobe Portfolio as a *cautionary self-tale* — he didn't document, and the meaning behind components was lost (lines 6027–6125). Useful pitch ammunition.

### Couldwell on governance — Guardians, Ambassadors, Leaders

A clear three-tier model (Ch.11):

- **Design system lead** — single point of accountability. Responsibilities listed (lines 7971–7984): advocate, establish processes, ensure upkeep, educate, research new approaches, promote design+dev pairing, keep team engaged, deal with resistance, recruit specialists.
- **Dedicated design systems team** — freed from BAU; broad skill set including designer-developer hybrids, FE engineers, copywriters, animation specialists.
- **Ambassadors / guardians** — embedded in product teams. Cites Sprout Social's Ben Lister: "Our design system ambassadors are designers from across the organization that act as liaisons between their embedded teams and the design systems team. They are our eyes, ears, and voice across the company." (lines 8036–8043). Selection criterion: "we seek out people who are not only passionate about design systems but also those who are systems thinkers, willing to stand up for good design and advocate for best practices."

Governance posture: **"the goal is to educate, not enforce."** (line 7946) "People don't generally respond well to orders. Approach the management of a design system from a teaching and collaborating perspective, not as the ruling authority."

### Couldwell on MVPs and constraints

- Ship an MVP/beta as fast as possible (lines 4401–4402): "You might not get it right the first time, so consider getting to an MVP (minimum viable product) — or a beta launch phase — as fast as possible."
- "Constraints are not a bad thing" — recurring framing, especially around limited colour/text-style sets.

### Notable quotes — Couldwell

- "A building built on sand will only stand for so long. You need to lay strong foundations, before you build anything." (line 2596)
- "A design system is a marathon, not a sprint. They're never finished." (line 8072)
- He closes with a Linzi Berry (Lyft) quote that captures the human framing: "Systems design is not only scientific and meticulous, it's the mastery of interacting with people in a sensitive and effective way." (lines 8087–8093)

---

## Hack the Design System (Idean, 2019) — key extractions

### Idean's working definition

> "A design system is a living system of guidelines, reusable code and design assets, and tools that helps organizations deliver consistent, on-brand experiences at scale and over time." (lines 444–447)

A **comprehensive design system should contain** (line 466):
- Principles and main goals
- Brand identity assets
- Functional patterns (design + code)
- Guidelines (UX/UI/tech)
- Tools (UI Kit, pattern library, etc.)
- Examples and best practices

### Two complementary approaches (named framework)

The book's most useful explicit framework (lines 509–532):

- **The user-experience approach** — get latest shared assets to digital teams; create core foundation for design language; align/upskill teams on UX; measure adoption and end-user impact.
- **The transformation approach** — ensure the system becomes stable *and* agile; crystallise governance and comms strategy; align/upskill on behaviour and role changes; measure impact in light of broader transformation.

Idean's argument is that you usually need both: the UX approach gets you tactical wins, the transformation approach gets you durable change.

### The five stages (named framework)

Two parallel five-stage tracks (lines 604–649):

For **system curators**:
1. Researching and getting initial buy-in
2. Building solid starting points while testing them early and often
3. Ensuring early-stage adoption and growth
4. Broadening the scope and making it more stable
5. Balancing major releases and smaller updates

For **makers leveraging the system**:
1. First potential advocates and partner units engaged
2. Primary users learning the principles
3. Early successes raise interest, questions, suggestions, worries
4. Changes appear in more products
5. New initiatives roll in as time and energy free up

### Governance: "Make tools, not rules"

This is their central governance slogan (line 1365). The supporting bullets (lines 1368–1390):
- Philosophy and principles define a shared direction, not the solution.
- Shared components and styles need clear purpose and built-in flexibility.
- Documentation provides insights hard to derive from assets alone — but is "soon discarded if it doesn't serve the needs of busy practitioners."
- Discussions and hands-on practice are often more effective for onboarding than documentation alone.

### Consultant-led / agency POV

Idean is candid about being on the outside helping clients in. The case studies are framed around *journeys* — ABB's CommonUX, IBM Carbon, AT&T, Dell, Mozilla, Crédit Agricole — and the narrative is consistently "the system was the trojan horse for cultural change." Useful peer benchmark for VML positioning.

A telling caveat for consultants (line 402–410, Audrey Hacq, Idean Design Lead):

> "If the maturity of the organization is low, especially when it comes to collaboration within cross-functional, digital teams… Then the design system is not the main solution, or the only one."

That is the cleanest articulation we have from a peer agency that **a design system can't fix an organisation that isn't ready to collaborate** — and it's worth quoting in our discovery materials.

### Iterating ideas based on shared principles (workshop activity)

A six-step facilitator activity (lines 1465–1483) for keeping principles top-of-mind: take principles → one-page templates → "How might we…" reframings → keep questions short → leave space → make templates available with a quick-use guide. Practical workshop material we can borrow.

### Notable language

- "It's an operating system but for user experiences." — Jeoff Wilks, IBM Carbon (line 332)
- "It's a product that serves other products. It's an enabler for the organization." — Petri Heiskanen, Idean (line 341)
- "A design system is more powerful than it appears. It's like a trojan horse going into a big organization to ignite bigger cultural change." — Jordan Fisher, Idean (line 428)
- "It's not a magic glue that fixes everything." — Kevin van der Bijl, Idean (line 379)
- "A design system is not a thing you do and then move onto the next thing." — Nathan Mitchell, National Instruments (line 388)
- On scope: "Few design systems will cover 100% of live UI assets. Ownership of the journeys, as well as the more unique, advanced, and specialized assets, remain within the product teams." (lines 1755–1757)
- On versioning: "We would keep every historical version of the system available until all of our digital products have migrated to an updated version." — Josh Baron, Dell (line 2661)

---

## Cross-cutting themes across the three

**Where they agree:**

1. **A design system is a product, not a project / not an artifact.** Frost, Couldwell, and the Idean interviewees converge on this almost word-for-word. Frost quotes Curtis ("a system isn't a project with an end"), Couldwell calls it "a marathon, not a sprint," Idean says "it's not an end game."
2. **Governance and ongoing investment determine success, not the launch artifact.** All three spend their final chapters on this. Neglect kills systems.
3. **Naming matters and is hard.** All three spend real time on it. None pretends there's a single right answer; all three insist on consistency between design, code, and docs.
4. **Education over enforcement.** Couldwell makes it explicit ("educate, not enforce"); Idean encodes it as "make tools, not rules"; Frost frames makers/users as collaborators.
5. **Cross-disciplinary teams.** Frost's makers-and-users diagram, Couldwell's lead/team/ambassadors, Idean's curators+makers — same idea, different names.
6. **Start small, ship something, prove value, then go official.** Frost's three-step "make a thing / show it's useful / make it official"; Couldwell's MVP-first stance; Idean's "create one… those are the two metrics — acceleration and quality — that you need to move the needle on" (Wilks, IBM, lines 670–687).

**Where they diverge:**

1. **Taxonomy.** Frost: atoms/molecules/organisms/templates/pages, with chemistry hierarchy. Couldwell: foundations/components/patterns/templates/pages (or features/screens for products), explicitly rejecting chemistry. Idean: doesn't propose a taxonomy at all — just "principles + functional patterns + guidelines + tools + examples." This is a real divergence; our internal materials borrow Frost's *taxonomy* but Couldwell's *foundations* layer name.
2. **Tokens.** Frost: barely mentioned. Couldwell: extensive, opinionated, with a primitive→semantic two-tier Sass-variable model. Idean: tokens not central; emphasis is on people and process. Couldwell is the only one of the three who is genuinely useful on tokens — and even he is pre-W3C-DTCG and pre-Figma-Variables.
3. **Audience posture.** Frost writes for the design/dev practitioner who needs a model. Couldwell writes for the senior IC who needs to convince their team and run the work day to day. Idean writes for the design leader and the C-suite stakeholder. The three are complementary, not redundant.
4. **Tooling.** Frost: Pattern Lab. Couldwell: Sketch + Sass. Idean: agnostic, mostly process-focused. None of these tooling chapters has aged well.

---

## Phase-tagged findings (canonical 8 phases)

- **Discovery & Strategy** — Idean's "two approaches" framing (UX vs. Transformation) is directly usable as a discovery lens. Idean's caveat that a DS won't fix a non-collaborative org (Hacq quote) belongs in every discovery conversation. Frost's "make a thing / show it's useful / make it official" is the pitch path. Couldwell's Ch.2 on "selling a design system" and "office politics" is the practitioner counterpart.
- **Design Foundations** — Couldwell's Foundations layer is the most complete enumeration in the three (brand identity, typography, colour, icons, photography, illustration, tone of voice, formatting, accessibility, responsive grids, animation). His colour-system construction (numeric scale, primitive + semantic) is the load-bearing decision rule.
- **Component Library** — Frost's atom/molecule/organism distinction is the canonical mental model. Couldwell's Components/Patterns split is the cleaner working vocabulary (Frost's "molecule" vs. "organism" line is fuzzy in practice; Couldwell's "small actionable element" vs. "larger recurring block" is clearer). Frost on Russian-nesting-doll inclusion (Pattern Lab section, lines 2174–2200) still describes how component composition should work in any modern tool.
- **Documentation** — Couldwell Ch.9 is the strongest of the three: document-as-you-go, document intent not just appearance, IKEA-without-instructions analogy. Frost's style-guide chapter is more historical at this point. Idean's "make tools, not rules" reframes docs as a service to busy practitioners.
- **Development Support** — Couldwell's design-token + Sass-variable two-tier pattern is the most directly portable to modern tokens (just translate Sass to Variables/CSS-vars). Frost's "holy grail" framing (pattern library and production stay in sync) is now table-stakes. Idean's framing of "design+code in sync" as a marriage is good stakeholder language.
- **Pilot & Implementation** — Frost's "pick a project that would be a great pilot" (line 4944) is the canonical phrasing. Idean's case studies (esp. ABB's CommonUX, 14 months from creation) provide realistic timelines for enterprise pilots. Couldwell's MVP-first stance is the IC-level corollary.
- **Governance & Adoption** — Couldwell's lead / team / ambassadors model is directly usable. Frost's makers/users distinction and the three change types (modify / add / retire) are the right governance scaffolding. Idean's "make tools, not rules" is the slogan worth stealing.
- **Ongoing Maintenance** — Frost Ch.5 is still the most complete: deprecation strategies (Salesforce Sass Deprecate), rolling updates, "state of the union" meetings, decision trees for accepting new patterns (Canonical's Vanilla diagram). Couldwell's Ch.11 "diplomacy is as important as the pixels" framing is the leadership half.

---

## What has aged WELL vs. POORLY

**Aged well (still load-bearing):**
- Frost's atomic taxonomy as *vocabulary*. Even teams that don't fold their components by it use the words.
- Frost's makers/users distinction and Ch.5 governance/maintenance content.
- Couldwell's naming-convention rules (semantic, scalable, code-design parity).
- Couldwell's primitive→semantic token two-tier model — survives nearly verbatim into W3C DTCG / Figma Variables thinking.
- Couldwell's Guardians/Ambassadors/Lead governance roles — directly usable today.
- Idean's "make tools, not rules" governance posture.
- Idean's "two approaches" framing (UX vs. Transformation) for discovery conversations.
- Frost's "design system is a product, not an artifact" reframe (still the single most quoted line).

**Aged poorly (superseded):**
- **Pattern Lab** as the canonical tooling reference. It still exists, but Storybook + Code Connect + Figma Variables have replaced this stack for most teams.
- **Sketch + Sketch Library** as the design-tool assumption (Couldwell). Figma is now dominant.
- **Sass variables as the token primitive.** The W3C Design Tokens Community Group spec and tool-native variables (Figma Variables, CSS custom properties + style-dictionary) have superseded Sass-only thinking. Couldwell's *logic* survives; his *implementation* doesn't.
- **No mention of multi-brand / multi-mode theming.** All three books predate the modes/themes era. None discusses Figma Variables modes, dark/light parity, density modes, or tenant theming.
- **No AI.** Obviously. None of the three discuss AI-assisted component generation, AI-assisted documentation, or how an LLM-era team should structure a system. This is the single biggest gap.
- **Frost on tokens specifically.** The book essentially predates tokens as a first-class concern. "Subatomic" framings for tokens are post-Frost VML/industry overlays — useful, but don't attribute them to him.
- **Idean's case studies as evidence.** They're 5+ years old; the named systems (ABB CommonUX, etc.) have evolved. Cite the *patterns*, not the *snapshots*.
- **Front-end framework discussion.** Frost is pre-React-as-default; Couldwell is mid-Sketch-symbol era. The handoff/integration chapters should be read as historical.

---

## Notable verbatim quotes (with source + year)

- "A style guide is an artifact of design process. A design system is a living, funded product with a roadmap & backlog, serving an ecosystem." — Nathan Curtis, quoted in Frost, *Atomic Design*, 2016
- "We're not designing pages, we're designing systems of components." — Frost, *Atomic Design*, 2016
- "The biggest existential threat to any system is neglect." — Alex Schleifer (Airbnb), quoted in Frost, 2016
- "The Design System informs our Product Design. Our Product Design informs the Design System." — Jina Bolton (Salesforce), quoted in Frost, 2016
- "A building built on sand will only stand for so long. You need to lay strong foundations, before you build anything." — Couldwell, *Laying the Foundations*, 2019
- "The guidelines and decisions you make when designing a system are no good just in your head. They shouldn't be communicated on a 'need to know' basis. Everybody needs to know." — Couldwell, 2019
- "A simple style guide is like a diagram of all the elements that make up a piece of IKEA furniture without the instructions telling you how to assemble them." — Couldwell, 2019
- "The goal is to educate, not enforce." — Couldwell, 2019
- "A design system is a marathon, not a sprint." — Couldwell, 2019
- "Make tools, not rules." — Idean, *Hack the Design System*, 2019
- "It's an operating system but for user experiences." — Jeoff Wilks (IBM Carbon), in Idean, 2019
- "It's a product that serves other products. It's an enabler for the organization." — Petri Heiskanen (Idean SVP), 2019
- "It's like a trojan horse going into a big organization to ignite bigger cultural change." — Jordan Fisher (Idean), 2019
- "It's not a magic glue that fixes everything." — Kevin van der Bijl (Idean), 2019
- "If the maturity of the organization is low… then the design system is not the main solution, or the only one." — Audrey Hacq (Idean), 2019

---

## Topics for the gaps file

These are areas where the three foundational books are *thin or silent* and where post-2020 sources (Curtis, Wolosin, etc.) need to fill in:

1. **Tokens as a first-class layer.** Frost barely mentions them; Couldwell treats them as Sass variables; Idean leaves them implicit. The W3C DTCG spec, the primitive/semantic/component three-tier model, Figma Variables, mode/theme handling — all of this is post-2019. Anywhere our internal materials say "tokens are subatomic / the foundation," that's a *VML and Curtis-era* extension, not a Frost extension.
2. **Multi-brand and multi-mode theming.** None of the three engages with multi-tenant or multi-brand systems, or with dark/light/density modes as governance objects. Critical gap for VML's enterprise clients.
3. **AI-era workflows.** Generative components, AI-generated docs, MCP-driven design-to-code, code-connect-as-data — all post-book. Major gap.
4. **Component anatomy / props / API design.** Frost stops at "molecule/organism"; he doesn't discuss prop schemas, slot patterns, or component APIs. Couldwell doesn't either. The UIC series (anatomy, props, layout, composition) addresses this gap.
5. **Metrics and ROI.** Idean gestures at "acceleration and quality" as the two needles to move (Wilks/IBM); none of the three has a working metrics framework. Curtis and the 90-days/MVP/benchmark sources fill this in.
6. **Code Connect / design-to-code parity.** Frost's "holy grail" intuition is right but the mechanism is now Code Connect + Storybook + tool integrations, not Pattern Lab.
7. **Contribution workflow at scale.** The books outline the *idea* of distributed contribution but not the modern PR-based, tokens-as-data, lint-and-CI-gated contribution flow.
8. **Variable Modes for theming/density/responsive.** Couldwell's responsive thinking is grid-based; Figma Variables modes have changed how this is modelled.
9. **Accessibility as a governed token-level concern.** All three mention accessibility; none treats it as a token-contract concern (e.g., contrast pairs as enforceable token relationships).
10. **Documentation as queryable data.** All three treat docs as a website. Modern thinking treats components and tokens as data that *generates* docs. Frost's Pattern Lab nearly got there; the modern equivalent (Storybook autodocs, MDX, component metadata) goes further.

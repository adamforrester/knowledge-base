# Notes: Motion / Expression / Developer-focus

Three specialized sources rounding out the knowledge base on dimensions our internal POV under-articulates: motion as a primitive, the counter-argument to consistency-driven systems, and what developers actually require from a DS.

## Per-doc reading log

- **ext-animation.txt** (1058 lines, "Animation in Design Systems," Val Head, Adobe, 2019/2020) — read in full. Compact, opinionated practitioner book. Five chapters: case for motion, defining scope, motion principles, building blocks (durations / easings / properties), and "taking it further" (named effects, choreography, tokens).
- **ext-expressive.txt** (4426 lines, "Expressive Design Systems," Yesenia Perez-Cruz, A Book Apart, 2019/2021) — read in full. Five chapters: purpose & principles, process behind the system, communicating brand, making room for variation, managing systems. The book's title is somewhat misleading — it is *less* a frontal assault on consistency than I expected; it is really a book about how to bake brand expression *into* a system so it doesn't homogenize. The pushback is real but tempered.
- **ext-ds-developers.txt** (1942 lines, "Design Systems for Developers," Michael Mangialardi, Leanpub, 2021) — read in full. Twelve short chapters. Narrowly scoped: the entire book is essentially "how to build a token pipeline with Style Dictionary." It is more a tutorial than a comprehensive engineering treatise on DS, but the architectural pattern it advocates is exactly what most pitch decks gloss over.

## Animation in Design Systems (2020) — extract

### Frameworks for systematizing motion

Head's framework has three layers, layered top-down:

1. **Motion principles** — high-level "why" statements; how motion serves UX and brand. Examples: Microsoft Fluent's *physical / functional / continuous / contextual*. Adobe Spectrum's *purposeful / intuitive / seamless*. Audi: "movements in the Audi look have a typically dynamic character." A *good* motion principle is (a) something whose opposite you can articulate, and (b) objective enough to use in design review.
2. **Building blocks** — durations, easings, animatable properties. The "smart defaults" layer.
3. **Choreography / named effects** — only for systems that lean heavily on motion. Sequencing, overlapping action, paths.

Three sources for motion principles: extrapolate from existing global brand principles, derive from voice/tone guidelines, or surface from a **motion audit** of existing animations grouped by purpose.

### Token approach to motion

Head explicitly recommends tokens for motion building blocks:

- **Duration tokens** — Carbon and Lightning both publish them. Approaches range from minimal (Photon: one duration, one easing) to elaborate (Material breaks duration recommendations down by both complexity and area covered).
- **Easing tokens** — three custom curves cover most needs: ease-in (exits), ease-out (entrances), ease-in-out (point-to-point). Pluralsight pairs durations with named animals; Carbon distinguishes *productive motion* (utility tasks) from *expressive motion* (marketing/onboarding) — each has its own duration and easing scales.
- Best practice: define your own custom curves rather than using CSS defaults — this builds "motion equity" (Sarah Drasner). Penner easing equations are a good starting point.

Common best practices on duration: shorter for simple/small effects, longer for complex/large, optimal timing changes by viewport size.

### Where motion lives — global vs. component-level

Two patterns:
- **Global named effect library** — small, composable molecules of animation (Fluent web's library of named effects, Lightning's previous library). Each has a name, design token, code snippet.
- **Baked into components** — animation specs live inside component documentation rather than centrally.

Head warns against large effect libraries: "more isn't always better… every effect listed is more time and effort to maintain. Make any collection of named effects as small as you possibly can."

Choreography guidelines worth establishing if motion is heavy:
- Entrances should inform exits (spatial logic)
- Sequencing — when to start animations together vs. staggered
- Overlapping action / staggers — small delays per item create organic feel
- Paths of motion — straight vs. curved (Carbon: "Elements in Carbon dance on the grid. Motion paths trace lines along the grid which never run diagonally.")

### Motion study technique

To define brand-specific easing curves: pick three brand attribute words, animate simple shapes (circles) with fade / scale / point-to-point, experiment with easings until the vibe matches. Three attributes is the right number — enough to focus, few enough not to overwhelm.

### Common pitfalls

- Leaving motion out of the system entirely → designers either freelance it or skip animation for lack of time
- Using CSS defaults — gives you no brand differentiation
- Too many easing curves used arbitrarily across the product
- Building a huge named-effects library that becomes a maintenance burden
- Trying to ship a "perfect" v1 — Head explicitly recommends shipping v1 even if incomplete and iterating

### Notable verbatim quotes

> "Just like typography and color, the animation you use says something about your product and its personality. So, when it's not addressed in a design system, that area of UI design tooling is left unaccounted for."

> "A strong motion principle should be something that it's easy to say the opposite of."

> "It's amazing how much information we can convey in fractions of a second."

> Dan Mall, quoted: "This is the kind of thing a design system should have guidelines for: perspective, point of view, extending creative direction to everyone that decides to build something with the design system. That stuff should be baked in."

## Expressive Design Systems (2021) — extract

### The argument, in the author's own words

The frontal critique appears in the introduction. Perez-Cruz lists frustrations designers express with systems:

> "Rigid systems that stifle creativity. Monotonous systems that lead to generic, cookie-cutter experiences. Overly specific systems that can't be adapted to enough use cases. Complicated, unexplained, and unsupported systems that lead to fragmented user experiences."

Her resolution is not "abandon systems" but "build expressiveness into the system." She defines an expressive design system as having three properties:

> "**Purpose-built.** Your design system should align your team on a shared vision of your brand's voice, visual style, and behavior. **Support a range of expression.** Your design system should enable meaningful experimentation and divergence while still retaining the spirit of the system writ large. **Inspire use.** Designers should feel motivated to solve complex problems with their design system, rather than feeling constrained by it."

The book's strongest claim is the "unity vs. cohesion" distinction in Chapter 1:

> "Unity means that things feel complete — all of your brand elements work together as one. But unity doesn't guarantee cohesion. Cohesion is the quality that makes your user interfaces easy to understand across the experience… Unity is easier to accomplish than cohesion, because it can be solved by creating tools: style guides, brand languages, shared components. Cohesion is more complicated because it can't be solved with a tool alone."

This is the real critique: shipping a component library makes you *unified*, not *cohesive*. Unity is necessary but not sufficient.

### The "design systems homogenize everything" critique

It is more measured than the title suggests. Perez-Cruz never says "consistency is bad." She argues that:

1. Generic, broadly-applicable systems (Bootstrap-style) are appropriate when your goal is reach across thousands of unrelated teams. They are *not* appropriate when you want products that feel distinctly like *your* brand.
2. Component libraries built around visual primitives (button, accordion) homogenize because they describe *what* not *why*. Group components by **purpose**, not appearance (extending Alla Kholmatova's purpose-directed inventory).
3. Variation must be designed-in or teams will create their own systems "on the outskirts" (the Brasilia metaphor — a planned city that didn't scale because it didn't account for how real people behave).

### Three kinds of deviation

- **Unintentional divergence** — designers can't find what they need. Fix with documentation.
- **Intentional but unnecessary divergence** — designers don't want to feel constrained. Fix by making contribution easy.
- **Intentional, meaningful divergence** — *the goal of an expressive system.* Solves a user problem no existing pattern solves.

### Specific tactics for expressiveness

The book is most useful as a tactical manual for *where* and *how* to vary. Tactics:

1. **Component hierarchy with different rules at each level**: basic / composite / container / layout. Basic components must be functional and neutral (UI fonts at high x-heights, color used for attention). Composite components are where personality lives — display fonts, brand color, generous space. Containers control density. Layouts express the relationship between everything.
2. **Levers and dials.** Four global levers: **size, scale, density, weight**. These set the global feel. Dials are granular type sizes, spacing units, color hex values. *"If you define your dials but not your levers, you risk ending up with design choices that feel arbitrary."* Worked example: Vox vs. The Verge — same Vox Media token system, but different lever positions made them feel like different brands.
3. **Type / spacing / color trifecta.** Type scale via modular ratio. Spacing on a base unit (often 4px) with named intervals (numbered preferred over T-shirt sizes for scale). Color groups (light/dark/bright/muted) mapped to background contexts rather than 300 individual variables. (Lyft's 15 pinks story is the cautionary tale.)
4. **Theming via tokens, roles, values.** Tokens are codes (`$text`). Roles are systematic usage ("primary text color"). Values vary by theme. Theming dials only (color) is simple; theming levers (type + space + color) requires three coordinated density scales (compact / default / loose) — see the Gmail density precedent.
5. **Variation contexts: brand, audience, environment.** Vox newsletter modules were unnecessary variation (purely visual difference, same purpose). Vox/Verge masthead was meaningful variation (allowed brand art-direction). Airbnb Plus vs. standard pulls density/weight levers for premium feel. Shopify POS in Polaris dark mode is environmental (retail lighting, arm's length, eyes-closed mastery).
6. **Signature patterns.** Paula Scher Public Theater approach — keep core identity, vary by season. Don't try to be expressive everywhere; pick a small number of high-leverage components where variation is meaningful.

### How this should interact with our internal POV

Our internal POV emphasizes consistency, scale, reuse. Reading this against that:

- **Compatible.** Perez-Cruz is not anti-consistency. She accepts the standard benefits (faster builds, better products, scalability, focus). She is anti the *failure mode* where a DS becomes a generic UI kit that flattens brand identity.
- **What we under-articulate.**
  - Purpose-grouped inventories (vs. visual). Our pitches default to component taxonomy.
  - "Levers and dials" as a vocabulary for global vs. granular decision-making. We don't have language for this.
  - Variation as a *first-class system feature* rather than an exception. Our slides treat variation as risk.
  - Cohesion vs. unity distinction. We routinely conflate the two.
- **Where to push back.** Her argument applies most cleanly to consumer brands with strong identity stakes (Vox/Verge, Airbnb, Shopify Polaris). For internal tools, B2B SaaS, or compliance-driven products, "expressive" can be a distraction from utility. Our work spans both kinds of clients — the POV needs to flex by context, not just preach expressiveness.
- **Risk of misreading.** Junior designers read this book as permission to override the system. The book is actually saying: *don't override; build the override path into the system itself*, with governance.

### Notable verbatim quotes

> "When you create a design system, you're not just creating reusable patterns — you're operationalizing how your company approaches design."

> "The human aspects of your system are more complicated than the tooling. Many of the conversations around design systems focus on tooling problems… Spend more time on creating a shared language and less time on tools."

> "If you don't plan your system well, people will start creating their own systems on the outskirts."

> "Your design system is your pantry, not your cookbook. You have space to create your own recipe… but you won't switch to an entirely different cuisine because you won't have those ingredients."

> "Borders contain the greatest sources of diversity and creativity. Pay attention to the borders of your design system."

> "Systems aren't neutral. Systems reflect the values of the people who make the system." (Closing — used to argue that segregated systems like Levittown are a cautionary tale for who gets to contribute to and benefit from a DS.)

> Christopher Alexander, quoted: "Patterns stay alive because the people who are using them are also testing them."

> Gall's law, quoted: "A complex system that works is invariably found to have evolved from a simple system that worked. A complex system designed from scratch never works and cannot be patched up to make it work."

> Stewart Brand, quoted (on building layers / pace layering applied to systems): "A building properly conceived is several layers of longevity of built components." → Perez-Cruz applies this to DS layers (principles change rarely; tokens change often).

### Governance models (drawn from Nathan Curtis & Jina Anne, summarized in Ch. 5)

- Solitary — one team, own needs
- Centralized — single team produces, others consume
- Federated — multiple product teams co-decide
- Cyclical — centralized core + product team contributions (the recommended model, but hard)

Plus the "ambassadors" pattern (Sprout Social, Etsy, GOV.UK working group) — designers embedded in product teams who liaise with the systems team.

## Design Systems for Developers (2022) — extract

### What developers actually need

Mangialardi frames the problem from the developer's seat as four difficulties:

1. The system has to **scale** as more apps are added.
2. It has to be **consumable across platforms and frameworks** (web, mobile, desktop; React, Vue, Angular).
3. It has to be **flexible** when designers update specs.
4. The implementation has to be **high-fidelity** to the design source of truth.

The naive failure mode: the DS gets encapsulated as a React component library; then a Vue app appears, then a plain-HTML marketing page, then a Java mobile app. Each generation of consumer creates its own representation of the design specs in code, and there is no longer a single source of truth.

### Build pipeline architecture (the book's central recommendation)

```
Design files (Figma/Sketch)
    ↓ extract (manual or via plugins like Figmagic / Specify)
Design tokens (key-value pairs in JSON)
    ↓ Style Dictionary (or equivalent)
Platform deliverables (CSS, SCSS, JS module, iOS, Android, Tailwind theme...)
    ↓ delivery (GitHub Actions, CLI, API, or npm package)
Consuming applications
```

The **style dictionary** is "a central management system for design tokens" — the source of truth in code. Mangialardi specifically endorses Amazon's `style-dictionary` npm package as the de facto tool. Token JSON gets transformed into per-platform deliverables on every build.

### Code-side token integration

Two tiers of tokens:
- **Simple tokens** — enumerated valid values (colors, type sizes, spacing). e.g. `color.primary`, `spacing.4`.
- **Composed / component tokens** — context-specific compositions referencing simple tokens. e.g. `component.button.primary.background.color`.

Naming guidance (drawing on Nathan Curtis's "Naming Tokens in Design Systems"):
- Levels in a token name fall into four groups: **base** (category, concept, property), **modifier** (variant, state, scale, mode), **object** (component, element, group), **namespace** (system, theme, domain).
- Order: namespace → object → base → modifier.
- Be clear but brief; don't include defaults (`component.button.color.primary.default.light` is wrong if `default` and `light` are defaults).
- No official W3C standard exists yet (W3C Design Tokens Community Group is in progress). Each org defines its own tokenized language — collaboration between designers and developers.

The **manual extraction approach** is pedagogically preferred over automation early on: it forces designer-developer conversation and creates the equivalent of an API contract.

Color values: use whatever the design files use (HEX/RGB/HSL); Style Dictionary can transform between them at build time. Line height should usually be unitless. Scalable elements (font, spacing) should use rem; non-scalable (border, shadow) px.

### Component API design

Mangialardi recommends **headless UI components** (per Tailwind Labs' Headless UI project) over fully styled libraries:

- Encapsulate functionality in framework-specific (React, Vue) plain unstyled components
- Apply transformed design tokens via styling layer of each consumer's choice (styled-components, Tailwind, CSS-in-JS, etc.)
- Decoupling functionality from styling means the UI library can outlive any single design language

He criticizes Material UI for the opposite reason: tightly coupled functionality and styling means consumers spend energy undoing Material defaults to apply their own brand.

### Delivery options (with tradeoffs)

1. **npm package** — simple but defeats the cross-platform purpose; only works for JS consumers.
2. **API endpoint** — consumers fetch deliverables; needs notification or polling.
3. **CLI** — same downsides as API.
4. **GitHub Actions copying deliverables to consumer repos** — *his recommendation.* On every token build, a workflow copies the relevant platform file to every consuming repo via the `andstor/copycat-action` step. Each consumer gets one parallel job in the workflow. New consumer = new job entry.

### Storybook usage

Notably absent. The book never discusses Storybook, visual regression, Chromatic, or testing strategies in depth. This is a gap.

### Testing strategies

Also notably absent. The book does not address:
- Visual regression testing
- Component-level unit/integration tests
- Accessibility testing in CI
- Token drift detection between Figma and code

### Documentation that engineers value

He recommends a `docs/` directory with Markdown for: onboarding designers to GitHub, meeting notes (`docs/meeting-notes/`), decision logs (`docs/decisions/` — basically lightweight ADRs for design system choices like "we chose flat token keys over CTI hierarchy because…"). The DS repo itself doubles as the documentation site.

### Notable verbatim quotes

> "Design tokens are simply a name, or label, for the design specifications you represent in code."

> "We have a label for the single place where we store our design tokens, build platform deliverables, and ship those deliverables to consuming applications. We may call it a style dictionary."

> "Having a style dictionary is similar to having API contracts… as design tokens are being added and updated in the style dictionary, you are essentially establishing a contract once those changes are merged into the main branch."

> "Without the solid foundation of a style dictionary, creating platform and technology-specific tools can lead to problems. However, with a solid foundation of a style dictionary, which can transform raw design tokens into deliverables for any given platform, building technology-specific tools/assets carries little risk and much reward."

## Phase-tagged findings (canonical 8 phases)

### Design Foundations
- **Motion as a foundation primitive.** Tokens for duration and easing belong alongside color, typography, space. Three custom easing curves (in / out / in-out) is the minimum viable system. Productive vs. expressive motion split (Carbon) maps neatly to "consistency vs. expression" tension.
- **Levers and dials vocabulary** for foundations: size, scale, density, weight as global levers; type/space/color values as granular dials.
- **Color as groups, not variables.** Define foreground roles per background context, not 300 individual color tokens.
- **Type scale via modular ratio**, not handpicked sizes.
- **Spacing scale on base 4px unit**, named numerically for extensibility.

### Component Library
- **Group components by purpose, not appearance** (Kholmatova, applied via Perez-Cruz). Two cards that look similar may serve different purposes; consolidate by problem, not visual similarity.
- **Component hierarchy** (basic / composite / container / layout) with different brand expression rules at each level. Basic = functional/neutral. Composite = expressive. Container = density. Layout = relationships.
- **Motion lives at component level when component-specific**, in a global named-effect library when reused across components.
- **Component tokens vs. simple tokens** distinction for code-side organization.
- **Headless UI** as architectural pattern for cross-framework component libraries.
- **Choreography guidelines** for components that animate (entrances inform exits, sequencing rules, paths).

### Development Support (bulk of Mangialardi)
- **Token pipeline architecture** (Figma → JSON → Style Dictionary → platform deliverables → consumers).
- **Style Dictionary** as the canonical tool. Custom transforms and formats when defaults don't fit.
- **Naming taxonomy** (Curtis) — namespace / object / base / modifier.
- **GitHub Actions delivery** as recommended distribution mechanism.
- **Decision logs (ADRs) and meeting notes in repo** as documentation pattern.
- **Headless component libraries** vs. opinionated ones.
- **Token contracts** as analog to API contracts — version-controlled, code-reviewed.

### Governance
- **Cyclical governance model** (Curtis/Anne) — centralized + contribution.
- **Ambassadors program** (Sprout Social, Etsy, GOV.UK) — embedded systems thinkers in product teams.
- **Variation policy** — three deviation categories (unintentional / unnecessary / meaningful) and how to handle each.
- **Contribution criteria** (GOV.UK example) — patterns must be useful for several teams and not duplicate existing patterns.

### Brand
- **Brand expression at every component level**, not as a skin on top.
- **Signature patterns** (Public Theater seasons; Verge masthead) over uniform application.
- **Brand attributes drive easing curves** (motion-as-brand-voice).

### Process & Planning
- **Ecosystem mapping** before component work.
- **Purpose-directed inventory** alongside visual inventory.
- **Motion audit** as a specific kind of inventory — capture all existing animations, group by purpose, identify trends.

### Adoption & Measurement
- **Scorecard testing** for consuming applications post-adoption (Mangialardi).
- **Border behavior analysis** — watch where teams combine system elements with custom styles; that's where the system needs to grow (Perez-Cruz, citing Donella Meadows).

## Tensions surfaced

### Consistency vs. expression
The defining tension Perez-Cruz raises. Consistency is necessary but not sufficient (it produces unity, not cohesion). Pushed too far, it produces homogeneity that erodes brand identity. Resolution: build expressiveness *into* the system (component hierarchy, levers, theming, signature patterns). Don't let teams override; let the system flex. The tension does not resolve cleanly — for B2B/utility products consistency wins; for brand-led consumer products expression wins; most clients are somewhere in between.

### Designer-centric vs. developer-centric DS
Perez-Cruz writes for designers. Mangialardi writes for engineers. Their books barely overlap in vocabulary. Perez-Cruz's "tokens, roles, values" theming model is the same architecture as Mangialardi's "design tokens → style dictionary → platform deliverables" but they don't read each other. Our internal POV needs to translate between these vocabularies — a single token set has both a brand-expression face (levers, theming, harmony) and an engineering face (Style Dictionary config, GitHub Actions delivery, semantic naming).

### Manual extraction vs. automation
Mangialardi explicitly chooses manual extraction over Figma plugins (Figmagic, Specify) because manual forces collaboration and the team's own naming convention. The cost: scale. For a fast-moving DS this becomes the bottleneck. Automation tools (Specify, Tokens Studio, Figma Variables → Style Dictionary) have matured since 2021. Worth a fresh look.

### Generic vs. branded
Bootstrap-level genericness is appropriate for tools used by thousands of unrelated teams. Branded components are appropriate for tools used by one organization's products. Choose deliberately. Most internal DS efforts default toward Bootstrap-style genericness because it's safer, then wonder why nothing feels distinct.

### Tooling vs. shared language
Perez-Cruz: "Spend more time on creating a shared language and less time on tools." Mangialardi: spends 60 pages on tools. Both are right in their context — but the order matters. Without a shared language about levers, purpose, hierarchy, the tooling encodes confused thinking and scales it.

## Notable verbatim quotes (consolidated, with source + year)

- "Just like typography and color, the animation you use says something about your product and its personality." — Val Head, *Animation in Design Systems*, 2020
- "A strong motion principle should be something that it's easy to say the opposite of." — Head, 2020
- "Unity is easier to accomplish than cohesion, because it can be solved by creating tools." — Yesenia Perez-Cruz, *Expressive Design Systems*, 2021
- "Spend more time on creating a shared language and less time on tools." — Perez-Cruz, 2021
- "If you don't plan your system well, people will start creating their own systems on the outskirts." — Perez-Cruz, 2021
- "Your design system is your pantry, not your cookbook." — Perez-Cruz, 2021
- "Borders contain the greatest sources of diversity and creativity. Pay attention to the borders of your design system." — Perez-Cruz, 2021
- "Systems aren't neutral. Systems reflect the values of the people who make the system." — Perez-Cruz, 2021
- "Design tokens are simply a name, or label, for the design specifications you represent in code." — Michael Mangialardi, *Design Systems for Developers*, 2021
- "Having a style dictionary is similar to having API contracts." — Mangialardi, 2021

## Topics for the gaps file

- **Motion as a foundation primitive.** Our pitches treat color/type/space as foundations and stop. Motion deserves the same treatment: principles, tokens (durations, easings), three custom easing curves at minimum, productive/expressive split for orgs that need both. We have no language for this in current decks.
- **Choreography guidelines** for systems with non-trivial motion. Sequencing, overlapping action, paths, entrances-inform-exits.
- **Levers and dials vocabulary.** We don't have a clean way to talk about global vs. granular decisions. Adopting Perez-Cruz's *size / scale / density / weight* as named levers would give pitch decks shared language for "feel."
- **Unity vs. cohesion distinction.** Worth working into our framing. "We can ship you unity in 8 weeks; cohesion takes longer and requires alignment work." Useful expectation-setting.
- **Purpose-directed inventories** as a first-class artifact alongside visual inventories. We default to button/card taxonomies.
- **Variation as a designed-in feature.** Three deviation categories (unintentional / unnecessary / meaningful) and the policy for each. Theming via tokens-roles-values.
- **Code-side token pipeline architecture** (the Mangialardi diagram). Most of our pitches show "tokens" as a Figma-side concern and don't articulate how they reach engineers across multiple frameworks. Style Dictionary, naming taxonomy, GitHub Actions delivery, decision logs — these are concrete engineering deliverables we should articulate.
- **Headless component pattern** as architectural choice for multi-framework orgs. Worth a slide.
- **Token naming conventions (Curtis taxonomy):** namespace / object / base / modifier — adopt as default, document the overrides.
- **Decision logs / ADRs for DS choices.** Lightweight pattern; almost no client has it. Easy win.
- **Ambassadors program** as governance pattern — under-articulated alongside our usual "centralized vs. federated" framing.
- **Border behavior analysis** as ongoing measurement — watching where teams diverge from the system tells you where it needs to grow. Different from compliance auditing.
- **Brand-attribute-driven motion studies** — small workshop-able exercise that gives motion a defensible brand identity in 1–2 sessions.
- **Productive vs. expressive motion split** (Carbon model). Maps directly to the consistency-vs-expression tension and could be a useful frame in client work.
- **What we don't yet say about engineering testing.** Mangialardi *also* doesn't cover visual regression, accessibility CI, or token drift detection — and neither do we. This is a gap in the published literature, not just our pitches.

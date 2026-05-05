# Notes: Nathan Curtis trio (Components as Data, Design Tokens, Workshop)

## Per-doc reading log

**1. ext-curtis-components-as-data.txt** — "Components as Data: How to define components independent of platforms to scale a system's impact." Sep 23, 2025. ~424 lines. Read in full. A short essay/manifesto in which Curtis describes representing UI components as platform-neutral structured data (YAML/JSON) — anatomy, props, styles, variants — so they flow into Figma, code generation, docs, AI tooling, and version control. The Pill component bookends the piece (he wrote about it for tokens almost a decade ago; his team now refactors it again, this time as data). Tone: architect-at-heart, AI-era, "Figma assets as output not input."

**2. ext-curtis-tokens.txt** — "Design tokens" workshop deck, Directed Edges LLC, Nov 2024. ~2451 lines. Read in full (chunks). A long instructional deck that systematically walks Foundations -> About tokens -> Generic tokens -> Semantic tokens -> Composite tokens -> Theming -> Component tokens -> Process. Curtis's canonical three-tier token taxonomy (Generic / Semantic / Component) is presented here with naming conventions, calculation rules, theming dimensions (mode, brand, density, generation, white-label), and a workshop-driven token process (Plan -> Discovery -> Decide -> Automation).

**3. ext-curtis-workshop.txt** — "Operating Design Systems," Curtis Day 1+2 workshop, prepared Oct 2021, presented Sep 2023. ~5518 lines. Read in 2000-line chunks (1-2000, 2000-4000, 4000-end skim). The two-day operating curriculum: Defining systems, Planning, People (team models), Communications, Features step-by-step, Process, Contributions, Systems of Systems (tiers), and Measuring Success. Heavy on operational frameworks — initiative types, team-model stages, contribution scale, library tiers.

## Curtis's overall framework / worldview

A handful of theses recur across all three documents:

1. **A design system is a product, not a project.** "A style guide is an artifact of design process. A design system is a living, funded product with a roadmap & backlog, serving an ecosystem." (Workshop) The system must be operated — staffed, planned, communicated, measured — not delivered once.

2. **Structure beats artifact.** Across tokens (named decisions), components (data definitions), and operations (initiatives, milestones), Curtis insists on naming, taxonomy, and structured data over ad-hoc artifacts. The 2025 Components-as-Data essay is the maturation of the same instinct that drove his 2016 token writing: make decisions explicit, named, machine-readable.

3. **Central + Federated, in stages.** Solitary -> Central -> Federated. "Start with core group ... Then gradually grow ... to engage a community." Overlords don't scale; pure federation is chaos. The right answer is staged.

4. **Promote across, only when reuse exists.** "Start within, then promote across" (tokens). YAGNI as governance principle ("Avoid premature optimization"). Don't pollute shared namespaces with one-team needs.

5. **Specificity over abstraction when it matters.** Curtis is suspicious of over-genericized naming (e.g., generic-only color systems that obscure intent). He favors purposeful, semantic naming and component-specific tokens when theming demands it.

6. **Designer as architect, less as point-and-clicker.** The 2025 essay explicitly: "designers are increasingly focusing on architecture more and pointing and clicking and dragging and setting values in the Figma UI less."

7. **Operational rituals matter as much as artifacts.** Workshop spends as much time on standups, demos, sprint reviews, communications channels, and praise patterns as on components.

## Components as Data (2025) — extract in detail

### The thesis (verbatim)
> "A component definition in data is a structured description of a UI component expressed in a neutral format (like YAML or JSON) instead of hard-coded in design tools or platform-specific code. Data breaks a component into parts like an anatomy of elements, props, styles, layout and how each varies when configurations change."

> "These days, I live much more in a text editor than a UI to plan, design, validate and deliver components as data with AI at my side."

### The shape of "component as data"
Curtis prescribes the following top-level structure per component (illustrated with the Pill):

```
{component name}:
  anatomy:
    {element name}: { type: container | slot | text | ... }
  props:
    {property name}: { type, default, enum/oneOf, nullable }
  default:
    {element name}:
      styles:
        {style name}: {style value or token reference}
  variants:
    - configuration: { {prop}: {non-default value} }
      elements:
        {element name}:
          styles:
            {style name}: {style value}
```

Anatomy element types include: `container`, `slot`, `text`. Props are typed as `boolean`, `string`/`enum`, or `slot` (with `nullable: true` and `oneOf` enumerations).

Styles mix raw values (e.g., `4`, `HUG`) with token references (e.g., `foundations/size/8x`, `foundations/color/surface/primary`). The root element's styles capture Figma-equivalent properties: `height`, `backgroundColor`, `borderColor`, `borderWeight`, `verticalAlign`, `itemSpacing`, `paddingLeft/Right`, `layoutDirection`, `layoutSizingHorizontal`, `cornerRadius`.

Variants are expressed as overrides keyed by a `configuration` (the prop combination) and a list of `elements` whose `styles` change.

### Scale benchmarks
- "Simple components (Divider) may only need 20–50 lines of data."
- "Sophisticated core components like Alert, Text Input or Card often require 500 lines or more."
- "A core.yaml file ... may include 30–50 components ... and be 10,000s lines long."
- "Want to store a component per file? Sure ... You decide."

### Relationship to AI-readiness, registries, metadata
- "AI is everywhere, and it favors structured data. So express components that way."
- LLMs can answer questions, compare implementations, propose improvements via prompts.
- Caveat on Figma's Dev Mode MCP: "that's a stochastic, incomplete, and imprecise component description biased towards one platform (like React) and framework (like Tailwind)."
- Component data enables: code generation across platforms, Figma asset generation (Figma as **output, not input**), automated examples/docs, version control over time, catalog-wide analysis ("Are accessibilityLabels applied across all potential cases?")

### Specific rules / decisions / opinions
- **Figma is one target among many.** Component definitions live independent of any platform.
- **Every raw value in a variant is a code smell** unless it's clearly intentional. Example callout: `backgroundColor: #045bbc ## Seriously? Token please!`
- **Some things data still can't capture well:** binding configurations to element values; motion / non-trivial interaction (Figma reactions are rarely used); accessibility (Figma is structurally weak); non-visual configs (Alert autohide duration, TextArea maxRows). Teams pair component data with unstructured handoff docs "for now, anyway."
- **Vocabulary must level up:** layoutSizingVertical implied by setting height; nullability; slots vs INSTANCE_SWAP; Boolean visibility props.
- **Designers should architect, not click.** "We may go back and forth between Figma and data ... but designers are increasingly focusing on architecture more."

### Notable quotes
- "It's as if the Pill offers us a choice: to see the truth of our explicit decisions, or stay in an illusion that manual handoffs and divergent tools carry our intentions ... without failure."
- "Tokens feels quaint by comparison."
- "Chats evoke nullability. We're overdosing on overloading."
- "Soon to be gone are the tedious, manual hours to produce countless variants."
- "It's difficult to imagine returning to a time when I architected components only in a visual tool like Figma."

## Design Tokens (Nov 2024) — extract in detail

### Token taxonomy / tiers

Curtis's canonical taxonomy is three-tier, expanding to four when you count themed variants:

| Tier | Definition (verbatim) | Also Known As |
|---|---|---|
| **Generic** | "A value available for use that lacks specific intent or purpose." | Option, Choice, Reference (Material) |
| **Semantic** | "A token imbued with purposeful intent reusable across 2+ components." | Decision, System (Material) |
| **Component** | "A token used for only one component to support an attribute that varies by theme and is not already supported by a semantic token." | — |
| **Composite** | "A token whose value follows a predefined structure of values either explicit or references to other tokens." | (used for shadow, border, typography) |

He maps tier specifically to theming layers (Theme Palette / Theme Mapping / Component mapping), citing Brad Frost's "many faces of themeable design systems."

### Token "levels" (compositional structure)

Curtis decomposes a token name like `ds-color-text-primary-on_dark` into **levels**:
- **system** (`ds`)
- **category** (`color`)
- **property** (`text`)
- **variant** (`primary`)
- **mode** (`on_dark`)

Full level-type catalog he names:
- `system` (top-level namespace, e.g., `slds`, `mds`)
- `Theme` (palette or product line, e.g., `seafoam`, `courtyard`)
- `Domain` (business unit, `consumer`, `marketing`)
- `Group` (related-component organizing, `forms`, `layered`)
- `Component` (specific component, `button`, `icon`, `card`)
- `Element` (element of component, `title`, `action`, `image`)
- `category` (color, font, space)
- `concept` (feedback, heading)
- `property` (background, size, padding)
- `variant` (red vs blue, error vs success)
- `state` (default, hover, disabled)
- `scale` (16, 2x, half-x, 300)
- `mode` (light, dark)

### Naming conventions

Curtis surveys the industry's naming for the foundation layer ("Base / Core / Design / Foundation / Fundamentals / Visual Language") and notes Foundation is the most common (Material, Atlassian, Spectrum, Polaris, Primer).

For colors, three approaches with explicit tradeoffs:
- **Increment value** (`neutral-900`) — less resilient to new stops between the 100s
- **Computed value** (`neutral-94`) — better for aligning stops across hues; enables adding stops as needed
- **Named stops** (`neutral-arctic`) — only viable for already-named brand colors

For font sizes, three options: TShirt (`xl`, `l`, `m`), Increment (`9`, `8`...), Step from initial (`600`, `500`...). He flags it explicitly as "opinions in naming."

For spacing: TShirt vs Step vs Proportion (`0_5x`, `1x`, `1_25x`). He notes that proportion approach (with a magic number, usually 16, 8, or 4) handles "between sizes" cleanly, where TShirt and increment do not.

### Naming principles (named verbatim)
- **"Avoid homonyms"** — Avoid terms in token levels that can be interpreted in different ways (e.g., `display` is ambiguous).
- **"Balance flexibility and specificity"** — generics favor composition, semantics favor reuse across contexts. "You can offer both."
- **"Avoid premature optimization"** — also known as **YAGNI**. "Avoid polluting a shared namespace with options relevant to few or one team, especially unstable options." Decision rule: needed by 1 team? Don't add to "Core." Needed by 7+ teams across 3+ business groups? Add it.
- **"Start within, then promote across"** — for component tokens. Don't manufacture a semantic token until 2+ components share the concept.

### Tokens vs Variables (a Curtis matrix)

| | Tokens | Variables |
|---|---|---|
| WHAT | Available in many formats | Available in one format |
| WHERE | Shared from central place | Stored in local place of one team |
| WHY | Reuse by all teams | Reuse by one team |
| WHEN | Versioned independently | Embedded in a team's evolving work |
| HOW | Named deliberately, for scale | Often named chaotically, as needed |

This is a critical distinction in his POV: Figma variables are not tokens unless treated with the discipline tokens require.

### Categories (the standard menu)
`color`, `font`, `space`, `shape` (radius), `breakpoints` (media_query), `elevation` (z_index), `opacity`, `shadow` (composite), `time` (motion). Color/font/space are most common; time is "less common."

### Theming dimensions (purpose × cost)
Curtis enumerates theming purposes against potential cost:
- **Responsiveness** (mobile/tablet/desktop)
- **Light and dark mode**
- **Multi-brand** (white-label-adjacent)
- **Campaigns** (extending brand for marketing)
- **Design generations** (legacy alongside latest, e.g., `DS2_0` vs `DS3_0`)
- **White label** (extensive customization at any decision level)
- **Density** (compact / cozy / comfortable)

All show ascending cost from low to high. Strategy guidance: "Define the customer problems, and work back from there."

### Surfaces and theme inheritance
- **Surface** definition: "A container that applies color and more to composed elements and components to ensure clear, accessible and legible color contrast against a set background."
- "Most core UI components like even buttons and notifications inherit a surface mode from a parent and are not themed individually."
- Theming applied via Page -> Tile -> Row scopes (containers).
- Technical approach: **prop** (object-level) vs **inherited** (parent/ThemeProvider/Mode).

### Composite tokens (typography)
DTCG-aligned typography composite includes `fontFamily`, `fontSize`, `fontWeight`, `letterSpacing`, `lineHeight`. He shows DTCG `$type: typography` JSON syntax. Border and Shadow are also composites with structured values referencing other tokens.

### Component tokens — when and why
Use a component token when:
- Generic-direct usage breaks under theming (the "as-is vs to-be" pattern: tile background should not point at `ds-color-brandA-orange-55` directly; create `ds-color-components-tile-background-accent-brandA` with that as alias).
- A semantic token doesn't exist and the concept doesn't generalize across components yet.
- An "inverse conundrum" arises (button label inverse, checkbox check inverse, badge success icon inverse) — only promote to semantic if it's clear inverse should rarely be used and only on atomic components.

### Tooling stance
Style Dictionary is named explicitly as the typical transformation pipeline. The "About tokens / Integration" diagram shows: Figma styles/variables -> Tokens (source of truth) -> Style Dictionary -> Less, Sass, JSON, TypeScript, CSS variables, iOS Swift, Android (Tokens.aar) -> npm/aar packages -> apps and libraries. DTCG `$type` and `$value` syntax is shown for composite tokens, indicating alignment with the W3C draft.

### Common mistakes Curtis names
- **Distinct languages** across apps for the same color
- **Inconsistent values** (e.g., `#0D0D0D` vs `#111111` for "the same" decision)
- **Hardcoded values** alongside named tokens
- **Impossible to propagate change** when languages diverge
- Using **generic tokens directly when varying color by mode** (instead of building a component token that enumerates aliases by mode)
- **Premature optimization** — adding tokens speculatively for one team's needs
- **Homonyms** in level names (e.g., `display` meaning different things)
- **Mixing brand and accessibility** decisions without explicit alternatives

### Token process (4-step)
**Plan -> Discovery -> Decide -> Automation (Figma + Style Dictionary).**

Two key choices in Approach:
- **Formal vs Organic** (audit + propose taxonomy + catalog-wide implementation, OR find/name useful tokens as you work)
- **Comprehensive vs Color-and-text-only** (everything including size/space/shape/elevation, OR start with color + text only)
- **Deliver tokens only vs Fix-and-enhance as-you-go** (new taxonomy then update components later, OR update components as you go)

Audit findings are organized by **INTENT**, **MISUSE**, **BY COMPONENT**.

### Notable verbatim language
- "Design systems present an illusion of choice, solving problems others face over and over."
- "From core kit made by a central group / To shared kits made by federated masses."
- "If I had a nickel for every time I detected a raw value in a stray variant when a token is needed, I'd be rich."
- "Many design systems limit color theming to refer to light versus dark mode ... And that's ok."

## Workshop (Sep 2023) — extract by topic

### Discovery / strategy
Curtis frames a system definition with seven questions:
1. What does it offer?
2. What outputs does it release?
3. Who makes it?
4. Who uses it?
5. Why do they need it?
6. When is it used?
7. (\*) How does it work?

**Feature categories** (frequency-tagged): Visual Style (Always), UI Components (Always), UX Patterns (More often), Editorial (More often), Charts (Less often), Accessibility (Less often), Page Templates (Rare).

**Outputs:** Code libraries (Always), Design libraries (Always), Web docs (More often).

**Outcomes** (priority-tagged): Consistency (Critical), Efficiency (Critical), Quality (High), Satisfaction (Moderate), Maintainability (Moderate), Reusability (Moderate), Language/Portability (Nice to Have).

**Strategy heuristic** — the "system definition mad-lib":
> "Our design system offers [X], released as libraries in [Y], documented at [URL], made by [Team], used by [Customers], so that our experiences are [Outcomes]."

He also asks team-defining questions: How clear are customer/adopter boundaries? How similar are the terms? How specific are outputs? How specific is the team? Is the team real, with real individual names?

### Foundations / Tokens
Covered exhaustively in the tokens deck (above). Workshop reinforces: tokens are foundational, sit alongside components and accessibility/UX patterns. Spacing tokens, semantic alerts, surfaces, theming all get FigJam activities.

### Components (anatomy, properties, naming, composition)
Workshop's "Features Step-by-Step" treats components as features moving through steps:
- **Plan -> Design -> Specs -> Code -> Design Doc -> Design Assets -> Release** (the canonical pipeline)
- "Plan" aka Discovery / Propose / Scope (Designer or Product).
- "Design" aka Explore (Designer).
- "Specs" aka Specifications / Production (Designer).
- "Code" aka Build (Developer).
- "Design Doc" aka Docs / Guidelines (Designer).
- "Design Assets" aka Symbols / Figma Variants (Designer).
- "Release" aka Publish (Developer/Product/Designer).

**Effort curve:** investment increases gradually through Plan -> Design -> Specs -> Code; declines slowly through Design Doc; increases quickly at Release (communications + publishing). Reviewer effort spikes at Specs and Code.

He compares processes from real systems: Discovery Education 2016, Morningstar 2017, Target 2018, REI 2018 — to show discovery, accessibility, harden, document, publish are distinct phases that order differently.

**Multi-platform delivery** — System team designs once, then multiple teams (web/iOS/Android) implement. The "handoff" is between Spec and Code.

**Subtask templates per task** — ticketing systems should template subtasks per step. AVOID: "Randomly write titles to obscure or conflate steps." ALWAYS: "Incorporate task type and predictable workflow steps."

### Documentation
Documentation is one of the seven steps in the feature lifecycle, with substeps: Setup from template, Source reusable assets, Examples, Design guidelines, Accessibility, Code API docs, Component explorer states, Code usage examples, Writing/editorial, Images, Prototype demos.

A documentation platform initiative ("Documentation Platform") is one of seven major-release tracks: content management platform, site IA & navigation, component page templates, other page templates, documentation components ("Do/Don't"), non-feature documentation, homepage design.

### Development support
Adoption Enablement is its own initiative — Roadshow, Getting Started materials, Training sessions, Office hours, Release announcements, Slack support. Warranty period after launch is named: "rapid releases of fixes, priority enhancement and supporting initial general integrations."

Code-side substeps in the "Code" step: Create code branch, Draft API, Generate file(s), Source reusable code, HTML/CSS/JS, Obtain API feedback, Browsers & devices, Unit tests, Accessibility (manual + automated), Visual regression, Functional, Document API, Update dependents, Merge pull request, Write changelog.

### Pilot / launch
Major-release **milestones**:
- **Commit** — to plan, design language, tech architecture
- **Alpha** — a few features through entire process to prove "how to build"
- **Beta** — enough features at sufficient stability for early adopters
- **Launch** — a major release of all features available generally

Progress measured by **Quantity** (component count: 2-4 alpha -> 10-15 beta -> 20-30 launch), **Quality** (low -> high -> full), **Stability** (moderate -> high -> full).

Major-release **tracks** (initiatives): Design Language, Technical Architecture, Visual Style, UI Components, Documentation Platform, Planning, Core Team Operations, Adoption Enablement.

### Governance / contribution / team models

**Team models** (named, in order):
- **Solitary** — one person.
- **Central** (aka Core) — funded team.
- **Federated** (aka Community) — distributed contributors.

**Decision rule:** "Start with core group to setup tools and form ways-of-working, then gradually grow to engage a community." "Overlords don't scale."

**Stages of getting to a core team:**
- Stage 1: Part Timers
- Stage 2: Allocated Individuals
- Stage 3: Dedicated Team

Discipline-oriented vs Team-oriented support is contrasted. Team-oriented (system team serves multiple product teams) is preferred.

**Sizing:** Small / Medium / Large — across Product (PM), Design (lead, visual), Development (tech lead, developers), Other (specialist).

**Ratios and capacity rules:**
- Designer-to-developer ratio: **1:2** ("Mine is 1:2.")
- Designers, developer capacity: **50% or bust**
- Specialists: negotiable
- "Protect from knowledge loss"

**Skills wanted:** "Thinks in systems, acts in systems. Copes with complex process, tests conscientiously. Writes well, documents meticulously. Connects inclusively, frames change effectively."

**Team-of-teams patterns** (5 examples named):
- Subgroups (Creative / UI Engineering / Accessibility / Prototyping)
- The "Discipline Wall" (UX vs Tooling separation)
- Shifting with Scope (every 6 months, leaders remix staff)
- Expanding Responsibility (system grows from "dumb" front-end to "smart" front+back)
- Mobile Stepchildren (web team + mobile design + iOS dev + Android dev)

**Communities of practice:**
- Steering Committee (directors/VPs)
- Extended Design Group (aka Ambassadors / Champions / Guild / Critique)
- Extended Developer Group (aka Front-end guild / Tech working group / Advocates)

**Contribution definition:** "Design, code, or documentation of a fix, enhancement, or new feature by someone NOT on the core team made available for others to use." Tangible / Useful / Federated / Released.

**Contributions ≠ Participation.** Reviewing PRs, suggesting examples, attending meetings, asking questions, using the system are *participation*, not contribution.

**Contribution scale:** Fix -> Small Enhancement -> Large Enhancement -> New Feature -> Catalog Wide -> New Catalog. The largest two ("Catalog Wide," "New Catalog") are **driven by system team, not contributor.**

**Contribution criteria** (named):
- **Shared Need** (1 = "keep it local," 4-5 = "let's get started")
- **Timing** (3 months = formal full release; 6 weeks = system-spec'd, locally-built; 2 weeks = build yourselves with consultation)
- **Responsibility** (who does which step)
- **Availability** (1 week = "let's go!"; 1 month = "set milestones"; 3 months = "discuss commitments"; 1 year = "discuss another time")
- **Capability**
- **Direction** (consistent with how system is growing?)
- **Cost** (relative to shared impact)
- **Relative Value**

**Curtis's named pattern:** "Self Directed (frequent & fast)" vs "Stewarded (rarer & deliberate)" contributions.

**Shepherd vs Steward:** "What do you call a core team member that helps the contributor?" Shepherd = guide in spiritual matters; Steward = manages another's property. Curtis names this distinction without explicit endorsement of one.

**Six-step contributor onboarding** (verbatim):
1. Start with a conversation, not a form
2. Prep with what they need to know, not more
3. Provide templates and outline with them
4. Refer to most-similar existing examples
5. Listen for what they believe they can do
6. Build cadence, check in, and avoid stalls
7. ("You manage community, they focus on work")

**Praise patterns:** @ mention in Slack (multiple times), doc page byline, email release announcement, release history line item, demo to large groups, promote to "expert" for area.

### Maintenance

**Initiative types** (named, with personality traits):
- **Scaling** — make more of what you already have. "Know how to do, predictable to plan and estimate."
- **Refactoring** — improve what's already made. "Often impacts entire catalog. Challenges mindsets to learn new ways. Invokes API/naming reconsiderations."
- **Expanding** — make something new. "Discovery and exploration unpredictable. Stresses process to expand, diversify."
- **Servicing** — support who you make things for. "Core team would rather 'make stuff.' Needs attention and perseverance. Not for all designers and developers."
- **Operating** — run and manage how you do things. "Once architected, predictable to execute."

**The "Feature Ceiling":** UI components maintained by core team plateau over time. "Demand justifies more" / "Our system isn't just UI components" / "Our system has grown unwieldy." Three views map to three growth strategies.

**Beyond Product:** Service (Onboarding, Plugins/tools, Satisfaction, Slack support, Sparring critique) and Community (Foundations, Contribution).

**Communications** are scheduled operationally:
- Sprint demo (every 2 weeks)
- Training events (quarterly)
- Semi-annual planning
- Release events with rolling "Major release is coming" / "New feature spotlight" / "Deep Dive" cadence

**Slack channels:** `system-core-team` (private), `#system-design` (public, releases + design help), `#system-dev` (public, releases + tech help), `system-[ambassadors]` (groups), `#system-ux-patterns` (special topics).

**Audience growth pattern:** Core team (100% attendance) -> Typical Attendees (60-80%) -> Irregular (25-50%) -> Irregular (<25%, attracted to "important" feature demos). Demos can grow from 8-15 people to 40-80.

**Initiative planning lifecycle:** Solicit (surveys + interviews) -> Score (must/should/could/shouldn't matrix) -> Validate (workshop with stakeholders, "We will / We might / We won't") -> Implement (communicate + prepare in Jira/Asana).

**Tickets without a process vs with a process:** Always title tickets with `[Component] [StepType]` (e.g., "Motion [Propose]", "Dialog [Design]", "Button Group Multi-Selection Defect [Code]"). AVOID randomly written titles.

**Subtask templates per task type** in project management.

### Systems of Systems / Tiers

A signature Curtis framework. **Library tiers** (in order):

| Tier | Definition | Used by | Maintained by |
|---|---|---|---|
| **Core foundation** | Foundational styles, templates, design assets that components/patterns are built on (e.g., Tokens) | DS team to build all features; teams for custom components | DS team |
| **Core library** | Reusable styles + UI components relevant across all teams | All teams | DS team |
| **Shared libraries** (Business unit / Platform / Feature) | UI components/styles serving shared needs beyond a single team | BU teams / platform teams / feature seekers | Contributors with help from DS team |
| **Team library** | Reusable styles + UI components for one team, often overlapping with core | A team | Team-identified maintainers |
| **Team project file** | Files used by one team to deliver a project | Single team members | (not a library) |

Default availability: Core foundation + core library are **on by default** for all adopters; shared libraries are opt-in; team library is on for that team only.

Sub-tier examples:
- **Business Unit** kits (`.com Expansion Pack`, intranet, TV)
- **Dev Platform** kits (iOS Expansion Pack, Android, Flutter, Angular)
- **Feature Sets** (Editor, Search, Charts, Navigation Templates)

Setup matrix per tier defines OWNED by (admin), MAINTAINED by (edit), VISIBLE TO (view), Location.

### Measuring Success
Six themes, each with questions, examples, data collection methods:

| Theme | Key Question | Examples | Data Collection |
|---|---|---|---|
| **Productivity** | How much did the (core/contributor) team make? | # components, # doc pages, # releases, # fixes | Project management, component code tagging |
| **Coverage** | Is the system being used? Who? How much? How up-to-date? | # of products using; % of page applying system; system feature life cycle status by adopter | Automated package.json audits, automated component tracking, downloads |
| **Satisfaction** | How satisfied are internal/external customers? | NPS, SUS, complaint frequency | Surveys, polls, sentiment analysis |
| **Consistency** | Is the experience consistent? On-brand? | Visual/content/interactive cohesiveness | Manual product/page audits, manual audits |
| **Quality** | Are products more performant? Accessible? Usable? | Accessibility scoring, usability testing, performance metrics | Manual audits, automated scoring tools, controlled studies |
| **Efficiency** | How much time was saved? Faster-to-market? Redundant work down? | % dev time reduced, # days reduced, % CSS reduced, average turnaround | Employee reviews, system v product codebase comparison |

Curtis explicitly calls NPS "Not well-respected in the design community." Prefers SUS for product ease-of-use, especially with open-ended follow-up.

**Coverage definitions** (he names three competing ones):
1. Proportion of components sourced from system relative to all UI components (didoo)
2. Proportion of a page using system components vs team-made (Morningstar)
3. Components in use across all code files / all repos (Veriff)

**Adoption pattern across versions:** Developer code packages taper *slowly* across past versions; designer asset downloads diminish *sharply* across past versions.

## Phase-tagged findings (canonical 8 phases)

- **Discovery & Strategy** — System definition mad-lib (offers/released-as/documented-at/made-by/used-by/so-that). Initiative types: Scaling/Refactoring/Expanding/Servicing/Operating. Solicit-Score-Validate-Implement planning loop. Survey + interview prompts ("imagine a year from now, the system failed — what's the evidence?"). Major-release tracks. Audit findings organized by INTENT / MISUSE / BY COMPONENT.

- **Design Foundations** — Three-tier token taxonomy (generic / semantic / component) plus composite tokens. Token levels: system-category-property-variant-mode. Naming principles: avoid homonyms, balance flexibility/specificity, avoid premature optimization, start within then promote across. Theming purposes (mode, brand, density, generation, white-label, responsive, campaign). Surface as the unit of theme inheritance. Tokens vs Variables distinction (sharing, format count, naming discipline).

- **Component Library** — Components-as-Data: anatomy / props / styles / variants. Pipeline: Plan -> Design -> Specs -> Code -> Design Doc -> Design Assets -> Release. Component tokens for theme-varying single-component decisions. Multi-platform handoff between Spec and Code. Subtask templates per step. Effort curve (gradual through code, sharp at release). Catalog scaling pattern: 2-4 alpha, 10-15 beta, 20-30 launch.

- **Documentation** — Documentation Platform as a major-release track. Doc as a feature step with substeps (template setup, examples, design guidelines, accessibility, code API, component explorer, usage, editorial, images, prototypes). Generated docs from component data definitions (essay 2025).

- **Development Support** — Style Dictionary as transformation pipeline. Token outputs across Less/Sass/JSON/TS/CSS/iOS/Android. DTCG composite types ($type, $value). Multi-platform code delivery. Code substeps including unit tests, manual + automated accessibility, visual regression, API docs, dependent updates. Adoption Enablement initiative (roadshow, getting-started, training, office hours, slack support, release announcements).

- **Pilot & Implementation** — Milestones: Commit -> Alpha -> Beta -> Launch. Quantity / Quality / Stability progression. Pilot team demos before launch. Warranty period of fast-fix releases post-launch. Launch-associated training events. Release messaging cadence with "release is coming" / "feature spotlight" / "deep dive" rotation.

- **Governance & Adoption** — Solitary -> Central -> Federated team-model evolution; "start central, grow community." 1:2 designer-to-developer ratio. 50% capacity floor for designers/devs. Steering Committee + Extended Design Group + Extended Developer Group. Contribution criteria (shared need, timing, responsibility, availability, capability, direction, cost, relative value). Contribution size scale (Fix -> Catalog Wide). Contributor onboarding (conversation not form, templates, similar examples, cadence). Praise patterns. Library tiers (Core foundation / Core library / Shared libraries / Team library / Team project file). Coverage measurement methods.

- **Ongoing Maintenance** — Five initiative types (Scaling, Refactoring, Expanding, Servicing, Operating) with their personality profiles. Feature ceiling. Sprint demo every 2 weeks. Semi-annual planning. Slack channel structure. Solicit-score-validate-implement planning ritual. Tickets titled `[Component] [Step]`. Subtask templates. Six measurement themes (productivity, coverage, satisfaction, consistency, quality, efficiency). Generation tokens (DS2_0 / DS3_0 alongside).

## Curtis's recurring frameworks (catalog)

1. **Three-tier token taxonomy** — Generic / Semantic / Component (+ Composite). Promote across when 2+ components share. (Tokens deck.)

2. **Token levels decomposition** — system / theme / domain / group / component / element / category / concept / property / variant / state / scale / mode. (Tokens deck.)

3. **Tokens vs Variables matrix** — WHAT/WHERE/WHY/WHEN/HOW. (Tokens deck.)

4. **Theming dimensions** — Responsive, Light/Dark, Multi-brand, Campaigns, Generations, White label, Density. (Tokens deck.)

5. **Components-as-Data shape** — anatomy / props / default / variants. (Essay 2025.)

6. **Initiative types** — Scaling / Refactoring / Expanding / Servicing / Operating. (Workshop.)

7. **Major-release milestones** — Commit / Alpha / Beta / Launch with Quantity/Quality/Stability progression. (Workshop.)

8. **Major-release tracks** — Design Language / Technical Architecture / Visual Style / UI Components / Documentation Platform / Planning / Core Team Operations / Adoption Enablement. (Workshop.)

9. **Team-model evolution** — Solitary -> Central -> Federated. (Workshop.)

10. **Core team sizing** — Small / Medium / Large with role mix; designer:dev ratio 1:2; 50% capacity floor. (Workshop.)

11. **Feature pipeline (7 steps)** — Plan / Design / Specs / Code / Design Doc / Design Assets / Release. (Workshop.)

12. **Effort curve** — gradually rising Plan->Code, slowly declining Doc, sharply rising Release. (Workshop.)

13. **Contribution scale** — Fix / Small Enhancement / Large Enhancement / Feature / Catalog Wide / New Catalog. (Workshop.)

14. **Contribution criteria** — Shared Need / Timing / Responsibility / Availability / Capability / Direction / Cost / Relative Value. (Workshop.)

15. **Contributor onboarding 6-step** — conversation > form, templates, examples, cadence. (Workshop.)

16. **Library tiers** — Core foundation / Core library / Shared libraries / Team library / Team project file. (Workshop.)

17. **Communities of practice** — Steering Committee / Extended Design Group / Extended Developer Group / Core team. (Workshop.)

18. **Six measurement themes** — Productivity / Coverage / Satisfaction / Consistency / Quality / Efficiency. (Workshop.)

19. **Solicit -> Score -> Validate -> Implement** planning loop. (Workshop.)

20. **YAGNI governance test** — needed by 1 team -> don't add to Core; needed across 7+ teams in 3+ BUs -> add it. (Tokens deck.)

## Notable verbatim quotes (with source doc)

- *"A style guide is an artifact of design process. A design system is a living, funded product with a roadmap & backlog, serving an ecosystem."* — Workshop

- *"A Design System isn't a Project. It's a Product, Serving Products."* — Workshop (article reference)

- *"Overlords Don't Scale."* — Workshop, Team Models section header

- *"Design systems present an illusion of choice, solving problems others face over and over."* — Tokens deck

- *"Tokens feels quaint by comparison [to components-as-data]."* — Components as Data

- *"AI is everywhere, and it favors structured data. So express components that way."* — Components as Data

- *"It's difficult to imagine returning to a time when I architected components only in a visual tool like Figma."* — Components as Data

- *"From core kit made by a central group / To shared kits made by federated masses."* — Tokens deck (Systems of Systems pattern, also in Workshop)

- *"Start with a conversation, not a form."* — Workshop (contributor onboarding)

- *"Contributions ≠ Participation."* — Workshop

- *"Designer-to-developer ratio? Mine is 1:2. Designers, developer capacity: 50% or bust."* — Workshop

- *"Start with core group to setup tools and form ways-of-working. Then gradually grow to engage a community."* — Workshop

- *"Avoid premature optimization ... YAGNI ... You ain't gonna need it."* — Tokens deck

- *"Start within, then promote across."* — Tokens deck (component tokens)

- *"Define the customer problems, and work back from there."* — Tokens deck (theming strategy)

- *"Slack + Office Hours ≠ communications plan."* — Workshop

## Where Curtis CHALLENGES typical industry POV

- **Figma variables ≠ tokens.** Most practitioners conflate them. Curtis's tokens-vs-variables matrix is an explicit pushback: variables are local, single-format, often chaotically named; tokens are versioned, multi-format, deliberately named for scale.

- **Figma's Dev Mode MCP is a trap.** "Stochastic, incomplete, and imprecise component description biased towards one platform (like React) and framework (like Tailwind)." Many in the industry treat Dev Mode/MCP as the AI-readiness solution; Curtis says no — formalize the data first.

- **Figma as output, not input.** A reversal of the typical "design in Figma, ship to code" pipeline. Most designers consider the Figma file the source of truth. Curtis: data is the source; Figma is generated.

- **NPS is "not well-respected in the design community."** Many leaders reach for NPS by default; Curtis prefers SUS with open-ended follow-up.

- **Components-as-Data over component spec docs.** Many systems teams produce extensive Confluence/Storybook spec docs. Curtis sidesteps that with structured YAML/JSON definitions that auto-generate docs and code.

- **Pure federation is chaos.** "No central foundation, curators or maintainers ... that is the chaos that leads to consistency, quality and maintainability." (Sarcastic, mocking the "we'll just contribute everything" assumption.) Federation is a *destination* reached after a strong center, not a starting point.

- **Catalog-wide and new-catalog work is system-team driven, not contributor.** Pushes back on the assumption that "contributions" can scale to anything.

- **Generic-only token taxonomies are insufficient when theming.** Many systems stop at generic + semantic. Curtis insists component tokens are necessary when theme-varying decisions belong to one component.

- **"Roadmap implies a project" is wrong** — the roadmap is the system's permanent product backlog.

- **Solitary maintainer is a real, named stage** that many leaders pretend doesn't exist or skip past. Curtis names it Stage 1.

- **YAGNI as a governance principle**, not just a coding heuristic, applied to token namespace pollution.

## Where Curtis ALIGNS with the practice's internal POV

- **DS as product/infrastructure** — directly affirmed. ("It's a Product, Serving Products.")

- **Tokens W3C DTCG** — composite token JSON examples in the tokens deck use the `$type`/`$value` syntax; Style Dictionary is named as the canonical pipeline.

- **Centralized team preferred but with contribution model** — directly affirmed. Solitary -> Central -> Federated, with central as the funded backbone and federation as a community layer; contribution model has explicit criteria, scale, and onboarding rituals.

- **4-tier component hierarchy** — Curtis's library tiers (Core foundation / Core library / Shared libraries / Team library / Team project file) maps almost exactly to a 4-tier hierarchy if you collapse "team library" and "team project" together. Internal "4-tier" likely reads: Foundations, Core, Shared/Brand, Product/Team — which is Curtis's tiers minus the file-only level.

- **Atomic design as mental model** — implicitly aligned: anatomy (elements -> root containers -> slots), composition of components into patterns, surfaces as containers, page templates as the topmost concern.

- **Brand-themes** — directly affirmed. Curtis's theming dimensions explicitly include Multi-brand and Brand model A/B/C. Component tokens enumerate brand-by-mode aliases.

- **Embedded handoff** — Curtis's design-step substeps explicitly include "To assigned developer(s)" and "To system team" review handoffs *during* the design step, not after. This is the embedded-handoff pattern.

## Gaps Curtis surfaces that internal docs may not cover

1. **Components-as-Data is recent (2025).** If internal docs predate this, they may not yet treat structured component definitions as a first-class artifact. Curtis: this is the AI-readiness move that surpasses tokens.

2. **The "Inverse conundrum"** — Curtis names a specific pitfall (button label inverse, checkbox check inverse) where teams over-promote inverse element/surface tokens to semantic tier. Internal token guidance may not name this explicitly.

3. **Density tokens** — Compact / Cozy / Comfortable as a theming dimension is often overlooked. Curtis names it alongside size as an interaction (size × density matrix).

4. **Generation tokens** — naming legacy tokens with `_legacy` prefix to coexist with current generation (DS2_0 vs DS3_0 example). Useful pattern for migrations.

5. **Composite tokens beyond typography** — Border, Shadow as DTCG composites with explicit reference structures.

6. **Scoring stakeholders with must/should/could/shouldn't** — concrete prioritization mechanic for initiative planning. Internal docs may have OKRs but not this fine-grained input gathering.

7. **Initiative-type personality profiles** — recognizing that Refactoring "challenges mindsets to learn new ways" and is "not for all designers and developers" is unusual psychological framing for staffing.

8. **Specific capacity rules:** 1:2 design:dev, 50% floor. Internal docs may say "centralized team" without naming the staffing math.

9. **Shepherd vs Steward distinction** for contribution coaching role.

10. **"Self-Directed vs Stewarded contributions"** — naming the social cadence of contributions, not just their size.

11. **Audience growth pattern** for sprint demos (8-15 -> 40-80) and the correlation with "extended" vs "steering" status.

12. **Tickets titled `[Component] [StepType]`** — concrete project-management hygiene.

13. **Library tier visibility/admin/edit/view matrix** — explicit per-tier RBAC pattern.

14. **Coverage definition is contested** — Curtis names three different industry definitions (didoo, Morningstar, Veriff) without picking one. Internal docs may pick a single coverage definition without acknowledging the alternatives.

15. **Asymmetric package taper** — code packages taper slowly across versions; design assets diminish sharply. This drives different deprecation strategies for code vs Figma assets.

16. **The "Feature Ceiling"** — explicitly naming that core-team-maintained UI component growth plateaus and requires either federation, scope expansion (Service/Community), or refactoring rather than more components.

17. **"Plan an hour, iterate an hour"** workflow for components — designers as architects, with point-and-click work delegated to generation.

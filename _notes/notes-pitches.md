# Notes: VML Pitches (CareCentrix 2026 + Thrive 2024)

## Source meta

**CareCentrix 2026**
- Title: "CareCentrix Design Language Partner"
- Date: March 2026 (Version 2)
- Line count: ~1304 lines (extracted text)
- Audience: External — CareCentrix prospect/client. RFP response for an internal-tooling design system.
- Author/lead: Adam Forrester, Group Director, Design Systems (cover letter signed)
- Framing: "design language partner" rather than vendor; positions VML as a strategic, embedded partner working alongside the client's engineering team from day one.

**Thrive (Thrivent) 2024**
- Title: "Design Systems — Digital Design Systems AT VML"
- Date: September 2024 (Version 1.0)
- Line count: ~1073 lines
- Audience: Thrivent (financial services, "Thrive" referenced). Internal-feeling pitch / educational deck — heavier on definitions, value framing, and "signs you need a DS".
- Team named on cover: Adam Forrester (Group Director, XD | KC), Aaron May (Director, XD | CIN), Sofia Andreadis (Sr. Program Director | CIN), Sam Thompson (Director, Technology | KC).

Both decks share asset DNA: the Wendy's Fresh DS and T-Mobile Apeiron case studies appear verbatim in each, and a recurring "brand → digital styles → UI components → product" diagram (attributed to Josh Clarke / Big Medium, "Design Systems at Scale: Episode 2" in the Thrive deck) anchors the conceptual model.

---

## CareCentrix 2026 — pitch arc & content

### Narrative spine
- This is not a design refresh — it's a foundational investment in how CareCentrix operates.
- Internal tools deserve the same craft as customer-facing products.
- A design system is infrastructure, not a one-time deliverable.
- Done right: faster engineers, more consistent interfaces, more resilient organization.
- Best systems are co-built — VML works alongside engineering from day one, not handed off at the end.
- "Built once. Used everywhere." A DS is a product serving the organization (consistency, efficiency, quality/scalability).
- For internal tooling specifically: visual consistency is the surface; the deeper goal is making engineers faster and tools more trustworthy to the people who depend on them daily.
- Four positioning pillars: Foundations that scale, Built for real users, Accessibility as a standard (WCAG 2.1 AA + Section 508), Brand made digital.
- Three-phase methodology: Discovery → Foundations → Build, with incremental handoff (not a final hand-off moment).
- Two engagement options: 12–16 weeks ($230–$320k) MVP; 16–24 weeks ($320–$500k) extended/adoption-ready.

### Section 02 — How We Think About Systems That Scale (full content)

Definition: "A design system is a collection of UI elements built as reusable code. They are guided by clear standards that help organizations deliver cohesive, on-brand experiences at scale, over time."

"Built once. Used everywhere." — A design system is not just a UI library, it's a product serving the organization.

A strong design system enables:
- Consistency across teams and products.
- Efficiency in building and maintaining experiences.
- Quality and scalability at every layer.

Quote pull: "The system addresses 80% of design and development needs so they can focus on the other 20%." (attributed to "You Need A Design System — Here's Why").

Layered model (brand → product):
- Brand Team owns Brand Identity / Design Language: logos, colors, fonts, tone of voice, photography, usage guidance.
- Design System Team owns Digital Styles & Foundations (accessible color scales, type scales, spacing & grids, UX writing guidelines) AND UI Component Libraries (UI design + code libraries, common patterns, best practices, usage guidance).
- Product Teams own product-specific local libraries.

Atomic Design model: Subatomic (design tokens) → Atomic → Molecule → Organism (Pattern) → Template (Pattern). Foundational tokens called out: Color, Typography, Spacing, Grids, Shadows.

### Section 03 — Our Approach (methodology, phases, activities)

**Your Ask (as VML restates it):** Establish a shared design language and component library for internal tooling — giving the engineering team a consistent, scalable foundation across multiple platforms and applications.

**Our Perspective:** A great DS for internal tooling isn't just visual consistency — it's making engineers faster and tools more trustworthy. Four pillars:
- Foundations that scale — typography, color, spacing, interaction defined as W3C DTCG-compliant design tokens; structured for consistency today and built to support enterprise-level growth.
- Built for real users — recognizable, intuitive design patterns prioritizing clarity and ease of use; documented so engineers can implement faithfully every time.
- Accessibility as a standard — as a healthcare org, inclusive design is not optional; built to WCAG 2.1 AA and Section 508 out of the gate.
- Brand, made digital — unified visual expression of CareCentrix across every internal application; consistent in color, type, tone.

**Phases of Our Process — three phases:**

1. **Discovery** — Understand the landscape, align on visual direction, establish tools and principles.
   - Brand onboarding (review existing brand guidelines/assets).
   - Application audit (inventory components, patterns, inconsistencies, redundancies across the ecosystem).
   - Stakeholder alignment (tools, Figma setup, ways of working).
   - Definition sessions (collaborative working sessions to surface requirements, priorities, open questions).
   - Component backlog (prioritized inventory based on application needs and usage frequency).
   - Define the design direction (visual language aligned to brand, validated through high-fidelity mockups).
   - North star (why the system exists, who it serves, principles guiding every decision).

2. **Foundations** — Define core visual and structural elements as design tokens, delivered in Figma.
   - Figma setup as source of truth (variables, styles, documentation tooling).
   - Naming & architecture (token naming standards; primitive/semantic variable structure).
   - Color (full palette: primary, secondary, neutral, semantic, status; documented usage rules; WCAG-compliant contrast).
   - Typography (scales across heading/body, multiple breakpoints, density levels).
   - Spacing (scales spanning data-dense to breathing-room interfaces — "consistency without rigidity").
   - Design tokens (color, type, spacing core; everything foundational encoded as W3C DTCG-compliant variables — "ready for consumption as your stack evolves").
   - Style guide (digital style guide in Figma covering all foundational elements with usage doc).

3. **Build** — Build the library, design and document components engineering can implement with confidence.
   - Component architecture (layers: foundational elements → composite patterns → containers/layout structures).
   - Component design (each component on the token foundation; themeable, accessible, adaptable).
   - Design patterns (common patterns for internal, data-heavy tooling — a playbook for frequent interface challenges).
   - Usage documentation (when/how to use each component, do/don't, annotated specs).
   - Content guidelines (tone of voice, error message patterns, help text best practices).
   - Component validation (validated with pilot teams in context, ideally via Storybook).

Cross-cutting framing: "We work alongside your team throughout — not a handoff at the end, but an iterative build from day one." "Handoff is incremental, not a moment."

**Team structure** (both engagement options use the same model, allocation differs):
- Project Lead: Design Director (25%) — executive oversight, strategic direction, quality/craft escalation.
- Core Production: Design Systems Lead (50% — day-to-day creative lead, drives architecture and alignment with engineering), UX Designer (100% — owns documentation strategy/UX framework), UI Designer (100% — designs/builds component library on token foundation), Delivery Lead (50% — PM, timelines, communication, sprint cycles).
- Supporting Roles: UX Copywriter (75 hours — voice/content standards, error/help text, tone), Accessibility Specialist (10 hours — WCAG 2.1 AA & Section 508 review at key milestones).

**Roles & Responsibilities** — the deck enumerates explicit bullet lists for each role; key signals:
- Design Systems Lead is the primary creative point of contact; leads discovery activities (audit, stakeholder sessions, design direction); drives system architecture; maintains backlog; leads incremental handoff sessions with engineering.
- UX Designer "owns the documentation strategy across the engagement"; defines structure/format of Figma component documentation; documents do/don't, states, accessibility notes; ensures docs are actionable for an engineering audience.
- UX Copywriter integrates content guidelines into component documentation.
- Accessibility Specialist reviews foundational decisions (color contrast, type scale, focus states) against WCAG 2.1 AA and Section 508; provides guidance during component design "so compliance is built in, not retrofitted"; available for targeted reviews at foundations approval and component completion.

### Section 04 — Milestones & Timeline

**Assumptions block:**
- Engagement & Process: dedicated client POC with approval authority; design direction approved within 2 review rounds before foundations begin; component feedback within agreed cycles; VML has access to brand assets and existing files at start.
- Tools & Access: Figma is the design and documentation tool; client provides/procures licensing or arranges file transfer from VML's Figma environment; VML gets access to existing application environments for audit; engineering available for alignment in discovery and incremental handoff touchpoints.
- Scope Boundaries: foundations + component design + documentation only — does NOT include front-end development, code delivery, or engineering implementation. Custom iconography NOT in scope (use existing or open-source). Application-specific UI redesign, journey mapping, UX research are OUT of scope. Extended component set is illustrative — final list defined collaboratively.
- Staffing: team composition consistent across both options; allocation varies by length. Accessibility SME scoped as a bucket of hours; additional accessibility audit work is a scope add.

**Option 1 — 12–16 Weeks ($230–$320k) — MVP**
- Discovery: 4 weeks
- Foundations: 4 weeks
- Build: 4–6 weeks

Sequencing milestones (Option 1 timeline view):
- Kickoff → Brand onboarding complete → Component backlog prioritized → Audit & research complete → Design direction approved → Color system defined → Typography system defined → Token architecture defined → Foundation direction approved → Full token set complete → Style guide complete & approved → Component design begins → First component handed off to engineering → Component & documentation alignment → Component library and documentation handoff → Pilot validation with engineering.

Discovery deliverables: Application audit report; prioritized component backlog; design principles (3–5 opinionated, decision-making principles); high-fidelity mockups demonstrating the approved design direction; Figma environment configured.

Foundations deliverables: Color system with semantic usage; typography system with breakpoint guidance; spacing system with density variants; complete W3C DTCG-compliant token set in Figma Variables (color, typography, spacing, border, radius, shadow, grid, motion); digital style guide in Figma; accessibility standards documentation (contrast ratios, type minimums, focus state specs).

Build deliverables: Core component set in Figma (built, annotated, token-connected); component usage documentation per component; design patterns documentation (common workflows and interface patterns for internal tooling); content guidelines (tone of voice, readability, error/help text best practices); published Figma component library ready for engineering consumption.

**Core Components (Option 1):** Button (primary, secondary, destructive, disabled); Text input & text area (with error/warning/success validation states); Select / dropdown; Checkbox / checkbox list; Radio button / radio button list; Toggle; Alert / notification banner; Badge / status tag.

**Core Design Patterns (Option 1):** Button groupings; Form layout and validation flow; General wayfinding patterns.

**Option 2 — 16–24 Weeks ($320–$500k) — Extended**
- Discovery: 4 weeks
- Foundations: 4 weeks
- Build: 16 weeks

Same Phase tasks/deliverables as Option 1 plus extended set. Milestones add: Extended component set confirmed → multiple Component & documentation alignment cycles → Pilot validation with engineering → Component & documentation handoff at week 24.

**Extended Components:** Modal / dialog with scrim; Data table (basic structure, column headers, row states); Pagination; Tooltip / popover; Search input; Tabs; Accordion; Loading spinner / skeleton loader.

**Extended Design Patterns:** Error state handling; Data table interactions (sorting, filtering, row actions); Confirmation and destructive action flows; Overlay and modal workflows; Search and filter patterns.

Framing for Option 2: "An extended timeline allows us to move beyond MVP creation into real-world validation, adoption and scale… expanding the component library, the extended timeline creates space for system-wide readiness, broader organizational adoption, and long-term scalability."

### Section 05 — Relevant Experience (case studies)

**Wendy's Fresh Design System** (freshds.wendys.com)
- Problem: Inconsistent and inaccessible digital experiences caused user frustration. Lack of standardization led to slow time-to-market and increased cost; updates were time- and resource-intensive.
- Solution: Created Fresh DS to support a rebuild of iOS & Android apps into a single Flutter codebase. Reduced 4000 lines of app code; increased time-to-market speeds by 600%. Expanded to digital ordering website and CRM. Includes usage guidelines.
- Numbers: 30 app components / 24 app components / 4000 lines of app code removed / 22 developers supported / 15 designers supported.
- Accessibility narrative: "Wendy's has the potential to be the most accessible food ordering app ever, and a gold star standard for screen reader experiences." 40+ web accessibility issues logged / 80+ app iOS & Android accessibility issues logged / 25 critical accessibility issues remediated.
- Theme: design tokens & themes — "leveraging tokens to enable stylistic consistency, scaling, and the ability to affect change across design and development with minimal effort."

**T-Mobile Apeiron Design System (2022–2023)**
- Brief: Q2 2022, VML led a blended agency + T-Mobile team to create a new DS supporting flagship app and website.
- The Ask: "Redeploy as Design-Centric" — rebuild flagship app and website from the ground up from a single consolidated DS to reduce maintenance cost, accelerate features, enable scalable cohesive experiences for customer and front-line.
- Apeiron = "flexible framework for the future of T-Mobile and Metro digital products across multiple platforms."
- VML's role: lead client/agency DS team; cross-disciplinary resources; define DS team processes & roadmaps; define implementation/adoption strategies; lead adoption efforts; define support strategies.
- Deliverables: UI libraries (Web, iOS, Android); T-Mobile & Metro brand themes; design tokens as single source of truth; design patterns; documentation; getting-started guides and integration support.
- Theme switching: "Changing brands with the flip of a switch" — single codebase with stylistic brand themes for Apeiron's T-Mobile and Metro brands; light and dark colors included.
- Numbers (started Apr 2022): 20+ UI elements researched / 500 design tokens / 2 brand themes / 18 UI elements designed / 24 elements researched / 39 team members since June / 3 platforms (iOS, Android, Web) / 15 elements in development / 20 pages of usage guidance & design patterns.

### Section 06 — Discovery Questions (VERBATIM)

Framing: "To refine our approach and ensure this proposal reflects your exact needs, we'd welcome clarity on the following before we begin. These answers will help us hit the ground running from day one."

**Tools & Licensing**
- Does CareCentrix have an existing Figma license, or will one need to be procured for this engagement?
- Are brand fonts licensed for digital use, or will font licensing need to be addressed as part of the engagement?
- Does CareCentrix have an existing icon library, or should we plan to recommend and adopt an open-source icon set?

**Stakeholders & Process**
- Who will serve as the day-to-day point of contact on the CareCentrix side?
- Who holds approval authority for design direction sign-off, and how are review decisions made?
- How available will the engineering team be for alignment sessions during discovery and incremental handoffs throughout the engagement?

**Brand & Content**
- Are existing brand guidelines and assets available for VML to reference at the start of the engagement?
- Will content guidelines and tone of voice work be informed by existing brand materials, or will stakeholder interviews with communications or marketing be required?

**Technical Context**
- Are there any existing design files, UI kits, or component libraries we should be aware of prior to the audit?
- What is the current status of the Backoffice Portal POC — is it actively in development, and will it serve as the primary pilot target for the design system?

### Notable language / framing (CareCentrix)
- "Design language partner" (cover concept).
- "Infrastructure, not a one-time deliverable."
- "Built once. Used everywhere."
- "Handoff is incremental, not a moment."
- "The system addresses 80% of design and development needs so they can focus on the other 20%."
- "A unified visual expression of CareCentrix across every internal application."
- "Built to be themeable, accessible, and adaptable."
- "Ready for consumption as your stack evolves."
- "Compliance is built in, not retrofitted."
- "Consistency without rigidity" (re: spacing for varying density).
- "From data-dense internal tools to interfaces that need more visual breathing room."

---

## Thrive 2024 — pitch arc & content

### Narrative spine / thesis
- Educates the audience on what a DS is and is NOT (style guide / UI kit / component library / brand DS — distinct things).
- A design system "provides a library of solved problems delivered as reusable UI elements, guidelines, and patterns" so teams can scale design, foster collaboration, and "focus on more complex problems."
- It's how organizations are approaching product design today — citation: "In 2020, 65% of companies said they use design systems, and that will only increase." (You Need A Design System — Here's Why)
- Design systems and accessibility are "the perfect pair" — addresses the "$1.2 trillion in annual disposable income / 1 billion disabled people worldwide" market opportunity (cited: "The Billion-Customer Opportunity: Digital Accessibility").
- Methodology framed as Crawl / Walk / Run.
- Six "signs you need a design system" — diagnostic objection-handling layer.
- Same case studies as CareCentrix (Wendy's, T-Mobile Apeiron) plus Ford FDS.

### Definitions block
- "A digital product refers to any software-based offering or tool that generates revenue, helps improve efficiency or enhances customer experiences. Common examples: websites, mobile apps, various software applications."
- DS definition reused (identical to CareCentrix).
- Key Deliverables: UI Component Libraries (Design Library + Code Library — "designed and coded so designers/developers can re-use them consistently") and Usage Guidance & Documentation ("the single source of truth that defines how components should be used, styled, and implemented"). Other deliverables: accessibility guidelines, code standards, design patterns, design assets, content guidelines.
- "Often confused with…" disambiguation:
  - Style guide — visual + sometimes written elements of brand/project.
  - UI kit — collections of pre-built elements (Figma/Sketch libraries) for quick assembly.
  - Component library — reusable code that can be assembled into UI.
  - Brand design system — broader brand identity, messaging, tone of voice, brand values.

### Value framing — "Why design systems"
Three pillars:
- **Efficient** — Teams hit the ground running with pre-built foundations, components & templates that typically take weeks/months to define.
- **Accessible** — Built from the ground up to be accessible and meet WCAG 2.2 standards (note: 2.2 here, vs CareCentrix's 2.1 AA + 508).
- **Reusable** — Work created, replicated, maintained quickly at scale; unifies language across cross-functional teams.

"More time spent on more meaningful work."

**Why companies invest in design systems:**
- Scaling — replicate and maintain at scale.
- Efficiency — speed-to-market significantly improved.
- Reusability — minimizes redundant work; teams focus on more meaningful problems.
- Consistency — visual unity across products, channels, departments.
- Maintainability — apply change at scale.
- Simplicity — unified language develops within and between cross-functional teams.

**Quotes (industry, used as social proof):**
- "The efficiency savings for designers and front end developers using the design system: 40%–50%." — Robin Cannon, Global Design Systems Lead.
- "The four months of work to update our brand across all apps can now be accomplished in minutes." — Gerrit Kaiser, Design Leader.
- "In just three months, our design system solved 30% of our accessibility issues across 50+ products." — Jehad Affoneh, Head of Design.

**Time-to-Efficiency chart:** Productivity over time, with a curve showing "without a design system" (linear/flat) vs. "with a design system" (steeper after initial investment dip).

### Methodology — Crawl / Walk / Run

**CRAWL — Planning & Strategy**
"Planning and upfront strategy are crucial to ensure alignment with business goals, user needs and technical feasibility, ultimately leading to a cohesive and effective system."
- Assess & Audit — review existing component libraries/systems to identify redundancies, inconsistencies, accessibility concerns.
- Identify a tech stack — choose tools/frameworks that best support DS development, maintenance, integration into existing tech infrastructure.
- Create a blueprint — define overarching structure and organization of the DS (hierarchy of brands, platforms, products, frameworks).
- Stakeholder alignment — identify key stakeholders to establish communication and decision-making channels.
- Establish governance & processes — tailored creation/governance process so the DS is consistently maintained and evolves with org needs.

**WALK — Building & Scaling**
"Define design tokens and create core elements that set the foundation to scale the system for use across teams and platforms."
- Define Foundations — color palettes, typography, spacing, grid systems.
- Design Tokens & Variables — provide consumer product teams with ongoing assistance as they integrate/maintain.
- Core Components — foundational set of reusable components (buttons, inputs, grids), scalable and adaptable across platforms.
- Guidelines & Documentation — strategy ensuring consumer teams understand how to implement and continue to effectively utilize the system.
- Design Patterns — provide consumer product teams ongoing assistance as they integrate/maintain.

Foundations sub-callout: Color (accessible palettes + tokens for each brand theme); Typography (type scales + Figma styles for each brand); Grids (desktop/mobile web); Spacing (scales + variables); Icons (robust icon library + useful icons/logos).

Design tokens defined: "small, repeatable design decisions. A token can be a color, font style, unit of white space, or even a motion animation designed for a specific need."

Why tokens:
- Visual consistency across digital products.
- Enable themes (dark mode, different brands).
- Simplify design/dev by streamlining handoff.
- "As Thrive's visual language evolves, changes can be made once across the system and products. No more finding and replacing hard-coded values everywhere."

Themes: "a collection of token values designed to achieve a certain look or style." Switch color schemes/styles everywhere using a single set of tokens. Light/dark/brand are examples; non-color themes possible — "cozy/comfortable/compact views, reduced motion, custom typography styles."

**RUN — Performing & Optimizing**
"Monitor adoption, gather feedback, and continuously improve the design system while providing training and managing contributions for ongoing evolution."
- Adoption & Integration Strategy — strategy ensuring teams understand how to implement AND continue to use effectively. "Crucial to maximizing the system's potential."
- Support consumer teams — ongoing assistance as they integrate and maintain.
- Communication strategy — covers releases & changes, eliciting feedback, conducting roadshows, ensuring seamless onboarding for new teams.
- Collect Feedback — regularly gather input from designers, developers, stakeholders to identify improvements in design and functionality.
- Contribution Process — established process for proposing changes/additions; system evolves while maintaining quality and consistency.

### Discovery questions
The Thrive deck does NOT include an explicit discovery-questions section in the same structured way as CareCentrix — it ends with "Questions" as a closing slide (line 1071) but no enumerated question list. The diagnostic content is delivered instead via the "Six Signs You Need a Design System" framework.

### "Six Signs You Need a Design System" — diagnostic / objection-handling
1. **Inconsistent, Inaccessible UI & UX** — Problem: confusion/frustration; stems from fragmentation, miscommunication, no standardization. DS provides single source of truth — same reusable accessible UI components, patterns, layouts, fonts, colors, guidelines.
2. **Design and Technical UI Debt** — Problem: shortcuts/poor decisions cause inconsistencies, usability issues, fragmented UX. DS establishes unified UX principles, components, pattern library — shared understanding mitigates accumulation of debt.
3. **Difficulty Maintaining and Scaling Your Product** — Problem: complexity grows; design debt accumulates; updates are time/resource intensive. DS lays foundation for scalable design via reusable components, standardized patterns, clear guidelines.
4. **Communication Gaps Between Designers and Developers** — Problem: misunderstandings, inconsistencies, delays from misaligned expectations. DS = single source of truth bridging the gap with shared language and implementation methods.
5. **Slow Time to Market** — Problem: missed deadlines, increased costs, reduced competitiveness. DS streamlines the entire design/development process, enabling faster response to demands.
6. **Duplicated Design & Development Work** — Problem: teams unknowingly replicate efforts (e.g., building multiple versions of an app bar). DS = single source of truth + UI library + standardized patterns + accessible guidelines, eliminating redundancy.

### Case studies (Thrive)
- **Wendy's Fresh DS** — same content as CareCentrix.
- **T-Mobile Apeiron** — same content as CareCentrix.
- **Ford Design System (FDS, 2018–2022)** — vision work on Ford Mustang Mach-E sparked a global transformation; FDS unifies Ford brand across channels including in-vehicle. Brand themes between Ford & Lincoln "saved developers 90% of the time it would typically take for Lincoln." Numbers: 900+ designers/developers/PM/BO invited to onboard; 5 regions (NA, SA, EU, IMG, CN); 50 agencies with FDS access; 45 components in web library; 250+ licensed DSM users; 90+ devs with code kit access; 100+ Ford URLs impacted to-date; 55 sprints over two years; 2 2020 award nominations (Ford API; WPP Extraordinary). Component examples called out: Simple Tracker, Activity Indicator, Standard Button, Standard Outline Button, Toggle, Filter Chip, Carousel Indicator, Standard Input, Floating Action button.

### Notable language / framing (Thrive)
- "A library of solved problems."
- "More time spent on more meaningful work."
- "Design systems are a perfect pair to accessibility." — Anna Zaremba, Senior Design Lead at eBay.
- "Accessibility can be baked into every part of a design system, from carefully tested foreground and background colors to individual components."
- "Underserved market" / "new levels of growth, market credibility, and trust" (accessibility ROI framing).
- "Less time testing for, and remediating, accessibility issues in development and QA."
- "Crawl / Walk / Run" as the methodology meta-frame.

---

## Phase-tagged findings (canonical 8 phases)

Mapping deck content to the canonical 8 phases:

**1. Discovery & Strategy**
- CareCentrix Phase 1 (Discovery): brand onboarding, application audit, stakeholder alignment, definition sessions, component backlog, design direction, north star.
- Thrive Crawl: Assess & Audit, Identify a tech stack, Create a blueprint, Stakeholder alignment, Establish governance & processes.
- Both call out a prioritized component backlog and a "north star" / blueprint as discovery outputs.

**2. Design Foundations**
- CareCentrix Phase 2 (Foundations): Figma setup as source of truth; naming & token architecture (primitive/semantic); color, typography, spacing systems; W3C DTCG-compliant tokens; accessibility baseline (contrast, type, focus); digital style guide.
- Thrive Walk: Define Foundations (color, type, spacing, grids); Design Tokens & Variables; Themes.
- Tokens called out as "subatomic" in CareCentrix's atomic-design model.

**3. Component Library**
- CareCentrix Phase 3 (Build): component architecture (foundational → composite → containers); component design on token foundation; design patterns for data-heavy tooling.
- Thrive Walk: Core Components (buttons, inputs, grids — "scalable and adaptable across platforms").

**4. Documentation**
- CareCentrix: usage documentation per component (purpose, states, do/don't, accessibility notes); design patterns documentation; content guidelines; UX Designer "owns the documentation strategy."
- Thrive: "Usage Guidance & Documentation" called out as a top-line key deliverable; "Guidelines & Documentation" is a Walk activity.

**5. Development Support**
- CareCentrix: Engineering team available for alignment sessions in discovery and at incremental handoffs; pilot validation in Storybook; "we work alongside your team throughout"; Design Systems Lead "collaborates with the engineering team to ensure design decisions are implementable."
- Thrive: T-Mobile Apeiron case study lists "Support for teams including Getting Started guides and integration support" as a deliverable.
- Note: CareCentrix explicitly excludes front-end development / code delivery from scope. Dev support means *alignment* and *handoff*, not implementation.

**6. Pilot & Implementation**
- CareCentrix: explicit "Pilot validation with engineering" milestone in both timeline options; Backoffice Portal POC discussed as a likely "primary pilot target" in discovery questions.
- Thrive: less explicit, but Ford and T-Mobile case studies show piloted-then-scaled adoption.

**7. Governance & Adoption**
- CareCentrix: Option 2 (16–24 weeks) explicitly "creates space for system-wide readiness, broader organizational adoption, and long-term scalability" — but governance is light in this deck (no dedicated section).
- Thrive Crawl includes "Establish governance & processes" as a Day-1 activity ("tailored creation and governance process ensures the DS is consistently maintained and evolves").
- Thrive Run: Adoption & Integration Strategy is the dedicated phase; communication strategy + roadshows + onboarding.

**8. Ongoing Maintenance**
- CareCentrix: largely out of scope for these engagements (engagement ends with library handoff); supporting roles framed as bucket-of-hours.
- Thrive Run: Support consumer teams; Collect Feedback; Contribution Process — the most explicit articulation of ongoing maintenance across the two decks.

**Phase coverage observation:** CareCentrix is a *build engagement* (phases 1–3 + a sliver of 5/6); Thrive is a *capability/POV deck* (covers all 8 conceptually but doesn't price any of them). Governance + Ongoing Maintenance are weakest in CareCentrix and strongest in Thrive's Run phase.

---

## Principles & philosophy (cross-cutting)

- A DS is a **product**, not a project — "infrastructure, not a one-time deliverable."
- "Built once. Used everywhere."
- The DS is a **library of solved problems** so teams can focus on the unsolved 20%.
- **Co-built with engineering**, not handed off — incremental handoff, alignment sessions throughout.
- **Tokens are foundational** — W3C DTCG-compliant, primitive/semantic structure, platform-agnostic.
- **Accessibility is built in, not retrofitted** — WCAG 2.1 AA / Section 508 (CareCentrix); WCAG 2.2 (Thrive).
- **Themes are how scale happens** — light/dark, multi-brand, density (cozy/comfortable/compact), reduced motion, custom typography.
- **Brand → Digital Styles & Foundations → UI Component Libraries → Product** — clear ownership boundaries between brand team, DS team, product teams.
- **Atomic design** as the structural mental model: Subatomic (tokens) → Atomic → Molecule → Organism → Template.
- **Internal tools deserve customer-facing craft.**
- **Crawl / Walk / Run** as the maturity framing (Thrive).
- **Discovery as alignment, not analysis** — "Discovery is where alignment happens."
- **Documentation is the single source of truth** — owned by a dedicated UX Designer role.
- **Consistency without rigidity** — flexibility for varying density needs.

---

## Selling design systems (cross-cutting)

### Problem statements (used to set up the sale)
- Inconsistent, inaccessible UI & UX → user confusion/frustration; brand erosion.
- Design + technical UI debt → consequences of shortcuts compound over time.
- Difficulty maintaining/scaling product → updates become time/resource intensive.
- Communication gaps between designers and developers → misinterpretations, rework.
- Slow time to market → missed deadlines, increased cost, reduced competitiveness.
- Duplicated design + dev work → teams unknowingly rebuild app bars / components in silos.
- (CareCentrix-specific) Internal tools that engineers depend on every day are under-invested in compared to customer-facing products.

### ROI / value claims (specific numbers used)
- 40%–50% efficiency savings for designers and front-end developers (Robin Cannon).
- "4 months of brand-update work → minutes" (Gerrit Kaiser).
- 30% of accessibility issues across 50+ products solved in 3 months (Jehad Affoneh).
- 65% of companies use DS as of 2020 (and growing).
- Wendy's Fresh: 4000 lines of code removed; 600% time-to-market increase; 25 critical accessibility issues remediated; 22 devs + 15 designers supported.
- T-Mobile Apeiron: 500 design tokens; 2 brand themes; 3 platforms; 39-person team; 20 pages of usage guidance.
- Ford FDS: 90% time savings switching brands (Ford ↔ Lincoln); 900+ people onboarded; 5 regions; 50 agencies with access; 100+ Ford URLs impacted; 55 sprints; 2020 award nominations.
- Accessibility market: 1B disabled people / $1.2T disposable income.
- "80% of design and development needs" addressed by the system (the recurring 80/20 pull-quote).

### Objection handling (Thrive's "6 signs" double as objection answers)
- "We can fix consistency without a DS" → addresses fragmentation root cause.
- "It's too expensive / not the right time" → tech-debt-now-or-later framing.
- "Our product can't scale this way" → DS as foundation for scale.
- "Designers and devs already collaborate" → shared SoT vs. lossy handoff.
- "We need to ship faster" → DS is the speed unlock.
- "We don't duplicate work" → in fact, every team rebuilds the app bar.

### "Why VML" / differentiation
- "Fusion of capabilities" diagram positions VML uniquely vs. four competitor categories: Creative Agencies (full digital growth services), Marketing (strategic enhancement without implementation), Consulting Firms (offerings, fragmented delivery), System Integrators (implementation only, lack of strategic offerings). VML's core capabilities span Consulting / Communication / Production / Experience / Commerce / Technology / Data.
- "Human First" framing — start with people, design with empathy, intention over automation.
- Embedded model: work alongside engineering from day one; incremental handoff.
- Track record across food (Wendy's), telco (T-Mobile), auto (Ford) — proof of multi-platform, multi-brand, accessibility-first systems.
- Roles bench: dedicated Design Systems Lead, dedicated Accessibility Specialist, dedicated UX Copywriter for content standards.

### Pricing / sizing language (CareCentrix)
- Option 1 — 12–16 weeks — $230k–$320k — MVP system.
- Option 2 — 16–24 weeks — $320k–$500k — extended set + adoption-readiness.
- Same team composition; allocation varies by length.
- "Costs are shown as a range to provide flexibility based on final scope and level of support."
- Caveats: "This estimate is based on the scope and assumptions outlined in this proposal. Changes to scope, timeline, or client availability may affect the final investment."
- Accessibility audit work explicitly framed as a scope addition.

---

## Frameworks, models, named concepts

- **Brand → Digital Styles & Foundations → UI Component Libraries → Product** four-layer ownership model (attributed in Thrive deck to Josh Clarke, Big Medium — "Design Systems at Scale: Episode 2").
- **Atomic Design** (Subatomic / Atomic / Molecule / Organism / Template) — used in CareCentrix.
- **Three-phase methodology** (CareCentrix): Discovery → Foundations → Build, with incremental handoff.
- **Crawl / Walk / Run** (Thrive): Planning & Strategy → Building & Scaling → Performing & Optimizing.
- **Primitive / Semantic token architecture** (CareCentrix Foundations).
- **W3C DTCG-compliant design tokens** (CareCentrix — explicit standard; "ready for consumption as your stack evolves").
- **Themes** as collections of token values — light/dark/multi-brand + non-color (cozy/comfortable/compact, reduced motion, custom typography).
- **Six Signs You Need a Design System** (Thrive diagnostic).
- **Time-to-Efficiency curve** (Thrive — productivity over time, with vs. without a DS).
- **Fusion of capabilities** matrix (CareCentrix "Why VML").
- **80/20 rule** — system handles 80% of design/dev needs.
- **Accessibility = the perfect pair** (Thrive metaphor).
- **"Library of solved problems"** (Thrive metaphor).
- **"Built once. Used everywhere."** (CareCentrix headline).
- **Design language partner** (CareCentrix positioning of VML).
- Accessibility standards: **WCAG 2.1 AA + Section 508** (CareCentrix, healthcare-specific) vs. **WCAG 2.2** (Thrive).

---

## Notable quotes (verbatim)

- "Thank you for the opportunity to partner with you on something that matters — not just to your engineering team, but to every person who depends on your internal tools to do their job well." (CareCentrix cover letter)
- "What we see isn't a design refresh — it's a foundational investment in how CareCentrix operates." (CareCentrix)
- "A design system is infrastructure, not a one-time deliverable." (CareCentrix)
- "The best systems are built with the teams that use them — which is why we work alongside your engineers from day one, not just hand off at the end." (CareCentrix)
- "Built once. Used everywhere." (CareCentrix)
- "A design system is not just a UI library—it's a product serving the organization." (CareCentrix)
- "The system addresses 80% of design and development needs so they can focus on the other 20%." (Both decks; cited as "You Need A Design System — Here's Why")
- "A great design system for internal tooling isn't just about visual consistency — it's about making your engineers faster and your tools more trustworthy to the people who depend on them every day." (CareCentrix)
- "Discovery is where alignment happens. Before a single component is designed, we establish the principles, priorities, and direction that guide everything that follows." (CareCentrix)
- "Handoff is incremental, not a moment. As components are completed, they're handed off to engineering — so your team starts building with the system before the engagement ends." (CareCentrix)
- "Compliance is built in, not retrofitted." (CareCentrix Accessibility Specialist role description)
- "Consistency without rigidity." (CareCentrix re: spacing for varying density)
- "A design system provides a library of solved problems delivered as reusable UI elements, guidelines, and patterns." (Thrive)
- "More time spent on more meaningful work." (Thrive)
- "Design systems are a perfect pair to accessibility." — Anna Zaremba, eBay (Thrive)
- "Accessibility can be baked into every part of a design system, from carefully tested foreground and background colors to individual components." — Anna Zaremba (Thrive)
- "The efficiency savings for designers and front end developers using the design system: 40%–50%." — Robin Cannon (Thrive)
- "The four months of work to update our brand across all apps can now be accomplished in minutes." — Gerrit Kaiser (Thrive)
- "In just three months, our design system solved 30% of our accessibility issues across 50+ products." — Jehad Affoneh (Thrive)
- "In 2020, 65% of companies said they use design systems, and that will only increase." (Thrive — "You Need A Design System — Here's Why")
- "As Thrive's visual language evolves, changes can be made once across the system and products. No more finding and replacing hard-coded values everywhere." (Thrive)
- "Saved developers 90% of the time it would typically take for Lincoln." (Thrive Ford case)
- "Wendy's has the potential to be the most accessible food ordering app ever, and be a gold star standard for screen reader experiences when ordering tasty nuggs." (Both decks)

---

## Tensions / contradictions (deck-to-deck evolution Sep 2024 → Mar 2026)

1. **Methodology naming.** Thrive uses **Crawl / Walk / Run** (5 activities per phase, total 15). CareCentrix uses **Discovery / Foundations / Build** (3 phases, more concrete tasks/deliverables, with incremental handoff layered through). Same conceptual arc, but CareCentrix is operationally tighter and tied to a price.

2. **Accessibility standard.** Thrive cites **WCAG 2.2**. CareCentrix cites **WCAG 2.1 AA + Section 508**. The shift is likely deliberate — CareCentrix is a US healthcare org where 508 is the legal anchor — but it's worth being aware of: Thrive used a newer standard; CareCentrix scopes to the older AA + 508 baseline. (May reflect a more conservative procurement context.)

3. **Governance + Maintenance coverage.** Thrive's "Run" phase is rich (adoption strategy, support, communication strategy, feedback collection, contribution process). CareCentrix's engagement options largely END at handoff — Option 2 nods to "system-wide readiness, broader organizational adoption" but there's no formal governance or contribution process deliverable. The CareCentrix engagement is scoped tighter and lighter on the Run phase.

4. **Scope of dev support.** CareCentrix is explicit: NO front-end dev, NO code delivery, NO engineering implementation. Thrive's case studies (T-Mobile, Ford) describe code libraries and dev support as part of the work. The 2026 sales motion appears to have narrowed: design+docs only, with engineering doing implementation.

5. **Discovery question style.** CareCentrix has an explicit, structured discovery questions section (10 questions across 4 categories). Thrive ends with a generic "Questions" slide and embeds discovery thinking inside its diagnostic "6 signs" content. The 2026 deck is more procurement-savvy.

6. **Token standard explicitness.** CareCentrix names the **W3C DTCG** standard explicitly. Thrive talks about tokens generally without that compliance anchor. CareCentrix has matured the technical framing.

7. **Internal vs. customer-facing positioning.** CareCentrix leans hard into "internal tools deserve customer-facing craft." Thrive is more general-purpose. The 2026 deck reflects a thesis that internal tooling is an underserved DS market.

8. **Voice/role of UX Copywriter.** CareCentrix names a UX Copywriter as a discrete supporting role with hour budget; Thrive doesn't call this out. Content standards have been operationalized in 2026.

9. **"Why VML" framing.** CareCentrix has a clearer competitor matrix (vs. creative agencies / marketing / consultancies / SIs). Thrive's "why VML" is implicit through case studies. CareCentrix is more positioned/sales-ready.

10. **Brand themes as a feature.** Both decks emphasize themes. CareCentrix expands the definition (cozy/comfortable/compact, reduced motion) — same language appears in Thrive, suggesting a stable VML POV.

---

## Gaps

What's missing or under-developed across both decks that the practice may want to strengthen:

- **Governance models.** Neither deck offers a concrete governance framework (e.g., contribution model with intake → triage → review tiers; federated vs. centralized model articulation; RACI for proposals). Thrive names the activity; neither deck shows a deliverable.
- **Adoption metrics / success measurement.** No KPIs proposed. Adoption rate, component coverage %, time-saved, ticket reduction, accessibility defect rate over time, etc. — would strengthen the ROI story beyond the third-party quotes.
- **Roadmap/lifecycle artifacts.** No roadmap template, versioning policy, deprecation policy, breaking-change policy, or release cadence shown.
- **Pricing for ongoing/Run phase.** CareCentrix prices Discovery/Foundations/Build only; no retainer, support tier, or governance subscription model offered for after handoff.
- **Tech architecture beyond Figma.** Storybook is mentioned in passing for component validation. No discussion of code-side architecture (Style Dictionary, Tokens Studio, build pipelines, CI/CD for tokens), framework strategy (React/Vue/Web Components), or how tokens flow from Figma to production codebases.
- **Research integration.** CareCentrix explicitly excludes UX research from scope. Neither deck addresses how user research feeds a system's pattern decisions or how usability validation works after launch.
- **Pattern library depth.** Patterns are listed but not deeply illustrated. No mention of complex patterns like wizards, dashboards, empty states, onboarding flows, permissions/role patterns.
- **Internationalization / localization.** Not addressed in either deck. Ford case touches on regions but doesn't articulate a localization model.
- **Motion / animation.** Mentioned in CareCentrix token list (motion) but not as a foundation with its own treatment.
- **Data viz / charting.** Not addressed — relevant for both healthcare (CareCentrix) and finance (Thrive).
- **Multi-brand / sub-brand architecture playbook.** Brand-theme switching is shown in cases but not generalized into a method.
- **AI / agent-ready DS thinking.** No mention of how the DS supports AI-generated UI, design-to-code automation, MCP/agent consumption, semantic component metadata. Worth adding given the 2026 timeframe.
- **Discovery questions for Thrive.** No verbatim list — would benefit from a parallel structured set if the deck is reused.
- **Org change management.** Workshops, training, champion programs, roadshows are mentioned in Thrive's Run but not scoped or productized.
- **Pilot definition.** "Pilot validation with engineering" is named but not defined: what makes a pilot successful, exit criteria, scope of pilot.
- **Documentation publishing/IA.** Where the docs live (Zeroheight, Storybook docs, custom site, Figma) and information architecture for docs is not discussed.

# Notes: DesignSystems-VML-2024-2026 (full)

## Source meta

- **File:** `/Users/aforrester/Library/CloudStorage/GoogleDrive-adam.forrester@vmlyr.com/My Drive/Design Systems/Knowledge Base/DS-KnowledgeBase/_source-text/vml-library.txt`
- **Origin:** DesignSystems-VML-2024-2026.pdf, ~250 slides, 86MB. Practice's flagship internal reference (the "Selling 2024 / Grab N' Go Slides" deck), with internal authorship by Adam Forrester (Group Director, XD | KC), Aaron May (Director, XD | CIN), Sofia Andreadis (Program Director | CIN), Sam Thompson (Director, Technology | KC).
- **Total lines:** 5,429
- **Section transitions identified (line ranges are approximate, set by chapter divider slides):**
  - Front matter / one-pager / Gartner Hype Cycle reprint: lines ~1–146
  - **Section 1 — Design Systems at VML:** lines ~147–340 (chapter divider at line 161, "01 Design systems at VML")
  - **Section 2 — Understanding Design Systems:** lines ~341–900 (divider at line 343, "02 Understanding design systems")
  - **Section 3 — Why Design Systems?:** lines ~903–1418 (divider at line 916, "03 Why Design Systems?")
  - **Section 4 — Our Process:** lines ~1419–2244 (divider at line 1413, "04 Our Process"). Sub-phases: Planning & Strategy (~1420–1696), Architecture & Governance (~1700–1932), Creation & Implementation (~1933–2150), Adoption/Support/Comms (~2151–2233)
  - **Section 5 — When a Design System is Needed:** lines ~2245–2398 (divider at line 2248, "05 When a design system is needed")
  - **Section 6 — Case Studies:** lines ~2399–3134 (divider at line 2411, "06 Case Studies"; covers Wendy's Fresh, T-Mobile Apeiron, Ford FDS)
  - **Section 7 — Scoping & Team Building:** lines ~3135–3517 (divider at line 3147, "07 Scoping & Team Building")
  - **Section 8 — PRISM:** lines ~3518–3800 (divider at line 3531, mistakenly labeled "07 PRISM" — actually the 8th section)
  - **Appendix:** lines ~3801–5429 (corporate VML one-pager, Selling DS deck objectives, "Design Systems as Infrastructure" / AI essay, Tech Discussion deck, Governance scaling content, Vision)

---

## Section 1 — Design Systems at VML

### Practice positioning (verbatim from front-matter one-pager, lines 10–48)

> "We provide expert guidance in developing and supporting enterprise design systems built to suit our client's specific requirements and needs."

> "By combining the expertise of XD, technology, and solutions delivery, we collaborate closely with organizations to develop bespoke, comprehensive and scalable design systems that empower enterprises to streamline their design and development processes. In doing so we foster consistency, efficiency, and brand cohesion across our clients' digital products, leading to enhanced user experiences and accelerated product delivery."

### Service stack (4 named offerings)

1. **Design System Development** — bespoke, comprehensive, scalable systems via XD + technology + solutions delivery.
2. **Strategy** — system architecture, roadmaps & priorities, team structure & processes, release & communication strategies, adoption & support strategies. Explicitly framed as "scalable across brands and platforms."
3. **Consulting & Training** — best practices, emerging trends, usability & accessibility, plus workshops to educate client design and dev teams.
4. **Integration & Support** — integrating DS into existing workflows/tools; tech support during implementation.
5. **Maintenance & Optimization** — ongoing support, maintenance, updates, audits, continuous improvement.

(Note: deck enumerates 5 offerings under a 4-pillar logic — Strategy is also called out separately.)

### Target customer & ideal circumstances

- **Customer:** "marketing and technology executives striving for a streamlined design and development processes by creating a scalable foundation for new or existing products."
- **Ideal trigger circumstances:** organizations experiencing growth, embarking on digital transformation, facing design inconsistencies, seeking to improve collaboration, or aiming to strengthen/renew brand identity.
- **Client-Partner Desired Impact:** "elevate customer experience through consistency across multiple products, drive efficiency and speed to market, and foster innovation."

### Competitive landscape

- Named competitors: Deloitte, Accenture, Sapient, "smaller digital design system consultancies."
- **Reasons to believe:**
  - "Quickly stand up a large cross-functional team"
  - "Specialized offering and experience creating enterprise design systems"
  - "Can be paired with other CX or Brand Studio offerings"

### Core competencies & tools (verbatim list)

- **Competencies:** Design thinking; Visual & Interaction design; Front-end Development; Collaboration & Communication; Solutions Delivery & Project Management.
- **Tools:** Figma; GitHub/GitLab; Documentation platforms (Knapsack, Supernova, ZeroHeight); Jira; Storybook.

### Investments/Bets Required to Win (verbatim)

- Expanding agency teams' expertise in design systems across disciplines
- Agency-funded design system documentation tool
- Increased cross-functional collaboration
- Accessibility knowledge across design & technology
- A system mindset towards product development
- Funding to create an internal design system to demonstrate capabilities and utilize as a project starter for teams (→ Prism)

### Practice leadership (line 132)

Adam Forrester (Group Director, XD | KC), Aaron May (Director, XD | CIN), Sofia Andreadis (Program Director | CIN), Sam Thompson (Director, Technology | KC).

### Embedded Gartner Hype Cycle reprint (lines 53–100)

Used as third-party validation. Cites: Benefit Rating: High; Market Penetration: 5–20%; Maturity: Adolescent. Drivers (Speed, Usability, Consistency, Scale, Reduction of defects, Brand compliance, Accessibility, AI-Ready). Obstacles (effort to maintain, lack of governance, cross-discipline buy-in, executive buy-in, originality fears).

---

## Section 2 — Understanding Design Systems

### Core narrative arc (lines 350–449, "Unprepared → Organized → Deliberate")

The deck builds the conceptual case in a sequenced reveal:

1. "A digital product refers to any software-based offering or tool that generates revenue, helps improve efficiency or enhances customer experiences."
2. "A common approach is to just start building a product, with our focus solely on the end result." (Unprepared)
3. "But when we take time to organize the parts we can produce better work in a shorter amount of time." (Organized)
4. "And we have a set of patterns that can be utilized to create similar products in a more deliberate and efficient way." (Deliberate)

### Definition (verbatim, primary, line 452)

> "A design system is a collection of UI elements built as reusable code. They are guided by clear standards that help organizations deliver cohesive, on-brand experiences at scale, over time. **It is not:** A style guide, a UI kit, or a brand system. (But can include these)."

### Alternate definitions used

- "A Design System is a systematic approach to front-end digital product design. It uses guidelines, principles, and code to scale design, collaborate, and create more space to focus on complex problems." (line 434)
- "A design system provides a library of solved problems delivered as reusable UI elements, guidelines, and patterns." (line 417)
- Client-friendly metaphor (line 178): "A design system is like a digital recipe book for your brand."

### Anatomy / Key Deliverables (line 479)

- **Pre-built Components:** Design Library + Code Library — "designed and coded in a way that makes it easy for designers and developers to re-use them consistently."
- **Usage Guidance & Documentation:** "single source of truth that ensures all team members are on the same page regarding how components should be used, styled, and implemented."
- **Other deliverables:** Accessibility guidelines, code standards, design patterns, design assets, content guidelines.

### "Often confused with…" disambiguation (line 506)

- **Style guide:** outlines visual/written elements of a brand or project (color, type, imagery).
- **UI kit:** pre-built elements to assemble UI quickly; typically Figma/Sketch library.
- **Component library:** reusable code only.
- **Brand design system:** broader brand identity — visual, messaging, tone, values.

### Hierarchy: Brand → DS → Product (line 533)

> "The brand defines the design language and the design system translates that into digital styles and libraries of user interface elements that can be utilized by all product teams."

Layered model:

1. **Brand Team** → Brand Identity / Design Language (logos, colors, fonts, tone of voice, photography, usage guidance)
2. **Design System Team** → Digital Styles & Foundations (accessible color scales, digital type scales, spacing & grids, UX writing guidelines) → Component Libraries (UI design & code libraries, common design patterns, best practices, usage guidance)
3. **Product Teams** → Product (product-specific local libraries)

### Quoted experts in this section

- Josh Clark, Big Medium — "Design Systems at Scale: Episode 2" (line 468, no quote text extracted)
- "The system addresses 80% of design and development needs so they can focus on the other 20%." — *You Need A Design System — Here's Why* (line 578)
- "You can't innovate on products without first innovating the way you build them." — Alex Schleifer, Airbnb (line 706)

### Maturity model: Chaos → Silos → Integration (line 604, verbatim)

**CHAOS** (signs):
- Reactive; no structured process; no long-term vision; no KPIs, no connection with business goals; design maturity is lacking; "Using a UI kit and calling it a design system"; constantly fixing "urgent" issues; lots of subjective thoughts, no data-backed decisions; patching components from different files and UI kits.

**SILOS:**
- Bigger org, more design teams; each team focuses solely on own KPIs; siloed DS team, insufficient syncing with product design; absence of feedback loops; product roadmaps not in sync; ineffective in broader strategy.

**INTEGRATION:**
- DS and product design aligned; involves strategic design; data-driven decisions, KPIs tracked; connected with business goals; cross-functional team; iterative process, changes logged; regular feedback loops; efficient design processes; cohesive UX; drives innovation; higher ROI.

> "You're burning cash when your product design and design systems aren't in sync. Period."

### Ben Callahan / Sparkbox quote (line 624, important verbatim)

> "The best design systems are simply a force multiplier for what's already happening inside an organization. Those systems refactor the already established practices and patterns of the org so they can be used everywhere. If your organization has healthy practices and patterns, your design system can help scale those across teams/brands/channels/etc. If your organization has unhealthy practices, expecting a design system alone to fix those practices is misplaced optimism. Design systems distill and magnify healthy practices and patterns while exposing and challenging unhealthy ones. The amount of resistance a healthy design system team experiences is directly related to the unhealthiness of the organization's established ways of working."

### Concept diagram (line 644, "Digital Design Systems" wheel)

Inputs orbiting a central "Digital Design Systems" hub:
- Content Design (Content Strategy, Voice & Tone)
- Design (Principles)
- Foundations (Brand)
- UI Kit (Design Tokens)
- Code

### "Design Systems are…" attributes deck (line 717+)

innovative; scalable; modular; efficient; collaborative; complex; for people; a big deal; critical.

### Emphatic positioning (line 595)

> "A Design System is not a deliverable, but a set of deliverables. It will evolve constantly with the product, the tools and new technologies."

---

## Section 3 — Why Design Systems?

### "Why companies invest" (verbatim list, line 928)

- **Scaling** — Work can be created, replicated, and maintained quickly and at scale.
- **Efficiency** — Speed-to-market is significantly improved across teams.
- **Reusability** — Sharing solutions minimizes redundant work so teams can focus on more meaningful problems.
- **Consistency** — Visual unity across products, channels, and departments.
- **Maintainability** — Teams and experience can more easily apply change at scale.
- **Simplicity** — A unified language develops within and between cross-functional teams.

### Stat callouts

- "In 2020, 65% of companies said they use design systems, and that will only increase." (line 962)
- Robin Cannon, Global DS Lead: **"The efficiency savings for designers and front end developers using the design system: 40%–50%."**
- Gerrit Kaiser, Design Leader: **"The four months of work to update our brand across all apps can now be accomplished in minutes."**
- Jehad Affoneh, Head of Design: **"In just three months, our design system solved 30% of our accessibility issues across 50+ products."**

### Twelve named value arguments (one per slide, lines 985–1172)

1. Consistency and Cohesion
2. Adaptability and Flexibility
3. Efficiency and Speed
4. Cross-Functional Collaboration
5. Scalability
6. Empowered Decision-Making
7. Accessibility at its core
8. Streamlined Updates
9. Reduced Duplication and Technical Debt
10. Improved User-Centered Design
11. Foster Innovation
12. Cultural Shift — "the adoption of a design system often requires a cultural shift within the organization."

### Accessibility business case (line 1316)

> "With 1 billion disabled people worldwide holding $1.2 trillion in annual disposable income, making your websites, apps, and customer portals accessible to people with disabilities isn't some compliance burden to be met or lawsuit to be avoided. It's a chance to embrace an underserved market…"

Quote, Anna Zaremba (eBay): "Design systems are a perfect pair to accessibility. Accessibility can be baked into every part of a design system, from carefully tested foreground and background colors to individual components."

### ROI calculator (line 1341, verbatim concrete numbers)

- **Button component:** Used 75x. Built per-use: 1,500 hrs. Built for reuse & shared: 485 hrs. Hours saved: 1,015. **Efficiency gain: 67.7%.**
- **Dynamic menu component:** Used 18x. Built per-use: 2,520 hrs. Built for reuse: 476 hrs. Hours saved: 2,044. **Efficiency gain: 81%.**
- "Calculate ROI for your company with the design system ROI calculator." (referenced — implies an external tool exists/is linked)

### "Time to Efficiency" curve (line 1380)

Two productivity curves; "with DS" investment dips below baseline initially, then crosses over and pulls ahead long-term.

### Aphorism (line 1367)

> "A key practice in scaling design across an organization is aligning on a common set of principles, foundations, components, guidelines & resources."

---

## Section 4 — Our Process (CRITICAL)

The VML methodology is structured into **3 named macro-phases**, each with its own sub-steps. The 3 phases:

1. **Planning, Strategy & Architecture** ("Kicking off the design system")
2. **Creation & Implementation** ("Building & Scaling")
3. **Adoption, Support & Comms** ("Performing & Optimizing")

### Macro-phase 1 — Planning & Strategy (lines 1419–1696)

> "Planning and upfront strategy are crucial to ensure alignment with business goals, user needs and technical feasibility, ultimately leading to a cohesive and effective system."

**Five-column intro slide (line 1438) lists these as the headline activities:**

1. **Assess & Audit** — "Review the existing component libraries or systems to identify redundancies, inconsistencies and accessibility concerns."
2. **Identify a tech stack** — "Choose the tools and frameworks that will best support the design system's development, maintenance, and integration."
3. **Create a blueprint** — "Define the overarching structure and organization of the design system. This involves determining the hierarchy and structure of the brands, platforms, products, and frameworks."
4. **Stakeholder alignment** — "Identifying key stakeholders within the organization helps establish effective communication and decision-making channels."
5. **Establish governance & processes** — "Crafting a tailored creation and governance process ensures that the design system is consistently maintained and evolves with the needs of the organization."

**Detail slides break this out further (lines 1483–1696):**

- **Assess Existing Libraries and Design Systems** — Review existing design assets, component libraries, and any existing systems. Identify redundancies, inconsistencies, accessibility concerns, areas for improvement.
- **Audit Digital Products and Experiences** — Assess current digital products. Understand how products are designed and used so the new system supports existing products and addresses UX pain points and accessibility issues.
- **Define a system blueprint** — Hierarchy/structure of brands, platforms, products, frameworks.
- **Define a tech stack** — Collaborate with partner's technology team.
- **Create a design system roadmap** — "phased approach for design system development, including milestones, deliverables and timelines, ensuring a well-paced and manageable project that delivers value quickly to consuming products."
- **Define stakeholders** — Ensure design, dev, product management are represented and aligned.
- **Define structure for the design system team** — "designers, developers, product managers, and QA, with clear roles and responsibilities, regular communication, and shared goals."
- **Defining creation and governance processes** — How components are created, approved, documented, updated.
- **Create a custom design system playbook** — Compile a comprehensive playbook specific to the client's organization.

**The 20 strategic discovery questions (line 1642, verbatim):**

> "We ask the right questions to drive the strategy and processes to ensure your design system is successful."

1. What is important to our organization at the highest level?
2. What design and code assets do we have at our disposal?
3. Who is important to our design system effort?
4. What work is coming up soon for our teams?
5. What unofficial systems already exist in design and code, even if they're not intentional or documented anywhere?
6. Which teams have upcoming needs that a design system could solve?
7. Which teams have the most immediate interface needs that can most effectively grow our design system?
8. Which teams should we and have we talked to?
9. Which stakeholders should we and have we talked to?
10. What opportunities already exist for systemization and scaling in the near future?
11. How can a design system fit seamlessly into the larger ecosystem of our organization's tools and technologies?
12. What end user problems and opportunities could a design system address?
13. What needs, desires, and concerns do our stakeholders have? What do they share?
14. What components do product or feature teams need now or soon?
15. What is our repeatable process for working on products and features?
16. What shared language can we start to use?
17. What components will we start with?
18. What information do our consumers need from a reference website?
19. When will we be working on each component?
20. How does our team make decisions?

### Architecture sub-phase (lines 1700–1776)

> "A design system is not just a UI library—it's a product serving the organization. Strong architecture enables: Consistency across teams and products. Efficiency in building and maintaining experiences. Quality and scalability at every layer."

**Foundational strategy & alignment**

- **Purpose & Principles (The North Star):** "Define why the design system exists and who it serves… clear, opinionated principles as decision-making tools… Aligns the system with organizational goals."
- **Discovery & Audits:** Asset & Code Audits (duplicate/divergent patterns); Ecosystem Mapping (product relationships & user journeys); Customer Interviews (designers, developers, PMs).
- "These activities ground the system in reality and identify where it can create the most impact."

**Architectural Models & Hierarchy**

- **Hierarchical Component Model:** Foundations → Components → Patterns → Templates → Pages. "Supports both Atomic Design and system-driven vocabularies."
- **Tier model:** Core Tier (essential, system team-maintained); Lower Tiers/Shared Libraries (sandbox for experiments and future promotion).
- **Namespace & Documentation:** Centrally curated namespace; naming as cross-disciplinary exercise.

**Technical Architecture Practices**

- **Visualize the Technical Ecosystem:** blueprint for design tokens, component libraries, UI kits, documentation site, guidelines.
- **Design Tokens as the Backbone:** single source of truth for color, type, spacing, motion. Implement via **Style Dictionary** for platform-specific outputs.
- **Repositories & Environments:** self-contained system repository packaged for consumption (npm, GitHub); public workshop environment (Storybook or equivalent).
- **Code Standards & Accessibility:** modular reusable code; enforce style guides with tooling/linting; accessibility built into components by default.

### Governance sub-phase (lines 1751–1932, also re-stated in lines 5079–5247 with edits)

**Multi-brand governance challenges:**
- Uncoordinated Contributions
- Competing Opinions
- Process Confusion

**Three governance approaches (verbatim):**

1. **Fully centralized:** A single core system with theming capabilities for brand-specific visual styles
2. **Federated:** A central system with defined extension points where brands can customize components
3. **Distributed with governance:** Brand-specific systems that adhere to shared principles and standards

**Recommended model:** "Centralized Model — A centralized model features a dedicated team responsible for the design system's development and maintenance. This approach provides clear ownership and accountability but may sometimes disconnect from day-to-day product needs if not carefully managed."

**Governance Best Practices (4 named):**

1. **Define Clear Roles** — explicitly state who owns, decides, contributes.
2. **Establish Intake & Contribution Processes** — straightforward workflows for proposing changes.
3. **Implement Version Control** — semantic versioning, changelog, deprecation strategy.
4. **Regular Reviews and Communications** — scheduled cross-team meetings; monthly/quarterly org-wide updates.

**Component Governance (4 strategies):**

1. Component Qualification (problem solved, differentiation, reusability across brands, technical feasibility & accessibility)
2. Component Request and Intake
3. Component Testing — content, accessibility, cross-browser/device, responsive, functionality, stress tests, internal code review, internal design review, application trials, internal QA
4. Contribution Workflow — proposal w/ use case → design/dev specs → peer review → cross-brand testing → docs → final approval → distribution & announcement

**Documentation Governance:** typography, color, spacing, icons, components, interface patterns; matures to include code snippets, usage examples, contribution guidelines. Standards: writing tone/style, required info per component, examples & implementation, accessibility, brand variations.

**Accessibility Governance:** WCAG 2.0 AA baseline; strive for 2.1 AA or 2.2. Centralized testing + brand-specific testing.

### Macro-phase 2 — Creation & Implementation (lines 1933–2150)

> "Building & Scaling — Define design tokens and creation core elements that set the foundation to scale the system for use across teams and platforms."

**Five-column headline activities:**

1. **Define Foundations** — color palettes, typography, spacing, grid systems.
2. **Design Tokens & Variables** — single source of truth for visual properties.
3. **Core Components** — buttons, inputs, grids; "scalable and adaptable across platforms."
4. **Guidelines & Documentation** — strategy to ensure consumer teams understand and continue effectively using the system.
5. **Design Patterns** — ongoing assistance for consumer teams.

**Atomic Design framing made explicit (line 1958):** Subatomic (Design tokens) → Atomic → Molecule → Organism → Template (Pattern).

**Foundations breakdown:** Color (accessible palettes + tokens per brand theme); Typography (type scales, Figma styles per brand); Grids (desktop + mobile web); Spacing (scales + variables); Icons (robust library); Components (accessible, flexible, all interactive/disabled states).

**Design Tokens explained (line 1984):**

> "Design tokens represent small, repeatable design decisions. A token can be a color, font style, unit of white space, or even a motion animation designed for a specific need."

Why: visual consistency; enables themes (dark mode, brands); simplifies handoff; "as visual language evolves, changes can be made once across the system and products. No more finding and replacing hard-coded values everywhere."

**Themes (line 2003):** Light/dark mode, brand themes, "cozy/comfortable/compact views, reduced motion, custom typography styles."

**Detail slides (lines 2036–2134):**

- Define the foundations
- Design tokens
- Component creation — "Based on your products' needs we will identify elements that deliver the most value."
- Documentation and guidelines
- Release strategy — rollout strategy for updates
- Implementation plan — "gradual adoption or comprehensive migration"

### Macro-phase 3 — Adoption, Support & Comms (lines 2151–2233)

> "Performing & Optimizing — Monitor adoption, gather feedback, and continuously improve the design system while providing training and managing contributions for ongoing evolution."

**Five-column headline:**

1. **Adoption & Integration Strategy** — ensure consumer teams understand AND continue to effectively utilize.
2. **Support consumer teams** — ongoing assistance.
3. **Communication strategy** — releases, changes, feedback, roadshows, onboarding.
4. **Collect Feedback** — designers, developers, stakeholders.
5. **Contribution Process** — proposals from team members.

**Detail slides: Define adoption strategy; Define support strategy; Communication strategy.**

**Two user groups (line 2218):** "1. The designers and developers working with the system. 2. The end users of the products built with the system." Both must be optimized for; sometimes a tradeoff judgment call.

### Mapping to canonical 8-phase model

| Canonical 8-phase | VML coverage | Notes |
|---|---|---|
| Discovery & Strategy | **Heavily covered** in Phase 1: Assess & Audit, Audit Digital Products, Stakeholder definition, 20 discovery questions, Customer Interviews, Ecosystem Mapping | Strongest coverage in deck |
| Design Foundations | **Covered** in Phase 2: Define Foundations (color/type/spacing/grids/icons), Design Tokens, Themes | Aligned with Atomic "Subatomic" tier |
| Component Library | **Covered** in Phase 2: Component creation, Atomic→Templates ladder, Hierarchical Component Model | |
| Documentation | **Covered** in Phase 2 + Governance: Documentation governance, structure, standards, namespace | |
| Development Support | **Light coverage:** tech stack, repositories (npm/GitHub), Storybook workshop env, Style Dictionary, Code Standards & Accessibility | Tech depth lighter than design depth |
| Pilot & Implementation | **Light coverage:** "Implementation plan… gradual adoption or comprehensive migration" — but no pilot-product methodology specified | **Gap** |
| Governance & Adoption | **Heavily covered** in Phase 3 + Architecture sub-phase: 3 governance models, 4 best practices, contribution workflow, component testing, adoption strategy | |
| Ongoing Maintenance | **Covered** in Phase 3 ("Performing & Optimizing"): support strategy, comms, feedback, contribution, version control, deprecation | |

VML's 3-phase model collapses Discovery+Strategy+Architecture into one heavy front-end macro-phase, then groups Foundations/Components/Docs into "Creation," then groups everything post-launch into "Adoption."

### Timing claims

- No explicit project-duration heuristics in this deck (e.g., no "12 weeks for foundations" rule of thumb).
- Roadmap is described as "phased approach with milestones, deliverables and timelines… delivers value quickly to consuming products."
- Stat: "In 5 days one designer was able to set up a foundational UI kit that we had scoped as 6 weeks of work" (Pull-Ups PM, re: Prism — line 3569). **This is the only concrete duration claim in the deck.**
- T-Mobile Apeiron timeline: started Apr 2022, "55 sprints over two years" implied (page 159 Ford ref).

---

## Section 5 — When a Design System is Needed

Six "Signs" — each frames a problem and how a DS helps. Verbatim:

### Sign #1 — Inconsistent, Inaccessible UI & UX

> "Inconsistent & inaccessible user interfaces and experiences can lead to confusion and frustration for users, negatively impacting their perception of your products. These issues may stem from design fragmentation, miscommunication, a lack of knowledge or no standardization among designers and developers working on different parts of a product or across products."

**How a DS helps:** "single source of truth with everyone using the same reusable, accessible UI components, patterns, layouts, fonts, colors, and guidelines."

### Sign #2 — Design and technical UI debt

> "Design and technical UI debt are the consequences of shortcuts and poor decisions in the design and development process. Over time, these compromises can lead to inconsistencies, usability issues, and a fragmented user experience."

**How a DS helps:** "unified set of UX design principles, components, and a pattern library… reducing the likelihood of miscommunications and inconsistencies."

### Sign #3 — Difficulty in maintaining and scaling your product

> "Maintaining and scaling its user interface becomes increasingly complex as your product evolves. Design debt accumulates, and the lack of consistent design patterns can make updates and expansions challenging, time-consuming, and resource-intensive."

### Sign #4 — Communication gaps between designers and developers

> "Misaligned expectations, differing interpretations of design mockups, or unclear documentation can result in a confusing and inefficient process."

### Sign #5 — Slow time to market

> "Slow product development leads to missed deadlines, increased costs, and reduced competitiveness, as your product takes longer to reach the market."

### Sign #6 — Duplicated design & development work

> "Without a centralized design system, teams often duplicate work when creating or updating UI elements—for example, building multiple versions of an app bar."

### Anti-signals / cautions (scattered)

- "Don't start a new design system from scratch unless you're prepared for a significant multiyear investment to catch up with established systems." (Gartner reprint)
- Ben Callahan: if your org has unhealthy practices, "expecting a design system alone to fix those practices is misplaced optimism."
- "You're burning cash when your product design and design systems aren't in sync."

### Maturity heuristic

The Chaos / Silos / Integration model (Section 2) functions as the deck's maturity ladder for assessing readiness.

---

## Section 6 — Case Studies

### Case Study 1 — Wendy's Fresh Design System (lines 2417–2566)

- **Client:** Wendy's
- **Problem:** Slow speeds, too many clicks, unintuitive UX, expiring digital ecosystem; inconsistent and inaccessible digital experiences across products; fragmentation increasing time-to-market and cost.
- **Approach:** Discovered, dissected, and strategized the evolution of nearly every customer-facing digital product. Created Wendy's Fresh Design System to support iOS + Android rebuild into a single Flutter codebase.
- **Deliverables:** Accessible reusable standard; Flutter-based codebase; usage guidelines as best-practice reference; expansion to digital ordering website and CRM platform.
- **Outcomes / metrics:**
  - **30 app components**
  - **24 app components** (second figure shown — likely web vs. app)
  - **4,000 lines of app code removed**
  - **600% increase in time-to-market speeds**
  - **22 developers supported, 15 designers supported**
  - **Accessibility:** 40+ web accessibility issues logged; 80+ app iOS/Android accessibility issues logged; **25 critical accessibility issues remediated**
- **Public URL:** https://freshds.wendys.com
- **Tagline:** "Fueling transformation across every touchpoint."
- **Listed value props:** Consistency & Cohesion; Adaptability & Flexibility; Streamlined Updates; Improved Accessibility; Reduced Technical Debt; Quicker to Market.

### Case Study 2 — T-Mobile Apeiron Design System (lines 2568–2858)

- **Client:** T-Mobile (also covers Metro brand)
- **Problem / Ask:** "Redeploy the T-Mobile flagship app and website from the ground-up, built from a single consolidated design system that will reduce the cost of maintaining T-Mobile's digital experiences, accelerate the introduction of new features and enable scalable, cohesive experiences for our customer and front-line."
- **Approach:** VML led a blended team of agency and T-Mobile resources starting Q2 2022.
- **VML's role:** Lead client/agency DS team; provide cross-disciplinary resources; define DS team processes & roadmaps; define implementation & adoption strategies; lead adoption efforts; define support strategies.
- **Deliverables:** UI libraries for Web, iOS & Android; T-Mobile & Metro brand themes; design tokens (single source of truth); defined design patterns; robust documentation; "Getting Started" guides and integration support.
- **By the numbers (Apr 2022 start):**
  - 20+ UI elements researched
  - 500 design tokens
  - 2 brand themes
  - 18 UI elements designed
  - 24 elements researched
  - 39 team members since June
  - 3 platforms (iOS, Android, Web)
  - 15 elements in development
  - 20 pages of usage guidance & design patterns

### Case Study 3 — Ford Design System (FDS) (lines 2870–3132)

- **Client:** Ford (and Lincoln brand)
- **Time period:** 2018–2022
- **Problem:** "Customers faced inconsistent and challenging brand interactions" across digital products. Required global transformation.
- **Approach / Origin:** Mustang Mach-E vision work seeded the system. Built into the Ford Design System (FDS), unifying brand across all channels including in-vehicle.
- **Deliverables:** Universal pattern library; guidelines for global teams; in-vehicle support; brand themes (Ford + Lincoln) on a single code base.
- **Notable quote (line 3082):** "The ability to change between Ford & Lincoln brands 'saved developers 90% of the time it would typically take for Lincoln.'"
- **By the numbers (2018–2022):**
  - **900+ designers, developers, PM, BO, etc. invited to onboard**
  - 5 regions (NA, SA, EU, IMG, CN)
  - 50 agencies with FDS access
  - 45 components in web library
  - 250+ licensed DSM users
  - 90+ devs with code kit access
  - 100+ Ford URLs impacted to-date
  - 55 sprints over two years
  - 2 award nominations (2020 Ford API; WPP Extraordinary)

### Implicit case mentions

- Sherwin-Williams (line 3782): listed as a case-study target for Q3/Q4 priorities, but no full case study slide.
- Abbott pitch (line 3588): five Prism slides drawn from Abbott pitch; no full case study.

---

## Section 7 — Scoping & Team Building (CRITICAL)

### Scoping framework (line 3159)

> "Scoping Design Systems — Value delivered through cost savings & efficiencies that result from streamlining work & optimizing allocations."

**Visual + checklist of scoping inputs/outputs (verbatim):**

- Visual: investing in a design system & systemized way of working adds more value the earlier you do it / ROI timeline
- Deliverables (how detailed?)
- Team Models (show scalability & flexibility — include allocations?)
- Roles & Responsibilities (language that can be dropped into SOWs)
- Ways of working (how to show this as a competitive advantage)
- High-level timing
- Other things:
  - Roadmap example
  - Backlog example (with t-shirt sizing example)
  - Sprint Timeline example
  - Request intake flow example

**Important read:** This slide reads as an unfinished scoping playbook outline rather than a finished framework. The bullet-point text is internal-author shorthand/TODO. **Gap signal: the deck *prompts* but does not *deliver* a complete scoping methodology with t-shirt sizing, sprint timing examples, or pricing logic.**

### Team makeup (line 3197, "Team Makeup")

**Disciplines (verbatim list):**

- **Client:** product owner, business lead
- **XD:** includes UX, UI, Copy
- **Technology:** Front End Dev, QA
- **Delivery / PM:** includes Leadership, Direction
- **Specialties:** Strategy

**A team graphic shows roles arrayed:** Strategy / Copy / Lead / Lead / PM / Dev / Dev / UX / UI / UX / UI / PM / QA — a ~13-role configuration with **3 Leads** (XD lead, Tech lead, Delivery/PM lead).

### Resourcing — Must Have / Should Have (line 3263, verbatim)

> "The composition and size of the team will depend on many factors including available resources, time, scope, budget, among others. The reality is that often team members will need to wear multiple hats, and/or split time between building the system and another product."

- **MUST HAVE / DESIGN:** "Design members can span sub-disciplines — visual, interaction, information architecture to name a few — but the team must excel in crafting an elegant visual language."
- **MUST HAVE / ENGINEERING:** "Front-end focus with platform-specific knowledge, seasoned skills to establish conventions, and tool building."
- **MUST HAVE / PM & LEADERSHIP:** "Establish vision, drive direction, curate roadmaps, monitor adoption, and organize backlogs, scrums and critiques."
- **MUST HAVE / Quality Assurance:** "QA ensures a high level quality of production. Quality of the components is everything for the system's ability to both function and ensure adoption."
- **SHOULD HAVE / SPECIALTY:** "Speciality concerns like content strategy, accessibility, performance, SEO, and more. While valuable, keep in mind that systems first and foremost marry design and engineering."

Reference cited: https://medium.com/eightshapes-llc/designing-a-systems-team-d22f27a2d81d (Nathan Curtis / EightShapes — explicit external influence on VML's team-building methodology).

### Team example (line 3298)

**"Lead" roles described in detail:**

- **Client lead:** "Client should provide a business lead or product owner for governance and to support integration and adoption across the business ecosystem."
- **Tech lead:** "Tech leadership is crucial in defining the [tech stack/architecture]…"
- **Design lead:** "Design leadership should be involved in defining principles, guiding the work, prioritizing the backlog, as well as engaging with the client on the system and other leadership duties."

**Minimum maker pairs:**

- "At a minimum a pair of UX & UI designers should be pairing to produce the work. They should have a broad skillset including a deep understanding of platform practices and components, communicating UX & UI requirements, systems thinking, accessibility, etc."
- "At a minimum a pair of front end developers should be pairing to produce the library."
- "QA is imperative to ensure that components meet the requirements and standards necessary to be released."
- "If possible, a content strategist and/or copywriter are crucial in helping to write and manage the documentation, as well as other inputs such as content authoring for components, voice, tone, etc."
- "At least one project management teammate should be included to managing the backlog, help coordinate team tasks, meetings, & manage development & QA."

**This implies a minimum viable team of approximately 9–11 people:** 3 leads (Client, Design, Tech) + 2 designers (UX+UI) + 2 devs + 1 QA + 1 PM + 1 content strategist (should-have).

### Team Models (lines 3236–3517)

**1. Centralized Team (preferred model — explicitly stated):**

> "A centralized team supports the system with a dedicated group that makes and spreads decisions and parts for other teams to use. This is our preferred model for a systems team. Dedicated does not necessarily mean full capacity. It means there is a group of makers who have been identified to spend at least a portion of their time dedicated to the system."

**Centralized teams CAN:**
- Spread a design language, components and patterns to a broad portfolio
- Serve many product teams, free from the bias of any product's priorities
- Identify opportunities and solicit requests to deepen a library
- Setup practices and processes to validate emerging design

**Centralized teams OFTEN LACK:**
- Context, normalizing solutions only indirectly grounded in actual product or platform constraints
- Power to foster active participation of — let alone the contribution of — designers on product teams
- Visibility into day-to-day, product-specific challenges
- Influence on product designers to balance tradeoffs between product and system objectives

(Source cited: EightShapes — "team-models-for-scaling-a-design-system-2cf9d03be6a0")

**2. Federated Model:** Example shown as "agency/client blended team" (line 3488). Mix of agency staff and client staff.

**3. Blended Teams:** "Many times the agency is paired or integrated with resources from the client. For example, there may be a VML design working with a client partner or a third party developer."

**Team-size variants:**

- **Small Teams:** "lean, highly aligned… typically the teams creating the system are also the ones consuming it. A lot of information is shared directly, and therefore there is minimal documentation."
- **Medium-Size Teams:** "Defined by the fact that the system is now being consumed by others than those creating it… team may grow and start to have dedicated members and require more documentation."
- **Smaller teams or limited scope:** "Wearing a few different hats. Additionally, some roles may have more of an 'advisory' role and not actively participate in producing the system."

**Time-horizon caveat (line 3387):**

> "Because of our role as an agency partner, our participation in a system may be finite, changing over time or even ending as a product launches. As such, the makeup of a team may evolve to include more client resources as we prepare to handoff, or as a system matures and stabilizes. Be adaptable and strategize the best path to set our client partners up for long term success."

**Communication priority (line 3437):**

> "It is imperative that the systems team is always getting input and feedback from the product teams who can communicate day-to-day, product-specific challenges. This will help identify and prioritize new components, as well as call out design flaws or gaps in documentation."

### Stakeholder mapping (lines 5266–5281, from late-deck/appendix Governance content)

> "To effectively scale a multi-brand design system, teams must identify all key stakeholders—designers, developers, product managers, brand leads, and executive sponsors—and understand their unique needs. Categorizing them by influence and interest helps prioritize engagement."

- **High Influence / High Interest:** Brand leads, Design leads, Tech leads, Product leads, DS Team
- **Low Influence / High Interest:** Developers, Junior designers, PMs
- **High Influence / Low Interest:** Executive sponsors, Cross-org leaders

(Standard 2x2 stakeholder/influence-interest matrix.)

### Pricing / sizing / timeline guidance

- **Not directly specified in the deck.** No SOW templates, no $-rates, no week-counts per phase.
- **Implicit signals only:** roadmaps with milestones; t-shirt-sized backlog (referenced as "to do" placeholder); 55 sprints over 2 years for Ford; T-Mobile started Apr 2022 with 39 team members reached by some later month.
- **Practitioner conclusion:** scoping methodology is a known gap the practice has flagged for itself.

### Mapping scope to canonical 8-phase model

The "Team Models" + "Resourcing" content focuses primarily on the **Component Library + Documentation + Governance & Adoption** phases (production team). Discovery & Strategy work appears to imply leadership-only resourcing with light strategist support. Pilot & Implementation phase resourcing is essentially undefined in the team-makeup discussion.

---

## Section 8 — Prism (internal white-label DS)

### What it is (lines 3537–3573)

> "Prism2 is VML's enterprise design system framework. It goes beyond a white-label UI library, providing a theme-able design token taxonomy, accessible foundations, a flexible UI kit, developer-ready code libraries, and purpose-built plugins that speed up theming and export. Prism2 enables teams across VML to design, build, and deliver consistent experiences more efficiently — giving more time for meaningful, creative work."

> "An internal design system and set of tools that enable agency teams to create more efficiently, allowing more time for meaningful work."

### Two flavors

1. **Multi-file, scalable design system** — for full DS engagements
2. **Single-file, quick project starter** — for pitches/prototypes

### What's in it (line 3614)

- **Color** — accessible color palettes and accompanying variables for light mode (with brand-themable structure)
- **Typography** — type scales and Figma styles for web desktop, mobile, iOS, Android
- **Grids** — desktop and mobile web
- **Spacing** — spacing scales with corresponding variables
- **Icons** — open source icon library plus other icons and logos
- **Components** — accessible, flexible, all interactive and disabled states
- "Components & templates are designed to be neutral, flexible and scalable, making them an ideal starting point for any project."

### Theming workflow (line 3629)

> "Applying brand elements to PRISM, we can quickly theme color, typography and components to a brand's identify. PRISM components will automatically update to reflect the changes to reveal a UI kit unique to the brand identity."

Steps: **Scaling color** (define color scales based on brand colors) → **Defining usage** (assign to interactive states) → **Update type** (PRISM fluid typography scale with brand fonts) → **Assign radius** (border radius values).

### Why it exists (line 3761)

> "As design system practitioners we are looking to solve both the difficult and mundane problems of our teams so they can focus on the more meaningful and specific problems for their clients and products."

Outcomes: "Happier designers & developers; Better communication across disciplines and clients; An increased sense of community and collaboration."

### Value claims

- **Efficient:** "Teams hit the ground running with pre-built foundations, components & templates that can typically take weeks or months to define."
- **Accessible:** "Built from the ground up to be accessible and meet all WCAG 2.2 standards."
- **Reusable:** "Work can be created, replicated, and maintained quickly and at scale, unifying language across cross-functional teams."
- **The headline proof point (line 3569):** "In 5 days one designer was able to set up a foundational UI kit that we had scoped as 6 weeks of work." — Pull-Ups PM. **(Implies ~6× speed-up.)**

### Adjacent practice infrastructure

- **Design Systems Hub** (SharePoint): internal hub with terminology, FAQs, "Design System 101," tools, documents, news. MVP version live.
- **"Selling Design Systems Deck":** **130 slides** of pre-built pitch material — one-pagers, definitions, case studies, visualizations, ROI, strategy, process, opportunity recognition. (This is the deck this document is analyzing.)

### Vision (lines 5388–5400)

- **2025–2026 Focus on Building:** Figma Library; Developer library; Design tokens; Usage Guidelines; Principles; Multiple brand themes
- **2027 & Beyond Focus on People:** Adoption & integration assistance; easier dev implementation; product team support; clarity in guidelines; supporting larger global network; user feedback incorporation; refined contribution models

---

## "Selling Design Systems" content (cross-cutting, scattered)

This deck IS the Selling Design Systems library. Specific selling-focused content found:

- **Cover slide (line 1):** "DESIGN SYSTEM / Selling 2024 / Design Systems Grab N' Go Slides — INTERNAL ONLY"
- **One-pager (lines 10–48):** Target customer, ideal circumstances, landscape, RTBs, competencies — full "leave-behind" sales material
- **Client-facing keynote slides (lines 173–298):** templated keynote slides under the heading "OUR KEYNOTE TEMPLATE" — to drop into client-facing decks. Themes: "Digital design systems"; "Amplify your brand impact"; "Accelerate your product delivery"; "Create space to focus on innovation"; "A partner in excellence." Marked "MAY 2021" — older content reused.
- **Stat callouts** (Section 3) — 40–50% efficiency, 4 months → minutes, 30% accessibility issues solved — **these are the deck's core sales stats**
- **ROI Calculator** (line 1341) — concrete dollar-translatable efficiency gains for buttons (67.7%) and dynamic menus (81%) — sales artillery
- **Sign #1–6 framework** (Section 5) — opportunity-recognition framework for new biz teams
- **Case studies** (Section 6) — Wendy's, T-Mobile, Ford (Sherwin-Williams flagged as TBD)
- **Practice objectives slide (lines 4218–4373):** explicit four pillars include **"02 SELL DESIGN SYSTEMS"** as a named objective. Activities under it:
  - Support client teams on general best practices across disciplines
  - Provide content and support for pitches that include design systems
  - Create case studies to showcase our DS work
- **Q3/Q4 priorities (line 3778):** "Materials for new business / pitches; Case studies for T-Mobile, Ford & Sherwin-Williams; Net-new elements & components for PRISM; Community presentations; Knowledge base for Design Systems 101 content; Accessibility content/practice integration."
- **Synergy slides (lines 4544–4602):** Selling DS *with* Brand Practice, Accessibility Practice, Content Practice — bundled-pitch logic.
- **"Design Systems are Infrastructure" essay (lines 4608–4675):** A future-tense reframe positioning DS as "infrastructure" and "the antidote" to AI-commoditized UX. Strong selling argument for executives skeptical of DS budget. Key line:
  > "Design systems are no longer just projects, tools, frameworks, or even products— design systems are infrastructure."
  >
  > "AI-driven design risks commoditizing user experiences, making products indistinguishable. A robust design system is the antidote, acting as the organization's design 'DNA.' It provides proprietary training data to ensure AI-generated designs reflect the brand's unique identity and standards."

---

## Phase-tagged findings (8 phases)

### 1. Discovery & Strategy
- 20 strategic discovery questions (Section 4) — most thorough single artifact in the deck for this phase
- "Assess existing libraries / Audit digital products" sub-steps
- Customer Interviews (designers, developers, PMs)
- Ecosystem Mapping
- Stakeholder definition + influence/interest 2x2
- Maturity assessment via Chaos/Silos/Integration model
- Six "Signs" (Section 5) as readiness diagnostic

### 2. Design Foundations
- Color, Typography, Spacing, Grids, Icons, Components (line 1971)
- Atomic Design as the underlying mental model
- **Design tokens as "the backbone"** — single source of truth
- Themes (light/dark; brand themes; cozy/comfortable/compact; reduced motion)
- Style Dictionary as the recommended platform-specific output tool

### 3. Component Library
- Hierarchical Component Model: Foundations → Components → Patterns → Templates → Pages
- Tier model: Core Tier (system team) vs. Lower/Shared (sandbox)
- Component Qualification criteria (problem solved, differentiation, reusability, technical/a11y feasibility)
- Component Testing checklist (10 items)

### 4. Documentation
- Single source of truth framing
- Documentation Structure: typography, color, spacing, icons, components, interface patterns; matures to code snippets/usage/contribution
- Documentation Standards: tone, required info, examples, accessibility, brand variations
- Maintenance Responsibility: centralized vs. component-owner vs. federated brand-rep models

### 5. Development Support
- Tech stack definition (collaborate with partner's tech team)
- Repositories & Environments: npm/GitHub for consumption; Storybook (or equivalent) for prototyping
- Design Tokens via Style Dictionary
- Code Standards: modular, reusable, linted; accessibility built into components by default
- "Getting Started" guides + integration support (T-Mobile case study deliverable)

### 6. Pilot & Implementation
- **Lightest coverage in the deck.** Only mentioned as "Implementation plan… gradual adoption or comprehensive migration" (line 2125). No pilot-product methodology, no rollout sequencing.

### 7. Governance & Adoption
- 3 governance approaches (centralized, federated, distributed)
- Recommendation: Centralized model
- 4 governance best practices (clear roles, intake/contribution, version control, regular reviews)
- Component governance (qualification, intake, testing, contribution workflow)
- Documentation governance, Accessibility governance
- Adoption strategy, Support strategy, Communication strategy
- Roadshows, onboarding, feedback loops

### 8. Ongoing Maintenance
- Performing & Optimizing macro-phase (Section 4 Phase 3)
- Component Refinement, Code Kit Refactoring, Patterns & Broader Guidance, Guideline Improvements, Training Content, Ongoing Maintenance, Increased System Flexibility & Openness, Storybook Migration (line 5031)
- Multiple input channels, proactive communication, ongoing engagement (line 5340)
- Reframe: DS as infrastructure that requires "continuous maintenance and improvement rather than being treated as a one-time deliverable"

---

## Principles & philosophy (cross-cutting)

- **DS is a product, not a deliverable** — "A Design System is not a deliverable, but a set of deliverables. It will evolve constantly with the product, the tools and new technologies."
- **DS is infrastructure, not a project** — late-deck reframe (line 4634)
- **DS as force multiplier, not fix** — Ben Callahan: magnifies healthy practices, exposes unhealthy ones
- **"Building products better, not just better products"** (line 4410)
- **80/20 rule** — system handles 80% of design/dev needs so teams focus on the 20% unique to their problem
- **"More space for meaningful work"** — Prism's recurring tagline; appears throughout the deck
- **Two user groups must be optimized for** — DS users (designers/devs) AND product end-users
- **Centralized model preferred** — but with explicit awareness of its blind spots
- **Cross-disciplinary by design** — "systems first and foremost marry design and engineering"
- **Accessibility is foundational, not additive** — WCAG 2.2 target; "perfect pair" framing
- **AI-readiness as new strategic justification** — DS as proprietary brand DNA / training data

---

## Frameworks, models, named concepts (catalog)

| Name | Origin | Role in deck |
|---|---|---|
| Chaos / Silos / Integration | Likely external (line 604) | Maturity model / readiness diagnostic |
| 6 "Signs" you need a DS | VML internal | Sales/discovery framework |
| 3-Phase Process (Planning → Creation → Adoption) | VML internal | Core methodology |
| 20 Discovery Questions | VML internal | Strategy phase tool |
| Hierarchical Component Model (Foundations → Components → Patterns → Templates → Pages) | Industry-standard | Architecture vocabulary |
| Atomic Design (Subatomic/Atoms/Molecules/Organisms/Templates) | Brad Frost | Component taxonomy |
| Brand → DS → Product layered model | VML internal | Org positioning |
| 3 Governance approaches (Centralized / Federated / Distributed) | Industry-standard | Multi-brand decision framework |
| 4 Governance Best Practices (Roles / Intake / Version Control / Reviews) | VML internal synthesis | Governance playbook |
| Stakeholder Influence/Interest 2x2 | Standard PM framework | Engagement prioritization |
| Team Models (Centralized / Federated / Blended; Small/Medium/Limited-Scope) | EightShapes / Nathan Curtis | Team sizing |
| Design Tokens as "Backbone" + Style Dictionary | Industry-standard | Technical architecture |
| 4 Practice Objectives (Support / Sell / Educate / Internal Tools) | VML internal | Practice charter |
| ROI Calculator (per-component reuse math) | Cited external tool | Sales artillery |
| 80/20 framing | "You Need A Design System" / Forrester | Value framing |
| "DS as Infrastructure" reframe | VML internal essay | Future positioning |
| Prism2 (two flavors: scalable vs. project-starter) | VML internal product | Practice accelerator |
| 3-Step Brand Theming workflow (color → usage → type → radius) | Prism workflow | Internal tool methodology |
| 4-Stage Lifecycle (Building / Scaling / Performing / Optimizing) | Forrester source (line 4988) | Project lifecycle |

---

## Notable verbatim quotes

- "A design system is a collection of UI elements built as reusable code. They are guided by clear standards that help organizations deliver cohesive, on-brand experiences at scale, over time. It is not: A style guide, a UI kit, or a brand system. (But can include these)."
- "A design system is like a digital recipe book for your brand."
- "The brand defines the design language and the design system translates that into digital styles and libraries of user interface elements that can be utilized by all product teams."
- "A Design System is not a deliverable, but a set of deliverables."
- "You're burning cash when your product design and design systems aren't in sync. Period."
- "Design systems distill and magnify healthy practices and patterns while exposing and challenging unhealthy ones." — Ben Callahan, Sparkbox
- "You can't innovate on products without first innovating the way you build them." — Alex Schleifer, Airbnb
- "The system addresses 80% of design and development needs so they can focus on the other 20%."
- "The efficiency savings for designers and front end developers using the design system: 40%-50%." — Robin Cannon
- "The four months of work to update our brand across all apps can now be accomplished in minutes." — Gerrit Kaiser
- "In just three months, our design system solved 30% of our accessibility issues across 50+ products." — Jehad Affoneh
- "In 5 days one designer was able to set up a foundational UI kit that we had scoped as 6 weeks of work." — Pull-Ups PM (re: Prism)
- "[Brand theming] saved developers 90% of the time it would typically take for Lincoln." — Ford case study
- "It's not just about building better products – it's about building products better."
- "Design systems are no longer just projects, tools, frameworks, or even products— design systems are infrastructure."
- "AI-driven design risks commoditizing user experiences… A robust design system is the antidote, acting as the organization's design 'DNA.'"
- "Dedicated does not necessarily mean full capacity. It means there is a group of makers who have been identified to spend at least a portion of their time dedicated to the system."
- "It is imperative that the systems team is always getting input and feedback from the product teams who can communicate day-to-day, product-specific challenges."

---

## Tensions / contradictions / open questions

1. **Centralized as preferred vs. acknowledged blind spots:** Deck explicitly recommends centralized model and lists its weaknesses (lack of context, low product designer participation, no day-to-day visibility, no influence on product tradeoffs). The federated model is shown but not recommended. **Tension unresolved.**

2. **Scoping methodology is incomplete:** The Section 7 scoping slide (line 3168) reads as an outline of TODOs ("Other things? — Roadmap example, Backlog example w/ t-shirt sizing, Sprint Timeline, Request intake flow"). The promised concrete examples are not delivered in this deck. **Practice has flagged this as a known gap.**

3. **Two definitions of Prism's relationship to a "UI Kit":** Section 2 says a DS is *not* a UI kit. The Prism appendix calls Prism "An internal UI Kit and set of tools" (line 3733) but elsewhere "An internal design system" (line 3553). **Inconsistent positioning.**

4. **Four phases vs. three phases:** Late-deck (line 4988) cites Forrester's 4-stage lifecycle (Building / Scaling / Performing / Optimizing). VML's own process (Section 4) is 3 phases (Planning / Creation / Performing-Optimizing). The two models are not reconciled in the deck.

5. **Older content reused without dating:** Multiple "MAY 2021" client-keynote slides and "DECEMBER 2022" branded slides ("VMLY&R") sit alongside 2024 content — visible co-existence of legacy and current material. This is an editorial gap rather than a content gap, but it could undermine credibility in client decks.

6. **Pricing/duration heuristics absent.** The only quantitative timing claim is the 5-days-vs-6-weeks Prism stat. No base SOW templates, no week-counts per phase, no $-rates, no fixed-vs-T&M guidance. **Major gap for senior practitioners.**

7. **Pilot/Implementation phase is a hole.** Robust on Discovery and on Foundations/Components/Docs; thin on the production handoff/rollout sequencing that real engagements require.

8. **Architecture content (line 1700–1776) appears more recent / 2025-tier.** It is clearly authored separately from the 2022/2024 base content (different visual treatment, different vocabulary including "Single Source of Truth," "Style Dictionary," Tier model). It hasn't yet been integrated with the rest of the methodology.

9. **Multi-brand coverage:** The governance section spends significant time on multi-brand systems, but the main 3-phase methodology never explicitly addresses multi-brand scoping/sequencing. Brand themes are introduced as a Foundations concept but not as an architectural decision driver.

10. **"Selling DS" sits as a Q3/Q4 priority + a practice objective, but the deck IS the selling material.** The artifact is self-referential — it does not separate "deck *about* selling DS" from "deck *for* selling DS." This makes the practice's selling motion partially opaque.

---

## Gaps

- **No SOW language or RACI templates** despite "Roles & Responsibilities (language that can be dropped into SOWs)" being flagged as a desired scoping output
- **No t-shirt sizing examples** despite being flagged
- **No sprint timeline examples** despite being flagged
- **No request intake flow examples** despite being flagged
- **No concrete project pricing or duration heuristics**
- **No pilot-team-and-product methodology** (which DS launches first? How do you choose pilot products? Migration sequencing?)
- **Limited measurement / KPI detail** — qualitative success stories abound but no template KPI tree (e.g., adoption rate, time-to-component, contribution velocity, defect-rate)
- **No discussion of design tooling versioning / Figma library publishing strategy at depth** — referenced but not detailed
- **No dedicated Code Connect or Figma-Variables-as-tokens workflow** — surprising omission for 2024–2026 content given Variables shipped in 2023
- **Ford case study lacks a "lessons learned" section** — pure achievements; Wendy's similarly metrics-forward
- **No explicit handling of design+content+research integration** beyond the Synergy slide
- **No mention of token taxonomies** (e.g., reference/system/component layered tokens) despite tokens being "the backbone"
- **No headcount-to-deliverable ratio guidance** (e.g., "for ~30 components expect X designer-weeks")
- **Limited discussion of decommissioning / what happens when an engagement ends** beyond a single line about "set client partners up for long-term success"

---

*Notes file end. Source: vml-library.txt (5,429 lines). Prepared as a synthesis for senior practice leadership reference.*

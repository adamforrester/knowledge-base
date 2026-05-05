# 10 — Design Systems in CMS Environments

> A design system and a CMS are two different governance models for the same frontend. The design system governs components. The CMS governs content. The seam between them is where most of the hard problems live — and where most agencies underestimate the work.

---

## What this file is and why it exists

The core phase framework in this knowledge base (phases 01–08) describes design systems work largely independent of the consuming technology stack. In practice, a large portion of VML's engagements involve delivering into a CMS — most commonly Adobe Experience Manager (AEM), and with some frequency Drupal. These platforms impose constraints, architectural patterns, and governance structures that change how design system work is scoped, built, and handed off.

This file does not duplicate what the phase files cover. It surfaces the CMS-specific layer: what changes about token delivery, component architecture, governance, and handoff when the consuming environment is AEM or Drupal. It assumes the reader knows what these platforms are at a working level.

**AEM is the primary focus.** It is the platform most frequently encountered in VML's enterprise client base. Drupal is covered as a secondary platform with comparative framing.

---

## The central problem

A design system component is a self-contained, portable unit: markup + styles + behavior, delivered as a Figma file, a React component, or a Web Component. An AEM component is something different: an HTL template, a Sling Model, an authoring dialog, and a clientlib reference — four surfaces bound together by a JCR content tree. Bridging these two models is the primary architectural challenge in every AEM design system engagement.

The same gap exists in Drupal, though the shape of it is different. Twig templates, theme libraries, and (in Drupal 10+) Single Directory Components have their own governance logic that does not map 1:1 to design system governance.

The key decision in every CMS engagement is: **at what layer does the design system live, and where does the CMS begin?** The answer determines the architecture, the delivery model, and the long-term maintenance burden.

**On team structure:** Unlike some agency models where a separate DS team hands off to a separate AEM development team, VML frequently operates as the full-stack team — designing and building both the design system and the AEM components within the same engagement. When that's the case, the "seam" between DS and CMS is an internal coordination question, not an external handoff. The architectural decisions below still apply; what changes is that VML has more control over how the DS is structured and consumed, and fewer coordination gaps to manage. The handoff question shifts to: what does the client team inherit, and can they maintain it? On engagements where VML is design-only and a client or third-party team handles AEM development, the handoff spec and delivery model become critical — which is covered in the agency handoff section below.

---

## AEM — Architecture Fundamentals

### What a DS practitioner needs to understand about how AEM works

AEM is a Java-backed, server-rendered platform running on Apache Sling and OSGi. Every component in AEM is addressed by a `sling:resourceType` path in a content tree. A "component" is the union of: an HTL template (markup), a Sling Model (typed Java object that feeds the template with JCR-mapped data), an authoring dialog (XML structure that defines what authors can configure), and a clientlib reference (the CSS/JS package that styles and animates the component). These four surfaces must stay in sync. When they drift, things break.

For DS work the critical implication: **there is a hard line between data shape (Sling Model) and presentation shape (HTL + clientlib CSS).** This is actually good for governance — you can update component markup from `v1` to `v2` without breaking authored content because content binds to `sling:resourceType` paths, not markup. But it means DS components are never fully portable out of the box. A React component or Web Component cannot trivially read JCR content — it must receive data marshalled through HTL attributes or exposed through the Sling Model Exporter (.model.json) and consumed client-side.

### Client Libraries (clientlibs) — how CSS and tokens get delivered

Clientlibs are AEM's asset-bundling mechanism. A clientlib node under `/apps/<site>/clientlibs/<name>` groups CSS and JS files with categories and dependencies, then serves them to pages via HTL. Modern AEM projects use a `ui.frontend` module (Webpack or Vite) to compile assets; a tool called `aem-clientlib-generator` converts the build output into clientlib structure; Maven packages it into a content package; Cloud Manager deploys it.

For design tokens: CSS custom properties live in a base clientlib category (e.g. `myproject.tokens`) loaded on every page. Component clientlibs declare a dependency on it. This is the delivery mechanism for a Style Dictionary pipeline — the token build emits a `tokens.css` file that gets pulled into the clientlib structure through the Maven build.

**The Style System** is the AEM-native mechanism for author-selectable variants. Template authors define CSS class options in content policies; authors select a variant in the page editor; the chosen class is injected on the component's wrapper element. The DS team controls the CSS — what each class does. The authoring vocabulary is controlled in the policy. This split — code-owned CSS, content-owned policy — is the closest AEM gets to a clean token-to-author handoff and is the right governance model for visual variants.

### Authoring model and its DS implications

**Editable templates** define page structure and allowed components. They have three layers: structure (locked — header/footer, root container), initial content (what authors see on a fresh page), and policies (per-component configuration and allowed variants). Policies are the governance lever. They enumerate which components are allowed in a container, expose Style System options, and restrict what authors can change.

**Experience Fragments** are reusable composed-content blocks (header, footer, hero treatments) that include layout and components. They belong at the design system level — they are how you encode "the header component" across multiple pages or sites.

**Content Fragments** are structured, presentation-agnostic content records exposed via GraphQL. They carry no presentation logic. In headless or hybrid deployments, Content Fragment Models define the content schema and should align with DS component structure: a `HeroFragment` model should map cleanly to a `<Hero>` DS component. If the DS team doesn't own these model schemas, they drift toward presentational concerns and the clean separation breaks down.

### The SPA Editor deprecation — a critical current change

Adobe deprecated the SPA Editor in January 2025. This matters for DS strategy. The SPA Editor embedded React/Angular components inside AEM by having AEM serve a JSON page model and the SPA render components mapped to AEM resource types. It worked for its era, but it forced the DS to live inside a React tree compiled into the AEM build, coupled the DS to the SPA Editor SDK's React version, and required every component to exist twice (AEM resource + React component).

**Adobe's current direction is the Universal Editor**, which decouples editing from AEM-specific SDKs entirely. Any web framework, any hosting model, instrumented through `data-aue-*` attributes on rendered HTML. For DS work this is significant: a Universal Editor project lets the DS live wherever it makes sense — its own repo, Storybook, npm package — and the AEM coupling collapses to a thin instrumentation layer.

**Implication for VML:** Any SPA Editor project in our portfolio is legacy and accruing migration debt. New AEM DS investment should target Universal Editor or HTL-native paths. Do not scope new work to the SPA Editor model.

---

## AEM — Integration Architecture Options

Three approaches, each with legitimate use cases and honest trade-offs.

### Option 1: Web Components

**How it works.** Design system is authored as Custom Elements (typically Lit-based), published as an npm package, and delivered into AEM via a clientlib that bundles the compiled Web Component modules. HTL templates emit the custom element tags; Sling Models populate the attributes from JCR content. Adobe's Spectrum Web Components is the reference implementation — framework-agnostic Lit components consumable from HTL without any React runtime on the page.

**Best fit for:**
- HTL-native AEM projects where a modern component model is wanted without a JS framework dependency
- DS shared across multiple channels (AEM sites, microsites, email, embedded widgets)
- Universal Editor era projects — the editor doesn't care what renders the markup, only that instrumentation attributes are present

**Trade-offs:**
- Authoring dialogs are still AEM Granite UI dialogs — the DS aesthetic stops at the page editor boundary
- Slot composition across an HTL boundary is awkward — passing rich children into a Web Component requires shadow DOM patterns that don't compose naturally with HTL's `data-sly-resource` model
- SSR for Web Components in AEM is non-trivial; initial HTML must be rendered from HTL into the light DOM and enhanced client-side
- Shadow DOM can interfere with the Universal Editor's click-target instrumentation — requires care in the component's DOM structure

### Option 2: React/HTL Hybrid via SPA Editor

**How it works.** AEM serves a JSON model of the page tree; a React app reads it through `ModelManager` and renders React components mapped to AEM resource types via `MapTo()`. DS components are normal React components consumed by the mapped wrappers.

**Best fit for:** Existing SPA Editor projects with significant sunk cost. That's it. Adobe's deprecation notice makes this the wrong choice for any new work.

**Trade-offs:**
- Every component exists twice: AEM resource and React component. The contract between them is the JSON model — fragile and verbose to maintain.
- DS is coupled to the SPA Editor SDK's React version, which lags.
- With deprecation, migration debt is accruing. Every quarter this architecture ages, the exit cost grows.

**VML stance:** Do not propose or scope new SPA Editor work. On existing SPA Editor engagements, scope the DS to minimize its surface area in the React/AEM coupling and plan for Universal Editor migration.

### Option 3: HTL-Native

**How it works.** Components are HTL templates backed by Sling Models. The DS lives as Sass/PostCSS modules, design tokens as CSS custom properties, behavior as vanilla JS or lightweight enhancement libraries (Stimulus, Alpine). All bundled through `ui.frontend` into clientlibs. AEM Core Components are the reference implementation.

**Best fit for:**
- Content-heavy marketing sites where server-side rendering, accessibility, and edge cacheability matter more than client-side interactivity
- Full alignment with the Style System for author-selectable variants
- Proxy Component pattern for project-specific overrides of Adobe-provided components

**Trade-offs:**
- Components with reactive state (faceted search, configurators, complex filters) become clunky in vanilla JS
- DS is not portable to non-AEM channels without re-implementation — there is no shared component artefact unless you also maintain a parallel Web Component or React export
- Recruiting frontend talent to maintain HTL is harder than React; the reading audience for HTL is shrinking

**Practical note:** For most VML AEM engagements, especially content sites for marketing or brand clients, HTL-native remains the safest architecture. It aligns with what AEM is designed to do and has the lowest total coupling.

---

## AEM — Token Delivery in Practice

**The standard pipeline:**

```
Design tokens (W3C DTCG JSON)
  → Style Dictionary build script (in ui.frontend)
  → tokens.css (generated CSS custom properties)
  → Webpack bundles it into ui.frontend dist
  → aem-clientlib-generator converts dist to clientlib structure in ui.apps
  → Maven packages into content package
  → Cloud Manager deploys
```

The token clientlib (`myproject.tokens`) sits at the bottom of the clientlib dependency graph, loaded on every page. Component clientlibs declare it as a dependency. This is straightforward and works reliably.

**Multi-brand / multi-site token scoping** — two production patterns:

*Theme clientlib per brand:* Common tokens (spacing, typography scale) live in a shared base clientlib. Brand-specific overrides live in separate clientlibs (`myproject.tokens.brandA`, `myproject.tokens.brandB`) that redefine the same custom property names with brand values. The page template selects the correct brand clientlib based on a content tree property or policy. Cleanest model when brands share component markup but diverge on visual values.

*Attribute selector theming:* A single bundle with `[data-theme="brandA"]` blocks at `:root` or `<body>` level. Simpler infrastructure, larger bundle; works well when brands switch dynamically.

**AEMaaCS-specific consideration:** In AEM as a Cloud Service, you cannot patch CSS in production by editing files on a publisher — everything deploys through Cloud Manager pipelines. Token-only changes that trigger a full pipeline are a real cost. Separating tokens into a smaller, independently deployable content package (rather than bundling them with component code) is worth the architecture investment for any multi-brand client.

---

## AEM — Governance Implications

### The two-version-stream problem

AEM Core Components version by path (`core/wcm/components/image/v1/image`, `.../v2/image`). The Proxy Component Pattern — where every project creates its own proxy that sets `sling:resourceSuperType` to the relevant Core Component version — means your DS effectively has two version streams: the upstream Core Component version and your proxy layer. Migration from `v1` to `v2` requires a planned cutover window. Existing content keeps rendering on the old path indefinitely, which is by design — but it means your DS and AEM's component versioning are not the same thing.

### Who controls what

Policy-driven component allowlists — not code — determine what authors can place on a page. The DS team should own the policy catalogue. In practice this fights with delivery squads who want to add a component variant quickly for a campaign. The common failure mode: a squad creates a project-specific component under `apps/<project>/components/special-card`, it never gets folded into the DS, and years later the DS team finds a proliferation of card variants with diverging behavior and accessibility compliance. This is an organizational problem more than a technical one, but it requires organizational enforcement — a contribution review process for all new `apps/<project>/components/*` additions.

### Agency-to-client handoff models

VML operates across all of these patterns depending on the engagement:

**VML as full-stack team (common in AEM engagements).** VML designs and builds both the DS and the AEM components. The client inherits the complete codebase. The critical handoff question: can the client team maintain what VML built? This requires intentional decisions about whether the DS is embedded or an NPM package (see DS Delivery Model section above), documented DS conventions, and knowledge transfer sufficient for the client to make changes without VML.

**Build-and-throw (embedded, single-repo).** VML builds the DS inside the AEM project monorepo and hands the whole repo over. Most common for single-site engagements. Long-term risk: the DS has no independent versioning or release cadence after handoff, and the client team may not maintain it with DS discipline. Acceptable when the engagement is scoped honestly as a product build, not a long-lived DS.

**DS as a separate Maven artifact.** DS ships as a versioned content package with its own release cadence. Client consumes it as a Maven dependency and upgrades on their own schedule. Right model for multi-site, multi-team enterprise clients — requires AEM Maven discipline on the client side.

**DS as design-only, client-built AEM components.** VML owns Figma + tokens + specs; client or a separate technology vendor owns the AEM component implementation. Most common in Figma-only patterns like CareCentrix. Requires very clean handoff documentation — the developer will make interpretation decisions; the quality of those decisions depends entirely on the quality of the specs VML leaves behind.

---

## Drupal

Drupal's design system integration story has improved substantially with Drupal 10/11. The architecture is lighter-weight than AEM and in some ways more DS-friendly — but the organizational maturity at Drupal clients varies widely.

### How Drupal's asset system compares to AEM clientlibs

Drupal assets attach through `THEME.libraries.yml`, declaring CSS/JS bundles with versioning and dependencies. Unlike AEM clientlibs (page-level by default), Drupal attaches libraries only when the components that need them are rendered — per-render-tree. This gives more granular per-page bundling and is a real performance advantage for component-heavy pages. The mental model for token delivery is the same: a base library defines CSS custom properties; component libraries depend on it.

### Single Directory Components (SDC) — the most important Drupal development for DS work

SDC landed stable in Drupal 10.3 and is core in Drupal 11. It is the closest any major CMS has come to a genuine component model aligned with design systems. An SDC is a directory containing a `*.component.yml` schema (typed props and slots), a `*.twig` template, optional CSS and JS, and optional Storybook stories. The render system validates props against the schema at render time — closer to a React PropTypes contract than to AEM's loose dialog-to-Sling-Model data flow.

SDC integrates cleanly with Storybook. Multiple agency tutorials now describe a Vite + Tailwind + Storybook + SDC stack as the modern Drupal DS development environment — a design surface that AEM lacks natively. This is significant: for new Drupal engagements, the DS development and documentation workflow can be much closer to the framework-agnostic ideal than anything AEM offers today.

SDC is also the substrate for Drupal's upcoming Experience Builder — Drupal's answer to the Universal Editor. Betting on SDC for new Drupal DS work is safe.

### Web Components in Drupal

Simpler than AEM. Drupal's Twig output is HTML; Custom Elements drop in as tags. Library declarations bundle the Web Component modules. There is no SPA Editor equivalent to navigate, no shadow DOM instrumentation complexity for the editor. If the DS is being delivered as Web Components, Drupal is the easier target of the two platforms.

### AEM vs Drupal comparison

| Dimension | AEM | Drupal |
|---|---|---|
| Component model | HTL + Sling Model + dialog + clientlib (4 surfaces) | SDC: yml + twig + css + js (1 directory) |
| Schema typing | Loose (dialog XML, ValueMap) | Strict (component.yml validated) |
| Asset attachment | Page-level clientlib categories | Render-tree-aware libraries |
| Multi-brand theming | Multiple clientlibs + policies | Theme inheritance + libraries |
| DS dev environment | Storybook is bolt-on | Storybook is first-class with SDC |
| Versioning model | Path-based (`/v1/`, `/v2/`) | Module/theme semver |
| Editor direction | Universal Editor (decoupling) | Experience Builder (built on SDC) |
| Web Components integration | Manageable with care | Straightforward |

The practical summary: for greenfield projects where the design system is the centre of gravity and the CMS is a delivery surface, Drupal with SDC is a shorter path. For Adobe-stack enterprises where AEM is non-negotiable, the Universal Editor + HTL-native + token-clientlib approach is the most defensible architecture today.

---

## DS Delivery Model: NPM Package vs. Embedded

This is one of the most consequential architectural decisions in a CMS engagement and one that rarely gets discussed explicitly in scoping conversations. Getting it wrong adds friction for the life of the project.

### The core question

Should the design system be a **separately versioned package** consumed by the CMS project, or **embedded directly inside the project repo** as a module or folder?

### When to embed (the Wendy's model)

Embed the DS inside the project when all of the following are true:

- **Single site or single codebase.** The DS is not consumed by any other website, product, or team.
- **Single team.** The same team building the DS is building the product. There is no meaningful boundary between "DS work" and "product work."
- **No independent release cadence.** DS changes ship with the product; there is no need to version and release the DS separately.

In this model, the DS lives as a dedicated module or folder within the project repo — a clear internal structure (`/design-system`, `/tokens`, `/components`) that maintains architectural discipline without the overhead of package management. Setting up an NPM package for a single-site, single-team project adds real overhead (versioning, publishing pipeline, package registry access, consumer update cycles) for no practical benefit.

### When to use an NPM package

Move to an NPM package when any of the following are true:

- **Multiple codebases consume the DS.** More than one project repo needs the same tokens, components, or foundations. This is the primary forcing function.
- **Multiple teams.** Separate teams — different VML squads, client internal teams, third-party vendors — need to consume the DS independently without access to the source repo.
- **Independent release cadence.** The DS needs to version and ship independently of any single product, because consumers need to upgrade on their own schedule or DS changes should not be coupled to product releases.
- **Regional or multi-site scale.** Multiple regional codebases consuming the same DS foundation — a scaled engagement like New Balance across regions is the clearest example.

AEM engagements are where this question comes up most frequently because AEM is the platform of choice for large enterprise clients who, by definition, tend to have multiple products, multiple regional sites, and multiple teams. The larger and more distributed the AEM deployment, the more likely an NPM package is the right answer. VML has used the NPM package model on larger, scaled AEM engagements previously and it remains the right default for enterprise multi-site work.

### The delivery mechanics in AEM

**Embedded:** The DS lives in a dedicated folder within `ui.frontend`. Token build scripts, component CSS, and any JS run through the same Webpack/Vite pipeline as the rest of the frontend. Straightforward, no external dependencies.

**NPM package:** The DS is installed as a dependency in `ui.frontend/package.json`. The consuming project imports tokens, CSS, or JS components from the package. `ui.frontend` still handles the build and `aem-clientlib-generator` still produces clientlib structure — the DS is just coming from `node_modules` rather than a local folder. Requires the package to be published to a registry (npm public, npm private org, Artifactory, or similar) accessible to the build environment, including Cloud Manager.

**Cloud Manager note:** In AEMaaCS, the `ui.frontend` build runs inside Cloud Manager's build container. Private NPM registries require Cloud Manager environment variable configuration for authentication. Not complex, but requires coordination with whoever manages Cloud Manager. Budget 4–8 hours for initial setup and testing.

### Decision guide

| Situation | Recommendation |
|---|---|
| Single site, single team, one codebase | Embed in project repo |
| Multiple sites or regions, same brand | NPM package |
| Multiple teams consuming the DS | NPM package |
| Client's internal team maintains separately from product | NPM package |
| Greenfield AEM, enterprise client with multiple products | Default to NPM, confirm in discovery |
| Figma-only delivery, no coded components | N/A — DS lives in Figma |

### The broader principle

This decision is not AEM-specific, but it surfaces most often in AEM contexts because of the enterprise scale. The same logic applies to any coded DS delivery: embed when it's one team, one codebase; package when it's multiple consumers. Non-AEM VML engagements have historically been less likely to use NPM packages, but as Prism2 matures toward formal adoption, the package model should become the standard approach for any multi-consumer scenario regardless of platform.

---

## Scoping Considerations for VML

CMS-backed DS engagements have scope items that don't appear in the standard phase framework. These should be surfaced explicitly in any scoping conversation.

**Technical environment assessment is non-negotiable.** AEM version (6.5 LTS on-prem vs. AEMaaCS), whether the SPA Editor is in use, the state of the existing `ui.frontend` pipeline, how clientlibs are currently structured — these answers change the architecture and the estimate. On-prem vs. cloud alone changes the deployment path significantly. Do not commit to architecture or hours before this is understood.

**The DS team typically does not own AEM component implementation.** In most VML engagements, we own design and Figma; a separate technology team (internal VML, client internal, or third-party) owns the AEM components. The handoff model — how our tokens and component specs translate into AEM clientlibs and HTL templates — must be explicitly scoped. Someone has to do this translation work; if it's not in our scope it must be in someone else's.

**Token pipeline integration adds real hours.** Getting a Style Dictionary pipeline wired into a `ui.frontend` Maven build is not complex, but it requires AEM development access, familiarity with the archetype structure, and coordination with the team running Cloud Manager. In Figma-only engagements this is out of scope by definition. In design + code engagements, budget 20–40 hours for initial pipeline setup and integration testing.

**Multi-brand / multi-site AEM adds significant token and QA scope.** Each additional brand clientlib requires a token audit to ensure the right custom properties are being overridden. Each additional site requires policy configuration. Budget accordingly.

**Drupal SDC engagements can move faster.** If a client is on Drupal 10/11 and the technology team is willing to use SDC, the design system development surface (Storybook + SDC) can accelerate both DS build and developer handoff compared to AEM. Factor this into estimates relative to AEM equivalents.

---

## Failure Modes

- **Skipping the technical environment assessment.** Assuming AEMaaCS when the client is on 6.5 LTS. Assuming HTL-native when the SPA Editor is in active use. These assumptions break architecture decisions and estimates.
- **Token delivery as an afterthought.** Design system tokens defined in Figma, never wired into the AEM clientlib pipeline. Developers hardcode hex values. Token layer exists in design, not in production.
- **DS versioning and AEM versioning conflated.** DS team treats their component updates like npm semver. AEM team treats their component proxies like AEM Core Component versions. Neither team owns the mapping between the two. Components drift.
- **Project-specific components never folded back into DS.** Delivery squads create one-off AEM components for campaign needs. DS team doesn't review. Three years later, eleven card variants with diverging accessibility.
- **Build-and-throw handoff with no DS versioning.** Agency delivers the DS inside the AEM monorepo, the client never updates it, the DS diverges from any future work VML does for that client.
- **SPA Editor proposed for new work.** Architecture decision made before the deprecation notice was understood. New project accrues migration debt from day one.
- **Drupal SDC ignored on Drupal 10+ engagements.** Technology team defaults to older theming patterns; DS loses the Storybook-integration advantage and prop validation.
- **Content Fragment Models owned by content team, not DS.** Models accumulate presentational fields. The clean separation between content schema and DS component breaks down.
- **Token sub-repo not established for multi-project AEM clients.** Token source of truth fragments across project repos. Multi-brand clients end up with diverging token values across their AEM properties.

---

## Tensions and Open Questions

1. **Web Components vs. HTL-native for new AEM work.** Web Components are more portable and better positioned for the Universal Editor era. HTL-native is lower risk, more widely understood, and better supported by AEM's existing tooling. For a mixed team (VML design + client AEM developers), HTL-native is almost always the safer choice unless there is a concrete multi-channel reuse need.

2. **Where does the DS end and the CMS component begin?** The most common scoping ambiguity in AEM engagements. VML's default position: DS owns tokens, Figma specs, component behavior definitions, and Storybook (if in scope). AEM owns HTL templates, Sling Models, dialogs, clientlib wiring. The seam is the handoff spec. This should be stated explicitly in every SOW that involves AEM.

3. **AEMaaCS front-end pipeline ownership.** The `ui.frontend` Maven build is technically owned by whoever has Cloud Manager access and Java build knowledge. In many engagements this is not the design team. Token changes that require a full pipeline run require coordination with the AEM development team — which slows iteration. Worth discussing in discovery: who owns the pipeline, and what is the turnaround time for a token change to reach production?

4. **Universal Editor adoption pace.** Adobe deprecated SPA Editor but the Universal Editor is still maturing. Enterprise clients with large AEM Sites investments move slowly. The right architecture for a 2026 engagement may not be the same as the right architecture for a client who won't migrate for 18 months. Scope to where the client will actually be, not where Adobe's product roadmap points.

5. **Drupal SDC as the default for new Drupal engagements.** SDC is the clear direction. The tension is that many existing Drupal clients are on older theming patterns and their technology teams are not yet familiar with SDC. Recommending SDC to a client team that hasn't used it adds ramp-up time. Factor this into estimates.

6. **Storybook as the shared DS development environment.** Drupal + SDC enables real Storybook integration. AEM does not natively. On mixed-platform clients (AEM + non-AEM), Storybook becomes the DS source of truth and AEM is a consumer — which is the right model but requires a client willing to treat AEM as a downstream, not the primary.

---

## Key External References

- **Adobe Core Components** — reference implementation for HTL-native component architecture. Treat as the architectural floor.
- **Spectrum Web Components** (Adobe/GitHub) — production blueprint for DS-as-Web-Components delivered into AEM.
- **AEM Project Archetype** (Adobe/GitHub) — canonical `ui.frontend` + clientlib pipeline structure.
- **Universal Editor documentation** (Experience League) — current Adobe authoring direction. Required reading before proposing any new AEM DS architecture.
- **SPA Editor deprecation notice** (Experience League, Jan 2025) — formal deprecation of the React/Angular authoring model.
- **Drupal SDC documentation** (drupal.org) — schema, rendering, and Storybook integration.
- **Bounteous multi-tenant theming** — multi-brand clientlib pattern in production.
- **Perficient Style System guidance** — clearest public articulation of the Style System as DS governance lever.

---

*Provenance: AEM architecture fundamentals, clientlib token delivery pipeline, three integration approaches (Web Components / React-HTL / HTL-native) with trade-offs, SPA Editor deprecation and Universal Editor direction, AEMaaCS vs on-prem implications, headless AEM and Content Fragment model alignment, governance patterns and agency handoff models, and Edge Delivery Services framing are synthesized from Claude Code research (April 2026) drawing on Adobe Experience League documentation, AEM Core Components GitHub, Spectrum Web Components documentation, Bounteous engineering blog, Perficient engineering blog, and AEM.Design conventions. Drupal fundamentals, SDC architecture, libraries.yml vs clientlibs comparison, and Storybook integration patterns are synthesized from the same research drawing on drupal.org SDC documentation, Drupalize.me, and independent agency SDC + Storybook tutorials. The AEM vs Drupal comparison table and VML-specific scoping considerations are original synthesis. Published case studies are scarce — most enterprise AEM DS architectures are confidential client work and agencies publish little detail.*

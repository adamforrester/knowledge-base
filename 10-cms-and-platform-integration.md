---
type: practice-area
title: CMS and Platform Integration
description: DS in CMS environments. The seam between component governance and content governance. AEM and Drupal at depth; the four CMS architectural shapes (traditional / hybrid / headless / composable) as the framing altitude; per-platform coverage of headless platforms (Sitecore XM Cloud / Contentful / Sanity / Strapi / Storyblok), WordPress as DS host, Salesforce Commerce Cloud Page Designer, the CMS-vs-DS authoring boundary, MCP / AI-readability for CMS-managed components, and composable-content patterns.
tags: [extension, cms, content, integration, headless, composable, hybrid, salesforce, wordpress, mcp]
timestamp: 2026-06-18
---

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

## The CMS architectural axis — four shapes as a decision tree

The CMS landscape splits into four architectural shapes. The shape determines the DS engagement scope, the integration discipline, the authoring boundary, and the run-phase retainer pattern. Naming the shape at scoping is the practice's most consequential CMS decision — getting it right cascades into every downstream decision; getting it wrong produces engagements that ship the wrong architecture for the brief.

This H2 surfaces the mental model for the platform-specific sections that follow. AEM and Drupal (covered in depth below) are *traditional*. WordPress and Salesforce Commerce Cloud Page Designer are *hybrid*. Sitecore XM Cloud, Contentful, Sanity, Strapi, and Storyblok are *headless*. Uniform / Vercel-native / orchestration architectures are *composable* — a cross-cutting axis rather than a single platform shape.

### The four shapes

**Traditional.** Server-rendered, page-tree-based, where the CMS owns presentation. The CMS authoring environment is also the rendering environment; preview-as-you-author is native; templates live in the CMS's templating language; component CSS lives in the CMS's asset pipeline. **AEM** sits here (HTL templates, Sling Models, clientlibs, Editable Templates). **Drupal** sits here (Twig templates, theme libraries, SDC in 10+).

**Hybrid.** The CMS owns content and supplies authoring chrome around components, but presentation is partially decoupled. Authors get preview-as-you-author through visual editor surfaces (block-editor, page-designer); rendering can be server-side (PHP / SFRA) or client-side (React / Next.js); the DS supplies components the CMS wraps. **WordPress block themes** (FSE / Gutenberg) sit here. **Salesforce Commerce Cloud Page Designer** sits here.

**Headless.** The CMS owns content and exposes it via API; presentation is fully decoupled. Authors work in the CMS's web app (schema-first); the front-end is a separate React / Next.js / Vue / Svelte application that consumes the API; preview-as-you-author requires custom preview infrastructure (preview deployments, preview tokens, Vercel Content Link / Stega-encoded source maps). **Sitecore XM Cloud, Contentful, Sanity, Strapi, Storyblok** all sit here.

**Composable.** The CMS is one of several services in a content mesh; content-as-data with explicit per-service schemas; the integration is per-channel and the orchestration layer reconciles. This is a *cross-cutting* axis rather than a single-shape axis — composable architectures use headless CMSes (typically multiple) plus PIM, DAM, commerce, search, and personalization services, with an orchestration layer pulling from each. **Uniform** (composable orchestration), the **Vercel + Next.js + v0 composable stack**, and **Storyblok's composable orchestrator pivot** inhabit this layer. The mid-2026 consolidation event worth flagging: **Edgio (formerly Layer0) Chapter 11 bankruptcy in late 2024**, ceased CDN operations January 2025, forced enterprises to migrate to Cloudflare / Fastly / Vercel.

### Why the four-axis framing matters for scoping

The shape cascades into every downstream decision:

- **Traditional → tight DS-CMS coupling.** Components ship as clientlibs / theme libraries / SDC modules; tokens flow through the CMS's asset pipeline; the DS engagement scopes the CMS-side wrapping work as a substantial deliverable (typically 30–50% of the build hours).
- **Hybrid → partial coupling per surface.** Components ship as Gutenberg blocks / Page Designer components; authoring chrome is the CMS-supplied visual editor; rendering can be server-side or client-side; the DS engagement scopes the wrapping work plus the authoring-schema definitions.
- **Headless → loose coupling.** Components ship as a standalone library (npm package or git submodule); the CMS supplies content via API; the DS engagement scopes the integration layer (the marshalling code mapping API fields to component props) but not CMS-specific wrapping.
- **Composable → multi-service integration.** Components are the same as headless; the integration multiplies (per service); the orchestration layer is custom (off-the-shelf options exist but are not yet mature); the DS engagement is one of multiple parallel engagements (DS + commerce + content + personalization).

The practice's discipline: name the architectural shape at scoping Discovery, *before* deciding the DS architecture. The same DS architecture (a token tree + component library + docs site) lands differently in each shape. The integration work, the authoring-boundary discipline, the AI-readiness pipeline, and the run-phase retainer all shift.

### The eight-platform comparison table (synthesis-ready artefact)

| Platform | Architectural shape | DS-integration model | Authoring authority | Content-storage model |
|---|---|---|---|---|
| **AEM** | Traditional | Tight (clientlibs, HTL, Core Components) | CMS (Editable Templates, Experience Fragments, Style System) | JCR tree (hierarchical, path-addressable) |
| **Drupal** | Traditional | Tight (SDC, Twig, theme libraries) | CMS (Layout Builder, Paragraphs, Blocks) | Drupal entity API (relational, content-type-driven) |
| **WordPress** (block themes) | Hybrid | Partially-coupled (Gutenberg blocks via Block API + theme.json + ACF Blocks) | CMS (Block Editor + FSE; block patterns for compositions) | WP database (post-meta + ACF for structured content) |
| **WordPress** (headless) | Headless | Loose (REST + WPGraphQL → separate Next.js / Remix front-end) | WP admin UI (schema-light; preview via custom infrastructure or Faust.js) | WP database (consumed via API) |
| **SFCC Page Designer** | Hybrid | Partially-coupled (JSON meta + ISML SFRA path or React PWA Kit path) | CMS (Page Designer drag-and-drop; Salesforce Business Manager-hosted editor) | Salesforce content asset model + B2C Commerce APIs |
| **Sitecore XM Cloud** | Headless | Loose (JSS SDK + Next.js + Edge GraphQL API) | CMS (Sitecore Pages + Content Editor; rendering manifest) | Sitecore Content Hub + Edge API |
| **Contentful** | Headless | Loose (Delivery API + Preview API; REST or GraphQL) | CMS (schema-driven web app; preview via Vercel Content Link / Stega source maps) | Spaces + environments + content types + entries |
| **Sanity** | Headless | Loose (GROQ or GraphQL; Portable Text rendering map) | CMS (customisable Sanity Studio defined in TypeScript) | Sanity Content Lake (real-time JSON) |
| **Strapi** | Headless | Loose (REST + GraphQL; Document Service API in v5) | CMS (Strapi admin UI; self-hosted) | Self-hosted database (PostgreSQL / MySQL / MongoDB) |
| **Storyblok** | Headless (with hybrid-style preview) | Loose (storyblok-react / -vue / -svelte SDK; iframe preview-as-you-author) | CMS (visual editor with rendered-component iframe preview) | Storyblok Content Delivery API |
| **Composable** (Uniform / Vercel / Storyblok composable) | Composable | DS components consume the orchestration layer's composed content stream | Per-service authoring (CMS + PIM + DAM + commerce + personalization) plus orchestration-layer rules | Multiple services + orchestration layer that reconciles per request |

The table is the artefact the practice carries into scoping conversations. The conversation it enables: *"Which shape is your platform on? Which row of the table are we talking about?"* — a more concrete entry point than asking abstractly about CMS choice.

### The miscategorisation costs

Three miscategorisations show up in agency proposals:

**Conflating "headless CMS" with "decoupled content delivery."** Headless CMS authoring is structurally different from traditional WYSIWYG authoring — schema-first rather than content-first; no preview-as-you-author by default; content modelled as data. The agency that pitches headless thinking the authoring experience matches WordPress Gutenberg produces engagements where the client's content team rejects the platform after launch.

**Conflating "Page Designer" with "block themes."** Both supply authoring chrome around components, but Salesforce's component model uses page types and regions while WordPress uses block-grid composition. The Salesforce-specific configuration-schema-per-component model doesn't map onto the WordPress block.json shape; agency teams who treat them as equivalent produce engagements where Page Designer's authoring forms drift from the component contracts.

**Conflating "composable" with "headless."** Composable is *multi-service*; headless is *single-CMS-decoupled*. A composable architecture uses headless CMSes (typically multiple) but adds the orchestration layer that headless alone doesn't have. The agency that pitches composable thinking it's "advanced headless" misses the orchestration scope and produces engagements that ship a single headless CMS plus marketing copy claiming composability.

Articulating the four-axis framing prevents all three miscategorisations.

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

## Headless CMS coverage — Sitecore XM Cloud / Contentful / Sanity / Strapi / Storyblok

The headless CMS market in 2025–2026 has bifurcated cleanly between enterprise-grade orchestrators prioritising high-availability CDNs and developer-first frameworks offering code-centric extensibility. The practice engages with five dominant platforms; each imposes unique constraints on how the DS marshals data, renders previews, and structures content schemas.

### Sitecore XM Cloud

The Sitecore platform direction since ~2023. Sitecore split the legacy Sitecore Experience Manager (XM) and Sitecore Experience Platform (XP) into a SaaS-first headless offering: **XM Cloud** for content management; **Sitecore Personalize** (the rebranded Boxever) for personalization; the **Sitecore Experience Edge** for global delivery. The split was driven by Sitecore's commercial pressure to compete with cloud-native headless competitors; the migration path from XM 10.x to XM Cloud is non-trivial (typically a re-platform rather than an upgrade). The legacy Layout Service API has been deprecated in favour of the **GraphQL Edge API**.

The DS-integration shape centres on the **Sitecore JavaScript Rendering SDK (JSS)** and Next.js. Components built by the DS team serve as the rendering layer, receiving layout and field data mapped by the JSS SDK. Sitecore routing is driven by the **JSS manifest** (`.sitecore.js` files), which maps frontend React components to Sitecore's rendering definitions through a `componentFactory` registry. The DS engagement scopes the component library, the JSS-side wrapping (the componentFactory + per-component data-shape mapping), the rendering manifest, and Pages templates.

Two operational constraints worth naming explicitly:

- **GraphQL query depth limit.** Complex, deeply nested component architectures frequently trigger `too nested to execute` errors on the Edge API. The workaround: abandon pure Layout Service hydration and implement component-level data fetching via Next.js `getStaticProps` (or App Router equivalents) to resolve subsequent layout branches independently.
- **System-field exclusion.** Retrieving operational system fields (creation / update dates, sortable indices) requires deploying specific schema-exclusion patches to the Edge API, because default headless configurations aggressively filter fields prefixed with `__`.

Code Connect / `.ai.json` integration is feasible but not yet default — the JSS rendering manifest is the closest analogue to Code Connect (it maps Sitecore components to React components) and is custom per project. The practice's bridge investment: extend the rendering manifest with `.ai.json`-shaped metadata for AI-readability per 30. Native Sitecore-side support for Code Connect / `.ai.json` is not on Sitecore's published roadmap as of mid-2026.

Sitecore engagements are still a real cohort despite the platform's commercial pressure — large enterprises with Sitecore portfolio investment continue to renew rather than re-platform. Build scope: ~600–1,200 hours for foundations + components + JSS wrapping + rendering manifest + Pages templates.

### Contentful

The canonical headless CMS reference. Contentful has shaped the field's mental model of headless CMS authoring since the mid-2010s; the platform's structure (spaces / environments / content types / entries / assets) is the field's default vocabulary.

**The architecture.** Spaces (the multi-tenant unit) and environments (master / staging / dev within a space) structure deployment. Content types define schemas (each field has a type, validations, appearance settings). Entries are instances. Assets handle media with built-in CDN and image-transformation API. The **Content Delivery API** (CDA — REST + GraphQL) serves published content; the **Content Preview API** (CPA) serves draft content; the **Content Management API** (CMA) handles authoring operations.

**The DS-integration shape.** Components consume entries via the Delivery API; field types map to component props via a marshalling layer. Rich-text fields use `@contentful/rich-text-react-renderer` (Contentful's React rendering library) which maps document-tree nodes to React components. The DS engagement scopes the component library, the content-type schema (typically co-designed with the CMS team per the boundary discussion below), the marshalling layer (~40–80 hours per content type), and the rich-text rendering map.

**The preview problem.** Contentful's web app is schema-driven — authors fill forms whose shape matches the content type. There is **no preview-as-you-author out of the box.** The canonical 2025–2026 solution: **Vercel Content Link** (formerly Visual Editing). The pipeline relies on **Content Source Maps** — a steganography-shaped mechanism that embeds hidden Unicode metadata directly into the rendered text strings via the Live Preview SDK. When Vercel detects these encoded strings in the preview environment, it overlays an edit link mapping directly to the Contentful entry ID. The DS engineering team must implement specific sanitisation routines (such as the `splitEncoding` pattern) where these invisible characters break CSS rules — notably `letter-spacing` — or corrupt URL values. Without the sanitisation, the preview-mode bridge silently degrades production fidelity. Build scope addition for preview infrastructure: ~40–80 hours per engagement.

**The CMS-vs-DS boundary.** Contentful is the cleanest separation in the field: Contentful owns content types, fields, and entries; the DS owns components, tokens, and rendering. The boundary is enforced by the platform — there is no Contentful-side templating language; every rendering decision is in the DS code. This makes Contentful the practice's default headless-CMS recommendation when the client's preference allows.

**MCP support.** As of mid-2026, Contentful ships an **official MCP server** (`Contentful MCP Server` on GitHub; supplementary `contentful-mcp` open-source integrations from AugmentCode and others). The server exposes tools via the Management API for querying entries, validating content models, and executing AI workflows across spaces. Wrapping this existing implementation to join with the DS contract is low-effort (~16–24 hours per engagement).

### Sanity

The structured-content approach. Sanity's differentiator is **Studio** — a self-hosted, customisable authoring tool defined in TypeScript code rather than configured via web UI. The Studio is part of the project repo; schemas are TypeScript files; custom input components extend Studio's authoring forms; Studio runs locally for authors or deploys to Sanity Studio hosting for team-wide use.

**The architecture.** Content stored in **Sanity Content Lake** (Sanity's managed real-time backend). Querying via **GROQ** (Graph-Relational Object Queries; pronounced "groke") or GraphQL. **Portable Text** is Sanity's distinctive contribution: a JSON representation of rich-text content that's renderer-agnostic; per-block-type rendering is defined in code (a React component per block type — paragraph, heading, blockquote, custom — composes the rendered output).

**The DS-integration shape.** Similar to Contentful at the rendering side (components consume content via API; React components render entries) but with **Studio customisability** — the DS team can explicitly import design system components, tokens, and icons directly into the CMS authoring interface, aligning the editorial experience with the frontend reality. Custom input fields render in Studio with the agency's design; preview panes show the rendered DS-component output alongside the authoring form. The DS engagement scopes the component library, the content schema (TypeScript files; ~20–40 hours per content type), Studio customisation (~80–160 hours for a substantive customisation), and the Portable Text rendering map.

**Preview via Vercel Visual Editing.** Sanity engagements use the same Stega-encoded source-map pattern as Contentful. The DS engineering team frequently uses the `vercelStegaSplit` utility to decouple the hidden source-map metadata from the actual string value before applying it to sensitive React attributes (e.g., URLs, styles); without the split, hidden characters break hydration matching or corrupt downstream styling.

**MCP support.** Sanity ships an **official hosted MCP server** at `mcp.sanity.io` (deeply integrated; not a self-hosted wrapper). The server automatically parses TypeScript schema definitions and lets AI clients execute complex GROQ queries, manage datasets, and patch documents with full schema awareness. Available out of the box; minimal practitioner-side wrapping needed.

**When Sanity wins over Contentful.** Engagements with heavy content-model customisation; engagements where the content team values authoring-UX over SaaS convenience; engagements where the agency wants to ship a distinctive Studio as part of the deliverable. Build scope: 700–1,400 hours for foundations + components + Studio + Portable Text rendering.

### Strapi

Open-source, self-hostable, plugin-extensible. The default for engagements requiring self-hosted infrastructure: regulated industries (healthcare data sovereignty, financial services on-prem), governments with on-prem mandates, clients with strict hosting-cost constraints.

**Strapi v4 → v5 (the load-bearing version transition).** v5 (late 2024 / early 2025; v5.47 the relevant mid-2026 version for native MCP) introduced substantial architectural shifts that drastically alter the DS-integration contract:

- **Document Service API replaces Entity Service API.** Response formats flatten — the deeply nested `data.attributes` wrappers prevalent in v4 are gone. Frontend DS consumers migrating from v4 to v5 require complete refactoring of data fetching and mapping utility layers.
- **Persistent `documentId` strings replace numeric `id` parameters.** This is a breaking change to every entry-retrieval call; the migration is mechanical but ubiquitous.
- **Vite replaces Webpack for the admin panel.** Faster admin builds; meaningful for plugin-development DX.
- **Robust TypeScript support.** DS component integration into custom Strapi plugins accelerates because the plugin surface is now type-safe end-to-end.

The v4 → v5 migration is non-trivial; engagements should target v5 for new builds; verify the version per project — some clients have invested in v4 plugins that need re-architecting for v5.

**MCP support.** As of v5.47, Strapi ships a **native, opt-in MCP server.** It authenticates via scoped Admin API tokens and dynamically generates CRUD tools for every content type. Because Strapi is self-hosted, the agency can deploy bespoke MCP wrappers directly alongside the infrastructure with zero vendor coordination. This makes Strapi the most agency-controllable MCP path of the five headless platforms.

The DS-integration shape, hosting, and authoring-experience details are otherwise as the prior Strapi treatment in field literature describes; build scope: 600–1,200 hours for the DS-side work; platform scope adds 200–400 hours for Strapi setup and operations.

### Storyblok

The visual-editor + headless-API combination. Storyblok's distinctive feature: a **visual editor** that previews the rendered site as authors edit (via the `storyblok-react` / `storyblok-vue` / `storyblok-svelte` SDK rendering the components in an iframe on storyblok.com). This bridges the WYSIWYG-vs-headless gap that Contentful and Sanity don't address natively.

**The architecture.** Content stored in Storyblok's managed backend; querying via Storyblok's Content Delivery API (REST). The **storyblok-bridge** library injects the editor's preview pane with the live front-end render; authors see the rendered DS components in the iframe; clicking a component in the iframe selects it for editing in the right pane.

**The DS-integration shape.** Components are React / Vue / Svelte; Storyblok's "blocks" (content types) map to components via a `StoryblokComponent` registry. The DS engagement scopes the component library, the block schemas, the component registry, and the preview integration.

**The iframe-sandbox tradeoff.** Storyblok's preview is sandbox-shaped — it renders inside an iframe on storyblok.com, not in the deployed application's full context. Complex frontend states, interactive single-page application (SPA) routing, and tightly-coupled React context providers frequently break within the editor. The DS team must construct robust fallback states and conditional rendering logic specifically optimised for the Storyblok preview environment. The cost is real — engagement scopes typically allocate ~20–40 hours per component family for preview-environment hardening.

**When Storyblok wins.** Engagements where the content team is migrating from WordPress / WYSIWYG and needs preview-as-you-author. Engagements where the marketing team is the primary author surface and visual fidelity-during-editing is non-negotiable. Build scope: 500–1,000 hours.

### The five-platform decision tree

| Decision driver | Recommendation |
|---|---|
| Sitecore portfolio investment | Sitecore XM Cloud |
| SaaS-first; English-only or simple-locale | Contentful |
| Bespoke content models; custom Studio | Sanity |
| On-prem / regulated / cost-constrained | Strapi |
| Content team needs preview-as-you-author | Storyblok |
| First-mover on native MCP support (already shipping mid-2026) | Contentful, Sanity, Strapi (all three have official MCP) |
| Multi-CMS portfolio (composable) | Multiple platforms per service |

None of these is the practice's "default headless CMS" — the platform choice is engagement-specific. The discipline: ask the decision-driver questions at scoping; recommend per the answers; flag the trade-offs honestly.

---

## WordPress as DS host

Despite heavy industry narrative favouring composable and headless architectures, WordPress remains a high-volume, highly relevant engagement type at the agency. Procurement shapes dictate two diverging integration paths: **block-theme builds** (modern WordPress; FSE) and **headless WordPress** (REST or WPGraphQL serving a separate React front-end). The two shapes scope and price differently; the agency should articulate them as distinct engagement types.

### Block themes and Full Site Editing (FSE)

WordPress 5.9 (Jan 2022) introduced FSE; 6.0–6.4 matured it; 6.5+ added pattern-based templates and the Site Editor's interactivity API. By mid-2026, FSE / block themes is the recommended path for new theme work; classic themes (PHP-templating-based) remain supported but are increasingly limited.

**theme.json — WordPress's design tokens surface.** The `theme.json` file at the root of a block theme defines `settings.color.palette`, `settings.color.gradients`, `settings.typography.fontSizes` and `.fontFamilies`, `settings.spacing.spacingSizes`, `settings.layout.contentSize` and `.wideSize`, plus element-level and block-level style tokens. This is directly analogous to design tokens in the DS sense.

**The DS-integration shape relies on Style Dictionary.** A custom format transform within Style Dictionary ingests the agency's primitive and semantic tokens and outputs a fully compliant `theme.json` artefact. Tokens automatically flow into the WordPress Block Editor (Gutenberg), populating the `settings.color.palette` and `settings.typography.fontSizes` UI controls. **Because there is currently no formal DTCG specification dictating CMS synchronisation, the practice must maintain custom parsers mapping the DTCG format to the WordPress schema.** Practitioner bridge investment: ~8–16 hours for the Style Dictionary transform; reusable across WordPress engagements.

**Block patterns and block templates.** Block patterns are reusable composed-content blocks (a "Hero with CTA" pattern); analogous to AEM Experience Fragments. Block templates define page structures (`single.html` defines the single-post layout); analogous to AEM Editable Templates. Both are governed by the theme.

### Custom blocks (Gutenberg blocks) as the component primitive

Each block is a React component (in the editor) plus a save function (rendered output) plus `block.json` (metadata). Two registration paths:

- **Native Block API.** Full path — JavaScript registration via `registerBlockType`; React component for the editor; save function or `render_callback` for the front-end. Higher engineering investment (React fluency required); higher fidelity (preview-as-you-author works exactly as designed).
- **ACF Blocks (Advanced Custom Fields).** Common workaround for clients without React engineering. ACF Blocks register via PHP; the editor renders via PHP-shaped previews (lower fidelity); fields configured via ACF's admin UI; `render_callback` handles output. **The trade-off is severe**: ACF blocks rely on server-side rendering via PHP, drastically reducing the instant client-side preview fidelity of the Block Editor and forcing the DS team to maintain dual template ecosystems (React for the DS documentation; PHP for the CMS).

The practice's discipline: native Block API for engagements with engineering depth; ACF Blocks for engagements where the client's content team will maintain blocks long-term without React skills.

### The DS-vs-block-pattern boundary

Block patterns are reusable layout compositions; DS components are reusable primitives. Where the DS-component library ends and the block-pattern library begins is a procurement-grade decision.

The practice's working position: **DS components ship as Gutenberg blocks (the primitives); block patterns are *compositions of DS components* (the layouts) and ship as part of the theme rather than the DS.** A "Hero" component (DS primitive) is a block. A "Hero with CTA above three feature cards" pattern (a layout composition) is a block pattern. Both ship from the theme; the DS owns the primitives; the theme owns the patterns.

Attempting to manage complex page layouts as monolithic DS components collapses the composability of the WordPress editor and forces the agency to ship updates as DS releases when they should be authoring updates in the theme.

### Headless WordPress

REST API + **WPGraphQL** (~2.0 stable as of mid-2026; the de facto standard). Content types and ACF fields surface via the API; a separate Next.js / Remix front-end consumes them.

**The DS-integration shape mirrors Contentful / Sanity at the consumer side.** WordPress's authoring surface is the trade-off — the WP admin UI is functional but not optimised for headless-CMS use; preview-mode states show the WP-classic UI elements that confuse content teams in a headless context.

**Architecture options.** **Faust.js** (WP Engine's headless-WordPress framework) is the most opinionated — provides preview infrastructure, authentication, and pre-built Next.js components. **WPGraphQL + Next.js bare** is the more flexible — agency builds the integration from scratch. **WordPress.com's headless toolchain** is a third option for clients on WordPress.com.

**MCP support.** As of mid-2026, WordPress core ships an **official MCP Adapter via Automattic**, built on the new **WordPress Abilities API**. The adapter translates MCP protocols to HTTP REST endpoints and uses a proxy (`mcp-wordpress-remote`) to execute authenticated operations. **InstaWP** provides one-click MCP-server deployments for managed setups; **WooCommerce** has its own MCP integration documented in WooCommerce Developer Docs. The adapter pattern is more layered than Contentful or Sanity's direct MCP servers but is shipping today.

### The two shapes price differently

| Engagement shape | Build scope | Notes |
|---|---|---|
| Block-theme build (DS + theme + custom blocks + block patterns) | ~250–500 hours | Tight coupling to WP editor environment; preview-as-you-author native via FSE |
| Headless WordPress (DS + components + Next.js front-end + WPGraphQL integration + custom preview) | ~300–600 hours | Loose coupling; custom preview infrastructure required; Faust.js alleviates routing friction |

The procurement shape determines team composition (block-theme needs WP-PHP fluency alongside React; headless WP can be React-only with WP set up by a separate team) and delivery model (block-theme ships into the WP install; headless WP ships a separate front-end with a content-API contract).

---

## Salesforce Commerce Cloud Page Designer

Per 00b §Active engagement examples — the New Balance engagement is on Salesforce Commerce Cloud (SFCC), with **Chakra UI** as the consuming front-end framework. The engagement built a Figma library for the Australian site launch (tied to Australian Open) which the client dev team built from. The current question is scaling the Australian work across other regions, with potential platform considerations including migration to SFCC if not already there. This section addresses the Salesforce-specific authoring surface — **Page Designer** — and its relationship to SFCC's broader architecture stack.

### The SFCC platform stack

Three layers, evolving over the platform's history:

**Storefront Reference Architecture (SFRA).** The legacy server-rendered path. Based on Mustache-shaped ISML templates (`.isml` files) and the SiteGenesis cartridge model. Cartridges are SFCC's deployment unit; the controller layer handles request routing; the model layer accesses the data API; the view layer renders ISML. Still in widespread use across SFCC's installed base; the cartridge model is the platform's foundation.

**Page Designer.** Salesforce's drag-and-drop component-composition authoring surface. Layered on top of SFRA (Page Designer pages are rendered by SFRA's controllers); gives content authors the ability to compose pages from pre-defined components without engineering involvement. Released ~2018, matured through 2020–2024; mid-2026 is stable but not the platform's flagship direction.

**Headless Commerce / PWA Kit / Composable Storefront / Storefront Next.** The modern direction since ~2022. **PWA Kit** is Salesforce's React-based front-end framework that consumes the **B2C Commerce APIs** (REST + GraphQL surfaces over the legacy SFRA models). The **Storefront Next** architecture is the 2025+ evolution: relies on **React Router 7**, leveraging streaming server-side rendering (SSR) and data loaders to fetch SFCC APIs before hydrating the React application on the client. ISML is entirely removed in this path. **Composable Storefront** ships as a Next.js / PWA Kit hybrid for greenfield engagements.

### Page Designer's component model

The authoring surface uses three concepts:

**Page types** — the top-level composable surface. Standard page types ship out of the box: `Storefront Page`, `Category Page`, `Product Page`, `Article Page`, `Search Results Page`. Custom page types are defined in JSON metadata; they declare which regions exist and which components are allowed in each region.

**Regions** — the slot-shapes within a page type. A page type might declare regions like `Header`, `Hero`, `Body`, `Footer`. Each region has a name, an ID, and rules about which components can drop into it (typed by component category — `Hero`, `Card`, `Slot`, etc.).

**Components** — the building blocks authors drop into regions. Each component requires a **JSON meta-definition file** located in the custom cartridge (`/experience/pages` or `/experience/components`). The schema dictates `region_definitions` (component exclusion rules and instantiation limits) and `attribute_definitions` (the configuration schemas that populate the merchant's authoring form). The DS-integration shape requires wrapping foundational DS components inside Page Designer component scripts; the merchant's input on the PD configuration schema is mapped directly to the DS component's props.

### Page Designer pages in PWA Kit / Storefront Next

Page Designer pages are resolved in the PWA Kit via a **component registry**. The DS integration requires executing an `initializeRegistry()` function during app startup that lazily imports React components mapped to specific SFCC `typeId` strings. When the Page Designer API returns a layout payload, the `<Component>` wrapper dynamically resolves the registered React component and injects the authored attributes.

This is the load-bearing operational pattern for headless SFCC engagements; build it wrong and Page Designer pages render as opaque containers in the headless front-end.

### Chakra UI as the New Balance choice

Chakra UI is a React component library with strong accessibility and theming support; selected by many SFCC engagements as the "DS in a box" starting point. The DS-integration question for the New Balance engagement: **how does the agency-built DS layer relate to Chakra?**

Two patterns:

**Pattern A: Lightweight extension** — map the agency's design tokens directly into Chakra's theming engine via Chakra's native theme system. Components consume Chakra primitives styled with the agency's tokens. Build scope: 200–400 hours.

**Pattern B: Heavy wrapping** — treat Chakra purely as an unstyled headless primitive layer (per 33 §4's headless-vs-opinionated split); wrap it in bespoke, agency-authored React components to exert total control over the DOM and visual styling. Build scope: 600–1,000 hours.

Pattern A is cheaper and faster but locks the engagement to Chakra's evolution; Pattern B is more expensive but produces a DS the client can maintain independently of Chakra's release cycle.

### Salesforce-specific authoring patterns and scoping

**The Page Designer visual editor is exclusively hosted within Salesforce Business Manager.** Unlike Storyblok or Sanity, the agency cannot easily inject custom iframe preview environments or local development UI wrappers without relying on complex proxy setups. The editor's component palette is determined by the component definitions registered in the cartridge; the configuration schemas drive the authoring forms authors fill in per instance.

**Per-component SFCC overhead beyond standard DS work.** Each component requires:
- A component definition file (~5–10 hours for a simple component; ~15–25 for complex)
- A configuration schema (~3–8 hours per component depending on author-configurable surface)
- An ISML or React render template (~4–10 hours per component)
- Per-region compatibility metadata (~1–2 hours per component)

Total: **~13–45 hours per component beyond standard DS-component work.** For a 30-component DS shipping to Page Designer: ~400–1,400 additional hours of SFCC-specific wrapping — a meaningful scope the practice should make visible in proposals.

### The scope of the Salesforce engagement

| Engagement shape | Build scope |
|---|---|
| Greenfield SFCC + DS + Page Designer + headless front-end with Chakra UI (Pattern A) | ~500–800 hours |
| Greenfield SFCC + DS + Page Designer + bespoke DS wrapping Chakra primitives (Pattern B) | ~900–1,400 hours |
| Migration / scaling engagement (per New Balance: existing DS, scale to new regions) | ~250–500 hours per region |

The complication 00b flags about platform migration. If the client is on legacy commerce architecture and the regional scaling triggers a platform decision, the SFCC platform migration itself is a $10–50M-range decision the DS engagement layers on top of — typically with a separate platform-implementation team (Salesforce-certified partner) handling the SFCC build while the agency handles the DS layer. The DS engagement should not absorb platform-migration scope; the practice's discipline is to scope the DS work explicitly against the chosen platform and flag platform decisions as parallel engagements.

---

## The CMS-vs-DS authoring boundary

One of the most profound scoping failures in agency CMS implementations stems from an undefined authoring boundary between the design system and the CMS. Without an articulated POV, engagements suffer from structural collapse: the CMS attempts to manage presentation details, or the DS inadvertently hardcodes editorial content. This section closes the gap.

### The boundary the existing material articulates

Per 04 §Content as a system layer — *"tokens for templated, system-level content; CMS for editorial, product-specific content."* The line is articulable at the *content* layer; this section extends it to the *component-anatomy* layer.

### The component-anatomy boundary

The DS owns component **structure** — the props the component accepts, the states it renders, the slots it composes. The CMS owns content **instances** — the specific values authors fill in per instance.

A worked example. A Hero component has props for `heading`, `subheading`, `ctaLabel`, `ctaUrl`, `backgroundImage`, and `variant: "left-aligned" | "centered" | "right-aligned"`. The DS owns the props' shape, the variants' rendering logic, the component's a11y contract. The CMS owns the per-instance values (the homepage's hero heading; the campaign-page's CTA label; the article's background image asset reference).

**Providing a CMS author with a hex-code color picker to override a component's background violates the boundary.** Providing a dropdown selection referencing `Brand Variant A` or `Brand Variant B` (which map back to DS tokens) respects it. The same logic applies to typography, spacing, motion — everything in the token tree.

### The Code Connect / `.ai.json` parallel

Per 30 — Code Connect binds Figma components to code components; `.ai.json` exposes the structured AI-readable surface. For CMS-managed components, the `.ai.json` registry must source from *both* the DS code surface (for component structure) and the CMS schema (for content-instance shape). The shape this implies:

```json
{
  "component": "Hero",
  "structure": {
    "source": "ds-code",
    "props": [
      { "name": "heading", "type": "string", "required": true },
      { "name": "ctaLabel", "type": "string", "required": true },
      { "name": "variant", "type": "enum", "values": ["left-aligned", "centered", "right-aligned"] }
    ]
  },
  "instances": {
    "source": "cms",
    "platform": "contentful",
    "contentType": "Hero",
    "fieldMapping": {
      "heading": "heading",
      "ctaLabel": "primaryCtaLabel",
      "variant": "layoutVariant"
    }
  }
}
```

The structured surface lets AI clients reason about *what components exist* (DS) AND *what content fills them per instance* (CMS).

### The boundary table (synthesis-ready artefact)

| Anatomy / content type | Source of truth | Operational rules & enforcement |
|---|---|---|
| **Component structure** (props, states, slots, DOM) | Design System | Defines accepted props, internal state logic, slots, DOM structure. Cannot be altered via CMS. |
| **Component variants** (visual / behavioural) | Design System | Defines visual / behavioural modes (Dark Mode, Outlined, Ghost). The CMS exposes these only as strict dropdown enumerations based on DS configuration schemas. |
| **Templated content** (CTAs, validation errors, empty states) | DS Tokens (per 04) | System-wide microcopy. Stored in the DS content-token catalogue. |
| **Editorial content** (marketing copy, product descriptions, asset media) | CMS | Authored per instance via the CMS's content-type form. |
| **Per-instance overrides** (this Hero's headline; this CTA's label) | CMS | Bounded by character limits and validation rules defined in the DS. |
| **Layout composition** (page-level structural orchestration) | CMS | The CMS dictates the grid and region layout, using DS components as the atomic building blocks. |
| **Localisation variants** | CMS / DS | Editorial content resides in the CMS; interface / system-level translations reside in the DS content-token catalogue. |
| **Component anatomy decisions** (what props exist, what states are valid) | DS | Schema changes to component anatomy require DS-team review; CMS adjusts to match. |
| **Content-type schema decisions** (what fields a content type has) | CMS team (with DS-team consultation) | Schema changes to content types require CMS-team ownership; DS provides the field-to-prop mapping. |

### Scoping implications

**Name the boundary in the SOW.** Without explicit naming, the boundary drifts during the engagement — typically toward CMS-instance-as-presentation, which collapses the DS's structural authority.

Three concrete failure modes the practice has lived through:

- **The CMS-instance-as-style-override failure.** Authors get the ability to override individual component styles per instance (font size, color, spacing) via CMS configuration fields. The boundary collapses; the DS's design tokens become advisory rather than enforced; visual fragmentation accumulates by release.
- **The CMS-as-component-author failure.** Content team starts authoring new component types in the CMS without DS-team review; new types replicate existing DS components with slight modifications; the catalogue of "what components exist" splits between DS code and CMS content-type definitions.
- **The DS-as-content-store failure.** DS team starts hardcoding content into components ("Welcome to our site!" embedded in a HomepageHero component); the boundary collapses in the other direction; content updates require DS code releases rather than CMS authoring.

Naming the boundary at scoping prevents all three. The boundary is reviewed at major release boundaries to ensure it's still where the practice put it.

---

## MCP / AI-readability for CMS-managed components

Per 30 §MCP and 34 §5 — the AI-readability registry exposes structured component contracts to AI clients. When components are authored *and stored* in the CMS, the `.ai.json` registry must source from the CMS too. **As of mid-2026, CMS-vendor-native MCP shipping has moved much faster than 34 §5 anticipated** — Contentful, Sanity, Strapi, and WordPress all ship official MCP support (with caveats per platform). This section is the per-CMS feasibility map.

### Per-CMS feasibility (mid-2026 reality)

| CMS | Native MCP status (mid-2026) | Surface | Practitioner-side wrapping |
|---|---|---|---|
| **Contentful** | **Official MCP server shipping.** The `Contentful MCP Server` (GitHub) operates via the Management API; community variants like `contentful-mcp` (AugmentCode) wrap delivery surfaces. | Tools for querying entries, validating content models, executing AI workflows across spaces. | Low-effort wrapping to join with DS contract: ~16–24 hours per engagement. |
| **Sanity** | **Official hosted MCP server at `mcp.sanity.io`.** Deeply integrated; auto-parses TypeScript schema definitions. | GROQ queries, dataset management, document patching with full schema awareness. | Available out of the box; minimal wrapping needed. |
| **Strapi** | **Native, opt-in MCP server in v5.47.** Built-in; authenticates via scoped Admin API tokens. | Dynamically generates CRUD tools for every content type. Self-hosted means zero vendor coordination. | Most agency-controllable MCP path; the agency deploys bespoke MCP wrappers directly alongside the Strapi infrastructure. |
| **WordPress** | **Official MCP Adapter via Automattic.** Built on the new WordPress Abilities API. | Adapter translates MCP protocols to HTTP REST endpoints; proxy (`mcp-wordpress-remote`) for authenticated operations; InstaWP provides one-click MCP-server deployments; WooCommerce has its own MCP integration. | More layered than Contentful / Sanity but shipping today. |
| **Storyblok** | Custom wrapping. Storyblok has signalled AI direction publicly; native MCP not yet shipping but expected. | Content Delivery API (REST) is the wrappable surface. | ~20–32 hours per engagement. |
| **Sitecore XM Cloud** | Custom wrapping. Edge GraphQL is well-structured but bespoke MCP server tooling is required. | JSS rendering manifest is the closest existing surface. | ~24–40 hours per engagement; rendering-manifest as partial Code Connect equivalent. |
| **AEM** | Custom wrapping. Sling Model Exporter (`.model.json`) is the closest API surface. | JCR content tree is genuinely different from a flat content-model API. | ~32–60 hours per engagement; non-trivial. |
| **Salesforce Page Designer / SFCC** | Not feasible at scale. B2C Commerce API surfaces are vendor-specific; vendor lock-in concerns and authentication complexities. | Custom wrapping typically out of scope for SFCC engagements. | ~32–60 hours when required; usually deferred. |

### The practice's bridge investment

For platforms without native MCP (Storyblok, Sitecore, AEM, SFCC), the practice operates a custom MCP wrapper per engagement. Typical scope: **16–60 hours per CMS** depending on platform shape and wrapping work required. Amortises across engagements that ship to the same CMS — an AEM MCP wrapper built for one engagement is reusable across the practice's AEM portfolio.

**The combined tool surface.** The seven-tool conceptual surface from 15 (`list_components`, `get_component`, etc.) extends to CMS-managed components with additional tools:
- `list_content_types` — lists the CMS's content-type catalogue
- `get_content_schema` (or `get_content_type`) — returns the schema for a specific content type
- `query_entries` — returns content instances matching filters
- `get_populated_instance` (or `get_entry`) — returns a specific content instance with all field values

Combined with the DS-side tools, the AI client reasons about *what components exist*, *what their structure is*, *what content types map to them*, *what instances exist*, *what values fill the instances*.

### The CMS-as-DS-source pattern (failure mode)

A specific case worth naming: when the CMS itself is the authoring surface for the DS's component structure. The DS's component anatomy lives in the CMS as content-type schemas; the rendering layer is generic; the design-system code is thin to the point of being absent.

**The practice's position: typically not appropriate.** This is the extreme case of CMS-vs-DS-authoring-boundary collapse; appropriate only for **thin presentation-layer DSes** where the component set is small and stable (under 10 components), a non-engineering team needs to author components without a code release, and the engineering investment required to ship a "real" DS is unjustified.

Outside those conditions, the pattern collapses the DS's structural authority, makes the AI-readability layer harder to ship cleanly, and produces engagements where the "design system" is effectively a CMS configuration. When the practice encounters this pattern, the discipline is to name it explicitly: *"This is a CMS-shaped pattern, not a design system. We can work with it; we cannot call it a design system without misrepresenting what we're delivering."*

---

## Composable-content patterns

The 2025–2026 composable movement represents the evolution of headless architecture into the "content mesh." In a composable digital experience platform (DXP), content is no longer the output of a single monolithic CMS; it is a continuously orchestrated artefact aggregated from specialised microservices via a unified orchestration layer.

### Vendors and the consolidation event

Vendors in this space:
- **Uniform** — composable orchestration; pulls from headless CMSes, commerce, personalization, search; provides a unified content-delivery layer with the **Uniform Visual Workspace** for canvas composition
- **Vercel's content-platform direction** — the Next.js + V0 + Vercel-native composable stack; uses Edge Functions and Vercel KV / Postgres / Blob as the orchestration substrate
- **Storyblok's composable direction** — Storyblok has pivoted from pure headless to composable-aware orchestration

**The consolidation event worth flagging: Edgio (formerly Layer0) Chapter 11 bankruptcy in late 2024**, ceased CDN operations January 2025. Enterprises on Layer0 / Edgio rapidly migrated to Cloudflare, Fastly, or Vercel. The composable-DXP layer is mid-maturity as of mid-2026 — the architectural shape is established; the off-the-shelf orchestration tooling is improving but still requires significant custom integration per engagement.

### What "composable" means architecturally

Content types are defined per service:
- **Editorial content** in a headless CMS (Contentful / Sanity)
- **Product data** in a commerce platform (Salesforce Commerce / commercetools / Shopify)
- **Marketing assets** in a DAM (Cloudinary / Bynder)
- **Search results** in a search service (Algolia / Elasticsearch)
- **Personalization decisions** in a personalization platform (Sitecore Personalize / Optimizely / Adobe Target / Segment / 6sense)

The orchestration layer pulls from each service per request and composes the rendered output. The DS sits at the rendering layer, consuming the orchestrated content stream rather than a single CMS's output. The DS-component contract is the same; the integration is per-service.

### Schema-first authoring and composition-at-render

Each service in the composable stack defines its own schema; the orchestration layer reconciles. The DS's component contract is the **common vocabulary** across the stack — components are the consumers of all services' content; the DS's schema defines what each component expects regardless of which service supplies the content.

A worked example. A ProductCard in a composable architecture might consume product name + price + image + SKU from the commerce platform, marketing copy + lifestyle imagery + brand story from the headless CMS, personalised recommendation rationale from the personalization platform, and search-relevance score from the search service when the card appears in search results. The DS defines the ProductCard's props (the component's expected input shape); the orchestration layer queries each service per request and assembles the props' values; the DS renders the assembled values.

Because composable content is bound at request-time on edge infrastructure, **preview-as-you-author becomes a highly complex, multi-service reconciliation problem.** Vercel addresses this via steganography (Content Source Maps) injected across the payload (the same Stega-encoded mechanism that Contentful and Sanity use); Uniform relies on dedicated Canvas compositions. The DS team must guarantee that component prop shapes are resilient to partial data payloads (e.g., if the PIM responds but the CMS draft fails to resolve in the preview environment).

### The variability-by-design problem applied to content

Per 04 §AI-surface enforcement (and 26's residual gap on variability-by-design tooling) — the variability-by-design problem applies at the composable layer. The author specifies a *space* of possible content compositions; the orchestration layer pulls from each service; the rendered output is one realisation of that space.

The practice's discipline: composable content benefits from the same variant-logging / eval-driven QA pattern that 27 names for adaptive UI. Per-render variance is bounded by the schema contract. Variant-logging captures what the authors specified and what the orchestration produces; eval-driven QA validates the rendered compositions against brand and content guidelines and against WCAG.

### The boundary between content tokens and composable content

Per 04 §Content as a system layer — content tokens are templated content the DS owns; composable content is editorial content the orchestration layer composes. Both treat content as data; the difference is the authoring surface (DS catalogue for tokens; CMS / PIM / DAM for composable content). The two coexist in composable architectures.

A worked example in a composable e-commerce architecture: the "Add to cart" button label is a DS content token (system-level; consistent across products and locales); the cart-update error message is a DS content token; the product name is composable content (from commerce); the marketing banner above the cart is composable content (from CMS, possibly personalised); the personalized recommendation rationale is composable content (from personalization). Both layers ship; the DS's content-token catalogue handles system-level templated content; the composable architecture handles editorial / product / marketing content.

### Practitioner-side scoping

Composable engagements are the most architecturally complex of the four shapes. Scope **~1.5–2× a comparable headless engagement** because the integration surface multiplies (each service is a separate integration); the orchestration layer is custom (typically; off-the-shelf orchestration is starting to ship from Uniform and Vercel but not yet mature).

For agency clients on composable platforms, the DS engagement typically lands as one of multiple parallel engagements (DS + commerce + content + personalization). The DS engagement scopes:
- The component library (standard DS scope)
- The DS-component contract (the common vocabulary that all services map onto)
- The orchestration-layer integration (typically custom; ~120–250 hours)
- The preview infrastructure (typically custom; ~80–160 hours)
- The variant-logging / eval-driven QA infrastructure (per 04 / 27; ~40–80 hours)

Total composable DS engagement scope: **~800–1,500 hours** for a moderate-complexity engagement; **~1,500–2,500 hours** for an enterprise composable platform with substantial integration surface.

The DS engagement rarely operates in isolation; it functions as one parallel workstream alongside dedicated commerce, CDP, and middleware integration squads, requiring highly disciplined API contract negotiations before the first React component is ever drafted.

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

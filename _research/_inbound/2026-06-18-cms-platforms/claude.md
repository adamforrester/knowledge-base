# Modern CMS platforms — the deepen layer above 10's AEM-and-Drupal shape

10's existing material treats AEM as the dominant treatment with Drupal as a secondary comparative. The treatment is rigorous at *traditional CMS* altitude — clientlibs, Sling Models, JCR, HTL, the Style System, Editable Templates, Experience Fragments, Content Fragments, the SPA Editor deprecation, the three integration-architecture options. The practice's audit at the start of the §1.32 run found 10 to be load-bearing for AEM-shaped engagements (still the primary cohort in the agency's enterprise client base) and useful as a comparative for Drupal-shaped engagements. What 10 does *not* cover — and what the agency's clients on Sitecore, Contentful, Sanity, Strapi, Storyblok, WordPress, and Salesforce Commerce Cloud increasingly need — is the modern composable / headless / hybrid / Page-Designer surface above and around the AEM / Drupal coverage. This run closes that gap.

The synthesis path is **deepen 10, not a new file** — committed in 09 §1.32 and confirmed for this run. Structurally: a new framing-altitude H2 lands near the top of 10 (between §Central problem and §AEM Architecture Fundamentals) that names the four CMS architectural shapes — traditional / hybrid / headless / composable — as a decision tree above the existing platform-specific material. New platform and concept H2 sections append after §Drupal but before §DS Delivery Model: NPM Package vs. Embedded. The existing §AEM and §Drupal sections stay intact; the cross-cutting §Delivery Model section continues to apply across all platforms.

A note on currency before anything else. The CMS landscape evolves faster than typography fundamentals (per 23) but slower than MCP tooling (per 34). Specific tooling claims about Sitecore XM Cloud's GraphQL Edge API, Contentful's Studio direction, Sanity's GROQ vs. GraphQL split, Salesforce Page Designer's relationship to PWA Kit, and the composable-DXP vendor landscape (Uniform, Layer0, Vercel's composable direction) all reflect mid-2026 platform state; verify against current docs before treating any specific claim as load-bearing in client work. The architectural shape — the four axes and the boundary disciplines they impose — is more durable than the platforms attached to it. Bet on the architecture, not on the platform.

---

## 1. The CMS architectural axis — the framing altitude

### Four shapes, one decision tree

Modern CMS work splits into four architectural shapes. The shape determines the DS engagement scope, the integration discipline, the authoring boundary, and the run-phase retainer pattern. Naming the shape at scoping is the practice's most consequential CMS decision.

**Traditional.** Server-rendered, page-tree-based, where the CMS owns presentation. The CMS authoring environment is also the rendering environment; preview-as-you-author is native; templates live in the CMS's templating language; component CSS lives in the CMS's asset pipeline. **AEM** sits here (HTL templates, Sling Models, clientlibs, Editable Templates). **Drupal** sits here (Twig templates, theme libraries, Single Directory Components in 10+).

**Hybrid.** The CMS owns content and supplies authoring chrome around components, but presentation is partially decoupled. Authors get preview-as-you-author through visual editor surfaces (block-editor, page-designer); rendering can be server-side (PHP/SFRA) or client-side (React/Next.js); the DS supplies components the CMS wraps. **WordPress block themes** (FSE / Gutenberg) sit here. **Salesforce Commerce Cloud Page Designer** sits here.

**Headless.** The CMS owns content and exposes it via API; presentation is fully decoupled. Authors work in the CMS's web app (schema-first); the front-end is a separate React / Next.js / Vue / Svelte application that consumes the API; preview-as-you-author requires custom preview infrastructure (preview deployments, preview tokens). **Sitecore XM Cloud, Contentful, Sanity, Strapi, Storyblok** all sit here.

**Composable.** The CMS is one of several services in a content mesh; content-as-data with explicit per-service schemas; the integration is per-channel and the orchestration layer reconciles. This is a *cross-cutting* axis rather than a single-shape axis — composable architectures use headless CMSes (typically multiple) plus PIM, DAM, commerce, search, and personalization services, with an orchestration layer pulling from each. **Uniform** (composable orchestration), **Layer0** (composable edge), and the **Vercel + Next.js composable stack** inhabit this layer. Storyblok and Contentful have both pivoted toward composable-aware orchestration alongside their headless cores.

### Why the four-axis framing matters for scoping

The agency that pitches a "CMS implementation" without knowing which shape the client's procurement or technology-selection conversation has already determined produces engagements that ship the wrong architecture for the brief. The shape cascades into every downstream decision:

- **Traditional → tight DS-CMS coupling.** Components ship as clientlibs / theme libraries / SDC modules; tokens flow through the CMS's asset pipeline; the DS engagement scopes the CMS-side wrapping work as a substantial deliverable (typically 30–50% of the build hours).
- **Hybrid → partial coupling per surface.** Components ship as Gutenberg blocks / Page Designer components; authoring chrome is the CMS-supplied visual editor; rendering can be server-side or client-side; the DS engagement scopes the wrapping work plus the authoring-schema definitions.
- **Headless → loose coupling.** Components ship as a standalone library (npm package or git submodule); the CMS supplies content via API; the DS engagement scopes the integration layer (the marshalling code mapping API fields to component props) but not CMS-specific wrapping.
- **Composable → multi-service integration.** Components are the same as headless; the integration multiplies (per service); the orchestration layer is custom (off-the-shelf options exist but are not yet mature); the DS engagement is one of multiple parallel engagements (DS + commerce + content + personalization).

The practice's discipline: name the architectural shape at scoping Discovery, *before* deciding the DS architecture. The same DS architecture (a token tree + component library + docs site) lands differently in each shape. The integration work, the authoring-boundary discipline, the AI-readiness pipeline, and the run-phase retainer all shift.

### The eight-platform comparison table (synthesis-ready artefact)

| Platform | Architectural shape | DS-integration model | Authoring authority | Content-storage model |
|---|---|---|---|---|
| **AEM** | Traditional | Clientlibs + HTL / Sling Models; React/Web Components via SPA Editor (deprecating); Edge Delivery as 2025+ direction | Editable templates + policies; Style System for variants; Experience Fragments for compositions | JCR content tree (hierarchical, path-addressable) |
| **Drupal** | Traditional | Theme libraries + Twig; Single Directory Components in 10+; Web Components via custom modules | Layout Builder + Paragraphs + Blocks; entity-type-driven content structure | Drupal entity API (relational, content-type-driven) |
| **WordPress (block themes)** | Hybrid | Gutenberg blocks via Block API + theme.json + ACF Blocks | Block Editor + FSE; block patterns for compositions; theme.json for tokens | WP database (post-meta-driven; ACF for structured content) |
| **WordPress (headless)** | Headless | REST + WPGraphQL → separate React/Next.js front-end | WP admin UI (schema-light; not optimised for headless); preview via custom infrastructure | WP database (same as block-theme but consumed via API) |
| **Salesforce Page Designer** | Hybrid | SFRA cartridge components or PWA Kit React components; Page Designer wrapping per component | Page Designer drag-and-drop; component config schemas | Salesforce content asset model + B2C Commerce APIs |
| **Sitecore XM Cloud** | Headless | React (typically Next.js) via Sitecore JSS SDK; Layout Service / Edge GraphQL | Sitecore CM web app; Pages editor; rendering manifest | Sitecore Content Hub + Edge API (GraphQL) |
| **Contentful** | Headless | Standalone React/Next.js consuming Delivery API + Preview API (REST or GraphQL) | Web app; schema-driven; preview via custom preview environment | Spaces + environments + content types + entries |
| **Sanity** | Headless | Standalone React/Next.js consuming GROQ or GraphQL; Studio customisation defined in code | Sanity Studio (self-hosted, customisable); Portable Text for rich content | Sanity Content Lake |
| **Strapi** | Headless | Standalone React/Next.js consuming REST or GraphQL; admin-API for management | Strapi admin UI (self-hosted); plugin-extensible | Self-hosted database (MySQL / PostgreSQL / MongoDB) |
| **Storyblok** | Headless (with hybrid-style preview) | Components consumed via storyblok-react / storyblok-vue / storyblok-svelte SDK | Visual editor with iframe preview-as-you-author; blocks-as-components mapping | Storyblok content delivery API |
| **Composable (Uniform / Layer0 / Vercel-native)** | Composable | DS components consume the orchestration layer's composed content stream | Per-service authoring (typically: editorial in headless CMS, product in commerce, marketing in DAM) plus orchestration-layer rules | Multiple services + orchestration layer that reconciles per request |

The table is the artefact the practice carries into scoping conversations. The conversation it enables: *"Which shape is your platform on? Which row of the table are we talking about?"* — a more concrete entry point than asking abstractly about CMS choice.

### The miscategorisation costs to name

Three miscategorisations show up in agency proposals.

**Conflating "headless CMS" with "decoupled content delivery."** The two concepts overlap but headless CMS authoring is structurally different from traditional WYSIWYG authoring — schema-first rather than content-first; no preview-as-you-author by default; content modelled as data. The agency that pitches headless thinking the authoring experience matches WordPress Gutenberg produces engagements where the client's content team rejects the platform after launch.

**Conflating "Page Designer" with "block themes."** Both supply authoring chrome around components, but Salesforce's component model uses page types and regions while WordPress uses block-grid composition. The Salesforce-specific configuration-schema-per-component model doesn't map onto the WordPress block.json shape; agency teams who treat them as equivalent produce engagements where Page Designer's authoring forms drift from the component contracts.

**Conflating "composable" with "headless."** Composable is *multi-service*; headless is *single-CMS-decoupled*. A composable architecture uses headless CMSes (typically multiple) but adds the orchestration layer that headless alone doesn't have. The agency that pitches composable thinking it's "advanced headless" misses the orchestration scope and produces engagements that ship a single headless CMS plus marketing copy claiming composability.

Articulating the four-axis framing prevents all three miscategorisations.

---

## 2. Headless CMS coverage — Sitecore XM Cloud / Contentful / Sanity / Strapi / Storyblok

### Sitecore XM Cloud

The Sitecore-platform direction since 2023. Sitecore split the legacy Sitecore Experience Manager (XM) and Sitecore Experience Platform (XP) into a SaaS-first headless offering: **XM Cloud** for content management; **Sitecore Personalize** (the rebranded Boxever) for personalization; the **Edge Delivery Network** for rendering and caching. The split was driven by Sitecore's commercial pressure to compete with cloud-native headless competitors; the migration path from XM 10.x to XM Cloud is non-trivial (typically a re-platform rather than an upgrade).

**Architecture for DS work.** Components in XM Cloud are React (typically Next.js with the Sitecore JSS — JavaScript Services — SDK). The CMS exposes layout via the **Edge GraphQL API** (the Layout Service API is being deprecated in favour of GraphQL Edge). Content surfaces via the same Edge API. Personalization data flows through Sitecore Personalize's API alongside content.

**The DS-integration shape.** The React components are the DS components (or a thin layer on top of the DS); the JSS SDK marshals JSS data → component props through a `componentFactory` registry that maps Sitecore component names to React components. The DS engagement scopes:
- The component library (standard DS scope)
- The JSS-side wrapping (the componentFactory + the per-component data-shape mapping)
- The rendering manifest (the JSON file declaring which components exist for the Sitecore CM authoring surface)
- Page templates (Sitecore Pages composes components; the templates declare allowed components and slot shapes)

**Code Connect and `.ai.json` integration.** Feasible but not yet default — the JSS rendering manifest is the closest analogue to Code Connect (it maps Sitecore components to React components) and is custom per project. The practice's bridge investment: extend the rendering manifest with `.ai.json`-shaped metadata for AI-readability per 30. As of mid-2026 this is custom work; native Sitecore-side support for Code Connect / `.ai.json` is not on Sitecore's published roadmap.

**Practitioner reality.** Sitecore engagements are still a real cohort despite the platform's commercial pressure — large enterprises with Sitecore portfolio investment continue to renew rather than re-platform. The DS engagement on Sitecore typically ships ~40–60 components (Sitecore's catalogue tends toward larger component sets than headless competitors because the authoring surface needs more granularity). Build scope: 600–1,200 hours for foundations + components + JSS wrapping + rendering manifest + Pages templates.

### Contentful

The canonical headless CMS reference. Contentful has shaped the field's mental model of headless CMS authoring since the mid-2010s; the platform's structure is the field's default vocabulary.

**Architecture.** Spaces (the multi-tenant unit) and environments (master / staging / dev within a space) structure deployment. **Content types** define schemas (each field has a type, validations, appearance settings). **Entries** are instances. **Assets** handle media (images / video / files) with built-in CDN and image-transformation API. The **Content Delivery API** (CDA, REST + GraphQL) serves published content; the **Content Preview API** (CPA) serves draft content; the **Content Management API** (CMA) handles authoring operations.

**The DS-integration shape.** Components consume entries via the Delivery API; field types map to component props via a marshalling layer. Rich-text fields use the Rich Text Renderer (Contentful's React / JS rendering library) which maps document-tree nodes to React components. The DS engagement scopes:
- The component library (standard DS scope)
- The content-type schema (typically co-designed with the CMS team; per the boundary discussion at §5)
- The marshalling layer (typically ~40–80 hours; per content type)
- The rich-text rendering map (per project; couples DS's Heading / Paragraph / List components to Contentful's document nodes)

**Authoring reality.** Contentful's web app is schema-driven — authors fill forms whose shape matches the content type. There is **no preview-as-you-author out of the box**, though the Preview API plus a custom preview environment closes the gap (commonly via Vercel / Netlify preview deployments tied to entry IDs). The lack of native preview is the most-frequent client friction point in Contentful engagements; agency teams scope a preview-environment build as a discrete deliverable on most engagements.

**The CMS-vs-DS boundary.** Contentful is the cleanest separation in the field: Contentful owns content types, fields, and entries; the DS owns components, tokens, and rendering. The boundary is enforced by the platform — there is no Contentful-side templating language; every rendering decision is in the DS code. This makes Contentful the practice's default headless-CMS recommendation when the client's preference allows.

**MCP-readiness.** Contentful's GraphQL surface plus the Content Model API together expose both content-instance shape and content-type schema in API-shaped form. An MCP wrapper is straightforward: 16–24 hours to expose `list_content_types`, `get_content_type`, `query_entries`, `get_entry` to AI clients. Contentful is the practice's bet for first-mover on native MCP support among headless CMSes; verify against Contentful's roadmap quarterly.

### Sanity

The structured-content approach. Sanity's differentiator is **Studio** — a self-hosted, customisable authoring tool defined in TypeScript code rather than configured via web UI. The Studio is part of the project repo; schemas are TypeScript files; custom input components extend Studio's authoring forms; the Studio runs locally for authors or deploys to studio.sanity.build / sanity.studio for hosted use.

**Architecture.** Content is stored in **Sanity Content Lake** (Sanity's managed hosted backend). Querying via **GROQ** (Sanity's domain-specific query language; pronounced "groke") or GraphQL. **Portable Text** is Sanity's distinctive contribution: a JSON representation of rich-text content that's renderer-agnostic; per-block-type rendering is defined in code (a React component per block type — paragraph, heading, blockquote, custom — composes the rendered output).

**The DS-integration shape.** Similar to Contentful at the rendering side (components consume content via API; React components render entries) but with **Studio customisability** — the DS team can extend Studio to align with the DS's component patterns. Custom input fields render in Studio with the agency's design; preview panes show the rendered DS-component output alongside the authoring form. The DS engagement scopes:
- The component library (standard DS scope)
- The content schema (TypeScript files; co-designed; ~20–40 hours per content type)
- Studio customisation (the agency's distinctive Sanity contribution; ~80–160 hours for a substantive customisation)
- The Portable Text rendering map (per project; couples DS components to Portable Text block types)

**When Sanity wins over Contentful.** Sanity is the right choice when the engagement needs heavy content-model customisation, when the client's content team values authoring-UX over SaaS convenience, or when the agency wants to ship a distinctive Studio as part of the deliverable. Sanity is over-engineered for engagements with simple content models or for clients who prefer pure SaaS without code-based configuration.

**Practitioner reality.** Sanity engagements skew larger than Contentful engagements because of the Studio customisation work; build scope: 700–1,400 hours for foundations + components + Studio + Portable Text rendering. The premium pays back when the content team's authoring workflow is a significant business concern.

### Strapi

Open-source, self-hostable, plugin-extensible. The open-source default for engagements where SaaS is unacceptable: regulated industries (healthcare data sovereignty, financial services on-prem), clients with strict hosting-cost constraints, governments with on-prem mandates.

**Architecture.** Content types defined in admin UI or via code (Strapi v5's content-type builder generates TypeScript types from the UI schema; the schema is also editable as JSON). The API is REST or GraphQL (configurable per collection). The admin UI is the authoring surface (similar in scope to Contentful's web app but self-hosted). Plugin system extends both admin UI and API.

**Strapi v4 vs. v5.** v5 (late 2024 / early 2025) is a meaningful rewrite: improved performance, document-storage redesign, breaking changes from v4. Engagements should target v5 for new builds; v4 → v5 migration is non-trivial. Verify the version per project — some clients have invested in v4 plugins that need re-architecting for v5.

**The DS-integration shape.** Same as Contentful at the consumer side; the difference is operational. The agency or client team operates Strapi as infrastructure (Docker + Kubernetes / managed PostgreSQL / Redis cache / S3-compatible asset storage). The DS engagement scopes:
- The component library (standard DS scope)
- The content-type schema (TypeScript or JSON; co-designed)
- The API marshalling layer (similar to Contentful)
- The hosting / DevOps setup (typically out of scope for the DS engagement; in scope for the platform engagement)

**Authoring reality.** Similar to Contentful — schema-driven, no native preview-as-you-author. Custom preview environments are built the same way. Strapi's plugin ecosystem can extend the admin UI more aggressively than Contentful's web app allows, but requires React engineering investment.

**Practitioner reality.** Strapi engagements scope similarly to Contentful but with hosting / DevOps overhead. Build scope: 600–1,200 hours for the DS-side work; platform scope adds 200–400 hours for the Strapi setup and operations.

### Storyblok

The visual-editor + headless-API combination. Storyblok's distinctive feature: a **visual editor** that previews the rendered site as authors edit (via the storyblok-react / storyblok-vue / storyblok-svelte SDK rendering the components in an iframe on the storyblok.com authoring surface). This bridges the WYSIWYG-vs-headless gap that Contentful and Sanity don't address natively.

**Architecture.** Content is stored in Storyblok's managed backend. Querying via Storyblok's Content Delivery API (REST). The **storyblok-bridge** library injects the editor's preview pane with the live front-end render; authors see the rendered DS components in the iframe; clicking a component in the iframe selects it for editing in the right pane.

**The DS-integration shape.** Components are React / Vue / Svelte; Storyblok's "blocks" (content types) map to components; the SDK renders the components via a `StoryblokComponent` registry. The DS engagement scopes:
- The component library (standard DS scope)
- The block schemas (Storyblok's content types; typically authored in Storyblok's web app but exportable as JSON)
- The component registry (the marshalling layer mapping block types to DS components)
- The preview integration (the storyblok-bridge wiring; usually straightforward)

**When Storyblok wins.** Engagements where the content team is migrating from WordPress / WYSIWYG and needs preview-as-you-author. Engagements where the marketing team is the primary author surface and visual fidelity-during-editing is non-negotiable. Storyblok's preview is sandbox-shaped (renders in iframe); complex page-level interactions (multi-step flows, persistent state across navigations) are harder to preview faithfully; verify per project.

**Practitioner reality.** Storyblok engagements scope similarly to Contentful at the DS side; the preview-as-you-author benefit reduces the per-engagement preview-environment work that Contentful engagements typically require. Build scope: 500–1,000 hours for the DS-side work.

### The five-platform decision tree

| Decision driver | Recommendation |
|---|---|
| Sitecore portfolio investment | Sitecore XM Cloud |
| SaaS-first; English-only or simple-locale | Contentful |
| Bespoke content models; custom Studio | Sanity |
| On-prem / regulated / cost-constrained | Strapi |
| Content team needs preview-as-you-author | Storyblok |
| First-mover on native MCP support (anticipated) | Contentful |
| Multi-CMS portfolio (composable) | Multiple platforms per service |

None of these is the practice's "default headless CMS" — the platform choice is engagement-specific. The discipline: ask the decision-driver questions at scoping; recommend per the answers; flag the trade-offs honestly.

---

## 3. WordPress as DS host

### The reality

WordPress is still a real engagement type at the agency, despite headless / composable narrative pressure. Two procurement shapes: **block-theme builds** (the modern WordPress direction since 5.9 / FSE / theme.json) and **headless-WordPress builds** (REST + WPGraphQL serving content to a separate React / Next.js front-end). The two shapes scope and price differently; the agency should articulate them as distinct engagement types.

### Block themes and Full Site Editing

WordPress 5.9 (Jan 2022) introduced FSE; 6.0–6.4 matured it; 6.5+ added pattern-based templates and the Site Editor's interactivity API; by mid-2026, FSE / block themes is the recommended path for new theme work. Classic themes (PHP-templating-based) remain supported but are increasingly limited.

**theme.json — WordPress's design tokens surface.** The `theme.json` file at the root of a block theme defines:
- `settings.color.palette` — color tokens
- `settings.color.gradients` — gradient tokens
- `settings.typography.fontSizes` and `.fontFamilies` — typography tokens
- `settings.spacing.spacingSizes` — spacing tokens
- `settings.layout.contentSize` and `.wideSize` — layout tokens
- `styles` — element-level and block-level style tokens

This is directly analogous to design tokens in the DS sense. Style Dictionary can target theme.json with a custom transform (the practitioner-side wrapping work; typically 8–16 hours); tokens flow to the editor and to the rendered front-end automatically. The block editor reads theme.json to populate the color picker, font-size dropdown, spacing controls, etc.

**Block patterns and block templates.** Block patterns are reusable composed-content blocks (e.g., a "Hero with CTA" pattern); analogous to AEM Experience Fragments. Block templates define page structures (e.g., the `single.html` template defines the single-post layout); analogous to AEM Editable Templates. Both are governed by the theme.

**The DS-integration shape for block-theme engagements.**
- Tokens map to theme.json (Style Dictionary transform or hand-authored)
- Custom blocks are React components registered via `block.json` and the Block API (`@wordpress/blocks`)
- The editor renders blocks via `@wordpress/block-editor`
- Server-side rendering uses PHP `render_callback` per block (or the `save` function for static blocks)
- Block patterns ship as part of the theme

The practice's bridge investment: a Style Dictionary transform that emits theme.json from the DS's source-of-truth tokens; this becomes a reusable practitioner asset across WordPress engagements.

### Custom blocks (Gutenberg blocks) as the component primitive

Each block is a React component (in the editor) plus a save function (rendered output) plus block.json (metadata). The Block API supports two registration paths:

**Native Block API.** The full path — JavaScript registration via `registerBlockType`; React component for the editor; save function or `render_callback` for the front-end. Higher engineering investment (React fluency required); higher fidelity (preview-as-you-author works exactly as designed).

**ACF Blocks (Advanced Custom Fields).** A common workaround for clients without React engineering. ACF Blocks register via PHP; the editor renders via PHP-shaped previews (lower fidelity but no React required); fields are configured via ACF's admin UI; render_callback handles output.

**The trade-off.** ACF Blocks are easier to ship but degrade preview fidelity — authors see a server-side-rendered preview that may not match the final output. Native Block API requires React investment but gives full editor fidelity. The practice's discipline: native Block API for engagements with engineering depth; ACF Blocks for engagements where the client's content team will maintain the blocks long-term without React skills.

### The DS-vs-block-pattern boundary

Block patterns are reusable layout compositions; design-system components are reusable primitives. Where DS-component library ends and block-pattern library begins is a procurement-grade decision.

The practice's working position: **DS components ship as Gutenberg blocks (the primitives); block patterns are *compositions of DS components* (the layouts) and ship as part of the theme rather than the DS.** This separation maps onto the broader CMS-vs-DS boundary at §5 — components are structure (DS); compositions are content-shaped layouts (theme / CMS).

A "Hero" component (a DS primitive) is a block. A "Hero with CTA above three feature cards" pattern (a layout composition) is a block pattern. Both ship from the theme; the DS owns the primitives; the theme owns the patterns. When the agency builds both, the DS team owns the blocks and a content-strategist or designer collaborates on the patterns.

### Headless WordPress

REST API + **WPGraphQL** (the canonical GraphQL extension; ~2.0 stable as of mid-2026; the de facto standard for headless WP). Content types and ACF fields surface via the API; a separate Next.js / Remix front-end consumes them; preview is custom (typically via Vercel preview deployments tied to draft post IDs and a preview-mode toggle).

**Architecture choices.** **Faust.js** (WP Engine's headless-WordPress framework) is the most opinionated choice — provides preview infrastructure, authentication, and pre-built Next.js components. **WPGraphQL + Next.js bare** is the more flexible choice — agency builds the integration from scratch. **Headless React / WordPress.com's headless toolchain** is a third option for clients on WordPress.com.

**The DS-integration shape.** Same as Contentful / Sanity at the consumer side; WordPress's authoring surface is the trade-off. The WP admin UI is functional but not optimised for headless-CMS use — it shows preview-mode states, custom-field UIs that the headless front-end doesn't render in the admin's preview pane, and a general impedance mismatch between "WordPress as CMS" and "WordPress as headless content service." Some agencies pair headless WP with a custom admin theme that hides the WordPress-classic UI elements that confuse content teams in a headless context.

### The two shapes price differently

| Engagement shape | Build scope | Notes |
|---|---|---|
| Block-theme build (DS + theme + custom blocks + block patterns) | ~250–500 hours | Scopes similarly to AEM-light engagements; tight coupling to WP's editor environment; preview-as-you-author native via FSE |
| Headless WordPress (DS + components + Next.js front-end + WPGraphQL integration + custom preview) | ~300–600 hours | Scopes similarly to Contentful / Sanity engagements; loose coupling; custom preview infrastructure required |

The procurement shape determines the team composition (block-theme needs WP-PHP fluency alongside React; headless WP can be React-only with WP set up by a separate team) and the delivery model (block-theme ships into the WP install; headless WP ships a separate front-end with a content-API contract).

---

## 4. Salesforce Commerce Cloud Page Designer

### The context

Per 00b §Active engagement examples — the New Balance engagement is on Salesforce Commerce Cloud (SFCC), with **Chakra UI** as the consuming front-end framework. The engagement built a Figma library for the Australian site launch (tied to Australian Open) which the client dev team built from. The current question is scaling the Australian work across other regions, with potential platform considerations including migration to SFCC if not already there.

This section addresses the Salesforce-specific authoring surface — **Page Designer** — and its relationship to SFCC's broader architecture stack.

### The SFCC platform stack

Three layers, evolving over the platform's history:

**Storefront Reference Architecture (SFRA).** The older, server-rendered shape. Based on Mustache templates (`.isml` files) and the SiteGenesis cartridge model. Cartridges are SFCC's deployment unit; the controller layer handles request routing; the model layer accesses the data API; the view layer renders ISML. Still in widespread use across SFCC's installed base; the cartridge model is the platform's foundation.

**Page Designer.** Salesforce's drag-and-drop component-composition authoring surface. Layered on top of SFRA (Page Designer pages are rendered by SFRA's controllers); gives content authors the ability to compose pages from pre-defined components without engineering involvement. Released ~2018, matured through 2020–2024; mid-2026 is stable but not the platform's flagship direction.

**Headless Commerce / PWA Kit / Composable Storefront.** The modern direction since ~2022. PWA Kit is Salesforce's React-based front-end framework that consumes the **B2C Commerce APIs** (REST + GraphQL surfaces over the legacy SFRA models). Composable Storefront ships as a Next.js / PWA Kit hybrid for greenfield engagements. Page Designer's role in the headless path is reduced — the React front-end can render Page Designer pages but the visual editor's preview fidelity drops because the editor is SFRA-coupled.

### Page Designer's component model

The authoring surface uses three concepts:

**Page types** — the top-level composable surface. Standard page types ship out of the box: `Storefront Page` (catch-all), `Category Page`, `Product Page`, `Article Page`, `Search Results Page`. Custom page types are defined in JSON metadata; they declare which regions exist and which components are allowed in each region.

**Regions** — the slot-shapes within a page type. A page type might declare regions like `Header`, `HeroBanner`, `Body`, `Footer`. Each region has a name, an ID, and rules about which components can drop into it (typed by component category — `Hero`, `Card`, `Slot`, etc.).

**Components** — the building blocks authors drop into regions. Each component is defined by:
- A **component definition file** (JSON metadata declaring the component's name, description, region-compatibility, configuration schema)
- A **render template** (ISML for SFRA path; React for PWA Kit / headless path)
- A **configuration schema** that drives the authoring form (what authors can customise per instance — text, images, links, color choices, layout options)

The DS-integration shape: **DS components are wrapped as Page Designer components via the component definition file plus the render template.** The configuration schema maps to component props; the rendered output is HTML (SFRA path) or React (PWA Kit / headless path).

### The relationship to SFRA and Headless Commerce

**Pure SFRA engagements.** Page Designer + ISML templates + SFRA cartridges. Server-rendered; preview-as-you-author works through Page Designer's Salesforce-hosted editor. The DS engagement scopes the cartridge wrapping work (~30–50% of build hours) alongside the standard component-library work.

**Pure headless / PWA Kit engagements.** B2C Commerce APIs + React (PWA Kit or custom Next.js) + Chakra UI or bespoke DS. Page Designer authoring may or may not be in scope — many headless engagements bypass Page Designer entirely and use a separate CMS (Contentful / Sanity / Storyblok) for editorial content while Salesforce handles product/commerce data only. The DS engagement looks like a Contentful / Sanity engagement at the consumer side.

**Hybrid SFRA + Page Designer + PWA Kit engagements.** The most-common shape for SFCC engagements with multi-region scaling needs (per the New Balance pattern). SFRA handles legacy pages and product / category / cart flows; Page Designer handles marketing / editorial pages; PWA Kit (or a custom React front-end) handles the modernised customer-facing UI. The DS supports all three surfaces.

### Chakra UI as the New Balance choice

Chakra UI is a React component library with strong accessibility and theming support; selected by many SFCC engagements as the "DS in a box" starting point. The DS-integration question for the New Balance engagement: **how does the agency-built DS layer relate to Chakra?**

Two patterns:

**Pattern A: Extend Chakra with the agency's tokens via Chakra's theme system (lightweight).** Chakra's theme is JSON-shaped; the agency's design tokens map onto Chakra's theme structure (`colors`, `space`, `fontSizes`, etc.). Components consume Chakra primitives styled with the agency's tokens. Build scope: 200–400 hours for the theme + per-component customisation.

**Pattern B: Replace Chakra with a bespoke DS that wraps Chakra's headless primitives (heavier but more controlled).** Use `@chakra-ui/react` as the headless behavioural layer (per 33 §4's headless-vs-opinionated split); build the visual layer from scratch with the agency's design language. Build scope: 600–1,000 hours.

The choice depends on the agency's commercial model and the client's longer-term maintenance plan. Pattern A is cheaper and faster but locks the engagement to Chakra's evolution; Pattern B is more expensive but produces a DS the client can maintain independently of Chakra's release cycle.

### Salesforce-specific authoring patterns

Page Designer's visual editor is **Salesforce-hosted** (no equivalent to Storyblok's iframe-preview customisation). The editor's component palette is determined by the component definitions registered in the cartridge; the configuration schemas drive the authoring forms authors fill in per instance.

**The implications.** The DS team scopes the component definitions, the configuration schemas, and the render templates as discrete deliverables. Each component requires:
- A component definition file (5–10 hours per component for a simple component; 15–25 for complex)
- A configuration schema (~3–8 hours per component depending on author-configurable surface)
- An ISML or React render template (~4–10 hours per component)
- Per-region compatibility metadata (~1–2 hours per component)

Total per-component overhead beyond the standard DS-component work: 13–45 hours per component. For a 30-component DS shipping to Page Designer, that's 400–1,400 additional hours of SFCC-specific wrapping — a meaningful scope that the practice should make visible in proposals.

### The scope of the Salesforce engagement

| Engagement shape | Build scope |
|---|---|
| Greenfield SFCC + DS + Page Designer + headless front-end with Chakra UI (Pattern A) | ~500–800 hours |
| Greenfield SFCC + DS + Page Designer + bespoke DS wrapping Chakra primitives (Pattern B) | ~900–1,400 hours |
| Migration / scaling engagement (per New Balance: existing DS, scale to new regions) | ~250–500 hours per region (per-region adaptation + Page Designer component coverage extension + per-region content modelling) |

The complication 00b flags about platform migration. If the client is on legacy commerce architecture (e.g., a custom platform pre-dating SFCC) and the regional scaling triggers a platform decision, the SFCC platform migration itself is a $10–50M-range decision the DS engagement layers on top of — typically with a separate platform-implementation team (Salesforce-certified partner) handling the SFCC build while the agency handles the DS layer. The DS engagement should not absorb platform-migration scope; the practice's discipline is to scope the DS work explicitly against the chosen platform and flag platform decisions as parallel engagements.

---

## 5. The CMS-vs-DS authoring boundary

### The procurement-grade decision

Per 09 §1.32 — *"where component anatomy lives in CMS schema vs. system schema; how the two source-of-truth claims reconcile; how Code Connect or `.ai.json` schemas align with CMS content models."* This is the question the practice ships against without an articulated POV. This section closes the gap.

### The boundary the existing material articulates

Per 04 §Content as a system layer — *"tokens for templated, system-level content; CMS for editorial, product-specific content."* The line is articulable at the *content* layer; this section extends it to the *component-anatomy* layer.

### The component-anatomy boundary

The DS owns component **structure** — the props the component accepts, the states it renders, the slots it composes. The CMS owns content **instances** — the specific values authors fill in per instance. The line is the same as design-tokens-vs-component-styles: structure in the DS; instance-level overrides in the CMS.

A worked example. A Hero component has:
- A heading (text) — props field `heading`
- A subheading (text) — props field `subheading`
- A primary CTA (button label + URL) — props fields `ctaLabel` and `ctaUrl`
- An optional secondary CTA — props fields `secondaryCtaLabel` and `secondaryCtaUrl`
- A background image (URL) — props field `backgroundImage`
- A layout variant — props field `variant: "left-aligned" | "centered" | "right-aligned"`

The DS owns: the props' shape (their names, types, validation rules), the component's render logic (how the variants render visually), the component's states (loading, error, empty), the component's a11y contract (the heading semantics, the CTA's keyboard model, the alt text requirement on the background image).

The CMS owns: the per-instance values (the specific heading text on the homepage's hero; the specific CTA label; the specific background image asset reference). The CMS schema (the content type definition) has fields that *match* the component's props; the DS-CMS contract is the field-to-prop mapping.

### The Code Connect / `.ai.json` parallel

Per 30 — Code Connect binds Figma components to code components; `.ai.json` exposes the structured AI-readable surface. For CMS-managed components, the AI-readability registry has to source from *both* the DS code surface (for component structure) and the CMS schema (for content-instance shape).

The shape this implies for `.ai.json`:

```json
{
  "component": "Hero",
  "structure": {
    "source": "ds-code",
    "props": [
      { "name": "heading", "type": "string", "required": true },
      { "name": "subheading", "type": "string", "required": false },
      { "name": "ctaLabel", "type": "string", "required": true },
      { "name": "ctaUrl", "type": "url", "required": true },
      { "name": "backgroundImage", "type": "asset-url", "required": true },
      { "name": "variant", "type": "enum", "values": ["left-aligned", "centered", "right-aligned"], "default": "left-aligned" }
    ]
  },
  "instances": {
    "source": "cms",
    "platform": "contentful",
    "contentType": "Hero",
    "fieldMapping": {
      "heading": "heading",
      "subheading": "subheading",
      "ctaLabel": "primaryCtaLabel",
      "ctaUrl": "primaryCtaUrl",
      "backgroundImage": "backgroundImage.fields.file.url",
      "variant": "layoutVariant"
    }
  }
}
```

The structured surface lets AI clients reason about *what components exist* (DS) AND *what content fills them per instance* (CMS). The seven-tool conceptual surface from 15 (`list_components`, `get_component`, `search_components`, `get_token_catalog`, `get_composition_rules`, `get_usage_guidelines`, `validate_implementation`) extends to CMS-managed components with additional tools: `list_content_types`, `get_content_type`, `query_entries`, `get_entry`. The combined surface lets AI clients reason about the full DS-CMS pairing.

The practice's bet: this is custom middleware work today; native CMS-vendor MCP support lands in 2026–2027 (per §6 below). Until then, the bridge investment is per-engagement (16–40 hours per CMS for the MCP wrapping; per §6).

### The boundary table (synthesis-ready artefact)

| Content type | Lives where | Notes |
|---|---|---|
| **Component structure** (props, states, slots) | DS | The DS code defines the contract; the CMS conforms to it |
| **Component variants** (visual / behavioural) | DS (with CMS surface for author selection per instance) | Variants are DS structure; per-instance variant *choice* is CMS-driven via the variant prop |
| **Templated content** (CTA verbs, error messages, empty states) | DS content tokens (per 04) | Per 04 §Content as a system layer's content-token catalogue |
| **Editorial content** (copy, images, marketing assets) | CMS | The CMS's primary purpose |
| **Per-instance content** (this Hero's headline; this CTA's label) | CMS | Authored per instance via the CMS's content-type form |
| **Layout composition** (page-level structure) | CMS (with DS components as composable units) | Page templates / block patterns / Page Designer page types live in CMS; they compose DS components |
| **Localisation variants** | CMS (for editorial); content-token catalogue (per 04) for templated | The 04 boundary applied per-locale |
| **Component anatomy decisions** (what props exist, what states are valid) | DS | Schema changes to component anatomy require DS-team review; CMS adjusts to match |
| **Content-type schema decisions** (what fields a content type has) | CMS team (with DS-team consultation) | Schema changes to content types require CMS-team ownership; DS provides the field-to-prop mapping |

### Scoping implications

The boundary determines who owns what at the instance level. The practice's discipline: **name the boundary in the SOW**. Without explicit naming, the boundary drifts during the engagement — typically toward CMS-instance-as-presentation, which collapses the DS's structural authority.

Three concrete failure modes the practice has lived through:

**The CMS-instance-as-style-override failure.** Authors get the ability to override individual component styles per instance (font size, color, spacing) via CMS configuration fields. The boundary collapses; the DS's design tokens become advisory rather than enforced; visual fragmentation accumulates across instances by release.

**The CMS-as-component-author failure.** Content team starts authoring new component types in the CMS without DS-team review; the new types replicate existing DS components with slight modifications; the catalogue of "what components exist" splits between DS code and CMS content-type definitions. The CMS-vs-DS-authoring-boundary collapses entirely.

**The DS-as-content-store failure.** DS team starts hardcoding content into components ("Welcome to our site!" embedded in a HomepageHero component); the boundary collapses in the other direction; content updates require DS code releases rather than CMS authoring.

Naming the boundary at scoping prevents all three. The boundary is reviewed at major release boundaries to ensure it's still where the practice put it.

---

## 6. MCP / AI-readability for CMS-managed components

### The case

Per 30 §MCP and 34 §5 — the AI-readability registry exposes structured component contracts to AI clients. When components are authored *and stored* in the CMS, the `.ai.json` registry must source from the CMS too. This is a natural extension of 30's pipeline; not yet articulated for CMS-managed components.

### Per-CMS feasibility assessment

| CMS | API surface | MCP-wrapping effort | Native MCP timeline (practice bet) |
|---|---|---|---|
| **Contentful** | GraphQL Delivery API + Content Model API; both API-shaped | 16–24 hours; relatively low-effort wrapping | First mover; likely 2026–2027 |
| **Sanity** | GROQ + GraphQL; Studio schema in TypeScript (AI-parseable) | 16–24 hours; straightforward | Early mover; likely 2026–2027 |
| **Strapi** | REST + GraphQL with admin-API; self-hosted | 20–32 hours; agency can ship MCP wrapper alongside Strapi deployment | Open-source community-driven; uncertain timeline |
| **Sitecore XM Cloud** | Edge GraphQL + JSS rendering manifest | 24–40 hours; rendering-manifest is partial Code Connect equivalent | 2027–2028 (Sitecore's commercial pressure on AI-readiness exists but velocity is lower) |
| **WordPress** | WPGraphQL or REST; Faust.js framework | 24–40 hours; Faust.js may eventually ship MCP support | 2027+ (open-source; depends on WPGraphQL maintainer + Faust.js direction) |
| **Storyblok** | Content Delivery API (REST) | 20–32 hours | Likely 2027 (Storyblok has public AI-readiness roadmap) |
| **AEM** | Sling Model Exporter (.model.json) | 32–60 hours; non-trivial because JCR content tree is genuinely different from flat content-model API | 2027+ (Adobe's MCP investment is uncertain; roadmap not public as of mid-2026) |
| **Salesforce Commerce Cloud / Page Designer** | B2C Commerce APIs (REST + GraphQL) | 32–60 hours; vendor-specific surfaces | 2028+ (typically out of scope for SFCC engagements due to platform vendor-lock-in concerns) |

### The bet

CMS-vendor-native MCP support lands in 2026–2027 alongside the design-token-vendor MCP per 34 §5. **Contentful and Sanity are the most likely first movers** — their AI-readiness pressure is most direct (their content surfaces are already AI-shaped via GraphQL); their APIs are closest to MCP shape. Strapi may follow via the open-source community. Storyblok has signalled AI direction publicly. Sitecore, WordPress, AEM, and SFCC are likely 2027–2028 timeframe; AEM and SFCC may be later because their architectural shapes (JCR for AEM; cartridge model for SFCC) require more wrapping work than the headless competitors.

The practice's recent capture of Supernova's mid-2026 MCP-shipping (per the housekeeping pass: Supernova ships MCP-endpoint distribution in private beta) is signal that vendor-native MCP is closer than the file initially anticipated. Verify quarterly across all eight platforms.

### The practice's bridge investment

Custom MCP wrappers per CMS, per engagement. The wrapper exposes:
- Content-type schema (per CMS — the content-model surface)
- Content-instance retrieval (per CMS — the entry / page / block retrieval surface)
- DS-component contract (joined from the DS code side)

Typical scope per CMS: 16–60 hours depending on the platform's API shape and the wrapping work the platform requires. Amortises across engagements that ship to the same CMS — a Contentful MCP wrapper built for one engagement is reusable across the practice's Contentful portfolio; an AEM MCP wrapper is reusable across the practice's AEM portfolio (the larger surface).

The seven-tool conceptual surface from 15 extends to CMS-managed components with additional tools:
- `list_content_types` — lists the CMS's content-type catalogue
- `get_content_type` — returns the schema for a specific content type
- `query_entries` — returns content instances matching filters
- `get_entry` — returns a specific content instance with all field values

Combined with the DS-side tools (`list_components`, `get_component`, etc.), the AI client can reason about the full DS-CMS pairing — what components exist, what their structure is, what content types map to them, what instances exist, what values fill the instances.

### The CMS-as-DS-source pattern (failure mode worth naming)

A specific case the practice should articulate: when the CMS itself is the authoring surface for the DS's component structure (rare but real — some engagements ship a "headless DS" where the components are authored as content types in the CMS rather than as code).

This is the extreme case of CMS-vs-DS-authoring-boundary collapse. The DS's component anatomy lives in the CMS as content-type schemas; the rendering layer is generic (typically a single React component that switches on content-type to render appropriate output); the design-system code is thin to the point of being absent.

**The practice's position: typically not appropriate.** The CMS-as-DS-source pattern is appropriate only for **thin presentation-layer DSes** where:
- The component set is small and stable (under 10 components)
- A non-engineering team needs to author components without a code release
- The engineering investment required to ship a "real" DS is unjustified

Outside those conditions, the pattern collapses the DS's structural authority, makes the AI-readability layer harder to ship cleanly (because the component contract is in the CMS rather than in code), and produces engagements where the "design system" is effectively a CMS configuration — not what the practice's commercial offering claims to deliver.

When the practice encounters a client who has built (or wants to build) a CMS-as-DS-source pattern, the discipline is to name it explicitly: *"This is a CMS-shaped pattern, not a design system. We can work with it; we cannot call it a design system without misrepresenting what we're delivering. The boundaries the practice's broader DS work assumes — structural authority in code, instance authority in CMS — are collapsed here. If you want a design system in the practice's sense, the architecture has to change."*

---

## 7. Composable-content patterns

### The 2025–2026 movement

Content-as-data with explicit schemas; sometimes called "headless DS-as-content-source" or "composable DXP." The integration story changes: content is not a single CMS's output but a *composed* artefact pulled from multiple services (CMS + PIM + DAM + commerce + personalization) via a unified content layer.

Vendors in this space:
- **Uniform** — composable orchestration; pulls from headless CMSes, commerce, personalization, search; provides a unified content-delivery layer
- **Layer0** — composable edge infrastructure; focuses on the rendering and caching layer of composable architectures
- **Vercel's content-platform direction** — the Next.js + V0 + Vercel-native composable stack; uses Edge Functions and Vercel KV / Postgres / Blob as the orchestration substrate
- **Storyblok's composable direction** — Storyblok has pivoted from pure headless to composable-aware orchestration; the Storyblok Edge surface composes from Storyblok content + integrated services

The composable-DXP layer is mid-maturity as of mid-2026 — the architectural shape is established; the off-the-shelf orchestration tooling is improving but still requires significant custom integration per engagement. The practice's bet: composable orchestration matures by 2027–2028 alongside CMS-vendor MCP support; until then, composable engagements ship with custom orchestration as part of the build scope.

### What "composable" means architecturally

Content types are defined per service:
- **Editorial content** in a headless CMS (Contentful / Sanity)
- **Product data** in a commerce platform (Shopify / Salesforce Commerce / commercetools)
- **Marketing assets** in a DAM (Cloudinary / Bynder)
- **Search results** in a search service (Algolia / Elasticsearch)
- **Personalization decisions** in a personalization platform (Sitecore Personalize / Optimizely / Adobe Target)

The orchestration layer pulls from each service per request and composes the rendered output. The DS sits at the rendering layer, consuming the orchestrated content stream rather than a single CMS's output. The DS-component contract is the same; the integration is per-service.

### Schema-first authoring

Each service in the composable stack defines its own schema; the orchestration layer reconciles. The DS's component contract is the **common vocabulary** across the stack — components are the consumers of all services' content; the DS's schema defines what each component expects regardless of which service supplies the content.

A worked example. A ProductCard component in a composable architecture might consume:
- Product name, price, image, SKU — from the commerce platform
- Marketing copy, lifestyle imagery, brand story — from the headless CMS
- Personalized recommendation rationale — from the personalization platform
- Search-relevance score — from the search service (when the card appears in search results)

The DS defines the ProductCard's props (the component's expected input shape); the orchestration layer queries each service per request and assembles the props' values; the DS renders the assembled values. The component contract is service-agnostic; the integration is per-service.

### Composition-at-render

The orchestration layer composes the content per request; the DS components render the composition; preview-as-you-author becomes a multi-service preview problem (each service's draft state has to be reconciled at preview time).

This is the hardest UX problem composable architectures face. Single-service preview is straightforward (one CMS's draft state renders against the live front-end). Multi-service preview requires:
- Per-service preview tokens / draft modes
- An orchestration-layer preview switch that respects per-service preview state
- A preview infrastructure that can render the composed output with mixed live + draft states
- A preview UX that signals to authors *which service contributed which content* in a given render

Most composable engagements as of mid-2026 ship with limited multi-service preview — typically a "preview with the current CMS in draft mode but other services in live mode" approximation. Full multi-service preview is custom infrastructure (typically 80–160 hours of preview-environment build) that engagements scope explicitly.

### The variability-by-design problem applied to content

Per 04 §AI-surface enforcement (and 26's residual gap on variability-by-design tooling) — the variability-by-design problem applies at the composable layer too. The author specifies a *space* of possible content compositions; the orchestration layer pulls from each service; the rendered output is one realisation of that space. The practice's discipline: composable content benefits from the same variant-logging / eval-driven QA pattern that 27 names for adaptive UI; per-render variance is bounded by the schema contract.

The pattern that fails: composable content composes free-form across services; the orchestration layer's logic is opaque to authors; per-render output is unpredictable; brand consistency degrades across renders. The pattern that works: the schema contract bounds the composition (each service supplies content matching the DS component's props' types); the orchestration layer's logic is documented; variant-logging captures what the authors and what the orchestration produces; eval-driven QA validates the rendered compositions against the brand and content guidelines.

### The boundary between content tokens and composable content

Per 04 §Content as a system layer — content tokens are templated content the DS owns; composable content is editorial content the orchestration layer composes. Both treat content as data; the difference is the authoring surface (DS catalogue for tokens; CMS / PIM / DAM for composable content). The two coexist in composable architectures: tokens for system-level microcopy, composable content for editorial / product / marketing.

A worked example in a composable e-commerce architecture:
- The "Add to cart" button label — DS content token (system-level; consistent across products and locales)
- The error message when the cart fails to update — DS content token
- The product name — composable content (from the commerce platform)
- The product description — composable content (from the headless CMS)
- The marketing banner above the cart — composable content (from the headless CMS, possibly personalized)
- The personalized recommendation rationale — composable content (from the personalization platform)

Both layers ship; the DS's content-token catalogue handles system-level templated content; the composable architecture handles editorial / product / marketing content. The boundary is the same as content-tokens-vs-CMS at §5 and at 04 §Content as a system layer — system-level vs. editorial / instance-level.

### Practitioner-side scoping

Composable engagements are the most architecturally complex of the four shapes. Scope ~1.5–2× a comparable headless engagement because the integration surface multiplies (each service is a separate integration); the orchestration layer is custom (typically; off-the-shelf orchestration is starting to ship from Uniform / Vercel but not yet mature).

For agency clients on composable platforms, the DS engagement typically lands as one of multiple parallel engagements (DS + commerce + content + personalization), each with its own discipline. The DS engagement scopes:
- The component library (standard DS scope)
- The DS-component contract (the common vocabulary that all services map onto)
- The orchestration-layer integration (typically custom; ~120–250 hours)
- The preview infrastructure (typically custom; ~80–160 hours)
- The variant-logging / eval-driven QA infrastructure (per 04 / 27; ~40–80 hours)

Total composable DS engagement scope: ~800–1,500 hours for a moderate-complexity engagement; ~1,500–2,500 for an enterprise composable platform with substantial integration surface. The premium pays back when the client's content / commerce / marketing surfaces are sufficiently complex that composable architecture is justified; for clients with simpler needs, headless or hybrid is the lower-cost / lower-risk path.

---

## 8. Integration — deepen 10, See also block

### The slot decision committed in this run

The synthesis path is **deepen 10, not a new file.** The structural plan:

**One new framing-altitude H2** lands near the top of 10 (between §Central problem and §AEM Architecture Fundamentals). The H2 covers §1 above — the four CMS architectural shapes as a decision tree, with the eight-platform comparison table. This H2 surfaces the mental model the reader navigates the existing platform-specific material with.

**New platform and concept H2 sections append after §Drupal but before §DS Delivery Model: NPM Package vs. Embedded.** Sections in order:
- **Headless CMS coverage — Sitecore XM Cloud / Contentful / Sanity / Strapi / Storyblok** (covers §2)
- **WordPress — block themes and headless** (covers §3)
- **Salesforce Commerce Cloud Page Designer** (covers §4)
- **The CMS-vs-DS authoring boundary** (covers §5)
- **MCP / AI-readability for CMS-managed components** (covers §6)
- **Composable-content patterns** (covers §7)

The cross-cutting **§DS Delivery Model: NPM Package vs. Embedded** section continues to apply across all platforms after the new sections. The principle generalises — embedded for tightly-coupled platforms (AEM, Drupal, WordPress block themes, Salesforce Page Designer SFRA path); NPM package for headless / composable platforms (Contentful, Sanity, Strapi, Sitecore XM Cloud, Storyblok, headless WordPress, Salesforce PWA Kit, composable architectures).

The existing **§AEM** and **§Drupal** sections stay intact at their current positions; the new framing H2 at the top makes their place in the four-axis taxonomy explicit (both under "traditional").

The section additions push 10 from ~5,000 words / 321 lines to roughly ~12,000 words / 700+ lines. Substantial growth; the file's load-bearing surface expands from "AEM with Drupal comparison" to "CMS landscape with depth on AEM, Drupal, headless platforms, hybrid platforms, composable patterns, the boundary discipline, and the AI-readability layer."

### See also block updates (in the new sections)

- **03** (the component-library altitude that consumes whichever CMS supplies content)
- **04 §Content as a system layer** (the content-token-vs-CMS boundary that this run extends to component anatomy)
- **30** (the AI-readability pipeline; the MCP-server-tooling reality that §6 extends to CMS-managed components)
- **33** (white-label engagements often ship to multiple CMSes in the reseller's stack; the per-reseller MCP shape per 33 §7 generalises)
- **34** (the workstation MCP stack reads CMS surfaces alongside Figma / Storybook)
- **24** (multi-brand token architectures often ship to multi-CMS portfolios; the cross-brand drift problem per 24 §Cross-brand drift parallels the cross-CMS drift problem composable architectures face)
- **13** (i18n content lives in CMS for editorial; in content tokens for system-level)
- **17 / 28** (a11y annotations carry through to CMS-rendered components; the CMS layer must not drop the annotation contract)
- **00b §Active engagement examples** (the New Balance SFCC engagement is the practice's primary Page Designer / Chakra UI reference)

### The open residual

The four-axis framing (traditional / hybrid / headless / composable) may evolve as the field shifts. Track quarterly; if a fifth shape emerges (e.g., **AI-native CMS** where content is *generated* rather than authored — early signals from Vercel's V0 and similar tools point this direction), the practice's framing extends.

This is a standing watch (analogous to the §1.27 watches) rather than a one-time gap — the field's evolution determines whether a fifth shape lands.

---

## References

The CMS landscape literature is fragmented across vendor docs, practitioner blogs, and analyst reports. References below organised by section.

### Architectural framing (§1)

- **Real Story Group's CMS landscape analysis** — `realstorygroup.com`. Annual reports on the headless / composable / traditional landscape.
- **Forrester Wave: Headless CMS** — annual Forrester analyst report. Behind paywall but worth the practice's reference if available.
- **Gartner Magic Quadrant for Digital Experience Platforms** — annual Gartner report. Behind paywall.
- **Jamstack.org documentation** — `jamstack.org`. The architectural-pattern documentation that defined "headless" as a category.

### Headless CMS platforms (§2)

- **Sitecore XM Cloud documentation** — `doc.sitecore.com/xmc`. Edge GraphQL API reference; JSS SDK documentation; rendering-manifest reference.
- **Contentful documentation** — `contentful.com/developers/docs`. Content Delivery API; Content Management API; Rich Text Renderer.
- **Sanity documentation** — `sanity.io/docs`. GROQ reference; Studio customisation; Portable Text reference.
- **Strapi documentation** — `docs.strapi.io`. v5 reference; plugin API; admin UI customisation.
- **Storyblok documentation** — `storyblok.com/docs`. Visual editor SDK; storyblok-react reference; bridge library reference.

### WordPress (§3)

- **WordPress documentation: theme.json** — `developer.wordpress.org/themes/global-settings-and-styles/`. The canonical theme.json reference.
- **Block API documentation** — `developer.wordpress.org/block-editor/reference-guides/block-api/`. Block registration; block.json reference.
- **WPGraphQL documentation** — `wpgraphql.com`. GraphQL extension reference; resolver patterns.
- **Faust.js documentation** — `faustjs.org`. Headless WordPress framework reference.
- **WP Engine's headless WordPress documentation** — `wpengine.com/headless-wordpress`. Platform-vendor-specific guidance.

### Salesforce Commerce Cloud (§4)

- **Salesforce Commerce Cloud documentation** — `developer.salesforce.com/docs/commerce`. SFRA reference; Page Designer reference; B2C Commerce APIs reference.
- **PWA Kit documentation** — `developer.salesforce.com/docs/commerce/pwa-kit-managed-runtime`. PWA Kit + Composable Storefront reference.
- **Page Designer development guide** — within the Salesforce Commerce Cloud docs; component definition reference; configuration schema reference.
- **Chakra UI documentation** — `chakra-ui.com/docs`. Theme system; component reference; headless primitives.

### MCP / AI-readability (§6)

- **Model Context Protocol specification** — `modelcontextprotocol.io`. The protocol's canonical reference (per 34's reference list).
- **Per-CMS MCP wrappers** — track via the DTCG GitHub community-group repo and per-vendor roadmap announcements; no canonical aggregator exists as of mid-2026.

### Composable-content patterns (§7)

- **Uniform documentation** — `uniform.app`. Composable orchestration reference.
- **Layer0 (now Edgio) documentation** — `edg.io`. Composable edge reference.
- **Vercel composable stack documentation** — `vercel.com/docs`. Edge Functions, Vercel KV / Postgres / Blob, Next.js App Router as the composable substrate.
- **MACH Alliance** — `machalliance.org`. The industry consortium for Microservices, API-first, Cloud-native, Headless architectures; defines the architectural principles.

### Practitioner writing on CMS-DS integration

- **Brad Frost on WordPress / Gutenberg** — `bradfrost.com`. Occasional posts on WordPress-as-DS-host.
- **Nathan Curtis (EightShapes) on CMS integration** — `medium.com/@nathanacurtis`. Less frequent than tokens / docs writing but occasional CMS-relevant material.
- **Jamstack Conf back catalogue** — `jamstackconf.com`. CMS-DS-integration talks throughout 2020–2026.
- **Headless Creator Conference** — recent industry conference focused on headless CMS practitioner content.
- **Chris Coyier's blog and CSS-Tricks archive** — practitioner-level WordPress and Jamstack writing.

### Verification notes

- All "as of mid-2026" claims about vendor positioning, platform versions, MCP support timelines, and headless-CMS market share reflect mid-2026 platform state. Verify against current docs before treating any specific claim as load-bearing in client work.
- The four-axis framing (traditional / hybrid / headless / composable) is the practice's articulation; verify whether the field's vocabulary has shifted in subsequent quarters before client-facing presentation.
- The eight-platform comparison table at §1 is current as of mid-2026; verify per-platform claims (especially Sitecore XM Cloud's API direction, Storyblok's preview SDK, Salesforce PWA Kit's composable direction, Strapi v5's stability) per project.
- The MCP-readiness assessment at §6 is observation-grounded against publicly visible vendor positioning; verify quarterly. Native vendor MCP from Contentful, Sanity, Storyblok, and others may land between when this file is captured and when the practice references it; the trajectory is faster than the typical CMS feature-release cadence because of the AI-readiness commercial pressure.
- The composable-DXP vendor landscape (Uniform, Layer0/Edgio, Vercel) is mid-maturity as of mid-2026; the off-the-shelf orchestration tooling is still evolving; verify per project.

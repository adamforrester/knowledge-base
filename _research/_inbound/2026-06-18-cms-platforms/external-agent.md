# Modern CMS Platforms and Design System Integration Architecture

## The CMS architectural axis — the framing altitude

The enterprise content management landscape of the 2025–2026 period demands a highly disciplined approach to design system (DS) integration, governed entirely by the underlying platform architecture. For a design systems practice operating at a global agency scale, scoping a "CMS implementation" without explicitly classifying the client's platform procurement into one of four distinct architectural shapes guarantees a severe misalignment of deliverables, integration models, and retainer parameters. Analyst consensus, including Forrester and Gartner's 2025–2026 evaluations of the Digital Experience Platform (DXP) market, indicates that the market has fundamentally bifurcated; differentiation now lies not in feature accumulation, but in how platforms orchestrate data across decoupled architectures.

The modern CMS axis splits into four highly defined architectural shapes:

- **Traditional Architecture**: Server-rendered, page-tree-based systems where the CMS maintains monolithic authority over both the content schema and the presentation layer. Platforms such as Adobe Experience Manager (AEM) and Drupal sit firmly here. In this shape, the design system must be tightly coupled to the CMS delivery mechanism, typically outputting proprietary artifacts such as AEM clientlibs or Drupal Single Directory Components (SDC). The DS team ultimately surrenders final HTML rendering authority to the CMS back-end infrastructure.
- **Hybrid Architecture**: Systems where the CMS maintains authority over the content and supplies a mandatory authoring chrome surrounding the components, yet presentation rendering remains partially decoupled depending on the digital surface. WordPress block themes (utilizing Full Site Editing) and Salesforce Commerce Cloud (SFCC) Page Designer inhabit this space. The design system operates in a partially coupled state: foundational tokens and primitives are heavily integrated into the CMS's primary UI layer (e.g., Gutenberg blocks or Page Designer JSON meta-definitions), while distinct storefronts or decoupled web applications may consume the exact same underlying component models headlessly via REST or GraphQL.
- **Headless Architecture**: API-first systems where the CMS strictly owns content storage and exposure, completely relinquishing presentation logic to decoupled consumers. Sitecore XM Cloud, Contentful, Sanity, Strapi, and Storyblok occupy this quadrant. Authoring paradigms shift entirely from visual, context-aware environments to schema-first, data-as-content models. The design system operates with maximum rendering autonomy, utilizing modern frontend frameworks (React, Vue, Svelte) to ingest JSON payloads and marshal data into component properties.
- **Composable Architecture**: A cross-cutting, multi-service content mesh representing the evolution of the headless CMS into a federated DXP. This architecture utilizes orchestration layers like Uniform or Vercel's content platform to ingest explicit schemas from multiple vendors (e.g., Contentful for editorial, Akeneo for product information, Algolia for search) and compile them at the edge. The design system functions as the rendering layer for an orchestrated stream of data, requiring components to act as universal translation layers capable of mapping heterogeneous API payloads to standardized props.

Naming this architectural shape during the Discovery phase of an engagement is the primary predictor of integration success. A traditional CMS implies tight DS-CMS coupling; a headless implementation guarantees loose coupling; a composable engagement multiplies the integration surface area per connected service; a hybrid model necessitates distinct pipelines for authoring-chrome components versus headless storefront consumption. The exact same DS architecture—a multi-brand token tree, a React component library, and a documentation site—lands completely differently across these four shapes.

Conflating these models introduces catastrophic scoping risks. An agency that conflates "headless CMS" with "decoupled content delivery" will underestimate the custom engineering required to provide content authors with a functional preview-as-you-author environment, a capability absent by default in strict schema-first headless platforms. Conflating "Page Designer" with WordPress "block themes" leads to the misapplication of block-grid composition models onto Salesforce's rigid page-type and slotted-region mechanics. Conflating "composable" with "headless" ignores the multi-service orchestration layer, drastically under-scoping the API marshalling logic required to reconcile disparate content models into unified component props.

To standardize scoping and Discovery conversations, the practice utilizes the following synthesis-ready comparison table to categorize platforms, determine DS-integration models, and locate the ultimate authority for authoring and storage.

| Platform | Architectural Shape | DS-Integration Model | Authoring Authority | Content-Storage Model |
|---|---|---|---|---|
| **AEM** | Traditional | Tight (Clientlibs, HTL, Core Components) | CMS (WYSIWYG, Experience Fragments) | JCR Tree (Hierarchical) |
| **Drupal** | Traditional | Tight (SDC, Twig templates) | CMS (Layout Builder, Paragraphs) | Relational DB (SQL) |
| **WordPress** | Hybrid | Partially-Coupled (Block Themes / theme.json) | CMS (Gutenberg FSE, Block Patterns) | Relational DB (MySQL) |
| **SFCC Page Designer** | Hybrid | Partially-Coupled (JSON Meta + React / ISML) | CMS (Page Designer drag-and-drop) | SFCC Proprietary DB |
| **Sitecore XM Cloud** | Headless | Loose (JSS SDK, Next.js, Edge GraphQL) | CMS (Sitecore Pages / Content Editor) | Edge CDN (GraphQL) |
| **Contentful** | Headless | Loose (Delivery API, React SDK) | CMS (Schema-driven web app) | API-First SaaS (Content Graph) |
| **Sanity** | Headless | Loose (Portable Text, GROQ / GraphQL) | CMS (Customizable Sanity Studio) | Sanity Content Lake (JSON) |
| **Strapi / Storyblok** | Headless | Loose (REST / GraphQL / Storyblok SDK) | CMS (Admin UI / Visual Editor iframe) | Relational / API-First |

## Headless CMS coverage

The headless CMS market in the 2025–2026 period bifurcates cleanly between enterprise-grade orchestrators prioritizing high-availability CDNs and developer-first frameworks offering code-centric extensibility. The practice engages with five dominant platforms in this space, each imposing unique constraints on how the design system marshals data, renders previews, and structures content schemas.

**Sitecore XM Cloud.** The Sitecore platform direction since ~2023 firmly separates the Experience Manager (XM) authoring surface from the Experience Platform (XP) personalization layer, delegating global delivery to the Sitecore Experience Edge. For headless content delivery, the legacy Layout Service API has been deprecated in favor of the GraphQL Edge API.

The DS-integration shape centers entirely on the Sitecore JavaScript Rendering SDK (JSS) and Next.js. Components built by the DS team serve as the rendering layer, receiving layout and field data mapped by the JSS SDK. Sitecore routing is driven by the JSS manifest (`.sitecore.js` files), which maps frontend React components to Sitecore's rendering definitions. A critical operational constraint for agency teams is the GraphQL query depth limit on the Edge API. Complex, deeply nested component architectures frequently trigger `too nested to execute` errors, requiring the DS team to abandon pure Layout Service hydration and implement component-level data fetching via Next.js `getStaticProps` to resolve subsequent layout branches independently. Furthermore, retrieving operational system fields (such as creation or update dates) for components requires deploying specific schema exclusion patches to the Edge API, as default headless configurations aggressively filter fields prefixed with `__`. The Code Connect and `.ai.json` integration pathways remain custom per project, heavily relying on the bespoke JSON output of the JSS manifest rather than standardized tooling.

**Contentful.** Serving as the canonical headless CMS reference, Contentful operates a strict multi-tenant SaaS model segregated into spaces and environments. It enforces a highly structured content graph utilizing standard field types and rich-text nodes. The DS-integration model operates via the Delivery API and Preview API (REST or GraphQL). The practice maps Contentful's field types directly to DS component props, employing the `@contentful/rich-text-react-renderer` to traverse abstract syntax tree (AST) nodes and replace default HTML tags with the agency's React components.

The primary operational hurdle is the absence of native preview-as-you-author capabilities, an inherent limitation of strict schema-first platforms. To close this gap, engagements rely on Vercel Content Link (formerly Visual Editing). This pipeline requires the DS team to implement Content Source Maps, a mechanism utilizing steganography to embed hidden Unicode metadata directly into the rendered text strings via the Live Preview SDK. When Vercel detects these encoded strings in the preview environment, it overlays an edit link mapping directly to the Contentful entry ID. The DS engineering team must implement specific sanitization routines (such as the `splitEncoding` function) where these invisible characters break CSS rules, notably `letter-spacing`, or corrupt URL values. Contentful represents the cleanest CMS-vs-DS boundary in the field: the CMS definitively owns content types and entries, while the DS strictly owns tokens and rendering logic.

**Sanity.** Sanity differentiates itself via Sanity Studio, a highly customizable, open-source authoring application defined entirely in code (React), backed by the real-time Sanity Content Lake. Unlike Contentful's locked SaaS UI, Sanity Studio permits the DS team to explicitly import design system components, tokens, and icons directly into the CMS authoring interface, perfectly aligning the editorial experience with the frontend reality.

Querying relies on GROQ (Graph-Relational Object Queries) or standard GraphQL. Rich text is handled via Portable Text, a JSON-based specification designed to be entirely renderer-agnostic. The DS-integration shape involves mapping Portable Text block types (`block`, `image`, `customWidget`) directly to DS React components. Similar to Contentful, Sanity preview environments leverage Vercel Visual Editing via Stega-encoded strings. The DS engineering team must frequently utilize the `vercelStegaSplit` utility to decouple the hidden source map metadata from the actual string value before applying it to sensitive React attributes, preventing hydration mismatches and broken styling overlays. Sanity is the strategic fit for engagements requiring deep custom modeling, whereas Contentful serves best for out-of-the-box SaaS demands.

**Strapi.** Strapi remains the default headless CMS for engagements requiring self-hosted infrastructure, particularly for clients in highly regulated industries or those possessing strict data-sovereignty and on-premise requirements. The release of Strapi v5 throughout late 2024 and early 2025 introduced substantial architectural shifts that drastically alter the DS-integration contract.

The legacy Entity Service API was entirely replaced by the Document Service API, flattening API response formats by removing the deeply nested `data.attributes` wrappers prevalent in v4. Consequently, any frontend DS consumer migrating from v4 to v5 requires complete refactoring of its data fetching and mapping utility layers, alongside transitioning from numeric `id` parameters to persistent `documentId` strings. The v5 architecture additionally replaced Webpack with Vite for the admin panel and introduced robust TypeScript support, heavily accelerating DS component integration into custom Strapi plugins. Furthermore, **Strapi v5 introduced a native, opt-in Model Context Protocol (MCP) server**, significantly altering the AI-readiness scoping phase for these engagements.

**Storyblok.** Storyblok uniquely combines API-first headless delivery with a native visual editor. As authors edit content schemas, the storyblok-react (or Vue/Svelte) SDK renders the frontend components inside an iframe hosted on storyblok.com, providing immediate preview fidelity.

This platform bridges the WYSIWYG-vs-headless gap, making it the strategic choice for clients migrating from traditional monolithic platforms (such as legacy WordPress installations) who demand visual composition without surrendering API delivery. The DS-integration shape maps Storyblok's "blocks" directly to React components via the SDK. However, the iframe-based sandbox environment carries heavy tradeoffs: complex frontend states, interactive single-page application (SPA) routing, and tightly coupled context providers frequently break within the editor, requiring the DS team to construct robust fallback states and conditional rendering logic specifically optimized for the Storyblok preview environment.

Across all five platforms, the DS engagement scope remains structurally consistent: a token tree, a component library, an API marshalling layer mapping data to props, and Studio or visual editor customizations. None of these represents a "default" headless CMS; the platform choice cascades from the client's commercial portfolio (Sitecore), SaaS preferences (Contentful), bespoke modeling needs (Sanity), hosting restrictions (Strapi), or editorial preview demands (Storyblok).

## WordPress as DS host

Despite heavy industry narrative favoring composable and headless architectures, WordPress remains a high-volume, highly relevant engagement type at the agency. Procurement shapes dictate two strictly diverging integration paths: block-theme builds (the modern direction since WordPress 5.9 / FSE) and headless-WordPress builds (REST or WPGraphQL serving a separate React frontend).

**Block themes and Full Site Editing (FSE).** Driven by the maturation of Full Site Editing (FSE) through versions 6.0 to 6.4, block themes represent the recommended path for coupled WordPress engagements in 2026. The architectural core of FSE is the `theme.json` file, which dictates global styles, color palettes, typography scales, and spacing constraints.

This maps directly to the practice's design tokens. The DS-integration shape relies heavily on Style Dictionary. A custom format transform within Style Dictionary ingests the agency's primitive and semantic tokens, outputting a fully compliant `theme.json` artifact. Tokens automatically flow into the WordPress Block Editor (Gutenberg), populating the `settings.color.palette` and `settings.typography.fontSizes` UI controls. Because there is currently no formal Design Tokens Community Group (DTCG) specification dictating CMS synchronization, the practice must maintain custom parsers mapping the DTCG format to the WordPress schema.

**Custom blocks (Gutenberg blocks) as the component primitive.** The building blocks of the WordPress presentation layer are Gutenberg blocks, constructed as React components wrapping the DS primitives, registered via `block.json` and the native WordPress Block API. Each block definition requires an editor component (rendered in the WP admin) and a save function (the serialized HTML output).

For clients lacking the React engineering capability to maintain native Gutenberg blocks, Advanced Custom Fields (ACF) Blocks provide a PHP-based alternative. The DS-integration tradeoff is severe: ACF blocks rely on server-side rendering (SSR) via PHP, drastically reducing the instant, client-side preview fidelity of the Block Editor and forcing the DS team to maintain dual template ecosystems (React for the DS documentation, PHP for the CMS).

**The DS-vs-block-pattern boundary.** A critical procurement-grade decision involves delineating design system components from WordPress block patterns. The practice enforces a strict boundary: DS components ship as individual Gutenberg blocks (the reusable primitives), whereas block patterns are localized compositions of DS components (reusable layouts). The design system provides the Button, Card, and Input blocks; the WordPress theme team composes those into a standard "Hero Section" block pattern. Attempting to manage complex page layouts as monolithic DS components collapses the composability of the WordPress editor.

**Headless WordPress.** Headless WordPress deployments decouple the presentation layer entirely, utilizing the REST API or the mature WPGraphQL extension to expose content types and ACF fields to a Next.js or Remix frontend. The consumer-side integration shape mirrors Contentful or Sanity, but carries a heavy authoring-side tradeoff. The standard WP admin interface is highly unoptimized for headless preview workflows, often requiring custom preview deployment infrastructure tied to draft post IDs. Agency scopes utilizing WP Engine's Faust.js framework or the Automattic-supplied headless toolchains alleviate some preview-routing friction, but the headless WordPress shape still scopes closer to a 300–600 hour headless engagement compared to the 250–500 hour scope of a native block-theme build. The procurement shape dictates the team composition and the delivery model entirely.

## Salesforce Commerce Cloud Page Designer

As demonstrated by the New Balance active engagement, integrating an agency-built design system into Salesforce Commerce Cloud (SFCC) requires navigating a complex, proprietary presentation architecture. The modern B2C Commerce stack currently straddles legacy Storefront Reference Architecture (SFRA) and the Headless Commerce/Composable Storefront (PWA Kit) directions.

**Page Designer's component model.** Page Designer (PD) serves as the drag-and-drop authoring surface for merchants, structured around a rigid, hierarchical component model. The top-level composable surface is the **Page Type** (e.g., Home, Category, Product), which defines specific slot-shapes known as **Regions** (e.g., Header, Main, Footer). Within these regions, authors place **Components**.

Each page type and component requires a JSON meta-definition file located in the custom cartridge (`/experience/pages` or `/experience/components`). This schema dictates the `region_definitions` (including component exclusion rules and instantiation limits) and the `attribute_definitions` (the configuration schemas that populate the merchant's authoring form). The DS-integration shape requires wrapping foundational DS components inside PD component scripts. The merchant's input on the PD configuration schema is mapped directly to the DS component's props.

**The relationship to SFRA and Headless Commerce.** SFRA represents the legacy server-rendered path based on ISML templates. Page Designer layers on top of SFRA, granting authors a visual composition surface above the traditional cartridge model. Conversely, Headless Commerce leveraging the PWA Kit represents the modern path for greenfield engagements. In this headless architecture, ISML is entirely removed. The frontend relies on React Router 7, leveraging streaming server-side rendering (SSR) and data loaders to fetch SFCC APIs before hydrating the React application on the client.

Page Designer pages are resolved in the PWA Kit via a component registry. The DS integration requires executing an `initializeRegistry()` function during app startup that lazily imports React components mapped to specific SFCC `typeId` strings. When the PD API returns a layout payload, the `<Component>` wrapper dynamically resolves the registered React component and injects the authored attributes.

**Chakra UI as the New Balance choice.** For engagements utilizing the PWA Kit, Chakra UI is frequently deployed as a foundational "DS in a box" due to its robust accessibility standard. The strategic decision for the agency involves determining the operational relationship between the bespoke design system and Chakra UI. The practice generally evaluates two patterns:

1. **Lightweight Extension**: Mapping the agency's design tokens directly into Chakra's theming engine via the native theme system.
2. **Heavy Wrapping**: Treating Chakra purely as an unstyled headless primitive layer, wrapping it in bespoke, agency-authored React components to exert total control over the DOM and visual styling.

**Salesforce-specific authoring patterns and scoping.** The Page Designer visual editor is exclusively hosted within Salesforce Business Manager. Unlike Storyblok or Sanity, the agency cannot easily inject custom iframe preview environments or local development UI wrappers without relying on complex proxy setups. Because merchants are restricted to the attributes explicitly defined in the JSON meta-definition files, the DS engagement must heavily scope the creation of these configuration schemas as discrete deliverables alongside the React code. Greenfield SFCC implementations with a headless frontend generally scope between 500–800 hours. Migration engagements (e.g., scaling the New Balance Australian site to global markets) scope smaller, primarily involving regional data binding and extended PD component coverage. The operational complication remains that underlying $10–50M platform migration decisions heavily constrain the DS deployment strategy.

## The CMS-vs-DS authoring boundary

One of the most profound scoping failures in agency CMS implementations stems from an undefined authoring boundary between the design system and the content management system. Without an articulated point of view, engagements suffer from structural collapse: the CMS attempts to manage presentation details, or the design system inadvertently hardcodes editorial content.

The practice's existing material firmly articulates this boundary at the content layer: design tokens manage templated, system-level content, while the CMS manages editorial, product-specific content. Applying this paradigm to the component-anatomy layer resolves the tension between DS and CMS schema dominance.

**The component-anatomy boundary.** The core principle dictates that the design system owns component **structure**, and the CMS owns content **instances**. The design system defines the rigid boundaries: the acceptable props, the predefined states (hover, disabled, active), the structural slots, and the specific variant combinations. The CMS exists solely to populate those structures with instance-level overrides. Providing a CMS author with a hex-code color picker to override a component's background violates the boundary; providing a dropdown selection referencing `Brand Variant A` or `Brand Variant B` (which map back to DS tokens) respects it.

This boundary becomes critical when integrating Code Connect and the `.ai.json` registry. For CMS-managed components, the AI readability pipeline must source the component contract (acceptable props, strict typing) from the design system's code surface, while simultaneously parsing the structural layout rules (available regions, permitted block combinations) from the CMS schema.

**The boundary table.** To prevent boundary drift during an engagement, the following synthesis-ready artifact explicitly defines the source of truth for component anatomy:

| Anatomy / Content Type | Source of Truth | Operational Rules & Enforcement |
|---|---|---|
| **Component Structure** | Design System | Defines accepted props, internal state logic, slots, and DOM structure. Cannot be altered via CMS. |
| **Component Variants** | Design System | Defines visual/behavioral modes (e.g., Dark Mode, Outlined, Ghost). The CMS exposes these only as strict dropdown enumerations based on DS configuration schemas. |
| **Templated Content** | DS Tokens | System-wide microcopy (CTAs, validation errors, empty states). Stored in the DS token dictionary. |
| **Editorial Content** | CMS | Marketing copy, product descriptions, asset media. Authored per instance. |
| **Per-Instance Overrides** | CMS | Data populating specific prop values (e.g., the specific text of a Hero Headline). Bounded by character limits defined in the DS. |
| **Layout Composition** | CMS | Page-level structural orchestration. The CMS dictates the grid and region layout, using DS components as the atomic building blocks. |
| **Localisation Variants** | CMS / DS | Editorial content resides in the CMS; interface/system-level translations reside in the DS token catalog. |

Naming this boundary explicitly in the Statement of Work (SOW) protects the structural authority of the design system. Without it, clients inevitably push for "WYSIWYG" flexibility, driving the CMS to store raw HTML or inline CSS, effectively decoupling the presentation layer from the design system's token pipeline and rendering systemic updates impossible.

## MCP / AI-readability for CMS-managed components

As the Model Context Protocol (MCP) rapidly standardizes how AI agents interface with remote data sources, exposing CMS schemas and content instances to AI clients has become a critical extension of the `.ai.json` pipeline. When components are authored and stored in the CMS, the design system's structured contracts are insufficient; the `.ai.json` registry must fuse the DS component anatomy with the CMS's content instance data.

**Per-CMS feasibility.** The readiness for native AI integration varies wildly across the practice's supported platforms. Notably, CMS-vendor MCP implementations are not yet native across the board, with the exception of early movers like Contentful, Sanity, and integration tools like Supernova.

- **Contentful**: Highly mature. Official MCP servers function via the Management API to expose tools for querying entries, validating content models, and executing AI workflows across spaces. Wrapping this existing implementation to join with the DS contract is low-effort.
- **Sanity**: Deeply integrated. The official Sanity MCP server is hosted infrastructure (`mcp.sanity.io`), automatically parsing TypeScript schema definitions and allowing AI clients to execute complex GROQ queries, manage datasets, and patch documents with full schema awareness.
- **Strapi**: As of v5.47, Strapi ships with a native, built-in MCP server. It authenticates via scoped Admin API tokens and dynamically generates CRUD tools for every content type. Because Strapi is self-hosted, the agency can deploy bespoke MCP wrappers directly alongside the infrastructure.
- **WordPress**: Supported via the official Automattic WordPress MCP Adapter, which relies heavily on the new WordPress Abilities API. The adapter translates MCP protocols to HTTP REST endpoints, utilizing a proxy (`mcp-wordpress-remote`) to execute authenticated operations. InstaWP provides one-click server deployments for managed setups.
- **Sitecore XM Cloud & SFCC**: Custom implementation required. Sitecore's Edge GraphQL is well-structured, but requires bespoke MCP server tooling to expose the JCR content tree in a flat, AI-parseable context. SFCC Page Designer completely lacks native MCP support, and wrapping the B2C Commerce API is fraught with vendor lock-in constraints and authentication complexities.

**The bet and the practice's bridge investment.** Native CMS-vendor MCP support will land ubiquitously in the 2026–2027 timeframe alongside design-token-vendor implementations. Contentful and Sanity are the definitive first movers; Strapi's open-source community provides rapid follow-on capabilities; Sitecore, WordPress core, AEM, and SFCC lag behind in the 2027–2028 timeframe.

Until native support achieves parity, the practice operates a custom MCP wrapper per engagement. This typically scopes at 16–40 hours per CMS. The custom server exposes combined data: the content-type schema, the specific content-instance retrieval, and the corresponding DS-component contract. This extends the conceptual tooling surface. In addition to standard DS tools (`list_components`, `get_component_props`), the MCP server registers `list_content_types`, `get_content_schema`, `query_entries`, and `get_populated_instance`. This combined surface enables AI clients to reason simultaneously about what components exist and what content fills them per instance.

**The CMS-as-DS-source pattern.** A specific architectural edge case involves the "headless DS," where the actual component structure (the definition of the props themselves) is authored as content types within the CMS, rather than existing as code. The practice strictly categorizes this as an anti-pattern. While it affords maximum flexibility to non-engineering teams, it completely collapses the CMS-vs-DS boundary, resulting in severe variability-by-design fractures. It should only be scoped for ultra-thin presentation layers where code deployments are actively prohibited by the client's operational model.

## Composable-content patterns

The 2025–2026 composable movement represents the evolution of headless architecture into the "content mesh." In a composable digital experience platform (DXP), content is no longer the output of a single monolithic CMS; it is a continuously orchestrated artifact aggregated from specialized microservices (CMS, PIM, DAM, CDP) via a unified orchestration layer.

**What "composable" means architecturally.** Vendors dominating this quadrant—such as Uniform, Vercel (via the v0/Next.js stack), and Storyblok's composable orchestrator pivot—redefine the integration narrative. The market underwent minor consolidation shocks, notably the late-2024 Chapter 11 bankruptcy of Edgio (formerly Layer0), which ceased its edge CDN operations by January 2025, forcing enterprises to rapidly migrate to Cloudflare, Fastly, or Vercel.

In a composable architecture, the design system sits downstream of the orchestrator. Content types are defined independently per service: editorial copy originates in Contentful, product specifications in Akeneo, and targeted audience segments in Segment or 6sense. The orchestration platform (e.g., Uniform's visual workspace) reconciles these disparate schemas per user request, compiling a unified JSON payload at the edge. For the design system, the component contract remains stable, but the integration surface multiplies exponentially. The DS components become the common vocabulary across the stack; they must accept standard props regardless of which upstream microservice supplied the underlying data.

**Schema-first authoring and composition-at-render.** Because composable content is bound at request-time on edge infrastructure, preview-as-you-author becomes a highly complex, multi-service reconciliation problem. Vercel addresses this via steganography (Content Source Maps) injected across the payload, while Uniform relies on dedicated Canvas compositions. The DS team must guarantee that component prop shapes are resilient to partial data payloads (e.g., if the PIM responds but the CMS draft fails to resolve in the preview environment).

**The variability-by-design problem applied to content.** The core challenge of the composable mesh is the sheer volume of per-render variance. The variability-by-design problem dictates that the author is no longer defining a single page, but rather a *space* of possible content compositions powered by AI-driven personalization engines. The practice must enforce strict guardrails: all dynamic composition must be bounded by the DS schema contract. Variant-logging and evaluation-driven QA patterns are mandatory to ensure that edge-composed content does not shatter the React component tree or violate accessibility (WCAG) guidelines.

The boundary between content tokens and composable content is explicit: content tokens constitute templated content owned strictly by the DS; composable content constitutes editorial content assembled by the orchestration layer. Both systems treat content as data, separated entirely by the authoring surface.

Practitioner-side scoping for composable engagements demands a 1.5× to 2× multiplier against comparable headless builds. The DS engagement rarely operates in isolation; it functions as one parallel workstream alongside dedicated commerce, CDP, and middleware integration squads, requiring highly disciplined API contract negotiations before the first React component is ever drafted.

## Integration — deepen 10, See also block

This document represents the deep-dive expansion on modern CMS architectures, complementing the established Adobe Experience Manager (AEM) and Drupal foundational materials. The framing altitude navigates the reader between the platform sections, enforcing architectural diagnosis before technical implementation.

**See Also:**

- 03-component-library-architecture.md: Detail on the component-library altitude that consumes the API payloads described across the headless and composable shapes.
- 04-content-as-a-system-layer.md: Outlines the foundational content-token vs. CMS boundary, which this report extends into the component-anatomy boundary table.
- 13-internationalisation.md: Strategies for i18n where editorial translation resides in the headless CMS, while system-level microcopy routing occurs via DS tokens.
- 17-accessibility-annotations.md / 28-a11y-testing.md: Ensuring ARIA states and accessibility constraints propagate correctly through CMS-rendered component wrappers (specifically within hybrid architectures like SFCC Page Designer).
- 24-multi-brand-architectures.md: Mapping complex token architectures into multi-tenant, multi-space headless configurations (e.g., Contentful environments).
- 30-ai-readability.md: The baseline AI-readability pipeline and `.ai.json` registry mechanics, which the MCP integration strategies in this report directly extend to CMS-managed components.
- 33-white-label-engagements.md: Architectural scoping for multi-CMS reseller stacks, heavily reliant on the headless and composable models outlined above.
- 34-workstation-mcp.md: Practical execution of the workstation MCP stack, bridging Figma, Storybook, and the CMS MCP servers detailed in this report.

**Open Residual to Track:** The four-axis framing (traditional, hybrid, headless, composable) represents the stable mid-2026 consensus. The practice must actively track the emergence of a definitive fifth shape—the "Agentic / AI-Native CMS"—where content is dynamically generated rather than authored, fundamentally altering the schema contract. Track quarterly against emerging features in platforms like Uniform and Anthropic-integrated workflows.

## References

- Strapi. "Strapi release roundup: Everything that changed between March and June 2026." Strapi Blog.
- Open Space Services. "Strapi v4 to v5 migration: what broke, what changed, and how to upgrade without losing data."
- Strapi. "Strapi v4 to v5 migration resources." Strapi Documentation.
- Salesforce. "Page Designer Meta Definition Files." B2C Commerce Documentation.
- Salesforce Developer Center. "B2C Commerce Development for Page Designer."
- Sitecore Diaries. "Connecting to Sitecore Edge and Headless Delivery."
- Dylan Young. "Sitecore XM Cloud: The Correct Way to Resolve GraphQL 'Too nested to execute' issue."
- Amit K. "How to Get System Fields in Sitecore GraphQL Query."
- Perficient. "Building with Sitecore APIs: From Authoring to Experience Edge."
- Contentful. "Contentful MCP Server." GitHub Repository.
- CrafterCMS. "What is the Model Context Protocol."
- Sanity. "Build with AI: MCP Server." Sanity Documentation.
- AugmentCode. "contentful-mcp."
- Contentful. "MCP Server Overview." Contentful Developer Documentation.
- Salesforce Developer Center. "Page Designer for PWA Kit."
- Salesforce Developer Center. "About PWA Kit and Managed Runtime."
- Salesforce Developer Center. "Storefront Next Architecture."
- Salesforce Developer Center. "Get Started with Storefront Next."
- Design Tokens Toolbox. "Theme Manager and Tokens Generator."
- Style Dictionary. "Style Dictionary v4 Documentation."
- Phrutos. "What are Design Tokens and When to Use Them."
- Publishing Project. "Using Design Tokens in CSS."
- Brad Frost. "Atomic Design: Chapter 5."
- Kontent.ai. "Make your design system content-friendly."
- InstaWP. "WordPress MCP Server."
- WooCommerce. "MCP Integration for WooCommerce." WooCommerce Developer Docs.
- Responsive Menu. "10 Best WordPress MCP Servers."
- Jonathan Bossenger. "From Abilities to AI Agents: Introducing the WordPress MCP Adapter." WordPress Developer Blog.
- Uniform. "Uniform Visual Workspace."
- Uniform. "Composable DXP Overview."
- DXP Scorecard. "Uniform Platform Assessment."
- Uniform. "Agentic Digital Experience Platform."
- CMSWire. "What You Need to Know About Digital Experience Platforms."
- Matrix BCG. "A Brief History of Edgio."
- Wikipedia. "Edgio."
- BlazingCDN. "Fastly Alternatives 2026."
- Prismetric. "What is Vercel v0?"
- Pooya Golchian. "Headless CMS 2026: Contentful vs Strapi vs Sanity vs Payload Compared."
- Agility CMS. "Agility CMS vs Contentful."
- Sitecore. "Types of JSS Manifest Data." Sitecore Developer Documentation.
- Sitecore. "Sitecore JavaScript Rendering SDK NPM, 'Architecture overview: JSS'."
- Sitecore. "Generating a JSS app manifest file."
- Salesforce Developer Center. "Page Designer Registry."
- Netguru. "Design System Tools."
- Design Tools FYI. "Best Tools for Prototyping (2026)."
- Contentful. "Content Source Maps with Vercel." Contentful Developer Documentation.
- NPM. "@sanity/client documentation."
- Sanity. "Troubleshooting Visual Editing." Sanity Documentation.

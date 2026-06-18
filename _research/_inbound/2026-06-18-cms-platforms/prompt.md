You are researching modern CMS platforms — the practitioner-facing
discipline of architecting and operating a design system across the
2025–2026 CMS landscape (headless / composable / hybrid / Salesforce
Commerce Cloud's Page Designer / WordPress) — for a senior design
systems practitioner leading the practice at a global creative agency.
The output is a structured knowledge document whose load-bearing
material will land as a deepen pass on `10-cms-and-platform-integration.md`
(currently AEM-and-Drupal-shaped at 321 lines / ~5,000 words; 12 H2
sections; AEM as the dominant treatment).

This run is the *modern-CMS-platform-coverage* half of the CMS
question. The traditional (AEM / Drupal) half is closed by 10's
existing coverage. What is *not* closed is the modern composable /
headless / hybrid / Page-Designer / WordPress surface that the
practice ships against without an articulated POV. Per 09 §1.32 the
agency's clients on Sitecore (a real cohort) and on Salesforce
Commerce Cloud (per the New Balance engagement in 00b §Active
engagement examples) currently get little from 10's existing AEM-
shaped material. This run closes that gap.

The synthesis path is **deepen 10, not a new file** — committed in 09
§1.32 and confirmed for this run. The structural plan: a new framing-
altitude H2 lands near the top of 10 (between §Central problem and
§AEM Architecture Fundamentals) that names the four architectural
shapes — traditional / hybrid / headless / composable — as a decision
tree above the existing platform-specific material. New platform
and concept H2 sections append after Drupal but before the cross-
cutting §DS Delivery Model: NPM Package vs. Embedded section. The
existing AEM and Drupal sections stay intact; the new framing H2 at
the top navigates the reader between the platform sections.

This is not an introductory guide — assume the reader is the practice
lead, has read 10 / 03 / 04 / 30 / 33 / 34 in the practice's vault,
knows what AEM clientlibs / Drupal SDC / WordPress block themes / GraphQL
/ REST / OpenAPI / SFRA / Headless Commerce are at a working level,
knows what a content model / content type / schema-first authoring is,
knows what Code Connect and `.ai.json` are (per 30), what an MCP
server is (per 34), and what the New Balance engagement on Salesforce
Commerce Cloud Australia is (per 00b §Active engagement examples).
Don't explain what GraphQL is, what a JSON content model is, what
Storefront Reference Architecture (SFRA) is at the basic level, what
WordPress Gutenberg is, what Sanity Studio is, what Sitecore XM
Cloud's split from XM is — explain how the practice should *operate*
the modern CMS layer as a discipline at agency scale, where each
platform's authoring model and DS-integration shape constrain the
engagement, where the field's CMS tooling has known gaps that
practitioners work around, what the four CMS architectural shapes
mean for scoping decisions, and how this layer relates to (but does
not replace) the AEM / Drupal coverage that 10 already ships.

Research scope — cover all of the following:

1. The CMS architectural axis — the framing altitude

- The case that modern CMS work splits into four architectural
  shapes: **traditional** (server-rendered, page-tree-based, where
  the CMS owns presentation — AEM and Drupal sit here); **hybrid**
  (the CMS owns content and supplies authoring chrome around
  components, but presentation is partially decoupled — WordPress
  block themes and Salesforce Commerce Cloud Page Designer sit
  here); **headless** (the CMS owns content and exposes it via API;
  presentation is fully decoupled — Sitecore XM Cloud, Contentful,
  Sanity, Strapi, Storyblok all sit here); **composable** (the CMS
  is one of several services in a content mesh; content-as-data
  with explicit schemas; the integration is per-channel — this is a
  *cross-cutting* axis rather than a single-shape axis, and the
  mid-2025–2026 wave of "DXP" platforms — Uniform, Layer0, etc. —
  inhabits it).
- Why the four-axis framing matters for scoping. The agency that
  pitches a "CMS implementation" without knowing which shape the
  client's procurement or technology-selection conversation has
  already determined produces engagements that ship the wrong
  architecture for the brief. The architecture choice cascades:
  traditional CMS implies tight DS-CMS coupling (clientlibs, SDC,
  block themes); headless implies loose coupling (component library
  consumes the CMS as a data source); composable implies the DS
  is one of several systems sourcing from a shared content layer;
  hybrid implies the DS is partially-coupled and partially-decoupled
  per surface.
- The shapes carry implications for the engagement scope. The
  practice's discipline: name the architectural shape at scoping
  Discovery, *before* deciding the DS architecture. The same DS
  architecture (a token tree + component library + docs site) lands
  differently in each shape — the integration work, the authoring-
  boundary discipline, the AI-readiness pipeline, and the run-phase
  retainer all shift.
- The synthesis-ready artefact: a comparison table — eight platforms
  (AEM, Drupal, WordPress, Salesforce Page Designer, Sitecore XM
  Cloud, Contentful, Sanity, Strapi/Storyblok grouped) × architectural
  shape × DS-integration model × authoring authority × content-storage
  model. The table the practice carries into scoping conversations.
- The miscategorisation costs to name. The agency that conflates
  "headless CMS" with "decoupled content delivery" misses the
  authoring-side reality that headless CMS authoring is structurally
  different from traditional WYSIWYG authoring (schema-first, no
  preview-as-you-author by default, content-modelled-as-data). The
  agency that conflates "Page Designer" with "block themes" misses
  the Salesforce-specific component model that uses page types and
  regions rather than block-grid composition. The agency that
  conflates "composable" with "headless" misses the multi-service
  content-mesh reality of composable architectures.

2. Headless CMS coverage — Sitecore XM Cloud / Contentful / Sanity /
   Strapi / Storyblok

- **Sitecore XM Cloud.** The Sitecore-platform direction since ~2023:
  Sitecore's headless SaaS offering, separating the Sitecore XM
  authoring surface from the XP personalization layer. Components
  in XM Cloud are React (typically Next.js with the Sitecore JSS
  SDK); the CMS exposes layout via the Layout Service API (deprecated
  in Headless XM/SaaS in favour of the GraphQL Edge API); content
  surfaces via the Sitecore Edge API (GraphQL); personalization via
  Sitecore Personalize (the rebranded Boxever). The DS-integration
  shape: the React components are the DS components (or a thin layer
  on top of the DS); the JSS SDK marshals JSS data → component props.
  Code Connect / `.ai.json` integration is feasible but not yet
  default — the JSS rendering manifest is the closest analogue to
  Code Connect and is custom per project. For agency clients on
  Sitecore (still a real cohort despite the platform's commercial
  pressure), the file currently provides little; this section closes
  that gap.
- **Contentful.** The canonical headless CMS reference. Spaces and
  environments structure the multi-tenant model; content types
  define the schema; entries are the instances; assets handle media;
  the Delivery API and Preview API serve content via REST or
  GraphQL. The DS-integration shape: components consume entries
  via the Delivery API; field types map to component props; rich-
  text fields use the Rich Text Renderer (per Contentful's React /
  JS rendering library). Authoring is in the web app (Contentful's
  SaaS UI) and is schema-driven — there is no preview-as-you-author
  out of the box, though the Preview API plus a custom preview
  environment closes the gap (commonly via Vercel / Netlify preview
  deployments tied to entry IDs). The CMS-vs-DS boundary: Contentful
  owns content types, fields, and entries; the DS owns components,
  tokens, and rendering. The cleanest separation in the field.
- **Sanity.** The structured-content approach. Sanity's
  differentiator is Studio (a self-hosted, customisable authoring
  tool defined in code) plus Portable Text (a JSON representation
  of rich-text that's renderer-agnostic). Content is stored in
  Sanity Content Lake; querying via GROQ (Sanity's query language)
  or GraphQL. The DS-integration shape: similar to Contentful but
  with Studio customisability — the DS team can extend Studio's
  authoring UI to align with the DS's component patterns; Portable
  Text is rendered through component-mapping (each block type maps
  to a DS component). Strong fit for engagements where the content
  model needs heavy customisation; less of a fit where the client
  wants out-of-the-box SaaS.
- **Strapi.** Open-source, self-hostable, plugin-extensible. The
  open-source default for engagements where SaaS is unacceptable
  (regulated industries; on-prem requirements; clients with
  hosting-cost constraints). Content types are defined in admin UI
  or via code; the API is REST or GraphQL (configurable per
  collection); the admin UI is the authoring surface. The DS-
  integration shape: similar to Contentful but with self-hosted
  responsibility — the agency or client team operates Strapi as
  infrastructure, not as a managed service. Strapi v4 vs. v5 (the
  rewrite that landed late 2024 / early 2025) is a meaningful
  upgrade; verify the version per project.
- **Storyblok.** The visual-editor + headless-API combination.
  Storyblok's distinctive feature: a visual editor that previews
  the rendered site as authors edit (via the storyblok-react /
  storyblok-vue / etc. SDK rendering the components in an iframe
  on storyblok.com). Bridges the WYSIWYG-vs-headless gap that
  Contentful and Sanity don't; useful for engagements where the
  client's content team is migrating from WordPress / WYSIWYG and
  needs preview-as-you-author. The DS-integration shape: components
  are React/Vue/Svelte; Storyblok's "blocks" map to components;
  the visual editor renders the components via the SDK. The trade-
  off: Storyblok's preview is sandbox-shaped (renders in iframe),
  not full-stack preview; complex page-level interactions are
  harder to preview faithfully.
- The shared shape across all five. Schema-first authoring (content
  types defined as data); API-served content (REST and/or GraphQL);
  decoupled rendering (the DS's component library renders content
  the CMS supplies). The DS engagement scope: token tree + component
  library + integration layer (the marshalling code that maps API
  fields to component props) + Studio / dialog customisation
  (where the platform supports it — Sanity, Strapi). For all five,
  the CMS-vs-DS authoring boundary is cleanest because the platform
  enforces the separation: content types in the CMS, components in
  the DS, integration in code.
- The five-platform decision tree. Sitecore XM Cloud → engagements
  on the Sitecore commercial track (typically large enterprises
  with Sitecore portfolio investment). Contentful → engagements
  with strong SaaS preference and English-only or simple-locale
  content. Sanity → engagements with bespoke content models and
  custom Studio needs. Strapi → engagements with on-prem /
  regulated / cost-constrained requirements. Storyblok →
  engagements where the content team needs preview-as-you-author.
  None of these is a "default headless CMS"; the platform choice
  is engagement-specific.

3. WordPress as DS host

- The reality. WordPress is still a real engagement type at the
  agency, despite headless / composable narrative pressure.
  Two procurement shapes: **block-theme builds** (the modern
  WordPress direction since 5.9 / FSE / theme.json) and
  **headless-WordPress builds** (REST + WPGraphQL serving content
  to a separate React / Next.js front-end).
- **Block themes and Full Site Editing (FSE).** WordPress 5.9 (Jan
  2022) introduced FSE; 6.0–6.4 matured it; by mid-2026 it's the
  recommended path for new theme work. The theme.json file defines
  global styles, color palette, typography, spacing scale — directly
  analogous to design tokens. Block patterns and block templates
  are reusable composed-content blocks (analogous to AEM
  Experience Fragments). The DS-integration shape for block-theme
  engagements: tokens map to theme.json's `settings.color.palette`,
  `settings.typography.fontSizes`, `settings.spacing.spacingSizes`;
  custom blocks are React components registered via
  `block.json` and the Block API; the editor renders blocks via
  the @wordpress/block-editor package. Style Dictionary can target
  theme.json with a custom transform; tokens flow to the editor
  and to the rendered front-end automatically.
- **Custom blocks (Gutenberg blocks) as the component primitive.**
  Each block is a React component (in the editor) plus a save
  function (rendered output) plus block.json (metadata). The DS-
  integration shape: DS components are wrapped as Gutenberg blocks
  via the Block API; ACF Blocks (Advanced Custom Fields' alternative
  registration path) is a common workaround for clients without
  React engineering; the trade-off is ACF Blocks render server-side
  via PHP and don't get the Block Editor's preview-as-you-author
  fidelity.
- **The DS-vs-block-pattern boundary.** Block patterns are reusable
  layout compositions; design-system components are reusable
  primitives. Where DS-component library ends and block-pattern
  library begins is a procurement-grade decision. The practice's
  working position: DS components ship as Gutenberg blocks (the
  primitives); block patterns are *compositions of DS components*
  (the layouts) and ship as part of the theme rather than the DS.
- **Headless WordPress.** REST API + WPGraphQL (the canonical
  GraphQL extension, ~2.0 stable). Content types and ACF fields
  surface via the API; a separate Next.js / Remix front-end consumes
  them; preview is custom (typically via Vercel preview deployments
  tied to draft post IDs). The DS-integration shape: same as
  Contentful / Sanity at the consumer side; WordPress's authoring
  surface is the trade-off — the WP admin UI is functional but not
  optimised for headless-CMS use. Faust.js (WP Engine's
  headless-WordPress framework) and the WP-supplied headless-react
  toolchain are both options.
- **The two shapes price differently.** Block-theme engagements
  scope similarly to AEM-light engagements (~250–500 hours for
  foundations + theme + blocks). Headless-WP engagements scope
  closer to Contentful / Sanity engagements (~300–600 hours for
  foundations + components + integration + custom front-end).
  The procurement shape determines the team composition and the
  delivery model.

4. Salesforce Commerce Cloud Page Designer

- The context. Per 00b §Active engagement examples — the New Balance
  engagement is on Salesforce Commerce Cloud, with Chakra UI as the
  consuming front-end framework. Page Designer is Salesforce's
  drag-and-drop component-composition authoring surface for B2C
  Commerce. The platform mix: Storefront Reference Architecture
  (SFRA, the older server-rendered shape based on Mustache templates
  and the SiteGenesis cartridge model) → Page Designer (the modern
  drag-and-drop authoring layer; works alongside SFRA) → Headless
  Commerce / Composable Storefront (the React / PWA Kit direction
  since ~2022; uses B2C Commerce APIs).
- **Page Designer's component model.** Page types (the top-level
  composable surface — Home, Category, Product, Article, etc.);
  regions (the slot-shapes within a page type — Header, Hero,
  Body, Footer); components (the building blocks authors drop into
  regions). Each component carries a *configuration schema* —
  what authors can customise per instance. The DS-integration
  shape: DS components are wrapped as Page Designer components
  via the component definition file (JSON metadata + render
  template); the configuration schema maps to component props; the
  rendered output is HTML (SFRA path) or React (PWA Kit / headless
  path).
- **The relationship to SFRA and Headless Commerce.** SFRA is the
  legacy/established path; Page Designer layers on top of SFRA
  and gives authors a composition surface above the cartridge
  model. Headless Commerce / PWA Kit is the modern path for
  greenfield engagements; it uses B2C Commerce APIs and renders
  via a separate React front-end (typically Chakra UI per New
  Balance, or a custom DS). Page Designer's role in the headless
  path is somewhat reduced — the React front-end can render Page
  Designer pages but the visual editor's preview fidelity drops.
- **Chakra UI as the New Balance choice.** Chakra UI is a popular
  React component library with strong accessibility and theming
  support; selected by many SFCC engagements as the "DS in a box"
  starting point. The DS-integration question for the New Balance
  engagement: how does the agency-built DS layer relate to Chakra?
  Two patterns: (a) extend Chakra with the agency's tokens via
  Chakra's theme system (lightweight), (b) replace Chakra with a
  bespoke DS that wraps Chakra's headless primitives (heavier but
  more controlled). The choice depends on the agency's commercial
  model and the client's longer-term maintenance plan.
- **Salesforce-specific authoring patterns.** Page Designer's
  visual editor is Salesforce-hosted (no equivalent to Storyblok's
  iframe-preview customisation); the editor's component palette
  is determined by the component definitions registered in the
  cartridge; the configuration schemas drive the authoring forms
  authors fill in per instance. The agency's DS engagement
  scopes the component definitions, the configuration schemas,
  and the render templates as discrete deliverables.
- **The scope of the Salesforce engagement.** Greenfield SFCC + DS
  + Page Designer + headless front-end with Chakra UI: typically
  ~500–800 hours for the DS-side work alone (foundations + 30–40
  components + Page Designer wrapping + headless-front-end
  integration). Migration engagements (the New Balance "scale
  Australia to other regions" shape) scope smaller because the
  DS exists; the work is per-region adaptation + Page Designer
  component coverage extension + per-region content modelling.
  The complication 00b flags: migrating from the Australian site
  to other regions may require a platform migration to SFCC if
  not already there; this is a $10–50M-range platform decision the
  DS engagement layers on top of.

5. The CMS-vs-DS authoring boundary

- The procurement-grade decision. Per 09 §1.32 — "where component
  anatomy lives in CMS schema vs. system schema; how the two
  source-of-truth claims reconcile; how Code Connect or `.ai.json`
  schemas align with CMS content models." This is the question
  the practice ships against without an articulated POV.
- **The boundary the practice's existing material articulates.**
  Per 04 §Content as a system layer — "tokens for *templated,
  system-level* content; CMS for *editorial, product-specific*
  content." The line is articulable at the content layer; this
  section extends it to the *component-anatomy* layer.
- **The component-anatomy boundary.** The DS owns component
  *structure* — the props the component accepts, the states it
  renders, the slots it composes; the CMS owns content *instances*
  — the specific values authors fill in per instance. The line
  is the same as design-tokens-vs-component-styles: structure in
  the DS; instance-level overrides in the CMS.
- **The Code Connect / `.ai.json` parallel.** Per 30 — Code Connect
  binds Figma components to code components; `.ai.json` exposes
  the structured AI-readable surface. For CMS-managed components,
  the `.ai.json` registry has to source from *both* the DS code
  surface (for component structure) and the CMS schema (for
  content-instance shape). The practice's bet: this is custom
  middleware work today; native CMS-vendor MCP support lands in
  2026–2027 (per §6 below).
- **The boundary table** (synthesis-ready artefact). What lives
  where, by content type:
  - Component structure (props, states, slots) → DS
  - Component variants (visual / behavioural) → DS (with CMS
    surface for author selection per instance via Style System,
    component config schema, etc.)
  - Templated content (CTAs, error messages, empty states) →
    DS content tokens (per 04)
  - Editorial content (copy, images, marketing assets) → CMS
  - Per-instance content (the Hero's headline; the CTA's label
    when overridden) → CMS
  - Layout composition (page-level structure) → CMS (with DS
    components as the composable units)
  - Localisation variants → CMS (for editorial); content-token
    catalogue (per 04) for templated
- **Scoping implications.** The boundary determines who owns what
  at the instance level; the practice's discipline is to name the
  boundary in the SOW. Without explicit naming, the boundary
  drifts during the engagement (typically toward CMS-instance-as-
  presentation, which collapses the DS's structural authority).

6. MCP / AI-readability for CMS-managed components

- The case. Per 30 §MCP and 34 §5 — the AI-readability registry
  exposes structured component contracts to AI clients. When
  components are authored *and stored* in the CMS, the `.ai.json`
  registry must source from the CMS too. This is a natural extension
  of 30's pipeline; not yet articulated for CMS-managed components.
- **Per-CMS feasibility.** **Contentful** — GraphQL surface is
  closest to MCP-ready; an MCP wrapper around the Delivery API +
  Content Model API exposes both content-instance shape and
  content-type schema; relatively low-effort wrapping. **Sanity**
  — GROQ + GraphQL surface; Studio's schema definitions are in
  TypeScript and AI-parseable; MCP wrapping is straightforward.
  **Strapi** — REST + GraphQL with admin-API; self-hosted means
  the agency can ship the MCP wrapper alongside the Strapi
  deployment. **Sitecore XM Cloud** — Edge GraphQL is API-shaped
  but Sitecore's tooling around Code Connect / MCP is custom
  per project. **WordPress** — WPGraphQL provides the API; an
  MCP wrapper is feasible but not native; Faust.js may eventually
  ship MCP support (verify per release). **AEM** — Sling Model
  Exporter (.model.json) is the closest API surface; MCP wrapping
  is custom and non-trivial because the JCR content tree is
  genuinely different from a flat content-model API. **Salesforce
  Page Designer** — B2C Commerce API surfaces are vendor-specific;
  no MCP-native support as of mid-2026; custom wrapping is
  typically out of scope for SFCC engagements due to platform
  vendor-lock-in concerns.
- **The bet.** CMS-vendor-native MCP support lands in 2026–2027
  alongside the design-token-vendor MCP per 34 §5. Contentful and
  Sanity are the most likely first movers (their AI-readiness
  pressure is most direct; their APIs are closest to MCP shape).
  Strapi may follow via the open-source community. Sitecore,
  WordPress, AEM, and SFCC are likely 2027–2028 timeframe.
- **The practice's bridge investment.** Custom MCP wrappers per
  CMS, per engagement. Typical scope: 16–40 hours per CMS for the
  MCP wrapping work; amortises across engagements that ship to
  the same CMS. The wrapper exposes content-type schema +
  content-instance retrieval + DS-component contract (joined
  from the DS code side). The seven-tool conceptual surface from
  15 (`list_components`, `get_component`, etc.) extends to
  CMS-managed components with additional tools:
  `list_content_types`, `get_content_type`, `query_entries`,
  `get_entry`. The combined surface lets AI clients reason
  about *what components exist* AND *what content fills them per
  instance*.
- **The CMS-as-DS-source pattern.** A specific case the practice
  should articulate: when the CMS itself is the authoring surface
  for the DS's component structure (rare but real — some
  engagements ship a "headless DS" where the components are
  authored as content types in the CMS rather than as code).
  This is the extreme case of CMS-vs-DS-authoring-boundary
  collapse; the practice should have a position on when this is
  appropriate (typically: not appropriate, except for thin
  presentation-layer DSes that a non-engineering team needs to
  author).

7. Composable-content patterns

- The 2025–2026 movement. Content-as-data with explicit schemas;
  sometimes called "headless DS-as-content-source" or "composable
  DXP." The integration story changes: content is not a single
  CMS's output but a *composed* artefact pulled from multiple
  services (CMS + PIM + DAM + commerce + personalization) via a
  unified content layer. Vendors in this space: **Uniform**
  (composable orchestration); **Layer0** (composable edge
  infrastructure); **Vercel's content-platform direction** (the
  Next.js + V0 + Vercel-native composable stack); **Storyblok's
  composable direction** (their pivot from pure headless to
  composable-aware orchestration).
- **What "composable" means architecturally.** Content types are
  defined per service (Contentful for editorial; Salesforce
  Commerce for product; Sanity for marketing; Algolia for
  search); the orchestration layer pulls from each service per
  request and composes the rendered output. The DS sits at the
  rendering layer, consuming the orchestrated content stream
  rather than a single CMS's output. The DS-component contract
  is the same; the integration is per-service.
- **Schema-first authoring.** Each service in the composable
  stack defines its own schema; the orchestration layer
  reconciles. The DS's component contract is the *common
  vocabulary* across the stack — components are the consumers
  of all services' content; the DS's schema defines what each
  component expects regardless of which service supplies the
  content.
- **Composition-at-render.** The orchestration layer composes
  the content per request; the DS components render the
  composition; preview-as-you-author becomes a multi-service
  preview problem (each service's draft state has to be
  reconciled at preview time).
- **The variability-by-design problem applied to content.** Per
  04 §AI-surface enforcement (and 26's residual gap on
  variability-by-design tooling) — the variability-by-design
  problem applies at the composable layer too. The author specifies
  a *space* of possible content compositions; the orchestration
  layer pulls from each service; the rendered output is one
  realisation of that space. The practice's discipline:
  composable content benefits from the same variant-logging /
  eval-driven QA pattern that 27 names for adaptive UI; per-render
  variance is bounded by the schema contract.
- **The boundary between content tokens and composable content.**
  Per 04 §Content as a system layer — content tokens are
  templated content the DS owns; composable content is editorial
  content the orchestration layer composes. Both treat content
  as data; the difference is the authoring surface (DS catalogue
  for tokens; CMS / PIM / DAM for composable content). The two
  coexist in composable architectures: tokens for system-level
  microcopy, composable content for editorial/product/marketing.
- **Practitioner-side scoping.** Composable engagements are the
  most architecturally complex of the four shapes; scope ~1.5–2×
  a comparable headless engagement because the integration
  surface multiplies (each service is a separate integration);
  the orchestration layer is custom (typically; off-the-shelf
  orchestration is starting to ship from Uniform / Vercel but
  not yet mature). For agency clients on composable platforms,
  the DS engagement typically lands as one of multiple parallel
  engagements (DS + commerce + content + personalization), each
  with its own discipline.

8. Integration — deepen 10, See also block

- The slot decision committed in this prompt. The synthesis path
  is **deepen 10, not a new file.** The structural plan:
  - One new framing-altitude H2 lands near the top of 10
    (between §Central problem and §AEM Architecture
    Fundamentals). The H2 covers §1 above — the four CMS
    architectural shapes as a decision tree, with the
    synthesis-ready comparison table. This H2 surfaces the
    mental model the reader navigates the existing platform-
    specific material with.
  - New platform and concept H2 sections append after §Drupal
    but before §DS Delivery Model: NPM Package vs. Embedded.
    Sections: §Headless CMS coverage (covers §2 above — Sitecore
    XM Cloud / Contentful / Sanity / Strapi / Storyblok);
    §WordPress (covers §3); §Salesforce Commerce Cloud Page
    Designer (covers §4); §The CMS-vs-DS authoring boundary
    (covers §5); §MCP / AI-readability for CMS-managed
    components (covers §6); §Composable-content patterns
    (covers §7).
  - The cross-cutting §DS Delivery Model: NPM Package vs.
    Embedded section continues to apply across all platforms
    after the new sections — the principle generalises.
  - The existing §AEM and §Drupal sections stay intact at their
    current positions.
- See also block updates (in the new sections):
  - 03 (the component-library altitude that consumes whichever
    CMS supplies content)
  - 04 §Content as a system layer (the content-token-vs-CMS
    boundary that this run extends to component anatomy)
  - 30 (the AI-readability pipeline; the MCP-server-tooling
    reality that §6 extends to CMS-managed components)
  - 33 (white-label engagements often ship to multiple CMSes
    in the reseller's stack; the per-reseller MCP shape per
    33 §7 generalises)
  - 34 (the workstation MCP stack reads CMS surfaces alongside
    Figma / Storybook)
  - 24 (multi-brand token architectures often ship to multi-CMS
    portfolios)
  - 13 (i18n content lives in CMS for editorial; in content
    tokens for system-level)
  - 17 / 28 (a11y annotations carry through to CMS-rendered
    components)
- Open residual to flag: the four-axis framing (traditional /
  hybrid / headless / composable) may evolve as the field shifts.
  Track quarterly; if a fifth shape emerges (e.g., AI-native CMS
  where content is generated rather than authored), the practice's
  framing extends.

Output format: Structured markdown. Use H2 section headings that match
the eight-section spine above. Synthesize findings — do not list
sources mechanically. Where the field has consensus, state it clearly;
where decisions are context-dependent, provide decision frameworks
rather than declaring a winner. Two synthesis-ready artefacts must
ship: the four-axis CMS architectural decision tree (per §1 — the
comparison table with eight platforms × shape × DS-integration model
× authoring authority × content-storage); the CMS-vs-DS authoring
boundary table (per §5 — what lives where by content type). Flag
where CMS tooling has known gaps (no DTCG-CMS spec; CMS-vendor MCP
not yet native except for Supernova-vs-Contentful-vs-Sanity early
movers; preview-as-you-author varies wildly across headless
platforms; the SFCC Page Designer / Headless Commerce split). Where
claims depend on current state — vendor positioning, platform
versions, MCP support timelines, headless-CMS market share — date
them and note the verification path. Include a references section
linking to primary sources (Sitecore XM Cloud documentation;
Contentful documentation; Sanity documentation; Strapi documentation;
Storyblok documentation; WordPress / Gutenberg / FSE documentation;
Salesforce Commerce Cloud documentation including Page Designer and
PWA Kit; Uniform / Layer0 / Vercel composable documentation; the
practitioner writing on CMS-DS integration — Brad Frost on
WordPress, Nathan Curtis on Sitecore, EightShapes catalogue if it
exists, the JAMstack Conf talks where headless CMS is a topic, the
2025–2026 composable DXP analyst reports — Forrester, Gartner,
Real Story Group).

Depth: Expert audience. Do not explain what GraphQL is, what a JSON
content model is, what Storefront Reference Architecture (SFRA) is
at the basic level, what WordPress Gutenberg is, what Sanity Studio
is, what Sitecore XM Cloud's split from XM is, what an MCP server
is — explain how the practice should *operate* the modern CMS layer
as a discipline at agency scale, where each platform's authoring
model and DS-integration shape constrain the engagement, where the
field's CMS tooling has known gaps that practitioners work around,
what the four CMS architectural shapes mean for scoping decisions,
and how this layer relates to (but does not replace) the AEM /
Drupal coverage that 10 already ships.

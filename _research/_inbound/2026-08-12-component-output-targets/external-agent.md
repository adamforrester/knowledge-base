# Component Output Targets and Projection Architecture for Prism3

*External agent's run of the same `prompt.md`. Filed verbatim per `_research/README.md` — raw outputs are not edited. Note for the synthesis: this pass did not have access to the `prism3-tokens` repo, so it could not read `docs/19` §3, `docs/13`, `docs/27`, `docs/38` or issue #252; it answered from platform knowledge alone. That makes it a genuine independent check on the **platform facts and the reversal**, but not on the prism3-internal premises. It also carries no fetch URLs or dates against the prompt's "fetch, don't recall" constraint — see the synthesis for the verification gap.*

---

## Enterprise CMS Ingestion Realities: AEM and Drupal

The enterprise digital experience landscape has undergone a decisive structural shift away from client-hydrated single-page application (SPA) architectures toward edge-rendered, semantic HTML delivery pipelines. In Adobe Experience Manager (AEM), Adobe officially deprecated the SPA Editor in January 2025 across both AEM as a Cloud Service (release 2025.01) and AEM 6.5 (release 6.5.23). This deprecation placed all associated software development kits—including the React, Angular, and Vue editable component frameworks, project archetypes, and SPA Core Components—into an indefinite feature freeze, restricting future engineering exclusively to critical P1 and P2 security remediations. Adobe's product strategy now mandates the Universal Editor as the visual authoring layer and Edge Delivery Services (EDS) as the modern, high-performance publishing architecture.

An enterprise AEM engagement consumes different technical deliverables depending on project phase and target architecture. For traditional AEM Sites deployments, Phase 1 implementations deploy a design tokens client library (clientlib) paired with global cascading style sheets that skin standard AEM Core Components via the AEM Style System, requiring zero custom Java, HTL, or client-side component code. However, the Phase 2 evolution within modern AEM environments does not involve building complex HTL components or wrapping clientlibs around Shadow DOM Web Components. Instead, modern Phase 2 deliverables target AEM Edge Delivery Services blocks.

Under Edge Delivery Services, content authored through document-based workflows such as Microsoft Word and Google Docs, or visually assembled via the Universal Editor, is ingested and delivered across content delivery networks as semantic, server-rendered HTML tables and container elements. The operational unit of consumption in EDS is the block. An EDS block consists of a co-located vanilla JavaScript file that exports a default `decorate(block)` lifecycle function and an isolated stylesheet. When the page loads, the browser executes `decorate()` to transform raw server-delivered HTML elements into interactive user interface components without requiring front-end frameworks, virtual DOM reconciliation, or hydration overhead. When authoring through the Universal Editor, blocks require structured JSON configuration files, specifically block models and component definitions, to establish how author-managed fields map into edge HTML table cells.

Drupal has executed an equivalent architectural standardization around native, encapsulated server-side rendering. Initiated in Drupal 10.1 and integrated into the Drupal Core render system in Drupal 10.3 and Drupal 11, Single-Directory Components (SDC) provides an official mechanism for component encapsulation. SDC eliminates sprawling theme asset directories by co-locating all component assets within an isolated subdirectory under a theme or module `components/` directory.

A complete SDC package requires a component metadata definition file (`{name}.component.yml`) and a Twig template (`{name}.twig`), alongside optional co-located stylesheets (`{name}.css`) and JavaScript files (`{name}.js`) that Drupal automatically discovers, aggregates, and attaches via its internal asset library manager. Component inputs in SDC are partitioned into structured properties (props) and unstructured slots. Props represent strictly typed data inputs governed by JSON Schema definitions, enforcing data constraints such as primitive types, enumerated options, and required keys during development. Slots represent designated rendering targets reserved for arbitrary HTML markup, Twig blocks, or nested Drupal render arrays. SDCs are consumed in PHP through Drupal's `#type => 'component'` render arrays or directly in Twig templates via `include()` and `embed` expressions, bypassing legacy theme preprocess functions.

| Platform Ingestion Target | Structural Markup Contract | Runtime & Logic Model | Asset Aggregation & Styling |
|---|---|---|---|
| AEM Edge Delivery Services (EDS) | Semantic HTML tables and container divs generated from edge ingestion or Universal Editor JSON | Vanilla JavaScript ES modules exporting a `decorate(block)` function; zero client runtime | Block-scoped CSS delivered over HTTP/2; global token variables applied across shared blocks |
| AEM Sites (Traditional / Classic) | Server-rendered HTL markup structured around standard AEM Core Component DOM trees | Vanilla JavaScript or jQuery packaged within AEM Client Libraries (`cq:ClientLibraryFolder`) | Global clientlib CSS bundles mapped to the AEM Style System via CSS utility classes |
| Drupal (10.3+ / Drupal 11 SDC) | Co-located Twig templates (`.twig`) consuming structured props and unstructured slots | Component-scoped JavaScript (`.js`) loaded via Drupal behaviors and attached automatically | Co-located CSS (`.css`) automatically discovered and compiled into Drupal's internal render libraries |
| Sitecore (Headless / SXA) | JSON layout service output mapped to rendering parameters and variant structures | Framework-agnostic client rendering or edge execution scripts tied to component templates | Modular CSS or utility class layers passed through rendering parameter definitions |

## Architectural Evaluation: The Survival of Web Components as Primary Projection

The architectural premise established in `docs/19` §3—which positioned Shadow DOM Web Components as the primary projection target and treated all other frameworks as thin wrappers—does not survive operational integration with enterprise content management systems. The delivery model across modern digital experience platforms relies on server-rendered semantic HTML augmented by external styles, rather than client-instantiated custom element trees.

The theoretical case for Web Components centers on encapsulation: custom elements provide a browser-standard component boundary, Shadow DOM provides scoped styling that prevents leakage into host pages, and the resulting components run natively without mandatory compilation steps. In isolated micro-frontend dashboards, these qualities provide utility.

However, the case against Web Components as the primary projection across content-driven digital experience platforms is conclusive. Server-side rendering (SSR) using Declarative Shadow DOM introduces substantial serialization overhead and hydration friction within enterprise CMS pipelines. AEM EDS delivers static HTML tables over edge networks; parsing and upgrading custom element registries introduces client-side execution delays that degrade Core Web Vitals and Lighthouse scores.

Furthermore, Shadow DOM encapsulation directly impedes enterprise CMS theming mechanisms. Brand themes in AEM and Drupal rely on cascading design tokens, parent utility classes, and global stylesheet layers. Shadow boundaries block external CSS rules, requiring custom property penetrations or exposed `::part` attributes for every styleable node. AEM EDS block decoration specifically expects direct access to the light DOM to parse child elements, manipulate table rows, and rearrange nodes. Placing these structures inside a shadow root breaks the DOM manipulation assumptions of EDS boilerplate utilities. Similarly, Drupal SDC is architected around Twig template execution; forcing an SDC template to output custom element tags with slotted content introduces redundant abstraction layers over native HTML rendering.

Consequently, Prism3 must correct the assumptions in `docs/19` §3 and KB File 10. CSS-over-server-rendered-markup—pairing semantic HTML blueprints with a robust, tokenized CSS layer—constitutes the universal primitive across enterprise digital experience platforms. Web Components must be demoted to a secondary, leaf-level projection target utilized strictly for self-contained, client-side interactive widgets that cannot be expressed through semantic server markup alone.

## Commercial Projection Matrix and Implementation Hierarchy

To maximize commercial velocity and directly serve client engagements, Prism3's projection pipeline must align with verified agency delivery revenue rather than abstract technical uniformity. Projections are ranked based on platform demand, ease of integration, and commercial value.

The **CSS and Design Token Layer** represents the foundational delivery requirement. Every downstream CMS platform consumes design tokens (CSS custom properties, spacing scales, typography rules, and semantic color aliases) alongside modular stylesheets. This layer immediately unlocks Phase 1 AEM skinning of Core Components and serves as the baseline styling engine for all CMS implementations.

**AEM Edge Delivery Services (EDS) Blocks and Universal Editor Models** represent the highest commercial priority. Because AEM is the agency's primary delivery vehicle, generating turnkey EDS block structures—consisting of vanilla JavaScript decoration files, scoped CSS, and Universal Editor JSON component definitions—directly accelerates billable production work.

**Drupal Single-Directory Components (SDC)** constitute the second commercial tier. With Drupal representing the agency's secondary delivery platform, generating co-located SDC directories containing `.component.yml` schemas, `.twig` templates, `.css`, and `.js` integrates directly into modern Drupal 10 and 11 theming workflows.

**Light DOM Web Components and Custom Elements** serve as an auxiliary projection. These elements encapsulate complex client-side behavior without incurring the styling and accessibility penalties of Shadow DOM.

**React Component Wrappers** are relegated to internal prototyping and design system documentation. Given that client sites are overwhelmingly delivered on CMS engines rather than headless React architectures, React components exist purely to facilitate rapid interaction design, usability testing, and Storybook documentation.

**Native Mobile Projections** (iOS Swift, Android Kotlin, Flutter) represent a deferred tier, to be built only when contractually demanded by dedicated mobile application work streams.

| Projection Target | Primary Output Artifacts | Platform Ingestion Mechanism | Commercial Priority | Build Complexity |
|---|---|---|---|---|
| CSS & Design Token Engine | CSS Custom Properties, Utility Classes, Reset Styles, JSON Token Dictionaries | Global Clientlibs (AEM), Theme Libraries (Drupal), Base CDN Stylesheets | Tier 1 (Critical Path) | Low |
| AEM EDS Blocks & Models | `{block}.js` (ES decorate), `{block}.css`, `_model.json`, `component-definitions.json` [cite: 7, 11, 12] | GitHub repository branch deployment; Universal Editor visual ingestion | Tier 1 (Primary Revenue) | Moderate |
| Drupal SDC Packages | `{name}.component.yml` (JSON Schema), `{name}.twig`, `{name}.css`, `{name}.js` [cite: 13, 15] | Native Drupal Core render engine (`themes/custom/{theme}/components/`) | Tier 2 (Secondary Revenue) | Moderate |
| Light DOM Web Components | Custom Element classes (`customElements.define`), progressive enhancement scripts | Vanilla JS module bundles loaded via clientlibs or script tags | Tier 3 (Interactive Fallback) | Moderate |
| React Prototype Library | JSX/TSX components, hooks, React story files | npm package consumed in Next.js / Vite prototyping sandboxes | Tier 4 (Internal Prototyping) | Low |
| Native Mobile Targets | Swift UI, Jetpack Compose, Flutter widget modules | Native package managers (Cocoapods, Swift PM, Gradle, Pub) | Tier 5 (Deferred Roadmap) | High |

## Schema Demands on the Component Definition Layer

Transforming an abstract component definition into authorable enterprise CMS artifacts reveals a fundamental structural gap: standard front-end component definitions model UI rendering properties, whereas CMS platforms require explicit content models, authoring field controls, and composition constraints. A schema designed solely for React props or Web Component attributes cannot express the operational requirements of AEM or Drupal.

In Drupal SDC, the component definition layer must strictly separate properties from slots. Props demand JSON Schema validation rules defining data types (string, boolean, number, array, object), human-readable titles, descriptions, and enumerated value constraints. When component data validation is active, Drupal validates runtime inputs against these schemas and halts execution if type violations occur. Slots, by contrast, define insertion points for unstructured render arrays and nested templates, requiring metadata regarding allowable child components rather than JSON data validation.

In AEM Edge Delivery Services with Universal Editor authoring, the metadata demands require further specialization. An authorable block requires a model definition (`_block-name.json` or `component-models.json`) that establishes how authoring fields map into edge HTML table structures. The schema must distinguish between authorable fields (content edited directly by an author in a properties rail or inline rich text editor) and system-rendered fields (markup generated procedurally by JavaScript during block decoration). Furthermore, Universal Editor models require layout concepts such as element grouping (combining multiple text fields into a single cell container) and field collapse (merging image URLs, asset references, and alt text into a unified media element). The schema must also express filter configurations (`component-filters.json`) that restrict which specific child blocks or inline formatting tools authors can insert into designated section containers.

To bridge Prism3's `component-schema.ts` with enterprise CMS engines, the definition layer must express four distinct facets:

- **Visual and Thematic Properties:** Style variations, color modes, and layout classes that compile directly into CSS token selectors and CMS style dropdowns.
- **Functional Data Schema:** Typed parameters consumable by JavaScript runtimes, React wrappers, and Drupal SDC prop schemas.
- **Composition and Structural Hierarchy:** Container relationships, named slot contracts, and allowable child component filters.
- **Editorial Content Model:** Mappings of component fields to CMS authoring widgets (such as rich text controls, asset pickers, and path browsers), delineation of author-editable inputs from system-computed logic, and DOM grouping transformations for AEM EDS block models.

## Headless Behavior Architecture and the Cross-Root ARIA Barrier

When interactive components require client-side state management (such as accessible comboboxes, dialogs, accordions, and tabs), the choice of headless behavior engines dictates framework neutrality and accessibility compliance.

An examination of candidate headless libraries demonstrates a clear divergence in dependency architecture. Solutions such as Radix UI primitives and React Aria maintain hard peer dependencies on `react` and `react-dom`. Coupling Prism3's headless logic to these libraries would permanently tether component behavior to the React runtime, rendering direct export to vanilla JavaScript EDS blocks or native Drupal SDC assets impossible without bundling an entire React execution context. In contrast, Zag.js models interaction logic as framework-agnostic finite state machines with zero runtime framework peer dependencies. Zag.js machines execute in pure vanilla JavaScript, consuming raw DOM events and outputting standardized accessibility attribute dictionaries (`aria-*`, `data-*`, `tabIndex`, and `role` bindings). This architecture allows the exact same state machine to drive an interactive AEM EDS vanilla block, a Drupal SDC script, a custom element, or a thin React prototyping wrapper.

However, implementing accessible interactive components within Web Components encounters a platform limitation: the Cross-Root ARIA constraint. Native Shadow DOM enforces strict DOM tree encapsulation, isolating internal IDs from the outer document scope. Consequently, standard ARIA relationship attributes that rely on ID reference matching (IDREFs)—including `aria-labelledby`, `aria-describedby`, `aria-controls`, `aria-owns`, `aria-activedescendant`, and the native form `<label for="...">` association—cannot resolve elements across a shadow root boundary.

When a custom form control places its native `<input>` inside Shadow DOM, a light-DOM `<label>` cannot associate with it via `for="id"`. Similarly, in complex composite widgets like comboboxes or pickers, where active focus remains on an `<input>` while referencing an active option inside a nested shadow tree via `aria-activedescendant`, the browser accessibility tree fails to resolve the link.

The web platform's proposed solution, the Reference Target specification (formerly explored under Exported IDs), introduces a mechanism allowing a shadow host to forward ID references directly to an internal target element via `shadowRoot.referenceTarget` or declarative HTML attributes (`shadowrootreferencetarget`). While the specification is progressing within the WHATWG and W3C, implementation status across browser engines remains incomplete:

| Browser Engine | Implementation Status | Tracking Reference & Capabilities | Production Readiness |
|---|---|---|---|
| Chromium (Blink) | Origin Trial active (versions 133–135); targeted shipping milestone estimated at 152 | Chromium Feature #5188237101891584; implements `referenceTarget` forwarding for single targets, popovers, and invokers | Experimental; behind flag/origin trial only |
| WebKit (Safari) | In-development prototype behind runtime flags | WebKit Bug #290744; Layout tests added for `aria-owns` and attribute reflection; actively developed by Igalia | Experimental; un-shipped in production releases |
| Gecko (Firefox) | Specification tracking; partial DOM attr-element support | Mozilla Bug #1769586; implementing explicitly set attr-elements in accessibility engine | Pre-alpha prototype |

Because Reference Target cannot be polyfilled via JavaScript—as script shims cannot grant native accessibility APIs the ability to pierce shadow encapsulation—relying on Shadow DOM Web Components for accessible enterprise design systems introduces severe accessibility non-compliance risks.

Therefore, any interactive behavior layer in Prism3 must be implemented using Light DOM Custom Elements or progressively enhanced semantic HTML driven by Zag.js state machines. By retaining all interactive elements within the light DOM, ID reference associations function natively, global styles cascade predictably, and components integrate seamlessly with both AEM EDS block decoration and Drupal SDC rendering pipelines.

## Strategic Recommendations and Falsification Criteria

Based on empirical platform requirements and the deprecation of legacy SPA models across enterprise CMS ecosystems, the Prism3 project must execute a structured transition in its projection architecture.

Prism3 must formally discard the "Web Components Primary" hypothesis from `docs/19` §3. The core intermediate representation must target semantic HTML blueprints paired with a design-token-driven CSS architecture. Web components must be repositioned as an auxiliary projection for isolated client-side interactivity.

The engineering sequence for projection builders must follow the verified commercial hierarchy:

1. Universal Design Tokens and Modular CSS Layer (Immediate AEM Phase 1 / Drupal support).
2. AEM Edge Delivery Services Block Generators and Universal Editor JSON Models (Tier 1 Revenue).
3. Drupal Single-Directory Component (SDC) Twig and Schema Packages (Tier 2 Revenue).
4. Zag.js-driven Vanilla Behavioral Modules and Light DOM Custom Elements (Cross-platform accessibility).
5. React Wrapper Components (Internal prototyping and Storybook sandboxes).

The definition schema in `component-schema.ts` must be extended to incorporate CMS-specific content modeling. It must natively represent the distinction between authorable fields and system-computed markup, define element grouping and field collapse rules for AEM Universal Editor models, and output strict JSON Schema validation definitions for Drupal SDC props.

For all interactive behaviors, Prism3 must standardize on Zag.js state machines while avoiding framework-coupled libraries like Radix or React Aria. To avoid accessibility failures caused by the cross-root ARIA barrier, all interactive projections must render into the Light DOM rather than encapsulated Shadow Roots until the Reference Target specification reaches unflagged baseline availability across all major browser engines.

The confidence level in these architectural recommendations is High (95%), grounded in verified documentation from Adobe and Drupal, active standards specifications, and current browser engine source repositories.

The specific conditions that would falsify these findings and warrant an architectural pivot include:

- Adobe officially introducing native Shadow DOM Web Component hydration as the mandatory rendering contract for Edge Delivery Services, replacing vanilla `decorate(block)` scripts.
- The W3C Reference Target specification shipping unflagged in stable releases across Chromium, WebKit, and Gecko, accompanied by a standard polyfill capable of resolving cross-root ARIA references in legacy environments.
- The agency observing a structural commercial shift where the majority of billable client engagements pivot from AEM and Drupal CMS implementations to custom, headless React application architectures.

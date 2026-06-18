# The Semantic Region: Architecting the Section Component

## 1. Framing
Within the taxonomy of a mature design system, the Section component represents the definitive semantic boundary. It acts as the fifth and final brief in the layout category, closing the continuum that begins with foundational primitives like Box and structural distributors like Stack and Grid. While the Card component defines a visually bounded, in-flow object characterized by surface chrome, elevation, and boundary radii, the Section operates as its semantic counterpart. A Section is a meaning-bearing document region, fundamentally defined by its landmark status and its heading-level contract, and it typically possesses no default visual chrome.

The industry demonstrates significant divergence in how this primitive is modeled, a fragmentation largely driven by a historical conflation of semantics and visual layout. Systems frequently fail to untangle the "Semantic Section" (a document structure concern mapping to accessibility landmarks and the accessibility tree) from the "Visual Section" (a layout concern mapping to edge-to-edge background bands and constrained-width content columns). This divergence results in systems either shipping purely visual Container components while ignoring semantic contracts entirely, or over-engineering semantic wrappers that result in accessibility tree noise and landmark fatigue for assistive technology users.

The practice's opinionated default requires drawing strict, unambiguous boundaries. The Section stands squarely on the polymorphic Box substrate, inheriting zero-runtime delivery, bidirectional logical properties, and spatial token scales. However, unlike Box, which is semantically null and invisible to the accessibility tree, the Section is responsible for the document outline. The defining tension of this component lies in two often-misunderstood web platform realities: the nameless-section landmark contract and the myth of the HTML5 document outline algorithm. A <section> element without an explicitly defined accessible name provides absolutely zero landmark value to assistive technologies, degrading gracefully but uselessly into a generic container. Furthermore, browsers never implemented the automatic calculation of heading levels promised by early HTML5 drafts. Therefore, a robust Section component must enforce manual or context-driven heading levels and strictly police its own accessible naming to earn its place in the document object model's accessibility tree.

## 2. Anatomy and Parts
The anatomy of a Section is fundamentally structural, composed of semantic nodes and layout boundaries rather than visual pixels. By default, it introduces no background colors, borders, or surface shadows, standing in stark contrast to the object-oriented nature of the Card component.

The component consists of three primary anatomical regions that govern its semantic and spatial behavior:

The Sectioning Element (Root): The rendered HTML tag, which defaults to <section> but must polymorphically adapt to <article>, <aside>, <nav>, or <div> based on the specific document context and the developer's intent. This root element acts as the container for both the layout and the ARIA attributes required for landmark synthesis.

The Section Header (Slot): The crucial semantic anchor of the component. This slot consists of a mandatory heading (which provides the accessible name for the region), an optional description string for supplementary context, and optional section-level actions (e.g., "View All," "Edit Settings," or "Manage"). The header acts as the programmatic label for the landmark, ensuring that screen reader users can identify the region's purpose before navigating into its body.

The Body (Slot): The primary content area, almost universally composed of a Stack (for vertical flow of disparate elements) or a Grid (hosting a matrix of Card objects or data tables). The body is entirely agnostic to its children but manages the spatial relationship between the header and the content payload.

In marketing layouts, editorial pages, or high-density dashboards, an optional Visual Variant introduces two additional anatomical concepts that bridge the gap between semantics and presentation:

The Full-Bleed Background: A surface treatment that ignores standard parent container padding and stretches edge-to-edge across the viewport. This is often used for alternating background colors in landing pages or applying expansive hero imagery behind constrained text.

The Constrained Content Column: An inner boundary that arrests the horizontal expansion of the header and body content, maintaining a maximum optimal reading width. This inner track ensures that typography does not exceed ergonomic reading lengths (typically 60 to 80 characters) and prevents UI elements from drifting too far apart on ultrawide displays.

## 3. Properties / API
The API of the Section component is designed to enforce accessibility invariants while providing the necessary layout flexibility required by product engineering teams. The following table delineates the standard properties, their types, and their systemic purpose.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| as | Enum | 'section' | The polymorphic HTML element defining the semantic wrapper. Accepts section, article, aside, div, or main. |
| title | String \| ReactNode | undefined | The human-readable string rendered in the Section Header. The component automatically generates a unique ID for this node and wires it to the root element's aria-labelledby attribute. |
| aria-label | String | undefined | An invisible accessible name. Required if title is omitted but the landmark is still semantically necessary for document navigation. |
| headingLevel | 1 \| 2 \| 3 \| 4 \| 5 \| 6 | Context-derived | The explicit rank of the section's heading. Overrides the auto-incrementing React Context if manual control is explicitly required by the developer. |
| variant | Enum | 'plain' | Controls the visual rendering behavior. Accepts plain (default flow) or full-bleed (viewport-spanning background with constrained inner track). |
| maxWidth | Token | 'auto' | Constrains the inner body content. Often mapped to design system width tokens (e.g., sm, md, lg) or character limits (60ch) to ensure typographic legibility. |
| padding | Token | 'none' | Inherited from the Box substrate. Controls the block and inline spacing within the region, ensuring adherence to the system's spatial rhythm. |
| actions | ReactNode | undefined | A dedicated slot for rendering interactive elements (buttons, links, menus) in the section header, typically aligned to the inline-end opposite the title. |

## 4. States and Variants
The Section component contains no interaction states (e.g., hover, focus, active, disabled), as it functions entirely as a structural and semantic wrapper rather than a user interface control. Its variants are strictly divided across two distinct axes: the semantic axis governing the accessibility tree, and the visual axis governing the render tree.

### Semantic Variants
The semantic variant modifies the structural meaning of the node in the accessibility tree, governed primarily by the polymorphic as prop and its corresponding ARIA role implications:

Region (<section>): A thematic grouping of content. The specification explicitly dictates that a <section> only maps to role="region" when it possesses an accessible name. Without a name, it remains a generic container. This variant is the default for named, distinct areas of a page.

Independent (<article>): A self-contained, syndicatable composition. The content within an <article> should make sense independently of the rest of the site (e.g., a forum post, a magazine article, a discrete comment). Like regions, it requires careful naming if it is to be treated as a navigable landmark.

Complementary (<aside>): Tangential content that supports the main document but is not part of the primary flow. When an <aside> is given an accessible name, it automatically maps to role="complementary", creating a specific landmark designed for sidebars, callout boxes, and related metadata.

Generic (<div>): Used when the layout requires a constrained container or full-bleed band for styling purposes, but the content does not warrant a distinct entry in the accessibility tree's landmark list. This prevents landmark noise.

### Visual Variants
The visual variations of the Section address the recurring need to manage content width and background treatments in responsive design:

Plain (Default): The component applies no background styling and allows its content to flow naturally according to the parent container's layout rules. It operates purely as a semantic boundary.

Full-Bleed Band: Applies a background color, gradient, or image that breaks out of parent constraints to touch the viewport edges on the inline axis, while simultaneously keeping the inner content centered and constrained to a maximum width. This is the foundational pattern for modern marketing pages and editorial layouts.

Constrained (Container): Acts purely as a max-width wrapper, mirroring the traditional behavior of the Bootstrap .container or Material UI <Container>. It restricts the content to an optimal width and centers it using auto-margins, without applying background styling.

## 5. Usage Guidance
A recurring systemic failure in product codebases is the over-application of the <section> element. Developers frequently equate "visual grouping" with "semantic section," mistakenly assuming that wrapping every distinct visual module in a <section> tag improves accessibility. In reality, this degrades the experience for assistive technology users by flooding the landmark rotor with trivial nodes.

The Decision Tree for Layout vs. Semantics:
The determination of whether to use a Section, a Card, or a simple Box relies on understanding the element's role in the user's mental model:

Is this a visually bounded object inside a flow? Use Card. Card is for discrete items representing a single entity (e.g., a dashboard widget, a product tile, an individual task). Cards are objects; Sections are the environments that contain those objects.

Does this content represent a major navigable region of the document? Use Section. The region must be important enough that a screen reader user would explicitly want to jump to it via a landmark shortcut. If the section contains a thematic shift and a distinct heading (e.g., "Billing History," "Security Settings"), it merits a Section.

Is this just a layout wrapper for spacing, flexbox alignment, or background color? Use Box (which defaults to rendering as a <div>). Do not use <section> simply to apply padding or a background token.

The Don't-Over-Landmark Rule:
Every time a valid, named Section is rendered, it is appended to the page's landmark navigation list. Consider a marketing page featuring a grid of twelve product benefits. Wrapping each of the twelve benefits in a named <section> creates twelve distinct landmarks. This constitutes severe "landmark noise," forcing a screen reader user to wade through a cluttered index just to navigate the page. The correct, inclusive structure is a single semantic <section> (named "Product Benefits") containing a Grid of twelve semantically generic <div>s or Cards.

When engineering marketing pages, the Visual Section (the full-bleed band) is frequently required to visually alternate content. However, if a background band does not represent a thematic shift in the document outline, the component must be explicitly configured to render as a <div> (as="div"). This decouples the visual presentation of a full-bleed band from the semantic weight of a landmark region.

## 6. Accessibility
The accessibility architecture of the Section component is defined by two absolute platform truths that are frequently misunderstood by practitioners: the nameless-section rule and the heading-level contract. Failure to adhere to these rules results in interfaces that are theoretically semantic in code, but functionally broken in assistive technologies.

### The Nameless-Section / Landmark Contract
In the W3C HTML Accessibility API Mappings (HTML-AAM), the <section> element does not automatically map to the region landmark role. A <section> without an accessible name is explicitly exposed to the accessibility tree as role="generic"—making it functionally identical to a standard <div>.

To elevate a <section> to a landmark, it must earn its status via an accessible name. A strict Section component automates this contract to prevent authoring errors. When a title prop is passed to the component, the internal logic generates a unique DOM ID for the rendered heading element and wires it to the <section> wrapper via the aria-labelledby attribute.

If a design calls for a landmark region but explicitly omits a visible heading, the component API must enforce the use of the aria-label attribute. If neither a title nor an ARIA label is provided, an opinionated design system will gracefully degrade the element to render as a <div>, or alternatively, throw a development-time console warning to prevent the silent deployment of empty, non-functional landmarks.

### The Heading-Level Contract and the Document Outline Algorithm Myth
The most pervasive accessibility myth in modern web development is the persistent belief that HTML5 sectioning elements automatically compute heading levels. The HTML5 specification initially promised a "Document Outline Algorithm" where authors could exclusively use <h1> tags regardless of depth, and the browser would automatically compute their true rank (<h2>, <h3>, <h4>) based on their nesting depth inside <section>, <article>, or <aside> elements.

No browser or assistive technology ever implemented this algorithm. It disrupted established scanning behaviors for screen reader users, who rely heavily on absolute heading ranks to understand document hierarchy, and it was explicitly rejected by browser accessibility vendors. Consequently, the algorithm was officially deprecated and entirely removed from the HTML standard (with final removals taking effect between 2022 and May 2025).

Because the outline algorithm is dead, authoring a flat sea of <h1> tags nested in <section> elements results in a completely broken document outline, violating WCAG Success Criterion 1.3.1 (Info and Relationships) and 2.4.6 (Headings and Labels).

The Section component must solve this. It does so by implementing a Heading-Level Context. Using the React context pattern popularized by accessibility advocates like Heydon Pickering (often referred to as the <H> component pattern or react-headings), a Section acts as a level provider. When a Section is nested inside another Section, it reads the current context depth and increments the integer value. Any heading rendered inside that section reads the context and automatically renders the mathematically correct semantic tag (<h2>, <h3>, <h4>), entirely decoupling the DOM structure from the visual component tree. This ensures programmatic compliance without requiring engineers to manually track heading depth across fragmented React component files.

### Landmark Navigation and Keybindings
Modern implementations of semantic regions often augment native browser behavior. For example, Adobe's React Aria provides the useLandmark hook, which polyfills F6 and Shift+F6 keyboard navigation. This enables power users and screen reader users to rapidly cycle focus directly between registered landmarks (banner, main, region, contentinfo) and restores focus predictably when landmarks dynamically mount and unmount in single-page applications.

## 7. Content Guidelines
The effectiveness of a Section as a navigational aid relies heavily on the quality of its header string, as this string becomes the definitive accessible name for the landmark.

Specific, not generic: Avoid naming sections with generic labels like "Content," "Details," or "More Information." Assistive technology users pull up lists of landmarks out of visual context. Use highly descriptive labels like "Billing History," "Shipping Preferences," or "User Roles".

Do not skip levels: The heading hierarchy within the document must not skip ranks (e.g., jumping from an <h1> directly to an <h3>). The context-driven <H> pattern prevents this programmatic failure by strictly incrementing levels by exactly one.

One H1 per document: While early HTML5 guidance permitted multiple <h1> tags inside discrete sectioning roots, modern standards strictly advise a single <h1> per page, representing the main overarching document title. The Section component's internal headings should therefore begin at <h2> and increment downward.

Don't wrap everything: Paragraphs, lists, and form fields that belong to the main flow do not need to be wrapped in Sections unless they represent a distinct, titled subdivision of the page.

## 8. Motion and Transition
As a semantic layout wrapper, the Section possesses minimal intrinsic motion. It is not an interactive widget and does not require complex state transitions. However, it serves as the primary structural anchor for scroll-based interactions and viewport management.

Scroll-into-view behavior: Sections are the standard targets for internal page navigation (e.g., table of contents links). When routed to via a hash link (#billing-section), the component should support a scroll-margin-top CSS token to account for fixed global headers or sticky navigation bars, ensuring the section title is not occluded by the application shell.

Scroll-snap alignment: In marketing layouts or horizontal carousels, Sections frequently act as the scroll-snap-align: start children within a scroll-snap-type parent container, driving rigid, presentation-style scrolling.

Reduce-motion compliance: Any entrance animations applied to the visual variant of a Section (such as a fade-in-up effect on scroll intersection) must be wrapped in media queries. If the user's operating system requests prefers-reduced-motion, all spatial transitions must resolve to zero duration, allowing the section to appear instantly without layout shifts.

## 9. Internationalization
The Section component inherits its robust internationalization (i18n) capabilities directly from its reliance on the Box substrate and modern CSS specifications.

Logical Properties: Padding, margins, and border assignments rely exclusively on logical CSS properties (padding-inline, padding-block, margin-inline-start) rather than physical directions (left, right, top, bottom). This ensures the Section seamlessly mirrors its internal spacing when rendered in Right-to-Left (RTL) languages such as Arabic or Hebrew.

Header Alignment Mirroring: The flexbox layout governing the Section Header ensures that the primary title sits on the inline-start edge, while optional trailing actions sit on the inline-end edge. This layout automatically reverses in RTL contexts without any manual developer intervention or conditional JavaScript.

Direction-Agnostic Backgrounds: The full-bleed visual variant handles background spans edge-to-edge. Because it relies on CSS Grid tracking rather than explicit left/right negative margins, the breakout pattern remains completely agnostic to reading direction, ensuring background integrity regardless of the locale.

Translated Landmark Names: The title or aria-label provided to the section must be hooked into the application's i18n translation dictionaries, ensuring that the landmark name announced by screen readers matches the user's localized language settings.

## 10. Naming
The naming of this component represents a major architectural divergence across industry systems, reflecting the split between those that prioritize semantics and those that prioritize visual constraints.

| Framework / System | Component Name | Primary Focus | Context & Usage |
| --- | --- | --- | --- |
| Shopify Polaris | Layout.Section / s-section | Structural / Semantic | Uses s-section strictly for card-like groupings with headings, keeping it distinct from the generic s-box. |
| GitHub Primer | PageLayout.Content | App Shell Regions | Rejects a generic "Section" in favor of explicit landmark slots (Header, Pane, Main, Footer) to manage the application shell. |
| Atlassian | PageLayout / Panel | Layout Slots | Uses top-level shell components with defined spatial slots (Banner, LeftSidebar, Main) to ensure consistent app-wide landmarks. |
| MUI (Material UI) | Container | Visual / Width | Ignores semantic sections by default, providing a purely visual wrapper to center and constrain max-width content. |
| Chakra UI | Container | Visual / Width | Provides the Container primitive to constrain widths to breakpoints (e.g., 60ch), optionally allowing as="section". |
| IBM Carbon | Grid (Row / Column) | Structural | Utilizes a strict 2x grid system where semantic sectioning is applied atop row and column boundaries. |

The practice's opinionated default is to name the semantic document region Section, while abstracting the visual width constraint into an entirely separate Container primitive. By composing them (<Section><Container>...</Container></Section>), systems resolve the historical conflation, allowing for semantically sound, full-bleed sections with beautifully constrained inner content tracks.

## 11. Implementation Notes
The implementation of a robust, enterprise-grade Section component requires solving three distinct engineering challenges: the landmark wiring, the heading-level context, and the full-bleed CSS layout.

### Name-to-Landmark Wiring
To ensure the <section> acts as a valid region, the component must automatically associate the heading with the wrapper. Relying on developers to manually type matching IDs is brittle and prone to typos. The component should generate IDs internally using React's useId() hook.

```jsx
const Section = ({ as: Component = 'section', title, children, ariaLabel }) => {
  const sectionId = useId();
  const headingId = title ? `${sectionId}-heading` : undefined;
  return (
    <Component 
      aria-labelledby={headingId} 
      aria-label={!title ? ariaLabel : undefined}
    >
      {title && <H id={headingId}>{title}</H>}
      {children}
    </Component>
  );
};
```

### The Heading-Level Context (<H> Pattern)
To bypass the deprecated and dead document outline algorithm, the Section must establish a React Context that auto-increments the heading level for all deeply nested content.

```jsx
const LevelContext = createContext(1);
export const SectionContext = ({ children }) => {
  const currentLevel = useContext(LevelContext);
  // Cap the level at 6 to prevent generating invalid HTML <h7> tags
  const nextLevel = Math.min(currentLevel + 1, 6); 
  
  return (
    <LevelContext.Provider value={nextLevel}>
      {children}
    </LevelContext.Provider>
  );
};
export const H = ({ children, ...props }) => {
  const level = useContext(LevelContext);
  const Tag = `h${level}`;
  return <Tag {...props}>{children}</Tag>;
};
```

This paradigm guarantees that an engineering team can move an entire Section from the main content area into a deeply nested sidebar or modal dialog, and all internal heading levels will automatically recalculate to remain semantically accurate, requiring zero refactoring of the internal JSX.

### The Full-Bleed Background CSS Pattern
The recurring layout trap in marketing pages is achieving a background color that breaks out of a constrained parent to touch the viewport edges. Legacy methods relied on brittle 100vw calculations combined with negative margins (e.g., margin-left: calc(50% - 50vw)), which famously triggered horizontal scrollbars on Windows operating systems due to the inclusion of the scrollbar in the viewport width calculation.

The modern CSS Grid breakout pattern solves this mathematically and elegantly without scrollbar side-effects.

```css
.section-breakout {
  display: grid;
  /* 
    1. Outer columns (full) absorb infinite space, shrinking to a minimum gap.
    2. Inner columns (content) restrict to the max container width token.
  */
  grid-template-columns:
    [full-start] minmax(var(--page-gutter), 1fr)
    [content-start] minmax(0, var(--max-content-width))
    [content-end] minmax(var(--page-gutter), 1fr)
    [full-end];
}
.section-breakout > * {
  /* Default all children to the constrained center track */
  grid-column: content; 
}
.section-breakout > .full-bleed-background {
  /* Allow the background layer to break out to the edges */
  grid-column: full;
}
```

## 12. Related and Alternative Components
The Section operates within a strict typed relationship ecosystem, interacting directly with both layout primitives and visual objects:

Stands on Box: The Section inherits the Box component's polymorphic asChild slot pattern, spacing token scale, and zero-runtime styling engine. The Section acts as a semantic wrapper around the Box's pure layout capabilities.

Boundary with Card: The boundary between Section and Card is strict. The Card is a visual object characterized by surface styling, elevation, and borders. The Section is a semantic environment. If an element requires a white background, a border-radius, and a drop shadow, it is a Card. If it is an invisible boundary grouping an <h2> and a list of internal links, it is a Section.

Composes Stack / Hosts Grid: The internal content of a Section is almost universally arranged by a Stack (for linear, one-dimensional flow of headers and descriptions) or a Grid (for hosting two-dimensional matrices of Cards).

Landmark Siblings: While Section handles the generic role="region", the broader application shell relies on specific top-level landmarks. Components like PageLayout handle main, banner (header), and contentinfo (footer). The Side Navigation component inherently renders a nav landmark. These components operate as peers in the accessibility tree.

## 13. Field POV Evolution
The architectural philosophy surrounding the Section component has experienced severe paradigm shifts over the last decade, driven by failures in web specifications and evolutions in CSS capabilities.

During the early HTML5 era (circa 2010–2015), the specification's promise of an automatic Document Outline Algorithm led to a proliferation of <section> tags populated exclusively with <h1> elements. Developers assumed browsers would automatically calculate the structural depth. When it became evident that accessibility APIs mapped these as flat, un-nested lists of <h1>s—destroying the navigability of the page for screen reader users—the field underwent a violent correction. Frameworks abandoned the algorithm, forcing a return to strict manual level mapping (h1 through h6).

Simultaneously, the widespread misuse of <section> tags as generic wrappers for styling triggered an epidemic of "landmark noise." Assistive technology users were overwhelmed by dozens of unlabeled regions. The W3C responded by clarifying the HTML Accessibility API Mappings: a <section> required a defined accessible name to graduate from a generic div to a region. This forced mature design systems to integrate automatic aria-labelledby wiring to prevent developer error.

In recent years, the industry consensus has settled on two dominant architectural patterns. First, the adoption of React Context to handle heading-level computation dynamically, effectively building the failed outline algorithm in user-land via components like react-headings. Second, the rise of CSS Grid layout breakouts, which finally allowed design systems to decouple the semantic document tree from the visual full-bleed viewport requirements, ending the reliance on brittle negative margin hacks.

Modern accessibility utilities like React Aria's useLandmark have further elevated expectations, standardizing F6 keyboard navigation across regions and ensuring focus restoration when single-page application routes change. This evolution has solidified the Section as a highly interactive, programmatic anchor rather than a mere semantic HTML tag.

## 14. Framework Versioning Context
The architectural assertions and mechanical definitions detailed in this report rely on the documented state of leading design systems and web specifications. To understand the current ecosystem, it is critical to contextualize the versions and platform states that dictate these rules.

| Framework / Specification | Epoch / Version Context | Architectural State |
| --- | --- | --- |
| W3C HTML & ARIA Specifications | Formalized to May 2025 | The complete removal of the Document Outline Algorithm from the normative HTML standard. The mandate that <section> defaults to role="generic" without an accessible name is solidified in ARIA 1.2/1.3 AAM. |
| Shopify Polaris | API v2025-10 to v2026-04 | Polaris underwent a massive architectural shift, deprecating its React library to ship framework-agnostic Web Components (s-section, s-page). This move escaped framework lock-in and reduced bundle sizes while maintaining semantic integrity. |
| GitHub Primer React | v37.x (Active 2025-2026) | Primer maintains its strict adherence to PageLayout sub-components (Header, Pane, Content) to enforce exact landmark regions, relying on React Context to manage complex application shell layouts. |
| Atlassian Design System | Active 2026 Patterns | Employs a strict three-tier composition model (Core, Platform, App) where layout shells (Banner, LeftSidebar, Main) dictate rigid landmark generation to prevent structural divergence. |
| Adobe React Aria | Active 2026 (useLandmark) | Leads the industry in programmatic landmark interaction, polyfilling F6 keyboard navigation and focus restoration for dynamic single-page applications via the useLandmark hook. |

## 15. Agent-Consumable Schema
```yaml
identity:
  name: Section
  aliases: [Region, Container, Layout.Section]
  category: Layout
  description: A semantic document region that establishes a landmark and heading-level context. The semantic counterpart to the visual Card.
anatomy:
  - root: The sectioning wrapper (polymorphic section/article/aside/div).
  - header: A slot containing the heading (accessible name) and optional actions.
  - body: The content area, typically a Stack or Grid.
api:
  as: Enum (section, article, aside, div)
  title: String (wires to aria-labelledby)
  aria-label: String (fallback for hidden names)
  headingLevel: Integer 1-6 (override for context-driven levels)
  variant: Enum (plain, full-bleed)
  maxWidth: Token (constrains inline width)
accessibility:
  landmarks:
    - Rule: <section> is NOT a landmark without an accessible name. Maps to generic.
    - Rule: Do not over-landmark. Limit regions to primary document segments.
  headings:
    - Rule: HTML5 outline algorithm is dead. Never rely on auto-computed native tags.
    - Contract: Manual control or Context-based auto-incrementing (the <H> pattern).
composition:
  inherits: Box (as/asChild, spacing tokens, logical RTL properties).
  composes: Stack (for header/body flow).
  hosts: Grid, Card (visual objects within the region).
implementation:
  - css_pattern: CSS Grid breakout `minmax` for full-bleed backgrounds with constrained inner content.
  - react_pattern: LevelContext provider wrapping children to increment nested `<Heading>` tags.
notes:
  unverified: Polyfills for F6 landmark navigation (via React Aria useLandmark) may have varying levels of screen-reader interception depending on user-agent configurations.
```

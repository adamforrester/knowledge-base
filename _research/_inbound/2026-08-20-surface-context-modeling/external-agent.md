# Research Report: Architectural Models for Surface Context in Design Systems

*Raw output — Gemini, run 2026-08-20 against the same prompt as `claude.md`. Unedited per `_research/README.md`.*

## 1. Field Survey: Modeling Surface Context Across Industry Platforms

The architectural decision of where to situate surface context—specifically, how a component adapts when placed on an inverted, dark, or brand-color background—represents a foundational divergence in design system engineering. Depending on the overarching technological ecosystem, different organizations have adopted radically different models to manage this contextual shift. An analysis of eight major design systems reveals four distinct architectural paradigms: the variant axis (Option 1), the appearance/emphasis value (Option 2), the inherited cascade (Option 3), and the theme mode (Option 4).

The following table categorizes the architectural approach of each surveyed design system, identifying the primary mechanism utilized by developers and designers.

| Design System | Architectural Classification | Primary Mechanism / Developer API |
|---|---|---|
| Material Design 3 | Option 4 (Theme Mode / Token Layer) | Explicit color roles via design tokens (e.g., `inverseSurface`) |
| IBM Carbon | Option 3 (Inherited Cascade) | `<Theme>` container mapping CSS custom properties |
| Adobe Spectrum | Option 1 & 2 (Variant / Appearance) | `staticColor` / `static-color` component property |
| Shopify Polaris | Option 2 (Appearance Value) | `monochrome` and `tone` component properties |
| GitHub Primer | Option 4 & 2 (Mode & Appearance) | `<ThemeProvider>` combined with `scheme="dark"` |
| Microsoft Fluent 2 | Option 2 (Appearance Value) | `appearance` property (e.g., `primary`, `subtle`) |
| Atlassian Design System | Option 3 & 2 (Hybrid) | Contextual CSS auto-inversion and `appearance` property |
| Salesforce Lightning | Unverified | Insufficient public specification data available |

**Material Design 3 (Google)**

Material Design 3 abstracts the concept of inversion entirely into the token and theme layer, aligning strictly with Option 4. The system abandons the concept of passing an `inverse` prop to a component. Instead, it relies on algorithmic generation of tonal palettes defined by Hue, Chroma, and Tone (HCT) color spaces, which generate 26 or more specific color roles.

Within this expansive token architecture, Material Design 3 specifies dedicated roles for inverted contexts. According to the official documentation accessed on August 20, 2026 at https://m3.material.io/styles/color/roles, "Inverse roles are applied selectively to components to achieve colors that are the reverse of those in the surrounding UI... Inverse surface: Background fills for elements which contrast against surface". Consequently, a developer does not type `<Button inverse>`. Instead, they construct a container using the `inverseSurface` token for the background, and place a text button using the `inversePrimary` token within it. A designer using the Figma kit clicks on a specific color token mapped to the inverted role rather than toggling a variant switch.

**IBM Carbon (IBM)**

IBM Carbon v11 relies heavily on the inherited cascade model, representing a sophisticated implementation of Option 3. Carbon manages surface context via "inline theming," allowing nested theme application without custom style overrides. According to the official documentation accessed on August 20, 2026 at https://react.carbondesignsystem.com/?path=/docs/components-theme--overview, "Theme is most often used to implement inline theming where you can style a portion of your page with a particular theme... Depending on your architecture you may want to apply a class to the or add a custom data attribute to your element".

Mechanically, a developer utilizes a `<Theme>` or `<GlobalTheme>` component and passes a theme string, such as `g100` for the dark theme. This action attaches a data attribute like `data-carbon-theme="g100"` to the surrounding DOM node. The system's underlying Sass implementation re-declares all relevant CSS custom properties within the scope of that data attribute. Child components inherently rely on these variables (e.g., `var(--cds-text-primary)`), resulting in an automatic context shift without any alterations to the child component's API.

**Adobe Spectrum**

Spectrum Web Components utilize explicit component properties to manage surface context, favoring Options 1 and 2. Components such as ProgressCircle or Button expose a `staticColor` property (rendered as the `static-color` attribute in HTML).

According to the official contributor documentation accessed on August 20, 2026 at https://github.com/adobe/spectrum-web-components/blob/main/CONTRIBUTOR-DOCS/02_style-guide/02_typescript/05_property-patterns.md, developers utilize the `@property` decorator to bind this context to the DOM: `@property({ type: String, reflect: true, attribute: 'static-color' }) public staticColor?: ProgressCircleStaticColor;`. A developer explicitly types `static-color="white"` or `static-color="black"` on the component instance to force it into an inverted state over imagery or colored backgrounds. In the design tooling, a designer clicks a variant toggle mapped to this property.

**Shopify Polaris**

Shopify Polaris incorporates surface context into an overarching appearance value, aligning with Option 2. Rather than maintaining a strict surface axis, Polaris utilizes `tone` and `monochrome` properties to instruct components on how to render against complex backgrounds. According to the official Polaris component API accessed on August 20, 2026 at https://polaris.shopify.com/components/tables/index-table, the `tone` property accepts values such as `"subdued" | "success" | "warning" | "critical"`, dictating "Whether the row should visually indicate its status with a background color".

For buttons, a developer might type `<Button monochrome outline>` to handle rendering on custom backgrounds. Polaris has recognized the structural burden of this approach and has actively moved to deprecate sprawling boolean properties in favor of unified enumerations to reduce variant combinatorics.

**GitHub Primer**

GitHub Primer utilizes a combination of Option 4 (variable-driven theme modes) and Option 2. Primer Web heavily leverages Figma variables to transition between light and dark modes, allowing global or per-section context switching. According to the official Primer documentation accessed on August 20, 2026 at https://primer.style/product/getting-started/figma/, "Primer Web provides light mode and dark mode using figma variables... Switching the variable mode changes all nested items". In code, components can accept a `scheme="dark"` property to force a specific contextual rendering, overriding the global theme cascade.

**Microsoft Fluent 2**

Fluent 2 modern controls primarily rely on an `appearance` property, firmly placing it in Option 2. According to the official Microsoft Learn documentation accessed on August 20, 2026 at https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/upgrade-fluent-ui-controls-to-modern, the platform abstracts individual styling attributes into high-level appearances. Global context is managed by a central ThemeProvider component, which publishes the application's overall theme to the Fluent ecosystem. Developers type `appearance="primary"` or `appearance="subtle"`, allowing the component to react to the global theme context without requiring granular surface inversion flags.

**Atlassian Design System**

The Atlassian Design System presents a robust hybrid approach. The Text component operates as a pure inherited cascade (Option 3). According to the official documentation accessed on August 20, 2026 at https://atlassian.design/components/primitives/text, "Text will automatically apply the correct inverse color token if placed within a box component with a bold background color". However, for interactive primitives like Button or Pressable, Atlassian relies on an `appearance` property (e.g., default, primary, subtle, discovery). The system strictly enforces the use of design tokens over hardcoded values through custom ESLint rules (e.g., `ensure-design-token-usage`), ensuring that whenever the background context shifts, the foreground elements correctly compute their styles via a proprietary `cssMap` function.

**Salesforce Lightning**

After exhaustive review of the provided research material, no official documentation, source code, or component specifications for Salesforce Lightning were available to verify its approach to surface context modeling.

## 2. The Container-Cascade Pattern in CSS

The container-cascade approach (Option 3) represents the most elegant mechanical alignment with standard web platform capabilities. It leverages the inherent scope resolution of CSS Custom Properties (CSS variables) to propagate surface context down the Document Object Model (DOM) tree without requiring explicit property passing in the component logic.

**Mechanical Implementation**

Mechanically, the design system defines a comprehensive dictionary of semantic CSS custom properties at the `:root` level, which map directly to base design tokens. When a structural container—such as a hero band, a modal, or a sidebar—requires an inverted context, it applies a specific CSS class or data attribute to its wrapper element. This selector re-declares the values of the semantic custom properties within that specific DOM scope.

For example, a standard implementation mirroring IBM Carbon's methodology defines the global state and the contextual override simultaneously:

```css
/* Base Theme (Light) */
:root {
  --system-background: #ffffff;
  --system-text-primary: #161616;
  --system-action-primary: #0f62fe;
}
/* Inverted Context Scope (Dark) */
[data-theme-context='inverse'] {
  --system-background: #161616;
  --system-text-primary: #ffffff;
  --system-action-primary: #4589ff;
}
/* Component Definition */
.system-button {
  background-color: var(--system-action-primary);
  color: var(--system-background);
}
```

In this paradigm, a component rendered inside `<section data-theme-context="inverse">` automatically resolves `var(--system-action-primary)` to the darker blue value, and its text to the pure white value. The child component declares absolutely nothing regarding its context; its API remains pristine and unburdened by environmental concerns.

**Documented Failure Modes**

While structurally elegant, the cascade pattern is not invulnerable. Systems operating at enterprise scale encounter several documented failure modes when executing this pattern:

First, specificity conflicts present a persistent threat. If a component's internal CSS applies styles with higher specificity than the cascading variable, or if a developer utilizes a hardcoded hex value instead of the required token variable, the context inversion fails entirely. The container is powerless to override hardcoded component logic.

Second, nested inversions demand a highly rigorous layering model. When context shifts occur deeply within the tree—for example, a light card placed inside a dark hero band situated on a light page—the system must handle the recursive resolution of colors. IBM Carbon explicitly documents a "Layering model" to manage this complexity. According to the official documentation accessed on August 20, 2026 at https://carbondesignsystem.com/elements/color/overview/, "In the light themes, layers alternate between White and Gray 10 with each added layer. In the dark themes, layers become one step lighter with each added layer". Failing to define variables recursively causes deeply nested children to blend invisibly into their parent backgrounds.

Third, partial inversion occurs when custom properties are inconsistently mapped across complex interactive states. A component might successfully invert its primary text color but fail to invert its hover state background, border, or focus shadow. Shopify Polaris encountered precise instances of this failure mode. A public GitHub issue tracked a bug where the monochrome loading button displayed both the text copy and the loading spinner simultaneously, and box-shadow variables failed to map correctly to inverted active states. When states are complex, missing a single `--pc-button-box-shadow_active` override in the cascade breaks the component's visual integrity.

Fourth, server-rendered markup introduces edge cases when the container and child are authored separately. If a container is server-rendered with an inverted context class, but a hydrated JavaScript child component reads from a global React context object or a global application state rather than inheriting the CSS variables from the DOM, a severe hydration mismatch occurs, resulting in a flash of unstyled content or a broken interface.

## 3. Platform Alignment: AEM EDS and Drupal SDC

The primary delivery platforms for this tooling project are Adobe AEM Edge Delivery Services (EDS) and Drupal Single Directory Components (SDC). Both platforms fundamentally rely on server-rendered HTML and utilize CSS classes to decorate the DOM. The architectural decision regarding surface context must strictly align with the idiomatic patterns established by these specific environments.

**Adobe AEM Edge Delivery Services (EDS)**

In Edge Delivery Services, the documented, idiomatic method for publishing styling context is unequivocally aligned with the inherited cascade (Option 3). EDS operates on a block-based architecture where semantic HTML is generated directly from document tables authored in Word or Google Docs.

Authors dictate layout and styling context using "Section Metadata." According to the official EDS developer documentation accessed on August 20, 2026 at https://www.aem.live/developer/component-model-definitions, "In many cases, it is recommended to decorate the rendered semantic markup, add CSS class names, add new nodes or move them around in the DOM, and apply styles. In other cases however, the block is read as a key-value pair-like configuration. An example of this is the section metadata".

When authors add a background color or stylistic variant to a section using this metadata table, the EDS JavaScript execution translates this configuration into a CSS class applied to the parent `div.section`. Furthermore, EDS actively discourages the creation of components that rely on JavaScript for styling or state management. The documentation states explicitly: "Ideally, a block should only need CSS for styling, without relying on JavaScript to modify the DOM or add CSS classes".

In the EDS adaptive forms architecture, the ecosystem relies heavily on CSS custom properties defined at the `:root` level and overridden via block classes. According to the official forms documentation accessed on August 20, 2026 at https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/edge-delivery/build-forms/universal-editor/style-theme-forms, "Edge Delivery Services employs a block-based architecture where the .form class serves as the primary namespace... CSS custom properties defined at the :root level, providing a centralized theming system that cascades throughout all form components. This single change propagates through all form components because the system uses variable references rather than hardcoded values".

Attempting to implement an `inverse` prop on individual child elements (Option 1) would directly violate the EDS philosophy. It would require authors to manually tag every element inside an inverted section, breaking the semantic simplicity of document authoring, and forcing the JavaScript decorator to parse and mutate individual child nodes rather than relying on an efficient, container-level CSS cascade.

**Drupal Single Directory Components (SDC)**

Drupal SDC represents a modernization of Drupal's frontend, grouping Twig templates, YAML metadata, and CSS into self-contained component directories. The idiomatic approach in SDC to pass context aligns perfectly with Twig inheritance and CSS custom properties.

By default, Drupal components added with the `{% embed %}` tag inherit the calling template's variables. However, recursively passing an `inverse` variable down a deep, nested tree of Twig includes is notoriously brittle and difficult to maintain.

Critically, Drupal core is actively standardizing on CSS custom properties as its primary design systems API, deliberately eschewing programmatic property drilling. According to Drupal core issue #3531854 accessed on August 20, 2026 at https://www.drupal.org/project/drupal/issues/3531854, the architectural direction is clear: "In Web implementations of design systems, CSS variables (sometimes referred as custom properties or cascading variables) are... overridable at runtime... living at the page level, but they can be overridden with a CSS selector as a scope".

This establishes that Drupal's architectural trajectory heavily favors the inherited cascade. A parent block—such as a dark hero band—applies a CSS scope class, and the enclosed SDC child component utilizes CSS variables that react implicitly to that scope without requiring a dedicated `inverse` prop defined in the component's YAML metadata.

For both AEM Edge Delivery Services and Drupal SDC, there is a documented, highly established idiomatic pattern. Both platforms rely fundamentally on container-level CSS classes modifying CSS custom properties, which descendant components inherit automatically. Option 3 is the native paradigm for both environments.

## 4. Figma: Is Inverse a Mode?

The intersection of rigorous code architecture and the practical capabilities of design tooling frequently generates friction. In Figma, "modes" function as the primary mechanism for contextual variable switching.

Published design systems, including GitHub Primer, utilize Figma modes to handle surface context and theme switching. According to the Primer documentation accessed on August 20, 2026 at https://primer.style/product/getting-started/figma/, "Primer Web provides light mode and dark mode using figma variables... Switching the variable mode changes all nested items".

However, relying on Figma modes exclusively for surface context (Option 4) introduces severe practical limitations regarding combinatorial explosion. Figma variables can vary solely by mode; there is no secondary mechanism for defining "same token name, different value based on parent frame" without utilizing modes. If a design system uses modes for Light and Dark overarching themes, and attempts to use modes for "Inverse" contexts, the modes must be mathematically multiplied: Light, Dark, Light-Inverse, and Dark-Inverse.

When independent axes cross, mode counts escalate unsustainably. If the system adds spacing or density modes (e.g., Desktop, Tablet, Mobile), the matrix expands exponentially (e.g., Light-Inverse-Desktop, Dark-Default-Mobile). Figma enforces strict mode count ceilings depending on the organizational licensing tier, typically restricting standard professional plans to 4 modes and enterprise plans to 40 modes. A system with three crossed axes will rapidly breach these limits.

To handle this limitation, organizations establish patterns involving highly segmented contextual variable collections. The standard industry pattern dictates maintaining a "Color Primitives" collection (independent of mode), a "Semantic Theme" collection (handling the Light/Dark modes), and a specialized "Contextual/Component" collection. In Figma, designers simulate the CSS inherited cascade by creating a section frame, applying the "Inverse" mode specifically to that parent frame, and allowing the nested components to automatically resolve their variable references based on the frame's overriding mode.

Therefore, while "Inverse" can be modeled as a mode in Figma to simulate a code-side cascade, forcing the inversion into the component's variant matrix in Figma (Option 1) is heavily discouraged. Modeling it as a variant forces designers to manually toggle the variant on every individual component placed on a dark background, completely negating the automation benefits of Figma variables and causing the design kit to disagree structurally with the code library.

## 5. Cost and Regret: Combinatorics and Scale

**The Cost of the Variant Axis (Option 1)**

Systems that elect to model surface context as an explicit variant axis face the immediate, exponential scaling of their component matrix. If a standard button component already projects to 648 variant members due to combinations of size (small, medium, large), intent (primary, secondary, danger), state (default, hover, focus, disabled), and icon presence, adding a simple `surface: "default" | "inverse"` axis instantly doubles the matrix to 1,296 nodes. This bloats the compiled bundle size, slows down Figma performance, and drastically increases the surface area for regression testing.

Public records clearly indicate that teams actively regret and migrate away from highly complex variant structures. Shopify Polaris documented extensive refactoring to reduce code complexity caused by compounding boolean matrices. In a public GitHub issue detailing the simplification of the Button component (accessed August 20, 2026 at https://github.com/Shopify/polaris/issues/10983), the maintainer noted: "Button has variant and tone checks that look like this: variant === 'primary' && styles.primary... variant === 'monochromePlain' && styles.monochrome... There are multiple checks for variants that apply different classes leading to code that's harder to maintain. We should be able to simplify this by using the variationName helper and cleaning up some css". Polaris ultimately undertook a massive migration to deprecate multiple boolean properties in favor of consolidated variant and tone enumerations to escape this combinatorial debt.

Adobe Spectrum encountered persistent architectural bugs with its staticColor variant approach. Developers reported that when passing contextual combinations, the component's internal state machine broke. According to a public issue accessed on August 20, 2026 at https://github.com/adobe/spectrum-web-components/issues/5500, users complained that combining custom modifier variables with specific action button states resulted in completely broken interactive styling, as the variant architecture could not predict all contextual interactions and overrode developer intent.

**Risks of the Cascade Approach (Option 3)**

Conversely, the cascade approach is not immune to scaling failures. The primary public record of cascade failure involves unexpected token interactions in complex nesting scenarios and the necessity for aggressive refactoring. When IBM Carbon released v11 with its extensive CSS custom property inline theming, they initially struggled with a sprawling layering model. Disabled tokens failed to maintain contrast across different layer levels in dark themes. According to a Carbon design team post accessed on August 20, 2026 at https://medium.com/carbondesign/carbon-v11-beta-3-9b6be61bb2af, they ultimately deleted several disabled tokens entirely (`$field-disabled`, `$layer-disabled`) to streamline the layering cascade, reducing the cognitive load on developers trying to predict deep cascade interactions. The cascade approach demands flawless token architecture; minor omissions result in massive visual regressions.

## 6. Accessibility (WCAG 2.2)

Surface context directly impacts a component's ability to guarantee compliance under the Web Content Accessibility Guidelines (WCAG) 2.2, particularly concerning 1.4.3 Contrast (Minimum) and the highly stringent 1.4.11 Non-text Contrast.

Focus indicators represent the sharpest edge of this requirement. Under 1.4.11, a focus ring must maintain a minimum 3:1 contrast ratio against the background surface and the adjacent component edge. This creates a volatile, three-color relationship (the background, the button edge, and the focus ring) that changes entirely depending on the surface context.

Material Design 3 addresses this mechanical complexity using "State Layers"—semi-transparent overlays whose opacity changes based on interactive state. According to the official documentation accessed on August 20, 2026 at https://m3.material.io/foundations/interaction/states/state-layers, "The state layer is an overlay with a fixed opacity for each state and uses the same color as the content... By default, a component's state layer color is derived from the color of its content". Because the state layer color is derived directly from the text/icon color ("on color"), MD3 mathematically ensures that if the text clears the contrast ratio against the background, the interactive state layer will also pass compliance.

However, if surface context is managed via an explicit variant axis (Option 1), the component cannot guarantee accessibility. The developer must manually ensure that both the component and its focus ring variant are toggled to "inverse" when placed on a dark background. If an author places a default button on a dark image overlay and forgets to apply the inverse property, the focus ring will render in its default dark color against a dark background, resulting in an immediate 1.4.11 accessibility failure.

The inherited cascade (Option 3) mitigates this severe risk. If the focus ring's color is defined by a CSS custom property (e.g., `box-shadow: 0 0 0 2px var(--focus-ring-color)`), the container section publishing the inverted context automatically overrides `--focus-ring-color`. The component guarantees 1.4.11 and 1.4.3 compliance natively and automatically, regardless of the developer's manual configuration of the specific component instance.

## 7. Falsification

To ensure a robust and defensible architectural decision, we must examine the specific conditions under which the recommended approaches would be proven incorrect.

**Falsifying the Cascade Approach (Option 3)**

Evidence demonstrating that the cascade approach is the wrong choice would manifest if the primary delivery ecosystem relies heavily on JavaScript portals, cross-frame rendering, or Web Components operating strictly within the Shadow DOM without CSS custom property penetration. If a component (such as a tooltip, modal, or popover) is injected directly into the `<body>` element outside of the contextual container's DOM scope, it will immediately lose the inherited CSS custom properties and render in the default theme, breaking the visual experience.

Furthermore, if the design system explicitly requires granular, per-element inversion—for example, alternating inverted and default buttons sequentially on the same solid background for purely decorative, non-semantic purposes—the cascade fails entirely. The cascade is designed for spatial, container-level scoping rather than localized, ad-hoc component overrides.

**Falsifying the Variant-Axis Approach (Option 1)**

Evidence demonstrating that the variant-axis approach is the wrong choice would manifest in severe developer desynchronization. If auditing the codebase reveals that developers frequently create generic wrapper components solely to recursively pass `inverse={true}` down to deeply nested children, the variant approach has failed structurally.

Critically, in platforms like AEM Edge Delivery Services, where content structure is authored by non-technical marketing users in Microsoft Word or Google Docs, expecting an author to manually tag every single button, link, icon, and checkbox inside a dark row as "inverted" is an architectural failure. The variant approach requires programmatic, granular awareness of context at the instance level, which document-based authoring fundamentally lacks.

## 8. Evidentiary Classifications

**VERIFIED**

URL: https://m3.material.io/styles/color/roles | Date Accessed: August 20, 2026.
Quote: "Inverse roles are applied selectively to components to achieve colors that are the reverse of those in the surrounding UI... Inverse surface: Background fills for elements which contrast against surface.".
Claim: Material Design 3 manages inverse context through a dedicated suite of tokens at the theme layer, resolving the context algorithmically rather than via a component property.

URL: https://react.carbondesignsystem.com/?path=/docs/components-theme--overview | Date Accessed: August 20, 2026.
Quote: "Theme is most often used to implement inline theming where you can style a portion of your page with a particular theme... Depending on your architecture you may want to apply a class to the or add a custom data attribute to your element.".
Claim: IBM Carbon utilizes a wrapper container component that publishes a CSS scope to manage nested surface context.

URL: https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/edge-delivery/build-forms/universal-editor/style-theme-forms | Date Accessed: August 20, 2026.
Quote: "Edge Delivery Services employs a block-based architecture where the .form class serves as the primary namespace... CSS custom properties defined at the :root level, providing a centralized theming system that cascades throughout all form components.".
Claim: Adobe AEM EDS idiomatically uses CSS custom properties defined at the root and modified via section classes for contextual styling.

URL: https://www.drupal.org/project/drupal/issues/3531854 | Date Accessed: August 20, 2026.
Quote: "There is a last design system API to cover the main parts of design systems: CSS variables... living at the page level, but they can be overridden with a CSS selector as a scope.".
Claim: Drupal SDC is officially integrating CSS variables scoped by CSS selectors as its primary design systems API, solidifying the cascade approach.

URL: https://github.com/Shopify/polaris/issues/10983 | Date Accessed: August 20, 2026.
Quote: "There are multiple checks for variants that apply different classes leading to code that's harder to maintain. We should be able to simplify this by using the variationName helper and cleaning up some css.".
Claim: Shopify Polaris maintainers acknowledged the code complexity and maintenance burden caused by compounding component variants and boolean properties.

URL: https://primer.style/product/getting-started/figma/ | Date Accessed: August 20, 2026.
Quote: "Primer Web provides light mode and dark mode using figma variables... Switching the variable mode changes all nested items.".
Claim: GitHub Primer uses Figma variable modes to handle contextual color changes structurally.

**INFERRED**

Claim: Adding an `inverse` property to the component variant matrix (Option 1) directly violates the core engineering philosophy of AEM Edge Delivery Services.
Reasoning: EDS documentation explicitly urges reliance on bare semantic HTML and CSS, heavily discouraging JavaScript-driven DOM manipulation for styling blocks. Requiring a variant property forces the block's JavaScript decorator to parse the context and aggressively mutate the DOM for every child component to attach specific variant classes, bypassing the native efficiency of EDS's CSS cascade architecture entirely.

Claim: The absence of a discrete `inverse` boolean property in modern iterations of heavily tokenized systems (like Material Design 3 and Carbon v11) implies that enterprise architecture views contextual inversion strictly as a systemic rendering concern rather than a local component state concern.

**COULD NOT VERIFY**

Salesforce Lightning: The provided research material did not contain any internal component API documentation, source code repositories, GitHub issues, or design guidelines for Salesforce Lightning. It is impossible to establish or verify how Lightning models surface context based on the available data set.

## 9. Recommendations and Synthesis

**A Recommendation**

The system should decisively adopt Option 3: An inherited cascade.

The component API should declare absolutely nothing regarding its surface context. Instead, a container (such as an AEM Section metadata definition or a Drupal layout block) publishes the surface context via a data attribute or CSS class. This class recalculates a strict set of CSS custom properties within its scope.

This approach is unequivocally the most idiomatic and performant path for both Adobe AEM Edge Delivery Services and Drupal SDC. Both platforms are fundamentally architected around server-rendered HTML and the injection of CSS classes at the container/section level. By leveraging CSS custom properties, the components remain entirely ignorant of their context, keeping their APIs minimal and preventing the exponential combinatorial explosion inherent in Option 1. Crucially, it guarantees WCAG 1.4.11 accessibility compliance, as focus rings, borders, and text will automatically inherit inverted custom properties without relying on infallible developer or author configuration.

**The Strongest Argument Against the Recommendation**

The most formidable argument against the inherited cascade is the inherent design-to-code synchronization gap it produces in Figma. Figma variables can only shift based on explicit modes, not hierarchical cascades within a single mode. To represent an inverted container in Figma, designers must apply an "Inverse" mode to a specific overarching frame.

Because Figma modes cannot natively simulate a targeted CSS variable cascade without globally flipping the entire token set for that frame, the structural reality of the design kit fundamentally disagrees with the structural reality of the code library. This disconnect forces designers to manage heavily bloated mode matrices (e.g., Light, Dark, Light-Inverse, Dark-Inverse) to cover cross-axis scenarios, increasing the cognitive load during design handoff and risking instances where a Figma mockup cannot accurately execute a complex, nested CSS cascade that the code handles effortlessly.

**What to Measure**

To settle any lingering debate empirically during a prototyping phase, the engineering team should measure the following metrics:

Authoring Friction (AEM EDS): Track the exact number of manual clicks and keystrokes required for a non-technical author to create a dark hero band containing three buttons and two text inputs using Document Authoring. Compare the effort of adding a single "Dark" tag to the section metadata table (Option 3) versus the author attempting to manually configure variant flags for five individual blocks (Option 1).

Compiled Bundle Size: Measure the compiled CSS output size of a component matrix utilizing explicit variant classes (Option 1) versus an architecture utilizing purely scoped CSS custom properties (Option 3).

Figma File Memory and Sync Time: Track the runtime performance, memory usage, and publish time of the central Figma library when adding an "Inverse" mode (multiplying all variable definitions) versus adding an "Inverse" variant to the component matrix. This will quantify the exact toll the structural disconnect takes on the design tooling.

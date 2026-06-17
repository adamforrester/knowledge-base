# The Avatar Component: Architectural Patterns and Implementation Truths in Enterprise Design Systems

## 1. Framing
The Avatar component serves as the foundational visual representation of an identity within a digital ecosystem. It is a highly specialized, context-aware graphical primitive that represents a user, an organization, a team, or an automated bot. Unlike a generic image component, which is designed to render arbitrary media, or an icon, which serves as a symbolic affordance for an action or concept, the Avatar is fundamentally bound to identity representation, stateful gracefulness, and precise accessibility contracts.

The true architectural complexity of the Avatar lies not in its default rendering, but in its failure modes and compositional requirements. The component operates on a strict fallback chain—gracefully degrading from an optimal photographic image to generated typographic initials, and finally to a generic icon placeholder when identity data is entirely absent. Concurrently, the Avatar functions as a host and substrate. It acts as the anchor for presence indicators (via nested Badge components) and frequently serves as a nested node within larger compositional tokens, such as Tags, Combobox selections, and list items.

Across leading enterprise design systems, structural disagreements emerge primarily around the state management of the fallback chain and the specific accessibility logic governing identity announcements. A standalone Avatar carries the entire burden of identifying a user to assistive technologies, necessitating an informative accessible name. Conversely, an Avatar rendered adjacent to a text node displaying the same identity becomes visually and semantically redundant, necessitating a decorative designation to prevent duplicative screen reader announcements. Establishing a strict, opinionated default that negotiates asynchronous image loading lifecycles, Server-Side Rendering (SSR) hydration, deterministic color generation, and accessible name computation forms the central architectural challenge of this component.

## 2. Anatomy and Parts
The physical architecture of the Avatar requires strict separation of concerns between positioning, masking, and content rendering to prevent cascading layout failures when combined with overlapping elements. A resilient Avatar is not a single HTML element, but a composite DOM structure designed to handle both internal media constraint and external composition.

| Anatomical Part | DOM Element | Architectural Purpose |
| --- | --- | --- |
| Host Wrapper | div or span | Establishes the bounding box, size, and explicit relative positioning context. Must strictly avoid overflow: hidden to ensure absolute-positioned compositional elements (like PresenceBadges) can break out of the bounding box without being clipped. |
| Masking Layer | div | Applies the semantic shape (circular, rounded-square, or hexagonal). Utilizes border-radius and overflow: hidden (or a vector clip-path) exclusively on the inner media to prevent background or image bleed. |
| Media Node | img | The primary visual payload. Utilizes object-fit: cover to prevent aspect ratio distortion regardless of the provided asset's intrinsic dimensions. |
| Typographic Fallback | span | A text node rendered inside the masking layer when the media node fails. Centered using flexbox or grid and paired with a deterministically hashed background color. |
| Placeholder Fallback | svg | Rendered when neither the image nor a valid name string is available. Inherits styling from standard Icon primitives. |
| Loading Skeleton | div | A substrate layer rendered during network transit, providing a visual placeholder without causing layout shifts. |
| Presence Anchor | div | A nested compositional slot, typically positioned at the bottom-right of the Host Wrapper, housing a status or presence indicator (Badge). |
| Group Ring | div pseudo-element | When rendered within an AvatarGroup face-pile, an external border stroke matching the underlying background color is applied to create visual separation between overlapping instances. |

The separation of the Host Wrapper from the Masking Layer is the critical structural decision. Design systems that attempt to apply overflow: hidden directly to the outermost wrapper inevitably encounter clipping bugs when attempting to host a PresenceBadge. The badge, which relies on absolute positioning to overhang the bottom-right quadrant of the circle, is mercilessly cropped by the overflow constraint. This necessitates a non-clipping parent to act as the positioning anchor, while the child mask contains the image.

## 3. Properties / API
An analysis of industry-leading implementations—including MUI, Radix UI, Chakra UI, Primer, and Fluent UI—reveals a converged API surface area designed to handle identity injection, fallback logic, and geometric constraints. The properties map directly to the underlying state machine and accessibility requirements.

| Property Name | Type | Design System Precedent | Architectural Function |
| --- | --- | --- | --- |
| src / srcSet | string | Universal | The URL of the primary image asset. srcSet handles high-DPI (Retina) scaling. |
| name | string | Chakra, Fluent, Atlassian | The raw identity string used to algorithmically generate initials and accessible labels. |
| alt | string | MUI, Primer, Polaris | Explicit alternative text. If omitted, the name prop typically serves as the fallback source for the accessible name. |
| size | enum / string | Universal | Maps to specific dimensional design tokens (e.g., sm, md, lg, xl). |
| shape / variant | enum | MUI, Primer, Fluent | Determines the mask geometry (circle, square, rounded, hexagon). |
| delayMs | number | Radix UI, Shadcn | Milliseconds to delay the rendering of the fallback state to prevent flashing during fast network responses. |
| presence / status | enum | Fluent, Atlassian | The configuration or slot for a nested presence badge. |
| getInitials | function | Chakra, Fluent | An override function allowing custom parsing logic for name-to-initials conversion. |
| color / idForColor | enum / string | Fluent | Explicit control over the deterministic color hash, allowing overrides when multiple users share identical names. |

While core properties like src and size are universal, systems diverge heavily on data injection. Chakra UI and Fluent UI lean heavily on the name prop, utilizing it simultaneously to feed the alt tag, compute the initials, and seed the color hashing algorithm. Conversely, primitive-focused libraries like Adobe React Aria and Radix UI favor a compositional API, separating the <Avatar.Image> from the <Avatar.Fallback>, requiring the consumer to manually orchestrate the data flow.

## 4. States and Variants
The Avatar is fundamentally a state machine that negotiates network unreliability. Its visual variants communicate the semantic nature of the identity it holds.

### The Fallback Chain State Machine
The core complexity of the Avatar lies in its transition through the fallback chain, progressing from an ideal state to graceful degradation.
- Idle / Loading: The initial state when a src is provided but the image has not yet painted. To prevent layout jank, this state often renders a Skeleton loader. Some systems, like Radix UI, implement a delayMs prop that intentionally holds off rendering the fallback for a few hundred milliseconds, anticipating a fast network response to avoid a jarring flash.
- Loaded (Image): The optimal state where the <img> resolves with a 200 OK status. The masking layer clips the image to the specified shape, and object-fit: cover ensures appropriate scaling.
- Error (Initials): Triggered when the src is missing, returns a 404, or the network fails. The component reads the name prop, executes the initials extraction algorithm, and renders the text node over a deterministically hashed background color.
- Error (Icon): Triggered when both src and name are missing, invalid, or unparseable. The component falls back to a generic user, organization, or bot icon.

### Shape and Entity Type Semantics
Shape serves as a primary semantic indicator of the entity type represented by the Avatar. Leading design systems rely on strict geometric conventions to orient users.
- Circle: The universal default for human users. Visual processing naturally aligns circular framing with human faces.
- Rounded Square: The established convention for organizations, workspaces, teams, or applications. GitHub Primer and Atlassian strictly enforce square or rounded-square avatars for repositories, projects, and non-human entities.
- Hexagon: An emerging variant used by systems like Atlassian to represent AI agents or bots (e.g., Atlassian Rovo), distinguishing automated generative entities from human users and static projects.

### Sizing and Typographic Scaling
Avatars map to a strict dimensional scale to fit diverse compositional contexts. A standard progression includes xs (20px, used inline in text or Tags), sm (24px, table rows), md (32px, standard application headers), lg (40px, profile cards), and xl/xxl (64px+, dedicated profile pages). The typographic fallback must scale proportionally. The mathematical standard is to map the font-size of the initials to approximately 40% of the Avatar's total bounding width, ensuring legibility across the scale without risking text overflow.

### The Avatar Group (Face-Pile)
When multiple identities are associated with a single resource, individual Avatars are stacked into an overlapping face-pile. The AvatarGroup acts as an orchestration wrapper. The standard offset is negative 20-25% of the avatar's width (e.g., -8px on a 32px avatar). To maintain visual separation, each avatar receives a solid border stroke matching the underlying canvas background. The group truncates based on a max prop, aggregating the remainder into a surplus counter styled distinctly (e.g., +5).

## 5. Usage Guidance
The structural integrity of a design system relies on strict delineation between graphical components. Clear usage guidelines prevent semantic drift and ensure consistent user experiences.
- Avatar vs. Icon: An Avatar always represents a specific, unique identity (a unique user, a specific organization, or a named bot). An Icon represents a universal action, concept, or object. System architects must enforce that Avatars are never used for UI metaphors; for example, a generic human silhouette icon should be used for a "User Profile" navigation link, whereas an Avatar should be used to display the currently logged-in user.
- Avatar vs. Image: Generic Image components handle content media (e.g., product photos, article thumbnails, marketing assets). Avatars are exclusively utilized when the media acts as an identity anchor.
- Standalone vs. Paired Contexts: A standalone Avatar (e.g., in an application header) relies heavily on its image or initials for recognition. However, in dense data displays like tables or lists, Avatars should virtually always be paired with an adjacent text node displaying the user's name. This reduces cognitive load, particularly when multiple users share similar initials or fallback colors.
- Group Limitations: Use an AvatarGroup when displaying a collection of collaborators or participants where horizontal space is constrained. Do not use AvatarGroups for standard sequential lists that require detailed interaction per user; use a standard list view instead.

## 6. Accessibility
The accessibility architecture of the Avatar hinges entirely on the concept of the accessible name contract. This contract dictates how assistive technologies, such as screen readers, interpret visual data based on its surrounding DOM context. Because avatars frequently transition between informative and decorative states depending on their placement, static alt text applications are insufficient.

### The Accessible Name Contract: Informative vs. Decorative
An Avatar operates in one of two distinct accessibility modes: informative or decorative.
- Informative (Standalone): If the Avatar is the sole visual indicator of a user's identity, it acts as an informative image. It must possess an explicit accessible name. This is typically achieved via an alt="Jane Doe" attribute on the underlying image, or an aria-label="Jane Doe" on the Host Wrapper if relying on background images or custom SVGs.
- Decorative (Redundant): If the Avatar is rendered immediately adjacent to a visible text node displaying the same identity (e.g., in a data table row reading [Avatar] Jane Doe), it becomes purely decorative. Applying an alt attribute in this context causes screen readers to redundantly announce "Jane Doe, Jane Doe." Here, the Avatar must expose an empty alt="" and ideally apply aria-hidden="true" to the Host Wrapper to completely remove the node from the accessibility tree.

Crucially, the fallback state must preserve this contract. If an image fails to load and the component renders the initials "JD", the aria-label on the wrapper must still expose the full string "Jane Doe" to the accessibility tree. Announcing the literal text "JD" is meaningless and creates an unequal experience for visually impaired users.

### Avatar Group Accessibility
AvatarGroups present a unique verbosity challenge. Exposing a stack of five individual overlapping images to a screen reader results in a tedious, sequential readout of five names. The opinionated default is to treat the group as a single semantic unit. The AvatarGroup wrapper should receive role="group" and a descriptive aria-label (e.g., aria-label="5 collaborators" or aria-label="Jane Doe, John Smith, and 3 others"), while simultaneously hiding all individual child avatars using aria-hidden="true". This ensures a concise, meaningful announcement that matches the visual synthesis of the face-pile.

### Color Contrast and WCAG Compliance
When falling back to initials, the background color is generated algorithmically. The resulting combination of background color and text color (typically white or dark gray) must maintain a minimum contrast ratio of 4.5:1 to comply with WCAG 1.4.3 (Contrast Minimum) for standard text, or 3:1 for large text.

Furthermore, under WCAG 1.4.1 (Use of Color), color must never be the sole visual means of conveying information. In the context of Avatars, the color serves as a decorative differentiator to aid quick scanning; the initials themselves, alongside the adjacent text, carry the actual semantic differentiation. System designers must curate their algorithmic color palettes strictly, removing any swatches that fail contrast requirements against the default initial text color.

## 7. Content Guidelines
Content strategies for the Avatar focus on the algorithmic generation of fallback text, handling linguistic edge cases, and preventing the inadvertent leakage of Personally Identifiable Information (PII).

### Initials Generation Rules
The algorithm for extracting initials from a name string must account for varied input formats.
- Standard Western Names: The default logic for space-delimited names is to extract the first character of the first word and the first character of the last word. A name like "Jane Anne Doe" resolves to "JD".
- Mononyms and Organizations: Single-word strings ("Etsy", "Prince") resolve to a single initial ("E", "P").
- Email Fallbacks: If the system lacks a formal name string and relies on an email address, the algorithm must strip the domain and extract initials from the local part (e.g., jane.doe@example.com resolves to "JD", while admin@example.com resolves to "A").
- Capitalization: The extraction algorithm should aggressively normalize outputs to uppercase, regardless of the input casing, to maintain typographic consistency within the circular mask.

### Group Surplus Labeling
The AvatarGroup surplus counter should strictly display numeric values preceded by a plus sign (e.g., +5). Including text strings like +5 more within the visual circle guarantees text overflow and illegibility at small token sizes. The explanatory text belongs exclusively in the aria-label or an accompanying tooltip.

### PII Leakage Prevention
Alt text and aria-label data must not expose PII beyond what is visually authorized for display in the current view. If an application obscures a user's last name for privacy reasons (rendering visually as "Jane D."), the alt text must precisely match the obscured string, not the full underlying database record. Extracting the full name for the accessibility tree while hiding it visually violates parity principles and risks data exposure.

## 8. Motion and Transition
Motion within the Avatar component should be subtle, performant, and entirely focused on minimizing layout shifts and jarring visual updates.
- Image Fade-In: Upon a successful network load, the transition from the loading skeleton or idle state to the image should utilize a brief opacity fade (e.g., opacity: 0 to opacity: 1 over 150ms ease-in). This prevents a harsh visual flash as the asset paints to the browser, smoothing the perceived performance of the application.
- Group Spread on Hover: AvatarGroups are traditionally rendered with negative horizontal margins to create the overlapping face-pile effect. A common interaction pattern applies a CSS transition on hover that resets the margins to a positive value (e.g., 4px), causing the avatars to horizontally spread and reveal their full faces. This transition must be guarded by a media query for @media (prefers-reduced-motion: reduce). If the user has disabled motion at the operating system level, this spread animation should be disabled or replaced with a static tooltip.

## 9. Internationalization
The algorithmic extraction of initials breaks down rapidly when exposed to global linguistic patterns and non-Latin scripts. A robust design system must anticipate and handle these variations gracefully.

### CJK Character Processing
The Western convention of combining the "first letter of the first name and first letter of the last name" does not map to Chinese, Japanese, or Korean (CJK) typography. CJK names do not utilize spaces to delimit words, and combining disparate characters fundamentally alters the semantic meaning of the name. Furthermore, CJK typography is highly dense; attempting to fit two CJK characters into a small circular mask results in illegible, overlapping strokes.

For CJK inputs, the initials algorithm must identify the script block (via Unicode range detection) and alter its behavior. The standard fallback is to extract only the first character—which represents the family name in CJK conventions—such as extracting "鈴" from "鈴木 一郎" (Suzuki Ichiro). Alternatively, systems may bypass initials entirely for CJK inputs and default directly to the generic icon fallback to avoid cultural or linguistic misrepresentation.

### Arabic and RTL Layout Stacking
Right-to-Left (RTL) languages, such as Arabic and Hebrew, require specific bidirectional text handling and layout inversion. When rendering an AvatarGroup in an RTL context, the overlapping z-index and negative margin rules must automatically mirror. The first avatar in the DOM array must render on the far right of the screen, and subsequent avatars should stack to the left. The z-index stacking order must also ensure that the leading rightmost avatar sits on top, with subsequent avatars tucking underneath.

## 10. Naming
The nomenclature for this primitive is largely settled across the industry, though slight variations exist depending on specific product ontologies.
- Avatar: The overwhelming industry standard, utilized by MUI, Chakra UI, Radix UI, GitHub Primer, Atlassian, and Base Web.
- Persona: Historically utilized by Microsoft Fluent UI. "Persona" traditionally represented a higher-order, heavier component that coupled an Avatar with adjacent text, presence data, and secondary details. However, Fluent UI v9 has aligned with the broader industry, separating Avatar as the core visual primitive and reserving Persona for the composite pattern.
- UserAvatar: Occasionally used (e.g., older IBM Carbon implementations) to explicitly distinguish human entities from system entities or generic icons.
- AvatarGroup / AvatarStack: Used to describe the overlapping collection of avatars. Both terms are widely understood, though AvatarGroup dominates the API landscape.

## 11. Implementation Notes
The Avatar presents some of the most deceptively complex implementation challenges in modern front-end architecture, primarily related to CSS masking limitations and React Server-Side Rendering (SSR) hydration lifecycles.

### The SSR Hydration and Cached Image Trap
Modern headless libraries, such as Radix UI, manage the fallback chain utilizing a custom React hook (often named useImageLoadingStatus). This hook instantiates a virtual window.Image() object, attaches onload and onerror event listeners, and updates component state before rendering the actual <img> tag to the DOM.

While this effectively prevents the browser from rendering a broken image icon during slow network loads, it introduces a severe SSR trap. On the server, window.Image does not exist, forcing the component to render the fallback initials into the initial HTML payload. When the client receives the HTML, the actual image asset may already be residing in the browser's cache. However, because the React component must mount, instantiate the virtual image, and wait for the asynchronous onload event to fire, the user witnesses a jarring "flash" of the fallback initials before the component swaps to the cached image. This flash duration scales directly with the application's hydration delay, resulting in poor perceived performance.

The Opinionated Default: To circumvent this, implementations must avoid purely JavaScript-driven image loading state machines for the initial render phase. Instead, the component should render the actual <img> tag with the src attribute immediately. Error handling should rely on the native onError event directly on the JSX element: <img src={src} onError={() => setFallback(true)} />. If the image is cached, the browser paints it synchronously alongside the HTML, entirely eliminating the hydration flash.

### The Presence-Dot Clipping Trap
A standard avatar achieves its circular or rounded shape via border-radius: 50% and overflow: hidden. However, design systems frequently compose a PresenceBadge (a small green or red dot indicating online/offline status) overlapping the bottom-right quadrant of the avatar.

Because the badge must be positioned partially outside the avatar's bounds to remain legible, placing it inside a container constrained by overflow: hidden clips the badge cleanly off at the circle's edge.

The Opinionated Default: The internal DOM must cleanly separate the absolute positioning context from the clipping context.

```html
<!-- Proper DOM Structure -->
<div class="avatar-host" style="position: relative;">
  <div class="avatar-mask" style="overflow: hidden; border-radius: 50%;">
    <img src="avatar.jpg" style="object-fit: cover;" />
  </div>
  <div class="presence-badge" style="position: absolute; bottom: 0; right: 0;"></div>
</div>
```

Alternatively, advanced CSS utilizes clip-path: inset(0 round 50%). Unlike overflow: hidden, clip-path creates a specific masking region that, in certain browser rendering contexts, allows absolute-positioned pseudo-elements to escape the bounding box. However, the DOM separation approach remains the most robust, predictable, and cross-browser compatible solution.

### The Deterministic Color Hash Algorithm
When an avatar falls back to displaying initials, assigning a random background color on every render results in jarring UI shifts across sessions and views. The color must be assigned deterministically based on the user's name string, ensuring "Jane Doe" always receives the identical purple background, establishing a visual anchor.

This is achieved by passing the name string through a hashing function that relies on bitwise shift operations to generate a consistent integer.

```javascript
function stringToHash(string) {
  let hash = 0;
  for (let i = 0; i < string.length; i += 1) {
    hash = string.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash;
}
```

This integer is then evaluated modulo the length of a predefined, accessibility-vetted array of design system color tokens. Generating arbitrary hex codes computationally must be strictly avoided, as it bypasses WCAG contrast validation and guarantees eventual accessibility failures.

## 12. Related and Alternative Components
The Avatar does not exist in isolation; it sits within a strict hierarchy of typed relationships and compositional boundaries.
- Icon (Substrate): The generic SVG fallback utilized when the fallback chain exhausts both image and name data. The Avatar passes specific dimensional boundaries and fill colors to the nested Icon primitive.
- Skeleton (Substrate): The loading state primitive. An Avatar in a loading state renders a Skeleton component of matching dimensions to reserve layout space without shifting content.
- Badge (Composed): The PresenceBadge is a specialized instance of the Badge primitive, positioned absolutely over the Avatar host. The Avatar controls the geographic positioning, while the Badge controls the status semantics.
- Tag / Combobox Token (Host): Avatars frequently act as children to structural components. GitHub Primer explicitly defines an AvatarToken—a specialized macro-component optimized for rendering within input fields and multiselect Tags.
- Image (Alternative): The architectural boundary. If the media does not represent a discrete entity or identity, developers should be directed to utilize a standard Image component, which exposes different loading and aspect-ratio APIs.

## 13. Field POV Evolution
The architectural philosophy surrounding the Avatar has matured significantly over the past five years, shifting from naive image tags to highly orchestrated state machines.
- Hardening of the Fallback Chain: Historically, an avatar was simply an <img alt="user" />. The industry has universally shifted toward multi-stage fallback components (Image → Initials → Icon) as broken image icons became unacceptable in high-fidelity enterprise applications.
- A11y Settling (The Decorative Rule): Early implementations naively appended the user's name to the alt tag of every single avatar on a page. As screen-reader testing became standardized, the industry recognized the severe UX degradation of double-announcing redundant text in lists. The rule that avatars adjacent to visible text must be aria-hidden is now a settled best practice.
- Shape as Semantics: The move toward utilizing squares and rounded-squares exclusively for organizations and repositories (popularized heavily by GitHub's Primer and Atlassian) has established shape as a primary semantic indicator of entity type, rather than just an aesthetic variant. This is evolving further with Atlassian's introduction of the hexagon to denote AI bots.
- The Web Component Shift: While React dominated the previous era of design systems, frameworks like Shopify Polaris are actively migrating their complex Avatar logic down to universal Web Components (<s-avatar>) to ensure interoperability across diverse tech stacks without rewriting fallback logic.

## 14. Platform State and Verification
To ensure the architectural assertions in this report remain grounded in field truth, the following systems were surveyed to track convergence and divergence in API design and implementation.

| Design System | Associated Entity | Focus Areas / Noteworthy Implementations | Version Baseline |
| --- | --- | --- | --- |
| MUI (Material UI) | Google Material | String-to-color hashing, generic fallback prioritization. | v5 |
| Chakra UI | Independent | Custom getInitials injection, strict token mapping. | v2 / v3 |
| Radix UI / Shadcn | Independent | Headless state-machine (useImageLoadingStatus), delayMs logic. | Latest |
| Fluent UI | Microsoft | idForColor deterministic overrides, Persona composition. | v9.68 |
| Primer | GitHub | AvatarToken composition, square shape semantics for orgs. | v36 |
| Atlassian Design System | Atlassian | Hexagon shapes for AI (Rovo), robust Presence/Status props. | v25 |
| Polaris | Shopify | Migration to <s-avatar> Web Components for framework agnosticism. | v13 |
| React Aria / Spectrum | Adobe | Strict adherence to WAI-ARIA group tagging and accessibility contracts. | v3 |

## 15. Agent-consumable Schema

### Avatar

### Identity
The Avatar component is a specialized visual representation of a user, organization, team, or automated entity. It serves as a dedicated identifier across the UI, functioning as a standalone element or paired with contextual text.

### Description
A context-aware graphical primitive that renders an entity's image. It includes a robust, multi-stage fallback chain that gracefully degrades to algorithmic typographic initials or a generic icon placeholder when image data fails or is unavailable.

### Anatomy
- HostWrapper: The outermost positioning container (relative). Prevents clipping of composed badges.
- Mask: The inner container that applies the geometric clipping (circle or square).
- Image: The primary media payload (object-fit: cover).
- InitialsText: The typographic fallback node.
- IconFallback: The generic SVG fallback node.
- PresenceAnchor: An absolute-positioned slot for status badges overriding the mask.

### API
- src (string): The URL of the image asset.
- name (string): The identity string used for initials and a11y labels.
- alt (string): Alternative text; dictates informative vs. decorative states.
- size (enum): The dimensional token map (xs, sm, md, lg, xl).
- shape (enum): The semantic geometric mask (circle, square, hexagon).
- presence (node): Slot for composing a PresenceBadge.

### States
- Loading: Displays a Skeleton substrate of matching dimensions.
- Loaded: Displays the primary image.
- Error/Initials: Displays text generated from the name over a hashed color.
- Error/Icon: Displays a generic SVG.

### Variants
- Entity Type: Circle (Person), Square (Organization/Project), Hexagon (Bot/AI).
- Group: Stacked variants requiring overlap layout control and surplus counters.

### Accessibility
- Informative: Standalone avatars require an accessible name.
- Decorative: Avatars adjacent to matching text must be hidden from screen readers.
- Color: Generated background colors must pass WCAG 1.4.3 (4.5:1) against the text.
- Groups: AvatarGroups must announce the total count on the wrapper, hiding individual images.

### Content
- Initials extract the first character of the first and last words.
- Single-word entities use the first character.
- Alt text must not leak obscured PII.

### Motion
- Images fade-in on successful load over 150ms.
- AvatarGroups utilize a margin-transition on hover to reveal hidden faces (respecting reduce-motion).

### I18n
- CJK name strings do not support multi-character initials; extract the first character (family name) or fallback to an icon.
- RTL layouts mirror the group stacking sequence via layout inversion.

### Implementation
- SSR Flash Trap: Avoid purely JS-driven loading state machines for the initial render. Render the <img> natively with an onError event to prevent flashes on cached images during hydration.
- Clipping Trap: Do not apply overflow: hidden to the host wrapper, as this clips overlapping PresenceBadges. Separate the masking container from the badge positioning container.
- Color Hashing: Background colors must be derived deterministically via bitwise shift algorithms from the name string mapped against a validated array of accessible color tokens.

### Composition
- Hosts: Badges (Presence/Status).
- Hosted By: Tags, Combobox Tokens, ListItems, AvatarGroups.

### Notes
- notes.unverified: The assumption that clip-path: inset() completely bypasses bounding box restrictions for all child pseudo-elements across older browser engines requires explicit QA validation before replacing the wrapper-separation method.

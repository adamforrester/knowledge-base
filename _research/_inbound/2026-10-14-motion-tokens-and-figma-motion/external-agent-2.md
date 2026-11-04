<!-- Second external-agent output for the identical prompt.md, pasted in by the owner on 2026-11-04. Raw: headings restored from the pasted text's run-in titles; wording and claims unchanged. Carries no URLs or fetch dates. Treat as hypothesis until checked; see the 2026-11-04 addendum in the synthesis. -->

# Architectural Strategies for Motion Tokenization and Figma Integration in Late 2026

The maturation of design systems has fundamentally elevated motion from a decorative afterthought to a core foundational pillar, existing alongside typography, color, and spacing. Historically, motion has been the most neglected category in design token architectures. This neglect stemmed from a structural disconnect between how designers authored motion—visually, via disparate prototyping tools or specialized software like After Effects—and how developers implemented it, typically via time-based CSS transitions or physics-based native platform APIs.

By late 2026, this paradigm has shifted dramatically. The Design Tokens Community Group (DTCG) specification 2025.10 established a stable data format for motion primitives, while design tools have natively integrated animation timelines bound directly to token variables. For a senior design systems practitioner tasked with encoding motion into a scalable, multi-platform token layer for a digital agency, the challenge is no longer merely defining a cubic-bezier curve. The contemporary architectural challenge lies in building a system that accommodates physics-based springs, multi-property choreographies, scroll-driven progress timelines, and rigorous accessibility standards, while maintaining a seamless pipeline from Figma's native motion tooling to production codebases.

This comprehensive report provides an exhaustive analysis of motion token architectures, pattern-level choreography, platform integration, and the boundaries of current token schemas to guide enterprise-scale architectural decisions.

## 1. What Mature Design Systems Ship as Motion Tokens Today

A comparative analysis of industry-leading design systems in 2026 reveals a distinct bifurcation in how motion is conceptualized and encoded. Mature systems universally separate motion into semantic tiers, ensuring that product developers never reference raw numerical values, but they disagree on the underlying mathematical model. The primary architectural schism exists between time-based systems, which rely on defined durations and bezier curves, and physics-based systems, which rely on spring dynamics and simulated physical momentum.

The IBM Carbon design system exemplifies a highly mature time-based architecture. Carbon categorizes motion into two distinct styles: productive and expressive. Productive motion is optimized for utility and cognitive efficiency, utilizing shorter durations and tighter cubic-bezier curves for micro-interactions, dropdowns, and data table rendering. Expressive motion is reserved for significant state changes, system alerts, and notification reveals, utilizing longer durations and highly pronounced easing curves to capture user attention and provide a rhythmic break to the productive experience. Carbon's token architecture relies heavily on a non-linear scale of static duration tokens, ranging from 70ms for micro-interactions to 700ms for background dimming. The system heavily leverages the contrast in duration based on the physical size of the component and the distance traveled on the screen.

Conversely, Material Design 3 (M3) fundamentally reimagined its motion system by deprecating traditional duration-based animations in favor of a physics-based spring engine. The M3 architecture abandons fixed durations, recognizing that a time-based animation feels jarring and artificial if a user interrupts it midway through its cycle. Instead, M3 utilizes springs defined by mass, stiffness, and damping ratios. M3 categorizes motion into "Spatial" tokens and "Effect" tokens. Spatial tokens are utilized for translating position, size, and orientation, allowing for physical overshoot and bounce. Effect tokens are strictly used for animating opacity and color changes, requiring critically high damping to prevent unnatural visual oscillation.

The Microsoft Fluent 2 system sits conceptually between these two paradigms. Fluent 2 explicitly models motion on physical laws—inertia, gravity, and velocity—dictating that entering elements must decelerate into the frame, while exiting elements must accelerate out. Fluent 2 relies on specific bezier curves to emulate these physical properties but maintains a strict rule against linear animation, reserving constant-rate motion exclusively for deterministic operations like loading spinners.

To formalize these approaches into a token architecture, modern systems utilize a three-tier semantic structure, ensuring that components are insulated from underlying aesthetic shifts.

| Token Tier | Architectural Characteristics | Examples | Implementation Role |
|---|---|---|---|
| Primitive Layer | Context-free raw mathematical values. Stored in global variables. | 700ms, [0.4, 0.14, 0.3, 1], stiffness: 300 | Forms the base palette; never applied directly to UI components by product engineers. |
| Semantic Layer | Values assigned to a specific interaction purpose or brand tone. | motion.productive.enter, spring.expressive.spatial | Consumed by engineers to apply system-wide behaviors to generic interface elements. |
| Component Layer | Motion logic heavily scoped to a specific UI pattern or internal state. | dialog.backdrop.fade, button.hover.scale | Bound directly to the component structure to ensure absolute consistency across deployments. |

The W3C DTCG Format Module 2025.10 formally standardizes the primitive layer. A duration token must declare $type: "duration", and its $value is an object containing a numeric value and a unit restricted exclusively to "ms" or "s". A cubic bezier token declares $type: "cubicBezier", with a $value array of exactly four numbers representing the two control points of the curve. The x-coordinates are strictly bounded between 0 and 1, while y-coordinates may exceed 1 to produce spatial overshoot. The consensus among mature systems indicates that a token model must support a dual-axis classification: one axis defining the style or personality of the motion, and the other axis defining the property being manipulated, as physical parameters that look natural on a translating container appear broken when applied to a fading text layer.

## 2. Pattern-Level Motion: Presets for Components and Transitions

Defining primitive duration and easing tokens solves only a fraction of the motion design equation. A token layer effectively describes the velocity and duration of a single property change, but modern user interfaces are composed of multiple elements transitioning simultaneously. The orchestration of these elements is known as pattern-level motion, or choreography. Mature design systems encapsulate pattern-level motion into reusable architectural primitives rather than leaving the orchestration to individual product developers.

The Atlassian Design System addresses this requirement by shipping a dedicated <Motion> primitive component, alongside specialized structural components like StaggeredEntrance and ExitingPersistence. These components act as wrappers that manage the complex lifecycle of entry and exit animations. By passing semantic enter and exit tokens directly into these primitives, the design system ensures that the precise staging of opacities, vertical translations, and staggered delays is universally applied across the application suite. The Atlassian architecture explicitly prioritizes CSS transitions over JavaScript for these primitives to ensure animations run on the browser's compositor thread, avoiding main-thread blocking and executing immediately during server-side rendering (SSR).

Component-level motion presets serve to eliminate the cognitive load on engineers. A developer constructing a complex modal should not be required to manually calculate the delay required for the modal's internal content to sequence properly after the container expands. The architectural solution involves composite transition tokens. The DTCG 2025.10 format module explicitly supports a $type: "transition" token, which binds a duration, a delay, and a timing function into a single, addressable unit. By defining composite transitions, a design system can declare a semantic modal-reveal token that inherently carries a 300ms duration, a 0ms delay, and a specific decelerating curve.

However, for multi-element choreography—such as a list where each subsequent row enters with an incrementally increasing delay—static JSON tokens face severe limitations. Choreography inherently requires dynamic computation, such as multiplying a base delay by an element's index. A static token file cannot natively express procedural logic. Consequently, the field consensus dictates that the token layer should supply the primitive interval values (the stagger duration), while the platform-specific component libraries (such as React, Vue, or Jetpack Compose) execute the mathematical iteration at runtime. Attempting to generate fifty discrete delay tokens in a JSON file for a fifty-item list represents an anti-pattern that bloats the token architecture.

The integration of pattern-level motion into design tokens also mandates strict rules regarding container states. Motion must communicate changes in the Z-axis (elevation via shadow expansion and scale), container transformations (responsive layout shifts), and interactive states (hover, focus, and press). For instance, hover interactions typically utilize highly damped, fast-response springs to feel immediately tactile and responsive, whereas layout shifts utilize slower, critically damped springs to prevent cognitive disorientation when the user's viewport changes. The token model must therefore provide pre-configured composites for these precise interaction patterns, segregating them structurally from generic page-level transitions.

## 3. Figma's Native Motion Tooling, Late 2026

A profound paradigm shift occurred in the digital design workflow in late 2026. Prior to this period, prototyping tools like Figma were structurally inadequate for rigorous motion design, forcing practitioners to rely on separate software like After Effects to dictate motion parameters, which developers then had to reverse-engineer into code. The introduction of Figma's native motion timeline at Config 2026 collapsed this fragmented workflow directly onto the design canvas.

The late-2026 state of Figma introduces an explicit motion timeline that allows designers to set independent keyframes for position, scale, rotation, and opacity across a temporal axis. This capability is augmented by the introduction of first-party animation definitions and local reusable "custom animation styles," which allow teams to compose brand-specific motion languages that can be universally applied to any object. Crucially for design systems practitioners, Figma exposed TIMING and EASING as native variable types via its Variables architecture and Plugin API.

This advancement allows animation styles and individual keyframes to bind directly to a central design system variable collection. By mapping an EASING variable to a specific spatial transition, designers ensure that any layout shift perfectly honors the brand's mathematical curves. Furthermore, because these are native variables, they inherently support Figma's mode-switching architecture. A single frame can be switched from a "Standard" motion mode to an "Expressive" motion mode, immediately updating every easing curve and duration token bound to the UI elements on the canvas.

| Figma Variable Type | DTCG Equivalent | API Translation Requirements | Limitations in Figma 2026 |
|---|---|---|---|
| TIMING | $type: "duration" | Must resolve units (ms/s) into raw numeric values expected by Figma's engine. | Lacks mathematical formulas for dynamic duration scaling based on distance. |
| EASING | $type: "cubicBezier" | Maps Bezier arrays to internal MotionEasing objects. | Cannot natively represent complex physics-based springs (mass/stiffness/damping) as raw variables; relies on Bezier approximations. |
| Styles (Composite) | $type: "transition" | Handled via Figma "Styles" rather than "Variables". | Variables cannot be nested inside other variables; complex transitions require applying styles. |

The integration pipeline between a central DTCG token repository (often managed via Git and manipulated by Tools like Tokens Studio) and Figma's variables requires a deep understanding of the platform's API boundaries. The Figma Variables REST API, restricted to Enterprise plans, supports the programmatic injection of TIMING and EASING variables. However, token synchronization tools must rigorously translate the DTCG $type: "duration" structure into Figma's expected numeric format, and carefully map DTCG $type: "cubicBezier" arrays to Figma's internal motion easing objects.

The introduction of Dev Mode's dedicated Motion tab allows developers to inspect every timing value, easing curve, and keyframe, exporting the animation code directly as raw CSS, JSON, or React. This drastically reduces the requirement for external documentation websites to host complex motion specifications, as the single source of truth is now seamlessly encoded into the design file's metadata. For a generated token system, this implies that the build process must output a payload specifically formatted for Figma's API, ensuring the EASING and TIMING variables are updated in the exact identical deployment phase as color and typography tokens.

## 4. The Hard Cases: What Tokens Can and Can't Carry

While the standard token schema handles simple transitions adeptly, an audit of a mature brand's motion inventory—such as the 105 production animations noted in this agency's context—frequently surfaces complex edge cases that resist standard tokenization. Attempting to force every kinetic behavior into a static JSON architecture results in brittle, unmaintainable systems. Understanding the boundaries of the token layer is essential for preventing architectural bloat.

### Brand-Defined Easing Curves and Per-Property Easing

Brand-defined easing curves present the most straightforward hard case to solve. The DTCG 2025.10 spec comprehensively supports $type: "cubicBezier", which allows arbitrary curve definitions restricted to standard geometric limitations. However, the complication arises with per-property easing within a single choreographed transition. When a modal scales up while fading in, the transform property frequently requires an elastic or bouncing spring curve to convey physical weight. Applying that same overshoot curve to the opacity property results in visual flickering, as opacity cannot mathematically exceed 1.0 without triggering undefined rendering behavior.

To support per-property easing, the token schema must never conflate structural motion with effect motion. The architecture must separate "Spatial" tokens from "Effect" tokens, requiring component engineers to apply two distinct tokens to the respective CSS properties or native animation targets, mirroring the Material 3 Expressive methodology.

### Scroll-Driven and Progress-Driven Motion

The most disruptive challenge to traditional token architecture is scroll-driven motion. The CSS Scroll-driven Animations module fundamentally alters the temporal axis of web animation. By leveraging the scroll-timeline or view-timeline properties, and binding them via animation-timeline: scroll() or view(), the progression of an animation is dictated entirely by the user's scroll position, rather than a wall-clock duration.

In a scroll-driven context, a duration token of 300ms becomes entirely meaningless. The animation's start and end times resolve intrinsically to the physical length of the scroll container's designated range. Therefore, the token architecture must account for progress-based modifiers. The system should supply easing curves (to dictate the rate of change relative to the scroll progress) and spatial offset tokens (defining how far an element moves), while strictly omitting duration tokens from any component mapped to a scroll timeline. Attempting to tokenize scroll percentages or animation-range bounds within a global design token file conflates layout context with foundational design decisions, leading to tightly coupled, fragile code.

### Physics Beyond Simple Springs

While design tools and basic frameworks handle simple springs, brand inventories often contain highly expressive physics: extreme inertia, decay-based scrolling, or fluid viscosity. Standard spring tokens—defined merely by mass, stiffness, and damping—cannot natively encode complex fluid dynamics or multi-stage collision physics. The DTCG community has actively debated the inclusion of physics-based composite tokens (Issue #429), acknowledging the gap in standardizing spring mechanics across disparate rendering engines.

When faced with hyper-expressive physics, the token layer should concede responsibility. Complex, multi-stage physics animations should be explicitly categorized as independent assets or custom code packages. The token system should only attempt to parameterize deterministic, general-purpose UI motion. Attempting to encode a complex inertia-decay algorithm into a static JSON token forces the build system to generate massive, highly brittle mathematical arrays that break across different platform rendering loops.

### Out-and-Back Pulses and Complex Keyframing

A comprehensive brand inventory will inevitably include multi-stage animations, such as a "pulse" that expands an element, holds for a specific duration, and contracts. Standard DTCG transition tokens encode a singular movement from Point A to Point B. They cannot encode sequential waypoints. While one could theoretically create a massive array of sequential transition tokens to represent a pulse, this violates the principle of separation of concerns.

The architectural decision framework dictates that token systems define the vocabulary (the durations, the curves, the spring constants), but the components define the grammar (the sequence and the keyframes). A pulsing animation should be constructed within the component's CSS or native code using @keyframes or native sequence APIs, referencing the design system's duration and easing tokens for the internal steps. The token layer must deliberately leave out keyframe percentages or multi-stage timeline orchestrations.

## 5. Reduced Motion and Accessibility as Architecture

In modern design systems, accessibility cannot be handled as an afterthought or an external review step; it must be structurally embedded into the token architecture. Motion poses significant cognitive and physical barriers for individuals with vestibular disorders or photosensitive epilepsy. Designing a system that respects these boundaries requires encoding accessibility parameters directly into the JSON data layer, ensuring compliance is paid for once at the architectural level rather than requiring constant vigilance from product developers.

The Web Content Accessibility Guidelines (WCAG) dictate strict, legally binding rules for motion. WCAG 2.2.2 (Level A) requires that any animation looping for more than five seconds must provide a mechanism to pause, stop, or hide it. WCAG 2.3.1 (Level A) mandates that no content may flash more than three times per second to prevent seizures. Most critically for motion architectures, WCAG 2.3.3 (Animation from Interactions, Level AAA) requires that any non-essential motion triggered by user interaction—including parallax scrolling and spatial translations—must be disabled if the user has requested a reduced motion experience via their operating system preferences.

To architecturally guarantee compliance without burdening product engineers, the design system must leverage token modes (or themes) to automate the prefers-reduced-motion implementation. Instead of relying on developers to manually wrap every animation in CSS media queries or native conditional logic, the token compilation process should automatically generate a "reduced-motion" twin for every motion token.

When the build system evaluates the tokens, it should generate a parallel output mode where all spatial translation curves are flattened to simple cross-fades, and all duration tokens are minimized. The Microsoft Fluent 2 system demonstrates an aggressive and highly effective approach to this by explicitly setting all transition and animation durations to 0.01ms when reduced motion is detected. This ensures that the application immediately reaches its final static state without requiring the developer to strip the animation logic entirely out of the component lifecycle, which can otherwise cause asynchronous callback failures in Javascript frameworks that await transition-end events.

Furthermore, the design system tooling should programmatically audit the token outputs for frequency violations. A continuous integration script can evaluate the combinations of duration tokens and cyclical animations to flag any pattern that could theoretically exceed the three-flashes-per-second threshold established by WCAG 2.3.1. By shifting the accessibility burden from human diligence to systemic property resolution, the token architecture prevents non-compliant motion from ever reaching the production environment.

## 6. Platform Delivery

Transforming a single JSON source of truth into platform-specific motion code requires a sophisticated, automated build pipeline. In 2026, Style Dictionary (version 5) remains the industry standard for resolving DTCG 2025.10 tokens and formatting them for the Web, iOS, and Android. Each platform utilizes entirely different rendering engines and mathematical models, requiring highly specific custom transforms to ensure the brand's kinetic identity remains identical across devices.

### Web and CSS: The linear() Easing Function and the Compositor Thread

Web platforms traditionally rely on cubic-bezier timing functions. However, standard beziers cannot accurately model complex spring physics, as they lack parameters for mass and stiffness, and do not simulate physical momentum or decay. To bridge the gap between physics-based design (like Material 3 Expressive) and CSS, the architecture must utilize the CSS linear() easing function, which gained universal browser support in recent years.

The linear() function accepts an arbitrary list of output values at evenly spaced input positions, effectively creating a high-resolution lookup table of a curve. During the Style Dictionary build process, a custom transformer must ingest the spring tokens (stiffness, damping, mass), numerically simulate the physical spring equation over time to determine the total duration until the spring settles, and sample the output at roughly 60 frames to generate a linear(0, 0.04, 0.16 ... 1) CSS string. This allows the web platform to execute perfect physics-based motion natively via CSS, requiring zero runtime JavaScript execution.

Furthermore, the output CSS variables must strictly align with browser performance architecture. The browser rendering pipeline consists of the main thread (parsing HTML, executing JavaScript, calculating layout) and the compositor thread (painting cached raster layers to the GPU). To ensure 120Hz smooth animations (which requires a strict 8.33ms frame budget), motion tokens should exclusively target compositor-friendly properties: transform and opacity. The design system documentation must explicitly forbid applying motion tokens to layout properties like width, height, or margin, as these trigger layout recalculations (reflows) that block the main thread, resulting in severe visual jank regardless of how optimized the token values are.

### Apple iOS: SwiftUI and Animation.spring

For Apple platforms, SwiftUI handles motion natively through its highly optimized core animation pipeline. When translating motion tokens for iOS, the build system must convert the raw spring data into SwiftUI's specific parameters: response, dampingFraction, and blendDuration.

The response parameter controls the speed of the animation (effectively acting as the inverse of stiffness), while the dampingFraction controls the oscillation. A dampingFraction of 1.0 represents a critically damped spring that smoothly settles without bounce, whereas values below 1.0 create increasingly pronounced oscillation. The build pipeline must map the semantic JSON tokens directly to these parameters, generating typed Swift constants that iOS developers invoke via .animation(.spring(response: X, dampingFraction: Y), value: state). Interactive springs, optimized for user interactions like dragging, utilize specific .interactiveSpring defaults tuned for finger tracking, requiring distinct token pipelines if the brand wishes to override native touch physics.

### Android: Jetpack Compose and SpringSpec

Android's modern UI toolkit, Jetpack Compose, utilizes a similar but distinct physics engine. The Style Dictionary transformer targeting Android must map the motion tokens to the SpringSpec class, which expects two primary parameters: dampingRatio and stiffness.

While Jetpack Compose provides internal constants (e.g., Spring.DampingRatioMediumBouncy, Spring.StiffnessLow), a mature design system must inject the exact numerical values derived from the token configuration to ensure perfect kinetic synchronization with the Web and iOS counterparts. The generated Kotlin output encapsulates these parameters into remember { SpringSpec(dampingRatio, stiffness) }, allowing the physics calculations to run smoothly on the Android rendering thread without causing unnecessary object allocation or recomposition drops during the animation lifecycle.

## 7. Recommendations for a Generated Token System

Based on the architectural analysis of mature design systems, the evolving DTCG specification, the complexities of platform delivery, and the integration capabilities of Figma's late-2026 motion APIs, the following frameworks establish precise recommendations for what to include, what to exclude, and how to structure a generated motion token system for a digital agency.

### Structure the Motion Taxonomy by Intent, Not Mathematics

Do not expose raw time or curve values to downstream developers. The architecture must enforce a semantic layer that insulates product code from mathematical updates. Define motion based on two axes: the style of motion (e.g., Expressive versus Productive/Functional) and the affected property (e.g., Spatial versus Effect).

- Spatial Tokens: Used strictly for translations, scale, and rotations. These should utilize spring physics (or linear() approximations on the web) to allow for natural overshoot and inertia.
- Effect Tokens: Used strictly for opacity, color transitions, and blurs. These must be critically damped or rely on standard ease-in/ease-out bezier curves to prevent visual flickering and unnatural oscillation.

### Implement the Build-Time Spring-to-Linear Transformation

To achieve cross-platform parity without sacrificing performance on the web, the token source of truth should be defined using physics-based spring parameters (mass, stiffness, damping) wherever possible.

- For Native (iOS/Android): Pass the physics parameters directly to the SwiftUI Animation.spring and Jetpack Compose SpringSpec constructors via Style Dictionary custom formats.
- For Web (CSS): Implement a custom Style Dictionary transformer that samples the spring equation and outputs a CSS linear() easing function, alongside the computationally derived settling duration. This achieves complex physics-based motion on the CSS compositor thread with zero runtime JavaScript cost, preserving the 120Hz frame budget.

### Fully Integrate with Figma Variables, but Acknowledge Boundaries

Leverage Figma's TIMING and EASING variables. The token pipeline should write the semantic duration and curve tokens directly into the Figma Variables REST API. This empowers designers to bind these variables natively to the Figma motion timeline, ensuring prototyping remains perfectly in sync with production code.

However, recognize the boundaries: Figma's variable system currently lacks complex mathematical composition for motion. Ensure that automated sync scripts gracefully map $type: "cubicBezier" and duration values into the exact structure the Figma API requires, dropping complex composite transitions that Figma cannot natively interpret in its variables panel. Manage complex choreographies via Figma Styles or Component Variants rather than raw variables.

### Systematize Reduced Motion as a First-Class Token Mode

Do not rely on developers to write @media (prefers-reduced-motion) queries in their application code. Treat accessibility as a standard token theme. Structure the token JSON to include an $extensions: { mode: { reduced: ... } } object for every semantic motion token. When compiled, the system should generate a parallel file or CSS custom property block where all durations are clamped to 0.01ms and all spatial curves are flattened to linear. This guarantees absolute systemic compliance with WCAG 2.3.3 and removes human error from the accessibility pipeline.

### Explicitly Omit Complex Choreography from the Token Layer

A resilient token architecture is highly opinionated about what it refuses to do.

- Omit out-and-back pulses and complex keyframes: Multi-stage keyframe animations cannot be elegantly represented in a flat token schema. Define the foundational curves and durations in the tokens, but construct the @keyframes inside the component library.
- Omit scroll-driven timelines: Because scroll-driven animations use scroll distance rather than time, duration tokens are functionally useless. Do not attempt to tokenize scroll percentages. Define spatial offsets in tokens, but manage the animation-timeline logic strictly in the frontend codebase.
- Omit layout-blocking transitions: Explicitly deprecate or forbid the use of tokens for animating height or width natively, as they block the main browser thread. Funnel all component-level changes through compositor-friendly properties like transform and scale.

By adhering to these architectural recommendations, a design systems practice ensures that its motion tokens remain agnostic to the underlying rendering engine, perfectly synchronized between Figma and code, and strictly compliant with accessibility mandates, ultimately culminating in a robust, enterprise-grade digital foundation.

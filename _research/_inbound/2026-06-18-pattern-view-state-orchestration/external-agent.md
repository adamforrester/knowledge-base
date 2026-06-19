# View-state orchestration

> "Components are inherently solipsistic. A Button knows how to spin; a Table knows how to render rows; an Empty State knows how to center an illustration. Yet none of these components possess the architectural awareness to decide when the Table should be replaced by the Empty State, or whether the region should render a Skeleton instead of a Spinner during a data fetch. View-state orchestration is the declarative composition pattern that assumes this responsibility. Its existence validates the foundations-exile principle: the rules governing cross-region state transitions cannot be exiled to basic foundation guidelines, nor can they be crammed into individual component props. They require a dedicated orchestration layer."

## Problem & Context

Digital interfaces operate over asynchronous networks where data availability is rarely instantaneous and operations frequently fail. The structural problem design systems face is not the design of a loading spinner or an empty state illustration. Those are solved, component-level problems. The recurring architectural challenge is the coordination of these states across a contiguous region or view. When systems lack a formalized view-state orchestration pattern, interface behavior degrades into localized, imperative decision-making. Developers conditionally render components based on raw boolean flags, leading to layout thrashing, flashes of unstyled or loading content, inaccessible transitions, and a chaotic mix of spinners and skeletons. Furthermore, without a centralized taxonomy, different product teams will apply the same empty state component for fundamentally different user scenarios, such as a first-use onboarding moment versus a filtered-out scenario, creating severe cognitive friction.

This brief validates the foundations-exile distinction codified within advanced design system architectures. The rule stating that a button shows a spinner while pending is a foundational component rule. It requires no awareness of the surrounding page context. Conversely, coordinating a multi-fetch dashboard where one region fails, one region streams data, and another resolves to zero results requires cross-cutting decision rules. View-state orchestration owns this region-scale coordination, elevating it from a mere structural guideline to a vital composition pattern. The orchestrator must determine whether a layout should be preserved with skeletal rows or collapsed entirely into an illustrated message. It must manage the live-region accessibility budget so that screen readers are not overwhelmed by simultaneous status updates. By defining these boundaries, the system ensures that performance optimization efforts—such as lazy loading and streaming server-side rendering (SSR)—translate into cohesive, accessible user experiences.

## Composition

View-state orchestration functions as a logical state machine that wraps and coordinates a specific set of typed components. It does not dictate the border-radius of the skeleton or the illustration style of the empty state; rather, it dictates the routing logic that determines when and how these components are deployed.

The orchestration assembly typically includes layout primitives such as grids, cards, tables, and lists. These serve as the underlying content containers whose visibility or structure is manipulated by the orchestrator. To manage latency, the pattern utilizes skeleton screens, which are structural, wireframe-like placeholders indicating determinate or indeterminate progress for specific layout shapes. When structural prediction is impossible, the orchestrator deploys spinners or progress indicators, which are animated elements denoting background processing without conveying layout. For resolved states lacking data, the pattern utilizes empty state or result components, characterized by centered, illustrated, or typographically distinct messaging. Finally, to handle recoverable or partial failures, the orchestrator relies on inline messages and banners rendered within the normal document flow.

The orchestra delta—the value added by this pattern over the sum of its parts—is the introduction of transition delays, fallback UI thresholds, accessible live-region announcements, and optimistic UI rollback mechanisms.

| Component Category | Component Responsibility | Orchestrator Responsibility |
| --- | --- | --- |
| **Loading Indicators** | Renders the SVG spinner or pulsing skeleton animation; manages local color tokens. | Determines whether the delay warrants a spinner, a skeleton, or nothing; enforces minimum display duration to prevent flickering. |
| **Empty States** | Centers the illustration and typography; exposes slots for action buttons. | Determines if the context requires a "first-use" or "no-results" variant; handles the taxonomy of the empty condition. |
| **Inline Errors** | Renders the red border, warning icon, and text styling. | Maps the network or validation failure to the correct region; ensures the layout does not collapse unnecessarily. |
| **Layout Primitives** | Renders columns, rows, and grid gaps. | Decides whether the layout skeleton is preserved during a refresh or if the entire layout is unmounted and replaced. |

## Decision Rules

A composition pattern earns its keep through machine-resolvable decision logic. The following frameworks represent the field-truth convergence on contested view-state forks. These rules shift the paradigm from subjective designer preference to objective, threshold-based logic.

### Skeleton vs. Spinner vs. Optimistic vs. Nothing

The most heavily litigated decision in view-state orchestration is how to represent latency. System orchestrators must evaluate duration thresholds, layout predictability, and interaction types to determine the appropriate fallback mechanism. Introducing a loading state too early creates a flash of unstyled content that perversely increases the perceived wait time. Conversely, failing to provide feedback for long-running operations leads to user abandonment and repeated, frustrated clicks.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Anticipated fetch is < 300ms (perceived as instantaneous) | Nothing | Introducing a loading state for sub-300ms requests causes a jarring visual flicker. Rely on the natural latency of the network. |
| Action is user-driven, predictable, and non-destructive (e.g., liking a post) | Optimistic UI | Assume success and update the layout immediately. This eliminates the friction of waiting, provided a silent background sync occurs. |
| Anticipated fetch is 300ms - 1s OR layout is highly unpredictable | Spinner / Progress Indicator | Spinners provide necessary feedback that the system is working without the layout-shift penalty of rendering an inaccurate skeleton. |
| Anticipated fetch is 1s - 10s, region is substantial, and layout is known | Skeleton Screen | Skeletons stabilize the layout and reduce perceived wait times by communicating structural progress and mimicking the final content. |
| Anticipated fetch is > 10s or involves heavy file transactions | Determinate Progress Bar | Skeletons and spinners induce abandonment anxiety after ten seconds. Explicit percent-done or time-remaining indicators are mandatory. |

### All-at-Once vs. Staggered Loading

The adoption of React Suspense, streaming Server-Side Rendering (SSR), and selective hydration has reshaped how orchestration patterns handle multi-region loads. Historically, developers loaded each component independently, resulting in a chaotic, staggered visual presentation where interface elements popped into existence haphazardly. Modern view-state orchestration utilizes declarative boundaries to control the rendering cascade.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Sibling regions depend on the same underlying data context | All-at-once orchestration | Wrap the regions in a single unified orchestration boundary. Render one comprehensive skeleton, replacing it only when the entire data object resolves. |
| Page consists of independent widgets with varying backend latency | Staggered (Streaming) orchestration | Wrap regions in nested or adjacent boundaries. Stream primary content first, leaving secondary regions in localized skeleton states to prevent the slowest query from blocking the entire view. |
| Deeply nested child components require independent fetches | Consolidate boundaries upward | Avoid over-nesting staggered loaders. Wrapping deep grandchildren independently causes severe layout thrashing. Position boundaries at natural loading units like routes or cards. |

### The Empty-State Taxonomy at View Scale

Leading systems heavily differentiate between the causes of an empty region, dictating structural and copy variants rather than relying on a single monolithic empty state illustration. Using a cheerful, celebratory illustration when a user's search query returns zero results is contextually jarring and frustrates the user. The orchestration layer must route the empty condition to the appropriate visual and semantic treatment.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| The user has never interacted with this region (First-Use / Blank Slate) | Onboarding Empty State | Functions as an entry point. Requires a high-prominence primary action (e.g., "Create project"), educational copy, and visually engaging illustrations. |
| Data exists, but the current query or filter yields nothing (Zero-Results) | Filtered-Out State | Do not use an illustration. Use terse, direct copy (e.g., "No matches"). The primary action must be a secondary-styled button to clear the filters. |
| The user has successfully resolved or deleted all items (Inbox Zero) | Success / Cleared State | Frame the state as a celebration. Use positive illustrations. No immediate primary action is required unless guiding the user to a new workflow. |
| Data exists, but the user lacks authorization or the system is pending setup | System-Empty / Permission State | Frame clearly without user blame. Provide technical context. Action buttons should direct to permission requests or external documentation. |

### The Error-State Taxonomy at Region Scale

Error orchestration must match the scale and recoverability of the failure. Applying a full-page error state for a localized component failure destroys the user's surrounding context and forces a complete workflow reset. Conversely, using a subtle toast notification for a fatal data fetch leaves the main viewport in a perpetually broken or empty state.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Error is a transient network blip or background synchronization failure | Toast / Notification | Do not disrupt the view state. Allow the user to continue operating on cached data while providing an ephemeral status update. |
| Specific component or isolated region fails to fetch data | Section-level Error Boundary | Replace the specific widget with an inline error message and a "Retry" button. Preserve the rest of the page layout so the user can continue other tasks. |
| User input validation fails upon submission | Inline Form Error + Error Summary | Highlight specific fields and provide an Error Summary banner at the top of the form to aid screen reader navigation. |
| Primary data payload for a core view fails completely (e.g., 500 error) | Full-page Error State | Replace the entire structural layout with a centralized error illustration and a safe navigation egress to prevent the user from interacting with a broken state. |

### Replacing the Underlying Layout vs. Preserving It

The orchestrator must decide whether to tear down the underlying HTML structure or preserve it during transition states. This choice distinguishes a composition pattern from a basic component.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Surrounding chrome (table headers, sidebar filters) provides context | Preserve Scaffold (Render in-place) | Render a Table and populate it with Skeleton rows. When data resolves to zero, keep headers visible and render an InlineMessage inside the table body. |
| Layout is meaningless without data (e.g., an empty image gallery) | Collapse to Message (Replace layout) | Unmount the data container entirely. Render a centralized EmptyState or Result component in the center of the parent region. |
| Container is highly constrained vertically (e.g., a mobile viewport) | Collapse to Message (Replace layout) | Keeping complex filter bars visible alongside an empty state on mobile forces the actionable recovery button below the fold, necessitating layout replacement. |

### State-Message-in-Region vs. Toast vs. Banner

The orchestration boundary between a regional view-state and the system-wide notification pattern is determined by user focus and action origin. The system must route messages to the surface where the user's attention is currently directed.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Message pertains directly to the data payload of the current visual region | State-Message-in-Region | The messaging replaces or sits adjacent to the localized data, keeping the error deeply contextualized to the failed content. |
| Message acknowledges a user-initiated background action | Toast Notification | Routes to the notification orchestrator, alerting the user to an asynchronous success or failure without interrupting their current localized task. |
| Message is a system-wide context affecting the current view | Global Banner | Placed at the top of the application shell, pushing regional content down to indicate pervasive states like "Read-Only Mode" or "Maintenance Scheduled". |

### Optimistic UI's Failure Mode

Optimistic updates drastically improve perceived performance by instantly resolving the user's action in the UI while handling the network request asynchronously. However, this pattern requires a strict rollback contract to maintain data integrity and user trust.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Optimistic network request fails | Instant Rollback + Contextual Toast | Revert the regional UI to its previous state instantly without triggering a full-page loading state, accompanied by an explicit explanation of the failure. |
| Action is destructive, financial, or asynchronous-by-design | Standard Loading Orchestration | Never use optimistic UI for deletions, purchases, or operations where the backend modifies the payload unpredictably. Force the user to wait for server confirmation. |

### The Skeleton's Faithfulness Contract

A skeleton screen serves as a visual promise of future layout. Violating this promise causes severe layout shifts—negatively impacting Cumulative Layout Shift (CLS) metrics—and disorients the user.

| Condition (IF) | Resolution (USE) | Rationale & Context |
| --- | --- | --- |
| Target component dimensions and column counts are known | Exact Match Skeleton | The skeleton must mathematically match the maximum dimensional constraints of the incoming component to prevent layout thrashing upon data resolution. |
| Target component layout changes frequently through CSS updates | Component-Driven Skeleton Generation | Skeletons must not be hard-coded SVG assets that experience "skeleton drift." Implement skeletons utilizing the exact same CSS grid/flexbox primitives as the target. |

## Flow & States

The view-state orchestrator operates as a deterministic state machine managing the lifecycle of a region. It transitions sequentially, preventing impossible UI overlaps, such as displaying a loading spinner alongside a populated data table.

The region begins in a pristine or idle state before any data fetching occurs. Upon initialization, it enters the loading state. Here, the orchestrator evaluates the aforementioned 300-millisecond threshold. If the threshold is breached, it injects the appropriate skeleton or spinner and signals to assistive technologies that the region is busy. Once the network request resolves successfully with a populated payload, the orchestrator transitions to the loaded state, stripping away loading indicators and swapping in the fully populated layout primitive.

If the data resolves successfully but the payload is mathematically zero, the orchestrator transitions to the empty state, triggering the taxonomic rules to decide between a first-use onboarding view or a no-results filter view. Finally, if the network request fails entirely, the state machine transitions to the error state, replacing the layout with a localized error boundary or injecting an inline alert for recovery.

In optimistic UI flows, the state machine bypasses the standard loading phase, jumping directly from pristine to an optimistic loaded state. The background fetch acts as a silent validator; if it succeeds, the state remains loaded. If it fails, the machine forces a rollback to the pristine state and triggers an error toast.

## Layout & Structure

While the orchestrator rarely owns its own visual design tokens—acting instead as an invisible wrapper like a React `<Suspense>` boundary or a bespoke `<ViewState>` wrapper—it bears heavy structural responsibilities. The primary layout mandate of the orchestrator is enforcing minimum height constraints.

During data fetches or transitions to empty states, the sudden unmounting of a massive data table can cause the page footer and surrounding elements to violently jump upward. To mitigate this layout thrashing, the orchestration wrapper must enforce a minimum height equivalent to either the anticipated skeleton's height or the standard empty state's height. When a table collapses into an empty state, the message should ideally be centered within a container that mathematically matches the previous data container's height, preventing vertical scroll-bar jarring and maintaining the user's optical focal point.

## Accessibility Orchestration

The single most frequent point of failure in loading and error patterns is the lack of accessible orchestration. Sighted users visually perceive a layout swapping from a shimmering skeleton to an illustrated empty state; however, users of assistive technology (AT) perceive absolutely nothing unless the orchestrator deliberately routes the state change to the browser's accessibility tree.

When a region enters the loading state, the orchestrator must programmatically apply the `aria-busy="true"` attribute to the wrapping container. This is a critical WCAG 4.1.3 compliance measure that instructs screen readers to pause announcements for internal Document Object Model (DOM) mutations until the state resolves. Continually interrupting a user's workflow to announce micro-loads creates extreme auditory fatigue. Therefore, orchestrators must rely on `aria-busy` to suppress noise rather than using explicit `aria-live` announcements to broadcast the wait. Once the content loads or resolves to an empty state, the orchestrator sets `aria-busy="false"` or removes the attribute entirely.

The live-region budget dictates how the orchestrator announces final states. When an empty state—such as a "No results found" message—or a non-critical localized error renders, the orchestrator must inject it into a container utilizing `aria-live="polite"` or `role="status"`. This polite setting allows the screen reader to gracefully finish its current sentence before announcing the update. Conversely, when a critical validation error or system failure renders, the orchestrator must utilize `aria-live="assertive"` or `role="alert"`, immediately interrupting the user to warn them of the failure.

State transitions must respect a strict focus management contract. Moving between loading, empty, and loaded states should not forcefully steal keyboard focus. Focus manipulation is only acceptable if a fatal, full-page error boundary has been triggered, completely removing the user's previous focus target from the DOM. In such catastrophic failures, focus should be shifted programmatically to the error summary or primary recovery heading.

## Content & Copy

System-level voice constraints heavily dictate the copy utilized within empty and error states across the orchestrated view. The overarching goal is clarity, conciseness, and actionability, avoiding technical jargon or user-blaming language.

For empty states, the voice must be direct and scannable. Platforms like Cloudscape and Atlassian explicitly mandate that headings avoid terminal punctuation, ensuring they read as structural titles rather than prose (e.g., "No distributions" rather than "No distributions."). Furthermore, the description body must not redundantly repeat the heading text, and directional language—such as "click the button below"—must be avoided to maintain device independence.

Loading messages accompanying a spinner or skeleton should be entirely omitted unless the action reliably exceeds ten seconds. If a loading message is deemed necessary, it must be highly precise. Instead of utilizing a generic "Please wait...", the copy should explicitly state the system action, such as "Loading S3 buckets..." or "Generating report...".

Error actionability is paramount. The system must never expose raw machine-generated exception strings to the end user as the primary message, nor should it adopt a tone that implies user fault. Instead of stating "You didn't enter a valid format," the copy should utilize active verbs detailing the explicit recovery path, such as "Refresh the code and try again" or "Enter a valid email address".

## Variants & Responsive

View-state orchestration scales responsively by dynamically altering its layout preservation logic based on viewport constraints. The decision to preserve the surrounding chrome or collapse entirely to a message is largely dictated by available screen real estate.

In desktop environments, abundant screen real estate heavily favors preserving scaffolds. An empty state message or a localized error can be comfortably rendered inside the footprint of a ten-column data table, keeping the table headers, sidebar filters, and pagination controls visible. This contextual preservation allows the user to quickly adjust parameters to recover from the empty state.

Conversely, strict spatial constraints in mobile viewports favor replacing layouts entirely. A mobile list view should collapse completely into a centralized empty state or error message. Attempting to keep complex list-headers or robust filter bars visible alongside an illustrated empty state on a narrow mobile screen forces the actionable recovery button below the fold, breaking the user experience and violating standard visibility guidelines.

## Anti-Patterns

Orchestrating complex asynchronous views presents numerous pitfalls. The following anti-patterns represent the most recurring traps observed in field implementations.

| Anti-Pattern | Description | UX Impact |
| --- | --- | --- |
| **Flash of Loading** | Rendering a skeleton or spinner for a sub-300ms network request. | Causes the UI to briefly flicker before showing content, paradoxically making the system feel slower and glitchier than if nothing was shown. |
| **Skeleton Drift** | Shipping a skeleton SVG or hard-coded CSS that no longer mathematically matches the structural layout of the evolving target component. | Causes a severe Cumulative Layout Shift (CLS) upon data resolution, disorienting the user as content violently shifts position. |
| **Spinner-by-Default** | Utilizing circular progress indicators as the default fallback for massive full-page loads or processes exceeding a few seconds. | Forces users to "watch the clock," increasing perceived wait times and failing to set structural expectations. |
| **Empty-States-as-Errors** | Utilizing the standard, playful empty state illustration for a critical data-fetch failure, 500 error, or a 403 permission state. | Violates contextual trust. Cheerful illustrations appear mocking or insensitive during catastrophic application failures. |
| **Over-nested Suspense** | Wrapping every individual micro-component in its own loading boundary rather than grouping them logically by region. | Results in a chaotic, staggered "popcorn" load effect that causes extreme layout thrashing and visual fatigue. |
| **Optimistic Destruction** | Faking the success of a "Delete Account" action, a financial transaction, or a complex backend generation task before server confirmation. | Leads to severe trust degradation when the action inevitably fails and the destroyed data "magically" reappears via a rollback. |
| **Polite Everything** | Using `aria-live="polite"` for every single state change, including fatal form validation errors. | Fails to interrupt the screen reader during critical failures, allowing visually impaired users to proceed without realizing an error occurred. |

## Related Patterns & Components

This pattern strictly defines logical coordination across a view. It maintains rigorous architectural boundaries against the individual components it orchestrates, as well as sibling composition patterns. Understanding these boundaries is critical to maintaining a clean, systematic taxonomy.

**View-state orchestration vs. Skeleton / Spinner / Empty State (Components):** The individual component owns its localized visual styling, SVG paths, motion physics, and local properties (e.g., the pulse animation of a skeleton or the border-radius of an empty state card). The view-state orchestrator, conversely, owns the logic dictating when the component mounts, how long it waits before displaying, and what asynchronous data thresholds trigger it.

**View-state orchestration vs. Notification orchestration (Pattern):** The boundary here is defined by trigger origin and user focus. If a foreground user action directly affects the current visual region (e.g., submitting a localized form), the view-state orchestration handles the resulting error or success directly in-region. If an asynchronous background event completes (e.g., "Batch export ready") or a system-wide broadcast occurs, the logic routes to the notification orchestration pattern, generating system-wide toasts or banners.

**View-state orchestration vs. Error Pages (Pattern):** This boundary is defined by the scale of disruption. Full-page 404s, 500s, or hard offline states are handled by the Error Pages pattern, which entirely replaces the application shell. View-state orchestration is strictly concerned with managing region-scale errors inside an active, functioning application shell.

**View-state orchestration vs. Onboarding (Pattern):** The threshold here is journey length. A single-frame, first-use empty state with a solitary call-to-action belongs to view-state orchestration. If interacting with that CTA triggers a multi-step modal tour, a tooltip sequence, or progressive disclosure, it crosses the boundary into the distinct Onboarding pattern.

**View-state orchestration vs. Bare Disabled/Loading States (Foundations):** This explicitly states the foundations-exile distinction upon which this schema rests. A standalone button locally disabling itself and showing a spinner while pending is a foundational rule embedded directly in the button component. However, the logic dictating that clicking "Delete" on a table row disables all other rows in the view and triggers a top-level inline banner requires cross-component awareness. That region-scale coordination is view-state orchestration.

## Field POV Evolution

The industry approach to view-state orchestration has matured significantly over the past decade, evolving from static visual indicators to psychological manipulation techniques, and finally settling into declarative streaming frameworks.

The concept of perceived performance gained massive traction between 2013 and 2016. Reacting against the anxiety-inducing nature of infinite spinners, Luke Wroblewski (via his work on the Polar app) and Daniel Eden (via Facebook) pioneered "skeleton screens." These wireframe placeholders shifted user focus away from the act of waiting and toward anticipating progress, artificially reducing perceived wait times by mimicking the final layout structure. During this era, design system documentation rapidly expanded to include dedicated skeleton primitives.

However, a partial walkback occurred between 2017 and 2020. Following widespread, often haphazard adoption, a 2017 Viget study and subsequent Nielsen Norman Group research revealed severe flaws. The studies showed that poorly implemented skeletons—specifically those used as static splash screens without motion, or those applied to loads exceeding ten seconds—actually performed worse than spinners in user perception tests. The field realized that skeletons require motion (pulsing or shimmering from left to right) and must strictly, mathematically match the incoming layout to prevent jarring visual shifts.

The contemporary era (2022 to present) is defined by the "Suspense Contract." The introduction of React 18's `<Suspense>` boundaries, the `use()` hook, and Streaming SSR fundamentally reshaped how engineers approach orchestration. Instead of writing imperative, deeply nested boolean logic (`if (loading) return <Skeleton/>`), orchestration evolved into declarative boundary management. This solved historic layout thrashing issues by allowing orchestrators to group regions into logical chunks that stream into the DOM cohesively, deferring rendering until data dependencies are met. Concurrently, optimistic UI normalized. Championed by data-fetching libraries like React Query and Apollo, optimistic updates transitioned from a niche "app-like" novelty to a baseline expectation for micro-interactions, necessitating the rigid rollback orchestration rules detailed in this report.

## Reference Instantiations & Verification Sources

Leading design systems handle orchestration through highly specific frameworks, validating the decision rules established in this pattern.

**The Atlassian Design System** distinguishes cleanly between an "Empty State" (where there is no data to display due to clearance or lack of access) and a "Blank Slate" (a first-use discovery moment). They provide explicit React-based `<EmptyState>` components with rigorous slot structures for headers, descriptions, and primary/secondary actions, enforcing strict voice and tone guidelines to avoid overly playful copy in frequently seen empty states.

**Cloudscape (AWS)** implements an exhaustive taxonomy for data absence, drawing a hard line between an "Empty State" (e.g., no distributions created) and a "Zero Results" state (e.g., filters applied, no matches). They enforce exact copy guidelines and dictate that "Zero Results" states must feature a secondary "Clear filter" button. Cloudscape also excels in defining "Error Boundaries" at the component, section, and page levels, isolating failures so a crashed chart does not take down an entire dashboard.

**Shopify Polaris** separates whole-page loading from in-region loading. They provide structural skeletons (`<SkeletonPage>`, `<SkeletonTabs>`) and explicitly restrict their basic `<Spinner>` component from being utilized for full-page loads, mandating that skeleton screens preserve layout context during heavy merchant data fetches.

**Material Design 3 (M3)** formalizes the distinction between indeterminate and determinate progress. Their guidelines dictate that skeleton loaders must utilize a pulsing animation moving from the top-left to the bottom-right, categorized structurally under "Transitions" to indicate indeterminate progress that mimics the final layout.

**Ant Design** utilizes a highly mature, three-part orchestration suite: the `<Empty>` component for data absence, the `<Skeleton>` component for latency, and the `<Result>` component for heavy operational conclusions, such as successful submissions or fatal access-denied errors.

Finally, **the GOV.UK Design System** provides a stark contrast regarding validation orchestration. They specifically reject HTML5 browser validation and heavy client-side skeleton screens due to accessibility and cognitive concerns. Instead, they rely on server-driven, highly accessible Error Summaries at the top of the page, explicitly linked to inline error messages with thick red borders, ensuring form values remain intact during the orchestration cycle.

| Source Entity | Verification Path / Notes | Version Date |
| --- | --- | --- |
| NN/g (Page Laubheimer, Samhita Tankala) | Validates 300ms/1s/10s duration thresholds; defines the danger of frame-only skeletons. | 2020, 2023 |
| Luke Wroblewski / Viget Study | Traces the origin of the skeleton screen (Polar app) and the subsequent empirical critique. | 2013, 2017 |
| React Documentation / Community | Establishes the modern Suspense/Streaming SSR boundaries that prevent staggered layout thrash. | 2024, 2025 |
| WCAG 2.2 / WAI-ARIA Standards | Mandates the use of `aria-busy` and the polite vs. assertive live-region budget for state changes. | Current |
| Daniel Eden (Facebook) | Explores the early lineage of CSS skeletons and design system grammar at scale. | 2014, 2017 |

## Agent-consumable schema

```yaml
id: view-state-orchestration
name: View-state orchestration
aliases: [loading-states, empty-states, state-coordination, suspense-boundaries]
tier: composition
goal: recover-from-error
status: validated
problem: >
  Components lack the architectural awareness to coordinate full-region state changes.
  Relying on localized conditional rendering creates layout thrash, inaccessible DOM mutations,
  and inconsistent taxonomic usage of empty/error states across an application.
composition:
  requires:
    - layout-primitive
    - skeleton
    - spinner
    - empty-state
    - result
    - inline-message
decision_rules:
  latency_fallback:
    - { if: "fetch < 300ms", use: "nothing" }
    - { if: "fetch 300ms - 1s", use: "spinner" }
    - { if: "fetch 1s - 10s AND layout predictable", use: "skeleton" }
    - { if: "fetch > 10s", use: "determinate-progress-bar" }
  orchestration_type:
    - { if: "sibling regions depend on shared data context", use: "all-at-once-suspense-boundary" }
    - { if: "independent widgets with varying latency", use: "staggered-streaming-suspense-boundaries" }
  empty_taxonomy:
    - { if: "first-use of feature", use: "empty-state-with-illustration-and-primary-cta" }
    - { if: "data filtered out / zero results", use: "empty-state-no-illustration-secondary-clear-filters-cta" }
  error_taxonomy:
    - { if: "transient network failure", use: "toast-notification" }
    - { if: "component-level fetch failure", use: "inline-error-boundary-replacement" }
    - { if: "page-level fatal failure", use: "full-page-error-state" }
  optimistic_ui:
    - { if: "action is non-destructive, highly predictable", use: "optimistic-update" }
    - { if: "optimistic update fails", use: "instant-rollback-plus-error-toast" }
flow:
  states: [pristine, loading, loaded, empty, error]
accessibility_orchestration:
  loading_state: "apply aria-busy='true' to region container"
  polite_status: "use aria-live='polite' or role='status' for empty/success states"
  assertive_status: "use aria-live='assertive' or role='alert' for critical validation/errors"
  focus_management: "preserve focus unless element is unmounted by fatal error boundary"
content:
  empty_voice: "sentence case, no terminal punctuation in headers, avoid user-blame"
  loading_voice: "omit text unless load exceeds 10s; use specific progress copy if used"
anti_patterns:
  - "Flash of loading (rendering skeletons for <300ms fetches)"
  - "Skeleton drift (skeletons dimensionally out of sync with target component causing CLS)"
  - "Spinner-by-default (using circular spinners for full-page loads > 1s)"
  - "Empty-state-as-error (using cheerful onboarding illustrations for 403/500 errors)"
  - "Over-nested suspense (wrapping every leaf node in a loader, causing UI popcorn)"
reference_instantiations:
  - { id: "atlassian-design-system", notes: "Rigorous distinction between Blank Slate and Empty State." }
  - { id: "cloudscape", notes: "Exhaustive Error Boundary and Zero-Results taxonomy." }
  - { id: "react-suspense", notes: "Declarative boundary pattern resolving layout thrash." }
relations:
  composes: [skeleton, spinner, empty-state, inline-message]
  relates-to: [notification-orchestration, error-pages]
  boundary: >
    Validates foundations-exile distinction: Bare disabled/loading rules are foundations.
    A single Empty State is a component. View-state orchestration is the logic coordinating
    WHEN to switch between them across a region. Notification orchestration handles background/global
    events; view-state handles foreground/regional events.
notes:
  - contested: "Duration thresholds (Viget study vs Wroblewski original assertions)."
  - verified: "Shift toward streaming SSR / React Suspense declarative boundaries over imperative state flipping."
```

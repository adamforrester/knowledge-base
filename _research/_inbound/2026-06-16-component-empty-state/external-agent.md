# Empty State — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/empty-state.md`; version numbers and the no-results-announcement AT specifics flagged unverified. The two passes converged almost completely; the external pass added the FOES trap, the table-replacement methodology, the SVG dark-mode/currentColor trap, the Atlassian headingLevel prop, and the Carbon Why+What error mapping.*

---

Empty State Component Research Report

## 1. Framing
The Empty State is the terminal rendering of a data container with no content — the fifth and final Feedback element, closing the category. It transforms an unacceptable blank container (a dead end) into an actionable, contextual waypoint. The container is a state machine: idle -> loading -> {content | empty | error | prohibited access}. Empty State handles EXPECTED absence + authorization barriers — strictly demarcated from loading (Skeleton/Progress) and system error (Banner/Inline). The heuristic: an empty result means the system worked but found nothing; a 500 means it failed entirely. Five genres drive the absence: first-use/onboarding (no data ever created — the highest-value, the user's first impression, prominent create CTA), no-results (a query returned zero — adjust parameters), user-cleared/all-done (inbox-zero success), error/failure (a localized container load failure — degrades to an error-flavored empty state to hold the layout), no-permission (data exists but the user lacks access — request-access workflow). Never leave a blank container.

## 2. Anatomy
Container (center-aligned flex/grid for a void; left-aligned/inline flex inside table rows; Primer uses container queries to scale padding/font in narrow bounds). Visual (inherits Icon for lightweight systemic, or a dedicated SVG illustration — Spectrum names the whole component IllustratedMessage; Atlassian guides degrading to a system icon for high-density). Heading (elevated typographic scale, the structural identifier). Body/description (lower-contrast, context + next steps). Primary action (inherits Button — high-prominence CTA). Secondary action (tertiary Button or Link — docs/permissions).

## 3. Properties / API
Architectural schism: Monolithic (Polaris/Primer/Atlassian/Ant — heading/description/image/primaryAction/secondaryAction props; rigorous tokens but low flexibility — traps when injecting rich HTML / troubleshooting lists / multiple buttons into string props; leads to margin-override/"unsquish" requests) vs Composable (Chakra/Radix-inspired — <EmptyState.Root>/.Content/.Indicator/.Title/.Description; inversion of control, slots nested lists/multi-button arrays via children; polymorphic as/asChild). A contested property: the heading-level injector — hardcoding <h3>/<h2> violates WCAG if it breaks the outline; Atlassian exposes headingLevel (default 4).

## 4. States and variants
No intrinsic interactive states (a layout wrapper delegating to Button/Link). States = genre taxonomy. first-use (highest prominence — full-color illustration, encouraging heading, value-prop description, high-contrast create CTA; onboarding). no-results (compact/utilitarian — monochrome icon e.g. magnifying glass, not a heavy illustration). user-cleared (celebratory but restrained — checkmark, often omits the primary CTA). error (strips decorative delight — warning icon, Retry/Reload/Clear). no-permission (lock/restricted badge, Request Access). Variant sizing: full-page (center viewport, max padding, large scale) vs in-card/in-section (tighter padding) vs compact (horizontal icon+text, save vertical space) vs empty table row (strip description + illustration, text only).

## 5. Usage guidance
Leaving a blank container is an anti-pattern (dead end, degrades trust). Implement across Table/List/Tree. The table-empty-state trap: rendering column headers alongside an empty message creates cognitive load + makes SRs announce empty table semantics first. IBM Carbon: complete replacement — unmount the entire table shell (headers/pagination/footers), replace with the Empty State. Polaris debated this — hiding headers during active filtering disorients users who need to remember the columns. Compromise: full replacement for first-use; inline replacement (preserve headers) for transient no-results. Genre->action mapping: first-use -> primary Button (adoption); no-results -> secondary Button/Link (clear filters/broaden — exploratory mode); error -> retry escape hatch; user-cleared -> empty action slot (let them bask) or a subtle home link. The Empty State is a localized just-in-time onboarding surface (vs intrusive modal tours).

## 6. Accessibility
Distinguish static DOM rendering from dynamic transition announcement. The Empty State is rendered HTML content — strictly NOT a live region; wrapping it in aria-live/role=alert is disastrous (spontaneously reads paragraphs + alt + button labels on data vanish, disorienting). The requirement centers on the dynamic no-results announcement: when a search/filter empties the container, a permanently-mounted off-screen role=status aria-live=polite element (reusing Toast's pattern) updates to "No results found"/"0 items returned", decoupled from the Empty State DOM. Focus management: WAI-ARIA forbids moving focus to the empty state heading/CTA on no-results — focus must remain in the search input (the user needs to backspace/broaden). Illustrations: redundant alt creates audible clutter (heading/description already state the context) -> aria-hidden=true on inline SVGs, or null alt="" + omit title on img. Document outline: if the container is under an <h2>, the empty-state heading must be <h3> — hardcoding destroys the semantic tree / rotor navigation.

## 7. Content guidelines
Headings: positive active statements ("Start by adding a project"/"Your inbox is clear"), not "No data" or hostile "You don't have any projects" (Intuit: don't shame users). Body: a strict Why + What heuristic. Carbon's error-condition mapping: Permissions (state the lack of access + how to request); Systems (note the external failure + a status log/retry); Configuration required (explain unconfigured + the first step); Action not supported (note the invalid parameter + the supported formats). Action labels: imperative verbs matching the heading ("Create project"/"Clear filters"/"Request access"), never "OK"/"Click Here"/"Submit". i18n: avoid abbreviations (don't translate out of context), keep sentences short for ~1.5x German expansion. NNG: prioritize constructive advice over technical precision, adapt to human error over exposing fault codes.

## 8. Motion
Restrained, deliberately paced. The component appears when content is removed/fails; aggressive animation (bouncing illustrations, sliding text) draws frantic attention to the absence. Minimal fast-easing fade-in (150-200ms). A high-visibility failure: Polaris's image is opacity:0 in CSS, relying on JS to append a Polaris-EmptyState--loaded class to fade in once the asset loads; during rapid client-side routing/unpredictable remounts, the load event fails to fire, trapping the image at zero opacity — a massive whitespace gap. Favor pure CSS @keyframes over brittle JS class toggling tied to async load events. Respect prefers-reduced-motion (snap to full opacity instantly).

## 9. i18n
RTL: center-aligned states stay stable; horizontal variants with hardcoded margin-left/right break — use logical CSS (margin-inline-start/end) so the illustration mirrors. Text expansion: descriptions expand up to ~50%; the container (often a small card) must use flexible flexbox not fixed heights so multiline wraps without clipping the action button. Illustration cultural neutrality: human figures, hand gestures, culturally specific clothing, hyper-localized metaphors fail globally and can offend; lean to abstract geometric/systemic iconography.

## 10. Naming
Primer Blankslate (generic placeholder). Spectrum IllustratedMessage (visual-centric, status updates). Ant Empty. The consensus (Polaris/Atlassian/Chakra/Carbon): EmptyState / Empty State — reflects the terminal-state-machine mental model of React/Vue/Svelte. Deprecate NoData/ZeroState/BlankSlate aliases for lexicon unity.

## 11. Implementation notes
Deterministic rendering mirroring the container lifecycle: an empty array intercepts the data map and mounts the Empty State. The Flash of Empty State (FOES) trap: an array is initialized empty before the request resolves; checking length without network status flashes the empty state for milliseconds before the skeleton/data. Enforce: if (!isLoading && data.length === 0) return <EmptyState/>. SVG dark-mode trap: Ant's default Empty relies on multi-layer SVGs that fail to adapt on dark theme (blazing white). The fix: PRESENTED_IMAGE_SIMPLE (hooks design tokens colorFill/colorBgContainer); robust implementations ensure SVGs accept currentColor for fill/stroke so CSS variables manage light/dark. Composable architecture (children / Chakra parts) lets consumers inject arbitrary DOM without the design system releasing minor updates for edge-case props (tertiary buttons, legal disclaimers, filter-clearing logic).

## 12. Related and alternative components
Button (composes for primary/secondary action slots — inherits tokens). Icon/Illustration (visual hierarchy + aria-hidden). Link (inline guidance/docs). Toast (the off-screen status live region borrows its accessibility architecture). Skeleton/Progress (the loading state — the immediate predecessor; transition without flashing). Banner/Inline Message (the error state — Banner = systemic failure that blocks; Empty State = expected absence/localized fault). Table/List/Tree (the primary consumers — compose the Empty State when array length is zero).

## 13. Field POV evolution
From a utilitarian technical fallback (dumping "404"/raw error codes/dead-end blanks) to a lucrative user-acquisition/onboarding surface (product-led growth — pitching the feature's value in the empty space). The Illustration question: the flat-design era's massive bespoke-illustration libraries proved costly (maintenance, cross-platform consistency, cultural neutrality, dark-mode incompatibility) -> sobering restraint, leaning to monochrome systemic icons for all but high-value first-use. Architectural maturation: monolithic -> composable parts. Accessibility consensus settled: decouple the static visual rendering from the dynamic status live-region announcement.

## 14. Sources cited
Shopify Polaris EmptyState v13.9.5. Adobe Spectrum IllustratedMessage v3.47.0. GitHub Primer Blankslate v38.26.0. Atlassian EmptyState v7.6.1/v7.4.10. Ant Design Empty v6.4.4. Chakra UI EmptyState (latest). IBM Carbon Empty states pattern (latest). Google Material 3 Empty states (latest). Base Web Empty State (latest). WAI-ARIA APG Alert and Status Live Region guidelines (latest).

## 15. Agent-consumable schema

```yaml
name: Empty State
description: The terminal rendered content of a data container when there is nothing to display, offering contextual guidance, explanations, and actionable next steps to prevent user dead ends.
category: Feedback
anatomy:
  - container: flex/grid centered, or inline flex for tight rows
  - visual: inherits Icon or an SVG illustration; avoid over-illustration
  - heading: primary identifier; requires dynamic heading-level injection
  - description: secondary block — why it is empty + what to do
  - primaryAction: inherits Button; main CTA
  - secondaryAction: inherits Button (tertiary) or Link; escape hatch/docs
api:
  - root: {size: [sm, md, lg], asChild: boolean, headingLevel: number}
  - composition: prefers modular sub-components over monolithic string props
states:
  - firstUse: high prominence, onboarding focus, primary create CTA
  - noResults: compact, icon-driven, clear-filter secondary CTA
  - userCleared: celebratory visual, no primary CTA
  - error: stripped utility, warning icon, retry CTA
  - noPermission: security focus, lock icon, request-access CTA
variants: {layout: [full-page, in-card, in-row, in-section], visual: [illustrated, iconOnly, textOnly]}
accessibility:
  - liveRegion: the visual DOM node is NOT aria-live (causes SR spam)
  - dynamicAnnouncement: a visually hidden role=status aria-live=polite announces "No results found"
  - focusManagement: focus MUST stay in the search/filter input; never steal to the empty state
  - decorativeImages: aria-hidden=true / alt="" on non-informative SVGs
content:
  - tone: positive/encouraging/helpful; never blame; no hostile wording
  - errorMapping: declare permissions/system/configuration (Why + What)
motion:
  - appearance: 150-200ms minimal fade-in
  - trap: avoid opacity:0 locked by a missing JS load class during client-side routing
i18n:
  - rtl: logical properties (margin-inline-start/end)
  - textExpansion: flexible flexbox wrapping; ~1.5x expansion
  - imagery: culturally neutral iconography over localized human illustrations
implementation:
  - logic: if (!isLoading && data.length === 0) return <EmptyState/> (prevents FOES)
  - visual: SVGs must accept currentColor for dark-mode compatibility
```

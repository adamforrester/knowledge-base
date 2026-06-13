---
type: practice-area
title: Accessibility Annotation Contract
description: What designers specify in Figma so engineers can implement accessibility faithfully. Per-concern annotation spec across mobile (iOS, Android, Flutter, Compose, RN) and web (ARIA, forced-colors, prefers-reduced-motion, landmark, headingLevel, inert).
tags: [extension, accessibility, a11y, figma, handoff, mobile, web, aria]
timestamp: 2026-06-13
---

# 17 — The Accessibility Annotation Contract

> What designers specify in Figma so engineers can implement accessibility faithfully — without guessing, without retrofitting, and without the contract evaporating between handoff and PR. This is the practice's annotation spec, derived from the implementation depth in 16-mobile-accessibility-implementation across the four mobile frameworks (iOS native, Android native, Flutter, Compose, React Native) and 28-web-accessibility-implementation for the web. The mobile contract was the first complete pass (May 2026); the web extension was added as the second (June 2026). The shape of the contract is the same — per-concern fields, framework-specific implementation, plus a small set of web-only fields the mobile contract does not need.

---

## Why this is a separate document

A design system that "ships accessible components" without an annotation contract puts the burden on every engineer to infer accessibility intent from visuals. That inference fails in predictable ways — interactive icons without roles, modals without focus return, gestures without alternatives, photos that invert into negatives, headings declared visually but not semantically. The annotation contract closes the inference gap. It is the single artefact that the design system can show a client when asked "how do you guarantee accessibility in the delivered build."

The contract has three audiences. Designers fill it in during handoff. Engineers consume it during implementation. QA and accessibility auditors read it during conformance verification. The structure below is shaped by all three needs.

---

## The contract, by concern

Each concern below specifies: what the designer marks, what the engineer implements, where in the design file the annotation lives, and what happens when it is missing.

### 1. Accessible name

**What the designer specifies.** The exact string that a screen reader will announce. Not the visible label — the spoken label, which is sometimes longer ("Add to favourites") and sometimes the same. For decorative imagery, the annotation is "decorative" rather than a string. For brand marks and logos with text content, the annotation may be the brand name even if the visual is purely a wordmark.

**What the engineer implements.** Flutter: `Semantics(label: ...)`. Compose: `contentDescription`. SwiftUI: `.accessibilityLabel(_:)`. UIKit: `accessibilityLabel`. React Native: `accessibilityLabel`. **Web:** in priority order: visible text content (the default; do not annotate anything else), `aria-labelledby` (when the visible label exists elsewhere in the DOM), `aria-label` (icon-only or when visible text is wrong). The annotation declares which mechanism — the system should not let engineers pick.

**Annotation location.** A field on every interactive element and every meaningful image in the component spec. Plain text. Localised — annotated names follow the same translation pipeline as visible copy. (See 13-internationalization-and-rtl for the i18n architecture.)

**What happens when missing.** The framework either falls back to the visible text (often correct, sometimes embarrassing — "Add to favourites button button"), reads "image" with no description (failure), or reads the asset filename ("ic_heart_outline_24"). The default is always wrong for production. On web, `aria-label` on non-interactive elements is silently ignored (see 28 §1).

**Rules:**

- Do not include the role word ("button," "link," "image"). The platform appends it.
- Names should make sense out of context. A button reading just "More" is useless in a screen-reader rotor list of all buttons.
- Names should not include keyboard shortcuts, hover hints, or visual state ("hovered," "focused").

### 2. Role

**What the designer specifies.** The semantic role of the element. Button, link, header, search field, tab, image, alert, dialog, switch, checkbox, radio, slider, progress, menu, list item. For custom components that simulate a native role (a card-shaped button, a custom toggle), the role of the simulated element.

**What the engineer implements.** Flutter: flags on `Semantics` (`button: true`, `header: true`) plus `SemanticsRole` where supported. Compose: `Modifier.semantics { role = Role.Button }`. SwiftUI: `.accessibilityAddTraits(.isButton)`. UIKit: `accessibilityTraits = .button`. React Native: `accessibilityRole = 'button'`. **Web:** the HTML element first (`<button>`, `<a href>`, `<input type="...">`, `<select>`, `<textarea>`, `<dialog>`); ARIA `role="..."` only where no native element fits or the system widget is Tier 2 / 3 per APG (see 28 §4). For Tier 2 composites, the annotation cites the APG pattern name (Combobox 1.2, Listbox, Tablist, Tree, etc.); engineering implements per APG.

**Annotation location.** A required field on every interactive element. Defaults are acceptable when the component is a native primitive being used in its native role (a `Button` is a button) — the annotation is required for custom-built or composed components, and recommended on all primitives for unambiguity.

**What happens when missing.** Screen readers either guess (sometimes correctly, often not) or treat the element as a generic group. Voice Control users cannot reach the element by name because the framework cannot tell what kind of element it is. Appium tests cannot select by role.

### 3. State

**What the designer specifies.** The dynamic state of the element when it varies meaningfully: selected/unselected, checked/unchecked, expanded/collapsed, disabled, busy/loading, toggled-on/toggled-off, current page in a paginated set. Visual-only states (hover, pressed) are not annotated; the framework handles them.

**What the engineer implements.** Flutter: `Semantics(selected: true, enabled: false, checked: true, toggled: true)`. Compose: `Modifier.semantics { selected = true; stateDescription = "Connecting" }`. SwiftUI: trait combinations (`.isSelected`, `.isToggle`) plus `.accessibilityValue(_:)` for state strings. UIKit: combine `accessibilityTraits` with `accessibilityValue`. React Native: `accessibilityState = { selected: true, disabled: false, expanded: true, busy: false }`. **Web:** native `<input>` attributes where they exist (`checked`, `disabled`, `readonly`, `required`); ARIA `aria-pressed`, `aria-selected`, `aria-expanded`, `aria-checked` (with tri-state support), `aria-current` per APG. The system pairs the visual rule (`:user-invalid`) with the AT rule (`aria-invalid`) — both fire after the user has engaged with the field, not on render (see 28 §6).

**Annotation location.** A row on the component's state table — one row per state, with the annotation for what the screen reader announces when that state is active.

**What happens when missing.** Stateful components read identically in different states. A toggle that visually changes colour but doesn't update its state semantically is silent to assistive tech. This is one of the highest-yield areas to audit on an existing system.

### 4. Value

**What the designer specifies.** For controls that have a magnitude, position, or progress — slider percentage, page-of-N for carousels and pagers, progress count, count of items in a list, "step 2 of 4" in a wizard. The string format the screen reader should announce, with placeholders for the dynamic numbers.

**What the engineer implements.** Flutter: `Semantics(value: 'Page 2 of 5')` plus `onIncrease`/`onDecrease`. Compose: `Modifier.semantics { progressBarRangeInfo = ProgressBarRangeInfo(...) }`. SwiftUI: `.accessibilityValue("50 percent")` or `.accessibilityAdjustableAction`. UIKit: `accessibilityValue` plus `.adjustable` trait. React Native: `accessibilityValue = { min, max, now, text }`. **Web:** native `<input type="range">`, `<progress>`, or ARIA `aria-valuenow` / `aria-valuemin` / `aria-valuemax` / `aria-valuetext` for custom widgets.

**Annotation location.** On every adjustable, incrementable, or progress-bearing element. The annotation includes both the value format and whether the user can change it via the increment/decrement gesture.

**Special case — carousels and horizontal pagers.** Every carousel needs `value` ("Page X of N"), `onIncrease`/`onDecrease` actions, and `liveRegion: true` so the screen reader announces the page change. This is the single highest-yield carousel annotation and is required for every carousel in the design system by default.

### 5. Focus container, merging, and traversal

**What the designer specifies.** Whether a compound element (a card, a list row, a header with multiple subcomponents) is one focus stop, one focus stop with custom actions, or a container the user enters to interact with children individually. For each option in a stateful navigation (tabs, accordions), the traversal grouping.

**What the engineer implements.** Flutter: `MergeSemantics` for one stop; per-child `Semantics` for entered containers; `ExcludeSemantics` for hidden subtrees. Compose: `Modifier.semantics(mergeDescendants = true)` for merged; `Modifier.clearAndSetSemantics { }` for clean override. SwiftUI: `.accessibilityElement(children: .combine | .contain | .ignore)`. UIKit: `isAccessibilityElement` plus `UIAccessibilityContainer` for entered containers. React Native: `accessible={true}` for merged, no `accessible` for entered, `accessibilityElementsHidden` / `importantForAccessibility="no-hide-descendants"` for excluded. **Web:** DOM source order is the canonical traversal mechanism; CSS reorder (flex / grid `order`, `flex-direction: row-reverse`) does not affect tab order. When source order must differ from visual order, the annotation declares the intended order explicitly. For Tier 2 composites, the annotation declares whether internal focus uses **roving tabindex** (the recommended default) or **`aria-activedescendant`** (only when DOM focus must remain on the parent — see 28 §2).

**Annotation location.** On every compound component. Three values: `merged` (one focus stop), `container` (entered to access children), or `hidden` (excluded entirely from accessibility tree).

**Plus traversal order.** When the visual layout diverges from logical reading order — circular layouts, responsive reflows, stacked overlays — the designer specifies the traversal order as a numbered sequence on the frame. The engineer implements via the framework's traversal-order primitive.

**What happens when missing.** Default merging is sometimes right and sometimes catastrophic. A card with title, subtitle, price, and four buttons read as one long announcement followed by no clear way to invoke the buttons is what happens when the default takes over and was wrong.

### 6. Focus management around transitions

**What the designer specifies.** For modals, sheets, dialogs, popovers, and any other dismiss-and-return interaction: which element receives focus when it opens, and which element receives focus when it closes. For routes that push new screens: which element receives focus on arrival, if not the default.

**What the engineer implements.** Initial focus via `autofocus`-style flags or `@AccessibilityFocusState` (SwiftUI), `FocusRequester` (Compose), `FocusNode.requestFocus` (Flutter), `AccessibilityInfo.setAccessibilityFocus` (RN), `UIAccessibility.post(.layoutChanged, argument:)` (UIKit). Return focus via the same primitives, called on dismissal. **Web:** `<dialog>` + `showModal()` handles initial focus, focus trap, Escape dismissal, and surrounding-document `inert` automatically; manual focus management is needed only for popover-API usage and pre-`<dialog>` legacy patterns. The annotation declares the **focus-return target** explicitly (default is the trigger that opened the surface; some patterns differ — a delete confirmation, on success, returns focus to the next item in the list, not the deleted one). For SPA route changes, focus moves to the new view's `<h1>` or `<main tabindex="-1">` and an optional polite announcement fires.

**Annotation location.** A required field on every modal, sheet, dialog, and overlay component. Two values: initial focus target (usually the first interactive element or the close button) and return target (usually the trigger that opened the modal).

**What happens when missing.** Focus returns to the top of the screen, the user loses their place, the modal-dismiss interaction becomes incoherent for screen reader and keyboard users. This is one of the most common accessibility failures in shipped mobile apps and one of the easiest to spec.

### 7. Dynamic-type behaviour

**What the designer specifies.** How the component reflows at increased text size. For typical components: nothing (the layout flows automatically). For horizontal-icon-plus-text layouts: the wrap or reflow strategy at AX1 / 200% scale. For fixed-size design primitives (buttons, app bars, badges): what gives way — the height grows, the icon hides, the label wraps, the badge moves to a separate line.

**What the engineer implements.** Flutter: `MediaQuery.textScalerOf` plus conditional layouts. Compose: `BoxWithConstraints` or branching off `LocalConfiguration.current.fontScale`. SwiftUI: `@Environment(\.dynamicTypeSize)` plus HStack-to-VStack swap. UIKit: Auto Layout constraints branching on `traitCollection.preferredContentSizeCategory`. React Native: `useWindowDimensions().fontScale` plus conditional layout. **Web:** browser-native — type tokens use `rem` against a user-configurable root font size, container queries (`@container`) drive responsive layouts, `clamp()` produces fluid type. The system enforces `rem`-based sizing across the type scale so the user-agent's text-size setting takes effect (see 23-typography-tokenisation for the architecture). Annotation is needed only where the component has a fixed-height affordance that breaks at scale — a badge, a one-line truncated label, an icon-with-text row.

**Annotation location.** A "scale behaviour" frame variant for each component, showing the layout at default, 130%, 200%, and AX5. Components that don't change between these values can be marked "static — flows naturally." Components that do need explicit frame variants.

**What happens when missing.** Buttons truncate, icons squeeze labels into illegible columns, app bars overflow, fixed-height containers crop text. The user with 200% scaling cannot use the app.

**Rule:** `maxFontSizeMultiplier` capping (RN) and equivalent caps in other frameworks are tools of last resort, used per-component with documented rationale, never globally. A global cap is a WCAG 1.4.4 failure.

### 8. Behaviour under system inversion and contrast

**What the designer specifies.** Whether the element should be excluded from Smart Invert (typically: photos, brand-coloured icons, illustrations, charts) or should invert with the rest of the UI (typically: chrome, decorative shapes, neutral backgrounds). For "Increase Contrast" / "High Text Contrast" state: any alternate colour values that diverge from the design system's default contrast swap. Note that we don't typically need to annotate the contrast swap for components using design-system color tokens — the token system handles it. Only divergences need annotation.

**What the engineer implements.** SwiftUI: `.accessibilityIgnoresInvertColors(true)`. UIKit: `accessibilityIgnoresInvertColors = true`. React Native: `accessibilityIgnoresInvertColors` on a wrapper `<View>` (the prop is unreliable on `<Image>` directly). Flutter: platform channel — no first-class framework API. Compose: not directly supported; for Android forced colors, teams build a `CompositionLocal`. **Web:** `@media (forced-colors: active)` block per component, with `system-color()` keywords (`Canvas`, `CanvasText`, `ButtonText`, `Highlight`, etc.) replacing brand tokens; transparent borders that render against system colours preserve structural visibility. `prefers-contrast: more` triggers a high-contrast theme at the system level. `prefers-color-scheme` plus the WebKit-only `inverted-colors` query handle dark mode and the Smart Invert double-inversion pitfall (see 28 §3). The annotation declares which media-query responses each component carries.

**Annotation location.** An "invert behaviour" field on every image-bearing component. Default to "exclude" for photos and illustrative content. Default to "invert" for chrome and decoration. The default-to-exclude policy for media is required by the design system.

**What happens when missing.** Photos in a feed render as surrealist negatives. Brand icons lose their colour cues. The Smart Invert user is shown an app where everything is half-broken.

### 9. Motion behaviour

**What the designer specifies.** For every transition, animation, or motion in the design: the behaviour when Reduce Motion is enabled. Three values: `same` (the animation is small enough or essential enough to keep), `cross-fade` (replace lateral motion with an opacity fade), `snap` (skip the animation, jump to the end state).

**What the engineer implements.** Flutter: `MediaQuery.of(context).disableAnimations` and `accessibleNavigation`. Compose: gate animations on `Settings.Global.ANIMATOR_DURATION_SCALE`. SwiftUI: `@Environment(\.accessibilityReduceMotion)` plus conditional `withAnimation`. UIKit: `UIAccessibility.isReduceMotionEnabled`. React Native: `AccessibilityInfo.isReduceMotionEnabled()` plus Reanimated's `useReducedMotion` hook. **Web:** `@media (prefers-reduced-motion: no-preference) { ... }` wrapper pattern (default state is no animation; animation is opt-in). Foundation-layer motion-duration tokens carry a `reduce` variant so component code references a token rather than writing media queries. The system fails PR review on any component-level `@media (prefers-reduced-motion)` block. Programmatic `scrollIntoView` and View Transitions both need explicit reduce-motion gating (see 28 §3 and 19-motion-implementation-web).

**Annotation location.** On every transition spec. Most animations cross-fade safely. Parallax, sliding panels, scale transitions, and physics-based animations need explicit alternatives.

**What happens when missing.** Vestibular-sensitive users get motion sickness from animations the system told them not to play. WCAG 2.3.3 failure.

### 10. Gesture alternatives

**What the designer specifies.** For every drag, swipe, long-press, multi-finger, and motion-actuated gesture: an alternative single-tap interaction with a name. Swipe-to-delete needs a "Delete" action. Long-press-for-context needs "Show options." Drag-to-reorder needs "Move up" / "Move down." Pinch-to-zoom needs explicit zoom in/zoom out actions. Shake-to-undo needs a button.

**What the engineer implements.** Flutter: `Semantics(onIncrease: ..., onDecrease: ..., customSemanticsActions: ...)`. Compose: `customActions` in semantics. SwiftUI: `.accessibilityAction(named: handler:)`. UIKit: `accessibilityCustomActions = [...]`. React Native: `accessibilityActions = [...]` with `onAccessibilityAction` handler. **Web:** keyboard or button alternative for any drag, swipe, long-press, or motion-actuated gesture. WCAG 2.5.7 (Dragging Movements, 2.2 AA). For drag-and-drop file upload, the underlying `<input type="file">` remains for keyboard and AT users; the drop zone is an enhancement. For reorder-by-drag, the annotation specifies "Move up" / "Move down" actions surfaced via menu or keyboard.

**Annotation location.** On every component with a gesture-only interaction. The label is what the screen reader announces in the rotor / actions menu; designers write it.

**What happens when missing.** The screen-reader user cannot perform the action. WCAG 2.5.7 (Dragging Movements, 2.2 AA) and 2.5.4 (Motion Actuation) failures.

### 11. Live-region intent

**What the designer specifies.** For every dynamic content region that updates without user input — search results count, form validation summaries, status banners, toast notifications, progress indicators, loading completions — whether the announcement is polite (waits for the screen reader to finish its current utterance) or assertive (interrupts).

**What the engineer implements.** Flutter: `Semantics(liveRegion: true)` for polite; `SemanticsService.sendAnnouncement` for explicit (use sparingly). Compose: `Modifier.semantics { liveRegion = LiveRegionMode.Polite | .Assertive }`. SwiftUI: `AccessibilityNotification.Announcement` with priority. UIKit: `UIAccessibility.post(notification: .announcement, argument:)`. React Native: `accessibilityLiveRegion="polite"` (Android) or `AccessibilityInfo.announceForAccessibility` (iOS, with the 200–400ms post-transition deferral). **Web:** `role="status"` (polite) or `role="alert"` (assertive) for new live regions; raw `aria-live="polite|assertive"` when a more specific role does not fit. The cardinal rule: **the live-region container must exist in the DOM before the text node is mutated** — the system ships a single persistent root-level `<LiveRegion>` provider that components push text into (see 28 §5). Per-component live regions are an architectural error.

**Annotation location.** On every dynamic region. Default to polite. Use assertive only with explicit rationale.

**What happens when missing.** Dynamic updates pass silently. The screen-reader user submits a form, sees a sighted person's eyes flick to the error message, but hears nothing. They re-submit. They re-submit again. They give up.

### 12. Tap target size

**What the designer specifies.** This is mostly a system-level constraint, not a per-component annotation — every interactive element in the design system meets the 44pt / 48dp minimum by default. Where the visual is smaller (a small close icon, a compact checkbox), the design system specifies the expanded touch area. Where the visual is at minimum, nothing is annotated (the default holds).

**What the engineer implements.** Flutter: `Material`'s `materialTapTargetSize` plus the `meetsGuideline` matchers in tests. Compose: `Modifier.minimumInteractiveComponentSize()` or `LocalMinimumInteractiveComponentSize`. SwiftUI: `.frame(minWidth: 44, minHeight: 44)` plus `.contentShape(Rectangle())`. UIKit: override `hitTest` or `pointInside`. React Native: `hitSlop`. **Web:** CSS `min-width` / `min-height` of 24×24 CSS pixels (WCAG 2.2 SC 2.5.8 AA) or 44×44 (SC 2.5.5 AAA) with appropriate spacing between adjacent targets; `padding` plus a transparent expanded hit area for visually-small affordances.

**Annotation location.** Component-level default; per-instance only when expanded.

**What happens when missing.** Tap targets shipped at 24dp or 16dp because they looked tight in the design. WCAG 2.5.5 (AAA) and 2.5.8 (AA, 2.2) failures. Motor-impaired users cannot reliably hit the target.

---

## Web-only fields

Five fields the mobile contract does not need; the web contract does. All derive from the platform's primitives covered in 28-web-accessibility-implementation.

### 13. Landmark and heading structure

**What the designer specifies.** For components that act as landmarks — the page header, the primary navigation, the main content region, complementary asides, the footer — the landmark role. For components that bear a heading — cards, sections, dialogs with titles — the *default* heading level for the typical use context, with the discipline that the component must accept a `headingLevel` prop so the consumer can override. A `Card` cannot hard-code `<h2>`; the consumer's document context decides.

**What the engineer implements.** Native `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<section aria-label="...">` elements where they fit; `role="banner"`, `role="navigation"`, `role="main"` only where the native element is unavailable. Headings are `<h1>` through `<h6>` driven by the `headingLevel` prop.

**Annotation location.** Component-level metadata for the default; per-instance only when the component is a landmark or carries a heading.

**What happens when missing.** Landmark navigation breaks; AT users cannot survey the page structure. Heading outline becomes incoherent — `<h2>` in one consuming surface, `<h4>` in another, no hierarchy across the document. This is one of the more-violated DS contracts in shipping product code (see 28 §2).

### 14. ARIA relationships (`aria-controls`, `aria-describedby`, etc.)

**What the designer specifies.** For components where ARIA relationships are part of the contract: which trigger controls which region (`aria-controls`), which message provides the description (`aria-describedby`), which message provides the error (`aria-errormessage`, with the hybrid `aria-describedby` fallback per 28 §6).

**What the engineer implements.** ARIA attributes pointing at DOM IDs (or, for web components, IDREF reflection via `ElementInternals` IDREF properties — see 28 §1).

**Annotation location.** A "relationships" diagram per component using arrows to indicate the linked elements. Designers draw the connections; engineering wires the IDREFs.

**What happens when missing.** Disclosure widgets do not announce their controlled regions. Form fields lose their help text on focus. Errors do not announce. The component looks accessible because each element has a name and role, but the relationships between them are silent.

**Avoid `aria-owns`.** WebKit and some Firefox configurations misnumber the child set. If the design requires reordering across the DOM, redesign to avoid it. The system should not allow `aria-owns` in component templates without explicit accessibility review (see 28 §1, §4).

### 15. `inert` regions and modal scope

**What the designer specifies.** For modal patterns and slide-out surfaces: which regions of the page become `inert` when the surface opens. With `<dialog showModal>`, the answer is "the rest of the page" automatically; with custom popovers or layered surfaces, the annotation declares the inert scope explicitly.

**What the engineer implements.** The HTML `inert` attribute on the appropriate ancestor when the surface is open; cleared when it closes.

**Annotation location.** A region overlay in the modal's spec frame showing what becomes `inert`. Default to "everything outside the dialog" for modal patterns; non-default scopes (e.g., "the side panel makes the main content `inert` but the page header stays interactive") need explicit annotation.

**What happens when missing.** Background content is reachable by Tab and announceable by AT while the modal is open. The modal is modal in look only — keyboard and AT users can interact with the obscured content underneath.

### 16. `forced-colors` survival

**What the designer specifies.** Per element, three values:

- **Survives unchanged** — works as-is in `forced-colors: active`. Default for native HTML elements.
- **Has a forced-colors variant** — the element has a specific `@media (forced-colors: active)` override (border in place of fill, `system-color()` in place of brand). The annotation declares what changes.
- **Custom paint stripped** — the element relies on `background-image`, gradient, `box-shadow`, or transparency, and has a forced-colors fallback re-establishing meaning via border, outline, or `system-color()`.

**What the engineer implements.** `@media (forced-colors: active)` blocks per component, with `system-color()` keywords (`Canvas`, `CanvasText`, `ButtonText`, `Highlight`, etc.). Transparent borders that render against system colours are the standard trick for restoring structural visibility on components without a default border (see 28 §3).

**Annotation location.** A frame variant in `forced-colors: active` simulation for components that need a variant. Components that survive unchanged are marked "default — no variant needed."

**What happens when missing.** WHCM users see components with stripped backgrounds, no borders, invisible focus rings, missing icons. The system is operable in look but illegible in fact.

### 17. APG keyboard model per composite widget

**What the designer specifies.** For Tier 2 composites (Combobox 1.2, Listbox, Menu / Menubar, Tablist, Tree, Treegrid, Grid, Disclosure, Tooltip, Toolbar — see 28 §4), the APG pattern name. The keyboard model is implied — Combobox 1.2 has a defined contract — and engineering follows APG. For Tier 3 bespoke widgets, the annotation must spell out keys. For Tier 1 native components, no annotation needed.

**What the engineer implements.** Per APG. For React systems: react-aria or Radix Primitives. For multi-framework: Ark UI. For web-component systems: Lit + Web Awesome's primitives. Building the keyboard model from scratch in 2026 is a yellow flag.

**Annotation location.** A field on the component metadata: `apgPattern: "combobox-1.2"`, etc.

**What happens when missing.** The composite ships with the keyboard model the engineer happened to implement. JAWS users encounter different behaviour from NVDA users; macOS VoiceOver users encounter different behaviour from iOS VoiceOver users. The component fails the AT × engine matrix.

---

## The shape of the annotation file

Two patterns work in practice; pick one per component library and hold it.

**Pattern A: annotation as a layer in Figma.** Each component has an "A11y" page or frame variant carrying the annotation table. Designers fill it in alongside the spec. Engineers consume it at build time. The advantage: lives where the design lives, can't be lost in handoff. The disadvantage: requires Figma discipline, and tables in Figma are awkward to maintain at scale. (See 12-figma-practice for the Figma-level treatment.)

**Pattern B: annotation as metadata in the component schema.** Each component carries an `accessibility` block in its design-token-aligned metadata file — the same components-as-data approach we use elsewhere. (See 03-component-library and 15-ai-in-ds.) The annotation is structured data, queryable, validatable, generatable into Storybook documentation and into accessibility test scaffolding.

Our practice's strong preference is Pattern B for systems mature enough to support it, Pattern A as the entry point, both as the bridging state. Pattern B is the only one that scales to AI-assisted code generation and ACR evidence pipelines.

---

## Defaults that obviate annotation

The annotation contract is not a requirement to annotate everything. It is a requirement to annotate where the framework default is wrong or absent. Where the default is right, no annotation is needed.

- **A `Button` with a text label** has the label as its accessible name and the role `button` by default. No annotation needed unless the spoken name should diverge from the visible text.
- **A `TextField` with an `InputDecoration.labelText` (Flutter) / `placeholder` (others)** has the label as its accessible name. No annotation needed.
- **A standard `Image` with `semanticLabel` set** is correct; only the choice between content and decoration needs annotation.
- **A Material 3 component used in its native role** has the role set automatically.

The annotation requirement scales with the deviation from primitives. A native `Button` needs almost nothing; a custom card with three actions and a swipe gesture needs the full contract.

---

## When the contract is contested

Three common contests with engineering teams worth pre-empting.

**"Why do we need to annotate when the framework defaults handle it?"** Because the defaults are right in some cases and silent in others, and we cannot tell which from a static review of the code. The annotation is the source of truth for what the design intended, independent of which framework happens to be implementing it. It also survives framework migrations and refactors that defaults do not.

**"The labels read out of context — can we make them shorter?"** Names should make sense out of context, which usually means longer than the visible text. A button reading just "More" in a rotor list of all the screen's buttons is useless. Cost is verbosity in one path; benefit is comprehensibility in another. The contract holds.

**"Custom actions in the rotor add clutter."** They do, and the alternative is users cannot perform the action. The cost is real but the trade is settled. Where rotor clutter is genuinely the problem, the design itself probably needs simplification — too many gesture-only interactions on one screen.

---

## Adaptive UI — the standing gap

This contract assumes a fixed surface designers can annotate ahead of build. Adaptive UI breaks that assumption — when the surface itself is generated per render, *what* gets annotated and *when* both shift. The reasonable interim discipline is to annotate the *component primitives* the LLM composes from (the slot types, the available components, the system prompt's "available UI design patterns" catalogue) rather than the rendered output, and to verify the rendered DOM in CI against the same field-by-field contract via in-pipeline accessibility scanning. This catches the 25–60% of WCAG violations automation reaches (see 28 §8 for the honest range); the remainder still needs manual testing with assistive technology, which becomes a standing engagement cost. (See 27-adaptive-interfaces-implementation §6.2 for the full verification gap; 26-adaptive-interfaces-foundations §4.1 for the ability-based-design evidence base that motivates the work.)

---

## See also

For the framework-level implementation depth underneath each annotation field on mobile, see 16-mobile-accessibility-implementation. For the same depth on web, see 28-web-accessibility-implementation.

For the architectural treatment of accessibility as a system concern — pair tokens, the four-layer model, conformance reporting — see 14-accessibility.

For the Figma-level treatment of how to structure annotation in component files, see 12-figma-practice.

For the components-as-data approach that underwrites Pattern B (annotation as structured metadata), see 03-component-library and 15-ai-in-ds. For the documentation architecture that surfaces it as machine-readable metadata, see 04-documentation.

---

## Provenance

The mobile fields (concerns 1–12) were pulled out of the synthesis that produced 16-mobile-accessibility-implementation, derived from cross-framework consensus across four dual-agent research runs filed 2026-05-13 (`_research/_inbound/2026-05-13-mobile-a11y-*/`). The web-specific elaborations on those concerns and the five web-only fields (concerns 13–17) were added from the synthesis that produced 28-web-accessibility-implementation, drawn from the dual-agent research run filed 2026-06-13 (`_research/_inbound/2026-06-13-web-a11y-implementation/`). The contract now covers both mobile and web; the residual standing gap is adaptive UI, where the surface is generated per render and the annotation target shifts to the component primitives.

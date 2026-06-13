You are researching web accessibility implementation for design systems for a senior design systems practitioner at a digital agency. The output is a structured knowledge document.

Context: our practice has architectural and per-platform accessibility positions documented for design systems — the four-layer model (tokens / components / docs / contribution gates), pair tokens for contrast, ARIA encapsulation as a principle, conformance reporting under EAA and Section 508, and mobile implementation depth across Flutter, Jetpack Compose, SwiftUI/UIKit, and React Native, plus a per-component accessibility annotation contract derived from those four mobile frameworks. What we lack is the equivalent web implementation depth and the web extension of the annotation contract. Web teams currently retrofit ARIA, the user-preference media queries (prefers-reduced-motion, prefers-contrast, forced-colors, prefers-color-scheme), focus management primitives (`inert`, `focus-visible`, focus trapping), the ARIA Authoring Practices keyboard interactions for composite widgets, and complex `aria-controls` / `aria-owns` / `aria-describedby` relationships at PR review rather than building them into the system. This research fills that gap. The audience target is the same: a senior DS lead deciding what the system should encode by default, what designers must annotate per component, and what evidence the toolchain can produce for an ACR/VPAT. Cover the platform as it actually ships in mid-2026 — current ARIA 1.3, current Baseline status of relevant CSS features, current screen-reader behaviour on the four-engine surface (NVDA on Chromium and Gecko, JAWS on Chromium, VoiceOver on WebKit, TalkBack on Chromium-Android, Narrator on Chromium-Edge).

This is not an introductory accessibility guide — assume the reader knows WCAG 2.2, the difference between role/name/state, what a screen reader is, what a design system is, and the architectural argument for accessibility-as-system-feature. Explain web's accessibility primitives at the level a senior engineer or design systems lead needs to make implementation and annotation decisions, where the platform's defaults are good enough, where they are wrong or absent, and where assistive-technology behaviour diverges across engines.

Research scope — cover all of the following. Use these as the section spine of the output:

1. The accessibility primitives the web platform exposes

   - Native HTML semantics as the first line of defence; the "build on the element, not above it" principle and where it breaks down (custom controls, design-system buttons that aren't `<button>`).
   - ARIA 1.3 surface area: roles, states, properties; abstract roles vs. concrete roles; ARIA-in-HTML rules (sixth presentational rule, role conflict resolution).
   - The accessibility tree and how engines build it from DOM + computed style + ARIA. Where the four major engines diverge in computed accessible name/role/state.
   - The Accessibility Object Model (AOM) — current spec status, ElementInternals.role and .ariaXxx reflected properties, IDREF properties, where this changes things for custom elements.
   - Common pitfalls: redundant roles, role override on semantic elements, ARIA without keyboard, ARIA without focus, `aria-label` on non-interactive content, `aria-hidden` on focusable elements, label/labelledby precedence.

2. Focus and keyboard

   - The native focus model — `tabindex`, `tabindex="-1"`, `tabindex="0"`, why positive tabindex is broken in practice.
   - `:focus-visible` as the system primitive for focus indication; the `:focus`/`:focus-visible`/`:focus-within` distinction; design-system implications for focus-ring tokens.
   - `inert` (Baseline since 2023) as the modern primitive for disabling interaction; when to use vs. focus trapping; behaviour with assistive tech.
   - Focus trapping and focus return for modal patterns — what `<dialog>` and the popover API give you; what they don't; when to write a manual trap.
   - Keyboard interaction patterns for composite widgets per ARIA Authoring Practices Guide (combobox, listbox, menu, menubar, tablist, tree, grid, treegrid). What the system encodes vs. what the application supplies.
   - Roving tabindex vs. aria-activedescendant — when to use which; what each engine handles correctly.
   - Skip links, landmark navigation, the heading outline; whether the practice still ships skip links by default.

3. User preferences and the media-query surface

   - `prefers-reduced-motion`, `prefers-reduced-transparency`, `prefers-reduced-data`, `prefers-contrast`, `prefers-color-scheme`, `forced-colors`, `inverted-colors`. Current Baseline status of each (verify against caniuse / Web Platform Status).
   - `forced-colors` mode (Windows High Contrast Mode) — how it overrides paint, what survives, the `system-color()` keywords (`CanvasText`, `Canvas`, `LinkText`, `ButtonFace`, etc.), how to preserve meaning when the design system's color tokens are stripped.
   - The reduce-motion contract — what a design system encodes once at the foundation layer (motion tokens that respect the query) vs. what each component decides locally (informational vs. decorative; vestibular triggers like parallax).
   - `prefers-contrast: more` and the relationship to WCAG enhanced contrast; whether brands have a formal high-contrast theme or rely on the user-agent's default.
   - System-level color inversion and dark mode interplay; double-inversion pitfalls; opting media out of inversion.

4. Composite widget patterns and the ARIA Authoring Practices contract

   - When the design system implements a custom widget vs. wraps a native control. The "use the platform" rule and where it loses (combobox, multi-select, tree, complex grid).
   - Per-pattern coverage with the keyboard model: Combobox 1.2, Listbox, Menu/Menubar, Tablist, Tree, Treegrid, Grid, Disclosure, Dialog, Tooltip, Toolbar.
   - How each pattern maps to ARIA roles and required relationships (`aria-controls`, `aria-owns`, `aria-activedescendant`, `aria-expanded`, `aria-selected`, `aria-current`).
   - Where APG guidance disagrees with current AT behaviour (the well-known Combobox autocomplete issues, the `aria-owns` cross-engine support gap, JAWS's table reading mode quirks).
   - Library landscape — react-aria, Radix, Headless UI, Reach UI legacy state, Ark UI, Web Awesome / Shoelace. Which of these are credible for the system to depend on; which problems they solve and which they punt.

5. Live regions, announcements, and dynamic content

   - `aria-live` (`polite`, `assertive`, `off`), `aria-atomic`, `aria-relevant`, `role="status"`, `role="alert"`, `role="log"`, `role="timer"`, `role="marquee"`. What each engine actually does with each.
   - The "live region must exist before the change" rule and how design-system components must architect their live-region holders.
   - Toast / snackbar / inline error / form-level error patterns and which live-region role applies.
   - The status-message problem (WCAG 2.2 SC 4.1.3) — why automation can verify presence of the live region but not whether the message was announced.
   - Initial-load announcements, navigation announcements in single-page applications, route-change announcement patterns.

6. Forms, errors, and the input contract

   - Native `<form>`, `<label>`, `<input>`, `<select>`, `<textarea>`, `<fieldset>`/`<legend>` and where they remain best-in-class.
   - Constraint validation API, `:user-invalid` / `:user-valid` (Baseline 2024 — verify), the `invalid` event, custom error messaging.
   - `aria-describedby` for help and error text; `aria-invalid` and its relationship to `:user-invalid`; `aria-errormessage` (current support).
   - Required-field indication patterns, optional-field indication patterns, error-summary patterns.
   - Date pickers, combobox, file upload, drag-and-drop file input — where native is now strong enough vs. where the system must provide.
   - Auto-fill, autocomplete attributes and their accessibility implications (WCAG 1.3.5).

7. Color, contrast, and the visual layer

   - WCAG 2.x contrast vs. APCA — current state, where APCA stands relative to WCAG 3, whether the practice should ship APCA-aware tooling.
   - Color contrast across themes (light/dark) and densities; the pair-token model from 14-accessibility on the web specifically.
   - Contrast for non-text content (UI components, graphical objects) — SC 1.4.11 — what the system enforces in tooling.
   - Focus-indicator contrast (SC 2.4.13 in WCAG 2.2 AA — verify) and its interaction with branded focus rings.
   - Color is not the sole carrier of meaning — what the system encodes (icons paired with status colors, text labels, patterns); what designers must annotate per component.

8. Testing, tooling, and conformance evidence

   - Static analysis: `eslint-plugin-jsx-a11y`, axe linter, Storybook a11y addon, build-time accessibility checks.
   - Runtime/automation: `axe-core`, Playwright + axe, Cypress + axe, Pa11y; what they catch (~30–40% per axe-core's own published figure — verify with current axe documentation), what they miss.
   - Storybook accessibility addon, Chromatic accessibility scanning, Component-level a11y test patterns.
   - Manual testing with the four engines × the four major screen readers; the device matrix the practice should ship.
   - Browser DevTools accessibility panels — Chromium's full accessibility tree, Firefox's accessibility inspector, WebKit's audit tab; what each is good for.
   - VPAT/ACR evidence — what automation produces, what manual auditing must produce, how to package the evidence for procurement.
   - Continuous monitoring: production a11y dashboards, regression detection, the role of synthetic vs. real-user accessibility metrics.

9. The Figma annotation contract for web

   - Given everything above, what must a designer specify in Figma so a web engineer can implement a component without guessing? The mobile contract (17-accessibility-annotation-contract) covers accessible name, role, state, traversal, dynamic-type/scaling, behaviour under inversion / forced colors, gesture alternative, live-region intent. Web extends this with: ARIA-specific fields (role, `aria-label` vs. visible label, `aria-describedby` targets, `aria-controls`/`aria-owns` relationships); `forced-colors` behaviour per element; `prefers-reduced-motion` treatment per animation; keyboard interaction per ARIA APG pattern; landmark/heading structure; `inert` regions in modal patterns; focus-return targets after dismiss.
   - Where web's defaults make annotation unnecessary, say so. Where the defaults are wrong or absent, the annotation is load-bearing — call this out.
   - How the web annotation rows map to component schemas (`.ai.json`, the four-layer documentation stack from 04-documentation, components-as-data from 03 and 15) so the contract can be machine-read by a code-generation pipeline, not just hand-implemented.

Output format: Structured markdown using the numbered scope as section headings. Synthesize — do not list sources mechanically. Where the field has clear consensus or one obvious choice (e.g. "use `<button>`, not `<div role="button">`"), state it; where decisions are context-dependent, give a decision framework rather than declaring a winner. Flag platform or tooling gaps that practitioners work around (e.g. `aria-owns` cross-engine support; APCA standardization; the "automation catches ~30%" ceiling). Where claims depend on current platform state — feature names, Baseline status, screen-reader behaviour, browser support, axe-core ruleset versions, ARIA spec version — date them and note the verification path (caniuse.com, Web Platform Status, MDN, ARIA spec, AT release notes). Include a references section linking to primary sources (W3C ARIA spec, WAI ARIA Authoring Practices Guide, WCAG 2.2, MDN Web Docs, web.dev, Web Platform Status, caniuse, axe-core docs, react-aria docs, Radix docs, NVDA / JAWS / VoiceOver / TalkBack release notes).

Depth: Expert audience. Do not explain what ARIA is or what a screen reader does — explain how the web platform's primitives expose the right semantics, where they fall short, where the four engines disagree, and what a designer must specify so an engineer can close the gap.

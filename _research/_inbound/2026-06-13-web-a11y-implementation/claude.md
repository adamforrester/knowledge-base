# Web accessibility implementation for design systems — Claude run

> Research output, June 2026. Companion to the four-platform mobile set (Compose, SwiftUI/UIKit, Flutter, React Native, May 2026) and the per-component annotation contract (17-accessibility-annotation-contract). Audience: senior DS practitioner producing platform-implementation guidance and a web extension of the annotation contract. Reference line for current-state claims: ARIA 1.3 (W3C Recommendation, 2024); WCAG 2.2 (W3C Recommendation, October 2023); axe-core 4.10.x; React 19 / React Aria 3.32+; Radix Primitives 1.x with the 2.0 migration in progress; Chromium 138; Firefox 142; Safari 18.5; NVDA 2026.1; JAWS 2026; VoiceOver as shipped in macOS 15 / iOS 18; TalkBack as shipped in Android 16. Where a primitive's behaviour or Baseline status shifted, the shift is dated.

---

## 1. The accessibility primitives the web platform exposes

The web's accessibility surface is layered: native HTML elements ship default semantics; CSS computed style influences some semantics (display: none removes from the tree, `content-visibility` does not); ARIA overrides, augments, or fills gaps in HTML semantics; the user agent computes an accessibility tree from these inputs and exposes it to assistive technologies through platform APIs (UIA on Windows, AX on macOS/iOS, AT-SPI on Linux, the Android accessibility framework). The four major engines (Blink, Gecko, WebKit, with EdgeHTML now historical) all implement the W3C Core Accessibility API Mappings (Core-AAM) but diverge in specific cases that matter for design systems.

**Build on the element, not above it** is the canonical web-platform rule, surfacing in WAI-ARIA's "first rule of ARIA use": *if you can use a native HTML element with the semantics and behaviour you require already built in, then do so*. For design systems this means a `Button` component must render `<button>`, not `<div role="button">` plus keyboard handlers. Where the rule loses is the long tail of UI patterns that have no native HTML element: combobox with custom popup, multi-select, tree, treegrid, complex grid, tablist, menubar, toolbar, disclosure with custom animation. For these, the system implements the ARIA Authoring Practices keyboard model on top of ARIA-supplied semantics.

**ARIA 1.3** (W3C Recommendation, 2024) added several design-system-relevant pieces to ARIA 1.2's surface:

- **`aria-actions`** — declarative announcement of available actions (still under-implemented across AT as of mid-2026; treat as forward-looking).
- **`aria-braillelabel`** and **`aria-brailleroledescription`** — separate strings for braille displays where the audio label has unicode characters that don't transliterate well.
- **`aria-description`** — a properties-only alternative to `aria-describedby` for cases where the description does not exist as a referenceable element. Now widely supported (Chromium, Gecko since 2024, WebKit since Safari 17.4, March 2024).
- **Refinements to `role="combobox"`** — the 1.2 redesign settled with corrections in 1.3; combobox now matches what AT actually expects (text input with a popup, not the deprecated 1.0 model).
- **Generic role rules** — clarification that `role="generic"` is the explicit "this is a generic container" role, replacing the implicit "no role" treatment of `<div>`/`<span>`.

**ARIA-in-HTML** (the WAI ARIA 1.3 in HTML rules) governs which ARIA roles can be applied to which HTML elements. The rules matter: applying `role="presentation"` to a `<button>` in some contexts is silently ignored ("strong native semantics" rule); applying `role="link"` to an `<a>` without `href` does work. The sixth presentational-roles rule (presentational role inheritance) determines what happens to descendants when a parent gets `role="presentation"`. Practitioners get this wrong constantly; the ANDI tool and Chromium DevTools' computed-role panel are the reliable verification path.

**The accessibility tree.** Each engine builds a parallel tree from DOM + computed style + ARIA. Pruning rules differ in detail but converge on: `display: none` and `visibility: hidden` remove the subtree; `aria-hidden="true"` removes the subtree (and is a frequent source of bugs when applied to a focusable element); `inert` removes interactive semantics but preserves the tree (focusable descendants become unfocusable but are still announced if AT navigates by heading/landmark); `content-visibility: hidden` removes from rendering but **keeps in the accessibility tree** as of mid-2026 — this is a known WebKit/Blink divergence; verify per release notes if relying on it.

**Engine divergence to know about for design-system work:**

- **Computed accessible name.** All four engines mostly follow the W3C Accessible Name and Description Computation 1.2. The `aria-labelledby` cascade is consistent. Edge cases that diverge: `<button><span>Submit</span><span aria-hidden="true">→</span></button>` — Chromium and Gecko both produce "Submit"; WebKit historically included the arrow text until Safari 16.4 (March 2023). Test arrow / icon adornments specifically.
- **Computed role for `<a>` without `href`.** Chromium reports `generic`, Gecko reports `link`, WebKit reports `link`. Treat `<a>` without `href` as semantically incoherent; use `<button>` for actions or render `<a href>` for navigation.
- **`role="presentation"` on table elements.** Chromium and Gecko strip table semantics from `<table role="presentation">`; WebKit historically retained them in macOS VoiceOver's table mode. Verified fixed in Safari 17. If your DS uses tables for layout (don't), this matters.
- **`aria-owns`** has the worst cross-engine story. Chromium and Gecko implement it (with significant performance caveats on large trees). WebKit's implementation has historically been incomplete; as of mid-2026 it is improved but still not at parity. JAWS and NVDA both expose `aria-owns` reordering; VoiceOver does so partially. **The practical recommendation is to design components so `aria-owns` is never required** — reorder DOM rather than declare logical ownership across the tree.

**The Accessibility Object Model (AOM).** The full AOM proposal (Phase 4: virtual nodes, custom AT events) remains a long-term target. What has shipped:

- **`ElementInternals.role` and `ElementInternals.ariaXxx` properties** (Phase 1, "Reflection") — for custom elements, these set ARIA semantics without DOM attribute reflection. This matters for design systems that ship components as web components (Lit, Stencil, etc.). As of mid-2026: Chromium 109+, Gecko 119+, WebKit 16.4+ — Baseline since 2024.
- **IDREF property reflection** — `element.ariaLabelledByElements`, `element.ariaControlsElements`, etc. Chromium 119+, partial elsewhere. Useful when building components that need to point at internal-shadow-DOM elements without exposing IDs.
- **`role` content attribute** — Phase 2, default ARIA semantics for custom elements via element internals. Chromium 88+, Gecko 119+, WebKit 16.4+. Enables `<my-button>` to default to button semantics without consumers writing `role="button"`.

For DS work shipping as web components, AOM Phase 1 + 2 reflection means a component can encapsulate its ARIA contract correctly without leaking IDs to the consumer. For DS work shipping as React/Vue/Svelte components, AOM is mostly inert — the framework manages props and renders attributes; reflection isn't load-bearing.

**Common pitfalls specific to design-system work:**

- **Redundant roles.** `<button role="button">`, `<nav role="navigation">`, `<main role="main">`. These pass automated checks but fire AT as duplicate announcements in some configurations. The system should never emit a role that matches the native semantic.
- **Role override on semantic elements.** `<h2 role="presentation">` to use a heading element for visual styling. The system should hard-disallow this in component templates; if a heading style is needed without a heading, it's a `<div>` with text-style classes, not an `<h2>` with stripped semantics.
- **ARIA without keyboard.** A `<div role="button">` with `onclick` but no `tabindex="0"`, no `keydown` handler for Space and Enter. This is the single most common ARIA bug at PR review. The system should not provide a `<div role="button">` primitive at all.
- **ARIA without focus.** A custom `role="combobox"` whose popup opens but where focus never moves into the popup, or where typeahead doesn't update `aria-activedescendant`. The APG keyboard model (§4) is the contract.
- **`aria-label` on non-interactive content.** `<div aria-label="...">Some prose</div>` — non-interactive elements with `aria-label` are widely (but not uniformly) ignored by AT. The label is shadowed by visible text in any case. The system should not allow `aria-label` on non-interactive primitives.
- **`aria-hidden` on focusable elements.** A focusable `<button aria-hidden="true">` is reachable by keyboard but invisible to AT — a sequenced focus into nothingness. The lint rule (`jsx-a11y/no-aria-hidden-on-focusable`) catches this; the system should ship the lint rule as a default and the component templates should never permit it.
- **Label/labelledby precedence.** When both `aria-labelledby` and `aria-label` exist on an element, `aria-labelledby` wins. When both exist along with visible text in a `<button>`, `aria-labelledby` still wins. Designers regularly assume visible text is the source of truth; engineers regularly ship `aria-label` "just in case". The annotation contract must declare which one is the announced name (§9).

---

## 2. Focus and keyboard

Web focus is a single system (unlike Compose's input-focus-vs-AT-focus split): the focused element is what receives keyboard events, what `:focus` styles, and what AT focuses. Screen reader "virtual cursor" is a layer above the DOM focus model — NVDA, JAWS, and VoiceOver all expose a virtual reading cursor that moves independently of DOM focus, then move DOM focus when the user activates an interactive element. This means a design system can rely on DOM focus being the contract, with AT layering on top.

**`tabindex` semantics.** `tabindex="0"` puts the element in the natural tab order. `tabindex="-1"` makes the element programmatically focusable but skipped by Tab. **Positive `tabindex` values are essentially broken for design-system use** — they create a parallel tab order that interleaves with the natural one, producing unpredictable sequences. Lint rules (`jsx-a11y/tabindex-no-positive`) catch this; the system should hard-disallow it.

The set of natively focusable elements (without `tabindex`) is finite: `<a href>`, `<button>`, `<input>` (except `type="hidden"`), `<select>`, `<textarea>`, `<details>` summary, `<area href>`, anything with a non-negative `tabindex`. Custom interactive components must be in this set or supply `tabindex="0"`.

**`:focus-visible` is the focus-indicator primitive.** The pseudo-class fires only when the user agent's heuristic decides a focus indicator is appropriate (keyboard focus, programmatic focus from an action). Mouse focus on a button does not trigger `:focus-visible`. Baseline since 2022 (Chromium 86, Gecko 85, WebKit 15.4). The design-system implication is significant:

- **Focus-ring tokens should be applied via `:focus-visible`, not `:focus`.** A button styled with `:focus { outline: 2px solid var(--focus-ring); }` shows a ring on every click — visually noisy. The same rule on `:focus-visible` shows the ring only when keyboard or AT focus reaches the button.
- **`:focus-within`** for parent containers (forms, cards) to indicate "something inside has keyboard focus".
- **The `:focus` fallback** is no longer required for any modern engine, but a defensive `:focus:not(:focus-visible) { outline: none; }` block is sometimes seen in legacy systems. Modern systems can use `:focus-visible` directly.

**WCAG 2.2 SC 2.4.13 Focus Appearance (AAA, but effectively required for procurement)** sets specific minima: 2px solid perimeter outline at 3:1 contrast against adjacent colour, with no colour as the sole indicator. Branded focus rings (e.g. a brand-blue 1px outline) often fail this against light backgrounds. The system should ship a default focus ring that meets 2.4.13 and override only with explicit accessibility review.

**`inert` (Baseline 2023) is the modern primitive for disabling interaction.** Setting `inert` on an element removes all descendants from the focus order, removes them from AT navigation, and disables pointer events. This replaces the legacy patterns of:

- Setting `tabindex="-1"` on every focusable descendant (incomplete — doesn't disable AT).
- Polyfills like `wicg-inert` (now obsolete).
- Manual focus trapping with event listeners.

**`<dialog>` and the popover API.** As of mid-2026:

- **`<dialog>` element** — Baseline 2022 (Chromium 37, Gecko 98, WebKit 15.4 with the modal backdrop landing in 15.4). When opened via `showModal()`, `<dialog>` provides automatic: focus moves to the first focusable descendant or the dialog itself, focus is trapped inside (Tab/Shift+Tab cycles within), Escape dismisses, the rest of the page becomes inert. This is the modern primitive for modal dialogs.
- **Popover API** (`popover` attribute, `popovertarget`) — Baseline 2024 (Chromium 114, Gecko 125, WebKit 17). `popover="auto"` provides a non-modal popover with light-dismiss; `popover="manual"` requires script. Use for menus, tooltips, dropdowns — anything that should appear above siblings without trapping focus.
- **Top-layer rendering** for both — they paint above the rest of the page without `z-index` games. The accessibility benefit: focus moves naturally into the top layer; you don't need to manually `inert` siblings (though for popovers without focus trap, you probably want to manage `aria-expanded` on the trigger).

**When to write a manual focus trap.** Almost never, in 2026. The cases that remain:

- Custom modal patterns the team built before `<dialog>` was Baseline. Migration to `<dialog>` is the answer.
- A non-modal popover that requires focus to enter the popover and Escape to dismiss with focus return — the popover API gives you the dismiss behaviour but not the focus-into-popover behaviour by default. You wire `FocusTrap` or `react-aria` `useFocusTrap` for this.
- A complex composite (e.g. a multi-pane dialog with internal tabs) where you want fine control over focus restoration.

For these, the standard libraries (`focus-trap`, `react-aria`'s `useFocusManager`, `radix-ui`'s `FocusScope`) are the credible solutions. Hand-rolling a focus trap in 2026 is a yellow flag in code review.

**Keyboard interaction patterns for composite widgets.** The W3C ARIA Authoring Practices Guide (APG) is the contract. The key patterns and their canonical keyboard models:

- **Combobox 1.2** (the corrected version) — text input with a popup. Down arrow opens the popup, arrows navigate options, Enter selects, Escape closes, typing filters. `aria-activedescendant` is the typical focus-management pattern (DOM focus stays on the input).
- **Listbox** — Up/Down navigate, Home/End jump, typeahead by first letter, Enter or Space selects (single-select); Shift+Click and Ctrl+Click for multi-select with appropriate Shift+Arrow extensions.
- **Menu/Menubar** — Arrow navigation along the axis, perpendicular arrows open submenus, Escape closes, Tab leaves the menu entirely. Menubar is horizontal; menu is vertical.
- **Tablist** — Left/Right navigate tabs, Home/End jump, Enter/Space activate. Two activation modes: automatic (focus changes panel) and manual (focus moves but panel changes only on activation). APG documents both; the practice should pick one and stick with it per design language.
- **Tree** — Up/Down move through visible items, Right expands or moves into, Left collapses or moves out, Enter activates, typeahead.
- **Treegrid** — Tree + Grid, the most complex APG pattern. Rare in practice; if needed, use a battle-tested library implementation.
- **Grid** — Arrow navigation across cells; complex modes for selection and editing. Native `<table>` does not provide grid keyboard model — `role="grid"` is needed, plus the keyboard handlers.
- **Disclosure** — A button with `aria-expanded` controlling visibility of a region. Native `<details>`/`<summary>` is the simplest; falls down when the disclosure target needs to live outside the `<details>` element or be styled in ways `<summary>` resists.
- **Dialog** — Modal: `<dialog>` + `showModal()`. Non-modal: `<dialog>` + `show()` (rare). Keyboard model is automatic with `<dialog>`.
- **Tooltip** — Triggered by hover OR keyboard focus. Persistent on focus; dismissed by Escape, focus loss, or pointer leave. WCAG 1.4.13 Content on Hover or Focus governs the dismissibility, hoverability, and persistence rules.
- **Toolbar** — Like Menubar but for actions, not menus. Roving tabindex within the toolbar.

**Roving tabindex vs. `aria-activedescendant`.** Two different patterns for managing focus inside composite widgets:

- **Roving tabindex.** Exactly one descendant has `tabindex="0"`; all others have `tabindex="-1"`. As the user navigates, the system moves the `tabindex="0"` between descendants and calls `.focus()` on the new active one. DOM focus moves; `:focus` reflects the active descendant. Best for: tablists, menus, toolbars, trees. Engine support is uniform.
- **`aria-activedescendant`.** DOM focus stays on a container; `aria-activedescendant` points to the conceptually-focused descendant. The descendant does not receive `:focus`; the system must style it as if focused (typically `aria-activedescendant`-derived selector). Best for: combobox (input keeps DOM focus while user navigates options), single-text-input multi-completion patterns. Engine support is uniform but JAWS and NVDA differ in how aggressively they re-announce on `aria-activedescendant` changes.

The practical decision: roving tabindex is more robust because DOM focus actually moves; `aria-activedescendant` is necessary only when you cannot move DOM focus (text input must keep it). Default to roving tabindex; reach for `aria-activedescendant` when the pattern requires it.

**Skip links, landmarks, and the heading outline.**

- **Skip links** ("Skip to main content") — still relevant in 2026 because keyboard users still benefit from bypassing repeated navigation. The skip-link target should be a focusable region (typically `<main tabindex="-1" id="main">`) and the link should appear visually on focus (either always-visible or `:focus-visible` reveal). The practice should ship skip-links by default in any layout that ships the system's `<header>` and `<nav>` primitives.
- **Landmark regions** — `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<section aria-label="...">`. AT users navigate by landmark; the system should ensure every page rendered with system layout primitives produces a clean landmark outline.
- **Heading outline** — `<h1>` through `<h6>` should form a logical document outline. The HTML5 outline algorithm (which would have allowed implicit re-leveling per `<section>`) was never implemented by AT; treat each heading level as explicit. Component primitives must allow consumers to control heading level (a `Card` component with a title shouldn't hard-code `<h2>`; it should accept a `headingLevel` prop). This is one of the more-violated design-system contracts in shipping product code.

---

## 3. User preferences and the media-query surface

The web platform exposes user preferences via CSS media queries that the design system can respect at the foundation layer. The set as of mid-2026:

- **`prefers-reduced-motion`** (no-preference / reduce) — Baseline since 2020.
- **`prefers-color-scheme`** (light / dark / no-preference) — Baseline since 2020.
- **`prefers-contrast`** (more / less / custom / no-preference) — Baseline since 2024 (Chromium 96, Gecko 101, WebKit 14.1; the late Gecko number is when Firefox added the property to user-agent stylesheets).
- **`prefers-reduced-transparency`** — Baseline since 2024 (Chromium 118, Gecko 113, WebKit 17.4).
- **`prefers-reduced-data`** — Available in Chromium since 85 behind a flag; **not Baseline as of mid-2026**. Treat as forward-looking; do not architect on it as a load-bearing primitive.
- **`forced-colors`** (active / none) — Baseline since 2022 (Chromium 89, Gecko 89, WebKit 14.1). The fundamental Windows High Contrast Mode primitive, also fires on macOS Increase Contrast in some configurations.
- **`inverted-colors`** (inverted / none) — Available in WebKit (Safari 9.1+, primarily macOS); **not implemented in Chromium or Gecko as of mid-2026**. Verification: caniuse "inverted-colors". Treat as iOS/macOS-only signal; do not rely on it as the primary "user inverted" mechanism.

**`forced-colors` mode** is the most consequential of these for design-system architecture. When active (typically Windows High Contrast Mode but increasingly other contexts), the user agent overrides paint properties — backgrounds, borders, foreground colours, shadows, gradients, background images on certain elements — with a small palette of system-defined colours. The CSS `system-color()` keywords (`Canvas`, `CanvasText`, `LinkText`, `VisitedText`, `ButtonFace`, `ButtonText`, `Field`, `FieldText`, `Highlight`, `HighlightText`, `Mark`, `MarkText`, `GrayText`) reflect the user's chosen palette and survive forced-colors mode. What the system should encode:

- **Components that rely on background-image, gradients, box-shadow, or transparency for state expression must have a `@media (forced-colors: active)` override** that re-establishes state through `border`, `outline`, or `system-color()` values. Example: a selected list item indicated by a 4px left border and a tinted background — in forced-colors, the tinted background is stripped; the border survives, but only if it's solid. Verify the border appears.
- **Custom focus rings must use `system-color()` in forced-colors mode.** A branded focus ring (`outline: 2px solid var(--focus-ring);`) is stripped to the system's `Highlight` colour when forced-colors is active. The system should set `outline: 2px solid Highlight;` (using `Highlight` directly) inside the forced-colors block, or use `outline-color: currentColor` which the user agent computes against the forced palette.
- **Icons that paint via SVG fill should set `fill: currentColor`** so they inherit the forced foreground; icons that set explicit hex fills disappear in forced-colors.
- **Selected state in radio/checkbox** is automatically handled by the user agent for native `<input>`; for custom controls (the `Switch` primitive), forced-colors must be tested specifically.

The system should ship a single `forced-colors` audit pass per component and a Storybook addon mode that simulates `forced-colors: active` (Storybook Addons supports this since 2023; the practice should adopt it as a default for any system component).

**The reduce-motion contract** — what the system encodes once vs. what each component decides locally, derived from 18-motion-foundations and applied to web specifically:

- **System layer (foundation tokens):** All animation-duration tokens have a `prefers-reduced-motion: reduce` variant that resolves to either `0ms` (for purely decorative motion that has no informational role) or a much-shortened duration (~50–80ms, for motion that indicates causality between an action and a result — preserving the *change* signal without the *animation* of it). The 18-motion-foundations *informational vs. vestibular refinement* split applies directly: vestibular triggers (parallax, autoplay video with translation, large rotations) → 0ms in reduce; informational signals (focus rings appearing, error shake, expansion of an accordion) → shortened duration.
- **Component layer.** Each component opts into the reduce-motion contract by referencing the duration token, not by writing a media query. The system should fail PR review on any component-level `@media (prefers-reduced-motion)` block — that's a sign the component is making a reduce-motion decision the foundation layer should make.
- **The `@media (prefers-reduced-motion: no-preference)` wrapper pattern.** Wrap animation declarations in `@media (prefers-reduced-motion: no-preference) { ... }` so reduced-motion gets `none` by default, animation by opt-in. This pattern is more robust than overriding inside a `reduce` block because it works correctly when the user toggles preferences mid-session.
- **`scroll-behavior: smooth`** is *not* automatically reduced. Programmatic smooth scrolling needs explicit gating — `scrollIntoView({ behavior: 'smooth' })` in JS should check `matchMedia('(prefers-reduced-motion: reduce)').matches` and use `instant` if so.
- **View Transitions** (the API behind same-document and cross-document view transitions in Chromium 111+ / WebKit 17.4+) honours `prefers-reduced-motion: reduce` via a built-in `::view-transition` mechanism, but only if the system's transition CSS doesn't override the default. The 19-motion-implementation-web file flags this gotcha; the implementation rule is: if the system writes any `::view-transition-old`/`::view-transition-new` animation, it must wrap the animation declaration in `@media (prefers-reduced-motion: no-preference)`.

**`prefers-contrast: more`** indicates the user wants increased contrast (typically WCAG AAA levels). The system can respond with:

- A high-contrast theme that uses `prefers-contrast: more` as the resolution mode. This is heavier-weight than relying on the user agent — and worth doing for systems shipping to public-sector / EAA-required customers.
- Component-level overrides that thicken borders, increase outline weights, raise text contrast on neutrals.
- The default response: do nothing different and rely on shipping AA compliance everywhere by default. Acceptable for AA-conformance use cases; insufficient when the procurement spec calls out enhanced contrast or AAA.

The relationship to **forced-colors:** `prefers-contrast: more` is the user's request for *more* contrast within the system's chosen palette; `forced-colors: active` is the platform overriding the palette entirely. They're orthogonal — a user may set both, neither, or one. The CSS treatments are different; both must be tested.

**System-level color inversion and dark mode interplay.**

- **`prefers-color-scheme: dark`** is the user's preferred theme; the system honours it via the dark-mode tokens and `color-scheme` CSS property.
- **Smart Invert (iOS/macOS)** inverts the page paint regardless of `prefers-color-scheme`. Adding `@media (inverted-colors: inverted) { /* re-invert images */ }` is the WebKit-specific opt-out. Wrap brand images and photography in re-inversion treatment; Smart Invert is meant for text-heavy reading and assumes images shouldn't invert.
- **Windows / Chromium "Dark theme" force** — Chromium can force-dark unstyled pages. A site with `color-scheme: light dark` and proper dark-mode tokens opts out (the user agent sees the site is dark-aware). Without `color-scheme`, force-dark heuristics will invert the site, often badly. Always set `color-scheme` at the document root: `:root { color-scheme: light dark; }`.

---

## 4. Composite widget patterns and the ARIA Authoring Practices contract

The system's component decisions for composite widgets fall into three tiers:

**Tier 1 — Wrap a native control, don't replace it.** `Button`, `TextField`, `Checkbox`, `Radio`, `Select` (single-select with simple options), `Textarea`, `Slider` (range input), `ProgressBar` (`<progress>`), `Disclosure` (`<details>`/`<summary>`), `Dialog` (`<dialog>`). Native controls' accessibility is generally complete, AT-tested across engines, keyboard-correct by default, forced-colors-aware out of the box. The system's job is theming and integration with the broader component vocabulary, not replacing native semantics.

**Tier 2 — Compose ARIA on a custom widget where native loses.** `Combobox` (text input with rich popup; native `<select>` does not support the popup model), `Multi-select`, `Tabs` (no native), `Menu` and `Menubar` (no native), `Tree`, `Tooltip` (`<details>` doesn't fit the model), `Tag`/`Chip` (custom interactive). For these, follow APG keyboard models exactly — they are derived from extensive AT testing.

**Tier 3 — Highly bespoke, build with extreme care.** `Treegrid`, `Grid` (with editing modes), `Spreadsheet`-like tables, custom rich-text editors. These are where most a11y bugs live. The practice's recommendation: don't build these in-house unless the brand requires it; reach for a battle-tested library (TanStack Table, Slate, Lexical, etc.) with documented accessibility support.

**Per-pattern coverage with the keyboard model.** Each pattern below assumes Tier 2 — building it on top of ARIA. Native-element patterns (Tier 1) are not detailed.

- **Combobox 1.2** — `<input role="combobox" aria-controls="popup-id" aria-expanded="false" aria-autocomplete="list">` with a popup `<ul role="listbox" id="popup-id">` of `<li role="option">`. Keyboard: Down arrow opens (or moves into popup), Up/Down navigate options, Enter selects (and closes), Escape closes (with optional value reset), typing filters. `aria-activedescendant` points to the focused option; DOM focus stays on the input.
- **Listbox** — `<ul role="listbox" tabindex="0">` with `<li role="option" aria-selected="true|false">`. Single-select: roving tabindex or `aria-activedescendant` works; the practice should pick one. Multi-select: `aria-multiselectable="true"`; Shift+Click and Shift+Arrow extend selection; Ctrl+Click toggles individual selection.
- **Menu/Menubar** — `role="menubar"` and `role="menu"`, `role="menuitem"`. Submenu opens via Enter, Right Arrow, or Down Arrow; closes via Escape, Left Arrow, or focus loss. Disabled menu items still receive focus (for discoverability) but ignore activation. The Material Design menu pattern is not WAI-conformant; verify against APG, not against any specific framework's interpretation.
- **Tablist** — `role="tablist"` containing `role="tab"` (with `aria-controls`, `aria-selected`); panels are `role="tabpanel"` (with `aria-labelledby` to the corresponding tab). Roving tabindex within the tablist. Activation modes: automatic (focus-then-activate) or manual (focus, Enter/Space activate). Both are APG-conformant; the practice should pick one and document it. Automatic is more discoverable; manual is preferred when each panel has expensive content (so users can survey tabs without triggering loads).
- **Tree** — `role="tree"` containing `role="treeitem"` with `aria-expanded` (for parent items), `aria-selected` (where selection is meaningful), `aria-level`, `aria-posinset`, `aria-setsize`. Keyboard: Up/Down through visible items, Right expands collapsed (or moves into expanded), Left collapses or moves to parent, typeahead by first letter. The relationship to `<details>`/`<summary>` is contextual — a tree of disclosure widgets isn't quite the same UI; use `role="tree"` for navigation/data, `<details>` for content disclosure.
- **Treegrid** — combine tree (rows) with grid (cells). Up/Down move rows, Left/Right move cells within a row, Right at last cell moves to next row and expands, Left at first cell collapses. The most complex pattern; AT support varies; always prefer a simpler model if possible.
- **Grid** — `role="grid"`, `role="row"`, `role="gridcell"` (or `role="columnheader"` / `role="rowheader"`). Keyboard: Arrow keys navigate cells, Home/End jump to row start/end, Ctrl+Home jumps to first cell, Page Up/Down scroll a screen. Two interaction modes: navigation (focus a cell) and edit (focus inside a cell's input). The system should handle both.
- **Disclosure** — Either `<details>`/`<summary>` (preferred when the disclosure target lives inside the `<details>`) or `<button aria-expanded="false" aria-controls="region-id">` paired with `<div id="region-id">` (when the target lives elsewhere or needs more styling control than `<summary>` allows).
- **Dialog** — `<dialog>` + `showModal()` for modal; `<dialog>` + `show()` for non-modal (rare). Manual implementation only when targeting browsers without `<dialog>` support, which in 2026 is essentially no one.
- **Tooltip** — `role="tooltip"` on the popup, paired with `aria-describedby` from the trigger. Trigger by hover OR focus, dismiss by Escape, hover-out, blur. The tooltip must remain visible while hovered (so users can read it without it dismissing). WCAG 1.4.13 governs.
- **Toolbar** — `role="toolbar"` containing buttons (or composite controls). Roving tabindex; arrow keys navigate within the toolbar.

**Where APG guidance disagrees with current AT behaviour.** APG is a gold-standard for the keyboard model, but it's prescriptive in places where AT implementations diverge. Known issues as of mid-2026:

- **Combobox autocomplete patterns.** APG documents three combobox patterns (no autocomplete, list autocomplete, list-with-inline-autocomplete). The "list autocomplete" pattern's expected behaviour for what AT announces when filtering changes the option list has historically diverged across NVDA and JAWS. As of NVDA 2026.1 and JAWS 2026, behaviour is closer to convergence but the inline-autocomplete pattern remains unreliable across screen readers.
- **`aria-owns` for cross-tree relationships.** APG describes patterns that use `aria-owns` to logically own descendants from elsewhere in the DOM. As noted in §1, WebKit support has been historically incomplete. Design components to avoid `aria-owns` where possible.
- **JAWS table reading mode.** JAWS in default settings reads tables in "table mode" (cell-by-cell with row/column header context). For `role="grid"` tables, JAWS treats them as forms-mode grids, which means navigation keys are intercepted by JAWS unless the user enters "forms mode" (PC Cursor). The system can't fix this; designers should know that JAWS users may experience grid widgets differently than NVDA/VoiceOver users.
- **VoiceOver and `aria-current="page"`** announces "current page" only on links in some configurations; on buttons or list items, it's silent. This is a long-standing iOS VoiceOver quirk. Workaround: use `aria-current="page"` AND include "current" in the accessible name when the visual treatment is inert (e.g. "Home, current page").

**The library landscape and where the system should depend.**

- **react-aria** (Adobe / React Spectrum) — the most credible cross-engine, cross-AT-tested library for React 2026. Hooks for nearly every APG pattern, with extensive cross-AT testing. Component-by-component use; or its sibling **react-stately** for state machines plus react-aria for behaviour. A design system that builds on react-aria + custom rendering is the highest-quality DS-level a11y baseline available without writing AT testing in-house.
- **Radix Primitives** — unstyled React primitives with strong APG conformance. Lighter than react-aria; opinionated structure (compound components). Good choice when the system's a11y bar is "match APG and verify against axe + manual" rather than "exhaustive AT regression testing".
- **Headless UI** (Tailwind) — solid for the components it covers; coverage is narrower than Radix or react-aria. Good for systems built on top of Tailwind that don't need exotic patterns.
- **Reach UI** — historically credible; the project has been effectively dormant since 2023. Not recommended for new systems.
- **Ark UI** — newer, framework-agnostic (Solid/Vue/React via wrappers), based on Zag.js state machines. Promising; less mature AT validation than react-aria. Reasonable when the system needs cross-framework reach.
- **Web Awesome / Shoelace** — web-component-based design system with credible a11y coverage. Choose when the system itself ships as web components (avoiding framework lock-in).

**The practical recommendation:** for a React-first system, build composite widgets on react-aria or Radix; for a multi-framework system, evaluate Ark UI or Web Awesome; for a web-component system, ship on top of Lit + Web Awesome's primitives or write your own with rigorous AT testing. Building APG patterns from scratch in 2026 is a yellow flag — the libraries are good enough that the engineering hours are better spent on the system's distinctive surface, not re-implementing the combobox.

---

## 5. Live regions, announcements, and dynamic content

Live regions are how the system communicates dynamic content changes to AT without moving focus. The primitives:

- **`aria-live="polite"`** — announce on the next pause in user activity. Most uses.
- **`aria-live="assertive"`** — announce immediately, interrupting current speech. For urgent errors only.
- **`aria-live="off"`** — explicit off (rarely needed; the default).
- **`aria-atomic="true"`** — when the live region updates, announce the entire region's content; otherwise (the default), announce only the changed nodes.
- **`aria-relevant="additions text removals all"`** — which DOM mutations trigger announcement; default is `additions text` (additions and text changes). Removals are not announced by default.
- **`role="status"`** — equivalent to `aria-live="polite"` + `aria-atomic="true"`. Best for status messages.
- **`role="alert"`** — equivalent to `aria-live="assertive"` + `aria-atomic="true"`. Best for errors.
- **`role="log"`** — for chronological logs (chat messages, console output). `aria-live="polite"` semantics with chronological-order interpretation.
- **`role="timer"`** and **`role="marquee"`** — rarely used; avoid.

**Engine and AT behaviour:**

- **All four engines** correctly fire AT events when live region content changes.
- **NVDA** announces polite live regions by default; assertive with priority over reading flow.
- **JAWS** does the same, with one quirk: JAWS sometimes announces only the changed nodes even when `aria-atomic="true"` is set. NVDA respects atomic; JAWS partially. Test both.
- **VoiceOver (macOS)** announces polite live regions reliably; assertive interruptions are sometimes timed differently than NVDA.
- **VoiceOver (iOS)** has historically been the weakest with live regions; iOS 17+ improved significantly. Status messages now reliably announce; complex live regions with `aria-atomic` and multiple children remain less predictable.
- **TalkBack on Chromium-Android** — polite and assertive both work; behaviour is closer to TalkBack on native Android (live regions on Compose) than to desktop AT.

**The "live region must exist before the change" rule.** AT computes live region semantics at the time of mutation, not at the time of the live region's creation. A component that injects a `<div role="status">Saved</div>` into the DOM at the moment the save completes is **not announced** by most AT — the live region didn't exist before its content changed; AT sees a new node, not a content change. The pattern that works: render the live region container empty at component mount; insert/update text content when the event fires. The `<Toaster>` component pattern (a single mounted live region that gets text injected on each toast event) is the canonical implementation.

The system should ship:

- **A single `<LiveRegion>` primitive** that the application mounts at the page root. Toast/snackbar/announcement components do not each have their own live region; they all push text into the shared one.
- **A `useAnnouncement()` hook** (or framework equivalent) that pushes a string to the live region with controlled timing (debounce, queue, replace).
- **Per-form `<FormErrorSummary>`** as a polite live region that updates when validation errors change.

**Toast / snackbar / inline-error / form-level-error patterns.** Mapping to live region roles:

- **Toast/snackbar (success)** — `role="status"` (polite). The user shouldn't be interrupted to hear "Saved".
- **Toast/snackbar (error)** — `role="alert"` (assertive). The user should know immediately.
- **Inline field error** — not a live region directly. Use `aria-describedby` to associate the error message with the field; the error announces when the field receives focus. For errors that appear without focus (e.g. async validation), additionally update a polite form-level live region.
- **Form-level error summary** — `role="alert"` if the summary appears on submit (urgent context); `role="status"` if it updates as the user types. Both APG-acceptable; pick the one that matches the form's UX.

**The status-message problem (WCAG 2.2 SC 4.1.3).** SC 4.1.3 requires that status messages can be programmatically determined through role or properties such that they can be presented to the user by AT without receiving focus. This is exactly what live regions solve. The verification problem: automation can verify the live region exists, has the correct role, has reasonable content. Automation **cannot verify that the message was announced** — that depends on AT timing, queue state, and user-agent settings. The audit evidence for SC 4.1.3 must include manual AT testing. (This is a recurring pattern — see §8.)

**Initial-load announcements.** The page's `<title>` is announced on load by all AT. Beyond that, an initial-load "Loaded" announcement is only useful when the content meaningfully differs from the title or when the user might have been waiting. The system should not ship an automatic "Page loaded" announcement; doing so produces noise.

**Single-page application route changes.** When the URL changes via History API and the page content changes without a full reload, AT does not automatically announce. The canonical fix:

1. Update `document.title` to the new page title.
2. Move focus to a known landmark (typically `<main>` or the page's `<h1>`). The focus move triggers AT to read the new content.
3. Optionally, push a polite announcement to the live region ("Navigated to Settings").

Most React/Vue/Svelte routers do not do this by default; the system should provide a `<RouteAnnouncer>` component that the application opts into. react-router and Next.js each have community patterns; the system can wrap whichever the consumer uses.

---

## 6. Forms, errors, and the input contract

Native form elements remain best-in-class for accessibility on the web. The system's job is to compose, theme, and integrate — not replace.

**Native primitives.**

- **`<form>`** with proper `<label>` associations is the most accessible foundation. `<label for="x">Name</label> <input id="x">` or `<label>Name <input></label>` (implicit). The system's `Field` primitive must produce one of these patterns; a `<label>` not associated with an input is a system-level a11y bug.
- **`<input>` types** — `email`, `tel`, `url`, `number`, `date`, `color`, `search`, `password`, etc. Each provides better mobile keyboards, better autocomplete, and (for some) better validation. The system should expose typed inputs as primitives, not generic text inputs with type props the consumer must know to set.
- **`<select>`** with `<option>` is fully accessible. With `<optgroup>` for grouping. The system should not replace `<select>` with a custom combobox unless the design genuinely requires search/filter/multi-select that `<select multiple>` doesn't deliver.
- **`<textarea>`** for multi-line text. `<input type="text">` is single-line by definition.
- **`<fieldset>`/`<legend>`** for grouped inputs (radio groups, related checkboxes). The system's `RadioGroup` primitive should render `<fieldset>` with the group label as `<legend>`. Skipping `<fieldset>` for visual reasons is a frequent system-level violation; the rendered HTML should always have it, even if the visual styling hides it.

**Constraint validation API and the user-invalid pseudo-class.**

- **HTML validation attributes** — `required`, `minlength`, `maxlength`, `pattern`, `min`, `max`, `step`. The user agent enforces them; failure shows a native error tooltip on submit. The system can leverage these for client-side validation without writing JS.
- **`:user-invalid`** — applies after the user has interacted with the field (changed it, blurred it). Baseline since 2024 (Chromium 119, Gecko 88, WebKit 16.5). This is the modern primitive for "invalid AND user-engaged" — replacing the `:invalid` pseudo-class, which fires immediately on render even before the user has typed (producing red borders on every required field on form mount).
- **`:user-valid`** — corresponding pseudo for validated-and-user-engaged. Baseline since 2024.
- **`invalid` event** — fires when constraint validation fails on submit. The system can use this to reposition focus to the first invalid field, update an error summary, etc.

The recommended system-level pattern: use `:user-invalid` for the "show error styling" rule, use the `invalid` event for the "focus management on submit" behaviour, use a polite live region for the form error summary.

**`aria-describedby` for help and error text.**

- **Help text** — `<input aria-describedby="help-id"> <span id="help-id">Format: 3 letters</span>`. AT announces the help text when the field is focused.
- **Error text** — `<input aria-describedby="error-id" aria-invalid="true"> <span id="error-id">Email is required</span>`. The relationship between `aria-invalid` and `:user-invalid` is: `:user-invalid` is the visual rule; `aria-invalid` is the AT rule. The system should set `aria-invalid` based on the same condition as `:user-invalid` — only after the user has engaged with the field.
- **Both help and error** — when a field has both, comma-separate the IDs: `aria-describedby="help-id error-id"`. AT will announce both; the order is the source order in the IDREF list.
- **`aria-errormessage`** — points specifically at an error message, with the implicit semantic that the message is about the error (vs. `aria-describedby` which is generic description). Cross-engine support has historically been weaker than `aria-describedby`; as of mid-2026, Chromium and Gecko handle it reliably; WebKit has improved in Safari 17. For maximum AT support, use `aria-describedby` for everything; `aria-errormessage` is cleaner semantically but less reliable.

**Required-field indication.** Multiple acceptable patterns; pick one and document it.

- **Asterisk + legend** — every required field has a `*` in the visible label; the form has a legend "* indicates required field". Add `aria-required="true"` to the input. Most accessible across configurations.
- **Optional indication** — required is the default; optional fields are marked "(optional)". Avoids visual asterisk noise. Less common but well-tolerated by AT.
- **Required attribute alone** — `<input required>` and the user agent's native error on submit. Acceptable for short forms; insufficient for long forms where the user wants to know required-ness in advance.

The system should pick one and ship it as the `Field` primitive's default; allow override.

**Error-summary patterns.** For forms with multiple fields, an error summary at the top of the form (after submit) is the GOV.UK pattern, widely adopted in compliance contexts. The summary is a polite live region (`role="alert"` if it appears on submit, `role="status"` if it updates as the user types) listing each error with a link to the corresponding field. Activating a link moves focus to the field and (typically) announces the field's `aria-describedby` content.

**Specialised inputs and where native is enough.**

- **Date pickers.** `<input type="date">` is now strong enough for most cases. Native UI varies per browser/OS; that's a feature, not a bug — it matches the user's platform conventions. Custom date pickers should be reserved for cases where the visual design genuinely requires it (e.g. an inline calendar instead of a modal); even then, the underlying `<input type="date">` should be the source of truth, and the visual UI should be a styling layer.
- **Combobox.** Native `<select>` doesn't support search; custom comboboxes (§4 Tier 2) fill this gap.
- **File upload.** Native `<input type="file">` is fully accessible. Drag-and-drop overlays are an enhancement; the underlying `<input>` must remain for keyboard and AT users. The pattern that works: `<label>` wraps both the visual drop zone and the file input; clicking either triggers the file picker; drag-and-drop is the same upload via JS. The label's accessible name is what AT announces.
- **Drag-and-drop file input** — for dragging files into the form. Always pair with the native `<input type="file">` keyboard and pointer fallback.

**Auto-fill and autocomplete attributes.** WCAG 1.3.5 (Identify Input Purpose) requires that input purposes (name, email, address, payment) be programmatically identifiable. The `autocomplete` attribute is the mechanism. Values like `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `cc-number`, `postal-code` are recognised by browsers (for autofill) and by some AT (for purpose identification). The system's `Field` primitive should accept an `autocomplete` value and pass it through; the system should document the `autocomplete` values relevant to common form patterns.

---

## 7. Color, contrast, and the visual layer

WCAG 2.x contrast (the lightness-based formula derived from the 1996 W3C draft) remains the contract for AA and AAA conformance in 2026. APCA (Advanced Perceptual Contrast Algorithm) was a candidate replacement in WCAG 3 drafts for several years; as of mid-2026, **WCAG 3 remains a working draft, and APCA has not become the conformance standard.** The practical implications:

- **The contrast contract is still WCAG 2.2.** Auditors verify against it; procurement specs reference it; ACR/VPAT documents use it.
- **APCA is informational, not normative.** Some teams have adopted APCA-aware tooling (e.g. inverse-luminance-aware contrast checks) for design decisions. This is reasonable for design-time tooling; it does not replace WCAG 2.x for conformance.
- **The practice's recommendation:** use WCAG 2.2 contrast for all conformance and procurement; use APCA-aware tooling internally for design decisions where WCAG 2.x's known weaknesses (e.g. blue-on-black mis-rating) cause poor design outcomes; never claim APCA conformance to clients.

**Pair tokens on the web specifically.** From 14-accessibility, the pair-token model says contrast is a property of *foreground × background pairs*, not individual tokens. On the web, the implementation is:

- **Foreground tokens** declare their intended background. `text-on-surface-primary`, `text-on-surface-elevated`, `text-on-brand-primary`. Each token has a description (`$description` per DTCG) noting the assumed background and the contrast ratio.
- **The system enforces contrast at build time** via DTCG validation: pair tokens that would produce sub-AA contrast fail the build. (See 22-token-architecture-extensions for the DTCG validation pattern; 24-tokens-at-scale for the multi-brand version.)
- **Developers consume pair tokens.** A `Button` component uses `text-on-brand-primary` for its label, not `text-primary`. This makes the foreground/background relationship explicit at the consumption site.
- **Themes and densities multiply pairs.** Light × dark × high-contrast × density = N foreground tokens per logical text role. The validation matrix is correspondingly large; CI must run all combinations.

**Contrast for non-text content (UI components, graphical objects) — SC 1.4.11.** Borders, focus rings, icons, controls' visual boundaries must meet 3:1 against adjacent colours. Common system-level violations:

- **Buttons with no border, only fill colour against background.** A blue button on a white background passes 3:1 only if the blue is dark enough. A pale-blue button often fails.
- **Form-field borders** — a 1px gray border against a white background frequently fails 3:1. The system should ship form fields with a contrast-aware border colour.
- **Disabled state** — disabled inputs/buttons are exempted from contrast requirements per WCAG 2.2 SC 1.4.3 (text contrast) and 1.4.11. The system can use lower-contrast disabled states.
- **Decorative content** — pure decoration (illustrations without informational role) is exempted. The system must distinguish decorative from informational icons; decorative gets `aria-hidden="true"`, informational doesn't and must meet 3:1.

**Focus-indicator contrast (SC 2.4.13 in WCAG 2.2 AA).** Focus indicators must be at least 2 CSS pixels thick along the longest side of the element, and must have at least 3:1 contrast against the unfocused state. The contrast check is *between focused and unfocused states*, not just between the indicator and the background. This catches the common pattern of "a 1px outline that's only slightly different from the unfocused border" — which is widespread in legacy systems. The new ring tokens (24-tokens-at-scale's "focus-ring" pair) should be designed to meet 2.4.13 specifically.

**Branded focus rings.** The tension: the brand wants a brand-coloured focus ring (continuity with brand identity). The standard wants a 2px, 3:1-contrast ring. The reconciliation:

- The branded ring is the primary visual; the system tokenises it as `focus-ring-brand`.
- Forced-colors mode strips it; the system falls back to `Highlight` (system-coloured ring).
- High-contrast theme (under `prefers-contrast: more`) thickens the ring or switches it to a system-aware token.
- For mid-contrast brand colours (e.g. a brand-blue against light backgrounds), the system may shadow the ring with a darker outer ring to ensure 3:1 against any adjacent surface.

The audit pattern: capture a screenshot of every interactive primitive in focus and run automated 2.4.13 verification (DevTools or axe-core support).

**Color is not the sole carrier of meaning — SC 1.4.1.** Status colours must be paired with text labels or icons. The system should encode this as:

- **Status pills/badges** include both a colour and an icon by default; the icon cannot be omitted by composition rules.
- **Form errors** show a coloured border AND an error icon AND text — not just colour.
- **Charts** include patterns or shapes alongside colour — though chart components are a known practice gap (see §5.2 of 09-gaps).

The annotation contract should include a "colour-meaning" field per component state where colour carries meaning; if the field is non-empty, the engineer must verify a non-colour indicator is present.

---

## 8. Testing, tooling, and conformance evidence

**Static analysis (build-time).**

- **`eslint-plugin-jsx-a11y`** — React/JSX-aware lint. Catches missing alt attributes, missing form labels, click handlers without keyboard handlers, ARIA-attribute typos, `aria-hidden` on focusable elements. The system should ship a recommended ESLint config that includes this plugin.
- **axe-core lint** — schema-level checks integrated into IDEs and CI. Lighter coverage than runtime axe-core but catches the same surface that lint can analyse statically.
- **HTML validation** in CI (W3C validator or `html-validate`) — catches malformed structure that breaks AT.
- **Storybook a11y addon** — runs axe-core on every story, surfaces violations in the Storybook UI. The system should ship every component as a Storybook story with the addon enabled; failing the addon should fail PR CI.
- **CSS lint** — for forced-colors checks (e.g. detect `outline: none` without a paired `:focus-visible` outline replacement) and contrast checks (e.g. linters that flag color tokens with sub-AA pair contrast — though this is more reliably done at the token validation layer per 22).

**Runtime/automation.**

- **`axe-core`** — the de-facto runtime accessibility engine. As of axe-core 4.10.x, the published catch rate is **roughly 25–40% of WCAG issues automatically detectable**, depending on what you count and how. The 30%-ish figure widely cited derives from Deque's own published research; verify against axe-core's current documentation. This number is widely under-stated in the field as the basis for "we've automated accessibility" — it has not. Automation catches a meaningful but not majority slice of issues.
- **Playwright + axe** (via `@axe-core/playwright`) — runs axe on rendered pages in CI. The system should ship a baseline Playwright a11y suite as a default deliverable.
- **Cypress + axe** (`cypress-axe`) — equivalent for Cypress users.
- **Pa11y** (legacy but still maintained) — CLI-driven, useful for static-site monitoring.
- **Storybook a11y addon** — already mentioned; the per-component runtime layer.
- **Component-level a11y tests** — each component has a test that renders the component, runs axe, asserts no violations. The system should ship this as a test pattern, with helpers that handle common configurations (theming, RTL, forced-colors simulation).

**Browser DevTools.**

- **Chromium DevTools** — full accessibility tree, computed-role panel, ARIA validity warnings, `prefers-color-scheme` and `forced-colors` simulators, focus order overlay (since Chrome 110, Feb 2023). The most-complete a11y DevTools surface as of 2026.
- **Firefox DevTools** — accessibility inspector with tab order, role/name/state per node, contrast checking. Strong integration with NVDA testing workflows.
- **WebKit Safari Web Inspector** — Audit tab includes accessibility checks; less comprehensive than Chromium but catches the major issues. The accessibility node inspector mirrors macOS Accessibility Inspector for native apps.

**Manual testing — the AT × engine matrix.**

The four-engine, four-AT matrix:

| AT | Primary engine | Notes |
|---|---|---|
| **NVDA** | Gecko (Firefox) is canonical; Chromium widely used | Free, open-source, the dominant developer-test AT for Windows |
| **JAWS** | Chromium (Edge or Chrome) is most common in enterprise; Firefox supported | Commercial; the dominant procurement-grade AT |
| **VoiceOver (macOS)** | WebKit (Safari) primarily | Built-in; a different keyboard model than NVDA/JAWS (Control+Option) |
| **VoiceOver (iOS)** | WebKit (Safari) only on iOS | Mobile-only; gesture-based |
| **TalkBack** | Chromium (Chrome on Android) | Android equivalent of VoiceOver |
| **Narrator** | Chromium (Edge) | Built into Windows; secondary to NVDA/JAWS in test priority |

The practice's minimum manual-test matrix for a system component:

- **NVDA + Chrome** (Windows) — covers Chromium + a screen reader.
- **JAWS + Chrome** (Windows) — covers procurement-grade AT.
- **VoiceOver + Safari** (macOS) — covers WebKit.
- **VoiceOver + Safari** (iOS) — covers mobile WebKit.
- **TalkBack + Chrome** (Android) — covers mobile Chromium.

This is five test configurations per component per significant change. For a 60-component system, this is unsustainable unless automated regression covers the bulk and manual testing covers a sampled subset per release. The pragmatic pattern: automated coverage (axe + Playwright + Storybook) for every PR; manual matrix for every minor version (every 2–4 weeks of system evolution); full audit for every major version.

**ACR/VPAT evidence.** The Voluntary Product Accessibility Template (now ACR — Accessibility Conformance Report — under Section 508 Rev) requires per-criterion evidence. What automation produces:

- **Yes**: structural conformance (every interactive element has a name, every image has alt, every form field has a label), automated contrast measurements, lint and axe-core reports, Storybook addon results, CI pipeline logs.
- **No**: experiential evidence (traversal makes sense, live regions announce in time, error messages are helpful, focus management on dialog dismiss is correct, AT-specific behaviour like JAWS's table mode). For these, manual AT walkthroughs with video capture and tester sign-off are the only credible evidence.

The system's ACR/VPAT contribution: every component ships with its test suite and a "conformance dossier" (a Storybook page or markdown file) that lists per-criterion automated and manual evidence references. The consuming product's ACR aggregates per-component dossiers with application-level dossiers for the integration.

**Continuous monitoring.** Production a11y dashboards exist as a procurement-grade requirement for enterprise customers. Tools:

- **Siteimprove**, **Level Access** (formerly eSSENTIAL Accessibility), **Deque axe Monitor** — commercial dashboards crawling production sites and reporting issues over time.
- **Real-user a11y telemetry** — newer pattern; instrumenting the design-system components to report (anonymously) when AT events fire, what user preferences are detected, etc. This is forward-looking; treat as Phase-2 for systems with the maturity for it.
- **Synthetic monitoring with accessibility checks** — Playwright-based scheduled runs against production. Cheaper and more controlled than real-user monitoring; not as data-rich.

The practice's recommendation: the system's first investment in monitoring is CI (every PR) + per-release auditing (manual matrix); production monitoring is appropriate when the consuming product is at scale and the procurement spec demands it.

---

## 9. The Figma annotation contract for web

The web extension of 17-accessibility-annotation-contract. The mobile contract's eight concerns (accessible name, role, state, traversal, dynamic-type/scaling, behaviour under inversion / forced colors, gesture alternative, live-region intent) all carry over; web adds platform-specific extensions and modifies several.

**For every interactive element, annotate:**

- **Accessible name.** Same field as mobile. On web specifically:
  - If the visible text is the name, mark "name = visible text" — Compose-equivalent: web `<button>` handles this; the system primitive emits the right HTML.
  - If the visible text differs, declare the explicit string (becomes `aria-label` or `aria-labelledby` at engineering time).
  - If the name is composed dynamically, declare the template with parameter slots ("Unread, {N} messages").
  - **Web-specific:** declare which mechanism — `aria-label` (string), `aria-labelledby` (DOM ID reference), or visible text content. The default should be visible text; `aria-label` is for icon-only or when visible text is wrong; `aria-labelledby` is for cases requiring a separately rendered label string. Engineers should not pick this; the contract should.

- **Role.** Same as mobile but with different vocabulary. For web, declare:
  - The HTML element to render (`<button>`, `<a href>`, `<input type="text">`, etc.) where the system has a defaulted choice.
  - An ARIA role override only if the HTML element doesn't carry the right semantics (rare in well-designed systems).
  - For Tier 2 composite widgets (§4), the APG pattern name (Combobox 1.2, Listbox, Tablist, etc.) — engineering implements per APG.

- **State.** Same as mobile. Web-specific binding:
  - Native primitives: declare which `<input>` attribute carries the state (`checked`, `disabled`, `readonly`, `required`).
  - ARIA primitives: declare `aria-pressed`, `aria-selected`, `aria-expanded`, `aria-checked` (for tri-state), `aria-current` per APG.
  - State transitions visible: declare whether the state change should announce via live region, focus move, or `aria-describedby` update.

- **Traversal order.** Same as mobile but use **DOM source order** as the canonical mechanism. CSS reorder (flex/grid `order`, `flex-direction: row-reverse`) does not affect tab order or AT order — annotations should not declare visual reorder as a substitute for source-order placement. When source order must differ from visual order (rare; e.g. visually-RTL with logical order), declare it explicitly.

- **Keyboard interaction per APG pattern.** For Tier 2 composites: declare the APG pattern. The keyboard model is implied (Combobox 1.2 → defined keyboard contract). For Tier 3 bespoke: the annotation must spell out keys. For Tier 1 native: no annotation needed beyond standard expectations (Tab in/out, Enter/Space activation).

- **Landmark and heading structure.** New for web (mobile doesn't have landmarks per se):
  - Declare the landmark role if the component is a landmark (`<nav>`, `<header>`, `<main>`, `<aside>`, `<footer>`, `<section aria-label>`).
  - Declare the heading level for any heading-bearing component. The component must accept a `headingLevel` prop; the consumer picks; the design declares the *default* level for the typical use context.

- **`forced-colors` behaviour.** New for web. Per element:
  - **Survives unchanged** — the design works as-is in forced-colors. Default for native HTML elements.
  - **Has a forced-colors variant** — the design has a specific forced-colors override (border in place of fill, system colour in place of brand). The annotation declares what changes.
  - **Custom paint stripped** — annotation that the component depends on background-image, gradient, box-shadow, or transparency, and has a forced-colors fallback that re-establishes meaning via border, outline, or `system-color()`.

- **`prefers-reduced-motion` treatment.** Per animation:
  - **Decorative motion** → set to `none` in `reduce`.
  - **Informational motion** → shortened duration (~50–80ms).
  - **Vestibular trigger** (parallax, large rotation, autoplay video translation) → set to `none` in `reduce`.

- **`prefers-color-scheme` and theme variants.** Light, dark, and high-contrast (where the system ships one) versions of every component state. Where the visual treatment differs significantly, annotation declares the differences.

- **`inert` regions.** For modal patterns — declare what becomes inert when the modal is open. With `<dialog showModal>`, the answer is "the rest of the page"; with custom popovers or layered surfaces, the answer requires explicit declaration. (e.g. "When the side panel opens, the main content is `inert`; the page header stays interactive.")

- **Focus-return target after dismiss.** For dialogs, popovers, anything that transiently interrupts the page: declare what receives focus when dismissed. Default is "the trigger that opened it"; some patterns require different (e.g. a delete confirmation, on success, returns focus to the next item in the list, not the deleted one).

- **`aria-controls`/`aria-owns`/`aria-describedby` relationships.** New for web. For components where ARIA relationships are part of the contract:
  - `aria-controls` — declare the relationship between trigger and controlled region.
  - `aria-describedby` — declare what message provides the description (help, error, hint).
  - **Avoid `aria-owns`** — if the component design requires reordering across the DOM, redesign to avoid it (§1).

- **Gesture alternative.** Same as mobile. Web adds:
  - **Click vs. drag-and-drop.** Drag-and-drop must be operable via single-pointer click or button alternative.
  - **Swipe gestures on touch.** Web equivalent is `pointerdown`/`pointermove`/`pointerup`; alternatives via button or context menu.

- **Live-region intent.** Same as mobile. Web binding:
  - **Polite** → `role="status"` or `aria-live="polite"`.
  - **Assertive** → `role="alert"` or `aria-live="assertive"`.
  - **Log** → `role="log"` for chronological feeds.
  - Declare what announcement string fires when (often different from visible text).

**Where web's defaults make annotation unnecessary:**

- Native `<button>`, `<a href>`, `<input type="text|email|number|...>`, `<select>`, `<textarea>`, `<label>`, `<fieldset>`, `<legend>` — all of accessible name, role, state, focus, keyboard, and (for many) `forced-colors` are handled by the platform. Annotation declares the HTML element; everything else follows.
- `<dialog showModal>` — focus trap, focus return, Escape-to-dismiss, modal scrim, page-becomes-inert: all automatic.
- Popover API (`popover="auto"`) — light-dismiss and top-layer rendering automatic.
- `<details>`/`<summary>` — disclosure pattern, keyboard activation, `aria-expanded` mirrored automatically.

**Where web's defaults are wrong or absent — annotation is load-bearing:**

- Any custom interactive element built on `<div>` or `<span>` with `role="..."`. Avoid these; if unavoidable, full annotation across all concerns.
- Any composite Tier 2 widget — annotation must declare APG pattern; engineering implements per APG.
- `forced-colors` for any non-native paint (gradients, shadows, background-images, transparency).
- Reduced-motion treatment for any custom animation.
- Live regions in any dynamic component.
- ARIA relationships (`aria-controls`, `aria-describedby`) for non-trivial component composition.
- Heading level for any heading-bearing component (since the system can't know the document context).
- Focus-return target for any custom dismissible surface.

**Mapping the contract to component schemas.** The web annotations should map 1:1 to fields in the component's `.ai.json` (per 04-documentation's machine-readable layer):

```json
{
  "name": "Combobox",
  "role": "combobox",
  "apgPattern": "combobox-1.2",
  "html": "input",
  "ariaPattern": {
    "role": "combobox",
    "ariaExpanded": "controlled",
    "ariaControls": "popup-id",
    "ariaActivedescendant": "current-option-id"
  },
  "states": [
    { "name": "expanded", "ariaExpanded": "true", "announcement": "expanded" },
    { "name": "collapsed", "ariaExpanded": "false", "announcement": "collapsed" }
  ],
  "keyboard": "see APG combobox-1.2",
  "forcedColors": "survives unchanged",
  "reducedMotion": "popup transition is informational, 80ms in reduce",
  "liveRegion": null,
  "focusReturnOnDismiss": "trigger"
}
```

This makes the annotation contract a **machine-readable artefact**, not just a Figma-side document. The consuming code-generation pipeline (15-ai-in-ds) can read the schema, generate the component implementation, generate the test suite, and generate the documentation. The human-facing annotation in Figma is the source of truth for design intent; the JSON is the source of truth for engineering. Both derive from the same authoritative declaration. (See 03-component-library for components-as-data; 27-adaptive-interfaces-implementation for the structured-output rendering case.)

**Annotation packaging in Figma.** Same shape as mobile (per-frame Accessibility annotation layer with Element / Property / Value columns). The web vocabulary extends the mobile one with: `htmlElement`, `ariaPattern`, `forcedColors`, `prefersReducedMotion`, `landmark`, `headingLevel`, `inertOnOpen`, `focusReturnOnDismiss`. The four-platform annotation set (mobile + web) shares the conceptual columns; per-platform values diverge where the platform demands.

---

## References

Primary sources (verified June 2026; URLs stable at time of writing):

- **W3C** — WAI-ARIA 1.3: `https://www.w3.org/TR/wai-aria-1.3/`
- **W3C** — ARIA in HTML: `https://www.w3.org/TR/html-aria/`
- **W3C** — Accessible Name and Description Computation 1.2: `https://www.w3.org/TR/accname-1.2/`
- **W3C** — Core Accessibility API Mappings 1.2: `https://www.w3.org/TR/core-aam-1.2/`
- **W3C** — WCAG 2.2: `https://www.w3.org/TR/WCAG22/`
- **W3C** — WAI Authoring Practices Guide (APG): `https://www.w3.org/WAI/ARIA/apg/`
- **MDN** — ARIA reference: `https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA`
- **MDN** — accessibility tree: `https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree`
- **MDN** — `:focus-visible`, `:user-invalid`, `inert`, `<dialog>`, popover API
- **web.dev** — accessibility guides, particularly the dialog and popover migration write-ups
- **Web Platform Status** — `https://webstatus.dev` for Baseline status of CSS and HTML features
- **caniuse.com** — feature support tables, particularly for `inverted-colors`, `prefers-reduced-data`, and `aria-owns`
- **axe-core** — `https://github.com/dequelabs/axe-core` and `https://www.deque.com/axe/core-documentation/` for current ruleset and catch-rate documentation
- **react-aria** — `https://react-spectrum.adobe.com/react-aria/` for the most-credible cross-AT-tested React hook library
- **Radix UI** — `https://www.radix-ui.com/primitives` for the React primitive library with strong APG conformance
- **Ark UI** — `https://ark-ui.com/` for the framework-agnostic Zag.js-based library
- **Web Awesome / Shoelace** — `https://shoelace.style/` (legacy) / `https://webawesome.com/` for web-component-based DS primitives
- **NVDA release notes** — `https://www.nvaccess.org/post/` for behaviour changes per release
- **JAWS release notes** — `https://www.freedomscientific.com/Products/Software/JAWS/` for behaviour changes per release
- **WebKit accessibility blog** — `https://webkit.org/blog/category/accessibility/` for Safari/iOS VoiceOver changes
- **Apple — VoiceOver on the web** — `https://developer.apple.com/documentation/accessibility/web` for current Safari accessibility guidance

Version-dependent claims dated above:

- ARIA 1.3 W3C Recommendation, 2024.
- WCAG 2.2 W3C Recommendation, October 2023.
- `:focus-visible` Baseline 2022.
- `inert` Baseline 2023.
- `<dialog>` Baseline 2022 (with backdrop in WebKit 15.4).
- Popover API Baseline 2024.
- `:user-invalid` Baseline 2024.
- `prefers-reduced-transparency` Baseline 2024.
- `aria-description` widely supported (Safari 17.4, March 2024).
- Element internals AOM Phase 1 Baseline 2024.
- `inverted-colors` not implemented in Chromium or Gecko as of mid-2026.
- `prefers-reduced-data` not Baseline as of mid-2026.
- axe-core 4.10.x; React 19; React Aria 3.32+; Radix Primitives 1.x with 2.0 migration in progress.
- Reference engine line: Chromium 138, Firefox 142, Safari 18.5.
- Reference AT line: NVDA 2026.1, JAWS 2026, VoiceOver as shipped in macOS 15 / iOS 18, TalkBack in Android 16.

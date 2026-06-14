---
type: practice-area
title: Web Accessibility Implementation
description: Web accessibility implementation depth — ARIA 1.3, the user-preference media-query surface, composite-widget patterns under APG, live regions, native form primitives, contrast and focus, the four-engine × four-AT test matrix, and the cross-engine divergences that change implementation decisions.
tags: [extension, accessibility, a11y, web, aria, wcag, forced-colors]
timestamp: 2026-06-13
---

# 28 — Web Accessibility Implementation

> Our position on accessibility as a design system concern is in 14-accessibility — pair tokens, ARIA encapsulation, the four-layer model, conformance reporting under EAA and Section 508. That file is what the system must encode. The four mobile implementation files (16, plus the SwiftUI/UIKit, Flutter, Compose, React Native synthesis they were drawn from) are what each native framework actually does with it. This file is the same depth for the web. The gap between the architectural intent and the engine behaviour is largest on web because the platform is four engines (Blink, Gecko, WebKit, with Edge now Chromium-flavoured) crossed with four screen readers (NVDA, JAWS, VoiceOver, TalkBack), and every meaningful primitive has at least one cross-engine quirk that changes the implementation decision. This is what we mean when we say accessibility is architecture: the architecture has to be specified at a level where these quirks are load-bearing, not at a level where they're details.

---

## 1. The accessibility primitives the web platform exposes

The web's accessibility surface is layered. Native HTML elements ship default semantics. CSS computed style influences some semantics — `display: none` removes the subtree, `visibility: hidden` removes the subtree, `content-visibility: hidden` historically did not remove from the accessibility tree though Chromium and WebKit have been converging. ARIA overrides, augments, or fills gaps in HTML semantics. The user agent computes an accessibility tree from these inputs and exposes it to assistive technologies through platform APIs — UIA on Windows, AX on macOS and iOS, AT-SPI on Linux, the Android accessibility framework. The four major engines all implement the W3C Core Accessibility API Mappings (Core-AAM) but diverge in specific cases that matter for design systems.

The canonical web-platform rule is **build on the element, not above it**, surfacing in WAI-ARIA's first rule of ARIA use: *if you can use a native HTML element with the semantics and behaviour you require already built in, then do so*. For design systems this means a `Button` component must render `<button>`, not `<div role="button">` plus a keyboard handler. Where the rule loses is the long tail of UI patterns that have no native HTML element — combobox with custom popup, multi-select, tree, treegrid, complex grid, tablist, menubar, toolbar, disclosure with custom animation. For these, the system implements the ARIA Authoring Practices keyboard model on top of ARIA-supplied semantics.

### ARIA 1.3 surface area, dated honestly

ARIA 1.3 is the active working draft of WAI-ARIA. As of June 2026 it has **not** reached W3C Recommendation status — Recommendation is targeted for completion within 2026 but has not landed. (Claude's run overshot here, dating it as Recommendation in 2024; external agent's framing — "active editor's draft targeted for expected completion in 2026" — is the correct read.) The practical implication for the practice: cite ARIA 1.3 features as forthcoming, default to ARIA 1.2 as the spec floor for production claims, and verify support per feature rather than assuming the whole spec ships at once.

The relevant 1.3 additions for design-system work:

- **`role="suggestion"`, `role="comment"`, `role="mark"`** for collaborative-document and rich-text-editor patterns. Useful where the system ships a comment or revisions surface; otherwise nice-to-have.
- **`aria-description`** as a properties-only alternative to `aria-describedby` for cases where the description does not exist as a referenceable element. Cross-engine and cross-AT support is **fragmented as of mid-2026** — reliable on NVDA and iOS VoiceOver; less reliable on JAWS, macOS VoiceOver, and TalkBack *(external)*. Use `aria-describedby` as the safe default; reach for `aria-description` only when an IDREF target is structurally impossible and the consumer is on a known-good AT.
- **Refinements to `role="combobox"`** — the 1.2 redesign settled with corrections in 1.3.

**Abstract roles** (`roletype`, `widget`, `structure`, `landmark`, etc.) are the spec's ontological scaffold and **must never be authored** — they exist only to organise concrete roles. Only concrete roles (`button`, `dialog`, `combobox`, `listbox`) belong in HTML.

**ARIA-in-HTML** governs which roles can be applied to which elements. The sixth presentational rule is the one most worth knowing: `role="presentation"` (or `role="none"`) on an element is silently ignored when the element is focusable or has a global ARIA attribute *(both agents)*. This is a fail-safe — developers cannot accidentally create ghost focusable elements with no semantics. The system should still avoid `role="presentation"` on semantic elements; relying on the fail-safe is a code smell.

### The accessibility tree and engine architecture

Engines compile a tree from DOM + computed style + ARIA. Each node exposes computed accessible name, accessible description, role, and state. Pruning and update mechanics differ:

- **Chromium (Blink)** uses a dual-tree architecture — an internal accessibility tree feeds a serialized public tree consumed by assistive technologies. DOM mutations mark nodes "dirty"; the dirty set is processed and the public tree updated *(external)*.
- **Gecko** and **WebKit** dispatch tree-update events on different schedules. In SPAs with rapid mutation, the engines can disagree about whether a particular ARIA change has propagated when AT queries the tree, leading to clipped or skipped announcements *(external)*.

**Engine divergence to know about for design-system work:**

- **Computed accessible name on a button with mixed children.** `<button><span>Submit</span><span aria-hidden="true">→</span></button>` produces "Submit" on Chromium and Gecko; WebKit included the arrow text until Safari 16.4 (March 2023) *(Claude)*. Test arrow and icon adornments specifically.
- **Computed role for `<a>` without `href`.** Chromium reports `generic`, Gecko reports `link`, WebKit reports `link` *(Claude)*. Treat `<a>` without `href` as semantically incoherent — use `<button>` for actions, `<a href>` for navigation.
- **`role="presentation"` on `<table>`.** Chromium and Gecko strip table semantics; WebKit historically retained them in macOS VoiceOver's table mode (verified fixed in Safari 17) *(Claude)*. If the system uses tables for layout — don't — this is one place it matters.
- **`aria-owns`** has the worst cross-engine story. JAWS-Chromium and Narrator-Edge handle multi-IDREF correctly; VoiceOver and some Firefox configurations misnumber the child set, announcing "Tab 1 of 1" instead of "Tab 1 of 5" *(external; both agents agree on the gap, external gives the failure mode)*. The practical rule for the system: design components so `aria-owns` is never required — reorder DOM rather than declare logical ownership across the tree.

### Accessible name computation

The W3C Accessible Name and Description Computation 1.2 algorithm is consistent across engines for the simple cases. The hierarchy: `aria-labelledby` (resolved from IDREF chain) → `aria-label` → native attributes (`alt`, `title`, `<label>`) → element's inner text content *(both agents)*. A common pitfall: applying `aria-label` to non-interactive elements (a `<div>` or `<span>` without a widget role). Non-interactive elements are typically pruned from the accessibility tree to keep it small; the label is silently ignored *(external)*. The system should not allow `aria-label` on non-interactive primitives.

### The Accessibility Object Model and ElementInternals

The full AOM proposal — virtual nodes, custom AT events — remains a long-term target. What has shipped and matters for design systems is **ElementInternals** with the ARIA mixin, Baseline since late 2023. For systems shipping web components (Lit, Stencil, plain custom elements):

- **`this.attachInternals().role = 'checkbox'`** sets default semantics without exposing a `role` attribute in the DOM. Consumers cannot accidentally strip the semantic identity by overriding the attribute *(external)*.
- **IDREF reflection properties** — `ariaDescribedByElements`, `ariaLabelledByElements`, `ariaOwnsElements`, `ariaControlsElements` — accept arrays of element references rather than string IDs. The architectural advantage is that **a custom element can reference nodes inside its own Shadow DOM** without exposing IDs, bypassing the historical limitation that IDREF strings cannot cross shadow boundaries *(external)*. This is the load-bearing AOM feature for any system shipping as web components.

For systems shipping as React, Vue, or Svelte components, AOM is largely inert — the framework manages props and renders attributes. The IDREF reflection benefit only materialises if the system ships web components that hide their internals from consumers.

### Common pitfalls specific to design-system work

- **Redundant roles.** `<button role="button">`, `<nav role="navigation">`, `<main role="main">`. These pass automated checks but can fire AT as duplicate announcements, and force redundant tree work. The system should never emit a role that matches the native semantic *(both agents)*.
- **Role override on semantic elements.** `<h2 role="presentation">` to use a heading element for visual styling, or `<summary role="button">` which destroys the native expand/collapse state reporting *(external)*. The system should hard-disallow this in component templates; if a heading style is needed without a heading, it is a `<div>` with text-style classes, not an `<h2>` with stripped semantics.
- **ARIA without keyboard.** A `<div role="button">` with `onclick` but no `tabindex="0"` and no `keydown` handler for Space and Enter. Most common ARIA bug at PR review *(both agents)*. The system should not provide a `<div role="button">` primitive at all.
- **ARIA without focus.** A custom `role="combobox"` whose popup opens but where focus never moves into the popup, or where typeahead does not update `aria-activedescendant`. The APG keyboard model (§4) is the contract.
- **`aria-label` on non-interactive content.** Silently shadowed by visible text or ignored *(external)*. The system should not allow it on non-interactive primitives.
- **`aria-hidden` on focusable elements.** A focusable `<button aria-hidden="true">` is reachable by keyboard but invisible to AT — sequenced focus into nothingness *(both agents)*. The lint rule (`jsx-a11y/no-aria-hidden-on-focusable`) catches this; the system should ship the lint rule as a default and component templates should never permit it.
- **Label/labelledby precedence.** `aria-labelledby` wins over `aria-label`; both win over visible text on a `<button>`. Designers regularly assume visible text is the source of truth; engineers regularly ship `aria-label` "just in case." The annotation contract (17-accessibility-annotation-contract, web extension) declares which one is the announced name.

---

## 2. Focus and keyboard

Web focus is a single system, unlike Compose's input-focus-vs-AT-focus split. The focused element receives keyboard events, gets `:focus` styling, and is what AT focuses. Screen-reader virtual cursors (NVDA, JAWS, VoiceOver) layer above DOM focus — they navigate independently and only move DOM focus when the user activates an interactive element. The design-system implication: DOM focus is the contract; AT layers on top.

### tabindex and the natively focusable set

The set of natively focusable elements is finite: `<a href>`, `<button>`, `<input>` (excluding `type="hidden"`), `<select>`, `<textarea>`, `<details>` summary, `<area href>`, anything with a non-negative `tabindex`. Everything else needs `tabindex="0"` to enter the tab order or `tabindex="-1"` for programmatic-only focus.

**Positive `tabindex` values** create a parallel tab order that interleaves with the natural one in unpredictable ways. Both agents converge on the discipline: the system hard-disallows positive `tabindex` via `jsx-a11y/tabindex-no-positive` (or equivalent) in CI.

### `:focus-visible`, `:focus`, `:focus-within`

`:focus-visible` is the focus-indicator primitive. Baseline 2022 (Chromium 86, Gecko 85, WebKit 15.4). The user agent's heuristic decides when an indicator is appropriate — keyboard focus and programmatic focus from action handlers trigger it; mouse focus on a button does not. The system implication is significant:

- **Focus-ring tokens apply via `:focus-visible`, not `:focus`.** A button styled with `:focus { outline: 2px solid var(--focus-ring); }` shows a ring on every click — visually noisy. `:focus-visible` shows the ring only when keyboard or AT focus reaches the button.
- **`:focus-within`** for parent containers (forms, cards) indicating "something inside has keyboard focus." Useful as a system-level pattern for compound-input affordances.
- **The legacy `:focus` fallback** is no longer required for any modern engine. Modern systems can use `:focus-visible` directly.

WCAG 2.2 SC 2.4.13 (Focus Appearance) is AAA but effectively procurement-grade. It mandates a 2px-thick perimeter outline at 3:1 contrast against adjacent colours, with no colour as the sole indicator *(both agents)*. Branded focus rings — a brand-blue 1px outline — often fail against light backgrounds. The system ships a default focus ring meeting 2.4.13 and overrides only with explicit accessibility review.

### `inert`

`inert` (Baseline 2023) is the modern primitive for disabling subtrees. Setting `inert` removes all descendants from the focus order, removes them from AT navigation, and disables pointer events. This replaces:

- Setting `tabindex="-1"` on every focusable descendant (incomplete — does not disable AT).
- Polyfills like `wicg-inert` (now obsolete).
- Manual focus trapping with event listeners.

The system uses `inert` for everything that should be visible-but-not-interactable — modal backgrounds, slide-out panels' main-content peers, off-screen-but-pre-rendered route panes.

### `<dialog>` and the popover API

- **`<dialog>` element** — Baseline 2022 (Chromium 37, Gecko 98, WebKit 15.4). When opened via `showModal()`, `<dialog>` provides automatic focus move into the dialog, focus trap (Tab cycles within), Escape dismissal, and surrounding-document `inert`. This is the modern modal-dialog primitive *(both agents)*.
- **Popover API** (`popover` attribute, `popovertarget`) — Baseline 2024 (Chromium 114, Gecko 125, WebKit 17). `popover="auto"` provides non-modal popover with light-dismiss and top-layer rendering; `popover="manual"` requires script. Use for menus, tooltips, dropdowns — anything that should appear above siblings without trapping focus.

The Popover API does **not** trap focus, does not move focus into the popover, and does not inert the background *(external)*. If the system uses `popover` for an interactive mega-menu, it must wire focus management explicitly — focus into the popover on open, focus trap or roving-tabindex within, focus return on dismiss.

### When to write a manual focus trap

Almost never, in 2026. The remaining cases:

- Custom modal patterns built before `<dialog>` was Baseline. Migration is the answer.
- Non-modal popovers that need focus-into and Escape-with-return — pair the popover API with `focus-trap`, `react-aria`'s `useFocusManager`, or `radix-ui`'s `FocusScope`.
- Complex composites (multi-pane dialog with internal tabs) needing fine-grained focus restoration.

Hand-rolling a focus trap from scratch in 2026 is a yellow flag in code review.

### APG keyboard models per pattern

The W3C ARIA Authoring Practices Guide is the keyboard contract. The patterns and their canonical models:

- **Combobox 1.2** — text input with a popup. Down arrow opens (or moves into popup), Up/Down navigate options, Enter selects (and closes), Escape closes (with optional value reset), typing filters. `aria-activedescendant` keeps DOM focus on the input while marking the focused option.
- **Listbox** — Up/Down navigate, Home/End jump, typeahead, Enter or Space selects. `aria-multiselectable="true"` for multi-select; Shift+Click and Shift+Arrow extend.
- **Menu and Menubar** — Arrow navigation along the axis, perpendicular arrows open submenus, Escape closes, Tab leaves entirely. Menubar horizontal; menu vertical.
- **Tablist** — Left/Right navigate, Home/End jump, Enter or Space activate. Two activation modes — automatic (focus changes panel) and manual (focus moves but panel changes only on activation). Both APG-conformant; the system picks one and documents it. Automatic is more discoverable; manual is preferred when each panel has expensive content.
- **Tree** — Up/Down move through visible items, Right expands or moves into, Left collapses or moves out, Enter activates, typeahead.
- **Treegrid** — Tree plus grid. Up/Down move rows, Left/Right move cells, Right at last cell moves to next row and expands, Left at first cell collapses. Most complex APG pattern. AT support varies; always prefer a simpler model if possible.
- **Grid** — Arrow navigation across cells, complex selection and edit modes. Native `<table>` does not provide grid keyboard model — `role="grid"` is needed plus the keyboard handlers.
- **Disclosure** — `<details>`/`<summary>` (preferred when target lives inside) or `<button aria-expanded aria-controls>` paired with a separate region.
- **Dialog** — `<dialog>` + `showModal()` for modal; `<dialog>` + `show()` non-modal (rare).
- **Tooltip** — Triggered by hover or keyboard focus. Persistent on focus; dismissed by Escape, focus loss, or pointer leave. WCAG 1.4.13 (Content on Hover or Focus) governs dismissibility, hoverability, persistence.
- **Toolbar** — Like menubar but for actions, not menus. Roving tabindex within.

### Roving tabindex vs. `aria-activedescendant`

Two patterns for managing focus inside composite widgets:

**Roving tabindex.** Exactly one descendant has `tabindex="0"`; all others have `tabindex="-1"`. As the user navigates, the system moves the `tabindex="0"` and calls `.focus()` on the new active descendant. DOM focus moves; `:focus` reflects the active descendant. Works on tablists, menus, toolbars, trees. **Engine and AT support is uniform** *(both agents)*.

**`aria-activedescendant`.** DOM focus stays on a container; `aria-activedescendant` points to the conceptually-focused descendant. The descendant does not receive `:focus`; the system styles it as active via an `[aria-activedescendant]`-derived selector. Best for combobox (input must keep DOM focus while user navigates options). **Brittle outside narrow patterns** — Narrator-Edge and TalkBack-Android frequently fail to announce virtual focus updates unless the parent and child roles match a predefined APG relationship *(external)*; JAWS and NVDA differ in re-announcement aggressiveness *(Claude)*.

The practical decision: roving tabindex is the recommended default *(both agents)*. Reach for `aria-activedescendant` only where the pattern requires it (a text input that must keep DOM focus while the user is selecting from a popup is the canonical case).

### Skip links, landmarks, and the heading outline

**Skip links** remain mandatory in 2026 because keyboard users still benefit from bypassing repeated navigation. The system's discipline:

- The skip link is the first focusable element in the document.
- It is visually hidden until focused (CSS clip-path, off-screen positioning) and becomes visible on focus, meeting standard contrast.
- The target — typically `<main id="main">` — must have **`tabindex="-1"`** *(external; load-bearing detail Claude omitted)*. Without it, the browser merely scrolls; the user's next Tab returns to the top of the document.

**Landmark regions.** `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<section aria-label="...">`. AT users navigate by landmark; the system's layout primitives must produce a clean landmark outline.

**Heading outline.** `<h1>` through `<h6>` form the document outline. The HTML5 outline algorithm (which would have allowed implicit re-leveling per `<section>`) was never implemented by AT; treat each level as explicit. **Component primitives must accept a `headingLevel` prop** rather than hard-coding a level. A `Card` with a title cannot decide its heading level — the consumer's document context decides. This is one of the more-violated DS contracts in shipping product code *(Claude)*.

---

## 3. User preferences and the media-query surface

The web platform exposes user preferences via CSS media queries the system respects at the foundation layer. Status as of mid-2026:

| Query | Baseline | Notes |
|---|---|---|
| `prefers-reduced-motion` | 2020 | Universally supported |
| `prefers-color-scheme` | 2020 | Light / dark / no-preference |
| `prefers-contrast` | 2024 | Chromium 96, Gecko 101, WebKit 14.1 |
| `prefers-reduced-transparency` | 2024 | Chromium 118, Gecko 113, WebKit 17.4 |
| `forced-colors` | 2022 | Chromium 89, Gecko 89, WebKit 14.1 |
| `prefers-reduced-data` | Not Baseline | Chromium-only behind a flag; treat as forward-looking |
| `inverted-colors` | Not Baseline | WebKit-only (iOS / macOS); not in Chromium or Gecko |

### `forced-colors` mode

`forced-colors: active` is the most consequential preference for design-system architecture. When active — typically Windows High Contrast Mode but increasingly other contexts — the user agent overrides paint properties (backgrounds, borders, foreground colours, shadows, gradients, certain background images) with a small palette of system-defined colours. The CSS `system-color()` keywords reflect the user's chosen palette and survive forced-colors mode:

| Keyword | Standard mapping | Design-system application |
|---|---|---|
| `Canvas` | Page background | Surface tokens, document backgrounds, modal scrims |
| `CanvasText` | Primary text | Body typography, data points, standard labels |
| `LinkText` | Hyperlinks | Standard `<a>` and link-styled buttons |
| `ButtonFace` | Button background | Interactive component backgrounds, toggle tracks |
| `ButtonText` | Button text | Text within interactive bounds, SVG icon fills in buttons |
| `Field` | Input background | Text-input surfaces |
| `FieldText` | Input text | Text within inputs |
| `GrayText` | Disabled text | Disabled inputs, unavailable options |
| `Highlight` | Selected text / focus | Focus rings, selected tab indicators, active slider tracks |
| `HighlightText` | Selected-text foreground | Text within selection / focus |

What the system encodes:

- **Components relying on `background-image`, gradients, `box-shadow`, or transparency for state expression need a `@media (forced-colors: active)` override** that re-establishes state through `border`, `outline`, or `system-color()` values. A selected list item indicated by a 4px left border and a tinted background — in forced-colors, the tinted background is stripped; the border survives only if it is solid.
- **Custom focus rings use `system-color()` in forced-colors mode.** A branded focus ring (`outline: 2px solid var(--focus-ring);`) is stripped to `Highlight` in forced-colors. The system sets `outline: 2px solid Highlight;` inside the forced-colors block, or uses `outline-color: currentColor` so the user agent computes against the forced palette.
- **The transparent-border trick** *(external)*. Borders declared as transparent are *rendered* in forced-colors using `ButtonText` or `Highlight` without dictating a hue in normal mode. This restores structural visibility for components that otherwise have no visible border. The system can ship this as a default for any container component whose default visual treatment is "no border."
- **SVG icons set `fill: currentColor`** so they inherit the forced foreground; icons with explicit hex fills disappear in forced-colors.
- **Selected state in radio / checkbox** is automatically handled by the user agent for native `<input>`; for custom controls (a `Switch` primitive), forced-colors must be tested specifically.

The system ships a single forced-colors audit pass per component and a Storybook addon mode that simulates `forced-colors: active`. The Storybook accessibility addon supports this since 2023; the practice should adopt it as a default mode for any system component.

### The reduce-motion contract

What the system encodes once vs. what each component decides locally — derived from 18-motion-foundations and applied to web specifically. The tripartite split is load-bearing:

- **Decorative motion** — animation that has no informational role. A pulse on a notification badge, a hover scale on a card, a parallax background. In `reduce`, set to `none`. Vestibular-trigger candidates (parallax, large rotations, autoplay video with translation) belong here and must always be `none`.
- **Informational motion** — motion that indicates causality between an action and a result. An accordion expanding, a focus ring appearing, an error-state shake. In `reduce`, shorten to ~50–80ms — preserve the *change* signal without the *animation* of it.
- **Essential motion** — motion that conveys content the user cannot otherwise discern. An indeterminate progress spinner; a video the user explicitly invoked. In `reduce`, replace with a static fallback or drastically simplify, but do not eliminate — without it, the user has no signal that the system is working *(external)*.

The system layer (foundation tokens) carries this in motion-duration tokens with `prefers-reduced-motion: reduce` variants. The component layer references the duration token, not a media query. The system fails PR review on any component-level `@media (prefers-reduced-motion)` block — that is a sign the component is making a decision the foundation layer should make.

The `@media (prefers-reduced-motion: no-preference) { ... }` wrapper pattern is more robust than overriding inside a `reduce` block, because it works correctly when the user toggles preferences mid-session. Default state is no animation; animation is opt-in.

**`scroll-behavior: smooth`** is *not* automatically reduced. Programmatic smooth scrolling needs explicit gating — `scrollIntoView({ behavior: 'smooth' })` in JS checks `matchMedia('(prefers-reduced-motion: reduce)').matches` and uses `instant` if so.

**View Transitions API** (Chromium 111+, WebKit 17.4+) honours `prefers-reduced-motion: reduce` via a built-in `::view-transition` mechanism, but only if the system's transition CSS does not override the default. 19-motion-implementation-web flags this gotcha; the implementation rule is to wrap any `::view-transition-old`/`::view-transition-new` animation in `@media (prefers-reduced-motion: no-preference)`.

### `prefers-contrast: more`

Indicates the user wants increased contrast — typically WCAG AAA levels. The system can:

- Ship a high-contrast theme that uses `prefers-contrast: more` as the resolution mode. Heavier-weight than relying on the user agent — and worth doing for systems shipping to public-sector / EAA-required customers.
- Apply component-level overrides — thicken borders, increase outline weights, raise text contrast on neutrals.
- Default to nothing different, relying on shipping AA everywhere by default. Acceptable for AA-conformance use cases; insufficient when procurement specifies enhanced contrast or AAA.

The relationship to `forced-colors`: `prefers-contrast: more` is the user's request for *more* contrast within the system's chosen palette; `forced-colors: active` is the platform overriding the palette entirely. They are orthogonal — a user may set both, neither, or one. CSS treatments differ; both must be tested.

### Color-scheme and the double-inversion pitfall

`prefers-color-scheme: dark` is the user's preferred theme; the system honours it via dark-mode tokens and the `color-scheme` CSS property. Always set `color-scheme` at the document root: `:root { color-scheme: light dark; }`. Without it, Chromium's force-dark heuristics may invert the site, often badly *(Claude)*.

The double-inversion pitfall: Smart Invert (iOS / macOS) inverts page paint regardless of `prefers-color-scheme`. If the system serves a dark theme to a user who has also enabled OS-level inversion, the dark theme is inverted back into a blindingly bright light theme — defeating the user's intent *(external)*. The mitigation is the WebKit-specific `inverted-colors` media query (where supported) or CSS filters to opt brand images, photography, and icons out of the inversion matrix. Smart Invert is meant for text-heavy reading; it assumes images should not invert.

---

## 4. Composite widget patterns and the ARIA Authoring Practices contract

The system's component decisions for composite widgets fall into three tiers.

**Tier 1 — Wrap a native control.** `Button`, `TextField`, `Checkbox`, `Radio`, `Select` (single-select with simple options), `Textarea`, `Slider` (range input), `ProgressBar` (`<progress>`), `Disclosure` (`<details>`/`<summary>`), `Dialog` (`<dialog>`). Native controls' accessibility is generally complete, AT-tested across engines, keyboard-correct by default, forced-colors-aware out of the box. The system's job is theming and integration, not replacing semantics.

**Tier 2 — Compose ARIA on a custom widget where native loses.** `Combobox` (text input with rich popup; native `<select>` does not support the popup model), `Multi-select`, `Tabs` (no native), `Menu` and `Menubar` (no native), `Tree`, `Tooltip`, `Tag`/`Chip` (custom interactive). For these, follow APG keyboard models exactly — they are derived from extensive AT testing.

**Tier 3 — Highly bespoke, build with extreme care.** `Treegrid`, `Grid` (with edit modes), spreadsheet-like tables, custom rich-text editors. These are where most a11y bugs live. The practice's recommendation: do not build these in-house unless the brand requires it; reach for a battle-tested library (TanStack Table, Slate, Lexical) with documented accessibility support.

### Where APG guidance disagrees with current AT behaviour

APG is gold-standard for the keyboard model but prescriptive in places where AT implementations diverge.

- **Combobox autocomplete patterns.** APG documents three (no autocomplete, list autocomplete, list-with-inline-autocomplete). The "list autocomplete" pattern's expected behaviour for what AT announces when the option list filters has historically diverged across NVDA and JAWS *(Claude)*. As of NVDA 2026.1 and JAWS 2026, behaviour is closer to convergence but the inline-autocomplete pattern remains unreliable.
- **APG live-region recommendations during combobox typing.** APG occasionally recommends a live region announcing the count of available suggestions as the user types. Appending dynamic strings to a live region during rapid keyboard input causes screen-reader buffers to flush — clipped, delayed, or chaotic announcements *(external)*. The system architects comboboxes to **debounce live-region updates** and **clear the region's text node on blur** to avoid stale residual content being read on next interaction. APG conformance is a starting point; the corrections are practitioner-tier.
- **`aria-owns` for cross-tree relationships.** APG describes patterns that use `aria-owns` to logically own descendants from elsewhere in the DOM. WebKit and some Firefox configurations misnumber the child set. Design components to avoid `aria-owns` where possible.
- **JAWS table mode.** JAWS in default settings reads tables in "table mode" (cell-by-cell with row/column header context). For `role="grid"`, JAWS treats them as forms-mode grids — navigation keys are intercepted by JAWS unless the user enters "forms mode" (PC Cursor). The system cannot fix this; designers should know JAWS users may experience grid widgets differently than NVDA / VoiceOver users.
- **VoiceOver and `aria-current="page"`** announces "current page" only on links in some configurations; on buttons or list items, it is silent. Long-standing iOS VoiceOver quirk *(Claude)*. Workaround: use `aria-current="page"` *and* include "current" in the accessible name when the visual treatment is inert ("Home, current page").

### The library landscape

Building APG patterns from scratch in 2026 is a yellow flag — the libraries are good enough that engineering hours are better spent on the system's distinctive surface, not re-implementing the combobox.

| Library | Use case | Accessibility depth | Trade-offs |
|---|---|---|---|
| **react-aria** (Adobe) | Enterprise, AAA-rigorous, government procurement | Exhaustive; deep iOS VoiceOver and touch-AT handling | Steep learning curve; opinionated hooks; bundle-size impact |
| **Radix Primitives** | Composable DS foundations | High; strong roving-tabindex; APG-conformant | Compound-component composition learning curve |
| **Headless UI** | Tailwind-centric | Moderate; basic ARIA states and focus traps | Limited API control; punts on complex i18n |
| **Ark UI** | Cross-framework (React, Vue, Solid) | High; finite-state-machine-driven (Zag.js) | Newer ecosystem; less mature AT validation |
| **Web Awesome / Shoelace** | Web-component-based DSes | Credible | Choose when the system itself ships as web components |
| **Reach UI** | — | Was credible | Effectively dormant since 2023; not recommended for new systems |

The practical recommendation:

- **React-first system targeting AAA / government / EAA-procurement** → react-aria. Gold standard for accessibility rigor, particularly for iOS VoiceOver virtual-cursor edge cases *(both agents)*.
- **React-first system targeting standard consumer or B2B SaaS** → Radix Primitives. Strong APG conformance, lighter learning curve, more composable than react-aria.
- **Multi-framework system** → Ark UI (React / Vue / Solid via Zag.js).
- **Web-component-based system** → Lit + Web Awesome's primitives, or write your own with rigorous AT testing.

---

## 5. Live regions, announcements, and dynamic content

Live regions are how the system communicates dynamic content changes to AT without moving focus.

### Mechanics

- **`aria-live="polite"`** — announce on the next pause in user activity. Most uses.
- **`aria-live="assertive"`** — announce immediately, interrupting current speech. Urgent errors only.
- **`aria-live="off"`** — explicit off (rarely needed; the default).
- **`aria-atomic="true"`** — when the region updates, announce the entire region's content; otherwise (the default), announce only the changed nodes. NVDA respects atomic; JAWS only partially *(Claude)*.
- **`aria-relevant="additions text removals all"`** — which DOM mutations trigger announcement. Default is `additions text`; removals are not announced by default.
- **`role="status"`** — implicit `aria-live="polite"` + `aria-atomic="true"`. Best for status messages.
- **`role="alert"`** — implicit `aria-live="assertive"` + `aria-atomic="true"`. Best for errors.
- **`role="log"`** — for chronological logs (chat, console output).
- **`role="timer"`** and **`role="marquee"`** — rarely used; engine support varies; avoid.

### Engine and AT behaviour

All four engines correctly fire AT events when live-region content changes. The variance is at the AT layer:

- **NVDA** announces polite reliably; assertive with priority over reading flow.
- **JAWS** does the same with the atomic quirk above.
- **VoiceOver (macOS)** announces polite reliably; assertive interruptions are sometimes timed differently than NVDA.
- **VoiceOver (iOS)** has historically been the weakest with live regions; iOS 17+ improved significantly. Status messages now announce reliably; complex regions with `aria-atomic` and multiple children remain less predictable *(Claude)*.
- **TalkBack on Chromium-Android** — polite and assertive both work.

### The cardinal rule

**The live-region container must exist in the DOM before the text node is mutated.** If a component mounts a new `<div aria-live="polite">Saved</div>` simultaneously with its payload, the accessibility tree interprets this as a static node insertion and AT does not announce *(both agents)*. This is the most frequent point of failure in React and other SPA architectures.

The system's architectural answer: **a single, persistent, visually hidden live-region provider mounted at the application root.** Toast / snackbar / announcement components do not each have their own live region; they all push text into the shared one *(both agents)*. The system ships:

- A `<LiveRegion>` primitive (or framework-equivalent provider) the application mounts at page root.
- A `useAnnouncement()` hook (or equivalent) that pushes a string with controlled timing — debounce, queue, replace.
- A per-form `<FormErrorSummary>` that updates as a polite live region when validation errors change.

### Patterns mapped to roles

- **Toast / snackbar (success)** → `role="status"`. The user should not be interrupted to hear "Saved."
- **Toast / snackbar (error)** → `role="alert"`. The user should know immediately.
- **Inline field error** — not a live region directly. Use `aria-describedby` to associate the message with the field; the error announces when the field receives focus. For async errors that appear without focus, additionally update a polite form-level live region.
- **Form-level error summary** — `role="alert"` if the summary appears on submit; `role="status"` if it updates as the user types. Both APG-acceptable; pick one and document.

### Status messages — the SC 4.1.3 evidence problem

WCAG 2.2 SC 4.1.3 (Status Messages) requires that status updates can be programmatically determined and presented by AT without receiving focus — exactly what live regions solve. The audit-evidence problem: automation can verify the live region exists, has the correct role, has reasonable content. Automation **cannot verify the message was announced** — that depends on AT timing, queue state, and user-agent settings *(both agents)*. SC 4.1.3 evidence must include manual AT testing.

### SPA route changes

When the URL changes via History API and the page content changes without a full reload, AT does not automatically announce. The canonical fix:

1. Update `document.title` to the new page title.
2. Move focus to a known landmark (typically `<main>` or the page's `<h1>`). The focus move triggers AT to read the new content.
3. Optionally push a polite announcement to the live region ("Navigated to Settings").

Most React, Vue, and Svelte routers do not do this by default; the system provides a `<RouteAnnouncer>` component the application opts into. react-router and Next.js each have community patterns; the system wraps whichever the consumer uses.

---

## 6. Forms, errors, and the input contract

Native form elements remain best-in-class for accessibility on the web. The system's job is to compose, theme, and integrate — not replace.

### Native primitives

- **`<form>` with `<label>` associations** — `<label for="x">Name</label> <input id="x">` or implicit `<label>Name <input></label>`. The `Field` primitive must produce one of these patterns; a `<label>` not associated with an input is a system-level a11y bug.
- **Typed `<input>`** — `email`, `tel`, `url`, `number`, `date`, `color`, `search`, `password`. Each provides better mobile keyboards, better autocomplete, sometimes better validation. The system exposes typed inputs as primitives, not generic text inputs with type props the consumer must know to set.
- **`<select>`** with `<option>` and `<optgroup>` is fully accessible. Do not replace `<select>` with a custom combobox unless the design requires search, filter, or rich items that `<select multiple>` cannot deliver.
- **`<fieldset>`/`<legend>`** for grouped inputs (radio groups, related checkboxes). The `RadioGroup` primitive renders `<fieldset>` with the group label as `<legend>`. Skipping `<fieldset>` for visual reasons is a frequent system-level violation; the rendered HTML must always have it, even if visual styling hides it. `<fieldset>` plus `<legend>` is **the only universally robust method** for ensuring the group description is announced alongside each child input *(external)*.

### Constraint validation and the `:user-invalid` pseudo-class

- **HTML validation attributes** — `required`, `minlength`, `maxlength`, `pattern`, `min`, `max`, `step`. The user agent enforces them; failure shows a native error tooltip on submit. The system can leverage these for client-side validation without writing JS.
- **`:user-invalid`** — applies after the user has interacted with the field (changed it, blurred it). Baseline 2024 (Chromium 119, Gecko 88, WebKit 16.5). Replaces `:invalid`, which fires immediately on render and produces red borders on every required field on form mount.
- **`:user-valid`** — corresponding pseudo for validated-and-engaged. Baseline 2024.
- **`invalid` event** — fires when constraint validation fails on submit. The system uses this to reposition focus to the first invalid field, update an error summary, etc.

The system pattern: `:user-invalid` for the visual error styling, the `invalid` event for focus management on submit, a polite live region for the form error summary.

### `aria-describedby` vs. `aria-errormessage`

`aria-describedby` is generic — AT announces the description regardless of whether the input is in a valid or invalid state, creating verbosity *(external)*. `aria-errormessage` (introduced in ARIA 1.1) is semantically precise: it points to the error container and only becomes pertinent when `aria-invalid="true"`.

Cross-engine and cross-AT support for `aria-errormessage` is fragmented as of mid-2026:

- **Robust:** JAWS-Chromium, NVDA, iOS VoiceOver *(external)*.
- **Unreliable:** macOS VoiceOver, TalkBack-Android — TalkBack's accessibility API expects string payloads rather than node references; `aria-errormessage` often results in silence *(external)*.

**The hybrid implementation pattern** *(external)*: use `aria-errormessage` to support modern APIs, and additionally inject the error string into the `aria-describedby` IDREF list when `aria-invalid="true"`. This maintains correct semantics where `aria-errormessage` is honoured and provides a fallback announcement everywhere else. Until support converges, the hybrid is the system's default.

The relationship to `:user-invalid`: `:user-invalid` is the *visual* rule; `aria-invalid` is the *AT* rule. Both fire on the same condition — after the user has engaged with the field.

### Required, optional, and error-summary patterns

Multiple acceptable patterns; pick one and document.

- **Asterisk plus legend** — every required field has a `*` in the visible label; the form has a legend "* indicates required field." Add `aria-required="true"` to the input. Most accessible across configurations.
- **Optional indication** — required is the default; optional fields are marked "(optional)." Avoids visual asterisk noise. Less common but well-tolerated by AT.
- **Required attribute alone** — `<input required>` and the user agent's native error on submit. Acceptable for short forms; insufficient for long forms where the user wants to know required-ness in advance.

**Error-summary patterns.** For forms with multiple fields, an error summary at the top of the form (after submit) is the GOV.UK pattern, widely adopted in compliance contexts. The summary is a polite live region (`role="alert"` if it appears on submit, `role="status"` if it updates as the user types) listing each error with a link to the corresponding field. Activating a link moves focus to the field and announces the field's `aria-describedby` content.

### Specialised inputs

- **Date pickers.** `<input type="date">` is now strong enough for most cases. Native UI varies per browser and OS; that is a feature — it matches the user's platform conventions. Custom date pickers are reserved for cases where the visual design requires it (an inline calendar instead of a modal); even then, the underlying `<input type="date">` should be the source of truth and the visual UI a styling layer. Where the system must restrict specific dates (holidays, blackout periods), a custom ARIA-grid-based date picker is justified, with full arrow-key traversal *(external)*.
- **Combobox.** Native `<select>` does not support search; custom comboboxes (§4 Tier 2) fill this gap.
- **File upload.** Native `<input type="file">` is fully accessible. Drag-and-drop overlays are an enhancement; the underlying `<input>` must remain for keyboard and AT users. The pattern: `<label>` wraps both the visual drop zone and the file input; clicking either triggers the file picker; drag-and-drop is the same upload via JS. The label's accessible name is what AT announces.

### `autocomplete` and SC 1.3.5

WCAG 2.1 SC 1.3.5 (Identify Input Purpose) requires that input purposes (name, email, address, payment) be programmatically identifiable. The `autocomplete` attribute is the mechanism. Values like `name`, `given-name`, `family-name`, `email`, `tel`, `street-address`, `cc-number`, `bday`, `postal-code` are recognised by browsers (for autofill) and by some AT (for purpose identification). The system's `Field` primitive accepts an `autocomplete` value and passes it through; the system documents the values relevant to common form patterns. This is a major cognitive-load and dexterity-affordance benefit, not an edge case.

---

## 7. Color, contrast, and the visual layer

### WCAG 2.x vs. APCA

The Advanced Perceptual Contrast Algorithm (APCA) provides a more nuanced calculation model that accounts for font weight, ambient context, and spatial frequencies, correcting known flaws in the WCAG 2.x relative-luminance formula (which under-rates blue-on-black and over-rates dark-mode pairs).

APCA was a candidate for WCAG 3, but the W3C Accessibility Guidelines Working Group **removed APCA from the WCAG 3.0 draft in late 2023** due to lack of consensus, and WCAG 3.0 itself is not expected to reach Recommendation status until roughly 2030 *(external)*.

The legal standard — including ADA enforcement and the EAA — remains strictly bound to **WCAG 2.1 / 2.2 contrast formulas**: 4.5:1 for normal text, 3:1 for large text and UI components. The practice's discipline:

- **Conformance and procurement use WCAG 2.x.** Auditors verify against it; ACR / VPAT documents reference it.
- **Design-time tooling can use APCA-aware checks** for cases where WCAG 2.x's known flaws produce poor outcomes (the dark-mode and blue-on-black cases).
- **Bridge-PCA formulas** can be used to build APCA-aware design tooling that *also* clears WCAG 2.x minimums *(external)*. This is the safe path to use APCA's perceptual benefits without legal-compliance risk.
- **Never claim APCA conformance to clients.** APCA is informational, not normative.

### Pair tokens on the web specifically

Per 14-accessibility, contrast is a property of *foreground × background pairs*, not individual tokens. On the web:

- **Foreground tokens declare their intended background.** `text-on-surface-primary`, `text-on-surface-elevated`, `text-on-brand-primary`. Each token has a `$description` (per DTCG) noting the assumed background and the contrast ratio.
- **The system enforces contrast at build time** via DTCG validation: pair tokens that produce sub-AA contrast fail the build. (See 22-token-architecture-extensions for the DTCG validation pattern; 24-tokens-at-scale for the multi-brand version.)
- **Developers consume pair tokens.** A `Button` uses `text-on-brand-primary` for its label, not `text-primary`. The foreground / background relationship is explicit at the consumption site.
- **Themes and densities multiply pairs.** Light × dark × high-contrast × density = N foreground tokens per logical text role. The validation matrix is correspondingly large; CI runs all combinations.

### Non-text contrast — SC 1.4.11

Borders, focus rings, icons, and controls' visual boundaries must meet 3:1 against adjacent colours. Common system-level violations:

- **Buttons with no border, only fill colour against background.** A blue button on white passes 3:1 only if the blue is dark enough. A pale-blue button often fails.
- **Form-field borders** — a 1px gray border against white frequently fails 3:1. Ship form fields with a contrast-aware border colour. (Text Field is the worked example for the rest of the form-field implementation contract — `useId`-generated id wiring, the auto-stitched `aria-describedby` helper+error chain, `forwardRef` to the input node, and the polite-live-region character counter; see components/text-field.md §6 and §11.)
- **Disabled state** — disabled inputs / buttons are exempted from contrast requirements per WCAG 2.2 SC 1.4.3 and 1.4.11. The system can use lower-contrast disabled states. (This exemption is exactly why a natively-disabled control can be both illegible *and* unreachable — the case for the focusable inactive pattern on relevant-but-blocked buttons; see components/button.md §4.)
- **Decorative content** — pure decoration (illustrations without informational role) is exempted. The system distinguishes decorative from informational icons; decorative gets `aria-hidden="true"`, informational meets 3:1.

### Focus-indicator contrast — SC 2.4.13

WCAG 2.2 SC 2.4.13 is AAA but procurement-grade. The criterion: focus indicators are at least 2 CSS pixels thick along the longest side, and have at least 3:1 contrast **between focused and unfocused states** *(both agents)*. The contrast check is between states, not just between indicator and background — catching the common pattern of "a 1px outline only slightly different from the unfocused border."

The branded-focus-ring tension: brand wants brand-coloured continuity; the standard wants 2px and 3:1. The reconciliation:

- The branded ring is the primary visual; the system tokenises it as `focus-ring-brand`.
- Forced-colors strips it; the system falls back to `Highlight`.
- High-contrast theme (under `prefers-contrast: more`) thickens the ring or switches to a system-aware token.
- For mid-contrast brand colours (a brand-blue against light backgrounds), the system shadows the ring with a darker outer ring to ensure 3:1 against any adjacent surface.

The audit pattern: capture a screenshot of every interactive primitive in focus and run automated 2.4.13 verification (DevTools or axe-core).

### Colour is not the sole carrier of meaning — SC 1.4.1

Status colours must be paired with text labels or icons. The system encodes:

- **Status pills and badges** include both colour and icon by default; the icon cannot be omitted by composition rules.
- **Form errors** show a coloured border *and* an error icon *and* text — not just colour.
- **Charts** include patterns or shapes alongside colour. (Chart components remain a known practice gap — see 09-gaps-and-open-questions §5.2.)

The annotation contract (17, web extension) carries a "colour-meaning" field per state where colour is meaningful; if non-empty, the engineer verifies a non-colour indicator is present.

---

## 8. Testing, tooling, and conformance evidence

### Static analysis

- **`eslint-plugin-jsx-a11y`** — React / JSX-aware lint. Catches missing alt, missing labels, click handlers without keyboard handlers, ARIA typos, `aria-hidden` on focusable elements. The system ships a recommended ESLint config.
- **axe-core lint** — IDE and CI integration; lighter coverage than runtime axe but catches the same statically-analysable surface.
- **HTML validation** in CI (W3C validator or `html-validate`) catches malformed structure that breaks AT.
- **Storybook accessibility addon** — runs axe-core on every story, surfaces violations in the Storybook UI. Every system component ships as a Storybook story with the addon enabled; failing the addon fails PR CI.
- **CSS lint** for forced-colors checks (e.g., flag `outline: none` without paired `:focus-visible` outline replacement) and contrast checks (more reliably done at the token-validation layer per 22).

### The automation ceiling — honest range

Both agents agree automation has a hard ceiling. The cited percentages diverge:

- Claude cites **~25–40%** of WCAG issues as automatically detectable, the figure published in axe-core and Deque marketing material.
- External cites **~57.4%** drawn from broader academic-audit data sets.

The honest range is 25–60% depending on what is counted (criteria covered, severity weighting, type of site under audit) and which study you are reading. The practical conclusion is the same in both cases: **automation catches a meaningful but not majority slice of issues**. Manual testing is mandatory; automation is the floor, not the ceiling. Cite the range, not a single number; tell clients which study a number came from.

### Runtime and CI automation

- **`axe-core` 4.10.x** — the de-facto runtime accessibility engine.
- **Playwright + axe** (`@axe-core/playwright`) — runs axe on rendered pages in CI. The system ships a baseline Playwright a11y suite as a default deliverable.
- **Cypress + axe** (`cypress-axe`) — equivalent for Cypress users.
- **Pa11y** (legacy but maintained) — CLI-driven, useful for static-site monitoring.
- **Component-level tests** — each component renders, runs axe, asserts no violations. The system ships this as a test pattern with helpers that handle theming, RTL, and forced-colors simulation.

### Browser DevTools

- **Chromium DevTools** — full accessibility tree, computed-role panel, ARIA validity warnings, `prefers-color-scheme` and `forced-colors` simulators, focus-order overlay (since Chrome 110, Feb 2023). Most-complete a11y DevTools surface as of 2026.
- **Firefox DevTools** — accessibility inspector with tab order, role / name / state per node, contrast checking, JavaScript event-listener highlighting (invaluable for debugging custom keyboard traps and roving-tabindex implementations) *(external)*.
- **WebKit Safari Web Inspector** — Audit tab includes accessibility checks; less comprehensive than Chromium but catches the major issues. The accessibility node inspector mirrors macOS Accessibility Inspector for native apps.

### The manual test matrix

The minimum reliable matrix per significant component change:

| AT | Engine | Notes |
|---|---|---|
| **NVDA** | Chrome (Windows) | Free, open-source; the developer-test baseline |
| **JAWS** | Chrome (Windows) | Commercial; the procurement-grade AT |
| **VoiceOver** | Safari (macOS) | Built-in; different keyboard model (Control+Option) |
| **VoiceOver** | Safari (iOS) | Mobile gesture-based |
| **TalkBack** | Chrome (Android) | Mobile equivalent of VoiceOver |

Five configurations per component per significant change. For a 60-component system this is unsustainable unless automated regression covers the bulk and manual testing covers a sampled subset per release. The pragmatic pattern:

- **Automated coverage** (axe, Playwright, Storybook) on every PR.
- **Manual matrix** on every minor version (every 2–4 weeks of system evolution).
- **Full audit** on every major version.

Narrator on Edge is secondary to NVDA / JAWS in test priority but worth a periodic check, particularly if the consuming product has Windows-enterprise distribution.

### ACR / VPAT evidence

The Accessibility Conformance Report (using the VPAT format under Section 508 Rev) requires per-criterion evidence. What automation produces:

- **Yes**: structural conformance (every interactive element has a name, every image has alt, every form field has a label), automated contrast measurements, lint and axe-core reports, Storybook addon results, CI pipeline logs.
- **No**: experiential evidence — traversal makes sense, live regions announce in time, error messages are helpful, focus management on dismiss is correct, AT-specific behaviour like JAWS's table mode. For these, **manual AT walkthroughs with video capture and tester sign-off remain the only credible evidence** *(both agents)*.

The system's ACR contribution: every component ships with its test suite and a **conformance dossier** (a Storybook page or markdown file) listing per-criterion automated and manual evidence. The consuming product's ACR aggregates per-component dossiers with application-level dossiers for the integration. Specific operational criteria worth calling out as manual-only:

- **SC 2.1.1 Keyboard.** Operability cannot be fully proved by automation.
- **SC 4.1.3 Status Messages.** Automation verifies the live region exists; manual verifies the announcement.
- **SC 2.4.11 Focus Not Obscured (Minimum, WCAG 2.2 AA).** Verifies sticky headers and overlays do not cover the focused element. Automation does not catch this reliably.

### Continuous monitoring

Production a11y dashboards exist as a procurement-grade requirement for enterprise customers:

- **Siteimprove**, **Level Access** (formerly eSSENTIAL Accessibility), **Deque axe Monitor** — commercial dashboards crawling production sites and reporting issues over time.
- **Real-user a11y telemetry** — newer pattern; instrumenting the design-system components to report (anonymously) when AT events fire, what user preferences are detected. Forward-looking; treat as Phase 2 for systems mature enough to support it.
- **Synthetic monitoring with accessibility checks** — Playwright-based scheduled runs against production. Cheaper and more controlled than real-user monitoring; less data-rich.

The practice's recommendation: the system's first investment is CI (every PR) plus per-release manual auditing. Production monitoring is appropriate when the consuming product is at scale and procurement demands it.

---

## See also

For the architectural treatment of accessibility as a system concern — pair tokens, four-layer model, conformance reporting under EAA / Section 508 — see 14-accessibility.

For mobile implementation depth across Flutter, Jetpack Compose, SwiftUI / UIKit, and React Native, see 16-mobile-accessibility-implementation.

For the per-component annotation contract that designers fill in to close the inference gap, see 17-accessibility-annotation-contract — including its web extension covering ARIA-specific fields, `forced-colors`, `prefers-reduced-motion`, landmark and heading structure, `inert` regions, focus-return targets, and ARIA relationships.

For the documentation architecture that surfaces the annotation contract as machine-readable metadata, see 04-documentation. For the components-as-data substrate that makes the schema possible, see 03-component-library and 15-ai-in-ds.

For motion's interaction with `prefers-reduced-motion` at the foundation layer, see 18-motion-foundations and the implementation depth in 19-motion-implementation-web — including the View Transitions reduce-motion gotcha.

---

## Provenance

Synthesis of the dual-agent research run filed 2026-06-13 (`_research/_inbound/2026-06-13-web-a11y-implementation/`). Both agents converged on the load-bearing architectural claims (build-on-the-element, `:focus-visible`, `inert`, `<dialog>` and the popover API, roving tabindex as default, the `aria-owns` cross-engine gap, automation has a hard ceiling, the manual test matrix is mandatory, the persistent root-level live region, WCAG 2.x as the legal contract). Where they diverged, the synthesis has applied corrections. ARIA 1.3 is dated as working draft (external's framing) rather than Recommendation (Claude overshoot). The `aria-errormessage` per-AT breakdown and the hybrid `aria-describedby`-fallback pattern are external-only. The skip-link `tabindex="-1"` requirement on the target is external-only. The combobox live-region debounce and the `<summary>`-with-`role="button"` anti-pattern are external-only. The decorative / informational / vestibular tripartite for reduced motion, the engine-divergence specifics on accessible-name computation and `<a>`-without-`href` role, the `headingLevel` prop discipline, the `color-scheme` document-root setting, and the View-Transitions reduce-motion gotcha are Claude-only. The library-landscape table draws on both. The automation catch-rate is held as a 25–60% range rather than picking a single figure. Closes 09-gaps-and-open-questions §1.16 and the web-extension gap flagged in 17.

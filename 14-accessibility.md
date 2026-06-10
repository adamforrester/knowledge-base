# 14 — Accessibility in Design Systems

> Accessibility lapses in the design system propagate to every consuming product simultaneously. That asymmetry — one fix in the DS, hundreds of fixes avoided downstream — is the strongest argument for treating accessibility as architecture, not as audit. This file is what that architecture looks like: how we encode accessibility into tokens, components, Figma, documentation, testing, and governance, so that products built from our system are accessible by default, not by retrofit.

---

## Why this is its own file

Accessibility runs through every other file in this vault — it's named in 00-principles as a foundational principle, in 02-design-foundations as a token concern, in 03-component-library as a component concern, in 11-mobile-and-cross-platform as a platform concern, in 13-internationalization-and-rtl as a multi-locale concern, and (for motion-sensitivity specifically) in 18-motion-foundations as the system-level contract that reduce-motion variants encode. **What this file does is consolidate the accessibility-specific architecture in one place** — the patterns we keep re-deriving per engagement, the conventions we keep documenting in slide decks, the failure modes we keep watching for. It is not a WCAG primer. It assumes the reader knows the standards at a working level. The focus is on how accessibility is encoded into the system so consumers can't get it wrong. (For the mobile implementation depth across Flutter, Compose, SwiftUI/UIKit, and React Native, see 16-mobile-accessibility-implementation. For the annotation contract designers fill in so engineers can implement faithfully, see 17-accessibility-annotation-contract.)

The argument for centralizing here, the same argument we made for i18n in 13: **the cost of building accessibility into the system from the first component is a small tax on every author; the cost of retrofitting is a multi-quarter project plus the legal exposure during the gap.** The cost is paid either way. The DS is the only place to pay it once.

---

## Accessibility architecture in a design system

### Accessible-by-default

The architectural goal is to make the accessible choice the *easy* choice — the one a hurried designer or engineer reaches for without thinking. **Anything that requires consumers to opt in to accessibility will produce inconsistent results.** A DS that ships a `Button` with built-in keyboard handling, focus visibility, and ARIA correctness produces accessible buttons across every consuming product. A DS that documents how to make `Button` accessible and leaves consumers to implement it produces accessible buttons in some products and broken buttons in others.

The corollary, and the load-bearing claim of this file: **accessibility lapses in the design system propagate to every consuming product simultaneously.** A focus state that fails contrast in the DS's `IconButton` is a contrast failure in every product. A modal that doesn't trap focus correctly is a broken modal everywhere it's used. This is the strongest architectural argument for treating accessibility as a first-class concern, not an audit activity.

### Where accessibility lives

Accessibility is not one layer; it's distributed across four:

| Layer | Implementation strategy | What it enforces |
|---|---|---|
| Tokens | Semantic color pairs, motion duration scales with reduced-motion variants, focus-indicator tokens, target-size constants | Contrast ratios, motion-sensitivity respect, focus visibility, touch-target sizing — at the atomic level |
| Components | Encapsulated ARIA states, keyboard event listeners, focus management (traps, return-focus), live-region announcements | Composite-widget patterns from APG, modal trapping, roving tabindex, semantic correctness |
| Documentation | Usage guidelines, "avoid-when" patterns, behavioral summaries, conformance declarations | Educates consumers on what they get vs. what they must provide |
| CI / contribution gates | Automated axe-core scans, visual regression, semantic linters, manual-review checklists | Prevents regressions; gates new contributions |

A system that addresses only one or two layers has accessibility ambitions; a system that addresses all four has accessibility architecture.

### Constraint vs. audit — the practical difference

Treated as an audit, accessibility issues surface late — at QA, in user research with assistive-tech users, or after launch from external complaints. Treated as a constraint, issues surface early — at component design, at the first PR, at the moment of writing CSS that hardcodes a hex color instead of a semantic token.

The cost asymmetry is well-known. **A DS that surfaces issues at the constraint layer pays the 10-minute cost; a DS that audits later pays the coordination cost on every issue.** Industry figures vary by source — commonly cited numbers are around 5% added design time when accessibility is built in vs. 15–30% more expensive to fix later (broadly aligned with IBM and Deque published benchmarks; attribute to source in client materials rather than asserting). The broader point is that the gap is large and weighted against retrofit.

There is also the **overlay-industry caution** worth surfacing in client conversations. The "automated overlay" market — third-party scripts that promise compliance via JavaScript injection — is increasingly the target of accessibility lawsuits because the scripts conflict with assistive technologies and don't address underlying structural issues. Clients sometimes ask about overlays; the practice should have a clear position that they're not a substitute for built-in accessibility, and that recommending them creates legal exposure rather than reducing it.

### Regulatory context

The 2025–2026 regulatory environment changes the stakes:

- **WCAG 2.2** is the current stable version of the technical standard. WCAG 3 is in working draft.
- **EAA (European Accessibility Act)** became enforceable on **June 28, 2025**, applying to products and services sold in the EU including most digital consumer-facing products. (Verify against current EU regulatory text before quoting in client materials.)
- **Section 508** (US federal procurement), **EN 301 549** (EU harmonised standard, basis of EAA technical conformance), **ADA Title III** (US private-sector litigation pathway), **AODA** (Ontario), and **Equality Act** (UK) are the principal regulatory frameworks our practice's clients are exposed to.
- For regulated industries (healthcare, finance, government, education) the exposure is more concrete; for consumer products in the EU the EAA has materially raised the floor.

This is the strongest external argument for treating the DS as the right place to absorb accessibility cost. Per-product compliance on a fragmented codebase is brittle and audit-prone; per-system compliance on a DS is auditable, defensible, and uniform.

---

## Token-level accessibility

### Pair tokens for contrast

The most consequential token-layer decision is whether color tokens encode contrast as a property of the **pair** or leave it as a property of the consumer's combination. **Encoding it as a pair is the only architecture that prevents drift.**

The pattern that has stabilized:

```
color/text/on-surface-primary          → 4.5:1 against color/surface/primary
color/text/on-surface-secondary        → 4.5:1 against color/surface/secondary
color/text/on-action-primary           → 4.5:1 against color/action/primary
color/border/on-surface-default        → 3:1 against color/surface/default (UI component contrast)
color/icon/on-surface-default          → 3:1 against color/surface/default
color/text/on-surface-subtle           → 4.5:1 against color/surface/subtle
```

The naming makes the pair explicit (`on-X` reads as "intended to sit on X") and the build pipeline validates the contrast ratio as part of the token build, **failing the build if a token edit drops a pair below the WCAG threshold**. This is the highest-leverage gate the practice can ship: the token system enforces compliance, automatically, at every theme change.

What this prevents: the all-too-common scenario where a designer applies `gray/700` text to `gray/200` background, both of which pass contrast in some pairings, and produces a 3.8:1 result that fails AA for body text. With pair tokens, that combination is unavailable — the picker shows `text/on-surface-secondary`, which resolves to whatever satisfies the contract.

This is particularly load-bearing for systems supporting **dark mode and multi-brand themes** — the pair tokens automatically adjust foreground based on background luminance per mode, ensuring every theme stays accessible without per-theme audit.

The **Adobe Spectrum convention** is the most-cited public example; Polaris (Shopify), Carbon (IBM), and most mature systems have converged on similar pair-based shapes. (See 02-design-foundations on the broader token architecture.)

### Contrast requirements by context

WCAG 2.2 Level AA sets the floor:

| Context | AA | AAA | DS encoding |
|---|---|---|---|
| Body/normal text | 4.5:1 | 7:1 | `text/on-surface/...` semantic tokens |
| Large text (≥18pt or ≥14pt bold) | 3:1 | 4.5:1 | Specialized heading tokens with separate validation |
| UI components, icons, focus indicators | 3:1 | n/a | `border/...`, `icon/...`, `focus/...` tokens |
| Decorative elements, disabled states, brand logos | No requirement | n/a | `decorative/...` tokens, scoped accordingly |
| Enhanced (AAA) text | 7:1 | — | Optional AAA theme variants |

**Most agencies should target WCAG 2.2 AA as the floor** and document any AAA exceptions explicitly. AAA across the board is rarely commercially viable for marketing-led products; it is the right floor for healthcare, government, and accessibility-first products.

The **24×24 minimum target size** requirement (WCAG 2.5.8, new in 2.2) is often overlooked — many existing libraries have icon buttons at 16×16 or 20×20 that fail this floor. **Audit on intake.**

### APCA — the perceptual contrast question

The field has an active debate between WCAG 2.x's mathematical contrast ratio (based on relative luminance) and APCA (Accessible Perceptual Contrast Algorithm), which models how the human visual system actually perceives contrast — particularly for medium-sized text and combinations involving deep blues and reds, which the WCAG 2.x algorithm systematically misjudges.

**Status as of early 2026:** APCA is a candidate for WCAG 3 but WCAG 3 itself is not yet stable. APCA can be used as an internal target and surfaces in tooling (Adobe Leonardo, Stark) but is not yet an accepted compliance standard. We land on the cautious side here because APCA is not yet a procurement-grade standard, even though some practitioner writing is more bullish about its near-term adoption.

The pragmatic stance:

- **Compliance:** continue to target WCAG 2.2 AA. Procurement, legal, and government contracts reference WCAG 2.x. EAA technical conformance maps to EN 301 549, which references WCAG 2.x.
- **Internal practice:** also check against APCA where you have the tooling. Where APCA flags a failure that WCAG 2.2 passes — particularly thin font weights against medium backgrounds — that's a real readability concern worth taking seriously even if not a compliance failure.
- **Public communication:** be explicit. "Targets WCAG 2.2 AA; APCA-validated where supported" is honest. "Beyond WCAG" without qualification reads as marketing.

Verify APCA's standardization status before recommending it as the primary contrast target — its trajectory in WCAG 3 has shifted multiple times and may continue to.

### Color blindness and the limits of contrast

Contrast ratios alone don't surface color-blindness issues. A red error indicator and a green success indicator can both pass contrast individually and still be indistinguishable to a deuteranope. The principle:

- **Never rely on color alone** to convey state, meaning, or required action. Pair color with an icon, a text label, a position, a pattern, or all of the above.
- **Test color-coded UI under simulated color-blindness conditions.** Stark, the Figma plugins, and Chrome DevTools' rendering panel all do this.
- **For data visualization,** color-blind-safe palettes (ColorBrewer, Viridis, Okabe-Ito) are well-established. Don't reinvent.

This same practice helps with cultural color-meaning variation across markets (see 13-internationalization-and-rtl). **Two concerns, one architectural response: status communication is multi-modal.** Color carries the affect; icon + text carry the meaning.

### Motion tokens and reduced motion

`prefers-reduced-motion` is a media query the operating system surfaces based on the user's accessibility settings (vestibular disorders, motion sensitivity). The DS architectural response is to make motion tokens respect it natively:

```
duration/short → 200ms (default), 0ms (reduced-motion)
duration/medium → 400ms (default), 0ms (reduced-motion)
easing/decel → cubic-bezier(0.2, 0, 0.4, 1) (default), step-end (reduced-motion)
```

Animations that can't simply be zeroed (a page transition that conveys spatial relationship) should fall back to an instant or near-instant version, or to a different transition style (cross-fade instead of slide). A parallel concern worth encoding is **calm easing tokens** — easing curves that avoid abrupt starts or stops, less likely to cause discomfort even for users without reduced-motion settings enabled.

**A frequent failure mode:** the DS ships motion tokens that respect reduced-motion at the duration level but components have hardcoded transitions that bypass the tokens. The contract holds only if all motion goes through the token layer. (See also 02-design-foundations on motion as foundation primitive, 18-motion-foundations for the current architectural treatment, 19-motion-implementation-web and 20-motion-implementation-mobile for per-platform spelling.)

**Refinement on the blanket "collapse to 0ms" pattern.** The convergent 2025–2026 position is that reduce-motion is *not* a blanket disable — it is an *informational vs. vestibular* split. Vestibular triggers (large-scale translation, parallax, 3D rotation, scale) should be replaced with a cross-fade. Informational motion (short fades, focus-state transitions, progress indicators) can be preserved unchanged or at reduced amplitude. The DS encodes this as a per-token decision, not a global override. See 18-motion-foundations for the token-layer contract.

**The View Transitions API gotcha (web).** `document.startViewTransition()` does *not* automatically respect `prefers-reduced-motion`. If an engineer calls it, the browser runs the transition regardless of the user's setting — a frequent compliance finding in late-2025 audits. The DS should ship a `safeViewTransition` wrapper that gates on the system setting and route all view-transition calls through it. The full pattern is in 19-motion-implementation-web.

### Focus indicator tokens

WCAG 2.4.11 (Focus Appearance, new in 2.2) sets minimum requirements: minimum size, minimum contrast (3:1) against adjacent colors, and persistence. Encoded as tokens:

```
focus/ring/color → high-contrast color, validated against expected backgrounds
focus/ring/width → 2px minimum (often 3px for clarity)
focus/ring/offset → 2px (separates ring from element edge)
focus/ring/style → solid (not dashed/dotted, which fail at small sizes)
```

The component layer applies these via `:focus-visible` (the modern pattern — only show the ring when keyboard-focused, not on click) with `:focus` as a fallback. **Components must never override focus tokens to hide the ring without providing an equivalent indicator.**

In complex layouts, **intelligent focus rings that change color based on the surface they inhabit** are worth shipping when the design system uses many surface colors. The ring color can be a function of the local surface mode rather than a single global value.

---

## Component-level accessibility

### ARIA: the system absorbs the complexity

The DS's job is to ship components with **correct ARIA built in**, so consumers don't have to think about it. The reference is the W3C ARIA Authoring Practices Guide (APG) — the canonical pattern catalog for composite widgets (combobox, menu, tabs, listbox, dialog, treegrid, etc.). Components that diverge from APG patterns should do so deliberately and document the deviation.

The DS-side discipline:

- **Use semantic HTML first.** A `<button>` is more accessible than a `<div role="button">` and never gets it wrong. Reach for ARIA only when semantic HTML can't express the pattern.
- **Don't double up.** `<button aria-label="Close">×</button>` is correct. `<button role="button">` adds nothing.
- **State, not just role.** Toggleable buttons need `aria-pressed`. Disclosure widgets need `aria-expanded`. Selection patterns need `aria-selected`.
- **Document what the component handles internally vs. what the consumer must provide.** This contract is the most important documentation the component ships.

The system absorbs ARIA complexity and exposes only high-level props to the consumer. A `Tabs` component generates `role="tablist"`, `role="tab"`, and `role="tabpanel"` internally; manages `aria-controls`, `aria-labelledby`, and `aria-selected` state; and exposes a clean React-style API.

To enforce correctness across the library, the DS uses:

- **Semantic linters** that prevent ARIA roles on inappropriate native elements
- **TypeScript interfaces that require labels** when no visible label is provided (a `Button` with no children must accept `aria-label`)
- **Internal state management** for dynamic states like `aria-expanded`, `aria-checked`, `aria-disabled`

### Keyboard navigation patterns

Each composite-widget category has an established keyboard pattern from APG. **Components must implement the pattern fully — partial implementations confuse users more than no implementation does.**

| Component pattern | Required keyboard behavior |
|---|---|
| Button | Enter and Space activate |
| Link | Enter activates |
| Modal/Dialog | Tab cycles within (focus trap), ESC closes, focus returns to trigger on close |
| Drawer | Same as modal when modal-style; otherwise focusable on open |
| Combobox | ArrowDown opens, ArrowUp/Down navigate, Enter selects, ESC closes |
| Listbox | ArrowUp/Down navigate, Home/End jump, Enter/Space select |
| Tabs | ArrowLeft/Right between tabs, roving tabindex (only one tab in tab order) |
| Menu | ArrowDown/Up navigate, ArrowRight/Left for submenus, Enter activates, ESC closes |
| Tree | ArrowRight expands, ArrowLeft collapses, Up/Down navigate, Enter activates |
| Slider | ArrowLeft/Right adjust, Home/End to extremes, PageUp/Down for larger steps |
| Date picker | ArrowKeys navigate calendar, PageUp/Down for month, Shift+PageUp/Down for year |

**The two focus-management strategies for composite widgets:**

| Pattern | Mechanism | Best for | Trade-off |
|---|---|---|---|
| Roving tabindex | Sets `tabindex="-1"` on all children except one (`tabindex="0"`); arrow keys update the tabindex and call `.focus()` | Radio groups, tabs, menus, toolbars | Pro: browser scrolls focused element into view automatically. Con: more DOM manipulation |
| `aria-activedescendant` | DOM focus stays on a container (e.g., text input); the attribute points to the ID of the "virtually focused" child | Comboboxes, autocomplete, search | Pro: simpler focus management for text inputs. Con: developer must manually manage visual highlighting and scrolling |

**Most DS implementations get roving tabindex wrong on first attempt** — they place `tabindex="0"` on every item, breaking page-level tab flow. This is one of the most frequent component-level a11y bugs.

**Document the keyboard pattern in the component's accessibility section,** not just the props. Engineers need to know what the component does so they don't break it via custom event handlers.

### Focus management

Components that change what's on screen must manage focus deliberately:

- **Modal opens** → focus moves into the modal (typically the first interactive element, sometimes the modal itself with `tabindex="-1"` for screen-reader announcement).
- **Modal closes** → focus returns to the element that opened it. The component tracks the opener.
- **Drawer/dropdown opens** → focus moves into the open content; ESC closes; focus returns.
- **Toast/notification appears** → does *not* steal focus. Provide a way to navigate to it (`aria-live` for announcement, a hidden landmark, or a key shortcut). Toast-steals-focus is a frequent failure mode worth naming explicitly in component docs.
- **Page navigation** (SPA route change) → manage focus on the new view's main heading or `<main>` element; announce via `aria-live`.

**The focus-trap mistake.** A modal's focus trap must include all interactive elements *within the modal* and exclude everything else — including the page underneath. Trap implementations that escape the modal break the model.

### Touch target sizing

WCAG 2.2 added 2.5.8 (Target Size — Minimum) at AA: **24×24 CSS pixels** for any pointer target. WCAG 2.5.5 (Target Size — Enhanced) at AAA requires 44×44.

Platform conventions are stricter than the WCAG floor:

- **iOS HIG:** 44×44 pt minimum
- **Material (Android):** 48×48 dp minimum
- **Touch-targeted web:** 44×44 CSS pixels is the safer floor

**The DS encoding pattern:** the visible element stays at the brand-defined size; the touch target is enlarged via padding or transparent borders. Specify these minimums as tokens used in the base component styles.

Auditing existing libraries: small icon buttons (16×16, 20×20) are the most common offenders.

### Form components

Forms concentrate a11y complexity because errors compound:

- **Visible labels.** Always. Placeholders are not labels — they disappear on focus, fail contrast, and screen readers handle them inconsistently.
- **`aria-describedby`** for helper text and error messages. Multiple IDs can be associated; screen readers read them in order after the label.
- **`aria-invalid="true"`** on fields with errors, paired with `aria-describedby` pointing at the error message. Visual error treatment supplements the announcement, doesn't replace it.
- **Required fields.** The HTML `required` attribute communicates required state to assistive tech. Visual indicators (asterisk) supplement it.
- **Error summaries.** For longer forms, an error summary at the top with links to each errored field aids navigation.
- **Inline validation timing.** Validate on blur, not on every keystroke; announce the error after the user has stopped typing. Aggressive validation interrupts users' thinking.
- **Above-the-input labels** translate cleanly across locales (see 13-internationalization-and-rtl); inline labels (label-on-the-left) break with text expansion.
- **Disabled / read-only / error states must be visually and programmatically distinct,** never color-only.

### Interactive state coverage

Every interactive element has states that must be visually distinct *and* accessible:

| State | Trigger | Accessibility requirement |
|---|---|---|
| Default | At rest | Meets contrast for its content |
| Hover | Mouse over | Visible change; never hide critical info behind hover (touch users don't have hover) |
| Focus | Keyboard or programmatic | Visible focus indicator (token-driven) meeting WCAG 2.4.11 |
| Focus-visible | Keyboard focus only | `:focus-visible`, the modern default |
| Active | During click/press | Brief visual feedback |
| Disabled | Not interactive | aria-disabled or disabled attribute (decision below); contrast requirements relaxed but consider readability |
| Error | Invalid input | Visual + ARIA announcement (aria-invalid + aria-describedby) |

**The disabled vs. aria-disabled decision.** The HTML `disabled` attribute removes the element from the tab order and prevents interaction — but assistive tech often skips disabled elements entirely, so users may not understand why the action is unavailable. `aria-disabled` keeps the element focusable and announceable but requires the component to handle the click and explain why nothing happened. Most modern accessibility-led patterns prefer `aria-disabled` paired with a tooltip or message explaining the reason. Both are defensible; **document which the component uses and why.**

---

## Accessibility in Figma

### What Figma can validate at design time

- **Color contrast.** Stark, Contrast, Able plugins compute WCAG ratios for selected pairings. Some scan an entire page.
- **Color-blindness simulation.** Stark and built-in plugins simulate the major types.
- **Type sizes and hierarchy.** Visible at design — too-small text, missing heading hierarchy, undifferentiated styles surface in review.
- **Touch target sizing.** Measurable; flag undersized targets at design review.
- **Visual focus indicators.** Designable; validate contrast and sizing.
- **Initial reading order.** Catchable with annotation tools, before code.
- **200% text reflow simulation** via Text Resizer plugin. Useful for catching layout fragility under user font scaling, with the caveat that browser reflow logic differs.

### What Figma cannot validate

- **Keyboard navigation flow.** Until the design is in code, keyboard order, focus traps, and roving tabindex behavior can't be exercised.
- **Screen reader output.** What a screen reader actually announces depends on HTML/ARIA implementation and screen reader behavior. Can't be predicted from a Figma file.
- **Live region announcements** (toast notifications, form validation messages). Behavior, not appearance.
- **Cognitive accessibility** at the interaction level — working memory load, error recovery, language clarity.
- **Touch-drag gestures.**

### Annotation practices

Figma's native annotations have improved through 2024–2025 and are the right surface for design-time accessibility documentation:

- **ARIA roles and labels.** Annotate composite widgets with their role (`tablist`, `combobox`, `dialog`) so engineers know which APG pattern to implement.
- **Reading order.** Numbered annotations indicate intended DOM/tab order. This often differs from visual order.
- **Focus behavior.** What gets focus when the component opens? Where does focus return on close?
- **Alt text and aria-labels.** Documented per image and per icon-only button. Distinguish decorative (`alt=""`) from informative.
- **Form label and error linking.** Which text is the label, helper, error.

The **Microsoft A11y Annotation Kit** is a well-developed Figma library of annotation components covering most of these concerns; many teams use it as a starting point and adapt.

### Plugins worth knowing

| Plugin | Utility | Known gaps |
|---|---|---|
| Stark | Contrast (WCAG and APCA), color-blindness simulation, focus order | Automated checks miss complex contrast scenarios (text over gradients) |
| Able | Real-time contrast checking between selected layers | Doesn't fully account for font-weight in APCA |
| Contrast | Lightweight contrast checker | Basic; no APCA |
| A11y Annotation Kit (Microsoft) | Standardized annotation components | Annotations are visual; don't sync to code automatically |
| Text Resizer | Simulates 200% text scaling | Can't simulate real browser reflow logic perfectly |

These are useful for what they validate but their utility decays past contrast and annotation. Focus order, keyboard flow, and screen reader output remain code-level concerns; the plugins simulate but don't validate.

### Handoff requirements

For each component shipped, the design spec must include:

1. **Role** (semantic HTML element or ARIA role)
2. **Label** (what the screen reader announces)
3. **States and visual treatments** (default, hover, focus, focus-visible, active, disabled, error, loading)
4. **Keyboard behavior** (which keys do what)
5. **Focus behavior** (what gets focus on open/activation; where focus goes on close)
6. **Live region behavior** (what gets announced asynchronously)
7. **Alt text or aria-label conventions**
8. **Reading order** (if visual order differs from DOM order)

**Components that don't ship with this in their spec are incomplete handoffs.** Treat these as definition-of-done, not nice-to-have. (See 12-figma-practice on component handoff structure generally.)

---

## Documentation and consumer guidance

### What consumers need to know

The accessibility documentation a consumer needs is different from what a component author needs. **Consumers need to know what they can rely on the component to handle and what they must do themselves.** That two-part declaration is the load-bearing piece.

Per-component, the docs should cover:

- **Behavioral summary.** Plain-language description of how the component behaves for assistive technology. "This is a tabbed interface where arrow keys move focus between tabs and Enter activates content."
- **What the component handles.** Explicit list: keyboard, focus, ARIA, contrast for built-in states, touch target sizing.
- **What the consumer must provide.** Explicit list: meaningful labels for icon-only buttons, alt text for images, descriptive error messages, sensible disabled states with explanation.
- **Keyboard map.** Table of every key the component supports and its function.
- **ARIA spec.** All roles, states, properties used internally.
- **When to use it / when not to use it.** Use-case framing.
- **Avoid-when patterns.** Specific misuse to flag.
- **Conformance level.** "WCAG 2.2 AA conformant when used as documented."

The **three audiences** (designers, developers, QA engineers) each need a different cut of this information; the documentation should be navigable per-audience without forcing one to read the others.

### Encoding accessible patterns in usage guidance

The usage section is where the DS prevents the most common misuse patterns. A few examples:

- **Modal vs. drawer vs. inline.** "Use a modal when the user must take action before continuing. Use a drawer for secondary content that complements the page. Use inline expansion when the content is part of the page's reading flow." Prevents modal abuse for non-critical content.
- **Toast vs. inline message.** "Use a toast for transient confirmation. Use an inline message for persistent feedback the user needs to read. Don't use a toast for errors the user must address." Prevents toast misuse for critical messages.
- **Tooltip vs. helper text.** "Do not use a Tooltip for essential information, as it is not consistently accessible to touch or screen reader users. Use Helper Text instead."
- **MenuButton vs. Combobox vs. Select.** "Use a MenuButton when the user is triggering an action. Use a Select or Combobox when they are choosing a value from a list."

These distinctions are accessibility decisions even when not framed as such. A toast that the user dismisses before reading is an accessibility failure as much as a UX one.

### Common misuse patterns to call out

Patterns that consistently produce a11y failures and benefit from being flagged in docs:

- **`<div onClick={...}>` instead of `<button>`.** No keyboard. No semantics. The DS ships a `Button` and documents "if you need a button, use Button — never an onClick on a div."
- **Placeholder as label.** Disappears on focus, fails contrast, screen reader inconsistency.
- **Color-only state communication.** Red border without an error icon or message; green checkmark without text.
- **Missing focus indicator.** `outline: none` without a replacement.
- **Modal without focus trap.** Focus escapes to the page beneath.
- **Form errors that aren't announced.** Visual error styling without `aria-invalid` and `aria-describedby`.
- **`aria-hidden` on focusable elements.** Hides from screen readers; element still focusable; user gets focus on something they can't perceive.
- **Heading hierarchy skipped.** `<h1>` then `<h3>`. Confuses screen reader navigation.
- **Live region noise.** `aria-live="assertive"` for non-critical updates floods screen reader users with announcements.

Documentation that names these patterns prevents them better than documentation that explains general principles.

### Conformance levels in documentation

A DS should be explicit about its accessibility commitment, per-component:

- **Out-of-the-box (OOTB) conformance.** "This component meets WCAG 2.2 AA standards for keyboard and screen reader support when used as documented."
- **Consumer responsibility.** "To reach AAA conformance, the consumer must ensure text is not placed over background images and supplements color-only indicators with icons."
- **Limitations.** Components that don't fully meet the standard (a complex data table that needs additional implementation work) declare what they meet and what consumers must complete.

The system-level commitment sits in the **Accessibility Conformance Report (ACR)**, the public artifact based on the **VPAT (Voluntary Product Accessibility Template)**. This ACR communicates to internal and external stakeholders exactly which version of WCAG the system adheres to, the level, and which components have known limitations. **Procurement and legal teams reference this; it must be findable.**

---

## Testing accessibility

### Automated testing in CI

Automated tools (axe-core is the dominant engine) catch a real subset of issues but never the whole picture. **Published figures vary by source and methodology — commonly cited numbers fall in the 30–60% range for the share of WCAG issues machine-detectable.** Cite Deque or WebAIM directly in client materials rather than asserting a specific percentage; the broader point is that automation is necessary, not sufficient.

What automation catches reliably:

- Missing or empty labels on form fields and buttons
- Insufficient color contrast (computable from CSS)
- Missing alt text on images
- ARIA misuse (invalid roles, invalid attributes, role/attribute mismatches)
- Heading hierarchy violations
- Duplicate IDs
- Missing language declarations
- Some keyboard-trap detection

What automation can't catch:

- **Whether labels are meaningful.** "Click here" passes; "Submit application" passes; only the second is useful.
- **Whether focus order makes sense.** Order is detectable; sense is not.
- **Whether keyboard navigation is logical.** The DOM tab order can be valid but the experience can be unusable.
- **Screen reader behavior.** What gets announced, in what order, with what intonation.
- **Cognitive accessibility.** Plain language, error message clarity, working memory load.
- **Whether disabled states are explained.** Automation detects `aria-disabled`; it can't tell if the user knows why.

The toolchain that's stabilized:

- **axe-core** in unit and integration tests — the engine.
- **Storybook a11y addon** — real-time dashboard surfacing violations during development.
- **Playwright accessibility / Cypress axe** — E2E coverage; can validate focus traps and keyboard navigation by simulating keystrokes and checking `document.activeElement`.
- **Pa11y** — CI-friendly headless tool.
- **Build-time token contrast validation** — fails the build if pair tokens drop below WCAG threshold. At portfolio scale, validation runs across the full brand × theme × density matrix; the discipline is to **block on WCAG failures and warn on APCA failures** (regulatory floor + perceptually-correct readability signal). See 24-tokens-at-scale for the validation operations layer.

(See 05-development-support on the broader CI architecture.)

### Manual testing requirements

The manual layer is non-negotiable. Per component, the minimum:

- **Keyboard-only navigation.** Tab through. Can every interactive element be reached? Is the order logical? Do focus indicators show? Does ESC close what should close?
- **Screen reader walkthrough.** Run with a screen reader. What gets announced? Is the announcement useful? Are state changes announced?
- **Reduced motion / high contrast.** Toggle the OS settings. Does the component respect them?
- **Touch.** On a touch device, are targets large enough? Do interactions work without hover?
- **Zoom to 200% and 400%.** Does layout reflow? Does anything become inaccessible?

These take 5–15 minutes per component. Significant in aggregate; one-time cost for stable components plus regression on changes.

### Screen reader testing matrix

The screen-reader landscape is fragmented; testing all of them is not realistic. The pragmatic minimum:

| Platform | Screen reader | Browser | When to test |
|---|---|---|---|
| Windows | NVDA | Firefox or Chrome | During component development; major releases |
| Windows | JAWS | Chrome or Edge | Final release validation for enterprise/government clients |
| macOS | VoiceOver | Safari | During design prototyping and component development |
| iOS / Android | VoiceOver / TalkBack | Safari / Chrome | Mobile-specific component variants and touch targets |

For a typical agency engagement, **NVDA + VoiceOver is the floor;** add JAWS for regulated industries; add TalkBack for mobile-heavy products. Different screen readers behave differently with the same ARIA — components that work in NVDA can fail in JAWS, particularly for newer ARIA patterns.

### Real-user testing

The hardest to operationalize, the highest signal: **testing with actual assistive-tech users.** Synthetic personas miss real friction. Worth budgeting for at major releases for regulated-industry clients, and at least once per engagement for any DS that's claiming serious accessibility commitment.

### Accessibility as a contribution gate

For new components proposed via the contribution workflow (see 07-governance-and-adoption), accessibility should be a non-bypassable review gate:

1. **Automated checks must pass.** axe-core, contrast checks, build-time validations.
2. **Manual checklist signed off.** Keyboard, focus, screen reader, reduced-motion, touch, zoom.
3. **Documentation declares conformance.** Per-component statement of what's handled and what consumers must do.
4. **APG conformance noted** for components that match a documented APG pattern; deviations called out and justified.

Components that fail any of these don't merge. **This sounds harsh; in practice it's the only way to maintain accessibility consistency at scale.**

---

## Accessibility governance

### The accessibility promise

The DS's accessibility promise is the contract clients and consumers rely on. It must be specific:

- **Standard and version:** "WCAG 2.2 Level AA"
- **Scope:** "All components, in their documented use, on web platforms. Native iOS and Android components target their respective platform accessibility guidelines (iOS HIG, Material). Multi-locale considerations covered separately (see 13-internationalization-and-rtl)."
- **Tested platforms:** "Latest two major versions of Chrome, Firefox, Safari, Edge. Screen readers: NVDA + Firefox/Chrome, VoiceOver + Safari, TalkBack + Chrome."
- **Out of scope:** What the DS doesn't promise — usually consumer-supplied content, custom modifications, third-party integrations.

This statement lives prominently in the DS documentation, not buried. **Procurement and legal teams need to find it.**

The **ACR / VPAT** is the public, formal version of this promise. Publishing it raises the bar; not publishing it is increasingly read as a signal that the system isn't sure of its own conformance.

### Accessibility debt

Existing component libraries carry accessibility debt — components built before the team had accessibility expertise, components with deferred fixes, components whose patterns weren't audited. **Prioritization matrix:**

| Priority | Criteria | Example |
|---|---|---|
| Critical | Blocks a user from completing a core task | A "Purchase" button that's not keyboard-accessible |
| High | Makes a task difficult or creates significant confusion | A modal that doesn't trap focus; missing error labels |
| Medium | Minor technical violation with limited impact on usability | A decorative icon not properly hidden from screen readers |
| Low | Enhancements for AAA compliance or best practices | Adding higher contrast ratios than the 4.5:1 minimum |

The remediation pattern:

1. **Audit and catalog.** Each component gets a current-state assessment.
2. **Prioritize by usage × severity.** High-usage components with critical issues first.
3. **Fix incrementally.** Each release includes a few component-level fixes. Don't try to fix everything in one heroic effort.
4. **Document the debt visibly.** A "known issues" page in the DS docs is honest and useful.
5. **Deprecate-and-replace** when the component's architecture is fundamentally inaccessible.

Treat this debt as **quality debt with legal and financial risk attached** — particularly under EAA and Section 508 enforcement. (See 08-ongoing-maintenance on debt management generally.)

### Non-accessible designs and deviation

Clients sometimes request designs that are inaccessible — a brand color combination that fails contrast, a custom interaction pattern that breaks keyboard navigation, a graphic-heavy hero with no alt-text equivalent. The practice for handling this:

- **Push back first.** The accessible alternative is usually achievable within the brand and the design intent. Most failures are preventable; the request often comes from the brand team without awareness of the cost.
- **Show the safe alternative.** Mock up the accessible version using the DS tokens and components.
- **If the client insists, document the deviation.** A formal **Risk Assessment** template or **architecture decision record (ADR)** capturing the request, the specific WCAG criteria violated, the accessibility cost, the legal/regulatory risk, and the named decision-maker.
- **Quantify the regulatory risk.** Section 508, EAA, ADA Title III, AODA, Equality Act — varying enforcement, varying penalties. For regulated industries the risk is concrete and current.
- **Limit scope.** A non-accessible design choice should be limited to a specific surface, not propagated through the system. The DS's tokens and components remain conformant; the deviation is in the consuming product.
- **Set a remediation horizon.** Most accessibility deviations should have a stated end date. Deviations that become permanent are technical debt that compounds.
- **Formal sign-off.** The named client stakeholder signs off on the risk in writing.

**The practice should never quietly ship a non-accessible design without the documentation trail.** The legal exposure for the client and the reputational exposure for the agency both compound when the deviation is undocumented.

---

## Failure modes

- **Accessibility documented but not enforced.** The DS describes how to make components accessible; consumers don't read it; products ship with the predictable failures.
- **Pair tokens not validated at build.** Contrast pairs are defined but the build doesn't fail when a theme update violates them. Drift accumulates silently.
- **Focus indicators stripped.** Designers remove the default outline for aesthetic reasons; components don't restore it via tokens. Keyboard users can't see where they are.
- **Modal focus trap broken.** Focus escapes to the page beneath. The modal isn't really modal.
- **Roving tabindex implemented as `tabindex="0"` everywhere.** Composite widgets break page-level tab flow. Common bug.
- **Disabled vs aria-disabled inconsistent.** Different components in the same library use different patterns. Users can't predict behavior.
- **Color-only state communication.** Red border without an icon; green checkmark without text. Fails for color-blind and culturally-variant interpretation alike.
- **APCA confidently asserted as a compliance standard.** It isn't yet. Public claims of "WCAG 3 / APCA conformant" mislead clients.
- **Toast used for critical errors.** Users dismiss before reading; the error never registers.
- **Tooltip used for required information.** Touch users and screen reader users inconsistent access.
- **Placeholder used as label.** Disappears on focus, fails contrast.
- **Heading hierarchy skipped.** `<h1>` then `<h3>`; screen reader navigation broken.
- **Aggressive `aria-live="assertive"` regions.** Floods screen-reader users with non-critical announcements.
- **Component ships without an accessibility section in docs.** Consumers don't know what's handled vs. what they must provide.
- **Automated checks run; manual testing skipped.** The gap between what automation catches and what users hit is what ships to production.
- **No screen reader testing in CI process.** Issues that automation can't catch reach users.
- **EAA / Section 508 requirements not quantified to clients.** Legal exposure not surfaced in scope conversations; client surprised when audit comes.
- **Overlay recommended as a "fix" for inaccessible legacy UI.** Creates legal exposure rather than reducing it.
- **Accessibility deviation shipped without documentation trail.** Agency carries the exposure unnecessarily.
- **No ACR / VPAT published.** Procurement and legal can't find the conformance commitment.

---

## Tensions and open questions

1. **APCA vs. WCAG 2.x — when do we move?** APCA is more perceptually accurate but not yet a compliance standard. The pragmatic stance is "WCAG 2.2 AA for compliance, APCA where tooling supports" — but as APCA stabilizes in WCAG 3 (timeline uncertain), our public stance and our pitch decks need to evolve. Worth tracking; not yet worth re-positioning around.

2. **AI as accessibility gate vs. advisory.** AI can run a first-pass accessibility review on PRs reliably. The decision is whether AI-flagged issues block merge or surface to the human reviewer. As models improve, the balance shifts; today the balance favors advisory. (See 15-ai-in-ds on the broader gate-vs-advisory question.)

3. **The "10% the consumer must do" question.** Per-component conformance docs say what the system handles and what the consumer must complete. How aggressively do we ship those docs vs. expect consumers to figure it out? Heavy docs cost authoring time but reduce misuse; light docs ship faster but accept misuse. We don't currently have a default policy.

4. **Cognitive accessibility.** Plain language, error message clarity, working memory load, attention. Currently under-articulated in most DS practice — including ours. Worth a POV piece. WCAG 2.2 added 2.4.11 and 2.5.8 but cognitive accessibility remains the dimension where compliance standards lag actual user need.

5. **Real-user testing with assistive-tech users.** Highest signal, hardest to operationalize. Should be a budgeted line item for engagements with significant a11y commitments, but currently isn't on most scoping templates. Worth building into our default scope for regulated-industry work.

6. **Cultural and linguistic accessibility.** Color connotations, language plain-ness across translations, RTL accessibility patterns. The intersection of accessibility and i18n (see 13-internationalization-and-rtl) is currently fragmented across both files in our practice; some clients will benefit from a unified accessibility-and-i18n review.

7. **The bidi-icon catalog and component-level accessibility metadata as IP.** A curated, opinionated list of which icons mirror, which don't, which need RTL variants — paired with accessibility metadata per component (APG pattern, keyboard contract, focus behavior) — is concrete, useful, defensible practice IP. We don't currently maintain it. High-leverage internal investment.

8. **Selling the accessibility floor.** EAA enforcement raises the regulatory floor for EU-facing products. Procurement increasingly references VPAT/ACR. The practice should default to "always raise accessibility in Discovery; always quantify the regulatory exposure" — but consistency on this varies by lead designer.

9. **AI-pattern accessibility is a separate conformance surface.** Conversational UI introduces accessibility concerns the rest of the system does not — `role="log"` on chat transcripts (Twilio Paste's `AIChatLog`), live-region announcement of streamed assistant messages, focus management when a tool-call approval prompt appears mid-stream, the VoiceOver/TalkBack experience of typewriter rendering, the "no input accepted while loading" rule that prevents sending into an unfinished response. Most published AI patterns are accessibility-light; the conformance work is consumer-side. (See 25-ai-aware-patterns-and-conversational-ui.)

10. **Adaptive UI is the strongest evidence base for accessibility *and* the weakest verification surface — at the same time.** The Gajos / Wobbrock ability-based-design lineage (CHI 2008; TACCESS 2011; CACM 2018) is the single most rigorous evidence base in adaptive-interface research — motor-impaired users completed tasks faster, made fewer errors, and *preferred* the adapted UI. But automated tooling catches only 25–40% of WCAG violations on a fixed surface, and 95.9% of the static top-million home pages still fail the bar (WebAIM 2026). When the surface itself varies per render, in-pipeline DOM scanning inherits the automation ceiling — it catches the floor, not the bar. The strategic implication: scope ongoing manual a11y testing with assistive technology as a standing cost of any generative-UI engagement; do not let a green CI check stand in for an accessibility guarantee. (See 26-adaptive-interfaces-foundations §4.1 for the evidence base, 27-adaptive-interfaces-implementation §6.2 for the verification gap.)

---

*Provenance: The W3C ARIA Authoring Practices Guide (w3.org/WAI/ARIA/apg) is the canonical reference for composite-widget keyboard patterns; component compliance is measured against APG. WCAG 2.2 (w3.org/TR/WCAG22) is the current stable standard; specific criteria cited (2.4.11 Focus Appearance, 2.5.5 and 2.5.8 Target Size) are the load-bearing additions in 2.2 most relevant to DS work. The pair-tokens contrast architecture is consistent with Adobe Spectrum's published model and parallel work in Polaris (Shopify) and Carbon (IBM). APCA and its candidacy for WCAG 3 are documented at github.com/Myndex/SAPC-APCA; WCAG 3 itself remains in working draft as of early 2026. The Accessibility Conformance Report (ACR) and VPAT are formal public artifacts established in Section 508 procurement context (section508.gov). The European Accessibility Act became enforceable June 28, 2025; verify against current EU regulatory sources before quoting specifics in client materials. The four-layer architectural decomposition (tokens / components / docs / contribution-gate), the avoid-when patterns (Tooltip for essential info, MenuButton vs. Combobox vs. Select, Toast vs. inline message), the screen-reader testing matrix (NVDA + Firefox/Chrome, VoiceOver + Safari, TalkBack + Chrome, JAWS for regulated industries), the focus-management responsibilities (trap, initial, return), and the deprecation pattern for accessibility debt are convergent practitioner consensus reflected across current writing from Deque, WebAIM, Heydon Pickering's *Inclusive Components*, Adrian Roselli's accessibility writing, Adobe Spectrum's accessibility documentation, and similar references. Industry figures (axe-core machine-detectable share, retrofit cost multiples, EAA scope) should be attributed to source (Deque, IBM, WebAIM) rather than asserted as practice POV. The disabled-vs-aria-disabled debate, toast-doesn't-steal-focus pattern, SPA route-change focus management, form-error-summary pattern, and cultural-color / accessibility tie-in are positions sharpened from internal practice work and connect to 13-internationalization-and-rtl. axe-core (deque.com), the Storybook a11y addon, Playwright accessibility testing, and Pa11y are the dominant CI-side tools; Stark, Able, Contrast, Microsoft A11y Annotation Kit, and Text Resizer are the well-known Figma design-time plugins; specific feature sets evolve. This file was synthesized from a dual-agent research run in May 2026 (see `_research/_archive/2026-05-05-accessibility.md` for the editorial trail).*

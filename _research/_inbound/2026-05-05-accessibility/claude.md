# Accessibility in Design Systems

A practitioner's reference for senior design systems engineers and designers. Covers how accessibility is encoded into a design system architecture — at the token layer, the component layer, in Figma, in documentation, in testing, and in governance — so that products built from the system are accessible by default rather than audited into compliance after the fact. Assumes fluency with WCAG and ARIA at a working level; focuses on the architectural translation, the trade-offs, and the gaps as of January 2026.

---

## 1. Accessibility architecture in a design system

### Accessible-by-default as the goal

The architectural goal is to make the accessible choice the *easy* choice — the one that a hurried designer or engineer reaches for without thinking. **Anything that requires consumers to opt in to accessibility will produce inconsistent results.** A DS that ships a `Button` component with built-in keyboard handling, focus visibility, and ARIA correctness produces accessible buttons across every consuming product. A DS that documents how to make `Button` accessible and leaves consumers to implement it produces accessible buttons in some products and broken buttons in others.

The corollary: **accessibility lapses in the design system propagate to every consuming product simultaneously.** A focus state that fails contrast in the DS's `IconButton` is a contrast failure in every product. This is the strongest argument for treating accessibility as a first-class architectural concern, not an audit activity.

### Where accessibility lives

Accessibility is not one layer; it's distributed across four:

1. **Tokens.** Color contrast pairs, motion tokens that respect `prefers-reduced-motion`, focus indicator tokens with sufficient contrast, touch-target sizing tokens. The token layer enforces choices that would otherwise be ad-hoc.
2. **Component behavior.** Keyboard handling, focus management, ARIA roles and states, screen reader announcements. Built into the component implementation, not delegated to consumers.
3. **Documentation.** What the component handles, what the consumer must provide, when to use it, when not to, common misuse patterns. The bridge between system and consumer.
4. **Contribution gates.** Automated checks in CI, manual review criteria for new components, accessibility sign-off in PR templates. The mechanism that prevents regressions.

A system that addresses only one or two of these has accessibility ambitions; a system that addresses all four has accessibility architecture.

### Constraint vs. audit

The practical difference is when issues surface. Treated as an audit, accessibility issues surface late — at QA, in user research with assistive-tech users, or after launch from external complaints. Treated as a constraint, issues surface early — at component design, at the first PR, at the moment of writing CSS that hardcodes a hex color instead of a semantic token.

The cost asymmetry is well-known: an accessibility issue caught at component design is a 10-minute fix; the same issue caught after launch is a multi-team coordination across content, engineering, design, and possibly legal. **A DS that surfaces issues at the constraint layer pays the 10-minute cost; a DS that audits later pays the coordination cost on every issue.**

This is the same architectural argument that applies to i18n (see 13-internationalization-and-rtl) and to performance budgets — building it in is cheap and uniform; retrofitting is expensive and uneven.

---

## 2. Token-level accessibility

### Contrast in a semantic color architecture

The most consequential token-layer decision is whether color tokens encode contrast as a property of the pair or leave it as a property of the consumer's combination. **Encoding it as a pair is the only architecture that prevents drift.**

The pattern that has stabilized:

```
color/text/on-surface-primary          → 4.5:1 against color/surface/primary
color/text/on-surface-secondary        → 4.5:1 against color/surface/secondary
color/text/on-action-primary           → 4.5:1 against color/action/primary
color/border/on-surface-default        → 3:1 against color/surface/default (UI component contrast)
color/icon/on-surface-default          → 3:1 against color/surface/default
```

The naming makes the pair explicit (`on-X` reads as "intended to sit on X") and the build pipeline can validate the contrast ratio as part of the token build, failing the build if a token edit drops a pair below WCAG threshold. **Adobe Spectrum's pattern of foreground-on-background contrast tokens is the most-cited example;** other systems (Polaris, Carbon) have converged on similar shapes.

What this prevents: the all-too-common scenario where a designer applies `gray/700` text to `gray/200` background, both of which pass contrast in some pairings, and produces a 3.8:1 result that fails AA for body text. With pair tokens, that combination is unavailable — the picker shows `text/on-surface-secondary`, which resolves to whatever satisfies the contract.

### Contrast requirements by context

WCAG 2.2 (the current stable version as of early 2026) sets the floor:

| Context | AA | AAA |
|---|---|---|
| Body text (normal) | 4.5:1 | 7:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 | 4.5:1 |
| UI components and graphical objects | 3:1 (2.4.11 Focus Appearance, 1.4.11 Non-text Contrast) | n/a |
| Decorative content, disabled states, brand logos | No requirement | n/a |
| Focus indicator vs. adjacent colors | 3:1 minimum (WCAG 2.4.11) | n/a |

**Most agencies should target WCAG 2.2 AA as the floor and document any AAA exceptions explicitly.** AAA across the board is rarely commercially viable for marketing-led products; it is the right floor for healthcare, government, and accessibility-first products.

The 24×24 minimum target size requirement (WCAG 2.5.8, new in 2.2) is often overlooked — many existing component libraries have icon buttons at 16×16 or 20×20 that fail this floor. Audit on intake.

### APCA — the perceptual contrast question

The field has an active debate between WCAG 2.x's mathematical contrast ratio (based on relative luminance) and APCA (Accessible Perceptual Contrast Algorithm), which models how the human visual system actually perceives contrast. APCA more accurately predicts readability — particularly for medium-sized text and for combinations involving deep blues and reds, which the WCAG 2.x algorithm systematically misjudges.

**Status as of early 2026:** APCA is a candidate for WCAG 3 but WCAG 3 itself is not yet stable. APCA can be used as an internal target and surfaces in some tooling (notably Adobe's Leonardo, Stark plugin) but is not yet an accepted compliance standard. The pragmatic stance:

- **Compliance:** continue to target WCAG 2.2 AA. Procurement, legal, and government contracts reference WCAG 2.x.
- **Internal practice:** also check against APCA where you have the tooling. Where APCA flags a failure that WCAG 2.2 passes, that's a real readability concern worth taking seriously even if not a compliance failure.
- **Public communication:** be explicit. "Targets WCAG 2.2 AA; APCA-validated where supported" is honest. "Beyond WCAG" without qualification reads as marketing.

Verify APCA's standardization status before recommending it as the primary contrast target — its trajectory in WCAG 3 has shifted multiple times and may continue to.

### Color blindness and the limits of contrast

Contrast ratios alone don't surface color-blindness issues. A red error indicator and green success indicator can both pass contrast individually and still be indistinguishable to a deuteranope. The principle:

- **Never rely on color alone** to convey state, meaning, or required action. Pair color with an icon, a text label, a position, a pattern, or all of the above.
- **Test color-coded UI under simulated color-blindness conditions.** Stark, the Figma color-blindness plugins, and Chrome DevTools' rendering panel (Vision Deficiencies emulation) all do this.
- **For data visualization,** color-blind-safe palettes (ColorBrewer, Viridis, Okabe-Ito) are well-established. Don't reinvent.

This same practice helps with cultural color-meaning variation across markets (see 13-internationalization-and-rtl). Two concerns, one architectural response: status communication is multi-modal.

### Motion tokens and reduced motion

`prefers-reduced-motion` is a media query the operating system surfaces based on the user's accessibility settings (vestibular disorders, motion sensitivity). The DS architectural response is to make motion tokens respect it natively:

```
duration/short → 200ms (default), 0ms (reduced-motion)
duration/medium → 400ms (default), 0ms (reduced-motion)
easing/decel → cubic-bezier(0.2, 0, 0.4, 1) (default), step-end (reduced-motion)
```

Animations that can't simply be zeroed (e.g., a page transition that conveys spatial relationship) should fall back to an instant or near-instant version, or to a different transition style (cross-fade instead of slide).

**A frequent failure mode:** the DS ships motion tokens that respect reduced-motion at the duration level but components have hardcoded transitions that bypass the tokens. The contract holds only if all motion goes through the token layer.

### Focus indicator tokens

WCAG 2.4.11 (Focus Appearance, new in 2.2) sets minimum requirements for visible focus indicators: minimum size, minimum contrast against adjacent colors (3:1), and persistence. Encoded as tokens:

```
focus/ring/color → high-contrast color, validated against expected backgrounds
focus/ring/width → 2px minimum (often 3px for clarity)
focus/ring/offset → 2px (separates ring from element edge)
focus/ring/style → solid (not dashed/dotted, which fail at small sizes)
```

The component layer applies these via `:focus-visible` (the modern pattern — only show the ring when keyboard-focused, not on click) with `:focus` as a fallback. Components must never override focus tokens to hide the ring without providing an equivalent indicator.

---

## 3. Component-level accessibility

### ARIA: roles, states, properties

The DS's job is to ship components with **correct ARIA built in**, so consumers don't have to think about it. The reference is the W3C ARIA Authoring Practices Guide (APG) — the canonical pattern catalog for composite widgets (combobox, menu, tabs, listbox, dialog, treegrid, etc.). Components that diverge from APG patterns should do so deliberately and documented.

The DS-side discipline:

- **Use semantic HTML first.** A `<button>` is more accessible than a `<div role="button">` and never gets it wrong. Reach for ARIA only when semantic HTML can't express the pattern.
- **Don't double-up.** `<button aria-label="Close">×</button>` is correct. `<button role="button">` adds nothing and reads as carelessness.
- **State, not just role.** Toggleable buttons need `aria-pressed`. Disclosure widgets need `aria-expanded`. Selection patterns need `aria-selected`. The role tells the screen reader *what* the element is; the state tells it *how* it currently behaves.
- **Document what the component handles.** The component's docs declare which ARIA attributes it sets internally and which the consumer must provide (e.g., `aria-label` for icon-only buttons).

### Keyboard navigation patterns

Each composite-widget category has an established keyboard pattern from APG. Components must implement the pattern fully — partial implementations confuse users more than no implementation does.

| Component pattern | Required keyboard behavior |
|---|---|
| Button | Enter and Space activate |
| Link | Enter activates |
| Modal/Dialog | Tab cycles within (focus trap), ESC closes, focus returns to trigger on close |
| Drawer | Same as modal when modal-style; otherwise focusable on open |
| Combobox | ArrowDown opens, ArrowUp/ArrowDown navigate, Enter selects, ESC closes |
| Listbox | ArrowUp/ArrowDown navigate, Home/End jump, Enter/Space select |
| Tabs | ArrowLeft/Right between tabs, roving tabindex (only one tab in tab order) |
| Menu | ArrowDown/Up navigate, ArrowRight/Left for submenus, Enter activates, ESC closes |
| Tree | ArrowRight expands, ArrowLeft collapses, Up/Down navigate, Enter activates |
| Slider | ArrowLeft/Right adjust, Home/End to extremes, PageUp/PageDown for larger steps |
| Date picker | ArrowKeys navigate calendar, PageUp/Down for month, Shift+PageUp/Down for year |

**Roving tabindex** (the pattern used by tabs, menus, toolbars) puts only one element of a composite in the tab order at a time and uses arrow keys to move within the composite. Most DS implementations get this wrong on first attempt — the component places `tabindex="0"` on every item, breaking page-level tab flow. This is one of the most frequent component-level a11y bugs.

**Document the keyboard pattern in the component's accessibility section,** not just the props. Engineers need to know what the component does so they don't break it via custom event handlers.

### Focus management

Components that change what's on screen must manage focus deliberately:

- **Modal opens** → focus moves into the modal (typically the first interactive element, sometimes the modal itself with `tabindex="-1"` for screen-reader announcement).
- **Modal closes** → focus returns to the element that opened it. Restoring this requires the component to track the opener; most modern modal components do this automatically.
- **Drawer/dropdown opens** → focus moves into the open content; ESC closes; focus returns.
- **Toast/notification appears** → does *not* steal focus. Provide a way to navigate to it (e.g., a hidden landmark, a key shortcut, or rely on `aria-live` for announcement).
- **Page navigation** (SPA route change) → manage focus on the new view's main heading or `<main>` element; announce the route change via `aria-live`.

**The focus-trap mistake.** A modal's focus trap must include all interactive elements *within the modal* and exclude everything else — including the page underneath. Trap implementations that escape the modal (e.g., when Tab reaches the last element and focus jumps to the browser chrome) break the model.

### Touch target sizing

WCAG 2.2 added 2.5.8 (Target Size — Minimum) at AA: 24×24 CSS pixels for any pointer target. WCAG 2.5.5 (Target Size — Enhanced) at AAA requires 44×44.

Platform conventions are stricter than the WCAG floor:

- **iOS HIG:** 44×44 pt minimum
- **Material Design (Android):** 48×48 dp minimum
- **Touch-targeted web:** 44×44 CSS pixels is the safer floor

**Auditing existing libraries:** small icon buttons (16×16, 20×20, 24×24 with no padding around them) are the most common offenders. The fix is usually to add a transparent padding zone around the visible icon — the visible element stays the brand-defined size; the touch target is larger via padding.

### Form components

Forms are where accessibility complexity concentrates because errors compound:

- **Visible labels.** Always. Placeholders are not labels — they disappear on focus, fail contrast, and screen readers handle them inconsistently.
- **`aria-describedby`** for helper text and error messages. Multiple IDs can be associated; screen readers read them in order after the label.
- **`aria-invalid="true"`** on fields with errors, paired with `aria-describedby` pointing at the error message. Visual error treatment supplements the announcement, doesn't replace it.
- **Required fields.** The `required` attribute (HTML5) communicates required state to assistive tech. Visual indicators (asterisk) supplement it. Document the convention and make it consistent.
- **Error summaries.** For longer forms, an error summary at the top of the form (with links to each errored field) aids navigation. This is a pattern, not a single component, and the DS should provide guidance.
- **Inline validation timing.** Validate on blur, not on every keystroke; announce the error after the user has stopped typing. Aggressive validation interrupts users' thinking.

### Interactive state coverage

Every interactive element has a set of states that must each be visually distinct *and* accessible:

| State | Trigger | Accessibility requirement |
|---|---|---|
| Default | At rest | Meets contrast for its content |
| Hover | Mouse over | Visible change; do not hide critical info behind hover (touch users don't have hover) |
| Focus | Keyboard or programmatic | Visible focus indicator (token-driven) meeting WCAG 2.4.11 |
| Focus-visible | Keyboard focus only | Same as focus, but only for keyboard — `:focus-visible` |
| Active | During click/press | Brief visual feedback |
| Disabled | Not interactive | aria-disabled or disabled attribute (decision below); contrast requirements relaxed (WCAG exempts disabled) but consider readability for users navigating to them |
| Error | Invalid input | Visual + ARIA announcement (aria-invalid + aria-describedby) |

**The `disabled` vs `aria-disabled` decision.** `disabled` (the HTML attribute) removes the element from the tab order and prevents interaction — but assistive tech often skips disabled elements entirely, so users may not understand why the action is unavailable. `aria-disabled` keeps the element focusable and announceable but requires the component to handle the click and explain why nothing happened. Most modern accessibility-led patterns prefer `aria-disabled` paired with a tooltip or message explaining the disabled reason. Both are defensible; document which one the component uses and why.

---

## 4. Accessibility in Figma

### What Figma can validate

Figma is a useful surface for some accessibility checks at design time:

- **Color contrast.** Stark, Contrast, and Able plugins compute WCAG ratios for selected pairings. Some can scan an entire page.
- **Color-blindness simulation.** Stark and built-in plugins simulate the major types (protanopia, deuteranopia, tritanopia, monochromacy).
- **Type sizes and hierarchy.** Visible at design — too-small text, missing heading hierarchy, undifferentiated text styles surface in review.
- **Touch target sizing.** Measurable; flag undersized targets at design review.
- **Visual focus indicators.** Designable; validate contrast and sizing at the design stage.

### What Figma can't validate

- **Keyboard navigation flow.** Until the design is in code, keyboard order, focus traps, and roving tabindex behavior can't be exercised.
- **Screen reader output.** What a screen reader actually announces depends on HTML/ARIA implementation and screen reader behavior. Can't be predicted from a Figma file.
- **Live region announcements** (toast notifications, form validation messages). Behavior, not appearance.
- **Cognitive accessibility** at the interaction level — how much working memory the flow demands, how forgiving the error states are, whether the language is plain.

### Annotation practices

Figma's native annotations have improved through 2024–2025 and are now the right surface for design-time accessibility documentation:

- **Reading order.** Numbered annotations on the design indicate intended DOM/tab order. This often differs from visual order — Figma's auto-layout left-to-right, top-to-bottom isn't always correct DOM order.
- **ARIA roles.** Annotate composite widgets with their role (`tablist`, `combobox`, `dialog`) so engineers know which APG pattern to implement.
- **Focus behavior.** What gets focus when the component opens? Where does focus return?
- **Alt text and aria-labels.** Documented per image and per icon-only button.
- **Form labels and error messages.** Which text is the label; which is the helper; which is the error.

The Microsoft A11y Annotation Kit is a well-developed Figma library of annotation components covering most of these concerns; many teams use it as a starting point and adapt to their conventions.

### Figma plugins worth knowing

- **Stark.** The most common contrast and color-blindness plugin. Does WCAG and APCA. Has a paid tier with broader features (focus order overlay, alt-text checks).
- **A11y Annotation Kit (Microsoft).** Component library + plugin for design-time annotation.
- **Able.** Lighter-weight contrast checker.
- **Contrast.** Simple contrast checker.
- **Include.** Annotation toolkit with reading order, roles, etc.

These are useful but their utility decays past contrast and annotation. Focus order, keyboard flow, and screen reader output remain code-level concerns; the plugins simulate but don't validate.

### Handoff requirements

For each component shipped, the design spec must include:

1. **Role** (semantic HTML element or ARIA role)
2. **Label** (what the screen reader announces)
3. **States and their visual treatment** (default, hover, focus, focus-visible, active, disabled, error, loading)
4. **Keyboard behavior** (which keys do what)
5. **Focus behavior** (what gets focus on open/activation; where focus goes on close)
6. **Live region behavior** (what gets announced asynchronously)
7. **Alt text or aria-label conventions** (for images, icons)
8. **Reading order** (if visual order differs from DOM order)

Components that don't ship with this in their spec are incomplete handoffs.

---

## 5. Documentation and consumer guidance

### What consumers need to know

The accessibility documentation a consumer needs is different from what a component author needs. **Consumers need to know what they can rely on the component to handle and what they must do themselves.** That two-part declaration is the load-bearing piece.

Per-component, the docs should cover:

- **What this component handles.** Explicit list: keyboard, focus, ARIA, contrast for built-in states, touch target sizing.
- **What the consumer must provide.** Explicit list: meaningful labels for icon-only buttons, alt text for images, descriptive error messages, sensible disabled states with explanation.
- **When to use it.** Use cases the component is designed for.
- **When not to use it.** Use cases it isn't designed for, with the alternative.
- **Avoid-when patterns.** Specific misuse to flag (e.g., "Don't use a Tooltip for critical information — tooltips are not reliably announced by all screen readers").
- **Conformance level.** "WCAG 2.2 AA conformant when used as documented."

### Encoding accessible patterns in usage guidance

The usage section is where the DS prevents the most common misuse patterns. A few examples:

- **Modal vs. drawer vs. inline.** "Use a modal when the user must take action before continuing. Use a drawer for secondary content that complements the page. Use inline expansion when the content is part of the page's reading flow." — prevents modal abuse for non-critical content.
- **Toast vs. inline message.** "Use a toast for transient confirmation. Use an inline message for persistent feedback the user needs to read. Don't use a toast for errors the user must address." — prevents toast misuse for critical messages.
- **Tooltip vs. helper text.** "Use a tooltip for supplemental info that isn't critical. Use helper text under the input for info the user needs to complete the form." — prevents tooltip misuse for required information.

These distinctions are accessibility decisions even when not framed that way. A toast that the user dismisses before reading is an accessibility failure as much as a UX one.

### Common misuse patterns to call out

Patterns that consistently produce a11y failures and benefit from being explicitly flagged in docs:

- **`<div onClick={...}>` instead of `<button>`.** No keyboard. No semantics. The DS should ship a `Button` and document "if you need a button, use Button — never an onClick on a div."
- **Placeholder as label.** Disappears on focus, fails contrast, screen reader inconsistency.
- **Color-only state communication.** Red border without an error icon or message; green checkmark without text.
- **Missing focus indicator.** `outline: none` without a replacement.
- **Modal without focus trap.** Focus escapes to the page beneath.
- **Form errors that aren't announced.** Visual error styling without `aria-invalid` and `aria-describedby`.
- **Aria-hidden on focusable elements.** Hides from screen readers; element still focusable; user gets focus on something they can't perceive.
- **Heading hierarchy skipped.** `<h1>` then `<h3>`. Confuses screen reader navigation.
- **Live region noise.** `aria-live="assertive"` for non-critical updates floods screen reader users with announcements.

Documentation that names these patterns prevents them better than documentation that explains general principles.

### Conformance levels in documentation

A DS should be explicit about its accessibility commitment, per-component:

- **What standard?** WCAG 2.2 AA is the typical floor. Some clients require Section 508 (US gov), EN 301 549 (EU), AODA (Ontario), or stricter levels.
- **What scope?** Web only? Mobile native too? US English only? Multi-locale (intersection with i18n)?
- **What level of testing has been done?** Automated only? Manual keyboard? Screen reader tested? On which screen readers?
- **What's the limitation?** Components that don't fully meet the standard (e.g., a complex data table that needs additional implementation work) should declare what they meet and what consumers must complete.

This per-component declaration is the contract. Without it, consumers assume conformance and ship products that quietly fail.

---

## 6. Testing accessibility

### What automation catches

Automated tools (axe-core is the dominant engine, used by Playwright accessibility, Cypress axe, the Storybook a11y addon, and most other tooling) catch a real subset of issues but never the whole picture. **Deque (the company behind axe-core) cites figures around 30–50% of WCAG issues being machine-detectable;** the exact percentage varies by methodology and content. Plan for this — automation is necessary, not sufficient.

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
- **Whether keyboard navigation is logical.** The DOM tab order can be valid but the user experience can be unusable.
- **Screen reader behavior.** What gets announced, in what order, with what intonation, depends on the screen reader and is not predictable from automated rules.
- **Cognitive accessibility.** Plain language, error message clarity, working memory load.
- **Whether disabled states are explained.** Automation can detect `aria-disabled`; it can't tell if the user knows why.
- **Whether color-coded UI works for color-blind users.** Detectable as a *risk* (color-only indicators); not detectable as a failure.

### Manual testing requirements

The manual layer is non-negotiable. The minimum a DS team should run, per component:

- **Keyboard-only navigation.** Tab through the component. Can every interactive element be reached? Is the order logical? Do focus indicators show? Does ESC close what should close?
- **Screen reader walkthrough.** Run through the component with a screen reader. What gets announced? Is the announcement useful? Are state changes announced?
- **Reduced motion / high contrast.** Toggle the OS settings. Does the component respect them?
- **Touch.** On a touch device, are targets large enough? Do interactions work without hover?
- **Zoom to 200% and 400%.** Does the layout reflow? Does anything become inaccessible?

These take 5–15 minutes per component. Multiplied across a 100-component library it's significant, but it's a one-time cost for a stable component plus regression on changes.

### Screen reader testing

The screen-reader landscape is fragmented; testing all of them is not realistic. The pragmatic minimum:

- **NVDA + Firefox and Chrome (Windows).** NVDA is free, widely used, and the most common screen reader on Windows after JAWS.
- **VoiceOver + Safari (macOS, iOS).** VoiceOver is the default Apple screen reader; Safari is its tightest pairing.
- **TalkBack + Chrome (Android).** Default Android screen reader.
- **JAWS + Chrome (Windows).** Still common in enterprise and government; expensive but worth covering for regulated-industry clients.

For a typical agency engagement, NVDA + VoiceOver is the floor; add JAWS for regulated industries; add TalkBack for mobile-heavy products. **Different screen readers behave differently with the same ARIA;** components that work in NVDA can fail in JAWS, particularly for newer ARIA patterns.

### When to test

The cycle that works:

- **Component author tests during development.** Keyboard, axe, one screen reader.
- **PR review includes accessibility checklist.** Reviewer runs through the manual checks.
- **CI runs axe on every PR.** Blocks on regressions.
- **Storybook a11y addon shows in development.** Surfaces issues live as the component is being built.
- **Periodic full-library audit.** External or rotating internal reviewer; quarterly is a defensible cadence; some shops do annually.
- **Real-user testing with assistive tech users.** Hardest to operationalize, highest signal. Worth budgeting for at major releases.

### Accessibility as a contribution gate

For new components proposed via the contribution workflow (see 07-governance-and-adoption), accessibility should be a non-bypassable review gate:

- **Automated checks must pass.** axe-core, contrast checks, build-time validations.
- **Manual checklist signed off.** Keyboard, focus, screen reader, reduced-motion, touch, zoom.
- **Documentation declares conformance.** Per-component statement of what's handled and what consumers must do.
- **APG conformance noted** for components that match a documented APG pattern; deviations called out and justified.

Components that fail any of these don't merge. This sounds harsh; in practice it's the only way to maintain accessibility consistency at scale.

---

## 7. Accessibility governance

### Defining the promise

The DS's accessibility promise is the contract clients and consumers rely on. It must be specific:

- **Standard and version:** "WCAG 2.2 Level AA"
- **Scope:** "All components, in their documented use, on web platforms. Native iOS and Android components target their respective platform accessibility guidelines (iOS HIG, Material). Multi-locale considerations covered separately (see 13-internationalization-and-rtl)."
- **Tested platforms:** "Latest two major versions of Chrome, Firefox, Safari, Edge. Screen readers: NVDA + Firefox/Chrome, VoiceOver + Safari, TalkBack + Chrome."
- **Out of scope:** What the DS doesn't promise — usually consumer-supplied content, custom modifications, third-party integrations.

This statement should live prominently in the DS documentation, not buried. Procurement and legal teams need to find it.

### Accessibility debt

Existing component libraries carry accessibility debt — components built before the team had accessibility expertise, components with deferred fixes, components whose patterns weren't audited. The remediation pattern:

1. **Audit and catalog.** Each component gets a current-state a11y assessment. Issues categorized: critical (blocks usage for assistive-tech users), major (significant friction), minor (cosmetic or edge case).
2. **Prioritize by usage.** High-usage components with critical issues are first; low-usage components with minor issues are last. The audit feeds a prioritized backlog.
3. **Fix incrementally.** Each release includes a few component-level a11y fixes. Don't try to fix everything in one heroic effort — the regression risk is too high.
4. **Document the debt visibly.** A "known issues" page in the DS docs is honest and useful. Consumers who hit the issues know they're known and being worked.
5. **Deprecate-and-replace** when the component's architecture is fundamentally inaccessible. A button with no keyboard handling can be retrofitted. A custom select that diverges from APG patterns and has been built without focus management is often easier to deprecate and replace than fix in place.

### Non-accessible designs and deviation

Clients sometimes request designs that are inaccessible — a brand color combination that fails contrast, a custom interaction pattern that breaks keyboard navigation, a graphic-heavy hero with no alt-text equivalent. The DS practice for handling this:

- **Push back first.** The accessible alternative is usually achievable within the brand and the design intent. Most failures are preventable; the request often comes from the brand team without awareness of the cost.
- **If the client insists, document the deviation.** An ADR (architecture decision record) capturing the request, the accessibility cost, the legal/regulatory risk, and the named decision-maker. This is the practice's cover and the client's eventual leverage.
- **Quantify the risk.** Section 508, ADA Title III (US), EU Accessibility Act, AODA (Ontario), Equality Act (UK) — varying enforcement, varying penalties. For regulated industries (healthcare, finance, government, education) the risk is concrete and current.
- **Limit scope of the deviation.** A non-accessible design choice should be limited to a specific surface, not propagated through the system. The DS's tokens and components remain conformant; the deviation is in the consuming product.
- **Set a remediation horizon.** Most accessibility deviations should have a stated end date — a release in which the issue is corrected. Deviations that become permanent are technical debt that compounds.

The practice should never quietly ship a non-accessible design without the documentation trail. The legal exposure for the client and the reputational exposure for the agency both compound when the deviation is undocumented.

---

## References

Primary sources, current as of Jan 2026.

**W3C and WAI:**
- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- WAI-ARIA 1.2: <https://www.w3.org/TR/wai-aria-1.2/>
- ARIA Authoring Practices Guide: <https://www.w3.org/WAI/ARIA/apg/>
- WCAG 3 working draft: <https://www.w3.org/TR/wcag-3.0/> (status: working draft; not yet stable)

**APCA:**
- APCA reference: <https://github.com/Myndex/SAPC-APCA>
- APCA-W3 in WCAG 3: candidate, status evolving

**Tooling:**
- axe-core: <https://github.com/dequelabs/axe-core>
- Deque on automation coverage: <https://www.deque.com/automated-accessibility-testing-coverage/>
- Storybook a11y addon: <https://storybook.js.org/addons/@storybook/addon-a11y>
- Playwright accessibility testing: <https://playwright.dev/docs/accessibility-testing>
- Pa11y: <https://pa11y.org/>

**Figma plugins:**
- Stark: <https://www.getstark.co/>
- Microsoft A11y Annotation Kit: searchable in Figma Community
- Include (annotation toolkit): searchable in Figma Community

**Platform HIG:**
- Apple HIG — Accessibility: <https://developer.apple.com/design/human-interface-guidelines/accessibility>
- Material Design — Accessibility: <https://m3.material.io/foundations/accessible-design/overview>
- Microsoft Inclusive Design: <https://inclusive.microsoft.design/>

**Practitioner sources:**
- Heydon Pickering — *Inclusive Components* (book and site): <https://inclusive-components.design/>
- Adrian Roselli — accessibility writing: <https://adrianroselli.com/>
- Sara Soueidan — accessibility-focused component writing
- Adobe Spectrum — accessibility documentation per-component: <https://spectrum.adobe.com/page/accessibility/>
- Polaris (Shopify) — accessibility documentation
- Carbon (IBM) — accessibility documentation

**Regulatory:**
- Section 508 (US): <https://www.section508.gov/>
- EN 301 549 (EU): published harmonised standard
- ADA Title III (US): enforcement context
- AODA (Ontario): regulatory framework
- EU Accessibility Act: in force as of June 2025

**Note on currency:** WCAG version (2.2 stable; 2.3 in development; 3.0 working draft), APCA standardization status, browser ARIA support, and screen reader behavior all evolve. For client-facing recommendations on contrast standards, conformance commitments, and regulatory scope, verify against current authoritative sources before locking in.

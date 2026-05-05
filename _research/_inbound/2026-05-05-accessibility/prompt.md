You are researching accessibility as it applies to design systems, for a senior design systems practitioner at a digital agency. The output is a structured knowledge document. This is not a WCAG primer — assume the reader knows the standards at a working level. The focus is on how accessibility is encoded into a design system so that products built from it are accessible by default, not by retrofit.

Research scope — cover all of the following:

1. Accessibility architecture in a design system

The principle of accessibility-by-default: how a DS can make the accessible choice the easy choice
Where accessibility lives in a DS: token layer, component behavior, documentation, contribution gates
Accessibility as a first-class design constraint vs. an audit activity — the practical difference in outcomes

2. Token-level accessibility

Color contrast in a semantic token architecture: how to structure color tokens so that accessible contrast pairs are enforced by the system, not checked after the fact
Contrast requirements by context: WCAG 2.2 AA vs. AAA, UI components vs. text, decorative elements
Color blindness and the limits of contrast ratios alone: additional considerations for DS color systems
Motion tokens: prefers-reduced-motion as a first-class token concern
Focus indicator tokens: how to encode visible focus states systematically

3. Component-level accessibility

ARIA roles, states, and properties: how to document and enforce correct ARIA usage in a DS component library
Keyboard navigation patterns: which components require which interaction patterns (modal trapping, roving tabindex, etc.) and how to document these for consumers
Focus management: patterns for components that control focus (modals, drawers, dropdowns, toasts)
Touch target sizing: WCAG 2.5.5 and 2.5.8, platform-specific considerations (iOS HIG, Material)
Form component accessibility: labeling, error states, helper text, required field conventions
Interactive state coverage: how to ensure all states (hover, focus, active, disabled, error) are accessible and documented

4. Accessibility in Figma

Annotation practices: documenting ARIA roles, reading order, focus behavior, alt text in Figma specs
Figma plugins for accessibility (Able, A11y Annotation Kit, etc.) — current utility and limitations
Designing accessible components in Figma: what can be validated at design stage vs. what requires code
Handoff: what accessibility information must be in the spec for developers to implement correctly

5. Documentation and consumer guidance

How to write useful accessibility documentation for DS consumers: what they need to implement correctly
Usage guidelines that encode accessible patterns: when to use a component, when not to, avoid-when
Common misuse patterns that create accessibility failures — how DS documentation can prevent them
Accessibility conformance levels in DS documentation: how to communicate what a component provides out of the box vs. what the consumer must implement

6. Testing accessibility in a design system

Automated accessibility testing in a DS CI pipeline: tools (axe-core, Playwright accessibility, Storybook a11y addon), what they catch and what they miss
Manual testing requirements that automation cannot replace
Screen reader testing: which screen readers to test, at what point in the development cycle, and what to test for
Accessibility as a contribution gate: how to enforce accessibility standards in a DS contribution workflow

7. Accessibility governance

How to define and communicate the DS's accessibility promise: what version of WCAG, what level, what scope
Handling accessibility debt in an existing component library
When a client requests a non-accessible design: how to document the deviation and its risk

Output format: Structured markdown. Use section headings that match the numbered scope above. Synthesize toward practical guidance, not compliance checklists. Where WCAG requirements translate into DS architecture decisions, make that translation explicit. Where the field has consensus, state it clearly; where decisions are context-dependent (e.g., APCA vs. WCAG 2.x contrast, automated vs. manual test split), provide decision frameworks rather than declaring a winner. Flag areas where DS tools (Figma, axe-core, Storybook a11y addon, screen readers, etc.) have known gaps that practitioners work around. Where claims depend on current platform state — WCAG version, APCA standardization status, browser ARIA support, screen reader behavior — date them and note the verification path. Include references to primary sources (WCAG 2.2, APCA, ARIA Authoring Practices Guide, platform HIG accessibility documentation, axe-core documentation).

Depth: Expert audience. Do not explain what ARIA is or what WCAG levels are — explain how a DS encodes them so that consumers can't get them wrong.

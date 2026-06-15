You are researching the Textarea component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a
textarea is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions that are still
contested, the implementation traps that recur across codebases.

The reader has already read the practice's Text Field brief
(components/text-field.md). Do NOT re-derive the concerns Textarea
shares with Text Field — label/helper/error wiring, the aria-describedby
chain, placeholder-is-not-a-label, read-only vs. disabled, the
required/optional convention. Reference them as shared and concentrate
on what is Textarea-specific: the auto-resize / auto-grow model, the
manual resize handle, min/max rows and scroll behaviour, the character
counter as a first-class concern, paste handling, Enter-key semantics
(newline vs. submit), maxLength enforcement, and the
textarea-vs-rich-text-editor boundary.

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum
- Google Material 3
- IBM Carbon
- GitHub Primer
- Atlassian Design System
- Shopify Hydrogen (where it diverges from Polaris)
- Base Web (Uber)

Mobile reference (where the component has a mobile dimension):

- Apple Human Interface Guidelines
- Material 3 (Compose / mobile)
- Microsoft Fluent

Cite each system referenced with a version date — e.g., (Polaris 12.0,
2025), (Material 3, 2024), (Spectrum 2024.4). Currency matters; section
14 of the brief is the auditable record.

Output structure — follow this 15-section spine:

1. Framing — what this component is, what it isn't, why systems
   disagree on it.
2. Anatomy and parts — structural model, named parts, slot vocabulary.
3. Properties / API — converged prop set across field leaders;
   divergences with reasoning.
4. States and variants — runtime states (rest / hover / focus-visible /
   pressed / disabled / loading / error / empty / read-only) vs.
   intentional variants (size / tone / density / emphasis); canonical
   matrix.
5. Usage guidance — when to use, when not to use, what to use instead.
6. Accessibility — component-specific concerns. The reader has read
   14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory;
   identify what is specific to this component (ARIA pattern, keyboard
   model, focus contract, AT announcements, the WCAG SC the component
   participates in).
7. Content guidelines — labels, tone, error / empty / CTA copy patterns.
8. Motion and transition — entry / exit, state transitions,
   reduce-motion contract.
9. Internationalization — RTL behaviour, text expansion, locale
   concerns.
10. Naming — what the field calls it; the practice's default; aliases
    consumers will reach for.
11. Implementation notes — framework-specific gotchas, prop-vs-slot
    decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships (composes
    with / alternative to / supersedes / superseded by).
13. Field POV evolution — how the leading systems' position has changed;
    recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing the
    brief's structured content as the practice's opinionated `.ai.json`
    shape for this component. Free-form YAML; the schema is the
    structured projection of sections 1–13. Cover: identity (id, name,
    aliases, category, status), API (props with
    type/default/required/deprecated/description), composition
    (composes-with, alternative-to, supersedes, superseded-by),
    accessibility (wcag-criteria, aria-attributes, keyboard-model,
    focus-behavior), states, variants, content (label-pattern,
    error-pattern, empty-pattern). The schema must not contradict any
    prose section above; if it does, the prose wins and the schema is
    wrong.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state —
feature names, version flags, ARIA attributes that recently changed —
date them and note the verification path.

Depth: Expert audience. Do not explain what a textarea is or that it
accepts multiple lines of text — explain the auto-resize / scroll model,
the character-counter and paste-handling contracts, the Enter-key
semantics, and the textarea-vs-rich-text boundary that field leaders
still disagree on.

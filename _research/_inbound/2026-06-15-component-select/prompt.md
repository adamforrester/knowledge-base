You are researching the Select component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a select
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions that are still contested, the
implementation traps that recur across codebases.

The reader has already read the practice's Text Field and Textarea
briefs (components/text-field.md, components/textarea.md). Do NOT
re-derive the shared form-field substrate — label/helper/error wiring,
the aria-describedby chain, placeholder-is-not-a-label, read-only vs.
disabled, the required/optional convention, the bundled-props vs.
composed-slots hybrid. Reference them as shared and concentrate on what
is Select-specific.

The defining tension to resolve: native <select> vs. a custom
ARIA-listbox component. Concentrate the brief on:
- the native-vs-custom decision and when each wins (mobile, styling,
  option-content richness, accessibility cost)
- the select-vs-combobox boundary (no text filtering = listbox; text
  filtering = combobox — the single most-confused adjacency)
- single vs. multi-select models (checkboxes, tags/tokens, the
  select-all, the count-summary trigger)
- option and option-group structure (optgroup, descriptions, icons,
  disabled options)
- the trigger/button anatomy, the popover/listbox positioning model
  (Floating UI / the CSS Anchor Positioning + Popover API shift),
  collision handling, and scroll-into-view
- the placeholder-option vs. label problem and the empty/no-selection
  state
- typeahead / type-to-select, keyboard model, and the long-list /
  virtualization problem

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

Depth: Expert audience. Do not explain what a select is or that it lets
a user choose from a list — explain the native-vs-custom decision, the
select-vs-combobox boundary, the multi-select models, the listbox
positioning and keyboard contract, and the long-list problem that field
leaders still disagree on.

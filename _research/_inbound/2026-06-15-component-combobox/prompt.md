You are researching the Combobox component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a
combobox is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions that are still
contested, the implementation traps that recur across codebases.

The reader has already read the practice's Text Field, Textarea, and
Select briefs (components/text-field.md, components/textarea.md,
components/select.md). Combobox stands on BOTH:
- from Text Field, the shared form-field substrate — label/helper/error
  wiring, the aria-describedby chain, placeholder-is-not-a-label,
  read-only vs. disabled, required/optional, the bundled-props vs.
  composed-slots hybrid;
- from Select, the overlay/listbox machinery — the popover/listbox
  positioning model (Floating UI / CSS Anchor Positioning + Popover
  API), the aria-activedescendant focus contract (DOM focus stays on
  the input), option/option-group structure, multi-select token vs.
  count models, long-list virtualization, and the mobile tray mutation.

Do NOT re-derive either substrate. Reference them as inherited and
concentrate on what is genuinely Combobox-specific. The defining fact:
a Combobox is a text input that destructively FILTERS a listbox as the
user types — that is the line that separates it from Select (see the
select brief's select-vs-combobox boundary). Concentrate the brief on:

- the editable text input as trigger (vs. Select's button trigger), and
  the full ARIA 1.2 combobox pattern (role=combobox on the input,
  aria-expanded, aria-controls, aria-autocomplete, aria-activedescendant)
- the autocomplete/autosuggest model: none vs. list vs. inline vs. both
  (the aria-autocomplete values), and inline-completion / typeahead-text
  selection behaviour and its pitfalls
- filtering and matching: substring vs. prefix vs. fuzzy, diacritic and
  case normalization, match highlighting, and who owns the filter
  (component vs. consumer)
- free-text / allow-arbitrary-value vs. strict (must-match) modes, and
  the boundary with a "creatable" select and with a tags/token input
- async / remote options: debounce, race-condition cancellation, the
  loading / empty / no-results / minimum-query states, and error
- single vs. multi-select combobox (token/tag input, the autocomplete
  multi pattern), and the combobox-vs-tags-input boundary
- selection-vs-input-value reconciliation: what the input shows after
  blur, restoring the last valid value, clearing, the controlled-value
  trap
- the combobox-vs-select and combobox-vs-search-field boundaries

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum (React Aria ComboBox)
- Google Material 3
- IBM Carbon (ComboBox / MultiSelect.Filterable)
- GitHub Primer
- Atlassian Design System (react-select)
- Shopify Hydrogen (predictive search, where it diverges)
- Base Web (Combobox / Select creatable)

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
    shape for this component. Free-form values, but follow the locked
    key order and conventions in components/_schema.md (identity,
    description, [anatomy], api, states, variants, accessibility,
    content, [motion], [i18n], [implementation], composition, notes;
    use inherits: for the text-field/select substrate; flag unverified
    claims under notes.unverified). The schema must not contradict any
    prose section above; if it does, the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state —
feature names, version flags, ARIA attributes that recently changed —
date them and note the verification path.

Depth: Expert audience. Do not explain what a combobox is or that it
filters a list — explain the autocomplete-mode model, the filtering and
free-text-vs-strict decisions, the async/race-condition handling, the
selection-vs-input-value reconciliation, and the multi-select/token
boundary that field leaders still disagree on.

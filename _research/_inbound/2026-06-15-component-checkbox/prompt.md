You are researching the Checkbox component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of
how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a
checkbox is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions that are still
contested, the implementation traps that recur across codebases.

The reader has already read the practice's Text Field, Select, and
Combobox briefs (components/text-field.md, components/select.md,
components/combobox.md). Do NOT re-derive the generic form-field
substrate those cover — the error/helper text association via
aria-describedby, the required/optional convention, disabled vs.
read-only, the bundled-props vs. composed-slots encapsulation tension in
the abstract. Reference them as shared. Concentrate on what is
Checkbox-specific.

THE CENTRAL ARCHITECTURAL QUESTION this brief must resolve (and the
reason it is being commissioned) is component DECOMPOSITION. A checkbox
shows up in the field at (at least) three different granularities, and
systems draw the component boundaries between them very differently:

  1. the ATOMIC control — the box/checkmark itself, with no label;
  2. the LABELLED ROW / FIELD — the box plus its adjacent label, an
     optional description/helper line, and an optional inline error,
     presented as a single clickable line item;
  3. the GROUP — a set of multiple rows under a shared group label
     (a fieldset/legend or role=group), often with group-level
     required/validation/error and a layout axis (vertical/horizontal).

Survey rigorously and WITHOUT a predetermined answer: does each field
leader ship one polymorphic Checkbox (label as an optional prop), or a
separate atomic control + a field/row wrapper + a group component?
Where does the label and description live — a prop on the control, or a
composed child? Where does the accessible name come from at each tier?
How does the group own the shared label, the value (array), and
group-level validation/required/error? What are the fieldset/legend vs.
role=group semantics? Land a clear, reasoned position on how the
practice should decompose this — how many components, where each
boundary sits, and why — because the same decomposition decision will
carry to Radio and Switch. Treat this as a first-class section of the
brief (it belongs primarily in §2 anatomy, §3 API, §10 naming, and §12
related components).

Also concentrate on these Checkbox-specific concerns:
- the INDETERMINATE (mixed/tri-state) state — that it is a visual/AT
  state set via JS property (not an HTML attribute and not a third
  value), the parent/child "select all" pattern, and aria-checked=mixed
- the label-association contract and click target — the whole row
  (control + label) is the hit target; label-beside not label-above
  (unlike text field); minimum target size
- alignment — top-aligned control with multi-line labels and
  descriptions; baseline vs. center alignment
- single standalone checkbox (e.g. a consent "I agree") vs. the
  checkbox set, and when a group is/ isn't required
- the checkbox-vs-switch boundary (pending state / form-submit vs.
  immediate effect) and the checkbox-vs-toggle-button boundary

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum (React Aria Checkbox / CheckboxGroup)
- Google Material 3
- IBM Carbon
- GitHub Primer
- Atlassian Design System
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
   (Resolve the atomic / row / group decomposition here.)
3. Properties / API — converged prop set across field leaders;
   divergences with reasoning. (Cover the control, the row, and the
   group APIs and where each boundary sits.)
4. States and variants — runtime states (rest / hover / focus-visible /
   pressed / disabled / indeterminate / error / read-only) vs.
   intentional variants (size / alignment / density); canonical matrix.
5. Usage guidance — when to use, when not to use, what to use instead.
6. Accessibility — component-specific concerns. The reader has read
   14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory;
   identify what is specific to this component (native input semantics,
   indeterminate/aria-checked=mixed, the group fieldset/legend or
   role=group + aria-describedby contract, keyboard model, the WCAG SC
   the component participates in).
7. Content guidelines — labels, tone, error / group-label copy patterns.
8. Motion and transition — check/uncheck/indeterminate transitions,
   reduce-motion contract.
9. Internationalization — RTL behaviour (control side swap), text
   expansion of labels, locale concerns.
10. Naming — what the field calls the control, the row, and the group;
    the practice's default; aliases consumers will reach for.
11. Implementation notes — framework-specific gotchas (indeterminate
    via ref, controlled/uncontrolled, the group value array), prop-vs-
    slot decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships (composes
    with / alternative to / supersedes / superseded by), including the
    control/row/group relationship and the radio/switch siblings.
13. Field POV evolution — how the leading systems' position has changed;
    recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing the
    brief's structured content as the practice's opinionated `.ai.json`
    shape for this component. Free-form values, but follow the locked
    key order and conventions in components/_schema.md (identity,
    description, [anatomy], api, states, variants, accessibility,
    content, [motion], [i18n], [implementation], composition, notes;
    use inherits: for the shared form-field substrate; flag unverified
    claims under notes.unverified). If the decomposition resolves to
    more than one component, represent that explicitly in the schema
    (e.g. nested identities or a components list). The schema must not
    contradict any prose section above; if it does, the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state —
feature names, version flags, ARIA attributes that recently changed —
date them and note the verification path.

Depth: Expert audience. Do not explain what a checkbox is or that it
toggles on and off — explain the atomic/row/group decomposition, the
indeterminate state mechanics, the label-association and hit-target
contract, and the group validation model that field leaders still
disagree on.

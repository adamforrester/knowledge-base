You are researching the Radio (radio button / radio group) component for
a senior design systems practitioner at a digital agency. The output is
a field-truth study of how the leading design systems handle this
component — what they converge on, where they diverge, and what the
practice's opinionated default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a radio
button is, knows what a design system is, and has shipped multiple
component libraries. Explain the non-obvious — the prop choices field
leaders disagree on, the accessibility decisions that are still
contested, the implementation traps that recur across codebases.

The reader has already read the practice's Text Field, Select, Combobox,
and especially CHECKBOX briefs (components/checkbox.md). The Checkbox
brief established the practice's SELECTION-CONTROL DECOMPOSITION, which
Radio INHERITS — do not re-derive it from scratch. That model is:
  - a two-component public surface: the labelled control (Checkbox) + a
    distinct group (CheckboxGroup) that owns the shared label, the value,
    and group-level validation;
  - PLUS an exposed atomic primitive (Checkbox.Control) that is the
    nestable unit for host components (list row, table cell, menu item,
    card), where the host provides the accessible name + hit target and
    the enclosing collection owns selection + group semantics.
Confirm how this decomposition maps to Radio and where it DIFFERS, then
spend the brief on the radio-specific substance. State the analogous
components (Radio / RadioGroup / Radio.Control) and the key structural
difference up front.

THE DEFINING RADIO-SPECIFIC DIFFERENCES to resolve and go deep on:
- the GROUP IS MANDATORY — a single radio is semantically meaningless;
  RadioGroup owns the shared `name`, the single selected value, and
  required/validation. (Contrast: a standalone Checkbox is valid; a
  standalone Radio is not.) What does this mean for the API and for the
  atomic primitive when nested in a collection (the collection IS the
  radiogroup, single-selection)?
- the KEYBOARD MODEL — the group is a SINGLE tab stop (roving tabindex),
  and arrow keys move between AND select options, unlike checkbox's
  Tab-to-each + Space. Cover roving tabindex vs. aria-activedescendant,
  Home/End, and wrap-around.
- SELECTION-FOLLOWS-FOCUS vs. explicit selection — the APG allows arrow
  to both move focus and select; when is each appropriate (and the trap
  for screen-reader users / expensive onChange)?
- NO DESELECT — clicking/activating a selected radio does not uncheck
  it; a radio group, once set, cannot return to none via the control
  (contrast checkbox). The implication for "no default selection" /
  optional groups, and whether to offer an explicit "None" option.
- DEFAULT / INITIAL SELECTION — should a radio group pre-select a
  default, or start with none selected? The accessibility and UX
  arguments both ways.
- NO INDETERMINATE state (unlike checkbox).
- the boundaries: radio-vs-segmented-control (same single-select
  semantics, different presentation/density), radio-vs-select (exposed
  vs. collapsed, the ~5-7 option threshold), radio-vs-switch, and
  radio-vs-checkbox (exactly-one vs. any-number).

Also cover, but lean on the checkbox brief rather than re-deriving:
label association and the whole-row hit target; top/baseline alignment;
RTL control-side swap; positive parallel label phrasing; reduced-motion.

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum (React Aria RadioGroup / Radio)
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
   (Map the inherited control / group / atomic-primitive decomposition;
   foreground the mandatory group.)
3. Properties / API — converged prop set; divergences with reasoning.
   (The group owns name + single value + validation.)
4. States and variants — runtime states (rest / hover / focus-visible /
   pressed / selected / disabled / error / read-only) vs. intentional
   variants (size / orientation / density); canonical matrix.
5. Usage guidance — when to use, when not to use, what to use instead.
6. Accessibility — component-specific concerns. The reader has read
   14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory;
   identify what is specific to this component (radiogroup/role=radio,
   roving tabindex + arrow selection, selection-follows-focus, the
   fieldset/legend or role=radiogroup contract, the WCAG SC it
   participates in).
7. Content guidelines — option labels, group label, tone, error copy.
8. Motion and transition — select transition, reduce-motion contract.
9. Internationalization — RTL behaviour, text expansion, locale.
10. Naming — control / group / atomic primitive; the practice's default;
    aliases consumers will reach for.
11. Implementation notes — framework-specific gotchas (roving tabindex,
    the shared name, controlled/uncontrolled single value), prop-vs-slot
    decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships (composes
    with / alternative to / supersedes / superseded by), incl. the
    control/group relationship and the checkbox/switch/segmented-control
    siblings.
13. Field POV evolution — how the leading systems' position has changed;
    recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing the
    brief's structured content as the practice's opinionated `.ai.json`
    shape for this component. Free-form values, but follow the locked
    key order and conventions in components/_schema.md (identity,
    description, [anatomy], api, states, variants, accessibility,
    content, [motion], [i18n], [implementation], composition, notes;
    use inherits: for the shared form-field substrate and the checkbox
    decomposition; flag unverified claims under notes.unverified).
    Represent the control / group / atomic-primitive decomposition
    explicitly. The schema must not contradict any prose section above;
    if it does, the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state —
feature names, version flags, ARIA attributes that recently changed —
date them and note the verification path.

Depth: Expert audience. Do not explain what a radio button is or that it
selects one of many — explain the mandatory-group architecture, the
roving-tabindex/arrow-selection keyboard model, selection-follows-focus,
the no-deselect and default-selection decisions, and the
radio-vs-segmented-control / radio-vs-select boundaries that field
leaders still disagree on.

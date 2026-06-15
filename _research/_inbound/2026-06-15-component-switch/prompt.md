You are researching the Switch (toggle) component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a switch
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions that are still contested, the
implementation traps that recur across codebases.

The reader has already read the practice's Text Field, Select, Combobox,
and especially the CHECKBOX and RADIO briefs (components/checkbox.md,
components/radio.md). The Checkbox brief established the practice's
SELECTION-CONTROL DECOMPOSITION — a labelled control + a distinct group +
an exposed atomic primitive (Checkbox.Control) that is the nestable unit
for host components, where the host provides the accessible name + hit
target. Radio inherited that with the group made MANDATORY. Switch is the
third refinement and is being commissioned partly to CLOSE this arc:
confirm how the decomposition maps to Switch and where it DIFFERS. The
expected difference is that a Switch has NO group (switches are
independent, immediate-effect toggles, not a member of a mutually-related
set) — so the surface is the labelled control (Switch) + the atomic
primitive (Switch.Control) for nesting in settings rows / list rows, with
no SwitchGroup. Confirm or challenge this up front, then spend the brief
on the switch-specific substance.

THE DEFINING SWITCH-SPECIFIC SUBSTANCE to resolve and go deep on:
- IMMEDIATE EFFECT is the defining property — toggling a switch applies
  the change instantly, with no save/submit step. This is the
  checkbox-vs-switch boundary (staged vs. immediate) stated from the
  switch's side. Go deep on what "immediate" demands of the component.
- THE ASYNC / OPTIMISTIC-UPDATE PROBLEM (the hardest, most contested
  part): when the immediate effect is a network call that can fail, what
  is the contract? Optimistic toggle + revert-on-error, a pending/loading
  state on the control, disabling during flight, error messaging, and
  the race conditions. How do field leaders handle (or duck) this?
- THE ARIA CONTRACT — role="switch" + aria-checked, and the precise
  distinction from checkbox (role=checkbox) and from a toggle BUTTON
  (role=button + aria-pressed). When is each correct? Screen-reader
  announcement differences ("on/off" vs "checked").
- LABEL SIDE — switches frequently place the label on the LEADING side
  with the control trailing (the settings-row pattern: label left,
  control right), the opposite of checkbox/radio (control leads). Resolve
  the practice's default and when it flips.
- ON/OFF AFFORDANCE — on/off text or I/O icons on the track, a visible
  state label, or neither; the contested iOS-vs-Material treatments.
- NO INDETERMINATE, the read-only question, no group/validation in the
  usual sense; whether a switch is ever "required".
- the boundaries: switch-vs-checkbox (immediate vs staged), switch-vs-
  toggle-button (aria-checked vs aria-pressed; setting vs action), and
  switch-vs-two-radios.

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum (React Aria Switch)
- Google Material 3
- IBM Carbon (Toggle)
- GitHub Primer (ToggleSwitch)
- Atlassian Design System (Toggle)
- Base Web (Uber)

Mobile reference (where the component has a mobile dimension — and the
switch is mobile-origin, so this matters more than usual):

- Apple Human Interface Guidelines (the canonical toggle)
- Material 3 (Compose / mobile)
- Microsoft Fluent

Cite each system referenced with a version date — e.g., (Polaris 12.0,
2025), (Material 3, 2024), (Spectrum 2024.4). Currency matters; section
14 of the brief is the auditable record.

Output structure — follow this 15-section spine:

1. Framing — what this component is, what it isn't, why systems
   disagree on it.
2. Anatomy and parts — structural model, named parts, slot vocabulary.
   (Map the inherited control / atomic-primitive decomposition; confirm
   the NO-group refinement.)
3. Properties / API — converged prop set; divergences with reasoning.
   (Include the async/pending props and the label-side prop.)
4. States and variants — runtime states (rest / hover / focus-visible /
   pressed / on / off / disabled / loading-pending / error / read-only)
   vs. intentional variants (size / label-side / with-icons); canonical
   matrix.
5. Usage guidance — when to use, when not to use, what to use instead.
6. Accessibility — component-specific concerns. The reader has read
   14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory;
   identify what is specific to this component (role=switch vs checkbox
   vs aria-pressed, on/off announcement, the immediate-effect
   announcement, keyboard model, the WCAG SC it participates in).
7. Content guidelines — label phrasing (describe the setting, not the
   state), on/off text, error copy.
8. Motion and transition — the thumb slide, state transition,
   reduce-motion contract.
9. Internationalization — RTL behaviour (the thumb travel direction and
   label side), text expansion, locale concerns.
10. Naming — Switch vs. Toggle vs. ToggleSwitch; the practice's default;
    aliases consumers will reach for.
11. Implementation notes — framework-specific gotchas (the optimistic-
    update + revert pattern, controlled/uncontrolled, role=switch), prop-
    vs-slot decisions, headless-vs-opinionated tension.
12. Related and alternative components — typed relationships (composes
    with / alternative to / supersedes / superseded by), incl. the
    checkbox / toggle-button / radio siblings and the settings-row host.
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
    Represent the control / atomic-primitive decomposition (and the
    absence of a group) explicitly. The schema must not contradict any
    prose section above; if it does, the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state —
feature names, version flags, ARIA attributes that recently changed —
date them and note the verification path.

Depth: Expert audience. Do not explain what a switch is or that it turns
something on and off — explain the immediate-effect contract, the
async/optimistic-update model, the role=switch-vs-checkbox-vs-aria-pressed
distinction, the label-side decision, and the switch-vs-checkbox /
switch-vs-toggle-button boundaries that field leaders still disagree on.

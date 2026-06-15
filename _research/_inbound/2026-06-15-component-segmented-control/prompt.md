You are researching the Segmented Control component (a.k.a. Connected
Button Group / ToggleButtonGroup) for a senior design systems
practitioner at a digital agency. Field-truth study; the practice is
establishing an opinionated default.

This is not an introductory guide. Assume the reader knows what a
segmented control is and has shipped multiple component libraries.
Explain the non-obvious — the prop choices field leaders disagree on, the
accessibility decisions still contested, the implementation traps.

The reader has already read the practice's BUTTON, RADIO, SWITCH,
CHECKBOX, and TOGGLE BUTTON briefs (components/button.md,
components/radio.md, components/toggle-button.md, etc.). Segmented Control
stands on two of them and you should NOT re-derive them:
- it is the GROUP of the TOGGLE BUTTON (the atomic unit;
  components/toggle-button.md) presented as a connected, horizontally
  joined control;
- for the single-select case it shares RADIO's semantics and keyboard
  model (the radio brief calls segmented control "identical single-select
  semantics, different skin"; roving tabindex, selection-follows-focus —
  components/radio.md).
Confirm how it inherits these and concentrate on the segmented-specific
substance.

THE DEFINING CONTESTED QUESTIONS to resolve and go deep on:
- THE SINGLE-VS-MULTI ARIA FORK — is a segmented control a single-select
  radiogroup (role=radiogroup + role=radio, roving tabindex, exactly one
  active) or a group of toggle buttons (role=group + aria-pressed,
  single OR multiple active)? Systems support different combinations
  (e.g. MUI ToggleButtonGroup exposes exclusive vs. multiple). Resolve
  the practice's model: when is it a radiogroup vs. a pressed-button
  group, and what ARIA + keyboard model follows from each.
- THE SEGMENTED-VS-RADIO boundary — same single-select semantics,
  different presentation/density. When to reach for which.
- THE SEGMENTED-VS-TABS boundary — both are horizontal single-select
  rows; tabs switch PANELS (role=tablist/tab/tabpanel) and are a
  navigation/disclosure pattern, segmented switches a value/filter/view
  in place. This boundary is heavily confused; resolve it crisply.
- THE SEGMENTED-VS-SELECT boundary — exposed compact vs. collapsed.
- segment-count + width constraints — the ~2-5 segment sweet spot,
  equal-width vs. content-width, the no-overflow rule (what to use when
  there are too many segments), and icon-only vs. text vs. icon+text
  segments.
- the iOS Segmented Control vs. Material 3 Connected/Segmented Button
  Group divergence (visual model, single vs. multi, selected treatment).
- the selected-segment indicator (the sliding pill / background) and its
  motion + reduce-motion contract.

Survey: Adobe Spectrum, Google Material 3 (Segmented/Connected Buttons),
IBM Carbon (ContentSwitcher), GitHub Primer (SegmentedControl), Atlassian,
Base Web (ButtonGroup), MUI (ToggleButtonGroup). Mobile: Apple HIG
(UISegmentedControl — the canonical), Material 3 Compose, Microsoft
Fluent. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for toggle-button / radio; flag
unverified under notes.unverified). Represent the single-vs-multi
decomposition explicitly.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a segmented control is —
explain the single-vs-multi ARIA fork, the segmented-vs-radio /
segmented-vs-tabs / segmented-vs-select boundaries, the segment-count and
width constraints, and the iOS-vs-Material divergence that field leaders
still disagree on.

You are researching the Slider (range slider) component for a senior
design systems practitioner at a digital agency. The output is a
field-truth study of how the leading design systems handle this
component — what they converge on, where they diverge, and what the
practice's opinionated default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what a slider
is, knows what a design system is, and has shipped multiple component
libraries. Explain the non-obvious — the prop choices field leaders
disagree on, the accessibility decisions still contested, the
implementation traps that recur across codebases.

The reader has already read the practice's form briefs, especially TEXT
FIELD (components/text-field.md), which established the shared form-field
substrate (label / helper / error wiring via aria-describedby, the
required/optional convention, disabled vs. read-only, the bundled-props
vs. composed-slots hybrid) and the NumberField as a distinct typed
sibling. Do NOT re-derive that substrate; reference it as shared.
Concentrate on what is Slider-specific.

THE DEFINING SLIDER-SPECIFIC SUBSTANCE to resolve and go deep on:
- SINGLE-THUMB vs. RANGE (two-thumb) — is the range a mode of one
  component or a separate component? The two-thumb model adds: thumb
  collision / minimum-distance, which thumb a track-click moves, and two
  independent aria-valuemin/max windows. Resolve the practice's model.
- THE STEP / TICK MODEL — continuous vs. stepped; step granularity;
  visible tick marks and snapping; float-step rounding traps; non-linear
  (e.g. logarithmic) scales for price/zoom.
- VALUE DISPLAY — tooltip-on-thumb vs. inline value label vs. min/max
  end labels; always-visible vs. on-interaction; finger-occlusion of the
  thumb tooltip on touch.
- THE KEYBOARD CONTRACT — Arrow = step, PageUp/PageDown = large step,
  Home/End = min/max; the shift/large-step convention; and the
  range-slider keyboard model (focusing and moving each thumb).
- THE ARIA CONTRACT — role="slider", aria-valuenow/valuemin/valuemax,
  and aria-valuetext for formatted/non-numeric values ("$50", "Medium",
  a date); per-thumb labelling in the range case.
- THE SLIDER-VS-NUMBER-FIELD (precision) BOUNDARY — sliders are for
  approximate/relative values where seeing the range matters; precise
  entry needs a paired number input. When to pair them, and the
  slider+input composite pattern.
- HIT TARGET + DRAG — small thumb vs. the 24/44px target minimum;
  click-on-track; drag on mouse/touch; the thumb-too-small trap.
- the accessibility critique — sliders are hard to operate precisely for
  motor-impaired and screen-reader users; the paired-number-input escape
  hatch and when a slider is the wrong component entirely.

Also cover, leaning on the substrate rather than re-deriving: the field
label + value association; disabled/read-only; RTL (min/max ends and fill
direction flip); reduced-motion; vertical orientation (rare).

Field-leader systems to survey (web, unless the component is
mobile-first):

- Shopify Polaris
- Adobe Spectrum (React Aria Slider)
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
2. Anatomy and parts — structural model (track, fill, thumb(s), ticks,
   value label), named parts, slot vocabulary.
3. Properties / API — converged prop set; divergences with reasoning
   (min/max/step, value scalar vs. tuple for range, marks, value
   formatting).
4. States and variants — runtime states (rest / hover / focus-visible /
   dragging / disabled / read-only / error) vs. intentional variants
   (single / range, with-ticks, with-input, orientation); canonical
   matrix.
5. Usage guidance — when to use, when not to use, what to use instead
   (including the slider-vs-number-field decision).
6. Accessibility — component-specific concerns. The reader has read
   14-accessibility, 17-accessibility-annotation-contract, and
   28-web-accessibility-implementation; do not re-state the theory;
   identify what is specific to this component (role=slider,
   aria-valuenow/min/max/valuetext, the keyboard model, per-thumb
   labelling, the precision/motor-impairment critique, the WCAG SC it
   participates in).
7. Content guidelines — labels, value formatting, min/max labels,
   units.
8. Motion and transition — thumb/fill movement, snapping, the
   reduce-motion contract.
9. Internationalization — RTL (min/max + fill direction), locale value
   formatting, text expansion of labels.
10. Naming — Slider vs. RangeSlider; the practice's default; aliases.
11. Implementation notes — framework-specific gotchas (controlled value,
   drag + pointer events, the thumb-measurement/track-geometry math,
   the paired-input sync), prop-vs-slot decisions, headless-vs-opinionated
   tension.
12. Related and alternative components — typed relationships (composes
   with / alternative to / supersedes / superseded by), incl. NumberField
   and the slider+input composite.
13. Field POV evolution — how the leading systems' position has changed;
   recent shifts worth flagging.
14. Sources cited — every system referenced, with version dates.
15. Agent-consumable schema — a fenced YAML block representing the
   brief's structured content as the practice's opinionated `.ai.json`
   shape for this component. Free-form values, but follow the locked key
   order and conventions in components/_schema.md (identity, description,
   [anatomy], api, states, variants, accessibility, content, [motion],
   [i18n], [implementation], composition, notes; use inherits: for the
   shared form-field substrate; flag unverified claims under
   notes.unverified). Represent the single-vs-range model explicitly.
   The schema must not contradict any prose section above; if it does,
   the prose wins.

Output format: Structured markdown. Use H2 headings that match the
numbered spine above. Synthesize findings — do not list sources
mechanically. Where the field has consensus, state it clearly; where
decisions are context-dependent, provide decision frameworks rather than
declaring a winner. Where claims depend on current platform state — feature
names, version flags, ARIA attributes that recently changed — date them
and note the verification path.

Depth: Expert audience. Do not explain what a slider is or that it picks
a value in a range — explain the single-vs-range model, the step/tick and
value-formatting decisions, the keyboard and aria-valuetext contract, the
slider-vs-number-field precision boundary, and the hit-target/drag traps
that field leaders still disagree on.

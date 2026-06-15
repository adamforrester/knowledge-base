---
okf_version: "0.1"
type: practice-area
title: Component Briefs
description: Field-truth studies of individual components — how the leading systems handle them, where they converge, where they diverge, and the practice's defaults. Upstream of the per-component docs page (29) and the practice's POV on the component model (03).
tags: [index, components]
timestamp: 2026-06-15
---

# Component Briefs

A flat catalogue of per-component field-truth briefs. Each brief is a single component's study — what the leading systems converge on, where they diverge, and where the practice lands by default. Briefs are the upstream artefact a real engagement uses to populate its per-component docs page (see 29-per-component-documentation-template) and to seed its component data file (see 30-generated-from-data-documentation §15 schemas). The catalogue is the practice's opinionated default; the engagement's reality overrides where it has to.

---

## How this catalogue works

**Platform scope.** The catalogue is web-primary with mobile as a reference dimension. The web is the authoritative API surface — properties, accessibility, and implementation are written against HTML/ARIA/React; mobile systems (Apple HIG, Material 3 Compose, Fluent) are cited only where a component genuinely diverges on touch or native behaviour. This is a deliberate commitment: most agency DS work is web-first and the `.ai.json` seed comes off the web API surface. A standing native-API section or a platform-agnostic abstraction is a future decision, not the current shape.

**Brief shape.** Every brief follows a 15-section spine: framing, anatomy, properties/API, states and variants, usage guidance, accessibility, content guidelines, motion, internationalization, naming, implementation notes, related and alternative components, field POV evolution, sources cited, and an embedded agent-consumable schema. Sections scale to component complexity — a brief on `Button` will be longer than a brief on `Divider`, and that is correct. Voice and depth match the numbered files: prose-led, opinionated, citations to real systems with version dates.

**Research workflow.** Briefs use the existing `_research/` dual-agent workspace with a purpose-built prompt template at `_research/_component-prompt-template.md`. Dual-agent is the default for any component where the field is contested; claude-only is allowed for components where the field genuinely converges (Divider, Spinner, simple primitives). The choice is recorded by the contents of the research folder — presence of `external-agent.md` means dual-agent, absence means claude-only.

**Synthesis path.** Default is direct from raw outputs into `components/<slug>.md`. The brief itself is the synthesis. An intermediate `_research/_synthesis/` file is used only when dual-agent outputs diverge enough to need explicit reconciliation.

**Promotion.** When a brief lands: update its entry in this index from "not yet briefed" to a link with one-line hook and status flag; add inline cross-references from the numbered files where the component is now relevant (03 always; 14 / 17 / 28 / 16 / 18 / 13 / 04 / 25 / 30 conditionally); leave the `_inbound/` folder in place as audit record.

**The §15 schema.** Section 15 of every brief is a fenced YAML block — the practice's opinionated default `.ai.json` shape for the component. The schema is a structured projection of the prose, not a parallel artefact; if section 3 says `tone: neutral | critical | success`, the schema says the same thing in machine-consumable form. The first six briefs used free-form YAML so the shape could stabilise through real use; it has now been **formalised** — see `_schema.md` for the locked key order, the ALWAYS/SCALES rule, and the `inherits:` / `notes.unverified` conventions, to which every brief conforms. Keys and ordering are locked; values stay free-form prose.

**Intake.** Engagement need pulls a brief forward. The seed target list below covers ~40 components across the seven categories. The list is the discipline; the order is the flexibility. Components without briefs are listed with a `scope:` note describing what the brief will cover.

---

## The catalogue

### Foundations

- **[Icon](icon.md)** — a primitive with two load-bearing decisions, meaningful-vs-decorative and how the set is delivered: the decorative-by-default accessible-name matrix (`aria-hidden` unless meaningfully standalone), the icon-only-button trap (the Icon is never the interactive node — the wrapping Button is), the geometric/optical anatomy, the `currentColor` model, the delivery trade (inline-SVG default; legacy icon fonts dead; variable WOFF2 a legitimate modern path for multi-axis sets), and the set-as-versioned-API deprecation/codemod problem. *stable* — promoted from claude-only to a **dual-agent** run; the second pass reopened the delivery question the solo brief had flattened.
- **Avatar** — *not yet briefed.* `scope: image vs. initials vs. fallback, group/stack composition, accessible name patterns, presence-indicator overlay.`
- **Badge** — *not yet briefed.* `scope: count vs. dot vs. status, the announcement contract, placement relative to host, color-as-sole-carrier failure.`
- **Tag** — *not yet briefed.* `scope: chip vs. tag vs. pill terminology, removable vs. static, multi-select interaction model, the tag-vs-badge boundary.`
- **[Divider](divider.md)** — the catalogue's thinnest component and sharpest accessibility test: the decorative-vs-semantic separator decision (`aria-hidden` by default, `role="separator"` only for true thematic breaks), the vertical-divider height trap, the inset model, the labelled "OR" divider, and the divider-versus-spacing judgment. *stable* — the catalogue's first claude-only brief; proves depth scales to the component (states and motion sections collapse, by design).
- **Spinner** — *not yet briefed.* `scope: indeterminate vs. determinate, when to use vs. skeleton, accessible loading announcement, the reduce-motion contract.`
- **Skeleton** — *not yet briefed.* `scope: shape-matched vs. block placeholders, animation discipline, accessibility (aria-busy on parent, hidden from AT), the spinner-vs-skeleton decision.`

### Layout

- **Box** — *not yet briefed.* `scope: the polymorphic primitive, prop-driven vs. style-driven, the as-prop contract, the box-as-escape-hatch trap.`
- **Stack** — *not yet briefed.* `scope: vertical vs. horizontal, gap vs. margin, divider-between, the alignment-and-justification matrix.`
- **Grid** — *not yet briefed.* `scope: container queries vs. viewport queries, named-track vs. auto-flow, the 12-column legacy, responsive prop shapes.`
- **Card** — *not yet briefed.* `scope: header / body / footer slot model, interactive-card vs. card-with-actions, the link-on-card-vs-button-in-card decision, elevation tokens.`
- **Section** — *not yet briefed.* `scope: structural vs. visual section, the heading-level contract, landmark roles, full-bleed vs. constrained.`

### Form

- **[Button](button.md)** — the action trigger, not navigation: the two-axis intent + appearance model over a single overloaded variant enum, the link-vs-button boundary, native-disabled vs. focusable-inactive, and the delayed-spinner / width-preserving loading contract. *stable* — the catalogue's calibration brief.
- **[Text Field](text-field.md)** — the data-capture primitive where accessibility, validation, and composition collide: bundled-props vs. composed-slots resolving to a hybrid, the graduated typed-family split (NumberField separate; email/url/tel as type+attrs), placeholder-is-not-a-label with static top labels, read-only ≠ disabled, the aria-describedby chain and the polite character counter, and presentational-by-default validation. *stable* — the second brief; calibrates the encapsulation-boundary and accessibility-wiring axis.
- **[Textarea](textarea.md)** — Text Field's multi-line sibling, where ~80% is the shared form-field substrate and the contested 20% is the sizing model: distinct component over a multiline prop, `resize` vertical-by-default (never horizontal) with auto-grow for composers, `rows` as line-count, soft over hard `maxLength` counted by grapheme, the threshold-based polite counter, Enter-as-newline with submit-on-Enter as an opt-in, and `field-sizing: content` retiring the ghost-sizer. *stable* — the third brief; calibrates the sizing model and the inherited-substrate discipline (the first brief to stand explicitly on another).
- **[Select](select.md)** — the form component where accessibility ideals collide hardest with styling ambitions, and the first whose core is contested at the *platform* level: the native-vs-custom decision (a framework, not a winner), the select-vs-combobox boundary (type-ahead vs. destructive filtering), the multi-select token/count models with mandatory option checkboxes, the `aria-activedescendant` focus contract (DOM focus stays on the trigger), and the Popover API / CSS Anchor Positioning / `appearance: base-select` platform shift that is collapsing the whole native-vs-custom trade. *stable* — the fifth brief; calibrates the native-vs-custom decision and writing durably across a moving platform.
- **[Combobox](combobox.md)** — the hardest widget in ARIA, and the first brief to stand on two substrates at once (the text-field form-stack and select's overlay/listbox machinery): the defining destructive filter, the two-state model (`inputValue` vs. `value`) as the core reconciliation problem, `aria-autocomplete=list` default, strict-vs-free-text, async debounce + `AbortController` race handling, the multi-select token-vs-checkbox split, and the ARIA 1.2 pattern (role on the input, not the deprecated 1.0 wrapper). *stable* — the seventh brief; calibrates the two-state reconciliation and standing on two inherited substrates.
- **[Checkbox](checkbox.md)** — the catalogue's decomposition calibration: the same control at three granularities (atomic box, labelled row, group) resolved to a **two-component surface** — `Checkbox` + `CheckboxGroup` — plus an exposed `Checkbox.Control` primitive (the text-field hybrid applied to a control); the indeterminate-as-DOM-property mechanic, the whole-row hit target, `role=group` over `fieldset`, the Tab-each-vs-arrow-within difference from radio, and the staged-vs-immediate checkbox-vs-switch boundary. *stable* — the eighth brief; establishes the selection-control decomposition that Radio (group mandatory) and Switch (no group) refine.
- **[Radio](radio.md)** — the Checkbox decomposition with one mutation: the group is **mandatory** (a lone radio is meaningless; `RadioGroup` owns `name` + single value + validation). Confirms the inherited control/group/`Radio.Control` model, resolves the roving-tabindex single-tab-stop keyboard model and the contested selection-follows-focus question (practice: follows-focus, native-aligned, with explicit-selection as a documented opt-out), and covers no-deselect + the explicit "None", start-empty default selection, and the radio-vs-segmented-control / radio-vs-select boundaries. *stable* — the ninth brief; refines the selection-control decomposition (mandatory group).
- **[Switch](switch.md)** — the control that closes the selection-control decomposition arc: **no group** (checkbox optional, radio mandatory, switch none). The immediate-effect contract (the staged-vs-immediate boundary from the switch side), the async/optimistic-update model (optimistic default + a first-class pending/loading lock), `role=switch` distinct from checkbox and `aria-pressed`, the label-leading settings-row pattern, supported read-only, and describe-the-setting (not the state) labels. *stable* — the tenth brief; completes the boolean/choice batch.
- **Slider** — *not yet briefed.* `scope: single-thumb vs. range, step model, keyboard increment, value-display pattern, the slider-vs-input decision.`
- **Date Picker** — *not yet briefed.* `scope: input vs. calendar, single vs. range, locale and RTL, the masked-input contract, accessibility patterns.`
- **File Upload** — *not yet briefed.* `scope: drag-and-drop vs. browse, multi-file, progress and error handling, accessibility, the file-list slot model.`
- **Form (composite)** — *not yet briefed.* `scope: the form as compositional unit, validation strategies, error summary pattern, submit-and-recovery flow, autofill contract.`

### Navigation

- **Link** — *not yet briefed.* `scope: link vs. button semantics, internal vs. external, visited state, focus visibility, the underline-discipline.`
- **Tabs** — *not yet briefed.* `scope: ARIA tabs pattern, manual vs. automatic activation, panel association, scroll/overflow handling, vertical orientation.`
- **Breadcrumbs** — *not yet briefed.* `scope: separator semantics, current-page convention, truncation/overflow, the breadcrumb-vs-back-button decision.`
- **Pagination** — *not yet briefed.* `scope: numbered vs. load-more vs. infinite, current-page announcement, the truncation pattern, accessibility.`
- **Menu** — *not yet briefed.* `scope: ARIA menu pattern, submenu navigation, the menu-vs-listbox-vs-combobox confusion, click-outside dismissal, focus management.`
- **Side Navigation** — *not yet briefed.* `scope: collapsed vs. expanded, multi-level structure, the active-state contract, mobile transformation, accessible landmark.`

### Feedback

- **Toast** — *not yet briefed.* `scope: role="status" vs. role="alert", auto-dismiss timing, queue behaviour, the accessible-name vs. body distinction, action-in-toast pattern.`
- **Banner / Alert** — *not yet briefed.* `scope: severity model, dismissibility, the inline-banner vs. page-banner distinction, action affordances, accessibility.`
- **Progress** — *not yet briefed.* `scope: determinate vs. indeterminate, accessible value announcement, the progress-vs-spinner decision, multi-step progress.`
- **Empty State** — *not yet briefed.* `scope: illustration / heading / body / action structure, the empty-vs-error vs. empty-vs-loading boundaries, content patterns.`
- **Inline Message** — *not yet briefed.* `scope: error vs. info vs. success, association with form fields, the live-region vs. static decision, content patterns.`

### Data

- **Table** — *not yet briefed.* `scope: column model, sort/filter/select, sticky headers, responsive transformation, virtualisation, accessibility patterns, the table-vs-list decision.`
- **List** — *not yet briefed.* `scope: ordered vs. unordered semantics, list-with-actions, the list-vs-table decision, virtualisation.`
- **Tree** — *not yet briefed.* `scope: ARIA tree pattern, multi-select, expand/collapse model, virtualisation, the tree-vs-nested-list decision.`
- **Chart (composite)** — *not yet briefed.* `scope: encoding rules, color-not-sole-carrier, axis and legend conventions, accessible name and description templates, sonification/table-fallback. (See 09-gaps-and-open-questions §5.2.)`

### Overlay

- **Dialog / Modal** — *not yet briefed.* `scope: focus-trap and return, inert scope, Escape and overlay-click behaviour, native <dialog>+showModal(), z-index and scroll-lock, the modal-vs-drawer decision.`
- **Drawer** — *not yet briefed.* `scope: edge-anchored placement, the drawer-vs-modal-vs-popover decision, focus management, mobile vs. desktop.`
- **Popover** — *not yet briefed.* `scope: trigger model, positioning (Floating UI / popover API), dismissibility, the popover-vs-tooltip-vs-menu boundaries.`
- **Tooltip** — *not yet briefed.* `scope: hover/focus trigger, the WCAG 1.4.13 contract, persistence and dismissibility, the tooltip-as-only-affordance anti-pattern.`

---

## Status flags

- *not yet briefed* — entry exists, no research run
- *draft* — `_research/_inbound/` folder exists, brief in `_synthesis/` or being authored
- *stable* — brief lives in `components/<slug>.md` and reflects current field state
- *superseded* — replaced by another brief; superseding slug noted inline

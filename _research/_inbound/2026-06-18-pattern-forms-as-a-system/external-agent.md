# Forms-as-a-system — external-agent pass

*Second independent pass for the Forms-as-a-system pattern brief. Captured verbatim as the dual-agent audit record. Synthesised with `claude.md` into `patterns/forms-as-a-system.md`.*

---

## Forms-as-a-system

A form control is merely a vessel for a scalar value; a form system is the topological orchestration of those values across time, state, and user intent. The boundary drawn by modern practice is definitive: the Form component provides the semantic DOM primitive, while the Forms-as-a-system pattern dictates the choreography of validation timing, error focus management, progressive disclosure, and persistence logic that no individual input can govern alone. It is the architectural framework that prevents dozens of localized controls from devolving into a chaotic, thrashing user experience.

### Problem & Context

The enterprise digital landscape suffers from systemic dissonance when development teams treat forms simply as a vertical stack of isolated input components. When inputs operate as ignorant, self-contained islands of state, the resulting interface inevitably degrades. A text field might validate aggressively on every keystroke, punishing the user before they have finished typing, while an adjacent dropdown waits entirely until submission to reveal its error state. Dynamic fields appear abruptly, shifting layouts and causing users to lose their visual anchor, while screen reader users are left entirely unaware of critical validation failures because live regions were not orchestrated at a macro level.

This fragmentation occurs because individual atomic components (such as a Text Field, Select, or Checkbox) are fundamentally unaware of the wider context. They manage their own internal focus and hover states, but they lack the capacity to coordinate cross-field dependencies, global submission states, or layout rhythms. The Forms-as-a-system pattern exists to unify these behaviors, establishing the definitive rules for when validation fires, how errors are aggregated, how the DOM announces structural changes to assistive technologies, and when a form has grown too complex to remain a single continuous scroll.

Design systems frequently diverge on how to solve this orchestration problem because they index on fundamentally different constraints. Systems like the GOV.UK Design System prioritize absolute cognitive accessibility and high completion rates across the entire population, leading to strict paradigms like one-thing-per-page, explicit submit validation, and highly verbose error summaries. Conversely, enterprise SaaS systems such as IBM Carbon, Shopify Polaris, and Atlassian deeply utilize dense layouts, inline validation, and complex dependency graphs to optimize for expert users executing repetitive, high-frequency data-entry tasks. Resolving these divergences requires establishing strict decision rules based on audience cognitive load and transaction complexity.

### Composition

This pattern composes individual atomic and molecular components into a functional, cohesive data-collection state machine. The pattern does not re-derive the internal specifications of these components—such as their hover states, border radii, or token assignments—but rather dictates their integration parameters and the systemic delta that elevates them into a workflow.

The core composition requires several typed component references to function correctly. The primary shell is the native Form element, augmented with submission interception and novalidate properties to disable inconsistent browser-native validation tooltips in favor of the system's controlled validation UI. Inside this shell, the system orchestrates various Input Controls, including text fields, selects, radio groups, and date pickers. Action execution is handled by Button or ButtonGroup components for primary submission and secondary cancellation workflows. Finally, the system relies heavily on feedback primitives: InlineMessage components bound contextually to specific controls, and an ErrorSummary banner acting as a global alert mechanism that aggregates failures for accessible routing.

What the Forms-as-a-system adds is the logical substrate. While a text input knows how to render a red border when passed an invalid state property, the system decides exactly when and why that property is passed. The system provides the schema validation engine, the form-state context provider, and the accessible focus-management contract that bridges the gap between a validation failure and a user's attention.

### Decision Rules

**1. Validation Timing.** The single most debated aspect. Validating on every keystroke (onChange) creates cognitive thrashing; waiting entirely until submission (onSubmit) delays critical feedback. The definitive practice is the hybrid "Reward early, punish late" paradigm: a pristine field undergoes no validation; first evaluation fires onBlur (punish late); once a field is in error, validation switches to onChange and clears the moment the input becomes valid (reward early). Exceptions: highly sensitive forms / high-cognitive-load audiences rely strictly on onSubmit; character-count-limited fields validate onChange for real-time capacity feedback.

**2. Error Presentation.** A severe bifurcation: purely inline (Material) vs top-of-page summary (GOV.UK). Defensible default is the Dual-Presentation Model. Every invalid field shows an error below the input, linked via aria-describedby; on a failed submission an Error Summary renders at the top aggregating all errors as anchor links; the system programmatically moves focus to the summary container. Clicking a summary link moves focus to the target field. Each invalid field sets aria-invalid="true".

**3. Required vs Optional Marking.** GOV.UK research: users expect all fields required unless stated, hence "(optional)". Carbon's scalable rule: mark the minority. If predominantly required, label only optional fields; if predominantly optional, flag only required. If an asterisk is used, render a descriptive legend.

**4. The Long-Form vs Wizard Threshold.** Forms exceeding ~15–20 fields benefit from being broken into steps. Branching → wizard or one-thing-per-page (prevents reflow chaos). If the user must pause to gather external info, split into steps backed by Save and resume. Public sector / low cognitive capacity → one-thing-per-page.

**5. Field Dependency & Conditional Reveal.** Disabling an irrelevant field is an anti-pattern; the field should be completely unmounted from the DOM (not display:none, not disabled). When revealed dynamically, inject immediately following the trigger control so the next Tab lands naturally on the revealed field.

**6. Cross-Field Validation.** Lift validation logic to a parent schema. Attach the error to the field currently being edited that violates the rule; if holistic, assign to the group container (`<fieldset>`/`<legend>`). Only trigger once all fields in the dependency graph have been touched.

**7. Save Model.** Simple single-session → explicit Submit. Dirty state + navigation away → beforeunload warning or modal. Long-lived forms → implicit Draft autosave to localStorage or API. Multi-step or completion >10 min → debounced autosave.

**8. Layout.** Single-column is the defensible default. Labels top-aligned (left-aligned decouples label/input, reduces scannability). Multi-column permitted only for cohesive clusters (First/Last name; City/State/Zip). Group related fields in `<fieldset>`/`<legend>`.

**9. Repeatable / Array Fields.** "Add another" as a secondary button below the last item; "Remove" inline per row as a subtle/ghost icon button. On add, move focus to the first input of the new row and announce; on remove, return focus to previous row or the Add button (never lose focus to body). (Ant Design ProFormList.)

**10. Submission States.** Do NOT disable the submit button until valid — it provides zero feedback as to why. Keep it interactive; clicking while invalid triggers holistic validation + error summary. On valid submit, enter a pending state with a spinner and aria-disabled="true" to prevent double-submit.

### Flow & States

Pristine → Editing (Dirty, isDirty set, clear errors on change per reward-early) → Validating (onBlur/onSubmit, run schema + cross-field) → Submitting (freeze inputs, prevent navigation, async request, loading button) → Success (clear dirty, route to confirmation) | Partial Failure (map server errors to field paths, render summary, force focus, inline errors).

### Layout & Structure

Strict spatial rhythm. Carbon-style: 2x grid alignment; ~32px between fields, ~48px between sections (tighter 24px only in dense admin tools); top-aligned labels universally; `<fieldset>`/`<legend>` for groups; if a section exceeds viewport height, refactor into wizard steps. Action area: footer-aligned, primary right / secondary left for enterprise SaaS; GOV.UK reverses to primary left (reading order). Multi-column inline fieldsets collapse to single column < 768px.

### Accessibility Orchestration

The cornerstone is the **Error Summary Focus Contract**: on failed validation a global summary appears at the top and JS explicitly moves focus to it, so screen readers announce the failure and the aggregated list. **aria-describedby linkage**: every error message has a unique id; the invalid input receives aria-describedby + aria-invalid="true". **WCAG 2.2 SC 3.3.7 (Redundant Entry)**: never require re-entering info already provided in the session — provide autofill or "Same as billing" mechanisms. **WCAG 2.2 SC 3.3.8/3.3.9 (Accessible Authentication)**: no cognitive-function tests without accessible alternatives (WebAuthn/biometrics, magic links); must support password-manager pasting (preventing paste is an explicit F109 failure). **Dynamic insertion**: announce newly inserted DOM nodes via an aria-live="polite" region.

### Content & Copy

Error messages must be surgical, actionable, blame-free: not "You entered an invalid email" (blame) nor "Invalid input" (vague), but "Enter an email address in the format name@example.com." Labels concise (1–3 words), no trailing colons, not framed as questions unless following GOV.UK conversational one-thing-per-page. Formatting constraints go in persistent helper text. Placeholders never replace labels (they disappear on interaction and commonly fail contrast).

### Variants & Responsive

Standard Page Form (single column, fieldset sections; multi-column collapses < 768px). Wizard (segmented linear, stepper → "Step 2 of 5" on mobile, 100%-width buttons). Side Panel / Drawer (denser; 100% width on mobile). Dialog / Modal Form (3–5 inputs max; never nested scrollbars; if content exceeds viewport, promote to full page; footer-anchored actions).

### Anti-Patterns

Disabled submit buttons for validation; validation on every keystroke (thrashing); placeholder as label; multi-column by default; reset/clear buttons next to submit (accidental catastrophic data loss).

### Related Patterns & Components

- **Form (Component) vs Forms-as-a-system (Pattern):** the component dictates the bare semantic HTML, gap spacing, CSS reset; the pattern dictates the state machine — validation schemas, cross-field resolution, routing, global cognitive orchestration.
- **vs Multi-step wizard (Pattern):** once rules dictate >~15 fields or complex branching, it graduates into the Multi-step wizard pattern (step-routing, inter-step persistence, timeline visualization).
- **vs "Ask users for X" (Recipes):** this pattern is the orchestration shell; specific field arrangements (international Address block, Date of Birth 3-inputs-vs-1) belong to specialized composition recipes.
- **vs Foundations:** the visual styling of read-only/disabled/focus-visible states belongs in Foundations/tokens; this pattern references when to apply them.

### Field POV Evolution

- **Validation architecture:** imperative jQuery/DOM validation → schema-driven (Zod, Valibot) detached from DOM, fed into state managers (React Hook Form). Driver: isomorphic client/server validation + TypeScript inference.
- **Required markings:** universal red asterisk → mark the minority (append "(optional)"). Driver: visual-noise reduction + the expectation that a presented field is necessary.
- **State management:** controlled components (useState on every keystroke) → uncontrolled subscription/proxy renders (TanStack Form, RHF). Driver: performance degradation in large forms.
- **Cognitive loading:** dense accordion forms on one infinite page → strict one-thing-per-page / segmented wizard. Driver: WCAG cognitive guidelines + drop-off analytics.

### Reference Instantiations

- **GOV.UK Design System** — Error Summary routing, "Check your answers", one-thing-per-page.
- **IBM Carbon** — fluid vs default layouts, label alignment, minority-marking.
- **Ant Design (ProComponents)** — ProFormList / ProFormDependency for repeatable, dependent arrays.
- **Atlassian Design System** — @atlaskit/form (Header/Section/Footer) minimizing boilerplate while enforcing alignment.

### Sources Cited (external pass)

Shopify Polaris (form layout, validation alignment); Atlassian @atlaskit/form (changelog, character counters, wrapper/Header/Section/Footer); GOV.UK (one-thing-per-page, check-your-answers, optional-vs-required, turning off HTML5 validation, error-summary focus, v6.2.0 June 2026); Microsoft Fluent / Design System QLD (avoid placeholders, column limits); Material Design 3 (form anatomy, error messages replacing helper text); React Hook Form (Zod integration, aria-invalid mapping, validation modes onSubmit/onBlur/onChange/onTouched, mobile/uncontrolled perf); TanStack Form (headless, array fields, composable conditions); Ant Design ProComponents (ProForm, ProFormList, ProFormDependency); IBM Carbon (login client-vs-server validation, top-aligned labels, fluid-vs-default, 2x grid, cancel-vs-clear, character counters, v11.109.0 June 2026); WCAG 2.2 (3.3.7 Redundant Entry, 3.3.8/3.3.9 Accessible Authentication, F109 paste failure, 4.1.1); "Reward early, punish late" (Filament/Laravel notes, inline-validation UX); form-marking research; accessible error messages (aria-invalid/aria-describedby); React Aria (role="alert", visually-hidden); SEB Design Library (error-summary nav landmark); Shopify Polaris (web-components/Preact migration, 2026-04).

*Note: the external pass's `[cite: N]` markers are retained in the practitioner's source notes; specific version strings (GOV.UK v6.2.0, Carbon v11.109.0, Polaris 2026-04) to be verified.*

### Agent-consumable schema (external pass)

```yaml
identity:
  id: forms-as-a-system
  name: Forms-as-a-system
  aliases: [form-orchestration, multi-field-form, data-collection-shell]
  tier: composition
  goal: ask-for-data
  status: definitive
problem: >
  Forms fail catastrophically when treated merely as a vertical stack of isolated input components. The system must orchestrate cross-component validation timing, layout rhythms, progressive disclosure, and global accessibility contracts (such as WCAG 2.2 focus management) to prevent severe cognitive thrashing and state dissonance among users.
composition:
  requires: [form-primitive, text-field, select, checkbox-group, radio-group, button-group, error-message, error-summary]
decision_rules:
  validation_timing: { if: "field is touched and invalid", use: "reward early (onChange), punish late (onBlur)" }
  error_presentation: { if: "form submission fails", use: "render error summary at top AND programmatically move focus to summary AND render inline errors" }
  required_optional: { if: "required fields > optional fields", use: "mark optional fields exclusively with '(optional)' text" }
  long_form_vs_wizard: { if: "field count > 15 OR high branching logic", use: "multi-step wizard OR one-thing-per-page pattern" }
  field_dependency: { if: "field is conditionally revealed", use: "insert into DOM immediately after trigger (do not use display:none or disabled attributes)" }
  layout: { if: "default rendering requested", use: "single column with top-aligned labels" }
  submission_state: { if: "form contains errors prior to submission", use: "keep submit button enabled to trigger the global error summary; do not disable the button" }
flow: [pristine, editing_dirty, validating, submitting_pending, success_or_partial_failure]
accessibility_orchestration:
  - "WCAG 3.3.7: Do not require redundant entry; utilize robust autofill parameters or 'same as' checkboxes."
  - "WCAG 3.3.8: Do not require cognitive tests for authentication; explicitly allow password pasting."
  - "Focus Management: Force browser focus to ErrorSummary on failed submit events."
  - "Linkage: Utilize aria-describedby to securely link input fields to their respective inline ErrorMessages."
content:
  error_voice: "Actionable, highly specific, and non-blaming (e.g., 'Enter a valid email', not 'Invalid format')."
  labels: "1-3 words maximum, no trailing colons. Rely on helper text, never placeholders, for critical instructions."
variants: [single_scroll_page, multi_step_wizard, side_panel, dialog_modal]
anti_patterns: [disabling_submit_pre_validation, validating_on_every_keystroke_initially, placeholder_as_label, multi_column_desktop_defaults, reset_buttons_next_to_submit]
relations:
  composes: [form-primitive, input-controls, buttons]
  relates-to: [multi-step-wizard, complex-data-recipes]
  boundary: "The atomic component defines the localized DOM; the system defines the macro state machine and cognitive orchestration."
notes:
  contested: "Asterisk versus (optional). Resolved by Carbon's mathematical rule: mark the minority."
  unverified: "The optimal threshold exact field count for wizard conversion varies heavily by audience cognitive capacity and context."
  secondary-tier: "Cross-field validation schemas requiring group-level fieldset hoisting."
```

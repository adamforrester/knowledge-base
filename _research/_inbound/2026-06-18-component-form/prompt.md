You are researching the Form component for a senior design systems
practitioner at a digital agency. The output is a field-truth study of how
the leading design systems handle this component — what they converge on,
where they diverge, and what the practice's opinionated default should be
when starting from scratch.

This is not an introductory guide. Assume the reader knows what a form is,
knows what a design system is, and has shipped multiple component libraries.
Explain the non-obvious — the choices field leaders disagree on, the
accessibility decisions still contested, the implementation traps that recur
across codebases.

Form is THE COMPOSITIONAL OWNER OF THE FORM CATEGORY — the component that
CLOSES the Form category by being the orchestrator the individual controls
plug into. It is the last Form brief, after the controls (Text Field,
Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker,
File Upload) and the field-level feedback (Inline Message).

CRITICAL SCOPE BOUNDARY — KEEP THIS BRIEF COMPONENT-SHAPED, NOT PATTERN-
SHAPED. There is a real component-vs-pattern duality here, and this brief
takes the COMPONENT side deliberately:
- THE COMPONENT (this brief): the Form PRIMITIVE — the <form> element + the
  submission contract, the validation ORCHESTRATION (the form-level strategy
  that coordinates the fields' own validation), the error-SUMMARY pattern,
  the field/submit wiring (the FormField/Field wrapper, the submit Button +
  its pending state), the layout/grouping (single-column, Fieldset/legend),
  and the autofill contract. A concrete, briefable compositional unit.
- THE PATTERN (explicitly OUT of scope — forward-reference to the patterns
  layer): Forms-as-a-system — the multi-step wizard, the long-form/multi-
  section flow, save-and-resume, the broader cross-page form UX. Name it as
  the boundary and DON'T resolve it here; it is the first big item of the
  coming patterns layer.

It STANDS ON / COMPOSES the briefed substrates — DON'T re-derive them:
- IT COMPOSES ALL THE FORM CONTROLS (Text Field, Select, Combobox, Checkbox,
  Radio, Switch, Slider, Date Picker, File Upload) — it is the orchestrator
  they plug into; the field-stack/aria-describedby chain is Text Field's
  (components/text-field.md).
- IT BUILDS ON INLINE MESSAGE (components/inline-message.md): the field-level
  error IS Inline Message (the field's own slot); the FORM-level error
  SUMMARY is the form's own live-region/landmark concern — Inline Message
  already settled that field-level live regions are abandoned in favour of
  aria-describedby + focus, with the live region surviving only at the
  form/summary level. Resolve the error summary as exactly that surviving
  form-level surface.
- IT COMPOSES BUTTON (the submit / reset — components/button.md) and its
  loading/pending state (the submit lock); and the Inline Message / Banner
  for the form-level success/error (components/banner.md).

THE DEFINING FORM-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE VALIDATION-STRATEGY / WHEN-TO-VALIDATE CRUX (the headline): the
  escalation model the field settled on — validate on SUBMIT first, then
  on BLUR for a field that's been touched, then on CHANGE only once a field
  is already in error (the "reward early, punish late" / "validate on submit,
  re-validate on change" model — Inline Message drew the field side; resolve
  the form-level orchestration). PLUS the schema-driven validation reality
  (Zod / Yup / Valibot schemas + the form engines — react-hook-form / Formik
  / TanStack Form / Final Form / React Aria) vs the native Constraint
  Validation API; and the CLIENT-vs-SERVER validation split (client is UX,
  server is truth — the same boundary File Upload drew for files; the server
  error must map back onto the fields).
- THE ERROR-SUMMARY + FOCUS-MANAGEMENT PATTERN (the a11y crux): the GOV.UK
  error-summary pattern — on a failed submit, render a summary at the top of
  the form listing each error as a link to its field, MOVE FOCUS to the
  summary, and announce it; each summary link jumps focus to the offending
  field. Resolve the focus-on-submit-with-errors contract (focus the summary,
  not the first field, per GOV.UK), the field-level error association
  (aria-describedby + aria-invalid — inherited from Text Field / Inline
  Message), and the required/optional marking decision (mark optional, or
  mark required consistently — never neither).
- THE SUBMISSION LIFECYCLE + PROGRESSIVE ENHANCEMENT (the submit crux): the
  submit state machine (idle -> submitting [the pending lock + the Button
  loading state, prevent double-submit] -> success | error), the
  preserve-entered-data-on-error rule, and the native-<form>-first /
  progressive-enhancement reality (the form works without JS via a native
  submit; JS enhances it) — INCLUDING the modern platform shift: React 19
  form Actions / useActionState / useFormStatus, and Server Actions
  (Next / Remix). Resolve the submit contract + the implicit submit (Enter
  in a single-field form) + multiple submit buttons (formaction).
- THE FIELD/LAYOUT MODEL: the FormField/Field wrapper (the composition
  primitive that wires label + control + helper + error — the bundled-vs-
  composed tension Text Field settled, now at the form level), the
  single-column-layout finding (the canonical forms-UX default; when 2-column
  is acceptable), field grouping (Fieldset/legend for radio/checkbox groups +
  related fields), label placement (top-aligned default — from Text Field),
  and the field spacing/rhythm (the Stack lineage).
- THE AUTOFILL / autocomplete CONTRACT: the autocomplete token list
  (name / email / tel / street-address / postal-code / cc-* / one-time-code /
  new-password / current-password), why it matters (WCAG 1.3.5 Identify Input
  Purpose + faster completion + password-manager interplay), and the traps
  (autocomplete=off is mostly ignored / harmful; the password-manager icon
  overlap).
- THE UNSAVED-CHANGES / RECOVERY GUARD: the dirty-form beforeunload / route-
  change guard, scroll-to-error, and the submit-error recovery (don't lose
  the user's input).

Field-leader systems to survey (web): WAI-ARIA APG + the GOV.UK Design System
(the gold-standard accessible-forms guidance + the error-summary pattern),
React Aria (the Form component + native validation behaviors + the
ValidationResult model), react-hook-form (+ the resolver model for
Zod/Yup/Valibot), Formik, TanStack Form, Final Form, the schema libraries
(Zod / Yup / Valibot), React 19 (form Actions / useActionState /
useFormStatus), Next.js / Remix Server Actions, the native Constraint
Validation API + the autocomplete spec (WHATWG HTML), IBM Carbon (Form /
FormGroup), Shopify Polaris (Form), Ant Design (Form — the rules/validation
model, the most feature-complete), Microsoft Fluent, MUI. Cite each with a
version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; Form COMPOSES the controls + Button + Inline Message;
builds on Inline Message's field-error + form-level-live-region split; flag
the Forms-as-a-system PATTERN as out-of-scope/forward-referenced; flag
unverified/volatile platform claims (React 19 / Server Actions) under
notes.unverified).

1. Framing — what it is (the compositional owner — the <form> primitive +
   the validation orchestration + the submission contract + the error summary)
   and what it isn't (a single control; the field-level error — that's Inline
   Message; the multi-step WIZARD / Forms-as-a-system — that's the PATTERN,
   forward-referenced); the validation-strategy + the error-summary + the
   progressive-enhancement crux up front; why systems disagree; THE COMPONENT-
   VS-PATTERN BOUNDARY stated explicitly.
2. Anatomy and parts — the <form> element, the FormField/Field wrappers (label
   + control + helper + error), the field groups (Fieldset/legend), the error
   summary (top-of-form), the form-level success/error message (Banner/Inline
   Message), the submit/reset Button(s) + the pending state, the required/
   optional marking.
3. Properties / API — onSubmit, the validation strategy/mode (onSubmit/onBlur/
   onChange/onTouched), the schema/resolver, the field-registration model,
   defaultValues, the submit/pending/error state, server-error mapping,
   the native vs controlled model, the autofill wiring.
4. States and variants — the form (idle / validating / submitting / success /
   error); the field (pristine/touched/dirty/valid/invalid); the submit Button
   (enabled/pending/disabled); single-column vs multi-column; inline vs
   stacked; the read-only/disabled whole-form.
5. Usage guidance — when a Form (multiple fields + a submit + validation
   orchestration) vs a single auto-saving field vs a Filter set (no submit);
   single-column default + when 2-column; required-vs-optional marking; the
   submit-button-disabled-until-valid debate (don't — it hides why); when to
   reach for the WIZARD pattern (forward-reference).
6. Accessibility — the error-summary + focus-on-submit (GOV.UK), the field
   error association (aria-describedby + aria-invalid — inherited), the
   required/invalid announcement, the Fieldset/legend grouping, the
   submit-feedback live region (the surviving form-level live region from
   Inline Message), the implicit-submit + the keyboard contract; WCAG SCs
   (3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 1.3.5, 4.1.3).
7. Content guidelines — the label/helper/error copy (inherited), the
   error-summary copy, the required/optional indicator, the submit-button
   label (specific verb, not "Submit"), the success confirmation copy, the
   legend/group headings.
8. Motion and transition — the error-summary appearance + scroll, the field
   error reveal (inherited from Inline Message — layout-shift), the submit
   pending transition, the success transition, reduce-motion.
9. Internationalization — the label/error/summary translation, RTL (the field
   layout + the required marker + the error summary mirror), the field-order
   /address-format locale variance (name order, address fields), the
   autocomplete-token locale, the validation-message locale.
10. Naming — Form / FormField / Field / FormGroup / Fieldset / FormControl;
    the wrapper-vs-orchestrator naming; the practice's default; aliases.
11. Implementation notes — native <form> + progressive enhancement (works
    without JS) + React 19 Actions / useActionState / useFormStatus + Server
    Actions; the form-engine choice (react-hook-form + a Zod resolver, vs
    React Aria native validation, vs controlled Formik); the validation
    escalation (submit -> blur-when-touched -> change-when-errored); the
    server-error-to-field mapping; the error-summary + focus + scroll-to-error;
    the prevent-double-submit + the pending lock; the dirty-form unsaved-changes
    guard; the autocomplete tokens; the uncontrolled-vs-controlled performance
    (re-render cost) trade.
12. Related and alternative components — typed relationships (COMPOSES all the
    form controls + Button + Inline Message; builds on Inline Message's
    field-error/form-summary split + Text Field's field-stack; BORDERS the
    Forms-as-a-system PATTERN [the wizard/multi-step — forward-reference];
    the Filter set [fields without a submit] alternative).
13. Field POV evolution — the native <form> -> the controlled JS form
    (Formik) -> the uncontrolled/performance turn (react-hook-form) + schema
    validation (Zod) -> the platform reclaiming it (React 19 Actions / Server
    Actions / progressive enhancement) -> the accessible error-summary
    standardizing (GOV.UK); the validation-strategy settling (reward early,
    punish late).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what a form is — explain the
validation-strategy / when-to-validate escalation (and the schema/engine vs
native-Constraint-Validation reality), the error-summary + focus-management
pattern (GOV.UK), the submission lifecycle + progressive enhancement (the
React 19 Actions / Server Actions shift), the field/layout model (the
FormField wrapper + the single-column finding), the autofill/autocomplete
contract, and the component-vs-pattern boundary (this is the COMPONENT; the
multi-step wizard / Forms-as-a-system is the PATTERN) that field leaders and
design systems draw differently.

# Form — field-truth study (Claude pass)

## 1. Framing
A Form is the **compositional owner of the Form category** — the `<form>` primitive plus the orchestration that turns a set of independent controls into a single submittable, validatable unit. It is the **last Form brief**, the orchestrator every prior control plugs into (Text Field, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload), and it **closes the Form category**. Its job is the *coordination* layer: the submission contract, the form-level validation strategy that sequences the fields' own validation, the error summary, the field/submit wiring, the layout, and the autofill contract.

**The component-vs-pattern boundary (stated up front, deliberately).** There is a real duality here, and this brief takes the **component** side:
- **The component (this brief):** the Form *primitive* — the `<form>` + the submit contract, the validation *orchestration*, the error *summary*, the FormField/Field wrapper, the submit Button + its pending state, the single-column layout + Fieldset grouping, and the autocomplete contract. A concrete, briefable compositional unit.
- **The pattern (out of scope — forward-referenced to the patterns layer):** **Forms-as-a-system** — the multi-step **wizard**, the long multi-section flow, save-and-resume, the cross-page form UX. Named here as the boundary, *not* resolved — it is the first big item of the coming patterns layer.

Three decisions define the component:
- **The validation-strategy / when-to-validate crux (the headline).** The escalation the field settled on: validate **on submit** first, then **on blur** for a touched field, then **on change** only once a field is already in error ("reward early, punish late" — Inline Message drew the field side; the Form orchestrates it across all fields) (§6/§11).
- **The error-summary + focus-management pattern (the a11y crux).** On a failed submit, render a summary at the top listing each error as a link to its field, **move focus to the summary**, and announce it (the GOV.UK pattern). This is the **surviving form-level live region** Inline Message pointed to (field-level live regions abandoned; the summary is where it lives) (§6).
- **The submission lifecycle + progressive enhancement (the submit crux).** The submit state machine (idle → submitting [the pending lock + the Button loading state, prevent double-submit] → success | error), the preserve-data-on-error rule, and the **native-`<form>`-first** reality — the form works without JS, JS enhances it (React 19 form Actions / `useActionState` / `useFormStatus`; Server Actions) (§11).

What it *isn't*: a single control (the Form owns *coordination*, not a value), the field-level error (that's **Inline Message** — see inline-message), or the multi-step **wizard / Forms-as-a-system** (the **pattern**, forward-referenced). Why systems disagree: the validation engine/strategy, the controlled-vs-uncontrolled model, the submit-disabled debate, and where the component ends and the pattern begins.

## 2. Anatomy and parts
- **the `<form>` element** — the real container: the `onSubmit`/`action`, the implicit-submit (Enter in a single text field), the native submit semantics (§11).
- **the FormField / Field wrappers** — the composition primitive wiring **label + control + helper + error** for each field (the bundled-vs-composed tension Text Field settled — see text-field — now at the form level, generalised to wrap *any* control).
- **the field groups** — **Fieldset + legend** for related fields and for radio/checkbox groups (the group's accessible name — see checkbox, radio).
- **the error summary** — a top-of-form block (on failed submit) listing each error as a **link to its field**; the focus target (§6).
- **the form-level message** — a **Banner / Inline Message** for the whole-form success/error ("Your changes were saved" / "Something went wrong") — distinct from the per-field errors (see banner, inline-message).
- **the submit / reset Button(s)** — the **submit Button** + its **pending state** (the loading lock — see button, spinner); reset is rare/discouraged; multiple submits via `formaction` (§11).
- **the required/optional marking** — a consistent indicator (mark optional, or mark required — never neither — §5).
- **the field layout** — single-column by default, with the Stack rhythm (see stack); Fieldset grouping for sections.

## 3. Properties / API
- **`onSubmit(values)`** / **`action`** — the submit handler (controlled) or the native/Server Action (progressive enhancement — §11).
- **the validation `mode`** — `onSubmit` / `onBlur` / `onChange` / `onTouched` / `all` (react-hook-form's vocabulary); the practice default escalates submit → blur(touched) → change(errored) (§11).
- **the `schema` / `resolver`** — a Zod/Yup/Valibot schema via a resolver (react-hook-form), or React Aria's native `validate` + the `ValidationResult` model, or the native Constraint Validation API (§11).
- **the field-registration model** — `register`/`Controller` (react-hook-form), `<Field>` (Formik/TanStack), or React Aria's native form integration.
- **`defaultValues`** — the initial values (uncontrolled-friendly).
- **the submit/pending/error state** — `isSubmitting` / `isValid` / `isDirty` / `errors` / `isSubmitSuccessful` (the form state machine — §4).
- **server-error mapping** — `setError(field, ...)` to map a server-returned error back onto the offending field (client is UX, server is truth — §11).
- **the native-vs-controlled model** — uncontrolled (native form data / refs — performance) vs controlled (every keystroke in state — Formik; the re-render cost — §11).
- **the autofill wiring** — the `autocomplete` tokens per field (§9/§11).
- **what it withholds** — the Form doesn't reinvent the controls (it composes them) or the field-level error (Inline Message); it adds the orchestration + the submit + the summary + the layout.

## 4. States and variants
- **The form states:** **idle** / **validating** / **submitting** (the pending lock — the submit Button loading, inputs optionally locked, double-submit prevented) / **success** / **error** (the summary + the field errors).
- **The field states (orchestrated, not owned):** pristine / **touched** / **dirty** / valid / **invalid** — the Form tracks these to drive the validation escalation (§11).
- **The submit Button states:** enabled / **pending** (loading) / disabled (the disabled-until-valid debate — §5).
- **Variants:**
  - **layout:** single-column (default) / multi-column (dense, related short fields) / inline (a single-row mini-form — search, a quick add).
  - **density / grouping:** flat / Fieldset-grouped sections.
  - **the whole-form** read-only / disabled (during submit).
  - **the submit model:** native (progressive enhancement) / controlled JS / Server Action.

## 5. Usage guidance
- **Use a Form for:** a set of fields the user fills and **submits together** with validation orchestration (a sign-up, a checkout step, a settings page, a create/edit record). The Form is the coordination unit.
- **Form vs the alternatives:**
  - **vs a single auto-saving field** — a settings toggle or an inline-edit field that saves *immediately* on change isn't a Form-submit; it's a control with its own optimistic-update (see switch). No submit, no summary.
  - **vs a Filter set** — filters apply *as you change them* (no submit button, no validation summary); a Filter set is a coordination of controls without the Form's submit contract (the Filtering *pattern* — forward-reference).
- **Single-column by default.** The canonical forms-UX finding: a single column is faster and less error-prone (the eye follows one path; multi-column invites mis-scanning and ambiguous label association). Use multi-column *only* for short, related fields (city/state/zip, expiry/CVC) — never for a top-to-bottom flow.
- **Required-vs-optional marking — mark consistently, never neither.** If most fields are required, **mark the optional** ones ("(optional)"); if most are optional, mark the required (the `*` + a legend). Never leave the user guessing — and never rely on the `*` alone without explaining it.
- **The submit-disabled-until-valid debate — don't.** Disabling the submit until the form is valid *hides why* the user can't proceed (especially for AT — a disabled button isn't focusable/announced) and is a common anti-pattern. Keep submit enabled; validate on submit and route focus to the error summary (§6). (A pending/loading lock *during* submit is different and correct.)
- **When to reach for the wizard (forward-reference):** a long form (many sections, >~7–10 fields, or a genuine sequence with dependencies) is a **multi-step wizard** — the **Forms-as-a-system pattern**, not this component. Resolve it in the patterns layer.

## 6. Accessibility
Form is where the catalogue's field-level a11y work composes into a whole-form contract.
- **The error-summary + focus-on-submit (the a11y crux — GOV.UK).** On a **failed submit**, render an **error summary** at the top of the form: a titled block ("There is a problem") listing **each error as a link** whose target is the offending field; **move focus to the summary** (not to the first field — the GOV.UK contract, so the user hears the full list); each summary link **jumps focus to its field**. The summary is the **surviving form-level live region** (Inline Message abandoned field-level live regions in favour of `aria-describedby` + focus — the live region lives here, at the form level — see inline-message).
- **The field error association (inherited).** Each field error associates via **`aria-describedby` + `aria-invalid`** (the Text Field / Inline Message chain — see text-field, inline-message); the Form orchestrates *when* it appears (the escalation — §11), but the wiring is the field's.
- **The required/invalid announcement** — `aria-required` (or native `required`) on required fields; the error text in the field's described-by; the summary announces the count.
- **The Fieldset/legend grouping** — related fields and radio/checkbox groups are wrapped in `<fieldset>` + `<legend>` (the group's accessible name — see checkbox, radio); don't over-fieldset (a legend on every single field is noise — see section's don't-over-landmark parallel).
- **The submit-feedback live region** — the form-level success/error announces (a `role=status`/`alert` — the Toast/Banner lineage — see banner); the pending state is announced (the submit Button's loading — see button, spinner).
- **The implicit submit + keyboard** — Enter in a single-line field submits the form (preserve this native behavior); the submit Button is reachable and Enter/Space-activatable.
- **WCAG SCs:** **3.3.1** (error identification — the summary + field errors), **3.3.2** (labels/instructions — every field labelled, the required marking), **3.3.3** (error suggestion — actionable error copy — §7), **3.3.4** (error prevention for legal/financial/data — confirm/review/reversible), **3.3.7** (redundant entry — don't re-ask for data already given; autofill), **1.3.5** (identify input purpose — the `autocomplete` tokens — §9), **4.1.3** (status messages — the summary + submit feedback). Form carries the densest WCAG-3.3 surface in the catalogue.

## 7. Content guidelines
- **The label/helper/error copy (inherited)** — clear top-aligned labels, helper for constraints, specific actionable errors (the Text Field / Inline Message discipline — see text-field, inline-message).
- **The error-summary copy** — a clear title ("There is a problem"), each entry restating the field's error as a link ("Enter your email address"); match the summary text to the field error text.
- **The required/optional indicator** — explain the `*` ("All fields are required unless marked optional"); be consistent (§5).
- **The submit-button label** — a **specific verb** describing the action ("Create account", "Save changes", "Place order"), *not* a generic "Submit" (the Button content discipline — see button).
- **The success confirmation** — confirm what happened ("Your changes were saved") and what's next; don't leave the user wondering whether the submit worked.
- **The legend/group headings** — a clear `<legend>` naming each fieldset/section.

## 8. Motion and transition
- **The error-summary appearance + scroll** — on failed submit, the summary appears at the top and the page **scrolls to it** (with focus moved — §6); keep it immediate, not a slow animation that delays the user.
- **The field error reveal (inherited)** — the field error appears in its reserved slot (the layout-shift discipline from Inline Message — reserve space or accept a controlled shift — see inline-message).
- **The submit pending transition** — the submit Button → its loading state (the Button/Spinner transition — see button, spinner).
- **The success transition** — the form-level success message (the Banner/Toast enter — see banner, toast).
- **Reduce-motion** — `prefers-reduced-motion: reduce` keeps the scroll-to-error instant (or near-instant) and drops decorative transitions; the error information is the point, not the motion.

## 9. Internationalization
- **The copy** — labels, helper, errors, the summary, the submit label, the success message all translate (the field copy is inherited).
- **RTL** — the field layout, the label/required-marker placement, the error summary, and the submit-button alignment mirror via logical properties (see box); the single-column flow is direction-agnostic but the alignment flips.
- **The field-order / address-format locale variance** — name order (given/family varies), address fields (the postal-code/state/city order and presence vary by country), the phone format — a form that hardcodes a US address shape is broken elsewhere; drive the address fields from the locale/country (the Date Picker calendar-system lineage — locale-derived, not assumed — see date-picker).
- **The `autocomplete` token** — the tokens are locale-independent (a stable spec vocabulary), but the *fields* they map to vary by locale (§11).
- **The validation-message locale** — schema/engine error messages translate (Zod/Yup support localized messages); don't ship English validation strings to a localized form.

## 10. Naming
- **The field set:** **`Form`** (the orchestrator — React Aria, Carbon, Polaris, Ant, MUI, Fluent); **`FormField`** / **`Field`** (the per-field label+control+helper+error wrapper — React Aria's `<TextField>` bundles it; a generic `Field` wraps arbitrary controls); **`FormGroup`** / **`Fieldset`** (the grouping — Carbon's `FormGroup`); **`FormControl`** (MUI/Chakra — the field context wrapper).
- **The practice's default — `Form`** for the orchestrator (the `<form>` + the submit/validation context), **`FormField`** (or `Field`) for the per-field wrapper (label + control + helper + error — the generalisation of Text Field's field stack), and **`Fieldset`** (+ legend) for grouping. The field-engine (validation/state) is a *hook/context* the Form provides, not a separate visible component. Don't ship a `FormControl` that duplicates `FormField` — pick one wrapper name.
- **Aliases to map:** Form, FormField, Field, FormGroup, Fieldset, FormControl, FormProvider.

## 11. Implementation notes
- **Native `<form>` + progressive enhancement (+ the React 19 / Server Actions shift)** — start from a real `<form>` with a real submit so it works without JS (the native submit posts the form); enhance with JS. The modern platform shift: **React 19 form Actions** (`<form action={fn}>`, `useActionState` for the result/pending, `useFormStatus` for a nested submit button's pending) and **Server Actions** (Next/Remix) reclaim the native form model with server-side handling + progressive enhancement. Date this — it's a live shift (verify the current React 19 / framework state under `notes.unverified`).
- **The form-engine choice** — the practice default is **react-hook-form + a Zod resolver** (uncontrolled/ref-based for performance + schema validation), with **React Aria's native validation** (the `ValidationResult` + native Constraint Validation) as the a11y-first alternative and **Formik** (controlled) as the legacy/heavier option. The engine owns field registration, the validation mode, the error state, and `isSubmitting`/`isDirty`.
- **The validation escalation** — orchestrate across fields: **on submit** validate everything (and route focus to the summary); **on blur** validate a field once it's been *touched*; **on change** validate a field only once it's *already in error* (so the error clears as the user fixes it, but a pristine field isn't nagged). This is "reward early, punish late" at the form level (Inline Message's field-side rule — see inline-message).
- **The server-error-to-field mapping** — client validation is UX; the **server is the source of truth** (the same boundary File Upload drew — see file-upload). On a server-rejected submit, map each server error back onto its field (`setError`) *and* surface a form-level message; never just show a generic failure that loses which field is wrong.
- **The error-summary + focus + scroll** — on failed submit, build the summary from the error map, render it at the top, move focus to it, and scroll it into view; each link targets its field's id and moves focus there (§6).
- **Prevent double-submit + the pending lock** — disable/lock the submit during the in-flight request (the Button loading state — see button), guard against a second submit (a ref/flag), and re-enable on success/error.
- **The dirty-form unsaved-changes guard** — when the form is dirty, warn on navigation away (the `beforeunload` event for tab close; the router's navigation guard for SPA route changes); clear the guard on successful submit.
- **The autocomplete tokens** — set the right `autocomplete` token per field (`name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `one-time-code`, `new-password`/`current-password`); **don't use `autocomplete=off`** broadly (browsers mostly ignore it and it harms usability/password managers); WCAG 1.3.5 (§9).
- **The uncontrolled-vs-controlled performance trade** — controlled forms (every keystroke in React state — Formik) re-render the whole form per keystroke and degrade on large forms; uncontrolled/ref-based (react-hook-form) isolates re-renders to the changed field. Default uncontrolled for anything non-trivial.
- **Headless vs opinionated** — the validation engine + the field-state machine + the form-state are heavy headless logic (react-hook-form / TanStack Form / React Aria); the layout/field-wrapper/summary are the design system's. **Build on a form engine**; don't hand-roll the validation-mode escalation and the field-registration.

## 12. Related and alternative components
- **Composes:** **all the form controls** — Text Field, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload (the orchestrator they plug into — see text-field, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload) — plus **Button** (the submit/reset + the pending lock — see button) and **Inline Message** / **Banner** (the field error + the form-level message — see inline-message, banner).
- **Builds on:** **Inline Message** (the field-level error *is* Inline Message; the form-level error summary is the **surviving form-level live region** Inline Message pointed to — see inline-message) and **Text Field** (the field-stack / `aria-describedby` chain generalised to the FormField wrapper — see text-field).
- **Borders (the component-vs-pattern boundary):** the **Forms-as-a-system pattern** — the multi-step **wizard**, the long multi-section flow, save-and-resume (the **pattern**, forward-referenced to the patterns layer, *not* this component); the **Filter set** (fields applied without a submit — the Filtering pattern).
- **Closes:** the **Form category** (the controls + Inline Message + the Form orchestrator).
- **Alternative to:** a single auto-saving control (no submit), a Filter set (no submit/summary).

(The compositional owner that closes the Form category — the `<form>` primitive + the validation orchestration + the submission contract + the error summary, the orchestrator every form control plugs into. It composes the controls + Button + Inline Message, builds on Inline Message's field-error/form-summary split + Text Field's field-stack, and borders the Forms-as-a-system PATTERN (the wizard — forward-referenced to the patterns layer). See text-field for the field substrate, inline-message for the field-error/live-region split, button for the submit/pending, file-upload/date-picker for the composite controls it orchestrates. 03-component-library; 29 for the docs template; the coming patterns layer for Forms-as-a-system.)

## 13. Field POV evolution
1. **The native `<form>` → the controlled JS form.** Forms began as native `<form>` + server round-trips; the SPA era moved state into JS, and **Formik** standardized the controlled-form model (every value in state, validation in JS).
2. **The uncontrolled / performance turn + schema validation.** Controlled forms re-rendered too much; **react-hook-form** moved to uncontrolled/ref-based registration (isolated re-renders), and **Zod/Yup/Valibot** schemas (via resolvers) became the validation source of truth — separating the schema from the UI.
3. **The platform reclaiming the form.** **React 19 form Actions** (`useActionState`/`useFormStatus`) and **Server Actions** (Next/Remix) brought back the native-form model with progressive enhancement + server-side handling — the form works without JS again, enhanced when it loads.
4. **The accessible error-summary standardizing.** The **GOV.UK** error-summary + focus-management pattern became the accessible-forms reference (summary at top, focus to it, links to fields), and the validation strategy settled on **"reward early, punish late"** (validate on submit, re-validate on change once errored).

## 14. Sources cited
*(External-pass version dates to be reconciled; flag any unverified under notes.unverified.)*
- WAI-ARIA APG + **GOV.UK Design System** — the gold-standard accessible-forms guidance + the **error-summary** pattern + the question-protocol.
- **React Aria** — the `Form` component + native validation behaviors + the `ValidationResult` model.
- **react-hook-form** — the uncontrolled/ref-based engine + the resolver model (Zod/Yup/Valibot).
- **Formik** / **TanStack Form** / **Final Form** — the controlled / modern form engines.
- **Zod / Yup / Valibot** — the schema-validation libraries.
- **React 19** — form Actions / `useActionState` / `useFormStatus`; **Next.js / Remix** — Server Actions.
- the native **Constraint Validation API** + the **`autocomplete`** spec (WHATWG HTML).
- **IBM Carbon** (`Form` / `FormGroup`), **Shopify Polaris** (`Form`), **Ant Design** (`Form` — the rules/validation model, the most feature-complete), **Microsoft Fluent**, **MUI** (`FormControl`).
- WCAG 2.2 — 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 1.3.5, 4.1.3.

## 15. Agent-consumable schema
```yaml
identity:
  id: form
  name: Form
  aliases: [Form, FormField, Field, FormGroup, Fieldset, FormControl, FormProvider]
  category: form
  status: stable
description: >
  The compositional OWNER of the Form category — the <form> primitive + the validation
  ORCHESTRATION (the form-level strategy sequencing the fields' own validation) + the
  submission contract + the error SUMMARY. The orchestrator every form control plugs into
  (Text Field, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload),
  which CLOSES the Form category. NOT a single control (it owns coordination, not a value),
  NOT the field-level error (that's Inline Message), and — the explicit COMPONENT-VS-PATTERN
  boundary — NOT the multi-step WIZARD / Forms-as-a-system (that's the PATTERN, forward-
  referenced to the patterns layer). Three decisions: the validation-strategy/when-to-validate
  escalation (submit -> blur-when-touched -> change-when-errored; reward early, punish late),
  the error-summary + focus-on-submit pattern (GOV.UK — focus the summary, link to each
  field; the surviving form-level live region Inline Message pointed to), and the submission
  lifecycle + progressive enhancement (native <form> first; React 19 Actions / Server Actions).
anatomy:
  parts:
    - "the <form> element: the onSubmit/action, the implicit-submit (Enter in a single text field), the native submit semantics"
    - "the FormField/Field wrappers: the composition primitive wiring label + control + helper + error per field (Text Field's field stack generalised to wrap ANY control)"
    - "the field groups: Fieldset + legend for related fields + radio/checkbox groups (the group's accessible name)"
    - "the error summary: a top-of-form block (on failed submit) listing each error as a LINK to its field; the focus target"
    - "the form-level message: a Banner/Inline Message for the whole-form success/error (distinct from per-field errors)"
    - "the submit/reset Button(s) + the pending state (the loading lock); reset rare/discouraged; multiple submits via formaction"
    - "the required/optional marking: a consistent indicator (mark optional, or mark required — never neither)"
    - "the field layout: single-column by default, the Stack rhythm; Fieldset grouping for sections"
api:
  composes: [text-field, textarea, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload, button, inline-message, banner]
  builds-on: [inline-message, text-field]
  props:
    - {name: "onSubmit(values) / action", type: "fn", default: ~, required: false, description: "the submit handler (controlled) or the native/Server Action (progressive enhancement)"}
    - {name: mode, type: "'onSubmit'|'onBlur'|'onChange'|'onTouched'|'all'", default: onSubmit, required: false, description: "the validation strategy; the practice escalates submit -> blur(touched) -> change(errored)"}
    - {name: schema/resolver, type: "Zod|Yup|Valibot schema | native validate", default: ~, required: false, description: "schema-driven (react-hook-form resolver) or React Aria native validation / Constraint Validation API"}
    - {name: field-registration, type: "register/Controller | <Field> | native", default: ~, required: false, description: "the engine's field-binding model"}
    - {name: defaultValues, type: object, default: ~, required: false, description: "the initial values (uncontrolled-friendly)"}
    - {name: "form-state", type: "isSubmitting/isValid/isDirty/errors/isSubmitSuccessful", default: ~, required: false, description: "the form state machine"}
    - {name: "server-error mapping", type: "setError(field,...)", default: ~, required: false, description: "map a server-returned error back onto the offending field (client UX, server truth)"}
    - {name: "model", type: "'uncontrolled'|'controlled'", default: uncontrolled, required: false, description: "uncontrolled/ref (react-hook-form — performance) vs controlled (Formik — re-render cost)"}
    - {name: autocomplete-wiring, type: "per-field tokens", default: ~, required: false, description: "the autocomplete token per field (WCAG 1.3.5)"}
  withholds: "doesn't reinvent the controls (composes them) or the field-level error (Inline Message); adds the orchestration + submit + summary + layout"
states:
  form: [idle, validating, submitting, success, error]   # submitting = the pending lock (submit loading, double-submit prevented)
  field-orchestrated: [pristine, touched, dirty, valid, invalid]   # the Form tracks these to drive the validation escalation
  submit-button: [enabled, pending, disabled]   # the disabled-until-valid debate: DON'T (hides why)
variants:
  layout: [single-column, multi-column, inline]   # single-column DEFAULT; multi only for short related fields
  grouping: [flat, fieldset-grouped]
  whole-form: [editable, read-only, disabled-during-submit]
  submit-model: [native-progressive-enhancement, controlled-js, server-action]
accessibility:
  wcag-criteria: ["3.3.1", "3.3.2", "3.3.3", "3.3.4", "3.3.7", "1.3.5", "4.1.3"]
  builds-on: [inline-message (the field-error/form-summary split), text-field (the aria-describedby chain)]
  error-summary: "THE crux (GOV.UK) — on a FAILED SUBMIT render a top-of-form summary ('There is a problem') listing each error as a LINK to its field; MOVE FOCUS to the summary (not the first field — so the user hears the full list); each link jumps focus to its field. The SURVIVING form-level live region (Inline Message abandoned field-level live regions for aria-describedby + focus; it lives here)"
  field-error-association: "each field error via aria-describedby + aria-invalid (the Text Field / Inline Message chain — inherited); the Form orchestrates WHEN it appears, the wiring is the field's"
  required-invalid: "aria-required (or native required) on required fields; the error text in described-by; the summary announces the count"
  fieldset-legend: "related fields + radio/checkbox groups in <fieldset> + <legend> (the group's accessible name); DON'T over-fieldset (a legend on every field is noise)"
  submit-feedback: "the form-level success/error announces (role=status/alert — the Banner lineage); the pending state announced (the submit Button loading)"
  implicit-submit: "Enter in a single-line field submits (preserve the native behavior); the submit Button reachable + Enter/Space-activatable"
content:
  labels-errors: "clear top-aligned labels + helper + specific actionable errors (inherited from Text Field / Inline Message)"
  summary-copy: "a clear title ('There is a problem'); each entry restates the field error as a link ('Enter your email address'); match the summary text to the field error"
  required-optional: "explain the * ('All fields required unless marked optional'); be consistent"
  submit-label: "a SPECIFIC verb ('Create account' / 'Save changes' / 'Place order'), NOT a generic 'Submit'"
  success: "confirm what happened ('Your changes were saved') + what's next; don't leave the user wondering"
  legends: "a clear <legend> naming each fieldset/section"
motion:
  error-summary: "on failed submit the summary appears at the top + the page scrolls to it (focus moved); immediate, not a slow animation"
  field-error-reveal: "the field error appears in its reserved slot (the layout-shift discipline from Inline Message)"
  submit-pending: "the submit Button -> its loading state (the Button/Spinner transition)"
  success: "the form-level success message (the Banner/Toast enter)"
  reduce-motion: "keep the scroll-to-error instant + drop decorative transitions; the error info is the point, not the motion"
i18n:
  copy: "labels/helper/errors/summary/submit-label/success translate (the field copy inherited)"
  rtl: "the field layout + the label/required-marker placement + the error summary + the submit alignment mirror via logical properties"
  address-locale-variance: "name order (given/family) + address fields (postal-code/state/city order + presence) + phone format vary by country — drive the address fields from locale/country, don't hardcode a US shape (the Date Picker locale-derived lineage)"
  autocomplete-token: "the tokens are locale-INDEPENDENT (a stable spec vocabulary); the FIELDS they map to vary by locale"
  validation-message-locale: "schema/engine error messages translate (Zod/Yup localized messages); don't ship English validation strings to a localized form"
implementation:
  - "native <form> + progressive enhancement (works without JS) + the platform shift: React 19 form Actions (<form action={fn}>, useActionState for result/pending, useFormStatus for a nested submit's pending) + Server Actions (Next/Remix) — reclaim the native form with server-side handling + PE. DATE this (verify current React 19 / framework state)"
  - "the form-engine choice: PRACTICE DEFAULT react-hook-form + a Zod resolver (uncontrolled/ref + schema), with React Aria native validation (ValidationResult + Constraint Validation) as the a11y-first alternative + Formik (controlled) as the legacy/heavier option. The engine owns field registration, the mode, errors, isSubmitting/isDirty"
  - "the validation escalation: on SUBMIT validate everything (+ focus the summary); on BLUR validate a field once TOUCHED; on CHANGE validate a field only once ALREADY IN ERROR (clears as the user fixes, pristine fields not nagged). 'Reward early, punish late' at the form level (Inline Message's field-side rule)"
  - "the server-error-to-field mapping: client validation is UX, the SERVER is the source of truth (the File Upload boundary). On a server-rejected submit, map each error back onto its field (setError) + surface a form-level message; never a generic failure that loses which field is wrong"
  - "the error-summary + focus + scroll: build the summary from the error map, render at the top, move focus to it, scroll into view; each link targets its field id + moves focus there"
  - "prevent double-submit + the pending lock: disable/lock the submit during the in-flight request (the Button loading), guard a second submit (a ref/flag), re-enable on success/error"
  - "the dirty-form unsaved-changes guard: when dirty, warn on navigation away (beforeunload for tab close; the router guard for SPA route changes); clear on successful submit"
  - "the autocomplete tokens: the right token per field (name/email/tel/street-address/postal-code/cc-number/one-time-code/new-password/current-password); DON'T use autocomplete=off broadly (browsers ignore it + it harms password managers); WCAG 1.3.5"
  - "the uncontrolled-vs-controlled performance trade: controlled (every keystroke in state — Formik) re-renders the whole form per keystroke + degrades on large forms; uncontrolled/ref (react-hook-form) isolates re-renders to the changed field. Default uncontrolled for anything non-trivial"
  - "headless vs opinionated: the validation engine + field-state machine + form-state are heavy headless logic (react-hook-form / TanStack Form / React Aria); the layout/field-wrapper/summary are the design system's. BUILD ON A FORM ENGINE — don't hand-roll the validation-mode escalation + field-registration"
composition:
  composes: [text-field, textarea, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload, button, inline-message, banner]
  builds-on: [inline-message, text-field]
  closes: "the Form category (the controls + Inline Message + the Form orchestrator)"
  borders: ["the Forms-as-a-system PATTERN (the multi-step wizard / long multi-section flow / save-and-resume — forward-referenced to the patterns layer, NOT this component)", "the Filter set (fields applied without a submit — the Filtering pattern)"]
  alternative-to: ["a single auto-saving control (no submit)", "a Filter set (no submit/summary)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the validation strategy — onSubmit (the safe default) vs aggressive onChange; the practice escalates submit -> blur(touched) -> change(errored) (reward early, punish late)"
    - "the form engine — react-hook-form + Zod (uncontrolled, practice default) vs React Aria native validation (a11y-first) vs Formik (controlled, heavier)"
    - "submit-disabled-until-valid — a common ANTI-PATTERN (hides why, a disabled button isn't announced); keep submit enabled + route focus to the summary"
    - "native <form> + React 19 Actions / Server Actions (the platform reclaiming) vs a fully controlled JS form"
    - "the COMPONENT-VS-PATTERN line — the Form primitive (this component) vs Forms-as-a-system / the multi-step wizard (the PATTERN, forward-referenced)"
    - "required-vs-optional marking — mark optional (if most required) or mark required (if most optional), NEVER neither"
  trap:
    - "submit-disabled-until-valid (hides the reason; AT can't focus a disabled button) — keep enabled, validate on submit, focus the summary"
    - "focusing the first field instead of the error summary on failed submit (GOV.UK: focus the summary so the user hears the full list)"
    - "field-level live regions (the double-announcement bug Inline Message resolved) — the live region survives only at the form/summary level"
    - "autocomplete=off broadly (browsers ignore it + it harms password managers); missing autocomplete tokens (WCAG 1.3.5)"
    - "a controlled form re-rendering on every keystroke (use uncontrolled/ref for large forms); losing the user's input on a submit error"
    - "hardcoding a US address/name shape (drive from locale/country); shipping English validation strings to a localized form"
    - "over-fieldsetting (a legend on every field is noise); a generic 'Submit' button label (use a specific verb)"
  inherited: "Inline Message's field-error model + the form-level-live-region split; Text Field's field-stack + aria-describedby chain + top-label default; Button's submit + loading/pending + the specific-verb label; the Stack rhythm for field spacing; Fieldset/legend from Checkbox/Radio; the client-UX-server-truth validation boundary from File Upload"
  role-in-family: "the compositional OWNER that CLOSES the Form category — the <form> primitive + the validation orchestration + the submission contract + the error summary; the orchestrator every form control plugs into; borders the Forms-as-a-system PATTERN (the wizard)"
  evolution:
    - "the native <form> -> the controlled JS form (Formik)"
    - "the uncontrolled/performance turn (react-hook-form) + schema validation (Zod/Yup/Valibot)"
    - "the platform reclaiming the form (React 19 Actions / useActionState/useFormStatus / Server Actions + progressive enhancement)"
    - "the accessible error-summary standardizing (GOV.UK: summary at top, focus to it, links to fields) + the validation strategy settling (reward early, punish late)"
  unverified:
    - "the React 19 form Actions / useActionState / useFormStatus API + the Next/Remix Server Actions state — verify against current platform"
    - "external 2026 version numbers (react-hook-form, React Aria Form, Ant Form, Zod/Valibot)"
    - "the GOV.UK error-summary current guidance specifics (focus-the-summary) — verify against the current GOV.UK Design System"
```

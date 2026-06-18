---
okf_version: "0.1"
type: component-brief
title: Form
description: The compositional owner that closes the Form category — a field-truth study of the validation-strategy/when-to-validate escalation (the two-prop validationMode + reValidateMode model — submit first, then blur-when-touched, then change-once-errored; reward early, punish late) and the schema-engine-vs-native-Constraint-Validation reality, the error-summary + focus-management pattern (GOV.UK — focus the summary not the first field, link to each field, the compound-field sub-target; the surviving form-level live region Inline Message pointed to), the submission lifecycle + progressive enhancement (native <form> + novalidate; the React 19 form Actions / useActionState / useFormStatus + Server Actions shift), the FormField wrapper + the single-column-layout finding, the autofill/autocomplete contract (the autocomplete=off-is-ignored + the password-manager-icon-overlap traps), and the unsaved-changes guard — composing all the form controls + Button + Inline Message, building on Inline Message's field-error/form-summary split + Text Field's field-stack, bordering the Forms-as-a-system PATTERN (the wizard — forward-referenced to the patterns layer), with the explicit component-vs-pattern boundary and the practice's defaults.
tags: [components, form]
category: Form
status: stable
aliases: [Form, FormField, Field, FormGroup, Fieldset, FormControl, FormProvider]
last-audited: 2026-06-18
timestamp: 2026-06-18
---

# Form

> A Form is the **compositional owner of the Form category** — the `<form>` primitive plus the orchestration that turns a set of independent controls into a single submittable, validatable unit. It is the **last Form brief** and **closes the Form category**: the orchestrator every prior control plugs into (Text Field, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload). Its job is the *coordination* layer — the submission contract, the form-level validation strategy that sequences the fields' own validation, the error summary, the field/submit wiring, the layout, and the autofill contract — and it reuses nothing it can compose: the controls own their internal a11y mappings, **Inline Message** owns field-level error rendering (see inline-message), **Button** owns the submit + its pending state (see button). **The component-vs-pattern boundary, stated up front and held deliberately:** this brief is the Form **component** — the `<form>` primitive, the validation orchestration, the error summary, the FormField wrapper, the single-column layout, the autocomplete contract — a concrete, briefable compositional unit. **Forms-as-a-system** — the multi-step **wizard**, the long multi-section flow, save-and-resume, the cross-page form UX — is the **pattern**, explicitly out of scope and forward-referenced to the coming patterns layer (it is the patterns layer's first big item). What it *isn't*: a single control (it owns coordination, not a value), the field-level error (that's **Inline Message**), or the wizard (the **pattern**). Three decisions define it: the **validation-strategy / when-to-validate** escalation (reward early, punish late), the **error-summary + focus-management** pattern (GOV.UK), and the **submission lifecycle + progressive enhancement** (native `<form>` first; React 19 Actions / Server Actions). Why systems disagree: the validation engine/strategy, the controlled-vs-uncontrolled model, the submit-disabled debate, and where the component ends and the pattern begins.

---

## 1. Framing
A Form is the *coordination* layer over a set of controls: it owns the submission contract, the form-level validation strategy that sequences the fields' own validation, the error summary, the field/submit wiring, the layout, and the autofill contract — and it composes everything it can (the controls own their internal a11y; Inline Message owns field-level errors; Button owns the submit/pending).

**The component-vs-pattern boundary (stated up front, held deliberately).** There is a real duality here, and this brief takes the **component** side:
- **The component (this brief):** the Form *primitive* — the `<form>` + the submit contract, the validation *orchestration*, the error *summary*, the FormField/Field wrapper, the submit Button + its pending state, the single-column layout + Fieldset grouping, and the autocomplete contract. A concrete, briefable compositional unit.
- **The pattern (out of scope — forward-referenced):** **Forms-as-a-system** — the multi-step **wizard**, the long multi-section flow, save-and-resume, the cross-page form UX. Named here as the boundary, *not* resolved — it is the coming patterns layer's first big item. (Polaris and Carbon draw the same line: a `Form` component for single-view orchestration, multi-step delegated to template patterns.)

Three decisions define the component:
- **The validation-strategy / when-to-validate crux (the headline).** The escalation the field settled on, expressed as two props: a **`validationMode`** (when validation *first* fires — `onSubmit` default) and a **`reValidateMode`** (when it re-fires *after* a failed submit — `onChange` default). The practice: validate **on submit** first, then **on blur** for a touched field, then **on change** only once a field is already in error ("reward early, punish late") (§6/§11).
- **The error-summary + focus-management pattern (the a11y crux).** On a failed submit, render a summary at the top listing each error as a link to its field, **move focus to the summary** (not the first field), and announce it (the GOV.UK pattern). This is the **surviving form-level live region** Inline Message pointed to — field-level live regions abandoned; the live region lives here (§6).
- **The submission lifecycle + progressive enhancement (the submit crux).** The submit state machine (idle → validating → submitting [the pending lock + the Button loading, prevent double-submit] → success | error), the preserve-data-on-error rule, and the **native-`<form>`-first** reality — the form works without JS, JS enhances it (React 19 form Actions / `useActionState` / `useFormStatus`; Server Actions) (§11).

What it *isn't*: a single control, the field-level error (Inline Message — see inline-message), or the multi-step wizard / Forms-as-a-system (the pattern, forward-referenced). Why systems disagree: the validation engine/strategy, controlled-vs-uncontrolled, the submit-disabled debate, and the component/pattern line.

## 2. Anatomy and parts
- **the `<form>` element** — the real container: the `onSubmit`/`action`, the implicit-submit (Enter in a single text field), the native submit semantics, and **`novalidate`** to suppress the native browser validation bubbles in favour of the custom UI (§11).
- **the FormField / Field wrappers** — the composition primitive wiring **label + control + helper + error** for each field (a context boundary that auto-binds `id`/`aria-labelledby`/`aria-describedby` across its children — the bundled-vs-composed tension Text Field settled, now at the form level, generalised to wrap *any* control — see text-field).
- **the field groups** — **Fieldset + legend** for related fields and for radio/checkbox groups (the `<legend>` is the group's accessible name — keep it concise; some SRs announce it before *every* contained input — see checkbox, radio).
- **the error summary** — a top-of-form block (on failed submit) wrapped in `role=alert`, with a heading + an unordered list of each error as a **link to its field**; the focus target (§6).
- **the form-level message** — a **Banner / Inline Message** for the whole-form success/fatal-error (a 500, "Your changes were saved") not mappable to a field — distinct from the per-field errors and the validation summary (see banner, inline-message).
- **the submit / reset Button(s)** — the **submit Button** + its **pending state** (the loading lock — see button, spinner); reset is rare/discouraged; multiple submits via `formaction` (§11).
- **the required/optional marking** — a consistent indicator (mark optional, or mark required — never neither — §5).
- **the field layout** — single-column by default, with the Stack rhythm (see stack); Fieldset grouping for sections.

## 3. Properties / API
- **`onSubmit(values)`** / **`action`** — the submit handler (controlled) or the native/Server Action (progressive enhancement — in React 19, `action` accepts a server action compatible with `useActionState`) (§11).
- **`validationBehavior`** — `'native'` (native HTML constraint validation blocks submission) vs **`'aria'`** (default; the engine handles errors via ARIA without blocking the native submit — preferred for custom validation logic). Distinct from *when* validation fires.
- **`validationMode`** — `onSubmit` (default) / `onBlur` / `onChange` / `onTouched` / `all` — when validation *first* fires.
- **`reValidateMode`** — `onSubmit` / `onBlur` / `onChange` (default) — when validation re-fires *after* a failed submit (the rapid error-recovery half of the escalation — §11).
- **`resolver`** — the bridge to a Zod/Yup/Valibot schema (react-hook-form), or React Aria's native `validate` + the `ValidationResult`, or the native Constraint Validation API (§11).
- **`defaultValues`** — the initial values (uncontrolled-friendly; crucial for edit/update mutations + caching).
- **the form state** — `isSubmitting` / `isValid` / `isDirty` / `errors` / `isSubmitSuccessful` (the form state machine — §4).
- **`validationErrors`** — server-side error mapping (a `Record<field, string[]>` translating backend errors back onto field names; React Aria/Spectrum's bridge — §11).
- **`preventMultiSubmit`** — disable the submit during a pending submission (default true).
- **the native-vs-controlled model** — uncontrolled (native form data / refs — performance) vs controlled (every keystroke in state — Formik; the re-render cost — §11).
- **the autofill wiring** — the `autocomplete` tokens per field (§9/§11).
- **what it withholds** — the Form doesn't reinvent the controls (it composes them) or the field-level error (Inline Message); it adds the orchestration + the submit + the summary + the layout.

## 4. States and variants
- **The form states (independent of the fields):** **idle** / **validating** (the transient async-schema/server-check phase) / **submitting** (the pending lock — the submit Button loading, mutations blocked, double-submit prevented) / **success** (clear / redirect / a confirmation banner) / **error** (client schema rejection or a server 400 → the summary mounts + hijacks focus).
- **The field states (orchestrated, not owned):** **pristine** → **dirty** (the unsaved-changes guard relies on the aggregate dirty state); **untouched** → **touched** (the primary metric the escalating validation uses to reveal inline errors). The Form tracks these to drive the validation escalation (§11).
- **The submit Button states:** enabled / **pending** (loading) / disabled — but **not** disabled-until-valid (§5).
- **Variants:**
  - **layout:** single-column (default) / multi-column (the exception — short related fields only) / inline (a single-row mini-form).
  - **density / grouping:** flat / Fieldset-grouped sections.
  - **the whole-form** read-only / disabled (during submit).
  - **the submit model:** native (progressive enhancement) / controlled JS / Server Action.

## 5. Usage guidance
- **Use a Form for:** a set of fields the user fills and **submits together** with validation orchestration (a sign-up, a checkout step, a settings page, a create/edit record). The Form is the coordination unit.
- **Form vs the alternatives:**
  - **vs a single auto-saving field** — a settings toggle or inline-edit field that saves *immediately* on change isn't a Form-submit; it's a control with its own optimistic-update (see switch). No submit, no summary.
  - **vs a Filter set** — filters apply *as you change them* (no submit, no validation summary, no POST); a Filter set bypasses the Form's validation engine and submit lifecycle (the Filtering *pattern* — forward-reference).
- **Single-column by default.** The canonical forms-UX finding: a single column completes faster with fewer errors (the eye follows one path; multi-column invites mis-scanning, missed right-periphery fields on mobile/magnification, and ambiguous label association). Use multi-column *only* for short, tightly-coupled units the user parses as one cognitive chunk (first+last name, city/state/zip, expiry/CVC) — and then keep the tab order following the visual flow.
- **Required-vs-optional marking — mark consistently, never neither.** Practice data-minimalism: collect only actionable data (eliminate a field rather than mark it optional), which makes most fields required — so **mark the rare optional ones with the word "(optional)"** rather than asterisking everything. If you do use the `*` for required, explain it and `aria-hidden` the glyph. Never leave the user guessing.
- **The submit-disabled-until-valid debate — don't.** Disabling the submit until the form is valid *hides why* the user can't proceed and gives zero feedback on which field they missed; worse, a disabled button isn't focusable/announced, trapping AT users without a clue. Keep submit **enabled**; on click, validate, surface the errors, and route focus to the error summary (§6). (A pending/loading lock *during* submit is different and correct.)
- **When to reach for the wizard (forward-reference):** a long form (disparate sections — personal then payment — or >~10 fields, or one needing external documents) is a **multi-step wizard** — the **Forms-as-a-system pattern**. The Form component still governs each *step*; the wizard pattern owns the progression, draft-saving, and cross-step validation. Resolve it in the patterns layer.

## 6. Accessibility
Form is where the catalogue's field-level a11y work composes into a whole-form contract.
- **The error-summary + focus-on-submit (the a11y crux — GOV.UK).** On a **failed submit**, render an **error summary** at the top of the form, wrapped in `role="alert"`: a titled block ("There is a problem") listing **each error as a link** whose target is the offending field; **move focus to the summary heading** (not the first field — so the user hears the full list of problems, the GOV.UK contract; since a heading isn't natively focusable, give it `tabindex="-1"`); each summary link **jumps focus to its field**. For a **compound field** (a three-part date input), the link targets the specific failed *sub-field* (e.g. the year input), not the generic fieldset wrapper. The summary is the **surviving form-level live region** (Inline Message abandoned field-level live regions in favour of `aria-describedby` + focus — the live region lives here — see inline-message).
- **The field error association (inherited).** Each invalid field gets **`aria-invalid="true"`** and the error message's id appended to its **`aria-describedby`** (the Text Field / Inline Message chain — see text-field, inline-message), so tabbing into it announces the label, value, type, and the specific error. The Form orchestrates *when* the error appears (the escalation — §11); the wiring is the field's.
- **The required/invalid announcement** — `aria-required` (or native `required`) on required fields; the error text in the described-by; the summary announces the count.
- **The Fieldset/legend grouping** — related fields and radio/checkbox groups are wrapped in `<fieldset>` + `<legend>` (the group's accessible name — see checkbox, radio); don't over-fieldset (a legend on every single field is noise — the Section don't-over-landmark parallel — see section).
- **The submit-feedback live region** — the form-level success/error announces (the Banner `role=status`/`alert` lineage — see banner); the pending state is announced (the submit Button's loading — see button, spinner).
- **The implicit submit + keyboard** — Enter in a single-line field submits the form (preserve this native behavior — which requires a genuine `<button type="submit">`, never a stylized div pseudo-button); the submit Button is reachable and Enter/Space-activatable.
- **WCAG SCs:** **3.3.1** (error identification — the summary + field errors), **3.3.2** (labels/instructions — every field labelled, the required marking), **3.3.3** (error suggestion — actionable error copy — §7), **3.3.4** (error prevention for legal/financial/data — confirm/review/reversible), **3.3.7** (redundant entry — don't re-ask for data already given; autofill), **1.3.5** (identify input purpose — the `autocomplete` tokens — §9), **4.1.3** (status messages — the summary + submit feedback). Form carries the densest WCAG-3.3 surface in the catalogue.

## 7. Content guidelines
- **The label/helper/error copy (inherited)** — clear top-aligned labels, helper for constraints, specific actionable errors (the Text Field / Inline Message discipline — see text-field, inline-message).
- **The error-summary copy** — a clear title ("There is a problem"), each entry restating the field's error as a link ("Enter your email address"); the summary text must **exactly match** the inline field error (a mismatch — "Invalid date" inline vs "Date of birth must be in the past" in the summary — is cognitive dissonance).
- **The inline error copy** — actionable + specific ("Enter your first name", "Password must be at least 8 characters", "The expiration date must be in the future"); never generic ("Invalid input", "An error occurred") or accusatory/technical ("illegal value", "forbidden", "form post error").
- **The required/optional indicator** — explain the `*` ("All fields are required unless marked optional"); be consistent (§5).
- **The submit-button label** — a **specific verb** describing the action ("Create account", "Save changes", "Pay now"), *not* a generic "Submit" (the Button content discipline — see button).
- **The success confirmation** — confirm what happened ("Your changes were saved") and what's next.
- **The legend/group headings** — the `<legend>` is the group's primary label (the exact phrase, e.g. "Preferred contact method"), not a stray paragraph above the inputs.

## 8. Motion and transition
- **The error-summary appearance + scroll** — on failed submit the summary appears at the top (a rapid slide-down/fade) and the page **scrolls to it** (with focus moved — §6); `scroll-behavior: smooth` helps sighted users locate their new position; keep it immediate, not a slow animation that delays recovery.
- **The field error reveal (inherited) + the CLS trap** — the field error appears in its reserved slot; mounting it *below* an input pushes subsequent fields down (a Cumulative Layout Shift that causes mis-clicks), so **reserve a fixed min-height for the error slot** or absolutely-position the error text (with padding for multi-line) — the layout-shift discipline from Inline Message (see inline-message).
- **The submit pending transition** — the submit Button → its loading state, snappy (~100–150ms — the Button/Spinner transition; see button, spinner).
- **The success transition** — the form-level success message (the Banner/Toast enter — see banner, toast).
- **Reduce-motion** — `prefers-reduced-motion: reduce` keeps the scroll-to-error and the summary appearance instant (or near-instant) and drops decorative transitions; the error information is the point, not the motion.

## 9. Internationalization
- **The copy** — labels, helper, errors, the summary, the submit label, the success message all translate (the field copy is inherited).
- **RTL** — the field layout, the label/required-marker placement (the marker shifts side), the error summary's alignment/padding, and the submit-button alignment mirror via logical properties (see box); the single-column flow is direction-agnostic but the alignment flips.
- **The field-order / address-format locale variance** — Western name order (given/family) doesn't apply globally (many cultures use a single name or a different surname order); address fields vary wildly (ZIP vs postal vs sorting codes; state/province presence and order); the API must let developers **dynamically reorder/hide/relabel** fields by locale **without breaking the validation schema** — a form that hardcodes a US address/name shape is broken elsewhere (the Date Picker locale-derived lineage — see date-picker).
- **The `autocomplete` token** — the tokens are **locale-independent** (a stable WHATWG vocabulary, browser-recognized regardless of display language — which is *why* you trigger password managers via the spec token, not localized label text); the *fields* they map to vary by locale (§11).
- **The validation-message locale** — schema/engine error messages need an i18n layer (Zod/Yup emit English by default — intercept and map through, e.g. `zod-i18n`); don't ship English validation strings to a localized form.

## 10. Naming
- **The field set:** **`Form`** (the orchestrator — React Aria, Carbon, Polaris, Ant, MUI, Fluent — universal); **`FormField`** / **`Field`** / **`FormControl`** (the per-field label+control+helper+error wrapper — `FormControl` in MUI/Chakra as a context boundary; `Field` in TanStack Form / react-hook-form); **`FormGroup`** / **`Fieldset`** (the grouping — Carbon's `FormGroup`; native-semantics systems prefer `Fieldset`).
- **The practice's default — `Form`** for the orchestrator (the `<form>` + the submit/validation context), **`FormField`** for the per-field wrapper (the generalisation of Text Field's field stack), and **`Fieldset`** (+ legend) for grouping. The field-engine (validation/state) is a *hook/context* the Form provides, not a separate visible component. Don't ship both a `FormControl` and a `FormField` that duplicate each other — pick one wrapper name.
- **Aliases to map:** Form, FormField, Field, FormGroup, Fieldset, FormControl, FormProvider.

## 11. Implementation notes
- **Native `<form>` + progressive enhancement (+ the React 19 / Server Actions shift)** — start from a real `<form>` with a real `<button type=submit>` so it works without JS (the native submit posts the form), and add **`novalidate`** to suppress the native validation bubbles in favour of the custom UI; then enhance with JS. The platform shift: **React 19 form Actions** (`<form action={fn}>` rather than `e.preventDefault()`, `useActionState` for the result/pending, `useFormStatus` for a nested submit button's pending — submitting `x-www-form-urlencoded` even if JS hasn't hydrated) and **Server Actions** (Next/Remix) reclaim the native model with server-side handling + progressive enhancement. Date this — it's a live shift, and the heavy reliance on `useActionState`/Server Actions can conflict with legacy client-side resolvers (verify the current React 19 / framework state under `notes.unverified`).
- **The form-engine choice** — the practice default is **react-hook-form + a Zod resolver** (uncontrolled/ref-based for performance + schema validation), with **React Aria's native validation** (the `ValidationResult` + native Constraint Validation, the `validationBehavior: 'aria'` route) as the a11y-first alternative and **Formik** (controlled) as the legacy/heavier option. The engine owns field registration, the validation mode, the error state, and `isSubmitting`/`isDirty`.
- **Schema-driven vs the Constraint Validation API** — the native HTML5 Constraint Validation API (`required`/`min`/`max`/`pattern`/`checkValidity()`) is fast and JS-free but can't do **cross-field validation** (end-date ≥ start-date) and styles custom messages inconsistently across browsers; modern practice favours a **schema** (Zod/Yup/Valibot) via a `resolver` (the engine runs `safeParse`, maps the `ZodError` array back to field names to trigger the error UI).
- **The validation escalation** — orchestrate across fields with the two-prop model: **`validationMode: onSubmit`** (validate everything on submit + route focus to the summary) plus **`reValidateMode: onChange`** (once a field is *in error*, re-validate on change so the error clears the moment the user fixes it — reward early), with **on blur** validating a *touched* field before submit. Don't validate on load or first keystroke (nagging an empty field is hostile). This is "reward early, punish late" at the form level (Inline Message's field-side rule — see inline-message).
- **The server-error-to-field mapping** — client validation is UX; the **server is the source of truth** (the same boundary File Upload drew — see file-upload). On a server-rejected submit (a 400), map each server error back onto its field (`validationErrors` / `setError`) *and* surface a form-level message; never a generic failure that loses which field is wrong.
- **The error-summary + focus + scroll** — build the summary from the error map, render it at the top (`role=alert`), move focus to its `tabindex=-1` heading, and scroll it into view; each link targets its field's id (the compound-field sub-target — §6) and moves focus there.
- **Prevent double-submit + the pending lock** — disable/lock the submit during the in-flight request (the Button loading state — see button), guard against a second submit (a ref/flag, or `preventMultiSubmit`/`useFormStatus`), and re-enable on success/error.
- **The dirty-form unsaved-changes guard** — track `isDirty`; when dirty, warn on navigation away (the `beforeunload` event for tab close/refresh; the router's navigation guard for SPA route changes); clear the guard on successful submit.
- **The autocomplete tokens (+ the two traps)** — set the right `autocomplete` token per field (`given-name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `one-time-code`, `new-password`/`current-password`); WCAG 1.3.5 (§9). **Trap 1:** `autocomplete="off"` is largely **ignored** by browsers/password managers (using it to force manual entry is an anti-pattern; if disabling is genuinely required, use a semantic token like `new-password`). **Trap 2 — the password-manager icon overlap:** LastPass/1Password/Bitwarden inject clickable icons into recognized inputs that **overlap a custom right-aligned icon** (a reveal-password toggle, a clear button), rendering both unclickable — allocate spatial padding for the injection or use the extension ignore attribute (`data-lpignore="true"`).
- **The uncontrolled-vs-controlled performance trade** — controlled forms (every keystroke in React state — Formik/Redux Form) re-render the whole form per keystroke and degrade on large forms; uncontrolled/ref-based (react-hook-form) isolates re-renders to the changed field. Default uncontrolled for anything non-trivial.
- **Headless vs opinionated** — the validation engine + the field-state machine + the form-state are heavy headless logic (react-hook-form / TanStack Form / React Aria); the layout/field-wrapper/summary are the design system's. **Build on a form engine**; don't hand-roll the validation-mode escalation and the field-registration.

## 12. Related and alternative components
- **Composes:** **all the form controls** — Text Field, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Date Picker, File Upload (the orchestrator they plug into — see text-field, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload) — plus **Button** (the submit/reset + the pending lock — see button) and **Inline Message** / **Banner** (the field error + the form-level message — see inline-message, banner).
- **Builds on:** **Inline Message** (the field-level error *is* Inline Message; the form-level error summary is the **surviving form-level live region** Inline Message pointed to — see inline-message) and **Text Field** (the field-stack / `aria-describedby` chain generalised to the FormField wrapper — see text-field).
- **Borders (the component-vs-pattern boundary):** the **Forms-as-a-system pattern** — the multi-step **wizard**, the long multi-section flow, save-and-resume (the **pattern**, forward-referenced to the patterns layer, *not* this component; the wizard owns routing + global state, the Form governs each step); the **Filter set** (fields applied without a submit — the Filtering pattern).
- **Closes:** the **Form category** (the controls + Inline Message + the Form orchestrator).
- **Alternative to:** a single auto-saving control (no submit), a Filter set (no submit/summary).

(The compositional owner that closes the Form category — the `<form>` primitive + the validation orchestration + the submission contract + the error summary, the orchestrator every form control plugs into. It composes the controls + Button + Inline Message, builds on Inline Message's field-error/form-summary split + Text Field's field-stack, and borders the Forms-as-a-system PATTERN (the wizard — forward-referenced to the patterns layer). See text-field for the field substrate, inline-message for the field-error/live-region split, button for the submit/pending, file-upload/date-picker for the composite controls it orchestrates. 03-component-library; 29 for the docs template; the coming patterns layer for Forms-as-a-system.)

## 13. Field POV evolution
1. **The native `<form>` → the controlled JS form.** Forms began as native `<form>` + synchronous POST round-trips with server-side validation; the SPA era moved state into JS, and **Redux Form / early Formik** standardized the controlled-form model (every value in state) — which notoriously degraded on large forms (cascading re-renders).
2. **The uncontrolled / performance turn + schema validation.** **react-hook-form** moved to uncontrolled/ref-based registration (re-render only on validation-state change), and **Zod/Yup/Valibot** schemas (via resolvers) became the validation source of truth — separating the schema from the UI and adding type safety.
3. **The platform reclaiming the form.** **React 19 form Actions** (`useActionState`/`useFormStatus`) and **Server Actions** (Next/Remix) brought back the native-form model with progressive enhancement + server-side handling — the form works without JS again, enhanced when it loads; state shifts back toward the server boundary.
4. **The accessible error-summary standardizing.** The **GOV.UK** error-summary + focus-management pattern became the accessible-forms reference (summary at top, focus to it, links to fields), and the validation strategy settled on **"reward early, punish late"** (validate on submit, re-validate on change once errored).

## 14. Sources cited
*(Conservative; the React 19 / Server Actions platform state + 2026 versions flagged unverified under §15.)* WAI-ARIA APG + the **GOV.UK Design System** (the gold-standard accessible-forms guidance + the **error-summary** pattern + the question-protocol); **React Aria** (the `Form` component + native validation behaviors + the `ValidationResult` model + `validationBehavior` native/aria + `validationErrors` server-mapping; 2024); **react-hook-form** (the uncontrolled/ref engine + the resolver model + `validationMode`/`reValidateMode`); **Formik** / **TanStack Form** / **Final Form** (the controlled / modern engines); **Zod / Yup / Valibot** (the schema-validation libraries; + `zod-i18n`); **React 19** (form Actions / `useActionState` / `useFormStatus`) + **Next.js / Remix** (Server Actions, 2024); the native **Constraint Validation API** + the **`autocomplete`** spec (WHATWG HTML); **IBM Carbon** (`Form` / `FormGroup`, v11), **Shopify Polaris** (`Form`, 2024), **Ant Design** (`Form` — the rules/validation model, the most feature-complete, v5), **Microsoft Fluent** (2024), **MUI** (`FormControl`, v5). WCAG 2.2 — 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7, 1.3.5, 4.1.3.

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
  escalation (the two-prop validationMode + reValidateMode model — submit -> blur-when-touched
  -> change-when-errored; reward early, punish late), the error-summary + focus-on-submit
  pattern (GOV.UK — focus the summary not the first field, link to each field; the surviving
  form-level live region Inline Message pointed to), and the submission lifecycle + progressive
  enhancement (native <form> + novalidate; React 19 Actions / Server Actions).
anatomy:
  parts:
    - "the <form> element: the onSubmit/action, the implicit-submit (Enter in a single text field), the native submit semantics, + novalidate to suppress the native validation bubbles in favour of custom UI"
    - "the FormField/Field wrappers: a context boundary auto-binding id/aria-labelledby/aria-describedby, wiring label + control + helper + error per field (Text Field's field stack generalised to wrap ANY control)"
    - "the field groups: Fieldset + legend for related fields + radio/checkbox groups (the legend is the group's accessible name — keep concise; some SRs announce it before every contained input)"
    - "the error summary: a top-of-form block (role=alert, on failed submit) with a heading + an unordered list of each error as a LINK to its field; the focus target"
    - "the form-level message: a Banner/Inline Message for the whole-form success/fatal-error (a 500) not mappable to a field (distinct from per-field errors + the validation summary)"
    - "the submit/reset Button(s) + the pending state (the loading lock); reset rare/discouraged; multiple submits via formaction"
    - "the required/optional marking: a consistent indicator (mark optional, or mark required — never neither)"
    - "the field layout: single-column by default, the Stack rhythm; Fieldset grouping for sections"
api:
  composes: [text-field, textarea, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload, button, inline-message, banner]
  builds-on: [inline-message, text-field]
  props:
    - {name: "onSubmit(values) / action", type: "fn", default: ~, required: false, description: "the submit handler (controlled) or the native/Server Action (PE; React 19 action accepts a server action compatible with useActionState)"}
    - {name: validationBehavior, type: "'native'|'aria'", default: aria, required: false, description: "native HTML constraint validation BLOCKS submission vs the engine handles errors via ARIA without blocking the native submit (preferred for custom logic)"}
    - {name: validationMode, type: "'onSubmit'|'onBlur'|'onChange'|'onTouched'|'all'", default: onSubmit, required: false, description: "when validation FIRST fires"}
    - {name: reValidateMode, type: "'onSubmit'|'onBlur'|'onChange'", default: onChange, required: false, description: "when validation RE-fires after a failed submit (the rapid error-recovery half — reward early)"}
    - {name: resolver, type: "Zod|Yup|Valibot schema | native validate", default: ~, required: false, description: "schema-driven (RHF resolver runs safeParse, maps ZodError back to field names) or React Aria native / Constraint Validation"}
    - {name: defaultValues, type: object, default: ~, required: false, description: "the initial values (uncontrolled-friendly; edit/update mutations + caching)"}
    - {name: "form-state", type: "isSubmitting/isValid/isDirty/errors/isSubmitSuccessful", default: ~, required: false, description: "the form state machine"}
    - {name: validationErrors, type: "Record<field, string[]>", default: ~, required: false, description: "server-side error mapping — translates backend errors back onto field names (React Aria/Spectrum's bridge)"}
    - {name: preventMultiSubmit, type: boolean, default: true, required: false, description: "disable the submit during a pending submission"}
    - {name: "model", type: "'uncontrolled'|'controlled'", default: uncontrolled, required: false, description: "uncontrolled/ref (react-hook-form — performance) vs controlled (Formik — re-render cost)"}
    - {name: autocomplete-wiring, type: "per-field tokens", default: ~, required: false, description: "the autocomplete token per field (WCAG 1.3.5)"}
  withholds: "doesn't reinvent the controls (composes them) or the field-level error (Inline Message); adds the orchestration + submit + summary + layout"
states:
  form: [idle, validating, submitting, success, error]   # submitting = the pending lock (submit loading, mutations blocked, double-submit prevented); error = client schema rejection or server 400 -> summary mounts + hijacks focus
  field-orchestrated: [pristine, dirty, untouched, touched, valid, invalid]   # dirty -> the unsaved-changes guard; touched -> the metric escalating validation uses
  submit-button: [enabled, pending, disabled]   # NOT disabled-until-valid (hides why; a disabled button isn't focusable/announced)
variants:
  layout: [single-column, multi-column, inline]   # single-column DEFAULT; multi only for short tightly-coupled units
  grouping: [flat, fieldset-grouped]
  whole-form: [editable, read-only, disabled-during-submit]
  submit-model: [native-progressive-enhancement, controlled-js, server-action]
accessibility:
  wcag-criteria: ["3.3.1", "3.3.2", "3.3.3", "3.3.4", "3.3.7", "1.3.5", "4.1.3"]
  builds-on: [inline-message (the field-error/form-summary split), text-field (the aria-describedby chain)]
  error-summary: "THE crux (GOV.UK) — on a FAILED SUBMIT render a top-of-form summary (role=alert, 'There is a problem') listing each error as a LINK to its field; MOVE FOCUS to the summary HEADING (tabindex=-1; NOT the first field — so the user hears the full list); each link jumps focus to its field. For a COMPOUND field (a 3-part date) the link targets the specific failed sub-field (the year), not the fieldset. The SURVIVING form-level live region (Inline Message abandoned field-level live regions for aria-describedby + focus; it lives here)"
  field-error-association: "each invalid field gets aria-invalid=true + the error message id appended to aria-describedby (the Text Field / Inline Message chain — inherited); tabbing in announces label+value+type+error. The Form orchestrates WHEN it appears, the wiring is the field's"
  required-invalid: "aria-required (or native required) on required fields; the error text in described-by; the summary announces the count"
  fieldset-legend: "related fields + radio/checkbox groups in <fieldset> + <legend> (the group's accessible name); DON'T over-fieldset (a legend on every field is noise)"
  submit-feedback: "the form-level success/error announces (role=status/alert — the Banner lineage); the pending state announced (the submit Button loading)"
  implicit-submit: "Enter in a single-line field submits (preserve the native behavior — requires a genuine <button type=submit>, never a stylized div); the submit Button reachable + Enter/Space-activatable"
content:
  labels-errors: "clear top-aligned labels + helper + specific actionable errors (inherited from Text Field / Inline Message)"
  summary-copy: "a clear title ('There is a problem'); each entry restates the field error as a link ('Enter your email address'); the summary text must EXACTLY match the inline field error (mismatch = cognitive dissonance)"
  inline-error-copy: "actionable + specific ('Enter your first name' / 'Password must be at least 8 characters'); never generic ('Invalid input') or accusatory/technical ('illegal value', 'forbidden')"
  required-optional: "explain the * ('All fields required unless marked optional'); be consistent"
  submit-label: "a SPECIFIC verb ('Create account' / 'Save changes' / 'Pay now'), NOT a generic 'Submit'"
  success: "confirm what happened ('Your changes were saved') + what's next"
  legends: "the <legend> is the group's primary label (the exact phrase, e.g. 'Preferred contact method'), not a stray paragraph above the inputs"
motion:
  error-summary: "on failed submit the summary appears at the top (rapid slide-down/fade) + the page scrolls to it (focus moved; scroll-behavior:smooth helps sighted users); immediate, not a slow animation"
  field-error-reveal: "the field error appears in its reserved slot; mounting BELOW an input pushes fields down (CLS -> mis-clicks) -> reserve a fixed min-height for the error slot or absolutely-position the error text (pad for multi-line). The Inline Message layout-shift discipline"
  submit-pending: "the submit Button -> its loading state, snappy (~100-150ms; the Button/Spinner transition)"
  success: "the form-level success message (the Banner/Toast enter)"
  reduce-motion: "keep the scroll-to-error + summary appearance instant + drop decorative transitions; the error info is the point, not the motion"
i18n:
  copy: "labels/helper/errors/summary/submit-label/success translate (the field copy inherited)"
  rtl: "the field layout + the label/required-marker placement (the marker shifts side) + the error summary alignment/padding + the submit alignment mirror via logical properties"
  address-locale-variance: "name order (given/family) + address fields (postal-code/state/city order + presence) + phone format vary by country — the API must allow dynamic reorder/hide/relabel by locale WITHOUT breaking the schema; don't hardcode a US shape (the Date Picker locale-derived lineage)"
  autocomplete-token: "the tokens are locale-INDEPENDENT (a stable WHATWG vocabulary, browser-recognized regardless of display language — WHY you trigger password managers via the spec token, not localized label text); the FIELDS they map to vary by locale"
  validation-message-locale: "schema/engine error messages need an i18n layer (Zod/Yup emit English by default -> intercept + map, e.g. zod-i18n); don't ship English validation strings to a localized form"
implementation:
  - "native <form> + a real <button type=submit> + novalidate (suppress native validation bubbles for custom UI) + progressive enhancement (works without JS) + the platform shift: React 19 form Actions (<form action={fn}> not e.preventDefault(); useActionState for result/pending; useFormStatus for a nested submit's pending; submits x-www-form-urlencoded even un-hydrated) + Server Actions (Next/Remix). DATE this — useActionState/Server Actions can conflict with legacy client-side resolvers; verify current"
  - "the form-engine choice: PRACTICE DEFAULT react-hook-form + a Zod resolver (uncontrolled/ref + schema), with React Aria native validation (ValidationResult + Constraint Validation; validationBehavior:aria) as the a11y-first alternative + Formik (controlled) as legacy/heavier. The engine owns field registration, the mode, errors, isSubmitting/isDirty"
  - "schema-driven vs the Constraint Validation API: native HTML5 (required/min/max/pattern/checkValidity()) is fast + JS-free but can't do cross-field validation (end>=start) + styles custom messages inconsistently; modern practice favours a schema (Zod/Yup/Valibot) via a resolver (safeParse -> map ZodError to field names)"
  - "the validation escalation (two-prop): validationMode:onSubmit (validate everything + focus the summary) + reValidateMode:onChange (once a field is IN ERROR, re-validate on change so it clears as the user fixes — reward early), with on-blur validating a TOUCHED field before submit. DON'T validate on load/first keystroke. 'Reward early, punish late' (Inline Message's field-side rule)"
  - "the server-error-to-field mapping: client validation is UX, the SERVER is the source of truth (the File Upload boundary). On a 400, map each error back onto its field (validationErrors/setError) + surface a form-level message; never a generic failure that loses which field is wrong"
  - "the error-summary + focus + scroll: build from the error map, render at the top (role=alert), move focus to its tabindex=-1 heading, scroll into view; each link targets its field id (the compound-field sub-target) + moves focus there"
  - "prevent double-submit + the pending lock: disable/lock the submit during the in-flight request (the Button loading), guard a second submit (a ref/flag, preventMultiSubmit, or useFormStatus), re-enable on success/error"
  - "the dirty-form unsaved-changes guard: track isDirty; when dirty, warn on navigation away (beforeunload for tab close/refresh; the router guard for SPA route changes); clear on successful submit"
  - "the autocomplete tokens + the TWO TRAPS: the right token per field (given-name/email/tel/street-address/postal-code/cc-number/one-time-code/new-password/current-password; WCAG 1.3.5). Trap 1: autocomplete=off is largely IGNORED (forcing manual entry is an anti-pattern; if disabling is required use a semantic token like new-password). Trap 2 — the PASSWORD-MANAGER ICON OVERLAP: LastPass/1Password/Bitwarden inject clickable icons that overlap a custom right-aligned icon (reveal/clear) -> pad for the injection or use the ignore attribute (data-lpignore=true)"
  - "the uncontrolled-vs-controlled performance trade: controlled (every keystroke in state — Formik/Redux Form) re-renders the whole form per keystroke + degrades on large forms; uncontrolled/ref (react-hook-form) isolates re-renders to the changed field. Default uncontrolled for anything non-trivial"
  - "headless vs opinionated: the validation engine + field-state machine + form-state are heavy HEADLESS logic (react-hook-form / TanStack Form / React Aria); the layout/field-wrapper/summary are the design system's. BUILD ON A FORM ENGINE — don't hand-roll the validation-mode escalation + field-registration"
composition:
  composes: [text-field, textarea, select, combobox, checkbox, radio, switch, slider, date-picker, file-upload, button, inline-message, banner]
  builds-on: [inline-message, text-field]
  closes: "the Form category (the controls + Inline Message + the Form orchestrator)"
  borders: ["the Forms-as-a-system PATTERN (the multi-step wizard / long multi-section flow / save-and-resume — forward-referenced to the patterns layer, NOT this component; the wizard owns routing + global state, the Form governs each step)", "the Filter set (fields applied without a submit — the Filtering pattern)"]
  alternative-to: ["a single auto-saving control (no submit)", "a Filter set (no submit/summary)"]
  supersedes: null
  superseded-by: null
notes:
  contested:
    - "the validation strategy — onSubmit (the safe default) vs aggressive onChange; the practice escalates validationMode:onSubmit + reValidateMode:onChange + blur-when-touched (reward early, punish late)"
    - "the form engine — react-hook-form + Zod (uncontrolled, practice default) vs React Aria native validation (a11y-first, validationBehavior:aria) vs Formik (controlled, heavier)"
    - "submit-disabled-until-valid — a common ANTI-PATTERN (hides why, a disabled button isn't focusable/announced); keep submit enabled + route focus to the summary"
    - "native <form> + React 19 Actions / Server Actions (the platform reclaiming) vs a fully controlled JS form"
    - "the COMPONENT-VS-PATTERN line — the Form primitive (this component) vs Forms-as-a-system / the multi-step wizard (the PATTERN, forward-referenced)"
    - "required-vs-optional marking — mark optional (if most required) or mark required (if most optional), NEVER neither; practice marks optional (data-minimalism -> most fields required)"
    - "validationBehavior native (blocks submit) vs aria (custom logic, no native block) — practice default aria"
  trap:
    - "submit-disabled-until-valid (hides the reason; AT can't focus a disabled button) — keep enabled, validate on submit, focus the summary"
    - "focusing the first field instead of the error summary on failed submit (GOV.UK: focus the summary so the user hears the full list); a summary link targeting the fieldset instead of the failed sub-field"
    - "field-level live regions (the double-announcement bug Inline Message resolved) — the live region survives only at the form/summary level"
    - "autocomplete=off broadly (browsers ignore it + it harms password managers); missing autocomplete tokens (WCAG 1.3.5); the password-manager-icon overlap on a custom right-aligned input icon (pad or data-lpignore)"
    - "a controlled form re-rendering on every keystroke (use uncontrolled/ref for large forms); losing the user's input on a submit error"
    - "hardcoding a US address/name shape (drive from locale/country); shipping English validation strings to a localized form"
    - "over-fieldsetting (a legend on every field is noise); a generic 'Submit' button label (use a specific verb); a summary error text that doesn't match the inline error text"
    - "the error-slot CLS (mounting the error below the input pushes fields down -> mis-clicks); a stylized div pseudo-button breaking implicit submit"
  inherited: "Inline Message's field-error model + the form-level-live-region split; Text Field's field-stack + aria-describedby chain + top-label default; Button's submit + loading/pending + the specific-verb label; the Stack rhythm for field spacing; Fieldset/legend from Checkbox/Radio; the client-UX-server-truth validation boundary from File Upload"
  role-in-family: "the compositional OWNER that CLOSES the Form category — the <form> primitive + the validation orchestration + the submission contract + the error summary; the orchestrator every form control plugs into; borders the Forms-as-a-system PATTERN (the wizard)"
  evolution:
    - "the native <form> -> the controlled JS form (Redux Form / Formik — re-render degradation)"
    - "the uncontrolled/performance turn (react-hook-form) + schema validation (Zod/Yup/Valibot)"
    - "the platform reclaiming the form (React 19 Actions / useActionState/useFormStatus / Server Actions + progressive enhancement)"
    - "the accessible error-summary standardizing (GOV.UK: summary at top, focus to it, links to fields) + the validation strategy settling (reward early, punish late)"
  unverified:
    - "the React 19 form Actions / useActionState / useFormStatus API + the Next/Remix Server Actions state (+ the conflict with legacy client-side resolvers) — verify against current platform"
    - "external 2026 version numbers (react-hook-form, React Aria Form, Ant Form v5, Zod/Valibot)"
    - "the GOV.UK error-summary current guidance specifics (focus-the-summary, the compound-field sub-target) — verify against the current GOV.UK Design System"
    - "the single-column completion/error-rate figures (the ~120% fewer-errors claim) — a commonly-cited research stat, verify the source"
```

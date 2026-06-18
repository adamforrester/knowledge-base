# Form — external-agent pass

## Identity
The Form component is the compositional owner and macro-orchestrator of the Form category — the structural/logical container individual controls plug into. A persistent wrapper-vs-orchestrator tension resolves into three identities: **Form** (top-level orchestrator — the native `<form>`, validation protocols, the submission lifecycle, the top-of-form error summary), **FormField / Field / FormControl** (the compositional wrapper wiring label + control + helper + inline error; Fluent 2024, MUI v5, React Aria 2024 codify it as a context-providing boundary that auto-binds `id`/`aria-labelledby`/`aria-describedby`), and **Fieldset / FormGroup** (the `<fieldset>`/`<legend>` grouping for radio groups / compound address fields). Opinionated default: `Form` for the root, `FormField` for the wrapper.

## Description
The native `<form>` primitive enhanced by a unified submission contract, centralized validation orchestration, accessible error summaries, and progressive enhancement. It does not reinvent substrates — controls own their internal a11y mappings; inline messages own field-level error rendering. The component-vs-pattern duality: the **component** (this spec) is the atomic, briefable compositional unit (validation escalation, schema validation, the error summary, focus-on-failure, pending state machines, single-column rhythm, the autofill contract); **forms-as-a-system** (multi-step wizards, long-form segmented flows, save-and-resume, cross-page persistence) belongs to the patterns layer (Polaris 2024, Carbon v11 delegate multi-step to template patterns). Field-level ARIA live regions are abandoned in favor of `aria-describedby` + focus management; the live region survives solely at the form level (the top-of-form error summary).

## Anatomy
- **Form Root** `<form>` — the submit event, implicit submission via Enter, `novalidate` to suppress native browser validation popups in favor of custom UI.
- **Error Summary** `<div role="alert">` — rendered conditionally at the top on failed submit; a heading + an unordered list of anchor links to invalid field IDs.
- **Fieldset Group** `<fieldset>` — clusters related controls (radios/checkboxes) so SR announces the shared context first.
- **Legend** `<legend>` — the accessible name for the fieldset; concise (announced for every contained input by some SRs).
- **Field Wrapper** (`FormField`) — the macro-wrapper coordinating label + control + helper/error, generating unique IDs + ARIA associations.
- **Global Banner** — a form-level success/fatal-error message (e.g. 500) not mappable to a field; distinct from the validation summary.
- **Submit Action** `<button type="submit">` — managed by the pending state to prevent double-submit.

## API
- `action: string | function` — submission endpoint; in React 19, a server action compatible with `useActionState` (progressive enhancement).
- `onSubmit: function` — legacy/client-side handler; fired only after validation clears.
- `validationBehavior: 'native' | 'aria'` (default `aria`) — native HTML constraint validation blocks submission (native) vs the engine handles errors via ARIA without blocking the native submit (aria, preferred for custom logic).
- `validationMode: 'onSubmit' | 'onBlur' | 'onChange' | 'onTouched'` (default `onSubmit`) — when field validation is FIRST triggered.
- `reValidateMode: 'onSubmit' | 'onBlur' | 'onChange'` (default `onChange`) — when validation re-triggers AFTER a failed submit (rapid error recovery).
- `resolver: function` — the schema-library bridge (Zod/Valibot/Yup).
- `defaultValues: object` — initial data (controlled inputs, update mutations, caching).
- `validationErrors: Record<string, string[]>` — server-side error mapping (backend strings → field names).
- `preventMultiSubmit: boolean` (default `true`) — disables the submit during a pending submission.

## States and Variants
Macro state machine (independent of fields): idle → validating → submitting/pending (submit lock, button loading, mutations blocked) → success (clear/redirect/confirmation banner) | error (client schema rejection or server 400 → the summary mounts + hijacks focus). Atomic field states: pristine → dirty (unsaved-changes guards rely on aggregate dirty); untouched → touched (the metric escalating validation uses). 

**Anti-pattern: disabling submit until valid.** A disabled button gives zero feedback, leaves the user guessing which field they missed, and can't receive keyboard focus (degraded AT). Default: keep submit enabled at all times; click → run validation → surface errors → move focus to the summary.

Layout: **single-column default** (faster completion, fewer errors — up to ~120% fewer in complex tasks; linear scanning path). Multi-column is the exception, only for tightly-coupled units (first+last name, city/state/zip). Requirement indicators: a rigid binary — mark required consistently (asterisk) OR mark optional consistently ("(optional)"), never mix/neither. GOV.UK + inclusive standards: request only necessary info (most fields required) → mark the rare optional fields with text.

## Usage Guidance
Deploy the Form orchestrator when multiple fields + cross-field validation + a discrete submission to a backend; single auto-saving fields or client-side filter sets bypass it. Default single-column (mobile/magnification users miss right-periphery fields); if multi-column is unavoidable, columns visually distinct + tab order follows visual flow. Data minimalism — eliminate non-actionable fields rather than mark them optional; spell out "optional" (asterisks misunderstood by lower digital literacy + SR issues without `aria-hidden`). Promote to a multi-step wizard (the pattern) past ~10 fields, disparate sections, or external-document gathering — the Form governs each step; the wizard owns progression/draft-saving/cross-step validation.

## Accessibility
The crux: the **GOV.UK Error Summary pattern**. On failed submit, render an ErrorSummary at the top wrapped in `<div role="alert">`; JS programmatically hijacks focus to the summary's heading (injected `tabindex="-1"` since headings aren't focusable). The summary lists each error as an anchor `<a href="#field-id">`; activating it jumps focus to the input. For compound fields (a three-part date input), the link targets the specific failed sub-field (e.g. the year), not the generic fieldset. Field-level: the invalid input gets `aria-invalid="true"` + the error message's id appended to `aria-describedby`. The implicit-submission contract: Enter in a single-line input submits — requires a genuine `<button type="submit">`, not a stylized div. WCAG 1.3.5: `autocomplete` with WHATWG tokens (given-name, email, tel, street-address) — a critical accessibility enhancement for motor/cognitive users, not mere convenience.

## Content Guidelines
Error-summary copy direct ("There is a problem" / "Please fix the following errors"); summary list items must EXACTLY match the inline field error text. Inline errors actionable + specific ("Enter your first name", "Password must be at least 8 characters"), never "Invalid input" / "An error occurred"; prohibit accusatory/technical jargon ("illegal value", "forbidden"). Submit labels = descriptive verbs ("Create account", "Save changes", "Pay now"), never "Submit". The `<legend>` is the group's primary label (the exact phrase, e.g. "Preferred contact method").

## Motion and Transition
Error-summary appearance sudden but not jarring (slide-down/fade, bound to `prefers-reduced-motion`); link-to-field navigation can use `scroll-behavior: smooth` (motion-preference-respecting). Pending submit transition snappy (100–150ms). The CLS trap: error messages mounting below inputs push elements down (Cumulative Layout Shift, accidental clicks) → reserve a fixed min-height for the error slot, or absolute-position the error text (with careful padding for multi-line).

## Internationalization
RTL: full mirror — the required marker shifts side, the summary text-align/padding switch. Locale variance: Western First/Last names don't apply globally; address formats vary (ZIP/postal/sorting codes, state/province) — the API must allow dynamic reorder/hide/relabel by locale without breaking the schema. Validation messaging needs an i18n layer — Zod/Yup emit English by default; intercept + map through (e.g. zod-i18n). The `autocomplete` tokens are universally browser-recognized regardless of display language (use the WHATWG spec, not localized label text, to trigger password managers).

## Naming
`Form` (universal — React Aria 2024, Polaris 2024, Ant v5, Carbon v11); `FormField`/`Field`/`FormControl` (FormControl in MUI v5/Chakra; Field in TanStack/RHF; default `FormField`); `Fieldset`/`FormGroup` (Carbon `FormGroup`; native-semantics systems prefer `Fieldset`).

## Implementation Notes
**Validation crux — escalate, don't annoy** ("reward early, punish late"): (1) no validation on load/initial typing; (2) validate on submit (halt, mount the ErrorSummary, reveal all inline errors); (3) re-validate on change once a field is in error (instant clear on fix — reward early); (4) validate on blur for touched-but-not-submitted fields. **Schema-driven vs Constraint Validation API**: native HTML5 (`min`/`max`/`pattern`/`required`/`checkValidity()`) is fast + JS-free but lacks cross-field validation (End ≥ Start) + inconsistent custom-message styling; modern practice favors schema (Zod/Yup/Valibot) via a `resolver` (the engine — RHF/TanStack — runs `safeParse`, maps the `ZodError` array back to field names). **Progressive enhancement + React 19**: Formik controlled every keystroke (re-render bottleneck) → RHF uncontrolled/refs (re-render only on validation-state change) → React 19 native Actions + `useActionState` + `useFormStatus`: pass an action to `<form action={formAction}>` (not `e.preventDefault()`), submit via native `x-www-form-urlencoded` even if JS fails, the hooks natively expose a `pending` boolean (no manual `isSubmitting`). **Client vs server**: client = UX, server = truth; on a 400, map the server payload back into the error state (the `validationErrors` prop — React Aria/Spectrum — bridges it). **The autofill traps**: `autocomplete="off"` is largely ignored (using it to force manual entry is an anti-pattern); the **password-manager icon overlap** — LastPass/1Password/Bitwarden inject clickable icons into recognized inputs that overlap a custom right-aligned icon (reveal-password/clear), rendering both unclickable → use extension ignore attributes (`data-lpignore="true"`) or pad the input for third-party injections. **Unsaved-changes guard**: track `isDirty` → attach a `beforeunload` listener (+ the SPA router guard); the browser shows the native "unsaved changes" dialog.

## Related and Alternative Components
Composes all controls (TextField/Select/Combobox/Checkbox/Radio/Switch/Slider/DatePicker/FileUpload); composes InlineMessage (slot errors) + Banner (global success/failure); borders the Forms-as-a-system pattern (the wizard governs routing/global state, the Form governs each step); alternative — a Filter Set (client-side data manipulation without a submission event).

## Field POV Evolution
Native `<form>` (synchronous POST + server-side validation) → heavy fully-controlled JS (Redux Form / early Formik — re-render degradation) → uncontrolled/ref-based performance (RHF) + schema validation (Zod) → the platform reclaiming the form (React 19 Actions / useActionState / Next Server Actions 2024 — progressive enhancement, state back at the server boundary). Accessible error handling standardized on the GOV.UK Error Summary; the validation strategy settled on "reward early, punish late".

## Agent-Consumable Schema
*(JSON/YAML in the external pass; reconciled into the synthesized brief's §15. Key props: `action`, `onSubmit`, `validationBehavior` (native|aria, default aria), `validationMode` (default onSubmit), `reValidateMode` (default onChange), `resolver`, `defaultValues`, `validationErrors`, `preventMultiSubmit`. Unverified flag: heavy reliance on React 19 useActionState / Server Actions may conflict with legacy client-side validation resolvers.)*

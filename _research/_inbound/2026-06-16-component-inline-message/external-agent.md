# Inline Message — field-truth study (external agent pass)

*Filed verbatim as received from the user's external research agent, 16 June 2026. Reconciled into `components/inline-message.md`; version numbers and the describedby-vs-live-region AT specifics flagged unverified. The two passes converged almost completely; the external pass sharpened the announcement model to the settled no-field-level-live-region consensus and added the visually-hidden prefix, label parity, the layout-shift models, and the API topologies.*

---

Architectural Field-Truth Study: The Inline Message Component in Enterprise Design Systems

## 1. Framing
The Inline Message is the atomic unit of contextual feedback, at the intersection of Feedback and Form — the foundational primitive composite form controls (Text Field, Select, Checkbox Group, Textarea) use to convey field-specific validation, requirements, and helper descriptions. Unlike standalone Banners (page/section boundaries) or Toasts (transient system feedback), it is strictly contextual, state-bound, and tethered to the surface it describes. Two scopes: field-level (bound to a single control, occupies the helper/error slot; controls compose the primitive, passing state via Context APIs) and section-level (scoped to a fieldset/group, strips the heavy Banner fill). Divergence stems from reconciling the scopes and the announcement model — the tension between structural association (aria-describedby on a focused input) and dynamic interruption (live regions via role=alert/aria-live) — plus the temporal logic of when the message is injected (eager-as-you-type vs lazy-on-blur vs on-submit).

## 2. Anatomy
Severity icon (inherits Icon; functional requirement for WCAG 1.4.1; token-mapped so a critical inline error uses the same SVG as a critical Banner). Text node (helper/validation payload; 12-14px step down; wraps infinitely — truncating validation text defeats the purpose). The assistive technology prefix (visually-hidden <span>Error:</span> injected before the text, GOV.UK; compensates where the red icon is ignored). Optional Link (routes to docs/policy). Strictly NO dismissibility — the message is a live reflection of DOM/input state, resolved only by correcting the field.

## 3. Properties / API
Two paradigms. Declarative string-passing (opinionated): parent accepts raw strings (Carbon invalidText, React Spectrum errorMessage/description); the parent instantiates the hidden primitive + handles ID generation + ARIA internally (guarantees compliance, low friction; limits complex HTML). Composable slot mapping (headless): developer renders the validation node as a child (Primer FormControl.Validation, MUI FormHelperText error); allows infinite composition (lists/links); requires Context API to secretly wire the child ID to the parent input's aria-describedby (else accessibility linkages are severed). Core: state/variant enum (error/warning/success/info — Fluent validationState toggles tokens + swaps icon). Critical: explicit id linking — if outside an automated Context wrapper, accept an id matching the field's aria-describedby; failure severs the a11y tree.

## 4. States and variants
Helper-to-Error slot swap: neutral state shows helper ("Password must be at least 8 characters"); on invalid, helper is aggressively unmounted and entirely replaced by error ("Password is too short") — React Spectrum hides description from the DOM if validationState=invalid + errorMessage present. Severity matrix: Helper (subdued gray, no icon, read as describedby on focus), Error (red, alert icon, blocks submit, aria-invalid=true, prefixed "Error:"), Warning (yellow/orange, allows submit, aria-invalid generally NOT applied), Success (green check, async positive reinforcement). Error Summary (GOV.UK): structured component at the top of a form; on submit with multiple errors, renders a list of hyperlinked error strings matching the field-level text 1:1; clicking shifts focus to the offending input.

## 5. Usage guidance
Boundaries: Inline Message = direct response to a state (encapsulates static helper + dynamic state indicator); Banner = page/section status, dismissible; section-level Inline Message for a specific grouping (failed multi-input date field), never dismissible; Toast = transient — form validation must NEVER use Toasts (they disappear on a timer, removing the context needed to fix). Eager validation (erroring on focus/first character) is strictly prohibited; defer to onBlur or submit. GitHub Primer's "Reward-Early / Punish-Late": valid/pristine fields are punished late (validate on blur); once a field is invalid, switch to eager onChange so the error disappears the keystroke the constraint is met (reward early). Cross-field constraints ("end date cannot precede start date") → section-level message above the fieldset, not field-level blame on one input.

## 6. Accessibility
The core debate: how does a screen reader become aware of a dynamically invalid field — structural association vs dynamic interruption. aria-describedby (static): canonical standard, ID on the input referencing the message container; reads on focus; highly reliable, non-interruptive; paired with aria-invalid=true. Live region (role=alert): interrupts speech to announce on DOM insertion; strongly deprecated for field-level errors. Hybrid (both): the catastrophic Double-Announcement Bug — on submit, JS injects errors into live regions AND moves focus to the first invalid field; the SR reads the message twice (once from the live-region mutation, once from describedby on focus); race condition. Android Material 3 TalkBack documented similar double-announce when custom semantics overlay the TextField supporting text. Field leaders diverged from live regions for field-level errors: GitHub Primer "removes live region from FormControl validation" and mandates "Live regions should not be used for form validation" — the standard relies on Focus Management + aria-describedby (update DOM, set aria-invalid, force focus onto the invalid input). Adobe Spectrum hit WCAG 4.1.3 challenges when Enter submitted an empty field (focus retained, message updated silently), prompting debate over a programmatic JS LiveAnnouncer vs static DOM live regions. The GOV.UK Error Summary (WCAG 3.3.1): on failure, a summary at the top gets role=alert / tabindex=-1, focus forced onto the summary heading; internal anchor links jump to the invalid fields. Color: WCAG 1.4.1 — never red border/text alone; the icon is mandatory. Text contrast >=4.5:1; icon/border >=3:1.

## 7. Content guidelines
Specific + actionable — what went wrong + how to fix; "First name must be 35 characters or less" / "Enter a valid email address, like name@example.com", never "Invalid input"/"An error occurred"/"This field is required". Forbid negative/hostile/technical language ("illegal"/"forbidden", raw exception codes, "You forgot..."); replace with neutral instruction ("Enter your first name"). No humour ("Oops!"). Label parity (GOV.UK): the error reuses the visible label's exact terminology ("How many hours...?" → "Enter how many hours..."); the field-level text must be a 1:1 identical match to the Error Summary text — discrepancies disorient SR users building a mental map.

## 8. Motion and transition
Layout shift management. Space Reservation (fixed min-height below the input regardless of presence) — eliminates shift but creates sparse forms. Dynamic Expansion (container grows, pushes content down) — enterprise default for tight rhythm (Carbon 32px); but a two-column grid requires grouped rows (if the left column expands for an error, the right must grow to match, maintaining horizontal alignment). Anti-pattern: position:absolute on the message (renders outside flow) — overlaps the next input's label, destroys readability on small viewports (common in custom MUI builds). Animation minimal-to-none; snap to completion under prefers-reduced-motion.

## 9. Internationalization
Text expansion up to 300% (German/Russian); never text-overflow:ellipsis (hiding constraints blocks the task); allow infinite multi-line wrap; layout-shift logic handles 2-4 lines on mobile. RTL: icon switches from left to right of the text, margin offset flips; logical CSS properties (margin-inline-start) handle natively. The visually-hidden "Error:" prefix must be exposed to translation (GOV.UK overrides it, e.g. "Gwall:" for Welsh) — a hardcoded English prefix before a localized message is disjointed.

## 10. Naming
Polaris InlineError (error-only). Spectrum HelpText / InlineAlert. Carbon invalidText / InlineNotification. Primer FormControl.Validation. MUI FormHelperText. Atlassian ErrorMessage / HelperMessage. Modern practice leans to generic structural naming (FormHelperText / FormControl.Validation) — accommodates the Helper-to-Error slot swap; an error-only name (InlineError) conceptually limits use and fragments the ecosystem.

## 11. Implementation notes
Deterministic IDs via useId(): the FormControl/Field generates a base prefix; label for=x, input id=x, InlineMessage id=x-validation, input aria-describedby=x-validation. Composable APIs use React Context / Vue Provide-Inject to pass the ID down so developers don't hand-match (the most common a11y failure). Static vs Dynamic: server-rendered error parses linearly (describedby handles announcement on tab-in); client-injected error must re-render, swap helper out, and update aria-invalid simultaneously. Error Summary: maintain a registry of input refs; onSubmit → preventDefault, compute errors, map to the summary, imperatively .focus() the summary container; anchor href maps to input id for native focus routing.

## 12. Related and alternative components
Text Field / Select / Checkbox Group: primary consumers — compose the Inline Message primitive internally (hierarchical: Inline Message is the substrate, controls are the composites). Banner: page/section boundary (heavy fill, dismissible). Toast: transient boundary (disappears — incompatible with validation). Icon: inherited severity substrate. Link: inherited documentation-routing substrate.

## 13. Field POV evolution
Native HTML5 constraint bubbles (required/pattern) fell out of favor (unstyleable, inconsistent SR behavior, restrictive timing). Custom JS validation era pushed aria-live=polite/role=alert on field errors → the catastrophic double-announcement bug in SPAs (focus management colliding with live-region mutations, chaotic on NVDA/JAWS). Current settlement (GOV.UK, GitHub Primer): abandon field-level live regions for bulletproof static DOM wiring — aria-describedby + aria-invalid + explicit focus routing; live regions survive at the form/summary level. Reward-early/punish-late timing. The Error Summary pattern's spread cements holistic accessible form architecture over isolated field punishment.

## 14. Sources cited
GOV.UK Design System (Error Summary, hidden "Error:" prefix, label parity). GitHub Primer React v36.x (FormControl.Validation, rejection of field-level live regions). IBM Carbon v11.x (invalidText, grouped-row layout-shift). Adobe Spectrum React v3.x (Helper-to-Error slot swap, LiveAnnouncer debate). Shopify Polaris v12.x/v3.13 (InlineError, severity-icon parity with Banners). Microsoft Fluent UI React v9 (validationState → semantic tokens + icon swap). Atlassian @atlaskit/form v7.x (MessageWrapper, ErrorMessage). MUI (FormHelperText). Ant Design (Form.Item help/validateStatus). Google Material 3 (supporting/error text, TalkBack double-announce). WAI-ARIA APG (Alert pattern, aria-describedby/aria-invalid association, live regions). WCAG 3.3.1, 3.3.3, 4.1.3, 1.4.1.

## 15. Agent-consumable schema

```yaml
name: Inline Message
aliases:
category: Feedback
interlocks: [Form]
description: A contextual, field-level or section-level feedback primitive displaying validation states, requirements, or helper text attached directly to a specific DOM node or fieldset.
inheritance:
  - Substrate: Icon (severity indication)
  - Substrate: Link (inline documentation routing)
  - Composed_by: [Text Field, Select, Textarea, Checkbox Group, Radio Group]
anatomy:
  - Severity Icon (required for warning/error per WCAG 1.4.1)
  - Message Payload (text node, infinite wrap)
  - Visually Hidden Prefix (AT enhancement, e.g. "Error:")
  - Interactive Links (optional)
properties:
  - severity/variant: [error, warning, success, info, none]
  - message/children: ReactNode | string
  - id: string (must map 1:1 with target aria-describedby)
accessibility:
  - field_association: aria-describedby on the target input pointing to message id
  - field_state: aria-invalid="true" when severity is error
  - live_region_policy: FORBIDDEN at field-level to prevent double-announcement
  - error_summary_policy: role="alert" or autofocus required on the top-level summary
  - color_contrast: 4.5:1 text, 3:1 icon/border (WCAG 1.4.3/1.4.11)
behavior:
  - timing: deferred to onBlur/onSubmit (punish-late); eager onChange upon correction (reward-early)
  - slot_swap: helper text unmounted and fully replaced by error on failure
  - layout_shift: container expands dynamically; grouped rows compensate laterally
  - dismissibility: FALSE (state-bound)
```

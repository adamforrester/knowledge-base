You are researching the Inline Message component for a senior design
systems practitioner at a digital agency. The output is a field-truth
study of how the leading design systems handle this component — what they
converge on, where they diverge, and what the practice's opinionated
default should be when starting from scratch.

This is not an introductory guide. Assume the reader knows what an inline
message / field validation message is, knows what a design system is, and
has shipped multiple component libraries. Explain the non-obvious — the
prop choices field leaders disagree on, the accessibility decisions still
contested, the implementation traps that recur across codebases.

Inline Message is the THIRD Feedback brief, and the one that INTERLOCKS
the Feedback category with the Form category. It is the field/section-level
message — the smallest, most contextual feedback surface, attached to a
specific control or scoped to a form section. It STANDS ON four substrates:
- THE FIELD-ASSOCIATION CHAIN is INHERITED from TEXT FIELD
  (components/text-field.md): the field-level Inline Message IS the
  helper/error slot Text Field already established — wired to the control
  via aria-describedby, with aria-invalid on the field, and the
  helper-text/error-text-share-the-slot model. The field-level Inline
  Message is the PRIMITIVE that form fields (Text Field, Textarea, Select,
  Checkbox group, etc.) compose. Don't re-derive the describedby chain —
  reference it and resolve the "Inline Message is the primitive / fields
  compose it" relationship.
- THE LIVE-REGION ANNOUNCEMENT PATTERN + the STATIC-vs-DYNAMIC refinement
  are INHERITED from TOAST and BANNER (components/toast.md,
  components/banner.md): role=status/alert + the rule that a message
  present at load is read in order while a dynamically-inserted one is a
  live region. Don't re-derive — reference and resolve the field-specific
  announcement question (below).
- THE SEVERITY ICON inherits ICON (components/icon.md); INLINE/SUMMARY
  LINKS inherit LINK (components/link.md).
It FORWARD-REFERENCES the siblings: Banner (the section/page boundary —
see components/banner.md; the inline variant is the bridge), Toast (the
transient boundary — see components/toast.md), and the form controls that
compose it (text-field, textarea, select, checkbox, radio).

THE DEFINING INLINE-MESSAGE-SPECIFIC SUBSTANCE to resolve and go deep on:
- THE FIELD-LEVEL vs SECTION-LEVEL SCOPE (the headline): a FIELD-LEVEL
  inline message is attached to a single control (the validation/helper
  text below an input — this IS Text Field's error/helper slot, and Inline
  Message is the primitive the fields compose); a SECTION-LEVEL inline
  message is scoped to a fieldset / a group of fields / a form section
  (smaller and lighter than a page Banner, stripped of heavy fill — the
  Spectrum-InlineAlert / Banner-inline boundary). Resolve the two scopes
  and the "fields compose the field-level primitive" relationship.
- THE ANNOUNCEMENT MODEL (the accessibility crux, and the contested point):
  how is a field error announced to a screen reader? Resolve the three
  patterns and their trade-offs — (1) aria-describedby on the field
  (announced when the field receives focus), (2) a live region
  (role=alert/status on the message, announced when it appears), (3) BOTH
  (and the double-announcement risk). Resolve the practice's default
  (describedby for the association + a live region only for the dynamic
  appearance, avoiding the double-announce) and the aria-invalid wiring.
- VALIDATION TIMING — when does the message appear? on-submit vs on-blur
  vs on-change (live/as-you-type); the eager-vs-lazy validation question
  (don't error a field the user hasn't finished / hasn't touched);
  reward-early/punish-late; and re-validation on correction. Resolve the
  practice's default timing.
- THE ERROR-SUMMARY PATTERN (the form-level accessibility pattern, GOV.UK
  canonical): a focusable summary at the top of a form listing all errors,
  each a link that moves focus to the offending field; focus moves to the
  summary on submit-with-errors. Resolve when an error summary is required
  (long/complex forms) and how it composes with the per-field messages.
- SEVERITY + HELPER-vs-ERROR — error (the dominant case) / warning /
  success ("looks good") / informational helper; the helper-text-and-
  error-text-share-the-slot model (inherited from Text Field — helper
  replaced by error, or both); color-not-sole-carrier (icon + text).
- THE STATIC-vs-DYNAMIC REFINEMENT (inherited from Banner) applied to
  fields — a server-rendered error present at page load (read in order)
  vs a client-validation error inserted on blur/submit (a live region).
- PLACEMENT + LAYOUT SHIFT — directly below/adjacent to the field
  (field-level) or above the section (section-level); the
  reserve-space-to-avoid-jump trap (an error appearing must not shove the
  form content down and disorient the user).
- THE BOUNDARIES — Inline Message (field/section, contextual, tied to a
  state, NOT user-dismissible) vs Banner (section/page, standalone,
  dismissible) vs Toast (transient) vs the bare field helper text.

Field-leader systems to survey (web): GOV.UK Design System (the Error
message + Error summary — the canonical accessible form-validation
pattern), Shopify Polaris (InlineError), IBM Carbon (form requirement /
inline notification + the field invalid/warn states), Adobe Spectrum (the
field error / HelpText / InlineAlert), GitHub Primer (FormControl
validation), MUI (FormHelperText + error), Microsoft Fluent (Field +
validationMessage/validationState), Atlassian (the Form field error /
HelperMessage/ErrorMessage), Ant Design (Form.Item help + validateStatus),
Google Material 3 (text field supporting text + error). WAI-ARIA APG (no
formal "inline message" pattern — the aria-describedby/aria-invalid field
association + the Alert pattern + live regions). WCAG 3.3.1 (Error
Identification), 3.3.3 (Error Suggestion), 4.1.3 (Status Messages), 1.4.1.
Mobile reference where relevant. Cite each with a version date.

Follow the 15-section spine and the locked key order/conventions in
components/_schema.md (identity, description, [anatomy], api, states,
variants, accessibility, content, [motion], [i18n], [implementation],
composition, notes; use inherits: for the Text Field describedby/invalid
chain, the Toast/Banner live-region pattern, the Icon severity, and the
Link summary/inline links; flag unverified claims under notes.unverified).

1. Framing — what it is (the field/section contextual message, the
   primitive form fields compose) and what it isn't (a standalone Banner /
   a transient Toast); the field-vs-section scope + the announcement-model
   realities up front; why systems disagree.
2. Anatomy and parts — the severity icon, the message text, optional
   inline/summary links; the field-association wiring; the (no) dismiss.
3. Properties / API — severity/validationState, message/children, the
   field-association (id/aria-describedby/aria-invalid, usually wired by
   the field), the live-region role (static vs dynamic), the error-summary
   composition.
4. States and variants — error/warning/success/info(helper); field-level
   vs section-level; with-icon; the helper↔error slot swap; the error
   summary.
5. Usage guidance — Inline Message (field/section, contextual) vs Banner
   (standalone, dismissible, page/section) vs Toast (transient) vs bare
   helper; validation-timing guidance (on-blur/submit, reward-early/
   punish-late); when an error summary is required.
6. Accessibility — the announcement model (aria-describedby vs live region
   vs both + the double-announce), aria-invalid, the error-summary +
   focus-on-submit, validation timing, static-vs-dynamic, color-not-sole-
   carrier, WCAG 3.3.1/3.3.3/4.1.3, WCAG SCs.
7. Content guidelines — specific + actionable error text (what + how to
   fix, not "Invalid"), positive validation, the helper, severity tone,
   no blame.
8. Motion and transition — minimal (appearance + the reserve-space/
   layout-shift consideration), reduce-motion.
9. Internationalization — RTL (icon side flip), text expansion (errors
   wrap), the error-summary order.
10. Naming — Inline Message / InlineError / HelpText / FormHelperText /
    ErrorMessage / FieldError / validationMessage; the practice's default;
    aliases.
11. Implementation notes — the field-association wiring (the field owns
    describedby/invalid; Inline Message is the rendered message), the
    static-vs-dynamic live region, validation timing + re-validation, the
    error-summary (focus management on submit), reserve-space for layout
    shift, headless vs opinionated.
12. Related and alternative components — typed relationships (Text Field
    et al. compose the field-level primitive, Banner section/page boundary
    + the inherited live-region pattern, Toast transient boundary, Icon
    severity, Link summary links, the Form composite).
13. Field POV evolution — recent shifts (the describedby-vs-live-region
    settling, the error-summary pattern spreading, reward-early/punish-late
    validation timing, the static-vs-dynamic clarification).
14. Sources cited — with version dates.
15. Agent-consumable schema — conformant to components/_schema.md.

Output: structured markdown, H2 headings matching the spine. Synthesize;
where decisions are context-dependent give frameworks, not winners; date
current-platform-state claims and note the verification path.

Depth: expert audience. Do not explain what an inline message is — explain
the field-vs-section scope (and that the field-level case IS Text Field's
error/helper slot, the primitive fields compose), the announcement model
(aria-describedby vs live region vs both + the double-announce risk + the
aria-invalid wiring), the validation-timing decision (on-blur/submit,
reward-early/punish-late), the error-summary pattern (GOV.UK, focus-on-
submit), the static-vs-dynamic refinement applied to fields, and the
Inline-Message-vs-Banner-vs-Toast-vs-bare-helper boundaries that field
leaders still diverge on.

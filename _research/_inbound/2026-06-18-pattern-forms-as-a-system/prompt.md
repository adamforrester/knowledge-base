You are advising a senior design systems practitioner at a digital agency
who maintains a personal knowledge base of design-systems field-truth. The
knowledge base has a ~45-component catalogue (each a field-truth brief: how
the leading systems handle a component, where they converge/diverge, the
practice's opinionated default) and is now opening a PATTERNS layer above it.

This is the FIRST pattern brief: **Forms-as-a-system**. A pattern is not a
component — it is an opinionated, goal-contextual COMPOSITION of components
that owns the orchestration no single component can. The boundary the
practice draws: **Form is the component** (the `<form>` primitive + single-
form validation orchestration, already briefed in the catalogue);
**Forms-as-a-system is the pattern** — the multi-field, multi-section form as
a SYSTEM: how it is structured, how fields depend on each other, how
validation is orchestrated across fields and time, how progress is saved, and
when a long form should instead become a multi-step wizard. Tier:
`composition`. Goal facet: `ask-for-data`.

Do NOT re-derive the Form component or the individual controls (Text Field,
Select, Checkbox, Radio Group, Date Picker) — assume those are briefed.
Document the DELTA the system adds: the cross-component orchestration and the
decision rules. This is field-truth synthesis, not a tutorial. Assume the
reader has shipped multiple design systems and knows what a form is. Explain
the non-obvious — where leading systems genuinely disagree, and what the
defensible default is.

=== WHAT TO SURVEY (the field) ===

Resolve how these sources actually handle the multi-field form as a system,
and where they diverge. Cite each with a version date and note the
verification path for current-state claims:
- Design systems: IBM Carbon (Forms pattern), Shopify Polaris (form layout +
  error patterns), Material Design 3 (text fields + form guidance), Atlassian
  (Forms pattern + the `@atlaskit/form` model), GOV.UK Design System ("Ask
  users for…", "Check your answers", "Question pages", one-thing-per-page),
  Microsoft Fluent, Adobe Spectrum, Ant Design (Form + ProForm).
- Form-logic lineage: the controlled-vs-uncontrolled model; React Hook Form,
  Formik, TanStack Form, Final Form — what they reveal about field
  dependency, validation timing, and array/repeatable fields.
- Standards: WCAG 2.2 (3.3.x error identification/suggestion/prevention,
  4.1.3 status messages), WAI-ARIA APG, the HTML form-validation + autofill
  (`autocomplete` tokens) substrate.

=== WHAT TO RESOLVE (the decision rules are the deliverable) ===

A pattern earns its keep in its DECISION RULES — the contested forks, given
as frameworks not winners, and made machine-resolvable (`IF condition → USE
resolution`) wherever a rule genuinely has a threshold. Resolve at least:

1. **Validation timing** — on-submit vs on-blur vs on-change vs hybrid; the
   "validate late, re-validate early" convention (don't error a field the
   user hasn't finished, but once errored, re-check on change); when each is
   right. The single most-debated form decision — resolve it with conditions.
2. **Error presentation** — inline-per-field vs an error summary at top vs
   both; the GOV.UK error-summary + anchor-link model vs the inline-only
   model; focus management on submit-with-errors (focus the summary? the
   first invalid field?); the live-region/`aria-describedby` contract.
3. **Required vs optional** — mark which? (the "mark optional, not required"
   argument vs the asterisk convention); when each holds.
4. **The long-form-vs-wizard threshold** — when does a long single form
   become a multi-step wizard, and when should it instead be one-thing-per-
   page (GOV.UK) vs a sectioned single scroll? Give the decision axes (field
   count, branching, error rate, completion context, save needs).
5. **Field dependency & conditional reveal** — progressive disclosure of
   fields, the "reveal on selection" pattern, the show/hide vs disable
   choice, focus/scroll behaviour on reveal, the a11y of dynamically
   inserted fields.
6. **Cross-field validation** — fields whose validity depends on other
   fields (password confirm, date ranges, "at least one of"), where the
   error lives, when it fires.
7. **Save model** — explicit-submit vs autosave vs save-and-resume/draft;
   the dirty-state/unsaved-changes guard; when a form needs persistence.
   (Note the boundary: full autosave/unsaved-changes is its own pattern —
   here, resolve only the part intrinsic to the form system.)
8. **Layout** — single-column-by-default (and the evidence for it),
   label placement (top vs left), grouping/sections/fieldset+legend, when
   multi-column is defensible, the responsive collapse.
9. **Repeatable / array fields** — add/remove rows, the "add another"
   model, reordering, the a11y of dynamic row insertion.
10. **Submission states** — the submit button's pending/disabled state (the
    never-disable-submit-pre-validation argument vs disable-while-pending),
    double-submit prevention, success/failure feedback, partial-failure.

=== THE BOUNDARIES TO HOLD ===

State explicitly, in a Related section:
- **Form (component) vs Forms-as-a-system (pattern)** — what stays in the
  component brief vs what this pattern owns.
- **Forms-as-a-system vs Multi-step wizard (pattern)** — the threshold where
  one becomes the other; this pattern's flow sibling.
- **Forms-as-a-system vs the data-collection "Ask users for X" recipes** —
  this pattern is the orchestration shell; the per-datum field recipes
  (address, name, date-of-birth, payment) are a sibling `composition`
  pattern. Don't absorb them; reference the boundary.
- What belongs in Foundations, not here (e.g. the bare disabled/read-only
  state rules, theming).

=== OUTPUT — follow this pattern-brief spine ===

Structured markdown. ALWAYS sections appear; SCALES appear when they carry
weight (they do, for this pattern). Order = reading order.
1. **Frontmatter** — YAML: type: pattern-brief, title, description, tags,
   tier: composition, goal: ask-for-data, status, timestamp.
2. **`# Forms-as-a-system` H1 + a one-paragraph blockquote** framing the
   problem and the boundary it holds.
3. **Problem & context** — the recurring problem; when it applies / doesn't;
   why systems diverge.
4. **Composition** — the components this assembles as typed references (Form,
   Text Field, Select, Checkbox, Radio Group, Date Picker, Button, Inline
   Message…); how they fit; the DELTA the system adds. Don't re-derive them.
5. **Decision rules** — the heart. The forks above, as machine-resolvable
   `IF → USE` rules where possible, prose for the genuinely-it-depends axes.
6. **Flow & states** (SCALES) — the form lifecycle: pristine → editing →
   validating → submitting → success/error; the state machine.
7. **Layout & structure** (SCALES) — single-column, sections, label
   placement, responsive.
8. **Accessibility orchestration** — the cross-component a11y the SYSTEM owns
   (not each control's own a11y): the error-summary focus contract, the
   live-region budget across fields, the fieldset/legend/heading structure,
   keyboard flow, the dynamic-field-insertion announcement.
9. **Content & copy** (near-ALWAYS here) — error-message voice and
   specificity, label/help/placeholder discipline, the required/optional
   wording, success copy.
10. **Variants & responsive** (SCALES) — single-scroll vs sectioned vs
    wizard; the responsive transforms.
11. **Anti-patterns** — the recurring traps (placeholder-as-label,
    disabled-submit-hiding-errors, on-change-validation-thrash, reset
    buttons, multi-column-by-default, validation-on-every-keystroke…).
12. **Related patterns & components** — the typed relationships and the four
    boundaries above.
13. **Field POV evolution** (SCALES) — how the field's answer has shifted
    (e.g. the move away from disabled submit; inline → summary+inline; the
    rise of schema-driven forms).
14. **Reference instantiations** (SCALES) — which systems to go look at and
    where (Carbon Forms, GOV.UK question pages + check-answers, Atlaskit
    Form).
15. **Sources cited** — with version dates; flag any claim lacking a solid
    source as unverified rather than inventing a citation.
16. **Agent-consumable schema** — a fenced YAML block: identity (id, name,
    aliases, tier, goal, status), problem, composition (requires: [typed
    component ids]), decision_rules (as `{ if, use }` where resolvable),
    flow, accessibility_orchestration, content, variants, anti_patterns,
    reference_instantiations, relations (composes / relates-to / boundary),
    notes (contested / unverified / secondary-tier).

Synthesize; give frameworks where context decides, defaults where the field
has genuinely converged. Be opinionated and declarative — the practice has a
POV. Flag contested claims and anything you can't source. Date current-state
platform claims.

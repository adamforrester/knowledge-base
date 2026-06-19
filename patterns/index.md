---
okf_version: "0.1"
type: practice-area
title: Pattern Briefs
description: Field-truth studies of cross-component patterns — the recurring compositions of components that solve a problem (Forms-as-a-system, Filtering, wizards, app shells, page templates). The patterns layer sits above the component catalogue: a component is a thing with props; a pattern is a way of composing things, resolved as decision rules. Upstream of an engagement's pattern library and the practice's POV on composition (03).
tags: [index, patterns]
timestamp: 2026-06-18
---

# Pattern Briefs

A catalogue of cross-component **pattern** briefs. Where the component catalogue (`components/`) studies individual things — a Button, a Form — the patterns layer studies the recurring *compositions* of those things: how the leading systems assemble components to solve a problem, where they converge, where they diverge, and the decision rules the practice lands on. A pattern is mostly decisions and orchestration, not markup; it composes briefed components and records only the delta.

The patterns layer opened once the component catalogue reached the point where whole categories had closed and components were forward-referencing assemblies no single brief could own — the Form brief's "Forms-as-a-system" hand-off being the trigger.

---

## How this layer works

**Relationship to the catalogue.** A pattern names the components it composes as typed references into `components/` and never re-derives them. The pattern-vs-component boundary is **opinionation, not packaging**: a component is goal-agnostic (a `Form`, a `Button`); a pattern is an opinionated resolution to a *user goal* that owns the cross-component orchestration no single component can — *Forms-as-a-system* (the multi-step wizard, save-and-resume) is the pattern, `Form` is the component it composes. A pattern can ship as a macro-component (`ProForm`, a `<Wizard>`, a shipped `AppShell`) and still be a pattern; the brief documents the decisions regardless. Where the catalogue already briefs a thing (Empty State, Table, the Search field), the pattern is the *orchestration around it*, never a re-brief. See `_schema.md` for the full boundary.

**Brief shape.** Patterns follow the flexible spine in `_schema.md` — a small ALWAYS core (problem, composition, decision rules, accessibility orchestration, anti-patterns, related, schema) plus SCALES sections (flow & states, layout & structure, content, variants, reference instantiations) that appear only when the pattern's tier gives them weight. Unlike the component spine (a locked key set), the pattern spine bends to the tier. Voice and depth match the catalogue and the numbered files.

**The three tiers + a goal facet.** Every pattern declares a `tier`, which predicts its shape — `composition` (a spatial recipe; composition/decision-heavy), `flow` (a temporal journey; flow/content-heavy), `layout-and-shell` (a structural archetype; layout-heavy) — and a `goal`, the GOV.UK-style user intent (`ask-for-data`, `help-user-decide`, `navigate`, `show-data`, `recover-from-error`) that makes a pattern findable by *what the user is trying to do*, not only by its shape. The goal facet is what the planned MCP `list_patterns()` index surfaces. **State conventions are not a tier:** cross-cutting rules for expressing a state or system property (disabled, read-only, theming/dark-mode, i18n/RTL) are **Foundations guidance** and live in the numbered files (00–10+), not here; only genuine cross-region *orchestration* (loading/empty/error across a view, notification routing) is a `composition` pattern. See `_schema.md`.

**Research workflow.** Patterns use the `_research/` dual-agent workspace — the same flow as the catalogue (a prompt run against two agents, synthesized to `patterns/<slug>.md`). Dual-agent is the default; patterns are contested by nature. The run folder is `_research/_inbound/YYYY-MM-DD-pattern-<slug>/`.

**Promotion.** When a pattern lands: flip its entry below from a `scope:` stub to a link + one-line hook + status; add inline cross-references from the component briefs and numbered files where the pattern is now relevant.

---

## The catalogue

The seed list spans the three tiers. It was validated against a meta-research run surveying how the leading systems structure their pattern libraries (see `_research/_inbound/2026-06-18-pattern-library-structure/`). The list is the discipline; engagement need pulls a pattern forward. Patterns without briefs carry a `scope:` note; each carries its `goal` facet.

A **prioritised author order** opens the layer (highest field-attestation × spine coverage first): **(1) Forms-as-a-system** — the trigger, exercises the most of the spine; **(2) View-state orchestration** — low-complexity, high-impact, validates the orchestration-as-`composition` call; **(3) the data-collection "Ask users for X" family** — highest field-attestation, validates the `goal` facet; **(4) Search orchestration**; **(5) App shell**; **(6) Destructive confirmation**; **(7) Master-detail**. The rest follow as engagements pull them.

### Composition — spatial recipes

- **Forms-as-a-system** — *briefed (the patterns layer's first run) — see `patterns/forms-as-a-system.md`.* The multi-field form as a system: reward-early/punish-late validation timing, the dual inline + error-summary model and its focus contract, mark-the-minority required/optional, the sectioned/one-per-page/wizard threshold, conditional reveal, cross-field validation, the save model, single-column layout, and the never-disable-submit contract. Composes Form + every control + Button + Inline Message; borders the multi-step wizard (flow), the "Ask users for X" recipes it composes, and the state/token rules in Foundations. `goal: ask-for-data.`
- **Data-collection recipes ("Ask users for X")** — *not yet briefed.* `goal: ask-for-data. scope: the GOV.UK "Ask users for…" family — address, name, date-of-birth, phone, email-with-confirmation, payment-card — the canonical field grouping, validation, and copy for each high-frequency datum. The field's most-reused, best-attested patterns. Composes Text Field/Form; the per-datum decision rules (one date field vs three, name parts).`
- **Filtering** — *not yet briefed.* `goal: show-data. scope: the filter set (controls applied without a submit) — inline vs panel vs drawer, applied-filter chips (Tag), the clear-all + result-count contract, faceted vs simple, URL/state persistence. Composes Combobox/Select/Checkbox/Tag/Button; the Form-vs-Filter-set boundary.`
- **Search orchestration** — *not yet briefed.* `goal: navigate. scope: the search experience around the Search field component — suggestions/typeahead, recent/scoped search, active-vs-focused states, the results + empty/no-results state, instant vs submit. Composes Combobox/Empty State/List; the field is the component, this is the orchestration.`
- **View-state orchestration (empty / loading / error)** — *not yet briefed.* `goal: recover-from-error. scope: coordinating a region's data states — the empty/first-use/no-results/loading/error matrix, skeleton vs spinner vs optimistic at view scale, staggered vs all-at-once, replacing the underlying layout (e.g. a Table) with state messaging. Composes Empty State/Spinner/Skeleton. (The cross-region orchestration the dissolved state-convention tier valued; the bare loading rule is Foundations.)`
- **Notification orchestration** — *not yet briefed.* `goal: recover-from-error. scope: the notification system — Toast vs Banner vs Inline vs a notification centre, priority/severity routing, the do-not-disturb/batching model, the live-region budget. Composes Toast/Banner/Inline Message.`
- **Action priority & overflow** — *not yet briefed.* `goal: help-user-act. scope: the action-priority model — primary/secondary/tertiary, the overflow menu, responsive action-collapse, destructive-action placement (the "Common actions" recipe Carbon names). Composes Button/Menu/Toolbar. NB: Toolbar itself is a missing component (see catalogue gap), not a pattern — this recipe is the priority/overflow logic above it.`
- **Bulk actions & selection** — *not yet briefed.* `goal: help-user-act. scope: list/table multi-select → a bulk-action bar — select-all/range/indeterminate, the contextual action bar, the count + clear contract, destructive bulk actions. Composes Checkbox/Table/Toolbar/Button.`
- **Inline edit** — *not yet briefed.* `goal: ask-for-data. scope: edit-in-place — the display↔edit toggle, save/cancel affordance, optimistic vs confirmed save, validation in place, edit-in-place vs edit-in-form. Composes Text Field/Button (Atlassian ships this as a pattern).`
- **Data visualization** — *not yet briefed.* `goal: show-data. scope: the charting layer — chart-archetype selection, categorical vs sequential colour mapping, the empty/loading chart, accessibility of data viz, the table-vs-chart decision. Borders Card/Dashboard. (May need its own depth; flag scope at brief time.)`
- **Comparison & pricing tables** — *not yet briefed.* `goal: help-user-decide. scope: the comparison archetype — feature-matrix layout, the recommended/highlighted column, responsive collapse, the dense-data legibility model. Composes Table/Card/Button.`

### Flow — temporal journeys

- **Destructive confirmation** — *not yet briefed.* `goal: help-user-act. scope: confirming irreversible actions — the confirmation dialog (alertdialog), type-to-confirm, the undo-instead-of-confirm alternative, the inline-alert-vs-modal threshold, the never-autofocus-destructive rule. Composes Dialog/Button; the Toast undo lineage.`
- **Multi-step wizard** — *not yet briefed.* `goal: ask-for-data. scope: the segmented flow — the step model, progress indication (Stepper), per-step vs end validation, back/next/save-draft, the linear-vs-non-linear decision, the wizard→accordion responsive transform. Composes Form/Button/Progress; the Forms-as-a-system flow sibling.`
- **Check answers** — *not yet briefed.* `goal: help-user-decide. scope: the GOV.UK review-before-submit pattern — the answer-summary list, change-in-context links back to each step, the final-submit contract. Composes List/Link/Button; the wizard's terminal step.`
- **Login & authentication** — *not yet briefed.* `goal: help-user-act. scope: the auth flow — sign-in/sign-up/reset/MFA, the credential form, OAuth/passkey options, error/lockout states, the autofill/one-time-code contract. Composes Form/Text Field/Button.`
- **Eligibility / triage** — *not yet briefed.* `goal: help-user-decide. scope: the "check this service is suitable" up-front gate — branching pre-qualification questions, the early exit/redirect, preventing deep-transaction failure (GOV.UK). Composes Form/Radio Group; borders the wizard.`
- **Save & unsaved-changes** — *not yet briefed.* `goal: help-user-act. scope: the save model — explicit-save vs autosave, the dirty-state guard (beforeunload/route guard), save status feedback, draft persistence. Composes Form/Toast/Banner.`
- **Onboarding** — *not yet briefed.* `goal: navigate. scope: the first-run journey — empty-state-as-onboarding, product tours/coachmarks, progressive setup checklists, the skip/dismiss contract. Composes Empty State/Dialog/the wizard. (Reclassified from page-template: it's a journey, not a skeleton.)`
- **AI conversational flow** — *not yet briefed.* `goal: help-user-act. scope: the generative-AI interaction surface — inline/widget vs side-by-side workspace vs full chat, streaming/stop/regenerate, citation & confidence display, the human-in-the-loop confirm (Fluent's Experience Patterns). Composes Text Field/Button/the message surface. (Emerging; flag unverified at brief time.)`

### Layout & shell — structural archetypes

- **App shell / global header** — *not yet briefed.* `goal: navigate. scope: the application frame — the global header, the primary nav (Side Navigation), the content region, the responsive collapse, the skip-link + landmark structure. Composes Side Navigation/Link/Menu/Avatar; the substrate every other archetype sits in.`
- **Master–detail (list–detail)** — *not yet briefed.* `goal: show-data. scope: the list + detail archetype (M3's canonical list-detail) — split-view vs drill-down, the responsive stack, selection-to-detail, the deep-link/URL model. Composes List/Table + the detail region.`
- **Dashboard** — *not yet briefed.* `goal: show-data. scope: the dashboard archetype — the card/widget grid, the responsive reflow, the data-density/refresh model, the empty/loading dashboard. Composes Card/Grid; the data-viz boundary.`
- **Settings** — *not yet briefed.* `goal: help-user-act. scope: the settings archetype — the sectioned settings page, immediate-save vs form-submit, the settings-row (label-leading Switch), nav-within-settings. Composes Form/Switch/Side Navigation.`
- **Error pages** — *not yet briefed.* `goal: recover-from-error. scope: the full-page error archetype — 404/500/403/offline, the recovery action, the empty-state lineage at page scale, the don't-blame voice. Composes Empty State/Button/Link.`
- **Feed & supporting-pane layouts** — *not yet briefed.* `goal: show-data. scope: two M3 canonical layouts — the feed (continuous-scroll consumption grid) and the supporting pane (primary content + secondary contextual pane). The responsive pane behaviour and breakpoint math. Composes Card/List/Grid.`

### Not patterns — exiled to Foundations (numbered files)

Cross-cutting rules a component obeys, not compositions that orchestrate components. Brief these (or cite them) from the numbered files, **not** here:

- **Disabled / Read-only semantics** — a global state rule each control obeys; belongs with the component model POV (03) / accessibility. (The *orchestration* of empty/loading/error across a view is a `composition` pattern — see View-state orchestration above — but the bare state rule is not.)
- **Theming / dark-mode** — a token-layer concern; foundations, not a pattern.
- **Internationalisation / RTL** — already the practice's `13-internationalization`; layout-direction rules are global, not a discrete pattern.
- **Responsive / adaptive layout philosophy** — global breakpoint/grid POV; the *specific* adaptive transforms (master-detail stacks on mobile) live in each archetype's variants section, not as a standalone pattern.

Borderline, leaning component (build in `components/`, not here): **Toolbar**, **Pagination** (the control; the pagination-vs-infinite-scroll *choice* is a decision rule inside the data patterns), **Command palette** (increasingly a single-import macro-component — revisit as a `composition` pattern only if the orchestration POV outgrows the component brief), **Comment thread / activity feed** (typically composite components).

---

## Provenance

The patterns layer and this index were opened after the component catalogue closed its seventh category (Form). The flexible spine is defined in `_schema.md`; **Forms-as-a-system** is the first worked example, chosen because the Form component explicitly forward-referenced it as the pattern boundary. See `03-component-library` for the practice's POV on the component model the patterns compose, and `CLAUDE.md` for the vault conventions.
